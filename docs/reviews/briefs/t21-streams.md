# Stream brief: M6.P2 T21, stage E (#668)

**The coordinator's, 2026-10-27, at T21's stage-D pause** (the lane's post of 00:23 UTC; #1184 the audit; the punch list `05` written under D-WORKFLOW-212 from the lane's inputs). Fourteen streams, serial, on the EmulationStation branch `feature/m6-es-state-and-bridge-668` in `/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668`, which leaves the pin `16dbac5211` for the first time here. The distribution worktree takes only the audit folder's records and the day's log. The dispositions that are not streams are in the ruling on #668; this file is only what changes code.

## The rules every stream keeps

- **Test first, then the fix, and the test's FAIL is recorded before the fix lands** (`engineering-practices.md` § Guards must fail closed). The positive is the item's own: a `stage-b/` or `stage-c/` fixture, a new doctest case in `es-app/tests/unit/` or `tests/app-unit/`, or a lifted file under ASan. Its output on the pin's code goes into `stage-e/sN-before.txt`, its output after into `stage-e/sN-after.txt`, the full checks into `stage-e/sN-checks.txt`.
- **D-WORKFLOW-210:** a suite that asserts the defect changes in the stream's commit -- exactly the checks the ruling reverses, each a recorded positive. **D-WORKFLOW-211:** a fixture that relied on the defect is completed in the stream's commit, no assertion changed.
- **The host builds the unit tests** with `tools/t21-build-tests.sh` (the recipe's own rapidjson, as stage A); `tools/es-syntax-check` exits 2 on this host, so a page source is `CANNOT` with that word and the compiler's check is the generated build where a test target compiles the source. A `.cpp` a stream edits that no test compiles is read twice and said so.
- **Every new player sentence ships in English and French in the same commit** (D-UI-051: the msgid byte for byte in `locale/lang/fr/LC_MESSAGES/emulationstation2.po`, the file's own style); `tools/es-untranslated --upstream bccd715707` names it in neither list. The words are the brief's proposed ones, built as proposed (D-UI-112); the maintainer changes a word later.
- **Non-ASCII comments:** the check runs over the lines the stream added (`git diff -U0 HEAD -- <file>`, its `+` lines, `grep -nP '[^\x00-\x7F]'`), never over upstream's lines (`es-code-traps.md`).
- **One commit per stream** on the ES branch, `Refs #668, #<the item's bug>` (the lane files the bug first; no closing keyword), the files named in the message; `.githooks/pre-push-test` before each push; `tools/register-check` on the distribution side before each record commit. A source a stream changes cites its bug number in a comment, never a register row.
- **`Already written:`** answered in the bug and in `02` § The streams (`upgrade-and-install.md`, D-WORKFLOW-050): the ladder's fixes read both shapes, the modes are narrowed once at start, nothing is migrated by a prompt.
- **Nothing changes under the distribution's `packages/`, `projects/` or `tools/`**, and nothing in T1's files (`001-functions`, `wifictl`, `chksysconfig`): those halves are bugs under the OS-scripts epic #695 for the integration's fix round (the ruling). The pin bump into the distribution is the coordinator's at integration.
- **No guest, no build, no fetch, no keyed council call, nothing on a unit.** The host is M7's on request; these streams are edits, host builds and host fixtures. `rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short command.
- **A question for the coordinator is posted on #668**, never only on the session's screen (Backlog #1183). If the harness refuses a stream's content, post the stream's number and stop that stream; the coordinator takes it (D-WORKFLOW-212).

## S1 -- PL-01, PL-10, PL-11: `SystemConf`'s write and read of a key (High)

Files: `es-core/src/SystemConf.cpp` (`applyChanges`, `set`, `loadSystemConf`, `recordLastGood`'s guard), `es-core/src/utils/AtomicFileUtil.cpp` (`parseKeyValues`), `es-core/src/guis/GuiSettings.cpp` (`addInputTextConfigRow`'s `updateVal`). The HOSTNAME row itself (`GuiMenu.cpp:9929`) is T26's: the row's empty value is refused where `updateVal` receives it, so every text row gets the guard.

1. **Positives, before:** `stage-c/positives/hostname-empty.py` on the pin (step 3 `value=[]`, both files to 221 keys); `stage-b/positives/state-units` U1 (`BATOCERA`), U2 (a second key), U3 (the default written); new `SystemConfTests` cases written first and FAILing: `set("system.hostname", "")` then save keeps `system.hostname=` in the live file and the record; a reload after `wifi.key=` leaves `get("wifi.key")` empty; `#k=1`/`k=2` saved with `k=3` holds one `k=` line and the comment; `set("new", "default")` writes no literal.
2. **The fix:** `applyChanges` keeps a key set to an empty value as `key=` (a removal is `default`, never a literal, never an empty string); the default comparison on the key, not `key=`; a comment line left alone; the BOM stripped at the parse; `parseKeyValues` keeps an empty value as present-and-empty, distinct from absent, and the hostname reader shows the device's own name for it; `loadSystemConf` clears the map before the parse; `set` refuses a value with a line end. The recorder publishes nothing while a save removed a key the record holds without an explicit `default` (the guard S2 completes).
3. **Positives, after:** the fixture passes (both files keep the line; `chksysconfig verify` reseeds nothing; the next start reads the player's keys); U1 to U3 and the new cases PASS; `AtomicFileTests` and `SystemConfTests` whole in the generated build's summary line.
4. **`Already written:`** PL-01's and PL-10's lines as `05` gives them (the total loss is total; `system.hostname=` on D-NET-009's devices reads as the device's name; revived `k=` lines and literal `default`s are read as today and not written again).
5. **Commit:** `es-core: SystemConf keeps a key written empty, parses an empty value as present, and clears the map on reload (Refs #668, #<PL-01's bug>, #<PL-10's bug>, #<PL-11's bug>)`.

## S2 -- PL-09 and PL-03's recorder half: the ladder and the recorder (High)

Files: `es-core/src/utils/AtomicFileUtil.cpp` (`chooseConfig`, `saveUnderLock`, `recordLastGood`), `es-core/src/SystemConf.cpp:232-238`.

1. **Positives, before:** new `SystemConfTests` cases FAILing on the pin: (a) the record, a cut copy of it touched newer, a `set` and a save, a reload -- the record's keys present; (b) a live file byte-identical to the shipped seed beside a record with other keys -- the record chosen and nothing recorded over it (S1 of `stage-b/positives/shell-writers` is the shell side's picture).
2. **The fix:** a live file whose text is a strict prefix of its record's is a recovery whatever its mtime; a save onto a live file whose key set is a strict subset of the record's re-chooses under the lock before it records; the recorder refuses to publish as the record a live file equal to the seed while a differing record exists.
3. **Positives, after:** (a) and (b) PASS; the kill sweep (`kill-writer.py`) still leaves old or new whole at every point.
4. **`Already written:`** PL-09's and PL-03's lines.
5. **Commit:** `es-core: the recovery ladder treats a cut live file as a recovery whatever its mtime, and the recorder never publishes the seed over a record (Refs #668, #<PL-09's bug>, #<PL-03's bug>)`.

## S3 -- PL-02 and PL-17's hash halves: the scraper's shell commands (High)

Files: `es-app/src/ApiSystem.cpp` `getMD5` (`:1527-1530`), `getCRC32` (`:1578-1586`), `unzipFile` (`:1659-1660`), `getPdfPageCount` (`:2509`), `extractPdfImages` (`:2593`).

1. **Positives, before:** a unit over the command builder as a pure function (the builder extracted to `CloudText`'s shape or beside it, `CommandLineTests`' file): a name carrying `"`, `$`, a backtick and `\` must reach the child as one argument byte for byte, and the pin's double-quoted string form is shown to split it; a unit: `getMD5` over an archive `7zr` cannot read stores no MD5 (the pin stores the digest of empty input); a unit: `getCRC32` over an empty entry returns no CRC. All FAIL on the pin.
2. **The fix:** every path reaches `7zr` and poppler through `Utils::String::shellQuote` (`StringUtil.cpp:426-444`) -- single quotes, the pipeline kept -- at the five lines; never double quotes; the exit of the pipeline checked (`executeEnumerationScript` returns it after S10; until then the empty output is the check); an empty extraction stores no hash; `getCRC32`'s empty entry and its `size_t` subtraction guarded. The argv executor (`posix_spawnp`, `GuiWifi.cpp:535-582`'s shape) is the better home and is a Backlog under #700, not this stream.
3. **Positives, after:** the units PASS; `tools/t21-commands.py` reports the double-quotes count down by the five live rows, its `--expect` asserted.
4. **`Already written:`** PL-02's line (the empty input's digest on a non-empty archive is treated as unhashed and hashed again).
5. **Commit:** `es-app: the scraper's 7zr and poppler commands quote the file's path and store no hash from a failed extraction (Refs #668, #<PL-02's bug>, #<PL-17's bug>)`; a #585 line in `02` (the lines are upstream's).

## S4 -- PL-04: the file-mode download and `renameFile` (Medium)

Files: `es-core/src/HttpReq.cpp` (`:324-345`, `:361-368`, `:377-378`, `:477-506`), `es-core/src/utils/FileSystemUtil.cpp` `renameFile` (`:1448-1463`).

1. **Positives, before:** a unit over the file-mode path with a transfer that fails after the open: the old file must be byte-identical after the call and `status()` not `REQ_SUCCESS` (the pin: the file is gone); a unit: `renameFile` of an absent source returns false (the pin: true).
2. **The fix:** the bytes to a unique temporary (`<path>.tmp.<pid>.<n>`, the atomic writer's shape), `fflush` and `fclose` checked, the artifact positive before the rename, the old file replaced only then; `renameFile` false for an absent source and no removal of the destination before `std::rename`.
3. **Positives, after:** both units PASS.
4. **`Already written:`** PL-04's line.
5. **Commit:** `es-core: a download replaces its target only after the whole artifact arrived, and renameFile fails on an absent source (Refs #668, #<PL-04's bug>)`; a #585 line.

## S5 -- PL-05 and PL-12's modes: the stores' modes (Medium)

Files: `es-core/src/utils/AtomicFileUtil.cpp` (`writeText`'s mode, `:115`, `:127-147`), `es-core/src/SystemConf.cpp`, `es-core/src/Settings.cpp` (`:533`, `:617`, `:629-631`). The seed's build step under `projects/` is the coordinator's and is named on #1184.

1. **Positives, before:** `AtomicFileTests` cases FAILing on the pin: `writeText` replacing a 0645 file with mode 0600 requested leaves 0600; a start-time narrowing over a 0645 live file and a 0644 record leaves both 0600; the recovery copy and the recording take the requested mode, not each other's.
2. **The fix:** both stores and both records written with an explicit 0600; the existing files narrowed once at the interface's start (idempotent); the crossed modes of `Settings`' ladder set from the same constant.
3. **Positives, after:** the cases PASS; `tools/settings-modes-test` PASS for the shell side (unchanged by this stream, read as the contract).
4. **`Already written:`** PL-05's line (every upgraded device: migrated by the start-time narrowing).
5. **Commit:** `es-core: the settings stores and their records are written 0600 and narrowed once at start (Refs #668, #<PL-05's bug>)`.

## S6 -- PL-06's page half: the Wi-Fi page says CONNECTED only when it is (Medium)

Files: `es-app/src/guis/GuiWifi.cpp` (`:385-395`, `:403-413`, `:548-569`), `es-app/src/ApiSystem.cpp` `enableWifi` (`:627-637`). `wifictl`'s device guard is T1's file (a bug under #695).

1. **Positives, before:** a unit over the page's decision as a pure function (the connect's exit and `wifictl current`'s answer in, the outcome out): exit 0 with no current network must not read as joined (the pin reads `system() == 0` as joined). `tests/wifi-profile-lifetime.py` PASS at the pin stays PASS.
2. **The fix:** after a connect the page asks `wifictl current` and says CONNECTED and saves `wifi.ssid`/`wifi.key` only on a current network; a no-device or no-network answer shows its own sentence -- **`WI-FI ISN'T AVAILABLE ON THIS DEVICE RIGHT NOW.`** (proposed, D-UI-112) with its French -- and saves nothing.
3. **Positives, after:** the unit PASSes; `es-untranslated` names the sentence in neither list.
4. **`Already written:`** PL-06's line.
5. **Commit:** `es-app: the Wi-Fi page says CONNECTED only on a current network and saves nothing otherwise (Refs #668, #<PL-06's bug>)`.

## S7 -- PL-07, PL-08, PL-19: `HttpReq`'s bounds (Medium)

Files: `es-core/src/HttpReq.cpp` (`:579-594`; `:432-433`; `:395`, `:416-521`, `:640-643`, `:439-473`, `:562`, `:174-179`).

1. **Positives, before:** `stage-b/positives/lifted` header under ASan (heap-buffer-overflow on the pin's lines); the status lines lifted with a stub `curl_easy_getinfo` writing 8 bytes, under ASan (stack-buffer-overflow on the pin's lines); ASan's leak check over a request with a custom header (the pin leaks the list); a unit over the log line's shape (a 10 kB body reaches the log as at most one bounded, masked line).
2. **The fix:** `std::string(buffer, size * nitems)`; a `long` for the response code, narrowed where used; `mStatus` atomic or read under `mMutex` at every read; the error body bounded and passed through `maskSecrets` (or at LogDebug); `curl_slist_free_all` in the destructor.
3. **Positives, after:** both ASan runs clean; the leak report empty; the unit PASSes; a 200, a 404 and a 503 still reach their rows of `status()`'s table.
4. **`Already written:`** nothing inherited (memory and tmpfs).
5. **Commit:** `es-core: HttpReq reads curl's header by its length, stores the response code as a long, bounds and masks the error body, and frees its header list (Refs #668, #<PL-07's bug>, #<PL-08's bug>, #<PL-19's bug>)`; #585 lines for the four.

## S8 -- PL-12: `Settings`' record (Low)

Files: `es-core/src/Settings.cpp`, `es-core/src/Settings.h`; new `es-app/tests/unit/SettingsTests.cpp` (pugixml from the recipe's build, as the generated line already links `SystemConfTests`).

1. **Positives, before:** `SettingsTests.cpp` written first with the ladder's cases: an empty, a cut and a non-`<config>` live file each recover from the record (the non-`<config>` one FAILs on the pin: any XML parses); a record write that fails keeps the flag dirty and the next save retries (FAILs on the pin).
2. **The fix:** a mutex on the maps and the `PidLock` shape around `saveFile` (D-CLOUD-079, refined by the coordinator's row); a failed record kept dirty; the parse requires `<config>`; the modes from S5.
3. **Positives, after:** `SettingsTests` PASS in the generated build's summary line; a save from a worker thread during a `getString` on the interface thread clean under ThreadSanitizer in the host build.
4. **`Already written:`** PL-12's line.
5. **Commit:** `es-core: Settings takes the stores' lock, retries a failed record, and parses only a config document (Refs #668, #<PL-12's bug>)`.

## S9 -- PL-13: the sweeps (Low)

Files: `es-core/src/utils/AtomicFileUtil.cpp` (`:50-64`, `:115`), `es-core/src/Settings.cpp:557-558`, `es-core/src/SystemConf.cpp:203-210`.

1. **Positives, before:** `kill-writer.py` with a sweep assertion after a simulated next start (the pin: 42 of 99 points leave a temporary); a unit: the start with a `system.cfg.backup.tmp` present leaves it (the pin removes it).
2. **The fix:** each store sweeps `<path>.tmp.*` whose pid is dead, at start and after every save; the start's sweep leaves `chksysconfig`'s name alone.
3. **Positives, after:** 0 temporaries left after the start's sweep; the unit PASSes. The upgrade rehearsal's seed is a Backlog under #903 (the coordinator's).
4. **`Already written:`** PL-13's line (migrated: the start's sweep removes every dead-pid temporary of both stores once).
5. **Commit:** `es-core: the stores sweep their own dead-pid temporaries and leave chksysconfig's backup temporary alone (Refs #668, #<PL-13's bug>)`.

## S10 -- PL-14: the executors (Low)

Files: `es-app/src/ApiSystem.cpp` `executeEnumerationScript` (`:2251`), `executeScriptLegacy` (`:2278-2291`), `executeScript`, the eleven `WEXITSTATUS` sites, `:593`.

1. **Positives, before:** `lifted enum` and `lifted script` (the pin returns the lines as success; a killed child reads 0); T20's `reader.cpp` at distribution `ffb6b686cb` (`stage-b/positives/reader.cpp` on T20's branch, read by `git show`): a 1,500-byte record is cut, a last line without a newline dropped, a signalled child read as success.
2. **The fix:** one bounded logical-line reader for the four executors (a unit of its own); the exit returned and checked, `WIFEXITED` then `WEXITSTATUS`, a signal a failure; an oversized record refused rather than cut, the last line kept; `executeEnumerationScript` returns the exit beside the lines and `getBiosInformations` says the check could not run; `cloud_oauth close`'s non-zero exit logged. The Windows shims at `:45-46` recorded, not changed.
3. **Positives, after:** the three lifted cases and the reader's three PASS.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the script executors read bounded logical lines and return a checked exit, a signal a failure (Refs #668, #<PL-14's bug>)`.

## S11 -- PL-15: the LED colour parse (Low)

Files: `es-app/src/ApiSystem.cpp` `getLEDColours` (`:1868-1890`), `setLEDBrightness` (`:2083-2087`); the parser as pure code with a doctest case (`es-code-traps.md` § Pure text has a home).

1. **Positives, before:** `lifted led` (the pin throws on `blue`, reads `255,0,165` as white); the pure parser's case written first.
2. **The fix:** a parse that returns the default on anything but three numbers in range; `stoul`'s shape the same.
3. **Positives, after:** `blue` returns the default without throwing; `255,0,165` returns 255 0 165 or the default; the case PASSes.
4. **`Already written:`** PL-15's line (a word already in `system.cfg` reads as the default and the page opens).
5. **Commit:** `es-app: the LED colour and brightness settings parse to a default instead of throwing (Refs #668, #<PL-15's bug>)`.

## S12 -- PL-18 and the certificate sentence: the ladder's three outcomes and the client's status classes (Low)

Files: `es-core/src/SystemConf.cpp:221-265`, `es-core/src/Settings.cpp:615-619`, `es-app/src/main.cpp:1041-1042`, `es-core/src/HttpReq.cpp:462-469`, `es-app/src/scrapers/ScreenScraper.cpp:989-990`; the mapping as pure code with cases.

1. **Positives, before:** a unit over the ladder's outcome words (restored and written back; restored in memory with the write-back owed; the file was missing) -- the pin says RESTORED for all three; a unit over the client's status classes: 501 to 504, redirects exhausted and a certificate failure each their own class (the pin: `YOU'RE NOT ONLINE`).
2. **The fix, the sentences proposed (D-UI-112), each with its French:** the ladder -- `YOUR SETTINGS FILE WAS DAMAGED. THE LAST GOOD COPY WAS RESTORED.` (kept, for the written-back case), **`YOUR SETTINGS FILE WAS DAMAGED. THE LAST GOOD COPY IS IN USE AND WILL BE SAVED NEXT TIME.`**, **`YOUR SETTINGS FILE WAS MISSING. THE LAST GOOD COPY WAS RESTORED.`**; the client -- **`THE SCRAPER'S SERVER ISN'T ANSWERING RIGHT NOW.`** for 501 to 504 and exhausted redirects, **`THE SCRAPER'S SERVER COULDN'T BE VERIFIED.`** for a certificate failure (S14 makes it reachable). `YOU'RE NOT ONLINE` stays for a connection that never opened.
3. **Positives, after:** the units PASS; `es-untranslated` names none of the four in either list.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-core, es-app: the recovery ladder and the scraper's client say what happened in three and four outcomes (Refs #668, #<PL-18's bug>)`.

## S13 -- PL-17's scraper halves: the scraper's readers (Low)

Files: `es-app/src/scrapers/ScreenScraper.cpp` `getThreadCount` (`:1075-1089`), `es-app/src/scrapers/Scraper.cpp:618-623` (a contained fix in T32's file, `bugs-are-agent-first.md` rule 6).

1. **Positives, before:** units FAILing on the pin: a non-XML user-info body yields a failure, not a thread count of 1; `Retry-After: <HTTP-date>` waits until that date or the default, never 0.
2. **The fix:** validity beside the data: an unparsable answer is a failure with its sentence (S12's class); the HTTP-date parsed with `curl_getdate` or the default wait.
3. **Positives, after:** the units PASS.
4. **`Already written:`** nothing inherited.
5. **Commit:** `es-app: the scraper reads an unparsable account answer as a failure and a Retry-After date as a date (Refs #668, #<PL-17's bug>)`.

## S14 -- #1154 and PL-25: verify the peer (the ruling's D-NET-017)

Files: `es-core/src/HttpReq.cpp` (`:192`, `:200`; the 429 retry's rebuild), `es-app/src/scrapers/Scraper.cpp:596`; the `HttpReqOptions` field beside T20's `httpsRedirectsOnly` (read by `git show` at ES `5c0ddaaee`, not merged).

1. **Positives, before:** a unit over the options' defaults (verification on unless the field is set; the 429 retry carries the options); the self-signed listener on the host (T20's `tls-probe.py` shape, a dummy account): on the pin the client accepts the self-signed peer; after the fix it refuses with the certificate class.
2. **The fix:** `CURLOPT_SSL_VERIFYPEER` and `VERIFYHOST` on by default with the image's bundle (`/etc/ssl/certs/ca-certificates.crt`, present on the image, `g01-identity.txt`); one `HttpReqOptions` field, `allowUnverifiedPeer`, that only the scrapers' media downloads set, and that the 429 retry preserves; a certificate failure maps to S12's class. The client-certificate path keeps verification on.
3. **Positives, after:** the units PASS; the listener refused.
4. **`Already written:`** PL-25's line (credentials already sent cannot be recalled; nothing to migrate).
5. **Commit:** `es-core: HttpReq verifies the peer by default and lets only media downloads opt out, through the retry (Refs #668, #1154)`.

## The record

- `02` § The streams: one row per stream with the positive before, the commit, the positive after, the `Already written:` answer and `proved: fix-unit-test` (the guest walks `fix-walk-pending-image`, the coordinator's at the integration window); `05`'s items point at it and the gate table and the `punch_index` move together at Phase 7.
- `00`: the stage-E entry naming the generated build's command file and each fixture's command.
- The hand-back after stage E's record, as the brief's § 10: both tips, the artifacts by path, `reviewed-at:`, `reviewed-at-es:`, `fixed-at:` and `fixed-at-es:` in #668's body; the bugs' `fixed-at-es` filled; the ES `pre-push-test` at the tip.

## What never runs here

A build, a compiler beyond the host's `g++` for the unit targets, a guest, a fetch, a keyed council call, anything on a unit, a change outside the ES branch and the audit folder, a change to any of T1's files or to upstream copies of a line.
