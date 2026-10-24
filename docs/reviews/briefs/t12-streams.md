# T12's remediation streams (#659, audit issue #984)

Written by the coordinator on 2026-10-24 at T12's stage-D pause
(D-WORKFLOW-189), in the shape of `t10-streams.md`: thirteen streams, each
with the files it owns, the test first, its `Already written:` line, its
acceptance and its commits; then the dispositions that are not streams, which
the lane writes into the Phase 7 table; then the order, the one guest cycle
and the hand-back. The lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659`,
branch `feature/m6-tooling-vm-harness-659`, stage-D tip `7774e86cfa`).
**Review depth per stream: Local** (plan § 6c), with the rule the harness's
own record adds: **a stream lands with the control case that fails on the
unfixed tool and passes on the fixed one, or it is not a stream**
(`engineering-practices.md` § Guards must fail closed: *prove the guard
fires*; blindspot 39, the first PASS of anything new is the one to distrust).

**The controls.** Two exist and grow (`tools/vm-pair-test`,
`tools/vm-stop-test`). One is new: **`tools/vm-harness-test`**, host-only,
no guest, whose cases are added stream by stream: an `ssh` and an `scp`
double on `PATH` answering from a table the case writes (a `BUILD_ID` line
for the os-release read, a `boot_id`, a `pgrep` answer, a failure on
demand), a scratch `tools/` directory holding a copy of `tools/vm-qa` beside
doubles of `vm-pair`, `cloud-test-backend` and `frame-diff` (the runner
resolves its siblings from its own location, so the copy is the seam and
the real tools are never edited by a case), a monitor-socket double that
accepts `sendkey` and fails `screendump`, a serial double that answers a
command with its status, recorded frames under the test's own directory,
and `PYTHONOPTIMIZE=1` for the `assert` class. It writes only under
`.qa-scratch/t12/` (gitignored, `.gitignore:63`) and the `TMPDIR` the lane
already uses (`/workspace/tmp/m6-t12/`), never `/tmp`. It is a fork tool:
S1 adds its entry to `PERSONAL_PATTERNS`, `fork-workflow.md`'s list and
`instruction-files.md`'s index (rule edits under this brief, as T10's S4
made; `tools/rules-check --quiet` passes after). Every positive -- the
unfixed tool's rc or report -- is quoted in `02` § The streams' positives
beside the fixed run's.

**Nothing here runs a handheld action (`device-act` against a device,
D-QA-015), `qa-accounts` against a real account, `ra-offline-test`'s account
path, a cloud test against a real provider, a guest found or stopped by
pattern, a build, `fork-worktree sync|remove|repair`, a write under
`/workspace/repos/rocknix*`, or a write under `/tmp`** -- the sockets and
pidfiles D-INFRA-031 moves go under `$XDG_RUNTIME_DIR`, which is
`/run/user/1000` on this host. The one stage-E guest cycle is § Order; it
waits for the M7 lane's return line on the host file (the coordinator
granted M7 a window at 20:44 UTC, bounded at 22:15 UTC; no M6 guest starts
before that return is recorded).

Three contract choices are decided here and recorded as **D-QA-061** (the
run's exit over a SKIP), **D-QA-062** (`time-to-play` judges every cell that
ran) and **D-INFRA-031** (the host state belongs to the worktree), each
reversible by a revert before the merge, each put to the maintainer on #346
the same hour.

**The lane's question, answered first.** A SKIP gets a **distinct exit, 3**
(D-QA-061). The suite-level convention already exists -- a suite returns 3
when it could not run, and `vm-qa:141` counts it apart from PASS -- so the
run's exit lifts the same code one level: 0 only when every selected suite
ran and passed; 1 when any failed; 2 on a usage error; 3 when nothing
failed and at least one was skipped. The footer's words stand (*has not
passed*). Why not 1: a FAIL says a defect was found and a reader goes
looking for it; a SKIP says a check did not happen and the reader goes
looking for the baseline, the guest or the source it lacked. Neither is
green: the fork CI, a nightly and `release-candidates.md` step 3 take 0
only, and that rule edit is PL-22's packet (below), not this lane's.

**What the lane found, in one sentence each, so the streams read in order:**
`vm-qa` passes a run that did not pass -- over a SKIP, over an unknown or
empty selection, over a bring-up it never checked (F-01, G-01, G-02, G-30,
G-40; two Highs between PL-04 and PL-05); `vm-pair` deletes every disk
under its directory after a stop that found no pidfile, and that directory
is a RAM tmpfs every session on the host shares (G-27, G-29, F-09);
`time-to-play`, `emulator-exit-test`, `ra-offline-test`,
`vm-upgrade-rehearsal` and `frame-diff` each accept a measurement or a
check they did not make (F-02, F-03, F-18, G-08 to G-12, G-50 to G-57,
G-66); a failed screendump and a failed serial command are silent (G-32 to
G-37); seven tools refuse with `assert` (F-04); and a dozen smaller gaps
(PL-18). Five Renovation and Documentation items (PL-19 to PL-23) were held
for the coordinator and are dispositioned below.

## S1. `vm-qa`'s exit, selection and header: a SKIP exits 3, an unknown or empty `--only` or `--walk` exits 2, `--help` prints the whole header, an unwritable report is a FAIL, the minutes count bring-up (PL-01, PL-17; #966, #982; D-QA-061) -- `fix-case`

- **Why a stream:** the runner's exit is what every caller reads -- the
  release procedure's step 3, a nightly, the lane's own cycle -- and it
  said 0 over `PASSED with 1 suite(s) SKIPPED` (P7). The selection that
  runs nothing and passes (`--only nosuch`, `--only ,`, `--walk ,`) is the
  same defect from the other side.
- **Decided (D-QA-061):** the exit codes above. An unknown suite name is
  refused by name (each name in `--only` checked against `$SUITES`, as
  `--walk` already checks `suite.txt`); an empty selection (`--only ''`,
  `--only ,`, a list that reduces to nothing) is a usage error; the exit is
  computed after the footer: `[ "$FAILS" = 0 ] || exit 1; [ "$SKIPS" = 0 ]
  || exit 3`.
- **Files owned:** `tools/vm-qa`; the new `tools/vm-harness-test` and its
  three list entries (`.githooks/pre-push`'s `PERSONAL_PATTERNS`,
  `fork-workflow.md` § Personal paths, `instruction-files.md` § The fork's
  own tools -- rule edits under this brief).
- **The shape:** `--help` prints the header to its last comment line (found
  by the first non-comment line, not a hard-coded `38`); the report
  directory's name carries seconds and is created with a `mkdir` that must
  succeed and must not find the directory already there (two runs in one
  minute never share, `vm-qa:131`'s own comment); a `$REPORT` that cannot
  be written fails the run before the first suite (`: > "$REPORT" || exit
  1`), and a write that fails later is a FAIL counted; the time bring-up
  and the fixture take is recorded as its own line under the footer
  (`bring-up Ns, fixture Ns`), outside the suite count, so the minutes a
  reader sums are the run's; the SKIP footer keeps its sentence and gains
  the exit it will give.
- **The test first** (`vm-harness-test`, cases named `exit-skip`,
  `only-unknown`, `only-empty`, `walk-empty`, `help-whole`,
  `report-unwritable`, `two-runs-one-minute`): the `ssh` double answers
  `BUILD_ID=0123456789ab` and `true`; `WALK_BASELINE` names an empty
  directory; `--skip-up --only frame-diff` under `ROCKNIX_ARTIFACTS` in the
  test's directory exits **3** with a `SKIP` row (the unfixed copy exits 0:
  the positive); `--skip-up --only nosuch` exits 2 naming `nosuch`;
  `--skip-up --only ,` exits 2; `--skip-up --only walks --walk ,` exits 2;
  `--help` names every suite `--list` prints (17 today; the case compares
  the two lists, not a number); an unwritable `ROCKNIX_ARTIFACTS` exits
  non-zero before any suite runs (the double records no call); two runs
  started in the same second write two directories.
- **Already written:** 59 reports under `/workspace/artifacts/rocknix-images/qa-*`
  carry `PASSED with N suite(s) SKIPPED` footers that their callers read
  as rc 0; they are history and are not rewritten. The catalog entries
  that cite a `vm-qa` PASS over a run with a SKIP are re-read by the
  coordinator at integration (`tools/release-catalog`, D-WORKFLOW-044) and
  the affected rows say so; nothing on a device.
- **Acceptance (#966, #982):** the seven cases by name with their
  positives quoted; `vm-qa --list` and `--help` agree; `rules-check
  --quiet` rc 0 with the new entries; `hooks-test` PASS (the pattern list
  still valid shell).
- **Commits:** `vm-qa: a SKIP exits 3, an unknown or empty selection exits 2 (#966)`,
  `vm-qa: --help whole, the report directory made once, bring-up in the minutes (#982)`,
  `doctrine: vm-harness-test in the lists (#659)`.

## S2. `vm-qa`'s bring-up, identity and tear-down: `down` and `up` are read, the guest's BUILD_ID is the image's, a run that brought the pair up takes it down, `fresh` reads the selected port (PL-04, PL-16's `fresh` half; #969, #981) -- `fix-case`

- **Why a stream:** one of the two Highs. `vm-pair down` is run with its
  output and status discarded, `vm-pair up` through `| tail -2` whose
  status is `tail`'s, and the first `SSH true` that answers is taken for
  the new guest -- so a guest that survived the `down` reports a green run
  under the requested image's name (G-02, G-30). Nothing tears the pair
  down at the end.
- **Files owned:** `tools/vm-qa` (the bring-up block `:118-125`, the
  `fresh` suite `:278-291`, the end), `tools/vm-harness-test`.
- **The shape:** `vm-pair down`'s status is read: a failure is a FAIL
  before bring-up, and S4's *nothing to stop* code (3) is not a failure;
  `vm-pair up` runs with its status read (`PIPESTATUS[0]`, or no pipe and
  the last lines kept another way), a failure exits 1 naming it; after
  bring-up the guest's `BUILD_ID` (the first ten characters, as `:124`
  reads them) is compared with the id in the image's filename
  (`g<12 hex>`) or its `.identity.json` beside it when present -- a
  mismatch exits 1 naming both; when the run brought the pair up, an EXIT
  trap runs `vm-pair down` at the end, its status in the report and in the
  exit (`--keep-up` opts out and the report says the pair was left up);
  `fresh` reads `$PORT`, not `10022`.
- **The test first** (`vm-harness-test`: `up-fails-guest-answers`,
  `build-id-mismatch`, `down-at-end`, `fresh-port`): the `vm-pair` double's
  `up` exits 1 while the `ssh` double answers `BUILD_ID=...` -- the fixed
  runner exits 1 naming the failed bring-up (the unfixed one writes a
  green report naming the requested image: the positive); `up` succeeds
  and the double's `BUILD_ID` differs from the image name's id -- exit 1
  naming both; a run that brought the pair up ends with one `down` call
  recorded by the double; `--guest b --only fresh` reaches the `ssh`
  double at port 10023.
- **Already written:** the 19 full runs in the record each began with a
  `down` whose result nobody read; whether any of them judged a surviving
  guest is not knowable from their reports (the report names the requested
  image, which is the defect) -- the coordinator notes it against the
  catalog at integration; nothing on a device.
- **Acceptance (#969, #981's `fresh` half):** the four cases with their
  positives; in the stage-E guest cycle (§ Order) the fixed runner brings
  the pair up from the `069fc2704421` image, the report's `BUILD_ID` line
  matches the image's, and the pair is down at the end with `down`'s rc 0
  in the report and the census 0.
- **Commits:** `vm-qa: read down and up, compare the guest's BUILD_ID with the image, take the pair down at the end (#969)`,
  `vm-qa: fresh reads the selected guest's port (#981)`.

## S3. The walks' preconditions and the host suites' sources: a reboot is a changed boot id and an answering interface, every seeding step is checked, only the QA cloud is matched against, a reseed follows a manifest, `ES_SRC` is compared with the image's pin (PL-08, PL-09, PL-16's ES half; #973, #974, #981) -- `fix-case`

- **Why a stream:** the walks press YES on a match dialog and run
  transfers; today they do so against whatever remote the guest has
  active, after a seeding whose failures are silent, after a reboot wait
  that neither checks a new boot happened nor fails when EmulationStation
  never answers (F-05, F-06, G-42 to G-44, G-70). The host suites that
  read `ES_SRC` judge a source nothing ties to the image (G-03, G-04).
- **Files owned:** `tools/vm-qa` (`:304-318`, `:341`, `:376-408`,
  `:476-477`, `:163-215`), `tools/vm-harness-test`.
- **The shape:** the reboot wait reads
  `/proc/sys/kernel/random/boot_id` before the reboot and requires a
  different one after, then an answering EmulationStation (the check the
  walks already use, a frame or the process), within the bound, else the
  walk FAILs naming which was missing; every seeding step's status is
  read (`set -o pipefail` in the function, each `scp` and `ssh` tested)
  and a failure fails the suite before the first walk; before `match-dialog`
  and the transfer walks the guest's active remote is read with the
  scripts' own helper and its endpoint compared with
  `cloud-test-backend`'s URL -- a mismatch refuses the walks before the
  first, naming the remote (never its credentials: the read goes through
  the dropping filter); the fixture is reseeded on a manifest (every
  file's name and sha256), not on one surviving file; a guest file the
  fixture would overwrite that is not in the manifest is a refusal naming
  it; the suites that read `ES_SRC` print its HEAD beside the image's
  EmulationStation pin (read from the build's source commit:
  `git show <BUILD_ID>:projects/ROCKNIX/packages/ui/emulationstation/package.mk`
  when the commit is present, else `(pin unreadable)`), and a mismatch
  makes those rows `SKIP` with the two hashes (a check that did not run
  on its subject has not passed, D-QA-061's words); `register`'s row says
  it ran without the interface's citations when `ES_SRC` is absent.
- **The test first** (`vm-harness-test`: `reboot-same-boot-id`,
  `reboot-es-silent`, `seed-scp-fails`, `remote-not-qa`,
  `reseed-manifest`, `overwrite-refused`, `es-src-mismatch`): the `ssh`
  double returns the same `boot_id` before and after -- the walk FAILs
  (the unfixed runner walks on: the positive); the `scp` double fails one
  seeding step -- the suite FAILs before the first walk; the double's
  `rclone.conf` names an endpoint other than the backend's -- the walks
  refuse before the first, the refusal line carrying no credential (the
  case greps for the double's stand-in value and requires its absence);
  one fixture file present, the manifest incomplete -- reseeded; a guest
  file in the fixture's path not in the manifest -- refused by name;
  `ES_SRC` at a commit other than the pin -- the ES rows read `SKIP (ES_SRC
  <a>, image pins <b>)` and the run exits 3.
- **Already written:** the walks in the record ran against the QA
  endpoint by construction of their runs (the `00` overrides), so no
  recorded run matched against a real remote; the `gb-160x144.png`
  fixture and the two rotation controls stay as they are; nothing on a
  device.
- **Acceptance (#973, #974, #981's ES half):** the seven cases with their
  positives; in the stage-E cycle the real walks suite passes its
  preconditions (the boot id changed, the remote the backend's, the
  manifest written) and the report carries `ES_SRC`'s HEAD beside the pin.
- **Commits:** `vm-qa: the reboot wait needs a new boot id and an answering interface (#973)`,
  `vm-qa: seeding checked, the QA endpoint required before a destructive walk, a manifest for the reseed (#974)`,
  `vm-qa: the ES suites compare ES_SRC with the image's pin; register says what it lacked (#981)`.

## S4. `vm-pair` and `vm-stop`: a disk is never removed while a process holds it, a missing pidfile is nothing to stop, a partial `up` rolls back, `down` stops both (PL-05; G-28; G-26 recorded; #970) -- `fix-case`

- **Why a stream:** the other High. `vm-stop` with no pidfile returns as
  if it had stopped something; `vm-pair up` then `rm -f`s every
  `vm-*.qcow2` and `.ovmf-vars.fd` under its directory -- under the shared
  default, another session's live guest's disk (G-27, G-29). A `vm-a` that
  came up when `vm-b` fails is left running; `down` stops `b` only when
  `a` stopped.
- **Files owned:** `tools/vm-pair`, `tools/vm-stop`, `tools/vm-pair-test`,
  `tools/vm-stop-test`.
- **The shape:** `vm-stop` with a missing pidfile exits **3** (*nothing
  to stop, nothing verified*) and removes nothing; before each `rm` in
  `up`, `vm-pair` checks that no process holds the file open (a scan of
  `/proc/*/fd` as the user, and of every `qemu-system-*` argv for
  `file=<path>`) and refuses naming the pid and its argv's first word;
  a partial `up` (guest `a` up, `b` failed) stops `a` through the same
  `vm-stop` and exits non-zero; `down` runs `stop_one` for both guests
  whatever the first returned and exits with the worst status; `vm-stop`'s
  compare-then-unlink is one step on one descriptor (`os.open` the pidfile,
  `fstat` and read through the descriptor, compare, `unlink` only when the
  content matched and the process is gone; a pidfile whose inode changed
  between the read and the unlink is reported, not removed) -- the window
  that remains is named in the code. **G-26 is a design, not a fix:**
  `vm-stop` identifies a QEMU by its argv and no hostile process is in the
  threat model (`vm-stop-test:29-33` runs a renamed python as an accepted
  case); the stream writes that sentence into `vm-stop`'s header and the
  Phase 7 table, and changes nothing there.
- **The test first** (`vm-pair-test`: `disk-held-no-pidfile`,
  `partial-up-rollback`, `down-stops-both`; `vm-stop-test`:
  `missing-pidfile-exit-3`, `pidfile-changed-under-us`): a fixture process
  holds `vm-a.qcow2` open with no pidfile recorded -- `up` refuses, the
  file survives, the refusal names the pid (the unfixed tool deletes the
  file: the positive, run against a copy of the tool in the test's own
  directory, never a real disk); the fixture's second launch fails -- the
  first is stopped and `up` exits non-zero; the first `stop_one` fails --
  the second still runs; `vm-stop <missing pidfile>` exits 3 (the unfixed
  tool exits 0); the pidfile rewritten between read and unlink -- reported,
  not removed.
- **Already written:** `/tmp/rocknix-vm-pair` on this host holds nothing
  today (the lane records `ls -la` in `00`); whether a past `up` destroyed
  another session's disk is not in the record (the tool prints what it
  removed only as a list of names). `worktrees.md` and
  `generic-x64-vm-testing.md` describe the stopping path as `tools/vm-stop`
  by pidfile; the new exit 3 is added to the rule's sentence in PL-22's
  packet, not here.
- **Acceptance (#970):** the five cases with their positives; the stage-E
  cycle's `down` exits 0 and the census after is 0; `vm-pair-test` and
  `vm-stop-test` rc 0 (the CI's `fork-checks.yml:47` reads `vm-pair-test`).
- **Commits:** `vm-stop: a missing pidfile is nothing to stop (exit 3); one descriptor from read to unlink (#970)`,
  `vm-pair: refuse to remove a disk a process holds; roll a partial up back; down stops both guests (#970)`.

## S5. The host state belongs to the worktree: the pair's disks, the QA cloud's state, the run's scratch files and the report under the checkout that runs them; sockets under the runtime directory; a held port is a refusal (PL-06, PL-21's `ROCKNIX_ARTIFACTS`; #971, #979's path half; D-INFRA-031) -- `fix-case`

- **Why a stream:** every default assumes one session on the host, and
  this host has two lanes and the M7 lane as one user (D-WORKFLOW-183): the
  pair's disks in a 30 GiB RAM tmpfs (`findmnt /tmp`), fixed sockets,
  pidfiles and ports, the QA cloud's state per user and reset by the walks,
  predictable `/tmp` files, one report directory per minute (F-09, F-10,
  G-05, G-17, G-53). S4 stops the deletion; this stream stops the sharing.
- **Decided (D-INFRA-031):** `VM_PAIR_DIR` defaults to the tool's own
  checkout's `.qa-scratch/vm-pair` (`$ROOT/.qa-scratch/vm-pair`;
  `/.qa-scratch/` is gitignored at `.gitignore:63`, and the checkout's
  filesystem is `/workspace`, not a tmpfs); `VM_QEMU_RUNTIME_DIR` defaults
  to `${XDG_RUNTIME_DIR:-/tmp}/pixelelated-vm-<first 8 hex of sha256 of
  $ROOT>` (a unix socket path is capped at 107 bytes; the checkout's path
  is already 78), written to `$VM_PAIR_DIR/RUNTIME` by `up` and read back
  by `down`, `info`, `ssh`, `serial`, `reimage` and by every tool that
  opens the sockets by their default (`vm-qa`, `time-to-play`,
  `ra-offline-test`, `emulator-exit-test`, `vm-visual-qa`); `vm-qa` exports
  `CLOUD_QA_STATE=$ROOT/.qa-scratch/cloud-qa` when it is unset (the
  backend's own default under `~/.cache` is its owner's -- a lead the
  coordinator carries, below); the fixed ports (10022, 10023, the VNC
  displays, the backend's port) are probed before a launch (`ss -ltnp`)
  and a holder is a refusal naming its pid, never a silent collision; the
  report root stays `${ROCKNIX_ARTIFACTS:-/workspace/artifacts}/rocknix-images`
  with S1's seconds; `vm-upgrade-rehearsal` reads `ROCKNIX_ARTIFACTS` as
  `vm-qa` does (`:30`); the host's scratch files (`time-to-play:137-139`,
  `ra-offline-test:259`, `:345`) move under the run's own directory. An
  explicit value of any of these is honoured as before, so a checkout that
  sets `VM_PAIR_DIR=/tmp/rocknix-vm-pair` keeps working; nothing under the
  old defaults is moved or removed.
- **Files owned:** `tools/vm-pair`, `tools/vm-qa`, `tools/time-to-play`,
  `tools/ra-offline-test`, `tools/emulator-exit-test`, `tools/vm-visual-qa`,
  `tools/vm-upgrade-rehearsal` (the path lines only), `tools/vm-harness-test`;
  `vm-pair info` prints the paths it resolved (the acceptance's *paths
  printed*).
- **The test first** (`vm-harness-test`: `two-checkouts-two-states`,
  `runtime-recorded`, `port-held-refused`, `no-tmp-writes`,
  `rehearsal-artifacts-root`): two scratch copies of the tools at two paths
  -- `vm-pair info` prints two different `VM_PAIR_DIR`s and runtime
  directories; `up`'s runtime directory is read back by `down` from
  `RUNTIME`; a fixture listener on 10022 -- `up` refuses naming the pid
  (the unfixed tool launches the double and fails later with a different
  message: the positive); `find /tmp -newer <marker>` before and after the
  whole `vm-harness-test` run lists nothing of the run's;
  `ROCKNIX_ARTIFACTS=<scratch> vm-upgrade-rehearsal` with the doubles
  writes under `<scratch>` (the unfixed tool writes under
  `/workspace/artifacts`: the positive, read from the double's recorded
  paths, never by writing there).
- **Already written:** `~/.cache/rocknix-cloud-qa` and `/tmp/rocknix-vm-pair`
  on this host are left as they are (the M7 lane's older checkout may use
  them by the old defaults; the host file coordinates until it adopts,
  as D-INFRA-029 said of the admission registry); the lane's own
  `/workspace/tmp/m6-t12/` overrides from the cycle are superseded by the
  defaults and said so in `00`; nothing on a device.
- **Acceptance (#971, #979's path half):** the five cases with their
  positives; the stage-E cycle runs `vm-qa <image>` from the lane's
  worktree **with no override set**, and the report's header prints the
  five paths it used, all under the worktree or `/run/user/1000`.
- **Commits:** `vm-pair: the state under the checkout's .qa-scratch, the runtime directory recorded, a held port refused (#971)`,
  `vm-qa, time-to-play, ra-offline-test, emulator-exit-test, vm-visual-qa: the run's files under the run; the QA cloud's state under the checkout (#971)`,
  `vm-upgrade-rehearsal: ROCKNIX_ARTIFACTS as vm-qa reads it (#979)`.

## S6. `time-to-play` measures or fails: `--repeat` below 1 and an empty `--only` refused, a sync timed only on a completed stamp, g2g needs its stamp, every cell that ran is judged, a launch starts from no RetroArch (PL-02; G-11, G-13 to G-16; #967, #983; D-QA-062) -- `fix-case`

- **Why a stream:** the measurement the register's one budget reads
  (D-CLOUD-119) accepted `--repeat 0` with empty cells at rc 0 (P8), a g2g
  row with stamp `-` and token `?` as PASS, a failing sync's stamp as a
  timing, and a launch over a RetroArch already running (F-02, G-08 to
  G-12).
- **Decided (D-QA-062):** every cell that ran is judged -- a cell that
  ran and produced no number fails the run and the report says which (the
  rule D-QA-022 made for the three headlines, applied to the cells that
  ran); the headline set and the one budget are unchanged, D-CLOUD-122
  stays open; the exit sync is timed only on a completed stamp (its rc
  field 0 or 9 and its token read; a failing stamp's row reads the token
  and is not a measurement); g2g requires its stamp; `--repeat` below 1
  and an `--only` naming no cell are usage errors (exit 2).
- **Files owned:** `tools/time-to-play`, `tools/vm-harness-test`.
- **The shape:** the five seat items with it: `scaled` left `None` by a
  failed panel read fails surface qualification instead of passing it
  (G-11, `:309`, `:1316-1318`); `seed_payload` honours `--rom` (G-13);
  `/tmp/ttp-kill` is reinstalled after the startup reboot and
  `kill_game()`'s status is read (G-14); the guest mutations and the backup
  `scp` move inside the `try` after the signal handlers are installed, and
  the `scp`'s status is read (G-15); `restore()` removes the seeded saves,
  puts `rclone.conf` back whenever a saved copy exists and records an
  empty marker when none did, and `read_routes` keeps every family's rows
  (G-16); a launch cell first asks the guest for a running `retroarch` and
  ends it through the guest's own helper, recording that it did.
- **The test first** (the four constructed logs the tool already has, plus
  `vm-harness-test`: `repeat-zero`, `only-empty`, `sync-stamp-failed`,
  `g2g-no-stamp`, `cell-ran-unmeasured`, `scaled-none`): `--repeat 0` exits
  2 (the unfixed tool exits 0 with empty cells: P8, the positive); a
  constructed exit-sync stamp with a non-zero rc is reported by its token
  and not timed; a g2g row without its stamp fails; a constructed run
  whose `launch` cell has no number fails with the cell named; a surface
  read returning no panel fails qualification.
- **Already written:** the record's `time-to-play.md` files with dashes
  over PASS and `docs/vm-qa-log.md`'s entries stand as history; the rows
  the cycle produced are re-read by the lane in `02` and marked (*would
  fail under D-QA-062*) without rewriting them; no budget changes; nothing
  on a device.
- **Acceptance (#967; #983's G-11, G-13 to G-16):** the six cases with
  their positives; in the stage-E cycle `--quick` on guest `a` once: every
  row measured or the run fails, the exit sync's stamp completed, and the
  report's numbers go under the `vm-qa` footer as before.
- **Commits:** `time-to-play: --repeat below 1 and an empty --only refused; a sync timed only on a completed stamp; g2g needs its stamp; every cell that ran is judged (#967)`,
  `time-to-play: scaled None fails qualification, --rom honoured, the kill helper reinstalled, mutations inside the try, restore complete (#983)`.

## S7. `emulator-exit-test` and `device-act` refuse what they cannot prove (PL-03, PL-13; #968, #978) -- `fix-case`

- **Why a stream:** two small tools with the same shape: a selection that
  checks nothing prints PASSED (`--only X`, P9), and a recorder that
  cannot write its BEGIN line acts anyway and prints *recorded* (G-59 to
  G-61), with the whole command -- a credential included -- in its log.
- **Files owned:** `tools/emulator-exit-test`, `tools/device-act`,
  `tools/vm-harness-test`.
- **The shape:** `--only` with no part among A to D exits 2 naming it;
  part D either constructs the marker case itself or exits 2 saying it
  runs only after A to C (the lane's choice, said in `--help`);
  `device-act` refuses to act when BEGIN cannot be written (exit non-zero
  before `ssh`), fails the run when END cannot be written and prints
  *recorded nothing*, logs the command through the mask
  (`sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'`, the
  expression `engineering-practices.md` gives), and says in its timeout
  line what the timeout supervises.
- **The test first** (`vm-harness-test`: `exit-only-unknown`,
  `exit-only-d-alone`, `act-begin-unwritable`, `act-end-fails`,
  `act-masked`): `--only X` exits 2 (the unfixed tool: PASSED, rc 0 --
  P9, the positive); `--only D` alone constructs or refuses, as chosen;
  with a fixture `ssh` on `PATH` that records its calls and an unwritable
  `DEVICE_ACTIONS_LOG`, the fixed tool exits non-zero and the fixture
  recorded no call (the unfixed one runs the command and prints
  *recorded*: the positive); an END write made to fail -- non-zero and
  *recorded nothing*; an argument `key=zzqq-standin` -- the log line
  carries `key=***` and the string `zzqq-standin` appears nowhere in it
  (the proof is the absence). **Never against a device** (D-QA-015): the
  fixture `ssh` is the only target.
- **Already written:** `/workspace/artifacts/rocknix-device-actions.log`
  holds every past act's full command; the coordinator reads it through
  the dropping filter at integration and redacts a line that carries a
  credential shape, recording the count (#962's family); nothing on a
  device.
- **Acceptance (#968, #978):** the five cases with their positives.
- **Commits:** `emulator-exit-test: --only needs a known part; D says what it needs (#968)`,
  `device-act: no act without its BEGIN, END's failure fails the run, the command masked in the log (#978)`.

## S8. `vm-visual-qa` and `vm-serial`: a missing frame fails, a walk counts its frames, a serial command returns its status, every channel has a deadline (PL-07, PL-11; G-35, G-39; #972, #976, #983) -- `fix-case`

- **Why a stream:** a failed `screendump` returns `None`, `wait-for-change`
  counts that as 100 % change and a landed key, a walk that captured fewer
  frames than its steps name exits 0, `vm-serial sh` returns 0 whatever the
  command did, and no SSH or serial call has an execution bound (G-32 to
  G-37, G-41).
- **Files owned:** `tools/vm-visual-qa`, `tools/vm-serial`,
  `tools/vm-walks/cloud-epic/vnc-grab.py` (G-35's half), `tools/vm-pair`
  (the key install `:110`), the `ssh` call sites in `tools/vm-qa`,
  `tools/emulator-exit-test`, `tools/ra-offline-test`,
  `tools/time-to-play` (the bound only), `tools/vm-harness-test`.
- **The shape:** `wait-for-change` with a `None` frame is a failure (never
  a change); a walk that captured fewer frames than its step file names
  exits non-zero naming the missing ones; the PPM header loop ends at EOF
  with an error; VNC coverage counts distinct pixels (or rows), not
  rectangle areas (G-35), and `vnc-grab.py` returns an incomplete
  framebuffer as a failure, not zero-filled; `dismiss_dialogs` ends on a
  checked state, never on GO TO announced as the carousel (G-39);
  `vm-serial sh` wraps the command with an exit marker and returns that
  status; `vm-pair`'s key install fails when `vm-serial sh` fails; every
  `ssh` the harness runs gets an execution bound (`timeout <n>` around the
  call, or the tool's own deadline) and the drains an absolute deadline.
- **The test first** (`vm-harness-test`: `screendump-fails`,
  `fewer-frames`, `ppm-truncated`, `serial-false`, `ssh-never-ends`,
  `vnc-partial`): a monitor-socket double that accepts `sendkey` and fails
  `screendump` -- the fixed walk exits non-zero at the first
  `wait-for-change` (the unfixed one exits 0: the positive); a walk whose
  steps name three frames and the double yields two -- non-zero naming the
  third; a truncated PPM -- an error, not a hang; a serial double
  answering `false` with its marker -- `vm-serial sh false` exits non-zero
  (the unfixed tool: 0); an `ssh` double that sleeps past the bound -- cut
  at the bound with the bound named; a VNC double sending half the
  framebuffer -- a failure.
- **Already written:** every recorded walk frame set stands; whether a
  recorded walk lost a frame silently is read by the lane in `02` from the
  frame counts against the step files for the accepted baseline
  (`d72084ccad`) and said; nothing on a device.
- **Acceptance (#972, #976; #983's G-35, G-39):** the six cases with their
  positives; in the stage-E cycle `vm-serial sh false` on guest `a` exits
  non-zero and the walks suite's frame counts equal its step files'.
- **Commits:** `vm-visual-qa: a missing frame fails; a walk counts its frames; the header loop ends (#972)`,
  `vm-serial: sh returns the command's status; the channels have deadlines (#976)`,
  `vm-visual-qa, vnc-grab: coverage by pixel, a partial framebuffer fails, dismissal ends on a checked state (#983)`.

## S9. `ra-offline-test` and `qa-accounts`: the account goes where `--host` says, cleanup runs and counts, a negative check needs a read, matches are exact, the endpoints are one guest's (PL-12; G-45, G-58; G-52 recorded; #977, #983) -- `fix-case`

- **Why a stream:** the suite that proves an achievement earned offline
  reaches the server sends the QA account to `127.0.0.1` with the default
  key whatever `--host` says, has no EXIT trap, lets a failed read pass a
  negative check, and matches `flushed=` and the id loosely (G-50 to G-57).
- **Files owned:** `tools/ra-offline-test`, `tools/qa-accounts`,
  `tools/vm-harness-test`.
- **The shape:** host, port and key are passed to `qa-accounts`
  (`--host`, `--port`, `--identity`); an EXIT trap runs cleanup and counts
  its failures into the result; a negative check requires a successful
  read first (rc 0, then the absence); exact matches for `flushed=<n>` and
  the achievement id (anchored); every requested capture is checked by
  name; the five endpoint flags stay for a hand run and are checked for
  consistency (the pidfile's QEMU argv names the ssh port and the serial
  socket; a disagreement is a refusal), and `--guest <letter>` derives them
  as `vm-qa:105-110` does (G-45); `qa-accounts` reads back equality with
  what it set, not non-emptiness, and reads back `global.retroachievements`
  too (G-58). **G-52 is a design:** one QA account across guests, an
  opt-in suite one lane runs at a time, coordinated by the host file; the
  stream writes that into the tool's header and the Phase 7 table.
- **The test first** (`vm-harness-test`: `negative-read-fails`,
  `host-passed-through`, `cleanup-counted`, `flushed-exact`,
  `endpoints-inconsistent`, `accounts-readback`): an `ssh` double that
  fails during a negative check -- the check FAILs (the unfixed tool
  passes it: the positive); `--host 127.0.0.2` -- the `qa-accounts` double
  records that host and the given key; a cleanup step made to fail -- the
  result is FAIL; `flushed=10` against an expected `1` -- FAIL (the unfixed
  substring match passes); a port and a serial that name different guests
  -- refused; `qa-accounts` against a `get_setting` double returning
  another value -- FAIL. **The account path never runs in the lane**
  (brief § 8; the pointer): no `qa-accounts` call reaches a guest, and no
  credential file is read -- the doubles carry stand-in words.
- **Already written:** the QA account's state on the RetroAchievements
  side is untouched by this stream; the real-account proof stays the
  release procedure's (step 3, `release-candidates.md:64`) with the
  coordinator's yes; nothing on a device.
- **Acceptance (#977; #983's G-58):** the six cases with their positives.
- **Commits:** `ra-offline-test: host and key through to qa-accounts, cleanup on EXIT and counted, negative checks need a read, exact matches, one guest's endpoints (#977)`,
  `qa-accounts: read back equality, and the achievements switch (#983)`.

## S10. `vm-upgrade-rehearsal`: a positive archive count before and after, seeded files compared by size and hash, a failed stop fails (PL-14; G-30's stop; #979) -- `fix-case`

- **Why a stream:** the rehearsal every candidate runs (`release-candidates.md`
  step 3) passes *backup archive kept* at zero archives before and after,
  checks that the seeded files' hashes exist rather than match, and
  ignores its stop's failure (G-66, G-30).
- **Files owned:** `tools/vm-upgrade-rehearsal`, `tools/vm-harness-test`.
- **The shape:** the archive count before the update is positive or the
  rehearsal fails before updating; after the update the count and the
  names match; every seeded file's size and sha256 are compared with the
  seed's own manifest; a failed stop makes RESULT FAIL. (The
  `ROCKNIX_ARTIFACTS` line is S5's.)
- **The test first** (`vm-harness-test`: `rehearsal-no-archive`,
  `rehearsal-hash-changed`, `rehearsal-stop-fails`): with `ssh` and `scp`
  doubles, a backup creation that fails -- RESULT FAIL (the unfixed tool:
  RESULT PASS, the positive); a seeded file whose hash the double returns
  changed -- FAIL naming it; a stop that fails -- FAIL. The real rehearsal
  from a previous image is the release procedure's and is not run here.
- **Already written:** the 19 recorded rehearsals (PASS every cut) are
  re-read by the lane in `02` for their archive counts, and a run whose
  count was zero is listed (*would fail under S10*); nothing is
  rewritten; nothing on a device.
- **Acceptance (#979):** the three cases with their positives.
- **Commits:** `vm-upgrade-rehearsal: a positive archive count, sizes and hashes against the seed, a failed stop fails (#979)`.

## S11. `frame-diff`, the masks and the claims: an empty baseline is refused, masks name screens, a proposal is inert, the sentence matches the flag, a scoped run compares its walks, a zero-size PNG is refused (PL-15; G-24; #980) -- `fix-case`

- **Why a stream:** the comparator every candidate's walks are judged by
  passes an empty baseline, masks whole walks (`masks.txt:7-9`), treats
  `PROPOSAL ONLY` claims as live (`claims.txt:38-40`, `:77-89`), says one
  thing about `--min-pixels` and does another, and compares a scoped
  `--walk` run against the whole baseline (F-18, G-19 to G-25).
- **Files owned:** `tools/frame-diff`, `tools/vm-walks/masks.txt`,
  `tools/vm-walks/claims.txt`, `tools/vm-harness-test`.
- **The shape:** a baseline with `BASELINE.txt` and no frame exits 1; the
  three transfer masks are narrowed to the frames and boxes they cover,
  with the boxes recorded in the mask's comment; a claim carrying the
  proposal marker is parsed as inert until the marker is removed (the
  claims file says so at its head); `--min-pixels`'s sentence and
  comparison agree; a compare over a scoped walk set reads the walks that
  ran (from the run's directory) and compares only those; a PNG whose width
  or height is 0 is refused (G-24). **Moving the baseline and pruning
  claims is the maintainer's** (`frame-diff accept`; the three whole-frame
  claims on the month-old `d72084ccad` baseline): the coordinator puts it
  on #346; the stream changes no claim's substance.
- **The test first** (`vm-harness-test`: `baseline-empty`,
  `mask-narrowed`, `proposal-inert`, `min-pixels-sentence`,
  `scoped-compare`, `png-zero`): an empty baseline with `BASELINE.txt` --
  exit 1 (the unfixed tool passes: P5, the positive); a change inside the
  old transfer mask on `run-transfer/01-cloud-hub.png` -- reported; a
  proposal claim's condition violated -- not reported until the marker is
  removed; a 0x0 PNG with a valid IDAT -- refused; a scoped run with one
  walk -- the report names one walk compared; the missing-claim control
  still exits 1.
- **Already written:** the accepted baseline and the 391 claims are
  unchanged in substance; a walk masked whole until now may have hidden a
  change in the accepted baseline's own frames -- the lane runs the fixed
  compare over the baseline against itself and the last accepted run and
  lists what the narrowed masks now show, for the coordinator's read;
  nothing on a device.
- **Acceptance (#980):** the six cases with their positives; the fixed
  compare's report over the stage-E cycle's walks.
- **Commits:** `frame-diff: an empty baseline is refused, a scoped compare follows the walks run, --min-pixels says what it does, a zero-size PNG is refused (#980)`,
  `vm-walks: the transfer masks name their screens; a proposal claim is inert (#980)`.

## S12. The `assert` class: seven tools refuse with a check that survives `-O` (PL-10; G-67; #975, #983) -- `fix-case`, one commit per tool

- **Why a stream:** `vm-manager-system-check` refuses with `assert`, so
  `PYTHONOPTIMIZE=1` turns every refusal into a PASS (P6); six more tools
  check the same way (`ra-ui-test`, `raofflineproxy-consent-test`,
  `raofflineproxy-installed-native-test`, `vm-pair-test`, `vm-stop-test`,
  `vm-upgrade-readiness-test`), and the consent test asserts before it
  records the event it is asserting about (G-67).
- **Files owned:** the seven tools, `tools/vm-harness-test`.
- **The shape:** each refusal is an explicit check that raises or exits
  with its message; a tool whose checks the lane cannot all rewrite in the
  stream refuses to run under optimisation instead (`sys.flags.optimize`
  non-zero: exit 2 naming it); the consent test records the event before
  it judges it. One commit per tool, so a revert is one tool.
- **The test first** (`vm-harness-test`: `optimize-<tool>` for each):
  `echo '[]' | PYTHONOPTIMIZE=1 tools/vm-manager-system-check nes gb`
  exits 1 (the unfixed tool: PASS -- P6, the positive); each of the other
  six, under `PYTHONOPTIMIZE=1`, still fails its own failing case or exits
  2 refusing to run; the consent test's declined case records its event
  when the collector raises.
- **Already written:** the CI runs `vm-pair-test` and
  `vm-upgrade-readiness-test` (`fork-checks.yml:47-48`) without `-O`, so
  no recorded CI pass was hollow on this account; nothing on a device.
- **Acceptance (#975; #983's G-67):** the seven cases with their
  positives; the seven tools' own controls rc 0.
- **Commits:** `<tool>: refusals survive -O (#975)` seven times;
  `raofflineproxy-consent-test: record the event before judging it (#983)`.

## S13. The small fixes, one commit per tool (PL-18's remaining ids; #983) -- `fix-case`

- **Why a stream:** each is a line the seat found and the lane verified
  (`seat-verify.md`), each with a constructed input; none changes what a
  tool is for.
- **Files owned and the shape:**
  - `tools/signin-memory` (G-47): the launch's status is read, the page
    marker is cleared before the run, the log is the run's own, and a
    process is matched by start time as well as name;
    `tools/es-launch-memory` (G-47): the oldest-name match carries the
    start time.
  - `tools/png-blackout` (G-62): an empty or off-image rectangle is a
    refusal, never *painted out*; the text chunks (`tEXt`, `iTXt`, `zTXt`)
    are dropped from the output -- the tool exists so a frame carrying a
    QA account's name can be filed, and a text chunk can carry the name
    too.
  - `tools/es-untranslated` (G-63, G-64): an unreadable current source is
    a failure, an empty current source is refused as the upstream one is,
    and a fuzzy or `msgctxt` entry does not count as French.
  - `tools/es-syntax-check` (G-65): the compile line must have changed
    after the substitution or the check fails, and the farm's `cp -rs`,
    `mkdir` and `ln -sfn` statuses are read.
  - `tools/ra-candidate-games` (G-68): the bare-list response is handled
    (one line; the tool's fate is PL-19's disposition below, and a fixed
    line costs a retirement nothing).
  - `tools/font-stems` (G-69): a reversed size range is a usage error, a
    glyph that fails to load is counted and reported, never dropped
    silently.
- **The test first** (`vm-harness-test`, one case per id): each
  constructed input recorded failing on the unfixed tool and passing on
  the fixed one -- a 0-width rectangle to `png-blackout` (the unfixed
  tool prints *painted out*: the positive); a `.po` with a `#, fuzzy`
  entry and a `msgctxt` entry counted as untranslated; a compile line
  the substitution cannot change -- FAIL; `[]` to `ra-candidate-games`'s
  parser; `--sizes 20 10` to `font-stems` -- exit 2.
- **Already written:** the frames filed with `png-blackout` in the
  record keep their text chunks; the coordinator lists them at integration
  (`find docs -name '*.png' | xargs -I{} sh -c 'grep -c tEXt {}'`-shaped,
  through the standard library) and the ones carrying text are re-filed;
  `es-untranslated`'s past counts may have been low by the fuzzy entries
  -- the fixed tool's count on the current ES pin is recorded in `02`;
  nothing on a device.
- **Acceptance (#983):** every id's case with its positive.
- **Commits:** one per tool, `<tool>: <the fix> (#983)`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-19 (what nothing runs, what has caught nothing).** Decided per
  row, the maintainer's veto open on #346 (D-QA-040 names the maintainer;
  preservation over deletion, `working-principles.md`):
  - **`signin-memory`:** kept; its caller is `release-candidates.md` step 3's
    webkitgtk proof (*the sign-in window for webkitgtk*), which names the
    proof and not the tool -- the rule edit naming it is PL-22's packet.
  - **`es-launch-memory`:** kept (it caught #310); its caller becomes step
    3 for a candidate whose EmulationStation pin moved -- PL-22's packet.
  - **`font-stems`:** kept as a by-hand measurement (blindspot 54 was its
    catch); the index row says when it is run (a font or a size changes) --
    PL-22's packet.
  - **`raofflineproxy-installed-native-test`:** kept; its caller becomes
    the proxy-refresh line beside `raofflineproxy-integration-test` --
    PL-22's packet.
  - **`ra-candidate-games`:** **retirement proposed** to the maintainer on
    #346: no caller, no catch, no positive, and its output (the chosen
    titles) lives in the fixtures; its record stays under `docs/`. It is
    not removed until the maintainer answers; G-68's one-line fix lands
    (S13) meanwhile.
  - **The six suites with nothing recorded** (`lifetime`, `wrapper`,
    `pair-identity`, `exit`, `time-to-play`, `ra-offline`): all kept, with
    the reason recorded: five have a constructed positive and cost under
    half a minute each; `ra-offline` gets its positive from S9's
    constructed refusals. A guard with a positive and no catch is a guard
    that has not yet been needed, not one that has failed.
  - **`vm-walks/cloud-epic/migration-protocol.sh` and `vnc-grab.py`:**
    their only caller is T14's `rasteratops-vm-cloud-epic` (`:149`, `:67`);
    their fate is joined to T14's stage-D proposal on that tool (the
    coordinator's, on #661) and nothing is removed here; G-35's `vnc-grab.py`
    fix (S8) lands regardless.
  - The coordinator files the **Backlog issue** that holds these
    dispositions, so *what we deliberately keep, and why* is findable.
- **PL-20 (the cost):** a **Backlog issue the coordinator files at this
  pause**: guest `b` on demand (up for `pair-identity` and `--guest b`
  only, down after), the host suites beside the guest suites, and the
  accepted baselines' retention (D-INFRA-022; the `du` and count from
  `02`). Not a stream: the saving is 8 GiB of RAM for 33 minutes in a
  window the host file already serialises, and restructuring the run
  while S1 to S3 fix its accounting is two changes to one exit code.
- **PL-21:** `es-syntax-check:53` is #640's (the lane posted it); the
  `ROCKNIX_ARTIFACTS` half is S5.
- **PL-22 (the rules and the index):** a **Backlog issue the coordinator
  files at this pause** for the rule edits made at integration in the
  doctrine packet after T4's merge: the index's six pointers to a rule
  that never names them (`q7-descriptions.txt`), `generic-x64-vm-testing.md:115`'s
  raw `kill` (to `tools/vm-stop` and its exit 3), `vm-first.md:59`'s *four
  suites* (to the list), `release-candidates.md` step 3's *every suite* (to
  rc 0 only, D-QA-061) and the callers PL-19 adds. Rule edits are not this
  lane's (brief § 8) except the three list entries S1 makes for the new
  control.
- **PL-23 (the seat's narrowed items):** G-07 (`register`'s mDNS line
  reads a past log line): a design documented at `vm-qa:247-255`, kept; a
  lead for #50's row, noted in the table. G-23 (alpha dropped before the
  compare): the frames are RGB; nothing to do. G-24: S11. G-26: S4 records
  the design. G-28: S4. G-38 (settling is a heuristic): the design (#125),
  kept. G-45: S9. G-46 (guest-side `pkill` by anchored pattern on a
  disposable QA guest): kept with the reason written into each tool's
  comment -- the processes are the test's own on a guest the test owns,
  and `engineering-practices.md`'s pidfile rule governs the host's
  processes. G-48 (growth, not peak): the documented bound, kept. G-52:
  S9's header. G-69: S13.
- **The seat's one withdrawn item:** nothing.
- **For the maintainer, on #346 (the coordinator posts them at this
  pause):** the three contract rows (D-QA-061, D-QA-062, D-INFRA-031) for
  veto; the `ra-candidate-games` retirement; the baseline move and the
  pruning of the three whole-frame claims (`frame-diff accept`, the
  maintainer's call under S11).
- **A lead carried by the coordinator:** `cloud-test-backend`'s own state
  and port defaults (`:82`, `:93`) are its owning slice's; S5 sets them
  from the caller.

## Order, the one guest cycle, and the hand-back

S1, S2, S3 first and in that order (the runner; `vm-harness-test` grows
with each); **S4 before S5** (the deletion is stopped before the defaults
move); S5; then S6 to S11 in any order; S12; S13 last. Each commit cites
its bugs (`Refs #N, #659`, no closing keyword: a bug closes when its fix is
on `next`) and carries the attribution line; `git status --short` before
every `git add -A` (`.qa-scratch/` is gitignored; the positives and the
doubles stay there).

**The stage-E guest cycle: one, the pair, after S5, after M7's return.**
The host file carries the coordinator's grant to the M7 lane (20:44 UTC,
bounded 22:15 UTC); the cycle starts only after M7's return line is on the
file, with the census read (`pgrep -c -x qemu-system-x86` 0) and `free -g`
recorded in `00`. Then, from the lane's worktree with **no override set**
(D-INFRA-031's defaults are the proof): the host file line before; the
`069fc2704421` image from `/workspace/artifacts/m6-t1-20261023/` checked
against its `.img.gz.sha256`; `tools/vm-qa <image>` whole with the default
suites (never `link` or `ra-offline`) by the fixed runner, which brings the
pair up, runs, and takes it down; in the same window before the `down`, the
guest acceptances S6 (`--quick` once), S7 (`--only A` on the guest), S8
(`vm-serial sh false`) and S3's walk preconditions run on guest `a`; the
report's header prints the five paths; `vm-stop`'s and `down`'s rc in `00`;
the census after; the host file line after; the disks under
`.qa-scratch/vm-pair` and the image copy retired after their record
(D-INFRA-022). It is bounded at 60 minutes from `up`. **A second cycle
needs a line on #659 first**, and no guest starts while another lane's or
M7's is up on the host file.

After S13: the Phase 7 table and the `punch_index` at their outcomes
(`fixed`, `deferred` with its issue, `design` with its sentence), `02`
§ The suites re-run (`vm-harness-test`, `vm-pair-test`, `vm-stop-test`,
the seven tools' controls, the cycle's report), the lint on the folder
(`PASS`, the default phase), `fixed-at:` in #659's body, the retro (stage
G, posted on #659: what the slice did to the two time-to-play numbers --
nothing to the numbers, and the cells now fail when unmeasured; what each
stream did to a refusal -- the list), then the hand-back comment naming the
tip and each artifact by path. The coordinator accepts by
`AUDIT_ISSUE=984 $S/t12-accept.sh <tip> <coordinator tip>` on an export
(membership, line counts, the three no-guest controls and
`vm-harness-test` at the tip and on the simulated merge with the
coordinator's branch, `register-check`, `rules-check --quiet`,
`work-log-index --check`, the lint), reads every stream's diff and
positives, ticks #659 and #984 from the artifacts, closes #984 when its
checkboxes read back ticked by name, and merges the branch in its turn
(after T10's, before T14's); the catalog re-read and the device-action
log's redaction S1 and S7 surface are the coordinator's, made at the
merge.
