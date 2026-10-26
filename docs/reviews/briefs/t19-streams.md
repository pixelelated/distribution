# Stream brief: M6.P2 T19, stage E (#666)

**The coordinator's, 2026-10-26, at T19's stage-D pause** (the lane's comment
of 13:39 UTC; the punch list at `704a2e50eb`, 23 items carrying 41 findings;
8 bugs proposed, all Low). Ten streams, serial, in this order, in the lane's
worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-offline-achievements-666`
on `feature/m6-offline-achievements-666`, on top of its tip `704a2e50eb`. The
dispositions that are not streams are in the ruling on #666; this file is
only what changes code.

## The rules every stream keeps

- **Test first, then the fix, and the test's FAIL is recorded before the fix
  lands** (`engineering-practices.md` § Guards must fail closed). A fixture
  runs the **real** script -- the ctl, a helper, the patched service -- in a
  bubblewrap sandbox started with `--clearenv`, with shims on `PATH` for
  `systemctl`, `get_setting`, `set_setting`, the client and the helpers it
  does not test, as `tools/last-good-scripts-test` and the lane's own
  `tools/t19-listing-fixture.py` do; its scratch root is asserted outside
  every real prefix, or nothing is rewritten (plan § 6b). The shell is the
  host's bash 5.3.9 (the tree pins 5.3; the retained donor holds busybox and
  rclone only, T29's erratum) and the python is the host's, each named beside
  every verdict with the image's version beside it. A fixture's secret-shaped
  value is a short synthetic word assembled at run time (#1061).
- **The fork-own files only**: the four scripts under
  `projects/ROCKNIX/packages/network/raofflineproxy/sources/`, the unit under
  `system.d/`, `package.mk`'s comment, and the patch series under `patches/`
  -- a new patch is a fork-own file, and upstream's lines change only inside
  one (`bugs-are-agent-first.md` rule 6), each such patch a #585 line in the
  lane's shape (D-WORKFLOW-164; never sent, D-WORKFLOW-165). `setsettings.sh`
  is T1's file and the interface is T20's: neither changes here; what they
  inherit is written in `02`.
- **Every stream answers `Already written:`** in its bug and in `02` § The
  streams (`upgrade-and-install.md`, D-WORKFLOW-050).
- **A `>>> why` token new to the interface's table** falls to its generic
  sentence (`CloudText::scanWhy`); a stream uses an existing token where one
  fits and records a new one in `02` § What T20 inherits, where its row and
  French are T20's (#667). No stream edits a player-read sentence of its
  own.
- **One commit per stream**, `Refs #666, #<bug>` (S10 `Refs #666`); the
  paths named in the message; no closing keyword; `tools/register-check`
  before each commit; `tools/pkgcheck raofflineproxy` after S10's
  `package.mk` edit; `tools/last-good-scripts-test`'s proxy cases before a
  commit that touches the ctl (plan § 6b: the suite before a covered
  script's commit), its PASS line in `stage-e/`.
- **The bug first** (D-WORKFLOW-187/189): the lane files each stream's `bug`
  before the stream, Low, `bug` label, referencing #666 as T17's were filed,
  with the trace, the `Already written:` line and the VM line from the punch
  item; `fixed-at` goes into the bug at the commit; a bug with every
  checkbox ticked stays open until the fix is on `next`.
- **Nothing runs on a unit; no guest** (the window is spent; the after that
  needs a guest is `fix-walk-pending-image`, run at the integration's
  window, which the coordinator grants); **no build; no fetch; no keyed
  council call**; the image's scripts are M7's, 233 lines apart from the
  tree's, so a verdict labels its side.
- **`rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short
  command, never inside a `bash -c` script.**

## S1 -- PL-01 (F-01, F-02): the offline login answers only a credential (D-RA-050)

File: a new patch `patches/022-offline-login-requires-credential.patch` on
the patched pin's `proxy_service.py` (`handle_offline_login`, `:491-505`)
and, for the password's hash, `storage.py` (upstream code; rule 6; a #585
line in `02` § The patches, written as the lane writes them).

1. **The positive, before.** The pin's tarball from
   `/workspace/cache/rocknix-sources/raofflineproxy/` (named by the pin)
   unpacked under `/workspace/tmp/m6-t19/s1/`, the 18 patches applied in
   series order with `patch -p1` (fuzz 0, as the recipe's comment says), the
   service started on a loopback port in the sandbox (`--unshare-net`, so
   upstream is unreachable by construction) with a store holding one
   `login2` row for a synthetic account; a `login2` naming the account with
   no credential answers 200 with a `Token` (the guest's `b1-07` on the
   image's service is the same fact, labelled). If the service cannot start
   on the host (the native module), the handler is exercised through a unit
   test the patch carries (`tests/test_offline_login.py`, the native module
   stubbed), and that test's FAIL on the unpatched tree is the before.
   `stage-e/s1-before.txt`.
2. **The fix.** The offline login answers only a request presenting the
   configured account's credential: `t=` equal to the cached row's token, or
   `p=` whose salted hash equals the one the proxy recorded at the last
   successful online `login2` that carried `p=` (a random salt made once per
   store, the hash beside the cached row; nothing recorded for a login that
   failed). Any other request -- no credential, a wrong one, an account other
   than the configured one, a `Host` that is not a loopback name, any
   `Origin` -- gets the API's own failed-login shape (`Success: false`, no
   `Token`) and no `X-RA-Offline` body. The patch carries its test; the
   change stays inside the handler, the storage column and the test, or the
   lane stops and says so on #666.
3. **The positive, after:** the no-credential request refused; the cached
   token and the recorded password each answered with the cached body; a
   foreign `Host` and an `Origin` refused; the unpatched test FAIL and the
   patched PASS in `stage-e/s1-after.txt`; `patch --dry-run -p1` of the new
   patch at fuzz 0 on the pin plus 001 to 021.
4. **`Already written:`** tokens already served over loopback cannot be
   recalled; `proxy.sqlite3` keeps the `login2` rows of every account ever
   signed in, and a row with no recorded hash answers only the token until
   the next online login records one (read both: the old row shape is
   honoured, the new column written). Nothing migrated, no row purged.
5. **Commit:** `raofflineproxy: the offline login answers only the account's
   credential (Refs #666, #<bug>)`, naming the patch and the #585 line.

## S2 -- PL-09 (F-04, F-25): the proxy's files are private (D-RA-049)

Files: `system.d/raofflineproxy.service`; `sources/raofflineproxy-ctl`.

1. **The positive, before.** A scratch proxy folder with files at 644 under
   a 755 directory, a symlink inside it pointing outside, the ctl run in the
   sandbox: nothing changes a mode (`stat -c %a`); `grep -c '^UMask=' `
   the unit prints 0. `stage-e/s2-before.txt`.
2. **The fix.** The unit gains `UMask=0077`; the ctl sets `umask 077` at its
   top (the helpers inherit it); a new ctl verb `private-modes` -- idempotent,
   non-destructive, following no symlink, removing nothing, reporting each
   failure and exiting non-zero on any -- sets the proxy's folder 0700 and
   every regular file under it 0600; `enable` runs it after its writes and
   the unit runs it as `ExecStartPre=`. The full sandboxing of the service
   (`User=`, `NoNewPrivileges`, `Protect*`, `Private*`,
   `CapabilityBoundingSet`, `RestrictAddressFamilies`) is the coordinator's
   Backlog, not this stream's.
3. **The positive, after:** the scratch folder 700 and its files 600, the
   symlink's target untouched (the control), a second run changing nothing
   and exiting 0, a file it cannot chmod reported with exit non-zero; the
   `UMask=` line present; the service's effective umask on the image is
   `fix-walk-pending-image`. `stage-e/s2-after.txt`.
4. **`Already written:`** every file the unfixed build wrote is 644 root,
   the store with the token row included; the pass at the next `enable` or
   service start sets them 600 (migrated: idempotent, non-destructive; the
   upgrade rehearsal's seed of a 644 proxy folder is the integration's owed
   item, named in `02`).
5. **Commit:** `raofflineproxy: umask 077 and a private-modes pass for the
   proxy's folder (Refs #666, #<bug>)`.

## S3 -- PL-02 (F-03): readiness is the service's own socket

File: `sources/raofflineproxy-ctl` (`port_listening`, `:925-937`; the unit's
`ExecStartPost` keeps calling `listening --wait 30`).

1. **The positive, before.** In the sandbox, a stand-in bound to
   `0.0.0.0:8080` by a python process, a `systemctl` shim answering
   `MainPID=<another pid>`: `listening` exits 0. `stage-e/s3-before.txt`.
2. **The fix.** `port_listening` reads the service's `MainPID`
   (`systemctl show -p MainPID --value raofflineproxy`), walks
   `/proc/<pid>/fd` for socket inodes, and is true only when one of them is
   a LISTEN row at port `1F90` in `/proc/net/tcp` or `tcp6`; no `MainPID`,
   or none of its sockets listening there, is 1; `--wait` polls that. The
   launch check in `setsettings.sh:536` is T1's and stays as it is (the
   stricter predicate); `02` records the two.
3. **The positive, after:** the stand-in alone, `listening` 1 and `enable`
   failing with the shims' state unchanged; with the stand-in's own pid as
   `MainPID`, 0. `stage-e/s3-after.txt`.
4. **`Already written:`** a device where the race happened holds
   `offlineproxy=1`, `hardcore=0` and the marker while the service failed;
   nothing reconciled by this fix; the next `enable` or `disable` rewrites
   the three.
5. **Commit:** `raofflineproxy-ctl: listening is the service's own socket
   (Refs #666, #<bug>)`.

## S4 -- PL-03 (F-06, F-39): disable cannot stop what it cannot see

File: `sources/raofflineproxy-ctl` (`stop_running_run` `:492`, `do_disable`
`:525`, `take_lock` `:1190`, the EXIT traps `:1981`).

1. **The positive, before.** The lock path a directory and a stand-in
   holder alive: `disable` exits 0 in a second, the `systemctl` shim records
   a stop, the holder is never asked to stop; a shim helper that sleeps
   shows the lock file at `/proc/<pid>/fd/9`. `stage-e/s4-before.txt`.
2. **The fix.** A lock that cannot be opened is `cannot_tell`: `disable`
   exits non-zero with nothing changed (the service, the toggle, the marker
   as they were) and says why; `stop_running_run`'s status is honoured -- a
   holder that did not stop within the bound leaves `disable` non-zero and
   the state as it was; every helper the ctl starts is launched with fd 9
   closed (`9<&-`), and the EXIT trap waits a bounded time for `CLIENT`
   after the kill.
3. **The positive, after:** the three cases above each as the acceptance
   says; the helper's `fd/9` absent. `stage-e/s4-after.txt`.
4. **`Already written:`** `/var/run` is tmpfs, so a lock path left wrong
   clears at reboot; a helper's partial cache work stays and the next run
   resumes it. Nothing to migrate.
5. **Commit:** `raofflineproxy-ctl: disable refuses a lock it cannot read,
   and helpers do not inherit it (Refs #666, #<bug>)`.

## S5 -- PL-04 and PL-21 (F-07, F-27, F-28): a writer's failure is seen

File: `sources/raofflineproxy-ctl` (`write_stamp` `:1073-1094` and its
callers `:1818`, `:1990`, `:2014`, `:2031`, `:2103`, `:2411`, `:2423`, `:2427`;
`put_back` `:421-423`, `enable_undo` `:430-436`, `disable`'s stop `:410`;
the index-pending fallback `:2150-2157`, `ack_index_pending` `:2176-2177`).

1. **The positive, before.** The stamp path a directory: the run exits 0
   and the row shows the run before; a `set_setting` shim failing for one
   key: `enable_undo` exits 0; a restore shim failing: the aside is removed.
   `stage-e/s5-before.txt`.
2. **The fix.** `write_stamp` refuses a stamp path that is a directory and
   removes its own `.tmp` on a failed `printf`; every caller checks its
   status and ends the run non-zero with a why (an existing token where one
   fits, else recorded for T20); `put_back` reads each setting back and
   `enable_undo` returns the first failure, `disable` reports a failed stop;
   the index-pending fallback writes a per-pid temp under the lock and
   `ack_index_pending` keeps the aside when its restore failed.
3. **The positive, after:** each case above non-zero and said; a normal
   write still the new line; the aside present after a failed restore.
   `stage-e/s5-after.txt`.
4. **`Already written:`** devices may hold an older `last-scan` and a stray
   `last-scan.tmp` (the next good write replaces the first, the fix removes
   the second), and a device where a rollback failed holds the settings the
   forward step wrote, rewritten by the next `enable` or `disable`. Nothing
   migrated.
5. **Commit:** `raofflineproxy-ctl: a stamp, an undo or a restore that
   failed is reported (Refs #666, #<bug>)`.

## S6 -- PL-05 (F-12): a mark ahead of the clock is no mark

File: `sources/raofflineproxy-ctl` (`do_topup` `:2221`, `:2235`, `:2264`).

1. **The positive, before.** In a scratch root, the mark `touch -d '+1 day'`
   and the history newer than the last pass: the top-up skips with "no game
   played". `stage-e/s6-before.txt`.
2. **The fix.** A mark whose mtime is ahead of now is treated as absent
   (removed, and said in the log); the mark's `touch` is checked and its
   failure reported.
3. **The positive, after:** the mark a day ahead and a game played, the pass
   runs; the mark two hours back, the half-hour gate holds. `stage-e/s6-after.txt`.
4. **`Already written:`** devices whose clock ran ahead may hold a
   future-dated mark; the fix treats it as absent, so they heal at the next
   link.
5. **Commit:** `raofflineproxy-ctl: a top-up mark dated ahead is ignored
   (Refs #666, #<bug>)`.

## S7 -- PL-06 and PL-23 (F-15, F-32, F-33): skipped, unread or unremoved is not clean

Files: `sources/raofflineproxy-ctl` (`do_topup`, `run_image_pass`:
`:2372-2380`, `:2362`, `:2389`, `:1854`); `sources/raofflineproxy-cache-images`
(`:338-343`, `:452`).

1. **The positive, before.** A helper shim exiting 0 with no result line: the
   pass reads `0 0 0` and the run is clean; the pass skipped under 60 s with
   no why; the helper missing, exit 0; on `--verify`, a damaged image in a
   read-only directory counts as present. `stage-e/s7-before.txt`.
2. **The fix.** A result line missing or unparseable with exit 0 ends the
   run non-zero with a why; a pass skipped for time is said in the stamp
   (the field the lane names, read by nobody yet; recorded for T20) and the
   run is not called clean; a missing helper is non-zero with a why; a
   failed unlink on `--verify` counts the image as not saved.
3. **The positive, after:** each case as the acceptance says. `stage-e/s7-after.txt`.
4. **`Already written:`** no record holds a wrong count from this; a run
   that skipped work wrote no stamp; a damaged file may stay in the cache
   and the next pass that can remove it fetches it again. Nothing inherited.
5. **Commit:** `raofflineproxy: a pass skipped, unread or unable to remove
   is not a clean run (Refs #666, #<bug>)`.

## S8 -- PL-07 (F-16, F-26): an unknown count is not a number

File: `sources/raofflineproxy-ctl` (`count_ready` `:888-897`, `do_account`
`:780-781`).

1. **The positive, before.** The export a directory: `ready` prints 0, exit
   0; a client shim exiting 1 whose last line is numeric: the number taken;
   a `login2` row of `[]` read as no points and `true` as a score.
   `stage-e/s8-before.txt`.
2. **The fix.** `count_ready` calls `cannot_tell` (exit 2, nothing on
   stdout) when the export cannot be read or the client failed, and no stamp
   records a count it did not read; `do_account` takes only a JSON object
   and only a number for a score.
3. **The positive, after:** the three cases as the acceptance says; a
   readable export still counted. `stage-e/s8-after.txt`.
4. **`Already written:`** stamps may carry `ready=0` from a failed read; the
   next scan or top-up overwrites them. Nothing to migrate.
5. **Commit:** `raofflineproxy-ctl: ready cannot tell is not zero
   (Refs #666, #<bug>)`.

## S9 -- PL-08 and PL-16's classifier (F-17, F-29, F-41, F-24): the job list carries any name

Files: `sources/raofflineproxy-ctl` (`list_jobs` `:1674`, `run_jobs`, the
classifier `:1736-1755`); `sources/raofflineproxy-cache-indexed` (its
reader); the lane's `tools/t19-listing-fixture.py` gains `--expect
unfixed|fixed` (T29's `t29-takeback.py` shape).

1. **The positive, before.** `t19-listing-fixture.py --expect unfixed` exits
   0 on the tree: a 0xff name fails the listing (`LIBRARY_UNREADABLE`), a
   newline name splits a job line, an `I` job with no id is hashed; a name
   carrying a stop word (`SKIP`, `stop`) changes the classification of its
   line. `stage-e/s9-before.txt`.
2. **The fix.** Job entries are written with `surrogateescape` and separated
   by NUL (`mapfile -d ''` and `split(b'\0')` on the reading side), one entry
   per path whatever bytes it holds; `DONE` is reconciled against the planned
   jobs and an unreported job counts as failed with its path; an `I` job
   with no id is refused, not hashed; the classifier reads the line's reason
   field, never the path.
3. **The positive, after:** `--expect fixed` exits 0 and `--expect unfixed`
   exits 1; the library with the 0xff name, the newline name and the
   stop-word name is listed whole and the rest cached (the fixture's own
   figure). `stage-e/s9-after.txt`.
4. **`Already written:`** the trigger is the player's own file, which an
   update does not rename; a `last-scan` with `why=LIBRARY_UNREADABLE` clears
   on the next good scan. No file renamed, no cache cleared.
5. **Commit:** `raofflineproxy: the job list carries any pathname, and the
   classifier reads the reason field (Refs #666, #<bug>)`.

## S10 -- PL-19 (F-21, F-22): the recipe says eighteen, and 020 and 021 say what they are

Files: `package.mk` (`:6`), `patches/020-rvz-padding-preserve-partial-word.patch`,
`patches/021-flush-reconnect-during-startup.patch`.

1. **Before:** `grep -c 'The16 patches' package.mk` prints 1; `head -n 5` of
   020 and 021 shows no header. `stage-e/s10-before.txt`.
2. **The fix.** The comment counts eighteen (001 to 021 with the gaps named);
   020 and 021 gain a header in the series' shape (what, why, the upstream
   state at the pin, the issue), before the first `---`/`diff` line so
   `patch` ignores it; `patch --dry-run -p1` of both at fuzz 0 on the pin
   plus their predecessors still applies; `tools/pkgcheck raofflineproxy`
   passes. The eight patches without drafts (003, 004, 010, 011, 012, 016,
   020, 021) and every draft's base older than the pin are #585 lines in
   `02` § The patches, in the lane's shape, for the coordinator to post; the
   drafts themselves are later (D-WORKFLOW-165).
3. **After:** the grep 0, the headers present, the dry runs clean, pkgcheck
   PASS. `stage-e/s10-after.txt`. No bug: documentation.
4. **`Already written:`** nothing on a device.
5. **Commit:** `raofflineproxy: the recipe counts its eighteen patches, and
   020 and 021 carry headers (Refs #666)`.

## The record

- `02` § The streams: one row per stream with the positive before, the
  commit, the positive after, the `Already written:` answer and `proved:
  fixture` (or `fix-walk-pending-image` where a guest is owed); `05`'s PL-01
  to PL-09, PL-16, PL-19, PL-21 and PL-23 rows point at it; every other row
  takes the outcome the ruling on #666 gives it.
- `02` § What T20 inherits: PL-13's staleness contract, PL-17's row, PL-18's
  `NO_GAMES_FOUND` row and comment, and every why token or stamp field a
  stream added; § The patches: the #585 lines (PL-01, PL-15 x2, PL-19, PL-22
  x2); the integration's owed items (the installed-native run against the
  tree's service on the built image, PL-20; the rehearsal's seed of a 644
  proxy folder, S2; the service's effective umask, S2).
- `00`: the stage-E entry naming the bash and python each fixture ran under
  and every fixture's command; `tools/` under the audit folder holds the
  fixtures; nothing under the repository's `tools/`.
- The hand-back after stage E's record, F, G and H as the brief's § 10: the
  tip, the artifacts by path, `reviewed-at:` and `fixed-at:` in #666's body,
  the audit issue and the nine bugs named.

## What never runs here

A build, a guest, a fetch, a keyed council call, anything on a unit or an
account, a change to `setsettings.sh` or any interface file, a change to an
upstream line outside a patch, a change outside the package's files and the
audit folder.
