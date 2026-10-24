# Retrospective — M6.P2 T12, the VM harness (#659)

Phase 3, read from the history of the 60 at `8ebaf8daad` and from the record (`02` § The record). The four questions of the retro are stage G's; this file is the audit's look back at how the harness came to be what it is.

## 3.1 What the history shows

- **The commits:** 144 non-merge commits since `c445081a59`: 1 in August, 106 in September and 37 in October.
  - **The first** is `1a5368ec62` (2026-08-18, `tools: add scripted visual QA for the GENERIC_X64 VM`).
  - **The most touched** are `vm-qa` (39 commits), `vm-walks/claims.txt` (15), `vm-walks/README.md` (14), `time-to-play` (14), `vm-upgrade-rehearsal` (12), `ra-offline-test` (11) and `vm-pair` (9).
- **The harness grew one guard per failure it met,** and each guard's comment names its failure:
  - #125: the fixed waits that derailed walks became `settle` and `wait-for-change`;
  - blindspot 39: a PASS over dashes became `headline_missing`;
  - blindspot 40: `$SSHO` inherited from a shell;
  - #252: a visual change nobody meant, which became `frame-diff`;
  - #454: a stop that did not wait, which became `vm-stop`;
  - #545: a launch failure read as up, which became `vm-pair-test`.
- **The record runs from 2026-10-03 to 10-15 in `docs/qa-logs/`.** Its 59 distinct `vm-qa` runs are mostly the M7 replacement rounds. The September runs are rows in `docs/vm-qa-log.md` (44 run windows).

## 3.2 What worked

- **The guards fail closed where they were built after a failure.** `vm-stop` uses a pidfd with an identity re-check; `vm-pair` checks that the started PID owns its disk; `frame-diff` treats a MISSING frame or a size change as a FAIL; `signin-memory` FAILs without the load-finished line; `es-launch-memory` validates its cycles and bounds; `raofflineproxy-installed-native-test` refuses any skip.
- **No guest is found or stopped by pattern** (P3). The one stopping path is the pidfile and the owned disk.
- **Every walk checks every key press** (P5): 22 of 22 step files pair each `key` with a `wait-for-change`.
- **The claims contract holds together** (P5): no orphan claim, and no walk without a claim.
- **The cycle's numbers match the record's** (`02` § The guest cycle). The harness is stable in cost on today's image.

## 3.3 What was hard, as the code shows it

- **A runner whose exit and whose report disagree.** The report says `has not passed` beside a SKIP, and the exit says 0 (F-01). The comment at `vm-qa:141` (`a suite that could not run (rc 3) is shown as such, never folded into PASS`) is true of the table and not of the exit code.
- **Arguments that empty a measurement.** `time-to-play --repeat 0` and `emulator-exit-test --only X` each run nothing and pass (F-02, F-03). The guards judge what ran, and nothing judges whether anything ran.
- **Host state in `/tmp` and in the user's cache.** It was written when one session used the host. Today two lanes share it, and `/tmp` is a RAM tmpfs that ran out of inodes on 2026-10-24 (F-09, F-10).
- **A month-old baseline.** All 391 claims name `d72084ccad`'s cut (F-18). `frame-diff` has nothing to compare against for a newer cut until a maintainer accepts one.

## 3.4 What the slice inherits from earlier lanes

- **T9's D-INFRA-028:** `build-preflight` lists guests and names `vm-stop`. The harness's own stop path agrees with it (P3).
- **T1:** the exit hotkey `emulator-exit-test` drives. T1's retained `t1.qcow2` and its `ttp-*` runs sit under `/workspace/artifacts/m6-t1-20261023/`; that is a retention observation for the coordinator.
- **The legacy layout (#640):** `es-syntax-check:53`.

## 3.5 The seams

| Seam | What crosses it | What the read found |
| --- | --- | --- |
| `vm-qa` × the cloud suites × the image | `cloud-test-backend up`, `reset`, `seed-content`, `seed-device`; `cloud-round-trip` | The backend's state is per user and so shared across lanes (F-10). Seeding is unchecked (F-06). The round trip passed on the cycle in 84 s. |
| `frame-diff` × `claims.txt` × the walks × the menu map | the walk frames, 391 claims, 7 masks; `menumap` reads the ES pin | The reconciliation is clean (P5). All claims sit on one month-old baseline, with three whole-frame claims (F-18). `menumap` caught #542 (`04` § Q6). |
| `time-to-play` × the exit sync's budget (D-CLOUD-119) | `over_budget` against 3 s, on the median of the exit cell | The budget holds on the cycle (1.59 s). An empty cell is never judged (F-02). |
| the pair × the host's memory (`device-builds.md`) | 2 × 8 GiB allocated, about 6 GB of disks in the `/tmp` tmpfs | A booted guest holds 2.54 GiB resident (P11), near `device-builds.md`'s "about 2 GB". The pair's disks in RAM-backed `/tmp` are unbudgeted (F-09). |
| the harness × the M7 lane's guests (the host file) | ports 10022 to 10026, VNC :9 and :10, the default socket and pidfile names under `/tmp`, the QA cloud | Two lanes collide on the defaults. The cycle avoided them only by setting `VM_PAIR_DIR`, `VM_QEMU_RUNTIME_DIR`, `ROCKNIX_ARTIFACTS`, `CLOUD_QA_STATE` and `CLOUD_QA_PORT` by hand (F-09, F-10). |
