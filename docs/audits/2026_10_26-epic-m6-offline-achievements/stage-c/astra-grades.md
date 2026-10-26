# The lane's grades of GPT-6 Astra's 55 items (T19, #666)

Each item is re-read at its lines before its grade. The re-reads that turned a finding are in `rereads/`: `a02-a51.out` (the request path, `proxy_service.py:286-326` at the patched pin); the ctl at `8ebaf8daad` for A-5 (:1244-1246), A-13 (:776-782), A-47 (:420-437), A-48 (:2150-2181); and `CloudText.cpp:1335-1345` for A-54.

**Counts:** accepted 51, accepted in part 1, plausible 3, rejected 0 (55).

| Item | Grade | What the re-read showed, and what changes |
| --- | --- | --- |
| A-1 | accepted | `handle_offline_login` as F-01 says; Astra's conditions are exact: a `login`/`login2`, a non-empty `u=`, a cached row, and an upstream result other than `success` or `http_error` (a 401 or 403 from upstream returns directly). It also returns a former account's row. F-01 stands. |
| A-2 | accepted | **The first reader missed a peer check:** `_handle_request` refuses any peer but `127.0.0.1` or `::1` with 403 (`proxy_service.py:290-292`). `02` § The listener is corrected. F-02 narrows to a conditional browser-origin reach (a page on the device connects from loopback); no rebinding read is demonstrated. |
| A-3 | accepted in part | The raw-query redactor matches literal lowercase `t=`/`p=` only (`utils.py:110`), so a percent-encoded name passes; the form redactor parses names. Accepted as a coverage gap (new F-35, Info). The `extra_files` bypass is real but its one caller passes a note naming no credential (`log_uploader.py:370-380`), so not a leak. |
| A-4 | accepted | `02`'s "none needed so far" overreaches: the error texts that reach `scan.log` come from code partly outside what was read. Narrowed to *no credential-bearing message found in what was read*. |
| A-5 | accepted | The rule at ctl :1244-1246 is the listing's ("the account name reaches the listing through the environment"), and the listing keeps it. F-05 narrows: four argv sites carry the public name, not a broken promise. F-25's "every file" narrows to *every file observed*. |
| A-6 | accepted | F-03 narrows: the predicate takes a foreign wildcard listener (the guest's `listening` rc 0), but `enable` also needs `systemctl start` to succeed, and the service's own bind to `127.0.0.1:8080` meets the wildcard socket. The guest showed `listening`, not a completed `enable`. |
| A-7 | accepted | F-04 as Info, defense in depth. |
| A-8 | accepted | And more: `do_disable` ignores `stop_running_run`'s status (ctl :525), the timeout's 1 included, so the fix is in `do_disable`, not only :492. F-06's fix note changes. |
| A-9 | accepted | `mv -f tmp dir` succeeds into a directory at `last-scan`, a success that publishes nothing; F-07's fix checks the published path. |
| A-10 | accepted | F-08 as written. |
| A-11 | accepted | F-15 as written, plus the exact-spelling grep. |
| A-12 | accepted | F-16 is wider: a failed client that prints a numeric last line is trusted. |
| A-13 | accepted | **New (F-26, Info):** a `login2` row of valid JSON that is not an object exits 1 (ctl :780-781), read as "no points", bypassing `cannot_tell`. |
| A-14 | accepted | F-17's scope is a pathname selected into the job list; the helper's strict read (`cache-indexed:149`) needs the same fix. |
| A-15 | accepted | F-18, F-24 as written; F-24 can also turn failures into skips. |
| A-16 | accepted | `02` § The bounds' wording: nine probes and eight sleeps (no 90 s ceiling); `STOP_WAIT` bounds a wait, not a stop. |
| A-17 | accepted | F-12 as written; it holds only on the plain link-return route. |
| A-18 | accepted | `02`'s "900 s, enforced" is too strong: `time_left` reads the wall clock (a backward step lengthens it), and the probe subprocess has no `timeout` of its own. The row becomes "a soft deadline". |
| A-19 | accepted | F-11 is policy (D-UI-078); the 120 s badge wait bounds a join. |
| A-20 | accepted | F-09, F-13 as written; an unremembered lookup can still block synchronously. |
| A-21 | accepted | F-14 narrows to the two functions; the full forwarding graph is outside the packet. |
| A-22 | accepted | F-01 Low; the fix requires credential proof before a cached token is returned. Already written: tokens already served cannot be recalled. |
| A-23 | accepted | F-02 narrowed (A-2). |
| A-24 | accepted | F-03 Low, narrowed (A-6). |
| A-25 | accepted | F-04 Info. |
| A-26 | accepted | F-05 narrowed (A-5). |
| A-27 | accepted | F-06 Low; the fix in `do_disable` (A-8). |
| A-28 | accepted | F-07 Low. |
| A-29 | accepted | F-08 Info. |
| A-30 | accepted | F-09 Info. |
| A-31 | accepted | F-10 Info. |
| A-32 | accepted | F-11 Info, the design. |
| A-33 | accepted | **F-12 proposed Low** (was Info), with the already-future marks on devices. |
| A-34 | accepted | F-13: the inflate's bound is an availability fix (with A-50). |
| A-35 | accepted | F-14 narrowed. |
| A-36 | accepted | **F-15 proposed Low** (was Info). |
| A-37 | accepted | F-16 Low, wider (A-12). |
| A-38 | accepted | F-17 Low; framed paths end to end, or a reported skip of the one entry. |
| A-39 | accepted | F-18 Info. |
| A-40 | accepted | F-19: `b` means failed, unattempted, or all unfinished; the "no reader" claim rests on the interface's calls listed in `01`, outside this packet. |
| A-41 | accepted | F-20 as written. |
| A-42 | accepted | F-21: the sibling recipes are outside the packet (the first reader read them). |
| A-43 | accepted | F-22 is bookkeeping, not a runtime finding. |
| A-44 | accepted | F-23 as written. |
| A-45 | accepted | F-24 as written. |
| A-46 | accepted | F-25 narrowed (A-5). |
| A-47 | accepted | **New (F-27, Info):** `put_back` reads nothing back and `enable_undo` ignores its results (ctl :421-423, :430-436), so a failed rollback is not seen; `03` § 3.3's "undoes every step" is narrowed. |
| A-48 | accepted | **New (F-28, Info):** the lock-less fallback writes one shared `.tmp`, and `ack_index_pending` removes the aside even when its restore `mv` failed (ctl :2176-2177), losing the only marker. |
| A-49 | plausible | **New (F-29, Info):** a newline in a pathname splits a job line (`splitlines`, `cache-indexed:149`). Not reproduced; a newline in a ROM name is rare. |
| A-50 | accepted | **New (F-30, Info):** patch 013's `png_problem` checks no IHDR or chunk order; the unbounded inflate is the `+` side's own (F-13). |
| A-51 | accepted | **New (F-31, Info):** a negative `Content-Length` passes the cap and reaches `rfile.read()` as an unbounded read (`proxy_service.py:298-302`); loopback peers only. |
| A-52 | accepted | **New (F-32, Info):** a missing image helper returns 0 (ctl :1854), and under 60 s left the recently played pass is skipped with no why (:2362, :2389). |
| A-53 | plausible | **New (F-33, Info):** a damaged image that cannot be unlinked stays counted present (`cache-images:338-343`, then presence at :452). Not reproduced. |
| A-54 | plausible | **New (F-34, Info):** `CloudText.cpp:1335-1342` treats a `running` line older than its bound as a dead run because "the ctl bounds its runs", but the scan does not (F-11), and its listing writes `running` once. T20's and T2's side; not reproduced. |
| A-55 | accepted | F-12 and F-15 proposed Low; F-13 an availability fix; `04`'s "no finding loses an award or a save" narrowed to *none demonstrated in what was read*. |
