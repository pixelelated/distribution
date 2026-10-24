## 1. New findings

These are code traces and conditional unsafe seams, not newly reproduced failures. Admission is explicitly an **operational guard, not a security boundary**; its bypasses below should be read in that light (`tools/host-maintenance/build-admission.md:9-10`).

### `reclaim-swap`

- **G-01 — Medium — `tools/host-maintenance/reclaim-swap:83-100`:** The busy-host refusal trusts mutable command-line names, examining only the first three words. Renamed QEMU/compiler processes, altered `argv[0]`, or a watcher behind additional interpreter options can evade it while forbidden work remains alive.

- **G-02 — Medium — `tools/host-maintenance/reclaim-swap:79-90`:** PID 1 being named `systemd` does not establish a host-wide process view. A systemd-led container or restricted `/proc` view can pass this test while omitting host jobs; whether the sudo caller can arrange such a view is not established.

- **G-03 — Medium — `tools/host-maintenance/reclaim-swap:149-163,200-209`; `tools/watch-build:102-106`:** Reclaimers serialize with each other, not with builders. New work or memory pressure can arrive after the last check; caller-controlled stdout backpressure can also suspend the flushed print at line 161 indefinitely between checks and `swapoff`.

- **G-04 — Medium — `tools/host-maintenance/reclaim-swap:111-120,146,169-179`:** `/etc/fstab` is neither ownership/identity-checked nor reread. Its default-looking entry also does not prove the flags used for the *current* activation. Manual activation or concurrent configuration changes can therefore lose activation settings on restoration.

- **G-05 — Low — `tools/host-maintenance/reclaim-swap:103-108,157-176`:** File identity is only device/inode/size, and commands reopen the pathname after checking it. Same-inode edits or privileged replacement between checking and use are not excluded. This is a concurrent-administrator seam, not evidence that the ordinary sudo caller can replace root-protected `/swap.img`.

- **G-06 — Medium — `tools/host-maintenance/reclaim-swap:20,162-184,230-232`:** Cleanup protects only SIGINT, SIGTERM and SIGHUP. Another terminating signal, such as SIGQUIT, delivered while swap is inactive can terminate Python without executing reactivation. The packet does not establish which signals the deployed sudo arrangement forwards.

- **G-07 — Medium — `tools/host-maintenance/reclaim-swap:130-135,167-182`; `tools/host-maintenance/test-swap-reclaim:139-147,150-170`:** The 120-second subprocess timeout is not an end-to-end recovery deadline: killing/reaping a kernel-blocked command can take longer. A `swapon` exception jumps straight to refusal without final state readback or another restoration attempt; the command doubles do not exercise actual timeout behavior.

### `install`

- **G-08 — High — `tools/host-maintenance/install:164-168,107-120,20-26`; `tools/host-maintenance/README.md:59-69`:** If an administrator installs from a writable checkout, its writer can substitute the installer itself, or a syntactically valid helper with the required shebang. No trusted expected digest or source ownership check binds the reviewed bytes; arbitrary substituted helper code becomes passwordlessly root-invokable. Immutable staging would remove this trigger, but is not demonstrated.

- **G-09 — Low — `tools/host-maintenance/install:20-26`; `tools/host-maintenance/test-swap-reclaim:408-420`:** “Sole added permission” is not established by parsing this command rule. Where `listpw=any` applies, a NOPASSWD entry also permits passwordless `sudo -l`; verification behavior depends on effective policy. The packet supplies neither relevant sudo-rs defaults nor effective-policy tests. This is not evidence of another root command being granted.

- **G-10 — Low — `tools/host-maintenance/install:38-47,112-156`:** Installation is not a crash-atomic two-file transaction. Default SIGTERM/SIGHUP termination does not enter the Python rollback handler, and parent directories are not fsynced after renames. Interruption can leave mismatched helper/policy versions or stale temporary files; the guide acknowledges the need for subsequent verification (`README.md:68-69`).

- **G-11 — Low — `tools/host-maintenance/install:120,160-179`:** Final installed-byte/mode verification uses `assert`. An explicit administrator invocation with Python `-O` removes that check; the `-I` shebang does not prohibit overriding interpreter options. The recommended invocation does not use `-O`, but the draft’s claim that the check is inherently safe is too strong.

### `build-admission`

- **G-12 — Medium — `tools/host-maintenance/build-admission:77-80,165-168,199-204`:** Reservations are shared by Git common directory, not by filesystem or host. Independent clones on the same volume can each admit against the same free bytes without accounting for the other registry’s outstanding reservations.

- **G-13 — Medium — `tools/host-maintenance/build-admission:84-94,169-172,199-216,48-53`:** Single use depends entirely on retained registry history. Missing `jobs.json` silently initializes generation zero; deleting/restoring that history can make a still-current, previously used receipt reusable. There is no registry-instance identity, and registry renames lack directory fsync for crash durability.

- **G-14 — Medium — `tools/host-maintenance/build-admission:84-94`:** An existing registry is checked only for final-path symlink status and UID—not writable mode, ancestors, lock-file identity or lock symlinks. In a writable existing registry, replacing `lock` can split mutual exclusion and replacing `jobs.json` can alter reservation history.

- **G-15 — Medium — `tools/watch-build:31-47,89-94`; `tools/host-maintenance/build-admission:220-226`:** An inherited run is a reusable bearer marker, not proof of parentage. Another process can attach to a live run without taking the worktree lock or spending another admission; a symlinked run directory in an identical-source checkout can replay it across checkouts/registries because nested validation binds neither location nor registry.

- **G-16 — Low — `scripts/build:7-11`; `scripts/build_distro:9-13`; `scripts/image:7-11`; `scripts/install:8-12`; `scripts/build_compat:5-9`:** The visible entry hooks can be skipped by supplying `RASTERATOPS_WATCH_EXEC` equal to `$0`. Thus “record-only cannot admit compilation” is an operational convention, not an enforced compiler boundary—the documented non-security limitation matters here.

- **G-17 — Medium — `tools/host-maintenance/build-admission:188-194,220-226`:** `BUILD_DIR` and the Docker mount-string contract are checked only on outer admission. A nested entry can change `BUILD_DIR` to an undeclared location while retaining matching source/profile and receive no capacity/output-location recheck.

- **G-18 — Medium — `tools/host-maintenance/build-admission:138-148,199-216`; `tools/watch-build:102-106`:** Declared output roots are not checked against other running jobs’ outputs. Separate worktrees can acquire separate worktree locks and admit writes to the same build/cache directory, provided aggregate byte capacity fits.

- **G-19 — Medium — `tools/host-maintenance/build-admission:60-74,121-126`; `tools/host-maintenance/retention-report:273-275`:** A protected directory’s own metadata is not recursive content identity. Overwriting an existing descendant can leave that identity unchanged; untracked build inputs are also outside `source_state()`. Such changes can escape the advertised changed-input refusal.

- **G-20 — Low — `tools/host-maintenance/build-admission:112-137,247-255`; `tools/host-maintenance/admission-test-fixture.py:23-35`; `tools/host-maintenance/test-build-admission:61-84`:** Evidence remains self-attested: a hand-built report with matching hashes is accepted, budget numbers are not derived from measurement contents, and a hashed build log suffices for a caller-labelled qualification. These checks establish consistency of supplied assertions, not report production, measurement adequacy or qualification.

- **G-21 — Medium — `tools/host-maintenance/build-admission:162-173,183-215,245-281`:** Plans, receipts and acceptance evidence are read, hashed and reread through separate pathname operations. Concurrent changes can make retained snapshots or recorded evidence hashes differ from the bytes actually validated; ordinary consumption does not recheck its evidence after acquiring the registry lock.

- **G-22 — Medium — `tools/host-maintenance/build-admission:245-274`:** Ordinary consumption trusts mutable `admission.json` fields but compares the registry row only by run path. Changing `submission_owner` can remove launcher checks, and missing PID files remove exit/group checks. Unlike recovery’s full-row comparison at line 440, the durable registry does not authenticate these consumption inputs.

- **G-23 — Medium — `tools/host-maintenance/build-admission:250-255`:** Ordinary consumption does not enforce integer result types, command/runner consistency, or agreement with the watcher’s outcome. For example, runner 0 plus command/build.rc 37 can be labelled qualified with a `finished` prefix; booleans also satisfy several zero comparisons.

- **G-24 — Medium — `tools/host-maintenance/build-admission:234-239,256-271`:** Empty `/proc/<pid>/cmdline` is treated as exit without checking process state, and missing cmdline is accepted without confirming disappearance of the PID directory. Argument availability is not a reliable exit proof.

- **G-25 — Medium — `tools/host-maintenance/build-admission:256-271`; `tools/watch-build:156-157,188-215`:** Ordinary completion covers leaders and the original command process group, not escaped groups/sessions or daemon-owned containers. A background descendant that redirects output and changes group/session can outlive a “finished” run and evade consumption’s custody check; the runner also stops forwarding signals once its leader exits.

- **G-26 — Medium — `tools/host-maintenance/build-admission:93-94,278-281,461-472`:** Consumption writes `admission-consumed.json` before committing the registry. A crash or registry-write failure between them leaves a running reservation and an existing exclusive receipt; retry then fails creating that receipt rather than reconciling the partial transaction.

### Runner and status file

- **G-27 — Medium — `tools/watch-build:180,190-200`:** If durable-log writing fails, the exception handler writes to the same failed log *before* terminating the child. A second write failure skips cleanup; failure writing `build.rc` can also abort finalization. Ordinary I/O failure—not only outright runner killing—can therefore orphan a payload.

- **G-28 — Medium — `tools/watch-build:174-187`:** Console writes are synchronous and unbounded. A connected but non-draining console can block log collection and eventually the payload’s output pipe indefinitely; handling `BrokenPipeError` does not handle this backpressure case.

- **G-29 — Medium — `tools/watch-build:137-148,174-188,202-214`:** After arming, the runner does not inspect monitor health until the command finishes. A watcher that dies early can leave a long build unsupervised for its remaining duration, although the eventual green result is correctly prevented.

- **G-30 — Low — `tools/watch-build:153-170`:** A handled cancellation during admission still proceeds to `Popen`; the signal is forwarded only afterward. The payload can execute and mutate outputs after cancellation was already recorded.

- **G-31 — Medium — `tools/watch-job:195-203,225-235,268`:** A valid result file takes precedence over an observation error. If activity scanning fails in the same iteration that `build.rc` appears, the watcher publishes `finished` and exits zero, suppressing the observation failure.

- **G-32 — Low — `tools/watch-job:176-188,212-216,261-265`:** Main-log readability is not checked, and disappearance/inaccessibility of discovered activity roots can silently remove them from observation. Failed progress/tail reads become empty display text rather than an observation error.

- **G-33 — Medium — `tools/watch-job:112-127,160,192,266`:** Output/input separation is pathname-based, not inode-based, and derived output names are not independently resolved. A pre-existing `.pid`/`.tmp` alias can overwrite an input; concurrent watchers using the same status name also have no exclusive ownership of the shared pidfile and temporary status.

- **G-34 — Low — `tools/watch-job:107-108,216,262,266`:** User patterns are passed to grep without `-e`/`--`, and `mv` receives potentially dash-leading status names without `--`. A pattern such as `--help` can pass “regex validation” while being interpreted as an option rather than a pattern.

- **G-35 — Low — `tools/watch-job:163-171,220-222`:** Initial attachment records the identity of whichever process currently occupies the supplied PID. If reuse occurred before attachment, the watcher follows the replacement process; start-time comparison protects only against reuse after that initial observation.

### Durable launcher

- **G-36 — Medium — `tools/watch-build-submit:32-49,69-89`:** The fresh-owner precheck omits `launcher-start.json`, `launcher-result.json` and `launcher-pid.json`. An incomplete/restored owner lacking `launcher-submission.json` can retain stale completion evidence or fail immediately on an old start receipt while the parent still announces submission.

- **G-37 — Medium — `tools/watch-build-submit:83-101`:** The worker is spawned before `launcher-pid.json` is exclusively written. A pid-receipt collision or write failure returns submission failure even though the worker—and potentially the build—has already started.

- **G-38 — Low — `tools/watch-build-submit:30-50`:** The worker has no signal forwarding or terminal-receipt cleanup around its synchronous runner wait. Ordinary SIGTERM/SIGHUP can leave the runner alive without launcher completion evidence, permanently obstructing ordinary consumption (`build-admission:259-262`).

- **G-39 — Low — `tools/watch-build-submit:74-86`; `tools/watch-build:50-57,114-116`:** The launcher hashes a mutable runner pathname and executes it later; it neither executes the hashed snapshot nor binds the watcher/admission dependencies. If the “frozen checkout” precondition fails, the retained hash need not identify the code actually executed.

### Retention report

- **G-40 — Medium — `tools/host-maintenance/retention-report:305-308`:** The plan is parsed before the scan but hashed afterward. A plan changed during reporting can receive a hash binding the report to bytes that were never used for that scan; admission subsequently trusts that hash (`build-admission:114`).

- **G-41 — Medium — `tools/host-maintenance/retention-report:269-293`; `tools/host-maintenance/build-admission:117-118`:** Report freshness starts at report completion, not observation/scan start. An arbitrarily long scan can produce already-old dependency observations that remain acceptable for another 900 seconds. The draft’s claim that the window includes scan time is incorrect.

- **G-42 — Medium — `tools/host-maintenance/retention-report:32-33,78-83,212-239`:** Protection, scan containment and independent-evidence checks are lexical. Symlink ancestors and `..` aliases can make the same physical object appear outside its protected/owner tree, allowing an otherwise protected candidate or non-independent evidence to pass those checks.

- **G-43 — Medium — `tools/host-maintenance/retention-report:172-199`; `tools/host-maintenance/build-admission:112-118`:** The report neither establishes a host PID view nor records one for admission to verify. A successful report from a narrower namespace can omit live host QEMU/owners; successfully inspecting Docker does not repair missing non-container process visibility.

- **G-44 — Medium — `tools/host-maintenance/retention-report:234-257`:** Lifecycle/replacement receipts are not bound to the candidate’s disk, owner, namespace or run. Truthy `passed`, arbitrary absent PID values and four equal—but not necessarily valid—channel values can satisfy completion checks; unrelated preserved receipts can therefore support an eligible proposal.

- **G-45 — Low — `tools/host-maintenance/retention-report:271-291`:** Proposed reclaim bytes sum every eligible candidate without checking its filesystem against `volume`. Candidates on another filesystem can inflate projected headroom, although ordinary admission correctly does not count this proposed reclamation as current free space.

- **G-46 — Low — `tools/host-maintenance/test-retention-report:37-43`; `tools/host-maintenance/retention-report:173-198`:** The retention controls are not host-isolated: each report performs real `/proc` and Docker enumeration. Their positives depend on daemon availability and absence of unrelated QEMU, contrary to the retrospective’s blanket claim that these controls do not touch real Docker.

### Preflight and disk migration

- **G-47 — Medium — `tools/build-preflight:101-123`:** Failed guest enumeration is indistinguishable from no guests: `pgrep` diagnostics/status are discarded. With healthy memory counters, a missing or failing `pgrep` can produce `READY` without any guest census, independently of F-03’s stopping defect.

- **G-48 — Low — `tools/build-preflight:67,93`; `tools/host-maintenance/reclaim-swap:143`:** Preflight compares free MB against truncated `total / 5`; the helper uses an exact multiplied comparison. A value just below 20% can therefore pass preflight and skip reclamation.

- **G-49 — High — `tools/fork-newdrive:12-15,31-35,87-99`:** The header instructs destructive partitioning/formatting by an unstable device name *before* invoking the guarded script. Following it after the documented device renumbering can destroy the system disk; the later system-disk refusal cannot protect those preceding commands.

- **G-50 — Medium — `tools/fork-newdrive:40-55,94-112`:** Discovery failures can become permission to proceed: failed mount discovery returns empty, the system-disk pipeline is used as an ordinary false predicate, mounted-disk errors are swallowed with `|| true`, and an `/etc/fstab` read error is treated like no UUID match.

- **G-51 — Medium — `tools/fork-newdrive:129-138`:** There is no existing-`OLD` refusal or rollback. `mv` can nest the source inside an existing destination, and mounting can fail after the source move and fstab append. A retry can then be blocked by the newly added UUID despite incomplete migration.

- **G-52 — Medium — `tools/fork-newdrive:123-150`:** Confirmation is not quiescence: no build/VM/worktree lock or live-writer check precedes moving directories, pruning registrations and copying the cache. Running jobs can continue against moved or newly overmounted paths.

- **G-53 — Low — `tools/fork-newdrive:18-22,105-106,132-133`:** Any filesystem with a UUID is accepted, but the new fstab entry hardcodes `ext4`; environment-supplied mount paths are also not fstab-escaped. A non-ext4 filesystem or whitespace-bearing path can break mounting after the migration has already mutated host state.

### Release preparation

- **G-54 — Low — `tools/fork-publish-release:23-25,89-113`:** Byte binding depends on the external bundle’s real immutability. Two pathname-based verifications do not exclude an ABA substitution during state inspection: if the bundle is writable, different bytes can be inspected and restored before final verification. The candidate-store implementation needed to close this seam is absent.

- **G-55 — Low — `tools/fork-publish-release:89-97`:** State inspection runs in a new session, but its cleanup requires Python unwinding. Default SIGTERM termination of the preparer can orphan that group; the parent-owned 900-second timeout then disappears with the parent.

## 2. Refuting the first reader

The draft’s risk summary is too reassuring: swap reclamation, installation and disk migration plainly mutate shared host state, not merely one run (`reclaim-swap:163-176`, `install:112-117`, `fork-newdrive:129-138`). F-07 is also an exclusion failure, not simply a fail-closed reporting problem.

- **F-01 — Agree Medium at this hash; narrow the historical assertion.** The supplied control output establishes three failures; the two submit receipts establish its missing-module/admission layers. Updated, admitted fixtures producing passing results would falsify current breakage; the packet shows the opposite. “Every hash since introduction” and the other fixtures’ exact histories are not independently demonstrated. The displayed CI step omits these controls (`.github/workflows/fork-checks.yml:40-44`).

- **F-02 — Provisionally agree Low for the observed leak.** The cited allocation is `docs/qa-logs/2026-10-05-watch-submit/test-submit.py:15`, and `02` P6 reports `/tmp` counts increasing 4→5→6. A `finally` cleanup or enclosing cleanup owner would falsify a permanent leak. The complete script and raw directory listing are absent, so “every run” is less firmly supported than the reported observations.

- **F-03 — Agree Medium, but narrow “every guest.”** Matching and signalling are broad, with no wait or failure contribution to the verdict (`tools/build-preflight:101-123`). Ordinary `kill` cannot necessarily stop another UID’s guests, and matching command lines need not actually be QEMU. Scoped PID identity, authorization and successful exit observation would falsify the defect; none appears in this path.

- **F-04 — Re-grade Medium.** This breaks an advertised execution route, not just diagnostics: `admit()` hashes immediately using the unavailable API, before payload launch (`build-admission:34,180`; `watch-build:163-165`). The supplied Python record says 3.10, while the guide supports interactive-container admission (`build-admission.md:101-104`). Python ≥3.11, a compatibility implementation, or exclusively host-side admission would falsify the affected-path claim; the last describes ordinary wrapped Docker, not docker-shell.

- **F-05 — Agree Low; broaden beyond startup/namespaces.** Failed `kill -0` or stat reads, including permission failures and later observation failures, collapse to `alive=no` (`tools/watch-job:163-171,218-233`). Explicit “unknown” handling or an enforced visibility contract would falsify this. The help only assigns namespace responsibility to the caller; it does not enforce it (`:68`).

- **F-06 — Agree Low; identify the precise escape.** The first timeout is caught; the *second* `monitor.wait(timeout=5)` can escape before `finish` (`tools/watch-build:202-214`). The top-level handler then returns 2 (`:221-223`). Guaranteed termination within that grace period or a finalization path covering timeout would falsify it; neither is shown, and no hung-watcher reproduction is supplied.

- **F-07 — Re-grade Medium.** Releasing the runner-owned lock while its command group survives permits concurrent mutation of one worktree; a retained capacity reservation does not enforce worktree exclusion (`tools/watch-build:102-106,165-167`). An inherited lock or an old-workload custody check would falsify this; neither exists. The killed-runner control observes death but does not attempt a second fresh admitted build (`test-build-monitor:260-275`).

- **F-08 — Agree, expand and re-grade Medium as an assurance finding.** The listed omissions are real, but the guard inventory and several claimed positives are also incomplete/misattributed, as below. Additional controls constructing the exact failures would falsify particular omissions. The supplied suites do not supply those controls; passing totals alone do not establish coverage.

- **F-09 — Narrow to Low migration/documentation debt.** The paths exist in defaults and a comment (`tools/fork-newdrive:20-21`; `tools/watch-job:36`). That does not itself prove erroneous execution: the defaults are overridable, the watcher example is non-executable, and the supplied record still reports legacy-layout runs. An intentionally supported legacy layout would defeat a functional-bug claim; the packet does not provide enough of #640 to resolve that policy question.

- **F-10 — Agree Low for the listed stale instructions, not a demonstrated destructive execution.** The detached fallback, old cache copy and removal advice are present (`tools/fork-newdrive:140-154`); the final removal is printed, not executed. A genuinely archival, non-current workflow with matching assumptions could narrow or eliminate the policy conflict. The executable script supplies no such retirement guard; its additional operational defects are G-49–G-53.

- **F-11 — Narrow to Low reproducibility/documentation debt.** No mutation runner appears in the supplied suite, but the retained low-memory boundary test *would fail* if the memory refusal were removed (`test-swap-reclaim:199-212`). Thus the guard is not untested, and “must fail” can be read as a requirement rather than a claim that a mutation runner exists (`README.md:95-101`). A retained mutation driver elsewhere would falsify the broader absence claim; only the first reader’s search report addresses that.

### Is Q6’s guard table complete, and are its `yes` rows sound?

**No on completeness; several `yes` labels overstate what their controls establish.**

**Explicit wired guards missing or submerged in overbroad families include:**

- Runner argument/activity checks and launcher owner/runner validity (`tools/watch-build:76-85`; `tools/watch-build-submit:63-68`).
- Admission path/type and registry validation; report expiry; volume, output, budget and profile-shape validation (`build-admission:60-67,84-101,117-152`). Ordinary consumption has additional launcher/result/group checks not individually controlled by row 37 (`:250-274`).
- Swapfile minimum size, changed swap configuration and unsafe lock-FD metadata (`reclaim-swap:106-107,152-154,205-207`); installer arguments, source validation, locking and final installed-byte verification (`install:120,162-178`).
- Retention scan-root/reference-store validation, duplicate candidates, oversized manifests, container failures and budget validation (`retention-report:78-90,165-166,191-198,277-285`). Row 59’s `evaluate()` range is not these guards.
- Migration block-device/primary-checkout/UUID/confirmation checks (`fork-newdrive:84-85,105-106,123-124`). Recovery census parsers also have their own refusals, while the tests replace those census functions (`build-admission:290-321`; `test-build-admission:148`).

**Specific misleading coverage claims:**

- **Row 14, worktree exclusion:** the second launch reuses the already-used admission (`test-build-monitor:219-226`). Removing the flock could still leave this test passing because admission refuses reuse (`build-admission:200`). It does not isolate the lock.
- **Row 16, stale heartbeat:** its fixture names a *missing* run (`test-build-monitor:190-195`), failing the status read before reaching the heartbeat-age check (`watch-build:36-42`).
- **Row 29, consumed single use:** the attempted second launch occurs at `test-build-admission:59`, but consumption occurs at `:83`. It tests reuse of a running/unconsumed admission, not persistence of single-use history after consumption.
- **Row 31, changed report:** the report mutation injects inventory errors (`test-build-admission:31`), exercising the explicit error refusal (`build-admission:113`), not independently demonstrating the report-digest binding.
- **Rows 38, 40, 49 and 54 are broader than their evidence:** mocked recovery censuses do not test their parsers; lock exclusion does not test every unsafe-FD condition; command/signal doubles do not test real timeout/signal propagation; syntax-valid sudoers is not an effective authorization test (`test-build-admission:148,186-193`; `test-swap-reclaim:48-74,150-170,238-282,408-420`).
- **Row 59’s arithmetic and isolation are wrong:** the 19 retention controls contain **four positives and fifteen negatives**, not eighteen refusals and one positive (`test-retention-report:43-94`). The “unreadable disk” case also changes its expected identity through chmod, so refusal can occur without proving the readability guard (`:46-50`; `retention-report:227-229`).

For balance, ordinary `admit()` **does** bind an unmodified receipt to checkout/state/registry path and rejects an ID retained in that registry (`build-admission:185-201`). G-12–G-17 identify different boundaries—separate registries, lost history and inherited-run reuse—not a claim that this direct comparison is absent.

## 3. What I could not judge

- **Deployed privilege boundary.** No installed helper/policy hashes, effective sudo authorization listing, sudo-rs authentication defaults, source-staging permissions or live path metadata are supplied. The installer’s checks and mocked tests are not installation proof (`install:85-120`; `test-swap-reclaim:438-444`; `README.md:95-101`). G-08’s exploitability therefore depends on actual staging writability.

- **Real swap recovery and namespace reachability.** The packet does not establish actual activation flags, automatic priority restoration, kernel timeout behavior, sudo signal forwarding, or the caller’s ability to obtain a misleading namespace. The swap command/state transitions are doubled, with priority restoration synthesized by the test (`test-swap-reclaim:150-181`).

- **External enforcement and full routing.** The candidate store, selected-state checker, release-test implementation, most Makefile content and script bodies are absent. I cannot establish real bundle immutability, inspection correctness, every build route, or the claimed release-control coverage (`fork-publish-release:22-24,85-113`; supplied entry-line excerpts; Q6 row 62).

- **Historical/global absence claims.** The supplied outputs establish the controls’ present results, not every intervening hash, complete CI reachability, all temporary-directory cleanup, or repository-wide absence of a mutation driver. The historical control bodies themselves are not supplied; the displayed CI evidence is only `.github/workflows/fork-checks.yml:30-50`.

- **Production evidence quality and success.** The record says 1,885 status files were `finished`; that state preserves any valid exit code, including failure (`tools/watch-job:225-230`). It proves neither successful builds nor qualification, complete process custody, adequate measured budgets, or absence of unsafe interleavings. The admission fixtures explicitly use synthetic budgets and reports (`admission-test-fixture.py:19-35`).

- **Production cost and exposure frequency.** The supplied timing output measures admission latency and elapsed log-scan time. It does not establish total pipeline CPU consumption, real retention-scan duration, or how often the identified races occur (`tools/watch-job:212-214`; output “the cost figures”). None of the new failure scenarios was reproduced in the packet.