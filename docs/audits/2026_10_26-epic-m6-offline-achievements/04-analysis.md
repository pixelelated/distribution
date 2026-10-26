# Analysis — M6.P2 T19, the offline achievements proxy (#666)

## Executive summary

The proxy is in good order where the fork has worked it hardest: every answer the interface acts on fails closed (`cannot_tell`, `added=unknown`), the stamps are written whole, the enable and disable undo themselves, and the integration test (12 OK) and the scripts suite (1,379 PASS) hold the preparation and the ctl's verbs. The eighteen patches apply to their pin at fuzz 0.

What the read found, in the brief's four families:

- **Where a credential travels.** The port answers a login naming the account, while upstream cannot be reached, with the cached sign-in body and its session token, comparing no password or token (F-01, upstream code). On this device every local process is root and could read `system.cfg`'s token anyway; the reach the port adds is a web page shown on the device, by DNS rebinding, since the service checks neither `Host` nor `Origin` (F-02). The username rides `python3`'s argv at four sites against the file's own rule (F-05).
- **What runs as root on an unauthenticated port.** The unit carries no hardening directive (F-04), and the ctl's readiness check takes any listener on `0.0.0.0:8080`, so a foreign one turns the toggle on while every launch goes direct (F-03).
- **A check whose failure reads as success.** The scan lock that cannot be opened reads as nothing running (F-06); a stamp that could not be written is not seen (F-07); an unreadable ready count prints 0 (F-16); one undecodable ROM name fails the whole listing, reproduced on the host (F-17).
- **A bound that is not enforced.** The scan has none, by design (F-11); the top-up's played check trusts the mark's mtime (F-12); the IDAT inflate and the lookup threads are unbounded (F-13); `http_post` marks no 429 pause (F-14, upstream).

Six are proposed as Low `bug`s (F-01, F-03, F-06, F-07, F-16, F-17); nineteen are Info. Five of the six fell on the guest as read (F-01, F-03, F-06, F-16, F-17), and F-17 on the host too; F-12 fell as well. Nothing is Medium or above: the port is loopback, the device is single-user and root, and no finding loses an award or a save.

## Acceptance-criteria scorecard

The brief's § 7 against this folder at stage C's start:

| Criterion | State |
| --- | --- |
| `00` to `05` | `00` to `04` written; `05` at stage C's end |
| the lint | pre-issue at stage C's end |
| `review-plan.json`, the four provenance files, the manifest | stage C |
| the punch-list issue | stage D |
| `reviewed-at`, `fixed-at`; nothing under `packages/`, `projects/`, `tools/` | R17 empty at stages A and B |
| `01` § Scope | written (`01`) |
| § Coverage 27 | 27 |
| § The listener | written; the user (`root`) and the bind (`127.0.0.1:8080`) read from the guest |
| § The credential's paths | written |
| § The writers, generated | 77 rows, `tools/t19-writers.py`, its drift control |
| § The patches, 18 | 18 |
| § The bounds | written |
| § The runs | written (R0 to R17, the unpack, the integration test, the suite, the generator) |
| § The guest cycle | written: START 12:43:49, RETURN 12:53:37 UTC; the image's scripts are M7's, so the tree's ran from `/storage/t19/bin/` |
| `00`'s closing census | at hand-back |
| `04` Q1 to Q8 | below |
| `proved:`, `question:`, § What T20 inherits | written in `02`; `question:` in `05` |
| the retro | stage G |
| the five checkers | before each push |

## Risk assessment

| Severity | Count | Findings |
| --- | ---: | --- |
| High | 0 | |
| Medium | 0 | |
| Low | 6 | F-01, F-03, F-06, F-07, F-16, F-17 |
| Info | 19 | F-02, F-04, F-05, F-08 to F-15, F-18 to F-25 |
| **Total** | **25** | |

The Low six share one shape: a state the device can be in -- a link down, a second listener, a full card, a lock or export that cannot be opened, a file name from an archive -- where the code's answer is wrong and nothing says so.

## Coverage boundary

- **Read:** the 27 whole at `8ebaf8daad`; the patched pin's request path, offline login, `auth`, `log_uploader`, `usage_report`, `storage` initialisation, `es_export`, `network` GET and POST; the interface's parsers at `16dbac5211`; the context files in `01`.
- **Not read, and why:** the rest of the upstream client (the menu, the queue internals, `rvz_datasource.py` beyond patch 020's hunk) -- upstream's, outside the four families; the rcheevos and libchdr sources -- T3's and the siblings' pins only; the per-emulator token files -- T30's.
- **Not run on the host:** the ctl outside `last-good-scripts-test`'s `bwrap`, the service, any network call. The guest's facts are in `02` § The guest cycle: the image's scripts are M7's, so `8ebaf8daad`'s four ran from `/storage/t19/bin/` against the image's client and service; the award proof could not run (the QA account's reachable achievements are spent, D-RA-006).

## Q1 The listener

Bound to `127.0.0.1:8080` by the client's default (`config.py:376-377`), AF_INET only; no `Host` or `Origin` check and no CORS header (`02` § The listener). Without identity it answers the store's game data, unlocks and badges, and -- while upstream cannot be reached -- a login naming the account with the cached sign-in and its token (F-01, F-02). The unit runs the service as root with the defaults (F-04). The readiness check takes a foreign `0.0.0.0` listener (F-03); `setsettings.sh` does not, so the two disagree. `cloud_oauth`'s serve shares the port on the LAN address (T17's).

## Q2 The credential's paths

The password and the token stay in `system.cfg` and the store; the ctl reads them for presence only. The username reaches argv at four sites (F-05) and the environment at one. The service's request log and the upload bundle redact `t=` and `p=` (`utils.py:110-124`); the bundle carries the account name and goes only on `upload_logs` being JSON `true` at the one automatic caller (patch 008); the usage report sends a salted hash of the name, only on consent (`usage_report.py:47-50`, `:180`). The port serves the token (F-01). `scan.log` takes the helpers' exception text; no credential-bearing message was found in the client's errors (`02` § The credential's paths).

## Q3 The writers

77 writing statements (`02` § The writers, generated). No script sets a mode; each file takes its writer's umask, read on the guest. Temp and rename everywhere a reader may race, except `verify-cursor` (F-09); `write_stamp`'s status ignored (F-07); the scan lock fails open (F-06); the fifo by name then object (F-10); the store written through `Storage()` by the listing (F-08); `es_export` writes `cached_game_ids.txt` by temp and `os.replace` (`es_export.py:58-69`).

## Q4 The bounds

`02` § The bounds, one row each. Enforced: the probe schedule, the stop wait, three in a row, the half hour, the top-up's 900 s, the image pass's 300 s, the refresh's 960 s, the badge wait, the batch cooldown. Not enforced: the scan's (F-11, by design: a foreground page with CANCEL, D-UI-078), the mark's write and its clock (F-12), the IDAT inflate and the lookup threads (F-13), the POST 429 pause (F-14). A kill is told from a result by its exit; an unreadable result is not (F-15).

## Q5 The patches

Eighteen, all absent from the pin and applying at fuzz 0: eleven fixes, six features, one identity (`02` § The patches). Ten have drafts, all on bases older than the pin; eight have none (F-22). The recipe's *"16 patches"* is the previous pin's count (F-21). A pin refresh (D-WORKFLOW-162): the cache holds fourteen revisions, the newest by date the pin's; what upstream did after `c7ebd1b6e7` is not readable without a fetch, so T19's answer is the procedure -- the integration test with the old pin as predecessor, `rc-preflight --only proxy-schema`, the suite -- and `NOT READ` for the upstream's later commits.

## Q6 What a failure reads as

`count_ready` prints 0 (F-16); one name fails the listing (F-17, reproduced); two usage exits (F-18); the refresh's `note()` on stdout and its `done` field (F-19, no reader); the recently played pass's `0 0 0` (F-15); the page's `have_account` comment (F-20).

## Q7 The protocol the interface reads

`02` § What T20 inherits: four producers, three on the `>>> ` protocol and `cache-indexed` on `OK`/`FAIL`/`DONE`; the stamps' shapes on both sides; the exit codes; the why tokens against `scanWhy`, which keeps a row for a token gone (F-20). T20 inherits the table, not an edit.

## Q8 The harness

`02` § The runs and the Positives table. `rc-preflight --only proxy-schema` is a comment check (F-23). `last-good-scripts-test` runs the real ctl in `bwrap` with shims; `raofflineproxy-integration-test` runs the shipped helper against the patched pin with a predecessor from the cache; the installed-native, consent and award tests are the guest's. The constructed positives: F-17's on the host (`tools/t19-listing-fixture.py`) and the guest; F-01, F-03, F-06, F-12 and F-16's on the guest. All six fell as read (`02` § Positives). The native test ran 18 with 4 failures on the image's M7 client (a lead outside the slice); the consent test passed 30 checks with no NIC; `ra-offline-test` could not run (D-RA-006).

## Second opinion

Phase 4.6 at Extended depth, two seats over one trimmed, scanned packet: GPT-6 Astra at `max`, then Gemini 4 Argon at `high` with the lane's grades of Astra. Not run yet; this section takes the plan, the provenance and every item's grade at stage C.

## Finding Verification

Each finding was read at its lines (`stage-b/reading-notes.md`); F-17 is reproduced by a fixture. The seats' refutations are graded against these at stage C.

## Renovation face

### Q1 Modernize
The two readers' parser is one (`CloudText`); the ctl's embedded python blocks (seven by word) are the shape a helper file would hold with a test of its own. F-08 is where the seam leaks.

### Q2 Standards
The temp-and-rename rule (D-CLOUD-078) holds but for F-09 and F-07; the credential rule holds but for F-05; guards fail closed but for F-06 and F-16.

### Q3 Bugs
F-01, F-03, F-06, F-07, F-16, F-17 (proposed Low).

### Q4 Package currency
The pin `c7ebd1b6e7` is upstream main at 2026-10-11 (the recipe's own comment); the siblings follow its submodules (F-21); later upstream commits are not read here (no fetch).

### Q5 Efficiency
F-13's unbounded inflate and threads; F-14's unpaced POSTs after a 429. The scan's listing parses each set row's head (`head_game_id`), not its body.

### Q6 Dead ends
`scanWhy`'s `NO_GAMES_FOUND` (F-20); the `refresh` and `images` verbs with no interface caller (F-19); the menu module shipped and never drawn (`package.mk:121-124` removes its fonts and images, not the module).

### Q7 Clarity and structure
The recipe's comment (F-21); `count_ready`'s comment against its code (F-16); the refresh's two meanings of `done` (F-19).

## Instruction File Recommendations

### Coverage gaps (would have prevented)
- A scan of a loopback service's request path for an answer that carries a credential to a caller that proved none (F-01) belongs beside the read filter in `engineering-practices.md`.

### Codification gaps (proposals for the coordinator)
- `last-good-scripts-test`'s bubblewrap shape for the ctl is the way to run a fork script on the host; the brief's "never on the host" could name it.

## Quality self-check

- Every finding cites lines at `8ebaf8daad` or the patched pin; one claim corrected before it was committed (`03`'s routing sentence: `setsettings.sh` checks `127.0.0.1:8080` only).
- No credential value was read: the store, `system.cfg` and the QA account file are unread; the scan of the reading notes for a credential-shaped value found 0.
- The severities are proposals for the stage-D ruling.
