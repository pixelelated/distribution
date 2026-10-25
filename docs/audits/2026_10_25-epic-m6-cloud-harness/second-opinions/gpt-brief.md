# Second opinion (Phase 4.6), M6 T13: the cloud test harness of pixelelated/distribution

You are the one independent reviewer for a code audit of nine fork-own test tools, `tools/cloud-*`, at commit `8ebaf8daad`. The first reader (another lab's model) wrote `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md`, all included below. Below them come three context sections and the nine files, line-numbered.

The lens is brittleness (blindspot 31: *a harness that agrees with itself*): **what each tool's PASS certifies, by what oracle, and what would have made it FAIL.** Your job is to refute, narrow or confirm, against the code: not to agree. Cite `file:line` for every claim. Say plainly where the first reader is wrong.

Answer these first, in this order:

1. **The assertion-shape table's gaps.** In 02 § Assertion shapes, which rows whose claim says a thing *reached the cloud*, *was restored*, *was withheld* or *nothing else changed* actually read only one end? Classify each by evidence: the device's own output or round trip, the device's own rclone listing the remote, or a planted input. Name every row you would reclassify, with the line that decides it. Check the eight `(reviewed)` overrides and the generator's rule (`tools/t13-shapes.py`'s docstring is quoted in 02).
2. **The two scripts that do not exist.** First, `cloud_reconcile` (`APPLY`, line 1771; used at 2388 and 2433): is the first reader right that A5 and RETENTION fail by construction, and that RETENTION's lines 2451 and 2453 pass vacuously? Is any other fixture affected? Second, `cloud_migrate_layout` in `cloud-pair-migration`.
3. **The no-network step's synthetic input** (`run_steps` step 24, lines 1460-1479: a stub `ip` first on `PATH`). What does its PASS prove about the real no-network path, and what does it not? The rule says *exit-4 timing* and the tool asserts 69: which is right, by the code?
4. **The retired tool's disposition** (`cloud-pair-migration`, exit 2 at lines 58-63). Is retirement right? Is anything in it worth keeping that the other eight do not already carry?

Then:

5. **Refute or confirm each finding F-01 to F-13** in 04 § Findings: confirmed, confirmed with narrowing (say how), or refuted (with the line). Weigh in particular:
   - F-12: `cloud-test-backend ls` ends in `|| true`, so a missing path lists as empty with rc 0, and `run_steps.27` and KILL4 judge absence on that listing. Are there more rows of that shape than the two named?
   - F-04: `caps()` marks no step of the single-device suite.
6. **What the first reader missed:** any check that cannot fail, any probe that cannot report absence, any wall-clock wait standing in for an ordering, any credential-handling risk in `cloud-test-backend` (it writes an sshd host key and composes connection strings), anything in the seven small tools.

**Output:** numbered items `G-1`, `G-2`, ..., each with one line saying *confirmed / narrowed / refuted / new*, the `file:line` evidence, and two to five sentences. Group them under the six headings above. Do not restate the packet. Do not reproduce long code. Keep the whole reply under about 12,000 words.


## The first reader's 02-forward-audit.md (whole)

# T13 forward audit: the cloud test harness (#660)

Phase 2 over #660's checklist, the nine tools at `8ebaf8daad`'s bytes. Stage A
wrote § The runs; stage B § Coverage, § Assertion shapes, § Positives and
§ Proofs; § The guest cycle is written in the window granted on #660.

## Coverage

One row per path. *Oracle* is what decides the tool's PASS; *caller* is
who runs it (`grep -n` of `tools/vm-qa`, the other eight, and `.github/`).

| Path | Lines | Subject | Oracle | Caller | Positive (§ Positives) | proved: |
| --- | ---: | --- | --- | --- | --- | --- |
| `tools/cloud-round-trip` | 7,808 | the cloud scripts on a guest, over SSH, against a QA endpoint | 24 rows read both ends, 10 the device's report, 44 a planted input (§ Assertion shapes) | `vm-qa` `round-trip` (single-device suite) and `link` (LINK1-7); the other registries by hand | refused SSH port: rc 2, `FAIL  no shell over ssh` | tool-run |
| `tools/cloud-test-backend` | 920 | five local endpoints and a dead port | it is the endpoint; `cat` checks existence first | `vm-qa`, `cloud-round-trip` | `cat no/such/object`: rc 1 on WebDAV, SFTP and S3 | tool-run |
| `tools/cloud-connections-test` | 307 | `cloud_connections` (staged connection transactions) | the module itself, under the **host's** rclone | nobody | the duplicate-name refusal defeated: `FAIL: test_duplicate_keeps_old_bytes`, rc 1 | fixture |
| `tools/cloud-census` | 306 | a handheld's `/storage` and logs over SSH | reading only | nobody | none: a handheld-only tool, never run (D-QA-015) | design |
| `tools/cloud-pair-migration` | 243 | two guests across `cloud_migrate_layout` | -- | nobody | none: exits 2 before anything on every tree after `e6645cb5ea` | tool-run |
| `tools/cloud-save-integrity` | 219 | manifests and save containers (D-CLOUD-181) | its sibling test's synthetic corruption, and rclone's Dropbox hash | nobody | its test's 19 rejection cases (stage A, `PASS total=24`) | tool-run |
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
- **The lane's review overrode eight rows,** each marked `(reviewed)` with its reason in the Note column.
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
| `run_steps.30` | 1674-1693 | seeding is idempotent and never clobbers an existing note | both ends | 0 | 3 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.31` | 1694-1713 | an older config's keys are carried across (D-UI-022, A12) | synthetic | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `run_steps.32` | 1714-1716 | one last-known-good of every record, and no writer's litter, after the suite | device report | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `prepare_device.1` | 309-317 | f'device {which}reachable and equipped | device report | 0 | 2 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) |  | tree |
| `prepare_device.2` | 318-383 | f'point device {which}at the QA bucket' if which else 'point the device at the QA bucket | device report | 0 | 1 | not read | the suite's: 2026-10-06, `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP` (`vm-qa-log.md:175`); the 2026-10-08 work log's 108 (`2026_10_08-work_log.md:111`) | setup: points the device at the QA endpoint; its one check is the device's active remote | tree |
| `A1` | 1972-1999 | both changed after a first pass: every writer, this device's copy newer and older | both ends | 0 | 2 | not read | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A2` | 2002-2043 | a failed push retried; an equal-size, equal-mtime change after a first pass | both ends | 0 | 3 | not read | none recorded |  | tree |
| `A3` | 2046-2082 | CHANGE CLOUD FOLDER to a folder holding different saves | both ends | 0 | 4 | not read | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A8` | 2085-2144 | a torn N64 pair: interrupted after one member, held, then cleared | both ends | 0 | 4 | not read | none recorded |  | tree |
| `A9` | 2147-2252 | delete and renumber; a retired hash put back; rm; an unmounted, empty, or empty-cloud root | both ends | 0 | 19 | not read | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A11` | 2255-2277 | a cloned device id refuses to publish | both ends | 0 | 2 | not read | none recorded |  | tree |
| `A12` | 2280-2318 | a legacy RESTOREPATH unlike BACKUPPATH: migrated, warned, nothing touched | synthetic | 0 | 9 | not read | none recorded |  | tree |
| `A14` | 2321-2377 | the manifest step: under savestates/.rocknix/, sha256, remote_hash per backend, one tier | both ends | 0 | 5 | hash | named 2026-09-07 (`vm-qa-log.md:39`; 1 row(s)) |  | tree |
| `A5` | 2380-2417 | the discarded-saves reader, from the second device | device report (reviewed) | 0 | 3 | not read | none recorded | the reader is device b's own rclone (lsf, cat); FAILS by construction: APPLY calls cloud_reconcile, which has never existed (line 1771) | tree |
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
| `KILL1` | 6771-6855 | saves backup killed mid-transfer, SIGKILL then SIGTERM: cloud holds v1 or whole v2, stamp never 0, lock released, re-run completes | synthetic | 0 | 13 | commit | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) |  | tree |
| `KILL2` | 6858-6956 | saves restore stopped mid-download by ES's TERM-then-KILL (D-CLOUD-076): the game's save stands, *.partial litter, re-run keeps the previous version | synthetic | 0 | 15 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL3` | 6975-7019 | backuptool backup killed mid-rotation: the previous archive is still what both readers find | synthetic | 0 | 10 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) |  | tree |
| `KILL4` | 7021-7070 | backuptool backup killed mid-tar: no truncated archive under a final name, nothing invalid uploaded | both ends | 0 | 9 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL5` | 7073-7159 | settings upload killed mid-copyto: marker, retention and device.json untouched; the re-run trims only this device's | both ends | 0 | 16 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL10` | 7162-7202 | set_setting killed mid-sed: the value stands, the temp is litter, the stale lock clears | synthetic | 0 | 5 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL11` | 7205-7235 | set_setting killed between delete and add: the previous value is not lost | synthetic | 0 | 3 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL12` | 7251-7352 | chksysconfig at boot with an empty, truncated, valid or binary system.cfg (power cut), and the clean-shutdown record | synthetic | 0 | 5 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL13` | 7375-7512 | es_settings.cfg and system.cfg power-cut through ES's own writers (arm A), and planted torn files at boot (arm B) | synthetic | 0 | 5 | not read | named 2026-09-10 (`vm-qa-log.md:48`; 3 row(s)) |  | tree |
| `KILL15` | 7515-7540 | an empty saves-root record refuses instead of reading as none | synthetic | 0 | 7 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL16` | 7543-7577 | content-systems: a kill before the write keeps the selection; an empty file is legal, so the writer must verify | synthetic | 0 | 3 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `KILL18` | 7580-7659 | backuptool restore killed mid-extract: the tree is half restored and the pre-restore state kept nowhere | synthetic | 0 | 10 | not read | named 2026-09-10 (`vm-qa-log.md:47`; 2 row(s)) |  | tree |
| `CONTRACT` | 4617-5128 | #9's transport contract under the reconciler (--transport copy,bisync) | both ends | 3 | 16 | not read | none recorded | not a registry cell: --list prints it beside PAIR; the Transport class reads the endpoint by cloud_sha (8) and backend_files/bytes (3) | tree |

Rows: 78 (34 steps + 44 cells) + `CONTRACT` = 79. By oracle over the 78: both ends 24, device report 10, synthetic 44.

**The class whose oracle is the device's own report: 10 rows.** `run_steps.3`, `.4` and `.6` are round trips through the device's own restore. `run_steps.12`, `.21`, `.25` and `.32` read the device's summary, log, ES paths and records. `prepare_device.1` and `.2` are setup. `A5` is device b's own rclone, and fails by construction. None of these reads the endpoint from the host: a PASS on them certifies what the device says, through the code under test. Four more rows read the remote with the device's own rclone and are classed by their other evidence: `run_steps.7`, `.9`, `.10` and `.13` (both device-rclone and planted), plus `A15` and `CONTRACT`.

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
| `cloud-save-integrity` | its sibling test's corrupt, truncated, unsafe and changed packets | `tools/cloud-save-integrity-test --rclone /usr/bin/rclone` (§ The runs) | each of the 19 rejection cases is the verifier refusing a constructed bad input (`PASS ... rejected` = the verifier's FAIL path taken) | tool-run |
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


## The first reader's 03-retrospective.md (whole)

# Retrospective: M6.P2 T13, the cloud test harness (#660)

Phase 3: what the harness was for, what drifted, what none of it noticed,
what the record says it caught, and the seams. Every claim cites
`02-forward-audit.md` or a file:line at `8ebaf8daad`.

## 3.1 What the harness was for

The harness exists to prove the cloud tiers from both ends after
blindspot 31. That was the day MinIO's `rclone cat` of a missing key exited 0
and a check that a file *reached the cloud* passed for a file that was never
there. The answer was `cloud-test-backend cat`'s existence check (lines
650-653) and `epath()` (line 1803), so the harness reads the endpoint itself
rather than asking the device. Its five local endpoints (D-QA-058) were built
so that no proof needs a person's cloud, and stage A found them doing that:
each refused `cat` of a missing object with rc 1 and left nothing running.

## 3.2 What drifted

- **The single file grew past one reader's reach.** `cloud-round-trip` went
  from 4,953 lines to 6,989 on 2026-09-10 alone and is 7,808 now, 77% of the
  slice (01 § History). Six registries and the single-device suite share one
  file, one `check()` and one `Fail`.
- **Its four descriptions came apart.** `vm-qa:36` says 27 steps; the file
  has 32 steps in `run_steps` and 460 `check()` calls; the ledger says 106
  PASS; the work log says 108 (02 § The runs). No PASS line says which count
  it certifies.
- **Two scripts it names are not in the tree.** `cloud_reconcile` was never
  added, so A5 and RETENTION cannot pass. `cloud_migrate_layout` was deleted
  by `e6645cb5ea`, so `cloud-pair-migration` refuses with rc 2.
- **The rule drifted from the tool.** `rclone-cloud-sync.md:375` says the
  no-network step checks *"the exit-4 timing"*; the tool asserts exit 69 at
  line 1469 (#909, open, its checkboxes ticked while this tree's rule still
  carries the sentence).

## 3.3 What none of them noticed

- **`caps()` marks nothing in the single-device suite.** It is read at three
  call sites: A14's helper twice, KILL1 once (02 § Assertion shapes). The
  promise *"nothing is skipped in silence"* holds there because nothing is
  marked or skipped at all. Every backend runs the same 34 steps, and the
  backend's capabilities never change what a step asserts.
- **Ten rows judge by the device's own report,** three of them round trips
  through the device's own restore, and four more read the remote through
  the device's rclone. Each certifies the code under test by that code's
  own output.
- **`cloud-test-backend` accepts `--backend` after the subcommand in
  silence** and answers for WebDAV, rc 0 (02 § The runs). The brief's own
  stage-A commands were written in that order, and so would any reader's be.
- **RETENTION's last two checks pass when nothing ran** (lines 2451, 2453):
  a cell that cannot run reports two PASS lines under its FAIL.

## 3.4 What the record says about catches

The harness found product defects: 19 `bug` issues name `cloud-round-trip`
as their proof (#53, #141-#143, #315, ...), and #366's eleven failures on a
`/GAMES` default were the harness catching its own fixture. The two
self-contained tests with documented positives were each seen to fire
again here: the stamp test over `f451252587`, and the integrity test with
its hash comparison defeated. Nothing in the record shows a red A5 or
RETENTION. Neither has a ledger row (02 § Assertion shapes, 8 rows with
none), so the cells that cannot pass were never reported as failing either.

## 3.5 The seams

| Seam | What crosses it | What this slice found there |
| --- | --- | --- |
| the harness x `vm-qa`'s suites | `vm-qa` runs `round-trip` and `link` (lines 295, 349) and describes the first as *27 steps* (line 36) | the count is wrong; `vm-qa` never runs `cloud-test-backend down` after a suite, so a backend outlives every run; its guest disks and sockets default to `/tmp` (lines 98-99) |
| the harness x the QA backends | `backend(...)` calls with `CLOUD_QA_BACKEND` exported (line 533) | the tool is called by environment, so the argument-order trap does not bite the harness; it bites a person at a prompt. `down` kills any listener on its port (lines 565-591), so two lanes on the default ports can stop each other's endpoint |
| the harness x the guests | SSH on 10022 (guest a, fixed), the serial and monitor sockets for LINK and KILL (defaults under `/tmp`, `cloud-round-trip` lines 503, 512) | the runtime directory and disks are parameters (`VM_QEMU_RUNTIME_DIR`, `VM_PAIR_DIR`), the SSH port is not |
| the harness x T15's shims | `last-good-scripts-test` names `cloud_migrate_layout` 55 times | the script is gone; T15's suite carries the name guarded by existence (a lead handed back, T15's) |
| the harness x the rule under #909 | `rclone-cloud-sync.md`'s `paths:` names four of the nine (`cloud-round-trip`, `cloud-test-backend`, `cloud-census`, `cloud-capture-stamp-test`) | opening the other five loads no rule; the no-network sentence is stale |
| the harness x `vm-visual-qa` under #972 | `cloud-round-trip` loads `tools/vm-visual-qa` as a module (`visual_qa()`, lines 6281-6292): for the `Monitor` class's VNC frame grab (line 6233), which the monitor-driven KILL cells use, and for KILL13's walks (`run_walk`, lines 7450 and 7494) | an open bug in that tool is a risk to those KILL cells, not to the single-device suite, which never loads it |


## The first reader's 04-analysis.md (whole)

# Analysis: M6.P2 T13, the cloud test harness (#660)

Phase 4 over the nine tools at `8ebaf8daad`'s bytes. Evidence is
`02-forward-audit.md` (§ Coverage, § Assertion shapes, § The runs,
§ Positives, § Proofs) and `03-retrospective.md`. Written at stage B; the
seat's grades (§ Second opinion) and the guest cycle's lines land at stages
C and F.

## Executive summary

The harness reads both ends where blindspot 31 said it must: 24 of the 78
rows read the endpoint from the host, and the endpoint's own `cat` refuses a
missing object on all three backends run (rc 1). Every tool that can fail on
the host was seen to fail on a constructed input. But five things a PASS
from it does not say:

1. **Which count it certifies.** The tool ends on a bare `PASSED`; its four
   descriptions say 27, 32/460, 106 and 108.
2. **That the backend changed anything.** `caps()` is read at three call
   sites, none in the single-device suite, so every backend runs the same
   34 steps.
3. **That an absence it asserts was looked for.** The endpoint's `ls` returns an empty listing with rc 0 when the path is not there, and two rows judge absence on that listing alone (F-12).
4. **That two of its cells can run at all.** A5 and RETENTION call
   `cloud_reconcile`, which was never added. They have no recorded verdict,
   and RETENTION prints two vacuous PASS lines under its FAIL.
5. **That its endpoint is the one named.** `cloud-test-backend` accepts
   `--backend` after the subcommand in silence and answers for WebDAV, rc 0.

Ten rows judge by the device's own report, three of them as round trips
through its own restore.

## Acceptance-criteria scorecard

| # | Criterion (#660) | State at stage B | Artifact |
| ---: | --- | --- | --- |
| 1 | the folder holds 00 to 05 | partial: 00-04 written, 05 at stage C/D | the folder |
| 2 | lint PASS (pre-issue before D, resolution at close) | open: `review-plan.json` and 05 owed (stage C) | `tools/lint-audit-artifacts ... --phase pre-issue` |
| 3 | `review-plan.json`, provenance, the packet's scan | open: stage C | `second-opinions/` |
| 4 | the punch-list issue at Phase 7 | open: stage D-G | -- |
| 5 | `reviewed-at`/`fixed-at`; no `tools/` file outside the nine changed | the read is on `8ebaf8daad` (diff empty); no file under `tools/` changed | 01 § Scope; `git status` |
| 6 | 01 § Scope with § 2's block and the history | done | 01 § Scope |
| 7 | 02 § Coverage, 9 rows | done: the awk prints 9 | 02 § Coverage |
| 8 | 02 § Assertion shapes | done: 79 rows (34 + 44 + `CONTRACT`), generator rc 0, no delta; the device-report class listed (10) | 02 § Assertion shapes |
| 9 | 02 § The runs | done for stage A; nothing left running | 02 § The runs |
| 10 | 02 § The guest cycle | waiting for the window on #660 | -- |
| 11 | 02 § Positives, one row per tool | done: 7 fire, 2 `none` with why | 02 § Positives |
| 12 | 00 shows none of the forbidden runs | holds so far | 00 |
| 13 | 04 § Q2, Q6, Q4, Q3 | Q2, Q4, Q6 written; Q3's `bug` issues are filed at stage D | below |
| 14 | `proved:` cells, `question:`, `box-check` | `proved:` in every 02 table; `question:` at stage D | 02 |
| 15 | the retro | stage G | -- |
| 16 | the five checkers on the branch | at hand-back | -- |

## Risk assessment

| Risk | Likelihood | Impact | Where |
| --- | --- | --- | --- |
| A green suite read as "the cloud tiers work on every backend" when no step is marked by backend | high (that is how the ledger reads it: *106 PASS each over WebDAV, SFTP and MinIO-S3*) | a backend-specific defect passes; blindspot 31's family | F-04 |
| A5 and RETENTION never run, so the discarded-saves store and the retention ordering have no proof at all | certain until the reconciler exists | T16 inherits two cells that cannot speak | F-01, F-02 |
| A backend run against the wrong endpoint because `--backend` followed the subcommand | medium (the brief itself wrote it that way) | a proof labelled SFTP that ran on WebDAV | F-03 |
| Two lanes' backends on the default ports, one `down` stopping the other's | medium on a shared host | a red run blamed on the code | F-07 |
| Host-only tests trusted for the image | low (each names its host oracle) | a busybox or rclone 1.75.2 difference passes the host | F-09 |

## Coverage boundary

Read: the nine tools whole for their oracles and positives; `cloud-round-trip`
by AST (every `step()`, every registry cell, every `caps()` call site, every
`check()`) and by hand for the eight overridden rows and the cells that
delegate (`Link.exercise`, `Pair.cloud_sha`, the `Transport` class).
Run: the four bare tests, the documented positive, the retired tool, three
backends (WebDAV, SFTP, S3) up/ls/cat/down, `--list`, and six constructed
positives. **Not run:** SMB and FTP (no stage-A run asked for them; their
images and venv are read for Q4 only), the single-device suite and CAP1-14
on a guest (the window), the PAIR, SOLO, LINK and KILL registries (two
guests, a throttled endpoint or a serial console; outside this slice's one
cycle), `cloud-census` (never: D-QA-015). Not read as code: the cloud scripts
the harness drives (T16's, T17's).

## Findings (Phase 4)

| ID | Finding | Q | Evidence (02 / 03) | proved: |
| --- | --- | --- | --- | --- |
| F-01 | A5 and RETENTION call `cloud_reconcile` (`APPLY`, line 1771), which has never existed; both fail by construction and neither has a recorded verdict | Q3 | § Proofs; § Assertion shapes | history |
| F-02 | RETENTION's last two checks (lines 2451, 2453) PASS when nothing ran: an assertion that holds only because nothing happened (blindspot 8) | Q3 | § Proofs | tree |
| F-03 | `cloud-test-backend` ignores `--backend` after the subcommand and answers for WebDAV, rc 0 (lines 57-63) | Q3 | § The runs; § Proofs | tool-run |
| F-04 | `caps()` marks no step of the single-device suite; it is read only by A14's helper and KILL1 | Q2 | § Assertion shapes | tree |
| F-05 | the tool's last line is a bare `PASSED` (line 619); its four descriptions give four counts | Q7 | § The runs | tree |
| F-06 | `cloud-pair-migration` cannot run on any tree after `e6645cb5ea`; it is retired by code | Q6 | § The runs | tool-run |
| F-07 | `vm-qa` never downs the backend after a suite; guest disks and sockets default to `/tmp`; `down` kills every listener on its port | Q1 | 03 § 3.5 | tree |
| F-08 | the rule's no-network sentence is stale (`rclone-cloud-sync.md:375`, #909) and its `paths:` names four of the nine | Q7 | 01 § The rule | tree |
| F-09 | two tools judge with the host's rclone (1.60.1-DEV, the image ships 1.75.2), two with the host's bash and coreutils | Q2 | § Coverage | tree |
| F-10 | `quay.io/minio/minio:latest`, `dperson/samba:latest` and `pyftpdlib` are unpinned | Q4 | § The runs | tool-run |
| F-12 | `cloud-test-backend ls` swallows every error (`|| true`, lines 629-633) and `backend_files()` ignores its exit (line 1838), so a listing that failed is an empty one; two rows judge absence on such a listing alone and PASS on it: `run_steps.27` ("an unselected system was not uploaded") and KILL4 ("uploaded no invalid archive") | Q3 | § Proofs | tool-run |
| F-13 | no tool among the nine proves a mixed installation under D-CLOUD-175's `/pixelelated` default (a device updated in place keeping its folder beside a fresh install, one cloud); D-CLOUD-158's gate was met on 2026-10-05 for the retired `/Rasteratops` default by `cloud-pair-migration`, now retired. **The coordinator ruled on #660 at 05:22 UTC: the proof is owed, as Backlog #1055 (the coordinator's)**; this slice defers the gap there | Q6 | 01 § The retired tool; `tools/archaeology mixed-installation` | history |
| F-11 | six fixed waits stand in for an event (lines 4915, 5294, 6692, 6910, 7496, 7500); the other 1-5 s sleeps are poll intervals or deliberate mtime separation | Q3 | below, Q3 | tree |

## Finding Verification (Phase 4.5)

Each finding re-read against its artifact at the hash, after it was written:

- **F-01:** `git log --all --oneline --diff-filter=A -- '*cloud_reconcile'` prints nothing. `grep -n '\bAPPLY\b'` shows lines 1771, 2388 and 2433, and line 1765's comment says *"the command fails today and the fixtures with it"*. **Verified.**
- **F-02:** with `APPLY` failing, `both_changed` left the cloud at HB and the device at HA, which is exactly what lines 2451 and 2453 assert. **Verified by reading**; a run needs two guests.
- **F-03:** re-run as `port`/`caps` in both orders: 9010 vs 9013, and WebDAV's caps vs S3's. **Verified.**
- **F-04:** `grep -n '\bcaps()'` shows `def` at 1792 and calls at 2369, 2372-2373 and 6786; the generator's `caps_keys` are empty for all 34 steps. **Verified.**
- **F-05:** line 619 prints `PASSED` or `N CHECK(S) FAILED` and nothing else on success. **Verified.**
- **F-06:** the stage-A run gave rc 2; lines 58-63. **Verified.**
- **F-07:** `vm-qa` has no `cloud-test-backend` call with `down`; lines 98-99 default to `/tmp`; `cloud-test-backend` lines 565-591. **Verified.**
- **F-08:** `rclone-cloud-sync.md:375` and lines 3-14 of its front matter. **Verified.**
- **F-09:** `cloud-connections-test` and `cloud-save-integrity-test --rclone /usr/bin/rclone` use `rclone v1.60.1-DEV`; `projects/ROCKNIX/packages/network/rclone/package.mk:7` gives `PKG_VERSION="1.75.2"`. `cloud-capture-stamp-test` and `cloud-input-test` run `bash` on `PATH` (shims first). **Verified.**
- **F-10:** `cloud-test-backend` lines 118, 134 and 212-214. **Verified.**
- **F-11:** each sleep read with its two preceding lines (Q3 below). **Verified as a lead, not a defect:** none was seen to fail.
- **F-12:** `CLOUD_QA_STATE=/workspace/tmp/m6-t13/no-such-state tools/cloud-test-backend --backend webdav ls` (and `--backend sftp`) gives **rc 0, 0 bytes** for a data directory that does not exist. Step 27's check (`"game.rom" not in listing`, line 1567) on that listing is true. Its only companion check is the device's unit-marker protocol, so nothing in the step asserts that the selected system reached the endpoint. KILL4's (lines 7054-7056) is `not bad_up` over `backend_files(folder)`. Steps 2, 17 and 18 pair their absence check with a presence check from the same listing, so they cannot pass on an empty one. **Verified.**

## Second opinion (Phase 4.6)

**Pending: stage C.** One seat, `gpt` (`openai/gpt-6-astra`, `max`), through
the local Facilitator, after the packet is scanned. `review-plan.json`, the
probe, the refutation and their provenance land under `second-opinions/`,
and each item is graded here with the artifact that decided it.

## Renovation face

### Q1 Modernize

One file holds the single-device suite and six registries: 7,808 lines,
77% of the slice, with one `check()`, one `Fail`, one `main()` and 46
`step()` calls. T14 found its tests good in the shape *one test, one
subject, one oracle*. Here, by contrast, a reader of a PASS line cannot
tell which of 79 rows produced it.

The registries are run by hand. CAP1-14 is about 10 minutes on one guest,
needs no cloud, and could be a `vm-qa` suite (T12's file: a lead). PAIR
needs two guests and A5 and RETENTION cannot pass, so it should not be
wired in until the reconciler exists. KILL needs the monitor and the serial
console, and LINK is already `vm-qa`'s `link` suite.

The seams are shared-host hazards (F-07). Each fix is small: `vm-qa` downs
what it brought up, and `down` stops its own pid, not every listener on its
port.

### Q2 Standards

**The oracle verdict, by `t13-shapes.py` and the lane's review (78 rows):**

| Oracle | Rows | Of which |
| --- | ---: | --- |
| both ends (the host reads the endpoint) | **24** | steps 2, 5, 8, 17, 18, 19, 22, 23, 27, 30; cells A1, A2, A3, A8, A9, A11, A14, RETENTION, LINK2, LINK3, LINK5, LINK6, KILL4, KILL5 |
| a synthetic input (planted, then the device's reaction read) | **44** | the other steps that plant (1, 7, 9-11, 13-16, 20, 24, 26, 28, 29, 31) and the cells A12, A15, CAP1-14, LINK1, LINK4, LINK7, KILL1-3, KILL10-13, KILL15, KILL16, KILL18 |
| the device's own report | **10** | `run_steps.3`, `.4` and `.6` (round trips), `.12`, `.21`, `.25` and `.32`, `prepare_device.1` and `.2`, A5 |

`CONTRACT`, outside the 78, reads both ends.

**`caps()` marks; it never skips. But it marks almost nothing.** The two
rows that read it mark by changing the expectation, not by skipping: A14
expects a null `remote_hash` on a hashless backend, and KILL1 accepts an
in-place commit where the endpoint is not atomic. No step of the
single-device suite reads it (F-04), so a WebDAV PASS and an S3 PASS are
the same 34 assertions, and nothing in the output says which capabilities
the run exercised.

**The host-rclone rows:**
- `cloud-connections-test` runs `cloud_connections` against the host's rclone 1.60.1-DEV. That is the module's choice, and its header says so.
- `cloud-save-integrity-test --rclone` uses the host's rclone as an independent oracle by design, the only second implementation among the nine.

Neither proves anything about the image's rclone 1.75.2.

**The host-bash rows:**
- `cloud-capture-stamp-test` runs `finish()` under the host's bash, with only `date` faked. CAP12 is its guest twin, under the image's busybox.
- `cloud-input-test` runs `wifictl` under host bash and coreutils inside `bwrap`.

Under D-QA-063 (T14's rule), each should say whose tools judged. Neither
does in its output.

### Q3 Bugs

- **F-01, `cloud_reconcile`:** A5 and RETENTION cannot pass, and no recorded run shows them failing. The fix is either the device script, if #22/#23 ever add it (T16's area), or a fixture that says it waits and reports `SKIP - waits for the reconciler` instead of running a command it knows does not exist. A `bug` at stage D, with the constructed case `--only A5,RETENTION --second-port`, which needs two guests.
- **F-02, RETENTION's vacuous PASS lines:** with `seen` false, the head and device-copy checks should not run. A `bug` at stage D, folded with F-01 unless the coordinator splits them.
- **F-03, `--backend` after the subcommand:** a stray argument accepted in silence. A `bug` at stage D; the constructed case is `tools/cloud-test-backend port --backend sftp` printing 9010.
- **F-05, a count that never prints:** the tool's PASS line should say how many checks it certifies, per backend. A `bug` at stage D, or a design row if the coordinator prefers.
- **The no-network step** asserts exit 69 (line 1469). The tool is right and the rule is wrong (#909's item 4; the fix is T4's `fcc7046f0e`).
- **Probes that cannot report absence (blindspot 22):**
  - `cat`'s existence check holds on all three backends (rc 1 on a missing object).
  - **`ls` does not**: both branches end in `|| true` (lines 629-633), so `backend("ls")` returns an empty string with rc 0 for a path, or a whole data directory, that is not there. `backend()`'s `check=True` (line 268) never sees a failure, and `backend_files()` (line 1838) does not even ask.
  - An absence judged on such a listing PASSes (F-12): `run_steps.27` and KILL4. Steps 2, 17 and 18 survive it because each pairs its absence check with a presence check from the same listing.
  - A `bug` at stage D. The constructed case is the `ls` above, rc 0 and empty; the fix is the stage-E `ls` failing on a missing path, and each absence check paired with a presence one.
- **F-11, the sleeps (blindspot 32):** 38 `time.sleep` calls.
  - 11 of the 1-5 s waits are poll intervals inside bounded loops.
  - 3 are deliberate mtime separations, each commented.
  - 6 stand in for an event: 4915 (4 s after a background transfer starts), 5294 (5 s), 6692 (4 s after ES restarts), 6910 (5 s after `touch_offset`), 7496 (2 s after the close key, before the save is checked) and 7500.
  - The rest are sub-second polls or computed waits.

  The six are leads, not defects: none was seen to fail.

### Q4 Currency

| Dependency | Pin | Resolved on 2026-10-25 | Source |
| --- | --- | --- | --- |
| `quay.io/minio/minio:latest` (S3) | none | `sha256:14cea493d9a3...`, `RELEASE.2025-09-07T16-13-09Z`, created 2025-09-07 (local, not pulled) | `docker image inspect` |
| `dperson/samba:latest` (SMB) | none | `sha256:66088b78a198...`, created 2020-07-03 | `docker image inspect` |
| `pyftpdlib` (FTP) | none (`pip install -q pyftpdlib`, lines 212-214) | 2.2.0, installed 2026-09-12 into the default state's venv | `pyftpdlib-2.2.0.dist-info` |
| host `rclone` (two tests' oracle) | the host's package | `v1.60.1-DEV`, against the image's `1.75.2` | `rclone version`; `package.mk:7` |

D-QA-058's baseline is WebDAV, SFTP and MinIO-S3. MinIO is the one baseline
endpoint whose version moves under `:latest`, and on this host it has not
moved in thirteen months because nothing pulls it.

### Q5 Efficiency

The single-device suite's recorded wall time is 81 s a backend (the brief's
figure). Stage A's host runs cost 4.0 s in all. The full set of registries
would add two guests (PAIR), a throttled endpoint and a serial console
(LINK, KILL), and power cuts through the monitor (KILL12, KILL13). Its
guest-minutes are not measured here; the one granted cycle measures the
suite and CAP1-14.

### Q6 Dead ends: the dispositions

These are proposals for the coordinator.

| Item | Disposition proposed | Why |
| --- | --- | --- |
| `cloud-connections-test` | keep; a lead to wire it into `vm-qa` as a host suite (T12's file) | 1.9 s, no guest, a real positive (§ Positives); its host-rclone limit stated (Q2) |
| `cloud-input-test` | keep as a hand-run host test; a lead for the OS-scripts area (Wi-Fi under the cloud prefix) | its subject is `wifictl` and `cloud_oauth`'s input, not a cloud tier; 1.0 s |
| `cloud-capture-stamp-test` | keep; CAP12 is its guest twin | 0.1 s, documented positive seen firing |
| `cloud-save-integrity-test` | keep; a lead to wire it into `vm-qa` as a host suite | 0.1 s, the only second implementation |
| `cloud-save-integrity` | keep as a hand-run verifier | it is a tool, not a test; its input manifest waits for a scoped collector (#517, D-CLOUD-181) |
| `cloud-census` | keep as a hand-run read of a handheld, never run in a slice; a lead to move it out of the cloud prefix | it asserts nothing; its subject is a person's device (D-QA-015), so its reads go through the D-QA-021 filter |
| `cloud-pair-migration` | retire (delete at stage E) | it exits 2 on every tree after `e6645cb5ea`. **Already written:** it ran only on QA guests and the QA endpoint, so nothing on a device or in a person's cloud; its proofs stay in history (`vm-qa-log.md:32`, #354 runs 96-99; the 2026-10-05 entry *Mixed-installation qualification completes*). **The gate it guarded:** D-CLOUD-158's *"the mixed-installation test runs on `tools/vm-pair` before the default ships"*, met on 2026-10-05 for the `/Rasteratops` default, which D-CLOUD-175 retired with the migration on 2026-10-07. Nothing among the nine guards a mixed installation under the `/pixelelated` default (F-13). **Ruled by the coordinator on #660 at 05:22 UTC:** the proof is owed as Backlog #1055; `cloud-pair-migration` stays retired, its removal deferred to #1055 with the gap |
| `cloud_reconcile` (never added) | the fixtures say they wait (Q3, F-01) | D-CLOUD-051, open, asks what the apply step is called; the harness should not name a command before the decision |
| `cloud_migrate_layout` (deleted) | named 0 times by `cloud-round-trip` and 8 by the tool to retire; T15's 55 are T15's | goes with `cloud-pair-migration` |
| the vendored copy (`docs/qa-logs/2026-10-07-cloud-validator/roundtrip/tools/cloud-round-trip`) | keep as evidence, unchanged | it is the 2026-10-07 record's copy (7,795 lines, `b534d174...`), not the tool, and no caller runs it |

### Q7 Clarity

A reader cannot tell from the PASS line what was certified, by which
oracle, or against which backend: the line is `PASSED`. The three
descriptions disagree:
- `vm-qa:36` says *27 steps*.
- The rule's runbook says *exit-4 timing* for a step that asserts 69, and its `paths:` covers four of the nine.
- The tool's header promises *nothing is skipped in silence*, which the suite keeps by marking nothing.

The fix is one line of output: the count of checks, the backend, and the
marked rows. The two descriptions that live elsewhere are leads.

## Instruction File Recommendations

These are proposals for the coordinator; this lane edits no rule.

1. **`rclone-cloud-sync.md`:** line 375's *exit-4 timing* becomes exit 69, which is T4's `fcc7046f0e` under #909. Its `paths:` should add the other five cloud tools, or `tools/cloud-*`.
2. **`tools/vm-qa:36`'s comment:** *27 steps* becomes 32, or better, the count the tool prints (T12's file).
3. **A line under `generic-x64-vm-testing.md`'s QA-backend notes:** `--backend` goes before the subcommand, and two lanes on one host give each run its own `CLOUD_QA_STATE`, `CLOUD_QA_PORT` and `CLOUD_QA_NAME`.

## Quality self-check

- Every finding cites a file:line at `8ebaf8daad` or a run in 02, and was re-read after it was written (Phase 4.5).
- The oracle counts come from the generator and the renderer, which can be re-run, and are not typed: 24 + 44 + 10 = 78.
- The recorded-verdict column cites ledger rows and never summarises them: an early cut read PASS or FAIL off a row's free text and was withdrawn.
- **Not done yet:** the guest cycle, the seat, the punch list and the `bug` issues. Each is named in the scorecard with its stage.


## Context: rclone-cloud-sync.md § Testing it without a cloud account (this tree; under #909)

## Testing it without a cloud account

`tools/cloud-test-backend` serves a directory on the host over WebDAV;
`tools/cloud-round-trip` drives a device through save backup/restore, the
settings-backup archive, and content sync against it
over SSH. A VM from `generic-x64-vm` reaches the host at `10.0.2.2`, so nothing
needs forwarding.

```bash
./tools/cloud-test-backend up                    # WebDAV on :9010
./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --identity <key>
./tools/cloud-test-backend ls                    # what the device uploaded
./tools/cloud-test-backend down

./tools/cloud-test-backend --backend s3 up       # or s3, sftp, smb, ftp (#133)
./tools/cloud-round-trip --host ... --backend s3
```



## Context: rclone-cloud-sync.md § Five backends, and what each one alone can tell you (this tree; under #909)

### Five backends, and what each one alone can tell you

One protocol's answers to *does this file exist*, *what does it hash to* and
*what survives a cut PUT* are not the answers. `--backend` picks among five,
all on this host, all reachable from a guest at `10.0.2.2`, none needing an
account (`generic-x64-vm-testing.md` has the ports and the data paths):

| `--backend` | Stands for | Hashes | Modtimes | Cut PUT |
| --- | --- | --- | --- | --- |
| `webdav` | Dropbox/Drive/OneDrive, the path-based tier | no | **no** | short file |
| `s3` | S3, B2, the bucket tier (#38, #123) | MD5 | yes | **commits or nothing** |
| `sftp` | a NAS or a seedbox; the hash-less remote | no | yes | short file |
| `smb` | the WINDOWS SHARE tier | no | yes | short file |
| `ftp` | the FTP rows, implicit and explicit | no | yes | short file |

**Run a change against more than WebDAV whenever it touches existence
checks, directory creation, layout, comparison or an exit code.** The first
matrix run (2026-09-12, image `d94ca7b159`) found three shipped defects that
WebDAV cannot show, on 33 steps that were green on WebDAV throughout:

- **#141 — on a bucket remote a wrong saves folder reports COMPLETED.** An
  empty folder does not exist on S3, so *not created yet* and *exists and is
  empty* are one observation, and `cloud_restore` resolves it the wrong way:
  a `SAVES_REMOTE` whose root does not exist at all exits **0** with
  `Game saves: COMPLETED`, where every path-based backend exits 1 and offers
  nothing. A typo in the folder name restores nothing and says it worked.
- **#142 — on FTP a missing directory is exit 1, not 3.** rclone surfaces the
  server's `501 "No such directory."` as a general error, so every
  *is it there yet?* branch reads *not created yet* as *your cloud couldn't
  be read*. And with `--retries 1` a copy into a directory that does not
  exist yet loses files: rclone's FTP backend fails its first pass on the
  destination root and only recovers on a retry we do not allow (2 of 3
  files landed).
- **#143 — a refused S3 endpoint is not bounded by our timeouts.** The AWS
  SDK's retryer backs off underneath `--contimeout 15s --timeout 30s
  --retries 1`; one `rclone lsf` against a closed port ran past 2m23s and the
  whole suite took 578 s against 128-156 s on the other four.

Two more traps that only the bucket path shows, found earlier the same way:

- **`rclone lsjson --stat` is not an existence test on a bucket remote.** It
  synthesises a directory entry for *any* path — `utterly-bogus-never-created`
  returns `IsDir: true` on 1.60, 1.74 and 1.75 — how bucket remotes work, not
  a bug awaiting a fix. Use a **listing**: does the path contain anything, or
  does its parent list it?
- **`rclone mkdir` exits 0 while creating nothing.** Empty directories do not
  exist on S3; rclone even says so and still returns success. The standard fix
  is a zero-byte object whose key ends in `/`, which rclone writes with
  **`--s3-directory-markers`** (default off). B2 has no equivalent flag.

### Runbook

```bash
./tools/cloud-test-backend up                       # WebDAV on :9010
./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --identity <key>
./tools/cloud-test-backend ls                       # what the device actually uploaded
./tools/cloud-test-backend down                     # ALWAYS -- see below
```

Four things that cost time on 2026-09-03:

- **`down` matters.** WebDAV, SFTP and FTP run as host processes and survive
  the session that started them; S3 and SMB are containers. A stale one
  holding the port makes the next `up` fail with `address already in use`.
  Since #133 each backend has a port of its own (9010/9012/9013/9014/9015) so
  several can be up at once and `down` takes down only the one named by
  `--backend`; `CLOUD_QA_PORT` still moves one if you need two of the same
  kind.
- **The host's rclone is not the device's.** This host had **1.60.1-DEV**; the
  device ships **1.74.4**. Backend options differ across that gap —
  `--s3-directory-markers` does not exist in 1.60. Test rclone behaviour by
  running rclone *on the device* against the QA endpoint, not on the host.
- **A real device can reach the host's MinIO too**, not just a VM: bind the
  backend and point the device's rclone config at the host's LAN address. Faster
  than booting a VM when the question is purely about rclone semantics.
- The device reaches a VM-host at `10.0.2.2`; a LAN device needs the real IP.

### Bucket remotes behave differently, and it is not a detail

The two traps above (`lsjson --stat`, `mkdir`) are the bucket tier's, and
both were found by running the S3 path. Three call sites branched on the
first, so on S3 the migration always refused ("destination already exists"),
the content-restore legacy fallback was dead, and the seeding report could
only ever say OK.

The consequence for design: a folder we want a player to *see* needs either a
marker or a file in it. Our seeded folders get both — the marker so the folder
persists, and a `README.txt` because a folder that says what belongs in it is
worth more than an empty one.

Getting a VM to an SSH target the driver can use: boot it, then over the
serial console (`-serial unix:`) enable sshd and drop in a key —
`systemctl start sshd`, then write your public key to
`/storage/.ssh/authorized_keys` (mode 600, directory 700). SSH is off on a
fresh image, and the console gives a root shell without login.

- **WebDAV is the default, and the harshest.** With `vendor=other` it carries
  neither hashes nor modtimes, so rclone compares by size alone — the shape of
  #53 — and a bug only WebDAV can catch is one WebDAV must keep catching.
- **Bucket and share remotes need a different `SAVES_REMOTE`.** Dropbox/Drive/OneDrive are path-based, so
  `SAVES_REMOTE="/GAMES"` is a folder. On S3 and B2 the first path component is the
  *bucket*. rclone creates buckets on demand, so a missing one is not the
  problem - the problem is that `GAMES` is not a **legal** bucket name
  (lowercase only, 3-63 chars), so it is rejected with `InvalidBucketName`
  before anything can be created (issue #38). SMB has the same shape with the
  *share* in place of the bucket, and SFTP a third — every path absolute,
  because an sshd running as an ordinary user cannot chroot. The backend
  states what it needs (`cloud-test-backend saves-remote`, and
  `endpoint-prefix` for what to strip) so no caller hard-codes a shape.
- **Local on purpose.** These tests exercise credential stripping and backup
  contents - the code paths most likely to leak a token into an archive, a log
  or a work log. A throwaway WebDAV password is worth nothing if it escapes.
- **The active connection is asserted, not assumed.** QA snapshots and restores
  both credentials and selection, including an absent or explicit empty selection.
  It refuses transfers unless the active connection is the QA endpoint. Only
  historical images without explicit selection use their old first-remote rule.
- **Restore is destructive**, so the suite works in `/storage/cloud-qa` unless
  `--real-roms` is passed. Never point it at a device with saves you want.
- An assertion that only holds because nothing happened is worse than no
  assertion: the allowlist check skips rather than passes when the upload
  produced nothing.

**Standing local qualification (D-QA-058, #462):** verify the candidate's
installed rclone/cloud scripts against WebDAV, SFTP and MinIO/S3. Keep a
separate report for each backend, exact image identity and actual endpoint
readback. Use the durable watcher and verify guest/backend cleanup. The
broader SMB/FTP matrix remains #133/#232; it is not a hosted-account gate.

Dropbox credentials, an offsite endpoint and hosted-provider accounts are
**not RC prerequisites now or in future routine qualification** (D-QA-041,
D-QA-058). Authenticated OAuth/token refresh and provider-owned pages remain
outside local-protocol proof; record them as optional observations when QA
access exists, without claiming they passed. #463 owns the deferred Dropbox
trust-page observation. This does not defer the separate RetroAchievements
award/reconnect proof. "We would need a real provider" is not an answer to
*can this be done on the VM?* (`vm-first.md`). The wizard's local gates
(`--connected`, `--check`, `--free-auth-port`) do test here.


## Context: docs/blindspot-register.md entry 31

## 31. A harness that writes and reads through the same wrong path agrees with itself

**Committed:** 2026-09-06 (found 2026-09-07). On MinIO the round-trip suite's
seeding step put the owner's note at the endpoint and read it back through
the same helper, and both doubled the bucket: `rocknix-qa/rocknix-qa/GAMES`.
"The owner's note survived a second seeding" passed on every MinIO run, about
a folder the device never looked at. The same day, `rclone cat` of a missing
S3 key exited 0 with no output, and "the manifest reached the cloud" passed on
MinIO for a manifest that was never there.

**The shape:** a check whose fixture and whose reading share a path derivation
is comparing the harness with itself. It cannot fail on the thing it names,
because the device under test is not on the path at all. Blindspot 22's rule
— a check that cannot run has not passed — has a sibling: a check that runs
somewhere the device does not look has not tested the device.

**The fix:** derive endpoint paths in one place (`epath()`), with the S3
bucket stripped where the backend's own commands add it; make the backend's
`cat` fail on a missing key; and, for any "it reached the cloud" assertion,
ask what the device would have had to do for it to pass — if the answer is
nothing, it is not evidence. See `engineering-practices.md` § "Guards must
fail closed".


## File: tools/cloud-round-trip (at 8ebaf8daad, 7808 lines)

```text
    1  #!/usr/bin/env python3
    2  """Round-trip the cloud-sync scripts against a local QA cloud backend.
    3  
    4  Drives a ROCKNIX device over SSH - a VM from generic-x64-vm, or real hardware
    5  on the LAN - through backup, restore and content sync, and checks the result
    6  from both ends: file contents on the device, and objects at the endpoint.
    7  
    8      ./tools/cloud-test-backend up
    9      ./tools/cloud-round-trip --host root@127.0.0.1 --port 10022
   10  
   11  --backend picks which of tools/cloud-test-backend's five endpoints to drive
   12  (#133); bring the same one up first. WebDAV is the default and the harshest
   13  -- vendor=other carries neither hashes nor modtimes, so rclone compares by
   14  size alone -- and the other four each answer "does this exist", "what does
   15  it hash to" and "what survives a cut PUT" differently:
   16  
   17      ./tools/cloud-test-backend --backend sftp up
   18      ./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --backend sftp
   19  
   20  A step that legitimately cannot hold on a backend reads its reason off
   21  `cloud-test-backend caps` and says so; nothing is skipped in silence.
   22      ./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --second-port 10023 \
   23          --identity /tmp/rocknix-vm-pair/qa-key          # the VM pair: two devices, one cloud
   24  
   25  With --second-port the two-device fixtures of #35 run after the single-device
   26  suite (--only A1,A9 runs just those): a conflict is a change on both sides
   27  since two devices last agreed, and only a pair can make one (D-QA-009).
   28  
   29      ./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --identity ... \
   30          --path-prefix /tmp/qa-bin --only CAP1,CAP2,CAP3,CAP4,CAP5,CAP6,CAP7,CAP8,CAP9,CAP10,CAP11,CAP12,CAP13,CAP14
   31  
   32  --only CAP1..CAP14 runs #21's capture fixtures against a staged cloud_capture
   33  on one device with no cloud at all -- no MinIO, no remote, no second guest
   34  (see the capture section below for what to stage). --only A15 runs #86's
   35  identity fixture: one device and the QA endpoint, no second guest. --list
   36  prints every registry without touching a device.
   37  
   38      CLOUD_QA_BWLIMIT=200k ./tools/cloud-test-backend up
   39      ./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --identity ... \
   40          --only LINK1,LINK2,LINK3,LINK4,LINK5,LINK6,LINK7 --serial-socket /tmp/rocknix-qemu-serial.sock
   41  
   42  --only LINK1..LINK7 (or --link after the suite) runs #103's link-loss cells:
   43  each starts a cloud operation, cuts the guest's link over its serial console
   44  at a named phase, restores it 40 s later and asserts the run ended within
   45  90 s with an honest exit and nothing partial left behind. They need a
   46  throttled endpoint (WebDAV, or s3 behind cloud-test-backend's proxy) and a
   47  guest with a serial console (a headless VM); on a handheld they are skipped,
   48  with a line saying so.
   49  
   50      ./tools/cloud-round-trip --host root@127.0.0.1 --port 10024 --identity ... \
   51          --only KILL1,KILL2,KILL3,KILL4,KILL5,KILL10,KILL11,KILL12,KILL13,KILL15,KILL16,KILL18 \
   52          --serial-socket /tmp/rocknix-qemu-serial-c.sock --monitor-socket /tmp/rocknix-qemu-monitor-c.sock
   53  
   54  --only KILL1,... (or --kill after the suite) runs #105's KILL cells: each
   55  writer killed at every step it has (a SIGKILL at rclone's per-file line, a
   56  guest-side watcher on a filesystem condition, an exported bash function
   57  that kills from inside the step, a planted torn file), then asserted on
   58  D-CLOUD-078 -- the previous state is what remains, the stamp never says 0,
   59  a re-run completes. KILL12 and KILL13 are power cuts: `system_reset` over
   60  QEMU's monitor with the config files planted torn, or behind
   61  EmulationStation's own page-close writers (the walk in
   62  tools/vm-walks/ui-settings-toggle.steps). Cells needing no endpoint prepare
   63  the device locally; the two power-cut cells need the serial console and the
   64  monitor and are skipped with a line without them. Every fixture in every
   65  registry now ends in litter_scan() -- one last-known-good of each record, no
   66  writer's litter -- and every failure fixture runs its output through
   67  assert_message() -- no exit code, log path or tool name where a player
   68  reads (the three outcome words are asserted by default; --no-vocabulary skips that).
   69  
   70  Two guards, both load-bearing:
   71  
   72  * Cloud tools use the explicit active connection (legacy images use their
   73    first remote). The suite preserves that selection and asserts the QA
   74    connection before any transfer; another saved account is never assumed safe.
   75  * Restore is destructive by design. The suite works in a scratch tree by
   76    default and only touches /storage/roms with --real-roms, so pointing this
   77    at a device with real saves cannot quietly delete them.
   78  """
   79  
   80  import argparse
   81  import hashlib
   82  import json
   83  import os
   84  import re
   85  import shlex
   86  import stat
   87  import subprocess
   88  import sys
   89  import time
   90  
   91  HERE = os.path.dirname(os.path.abspath(__file__))
   92  BACKEND = os.path.join(HERE, "cloud-test-backend")
   93  
   94  SCRATCH = "/storage/cloud-qa"
   95  CONF = "/storage/.config/cloud_sync.conf"
   96  RCLONE_CONF = "/storage/.config/rclone/rclone.conf"
   97  
   98  # Content chosen to catch the failure modes that have actually bitten:
   99  # a nested path, a name with a space (quoting), and a file the allowlist
  100  # must exclude - the filter is what stands between --delete-excluded and
  101  # somebody's cloud data.
  102  FIXTURES = {
  103      "saves/game1.srm": b"save-one-v1",
  104      "saves/nested/deep/game2.srm": b"save-two-v1",
  105      "saves/game with space.srm": b"save-three-v1",
  106      "savestates/game1.state": b"state-one-v1",
  107      # Standalone N64 writes beside the ROM, not into a save directory: every
  108      # shipped mupen64plus.cfg sets SaveSRAMPath to /storage/roms/n64. The
  109      # allowlist's /n64/save/*.eep lines match the libretro layout and never
  110      # matched these, so they were carried by nothing until #89 (D-CLOUD-086).
  111      # Both depths are here on purpose: the widened rules must take the file
  112      # beside the ROM without dropping the one in the save directory.
  113      "n64/Mario Probe 64.eep": b"n64-eeprom-v1",
  114      "n64/Mario Probe 64.mpk": b"n64-controller-pak-v1",
  115      "n64/Mario Probe 64.sra": b"n64-sram-v1",
  116      "n64/Mario Probe 64.fla": b"n64-flashram-v1",
  117      "n64/save/Libretro Probe 64.eep": b"n64-libretro-layout-v1",
  118  }
  119  # The ROM beside those N64 saves must NOT ride along on the saves tier: it is
  120  # the ROMs and BIOS tier's, and an allowlist that took *.z64 would put a
  121  # player's whole N64 library into their saves folder.
  122  EXCLUDED = {"saves/scratch.tmp": b"should-never-leave-the-device",
  123              "n64/Mario Probe 64.z64": b"a-rom-must-not-ride-the-saves-tier"}
  124  
  125  # Content sync is a different code path: whole directories of ROMs and BIOS,
  126  # not allowlisted save files. Its directory is created and removed by the test
  127  # and named so it is obvious what it is if a run is interrupted.
  128  # The settings-backup archive: phase 2 of both scripts. Nothing exercised this
  129  # until it was found broken - cloud_restore filtered on "backup/*.zip" while
  130  # the archive sits at the root of SETTINGS_REMOTE, so it restored nothing and
  131  # still reported SUCCESS. A silent no-op is exactly what a round-trip catches.
  132  # A dated name, because the uploader dates an undated one on the way up
  133  # (ROCKNIX-backup-qa.zip went up as 2026_09_06-180107-ROCKNIX-backup-qa.zip)
  134  # and the restorer brings the dated name back -- a harness looking for its
  135  # own undated path on either side saw nothing (Gate 0, #35).
  136  # The pre-label shape, on purpose. Since 2026-09-08 backuptool writes
  137  # <stamp>-<device>-ROCKNIX_SETTINGS.tar.gz, and every device in the field
  138  # still holds archives named ROCKNIX_ locally and in the cloud; this one
  139  # stands for those, so the round trip proves the upgrade path -- an unlabelled
  140  # archive is still uploaded, and still comes back through the restorer's
  141  # newest-overall fallback. The labelled shape is asserted on the archive
  142  # backuptool itself writes, and the retention step plants both shapes side by
  143  # side.
  144  ARCHIVE_NAME = "2026_01_01-000000-ROCKNIX_SETTINGS.tar.gz"
  145  # Real archives, since 2026-09-10: cloud_backup lists an archive (tar -tzf)
  146  # before it sends it and refuses one that does not list -- so a planted run
  147  # of bytes is "damaged" and never uploaded, which is how the whole settings
  148  # step went red the first time the suite met tranche A's scripts. One member,
  149  # storage/.config/qa-suite/settings.cfg, whose text says which version.
  150  def _settings_archive(version, pad=0):
  151      import io, tarfile, gzip
  152      raw = io.BytesIO()
  153      with tarfile.open(fileobj=raw, mode="w", format=tarfile.GNU_FORMAT) as t:
  154          body = (f"qa-suite-settings={version}\n" + " " * pad).encode()
  155          ti = tarfile.TarInfo("storage/.config/qa-suite/settings.cfg")
  156          ti.size = len(body); ti.mtime = 1700000000; ti.mode = 0o644
  157          t.addfile(ti, io.BytesIO(body))
  158      return gzip.compress(raw.getvalue(), mtime=0)
  159  
  160  def _same_size_pair():
  161      """v1 and v2 at the same compressed size. A remote with no modtimes and no
  162      hashes leaves rclone comparing by size alone, so a second archive of
  163      identical size was silently never uploaded while the run reported success
  164      (#53); the regression case needs two archives that differ and weigh the
  165      same. Padding inside the member finds a pair; the deflate of two texts
  166      that differ by one character almost always lands on the same length."""
  167      a = _settings_archive("v1")
  168      for pad in range(0, 64):
  169          b = _settings_archive("v2", pad)
  170          if len(b) == len(a):
  171              return a, b
  172      raise SystemExit("could not build two settings archives of the same size")
  173  
  174  ARCHIVE_BODY, ARCHIVE_BODY_V2 = _same_size_pair()
  175  assert len(ARCHIVE_BODY_V2) == len(ARCHIVE_BODY)
  176  
  177  # A system EmulationStation declares (D-CLOUD-019): the content tier lists
  178  # only those. Vectrex, because nobody's library is likely to be there -- and
  179  # the harness refuses to run if it is (see the content step).
  180  CONTENT_DIR = "vectrex"
  181  CONTENT_FIXTURES = {
  182      "rom1.bin": b"rom-one",
  183      "sub/rom2.bin": b"rom-two",
  184      "rom with space.bin": b"rom-three",
  185  }
  186  
  187  
  188  class Fail(Exception):
  189      pass
  190  
  191  
  192  class Device:
  193      def __init__(self, host, port, identity=None, path_prefix=None):
  194          # --path-prefix: a directory on the device put first on PATH for every
  195          # command, so a script fixed on the host can be proven against the
  196          # suite before an image carries it (the VM tests it first, D-QA-007).
  197          self.path_prefix = path_prefix
  198          self.host, self.port = host, port
  199          # One multiplexed connection per device: a fixture makes hundreds of
  200          # calls, and a fresh handshake costs ~90 ms against ~5 ms over the
  201          # control socket. Its path must stay under 108 bytes, which rules
  202          # out any scratch directory, so it lives in /tmp.
  203          self.base = ["ssh", "-o", "StrictHostKeyChecking=no",
  204                       "-o", "UserKnownHostsFile=/dev/null",
  205                       "-o", "LogLevel=ERROR",
  206                       "-o", "ControlMaster=auto", "-o", f"ControlPath=/tmp/crt-{os.getuid()}-%C",
  207                       "-o", "ControlPersist=120", "-o", "ConnectTimeout=20", "-p", str(port)]
  208          if identity:
  209              self.base += ["-i", identity]
  210          self.base.append(host)
  211  
  212      def disconnect(self):
  213          """Close the multiplexed connection. A command sent over a master
  214          whose guest has lost its link blocks until TCP gives up or the link
  215          returns; the LINK fixtures close it before the cut and let the next
  216          command open a fresh one once the link is back."""
  217          subprocess.run(self.base[:-1] + ["-O", "exit", self.host], capture_output=True)
  218  
  219      def run(self, cmd, check=True):
  220          if self.path_prefix:
  221              cmd = f"PATH={shlex.quote(self.path_prefix)}:$PATH; " + cmd
  222          p = subprocess.run(self.base + [cmd], capture_output=True, text=True)
  223          if check and p.returncode != 0:
  224              raise Fail(f"{cmd!r} exited {p.returncode}: {p.stderr.strip() or p.stdout.strip()}")
  225          return p.stdout
  226  
  227      def write(self, path, data: bytes):
  228          self.run(f"mkdir -p {shlex.quote(os.path.dirname(path))}")
  229          p = subprocess.run(self.base + [f"cat > {shlex.quote(path)}"],
  230                             input=data, capture_output=True)
  231          if p.returncode != 0:
  232              raise Fail(f"writing {path}: {p.stderr.decode().strip()}")
  233  
  234      def sha(self, path):
  235          out = self.run(f"sha256sum {shlex.quote(path)} 2>/dev/null || true")
  236          return out.split()[0] if out.strip() else None
  237  
  238  
  239  class Serial:
  240      """The guest's serial console, through tools/vm-serial (#103).
  241  
  242      The LINK fixtures need one channel that survives the guest losing its
  243      network: the cut and the restore go over it, and so does the poll for
  244      the run's exit while the link is down. It is optional -- a handheld has
  245      no serial console -- and a fixture that needs it is skipped with a line
  246      saying so. `usable` is a check that the socket is a socket and the tool
  247      is executable; whether the console belongs to the device on --host is
  248      proven separately (Link.assert_same_guest), because cutting the link of
  249      the wrong machine is exactly the kind of mistake nothing would report."""
  250  
  251      def __init__(self, socket_path, tool):
  252          self.socket, self.tool = socket_path, tool
  253  
  254      def usable(self):
  255          try:
  256              return stat.S_ISSOCK(os.stat(self.socket).st_mode) and os.access(self.tool, os.X_OK)
  257          except OSError:
  258              return False
  259  
  260      def run(self, cmd, timeout=30):
  261          p = subprocess.run([self.tool, "--socket", self.socket, "--timeout", str(timeout), "sh", cmd],
  262                             capture_output=True, text=True, timeout=timeout + 20)
  263          if p.returncode != 0:
  264              raise Fail(f"serial {cmd!r}: {(p.stderr or p.stdout).strip() or 'no END marker'}")
  265          return p.stdout
  266  
  267  
  268  def backend(*args):
  269      return subprocess.run([BACKEND, *args], capture_output=True, text=True,
  270                            check=True).stdout
  271  
  272  
  273  def step(name):
  274      print(f"\n=== {name}")
  275  
  276  
  277  def check(cond, ok, bad):
  278      print(f"    {'PASS' if cond else 'FAIL'}  {ok if cond else bad}")
  279      return cond
  280  
  281  
  282  class Prepared:
  283      """A device the harness has pointed at the QA endpoint, and what it
  284      looked like before, so it can be put back whatever happens."""
  285  
  286      def __init__(self, dev):
  287          self.dev = dev
  288          self.settings = {}
  289          self.prev_paths = {}
  290          self.prev_rclone_conf = ""
  291          self.prev_active = None
  292          # A capture-only run (prepare_local) reads no rclone.conf and asks the
  293          # backend for nothing; restore_device must then put back neither.
  294          self.local_only = False
  295  
  296  
  297  # Only images predating explicit selection may use the historical fallback.
  298  ACTIVE_COMMAND = 'if test -f "$(dirname "$(command -v cloud_remote)")/cloud_connections.py"; then cloud_remote active; else rclone listremotes 2>/dev/null | head -1; fi'
  299  
  300  def active_remote(dev):
  301      return dev.run(ACTIVE_COMMAND).strip()
  302  
  303  
  304  def prepare_device(dev, remote, root, args, prepared, which=""):
  305      """Point one device at the QA endpoint. It is appended to `prepared` as
  306      soon as its previous state is captured -- before anything is written --
  307      so the block that restores devices covers it even if this raises."""
  308      p = Prepared(dev)
  309      step(f"device {which}reachable and equipped")
  310      who = dev.run("echo ok", check=False).strip()
  311      if not check(who == "ok", "ssh works", "no shell over ssh"):
  312          raise Fail(f"no shell over ssh on {dev.host} port {dev.port}")
  313      have = dev.run("command -v rclone cloud_backup cloud_restore || true")
  314      check("rclone" in have and "cloud_backup" in have,
  315            "rclone and cloud scripts present",
  316            "device is missing rclone or the cloud scripts")
  317  
  318      step(f"point device {which}at the QA bucket" if which else "point the device at the QA bucket")
  319      # The device's own remote comes back at the end: a device the suite has
  320      # finished with has the remote it started with (Gate 0, #35).
  321      p.prev_rclone_conf = dev.run(f"cat {RCLONE_CONF} 2>/dev/null || true")
  322      if dev.run(f"test -f {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection && echo present", check=False).strip() == "present":
  323          p.prev_active = dev.run(f"cat {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection")
  324      for key in ("SAVESPATH", "SETTINGS_BACKUPS", "SAVES_REMOTE", "SETTINGS_REMOTE", "CONTENT_REMOTE",
  325                  "BACKUPPATH", "BACKUPFOLDER", "SYNCPATH", "SYNCPATH_BACKUP", "CONTENTPATH"):
  326          p.prev_paths[key] = dev.run(f"grep -m1 '^{key}=' {CONF} 2>/dev/null || true").strip()
  327      prepared.append(p)
  328      dev.run(f"mkdir -p {os.path.dirname(RCLONE_CONF)}")
  329      dev.write(RCLONE_CONF, backend("rclone-conf").encode())
  330      dev.write(RCLONE_CONF.rsplit("/", 1)[0] + "/active-connection", (remote + "\n").encode())
  331      dev.run(f"chmod 600 {RCLONE_CONF} {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection")
  332      first = active_remote(dev).rstrip(":")
  333      if not check(first == remote,
  334                   f"active remote is {remote!r}, which is what the scripts will use",
  335                   f"active remote is {first!r}, not {remote!r} - refusing to sync "
  336                   f"someone else's account"):
  337          raise Fail("refusing to sync someone else's account")
  338  
  339      settings = {}
  340      if not args.real_roms:
  341          # Keep the scripts' own defaults for everything except where they
  342          # read and write, so the code under test is unchanged.
  343          dev.run(f"mkdir -p {SCRATCH}")
  344          # Remember what these were. Pointing a device at a scratch tree and
  345          # leaving it there means its next real backup silently captures
  346          # nothing -- the failure this suite exists to catch, caused by the
  347          # suite. Found when a later manual run reported "Backup folder
  348          # /storage/cloud-qa/backup does not exist" on a device the test had
  349          # finished with.
  350          settings.update({"SAVESPATH": SCRATCH,
  351                           "SETTINGS_BACKUPS": f"{SCRATCH}/backup"})
  352  
  353      # A bucket-based endpoint needs the bucket as the first path component,
  354      # and the shipped "/GAMES" is not a legal bucket name (issue #38). The
  355      # backend states what it needs rather than the driver assuming.
  356      syncpath = backend("saves-remote").strip()
  357      settings["SAVES_REMOTE"] = syncpath
  358      # A SIBLING of syncpath, not a child. Phase 1 syncs syncpath with
  359      # --delete-excluded and the archive is excluded, so a nested path gets
  360      # deleted there; a full run masks it because phase 2 re-uploads, but a
  361      # --saves-only run deletes the archives and puts nothing back.
  362      settings["SETTINGS_REMOTE"] = backend("settings-remote").strip()
  363      # cloud_content_* default to the remote root, which on a bucket-based
  364      # endpoint means a bucket per content directory (#38, same cause).
  365      settings["CONTENT_REMOTE"] = backend("content-remote").strip()
  366  
  367      # An image that has not renamed its keys (before #73) reads the old
  368      # names; write what the scripts on this device actually read
  369      # (D-UI-022, read-old-if-new-absent -- from the harness's side).
  370      old_names = {"SAVESPATH": "BACKUPPATH", "SETTINGS_BACKUPS": "BACKUPFOLDER",
  371                   "SAVES_REMOTE": "SYNCPATH", "SETTINGS_REMOTE": "SYNCPATH_BACKUP",
  372                   "CONTENT_REMOTE": "CONTENTPATH"}
  373      new_keys = "SAVES_REMOTE" in dev.run("cat $(command -v cloud_backup) 2>/dev/null || true")
  374      if not new_keys:
  375          settings = {old_names[k]: v for k, v in settings.items()}
  376          print("    old key names: this image predates the rename")
  377      p.prev_paths = {k: v for k, v in p.prev_paths.items() if k in settings}
  378      apply_settings(dev, settings)
  379      p.settings = settings
  380      if not args.real_roms:
  381          print(f"    scratch tree {SCRATCH} (pass --real-roms to use /storage/roms)")
  382      print(f"    SAVES_REMOTE {syncpath} on the {backend('backend').strip()} endpoint")
  383      return p
  384  
  385  
  386  def assert_two_devices(a, b):
  387      """Two guests are two devices only if cloud_device_id says so, and every
  388      two-device fixture rests on that: with one id they would write one
  389      manifest-<id>.json, one settings folder and one set of agreement records,
  390      and agree with themselves (blindspot 31's shape). It hashes the permanent
  391      MAC, and until fork #91 tools/vm-pair started both guests on the profile's
  392      fixed address -- so both printed one id, and this harness rewrote b's to
  393      "<id>-second" for the run, which put every pair fixture on an identity the
  394      harness had invented. Now a shared id stops the run before either device
  395      is prepared: nothing is written, so there is nothing to put back.
  396  
  397      Runs the tool as the fixtures do (cloud_device_id, on each guest's own
  398      PATH prefix); an id that cannot be read fails the same way, because a
  399      check that could not run has not passed."""
  400      step("the two devices are two devices, not one id twice (#91)")
  401      ids = [d.run("cloud_device_id 2>/dev/null || true").strip() for d in (a, b)]
  402      if check(all(ids) and ids[0] != ids[1],
  403               f"a is {ids[0]}, b is {ids[1]}",
  404               f"a is {ids[0] or 'no id'}, b is {ids[1] or 'no id'} -- one id, or none, between two devices (#91)"):
  405          return
  406      # Which remedy: a blank id is the tool missing or failing, not a clone; a
  407      # guest pair on one MAC needs `tools/vm-pair up` again (the id is derived
  408      # from the address and stored on first boot, so clearing the stored one
  409      # re-derives the same); a pair on two MACs with one id is a stale clone
  410      # -- A11 writes a's id onto b and puts it back, and an interrupted run
  411      # can leave it -- and there the stored id is what to clear.
  412      macs = [d.run("cat /sys/class/net/eth0/address 2>/dev/null || true").strip() for d in (a, b)]
  413      if not all(ids):
  414          why = (f"cloud_device_id printed nothing on {'a' if not ids[0] else 'b'}: the tool is missing there or "
  415                 "failed (check `command -v cloud_device_id` on that guest, and --path-prefix)")
  416      elif macs[0] and macs[0] == macs[1]:
  417          why = (f"both guests carry the MAC {macs[0]}: this pair predates vm-pair giving guest b its own address; "
  418                 "re-create it with `tools/vm-pair up <img.gz>` (clearing b's stored id alone re-derives the same one)")
  419      else:
  420          why = (f"the MACs differ ({macs[0] or '?'} / {macs[1] or '?'}), so b's stored id is a stale clone; "
  421                 f"remove {ID_FILE} on b and run again")
  422      raise Fail(f"refusing the two-device fixtures: {why} (#91)")
  423  
  424  
  425  def prepare_local(dev, root, args, prepared, keys=("SAVESPATH",), capture=True):
  426      """Point one device's saves root at the scratch tree and nothing else: no
  427      remote, no bucket, no second guest. The capture fixtures (#21) drive a
  428      producer that opens no socket, so the QA endpoint is never asked for
  429      anything and the device's rclone.conf is never read -- which is why
  430      restore_device must not "put back" a remote this prepare never captured
  431      (as written it deleted the file whenever prev_rclone_conf was blank)."""
  432      if args.real_roms:
  433          raise Fail("the capture fixtures empty the saves root between runs; they never run against real ROMs")
  434      p = Prepared(dev)
  435      p.local_only = True
  436      step("device reachable and equipped (local: no cloud)")
  437      who = dev.run("echo ok", check=False).strip()
  438      if not check(who == "ok", "ssh works", "no shell over ssh"):
  439          raise Fail(f"no shell over ssh on {dev.host} port {dev.port}")
  440      have = dev.run("command -v jq cloud_device_id cloud_saves_root cloud_capture || true")
  441      check(all(t in have for t in ("jq", "cloud_device_id", "cloud_saves_root")),
  442            "jq and the sibling helpers present", "device is missing jq, cloud_device_id or cloud_saves_root")
  443      if capture:
  444          check("cloud_capture" in have, "cloud_capture resolves (staged by hand under --path-prefix)",
  445                "cloud_capture does not resolve: stage it into the prefix directory; every fixture will fail its setup")
  446      step("point the device's saves root at the scratch tree")
  447      for key in keys:
  448          p.prev_paths[key] = dev.run(f"grep -m1 '^{key}=' {CONF} 2>/dev/null || true").strip()
  449      prepared.append(p)
  450      dev.run(f"mkdir -p {shlex.quote(root)}")
  451      p.settings = {"SAVESPATH": root}
  452      if "SETTINGS_BACKUPS" in keys:
  453          p.settings["SETTINGS_BACKUPS"] = f"{root}/backup"
  454      apply_settings(dev, p.settings)
  455      print(f"    scratch tree {root}; {' and '.join(keys)} point at it for the run; no remote is touched")
  456      return p
  457  
  458  
  459  def list_fixtures():
  460      """The registries, for --list: what --only can name, without a device."""
  461      print("two-device fixtures (need --second-port; --only A1,A9,...):")
  462      for key, title, _ in PAIR_FIXTURES:
  463          print(f"  {key:<10}{title}")
  464      print(f"  {'CONTRACT':<10}#9's transport contract under the reconciler (see --transport)")
  465      print("\nsingle-device cloud fixtures (one device and the QA endpoint; --only A15):")
  466      for key, title, _ in SOLO_FIXTURES:
  467          print(f"  {key:<10}{title}")
  468      print("\ncapture fixtures (one device, no cloud; --only CAP1,...,CAP14):")
  469      for key, title, _ in CAPTURE_FIXTURES:
  470          print(f"  {key:<10}{title}")
  471      print("\nlink-loss fixtures (one guest, the throttled QA endpoint, and its serial console; --link, or --only LINK1,...,LINK7):")
  472      for key, title, _ in LINK_FIXTURES:
  473          print(f"  {key:<10}{title}")
  474      print("\nKILL cells (a writer killed at every step, the config files power-cut; --kill, or --only KILL1,...; #105):")
  475      print(f"  {'':<10}{'needs':<22}what")
  476      for key, title, _, needs in KILL_FIXTURES:
  477          need = ", ".join(KILL_NEEDS_TEXT[n] for n in sorted(needs)) or "none (local)"
  478          print(f"  {key:<10}{need:<22}{title}")
  479  
  480  
  481  def main():
  482      ap = argparse.ArgumentParser(description=__doc__,
  483                                   formatter_class=argparse.RawDescriptionHelpFormatter)
  484      ap.add_argument("--host", help="ssh target, e.g. root@127.0.0.1 (required unless --list)")
  485      ap.add_argument("--port", type=int, default=10022)
  486      ap.add_argument("--identity", help="ssh private key")
  487      ap.add_argument("--real-roms", action="store_true",
  488                      help="use /storage/roms instead of a scratch tree (DESTRUCTIVE)")
  489      ap.add_argument("--keep", action="store_true", help="leave fixtures in place")
  490      ap.add_argument("--path-prefix", help="a directory on the device to put first on PATH (scripts under test, before an image carries them)")
  491      ap.add_argument("--second-port", type=int,
  492                      help="ssh port of a second device -- the VM pair's guest b -- which turns on the two-device fixtures (D-QA-009)")
  493      ap.add_argument("--second-host", help="ssh target of the second device (default: the same as --host)")
  494      ap.add_argument("--only", help="run only these fixtures, skipping the single-device suite (comma-separated: A1,A9,CONTRACT "
  495                      "for the two-device set, which needs --second-port; CAP1..CAP14 for the capture set, one device, no cloud)")
  496      ap.add_argument("--list", action="store_true", help="print the fixture registries and exit without touching a device")
  497      ap.add_argument("--transport", default="copy,bisync", help="transports for #9's contract fixtures: copy, bisync, or both (default)")
  498      ap.add_argument("--bisync-flags", default="", help="extra flags for every rclone bisync run (Gate 11 variants)")
  499      ap.add_argument("--dump", help="a host directory to write raw outputs into: every transport run's (Gate 11's record), "
  500                      "and each LINK cell's detached run and re-run (<dump>/LINKn/{out,rc,rerun.out})")
  501      ap.add_argument("--link", action="store_true",
  502                      help="run the link-loss fixtures LINK1..LINK7 after the suite (#103); they take minutes and need the guest's serial console")
  503      ap.add_argument("--serial-socket", default="/tmp/rocknix-qemu-serial.sock",
  504                      help="the guest's serial console socket, from generic-x64-vm run --headless (default: %(default)s); "
  505                           "the link-loss fixtures are skipped when it is not there")
  506      ap.add_argument("--vm-serial", default=os.path.join(HERE, "vm-serial"), help="the serial client (default: %(default)s)")
  507      ap.add_argument("--link-restore-after", type=float, default=40,
  508                      help="seconds after the cut at which the link is restored (default: %(default)s; 120 shows an unbounded run overshoot the bound)")
  509      ap.add_argument("--kill", action="store_true",
  510                      help="run the KILL cells after the suite (#105): a writer killed at every step, the config files power-cut; "
  511                           "--only KILL1,... for a subset (cells needing no endpoint prepare the device locally)")
  512      ap.add_argument("--monitor-socket", default="/tmp/rocknix-qemu-monitor.sock",
  513                      help="QEMU's monitor socket, from generic-x64-vm run --headless (default: %(default)s); the power-cut cells "
  514                           "KILL12/KILL13 are skipped when it is not there")
  515      ap.add_argument("--power-cut-trials", type=int, default=3, help="KILL13 arm A: how many of --cut-after-ms to run (default: %(default)s)")
  516      ap.add_argument("--cut-after-ms", default="0,50,200,1000",
  517                      help="KILL13 arm A: the gaps between the page close and system_reset, in ms (default: %(default)s)")
  518      ap.add_argument("--vocabulary", dest="vocabulary", action="store_true", default=True,
  519                      help="assert the three outcome words (COMPLETED, COULDN'T FINISH, SKIPPED) on every run's last line; on by "
  520                           "default since 2026-09-10 (the FORBIDDEN check -- no exit codes, log paths or tool names on the screen -- is always on)")
  521      ap.add_argument("--no-vocabulary", dest="vocabulary", action="store_false",
  522                      help="skip the outcome-word assertion, for an image that predates the strings")
  523      ap.add_argument("--backend", default=os.environ.get("CLOUD_QA_BACKEND", "webdav"),
  524                      help="which QA endpoint to drive: webdav (default), s3, sftp, smb or ftp (#133). "
  525                           "Bring it up first with the same name: tools/cloud-test-backend --backend <name> up")
  526      args = ap.parse_args()
  527      # Everything this harness knows about the endpoint it asks
  528      # cloud-test-backend, and that tool reads CLOUD_QA_BACKEND. Setting it
  529      # here rather than threading a parameter through two hundred call sites
  530      # means one switch cannot be half-applied: there is no path by which the
  531      # stanza written onto the device and the directory read back afterwards
  532      # could come from different backends.
  533      os.environ["CLOUD_QA_BACKEND"] = args.backend
  534      # Line-buffered even when redirected: a run in the background used to
  535      # show nothing until it ended, and a run that hangs showed nothing ever.
  536      try:
  537          sys.stdout.reconfigure(line_buffering=True)
  538      except (AttributeError, ValueError):
  539          pass
  540      if args.list:
  541          list_fixtures()
  542          return 0
  543      if not args.host:
  544          ap.error("--host is required")
  545      if args.real_roms and args.second_port:
  546          raise Fail("the two-device fixtures rewrite both saves trees; they never run against real ROMs (D-QA-009)")
  547  
  548      cap_keys = {k for k, _, _ in CAPTURE_FIXTURES}
  549      solo_keys = {k for k, _, _ in SOLO_FIXTURES}
  550      link_keys = {k for k, _, _ in LINK_FIXTURES}
  551      kill_keys = {k for k, _, _, _ in KILL_FIXTURES}
  552      kill_local_keys = {k for k, _, _, needs in KILL_FIXTURES if "backend" not in needs}
  553      only = {k.strip().upper() for k in args.only.split(",")} if args.only else None
  554      skipped = []
  555      # A run naming only capture fixtures needs no MinIO and no second guest:
  556      # the producer is network-free, so the backend is asked for nothing. The
  557      # same for the KILL cells that touch no endpoint (backuptool, set_setting,
  558      # the local records, and the power-cut cells, which need the console and
  559      # the monitor but no cloud).
  560      cap_only = only is not None and only <= cap_keys
  561      kill_local = only is not None and bool(only) and only <= kill_local_keys
  562      local_only = cap_only or kill_local
  563      remote = "" if local_only else backend("remote-name").strip()
  564      root = "/storage/roms" if args.real_roms else SCRATCH
  565      devices = [Device(args.host, args.port, args.identity, args.path_prefix)]
  566      if args.second_port:
  567          devices.append(Device(args.second_host or args.host, args.second_port, args.identity, args.path_prefix))
  568  
  569      failures = 0
  570      prepared = []
  571      archive = f"{root}/backup/{ARCHIVE_NAME}"
  572      # From the first capture on, every device carries the harness's settings;
  573      # whatever happens below -- a failing check, an exception, a Ctrl-C --
  574      # the block after the try puts each one back (Gate 0, #35: a device the
  575      # harness has finished with has the remote it started with). Found the
  576      # hard way: a run that aborted on guest b left the QA remote and the QA
  577      # paths behind.
  578      try:
  579          if local_only:
  580              first = prepare_local(devices[0], root, args, prepared,
  581                                    keys=("SAVESPATH", "SETTINGS_BACKUPS") if kill_local else ("SAVESPATH",), capture=cap_only)
  582          else:
  583              if len(devices) > 1:
  584                  assert_two_devices(devices[0], devices[1])
  585              first = prepare_device(devices[0], remote, root, args, prepared, which="a " if len(devices) > 1 else "")
  586              if len(devices) > 1:
  587                  prepare_device(devices[1], remote, root, args, prepared, which="b ")
  588          if not args.only:
  589              failures += run_steps(first.dev, root, remote, args, first.settings, first.prev_paths)
  590          if len(prepared) > 1:
  591              failures += run_pair(prepared[0].dev, prepared[1].dev, root, remote, args, first.settings)
  592          elif only and only - cap_keys - solo_keys - link_keys - kill_keys:
  593              print("\n--only names two-device fixtures; pass --second-port for the VM pair's guest b")
  594          if only and only & solo_keys:
  595              failures += run_solo(first.dev, root, remote, args, first.settings, only)
  596          if only and only & cap_keys:
  597              failures += run_capture(first.dev, root, args, only)
  598          if args.link or (only and only & link_keys):
  599              # Off by default in the suite: minutes per cell, and a channel a
  600              # handheld does not have. Skipped -- said, not silently -- when
  601              # the console is not there.
  602              serial = Serial(args.serial_socket, args.vm_serial)
  603              if serial.usable():
  604                  failures += run_link(first.dev, root, remote, args, first.settings, serial, only)
  605              else:
  606                  skipped.append(f"LINK fixtures: no serial console at {args.serial_socket} (or {args.vm_serial} is not executable); "
  607                                 "a guest from `generic-x64-vm run --headless` has one, a handheld has none")
  608                  print(f"\n    SKIP  {skipped[-1]}")
  609          if args.kill or (only and only & kill_keys):
  610              # Off by default: minutes per cell, and two of them reboot the
  611              # guest. Cells whose channel is missing are skipped one by one,
  612              # with a line each, inside run_kill.
  613              serial = Serial(args.serial_socket, args.vm_serial)
  614              failures += run_kill(first.dev, root, remote, args, first.settings, serial, only, local_only)
  615      finally:
  616          for p in prepared:
  617              restore_device(p, args, archive)
  618      note = f" ({'; '.join(skipped)})" if skipped else ""
  619      print(f"\n{'PASSED' if failures == 0 else f'{failures} CHECK(S) FAILED'}{note}")
  620      return 1 if failures else 0
  621  
  622  
  623  def run_steps(dev, root, remote, args, settings, prev_paths):
  624      failures = 0
  625      step("plant fixtures")
  626      for rel, data in {**FIXTURES, **EXCLUDED}.items():
  627          dev.write(f"{root}/{rel}", data)
  628      before = {rel: dev.sha(f"{root}/{rel}") for rel in FIXTURES}
  629      failures += not check(all(before.values()), "fixtures written",
  630                            "could not write fixtures")
  631  
  632      step("saves back up to the cloud")
  633      backend("reset")
  634      # Nothing is in the cloud yet. Two shapes are acceptable and one never
  635      # is. A truthful empty: the parent of the saves folder answers, so the
  636      # run ends 0 with "There's nothing in your cloud to restore yet." and
  637      # the offer line EmulationStation turns into CREATE IT (#100,
  638      # D-CLOUD-085; since #127, D-CLOUD-092, a folder at the root -- the
  639      # suite's /GAMES -- has the root for its parent and takes this shape
  640      # too). Or a failure with its own code, when the parent itself is
  641      # missing. Never a sentinel: cloud_restore used to leave with rclone's
  642      # "directory not found", 3, which until 2026-09-09 was also the lock
  643      # sentinel, and the page said SKIPPED - ANOTHER CLOUD SYNC IS RUNNING
  644      # over a run that had moved five files (VM; #99). The sentinels are 75
  645      # and 69 now, codes rclone cannot return. And never a bare 0: a run
  646      # that restored nothing and said COMPLETED with no offer is the shape
  647      # that shipped broken in four images (blindspot 13).
  648      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
  649      truthful_empty = rc == 0 and ">>> offer create-saves-folder" in out and "nothing to restore" in out.lower()
  650      failures += not check(truthful_empty or rc not in (0, 75, 69),
  651                            "a restore with no Saves folder in the cloud is a truthful empty (0 + the offer) or fails with its own code, never a sentinel",
  652                            f"cloud_restore exited {rc!r} against an empty endpoint with no offer (0 = silent success, 75/69 = read as a sentinel): {out.strip()[-160:]!r}")
  653      # As BACK UP SAVES TO THE CLOUD runs it: --saves-only, or the settings
  654      # phase rides along under a saves label (2026-09-06).
  655      dev.run("cloud_backup --yes --saves-only >/dev/null 2>&1 || true", check=False)
  656      listing = backend("ls")
  657      uploaded = {rel for rel in FIXTURES if os.path.basename(rel) in listing}
  658      failures += not check(len(uploaded) == len(FIXTURES),
  659                            f"all {len(FIXTURES)} fixtures reached the bucket",
  660                            f"only {len(uploaded)}/{len(FIXTURES)} reached the bucket")
  661      # Only meaningful once something uploaded: if the backup did nothing at
  662      # all, "the excluded file is absent" is true for the wrong reason and
  663      # reports a pass over a broken run.
  664      leaked = [rel for rel in EXCLUDED if os.path.basename(rel) in listing]
  665      if uploaded:
  666          failures += not check(not leaked,
  667                                "the allowlist kept excluded files out of the cloud",
  668                                f"excluded file(s) uploaded: {leaked}")
  669      else:
  670          print("    SKIP  allowlist check - nothing uploaded, so it proves nothing")
  671  
  672      step("a second backup replaces several saves at once")
  673      # Every saves assertion above this line is about a FIRST upload, and a
  674      # first upload has nothing to move out of the way. The exit sync after a
  675      # game is the other case -- saves already in the cloud, replaced -- and it
  676      # was broken on Dropbox for as long as #103's retry bound shipped, with
  677      # the harness green throughout (#107, D-CLOUD-083). --backup-dir turns
  678      # each replacement into a server-side move as well as an upload, so this
  679      # exercises twice the writes per file and several files at once.
  680      #
  681      # This backend has no per-folder write lock, so it cannot reproduce
  682      # Dropbox's contention; what it can prove is that the replace path works
  683      # at all and that the cloud ends up holding the new bytes. Both were
  684      # untested until now.
  685      for rel in FIXTURES:
  686          dev.run(f"printf 'v2-%s' {shlex.quote(rel)} >> {shlex.quote(f'{root}/{rel}')}")
  687      want = {rel: dev.sha(f"{root}/{rel}") for rel in FIXTURES}
  688      rc, out = run_rc(dev, "cloud_backup --yes --saves-only")
  689      failures += not check(rc == 0, f"the second backup completed (exit {rc})",
  690                            f"the second backup exited {rc}: {out.strip()[-200:]!r}")
  691      # Read the cloud copies back, not the run's own report (#53's lesson).
  692      stale = []
  693      for rel in FIXTURES:
  694          dev.run(f"rm -f {shlex.quote(f'{root}/{rel}')}")
  695      run_rc(dev, "cloud_restore --yes --saves-only")
  696      for rel in FIXTURES:
  697          if dev.sha(f"{root}/{rel}") != want[rel]:
  698              stale.append(rel)
  699      failures += not check(not stale,
  700                            f"all {len(FIXTURES)} replaced saves came back from the cloud as the new bytes",
  701                            f"the cloud still holds the old bytes for: {stale}")
  702      # These files legitimately hold their v2 bytes from here on, on both
  703      # sides. The round-trip check below compares against what was here before
  704      # the first backup, so it is told what "before" means now -- otherwise it
  705      # reports 0/4 matched for a restore that worked perfectly.
  706      before = dict(want)
  707  
  708      step("saves restore from the cloud")
  709      for rel in FIXTURES:
  710          dev.run(f"rm -f {shlex.quote(f'{root}/{rel}')}")
  711      gone = [rel for rel in FIXTURES if dev.sha(f"{root}/{rel}")]
  712      failures += not check(not gone, "local copies removed before restore",
  713                            f"still present: {gone}")
  714      dev.run("cloud_restore --yes --saves-only >/dev/null 2>&1 || true", check=False)
  715      after = {rel: dev.sha(f"{root}/{rel}") for rel in FIXTURES}
  716      same = [rel for rel in FIXTURES if before[rel] and before[rel] == after[rel]]
  717      failures += not check(len(same) == len(FIXTURES),
  718                            f"all {len(FIXTURES)} files restored byte-identical",
  719                            f"only {len(same)}/{len(FIXTURES)} matched: "
  720                            f"{[r for r in FIXTURES if r not in same]}")
  721  
  722      step("the settings archive round-trips")
  723      # Off by default, so the phase would otherwise never run here. Remember the
  724      # device's own setting: leaving it on would mean a later user-initiated
  725      # restore also pulls archives down, which they never asked for.
  726      dev.run(f"grep -m1 '^BACKUPFILE_RESTORE_OPTION=' {CONF} > {CONF}.qa-prev 2>/dev/null || : > {CONF}.qa-prev")
  727      dev.run(f"grep -q '^BACKUPFILE_RESTORE_OPTION=' {CONF} "
  728              f"&& sed -i 's|^BACKUPFILE_RESTORE_OPTION=.*|BACKUPFILE_RESTORE_OPTION=\"yes\"|' {CONF} "
  729              f"|| echo 'BACKUPFILE_RESTORE_OPTION=\"yes\"' >> {CONF}")
  730      archive = f"{root}/backup/{ARCHIVE_NAME}"
  731      dev.write(archive, ARCHIVE_BODY)
  732      arch_before = dev.sha(archive)
  733      backend("reset")
  734      # As the settings tier runs it (backuptool backup && cloud_backup --yes --system-only).
  735      rc_sb, out_sb = run_rc(dev, "cloud_backup --yes --system-only")
  736      listing = backend("ls")
  737      uploaded_archive = ARCHIVE_NAME in listing
  738      failures += not check(uploaded_archive,
  739                            "the settings backup archive reached the cloud",
  740                            "the archive was not uploaded")
  741      # And the run says so: its exit and its own last line are the settings
  742      # phase's outcome, not the skipped saves phase's (audit #307 PL-028,
  743      # whose 9-beside-a-failure case is tools/last-good-scripts-test A6).
  744      # Read by the vocabulary gate's own reader (colour, protocol markers,
  745      # rclone's lines and rules off), not a filter of its own (the audit of
  746      # the fixes, claude G-A-04).
  747      last_sb = last_player_line(out_sb)
  748      failures += not check(rc_sb == 0 and last_sb == "Completed.",
  749                            "the settings backup exited 0 and ended on Completed.",
  750                            f"the settings backup exited {rc_sb}, last line {last_sb or '(none)'!r}")
  751  
  752      # It must land under this device's own folder. A single shared filename is
  753      # what let the second device to run replace the first device's archive,
  754      # with no remote history to recover it from (#49). One device cannot
  755      # demonstrate the collision, but it can prove the archive is namespaced --
  756      # which is the property that prevents it.
  757      if uploaded_archive:
  758          device_id = dev.run("cloud_device_id 2>/dev/null || true").strip()
  759          failures += not check(
  760              bool(device_id) and f"{device_id}/{ARCHIVE_NAME}" in listing,
  761              f"the archive is filed under this device ({device_id or 'no id'})",
  762              "the archive sits at the root of the backup path - a second "
  763              "device would overwrite it")
  764      dev.run(f"rm -f {shlex.quote(archive)}")
  765      mark = log_mark(dev)
  766      rc_sr, _ = run_rc(dev, "cloud_restore --yes --system-only")
  767      if uploaded_archive:
  768          failures += not check(rc_sr == 0, "the settings restore exited 0",
  769                                f"the settings restore exited {rc_sr}")
  770          arch_after = dev.sha(archive)
  771          failures += not check(arch_after is not None and arch_after == arch_before,
  772                                "the archive came back byte-identical",
  773                                "the archive did not come back - restore can report "
  774                                "SUCCESS while its filter matches nothing")
  775          # The archive carries no device name, so the restorer had none of this
  776          # device's to prefer and must say it took the newest overall instead.
  777          tail = dev.run(f"tail -n +{mark + 1} {LOG} 2>/dev/null || true", check=False)
  778          failures += not check("restoring the newest there" in tail,
  779                                "and the restorer said it fell back to the newest archive overall",
  780                                "a pre-label archive was restored without the fallback being logged")
  781      else:
  782          print("    SKIP  archive restore - nothing was uploaded, so it proves nothing")
  783  
  784      # A second backup, against a remote that already holds one. The first
  785      # transfer always happens, so it cannot detect a comparison that wrongly
  786      # decides the file is already there - which is what #53 was.
  787      if uploaded_archive:
  788          step("a changed archive of the same size still reaches the cloud")
  789          dev.write(archive, ARCHIVE_BODY_V2)
  790          v2_local = dev.sha(archive)
  791          dev.run("cloud_backup --yes --system-only >/dev/null 2>&1 || true", check=False)
  792          dev.run(f"rm -f {shlex.quote(archive)}")
  793          dev.run("cloud_restore --yes --system-only >/dev/null 2>&1 || true", check=False)
  794          v2_back = dev.sha(archive)
  795          failures += not check(v2_back is not None and v2_back == v2_local,
  796                                "the second archive replaced the first in the cloud",
  797                                "the changed archive never reached the cloud - a "
  798                                "size-only comparison can skip the upload and "
  799                                "still report SUCCESS")
  800  
  801      # --- per-device names: retention and preference -------------------------
  802      # Since 2026-09-08 an archive's name carries the device that wrote it,
  803      # between the date and ROCKNIX (<stamp>-<label>-ROCKNIX_SETTINGS.tar.gz),
  804      # and two rules hang off that. Retention counts and removes only archives
  805      # carrying this device's label, in this device's own folder: one carrying
  806      # another device's label (restored here and sent up again, or written by a
  807      # device sharing the folder through a cloned id, #86) or none (from before
  808      # names carried a device) is left alone. And a restore brings back this
  809      # device's newest before anything newer another device wrote. One device
  810      # proves both by planting the other shapes in its own folder: the VM
  811      # pair's guest b gets its own folder by construction, so the pair cannot
  812      # share one without a cloned id, which A11 refuses. A same-label archive
  813      # from another device of the same model is not planted: by design it
  814      # cannot be told from this device's own, and counts as one of them.
  815      step("retention removes only archives carrying this device's name, and restore prefers them")
  816      label = dev.run("cloud_device_id --label 2>/dev/null || true").strip()
  817      osn = os_name(dev)
  818      device_id = dev.run("cloud_device_id 2>/dev/null || true").strip()
  819      settings_remote = settings.get("SETTINGS_REMOTE") or settings.get("SYNCPATH_BACKUP") or ""
  820      keep_raw = dev.run(f"grep -m1 '^CLOUD_BACKUP_KEEP=' {CONF} 2>/dev/null | cut -d= -f2 | tr -d '\"' || true").strip()
  821      keep = int(keep_raw) if keep_raw.isdigit() else 3
  822      folder = f"{remote}:{settings_remote}/{device_id}"
  823      if not (label and device_id and settings_remote) or not 1 <= keep <= 20:
  824          failures += not check(False, "",
  825                                f"cannot set the fixture up (label {label!r}, id {device_id!r}, "
  826                                f"settings remote {settings_remote!r}, keep {keep})")
  827      else:
  828          other = f"2026_01_01-000000-Other-Handheld-{osn}_SETTINGS.tar.gz"
  829          # Both pre-label shapes a folder in the field holds: the dated tar,
  830          # and the zip the uploader dated on its way up.
  831          unlabelled = [f"2026_01_01-000000-{osn}_SETTINGS.tar.gz", f"2026_01_01-000000-{osn}_BACKUP.zip"]
  832          # keep of this device's planted, one more uploaded: exactly one goes.
  833          own = [f"2026_01_{d:02d}-000000-{label}-{osn}_SETTINGS.tar.gz" for d in range(2, 2 + keep)]
  834          newest_own = f"2026_01_{2 + keep:02d}-000000-{label}-{osn}_SETTINGS.tar.gz"
  835          newer_other = f"2099_01_01-000000-Other-Handheld-{osn}_SETTINGS.tar.gz"
  836          plant = "/tmp/qa-plant"
  837          broot = f"{root}/backup"
  838          dev.run(f"rclone purge {shlex.quote(folder)} >/dev/null 2>&1; rm -rf {plant}; mkdir -p {plant} {shlex.quote(broot)}",
  839                  check=False)
  840          # A fixture that cannot be planted is a FAIL here, not an abort of
  841          # every step after this one.
  842          try:
  843              for name in [other] + unlabelled + own:
  844                  dev.write(f"{plant}/{name}", name.encode())
  845                  dev.run(f"rclone copyto {shlex.quote(f'{plant}/{name}')} {shlex.quote(f'{folder}/{name}')}")
  846              planted = True
  847          except Fail as e:
  848              planted = False
  849              failures += not check(False, "", f"could not plant the fixture in {folder}: {e}")
  850          ran = False
  851          if planted:
  852              # One archive of this device's at the root so the upload runs and
  853              # retention runs after it; the marker is cleared so a root that
  854              # looks unchanged is not skipped.
  855              dev.run(f"rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip {CACHE}/settings-backup.uploaded", check=False)
  856              # A real archive: cloud_backup lists it before sending and refuses
  857              # one that does not list (2026-09-10), so a run of bytes never
  858              # uploads and retention never runs.
  859              dev.write(f"{broot}/{newest_own}", ARCHIVE_BODY)
  860              rc, _ = run_rc(dev, "cloud_backup --yes --system-only")
  861              listing = dev.run(f"rclone lsf --files-only {shlex.quote(folder + '/')} 2>/dev/null || true", check=False).split()
  862              mine = sorted(n for n in listing if n.endswith(f"-{label}-{osn}_SETTINGS.tar.gz"))
  863              ran = check(rc == 0 and newest_own in listing,
  864                          f"the upload ran (exit {rc})",
  865                          f"the upload did not run (exit {rc}); retention cannot be judged")
  866              failures += not ran
  867          if ran:
  868              failures += not check(mine == sorted(own[1:] + [newest_own]),
  869                                    f"this device's archives were trimmed to CLOUD_BACKUP_KEEP={keep}, oldest first",
  870                                    f"retention did not keep the newest {keep} of this device's: {mine}")
  871              spared = [other] + unlabelled
  872              failures += not check(all(n in listing for n in spared),
  873                                    "another device's archive and both pre-label shapes were left alone",
  874                                    "RETENTION REMOVED WHAT IS NOT THIS DEVICE'S: "
  875                                    f"{[n for n in spared if n not in listing]}")
  876  
  877              # Restore: the other device's is newer, and this device's must still win.
  878              dev.write(f"{plant}/{newer_other}", newer_other.encode())
  879              dev.run(f"rclone copyto {shlex.quote(f'{plant}/{newer_other}')} {shlex.quote(f'{folder}/{newer_other}')}")
  880              dev.run(f"rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip", check=False)
  881              run_rc(dev, "cloud_restore --yes --system-only")
  882              local = dev.run(f"ls -1 {shlex.quote(broot)}/ 2>/dev/null || true", check=False).split()
  883              failures += not check(newest_own in local and newer_other not in local,
  884                                    "restore brought back this device's newest, not the other device's newer archive",
  885                                    f"restore chose {local or 'nothing'} over this device's own {newest_own}")
  886              # With none of this device's own left, the newest overall -- the
  887              # fresh-device journey (#26) -- and the log says whose it was.
  888              for name in mine:
  889                  dev.run(f"rclone deletefile {shlex.quote(f'{folder}/{name}')} >/dev/null 2>&1 || true", check=False)
  890              dev.run(f"rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip", check=False)
  891              mark = log_mark(dev)
  892              run_rc(dev, "cloud_restore --yes --system-only")
  893              local = dev.run(f"ls -1 {shlex.quote(broot)}/ 2>/dev/null || true", check=False).split()
  894              tail = dev.run(f"tail -n +{mark + 1} {LOG} 2>/dev/null || true", check=False)
  895              failures += not check(newer_other in local,
  896                                    "with none of its own, restore took the newest overall",
  897                                    f"restore took {local or 'nothing'} when only other devices' archives remained")
  898              failures += not check("made on Other-Handheld" in tail,
  899                                    "and the log named the device that made it",
  900                                    "the fallback restore did not say whose archive it took")
  901          dev.run(f"rm -rf {plant}; rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip {CACHE}/settings-backup.uploaded",
  902                  check=False)
  903          dev.run(f"rclone purge {shlex.quote(folder)} >/dev/null 2>&1 || true", check=False)
  904  
  905      # --- content backup / restore -------------------------------------------
  906      # cloud_content_backup hardcodes DEST=/storage/roms and ignores SAVESPATH,
  907      # so the scratch tree cannot contain this one. It is confined instead to a
  908      # directory the harness creates and removes, and driven per-directory:
  909      # `--all` would upload the whole ROM library, which is never what a test
  910      # should do to someone's device.
  911      step("ROMs and BIOS back up a system directory")
  912      croot = f"/storage/roms/{CONTENT_DIR}"
  913      # Never delete somebody's library: the fixture directory is a real
  914      # system's, and the harness owns it only if it is empty or absent.
  915      existing = dev.run(f"find {shlex.quote(croot)} -type f 2>/dev/null | head -3 || true").strip()
  916      if existing and not args.real_roms:
  917          raise Fail(f"{croot} holds files ({existing.splitlines()[0]} ...); refusing to use it as a fixture")
  918      dev.run(f"rm -rf {shlex.quote(croot)}")
  919      for rel, data in CONTENT_FIXTURES.items():
  920          dev.write(f"{croot}/{rel}", data)
  921      cbefore = {rel: dev.sha(f"{croot}/{rel}") for rel in CONTENT_FIXTURES}
  922  
  923      listed = dev.run(f"cloud_content_backup --list 2>/dev/null || true")
  924      failures += not check(CONTENT_DIR in listed,
  925                            f"{CONTENT_DIR} is offered as a content directory",
  926                            f"--list did not offer it: {listed.split() or 'nothing'}")
  927  
  928      dev.run(f"cloud_content_backup {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true",
  929              check=False)
  930      clisting = backend("ls")
  931      cup = {rel for rel in CONTENT_FIXTURES if os.path.basename(rel) in clisting}
  932      ok = check(len(cup) == len(CONTENT_FIXTURES),
  933                 f"all {len(CONTENT_FIXTURES)} content files reached the cloud",
  934                 f"only {len(cup)}/{len(CONTENT_FIXTURES)} reached the cloud")
  935      failures += not ok
  936      if not ok:
  937          # Distinguish "this device has the known bug" from "the harness is
  938          # broken" - otherwise a real, already-diagnosed defect reads as a
  939          # problem with the test.
  940          body = dev.run("cat $(command -v cloud_content_backup) 2>/dev/null || true")
  941          if "Restoring ${DIR:-everything} from the cloud" in body:
  942              print("          ^ this device ships the inverted cloud_content_backup "
  943                    "(issue #40): it copies cloud -> device, so nothing is ever "
  944                    "uploaded. Expected until a build carries the fix.")
  945  
  946      step("a user's own rule sits above the catch-all and keeps its file off the cloud")
  947      # #39: rclone filters are first-match-wins, and user rules used to be
  948      # appended below "- /**", where nothing reaches them. The merge puts them
  949      # first now; this proves it the only way that matters -- a file the user
  950      # excluded does not travel -- and reads the file's order as well.
  951      probe_rel = "saves/keep-off-the-cloud.probe"
  952      dev.run(f"printf 'never leaves' > {shlex.quote(f'{root}/{probe_rel}')}")
  953      dev.run(f"grep -qxF -- '- /**/*.probe' {RULES} || sed -i '1i - /**/*.probe' {RULES}")
  954      rc, out = run_rc(dev, "cloud_backup --yes --saves-only")
  955      failures += not check(rc == 0, f"the backup with a user rule completed (exit {rc})", f"exit {rc}: {out.strip()[-160:]!r}")
  956      order = dev.run(f"grep -nxF -e '- /**/*.probe' -e '- /**' {RULES} | cut -d: -f1 | tr '\\n' ' '").split()
  957      failures += not check(len(order) == 2 and int(order[0]) < int(order[1]),
  958                            f"the user rule sits above the catch-all in the merged file (lines {' < '.join(order) if order else '?'})",
  959                            f"rules order was {order}")
  960      saves_remote = dev.run(f"grep -m1 '^SAVES_REMOTE=' {CONF} | cut -d'\"' -f2").strip()
  961      remote_name = active_remote(dev)
  962      listing = dev.run(f"rclone lsf -R --files-only {shlex.quote(remote_name + saves_remote)} 2>/dev/null || true")
  963      failures += not check("keep-off-the-cloud.probe" not in listing and "game1.srm" in listing,
  964                            "the excluded file stayed home while the ordinary save travelled",
  965                            f"cloud listing: {listing.strip()[:200]!r}")
  966      dev.run(f"sed -i '/^- \\/\\*\\*\\/\\*\\.probe$/d' {RULES}; rm -f {shlex.quote(f'{root}/{probe_rel}')}")
  967  
  968      step("an edited RCLONEOPTS without --filter-from still keeps the allowlist")
  969      # #71: the allowlist rode along only inside the shipped default value of
  970      # RCLONEOPTS, so a player who edited that line (a --bwlimit, dropping
  971      # --progress) and did not keep --filter-from sent the whole ROM library
  972      # into the saves folder. The scripts add the rules file whenever the
  973      # options do not name one; a file outside the allowlist must stay home.
  974      dev.run(f"cp {CONF} {CONF}.qa-71")
  975      dev.run(f"sed -i '/^RCLONEOPTS=/,/[^\\\\]$/d' {CONF}; echo 'RCLONEOPTS=\"--progress\"' >> {CONF}")
  976      rom_rel = "saves/not-a-save.rom"
  977      dev.run(f"printf 'a rom, not a save' > {shlex.quote(f'{root}/{rom_rel}')}")
  978      rc, out = run_rc(dev, "cloud_backup --yes --saves-only")
  979      failures += not check(rc == 0, f"the backup with a bare RCLONEOPTS completed (exit {rc})", f"exit {rc}: {out.strip()[-160:]!r}")
  980      listing = dev.run(f"rclone lsf -R --files-only {shlex.quote(remote_name + saves_remote)} 2>/dev/null || true")
  981      failures += not check("not-a-save.rom" not in listing and "game1.srm" in listing,
  982                            "the file outside the allowlist stayed home while the save travelled",
  983                            f"cloud listing: {listing.strip()[:200]!r}")
  984      warned = dev.run("grep -c 'carried no --filter-from' /var/log/cloud_sync.log 2>/dev/null || echo 0").strip()
  985      failures += not check(warned.isdigit() and int(warned) > 0, "the log says the allowlist was added", "no such log line")
  986      # The restore half: a non-save planted IN the cloud must not come down
  987      # either, with the same bare options.
  988      dev.run(f"printf 'cloud-side rom' > /tmp/qa-cloud-side.rom; rclone copyto /tmp/qa-cloud-side.rom "
  989              f"{shlex.quote(remote_name + saves_remote + '/saves/qa-cloud-side.rom')} >/dev/null 2>&1; rm -f /tmp/qa-cloud-side.rom")
  990      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
  991      came_down = dev.run(f"test -e {shlex.quote(f'{root}/saves/qa-cloud-side.rom')} && echo yes || echo no").strip()
  992      failures += not check(rc == 0 and came_down == "no",
  993                            f"a restore with a bare RCLONEOPTS left the cloud-side non-save in the cloud (exit {rc})",
  994                            f"exit {rc}, came down: {came_down}")
  995      dev.run(f"rclone deletefile {shlex.quote(remote_name + saves_remote + '/saves/qa-cloud-side.rom')} >/dev/null 2>&1 || true", check=False)
  996      # A user who names their own filter file keeps control: nothing is added,
  997      # and their rule -- excluding one save by name -- is what governs.
  998      dev.run(f"printf -- '- /**/own-rule-victim.srm\n+ /**\n' > /tmp/qa-own-rules.txt; "
  999              f"sed -i '/^RCLONEOPTS=/d' {CONF}; echo 'RCLONEOPTS=\"--progress --filter-from /tmp/qa-own-rules.txt\"' >> {CONF}; "
 1000              f"printf 'victim' > {shlex.quote(f'{root}/saves/own-rule-victim.srm')}")
 1001      before_warn = dev.run("grep -c 'carried no --filter-from' /var/log/cloud_sync.log 2>/dev/null || echo 0").strip()
 1002      rc, out = run_rc(dev, "cloud_backup --yes --saves-only")
 1003      listing = dev.run(f"rclone lsf -R --files-only {shlex.quote(remote_name + saves_remote)} 2>/dev/null || true")
 1004      after_warn = dev.run("grep -c 'carried no --filter-from' /var/log/cloud_sync.log 2>/dev/null || echo 0").strip()
 1005      failures += not check(rc == 0 and "own-rule-victim.srm" not in listing and after_warn == before_warn,
 1006                            "a user's own --filter-from is honoured and nothing is added over it",
 1007                            f"exit {rc}; victim in cloud: {'own-rule-victim.srm' in listing}; added-lines {before_warn}->{after_warn}")
 1008      dev.run(f"mv -f {CONF}.qa-71 {CONF}; rm -f {shlex.quote(f'{root}/{rom_rel}')} {shlex.quote(f'{root}/saves/own-rule-victim.srm')} /tmp/qa-own-rules.txt")
 1009      step("the transfer lock is free the moment a run returns, and no child of a run can hold it")
 1010      # #124. `exec 9>lock` carries no close-on-exec, so the lock descriptor
 1011      # used to reach rclone and everything else a run started. While the
 1012      # script outlived its children that was invisible -- bash waits for each
 1013      # of them -- and the moment it did not, killed or orphaned while rclone
 1014      # was still copying, the lock outlived the run: every sync afterwards
 1015      # refused with "another cloud sync is running" when nothing was running.
 1016      #
 1017      # This step used to WAIT up to ten seconds for the lock to fall free,
 1018      # which is how the symptom stayed hidden: a wait turns a defect into a
 1019      # delay and reports nothing.
 1020      #
 1021      # Two assertions, because the first one cannot catch the defect on its
 1022      # own. A run that completes normally releases the lock even with the
 1023      # descriptor leaking, so the shipped scripts passed "free after a run"
 1024      # 100 times out of 100 (measured on the VM, 2026-09-11). The one that
 1025      # fails on the unfixed code is the second: it asks whether a command
 1026      # started under the lock can see the descriptor at all.
 1027      probe = "/tmp/qa-lock-fd-probe.sh"
 1028      dev.write(probe, b"""#!/bin/bash
 1029  # Does an external command started under the transfer lock still see the
 1030  # lock's descriptor? A bash function named rclone wins over PATH in every
 1031  # bash the run starts (these scripts source /etc/profile, which discards a
 1032  # --path-prefix), and the `sh -c` inside it is a real exec'd child -- which
 1033  # is what rclone is. Prints <saw-it>/<invocations>.
 1034  OUT=/tmp/qa-lock-fd-probe.out
 1035  : > "$OUT"
 1036  rclone() { sh -c 'ls -l /proc/$$/fd 2>/dev/null | grep -c cloud_sync.lock' >> "$OUT"; command rclone "$@"; }
 1037  export -f rclone
 1038  export OUT
 1039  "$@" >/dev/null 2>&1
 1040  saw=$(grep -c '^[1-9]' "$OUT" 2>/dev/null); all=$(wc -l < "$OUT" 2>/dev/null)
 1041  rm -f "$OUT"
 1042  echo "${saw:-0}/${all:-0}"
 1043  """)
 1044      for tool in ("cloud_backup", "cloud_restore"):
 1045          seen = dev.run(f"bash {probe} {tool} --yes --saves-only", check=False).strip()
 1046          saw, _, total = seen.partition("/")
 1047          # An "of 0" result is not a pass: it would mean the run started no
 1048          # rclone at all, and the assertion would be holding because nothing
 1049          # happened.
 1050          failures += not check(saw == "0" and total.isdigit() and int(total) > 0,
 1051                                f"no command {tool} starts under the lock sees its descriptor (0 of {total or '?'})",
 1052                                f"{tool}: {saw} of {total or '?'} rclone invocations inherited the lock descriptor")
 1053      dev.run(f"rm -f {probe}", check=False)
 1054      # And the symptom #124 names, in the shape its acceptance criterion asks
 1055      # for: a run, then the lock, in one shell with nothing in between. The
 1056      # 0.2 s bound only says how long a failure took; the pass is the first,
 1057      # immediate attempt.
 1058      out = dev.run(
 1059          "cloud_backup --yes --saves-only >/dev/null 2>&1; rc=$?; "
 1060          "if flock -n /var/run/cloud_sync.lock true 2>/dev/null; then echo \"FREE rc=$rc\"; exit 0; fi; "
 1061          "h=''; for p in /proc/[0-9]*; do ls -l $p/fd 2>/dev/null | grep -q cloud_sync.lock && "
 1062          "h=\"$h $(basename $p)=$(tr '\\0' ' ' < $p/cmdline | cut -c1-50)\"; done; "
 1063          "late=no; for i in 1 2 3 4; do sleep 0.05; "
 1064          "flock -n /var/run/cloud_sync.lock true 2>/dev/null && { late=yes; break; }; done; "
 1065          "echo \"HELD rc=$rc free-within-0.2s=$late by$h\"", check=False).strip()
 1066      failures += not check(out.startswith("FREE"),
 1067                            f"the lock is free the moment the run returns ({out})",
 1068                            f"the lock outlived the run: {out[:240]}")
 1069  
 1070      step("a settings-only backup with nothing on the device to send is skipped, and says so once")
 1071      # #126: with no archive under SETTINGS_BACKUPS the run printed "There's no
 1072      # settings backup on this device yet." and then "Settings backup:
 1073      # COMPLETED" -- two lines that contradict each other, and a last-run
 1074      # stamp for a run that sent nothing. Now the phase line and the summary
 1075      # word agree (SKIPPED - NOTHING TO SEND YET), the exit is still 0, and
 1076      # the stamp keeps describing the last upload that happened. Under
 1077      # --system-only the saves line says it was skipped too, rather than
 1078      # COMPLETED for a phase that never ran.
 1079      bk_dir = dev.run(f"grep -m1 '^SETTINGS_BACKUPS=' {CONF} | cut -d'\"' -f2").strip() or "/storage/roms/backup"
 1080      stash = "/storage/.cache/qa/126-stash"
 1081      dev.run(f"mkdir -p {shlex.quote(stash)} {shlex.quote(bk_dir)}; mv {shlex.quote(bk_dir)}/* {shlex.quote(stash)}/ 2>/dev/null; true", check=False)
 1082      stamp_before = dev.run("cat /storage/.cache/cloud_sync/last-settings-backup 2>/dev/null || true").strip()
 1083      rc, out = run_rc(dev, "cloud_backup --yes --system-only")
 1084      lines = [clean_line(l) for l in out.splitlines()]
 1085      settings_words = [l for l in lines if l.startswith("Settings backup:")]
 1086      saves_words = [l for l in lines if l.startswith("Game saves:")]
 1087      said_skipped = any(l.startswith("Skipped settings this time") for l in lines)
 1088      failures += not check(rc == 0 and said_skipped and settings_words == ["Settings backup: SKIPPED - NOTHING TO SEND YET"],
 1089                            "the settings phase says it was skipped and the summary agrees: SKIPPED - NOTHING TO SEND YET",
 1090                            f"exit {rc}; phase line said skipped: {said_skipped}; summary: {settings_words}; tail: {out.strip()[-200:]!r}")
 1091      failures += not check(saves_words == ["Game saves: SKIPPED - SETTINGS ONLY"],
 1092                            "and the saves line says the phase was skipped, not COMPLETED",
 1093                            f"summary saves line: {saves_words}")
 1094      stamp_after = dev.run("cat /storage/.cache/cloud_sync/last-settings-backup 2>/dev/null || true").strip()
 1095      failures += not check(stamp_after == stamp_before,
 1096                            f"the settings stamp still describes the last upload that happened ({stamp_after or 'absent'})",
 1097                            f"the stamp moved from {stamp_before!r} to {stamp_after!r} for a run that sent nothing")
 1098      dev.run(f"mv {shlex.quote(stash)}/* {shlex.quote(bk_dir)}/ 2>/dev/null; rmdir {shlex.quote(stash)} 2>/dev/null; true", check=False)
 1099  
 1100      step("folder choices are independent; discovery preserves those choices")
 1101      # #508/#510: selecting saves must preserve a separately chosen archive
 1102      # or library path. Each pointer changes only through its own action.
 1103      before_choice_conf = dev.run(f"cat {CONF}")
 1104      prev = {k: dev.run(f"grep -m1 '^{k}=' {CONF} | cut -d'\"' -f2").strip() for k in ("SAVES_REMOTE", "SETTINGS_REMOTE", "CONTENT_REMOTE")}
 1105      rc, out = run_rc(dev, f"cloud_setup --set-saves-remote {rpath('QA-Custom/Saves')}")
 1106      now = {k: dev.run(f"grep -m1 '^{k}=' {CONF} | cut -d'\"' -f2").strip() for k in ("SAVES_REMOTE", "SETTINGS_REMOTE", "CONTENT_REMOTE")}
 1107      failures += not check(rc == 0 and now == dict(prev, SAVES_REMOTE=rpath("QA-Custom/Saves")),
 1108                            "selecting saves preserves the settings and library paths", f"exit {rc}; conf reads {now}")
 1109      rc, out = run_rc(dev, f"cloud_setup --set-settings-remote {shlex.quote(rpath('QA-Custom/Backups'))}")
 1110      now = {k: dev.run(f"grep -m1 '^{k}=' {CONF} | cut -d'\"' -f2").strip() for k in prev}
 1111      failures += not check(rc == 0 and now == dict(prev, SAVES_REMOTE=rpath("QA-Custom/Saves"), SETTINGS_REMOTE=rpath("QA-Custom/Backups")),
 1112                            "selecting settings preserves saves and the library path", f"exit {rc}; conf reads {now}")
 1113      # The upload wants a local archive to send; the settings steps above may
 1114      # have pointed SETTINGS_BACKUPS back at the device default, so plant one
 1115      # where it points now and take it away afterwards.
 1116      bk_dir = dev.run(f"grep -m1 '^SETTINGS_BACKUPS=' {CONF} | cut -d'\"' -f2").strip() or "/storage/roms/backup"
 1117      bk_name = "2026_01_02-000000-QA-ROCKNIX_SETTINGS.tar.gz"
 1118      dev.run(f"mkdir -p {shlex.quote(bk_dir)}")
 1119      dev.write(f"{bk_dir}/{bk_name}", ARCHIVE_BODY)
 1120      rc, out = run_rc(dev, "cloud_backup --yes --system-only")
 1121      failures += not check(rc == 0 and "inside" not in out.lower(),
 1122                            f"a settings backup ran without the nesting warning (exit {rc})", f"exit {rc}: {out.strip()[-200:]!r}")
 1123      label = dev.run("cloud_device_id --label 2>/dev/null || true").strip()
 1124      landed = dev.run(f"rclone lsf -R --files-only {shlex.quote(remote_name + rpath('QA-Custom/Backups'))} 2>/dev/null || true")
 1125      failures += not check(".tar.gz" in landed and (not label or label in landed),
 1126                            f"the archive landed under {rpath('QA-Custom/Backups')}/{label or '<device>'}/", f"listing: {landed.strip()[:200]!r}")
 1127      conf_before = dev.run(f"sha256sum {CONF}").strip()
 1128      rc, out = run_rc(dev, "cloud_setup --folder-state")
 1129      facts = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
 1130      expected = {"SAVES": now["SAVES_REMOTE"], "BACKUPS": now["SETTINGS_REMOTE"],
 1131                  "CONTENT": now["CONTENT_REMOTE"]}
 1132      failures += not check(rc == 0 and facts.get("STATE") in ("ready", "missing")
 1133                            and all(facts.get(k) == v for k, v in expected.items())
 1134                            and dev.run(f"sha256sum {CONF}").strip() == conf_before,
 1135                            "folder discovery reports the selected paths without changing settings",
 1136                            f"exit {rc}: {out.strip()[-200:]!r}")
 1137      dev.run(f"rm -f {shlex.quote(f'{bk_dir}/{bk_name}')}; "
 1138              f"rclone purge {shlex.quote(remote_name + rpath('QA-Custom'))} >/dev/null 2>&1 || true", check=False)
 1139      dev.write(CONF, before_choice_conf.encode())
 1140  
 1141      step("a cloud with no saves folder yet is empty, not broken; a wrong root still fails")
 1142      # #100: the parent decides. Root present and only Saves missing is the
 1143      # everyday shape of a device whose saves were never backed up -- exit 0,
 1144      # a plain line, and the offer EmulationStation turns into CREATE IT.
 1145      # The root itself missing is a wrong setting and must keep failing, or
 1146      # a typo in the folder name would restore nothing and report success.
 1147      # Done on a folder of its own rather than by moving the suite's saves
 1148      # folder aside: the suite's SAVES_REMOTE may sit at the root (/GAMES),
 1149      # where by design there is no parent to tell the two shapes apart.
 1150      prev_saves = dev.run(f"grep -m1 '^SAVES_REMOTE=' {CONF} | cut -d'\"' -f2").strip()
 1151      dev.run(f"sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"{rpath('QA-Empty/Saves')}\"|' {CONF}; "
 1152              f"rclone purge {shlex.quote(remote_name + rpath('QA-Empty'))} >/dev/null 2>&1; "
 1153              # a file, not mkdir: on a bucket an empty directory does not exist
 1154              f"rclone touch {shlex.quote(remote_name + rpath('QA-Empty/Backups/.keep'))} >/dev/null 2>&1", check=False)
 1155      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
 1156      failures += not check(rc == 0 and "nothing to restore" in out.lower() and ">>> offer create-saves-folder" in out,
 1157                            "root present, Saves absent: exit 0, the plain line, and the offer",
 1158                            f"exit {rc}: {out.strip()[-200:]!r}")
 1159      dev.run(f"sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"{rpath('QA-No-Such-Root/Saves')}\"|' {CONF}")
 1160      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
 1161      # On a bucket the same holds since 2026-09-12: a folder exists when its
 1162      # parent lists it (a directory marker or objects), so a root nothing
 1163      # lists fails there too (#141). The fixtures above are files, because
 1164      # mkdir on a bucket without directory markers makes nothing.
 1165      failures += not check(rc != 0 and ">>> offer" not in out,
 1166                            f"root absent: the restore fails (exit {rc}) and offers nothing",
 1167                            f"exit {rc}: {out.strip()[-200:]!r}")
 1168      # #127: a saves folder at the cloud's root has the root for a parent,
 1169      # and the root answers, so an empty cloud gets the offer there too.
 1170      dev.run(f"sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"{rpath('QA-Root-Saves')}\"|' {CONF}; "
 1171              f"rclone purge {shlex.quote(remote_name + rpath('QA-Root-Saves'))} >/dev/null 2>&1 || true", check=False)
 1172      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
 1173      failures += not check(rc == 0 and f">>> offer create-saves-folder|{rpath('QA-Root-Saves')}" in out,
 1174                            "a root-level saves folder on an empty cloud: exit 0 and the offer names it",
 1175                            f"exit {rc}: {out.strip()[-200:]!r}")
 1176      # #127: a typo in the LAST component has a present parent. The offer
 1177      # carries the folder that sits beside it under a near name, and the
 1178      # player line names both, so CREATE IT is not the only way forward.
 1179      dev.run(f"sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"{rpath('QA-Near/Savez')}\"|' {CONF}; "
 1180              f"rclone purge {shlex.quote(remote_name + rpath('QA-Near'))} >/dev/null 2>&1; "
 1181              f"rclone touch {shlex.quote(remote_name + rpath('QA-Near/Saves/.keep'))} >/dev/null 2>&1; "
 1182              f"rclone touch {shlex.quote(remote_name + rpath('QA-Near/Backups/.keep'))} >/dev/null 2>&1", check=False)
 1183      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
 1184      failures += not check(rc == 0 and f">>> offer create-saves-folder|{rpath('QA-Near/Savez')}|{rpath('QA-Near/Saves')}" in out
 1185                            and f"{rpath('QA-Near/Saves')} but no {rpath('QA-Near/Savez')}" in out,
 1186                            "Savez beside Saves: exit 0, the offer carries the near name, the line names both",
 1187                            f"exit {rc}: {out.strip()[-240:]!r}")
 1188      # And a name that is not near anything (Backups is three edits from
 1189      # Photos) gets the plain offer, not a false match.
 1190      dev.run(f"sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"{rpath('QA-Near/Photos')}\"|' {CONF}")
 1191      rc, out = run_rc(dev, "cloud_restore --yes --saves-only")
 1192      failures += not check(rc == 0 and f">>> offer create-saves-folder|{rpath('QA-Near/Photos')}\n" in out.replace("\r", "") + "\n"
 1193                            and "but no" not in out,
 1194                            "a missing folder near nothing gets the plain offer",
 1195                            f"exit {rc}: {out.strip()[-200:]!r}")
 1196      dev.run(f"sed -i 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"{prev_saves}\"|' {CONF}; "
 1197              f"rclone purge {shlex.quote(remote_name + rpath('QA-Empty'))} >/dev/null 2>&1; "
 1198              f"rclone purge {shlex.quote(remote_name + rpath('QA-Near'))} >/dev/null 2>&1; "
 1199              f"rclone purge {shlex.quote(remote_name + rpath('QA-Root-Saves'))} >/dev/null 2>&1 || true", check=False)
 1200  
 1201      step("ROMs and BIOS restore it")
 1202      # Plant at the endpoint directly rather than restoring what the upload
 1203      # step just wrote: otherwise a broken uploader fails this check for the
 1204      # wrong reason and one bug masks the other's status (audit F-03).
 1205      backend("reset")
 1206      stage = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
 1207      for rel, data in CONTENT_FIXTURES.items():
 1208          f = os.path.join(stage, CONTENT_DIR, rel)
 1209          os.makedirs(os.path.dirname(f), exist_ok=True)
 1210          open(f, "wb").write(data)
 1211      # The selected layout: ROMs/<system> under CONTENT_REMOTE. Backup and
 1212      # restore use this same shape; there is no account-root or flat fallback.
 1213      cpath = epath(backend("content-remote"))
 1214      backend("put", os.path.join(stage, CONTENT_DIR), f"{cpath}/ROMs/{CONTENT_DIR}")
 1215      dev.run(f"rm -rf {shlex.quote(croot)}")
 1216      failures += not check(not dev.sha(f"{croot}/{list(CONTENT_FIXTURES)[0]}"),
 1217                            "local content removed before restore",
 1218                            "local content still present")
 1219      dev.run(f"cloud_content_restore {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true",
 1220              check=False)
 1221      cafter = {rel: dev.sha(f"{croot}/{rel}") for rel in CONTENT_FIXTURES}
 1222      csame = [r for r in CONTENT_FIXTURES if cbefore[r] and cbefore[r] == cafter[r]]
 1223      failures += not check(len(csame) == len(CONTENT_FIXTURES),
 1224                            f"all {len(CONTENT_FIXTURES)} content files restored byte-identical",
 1225                            f"only {len(csame)}/{len(CONTENT_FIXTURES)} matched")
 1226  
 1227      dev.run(f"rm -rf {shlex.quote(croot)}")
 1228  
 1229      # --all is the journey's first restore (main.cpp's first-device prompt).
 1230      # It restored ROMs/ as one unit and never BIOS, and said "Restored
 1231      # everything." (audit #307 PL-012). Every system the cloud holds and
 1232      # BIOS, each a unit of its own. The BIOS file is the harness's own, by
 1233      # a name nobody's BIOS folder carries, and it is removed afterwards; the
 1234      # endpoint is reset first, so the cloud holds only the fixture.
 1235      step("--all restores every system and BIOS, each a unit of its own")
 1236      backend("reset")
 1237      bios_name = f"qa-bios-{os.getpid()}.bin"
 1238      bios_body = b"qa bios, the ROMs and BIOS tier owns this"
 1239      bstage = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
 1240      open(os.path.join(bstage, bios_name), "wb").write(bios_body)
 1241      backend("put", os.path.join(stage, CONTENT_DIR), f"{cpath}/ROMs/{CONTENT_DIR}")
 1242      backend("put", bstage, f"{cpath}/BIOS")
 1243      subprocess.run(["rm", "-rf", bstage])
 1244      bdest = f"/storage/roms/bios/{bios_name}"
 1245      dev.run(f"rm -rf {shlex.quote(croot)}; rm -f {shlex.quote(bdest)}")
 1246      rc, out = run_rc(dev, "cloud_content_restore --all")
 1247      ok, items, detail = unit_protocol(out)
 1248      failures += not check(rc == 0, "--all exited 0", f"--all exited {rc}: {out.strip()[-200:]!r}")
 1249      failures += not check(dev.sha(bdest) == sha(bios_body),
 1250                            "the BIOS file came down with --all",
 1251                            f"the BIOS file is not on the device after --all ({detail}) (#307 PL-012)")
 1252      aafter = {rel: dev.sha(f"{croot}/{rel}") for rel in CONTENT_FIXTURES}
 1253      failures += not check(all(aafter[r] and aafter[r] == cbefore[r] for r in CONTENT_FIXTURES),
 1254                            f"and {CONTENT_DIR}'s {len(CONTENT_FIXTURES)} files, byte-identical",
 1255                            f"{CONTENT_DIR} after --all: {sum(1 for r in CONTENT_FIXTURES if aafter[r] == cbefore[r])}/{len(CONTENT_FIXTURES)} matched")
 1256      failures += not check(ok and "bios" in items and CONTENT_DIR in items,
 1257                            f"each announced as a unit, numbered across the run ({detail})",
 1258                            f"the units do not name the system and BIOS, or do not add up (#95): {detail}")
 1259      dev.run(f"rm -rf {shlex.quote(croot)}; rm -f {shlex.quote(bdest)}")
 1260  
 1261      # --- tier boundaries ----------------------------------------------------
 1262      # The regression test for blindspot 21. Content sync and the saves sync
 1263      # both operate over /storage/roms; a save file living next to a ROM must
 1264      # be carried by the saves tier and NOT by content. This existed as a
 1265      # defect for a day and was caught by a human reading an upload listing,
 1266      # not by this harness.
 1267      step("a save file inside a system directory does not reach the ROMs and BIOS tier")
 1268      backend("reset")
 1269      dev.write(f"{croot}/Some Game.srm", b"battery save, saves tier owns this")
 1270      dev.write(f"{croot}/Some Game.rom", b"a rom, content tier owns this")
 1271      dev.run(f"cloud_content_backup {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true",
 1272              check=False)
 1273      listing = backend("ls")
 1274      # Both directions, or the assertion cannot fail: the ROM proves the
 1275      # transfer ran at all, the .srm proves the exclusion bit.
 1276      failures += not check("Some Game.rom" in listing,
 1277                            "the ROM reached the content tier",
 1278                            "the ROM did not transfer - exclusion cannot be judged")
 1279      failures += not check("Some Game.srm" not in listing,
 1280                            "the save file was correctly withheld from content",
 1281                            "SAVE DATA REACHED THE CONTENT TIER (blindspot 21)")
 1282  
 1283      # A sync conflict is another client's dispute, and moving it makes it
 1284      # immortal: a device that downloads one uploads it again, so deleting it
 1285      # in the cloud looks like the provider putting it back. 271 directories of
 1286      # BIOS were resurrected exactly that way on 2026-09-04.
 1287      step("a sync-conflict artifact is carried by no tier, in either direction")
 1288      backend("reset")
 1289      conflict_dir = "Machines (Someone's conflicted copy 2026-09-03)"
 1290      dev.write(f"{croot}/Real.rom", b"content tier owns this")
 1291      dev.write(f"{croot}/{conflict_dir}/dup.rom", b"dropbox left this behind")
 1292      dev.write(f"{croot}/Other.sync-conflict-20260903-120000-ABCDEF.rom", b"syncthing")
 1293      dev.run(f"cloud_content_backup {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true",
 1294              check=False)
 1295      listing = backend("ls")
 1296      # Real.rom first: without it the exclusions below prove nothing, because a
 1297      # transfer that moved nothing at all also mentions no conflicted copy.
 1298      failures += not check("Real.rom" in listing,
 1299                            "the ordinary ROM reached the content tier",
 1300                            "nothing transferred - the exclusions cannot be judged")
 1301      failures += not check("conflicted copy" not in listing,
 1302                            "the conflicted copy was withheld from the cloud",
 1303                            "A CONFLICTED COPY WAS UPLOADED (D-CLOUD-022)")
 1304      failures += not check("sync-conflict" not in listing,
 1305                            "the Syncthing conflict file was withheld",
 1306                            "A .sync-conflict FILE WAS UPLOADED (D-CLOUD-022)")
 1307      # And it must not count as content this device holds, or the picker's
 1308      # badge reports a size the cloud will never agree with.
 1309      sizes = dev.run("cloud_content_backup --list-sizes 2>/dev/null || true")
 1310      failures += not check("conflicted copy" not in sizes,
 1311                            "--list-sizes ignores conflict artifacts",
 1312                            "--list-sizes counted a conflicted copy as content")
 1313  
 1314      # gamelist.xml is shared metadata with a per-device tail. It rides in its
 1315      # own --update pass so the freshest list wins rather than whoever ran last:
 1316      # a device that scans its own ROMs and uploads before ever restoring would
 1317      # otherwise push a thin list over a rich one.
 1318      step("gamelist.xml moves with game content, newest-first, in its own pass")
 1319      # The game list is game content (D-CLOUD-049): it moves only when game
 1320      # content is in scope, so this step runs --with-media, and restores
 1321      # --selected with a selection that exists.
 1322      backend("reset")
 1323      dev.write(f"{croot}/Real.rom", b"content")
 1324      dev.write(f"{croot}/gamelist.xml", b"<gameList><game><path>./Real.rom</path></game></gameList>")
 1325      dev.run(f"cloud_content_restore --set-systems {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true", check=False)
 1326      dev.run(f"cloud_content_backup --with-media {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true", check=False)
 1327      listing = backend("ls")
 1328      failures += not check("Real.rom" in listing,
 1329                            "the ROM reached the content tier",
 1330                            "nothing transferred - the gamelist assertions cannot be judged")
 1331      failures += not check("gamelist.xml" in listing,
 1332                            "the gamelist reached the cloud in its own pass",
 1333                            "gamelist.xml was not uploaded at all")
 1334  
 1335      # Now make the local copy newer and poorer, and restore: --update must
 1336      # refuse to overwrite it.
 1337      dev.write(f"{croot}/gamelist.xml", b"<gameList><!--LOCAL-NEWER--></gameList>")
 1338      # Unmistakably newer: on a fast guest the upload and this write land in
 1339      # the same second, WebDAV keeps one-second modtimes, and --update falls
 1340      # back to size when times are equal -- which is not the case under test.
 1341      # busybox touch takes "YYYY-MM-DD hh:mm:ss", not @epoch; the arithmetic runs on the device.
 1342      dev.run(f'touch -d "$(date -d @$(( $(date +%s) + 120 )) \'+%Y-%m-%d %H:%M:%S\')" {shlex.quote(croot)}/gamelist.xml')
 1343      dev.run(f"rm -f {shlex.quote(croot)}/Real.rom")
 1344      dev.run("sync", check=False)
 1345      _, out = run_rc(dev, "cloud_content_restore --with-media --selected")
 1346      ok, items, detail = unit_protocol(out)
 1347      failures += not check(ok and CONTENT_DIR in items,
 1348                            f"--selected announced every unit it moved, numbered across the run ({detail})",
 1349                            f"the unit markers do not add up to the run (#95): {detail}")
 1350      # The restore must have done something before "the local one survived"
 1351      # means anything: the ROM removed above is back.
 1352      failures += not check(bool(dev.sha(f"{croot}/Real.rom")),
 1353                            "the restore ran (the removed ROM is back)",
 1354                            "the restore transferred nothing - the gamelist assertion below would pass for the wrong reason")
 1355      local = dev.run(f"cat {shlex.quote(croot)}/gamelist.xml 2>/dev/null || true")
 1356      failures += not check("LOCAL-NEWER" in local,
 1357                            "a newer local gamelist survived the restore",
 1358                            "RESTORE CLOBBERED A NEWER LOCAL GAMELIST (--update not applied)")
 1359  
 1360      # Three callers can start a cloud sync -- boot, game exit, the menu -- and
 1361      # until 2026-09-04 nothing stopped two from running at once. The lock lives
 1362      # in the scripts, so this test is caller-agnostic: hold it, then ask.
 1363      step("a second cloud sync while one runs is refused, exits 75, and stamps nothing")
 1364      dev.run("rm -f /storage/.cache/cloud_sync/last-backup", check=False)
 1365      out = dev.run(
 1366          "exec 9>/var/run/cloud_sync.lock; flock -n 9 || echo HOLDER-FAILED; "
 1367          "cloud_backup --yes >/tmp/second.out 2>&1; echo rc=$?; "
 1368          "exec 9>&-", check=False)
 1369      failures += not check("HOLDER-FAILED" not in out,
 1370                            "the test could hold the lock itself",
 1371                            "could not take the lock to set up the test")
 1372      failures += not check("rc=75" in out,
 1373                            "the second sync exited 75 (EX_TEMPFAIL, the lock sentinel)",
 1374                            f"expected exit 75 while the lock was held, got: {out.strip()[-40:]}")
 1375      second = dev.run("cat /tmp/second.out 2>/dev/null || true")
 1376      failures += not check("already running" in second.lower(),
 1377                            "and said another sync was running",
 1378                            "exit 75 without the message somebody would read")
 1379      failures += assert_message(second, 75, args.vocabulary, label="the refusal: ")
 1380      stamp = dev.run("cat /storage/.cache/cloud_sync/last-backup 2>/dev/null || echo NONE")
 1381      failures += not check(stamp.strip() == "NONE",
 1382                            "no last-run stamp was written for work that did not happen",
 1383                            "A SKIPPED SYNC STAMPED A LAST-RUN (would read as success/failure)")
 1384  
 1385      # The game-exit sync runs cloud_backup --yes --saves-only --recent: only
 1386      # what changed since the last backup that worked, no remote probe, no
 1387      # tidy, and exit 69 at once when there is no network. Each is a claim a
 1388      # player waits on after every game, so each is asserted here -- against
 1389      # the script's own log, because "fast" is not observable from a listing.
 1390      step("a --recent sync with nothing changed leaves the remote alone")
 1391      dev.run("cloud_backup --yes --saves-only >/dev/null 2>&1 || true", check=False)  # a success to measure from
 1392      mark = dev.run("wc -l < /var/log/cloud_sync.log 2>/dev/null || echo 0").strip() or "0"
 1393      out = dev.run("cloud_backup --yes --saves-only --recent >/dev/null 2>&1; echo rc=$?", check=False)
 1394      tail = dev.run(f"tail -n +{int(mark) + 1} /var/log/cloud_sync.log 2>/dev/null || true")
 1395      failures += not check("rc=0" in out, "the recent sync exited 0",
 1396                            f"recent sync failed: {out.strip()[-40:]}")
 1397      failures += not check("--max-age" in tail and "--no-traverse" in tail,
 1398                            "rclone was given a recency window and told not to list the remote",
 1399                            "--recent did not narrow the copy (no --max-age/--no-traverse in the log)")
 1400      failures += not check("nothing to transfer" in tail.lower(),
 1401                            "and found nothing to move",
 1402                            "a recent sync with nothing changed transferred something")
 1403      failures += not check("Ensuring remote sync path" not in tail and "Removing orphaned" not in tail,
 1404                            "no probe and no tidy round trips were made",
 1405                            "a recent sync still probed or tidied the remote")
 1406  
 1407      step("a --recent sync after one save is written pushes that file")
 1408      dev.write(f"{root}/savestates/recent-probe.state", b"recent")
 1409      dev.run("sync", check=False)
 1410      mark = dev.run("wc -l < /var/log/cloud_sync.log 2>/dev/null || echo 0").strip() or "0"
 1411      out = dev.run("cloud_backup --yes --saves-only --recent >/dev/null 2>&1; echo rc=$?", check=False)
 1412      tail = dev.run(f"tail -n +{int(mark) + 1} /var/log/cloud_sync.log 2>/dev/null || true")
 1413      failures += not check("rc=0" in out and "recent-probe.state" in backend("ls"),
 1414                            "the new save reached the bucket",
 1415                            "the save written after the last sync did not reach the bucket")
 1416      failures += not check("Transferred:            1 / 1" in tail,
 1417                            "and it was the only file transferred",
 1418                            "more than one file moved for one changed save")
 1419  
 1420      step("a changed save of the same size still reaches the cloud (#315)")
 1421      # A battery save is the same size every time it is written. On a backend
 1422      # with neither hashes nor a settable modtime (WebDAV, vendor=other) rclone
 1423      # decides on size alone -- "Sizes identical" at -vv -- and the saves tier
 1424      # carries no content marker: D-CLOUD-005 guards only the settings archive
 1425      # (the archive's twin of this step is above). Found by X-size-same on
 1426      # 8196071ff5, 2026-09-28; the pair fixture A2 covers it but vm-qa does not
 1427      # run the pair. Expected to FAIL on webdav until #315 is fixed: the suite
 1428      # stays red over a known defect rather than green.
 1429      #
 1430      # Not in the same second as the upload above. The fix compares the local
 1431      # mtime with the backend's upload time (--update), and this backend keeps
 1432      # whole seconds: a same-size change written within the same second as
 1433      # its upload reads as equal in time and identical in size, and is not
 1434      # sent (measured 2026-09-29 on the host against the QA WebDAV: the same
 1435      # second not sent, 1.2 s later sent; vm-qa run 72 on 8dd6765af0 failed
 1436      # this step for exactly that reason, while X-size-same on the guest, which
 1437      # waits 2 s, passed). A player's next change is minutes after the last
 1438      # exit sync; the suite waits two seconds, as the proof does.
 1439      time.sleep(2)
 1440      dev.write(f"{root}/savestates/recent-probe.state", b"RECENT")   # six bytes again, new ones
 1441      dev.run("sync", check=False)
 1442      out = dev.run("cloud_backup --yes --saves-only --recent >/dev/null 2>&1; echo rc=$?", check=False)
 1443      # The bucket path carries the remote folder; find the copy by its tail
 1444      # in the listing rather than guessing the prefix (run 71 read None).
 1445      # The live copy, never one under a -replaced folder (the audit of the
 1446      # fix, F-SS-06 / gpt F-SS-04): the shortest matching path outside any
 1447      # "-replaced/" component is the saves folder's own.
 1448      paths = sorted((l.split(None, 1)[1] for l in backend("ls").splitlines()
 1449                      if len(l.split(None, 1)) == 2 and l.split(None, 1)[1].endswith("savestates/recent-probe.state")
 1450                      and "-replaced/" not in l.split(None, 1)[1] and "/replaced/" not in l.split(None, 1)[1]), key=len)
 1451      got = backend_bytes(paths[0]) if paths else None
 1452      if got is None:
 1453          failures += not check(False, "", f"could not read the bucket's copy back (listing paths: {paths}); nothing proven")
 1454      else:
 1455          failures += not check("rc=0" in out and got == b"RECENT",
 1456                                "the same-size change reached the bucket as the new bytes",
 1457                                f"the same-size change was not sent: the bucket holds {got!r} (exit {out.strip()[-4:]}; "
 1458                                "#315, size-only comparison on this backend)")
 1459  
 1460      step("with no network the exit sync returns 69 at once and stamps nothing")
 1461      out = dev.run(
 1462          "mkdir -p /tmp/noroute && printf '#!/bin/sh\nexit 0\n' > /tmp/noroute/ip && chmod +x /tmp/noroute/ip; "
 1463          "s0=$(cat /storage/.cache/cloud_sync/last-backup 2>/dev/null); "
 1464          "t0=$(date +%s%N); PATH=/tmp/noroute:$PATH cloud_backup --yes --saves-only --recent >/tmp/qa-noroute.out 2>&1; "
 1465          "rc=$?; t1=$(date +%s%N); s1=$(cat /storage/.cache/cloud_sync/last-backup 2>/dev/null); "
 1466          "echo rc=$rc ms=$(( (t1 - t0) / 1000000 )) stamp=$([ \"$s0\" = \"$s1\" ] && echo same || echo CHANGED); "
 1467          "rm -rf /tmp/noroute", check=False)
 1468      fields = dict(kv.split("=", 1) for kv in out.split() if "=" in kv)
 1469      failures += not check(fields.get("rc") == "69", "exit 69 (EX_UNAVAILABLE, the no-network sentinel) with no default route",
 1470                            f"expected exit 69 without a route, got: {out.strip()}")
 1471      failures += not check(fields.get("ms", "99999").isdigit() and int(fields.get("ms", "99999")) < 2000,
 1472                            "and it answered in under two seconds",
 1473                            f"took {fields.get('ms')} ms to notice there was no network")
 1474      failures += not check(fields.get("stamp") == "same",
 1475                            "no last-run stamp was written for work that did not happen",
 1476                            "A NO-NETWORK SKIP STAMPED A LAST-RUN")
 1477      failures += assert_message(dev.run("cat /tmp/qa-noroute.out 2>/dev/null || true", check=False),
 1478                                 int(fields["rc"]) if fields.get("rc", "").isdigit() else None, args.vocabulary, label="the no-network skip: ")
 1479  
 1480      step("every EmulationStation system path is carried by exactly one tier")
 1481      # The complement of the rule above: a path in NO tier is silent data loss
 1482      # on restore. Four were found this way (gmu/playlists, idtech, modules,
 1483      # scummvm/games) after a ScummVM player would have lost their entries.
 1484      orphans = dev.run(
 1485          "C=$(ls /storage/.config/emulationstation/es_systems.cfg "
 1486          "/usr/config/emulationstation/es_systems.cfg 2>/dev/null | head -1); "
 1487          "B=$(command -v backuptool); "
 1488          "grep -oP '(?<=<path>)[^<]+' \"$C\" | sort -u | while read -r p; do "
 1489          "  case \"$p\" in /storage/roms/*) continue ;; esac; "
 1490          "  grep -qF \"$p\" \"$B\" || echo \"$p\"; "
 1491          "done").split()
 1492      failures += not check(not orphans,
 1493                            "every ES path outside /storage/roms is in the settings backup",
 1494                            f"carried by no tier: {' '.join(orphans)}")
 1495  
 1496      # --- archive format -----------------------------------------------------
 1497      step("the settings archive is a tar archive named for this device, and every reader finds it")
 1498      # A real archive, written by backuptool where the conf says archives live.
 1499      dev.run("backuptool backup >/dev/null 2>&1 || true", check=False)
 1500      # backuptool's own finder, not a copy of its globs: what RESTORE SETTINGS
 1501      # FROM THIS DEVICE will apply is what this asserts. The script is resolved
 1502      # BEFORE /etc/profile is sourced, because the profile rewrites PATH and
 1503      # would drop the --path-prefix directory; the profile is sourced at all
 1504      # because the script itself does. Archive suffixes are a persisted
 1505      # compatibility contract, independent of the displayed OS_NAME (#396).
 1506      finder = finder_cmd       # module-level since the KILL cells use it too
 1507      newest_cmd = finder('"$(command -v backuptool)"')
 1508      newest = dev.run(newest_cmd, check=False).strip()
 1509      failures += not check(newest.endswith(".tar.gz"),
 1510                            f"newest archive is a tar.gz ({os.path.basename(newest) or 'none'})",
 1511                            f"newest archive is not a tar.gz: {newest or 'none found'}")
 1512      if newest:
 1513          failures += not check(dev.run(f"tar -tzf {shlex.quote(newest)} >/dev/null 2>&1 && echo ok", check=False).strip() == "ok",
 1514                                "the archive passes tar integrity",
 1515                                "the archive is not readable by tar")
 1516      # The device's name sits between the stamp and ROCKNIX (2026-09-08): two
 1517      # handhelds' archives used to be told apart by nothing.
 1518      label = dev.run("cloud_device_id --label 2>/dev/null || true").strip()
 1519      # New archives must remain readable by older ROCKNIX images (#376).
 1520      # Do not derive the expected writer suffix from the displayed OS name,
 1521      # or from the writer itself: either would miss a compatibility regression.
 1522      archive_osn = "ROCKNIX"
 1523      named = bool(label) and re.fullmatch(
 1524          rf"\d{{4}}_\d{{2}}_\d{{2}}-\d{{6}}-{re.escape(label)}-{archive_osn}_SETTINGS\.tar\.gz",
 1525          os.path.basename(newest)) is not None
 1526      failures += not check(named,
 1527                            f"the archive is named for this device, between the date and {archive_osn} ({label or 'no label'})",
 1528                            f"the archive does not carry this device's name between the date and {archive_osn}: "
 1529                            f"{os.path.basename(newest) or 'none'} (label {label or 'none'})")
 1530      # In the MIDDLE, so that the finder every image already carries --
 1531      # *-ROCKNIX_SETTINGS.tar.gz -- still matches. The installed backuptool is
 1532      # asked through its own function: on a device running an image from
 1533      # before the label, that is an older reader finding a new archive, which
 1534      # a first cut of this change broke (review, 2026-09-08). Where the
 1535      # installed script is itself the one under test, this holds trivially.
 1536      installed = dev.run(finder("/usr/bin/backuptool"), check=False).strip()
 1537      failures += not check(bool(newest) and installed == newest,
 1538                            "the installed image's own backuptool finds the same archive",
 1539                            f"the installed backuptool's finder got {os.path.basename(installed) or 'nothing'}, "
 1540                            f"not {os.path.basename(newest) or 'none'}")
 1541      # Every device in the field has archives from before names carried a
 1542      # device. A newer one of those must still be found.
 1543      legacy = f"{os.path.dirname(newest) if newest else f'{root}/backup'}/2099_12_31-235959-{os_name(dev)}_BACKUP.zip"
 1544      dev.run(f": > {shlex.quote(legacy)}")
 1545      found = dev.run(newest_cmd, check=False).strip()
 1546      dev.run(f"rm -f {shlex.quote(legacy)}")
 1547      failures += not check(found == legacy,
 1548                            "a newer archive under the pre-label name is still found",
 1549                            f"the finder skipped a pre-label archive: got {os.path.basename(found) or 'none'}")
 1550  
 1551      # --- per-device system selection ---------------------------------------
 1552      step("content transfers honour the system selection")
 1553      dev.run(f"cloud_content_restore --set-systems {shlex.quote(CONTENT_DIR)} >/dev/null 2>&1 || true",
 1554              check=False)
 1555      sel = dev.run("cloud_content_restore --systems 2>/dev/null || true").split()
 1556      failures += not check(sel == [CONTENT_DIR],
 1557                            f"selection persisted as {sel}",
 1558                            f"selection did not round-trip: {sel}")
 1559      # A selection of exactly one directory must exclude a second one that
 1560      # also has content - otherwise "only selected" is untested.
 1561      other = f"{CONTENT_DIR}-unselected"
 1562      dev.write(f"/storage/roms/{other}/game.rom", b"should not be uploaded")
 1563      backend("reset")
 1564      _, out = run_rc(dev, "cloud_content_backup --selected")
 1565      ok, items, detail = unit_protocol(out)
 1566      listing = backend("ls")
 1567      failures += not check("game.rom" not in listing,
 1568                            "an unselected system was not uploaded",
 1569                            "an UNSELECTED system was uploaded")
 1570      failures += not check(ok and CONTENT_DIR in items and other not in items,
 1571                            f"--selected announced the selected units and only those, numbered across the run ({detail})",
 1572                            f"the unit markers do not add up to the run (#95): {detail}")
 1573      # The match flow numbers its items the same way, and every chosen system
 1574      # is one -- including one with nothing to do. Until 2026-09-09 such a
 1575      # system was skipped without an announcement while n still counted it,
 1576      # so a run over three systems ended on ITEM 2 OF 3 (#95). `ghost` exists
 1577      # in neither the cloud nor the device: its plan is `none`.
 1578      ghost = "ghost-never-a-system"
 1579      dev.run(f"cloud_content_restore --set-systems {shlex.quote(CONTENT_DIR)} {ghost} >/dev/null 2>&1 || true", check=False)
 1580      # --apply is the second half of a check, as the page runs it: --match,
 1581      # the confirmation, then --match --apply, which acts on the plan the
 1582      # check wrote and refuses without one (audit #307 PL-001). This step
 1583      # used to run --apply alone, which the plan contract refuses (vm-qa run
 1584      # 68 on the fix build).
 1585      prc, pout = run_rc(dev, "cloud_content_restore --match")
 1586      rc, out = run_rc(dev, "cloud_content_restore --match --apply")
 1587      ok, items, detail = unit_protocol(out)
 1588      failures += not check(prc == 0 and rc == 0 and ok and sorted(items) == sorted([CONTENT_DIR, ghost]),
 1589                            f"--match --apply announced both chosen systems as ITEM i OF 2, the one with nothing to do included ({detail})",
 1590                            f"check exit {prc}, apply exit {rc}; {detail}; tail {out.strip()[-160:]!r}")
 1591      failures += not check(f"Nothing to remove from {ghost}" in out,
 1592                            "and said so for the system that already matches",
 1593                            "no 'Nothing to remove' line for the system with nothing to do")
 1594      dev.run(f"rm -rf /storage/roms/{shlex.quote(other)}")
 1595      dev.run("rm -f /storage/.cache/cloud_sync/content-systems")
 1596  
 1597      step("a system this device cannot run is marked unsupported")
 1598      # Plant a cloud directory for a system absent from es_systems.cfg.
 1599      backend("reset")
 1600      stage2 = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
 1601      os.makedirs(f"{stage2}/ROMs/definitely-not-a-system", exist_ok=True)
 1602      open(f"{stage2}/ROMs/definitely-not-a-system/x.rom", "wb").write(b"x")
 1603      cpath2 = epath(backend("content-remote"))
 1604      subprocess.run([BACKEND, "put", f"{stage2}/ROMs", f"{cpath2}/ROMs"], capture_output=True, text=True)
 1605      scan = dev.run("cloud_content_restore --scan 2>/dev/null || true")
 1606      row = [l for l in scan.splitlines() if l.startswith("definitely-not-a-system|")]
 1607      # name|cloud_bytes|supported|device_bytes|... -- the third field, not the tail
 1608      failures += not check(bool(row) and row[0].split("|")[2:3] == ["0"],
 1609                            "the unrunnable system is flagged 0 (unsupported)",
 1610                            f"scan did not mark it unsupported: {row or 'row absent'}")
 1611      # The comparison fields (2026-09-08): x.rom is one byte the device lacks;
 1612      # y.rom is one byte in the cloud and two here, so it is "not here" at the
 1613      # cloud's size and "not in the cloud" at the device's. Names alone would
 1614      # have called y.rom present on both sides. Expected, by planted sizes:
 1615      # cloud 2 bytes, unsupported, device 2 bytes, 2 files/2 bytes to restore,
 1616      # 1 file/2 bytes to back up.
 1617      open(f"{stage2}/ROMs/definitely-not-a-system/y.rom", "wb").write(b"y")
 1618      subprocess.run([BACKEND, "put", f"{stage2}/ROMs", f"{cpath2}/ROMs"], capture_output=True, text=True)
 1619      dev.write("/storage/roms/definitely-not-a-system/y.rom", b"yy")
 1620      scan = dev.run("cloud_content_restore --scan 2>/dev/null || true")
 1621      row = [l for l in scan.splitlines() if l.startswith("definitely-not-a-system|")]
 1622      failures += not check(bool(row) and row[0].split("|")[1:] == ["2", "0", "2", "2", "1", "2", "2"],
 1623                            "the scan says what a copy each way would move, in files and bytes",
 1624                            f"scan fields 2-8 were not 2|0|2|2|1|2|2: {row or 'row absent'}")
 1625      # The game list is sized, never compared (2026-09-08): three bytes in the
 1626      # cloud, five on the device. Under ROMs alone neither side lists a
 1627      # system's own list, so the row is what it was; under game content each
 1628      # total grows by its list and every comparison field stays put, since
 1629      # the list's direction is a modtime the scan does not have.
 1630      open(f"{stage2}/ROMs/definitely-not-a-system/gamelist.xml", "wb").write(b"ccc")
 1631      subprocess.run([BACKEND, "put", f"{stage2}/ROMs", f"{cpath2}/ROMs"], capture_output=True, text=True)
 1632      dev.write("/storage/roms/definitely-not-a-system/gamelist.xml", b"ddddd")
 1633      scan = dev.run("cloud_content_restore --scan 2>/dev/null || true")
 1634      row = [l for l in scan.splitlines() if l.startswith("definitely-not-a-system|")]
 1635      failures += not check(bool(row) and row[0].split("|")[1:] == ["2", "0", "2", "2", "1", "2", "2"],
 1636                            "under ROMs alone the game list is neither sized nor counted",
 1637                            f"scan fields 2-8 were not 2|0|2|2|1|2|2 with a game list present: {row or 'row absent'}")
 1638      scan = dev.run("cloud_content_restore --scan --with-media 2>/dev/null || true")
 1639      row = [l for l in scan.splitlines() if l.startswith("definitely-not-a-system|")]
 1640      failures += not check(bool(row) and row[0].split("|")[1:] == ["5", "0", "7", "2", "1", "2", "2"],
 1641                            "under game content the game list is sized on each side and never counted as moving",
 1642                            f"scan fields 2-8 were not 5|0|7|2|1|2|2: {row or 'row absent'}")
 1643      dev.run("rm -rf /storage/roms/definitely-not-a-system")
 1644  
 1645      step("a scan the cloud refused exits with rclone's code and lists nothing")
 1646      # The network is up and the cloud is not: the stanza's endpoint moved to a
 1647      # port nothing listens on, on the same host. This is the case the scan's
 1648      # network probe must not read as "no network" (that is LINK7's 69) and
 1649      # must not read as an empty cloud either -- it did, and the picker listed
 1650      # every system on the device as "not yet in your cloud" (2026-09-10).
 1651      good_conf = dev.run(f"cat {RCLONE_CONF}")
 1652      # The backend writes its own refusing stanza (#133). This was a sed over
 1653      # `url|endpoint`, which are the address fields of exactly two of the five
 1654      # backends: on SFTP, SMB and FTP it matched nothing, the scan ran against
 1655      # a working cloud, and the check that a refused cloud does not read as an
 1656      # empty one passed on a cloud that was never refused.
 1657      dead_port = backend("dead-port").strip()
 1658      dev.write(RCLONE_CONF, backend("dead-conf").encode())
 1659      moved = dev.run(f"grep -E '^(url|endpoint|port) *=' {RCLONE_CONF} || true").strip()
 1660      rc, out = run_rc(dev, "cloud_content_restore --scan")
 1661      dev.write(RCLONE_CONF, good_conf.encode())
 1662      rows = [l for l in out.splitlines() if l.count("|") >= 2]
 1663      failures += not check(dead_port in moved, f"the stanza's endpoint is the dead port {dead_port}",
 1664                            f"the stanza does not name the dead port {dead_port}: {moved!r}")
 1665      failures += not check(rc not in (0, 69) and not rows,
 1666                            f"the scan exited {rc} with no system lines",
 1667                            f"exit {rc} with {len(rows)} system line(s): a refused cloud read as an empty one")
 1668      rc, out = run_rc(dev, "cloud_content_restore --scan")
 1669      failures += not check(rc == 0 and any(l.count("|") >= 2 for l in out.splitlines()),
 1670                            "with the stanza restored the scan lists systems again (exit 0)",
 1671                            f"exit {rc} after restoring the stanza: {out.strip()[-120:]!r}")
 1672  
 1673      # --- folder seeding -----------------------------------------------------
 1674      step("seeding is idempotent and never clobbers an existing note")
 1675      seed_command = "cloud_setup --seed-folders saves,settings,roms,bios,media"
 1676      seed_rc, seed_out = run_rc(dev, seed_command)
 1677      failures += not check(seed_rc == 0,
 1678                            "explicit selected-category seeding completed",
 1679                            f"seeding exited {seed_rc}: {seed_out.strip()[-120:]}")
 1680      marker = b"OWNER WROTE THIS"
 1681      stage3 = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
 1682      open(f"{stage3}/README.txt", "wb").write(marker)
 1683      spath = epath(backend("saves-remote"))
 1684      subprocess.run([BACKEND, "put", stage3, spath], capture_output=True, text=True)
 1685      second_rc, second = run_rc(dev, seed_command)
 1686      failures += not check(second_rc == 0 and second.count("OK ") >= 2,
 1687                            "a second seeding run reports the folders present",
 1688                            f"second run exited {second_rc}: {second.strip()[:80]}")
 1689      note = subprocess.run([BACKEND, "cat", f"{spath}/README.txt"], capture_output=True).stdout
 1690      failures += not check(note == marker,
 1691                            "the owner's note survived a second seeding",
 1692                            f"the note was replaced: {note[:40]!r}")
 1693  
 1694      step("an older config's keys are carried across (D-UI-022, A12)")
 1695      # A conf shaped like one from before #73 -- old names, no new ones, and a
 1696      # RESTOREPATH equal to BACKUPPATH (the legal shape; the unequal one is a
 1697      # refusal, A12 proper). The helper carries every value to its new name.
 1698      saved_conf = dev.run(f"cat {CONF}")
 1699      old_conf = "\n".join([
 1700          'BACKUPPATH="/storage/qa-old-saves"', 'BACKUPFOLDER="/storage/qa-old-saves/backup"',
 1701          'RESTOREPATH="/storage/qa-old-saves"', 'SYNCPATH="/QA-OLD"', 'SYNCPATH_BACKUP="/QA-OLD-BACKUPS"',
 1702          'CONTENTPATH="/QA-OLD-CONTENT"', ""])
 1703      dev.write(CONF, old_conf.encode())
 1704      dev.run("cloud_sync_helper >/dev/null 2>&1 || true", check=False)
 1705      migrated = dev.run(f"cat {CONF}")
 1706      carried = {"SAVESPATH": "/storage/qa-old-saves", "SETTINGS_BACKUPS": "/storage/qa-old-saves/backup",
 1707                 "SAVES_REMOTE": "/QA-OLD", "SETTINGS_REMOTE": "/QA-OLD-BACKUPS", "CONTENT_REMOTE": "/QA-OLD-CONTENT"}
 1708      missing = [k for k, v in carried.items() if f'{k}="{v}"' not in migrated]
 1709      failures += not check(not missing, "every old key reached its new name with its value",
 1710                            f"not carried: {missing}")
 1711      dev.write(CONF, saved_conf.encode())
 1712  
 1713      # The one-record assertion over everything the suite touched (#105).
 1714      step("one last-known-good of every record, and no writer's litter, after the suite")
 1715      failures += litter_scan(dev, settings, remote)
 1716      return failures
 1717  
 1718  
 1719  # ===========================================================================
 1720  # Two devices against one cloud: the fixtures epic #11 builds against (#35)
 1721  # ===========================================================================
 1722  #
 1723  # Every fixture here is written before the code it tests and fails against
 1724  # the shipped scripts by design (`engineering-practices.md`, "A failure you
 1725  # find is yours to fix"): its first commit carries the failing output, and it
 1726  # turns green when #21/#22 land. The pair runs on GENERIC_X64 guests only
 1727  # (D-QA-009). A conflict is a change on both sides since two devices last
 1728  # agreed; one guest cannot make one, and a handheld is where a mistake
 1729  # becomes somebody's evening.
 1730  #
 1731  # a is the device under test; b is the other handheld, the one whose change
 1732  # a's copy has not seen. Every fixture begins with a first pass that brings
 1733  # both to agreement, because a suite that starts from an empty remote only
 1734  # ever tests first uploads (#53; the #35 futro).
 1735  
 1736  ID_FILE = "/storage/.config/cloud_sync-device-id"
 1737  LOG = "/var/log/cloud_sync.log"
 1738  CACHE = "/storage/.cache/cloud_sync"
 1739  
 1740  # The writers of the saves tree (#22 R1), as they run today: the startup
 1741  # sync EmulationStation runs at boot with SYNC SAVES DURING STARTUP on (the
 1742  # same pair as the SYNC SAVES WITH THE CLOUD row; it ran headless from the
 1743  # autostart 102-cloud-saves until #94); GuiMenu.cpp's SYNC SAVES WITH THE
 1744  # CLOUD, BACK UP SAVES TO THE CLOUD and RESTORE SAVES FROM THE CLOUD (the
 1745  # transfer page's SAVES tick runs the last two); FileData.cpp's game-exit
 1746  # push; and the two scripts from a shell. A1 runs each one. When a writer
 1747  # changes, this table changes in the same commit: the fixture tests what the
 1748  # labels run.
 1749  WRITERS = [
 1750      ("the startup sync (EmulationStation at boot; the autostart's pair until #94)",
 1751       "cloud_restore --yes --method=copy --update --saves-only; "
 1752       "cloud_backup --yes --method=copy --update --saves-only"),
 1753      ("SYNC SAVES WITH THE CLOUD",
 1754       "cloud_restore --yes --method=copy --update --saves-only && "
 1755       "cloud_backup --yes --method=copy --update --saves-only"),
 1756      ("BACK UP SAVES TO THE CLOUD (and the SAVES tick, backing up)",
 1757       "cloud_backup --yes --saves-only"),
 1758      ("RESTORE SAVES FROM THE CLOUD (and the SAVES tick, restoring)",
 1759       "cloud_restore --yes --saves-only"),
 1760      ("the game-exit push", "cloud_backup --yes --saves-only --recent"),
 1761      ("cloud_backup from a shell", "cloud_backup --yes"),
 1762      ("cloud_restore from a shell", "cloud_restore --yes"),
 1763  ]
 1764  BOOT_PAIR = WRITERS[0][1]
 1765  
 1766  # The wizard's apply step, as the two fixtures that need a decision call it.
 1767  # Named here, once, so they can run at all before #22/#23 exist: the command
 1768  # fails today and the fixtures with it. `left` keeps the cloud's copy -- the
 1769  # device's is the loser, pushed to the store first (#22 R9); `right` keeps
 1770  # the device's.
 1771  APPLY = "cloud_reconcile --apply --unit {unit} --keep {side}"
 1772  
 1773  
 1774  def sha(data):
 1775      return hashlib.sha256(data).hexdigest()
 1776  
 1777  
 1778  _PREFIX = None
 1779  _CAPS = None
 1780  
 1781  
 1782  def endpoint_prefix():
 1783      """What a remote path carries that the endpoint's own commands do not
 1784      want. Asked once and remembered: it is a property of the backend, not of
 1785      the run."""
 1786      global _PREFIX
 1787      if _PREFIX is None:
 1788          _PREFIX = backend("endpoint-prefix").strip()
 1789      return _PREFIX
 1790  
 1791  
 1792  def caps():
 1793      """What this endpoint can do: hash, modtime, commit (#133). A test that
 1794      legitimately cannot hold on a backend is marked with the reason it
 1795      cannot, never skipped in silence -- a silent skip is how a check that
 1796      proves nothing reads as a pass."""
 1797      global _CAPS
 1798      if _CAPS is None:
 1799          _CAPS = dict(kv.split("=", 1) for kv in backend("caps").split())
 1800      return _CAPS
 1801  
 1802  
 1803  def epath(remote_path):
 1804      """The endpoint path of a cloud path, for `cloud-test-backend cat/put/ls`.
 1805      On WebDAV and FTP the folder is the path; on S3 the first component is
 1806      the bucket and on SMB the share, which the backend's own commands already
 1807      prefix -- passing it again doubled the path, and the seeding step read
 1808      its note back from a place the device never looked. On SFTP the whole
 1809      data directory is the prefix, because an sshd running as an ordinary user
 1810      cannot chroot. The backend states its own prefix rather than the driver
 1811      guessing from the shape of the path."""
 1812      path = remote_path.strip()
 1813      pre = endpoint_prefix()
 1814      if pre and path.startswith(pre):
 1815          path = path[len(pre):]
 1816      return path.lstrip("/")
 1817  
 1818  
 1819  def rpath(*parts):
 1820      """A remote path for a fixture folder, under whatever root this endpoint
 1821      needs: nothing on WebDAV and FTP, the bucket on S3, the share on SMB, the
 1822      data directory on SFTP (#133).
 1823  
 1824      A hard-coded "/QA-Custom" is a legal folder on Dropbox and an illegal
 1825      bucket name on S3, so cloud_setup refused it and six checks below failed
 1826      for a reason that had nothing to do with the code under test. The path a
 1827      fixture asks for has to be one this endpoint could actually hold."""
 1828      return endpoint_prefix() + "".join("/" + str(x).strip("/") for x in parts)
 1829  
 1830  
 1831  def backend_bytes(path):
 1832      p = subprocess.run([BACKEND, "cat", path], capture_output=True)
 1833      return p.stdout if p.returncode == 0 else None
 1834  
 1835  
 1836  def backend_files(path):
 1837      """Every file under an endpoint path, as paths relative to it."""
 1838      out = subprocess.run([BACKEND, "ls", path], capture_output=True, text=True).stdout
 1839      return [line.split(None, 1)[1] for line in out.splitlines() if len(line.split(None, 1)) == 2]
 1840  
 1841  
 1842  def backend_sizes(path):
 1843      """Every file under an endpoint path with its size: {relative path: bytes}."""
 1844      out = subprocess.run([BACKEND, "ls", path], capture_output=True, text=True).stdout
 1845      sizes = {}
 1846      for line in out.splitlines():
 1847          parts = line.split(None, 1)
 1848          if len(parts) == 2 and parts[0].isdigit():
 1849              sizes[parts[1]] = int(parts[0])
 1850      return sizes
 1851  
 1852  
 1853  def set_key(dev, key, val):
 1854      dev.run(f"grep -q '^{key}=' {CONF} && sed -i 's|^{key}=.*|{key}=\"{val}\"|' {CONF} "
 1855              f"|| echo '{key}=\"{val}\"' >> {CONF}")
 1856  
 1857  
 1858  def apply_settings(dev, settings):
 1859      for key, val in settings.items():
 1860          set_key(dev, key, val)
 1861  
 1862  
 1863  UNIT_MARK = re.compile(r"^>>> unit (.*)\|(\d*)\|(\d*)$")
 1864  
 1865  
 1866  def unit_protocol(out):
 1867      """What the transfer page needs from a script's `>>> unit <item>|i|n`
 1868      markers (#95): the page shows ITEM i OF n with the script's own n, so
 1869      every n must be the same and equal to the number of announcements the
 1870      run actually made, and i their running count, 1..n in order. A unit
 1871      skipped without an announcement, or a stale n, reads on the page as a
 1872      run that ended short (ITEM 2 OF 3). The saves scripts announce
 1873      `SAVES||` and `SETTINGS||` with no numbers and let the page count; that
 1874      shape passes when every marker in the run is unnumbered, and a mix does
 1875      not. Returns (ok, items in order, a line for the message). A run with no
 1876      marker at all is (True, [], ...) -- the caller says whether it expected one."""
 1877      marks = [m.groups() for m in map(UNIT_MARK.match, out.splitlines()) if m]
 1878      items = [item for item, _, _ in marks]
 1879      detail = "announced " + ", ".join(f"{item}|{i}|{n}" for item, i, n in marks) if marks else "no unit announcement"
 1880      if not marks:
 1881          return True, items, detail
 1882      if all(i == "" and n == "" for _, i, n in marks):
 1883          return True, items, detail
 1884      ok = (all(i.isdigit() and n.isdigit() for _, i, n in marks)
 1885            and len({n for _, _, n in marks}) == 1
 1886            and int(marks[0][2]) == len(marks)
 1887            and [int(i) for _, i, _ in marks] == list(range(1, len(marks) + 1)))
 1888      return ok, items, detail
 1889  
 1890  
 1891  def run_rc(dev, cmd, env=""):
 1892      """Run a command the way its caller does; return (exit code, its output)."""
 1893      out = dev.run(f"( {env} {cmd} ) >/tmp/qa-run.out 2>&1; echo rc=$?; cat /tmp/qa-run.out", check=False)
 1894      first, _, rest = out.partition("\n")
 1895      return (int(first[3:]) if first.startswith("rc=") else -1), rest
 1896  
 1897  
 1898  def touch_offset(dev, path, seconds):
 1899      """Move a file's mtime relative to the device's clock -- the lever the
 1900      shipped pipeline resolves by. busybox touch takes a date, not @epoch."""
 1901      dev.run(f'touch -d "$(date -d @$(( $(date +%s) + ({seconds}) )) \'+%Y-%m-%d %H:%M:%S\')" {shlex.quote(path)}')
 1902  
 1903  
 1904  def log_mark(dev):
 1905      return int(dev.run(f"wc -l < {LOG} 2>/dev/null || echo 0").strip() or 0)
 1906  
 1907  
 1908  def os_name(dev):
 1909      """What every settings archive's name ends with: OS_NAME, read from the
 1910      file /etc/profile reads it from, since an ssh session has run no profile."""
 1911      return dev.run('. /etc/os-release 2>/dev/null; echo "$OS_NAME"', check=False).strip() or "ROCKNIX"
 1912  
 1913  
 1914  def log_since(dev, mark):
 1915      return dev.run(f"tail -n +{mark + 1} {LOG} 2>/dev/null || true")
 1916  
 1917  
 1918  def name_of(digest, known):
 1919      """Which planted version a hash is, for a message somebody can read."""
 1920      for name, data in known.items():
 1921          if digest == sha(data):
 1922              return name
 1923      return "absent" if digest is None else "neither (partial or foreign bytes)"
 1924  
 1925  
 1926  class Pair:
 1927      def __init__(self, a, b, root, settings):
 1928          self.a, self.b, self.root, self.settings = a, b, root, settings
 1929          self.saves_remote = settings["SAVES_REMOTE"]
 1930          self.spath = epath(self.saves_remote)
 1931  
 1932      def path(self, rel):
 1933          return f"{self.root}/{rel}"
 1934  
 1935      def reset(self):
 1936          """Empty the cloud and both saves trees, forget every stamp and
 1937          record, put both devices back on the shared folder. Each fixture
 1938          starts from nothing, so what one leaves behind cannot pass the next."""
 1939          backend("reset")
 1940          for d in (self.a, self.b):
 1941              d.run(f"rm -rf {shlex.quote(self.root)} {CACHE}; mkdir -p {shlex.quote(self.root)} {CACHE}")
 1942              apply_settings(d, self.settings)
 1943  
 1944      def cloud_sha(self, rel, folder=None):
 1945          data = backend_bytes(f"{self.spath if folder is None else folder}/{rel}")
 1946          return sha(data) if data is not None else None
 1947  
 1948      def agree(self, files):
 1949          """The first pass: a backs up, b restores, both hold what the cloud holds."""
 1950          for rel, data in files.items():
 1951              self.a.write(self.path(rel), data)
 1952          rc, _ = run_rc(self.a, "cloud_backup --yes --saves-only")
 1953          rc2, _ = run_rc(self.b, "cloud_restore --yes --saves-only")
 1954          wrong = [rel for rel, data in files.items()
 1955                   if not (self.cloud_sha(rel) == sha(data) == self.b.sha(self.path(rel)))]
 1956          if wrong:
 1957              raise Fail(f"the first pass left {wrong} without agreement (backup exit {rc}, restore exit {rc2})")
 1958  
 1959      def both_changed(self, rel, h0, ha, hb, a_offset=3600):
 1960          """Agreement on h0; b publishes hb; a edits to ha offline, its copy
 1961          `a_offset` seconds newer (positive) or older than b's upload."""
 1962          self.reset()
 1963          self.agree({rel: h0})
 1964          self.b.write(self.path(rel), hb)
 1965          run_rc(self.b, "cloud_backup --yes --saves-only")
 1966          if self.cloud_sha(rel) != sha(hb):
 1967              raise Fail("b's publication did not reach the cloud")
 1968          self.a.write(self.path(rel), ha)
 1969          touch_offset(self.a, self.path(rel), a_offset)
 1970  
 1971  
 1972  def fx_a1(p):
 1973      """A1: two devices agree on H0; b publishes HB; a edits to HA offline and
 1974      runs every writer. Neither HA nor HB may be overwritten anywhere, and one
 1975      conflict is reported. As shipped each writer is a recency resolver
 1976      (blindspot 28): the cloud's copy or this device's is replaced, and
 1977      nothing says so."""
 1978      f = 0
 1979      rel = "saves/Both Changed.srm"
 1980      v = {"H0": b"H0: what both devices agreed on",
 1981           "HA": b"HA: this device's edit, made offline, never seen by the cloud",
 1982           "HB": b"HB: the other device's edit, already published"}
 1983      for label, cmd in WRITERS:
 1984          lost, rcs = [], []
 1985          for timing, offset in (("this device's copy newer", 3600), ("the cloud's copy newer", -3600)):
 1986              p.both_changed(rel, v["H0"], v["HA"], v["HB"], offset)
 1987              rc, _ = run_rc(p.a, cmd)
 1988              rcs.append(rc)
 1989              cloud, local = p.cloud_sha(rel), p.a.sha(p.path(rel))
 1990              if cloud != sha(v["HB"]):
 1991                  lost.append(f"{timing}: the cloud's HB became {name_of(cloud, v)}")
 1992              if local != sha(v["HA"]):
 1993                  lost.append(f"{timing}: this device's HA became {name_of(local, v)}")
 1994          f += not check(not lost, f"{label}: neither HA nor HB was overwritten",
 1995                         f"{label}: " + "; ".join(lost) + " (blindspot 28)")
 1996          f += not check(all(rc == 5 for rc in rcs),
 1997                         f"{label}: reported one queued conflict (exit 5)",
 1998                         f"{label}: no conflict reported (exit {rcs[0]} / {rcs[1]})")
 1999      return f
 2000  
 2001  
 2002  def fx_a2(p):
 2003      """A2: a failed push is retried at the next exit with nothing changed; an
 2004      equal-size, equal-mtime byte change enters the changed set at the next
 2005      full pass -- the hash catches what size and mtime cannot (#53's shape,
 2006      on a save)."""
 2007      f = 0
 2008      rel = "saves/Retry.srm"
 2009      v = {"H0": b"H0 agreed", "HA": b"HA: changed while the cloud was unreachable"}
 2010      p.reset()
 2011      p.agree({rel: v["H0"]})
 2012      p.a.write(p.path(rel), v["HA"])
 2013      # One push fails the way a lapsed sign-in does: the remote's password
 2014      # (or S3 secret) wrong for that run, then put back. A closed port would
 2015      # do too, but rclone retries a refused connection for ten minutes.
 2016      good = p.a.run(f"cat {RCLONE_CONF}")
 2017      p.a.run(f"sed -i \"s|^pass = .*|pass = $(rclone obscure wrong-password)|; s|^secret_access_key = .*|secret_access_key = wrong|\" {RCLONE_CONF}")
 2018      rc1, _ = run_rc(p.a, "cloud_backup --yes --saves-only --recent")
 2019      p.a.write(RCLONE_CONF, good.encode())
 2020      f += not check(rc1 != 0, f"the push failed while the cloud refused the sign-in (exit {rc1}; the setup)",
 2021                     "a push the cloud refused reported success")
 2022      rc2, _ = run_rc(p.a, "cloud_backup --yes --saves-only --recent")
 2023      f += not check(p.cloud_sha(rel) == sha(v["HA"]),
 2024                     "the next exit, with nothing changed since, retried and published",
 2025                     f"the failed push was not retried: the cloud holds {name_of(p.cloud_sha(rel), v)} (exit {rc2})")
 2026  
 2027      rel = "saves/Same Size.srm"
 2028      one, two = b"version-one-of-this-save", b"version-two-of-this-save"
 2029      assert len(one) == len(two)
 2030      p.reset()
 2031      p.agree({rel: one})
 2032      # On b: new bytes, the same length, the mtime put back to what it was.
 2033      q = shlex.quote(p.path(rel))
 2034      p.b.run(f"cp -p {q} {q}.ref")
 2035      p.b.write(p.path(rel), two)
 2036      p.b.run(f"touch -r {q}.ref {q}; rm -f {q}.ref; sync")
 2037      run_rc(p.b, "cloud_backup --yes --saves-only")
 2038      run_rc(p.a, "cloud_restore --yes --saves-only")
 2039      f += not check(p.a.sha(p.path(rel)) == sha(two),
 2040                     "an equal-size, equal-mtime byte change entered the changed set at the full pass",
 2041                     "an equal-size, equal-mtime byte change was never noticed: size and mtime matched "
 2042                     "and nothing hashed, so a still holds version one (A2)")
 2043      return f
 2044  
 2045  
 2046  def fx_a3(p):
 2047      """A3: CHANGE CLOUD FOLDER to a folder holding different saves. Nothing
 2048      downloads silently; identical pairs seed agreement; differing pairs
 2049      queue. As shipped the pass after a re-link is the boot pair, which
 2050      replaces this device's copy with the folder's newer one."""
 2051      f = 0
 2052      same, diff = "saves/Same In Both.srm", "saves/Differs.srm"
 2053      v = {"H0": b"H0: in both folders", "X": b"X: this device's version",
 2054           "Y": b"Y: the other folder's version, never seen here"}
 2055      p.reset()
 2056      p.agree({same: v["H0"], diff: v["X"]})
 2057      second = p.saves_remote.rstrip("/") + "-second"
 2058      set_key(p.b, "SAVES_REMOTE", second)
 2059      p.b.write(p.path(same), v["H0"])
 2060      p.b.write(p.path(diff), v["Y"])
 2061      run_rc(p.b, "cloud_backup --yes --saves-only")
 2062      set_key(p.b, "SAVES_REMOTE", p.saves_remote)
 2063      if p.cloud_sha(diff, epath(second)) != sha(v["Y"]):
 2064          raise Fail("b could not fill the second folder")
 2065      # a changes folder the way CHANGE CLOUD FOLDER does; its differing copy is
 2066      # older than the folder's, the shape recency gets wrong.
 2067      rc, out = run_rc(p.a, f"cloud_setup --set-saves-remote {shlex.quote(second)}")
 2068      if rc != 0:
 2069          raise Fail(f"cloud_setup --set-saves-remote refused {second}: {out.strip()[-80:]}")
 2070      touch_offset(p.a, p.path(diff), -3600)
 2071      rc, _ = run_rc(p.a, BOOT_PAIR)
 2072      got = p.a.sha(p.path(diff))
 2073      f += not check(got == sha(v["X"]), "nothing on this device was replaced by the new folder's saves",
 2074                     f"A SAVE WAS SILENTLY REPLACED after CHANGE CLOUD FOLDER: {diff} became {name_of(got, v)} (A3)")
 2075      f += not check(p.a.sha(p.path(same)) == sha(v["H0"]), "the identical pair is untouched", "the identical pair changed")
 2076      f += not check(rc == 5, "the differing pair was queued (exit 5)", f"no queue for the differing pair (exit {rc})")
 2077      agreed = p.a.run(f"cat {CACHE}/agreed.json 2>/dev/null || true")
 2078      f += not check(same in agreed and diff not in agreed,
 2079                     "the identical pair seeded agreement and the differing one did not",
 2080                     "no agreement record for the identical pair" if not agreed.strip()
 2081                     else "the agreement record is wrong about which pair agrees")
 2082      return f
 2083  
 2084  
 2085  def fx_a8(p):
 2086      """A8: a publication interrupted after one member of an N64 pair (.eep and
 2087      .mpk: one unit). No device installs the mixed set; an unrelated unit still
 2088      moves; the hold clears when the second member lands.
 2089  
 2090      The pair sits beside the ROM (n64/Torn.eep, n64/Torn.mpk): every shipped
 2091      mupen64plus.cfg has SaveSRAMPath = "/storage/roms/n64", so that is the
 2092      layout the emulator writes and the unit capture can see (#21). It was
 2093      n64/save/, a directory only the allowlist ever named."""
 2094      f = 0
 2095      eep, mpk, other = "n64/Torn.eep", "n64/Torn.mpk", "saves/Unrelated.srm"
 2096      e = {"old": os.urandom(2048), "new": os.urandom(2560)}
 2097      m = {"old": os.urandom(32768), "new": os.urandom(40960)}
 2098      u0, u1 = b"unrelated, agreed", b"unrelated, changed on a meanwhile"
 2099      p.reset()
 2100      try:
 2101          p.agree({eep: e["old"], mpk: m["old"], other: u0})
 2102      except Fail as x:
 2103          # The shipped allowlist admits n64/save/*.eep and **/*.srm, not the
 2104          # .eep/.mpk the emulator writes beside the ROM, so until the includes
 2105          # land (#89, the allowlist issue split from #21) the pair never
 2106          # reaches the cloud and A8 cannot get past its first pass. Say so --
 2107          # but only when the evidence is that shape: the .srm made it and
 2108          # neither member of the pair did. A backend outage or a broken
 2109          # cloud_backup is re-raised as itself, not dressed as the known gap.
 2110          if p.cloud_sha(other) == sha(u0) and not p.cloud_sha(eep) and not p.cloud_sha(mpk):
 2111              raise Fail(f"{x} -- a standalone N64 pair beside the ROM is not in the sync allowlist yet "
 2112                         "(+ /**/*.eep, + /**/*.mpk: #89, the allowlist issue split from #21); A8 waits on it")
 2113          raise
 2114      p.b.write(p.path(eep), e["new"])
 2115      p.b.write(p.path(mpk), m["new"])
 2116      # b publishes one file at a time at 8 KiB/s; rclone is killed once the
 2117      # .eep (first by name) has landed and the .mpk is still in flight.
 2118      p.b.run("rm -f /tmp/qa-torn.out; (RCLONE_TRANSFERS=1 RCLONE_BWLIMIT=8k setsid cloud_backup --yes --saves-only "
 2119              ">/tmp/qa-torn.out 2>&1 &)")
 2120      for _ in range(120):
 2121          time.sleep(0.25)
 2122          if p.cloud_sha(eep) == sha(e["new"]):
 2123              break
 2124      p.b.run("pkill -9 -x rclone; for i in $(seq 40); do pgrep -x cloud_backup >/dev/null || break; sleep 0.25; done; true",
 2125              check=False)
 2126      torn = p.cloud_sha(eep) == sha(e["new"]) and p.cloud_sha(mpk) != sha(m["new"])
 2127      f += not check(torn, "b's publication was interrupted after its first member (the setup)",
 2128                     f"could not leave the publication torn: .eep is {name_of(p.cloud_sha(eep), e)}, "
 2129                     f".mpk is {name_of(p.cloud_sha(mpk), m)}")
 2130      if not torn:
 2131          return f
 2132      p.a.write(p.path(other), u1)
 2133      run_rc(p.a, BOOT_PAIR)
 2134      got = (name_of(p.a.sha(p.path(eep)), e), name_of(p.a.sha(p.path(mpk)), m))
 2135      f += not check(got in {("old", "old"), ("new", "new")}, f"a installed no mixed set (its pair is {got[0]}/{got[1]})",
 2136                     f"A MIXED SET WAS INSTALLED on a: .eep {got[0]}, .mpk {got[1]} (A8)")
 2137      f += not check(p.cloud_sha(other) == sha(u1), "an unrelated unit still moved while the torn one was held",
 2138                     "the unrelated unit did not move")
 2139      run_rc(p.b, "cloud_backup --yes --saves-only")
 2140      run_rc(p.a, BOOT_PAIR)
 2141      got = (name_of(p.a.sha(p.path(eep)), e), name_of(p.a.sha(p.path(mpk)), m))
 2142      f += not check(got == ("new", "new"), "the hold cleared when the second member landed",
 2143                     f"after the second member landed a holds .eep {got[0]}, .mpk {got[1]}")
 2144      return f
 2145  
 2146  
 2147  def fx_a9(p):
 2148      """A9: delete and renumber on one device, sync repeatedly on the other; a
 2149      retired hash put back; an unexplained rm; a saves root that is unmounted,
 2150      empty, or pointed at an empty cloud folder, with agreement on record.
 2151  
 2152      The states live under savestates/gba/ and the save under gba/ -- the
 2153      layout ES and RetroArch write, so the unit is one capture can see (#21).
 2154      Where the deletion models the save-state manager's, `cloud_capture
 2155      --retire` runs before the unlink, as GuiSaveState does, so the retired
 2156      record #22 needs exists in the case that tests it (D-CLOUD-053)."""
 2157      f = 0
 2158      s = {"S1": os.urandom(3001), "S2": os.urandom(3002), "S3": os.urandom(3003)}
 2159      st = lambda n: f"savestates/gba/Renumber.state{n}"
 2160      p.reset()
 2161      p.agree({st(1): s["S1"], st(2): s["S2"], st(3): s["S3"]})
 2162      # a deletes slot 2 from the manager -- which records the deletion first
 2163      # -- and ES renumbers: slot 3 becomes slot 2.
 2164      rc, _ = run_rc(p.a, f"cloud_capture --retire {shlex.quote(p.path(st(2)))}")
 2165      rows = [r for r in (manifest_of(p.a) or {}).get("retired") or [] if r.get("path") == st(2)]
 2166      f += not check(rc == 0 and bool(rows) and rows[0].get("sha256") == sha(s["S2"]),
 2167                     "the manager's deletion left a retired row for state2 with S2's sha (#21; the record #22 propagates)",
 2168                     f"cloud_capture --retire exited {rc}; retired rows for state2: {[(r.get('sha256') or '')[:8] for r in rows]} "
 2169                     "-- the #22 checks below would fail on a #21 precondition")
 2170      p.a.run(f"rm -f {shlex.quote(p.path(st(2)))}; mv {shlex.quote(p.path(st(3)))} {shlex.quote(p.path(st(2)))}")
 2171      run_rc(p.a, BOOT_PAIR)
 2172      for _ in range(2):
 2173          run_rc(p.b, BOOT_PAIR)
 2174  
 2175      def on(dev):
 2176          out = dev.run(f"cd {shlex.quote(p.root)} && sha256sum savestates/gba/* 2>/dev/null || true")
 2177          return sorted(name_of(line.split()[0], s) for line in out.splitlines() if line.strip())
 2178  
 2179      def in_cloud():
 2180          return sorted(name_of(sha(backend_bytes(f"{p.spath}/{rel}") or b""), s)
 2181                        for rel in backend_files(p.spath) if rel.startswith("savestates/"))
 2182  
 2183      f += not check(on(p.b) == ["S1", "S3"], "after repeated syncs b holds S1 and S3, each exactly once",
 2184                     f"b holds {on(p.b)} (A9: each surviving version exactly once)")
 2185      f += not check(in_cloud() == ["S1", "S3"], "and so does the cloud", f"the cloud holds {in_cloud()}")
 2186      # The retired hash put back, as the discarded-saves tool would: a new
 2187      # publication, which the old retired record must not consume.
 2188      p.a.write(p.path(st(3)), s["S2"])
 2189      run_rc(p.a, BOOT_PAIR)
 2190      run_rc(p.b, BOOT_PAIR)
 2191      f += not check(on(p.b) == ["S1", "S2", "S3"], "a retired hash put back reached b as a new publication",
 2192                     f"b holds {on(p.b)} after the retired hash was put back")
 2193  
 2194      # An unexplained absence: rm, not ES's delete, so no retired record.
 2195      gone, kept = "gba/Removed By Hand.srm", "saves/Kept.srm"
 2196      g0 = b"removed by rm on a"
 2197      p.reset()
 2198      p.agree({gone: g0, kept: b"kept"})
 2199      p.a.run(f"rm -f {shlex.quote(p.path(gone))}")
 2200      rc, _ = run_rc(p.a, BOOT_PAIR)
 2201      f += not check(p.a.sha(p.path(gone)) is None, "the file removed by hand was not put back on a",
 2202                     "THE FILE REMOVED BY HAND CAME BACK: an absence was resolved by a download (A9)")
 2203      f += not check(p.cloud_sha(gone) == sha(g0), "and the cloud's copy was not deleted",
 2204                     "the cloud's copy was deleted on an unexplained absence")
 2205      f += not check(rc == 5, "a question was queued (exit 5)", f"no question queued (exit {rc})")
 2206      run_rc(p.b, BOOT_PAIR)
 2207      f += not check(p.b.sha(p.path(gone)) == sha(g0), "b's copy was untouched", "b's copy was touched by a's unexplained absence")
 2208  
 2209      # Mass absence, with agreement on record: the root unmounted, then empty,
 2210      # then the cloud folder empty. Every pass refuses and names the reason.
 2211      p.reset()
 2212      p.agree({"saves/On Record.srm": b"agreed and on record"})
 2213      passes = WRITERS[:5]
 2214      q = shlex.quote(p.root)
 2215      p.a.run(f"mv {q} {q}.away")
 2216      try:
 2217          runs = [run_rc(p.a, c) for _, c in passes]
 2218          rcs = [rc for rc, _ in runs]
 2219          present = p.a.run(f"find {q} -type f 2>/dev/null | wc -l").strip()
 2220      finally:
 2221          p.a.run(f"rm -rf {q}; mv {q}.away {q}")
 2222      f += not check(all(rc == 1 for rc in rcs), "with the saves root unmounted every pass refused (exit 1)",
 2223                     f"passes on an unmounted root exited {rcs} (A9: refuse, reason named)")
 2224      f += assert_message(runs[0][1], runs[0][0], label="the refusal (unmounted root): ")
 2225      f += not check(present == "0", "and nothing was written where the root should be",
 2226                     f"{present} file(s) were written into a root that was not mounted")
 2227      p.a.run(f"mv {q} {q}.away; mkdir -p {q}")
 2228      try:
 2229          runs = [run_rc(p.a, c) for _, c in passes]
 2230          rcs = [rc for rc, _ in runs]
 2231          present = p.a.run(f"find {q} -type f 2>/dev/null | wc -l").strip()
 2232      finally:
 2233          p.a.run(f"rm -rf {q}; mv {q}.away {q}")
 2234      f += not check(all(rc == 1 for rc in rcs), "with the saves root empty every pass refused (exit 1)",
 2235                     f"passes on an empty root exited {rcs}")
 2236      f += assert_message(runs[0][1], runs[0][0], label="the refusal (empty root): ")
 2237      f += not check(present == "0", "and nothing was downloaded into it",
 2238                     f"{present} file(s) were downloaded into an empty root with agreement on record")
 2239      empty = p.saves_remote.rstrip("/") + "-empty"
 2240      set_key(p.a, "SAVES_REMOTE", empty)
 2241      runs = [run_rc(p.a, c) for _, c in passes]
 2242      rcs = [rc for rc, _ in runs]
 2243      set_key(p.a, "SAVES_REMOTE", p.saves_remote)
 2244      f += assert_message(runs[0][1], runs[0][0], label="the refusal (empty cloud folder): ")
 2245      uploaded = backend_files(epath(empty))
 2246      f += not check(all(rc == 1 for rc in rcs), "with the cloud folder empty every pass refused (exit 1)",
 2247                     f"passes against an empty cloud folder exited {rcs}")
 2248      f += not check(not uploaded, "and nothing was uploaded to it",
 2249                     f"{len(uploaded)} file(s) were uploaded into an empty cloud folder with agreement on record")
 2250      queued = p.a.run(f"cat {CACHE}/queue.json 2>/dev/null || true").strip()
 2251      f += not check(not queued, "no question was queued for a mass absence", "a mass absence queued questions")
 2252      return f
 2253  
 2254  
 2255  def fx_a11(p):
 2256      """A11: a cloned card -- the second device carries the first's identity.
 2257      It refuses to publish with duplicate-device-id and transfers nothing."""
 2258      f = 0
 2259      rel = "saves/Cloned.srm"
 2260      h0 = b"H0 published by the first card"
 2261      a_id = p.a.run("cloud_device_id").strip()
 2262      prev = p.b.run(f"cat {ID_FILE} 2>/dev/null || true")
 2263      p.reset()
 2264      p.agree({rel: h0})
 2265      p.b.write(ID_FILE, (a_id + "\n").encode())
 2266      try:
 2267          p.b.write(p.path(rel), b"HB from the clone")
 2268          mark = log_mark(p.b)
 2269          rc, out = run_rc(p.b, "cloud_backup --yes --saves-only")
 2270          said = "duplicate-device-id" in out + log_since(p.b, mark)
 2271          f += not check(rc == 1 and said, "the clone was refused with duplicate-device-id",
 2272                         f"THE CLONE PUBLISHED (exit {rc}, no duplicate-device-id refusal) (A11)")
 2273          f += not check(p.cloud_sha(rel) == sha(h0), "and transferred nothing",
 2274                         "the clone's copy replaced the first card's in the cloud")
 2275      finally:
 2276          p.b.write(ID_FILE, prev.encode())
 2277      return f
 2278  
 2279  
 2280  def fx_a12(p):
 2281      """A12 (D-CLOUD-040): an upgraded config carrying a legacy RESTOREPATH
 2282      unlike BACKUPPATH. The helper migrates SAVESPATH from BACKUPPATH, drops
 2283      RESTOREPATH and writes one WARN naming the ignored folder; nothing in that
 2284      folder is touched; the passes proceed."""
 2285      f = 0
 2286      a = p.a
 2287      other = SCRATCH + "-other"
 2288      p.reset()
 2289      p.agree({"saves/Agreed.srm": b"agreed before the upgrade"})
 2290      untouched = b"lives in the folder RESTOREPATH named"
 2291      a.write(f"{other}/saves/Untouched.srm", untouched)
 2292      saved = a.run(f"cat {CONF}")
 2293      keep = [l for l in saved.splitlines()
 2294              if not re.match(r"^(SAVESPATH|SETTINGS_BACKUPS|SAVES_REMOTE|SETTINGS_REMOTE|CONTENT_REMOTE)=", l)]
 2295      old = keep + [f'BACKUPPATH="{p.root}"', f'BACKUPFOLDER="{p.root}/backup"', f'RESTOREPATH="{other}"',
 2296                    f'SYNCPATH="{p.settings["SAVES_REMOTE"]}"', f'SYNCPATH_BACKUP="{p.settings["SETTINGS_REMOTE"]}"',
 2297                    f'CONTENTPATH="{p.settings["CONTENT_REMOTE"]}"', ""]
 2298      a.write(CONF, "\n".join(old).encode())
 2299      try:
 2300          mark = log_mark(a)
 2301          rc_h, out_h = run_rc(a, f"cloud_sync_helper {LOG}")
 2302          f += assert_message(out_h, rc_h, label="the helper's migration: ")
 2303          conf = a.run(f"cat {CONF}")
 2304          warns = [l for l in log_since(a, mark).splitlines() if "WARN" in l and other in l]
 2305          f += not check(f'SAVESPATH="{p.root}"' in conf, "SAVESPATH was migrated from BACKUPPATH",
 2306                         "SAVESPATH was not carried from BACKUPPATH")
 2307          f += not check("RESTOREPATH=" not in conf, "RESTOREPATH was dropped",
 2308                         "RESTOREPATH is still in the config (A12: dropped, warned once)")
 2309          f += not check(len(warns) == 1, "one WARN names the ignored folder",
 2310                         f"{len(warns)} WARN line(s) name {other}; expected exactly one")
 2311          rc, _ = run_rc(a, BOOT_PAIR)
 2312          f += not check(rc == 0, "the pass proceeded (exit 0)", f"the pass refused (exit {rc}) instead of migrating")
 2313          f += not check(a.sha(f"{other}/saves/Untouched.srm") == sha(untouched),
 2314                         "nothing in the ignored folder was touched", "the ignored folder was touched")
 2315      finally:
 2316          a.write(CONF, saved.encode())
 2317          a.run(f"rm -rf {shlex.quote(other)}")
 2318      return f
 2319  
 2320  
 2321  def fx_a14(p):
 2322      """A14: the manifest step, in two halves. #21's: a state (with its
 2323      thumbnail) and a save planted on the unit layout, the producer run the way
 2324      ES runs it at exit -- the working copy at /storage/.cache/cloud_sync holds
 2325      an entry for both with the planted shas. #22's: the exit path pushes it,
 2326      so the manifest is on the remote under savestates/.rocknix/ with the same
 2327      sha256, remote_hash null on WebDAV and non-null on MinIO; and the
 2328      ROMs-and-BIOS tier never sees the savestates directory. The remote checks
 2329      stay, and stay failing, until #22 pushes the file.
 2330  
 2331      The paths carry a <system> component because no unit table can see
 2332      savestates/Manifest Game.state1 or saves/Manifest Game.srm: without the
 2333      layout and without a call to the producer, nothing would ever have
 2334      written the entry this fixture asserted."""
 2335      f = 0
 2336      state, save = "savestates/gba/Manifest Game.state1", "gba/Manifest Game.srm"
 2337      sbytes, vbytes = b"#RZIPv" + os.urandom(2000), os.urandom(512)
 2338      p.reset()
 2339      p.a.write(p.path(state), sbytes)
 2340      p.a.write(p.path(state + ".png"), b"\x89PNG" + os.urandom(300))
 2341      p.a.write(p.path(save), vbytes)
 2342      rc, _ = capture(p.a, p.root, "gba", p.path("gba/Manifest Game.gba"))
 2343      a_id = p.a.run("cloud_device_id").strip()
 2344      local = manifest_of(p.a)
 2345      got = {rel: (entry(local, rel) or {}).get("sha256") for rel in (state, save)}
 2346      f += not check(rc == 0 and got[state] == sha(sbytes) and got[save] == sha(vbytes),
 2347                     f"the working copy {CACHE}/manifest-{a_id}.json holds both entries with the planted shas (#21)",
 2348                     f"exit {rc}; working copy {'absent' if local is None else 'present'}; entries "
 2349                     f"{ {k: (v or '')[:8] for k, v in got.items()} } (#21)")
 2350      run_rc(p.a, "cloud_backup --yes --saves-only --recent")
 2351      mpath = f"{p.spath}/savestates/.rocknix/manifest-{a_id}.json"
 2352      raw = backend_bytes(mpath)
 2353      f += not check(raw is not None, "the manifest reached the cloud under savestates/.rocknix/",
 2354                     f"no manifest at {mpath} after the exit path (A14)")
 2355      if raw is not None:
 2356          try:
 2357              m = json.loads(raw)
 2358          except ValueError:
 2359              m = {}
 2360          pushed = m.get("entries", {}).get(state) if isinstance(m, dict) else None
 2361          f += not check(bool(pushed) and pushed.get("sha256") == sha(sbytes),
 2362                         "its entry for the state carries the planted bytes' sha256 (#22)",
 2363                         "the pushed manifest has no entry for the state, or its sha256 is not the planted bytes' (#22)")
 2364          kind = backend("backend").strip()
 2365          # Whether a remote hash exists at all is the backend's property, not
 2366          # WebDAV's: three of the five carry no hash (#133), and reading the
 2367          # name rather than the capability made this check assert "non-null"
 2368          # against SFTP, SMB and FTP, where null is the correct answer.
 2369          hashless = caps()["hash"] == "none"
 2370          rh = (pushed or {}).get("remote_hash", "unset")
 2371          f += not check((rh is None) if hashless else rh not in (None, "unset"),
 2372                         f"remote_hash is {'null' if hashless else 'non-null'} on {kind} (hash={caps()['hash']})",
 2373                         f"remote_hash is {rh!r} on {kind} (hash={caps()['hash']})")
 2374      listed = p.a.run("cloud_content_backup --list 2>/dev/null || true").split()
 2375      f += not check("savestates" not in listed, "the ROMs-and-BIOS tier never offers savestates",
 2376                     "the content tier offers the savestates directory (the manifest would ride twice)")
 2377      return f
 2378  
 2379  
 2380  def fx_a5(p):
 2381      """A5: a test-only reader answers "this game, newest first, thumbnail,
 2382      producing device, winning side" from the cloud store alone, on a second
 2383      device that never made the decision."""
 2384      f = 0
 2385      rel = "savestates/Decided.state1"
 2386      p.both_changed(rel, os.urandom(4001), os.urandom(4002), os.urandom(4003))
 2387      p.a.write(p.path(rel + ".png"), b"\x89PNG a's thumbnail")
 2388      rc, _ = run_rc(p.a, APPLY.format(unit=shlex.quote(rel), side="left"))
 2389      store = p.saves_remote.rstrip("/") + "-discarded"
 2390      # The reader, on b: the store listed and every record read as one line;
 2391      # nothing local consulted.
 2392      reader = ("R=$(" + ACTIVE_COMMAND + "); S=" + shlex.quote(store) + "; "
 2393                "rclone lsf -R --files-only \"${R}${S}\" 2>/dev/null | while IFS= read -r r; do "
 2394                "case \"$r\" in */record.json|record.json) rclone cat \"${R}${S}/${r}\" | jq -c . ;; "
 2395                "*) echo \"MEMBER $r\" ;; esac; done")
 2396      out = p.b.run(reader, check=False)
 2397      records, members = [], []
 2398      for line in out.splitlines():
 2399          if line.startswith("MEMBER "):
 2400              members.append(line[7:])
 2401              continue
 2402          try:
 2403              records.append(json.loads(line))
 2404          except ValueError:
 2405              pass
 2406      f += not check(bool(records), "b read a decision record from the store",
 2407                     f"NO RECORD IN THE STORE at {epath(store)} (apply exit {rc}) (A5)")
 2408      if records:
 2409          r = sorted(records, key=lambda r: r.get("decided_at", ""), reverse=True)[0]
 2410          want = {"decided_at": r.get("decided_at"),
 2411                  "producer": (r.get("loser") or {}).get("producer") or r.get("producer"),
 2412                  "winner side": (r.get("winner") or {}).get("side")}
 2413          f += not check(all(want.values()), "the newest record names when, the producing device and the winning side",
 2414                         f"the record lacks {[k for k, v in want.items() if not v]}")
 2415          f += not check(any(m.endswith(".png") for m in members), "the loser's thumbnail travelled with it",
 2416                         "no thumbnail beside the record")
 2417      return f
 2418  
 2419  
 2420  def fx_retention(p):
 2421      """The retention ordering (#22 R9): the loser and its record are verified
 2422      in the cloud before the winner replaces anything. Killed between the two,
 2423      the loser is in the store, the head is unchanged, the device's copy is
 2424      still its own."""
 2425      f = 0
 2426      rel = "saves/Ordered.srm"
 2427      v = {"H0": os.urandom(65536), "HA": os.urandom(65537), "HB": os.urandom(65538)}
 2428      p.both_changed(rel, v["H0"], v["HA"], v["HB"])
 2429      store = epath(p.saves_remote.rstrip("/") + "-discarded")
 2430      # KEEP LEFT: the cloud's HB wins; a's HA is the loser, pushed to the store
 2431      # first. At 8 KiB/s a 64 KiB transfer takes eight seconds, so the record
 2432      # is on the remote well before the winner's replacement completes.
 2433      p.a.run("rm -f /tmp/qa-apply.out; (RCLONE_BWLIMIT=8k setsid " + APPLY.format(unit=shlex.quote(rel), side="left")
 2434              + " >/tmp/qa-apply.out 2>&1 &)")
 2435      seen = False
 2436      for _ in range(160):
 2437          time.sleep(0.25)
 2438          if any(r.endswith("record.json") for r in backend_files(store)):
 2439              seen = True
 2440              break
 2441          if not p.a.run("pgrep -x cloud_reconcile >/dev/null && echo running", check=False).strip():
 2442              break
 2443      p.a.run("pkill -9 -x rclone; pkill -9 -x cloud_reconcile; true", check=False)
 2444      tail = p.a.run("tail -c 120 /tmp/qa-apply.out 2>/dev/null || true", check=False).strip()
 2445      f += not check(seen, "the loser's record appeared in the store (the kill point)",
 2446                     f"no record.json ever appeared under {store} (apply said: {tail!r})")
 2447      if seen:
 2448          stored = [sha(backend_bytes(f"{store}/{r}") or b"") for r in backend_files(store) if not r.endswith("record.json")]
 2449          f += not check(sha(v["HA"]) in stored, "the loser's bytes are in the store, hash-equal",
 2450                         f"the store holds {[name_of(x, v) for x in stored]}, not HA")
 2451      f += not check(p.cloud_sha(rel) == sha(v["HB"]), "the head is unchanged",
 2452                     f"the head became {name_of(p.cloud_sha(rel), v)}")
 2453      f += not check(p.a.sha(p.path(rel)) == sha(v["HA"]), "the device's copy was not replaced before the loser was verified",
 2454                     f"the device's copy became {name_of(p.a.sha(p.path(rel)), v)}")
 2455      return f
 2456  
 2457  
 2458  PAIR_FIXTURES = [
 2459      ("A1", "both changed after a first pass: every writer, this device's copy newer and older", fx_a1),
 2460      ("A2", "a failed push retried; an equal-size, equal-mtime change after a first pass", fx_a2),
 2461      ("A3", "CHANGE CLOUD FOLDER to a folder holding different saves", fx_a3),
 2462      ("A8", "a torn N64 pair: interrupted after one member, held, then cleared", fx_a8),
 2463      ("A9", "delete and renumber; a retired hash put back; rm; an unmounted, empty, or empty-cloud root", fx_a9),
 2464      ("A11", "a cloned device id refuses to publish", fx_a11),
 2465      ("A12", "a legacy RESTOREPATH unlike BACKUPPATH: migrated, warned, nothing touched", fx_a12),
 2466      ("A14", "the manifest step: under savestates/.rocknix/, sha256, remote_hash per backend, one tier", fx_a14),
 2467      ("A5", "the discarded-saves reader, from the second device", fx_a5),
 2468      ("RETENTION", "the retention ordering: killed after the loser is stored, before the winner replaces", fx_retention),
 2469  ]
 2470  
 2471  
 2472  def run_pair(a, b, root, remote, args, settings):
 2473      failures = 0
 2474      only = {k.strip().upper() for k in args.only.split(",")} if args.only else None
 2475      p = Pair(a, b, root, settings)
 2476      # The cache directory holds each device's stamps and selections; the
 2477      # fixtures wipe it between runs, so it is carried across and put back.
 2478      had = {d: snapshot_cache(d) for d in (a, b)}
 2479      try:
 2480          for key, title, fn in PAIR_FIXTURES:
 2481              if only and key not in only:
 2482                  continue
 2483              step(f"{key} -- {title}")
 2484              try:
 2485                  failures += fn(p)
 2486              except Fail as e:
 2487                  failures += 1
 2488                  print(f"    FAIL  {e}")
 2489              for which, d in (("a", a), ("b", b)):
 2490                  failures += litter_scan(d, settings, remote, label=f"{key} on {which}: ")
 2491          if not only or "CONTRACT" in only:
 2492              for kind in args.transport.split(","):
 2493                  failures += run_contract(p, kind.strip(), args)
 2494      finally:
 2495          p.reset()
 2496          for d in (a, b):
 2497              restore_cache(d, had[d])
 2498      return failures
 2499  
 2500  
 2501  # ===========================================================================
 2502  # #86: where the device's identity comes from -- one device, and the cloud
 2503  # ===========================================================================
 2504  #
 2505  # The single-device suite proves what a device does with its id; this proves
 2506  # where the id comes from. Both handhelds printed the same hash, ee5013fc56,
 2507  # because every kernel that builds in the IPv6 sit tunnel has a sit0 that
 2508  # sorts before wlan0, `ethtool -P sit0` says "not set", and the old
 2509  # permanent_address accepted the string "notset" as a seed. The VM's kernel
 2510  # has sit as a module and its eth0 sorts first, so it never hit the trap by
 2511  # accident; here sit is loaded and the functions of the staged script are run
 2512  # with the interface list narrowed to sit0 -- by overriding usable_interfaces
 2513  # in the harness's own shell after sourcing the script, never through a hook
 2514  # in the product. A macvlan on eth0 stands in for an interface the name list
 2515  # does not know: it is ARPHRD_ETHER with no bus device behind it, so only the
 2516  # sysfs tests can refuse it. The restore half needs the QA endpoint, which is
 2517  # why this is its own registry and not a capture fixture.
 2518  
 2519  # md5("notset|unknown")[:10]: the hash every affected device carried.
 2520  POISONED = hashlib.md5(b"notset|unknown").hexdigest()[:10]
 2521  assert POISONED == "ee5013fc56"
 2522  
 2523  A15_DRIVER = "/tmp/qa-a15-fn"
 2524  A15_HOST = "A15HOST"
 2525  A15_PLANT = "/tmp/qa-a15-plant"
 2526  A15_ASIDE = "/tmp/qa-a15-aside"      # the device's own manifest working copies, for the run
 2527  A15_MACVLAN = "qa0mv"                # type 1, no device link: only the sysfs tests refuse it
 2528  
 2529  
 2530  def fx_a15(dev, root, remote, settings):
 2531      """A15 (#86): the seed is a MAC or nothing.
 2532  
 2533      (a) With sit0 present, the old pipeline yields "notset" for it (the trap
 2534          is real on this kernel); permanent_address yields nothing for sit0
 2535          and a MAC for eth0; the product's own interface list omits sit0.
 2536          A macvlan on eth0 is type 1 with no device link and matches no name
 2537          pattern, so only the sysfs tests can refuse it: the list omits it
 2538          too, and permanent_address reaches eth0 past it.
 2539      (b) A planted <hostname>-ee5013fc56 -- the RG35XX SP's shape -- heals on
 2540          one run to <label>-<md5(MAC|unknown)[:10]>, which is the hash this
 2541          guest already had, so the recipe is unchanged; the old id is kept in
 2542          .previous, the change is in the cloud-sync log and the journal (both
 2543          marked before the run, so only this run's lines count), and
 2544          --previous lists the recorded id, then <label>-ee5013fc56, then
 2545          <hostname>-ee5013fc56 for a hostname unlike the label. cloud_capture
 2546          --full then carries manifest-<old id>.json to the new name, once.
 2547      (c) An archive planted under the old folder is found by cloud_restore
 2548          through the --previous tier, and the log names the folder and why;
 2549          an archive in the device's own folder wins over it. With the upload
 2550          marker saying the local archive was already sent -- as an old build
 2551          left it after uploading to the old folder -- a backup still lands in
 2552          the healed folder, the marker then names that folder, and the run
 2553          after has nothing to send; the old folder is neither written to nor
 2554          trimmed.
 2555      (d) A second run returns the healed id and rewrites nothing -- mtimes
 2556          moved back first, so a same-content rewrite would show; a healthy id
 2557          that does not match this hardware is returned unchanged.
 2558      (e) With no usable adapter the poisoned id is returned unchanged and
 2559          nothing is written.
 2560      (f) Without sit0 the two guessed names leave --previous: a device that
 2561          never had one could not have written under the constant."""
 2562      f = 0
 2563      tool = dev.run("command -v cloud_device_id 2>/dev/null || true").strip()
 2564      if not tool:
 2565          raise Fail("cloud_device_id does not resolve on the device")
 2566      print(f"    under test: {tool}")
 2567  
 2568      # What the fixture disturbs, captured before anything is written.
 2569      saved_id = dev.run(f"cat {ID_FILE} 2>/dev/null || true")
 2570      had_prev = dev.run(f"[ -e {ID_FILE}.previous ] && echo yes || echo no").strip() == "yes"
 2571      saved_prev = dev.run(f"cat {ID_FILE}.previous 2>/dev/null || true")
 2572      had_sit = dev.run("[ -d /sys/class/net/sit0 ] && echo yes || echo no").strip() == "yes"
 2573      hostname = dev.run("hostname").strip()
 2574      opt_line = dev.run(f"grep -m1 '^BACKUPFILE_RESTORE_OPTION=' {CONF} 2>/dev/null || true").strip()
 2575      marker = f"{CACHE}/settings-backup.uploaded"
 2576      had_marker = dev.run(f"[ -e {marker} ] && echo yes || echo no").strip() == "yes"
 2577      saved_marker = dev.run(f"cat {marker} 2>/dev/null || true")
 2578      # What cloud_capture --full leaves in the cache besides the manifest: its
 2579      # stamp and stage directory. Removed afterwards only if this run made them.
 2580      capture_litter = [x for x in (f"{CACHE}/last-capture", f"{CACHE}/stage")
 2581                        if dev.run(f"[ -e {x} ] && echo yes || echo no").strip() == "no"]
 2582      # The device's manifest working copies, whatever their names: (b) plants
 2583      # one under the poisoned id and expects it under the healed one, and a
 2584      # real one under either name would be mistaken for the fixture's.
 2585      dev.run(f"rm -rf {A15_ASIDE}; mkdir -p {A15_ASIDE}; "
 2586              f"for m in {CACHE}/manifest-*.json; do [ -e \"$m\" ] && mv \"$m\" {A15_ASIDE}/; done; true", check=False)
 2587      settings_remote = settings.get("SETTINGS_REMOTE") or settings.get("SYNCPATH_BACKUP") or ""
 2588      if not settings_remote:
 2589          raise Fail("no SETTINGS_REMOTE in the harness's settings; cannot plant a folder")
 2590      base = f"{remote}:{settings_remote}"
 2591      broot = f"{root}/backup"
 2592      a15_save = f"{root}/saves/qa-a15.srm"
 2593      folders = []
 2594      mv_made = False
 2595  
 2596      # One function of the staged script, in a shell that has sourced every
 2597      # definition but the final dispatch line. A15_IFACES, when set, replaces
 2598      # usable_interfaces in that shell -- the narrowing lives here.
 2599      driver = """#!/bin/bash
 2600  tool="$1"; fn="$2"; shift 2
 2601  eval "$(sed '/^main "\\$@"$/d' "${tool}")"
 2602  if [ -n "${A15_IFACES}" ]; then
 2603      usable_interfaces() { tr ' ' '\\n' <<< "${A15_IFACES}"; }
 2604  fi
 2605  "${fn}" "$@"
 2606  """
 2607      dev.write(A15_DRIVER, driver.encode())
 2608      dev.run(f"chmod +x {A15_DRIVER}")
 2609  
 2610      def fn(name, ifaces=None):
 2611          env = f"A15_IFACES={shlex.quote(ifaces)}" if ifaces is not None else ""
 2612          return run_rc(dev, f"{A15_DRIVER} {shlex.quote(tool)} {name}", env=env)
 2613  
 2614      def id_file():
 2615          return dev.run(f"cat {ID_FILE} 2>/dev/null || true").strip()
 2616  
 2617      def prev_file():
 2618          return dev.run(f"cat {ID_FILE}.previous 2>/dev/null || true").split()
 2619  
 2620      def mtime(path):
 2621          # Nanoseconds. %Y is whole seconds, and a run that finishes in the
 2622          # same second as the plant would hide a rewrite behind it.
 2623          return dev.run(f"stat -c '%y' {shlex.quote(path)} 2>/dev/null || true", check=False).strip()
 2624  
 2625      def journal_mark():
 2626          # Line count, as log_mark does for the file: every earlier A15 run
 2627          # left an identical "healed" line in the journal, so a tail of the
 2628          # journal matched with or without this run writing one.
 2629          return int(dev.run("journalctl -t cloud_device_id -o cat --no-pager 2>/dev/null | wc -l",
 2630                             check=False).strip() or 0)
 2631  
 2632      def journal_since(mark):
 2633          return dev.run(f"journalctl -t cloud_device_id -o cat --no-pager 2>/dev/null | tail -n +{mark + 1}",
 2634                         check=False)
 2635  
 2636      def plant(folder, name, body):
 2637          dev.write(f"{A15_PLANT}/{name}", body)
 2638          dev.run(f"rclone copyto {shlex.quote(f'{A15_PLANT}/{name}')} {shlex.quote(f'{folder}/{name}')}")
 2639          if folder not in folders:
 2640              folders.append(folder)
 2641  
 2642      def listing(folder):
 2643          return dev.run(f"rclone lsf --files-only {shlex.quote(folder + '/')} 2>/dev/null || true", check=False).split()
 2644  
 2645      try:
 2646          # --- (a) ---------------------------------------------------------------
 2647          print("    -- (a) the guard: sit0 yields nothing, eth0 yields a MAC")
 2648          if not had_sit:
 2649              dev.run("modprobe sit 2>/dev/null || true", check=False)
 2650          sit_now = dev.run("[ -d /sys/class/net/sit0 ] && echo yes || echo no").strip() == "yes"
 2651          f += not check(sit_now, "sit0 is present (modprobe sit)",
 2652                         "sit0 could not be created; the trap cannot be reproduced on this guest")
 2653          raw = dev.run("ethtool -P sit0 2>/dev/null | sed 's/.*: //' | tr -d ' \\r\\n'").strip()
 2654          f += not check(raw == "notset",
 2655                         f"the old pipeline turns `ethtool -P sit0` into {raw!r} -- the string both handhelds hashed",
 2656                         f"`ethtool -P sit0` became {raw!r}, not 'notset'; this kernel does not reproduce the trap")
 2657          stype = dev.run("cat /sys/class/net/sit0/type 2>/dev/null; [ -e /sys/class/net/sit0/device ] && echo device || echo no-device").split()
 2658          etype = dev.run("cat /sys/class/net/eth0/type 2>/dev/null; [ -e /sys/class/net/eth0/device ] && echo device || echo no-device").split()
 2659          print(f"          sit0: type {stype[0] if stype else '?'}, {stype[1] if len(stype) > 1 else '?'}; "
 2660                f"eth0: type {etype[0] if etype else '?'}, {etype[1] if len(etype) > 1 else '?'}")
 2661          rc, out = fn("permanent_address", "sit0")
 2662          f += not check(rc != 0 and not out.strip(),
 2663                         f"permanent_address yields nothing for sit0 (exit {rc})",
 2664                         f"permanent_address ACCEPTED sit0: exit {rc}, {out.strip()!r}")
 2665          rc, out = fn("usable_interfaces")
 2666          listed = out.split()
 2667          f += not check("eth0" in listed and "sit0" not in listed and "lo" not in listed,
 2668                         f"the script's own usable_interfaces lists {listed} with sit0 present",
 2669                         f"usable_interfaces listed {listed}")
 2670          mac = dev.run("ethtool -P eth0 2>/dev/null | sed 's/.*: //' | tr -d ' \\r\\n'").strip()
 2671          rc, out = fn("permanent_address", "eth0")
 2672          f += not check(rc == 0 and out.strip() == mac
 2673                         and re.fullmatch(r"([0-9a-f]{2}:){5}[0-9a-f]{2}", mac, re.I) is not None,
 2674                         f"permanent_address yields eth0's permanent address, {mac}",
 2675                         f"permanent_address gave {out.strip()!r} (exit {rc}) for eth0, whose address is {mac!r}")
 2676          if not mac:
 2677              raise Fail("eth0 has no permanent address; the rest of the fixture cannot run")
 2678          expected_hash = hashlib.md5(f"{mac}|unknown".encode()).hexdigest()[:10]
 2679          rc, out = fn("poisoned_hash")
 2680          f += not check(out.strip() == POISONED,
 2681                         f"the script derives the poisoned constant as {out.strip()}",
 2682                         f"the script's poisoned_hash is {out.strip()!r}, not {POISONED}")
 2683          # The sysfs tests on their own. sit0 is refused by its name as well,
 2684          # so a script with the two tests deleted still passed the checks
 2685          # above. A macvlan matches no name pattern and is ARPHRD_ETHER with
 2686          # no bus device behind it -- the only thing that can refuse it is
 2687          # the device-link test; `ethtool -P` on it says "not set", which is
 2688          # the trap's own string.
 2689          dev.run(f"ip link del {A15_MACVLAN} 2>/dev/null || true", check=False)
 2690          rc_mv, out_mv = run_rc(dev, f"ip link add {A15_MACVLAN} link eth0 type macvlan")
 2691          mv_made = rc_mv == 0
 2692          if mv_made:
 2693              mtype = dev.run(f"cat /sys/class/net/{A15_MACVLAN}/type 2>/dev/null; "
 2694                              f"[ -e /sys/class/net/{A15_MACVLAN}/device ] && echo device || echo no-device").split()
 2695              f += not check(mtype[:2] == ["1", "no-device"],
 2696                             f"{A15_MACVLAN} (a macvlan on eth0) is type 1 with no device link: no name pattern catches it, only the sysfs tests can",
 2697                             f"{A15_MACVLAN} is {mtype}; it does not isolate the sysfs tests")
 2698              rc, out = fn("usable_interfaces")
 2699              listed = out.split()
 2700              f += not check("eth0" in listed and A15_MACVLAN not in listed,
 2701                             f"usable_interfaces omits {A15_MACVLAN} and keeps eth0: {listed}",
 2702                             f"usable_interfaces listed {listed}: the device-link test did not refuse {A15_MACVLAN}")
 2703              rc, out = fn("permanent_address", f"{A15_MACVLAN} eth0")
 2704              f += not check(rc == 0 and out.strip() == mac,
 2705                             f"with {A15_MACVLAN} sorting first, permanent_address still yields eth0's address (valid_mac refuses its 'not set')",
 2706                             f"permanent_address gave {out.strip()!r} (exit {rc}) with the list {A15_MACVLAN} eth0")
 2707          else:
 2708              f += not check(False, "",
 2709                             f"could not create a macvlan {A15_MACVLAN} on eth0 (exit {rc_mv}: {out_mv.strip()[-80:]}); the sysfs tests are unproven")
 2710  
 2711          # --- (b) ---------------------------------------------------------------
 2712          print("    -- (b) a poisoned stored id heals once")
 2713          label = dev.run("cloud_device_id --label").strip()
 2714          if not label:
 2715              raise Fail("cloud_device_id --label printed nothing")
 2716          # The hostname shape: ROCKNIX-ee5013fc56 on the RG35XX SP, whose id
 2717          # predates the label. The label shape (the RG SP's) is then the
 2718          # guessed line of --previous, covered on its own below.
 2719          poisoned = f"{hostname}-{POISONED}"
 2720          label_p = f"{label}-{POISONED}"
 2721          expected = f"{label}-{expected_hash}"
 2722          if hostname == label:
 2723              print(f"          (hostname and label are both {label}: the two shapes of the constant collapse here)")
 2724          dev.run(f"printf '%s\\n' {shlex.quote(poisoned)} > {ID_FILE}; rm -f {ID_FILE}.previous")
 2725          mark = log_mark(dev)
 2726          jmark = journal_mark()
 2727          rc, out = run_rc(dev, "cloud_device_id")
 2728          new_id = out.strip()
 2729          f += not check(rc == 0 and new_id == expected,
 2730                         f"{poisoned} healed to {new_id}",
 2731                         f"cloud_device_id printed {new_id!r} (exit {rc}); expected {expected}")
 2732          f += not check(id_file() == expected, "the id file holds the healed id",
 2733                         f"the id file holds {id_file()!r}")
 2734          f += not check(prev_file() == [poisoned],
 2735                         f"the .previous file holds the old id once",
 2736                         f".previous holds {prev_file()}")
 2737          # The hash, not the whole id: the guest's stored id was written by the
 2738          # image's own cloud_device_id, whose label rule may be older than the
 2739          # staged script's (GENERICX64 from the hostname against GENERIC-X64
 2740          # from HW_DEVICE, 2026-09-08). The recipe under test is the hash.
 2741          before = saved_id.strip()
 2742          before_hash = before.rsplit("-", 1)[-1] if before else ""
 2743          if before_hash and before_hash != POISONED:
 2744              f += not check(expected_hash == before_hash,
 2745                             f"the healed hash {expected_hash} is the one this guest generated before the change ({before}): the recipe is unchanged",
 2746                             f"the healed hash {expected_hash} differs from the guest's own {before}: THE RECIPE CHANGED")
 2747              if before != new_id:
 2748                  print(f"          (label {before.rsplit('-', 1)[0]} -> {label}: the label rule, not the hash)")
 2749          else:
 2750              print(f"    SKIP  recipe check - the guest's own id ({before or 'none'}) is not a healthy one to compare with")
 2751          legacy = dev.run("cloud_device_id --legacy").strip()
 2752          f += not check(legacy == f"{hostname}-{expected_hash}",
 2753                         f"--legacy is {legacy}: the hostname and the same hash",
 2754                         f"--legacy is {legacy!r}; expected {hostname}-{expected_hash}")
 2755          tail = log_since(dev, mark)
 2756          f += not check(poisoned in tail and expected in tail and "[cloud_device_id]" in tail,
 2757                         "the cloud-sync log records old -> new under the cloud_device_id tag",
 2758                         f"the cloud-sync log does not: {tail.strip()[-200:]!r}")
 2759          journal = journal_since(jmark)
 2760          f += not check(expected in journal and poisoned in journal,
 2761                         "and so does the journal (logger -t cloud_device_id), in a line this run wrote",
 2762                         f"the journal gained nothing saying so: {journal.strip()[-200:]!r}")
 2763          rc, out = run_rc(dev, "cloud_device_id --previous")
 2764          lines = out.split()
 2765          want = [poisoned] if hostname == label else [poisoned, label_p]
 2766          f += not check(lines == want,
 2767                         f"--previous lists {lines}: the recorded id, then <label>-{POISONED}"
 2768                         + (" (which is the recorded one here)" if hostname == label else f"; <hostname>-{POISONED} is the recorded one"),
 2769                         f"--previous listed {lines}; expected {want}")
 2770          dev.run(f"hostname {A15_HOST}")
 2771          rc, out = run_rc(dev, "cloud_device_id --previous")
 2772          dev.run(f"hostname {shlex.quote(hostname)}")
 2773          lines2 = out.split()
 2774          want2 = want + [f"{A15_HOST}-{POISONED}"]
 2775          f += not check(lines2 == want2,
 2776                         f"with the hostname {A15_HOST}, --previous adds {A15_HOST}-{POISONED} last",
 2777                         f"--previous listed {lines2}; expected {want2}")
 2778  
 2779          # The working copy follows the id. The boot pass is `cloud_capture
 2780          # --full`, whose first act is to call cloud_device_id -- so on the
 2781          # handhelds this is where the heal happens and where the manifest
 2782          # written under the old id would be orphaned.
 2783          print("    -- (b) cloud_capture --full carries the working copy to the healed id")
 2784          man_old = f"{CACHE}/manifest-{poisoned}.json"
 2785          man_new = f"{CACHE}/manifest-{expected}.json"
 2786          dev.write(man_old, b'{"schema":1,"entries":{},"units":{},"retired":[]}\n')
 2787          dev.write(a15_save, b"a15")   # --full refuses an empty root
 2788          mark = log_mark(dev)
 2789          rc, out = run_rc(dev, "cloud_capture --full")
 2790          tail = log_since(dev, mark)
 2791          old_there = dev.run(f"[ -e {shlex.quote(man_old)} ] && echo yes || echo no").strip() == "yes"
 2792          new_ok = dev.run(f"jq -e '.entries' {shlex.quote(man_new)} >/dev/null 2>&1 && echo yes || echo no",
 2793                           check=False).strip() == "yes"
 2794          f += not check(not old_there and new_ok and "adopted" in tail and poisoned in tail and expected in tail,
 2795                         f"cloud_capture --full adopted manifest-{poisoned}.json as manifest-{expected}.json and said so (exit {rc})",
 2796                         f"exit {rc}; old manifest {'still there' if old_there else 'gone'}, new one "
 2797                         f"{'parses' if new_ok else 'absent or unparsable'}; log: {tail.strip()[-300:]!r}")
 2798          mark = log_mark(dev)
 2799          rc, out = run_rc(dev, "cloud_capture --full")
 2800          tail = log_since(dev, mark)
 2801          f += not check("adopted" not in tail and "could not adopt" not in tail,
 2802                         "a second --full adopts nothing more (the current name exists)",
 2803                         f"the second --full logged: {tail.strip()[-300:]!r}")
 2804  
 2805          # --- (c) ---------------------------------------------------------------
 2806          print("    -- (c) the old folder stays restorable; backup and retention never touch it")
 2807          osn = os_name(dev)
 2808          old_folder = f"{base}/{poisoned}"
 2809          new_folder = f"{base}/{expected}"
 2810          old_archive = f"2026_01_01-000000-{osn}_SETTINGS.tar.gz"   # the pre-label shape the RG35XX SP's folder holds
 2811          backend("reset")
 2812          dev.run(f"rm -rf {A15_PLANT}; mkdir -p {A15_PLANT} {shlex.quote(broot)}")
 2813          plant(old_folder, old_archive, b"written under the shared id")
 2814          dev.run(f"grep -q '^BACKUPFILE_RESTORE_OPTION=' {CONF} "
 2815                  f"&& sed -i 's|^BACKUPFILE_RESTORE_OPTION=.*|BACKUPFILE_RESTORE_OPTION=\"yes\"|' {CONF} "
 2816                  f"|| echo 'BACKUPFILE_RESTORE_OPTION=\"yes\"' >> {CONF}")
 2817          dev.run(f"rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip", check=False)
 2818          mark = log_mark(dev)
 2819          rc, out = run_rc(dev, "cloud_restore --yes --system-only")
 2820          local = dev.run(f"ls -1 {shlex.quote(broot)}/ 2>/dev/null || true", check=False).split()
 2821          tail = log_since(dev, mark)
 2822          f += not check(old_archive in local,
 2823                         f"cloud_restore found the archive under {poisoned} (the hostname shape) through the --previous tier (exit {rc})",
 2824                         f"restore brought back {local or 'nothing'} (exit {rc})")
 2825          f += not check(poisoned in tail and "shared constant" in tail,
 2826                         "and the log names the folder it took and why",
 2827                         f"the log did not name the folder: {tail.strip()[-300:]!r}")
 2828          own_archive = f"2026_01_02-000000-{label}-{osn}_SETTINGS.tar.gz"
 2829          plant(new_folder, own_archive, b"written under the healed id")
 2830          dev.run(f"rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip", check=False)
 2831          mark = log_mark(dev)
 2832          run_rc(dev, "cloud_restore --yes --system-only")
 2833          local = dev.run(f"ls -1 {shlex.quote(broot)}/ 2>/dev/null || true", check=False).split()
 2834          tail = log_since(dev, mark)
 2835          f += not check(own_archive in local and old_archive not in local,
 2836                         "with an archive in its own folder, restore takes that one before the old folder's",
 2837                         f"restore brought back {local or 'nothing'}")
 2838          f += not check(f"own cloud folder ({expected})" in tail,
 2839                         "and says it restored from the device's own folder",
 2840                         f"the log did not: {tail.strip()[-300:]!r}")
 2841          keep_raw = dev.run(f"grep -m1 '^CLOUD_BACKUP_KEEP=' {CONF} 2>/dev/null | cut -d= -f2 | tr -d '\"' || true").strip()
 2842          keep = int(keep_raw) if keep_raw.isdigit() and 1 <= int(keep_raw) <= 20 else 3
 2843          # More of this device's own labelled archives than retention keeps,
 2844          # in the OLD folder: if retention reached it, some would go.
 2845          old_own = [f"2026_01_{d:02d}-000000-{label}-{osn}_SETTINGS.tar.gz" for d in range(3, 3 + keep + 2)]
 2846          for name in old_own:
 2847              plant(old_folder, name, name.encode())
 2848          old_before = sorted(listing(old_folder))
 2849          upload = f"2026_02_01-000000-{label}-{osn}_SETTINGS.tar.gz"
 2850          dev.run(f"rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip", check=False)
 2851          dev.write(f"{broot}/{upload}", b"this run's archive")
 2852          # The regression: the archive has not changed since it was last sent,
 2853          # and the marker says so -- the bare hash an old build wrote after
 2854          # uploading to the OLD folder. A game-exit backup on the new build
 2855          # runs from exactly this state, and a marker that knew only what was
 2856          # sent answered "nothing to send" and left the healed folder empty.
 2857          # The hash is computed as cloud_backup computes it: md5 of the
 2858          # md5sum listing of the archives at the root of SETTINGS_BACKUPS.
 2859          local_sum = dev.run(f"md5sum {shlex.quote(broot)}/*.tar.gz | md5sum | cut -d' ' -f1").strip()
 2860          dev.run(f"printf '%s\\n' {local_sum} > {marker}")
 2861          mark = log_mark(dev)
 2862          rc, _ = run_rc(dev, "cloud_backup --yes --system-only")
 2863          new_list = listing(new_folder)
 2864          old_after = sorted(listing(old_folder))
 2865          f += not check(rc == 0 and upload in new_list,
 2866                         f"with the marker saying this archive was already sent (an old build's marker, from the old folder), the backup still landed in the healed folder {expected} (exit {rc})",
 2867                         f"the backup did not land in {expected} (exit {rc}): {new_list}; log: {log_since(dev, mark).strip()[-200:]!r}")
 2868          f += not check("device.json" in new_list,
 2869                         "and wrote the healed folder's device.json",
 2870                         f"no device.json in {expected}: {new_list}")
 2871          now_marker = dev.run(f"cat {marker} 2>/dev/null || true").strip()
 2872          f += not check(now_marker == f"{local_sum} {new_folder}",
 2873                         f"the marker now records where as well as what: {now_marker}",
 2874                         f"the marker reads {now_marker!r}; expected {local_sum} {new_folder}")
 2875          mark = log_mark(dev)
 2876          rc, _ = run_rc(dev, "cloud_backup --yes --system-only")
 2877          tail = log_since(dev, mark)
 2878          # The marker's own line, not the transfer banner (which names the
 2879          # folder on every run), and no upload: a marker that never learnt
 2880          # the new shape would send 17 MB on every game exit.
 2881          f += not check(rc == 0 and f"unchanged since the last upload to {new_folder}" in tail and "Uploading" not in tail,
 2882                         "and the run after that has nothing to send, and sends nothing",
 2883                         f"the run after: exit {rc}, log {tail.strip()[-300:]!r}")
 2884          f += not check(upload not in old_after and old_after == old_before
 2885                         and all(n in old_after for n in [old_archive] + old_own),
 2886                         f"nothing was written to or removed from {poisoned}: it still holds its {len(old_before)} archives",
 2887                         f"THE OLD FOLDER CHANGED: before {old_before}, after {old_after}")
 2888  
 2889          # --- (d) ---------------------------------------------------------------
 2890          print("    -- (d) a healthy stored id is left alone")
 2891          touch_offset(dev, ID_FILE, -5)
 2892          touch_offset(dev, f"{ID_FILE}.previous", -5)
 2893          m_id, m_prev = mtime(ID_FILE), mtime(f"{ID_FILE}.previous")
 2894          rc, out = run_rc(dev, "cloud_device_id")
 2895          f += not check(out.strip() == expected and id_file() == expected and prev_file() == [poisoned]
 2896                         and mtime(ID_FILE) == m_id and mtime(f"{ID_FILE}.previous") == m_prev,
 2897                         "a second run returns the healed id and rewrites nothing (the id file and .previous keep their mtimes)",
 2898                         f"second run: printed {out.strip()!r}, file {id_file()!r} (mtime {m_id} -> {mtime(ID_FILE)}), "
 2899                         f".previous {prev_file()} (mtime {m_prev} -> {mtime(f'{ID_FILE}.previous')})")
 2900          healthy = "Some-Other-Handheld-0123456789"
 2901          dev.run(f"printf '%s\\n' {healthy} > {ID_FILE}")
 2902          touch_offset(dev, ID_FILE, -5)
 2903          m_id = mtime(ID_FILE)
 2904          mark = log_mark(dev)
 2905          rc, out = run_rc(dev, "cloud_device_id")
 2906          f += not check(out.strip() == healthy and id_file() == healthy and prev_file() == [poisoned]
 2907                         and mtime(ID_FILE) == m_id and healthy not in log_since(dev, mark),
 2908                         "a healthy id that does not match this hardware is returned unchanged and not rewritten (the module-swap case)",
 2909                         f"printed {out.strip()!r}, file {id_file()!r} (mtime {m_id} -> {mtime(ID_FILE)}), .previous {prev_file()}")
 2910  
 2911          # --- (e) ---------------------------------------------------------------
 2912          print("    -- (e) no adapter, no healing")
 2913          dev.run(f"printf '%s\\n' {shlex.quote(poisoned)} > {ID_FILE}; rm -f {ID_FILE}.previous")
 2914          touch_offset(dev, ID_FILE, -5)
 2915          stamp_before = mtime(ID_FILE)
 2916          mark = log_mark(dev)
 2917          rc, out = fn("main", "sit0")
 2918          stamp_after = mtime(ID_FILE)
 2919          f += not check(rc == 0 and out.strip() == poisoned,
 2920                         f"with the interface list narrowed to sit0 the poisoned id is returned unchanged (exit {rc})",
 2921                         f"printed {out.strip()!r} (exit {rc}); expected {poisoned}")
 2922          untouched = (id_file() == poisoned and not prev_file()
 2923                       and stamp_before == stamp_after
 2924                       and "healed" not in log_since(dev, mark))
 2925          f += not check(untouched, "and nothing was written: the id file keeps its mtime, no .previous, no log line",
 2926                         f"file {id_file()!r} (mtime {stamp_before} -> {stamp_after}), .previous {prev_file()}")
 2927  
 2928          # --- (f) ---------------------------------------------------------------
 2929          print("    -- (f) without sit0 the guessed names are not offered")
 2930          # Under a hostname unlike the recorded id's, so that both guessed
 2931          # names -- <label>-P and <hostname>-P -- would be new lines if the
 2932          # gate let them through; with the real hostname the second collapses
 2933          # into the recorded id and an ungated script passes by dedup.
 2934          dev.run(f"printf '%s\\n' {shlex.quote(poisoned)} > {ID_FILE}.previous")
 2935          rc_rm, out_rm = run_rc(dev, "rmmod sit")
 2936          sit_gone = dev.run("[ -d /sys/class/net/sit0 ] && echo yes || echo no").strip() == "no"
 2937          if sit_gone:
 2938              dev.run(f"hostname {A15_HOST}")
 2939              rc, out = run_rc(dev, "cloud_device_id --previous")
 2940              dev.run(f"hostname {shlex.quote(hostname)}")
 2941              lines = out.split()
 2942              f += not check(lines == [poisoned],
 2943                             f"with no sit0 (hostname {A15_HOST}), --previous lists {lines}: the recorded id only -- a device that never had a sit0 could not have hashed 'notset'",
 2944                             f"--previous listed {lines} with no sit0; expected [{poisoned}]")
 2945              if had_sit:
 2946                  dev.run("modprobe sit 2>/dev/null || true", check=False)
 2947          else:
 2948              f += not check(False, "", f"sit could not be unloaded (exit {rc_rm}: {out_rm.strip()[-80:]}); the sit0 gate is unproven")
 2949      finally:
 2950          # Everything back: the hostname, the identity, sit, the macvlan, the
 2951          # settings-restore option, the upload marker, the manifests, the
 2952          # planted folders, the scratch archives, the driver.
 2953          dev.run(f"hostname {shlex.quote(hostname)}", check=False)
 2954          if saved_id.strip():
 2955              dev.write(ID_FILE, saved_id.encode())
 2956          else:
 2957              dev.run(f"rm -f {ID_FILE}", check=False)
 2958          if had_prev:
 2959              dev.write(f"{ID_FILE}.previous", saved_prev.encode())
 2960          else:
 2961              dev.run(f"rm -f {ID_FILE}.previous", check=False)
 2962          if not had_sit:
 2963              dev.run("rmmod sit 2>/dev/null || true", check=False)
 2964          if mv_made:
 2965              dev.run(f"ip link del {A15_MACVLAN} 2>/dev/null || true", check=False)
 2966          if opt_line:
 2967              dev.run(f"sed -i 's|^BACKUPFILE_RESTORE_OPTION=.*|{opt_line}|' {CONF}", check=False)
 2968          else:
 2969              dev.run(f"sed -i '/^BACKUPFILE_RESTORE_OPTION=/d' {CONF}", check=False)
 2970          if had_marker:
 2971              dev.write(marker, saved_marker.encode())
 2972          else:
 2973              dev.run(f"rm -f {marker}", check=False)
 2974          dev.run(f"rm -f {CACHE}/manifest-*.json; "
 2975                  f"for m in {A15_ASIDE}/manifest-*.json; do [ -e \"$m\" ] && mv \"$m\" {CACHE}/; done; "
 2976                  f"rm -rf {A15_ASIDE} {shlex.quote(a15_save)}; true", check=False)
 2977          for x in capture_litter:
 2978              dev.run(f"rm -rf {shlex.quote(x)}", check=False)
 2979          for folder in folders:
 2980              dev.run(f"rclone purge {shlex.quote(folder)} >/dev/null 2>&1 || true", check=False)
 2981          dev.run(f"rm -rf {A15_PLANT} {A15_DRIVER}; rm -f {shlex.quote(broot)}/*.tar.gz {shlex.quote(broot)}/*.zip",
 2982                  check=False)
 2983          now = id_file()
 2984          sit_after = dev.run("[ -d /sys/class/net/sit0 ] && echo yes || echo no", check=False).strip() == "yes"
 2985          mv_after = dev.run(f"[ -d /sys/class/net/{A15_MACVLAN} ] && echo yes || echo no", check=False).strip() == "yes"
 2986          print(f"    put back: id {now or 'none'}{' (as before)' if now == saved_id.strip() else ' (DIFFERS from ' + (saved_id.strip() or 'none') + ')'}, "
 2987                f".previous {'restored' if had_prev else 'absent'}, marker {'restored' if had_marker else 'absent'}, "
 2988                f"sit0 {'present' if sit_after else 'absent'} (was {'present' if had_sit else 'absent'}), "
 2989                f"{A15_MACVLAN} {'STILL PRESENT' if mv_after else 'gone'}, hostname {dev.run('hostname', check=False).strip()}")
 2990      return f
 2991  
 2992  
 2993  SOLO_FIXTURES = [
 2994      ("A15", "the seed is a MAC or nothing: sit0 and a macvlan are refused, a poisoned id heals once, "
 2995              "the working copy and the next backup follow it, its old folder stays restorable", fx_a15),
 2996  ]
 2997  
 2998  
 2999  def run_solo(dev, root, remote, args, settings, only):
 3000      """The single-device cloud fixtures, on the first (only) device."""
 3001      failures = 0
 3002      for key, title, fn in SOLO_FIXTURES:
 3003          if only and key not in only:
 3004              continue
 3005          step(f"{key} -- {title}")
 3006          try:
 3007              failures += fn(dev, root, remote, settings)
 3008          except Fail as e:
 3009              failures += 1
 3010              print(f"    FAIL  {e}")
 3011          failures += litter_scan(dev, settings, remote, label=f"{key}: ")
 3012      return failures
 3013  
 3014  
 3015  # ===========================================================================
 3016  # #21's producer: cloud_capture, on one device, with no cloud
 3017  # ===========================================================================
 3018  #
 3019  # The capture fixtures drive /usr/bin/cloud_capture the way EmulationStation
 3020  # does at game exit (--system/--rom/--emulator/--core/--started/--exit), the
 3021  # way the save-state manager does (--retire, --rescan) and the way the boot
 3022  # autostart does (--full), and read the working copy it writes at
 3023  # /storage/.cache/cloud_sync/manifest-<device-id>.json. The producer opens no
 3024  # socket and spawns no rclone, so these need neither MinIO nor a second guest:
 3025  # --only CAP1,...,CAP14 prepares the device locally (prepare_local) and the
 3026  # QA endpoint is never asked for anything.
 3027  #
 3028  # The harness copies nothing onto the device. Stage the producer and its two
 3029  # siblings by hand before a run -- they are resolved beside $0, so all three
 3030  # must sit in the same directory:
 3031  #
 3032  #     scp -i /tmp/rocknix-vm-pair/qa-key -P 10022 \
 3033  #         projects/ROCKNIX/packages/network/rclone/sources/{cloud_capture,cloud_device_id,cloud_saves_root} \
 3034  #         root@127.0.0.1:/tmp/qa-bin/ && ssh ... chmod +x /tmp/qa-bin/cloud_*
 3035  #     ./tools/cloud-round-trip --host root@127.0.0.1 --port 10022 --identity /tmp/rocknix-vm-pair/qa-key \
 3036  #         --path-prefix /tmp/qa-bin --only CAP1,CAP2,CAP3,CAP4,CAP5,CAP6,CAP7,CAP8,CAP9,CAP10,CAP11,CAP12,CAP13,CAP14
 3037  #
 3038  # CAP10 (d) also reads autostart/102-cloud-saves: stage it into the same
 3039  # directory to check the repo's copy rather than the image's. CAP11 copies
 3040  # the staged producer beside a cloud_device_id shim of its own.
 3041  #
 3042  # What the harness cannot prove is ES's half -- that the call is made outside
 3043  # the cloudsaves.gameexit gate, on a nonzero exit, with the --core= token of
 3044  # the finished command -- because it cannot drive EmulationStation. Those are
 3045  # the six VM procedures in the #21 design; each fixture's docstring says
 3046  # which half it covers.
 3047  
 3048  ISO_UTC = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
 3049  
 3050  
 3051  def require_capture(dev):
 3052      """The producer must resolve under the PATH prefix. It is staged by hand;
 3053      the harness copies nothing, so its absence is a setup failure, not a
 3054      finding about the script."""
 3055      have = dev.run("command -v cloud_capture 2>/dev/null || true").strip()
 3056      if not have:
 3057          raise Fail("cloud_capture does not resolve on the device (with --path-prefix): stage "
 3058                     "projects/ROCKNIX/packages/network/rclone/sources/cloud_capture into the prefix directory "
 3059                     "beside cloud_device_id and cloud_saves_root, chmod +x -- the harness copies nothing")
 3060      return have
 3061  
 3062  
 3063  def local_reset(dev, root):
 3064      """Empty the saves root and the cache -- manifest, stage, stamps, the
 3065      saves-root record -- so what one fixture leaves cannot pass the next. No
 3066      backend("reset"): there is no cloud in a capture run."""
 3067      dev.run(f"rm -rf {shlex.quote(root)} {CACHE}; mkdir -p {shlex.quote(root)} {CACHE}")
 3068  
 3069  
 3070  def manifest_text(dev):
 3071      """(present, text) of the working copy. Presence is asserted with [ -e ],
 3072      never inferred from an empty stdout (blindspot 31: a helper that reads
 3073      through the wrong path agrees with itself)."""
 3074      out = dev.run(f"f={CACHE}/manifest-$(cloud_device_id 2>/dev/null).json; "
 3075                    "if [ -e \"$f\" ]; then echo PRESENT; cat \"$f\"; else echo ABSENT; fi")
 3076      head, _, rest = out.partition("\n")
 3077      return head.strip() == "PRESENT", rest
 3078  
 3079  
 3080  def manifest_of(dev):
 3081      """The parsed working copy, or None when the file is absent. A file that
 3082      is present but does not parse raises -- the fixture that expects one
 3083      (CAP9 d) reads manifest_text itself."""
 3084      present, text = manifest_text(dev)
 3085      if not present:
 3086          return None
 3087      try:
 3088          return json.loads(text)
 3089      except ValueError as e:
 3090          raise Fail(f"the manifest is present but does not parse: {e}")
 3091  
 3092  
 3093  def manifest_stat(dev):
 3094      """(mtime, inode, sha256) of the working copy, or None when absent. All
 3095      three, because ext4 keeps seconds: a rewrite within the same second is
 3096      invisible by mtime alone (I8 is asserted on all three)."""
 3097      out = dev.run(f"f={CACHE}/manifest-$(cloud_device_id 2>/dev/null).json; "
 3098                    "if [ -e \"$f\" ]; then stat -c '%Y %i' \"$f\"; sha256sum \"$f\" | cut -c1-64; else echo ABSENT; fi")
 3099      fields = out.split()
 3100      if fields == ["ABSENT"]:
 3101          return None
 3102      return int(fields[0]), int(fields[1]), fields[2]
 3103  
 3104  
 3105  def entry(m, rel):
 3106      return ((m or {}).get("entries") or {}).get(rel)
 3107  
 3108  
 3109  def members(m, unit):
 3110      return (((m or {}).get("units") or {}).get(unit) or {}).get("members")
 3111  
 3112  
 3113  def nulls(e, keys):
 3114      """Every key present and null -- absent is not null (§6)."""
 3115      return bool(e) and all(k in e and e[k] is None for k in keys)
 3116  
 3117  
 3118  def capture(dev, root, system, rom, emulator="retroarch", core="mgba", started=0, exit_code=None, env=""):
 3119      """Run the producer the way ES does at exit, every value quoted the way
 3120      shellQuote would. --started 0 by default: the explicit record-everything
 3121      form, since a fixture's planted files predate any real session."""
 3122      cmd = (f"cloud_capture --system {shlex.quote(system)} --rom {shlex.quote(rom)} "
 3123             f"--emulator {shlex.quote(emulator)} --core {shlex.quote(core)} --started {int(started)}")
 3124      if exit_code is not None:
 3125          cmd += f" --exit {int(exit_code)}"
 3126      return run_rc(dev, cmd, env)
 3127  
 3128  
 3129  def plant(dev, root, rel, data):
 3130      """Write one member; hand its bytes back so the caller can hash them."""
 3131      dev.write(f"{root}/{rel}", data)
 3132      return data
 3133  
 3134  
 3135  def plant_unit(dev, root, system, stem, save=None, states=None, auto=None, png=None, romdir=None):
 3136      """Plant a libretro unit's members with random bodies and return
 3137      {relative path: bytes}. `states` maps slot -> size (slot 0 is the bare
 3138      .state); `png` is the thumbnail size beside every state and auto, or None
 3139      for none; `romdir` is where the .srm goes (the ROM's directory, because
 3140      savefiles_in_content_dir is true), defaulting to <system>."""
 3141      romdir = romdir or system
 3142      planted = {}
 3143      if save is not None:
 3144          planted[f"{romdir}/{stem}.srm"] = os.urandom(save)
 3145      for slot, size in sorted((states or {}).items()):
 3146          rel = f"savestates/{system}/{stem}.state{'' if slot == 0 else slot}"
 3147          planted[rel] = b"#RZIPv" + os.urandom(size)
 3148          if png:
 3149              planted[rel + ".png"] = b"\x89PNG" + os.urandom(png)
 3150      if auto is not None:
 3151          rel = f"savestates/{system}/{stem}.state.auto"
 3152          planted[rel] = b"#RZIPv" + os.urandom(auto)
 3153          if png:
 3154              planted[rel + ".png"] = b"\x89PNG" + os.urandom(png)
 3155      for rel, data in planted.items():
 3156          dev.write(f"{root}/{rel}", data)
 3157      return planted
 3158  
 3159  
 3160  def stage_count(dev):
 3161      return int(dev.run(f"ls {CACHE}/stage 2>/dev/null | wc -l").strip() or 0)
 3162  
 3163  
 3164  def stage_sha(dev, digest):
 3165      """sha256sum of the sealed copy named by a hash -- an integrity check,
 3166      not a tautology, because the name is the hash the producer recorded."""
 3167      return dev.sha(f"{CACHE}/stage/{digest}")
 3168  
 3169  
 3170  def iso_mtime(dev, path):
 3171      """A file's mtime rendered the way the producer renders it."""
 3172      return dev.run(f"date -u -d @$(stat -c %Y {shlex.quote(path)}) +%FT%TZ").strip()
 3173  
 3174  
 3175  def last_capture_lines(dev):
 3176      """Every line of the durable stamp as written: one per mode since
 3177      D-CLOUD-070, one in all from a producer before it. Blank lines dropped,
 3178      nothing else touched."""
 3179      out = dev.run(f"cat {CACHE}/last-capture 2>/dev/null || true")
 3180      return [l for l in out.splitlines() if l.strip()]
 3181  
 3182  
 3183  def stamp_mode(line):
 3184      """A stamp line's mode: the third field with any !card marker stripped,
 3185      or None for a line too short to have one."""
 3186      fields = line.split()
 3187      return fields[2].split("!")[0] if len(fields) >= 3 else None
 3188  
 3189  
 3190  def parse_capture_line(line):
 3191      """One stamp line as (epoch, rc, mode, unit, "emu-exit=<N|?>",
 3192      "<emulator>/<core>"), or None for anything else -- a four-field line from
 3193      before the launch's exit and the frozen pair were carried is None too, so
 3194      every check on the trailing fields fails against it. emu-exit is what ES
 3195      passed to --exit: runemu.sh's 0/1, not the emulator's code. The unit may
 3196      contain spaces (a ROM stem); the two trailing fields never do, so the
 3197      parse takes three fields from the front and two from the back."""
 3198      parts = (line or "").strip().rsplit(None, 2)
 3199      if len(parts) != 3 or not parts[1].startswith("emu-exit=") or "/" not in parts[2]:
 3200          return None
 3201      front = parts[0].split(None, 3)
 3202      return (*front, parts[1], parts[2]) if len(front) == 4 else None
 3203  
 3204  
 3205  def last_capture(dev, mode):
 3206      """The stamp's line for one mode, parsed, or None when there is none. The
 3207      file holds one line per mode (D-CLOUD-070, CAP12), so a check on an exit
 3208      capture reads the exit line whatever --full or --retire has run since --
 3209      and a one-line stamp from an older producer is read the same way, as its
 3210      mode's line. Were the file ever to hold two lines of one mode, the later
 3211      one is taken; CAP12 is where that would be a FAIL."""
 3212      found = None
 3213      for line in last_capture_lines(dev):
 3214          if stamp_mode(line) == mode:
 3215              found = line
 3216      return parse_capture_line(found) if found is not None else None
 3217  
 3218  
 3219  def failures_lines(dev):
 3220      return int(dev.run(f"wc -l < {CACHE}/capture-failures 2>/dev/null || echo 0").strip() or 0)
 3221  
 3222  
 3223  class Solo:
 3224      """One device, its scratch saves root and the producer's working copy.
 3225      No cloud: nothing here calls backend() or reads rclone.conf."""
 3226  
 3227      def __init__(self, a, root):
 3228          self.a, self.root = a, root
 3229          self.id = a.run("cloud_device_id 2>/dev/null || true").strip()
 3230          self.manifest = f"{CACHE}/manifest-{self.id}.json"
 3231          self.stage = f"{CACHE}/stage"
 3232  
 3233      def path(self, rel):
 3234          return f"{self.root}/{rel}"
 3235  
 3236      def reset(self):
 3237          """Every fixture starts here: the producer resolves, and the root and
 3238          cache are empty."""
 3239          require_capture(self.a)
 3240          local_reset(self.a, self.root)
 3241  
 3242  
 3243  def fx_cap1(p):
 3244      """CAP1: capture on every exit -- with the transfer lock held by another
 3245      process, no route, an rclone shim counting spawns, and exit 1 from the
 3246      emulator. The unit is recorded; each seal is the planted bytes; the
 3247      thumbnails are declared members with no entry; the .state.auto.bak decoy
 3248      is nothing; nothing is written into the saves tree; stdout stays empty
 3249      (ES reads that pipe); no rclone was spawned; the durable stamp names the
 3250      unit.
 3251  
 3252      The toggle-off half is ES's: FileData.cpp calls the producer outside the
 3253      cloudsaves.gameexit gate. VM procedure (1) of the #21 design proves it
 3254      (cloudsaves.gameexit=0, launch and exit a game, read the manifest); the
 3255      harness cannot drive EmulationStation."""
 3256      f = 0
 3257      a, root = p.a, p.root
 3258      p.reset()
 3259      unit = "gba:Game"
 3260      srm, s1, auto = "gba/Game.srm", "savestates/gba/Game.state1", "savestates/gba/Game.state.auto"
 3261      planted = plant_unit(a, root, "gba", "Game", save=604, states={1: 40 * 1024}, auto=30 * 1024, png=3 * 1024)
 3262      plant(a, root, auto + ".bak", b"ES's launch-time swap (SaveState.cpp), never a member")
 3263      a.run("touch /tmp/qa-mark; sleep 1")
 3264      # One guest command: the lock held on fd 9 (run_steps' recipe), the ip
 3265      # shim that reports no route, the rclone shim that counts spawns.
 3266      out = a.run(
 3267          "mkdir -p /tmp/noroute /tmp/qa-shim; printf '#!/bin/sh\\nexit 0\\n' > /tmp/noroute/ip; chmod +x /tmp/noroute/ip; "
 3268          "printf '#!/bin/sh\\necho \"$@\" >> /tmp/qa-spawns\\nexec /usr/bin/rclone \"$@\"\\n' > /tmp/qa-shim/rclone; "
 3269          "chmod +x /tmp/qa-shim/rclone; rm -f /tmp/qa-spawns /tmp/qa-cap1.out /tmp/qa-cap1.err; "
 3270          "exec 9>/var/run/cloud_sync.lock; flock -n 9 || echo HOLDER-FAILED; "
 3271          f"PATH=/tmp/noroute:/tmp/qa-shim:$PATH cloud_capture --system gba --rom {shlex.quote(p.path('gba/Game.gba'))} "
 3272          "--emulator retroarch --core mgba --started 0 --exit 1 >/tmp/qa-cap1.out 2>/tmp/qa-cap1.err; echo rc=$?; "
 3273          "exec 9>&-", check=False)
 3274      rc = next((int(w[3:]) for w in out.split() if w.startswith("rc=") and w[3:].lstrip("-").isdigit()), -1)
 3275      f += not check("HOLDER-FAILED" not in out, "the test held the transfer lock itself (the setup)",
 3276                     "could not take the lock to set up the test")
 3277      f += not check(rc == 0, "capture exited 0 under a held lock, with no route, after exit 1 from the emulator",
 3278                     f"capture exited {rc} (stderr: {a.run('tail -c 200 /tmp/qa-cap1.err 2>/dev/null || true').strip()!r})")
 3279      m = manifest_of(a)
 3280      f += not check(m is not None, "the manifest exists and parses", "no manifest was written")
 3281      if m is None:
 3282          a.run("rm -rf /tmp/noroute /tmp/qa-shim /tmp/qa-spawns /tmp/qa-mark", check=False)
 3283          return f
 3284      for rel in (srm, s1, auto):
 3285          e = entry(m, rel) or {}
 3286          want = sha(planted[rel])
 3287          f += not check(e.get("sha256") == want == a.sha(p.path(rel)) and e.get("size") == len(planted[rel]),
 3288                         f"{rel}: sha256 and size are the planted bytes'",
 3289                         f"{rel}: {'no entry' if not e else 'sha256/size differ from the planted bytes'}")
 3290      three = [entry(m, r) or {} for r in (srm, s1, auto)]
 3291      f += not check([e.get("kind") for e in three] == ["save", "state", "auto"],
 3292                     "kinds save/state/auto", f"kinds {[e.get('kind') for e in three]}")
 3293      f += not check([e.get("slot") for e in three] == [None, 1, None],
 3294                     "slots null/1/null", f"slots {[e.get('slot') for e in three]}")
 3295      f += not check([e.get("screenshot") for e in three] == [None, s1 + ".png", auto + ".png"],
 3296                     "the state and the auto name their .png as screenshot; the save has none",
 3297                     f"screenshots {[e.get('screenshot') for e in three]}")
 3298      f += not check(all(e.get("unit") == unit for e in three), f"unit {unit!r} on all three",
 3299                     f"units {[e.get('unit') for e in three]}")
 3300      prov = {k: three[1].get(k) for k in ("emulator", "core", "system", "rom")}
 3301      f += not check(prov == {"emulator": "retroarch", "core": "mgba", "system": "gba", "rom": "Game.gba"},
 3302                     "emulator/core/system/rom are the arguments, verbatim", f"provenance {prov}")
 3303      f += not check(all(nulls(e, ("producer", "pub", "published_at", "replaces", "remote_hash")) for e in three),
 3304                     "producer/pub/published_at/replaces/remote_hash are present and null",
 3305                     "a first version carries a non-null (or absent) producer/pub/published_at/replaces/remote_hash")
 3306      f += not check(all(isinstance(e.get("clock_synced"), bool) for e in three),
 3307                     "clock_synced is a bool", f"clock_synced {[e.get('clock_synced') for e in three]!r}")
 3308      f += not check(members(m, unit) == sorted(planted),
 3309                     "units[gba:Game].members is the five planted paths, sorted, without the .bak",
 3310                     f"members {members(m, unit)}")
 3311      f += not check(not any(k.endswith(".png") for k in m.get("entries", {})),
 3312                     "no entry is keyed on a .png (sidecars are members, not versions)",
 3313                     f"png entries: {[k for k in m.get('entries', {}) if k.endswith('.png')]}")
 3314      sealed = [(rel, stage_sha(a, (entry(m, rel) or {}).get("sha256", "")) == (entry(m, rel) or {}).get("sha256"))
 3315                for rel in (srm, s1, auto)]
 3316      f += not check(all(ok for _, ok in sealed), "stage/<sha> hashes to its own name for each version",
 3317                     f"seals wrong or missing for {[rel for rel, ok in sealed if not ok]}")
 3318      spawns = a.run("cat /tmp/qa-spawns 2>/dev/null || true").strip()
 3319      f += not check(not spawns, "no rclone was spawned", f"rclone was spawned: {spawns[:80]!r}")
 3320      newer = a.run(f"find {shlex.quote(root)} -newer /tmp/qa-mark 2>/dev/null || true").strip()
 3321      f += not check(not newer, "nothing was written into the saves tree",
 3322                     f"written into the saves tree: {newer.splitlines()[:3]}")
 3323      size = a.run("wc -c < /tmp/qa-cap1.out 2>/dev/null || echo -1").strip()
 3324      f += not check(size == "0", "stdout was empty (ES reads that pipe)", f"{size} byte(s) on stdout")
 3325      stamp = last_capture(a, "exit")
 3326      f += not check(stamp is not None and stamp[1] == "0" and stamp[2].split("!")[0] == "exit" and stamp[3] == unit,
 3327                     f"{CACHE}/last-capture records rc 0, mode exit, the unit", f"last-capture is {stamp!r}")
 3328      f += not check(stamp is not None and stamp[4] == "emu-exit=1" and stamp[5] == "retroarch/mgba",
 3329                     "and carries the launch's exit as ES passed it (emu-exit=1: runemu.sh's 0/1, not the emulator's own code) "
 3330                     "and the frozen pair retroarch/mgba, which only the exit path knew",
 3331                     f"last-capture is {stamp!r}")
 3332      a.run("rm -rf /tmp/noroute /tmp/qa-shim /tmp/qa-spawns /tmp/qa-mark /tmp/qa-cap1.out /tmp/qa-cap1.err", check=False)
 3333      return f
 3334  
 3335  
 3336  def fx_cap2(p):
 3337      """CAP2: the recorded core is the argument, never a default. gba's save is
 3338      captured under snes9x2005_plus, then under mgba; a standalone with an
 3339      empty --core records the emulator's name (§6: core is never empty).
 3340  
 3341      ES's half -- that the value is the --core= token of the finished command,
 3342      read after setupSaveState, and that the call is ungated -- is proven by
 3343      inspection of FileData.cpp (~656, ~764) and by VM procedures (1) and (3),
 3344      not by the harness."""
 3345      f = 0
 3346      a, root = p.a, p.root
 3347      p.reset()
 3348      rel, rom = "gba/Core.srm", p.path("gba/Core.gba")
 3349      v1 = plant(a, root, rel, os.urandom(700))
 3350      rc, _ = capture(a, root, "gba", rom, core="snes9x2005_plus")
 3351      e1 = entry(manifest_of(a), rel) or {}
 3352      f += not check(rc == 0 and e1.get("core") == "snes9x2005_plus" and e1.get("emulator") == "retroarch",
 3353                     "core is snes9x2005_plus (not gba's default), emulator retroarch",
 3354                     f"exit {rc}; core {e1.get('core')!r}, emulator {e1.get('emulator')!r}")
 3355      time.sleep(1.1)   # captured_at keeps seconds
 3356      plant(a, root, rel, os.urandom(701))
 3357      rc, _ = capture(a, root, "gba", rom, core="mgba")
 3358      e2 = entry(manifest_of(a), rel) or {}
 3359      f += not check(e2.get("core") == "mgba", "the next version records mgba", f"core {e2.get('core')!r}")
 3360      f += not check(e2.get("replaces") == sha(v1), "replaces is the first version's sha",
 3361                     f"replaces {e2.get('replaces')!r}")
 3362      f += not check((e2.get("captured_at") or "") > (e1.get("captured_at") or "") and ISO_UTC.match(e2.get("captured_at") or ""),
 3363                     "captured_at advanced", f"captured_at {e1.get('captured_at')!r} -> {e2.get('captured_at')!r}")
 3364      f += not check(nulls(e2, ("pub", "published_at")), "pub and published_at are still null",
 3365                     f"pub {e2.get('pub')!r}, published_at {e2.get('published_at')!r}")
 3366      plant(a, root, "n64/Empty.eep", os.urandom(2048))
 3367      rc, _ = capture(a, root, "n64", p.path("n64/Empty.z64"), emulator="mupen64plus", core="")
 3368      e3 = entry(manifest_of(a), "n64/Empty.eep") or {}
 3369      f += not check(rc == 0 and e3.get("core") == "mupen64plus" and e3.get("emulator") == "mupen64plus",
 3370                     "an empty --core is recorded as the emulator's name (never empty)",
 3371                     f"exit {rc}; core {e3.get('core')!r}, emulator {e3.get('emulator')!r}")
 3372      return f
 3373  
 3374  
 3375  def fx_cap3(p):
 3376      """CAP3: the seal is an independent copy. (a) The sealed copy has one link
 3377      and its own inode, and an in-place write to the source afterwards does
 3378      not change it. (b) The negative control on the same filesystem: a hard
 3379      link does follow the write, which is why the seal is a copy (D-CLOUD-034).
 3380      (c) The seal guard's observed positive: a writer racing the copy of a
 3381      64 MiB state; either a clean seal or a declined member, never an entry
 3382      whose bytes are not in the stage."""
 3383      f = 0
 3384      a, root = p.a, p.root
 3385      p.reset()
 3386      rel, rom = "savestates/gba/Seal.state1", p.path("gba/Seal.gba")
 3387      src = shlex.quote(p.path(rel))
 3388      plant(a, root, rel, b"#RZIPv" + os.urandom(2 * 1024 * 1024))
 3389      rc, _ = capture(a, root, "gba", rom)
 3390      e = entry(manifest_of(a), rel) or {}
 3391      rec = e.get("sha256") or ""
 3392      if rc != 0 or not rec:
 3393          raise Fail(f"the setup capture recorded nothing (exit {rc})")
 3394      links = a.run(f"stat -c '%h %i' {CACHE}/stage/{rec} 2>/dev/null || true").split()
 3395      src_ino = a.run(f"stat -c %i {src}").strip()
 3396      f += not check(links[:1] == ["1"] and len(links) == 2 and links[1] != src_ino,
 3397                     "the seal has one link and its own inode", f"seal stat {links} vs source inode {src_ino}")
 3398      a.run(f"dd if=/dev/urandom of={src} bs=4096 count=1 conv=notrunc 2>/dev/null; sync")
 3399      f += not check(a.sha(p.path(rel)) != rec, "the in-place write to the source landed (the setup)",
 3400                     "the mutation did not change the source; the check below would pass for the wrong reason")
 3401      f += not check(stage_sha(a, rec) == rec, "stage/<sha> still hashes to its name after the source was rewritten",
 3402                     "THE SEAL FOLLOWED AN IN-PLACE WRITE TO THE SOURCE (a link, not a copy)")
 3403      size = a.run(f"stat -c %s {CACHE}/stage/{rec} 2>/dev/null || echo -1").strip()
 3404      f += not check(str(e.get("size")) == size, "the recorded size is the sealed copy's", f"size {e.get('size')} vs seal {size}")
 3405  
 3406      # (b) the control: the scratch root and /storage/.cache are one filesystem
 3407      # (/dev/vda2 on the VM), so ln makes a real hard link; /tmp is tmpfs and
 3408      # would fail with EXDEV.
 3409      rel2 = "savestates/gba/Seal.state2"
 3410      src2 = shlex.quote(p.path(rel2))
 3411      plant(a, root, rel2, b"#RZIPv" + os.urandom(1024 * 1024))
 3412      linked = a.run(f"ln {src2} {CACHE}/qa-link 2>&1 && echo LINKED || true")
 3413      same = a.run(f"stat -c '%h %i' {src2} {CACHE}/qa-link 2>/dev/null || true").split()
 3414      f += not check(len(same) == 4 and same[0] == same[2] == "2" and same[1] == same[3],
 3415                     "the control's premise, stated: qa-link and its source are one inode with two links",
 3416                     f"the control is not a hard link (stat '%h %i' gives {same}); what it shows below proves nothing")
 3417      h1 = a.sha(f"{CACHE}/qa-link")
 3418      a.run(f"dd if=/dev/urandom of={src2} bs=4096 count=1 conv=notrunc 2>/dev/null; sync")
 3419      h2 = a.sha(f"{CACHE}/qa-link")
 3420      a.run(f"rm -f {CACHE}/qa-link")
 3421      f += not check("LINKED" in linked and h1 and h2 and h1 != h2,
 3422                     "the hard-linked variant follows the in-place write, which is why the seal is a copy (D-CLOUD-034)",
 3423                     "the hard link did not follow the write -- the control proves nothing"
 3424                     + ("" if "LINKED" in linked else f" (ln failed: {linked.strip()[:60]})"))
 3425  
 3426      # (c) a writer racing the seal of a big state. The writer is a script so
 3427      # the wait below can find it by a pattern its own shell cannot match.
 3428      big = "savestates/gba/Race.state1"
 3429      bsrc = shlex.quote(p.path(big))
 3430      a.run(f"mkdir -p $(dirname {bsrc}); head -c 67108864 /dev/urandom > {bsrc}; sync")
 3431      a.write("/tmp/qa-cap3-writer.sh",
 3432              (f"#!/bin/bash\nfor i in $(seq 2000); do dd if=/dev/urandom of={bsrc} bs=4096 count=1 "
 3433               "seek=$((RANDOM % 16000)) conv=notrunc 2>/dev/null; done\n").encode())
 3434      mark = log_mark(a)
 3435      a.run("setsid bash /tmp/qa-cap3-writer.sh >/dev/null 2>&1 < /dev/null &")
 3436      rc, _ = capture(a, root, "gba", p.path("gba/Race.gba"))
 3437      a.run("for i in $(seq 200); do pgrep -f 'qa-cap[3]-writer' >/dev/null || break; sleep 0.2; done; rm -f /tmp/qa-cap3-writer.sh",
 3438            check=False)
 3439      e = entry(manifest_of(a), big)
 3440      tail = log_since(a, mark)
 3441      if e is not None:
 3442          sealed = stage_sha(a, e.get("sha256", ""))
 3443          f += not check(sealed == e.get("sha256"), "a clean seal: the entry's sha is a stage file hashing to its name",
 3444                         "AN ENTRY WHOSE BYTES ARE NOT IN THE STAGE (sha recorded, seal absent or torn)")
 3445      else:
 3446          f += not check(rc == 1 and "changed while it was being sealed" in tail,
 3447                         "the member changed under the seal three times and was declined (exit 1, WARN)",
 3448                         f"no entry and no declined-seal WARN (exit {rc}): the guard neither sealed nor said why")
 3449      return f
 3450  
 3451  
 3452  def fx_cap4(p):
 3453      """CAP4: nothing changed, nothing rewritten, in all three modes (I8) --
 3454      the manifest's mtime, inode and content all stand, the stage does not
 3455      grow, and nothing above DEBUG is logged. Then the positive controls, so
 3456      the check can fail: a touch changes the manifest and the entry's mtime
 3457      but not its version; new bytes make a version; a deleted thumbnail leaves
 3458      the declaration."""
 3459      f = 0
 3460      a, root = p.a, p.root
 3461      p.reset()
 3462      unit, srm, s1 = "gba:Game", "gba/Game.srm", "savestates/gba/Game.state1"
 3463      rom = p.path("gba/Game.gba")
 3464      planted = plant_unit(a, root, "gba", "Game", save=604, states={1: 40 * 1024}, auto=30 * 1024, png=3 * 1024)
 3465      rc, _ = capture(a, root, "gba", rom)
 3466      m0, n0 = manifest_stat(a), stage_count(a)
 3467      if rc != 0 or m0 is None:
 3468          raise Fail(f"the setup capture recorded nothing (exit {rc})")
 3469      e0 = entry(manifest_of(a), srm) or {}
 3470      mark = log_mark(a)
 3471      time.sleep(2)   # ext4 keeps seconds: a same-second rewrite is invisible by mtime alone
 3472  
 3473      def unchanged(label, rc, quiet=True):
 3474          # A no-op exit or --full writes nothing and logs nothing above DEBUG
 3475          # (I8). A --retire of a path nothing is known about is allowed its
 3476          # one INFO line ("nothing known about ...; not recorded").
 3477          loud = [l for l in log_since(a, mark).splitlines() if "[cloud_capture]" in l and "[DEBUG]" not in l] if quiet else []
 3478          return not check(rc == 0 and manifest_stat(a) == m0 and stage_count(a) == n0 and not loud,
 3479                           f"{label}: exit 0; manifest mtime/inode/sha and stage count unchanged"
 3480                           + ("; nothing above DEBUG logged" if quiet else ""),
 3481                           f"{label}: exit {rc}; stat {manifest_stat(a)} vs {m0}; stage {stage_count(a)} vs {n0}; "
 3482                           f"logged {loud[:2]}")
 3483  
 3484      rc, _ = capture(a, root, "gba", rom)
 3485      f += unchanged("a second exit with identical arguments", rc)
 3486      for i in (1, 2):
 3487          rc, _ = run_rc(a, "cloud_capture --full")
 3488          f += unchanged(f"--full, pass {i}", rc)
 3489      rc, _ = run_rc(a, "cloud_capture --retire savestates/gba/Nothing.state9")
 3490      f += unchanged("--retire of a path with no entry and no file", rc, quiet=False)
 3491  
 3492      touch_offset(a, p.path(srm), 60)
 3493      rc, _ = capture(a, root, "gba", rom)
 3494      m1 = manifest_stat(a)
 3495      e1 = entry(manifest_of(a), srm) or {}
 3496      f += not check(rc == 0 and m1 is not None and all(x != y for x, y in zip(m1, m0)),
 3497                     "a touch rewrote the manifest (mtime, inode and sha all changed)",
 3498                     f"after a touch the manifest stat is {m1} against {m0}")
 3499      f += not check(e1.get("mtime") == iso_mtime(a, p.path(srm)),
 3500                     "the entry's mtime is the file's new value, ISO-UTC", f"mtime {e1.get('mtime')!r}")
 3501      f += not check(all(e1.get(k) == e0.get(k) for k in ("sha256", "replaces", "captured_at")),
 3502                     "sha256, replaces and captured_at stand (a touch is metadata, not a version)",
 3503                     "a touch made a version: sha256/replaces/captured_at changed")
 3504      plant(a, root, srm, os.urandom(605))
 3505      rc, _ = capture(a, root, "gba", rom)
 3506      e2 = entry(manifest_of(a), srm) or {}
 3507      f += not check(e2.get("sha256") == a.sha(p.path(srm)) != e0.get("sha256") and e2.get("replaces") == e0.get("sha256"),
 3508                     "new bytes made a version whose replaces is the old sha",
 3509                     f"sha {e2.get('sha256', '')[:12]} replaces {e2.get('replaces')!r}")
 3510      a.run(f"rm -f {shlex.quote(p.path(s1 + '.png'))}")
 3511      rc, _ = capture(a, root, "gba", rom)
 3512      m = manifest_of(a)
 3513      f += not check((entry(m, s1) or {}).get("screenshot", "unset") is None,
 3514                     "a deleted thumbnail refreshes the state's screenshot to null",
 3515                     f"screenshot {(entry(m, s1) or {}).get('screenshot', 'unset')!r}")
 3516      f += not check(members(m, unit) == sorted(k for k in planted if k != s1 + ".png"),
 3517                     "and it left units[gba:Game].members", f"members {members(m, unit)}")
 3518      return f
 3519  
 3520  
 3521  def fx_cap5(p):
 3522      """CAP5: core_build is the pin of the core's package -- through the
 3523      exception table and the regular rule -- and an unmapped core is
 3524      "unknown", never empty. Against a planted pins file (CLOUD_CAPTURE_PINS,
 3525      because /usr is read-only), mapped cases first so a negative cannot pass
 3526      for the wrong reason. Every capture writes new bytes first: a repeat with
 3527      only a different --core is an I8 no-op that would read back the previous
 3528      entry (three earlier drafts of this fixture could not pass for that
 3529      reason)."""
 3530      f = 0
 3531      a, root = p.a, p.root
 3532      p.reset()
 3533      pins = {"mgba-lr": "1" * 40, "snes9x2005_plus-lr": "2" * 40, "vice-lr": "3" * 40,
 3534              "neocd_lr": "4" * 40, "mupen64plus-sa": "5" * 40, "ffmpeg-lr": "6" * 40}
 3535      a.write("/tmp/qa-pins", ("".join(f"{k} {v}\n" for k, v in pins.items())).encode())
 3536      env = "CLOUD_CAPTURE_PINS=/tmp/qa-pins"
 3537      mgba_dv = a.run(r"""sed -n 's/^display_version *= *"\(.*\)"$/\1/p' /usr/lib/libretro/mgba_libretro.info 2>/dev/null | head -1""").strip() or None
 3538      n = [0]
 3539  
 3540      def run(core, emulator="retroarch", env=env):
 3541          n[0] += 1
 3542          system = "n64" if emulator == "mupen64plus" else "gba"
 3543          rel = f"{system}/Pins.eep" if emulator == "mupen64plus" else f"{system}/Pins.srm"
 3544          plant(a, root, rel, os.urandom(800 + n[0]))
 3545          rc, out = capture(a, root, system, p.path(f"{system}/Pins.{'z64' if system == 'n64' else 'gba'}"),
 3546                            emulator=emulator, core=core, env=env)
 3547          e = entry(manifest_of(a), rel) or {}
 3548          if rc != 0 or e.get("core") != (core or emulator):
 3549              raise Fail(f"--core {core!r}: exit {rc}, entry {e.get('core')!r} (the setup for the pin check)")
 3550          return e
 3551  
 3552      try:
 3553          f += cap5_cases(a, run, pins, mgba_dv)
 3554      finally:
 3555          a.run("rm -f /tmp/qa-pins", check=False)
 3556      return f
 3557  
 3558  
 3559  def cap5_cases(a, run, pins, mgba_dv):
 3560      """CAP5's assertions, split out so the planted pins file is removed on a
 3561      Fail as well as on the way through."""
 3562      f = 0
 3563      e = run("mgba")
 3564      f += not check(e.get("core_build") == pins["mgba-lr"], "mgba -> mgba-lr's pin (the regular rule)",
 3565                     f"mgba -> core_build {e.get('core_build')!r}")
 3566      f += not check(e.get("core_display_version") == mgba_dv,
 3567                     f"core_display_version is the .info's display_version ({mgba_dv!r})",
 3568                     f"core_display_version {e.get('core_display_version')!r}, .info says {mgba_dv!r}")
 3569      for core, pkg, why in (("snes9x2005_plus", "snes9x2005_plus-lr", "the underscore is kept"),
 3570                             ("vice_x64", "vice-lr", "five .so, one package"),
 3571                             ("neocd", "neocd_lr", "the only _lr package")):
 3572          e = run(core)
 3573          f += not check(e.get("core_build") == pins[pkg], f"{core} -> {pkg}'s pin ({why})",
 3574                         f"{core} -> core_build {e.get('core_build')!r}, wanted {pkg}'s")
 3575      e = run("mupen64plus-sa", emulator="mupen64plus")
 3576      f += not check(e.get("core_build") == pins["mupen64plus-sa"], "mupen64plus-sa -> its own pin (the *-sa identity rule)",
 3577                     f"mupen64plus-sa -> core_build {e.get('core_build')!r}")
 3578      e = run("no-such-core")
 3579      f += not check(e.get("core_build") == "unknown" and "core_display_version" in e and e["core_display_version"] is None,
 3580                     "an unmapped core -> core_build \"unknown\", core_display_version null",
 3581                     f"no-such-core -> {e.get('core_build')!r} / {e.get('core_display_version', 'absent')!r}")
 3582      e = run("ffmpeg")
 3583      f += not check(e.get("core_build") == "unknown",
 3584                     "ffmpeg -> \"unknown\" despite a planted ffmpeg-lr line (the exception table fires)",
 3585                     f"ffmpeg -> core_build {e.get('core_build')!r}: the exception table did not fire")
 3586      e = run("mupen64plus")
 3587      f += not check("core_display_version" in e and e["core_display_version"] is None,
 3588                     "mupen64plus (a .so with no .info) -> core_display_version null",
 3589                     f"mupen64plus -> core_display_version {e.get('core_display_version', 'absent')!r}")
 3590      has_pins = a.run("[ -e /usr/share/rocknix/core-pins ] && echo yes || echo no").strip() == "yes"
 3591      if has_pins:
 3592          image_pin = a.run("awk '$1 == \"mgba-lr\" { print $2; exit }' /usr/share/rocknix/core-pins").strip()
 3593          e = run("mgba", env="")
 3594          f += not check(bool(image_pin) and e.get("core_build") == image_pin,
 3595                         f"without the override core_build is the image's own mgba-lr pin ({image_pin[:12]}...)",
 3596                         f"image pin {image_pin!r}, recorded {e.get('core_build')!r}")
 3597      else:
 3598          print("    SKIP  image carries no /usr/share/rocknix/core-pins (predates 27eb3264a2); "
 3599                "the map was proven against a planted file")
 3600          e = run("mgba", env="")
 3601          f += not check(e.get("core_build") == "unknown",
 3602                         "without the override an absent pins file renders as \"unknown\", never as a failure",
 3603                         f"no pins file, core_build {e.get('core_build')!r}")
 3604      return f
 3605  
 3606  
 3607  def fx_cap6(p):
 3608      """CAP6: a unit is what the emulator writes. (a) libretro, the ROM in a
 3609      subfolder and a stem with glob and shell characters, with decoys that
 3610      share the prefix. (b) standalone N64: the .eep/.mpk pair beside the ROM
 3611      (SaveSRAMPath in every shipped mupen64plus.cfg), one unit, both members
 3612      declared -- acceptance (7). (c) the historical n64/save/ directory as the
 3613      row's second candidate. (d) a libretro exit of the same N64 ROM joins
 3614      the unit without restamping the standalone's files (rows are keyed by
 3615      emulator)."""
 3616      f = 0
 3617      a, root = p.a, p.root
 3618      p.reset()
 3619      stem = "Game [!] & (x) v1.1"
 3620      unit = f"gba:{stem}"
 3621      planted = plant_unit(a, root, "gba", stem, save=700, states={3: 4096}, auto=4096, png=512, romdir="gba/sub")
 3622      srm, st0, st3, auto = (f"gba/sub/{stem}.srm", f"savestates/gba/{stem}.state",
 3623                             f"savestates/gba/{stem}.state3", f"savestates/gba/{stem}.state.auto")
 3624      planted[st0] = plant(a, root, st0, b"#RZIPv" + os.urandom(4096))   # slot 0, with no thumbnail: six members
 3625      for decoy in (f"savestates/gba/{stem}.state.auto.bak", f"savestates/gba/{stem}x.state9", "savestates/gba/Other.state1"):
 3626          plant(a, root, decoy, b"#RZIPv decoy")
 3627      rc, _ = capture(a, root, "gba", p.path(f"gba/sub/{stem}.gba"))
 3628      m = manifest_of(a) or {}
 3629      entries = m.get("entries", {})
 3630      f += not check(rc == 0 and sorted(entries) == sorted([srm, st0, st3, auto]),
 3631                     "exactly four entries: the .srm (keyed under gba/sub/), .state, .state3, .state.auto",
 3632                     f"exit {rc}; entries {sorted(entries)}")
 3633      f += not check(all(e.get("unit") == unit for e in entries.values()) and entries,
 3634                     f"all with unit {unit!r}", f"units {[e.get('unit') for e in entries.values()]}")
 3635      slots = [(entries.get(r) or {}).get("slot", "absent") for r in (srm, st0, st3, auto)]
 3636      f += not check(slots == [None, 0, 3, None], "slots null/0/3/null (a bare .state is slot 0)", f"slots {slots}")
 3637      f += not check((entries.get(st3) or {}).get("screenshot") == st3 + ".png",
 3638                     "state3's screenshot is its .png", f"screenshot {(entries.get(st3) or {}).get('screenshot')!r}")
 3639      f += not check(members(m, unit) == sorted(planted),
 3640                     "members are exactly the six real paths -- no decoy, no Other.state1",
 3641                     f"members {members(m, unit)}")
 3642  
 3643      eep, mpk = "n64/Torn.eep", "n64/Torn.mpk"
 3644      plant(a, root, eep, os.urandom(2048))
 3645      plant(a, root, mpk, os.urandom(32768))
 3646      rc, _ = capture(a, root, "n64", p.path("n64/Torn.z64"), emulator="mupen64plus", core="mupen64plus-sa")
 3647      m = manifest_of(a) or {}
 3648      pair = [entry(m, r) or {} for r in (eep, mpk)]
 3649      f += not check(rc == 0 and all(e.get("kind") == "save" and e.get("unit") == "n64:Torn"
 3650                                     and "slot" in e and e["slot"] is None and "screenshot" in e and e["screenshot"] is None
 3651                                     for e in pair),
 3652                     "the standalone pair: two save entries, slot and screenshot null, one unit n64:Torn",
 3653                     f"exit {rc}; pair {[(e.get('kind'), e.get('unit'), e.get('slot', 'absent')) for e in pair]}")
 3654      f += not check(members(m, "n64:Torn") == [eep, mpk], "units[n64:Torn].members declares both (acceptance 7)",
 3655                     f"members {members(m, 'n64:Torn')}")
 3656  
 3657      plant(a, root, "n64/save/Old.eep", os.urandom(2048))
 3658      plant(a, root, "n64/save/Old.mpk", os.urandom(32768))
 3659      rc, _ = capture(a, root, "n64", p.path("n64/Old.z64"), emulator="mupen64plus", core="mupen64plus-sa")
 3660      m = manifest_of(a) or {}
 3661      old = [(entry(m, r) or {}).get("unit") for r in ("n64/save/Old.eep", "n64/save/Old.mpk")]
 3662      f += not check(rc == 0 and old == ["n64:Old", "n64:Old"],
 3663                     "the historical n64/save/ directory is the row's second candidate (what the allowlist has named for years)",
 3664                     f"exit {rc}; units {old}")
 3665  
 3666      plant(a, root, "n64/Torn.srm", os.urandom(1024))
 3667      plant(a, root, "savestates/n64/Torn.state1", b"#RZIPv" + os.urandom(4096))
 3668      rc, _ = capture(a, root, "n64", p.path("n64/Torn.z64"), emulator="retroarch", core="mupen64plus_next")
 3669      m = manifest_of(a) or {}
 3670      lr = [(entry(m, r) or {}) for r in ("n64/Torn.srm", "savestates/n64/Torn.state1")]
 3671      f += not check(rc == 0 and all(e.get("unit") == "n64:Torn" and e.get("emulator") == "retroarch" for e in lr),
 3672                     "a libretro exit of the same ROM joins unit n64:Torn", f"exit {rc}; {[(e.get('unit'), e.get('emulator')) for e in lr]}")
 3673      f += not check(members(m, "n64:Torn") == [eep, mpk, "n64/Torn.srm", "savestates/n64/Torn.state1"],
 3674                     "units[n64:Torn] now declares all four", f"members {members(m, 'n64:Torn')}")
 3675      f += not check(all((entry(m, r) or {}).get("emulator") == "mupen64plus" for r in (eep, mpk)),
 3676                     "the .eep/.mpk entries still say mupen64plus (rows are keyed by emulator)",
 3677                     f"standalone entries now say {[(entry(m, r) or {}).get('emulator') for r in (eep, mpk)]}")
 3678      return f
 3679  
 3680  
 3681  def fx_cap7(p):
 3682      """CAP7: a renumber is a move, a deletion is a retired record, and nothing
 3683      is invented. The manager's path (--retire before the unlink, --rescan
 3684      after the renumber) carries captured_at, replaces and provenance across
 3685      the move and grows the stage by nothing; a chain of moves resolves; the
 3686      shell path (rm + mv, no --retire) records the move, invents no retired
 3687      row and drops the displaced entry with a WARN, while a member that merely
 3688      vanished keeps its entry; retired is bounded at 200; a path outside the
 3689      root is refused. A thumbnail is a declared member with no entry
 3690      (D-CLOUD-059): retired beside its state it leaves members with the
 3691      state's entry, retired alone its state's screenshot goes to null, and
 3692      neither writes a retired row."""
 3693      f = 0
 3694      a, root = p.a, p.root
 3695      p.reset()
 3696  
 3697      def st(stem, n):
 3698          return f"savestates/gba/{stem}.state{n}"
 3699  
 3700      def q(rel):
 3701          return shlex.quote(p.path(rel))
 3702  
 3703      # The manager's path.
 3704      s = {n: b"#RZIPv" + os.urandom(3000 + n) for n in (1, 2, 3)}
 3705      plant(a, root, "gba/Re.srm", os.urandom(512))
 3706      for n, data in s.items():
 3707          plant(a, root, st("Re", n), data)
 3708          plant(a, root, st("Re", n) + ".png", b"\x89PNG" + os.urandom(300 + n))
 3709      rc, _ = capture(a, root, "gba", p.path("gba/Re.gba"))
 3710      m = manifest_of(a) or {}
 3711      before = {n: dict(entry(m, st("Re", n)) or {}) for n in s}
 3712      if rc != 0 or not all(before[n].get("sha256") == sha(s[n]) for n in s):
 3713          raise Fail(f"the setup capture did not record the three states (exit {rc})")
 3714      # The state and its thumbnail together, as GuiSaveState hands them over.
 3715      rc, _ = run_rc(a, f"cloud_capture --retire {q(st('Re', 2))} {shlex.quote(st('Re', 2) + '.png')}")
 3716      m = manifest_of(a) or {}
 3717      retired = m.get("retired") or []
 3718      f += not check(rc == 0 and entry(m, st("Re", 2)) is None and st("Re", 2) + ".png" not in m.get("entries", {}),
 3719                     "--retire (one absolute, one relative path) exited 0 and removed the state's entry",
 3720                     f"exit {rc}; state2 entry {'present' if entry(m, st('Re', 2)) else 'gone'}")
 3721      rows = {r.get("path"): r for r in retired}
 3722      f += not check(len(retired) == 1 and rows.get(st("Re", 2), {}).get("sha256") == sha(s[2]) and st("Re", 2) + ".png" not in rows,
 3723                     "one retired row: the state with its entry's sha, root-relative; none for the thumbnail, "
 3724                     "which has no version to retire (D-CLOUD-059)",
 3725                     f"retired {[(r.get('path'), (r.get('sha256') or '')[:8]) for r in retired]}")
 3726      f += not check(all("retires_pub" in r and r["retires_pub"] is None and ISO_UTC.match(r.get("at") or "") for r in retired),
 3727                     "retires_pub null and `at` ISO-UTC on it", f"rows {retired}")
 3728      f += not check(members(m, "gba:Re") is not None and not any(x in members(m, "gba:Re") for x in (st("Re", 2), st("Re", 2) + ".png")),
 3729                     "units[gba:Re].members no longer names either", f"members {members(m, 'gba:Re')}")
 3730      stamp = last_capture(a, "retire")
 3731      f += not check(stamp is not None and stamp[2] == "retire" and stamp[4:] == ("emu-exit=?", "-/-"),
 3732                     "last-capture for a --retire reads mode retire, emu-exit=? and -/- (no game ran)", f"last-capture is {stamp!r}")
 3733      # A thumbnail alone (the manager can delete just the picture): the
 3734      # state's entry stays, its screenshot goes to null, and that is what
 3735      # drops the .png from members -- still no retired row.
 3736      png1 = st("Re", 1) + ".png"
 3737      rc, _ = run_rc(a, f"cloud_capture --retire {q(png1)}")
 3738      m = manifest_of(a) or {}
 3739      e1 = entry(m, st("Re", 1)) or {}
 3740      f += not check(rc == 0 and e1.get("sha256") == sha(s[1]) and "screenshot" in e1 and e1["screenshot"] is None,
 3741                     "--retire of a thumbnail alone: exit 0, the state's entry stays with screenshot null",
 3742                     f"exit {rc}; state1 {'HAS NO ENTRY' if not e1 else 'screenshot ' + repr(e1.get('screenshot'))}")
 3743      f += not check(len(m.get("retired") or []) == 1 and png1 not in {r.get("path") for r in m.get("retired") or []},
 3744                     "and retired gained nothing", f"retired {[(r.get('path'), (r.get('sha256') or '')[:8]) for r in m.get('retired') or []]}")
 3745      f += not check(members(m, "gba:Re") is not None and png1 not in members(m, "gba:Re") and st("Re", 1) in members(m, "gba:Re"),
 3746                     "units[gba:Re].members drops the png and keeps the state", f"members {members(m, 'gba:Re')}")
 3747      f += not check(not any(k.endswith(".png") for k in m.get("entries", {})),
 3748                     "no entry was created for the png (a meta op on a missing entry makes nothing)",
 3749                     f"png entries: {[k for k in m.get('entries', {}) if k.endswith('.png')]}")
 3750      a.run(f"rm -f {q(png1)}")
 3751      # The stage baseline is taken after the retire: its GC drops the retired
 3752      # version's seal (referenced by no entry), and the claim under test is
 3753      # that the *move* adds nothing. rename keeps mtime, as copyToSlot(move=true) does.
 3754      n_stage, s3_stat = stage_count(a), a.run(f"stat -c '%i %Y' {CACHE}/stage/{sha(s[3])}").strip()
 3755      a.run(f"rm -f {q(st('Re', 2))} {q(st('Re', 2) + '.png')}; mv {q(st('Re', 3))} {q(st('Re', 2))}; "
 3756            f"mv {q(st('Re', 3) + '.png')} {q(st('Re', 2) + '.png')}")
 3757      rc, _ = run_rc(a, f"cloud_capture --rescan --system gba --rom {q('gba/Re.gba')}")
 3758      m = manifest_of(a) or {}
 3759      e2 = entry(m, st("Re", 2)) or {}
 3760      f += not check(rc == 0 and e2.get("sha256") == sha(s[3]) and e2.get("slot") == 2 and e2.get("screenshot") == st("Re", 2) + ".png",
 3761                     "--rescan re-keyed state3's version at state2 with slot 2 and its png",
 3762                     f"exit {rc}; state2 sha {(e2.get('sha256') or '')[:8]} slot {e2.get('slot')!r} screenshot {e2.get('screenshot')!r}")
 3763      f += not check(e2.get("captured_at") == before[3].get("captured_at") and e2.get("replaces") == before[3].get("replaces"),
 3764                     "captured_at and replaces carried from the moved entry",
 3765                     f"captured_at {e2.get('captured_at')!r} vs {before[3].get('captured_at')!r}; replaces {e2.get('replaces')!r}")
 3766      f += not check(e2.get("emulator") == "retroarch" and e2.get("core") == "mgba",
 3767                     "emulator/core carried across the move, not \"unknown\" (a move carries provenance)",
 3768                     f"emulator {e2.get('emulator')!r} core {e2.get('core')!r}")
 3769      f += not check(entry(m, st("Re", 3)) is None, "no entry at state3", "state3 still has an entry")
 3770      f += not check(stage_count(a) == n_stage and a.run(f"stat -c '%i %Y' {CACHE}/stage/{sha(s[3])}").strip() == s3_stat,
 3771                     "the stage did not grow (a move needs no new copy)", f"stage {stage_count(a)} vs {n_stage}")
 3772      f += not check(len(m.get("retired") or []) == 1, "retired is still length 1", f"retired length {len(m.get('retired') or [])}")
 3773  
 3774      # A copy and a new version at its source in one pass: cp -p state1 state2
 3775      # (a copyToSlot without move keeps the mtime) then new bytes at state1.
 3776      # That is a MOVE (state1's old version now sits at state2) and a PUT
 3777      # (state1 holds a new version). The merge once deleted every move source
 3778      # after the reduce, put included, and state1's new bytes were never
 3779      # recorded again -- no entry, and an mtime below every later --started.
 3780      k = {"A": b"#RZIPv" + os.urandom(6001), "B": b"#RZIPv" + os.urandom(6002)}
 3781      plant(a, root, st("Copy", 1), k["A"])
 3782      capture(a, root, "gba", p.path("gba/Copy.gba"))
 3783      ka = dict(entry(manifest_of(a), st("Copy", 1)) or {})
 3784      a.run(f"cp -p {q(st('Copy', 1))} {q(st('Copy', 2))}")
 3785      plant(a, root, st("Copy", 1), k["B"])
 3786      rc, _ = run_rc(a, f"cloud_capture --rescan --system gba --rom {q('gba/Copy.gba')}")
 3787      m = manifest_of(a) or {}
 3788      k1, k2 = entry(m, st("Copy", 1)) or {}, entry(m, st("Copy", 2)) or {}
 3789      f += not check(rc == 0 and k2.get("sha256") == sha(k["A"]) and k2.get("captured_at") == ka.get("captured_at"),
 3790                     "cp -p then rewrite: state2 holds the old version as a move (original captured_at)",
 3791                     f"exit {rc}; state2 {(k2.get('sha256') or '')[:8]} captured_at {k2.get('captured_at')!r} vs {ka.get('captured_at')!r}")
 3792      f += not check(k1.get("sha256") == sha(k["B"]) and k1.get("replaces") == sha(k["A"]),
 3793                     "and state1 keeps its new version as a put whose replaces is the old sha (a put at a move source survives)",
 3794                     f"state1 {'HAS NO ENTRY' if not k1 else (k1.get('sha256') or '')[:8]} replaces {(k1.get('replaces') or '')[:8]} "
 3795                     "-- a put at a move source was dropped with the source (R5: a version nothing will record again)")
 3796  
 3797      # A renumber chain: state4 -> state3 -> state2.
 3798      c = {n: b"#RZIPv" + os.urandom(4000 + n) for n in (1, 2, 3, 4)}
 3799      for n, data in c.items():
 3800          plant(a, root, st("Chain", n), data)
 3801      capture(a, root, "gba", p.path("gba/Chain.gba"))
 3802      m = manifest_of(a) or {}
 3803      cb = {n: dict(entry(m, st("Chain", n)) or {}) for n in c}
 3804      run_rc(a, f"cloud_capture --retire {q(st('Chain', 2))}")
 3805      a.run(f"rm -f {q(st('Chain', 2))}; mv {q(st('Chain', 3))} {q(st('Chain', 2))}; mv {q(st('Chain', 4))} {q(st('Chain', 3))}")
 3806      rc, _ = run_rc(a, f"cloud_capture --rescan --system gba --rom {q('gba/Chain.gba')}")
 3807      m = manifest_of(a) or {}
 3808      c2, c3 = entry(m, st("Chain", 2)) or {}, entry(m, st("Chain", 3)) or {}
 3809      f += not check(rc == 0 and c2.get("sha256") == sha(c[3]) and c3.get("sha256") == sha(c[4]),
 3810                     "the chain resolved: state2 holds S3 and state3 holds S4",
 3811                     f"exit {rc}; state2 {(c2.get('sha256') or '')[:8]} state3 {(c3.get('sha256') or '')[:8]}")
 3812      f += not check(c2.get("captured_at") == cb[3].get("captured_at") and c3.get("captured_at") == cb[4].get("captured_at")
 3813                     and c2.get("replaces") == cb[3].get("replaces") and c3.get("replaces") == cb[4].get("replaces"),
 3814                     "both as moves: original captured_at, no fabricated replaces",
 3815                     f"captured_at {c2.get('captured_at')!r}/{c3.get('captured_at')!r}; replaces {c2.get('replaces')!r}/{c3.get('replaces')!r}")
 3816      chain = sorted(k for k in m.get("entries", {}) if k.startswith("savestates/gba/Chain."))
 3817      f += not check(chain == [st("Chain", 1), st("Chain", 2), st("Chain", 3)], "no new versions: three Chain entries",
 3818                     f"Chain entries {chain}")
 3819  
 3820      # The shell path (A9's shape): rm and mv with no --retire.
 3821      h = {n: b"#RZIPv" + os.urandom(5000 + n) for n in (1, 2, 3)}
 3822      for n, data in h.items():
 3823          plant(a, root, st("Shell", n), data)
 3824      capture(a, root, "gba", p.path("gba/Shell.gba"))
 3825      m = manifest_of(a) or {}
 3826      hb = dict(entry(m, st("Shell", 3)) or {})
 3827      n_retired = len(m.get("retired") or [])
 3828      a.run(f"rm -f {q(st('Shell', 2))}; mv {q(st('Shell', 3))} {q(st('Shell', 2))}")
 3829      mark = log_mark(a)
 3830      rc, _ = capture(a, root, "gba", p.path("gba/Shell.gba"))
 3831      m = manifest_of(a) or {}
 3832      tail = log_since(a, mark)
 3833      h2 = entry(m, st("Shell", 2)) or {}
 3834      f += not check(rc == 0 and h2.get("sha256") == sha(h[3]) and h2.get("captured_at") == hb.get("captured_at"),
 3835                     "the move was recorded at exit (state2 holds S3 with its original captured_at)",
 3836                     f"exit {rc}; state2 {(h2.get('sha256') or '')[:8]} captured_at {h2.get('captured_at')!r} vs {hb.get('captured_at')!r}")
 3837      f += not check(len(m.get("retired") or []) == n_retired, "retired gained nothing (no retire record is invented)",
 3838                     f"retired grew from {n_retired} to {len(m.get('retired') or [])}")
 3839      f += not check("displaced at" in tail and "without a retire record" in tail,
 3840                     "the displaced version was named in a WARN", "no 'displaced at ... without a retire record' WARN")
 3841      f += not check(entry(m, st("Shell", 3)) is None, "the vanished state3 path has no entry", "state3 still has an entry")
 3842      plant(a, root, "gba/Kept.srm", os.urandom(600))
 3843      plant(a, root, st("Kept", 1), b"#RZIPv" + os.urandom(2000))   # a second member, so the unit still scans
 3844      capture(a, root, "gba", p.path("gba/Kept.gba"))
 3845      a.run(f"rm -f {q('gba/Kept.srm')}")
 3846      mark = log_mark(a)
 3847      rc, _ = capture(a, root, "gba", p.path("gba/Kept.gba"))
 3848      m = manifest_of(a) or {}
 3849      f += not check(rc == 0 and entry(m, "gba/Kept.srm") is not None and "claimed but not on disk" in log_since(a, mark),
 3850                     "a member that merely vanished keeps its entry (I5) and the log says 'claimed but not on disk'",
 3851                     f"exit {rc}; entry {'kept' if entry(m, 'gba/Kept.srm') else 'GONE'}; WARN {'present' if 'claimed but not on disk' in log_since(a, mark) else 'absent'}")
 3852  
 3853      # The bound: 250 synthetic rows, one more retire, 200 remain.
 3854      synthetic = [{"sha256": f"{i:064x}", "path": f"savestates/gba/Synthetic.state{i}", "retires_pub": None,
 3855                    "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1577836800 + i))} for i in range(250)]
 3856      a.write("/tmp/qa-retired.json", json.dumps(synthetic).encode())
 3857      a.run(f"jq --slurpfile r /tmp/qa-retired.json '.retired = $r[0]' {p.manifest} > {p.manifest}.tmp && mv -f {p.manifest}.tmp {p.manifest}; "
 3858            "rm -f /tmp/qa-retired.json")
 3859      plant(a, root, "gba/Bound.srm", os.urandom(640))
 3860      capture(a, root, "gba", p.path("gba/Bound.gba"))
 3861      rc, _ = run_rc(a, f"cloud_capture --retire {q('gba/Bound.srm')}")
 3862      m = manifest_of(a) or {}
 3863      retired = m.get("retired") or []
 3864      ats = {r.get("at") for r in retired}
 3865      f += not check(rc == 0 and len(retired) == 200, "retired is trimmed to 200", f"exit {rc}; retired length {len(retired)}")
 3866      f += not check(bool(retired) and retired[-1].get("path") == "gba/Bound.srm", "the newest row is the one just written",
 3867                     f"last row {retired[-1] if retired else None}")
 3868      f += not check(not any(r["at"] in ats for r in synthetic[:51]) and all(r["at"] in ats for r in synthetic[51:]),
 3869                     "the oldest 51 are gone and the rest kept", "the trim did not drop the oldest 51")
 3870  
 3871      mark = log_mark(a)
 3872      rc, _ = run_rc(a, "cloud_capture --retire /storage/cloud-qa-elsewhere/gba/Outside.srm")
 3873      m = manifest_of(a) or {}
 3874      f += not check(rc == 1 and len(m.get("retired") or []) == 200 and "WARN" in log_since(a, mark),
 3875                     "--retire of a path outside the saves root: exit 1, nothing recorded, WARN logged",
 3876                     f"exit {rc}; retired length {len(m.get('retired') or [])}; WARN {'present' if 'WARN' in log_since(a, mark) else 'absent'}")
 3877      return f
 3878  
 3879  
 3880  def fx_cap8(p):
 3881      """CAP8: nothing is stamped that this session did not write; the A2 shape
 3882      at exit; --full's limits. (a) A member with no entry older than --started
 3883      is not recorded, per member; --started 0 records it. (b) An equal-size,
 3884      equal-mtime rewrite is invisible at exit (the documented limit of a
 3885      size+mtime changed set). (c) --full catches it with "unknown" provenance
 3886      and GCs the old seal. (d) --full adopts no path without an entry. (e)
 3887      --full refuses an empty root (A9's shape, fail-closed)."""
 3888      f = 0
 3889      a, root = p.a, p.root
 3890      p.reset()
 3891      old, rom = "savestates/gba/Old.state1", p.path("gba/Old.gba")
 3892      plant(a, root, old, b"#RZIPv" + os.urandom(3000))
 3893      touch_offset(a, p.path(old), -3600)
 3894      started = int(a.run("date +%s").strip())
 3895      mark = log_mark(a)
 3896      rc, _ = capture(a, root, "gba", rom, started=started)
 3897      f += not check(rc == 0 and manifest_of(a) is None,
 3898                     "a member older than --started with no entry: exit 0 and no manifest was created",
 3899                     f"exit {rc}; manifest {'created' if manifest_of(a) is not None else 'absent'}")
 3900      f += not check("have no entry and were not stamped" in log_since(a, mark),
 3901                     "the log says it was not stamped", "no 'have no entry and were not stamped' line")
 3902      # The same unit gains a member this session wrote: recorded, the old one still not.
 3903      plant(a, root, "gba/Old.srm", os.urandom(512))
 3904      rc, _ = capture(a, root, "gba", rom, started=started)
 3905      m = manifest_of(a)
 3906      f += not check(rc == 0 and entry(m, "gba/Old.srm") is not None and entry(m, old) is None,
 3907                     "the fresh .srm is recorded and the old state still is not (the rule is per member, not per run)",
 3908                     f"exit {rc}; srm {'recorded' if entry(m, 'gba/Old.srm') else 'missing'}, old state {'STAMPED' if entry(m, old) else 'not recorded'}")
 3909      rc, _ = capture(a, root, "gba", rom, started=0)
 3910      f += not check(rc == 0 and entry(manifest_of(a), old) is not None, "--started 0 records it",
 3911                     f"exit {rc}; old state {'recorded' if entry(manifest_of(a), old) else 'still missing'}")
 3912  
 3913      same, srom = "gba/Same.srm", p.path("gba/Same.gba")
 3914      one, two = b"version-one-of-this-save", b"version-two-of-this-save"
 3915      assert len(one) == len(two)
 3916      plant(a, root, same, one)
 3917      capture(a, root, "gba", srom)
 3918      qf = shlex.quote(p.path(same))
 3919      a.run(f"cp -p {qf} {qf}.ref")
 3920      plant(a, root, same, two)
 3921      a.run(f"touch -r {qf}.ref {qf}; rm -f {qf}.ref; sync")
 3922      m0 = manifest_stat(a)
 3923      rc, _ = capture(a, root, "gba", srom)
 3924      f += not check(rc == 0 and (entry(manifest_of(a), same) or {}).get("sha256") == sha(one) and manifest_stat(a) == m0,
 3925                     "an equal-size, equal-mtime rewrite is not seen at exit (the documented limit of size+mtime)",
 3926                     f"exit {rc}; entry sha is {name_of((entry(manifest_of(a), same) or {}).get('sha256'), {'one': one, 'two': two})}")
 3927      rc, _ = run_rc(a, "cloud_capture --full")
 3928      m = manifest_of(a)
 3929      e = entry(m, same) or {}
 3930      f += not check(rc == 0 and e.get("sha256") == sha(two) and e.get("replaces") == sha(one),
 3931                     "--full caught it: version two, replaces version one",
 3932                     f"exit {rc}; sha {name_of(e.get('sha256'), {'one': one, 'two': two})} replaces {name_of(e.get('replaces'), {'one': one, 'two': two})}")
 3933      f += not check(e.get("emulator") == e.get("core") == e.get("core_build") == "unknown"
 3934                     and "core_display_version" in e and e["core_display_version"] is None,
 3935                     "with emulator/core/core_build \"unknown\" and core_display_version null (the session was not observed)",
 3936                     f"provenance {[e.get(k) for k in ('emulator', 'core', 'core_build', 'core_display_version')]}")
 3937      f += not check(e.get("system") == "gba" and e.get("rom") == "Same.gba" and e.get("unit") == "gba:Same" and e.get("kind") == "save",
 3938                     "system/rom/unit/kind carried", f"{[e.get(k) for k in ('system', 'rom', 'unit', 'kind')]}")
 3939      f += not check(nulls(e, ("producer", "pub", "published_at")), "producer/pub/published_at null",
 3940                     f"{[e.get(k, 'absent') for k in ('producer', 'pub', 'published_at')]}")
 3941      f += not check(stage_sha(a, sha(two)) == sha(two) and stage_sha(a, sha(one)) is None,
 3942                     "the new sha is in the stage and the old one was GC'd",
 3943                     f"stage: two {'present' if stage_sha(a, sha(two)) else 'MISSING'}, one {'still present' if stage_sha(a, sha(one)) else 'gone'}")
 3944  
 3945      plant(a, root, "savestates/gba/Stray.state7", b"#RZIPv" + os.urandom(2000))
 3946      m0 = manifest_stat(a)
 3947      rc, _ = run_rc(a, "cloud_capture --full")
 3948      f += not check(rc == 0 and entry(manifest_of(a), "savestates/gba/Stray.state7") is None and manifest_stat(a) == m0,
 3949                     "--full adopts nothing: a fresh file with no entry stays unrecorded and the manifest is untouched",
 3950                     f"exit {rc}; stray {'ADOPTED' if entry(manifest_of(a), 'savestates/gba/Stray.state7') else 'not adopted'}; "
 3951                     f"stat {'unchanged' if manifest_stat(a) == m0 else 'CHANGED'}")
 3952  
 3953      ents0 = (manifest_of(a) or {}).get("entries")
 3954      qr = shlex.quote(root)
 3955      mark = log_mark(a)
 3956      a.run(f"mv {qr} {qr}.away; mkdir -p {qr}")
 3957      try:
 3958          rc, _ = run_rc(a, "cloud_capture --full")
 3959          tail = log_since(a, mark)
 3960      finally:
 3961          a.run(f"rm -rf {qr}; mv {qr}.away {qr}")
 3962      f += not check(rc == 1 and (manifest_of(a) or {}).get("entries") == ents0 and root in tail,
 3963                     "--full on an empty root: exit 1, entries untouched, the log names the root",
 3964                     f"exit {rc}; entries {'unchanged' if (manifest_of(a) or {}).get('entries') == ents0 else 'CHANGED'}; "
 3965                     f"root named {'yes' if root in tail else 'no'}")
 3966      return f
 3967  
 3968  
 3969  def fx_cap9(p):
 3970      """CAP9: the error policy is the one written down, and the un-provable is
 3971      not faked. Usage errors exit 2 on stderr; a missing SAVESPATH, an
 3972      unwritable stage and a newer schema exit 1 with the manifest untouched
 3973      and an ERROR naming the path; a corrupt manifest is moved aside and the
 3974      session still recorded; the durable stamps survive where /var/log does
 3975      not; the no-lock claim is a static check, labelled as one; the jq-absent
 3976      branch is not reachable on a read-only /usr and is not pretended."""
 3977      f = 0
 3978      a, root = p.a, p.root
 3979      p.reset()
 3980      rom = p.path("gba/Policy.gba")
 3981      for label, cmd in (("no --started", "cloud_capture --system gba --rom x.gba --emulator retroarch --core mgba"),
 3982                         ("no --core", "cloud_capture --system gba --rom x.gba --emulator retroarch --started 0"),
 3983                         ("an unknown flag", "cloud_capture --bogus"),
 3984                         ("--retire with no path", "cloud_capture --retire")):
 3985          out = a.run(f"{cmd} >/tmp/qa-u.out 2>/tmp/qa-u.err; echo rc=$?; wc -c < /tmp/qa-u.err", check=False).split()
 3986          rc = int(out[0][3:]) if out and out[0].startswith("rc=") else -1
 3987          err = int(out[1]) if len(out) > 1 and out[1].isdigit() else 0
 3988          f += not check(rc == 2 and err > 0, f"{label}: exit 2 with a line on stderr", f"{label}: exit {rc}, {err} byte(s) on stderr")
 3989      f += not check(manifest_of(a) is None, "usage errors created no manifest", "a usage error created a manifest")
 3990      a.run("rm -f /tmp/qa-u.out /tmp/qa-u.err", check=False)
 3991  
 3992      # A system with no <emulators> element (tools) exits with an empty pair.
 3993      # That is nothing to record, not a usage error: exit 0, no manifest, and
 3994      # no capture-failures row -- one per run of such a system would crowd the
 3995      # real failures out of the 20 the stamp keeps. ES also skips the spawn
 3996      # for an empty launchedEmulator; this is the producer's own guard.
 3997      n0 = failures_lines(a)
 3998      rc, _ = run_rc(a, "cloud_capture --system tools --rom /storage/roms/tools/x.sh --emulator '' --core '' --started 0 --exit 0")
 3999      stamp = last_capture(a, "exit")
 4000      f += not check(rc == 0 and manifest_of(a) is None and failures_lines(a) == n0 and stamp is not None and stamp[1] == "0",
 4001                     "--emulator '' (a system with no emulator): exit 0, nothing recorded, no capture-failures row, last-capture rc 0",
 4002                     f"exit {rc}; manifest {'created' if manifest_of(a) is not None else 'absent'}; failures {failures_lines(a)} vs {n0}; stamp {stamp!r}")
 4003      f += not check(stamp is not None and stamp[4:] == ("emu-exit=0", "-/-"),
 4004                     "its stamp carries the exit it was given (emu-exit=0) and -/- for the empty pair", f"stamp {stamp!r}")
 4005  
 4006      set_key(a, "SAVESPATH", "/storage/cloud-qa-missing")
 4007      n0 = failures_lines(a)
 4008      mark = log_mark(a)
 4009      rc, _ = capture(a, root, "gba", rom)
 4010      set_key(a, "SAVESPATH", root)
 4011      tail = log_since(a, mark)
 4012      f += not check(rc == 1 and manifest_of(a) is None and "ERROR" in tail and "/storage/cloud-qa-missing" in tail,
 4013                     "SAVESPATH not a directory: exit 1, no manifest, ERROR naming the path",
 4014                     f"exit {rc}; manifest {'created' if manifest_of(a) is not None else 'absent'}; log {tail.strip()[-80:]!r}")
 4015      f += not check(failures_lines(a) > n0, "capture-failures gained a line", "no capture-failures line for a refused run")
 4016      stamp_b = last_capture(a, "exit")
 4017  
 4018      plant(a, root, "gba/Policy.srm", os.urandom(512))
 4019      rc, _ = capture(a, root, "gba", rom)
 4020      m0 = manifest_stat(a)
 4021      if rc != 0 or m0 is None:
 4022          raise Fail(f"the setup capture recorded nothing (exit {rc})")
 4023      a.run(f"rm -rf {CACHE}/stage; touch {CACHE}/stage")
 4024      plant(a, root, "gba/Policy.srm", os.urandom(513))
 4025      mark = log_mark(a)
 4026      rc, _ = capture(a, root, "gba", rom)
 4027      tail = log_since(a, mark)
 4028      a.run(f"rm -f {CACHE}/stage")
 4029      f += not check(rc == 1 and manifest_stat(a) == m0 and "ERROR" in tail and f"{CACHE}/stage" in tail,
 4030                     "stage unwritable (a file where the directory goes): exit 1, manifest untouched, ERROR naming the stage",
 4031                     f"exit {rc}; stat {'unchanged' if manifest_stat(a) == m0 else 'CHANGED'}; log {tail.strip()[-80:]!r}")
 4032  
 4033      a.run(f"printf 'not json{{' > {p.manifest}")
 4034      plant(a, root, "gba/After.srm", os.urandom(520))
 4035      mark = log_mark(a)
 4036      rc, _ = capture(a, root, "gba", p.path("gba/After.gba"))
 4037      tail = log_since(a, mark)
 4038      aside = a.run(f"for x in {p.manifest}.corrupt-*; do [ -e \"$x\" ] && cat \"$x\"; done 2>/dev/null || true")
 4039      present, text = manifest_text(a)
 4040      try:
 4041          m = json.loads(text) if present else None
 4042      except ValueError:
 4043          m = None
 4044      # The aside is written, named in the log, and then removed by the run
 4045      # that completed: a completed run is the last known good state and the
 4046      # manifests moved aside before it were the previous one (D-CLOUD-078,
 4047      # 2026-09-10). This check expected the aside to remain, which it did
 4048      # until then; it had not run since (found 2026-09-17, CAP9 against the
 4049      # build 9 script failed the same way).
 4050      f += not check(rc == 0 and "would not parse; moved aside to" in tail and aside == "",
 4051                     "a corrupt manifest is moved aside as manifest-<id>.json.corrupt-<epoch>, the log names it, and the completed run removes the aside (D-CLOUD-078)",
 4052                     f"exit {rc}; aside holds {aside!r}; log: {tail[-240:]!r}")
 4053      f += not check(m is not None and entry(m, "gba/After.srm") is not None,
 4054                     "the new manifest parses and holds this session's entries",
 4055                     "no parseable manifest with this session's entry after the corrupt one was set aside")
 4056      f += not check("WARN" in tail or "ERROR" in tail, "and it was logged", "nothing logged about the corrupt manifest")
 4057  
 4058      a.run(f"jq '.schema = 2' {p.manifest} > {p.manifest}.tmp && mv -f {p.manifest}.tmp {p.manifest}")
 4059      m0 = manifest_stat(a)
 4060      plant(a, root, "gba/After.srm", os.urandom(521))
 4061      n0 = failures_lines(a)
 4062      mark = log_mark(a)
 4063      rc, _ = capture(a, root, "gba", p.path("gba/After.gba"))
 4064      tail = log_since(a, mark)
 4065      f += not check(rc == 1 and manifest_stat(a) == m0 and "ERROR" in tail and "schema" in tail,
 4066                     "a manifest claiming a newer schema: exit 1, untouched, ERROR naming the schema",
 4067                     f"exit {rc}; stat {'unchanged' if manifest_stat(a) == m0 else 'CHANGED'}; log {tail.strip()[-80:]!r}")
 4068      stamp_e = last_capture(a, "exit")
 4069      reason = a.run(f"tail -1 {CACHE}/capture-failures 2>/dev/null || true").strip()
 4070      f += not check(stamp_b is not None and stamp_b[1] == "1" and stamp_e is not None and stamp_e[1] == "1",
 4071                     "last-capture recorded rc 1 after both refusals (a stamp that survives the reboot /var/log does not)",
 4072                     f"last-capture after SAVESPATH: {stamp_b!r}; after schema: {stamp_e!r}")
 4073      f += not check(stamp_b is not None and stamp_b[4:] == ("emu-exit=?", "retroarch/mgba")
 4074                     and stamp_e is not None and stamp_e[4:] == ("emu-exit=?", "retroarch/mgba"),
 4075                     "both refusals still stamped the frozen pair retroarch/mgba and emu-exit=? (no --exit was passed): "
 4076                     "the run that could not record is the one whose log line will be gone",
 4077                     f"after SAVESPATH: {stamp_b!r}; after schema: {stamp_e!r}")
 4078      f += not check(failures_lines(a) > n0 and "schema" in reason, "capture-failures names the reason",
 4079                     f"capture-failures last line {reason!r}")
 4080  
 4081      # A rev 1 manifest -- no unit, units or retired, the shape this writer
 4082      # advertises upgrading in place. --full derives each entry's unit from
 4083      # its system and rom, stamps it on the unchanged entry too, and declares
 4084      # both in units; nothing is filed under "-".
 4085      p.reset()
 4086      r1, k1 = "gba/RevOne.srm", "gba/Kept1.srm"
 4087      one, kept = plant(a, root, r1, b"rev-one-bytes"), plant(a, root, k1, b"kept-bytes")
 4088  
 4089      def rev1(rel, data, digest):
 4090          return {"kind": "save", "sha256": digest, "size": len(data), "mtime": iso_mtime(a, p.path(rel)), "system": "gba",
 4091                  "rom": rel.split("/")[1].replace(".srm", ".gba"), "slot": None, "screenshot": None, "pub": None}
 4092  
 4093      a.write(p.manifest, json.dumps({"schema": 1, "entries": {r1: rev1(r1, one, "1" * 64), k1: rev1(k1, kept, sha(kept))}}).encode())
 4094      mark = log_mark(a)
 4095      rc, _ = run_rc(a, "cloud_capture --full")
 4096      m = manifest_of(a) or {}
 4097      e1, ek = entry(m, r1) or {}, entry(m, k1) or {}
 4098      f += not check(rc == 0 and e1.get("sha256") == sha(one) and e1.get("replaces") == "1" * 64 and e1.get("unit") == "gba:RevOne",
 4099                     "a rev 1 entry re-hashed by --full carries unit gba:RevOne, derived from its system and rom",
 4100                     f"exit {rc}; unit {e1.get('unit')!r} sha {(e1.get('sha256') or '')[:8]} replaces {(e1.get('replaces') or '')[:8]}")
 4101      f += not check(ek.get("unit") == "gba:Kept1" and ek.get("sha256") == sha(kept),
 4102                     "an unchanged rev 1 entry gains its unit too (the upgrade in place)", f"unit {ek.get('unit')!r}")
 4103      f += not check(members(m, "gba:RevOne") == [r1] and members(m, "gba:Kept1") == [k1] and "-" not in (m.get("units") or {}),
 4104                     "units declares both and nothing is filed under \"-\"", f"units {m.get('units')}")
 4105      f += not check("rev 1" in log_since(a, mark), "the upgrade was logged", "no 'rev 1' line in the log")
 4106  
 4107      script = a.run("command -v cloud_capture").strip()
 4108      hits = a.run(f"grep -v '^[[:space:]]*#' {shlex.quote(script)} | grep -c -e flock -e cloud_sync.lock -e rclone -e curl -e wget || true").strip()
 4109      f += not check(hits == "0", "static: no flock, no lock file, no rclone, curl or wget in the shipped script's code "
 4110                     "(CAP1 proves it does not block on a held lock and spawns no rclone through PATH, different claims)",
 4111                     f"static: {hits} non-comment line(s) mention flock, cloud_sync.lock, rclone, curl or wget")
 4112      print("    SKIP  jq-absent branch is not reachable on a read-only /usr; it is covered by code reading, not by this fixture")
 4113      return f
 4114  
 4115  
 4116  def boot_caller_gate(lines):
 4117      """How the autostart runs `cloud_capture --full`, resolved from the file's
 4118      structure rather than from line order. None when there is no --full line;
 4119      else (index, enclosing test text or None, gate_ok, background_ok).
 4120  
 4121      The gate is the `if` that ENCLOSES the --full line: walk back over the
 4122      non-comment lines, where a `fi` opens a nested block that its own `if`
 4123      closes, and the first unmatched `if` is the one guarding us -- an `else`
 4124      or `elif` met first means the line runs when that test is false. It must
 4125      name BOTH toggles (orchestrator decision 2: a gameexit-only device runs
 4126      it too). Line order is not evidence: until #94 the file also held the
 4127      headless sync block, whose own toggle test sat above any line appended
 4128      after its `fi` and satisfied the old check for an ungated --full. The line
 4129      itself must be detached (setsid or nohup, ending in a single `&` -- `&&`
 4130      is a foreground chain) and niced."""
 4131      code = [(i, l.strip()) for i, l in enumerate(lines) if l.strip() and not l.lstrip().startswith("#")]
 4132      full = [i for i, s in code if "cloud_capture --full" in s]
 4133      if not full:
 4134          return None
 4135      enclosing, depth = None, 0
 4136      for i, s in reversed([(i, s) for i, s in code if i < full[0]]):
 4137          if s == "fi" or s.startswith("fi;") or s.startswith("fi "):
 4138              depth += 1
 4139          elif s.startswith("if "):
 4140              if depth == 0:
 4141                  enclosing = s
 4142                  break
 4143              depth -= 1
 4144          elif depth == 0 and (s == "else" or s.startswith("elif ")):
 4145              enclosing = s
 4146              break
 4147      gate_ok = (enclosing is not None and enclosing.startswith("if ")
 4148                 and bool(re.search(r"cloudsaves\.startup", enclosing)) and bool(re.search(r"cloudsaves\.gameexit", enclosing)))
 4149      line = lines[full[0]]
 4150      bg_ok = bool(re.search(r"(setsid|nohup).*(?<!&)&\s*$", line)) and "nice" in line
 4151      return full[0], enclosing, gate_ok, bg_ok
 4152  
 4153  
 4154  def fx_cap10(p):
 4155      """CAP10: the card context informs, it never silently refuses -- and a
 4156      flip discards. (a) A wrong-but-stable card: the version is recorded, the
 4157      log carries cloud_saves_root's sentence, the stamp carries !card. (b) A
 4158      card that changes during the run: discarded, manifest untouched, ERROR,
 4159      capture-failures. (c) --full waits for the usual card and then records.
 4160      (d) The boot caller, statically: --full runs from the autostart behind
 4161      the cloud-saves toggle and in the background (D-CLOUD-057: boot time is
 4162      not ours to spend).
 4163  
 4164      The fireable form: local_reset wipes the saves-root record and with no
 4165      record `cloud_saves_root check` exits 0, so a bogus record is planted."""
 4166      f = 0
 4167      a, root = p.a, p.root
 4168      p.reset()
 4169      rel, rom = "gba/Card.srm", p.path("gba/Card.gba")
 4170      plant(a, root, rel, os.urandom(512))
 4171      rc, _ = capture(a, root, "gba", rom)
 4172      if rc != 0:
 4173          raise Fail(f"the setup capture exited {rc}")
 4174      a.run(f"echo 'uuid:00000000-0000-0000-0000-000000000000' > {CACHE}/saves-root")
 4175      new = plant(a, root, rel, os.urandom(513))
 4176      mark = log_mark(a)
 4177      rc, _ = capture(a, root, "gba", rom)
 4178      tail = log_since(a, mark)
 4179      stamp = last_capture(a, "exit")
 4180      f += not check(rc == 0 and (entry(manifest_of(a), rel) or {}).get("sha256") == sha(new),
 4181                     "on a wrong-but-stable card the new version IS recorded (the file is real; its claim belongs, I5)",
 4182                     f"exit {rc}; entry sha {'is the new bytes' if (entry(manifest_of(a), rel) or {}).get('sha256') == sha(new) else 'is not the new bytes'}")
 4183      f += not check("different card" in tail, "the log carries cloud_saves_root's 'different card' sentence",
 4184                     f"log {tail.strip()[-100:]!r}")
 4185      f += not check(stamp is not None and "!card" in stamp[2], "last-capture carries the !card marker", f"last-capture {stamp!r}")
 4186  
 4187      # (b) a shim beside a copy of the producer: siblings resolve beside $0,
 4188      # so the copy is what makes the shim the one that answers.
 4189      real = a.run("cloud_saves_root identity").strip()
 4190      capbin, idbin = a.run("command -v cloud_capture").strip(), a.run("command -v cloud_device_id").strip()
 4191      a.run(f"rm -rf /tmp/qa-flip; mkdir -p /tmp/qa-flip; cp {shlex.quote(capbin)} /tmp/qa-flip/cloud_capture; "
 4192            f"cp {shlex.quote(idbin)} /tmp/qa-flip/cloud_device_id")
 4193      a.write("/tmp/qa-flip/cloud_saves_root",
 4194              ("#!/bin/sh\ncase \"$1\" in\n"
 4195               f"    check) echo {shlex.quote(real)}; exit 0 ;;\n"
 4196               "    identity) echo uuid:ffffffff-ffff-ffff-ffff-ffffffffffff; exit 0 ;;\n"
 4197               "esac\nexit 0\n").encode())
 4198      a.run("chmod +x /tmp/qa-flip/*")
 4199      m0, n0 = manifest_stat(a), failures_lines(a)
 4200      plant(a, root, rel, os.urandom(514))
 4201      mark = log_mark(a)
 4202      rc, _ = run_rc(a, f"/tmp/qa-flip/cloud_capture --system gba --rom {shlex.quote(rom)} --emulator retroarch --core mgba --started 0")
 4203      tail = log_since(a, mark)
 4204      a.run("rm -rf /tmp/qa-flip", check=False)
 4205      f += not check(rc == 1 and manifest_stat(a) == m0, "a card that changed during the run: exit 1, the manifest untouched (the run was discarded)",
 4206                     f"exit {rc}; stat {'unchanged' if manifest_stat(a) == m0 else 'CHANGED: a scan spanning two trees was recorded'}")
 4207      f += not check("ERROR" in tail and failures_lines(a) > n0, "ERROR logged and capture-failures gained a line",
 4208                     f"ERROR {'present' if 'ERROR' in tail else 'absent'}; failures {failures_lines(a)} vs {n0}")
 4209  
 4210      # (c) --full with the bogus record still in place: it waits (bounded), then records.
 4211      new = plant(a, root, rel, os.urandom(515))
 4212      mark = log_mark(a)
 4213      out = a.run("t0=$(date +%s%N); cloud_capture --full >/dev/null 2>&1; rc=$?; t1=$(date +%s%N); "
 4214                  "echo rc=$rc ms=$(( (t1 - t0) / 1000000 ))", check=False)
 4215      fields = dict(kv.split("=", 1) for kv in out.split() if "=" in kv)
 4216      rc, ms = int(fields.get("rc", -1)), int(fields.get("ms", -1))
 4217      tail = log_since(a, mark)
 4218      f += not check(rc == 0 and (entry(manifest_of(a), rel) or {}).get("sha256") == sha(new),
 4219                     "--full on a wrong-but-stable card: exit 0 and the entry updated (it informs, it does not refuse)",
 4220                     f"exit {rc}; entry {'updated' if (entry(manifest_of(a), rel) or {}).get('sha256') == sha(new) else 'NOT updated'}")
 4221      f += not check(9000 <= ms < 60000, f"and it waited for the usual card first ({ms} ms; the 10 s ceiling of D-CLOUD-057)",
 4222                     f"--full took {ms} ms: it did not wait for the card (or waited far past the ceiling)")
 4223      f += not check("different card" in tail or "wait" in tail.lower(), "the wait was logged",
 4224                     f"no card message in the log: {tail.strip()[-100:]!r}")
 4225  
 4226      # (d) the boot caller, statically. The staged copy first (the repo's
 4227      # file), then the image's.
 4228      staged = f"{a.path_prefix}/102-cloud-saves" if a.path_prefix else ""
 4229      where = a.run(f"for x in {shlex.quote(staged)} /usr/lib/autostart/common/102-cloud-saves; do "
 4230                    "[ -n \"$x\" ] && [ -e \"$x\" ] && { echo \"$x\"; break; }; done; true").strip()
 4231      text = a.run(f"cat {shlex.quote(where)} 2>/dev/null || true") if where else ""
 4232      absent = (f"static: {where or 'no autostart found'} has no 'cloud_capture --full' line -- the image predates the boot "
 4233                "caller; stage autostart/102-cloud-saves beside the producer to check the repo's copy")
 4234      got = boot_caller_gate(text.splitlines())
 4235      if got is None:
 4236          f += not check(False, "", absent)
 4237          f += not check(False, "", absent)
 4238          return f
 4239      idx, enclosing, gate_ok, bg_ok = got
 4240      f += not check(gate_ok, f"static: --full runs at boot inside an `if` on both cloud-saves toggles ({where}:{idx + 1})",
 4241                     f"static: {where}:{idx + 1}: the enclosing test is {enclosing!r} -- expected an `if` naming both "
 4242                     "cloudsaves.startup and cloudsaves.gameexit (a gameexit-only device runs it too; a line after another block's fi is ungated)")
 4243      f += not check(bg_ok, "static: and detached under nice, ending in a single & (never delaying boot, D-CLOUD-057)",
 4244                     f"static: the --full line is not `setsid|nohup ... nice ... &`: {text.splitlines()[idx].strip()[:90]!r}")
 4245      return f
 4246  
 4247  
 4248  def fx_cap11(p):
 4249      """CAP11: two writers of one manifest. The boot --full runs detached
 4250      (D-CLOUD-064) and can overlap the first game's exit capture; capture
 4251      takes no lock, so the loser must notice, and must not lose a first
 4252      version -- a member with no entry and an mtime below the next --started
 4253      is never stamped again. A shim beside a copy of the producer rewrites the
 4254      manifest (adding an entry of its own) between the run's load and its
 4255      rename, once. An exit capture that loses re-runs once against the
 4256      winner's document: exit 0, its version recorded, the other writer's
 4257      entry kept, the re-run logged. --full never retries: exit 1 and
 4258      manifest-moved in capture-failures."""
 4259      f = 0
 4260      a, root = p.a, p.root
 4261      p.reset()
 4262      rel, rom = "gba/Two.srm", p.path("gba/Two.gba")
 4263      plant(a, root, rel, os.urandom(500))
 4264      rc, _ = capture(a, root, "gba", rom)
 4265      if rc != 0:
 4266          raise Fail(f"the setup capture exited {rc}")
 4267      # The shim answers as cloud_device_id (siblings resolve beside $0) and on
 4268      # the --label call -- which the producer makes after loading the manifest
 4269      # and before writing it -- rewrites the manifest through tmp+rename, once.
 4270      capbin, idbin, srbin = (a.run(f"command -v {x}").strip() for x in ("cloud_capture", "cloud_device_id", "cloud_saves_root"))
 4271      other = {"kind": "save", "sha256": "f" * 64, "size": 1, "mtime": "2026-01-01T00:00:00Z", "unit": "gba:Other", "pub": None}
 4272      a.run(f"rm -rf /tmp/qa-two; mkdir -p /tmp/qa-two; cp {shlex.quote(capbin)} /tmp/qa-two/cloud_capture; "
 4273            f"cp {shlex.quote(srbin)} /tmp/qa-two/cloud_saves_root")
 4274      a.write("/tmp/qa-two/cloud_device_id",
 4275              ("#!/bin/sh\n"
 4276               "if [ \"$1\" = --label ] && [ ! -e /tmp/qa-two/written ]; then\n"
 4277               "    : > /tmp/qa-two/written\n"
 4278               f"    m={shlex.quote(p.manifest)}\n"
 4279               f"    [ -f \"$m\" ] && jq --argjson o {shlex.quote(json.dumps(other))} '.entries[\"gba/Other.srm\"] = $o' \"$m\" > \"$m.qa\" "
 4280               "&& mv -f \"$m.qa\" \"$m\"\n"
 4281               "fi\n"
 4282               f"exec {shlex.quote(idbin)} \"$@\"\n").encode())
 4283      a.run("chmod +x /tmp/qa-two/*")
 4284      try:
 4285          new = plant(a, root, rel, os.urandom(501))
 4286          mark = log_mark(a)
 4287          rc, _ = run_rc(a, f"/tmp/qa-two/cloud_capture --system gba --rom {shlex.quote(rom)} --emulator retroarch --core mgba --started 0")
 4288          tail = log_since(a, mark)
 4289          m = manifest_of(a) or {}
 4290          f += not check(a.run("[ -e /tmp/qa-two/written ] && echo yes || echo no").strip() == "yes",
 4291                         "the second writer landed between the run's load and its rename (the setup)",
 4292                         "the shim never wrote: the race was not staged, and the checks below prove nothing")
 4293          f += not check(rc == 0 and (entry(m, rel) or {}).get("sha256") == sha(new),
 4294                         "the exit capture that lost the race exited 0 with its version recorded",
 4295                         f"exit {rc}; entry sha {'is the new bytes' if (entry(m, rel) or {}).get('sha256') == sha(new) else 'IS NOT the new bytes -- a first version was dropped'}")
 4296          f += not check((entry(m, "gba/Other.srm") or {}).get("sha256") == "f" * 64,
 4297                         "and the winner's entry stands (the re-run built on the new document, not over it)",
 4298                         "the other writer's entry is gone: the re-run clobbered the document it lost to")
 4299          f += not check("re-running once" in tail, "the re-run was logged", f"no 're-running once' line: {tail.strip()[-100:]!r}")
 4300          # --full does not retry: it is the writer an exit capture yields to.
 4301          a.run("rm -f /tmp/qa-two/written")
 4302          old = new
 4303          plant(a, root, rel, os.urandom(502))
 4304          n0 = failures_lines(a)
 4305          rc, _ = run_rc(a, "/tmp/qa-two/cloud_capture --full")
 4306          reason = a.run(f"tail -1 {CACHE}/capture-failures 2>/dev/null || true").strip()
 4307          f += not check(rc == 1 and (entry(manifest_of(a), rel) or {}).get("sha256") == sha(old),
 4308                         "--full that lost the race: exit 1 and its version not recorded (no retry; the next run's job)",
 4309                         f"exit {rc}; entry {'still the previous version' if (entry(manifest_of(a), rel) or {}).get('sha256') == sha(old) else 'CHANGED'}")
 4310          f += not check(failures_lines(a) > n0 and "manifest-moved" in reason, "capture-failures names manifest-moved",
 4311                         f"capture-failures last line {reason!r}")
 4312      finally:
 4313          a.run("rm -rf /tmp/qa-two", check=False)
 4314      return f
 4315  
 4316  
 4317  def fx_cap12(p):
 4318      """CAP12: last-capture keeps one line per mode (D-CLOUD-070, #94). A
 4319      single line rewritten on every run let the boot --full pass write over
 4320      the record of the last game exit (RG SP, 2026-09-09: an exit at 08:19Z,
 4321      `full - emu-exit=? -/-` in its place ten hours later), so a row saying
 4322      how the last exit went would have described the boot pass. (a) A stamp
 4323      in the old shape -- one line, from a producer before this -- is read as
 4324      its mode's line and survives a --full pass byte for byte, which adds its
 4325      own line. (b) An exit after that replaces only the exit line, and a
 4326      second --full only the full line, each with its own mode and a newer
 4327      epoch. (c) --retire adds a third line; no mode ever appears twice, and
 4328      every line still parses the way the one-line stamp did.
 4329  
 4330      The fireable form: against the shipped finish() (one line, overwritten)
 4331      (a) reads one line and (b) finds the full line gone after the exit --
 4332      tools/cloud-capture-stamp-test runs the same sequence against a copy of
 4333      the function with no device at all."""
 4334      f = 0
 4335      a, root = p.a, p.root
 4336      p.reset()
 4337      unit, rel, rom = "gba:Stamp", "gba/Stamp.srm", p.path("gba/Stamp.gba")
 4338      plant(a, root, rel, os.urandom(500))
 4339      rc, _ = capture(a, root, "gba", rom, exit_code=0)
 4340      if rc != 0:
 4341          raise Fail(f"the setup capture exited {rc}")
 4342      # (a) the old shape, planted over the setup's stamp: an exit an hour ago,
 4343      # told apart from anything this fixture writes by its unit and epoch.
 4344      old = f"{int(time.time()) - 3600} 0 exit gba:Before emu-exit=0 retroarch/mgba"
 4345      a.run(f"printf '%s\\n' {shlex.quote(old)} > {CACHE}/last-capture")
 4346      rc, _ = run_rc(a, "cloud_capture --full")
 4347      lines = last_capture_lines(a)
 4348      modes = sorted(m for m in map(stamp_mode, lines) if m)
 4349      f += not check(rc == 0 and old in lines,
 4350                     "a one-line stamp from before (an exit) survives a --full pass byte for byte",
 4351                     f"--full exit {rc}; the file holds {lines}")
 4352      f += not check(modes == ["exit", "full"], "and the file holds exactly two lines, exit and full",
 4353                     f"modes {modes}")
 4354      full1 = last_capture(a, "full")
 4355      f += not check(full1 is not None and full1[1] == "0" and full1[3] == "-" and full1[4:] == ("emu-exit=?", "-/-"),
 4356                     "the full line reads rc 0, unit -, emu-exit=? -/-", f"full line {full1!r}")
 4357      f += not check(last_capture(a, "exit") == parse_capture_line(old),
 4358                     "and the exit line, read by mode, is the old one", f"exit line {last_capture(a, 'exit')!r}")
 4359      # (b) an exit replaces the exit line and nothing else
 4360      time.sleep(1)   # epochs are seconds; a same-second replacement is invisible by epoch alone
 4361      plant(a, root, rel, os.urandom(501))
 4362      rc, _ = capture(a, root, "gba", rom, exit_code=1)
 4363      ex = last_capture(a, "exit")
 4364      lines = last_capture_lines(a)
 4365      f += not check(rc == 0 and ex is not None and ex[3] == unit and ex[4] == "emu-exit=1" and int(ex[0]) > int(old.split()[0]),
 4366                     "an exit capture replaced the exit line: this run's unit and emu-exit, a newer epoch",
 4367                     f"exit {rc}; exit line {ex!r}")
 4368      f += not check(old not in lines and last_capture(a, "full") == full1 and len(lines) == 2,
 4369                     "the old exit line is gone, the full line stands unchanged, still two lines",
 4370                     f"the file holds {lines}")
 4371      time.sleep(1)
 4372      rc, _ = run_rc(a, "cloud_capture --full")
 4373      full2 = last_capture(a, "full")
 4374      lines = last_capture_lines(a)
 4375      f += not check(rc == 0 and full2 is not None and int(full2[0]) > int(full1[0]) and last_capture(a, "exit") == ex and len(lines) == 2,
 4376                     "a second --full replaced the full line only: a newer epoch, the exit line unchanged, two lines",
 4377                     f"exit {rc}; full {full2!r} was {full1!r}; exit {last_capture(a, 'exit')!r}; {len(lines)} line(s)")
 4378      # (c) a third mode is a third line; the ceiling is one per mode
 4379      rc, _ = run_rc(a, "cloud_capture --retire savestates/gba/Nothing.state9")
 4380      lines = last_capture_lines(a)
 4381      modes = [m for m in map(stamp_mode, lines) if m]
 4382      f += not check(rc == 0 and sorted(modes) == ["exit", "full", "retire"],
 4383                     "--retire adds a retire line: three lines, one per mode, no mode twice",
 4384                     f"exit {rc}; modes {modes}")
 4385      f += not check(all(parse_capture_line(l) is not None for l in lines),
 4386                     "every line parses as the one-line stamp did (three fields from the front, two from the back)",
 4387                     f"unparseable: {[l for l in lines if parse_capture_line(l) is None]}")
 4388      return f
 4389  
 4390  
 4391  def fx_cap13(p):
 4392      """CAP13: --retire --unlink is the save-state manager's deletion as one
 4393      unit (D-CLOUD-133, #205): the retired row, then the files, in one process
 4394      that ignores SIGTERM -- build 9 held the unlink in EmulationStation and a
 4395      stop between the two left the row with the file still there. (a) A
 4396      recorded slot: the row carries its sha, its entry is gone, the state and
 4397      its thumbnail are gone from disk. (b) A slot with no entry: the row
 4398      carries the live hash and the file goes. (c) --unlink without --retire is
 4399      a usage error (2) and removes nothing. (d) A SIGTERM sent as the run
 4400      starts is ignored: it finishes, the row is written, the file goes."""
 4401      f = 0
 4402      a, root = p.a, p.root
 4403      p.reset()
 4404      rom = p.path("gba/Unit.gba")
 4405      planted = plant_unit(a, root, "gba", "Unit", states={1: 700, 2: 800, 3: 900}, png=64)
 4406      rc, _ = capture(a, root, "gba", rom, exit_code=0)
 4407      if rc != 0:
 4408          raise Fail(f"the setup capture exited {rc}")
 4409      st2, png2 = "savestates/gba/Unit.state2", "savestates/gba/Unit.state2.png"
 4410      rc, _ = run_rc(a, f"cloud_capture --retire --unlink {shlex.quote(p.path(st2))} {shlex.quote(p.path(png2))}")
 4411      m = manifest_of(a) or {}
 4412      rows = [r for r in m.get("retired") or [] if r.get("path") == st2]
 4413      on_disk = a.run(f"for x in {shlex.quote(p.path(st2))} {shlex.quote(p.path(png2))}; do [ -e \"$x\" ] && echo yes || echo no; done").split()
 4414      f += not check(rc == 0 and bool(rows) and rows[0].get("sha256") == sha(planted[st2]) and st2 not in (m.get("entries") or {}),
 4415                     "(a) the retired row carries state2's sha and its entry is gone",
 4416                     f"rc {rc}; rows {rows[:1]}; entry still present: {st2 in (m.get('entries') or {})}")
 4417      f += not check(on_disk == ["no", "no"], "(a) the state and its thumbnail are gone from disk", f"on disk: {on_disk}")
 4418      st7 = "savestates/gba/Unit.state7"
 4419      data = plant(a, root, st7, b"#RZIPv" + os.urandom(300))
 4420      rc, _ = run_rc(a, f"cloud_capture --retire --unlink {shlex.quote(p.path(st7))}")
 4421      m = manifest_of(a) or {}
 4422      rows = [r for r in m.get("retired") or [] if r.get("path") == st7]
 4423      gone = a.run(f"[ -e {shlex.quote(p.path(st7))} ] && echo yes || echo no").strip()
 4424      f += not check(rc == 0 and bool(rows) and rows[0].get("sha256") == sha(data) and gone == "no",
 4425                     "(b) a slot with no entry: the row carries the live hash and the file goes",
 4426                     f"rc {rc}; rows {rows[:1]}; on disk: {gone}")
 4427      st3 = "savestates/gba/Unit.state3"
 4428      rc, _ = run_rc(a, f"cloud_capture --unlink {shlex.quote(p.path(st3))}")
 4429      still = a.run(f"[ -e {shlex.quote(p.path(st3))} ] && echo yes || echo no").strip()
 4430      f += not check(rc == 2 and still == "yes", "(c) --unlink without --retire is refused (2) and removes nothing",
 4431                     f"rc {rc}; state3 on disk: {still}")
 4432      out = a.run(f"cloud_capture --retire --unlink {shlex.quote(p.path(st3))} & pid=$!; sleep 0.05; kill -TERM $pid 2>/dev/null; "
 4433                  f"wait $pid; echo rc=$?; [ -e {shlex.quote(p.path(st3))} ] && echo yes || echo no")
 4434      m = manifest_of(a) or {}
 4435      rows = [r for r in m.get("retired") or [] if r.get("path") == st3]
 4436      f += not check("rc=0" in out and out.strip().endswith("no") and bool(rows),
 4437                     "(d) a SIGTERM as the run starts is ignored: it finishes, the row is written, the file goes",
 4438                     f"out {out.strip()!r}; rows for state3: {len(rows)}")
 4439      # (e) A path outside the saves folder is refused a row and refused the rm
 4440      # (audit #258 PL-002): until 2026-09-24 finish() unlinked every argument
 4441      # once the record was over, refused or not, so a caller's bad path was
 4442      # deleted with a warning and no row. A sibling that is this unit's, given
 4443      # in the same call, is still retired and removed.
 4444      probe = "/tmp/cap13-outside-probe"
 4445      a.run(f"printf outside > {probe}")
 4446      st1 = "savestates/gba/Unit.state1"
 4447      rc, _ = run_rc(a, f"cloud_capture --retire --unlink {shlex.quote(probe)} {shlex.quote(p.path(st1))}")
 4448      m = manifest_of(a) or {}
 4449      rows = [r for r in m.get("retired") or [] if r.get("path") == st1]
 4450      probe_there = a.run(f"[ -e {probe} ] && echo yes || echo no").strip()
 4451      st1_there = a.run(f"[ -e {shlex.quote(p.path(st1))} ] && echo yes || echo no").strip()
 4452      warned = a.run(f"grep -c 'outside the saves folder' /var/log/cloud_sync.log 2>/dev/null || echo 0").strip()
 4453      f += not check(rc == 1 and probe_there == "yes" and st1_there == "no" and bool(rows) and warned not in ("", "0"),
 4454                     "(e) a path outside the saves folder is refused the row and the rm (exit 1, the warning logged); the sibling that is this unit's is retired and removed",
 4455                     f"rc {rc}; probe on disk: {probe_there}; state1 on disk: {st1_there}; rows for state1: {len(rows)}; warnings: {warned}")
 4456      a.run(f"rm -f {probe}")
 4457      return f
 4458  
 4459  
 4460  def fx_cap14(p):
 4461      """CAP14: --adopt records the copy the save-state manager made (#206), which
 4462      no other mode ever did: exit mode takes only what a launch wrote, the
 4463      verify passes adopt nothing new. (a) The source has an entry and the bytes
 4464      match: the new path gets the source's version -- the same sha, emulator,
 4465      core and core_build -- with its own slot, size and thumbnail, replaces and
 4466      pub null, and joins the unit's members. (b) The source has no entry: the
 4467      copy is recorded with unknown provenance and the live hash; the source
 4468      stays unrecorded. (c) A path that is not this unit's: nothing recorded,
 4469      exit 0. (d) A copy then --retire --unlink of it: the row names the copy's
 4470      sha and the files go."""
 4471      f = 0
 4472      a, root = p.a, p.root
 4473      p.reset()
 4474      rom = p.path("gba/Copy.gba")
 4475      planted = plant_unit(a, root, "gba", "Copy", states={3: 900}, png=64)
 4476      rc, _ = capture(a, root, "gba", rom, exit_code=0)
 4477      if rc != 0:
 4478          raise Fail(f"the setup capture exited {rc}")
 4479      st3, st4 = "savestates/gba/Copy.state3", "savestates/gba/Copy.state4"
 4480      a.run(f"cp {shlex.quote(p.path(st3))} {shlex.quote(p.path(st4))}; cp {shlex.quote(p.path(st3 + '.png'))} {shlex.quote(p.path(st4 + '.png'))}")
 4481      rc, _ = run_rc(a, f"cloud_capture --adopt {shlex.quote(p.path(st4))} --from {shlex.quote(p.path(st3))} --system gba --rom {shlex.quote(rom)}")
 4482      m = manifest_of(a) or {}
 4483      ent = m.get("entries") or {}
 4484      e3, e4 = ent.get(st3) or {}, ent.get(st4) or {}
 4485      f += not check(rc == 0 and bool(e4) and e4.get("sha256") == sha(planted[st3]) == e3.get("sha256"),
 4486                     "(a) the copy's entry carries the source's sha", f"rc {rc}; entry {e4}")
 4487      f += not check(bool(e4) and e4.get("emulator") == e3.get("emulator") == "retroarch" and e4.get("core") == e3.get("core")
 4488                     and e4.get("core_build") == e3.get("core_build"),
 4489                     "(a) and the source's emulator, core and core_build",
 4490                     f"copy {e4.get('emulator')}/{e4.get('core')}/{e4.get('core_build')} vs source {e3.get('emulator')}/{e3.get('core')}/{e3.get('core_build')}")
 4491      f += not check(e4.get("slot") == 4 and e4.get("kind") == "state" and e4.get("screenshot") == st4 + ".png"
 4492                     and e4.get("replaces") is None and e4.get("pub") is None,
 4493                     "(a) its own slot, kind and thumbnail; replaces and pub null",
 4494                     f"slot {e4.get('slot')} kind {e4.get('kind')} shot {e4.get('screenshot')} replaces {e4.get('replaces')} pub {e4.get('pub')}")
 4495      members = ((m.get("units") or {}).get("gba:Copy") or {}).get("members") or []
 4496      f += not check(st4 in members and st4 + ".png" in members, "(a) the copy and its thumbnail are the unit's members",
 4497                     f"members {members}")
 4498      st8, st9 = "savestates/gba/Copy.state8", "savestates/gba/Copy.state9"
 4499      data = plant(a, root, st8, b"#RZIPv" + os.urandom(333))
 4500      a.run(f"cp {shlex.quote(p.path(st8))} {shlex.quote(p.path(st9))}")
 4501      rc, _ = run_rc(a, f"cloud_capture --adopt {shlex.quote(p.path(st9))} --from {shlex.quote(p.path(st8))} --system gba --rom {shlex.quote(rom)}")
 4502      m = manifest_of(a) or {}
 4503      ent = m.get("entries") or {}
 4504      e9 = ent.get(st9) or {}
 4505      f += not check(rc == 0 and bool(e9) and e9.get("sha256") == sha(data) and e9.get("emulator") == "unknown"
 4506                     and e9.get("core") == "unknown" and e9.get("core_build") == "unknown" and st8 not in ent,
 4507                     "(b) a copy of an unrecorded source is recorded with unknown provenance and the live hash; the source stays unrecorded",
 4508                     f"rc {rc}; entry {e9}; source recorded: {st8 in ent}")
 4509      other = "savestates/gba/Other.state1"
 4510      plant(a, root, other, b"#RZIPv" + os.urandom(200))
 4511      rc, _ = run_rc(a, f"cloud_capture --adopt {shlex.quote(p.path(other))} --from {shlex.quote(p.path(st3))} --system gba --rom {shlex.quote(rom)}")
 4512      m = manifest_of(a) or {}
 4513      f += not check(rc == 3 and other not in (m.get("entries") or {}),
 4514                     "(c) a path that is not this unit's is not adopted (exit 3, nothing recorded; audit #258 PL-016)",
 4515                     f"rc {rc}; recorded: {other in (m.get('entries') or {})}")
 4516      rc, _ = run_rc(a, f"cloud_capture --retire --unlink {shlex.quote(p.path(st4))} {shlex.quote(p.path(st4 + '.png'))}")
 4517      m = manifest_of(a) or {}
 4518      rows = [r for r in m.get("retired") or [] if r.get("path") == st4]
 4519      on_disk = a.run(f"for x in {shlex.quote(p.path(st4))} {shlex.quote(p.path(st4 + '.png'))}; do [ -e \"$x\" ] && echo yes || echo no; done").split()
 4520      f += not check(rc == 0 and bool(rows) and rows[0].get("sha256") == sha(planted[st3]) and on_disk == ["no", "no"]
 4521                     and st4 not in (m.get("entries") or {}),
 4522                     "(d) the copy deleted with --retire --unlink: the row names its sha, the files go, the entry goes",
 4523                     f"rc {rc}; rows {rows[:1]}; on disk {on_disk}")
 4524      return f
 4525  
 4526  
 4527  CAPTURE_FIXTURES = [
 4528      ("CAP1", "capture on every exit: lock held, no route, no rclone, nothing written into the tree", fx_cap1),
 4529      ("CAP2", "the recorded core is the argument, never a default", fx_cap2),
 4530      ("CAP3", "the seal is an independent copy; a hard link fails; the seal guard fires", fx_cap3),
 4531      ("CAP4", "nothing changed, nothing rewritten -- in all three modes (I8)", fx_cap4),
 4532      ("CAP5", "core_build is the pin for the core's package; unmapped is unknown", fx_cap5),
 4533      ("CAP6", "a unit is what the emulator writes: members, decoys, subfolders, and both N64 layouts", fx_cap6),
 4534      ("CAP7", "a renumber is a move, a deletion is a retired record, and nothing is invented", fx_cap7),
 4535      ("CAP8", "nothing is stamped that this session did not write; the A2 shape; --full's limits", fx_cap8),
 4536      ("CAP9", "the error policy is the one written down, and the un-provable is not faked", fx_cap9),
 4537      ("CAP10", "the card context informs, it never silently refuses -- and a flip discards", fx_cap10),
 4538      ("CAP11", "two writers of one manifest: the loser re-runs once and a first version is not lost", fx_cap11),
 4539      ("CAP12", "last-capture keeps one line per mode: an exit survives the boot pass; the old one-line stamp is read", fx_cap12),
 4540      ("CAP13", "--retire --unlink is the manager's deletion as one unit: row, then files, SIGTERM ignored; a path outside the saves folder is refused the rm", fx_cap13),
 4541      ("CAP14", "--adopt records the copy the manager made: the source's version at the new path, or unknown provenance", fx_cap14),
 4542  ]
 4543  
 4544  
 4545  def snapshot_cache(dev, where="/tmp/qa-cache.tgz"):
 4546      """Archive /storage/.cache/cloud_sync before the fixtures wipe it. Returns
 4547      whether the directory existed, which restore_cache needs to tell "nothing
 4548      to put back" from "the snapshot failed". `where` is on /tmp by default;
 4549      the KILL cells put it on /storage, because a power cut empties /tmp."""
 4550      had = dev.run(f"[ -d {CACHE} ] && echo yes || echo no", check=False).strip() == "yes"
 4551      dev.run(f"rm -f {where}; tar -C /storage/.cache -czf {where} cloud_sync 2>/dev/null || true", check=False)
 4552      return had
 4553  
 4554  
 4555  def restore_cache(dev, had, where="/tmp/qa-cache.tgz"):
 4556      """Put the cache directory back from the snapshot -- only when the
 4557      snapshot exists. tar exiting non-zero for any reason but an absent
 4558      directory (/tmp full, a read error) left no archive, and deleting the
 4559      live directory then would drop the device's saves-root record and every
 4560      last-* stamp on the strength of nothing: a guard that fails open."""
 4561      have = dev.run(f"[ -s {where} ] && echo yes || echo no", check=False).strip() == "yes"
 4562      if have:
 4563          dev.run(f"rm -rf {CACHE}; tar -C /storage/.cache -xzf {where} 2>/dev/null; rm -f {where}", check=False)
 4564      elif had:
 4565          print(f"    WARN  cache snapshot missing; {CACHE} not restored -- the device's stamps and saves-root record "
 4566                "are whatever the fixtures left", file=sys.stderr)
 4567      else:
 4568          dev.run(f"rm -rf {CACHE}", check=False)   # there was none before the run
 4569  
 4570  
 4571  def run_capture(dev, root, args, only):
 4572      """The capture fixtures on one device. The cache directory holds the
 4573      device's own stamps and its saves-root record; the fixtures wipe it, so
 4574      it is carried across and put back, as run_pair does."""
 4575      failures = 0
 4576      p = Solo(dev, root)
 4577      had = snapshot_cache(dev)
 4578      try:
 4579          for key, title, fn in CAPTURE_FIXTURES:
 4580              if only and key not in only:
 4581                  continue
 4582              step(f"{key} -- {title}")
 4583              try:
 4584                  failures += fn(p)
 4585              except Fail as e:
 4586                  failures += 1
 4587                  print(f"    FAIL  {e}")
 4588              failures += litter_scan(dev, {"SAVESPATH": root}, label=f"{key}: ")
 4589      finally:
 4590          local_reset(dev, root)
 4591          restore_cache(dev, had)
 4592      return failures
 4593  
 4594  
 4595  # ===========================================================================
 4596  # #9's contract: the transport under the reconciler, on the pair
 4597  # ===========================================================================
 4598  #
 4599  # Each item runs under `bisync` (rclone bisync between the saves root and the
 4600  # shared folder, --conflict-resolve none, one explicit --resync as the
 4601  # recorded first run) and under `copy` -- the reconciler's own transport
 4602  # (I22): a stand-in classifier over sha256 against a local agreement record,
 4603  # then `rclone copy --files-from --ignore-times` per direction. The harness
 4604  # runs and records; reading each FAIL as upstream-shaped or architectural is
 4605  # Gate 11's job (#9).
 4606  
 4607  RULES = "/storage/.config/cloud_sync-rules.txt"
 4608  BISYNC_STATE = "/storage/.cache/rclone/bisync"   # rclone's default workdir
 4609  AGREED = "/tmp/qa-agreed.json"                   # the stand-in's agreement record
 4610  
 4611  
 4612  def transferred(out):
 4613      m = re.findall(r"Transferred:\s+(\d+) / (\d+)", out)
 4614      return int(m[-1][0]) if m else 0
 4615  
 4616  
 4617  class Transport:
 4618      def __init__(self, kind, pair, extra="", dump=None):
 4619          self.kind, self.p, self.extra = kind, pair, extra
 4620          self.last_cmd = ""
 4621          self.dump, self.tag, self.seq = dump, "setup", 0
 4622  
 4623      def record(self, dev, cmd, rc, out):
 4624          """The raw output of one run, on the host, named by item and order."""
 4625          if not self.dump:
 4626              return
 4627          os.makedirs(self.dump, exist_ok=True)
 4628          self.seq += 1
 4629          who = "a" if dev is self.p.a else "b"
 4630          with open(os.path.join(self.dump, f"{self.kind}-{self.tag}-{self.seq:02d}-{who}.log"), "w") as f:
 4631              f.write(f"$ {cmd}\n# exit {rc}\n{out}")
 4632  
 4633      def remote(self, dev):
 4634          return active_remote(dev) + self.p.saves_remote
 4635  
 4636      def clear(self, dev):
 4637          dev.run(f"rm -rf {BISYNC_STATE} {AGREED}", check=False)
 4638  
 4639      def first(self, dev):
 4640          """The maintainer-driven first run: the one explicit --resync, or the
 4641          agreement record seeded from what both sides hold."""
 4642          # The folder has to exist on the remote before bisync will look at it
 4643          # (a missing path2 is fatal, exit 7); cloud_backup creates it the same way.
 4644          dev.run(f"rclone mkdir {shlex.quote(self.remote(dev))}", check=False)
 4645          if self.kind == "bisync":
 4646              return self.bisync(dev, "--resync")
 4647          return self.copy_pass(dev)
 4648  
 4649      def run(self, dev, hold=(), dry=False, env="", background=False):
 4650          if self.kind == "bisync":
 4651              flags = "--dry-run" if dry else ""
 4652              if hold:
 4653                  # rclone refuses --files-from beside any other filter, so the
 4654                  # decided set replaces the allowlist for this run; whether
 4655                  # bisync then accepts a changed filter without --resync is
 4656                  # what the item records.
 4657                  dev.write("/tmp/qa-decided.txt", "\n".join(sorted(set(self.p.files) - set(hold))).encode() + b"\n")
 4658                  flags += " --files-from /tmp/qa-decided.txt"
 4659                  return self.bisync(dev, flags, env, background, filters=False)
 4660              return self.bisync(dev, flags, env, background)
 4661          return self.copy_pass(dev, hold, dry, env, background)
 4662  
 4663      def bisync(self, dev, flags, env="", background=False, filters=True):
 4664          cmd = (f"rclone bisync {shlex.quote(self.p.root)} {shlex.quote(self.remote(dev))} "
 4665                 f"{'--filters-file ' + RULES if filters else ''} --conflict-resolve none --resilient --recover "
 4666                 f"--use-json-log -v {self.extra} {flags}")
 4667          self.last_cmd = cmd
 4668          if background:
 4669              dev.run(f"rm -f /tmp/qa-bg.out; ({env} setsid {cmd} >/tmp/qa-bg.out 2>&1 &)")
 4670              return {"rc": None, "out": "", "conflicts": [], "transferred": 0, "moved": []}
 4671          rc, out = run_rc(dev, cmd, env)
 4672          self.record(dev, cmd, rc, out)
 4673          # A conflict is a file bisync queues under a conflict suffix, or a
 4674          # non-zero count of differences -- not every line that mentions the
 4675          # word ("Checking potential conflicts..." is printed on every run).
 4676          # `moved` is every object rclone reports copying, renaming or
 4677          # deleting, so a transfer count has names behind it.
 4678          conflicts, moved, raw = [], [], None
 4679          for line in out.splitlines():
 4680              if not line.startswith("{"):
 4681                  continue
 4682              try:
 4683                  j = json.loads(line)
 4684              except ValueError:
 4685                  continue
 4686              msg = j.get("msg", "")
 4687              if re.search(r"\.conflict\d|[1-9]\d* differences found", msg):
 4688                  conflicts.append(re.sub(r"\x1b\[[0-9;]*m", "", msg).strip())
 4689                  raw = raw or line
 4690              if j.get("object") and re.match(r"(Copied|Moved|Renamed|Deleted|Updated)", msg):
 4691                  moved.append(f"{j['object']}: {msg.split(' (')[0].split(':')[0]}")
 4692          return {"rc": rc, "out": out, "conflicts": conflicts, "transferred": transferred(out), "moved": moved, "raw": raw}
 4693  
 4694      def hashes(self, dev, remote=False):
 4695          """path -> sha256 of every allowlisted file on one side. The remote's
 4696          are hashed after a fetch: the QA WebDAV offers none (#53)."""
 4697          if remote:
 4698              r = shlex.quote(self.remote(dev))
 4699              cmd = (f"rclone lsf -R --files-only --filter-from {RULES} {r} 2>/dev/null | while IFS= read -r f; do "
 4700                     f"printf '%s %s\\n' \"$(rclone cat {r}/\"$f\" 2>/dev/null | sha256sum | cut -c1-64)\" \"$f\"; done")
 4701          else:
 4702              cmd = (f"cd {shlex.quote(self.p.root)} 2>/dev/null && rclone lsf -R --files-only --filter-from {RULES} . "
 4703                     f"2>/dev/null | while IFS= read -r f; do printf '%s %s\\n' \"$(sha256sum \"$f\" | cut -c1-64)\" \"$f\"; done")
 4704          out = dev.run(cmd, check=False)
 4705          return {line[65:]: line[:64] for line in out.splitlines() if len(line) > 65}
 4706  
 4707      def copy_pass(self, dev, hold=(), dry=False, env="", background=False):
 4708          """The stand-in reconciler: identity by sha256 against agreement, then
 4709          decided transfers only. Absences with agreement on record are
 4710          questions, never transfers; an empty side with agreement on record
 4711          refuses the pass (#22 R4)."""
 4712          local, cloud = self.hashes(dev), self.hashes(dev, remote=True)
 4713          try:
 4714              agreed = json.loads(dev.run(f"cat {AGREED} 2>/dev/null || echo {{}}", check=False) or "{}")
 4715          except ValueError:
 4716              agreed = {}
 4717          r = {"rc": 0, "out": "", "conflicts": [], "questions": [], "pushed": [], "fetched": [], "transferred": 0, "moved": []}
 4718          if agreed and (not local or not cloud):
 4719              r["rc"], r["out"] = 1, "refused: a side is empty with agreement on record"
 4720              return r
 4721          for path in sorted(set(local) | set(cloud)):
 4722              if path in hold:
 4723                  continue
 4724              l, c, a = local.get(path), cloud.get(path), agreed.get(path)
 4725              if l == c:
 4726                  agreed[path] = l
 4727              elif l and c:
 4728                  if c == a:
 4729                      r["pushed"].append(path)
 4730                  elif l == a:
 4731                      r["fetched"].append(path)
 4732                  else:
 4733                      r["conflicts"].append(path)
 4734              elif a is None:
 4735                  (r["pushed"] if l else r["fetched"]).append(path)
 4736              else:
 4737                  r["questions"].append(path)
 4738          if dry:
 4739              r["out"] = f"dry-run: push {r['pushed']} fetch {r['fetched']} conflicts {r['conflicts']} questions {r['questions']}"
 4740              return r
 4741          root, remote = shlex.quote(self.p.root), shlex.quote(self.remote(dev))
 4742          cmds = []
 4743          if r["pushed"]:
 4744              dev.write("/tmp/qa-push.txt", "\n".join(r["pushed"]).encode() + b"\n")
 4745              cmds.append(f"rclone copy --files-from /tmp/qa-push.txt --ignore-times {root} {remote}")
 4746          if r["fetched"]:
 4747              dev.write("/tmp/qa-fetch.txt", "\n".join(r["fetched"]).encode() + b"\n")
 4748              cmds.append(f"rclone copy --files-from /tmp/qa-fetch.txt --ignore-times {remote} {root}")
 4749          self.last_cmd = " && ".join(cmds) or "(nothing to transfer)"
 4750          if cmds:
 4751              if background:
 4752                  dev.run(f"rm -f /tmp/qa-bg.out; ({env} setsid sh -c {shlex.quote(' && '.join(cmds))} >/tmp/qa-bg.out 2>&1 &)")
 4753                  r["rc"] = None
 4754                  return r
 4755              r["rc"], r["out"] = run_rc(dev, " && ".join(cmds), env)
 4756              self.record(dev, " && ".join(cmds), r["rc"], r["out"])
 4757          if r["rc"] == 0:
 4758              for path in r["pushed"]:
 4759                  agreed[path] = local[path]
 4760              for path in r["fetched"]:
 4761                  agreed[path] = cloud[path]
 4762          dev.write(AGREED, json.dumps(agreed).encode())
 4763          r["transferred"] = len(r["pushed"]) + len(r["fetched"])
 4764          r["moved"] = [f"{x}: pushed" for x in r["pushed"]] + [f"{x}: fetched" for x in r["fetched"]]
 4765          if r["conflicts"]:
 4766              r["rc"] = r["rc"] or 5
 4767          return r
 4768  
 4769  
 4770  def run_contract(p, kind, args):
 4771      f = 0
 4772      t = Transport(kind, p, args.bisync_flags if kind == "bisync" else "", args.dump)
 4773      p.files = []
 4774  
 4775      def fresh(files):
 4776          """Agreement through the transport itself: a's first run publishes,
 4777          b's first run receives."""
 4778          p.reset()
 4779          t.clear(p.a)
 4780          t.clear(p.b)
 4781          # Ballast: files that never change. A tree of one file makes every
 4782          # change "all files changed", which bisync refuses outright as a
 4783          # safety abort (seen on the first run); a saves tree with one save
 4784          # would hit the same wall, which Gate 11 weighs from this output.
 4785          files = {**{f"saves/Ballast {i}.srm": f"ballast {i}".encode() for i in range(3)}, **files}
 4786          p.files = sorted(files)
 4787          for rel, data in files.items():
 4788              p.a.write(p.path(rel), data)
 4789          ra, rb = t.first(p.a), t.first(p.b)
 4790          wrong = [rel for rel, data in files.items() if not (p.cloud_sha(rel) == sha(data) == p.b.sha(p.path(rel)))]
 4791          if wrong:
 4792              tail = (rb["out"] or ra["out"]).strip().splitlines()[-3:]
 4793              raise Fail(f"the first run under {kind} left {wrong} without agreement (a exit {ra['rc']}, b exit {rb['rc']}): "
 4794                         + " | ".join(tail))
 4795  
 4796      def say(r):
 4797          print(f"          {t.last_cmd}")
 4798          print(f"          exit {r['rc']}, {r['transferred']} transferred, {len(r['conflicts'])} conflict line(s)"
 4799                + (f", questions {r['questions']}" if r.get("questions") else ""))
 4800          for m in r.get("moved", [])[:8]:
 4801              print(f"          moved: {m[:160]}")
 4802          for c in r["conflicts"][:2]:
 4803              print(f"          conflict: {c[:200]}")
 4804          if r.get("raw") and not getattr(say, "shown", False):
 4805              # The shape of one conflict line as bytes, before any parsing
 4806              # trusted it (the #35 futro asked for od -c; repr is the same
 4807              # record in one line).
 4808              say.shown = True
 4809              print(f"          shape: {r['raw'][:400]!r}")
 4810          if r["rc"]:
 4811              # What the transport said went wrong: rclone's own words, the
 4812              # last few, so a FAIL below can be read without a rerun.
 4813              said = []
 4814              for line in r["out"].splitlines():
 4815                  if line.startswith("{"):
 4816                      try:
 4817                          j = json.loads(line)
 4818                      except ValueError:
 4819                          continue
 4820                      if j.get("level") in ("error", "critical", "notice") and "Transferred:" not in j.get("msg", ""):
 4821                          said.append(j.get("msg", "").strip())
 4822                  elif line.strip() and "Transferred:" not in line and "Elapsed time" not in line and "Checks:" not in line:
 4823                      said.append(line.strip())
 4824              for s in said[-3:]:
 4825                  print(f"          > {s[:200]}")
 4826  
 4827      if kind == "bisync":
 4828          print(f"\n    rclone on the guest: {p.a.run('rclone version 2>/dev/null | head -1').strip()}")
 4829  
 4830      def item(n, title):
 4831          t.tag = f"item{n:02d}"
 4832          step(f"#9 item {n} ({kind}) -- {title}")
 4833  
 4834      try:
 4835          item(1, "reports, never resolves")
 4836          rel = "saves/Contract Both.srm"
 4837          v = {"H0": b"H0 agreed under the transport", "HA": b"HA: a's offline edit", "HB": b"HB: b's published edit"}
 4838          fresh({rel: v["H0"]})
 4839          p.b.write(p.path(rel), v["HB"])
 4840          say(t.run(p.b))
 4841          p.a.write(p.path(rel), v["HA"])
 4842          touch_offset(p.a, p.path(rel), 3600)
 4843          dry = t.run(p.a, dry=True)
 4844          guard = "conflict" in dry["out"].lower() or bool(dry["conflicts"])
 4845          # A reconciler refuses the wet run when the guard fires (item 2); the
 4846          # wet run is made only when it does not, so the outcome is recorded.
 4847          r = dry if guard else t.run(p.a)
 4848          say(r)
 4849          f += not check(guard or bool(r["conflicts"]), "the both-changed pair was reported in a parseable form",
 4850                         f"no conflict reported (exit {r['rc']})")
 4851          f += not check(p.cloud_sha(rel) == sha(v["HB"]) and p.a.sha(p.path(rel)) == sha(v["HA"]),
 4852                         "and neither file changed",
 4853                         f"a file changed: cloud {name_of(p.cloud_sha(rel), v)}, device {name_of(p.a.sha(p.path(rel)), v)}")
 4854  
 4855          item(2, "no renames on the saves tree")
 4856          f += not check(guard, "the dry-run guard fired on the constructed conflict",
 4857                         "the dry-run guard did not fire on a constructed conflict")
 4858          renamed = [x for x in backend_files(p.spath) + p.a.run(f"ls -R {shlex.quote(p.root)}").split() if "conflict" in x.lower()]
 4859          f += not check(not renamed, "no file on either side was renamed", f"RENAMED: {renamed}")
 4860  
 4861          item(3, "decided transfers only")
 4862          u1, u2 = "saves/Decided.srm", "saves/Held.srm"
 4863          fresh({u1: b"u1 v0", u2: b"u2 v0"})
 4864          p.a.write(p.path(u1), b"u1 v1 decided")
 4865          p.a.write(p.path(u2), b"u2 v1 held back by the reconciler")
 4866          r = t.run(p.a, hold={u2})
 4867          say(r)
 4868          f += not check(p.cloud_sha(u1) == sha(b"u1 v1 decided"), "the decided unit moved", "the decided unit did not move")
 4869          f += not check(p.cloud_sha(u2) == sha(b"u2 v0"), "the held unit did not", "THE HELD UNIT WAS TRANSFERRED")
 4870  
 4871          item(4, "hashless backend: an equal-size, equal-mtime change")
 4872          rel = "saves/Same Size Contract.srm"
 4873          one, two = b"contract-version-one", b"contract-version-two"
 4874          fresh({rel: one})
 4875          q = shlex.quote(p.path(rel))
 4876          p.b.run(f"cp -p {q} {q}.ref")
 4877          p.b.write(p.path(rel), two)
 4878          p.b.run(f"touch -r {q}.ref {q}; rm -f {q}.ref; sync")
 4879          say(t.run(p.b))
 4880          say(t.run(p.a))
 4881          f += not check(p.a.sha(p.path(rel)) == sha(two), "the byte change reached a",
 4882                         "an equal-size, equal-mtime change was treated as identical")
 4883  
 4884          item(5, "external resolution without --resync")
 4885          rel = "saves/Resolved Outside.srm"
 4886          v = {"H0": b"H0 resolved-outside", "HA": b"HA: a's edit", "HB": b"HB: b's edit, the winner"}
 4887          fresh({rel: v["H0"]})
 4888          p.b.write(p.path(rel), v["HB"])
 4889          t.run(p.b)
 4890          p.a.write(p.path(rel), v["HA"])
 4891          touch_offset(p.a, p.path(rel), 3600)
 4892          dry = t.run(p.a, dry=True)
 4893          if not ("conflict" in dry["out"].lower() or dry["conflicts"]):
 4894              t.run(p.a)
 4895          # The wizard installs the winner on a and pushes it (a decided transfer).
 4896          p.a.write(p.path(rel), v["HB"])
 4897          rem = shlex.quote(t.remote(p.a) + "/" + rel)
 4898          run_rc(p.a, f"rclone copyto --ignore-times {shlex.quote(p.path(rel))} {rem}")
 4899          if kind == "copy":
 4900              agreed = json.loads(p.a.run(f"cat {AGREED} 2>/dev/null || echo {{}}", check=False) or "{}")
 4901              agreed[rel] = sha(v["HB"])
 4902              p.a.write(AGREED, json.dumps(agreed).encode())
 4903          r = t.run(p.a)
 4904          say(r)
 4905          f += not check(not r["conflicts"] and not r["moved"] and (r["rc"] or 0) == 0,
 4906                         "the next run neither re-flagged nor re-transferred the pair",
 4907                         f"after an outside resolution: exit {r['rc']}, {len(r['moved'])} object(s) moved, {len(r['conflicts'])} conflict line(s)")
 4908  
 4909          item(6, "interruption: killed mid-transfer, completed by the next run")
 4910          big = {f"saves/Big {i}.srm": os.urandom(98304) for i in range(4)}
 4911          fresh({"saves/Seed.srm": b"seed"})
 4912          for rel, data in big.items():
 4913              p.a.write(p.path(rel), data)
 4914          t.run(p.a, env="RCLONE_BWLIMIT=32k RCLONE_TRANSFERS=1", background=True)
 4915          time.sleep(4)
 4916          p.a.run("pkill -9 -x rclone; sleep 1; true", check=False)
 4917          landed = [rel for rel, data in big.items() if p.cloud_sha(rel) == sha(data)]
 4918          print(f"          killed after {len(landed)} of {len(big)} had landed")
 4919          r = t.run(p.a)
 4920          say(r)
 4921          if r["rc"] and "lock file" in r["out"]:
 4922              # bisync leaves its lock behind after a kill and refuses every
 4923              # later run; a reconciler would clear it once no bisync process
 4924              # remains. Whether the run then completes is measured too.
 4925              print("          the killed run's lock was left behind; cleared, and the next run tried again:")
 4926              p.a.run(f"pgrep -x rclone >/dev/null || rm -f {BISYNC_STATE}/*.lck", check=False)
 4927              r = t.run(p.a)
 4928              say(r)
 4929          done = [rel for rel, data in big.items() if p.cloud_sha(rel) == sha(data)]
 4930          f += not check(len(done) == len(big) and (r["rc"] or 0) == 0, "the next run completed the transfer, nothing lost",
 4931                         f"{len(done)}/{len(big)} in the cloud after the next run (exit {r['rc']})")
 4932          f += not check("resync" not in r["out"].lower(), "and did not ask for --resync",
 4933                         "the next run demanded --resync after an interruption")
 4934  
 4935          item(7, "renumber: same hash, new slot")
 4936          s = {"S1": os.urandom(3001), "S2": os.urandom(3002), "S3": os.urandom(3003)}
 4937          st = lambda n: f"savestates/Contract.state{n}"
 4938          fresh({st(1): s["S1"], st(2): s["S2"], st(3): s["S3"]})
 4939          p.a.run(f"rm -f {shlex.quote(p.path(st(2)))}; mv {shlex.quote(p.path(st(3)))} {shlex.quote(p.path(st(2)))}")
 4940          say(t.run(p.a))
 4941          say(t.run(p.b))
 4942          out = p.b.run(f"cd {shlex.quote(p.root)} && sha256sum savestates/* 2>/dev/null || true")
 4943          on_b = sorted(name_of(line.split()[0], s) for line in out.splitlines() if line.strip())
 4944          cloud = sorted(name_of(sha(backend_bytes(f"{p.spath}/{x}") or b""), s) for x in backend_files(p.spath) if x.startswith("savestates/"))
 4945          print(f"          b holds {on_b}; the cloud holds {cloud}")
 4946          f += not check("S1" in on_b and "S3" in on_b and "S1" in cloud and "S3" in cloud, "no surviving version was lost",
 4947                         f"a surviving version is missing: b {on_b}, cloud {cloud}")
 4948          f += not check(on_b.count("S3") == 1 and cloud.count("S3") == 1, "the moved version exists once on each side",
 4949                         f"the moved version is duplicated: b {on_b}, cloud {cloud}")
 4950  
 4951          item(8, "absence never deletes without the reconciler's word")
 4952          rel = "saves/Absent Root.srm"
 4953          fresh({rel: b"kept in the cloud"})
 4954          q = shlex.quote(p.root)
 4955          p.a.run(f"mv {q} {q}.away")
 4956          r = t.run(p.a)
 4957          say(r)
 4958          p.a.run(f"rm -rf {q}; mv {q}.away {q}")
 4959          f += not check(p.cloud_sha(rel) == sha(b"kept in the cloud"), "an unmounted root deleted nothing in the cloud",
 4960                         "AN UNMOUNTED ROOT DELETED THE CLOUD'S COPY")
 4961          f += not check((r["rc"] or 0) != 0, f"the run refused (exit {r['rc']})", "the run did not refuse an unmounted root")
 4962  
 4963          item(9, "budget: a full pass with nothing changed")
 4964          fresh({"saves/Idle.srm": b"idle"})
 4965          # Every rclone the pass spawns is counted -- the transport's and the
 4966          # stand-in classifier's listings and fetches alike -- by putting the
 4967          # shim first on PATH for every command of the item, not only the
 4968          # transfer. A `cat` is a download.
 4969          p.a.run("mkdir -p /tmp/qa-shim; printf '#!/bin/sh\\necho \"$@\" >> /tmp/qa-spawns\\nexec /usr/bin/rclone \"$@\"\\n' > /tmp/qa-shim/rclone; "
 4970                  "chmod +x /tmp/qa-shim/rclone; rm -f /tmp/qa-spawns")
 4971          prev_prefix = p.a.path_prefix
 4972          p.a.path_prefix = "/tmp/qa-shim" + (f":{prev_prefix}" if prev_prefix else "")
 4973          t0 = time.time()
 4974          try:
 4975              r = t.run(p.a)
 4976          finally:
 4977              p.a.path_prefix = prev_prefix
 4978          secs = time.time() - t0
 4979          spawned = p.a.run("cat /tmp/qa-spawns 2>/dev/null || true").splitlines()
 4980          downloads = sum(1 for s in spawned if s.split()[:1] == ["cat"])
 4981          p.a.run("rm -rf /tmp/qa-shim /tmp/qa-spawns")
 4982          say(r)
 4983          print(f"          {len(spawned)} rclone spawn(s) ({downloads} download(s)), {secs:.1f} s on the guest (a VM, not the H700)")
 4984          f += not check(not r["moved"] and (r["rc"] or 0) == 0, "nothing transferred",
 4985                         f"an idle pass moved {len(r['moved'])} object(s)")
 4986          # --download-hash and the like report hash downloads in the same
 4987          # Transferred: total; that is budget, not a copy, and it is recorded.
 4988          if r["transferred"] and not r["moved"]:
 4989              print(f"          {r['transferred']} download(s) for hashing on an idle pass -- the whole tree, every pass")
 4990  
 4991          item(10, "single authority: the transport's own state is not the agreement")
 4992          rel = "saves/Authority.srm"
 4993          fresh({rel: b"agreed"})
 4994          p.a.run(f"rm -rf {BISYNC_STATE}")
 4995          r = t.run(p.a)
 4996          say(r)
 4997          f += not check((r["rc"] or 0) == 0 and "resync" not in r["out"].lower() and not r["moved"],
 4998                         "with the transport's listings gone the pass still ran from agreement alone",
 4999                         f"without its own listings the transport could not run (exit {r['rc']}; resync demanded: {'resync' in r['out'].lower()})")
 5000      except Fail as e:
 5001          f += 1
 5002          print(f"    FAIL  {e}")
 5003      finally:
 5004          # The transport's own state -- bisync's listings, the stand-in's
 5005          # agreement record -- leaves with the run, on both guests.
 5006          t.clear(p.a)
 5007          t.clear(p.b)
 5008      return f
 5009  
 5010  
 5011  # ===========================================================================
 5012  # #103: the network goes away mid-run -- one device, the QA endpoint, and
 5013  # the serial console that can cut the device's link
 5014  # ===========================================================================
 5015  #
 5016  # What #102 exposed is a failure mode nothing bounds: the link dropping
 5017  # *during* a cloud operation. The scripts probe reachability with short
 5018  # rclone timeouts and then run the copy itself on RCLONEOPTS, which sets
 5019  # none -- rclone's defaults are 60 s to connect, 5 min of idle I/O, three
 5020  # retries and ten low-level retries -- and the RG SP's startup sync sat on a
 5021  # dead connection with the launch gate held (#101). Each cell here starts an
 5022  # operation, waits for the phase it names, cuts the guest's link, restores it
 5023  # after --link-restore-after seconds (40), and asserts what a bounded
 5024  # operation must do: end within LINK_BOUND seconds of the cut with an honest
 5025  # exit (69, the no-network sentinel, or a plain failure -- never 0, never
 5026  # 75), leave no partial file and no truncated one on the receiving side,
 5027  # stamp the failure or nothing (never 0), keep the settings upload marker
 5028  # unless the archive completed, and complete on a plain re-run once the link
 5029  # is back. Time-to-exit is read in the guest's own monotonic clock: the
 5030  # detached wrapper writes `$? <uptime>` when the operation ends, and the cut
 5031  # records the uptime it happened at.
 5032  #
 5033  # Two channels, because the cut kills SSH. The operation is started detached
 5034  # over SSH (setsid nohup, stdout and stderr to a file, the exit code to
 5035  # another), the cut and the restore go over the serial console -- `ip link
 5036  # set eth0 down` / `up`, tools/vm-serial -- and the result is read over SSH
 5037  # once the link is back. A real handheld has no serial console, so these
 5038  # cells are skipped, with a line saying so, when the console is not there.
 5039  #
 5040  # Measured on the GENERIC_X64 guest (2026-09-09, build d574edf975, NM-managed
 5041  # eth0, the WebDAV endpoint throttled to 200k): after `ip link set eth0
 5042  # down` the routes are gone at once, the IPv4 address stays until
 5043  # NetworkManager notices and flushes it (~8 s, state `unavailable`), and an
 5044  # established TCP connection stalls -- it is not reset. After `up` the
 5045  # address, the default route and a ping to the endpoint are back within a
 5046  # second. A fresh connection on the dead link fails in 20 ms (`network is
 5047  # unreachable`; rclone does not retry it). So the hang lives in the transfer
 5048  # that was in flight: TCP retransmits on its doubling schedule, lands the
 5049  # moment the link is back (~51 s after a cut when the outage is 40 s), and an
 5050  # unbounded rclone then *completes*, exit 0, some 50 s after the cut. That is
 5051  # what an unbounded run looks like in these cells with the default outage:
 5052  # not a hang past the bound but a success reported for a run that waited the
 5053  # outage out. `--link-restore-after 120` makes the same run overshoot the
 5054  # bound (TCP's next retransmit is at ~205 s), which is #102's shape. Either
 5055  # way a bounded run ends with the link still down and exits 69.
 5056  #
 5057  # That is WebDAV, whose rclone backend does not retry a dial the dead link
 5058  # refuses. On s3 it does: --low-level-retries goes to the AWS SDK as its
 5059  # attempt count, with the SDK's exponential backoff between attempts, and no
 5060  # timeout covers the backoff (cloud_backup's own note beside
 5061  # RCLONE_LIST_OPTS: 230 s at ten attempts). LINK5 on MinIO behind the
 5062  # throttle proxy (2026-09-13, build 519f40aa0c, rclone 1.75.0, guest d):
 5063  # the cut PUT died when the link came back (8.4 of 12 MiB delivered; MinIO
 5064  # discarded it), the next attempt re-dialled within 2-6 s and uploaded the
 5065  # whole archive, and the deliberate `cloud_backup --system-only` exited 0
 5066  # -- 88.8 s after a 40 s cut, 163.6 s after a 120 s cut, past the bound,
 5067  # with last-settings-backup recording success. The FAILs that produces are
 5068  # the finding, not a harness fault; the automatic path is unaffected, its
 5069  # busybox timeout ceiling holding on every backend.
 5070  #
 5071  # The endpoint must be throttled (CLOUD_QA_BWLIMIT), or nine MiB cross the
 5072  # loopback before the poll can see the transfer start; the cells refuse an
 5073  # unthrottled one rather than report "ended before the cut" seven times. The
 5074  # server's bwlimit is a token bucket with a 4 MiB burst, so three 3 MiB files
 5075  # spend about 25 s in flight. On WebDAV that bucket is rclone serve's own; on
 5076  # s3 it is the proxy cloud-test-backend puts in front of MinIO (which has no
 5077  # such knob), built to the same shape, so the figures hold on both. The other
 5078  # three backends cannot be throttled. The two listing-bound cells (a compare with
 5079  # everything already in the cloud; the picker scan) run rclone under
 5080  # RCLONE_TPSLIMIT=2 -- two HTTP transactions a second, a stand-in for a
 5081  # provider whose listing is rate-limited -- because this endpoint lists
 5082  # twenty-five directories in well under a second and the cut would land
 5083  # after the compare had finished. The environment variable reaches rclone
 5084  # through the script under test unchanged; nothing in the scripts is edited.
 5085  
 5086  LINK_DIR = "/tmp/qa-link"       # on the device: the detached run's out, rc and pid
 5087  LINK_MIB = 3                    # each transferred fixture file
 5088  LINK_FILES = 3                  # per transfer cell: 9 MiB, ~25 s in flight at 200k after the 4 MiB burst
 5089  LINK_BOUND = 90                 # seconds after the cut by which the run must have ended
 5090  LINK_HANG = 360                 # seconds after the cut before the run is called hung
 5091  LINK_GIVE_UP = 600              # after the hang verdict, how much longer it may take to finish before it is killed
 5092  LINK_TPS = 2                    # RCLONE_TPSLIMIT for the listing-bound cells
 5093  LINK_STAMPS = ("last-backup", "last-restore", "last-settings-backup", "last-settings-restore",
 5094                 "last-content-backup", "last-content-restore", "last-content-match")
 5095  LINK_MARKER_FILE = re.compile(r"^\s*\*\s+\S.*?:\s*\d+% /", re.M)   # rclone's per-file progress line
 5096  LINK_MARKER_CHECKS = re.compile(r"^Checks:\s+\d+ / \d+", re.M)       # the compare phase, in the stats block
 5097  LINK_FILE_PERCENT = re.compile(r"^\s*\*\s+\S.*?:\s*(\d+)% /", re.M)   # the per-file line's percentage
 5098  # The deliberate run's stall ceiling ending an rclone (cloud_backup / cloud_restore
 5099  # bounded_rclone, D-CLOUD-127): the wrapper's own log line.
 5100  LINK_STALL_ENDED = re.compile(r"rclone \w+ made no progress for \d+s and was ended \(it returned \d+\); reporting 124")
 5101  
 5102  
 5103  def last_file_percent(out):
 5104      """The percentage on rclone's last per-file progress line in `out`, or -1
 5105      when it printed none."""
 5106      found = LINK_FILE_PERCENT.findall(out)
 5107      return int(found[-1]) if found else -1
 5108  
 5109  
 5110  def backend_throttled():
 5111      """Whether the endpoint runs with --bwlimit. Read off the server's own
 5112      command line (its pid is beside its data directory), not off an
 5113      environment variable this process may or may not share with the one
 5114      that started it. On WebDAV that server is rclone serve; on s3 it is the
 5115      token-bucket proxy cloud-test-backend puts in front of MinIO, started
 5116      with the same flag and leaving its pid in the same place. The other
 5117      three have no throttle, so they never pass."""
 5118      kind = backend("backend").strip()
 5119      if kind not in ("webdav", "s3"):
 5120          return False
 5121      state = os.path.dirname(backend("path").strip())
 5122      try:
 5123          pid = open(os.path.join(state, f"{kind}.pid")).read().strip()
 5124          return "--bwlimit" in open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="replace")
 5125      except OSError:
 5126          return False
 5127  
 5128  
 5129  class Link:
 5130      """One device, the QA endpoint, and the console that can cut the link."""
 5131  
 5132      def __init__(self, dev, serial, root, remote, settings, args):
 5133          self.dev, self.serial, self.root, self.remote, self.settings, self.args = dev, serial, root, remote, settings, args
 5134          self.restore_after = args.link_restore_after
 5135          self.saves_remote = settings.get("SAVES_REMOTE") or settings.get("SYNCPATH")
 5136          self.settings_remote = settings.get("SETTINGS_REMOTE") or settings.get("SYNCPATH_BACKUP")
 5137          self.content_remote = settings.get("CONTENT_REMOTE") or settings.get("CONTENTPATH")
 5138          # The interface that carries the default route -- eth0 on the VM,
 5139          # wlan0 on a handheld -- read from the guest rather than assumed.
 5140          self.iface = dev.run("ip -4 route show default 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i==\"dev\") print $(i+1)}' | head -1").strip()
 5141          if not self.iface:
 5142              raise Fail("the device has no default route to cut")
 5143          m = re.search(r"(?:url|endpoint)\s*=\s*\w+://([^/\s]+)", backend("rclone-conf"))
 5144          if not m:
 5145              raise Fail("cannot read the endpoint's host:port from the backend's rclone stanza")
 5146          self.hostport = m.group(1)
 5147          self.host_ip = self.hostport.split(":")[0]
 5148          self.t_cut = None
 5149  
 5150      # -- the guard: the console must belong to the device on --host --------
 5151      def assert_same_guest(self):
 5152          nonce = hashlib.sha256(os.urandom(16)).hexdigest()[:16]
 5153          self.dev.run(f"echo {nonce} > /tmp/qa-link-nonce")
 5154          seen = self.serial.run("cat /tmp/qa-link-nonce 2>/dev/null").strip()
 5155          self.dev.run("rm -f /tmp/qa-link-nonce", check=False)
 5156          if seen != nonce:
 5157              raise Fail(f"the serial console at {self.serial.socket} is not the device on --host "
 5158                         f"(wrote {nonce} over ssh, read {seen or 'nothing'} over serial); refusing to cut a link")
 5159  
 5160      # -- planting ------------------------------------------------------------
 5161      def big(self, name):
 5162          return os.urandom(LINK_MIB * 1024 * 1024)
 5163  
 5164      def plant_device(self, base, files):
 5165          for rel, data in files.items():
 5166              self.dev.write(f"{base}/{rel}", data)
 5167  
 5168      def plant_cloud(self, files, endpoint_path):
 5169          stage = subprocess.run(["mktemp", "-d"], capture_output=True, text=True).stdout.strip()
 5170          for rel, data in files.items():
 5171              path = os.path.join(stage, rel)
 5172              os.makedirs(os.path.dirname(path), exist_ok=True)
 5173              open(path, "wb").write(data)
 5174          backend("put", stage, endpoint_path)
 5175          subprocess.run(["rm", "-rf", stage])
 5176  
 5177      def content_dir(self):
 5178          """/storage/roms/<CONTENT_DIR>, which the harness owns only if empty."""
 5179          croot = f"/storage/roms/{CONTENT_DIR}"
 5180          existing = self.dev.run(f"find {shlex.quote(croot)} -type f 2>/dev/null | head -3 || true").strip()
 5181          if existing and not self.args.real_roms:
 5182              raise Fail(f"{croot} holds files ({existing.splitlines()[0]} ...); refusing to use it as a fixture")
 5183          self.dev.run(f"rm -rf {shlex.quote(croot)}; mkdir -p {shlex.quote(croot)}")
 5184          return croot
 5185  
 5186      def reset(self):
 5187          self.dev.run(f"rm -rf {shlex.quote(self.root)}; mkdir -p {shlex.quote(self.root)}; "
 5188                       f"rm -rf /storage/roms/{shlex.quote(CONTENT_DIR)} {LINK_DIR}", check=False)
 5189          backend("reset")
 5190  
 5191      # -- the detached run ----------------------------------------------------
 5192      def start(self, cmd, env=""):
 5193          self.dev.run(f"rm -rf {LINK_DIR}; mkdir -p {LINK_DIR}")
 5194          inner = f"echo $$ > {LINK_DIR}/pid; {env} {cmd}; echo $? $(cut -d' ' -f1 /proc/uptime) > {LINK_DIR}/rc"
 5195          self.dev.run(f"setsid nohup sh -c {shlex.quote(inner)} >{LINK_DIR}/out 2>&1 &")
 5196  
 5197      def status(self):
 5198          """(out, rc line or '', established connections to the endpoint)."""
 5199          out = self.dev.run(f"cat {LINK_DIR}/out 2>/dev/null; printf '\\n@@RC %s\\n' \"$(cat {LINK_DIR}/rc 2>/dev/null)\"; "
 5200                             f"printf '@@CONN %s\\n' \"$(netstat -tn 2>/dev/null | grep -c '{self.hostport} .*ESTABLISHED')\"",
 5201                             check=False)
 5202          body, _, tail = out.partition("\n@@RC ")
 5203          rc, _, conn = tail.partition("\n@@CONN ")
 5204          return body, rc.strip(), int(conn.strip() or 0)
 5205  
 5206      def wait_marker(self, marker, timeout=120):
 5207          """Until the run prints the marker (a regex) -- or, for marker None,
 5208          holds a connection to the endpoint, which is the only sign a scan
 5209          gives before it ends. (False, out) when the run ended first."""
 5210          t0 = time.time()
 5211          while time.time() - t0 < timeout:
 5212              body, rc, conn = self.status()
 5213              if marker is not None and marker.search(body):
 5214                  return True, body
 5215              if marker is None and conn > 0:
 5216                  return True, body
 5217              if rc:
 5218                  return False, body
 5219              time.sleep(0.3)
 5220          raise Fail(f"no marker in {timeout}s: {body.strip().splitlines()[-1][:120] if body.strip() else 'no output'}")
 5221  
 5222      def rc_line(self, text):
 5223          parts = text.strip().split()
 5224          return parts if len(parts) == 2 and parts[0].lstrip("-").isdigit() else None
 5225  
 5226      # -- the cut and the restore, over serial --------------------------------
 5227      def cut(self):
 5228          self.dev.disconnect()
 5229          out = self.serial.run(f"ip link set {self.iface} down; cut -d' ' -f1 /proc/uptime")
 5230          self.t_cut = time.time()
 5231          return float(out.split()[-1])
 5232  
 5233      def restore(self):
 5234          out = self.serial.run(f"ip link set {self.iface} up; cut -d' ' -f1 /proc/uptime")
 5235          up = float(out.split()[-1])
 5236          t = time.time()
 5237          test = (f"ip -4 -o addr show {self.iface} | grep -q 'inet ' && ip -4 route show default | grep -q . "
 5238                  f"&& ping -c1 -W1 {self.host_ip} >/dev/null 2>&1 && echo NETOK")
 5239          while time.time() - t < 90:
 5240              if "NETOK" in self.serial.run(test):
 5241                  return up, time.time() - t
 5242              time.sleep(1)
 5243          raise Fail(f"{self.iface} did not regain an address, a default route and the endpoint within 90 s of `ip link set up`")
 5244  
 5245      def wait_exit(self, cut_up):
 5246          """The run's `rc uptime` line: polled over serial while the link is
 5247          down, over ssh after it is restored. None if it has not ended
 5248          LINK_HANG seconds after the cut."""
 5249          seen = None
 5250          polls = 0
 5251          while time.time() - self.t_cut < self.restore_after:
 5252              time.sleep(min(5, max(0.5, self.restore_after - (time.time() - self.t_cut))))
 5253              polls += 1
 5254              if polls <= 2:
 5255                  # The first poll proves the cut took -- a guard that cannot
 5256                  # tell eth0 from the wrong interface has not cut anything --
 5257                  # and the second describes the state NetworkManager leaves
 5258                  # once it has noticed (it flushes the address ~8 s in).
 5259                  st = self.serial.run(f"ip -4 route show default 2>/dev/null | grep -c .; "
 5260                                       f"nmcli -t -f DEVICE,STATE dev 2>/dev/null | grep '^{self.iface}:' | cut -d: -f2; "
 5261                                       f"ip -4 -o addr show {self.iface} | grep -c 'inet '").split()
 5262                  routes, nm, addrs = (st + ["?", "?", "?"])[:3]
 5263                  if polls == 1 and routes != "0":
 5264                      raise Fail(f"the cut did not take: {routes} default route(s) still present after `ip link set {self.iface} down`")
 5265                  if polls == 2:
 5266                      print(f"          {time.time() - self.t_cut:.0f}s into the outage: default route gone; NetworkManager says "
 5267                            f"{nm}; {'an address still' if addrs not in ('0', '?') else 'no address'} on {self.iface}")
 5268              r = self.rc_line(self.serial.run(f"cat {LINK_DIR}/rc 2>/dev/null"))
 5269              if r and seen is None:
 5270                  seen = r
 5271                  print(f"          ended {float(r[1]) - cut_up:.1f}s after the cut, with the link still down (rc {r[0]})")
 5272          rest_up, back = self.restore()
 5273          print(f"          link restored {rest_up - cut_up:.1f}s after the cut; address, default route and the endpoint back in {back:.1f}s")
 5274          if seen:
 5275              return seen
 5276          deadline = self.t_cut + LINK_HANG
 5277          while time.time() < deadline:
 5278              r = self.rc_line(self.dev.run(f"cat {LINK_DIR}/rc 2>/dev/null", check=False))
 5279              if r:
 5280                  return r
 5281              time.sleep(2)
 5282          return None
 5283  
 5284      def finish_or_kill(self):
 5285          """After a hang verdict: the link is back, so let the run finish --
 5286          the VM has to be clean for the next cell -- and kill its process
 5287          group only when even that does not end it."""
 5288          deadline = time.time() + LINK_GIVE_UP
 5289          while time.time() < deadline:
 5290              r = self.rc_line(self.dev.run(f"cat {LINK_DIR}/rc 2>/dev/null", check=False))
 5291              if r:
 5292                  print(f"          (it finished on its own {time.time() - self.t_cut:.0f}s after the cut, rc {r[0]})")
 5293                  return r
 5294              time.sleep(5)
 5295          pid = self.dev.run(f"cat {LINK_DIR}/pid 2>/dev/null", check=False).strip()
 5296          self.dev.run(f"kill -TERM -- -{pid} 2>/dev/null; sleep 2; kill -KILL -- -{pid} 2>/dev/null; true", check=False)
 5297          print(f"          (killed process group {pid} {time.time() - self.t_cut:.0f}s after the cut; it never ended)")
 5298          return None
 5299  
 5300      # -- what the receiving side holds ----------------------------------------
 5301      def fingerprint(self, side):
 5302          """{relpath: (size, sha256)} on the receiving side. Content, not
 5303          size: rclone's local backend -- the QA server's store -- preallocates
 5304          a file to its full length when the upload starts, so a PUT whose tail
 5305          never arrived reads as whole by size (LINK5, 2026-09-09)."""
 5306          kind, where = side
 5307          if kind == "cloud":
 5308              out = {}
 5309              for rel, size in backend_sizes(where).items():
 5310                  data = backend_bytes(f"{where}/{rel}")
 5311                  out[rel] = (size, sha(data) if data is not None else None)
 5312              return out
 5313          raw = self.dev.run(f"cd {shlex.quote(where)} 2>/dev/null && find . -type f | while read -r f; do "
 5314                             f"printf '%s %s %s\n' \"$(stat -c %s \"$f\")\" \"$(sha256sum \"$f\" | cut -d' ' -f1)\" \"$f\"; done; true",
 5315                             check=False)
 5316          out = {}
 5317          for line in raw.splitlines():
 5318              parts = line.split(" ", 2)
 5319              if len(parts) == 3 and parts[0].isdigit() and parts[2].startswith("./"):
 5320                  out[parts[2][2:]] = (int(parts[0]), parts[1])
 5321          return out
 5322  
 5323      def settle(self, side):
 5324          """The receiving side's fingerprints once they have stopped changing:
 5325          the server keeps taking bytes already in the buffers after the client
 5326          is gone, and a comparison taken mid-drain reads as truncation."""
 5327          last = self.fingerprint(side)
 5328          for _ in range(40):
 5329              time.sleep(3)
 5330              now = self.fingerprint(side)
 5331              if now == last:
 5332                  return now
 5333              last = now
 5334          return last
 5335  
 5336      def endpoint_quiet(self, limit=180):
 5337          """Wait until the QA WebDAV server has finished taking the cut run's
 5338          upload. The guest forgets the socket the moment rclone gives up, but
 5339          QEMU's user-mode stack has already accepted the whole body and keeps
 5340          feeding it to the server, which holds the destination file open and
 5341          writes it to disk at the throttled rate -- and returns `423 Locked`
 5342          to any PUT of that path meanwhile (proven on the host, 2026-09-09:
 5343          fd open and one CLOSE-WAIT socket for the ~60 s a 16 MiB body takes at
 5344          200k, PUT of the same name 423 throughout, 201 the instant the fd
 5345          closed). So the ESTABLISHED socket clearing is not enough; wait for
 5346          the server to hold no open fd under its data directory. WebDAV only
 5347          -- a real provider resets an aborted PUT and has no such drain, and
 5348          the check reads a local rclone serve's /proc. On s3 the throttle
 5349          proxy drains the same buffer into MinIO, but the cut PUT ended when
 5350          the link came back (the guest's RST reached slirp) and the atomic
 5351          PUT discarded it, so nothing is held (LINK5, 2026-09-13). Returns
 5352          how long it took."""
 5353          if backend("backend").strip() != "webdav":
 5354              return 0.0
 5355          data = backend("path").strip()
 5356          state = os.path.dirname(data)
 5357          try:
 5358              pid = open(os.path.join(state, "webdav.pid")).read().strip()
 5359          except OSError:
 5360              pid = ""
 5361          port = self.hostport.rsplit(":", 1)[-1]
 5362          t = time.time()
 5363          while time.time() - t < limit:
 5364              socks = subprocess.run(["ss", "-Htn", f"( sport = :{port} )"], capture_output=True, text=True).stdout
 5365              busy = any(st in socks for st in ("ESTAB", "CLOSE-WAIT"))
 5366              fds = "0"
 5367              if pid:
 5368                  fds = subprocess.run(["bash", "-c", f"ls -l /proc/{pid}/fd 2>/dev/null | grep -c {shlex.quote(data)} || true"],
 5369                                       capture_output=True, text=True).stdout.strip()
 5370              if not busy and fds in ("0", ""):
 5371                  break
 5372              time.sleep(2)
 5373          return time.time() - t
 5374  
 5375      def stamps(self):
 5376          out = self.dev.run(f"cd {CACHE} 2>/dev/null && for s in {' '.join(LINK_STAMPS)} settings-backup.uploaded; do "
 5377                             f"printf '%s=%s\\n' \"$s\" \"$(cat $s 2>/dev/null)\"; done; true", check=False)
 5378          return dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
 5379  
 5380      # -- one cell -------------------------------------------------------------
 5381      def keep(self, key, rerun_out):
 5382          """Keep the cell's evidence: the detached run's out/rc/pid move to
 5383          /tmp/qa-link-<KEY>/ on the guest (reset() wipes /tmp/qa-link for the
 5384          next cell), the re-run's output beside them, and copies of both under
 5385          --dump on the host when it is given. A FAIL with no output file is a
 5386          FAIL nobody can read."""
 5387          keep_dir = f"{LINK_DIR}-{key}"
 5388          self.dev.write(f"{keep_dir}/rerun.out", rerun_out.encode())
 5389          self.dev.run(f"cp {LINK_DIR}/out {LINK_DIR}/rc {LINK_DIR}/pid {keep_dir}/ 2>/dev/null; true", check=False)
 5390          where = f"{keep_dir}/ on the guest"
 5391          if self.args.dump:
 5392              host_dir = os.path.join(self.args.dump, key)
 5393              os.makedirs(host_dir, exist_ok=True)
 5394              for name in ("out", "rc", "rerun.out"):
 5395                  data = self.dev.run(f"cat {keep_dir}/{name} 2>/dev/null; true", check=False)
 5396                  open(os.path.join(host_dir, name), "w").write(data)
 5397              where += f", {host_dir}/ here"
 5398          print(f"          outputs kept: {where}")
 5399  
 5400      def exercise(self, key, cmd, marker, receiving, sources, stamps, env="", rerun=None, verify=None, upload_marker=False, strict_retry=False):
 5401          """Start `cmd` detached, cut at `marker`, restore after
 5402          restore_after seconds, and assert the contract. `receiving` is
 5403          ("cloud", endpoint path) or ("device", directory) -- where the
 5404          operation writes; `sources` maps each file it moves to (size, sha256);
 5405          `stamps` names the last-* files it may write. `verify(out)` replaces
 5406          the file comparison after the re-run for an operation that moves
 5407          nothing (the scan). Returns the number of failed checks."""
 5408          f = 0
 5409          before = self.stamps()
 5410          self.start(cmd, env)
 5411          landed, out = self.wait_marker(marker)
 5412          if not landed:
 5413              rc = self.rc_line(self.status()[1])
 5414              return f + (not check(False, "", f"the run ended (rc {rc[0] if rc else '?'}) before the cut could land; "
 5415                                              f"last line: {out.strip().splitlines()[-1][:100] if out.strip() else 'none'}"))
 5416          cut_up = self.cut()
 5417          where = out.strip().splitlines()[-1].strip()[:90] if out.strip() else "no output yet"
 5418          print(f"          cut {self.iface} at guest uptime {cut_up:.2f} ({time.strftime('%H:%M:%S')}); last line: {where!r}")
 5419          r = self.wait_exit(cut_up)
 5420          hung = r is None
 5421          if hung:
 5422              f += not check(False, "", f"HANG: the run had not ended {LINK_HANG}s after the cut (bound {LINK_BOUND}s); "
 5423                                        f"link restored {self.restore_after}s after it")
 5424              r = self.finish_or_kill()
 5425          if r:
 5426              rc, tte = int(r[0]), float(r[1]) - cut_up
 5427              if not hung:
 5428                  why = ("" if tte <= LINK_BOUND else
 5429                         f": past the {LINK_BOUND}s bound" + (" -- it rode the outage out and completed once the link was back"
 5430                                                              if rc == 0 else ""))
 5431                  f += not check(tte <= LINK_BOUND, f"ended {tte:.1f}s after the cut (bound {LINK_BOUND}s)",
 5432                                 f"ended {tte:.1f}s after the cut{why}")
 5433              if rc == 69:
 5434                  what = "exit 69: SKIPPED - NO NETWORK CONNECTION, the sentinel"
 5435              elif rc == 0 and tte < self.restore_after:
 5436                  what = f"exit 0 {tte:.1f}s after the cut, with the link still down: a success reported for a run that could not reach the cloud"
 5437              elif rc == 0:
 5438                  # How it waited differs by backend -- TCP retransmits on
 5439                  # WebDAV, the S3 backend's re-dials through its low-level
 5440                  # retries on s3 (the header, 2026-09-13) -- so the line
 5441                  # names the outcome and not a mechanism.
 5442                  what = (f"exit 0 {tte:.1f}s after the cut: a success reported for a run the network left -- it waited "
 5443                          f"the {self.restore_after:.0f}s outage out instead of ending within its own bound")
 5444              elif rc == 75:
 5445                  what = "exit 75: the lock sentinel, for a run nothing else held the lock against"
 5446              else:
 5447                  what = f"exit {rc}: a plain failure"
 5448              f += not check(rc == 69 or rc not in (0, 75), what, what)
 5449          else:
 5450              rc, tte = None, None
 5451          # The receiving side, once quiet: nothing under a temporary name, and
 5452          # nothing under a final name that is not the whole file.
 5453          got = self.settle(receiving) if receiving else {}
 5454          if receiving:
 5455              partials = sorted(r for r in got if ".partial" in r)
 5456              f += not check(not partials, "no *.partial left on the receiving side",
 5457                             f"partial files left on the receiving side: {partials}")
 5458              there = [r for r in got if r in sources]
 5459              broken = {r: f"{got[r][0]} of {sources[r][0]} bytes{'' if got[r][0] != sources[r][0] else ', content differs'}"
 5460                        for r in there if got[r] != sources[r]}
 5461              f += not check(not broken, f"every file present on the receiving side is whole, by content ({len(there)} of {len(sources)} there)",
 5462                             f"under a final name but not the file: {broken}")
 5463          after = self.stamps()
 5464          for s in stamps:
 5465              if after.get(s, "") == before.get(s, ""):
 5466                  check(True, f"{s} unchanged ({after.get(s) or 'absent'})", "")
 5467                  continue
 5468              parts = after.get(s, "").split()
 5469              # A failure stamp may carry an outcome token and reason after
 5470              # its return code (#398); validate the prefix, not total fields.
 5471              code = (int(parts[1]) if len(parts) >= 2 and parts[0].isdecimal()
 5472                      and parts[1].isdecimal() and int(parts[1]) <= 255 else None)
 5473              f += not check(code not in (0, None), f"{s} records the failure ({after.get(s)})",
 5474                             f"{s} does not record a valid failure ({after.get(s)}) for a run the network left")
 5475          if upload_marker:
 5476              m0, m1 = before.get("settings-backup.uploaded", ""), after.get("settings-backup.uploaded", "")
 5477              complete = all(got.get(r) == src for r, src in sources.items())
 5478              f += not check(m1 == m0 or complete,
 5479                             "settings-backup.uploaded unchanged" if m1 == m0 else "settings-backup.uploaded moved, and the archive is whole in the cloud",
 5480                             f"settings-backup.uploaded moved ({m0 or 'absent'} -> {m1}) though the archive is not whole in the cloud")
 5481          # The plain re-run, with the link back -- once the endpoint has let go
 5482          # of the cut run. rclone gave up, but what it had already written is
 5483          # still in flight: the guest kernel's orphaned socket, and behind it
 5484          # QEMU's user-mode stack, which took LINK5's whole 16.5 MiB archive in
 5485          # under a second and delivers it to the server at the server's pace
 5486          # long after the guest has forgotten the socket. A second PUT of the
 5487          # same name meanwhile gets `423 Locked` from rclone serve webdav
 5488          # (2026-09-09, twice). A handheld buffers a few MiB at most
 5489          # (tcp_wmem), so its window is seconds; it is printed here because it
 5490          # is real, and a retry right after the link returns can fall into it.
 5491          waited = self.endpoint_quiet()
 5492          if waited > 2:
 5493              print(f"          waited {waited:.0f}s for the endpoint to let go of the cut run before the re-run")
 5494          # The re-run. On this QA server two cases need tolerating, both the
 5495          # same buffer. One: the cut run's copyto delivered the whole archive
 5496          # body through QEMU's slirp buffer even as rclone reported failure
 5497          # (the receiving-side check above finds it whole), and rclone serve
 5498          # webdav then holds that dated filename's lock for a moment -- a PUT
 5499          # of the SAME name gets `423 Locked`. A real provider resets an
 5500          # aborted PUT and has no such lock. Two: the re-run's own PUT goes
 5501          # into the same buffer at once and is drained by the throttled server
 5502          # for longer than the deliberate run's stall ceiling (D-CLOUD-128,
 5503          # below). Both are the fixture, so tolerate only those exact
 5504          # signatures, only on WebDAV, and say so. A genuine re-run failure
 5505          # carries neither and is reported at once.
 5506          webdav = backend("backend").strip() == "webdav"
 5507          mark = log_mark(self.dev)
 5508          rc2, out2 = run_rc(self.dev, rerun or cmd, env)
 5509          self.keep(key, out2)
 5510          # What the card and the page had to show for the cut run: its whole
 5511          # stdout (re-read now that it has ended; `out` stopped at the cut) and
 5512          # its exit. The vocabulary gate (#105, D-UI-028) judges that.
 5513          f += assert_message(self.status()[0], rc, self.args.vocabulary, label="the cut run: ")
 5514          # rclone's "423 Locked" goes to the --log-file, not to stdout, so the
 5515          # log is where a lock shows. One case on this backend is not a script
 5516          # fault and not the harness's to pass off as one: when the operation
 5517          # re-PUTs a file under the SAME name (the settings archive), the QA
 5518          # WebDAV server can still be holding that name's lock. The cut run's
 5519          # copyto delivered the whole body through QEMU's slirp buffer -- which
 5520          # is why the post-cut "whole in the cloud" check above passed -- but
 5521          # rclone serve webdav keeps the PUT open, waiting for a request body
 5522          # that never finishes (the guest's rclone exited with the link down,
 5523          # so slirp never sees the connection close), and refuses a second PUT
 5524          # of that name with 423 for as long as it waits. Both faces are the
 5525          # same slirp artifact: on a real provider an aborted PUT leaves
 5526          # nothing, and the re-run genuinely re-uploads and succeeds. So where
 5527          # the archive is already whole and correct in the cloud and the only
 5528          # thing stopping the re-run is that lock, this criterion is SKIPPED
 5529          # with the reason, not FAILED. On every other backend `locked` is
 5530          # False and both checks run; on MinIO they have (LINK5, 2026-09-13,
 5531          # 40 s and 120 s outages): the re-run was accepted at once and the
 5532          # archive matched after it, the stale short body discarded by the
 5533          # atomic PUT rather than kept under the name.
 5534          since = log_since(self.dev, mark)
 5535          locked = webdav and rc2 != 0 and "423 Locked" in since
 5536          # The buffer's other face, seen the first time the cell ran under the
 5537          # stall ceiling (LINK5 on WebDAV, 4d7eb1f303, 2026-09-13): the re-run
 5538          # started only after endpoint_quiet() saw the server hold no fd, so
 5539          # no PUT held the name and nothing 423-shaped was logged; its own PUT
 5540          # of the 12 MiB archive was taken by slirp at once, the server drained
 5541          # it at 200k for ~40 s after the 4 MiB burst (the fixture's sizing,
 5542          # fx_link5), and rclone's counter -- bytes handed to the kernel, not
 5543          # bytes the server has -- read 100% and moved nothing for all of it.
 5544          # 36 s of that is the ceiling: the wrapper ended a healthy upload
 5545          # (`made no progress for 36s ... reporting 124`), and the archive was
 5546          # whole on the receiving side afterwards, the buffer having delivered
 5547          # the body regardless. Over a link TCP sizes the in-flight bytes to
 5548          # the path, so that leg is seconds on a handheld; here it is the whole
 5549          # archive. So: rc 124, the wrapper's line, no lock, the last per-file
 5550          # line at 100%, the archive already whole -- and only on WebDAV. The
 5551          # comparison after the re-run still runs (the drain must have
 5552          # finished the file), and on S3 every check runs: the proxy pumps the
 5553          # same way, the 12 MiB re-run passed there by the margin of a smaller
 5554          # buffer, and a 124 there is a FAIL to look at, not a face to learn.
 5555          # KILL5's 6 MiB archive drains inside the ceiling and is unaffected.
 5556          drained = (webdav and rc2 == 124 and not locked
 5557                     and LINK_STALL_ENDED.search(since) is not None and last_file_percent(out2) == 100)
 5558          archive_whole = receiving and all(got.get(r) == src for r, src in sources.items())
 5559          telling = [l for l in out2.splitlines() if re.search(r"ERROR|WARN|Failed|failed|exit", l)]
 5560          last = (telling or out2.strip().splitlines() or ["no output"])[-1].strip()[:160]
 5561          if locked and archive_whole and not strict_retry:
 5562              print("    SKIP  the re-run is refused by the QA WebDAV server's stale-PUT lock (423 Locked) on the same "
 5563                    "archive name -- a slirp artifact, not the script; the archive is already whole in the cloud. "
 5564                    "Asserted on MinIO (LINK5, 2026-09-13): no lock, the re-run exits 0 and the archive matches after it.")
 5565          elif drained and archive_whole and not strict_retry:
 5566              print("    SKIP  the re-run was ended by the stall ceiling with rclone's counter at 100%: QEMU's user-mode "
 5567                    "stack takes the whole body at once and the throttled QA WebDAV server drains it for longer than the "
 5568                    "ceiling, so the counter shows no progress while the upload completes -- the fixture, not the script "
 5569                    "(D-CLOUD-128, 2026-09-13); the archive is already whole in the cloud and is compared again below. "
 5570                    "Asserted on MinIO (LINK5, 4d7eb1f303, 2026-09-13): the re-run exits 0 and the archive matches after it.")
 5571          else:
 5572              f += not check(rc2 == 0, "a plain re-run with the link back exits 0", f"the re-run exits {rc2}: {last!r}")
 5573          if verify:
 5574              ok, msg = verify(out2)
 5575              f += not check(ok, msg, msg)
 5576          elif receiving and locked and archive_whole and not strict_retry:
 5577              # The lock's second face: the stale PUT the server is still
 5578              # holding open commits or aborts when slirp finally drops the
 5579              # connection, and the stored file changes under a name the re-run
 5580              # was refused for. Comparing it now judges the QA server, not the
 5581              # script (LINK5 on db6b42c180, 2026-09-13: whole and matching after
 5582              # the cut, refused with 423 on the re-run, then no longer
 5583              # matching). Same artifact, same disposition as the line above.
 5584              # On MinIO the same day (519f40aa0c, guest d, 40 s and 120 s
 5585              # outages) this check ran and passed: whole and matching after
 5586              # the cut and after the re-run, the cut PUT's 8.4 MiB discarded.
 5587              print("    SKIP  the receiving side after the re-run: under the stale-PUT lock the QA WebDAV server's copy "
 5588                    "changes when the cut connection finally closes; not the script's doing. Asserted on MinIO "
 5589                    "(LINK5, 2026-09-13): whole and matching after the cut and after the re-run.")
 5590          elif receiving:
 5591              got2 = self.settle(receiving)
 5592              bad = [r for r in sources if got2.get(r) != sources[r]]
 5593              f += not check(not bad, f"after the re-run all {len(sources)} files match on the receiving side",
 5594                             f"after the re-run these do not match on the receiving side: {bad}")
 5595          return f
 5596  
 5597  
 5598  # -- the cells -----------------------------------------------------------------
 5599  
 5600  def link_files(prefix, n=LINK_FILES, ext="bin"):
 5601      return {f"{prefix}{i}.{ext}": os.urandom(LINK_MIB * 1024 * 1024) for i in range(1, n + 1)}
 5602  
 5603  
 5604  def srcmap(files):
 5605      """{rel: bytes} -> {rel: (size, sha256)}, what exercise compares against."""
 5606      return {rel: (len(data), sha(data)) for rel, data in files.items()}
 5607  
 5608  
 5609  def fx_link1(L):
 5610      """Saves restore, the startup sync's command, cut during the compare:
 5611      everything already in the cloud, nothing to move, the listing in flight."""
 5612      files = {f"saves/sys{d:02d}/game{g}.srm": f"save {d}-{g}".encode() for d in range(1, 25) for g in (1, 2)}
 5613      L.plant_device(L.root, files)
 5614      rc, out = run_rc(L.dev, "cloud_backup --yes --saves-only")
 5615      if rc != 0 or len(backend_sizes(epath(L.saves_remote))) < len(files):
 5616          raise Fail(f"seeding the cloud with the saves failed (rc {rc}); cannot stage a compare")
 5617      print(f"          {len(files)} saves in 24 directories on both sides; RCLONE_TPSLIMIT={LINK_TPS} makes the compare last")
 5618      return L.exercise("LINK1", "cloud_restore --yes --method=copy --update --saves-only", LINK_MARKER_CHECKS,
 5619                        ("device", L.root), srcmap(files), ["last-restore"], env=f"RCLONE_TPSLIMIT={LINK_TPS}")
 5620  
 5621  
 5622  def fx_link2(L):
 5623      """Saves backup, cut during the transfer."""
 5624      files = link_files("savestates/link-", ext="state")
 5625      L.plant_device(L.root, files)
 5626      return L.exercise("LINK2", "cloud_backup --yes --saves-only", LINK_MARKER_FILE,
 5627                        ("cloud", epath(L.saves_remote)), srcmap(files), ["last-backup"])
 5628  
 5629  
 5630  def fx_link3(L):
 5631      """ROMs and BIOS back up a system, cut during the transfer."""
 5632      croot = L.content_dir()
 5633      files = link_files("link-")
 5634      L.plant_device(croot, files)
 5635      return L.exercise("LINK3", f"cloud_content_backup {shlex.quote(CONTENT_DIR)}", LINK_MARKER_FILE,
 5636                        ("cloud", f"{epath(L.content_remote)}/ROMs/{CONTENT_DIR}"), srcmap(files), ["last-content-backup"])
 5637  
 5638  
 5639  def fx_link4(L):
 5640      """ROMs and BIOS restore a system, cut during the transfer."""
 5641      croot = L.content_dir()
 5642      files = link_files("link-")
 5643      L.plant_cloud(files, f"{epath(L.content_remote)}/ROMs/{CONTENT_DIR}")
 5644      return L.exercise("LINK4", f"cloud_content_restore {shlex.quote(CONTENT_DIR)}", LINK_MARKER_FILE,
 5645                        ("device", croot), srcmap(files), ["last-content-restore"])
 5646  
 5647  
 5648  def fx_link5(L):
 5649      """The settings archive -- backuptool's own, then cloud_backup
 5650      --system-only -- cut mid-upload. The upload marker must not move unless
 5651      the archive completed."""
 5652      broot = f"{L.root}/backup"
 5653      # Six MiB leaves data in flight after the endpoint's four-MiB burst,
 5654      # but drains inside the unchanged 36-second stall ceiling at 200k.
 5655      # The old 12-MiB fixture exceeded that bound by construction, masking
 5656      # retry evidence behind a WebDAV skip (D-CLOUD-128, #400). Assert the
 5657      # cut actually lands and require a successful retry on both providers.
 5658      pad = "/storage/.config/retroarch/link5-padding.bin"
 5659      L.dev.run(f"head -c 6291456 /dev/urandom > {pad}; sync")
 5660      try:
 5661          rc, out = run_rc(L.dev, "backuptool backup")
 5662      finally:
 5663          L.dev.run(f"rm -f {pad}", check=False)
 5664      names = L.dev.run(f"cd {shlex.quote(broot)} 2>/dev/null && ls *.tar.gz *.zip 2>/dev/null; true", check=False).split()
 5665      if rc != 0 or not names:
 5666          raise Fail(f"backuptool backup wrote no archive under {broot} (rc {rc}): {out.strip().splitlines()[-1][:120] if out.strip() else ''}")
 5667      name = names[0]
 5668      size = int(L.dev.run(f"stat -c %s {shlex.quote(f'{broot}/{name}')}").strip())
 5669      digest = L.dev.sha(f"{broot}/{name}")
 5670      print(f"          archive {name}, {size / 1048576:.1f} MiB")
 5671      folder = L.dev.run("cloud_device_id 2>/dev/null || true").strip()
 5672      if not folder:
 5673          raise Fail("cloud_device_id printed nothing; cannot name the archive's cloud folder")
 5674      # The marker says what this device last sent and where; without it this
 5675      # run wants to send the archive, which is the point of the cell.
 5676      L.dev.run(f"rm -f {CACHE}/settings-backup.uploaded", check=False)
 5677      return L.exercise("LINK5", "cloud_backup --yes --system-only", LINK_MARKER_FILE,
 5678                        ("cloud", f"{epath(L.settings_remote)}/{folder}"), {name: (size, digest)},
 5679                        ["last-settings-backup"], upload_marker=True, strict_retry=True)
 5680  
 5681  
 5682  def fx_link6(L):
 5683      """The exit sync -- cloud_backup --yes --saves-only --recent -- cut
 5684      during the transfer. A stamp of success before it, so --recent takes its
 5685      filtered path."""
 5686      files = link_files("savestates/link-", ext="state")
 5687      L.plant_device(L.root, files)
 5688      L.dev.run(f"mkdir -p {CACHE}; printf '%s 0\\n' $(( $(date +%s) - 600 )) > {CACHE}/last-backup")
 5689      return L.exercise("LINK6", "cloud_backup --yes --saves-only --recent", LINK_MARKER_FILE,
 5690                        ("cloud", epath(L.saves_remote)), srcmap(files), ["last-backup"])
 5691  
 5692  
 5693  def fx_link7(L):
 5694      """The picker scan, cut mid-scan. Twenty-four systems and BIOS in the
 5695      cloud, the listing paced to two transactions a second; S3 is paginated
 5696      one entry per request so its batched listing stays in flight. The scan prints
 5697      nothing until it is done, so the cut lands once it holds a connection.
 5698      The re-run must name every planted system."""
 5699      systems = [f"sys{d:02d}" for d in range(1, 25)]
 5700      cloud = {f"ROMs/{s}/game.bin": f"rom {s}".encode() for s in systems}
 5701      cloud["BIOS/bios.bin"] = b"bios"
 5702      L.plant_cloud(cloud, epath(L.content_remote))
 5703  
 5704      def verify(out):
 5705          names = {line.split("|")[0] for line in out.splitlines() if "|" in line}
 5706          missing = sorted(set(systems + ["bios"]) - names)
 5707          return (not missing, f"the re-run's scan names all {len(systems)} systems and bios"
 5708                  if not missing else f"the re-run's scan is missing {missing}")
 5709      env = f"RCLONE_TPSLIMIT={LINK_TPS}"
 5710      if backend("backend").strip() == "s3":
 5711          # Default MaxKeys=1000 fits this entire fixture in one response,
 5712          # before the cut can land (#402). Page size changes only the QA
 5713          # invocation, not the product or endpoint. Completion before the
 5714          # actual cut remains a failure in Link.exercise.
 5715          env += " RCLONE_S3_LIST_CHUNK=1"
 5716      return L.exercise("LINK7", "cloud_content_restore --scan", None, None, {}, ["last-content-match", "last-content-restore"],
 5717                        env=env, verify=verify)
 5718  
 5719  
 5720  LINK_FIXTURES = [
 5721      ("LINK1", "saves restore (the startup sync's command), link cut during the compare", fx_link1),
 5722      ("LINK2", "saves backup, link cut during the transfer", fx_link2),
 5723      ("LINK3", "ROMs and BIOS backup, link cut during the transfer", fx_link3),
 5724      ("LINK4", "ROMs and BIOS restore, link cut during the transfer", fx_link4),
 5725      ("LINK5", "settings archive upload (backuptool backup; cloud_backup --system-only), link cut mid-upload", fx_link5),
 5726      ("LINK6", "the exit sync (cloud_backup --yes --saves-only --recent), link cut during the transfer", fx_link6),
 5727      ("LINK7", "the picker scan (cloud_content_restore --scan), link cut mid-scan", fx_link7),
 5728  ]
 5729  
 5730  
 5731  def run_link(dev, root, remote, args, settings, serial, only):
 5732      """The link-loss cells on one device (#103). Every cell resets the
 5733      scratch tree and the endpoint first; the cache directory (stamps, upload
 5734      marker, saves-root record) is carried across and put back, as run_pair
 5735      does."""
 5736      step("the link-loss cells: a serial console, a throttled endpoint, one guest")
 5737      if args.real_roms:
 5738          raise Fail("the link-loss cells empty the saves root between cells; they never run against real ROMs")
 5739      if not check(backend_throttled(), "the endpoint is throttled (--bwlimit on the server)",
 5740                   "the endpoint is not throttled: nine MiB cross the loopback before the transfer can be cut -- "
 5741                   "`tools/cloud-test-backend [--backend s3] down && CLOUD_QA_BWLIMIT=200k tools/cloud-test-backend [--backend s3] up` "
 5742                   "(WebDAV or s3; the other three cannot be throttled)"):
 5743          return 1
 5744      L = Link(dev, serial, root, remote, settings, args)
 5745      L.assert_same_guest()
 5746      check(True, f"the serial console is this device's; its default route runs over {L.iface}; the endpoint is {L.hostport}", "")
 5747      print(f"    link restored {L.restore_after}s after each cut; a run must end within {LINK_BOUND}s of it")
 5748      failures = 0
 5749      had = snapshot_cache(dev)
 5750      try:
 5751          for key, title, fn in LINK_FIXTURES:
 5752              if only and key not in only:
 5753                  continue
 5754              step(f"{key} -- {title}")
 5755              L.reset()
 5756              try:
 5757                  failures += fn(L)
 5758                  failures += litter_scan(dev, settings, remote, label=f"{key}: ")
 5759              except Fail as e:
 5760                  failures += 1
 5761                  print(f"    FAIL  {e}")
 5762                  # A Fail mid-cell may have left the link down, or a run going.
 5763                  try:
 5764                      L.serial.run(f"ip link set {L.iface} up")
 5765                      running = L.dev.run(f"[ -e {LINK_DIR}/pid ] && [ ! -e {LINK_DIR}/rc ] && echo yes || true",
 5766                                          check=False).strip() == "yes"
 5767                      if running:
 5768                          L.finish_or_kill()
 5769                  except Fail as e2:
 5770                      print(f"    WARN  could not tidy after the failure: {e2}", file=sys.stderr)
 5771      finally:
 5772          L.reset()
 5773          restore_cache(dev, had)
 5774      return failures
 5775  
 5776  
 5777  # ===========================================================================
 5778  # #105: a writer killed at every step, and the power cut (D-CLOUD-077/078/079)
 5779  # ===========================================================================
 5780  #
 5781  # D-CLOUD-078 asks every writer three things, in order: know that you
 5782  # succeeded; replace the old state only after that; remove the superseded
 5783  # record once, so exactly one last-known-good exists at rest. The rule in
 5784  # engineering-practices.md says how to test it: kill the writer at every step
 5785  # and assert the previous state is what remains. These cells do that, each
 5786  # against the shipped scripts and the running EmulationStation, and each was
 5787  # first committed with its failing output (the harness's rule).
 5788  #
 5789  # Four mechanisms, chosen per step (docs/audits/2026_09_10-graceful-
 5790  # degradation/kill-fixtures-design.md):
 5791  #
 5792  # * PG@marker -- SIGKILL (or SIGTERM) the detached run's process group when a
 5793  #   regex matches its stdout: rclone's per-file progress line, so the kill
 5794  #   lands mid-transfer (LINK's wait_marker).
 5795  # * watcher -- a guest-side script polling a filesystem condition every 20 ms
 5796  #   and killing the group the moment it holds. For a window inside one long
 5797  #   binary (tar over 20k files, gzip over 64 MiB) where no line is printed.
 5798  #   It is a file, not a pkill pattern, because of the self-match lesson.
 5799  # * shim -- a bash function of a command's name, exported so it wins over
 5800  #   PATH in every bash the run starts. backuptool and cloud_content_restore
 5801  #   source /etc/profile, which puts /usr/bin first, so a --path-prefix
 5802  #   directory is not enough; an exported function survives that (bash
 5803  #   imports BASH_FUNC_* on start, proven on the guest). set_setting is a
 5804  #   function of the calling shell, so its override is defined in that shell
 5805  #   after the profile is sourced.
 5806  # * plant -- the torn state written directly, standing for a kill inside a
 5807  #   builtin or a single write() syscall that no external signal lands in
 5808  #   deterministically. Labelled as such in the PASS/FAIL text.
 5809  # * reset -- HMP `system_reset` over QEMU's monitor: every dirty page in the
 5810  #   guest is gone, the disk holds exactly what the guest issued. It models a
 5811  #   battery dying. It cannot model an SD card's write cache or FTL, which is
 5812  #   what the RG SP's truncated system.cfg (#102) may have been; that is what
 5813  #   the VM cannot prove, and the cells say so.
 5814  #
 5815  # The record's name follows D-CLOUD-079, not the design's draft: the
 5816  # last-known-good copy of system.cfg keeps its name, `system.cfg.backup`, and
 5817  # es_settings.cfg gains `es_settings.cfg.backup`. The scans accept
 5818  # `.last-good` too, so a build carrying either name is judged on the rule.
 5819  
 5820  import socket
 5821  import xml.etree.ElementTree as ET
 5822  
 5823  KILL_WATCH = "/tmp/qa-kill/watch.sh"
 5824  KILL_SCRATCH = "/storage/cloud-qa-kill"           # 20k empty files and a 64 MiB blob: a tar with a window
 5825  KILL_MANY = 20000
 5826  KILL_BLOB_MIB = 64
 5827  KILL_CONFIGS_TGZ = "/storage/.cache/qa-kill-configs.tgz"   # on /storage: /tmp does not survive a power cut
 5828  SYSCFG_DIR = "/storage/.config/system/configs"
 5829  SYSCFG = f"{SYSCFG_DIR}/system.cfg"
 5830  SYSCFG_LOCK = "/tmp/.system.cfg.lock"
 5831  SYSCFG_DEFAULT = "/usr/config/system/configs/system.cfg"
 5832  ES_DIR = "/storage/.config/emulationstation"
 5833  ES_SETTINGS = f"{ES_DIR}/es_settings.cfg"
 5834  ES_LOG = "/var/log/es_log.txt"
 5835  ES_PARSE_ERROR = "Could not parse Settings file"
 5836  BACKUPTOOL_CONF = "/storage/.config/backuptool.conf"
 5837  RESTORE_PENDING = "/storage/.config/.restore-finish-pending"
 5838  CLOUD_LOCK = "/var/run/cloud_sync.lock"
 5839  RECORD_NAMES = (".backup", ".last-good")          # D-CLOUD-079 keeps .backup; the design drafted .last-good
 5840  KILL_MARKER_NAME = re.compile(r"^\s*\*\s+(\S.*?):\s*\d+% /", re.M)   # the file rclone is on right now
 5841  WALK_TOGGLE = os.path.join(HERE, "vm-walks", "ui-settings-toggle.steps")
 5842  
 5843  
 5844  # -- 2a. the vocabulary gate ----------------------------------------------------
 5845  #
 5846  # What "player-visible" means today, from the classifiers on
 5847  # origin/test/qa-integration: the card (ThreadedCloudSync.cpp) shows a script
 5848  # line iff it has `%`, ` / `, or ERROR|FAILED|WARN case-folded and is not a
 5849  # `>>> ` protocol line; the page (GuiCloudTransfer::handleLine) shows only
 5850  # `>>> ` markers and rclone's own lines. So the gate checks every line the
 5851  # card would show and the last prose line of the run -- which is what #105
 5852  # makes the outcome line -- against words a handheld's screen must never
 5853  # carry. FORBIDDEN is active now: it fails, correctly, on today's `Log file:
 5854  # /var/log/cloud_sync.log`, `(rclone exit 3)`, `Check 'logger' output` and
 5855  # `run: cloud_setup --accept-saves-root`. The ALLOWED shapes are D-UI-028's
 5856  # four words and sit behind --vocabulary until the strings land.
 5857  
 5858  MSG_PROTO = re.compile(r"^>>> ")
 5859  MSG_RCLONE = re.compile(r"^(Transferred:|Checks:|Elapsed time:|Errors:|Deleted:|Renamed:|Transferring:|Checking:)|^\s*\*\s")
 5860  MSG_DECOR = re.compile(r"^[=\-]{4,}$|^\s*$")
 5861  ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
 5862  # Each alternative names a fragment seen in the scripts today: exit codes,
 5863  # rc=, log paths, logger, rclone, CLI flags and script names as "recovery"
 5864  # instructions, signals, sysexits.
 5865  FORBIDDEN = re.compile(
 5866      r"(?i)(\bexit(ed)?(\s+code)?\s*[:=]?\s*\(?-?\d+\)?|\brc\s*=\s*-?\d+|/var/log\S*|\S+\.log\b"
 5867      r"|\blogger\b|\bjournalctl\b|\brclone\b|\bstderr\b|\bsysexits\b|\bEX_[A-Z]+\b|\bSIG(TERM|KILL|INT)\b"
 5868      r"|\berrno\b|\bpid\s+\d+|\bflock\b|\bsentinel\b|\bcloud_[a-z_]+\b|\bbackuptool\b|(^|\s)--[a-z][a-z-]+"
 5869      r"|\bCOMPLETED WITH ERRORS\b)")
 5870  # The positive shape: three words since D-UI-030 retired COMPLETED WITH GAPS
 5871  # (a partial run is COULDN'T FINISH with what arrived counted on the page).
 5872  # On by default since 2026-09-10 (#105's last box): --no-vocabulary turns it
 5873  # off for a run against an image that predates the strings.
 5874  ALLOWED_SURFACE = re.compile(r"^(COMPLETED|COULDN'T FINISH|SKIPPED)( - [A-Z0-9 ,.'-]+)?$")
 5875  ALLOWED_SCRIPT = re.compile(r"^(Completed|Couldn't finish|Skipped)\b.*[.!]$")
 5876  RECOVERY = re.compile(r"(?i)\btry again\b|\bwhen you'?re (back )?online\b")
 5877  
 5878  
 5879  def clean_line(raw):
 5880      # Colour codes first, then anything unprintable: stripping ESC before the
 5881      # regex leaves "[32m" in front of the text.
 5882      return "".join(c for c in ANSI.sub("", raw) if 32 <= ord(c) < 127).strip()
 5883  
 5884  
 5885  def card_visible(out):
 5886      """Exactly the card's predicate, applied to a run's stdout."""
 5887      for raw in out.splitlines():
 5888          s = clean_line(raw)
 5889          if not s or MSG_PROTO.match(s):
 5890              continue
 5891          u = s.upper()
 5892          if "%" in s or " / " in s or any(w in u for w in ("ERROR", "FAILED", "WARN")):
 5893              yield s
 5894  
 5895  
 5896  def last_player_line(out):
 5897      """The last prose line of a run: not a protocol marker, not rclone's, not
 5898      a rule of dashes. What #105 turns into the outcome line."""
 5899      lines = [clean_line(l) for l in out.splitlines()]
 5900      lines = [l for l in lines if l and not (MSG_PROTO.match(l) or MSG_RCLONE.match(l) or MSG_DECOR.match(l))]
 5901      return lines[-1] if lines else ""
 5902  
 5903  
 5904  def assert_message(out, rc, vocabulary=False, stamp=None, label=""):
 5905      """The vocabulary gate on one run's stdout. Returns the number of failed
 5906      checks. `stamp` is (name, contents) of the last-* file the run wrote,
 5907      whose second field must be the exit code the run left with."""
 5908      f = 0
 5909      visible = list(card_visible(out))
 5910      last = last_player_line(out)
 5911      offenders = []
 5912      for line in visible + ([last] if last else []):
 5913          m = FORBIDDEN.search(line)
 5914          if m:
 5915              offenders.append(f"{line[:90]!r} <- {m.group(0)!r}")
 5916      seen = set()
 5917      offenders = [o for o in offenders if not (o in seen or seen.add(o))]
 5918      f += not check(not offenders,
 5919                     f"{label}no developer words on the {len(visible)} card-visible line(s) or the outcome line ({last[:70]!r})",
 5920                     f"{label}developer words where a player reads ({len(offenders)}): " + "; ".join(offenders[:3]))
 5921      if vocabulary:
 5922          f += not check(bool(ALLOWED_SCRIPT.match(last)),
 5923                         f"{label}the outcome line is one of the three outcome words ({last[:70]!r})",
 5924                         f"{label}the outcome line is not Completed / Couldn't finish / Skipped: {last[:90]!r}")
 5925          if rc is not None and rc not in (0, 75, 69):
 5926              f += not check(bool(RECOVERY.search(last)),
 5927                             f"{label}a failed run says how to recover",
 5928                             f"{label}exit {rc} and the outcome line names no recovery (TRY AGAIN ...): {last[:90]!r}")
 5929      if stamp is not None and rc is not None:
 5930          name, contents = stamp
 5931          parts = (contents or "").split()
 5932          f += not check(len(parts) >= 2 and parts[1] == str(rc),
 5933                         f"{label}{name} records the exit the run left with ({rc})",
 5934                         f"{label}{name} says {contents.strip()!r} for a run that exited {rc}")
 5935      return f
 5936  
 5937  
 5938  # -- 2b. the one-record assertion ----------------------------------------------
 5939  
 5940  LITTER_ALLOW = {f"{CONF}.qa-prev"}      # the harness's own, put back by restore_device
 5941  ARCHIVE_SHAPES = re.compile(r".*_SETTINGS\.tar\.gz$|.*_BACKUP\.tar\.gz$|.*_BACKUP\.zip$")
 5942  STAMP_LINE = re.compile(r"^\d+ -?\d+( .+)?$")     # epoch rc [token] [why...] -- D-UI-028: EmulationStation writes a token and the scripts' sentence; the scripts write the sentence with underscores
 5943  
 5944  
 5945  def valid_syscfg(text):
 5946      """(ok, why) for system.cfg's contents: non-empty, no NUL, has the
 5947      hostname, every non-blank line key=value."""
 5948      if not text:
 5949          return False, "empty"
 5950      if "\0" in text:
 5951          return False, "binary"
 5952      if "system.hostname=" not in text:
 5953          return False, f"{len(text)} bytes, system.hostname missing"
 5954      bad = [l for l in text.splitlines() if l.strip() and not re.match(r"^[^=\s]+=", l)]
 5955      if bad:
 5956          return False, f"{len(bad)} line(s) not key=value, e.g. {bad[0][:40]!r}"
 5957      return True, f"{len(text.splitlines())} keys"
 5958  
 5959  
 5960  def parse_syscfg(text):
 5961      out = {}
 5962      for l in text.splitlines():
 5963          if "=" in l and l.strip() and not l.startswith("#"):
 5964              k, _, v = l.partition("=")
 5965              out[k.strip()] = v
 5966      return out
 5967  
 5968  
 5969  def parse_es(text):
 5970      """{name: value} of an es_settings.cfg, or None when it does not parse."""
 5971      try:
 5972          root = ET.fromstring(text)
 5973      except ET.ParseError:
 5974          return None
 5975      if root.tag != "config":
 5976          return None
 5977      return {n.get("name"): n.get("value") for n in root if n.get("name") is not None}
 5978  
 5979  
 5980  def litter_scan(dev, settings, remote="", label=""):
 5981      """The one-record assertion, run at the end of every fixture: nothing a
 5982      writer left half-done, and exactly one last-known-good of each record.
 5983      One bounded `find` per root, classification host-side. Returns the number
 5984      of failed checks (0 or 1) and prints one line naming the first offenders
 5985      -- or, on a pass, what it counted, because a scan that finds nothing must
 5986      say what it looked at (engineering-practices, guards fail closed)."""
 5987      off = []       # (path, why)
 5988      counted = []
 5989  
 5990      def find(root, maxdepth=None, extra=""):
 5991          md = f"-maxdepth {maxdepth}" if maxdepth else ""
 5992          out = dev.run(f"find {shlex.quote(root)} -xdev {md} -type f {extra} 2>/dev/null | head -20000; true", check=False)
 5993          return [l for l in out.splitlines() if l]
 5994  
 5995      def cat(path):
 5996          return dev.run(f"cat {shlex.quote(path)} 2>/dev/null || true", check=False)
 5997  
 5998      # 1. the system config and its record
 5999      files = find(SYSCFG_DIR, 1)
 6000      for p in files:
 6001          b = os.path.basename(p)
 6002          if b == "system.cfg.tmp" or re.fullmatch(r"system\.cfg[A-Za-z0-9]{6}", b) or re.fullmatch(r"sed[A-Za-z0-9]{6}", b) or ".qa" in b:
 6003              off.append((p, "a writer's temporary file"))
 6004      ok, why = valid_syscfg(cat(SYSCFG))
 6005      if not ok:
 6006          off.append((SYSCFG, f"invalid: {why}"))
 6007      records = [p for p in files if os.path.basename(p) in {f"system.cfg{s}" for s in RECORD_NAMES}]
 6008      if len(records) != 1:
 6009          off.append((f"{SYSCFG}{{{','.join(RECORD_NAMES)}}}", f"{len(records)} last-known-good record(s), not one (D-CLOUD-078/079)"))
 6010      for r in records:
 6011          rok, rwhy = valid_syscfg(cat(r))
 6012          if not rok:
 6013              off.append((r, f"the record is invalid: {rwhy}"))
 6014      counted.append(f"system.cfg {why}" + (f", record {os.path.basename(records[0])[10:]}" if len(records) == 1 else ""))
 6015  
 6016      # 2. EmulationStation's settings and its record
 6017      files = find(ES_DIR, 1)
 6018      corrupt = [p for p in files if ".corrupt" in os.path.basename(p)]
 6019      for p in files:
 6020          if os.path.basename(p) == "es_settings.cfg.tmp":
 6021              off.append((p, "a writer's temporary file"))
 6022      if len(corrupt) > 1:
 6023          off.append((corrupt[1], f"{len(corrupt)} torn copies kept aside; one at most"))
 6024      es_text = cat(ES_SETTINGS)
 6025      es = parse_es(es_text) if es_text else {}
 6026      if es is None:
 6027          off.append((ES_SETTINGS, f"does not parse ({len(es_text)} bytes)"))
 6028      es_records = [p for p in files if os.path.basename(p) in {f"es_settings.cfg{s}" for s in RECORD_NAMES}]
 6029      if len(es_records) != 1:
 6030          off.append((f"{ES_SETTINGS}{{{','.join(RECORD_NAMES)}}}", f"{len(es_records)} last-known-good record(s), not one (D-CLOUD-079)"))
 6031      elif parse_es(cat(es_records[0])) is None:
 6032          off.append((es_records[0], "the record does not parse"))
 6033      counted.append(f"es_settings.cfg {len(es or {})} keys")
 6034  
 6035      # 3. the config root and the rclone directory
 6036      files = find("/storage/.config", 1) + find("/storage/.config/rclone", 1)
 6037      for p in files:
 6038          b = os.path.basename(p)
 6039          if p in LITTER_ALLOW:
 6040              continue
 6041          if b.endswith(".tmp") or b.endswith("~") or ".qa" in b:
 6042              off.append((p, "a writer's temporary file"))
 6043          elif b.endswith(".bak"):
 6044              # cloud_sync_helper takes the .bak before every merge and the run
 6045              # removes it once it completes (D-CLOUD-079), so a .bak at rest is
 6046              # the record a failed run falls back to until the next run
 6047              # completes -- and a violation only if a run completed after it
 6048              # was taken and left it there. The newest completed stamp says.
 6049              taken = int(dev.run(f"stat -c %Y {shlex.quote(p)} 2>/dev/null || echo 0", check=False).strip() or 0)
 6050              done = 0
 6051              for st in dev.run(f"cat {CACHE}/last-* 2>/dev/null; true", check=False).splitlines():
 6052                  parts = st.split()
 6053                  if len(parts) >= 2 and parts[1] in ("0", "9") and parts[0].isdigit():
 6054                      done = max(done, int(parts[0]))
 6055              if done > taken:
 6056                  off.append((p, f"a migration copy kept past a run that completed {done - taken}s after it was taken (D-CLOUD-079: removed after the next good run)"))
 6057      dev_id = cat(ID_FILE)
 6058      if dev_id and len(dev_id.splitlines()) != 1:
 6059          off.append((ID_FILE, f"{len(dev_id.splitlines())} lines, not one"))
 6060      prev = cat(f"{ID_FILE}.previous").split()
 6061      if len(prev) != len(set(prev)):
 6062          off.append((f"{ID_FILE}.previous", "duplicate lines"))
 6063  
 6064      # 4. the cache: every stamp and the producer's working copy
 6065      files = find(CACHE)
 6066      cache_pats = (".tmp.", ".ops.", ".cand.", ".canon.", ".manifest.", ".last-capture.", ".capture-failures.")
 6067      manifests = []
 6068      stamps = 0
 6069      for p in files:
 6070          b = os.path.basename(p)
 6071          if any(b.startswith(x) for x in cache_pats) or b.endswith(".tmp") or b.endswith(".partial"):
 6072              off.append((p, "a dead writer's scratch file"))
 6073          elif re.fullmatch(r"manifest-.*\.json", b) and os.path.dirname(p) == CACHE:
 6074              manifests.append(p)
 6075          elif b.startswith("last-") and b != "last-capture" and os.path.dirname(p) == CACHE:
 6076              stamps += 1
 6077              lines = [l for l in cat(p).splitlines() if l.strip()]
 6078              if len(lines) != 1 or not STAMP_LINE.match(lines[0]):
 6079                  off.append((p, f"not one `epoch rc` line: {lines[:2]!r}"))
 6080      if len(manifests) > 1:
 6081          off.append((manifests[1], f"{len(manifests)} working copies; one, manifest-<device id>.json"))
 6082      elif manifests and dev_id.strip() and os.path.basename(manifests[0]) != f"manifest-{dev_id.strip()}.json":
 6083          off.append((manifests[0], f"not this device's (id {dev_id.strip()})"))
 6084      lc = [l for l in cat(f"{CACHE}/last-capture").splitlines() if l.strip()]
 6085      modes = [stamp_mode(l) for l in lc]
 6086      if len(modes) != len(set(modes)):
 6087          off.append((f"{CACHE}/last-capture", f"more than one line for a mode: {modes}"))
 6088      marker = cat(f"{CACHE}/settings-backup.uploaded")
 6089      if marker and not re.fullmatch(r"[0-9a-f]{32}([0-9a-f]{32})? \S+\n?", marker):
 6090          off.append((f"{CACHE}/settings-backup.uploaded", f"not one `hash dest` line: {marker.strip()[:60]!r}"))
 6091      if dev.run(f"[ -e {CACHE}/saves-root ] && [ ! -s {CACHE}/saves-root ] && echo EMPTY || true", check=False).strip() == "EMPTY":
 6092          off.append((f"{CACHE}/saves-root", "an empty record: the #83 guard reads it as none (KILL15)"))
 6093      counted.append(f"{stamps} last-* stamps, {len(lc)} capture line(s), {len(manifests)} manifest")
 6094  
 6095      # 5. the settings archives
 6096      backups = settings.get("SETTINGS_BACKUPS") or settings.get("BACKUPFOLDER")
 6097      if backups:
 6098          files = find(backups)
 6099          roots = [p for p in files if os.path.dirname(p) == backups and ARCHIVE_SHAPES.match(os.path.basename(p))]
 6100          archived = [p for p in files if os.path.dirname(p) == f"{backups}/archive"]
 6101          for p in files:
 6102              b = os.path.basename(p)
 6103              if b.endswith(".partial") or b.endswith(".tmp") or b.startswith(".qa-"):
 6104                  off.append((p, "a writer's temporary file"))
 6105          if len(roots) > 1:
 6106              off.append((roots[1], f"{len(roots)} archives at the root: two candidates, not one record"))
 6107          for p in roots:
 6108              test = "unzip -t" if p.endswith(".zip") else "tar -tzf"
 6109              if dev.run(f"{test} {shlex.quote(p)} >/dev/null 2>&1 && echo ok || echo BAD", check=False).strip() != "ok":
 6110                  off.append((p, "the newest archive does not pass integrity"))
 6111          if len(archived) > 3:
 6112              off.append((archived[3], f"{len(archived)} in archive/, more than ARCHIVE_KEEP (3)"))
 6113          counted.append(f"{len(roots)} archive at root, {len(archived)} in archive/")
 6114  
 6115      # 6. the saves tree. The harness's own allowlist fixture (saves/scratch.tmp,
 6116      # planted to prove the filter keeps a .tmp out of the cloud) is not litter.
 6117      saves = settings.get("SAVESPATH") or settings.get("BACKUPPATH")
 6118      if saves:
 6119          own = {f"{saves}/{rel}" for rel in EXCLUDED}
 6120          files = find(saves, None, r"\( -name '*.partial' -o -name '*.tmp' \)")
 6121          for p in files:
 6122              if p in own or p.endswith(".state.auto.bak"):
 6123                  continue
 6124              off.append((p, "rclone's temporary copy of a save, left by a cut transfer" if p.endswith(".partial")
 6125                          else "a writer's temporary file"))
 6126          counted.append(f"saves tree clean of *.partial/*.tmp")
 6127  
 6128      # 7. the cloud folder
 6129      if remote:
 6130          sremote = settings.get("SETTINGS_REMOTE") or settings.get("SYNCPATH_BACKUP") or ""
 6131          cloud = backend_files(epath(sremote)) if sremote else []
 6132          for rel in cloud:
 6133              if rel.endswith(".partial"):
 6134                  off.append((f"cloud:{rel}", "a partial upload under the settings folder"))
 6135          by_folder = {}
 6136          for rel in cloud:
 6137              if "/" in rel:
 6138                  by_folder.setdefault(rel.split("/", 1)[0], []).append(rel.split("/", 1)[1])
 6139          for folder, names in by_folder.items():
 6140              if names.count("device.json") > 1:
 6141                  off.append((f"cloud:{folder}/device.json", "more than one"))
 6142          label_ = dev.run("cloud_device_id --label 2>/dev/null || true", check=False).strip()
 6143          if dev_id.strip() and label_ and dev_id.strip() in by_folder:
 6144              osn = os_name(dev)
 6145              own = [n for n in by_folder[dev_id.strip()] if re.fullmatch(rf"\d{{4}}_\d\d_\d\d-\d{{6}}-{re.escape(label_)}-{re.escape(osn)}_SETTINGS\.tar\.gz", n)]
 6146              keep_raw = dev.run(f"grep -m1 '^CLOUD_BACKUP_KEEP=' {CONF} 2>/dev/null | cut -d= -f2 | tr -d '\"' || true", check=False).strip()
 6147              keep = int(keep_raw) if keep_raw.isdigit() else 3
 6148              if len(own) > keep:
 6149                  off.append((f"cloud:{dev_id.strip()}/", f"{len(own)} of this device's archives, more than CLOUD_BACKUP_KEEP={keep}"))
 6150          sroot = settings.get("SAVES_REMOTE") or settings.get("SYNCPATH") or ""
 6151          for rel in (backend_files(epath(sroot)) if sroot else []):
 6152              if rel.endswith(".partial"):
 6153                  off.append((f"cloud:{rel}", "a partial upload under the saves folder"))
 6154          counted.append(f"cloud {len(cloud)} settings file(s)")
 6155  
 6156      shown = "; ".join(f"{p} ({w})" for p, w in off[:5]) + (f"; +{len(off) - 5} more" if len(off) > 5 else "")
 6157      return int(not check(not off,
 6158                           f"{label}one record each, no litter: " + "; ".join(counted),
 6159                           f"{label}{len(off)} record/litter violation(s): {shown}"))
 6160  
 6161  
 6162  # -- the monitor -------------------------------------------------------------------
 6163  
 6164  class Monitor:
 6165      """QEMU's human monitor over its unix socket: connect, read the prompt,
 6166      send a line, read the prompt back. `system_reset` is the power cut."""
 6167  
 6168      def __init__(self, path, timeout=10):
 6169          self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
 6170          self.sock.settimeout(timeout)
 6171          self.sock.connect(path)
 6172          self._prompt()
 6173  
 6174      def _prompt(self, timeout=5.0):
 6175          buf = b""
 6176          end = time.time() + timeout
 6177          self.sock.settimeout(0.5)
 6178          while time.time() < end:
 6179              try:
 6180                  chunk = self.sock.recv(4096)
 6181              except (socket.timeout, TimeoutError):
 6182                  if buf.rstrip().endswith(b"(qemu)"):
 6183                      break
 6184                  continue
 6185              if not chunk:
 6186                  break
 6187              buf += chunk
 6188              if buf.rstrip().endswith(b"(qemu)"):
 6189                  break
 6190          return buf.decode("utf-8", "replace")
 6191  
 6192      def cmd(self, text):
 6193          self.sock.sendall((text + "\n").encode())
 6194          return self._prompt()
 6195  
 6196      def sendkey(self, key, times=1, gap=0.15):
 6197          for _ in range(times):
 6198              self.cmd("sendkey " + key)
 6199              time.sleep(gap)
 6200  
 6201      def system_reset(self):
 6202          self.cmd("system_reset")
 6203  
 6204      def screendump(self, path):
 6205          try:
 6206              os.remove(path)
 6207          except OSError:
 6208              pass
 6209          # A GL scanout (a guest on virgl, fork #291) has no surface for the
 6210          # monitor's screendump; the frame comes from QEMU's VNC server then,
 6211          # through vm-visual-qa's grabber, as the same P6 file.
 6212          if getattr(self, "_vnc", None):
 6213              return self._vnc_screendump(path)
 6214          if "no surface" in (self.cmd("screendump " + path) or ""):
 6215              return self._vnc_screendump(path)
 6216          for _ in range(60):
 6217              if os.path.exists(path) and os.path.getsize(path) > 0:
 6218                  size = -1
 6219                  while size != os.path.getsize(path):
 6220                      size = os.path.getsize(path)
 6221                      time.sleep(0.05)
 6222                  return True
 6223              time.sleep(0.05)
 6224          return False
 6225  
 6226      def _vnc_screendump(self, path):
 6227          if getattr(self, "_vnc", None) is None:
 6228              m = re.search(r"Server:\s+([0-9.]+):(\d+)", self.cmd("info vnc") or "")
 6229              if not m:
 6230                  return False
 6231              self._vnc = (m.group(1), int(m.group(2)))
 6232          try:
 6233              w, h, rgb = visual_qa().vnc_frame(self._vnc[0], self._vnc[1])
 6234          except (OSError, ValueError, Fail):
 6235              return False
 6236          with open(path, "wb") as fh:
 6237              fh.write(b"P6\n%d %d\n255\n" % (w, h))
 6238              fh.write(rgb)
 6239          return True
 6240  
 6241      def frame(self):
 6242          """The framebuffer as bytes, for the walk's settle/wait-for-change
 6243          steps. One scratch file, reused."""
 6244          if getattr(self, "_scratch", None) is None:
 6245              import tempfile
 6246              self._scratch = os.path.join(tempfile.mkdtemp(prefix="crt-frame-"), "f.ppm")
 6247          if not self.screendump(self._scratch):
 6248              return None
 6249          try:
 6250              with open(self._scratch, "rb") as fh:
 6251                  return fh.read()
 6252          except OSError:
 6253              return None
 6254  
 6255      def close(self):
 6256          try:
 6257              self.sock.close()
 6258          except OSError:
 6259              pass
 6260  
 6261  
 6262  def walk_steps(path):
 6263      """A tools/vm-walks step file as [(verb, rest)] -- the same grammar
 6264      tools/vm-visual-qa reads, so one file serves both."""
 6265      steps = []
 6266      for raw in open(path):
 6267          line = raw.split("#", 1)[0].strip()
 6268          if line:
 6269              verb, _, rest = line.partition(" ")
 6270              steps.append((verb, rest.strip()))
 6271      return steps
 6272  
 6273  
 6274  def steps_without_toggle(steps):
 6275      """The walk up to, not including, its last `key x` -- the toggle press --
 6276      so the same file drives a page open/close that changes nothing."""
 6277      idx = max((i for i, s in enumerate(steps) if s == ("key", "x")), default=len(steps))
 6278      return steps[:idx]
 6279  
 6280  
 6281  def visual_qa():
 6282      """tools/vm-visual-qa as a module, for the walk step semantics.
 6283  
 6284      The step grammar has one implementation, not two: `settle` and
 6285      `wait-for-change` are frame comparisons with calibrated thresholds
 6286      (fork #125), and a second copy of those numbers here would drift from
 6287      the one the walks are written against."""
 6288      import importlib.machinery
 6289      import importlib.util
 6290      path = os.path.join(HERE, "vm-visual-qa")
 6291      try:
 6292          loader = importlib.machinery.SourceFileLoader("vm_visual_qa", path)
 6293          spec = importlib.util.spec_from_loader("vm_visual_qa", loader)
 6294          mod = importlib.util.module_from_spec(spec)
 6295          loader.exec_module(mod)
 6296          return mod
 6297      except Exception as exc:                                  # noqa: BLE001
 6298          raise Fail(f"the walk steps need {path}: {exc}")
 6299  
 6300  
 6301  def run_walk(mon, steps):
 6302      vq = visual_qa() if any(v in ("settle", "wait-for-change", "wake", "dismiss-dialogs")
 6303                              for v, _ in steps) else None
 6304      before, last_key = None, None
 6305      tracking = any(v == "wait-for-change" for v, _ in steps)
 6306      for verb, rest in steps:
 6307          if verb == "key":
 6308              m = re.match(r"^(\S+)(?:\s+x(\d+))?$", rest)
 6309              if not m:
 6310                  raise Fail(f"bad key step: {rest!r}")
 6311              name, times = m.group(1), int(m.group(2) or 1)
 6312              if tracking:
 6313                  # From a still screen, or the last transition's tail reads
 6314                  # as this press landing -- see tools/vm-visual-qa.
 6315                  vq.settle(mon.frame, timeout=vq.PRE_KEY_TIMEOUT, quiet=vq.PRE_KEY_QUIET)
 6316                  before = mon.frame()
 6317              last_key = (name, times)
 6318              mon.sendkey(name, times)
 6319          elif verb == "wait":
 6320              time.sleep(float(rest))
 6321          elif verb == "shot":
 6322              pass                    # frames are for people; the harness reads files
 6323          elif verb == "wake":
 6324              mon.sendkey("shift")
 6325              vq.settle(mon.frame, timeout=8.0, quiet=0.8)
 6326          elif verb == "dismiss-dialogs":
 6327              vq.dismiss_dialogs(mon.frame, mon.sendkey)
 6328          elif verb == "settle":
 6329              a = rest.split()
 6330              vq.settle(mon.frame,
 6331                        timeout=float(a[0]) if a else vq.SETTLE_TIMEOUT,
 6332                        quiet=float(a[1]) if len(a) > 1 else vq.SETTLE_QUIET)
 6333          elif verb == "wait-for-change":
 6334              if last_key is None:
 6335                  raise Fail("wait-for-change with no key step before it")
 6336              a = rest.split()
 6337              timeout = float(a[0]) if a else vq.CHANGE_TIMEOUT
 6338              retries = int(float(a[1])) if len(a) > 1 else vq.CHANGE_RETRIES
 6339              ok, _ = vq.wait_for_change(mon.frame, before, timeout=timeout)
 6340              tries = 0
 6341              while not ok and tries < retries:
 6342                  tries += 1
 6343                  mon.sendkey(*last_key)
 6344                  ok, _ = vq.wait_for_change(mon.frame, before, timeout=timeout)
 6345              if not ok:
 6346                  raise Fail(f"the walk's `key {last_key[0]}` was eaten: the screen did not change "
 6347                             f"within {timeout:.0f}s, so the page under it is not the one the walk "
 6348                             f"assumes -- read the frames of tools/vm-walks/")
 6349          else:
 6350              # Never silently: an unknown verb used to fall through, so a walk
 6351              # rewritten on a step this copy did not know would have run its
 6352              # keys back to back with no waits at all.
 6353              raise Fail(f"unknown walk step: {verb} {rest}")
 6354  
 6355  
 6356  # -- the class --------------------------------------------------------------------
 6357  
 6358  WATCH_SH = r"""#!/bin/sh
 6359  # watch.sh PIDFILE RCFILE RESULT DEADLINE SIG COND...
 6360  # Poll COND (evaluated by this shell) every 20 ms. The moment it holds, kill
 6361  # the run's process group -- the pid in PIDFILE is its setsid leader -- with
 6362  # SIG and record when. If the run ends first (RCFILE appears) record that the
 6363  # kill was missed; give up at DEADLINE seconds.
 6364  pidfile=$1; rcfile=$2; result=$3; deadline=$4; sig=$5; shift 5; cond="$*"
 6365  end=$(( $(cut -d. -f1 /proc/uptime) + deadline ))
 6366  while :; do
 6367    if eval "$cond"; then
 6368      pgid=$(cat "$pidfile" 2>/dev/null)
 6369      [ -n "$pgid" ] && kill -"$sig" -- -"$pgid" 2>/dev/null
 6370      echo "landed $(cut -d' ' -f1 /proc/uptime)" > "$result"; exit 0
 6371    fi
 6372    if [ -e "$rcfile" ]; then echo "missed $(cut -d' ' -f1 /proc/uptime)" > "$result"; exit 0; fi
 6373    if [ "$(cut -d. -f1 /proc/uptime)" -ge "$end" ]; then echo timeout > "$result"; exit 0; fi
 6374    usleep 20000
 6375  done
 6376  """
 6377  
 6378  
 6379  class Kill(Link):
 6380      """One device, its console and monitor, and the QA endpoint when a cell
 6381      needs one. Inherits the detached run, the marker wait, the receiving-side
 6382      fingerprints and the stamps from Link; adds the kill mechanisms, the
 6383      power cut, and snapshots of the two config files."""
 6384  
 6385      def __init__(self, dev, serial, root, remote, settings, args, monitor_path=None, endpoint=True):
 6386          self.dev, self.serial, self.root, self.remote, self.settings, self.args = dev, serial, root, remote, settings, args
 6387          self.restore_after = 0
 6388          self.endpoint = endpoint
 6389          self.saves_remote = settings.get("SAVES_REMOTE") or settings.get("SYNCPATH") or ""
 6390          self.settings_remote = settings.get("SETTINGS_REMOTE") or settings.get("SYNCPATH_BACKUP") or ""
 6391          self.content_remote = settings.get("CONTENT_REMOTE") or settings.get("CONTENTPATH") or ""
 6392          self.backups = settings.get("SETTINGS_BACKUPS") or settings.get("BACKUPFOLDER") or f"{root}/backup"
 6393          self.iface = dev.run("ip -4 route show default 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i==\"dev\") print $(i+1)}' | head -1",
 6394                               check=False).strip() or "eth0"
 6395          self.hostport, self.host_ip = "0.0.0.0:0", "10.0.2.2"
 6396          if endpoint:
 6397              m = re.search(r"(?:url|endpoint)\s*=\s*\w+://([^/\s]+)", backend("rclone-conf"))
 6398              if m:
 6399                  self.hostport = m.group(1)
 6400                  self.host_ip = self.hostport.split(":")[0]
 6401          self.monitor_path = monitor_path
 6402          self.t_cut = None
 6403          self.cleanups = []
 6404          self.after_restart = False
 6405          self.label = dev.run("cloud_device_id --label 2>/dev/null || true", check=False).strip()
 6406          self.device_id = dev.run("cloud_device_id 2>/dev/null || true", check=False).strip()
 6407          self.osn = os_name(dev)
 6408          keep_raw = dev.run(f"grep -m1 '^CLOUD_BACKUP_KEEP=' {CONF} 2>/dev/null | cut -d= -f2 | tr -d '\"' || true", check=False).strip()
 6409          self.keep_n = int(keep_raw) if keep_raw.isdigit() else 3
 6410          self.scratch_made = False
 6411  
 6412      def q(self, s):
 6413          return shlex.quote(s)
 6414  
 6415      def reset(self):
 6416          self.dev.run(f"rm -rf {self.q(self.root)}; mkdir -p {self.q(self.root)}; "
 6417                       f"rm -rf /storage/roms/{shlex.quote(CONTENT_DIR)} {LINK_DIR}", check=False)
 6418          if self.endpoint:
 6419              backend("reset")
 6420  
 6421      # -- the guards: the console and the monitor are this guest's -----------------
 6422      def assert_same_qemu(self):
 6423          """The monitor socket and the serial console must sit on one QEMU
 6424          command line. A `system_reset` sent to the wrong guest is a power cut
 6425          on somebody else's machine, so this fails closed before the by-effect
 6426          proof (uptime falls) can be attempted."""
 6427          mon, ser = os.path.realpath(self.monitor_path), os.path.realpath(self.serial.socket)
 6428          for pid in os.listdir("/proc"):
 6429              if not pid.isdigit():
 6430                  continue
 6431              try:
 6432                  argv = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
 6433              except OSError:
 6434                  continue
 6435              if not argv or b"qemu-system" not in argv[0]:
 6436                  continue
 6437              joined = b" ".join(argv).decode(errors="replace")
 6438              if mon in joined and ser in joined:
 6439                  return pid
 6440          raise Fail(f"no QEMU process names both {mon} (monitor) and {ser} (serial) on its command line; "
 6441                     "refusing to reset a guest the console does not belong to")
 6442  
 6443      # -- the detached run, with a prelude and an optional watcher -------------------
 6444      def start(self, cmd, env="", prelude="", shell="sh", watch=None):
 6445          """Start `cmd` detached in its own process group (setsid), the group
 6446          id in {LINK_DIR}/pid, and -- when `watch` is (condition, signal) --
 6447          a guest-side watcher polling that condition every 20 ms and killing
 6448          the group when it holds. `prelude` runs in the same shell before
 6449          `cmd` (exported function shims; QA_PGID is the group id)."""
 6450          self.dev.run(f"rm -rf {LINK_DIR}; mkdir -p {LINK_DIR}")
 6451          if watch:
 6452              cond, sig = watch
 6453              self.dev.write(KILL_WATCH, WATCH_SH.encode())     # /tmp: a power cut empties it, so every time
 6454              self.dev.run(f"setsid nohup sh {KILL_WATCH} {LINK_DIR}/pid {LINK_DIR}/rc {LINK_DIR}/watch 120 {sig} "
 6455                           f"{shlex.quote(cond)} >/dev/null 2>&1 &")
 6456          inner = (f"echo $$ > {LINK_DIR}/pid; export QA_PGID=$$; {prelude} {env} {cmd}; "
 6457                   f"echo $? $(cut -d' ' -f1 /proc/uptime) > {LINK_DIR}/rc")
 6458          self.dev.run(f"setsid nohup {shell} -c {shlex.quote(inner)} >{LINK_DIR}/out 2>&1 &")
 6459  
 6460      def pid(self):
 6461          return self.dev.run(f"cat {LINK_DIR}/pid 2>/dev/null || true", check=False).strip()
 6462  
 6463      def group_pids(self, pgid):
 6464          out = self.dev.run(f"ps -o pid,pgid 2>/dev/null | awk '$2 == {pgid} {{print $1}}'; true", check=False)
 6465          return out.split()
 6466  
 6467      def kill_group(self, sig="KILL", wait=3.0, then_kill_at=None):
 6468          """Signal the run's process group; return the seconds until no process
 6469          of the group was left, or None if some still were after `wait`.
 6470          then_kill_at is D-CLOUD-076's procedure: TERM, then KILL at that many
 6471          seconds if the group is still up."""
 6472          pgid = self.pid()
 6473          if not pgid:
 6474              raise Fail("the detached run left no pid file; nothing to kill")
 6475          self.dev.run(f"kill -{sig} -- -{pgid} 2>/dev/null; true", check=False)
 6476          t0 = time.time()
 6477          killed = False
 6478          while time.time() - t0 < wait:
 6479              if not self.group_pids(pgid):
 6480                  return time.time() - t0
 6481              if then_kill_at is not None and not killed and time.time() - t0 >= then_kill_at:
 6482                  self.dev.run(f"kill -KILL -- -{pgid} 2>/dev/null; true", check=False)
 6483                  killed = True
 6484              time.sleep(0.1)
 6485          return None if self.group_pids(pgid) else time.time() - t0
 6486  
 6487      def watch_result(self, timeout=90):
 6488          """What the watcher recorded: ('landed', guest uptime), ('missed',
 6489          uptime) when the run ended before its condition held, or ('timeout',)."""
 6490          t = time.time()
 6491          while time.time() - t < timeout:
 6492              r = self.dev.run(f"cat {LINK_DIR}/watch 2>/dev/null || true", check=False).split()
 6493              if r:
 6494                  if r[0] in ("landed", "missed"):
 6495                      # The group is gone (or was never signalled): give it a moment.
 6496                      pgid = self.pid()
 6497                      for _ in range(30):
 6498                          if not pgid or not self.group_pids(pgid):
 6499                              break
 6500                          time.sleep(0.1)
 6501                      return (r[0], float(r[1]))
 6502                  return ("timeout",)
 6503              time.sleep(0.2)
 6504          raise Fail(f"the watcher recorded nothing in {timeout}s")
 6505  
 6506      def ended(self):
 6507          """(rc, uptime) of a run that ended on its own, else None."""
 6508          return self.rc_line(self.dev.run(f"cat {LINK_DIR}/rc 2>/dev/null || true", check=False))
 6509  
 6510      def inflight(self, out):
 6511          names = KILL_MARKER_NAME.findall(out)
 6512          return names[-1] if names else ""
 6513  
 6514      @staticmethod
 6515      def shim(name, body):
 6516          """A bash function of a command's name, exported so it wins over PATH
 6517          in every bash the run starts (backuptool re-sources /etc/profile, so a
 6518          PATH directory would lose). The body may kill the group via QA_PGID."""
 6519          return f"{name}() {{ {body}; }}; export -f {name};"
 6520  
 6521      # -- the power cut -----------------------------------------------------------------
 6522      def mark(self):
 6523          """Over serial, just before a reset: the guest's uptime, its boot_id
 6524          and the wall clock. reboot_wait proves the reset against these."""
 6525          out = self.serial.run("cut -d' ' -f1 /proc/uptime; cat /proc/sys/kernel/random/boot_id", timeout=8).split()
 6526          return {"u0": float(out[0]), "boot0": out[1] if len(out) > 1 else "", "t0": time.time()}
 6527  
 6528      def reboot_wait(self, m, deadline=300, retried=False):
 6529          """After a reset: the guest's boot_id has changed and its uptime is
 6530          below what it would read had no reset happened (u0 plus the wall
 6531          time since -- a fresh boot's uptime is small, but u0 is too when the
 6532          previous boot was seconds ago), which proves the reset hit THIS
 6533          guest; exactly one emulationstation runs (`vm-serial wait` alone
 6534          returns at once while an old ES is still up); the network is back
 6535          (LINK's test); the cloud lock is free (the startup sync has run).
 6536          Then SSH reconnects on a fresh master. Returns (uptime, seconds)."""
 6537          t = time.time()
 6538          test = (f"cut -d' ' -f1 /proc/uptime; cat /proc/sys/kernel/random/boot_id; echo ES=$(pgrep emulationstation | wc -l); "
 6539                  f"ip -4 -o addr show {self.iface} | grep -q 'inet ' && ip -4 route show default | grep -q . "
 6540                  f"&& ping -c1 -W1 {self.host_ip} >/dev/null 2>&1 && echo NETOK; "
 6541                  f"flock -n {CLOUD_LOCK} true && echo LOCKFREE")
 6542          up, boot = None, ""
 6543          answered = False
 6544          while time.time() - t < deadline:
 6545              try:
 6546                  out = self.serial.run(test, timeout=8)
 6547              except Fail:
 6548                  # No shell on the console at all. Once on 2026-09-10 a reset
 6549                  # boot came up with a garbage command line (BOOT_IMAGE=<junk>,
 6550                  # no boot=/disk=) and sat in the initramfs shell on the VGA
 6551                  # console, ESP intact -- a transient of that one boot. A
 6552                  # player would power-cycle again; so does the harness, once.
 6553                  if not answered and time.time() - t > 150 and not retried:
 6554                      print("          no console shell 150s after the reset (the guest may sit in the initramfs shell); "
 6555                            "resetting once more")
 6556                      mon = Monitor(self.monitor_path)
 6557                      mon.system_reset()
 6558                      mon.close()
 6559                      return self.reboot_wait(m, deadline, retried=True)
 6560                  time.sleep(2)
 6561                  continue
 6562              answered = True
 6563              words = out.split()
 6564              try:
 6565                  up = float(words[0])
 6566                  boot = words[1]
 6567              except (IndexError, ValueError):
 6568                  time.sleep(2)
 6569                  continue
 6570              no_reset = m["u0"] + (time.time() - m["t0"])
 6571              if boot != m["boot0"] and up < no_reset - 5 and "ES=1" in words and "NETOK" in words and "LOCKFREE" in words:
 6572                  break
 6573              time.sleep(2)
 6574          else:
 6575              raise Fail(f"the guest did not come back within {deadline}s of the reset (last uptime {up}, boot_id "
 6576                         f"{'unchanged' if boot == m['boot0'] else 'changed'}; wanted a new boot_id and an uptime under "
 6577                         f"{m['u0'] + (time.time() - m['t0']) - 5:.0f})")
 6578          self.ssh_back()
 6579          self.after_restart = False
 6580          return up, time.time() - t
 6581  
 6582      def ssh_ok(self):
 6583          return self.dev.run("echo ok", check=False).strip() == "ok"
 6584  
 6585      def ssh_back(self, budget=150):
 6586          """SSH after a boot. When it does not return, the usual cause is a
 6587          system.cfg that came up as /usr/config's defaults -- ssh.enabled is
 6588          read at boot, and a boot that reseeded the file left sshd off (guest
 6589          a, 2026-09-10, after a 0 ms cut behind a page close). That is the
 6590          FINDING the cell is about to report, not a reason to abort it, so
 6591          sshd is started over serial -- the files under test are not touched
 6592          -- and said."""
 6593          t = time.time()
 6594          while time.time() - t < 30:
 6595              if self.ssh_ok():
 6596                  return
 6597              time.sleep(2)
 6598          state = self.serial.run("systemctl is-active sshd; get_setting() { grep -m1 \"^$1=\" " + SYSCFG +
 6599                                  " 2>/dev/null | cut -d= -f2; }; echo ssh.enabled=$(get_setting ssh.enabled); "
 6600                                  "wc -c < " + SYSCFG, timeout=10).split()
 6601          print(f"          ssh is not back 30s after the boot: sshd {state[0] if state else '?'}, {' '.join(state[1:])} bytes in system.cfg; "
 6602                "starting sshd over serial so the cell can read the files (the boot left it off)")
 6603          # sshd.service has ConditionPathExists=/storage/.cache/services/sshd.conf;
 6604          # 099-networkservices writes that marker from ssh.enabled at boot, so
 6605          # a boot on defaults left none and a bare `systemctl start` is a no-op.
 6606          self.serial.run("mkdir -p /storage/.cache/services; touch /storage/.cache/services/sshd.conf; systemctl start sshd", timeout=20)
 6607          while time.time() - t < budget:
 6608              if self.ssh_ok():
 6609                  return
 6610              time.sleep(2)
 6611          raise Fail(f"ssh did not come back within {budget}s of the boot, even after `systemctl start sshd` over serial")
 6612  
 6613      def run_any(self, cmd, timeout=60):
 6614          """Over SSH when it answers, over serial when it does not -- for the
 6615          restores that must happen whatever state a boot left the guest in."""
 6616          if self.serial is None or self.ssh_ok():
 6617              return self.dev.run(cmd, check=False)
 6618          return self.serial.run(cmd, timeout=timeout)
 6619  
 6620      def power_cut(self, mon=None):
 6621          """Close the SSH master (a command over it would stall across the
 6622          reset exactly as across a link cut), read the uptime over serial,
 6623          `system_reset` over the monitor, wait for the boot. Returns (uptime at
 6624          the cut, uptime when back, seconds it took)."""
 6625          self.dev.disconnect()
 6626          m = self.mark()
 6627          own = mon is None
 6628          if own:
 6629              mon = Monitor(self.monitor_path)
 6630          mon.system_reset()
 6631          if own:
 6632              mon.close()
 6633          up, took = self.reboot_wait(m)
 6634          print(f"          power cut at guest uptime {m['u0']:.0f}s; back with uptime {up:.0f}s after {took:.0f}s "
 6635                "(the monitor is this guest: its boot_id changed and its uptime fell)")
 6636          return m["u0"], up, took
 6637  
 6638      def clean_reboot(self):
 6639          """`systemctl reboot` over serial: the shutdown hook runs."""
 6640          self.dev.disconnect()
 6641          m = self.mark()
 6642          try:
 6643              self.serial.run("systemctl reboot", timeout=5)
 6644          except Fail:
 6645              pass        # the console goes with the system; no END marker is expected
 6646          up, took = self.reboot_wait(m)
 6647          print(f"          clean reboot from uptime {m['u0']:.0f}s; back with uptime {up:.0f}s after {took:.0f}s")
 6648  
 6649      # -- the two config files, put back whatever happens -------------------------------
 6650      CONFIG_FILES = [SYSCFG, f"{SYSCFG}.backup", f"{SYSCFG}.last-good", f"{SYSCFG}.tmp",
 6651                      ES_SETTINGS, f"{ES_SETTINGS}.backup", f"{ES_SETTINGS}.last-good", BACKUPTOOL_CONF, RESTORE_PENDING]
 6652  
 6653      def snapshot_configs(self, files=None):
 6654          """Archive the config files a cell disturbs, on /storage (a power cut
 6655          empties /tmp). Returns which of them existed."""
 6656          self.snap_files = list(files or self.CONFIG_FILES)
 6657          had = set(self.dev.run("for f in " + " ".join(self.snap_files) + "; do [ -e \"$f\" ] && echo \"$f\"; done; true",
 6658                                 check=False).split())
 6659          names = " ".join(shlex.quote(p.lstrip("/")) for p in sorted(had))
 6660          self.dev.run(f"rm -f {KILL_CONFIGS_TGZ}; " + (f"tar -C / -czf {KILL_CONFIGS_TGZ} {names}" if names else f": > {KILL_CONFIGS_TGZ}"))
 6661          return had
 6662  
 6663      def restore_configs_quiet(self, had):
 6664          """Put every snapshotted file back and remove the ones that did not
 6665          exist -- for cells that touched only backuptool.conf and the archives.
 6666          Over serial when SSH is gone (a boot on defaults leaves sshd off)."""
 6667          absent = [p for p in self.snap_files if p not in had]
 6668          self.run_any("rm -f " + " ".join(absent) + "; true")
 6669          if had:
 6670              self.run_any(f"tar -C / -xzf {KILL_CONFIGS_TGZ} 2>/dev/null; true")
 6671          self.run_any(f"rm -f {KILL_CONFIGS_TGZ}; sync")
 6672  
 6673      def restore_configs(self, had):
 6674          """restore_configs_quiet, then restart EmulationStation -- it holds its
 6675          settings in memory and would rewrite the restored file on its next save."""
 6676          self.restore_configs_quiet(had)
 6677          self.es_restart()
 6678  
 6679      def es_unit(self):
 6680          for u in ("essway", "emustation"):
 6681              if self.run_any(f"systemctl is-active {u} 2>/dev/null || true").strip() == "active":
 6682                  return u
 6683          return "essway"
 6684  
 6685      def es_restart(self):
 6686          unit = self.es_unit()
 6687          self.run_any(f"systemctl restart {unit}; systemctl start sshd 2>/dev/null; true")
 6688          for _ in range(30):
 6689              time.sleep(1)
 6690              if self.run_any("pgrep emulationstation | wc -l").strip() == "1":
 6691                  break
 6692          time.sleep(4)
 6693          self.after_restart = True
 6694  
 6695      # -- scratch for the archive cells -------------------------------------------------
 6696      def make_scratch(self):
 6697          """20k empty files and a 64 MiB blob under one directory, so a tar
 6698          over it -- collecting, compressing, or extracting -- runs for
 6699          seconds and a 20 ms poll lands inside it. Made once per run."""
 6700          if self.scratch_made:
 6701              return
 6702          self.dev.run(f"rm -rf {KILL_SCRATCH}; mkdir -p {KILL_SCRATCH}/many; "
 6703                       f"seq 1 {KILL_MANY} | sed 's|^|{KILL_SCRATCH}/many/f|' | xargs touch; "
 6704                       f"head -c {KILL_BLOB_MIB * 1048576} /dev/urandom > {KILL_SCRATCH}/blob.bin; sync")
 6705          self.scratch_made = True
 6706  
 6707      def remove_scratch(self):
 6708          self.dev.run(f"rm -rf {KILL_SCRATCH}", check=False)
 6709          self.scratch_made = False
 6710  
 6711      def plant_tar(self, path, stem, blob_mib=0):
 6712          """A valid .tar.gz at `path`, made on the guest, with one distinctive
 6713          member so archives can be told apart by content -- and, with
 6714          blob_mib, an incompressible member of that size so an upload lasts."""
 6715          blob = f"head -c {blob_mib * 1048576} /dev/urandom > $d/storage/.config/qa-kill/blob.bin; " if blob_mib else ""
 6716          self.dev.run(f"d=$(mktemp -d); mkdir -p $d/storage/.config/qa-kill; echo {shlex.quote(stem)} > $d/storage/.config/qa-kill/{shlex.quote(stem)}.cfg; "
 6717                       f"{blob}mkdir -p {shlex.quote(os.path.dirname(path))}; tar -czf {shlex.quote(path)} -C $d storage; rm -rf $d")
 6718  
 6719      def marker_sum(self):
 6720          """The upload marker's first field as cloud_backup computes it
 6721          (cloud_backup:1042): the md5 of the md5 list of every archive at the
 6722          root, .zip then .tar.gz."""
 6723          return self.dev.run(f"a=$(ls {self.q(self.backups)}/*.zip {self.q(self.backups)}/*.tar.gz 2>/dev/null); "
 6724                              f"[ -n \"$a\" ] && md5sum $a | md5sum | cut -d' ' -f1", check=False).strip()
 6725  
 6726      def finder(self):
 6727          """What `backuptool restore` (and RESTORE SETTINGS FROM THIS DEVICE)
 6728          would apply: the script's own newest_backup, run as run_steps runs it."""
 6729          return self.dev.run(finder_cmd('"$(command -v backuptool)"'), check=False).strip()
 6730  
 6731      def root_archives(self):
 6732          return self.dev.run(f"cd {self.q(self.backups)} 2>/dev/null && ls -1 *.tar.gz *.zip 2>/dev/null; true", check=False).split()
 6733  
 6734      def archived(self):
 6735          return self.dev.run(f"ls -1 {self.q(self.backups)}/archive/ 2>/dev/null; true", check=False).split()
 6736  
 6737      def tar_ok(self, path):
 6738          return self.dev.run(f"tar -tzf {shlex.quote(path)} >/dev/null 2>&1 && echo ok || echo BAD", check=False).strip() == "ok"
 6739  
 6740      def bash_profile(self, body):
 6741          """Run `body` in a bash that has sourced /etc/profile -- where
 6742          set_setting, get_setting and the lock live."""
 6743          return f"bash -c {shlex.quote('. /etc/profile >/dev/null 2>&1; ' + body)}"
 6744  
 6745      def count_in(self, path, needle):
 6746          """How many lines of a file on the device contain `needle`. `grep -c`
 6747          prints 0 AND exits 1 when there is none, so `|| echo 0` after it
 6748          yields "0\n0"; take the first line."""
 6749          out = self.dev.run(f"grep -c {shlex.quote(needle)} {shlex.quote(path)} 2>/dev/null; true", check=False).split()
 6750          return int(out[0]) if out and out[0].isdigit() else 0
 6751  
 6752      def clear_settings_lock(self):
 6753          """No stale lock before a set_setting cell, or wait_lock's own stale
 6754          removal would run the rm shim early."""
 6755          self.dev.run(f"h=$(cat {SYSCFG_LOCK} 2>/dev/null); if [ -z \"$h\" ] || ! kill -0 \"$h\" 2>/dev/null; then rm -f {SYSCFG_LOCK}; fi; true",
 6756                       check=False)
 6757  
 6758  
 6759  def finder_cmd(script):
 6760      """backuptool's own newest_backup, evaluated in a shell that has sourced
 6761      the profile (the globs are built on OS_NAME) and the conf. The script is
 6762      resolved BEFORE the profile rewrites PATH."""
 6763      return (f"B={script}; . /etc/profile >/dev/null 2>&1; . {CONF}; "
 6764              "eval \"$(sed -n '/^newest_backup()/,/^}/p' \"$B\")\"; newest_backup")
 6765  
 6766  
 6767  
 6768  
 6769  # -- the cells --------------------------------------------------------------------------
 6770  
 6771  def fx_kill1(L):
 6772      """KILL1: `cloud_backup --yes --saves-only` killed mid-transfer, twice --
 6773      SIGKILL (1a, nothing runs afterwards) and SIGTERM (1b, the script's trap).
 6774      Cloud holds v1 of three 3 MiB states, the device v2. After the kill the
 6775      cloud holds, per file, v1 or whole v2 -- never a truncated file under a
 6776      final name -- and no *.partial; the stamp is unchanged (1a) or 130 (1b),
 6777      never 0; the lock is released; a plain re-run exits 0 and lands all v2.
 6778  
 6779      A backend that writes into the final name preallocates it when the PUT
 6780      starts, so a file cut mid-body reads as truncated there; that is the QA
 6781      backend's artifact (LINK5), reported as SKIP with the reason, and
 6782      asserted cleanly on MinIO (--backend s3) where a PUT commits or leaves
 6783      nothing. WebDAV, SFTP, SMB and FTP all write in place (`caps` says
 6784      commit=partial); only S3 commits atomically."""
 6785      f = 0
 6786      inplace = caps()["commit"] != "atomic"
 6787      for variant, sig in (("1a", "KILL"), ("1b", "TERM")):
 6788          L.reset()
 6789          v1 = link_files("savestates/kill1-", ext="state")
 6790          # A different SIZE, not only different bytes: against the QA WebDAV
 6791          # (vendor=other, no modtime support) rclone compares by size alone --
 6792          # "Sizes identical, Unchanged skipping", proven on the guest -- so a
 6793          # same-size v2 never transfers and the kill has nothing to land in
 6794          # (#53's shape, on the saves tier). The 4 KiB is the grown save.
 6795          v2 = {rel: os.urandom(len(data) + 4096) for rel, data in v1.items()}
 6796          L.plant_cloud(v1, epath(L.saves_remote))
 6797          L.plant_device(L.root, v2)
 6798          for rel in v2:
 6799              touch_offset(L.dev, f"{L.root}/{rel}", 60)
 6800          before = L.stamps()
 6801          L.start("cloud_backup --yes --saves-only")
 6802          landed, out = L.wait_marker(LINK_MARKER_FILE)
 6803          if not landed:
 6804              r = L.ended()
 6805              f += not check(False, "", f"{variant}: the run ended (rc {r[0] if r else '?'}) before the kill could land")
 6806              continue
 6807          name = L.inflight(out)
 6808          gone = L.kill_group(sig, wait=3.0)
 6809          f += not check(gone is not None, f"{variant}: SIG{sig} mid-transfer of {name!r}: the process group was gone in {gone or 0:.2f}s",
 6810                         f"{variant}: SIG{sig} sent; processes of the group still up after 3s")
 6811          got = L.settle(("cloud", epath(L.saves_remote)))
 6812          partials = sorted(r for r in got if ".partial" in r)
 6813          f += not check(not partials, f"{variant}: no *.partial in the cloud", f"{variant}: partial files in the cloud: {partials}")
 6814          states = {}
 6815          for rel in v1:
 6816              g = got.get(rel)
 6817              states[rel] = ("absent" if g is None else "v1" if g == (len(v1[rel]), sha(v1[rel]))
 6818                             else "v2" if g == (len(v2[rel]), sha(v2[rel])) else f"TORN ({g[0]} bytes)")
 6819          torn = {r: s for r, s in states.items() if s.startswith("TORN")}
 6820          if torn and inplace:
 6821              print(f"    SKIP  {variant}: {torn} -- this endpoint ({backend('backend').strip()}) writes into the final name and "
 6822                    "keeps what arrived; a real provider resets an aborted PUT. Assert this on MinIO (--backend s3).")
 6823          else:
 6824              f += not check(not torn, f"{variant}: every file in the cloud is v1 or whole v2 ({states})",
 6825                             f"{variant}: a truncated file under a final name in the cloud: {torn} (all: {states})")
 6826          after = L.stamps()
 6827          if sig == "KILL":
 6828              f += not check(after.get("last-backup") == before.get("last-backup"),
 6829                             f"{variant}: last-backup unchanged ({after.get('last-backup') or 'absent'}) -- nothing ran after SIGKILL",
 6830                             f"{variant}: last-backup moved to {after.get('last-backup')!r} after a SIGKILL")
 6831          else:
 6832              code = (after.get("last-backup") or "").split()[1:2]
 6833              f += not check(code == ["130"] or after.get("last-backup") == before.get("last-backup"),
 6834                             f"{variant}: last-backup records the interruption ({after.get('last-backup')})",
 6835                             f"{variant}: last-backup is {after.get('last-backup')!r}: the trap should stamp 130, never 0")
 6836          free = L.dev.run(f"flock -n {CLOUD_LOCK} true && echo FREE || echo HELD", check=False).strip()
 6837          f += not check(free == "FREE", f"{variant}: the cloud lock is released", f"{variant}: the cloud lock is still held after the kill")
 6838          waited = L.endpoint_quiet()
 6839          if waited > 2:
 6840              print(f"          waited {waited:.0f}s for the endpoint to let go of the cut PUT")
 6841          mark = log_mark(L.dev)
 6842          rc2, out2 = run_rc(L.dev, "cloud_backup --yes --saves-only")
 6843          L.keep(f"KILL{variant}", out2)
 6844          got2 = L.settle(("cloud", epath(L.saves_remote)))
 6845          whole = all(got2.get(r) == (len(v2[r]), sha(v2[r])) for r in v2)
 6846          locked = webdav and rc2 != 0 and "423 Locked" in log_since(L.dev, mark)
 6847          if locked and whole:
 6848              print("    SKIP  the re-run met the QA WebDAV server's stale-PUT lock (423 Locked) on the cut file's name; "
 6849                    "everything is v2 in the cloud regardless. Assert idempotency on MinIO/S3.")
 6850          else:
 6851              f += not check(rc2 == 0, f"{variant}: a plain re-run exits 0", f"{variant}: the re-run exits {rc2}")
 6852          f += not check(whole, f"{variant}: after the re-run the cloud holds whole v2 of all {len(v2)} files",
 6853                         f"{variant}: after the re-run the cloud does not hold v2 of: {[r for r in v2 if got2.get(r) != (len(v2[r]), sha(v2[r]))]}")
 6854          f += assert_message(out2, rc2, L.args.vocabulary, label=f"{variant} re-run: ")
 6855      return f
 6856  
 6857  
 6858  def fx_kill2(L):
 6859      """KILL2: `cloud_restore --yes --method=copy --update --saves-only` -- the
 6860      startup pair's first half -- stopped mid-download. Arm 2a is
 6861      EmulationStation's own procedure (D-CLOUD-076): SIGTERM to the group,
 6862      SIGKILL at 1.5 s, two seconds in all, because a game is about to start
 6863      and a rename landing on a save the game has just written would lose it.
 6864      Arm 2b is a plain SIGKILL, the hard stop nothing handles. RCLONE_BWLIMIT=64k
 6865      on the guest keeps a 3 MiB download in flight for ~45 s.
 6866  
 6867      Asserted: the group is empty within the two-second budget (2a); a save
 6868      "the game" writes into the in-flight file one second later still stands
 6869      five seconds on (no rename landed); every other file is v1 or whole v2;
 6870      the stamp is 130 (2a) or unchanged (2b), never 0; rclone's
 6871      `<name>.<rand>.partial` under SAVESPATH is enumerated -- rclone removes
 6872      it on SIGTERM itself (found here; the design expected litter in 2a too),
 6873      so 2b is where it stays, a FAIL under the rule until a sweep lands; and
 6874      the re-run completes to v2 while KEEPING the previous local version
 6875      somewhere (`--backup-dir` -- D-CLOUD-078's "would"; a FAIL today)."""
 6876      f = 0
 6877      for variant, sig in (("2a", "TERM"), ("2b", "KILL")):
 6878          L.reset()
 6879          v1 = link_files("savestates/kill2-", ext="state")
 6880          v2 = {rel: os.urandom(len(data)) for rel, data in v1.items()}
 6881          L.plant_device(L.root, v1)
 6882          for rel in v1:
 6883              touch_offset(L.dev, f"{L.root}/{rel}", -3600)
 6884          L.plant_cloud(v2, epath(L.saves_remote))
 6885          before = L.stamps()
 6886          L.start("cloud_restore --yes --method=copy --update --saves-only", env="RCLONE_BWLIMIT=64k")
 6887          landed, out = L.wait_marker(LINK_MARKER_FILE, timeout=180)
 6888          if not landed:
 6889              r = L.ended()
 6890              f += not check(False, "", f"{variant}: the run ended (rc {r[0] if r else '?'}) before the stop could land")
 6891              continue
 6892          name = L.inflight(out)
 6893          t_sig = time.time()
 6894          if sig == "TERM":
 6895              gone = L.kill_group("TERM", wait=2.5, then_kill_at=1.5)
 6896              f += not check(gone is not None and gone <= 2.0,
 6897                             f"{variant}: TERM then KILL at 1.5s: the group was empty {gone or 0:.2f}s after the signal (budget 2s), mid-download of {name!r}",
 6898                             f"{variant}: the group was {'still up after 2.5s' if gone is None else f'gone only after {gone:.2f}s'} -- past D-CLOUD-076's two-second budget")
 6899          else:
 6900              gone = L.kill_group("KILL", wait=3.0)
 6901              f += not check(gone is not None, f"{variant}: SIGKILL mid-download of {name!r}: the group was gone in {gone or 0:.2f}s",
 6902                             f"{variant}: processes of the group still up 3s after SIGKILL")
 6903          time.sleep(max(0, 1.0 - (time.time() - t_sig)))
 6904          v3 = os.urandom(len(v1[name])) if name in v1 else os.urandom(3 * 1048576)
 6905          game_path = f"{L.root}/{name}" if name in v1 else f"{L.root}/savestates/kill2-1.state"
 6906          L.dev.write(game_path, v3)
 6907          # Newer than anything the cloud holds, so the re-run's --update leaves
 6908          # it alone: the hazard under test is the rename, not the comparison.
 6909          touch_offset(L.dev, game_path, 120)
 6910          time.sleep(5)
 6911          now = L.dev.sha(game_path)
 6912          f += not check(now == sha(v3), f"{variant}: the save the game wrote 1s after the stop still stands 5s later (no rename landed on it)",
 6913                         f"{variant}: THE GAME'S SAVE WAS OVERWRITTEN: {game_path} is {name_of(now, {'v1': v1.get(name, b''), 'v2': v2.get(name, b'')})}")
 6914          got = L.fingerprint(("device", L.root))
 6915          others = {}
 6916          for rel in v1:
 6917              if f"{L.root}/{rel}" == game_path:
 6918                  continue
 6919              g = got.get(rel)
 6920              others[rel] = ("absent" if g is None else "v1" if g == (len(v1[rel]), sha(v1[rel]))
 6921                             else "v2" if g == (len(v2[rel]), sha(v2[rel])) else f"TORN ({g[0]} bytes)")
 6922          f += not check(all(not st.startswith("TORN") and st != "absent" for st in others.values()),
 6923                         f"{variant}: every other file is v1 or whole v2 ({others})", f"{variant}: a file is torn or gone: {others}")
 6924          partials = [r for r in got if ".partial" in r]
 6925          f += not check(not partials, f"{variant}: no rclone *.partial left under SAVESPATH",
 6926                         f"{variant}: rclone's temporary copy left under SAVESPATH, and nothing removes it: {partials} (D-CLOUD-078: litter forever)")
 6927          after = L.stamps()
 6928          code = (after.get("last-restore") or "").split()[1:2]
 6929          if sig == "TERM":
 6930              f += not check(code == ["130"] or after.get("last-restore") == before.get("last-restore"),
 6931                             f"{variant}: last-restore is {after.get('last-restore') or 'unchanged/absent'}: the stop is recorded, never as 0",
 6932                             f"{variant}: last-restore is {after.get('last-restore')!r} after a stopped run")
 6933          else:
 6934              f += not check(after.get("last-restore") == before.get("last-restore"),
 6935                             f"{variant}: last-restore unchanged ({after.get('last-restore') or 'absent'}) -- nothing ran after SIGKILL",
 6936                             f"{variant}: last-restore moved to {after.get('last-restore')!r} after SIGKILL")
 6937          rc2, out2 = run_rc(L.dev, "cloud_restore --yes --method=copy --update --saves-only")
 6938          L.keep(f"KILL{variant}", out2)
 6939          f += not check(rc2 == 0, f"{variant}: a plain re-run exits 0", f"{variant}: the re-run exits {rc2}: {last_player_line(out2)[:100]!r}")
 6940          got2 = L.fingerprint(("device", L.root))
 6941          expect = {rel: ("v3" if f"{L.root}/{rel}" == game_path else "v2") for rel in v1}
 6942          have = {}
 6943          for rel in v1:
 6944              g = got2.get(rel)
 6945              have[rel] = ("v3" if g == (len(v3), sha(v3)) else "v2" if g == (len(v2[rel]), sha(v2[rel]))
 6946                           else "v1" if g == (len(v1[rel]), sha(v1[rel])) else "absent" if g is None else "TORN")
 6947          f += not check(have == expect, f"{variant}: after the re-run: the game's save kept, the rest v2 ({have})",
 6948                         f"{variant}: after the re-run the tree is {have}, expected {expect}")
 6949          overwritten = [rel for rel in v1 if have.get(rel) == "v2"]
 6950          kept = L.dev.run(f"find {L.q(L.root)} {CACHE} -type f 2>/dev/null | while read -r p; do sha256sum \"$p\"; done | cut -d' ' -f1; true",
 6951                           check=False).split()
 6952          missing = [rel for rel in overwritten if sha(v1[rel]) not in kept]
 6953          f += not check(not missing, f"{variant}: the previous version of every overwritten save is kept somewhere ({len(overwritten)} checked)",
 6954                         f"{variant}: the previous version of {missing} is kept NOWHERE: the restore overwrote it with no --backup-dir (D-CLOUD-078)")
 6955          f += assert_message(out2, rc2, L.args.vocabulary, label=f"{variant} re-run: ")
 6956      return f
 6957  
 6958  
 6959  def kill_backuptool_prestate(L, tag):
 6960      """A good archive A at the root and two older ones in archive/, under a
 6961      backuptool.conf whose LOCATIONS is the scratch directory (20k files and
 6962      a 64 MiB blob) so collecting and compressing take seconds. Returns A."""
 6963      L.make_scratch()
 6964      broot = L.backups
 6965      A = f"2026_03_01-000000-{L.label + '-' if L.label else ''}{L.osn}_SETTINGS.tar.gz"
 6966      L.dev.run(f"rm -rf {L.q(broot)}; mkdir -p {L.q(broot)}/archive")
 6967      L.plant_tar(f"{broot}/{A}", f"{tag}-A")
 6968      for d in (1, 2):
 6969          L.plant_tar(f"{broot}/archive/2026_02_0{d}-000000-{L.label + '-' if L.label else ''}{L.osn}_SETTINGS.tar.gz", f"{tag}-old{d}")
 6970      L.dev.write(BACKUPTOOL_CONF, f"LOCATIONS=(\n  {KILL_SCRATCH}\n)\n".encode())
 6971      L.dev.run("sync")
 6972      return A
 6973  
 6974  
 6975  def fx_kill3(L):
 6976      """KILL3: `backuptool backup` killed mid-rotation. Since 2026-09-10 the
 6977      new archive is written to .partial, listed back, renamed into place, and
 6978      ONLY THEN is the previous archive A moved into archive/ and the folder
 6979      trimmed (D-CLOUD-078: the previous copy stays until the new one is
 6980      verifiably there). The watcher fires the moment archive/A exists, which is
 6981      now after the new archive is at the root and before trim_archive runs.
 6982      Asserted: newest_backup and the root glob find the new, valid archive (a
 6983      restore or a cloud upload right now would use it); A is in archive/;
 6984      archive/ holds at most ARCHIVE_KEEP; a re-run leaves exactly one valid
 6985      archive at the root and keeps A -- rotation trims by the date in the name,
 6986      so the oldest planted archive goes, not A. Before the change the archive
 6987      was moved first and a kill here left the root empty ("No settings backup
 6988      found"); the old watcher also tested `ls root/*.tar.gz root/*.zip`, which
 6989      fails whenever no .zip matches, so it fired on any state at all."""
 6990      f = 0
 6991      had = L.snapshot_configs([BACKUPTOOL_CONF])
 6992      try:
 6993          A = kill_backuptool_prestate(L, "kill3")
 6994          broot = L.backups
 6995          cond = f"[ -e {shlex.quote(broot + '/archive/' + A)} ]"
 6996          L.start("backuptool backup", shell="bash", watch=(cond, "KILL"))
 6997          r = L.watch_result()
 6998          f += not check(r[0] == "landed", f"the kill landed mid-rotation (archive/{A} present)",
 6999                         f"the kill did not land: watcher says {r}; the run {'ended first' if r[0] == 'missed' else 'never opened the window'}")
 7000          newest = L.finder()
 7001          roots = L.root_archives()
 7002          f += not check(len(roots) == 1 and roots[0] != A and L.tar_ok(f"{broot}/{roots[0]}") and newest == f"{broot}/{roots[0]}",
 7003                         f"the new archive is at the root, lists, and is what newest_backup finds ({roots[0] if roots else 'none'})",
 7004                         f"root holds {roots or 'no archive'}; newest_backup finds {os.path.basename(newest) or 'nothing'}")
 7005          f += not check(A in L.archived(), "A is in archive/", f"A is not in archive/: {L.archived()}")
 7006          f += not check(len(L.archived()) <= 3, f"archive/ holds {len(L.archived())} (<= ARCHIVE_KEEP)", f"archive/ holds {len(L.archived())}")
 7007          rc2, out2 = run_rc(L.dev, "backuptool backup")
 7008          L.keep("KILL3", out2)
 7009          roots2 = L.root_archives()
 7010          f += not check(rc2 == 0 and len(roots2) == 1 and roots2[0] not in (A, roots[0] if roots else "") and L.tar_ok(f"{broot}/{roots2[0]}"),
 7011                         f"a re-run leaves exactly one valid archive at the root ({roots2[0] if roots2 else 'none'})",
 7012                         f"after the re-run (rc {rc2}) the root holds {roots2}")
 7013          f += not check(A in L.archived() and len(L.archived()) <= 3,
 7014                         f"and archive/ keeps A, trimmed by the date in the name to {len(L.archived())}",
 7015                         f"archive/ after the re-run: {L.archived()} (A {'kept' if A in L.archived() else 'GONE -- trimmed by mtime, not by name'})")
 7016          f += assert_message(out2, rc2, L.args.vocabulary, label="re-run: ")
 7017      finally:
 7018          L.restore_configs_quiet(had)
 7019      return f
 7020  
 7021  def fx_kill4(L):
 7022      """KILL4: `backuptool backup` killed mid-`tar -czf`, once the new archive
 7023      at its FINAL dated name has grown past 1 MiB (the 64 MiB blob keeps gzip
 7024      busy). Asserted: what the readers find passes `tar -tzf` -- FAILS today,
 7025      the truncated archive is newest and A is already rotated away; nothing
 7026      invalid is uploaded by cloud_backup --system-only afterwards -- FAILS
 7027      today, no integrity check before upload (cloud_backup:1110-1129); no
 7028      truncated file under a final name at the root; a re-run leaves one valid
 7029      archive at the root."""
 7030      f = 0
 7031      had = L.snapshot_configs([BACKUPTOOL_CONF])
 7032      try:
 7033          A = kill_backuptool_prestate(L, "kill4")
 7034          broot = L.backups
 7035          cond = (f"f=$(ls {shlex.quote(broot)}/*.tar.gz 2>/dev/null | grep -v {shlex.quote(A)} | head -1); "
 7036                  f"[ -n \"$f\" ] && [ \"$(stat -c %s \"$f\" 2>/dev/null || echo 0)\" -gt 1048576 ]")
 7037          L.start("backuptool backup", shell="bash", watch=(cond, "KILL"))
 7038          r = L.watch_result()
 7039          f += not check(r[0] == "landed", "the kill landed while tar was writing the new archive",
 7040                         f"the kill did not land: watcher says {r}")
 7041          newest = L.finder()
 7042          roots = L.root_archives()
 7043          truncated = [n for n in roots if not L.tar_ok(f"{broot}/{n}")]
 7044          f += not check(bool(newest) and L.tar_ok(newest),
 7045                         f"what the readers find passes tar -tzf ({os.path.basename(newest)})",
 7046                         f"the readers find {os.path.basename(newest) or 'nothing'}, which {'is truncated' if newest else 'does not exist'}; "
 7047                         f"A is already in archive/ (FAIL today: backuptool:413 writes the final name directly)")
 7048          f += not check(not truncated, "no truncated archive under a final name at the root",
 7049                         f"truncated archive(s) under a final name at the root: {truncated}")
 7050          if L.endpoint and L.settings_remote and L.device_id:
 7051              folder = f"{epath(L.settings_remote)}/{L.device_id}"
 7052              L.dev.run(f"rm -f {CACHE}/settings-backup.uploaded", check=False)
 7053              rc_up, out_up = run_rc(L.dev, "cloud_backup --yes --system-only")
 7054              cloud = backend_files(folder)
 7055              bad_up = [n for n in cloud if n in truncated]
 7056              f += not check(not bad_up, f"cloud_backup --system-only uploaded no invalid archive (rc {rc_up}; cloud holds {cloud})",
 7057                             f"cloud_backup --system-only UPLOADED A TRUNCATED ARCHIVE as this device's newest: {bad_up} (rc {rc_up}; no integrity check)")
 7058              f += assert_message(out_up, rc_up, L.args.vocabulary, label="settings upload: ")
 7059          else:
 7060              print("    SKIP  the upload half needs the QA endpoint (run without --only KILL4 alone, or with it prepared)")
 7061          rc2, out2 = run_rc(L.dev, "backuptool backup")
 7062          L.keep("KILL4", out2)
 7063          roots2 = L.root_archives()
 7064          f += not check(rc2 == 0 and len(roots2) == 1 and L.tar_ok(f"{broot}/{roots2[0]}"),
 7065                         f"a re-run leaves exactly one valid archive at the root ({roots2[0] if roots2 else 'none'})",
 7066                         f"after the re-run (rc {rc2}) the root holds {roots2} ({[n for n in roots2 if not L.tar_ok(f'{broot}/{n}')]} invalid)")
 7067          f += assert_message(out2, rc2, L.args.vocabulary, label="re-run: ")
 7068      finally:
 7069          L.restore_configs_quiet(had)
 7070      return f
 7071  
 7072  
 7073  def fx_kill5(L):
 7074      """KILL5: `cloud_backup --yes --system-only` killed (SIGKILL) mid-copyto
 7075      of a 6 MiB archive (LINK5's shape). The marker is planted as
 7076      `<hash of a previous archive> <dest>`; the cloud folder holds three own
 7077      labelled archives, one other device's, one unlabelled, and a device.json
 7078      with distinctive bytes. Asserted: the marker is byte-identical; all five
 7079      planted archives are still there (retention did not run); device.json is
 7080      unchanged; last-settings-backup is never 0; the re-run writes the marker
 7081      as `<new hash> <dest>`, trims this device's archives to CLOUD_BACKUP_KEEP,
 7082      leaves the others, and there is exactly one device.json.
 7083  
 7084      WebDAV and MinIO differ on the receiving side (a preallocated final name
 7085      and a stale-PUT lock against a PUT that commits or leaves nothing); run it
 7086      once on each, as the pair fixtures prescribe."""
 7087      f = 0
 7088      if not L.device_id or not L.label:
 7089          raise Fail("cloud_device_id gave no id or label; cannot name the folder")
 7090      L.reset()
 7091      webdav = backend("backend").strip() == "webdav"
 7092      broot = L.backups
 7093      folder = f"{epath(L.settings_remote)}/{L.device_id}"
 7094      own = [f"2026_01_0{d}-000000-{L.label}-{L.osn}_SETTINGS.tar.gz" for d in (2, 3, 4)]
 7095      other = f"2026_01_01-000000-Other-Handheld-{L.osn}_SETTINGS.tar.gz"
 7096      unlabelled = f"2026_01_01-000000-{L.osn}_SETTINGS.tar.gz"
 7097      device_json = b'{"id": "planted-by-KILL5", "distinctive": "' + os.urandom(8).hex().encode() + b'"}\n'
 7098      planted = {n: n.encode() for n in own + [other, unlabelled]}
 7099      planted["device.json"] = device_json
 7100      L.plant_cloud(planted, folder)
 7101      archive = f"2026_02_01-000000-{L.label}-{L.osn}_SETTINGS.tar.gz"
 7102      L.dev.run(f"rm -rf {L.q(broot)}; mkdir -p {L.q(broot)}")
 7103      L.plant_tar(f"{broot}/{archive}", "kill5", blob_mib=6)       # ~30 s in flight at 200k
 7104      body_sha = L.dev.sha(f"{broot}/{archive}")
 7105      body_len = int(L.dev.run(f"stat -c %s {L.q(broot)}/{archive}").strip())
 7106      expect_sum = L.marker_sum()
 7107      dest = f"{L.remote}:{L.settings_remote}/{L.device_id}"
 7108      marker0 = f"{sha(b'the previous archive')} {dest}\n"
 7109      L.dev.write(f"{CACHE}/settings-backup.uploaded", marker0.encode())
 7110      before = L.stamps()
 7111      L.start("cloud_backup --yes --system-only")
 7112      landed, out = L.wait_marker(LINK_MARKER_FILE)
 7113      if not landed:
 7114          r = L.ended()
 7115          return f + (not check(False, "", f"the run ended (rc {r[0] if r else '?'}) before the kill could land"))
 7116      gone = L.kill_group("KILL", wait=3.0)
 7117      f += not check(gone is not None, f"SIGKILL mid-copyto of {L.inflight(out)!r}: the group was gone in {gone or 0:.2f}s", "the group is still up")
 7118      after = L.stamps()
 7119      f += not check(after.get("settings-backup.uploaded") == marker0.strip(),
 7120                     "settings-backup.uploaded is byte-identical (the upload was never confirmed)",
 7121                     f"the marker moved: {after.get('settings-backup.uploaded')!r}")
 7122      cloud = backend_files(folder)
 7123      still = [n for n in own + [other, unlabelled] if n in cloud]
 7124      f += not check(len(still) == 5, "all five planted archives are still in the folder (retention did not run)",
 7125                     f"planted archives missing after a killed upload: {[n for n in own + [other, unlabelled] if n not in cloud]}")
 7126      f += not check(backend_bytes(f"{folder}/device.json") == device_json, "device.json is unchanged",
 7127                     f"device.json changed on a killed run: {(backend_bytes(f'{folder}/device.json') or b'')[:60]!r}")
 7128      f += not check(after.get("last-settings-backup") == before.get("last-settings-backup"),
 7129                     f"last-settings-backup unchanged ({after.get('last-settings-backup') or 'absent'})",
 7130                     f"last-settings-backup moved to {after.get('last-settings-backup')!r} after SIGKILL")
 7131      waited = L.endpoint_quiet()
 7132      if waited > 2:
 7133          print(f"          waited {waited:.0f}s for the endpoint to let go of the cut PUT")
 7134      mark = log_mark(L.dev)
 7135      rc2, out2 = run_rc(L.dev, "cloud_backup --yes --system-only")
 7136      L.keep("KILL5", out2)
 7137      cloud2 = backend_files(folder)
 7138      got_body = backend_bytes(f"{folder}/{archive}")
 7139      whole = got_body is not None and len(got_body) == body_len and sha(got_body) == body_sha
 7140      locked = webdav and rc2 != 0 and "423 Locked" in log_since(L.dev, mark)
 7141      if locked and whole:
 7142          print("    SKIP  the re-run met the QA WebDAV server's stale-PUT lock (423 Locked) on the same archive name; "
 7143                "the archive is whole in the cloud. The marker/retention checks below are judged on what a locked re-run leaves.")
 7144      else:
 7145          f += not check(rc2 == 0, "a plain re-run exits 0", f"the re-run exits {rc2}: {last_player_line(out2)[:100]!r}")
 7146          marker2 = L.stamps().get("settings-backup.uploaded", "")
 7147          f += not check(marker2.split()[:1] == [expect_sum] and marker2.endswith(f"/{L.device_id}"),
 7148                         f"the marker now says <hash of the archives> <dest> ({marker2[:12]}... {marker2.split()[-1] if marker2 else ''})",
 7149                         f"the marker after the re-run is {marker2!r}, expected {expect_sum} <dest ending /{L.device_id}>")
 7150          mine = sorted(n for n in cloud2 if re.fullmatch(rf"\d{{4}}_\d\d_\d\d-\d{{6}}-{re.escape(L.label)}-{re.escape(L.osn)}_SETTINGS\.tar\.gz", n))
 7151          f += not check(mine == sorted(own[1:] + [archive]),
 7152                         f"this device's archives trimmed to CLOUD_BACKUP_KEEP={L.keep_n}, oldest first ({mine})",
 7153                         f"retention left {mine}, expected {sorted(own[1:] + [archive])}")
 7154      f += not check(other in cloud2 and unlabelled in cloud2, "another device's archive and the unlabelled one were left alone",
 7155                     f"RETENTION REMOVED WHAT IS NOT THIS DEVICE'S: {[n for n in (other, unlabelled) if n not in cloud2]}")
 7156      f += not check(cloud2.count("device.json") == 1, "exactly one device.json", f"{cloud2.count('device.json')} device.json")
 7157      f += not check(whole, "the archive is whole in the cloud", "the archive in the cloud is not the one sent")
 7158      f += assert_message(out2, rc2, L.args.vocabulary, label="re-run: ")
 7159      return f
 7160  
 7161  
 7162  def fx_kill10(L):
 7163      """KILL10: `set_setting k v` killed mid-write. Since 2026-09-10 the writer
 7164      is one awk into system.cfg.tmp and a rename over system.cfg; the override
 7165      is an `awk` function in the calling shell that kills the group, so the
 7166      shell has opened system.cfg.tmp (empty) and nothing has been renamed.
 7167      Asserted: the value stands (k=old); the temporary is present after the
 7168      kill and gone after the re-run, which replaces it (chksysconfig verify
 7169      sweeps one at boot as well); the stale /tmp/.system.cfg.lock is removed by
 7170      the next wait_lock within 2 s (wait-lock-test's property); the re-run sets
 7171      k=v. Before, a `sed -i` with `/^k=/d` and `$a k=v` lost the key whenever
 7172      its line was the file's last -- which a freshly appended key always is."""
 7173      f = 0
 7174      key = "qa.kill10"
 7175      L.clear_settings_lock()
 7176      L.dev.run(L.bash_profile(f"set_setting {key} old"))
 7177      b0 = L.dev.sha(f"{SYSCFG}.backup")
 7178      L.cleanups.append(lambda: L.dev.run(L.bash_profile(f"del_setting {key}") + f"; rm -f {SYSCFG}.tmp", check=False))
 7179      body = (f"awk() {{ kill -KILL -- -$QA_PGID; }}; "
 7180              f"set_setting {key} new")
 7181      L.start(L.bash_profile(body), shell="bash")
 7182      for _ in range(50):
 7183          if not L.pid() or not L.group_pids(L.pid()):
 7184              break
 7185          time.sleep(0.1)
 7186      val = L.dev.run(L.bash_profile(f"grep '^{key}=' {SYSCFG} | cut -d= -f2"), check=False).strip()
 7187      f += not check(val == "old", f"{key} still reads old after the kill mid-write", f"{key} reads {val!r} after a kill mid-write")
 7188      f += not check(L.dev.run(f"[ -e {SYSCFG}.tmp ] && echo yes || echo no", check=False).strip() == "yes",
 7189                     "the writer's temporary (system.cfg.tmp) is present after the kill",
 7190                     "the kill did not land inside the writer: no system.cfg.tmp")
 7191      stale = L.dev.run(f"cat {SYSCFG_LOCK} 2>/dev/null || echo none", check=False).strip()
 7192      t0 = time.time()
 7193      rc2, out2 = run_rc(L.dev, L.bash_profile(f"set_setting {key} new"))
 7194      took = time.time() - t0
 7195      val2 = L.dev.run(f"grep '^{key}=' {SYSCFG} | cut -d= -f2", check=False).strip()
 7196      f += not check(rc2 == 0 and val2 == "new" and took < 5,
 7197                     f"the re-run cleared the stale lock (held by pid {stale}) and set {key}=new in {took:.1f}s",
 7198                     f"the re-run took {took:.1f}s (rc {rc2}) and {key} reads {val2!r}; lock was {stale!r}")
 7199      f += not check(L.dev.run(f"[ -e {SYSCFG}.tmp ] && echo yes || echo no", check=False).strip() == "no",
 7200                     "and the re-run replaced the temporary (none left)", "system.cfg.tmp is still there after the re-run")
 7201      f += not check(L.dev.sha(f"{SYSCFG}.backup") == b0, "system.cfg.backup untouched", "system.cfg.backup changed")
 7202      return f
 7203  
 7204  
 7205  def fx_kill11(L):
 7206      """KILL11: `set_setting k v` killed the moment the lock is released. It
 7207      used to be released between the delete and the add, so the kill found
 7208      the key gone (empty = the default); since 2026-09-10 the write is one
 7209      rename under one lock hold and the release comes after it, so the kill
 7210      finds the new value in place. Asserted: get_setting k is old or new and
 7211      never empty -- the previous value is not lost, whichever side of the
 7212      rename the kill lands; .backup untouched; a re-run sets k=v. The override
 7213      is an `rm` function that runs the real rm and kills when its target is
 7214      the lock."""
 7215      f = 0
 7216      key = "qa.kill11"
 7217      L.clear_settings_lock()
 7218      L.dev.run(L.bash_profile(f"set_setting {key} old"))
 7219      b0 = L.dev.sha(f"{SYSCFG}.backup")
 7220      L.cleanups.append(lambda: L.dev.run(L.bash_profile(f"del_setting {key}"), check=False))
 7221      body = (f"rm() {{ command rm \"$@\"; if [ \"$2\" = \"$J_CONF_LOCK\" ]; then kill -KILL -- -$QA_PGID; fi; }}; "
 7222              f"set_setting {key} new")
 7223      L.start(L.bash_profile(body), shell="bash")
 7224      for _ in range(50):
 7225          if not L.pid() or not L.group_pids(L.pid()):
 7226              break
 7227          time.sleep(0.1)
 7228      val = L.dev.run(L.bash_profile(f"get_setting {key}"), check=False).strip()
 7229      f += not check(val in ("old", "new"), f"{key} reads {val!r} after the kill at the lock release: old or new, never lost",
 7230                     f"{key} reads {val!r} (empty = the default): the value was LOST across the write")
 7231      f += not check(L.dev.sha(f"{SYSCFG}.backup") == b0, "system.cfg.backup untouched", "system.cfg.backup changed")
 7232      rc2, _ = run_rc(L.dev, L.bash_profile(f"set_setting {key} new"))
 7233      val2 = L.dev.run(f"grep '^{key}=' {SYSCFG} | cut -d= -f2", check=False).strip()
 7234      f += not check(rc2 == 0 and val2 == "new", f"the re-run set {key}=new", f"the re-run (rc {rc2}) left {key}={val2!r}")
 7235      return f
 7236  
 7237  
 7238  def torn_shapes(good):
 7239      """(b1) cut so system.hostname is lost; (b2) cut inside the last line
 7240      with the hostname kept. Both computed from the good file's own bytes."""
 7241      b1 = good[: max(1, int(len(good) * 0.4))]
 7242      if b"system.hostname=" in b1:
 7243          b1 = good[: good.index(b"system.hostname=")]
 7244      last_nl = good.rstrip(b"\n").rfind(b"\n")
 7245      b2 = good[: last_nl + 1 + max(1, (len(good) - last_nl - 1) // 2)]
 7246      if b"system.hostname=" not in b2:
 7247          b2 = None
 7248      return b1, b2
 7249  
 7250  
 7251  def fx_kill12(L):
 7252      """KILL12: what `chksysconfig verify` (autostart/001-setup:27) does at boot
 7253      with a planted system.cfg: (a) empty, (b1) truncated with system.hostname
 7254      lost, (b2) truncated with it kept, (c) valid, (d) binary garbage -- today's
 7255      only handled case, the positive control. Each is planted over SSH,
 7256      synced, and followed by a power cut (the shutdown hook does not run).
 7257      Arm C plants (a) and reboots CLEANLY, so save-sysconfig.service runs
 7258      `chksysconfig backup`.
 7259  
 7260      Pre-state: a known-good .backup (D-CLOUD-079's record) and a distinctive
 7261      value in es_settings.cfg. Asserted per D-CLOUD-079: after boot system.cfg
 7262      equals the record (compared as key=value maps; sort_settings rewrites the
 7263      file at every boot) in (a)(b1)(b2)(d) and is untouched in (c); the planted
 7264      ES value survives; the record is still the good copy; a `logger -t
 7265      chksysconfig` line names the recovery. Today (a) and (b1) trigger
 7266      `rsync -a /usr/config/ /storage/.config` (chksysconfig:31), which resets
 7267      es_settings.cfg and retroarch.cfg to defaults too -- #102's "defaults
 7268      won"; (b2) stands, nothing said; arm C copies the empty file over the good
 7269      record (chksysconfig:13).
 7270  
 7271      What the VM cannot prove: an SD card's write cache and FTL on power loss;
 7272      the reset drops dirty pages, which a card may also do to blocks the
 7273      kernel believed written."""
 7274      f = 0
 7275      L.assert_same_guest()
 7276      L.assert_same_qemu()
 7277      had = L.snapshot_configs()
 7278      try:
 7279          good = L.dev.run(f"cat {SYSCFG}", check=False)
 7280          ok, why = valid_syscfg(good)
 7281          if not ok:
 7282              raise Fail(f"the device's own system.cfg is not valid ({why}); cannot stage a known-good record")
 7283          # A key only the good copy carries. Whole-map equality is the wrong
 7284          # test: sort_settings rewrites the file at every boot and the boot
 7285          # scripts add keys, so "the last known good" is judged by this
 7286          # marker and the hostname, "defaults" by the marker's absence.
 7287          if "qa.kill12.marker=" not in good:
 7288              good = good.rstrip("\n") + "\nqa.kill12.marker=kept\n"
 7289          good = good.encode()
 7290          good_map = parse_syscfg(good.decode())
 7291          hostname = good_map.get("system.hostname", "")
 7292  
 7293          def state_of(text):
 7294              m = parse_syscfg(text)
 7295              ok_, why_ = valid_syscfg(text)
 7296              if not ok_:
 7297                  return "INVALID", f"invalid ({why_})"
 7298              if m.get("qa.kill12.marker") == "kept" and m.get("system.hostname") == hostname:
 7299                  return "GOOD", f"the last known good ({len(m)} keys)"
 7300              return "DEFAULTS", f"defaults -- the planted marker is gone ({len(m)} keys)"
 7301  
 7302          L.dev.write(SYSCFG, good)
 7303          L.dev.write(f"{SYSCFG}.backup", good)
 7304          L.cleanups.append(lambda: L.dev.run(L.bash_profile("del_setting qa.kill12.marker"), check=False))
 7305          es0 = L.dev.run(f"cat {ES_SETTINGS}", check=False)
 7306          marker = '  <string name="QaKill12Marker" value="kept" />\n'
 7307          es_marked = (es0.replace("</config>", marker + "</config>") if "</config>" in es0
 7308                       else f'<?xml version="1.0"?>\n<config>\n{marker}</config>\n')
 7309          b1, b2 = torn_shapes(good)
 7310          cases = [("a", b"", "empty"), ("b1", b1, f"truncated to {len(b1)} bytes, system.hostname lost"),
 7311                   ("b2", b2, f"truncated to {len(b2 or b'')} bytes inside the last line, system.hostname kept"),
 7312                   ("c", good, "valid"), ("d", os.urandom(4096), "binary garbage")]
 7313          for case, body, shape in cases:
 7314              if body is None:
 7315                  print(f"    SKIP  ({case}) cannot cut this file inside its last line and keep the hostname")
 7316                  continue
 7317              print(f"    -- ({case}) system.cfg planted {shape}")
 7318              L.dev.write(SYSCFG, body)
 7319              L.dev.write(ES_SETTINGS, es_marked.encode())
 7320              L.dev.run("sync")
 7321              L.power_cut()
 7322              now = L.dev.run(f"cat {SYSCFG} 2>/dev/null || true", check=False)
 7323              rec = L.dev.run(f"cat {SYSCFG}.backup 2>/dev/null || true", check=False)
 7324              es = L.dev.run(f"cat {ES_SETTINGS} 2>/dev/null || true", check=False)
 7325              logged = int(L.dev.run("journalctl -t chksysconfig -o cat --no-pager 2>/dev/null | wc -l", check=False).strip() or 0)
 7326              state, said = state_of(now)
 7327              f += not check(state == "GOOD",
 7328                             f"({case}) after boot system.cfg is {said}",
 7329                             f"({case}) after boot system.cfg is {said}" + (" -- chksysconfig:21-32 restores only a 'binary' file and reseeds /usr/config for a missing hostname"
 7330                                                                          if case in ("a", "b1") else " -- a truncated text file stands, nothing said" if case == "b2" else ""))
 7331              f += not check("QaKill12Marker" in es,
 7332                             f"({case}) the planted es_settings.cfg value survived the boot",
 7333                             f"({case}) es_settings.cfg was RESET TO DEFAULTS by `rsync -a /usr/config/ /storage/.config` (#102: every differing file goes)")
 7334              f += not check(state_of(rec)[0] == "GOOD", f"({case}) system.cfg.backup is still the good copy",
 7335                             f"({case}) system.cfg.backup is no longer the good copy ({state_of(rec)[1]})")
 7336              if case != "c":
 7337                  f += not check(logged > 0, f"({case}) `logger -t chksysconfig` recorded the recovery ({logged} line(s) this boot)",
 7338                                 f"({case}) nothing in the journal from chksysconfig this boot: the recovery, or its absence, is silent")
 7339          print("    -- (arm C) system.cfg planted empty, then a CLEAN reboot so save-sysconfig.service runs `chksysconfig backup`")
 7340          L.dev.write(SYSCFG, b"")
 7341          L.dev.write(ES_SETTINGS, es_marked.encode())
 7342          L.dev.run("sync")
 7343          L.clean_reboot()
 7344          rec = L.dev.run(f"cat {SYSCFG}.backup 2>/dev/null || true", check=False)
 7345          now = L.dev.run(f"cat {SYSCFG} 2>/dev/null || true", check=False)
 7346          f += not check(state_of(rec)[0] == "GOOD",
 7347                         "(arm C) the shutdown hook kept the good record when the live file was empty",
 7348                         f"(arm C) system.cfg.backup after a clean reboot is {state_of(rec)[1]}: chksysconfig:13 copied the empty live file over the good copy; "
 7349                         f"system.cfg came up as {state_of(now)[1]}")
 7350      finally:
 7351          L.restore_configs(had)
 7352      return f
 7353  
 7354  
 7355  def classify(parsed, s0, toggle_key, toggle_default, marker_keys, record=None):
 7356      """kept-old | kept-new | DEFAULTS | RECORD | TORN for one config file after
 7357      a power cut: TORN when it does not parse; RECORD when it equals the
 7358      .backup that predates S0 (chksysconfig's binary-file path restored a
 7359      torn file from a record written at the last clean shutdown -- D-CLOUD-079
 7360      writes it after every validated save instead); DEFAULTS when the planted
 7361      marker keys are gone otherwise; else which side of the toggle it is on."""
 7362      if parsed is None:
 7363          return "TORN"
 7364      if any(parsed.get(k) != v for k, v in marker_keys.items()):
 7365          if record is not None and parsed == record:
 7366              return "RECORD"
 7367          return "DEFAULTS"          # /usr/config's copy is an empty <config/>, 41 bytes
 7368      old = s0.get(toggle_key)
 7369      new = parsed.get(toggle_key)
 7370      if new == old or (new is None and old in (None, toggle_default)):
 7371          return "kept-old"
 7372      return "kept-new"
 7373  
 7374  
 7375  def fx_kill13(L):
 7376      """KILL13: es_settings.cfg AND system.cfg power-cut through EmulationStation's
 7377      own writers. Closing any settings page runs GuiSettings::save(), which
 7378      calls Settings::saveFile() -- pugixml save_file, fopen("wb"), truncate,
 7379      write, no fsync, no rename -- and SystemConf::saveSystemConf(), which
 7380      writes system.cfg.tmp and then COPIES it into system.cfg with a
 7381      truncating stream (the tmp is never renamed into place).
 7382  
 7383      Arm A, the writer: each trial plants S0 in both files and boots (so ES
 7384      holds S0 and starts on the carousel), then a walk
 7385      (tools/vm-walks/ui-settings-toggle.steps) flips a Settings-backed switch
 7386      on USER INTERFACE SETTINGS, then on ONE monitor connection `sendkey z`
 7387      (the close: both saves) followed by `system_reset` after a gap from
 7388      --cut-after-ms; plus two controls, one with `sync` over serial between
 7389      close and reset (must read kept-new, or the walk is not reaching the
 7390      switch) and one with no change (kept-old). Per trial, per file: parses,
 7391      the planted markers survive (not /usr/config's defaults), kept-old or
 7392      kept-new -- TORN and DEFAULTS are failures; no system.cfg.tmp. The design
 7393      expected ext4's auto_da_alloc to carry today's in-place writers through
 7394      this arm; on 2026-09-10 it did not: at 0, 50 and 200 ms -- and after a
 7395      close that changed nothing -- system.cfg came up EMPTY, chksysconfig
 7396      reseeded /usr/config over /storage/.config (es_settings.cfg to its
 7397      41-byte default, ssh.enabled with it), and SSH was off after the boot.
 7398      auto_da_alloc starts writeback on close(); it does not wait for it. The
 7399      RG SP's SD card is what the VM still cannot model; the truncate window
 7400      it does.
 7401  
 7402      Arm B, the reader, planted: es_settings.cfg (i) empty and (ii) cut inside
 7403      a tag, synced, power cut. Today ES logs `Could not parse Settings file!`
 7404      and runs on defaults, and the next page close writes those defaults over
 7405      the file -- asserted by driving one page open/close and reading it back
 7406      (FAIL: D-CLOUD-078's "never defaults"). Proposed (D-CLOUD-079): the file
 7407      equals es_settings.cfg.backup after boot. system.cfg's planted shapes are
 7408      KILL12's (a) and (b1)."""
 7409      f = 0
 7410      L.assert_same_guest()
 7411      L.assert_same_qemu()
 7412      had = L.snapshot_configs()
 7413      steps = walk_steps(WALK_TOGGLE)
 7414      toggle_key, toggle_default = "ShowCheevosIcon", "true"
 7415      try:
 7416          es0 = L.dev.run(f"cat {ES_SETTINGS}", check=False)
 7417          es_map0 = parse_es(es0) or {}
 7418          marker_es = {"ScreenSaverTime": "1234567", "QaKill13Marker": "kept"}
 7419          plant = ''.join(f'  <{"int" if k == "ScreenSaverTime" else "string"} name="{k}" value="{v}" />\n' for k, v in marker_es.items())
 7420          es_s0 = (es0.replace("</config>", plant + "</config>") if "</config>" in es0
 7421                   else f'<?xml version="1.0"?>\n<config>\n{plant}</config>\n')
 7422          es_s0 = re.sub(r'\s*<int name="ScreenSaverTime" value="(?!1234567)[^"]*" />\n?', "\n", es_s0)
 7423          L.dev.write(ES_SETTINGS, es_s0.encode())
 7424          L.dev.run(L.bash_profile("set_setting system.qa.kill13 1"))
 7425          L.dev.run("sync")
 7426          s0_es = parse_es(L.dev.run(f"cat {ES_SETTINGS}"))
 7427          s0_sys = parse_syscfg(L.dev.run(f"cat {SYSCFG}"))
 7428          marker_sys = {"system.qa.kill13": "1", "system.hostname": s0_sys.get("system.hostname", "")}
 7429          sys_s0 = L.dev.run(f"cat {SYSCFG}", check=False)
 7430          rec_sys = parse_syscfg(L.dev.run(f"cat {SYSCFG}.backup 2>/dev/null || true", check=False))
 7431          gaps = [int(x) for x in str(L.args.cut_after_ms).split(",") if x.strip()][: max(0, L.args.power_cut_trials)]
 7432          trials = [("sync control", None)] + [("cut", g) for g in gaps] + [("no-change control", 0)]
 7433          print(f"    -- arm A: {len(trials)} trials: {[t[0] + (f' {t[1]}ms' if t[1] is not None else '') for t in trials]}; "
 7434                "each starts from S0 planted in both files and a boot, so EmulationStation holds S0 and starts on the carousel")
 7435          for kind, gap in trials:
 7436              # S0 again, and a boot: a trial that left defaults would otherwise
 7437              # hand the next one a file without the markers and an ES holding
 7438              # defaults in memory, and every later trial would read DEFAULTS.
 7439              L.dev.write(ES_SETTINGS, es_s0.encode())
 7440              L.dev.write(SYSCFG, sys_s0.encode())
 7441              L.dev.run("sync")
 7442              L.power_cut()
 7443              cur_es = parse_es(L.dev.run(f"cat {ES_SETTINGS} 2>/dev/null || true", check=False)) or s0_es
 7444              cur_sys = parse_syscfg(L.dev.run(f"cat {SYSCFG} 2>/dev/null || true", check=False)) or s0_sys
 7445              if classify(cur_es, s0_es, toggle_key, toggle_default, marker_es) == "DEFAULTS":
 7446                  f += not check(False, "", f"[{kind}] the setup boot itself came up without S0 in es_settings.cfg; the trial cannot be judged")
 7447                  continue
 7448              mon = Monitor(L.monitor_path)
 7449              try:
 7450                  run_walk(mon, steps_without_toggle(steps) if kind.startswith("no-change") else steps)
 7451                  L.dev.disconnect()
 7452                  m = L.mark()
 7453                  mon.sendkey("z")
 7454                  if kind == "sync control":
 7455                      time.sleep(1.5)
 7456                      L.serial.run("sync", timeout=8)
 7457                  elif gap:
 7458                      time.sleep(gap / 1000.0)
 7459                  mon.system_reset()
 7460              finally:
 7461                  mon.close()
 7462              up, took = L.reboot_wait(m)
 7463              es = L.dev.run(f"cat {ES_SETTINGS} 2>/dev/null || true", check=False)
 7464              sy = L.dev.run(f"cat {SYSCFG} 2>/dev/null || true", check=False)
 7465              parse_err = L.count_in(ES_LOG, ES_PARSE_ERROR)
 7466              tmp = L.dev.run(f"[ -e {SYSCFG}.tmp ] && echo yes || echo no", check=False).strip() == "yes"
 7467              c_es = classify(parse_es(es), cur_es, toggle_key, toggle_default, marker_es)
 7468              c_sy = classify(parse_syscfg(sy) if sy.strip() else None, cur_sys, "__none__", None, marker_sys, record=rec_sys or None)
 7469              tag = f"{kind}{f' {gap}ms' if gap is not None else ''}"
 7470              what = f"es_settings.cfg {c_es} ({len(es)} bytes), system.cfg {c_sy} ({len(sy)} bytes); boot {took:.0f}s"
 7471              why = ("" if c_sy != "RECORD" else " -- system.cfg came up torn and chksysconfig restored the .backup from the last clean "
 7472                     "shutdown, which predates S0: the saved settings are lost")
 7473              f += not check(c_es not in ("TORN", "DEFAULTS", "RECORD") and c_sy not in ("TORN", "DEFAULTS", "RECORD"),
 7474                             f"[{tag}] {what}", f"[{tag}] {what} -- a torn, defaulted or stale-record file after the cut (D-CLOUD-078){why}")
 7475              if kind == "sync control":
 7476                  f += not check(c_es == "kept-new", f"[{tag}] the toggle was recorded: the walk reaches the switch",
 7477                                 f"[{tag}] the synced close did not record the toggle ({c_es}): the walk is not reaching the switch, "
 7478                                 "so the cut trials measure nothing -- read the frames of tools/vm-walks/ui-settings-toggle.steps")
 7479              f += not check(not tmp, f"[{tag}] no system.cfg.tmp left", f"[{tag}] system.cfg.tmp left behind (SystemConf copies its tmp instead of renaming it)")
 7480              # Informational, not a check: Settings are loaded before the log
 7481              # file is opened, so the parse error of a torn file never reaches
 7482              # es_log.txt (0 on every torn boot, 2026-09-10) -- an assertion on
 7483              # it could not fail.
 7484              print(f"          [{tag}] es_log.txt mentions '{ES_PARSE_ERROR}' {parse_err} time(s)")
 7485          print("    -- arm B: torn es_settings.cfg planted, power cut, then one page open/close to make ES save")
 7486          for shape, body in (("empty", b""), ("cut inside a tag", es_s0.encode()[: int(len(es_s0) * 0.6)])):
 7487              L.dev.write(ES_SETTINGS, body)
 7488              L.dev.run("sync")
 7489              L.power_cut()
 7490              parse_err = L.count_in(ES_LOG, ES_PARSE_ERROR)
 7491              rec = L.dev.run(f"for r in {ES_SETTINGS}.backup {ES_SETTINGS}.last-good; do [ -e $r ] && cat $r && break; done; true", check=False)
 7492              mon = Monitor(L.monitor_path)
 7493              try:
 7494                  run_walk(mon, steps_without_toggle(steps))   # to the page's last row, no toggle
 7495                  mon.sendkey("z")                # close: the save
 7496                  time.sleep(2)
 7497                  mon.sendkey("z")                # close the menu
 7498              finally:
 7499                  mon.close()
 7500              time.sleep(1)
 7501              es = L.dev.run(f"cat {ES_SETTINGS} 2>/dev/null || true", check=False)
 7502              parsed = parse_es(es)
 7503              kept = parsed is not None and all(parsed.get(k) == v for k, v in marker_es.items())
 7504              print(f"          ({shape}) es_log.txt mentions the parse error {parse_err} time(s) (Settings load before the log opens); "
 7505                    f"a record {'exists' if rec else 'does not exist'}")
 7506              f += not check(kept, f"({shape}) after boot and one save es_settings.cfg carries the last known good settings",
 7507                             f"({shape}) after boot and one save es_settings.cfg is "
 7508                             f"{'DEFAULTS: ' + str(len(parsed)) + ' key(s), the planted ones gone' if parsed is not None else 'unparsable'} "
 7509                             "-- Settings.cpp:512-518 logs and continues on defaults, and the next save writes them over the torn file (D-CLOUD-079: restore from .backup)")
 7510      finally:
 7511          L.restore_configs(had)
 7512      return f
 7513  
 7514  
 7515  def fx_kill15(L):
 7516      """KILL15: `cloud_saves_root record` writes its one-line record in place
 7517      (`echo >`, a builtin: no external kill lands in it), so the torn state is
 7518      planted -- an empty saves-root. Asserted: `check` REFUSES an empty record
 7519      (with the accept instruction), because `-s` false reads today as "no
 7520      record" and the #83 guard is silently off (FAIL, fails open); the refusal
 7521      text carries no CLI name (assert_message)."""
 7522      f = 0
 7523      rec = L.dev.run(f"cat {CACHE}/saves-root 2>/dev/null || true", check=False)
 7524      if not rec.strip():
 7525          rc0, _ = run_rc(L.dev, "cloud_saves_root record")
 7526          rec = L.dev.run(f"cat {CACHE}/saves-root 2>/dev/null || true", check=False)
 7527          if not rec.strip():
 7528              raise Fail(f"cloud_saves_root record wrote no record (rc {rc0})")
 7529      L.cleanups.append(lambda: L.dev.write(f"{CACHE}/saves-root", rec.encode()))
 7530      L.dev.run(f"mkdir -p {CACHE}; : > {CACHE}/saves-root")
 7531      rc, out = run_rc(L.dev, "cloud_saves_root check")
 7532      f += not check(rc != 0, "an empty saves-root record is refused (exit 1) rather than read as none",
 7533                     f"cloud_saves_root check exited {rc} on an EMPTY record: the #83 guard fails open (cloud_saves_root:109 tests -s)")
 7534      f += assert_message(out, rc, L.args.vocabulary, label="check: ")
 7535      rc2, out2 = run_rc(L.dev, "cloud_saves_root record")
 7536      now = L.dev.run(f"cat {CACHE}/saves-root 2>/dev/null || true", check=False).strip()
 7537      f += not check(rc2 == 0 and now == rec.strip(), f"record rewrites the identity ({now})", f"record (rc {rc2}) left {now!r}, expected {rec.strip()!r}")
 7538      temps = L.dev.run(f"ls {CACHE}/saves-root.* {CACHE}/.saves-root* 2>/dev/null; true", check=False).split()
 7539      f += not check(not temps, "no saves-root temp left", f"temps left: {temps}")
 7540      return f
 7541  
 7542  
 7543  def fx_kill16(L):
 7544      """KILL16: `content-systems`, written by `cloud_content_restore
 7545      --set-systems` (the picker's backend, :845-853) in place. Shim arm: an
 7546      exported `mkdir` function kills the group before the write, so the
 7547      selection stands (PASS by construction). Plant arm: an empty file is a
 7548      LEGAL answer ("none"), indistinguishable from a torn one by design, so
 7549      the only fix is the writer: after `--set-systems a b` exactly two lines,
 7550      no `content-systems.*` temp."""
 7551      f = 0
 7552      sel0 = L.dev.run(f"cat {CACHE}/content-systems 2>/dev/null || true", check=False)
 7553      had = L.dev.run(f"[ -e {CACHE}/content-systems ] && echo yes || echo no", check=False).strip() == "yes"
 7554      L.cleanups.append(lambda: (L.dev.write(f"{CACHE}/content-systems", sel0.encode()) if had
 7555                                 else L.dev.run(f"rm -f {CACHE}/content-systems", check=False)))
 7556      rc0, _ = run_rc(L.dev, "cloud_content_restore --set-systems qa-a qa-b")
 7557      if rc0 != 0:
 7558          raise Fail(f"--set-systems qa-a qa-b exited {rc0}")
 7559      prelude = Kill.shim("mkdir", 'case "$*" in *cloud_sync*) kill -KILL -- -$QA_PGID ;; esac; command mkdir "$@"')
 7560      L.start("cloud_content_restore --set-systems qa-c qa-d", prelude=prelude, shell="bash")
 7561      for _ in range(50):
 7562          if not L.pid() or not L.group_pids(L.pid()):
 7563              break
 7564          time.sleep(0.1)
 7565      sel = L.dev.run("cloud_content_restore --systems 2>/dev/null || true", check=False).split()
 7566      f += not check(sel == ["qa-a", "qa-b"], "killed before the write (mkdir shim): the selection still reads qa-a qa-b",
 7567                     f"the selection reads {sel} after a kill before the write")
 7568      L.dev.run(f": > {CACHE}/content-systems")
 7569      none = L.dev.run("cloud_content_restore --systems 2>/dev/null || true", check=False).split()
 7570      print(f"          an empty file reads as {none or 'no systems'} -- legal by design (the picker's 'none'); a torn write is indistinguishable")
 7571      rc2, out2 = run_rc(L.dev, "cloud_content_restore --set-systems qa-a qa-b")
 7572      lines = [l for l in L.dev.run(f"cat {CACHE}/content-systems", check=False).splitlines() if l.strip()]
 7573      temps = L.dev.run(f"ls {CACHE}/content-systems.* {CACHE}/.content-systems* 2>/dev/null; true", check=False).split()
 7574      f += not check(rc2 == 0 and lines == ["qa-a", "qa-b"], "after --set-systems a b the file holds exactly those two lines",
 7575                     f"after --set-systems (rc {rc2}) the file holds {lines}")
 7576      f += not check(not temps, "no content-systems temp left", f"temps left: {temps}")
 7577      return f
 7578  
 7579  
 7580  def fx_kill18(L):
 7581      """KILL18: `backuptool restore` killed mid-`tar -xzf ... -C /`
 7582      (backuptool:220). The archive holds a.cfg, then 20k small files, then
 7583      b.cfg -- in that order -- so the watcher fires once a.cfg carries the
 7584      archive's value while b.cfg is still live. Asserted: the tree is either
 7585      wholly restored or as it was -- FAILS today (a.cfg from the archive, b.cfg
 7586      live, half applied); the pre-restore state is kept somewhere (a
 7587      PRE_RESTORE archive under archive/, D-CLOUD-078) -- FAILS today, kept
 7588      nowhere; the re-run completes (its group is killed the moment the restore
 7589      marker appears, before backuptool's `systemctl reboot`)."""
 7590      f = 0
 7591      L.make_scratch()
 7592      had = L.snapshot_configs([RESTORE_PENDING, BACKUPTOOL_CONF])
 7593      live = f"{L.root}/kill18-live"
 7594      broot = L.backups
 7595      try:
 7596          L.dev.run(f"rm -rf {L.q(live)} {L.q(broot)}; mkdir -p {L.q(live)} {L.q(broot)}; "
 7597                    f"echo LIVE > {L.q(live)}/a.cfg; echo LIVE > {L.q(live)}/b.cfg; rm -f {RESTORE_PENDING}")
 7598          # The copy backuptool takes aside covers LOCATIONS, so the tree the
 7599          # archive writes over has to be in them for the boot-time revert to
 7600          # have anything to put back -- on a device the two are the same set.
 7601          L.dev.write(BACKUPTOOL_CONF, f"LOCATIONS=(\n  {live}\n)\n".encode())
 7602          rel = live.lstrip("/")
 7603          stage = "/storage/cloud-qa-kill/stage18"
 7604          name = f"2098_01_01-000000-{L.label + '-' if L.label else ''}{L.osn}_SETTINGS.tar.gz"
 7605          L.dev.run(f"rm -rf {stage}; mkdir -p {stage}/{rel}; echo ARCHIVE > {stage}/{rel}/a.cfg; echo ARCHIVE > {stage}/{rel}/b.cfg; "
 7606                    f"cp -r {KILL_SCRATCH}/many {stage}/{rel}/many; "
 7607                    f"tar -czf {L.q(broot)}/{name} -C {stage} {rel}/a.cfg {rel}/many {rel}/b.cfg; rm -rf {stage}; sync")
 7608          newest = L.finder()
 7609          if os.path.basename(newest) != name:
 7610              raise Fail(f"newest_backup finds {newest!r}, not the planted {name}")
 7611          u_before = float(L.dev.run("cut -d' ' -f1 /proc/uptime").strip())
 7612          cond = f"[ \"$(cat {shlex.quote(live)}/a.cfg 2>/dev/null)\" = ARCHIVE ] || [ -e {RESTORE_PENDING} ]"
 7613          L.start("backuptool restore", shell="bash", watch=(cond, "KILL"))
 7614          r = L.watch_result()
 7615          a = L.dev.run(f"cat {L.q(live)}/a.cfg 2>/dev/null || true", check=False).strip()
 7616          b = L.dev.run(f"cat {L.q(live)}/b.cfg 2>/dev/null || true", check=False).strip()
 7617          many = L.dev.run(f"ls {L.q(live)}/many 2>/dev/null | wc -l", check=False).strip()
 7618          pending = L.dev.run(f"[ -e {RESTORE_PENDING} ] && echo yes || echo no", check=False).strip() == "yes"
 7619          f += not check(r[0] == "landed" and not pending, f"the kill landed mid-extract (a.cfg {a}, {many} of {KILL_MANY} small files, b.cfg {b})",
 7620                         f"the kill did not land mid-extract: watcher {r}, restore marker {'set' if pending else 'unset'}")
 7621          # tar writes over the live tree, so right after the kill the tree IS
 7622          # half restored (a.cfg from the archive, b.cfg live); nothing running
 7623          # can undo it. What must hold is that the copy taken aside exists and
 7624          # that the next boot puts it back: backuptool leaves
 7625          # .restore-in-progress naming the copy, and `chksysconfig verify`
 7626          # (sysinit, rocknix-sysconfig.service) reads it. Run here as the boot
 7627          # would (D-CLOUD-078; 2026-09-10).
 7628          snap = L.dev.run(f"ls {L.q(broot)}/archive/ 2>/dev/null | grep -i 'PRE_RESTORE\\|pre-restore'; true", check=False).split()
 7629          f += not check(bool(snap), f"the pre-restore state is kept ({snap}) while the tree is half restored (a.cfg {a}, b.cfg {b}, {many} of {KILL_MANY} files)",
 7630                         "the pre-restore state is kept NOWHERE: a killed restore has nothing to revert to (D-CLOUD-078)")
 7631          mark = L.dev.run("[ -e /storage/.config/.restore-in-progress ] && echo yes || echo no", check=False).strip()
 7632          f += not check(mark == "yes", "the restore-in-progress marker names the copy for the next boot",
 7633                         "no .restore-in-progress marker: the boot would not know a restore was cut off")
 7634          L.dev.run(". /etc/profile >/dev/null 2>&1; chksysconfig verify >/dev/null 2>&1; true", check=False)
 7635          a3 = L.dev.run(f"cat {L.q(live)}/a.cfg 2>/dev/null || true", check=False).strip()
 7636          b3 = L.dev.run(f"cat {L.q(live)}/b.cfg 2>/dev/null || true", check=False).strip()
 7637          said = L.dev.run("cat /storage/.config/.restore-reverted 2>/dev/null; rm -f /storage/.config/.restore-reverted", check=False).strip()
 7638          mark2 = L.dev.run("[ -e /storage/.config/.restore-in-progress ] && echo yes || echo no", check=False).strip()
 7639          f += not check((a3, b3) == ("LIVE", "LIVE") and said == "reverted" and mark2 == "no",
 7640                         f"the boot-time check put the copy back (a.cfg {a3}, b.cfg {b3}), left 'reverted' for EmulationStation to say, and cleared the marker",
 7641                         f"after chksysconfig verify: a.cfg {a3}, b.cfg {b3}; .restore-reverted {said!r}; marker {'still there' if mark2 == 'yes' else 'gone'}")
 7642          u_now = float(L.dev.run("cut -d' ' -f1 /proc/uptime").strip())
 7643          f += not check(u_now > u_before, "the guest did not reboot", "THE GUEST REBOOTED (backuptool restore's systemctl reboot ran)")
 7644          # The re-run, stopped the instant its marker appears -- after tar,
 7645          # before `sleep 5; systemctl reboot`.
 7646          L.start("backuptool restore", shell="bash", watch=(f"[ -e {RESTORE_PENDING} ]", "KILL"))
 7647          r2 = L.watch_result()
 7648          out2 = L.dev.run(f"cat {LINK_DIR}/out 2>/dev/null || true", check=False)
 7649          L.keep("KILL18", out2)
 7650          a2 = L.dev.run(f"cat {L.q(live)}/a.cfg 2>/dev/null || true", check=False).strip()
 7651          b2 = L.dev.run(f"cat {L.q(live)}/b.cfg 2>/dev/null || true", check=False).strip()
 7652          f += not check(r2[0] == "landed" and (a2, b2) == ("ARCHIVE", "ARCHIVE"),
 7653                         f"a re-run completes the restore (a.cfg {a2}, b.cfg {b2}; stopped before its reboot)",
 7654                         f"the re-run left a.cfg {a2}, b.cfg {b2} (watcher {r2})")
 7655          f += assert_message(out2, None, L.args.vocabulary, label="re-run: ")
 7656      finally:
 7657          L.dev.run(f"rm -f {RESTORE_PENDING}; rm -rf {L.q(live)}", check=False)
 7658          L.restore_configs_quiet(had)
 7659      return f
 7660  
 7661  
 7662  KILL_FIXTURES = [
 7663      ("KILL1", "saves backup killed mid-transfer, SIGKILL then SIGTERM: cloud holds v1 or whole v2, stamp never 0, lock released, re-run completes", fx_kill1, {"backend"}),
 7664      ("KILL2", "saves restore stopped mid-download by ES's TERM-then-KILL (D-CLOUD-076): the game's save stands, *.partial litter, re-run keeps the previous version", fx_kill2, {"backend"}),
 7665      ("KILL3", "backuptool backup killed mid-rotation: the previous archive is still what both readers find", fx_kill3, set()),
 7666      ("KILL4", "backuptool backup killed mid-tar: no truncated archive under a final name, nothing invalid uploaded", fx_kill4, set()),
 7667      ("KILL5", "settings upload killed mid-copyto: marker, retention and device.json untouched; the re-run trims only this device's", fx_kill5, {"backend"}),
 7668      ("KILL10", "set_setting killed mid-sed: the value stands, the temp is litter, the stale lock clears", fx_kill10, set()),
 7669      ("KILL11", "set_setting killed between delete and add: the previous value is not lost", fx_kill11, set()),
 7670      ("KILL12", "chksysconfig at boot with an empty, truncated, valid or binary system.cfg (power cut), and the clean-shutdown record", fx_kill12, {"serial", "monitor"}),
 7671      ("KILL13", "es_settings.cfg and system.cfg power-cut through ES's own writers (arm A), and planted torn files at boot (arm B)", fx_kill13, {"serial", "monitor"}),
 7672      ("KILL15", "an empty saves-root record refuses instead of reading as none", fx_kill15, set()),
 7673      ("KILL16", "content-systems: a kill before the write keeps the selection; an empty file is legal, so the writer must verify", fx_kill16, set()),
 7674      ("KILL18", "backuptool restore killed mid-extract: the tree is half restored and the pre-restore state kept nowhere", fx_kill18, set()),
 7675  ]
 7676  KILL_NEEDS_TEXT = {"backend": "QA endpoint", "minio": "MinIO", "serial": "serial", "monitor": "monitor"}
 7677  
 7678  
 7679  
 7680  
 7681  def run_kill(dev, root, remote, args, settings, serial, only, local_only):
 7682      """The KILL cells on one device (#105). Each cell resets the scratch tree
 7683      (and the endpoint, when there is one) first; the cache directory is
 7684      carried across and put back, from a snapshot on /storage because a power
 7685      cut empties /tmp. A cell whose channel is missing is skipped with a line
 7686      naming it; the set never is."""
 7687      step("the KILL cells: a writer killed at every step, the power cut, one record at rest (#105, D-CLOUD-078)")
 7688      if args.real_roms:
 7689          raise Fail("the KILL cells empty the saves root and the settings archives between cells; they never run against real ROMs")
 7690      serial_ok = serial is not None and serial.usable()
 7691      try:
 7692          monitor_ok = stat.S_ISSOCK(os.stat(args.monitor_socket).st_mode)
 7693      except OSError:
 7694          monitor_ok = False
 7695      throttled = (not local_only) and backend_throttled()
 7696      L = Kill(dev, serial if serial_ok else None, root, remote, settings, args, monitor_path=args.monitor_socket, endpoint=not local_only)
 7697      print(f"    device {L.device_id or 'no id'} ({L.label or 'no label'}); endpoint {'none (local cells only)' if local_only else L.hostport + (' throttled' if throttled else ' NOT throttled')}; "
 7698            f"serial {'yes' if serial_ok else 'no'}; monitor {'yes' if monitor_ok else 'no'}")
 7699      failures = 0
 7700      had = snapshot_cache(dev, where="/storage/.cache/qa-kill-cache.tgz")
 7701      try:
 7702          for key, title, fn, needs in KILL_FIXTURES:
 7703              if only and key not in only:
 7704                  continue
 7705              missing = []
 7706              if "backend" in needs and local_only:
 7707                  missing.append("the QA endpoint (this run prepared the device locally)")
 7708              elif "backend" in needs and not throttled:
 7709                  missing.append("a throttled endpoint: `tools/cloud-test-backend down && CLOUD_QA_BWLIMIT=200k tools/cloud-test-backend up`")
 7710              if "serial" in needs and not serial_ok:
 7711                  missing.append(f"a serial console at {args.serial_socket}")
 7712              if "monitor" in needs and not monitor_ok:
 7713                  missing.append(f"a monitor socket at {args.monitor_socket} (--monitor-socket)")
 7714              step(f"{key} -- {title}")
 7715              if missing:
 7716                  print(f"    SKIP  {key} needs {'; '.join(missing)}")
 7717                  continue
 7718              L.reset()
 7719              L.cleanups = []
 7720              t0 = time.time()
 7721              try:
 7722                  failures += fn(L)
 7723              except Fail as e:
 7724                  failures += 1
 7725                  print(f"    FAIL  {e}")
 7726                  try:
 7727                      pgid = L.pid()
 7728                      if pgid and L.group_pids(pgid):
 7729                          L.dev.run(f"kill -KILL -- -{pgid} 2>/dev/null; true", check=False)
 7730                  except Fail:
 7731                      pass
 7732              failures += litter_scan(dev, settings, "" if local_only else remote, label=f"{key}: ")
 7733              for c in L.cleanups:
 7734                  try:
 7735                      c()
 7736                  except Fail as e:
 7737                      print(f"    WARN  {key}: cleanup incomplete: {e}", file=sys.stderr)
 7738              print(f"    ({key} took {time.time() - t0:.0f}s)")
 7739      finally:
 7740          L.reset()
 7741          L.remove_scratch()
 7742          dev.run(f"rm -rf {os.path.dirname(KILL_WATCH)}", check=False)
 7743          restore_cache(dev, had, where="/storage/.cache/qa-kill-cache.tgz")
 7744      return failures
 7745  
 7746  
 7747  def restore_device(p, args, archive):
 7748      """Put the device back: its remote, its paths, the settings-restore
 7749      option, the scratch tree, the fixture system -- on every exit. Its
 7750      identity is not the harness's to touch: prepare never writes it (#91),
 7751      and A11, which clones one on purpose, puts it back itself."""
 7752      if args.keep:
 7753          return
 7754      dev, prev_paths, prev_rclone_conf = p.dev, p.prev_paths, p.prev_rclone_conf
 7755      step(f"clean up {dev.host} port {dev.port}")
 7756      try:
 7757          dev.run(f"rm -f {shlex.quote(archive)}", check=False)
 7758          # The settings-restore option is put back only when the suite saved
 7759          # it: run_steps writes {CONF}.qa-prev, a --only run never does, and
 7760          # "no saved value" is not "delete the device's line".
 7761          if dev.run(f"[ -e {CONF}.qa-prev ] && echo yes || echo no", check=False).strip() == "yes":
 7762              prev = dev.run(f"grep -m1 '^BACKUPFILE_RESTORE_OPTION=' {CONF}.qa-prev 2>/dev/null || true", check=False).strip()
 7763              if prev:
 7764                  dev.run(f"sed -i 's|^BACKUPFILE_RESTORE_OPTION=.*|{prev}|' {CONF}", check=False)
 7765              else:
 7766                  dev.run(f"sed -i '/^BACKUPFILE_RESTORE_OPTION=/d' {CONF}", check=False)
 7767              dev.run(f"rm -f {CONF}.qa-prev", check=False)
 7768          for key, line in prev_paths.items():
 7769              if line:
 7770                  dev.run(f"sed -i 's|^{key}=.*|{line}|' {CONF}", check=False)
 7771              else:
 7772                  dev.run(f"sed -i '/^{key}=/d' {CONF}", check=False)
 7773          if not args.real_roms:
 7774              # .away is where A9 and CAP8 park the root to test an unmounted
 7775              # one; a Fail or a dropped ssh between the mv and its undo leaves
 7776              # it behind, and nothing else knows the name.
 7777              dev.run(f"rm -rf {shlex.quote(SCRATCH)} {shlex.quote(SCRATCH)}.away", check=False)
 7778          if p.local_only:
 7779              # A local prepare read no rclone.conf and created no content
 7780              # fixture: putting back a blank remote would delete the device's
 7781              # real one, and resetting the bucket would need a backend that
 7782              # was never asked for.
 7783              print("    scratch tree removed and the saves root put back; no remote or bucket was touched")
 7784              return
 7785          if not args.real_roms:
 7786              dev.run(f"rm -rf /storage/roms/{shlex.quote(CONTENT_DIR)} /storage/roms/{shlex.quote(CONTENT_DIR)}-unselected", check=False)
 7787          if prev_rclone_conf.strip():
 7788              dev.write(RCLONE_CONF, prev_rclone_conf.encode())
 7789          else:
 7790              dev.run(f"rm -f {RCLONE_CONF}", check=False)
 7791          if p.prev_active is None:
 7792              dev.run(f"rm -f {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection", check=False)
 7793          else:
 7794              dev.write(RCLONE_CONF.rsplit("/", 1)[0] + "/active-connection", p.prev_active.encode())
 7795          backend("reset")
 7796          print("    scratch tree and bucket emptied; the device's own remote, paths and "
 7797                "settings-backup setting restored")
 7798      except Fail as e:
 7799          print(f"    WARN  clean-up incomplete: {e}", file=sys.stderr)
 7800  
 7801  if __name__ == "__main__":
 7802      try:
 7803          sys.exit(main())
 7804      except Fail as e:
 7805          print(f"\nerror: {e}", file=sys.stderr)
 7806          sys.exit(2)
 7807      except KeyboardInterrupt:
 7808          sys.exit(130)
```

## File: tools/cloud-test-backend (at 8ebaf8daad, 920 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # A disposable cloud endpoint for cloud-sync QA, in five protocols.
    6  #
    7  # Serves a directory on this host over WebDAV, S3, SFTP, SMB or FTP. A VM
    8  # started by generic-x64-vm reaches every one of them at 10.0.2.2 (QEMU
    9  # user-mode networking always routes that to the host), so nothing needs
   10  # forwarding and no real cloud account is involved.
   11  #
   12  #   ./tools/cloud-test-backend --backend sftp up
   13  #   CLOUD_QA_BACKEND=sftp ./tools/cloud-test-backend up     # the same thing
   14  #
   15  # WebDAV is the default, because it matches what people actually use.
   16  # Dropbox, Google Drive and OneDrive are path-based, so SAVES_REMOTE="/GAMES"
   17  # is a folder. On S3 and SMB the first path component is the *bucket* or the
   18  # *share*, so the same setting asks for a bucket named GAMES and fails with
   19  # InvalidBucketName. Every backend states its own three remotes and the
   20  # prefix a caller must strip to address the endpoint directly
   21  # (`saves-remote`, `endpoint-prefix`), so no caller has to know which shape
   22  # it is talking to.
   23  #
   24  # What each one is, and what it cannot do (`caps` prints this per backend):
   25  #
   26  #   webdav  :9010  rclone serve webdav        no hashes, NO MODTIMES
   27  #   s3      :9012  MinIO in a container       MD5 hashes, modtimes, atomic PUT
   28  #   sftp    :9013  an unprivileged sshd       no hashes (no shell), modtimes
   29  #   smb     :9014  Samba in a container       no hashes, modtimes
   30  #   ftp     :9015  pyftpdlib in a venv        no hashes, modtimes
   31  #
   32  # WebDAV with vendor=other is the harshest of the five: with neither hashes
   33  # nor modtimes rclone compares by size alone, which is the shape of #53. The
   34  # other four all carry modtimes, so a change that only WebDAV catches is a
   35  # change WebDAV must keep catching.
   36  #
   37  # Deliberately local, all five: these tests exercise credential stripping and
   38  # backup contents, so a live provider token would be handled by exactly the
   39  # code paths most likely to leak it. Every listener binds 127.0.0.1 (set
   40  # CLOUD_QA_BIND=0.0.0.0 deliberately for a LAN device), and every port is in
   41  # the 9010-9099 range this fork reserves for QA services.
   42  #
   43  #   ./tools/cloud-test-backend up          # start it (CLOUD_QA_BWLIMIT=1M to throttle WebDAV or S3)
   44  #   ./tools/cloud-test-backend reset       # empty it between tests
   45  #   ./tools/cloud-test-backend ls [path]   # what the device actually uploaded
   46  #   ./tools/cloud-test-backend cat <path>  # one uploaded file's bytes
   47  #   ./tools/cloud-test-backend rclone-conf # the stanza to place on a device
   48  #   ./tools/cloud-test-backend caps        # hashes / modtimes / commit shape
   49  #   ./tools/cloud-test-backend seed-content [root]   # a content-tier fixture at the endpoint
   50  #   ./tools/cloud-test-backend seed-device [root]    # the matching guest-side script, on stdout
   51  #   ./tools/cloud-test-backend down        # stop it
   52  set -euo pipefail
   53  
   54  # --backend <name> is first-class; CLOUD_QA_BACKEND still works and means the
   55  # same thing, so every existing caller and every doc line keeps working.
   56  BACKEND="${CLOUD_QA_BACKEND:-webdav}"
   57  while [ $# -gt 0 ]; do
   58    case "${1}" in
   59      --backend) BACKEND="${2:-}"; shift 2 ;;
   60      --backend=*) BACKEND="${1#--backend=}"; shift ;;
   61      *) break ;;
   62    esac
   63  done
   64  case "${BACKEND}" in
   65    webdav|s3|sftp|smb|ftp) ;;
   66    *) echo "error: unknown backend '${BACKEND}' (webdav, s3, sftp, smb, ftp)" >&2; exit 2 ;;
   67  esac
   68  # Nested helper calls (seed-device, status and endpoint notes) must keep the
   69  # explicit CLI selection, even when the incoming environment named another.
   70  export CLOUD_QA_BACKEND="${BACKEND}"
   71  
   72  # One port each, so more than one backend can be up at a time: a matrix run
   73  # that had to take the previous endpoint down between rows would test the
   74  # teardown as much as the code. 9010 is WebDAV's and does not move; 9011 is
   75  # the deliberately dead port the failure fixtures aim at, and is never bound.
   76  default_port() {
   77    case "${1}" in
   78      webdav) echo 9010 ;; s3) echo 9012 ;; sftp) echo 9013 ;;
   79      smb)    echo 9014 ;; ftp) echo 9015 ;;
   80    esac
   81  }
   82  PORT="${CLOUD_QA_PORT:-$(default_port "${BACKEND}")}"
   83  # The deliberately dead port: nothing ever binds it, on any backend. A
   84  # failure fixture needs a stanza that is right in every other respect and
   85  # cannot connect, and rewriting a live stanza with sed only works on the two
   86  # backends whose address is a URL -- on SFTP, SMB and FTP the sed matched
   87  # nothing and the "refused cloud" test quietly ran against a working one.
   88  DEAD_PORT="${CLOUD_QA_DEAD_PORT:-9011}"
   89  BIND="${CLOUD_QA_BIND:-127.0.0.1}"
   90  USER_NAME="${CLOUD_QA_USER:-qauser}"
   91  PASS="${CLOUD_QA_PASS:-qa-password}"   # >=8 chars: MinIO rejects shorter root passwords
   92  
   93  STATE="${CLOUD_QA_STATE:-${XDG_CACHE_HOME:-${HOME}/.cache}/rocknix-cloud-qa}"
   94  # WebDAV's data directory does not move -- it is the one every existing
   95  # caller, log line and instruction file names. The four added backends get a
   96  # subdirectory each, so all five can hold fixtures at once.
   97  if [ "${BACKEND}" = "webdav" ]; then
   98    DATA="${STATE}/data"
   99    PIDFILE="${STATE}/webdav.pid"
  100    LOGFILE="${STATE}/webdav.log"
  101  else
  102    DATA="${STATE}/${BACKEND}/data"
  103    PIDFILE="${STATE}/${BACKEND}/${BACKEND}.pid"
  104    LOGFILE="${STATE}/${BACKEND}/${BACKEND}.log"
  105  fi
  106  CONFDIR="$(dirname "${PIDFILE}")"
  107  
  108  # The QA connection name. The driver explicitly selects it, verifies the
  109  # active reader and restores prior selection with credentials after testing.
  110  # Historical images use their first-remote rule, asserted at the same boundary.
  111  REMOTE="${CLOUD_QA_REMOTE:-qa-cloud}"
  112  
  113  GUEST_HOST="${CLOUD_QA_GUEST_HOST:-10.0.2.2}"
  114  
  115  # --- S3 ---------------------------------------------------------------------
  116  S3_NAME="${CLOUD_QA_NAME:-rocknix-cloud-qa}"
  117  S3_BUCKET="${CLOUD_QA_BUCKET:-rocknix-qa}"
  118  S3_IMAGE="${CLOUD_QA_IMAGE:-quay.io/minio/minio:latest}"
  119  S3_CONF="${STATE}/s3-host.conf"
  120  # Throttled S3 (CLOUD_QA_BWLIMIT): MinIO has no bandwidth knob of its own, so
  121  # it listens on this loopback port and a token-bucket proxy (write_throttle)
  122  # takes PORT in front of it. The guest meets the proxy; this host's own rclone
  123  # (reset, ls, cat, put) meets MinIO directly, the way the WebDAV commands read
  124  # the data directory rather than the throttled server. Where MinIO actually
  125  # listens is recorded beside the proxy's pid, so a later invocation reads the
  126  # mode off the state and not off an environment variable it may not share
  127  # with the one that started it.
  128  S3_UPSTREAM_PORT="${CLOUD_QA_S3_UPSTREAM_PORT:-9022}"
  129  S3_API_PORT_FILE="${CONFDIR}/api-port"
  130  
  131  # --- SMB --------------------------------------------------------------------
  132  SMB_NAME="${CLOUD_QA_SMB_NAME:-rocknix-cloud-qa-smb}"
  133  SMB_SHARE="${CLOUD_QA_SMB_SHARE:-qashare}"
  134  SMB_IMAGE="${CLOUD_QA_SMB_IMAGE:-dperson/samba:latest}"
  135  
  136  # --- SFTP -------------------------------------------------------------------
  137  SFTP_KEY="${CONFDIR}/qa-sftp-key"
  138  SFTP_HOSTKEY="${CONFDIR}/hostkey"
  139  SFTP_USER="${CLOUD_QA_SFTP_USER:-$(id -un)}"
  140  
  141  # --- FTP --------------------------------------------------------------------
  142  # Passive data connections need their own ports, and they are inside the
  143  # fork's 9010-9099 QA range so nothing here ever strays onto a real service.
  144  FTP_PASV_LOW="${CLOUD_QA_FTP_PASV_LOW:-9060}"
  145  FTP_PASV_HIGH="${CLOUD_QA_FTP_PASV_HIGH:-9069}"
  146  # What the server tells a client to dial for the data connection. The guest
  147  # knows this host as 10.0.2.2 and cannot reach 127.0.0.1, so PASV must name
  148  # the guest-facing address; set CLOUD_QA_FTP_MASQ=127.0.0.1 to drive it from
  149  # the host instead.
  150  FTP_MASQ="${CLOUD_QA_FTP_MASQ:-${GUEST_HOST}}"
  151  VENV="${STATE}/venv"
  152  
  153  need() { command -v "${1}" >/dev/null 2>&1 || { echo "error: ${1} is required" >&2; exit 1; }; }
  154  
  155  s3_api_port() { cat "${S3_API_PORT_FILE}" 2>/dev/null || echo "${PORT}"; }
  156  
  157  s3_host_conf() {
  158    mkdir -p "${STATE}"
  159    # A config file rather than an on-the-fly connection string: rclone's
  160    # connection-string parser splits on ':' and mangles an endpoint URL,
  161    # failing with "dial tcp: lookup http" on versions many distros ship.
  162    cat > "${S3_CONF}" <<EOF
  163  [qa-host]
  164  type = s3
  165  provider = Minio
  166  env_auth = false
  167  access_key_id = ${USER_NAME}
  168  secret_access_key = ${PASS}
  169  endpoint = http://127.0.0.1:$(s3_api_port)
  170  force_path_style = true
  171  region = us-east-1
  172  EOF
  173    chmod 600 "${S3_CONF}"
  174  }
  175  s3() { s3_host_conf; rclone --config "${S3_CONF}" "$@"; }
  176  
  177  pid_running() {
  178    [ -f "${PIDFILE}" ] && kill -0 "$(cat "${PIDFILE}")" 2>/dev/null
  179  }
  180  
  181  container_of() {
  182    case "${BACKEND}" in s3) echo "${S3_NAME}" ;; smb) echo "${SMB_NAME}" ;; *) echo "" ;; esac
  183  }
  184  
  185  # Which backends keep their data in a directory this host can read directly,
  186  # and which need a client to reach it. Reading the bytes off disk is reading
  187  # the artifact -- for S3 the artifact is inside MinIO, and reading the WebDAV
  188  # directory instead read back empty (the seeding step, 2026-09-07).
  189  fs_backed() { [ "${BACKEND}" != "s3" ]; }
  190  
  191  # A listing cached by the server outlives a fixture written behind its back.
  192  # rclone serve webdav is the only one of the five that caches (1 s, set at
  193  # start); the rest read the directory on every request. One place to ask.
  194  settle_cache() { [ "${BACKEND}" = "webdav" ] && sleep 1.5 || true; }
  195  
  196  wait_port() {   # wait_port <seconds> -- the listener is up
  197    local n="${1}"
  198    for _ in $(seq 1 "${n}"); do
  199      ss -ltn 2>/dev/null | grep -q ":${PORT} " && return 0
  200      sleep 1
  201    done
  202    return 1
  203  }
  204  
  205  venv_python() {
  206    # A virtualenv beside the QA data rather than a system package: this host
  207    # installs nothing, and a wiped /tmp or a fresh clone rebuilds it here.
  208    if [ ! -x "${VENV}/bin/python" ]; then
  209      need python3
  210      echo "ftp: creating ${VENV} (pyftpdlib)" >&2
  211      python3 -m venv "${VENV}" >&2
  212      "${VENV}/bin/pip" install -q pyftpdlib >&2
  213    fi
  214    "${VENV}/bin/python" -c 'import pyftpdlib' 2>/dev/null || "${VENV}/bin/pip" install -q pyftpdlib >&2
  215    echo "${VENV}/bin/python"
  216  }
  217  
  218  write_ftp_server() {
  219    cat > "${CONFDIR}/ftpd.py" <<'PY'
  220  import sys
  221  from pyftpdlib.authorizers import DummyAuthorizer
  222  from pyftpdlib.handlers import FTPHandler
  223  from pyftpdlib.servers import FTPServer
  224  
  225  root, bind, port, user, pw, masq, lo, hi = sys.argv[1:9]
  226  auth = DummyAuthorizer()
  227  # The user's home is the data directory, so every path the client names is
  228  # relative to it -- an FTP server is chrooted by construction, which is why
  229  # this backend needs no path prefix where SMB and S3 do.
  230  auth.add_user(user, pw, root, perm="elradfmwMT")
  231  handler = FTPHandler
  232  handler.authorizer = auth
  233  handler.masquerade_address = masq
  234  handler.passive_ports = range(int(lo), int(hi) + 1)
  235  handler.banner = "rocknix cloud QA"
  236  handler.use_sendfile = False
  237  FTPServer.max_cons = 64
  238  FTPServer((bind, int(port)), handler).serve_forever()
  239  PY
  240  }
  241  
  242  write_throttle() {
  243    cat > "${CONFDIR}/throttle.py" <<'PY'
  244  """A TCP proxy that paces bytes through a token bucket: what `rclone serve
  245  --bwlimit` does for the WebDAV endpoint, done for MinIO, which has no such
  246  knob. One bucket per direction, both at the rate given, 4 MiB burst --
  247  rclone's own bucket shape (accounting/token_bucket.go), which the link-loss
  248  cells' file sizes and bounds were measured against."""
  249  import argparse
  250  import asyncio
  251  import re
  252  import sys
  253  import time
  254  
  255  BURST = 4 * 1024 * 1024          # rclone's maxBurstSize
  256  CHUNK = 64 * 1024
  257  UNITS = {"": 1024, "b": 1, "k": 1024, "m": 1024 ** 2, "g": 1024 ** 3}
  258  
  259  
  260  def parse_rate(text):
  261      # rclone's SizeSuffix as --bwlimit reads it: a bare number is KiB/s; B, K,
  262      # M, G scale it (a trailing i or B is tolerated: 200Ki, 1MiB). Anything
  263      # else -- an up:down pair, a timetable -- is refused, not half-honoured.
  264      m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([bBkKmMgG]?)(?:i?[bB]?)?\s*", text)
  265      if not m or float(m.group(1)) <= 0:
  266          sys.exit(f"throttle: cannot read --bwlimit {text!r}; one positive rate such as 200k or 1M")
  267      return float(m.group(1)) * UNITS[m.group(2).lower()]
  268  
  269  
  270  class Bucket:
  271      def __init__(self, rate):
  272          self.rate, self.tokens, self.at = rate, float(BURST), time.monotonic()
  273  
  274      async def take(self, n):
  275          while True:
  276              now = time.monotonic()
  277              self.tokens = min(float(BURST), self.tokens + (now - self.at) * self.rate)
  278              self.at = now
  279              if self.tokens >= n:
  280                  self.tokens -= n
  281                  return
  282              await asyncio.sleep((n - self.tokens) / self.rate)
  283  
  284  
  285  async def pump(reader, writer, bucket, count):
  286      # One direction. The bucket is taken before the bytes move on and nothing
  287      # more is read until they have, so a slow bucket backs up into the
  288      # sender's TCP window the way rclone serve's does -- which is what lets
  289      # QEMU's user-mode stack hold a guest's whole upload after the guest is
  290      # gone, the artifact the link-loss cells are built around.
  291      try:
  292          while True:
  293              data = await reader.read(CHUNK)
  294              if not data:
  295                  break
  296              await bucket.take(len(data))
  297              writer.write(data)
  298              await writer.drain()
  299              count[0] += len(data)
  300      except OSError:
  301          pass
  302      finally:
  303          try:
  304              if writer.can_write_eof():
  305                  writer.write_eof()
  306          except (OSError, RuntimeError):
  307              pass
  308  
  309  
  310  async def serve(listen, upstream, rate):
  311      host, port = listen.rsplit(":", 1)
  312      up_host, up_port = upstream.rsplit(":", 1)
  313      buckets = (Bucket(rate), Bucket(rate))       # to upstream, back
  314      seq = [0]
  315  
  316      def log(msg):
  317          print(f"{time.strftime('%H:%M:%S')} throttle: {msg}", flush=True)
  318  
  319      async def handle(cr, cw):
  320          seq[0] += 1
  321          k = seq[0]
  322          peer = cw.get_extra_info("peername") or ("?", "?")
  323          t0 = time.monotonic()
  324          try:
  325              sr, sw = await asyncio.open_connection(up_host, int(up_port))
  326          except OSError as e:
  327              log(f"#{k}: upstream {upstream} refused ({e}); closing {peer[0]}:{peer[1]}")
  328              cw.close()
  329              return
  330          log(f"#{k}: open from {peer[0]}:{peer[1]}")
  331          sent, got = [0], [0]
  332          await asyncio.gather(pump(cr, sw, buckets[0], sent), pump(sr, cw, buckets[1], got))
  333          for w in (cw, sw):
  334              w.close()
  335          for w in (cw, sw):
  336              try:
  337                  await w.wait_closed()
  338              except OSError:
  339                  pass
  340          log(f"#{k}: closed after {time.monotonic() - t0:.1f}s; {sent[0]} B to upstream, {got[0]} B back")
  341  
  342      server = await asyncio.start_server(handle, host, int(port))
  343      log(f"{listen} -> {upstream} at {rate:.0f} B/s each way, burst {BURST >> 20} MiB")
  344      async with server:
  345          await server.serve_forever()
  346  
  347  
  348  ap = argparse.ArgumentParser(description=__doc__)
  349  ap.add_argument("--listen", required=True, help="host:port the guest dials")
  350  ap.add_argument("--upstream", required=True, help="host:port MinIO listens on")
  351  ap.add_argument("--bwlimit", required=True, help="rclone syntax: 200k, 1M")
  352  a = ap.parse_args()
  353  try:
  354      asyncio.run(serve(a.listen, a.upstream, parse_rate(a.bwlimit)))
  355  except KeyboardInterrupt:
  356      pass
  357  PY
  358  }
  359  
  360  throttle_rate() {
  361    # The rate the running proxy was started with, off its own argv -- the
  362    # place cloud-round-trip's backend_throttled() reads the flag from too.
  363    tr '\0' '\n' < "/proc/$(cat "${PIDFILE}")/cmdline" 2>/dev/null | grep -A1 -x -- --bwlimit | tail -1
  364  }
  365  
  366  throttle_down() {
  367    # The s3 throttle proxy and its record of where MinIO listens; harmless
  368    # when there is none.
  369    if [ -f "${PIDFILE}" ]; then kill "$(cat "${PIDFILE}")" 2>/dev/null || true; fi
  370    rm -f "${PIDFILE}" "${S3_API_PORT_FILE}"
  371  }
  372  
  373  write_sshd_config() {
  374    # An sshd of our own, run as this user on a high port: no root, no PAM, no
  375    # system configuration touched, and it goes away with `down`. Key auth only
  376    # -- a password would need PAM and therefore root.
  377    [ -f "${SFTP_HOSTKEY}" ] || ssh-keygen -q -t ed25519 -N '' -f "${SFTP_HOSTKEY}" -C rocknix-qa-host
  378    [ -f "${SFTP_KEY}" ]     || ssh-keygen -q -t ed25519 -N '' -f "${SFTP_KEY}" -C rocknix-qa
  379    cp "${SFTP_KEY}.pub" "${CONFDIR}/authorized_keys"
  380    chmod 600 "${CONFDIR}/authorized_keys" "${SFTP_HOSTKEY}" "${SFTP_KEY}"
  381    cat > "${CONFDIR}/sshd_config" <<EOF
  382  Port ${PORT}
  383  ListenAddress ${BIND}
  384  HostKey ${SFTP_HOSTKEY}
  385  PidFile ${PIDFILE}
  386  AuthorizedKeysFile ${CONFDIR}/authorized_keys
  387  AllowUsers ${SFTP_USER}
  388  PasswordAuthentication no
  389  KbdInteractiveAuthentication no
  390  UsePAM no
  391  PermitRootLogin no
  392  StrictModes no
  393  PrintMotd no
  394  X11Forwarding no
  395  AllowTcpForwarding no
  396  Subsystem sftp internal-sftp -d ${DATA}
  397  ForceCommand internal-sftp -d ${DATA}
  398  EOF
  399  }
  400  
  401  case "${1:-}" in
  402    up)
  403      mkdir -p "${DATA}" "${CONFDIR}"
  404      case "${BACKEND}" in
  405        s3)
  406          need docker; need rclone
  407          # A container that is not running is replaced, never restarted. A
  408          # stopped one carries the port mapping it was created with, so after
  409          # the backends were given a port each the old `docker start` failed
  410          # on the address already in use and the fallback `docker run` then
  411          # failed on the name -- two errors, neither of them the cause. There
  412          # is no volume and `reset` empties the bucket anyway, so recreating
  413          # costs nothing.
  414          if docker ps --format '{{.Names}}' | grep -qx "${S3_NAME}"; then
  415            # Up already, and it stays in the mode it is up in: a throttle
  416            # asked for over an unthrottled MinIO -- or the reverse -- is
  417            # refused, rather than answered with the other one.
  418            if [ -n "${CLOUD_QA_BWLIMIT:-}" ] && ! pid_running; then
  419              echo "error: s3 is up unthrottled; 'down' first, then CLOUD_QA_BWLIMIT=${CLOUD_QA_BWLIMIT} up" >&2; exit 1
  420            fi
  421            if [ -z "${CLOUD_QA_BWLIMIT:-}" ] && pid_running; then
  422              echo "error: s3 is up throttled (proxy pid $(cat "${PIDFILE}")); 'down' first for an unthrottled one" >&2; exit 1
  423            fi
  424            if pid_running && [ "$(throttle_rate)" != "${CLOUD_QA_BWLIMIT}" ]; then
  425              echo "error: s3 is up throttled to $(throttle_rate), not ${CLOUD_QA_BWLIMIT}; 'down' first" >&2; exit 1
  426            fi
  427          else
  428            docker rm -f "${S3_NAME}" >/dev/null 2>&1 || true
  429            throttle_down
  430            if [ -n "${CLOUD_QA_BWLIMIT:-}" ]; then
  431              need python3
  432              docker run -d --name "${S3_NAME}" -p "127.0.0.1:${S3_UPSTREAM_PORT}:9000" \
  433                -e "MINIO_ROOT_USER=${USER_NAME}" -e "MINIO_ROOT_PASSWORD=${PASS}" \
  434                "${S3_IMAGE}" server /data >/dev/null
  435              echo "${S3_UPSTREAM_PORT}" > "${S3_API_PORT_FILE}"
  436              write_throttle
  437              nohup python3 "${CONFDIR}/throttle.py" --listen "${BIND}:${PORT}" \
  438                    --upstream "127.0.0.1:${S3_UPSTREAM_PORT}" --bwlimit "${CLOUD_QA_BWLIMIT}" > "${LOGFILE}" 2>&1 &
  439              echo $! > "${PIDFILE}"
  440              # Alive AND bound, or it has not come up: a proxy that died on
  441              # its arguments leaves the guest a refused port and every cell
  442              # failing for a reason that names nothing.
  443              wait_port 10 && pid_running || {
  444                echo "error: the s3 throttle did not come up on ${PORT}; see ${LOGFILE}" >&2
  445                throttle_down; docker rm -f "${S3_NAME}" >/dev/null 2>&1 || true; exit 1; }
  446            else
  447              docker run -d --name "${S3_NAME}" -p "${BIND}:${PORT}:9000" \
  448                -e "MINIO_ROOT_USER=${USER_NAME}" -e "MINIO_ROOT_PASSWORD=${PASS}" \
  449                "${S3_IMAGE}" server /data >/dev/null
  450            fi
  451          fi
  452          for _ in $(seq 1 60); do
  453            s3 mkdir "qa-host:${S3_BUCKET}" >/dev/null 2>&1 && break
  454            # A container that has already exited will never become ready, so say
  455            # why now instead of waiting out the timeout on a corpse.
  456            if ! docker ps --format '{{.Names}}' | grep -qx "${S3_NAME}"; then
  457              echo "error: ${S3_NAME} exited during startup:" >&2
  458              docker logs --tail 5 "${S3_NAME}" >&2 2>/dev/null || true
  459              exit 1
  460            fi
  461            sleep 1
  462          done
  463          s3 lsd "qa-host:${S3_BUCKET}" >/dev/null 2>&1 || {
  464            echo "error: bucket not reachable; try: docker logs ${S3_NAME}" >&2; exit 1; }
  465          echo "up: s3 bucket ${S3_BUCKET} on port ${PORT}${CLOUD_QA_BWLIMIT:+ (throttled to ${CLOUD_QA_BWLIMIT} by a proxy; MinIO itself on 127.0.0.1:${S3_UPSTREAM_PORT})}"
  466          echo "note: SAVES_REMOTE must start with the bucket, e.g. $("$0" saves-remote)"
  467          exit 0
  468          ;;
  469  
  470        smb)
  471          need docker
  472          if docker ps --format '{{.Names}}' | grep -qx "${SMB_NAME}"; then
  473            echo "up: smb share ${SMB_SHARE} already serving ${DATA} on port ${PORT}"; exit 0
  474          fi
  475          docker rm -f "${SMB_NAME}" >/dev/null 2>&1 || true
  476          # Samba writes into the share as root inside the container, which on
  477          # the host is root:<our group> and group-writable -- so the data
  478          # directory is still ours to read, seed and empty from outside. The
  479          # share name is the first component of every remote path here, the
  480          # way a bucket is on S3.
  481          docker run -d --name "${SMB_NAME}" -p "${BIND}:${PORT}:445" \
  482            -v "${DATA}:/share" \
  483            -e "USERID=$(id -u)" -e "GROUPID=$(id -g)" \
  484            "${SMB_IMAGE}" -u "${USER_NAME};${PASS}" \
  485            -s "${SMB_SHARE};/share;yes;no;no;${USER_NAME};${USER_NAME};${USER_NAME}" -p >/dev/null
  486          wait_port 60 || {
  487            echo "error: smb did not come up; try: docker logs ${SMB_NAME}" >&2; exit 1; }
  488          # A bound port is not a served share: ask for the share list before
  489          # calling it up, so a container that starts and refuses logins fails
  490          # here rather than in the middle of somebody's fixture.
  491          for _ in $(seq 1 30); do
  492            docker logs "${SMB_NAME}" 2>&1 | grep -q "ready to serve connections" && break
  493            sleep 1
  494          done
  495          docker logs "${SMB_NAME}" 2>&1 | grep -q "ready to serve connections" || {
  496            echo "error: smbd never reported ready; try: docker logs ${SMB_NAME}" >&2; exit 1; }
  497          echo "up: smb share //${GUEST_HOST}/${SMB_SHARE} serving ${DATA} on port ${PORT}"
  498          echo "note: SAVES_REMOTE must start with the share, e.g. $("$0" saves-remote)"
  499          exit 0
  500          ;;
  501  
  502        sftp)
  503          need ssh-keygen
  504          command -v sshd >/dev/null 2>&1 || [ -x /usr/sbin/sshd ] || {
  505            echo "error: sshd is required (looked in PATH and /usr/sbin)" >&2; exit 1; }
  506          SSHD=$(command -v sshd 2>/dev/null || echo /usr/sbin/sshd)
  507          if pid_running; then
  508            echo "up: sftp already serving ${DATA} on port ${PORT}"; exit 0
  509          fi
  510          write_sshd_config
  511          "${SSHD}" -f "${CONFDIR}/sshd_config" -E "${LOGFILE}"
  512          wait_port 30 || { echo "error: sftp did not come up; see ${LOGFILE}" >&2; exit 1; }
  513          # Prove a login, not just a socket: a guard that cannot run has not
  514          # passed, and an sshd that binds but rejects every key looks
  515          # identical from outside.
  516          echo ls | sftp -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  517                -o LogLevel=ERROR -o BatchMode=yes -i "${SFTP_KEY}" -P "${PORT}" \
  518                "${SFTP_USER}@127.0.0.1" >/dev/null 2>&1 || {
  519            echo "error: sftp is listening but the QA key cannot log in; see ${LOGFILE}" >&2; exit 1; }
  520          echo "up: sftp serving ${DATA} at ${SFTP_USER}@127.0.0.1:${PORT} (guest: ${GUEST_HOST}:${PORT})"
  521          echo "note: this sshd cannot chroot unprivileged, so the remotes are absolute: $("$0" saves-remote)"
  522          exit 0
  523          ;;
  524  
  525        ftp)
  526          if pid_running; then
  527            echo "up: ftp already serving ${DATA} on port ${PORT}"; exit 0
  528          fi
  529          PY_BIN=$(venv_python)
  530          write_ftp_server
  531          nohup "${PY_BIN}" "${CONFDIR}/ftpd.py" "${DATA}" "${BIND}" "${PORT}" \
  532                "${USER_NAME}" "${PASS}" "${FTP_MASQ}" "${FTP_PASV_LOW}" "${FTP_PASV_HIGH}" \
  533                > "${LOGFILE}" 2>&1 &
  534          echo $! > "${PIDFILE}"
  535          wait_port 30 || { echo "error: ftp did not come up; see ${LOGFILE}" >&2; exit 1; }
  536          echo "up: ftp serving ${DATA} on port ${PORT} (guest: ${GUEST_HOST}:${PORT}, PASV ${FTP_PASV_LOW}-${FTP_PASV_HIGH} as ${FTP_MASQ})"
  537          exit 0
  538          ;;
  539      esac
  540  
  541      need rclone; need curl
  542      if pid_running; then
  543        echo "up: webdav already serving ${DATA} on port ${PORT}"; exit 0
  544      fi
  545      # --dir-cache-time: rclone serve caches directory listings for five
  546      # minutes by default, so a fixture written into DATA after the server
  547      # starts stays invisible to the device - a test then fails for a reason
  548      # that has nothing to do with the code under test.
  549      # CLOUD_QA_BWLIMIT=1M throttles the server, so a transfer page or a
  550      # progress parser can be watched mid-transfer on a loopback link that
  551      # would otherwise finish before the first frame. rclone's own syntax.
  552      nohup rclone serve webdav "${DATA}" --addr "${BIND}:${PORT}" ${CLOUD_QA_BWLIMIT:+--bwlimit "${CLOUD_QA_BWLIMIT}"} \
  553        --dir-cache-time 1s \
  554        --user "${USER_NAME}" --pass "${PASS}" > "${LOGFILE}" 2>&1 &
  555      echo $! > "${PIDFILE}"
  556      for _ in $(seq 1 30); do
  557        curl -fsS -u "${USER_NAME}:${PASS}" "http://127.0.0.1:${PORT}/" >/dev/null 2>&1 && break
  558        sleep 1
  559      done
  560      curl -fsS -u "${USER_NAME}:${PASS}" "http://127.0.0.1:${PORT}/" >/dev/null 2>&1 || {
  561        echo "error: webdav did not come up; see ${LOGFILE}" >&2; exit 1; }
  562      echo "up: webdav serving ${DATA} at http://127.0.0.1:${PORT} (guest: http://${GUEST_HOST}:${PORT})"
  563      ;;
  564  
  565    down)
  566      name=$(container_of)
  567      if [ -n "${name}" ]; then
  568        docker rm -f "${name}" >/dev/null 2>&1 || true
  569        if [ "${BACKEND}" = s3 ]; then throttle_down; fi
  570      else
  571        [ -f "${PIDFILE}" ] && kill "$(cat "${PIDFILE}")" 2>/dev/null || true
  572        rm -f "${PIDFILE}"
  573        # The pid recorded at start is not always the process that ends up
  574        # holding the socket, so sweep any serve still bound to our port -
  575        # reporting "down" while it is still listening is worse than failing.
  576        for p in $(ss -ltnp 2>/dev/null \
  577                   | awk -v port=":${PORT}\$" '$4 ~ port {print $0}' \
  578                   | grep -oE 'pid=[0-9]+' | cut -d= -f2 | sort -u); do
  579          kill "${p}" 2>/dev/null || true
  580        done
  581      fi
  582      for _ in $(seq 1 10); do
  583        ss -ltn 2>/dev/null | grep -q ":${PORT} " || break
  584        sleep 1
  585      done
  586      if ss -ltn 2>/dev/null | grep -q ":${PORT} "; then
  587        echo "error: something is still listening on ${PORT}" >&2
  588        exit 1
  589      fi
  590      echo "down"
  591      ;;
  592  
  593    reset)
  594      if fs_backed; then
  595        # A plain directory, so resetting is a delete and inspecting it is ls.
  596        rm -rf "${DATA:?}"/* "${DATA:?}"/.[!.]* 2>/dev/null || true
  597        mkdir -p "${DATA}"
  598        # The server caches listings for --dir-cache-time (1s); a device that
  599        # lists within that second still sees what was just deleted. Wait it
  600        # out here, once, so no caller has to know.
  601        settle_cache
  602      else
  603        need rclone
  604        s3 purge "qa-host:${S3_BUCKET}" >/dev/null 2>&1 || true
  605        # MinIO keeps zero-byte "dir/" objects as directory markers. rclone
  606        # without --s3-directory-markers lists them as directories and never
  607        # deletes them, so purge ends BucketNotEmpty behind the || true and the
  608        # "empty" endpoint still holds GAMES/savefiles/ and friends -- which is
  609        # a saves folder that exists, not an empty cloud, and the round trip's
  610        # empty-endpoint step read the difference (2026-09-12). The AWS CLI
  611        # sees every key; where it is installed it takes the markers too, and
  612        # the reset says so if anything survived rather than claiming empty.
  613        if command -v aws >/dev/null 2>&1; then
  614          AWS_ACCESS_KEY_ID="${USER_NAME}" AWS_SECRET_ACCESS_KEY="${PASS}" AWS_EC2_METADATA_DISABLED=true AWS_DEFAULT_REGION=us-east-1 \
  615            aws --endpoint-url "http://127.0.0.1:$(s3_api_port)" s3 rm "s3://${S3_BUCKET}" --recursive >/dev/null 2>&1 || true
  616        fi
  617        s3 mkdir "qa-host:${S3_BUCKET}" >/dev/null
  618        if command -v aws >/dev/null 2>&1; then
  619          left=$(AWS_ACCESS_KEY_ID="${USER_NAME}" AWS_SECRET_ACCESS_KEY="${PASS}" AWS_EC2_METADATA_DISABLED=true AWS_DEFAULT_REGION=us-east-1 \
  620            aws --endpoint-url "http://127.0.0.1:$(s3_api_port)" s3api list-objects-v2 --bucket "${S3_BUCKET}" --query 'KeyCount' --output text 2>/dev/null)
  621          if [ -n "${left}" ] && [ "${left}" != "0" ] && [ "${left}" != "None" ]; then
  622            echo "warning: ${left} object(s) survived the reset of ${S3_BUCKET}" >&2
  623          fi
  624        fi
  625      fi
  626      echo "reset: endpoint is empty"
  627      ;;
  628  
  629    ls)
  630      if fs_backed; then
  631        ( cd "${DATA}${2:+/$2}" 2>/dev/null && find . -type f -printf '%10s %P\n' | sort -k2 ) || true
  632      else
  633        need rclone; s3 ls "qa-host:${S3_BUCKET}${2:+/$2}" 2>/dev/null || true
  634      fi
  635      ;;
  636  
  637    path) echo "${DATA}" ;;
  638  
  639    cat)
  640      # cat <path-under-root> - the bytes the endpoint holds, on any backend;
  641      # reading the WebDAV directory on disk is wrong on S3, where the data is
  642      # in MinIO (the seeding step's note read back as empty there).
  643      [ -n "${2:-}" ] || { echo "usage: cat <path>" >&2; exit 1; }
  644      if fs_backed; then
  645        cat "${DATA}/${2}"
  646      else
  647        need rclone
  648        # rclone cat of a key that does not exist prints nothing and exits 0
  649        # (a missing key reads as an empty prefix), so a check for "the file
  650        # reached the cloud" passed on MinIO for a file that was never there
  651        # (A14, 2026-09-07). Existence first, then the bytes.
  652        s3 lsf --files-only "qa-host:${S3_BUCKET}/${2}" 2>/dev/null | grep -q . \
  653          || { echo "cat: no such file at the endpoint: ${2}" >&2; exit 1; }
  654        s3 cat "qa-host:${S3_BUCKET}/${2}"
  655      fi
  656      ;;
  657  
  658    put)
  659      # put <local-dir> <path-under-root> - stage fixtures at the endpoint
  660      # without going through the device, so a test can exercise restore
  661      # independently of upload.
  662      [ -n "${2:-}" ] && [ -n "${3:-}" ] || { echo "usage: put <local-dir> <path>" >&2; exit 1; }
  663      if fs_backed; then
  664        mkdir -p "${DATA}/${3}"; cp -a "${2}/." "${DATA}/${3}/"
  665        # Same cache as reset: a device that scans right away lists the
  666        # directory as it was a second ago and misses the fixture (the
  667        # unsupported-system step, 2026-09-06).
  668        settle_cache
  669      else
  670        need rclone; s3 copy "${2}" "qa-host:${S3_BUCKET}/${3}" >/dev/null
  671      fi
  672      echo "put: ${3}"
  673      ;;
  674  
  675    status)
  676      name=$(container_of)
  677      if [ -n "${name}" ]; then
  678        docker ps --format '{{.Names}}' | grep -qx "${name}" || { echo "not running"; exit 1; }
  679        extra=""
  680        if [ "${BACKEND}" = s3 ] && [ -f "${S3_API_PORT_FILE}" ]; then
  681          # Throttled: MinIO sits behind the proxy, so the proxy has to be up
  682          # too -- a container that looks fine from here is a refused port to
  683          # the guest when it is not.
  684          if pid_running; then
  685            extra=" (throttled: proxy pid $(cat "${PIDFILE}") on ${PORT}, MinIO on 127.0.0.1:$(s3_api_port))"
  686          else
  687            echo "broken: ${BACKEND} ${name} is up on 127.0.0.1:$(s3_api_port) but its throttle proxy on ${PORT} is not; 'down', then 'up'" >&2
  688            exit 1
  689          fi
  690        fi
  691        echo "running: ${BACKEND} ${name} port ${PORT}${extra}"
  692      elif pid_running; then
  693        echo "running: ${BACKEND} ${DATA} port ${PORT} ($(find "${DATA}" -type f 2>/dev/null | wc -l) files)"
  694      else
  695        echo "not running"; exit 1
  696      fi
  697      ;;
  698  
  699    rclone-conf)
  700      # What goes in /storage/.config/rclone/rclone.conf on the device.
  701      case "${BACKEND}" in
  702        s3)
  703          cat <<EOF
  704  [${REMOTE}]
  705  type = s3
  706  provider = Minio
  707  env_auth = false
  708  access_key_id = ${USER_NAME}
  709  secret_access_key = ${PASS}
  710  endpoint = http://${GUEST_HOST}:${PORT}
  711  force_path_style = true
  712  directory_markers = true
  713  EOF
  714          ;;
  715        sftp)
  716          # key_pem rather than key_file: the harness writes one file onto the
  717          # guest (rclone.conf) and nothing else, so the key has to travel
  718          # inside the stanza. shell_type/disable_hashcheck stop rclone probing
  719          # for a shell it will never get -- this sshd runs internal-sftp and
  720          # nothing else, which is exactly why SFTP is the hash-less row of the
  721          # matrix.
  722          [ -f "${SFTP_KEY}" ] || { echo "error: no QA key yet; run 'up' first" >&2; exit 1; }
  723          cat <<EOF
  724  [${REMOTE}]
  725  type = sftp
  726  host = ${GUEST_HOST}
  727  port = ${PORT}
  728  user = ${SFTP_USER}
  729  key_pem = $(awk '{printf "%s\\n", $0}' "${SFTP_KEY}")
  730  shell_type = none
  731  disable_hashcheck = true
  732  known_hosts_file =
  733  EOF
  734          ;;
  735        smb)
  736          cat <<EOF
  737  [${REMOTE}]
  738  type = smb
  739  host = ${GUEST_HOST}
  740  port = ${PORT}
  741  user = ${USER_NAME}
  742  pass = $(rclone obscure "${PASS}" 2>/dev/null || echo "${PASS}")
  743  EOF
  744          ;;
  745        ftp)
  746          cat <<EOF
  747  [${REMOTE}]
  748  type = ftp
  749  host = ${GUEST_HOST}
  750  port = ${PORT}
  751  user = ${USER_NAME}
  752  pass = $(rclone obscure "${PASS}" 2>/dev/null || echo "${PASS}")
  753  EOF
  754          ;;
  755        *)
  756          cat <<EOF
  757  [${REMOTE}]
  758  type = webdav
  759  url = http://${GUEST_HOST}:${PORT}
  760  vendor = other
  761  user = ${USER_NAME}
  762  pass = $(rclone obscure "${PASS}" 2>/dev/null || echo "${PASS}")
  763  EOF
  764          ;;
  765      esac
  766      ;;
  767  
  768    endpoint-prefix)
  769      # What to strip from a remote path to address this endpoint directly with
  770      # ls/cat/put. Empty where the remote root is the data directory; the
  771      # bucket on S3, the share on SMB, and the absolute path on SFTP, where an
  772      # unprivileged sshd cannot chroot. A caller that hard-codes "the first
  773      # component is the bucket" is right on S3 and wrong on three others.
  774      case "${BACKEND}" in
  775        s3)   echo "/${S3_BUCKET}" ;;
  776        smb)  echo "/${SMB_SHARE}" ;;
  777        sftp) echo "${DATA}" ;;
  778        *)    echo "" ;;
  779      esac
  780      ;;
  781  
  782    caps)
  783      # What this endpoint can and cannot do, so a test that legitimately
  784      # cannot hold here is marked with the reason rather than skipped in
  785      # silence. hash: what rclone can compare besides size. modtime: whether
  786      # rclone can set and read a modification time. commit: whether a PUT cut
  787      # in flight leaves nothing (atomic) or a short file under the final name
  788      # (partial).
  789      # bucket: whether a folder is a prefix on object names and nothing else
  790      # (rclone: BucketBased), so a folder with no objects does not exist and an
  791      # absent one lists as empty -- the shape of #141.
  792      case "${BACKEND}" in
  793        webdav) echo "hash=none modtime=no commit=partial bucket=no" ;;
  794        s3)     echo "hash=md5 modtime=yes commit=atomic bucket=yes" ;;
  795        sftp)   echo "hash=none modtime=yes commit=partial bucket=no" ;;
  796        smb)    echo "hash=none modtime=yes commit=partial bucket=no" ;;
  797        ftp)    echo "hash=none modtime=yes commit=partial bucket=no" ;;
  798      esac
  799      ;;
  800  
  801    saves-remote)
  802      # What SAVES_REMOTE must be for this endpoint. On a path-based backend it is
  803      # just a folder. On a bucket- or share-based one the first component is the
  804      # bucket or share, and it has to be a legal name - lowercase, 3-63 chars for
  805      # S3 - so the shipped "/GAMES" is rejected outright (issue #38). rclone will
  806      # create the bucket itself once the name is valid. On SFTP every path is
  807      # absolute, because an sshd running as an ordinary user cannot chroot.
  808      echo "$("$0" --backend "${BACKEND}" endpoint-prefix)$("$0" shipped-default SAVES_REMOTE)"
  809      ;;
  810  
  811    settings-remote)
  812      # Where the settings-backup archive goes. It must be a SIBLING of syncpath,
  813      # never inside it. Phase 1 syncs syncpath with --delete-excluded and the
  814      # archive is an excluded file, so a nested path is deleted by phase 1. A
  815      # full run hides this - phase 2 re-uploads it moments later - but any run
  816      # that skips the system phase (--saves-only, or BACKUPFILE_BACKUP_OPTION
  817      # set to no) removes the archives and puts nothing back. Verified both
  818      # ways: nested, --saves-only leaves 0 archives; sibling leaves them intact.
  819      echo "$("$0" --backend "${BACKEND}" endpoint-prefix)$("$0" shipped-default SETTINGS_REMOTE)"
  820      ;;
  821  
  822    shipped-default)
  823      # The folder cloud_sync.conf.defaults ships for DEFAULT_<KEY> (SAVES_REMOTE,
  824      # SETTINGS_REMOTE, CONTENT_REMOTE), with its leading slash. The fixtures
  825      # below and vm-qa take the folder names from here: a default copied into
  826      # a fixture as a literal is a second copy of the default, and when the
  827      # fork's folder moved from /ROCKNIX to /Rasteratops (D-CLOUD-156) the
  828      # literals stayed, run 96 read PASS against a cloud laid out by the
  829      # previous build's names, and the frames carried a TIDY UP row for it
  830      # (2026-10-01, blindspot 71). Exits 2 when the key has no default.
  831      defaults="${CLOUD_QA_DEFAULTS:-$(dirname "$(readlink -f "$0")")/../projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf.defaults}"
  832      v=$(sed -n "s|^DEFAULT_${2:-}=\"\([^\"]*\)\"$|\1|p" "${defaults}" 2>/dev/null | head -1)
  833      [ -n "${v}" ] || { echo "shipped-default: no DEFAULT_${2:-} in ${defaults}" >&2; exit 2; }
  834      echo "${v}"
  835      ;;
  836  
  837    content-remote)
  838      # Where cloud_content_backup/restore put whole content directories.
  839      # Same bucket-vs-folder split as syncpath.
  840      echo "$("$0" --backend "${BACKEND}" endpoint-prefix)/CONTENT"
  841      ;;
  842  
  843    seed-content)
  844      # The content-tier fixture (D-CLOUD-048), at the endpoint. Under <root>
  845      # (default the shipped CONTENT_REMOTE, read from cloud_sync.conf.defaults): an SNES folder
  846      # with a ROM the device also has, a ROM only the cloud has, a gamelist
  847      # and a scraped image; an NES folder only the cloud has; a BIOS file.
  848      # With seed-device on the guest, every verdict the systems pages can
  849      # give has a system that produces it: IN YOUR CLOUD ONLY (nes), NOT IN
  850      # YOUR CLOUD YET (gb), N FILES NOT ... (snes), and -- the case that
  851      # opened #76 -- scraped files on one side only, which must not count
  852      # unless the switch is on. Sizes are distinct so a total says which
  853      # files a side holds. Random bytes, so nothing here is a real ROM.
  854      root="${2:-}"
  855      [ -n "${root}" ] || { root=$("$0" shipped-default CONTENT_REMOTE) || exit 2; root="${root#/}"; }
  856      fx=$(mktemp -d)
  857      mkdir -p "${fx}/ROMs/snes/images" "${fx}/ROMs/nes" "${fx}/BIOS"
  858      head -c 300000 /dev/urandom > "${fx}/ROMs/snes/shared.sfc"
  859      head -c 200000 /dev/urandom > "${fx}/ROMs/snes/cloudonly.sfc"
  860      printf '<?xml version="1.0"?>\n<gameList>\n  <game><path>./shared.sfc</path><name>Shared</name></game>\n</gameList>\n' > "${fx}/ROMs/snes/gamelist.xml"
  861      head -c 50000 /dev/urandom > "${fx}/ROMs/snes/images/cloud-image.png"
  862      head -c 100000 /dev/urandom > "${fx}/ROMs/nes/n.nes"
  863      head -c 4096 /dev/urandom > "${fx}/BIOS/foo.bin"
  864      "$0" --backend "${BACKEND}" put "${fx}" "${root}" >/dev/null
  865      rm -rf "${fx}"
  866      echo "seed-content: ${root} holds snes (shared, cloudonly, gamelist, images/), nes, BIOS"
  867      ;;
  868  
  869    seed-device)
  870      # The guest half of seed-content, as a script for the serial console
  871      # (tools/vm-serial script <(./tools/cloud-test-backend seed-device)):
  872      # this endpoint as the device's only remote, the shipped defaults via
  873      # cloud_sync_helper, a reachability check, and device ROMs that pair
  874      # with the fixture -- the shared SNES ROM (same name and size, so it
  875      # counts as present on both sides), one only the device has, scraped
  876      # images/ and videos/ only the device has, and a GB folder the cloud
  877      # has never seen.
  878      root="${2:-}"
  879      [ -n "${root}" ] || { root=$("$0" shipped-default CONTENT_REMOTE) || exit 2; root="${root#/}"; }
  880      # CONTENT_REMOTE is a path the device gives rclone, so it carries the
  881      # bucket, share or absolute root this backend needs; seed-content's
  882      # <root> is endpoint-relative and does not.
  883      cr="$("$0" --backend "${BACKEND}" endpoint-prefix)/${root}"
  884      cat <<EOF
  885  mkdir -p /storage/.config/rclone
  886  cat > /storage/.config/rclone/rclone.conf <<'RC'
  887  $("$0" --backend "${BACKEND}" rclone-conf)
  888  RC
  889  printf '%s\n' '${REMOTE}' > /storage/.config/rclone/active-connection
  890  chmod 600 /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection
  891  /usr/bin/cloud_sync_helper >/dev/null 2>&1
  892  grep -q '^CONTENT_REMOTE="${cr}"' /storage/.config/cloud_sync.conf || sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="${cr}"|' /storage/.config/cloud_sync.conf
  893  /usr/bin/cloud_setup --check
  894  mkdir -p /storage/roms/snes/images /storage/roms/snes/videos /storage/roms/gb
  895  head -c 300000 /dev/zero | tr '\0' 'S' > /storage/roms/snes/shared.sfc
  896  head -c 150000 /dev/urandom > /storage/roms/snes/deviceonly.sfc
  897  printf '<?xml version="1.0"?>\n<gameList>\n  <game><path>./shared.sfc</path><name>Shared</name></game>\n</gameList>\n' > /storage/roms/snes/gamelist.xml
  898  head -c 60000 /dev/urandom > /storage/roms/snes/images/a.png
  899  head -c 250000 /dev/urandom > /storage/roms/snes/videos/a.mp4
  900  head -c 80000 /dev/urandom > /storage/roms/gb/only.gb
  901  echo "seeded: \$(find /storage/roms/snes /storage/roms/gb -type f | wc -l) device files"
  902  EOF
  903      ;;
  904  
  905    dead-conf)
  906      # The same stanza, pointing at the dead port: a cloud that refuses.
  907      CLOUD_QA_PORT="${DEAD_PORT}" exec "$0" --backend "${BACKEND}" rclone-conf
  908      ;;
  909  
  910    dead-port)   echo "${DEAD_PORT}" ;;
  911    remote-name) echo "${REMOTE}" ;;
  912    backend)     echo "${BACKEND}" ;;
  913    backends)    echo "webdav s3 sftp smb ftp" ;;
  914    port)        echo "${PORT}" ;;
  915  
  916    *)
  917      echo "usage: ${0##*/} [--backend webdav|s3|sftp|smb|ftp] {up|down|reset|ls [path]|path|cat <path>|put <dir> <path>|status|rclone-conf|caps|dead-conf|dead-port|endpoint-prefix|saves-remote|settings-remote|content-remote|seed-content|seed-device|remote-name|backend|backends|port}" >&2
  918      exit 1
  919      ;;
  920  esac
```

## File: tools/cloud-capture-stamp-test (at 8ebaf8daad, 116 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # cloud-capture-stamp-test - a device-less check of cloud_capture's durable
    6  # stamp: finish() keeps ONE LINE PER MODE in last-capture (D-CLOUD-070, #94),
    7  # so the boot --full pass no longer writes over the record of the last game
    8  # exit, and a one-line stamp from an older build is read as its mode's line.
    9  #
   10  # It lifts finish() out of the script it is given (default: the repo's
   11  # cloud_capture), runs it in a subshell with CACHE pointed at a temp directory
   12  # and `date` faked so every epoch is chosen, and reads the file back. The same
   13  # sequence runs on a device as tools/cloud-round-trip's CAP12; this is what
   14  # runs when there is no device. To watch the guard fire, point it at the
   15  # finish() from before the change:
   16  #
   17  #     git show f451252587:projects/ROCKNIX/packages/network/rclone/sources/cloud_capture > /tmp/old
   18  #     tools/cloud-capture-stamp-test /tmp/old      # FAILs: one line, overwritten
   19  #     tools/cloud-capture-stamp-test               # PASSED
   20  #
   21  # Exit 0 when every check passes, 1 otherwise, 2 when it cannot run.
   22  set -u
   23  
   24  SCRIPT="${1:-$(dirname "$(readlink -f "$0")")/../projects/ROCKNIX/packages/network/rclone/sources/cloud_capture}"
   25  [ -r "${SCRIPT}" ] || { echo "cannot read ${SCRIPT}" >&2; exit 2; }
   26  
   27  # finish() as the script defines it, and nothing else of the script: it
   28  # reads MODE, CARD, UNIT, RC, REASON, EXITCODE, EMULATOR, CORE and CACHE, and
   29  # calls date, mkdir, printf, cat, tail, mv (and awk since D-CLOUD-070).
   30  FINISH="$(sed -n '/^finish() {/,/^}/p' "${SCRIPT}")"
   31  [ -n "${FINISH}" ] || { echo "no finish() found in ${SCRIPT}" >&2; exit 2; }
   32  
   33  TMP="$(mktemp -d)"; trap 'rm -rf "${TMP}"' EXIT
   34  CACHE="${TMP}/cloud_sync"
   35  STAMP="${CACHE}/last-capture"
   36  FAIL=0
   37  
   38  check() { # <0|nonzero> ok-text bad-text
   39      if [ "$1" -eq 0 ]; then echo "    PASS  $2"; else echo "    FAIL  $3"; FAIL=$((FAIL + 1)); fi
   40  }
   41  
   42  # One run of finish(): the epoch `date` will answer, then the run's context.
   43  # finish() ends in `exit`, so it runs in a subshell; its status is the rc.
   44  stamp() { # NOW MODE RC UNIT [CARD] [EXITCODE] [EMULATOR] [CORE]
   45      (
   46          eval "${FINISH}"
   47          date() { echo "${FAKE_NOW}"; }
   48          FAKE_NOW="$1" MODE="$2" RC="$3" UNIT="$4" CARD="${5:-}" EXITCODE="${6:-?}" \
   49              EMULATOR="${7:-}" CORE="${8:-}" REASON="" CACHE="${CACHE}"
   50          finish "${RC}" >/dev/null 2>&1
   51      )
   52  }
   53  
   54  lines()   { [ -e "${STAMP}" ] && grep -c . "${STAMP}" || echo 0; }
   55  modes()   { awk 'NF >= 3 { f = $3; sub(/!.*$/, "", f); print f }' "${STAMP}" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//'; }
   56  line_of() { awk -v m="$1" 'NF >= 3 { f = $3; sub(/!.*$/, "", f); if (f == m) print }' "${STAMP}" 2>/dev/null; }
   57  show()    { echo "          last-capture: $(lines) line(s)"; sed 's/^/          | /' "${STAMP}" 2>/dev/null; }
   58  
   59  echo "cloud-capture-stamp-test: finish() from ${SCRIPT}"
   60  
   61  echo "  1. a first exit writes the one line it always did"
   62  mkdir -p "${CACHE}"
   63  stamp 1000 exit 0 "gba:Game" "" 0 retroarch mgba
   64  want="1000 0 exit gba:Game emu-exit=0 retroarch/mgba"
   65  [ "$(cat "${STAMP}" 2>/dev/null)" = "${want}" ]; check $? "the stamp is exactly '${want}'" "the stamp is '$(cat "${STAMP}" 2>/dev/null)', not '${want}'"
   66  
   67  echo "  2. a one-line stamp from before (an exit) survives a --full pass byte for byte"
   68  old="900 0 exit gba:Before emu-exit=0 retroarch/mgba"
   69  printf '%s\n' "${old}" > "${STAMP}"
   70  stamp 2000 full 0 ""
   71  grep -qxF "${old}" "${STAMP}"; check $? "the old exit line is still there, unchanged" "the old exit line is gone: $(show)"
   72  [ "$(lines)" = 2 ] && [ "$(modes)" = "exit full" ]; check $? "two lines: exit and full" "$(lines) line(s), modes '$(modes)'"
   73  [ "$(line_of full)" = "2000 0 full - emu-exit=? -/-" ]; check $? "the full line reads '2000 0 full - emu-exit=? -/-'" "the full line is '$(line_of full)'"
   74  show
   75  
   76  echo "  3. an exit replaces the exit line only"
   77  stamp 3000 exit 0 "gba:Game" "" 1 retroarch mgba
   78  [ "$(line_of exit)" = "3000 0 exit gba:Game emu-exit=1 retroarch/mgba" ]; check $? "the exit line is this run's" "the exit line is '$(line_of exit)'"
   79  ! grep -qxF "${old}" "${STAMP}" && [ "$(line_of full)" = "2000 0 full - emu-exit=? -/-" ] && [ "$(lines)" = 2 ]
   80  check $? "the old exit line is gone, the full line stands, still two lines" "expected the exit line replaced and the full line kept; $(show)"
   81  
   82  echo "  4. a second --full replaces the full line only"
   83  stamp 4000 full 0 ""
   84  [ "$(line_of full)" = "4000 0 full - emu-exit=? -/-" ] && [ "$(line_of exit)" = "3000 0 exit gba:Game emu-exit=1 retroarch/mgba" ] && [ "$(lines)" = 2 ]
   85  check $? "full line at 4000, exit line unchanged, two lines" "expected the full line replaced and the exit line kept; $(show)"
   86  
   87  echo "  5. every other mode is its own line; none appears twice"
   88  stamp 5000 retire 0 ""
   89  stamp 6000 rescan 0 "gba:Game"
   90  stamp 7000 "" 2 ""          # a bad invocation: MODE empty reads as usage
   91  [ "$(lines)" = 5 ] && [ "$(modes)" = "exit full rescan retire usage" ]; check $? "five lines: exit full rescan retire usage" "$(lines) line(s), modes '$(modes)'"
   92  [ "$(line_of usage)" = "7000 2 usage - emu-exit=? -/-" ]; check $? "the usage line carries rc 2" "the usage line is '$(line_of usage)'"
   93  show
   94  
   95  echo "  6. the !card marker does not make a second exit line"
   96  stamp 8000 exit 0 "gba:Game" "!card" 0 retroarch mgba
   97  [ "$(lines)" = 5 ] && [ "$(line_of exit)" = "8000 0 exit!card gba:Game emu-exit=0 retroarch/mgba" ]
   98  check $? "exit!card replaced the exit line; still five lines" "expected five lines with exit!card in the exit slot; $(show)"
   99  stamp 9000 exit 0 "gba:Game" "" 0 retroarch mgba
  100  [ "$(lines)" = 5 ] && [ "$(line_of exit)" = "9000 0 exit gba:Game emu-exit=0 retroarch/mgba" ]
  101  check $? "and a plain exit replaced the exit!card line" "expected five lines with a plain exit in the slot; $(show)"
  102  
  103  echo "  7. a file that somehow holds a mode twice converges on the next run of that mode"
  104  printf '%s\n' "100 0 exit gba:A emu-exit=0 retroarch/mgba" "200 0 full - emu-exit=? -/-" "300 0 exit gba:B emu-exit=0 retroarch/mgba" "" > "${STAMP}"
  105  stamp 9500 exit 0 "gba:C" "" 0 retroarch mgba
  106  [ "$(lines)" = 2 ] && [ "$(line_of exit)" = "9500 0 exit gba:C emu-exit=0 retroarch/mgba" ] && [ "$(line_of full)" = "200 0 full - emu-exit=? -/-" ]
  107  check $? "one exit line, the full line kept, the blank line dropped" "expected two lines, exit gba:C and the full line; $(show)"
  108  
  109  echo "  8. a unit with spaces still parses from the back, and nothing is left beside the stamp"
  110  stamp 9900 exit 0 "gba:Two Words" "" 0 retroarch mgba
  111  [ "$(line_of exit | awk '{print $(NF-1), $NF}')" = "emu-exit=0 retroarch/mgba" ]; check $? "the two trailing fields are intact past a spaced unit" "exit line '$(line_of exit)'"
  112  left="$(ls -A "${CACHE}" | grep -v -e '^last-capture$' -e '^capture-failures$' || true)"
  113  [ -z "${left}" ]; check $? "no temp file left in the cache directory" "left behind: ${left}"
  114  
  115  echo
  116  if [ "${FAIL}" -eq 0 ]; then echo "PASSED"; exit 0; else echo "${FAIL} CHECK(S) FAILED"; exit 1; fi
```

## File: tools/cloud-census (at 8ebaf8daad, 306 lines)

```text
    1  #!/usr/bin/env python3
    2  """The census (Gate 12, #11): what a game exit actually writes, on a handheld.
    3  
    4  Read-only. `begin` records the saves tier as the sync sees it -- every file
    5  the shipped allowlist admits under the saves root, with size, mtime and
    6  sha256 -- plus the log positions. The owner then plays. `report` records it
    7  again and reads the difference: which files each session wrote, grouped by
    8  emulator; how many bytes an exit seals; what retention at count 3 would hold;
    9  and what the exit push cost, from the sync log. Those numbers are #21's unit
   10  table and #22's admission ceiling.
   11  
   12      ./tools/cloud-census --host root@192.168.1.81 begin  --out census.json
   13      ...the owner plays...
   14      ./tools/cloud-census --host root@192.168.1.81 report --baseline census.json
   15  
   16  Nothing on the device is written, moved or restarted (D-QA-008). It runs
   17  over SSH and reads /storage, /var/log/cloud_sync.log and EmulationStation's
   18  log; the device's own scripts are not run.
   19  """
   20  
   21  import argparse
   22  import json
   23  import os
   24  import re
   25  import shlex
   26  import subprocess
   27  import sys
   28  import time
   29  from collections import defaultdict
   30  
   31  RULES = "/storage/.config/cloud_sync-rules.txt"
   32  SYNC_LOG = "/var/log/cloud_sync.log"
   33  ES_LOG = "/storage/.config/emulationstation/es_log.txt"
   34  CONF = "/storage/.config/cloud_sync.conf"
   35  SESSION_GAP = 180   # seconds between writes that separates two sessions in one system
   36  
   37  
   38  def ssh(args, cmd):
   39      base = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
   40              "-o", "LogLevel=ERROR", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", "-p", str(args.port)]
   41      if args.identity:
   42          base += ["-i", args.identity]
   43      p = subprocess.run(base + [args.host, cmd], capture_output=True, text=True)
   44      if p.returncode != 0:
   45          sys.exit(f"ssh {args.host}: {p.stderr.strip() or p.stdout.strip() or p.returncode}")
   46      return p.stdout
   47  
   48  
   49  def snapshot(args):
   50      """The saves tier as rclone would list it, with size, mtime, sha256."""
   51      root = ssh(args, f". {CONF} 2>/dev/null; echo \"${{SAVESPATH:-/storage/roms}}\"").strip()
   52      # rclone applies the allowlist exactly as the sync does; busybox stat and
   53      # sha256sum do the rest. Paths may hold spaces, so the list is read
   54      # line by line and every use is quoted.
   55      listing = ssh(args, (
   56          f"cd {shlex.quote(root)} && rclone lsf -R --files-only --filter-from {RULES} . 2>/dev/null | "
   57          "while IFS= read -r f; do "
   58          "  s=$(stat -c '%s %Y' \"$f\" 2>/dev/null) || continue; "
   59          "  h=$(sha256sum \"$f\" 2>/dev/null | cut -c1-64); "
   60          "  printf '%s|%s|%s\\n' \"$s\" \"$h\" \"$f\"; done"))
   61      files = {}
   62      for line in listing.splitlines():
   63          parts = line.split("|", 2)
   64          if len(parts) != 3:
   65              continue
   66          size_mtime, sha, path = parts
   67          size, mtime = size_mtime.split()
   68          files[path] = {"size": int(size), "mtime": int(mtime), "sha256": sha}
   69      meta = ssh(args, (
   70          f"echo device_time=$(date +%s); "
   71          f"echo sync_log_lines=$(wc -l < {SYNC_LOG} 2>/dev/null || echo 0); "
   72          f"echo es_log_lines=$(wc -l < {ES_LOG} 2>/dev/null || echo 0); "
   73          "echo exit_sync=$(grep -o 'cloudsaves.gameexit=[01]' /storage/.config/system/configs/system.cfg 2>/dev/null | cut -d= -f2); "
   74          "echo startup_sync=$(grep -o 'cloudsaves.startup=[01]' /storage/.config/system/configs/system.cfg 2>/dev/null | cut -d= -f2); "
   75          "echo build=$(grep ^BUILD_ID= /etc/os-release | cut -c11-20); "
   76          "echo device=$(cloud_device_id 2>/dev/null); "
   77          "echo tz=$(date +%z)"))
   78      m = dict(l.split("=", 1) for l in meta.splitlines() if "=" in l)
   79      return {"taken_at": int(time.time()), "root": root, "files": files, "meta": m}
   80  
   81  
   82  def family(path):
   83      """Which emulator layout a save path belongs to -- the unit table's rows."""
   84      p = path.lower()
   85      if p.startswith("savestates/"):
   86          return "savestates (libretro)"
   87      if p.startswith("n64/save/"):
   88          return "n64 (mupen: .eep/.mpk/.sra)"
   89      if p.startswith("psx/memcards/"):
   90          return "psx (duckstation memcards)"
   91      if p.startswith("dc/shared/"):
   92          return "dc (flycast VMU)"
   93      if p.startswith("psp/ppsspp/"):
   94          return "psp (ppsspp savedata)"
   95      if p.startswith("screenshots/"):
   96          return "screenshots"
   97      if p.startswith("savefiles/"):
   98          return "savefiles"
   99      return f"{p.split('/')[0]} (in-game save beside the ROM)"
  100  
  101  
  102  def game_of(path):
  103      """The game a save path names, as well as a path can say it."""
  104      base = os.path.basename(path)
  105      base = re.sub(r"\.(state\d*|auto|state\d*\.png|state\.auto\.png|png)$", "", base, flags=re.I)
  106      return os.path.splitext(base)[0] if "." in base else base
  107  
  108  
  109  def sync_log_since(args, line):
  110      return ssh(args, f"tail -n +{int(line) + 1} {SYNC_LOG} 2>/dev/null || true")
  111  
  112  
  113  def es_log_since(args, line):
  114      return ssh(args, f"tail -n +{int(line) + 1} {ES_LOG} 2>/dev/null || true")
  115  
  116  
  117  def runs_from_sync_log(text):
  118      """Each cloud_backup/cloud_restore run in the log: when, what, how long, how much."""
  119      runs, cur = [], None
  120      for l in text.splitlines():
  121          m = re.match(r"\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\] \[\w+\] \[(cloud_\w+)\] (.*)", l)
  122          if m:
  123              when, script, msg = m.groups()
  124              if "STARTING" in msg and "BACKUP" in msg or "STARTING" in msg and "RESTORE" in msg:
  125                  cur = {"when": when, "script": script, "recent": False, "spawns": 0, "seconds": None,
  126                         "exit": None, "bytes": None, "files": None}
  127                  runs.append(cur)
  128              if cur is None:
  129                  continue
  130              if msg.startswith("recent:"):
  131                  cur["recent"] = True
  132              if msg.startswith("About to execute: rclone"):
  133                  cur["spawns"] += 1
  134              mm = re.search(r"completed in (\d+) seconds with exit code (\d+)", msg)
  135              if mm:
  136                  cur["seconds"], cur["exit"] = int(mm.group(1)), int(mm.group(2))
  137                  cur = None
  138          elif cur is not None:
  139              mm = re.match(r"Transferred:\s+([\d.]+ \w*B) / ([\d.]+ \w*B),", l)
  140              if mm:
  141                  cur["bytes"] = mm.group(1)
  142              mm = re.match(r"Transferred:\s+(\d+) / (\d+),", l)
  143              if mm:
  144                  cur["files"] = mm.group(1)
  145      return runs
  146  
  147  
  148  def sessions_from_es_log(text):
  149      """Game launches and returns, where EmulationStation logged them."""
  150      out = []
  151      for l in text.splitlines():
  152          if re.search(r"launch|Launching|running command|game-start|game-end", l, re.I):
  153              out.append(l.strip()[:160])
  154      return out
  155  
  156  
  157  def local(ts, meta):
  158      """A device epoch as the device's own wall clock, the way its logs read."""
  159      tz = meta.get("tz", "+0000")
  160      sign = -1 if tz.startswith("-") else 1
  161      off = sign * (int(tz[1:3]) * 3600 + int(tz[3:5]) * 60) if len(tz) == 5 else 0
  162      return time.strftime("%H:%M:%S", time.gmtime(ts + off))
  163  
  164  
  165  def human(n):
  166      for unit in ("B", "KB", "MB", "GB"):
  167          if n < 1024 or unit == "GB":
  168              return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
  169          n /= 1024.0
  170  
  171  
  172  def report(args, before, after):
  173      b, a = before["files"], after["files"]
  174      changed = {p: a[p] for p in a if p not in b or a[p]["sha256"] != b[p]["sha256"]}
  175      removed = sorted(p for p in b if p not in a)
  176      out = []
  177      m = after["meta"]
  178      out.append(f"# Census — {m.get('device', '?')} on {m.get('build', '?')}, "
  179                 f"{time.strftime('%Y-%m-%d', time.gmtime(before['taken_at']))} "
  180                 f"{local(before['taken_at'], m)}–{local(after['taken_at'], m)} device time (UTC{m.get('tz', '')})")
  181      out.append("")
  182      out.append(f"Saves tier under `{after['root']}` as the allowlist admits it: {len(b)} files before, {len(a)} after; "
  183                 f"**{len(changed)} written or changed**, {len(removed)} removed (a file created *and* deleted inside the window "
  184                 f"is invisible to two snapshots, and ES's renumber reuses the deleted slot's path -- so a deletion shows here only "
  185                 f"when it removed a file the baseline had). Exit sync was "
  186                 f"{'ON' if after['meta'].get('exit_sync') == '1' else 'OFF'}, startup sync "
  187                 f"{'ON' if after['meta'].get('startup_sync') == '1' else 'OFF'}.")
  188      out.append("")
  189  
  190      # Sessions: per system directory, writes clustered by mtime.
  191      by_sys = defaultdict(list)
  192      for p, e in changed.items():
  193          by_sys[p.split("/")[0] if not p.startswith("savestates/") else "/".join(p.split("/")[:2])].append((e["mtime"], p, e))
  194      sessions = []
  195      for sysdir, items in by_sys.items():
  196          items.sort()
  197          cur = []
  198          for mt, p, e in items:
  199              if cur and mt - cur[-1][0] > SESSION_GAP:
  200                  sessions.append((sysdir, cur)); cur = []
  201              cur.append((mt, p, e))
  202          if cur:
  203              sessions.append((sysdir, cur))
  204      sessions.sort(key=lambda s: s[1][0][0])
  205  
  206      out.append("## Sessions (writes clustered by time, per system)")
  207      out.append("")
  208      out.append("| # | When (device time) | System | Files written | Bytes sealed | What |")
  209      out.append("| --- | --- | --- | --- | --- | --- |")
  210      for i, (sysdir, items) in enumerate(sessions, 1):
  211          bytes_ = sum(e["size"] for _, _, e in items)
  212          kinds = sorted({os.path.splitext(p)[1] or os.path.basename(p) for _, p, _ in items})
  213          games = sorted({game_of(p) for _, p, _ in items})
  214          out.append(f"| {i} | {local(items[0][0], m)} | {sysdir} | {len(items)} | {human(bytes_)} | "
  215                     f"{', '.join(kinds)[:60]} — {', '.join(games)[:50]} |")
  216      if not sessions:
  217          out.append("| — | — | — | 0 | 0 | nothing changed in the saves tier |")
  218      out.append("")
  219  
  220      # The unit table: per family, which extensions travel together for one game in one session.
  221      out.append("## Unit table (per emulator layout: what one game writes in one session)")
  222      out.append("")
  223      out.append("| Layout | Sessions | Files per session (min–max) | Bytes per session (min–max) | Members seen together |")
  224      out.append("| --- | --- | --- | --- | --- |")
  225      fam = defaultdict(list)
  226      for sysdir, items in sessions:
  227          for g in {game_of(p) for _, p, _ in items}:
  228              members = [(p, e) for _, p, e in items if game_of(p) == g]
  229              fam[family(members[0][0])].append(members)
  230      for f, groups in sorted(fam.items()):
  231          counts = [len(g) for g in groups]
  232          sizes = [sum(e["size"] for _, e in g) for g in groups]
  233          exts = sorted({(os.path.splitext(p)[1] or os.path.basename(p)) for g in groups for p, _ in g})
  234          out.append(f"| {f} | {len(groups)} | {min(counts)}–{max(counts)} | {human(min(sizes))}–{human(max(sizes))} | {', '.join(exts)} |")
  235      if not fam:
  236          out.append("| — | 0 | — | — | — |")
  237      out.append("")
  238  
  239      # Retention at count 3, per unit: three versions of each unit's members.
  240      total_unit_bytes = sum(sum(e["size"] for _, e in g) for groups in fam.values() for g in groups)
  241      largest = max((sum(e["size"] for _, e in g) for groups in fam.values() for g in groups), default=0)
  242      out.append("## Retention and ceiling")
  243      out.append("")
  244      out.append(f"- Bytes sealed across every session: **{human(total_unit_bytes)}**; the largest single unit written: **{human(largest)}**.")
  245      out.append(f"- Retention at count 3 for these units alone: **{human(3 * total_unit_bytes)}** in the discarded store, if every one lost a decision three times (the bound, not the expectation).")
  246      out.append(f"- Largest per-file write: **{human(max((e['size'] for e in changed.values()), default=0))}**.")
  247      out.append("")
  248  
  249      # The exit push, from the sync log.
  250      runs = runs_from_sync_log(sync_log_since(args, before["meta"].get("sync_log_lines", 0)))
  251      out.append("## The exit push, from /var/log/cloud_sync.log since the baseline")
  252      out.append("")
  253      out.append("| When | Script | --recent | rclone spawns | Seconds | Exit | Bytes | Files |")
  254      out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
  255      for r in runs:
  256          out.append(f"| {r['when']} | {r['script']} | {'yes' if r['recent'] else 'no'} | {r['spawns']} | {r['seconds']} | {r['exit']} | {r['bytes'] or '—'} | {r['files'] or '—'} |")
  257      if not runs:
  258          out.append("| — | — | — | — | — | — | — | no cloud_backup/cloud_restore run was logged in the window |")
  259      out.append("")
  260  
  261      es = sessions_from_es_log(es_log_since(args, before["meta"].get("es_log_lines", 0)))
  262      if es:
  263          out.append("## EmulationStation's own record of launches")
  264          out.append("")
  265          for l in es[:40]:
  266              out.append(f"    {l}")
  267          out.append("")
  268  
  269      out.append("## Every changed file")
  270      out.append("")
  271      out.append("| Path | Size | mtime (device time) | Before |")
  272      out.append("| --- | --- | --- | --- |")
  273      for p in sorted(changed, key=lambda p: changed[p]["mtime"]):
  274          e = changed[p]
  275          out.append(f"| `{p}` | {e['size']} | {local(e['mtime'], m)} | "
  276                     f"{'new' if p not in b else 'changed (' + str(b[p]['size']) + ' B)'} |")
  277      for p in removed:
  278          out.append(f"| `{p}` | — | — | removed ({b[p]['size']} B) |")
  279      return "\n".join(out) + "\n"
  280  
  281  
  282  def main():
  283      ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  284      ap.add_argument("--host", required=True)
  285      ap.add_argument("--port", type=int, default=22)
  286      ap.add_argument("--identity")
  287      sub = ap.add_subparsers(dest="cmd", required=True)
  288      b = sub.add_parser("begin"); b.add_argument("--out", required=True)
  289      r = sub.add_parser("report"); r.add_argument("--baseline", required=True); r.add_argument("--out")
  290      args = ap.parse_args()
  291      if args.cmd == "begin":
  292          snap = snapshot(args)
  293          json.dump(snap, open(args.out, "w"), indent=1)
  294          print(f"baseline: {len(snap['files'])} files in the saves tier under {snap['root']} on {snap['meta'].get('device')} "
  295                f"({snap['meta'].get('build')}); exit sync {'ON' if snap['meta'].get('exit_sync') == '1' else 'OFF'}; written to {args.out}")
  296          return 0
  297      before = json.load(open(args.baseline))
  298      text = report(args, before, snapshot(args))
  299      if args.out:
  300          open(args.out, "w").write(text)
  301      print(text)
  302      return 0
  303  
  304  
  305  if __name__ == "__main__":
  306      sys.exit(main())
```

## File: tools/cloud-connections-test (at 8ebaf8daad, 307 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Credential-free regression tests using the actual connection module/rclone."""
    5  import importlib.util
    6  import os
    7  from pathlib import Path
    8  import subprocess
    9  import sys
   10  import tempfile
   11  import unittest
   12  import importlib.machinery
   13  from unittest import mock
   14  
   15  ROOT = Path(__file__).resolve().parents[1]
   16  SOURCE = ROOT / 'projects/ROCKNIX/packages/network/rclone/sources'
   17  sys.path.insert(0, str(SOURCE))
   18  import cloud_connections as c
   19  
   20  class Connections(unittest.TestCase):
   21      def setUp(self):
   22          self.tmp = tempfile.TemporaryDirectory()
   23          self.addCleanup(self.tmp.cleanup)
   24          self.root = Path(self.tmp.name)
   25          c.CONFIG = self.root / 'rclone.conf'
   26          c.ACTIVE = self.root / 'active-connection'
   27          c.LOCK = self.root / 'cloud.lock'
   28          c.SYSTEM = self.root / 'system.cfg'
   29          self.data = self.root / 'files'
   30          self.data.mkdir()
   31          self.settings = [('remote', str(self.data))]
   32          c.CONFIG.write_text('[zulu]\ntype = alias\nremote = %s\n' % self.data)
   33          self.original = c.CONFIG.read_bytes()
   34  
   35      def test_encrypted_config_stays_encrypted_through_management(self):
   36          import pexpect
   37          password = '<redacted: a synthetic QA fixture value that T10's widened pattern matches>'
   38          child = pexpect.spawn(c.RCLONE, ['--config', str(c.CONFIG), 'config'], encoding='utf-8', timeout=5)
   39          try:
   40              child.expect('e/n/d/r/c/s/q>'); child.sendline('s')
   41              child.expect('a/q>'); child.sendline('a')
   42              child.expect('Enter NEW configuration password:'); child.sendline(password)
   43              child.expect('Confirm NEW configuration password:'); child.sendline(password)
   44              child.expect('c/u/q>'); child.sendline('q')
   45              child.expect('e/n/d/r/c/s/q>'); child.sendline('q')
   46              child.expect(pexpect.EOF)
   47          finally:
   48              child.close(force=True)
   49          self.assertIn(b'RCLONE_ENCRYPT_V0:', c.CONFIG.read_bytes())
   50          with mock.patch.dict(os.environ, {'RCLONE_CONFIG_PASS': password}):
   51              self.assertEqual(c.active(), 'zulu')
   52              c.save('alpha', 'alias', self.settings)
   53              c.save('zulu', 'alias', self.settings, replace=True)
   54              c.select('alpha'); c.remove('alpha')
   55              self.assertEqual(c.active(), '')
   56              self.assertEqual(c.read_config()[1]['zulu']['remote'], str(self.data))
   57          self.assertIn(b'RCLONE_ENCRYPT_V0:', c.CONFIG.read_bytes())
   58          self.assertNotIn(str(self.data).encode(), c.CONFIG.read_bytes())
   59  
   60      def test_add_keeps_legacy_selection(self):
   61          c.save('alpha', 'alias', self.settings)
   62          self.assertEqual(c.active(), 'zulu')
   63          self.assertEqual(c.ACTIVE.stat().st_mode & 0o777, 0o600)
   64          self.assertEqual(c.CONFIG.stat().st_mode & 0o777, 0o600)
   65          self.assertEqual(c.read_config()[1]['zulu']['remote'], str(self.data))
   66  
   67      def test_failed_first_publication_restores_absence(self):
   68          c.CONFIG.unlink()
   69          def failed_record(commit):
   70              commit()
   71              raise OSError('record failed')
   72          with self.assertRaises(OSError): c.save('alpha', 'alias', self.settings, publish=failed_record)
   73          self.assertFalse(c.CONFIG.exists())
   74          self.assertFalse(c.ACTIVE.exists())
   75  
   76      def test_duplicate_keeps_old_bytes(self):
   77          with self.assertRaises(c.Refused): c.save('zulu', 'alias', self.settings)
   78          self.assertEqual(c.CONFIG.read_bytes(), self.original)
   79          self.assertFalse(c.ACTIVE.exists())
   80  
   81      def test_failed_renewal_keeps_old_bytes(self):
   82          with self.assertRaises(c.Refused): c.save('zulu', 'alias', [('remote', str(self.root/'absent'))], replace=True)
   83          self.assertEqual(c.CONFIG.read_bytes(), self.original)
   84          self.assertEqual(list(self.root.glob('.connection-*')), [])
   85  
   86      def test_cancelled_attempt_does_not_install(self):
   87          def cancelled(commit): raise c.Refused('cancelled')
   88          with self.assertRaises(c.Refused): c.save('alpha', 'alias', self.settings, publish=cancelled)
   89          self.assertEqual(c.CONFIG.read_bytes(), self.original)
   90  
   91      def test_success_record_failure_rolls_back(self):
   92          def failed_record(commit):
   93              commit()
   94              raise OSError('record failed')
   95          with self.assertRaises(OSError): c.save('zulu', 'alias', self.settings, replace=True, publish=failed_record)
   96          self.assertEqual(c.CONFIG.read_bytes(), self.original)
   97          self.assertFalse(c.ACTIVE.exists())
   98  
   99      def test_remove_write_failure_restores_selection(self):
  100          atomic = c.atomic
  101          def failed_config(path, data):
  102              if path == c.CONFIG:
  103                  raise OSError('synthetic write failure')
  104              atomic(path, data)
  105          for selected in (None, b'zulu\n'):
  106              if selected is None:
  107                  c.ACTIVE.unlink(missing_ok=True)
  108              else:
  109                  c.ACTIVE.write_bytes(selected)
  110              with mock.patch.object(c, 'atomic', side_effect=failed_config):
  111                  with self.assertRaises(OSError): c.remove('zulu')
  112              self.assertEqual(c.CONFIG.read_bytes(), self.original)
  113              self.assertEqual(c.ACTIVE.read_bytes() if c.ACTIVE.exists() else None, selected)
  114  
  115      def test_external_write_refuses_commit(self):
  116          def changed(commit):
  117              c.CONFIG.write_bytes(self.original + b'other = preserved\n')
  118              commit()
  119          with self.assertRaises(c.Refused): c.save('alpha', 'alias', self.settings, publish=changed)
  120          self.assertEqual(c.CONFIG.read_bytes(), self.original + b'other = preserved\n')
  121  
  122      def test_selection_and_removal_never_move_files(self):
  123          marker = self.data / 'save.srm'; marker.write_bytes(b'fixture-save')
  124          c.save('alpha', 'alias', self.settings)
  125          c.select('alpha')
  126          self.assertEqual(c.active(), 'alpha')
  127          c.remove('alpha')
  128          self.assertEqual(c.active(), '')
  129          self.assertIn('zulu', c.read_config()[1])
  130          self.assertEqual(marker.read_bytes(), b'fixture-save')
  131  
  132      def test_selection_refusal_distinguishes_saved_connections_from_none(self):
  133          for value in ('', 'missing'):
  134              c.ACTIVE.write_text(value + '\n')
  135              self.assertEqual(c.selection_reason(), 'CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.')
  136          c.CONFIG.write_text('')
  137          self.assertEqual(c.selection_reason(), "YOUR CLOUD STORAGE ISN'T SET UP YET")
  138  
  139      def test_missing_selection_never_falls_back(self):
  140          c.ACTIVE.write_text('missing\n')
  141          with self.assertRaises(c.Refused): c.active()
  142          c.select('zulu')
  143          self.assertEqual(c.active(), 'zulu')
  144  
  145      def test_automatic_sync_requires_deliberate_disable(self):
  146          c.SYSTEM.write_text('cloudsaves.startup=1\ncloudsaves.gameexit=0\n')
  147          for action in (lambda: c.select('zulu'), lambda: c.remove('zulu'), lambda: c.save('zulu','alias',self.settings,replace=True)):
  148              with self.assertRaises(c.Refused): action()
  149          self.assertEqual(c.CONFIG.read_bytes(), self.original)
  150  
  151      def test_busy_transfer_refuses_management(self):
  152          with c.locked():
  153              for action in (lambda: c.select('zulu'), lambda: c.remove('zulu'), lambda: c.save('alpha','alias',self.settings)):
  154                  with self.assertRaises(c.Refused): action()
  155          self.assertEqual(c.CONFIG.read_bytes(), self.original)
  156  
  157      def test_dependency_refuses_removal(self):
  158          c.CONFIG.write_bytes(self.original + b'\n[wrapped]\ntype = alias\nremote = zulu:folder\n')
  159          before = c.CONFIG.read_bytes()
  160          with self.assertRaises(c.Refused): c.remove('zulu')
  161          self.assertEqual(c.CONFIG.read_bytes(), before)
  162  
  163      def test_first_connection_and_manual_empty_selection(self):
  164          c.CONFIG.unlink()
  165          c.save('first','alias',self.settings)
  166          self.assertEqual(c.active(), 'first')
  167          c.remove('first')
  168          c.save('second','alias',self.settings)
  169          self.assertEqual(c.active(), '')
  170  
  171      def test_blank_edit_preserves_existing_values(self):
  172          before = dict(c.read_config()[1]['zulu'])
  173          c.save('zulu', 'alias', [], replace=True)
  174          self.assertEqual(dict(c.read_config()[1]['zulu']), before)
  175  
  176      def test_object_store_defaults_only_apply_to_new_connections(self):
  177          loader = importlib.machinery.SourceFileLoader('qa_cloud_remote', str(SOURCE/'cloud_remote'))
  178          spec = importlib.util.spec_from_loader(loader.name, loader)
  179          cli = importlib.util.module_from_spec(spec); loader.exec_module(cli)
  180          with mock.patch.object(cli, 'load_providers', return_value=[{'Name':'s3'}]), mock.patch.object(c, 'save') as save, mock.patch('builtins.print'):
  181              cli.cmd_create('bucket', 's3', [], replace=True)
  182              self.assertEqual(save.call_args.args[2], [])
  183              cli.cmd_create('bucket2', 's3', [], replace=False)
  184              self.assertIn(('directory_markers', 'true'), save.call_args.args[2])
  185  
  186      def test_verified_update_keeps_other_connections(self):
  187          c.save('alpha','alias',self.settings)
  188          elsewhere = self.root/'elsewhere'; elsewhere.mkdir()
  189          c.save('zulu','alias',[('remote',str(elsewhere))],replace=True)
  190          config = c.read_config()[1]
  191          self.assertEqual(config['alpha']['remote'], str(self.data))
  192          self.assertEqual(config['zulu']['remote'], str(elsewhere))
  193          self.assertEqual(c.active(), 'zulu')
  194  
  195  class OAuthOwnership(unittest.TestCase):
  196      def setUp(self):
  197          Connections.setUp(self)
  198          loader = importlib.machinery.SourceFileLoader('qa_cloud_oauth', str(SOURCE/'cloud_oauth'))
  199          spec = importlib.util.spec_from_loader(loader.name, loader)
  200          self.oauth = importlib.util.module_from_spec(spec)
  201          loader.exec_module(self.oauth)
  202          self.oauth.STATE_DIR = str(self.root/'oauth-state')
  203          self.oauth.LOG_FILE = str(self.root/'oauth.log')
  204          self.oauth.reset_state(attempt='serve-old', session='session-old', status='waiting')
  205          self.session = self.oauth.Session('alias', 'zulu', 60)
  206          self.session.attempt = 'serve-old'; self.session.gen = 'session-old'
  207          self.session.replace = True; self.session.token = '{"access_token":"synthetic-only"}'
  208  
  209      def test_real_oauth_config_create_and_renew_use_the_collected_token(self):
  210          # Only the account listing is synthetic. The packaged rclone executes
  211          # its real Dropbox configuration state machine without account access.
  212          original_run = c.run
  213          for replace in (False, True):
  214              with self.subTest(replace=replace):
  215                  name = 'zulu' if replace else 'dropbox test'
  216                  if replace:
  217                      c.CONFIG.write_text('[zulu]\ntype = dropbox\ntoken = {"access_token":"old-synthetic"}\n')
  218                  self.oauth.reset_state(attempt='serve-old', session='session-old', status='waiting')
  219                  session = self.oauth.Session('dropbox', name, 60)
  220                  session.attempt = 'serve-old'; session.gen = 'session-old'
  221                  session.replace = replace
  222                  session.token = '{"access_token":"new-synthetic"}'
  223                  listings = []
  224                  def verify(args):
  225                      if 'lsd' in args:
  226                          listings.append(args)
  227                          return ''
  228                      return original_run(args)
  229                  with mock.patch.object(c, 'run', side_effect=verify):
  230                      ok, result = session._create_remote()
  231                  self.assertTrue(ok, result)
  232                  self.assertEqual(len(listings), 1)
  233                  self.assertEqual(c.read_config()[1][name]['token'], session.token)
  234                  self.assertEqual(self.oauth.read_state()['status'], 'signed-in')
  235  
  236      def test_normal_shutdown_waits_for_http_worker_staging_cleanup(self):
  237          import threading
  238          original_run = c.run
  239          entered, release = threading.Event(), threading.Event()
  240          holder = self.oauth.SessionHolder('alias', 'zulu', 'QA', 60)
  241          holder.session = self.session
  242          def blocked(args):
  243              entered.set()
  244              self.assertTrue(release.wait(2))
  245              return original_run(args)
  246          with mock.patch.object(c, 'run', side_effect=blocked):
  247              worker = threading.Thread(target=self.session._create_remote)
  248              worker.start()
  249              self.assertTrue(entered.wait(2))
  250              timer = threading.Timer(.05, release.set)
  251              timer.start()
  252              try:
  253                  holder.end()
  254                  self.assertFalse(list(self.root.glob('.connection-*')))
  255                  self.assertEqual(c.CONFIG.read_bytes(), self.original)
  256              finally:
  257                  release.set(); worker.join(2); timer.join(2)
  258  
  259      def test_cancel_between_configuration_and_listing_cleans_staging(self):
  260          original_run = c.run
  261          def cancelled_after_create(args):
  262              result = original_run(args)
  263              self.session.superseded = True
  264              return result
  265          with mock.patch.object(c, 'run', side_effect=cancelled_after_create) as run:
  266              ok, _ = self.session._create_remote()
  267          self.assertFalse(ok)
  268          self.assertEqual(run.call_count, 1)
  269          self.assertEqual(c.CONFIG.read_bytes(), self.original)
  270          self.assertFalse(list(self.root.glob('.connection-*')))
  271  
  272      def test_unanswered_provider_question_still_refuses_publication(self):
  273          with mock.patch.object(c, 'run', return_value='{"State":"provider-question"}') as run:
  274              with self.assertRaises(c.Refused):
  275                  c.save('new', 'alias', self.settings)
  276          self.assertEqual(run.call_count, 1)
  277          self.assertEqual(c.CONFIG.read_bytes(), self.original)
  278          self.assertFalse(list(self.root.glob('.connection-*')))
  279  
  280      def test_superseded_session_cannot_replace_credentials(self):
  281          self.oauth.write_state(session='session-new')
  282          ok, _ = self.session._create_remote()
  283          self.assertFalse(ok)
  284          self.assertEqual(c.CONFIG.read_bytes(), self.original)
  285          self.assertEqual(self.oauth.read_state()['session'], 'session-new')
  286  
  287      def test_cancel_during_verification_prevents_commit(self):
  288          original_run = c.run
  289          def cancel_during_listing(args):
  290              result = original_run(args)
  291              if 'lsd' in args: self.oauth.write_state(status='idle')
  292              return result
  293          with mock.patch.object(c, 'run', side_effect=cancel_during_listing):
  294              ok, _ = self.session._create_remote()
  295          self.assertFalse(ok)
  296          self.assertEqual(c.CONFIG.read_bytes(), self.original)
  297          self.assertEqual(self.oauth.read_state()['status'], 'idle')
  298  
  299      def test_success_publishes_matching_connection_and_state(self):
  300          ok, name = self.session._create_remote()
  301          self.assertTrue(ok, name)
  302          self.assertEqual(name, 'zulu')
  303          self.assertEqual(self.oauth.read_state()['status'], 'signed-in')
  304          self.assertEqual(self.oauth.read_state()['remote'], 'zulu')
  305          self.assertEqual(c.read_config()[1]['zulu']['token'], self.session.token)
  306  
  307  if __name__ == '__main__': unittest.main(verbosity=2)
```

## File: tools/cloud-input-test (at 8ebaf8daad, 132 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Full wifictl with synthetic NetworkManager; actual phone JS under delayed HTTP."""
    5  from pathlib import Path
    6  import json, os, re, subprocess, sys, tempfile, unittest
    7  ROOT=Path(__file__).resolve().parents[1]
    8  WIFI=ROOT/'projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl'
    9  OAUTH=ROOT/'projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'
   10  
   11  class Wifi(unittest.TestCase):
   12   def setUp(self):
   13    self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
   14    self.root=Path(self.temp.name);(self.root/'shim').mkdir();(self.root/'run').mkdir()
   15    (self.root/'profile').write_text('get_setting() { case "$1" in wifi.key) echo OLD_FIXTURE_KEY;; wifi.adhoc.enabled) echo 0;; esac; }\n')
   16    shim=self.root/'shim'
   17    (shim/'nmcli').write_text('''#!/usr/bin/python3
   18  import sys,json
   19  from pathlib import Path
   20  a=sys.argv[1:]
   21  with open('/run/calls','a') as f:f.write(json.dumps(a)+'\\n')
   22  if Path('/run/fail').exists():sys.exit(1)
   23  if 'SSID,SECURITY' in a: print(Path('/run/scan').read_text(),end='')
   24  elif 'NAME,TYPE,ACTIVE' in a: print(Path('/run/profiles').read_text(),end='')
   25  elif '802-11-wireless.ssid' in a: print(Path('/run/saved-ssid').read_text(),end='')
   26  elif 'DEVICE,STATE' in a: print('wlan0:disconnected')
   27  ''')
   28    (shim/'iwctl').write_text('#!/bin/sh\necho wlan0\n')
   29    for name in ('sleep','iw'): (shim/name).write_text('#!/bin/sh\nexit 0\n')
   30    for p in shim.iterdir():p.chmod(0o755)
   31    for name in ('scan','profiles','saved-ssid','calls'):(self.root/'run'/name).write_text('')
   32   def call(self,*args):
   33    result = subprocess.run(['bwrap','--ro-bind','/','/','--dev','/dev','--tmpfs','/sys','--dir','/sys/class/net/wlan0','--ro-bind',str(self.root/'profile'),'/etc/profile','--ro-bind',str(self.root/'shim'),str(self.root/'shim'),'--bind',str(self.root/'run'),'/run','--setenv','PATH',str(self.root/'shim')+':/usr/bin:/bin','bash',str(WIFI),*args],text=True,capture_output=True)
   34    self.assertEqual(result.stderr, '', 'fixture or script emitted an unexpected error')
   35    return result
   36   def scan(self,*rows): (self.root/'run/scan').write_text('\n'.join(rows)+'\n')
   37   def calls(self):return [json.loads(x) for x in (self.root/'run/calls').read_text().splitlines()]
   38   def test_open_escaped_name_connects_without_key_or_delete(self):
   39    name='Cafe: \\Guest';self.scan('Cafe\\: \\\\Guest:')
   40    r=self.call('security',name);self.assertEqual((r.returncode,r.stdout),(0,'open\n'),r.stderr)
   41    r=self.call('connect-open',name);self.assertEqual(r.returncode,0,r.stderr)
   42    args=next(a for a in self.calls() if 'connect' in a)
   43    self.assertIn(name,args);self.assertNotIn('password',args)
   44    self.assertFalse(any('delete' in a for a in self.calls()))
   45   def test_protected_and_unknown_do_not_connect_open(self):
   46    for value in ('WPA2','WEP','OWE','802.1X','unexpected'):
   47     self.scan('Public:'+value)
   48     self.assertNotEqual(self.call('security','Public').stdout,'open\n')
   49     self.assertNotEqual(self.call('connect-open','Public').returncode,0)
   50    self.assertFalse(any('connect' in a for a in self.calls()))
   51   def test_mixed_and_absent_fail_closed(self):
   52    self.scan('Public:','Public:WPA2')
   53    self.assertEqual(self.call('security','Public').stdout,'unknown\n')
   54    self.assertNotEqual(self.call('connect-open','Public').returncode,0)
   55    self.assertNotEqual(self.call('connect-open','Missing').returncode,0)
   56   def test_service_failure_does_not_connect(self):
   57    self.scan('Public:');(self.root/'run/fail').touch()
   58    self.assertNotEqual(self.call('connect-open','Public').returncode,0)
   59    self.assertFalse(any('connect' in a for a in self.calls()))
   60   def test_renamed_saved_profile_is_preserved(self):
   61    self.scan('Public:');(self.root/'run/profiles').write_text('Personal Name:802-11-wireless:no\n');(self.root/'run/saved-ssid').write_text('Public\n')
   62    self.assertNotEqual(self.call('connect-open','Public').returncode,0)
   63    self.assertFalse(any('connect' in a or 'delete' in a for a in self.calls()))
   64   def test_explicit_empty_key_never_borrows_old_key(self):
   65    self.scan('Public:')
   66    r=self.call('connect','Public','','US')
   67    self.assertEqual(r.returncode,0)
   68    self.assertTrue(self.calls())
   69    self.assertFalse(any('OLD_FIXTURE_KEY' in x for a in self.calls() for x in a))
   70  
   71  class Phone(unittest.TestCase):
   72   def program(self,source):
   73    # Evaluate unchanged production functions, with controllably delayed fetch.
   74    start=source.index('  var queue = Promise.resolve();')
   75    end=source.index('  // Two different strings,',start)
   76    send=source[start:end]
   77    a=source.index('  // Movement is coalesced, not queued.') if '  // Movement is coalesced, not queued.' in source else source.index('  // Coalesce only adjacent, unsent moves')
   78    b=source.index('  function down(e)',a)
   79    move=source[a:b]
   80    a=source.index('  function up(e)');b=source.index('  pad.addEventListener',a)
   81    up=source[a:b]
   82    return '''var pin='1234', events=[], waiting=[];
   83  var tracking=true,moved=0,pad={classList:{remove:function(){}}};
   84  function fetch(url,opts) {events.push(opts.body.split('&')[0]);return new Promise(function(resolve){waiting.push(resolve);});}
   85  '''+send+move+up+'''
   86  (async function(){
   87   pushMove(3,0); await Promise.resolve();
   88   pushMove(2,0); up({preventDefault:function(){}});
   89   await new Promise(r=>setTimeout(r,100));
   90   if(events.length!==1)throw Error('click overtook unfinished movement: '+events);
   91   waiting.shift()(); await new Promise(r=>setImmediate(r));
   92   if(events[1]!=='move=2,0')throw Error('pending movement lost: '+events);
   93   waiting.shift()(); await new Promise(r=>setImmediate(r));
   94   if(events[2]!=='click=1')throw Error('tap missing or out of order: '+events);
   95   waiting.shift()(); await new Promise(r=>setImmediate(r));
   96   console.log('PASS delayed movement arrives before tap');
   97  })().catch(e=>{console.error(e.message);process.exitCode=1;});
   98  '''
   99   def test_delayed_movement_and_click(self):
  100    result=subprocess.run(['node','-e',self.program(OAUTH.read_text())],text=True,capture_output=True)
  101    self.assertEqual(result.returncode,0,result.stderr)
  102   def test_drag_moves_without_click_and_keys_stay_ordered(self):
  103    source=OAUTH.read_text()
  104    queue=source[source.index('  var queue = Promise.resolve();'):source.index('  // Two different strings,')]
  105    movement=source[source.index('  var px = 0, py = 0, moved = 0, tracking = false;'):source.index('  pad.addEventListener')]
  106    program="""var pin='1234', events=[], waiting=[], pad={classList:{add:function(){},remove:function(){}}};
  107  function fetch(url,opts) {events.push(opts.body.split('&')[0]);return new Promise(resolve=>waiting.push(resolve));}
  108  """+queue+movement+"""
  109  (async function(){
  110   const event=(x,y)=>({clientX:x,clientY:y,preventDefault:function(){}});
  111   down(event(0,0));move(event(20,10));await Promise.resolve();
  112   move(event(35,20));up(event(35,20));send('key=tab');
  113   down(event(0,0));up(event(0,0));
  114   if(events.join('|')!=='move=20,10')throw Error('drag sent a click or overtook motion');
  115   const expected=['move=20,10','move=15,10','key=tab','click=1'];
  116   for(let n=0;n<4;n++) {
  117    if(events[n]!==expected[n])throw Error('event ordering: '+events);
  118    waiting.shift()();await new Promise(r=>setImmediate(r));
  119   }
  120   if(events.length!==4)throw Error('drag produced unexpected events: '+events);
  121   console.log('PASS drag has no click and later key/tap preserve order');
  122  })().catch(e=>{console.error(e.message);process.exitCode=1;});
  123  """
  124    result=subprocess.run(['node','-e',program],text=True,capture_output=True)
  125    self.assertEqual(result.returncode,0,result.stderr)
  126   def test_original_source_negative_control(self):
  127    old=subprocess.check_output(['git','show','a1b0c65165:projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'],cwd=ROOT,text=True)
  128    result=subprocess.run(['node','-e',self.program(old)],text=True,capture_output=True)
  129    self.assertNotEqual(result.returncode,0)
  130    self.assertIn('click overtook',result.stderr)
  131  
  132  if __name__=='__main__': unittest.main(verbosity=2)
```

## File: tools/cloud-pair-migration (at 8ebaf8daad, 243 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # cloud-pair-migration -- the mixed-installation test (D-CLOUD-158's gate,
    6  # #354's fifth phase) on tools/vm-pair: one QA cloud, a device updated in
    7  # place from the previous build and a fresh install of the new one.
    8  #
    9  #   ./tools/cloud-pair-migration <previous img.gz> <new img.gz> <new tar>
   10  #
   11  # Guest a boots the previous image, whose default cloud folder is an earlier
   12  # one this project shipped (/ROCKNIX); guest b is a fresh install of the new
   13  # image. Both share the QA WebDAV (tools/cloud-test-backend), which is reset
   14  # first. Every step is the shipped scripts over ssh -- the commands the
   15  # interface's pages run -- and every check is read from the cloud, the conf
   16  # or the file itself:
   17  #
   18  #   1. a (previous build) backs up a save and its settings to the earlier
   19  #      folder; the cloud also holds a ROM there.
   20  #   2. b (fresh) is set up as the wizard sets it up: the cloud folder
   21  #      step's scan (cloud_scan --folder, D-CLOUD-170) joins the earlier
   22  #      folder rather than leaving b on an empty /pixelelated beside it and
   23  #      reads the state that asks MOVE (not CREATE IT); the player's NOT NOW
   24  #      runs nothing; the seeding (cloud_setup --seed-folders) makes nothing
   25  #      at /pixelelated; b's restore brings a's save; and --needs-step says
   26  #      the step comes again at b's next boot.
   27  #   3. a is updated in place through /storage/.update: the new BUILD_ID, and
   28  #      its conf still on the earlier folder (the configured root wins).
   29  #   4. a's scan reads the move; MOVE (cloud_migrate_layout --apply) copies,
   30  #      verifies and only then removes, unit by unit in its own log; the
   31  #      cloud then holds /pixelelated whole with its marker and nothing under
   32  #      the earlier saves folder, and a's conf points at /pixelelated.
   33  #   5. b's step at its next boot follows (its old folder is empty now): the
   34  #      scan re-points it with no question, --needs-step then says no step;
   35  #      its new save lands at /pixelelated and a's restore brings it.
   36  #   5m. A device that missed its step (b's pointers set back by hand, a
   37  #      staged input): its backup does not re-make the earlier folder the
   38  #      move removed -- it sends nothing and offers the folder (D-CLOUD-172)
   39  #      -- and its next step follows the fleet with no question, after which
   40  #      its save goes up to /pixelelated.
   41  #   5n. A device on an older build that kept writing to the earlier folder
   42  #      after the move (stood in by a save put there directly, named): its
   43  #      step asks MOVE and the move merges into /pixelelated (D-CLOUD-168):
   44  #      every save there, a's untouched, nothing left behind.
   45  #   6. Both confs read the shipped /pixelelated folders.
   46  #   7. A provider error is not an absence: b pointed at a dead endpoint --
   47  #      its scan ends non-zero with no state written, and nothing in its conf
   48  #      moves.
   49  #
   50  # Exit 0 when every check passed, 1 when one failed, 2 when the test could
   51  # not run (a pair already up: another run owns the QA cloud -- one writer
   52  # per QA cloud folder). The log and an rc file go to
   53  # /workspace/artifacts/rocknix-images/qa-<new id>-pair-migration-from-<old id>-<date>/.
   54  # The pair is taken down at the end; --keep leaves it up.
   55  set -u
   56  HERE=$(cd "$(dirname "$0")" && pwd)
   57  ROOT=$(cd "$HERE/.." && pwd)
   58  # Historical migration proof only (D-CLOUD-175/#508). Refuse before
   59  # creating guests, changing their state or resetting a synthetic backend.
   60  if [ ! -f "${ROOT}/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout" ]; then
   61    echo 'This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manual cloud setup.' >&2
   62    exit 2
   63  fi
   64  KEEP=0
   65  [ "${1:-}" = "--keep" ] && { KEEP=1; shift; }
   66  OLD=${1:-}; NEW=${2:-}; TAR=${3:-}
   67  for f in "$OLD" "$NEW" "$TAR"; do
   68    [ -n "$f" ] && [ -f "$f" ] || { sed -n '2,54p' "$0" | sed 's/^# \{0,1\}//'; echo "cloud-pair-migration: no such file: '$f'" >&2; exit 2; }
   69  done
   70  VP="$HERE/vm-pair"; BE="$HERE/cloud-test-backend"
   71  
   72  # A pair that is already up belongs to another run (vm-qa, the rehearsal),
   73  # and this test resets the QA cloud under it.
   74  alive=0
   75  for p in $("$VP" info 2>/dev/null | grep -o 'pid [0-9][0-9]*' | awk '{print $2}'); do kill -0 "$p" 2>/dev/null && alive=1; done
   76  [ "$alive" = 0 ] || { echo "cloud-pair-migration: a guest pair is already up -- another run owns the QA cloud; not starting" >&2; exit 2; }
   77  
   78  idof() { basename "$(dirname "$1")" | grep -oE '[0-9a-f]{10}$' || echo unknown; }
   79  OUT=/workspace/artifacts/rocknix-images/qa-$(idof "$NEW")-pair-migration-from-$(idof "$OLD")-$(date -u +%Y%m%d-%H%M)
   80  mkdir -p "$OUT"; LOG=$OUT/pair-migration.log; : > "$LOG"
   81  say() { echo "=== $(date -u '+%H:%M:%S') $*" | tee -a "$LOG"; }
   82  PASSES=0; FAILS=0
   83  check() { # <0|nonzero> <what> [detail on failure]
   84    if [ "$1" = 0 ]; then echo "PASS $2" | tee -a "$LOG"; PASSES=$((PASSES + 1))
   85    else echo "FAIL $2${3:+ -- $3}" | tee -a "$LOG"; FAILS=$((FAILS + 1)); fi
   86  }
   87  # A guest's output goes to the log through the read filter: a conf or a
   88  # script's line can carry a sign-in (engineering-practices.md, D-QA-021).
   89  mask() { grep -v -i -E 'key|pass|token|user|psk'; }
   90  on() { local g="$1"; shift; "$VP" ssh "$g" ". /etc/profile >/dev/null 2>&1; $*"; }
   91  ptrs() { on "$1" "for k in SAVES_REMOTE SETTINGS_REMOTE CONTENT_REMOTE; do sed -n \"s/^\$k=\\\"\\(.*\\)\\\"\$/\\1/p\" /storage/.config/cloud_sync.conf | head -1; done | tr '\\n' ' '" 2>/dev/null | sed 's/ $//'; }
   92  cloud_files() { "$BE" ls "$1" 2>/dev/null | awk '{print $2}' | tr '\n' ' '; }
   93  finish() {
   94    say "RESULT $([ "$FAILS" = 0 ] && echo PASS || echo FAIL): $PASSES passed, $FAILS failed (log $LOG)"
   95    [ "$KEEP" = 1 ] || "$VP" down >>"$LOG" 2>&1
   96    local rc=$(( FAILS == 0 ? 0 : 1 )); [ -n "${1:-}" ] && rc=$1
   97    echo "$rc" > "$OUT/rc"; exit "$rc"
   98  }
   99  
  100  # The shipped folders, from the tree's defaults (blindspot 71: never a literal).
  101  CUR_SAVES=$("$BE" shipped-default SAVES_REMOTE) || { echo "no shipped saves default" >&2; exit 2; }
  102  CUR_BACKUPS=$("$BE" shipped-default SETTINGS_REMOTE) || exit 2
  103  CUR_CONTENT=$("$BE" shipped-default CONTENT_REMOTE) || exit 2
  104  CUR_ROOT="${CUR_SAVES%/*}"
  105  
  106  say "backend: $("$BE" status 2>&1 | head -1)"; "$BE" up >>"$LOG" 2>&1 || true
  107  "$BE" reset >>"$LOG" 2>&1
  108  say "pair up from $(basename "$OLD"), then b rebuilt from $(basename "$NEW")"
  109  "$VP" up "$OLD" >>"$LOG" 2>&1 || { say "vm-pair up FAILED"; finish 2; }
  110  "$VP" reimage b "$NEW" >>"$LOG" 2>&1 || { say "vm-pair reimage b FAILED"; finish 2; }
  111  BID_A0=$(on a 'grep ^BUILD_ID= /etc/os-release | cut -d\" -f2'); BID_NEW=$(on b 'grep ^BUILD_ID= /etc/os-release | cut -d\" -f2')
  112  say "a on ${BID_A0:0:10} (previous), b on ${BID_NEW:0:10} (new)"
  113  [ -n "$BID_A0" ] && [ -n "$BID_NEW" ] && [ "$BID_A0" != "$BID_NEW" ]; check $? "the two guests run two different builds" "a '${BID_A0}' b '${BID_NEW}'"
  114  
  115  say "the QA remote on both; the automatic syncs off, so only the steps below write"
  116  CONF=$("$BE" rclone-conf)
  117  for g in a b; do
  118    on "$g" "mkdir -p /storage/.config/rclone /storage/roms/nes; cat > /storage/.config/rclone/rclone.conf <<'RC'
  119  $CONF
  120  RC
  121  chmod 600 /storage/.config/rclone/rclone.conf; /usr/bin/cloud_sync_helper >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; true" >>"$LOG" 2>&1
  122  done
  123  A_PTRS0=$(ptrs a); B_PTRS0=$(ptrs b)
  124  EARLY_SAVES=${A_PTRS0%% *}; EARLY_ROOT="${EARLY_SAVES%/*}"
  125  say "a's folders: $A_PTRS0   b's folders: $B_PTRS0"
  126  on b "/usr/bin/cloud_migrate_layout --superseded" 2>/dev/null | grep -qFx -- "$EARLY_SAVES"
  127  check $? "the previous build's default ($EARLY_SAVES) is one the new build lists as superseded -- the premise of this test"
  128  [ "$B_PTRS0" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ]; check $? "the fresh install starts on the shipped folders" "$B_PTRS0"
  129  
  130  say "1. a (previous build) backs up a save and its settings to $EARLY_ROOT; a ROM is put there too"
  131  on a 'head -c 4000 /dev/urandom > /storage/roms/nes/FromA.srm; /usr/bin/cloud_backup --yes --method=copy --update --saves-only >/dev/null 2>&1; echo "saves backup rc=$?"; /usr/bin/backuptool backup >/dev/null 2>&1; /usr/bin/cloud_backup --yes --system-only >/dev/null 2>&1; echo "settings backup rc=$?"' 2>&1 | mask | tee -a "$LOG"
  132  SUM_A=$(on a 'sha256sum /storage/roms/nes/FromA.srm | cut -c1-64')
  133  ROMD=$(mktemp -d); mkdir -p "$ROMD/ROMs/nes"; head -c 50000 /dev/urandom > "$ROMD/ROMs/nes/Pair.nes"
  134  "$BE" put "$ROMD" "${EARLY_ROOT#/}/Content" >>"$LOG" 2>&1; rm -rf "$ROMD"
  135  cloud_files "${EARLY_SAVES#/}" | grep -q 'nes/FromA.srm'; check $? "1: a's save is in ${EARLY_SAVES}" "$(cloud_files "${EARLY_SAVES#/}")"
  136  cloud_files "${EARLY_ROOT#/}/Backups" | grep -q '_SETTINGS.tar.gz'; check $? "1: a's settings backup is in ${EARLY_ROOT}/Backups" "$(cloud_files "${EARLY_ROOT#/}/Backups")"
  137  
  138  say "2. b (fresh) is set up as the wizard does it: the cloud folder step's scan, NOT NOW, then --seed-folders"
  139  on b '/usr/bin/cloud_scan --folder >/dev/null 2>&1; echo "folder scan rc=$?"' 2>&1 | tee -a "$LOG"
  140  B_STATE=$(on b 'cat /storage/.cache/cloud_sync/scan/state 2>/dev/null' | mask | tr '\n' ' ')
  141  echo "$B_STATE" | grep -q 'STATE=superseded-with-files' && echo "$B_STATE" | grep -q "SOURCE=$EARLY_SAVES"; check $? "2: the wizard's folder step reads the move from ${EARLY_SAVES}, not CREATE IT (D-CLOUD-170)" "$B_STATE"
  142  on b '/usr/bin/cloud_setup --seed-folders; echo "seed rc=$?"' 2>&1 | mask | tee -a "$LOG"
  143  B_PTRS1=$(ptrs b)
  144  [ "$B_PTRS1" = "$EARLY_SAVES $EARLY_ROOT/Backups $EARLY_ROOT/Content" ]; check $? "2: the fresh install joined the folder the saves are in, with its backups and content (D-CLOUD-158)" "b's folders: $B_PTRS1"
  145  [ -z "$(cloud_files "${CUR_ROOT#/}")" ]; check $? "2: nothing was made at ${CUR_ROOT} beside them" "$(cloud_files "${CUR_ROOT#/}")"
  146  on b '/usr/bin/cloud_restore --yes --method=copy --update --saves-only >/dev/null 2>&1; echo "restore rc=$?"' 2>&1 | tee -a "$LOG"
  147  [ -n "$SUM_A" ] && [ "$(on b 'sha256sum /storage/roms/nes/FromA.srm 2>/dev/null | cut -c1-64')" = "$SUM_A" ]; check $? "2: b's restore brought a's save, byte for byte"
  148  B_NEED=$(on b '/usr/bin/cloud_migrate_layout --needs-step >/dev/null 2>&1; echo $?')
  149  [ "$B_NEED" = 0 ]; check $? "2: and the step comes again at b's next boot (--needs-step 0)" "--needs-step said '${B_NEED}'"
  150  
  151  say "3. a is updated in place to $(basename "$TAR")"
  152  "$VP" scp a "$TAR" /storage/.update/ >>"$LOG" 2>&1 || say "scp FAILED"
  153  BOOT0=$(on a 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null)
  154  on a 'sync; reboot' >/dev/null 2>&1
  155  BID_A1=""
  156  for _ in $(seq 1 60); do
  157    B=$(on a 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null)
  158    if [ -n "$B" ] && [ "$B" != "$BOOT0" ]; then BID_A1=$(on a 'grep ^BUILD_ID= /etc/os-release | cut -d\" -f2' 2>/dev/null); [ "$BID_A1" = "$BID_NEW" ] && break; fi
  159    sleep 5
  160  done
  161  [ "$BID_A1" = "$BID_NEW" ]; check $? "3: a runs the new build after the update" "a reads '${BID_A1}'"
  162  [ "$(ptrs a)" = "$A_PTRS0" ]; check $? "3: a's conf still names the folder it was set to (the configured root wins on update)" "$(ptrs a)"
  163  
  164  say "4. a's scan, then MOVE"
  165  on a '/usr/bin/cloud_scan >/dev/null 2>&1; echo "scan rc=$?"' 2>&1 | tee -a "$LOG"
  166  on a 'cat /storage/.cache/cloud_sync/scan/state 2>/dev/null' | mask | tr '\n' ' ' | grep -q 'STATE=superseded-with-files'; check $? "4: a's scan reads the move"
  167  on a '/usr/bin/cloud_migrate_layout --apply > /tmp/pair-move.out 2>&1; echo "move rc=$?"' 2>&1 | tee -a "$LOG"
  168  MOVE=$(on a 'cat /tmp/pair-move.out' | mask); printf '%s\n' "$MOVE" | grep -E '^>>> (unit|doing)' >> "$LOG"
  169  # Unit by unit, the remove never comes before that unit's copy and verify.
  170  ORDER=$(printf '%s\n' "$MOVE" | awk '
  171    /^>>> unit /     { u = $0; c = 0; v = 0; next }
  172    /^>>> doing copy/   { c = 1; next }
  173    /^>>> doing verify/ { if (!c) bad = bad "verify before copy in " u "; "; v = 1; next }
  174    /^>>> doing remove/ { removes++; if (!c || !v) bad = bad "remove before copy and verify in " u "; "; next }
  175    END { if (removes == 0) bad = bad "no remove at all; "; printf "%s", bad }')
  176  [ -z "$ORDER" ]; check $? "4: each unit was copied and verified before anything of it was removed" "$ORDER"
  177  cloud_files "${CUR_SAVES#/}" | grep -q 'nes/FromA.srm'; check $? "4: the saves are at ${CUR_SAVES}" "$(cloud_files "${CUR_SAVES#/}")"
  178  cloud_files "${CUR_BACKUPS#/}" | grep -q '_SETTINGS.tar.gz'; check $? "4: the settings backups are at ${CUR_BACKUPS}"
  179  cloud_files "${CUR_CONTENT#/}" | grep -q 'ROMs/nes/Pair.nes'; check $? "4: the ROM is at ${CUR_CONTENT}"
  180  [ "$("$BE" cat "${CUR_ROOT#/}/.layout" 2>/dev/null | head -1)" = "layout=2" ]; check $? "4: the fleet's marker is at ${CUR_ROOT}"
  181  [ -z "$(cloud_files "${EARLY_SAVES#/}")" ]; check $? "4: nothing is left under ${EARLY_SAVES}" "$(cloud_files "${EARLY_SAVES#/}")"
  182  [ "$(ptrs a)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ]; check $? "4: a's conf points at the current folders" "$(ptrs a)"
  183  
  184  say "5. b's step at its next boot follows the fleet; its new save goes up; a restores it"
  185  on b '/usr/bin/cloud_scan --folder >/dev/null 2>&1; echo "folder scan rc=$?"' 2>&1 | tee -a "$LOG"
  186  [ "$(ptrs b)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ]; check $? "5: b's step followed: its conf points at the current folders" "$(ptrs b)"
  187  on b 'journalctl -b -t cloud_migrate_layout 2>/dev/null | grep -q "followed the fleet"'; check $? "5: and its journal says so, with no question asked (D-CLOUD-160)"
  188  on b 'grep -qx "STATE=current" /storage/.cache/cloud_sync/scan/state'; check $? "5: the step's scan then reads the current folder, so it goes straight on"
  189  B_NEED=$(on b '/usr/bin/cloud_migrate_layout --needs-step >/dev/null 2>&1; echo $?')
  190  [ "$B_NEED" = 1 ]; check $? "5: settled: no step at b's next boot (--needs-step 1)" "--needs-step said '${B_NEED}'"
  191  on b 'head -c 3000 /dev/urandom > /storage/roms/nes/FromB.srm; /usr/bin/cloud_backup --yes --method=copy --update --saves-only >/dev/null 2>&1; echo "backup rc=$?"' 2>&1 | tee -a "$LOG"
  192  SUM_B=$(on b 'sha256sum /storage/roms/nes/FromB.srm | cut -c1-64')
  193  cloud_files "${CUR_SAVES#/}" | grep -q 'nes/FromB.srm'; check $? "5: b's new save is at ${CUR_SAVES}" "$(cloud_files "${CUR_SAVES#/}")"
  194  [ -z "$(cloud_files "${EARLY_SAVES#/}")" ]; check $? "5: and nothing was written back under ${EARLY_SAVES}" "$(cloud_files "${EARLY_SAVES#/}")"
  195  on a '/usr/bin/cloud_restore --yes --method=copy --update --saves-only >/dev/null 2>&1; echo "restore rc=$?"' 2>&1 | tee -a "$LOG"
  196  [ -n "$SUM_B" ] && [ "$(on a 'sha256sum /storage/roms/nes/FromB.srm 2>/dev/null | cut -c1-64')" = "$SUM_B" ]; check $? "5: a's restore brought b's save, byte for byte"
  197  
  198  say "5m. a device that missed its step: b's pointers set back by hand (staged); its backup re-makes nothing; its step follows"
  199  read -r E_SAVES E_BACKUPS E_CONTENT <<< "$A_PTRS0"
  200  set_early() { on b "sed -i -e 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"$E_SAVES\"|' -e 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE=\"$E_BACKUPS\"|' -e 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE=\"$E_CONTENT\"|' /storage/.config/cloud_sync.conf" >>"$LOG" 2>&1; }
  201  set_early
  202  [ "$(ptrs b)" = "$A_PTRS0" ]; check $? "5m: (staged) b's pointers are back on ${EARLY_ROOT}, as on a device that never ran its step" "$(ptrs b)"
  203  on b 'head -c 2000 /dev/urandom > /storage/roms/nes/FromB2.srm; /usr/bin/cloud_backup --yes --method=copy --update --saves-only > /tmp/pair-5m.out 2>&1; echo "backup rc=$?"' 2>&1 | tee -a "$LOG" > "$OUT/5m-rc.txt"
  204  SUM_B2=$(on b 'sha256sum /storage/roms/nes/FromB2.srm | cut -c1-64')
  205  grep -qx 'backup rc=0' "$OUT/5m-rc.txt" && [ -z "$(cloud_files "${EARLY_SAVES#/}")" ] && on b "grep -qx '>>> offer create-saves-folder|${EARLY_SAVES}' /tmp/pair-5m.out"; check $? "5m: its backup made no ${EARLY_SAVES} again, sent nothing and offered the folder (D-CLOUD-172)" "$(cat "$OUT/5m-rc.txt"); ${EARLY_SAVES}: $(cloud_files "${EARLY_SAVES#/}")"
  206  on b '/usr/bin/cloud_scan --folder >/dev/null 2>&1; echo "folder scan rc=$?"' 2>&1 | tee -a "$LOG"
  207  [ "$(ptrs b)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ] && on b 'grep -qx "STATE=current" /storage/.cache/cloud_sync/scan/state'; check $? "5m: its step's scan followed the fleet with no question" "$(ptrs b)"
  208  on b '/usr/bin/cloud_backup --yes --method=copy --update --saves-only >/dev/null 2>&1; echo "backup rc=$?"' 2>&1 | tee -a "$LOG"
  209  [ "$("$BE" cat "${CUR_SAVES#/}/nes/FromB2.srm" 2>/dev/null | sha256sum | cut -c1-64)" = "$SUM_B2" ]; check $? "5m: and its next backup sent the save to ${CUR_SAVES}, byte for byte" "$(cloud_files "${CUR_SAVES#/}")"
  210  
  211  say "5n. a device on an older build that kept writing to ${EARLY_ROOT} after the move (stood in: a save put there directly); its step's MOVE merges"
  212  STAND=$(mktemp -d); mkdir -p "$STAND/nes"; head -c 1500 /dev/urandom > "$STAND/nes/FromOld.srm"; SUM_OLD=$(sha256sum "$STAND/nes/FromOld.srm" | cut -c1-64)
  213  "$BE" put "$STAND" "${EARLY_SAVES#/}" >>"$LOG" 2>&1; rm -rf "$STAND"
  214  cloud_files "${EARLY_SAVES#/}" | grep -q 'nes/FromOld.srm'; check $? "5n: (stood in) ${EARLY_SAVES} holds a save an older build wrote after the move" "$(cloud_files "${EARLY_SAVES#/}")"
  215  set_early
  216  on b '/usr/bin/cloud_scan --folder >/dev/null 2>&1; echo "folder scan rc=$?"' 2>&1 | tee -a "$LOG"
  217  B_STATE=$(on b 'cat /storage/.cache/cloud_sync/scan/state 2>/dev/null' | mask | tr '\n' ' ')
  218  echo "$B_STATE" | grep -q 'STATE=superseded-with-files' && echo "$B_STATE" | grep -q 'CURRENT_EXISTS=1'; check $? "5n: its step's scan reads the move with the fleet's folder already there, so the step asks MOVE" "$B_STATE"
  219  on b '/usr/bin/cloud_migrate_layout --apply > /tmp/pair-merge.out 2>&1; echo "merge rc=$?"' 2>&1 | tee -a "$LOG" > "$OUT/merge-rc.txt"
  220  on b 'cat /tmp/pair-merge.out' | mask | grep -E '^>>> |differ|shelv' >> "$LOG"
  221  grep -qx 'merge rc=0' "$OUT/merge-rc.txt"; check $? "5n: MOVE onto the fleet's folder ends 0" "$(cat "$OUT/merge-rc.txt")"
  222  CUR_LIST=$(cloud_files "${CUR_SAVES#/}")
  223  echo "$CUR_LIST" | grep -q 'nes/FromOld.srm' && echo "$CUR_LIST" | grep -q 'nes/FromB2.srm' && echo "$CUR_LIST" | grep -q 'nes/FromA.srm'; check $? "5n: every save is at ${CUR_SAVES}: a's, b's, and the one the older build wrote" "$CUR_LIST"
  224  [ "$("$BE" cat "${CUR_SAVES#/}/nes/FromA.srm" 2>/dev/null | sha256sum | cut -c1-64)" = "$SUM_A" ] && [ "$("$BE" cat "${CUR_SAVES#/}/nes/FromOld.srm" 2>/dev/null | sha256sum | cut -c1-64)" = "$SUM_OLD" ]; check $? "5n: a's save untouched by the merge, and the merged one byte for byte"
  225  [ -z "$(cloud_files "${EARLY_SAVES#/}")" ]; check $? "5n: nothing is left under ${EARLY_SAVES}" "$(cloud_files "${EARLY_SAVES#/}")"
  226  [ "$(ptrs b)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ]; check $? "5n: and b's conf points at the current folders" "$(ptrs b)"
  227  
  228  say "6. both devices on the shipped folders"
  229  [ "$(ptrs a)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ] && [ "$(ptrs b)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ]; check $? "6: both confs read ${CUR_SAVES}, ${CUR_BACKUPS} and ${CUR_CONTENT}" "a: $(ptrs a); b: $(ptrs b)"
  230  
  231  say "7. a provider error is not an absence: b against a dead endpoint"
  232  on b 'cp /storage/.config/rclone/rclone.conf /tmp/pair-rclone.conf' >/dev/null 2>&1
  233  DEAD=$("$BE" dead-conf)
  234  on b "cat > /storage/.config/rclone/rclone.conf <<'RC'
  235  $DEAD
  236  RC
  237  /usr/bin/cloud_scan >/dev/null 2>&1; echo \"scan rc=\$?\"" 2>&1 | tee -a "$LOG" > "$OUT/dead-scan.txt"
  238  grep -qE '^scan rc=[1-9][0-9]*$' "$OUT/dead-scan.txt"; check $? "7: the scan against a cloud that refuses ends non-zero" "said: $(cat "$OUT/dead-scan.txt")"
  239  [ -z "$(on b 'grep -h "^STATE=" /storage/.cache/cloud_sync/scan/state 2>/dev/null')" ]; check $? "7: and writes no state the interface could offer from"
  240  [ "$(ptrs b)" = "$CUR_SAVES $CUR_BACKUPS $CUR_CONTENT" ]; check $? "7: and nothing in b's conf moved" "$(ptrs b)"
  241  on b 'cp /tmp/pair-rclone.conf /storage/.config/rclone/rclone.conf; rm -f /tmp/pair-rclone.conf' >/dev/null 2>&1
  242  
  243  finish
```

## File: tools/cloud-save-integrity (at 8ebaf8daad, 219 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Offline save-byte verification; no network, device actions or repair (#517).
    5  
    6  Input: before.json/after.json (successful full rclone lsjson --hash-type Dropbox),
    7  ordered.json (before sorted by Path), reads.json (index/rc/bytes), payloads/0000...
    8  from a bounded, separately authorized collector. Keep this directory private.
    9  This verifier cannot prove the collector's scope or honest success receipts.
   10  Exit 0 means byte checks passed and no supported-container defect was found;
   11  raw/core-specific semantics and emulator compatibility are ALWAYS unverified.
   12  
   13  Dropbox: https://docs.dropboxapi.com/dropbox-api/docs/technical-reference/content-hash
   14  RZIP v1: libretro-common/streams/rzip_stream.c; RASTATE v1: RetroArch/tasks/task_save.c
   15  PNG: chunk CRC, IHDR, IDAT zlib and non-interlaced scanline checks only, not rendering.
   16  """
   17  import argparse
   18  import collections
   19  import hashlib
   20  import json
   21  import os
   22  from pathlib import Path
   23  import re
   24  import struct
   25  import sys
   26  import zlib
   27  
   28  LIMIT = 64 * 1024 * 1024
   29  BLOCK = 4 * 1024 * 1024
   30  PNG = b'\x89PNG\r\n\x1a\n'
   31  
   32  
   33  def require(condition, reason):
   34      if not condition:
   35          raise ValueError(reason)
   36  
   37  
   38  def dropbox_hash(data):
   39      h = hashlib.sha256()
   40      for i in range(0, len(data), BLOCK):
   41          h.update(hashlib.sha256(data[i:i + BLOCK]).digest())
   42      return h.hexdigest()
   43  
   44  
   45  def inflate(data, limit):
   46      require(0 <= limit <= LIMIT, 'decompression-bound')
   47      d = zlib.decompressobj()
   48      result = d.decompress(data, limit + 1)
   49      require(len(result) <= limit and d.eof and not d.unused_data and not d.unconsumed_tail,
   50              'incomplete-or-excess-zlib-stream')
   51      return result
   52  
   53  
   54  def rastate(data):
   55      if not data.startswith(b'RASTATE'):
   56          return 'core-payload-unverified'
   57      require(data[:8] == b'RASTATE\x01', 'unsupported-rastate-version')
   58      p, mem = 8, False
   59      while p + 8 <= len(data):
   60          tag, size = data[p:p + 4], struct.unpack_from('<I', data, p + 4)[0]
   61          p += 8
   62          require(size <= len(data) - p, 'truncated-rastate-block')
   63          if tag == b'END ':
   64              require(size == 0 and mem, 'invalid-rastate-end')
   65              # Some writers allocate trailing zero padding; it is not game state.
   66              require(not any(data[p:]), 'nonzero-rastate-tail')
   67              return 'rastate-envelope-ok-core-unverified'
   68          if tag == b'MEM ':
   69              require(size > 0 and not mem, 'invalid-rastate-mem')
   70              mem = True
   71          p += (size + 7) & ~7
   72          require(p <= len(data), 'truncated-rastate-padding')
   73      raise ValueError('missing-rastate-end')
   74  
   75  
   76  def rzip(data):
   77      require(len(data) >= 20 and data[:8] == b'#RZIPv\x01#', 'unsupported-or-truncated-rzip')
   78      chunk, total = struct.unpack_from('<IQ', data, 8)
   79      require(0 < chunk <= LIMIT and 0 < total <= LIMIT, 'rzip-size-bound')
   80      p, output = 20, bytearray()
   81      while len(output) < total:
   82          require(p + 4 <= len(data), 'missing-rzip-chunk')
   83          size = struct.unpack_from('<I', data, p)[0]
   84          p += 4
   85          require(0 < size <= len(data) - p, 'truncated-rzip-chunk')
   86          block = inflate(data[p:p + size], min(chunk, total - len(output)))
   87          require(len(block) == min(chunk, total - len(output)), 'rzip-chunk-length')
   88          output.extend(block)
   89          p += size
   90      require(p == len(data), 'rzip-trailing-data')
   91      return 'rzip-stream-ok/' + rastate(bytes(output))
   92  
   93  
   94  def png(data):
   95      require(data.startswith(PNG), 'invalid-png-signature')
   96      p, chunks, image = 8, [], bytearray()
   97      header = None
   98      while p + 12 <= len(data):
   99          size = struct.unpack_from('>I', data, p)[0]
  100          tag = data[p + 4:p + 8]
  101          require(size <= len(data) - p - 12, 'truncated-png-chunk')
  102          value = data[p + 8:p + 8 + size]
  103          crc = struct.unpack_from('>I', data, p + 8 + size)[0]
  104          require(zlib.crc32(tag + value) & 0xffffffff == crc, 'png-crc')
  105          p += size + 12
  106          if not chunks:
  107              require(tag == b'IHDR' and size == 13, 'missing-png-header')
  108              header = struct.unpack('>IIBBBBB', value)
  109          elif tag == b'IHDR':
  110              raise ValueError('duplicate-png-header')
  111          if tag == b'IDAT':
  112              require(b'IDAT' not in chunks or chunks[-1] == b'IDAT',
  113                      'nonconsecutive-png-data')
  114              image.extend(value)
  115          chunks.append(tag)
  116          if tag == b'IEND':
  117              require(size == 0 and p == len(data) and b'IDAT' in chunks, 'invalid-png-end')
  118              break
  119      require(chunks and chunks[-1] == b'IEND', 'missing-png-end')
  120      w, h, depth, color, compression, filtering, interlace = header
  121      depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8), 4: (8, 16), 6: (8, 16)}
  122      require(w > 0 and h > 0 and color in depths and depth in depths[color]
  123              and compression == 0 and filtering == 0 and interlace in (0, 1), 'invalid-png-header')
  124      if color == 3:
  125          require(b'PLTE' in chunks and chunks.index(b'PLTE') < chunks.index(b'IDAT'), 'missing-png-palette')
  126      pixels = inflate(bytes(image), LIMIT)
  127      if interlace:
  128          return 'png-crc-zlib-ok-interlaced-layout-unverified'
  129      channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
  130      row = 1 + (w * channels * depth + 7) // 8
  131      require(row * h <= LIMIT and len(pixels) == row * h, 'png-scanline-length')
  132      require(all(pixels[n] <= 4 for n in range(0, len(pixels), row)), 'png-row-filter')
  133      return 'png-crc-zlib-scanlines-ok-rendering-unverified'
  134  
  135  
  136  def structure(data, path):
  137      if data.startswith(PNG) or path.lower().endswith('.png'):
  138          return png(data)
  139      if data.startswith(b'#RZIP'):
  140          return rzip(data)
  141      if data.startswith(b'RASTATE'):
  142          return rastate(data)
  143      return 'raw-or-unsupported-structure-unverified'
  144  
  145  
  146  def inventory(rows):
  147      require(isinstance(rows, list) and 0 < len(rows) <= 4096, 'inventory-count')
  148      seen, size = {}, 0
  149      for f in rows:
  150          path = f['Path']
  151          require(isinstance(path, str) and not path.startswith('/')
  152                  and all(part not in ('', '.', '..') for part in path.split('/'))
  153                  and not any(ord(c) < 32 for c in path), 'unsafe-inventory-path')
  154          require(path not in seen and f['IsDir'] is False, 'duplicate-or-directory')
  155          require(type(f['Size']) is int and 0 <= f['Size'] <= LIMIT, 'file-size-bound')
  156          digest = f.get('Hashes', {}).get('dropbox', '')
  157          require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest), 'missing-provider-hash')
  158          require(isinstance(f.get('ID'), str) and f['ID'] and isinstance(f.get('ModTime'), str)
  159                  and f['ModTime'], 'missing-identity')
  160          seen[path] = (f['Size'], f['ModTime'], f['ID'], digest)
  161          size += f['Size']
  162      require(size <= 128 * 1024 * 1024, 'total-size-bound')
  163      return seen
  164  
  165  
  166  def verify(root):
  167      def read(name):
  168          p = root / name
  169          require(p.stat().st_size <= 8 * 1024 * 1024, 'metadata-size-bound')
  170          return json.loads(p.read_text())
  171      before, after, ordered, reads = [read(x) for x in ('before.json', 'after.json', 'ordered.json', 'reads.json')]
  172      original = inventory(before)
  173      require(original == inventory(after), 'cloud-changed-during-read')
  174      require(original == inventory(ordered) and ordered == sorted(before, key=lambda x: x['Path']),
  175              'ordered-manifest-mismatch')
  176      require(isinstance(reads, list) and len(reads) == len(ordered), 'incomplete-read-receipts')
  177      outcomes = []
  178      for i, (entry, receipt) in enumerate(zip(ordered, reads)):
  179          row = {'index': i, 'bytes': entry['Size'], 'playability': 'unverified'}
  180          try:
  181              require(receipt['index'] == i and receipt['rc'] == 0, 'read-failed')
  182              p = root / 'payloads' / f'{i:04d}'
  183              require(not p.is_symlink() and p.is_file() and p.stat().st_size <= LIMIT, 'missing-or-invalid-payload')
  184              data = p.read_bytes()
  185              require(len(data) == entry['Size'] == receipt['bytes'], 'size-mismatch')
  186              require(dropbox_hash(data) == entry['Hashes']['dropbox'], 'provider-hash-mismatch')
  187              row.update(byte_integrity='ok', sha256=hashlib.sha256(data).hexdigest())
  188              row['structure'] = structure(data, entry['Path'])
  189          except (ValueError, OSError, zlib.error, KeyError) as e:
  190              row['error'] = str(e) if isinstance(e, ValueError) else type(e).__name__
  191          outcomes.append(row)
  192      summary = {'files': len(outcomes), 'bytes_ok': sum(x.get('byte_integrity') == 'ok' for x in outcomes),
  193                 'errors': sum('error' in x for x in outcomes),
  194                 'structure': dict(collections.Counter(x.get('structure', 'not-verified') for x in outcomes)),
  195                 'cloud_inventory_stable': True, 'playability': 'unverified'}
  196      return {'summary': summary, 'files': outcomes}
  197  
  198  
  199  def main():
  200      parser = argparse.ArgumentParser(description=__doc__)
  201      parser.add_argument('packet', type=Path)
  202      parser.add_argument('--report', type=Path, required=True, help='New private JSON file; never overwrites')
  203      args = parser.parse_args()
  204      os.umask(0o077)
  205      try:
  206          result = verify(args.packet)
  207          with args.report.open('x') as f:
  208              json.dump(result, f, indent=2)
  209              f.write('\n')
  210          print(json.dumps(result['summary']))
  211          return int(result['summary']['errors'] > 0)
  212      except (OSError, ValueError, KeyError, TypeError) as e:
  213          # Paths and provider identities stay out of stdout/stderr.
  214          print('Verification refused: ' + (str(e) if type(e) is ValueError else type(e).__name__), file=sys.stderr)
  215          return 2
  216  
  217  
  218  if __name__ == '__main__':
  219      sys.exit(main())
```

## File: tools/cloud-save-integrity-test (at 8ebaf8daad, 114 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Synthetic corruption controls for cloud-save-integrity (#517); no personal input."""
    5  import argparse
    6  import copy
    7  import json
    8  from pathlib import Path
    9  import runpy
   10  import struct
   11  import subprocess
   12  import tempfile
   13  import zlib
   14  
   15  api = runpy.run_path(str(Path(__file__).with_name('cloud-save-integrity')))
   16  verify, digest, structure = api['verify'], api['dropbox_hash'], api['structure']
   17  p = argparse.ArgumentParser(description=__doc__)
   18  p.add_argument('--rclone', type=Path, required=True, help='Independent local Dropbox hash oracle')
   19  a = p.parse_args()
   20  count = 0
   21  
   22  
   23  def check(name, value):
   24      global count
   25      if not value:
   26          raise SystemExit('FAIL ' + name)
   27      count += 1
   28      print('PASS ' + name)
   29  
   30  
   31  def rejects(fn):
   32      try:
   33          value = fn()
   34          return isinstance(value, dict) and value['summary']['errors'] > 0
   35      except (ValueError, KeyError, OSError, zlib.error):
   36          return True
   37  
   38  
   39  def chunk(tag, data):
   40      return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
   41  
   42  
   43  png = api['PNG'] + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(b'\0\xff\0\0')) + chunk(b'IEND', b'')
   44  state = b'RASTATE\x01MEM ' + struct.pack('<I', 3) + b'abc' + b'\0' * 5 + b'END ' + b'\0' * 4
   45  compressed = zlib.compress(state)
   46  rzip = b'#RZIPv\x01#' + struct.pack('<IQI', 131072, len(state), len(compressed)) + compressed
   47  with tempfile.TemporaryDirectory(prefix='pix-save-integrity-control-') as temp:
   48      root = Path(temp)
   49      (root/'payloads').mkdir()
   50      payloads = [png, rzip, b'raw save bytes']
   51      entries = [{'Path': n, 'Size': len(d), 'ID': str(i + 1), 'IsDir': False,
   52                  'ModTime': '2026-01-01T00:00:00Z', 'Hashes': {'dropbox': digest(d)}}
   53                 for i, (n, d) in enumerate(zip(['screenshots/key.png', 'savestates/a.state', 'gba/a.srm'], payloads))]
   54      # Sort exactly as the collector contract specifies.
   55      pairs = sorted(zip(entries, payloads), key=lambda x: x[0]['Path'])
   56      entries, payloads = map(list, zip(*pairs))
   57      reads = [{'index': i, 'rc': 0, 'bytes': len(d)} for i, d in enumerate(payloads)]
   58      def write(name, obj):
   59          (root/name).write_text(json.dumps(obj))
   60      def reset():
   61          for name in ['before.json', 'after.json', 'ordered.json']:
   62              write(name, entries)
   63          write('reads.json', reads)
   64          for i, data in enumerate(payloads):
   65              (root/'payloads'/f'{i:04d}').write_bytes(data)
   66      reset()
   67      check('valid scoped packet including filename containing key', verify(root)['summary']['errors'] == 0)
   68      for label, data in [('changed', b'X' + payloads[0][1:]), ('truncated', payloads[0][:-1])]:
   69          (root/'payloads/0000').write_bytes(data)
   70          check(label + ' payload rejected', rejects(lambda: verify(root)))
   71          reset()
   72      (root/'payloads/0000').unlink()
   73      check('missing payload rejected', rejects(lambda: verify(root)))
   74      reset()
   75      for label, change in [
   76          ('wrong hash', lambda x: x[0]['Hashes'].update(dropbox='0' * 64)),
   77          ('missing hash', lambda x: x[0].update(Hashes={})),
   78          ('duplicate path', lambda x: x.append(copy.deepcopy(x[0]))),
   79          ('unsafe path', lambda x: x[0].update(Path='../escape')),
   80          ('size bound', lambda x: x[0].update(Size=api['LIMIT']+1)),
   81      ]:
   82          changed = copy.deepcopy(entries);change(changed)
   83          for name in ['before.json', 'after.json', 'ordered.json']: write(name, changed)
   84          check(label + ' rejected', rejects(lambda: verify(root)))
   85          reset()
   86      changed=copy.deepcopy(entries);changed[0]['ModTime']='2026-02-01T00:00:00Z'
   87      write('after.json',changed)
   88      check('remote change rejected', rejects(lambda: verify(root)))
   89      reset()
   90      changed=copy.deepcopy(reads);changed[0]['rc']=1;write('reads.json',changed)
   91      check('nonzero collector read rejected', rejects(lambda: verify(root)))
   92      reset();write('reads.json',reads[:-1])
   93      check('missing read receipt rejected', rejects(lambda: verify(root)))
   94      reset()
   95      # Provider can accurately hash already-corrupt data: structure must still fail.
   96      i=next(i for i,e in enumerate(entries) if e['Path'].endswith('.png'))
   97      bad=png[:-1]+bytes([png[-1]^1]);changed=copy.deepcopy(entries)
   98      changed[i]['Hashes']['dropbox']=digest(bad)
   99      for name in ['before.json','after.json','ordered.json']:write(name,changed)
  100      (root/'payloads'/f'{i:04d}').write_bytes(bad)
  101      r=verify(root)
  102      check('valid provider hash does not hide corrupt PNG', r['files'][i].get('byte_integrity')=='ok' and r['summary']['errors']==1)
  103      for name, data, path in [('PNG truncation',png[:-5],'x.png'),('RZIP truncation',rzip[:-1],'x.state'),
  104                               ('RZIP declared length',rzip[:12]+struct.pack('<Q',len(state)+1)+rzip[20:],'x.state'),
  105                               ('RZIP checksum',rzip[:-1]+bytes([rzip[-1]^1]),'x.state'),
  106                               ('RASTATE truncated block',state[:-4],'x.state')]:
  107          check(name+' rejected',rejects(lambda:structure(data,path)))
  108      check('raw save semantics stay unverified','unverified' in structure(b'raw save','x.srm'))
  109      # Four block-boundary cases plus empty input use a separately implemented oracle.
  110      for size in [0, api['BLOCK']-1, api['BLOCK'], api['BLOCK']+1, 2*api['BLOCK']+17]:
  111          data=(b'0123456789abcdef' * ((size+15)//16))[:size]
  112          oracle=subprocess.run([str(a.rclone),'hashsum','Dropbox','-'],input=data,capture_output=True,timeout=15)
  113          check('Dropbox oracle '+str(size),oracle.returncode==0 and oracle.stdout.decode().split()[0]==digest(data))
  114  print('PASS total='+str(count))
```