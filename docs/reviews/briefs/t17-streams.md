# Stream brief: M6.P2 T17, stage E (#664)

**The coordinator's, 2026-10-26, at T17's stage-D pause** (the lane's comment of
07:32 UTC; the punch list at `3a7fdb0ec2`, 22 items). Six streams, serial, in the
lane's worktree `/workspace/repos/pixelelated/distribution.worktrees/m6-cloud-setup-content-664`
on `feature/m6-cloud-setup-content-664`, on top of the stage-D tip. The
dispositions that are not streams are in the ruling on #664; this file is only
what changes code. Every stream is in a fork-own file, so D-WORKFLOW-209
reaches none of it.

## The rules every stream keeps

- **The bug first, then the test, then the fix, and the test's FAIL is
  recorded before the fix lands.** The lane files each `bug` at stage D with
  its trace, its `Already written:` line and its VM line (D-WORKFLOW-187);
  the fixture runs on the host under the donor's rclone 1.75.2 and the host's
  python, each named beside its verdict; the guest, if its window comes
  before the hand-back, repeats the fixture against the installed (unfixed)
  files and the record says so.
- **Every stream answers `Already written:`** in its bug and in `02` § The
  streams (`upgrade-and-install.md`, D-WORKFLOW-050).
- **One commit per stream**, `Refs #664, #<bug>`, the paths named in the
  message, no closing keyword; `tools/register-check` before each commit;
  `tools/pkgcheck` is not involved (no `package.mk` changes).
- **A credential-shaped line is never quoted and never written to a file at
  rest**; a fixture's values are assembled at run time (#1061).
- **Nothing runs on a unit; no guest outside the granted window; no build;
  no fetch; no keyed council call** (the slice's four were spent at stage C).
  The host is M7's under the 04:47 handoff; the streams are reads and host
  fixtures.
- **`rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short
  command, never inside a `bash -c` script.**

## S1 -- `cloud_oauth`: the PIN gate (PL-01) and rclone's words in HTML (PL-14)

File: `projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth` (fork-own).

1. **Positive before:** `tools/t17-pin-fixture.py --expect unfixed` met at
   the stage-D tip; `--expect fixed` fails on it. A second case for PL-14:
   a provider error string carrying a tag reaches the paste page unescaped
   (the fixture renders the page with a run-time-assembled `<b>` string and
   finds it raw). `stage-e/s1-before.txt`.
2. **The fix:** `_supplied()` (`:2330-2344`) takes a PIN only when the first
   path segment is exactly four ASCII digits, checked before
   `compare_digest` on GET and POST; `/favicon.ico` and the touch-icon
   routes answer 404 before `_gate()`; the ten-attempt count moves after the
   shape check, so an icon request spends nothing (this also ends F-09's
   `TypeError` on a non-ASCII PIN). Rclone's words are HTML-escaped where the
   paste flow renders them.
3. **Positive after:** the ten-icon cases answer 200 for the right PIN;
   ten real wrong PINs still lock out (the control); the tag arrives
   escaped; `python3 -m py_compile`. `stage-e/s1-after.txt`.
4. **`Already written:`** nothing persisted: the counter lives in the serve's
   memory and a new serve starts at 0; a page is rendered per request.
5. **Commit:** `cloud_oauth: take only a four-digit PIN, answer icon routes
   before the gate, escape rclone's words on the paste page (Refs #664, #<S1 bug>)`.

## S2 -- the content scripts: an allowlist for `RCLONE_NET_OPTS` (PL-02; D-CLOUD-185)

Files: `cloud_content_transfer` (the shared home), `cloud_content_restore:235-279`,
`cloud_content_backup` (its array builder), all fork-own. **T16's twins
(`cloud_restore:1406-1411`, `cloud_backup:1367-1371`) split the same value
the same way and are routed to #663 by the coordinator; this stream does
not touch them.**

1. **Positive before:** `tools/t17-content-fixture.py --expect unfixed
   --real-rclone <the donor's 1.75.2>`: with `--delete-excluded` in the conf
   the match's apply deletes `a.srm` over the local cloud; **a second case,
   Argon's R-9**: a `--filter` flag ahead of the excludes reaching the saves
   without `--delete-excluded` (run on the host first; the guest, if its
   window comes, repeats both under the stage-B conditions: the guest's conf
   only, the synthetic root only, the conf put back). `stage-e/s2-before.txt`.
2. **The fix, the decision D-CLOUD-185:** the value is split once, in
   `cloud_content_transfer`, into an array that admits only an allowlist of
   flags with checked values -- `--contimeout`, `--timeout`,
   `--low-level-retries`, `--retries`, `--bwlimit`, each value a duration, a
   count or a rate -- and every other token is dropped with one log line
   naming the flag's shape (never its value) and a `>>> why` only when the
   drop leaves the run unable to proceed; both scripts take the array from
   there. Stripping one spelling is not the fix.
3. **Positive after:** `a.srm` kept in both cases; the allowed flags still
   reach rclone (the control: `--timeout 5s` observed in the fixture's
   argv capture); the unfixed file still loses it. `stage-e/s2-after.txt`.
4. **`Already written:`** a device whose conf holds such a flag has lost
   nothing until a match applied; one that applied has lost saves the fix
   cannot bring back (stated so in the bug); the fixed reader reads the
   value on the card and drops the flag at the next run, never migrating it.
5. **Commit:** `cloud_content_transfer: RCLONE_NET_OPTS reaches rclone only
   through an allowlist of checked flags (Refs #664, #<S2 bug>)`.

## S3 -- `cloud_content_backup`: the explicit names are checked (PL-03)

File: `cloud_content_backup:583-585` (fork-own); the restore's loop at
`cloud_content_restore:1482-1487` is the model.

1. **Positive before:** the fixture's `backup-traversal` case: `'../.config'`
   is accepted and rclone is called with `${ROOT}ROMs/../.config`.
   `stage-e/s3-before.txt`.
2. **The fix:** the restore's name check, before the lock: every explicit
   name must be a known system directory name (the `--known-directories`
   set), with no `/`, `.` or `..`; a refused name ends the run with a `>>> why`
   in the player's words and no rclone call.
3. **Positive after:** `../.config` refused with no rclone call; `snes`
   still copies (the control). `stage-e/s3-after.txt`.
4. **`Already written:`** nothing on the device; a cloud that already
   received such an upload keeps it, and the bug says so: inspect, and where
   `rclone.conf` went up, rotate the credential -- never an automatic
   deletion (A-28).
5. **Commit:** `cloud_content_backup: check every explicit name as the
   restore does, before the lock (Refs #664, #<S3 bug>)`.

## S4 -- `cloud_connections.py`: the option key's shape (PL-04) and the staged sweep (PL-08)

Files: `cloud_connections.py:161-165` and `cloud_remote:329-334` (fork-own).

1. **Positive before:** `tools/t17-option-key-fixture.py`: a `--config=<path>`
   shaped key writes the connection to `<path>` and the save then refuses; a
   SIGKILL mid-save leaves `.connection-*` and `.rclone.conf-*` beside
   `rclone.conf`. `stage-e/s4-before.txt`.
2. **The fix:** `save()` refuses a key outside `^[a-z0-9_]+$` before staging
   (the provider's option list is the stronger check, recorded as the
   follow-up if it is not taken now); at the start of `save()`, under the
   lock, the staged leftovers of an earlier save are removed (the sweep
   PL-08 asks for), and the `Refused` words stay the player's.
3. **Positive after:** the `config` and `dash-key` cases refuse with no
   outside file; the control still saves; a staged leftover planted before a
   save is gone after it. `stage-e/s4-after.txt`.
4. **`Already written:`** a file an option-shaped key created holds a
   connection the fix cannot find (stated); staged leftovers on a device cut
   mid-sign-in are removed by the first save after the fix.
5. **Commit:** `cloud_connections: refuse an option key of the wrong shape
   before staging, and sweep an earlier save's leftovers (Refs #664, #<S4 bug>)`.

## S5 -- `cloud_content_restore --set-systems`: whole or not at all (PL-06)

File: `cloud_content_restore:1405-1406` (fork-own).

1. **Positive before:** a full-card fixture (a size-capped tmpfs, or a
   `printf` that fails) over the real `--set-systems`: a partial temp file is
   installed. `stage-e/s5-before.txt`.
2. **The fix:** the write's status is checked before the `mv`; on failure
   the temp file is removed and the old selection stands, with a log line.
3. **Positive after:** the old selection stands on the full card; a normal
   write still installs (the control). `stage-e/s5-after.txt`.
4. **`Already written:`** a selection file already cut short is read as
   written and the fix cannot tell it from a choice (stated in the bug).
5. **Commit:** `cloud_content_restore: --set-systems installs the selection
   whole or not at all (Refs #664, #<S5 bug>)`.

## S6 -- `cloud_setup:797`: the rule's word (PL-05)

File: `cloud_setup:797` (fork-own). `backuptool:1495`'s D-UI-117 sentence
stays as proposed words; its French pair is T18's (#665) and is routed there
by the coordinator.

1. **Positive before:** `stage-b/why-lines.txt` shows `ANOTHER CLOUD SYNC IS
   RUNNING` printed at `:797` and absent from `CloudText::whySentences` at
   the ES pin, while `A SYNC IS ALREADY RUNNING` is present.
2. **The fix:** the sentence at `:797` becomes `A SYNC IS ALREADY RUNNING`
   (`es-player-text.md`'s word, D-UI-031).
3. **Positive after:** the why-lines read shows the new sentence present in
   the table at the pin; `bash -n`. `stage-e/s6-after.txt`.
4. **`Already written:`** nothing persisted (a printed line).
5. **Commit:** `cloud_setup: the lock's why sentence is the rule's (Refs #664, #<S6 bug>)`.

## The record

- `02` § The streams: one row per stream with the positive before, the
  commit, the positive after, the `Already written:` answer and
  `proved: fixture`; `05`'s rows for PL-01 to PL-06, PL-08 and PL-14 point at
  it.
- `00`: the stage-E entry naming the donor's rclone (its sha256 from
  RECORD.txt), the host's python and bash versions, and every fixture's
  command.
- The hand-back after stage E's record, as the brief's § 10: the tip, the
  artifacts by path, `reviewed-at:` and `fixed-at:` in #664's body.

## What never runs here

A build, a compiler, a guest outside the granted window, a fetch, a keyed
council call, anything on a unit or a person's cloud, a change outside the
six files named and the audit folder, a change to T16's twins.

## S7 -- `backuptool`: member types the name check does not inspect (F-24, PL-23; added at the hand-back, 2026-10-26 08:2x UTC)

Found by the lane in its guest window through a full `backuptool restore` of
hand-made archives: a standalone symlink member (to `/var/tmp`) was restored
with rc 0; a symlink with a child failed and **its revert failed too**, leaving
a directory and `.restore-in-progress`; a hard link and then a file failed
cleanly. A `bug`, Low (the archive must be hand-made; the interface restores
its own), the lane's to file, fork-own.

File: `projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool` (the
member check `:551-558`, `foreign_member()`, and the revert).

1. **Positive before:** `tools/t17-archive-fixture.py` (the shape of the
   guest run) over hand-made archives of each member type -- a standalone
   symlink, a symlink with a child, a hard link, a device node, a regular
   file, a directory -- through `backuptool restore` on the host under the
   image's busybox `tar` from the donor: the standalone symlink restored,
   the symlink-with-child's revert leaving a directory and the marker.
   `stage-e/s7-before.txt`.
2. **The fix:** `foreign_member()` refuses every member type other than a
   regular file or a directory, before extraction, by `tar -tvf`'s type
   column (`l`, `h`, `c`, `b`, `p`, `s`), with the refusal in the player's
   words and the restore reverting to the previous settings; and the
   revert's handling of a restored-into directory read and made whole: a
   directory where the live tree had a file is removed before the previous
   file is put back, so `.restore-in-progress` never survives a revert.
3. **Positive after:** every foreign member refused with nothing written
   outside `/storage` and nothing left in the live tree; the regular file
   and the directory still restore (the control); a forced mid-restore
   failure's revert leaves no directory and no marker. `stage-e/s7-after.txt`.
4. **`Already written:`** an archive already in a cloud is read by the same
   check at its next restore and refused if it holds a foreign member --
   the player is told which (the restore's why line) and the previous
   settings stand; nothing persisted on a device beyond what an earlier
   restore left, which the fix does not touch.
5. **Commit:** `backuptool: refuse archive members that are not files or
   directories, and make the revert whole over a restored-into directory
   (Refs #664, #<S7 bug>)`.
