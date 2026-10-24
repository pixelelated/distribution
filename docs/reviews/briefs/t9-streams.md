# T9's remediation streams (#656, audit issue #924)

Written by the coordinator on 2026-10-24 at T9's stage-D pause
(D-WORKFLOW-189), in the shape of `t8-streams.md`: eight streams, each with
the files it owns, the test first, its `Already written:` line, its
acceptance and its commit; then the dispositions that are not streams, which
the lane writes into the Phase 7 table; then the order and the hand-back. The
lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-build-supervision-656`,
branch `feature/m6-tooling-build-supervision-656`, stage-D tip `cb8019a10b`).
**Review depth per stream: Local** (plan § 6c: a contained fix with a
control; the executor, the control, and the coordinator reading the diff on
the bug). **Nothing here builds, starts a guest, reclaims swap, installs a
helper, formats a disk, or publishes.** Three contract choices the punch list
left to the coordinator are decided here and recorded as D-INFRA-028,
D-INFRA-029 and D-INFRA-030 (the register, the same session); each is
reversible by a revert before the merge, and each is put to the maintainer on
#346 the same hour.

**The host during stage E.** The M7 lane holds a bounded exclusive VM window
from about 16:50 UTC (one 2 GiB no-network GENERIC guest; the grant is on
`/tmp/m7-m6-host-coordination-20261023.txt`). So a real `qemu-system-x86_64`
may be on the host while these streams run, and two things follow: **the
unfixed `build-preflight --stop-vms` is never run** (it would stop M7's
guest; the brief forbade it and the grant repeats it), and **S1's isolation
of `test-retention-report` precedes every control that reads `/proc` for a
guest** (the stage-A baseline was taken at a census of zero). The one
container start S3 may make is posted on the host file with a census before
it runs. The lane's stage-D bug drafts sit under `/workspace/tmp/m6-t8/`
(T8's directory); move them under `/workspace/tmp/m6-t9/` at the first
commit, so the T8 retention pass does not take them.

## S1. The three recorded watcher controls take the admission route, `test-submit` cleans its root, `test-retention-report` is isolated from the host (PL-01, PL-02, PL-15; #913) -- `fix-case`

- **Why a stream:** Medium; three controls the record cites (blindspot 73's
  progress control, the routing fixture, the durable-submission control)
  have failed since `d7e2d6be41` (2026-10-13) and nothing ran them; the
  fix is in the fixtures, not the tool. The fork CI's wiring of the three
  is **not** this stream's: `.github/workflows/fork-checks.yml` is T10's
  file (#657, being read at the hash now), so the coordinator posts the
  wiring as a row on #657 and PL-01's last clause moves there.
- **Files owned:** `docs/qa-logs/2026-10-04-watch-progress/test-progress.py`,
  `docs/qa-logs/2026-10-04-watch-progress/test-watch-build.py`,
  `docs/qa-logs/2026-10-05-watch-submit/test-submit.py`,
  `tools/host-maintenance/test-retention-report`. **Not** `tools/watch-build`
  (S3's and S5's), not `fork-checks.yml`.
- **The shape:** each fixture prepares an admission the way
  `test-build-monitor` does, through `admission-test-fixture.py` (the module
  copied *and* a receipt prepared), for every case that launches a build-
  shaped payload; a case whose payload is QA-shaped takes `--record-only`.
  Read what each case exercises before choosing: a case that exercises the
  admission guard itself keeps its refusal as the positive. `test-submit.py`
  removes its `mkdtemp` root in a `finally`, as the other controls do.
  `test-retention-report` injects its process and container observations as
  `test-build-admission`'s recovery cases do, so a live QEMU on the host
  changes nothing it reads.
- **The test first**, each output pasted on #913 and in `02`: the three
  controls at the stage-D tip, unchanged, fail (the stage-A exits); the
  stage-A diagnostic copies (`.qa-scratch/t9/diag/`, module added, no
  receipt) fail on layer 2 (`watch-build: build admission required`); then
  the fixed controls exit 0; then **a copy of each fixed control with its
  admission step removed fails** -- that copy is the constructed positive
  and is kept under `.qa-scratch/t9/positives/`, its exit quoted.
  `test-submit.py`: the count of `/tmp/pixelelated-watch-submit-*` before
  and after a run, equal. `test-retention-report`: passes with a process
  named `qemu-system-x86_64` present (a renamed sleeper in the lane's own
  session, `exec -a qemu-system-x86_64 sleep 300`, killed by its PID
  afterwards, never by pattern), quoted.
- **Already written:** ten `/tmp/pixelelated-watch-submit-*` directories
  on 2026-10-24, six of them this lane's runs: the stream removes the six
  it owns (named by their mtimes in `02`), lists the other four with their
  mtimes on #913 and leaves them; nothing reads them.
- **Acceptance (PL-01, PL-02, PL-15; #913's criteria less the CI clause):**
  the three exit 0 at the fix; each positive copy fails, by name; the
  `/tmp` count equal before and after; the retention control passes with
  the renamed sleeper present. The CI clause is #657's row.
- **Commits:** `qa-logs: the three watcher controls prepare an admission; test-submit cleans its root (#913)`
  and `host-maintenance: test-retention-report injects its host observations (#913)`,
  each `Refs #913, #656`, the attribution line.

## S2. `build-preflight` stops nothing: `--stop-vms` reports each guest and names `tools/vm-stop`; a failed census is an error (PL-03; #914; D-INFRA-028) -- `fix-case`

- **Why a stream:** Medium; the tool `pgrep -f`s every `qemu-system-x86_64`
  of the user and `kill`s each on a flag, with no ownership check and no
  wait, then can print READY. On this host that is another lane's guest
  (T8's today; M7's during this very stage). The contract is the
  coordinator's and is decided: **a preflight reports; it never stops a
  guest.** `tools/vm-stop` is the one way a guest is stopped (by its
  pidfile and owned disk, awaited; `generic-x64-vm-testing.md`), and
  `CLAUDE.md` already says *stop the VM by its pidfile, never by `pkill`
  pattern*. The flag stays accepted so a scripted caller does not break,
  and prints that it no longer stops anything.
- **Files owned:** `tools/build-preflight`; a new control
  `tools/host-maintenance/test-build-preflight` (under `host-maintenance/`,
  which is already a personal pattern as a directory, so no list changes);
  the one sentence in `.claude/rules/device-builds.md:463` and the one in
  `.claude/rules/generic-x64-vm-testing.md:952` that say `--stop-vms` stops
  guests (rule edits under this brief, D-WORKFLOW-189: they say instead
  that the preflight lists guests and that `tools/vm-stop <pidfile>` stops
  one). **Not** `tools/vm-stop`.
- **The shape:** with or without the flag the tool lists each guest (pid,
  monitor socket, RSS, uptime, and the `-pidfile` argument from its
  command line when there is one) and the exact `tools/vm-stop` command for
  it; with `--stop-vms` it adds one line, *this flag no longer stops
  anything; stop a guest you own with the command beside it*; the verdict is
  1 while a guest is listed. A `pgrep` that fails (exit 2 or above; exit 1 is
  "none") is `ERROR: cannot census guests`, exit 1, never "no guests"
  (G-47). The swap threshold is compared as the installed helper compares it,
  at the boundary (G-48; read `reclaim-swap`'s comparison and match it).
- **The test first:** the control runs the tool with `PATH` doubles for
  `pgrep` and `ps` (the tool calls both unqualified) over renamed sleepers
  in the control's own session, and proves: a listed guest is still alive
  after a run with `--stop-vms` (the sleeper's PID answers `kill -0`), the
  verdict is 1 and the notice line is printed; a `pgrep` double exiting 3
  gives the error line and exit 1; no guest gives READY; the threshold at
  the boundary matches the helper's. Before the fix, the same control shows
  the sleeper gone after `--stop-vms` -- that run is the constructed
  positive, quoted; **it uses the control's own sleepers only, never the
  real tool against the real host.**
- **Already written:** nothing persistent; whether a past `--stop-vms`
  ever ended another lane's guest is not in the record (PL-03).
- **Acceptance (PL-03; #914's criteria, rewritten here by the coordinator
  for the decided contract):** the control's five cases quoted; the two
  rule sentences changed; `tools/rules-check --quiet` rc 0.
- **Commits:** `build-preflight: --stop-vms reports guests and names tools/vm-stop; a failed census is an error (#914)`
  and `doctrine: the preflight lists guests; tools/vm-stop stops one (#914)`.

## S3. The admission and retention tools hash with a streamed loop, and a failed digest reaches `watch-build`'s refusal (PL-04; #915) -- `fix-case`

- **Why a stream:** Medium; `hashlib.file_digest` is Python 3.11's, the
  pinned container's interpreter is 3.10 (`device-builds.md:379-380`, the
  pin unchanged since `2c349c6d51`), and `build-admission.md:101-102`
  describes an admitted docker-shell run as supported. #492 met the same
  class on 2026-10-08 and fixed it with a streamed loop.
- **Files owned:** `tools/host-maintenance/build-admission:34`,
  `retention-report:22`, `:69`; in `tools/watch-build` **only** the two
  except tuples at `:190` and `:221` (S5 owns the rest of that file and
  runs after this stream); `test-build-admission` (a case for the broken
  digest).
- **The shape:** a `hashlib.sha256()` loop over fixed-size reads (#492's
  shape); the admission path's failures reach `watch-build`'s refusal as
  `watch-build: <reason>`, rc 2, never a traceback (a `ValueError`, or the
  except tuples widened to the exceptions the helper actually raises; read
  which).
- **The test first:** a fixture file hashes equal under the host's Python
  and under a 3.10. **The 3.10 is the pinned container's** if the image is
  local: `docker image ls --digests` for `988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`
  (Makefile:138); if present, one read-only start --
  `docker run --rm --network none -v <fixture dir>:/f:ro <image> python3 -c '...'`
  -- posted on the host file with a census first (the M7 window may be
  open; a container of seconds is not a guest, and the grant names it). If
  the image is not local, **do not pull it**: the proof is `fix-tree` with
  the interpreter named, and the acceptance says so. A deliberately broken
  digest (the control edits the payload after the receipt) gives
  `watch-build: <reason>`, rc 2, quoted. `grep -rn file_digest tools/`
  prints nothing after.
- **Already written:** nothing inherited: all 664 recorded admissions carry
  the host's PID namespace; no docker-shell admission was ever made (PL-04).
- **Acceptance (PL-04; #915's criteria):** the two hashes equal, the
  interpreter versions named; the broken digest's refusal line; the grep
  empty.
- **Commit:** `host-maintenance: hash with a streamed loop; a failed digest is a refusal, not a traceback (#915)`.

## S4. `watch-job`: an unreadable PID is not `died`, and the caller's pattern and names reach `grep` and `mv` guarded (PL-05, PL-18; #916) -- `fix-case`

- **Why a stream:** Low twice, one file, one control; #506's rule (an
  invisible PID is unknown, not exited) is the record's, and the tool
  says `died` where it cannot read.
- **Files owned:** `tools/watch-job`;
  `docs/qa-logs/2026-10-03-watch-job/test-watch-job.py` (the cases). **Read
  first:** no `watch-job` from the M6 tree is running
  (`pgrep -af tools/watch-job | grep /workspace/repos/pixelelated/` is
  empty; M7's watchers run their own frozen copies and are not this tree's).
  A bash tool is never edited while a run of it is in flight
  (`engineering-practices.md`).
- **The shape:** an identity unreadable at start, or a `kill -0` refused for
  permission, gives `error` (or an `unknown` no reader mistakes for death),
  never `died`; `grep -E -e "$PATTERN"` and `--` before every path; the
  `.pid` and `.tmp` names resolved into the overlap check.
- **The test first:** a case whose PID the watcher cannot read (a sleeper
  in an unprivileged `unshare -Upf --mount-proc` namespace is the input)
  gets a non-`died` state; a case whose job truly dies still gets `died`;
  `--pattern --help` is refused or matched literally; a status name
  beginning with `-` works; each quoted, and each fails on the unfixed tool
  (the positives).
- **Already written:** nothing inherited: every one of the 1,885 recorded
  statuses is `finished`; none says `died` (PL-05).
- **Acceptance (PL-05, PL-18; #916's criteria):** the four cases quoted,
  with their failing runs on the unfixed tool.
- **Commit:** `watch-job: an unreadable PID is unknown, not died; arguments reach grep and mv guarded (#916)`.

## S5. `watch-build`: the end-of-run paths finish, and the worktree lock lasts the command's lifetime (PL-06, PL-07; #917, #918) -- `fix-case`

- **Why a stream:** Medium (the lock is the one-builder rule's only
  enforcement, `worktrees.md` § One builder per build worktree) and Low (four
  end-of-run paths). Runs **after S3**, which owns the two except tuples.
- **Files owned:** `tools/watch-build`; `tools/host-maintenance/test-build-monitor`
  (the cases; the lock control isolated with a fresh admission,
  `test-build-monitor:219-226`).
- **The shape:** a late watcher (the second `monitor.wait` timeout) still
  records a finish (F-06); a failed log write kills the child before the
  write (G-27); `interrupted` is checked before `Popen` (G-30); the console
  write is bounded or dropped on backpressure (G-28). The lock: exclusion
  for the command's lifetime -- the lock descriptor inherited by the
  command, or a refusal while an earlier run's `command.pid` group is alive
  (the lane picks and says why in `02`).
- **The test first:** a control with a watcher that will not exit records
  the runner's result; one whose log write fails leaves no live payload; a
  signal during admission starts no payload; a runner killed with its
  command alive, then a second admitted launch in the same worktree,
  refused; the lock control with a fresh admission. Each case fails on the
  unfixed tool and is quoted.
- **Already written:** nothing inherited: no recorded run holds a
  `runner-error` or lacks a terminal status among the 1,885; the lock fix
  changes the next launch (PL-06, PL-07). `tools/watch-build` is a file the
  M7 lane also changed (#597): the conflict at the merge is the
  coordinator's, with this stream's paragraphs re-applied (futro A8).
- **Acceptance (PL-06, PL-07; #917's and #918's criteria):** the five cases
  quoted with their failing runs.
- **Commits:** `watch-build: every end-of-run path records a finish (#917)` and
  `watch-build: the worktree lock lasts the command's lifetime (#918)`.

## S6. The admission registry is keyed by the measured filesystem, `consume` trusts the registry row, and the retention report binds its plan bytes (PL-12, PL-16, PL-14; #919, #921, #920; D-INFRA-029) -- `fix-case`

- **Why a stream:** Medium (two clones on one volume each admit against the
  same free bytes -- true on this host: `/workspace/repos/rocknix/.git` and
  `/workspace/repos/pixelelated/distribution/.git` are both on device
  66304) and two Lows in the same tools. Runs **after S1** (the isolated
  `test-retention-report`).
- **The contract, decided (D-INFRA-029):** a reservation is a claim on a
  filesystem's free bytes, so **the registry lives per filesystem, at a
  host-wide path derived from the measured volume's identity** (its device
  and filesystem id; under the user's state directory,
  `${XDG_STATE_HOME:-~/.local/state}/pixelelated/build-admission/<fs-id>/`,
  or on the volume itself -- the lane picks and says why; neither is inside a
  clone's `.git`). Two clones that measure one volume read one registry.
  **Existing registries migrate nothing:** the M6 clone's is empty; M7's
  under `/workspace/repos/rocknix/.git/pixelelated-build-admission/` stays
  as the record of its reservations and is read by nothing new; until the
  M7 lane runs the fixed tool (its cutover), cross-lane capacity is
  coordinated as it is today, on the host file. `build-admission.md` says
  where the registry lives and why.
- **Files owned:** `tools/host-maintenance/build-admission` (the registry
  path `:77-80`, `:165-168`, `:202-204`; `consume` `:245-282`, `:440`),
  `build-admission.md`, `retention-report` (`:305-308`, `:293`, `:287`),
  `retention-report.md`, `test-build-admission`, `test-retention-report`.
- **The shape:** `consume` compares the whole registry row as recovery does
  (G-22) and commits the registry before its receipt, or reconciles an
  existing `admission-consumed.json` on retry (G-26). `retention-report`
  reads the plan's bytes once and hashes those (G-40), stamps the
  observation start and lets the window run from it (G-41), and counts only
  candidates on `volume` (G-45).
- **The test first:** a control with two clones on one filesystem (two
  temporary clones of a fixture repository on the same temporary volume
  root) refuses the second admission when the first's unconsumed
  reservation leaves too little; an edited `admission.json` is refused; a
  failed registry commit retries to `consumed`; a plan edited during a scan
  gets a mismatch; the report carries its observation start; a candidate
  off `volume` is not summed. Each fails on the unfixed tools and is
  quoted.
- **Already written:** M7's registry holds its reservations where it is;
  664 recorded admissions, their rows and receipts read unchanged by the
  fixed `consume`; earlier retention reports stay valid for their 900 s and
  expire (PL-12, PL-14, PL-16).
- **Acceptance (PL-12, PL-14, PL-16; #919's, #920's, #921's criteria):**
  the six cases quoted; `build-admission.md` and `retention-report.md` say
  what the code does (the lane re-reads both against the diff, Q7).
- **Commits:** one per bug: `host-maintenance: the admission registry is keyed by the measured filesystem (#919)`,
  `host-maintenance: consume trusts the registry row and commits it first (#921)`,
  `host-maintenance: retention-report hashes the plan it read and stamps its observation start (#920)`.

## S7. The swap helper's signals and the launcher's receipts (PL-17, PL-19; #922, #923) -- `fix-case`

- **Why a stream:** two Lows with controls that exist. Runs **after S1**
  (the revived `test-submit.py` carries PL-19's cases).
- **Files owned:** `tools/host-maintenance/reclaim-swap`, `test-swap-reclaim`;
  `tools/watch-build-submit`, `docs/qa-logs/2026-10-05-watch-submit/test-submit.py`.
- **The shape:** `reclaim-swap` blocks every catchable terminating signal
  around the mutation (SIGQUIT, SIGUSR1, SIGUSR2, SIGALRM, SIGPIPE beside
  the three it defers) and prints before the final checks (G-06, G-03).
  `watch-build-submit` checks every launcher receipt name before reserving
  (G-36), writes `launcher-pid.json` before or atomically with the start
  (G-37), and forwards termination to the runner and records it (G-38).
- **The test first:** `test-swap-reclaim`'s doubles deliver SIGQUIT during
  `swapoff` and see reactivation verified -- **doubles only, never a real
  swap command** (the brief § 8); `test-submit.py`: a stale
  `launcher-result.json` in the owner is refused; a signal to the worker
  reaches the runner and is recorded. Each fails on the unfixed tool.
- **Already written:** the installed helper on serval is unchanged until
  the owner reinstalls (D-INFRA-015): the source changes here; the
  reinstallation is the owner's, asked for on #346 by the coordinator with
  the diff; `build-preflight --reclaim-swap` keeps using the installed one
  until then, and `02` says so (PL-17). Nothing else inherited (PL-19).
- **Acceptance (PL-17, PL-19; #922's and #923's criteria):** the three
  cases quoted with their failing runs.
- **Commits:** `host-maintenance: reclaim-swap blocks every terminating signal around the mutation (#922)` and
  `watch-build-submit: every receipt checked before reserving; the pid receipt first; termination forwarded (#923)`.

## S8. `fork-newdrive` is retired (PL-10; D-INFRA-030) -- `fix-tree`

- **Why a stream:** Medium; a one-time migration (the 2026-09-04 move to
  `/workspace`, done) whose header partitions and formats a device its own
  usage text says may be the OS disk, with discovery errors read as false,
  no rollback, a hard-coded `ext4`, a detached-worktree fallback against
  `worktrees.md` and `sudo rm -rf` advice (G-49 to G-53). Nothing plans to
  run it again, and keeping unsafe steps current costs a rewrite nobody
  needs. **Decided (D-INFRA-030): retired**, not quarantined -- the
  procedure it encoded stays in `device-builds.md` § Where things live and
  the 2026-09-04 work log, git history keeps the script, and a revert
  restores it if the maintainer says so on #346 before the merge.
- **Files owned:** `tools/fork-newdrive` (`git rm`); the index row in
  `.claude/rules/instruction-files.md:159` and the entry in
  `.claude/rules/fork-workflow.md:33`'s list (rule edits under this brief);
  one sentence in `.claude/rules/device-builds.md` § Where things live
  naming the retirement and where the procedure is read. **Not**
  `.githooks/pre-push` (T10's file: its `'tools/fork-newdrive'` pattern
  stays until T10's stream or the integration packet; the coordinator posts
  the row on #657).
- **The test first:** `tools/rules-check --quiet` rc 0 after (the index and
  the counts); `git grep -n fork-newdrive -- . ':!.githooks' ':!docs'` prints
  nothing; `.githooks/hooks-test` PASS (the pattern list is still valid shell).
- **Already written:** nothing on devices or in clouds; the build estate
  it moved is where it put it (PL-10).
- **Acceptance (PL-10; the coordinator's disposition):** the three checks
  quoted; #640's `fork-newdrive:20-21` row noted moot by the lane on #640
  (the `watch-job:36` row stands).
- **Commits:** `tools: retire fork-newdrive, the 2026-09-04 one-time migration (#656)` and
  `doctrine: fork-newdrive retired; the index and the personal-paths list (#656)`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-01's CI clause** (*the three run in `fork-checks.yml`*): deferred to
  **#657** -- `.github/workflows/fork-checks.yml` is T10's path, read at the
  hash now; the coordinator posts the row there (T10's stage E, or the
  integration packet after both). S1 resolves the rest of PL-01.
- **PL-08** (73 guards, 23 without a running control, 3 partial): each
  stream above adds the controls for the guards it touches and names the
  table rows it closes in `02`; the `none` rows no stream reaches are
  deferred to a **Backlog issue the coordinator files at this pause** (the
  rows listed by number from `04` § Q6, under epic #903); the five
  misattributed `yes` rows are corrected in `04` by the lane (14, 16, 29,
  31, 59) with the controls S5 and S6 add.
- **PL-09:** deferred to **#640** as the lane wrote; after S8 the
  `fork-newdrive:20-21` row is moot (the lane says so on #640).
- **PL-11:** withdrawn at stage C (the retained control).
- **PL-13** (the installer trusts a writable checkout's bytes, no digest,
  an `assert`): a lead for the owner (D-INFRA-015): the coordinator files
  an **`Ops:` issue** and puts it to the maintainer on #346; no stream here,
  never a real installation.
- **PL-20** (the release preparer's store and orphan): deferred whole to
  **#528** (the publication and custody issue), with the seat's G-54 and
  G-55 quoted by the coordinator; the store is outside this slice.
- **PL-21** (the admission's operational-guard boundaries, G-13 to G-19,
  G-21, G-25, G-42 to G-44): deferred to a **Backlog issue the coordinator
  files at this pause**, one lead per letter, to be dispositioned with the
  owner as contract rows.
- **Criterion 15's form** (the lane's question): the coordinator edits the
  criterion on #656 and in the brief's § 7 to read from the lane's tip at
  dispatch: `git diff --stat cdc45513b0 <fixed-at> -- tools` is empty, or
  every hunk is a stream briefed here. The inherited fifteen files are P1's
  and the coordinator's, recorded in `00` and `02` (`cb8019a10b`).

## Order and hand-back

S1, S2 and S4 first (independent files); S3, then S5 (both touch
`tools/watch-build`); S6 and S7 after S1; S8 last (the rules edits, then
`rules-check`). Each stream's commits cite its bug (`Refs #N, #656`, no
closing keyword: a bug closes when its fix is on `next`, at the merge) and
carry the attribution line; `git status --short` is read before every
`git add -A` (`.qa-scratch/` is gitignored; the positives stay there).
After S8: the Phase 7 table and the `punch_index` at their outcomes
(`resolved:<commit>`, `deferred:#N`, `withdrawn`), `02` § The suites
re-run with the stream cases counted, the lint on the folder (`PASS`, the
default phase), `fixed-at:` in #656's body, the retro (stage G, posted on
#656: what the slice did to the two time-to-play numbers -- nothing; what
S2 did to a guard's refusals -- `--stop-vms` refuses to stop), then the
hand-back comment naming the tip and each artifact by path. The coordinator
accepts by `AUDIT_ISSUE=924 $S/t9-accept.sh <tip> <coordinator tip>` on an
export, reads every stream's diff and positives, ticks #656 and #924 from
the artifacts, closes #924 when its checkboxes read back ticked by name, and
merges the branch in its turn (after T8's, before T10's and T4's).
