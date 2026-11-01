# Stream brief: M6.P2 T18, stage E (#665)

**The coordinator's, 2026-10-26, at T18's stage-D pause** (the lane's punch
list of 11:10 UTC, 23 items at `69baebf049`; the audit issue and the bugs
are the lane's to file, D-WORKFLOW-187). Six streams, serial, **on the
EmulationStation branch** `feature/m6-es-cloud-pages-665` in
`/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665`,
cut from the pin `16dbac5211`; the distribution worktree
`/workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665`
takes the record (`02` § The streams, `05`'s rows, `00`), the menu map's
line (S3) and nothing else. The dispositions that are not streams are in the
ruling on #665; this file is only what changes code.

## The rules every stream keeps

- **Test first, then the fix, and the test's FAIL is recorded before the fix
  lands** (`engineering-practices.md` § Guards must fail closed). Where the
  code is pure, `fix-unit-test`: a case in `es-app/tests/unit` or
  `tests/app-unit`, built and run by the lane's generated `g++` command
  (`tools/t18-build-tests.sh`), FAIL on the pin, PASS after. Where it
  draws, `fix-walk-pending-image`: the walk's steps file written under the
  audit folder's `stage-e/walks/` (never under `tools/` -- the coordinator
  moves it into `tools/vm-walks/` at integration) and the frame owed to the
  integration build that carries the moved pin; the window's `pin-binary`
  frames are the befores where they exist.
- **Every edited `.cpp`:** the host `g++ -std=c++17 -fsyntax-only` with the
  ES include roots where the file's includes allow, else `CANNOT` with the
  missing header named (#1137: the host has no toolchain; the compile that
  catches a brace is the integration build's, which the coordinator runs
  before the pin lands); `grep -nP '^\s*//.*[^\x00-\x7F]'` clean on every
  touched file; **`es-unit-tests` and `jobs-tests` built and run before
  every commit** (the plan § 6b's stream practice).
- **French in the same commit** for every new or changed `_("")` string, in
  the catalog's style and with the catalog's existing terms for *match*,
  *back up* and *restore* (D-UI-051). The words below are proposed by the
  coordinator, shipped as proposed and put to the maintainer at the next
  build (D-UI-112); a wrong word costs one string.
- **Every stream answers `Already written:`** in its bug and in `02` § The
  streams (D-WORKFLOW-050): a stamp or a string already on a device is read
  as it is; nothing is migrated.
- **One commit per stream** on the ES branch, `Refs #665, #<bug>`, the
  paths named, no closing keyword; the pin in `package.mk` is **not** moved
  (the coordinator moves it at integration). The distribution worktree's
  commits are `docs: ...` only.
- **Nothing runs on a unit; no guest (the window is spent); no build; no
  fetch; no keyed council call; `rm -rf` only as `"${VAR:?}"/...` or a
  literal path, in its own short command.**

## S1 -- the why table and the comments (PL-03, PL-08)

Files: `es-app/src/CloudText.cpp` (`whySentences` `:414-467`, the comment at
`:419-422`, `localizedWhy`/`isKnownWhy` `:469-484`), `es-app/tests/unit/CloudTextTests.cpp`,
`locale/lang/fr/LC_MESSAGES/emulationstation2.po`, and the comments PL-08 lists
(`ThreadedCloudSync.h:93-98` and the others in `02` § Findings index, F-13).

1. **The positive, before.** Two cases in `CloudTextTests.cpp`: `isKnownWhy`
   on `THIS BACKUP HOLDS FILES A RESTORE CAN'T PUT BACK, SO NOTHING WAS
   CHANGED. RESTORE SETTINGS FROM THE CLOUD AGAIN, OR BACK UP SETTINGS TO
   REPLACE IT.` (D-UI-117's words, `backuptool:1495`) and on `A SYNC IS
   ALREADY RUNNING` (`cloud_setup:797` after T17's S6, `3e95bf18f4`) -- FAIL
   on the pin; and a round-trip case over **every** row of the table: each
   sentence normalized as the parser normalizes a `>>> why` line (the
   trailing full stop stripped) must still match its own row -- FAIL on the
   pin for `CHOOSE A CONNECTION ...` (A-36). Recorded in `stage-e/s1-before.txt`.
2. **The fix:** the two rows added with their French; the full-stop row
   normalized (in the table, so the French key matches the source byte for
   byte); the comment at `:419-422` rewritten to what the test actually does;
   PL-08's comments rewritten to the shipped behaviour (the fallback map's
   words, `SKIPPED - A GAME WAS STARTED`, "four words", the translation
   contract, `COMPLETED WITH GAPS` -- each to the current string or removed),
   ASCII only.
3. **The positive, after:** the three cases PASS; `t18-why-table.py`'s
   assertions updated to the new counts and seen to exit 0 on the fix and 1
   on the pin (`stage-e/s1-after.txt`); `es-untranslated` 0 in the eight.
4. **`Already written:`** nothing persisted: the table is read at run time;
   a device with the old binary shows the fallback sentence until the pin
   moves.
5. **Commit:** `CloudText: two why rows the scripts print, the full stop
   normalized, the comments made true (Refs #665, #<bug>)`.

## S2 -- `writeStamp` (PL-01)

File: `es-app/src/ThreadedCloudSync.cpp` (`:892-949`, the writer; the restamp
that logs success).

1. **Before:** a case in `es-app/tests/unit` (or `tests/app-unit` with the
   fake) writing the stamp into a directory made unwritable, then reading
   it back: on the pin the previous stamp is replaced by an empty or stale
   temporary and the log says success -- FAIL recorded.
2. **The fix:** the write through `Utils::AtomicFile::writeText` (tested in
   this slice), its result returned by `writeStamp`, and the restamp's log
   line written from the result (success only on success; otherwise the
   previous stamp stands and the log says it could not be written).
3. **After:** the case PASS; the stamp's previous line intact under the
   failure. D-CLOUD-078 named in the bug.
4. **`Already written:`** stamps on devices are read as they are; a stamp
   the old code truncated reads as the row's "not done yet" until the next
   run rewrites it; nothing migrated.
5. **Commit:** `ThreadedCloudSync: write the stamp atomically and say when
   it could not be (Refs #665, #<bug>)`.

## S3 -- the words (PL-02, PL-05, PL-07, PL-14's unfitted rows)

Files: `es-app/src/guis/GuiCloudTransfer.cpp` (`:357-358` the CANCEL
confirmation; `:807-808` the 640-px forms; the `DID NOT FINISH` / `CAME DOWN`
lines; the rows set without `fitOneLine`), `es-app/src/CloudText.cpp`
(`outcomeCandidates` where the candidates live), the French catalog,
`docs/es-menu-map.md` (the transfer page's dialog line, D-UI-039).

The words, the coordinator's (`es-player-text.md`: a statement, one
consequence, two verbs; the canonical verb, never a paraphrase; D-UI-035
the longer candidate first):

- **The CANCEL confirmation over a match** (PL-02), a new arm beside the
  backup/restore one: `CANCEL THIS MATCH?\n\nWHAT'S ALREADY BEEN REMOVED
  STAYS REMOVED. CHECK WHAT WOULD CHANGE AGAIN TO FINISH.` -- the same
  buttons as the existing dialog, the back button landing on NO.
- **PL-05**, the 640-px forms: `NOTHING NEW TO RESTORE` / `NOTHING NEW TO
  BACK UP` (the long forms stay the long forms).
- **PL-07:** `DID NOT FINISH` → `COULDN'T FINISH` (the outcome word,
  D-UI-028); `CAME DOWN` → the restore verb's form in the same slot (`N
  FILES RESTORED`; the backup half, if it has a twin, `N FILES BACKED UP`).
- **PL-14:** every row set without `fitOneLine` goes through it (A-40).

1. **Before:** `outcomeCandidates`/`chooseThatFits` cases for the new
   candidates FAIL on the pin where the strings are pure; for the dialog, the
   window's `pin-binary` frame of the match's CANCEL dialog is the before
   (or, where the walk did not reach it, `CANNOT` with #1141 cited and the
   before owed to the integration build's walk).
2. **The fix:** the strings and their French; the dialog's Match arm; the
   `fitOneLine` calls.
3. **After:** the cases PASS; the walk steps under `stage-e/walks/` for the
   dialog and the done page; `fix-walk-pending-image`; the menu map's line
   updated in the distribution worktree.
4. **`Already written:`** nothing persisted.
5. **Commit:** `GuiCloudTransfer, CloudText: the match's cancel words, the
   640-px forms, the outcome verbs, every row fitted (Refs #665, #<bug>)`.

## S4 -- the card's wrapper, and the glued line (PL-04, PL-19)

Files: `es-app/src/ThreadedCloudSync.cpp` (`:206-208`, the wrapper),
`es-app/src/CloudTransferJob.cpp` (`:636-638`, the job's, the model), a host
fixture under the audit folder's `tools/`.

1. **Before:** a host fixture runs a script through each wrapper string with
   the read end closed early (the interface gone): the job's wrapper keeps
   the script alive to its stamp, the card's dies on SIGPIPE -- FAIL
   recorded. The same fixture feeds the reader a `>>> ` line glued to an
   unterminated rclone tail (PL-19, A-35) and records whether the marker is
   found (the donor's rclone at
   `/workspace/artifacts/m6-donor/1a0266484423/image/system/usr/bin/rclone`
   may produce the real tail; the fixture says which it used).
2. **The fix:** one wrapper shape for both, `trap '' PIPE` before the pid
   echo; PL-19 fixed **only if its fixture falls**, else recorded as
   written with the fixture's output.
3. **After:** the fixture PASS; `fix-walk-pending-image` for the card's
   stamp after the interface restarts mid-sync (the walk under
   `stage-e/walks/`).
4. **`Already written:`** nothing persisted.
5. **Commit:** `ThreadedCloudSync: the card's scripts survive the interface
   going away, as the job's do (Refs #665, #<bug>)`.

## S5 -- a stop or cancel against an ending run (PL-18)

Files: `es-app/src/ThreadedCloudSync.cpp` (`cancelForLaunch`, the linger
`:731`, the outcome's restamp), `es-app/src/CloudTransferJob.cpp`
(`requestStop` `:139`, the late pid), `tests/app-unit/` (`jobs-tests`,
`proxycards-tests` shapes).

1. **Before:** cases: a cancel arriving after the run completed must leave
   COMPLETED (on the pin it relabels to `SKIPPED - YOU STARTED A GAME`);
   a stop after the job failed on its own must leave the failure (not
   "cancelled"); a cancel before the pid is known must be delivered when
   the pid arrives (on the pin it is lost); a launch during the card's
   linger must not run `CloudOffer`/`ProxyCards::afterSync` after it --
   FAIL recorded for each.
2. **The fix:** the outcome taken from the run's own exit when the run has
   ended; the cancel's intent kept until the pid arrives; the linger's
   launch gate. **`afterSync`'s own guard is routed to #667** (T20, the
   cards' side), not changed here.
3. **After:** the cases PASS; the walk for the launch over an ending card
   under `stage-e/walks/`, `fix-walk-pending-image`.
4. **`Already written:`** a stamp an old binary relabelled stays as written;
   the next run rewrites it; nothing migrated.
5. **Commit:** `ThreadedCloudSync, CloudTransferJob: a stop or cancel never
   relabels a run that has ended, and reaches a late pid (Refs #665, #<bug>)`.

## S6 -- the job's why handling (PL-20, PL-22)

Files: `es-app/src/CloudTransferJob.cpp` (the part/unit bookkeeping, `mWhy`),
`es-app/src/guis/GuiCloudTransfer.cpp` (the outcome's line 4),
`es-app/src/CloudText.cpp` (the stamp's offline why, as the card reads it),
`es-app/tests/unit/CloudTextTests.cpp`, `tests/app-unit/jobs-tests`.

1. **Before:** a case feeding a part's early `>>> why` before its unit line:
   on the pin it is filed under the previous part (A-37) -- FAIL; a case with
   a content transfer's stamp carrying the offline why (`69 gaps`, `YOU WENT
   OFFLINE PART-WAY THROUGH`): on the pin the page's line 4 is blank (R-42)
   -- FAIL.
2. **The fix:** the why attached to the part that printed it; the page reads
   the stamp's offline why as the card does (one reader where the change is
   small; otherwise the same rule in both, and #1143 keeps the refactor).
3. **After:** the cases PASS; the page's line 4 shows the why in a
   `fix-walk-pending-image` frame (the walk under `stage-e/walks/`).
4. **`Already written:`** stamps are read as they are.
5. **Commit:** `CloudTransferJob, GuiCloudTransfer: a part's why stays with
   its part, and the page says why a cut transfer stopped (Refs #665, #<bug>)`.

## The record

- `02` § The streams: one row per stream with the positive before, the
  commit (the ES hash), the positive after, the `Already written:` answer and
  `proved: fix-unit-test` / `fixture` / `fix-walk-pending-image`; `05`'s rows
  for PL-01, 02, 03, 04, 05, 07, 08, 14, 18, 19, 20, 22 point at it; PL-09
  deferred to #909; PL-15 to #1142; PL-11, 12, 23 and PL-16's refactor to
  #1143; PL-16's suites to #1144; PL-17 and PL-21's composers' half to #673;
  PL-06, 10, 13, 21's readers' half recorded as written.
- `00`: the stage-E entry naming the generated build command's source list,
  the syntax check's result per file (or its `CANNOT`), and each fixture's
  command.
- The hand-back after stage E's record, as the brief's § 10: **both tips**
  (the distribution branch's and the ES branch's), the artifacts by path,
  `reviewed-at:` and `fixed-at:` in #665's body (`fixed-at` the ES tip).

## What never runs here

A build, a compiler beyond `g++ -fsyntax-only` and the generated test
build, a guest, a fetch, a keyed council call, anything on a unit, a change
under the distribution's `packages/`, `projects/` or `tools/`, a change in
the ES worktree outside the files each stream names, a move of the pin.

**Erratum at acceptance (2026-10-26).** S1's first case named D-UI-117's long
sentence, which is `backuptool`'s console `fail` text at `:1496`; the `>>> why`
a reader receives is the short sentence at `:1495`, `THIS BACKUP HOLDS FILES A
RESTORE CAN'T PUT BACK`, and S1's row is that one (the lane's correction at
stage D, `1a1828a8b`). PL-19's fixture did not reproduce the glued line with
the donor's rclone 1.75.2, so S4 fixed only the wrapper (Withdrawn, as the
brief allowed). S6 also covered the composed run's part that ended 69 without
a word (`GuiMenu.cpp:5006`), beyond the brief.
