# T13 forward audit: the cloud test harness (#660)

Phase 2 over #660's checklist, the nine tools at `8ebaf8daad`'s bytes. Stage A
wrote § The runs; stage B § Coverage, § Assertion shapes, § Positives and
§ Proofs; § The guest cycle is written in the window granted on #660.

## Coverage

One row per path. *Oracle* is what decides the tool's PASS; *caller* is
who runs it (`grep -n` of `tools/vm-qa`, the other eight, and `.github/`).

| Path | Lines | Subject | Oracle | Caller | Positive (§ Positives) | proved: |
| --- | ---: | --- | --- | --- | --- | --- |
| `tools/cloud-round-trip` | 7,808 | the cloud scripts on a guest, over SSH, against a QA endpoint | 24 rows read both ends, 8 the device's report, 46 a planted input (§ Assertion shapes, after the seat) | `vm-qa` `round-trip` (single-device suite) and `link` (LINK1-7); the other registries by hand | refused SSH port: rc 2, `FAIL  no shell over ssh` | tool-run |
| `tools/cloud-test-backend` | 920 | five local endpoints and a dead port | it is the endpoint; `cat` checks existence first | `vm-qa`, `cloud-round-trip` | `cat no/such/object`: rc 1 on WebDAV, SFTP and S3 | tool-run |
| `tools/cloud-connections-test` | 307 | `cloud_connections` (staged connection transactions) | the module itself, under the **host's** rclone | nobody | the duplicate-name refusal defeated: `FAIL: test_duplicate_keeps_old_bytes`, rc 1 | fixture |
| `tools/cloud-census` | 306 | a handheld's `/storage` and logs over SSH | reading only | nobody | none: a handheld-only tool, never run (D-QA-015) | design |
| `tools/cloud-pair-migration` | 243 | two guests across `cloud_migrate_layout` | -- | nobody | none: exits 2 before anything on every tree after `e6645cb5ea` | tool-run |
| `tools/cloud-save-integrity` | 219 | manifests and save containers (D-CLOUD-181) | its sibling test's synthetic corruption, and rclone's Dropbox hash | nobody | its test's 17 rejection checks (stage A, `PASS total=24`; G-52) | tool-run |
| `tools/cloud-input-test` | 132 | `wifictl` under shims, `cloud_oauth` under `node` | the scripts themselves under **host** bash and coreutils | nobody | a `wifictl` that exits 0 doing nothing: 6 `FAIL`, rc 1; its own negative control (old `cloud_oauth`) | fixture |
| `tools/cloud-capture-stamp-test` | 116 | `cloud_capture`'s `finish()`, lifted by `sed` | its documented control (`f451252587`), under **host** bash | nobody (CAP12 mirrors it on a guest) | `f451252587`'s `cloud_capture`: rc 1, 8 FAIL | tool-run |
| `tools/cloud-save-integrity-test` | 114 | `cloud-save-integrity` | a second implementation: rclone's `hashsum Dropbox` | nobody | the provider-hash comparison defeated: rc 1, `FAIL changed payload rejected` | fixture |

## Assertion shapes

One row per `step()` of the single-device suite (`run_steps`, 32, and `prepare_device`, 2) and per registry cell (PAIR 10 with `RETENTION`, SOLO 1, CAP 14, LINK 7, KILL 12: 44), plus `CONTRACT`. The table is generated, never typed:

```bash
git show 8ebaf8daad:tools/cloud-round-trip > /workspace/tmp/m6-t13/cloud-round-trip.8ebaf8daad
python3 -I -B docs/audits/2026_10_25-epic-m6-cloud-harness/tools/t13-shapes.py /workspace/tmp/m6-t13/cloud-round-trip.8ebaf8daad --json .qa-scratch/t13/shapes.json
#   {"steps": 34, "cells": 44, "rows": 78, "by_oracle_rule": {"both ends": 25, "device report": 11, "synthetic": 42}, "deltas": []}   rc 0
python3 -I -B docs/audits/2026_10_25-epic-m6-cloud-harness/tools/t13-render.py .qa-scratch/t13/shapes.json docs/vm-qa-log.md
```

- **The generator asserts the counts against the AST and the registry literals.** It checks 32 + 2 `step()` calls in their two functions and 10/1/14/7/12 entries in the five registries, and exits 1, naming the delta, on another revision. At the hash there is **no delta**.
- **`CONTRACT`** is the one difference from the coordinator's figures. `--list` prints it as a 45th line, but it is not a registry cell: it is #9's transport contract, run with `--only CONTRACT` or `--transport`. It has a row of its own, marked, so the count below is **79** = 78 + `CONTRACT`.
- **The oracle column's rule, in this precedence:**
  1. *Both ends*: the row reads the endpoint from the host, by `backend('ls')`/`backend('cat')`, a host run of the tool, `Pair.cloud_sha` (a host `cat`), or a `Link.exercise` whose receiving side is `("cloud", …)`.
  2. *Synthetic input*: otherwise, the row plants its condition (a stub on `PATH`, a held lock, a kill, a link or power cut, a put at the endpoint, a config edited under the scripts) and reads the device's reaction.
  3. *The device's report*: otherwise, the device's own exit, output, log, stamp or files, including a round trip through its own restore.
- **The lane's review overrode 11 rows,** each marked `(reviewed)` with its reason in the Note column. Five of those overrides came from the seat's refutation (G-3, G-6, G-7, G-8): A3, `prepare_device.2` and step 30 became synthetic, KILL1 and step 32 both ends. KILL4 is conditional and A5's device-rclone reads are counted by hand. The first cut said "eight overrides" while only six rows showed the mark (the seat's G-1).
- **`caps()` column:** the keys the row's code reads.
- **Recorded verdict:** the newest `docs/vm-qa-log.md` row naming the cell or its registry's range, cited by date and line and never summarised. The 34 steps share the suite's one verified line.
- **Device-rclone reads:** the device's own `rclone lsf`/`cat`/... of the remote. That reads the other end, but through the client under test.

| Row | Lines | Claim | Oracle | Device-rclone reads | `check()` | `caps()` | Recorded verdict | Note | proved: |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| `run_steps.1` | 625-631 | plant fixtures | synthetic | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.2` | 632-671 | saves back up to the cloud | both ends | 0 | 3 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.3` | 672-707 | a second backup replaces several saves at once | device report (reviewed) | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | a round trip: the device's own restore reads the second backup back; no host read of the endpoint | tree |
| `run_steps.4` | 708-721 | saves restore from the cloud | device report (reviewed) | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | a round trip: local copies removed, the device's own restore, bytes compared on the device | tree |
| `run_steps.5` | 722-787 | the settings archive round-trips | both ends | 0 | 6 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.6` | 788-814 | a changed archive of the same size still reaches the cloud | device report (reviewed) | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | a round trip through the device's own settings backup and restore | tree |
| `run_steps.7` | 815-910 | retention removes only archives carrying this device's name, and restore prefers them | synthetic | 1 | 8 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.8` | 911-945 | ROMs and BIOS back up a system directory | both ends | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.9` | 946-967 | a user's own rule sits above the catch-all and keeps its file off the cloud | synthetic | 1 | 3 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.10` | 968-1008 | an edited RCLONEOPTS without --filter-from still keeps the allowlist | synthetic | 2 | 5 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.11` | 1009-1069 | the transfer lock is free the moment a run returns, and no child of a run can hold it | synthetic | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.12` | 1070-1099 | a settings-only backup with nothing on the device to send is skipped, and says so once | device report | 0 | 3 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.13` | 1100-1140 | folder choices are independent; discovery preserves those choices | synthetic | 1 | 5 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.14` | 1141-1200 | a cloud with no saves folder yet is empty, not broken; a wrong root still fails | synthetic | 0 | 5 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.15` | 1201-1234 | ROMs and BIOS restore it | synthetic | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.16` | 1235-1266 | --all restores every system and BIOS, each a unit of its own | synthetic | 0 | 4 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.17` | 1267-1286 | a save file inside a system directory does not reach the ROMs and BIOS tier | both ends | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.18` | 1287-1317 | a sync-conflict artifact is carried by no tier, in either direction | both ends | 0 | 4 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.19` | 1318-1362 | gamelist.xml moves with game content, newest-first, in its own pass | both ends | 0 | 5 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.20` | 1363-1389 | a second cloud sync while one runs is refused, exits 75, and stamps nothing | synthetic | 0 | 8 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.21` | 1390-1406 | a --recent sync with nothing changed leaves the remote alone | device report | 0 | 4 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.22` | 1407-1419 | a --recent sync after one save is written pushes that file | both ends | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.23` | 1420-1459 | a changed save of the same size still reaches the cloud (#315) | both ends | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.24` | 1460-1479 | with no network the exit sync returns 69 at once and stamps nothing | synthetic | 0 | 7 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.25` | 1480-1496 | every EmulationStation system path is carried by exactly one tier | device report | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.26` | 1497-1551 | the settings archive is a tar archive named for this device, and every reader finds it | synthetic | 0 | 5 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.27` | 1552-1596 | content transfers honour the system selection | both ends | 0 | 5 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.28` | 1597-1644 | a system this device cannot run is marked unsupported | synthetic | 0 | 4 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.29` | 1645-1673 | a scan the cloud refused exits with rclone's code and lists nothing | synthetic (reviewed) | 0 | 3 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | the dead-port stanza is planted (backend dead-conf); the scan's exit and rows are the device's | tree |
| `run_steps.30` | 1674-1693 | seeding is idempotent and never clobbers an existing note | synthetic (reviewed) | 0 | 3 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | the harness writes README.txt itself and reads that same path back; a no-op seeder passes (the seat, G-7) | tree |
| `run_steps.31` | 1694-1713 | an older config's keys are carried across (D-UI-022, A12) | synthetic | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.32` | 1714-1716 | one last-known-good of every record, and no writer's litter, after the suite | both ends (reviewed) | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | litter_scan() reads the endpoint (6129-6153) (the seat, G-8) | tree |
| `prepare_device.1` | 309-317 | f'device {which}reachable and equipped | device report | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `prepare_device.2` | 318-383 | f'point device {which}at the QA bucket' if which else 'point the device at the QA bucket | synthetic (reviewed) | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | setup: writes the QA stanza and selection, then checks the active name; certifies neither connectivity nor a transfer (the seat, G-6) | tree |
| `A1` | 1972-1999 | both changed after a first pass: every writer, this device's copy newer and older | both ends | 0 | 2 | not read | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A2` | 2002-2043 | a failed push retried; an equal-size, equal-mtime change after a first pass | both ends | 0 | 3 | not read | none recorded |  | tree |
| `A3` | 2046-2082 | CHANGE CLOUD FOLDER to a folder holding different saves | synthetic (reviewed) | 0 | 4 | not read | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) | the endpoint hash at 2063 checks the second folder's setup; every outcome check (2073-2078) is local (the seat, G-6) | tree |
| `A8` | 2085-2144 | a torn N64 pair: interrupted after one member, held, then cleared | both ends | 0 | 4 | not read | none recorded |  | tree |
| `A9` | 2147-2252 | delete and renumber; a retired hash put back; rm; an unmounted, empty, or empty-cloud root | both ends | 0 | 19 | not read | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A11` | 2255-2277 | a cloned device id refuses to publish | both ends | 0 | 2 | not read | none recorded |  | tree |
| `A12` | 2280-2318 | a legacy RESTOREPATH unlike BACKUPPATH: migrated, warned, nothing touched | synthetic | 0 | 9 | not read | none recorded |  | tree |
| `A14` | 2321-2377 | the manifest step: under savestates/.rocknix/, sha256, remote_hash per backend, one tier | both ends | 0 | 5 | hash | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A5` | 2380-2417 | the discarded-saves reader, from the second device | device report (reviewed) | 2 | 3 | not read | none recorded | the reader is device b's own rclone (lsf, cat); FAILS by construction: APPLY calls cloud_reconcile, which has never existed (line 1771) | tree |
| `RETENTION` | 2420-2455 | the retention ordering: killed after the loser is stored, before the winner replaces | both ends | 0 | 4 | not read | none recorded | FAILS by construction (cloud_reconcile, line 2433); when nothing ran, its head-unchanged and device-copy checks PASS vacuously | tree |
| `A15` | 2530-2990 | the seed is a MAC or nothing: sit0 and a macvlan are refused, a poisoned id heals once, the working copy and the next backup follow it, its old folder | synthetic | 1 | 36 | not read | none recorded |  | tree |
| `CAP1` | 3243-3333 | capture on every exit: lock held, no route, no rclone, nothing written into the tree | synthetic | 0 | 19 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 3 row(s)) |  | tree |
| `CAP2` | 3336-3372 | the recorded core is the argument, never a default | synthetic | 0 | 6 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP3` | 3375-3449 | the seal is an independent copy; a hard link fails; the seal guard fires | synthetic | 0 | 8 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP4` | 3452-3518 | nothing changed, nothing rewritten -- in all three modes (I8) | synthetic | 0 | 7 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP5` | 3521-3556 | core_build is the pin for the core's package; unmapped is unknown | synthetic | 0 | 9 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP6` | 3607-3678 | a unit is what the emulator writes: members, decoys, subfolders, and both N64 layouts | synthetic | 0 | 11 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP7` | 3681-3877 | a renumber is a move, a deletion is a retired record, and nothing is invented | synthetic | 0 | 29 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP8` | 3880-3966 | nothing is stamped that this session did not write; the A2 shape; --full's limits | synthetic | 0 | 12 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP9` | 3969-4113 | the error policy is the one written down, and the un-provable is not faked | synthetic | 0 | 19 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP10` | 4154-4245 | the card context informs, it never silently refuses -- and a flip discards | synthetic | 0 | 12 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 3 row(s)) |  | tree |
| `CAP11` | 4248-4314 | two writers of one manifest: the loser re-runs once and a first version is not lost | synthetic | 0 | 6 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 2 row(s)) |  | tree |
| `CAP12` | 4317-4388 | last-capture keeps one line per mode: an exit survives the boot pass; the old one-line stamp is read | synthetic | 0 | 9 | not read | named 2026-09-17 (`vm-qa-log.md:102`; 3 row(s)) |  | tree |
| `CAP13` | 4391-4457 | --retire --unlink is the manager's deletion as one unit: row, then files, SIGTERM ignored; a path outside the saves folder is refused the rm | synthetic | 0 | 6 | not read | named 2026-09-24 (`vm-qa-log.md:127`; 4 row(s)) |  | tree |
| `CAP14` | 4460-4524 | --adopt records the copy the manager made: the source's version at the new path, or unknown provenance | synthetic | 0 | 7 | not read | named 2026-09-24 (`vm-qa-log.md:127`; 4 row(s)) |  | tree |
| `LINK1` | 5609-5619 | saves restore (the startup sync's command), link cut during the compare | synthetic (reviewed) | 0 | 0 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) | the seed is checked at the endpoint (backend_sizes); the cut's verdict is the device's receiving side; its checks are Link.exercise's, shared by every LINK cell | tree |
| `LINK2` | 5622-5627 | saves backup, link cut during the transfer | both ends | 0 | 0 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) | its checks are Link.exercise's, shared by every LINK cell | tree |
| `LINK3` | 5630-5636 | ROMs and BIOS backup, link cut during the transfer | both ends | 0 | 0 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) | its checks are Link.exercise's, shared by every LINK cell | tree |
| `LINK4` | 5639-5645 | ROMs and BIOS restore, link cut during the transfer | synthetic | 0 | 0 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) | its checks are Link.exercise's, shared by every LINK cell | tree |
| `LINK5` | 5648-5679 | settings archive upload (backuptool backup; cloud_backup --system-only), link cut mid-upload | both ends | 0 | 0 | not read | named 2026-09-13 (`vm-qa-log.md:80`; 6 row(s)) | its checks are Link.exercise's, shared by every LINK cell | tree |
| `LINK6` | 5682-5690 | the exit sync (cloud_backup --yes --saves-only --recent), link cut during the transfer | both ends | 0 | 0 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) | its checks are Link.exercise's, shared by every LINK cell | tree |
| `LINK7` | 5693-5717 | the picker scan (cloud_content_restore --scan), link cut mid-scan | synthetic | 0 | 0 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 4 row(s)) | its checks are Link.exercise's, shared by every LINK cell | tree |
| `KILL1` | 6771-6855 | saves backup killed mid-transfer, SIGKILL then SIGTERM: cloud holds v1 or whole v2, stamp never 0, lock released, re-run completes | both ends (reviewed) | 0 | 13 | commit | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) | its cloud fingerprints are host ls/cat (6811-6825); but it cannot complete: `webdav` is undefined at 6846 (NameError, G-30), and an absent file is not counted torn (G-35) | tree |
| `KILL2` | 6858-6956 | saves restore stopped mid-download by ES's TERM-then-KILL (D-CLOUD-076): the game's save stands, *.partial litter, re-run keeps the previous version | synthetic | 0 | 15 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL3` | 6975-7019 | backuptool backup killed mid-rotation: the previous archive is still what both readers find | synthetic | 0 | 10 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) |  | tree |
| `KILL4` | 7021-7070 | backuptool backup killed mid-tar: no truncated archive under a final name, nothing invalid uploaded | both ends | 0 | 9 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) | conditional: run alone it is prepared locally and skips the upload half; with an endpoint it reads both ends; its invalid-upload check is absence-only (F-12, G-8) | tree |
| `KILL5` | 7073-7159 | settings upload killed mid-copyto: marker, retention and device.json untouched; the re-run trims only this device's | both ends | 0 | 16 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL10` | 7162-7202 | set_setting killed mid-sed: the value stands, the temp is litter, the stale lock clears | synthetic | 0 | 5 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL11` | 7205-7235 | set_setting killed between delete and add: the previous value is not lost | synthetic | 0 | 3 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL12` | 7251-7352 | chksysconfig at boot with an empty, truncated, valid or binary system.cfg (power cut), and the clean-shutdown record | synthetic | 0 | 5 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL13` | 7375-7512 | es_settings.cfg and system.cfg power-cut through ES's own writers (arm A), and planted torn files at boot (arm B) | synthetic | 0 | 5 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) |  | tree |
| `KILL15` | 7515-7540 | an empty saves-root record refuses instead of reading as none | synthetic | 0 | 7 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL16` | 7543-7577 | content-systems: a kill before the write keeps the selection; an empty file is legal, so the writer must verify | synthetic | 0 | 3 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL18` | 7580-7659 | backuptool restore killed mid-extract: the tree is half restored and the pre-restore state kept nowhere | synthetic | 0 | 10 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `CONTRACT` | 4617-5128 | #9's transport contract under the reconciler (--transport copy,bisync) | both ends | 3 | 16 | not read | none recorded | not a registry cell: --list prints it beside PAIR; the Transport class reads the endpoint by cloud_sha (8) and backend_files/bytes (3) | tree |

Rows: 78 (34 steps + 44 cells) + `CONTRACT` = 79. By oracle over the 78: both ends 24, device report 8, synthetic 46.

**The class whose oracle is the device's own report: 8 rows** (after the seat's grading; 10 at stage B).

- **Round trips through the device's own restore:** `run_steps.3`, `.4` and `.6`.
- **The device's summary, log and ES paths:** `run_steps.12`, `.21` and `.25`. Step 25 PASSes on an empty probe (G-33).
- **Setup:** `prepare_device.1`.
- **Device b's own rclone:** `A5`, which fails by construction.

None of these reads the endpoint from the host, so a PASS on them certifies what the device says, through the code under test. The seat adds that step 5's restore half and A2's equal-size half have device-side verdicts inside rows classed both ends (G-2). Four more rows read the remote with the device's own rclone and are classed by their other evidence: `run_steps.7`, `.9`, `.10` and `.13` (both device-rclone and planted), plus `A15` and `CONTRACT`.

**`caps()` marks nothing in the single-device suite.** It is read at three call sites in the file: twice in A14's helper (`hash`, lines 2369-2373) and once in KILL1 (`commit`, line 6786). None of the 34 steps reads it, so the suite runs the same assertions on every backend and marks no step, which is a Q2 finding (04). The tool's header line 21, *"nothing is skipped in silence"*, is true of the suite only because nothing is skipped at all.

**No recorded verdict: 8 rows.** `A2`, `A8`, `A11`, `A12`, `A5`, `RETENTION`, `A15` and `CONTRACT` have no `docs/vm-qa-log.md` row naming them. A5 and RETENTION could not pass on any tree since the fixtures were written: `APPLY` (line 1771) calls `cloud_reconcile`, and `git log --all --diff-filter=A -- '*cloud_reconcile'` is empty.

## The runs

All on the build host, 2026-10-25 05:00-05:01 UTC, in the worktree, with
`TMPDIR=/workspace/tmp/m6-t13/tmp`. Raw outputs are under `.qa-scratch/t13/`
(gitignored). Wall times are `date +%s.%N` differences around each command.
The host's rclone is `rclone v1.60.1-DEV`.

### The four bare tests, the documented positive, the retired tool

| Run | Command | Exit | Wall | What it printed | A FAIL would mean ... | proved: |
| --- | --- | ---: | ---: | --- | --- | --- |
| `cloud-connections-test` | `tools/cloud-connections-test` | 0 | 1.9 s | `Ran 26 tests in 1.864s` / `OK` (26 `... ok` lines) | the connection module's staged transactions, its rclone-state handling or its shutdown cleanup diverged from a case, as judged by the module itself and the **host's** rclone (not the image's) | tool-run |
| `cloud-input-test` | `tools/cloud-input-test` | 0 | 1.0 s | `Ran 9 tests in 0.964s` / `OK` (9 `... ok` lines) | `wifictl` under `bwrap` with shimmed `nmcli`/`iwctl` (host bash, host coreutils) or `cloud_oauth` under the host's `node` broke one of its cases | tool-run |
| `cloud-capture-stamp-test` | `tools/cloud-capture-stamp-test` | 0 | 0.1 s | 14 `PASS` lines, `PASSED` | `cloud_capture`'s `finish()`, lifted by `sed` and run under the **host's** bash with `date` faked, no longer keeps one line per mode | tool-run |
| its documented positive | `git show f451252587:.../cloud_capture > $TMPDIR/old-cloud_capture; tools/cloud-capture-stamp-test $TMPDIR/old-cloud_capture` | **1** | 0.1 s | 6 `PASS`, 8 `FAIL`, `8 CHECK(S) FAILED` (first: `the old exit line is gone: last-capture: 1 line(s)`) | -- this is the FAIL: the pre-fix `finish()` overwrites the stamp with one line, and the test sees it | tool-run |
| `cloud-save-integrity-test` | `tools/cloud-save-integrity-test --rclone "$(command -v rclone)"` | 0 | 0.1 s | 24 checks (`PASS total=24`; 25 lines start `PASS`, the last being the total): 19 rejection and structure cases, 5 `Dropbox oracle` sizes (0, 4194303, 4194304, 4194305, 8388625) | the verifier accepted a corrupt, truncated, unsafe or changed packet, or its Dropbox content hash disagreed with rclone's (the one second implementation among the nine) | tool-run |
| `cloud-pair-migration` | `tools/cloud-pair-migration /nonexistent/a.img.gz /nonexistent/b.img.gz /nonexistent/c.tar` | **2** | 0.00 s | `This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manual cloud setup.` | -- it cannot FAIL on this tree: it refuses before anything (lines 58-63), keyed on `cloud_migrate_layout`'s absence | tool-run |

**The brief's counting line counts nothing here.** § 5 counts
`grep -c -E '^(PASS|ok)'`. The two unittest tools print `... ok` at the line's
end and `OK` alone, and the stamp test indents its `PASS`, so that grep reads
0, 0 and 1 for runs whose real counts are 26, 9 and 14. The counts above are
`grep -c -E ' \.\.\. ok$'` and `grep -c -E '^\s+PASS'`.

### The backends: up, ls, cat of a missing object, down

**Isolation, by the tool's own parameters:** `CLOUD_QA_STATE=/workspace/tmp/m6-t13/state`,
`CLOUD_QA_PORT` 9080 / 9083 / 9082, `CLOUD_QA_NAME=rocknix-cloud-qa-m6t13`,
`CLOUD_QA_S3_UPSTREAM_PORT=9092`. The reason is that `down` kills every
listener on its port (lines 565-591) and the M7 lane runs guests on this host.
Before the runs nothing listened on 9010-9099 and no QA container existed.
Each backend got one object by `put` first, so that `ls` and `cat`'s
present case have something to read.

| Backend | `up` | `ls` | `cat` of the put object | `cat no/such/object` | `reset` | `down` | `status` after | A FAIL would mean ... | proved: |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WebDAV `:9080` (`rclone serve webdav`) | rc 0, 0.0 s | rc 0, `6 t13/probe.txt` | rc 0, 6 bytes | **rc 1**: `cat: <state>/data/no/such/object: No such file or directory` | rc 0 | rc 0, 0.1 s, `down` | `not running`, rc 1 | the endpoint did not start, could not list, reported a missing object as present (blindspot 22/31), or left its listener up | tool-run |
| SFTP `:9083` (unprivileged sshd) | rc 0, 0.1 s; `note: this sshd cannot chroot unprivileged, so the remotes are absolute` | rc 0, `6 t13/probe.txt` | rc 0, 6 bytes | **rc 1**: `cat: <state>/sftp/data/no/such/object: No such file or directory` | rc 0 | rc 0, 0.1 s | `not running`, rc 1 | the same | tool-run |
| S3 `:9082` (MinIO container) | rc 0, 1.6 s | rc 0, `6 t13/probe.txt` | rc 0, 6 bytes | **rc 1**: `cat: no such file at the endpoint: no/such/object` (the existence check of lines 650-653; bare `rclone cat` of a missing key exits 0 on MinIO) | rc 0 | rc 0, 0.3 s | `not running`, rc 1 | the same; on S3 specifically, that the existence check stopped standing between `cat` and MinIO's exit-0 on a missing key | tool-run |

**Nothing left running** (05:01 UTC): `ss -ltn` shows 0 listeners on
9010-9099; `docker ps -a` shows 0 containers named `rocknix-cloud-qa*`;
`pgrep -f` for `rclone serve webdav`, `sshd -f /workspace/tmp/m6-t13` and
`minio server` finds no process other than the checking shell.

**For Q4, the images `up` would use, as resolved on 2026-10-25** (local,
nothing pulled; `docker image inspect`):

- `quay.io/minio/minio:latest` is `sha256:14cea493d9a3...`, created
  2025-09-07, label `version=RELEASE.2025-09-07T16-13-09Z`.
- `dperson/samba:latest` is `sha256:66088b78a198...`, created 2020-07-03.
- pyftpdlib is not resolved: FTP was not brought up at stage A.

**The argument order (a lead for stage B).** The option loop (lines 57-63)
stops at the first non-option, so a `--backend` after the subcommand is
ignored and the tool answers for the default (WebDAV) with rc 0.

```
tools/cloud-test-backend port --backend sftp    -> 9010 rc=0   (WebDAV's)
tools/cloud-test-backend --backend sftp port    -> 9013 rc=0
tools/cloud-test-backend caps --backend s3      -> hash=none modtime=no commit=partial bucket=no   (WebDAV's)
tools/cloud-test-backend --backend s3 caps      -> hash=md5 modtime=yes commit=atomic bucket=yes
```

The brief's § 5 loop writes `up --backend "$b"`; run as written, it would
have brought up WebDAV three times and called that WebDAV, SFTP and S3.

### The harness without a device

| Run | Command | Exit | Wall | Result | A FAIL would mean ... | proved: |
| --- | --- | ---: | ---: | --- | --- | --- |
| `--list` | `tools/cloud-round-trip --list` | 0 | 0.1 s | 55 lines, **45 cells**: two-device 11 (PAIR's 10 with `RETENTION`, plus `CONTRACT`), single-device 1 (A15), CAP 14, LINK 7, KILL 12 | the registries failed to load or print without a device | tool-run |

The brief's `grep -c -E '^(A|CAP|LINK|KILL)[0-9]'` reads 0, because every
cell line is indented two spaces; the count is `grep -c -E '^  [A-Z]'`.

### Four descriptions of one suite

| Where | Says | proved: |
| --- | --- | --- |
| `tools/vm-qa:36` | `round-trip  tools/cloud-round-trip  -- 27 steps over SSH against the QA cloud` | tree |
| `tools/cloud-round-trip` (AST) | 32 `step()` in `run_steps`, 2 in `prepare_device`, 46 in the file; 460 `check()` calls | tree |
| `docs/vm-qa-log.md:175` (2026-10-06) | `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP;318 total` | history |
| `docs/work-logs/2026_10-work_logs/2026_10_08-work_log.md:111` | `Both ordinary VM round trips already passed 108` | history |

A FAIL here would mean the four agree, and they do not. Which one a PASS line
certifies is stage B's question (Q7), answered from the tool's own summary
line in the guest cycle.

## Positives

One row per tool: the input constructed to make it FAIL, the command, and the FAIL observed. Run on the host, 2026-10-25 05:12-05:13 UTC (the outputs' mtimes). The sabotaged copies live in scratch trees under `/workspace/tmp/m6-t13/pos/`; the worktree is unchanged (`git status` shows no file under `tools/` or `projects/`).

| Tool | Constructed input | Command | FAIL observed | proved: |
| --- | --- | --- | --- | --- |
| `cloud-round-trip` | a device that does not answer: SSH port 1 (refused), no key | `CLOUD_QA_STATE=/workspace/tmp/m6-t13/state tools/cloud-round-trip --host root@127.0.0.1 --port 1 --identity /nonexistent/qa-key` | rc 2 in 0.1 s: `FAIL  no shell over ssh`, then `error: no shell over ssh on root@127.0.0.1 port 1`; nothing left listening on 9010-9099. A step's own FAIL against a working guest waits for the window (§ The guest cycle). | tool-run |
| `cloud-test-backend` | an object that is not there | `--backend <b> cat no/such/object` (§ The runs) | rc 1 on WebDAV, SFTP and S3; S3's is the existence check of lines 650-653 | tool-run |
| `cloud-connections-test` | `cloud_connections.py` line 147's duplicate-name refusal defeated (`if False and replace != exists:`) in a scratch copy of the sources | `cd /workspace/tmp/m6-t13/pos/conn && python3 -I -B tools/cloud-connections-test` | rc 1: `FAIL: test_duplicate_keeps_old_bytes`, `FAILED (failures=1)` of 26: exactly the one case that names the guard | fixture |
| `cloud-census` | none | -- | none: it reads a handheld over SSH (`--host root@192.168.1.81`) and is never run in this slice (D-QA-015); it asserts nothing, so it has no FAIL to construct | design |
| `cloud-pair-migration` | none | -- | none: it refuses with rc 2 before any input on every tree after `e6645cb5ea` (lines 58-63), so no input reaches a check | tool-run |
| `cloud-save-integrity` | its sibling test's corrupt, truncated, unsafe and changed packets | `tools/cloud-save-integrity-test --rclone /usr/bin/rclone` (§ The runs) | its 17 rejection checks are the verifier refusing a constructed bad input (`PASS ... rejected` = the verifier's FAIL path taken); of the 19 pre-oracle checks, one is the valid packet and one the raw-semantics case (the seat's G-52 corrects the first cut's 19) | tool-run |
| `cloud-input-test` | a `wifictl` that does nothing and exits 0, in a scratch tree | `cd /workspace/tmp/m6-t13/pos/input && python3 -I -B tools/cloud-input-test` | rc 1, 6 `FAIL:`: all six `Wifi` cases. The three `Phone` cases run the unchanged `cloud_oauth` under `node`; two pass. Its own negative control `test_original_source_negative_control` ERRORed **because of the scratch tree, not the sabotage**: it runs `git show a1b0c65165:...` with `cwd=ROOT`, and the scratch tree is no checkout (exit 128). In the worktree that control passes (stage A, 9 OK). | fixture |
| `cloud-capture-stamp-test` | `cloud_capture` before its fix, `f451252587` | `tools/cloud-capture-stamp-test $TMPDIR/old-cloud_capture` (§ The runs) | rc 1: 8 FAIL, `8 CHECK(S) FAILED` | tool-run |
| `cloud-save-integrity-test` | `cloud-save-integrity` line 186's provider-hash comparison defeated (`require(True, ...)`) in a scratch copy | `cd /workspace/tmp/m6-t13/pos/integ && python3 -I -B tools/cloud-save-integrity-test --rclone /usr/bin/rclone` | rc 1: `FAIL changed payload rejected`. The test stops at its first FAIL, so the later cases did not run. | fixture |

## Proofs

| Claim | Evidence | proved: |
| --- | --- | --- |
| The nine are read at `8ebaf8daad`'s bytes | `git diff --stat 8ebaf8daad e1d51b3a04 -- $(cat .qa-scratch/t13/paths.txt)` empty; `cmp` of `git show 8ebaf8daad:tools/cloud-round-trip` with the worktree's: equal | tree |
| 34 steps and 44 cells, no delta | `t13-shapes.py` rc 0, `"deltas": []` | tree |
| `cloud_reconcile` was never added; A5 and RETENTION cannot pass | `git log --all --oneline --diff-filter=A -- '*cloud_reconcile'` empty; `APPLY` at line 1771; used at 2388 and 2433 | history |
| `cloud_migrate_layout` was deleted by `e6645cb5ea`; `cloud-pair-migration` refuses on its absence | `git log --diff-filter=D`; the stage-A run rc 2 | tool-run |
| `--backend` after the subcommand is ignored, rc 0 | `port --backend sftp` prints 9010; `--backend sftp port` prints 9013 | tool-run |
| `caps()` marks no step of the single-device suite | its three call sites, lines 2369-2373 (A14's helper) and 6786 (KILL1); `t13-shapes.py`'s `caps_keys` empty for all 34 steps | tree |
| The four descriptions disagree | `vm-qa:36` (27), the AST (32 steps, 460 checks), `vm-qa-log.md:175` (106), `2026_10_08-work_log.md:111` (108) | tree |
| The rule's no-network sentence is stale | `rclone-cloud-sync.md:375` says "exit-4 timing"; the tool asserts `rc == "69"` at 1469 (#909) | tree |
| The endpoint's `ls` reports a missing path as empty, rc 0; `run_steps.27`'s and KILL4's absence checks PASS on it | `CLOUD_QA_STATE=/workspace/tmp/m6-t13/no-such-state tools/cloud-test-backend --backend webdav ls`: rc 0, 0 bytes (SFTP the same); lines 629-633, 1567, 1838, 7054-7056 | tool-run |
| RETENTION's two last checks pass when nothing ran | lines 2451 and 2453: with `cloud_reconcile` absent the head and the device's copy are untouched, so both `check()` calls are true | tree |

## The streams' positives

**Kept on the branch (the coordinator's ask on #660, 06:45 UTC):** every positive below can be re-run from `stage-e/` in this folder. The README there (`stage-e/README.md`) has a table with one row per positive: the driver or the shell command for the unfixed clone (`tools/` at `8a2518fa44`) and for the fixed tree, and the line each prints.
- **The drivers:** `stage-e/pos1066`, `pos1060`, `pos1062`, `pos1063`, `pos1057`, `pos1059`, `pos1064`, `pos1069` and `pos1070` (`drive.py` each, sharing `stage-e/common.py`). Each takes the tool's path and `unfixed|fixed`, writes only under `$TMPDIR`, and prints one verdict line last: `pos<bug>: unfixed-expectation-met | fixed-expectation-met | UNEXPECTED ...`.
- **The #1068 shims** are built by `stage-e/shim1068/build.sh <dir under $TMPDIR>`.
- **All eighteen runs** (nine drivers in both states) met their expectation on 2026-10-25 at `cee4bf481d`. The README's shell rows were run as written.
- The scratch versions under `/workspace/tmp/m6-t13/pos*/`, which the lines below were first produced with, are superseded by these.

Stage E (the brief `docs/reviews/briefs/t13-streams.md` at `44fdec1e16`). Each bug's case is run first against the unfixed file (a shared clone at `8a2518fa44`, `/workspace/tmp/m6-t13/unfixed`, `tools/` checked out), then against the fix. Backends always run under the isolation environment; every case is taken down after, and the leftover check is in `00`. `proved:` tool-run for each.

### #1058 (S1): `--backend` after the subcommand
- unfixed (`8a2518fa44`, clone `/workspace/tmp/m6-t13/unfixed`): `tools/cloud-test-backend up --backend sftp` -> `up: webdav serving /workspace/tmp/m6-t13/state/data at http://127.0.0.1:9080 ...`, **rc 0**, listener `127.0.0.1:9080` (WebDAV's, brought down by `--backend webdav down`)
- fixed: `up --backend sftp` / `ls --backend s3` / `port --backend sftp` -> `error: '--backend' after '<sub>': options go before the subcommand (...)`, **rc 2** each, 0 listeners; `--backend sftp port` -> 9013 rc 0; `--backend s3 caps` -> `hash=md5 modtime=yes commit=atomic bucket=yes` rc 0; `ls t13` (a path) rc 0
### #1067 (S1): the SFTP endpoint confined, under a QA identity
- unfixed (`8a2518fa44`): `--backend sftp up` -> `up: sftp serving <state>/sftp/data at <host-login>@127.0.0.1:9083`; the stanza's `user =` is **the host's own login**; with the QA key, `sftp ... ls -1 /etc` through the endpoint returned **232 entries** and `ls ..` 9 (counts only; no names printed)
- fixed (`rclone serve sftp` rooted at the data directory, `--authorized-keys`, the generated host key): `up` -> `up: sftp serving <state>/sftp/data at rocknix-qa@127.0.0.1:9083`; stanza user `rocknix-qa` (not the host login); `ls /etc` -> `Can't ls: "/etc" not found`; `ls ..`, `ls ../..`, `ls /` list only the endpoint's (empty) root; `saves-remote` -> `/pixelelated/Saves` (relative now: the endpoint prefix is empty); an `rclone copy` through the endpoint kept the source modtime (`2020-01-02 03:04:05`), and `ls`/`cat` read it back (`caps` `modtime=yes` holds)
- **stated, not hidden:** rclone does not check the user name under key auth (a spare server on :9084 with `--user rocknix-qa` accepted `rocknix-qa`, another name and the host login with the QA key, rc 0 each); the guarantee is the key plus the confinement to the data directory -- no host account is behind any login
### #1068 (S1): no stanza from a failed obscure; the S3 config created private
- shims under `/workspace/tmp/m6-t13/shim1068/`: an `rclone` whose `obscure` exits 1 (all else to `/usr/bin/rclone`), and a `chmod` that does nothing
- unfixed: `--backend webdav|smb|ftp rclone-conf` with obscure failing -> **rc 0** and `pass = ***` (masked here) equal to the clear QA password, each; `--backend s3 ls` on a fresh state with chmod a no-op -> `s3-host.conf` mode **664**
- fixed: the same three -> **rc 1**, `error: rclone obscure failed; no stanza written (a clear password never goes in one)`, 0 `pass` lines; with the real rclone each writes an obscured `pass` (the clear value: 0 lines); the S3 config with chmod a no-op -> mode **600**
### #1060, backend half (S1): ls and reset fail closed
- unfixed (`8a2518fa44`), state `/workspace/tmp/m6-t13/state-1060`: `--backend webdav ls` with the state missing -> **rc 0, 0 bytes**; `--backend s3 ls` with no MinIO running -> **rc 0, 0 bytes**; `--backend webdav reset` with an undeletable survivor (a file in a mode-555 directory) -> `reset: endpoint is empty`, **rc 0**, 1 file left
- fixed: `ls` with the state missing -> `error: no endpoint state at <state>/no-such/data; 'up' first`, **rc 1**; `ls no/such/prefix` under live state -> rc 0, 0 bytes (an absent prefix stays empty); `s3 ls` with no MinIO -> **rc 1** with rclone's own error (`dial t...`); `reset` with the survivor -> `error: reset left 2 entr(y/ies) in <state>/data; the endpoint is not empty`, **rc 1**; with it deletable again -> rc 0, 0 left; a `..dotdot` name is removed (the old globs missed it)

**After S1** (06:14 UTC, at `7345a65e9d`), the three backends once each under the isolation environment:

```
== webdav :9080 06:14:28
up rc=0 1.0s
put rc=0
ls rc=0 lines=1
ls no/such/prefix rc=0 bytes=0
cat present rc=0
cat missing rc=1
reset: reset: endpoint is empty rc=0
ls after reset: rc=0 lines=0
caps: hash=none modtime=no commit=partial bucket=no
down: down rc=0
== sftp :9083 06:14:32
up rc=0 1.1s
put rc=0
ls rc=0 lines=1
ls no/such/prefix rc=0 bytes=0
cat present rc=0
cat missing rc=1
reset: reset: endpoint is empty rc=0
ls after reset: rc=0 lines=0
caps: hash=none modtime=yes commit=partial bucket=no
down: down rc=0
== s3 :9082 06:14:34
up rc=0 0.7s
put rc=0
ls rc=0 lines=1
ls no/such/prefix rc=0 bytes=0
cat present rc=0
cat missing rc=1
reset: reset: endpoint is empty rc=0
ls after reset: rc=0 lines=0
caps: hash=md5 modtime=yes commit=atomic bucket=yes
down: down rc=0
leftover: ss 0 docker 0 rclone-serve 0 minio 0
```

**#1067's second checkbox, rewritten** under the coordinator's ruling on #660 (06:17 UTC): it asked "does not authenticate as the host's own login user", a property sshd has and `rclone serve sftp` does not model. The checkbox now reads the QA key as the only accepted credential, confinement to the data directory under any user name, and no shell and no host account. It is ticked from these runs (06:2x UTC, at `94c050ed5a`, the evidence on #1067):
- ssh's defaults with the host login: `Permission denied (password,publickey)`, rc 255;
- the host's `~/.ssh/id_ed25519_devboxes` alone: `Permission denied (password,publickey)`, rc 255;
- an exec of `id`: `"id" not implemented`, rc 1;
- an exec of `sh -c true`: `"sh -c true" not implemented`, rc 1;
- the S1 confinement probes above.

rclone answers its built-in `md5sum`, `sha1sum` and `df` itself, executing nothing on the host. `df` printed the backing filesystem's figures, which is stated on #1067.

### #1066 (S2, High): the cleanup never removes what the run did not create
- driver `/workspace/tmp/m6-t13/pos1066/drive.py`: the tool loaded as a module, a stub device whose `/storage` and `/tmp` live under a scratch root (one regex pass maps only a path start; the first cut's two plain replaces rewrote the root's own `/tmp/` and aimed `rm -rf` at nothing -- the driver's bug, caught by tracing its commands), `backend()` a no-op; an occupied `/storage/roms/vectrex` seeded, then `restore_device`
- unfixed (`8a2518fa44`): the cleanup ran `rm -rf <root>/storage/roms/vectrex <root>/storage/roms/vectrex-unselected` -> the occupied library **DELETED**
- fixed: `content_root()` -> `refusal: /storage/roms/vectrex holds files (.../a-real-game.vec ...); refusing to use it as a fixture, and leaving it as found`; the cleanup -> `keep  /storage/roms/vectrex: this run did not create it, so it does not remove it`; the library **STILL THERE**
- control, fixed: `vectrex` absent at the start -> claimed, the run's own fixture written, the cleanup **REMOVED** it
- `grep -n 'rm -rf.*/storage/roms' tools/cloud-round-trip` at the fix: no line; every removal under `/storage/roms` (step 8, steps 15/16, step 27's `-unselected`, step 28's `definitely-not-a-system`, the LINK and KILL resets, `restore_device`) goes through `rm_owned`
### #1060, harness half (S2): an absence is judged only on a listing that happened
- driver `/workspace/tmp/m6-t13/pos1060/drive.py`: the tool loaded as a module with `BACKEND` pointed at S1's fixed `cloud-test-backend` and `CLOUD_QA_STATE` a directory that does not exist
- unfixed (`8a2518fa44`): `backend_files('ROMs')` -> `[]`, `backend_sizes('ROMs')` -> `{}`: step 27's "an unselected system was not uploaded" would read **PASS**; `backend('ls')` -> `CalledProcessError` (not a `Fail`: the runners do not catch it)
- fixed: all three -> `Fail: could not list the endpoint at 'ROMs' (exit 1: error: no endpoint state at <missing-state>/data; 'up' first); an absence on it would prove nothing` (and `backend('ls')`'s own `Fail` with the tool's line); the only direct `ls` call left is `backend_listing`, so A9, CONTRACT item 2, KILL1, the LINK cells and step 32's litter scan (the seat's G-28) read through it
- also: `epath()`/`rpath()`'s docstrings now say SFTP is rooted at its data directory (#1067)
### #1062 (S2): KILL1 reaches its verdict, and a deleted cloud file fails it
- driver `/workspace/tmp/m6-t13/pos1062/drive.py`: (1) the names `fx_kill1` reads that neither it, its parameters, module scope nor the builtins assign (module scope only -- the driver's first cut counted `Link.exercise`'s and `fx_kill5`'s local `webdav` as module-level and read "none"); (2) the preservation predicate over `{a: absent, b: v1, c: v2}` (unfixed: the inline `torn = {...}` evaluated from the AST; fixed: `kill1_bad()`)
- unfixed (`8a2518fa44`): unassigned reads `['webdav']` (the `NameError` at its re-run); the predicate fails **none** -> "every file in the cloud is v1 or whole v2" would read **PASS** with a file gone
- fixed: unassigned reads **none** (`webdav` assigned as KILL5 does); the predicate fails `{'saves/a.state': 'absent'}` -> **FAIL**; controls: all v1/v2 -> none, one torn -> that file; the in-place SKIP now applies only when every failing file is torn
- **guest half pending the window:** KILL1 run to its verdict on a QA guest
### #1063 (S2): CONTRACT's dry-run guard fires on a reported conflict, not on a word
- driver `/workspace/tmp/m6-t13/pos1063/drive.py`: the guard over a copy-arm dry run with no conflict (`out` = `dry-run: push ['saves/x.srm'] fetch [] conflicts [] questions []`, `conflicts` = `[]`) and over one with a conflict (unfixed: the `guard = ...` expression evaluated from the AST; fixed: `contract_guard()`)
- unfixed (`8a2518fa44`): no conflict found -> the guard **FIRES** (the banner's word); one conflict -> FIRES
- fixed: no conflict found -> the guard **does not fire**; one conflict -> FIRES (the structured list; bisync's list is built only from conflict lines, so the same test serves both arms)
### #1057 (S2): a cell whose script the image lacks is one SKIP, never a FAIL with PASS lines under it
- driver `/workspace/tmp/m6-t13/pos1057/drive.py`: `fx_retention` and `fx_a5` against a stub pair (device without `cloud_reconcile`; the endpoint read stubbed to what `both_changed` left; sleeps instant)
- unfixed (`8a2518fa44`): RETENTION -> `FAIL  no record.json ever appeared ...` then **`PASS  the head is unchanged`** and **`PASS  the device's copy was not replaced ...`** (vacuous), failures 1; A5 -> `FAIL  NO RECORD IN THE STORE ... (apply exit 127)`
- fixed: RETENTION -> `SKIP  RETENTION: cloud_reconcile is not on this image -- the wizard's apply step from a shell is the open decision D-CLOUD-051, and the cell waits for it (#1057)`, failures 0; A5 -> the same SKIP for A5; both in `SKIPPED`, the one list `main()`'s note and #1059's verdict read
- control, fixed, the script present and no record appearing: RETENTION -> only its FAIL, no PASS under it (the two checks are gated on the kill point)
- **guest half pending the window:** A5 and RETENTION on the QA image read as SKIP
### #1059 (S2, with PL-15): the verdict says what was checked, against which backend, and refuses what cannot run
- unfixed (`8a2518fa44`): `--only NO-SUCH-CELL --host root@127.0.0.1 --port 1 --identity /nonexistent` -> `FAIL  no shell over ssh`, rc 2, **the unknown name never named**; driver `/workspace/tmp/m6-t13/pos1059/drive.py`: `prepare_device` on a stub with ssh and no cloud scripts -> the equipment FAIL printed **and setup went on to its next step**; the last line after one SKIP and no failure (the unfixed `print` expression, evaluated) -> `PASSED (one cell could not run)` -- no counts, no backend
- fixed: `--only NO-SUCH-CELL` -> `error: --only names no fixture: NO-SUCH-CELL (tools/cloud-round-trip --list)`, **rc 2**, before any device; `--only A1` without `--second-port` -> `error: --only names two-device fixtures (A1); pass --second-port for the VM pair's guest b`, rc 2; the equipment check -> `Fail: the device lacks rclone or the cloud scripts (command -v found: nothing)`, setup stops; the last line -> `PASSED -- backend webdav (hash=none modtime=no commit=partial bucket=no): 1 passed, 0 failed, 1 skipped`; a run with nothing checked -> `NOTHING CHECKED -- ...`, exit 2
- the 14 ad-hoc `SKIP` prints now go through `skip()` (16 calls with #1057's two), so every skip is counted; the driver's first cut stubbed `backend()` for its last part and printed `backend  ()` -- the driver's, corrected; and a dead-device rc read as 0 was the measurement (`PIPESTATUS` after a command substitution), re-measured rc 2
### #1064 (S2): step 25 fails when its probe reads no ES path
- driver `/workspace/tmp/m6-t13/pos1064/drive.py`: the probe run on the host, where neither `es_systems.cfg` path exists (asserted), so it reads nothing (unfixed: the command taken from the AST and its `.split()`; fixed: `es_path_orphans()`)
- unfixed (`8a2518fa44`): orphans `[]` -> step 25 (`not orphans`) would read **PASS** with nothing compared
- fixed: `paths read: 0; orphans: []` -> step 25 reads **FAIL** (`the probe read no ES path at all ...`); the PASS line now prints the count read
- control, fixed: a stub with a planted `es_systems.cfg` of three paths and a fake `backuptool` naming one -> `(3, ['/storage/.config/bar'])`, the ROMs path skipped (the stub's first cut rewrote the `case` pattern inside the command and listed the ROMs path as an orphan -- the stub's, corrected to rewrite only the config's path)
- **guest half pending the window:** the count read on the QA image, in step 25's PASS line
### #1065 (S2): CAP13's warning check reads this call's log and tells absent from zero
- the shell fragment on the host over a log without the warning: `grep -c 'outside the saves folder' <log> 2>/dev/null || echo 0` -> `0\n0` (od: `0 \n 0`); the unfixed predicate `warned not in ("", "0")` on it -> **PASS** with no warning logged; the fixed predicate (the warning's presence in this call's part of the log, `log_mark`/`log_since`) on the same text -> **FAIL**
- **the sweep** (`grep -n 'grep -c.*|| echo 0' tools/cloud-round-trip`, at `8a2518fa44`), each hit with its cell and its disposition:
  - `:1115` (step 10, `warned`): read as `warned.isdigit() and int(warned) > 0`; `0\n0` is not a digit, so an absent warning FAILs -- the safe direction; **named, harmless, unchanged**
  - `:1132`, `:1135` (step 10, `before_warn`/`after_warn`): compared with each other only; two absent counts are `0\n0` == `0\n0` -- equal, as two zeros would be; **named, harmless, unchanged**
  - `:4592` (CAP13): the defect; **fixed** here
- **guest half pending the window:** CAP13 on a QA guest with the warning present (PASS) and absent (FAIL)
### #1069 (S2): A15 uploads an archive cloud_backup accepts
- driver `/workspace/tmp/m6-t13/pos1069/drive.py`: A15's upload fixture (the `dev.write(... upload ...)` argument, from the AST) written out and listed with `tar -tzf`, the check `cloud_backup` applies before sending
- unfixed (`8a2518fa44`): `b"this run's archive"` -> 18 bytes; `tar -tzf` **rc 2**: `gzip: stdin: not in gzip format` (cloud_backup refuses it, so A15 failed before the behaviour it names)
- fixed: `_settings_archive('a15')` (the helper the other fixtures use since 2026-09-10) -> 141 bytes; `tar -tzf` **rc 0**: `storage/.config/qa-suite/settings.cfg`
- **guest half pending the window:** A15 run to its verdict on a QA guest
### #1070 (S2): KILL5 expects what CLOUD_BACKUP_KEEP says
- driver `/workspace/tmp/m6-t13/pos1070/drive.py`: at `CLOUD_BACKUP_KEEP=2`, two retention results -- a correct one keeping the newest 2, and one hard-coded to 3 -- against KILL5's expectation (unfixed: `sorted(own[1:] + [archive])` over the three planted; fixed: `kill5_names(label, osn, keep)`)
- unfixed (`8a2518fa44`): the correct retention -> **FAIL**; the hard-coded 3 -> **PASS**
- fixed: the correct retention -> **PASS**; the hard-coded 3 -> **FAIL**; KILL5 now plants `keep` own archives (so the run's upload makes `keep + 1` and retention trims exactly one), and its "all planted archives are still there" count is `len(own) + 2` where it read a literal 5 (found while fixing; the docstring's "three own" and "all five" corrected with it)
- **guest half pending the window:** KILL5 on a QA guest at the default keep and at `CLOUD_BACKUP_KEEP=2`

**After S2** (at `77e7b16193`): `tools/cloud-round-trip --list` prints 45 cells; the dead-device case (`--host root@127.0.0.1 --port 1 --identity /nonexistent/qa-key`) exits **2** with `error: no shell over ssh on root@127.0.0.1 port 1`; no listener on 9010-9099, no QA container.

### #1061 (S3): the fixture value is assembled at run time
- T10's widened patterns read with `git show feature/m6-tooling-guards-657:.githooks/secret-patterns` into `/workspace/tmp/m6-t13/secret-patterns.t10` (`cmp` equal; never merged), sourced as the hooks source them, `/usr/bin/grep -a -c -E "$SECRET_PATTERNS"`
- unfixed (`8a2518fa44`): `tools/cloud-connections-test` -> **1** line (line 37's assignment)
- fixed: **0** lines under T10's set and this branch's; the value is `'-'.join(('qa', 'only', 'fixture', 'pass' + 'word'))`, byte-equal to the old literal (checked); `tools/cloud-connections-test` -> `Ran 26 tests in 1.867s` / `OK`
### #1081 (S3): the census reads the stored id and runs no device script
- unfixed (`8a2518fa44`): `grep -c cloud_device_id tools/cloud-census` -> **1** (line 76, `echo device=$(cloud_device_id 2>/dev/null)`); an AST read of the file's string constants for any script under `projects/ROCKNIX/packages/network/rclone/sources/` invoked -> **`['cloud_device_id']`**
- fixed: `grep -c` -> **0**; line 79 reads `echo device=$(cat /storage/.config/cloud_sync-device-id 2>/dev/null || echo unset)` (the file `cloud_device_id:54` names and `write_id` at `:288` writes, one line, the same id the script prints); the AST read -> **none**; the header's "the device's own scripts are not run" is now true and stays. The census was not run against anything.
### #1067, follow-up under the coordinator's ruling (#660, 08:12 UTC): the endpoint's directory cache (G-1)

The cause is `rclone serve`'s directory cache, not the rclone version. Its default is five minutes. A fixture put into DATA after the server had started (its own login check lists `/`) stayed hidden, and the content tier's scan, `lsf -R --files-only --format sp --separator '|' qa-cloud:/CONTENT/ROMs/`, answered `directory not found` (rc 3). The script reads rc 3 as an empty cloud. The host diagnosis (08:13 UTC, the M6 donor's 1.75.2 as the client throughout):

| Server | Fixtures present at start | Fixtures written after start, default cache | Written after start, `--dir-cache-time 1s` |
| --- | --- | --- | --- |
| host rclone 1.60.1 | rc 0, both listed | rc 3 | rc 0 |
| donor rclone 1.75.2 | rc 0, both listed | rc 3 | rc 0 |

Fixed in `7a71af7671`: the endpoint serves with `--dir-cache-time 1s`, as WebDAV does, and `settle_cache` now waits for sftp too, so `put`, `reset` and `seed-content` settle on both. The positive is `stage-e/pos1067cache/run.sh`:

- the tool at `22099cb7f9`: `scan rc=3, files listed 0 of 2`, unfixed expectation met;
- the tool at `7a71af7671`: `scan rc=0, files listed 2 of 2`, fixed expectation met;
- the crossed run (old tool, `fixed`): `UNEXPECTED`, exit 1.

An earlier probe, with no settle after the write, listed nothing on the fixed tool either; that was the 1 s window, and the driver goes through `put` so it settles as the harness does. No `CLOUD_QA_RCLONE` was added: the version is not the cause. **Not yet shown:** G-1 quotes `rclone exit 5` from the guest's log, and the retained cycle record does not carry that line. The seven failures it does carry all read the cloud side as missing or empty. The second window's SFTP suite is the proof, and it keeps the guest's content log.

### #1059, follow-up under the coordinator's ruling (#660, 06:33 UTC, D-QA-063): nothing checked exits 3
- `main()`'s final return, evaluated from the AST at the follow-up: a run whose verdict line reads `NOTHING CHECKED -- backend webdav (hash=none modtime=no commit=partial bucket=no): 0 passed, 0 failed, 1 skipped` -> **exit 3** (was 2 at `e71d077882`); a pass -> 0; a failure -> 1; the usage error (`--only NO-SUCH-CELL`) stays **rc 2**; `--list` 45

**After S3** (at `cee4bf481d`): `tools/cloud-connections-test` -> `Ran 26 tests in 1.846s` / `OK`; `git diff --stat e1d51b3a04 cee4bf481d -- tools` names only `cloud-connections-test`, `cloud-census`, `cloud-round-trip` and `cloud-test-backend`.

## The guest cycle

**The window:** granted by the coordinator on #660 at 07:50 UTC (its own comment, after the M7 lane's FINAL RETURN), with a 45-minute bound.
- **START:** 07:52:28 UTC, with `pgrep -x qemu-system-x86 -r R,S,D,T | wc -l` reading 1 (#660).
- **The guest stopped:** 08:09:21 UTC, about 17 minutes in.

**The image:** M6's own copy, `/workspace/artifacts/m6-t3-20261024/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (sha256 prefix `6b4c3079bdee2f47`). Its `/etc/os-release` reads BUILD_ID **`069fc270442134fe771258418adf4e666e0473fb`**, as its `.identity.json` does (copied to `stage-e/cycle/image.identity.json`).

**One guest:**
- **Booted** with `tools/vm-pair reimage a <image>`: 43 s, answering over SSH on :10022. `vm-pair up` would have started two guests, and `vm-qa` ran with `--skip-up`.
- **Isolation:** `VM_PAIR_DIR=/workspace/tmp/m6-t13/vm-pair`, `VM_QEMU_RUNTIME_DIR=/workspace/tmp/m6-t13/run`, `ROCKNIX_ARTIFACTS=/workspace/tmp/m6-t13/artifacts`; backends on `CLOUD_QA_STATE=/workspace/tmp/m6-t13/state` (WebDAV :9080, throttled to 200k for KILL1 and KILL5; SFTP :9083).

**The record:** `stage-e/cycle/`.
- every cell's output: `u-*.out` (the clone at `8a2518fa44`) and `f-*.out` (this branch);
- `vm-qa-webdav/` and `vm-qa-sftp/` (each `vm-qa` report and its `round-trip.log`; the round-trip suite takes no frames, so their `walks/` were empty);
- `boot.out`, `down.out` and `leftover.txt`;
- `notes.txt`.

| Cell | Unfixed (`8a2518fa44`) | Fixed (this branch) | The bug's guest criterion | proved: |
| --- | --- | --- | --- | --- |
| KILL1 (#1062) | `NameError: name 'webdav' is not defined`, rc 1 (`u-kill1.out`) | reached its verdict: `3 CHECK(S) FAILED -- backend webdav (...): 21 passed, 3 failed, 0 skipped`. Both variants' re-runs after the kill exit **124** under the 200k throttle, and 1a's cloud lacks v2 of `savestates/kill1-2.state`: new, below (`f-kill1.out`) | **met:** KILL1 runs to its verdict | guest |
| CAP13 (#1065) | warning present: PASS. Warning absent (`/var/log/cloud_sync.log` a symlink to `/dev/null` for the run, a named synthetic input, the log restored after): **PASS, wrongly** (`u-cap13-*.out`) | at `f7482f9684` **both FAILED**: the image's `cloud_capture` writes `<path> is not a path under the saves folder <root>; not recorded`, and "outside the saves folder" appears nowhere in it, so the old check had passed only through `0\n0`. Fixed in-window by `a70b4889a3` (#1065). Then present -> `PASSED -- ... 10 passed, 0 failed`; absent -> `1 CHECK(S) FAILED`, `the warning in this call's log: absent` | **met:** present PASS, absent FAIL | guest |
| A15 (#1069) | `6 CHECK(S) FAILED` (32 passed), among them `the backup did not land in GENERIC-X64-15ca35b6b4 (exit 1)` and `no device.json` (`u-a15.out`) | `2 CHECK(S) FAILED -- backend webdav (...): 36 passed, 2 failed`. The backup lands. The two left (`the log did not name the folder`, `the log did not: ...`) were there unfixed too: a separate finding, below (`f-a15.out`) | **met:** A15 runs to its verdict, and #1069's failures are gone | guest |
| KILL5 (#1070) | keep 3 (the image's default): PASSED (`u-kill5.out`) | keep 3: `PASSED -- ... 17 passed`; `CLOUD_BACKUP_KEEP=2` set on the guest for the run and restored after: `PASSED -- ... 17 passed`, with `all 4 planted archives are still in the folder` (`f-kill5-keep*.out`) | **met:** passes at the default keep and at 2 | guest |
| step 5b, A5 and RETENTION (#1057), with **device b being guest a itself** (`--second-port 10022`) | not run | **refused before either cell:** `a is GENERIC-X64-15ca35b6b4, b is GENERIC-X64-15ca35b6b4 -- one id, or none, between two devices (#91)` and `error: refusing the two-device fixtures: both guests carry the MAC 52:54:00:52:4e:58 ...`, rc 2 (`f-5b.out`). The harness's own #91 guard stops a pair that agrees with itself; it was not bypassed | **not met:** needs two guests; the host positive (`stage-e/pos1057`) stands | guest |
| the suite over WebDAV (#1059, #1064) | -- | `PASSED -- backend webdav (hash=none modtime=no commit=partial bucket=no): 108 passed, 0 failed, 0 skipped`; step 25: `every ES path outside /storage/roms is in the settings backup (128 ES paths read)`; `vm-qa` row `round-trip PASS 84s` | **met:** #1064's count read on the image (128); #1059's line on a guest | guest |
| the suite over SFTP | the unfixed harness over the **old** sshd endpoint: `PASSED`, rc 0, 67 s (`u-suite-sftp.out`) | `7 CHECK(S) FAILED -- backend sftp (hash=none modtime=yes commit=partial bucket=no): 101 passed, 7 failed, 0 skipped`, all in the content tier (the BIOS absent after `--all`; scans reading the cloud side as 0; one apply exiting 1). The guest's log: `cloud_content_restore scan: the cloud could not be read (rclone exit 5)` (`vm-qa-sftp/`) | **a regression of #1067's endpoint**, below | guest |

**Found by the cycle** (each goes to stage F and 05):
- **G-1. #1067's `rclone serve sftp` endpoint breaks the content tier over SFTP.** The same guest passes the whole suite over the old sshd endpoint and fails 7 content checks over the new one. #1067's confinement is real (02 § The streams' positives), but its fix as made is not a working endpoint for the content tier. The rclone call that fails has not been pinned down. The device's rclone (1.75.2) talks to the host's `serve sftp` (1.60.1), and the scan's listing returns exit 5.
- **G-2. KILL1's re-run exits 124 under the 200k throttle,** where LINK's `exercise` has a `drained` branch for a 124 on WebDAV. KILL1 reached this only now: every run since `931a413457` stopped at the `NameError`.
- **G-3. A15's two log-wording checks** (`the log did not name the folder` and `the log did not: ...`) fail both unfixed and fixed. That is likely a stale needle like CAP13's, not yet read.
- **G-4. CAP13's needle was stale** (found and fixed in-window, `a70b4889a3`).

**The teardown:** `tools/vm-pair down` gave `down: owned QEMU exited (pid 705918)`, the stop by pidfile through `vm-stop`. `--backend webdav down` and `--backend sftp down` both printed `down`. The leftover check at 08:09:21 UTC (`stage-e/cycle/leftover.txt`): qemu 0; `ss -ltn` 0 on 9010-9099 and 0 on 10022; `docker ps -a` 0 `rocknix-cloud-qa*`; 0 sshd on the `m6-t13` config; 0 `rclone serve`; 0 `minio server`.

**My own slip, recorded:** the clone held `tools/` only, so the unfixed backend's `shipped-default` read no defaults file and the first KILL1 control stopped at planting (`put <stage> ''`). I checked out `projects/ROCKNIX/packages/network/rclone/sources` at `8a2518fa44` into the clone and re-ran the control; the first output was overwritten by the re-run. `stage-e/README.md`'s clone command is corrected below.
