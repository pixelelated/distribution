# Retrospective audit — M6.P2 T19, the offline achievements proxy (#666)

The proxy against its own record: the epic audit `docs/audits/2026_09_14-epic-offline-retroachievements/` (#186), the fix rounds #307 and #308 its comments and patches cite, and the decisions D-RA-001 to D-RA-048. Read at `8ebaf8daad`; the upstream at its pin, patched (`02`).

## 3.1 Architectural coherence

- **One door.** The ctl is the OS's and the interface's one way to the proxy (enable, disable, the answers, the scan, the top-up), and every answer the interface reads is a last line or a stamp it parses in `CloudText` (`02` § What T20 inherits). The shape held across nineteen rounds of change: 99 commits, 2026-09-13 to 2026-10-14.
- **What runs where.** The service is upstream's, patched; the four scripts are the fork's. The seam between them is the store: the ctl reads it read-only through its own `sqlite3` calls -- except `list_jobs`, which opens it through the client's `Storage()` (F-08). One rule, held almost everywhere.
- **The fork's lanes.** Every patch is in a lane the fork works (D-UI-079): the cards, the scan, the images, the sign-in, the consent. None changes how awards are signed or queued.

## 3.2 Project conformance

- **Guards fail closed** (`engineering-practices.md`): `cannot_tell` (exit 2, nothing on stdout) for every store read the interface acts on; `added=unknown` rather than a count (PL-031); `as_flag` for every setting. Two exceptions read in the tree: `count_ready`'s 0 (F-16) and the scan lock's `|| return 0` (F-06).
- **The last known good state** (D-CLOUD-078): `last-scan`, `running`, `index-pending`, `scan-cursor`, `absent` and the service's `last-flush` and `cached_game_ids.txt` are written whole by temp and rename. `verify-cursor` is not (F-09), and `write_stamp`'s status is ignored (F-07).
- **A credential never on a command line**: the file states it (`:1244-1246`) and follows it once (`:1265`); four python calls pass the username on argv (F-05). The token and the password are never read into a variable by the ctl.
- **Every fix answers what was already written** (`upgrade-and-install.md`): the integration test's upgrade case reopens the predecessor's store with current `Storage` and keeps its bytes (`stage-a/unpack.txt`).

## 3.3 Spec fidelity

- **D-RA-001, D-RA-002** (one system-wide toggle, casual only, hardcore switched with the sentence on screen): `do_enable` records hardcore once, turns it off, sets the toggle last, and undoes every step on a failure; `do_disable` puts it back from the record (`02`). Held.
- **D-RA-004, D-UI-095, D-UI-101** (the cards at the link's return): the `flushed` stamp taken by rename, once per flush (patch 003, ctl `do_flushed`). Held.
- **D-RA-010, D-RA-013** (the scan and the index): the I and H job shapes, the index rule per system, the cursor (#307 PL-059). Held; F-17 is the walk's one input that fails the whole listing.
- **D-RA-016, D-WORKFLOW-164, -165** (whatever the fork changes in the proxy goes back; not sent until the build): ten drafts, none sent; eight patches without one (F-22).
- **#186 PL-12** (the storage-corruption upload opt-in): patch 008 gates the one automatic caller (`proxy_service.py:1477`); the manual upload is in `menu_sdl.py`, which the image never draws. Held.

## 3.4 Platform conformance

- **The unit** carries the fork's start-up contract (`ExecStartPost` waits for the listener; five starts in 300 s) and no hardening directive (F-04): every other directive is the defaults'. T22's table of the other units is compared at stage C.
- **The busybox shell** is not the ctl's: it is `#!/bin/bash` and the recipe depends on `bash`, `coreutils` (`timeout`) and GNU `grep` (#308 F-RA-23, F-RA-24); `last-good-scripts-test` runs it under the donor's busybox applets in `bwrap` (1,379 PASS).

## 3.5 Cross-system interaction audit

### Interaction: the ctl x EmulationStation (T20's, T2's)
The interface calls `pending`, `flushed`, `account`, `summary`, `pending-ids`, `topup`, `index-offline`, `scan` and `enable`/`disable` at the pin; never `refresh` or `images` (F-19). Every reader parses the producer's shape in `CloudText`; one reader row has no producer (F-20). `stopRun` signals the flock's holder found by `/proc/<pid>/fd` (`OfflineAchievements.cpp:339-358`); the ctl writes its pid into the lock for that (`take_lock`).

### Interaction: the port x the launch scripts (T1's)
`setsettings.sh:532-545` routes RetroArch to 8080 only when the toggle is 1, hardcore 0 and `netstat -ltn` shows a listener on `127.0.0.1:8080 ` (:536). That is a different check from the ctl's: it takes any owner on `127.0.0.1:8080` but not `0.0.0.0:8080`, which the ctl's `port_listening` takes. So a foreign `0.0.0.0` listener satisfies `enable` and the unit's start, and every launch then goes direct (F-03).

### Interaction: the port x `cloud_oauth`'s serve (T17's)
Both take 8080; the suite's case holds that the serve comes up on the LAN address with the proxy on loopback. F-01's answer is readable to a web page only by DNS rebinding (F-02), and the sign-in window opens a provider's page only.

### Interaction: the store x `backuptool` (T17's)
`/storage/.config/raofflineproxy/` is a DEVICEONLYDIRS entry: the store, the token row and the queue never travel in a settings backup; the toggle in `system.cfg` does, and `daemons/006` re-derives the marker at boot.

### Interaction: the service x RetroArch's command patch (T3's #825)
With the toggle on, an achievement's title and description reach RetroArch from this store; T3's PL-032 is that patch's half. Nothing here changes it.

### Interaction: M7's open work on these files
None read: M7's worktrees are not this lane's (the brief's § 1).
