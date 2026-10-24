# Analysis — M6.P2 T9, build supervision and host maintenance (#656)

Phase 4. Every line number is `8ebaf8daad`'s (the export `.qa-scratch/t9/at-hash/`).

## Executive summary

The 18 files are the fork's own build supervision: the runner every build enters, the status file, the durable launcher, the admission guard with its retention report, the root-owned swap helper with its installer, the preflight, the release preparer and the old disk-move tool.

The guards are carefully built. Most of them construct their refusals in controls that pass today: 37 swap tests, 68 admission checks, 36 monitor checks, 32 watcher checks and 19 retention controls. The recorded runs agree with the watcher's contract: 1,885 runs, every status `finished`.

**The slice's lead finding is about the controls rather than the tools (F-01).** The admission guard of 2026-10-13 made the runner refuse unadmitted runs, and three recorded controls broke without notice: the progress control (blindspot 73's), the routing fixture and the submission control. Their fixtures lack the admission module, and past that their payloads carry no admission.

**Beside it**, as graded after the second opinion (`§ Second opinion`):
- **Medium:**
  - **F-03:** `--stop-vms` stops guests by `pgrep -f` pattern and a plain `kill` (with G-47, G-48), on a host two lanes share.
  - **F-04:** Python 3.11 against the container's 3.10 on the docker-shell route.
  - **F-07:** the lock does not exclude a second build beside an orphaned command.
  - **F-08:** guards with no control, expanded to 73 rows with five corrected.
  - **F-10:** the disk-move tool, whose header names the OS disk.
  - **F-12:** two clones' admission registries on one volume.
  - **F-13:** the installer's trust in a writable checkout, a lead.
- **Low:**
  - **F-05:** an unreadable PID becomes `died`.
  - **F-06:** the runner's end-of-run and I/O-failure paths.
  - **F-14:** the report's plan hash and freshness.
  - **F-15:** the retention control's host dependence.
  - **F-16:** `consume`'s row trust and commit order.
  - **F-17:** the helper's unhandled signals.
  - **F-18:** `watch-job`'s argument hygiene.
  - **F-19:** the launcher's receipts.
  - **F-20:** the release preparer's seams.
- **Leads and rows:**
  - **F-21:** the admission's operational-guard boundaries, a lead.
  - **F-09:** #640's rows.
- **Withdrawn:** F-11.

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

- **Shared host state is what these tools mutate.** `--stop-vms` ends any same-UID guest (F-03); `reclaim-swap` turns swap off and on (F-17 for its unhandled signals); `install` writes root's sudo policy from a user-writable checkout (F-13); `fork-newdrive` moves the worktrees and edits `fstab` (F-10).
- **The broken controls (F-01)** mean a regression in progress reporting, routing or submission would pass the fork CI.
- **F-07 is an exclusion failure,** not only a reporting gap: after an outright kill, a second build can mutate the same worktree beside an orphaned one. F-12 lets two clones' admissions count the same free bytes. F-04 and F-06 fail closed (no payload starts; the reservation is held).

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

- **Medium:**
  - **F-01:** three recorded controls broken since 2026-10-13 (P10).
  - **F-03:** `--stop-vms` stops any same-UID guest by pattern; a failed census reads as none.
  - **F-04:** `AttributeError` on the docker-shell admitted path.
  - **F-07:** the worktree lock does not cover an orphaned command.
  - **F-12:** admission reservations split across two clones on one volume.
- **Low:**
  - **F-02:** `test-submit.py` leaks a directory under `/tmp` on every run.
  - **F-05:** an unreadable PID reported as `died`.
  - **F-06:** the runner's late-watcher, I/O-failure, cancellation and backpressure paths.
  - **F-14:** `retention-report`'s plan hash and freshness.
  - **F-15:** the retention control's host dependence.
  - **F-16:** `consume`'s row trust and commit order.
  - **F-17:** the helper's unhandled terminating signals.
  - **F-18:** `watch-job`'s argument hygiene.
  - **F-19:** the launcher's receipts.
  - **F-20:** the release preparer's seams.
- **A lead (the installer's contract):** F-13, Medium.

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
| 14 | `watch-build` | one top-level build per worktree (`:102-106`) | `test-build-monitor` "one top-level build per worktree" (`:219-226`); **the second launch reuses the first's admission, so with the lock removed the reuse refusal would still pass it: the lock is not isolated** (the seat's refutation, § Second opinion) | partial |
| 15 | `watch-build` | an admission is required (`:96-98`) | `test-build-admission` "missing receipt blocks payload" | yes |
| 16 | `watch-build` | a stale inherited marker is refused (`:41-42`) | none: "stale inherited marker cannot bypass monitoring" names a *missing* run (`test-build-monitor:190-195`), refused at the status read (`:36`), not at the heartbeat age | -- |
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
| 29 | `build-admission` | single use (`:200`) | "consumed admission cannot launch twice" (`test-build-admission:59`): the second launch precedes consumption (`:83`); the membership check it exercises is the same one, so the guard is covered and the label is not | yes |
| 30 | `build-admission` | capacity at preparation and at launch, less reservations (`:166-168`, `:202-204`) | "prepare refuses insufficient current capacity", "launch rechecks capacity after preparation", "existing unresolved reservations reduce new capacity" | yes |
| 31 | `build-admission` | changed plan, source, measurement, protected input, profile or registry (`:104-159`, `:183-201`); a report with inventory errors (`:113`) | the seven "changed ... blocks payload" cases and "refused report blocks payload" (`test-build-admission:28-32`) | yes |
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
| 51 | `reclaim-swap` | the memory refusal, if removed (`README.md:99`) | `test_insufficient_memory_and_boundary` (`test-swap-reclaim:199-206`) fails without it; the 2026-10-04 mutation run (work log `:241`) proved that once | yes |
| 52 | `install` | sudoers order and later files (`:67-79`) | `test_rule_order_refuses_later_files_or_main_directives` | yes |
| 53 | `install` | the include required (`:59-64`) | `test_policy_directory_must_be_included`, `test_real_visudo_rejects_unowned_include_directory` | yes |
| 54 | `install` | the exact policy line (`:20-26`) | `test_policy_is_exact_action_with_hash_receipt_and_valid_sudoers` | yes |
| 55 | `install` | non-root refused (`:83-84`) | `test_unprivileged_installation_cannot_write` | yes |
| 56 | `install` | validation rollback of both files (`:123-151`) | `test_policy_validation_failure_rolls_back_both_files`, `test_failed_policy_restore_still_restores_helper_and_cleans_temps` | yes |
| 57 | `install` | legacy migration only if unchanged (`:101-102`) | `test_migrate_only_unchanged_legacy_policy` | yes |
| 58 | `install` | host and account (`:85-88`) and `secure()` of paths (`:29-35`, `:89-94`) | none: patched to pass in every test (F-08) | -- |
| 59 | `retention-report` | `evaluate()`'s refusals (`:207-265`) | `test-retention-report`'s 19 controls: **four positives and fifteen refusals**; not host-isolated, it reads the real `/proc` and `docker ps` (F-15) | yes, host-dependent |
| 60 | `build-preflight` | default read-only, opt-in helper, missing helper, inactive swap, bad observations and options (`:36-99`) | `test-swap-reclaim` `Preflight`'s six tests | yes |
| 61 | `build-preflight` | `--stop-vms` (`:101-119`) | none: only the combination refusal (`:368-369`) (F-03, F-08) | -- |
| 62 | `fork-publish-release` | the plan checks (`:21-125`) | `tools/build-identity-test:104-167` (outside the slice) | yes, by its own run |
| 63 | `fork-newdrive` | system-disk, mounted-disk and existing-`fstab` refusals (`:94-112`) | none (F-08); a one-time tool run by hand | -- |

**Rows the seat added** (a wired guard with no control, each part of F-08):

| # | Tool | Guard (where) | Control | Running |
| --- | --- | --- | --- | --- |
| 64 | `watch-build` | argument checks: command, interval, stall, `--recursive-activity`, `--activity-dir` (`:76-81`) | none | -- |
| 65 | `watch-build-submit` | an existing owner and an executable runner (`:63-66`) | `test-submit.py` (broken, F-01) | **no** |
| 66 | `build-admission` | path identity, registry owner and schema, report expiry, volume, outputs, budget and profile shape (`:60-67`, `:84-101`, `:117-152`) | none named | -- |
| 67 | `build-admission` | `consume`'s launcher, result and group checks (`:250-274`) | in part, through row 37's cases | partial |
| 68 | `build-admission` | the recovery census parsers (`:290-321`) | none: the tests replace them (`test-build-admission:148`) | -- |
| 69 | `build-admission` | the retention report's plan and tool digests (`:114-116`) | none | -- |
| 70 | `reclaim-swap` | minimum swapfile size, changed configuration, unsafe lock metadata (`:106-107`, `:152-154`, `:205-207`) | none named | -- |
| 71 | `install` | arguments, source shebang and syntax, its lock, the final byte and mode check (`:120`, `:162-178`) | none | -- |
| 72 | `retention-report` | roots, stores, duplicate candidates, oversized manifests, container failure, budgets (`:78-90`, `:165-166`, `:191-198`, `:277-285`) | in part | partial |
| 73 | `fork-newdrive` | block device, primary checkout, UUID and confirmation (`:84-85`, `:105-106`, `:123-124`) | none | -- |

**Rows with no running control:** 12, 27 and 65 (F-01); 13, 16, 17, 19, 25, 26, 33 to 36, 58, 61, 63, 64, 66, 68 to 71 and 73 (F-08). Partial: 14, 67, 72. Host-dependent: 59 (F-15).

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

1. F-01, F-02, F-15: the controls repaired, isolated and put in the fork CI (a stream).
2. F-03: `--stop-vms` through `tools/vm-stop` or removed (its contract is the coordinator's).
3. F-04, F-05, F-06, F-07, F-12, F-14, F-16 to F-19: bugs, each with its control at stage E.
4. F-08: a control per `none` row, beside its stream or as one Renovation stream.
5. F-09, F-10: #640, and the coordinator's call on retiring `fork-newdrive`.
6. F-13, F-20, F-21: leads for the coordinator (contracts and an outside store).

## Quality Self-Check

- Every finding cites a line at the hash and was re-read before it was written.
- Each `none` in the guard table came from a text search and the named checks, not from the absence of a match alone. Row 58's `none` was confirmed by reading the patches.
- No guard was run against the host; F-04's container fact is history.
- The counts in `02`, P1 to P9, and this file agree.

## Second opinion (Phase 4.6)

**One seat, GPT-6 Astra at `max`, through the Facilitator** (D-WORKFLOW-184, `review-plan.json`).
- **The probe** at 16:01 passed: served `openai/gpt-6-astra`, identity from the provider's response, provider OpenAI, effort `max`, 302 reasoning tokens.
- **The refutation** ran 16:02:33 to 16:22:33 over the packet (295,270 bytes, sha256 `4e15670d…`, equal to the provenance's `user_prompt_sha256`):
  - one attempt, http 200, served `openai/gpt-6-astra` by OpenAI, effort `max`;
  - 44,956 reasoning tokens, 51,800 completion tokens, `outcome=success`, 1,200 s;
  - USD 3.59458; output `gpt-audit.md`, 30,928 bytes.
- Every item below was read at its site in `.qa-scratch/t9/at-hash/` before it was graded.

### The seat's new items

| G | Seat | Grade | Decided by | Lands in |
| --- | --- | --- | --- | --- |
| G-01 | Medium | **Narrowed, no item.** The busy check reads names, so a renamed process evades it. The helper guards against accidental builds, not disguised ones, and real compilers run under `make`, `ninja` or a `*-gcc` name, which it catches. | `reclaim-swap:83-100`; `README.md:11-12` | -- |
| G-02 | Medium | **Narrowed, no item.** PID 1 `systemd` inside a container would pass, but the helper is reached through host `sudo`, not from a container. | `reclaim-swap:81-82`; the sudo rule | -- |
| G-03 | Medium | **Confirmed in part, Low.** The race with new work is documented ("snapshots, not reservations", `README.md:24`). New: the flushed `print` at `:161` sits between the last check and `swapoff`, so a blocked stdout can stall the mutation past its checks. | `reclaim-swap:157-163` | F-17 |
| G-04 | Medium | **Documented, no item.** The helper is scoped to the reviewed default activation and says so; restoring other flags is out of its contract. | `reclaim-swap:111-113`; `README.md:9-10` | -- |
| G-05 | Low | **Agreed, no item:** a concurrent-administrator seam. | `reclaim-swap:103-108` | -- |
| G-06 | Medium | **Confirmed, Low.** Only SIGINT, SIGTERM and SIGHUP are deferred. A SIGQUIT (Ctrl-\ from a terminal) during `swapoff` ends Python before `swapon`, leaving swap off. The next preflight then says `NO ACTIVE SWAP` and the README names the recovery, so it is loud, not silent. | `reclaim-swap:20`, `:162-184`; `build-preflight:88-92` | F-17 |
| G-07 | Medium | **Withdrawn.** A failed `swapon` raising to the administrator-recovery refusal is the designed fallback. | `reclaim-swap:180-182`; `README.md:88-93` | -- |
| G-08 | High | **Confirmed as a seam, narrowed to Medium.** The installer installs whatever helper bytes sit beside it in a user-writable checkout, as root, with no expected digest. On this host the writer is `max`, who already holds `(ALL : ALL) ALL` with a password. What the seam adds is that any process running as `max`, such as an unattended agent, could plant a helper that later runs passwordless as root. The README's staging instruction (`:65-67`) is a procedure, not a check. A contract change, so a lead for the coordinator (D-INFRA-015 is the owner's). | `install:160-168`; brief § 1 (the fleet rule) | F-13 |
| G-09 | Low | **Withdrawn.** A passwordless `sudo -l` reveals policy; it grants no command. | `install:25-26` | -- |
| G-10 | Low | **Agreed, documented.** "An interrupted installation must be verified/reinstalled" (`README.md:68-69`). | `install:106-157` | F-13 |
| G-11 | Low | **Agreed.** My coverage row said the `assert` was safe "because `-O` is never passed". An administrator can run `python3 -O -I install`. Corrected in `02`. | `install:120` | F-13 |
| G-12 | Medium | **Confirmed, and real on this host.** Reservations live in the Git common directory (`:77-80`). `/workspace/repos/rocknix/.git` and `/workspace/repos/pixelelated/distribution/.git` are both on device 66304. The first holds `pixelelated-build-admission/` and the second has none, so an M6 admission would count against free bytes M7 has already reserved. | `build-admission:77-80`, `:165-168`; `stat` of both | **F-12** |
| G-13 | Medium | **Narrowed to a lead.** Single use rests on the registry's history inside `.git`. Deleting it is tampering, outside an operational guard's model (`build-admission.md:9-10`). | `:84-94` | F-21 |
| G-14 | Medium | **Narrowed to a lead,** the same class: a writable registry in the user's own `.git`. | `:84-94` | F-21 |
| G-15 | Medium | **Narrowed to a lead.** The inherited marker is a bearer token by design. `device-builds.md` forbids pre-setting it, and the tool refuses a stale or finished one. | `watch-build:31-47` | F-21 |
| G-16 | Low | **Agreed, documented.** `scripts/build:8` skips on `RASTERATOPS_WATCH_EXEC == $0`, which `device-builds.md` names as an internal marker, not an opt-out. | `scripts/build:7-10` | F-21 |
| G-17 | Medium | **Confirmed, Low.** `nested()` checks source and profile, not `BUILD_DIR` or the Docker mount. A nested entry can redirect output past the outer check. | `build-admission:220-226` | F-21 |
| G-18 | Medium | **Narrowed to a lead.** Output overlap across worktrees is not checked; the shared download cache is the known shared output (`device-builds.md`). | `:138-148` | F-21 |
| G-19 | Medium | **Narrowed to a lead.** Protected identities are metadata, not content, and untracked inputs are outside `source_state()`. That is the guard's declared scope (`build-admission.md:66-73`), and a content identity is a contract change. | `:60-74`, `:121-126` | F-21 |
| G-20 | Low | **Agreed, no item.** The guide calls it an operational guard over supplied evidence. | `build-admission.md:9-10` | -- |
| G-21 | Medium | **Narrowed to a lead.** Read-then-hash on separate opens; concurrent edits of the operator's own plan. | `:162-216` | F-21 |
| G-22 | Medium | **Confirmed, Low.** `consume` compares the registry row by `run` only (`:274`), while recovery compares the whole row (`:440`). An edited `admission.json` (a `submission_owner` removed) drops the launcher checks. | `:245-274`, `:440` | F-16 |
| G-23 | Medium | **Narrowed, no item.** Runner 0 with command 37 needs a forged `runner-result.json`: `watch-build` writes `finish(run, code, monitor_code, code)` (`:214`), runner equal to command. Its watcher-outcome point is F-16's row check. | `watch-build:212-214` | -- |
| G-24 | Medium | **Narrowed, no item.** An empty `cmdline` is a zombie or kernel thread, and a missing one means the PID directory is gone. Only a live process that blanks its own argv would read as exited, and none of these tools does. | `build-admission:234-239` | -- |
| G-25 | Medium | **Narrowed to a lead.** Custody covers the command's group, not escaped sessions; the guide's scope says "no root dependency visibility". | `:256-271`; `build-admission.md:108-110` | F-21 |
| G-26 | Medium | **Confirmed, Low.** `admission-consumed.json` is written inside the registry context before `jobs.json` commits on exit. If that commit fails, a retry fails on the exclusive receipt and cannot reconcile. | `:272-282`, `:93-94` | F-16 |
| G-27 | Medium | **Confirmed, Low.** If the log write fails (a full disk), the handler writes to the same log (`:191`) before killing the child (`:192-198`). A second failure skips the kill, and the payload outlives the runner. | `watch-build:176-198` | F-06 |
| G-28 | Medium | **Plausible, Low.** A connected console that does not drain blocks the runner's read loop and then the payload. The durable launcher writes to a file, so it does not meet this. | `watch-build:180-187`; `watch-build-submit:83-88` | F-06 |
| G-29 | Medium | **Narrowed, Low.** A watcher that dies early leaves its heartbeat stale, the designed signal (`watch-job:18-21`); the runner prevents a green result at the end. No check during the run is added by the design. | `watch-build:209-213` | F-06 |
| G-30 | Low | **Confirmed.** A signal during `admit()` sets `interrupted`, `Popen` still starts the command, and then forwards the signal. | `watch-build:153-170` | F-06 |
| G-31 | Medium | **Withdrawn.** Once the result file exists, the exit code is the outcome, and activity scanning is liveness only. A scan error at the moment of completion changes nothing a reader acts on. | `watch-job:225-235` | -- |
| G-32 | Low | **Agreed, no item.** These are display reads: `progress` and `tail` never decide a state. | `watch-job:212-216`, `:261-265` | -- |
| G-33 | Medium | **Narrowed, Low.** The overlap check resolves `STATUS` but writes `"$STATUS.pid"` and `.tmp` by name, so a pre-planted symlink in the private run directory could redirect a write. | `watch-job:112-127`, `:160`, `:266` | F-18 |
| G-34 | Low | **Confirmed.** `grep -E "$PATTERN"` without `--`: the pattern `--help` passes validation as grep's own help (rc 0). `mv` likewise takes a dash-leading status name as an option. | `watch-job:107-108`, `:216`, `:262`, `:266` | F-18 |
| G-35 | Low | **Agreed, no item.** Attach-time PID reuse is inherent to `--pid`. `watch-build` passes its own live PID. | `watch-build:132` | -- |
| G-36 | Medium | **Confirmed, Low.** The fresh-owner list omits `launcher-start.json`, `launcher-result.json` and `launcher-pid.json`. A partly restored owner can carry an old result, or fail in the worker after the parent announced submission. | `watch-build-submit:69-71`, `:32` | F-19 |
| G-37 | Medium | **Confirmed, Low.** The worker starts before `launcher-pid.json` is written exclusively, so a collision reports failure over a started build. | `:83-89` | F-19 |
| G-38 | Low | **Agreed.** A signal to the worker leaves the runner without launcher completion evidence, and `consume` then holds the reservation (fail closed). | `:30-50`; `build-admission:259-262` | F-19 |
| G-39 | Low | **Agreed, no item.** Recorded in `04` § Q7: `launcher-submission.json` hashes `watch-build` only. | `watch-build-submit:76` | -- |
| G-40 | Medium | **Confirmed, Low.** The plan is parsed before the scan (`:305`) and hashed after it (`:307`), so the report binds bytes it may not have read. | `retention-report:305-308` | F-14 |
| G-41 | Medium | **Confirmed. My `03` § 3.5 claim was wrong.** The report's `utc` is stamped at completion (`:293`), so the 900 s window starts after the scan, not before it. Corrected in `03`. | `retention-report:293`; `build-admission:117-118` | F-14 |
| G-42 | Medium | **Narrowed to a lead.** Containment is lexical over operator-supplied absolute paths; the plan is reviewed. | `:32-33` | F-21 |
| G-43 | Medium | **Narrowed to a lead,** the namespace class of F-05 and of `reclaim-swap`'s PID 1 check: the report does not record its PID view. | `:172-189` | F-21 |
| G-44 | Medium | **Narrowed to a lead.** Receipts are bound by hash to the evidence list, not to the candidate's run. | `:234-257` | F-21 |
| G-45 | Low | **Confirmed, Low.** `eligible_reclaim_bytes` sums candidates on any filesystem; a display figure, not counted as free space. | `:287` | F-14 |
| G-46 | Low | **Confirmed. My `03` § 3.2 claim was too broad.** `test-retention-report` calls the real `report()`, which reads the real `/proc` and runs `docker ps`. A live QEMU anywhere on the host would flip its four positive cases. Corrected in `03`. | `test-retention-report:37-43`; `retention-report:172-198` | F-15 |
| G-47 | Medium | **Confirmed, Low.** `pgrep` errors are discarded, so a failed census reads as no guests and the preflight can say READY. | `build-preflight:101` | F-03 |
| G-48 | Low | **Confirmed.** The preflight compares MB against a truncated `total / 5`; the helper compares exactly. | `build-preflight:67`, `:93`; `reclaim-swap:143` | F-03 |
| G-49 | High | **Confirmed, graded Medium within F-10.** The header's example commands partition and format `/dev/nvme1n1`, the device name the usage text (`:31-35`) says turned out to be the OS disk, and the script's own refusal cannot cover commands run before it. A one-time tool, last used 2026-09-04. | `fork-newdrive:12-15`, `:31-35` | F-10 |
| G-50 | Medium | **Confirmed, in F-10:** discovery errors read as false and `|| true`. | `fork-newdrive:40-55`, `:100-112` | F-10 |
| G-51 | Medium | **Confirmed, in F-10:** no existing-`OLD` refusal and no rollback after `mv` or the `fstab` append. | `:129-138` | F-10 |
| G-52 | Medium | **Confirmed, in F-10:** no check for live builds or guests before the move. | `:123-150` | F-10 |
| G-53 | Low | **Confirmed, in F-10:** `fstab` hardcodes `ext4`. | `:132` | F-10 |
| G-54 | Low | **Lead:** bundle immutability is the candidate store's, outside the slice. | `fork-publish-release:22-24`, `:113` | F-20 |
| G-55 | Low | **Confirmed, Low.** SIGTERM ends the preparer without its `finally`, orphaning the state-check group. | `:89-97` | F-20 |

### The seat's refutations of the first reader

- **F-01: agreed, and the history is now proved (P10).** On exports of `e198f0fc3b` (`d7e2d6be41^`) the three controls pass, with rc 0, `13 PASS; 0 FAIL` and `35 PASS; 0 FAIL`. At `d7e2d6be41` they fail with rc 1.
- **F-02: agreed.** The leak happens on passing runs too: the `/tmp` count rose with the history runs' passing `test-submit` (now 10).
- **F-03: agreed Medium, narrowed by UID.** A plain `kill` reaches only same-UID processes. On this host both lanes' guests run as `max`, so here it reaches every guest. G-47 and G-48 join it.
- **F-04: re-graded Medium, accepted.** It breaks a route the guide advertises.
- **F-05: broadened, accepted.** Any failed identity read, not only one at start, collapses to `alive=no`.
- **F-06: the precise escape accepted:** the second `wait(timeout=5)`. G-27 to G-30 join it.
- **F-07: re-graded Medium, accepted.** One builder per worktree is the rule (`worktrees.md`), and the lock is its only enforcement. The killed-runner control does not try a second build.
- **F-08: expanded, Medium, accepted.** The guard table gains the seat's missing rows, and five `yes` rows are corrected (rows 14, 16, 29, 31, 59; see Q6).
- **F-09: Low, unchanged.**
- **F-10: re-graded Medium,** with G-49 to G-53.
- **F-11: withdrawn.** `test_insufficient_memory_and_boundary` (`test-swap-reclaim:199-206`) fails if the memory refusal is removed, so it is the retained control the README asks for. The one-time mutation run of 2026-10-04 was that check's proof. Row 51 is corrected.
- **The risk summary:** agreed, it was too reassuring. `reclaim-swap`, `install` and `fork-newdrive` mutate shared host state, and F-07 is an exclusion failure. Corrected in § Risk Assessment.
- **"1,885 finished proves no success":** agreed. The record's outcomes are now in `02`: rc 0 1,470; rc 1 397; rc 2 10; rc 125 4; rc 143 3; rc 137, 130 and 127 one each.

### What the seat could not judge

These are recorded as limits, not findings:
- the deployed sudo policy and staging permissions (G-08's exploitability);
- real kernel swap behaviour;
- the candidate store;
- every route through the Makefile;
- the CI's full reach;
- production frequency of the races.
