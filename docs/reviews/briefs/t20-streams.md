# Stream brief: M6.P2 T20, stage E (#667)

**The coordinator's, 2026-10-26, at T20's stage-D pause** (the lane's comment
of 18:39 UTC; the punch list at `d3b1adc2e4`, 25 items; the audit issue
#1167). Twelve streams, serial, in this order, **on the EmulationStation
branch `feature/m6-es-achievements-pages-667`** in the lane's ES worktree
`/home/max/Development/emulationstation-next.worktrees/m6-es-achievements-pages-667`
(at the pin `16dbac5211` until S1 lands), with S12 alone on the distribution
branch. The dispositions that are not streams are in the ruling on #667;
this file is only what changes code.

## The rules every stream keeps

- **Test first, then the fix, and the test's FAIL is recorded before the fix
  lands** (`engineering-practices.md` § Guards must fail closed). The host
  has no cross toolchain (#1137): the proof of choice is a case in the unit
  tests built by the lane's generated commands (`tools/t20-build-tests.sh`,
  `t20-build-app-tests.sh`; rapidjson from the download cache's own
  tarball with the recipe's patches), run before every commit on the ES
  branch -- `es-unit-tests`, `es-file-tests`, `es-conf-tests`, `jobs-tests`,
  `proxycards-tests` as each stream names; a pure helper that has no unit
  yet becomes one (`es-code-traps.md` § Pure text has a home). A fix only a
  guest can show is `fix-walk-pending-image`: **no guest runs in stage E**
  (M7 holds the host under the 18:19 chain until its RETURN, and T20's one
  window is spent); its walk's steps go under the audit folder's
  `stage-e/walks/` for the integration's window. Fixture compiles stay
  single-threaded `g++` runs of seconds while M7 holds the host.
- **The files in the slice only**, on the ES branch; `FileSystemUtil.cpp`
  (S8, upstream-carried) under `bugs-are-agent-first.md` rule 6 with a #585
  line; `ApiSystem.cpp` and `HttpReq.cpp` are T21's (#668) and do not change
  here; the ctl is T19's and does not change here. `docs/es-menu-map.md`
  (S12) changes on the distribution branch, D-UI-039.
- **Every string a player reads** follows `es-player-text.md` and
  `player-language.md`; a new or changed `_("")` string ships with its
  French in `locale/lang/fr/LC_MESSAGES/emulationstation2.po` in the same
  commit (D-UI-051), and `tools/es-untranslated --upstream bccd715707`
  stays at 0 without. No non-ASCII byte in a comment near a `_()` (the
  grep before each commit). `rc=$?` on its own line.
- **Every stream answers `Already written:`** in its bug and in `02` § The
  streams (`upgrade-and-install.md`, D-WORKFLOW-050).
- **One commit per stream**, the ES package's convention, `Refs #667,
  #<bug>`; the paths named; no closing keyword; before each ES commit the
  unit tests' summary lines, the non-ASCII grep, and the ES fork's
  `.githooks/pre-push-test` after the branch moves; `tools/register-check`
  before each distribution commit. A source cites its bug number, never a
  register row (D-WORKFLOW-211's practice; the rows reach the lane at
  hand-back).
- **The bug first** (D-WORKFLOW-187/189): the lane files each stream's `bug`
  before the stream, with the trace, the `Already written:` line and the VM
  line from the punch item, severity as ruled below; `fixed-at-es` into the
  bug at the commit; a bug with every checkbox ticked stays open until the
  pin moves on `next`.
- **No guest, no build, no fetch, no keyed call, nothing on a unit or an
  account; the pin is not moved by the lane.** `rm -rf` only as
  `"${VAR:?}"/...` or a literal path, in its own short command.

## S1 -- PL-01 (High, #bug-1): one owner for the hasher's lifetime

Files: `es-app/src/ThreadedHasher.{h,cpp}` (fork-modified); a new unit under
`tests/app-unit/` or `es-app/tests/unit/` for the lifetime.

1. **The positive, before.** The lifetime moved into a testable unit --
   the queue, the workers, the completion, the publication and `stop()`,
   with `Window`, `FileData` and `SystemData` behind fakes as
   `tests/app-unit/fakes/` already does -- and a short-queue schedule in
   which every worker ends before `start()` returns, built with
   `-fsanitize=address,undefined`: the pin's shape (the constructor starts
   the workers at `:138-139`, the last worker's `delete this` and the
   nulling of `mInstance` at `:258-265`, `start()` reading the freed object
   at `:378-392`, `stop()` writing through it at `:403-411`) fails under
   the sanitizer. `stage-e/s1-before.txt`.
2. **The fix** (both seats' shape): a retained job owns the hasher; every
   member is initialized and `mInstance` published before any worker
   starts; completion, publication and `stop()` are coordinated under that
   one lifetime; `mExit` and the counters are `std::atomic`; every
   `std::thread` is joined or detached and its object deleted; a second
   `start()` while a run lives is refused or queued, never a second owner.
3. **The positive, after:** the schedule passes under the sanitizer;
   `stop()` during and after a run touches no freed object; no thread
   leaks across two runs; the existing callers (`SystemData.cpp:1134`,
   `NetworkThread.cpp:251`, `GuiMenu.cpp:1214`,
   `GuiRetroAchievementsSettings.cpp:800`) unchanged in behaviour by
   reading; the silent startup run is `fix-walk-pending-image`.
   `stage-e/s1-after.txt`.
4. **`Already written:`** recovery metadata, the daily `CheevosLookupOnlyLast`
   stamp and a destructor's top-up may have run before a failure; kept,
   the next run reconciles; nothing on disk or in a cloud is corrupted by
   the race. Nothing migrated.
5. **Commit:** `ThreadedHasher: one owner for the hasher's lifetime, published
   before the workers start (Refs #667, #<bug-1>)`.

## S2 -- PL-02 (Medium, #bug-2): the sign-in's credential out of the URL, and no `http` for it

Files: `es-app/src/RetroAchievements.cpp` (`testAccount` `:1037`, the request
builder); the caller's half of #1154 -- `HttpReq.cpp`'s verification is
T21's and does not change here.

1. **Establish, from the tree, not the network:** whether the service
   takes the login by POST body -- the vendored client's own request
   builder (`external/libcheevos/rcheevos/src/rapi/rc_api_user.c`, the
   login request's `post_data`) decides it; record the lines in `02`.
2. **The positive, before:** on the host, a unit over the request builder
   (pure once lifted) showing the password in the URL's query; the guest's
   self-signed listener recorded `p=` in the request line (the window's
   `g07`), `fix-walk-pending-image` for the after.
3. **The fix:** the credentials in the POST body (`options.dataToPost`,
   `HttpReq.cpp:165-170`) when the service takes them there, else the
   request refused rather than sent over a redirect; **an `https`-only
   redirect policy for any request that carries a credential**, set through
   `HttpReqOptions` as the pin provides (a field the lane adds to the
   options if none exists, in `HttpReq.h` -- T21's file; the lane names the
   one field and the coordinator rules at the next question if more is
   needed); the hash library's and the pages' requests unchanged.
4. **The positive, after:** the unit shows no `p=` in any URL; the listener
   walk pending-image. `stage-e/s2-*.txt`.
5. **`Already written:`** passwords already sent in a query cannot be
   recalled from whoever held the link; `system.cfg` keeps the account's
   password and token as before; nothing migrated; a credential rotation is
   the player's own response.
6. **Commit:** `RetroAchievements: the sign-in's credential in the request
   body, and no http redirect for it (Refs #667, #<bug-2>)`.

## S3 -- PL-03 (Medium, #bug-3) and PL-16's cancel: the job's pid taken once, and a CANCEL that can be pressed again

Files: `es-app/src/OfflineScanJob.{h,cpp}` (fork-own).

1. **Before:** a `jobs-tests` case feeds `handleLine` the wrapper's pid line
   then `>>> pid 1`: `mPid` becomes 1 and `cancel()` would signal `-1`;
   a second case marks the job cancelled before the signal and refuses a
   second CANCEL. `stage-e/s3-before.txt`.
2. **The fix:** `pid` taken once, while `mPid == 0`, from the wrapper's
   first line, and only when above 1; a later `>>> pid` line ignored and
   logged; `cancel()` marks cancelled only after the signal was delivered
   (its failure reported, the state unchanged) so a CANCEL that did not
   land can be pressed again.
3. **After:** both cases pass. `stage-e/s3-after.txt`. The guest walk with
   a CR-named ROM is `fix-walk-pending-image` (T19's S9 replaces control
   characters in names on the ctl's side after integration).
4. **`Already written:`** nothing inherited; the reader keeps no state
   across runs.
5. **Commit:** `OfflineScanJob: the pid taken once and above 1; a CANCEL that
   did not land can be pressed again (Refs #667, #<bug-3>)`.

## S4 -- PL-04 (Medium, #bug-4), PL-18 and PL-23's comment: the page reads the file back

Files: `es-app/src/guis/GuiRetroAchievementsSettings.cpp` (fork-own).

1. **Before:** the pure part -- the outcome from `system.cfg`'s two keys
   (the toggle, hardcore) -- lifted into `CloudText`-style code with a
   unit case: an exit 1 after the toggle was written off reads as on at
   the pin (`:490-496` reverts the switch). `stage-e/s4-before.txt`.
2. **The fix:** after any exit of `enable`/`disable`, the page reads the
   state back from `system.cfg` (the toggle and hardcore) and sets its rows
   and `SystemConf` from the file, separately from whether every step
   succeeded (never re-enabling automatically); the dialog says it could
   not finish when the exit was non-zero. PL-18: the LED switch's callback
   captures itself weakly (`:688`); the toggle's thread posts through
   `AppWindow::post` (`:484`). PL-23: the comment at `:154` names
   `have_account` as what it is.
3. **After:** the unit case passes; the stub-ctl walk (writes the toggle
   off and exits 1; exits 1 before any write) is `fix-walk-pending-image`.
   `stage-e/s4-after.txt`.
4. **`Already written:`** a device may hold the toggle off while the page
   showed on; the fix reads the file each time, so the inherited state is
   read, not migrated.
5. **Commit:** `GuiRetroAchievementsSettings: the toggle's state read back
   from system.cfg after any exit; two lifetimes (Refs #667, #<bug-4>)`.

## S5 -- PL-05 (Medium, #bug-5) and PL-15: a non-number is not 0

Files: `es-app/src/OfflineScanJob.cpp`, `es-app/src/CloudText.{h,cpp}`,
`es-app/src/OfflineAchievements.cpp` (fork-own).

1. **Before:** `jobs-tests` and `es-unit-tests` cases (`stage-b/positives/num.cpp`,
   `StampProbe.cpp` are the fixtures): `>>> done 3|0|unknown|0` sets `ready`
   to 0 and the page says NO GAMES READY FOR OFFLINE PLAY YET; a stamp with
   `ready=unknown` and numeric `added` makes the card say EVERYTHING'S UP TO
   DATE; PL-15's readers: an all-malformed summary is `ok`, an unreadable
   pending list is "none", a missing ready file is 0.
   `stage-e/s5-before.txt`.
2. **The fix:** a `ReadyUnknown` sentinel beside `AddedUnknown`; the page
   keeps -1 for a non-number and counts from the export; the stamp's
   reader carries unknown through to the card (no count said); old numeric
   stamps read as before; PL-15: validity carried beside the data
   (`storeSummary`, the ready file, `pending-ids`), an all-malformed or
   unreadable input is not `ok`, not "none", not 0.
3. **After:** every case passes. `stage-e/s5-after.txt`.
4. **`Already written:`** after integration a store may hold `ready=unknown`
   stamps (T19's S8), which the fixed parser reads; older numeric zeros
   cannot be told apart and are left as they are.
5. **Commit:** `OfflineScanJob, CloudText, OfflineAchievements: unknown is
   not zero, and an unreadable answer is not an empty one (Refs #667,
   #<bug-5>)`.

## S6 -- PL-06 (Medium, #bug-6), PL-17 and PL-19's comment: the sign-in off the thread, bounded, tied to its account

Files: `es-app/src/guis/GuiRetroAchievementsSettings.cpp`,
`es-app/src/RetroAchievements.cpp` (fork-modified).

1. **Before:** a host case over the options the sign-in uses (connect 10 s,
   total 0, stall 0 at the pin); the freeze at the page's close with a
   listener that accepts and never answers is the window's shape,
   `fix-walk-pending-image`. PL-17: a case showing `offlineScanStart`'s
   save at `:321` lands before the parent's token handling (`:743-807`), so
   a scan runs with the new name and the old token. `stage-e/s6-before.txt`.
2. **The fix:** the sign-in at the page's close runs off the interface
   thread, as the watcher's does, with a total and a stall bound
   (`HttpReqOptions` as the pin provides them), its token tied to the
   account revision that asked for it; PL-17: an account change clears or
   replaces the token before any scan start saves, so a scan never runs
   with another account's token; PL-19: the comment at
   `RetroAchievements.cpp:173` says what `:178-185` does (the username in
   the `User-Agent` when an API login exists -- recorded as written, the
   name is not a secret).
3. **After:** the options case and the token-revision case pass; the
   freeze walk pending-image. `stage-e/s6-after.txt`.
4. **`Already written:`** a token already stored is the same token; a
   device may briefly hold a new name beside an old token until the page
   closes -- read, not migrated.
5. **Commit:** `RetroAchievements, GuiRetroAchievementsSettings: the sign-in
   off the interface thread and bounded; a scan never runs with another
   account's token (Refs #667, #<bug-6>)`.

## S7 -- PL-12 (Low, #bug-7): the top-up's card takes only its own run

Files: `es-app/src/ProxyCards.cpp`, `es-app/src/CloudText.{h,cpp}`, the
French catalog.

1. **Before:** a `proxycards-tests` case: a scan's `running` file and a
   scan's stamp newer than the top-up's start are adopted as the top-up's
   (`ProxyCards.cpp:274`, `:314-320`); `es-unit-tests`: `STAMP_UNWRITABLE`
   and `RESULT_UNREADABLE` have no row. `stage-e/s7-before.txt`.
2. **The fix:** the card matches `route=topup` and `topup` and an explicit
   run identity; `topUpRunning()` reads liveness from the run, not the
   file's presence (PL-13's page half from T19); the two tokens get their
   rows in English and French (`TOOK_TOO_LONG` already falls through to
   `scanWhy`'s row); `NO_GAMES_FOUND`'s dead row is recorded (PL-23), not
   removed.
3. **After:** the cases pass; `es-untranslated` 0. `stage-e/s7-after.txt`.
4. **`Already written:`** nothing inherited.
5. **Commit:** `ProxyCards, CloudText: the top-up's card takes only its own
   run; two why rows (Refs #667, #<bug-7>)`.

## S8 -- PL-09 (Low, #bug-8): a file under three bytes

File: `es-core/src/utils/FileSystemUtil.cpp` (`skipUtf8Bom` `:1369-1379`,
`readAllText` `:1418-1427`; upstream-carried, rule 6, a #585 line to
batocera's tree in `02` § The #585 lines).

1. **Before:** `es-file-tests` cases for 0-, 1-, 2- and 3-byte files and a
   BOM-prefixed file (the fixture `readall.cpp`): the 1- and 2-byte files
   read as `""`. `stage-e/s8-before.txt`.
2. **The fix:** `file.clear()` before `seekg(0)`; `readAllLines` mended
   with it.
3. **After:** the bytes of every file returned, the BOM still skipped;
   `7\n` counts one game ready is `fix-walk-pending-image`.
   `stage-e/s8-after.txt`.
4. **`Already written:`** nothing inherited: the files are read afresh.
5. **Commit:** `FileSystemUtil: readAllText reads a file under three bytes
   (Refs #667, #<bug-8>)`.

## S9 -- PL-10 (Low, #bug-9), PL-11 and PL-16's words: the player's words on every failure surface

Files: `es-app/src/RetroAchievements.cpp` (`:925`, `:165`, `:737`),
`es-app/src/ThreadedHasher.cpp` (`:117`, `:146`, `:383-390`, `:399`),
`es-app/src/guis/GuiRetroAchievements.cpp` (`:44`),
`es-app/src/guis/GuiGameAchievements.cpp` (`:41-42`),
`es-app/src/guis/GuiRetroAchievementsSettings.cpp` (`:784`), `CloudText`
for the sentences, the French catalog.

1. **Before:** a host case (`slice.cpp`'s shape) showing `throw e;`
   slicing the hasher's error to `std::exception`; the window's `g05` log
   line; a unit over the sentence chooser showing the server's `Error`,
   curl's message and the `AN ERROR OCCURRED` prefix reaching the screen.
   `stage-e/s9-before.txt`.
2. **The fix:** `throw;` (or no rethrow) with the cause logged; every
   failure surface shows a sentence from the fork's catalog in the
   player's words (`player-language.md`; `es-player-text.md` § Outcome
   words: the register everyday, not formal), the detail to the log; the
   game page's prefix dropped where the sentence already says what
   happened; PL-16: a stopped hasher says it was stopped, not INDEXING
   COMPLETED (`:146` reads `mExit`); an empty library without an exception
   (a captive portal's 200) says the library could not be read, not NO
   GAMES FIT THAT CRITERIA. French for every new or changed string.
3. **After:** the cases pass; `es-untranslated` 0; the frames
   `fix-walk-pending-image`. `stage-e/s9-after.txt`.
4. **`Already written:`** nothing inherited.
5. **Commit:** `RetroAchievements, ThreadedHasher, the pages: the player's
   words on every failure surface, the cause in the log (Refs #667,
   #<bug-9>)`.

## S10 -- PL-13 (Low, #bug-10; D-RA-052): HARDCORE MODE gated while offline achievements are on

File: `es-app/src/guis/GuiRetroAchievementsSettings.cpp` (`:621`).

1. **Before:** a host case over the rows' build: with `offlineproxy=1` the
   HARDCORE MODE switch is selectable and writable. `stage-e/s10-before.txt`.
2. **The fix (the ruling):** D-RA-001's casual-only feature is enforced at
   the switch -- while offline achievements are on, HARDCORE MODE is
   **dimmed, not hidden** (`es-ui-style-guide.md` § Dim, don't hide), with
   one line under it in the player's words saying why and where (its
   sentence proposed by the lane, with French; D-UI-023's two lines), and
   its value is not writable from the page; `disable`'s restore of the
   record taken at `enable` (T19's ctl) is consistent with the gate and
   stays. Devices holding both keys on are read as they are (the ctl's
   next `disable` restores its record; nothing rewritten by the page).
3. **After:** the case passes; the frame at 640x480 `fix-walk-pending-image`.
   `stage-e/s10-after.txt`.
4. **`Already written:`** devices may hold both on; the page reads both
   keys and rewrites neither.
5. **Commit:** `GuiRetroAchievementsSettings: HARDCORE MODE dimmed with its
   reason while offline achievements are on (Refs #667, #<bug-10>)`.

## S11 -- PL-14 (Low, #bug-11): a sign-in needs a usable token; JSON by type

File: `es-app/src/RetroAchievements.cpp` (`:879-880`, `:904-905`,
`:1052-1056`, `:1064`); the parse lifted into pure code with a unit.

1. **Before:** a unit over the lifted parse: `Success` without `Token`
   counts as signed in; `Token`, `Error`, `Response`, `MD5List` used without
   `IsString()`/`IsObject()`. `stage-e/s11-before.txt`.
2. **The fix:** a `Success` without a usable token is a failure; every
   member type-checked, a malformed member refused without an assertion.
3. **After:** the cases pass. `stage-e/s11-after.txt`.
4. **`Already written:`** an empty token stored this way is retried by the
   watcher; nothing to migrate.
5. **Commit:** `RetroAchievements: a sign-in needs a usable token, and the
   answer's members are read by type (Refs #667, #<bug-11>)`.

## S12 -- PL-20: the menu map (a docs commit on the distribution branch)

File: `docs/es-menu-map.md` (D-UI-039).

1. **The fix:** `:595`'s line describes the scan page as it ships (the
   fourth-tier page with CANCEL, D-UI-078, not the leavable design); the
   scan page's title `SCANNING GAMES FOR OFFLINE ACHIEVEMENTS` and its rows
   mapped; `tools/es-menu-map-check --es-src <W> --ref <pin>` prints
   `0 missing` and the map's `## Not mapped` unchanged.
2. **Commit** (the distribution branch): `docs: the menu map's scan page and
   its running line as they ship (Refs #667)`. No bug.

## The record

- `02` § The streams: one row per stream with the positive before, the
  commit, the positive after, the `Already written:` answer and `proved:
  fix-unit-test` or `fix-walk-pending-image`; `05`'s PL-01 to PL-06,
  PL-09 to PL-18, PL-20 and PL-23 rows point at it; the other rows take
  the outcome the ruling gives them.
- `02` § What T21 and T26 inherit: PL-08's reader (deferred to #668 with
  its fixture `reader.cpp`), the `HttpReqOptions` field S2 touches, the
  gates and the title's source for T26; § The #585 lines: PL-21's four and
  S8's one, in the lane's shape, for the coordinator to post.
- `00`: the stage-E entry naming the generated build's commands, every
  fixture's command, and that no guest ran.
- The hand-back after stage E's record, F, G and H as the brief's § 10:
  **both tips**, the artifacts by path, `reviewed-at:`, `reviewed-at-es:`,
  `fixed-at:` and `fixed-at-es:` in #667's body, the audit issue and the
  eleven bugs named.

## What never runs here

A build, a guest, a fetch, a keyed council call, anything on a unit or an
account, a change to `ApiSystem.cpp`, `HttpReq.cpp` beyond S2's one options
field, the ctl, or any file outside the slice and the audit folder, a move
of the pin.
