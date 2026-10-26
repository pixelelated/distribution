# Punch list — M6.P2 T20, EmulationStation's RetroAchievements and offline pages (#667)

**Extended depth:** two seats, GPT-6 Astra at `max`, then Gemini 4 Argon at `high` (`04` § Second opinion). The audit issue is #1167, a sub-issue of #667, opened at stage D.

- **Eleven `bug`s, filed by the lane at the stage-D ruling (#667, 18:45 UTC):** #1170 (PL-01, High); #1171 to #1175 (PL-02 to PL-06 with their companions, Medium); #1176 (PL-12), #1177 (PL-09), #1178 (PL-10, PL-11, PL-16's words), #1179 (PL-13, D-RA-052) and #1180 (PL-14), Low.
- **The streams:** `docs/reviews/briefs/t20-streams.md` at `60c1dc2db3`, S1 to S11 on the ES branch, S12 on the distribution branch.
- **Nothing in this list changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. Removals: none; every dead end is a proposal.
- **One guest window,** 17:36:17 to 17:57:04 UTC at 640x480, on an image whose EmulationStation is M7's composition over the pin (`02` § The guest cycle). **Nothing ran on a person's device or cloud.**

---

## PL-01: the hasher's lifetime: start() and the constructor use and publish a hasher its own threads may have deleted (a `bug` proposed)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-21, L-22, L-26 (threads); A-12, A-13, A-44, A-45, R-9, R-10
- **Owner area:** es-app/src/ThreadedHasher.cpp (fork-modified)
- **What:**
  - **The cause:** the constructor starts the workers (`ThreadedHasher.cpp:138-139`), and the last worker runs `delete this` and nulls `mInstance` (`:258-265`).
    - `start()` then reads `hasher->mCheevosHashes` and `hasher->mTotal` and writes `mInstance = hasher` (`:378-392`).
    - The constructor's own final `push_back` can follow the deletion.
    - `stop()` writes `mExit` through an unretained pointer (`:403-411`), and `mExit` is a plain `bool` read by the workers.
    - The `std::thread*` objects are never joined, detached or deleted.
  - **When:** a short queue with at least one recognized hash, such as the silent lookups-alone run whose `start()` writes `es_settings.cfg` in that window, or a one-game queue.
  - **The fix shape (both seats):** a retained job owns the hasher. Everything is initialized and published before the workers start. Completion, publication and `stop()` are coordinated under one lifetime, with `std::atomic` flags and the threads joined or detached.
- **Can this be done on the VM?** Partly. The constructor and `start()` need `Window`, `FileData` and `SystemData`, so the host fixture is `CANNOT` as the class stands. A stream that moves the lifetime into a unit gets a `fix-unit-test`, with a short-queue schedule run under a sanitizer; the guest's silent startup run is the integration walk (`fix-walk-pending-image`).
- **Already written:** recovery metadata, the daily `CheevosLookupOnlyLast` stamp and a destructor's top-up may have happened before a failure. They are kept, and the next run reconciles; nothing on disk or in a cloud is corrupted by the race itself (A-44, R-21).
- **Acceptance:** a short-queue schedule in which every worker ends before `start()` returns reads and publishes no freed object (a case that fails on the pin's lifetime); `stop()` during and after a run touches no freed object; no `std::thread` is leaked across two runs
- **Disposition note:** `bug` #1170 (High), stream S1, at the stage-D ruling (#667, 18:45 UTC)

## PL-02: the sign-in sends the password in the login's query string to a peer nobody verified, with redirects followed to `http` (a `bug` proposed, the caller's half of #1154)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** L-01; A-2, A-24, R-2, R-18; guest `g07`
- **Owner area:** es-app/src/RetroAchievements.cpp (fork-modified); es-core/src/HttpReq.cpp (#1154)
- **What:**
  - **The cause:** `testAccount` builds `dorequest.php?r=login&u=…&p=…` (`RetroAchievements.cpp:1037`). `HttpReq` disables peer verification (`HttpReq.cpp:192`) and follows up to two redirects to `http` or `https`.
  - **Proved on the guest:** with dummy credentials, the sign-in reached a self-signed listener for `retroachievements.org` one second after ES started, while a CA-checking `curl` was refused.
  - **The fix shape:**
    - the transport's verification and an `https`-only redirect for credential requests (#1154);
    - the credentials in a POST body (`options.dataToPost`, `HttpReq.cpp:165-170`) if the service accepts them there, which the stream's first step establishes.
- **Can this be done on the VM?** Yes. The guest's self-signed listener on loopback, with the name in `/etc/hosts` (`guest-cycle/scripts/tls-probe.py`), is the positive: it fails on the pin and passes once the request is refused or carries no `p=`.
- **Already written:** passwords already sent this way cannot be recalled from whoever held the link (A-24). `system.cfg` keeps the account's password and token, as before. Nothing to migrate; a credential rotation is the player's own response, not the fix's.
- **Acceptance:** against the guest's self-signed listener the sign-in is refused before any request line arrives, and no request line the listener records carries a `p=` value; an `http` redirect is not followed for a credential request
- **Disposition note:** `bug` #1171, stream S2; the transport stays #1154's (T21, #668), at the stage-D ruling (#667, 18:45 UTC)

## PL-03: a second `>>> pid` line, which an unreplaced ROM name can plant, turns CANCEL into `kill(-1, SIGINT)` as root (a `bug` proposed)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** L-10; A-11, A-33, R-5, R-19
- **Owner area:** es-app/src/OfflineScanJob.cpp (fork-own)
- **What:**
  - **The cause:** `handleLine` takes `pid` from any line (`OfflineScanJob.cpp:209-219`), and `cancel()` signals `-pid` (`:77-78`).
    - At `8ebaf8daad` the ctl prints the ROM's basename unreplaced in its `game` line (`raofflineproxy-ctl:1723`, `:1778`).
    - The reader ends a line at `\r` (`:143`).
    - So a file named with a CR and `>>> pid 1` sets `mPid` to 1, and a CANCEL signals every process.
  - **T19's S9** replaces control characters in names, after integration. The reader's half is this slice's.
  - **The fix shape:** take `pid` once, while `mPid == 0`, from the wrapper's first line; require it above 1.
- **Can this be done on the VM?** Yes, on the host. A `jobs-tests`-style case feeds `handleLine` the wrapper's pid line, then a second `>>> pid 1`, and checks the group cancel would signal (`fix-unit-test`). The guest walk with such a ROM name is `fix-walk-pending-image`.
- **Already written:** nothing inherited: the reader keeps no state across runs.
- **Acceptance:** after the wrapper's pid line, a later `>>> pid` line (1 or any other) leaves the group unchanged, and `cancel()` never signals a group of 1 or less (a case that fails on the pin)
- **Disposition note:** `bug` #1172, stream S3 (with PL-16's cancel), at the stage-D ruling (#667, 18:45 UTC)

## PL-04: `disable` failing after it has written the toggle off leaves the page, and `SystemConf` in memory, saying on (a `bug` proposed)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-09; A-8, A-32, R-8, R-19
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp (fork-own)
- **What:**
  - **The cause:** `do_disable` writes the toggle off first (`raofflineproxy-ctl:523-524`), then can exit 1 at the hardcore restore, the record's clearing or the marker (`:538-544`). T19's S5 adds an exit 1 when the service will not stop.
    - On any non-zero exit the page reverts its switch to on and mirrors nothing (`GuiRetroAchievementsSettings.cpp:490-496`), so `OfflineAchievements::toggleOn()` answers yes for a feature that is off on disk.
  - **The fix shape:** after any exit, read the state back from `system.cfg` (the toggle and hardcore) and set the rows and `SystemConf` from it, separately from whether every step succeeded (A-32).
- **Can this be done on the VM?** Yes, on the guest, with a stub ctl that writes the toggle off and exits 1 (`fix-walk-pending-image`). The read-back's pure part, the outcome from the file's two keys, takes a host case.
- **Already written:** a device may hold the toggle off with the page having shown on. The fix reads the file each time, so the inherited state is read, not migrated (A-32: never re-enable automatically).
- **Acceptance:** with the ctl exiting 1 after writing the toggle off, the switch and `SystemConf` read off and the dialog says it could not finish; with it exiting 1 before any write, both read on
- **Disposition note:** `bug` #1173, stream S4 (with PL-18 and PL-23's comment), at the stage-D ruling (#667, 18:45 UTC)

## PL-05: `unknown` counts are read as 0 by the scan page and by the stamp's reader (a `bug` proposed, the seam with T19's S8)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-07; A-10, A-30, R-8, R-19
- **Owner area:** es-app/src/OfflineScanJob.cpp, es-app/src/CloudText.{h,cpp} (fork-own)
- **What:**
  - **The cause:** `>>> done c|s|unknown|limit` sets `ready` from -1 to `num("unknown") = 0` (`OfflineScanJob.cpp:196-205`, `:256`), and the page says `NO GAMES READY FOR OFFLINE PLAY YET`. `parseScanStamp` leaves `ready` at its default 0 for `ready=unknown` (`CloudText.cpp:1259-1266`, `CloudText.h:492`), and the card says `EVERYTHING'S UP TO DATE.` when `added` is numeric.
  - **The fix shape:** a `ReadyUnknown` sentinel beside `AddedUnknown`; the page keeps -1 for a non-number; old numeric stamps read as before.
- **Can this be done on the VM?** Yes, on the host: the `jobs-tests` and `es-unit-tests` cases (`stage-b/positives/num.cpp`, `StampProbe.cpp` are the fixtures), `fix-unit-test`.
- **Already written:** after integration a store may hold `ready=unknown` stamps; the fixed parser reads them. Older numeric zeros cannot be told apart and are left as they are (A-30).
- **Acceptance:** `>>> done 3|0|unknown|0` leaves the page counting from the export, and a stamp with `ready=unknown` and numeric `added` makes the card say no count; both fail on the pin
- **Disposition note:** `bug` #1174, stream S5 (with PL-15), at the stage-D ruling (#667, 18:45 UTC)

## PL-06: the sign-in at the settings page's close runs on the interface thread with no total and no stall bound (a `bug` proposed)

- **Severity:** Medium
- **Category:** Performance
- **Question:** Q3
- **Source Finding:** L-02; A-3, A-25, R-3, R-18
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp, es-app/src/RetroAchievements.cpp (fork-modified)
- **What:**
  - **The cause:** when `CheevosRetry::saveSignIn` answers `Now`, the save calls `testAccount` synchronously (`GuiRetroAchievementsSettings.cpp:772-776`), with `getHttpOptions()`'s connect 10 s, total 0 and stall 0 (`HttpReq.h:52-54`). A server that accepts and then stalls freezes the screen until TCP gives up (`es-code-traps.md` § A pooled connection).
  - **The fix shape:** the sign-in off the interface thread, as the watcher's already is, with a total and a stall bound, and the token tied to the account revision that asked for it (A-25).
- **Can this be done on the VM?** Yes, on the guest: a listener that accepts and never answers, and a frame series timing the screen's freeze at the page's close (`fix-walk-pending-image`). The bound's options take a host case.
- **Already written:** nothing inherited: a token already stored is the same token.
- **Acceptance:** with a listener that accepts and never answers, closing the page leaves the interface answering input within a second, and the sign-in ends within its bound with the reconnect dialog
- **Disposition note:** `bug` #1175, stream S6 (with PL-17 and PL-19's comment), at the stage-D ruling (#667, 18:45 UTC)

## PL-07: the hash library is fetched on the interface thread with no total bound

- **Severity:** Medium
- **Category:** Performance
- **Question:** Q5
- **Source Finding:** L-19; A-42, R-21
- **Owner area:** es-app/src/ThreadedHasher.cpp, es-app/src/RetroAchievements.cpp
- **What:**
  - **The cause:** the constructor fetches on its caller's thread, which is the interface thread for every caller (`ThreadedHasher.cpp:63`). Each request has connect 10 s and stall 30 s, and no total (`RetroAchievements.cpp:863`), so a transfer that keeps moving is not bounded.
  - **Owner:** #300 (moving the fetch off the thread).
- **Can this be done on the VM?** Yes, the guest's startup run with a slow listener; #300's.
- **Already written:** nothing inherited.
- **Acceptance:** #300's criteria
- **Disposition note:** Deferred: #300, at the stage-D ruling (#667, 18:45 UTC)

## PL-08: the shared process reader loses a long line's head, drops a last line without a newline, and reads a signal as exit 0

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q1
- **Source Finding:** L-05, L-06; A-5, A-6, A-28, A-29, R-5, R-6, R-18
- **Owner area:** es-app/src/ApiSystem.cpp (T21's function)
- **What:**
  - **The cause:** `executeScriptLegacy` (`ApiSystem.cpp:2278-2291`):
    - `fgets` into 1,024 bytes, and each fragment's `getline(...).good()`, drop a fragment without a newline;
    - `WEXITSTATUS` without `WIFEXITED`.
  - **Fixtures:** `stage-b/positives/reader.out`.
  - **On the image** the ctl's own death reads 128+N (bash forks), so a signal reads 0 only for the wrapping shell (guest `g02`).
  - **The fix shape (Q1, modernize):** one bounded logical-line reader for both readers. An oversized record is refused, not passed on cut; a signal is a failure. The function is T21's.
- **Can this be done on the VM?** Yes, on the host (the reader verbatim, `reader.cpp`), `fix-unit-test` once the reader is a unit.
- **Already written:** nothing inherited.
- **Acceptance:** a 1,500-byte record is refused, not passed cut; a last line without a newline is kept; a waited process killed by a signal is a failure
- **Disposition note:** Deferred: T21, #668 (with the fixture `reader.cpp`), at the stage-D ruling (#667, 18:45 UTC)

## PL-09: `readAllText` reads a file under three bytes as empty: one one-digit id reads as no games ready (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-13; A-15, A-36, A-55, R-12; guest `g06`
- **Owner area:** es-core/src/utils/FileSystemUtil.cpp (upstream-carried; a contained fix, `bugs-are-agent-first.md` rule 6)
- **What:**
  - **The cause:** `skipUtf8Bom` reads three bytes and seeks back without `clear()` (`FileSystemUtil.cpp:1369-1379`), so `readAllText` returns `""` for a one- or two-byte file (`:1418-1427`).
  - **Proved on the guest:** a ready file of `7\n` made the SCAN row say `NO GAMES TO SCAN YET`; with `7\n12\n`, `2 GAMES READY FOR OFFLINE PLAY`.
  - **The fix:** `file.clear()` before `seekg(0)`. It mends `readAllLines` too. It is the trap `es-code-traps.md` § A file under three bytes describes.
- **Can this be done on the VM?** Yes, on the host: `es-file-tests` cases for 0- to 3-byte files (the fixture `readall.cpp`), `fix-unit-test`. The guest frame is the walk's (`fix-walk-pending-image`).
- **Already written:** nothing inherited: the files are read afresh each time.
- **Acceptance:** `readAllText` returns the bytes of a 1-, 2- and 3-byte file, a BOM is still skipped, and `7\n` counts one game ready
- **Disposition note:** `bug` #1177, stream S8 (a #585 line), at the stage-D ruling (#667, 18:45 UTC)

## PL-10: `throw e;` slices the hasher's error to `std::exception`, which becomes the dialog's whole text (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-20; A-43, R-4, R-21; guest `g05`
- **Owner area:** es-app/src/RetroAchievements.cpp, es-app/src/ThreadedHasher.cpp
- **What:**
  - **The cause:** `throw e;` at `RetroAchievements.cpp:925` and `ThreadedHasher.cpp:117`, and `e.what()` shown at `ThreadedHasher.cpp:399` outside `_( )`.
  - **On the guest:** `Game Hash failed : std::exception` in the log.
  - **The fix:** `throw;` (or no rethrow), the cause logged, and a translated sentence on screen.
  - **Severity:** the seats disagree (Astra Low, Argon Medium for the screen); the lane keeps Low.
- **Can this be done on the VM?** Yes, on the host (`slice.cpp`) and the guest's startup run offline (`g05`).
- **Already written:** nothing inherited.
- **Acceptance:** the startup run offline logs the HTTP cause in its `Game Hash failed` line, and a non-silent run shows a translated sentence, not `std::exception`
- **Disposition note:** `bug` #1178, stream S9 (Low), at the stage-D ruling (#667, 18:45 UTC)

## PL-11: a tool's words reach the screen: the server's `Error`, curl's message on the account page, and `AN ERROR OCCURRED` before a sentence already in the player's words

- **Severity:** Low
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** L-03, L-32; A-4, A-26, R-4, R-25
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp, GuiRetroAchievements.cpp, GuiGameAchievements.cpp, es-app/src/RetroAchievements.cpp
- **What:**
  - **What reaches the screen:**
    - the server's JSON `Error` (`GuiRetroAchievementsSettings.cpp:784`, when refused);
    - curl's message through `getLoginErrorMessage` (`RetroAchievements.cpp:165`, `:737`; `GuiRetroAchievements.cpp:44`);
    - the game page's `AN ERROR OCCURRED` prefix on a sentence that already says what happened (`GuiGameAchievements.cpp:41-42`).
  - **What the first reader claimed and does not hold:** curl's message at `:784`.
  - **The fix shape:** categories in the player's words (`player-language.md`); detail to the log.
- **Can this be done on the VM?** Yes, on the guest: a refusing listener and the account page with the link cut (`fix-walk-pending-image`).
- **Already written:** nothing inherited.
- **Acceptance:** each failure surface shows a sentence from the fork's catalog, in French too, and no server or curl string
- **Disposition note:** `bug` #1178, stream S9, at the stage-D ruling (#667, 18:45 UTC)

## PL-12: the top-up's card adopts another run's progress and stamp; two why tokens have no row; `NO_GAMES_FOUND` is a dead row (a `bug` proposed for the adoption)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-08, PL-13's page half (T19); A-31, A-54, R-7, R-19
- **Owner area:** es-app/src/ProxyCards.cpp, es-app/src/CloudText.cpp (fork-own)
- **What:**
  - **The adoption:** `runTopUp` takes any `running` file as its own progress, and any stamp newer than its start as its own outcome. It checks neither `route` nor `topup` (`ProxyCards.cpp:274`, `:314-320`). So a top-up refused with 75 while a scan runs can show that scan's progress and then a COULDN'T FINISH.
  - **Liveness:** `topUpRunning()` treats the file as liveness (PL-13's page half).
  - **The rows:** `STAMP_UNWRITABLE` and `RESULT_UNREADABLE` (T19's S5 and S7) have no row; `NO_GAMES_FOUND` has no producer (`CloudText.cpp:1032-1033`).
  - **The fix shape:** match `route=topup` and `topup`; an explicit run identity; the two rows with French.
- **Can this be done on the VM?** Yes, on the host for the matching (`proxycards-tests`), `fix-unit-test`; the rows in `es-unit-tests`.
- **Already written:** nothing inherited.
- **Acceptance:** a scan's progress file and stamp are not taken as a top-up's; the two tokens have rows in English and French
- **Disposition note:** `bug` #1176, stream S7, at the stage-D ruling (#667, 18:45 UTC)

## PL-13: HARDCORE MODE can be turned on with offline achievements on, and `disable` restores a preference made obsolete since

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-14; A-19, A-37, R-14
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp; the ctl's `disable` (T19's)
- **What:**
  - **The contradiction:** `system.cfg` can hold `offlineproxy=1` with `hardcore=1`, against D-RA-001's casual-only feature (`GuiRetroAchievementsSettings.cpp:621`).
  - **The restore:** `disable` restores the record taken at `enable`, over any change made since (`raofflineproxy-ctl:529-540`).
  - **A question for the coordinator:** reconcile the two modes (gate the switch while the feature is on with its reason, or ask), or record as the player's right. Both seats call it a defect.
- **Can this be done on the VM?** Yes, on the guest (`fix-walk-pending-image`).
- **Already written:** devices may hold both on; a fix reads both keys, it does not rewrite them.
- **Acceptance:** per the ruling
- **Disposition note:** Ruled by D-RA-052: `bug` #1179, stream S10, at the stage-D ruling (#667, 18:45 UTC)

## PL-14: a sign-in that says `Success` with no `Token` counts as signed in; JSON members are used without type checks (a `bug` proposed)

- **Severity:** Low
- **Category:** Security
- **Question:** Q3
- **Source Finding:** L-28; A-52, R-23
- **Owner area:** es-app/src/RetroAchievements.cpp
- **What:**
  - **The cause:**
    - `testAccount` returns true with an empty token when `Success` is true and `Token` is absent (`RetroAchievements.cpp:1052-1056`), and the caller stores it (`GuiRetroAchievementsSettings.cpp:776-777`);
    - `Token`, `Error`, `Response` and `MD5List` are used without `IsString()` or `IsObject()` (`:879-880`, `:904-905`, `:1055`, `:1064`).
  - **Severity:** Low; more beside #1154's unverified peer.
- **Can this be done on the VM?** Yes, on the host if the parse moves into `CloudText`-style pure code (`fix-unit-test`), or on the guest with the probe listener answering such bodies.
- **Already written:** an empty token stored this way is retried by the watcher; nothing to migrate.
- **Acceptance:** a `Success` without a usable token is a failure; malformed members are refused without an assertion
- **Disposition note:** `bug` #1180, stream S11, at the stage-D ruling (#667, 18:45 UTC)

## PL-15: readers turn an incomplete answer into an empty one

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-27; A-51
- **Owner area:** es-app/src/OfflineAchievements.cpp
- **What:**
  - `storeSummary` returns `ok` after skipping every malformed line (`OfflineAchievements.cpp:252-263`).
  - A missing or unreadable ready file reads as 0 (`:152-165`).
  - An unreadable `pending-ids` reads as "none" (`:271-279`).
  - **The fix shape:** carry validity beside the data.
- **Can this be done on the VM?** Yes, on the host once the parse is pure.
- **Already written:** nothing inherited.
- **Acceptance:** an all-malformed summary is not `ok`; an unreadable pending list is not "none"
- **Disposition note:** `bug` #1174, stream S5, at the stage-D ruling (#667, 18:45 UTC)

## PL-16: a stopped hasher says INDEXING COMPLETED; an empty library says NO GAMES FIT THAT CRITERIA; a CANCEL that was not delivered leaves no way out

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-29, L-30; A-53, R-22, R-25
- **Owner area:** es-app/src/ThreadedHasher.cpp, es-app/src/OfflineScanJob.cpp
- **What:**
  - **INDEXING COMPLETED:** the toast at `ThreadedHasher.cpp:146` ignores `mExit`.
  - **NO GAMES FIT THAT CRITERIA:** an empty library without an exception (a captive portal's 200) makes `mTotal` 0, and a non-silent run says `NO GAMES FIT THAT CRITERIA.` over the offline card (`:383-390`).
  - **CANCEL:** `cancel()` marks the job cancelled before the signal, ignores its failure, and refuses a second CANCEL (`OfflineScanJob.cpp:65-80`).
- **Can this be done on the VM?** Yes, on the guest (`fix-walk-pending-image`); the cancel's state on the host.
- **Already written:** nothing inherited.
- **Acceptance:** a stopped run says it was stopped; an empty library says the library could not be read; a CANCEL that did not land can be pressed again
- **Disposition note:** `bug` #1172 (the cancel, S3) and #1178 (the words, S9), at the stage-D ruling (#667, 18:45 UTC)

## PL-17: starting a scan saves an edited username beside the previous account's token

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** L-31; R-24
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp
- **What:**
  - **The cause:** `offlineScanStart` saves `SystemConf` (`:321`) before the parent's save has cleared or replaced the token (`:743-807`). So the scan runs with the new name and the old token, until the parent page closes.
- **Can this be done on the VM?** Yes, on the guest (`fix-walk-pending-image`).
- **Already written:** a device may briefly hold the pair; the parent's close replaces the token.
- **Acceptance:** a scan started after an account change runs with no token from another account
- **Disposition note:** `bug` #1175, stream S6, at the stage-D ruling (#667, 18:45 UTC)

## PL-18: two small lifetimes: the LED switch's callback captures itself, and the toggle's thread posts through a raw `Window*`

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q7
- **Source Finding:** L-26; A-50, R-10
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp
- **What:**
  - **The LED switch:** its callback captures its own `shared_ptr` (`:688`), which leaks the component.
  - **The toggle's thread:** it posts through `window->postToUiThread` (`:484`), where the scan job uses `AppWindow::post`.
- **Can this be done on the VM?** On the host where the post is a unit; otherwise by reading.
- **Already written:** nothing inherited.
- **Acceptance:** the switch's callback holds it weakly; the toggle's thread posts through `AppWindow::post`
- **Disposition note:** `bug` #1173, stream S4, at the stage-D ruling (#667, 18:45 UTC)

## PL-19: the credential inventory: the username in the `User-Agent` and in the ctl's argv, and a stale comment

- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Source Finding:** L-04; A-1, A-27, A-49, R-1
- **Owner area:** es-app/src/RetroAchievements.cpp; the ctl (T19's)
- **What:**
  - **The `User-Agent`:** it carries the URL-encoded user when an API login exists, on the API's, the sign-in's and the library's requests (`RetroAchievements.cpp:178-185`). The comment at `:173` says otherwise.
  - **The ctl:** it passes the username as Python argv (`:616`, `:647`, `:788`).
  - **Recorded as written** unless the coordinator rules a change: the account name is not a secret, and the argv is root's own process.
- **Can this be done on the VM?** Yes (`ps` on the guest).
- **Already written:** nothing inherited.
- **Acceptance:** the comment says what the code does
- **Disposition note:** recorded as written; the comment at `:173` fixed in S6 (#1175), at the stage-D ruling (#667, 18:45 UTC)

## PL-20: the menu map's `:595` drift and the scan page's missing title

- **Severity:** Low
- **Category:** Documentation
- **Question:** Q2
- **Source Finding:** L-17; A-40, R-20
- **Owner area:** docs/es-menu-map.md
- **What:**
  - **The drift:** `docs/es-menu-map.md:595` names PL-07's drift, and `SCANNING GAMES FOR OFFLINE ACHIEVEMENTS` is absent from the map (R11: 0).
  - **The owner:** D-UI-039 puts the correction with the next change to these rows, or with an owner the coordinator names.
- **Can this be done on the VM?** Yes (`tools/es-menu-map-check`, a grep).
- **Already written:** nothing inherited.
- **Acceptance:** the map names the scan page and its rows as they ship
- **Disposition note:** stream S12 on the distribution branch (D-UI-039), at the stage-D ruling (#667, 18:45 UTC)

## PL-21: four #585 lines owed for the library's imported edits

- **Severity:** Info
- **Category:** Upstream
- **Question:** Q4
- **Source Finding:** L-24; A-47, R-15, R-21
- **Owner area:** external/libcheevos (rcheevos, libretro-common)
- **What:**
  - **Three rcheevos lines** (`hash_disc.c`): the read checks, the 64-bit header sum, the double close.
  - **One libretro-common line** (`md5.c`): the `memcpy` word load.
  - Whether rcheevos 12.5.0 carries them is `CANNOT` without a tarball. Written in `02` § The library.
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:** the four lines on #585
- **Disposition note:** Deferred: #585 (the four lines in `02`, posted by the coordinator with S8's), at the stage-D ruling (#667, 18:45 UTC)

## PL-22: the harness: no RVZ fixture independent of the readers, no baseline for the one walk, and an identity check that proves only "contains"

- **Severity:** Low
- **Category:** Harness
- **Question:** Q7
- **Source Finding:** Q7, Q8; L-25; the friction log's 17:45 UTC line
- **Owner area:** tools/vm-walks, docs/qa-logs/2026-10-13-rvz-source, generic-x64-vm-testing.md
- **What:**
  - **RVZ:** `make-fixtures.py` writes padding with the readers' own constants, so the three hashers agree by construction. A fixture from Dolphin's generator is the independent one (`bugs-are-agent-first.md` rule 3).
  - **The walk:** `m7-retro-achievements.steps` has no baseline, claim or mask (R12), so `frame-diff` sees no change to these pages (#1144's family).
  - **The identity check:** a window's identity step names one literal the pin added and one it lacks, so a composition over the pin is seen at step 1.
  - **`ra-ui-test`** fails closed on a lane's leftover state, which is right. Its guide could say which states to clear first.
- **Can this be done on the VM?** Yes, all on the VM.
- **Already written:** nothing inherited.
- **Acceptance:** the Backlog issues the coordinator files
- **Disposition note:** Deferred: Backlogs #1168 and #1169 (under #903), at the stage-D ruling (#667, 18:45 UTC)

## PL-23: dead ends: a reader row with no producer, two uncalled methods, a comment naming a function as a verb

- **Severity:** Low
- **Category:** Dead code
- **Question:** Q6
- **Source Finding:** L-08, L-22; Q6
- **Owner area:** es-app/src/CloudText.cpp, ThreadedHasher.{h,cpp}, GuiRetroAchievementsSettings.cpp
- **What:**
  - `NO_GAMES_FOUND` (`CloudText.cpp:1032-1033`).
  - `pause()`/`resume()` (`ThreadedHasher.h`).
  - `GuiRetroAchievementsSettings.cpp:154`'s `have_account`, which names a ctl function as if it were a verb.
  - **Proposals only;** nothing is removed here.
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:** per the ruling
- **Disposition note:** recorded as written (D-WORKFLOW-209); the `:154` comment fixed in S4 (#1173), at the stage-D ruling (#667, 18:45 UTC)

## PL-24: a runtime msgid from a sound's file name

- **Severity:** Info
- **Category:** Standards
- **Question:** none
- **Source Finding:** L-18; A-41, R-20
- **Owner area:** es-app/src/guis/GuiRetroAchievementsSettings.cpp
- **What:**
  - `_(Utils::String::toUpper(snd).c_str())` (`:671`) cannot be extracted; a file name need not be translated.
  - **Recorded as written.**
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:** none
- **Disposition note:** recorded as written, at the stage-D ruling (#667, 18:45 UTC)

## PL-25: notes for T21, T26 and T19

- **Severity:** Info
- **Category:** Handoff
- **Question:** none
- **Source Finding:** 02 § What T21 and T26 inherit; the guest's M7 observation
- **Owner area:** —
- **What:**
  - **T21:** `ApiSystem`'s readers (PL-08's function) and `HttpReq`'s options.
  - **T26:** the gates and the title's source.
  - **T19 / M7:** the installed ctl's `disable` exited 75 twice with its lock naming a dead pid (`guest-cycle/g08-ra-ui-pre.txt`).
- **Can this be done on the VM?** n/a.
- **Already written:** nothing inherited.
- **Acceptance:** the notes on #673 and the M7 issue the coordinator names
- **Disposition note:** routed: PL-08 and the `HttpReqOptions` field to T21 (#668); the gates and the title's source to T26 (#673); the M7 observation on #1111, at the stage-D ruling (#667, 18:45 UTC)

## Phase 7 resolution gate

Every item is open until the coordinator's stage-D ruling and stage F.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Resolved | Resolved in `698040b5c` (ES, S1) under #1170: one owner for the hasher's lifetime; `hasher-tests` heap-use-after-free before, 3 of 3 clean after (`stage-e/s1-*.txt`); the startup walk owed (`stage-e/walks/s1-startup-lookups.steps`) |
| PL-02 | Resolved | Resolved in `d3137f992` (ES, S2) under #1171: the credential in a POST body as the vendored client sends it, and `httpsRedirectsOnly` for it; the unit FAIL before, PASS after (`stage-e/s2-*.txt`); the listener walk owed; the transport's verification stays #1154's |
| PL-03 | Resolved | Resolved in `ad2989aa5` (ES, S3) under #1172: the pid taken once and above 1, a later line ignored and logged; `jobs-tests` FAIL before, PASS after (`stage-e/s3-*.txt`); the CR-named ROM's walk owed |
| PL-04 | Resolved | Resolved in `f85061f14` (ES, S4) under #1173: the page reads the toggle back from the ctl's status after any exit; the LED callback weak; `AppWindow::post` (`stage-e/s4-*.txt`); the stub-ctl walk owed |
| PL-05 | Resolved | Resolved in `274a71add` (ES, S5) under #1174: unknown kept unknown at both readers and the card; the three readers carry validity (`stage-e/s5-*.txt`) |
| PL-06 | Resolved | Resolved in `2d8a0a135` (ES, S6) under #1175: the sign-in off the interface thread with a 15 s total and a 10 s stall, its answer tied to the account; a scan never carries another account's token (`stage-e/s6-*.txt`); the stalling-listener walk owed |
| PL-07 | Deferred | Deferred: #300, as ruled at the stage-D ruling (#667, 18:45 UTC) |
| PL-08 | Deferred | Deferred: #668 (T21), with `stage-b/positives/reader.cpp`, as ruled at the stage-D ruling (#667, 18:45 UTC) |
| PL-09 | Resolved | Resolved in `d9afa5c7c` (ES, S8) under #1177: `file.clear()` before `seekg(0)`; `es-file-tests` FAIL before, PASS after (`stage-e/s8-*.txt`); the row's walk owed; the #585 line in `02` |
| PL-10 | Resolved | Resolved in `61d7152b0` (ES, S9) under #1178 (and PL-16's cancel in `ad2989aa5`, S3, #1172): `throw;`, the player's words on every failure surface with French, a stopped run and an empty library said as they are (`stage-e/s9-*.txt`); the frames owed |
| PL-11 | Resolved | Resolved in `61d7152b0` (ES, S9) under #1178 (and PL-16's cancel in `ad2989aa5`, S3, #1172): `throw;`, the player's words on every failure surface with French, a stopped run and an empty library said as they are (`stage-e/s9-*.txt`); the frames owed |
| PL-12 | Resolved | Resolved in `d7a30f0c6` (ES, S7) under #1176: the card takes only its own run, `topUpRunning()` from the run, the two rows with French (`stage-e/s7-*.txt`); `NO_GAMES_FOUND` recorded |
| PL-13 | Resolved | Resolved in `2b521c34b` (ES, S10) under #1179, as D-RA-052 rules: HARDCORE MODE dimmed with its reason and not writable while offline achievements are on (`stage-e/s10-*.txt`); the frame owed |
| PL-14 | Open | its stream (the ruling at the stage-D ruling (#667, 18:45 UTC)) |
| PL-15 | Resolved | Resolved in `274a71add` (ES, S5) under #1174: unknown kept unknown at both readers and the card; the three readers carry validity (`stage-e/s5-*.txt`) |
| PL-16 | Resolved | Resolved in `61d7152b0` (ES, S9) under #1178 (and PL-16's cancel in `ad2989aa5`, S3, #1172): `throw;`, the player's words on every failure surface with French, a stopped run and an empty library said as they are (`stage-e/s9-*.txt`); the frames owed |
| PL-17 | Resolved | Resolved in `2d8a0a135` (ES, S6) under #1175: the sign-in off the interface thread with a 15 s total and a 10 s stall, its answer tied to the account; a scan never carries another account's token (`stage-e/s6-*.txt`); the stalling-listener walk owed |
| PL-18 | Resolved | Resolved in `f85061f14` (ES, S4) under #1173: the page reads the toggle back from the ctl's status after any exit; the LED callback weak; `AppWindow::post` (`stage-e/s4-*.txt`); the stub-ctl walk owed |
| PL-19 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#667, 18:45 UTC); the `:173` comment fixed in `2d8a0a135` (ES, S6, #1175) |
| PL-20 | Open | its stream (the ruling at the stage-D ruling (#667, 18:45 UTC)) |
| PL-21 | Deferred | Deferred: #585, the four lines in `02` § The library, as ruled at the stage-D ruling (#667, 18:45 UTC) |
| PL-22 | Deferred | Deferred: Backlogs #1168 and #1169 (under #903), filed at the stage-D ruling (#667, 18:45 UTC) |
| PL-23 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#667, 18:45 UTC; D-WORKFLOW-209); the `:154` comment fixed in `f85061f14` (ES, S4, #1173) |
| PL-24 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#667, 18:45 UTC) |
| PL-25 | Deferred | Deferred: routed to #668 (T21), #673 (T26) and #1111 (M7), as ruled at the stage-D ruling (#667, 18:45 UTC) |

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q3
  source_finding: "L-21, L-22, L-26 (threads)"
  outcome: "resolved"
- id: PL-02
  severity: "Medium"
  category: Security
  question: Q3
  source_finding: "L-01"
  outcome: "resolved"
- id: PL-03
  severity: "Medium"
  category: Security
  question: Q3
  source_finding: "L-10"
  outcome: "resolved"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "L-09"
  outcome: "resolved"
- id: PL-05
  severity: "Medium"
  category: Correctness
  question: Q3
  source_finding: "L-07"
  outcome: "resolved"
- id: PL-06
  severity: "Medium"
  category: Performance
  question: Q3
  source_finding: "L-02"
  outcome: "resolved"
- id: PL-07
  severity: "Medium"
  category: Performance
  question: Q5
  source_finding: "L-19"
  outcome: "deferred"
- id: PL-08
  severity: "Low"
  category: Correctness
  question: Q1
  source_finding: "L-05, L-06"
  outcome: "deferred"
- id: PL-09
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-13"
  outcome: "resolved"
- id: PL-10
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-20"
  outcome: "resolved"
- id: PL-11
  severity: "Low"
  category: Standards
  question: Q2
  source_finding: "L-03, L-32"
  outcome: "resolved"
- id: PL-12
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-08, PL-13's page half (T19)"
  outcome: "resolved"
- id: PL-13
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-14"
  outcome: "resolved"
- id: PL-14
  severity: "Low"
  category: Security
  question: Q3
  source_finding: "L-28"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-27"
  outcome: "resolved"
- id: PL-16
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-29, L-30"
  outcome: "resolved"
- id: PL-17
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "L-31"
  outcome: "resolved"
- id: PL-18
  severity: "Low"
  category: Correctness
  question: Q7
  source_finding: "L-26"
  outcome: "resolved"
- id: PL-19
  severity: "Low"
  category: Security
  question: Q2
  source_finding: "L-04"
  outcome: "withdrawn"
- id: PL-20
  severity: "Low"
  category: Documentation
  question: Q2
  source_finding: "L-17"
  outcome: "open"
- id: PL-21
  severity: "Info"
  category: Upstream
  question: Q4
  source_finding: "L-24"
  outcome: "deferred"
- id: PL-22
  severity: "Low"
  category: Harness
  question: Q7
  source_finding: "Q7, Q8"
  outcome: "deferred"
- id: PL-23
  severity: "Low"
  category: Dead code
  question: Q6
  source_finding: "L-08, L-22"
  outcome: "withdrawn"
- id: PL-24
  severity: "Info"
  category: Standards
  question: none
  question_reason: "an extraction note or a handoff, not a renovation question"
  source_finding: "L-18"
  outcome: "withdrawn"
- id: PL-25
  severity: "Info"
  category: Handoff
  question: none
  question_reason: "an extraction note or a handoff, not a renovation question"
  source_finding: "02 § What T21 and T26 inherit"
  outcome: "deferred"
```
