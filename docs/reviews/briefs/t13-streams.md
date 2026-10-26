# T13's remediation streams (#660, audit issue #1073)

Written by the coordinator on 2026-10-25 at T13's stage-D pause
(D-WORKFLOW-189), in the shape of `t15-streams.md`: three streams, each with
the files it owns, the test first, its `Already written:` line, its
acceptance and its commits; then the one guest cycle the slice still owes
and what it now carries; then the dispositions that are not streams; then
the order and the hand-back. The lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-harness-660`,
branch `feature/m6-cloud-harness-660`, stage-D tip `8a2518fa44`, the
rulings applied). **Review depth per stream: Local** (plan § 6c; the
Independent seat sat at stage C and does not sit again). The harness is its
own test, so **a stream lands with a case whose constructed input fails on
the unfixed file and passes on the fixed one, or it is not a stream** -- the
positive produced on the host against a copy of the file at `8a2518fa44`
(from a clone or `git worktree add --detach`, never `git archive`; or the
function extracted into a scratch module with its inputs stubbed), and
quoted in `02` § The streams' positives with the command, the exit and the
line. Where only a guest can show the behaviour, the host half is proved in
the stream and the guest half in § The guest cycle below; until that run the
bug's checkbox stays open with the stream's note (`vm-first.md`: a proof of
the path is not a proof of the input). `TMPDIR` under `/workspace/tmp/m6-t13/`;
every backend brought up under the isolation the lane already uses
(`CLOUD_QA_STATE=/workspace/tmp/m6-t13/state`, `CLOUD_QA_PORT` 9080 / 9083 /
9082, `CLOUD_QA_NAME=rocknix-cloud-qa-m6t13`, `CLOUD_QA_S3_UPSTREAM_PORT=9092`,
option first: `tools/cloud-test-backend --backend <b> <subcommand>`) and
taken down by the same tool before the stream's commit, with the leftover
check (`ss -ltn` on 9010-9099, `docker ps -a` for `rocknix-cloud-qa*`,
`pgrep -f` on the three service lines) in `00`.

**Nothing here runs a guest before the window (§ The guest cycle), a
provider, a handheld action, a build, `tools/council/run invoke`, an edit to
any file but the nine (`cloud-harness.md` § 1 line 147; T12's `vm-qa` and
T10's guards are read, never edited), to a rule, a decided register row or
`CLAUDE.md`, or a write under `/workspace/repos/rocknix*` or `/tmp`.** A
fixture that must look like a credential is assembled at run time, never
written as a literal (`engineering-practices.md` § Guards must fail closed;
the pre-commit refuses it). `rm -rf` only as `"${X:?}"/...` or a literal
path, in its own short command; `--real-roms` never.

**The lane's question, answered first.** The four guest criteria (#1062
KILL1 to its verdict, #1064 step 25's floor, #1069 A15 to its verdict,
#1070 KILL5 at two keeps) **fold into the held window's one cycle**, with
#1057's A5/RETENTION SKIP and #1065's CAP13 present/absent pair beside
them: a bug fixed to the best of our ability is closed on a VM artifact
(`bugs-are-agent-first.md`), and "the next qualification run" has no owner.
The cycle grows by the fifteen minutes the lane estimated and keeps its
bound (below). The host halves are proved in the streams now.

**What the lane found, in one sentence each, so the streams read in order:**
the backend tool accepts `--backend` after the subcommand in silence and
answers for another backend (#1058); its SFTP endpoint is not confined and
its guest key authenticates as the host's own user (#1067, High); its
stanzas fall back to the clear password when `rclone obscure` fails
(#1068); its `ls` and `reset` report a failure as an empty endpoint (#1060's
backend half); the harness's step 8 refuses an occupied `/storage/roms/vectrex`
and its cleanup then deletes it (#1066, High); its absence-only checks pass
on a failed listing (#1060's harness half); KILL1 raises `NameError` before
its verdict and its preservation predicate passes a deleted cloud file
(#1062); CONTRACT's dry-run guard fires on every dry run (#1063); A5 and
RETENTION call `cloud_reconcile`, which has never existed, and RETENTION
prints two PASS lines when nothing ran (#1057); the verdict line does not
account for what it checked (#1059, with PL-15's backend capabilities);
step 25 passes on an empty probe (#1064); CAP13's warning check yields 0
twice (#1065); A15 uploads plain bytes named `.tar.gz` (#1069); KILL5
expects three archives whatever `CLOUD_BACKUP_KEEP` says (#1070);
`cloud-connections-test` carries a credential-shaped literal at rest
(#1061); and `cloud-census` runs `cloud_device_id`, which writes (#1081).

## S1. `cloud-test-backend`: the entry parses, the SFTP endpoint is confined, the stanzas never fall back, a failure is never an empty listing (#1058, #1067, #1068, #1060's backend half)

- **Why first:** every later re-run enters through #1058's parsing, and
  #1060's harness half has nothing to read until `ls` exits non-zero on a
  failure (the digest's dependency 1 and 6).
- **Files owned:** `tools/cloud-test-backend` (the CLI at its `argparse` or
  option loop; the SFTP service `:137-139`, `:396-397`; the stanza writers
  `:742-762`; `ls`/`reset` `:629-633`).
- **The shape.** #1058: a `--backend` after the subcommand is refused with
  exit 2 and a line naming the order, never accepted as another backend's
  default; the lane's option-first order keeps working. #1067: the SFTP QA
  endpoint cannot read or write outside its data directory and its key
  authenticates as a QA identity, not the host's user -- the mechanism is
  the lane's (a container pinned by tag and digest as #1077 asks, a Python
  SFTP server that confines by path, or a restricted `sftp-server`), chosen
  from what the tool's own `up` note says it cannot do unprivileged, and
  named in the commit; a mechanism that needs root is not a mechanism here.
  #1068: a stanza is written only from `rclone obscure`'s output; when
  `obscure` fails the stanza is not written and the tool exits non-zero
  naming it. #1060: `ls` and `reset` exit non-zero on a failed listing or a
  missing state, with the error on stderr, never an empty listing with rc 0
  (`|| true` goes).
- **The test first.** #1058: `tools/cloud-test-backend up --backend sftp`
  on the unfixed file brings up WebDAV and prints no refusal (quote the
  listener on 9080); on the fixed file it exits 2 with the line, and nothing
  listens. #1067: with the SFTP endpoint up, an `rclone lsd` (or `sftp` `ls`)
  through the endpoint at a path above the data directory (`..`, `/etc`)
  returns the host's entries on the unfixed file and an error on the fixed
  one; and the authenticating identity reported by the server (its log, or
  `whoami` through an `ssh` to the endpoint where the mechanism allows one)
  is the host's user on the unfixed file and the QA identity on the fixed.
  #1068: `rclone` replaced on `PATH` by a shim whose `obscure` exits 1: the
  unfixed file writes a stanza carrying the clear value (quote the line
  masked); the fixed writes none and exits non-zero. #1060: `ls` with
  `CLOUD_QA_STATE` naming a directory that does not exist: rc 0 and empty
  on the unfixed file; non-zero with the error on the fixed. Each case
  quoted in `02` § The streams' positives, run through the isolation
  environment and taken down after.
- **Already written:** nothing on a device; the QA endpoints live under
  `/workspace/tmp/m6-t13/state` and are reset by the stream; a stanza
  written by the unfixed writer on an earlier run is under the same state
  directory and is removed by `reset` before the fixed case.
- **Acceptance:** each bug's checkboxes from its own case, `fixed-at` set to
  the stream's last commit; `caps` still prints for the three backends; the
  leftover check clean.
- **Commits**, one per bug, in this order: `cloud-test-backend: refuse
  --backend after the subcommand (#1058)`; `cloud-test-backend: confine the
  SFTP QA endpoint to its data directory under a QA identity (#1067)`;
  `cloud-test-backend: a stanza is written only from rclone obscure's output
  (#1068)`; `cloud-test-backend: ls and reset fail closed on a failed
  listing (#1060)` -- each `Refs #N, #660`.

## S2. `cloud-round-trip`: the cleanup never deletes what it refused, every check reads a success, every verdict says what it counted (#1066, #1060's harness half, #1062, #1063, #1057, #1059, #1064, #1065, #1069, #1070)

- **Why a stream:** ten bugs on one 7,808-line file whose regions overlap
  (KILL1 is #1060's and #1062's; CONTRACT #1060's and #1063's; the KILL and
  LINK resets run through #1066's ownership rule; skip accounting is
  #1057's and #1059's), so the commits are serial in the order below and
  each leaves a harness whose `--list` and dead-device case still answer.
- **Files owned:** `tools/cloud-round-trip` (`restore_device` and the
  ownership of `/storage/roms/vectrex` `:612-618`, `:915-916`,
  `:7775-7785`; `backend_files()`/`backend_sizes()` `:1836-1849`; `fx_kill1`
  `:6786-6850`; CONTRACT's dry-run guard; A5 and RETENTION; the verdict
  `:619`, the equipment check `:313-316`, `--only`; step 25's probe; CAP13's
  count; A15's fixture; KILL5 `:7094`, `:7151`).
- **The shape.** #1066: a device-side directory the harness did not create
  is never removed by it -- the harness records what it created and the
  cleanup removes only that; an occupied `vectrex` is a refusal that leaves
  the directory as found, and `grep -n 'rm -rf .*roms'` after the stream
  shows every removal guarded by that record (`--real-roms` is not a
  guard). #1060: an absence check pairs with "the listing succeeded" and
  fails when it did not. #1062: `webdav` assigned before it is read, and
  the preservation predicate fails on a file the cloud no longer has.
  #1063: the dry-run guard fires on a conflict line, not on the word in the
  copy arm's banner. #1057: a cell that calls a script the image does not
  ship is a SKIP that names the script (one `SKIP` line, never two `PASS`),
  and "skipped" has one definition shared with #1059. #1059: the last line
  carries the backend, its capabilities (PL-15) and passed / failed /
  skipped counts; an unknown `--only` is refused with exit 2; a failed
  equipment check fails the run. #1064: step 25 fails when its probe finds
  no ES path. #1065: CAP13 reads this invocation's part of the log and
  distinguishes absent from zero; the sibling sweep (`grep -n 'grep -c.*||
  echo 0'`) is listed in `02` with each hit's cell and whether the stream
  fixed it or named it for the cell's owner. #1069: A15's fixture is an
  archive `cloud_backup` accepts, so A15 reaches the behaviour it names.
  #1070: KILL5 expects `CLOUD_BACKUP_KEEP` archives, read from the setting
  the run used.
- **The test first.** On the host, against a copy of the file at
  `8a2518fa44` or an extracted function: #1066 a stub device directory
  seeded occupied (a local `--host` the harness can reach, or the function
  with its `ssh` runner stubbed) -- the unfixed cleanup removes it, the fixed
  leaves it and the refusal line is quoted; #1060 `backend_files()` over a
  backend whose `ls` fails (S1's fixed tool with a missing state) -- the
  unfixed check passes, the fixed fails; #1062 `fx_kill1` imported and
  called to the line that reads `webdav` -- `NameError` on the unfixed,
  none on the fixed; and the predicate over a listing without the file;
  #1063 the guard's function over a dry-run output with no conflict line --
  fires on the unfixed, not on the fixed; #1057 the cell's runner with the
  script absent on the stub -- two PASS on the unfixed, one SKIP naming
  `cloud_reconcile` on the fixed; #1059 `--only no-such-cell` -- rc 0 on the
  unfixed, 2 on the fixed; and the verdict line built from a run with one
  SKIP; #1065 the shell fragment -- `0` twice on the unfixed, `absent` on the
  fixed; #1064, #1069, #1070 the host half where one exists (the fixture's
  bytes are an archive, the floor's predicate over an empty list, the
  expectation read from the setting) and the rest in § The guest cycle.
  Each quoted in `02` § The streams' positives with its command and lines.
- **Already written:** nothing on a device; on a QA guest an earlier run of
  the unfixed harness may have left `/storage/roms/vectrex` deleted or
  seeded -- the guest cycle starts from a fresh guest, so nothing is
  inherited; the host's QA state is reset by S1's tool.
- **Acceptance:** each bug's host checkboxes from its own case, the guest
  checkboxes after § The guest cycle; `--list` still 45 cells; the
  dead-device case still rc 2; `fixed-at` set to the stream's last commit.
- **Commits**, one per bug, in this order: #1066, #1060, #1062, #1063,
  #1057, #1059, #1064, #1065, #1069, #1070 -- `cloud-round-trip: <the fix>
  (#N)`, each `Refs #N, #660`.

## S3. The small tools: a fixture built at run time, a census that only reads (#1061, #1081)

- **Files owned:** `tools/cloud-connections-test:37` and
  `tools/cloud-census:76` with its header.
- **The shape.** #1061: the value is assembled when the case runs
  (`printf` into a format string, a value passed through `$(...)`), so the
  file at rest carries no line T10's widened set matches. #1081: the
  command string reads `cat /storage/.config/cloud_sync-device-id
  2>/dev/null || echo unset` and never names `cloud_device_id`; the header's
  *read-only* sentence is then true and stays.
- **The test first.** #1061: T10's widened patterns read with `git show
  feature/m6-tooling-guards-657:.githooks/secret-patterns` into
  `/workspace/tmp/m6-t13/` (never merged): `grep -a -c -E -f <patterns>
  tools/cloud-connections-test` is 1 on the unfixed file and 0 on the
  fixed, and the bare run still ends `Ran 26 tests` / `OK`. #1081:
  `grep -c 'cloud_device_id' tools/cloud-census` is 1 on the unfixed file
  (the call) and 0 on the fixed, or the one mention is the header's
  sentence saying it is not run; the census is not run against anything.
- **Already written:** #1061 nothing; #1081 nothing inherited -- no run of
  the census is in this project's ledger, and a device whose id file the
  census created carries a valid id the scripts would have made anyway.
- **Commits:** `cloud-connections-test: the credential-shaped fixture is
  built at run time (#1061)`; `cloud-census: read the stored id, never run
  cloud_device_id (#1081)`.

## The guest cycle, as the window now carries it

The one cycle the brief holds behind the M7 lane's FINAL RETURN (its
§ 1 and § 5): the single-device suite over WebDAV then SFTP on one
GENERIC_X64 guest with the CAP cells, now **plus** the stage-E positives
that only a guest can show. Before the window the lane posts on #660 the
cycle's plan: the cells, in order -- first the controls on the unfixed
harness from a clone at `8a2518fa44` (KILL1 to its `NameError`, A5/RETENTION's
two PASS, step 25 over the empty probe, CAP13's present/absent pair, A15 to
its refusal, KILL5 at the default keep), then the fixed harness at the
stream's tip over the same cells with KILL5 at the default keep and at
`CLOUD_BACKUP_KEEP=2`, then the suite whole over WebDAV then SFTP -- each
with its expected minutes from `--list` and the stage-A timings, the total
under **45 minutes** on one guest, the backends under the isolation
environment, S3 by MinIO only if the suite's cells name it (D-QA-058 names
three; the plan says which run). The coordinator grants the window on #660
with that bound after the FINAL RETURN; the lane posts START and RETURN on
#660, writes nothing on the host file (the coordinator does), stops the
guest by its pidfile, downs every backend, and runs the leftover check. The
guest checkboxes of #1057, #1062, #1064, #1065, #1069 and #1070 are ticked
from that cycle's lines, the suite's verdict line (#1059's shape) quoted
for both backends in `02` § The suites re-run.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- PL-15 rides on #1059 (S2). PL-16 is #1055. PL-17 #1075, PL-19 #1076,
  PL-20 #1077, PL-21 #1078, PL-23 #1079, PL-24 #1080: Backlogs, deferred.
  PL-18: the stale sentence to #909; the rule's `paths:` naming four of the
  nine is a rule-edit packet the coordinator files (the brief's errata).
  PL-22 is #1081 (S3).
- The seat's rule break (`tools/council/run --help` sourcing the env file,
  no call made) stays in `00` and the friction line; its guard is on #1044.

## Order and hand-back

S1, then S2, then S3; one file per stream, so the streams are serial and
each commit is a working tool: after S1 the three backends' `up`/`ls`/
`cat`/`reset`/`down` run once each under the isolation environment and
their lines go in `00`; after S2 `--list` (45 cells) and the dead-device
case (rc 2) run once and go in `00`; after S3 `cloud-connections-test`'s
`Ran 26 tests` / `OK`. Each commit cites its bug (`Refs #N, #660`, never a
closing keyword: a bug stays open until its fix reaches `next`) and
carries the attribution line; `git status --short` before every `git add
-A`; nothing under `tools/` but the nine.

After S3: the Phase 7 table and the `punch_index` at their outcomes
(`fixed` with its commit for the host halves, `fixed, guest criterion
pending the window` for the six, `deferred` with its issue for the rest),
`02` § The streams' positives, the lint on the folder (`--phase pre-issue`
until the cycle, then the default), `fixed-at:` in #660's body, and the
hand-back comment naming the tip and each artifact by path. The coordinator
accepts the streams by `AUDIT_ISSUE=1073 DISPATCH_TIP=e1d51b3a04 $S/t13-accept.sh
<tip> <coordinator tip>` on a clone of the lane's branch, extended with the
host positives above (each case re-run against the stream's tip, the three
backends up and down under a separate `CLOUD_QA_STATE`, the two greps of
S3), reads every stream's diff, and ticks the host checkboxes of #660,
#1073 and the bugs from the artifacts. Stage F (the re-verification), the
retro (stage G) and the close-out (stage H) follow the guest cycle, since
they read its lines; the coordinator closes #1073 when its checkboxes read
back ticked by name, and merges the branch in its turn (after T12's and
T15's, before T4's).

## Errata, 2026-10-25 (the coordinator's, after the guest cycle)

- **Step 5b as the coordinator ruled it (06:41) -- A5 and RETENTION with
  "device b being guest a itself" -- is refused by the harness's own #91
  guard** (one device id for two devices; both guests carrying one MAC),
  and rightly: a two-device cell needs two guests. #1057's guest criterion
  moves to the second window (a guest pair, with the SFTP re-proof).
- **#1067's `rclone serve sftp` endpoint fails the content tier** (seven
  checks, `cloud_content_restore scan: the cloud could not be read (rclone
  exit 5)`) where the old sshd endpoint passed; the host's `serve sftp` is
  1.60.1-DEV against the image's client 1.75.2. Fix forward ruled (08:12)
  with the retained donor's own 1.75.2 as the client on the host, a bound
  of 09:15 UTC and a revert of `94c050ed5a` as the fallback; S1's shape
  gains: *the endpoint serves with a rclone of the client's generation when
  one is available, and `caps` prints the server's version*.
- KILL1 under the 200k throttle exits 124 on both re-runs and lacks the
  `drained` branch LINK has; A15's two "the log did not name the folder"
  checks fail on both trees (a stale needle). Stage F fixes with positives.
