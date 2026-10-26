# Punch list — M6.P2 T19, the offline achievements proxy (#666)

**Extended depth** (two seats: GPT-6 Astra at `max`, then Gemini 4 Argon at `high`; `04` § Second opinion). The audit issue is opened at stage D as a sub-issue of #666, after the coordinator's dispositions.

- **Nine `bug`s filed at the stage-D ruling (#666, 13:48 UTC), all Low**: #1157 to #1165 (PL-01 to PL-09; PL-04 with PL-21, PL-06 with PL-23, PL-08 with PL-16's classifier); the streams are `docs/reviews/briefs/t19-streams.md` at `6064579a3f`; the audit issue is #1156. Originally 8 proposed (PL-01 to PL-08), each with its trace, `Already written:` line and VM line; the rest Info. Nothing is Medium or above.
- **Nothing** in this list changes a file under `packages/`, `projects/` or `tools/` at stages A to D; a fix lands only under a stream brief at the stage-D pause. Removals: none.
- **One guest window**, 12:43:49 to 12:53:37 UTC, two boots; the image's scripts are M7's, so the tree's four ran from `/storage/t19/bin/` (`02` § The guest cycle, labelled as ruled). **Nothing ran on a person's device or account.**
- **Found at stage E:** F-42, PL-24, #1166 (Low), in S5's function, ruled into S5 (#666, 15:15 UTC). The list is 24 items carrying 42 findings.
- **A lead outside the slice:** the image's M7 client fails 4 of 18 native cases (`guest-cycle/b1-08-*`), posted by the coordinator on #1111.

---

## PL-01: the offline login answers any request naming the account with the cached sign-in body and its session token (a `bug` proposed)

- **Severity:** Low
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-01, F-02
- **Owner area:** the patched pin's `proxy_service.py` `handle_offline_login` (upstream code; a contained fix under `bugs-are-agent-first.md` rule 6, and a #585 line)
- **What:**
  - `handle_offline_login` (`proxy_service.py:491-505`) returns the cached `login2` row's body, `Token` included, to any `login`/`login2` naming the account while upstream cannot be reached; it compares no password or token and checks neither invalidation nor the configured account (A-1, R-1).
  - Reach: a loopback peer (`:290-292`); every native process is root and could read `system.cfg` anyway. A page in the sign-in window reaches it only by DNS rebinding with upstream failing at the same moment (F-02, conditional; A-2, R-2).
  - Fell on the guest against the image's service (M7's client): 200, `X-RA-Offline: 1`, `Token` present (`guest-cycle/b1-07-positive-f01.txt`); the pin's code is the same at these lines (`design`).
  - The fix: answer the offline login only to a request presenting the configured account's cached token or password; reject a foreign `Host` and any `Origin` (F-02).
- **Evidence:** F-01, F-02; A-1, A-2, A-22, A-23, R-1, R-2, R-19, R-20; `b1-07`
- **Can this be done on the VM?** Yes: the guest's probe (the link cut on the monitor, key names only) is the before and the after.
- **Already written:** tokens already served over loopback cannot be recalled; `proxy.sqlite3` keeps the `login2` rows of every account ever signed in. The fix changes what the port answers, not the rows; nothing to migrate, and a stale account's row is refused rather than purged (A-22, R-19).
- **Acceptance:** with the link cut, a `login2` naming the account and presenting no credential gets no `Token` (the probe's key names), and one presenting the configured token or password still gets the cached body; a request with a foreign `Host` or an `Origin` is refused
- **Disposition note:** a `bug`, #1157, filed at the stage-D ruling (#666, 13:48 UTC); stream S1 (D-RA-050)

## PL-02: the readiness check takes a foreign listener on `0.0.0.0:8080`, and the launch check does not (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-03
- **Owner area:** `raofflineproxy-ctl` `port_listening` (fork-own); the unit's `ExecStartPost`
- **What:**
  - `port_listening` (ctl :925-937) accepts any LISTEN at `00000000:1F90`, owner unchecked; `setsettings.sh:536` takes `127.0.0.1:8080` only, so the two predicates disagree.
  - With `Type=simple`, `ExecStartPost` looks right after the fork, before the service binds (`raofflineproxy.service:34-40`), so a pre-existing wildcard listener can let `enable` complete before the service dies on `EADDRINUSE` (R-6, plausible; A-6 argued the opposite).
  - Fell on the guest: `listening` rc 0 with a stand-in on `0.0.0.0:8080`, while the launch check went direct (`b1-04-positive-f03.txt`).
  - The fix: readiness is the service's own socket (its MainPID's inode) or an HTTP answer carrying `X-RA-Proxy: 1`; one predicate for the start and the launch.
- **Evidence:** F-03; A-6, A-24, R-6, R-21; `b1-04`
- **Can this be done on the VM?** Yes: the guest's stand-in listener, then `enable` itself.
- **Already written:** a device where the race happened holds `offlineproxy=1`, `hardcore=0` and the marker while the service failed; the boot pass retries the service. The fix reconciles nothing written; the next `enable` or `disable` rewrites the three (A-24, R-21).
- **Acceptance:** with a stand-in on `0.0.0.0:8080` and the service stopped, `listening` exits 1 and `enable` fails with the device as it was; with the service up, both exit 0
- **Disposition note:** a `bug`, #1159, filed at the stage-D ruling (#666, 13:48 UTC); stream S3

## PL-03: `disable` stops the service under a scan or top-up it could not see or could not stop (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-06, F-39
- **Owner area:** `raofflineproxy-ctl` `stop_running_run`, `do_disable`, `take_lock` (fork-own)
- **What:**
  - `exec 7<>"${SCAN_LOCK}" || return 0` (ctl :492) reads a lock it cannot open as nothing running; `do_disable` ignores `stop_running_run`'s status, its own timeout's 1 included (:525; A-8, R-8).
  - `take_lock` opens fd 9 with no close-on-exec, so every helper inherits the locked file, and the EXIT traps kill `CLIENT` without waiting: a helper that outlives the ctl keeps the lock under a pid that is gone (:1190, :1981; F-39, R-37).
  - Fell on the guest: with the lock path unopenable, `disable` rc 0 in 1 s, the service stopped, the holder alive, no request to stop it (`b1-06-positive-f06.txt`).
- **Evidence:** F-06, F-39; A-8, A-27, R-8, R-24, R-37; `b1-06`
- **Can this be done on the VM?** Yes: the guest's stand-in holder.
- **Already written:** `/var/run` is tmpfs, so a lock path left wrong clears at reboot; a helper's partial cache work stays and the next run resumes it. Nothing to migrate (A-27, R-24).
- **Acceptance:** with a holder alive and the lock unopenable, `disable` exits non-zero with the service and the toggle as they were, or stops the holder first; a helper does not hold the lock after its ctl has gone
- **Disposition note:** a `bug`, #1160, filed at the stage-D ruling (#666, 13:48 UTC); stream S4

## PL-04: a stamp that could not be written is not seen (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-07
- **Owner area:** `raofflineproxy-ctl` `write_stamp` and its callers (fork-own)
- **What:**
  - `write_stamp` (ctl :1073-1094) returns its failure and every caller ignores it (:1818, :1990, :2014, :2031, :2103, :2411, :2423, :2427), so the run exits as recorded and the row shows the run before.
  - `mv -f` into a `last-scan` that is a directory succeeds without publishing (A-9, R-9); a failed `printf` leaves `last-scan.tmp`.
- **Evidence:** F-07; A-9, A-28, R-9, R-25
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** devices may hold an older `last-scan` and a stray `last-scan.tmp`; the next good write replaces the first, and the fix removes the second. Nothing to migrate.
- **Acceptance:** with the stamp path made a directory, or the write failing, the run exits non-zero and says so; with a normal write the stamp is the new line
- **Disposition note:** a `bug`, #1161 (with PL-21), filed at the stage-D ruling (#666, 13:48 UTC); stream S5

## PL-05: a top-up mark dated ahead of the clock silences the link-return top-up (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-12
- **Owner area:** `raofflineproxy-ctl` `do_topup` (fork-own)
- **What:**
  - The played check compares the history's mtime with the mark's (ctl :2221, :2235); a mark touched while the clock ran ahead holds every later play "not newer" until wall time passes it; the mark's `touch` is unguarded (:2264).
  - Fell on the guest: the mark a day ahead, the top-up skipped with "no game played" (`b1-09-positive-f12.txt`).
- **Evidence:** F-12; A-17, A-33, R-27; `b1-09`
- **Can this be done on the VM?** Yes: `touch -d` on the guest, no clock change needed.
- **Already written:** devices whose clock ran ahead may hold a future-dated mark; the fix treats a mark ahead of now as absent, so those heal at the next link (R-27).
- **Acceptance:** with the mark a day ahead and a game played, the top-up runs; with the mark two hours back, the half-hour gate holds as before
- **Disposition note:** a `bug`, #1162, filed at the stage-D ruling (#666, 13:48 UTC); stream S6

## PL-06: work skipped or unread reads as a clean run (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-15, F-32
- **Owner area:** `raofflineproxy-ctl` `do_topup`, `run_image_pass` (fork-own)
- **What:**
  - The recently played pass's result line missing or unparseable with exit 0 reads `0 0 0`, nothing cached (ctl :2372-2380; A-11, R-11).
  - Under 60 s left, that pass is skipped with no why (:2362, :2389); a missing image helper returns 0 (:1854) (F-32; A-52, R-35).
- **Evidence:** F-15, F-32; A-11, A-36, A-52, R-11, R-27, R-35
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** no record holds a wrong count from this; a run that skipped work wrote no stamp. Nothing inherited.
- **Acceptance:** a pass that exits 0 without a valid result, a skipped pass and a missing helper each end the run with a why
- **Disposition note:** a `bug`, #1163 (with PL-23), filed at the stage-D ruling (#666, 13:48 UTC); stream S7

## PL-07: an unknown count reads as a number (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-16, F-26
- **Owner area:** `raofflineproxy-ctl` `count_ready`, `do_account` (fork-own)
- **What:**
  - `count_ready` (ctl :888-897) prints 0 when the export cannot be read and trusts a failed client's last numeric line behind `tail -n 1`; it never calls `cannot_tell`, and the number goes into the stamps (A-12, R-12).
  - `do_account` reads a `login2` row of valid JSON that is not an object as "no points" (:780-781) and takes a JSON boolean as a score (F-26; A-13, R-13).
  - Fell on the guest: the export a directory, `ready` 0 (`b1-05-positives-f16-f17.txt`).
- **Evidence:** F-16, F-26; A-12, A-13, A-37, R-12, R-13, R-28; `b1-05`
- **Can this be done on the VM?** Yes: the guest's export made a directory.
- **Already written:** stamps may carry `ready=0` from a failed read; the next scan or top-up overwrites them. Nothing to migrate (R-28).
- **Acceptance:** with the export unreadable, `ready` says it cannot tell (exit 2, nothing on stdout) and no stamp records a count it did not read
- **Disposition note:** a `bug`, #1164, filed at the stage-D ruling (#666, 13:48 UTC); stream S8

## PL-08: one pathname the job list cannot carry fails or mangles the whole listing (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-17, F-29, F-41
- **Owner area:** `raofflineproxy-ctl` `list_jobs`, `run_jobs`; `raofflineproxy-cache-indexed` (fork-own)
- **What:**
  - A selected pathname with a byte invalid in UTF-8 raises at the job file's strict write (ctl :1674): the scan reads `why LIBRARY_UNREADABLE` (A-14, R-14).
  - A newline in a pathname splits a job line (`mapfile`, `splitlines`), and the ctl does not reconcile `DONE` with its planned jobs (F-29; A-49, R-32); an `I` job with no id falls through to hashing (F-41, R-39).
  - Reproduced on the host (`tools/t19-listing-fixture.py`, `stage-b/listing-fixture.txt`) and the guest (`b1-05`).
- **Evidence:** F-17, F-29, F-41; A-14, A-38, A-49, R-14, R-28, R-32, R-39; the fixture; `b1-05`
- **Can this be done on the VM?** Yes: `tools/t19-listing-fixture.py` on the host is the before; the guest's 0xff name too.
- **Already written:** the trigger is the player's own file, which an update does not rename; a `last-scan` with `why=LIBRARY_UNREADABLE` clears on the next good scan. No file is renamed and no cache cleared (A-38).
- **Acceptance:** `tools/t19-listing-fixture.py` lists the library with the 0xff name and the newline name and caches the rest (exit 1 on the fix: the defect no longer reproduces), or reports the one entry and goes on
- **Disposition note:** a `bug`, #1165 (with PL-16's classifier), filed at the stage-D ruling (#666, 13:48 UTC); stream S9

## PL-09: the unit runs as root with no hardening, and every file it writes is world-readable (a `bug`, ruled)

- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Source Finding:** F-04, F-25
- **Owner area:** `raofflineproxy.service`; the four scripts (fork-own)
- **What:**
  - No `User=`, `NoNewPrivileges`, `Protect*`, `Private*`, `CapabilityBoundingSet`, `RestrictAddressFamilies` or `UMask=` (R3: 0); the service parses network bodies and ROM images in native code (R-7).
  - Every file observed under the proxy's folder is `644 root`, the store with the token row included (`b1-03-scan.txt`; A-5, R-5).
- **Evidence:** F-04, F-25; A-7, A-25, A-46, R-7, R-22, R-29; `b1-02`, `b1-03`
- **Can this be done on the VM?** Yes: `systemctl show` and `stat` on the guest.
- **Already written:** existing files keep their modes; a `UMask=` changes only new ones, so a hardening stream carries a non-destructive mode pass (A-46).
- **Acceptance:** recorded as the design question for the coordinator; a hardening stream, if one is ruled, ends with the service's directives and the files' modes read from a guest
- **Disposition note:** a `bug`, Low, #1158, filed at the stage-D ruling (#666, 13:48 UTC); stream S2 (D-RA-049); the full sandboxing Backlog #1155

## PL-10: the username on argv at four sites

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-05
- **Owner area:** `raofflineproxy-ctl` (fork-own)
- **What:**
  - Four `python3` calls pass the public account name on argv (ctl :616, :647, :764, :1029); the listing passes it in the environment (:1265), as its own rule says (A-5, R-5).
- **Evidence:** F-05; A-5, A-26, R-5, R-23
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** nothing persisted.
- **Acceptance:** recorded as written, or the environment at all five sites
- **Disposition note:** recorded as written: the account name is public; the listing's environment rule stays

## PL-11: the listing writes the store through the client's `Storage()`

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-08
- **Owner area:** `raofflineproxy-ctl` `list_jobs` (fork-own)
- **What:**
  - `storage = Storage()` (ctl :1417) sets WAL and creates the schema (`storage.py:106-151`); the ctl's own reads are `mode=ro` (A-10, R-10). It closes at :1564.
- **Evidence:** F-08; A-10, A-29, R-10, R-26
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** nothing beyond the schema the service writes anyway.
- **Acceptance:** recorded as written, or the listing reads through `mode=ro`
- **Disposition note:** recorded as written: the schema the service writes anyway; Argon's "never closed" refuted at ctl :1564

## PL-12: writer hygiene: the verify cursor, the log's rotation, the fifo

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-09, F-10
- **Owner area:** `raofflineproxy-cache-images`; `raofflineproxy-ctl` (fork-own)
- **What:**
  - `verify-cursor` is written directly (`cache-images:169-177`); the helpers' stderr appends bypass `slog`'s rotation (ctl :1711, :1713, :1876, :1987, :2301, :2366); the fifo is named by `mktemp -u` then made (:1708-1709).
- **Evidence:** F-09, F-10; A-20, A-30, A-31, R-26
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** a large `scan.log` rotates at the next `slog`; nothing to migrate.
- **Acceptance:** recorded as written, or each writer temp-and-renamed and the log bounded
- **Disposition note:** recorded as written: the cursor regenerable, the log rotating at the next `slog`; `02` names the fifo's directory

## PL-13: the scan's missing deadline against the interface's staleness bound

- **Severity:** Info
- **Category:** Clarity
- **Question:** Q7
- **Source Finding:** F-11, F-34
- **Owner area:** `raofflineproxy-ctl` `do_scan` (fork-own); `CloudText::parseRunningProgress` (T20's and T2's)
- **What:**
  - The scan has no deadline by design (a foreground page with CANCEL, D-UI-078); the interface treats a `running` line older than its bound as a dead run because "the ctl bounds its runs" (`CloudText.cpp:1335-1342`), and `run_jobs` removes `running` before the image pass (A-19, A-54, R-17).
- **Evidence:** F-11, F-34; A-19, A-32, A-54, R-17, R-27
- **Can this be done on the VM?** Yes: a slow listing on a guest with the page open.
- **Already written:** nothing persisted.
- **Acceptance:** recorded as the design; the staleness contract handed to T20 (#667)
- **Disposition note:** handed to T20 (#667): the staleness contract in `02` § What T20 inherits

## PL-14: patch 013 and 015's inputs without a bound, and 013's validator

- **Severity:** Info
- **Category:** Efficiency
- **Question:** Q5
- **Source Finding:** F-13, F-30, F-36
- **Owner area:** patches 013 and 015 (the fork's `+` side)
- **What:**
  - `zlib.decompress(idat)` has no `max_length` and `_fetch_image` reads bodies whole (patch 013); `png_problem` checks no IHDR or chunk order (F-30); a short read raises out of the retry loop (F-36); the lookup threads are uncapped in number (patch 015) (A-20, A-34, A-50, R-16, R-33).
- **Evidence:** F-13, F-30, F-36; A-20, A-34, A-50, R-16, R-27, R-33
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** cached images published before 013 stay until a `--verify` pass; nothing to migrate.
- **Acceptance:** recorded as written, or a bounded inflate and a structural check, each with a case
- **Disposition note:** recorded as written: the badge CDN's images; the lookup threads bounded by the lookups

## PL-15: upstream's POST path paces nothing after a 429, and the usage report takes any account's row

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-14, F-38
- **Owner area:** the patched pin's `network.py` `http_post`, `usage_report.py` (upstream code; #585 lines)
- **What:**
  - `http_post` marks no 429 pause and skips the throttle `http_get` waits on (`network.py:516-575` against `:376-420`); with patch 001 the 429 reaches the emulator (A-21, R-18).
  - `usage_report._report` takes `storage.load_login_credentials()`, which patch 007 replaced in `resolve_credentials` (`usage_report.py:185`; R-36).
- **Evidence:** F-14, F-38; A-21, A-35, R-18, R-36
- **Can this be done on the VM?** Yes: a loopback stand-in for the server answering 429.
- **Already written:** nothing persisted.
- **Acceptance:** two #585 lines written in the lane's shape (the target, the current-source comparison, the minimal patch); never sent (D-WORKFLOW-165)
- **Disposition note:** deferred to #585: two lines in `02` § The patches; the coordinator posts them

## PL-16: usage exits and the jobs' classifier

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-18, F-24
- **Owner area:** `raofflineproxy-ctl` (fork-own)
- **What:**
  - Usage exits 2 at the dispatch (:2453) and 64 elsewhere (:944, :1935, :1938).
  - The jobs' classifier matches stop words over the whole line, file name included: a name can stop a scan, set the limit, or turn failures into skips (ctl :1736-1755; A-15, R-15).
- **Evidence:** F-18, F-24; A-15, A-39, A-45, R-15, R-29
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** nothing persisted.
- **Acceptance:** recorded as written, or one usage code and a classifier that reads the reason field
- **Disposition note:** the classifier fixed with PL-08 (#1165, stream S9); the usage exits recorded as written

## PL-17: the refresh helper's protocol and cost

- **Severity:** Info
- **Category:** Clarity
- **Question:** Q7
- **Source Finding:** F-19, F-40
- **Owner area:** `raofflineproxy-refresh` (fork-own)
- **What:**
  - `note()` lines on the protocol's stdout; `done a|b` means failed, left, or all unfinished by path (`refresh:170`, `:223`, `:227`); `row_ages` reads three whole prefixes per game (F-40). No interface caller at the pin.
- **Evidence:** F-19, F-40; A-40, R-29, R-38
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** nothing persisted.
- **Acceptance:** handed to T20 (#667) for the row #224 would add
- **Disposition note:** handed to T20 (#667), with #224's row

## PL-18: a reader row for a token gone, and a comment naming a function as a verb

- **Severity:** Info
- **Category:** Clarity
- **Question:** Q6
- **Source Finding:** F-20
- **Owner area:** EmulationStation `CloudText.cpp`, `GuiRetroAchievementsSettings.cpp` (T20's)
- **What:**
  - `scanWhy` keeps `NO_GAMES_FOUND` (`CloudText.cpp:1032-1033`), which no producer emits; the page's comment at `:154` names `have_account` as a verb.
- **Evidence:** F-20; A-41, R-29
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** nothing persisted.
- **Acceptance:** handed to T20 (#667), as the coordinator said at 12:41
- **Disposition note:** handed to T20 (#667)

## PL-19: the recipe's comment, the siblings' provenance, 020 and 021's headers, and the drafts owed

- **Severity:** Info
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-21, F-22
- **Owner area:** `package.mk`, the sibling recipes, patches 020 and 021 (fork-own); `docs/upstream/raofflineproxy/`
- **What:**
  - `package.mk:6` says *"The16 patches"* over eighteen; the siblings name older proxy commits as their pins' source; 020 and 021 carry no header.
  - Eight patches have no draft (003, 004, 010, 011, 012, 016, 020, 021) and every draft's base is older than the pin (`02` § The patches).
- **Evidence:** F-21, F-22; A-42, A-43, R-29
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** nothing persisted.
- **Acceptance:** the comment corrected, or the #585 lines written in `02` § The patches
- **Disposition note:** stream S10 (documentation, no bug); the missing drafts and stale bases a #585 line in `02` § The patches

## PL-20: what the harness proves

- **Severity:** Info
- **Category:** Standards
- **Question:** Q2
- **Source Finding:** F-23
- **Owner area:** `tools/rc-preflight`, `tools/last-good-scripts-test` (T12's and T15's)
- **What:**
  - The proxy-schema check is a comment check; the scripts suite runs the real ctl in `bwrap` with shims; upstream's native tests need a built library (3 OK, 15 skipped on the host).
- **Evidence:** F-23; A-44, R-29; `stage-c/native-host.out`
- **Can this be done on the VM?** Yes: the integration build's installed-native run against the tree's service (`pending-image`).
- **Already written:** nothing persisted.
- **Acceptance:** recorded as written
- **Disposition note:** recorded as written; the installed-native run on the built image is the integration's owed item

## PL-21: a rollback not read back, and the pending marker lost on a failed restore

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-27, F-28
- **Owner area:** `raofflineproxy-ctl` `enable_undo`, `put_back`, `ack_index_pending` (fork-own)
- **What:**
  - `put_back` reads nothing back and `enable_undo` ignores its results (ctl :421-423, :430-436); `disable` swallows a failed stop (:410) (A-47, R-30).
  - The index-pending fallback writes one shared `.tmp` without the lock, and `ack_index_pending` removes the aside even when its restore failed (:2150-2157, :2176-2177) (A-48, R-31).
- **Evidence:** F-27, F-28; A-47, A-48, R-30, R-31
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** a device where a rollback failed holds the settings the forward step wrote; the next `enable` or `disable` rewrites them.
- **Acceptance:** recorded as written, or each undo read back and the aside kept on a failed restore
- **Disposition note:** fixed with PL-04 (#1161, stream S5)

## PL-22: the request path's malformed inputs and the redaction's reach

- **Severity:** Info
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-31, F-35, F-37
- **Owner area:** the patched pin's `proxy_service.py`, `utils.py` (upstream code; #585 lines)
- **What:**
  - A negative `Content-Length` reaches `rfile.read()` as an unbounded read; a non-numeric one, a non-UTF-8 body and a non-integer `g=` raise unhandled (`proxy_service.py:298-303`, `:439`); loopback only (A-51, R-34).
  - The query redactor matches literal lowercase `t=`/`p=` only (`utils.py:110`): percent-encoded and uppercase names pass (A-3, R-3).
- **Evidence:** F-31, F-35, F-37; A-3, A-51, R-3, R-34
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** the service's log may hold such lines; nothing to migrate.
- **Acceptance:** #585 lines written in the lane's shape
- **Disposition note:** deferred to #585: two lines in `02` § The patches; the coordinator posts them

## PL-23: a damaged image that cannot be removed counts as present

- **Severity:** Info
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-33
- **Owner area:** `raofflineproxy-cache-images` (fork-own)
- **What:**
  - On `--verify`, an unlink that fails is logged and the file then counts as present (`cache-images:338-343`, `:452`) (A-53, R-35).
- **Evidence:** F-33; A-53, R-35
- **Can this be done on the VM?** Yes: on the host, the script's function run against a fixture, as `tools/t19-listing-fixture.py` does for F-17, or on a guest window; the window's record (`02` § The guest cycle) is the before.
- **Already written:** a damaged file may stay in the cache; the next pass that can remove it fetches it again.
- **Acceptance:** recorded as written, or a failed removal counted as an image not saved
- **Disposition note:** fixed with PL-06 (#1163, stream S7)

## PL-24: the ctl's stderr goes to /dev/null for the rest of a run once pending_lock has run (found at stage E)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-42
- **Owner area:** `raofflineproxy-ctl` `pending_lock` (fork-own)
- **What:**
  - `exec 6<>"${PENDING_LOCK}" 2>/dev/null || return 1`. An `exec` with no command applies its redirections to the shell, so from the first `pending_lock` to the end of the run the ctl's stderr is `/dev/null`, `fail`'s line included. `say` (the journal) is unaffected.
  - Found by the lane in S5 (#1161), filed as #1166. Ruled into S5 by the coordinator (#666, 15:15 UTC; `t19-streams.md` at `648dadebf1`).
- **Evidence:** F-42; `stage-e/s5-before.txt` and `s5-after.txt`, case 6
- **Can this be done on the VM?** Yes: on the host, the real ctl's `index-offline` in the lane's bubblewrap harness, with the marker's publication refused while the lock is held.
- **Already written:** nothing; stderr is not stored.
- **Acceptance:** a `fail` after `pending_lock` reaches stderr: FAIL before, PASS after
- **Disposition note:** a `bug`, #1166, carried by stream S5 (#1161) at the coordinator's ruling of 15:15 UTC

## Phase 7 resolution gate

Every item was open until stage F; each row now takes its outcome (resolved with its commit, deferred to a named issue, or withdrawn: recorded as written with its reason). The dispositions are the coordinator's at the stage-D pause (#666, 13:48 UTC), and PL-24's at 15:15 UTC. Stage F, 2026-10-26: every row at its outcome -- 14 resolved, 5 deferred (#667 three, #585 two), 5 withdrawn.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Resolved | Resolved in `57c5e8c4ec` (S1) under #1157, D-RA-050: patch `022-offline-login-requires-credential.patch`; the offline login answers the cached token or a password matching its recorded hash, for the configured account, from a loopback Host with no Origin; the suite's 011 check carried over in `5810eff004` (`stage-e/s1-*.txt`) |
| PL-02 | Resolved | Resolved in `6aca961c00` (S3) under #1159: `listening` counts only the unit's MainPID's own socket; two suite checks carried over (`stage-e/s3-*.txt`) |
| PL-03 | Resolved | Resolved in `fdcd576e99` (S4) under #1160: a lock it cannot open is `cannot_tell`, a run that did not stop leaves the device on, helpers start without fd 9, the EXIT traps wait bounded (`stage-e/s4-*.txt`) |
| PL-04 | Resolved | Resolved in `44120e2e17` (S5) under #1161: a stamp that could not be written ends the run 1 with `STAMP_UNWRITABLE`; the undo's steps read back (`stage-e/s5-*.txt`) |
| PL-05 | Resolved | Resolved in `7239b1adc1` (S6) under #1162: a mark dated ahead of the clock is no mark (`stage-e/s6-*.txt`) |
| PL-06 | Resolved | Resolved in `54ab8c6c10` (S7) under #1163: an unreadable result is `RESULT_UNREADABLE`, a pass skipped for time `TOOK_TOO_LONG`, a missing helper `SOME_IMAGES_NOT_SAVED`; the suite's fixture completed (D-WORKFLOW-211) (`stage-e/s7-*.txt`) |
| PL-07 | Resolved | Resolved in `72f0f3e3dd` (S8) under #1164: `ready` cannot tell is exit 2 and nothing on stdout; stamps say `ready=unknown`; `account` takes only an object and a number (`stage-e/s8-*.txt`) |
| PL-08 | Resolved | Resolved in `09b204153d` (S9) under #1165: the job list is NUL-separated in surrogateescape, `DONE` reconciled, an id-less index job refused; `tools/t19-listing-fixture.py --expect` (`stage-e/s9-*.txt`) |
| PL-09 | Resolved | Resolved in `76658dd062` (S2) under #1158, D-RA-049: `UMask=0077`, `umask 077`, the `private-modes` pass at `enable` and `ExecStartPre=-`; the full sandboxing is Backlog #1155 (`stage-e/s2-*.txt`) |
| PL-10 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#666, 13:48 UTC); the account name is public and the listing's environment rule stays; no change made |
| PL-11 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#666, 13:48 UTC); the schema is the service's own, and Argon's "never closed" is refuted at ctl `:1564`; no change made |
| PL-12 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#666, 13:48 UTC); the cursor is regenerable and the log rotates at the next `slog`; `02` § The writers names the fifo's directory (`/tmp`); no change made |
| PL-13 | Deferred | Deferred: #667 (T20), the staleness contract in `02` § What T20 inherits, as ruled at the stage-D ruling (#666, 13:48 UTC) |
| PL-14 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#666, 13:48 UTC); the badge CDN's images; the lookup threads bounded by the lookups; no change made |
| PL-15 | Deferred | Deferred: #585, two lines in `02` § The patches, The #585 lines (`http_post`'s 429; the usage report's row), for the coordinator to post; not sent (D-WORKFLOW-165) |
| PL-16 | Resolved | Resolved in `09b204153d` (S9) under #1165 for the classifier (it reads the reason field, never the file name); the usage exits recorded as written at the stage-D ruling (#666, 13:48 UTC) |
| PL-17 | Deferred | Deferred: #667 (T20), with #224's row, in `02` § What T20 inherits, as ruled at the stage-D ruling (#666, 13:48 UTC) |
| PL-18 | Deferred | Deferred: #667 (T20), `NO_GAMES_FOUND`'s row and the page's comment, in `02` § What T20 inherits, as ruled at the stage-D ruling (#666, 13:48 UTC) |
| PL-19 | Resolved | Resolved in `49f3dc8679` (S10): the recipe counts nineteen patches with the gaps named; 020 and 021 carry headers; `tools/pkgcheck raofflineproxy` exits 0; the missing drafts and stale bases a #585 line in `02` § The patches (`stage-e/s10-*.txt`) |
| PL-20 | Withdrawn | Withdrawn: recorded as written at the stage-D ruling (#666, 13:48 UTC); the installed-native run against the tree's own service on the built image is the integration's owed item (`02` § The guest cycle); no change made |
| PL-21 | Resolved | Resolved in `44120e2e17` (S5) with PL-04, under #1161: `put_back` and `enable_undo` read back; the aside is kept when its put-back fails (`stage-e/s5-*.txt`) |
| PL-22 | Deferred | Deferred: #585, two lines in `02` § The patches, The #585 lines (the request path's malformed inputs; the query redactor's reach), for the coordinator to post; not sent (D-WORKFLOW-165) |
| PL-23 | Resolved | Resolved in `54ab8c6c10` (S7) with PL-06, under #1163: a damaged image `--verify` cannot remove counts as not saved (`stage-e/s7-*.txt`) |
| PL-24 | Resolved | Resolved in `44120e2e17` (S5) under #1166, ruled into S5 (#666, 15:15 UTC): `pending_lock`'s redirect scoped to the open (`stage-e/s5-*.txt`, case 6) |

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: "Low"
  category: Security
  question: Q3
  source_finding: "F-01, F-02"
  outcome: "resolved"
- id: PL-02
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-03"
  outcome: "resolved"
- id: PL-03
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-06, F-39"
  outcome: "resolved"
- id: PL-04
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-07"
  outcome: "resolved"
- id: PL-05
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-12"
  outcome: "resolved"
- id: PL-06
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-15, F-32"
  outcome: "resolved"
- id: PL-07
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-16, F-26"
  outcome: "resolved"
- id: PL-08
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-17, F-29, F-41"
  outcome: "resolved"
- id: PL-09
  severity: "Low"
  category: Security
  question: Q2
  source_finding: "F-04, F-25"
  outcome: "resolved"
- id: PL-10
  severity: "Info"
  category: Standards
  question: Q2
  source_finding: "F-05"
  outcome: "withdrawn"
- id: PL-11
  severity: "Info"
  category: Standards
  question: Q2
  source_finding: "F-08"
  outcome: "withdrawn"
- id: PL-12
  severity: "Info"
  category: Standards
  question: Q2
  source_finding: "F-09, F-10"
  outcome: "withdrawn"
- id: PL-13
  severity: "Info"
  category: Clarity
  question: Q7
  source_finding: "F-11, F-34"
  outcome: "deferred"
- id: PL-14
  severity: "Info"
  category: Efficiency
  question: Q5
  source_finding: "F-13, F-30, F-36"
  outcome: "withdrawn"
- id: PL-15
  severity: "Info"
  category: Correctness
  question: Q3
  source_finding: "F-14, F-38"
  outcome: "deferred"
- id: PL-16
  severity: "Info"
  category: Standards
  question: Q2
  source_finding: "F-18, F-24"
  outcome: "resolved"
- id: PL-17
  severity: "Info"
  category: Clarity
  question: Q7
  source_finding: "F-19, F-40"
  outcome: "deferred"
- id: PL-18
  severity: "Info"
  category: Clarity
  question: Q6
  source_finding: "F-20"
  outcome: "deferred"
- id: PL-19
  severity: "Info"
  category: Renovation
  question: Q4
  source_finding: "F-21, F-22"
  outcome: "resolved"
- id: PL-20
  severity: "Info"
  category: Standards
  question: Q2
  source_finding: "F-23"
  outcome: "withdrawn"
- id: PL-21
  severity: "Info"
  category: Correctness
  question: Q3
  source_finding: "F-27, F-28"
  outcome: "resolved"
- id: PL-22
  severity: "Info"
  category: Security
  question: Q3
  source_finding: "F-31, F-35, F-37"
  outcome: "deferred"
- id: PL-23
  severity: "Info"
  category: Correctness
  question: Q3
  source_finding: "F-33"
  outcome: "resolved"
- id: PL-24
  severity: "Low"
  category: Correctness
  question: Q3
  source_finding: "F-42"
  outcome: "resolved"
```
