# Analysis — M6.P2 T12, the VM harness (#659)

## Executive summary

The harness is the fork's bench for every behaviour proof (`vm-first.md`). Read through the lens of cost against value, it is sound where it was rebuilt after a failure, and it is open where nothing has failed yet.

- **What is sound:**
  - No guest is found or stopped by pattern (P3). `vm-stop` is pidfd-exact, and the claims contract holds together (P5). Every walk checks every key press.
  - On today's image the guest suites cost what the record says (`02` § The guest cycle).
- **What is open:**
  - **Three tools can pass while proving nothing,** each shown on the guest (F-01, F-02, F-03).
  - **A default run's state assumes one user on the host:** the pair's disks in RAM-backed `/tmp`, and the QA cloud's state in the user's cache, which the walks reset (F-09, F-10).
  - **The cost concentrates in two suites:** `walks` and `scripts` are about 90 % of a 33-minute run (F-17).
  - **The value side shows:**
    - one suite, `exit`, with nothing recorded at all;
    - five more whose recorded failures were all the harness's own (F-16);
    - five tools nobody runs (F-14);
    - one fixture script for a retired migration (F-15).

The coordinator ruled at 19:33 on #659 that F-01, F-02 and F-03 are stage-D bugs, and that F-10 is a Q2/Q6 row.

## Acceptance-criteria scorecard

#659's 17 criteria, at stage B. The detail is in `02` § Phase 2.

| Met at stage B | Pending |
| --- | --- |
| 6 (`01` § Scope), 7 (coverage, 60), 8 (the controls), 9 (the guest cycle), 10 (nothing never-run), 11 (Q5 below), 12 (Q6 below), 13 (Q3 below), 14 (Q7 below), 15 (11 class cells = 11 PROOF lines) | 1 to 5 and 16 to 17: stages C to H |

## Code Quality Assessment

### Strengths

- **The guards name their own failure.** Each comment near a guard says what failed before it existed: #125, blindspots 39 and 40, #252, #454, #545.
- **The stop path is exact:** `vm-stop` uses a pidfd, re-checks identity, and keeps the pidfile when it times out.
- **Measurement tools refuse what they cannot read:** `signin-memory`, `es-launch-memory`'s bounds, and `raofflineproxy-installed-native-test`'s no-skips rule.

### Concerns

- **Pass-without-proving through arguments, and through the exit code** (F-01 to F-03). Each tool judges what ran and does not check that anything ran.
- **`assert` as a check** in seven tools (F-04).
- **Host defaults from a one-session host:** `/tmp` roots, a per-user QA cloud and fixed ports (F-09, F-10).

### Complexity Hotspots

- **`vm-qa`:** 541 lines, 17 suites and four fixture builders in one bash file. Its fixture seeding is unchecked (F-06).
- **`time-to-play`:** 1,593 lines, the slice's largest file. Its headline rule is sound for every cell that ran (F-02).

## Risk Assessment

| Risk | Shape | Today |
| --- | --- | --- |
| A green run that did not pass | F-01 (a SKIP), F-02, F-03 (an empty measurement) | Each is reached only through a SKIP or a hand-typed argument; the default `vm-qa` run is not affected except by F-01 |
| Two lanes on one host | the shared QA cloud state (F-10), `/tmp` sockets, pidfiles and ports (F-09) | Avoided on this cycle by five environment variables set by hand |
| Host memory under a build | the pair's disks in a RAM tmpfs (F-09) | About 6 GB per `up`, beside 2 × 8 GiB guests; a booted guest holds 2.54 GiB resident (P11) |
| A baseline nobody moves | F-18 | All 391 claims are against the 2026-09-26 cut |

## Coverage Boundary

- **Read:** the 60, line by line for `vm-qa`, `vm-pair`, `vm-stop`, `frame-diff` and `emulator-exit-test`. The rest are read for their exit and pass logic, their find/stop paths and their `/tmp` and legacy paths (`02` § Mechanical checks).
- **Run:** the three no-guest controls; one guest cycle (`vm-qa` with five suites and two argument probes); one host probe (P6).
- **Not run:**
  - `walks` (16.7 min, and the record holds 23 runs);
  - `pair-identity` (needs the pair);
  - `link` and `ra-offline` (opt-in; brief § 8);
  - `ra-offline-test`, `ra-ui-test`, the three `raofflineproxy-*` tests, `signin-memory`, `es-launch-memory`, `vm-upgrade-rehearsal`, `font-stems` and `ra-candidate-games`. Their costs come from the record, through the research helper.
  - `device-act` and `qa-accounts` are read only.
- **The record:** the 61 `vm-qa` reports under `docs/qa-logs/` (2026-10-03 to 10-15). The September runs are kept only as `docs/vm-qa-log.md` rows; their full reports are under `/workspace/artifacts`, which was not read.

## Finding Verification (Phase 4.5)

Each finding was re-read against its artifact, looking for the reading that would refute it.

| ID | The refutation tried | Verdict |
| --- | --- | --- |
| F-01 | Is exit 0 over a SKIP intended? The header promises `exits non-zero if any suite failed -- so a nightly can tell`. A SKIP is "not passed" in the report's own words (`:528`) and passed in its exit (`:541`). | Stands (P7). Whether a SKIP should fail the exit is the coordinator's contract question; that it reads as a pass is the bug. |
| F-02 | Does `--quick` make it unreachable? Yes, for `vm-qa`'s call (`:1017-1019`). A hand run is the documented form for proposing a register number (`vm-qa:332-333`), and that is where it is reached. | Stands, Low (P8) |
| F-03 | Same question; `vm-qa` passes the default `ABCD` | Stands, Low (P9) |
| F-04 | Does anyone run with `-O`? Nothing in the tree, nor in this host's environment. | Stands as a latent fail-open (P6), Low |
| F-05 | Does the walk's first `wake` / `dismiss-dialogs` fail on an absent EmulationStation? `settle` never fails (`vm-visual-qa:350-367`), and a framebuffer still exists, so it does not. `frame-diff` would catch it with a baseline. | Stands, Low |
| F-06 | Does a failed seed show elsewhere? The walks' frames would differ, which `frame-diff` catches only with a baseline; `time-to-play` refuses an unreachable remote (`:1324-1326`). | Stands, Low |
| F-07 | Its log says the register was checked without the interface's citations, and the report does not | Stands, Low |
| F-08 | `frame-diff` reports a MISSING frame as a FAIL when a baseline exists | Stands, Low, joined to F-01's SKIP |
| F-09 | Is `/tmp` a RAM tmpfs here? `findmnt`: `tmpfs 30.4G`. `vm-pair` documents the default and its override (`:28-32`). | Stands, Medium for the host's memory |
| F-10 | Does `vm-qa` set `CLOUD_QA_STATE`? No. The default is `${XDG_CACHE_HOME:-~/.cache}/rocknix-cloud-qa`, per user. | Stands |
| F-11 | Is the root absent? `ls` says so | Stands, #640 |
| F-12 | `sed -n '5,38p'` against the header's length | Stands, Low |
| F-13 | Re-derived against `next` (`q7-descriptions.txt`) | Stands, a rule drift: a lead |
| F-14 | Re-derived for three; the helper confirmed the other two | Stands, Renovation |
| F-15 | The guest: `cloud_migrate_layout` absent (P10) | Stands, Renovation |
| F-16 | Spot-checked three catches; the "nothing recorded" rows rest on the helper's search of the work logs, `docs/qa-logs` and the registers | Stands as recorded, Renovation |
| F-17 | Re-derived medians (P4) | Stands, Renovation |
| F-18 | `BASELINE.txt` and `claims.txt`'s heads | Stands, Low |
| F-19 | `du` on the host | Stands, Low |
| F-20 | `vm-upgrade-rehearsal:30` | Stands, Low |

**Withdrawn at Phase 4.5:** L2 (that `vm-qa` folds a real failure into a SKIP). Rc 3 is a deliberate skip in `last-good-scripts-test` and in the `frame-diff` suite, and `retroarch-wrapper-test`'s binary returns 0 or 1.

## Renovation face

### Q1 Modernize

| Row | Where | Reading |
| --- | --- | --- |
| Legacy build root | `es-syntax-check:53` | `/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64`, absent; rc 2 (F-11, #640) |
| Host `/tmp` roots | `vm-pair:37`, `:41`; `vm-qa:98-99`; `time-to-play:158`; `ra-offline-test:65-66`, `:259`, `:345` | They predate the inode exhaustion of 2026-10-24 and two lanes sharing one host (F-09) |
| `ES_SRC` default | `vm-qa:167` and five more | `~/Development/emulationstation-next.worktrees/qa-integration`, present at the pin `16dbac521`; a per-user path, not the canonical layout (#640's question) |
| Retired mechanism | `vm-walks/cloud-epic/migration-protocol.sh:9-12` | `cloud_migrate_layout` (D-CLOUD-175) (F-15) |
| QEMU and Python | the host | QEMU 10.2.1, Python 3.14.4. `pidfd_open`, `int.to_bytes`, f-strings and stdlib PNG all work (Q4) |

### Q2 Standards and best practices

| Row | Where | Reading |
| --- | --- | --- |
| Find/stop | the eight tools | pidfile and owned disk; no pattern (P3) |
| `assert` as a check | 7 tools | F-04 |
| Unchecked seeding | `vm-qa:389`, `:397-398`, `:408`, `:341` | F-06 |
| Shared state | `vm-qa:397`; `cloud-test-backend:93` | F-10 |
| An override honoured by some | `vm-upgrade-rehearsal:30` | F-20 |
| `pipefail` | `vm-qa` uses `set -u` only; `vm-pair` uses `set -euo pipefail` | `vm-qa`'s pipelines are not gating except `walk_all`'s `\| timeout … vm-visual-qa`, whose exit is the last command's, the one wanted |
| Credentials | `qa-accounts`, `ra-offline-test:263` | the account is masked (`sed "s/${ACCOUNT}/<account>/g"`); `qa-accounts` prints no value. Read, not run. |

### Q3 Bugs

**The pass-without-proving hunt, suite by suite.** A constructed input is named where one passes wrongly. "None" means the lane found none.

| Suite or tool | Line read | Constructed input that passes wrongly |
| --- | --- | --- |
| `vm-qa` (the runner) | `:141-148`, `:541` | any SKIP: `frame-diff` with no baseline, run on the guest: rc 0 (P7, F-01) |
| scripts | `last-good-scripts-test` tail | skipped checks: exit 3, then SKIP, then F-01 |
| lifetime | `vm-qa:166-175` | none: a missing checkout is rc 1 |
| wrapper | `retroarch-wrapper-test:216-226` | none: rc 2 with no source; the binary is 0 or 1 |
| vocabulary, french, quoting, menumap | `vm-qa:186-196` | none found; each fails on an absent checkout or a missing file (`es-untranslated` rc 2) |
| register | `vm-qa:205-215` | an absent ES checkout: checks less and passes (F-07) |
| pair-identity | `vm-qa:222-269` | none: every field asserted non-empty first; no mDNS line is a FAIL |
| fresh | `vm-qa:278-293` | none: the link targets are compared exactly; an unanswered SSH gives an empty target, which is a FAIL |
| round-trip | `vm-qa:295` → `cloud-round-trip` | none in the call (no `--only`); the tool is another slice's |
| exit | `emulator-exit-test:145-196` | `--only X`, run on the guest: `PASSED` rc 0 (P9, F-03); `vm-qa` passes `ABCD` |
| time-to-play | `time-to-play:994-1019`, `:1306-1332` | `--repeat 0`, run on the guest: rc 0 with empty cells (P8, F-02); `vm-qa` passes `--quick` |
| link | `vm-qa:349` | not run; its stamp parser was the harness's own failure (#398, recorded) |
| ra-offline | `vm-qa:358`; `ra-offline-test` | not run; a stale `exec.log` false PASS is blindspot 50, already fixed |
| walks | `vm-qa:426-513`; `vm-visual-qa:524-530` | an EmulationStation that never returns after the reboot (F-05); a monitor whose screendump fails (F-08); both leave rc 0 and are caught by `frame-diff` only with a baseline |
| frame-diff | `frame-diff:264-353` | none while a baseline exists; three whole-frame claims make three screens uncomparable (F-18) |
| `vm-manager-system-check` | `:12-15` | `PYTHONOPTIMIZE=1` (P6, F-04) |
| `es-launch-memory` | `:39-42`, `:157-161` | none: bounds required for acceptance |
| `signin-memory` | `:108-125` | none |
| `vm-upgrade-rehearsal` | `:35-51`, `:168-170` | none found |

**Every tool that touches a QEMU, classified:**

| Tool | Finds | Waits | Stops | Class |
| --- | --- | --- | --- | --- |
| `vm-pair` | its pidfile, checked against its disk (`:78-95`) | `vm-serial wait --up-to 300`, then SSH 100 tries | `vm-stop` pidfile + disk (`:129`) | pidfile-and-disk |
| `vm-stop` | pidfile; identity re-check | pidfd poll, 20 s | pidfd SIGTERM | pidfile-and-disk |
| `vm-qa` | reads `$RUNTIME/rocknix-qemu.pid` for the display line only (`:137-138`) | SSH 40 tries | never (`vm-pair down` when not `--skip-up`) | pidfile-and-disk |
| `time-to-play`, `ra-offline-test`, `emulator-exit-test`, `es-launch-memory`, `signin-memory` | none: SSH, serial or monitor to a running guest | their own bounded loops | none host-side | n/a (guest-side only) |
| `vm-upgrade-rehearsal` | through `vm-pair` | through `vm-pair` | through `vm-pair down` | pidfile-and-disk |

### Q4 Package currency

Not a package slice. The tools assume QEMU's monitor and `pidfd` (Python 3.9 or later), and the host has QEMU 10.2.1 and Python 3.14.4. The image the record ran on was mostly the M7 replacements, 2026-10-03 to 10-15. The newest image present is `069fc2704421` (2026-10-22), on which the cycle ran.

### Q5 Efficiency

**The cost table.** Minutes are medians from the 59 distinct reports (P4), with the cycle's figure where it ran. "Host" is what the suite itself needs; under a default run every suite also sits inside the pair and the QA cloud that `vm-qa` brings up first (`vm-qa:118-122`), and the report's minutes leave out that bring-up and the fixture work outside `run_suite` (the seat's G-71). "Cadence" is from `vm-qa:64` and `release-candidates.md` step 3.

| Suite or measurement | Minutes (median / max) | Host it holds | Cadence |
| --- | --- | --- | --- |
| scripts | 13.0 / 15.1 | host only (busybox shims, bubblewrap) | every candidate |
| lifetime | 0.02 | host only, ES checkout | every candidate |
| wrapper | 0.0 | host only, a RetroArch source in a build root | every candidate |
| vocabulary | 0.0 | host only | every candidate |
| register | 0.03 | host only | every candidate (also the fork CI and the pre-push gate) |
| french | 0.0 | host only | every candidate |
| quoting | 0.0 | host only | every candidate |
| menumap | 0.0 | host only | every candidate |
| pair-identity | 0.02 | both guests | every candidate |
| fresh | 0.0 (cycle: 1 s) | guest a | every candidate |
| round-trip | 1.41 / 2.0 (cycle: 84 s) | guest a + the QA cloud | every candidate |
| exit | 0.47 / 0.48 (cycle: 27 s) | guest a | every candidate |
| time-to-play | 1.15 / 1.42 (cycle: 72 s) | guest a + the QA cloud | every candidate |
| link | 7.95 / 9.0 | guest a, serial, the QA cloud | opt-in (11 runs) |
| ra-offline | none in any report; standalone 4 to 5.7 | the selected guest (a by default, `vm-qa:57`; d in the header's example), serial, the QA account | opt-in (0 runs in `vm-qa`) |
| walks | 16.7 / 17.2 | guest a, 16 reboots | every candidate |
| frame-diff | 0.02 | host only, the baseline (12 MB) | every candidate (SKIP without a baseline) |
| **a default run** | **33 (28 to 35)**, 19 full runs | **the pair (2 × 8 GiB, 8 vCPU) the whole run**, about 6 GB of `/tmp` disks | every candidate |
| `time-to-play` (standalone, `--repeat 5`) | no recorded run | one guest | by hand, for a register row |
| `signin-memory` | 1.4 to 1.5 | one guest (1 GiB form) | webkitgtk bumps |
| `es-launch-memory` | 7.0 for 50 cycles; 9.3 to 17.8 in combined jobs | one guest | no rule schedules it |
| `vm-upgrade-rehearsal` | about 1.9 (96 to 159 s), 19 runs | both guests | every candidate (step 3) |
| `ra-ui-test` | 7.7 to 8.6, 4 runs | one guest | proxy UI changes |
| `raofflineproxy-integration-test` | 0.3 | host only | proxy refreshes |
| `raofflineproxy-consent-test` | 0.8 | one isolated guest | proxy refreshes |

**What it says:**
- `walks` and `scripts` are about 30 of a default run's 33 minutes (F-17).
- The pair is held for the whole run, while one 1-second suite, `pair-identity`, needs guest b (F-17).
- Ten suites take under 3 seconds each (lifetime, wrapper, vocabulary, register, french, quoting, menumap, pair-identity, fresh and frame-diff); corrected after the seat counted the table.
- The record holds no full-cell `time-to-play` run.

### Q6 Dead ends

**The value table.** The source for every row is `/workspace/tmp/m6-t12/research-q6.md` (with path:line), spot-checked by the lane (`00`). "Catch" means a product or record defect the item found. "Positive" means a constructed failure it was seen to fail on. "Callers" means who runs it: `vm-qa`, the CI, a rule's instruction or a skill. `nobody` means none of those.

**Suites:**

| Suite | Last recorded catch | Recorded positive | Callers |
| --- | --- | --- | --- |
| scripts | #414, 2026-10-04 (a stale schema pin) | its sections' failing-copy cases; blindspots 60 and 61 | `vm-qa`; rules |
| lifetime | **nothing recorded** (its FAILs were its own test double, 2026-10-11) | the ASan pre-fix run, 2026-09-06 | `vm-qa` |
| wrapper | **nothing recorded** by the suite (written after #211) | 2017 runs of 2000 posts against the unfixed source | `vm-qa` |
| vocabulary | #148 at introduction, 2026-09-12 | 3 of 3 constructed violations | `vm-qa` |
| register | D-CLOUD-007 and a dangling citation (`vm-qa:202-203`) | `4b219ef937`, `f00ab3e163` | `vm-qa`, **CI** `fork-checks.yml:37`, `ceremony-check` |
| french | #152, 2026-09-17 | a probe string, `196f823c60` | `vm-qa` |
| quoting | blindspot 57, 2026-09-25 (`GuiMenu.cpp:7597`) | before and after ES `459fc168f` | `vm-qa` |
| menumap | #542, 2026-10-11 (CONNECTION SAVED) | `cc996bd0de` | `vm-qa` |
| pair-identity | **nothing recorded** but its own (blindspot 40) | a recorded lost race through a fake `ssh`, 2026-09-13 | `vm-qa` |
| fresh | audit #258 PL-001, 2026-09-24 (`es_savestates.cfg`) | the same run on `443028ff7a` | `vm-qa` |
| round-trip | #315, 2026-09-28/29 (and two stream-A regressions) | run 71's expected FAIL | `vm-qa`; rules |
| exit | **nothing recorded as a catch** (it has a recorded positive) | the debounce-stripped copy, `6b95a93d2f` | `vm-qa`; rule command |
| time-to-play | **nothing recorded** but its own (blindspots 39 and 56) | `ttp-263c`; four constructed logs | `vm-qa` |
| link | #401, 2026-10-03 | `test-stamp-assertion.py` 7/7 | opt-in in `vm-qa`; rule |
| ra-offline | **nothing recorded** but its own (blindspot 50) | none found | opt-in; `release-candidates.md:64` |
| walks | G-E2-O1 through `confirm-cloud-folder`, 2026-09-28 | none per walk; `frame-diff` is its comparator | `vm-qa`; `es-ui-style-guide.md:62` |
| frame-diff | G-E2-O1, 2026-09-28 | the missing-claim control rc 1, 2026-10-11 | `vm-qa`; `release-candidates.md:62` |

**Measurements and other scripts** (the drivers, `vm-pair`, `vm-serial`, `vm-stop`, `vm-visual-qa` and `png-blackout`, are infrastructure, not detectors):

| Script | Last recorded catch | Positive | Callers |
| --- | --- | --- | --- |
| `time-to-play` (standalone) | as its suite | as its suite | `vm-qa` only |
| `signin-memory` | **nothing recorded**; it was blindspot 59's false PASS | Dropbox FAIL, example.org PASS | **nobody** (index only) |
| `es-launch-memory` | #310, 2026-10-03 (ES leaks) | the RSS endurance control | **nobody** (index only) |
| `vm-upgrade-rehearsal` | **nothing recorded** (PASS every cut) | `24ceb9e15a` checks | `release-candidates.md` step 3 |
| `ra-ui-test` | **nothing recorded** | the refusal profile | rule mention |
| `raofflineproxy-integration-test` | **nothing recorded** | the wrong-duration negative, `8829907b12` | `release-candidates.md` (proxy) |
| `raofflineproxy-consent-test` | #457, 2026-10-06 | three assertions before patch 019 | rule mention |
| `raofflineproxy-installed-native-test` | **nothing recorded** | none found | **nobody** (descriptive paragraph) |
| `font-stems` | blindspot 54, 2026-09-24 | none found | **nobody** (descriptive mention) |
| `ra-candidate-games` | **nothing recorded** | none found | **nobody** (index only) |
| `es-untranslated` | #152 | `196f823c60` | `vm-qa` french |
| `es-syntax-check` | **nothing recorded** of an edit; its own silent FAIL is #699 | a broken copy FAILs | rule instruction |
| `emulator-exit-test` | **nothing recorded** | `6b95a93d2f` | `vm-qa` exit |
| `qa-accounts` | **nothing recorded** | proven both ways, `4e11497aa7` | `ra-offline-test` |
| `device-act` | a recorder; its own failures 2026-09-27 | none found | rule instruction |
| `vm-pair-test` | **nothing recorded** (no red CI run read) | the original source falsely says up | **CI** `fork-checks.yml:47` |
| `vm-upgrade-readiness-test` | **nothing recorded** after creation (#546's regression) | seven controls | **CI** `fork-checks.yml:48` |
| `vm-stop-test` | **nothing recorded** after creation | the corrected seventh case | rule mention |
| `vm-manager-system-check` | **nothing recorded** (written after #455) | its own controls | `vm-qa` |
| `vm-walks/cloud-epic/migration-protocol.sh` | **nothing recorded**; refuses on current images (P10) | none | `rasteratops-vm-cloud-epic:149` |
| `vm-walks/cloud-epic/vnc-grab.py` | **nothing recorded** | none | `rasteratops-vm-cloud-epic:67` |
| `vm-walks/fixtures/system-selected.sh` | **nothing recorded** | none | `vm-qa:473` |

**Walks** (16 in `suite.txt`, each run by `vm-qa`'s walks suite and keyed to `frame-diff` by its claims; P5):

| Walk | Claims | Last recorded catch |
| --- | ---: | --- |
| to-manage-cloud-storage | 3 | nothing recorded |
| back-up-page | 8 | nothing recorded |
| restore-page | 9 | nothing recorded |
| match-dialog | 19 | its 2026-09-07 cycle ("1 FILES", the preview's 0-byte line) |
| to-change-cloud-folder | 21 | its 2026-09-07 cycle (the editor's field) |
| confirm-cloud-folder | 32 | G-E2-O1, 2026-09-28 |
| tick-roms | 13 | nothing recorded |
| tick-settings | 13 | nothing recorded |
| tick-game-content | 13 | nothing recorded |
| continue-to-systems | 23 | nothing recorded |
| run-transfer-frames | 115 | its 2026-09-09 cycle (row 4 clipped, `e7e672524`) |
| run-transfer | 39 | nothing recorded as a defect (#278, the walk's state) |
| ui-settings-toggle | 6 | nothing recorded |
| manager-nes | 2 | nothing recorded (the standing #245/#250 guard) |
| manager-gb | 7 | its own (#455: it showed FBNeo) |
| manager-fbn | 68 | nothing recorded |

**The step files no suite walk replays,** and their callers:
- the four `docs/*.steps` (rocknix.org, #323), and `m7-cloud-sync` and `m7-retro-achievements` (M7's hand walks), each named in 24 to 41 record files and in the #603 audit's lead-verification config;
- `reset` and `wake`, utility legs.

**Fixtures:**
- **`nes-256x240-right.png` and `arcade-vertical-raw-left.png`:** read by `vm-qa:380-385`. They were the controls in #288's session proof, 2026-09-26.
- **`gb-160x144.png`:** read by `vm-qa:381`, `:384`; nothing recorded.

**The reconciliation** (P5): there are 391 claims and 16 walks; no claim's glob matches no walk, and no walk lacks a claim. All 391 are against `d72084ccad` (F-18).

### Q7 Clarity and structure

| Row | Where | Reading |
| --- | --- | --- |
| `vm-qa --help` | `:81` | prints lines 5 to 38, cutting four suites (F-12) |
| The header's suite list against `SUITES` | `:20-49`; `:63` | the same 17, in the same order |
| `release-candidates.md` step 3 against the default | `release-candidates.md` on `next` | "`tools/vm-qa` with every suite"; the default omits `link` and `ra-offline` (`vm-qa:64`). A reader cannot tell whether "every suite" means the default or all 17: **a lead for the coordinator** |
| The index against the owning rule | `instruction-files.md`; `generic-x64-vm-testing.md` (`next`) | six tools pointed at a rule that never names them; three walk scripts with no row (F-13): **a lead** |
| `suite.txt` | the brief | 16 walks, against the brief's 17 (a delta, `01`) |
| The image's identity | the brief; criterion 9 | the sha256 is in the `.img.gz.sha256` sidecar, not in `.identity.json`; corrected on #659 at 19:33 |
| `generic-x64-vm --daemonize`'s help | another slice's file | "stop it with kill $(cat pidfile)", against `vm-stop` (context for its slice, not a row here) |
| `device-builds.md`'s "about 2 GB" per guest | `next` | measured at 2.54 GiB resident after boot (P11): close. The profile allocates 8 GiB. |

## Instruction File Recommendations

### Coverage Gaps (would-have-prevented)

- **"A guard judges that something ran, not only what ran."** F-01 to F-03 share one shape: the result is computed over an empty set. `engineering-practices.md` § Guards must fail closed says *a tool that reports numbers fails when the numbers are missing*; the empty set is that case one level up. **A proposal for the coordinator.**

### Codification Gaps (needs-new-rule)

- **A harness run's host state is named by the run.** The QA cloud's state, the pair's directory, the sockets and the ports are all defaults that assume one session on the host (F-09, F-10). The cycle set five variables by hand. **A proposal for the coordinator,** since the rules are not this lane's.

### Recommended Action Sequence

1. F-01 to F-03: the coordinator's stage-D bugs, with their inputs.
2. F-10 and F-09: the shared state.
3. F-04: the `assert` class.
4. F-14 to F-17: the coordinator's dispositions with the maintainer.
5. The Lows.

## Quality Self-Check

- **The coverage table** has 60 rows (`grep -c -E '^\| \`tools/'` gives 60).
- **The proof cells match:** 11 PROOF lines in `00` and 11 class cells in `02`.
- **Every finding has an artifact,** and the record-sourced rows name the helper's file and the lane's spot checks.
- **Every time** comes from `date -u` or an artifact's mtime.

## Second opinion (Phase 4.6)

**The seat:** GPT-6 Astra at `max` through the Facilitator, one refutation over one packet. Its provenance:
- `verification PASS`, observed `openai/gpt-6-astra`;
- `effort_verification PASS`, 44,475 reasoning tokens;
- `provider_verification PASS`, OpenAI;
- `outcome success`, 19:41:36 to 20:16:02 (`second-opinions/gpt-audit.md.provenance.json`).

The probe passed at 19:41. The packet (712,845 bytes) was scanned before it was sent (`00` § Stage C).

**How each item was graded:** each of the seat's 72 new items was read at its cited lines.
- The lane read G-02, G-08, G-27, G-37, G-50, G-51, G-59 and G-60 itself.
- A read-only helper checked every item's factual claim against the export (`/workspace/tmp/m6-t12/seat-verify.md`): 71 TRUE and 1 PARTLY (G-41). The lane spot-checked five of its rows (G-01, G-19, G-43, G-67, G-72) against the code (`00`).
- A factual claim that holds is not yet a grade. The grade weighs reach (the default run, a hand run, an opt-in suite), the threat model (QA-only guests, D-QA-016) and whether the item is a defect or a documented design.

**The grades:** 56 confirmed, 15 narrowed to leads, and 1 withdrawn.

### The seat's new items

| G | Seat | Verified | Grade | Severity | Punch item | Why, and the artifact that decided it |
| --- | --- | --- | --- | --- | --- | --- |
| G-01 | Medium | TRUE | Confirmed | Medium | PL-01 | joins F-01: an unknown or empty `--only` runs nothing and passes; vm-qa:74 `--only) ONLY=$2` has no name validation. Each suite is gated by `case ",$ONLY," in *,name,*)`, so a typo matches nothing. With FAILS=0 and SKIPS=0, line 528 prints `**PASSED**` and line 541 `[ "$FAILS" = 0 ]` exits 0. Th |
| G-02 | High | TRUE | Confirmed | High | PL-04 | `vm-pair down` ignored and `up \| tail -2` masks its status (`vm-qa:120-121`); vm-qa:120 `"$ROOT/tools/vm-pair" down >/dev/null 2>&1` (status ignored); :121 `vm-pair up "$IMAGE" 2>&1 \| tail -2` (the pipeline status is tail's; :55 is only `set -u`, no pipefail). BUILD then comes from whatever answers on the |
| G-03 | Medium | TRUE | Confirmed | Low | PL-16 | `fresh` reads port 10022 whatever `--guest` says; fresh_suite hardcodes `-p 10022` (:281, :285, :289) whatever `--guest` is, while :139 reports `guest $GUEST at :$PORT`. It reads current `readlink`/`.configured` only, so with `--skip-up` nothing ties the result to a fresh install |
| G-04 | Medium | TRUE | Confirmed | Medium | PL-16 | `ES_SRC` is not bound to the image's pin; vm-qa:167 `es="${ES_SRC:-$HOME/...qa-integration}"`. :171 only echoes `git rev-parse --short HEAD`. :188/:191 point french and quoting at the same default. es-untranslated:143 `src = source_strings(a.es_src)`. Nothing compares the |
| G-05 | Medium | TRUE | Confirmed | Low | PL-06 | same build, backend, guest and minute share a directory; vm-qa:131 `OUT=...qa-${BUILD}-${BACKEND}-${GUEST}-$(date +%Y%m%d-%H%M)`; :132 `mkdir -p` reuses the directory; :139 `> "$REPORT"` and :145 `> "$log"` overwrite; :533 `if [ -f "$OUT/time-to-play/time-to-play.md" ]` appends whatever |
| G-06 | Medium | TRUE | Confirmed | Low | PL-17 | a report-write failure is not a FAIL; :132 `mkdir -p "$OUT/walks"`, the :139 report write and the :149 append are all unchecked. The exit at :541 depends only on FAILS. |
| G-07 | Medium | TRUE | Narrowed | Low | PL-23 | a publication log, not an answer: the suite's documented design (`vm-qa:247-255`); a lead; :257 `journalctl -b -u avahi-daemon -o cat ... sed -n "s/.*Host name is ...` reads a past log line. No mDNS query is made. |
| G-08 | High | TRUE | Confirmed | Medium | PL-02 | the first changed stamp is timed without its rc or token (`time-to-play:641-647`, `:685-689`); time-to-play:687 `if now and now != before:` accepts any changed stamp. parse_stamp (:641-647) is never judged. headline_missing (:1311-1331) checks only `t_sync_stamp is None` plus `remote_reachable` (`rclone lsd qa-cloud:`, :117 |
| G-09 | Medium | TRUE | Confirmed | Medium | PL-02 | startup, offline and bounds results never judged; headline_missing checks cells launch/exit/g2g only (:1311-1313). Startup `entry["error"]` (:1348) is never judged. :1241 `conds = [c for c in want if c in conds] or want` lets unknown names through, and an unknown cond takes the ` |
| G-10 | Medium | TRUE | Confirmed | Medium | PL-02 | shown by the cycle: g2g stamp `-`, token `?`, PASS; g2g is judged only on `t_second_game_frame` (:1313), and exit only on `t_sync_stamp` (`t_card_gone` is not judged). In cycle/vm-qa/report.md, g2g's "the exit sync's stamp" row reads `-`, the token reads `` `?` x1 ``, and the suite |
| G-11 | Medium | TRUE | Confirmed | Low | PL-18 | surface qualification once, scaled `None` passes; :309 `if sw and panel:` means `scaled` stays None when the panel read fails. :1316 `if surf.get("scaled")` then passes, and :1318's fallback fires only when `surface is None`. That fallback also requires `cells.get("launch")`, so  |
| G-12 | Medium | TRUE | Confirmed | Medium | PL-02 | an already-running RetroArch satisfies the launch; measure_launch (:524-590) marks `ra["seen"]` on any RetroArch pid with no comparison to an earlier pid. `result["http"] = http` (:540) is never judged. The `wait_drawing(g)` return is discarded at :1196 and :1203. |
| G-13 | Medium | TRUE | Confirmed | Low | PL-18 | the workload ignores `--rom`; jitter 0 in quick; seed_payload always writes `savestates/nes/Probe.*` and `nes/Probe.srm` (:418-434), whatever the rom: a `--rom` value or the GB fallback (:378). With `--quick`, repeat is 1, so `cycle(..., i, ...)` gets jitter 0 at both :1211 and  |
| G-14 | Medium | TRUE | Confirmed | Low | PL-18 | `/tmp/ttp-kill` lost across the startup reboot; `/tmp/ttp-kill` is written by install_helpers (:394-401), called once (:1048). measure_startup reboots (:1343) and never reinstalls it. `g.kill_game()` (:1392, and later settle_sync/measure_exit) discards the rc. :1043's comment s |
| G-15 | Medium | TRUE | Confirmed | Low | PL-18 | guest mutation before the cleanup's `try`; :1041 `set_setting cloudsaves.gameexit 1...`, the :1047 reboot and the :1081/:1085 cfg edits all run before the :1121 signal handlers and the :1125 `try`. The backup scp's (:1065-1068) returncode is ignored. :1124 `fr = Frames(... |
| G-16 | Medium | TRUE | Confirmed | Low | PL-18 | restoration incomplete; restore() (:1088-1115) never removes the seeded Probe.* saves. It puts rclone.conf back only `if os.path.exists(saved_conf) and getsize>0`, so a conf the run created stays. read_routes keeps `head -1` per family (:904-905) and DEL |
| G-17 | Medium | TRUE | Confirmed | Low | PL-06 | fixed fixture ports, unowned; :137-139 hardcode the ports 9016/9017. Fixture.up() (:809-817) returns True on any `create_connection` success, without checking `self.proc`. The callers at :1415 and :1422 ignore the return value. |
| G-18 | Low | TRUE | Withdrawn | - | - | no CLI path produces a NaN or negative headline; the seat says so itself; headline_missing tests only `r.get(field) is None` (:1329), and over_budget only `med > EXIT_SYNC_BUDGET_S` (:1300). A negative value or NaN passes both (NaN > 3 is False). As the seat says, no CLI path that produces such a value  |
| G-19 | Medium | TRUE | Confirmed | Low | PL-15 | an empty baseline with an empty run passes; frame-diff:289 `screens = sorted(set(bframes) \| set(rframes))`. With both empty, nothing is marked missing and :344 gives PASS. os.walk on a run directory that does not exist yields nothing. accept (:397) refuses only an empty s |
| G-20 | Low | TRUE | Confirmed | Low | PL-15 | `PROPOSAL ONLY` claims are live; claims.txt:77 `# PROPOSAL ONLY...` is a comment, which read_rects (:137) skips. Lines 89-91+ carry `d72084ccad ...`, and :285 `live = [c for c in claims if c['head'] in ('*', bid)]` makes them live. The tail (`#578 ...`) is free t |
| G-21 | Medium | TRUE | Confirmed | Medium | PL-15 | `run-transfer*/*` masks cover every screen of those walks; masks.txt:7-9 use the glob `run-transfer*/*`. fnmatch (:156) matches it against every screen in the run-transfer dirs. suite.txt:90 composes run-transfer from `to-manage-cloud-storage ...`, whose step file shots `cloud-hub`, so `r |
| G-22 | Low | TRUE | Confirmed | Low | PL-15 | `--min-pixels` makes the identical-screens sentence false; :327 `if n < minpx: continue`, so a below-threshold box appends no line. :343 then prints `Every walked screen is pixel-identical...` when `lines` is empty. The header (:25-28) says every changed pixel must be claimed. |
| G-23 | Medium | TRUE | Narrowed | Low | PL-23 | the frames are RGB (PPM to PNG, `vm-visual-qa:417-466`); alpha matters only for a hand-made RGBA frame; :119-124: for RGBA, `rgb[0::3] = cur[0::4]` etc. Alpha is dropped before the comparison. |
| G-24 | Low | TRUE | Narrowed | Low | PL-23 | needs a crafted zero-size PNG with a valid IDAT; :76 unpacks only `w,h,depth,ctype` (the interlace byte is never read), and :81 checks only depth and ctype. Width and height of 0 are not refused. :92 `line = raw[q:q+stride]` takes a short slice without a check (filter 0 accepts  |
| G-25 | Low | TRUE | Confirmed | Low | PL-15 | a scoped `--walk` against the whole baseline; vm-qa:464-466 skip walks not in `--walk`. :525 compares `$OUT/walks` against the whole baseline, and frame-diff:298-300 count each baseline screen absent from the run as `MISSING ... **FAIL**`. The default ONLY includes frame-diff |
| G-26 | Medium | TRUE | Narrowed | Low | PL-23 | argv identity is the design the controls test; no hostile process is in the threat model; vm-stop:28 `if not Path(os.fsdecode(args[0])).name.startswith('qemu-system-')` checks argv[0] only. vm-stop-test:29-33 runs `argv0 'qemu-system-fixture'` with `executable=sys.executable` as an accepted case. |
| G-27 | High | TRUE | Confirmed | High | PL-05 | a missing pidfile counts as a stop, then every `vm-*.qcow2` is deleted (`vm-stop:15-17`, `vm-pair:136-137`); vm-stop:16-17 `except FileNotFoundError: return` (success). vm-pair:136-137 `stop_one a; stop_one b` then `rm -f "$DIR"/vm-*.qcow2`, and :157-158 likewise for reimage. The glob covers any vm-*.qcow2 in $DIR. |
| G-28 | Medium | TRUE | Narrowed | Low | PL-23 | a compare-then-unlink window; vm-stop:51-53 `if pidfile.read_text() != recorded: raise ...` then `pidfile.unlink()`. That is a check followed by an unlink, not one atomic step. |
| G-29 | Medium | TRUE | Confirmed | Medium | PL-05 | no rollback after a partial launch; `down` stops after guest a fails (`set -e`); vm-pair:33 `set -euo pipefail`. In :146-147, a failure in start_one b or ready_one exits with guest a still up, and there is no rollback. :167 `down) stop_one a; stop_one b`: if a fails, set -e exits before b. |
| G-30 | Medium | TRUE | Confirmed | Medium | PL-04 | `vm-qa` never tears down; the rehearsal ignores its stop's failure; vm-qa ends at :528-541 without calling `vm-pair down`. In vm-upgrade-rehearsal, the exits at :57, :62 and :144 skip the :167 teardown. :167 `./tools/vm-pair down >>"$LOG" 2>&1` does not touch `fail`, so RESULT/rc stay as they were |
| G-31 | Medium | TRUE | Narrowed | Low | PL-22 | a rule: `generic-x64-vm-testing.md:115` (on `next`) uses a raw kill; the coordinator's; generic-x64-vm-testing.md:115 `kill "$(cat /tmp/rocknix-qemu.pid)"  # stop it -- by PID, never by pattern`, while :202-207 require vm-stop's verify/pidfd/bounded wait. |
| G-32 | Medium | TRUE | Confirmed | Medium | PL-11 | SSH commands bounded only by `ConnectTimeout`; vm-qa:115 `SSH() { ssh -n ... -o ConnectTimeout=8 ...}`, with no command deadline. Loops of attempts: vm-qa:123, vm-pair:113, emulator-exit-test:145, ra-offline-test:328. vm-pair:170 `exec ssh`, emulator-exit-test:51 and ra-offlin |
| G-33 | Medium | TRUE | Confirmed | Low | PL-11 | drain and stabilisation loops without an absolute deadline; vm-visual-qa:231-237 `while True: chunk = self.sock.recv(4096)` ends only on a socket timeout (silence). :277-279 `while size != os.path.getsize(path)` has no deadline. vm-serial:47 `while self.sock.recv(65536): pass` has none eit |
| G-34 | Medium | TRUE | Confirmed | Low | PL-07 | PPM header EOF loop; single-shot reports a PNG it did not write; vm-visual-qa:444 `while not data[pos:pos+1].isspace(): pos += 1`: at EOF `b''.isspace()` is False, so the loop never ends (any EOF before four header fields). :448-449 return False for a non-P6/255 file. In shot mode, :657 `to_png |
| G-35 | Medium | TRUE | Confirmed | Low | PL-18 | VNC coverage by area; `vnc-grab.py` zero-fills on deadline; vm-visual-qa:204 `covered += rw * rh` sums rectangle areas, so overlaps count twice. vnc-grab.py:34-50 `while covered < w*h and time.time() < deadline: ... s.close(); return w, h, fb` returns a partial framebuffer with no complete |
| G-36 | Medium | TRUE | Confirmed | Medium | PL-11 | `vm-serial sh` returns 0 whatever the command did, so `vm-pair`'s key install cannot fail; vm-serial:72-73 returns `(..., True)` whenever the END marker appears, and the command's exit status is never captured (:57). For a script, :121 `... && %s %s 2>&1` drops the rc. For wait, :102/:104 use `"READY" in out` (a substri |
| G-37 | High | TRUE | Confirmed | Medium | PL-07 | joins F-08: a missing frame counts as a landed key; vm-visual-qa:342-343 `if a is None or b is None ...: return 1.0`. wait_for_change (:374) returns True when `frame_diff(...) >= CHANGED_MIN`, so a missing pre or post frame counts as a change. The run path is at :560/:577. |
| G-38 | Medium | TRUE | Narrowed | Low | PL-23 | settling is a heuristic, not causality; the design (`#125`); vm-visual-qa:559 `settle(mon.frame, timeout=PRE_KEY_TIMEOUT, ...)`: the result is discarded and `before = mon.frame()` (:560) is taken anyway. Any later change satisfies :577, with no check of the intended screen. |
| G-39 | Medium | TRUE | Confirmed | Low | PL-18 | dismissal can end on GO TO and announce the carousel; dismiss_dialogs (:396-414): starting on GO TO, `seen=[GOTO]` → B → carousel (appended) → B → GO TO, which matches `seen[:-1]` and returns while GO TO is open. The limit-exhausted and `eaten > 2` paths return without any check of w |
| G-40 | Medium | TRUE | Confirmed | Medium | PL-01 | an empty suite file or `--walk ,` gives an empty successful walk; vm-qa:87: `--walk ,` makes the loop iterate nothing, so validation is skipped. Then :465 `case ",$WALKS,"` matches no name, nothing runs, and `rc=0`. An empty suite.txt also yields rc 0. :497 `cat ...$w.steps` failures do not affe |
| G-41 | Low | PARTLY | Narrowed | Low | PL-07 | `vm-qa` passes an absolute `--outdir` (`vm-qa:498`); hand runs only; Unquoted is true: vm-visual-qa:269 `self.cmd("screendump " + path ...)`, and the walk path (:528) is not passed through abspath (only shot mode, :655). The run then continues through :531 `WARN`. Overstated: walk paths are relativ |
| G-42 | Medium | TRUE | Confirmed | Low | PL-09 | one surviving `shared.sfc` skips reseeding; vm-qa:390 `SSH 'test -f /storage/roms/snes/shared.sfc' && return 0` also skips the `cloud-test-backend reset/seed` at :397-398. suite.txt:77 default-pre does not sign out of RetroAchievements, while to-manage-cloud-storage.steps:7 |
| G-43 | High | TRUE | Confirmed | Medium | PL-09 | any active remote is accepted and the match walk presses YES (`match-dialog.steps:19-26`); re-graded from High: the guests are QA-only by D-QA-016; vm-qa:306 `[ -n "$(SSH "$ACTIVE_READER" ...)" ] && return 0` accepts any active remote, with no QA-ownership check. suite.txt:82 match-dialog presses YES on the match (match-dialog.steps:19-26), and :89-90 are the run-transfer wal |
| G-44 | Medium | TRUE | Confirmed | Low | PL-09 | the manager fixture overwrites named ROMs and saves; vm-qa:376: the sentinel `test -f` fails, so :379 runs `head -c 4096 /dev/urandom > /storage/roms/$f` over the named ROMs and states, and :386 runs `touch -d ... /storage/roms/savestates/*/* /storage/roms/screenshots/* /storage/rom |
| G-45 | High | TRUE | Narrowed | Medium | PL-23 | the callers derive the three endpoints from one guest letter (`vm-qa:105-110`); a hand run's mismatch is a lead; ra-offline-test:94-98 take `--host/--port/--identity/--monitor/--serial` independently. The preconditions (:146-157) check that each one answers, not that they are the same guest. time-to-play:1027 `Guest(...)` and :1124 `Frames(a |
| G-46 | Medium | TRUE | Narrowed | Low | PL-23 | guest-side pattern kills on a disposable QA guest; a lead; signin-memory:105 `kill $(cat /tmp/signin-memory.pid) ...; pkill -x WebKitWebProces; pkill -x WebKitNetworkPr`. emulator-exit-test:113 `pkill -TERM -f '^/usr/bin/retroarch'`. ra-offline-test:233 `pkill -f ^/usr/bin/retroarch`. All |
| G-47 | Medium | TRUE | Confirmed | Low | PL-18 | stale shared logs; oldest-name match without start time; signin-memory:85 discards the launch `ssh(...)` result. `/tmp/sm-page` is not cleared beforehand, and :104 greps the shared `/tmp/signin-memory.log`. :91 matches every process whose comm matches. es-launch-memory:76 `pgrep -o --`  |
| G-48 | Low | TRUE | Narrowed | Low | PL-23 | growth, not peak, is the documented bound; es-launch-memory:153-159: `baseline, last = rows[args.warmup], rows[-1]`, and the pass condition is `last - baseline < max`. Intermediate rows are never bounded. |
| G-49 | Medium | TRUE | Confirmed | Low | PL-03 | C clears the marker before D asserts its absence; emulator-exit-test:185, part C: `... rm -f /tmp/xprobe /tmp/exit-window /tmp/.process-kill-requested; ...`. Part D (:192-194) then asserts `test ! -e /tmp/.process-kill-requested`. `--only D` runs no launch first. |
| G-50 | High | TRUE | Confirmed | Medium | PL-12 | account set on `127.0.0.1` with the default key whatever `--host`; re-graded from High: opt-in, QA accounts only; ra-offline-test:241/:243/:259 call `"$ROOT/tools/qa-accounts" "$PORT" ra\|clear` and pass neither HOST nor KEY. qa-accounts:52 `KEY="${QA_KEY:-/tmp/rocknix-vm-pair/qa-key}"` and :59-60 `root@127.0.0.1`. |
| G-51 | High | TRUE | Confirmed | Medium | PL-12 | no EXIT trap; cleanup's failures do not count; ra-offline-test has no `trap` (grep finds none). cleanup (:231-251) runs commands whose failures never reach `check`/FAILS, and :248 always prints `account cleared`. :240-241 re-provision the QA account (`qa-accounts ... ra`), not |
| G-52 | Medium | TRUE | Narrowed | Low | PL-23 | one QA account across guests; an opt-in suite one lane runs; The shared account is sourced from ACCOUNTS (:69, :163-165). earned() (:199-206) and the final check (:512-516) take no lock on the account or the achievement. |
| G-53 | Medium | TRUE | Confirmed | Low | PL-06 | host `/tmp` files with predictable names; :345 `printf ... > /tmp/ra-offline-dismiss.steps` then `rm -f` at :347 (a fixed shared path). :259 `> /tmp/ra-offline-acct.$$` (predictable name, no exclusive create). |
| G-54 | Medium | TRUE | Confirmed | Medium | PL-12 | a failed read passes a negative check; :269 `check "$(S 'netstat ... \| grep -q ...'; [ $? != 0 ]; echo $?)"` and :392, the same `[ $? != 0 ]` pattern. ssh's 255 counts as "absent". |
| G-55 | Medium | TRUE | Confirmed | Low | PL-12 | a missing achievement reads unearned; `flushed=10` matches 1; :205 `if .Achievements[$id].DateEarned then ... else "0" end` returns "0" (unearned) when the ID is missing. :479 `case "$fl" in *"flushed=1"*)` is a substring match, so `flushed=10` matches. |
| G-56 | Medium | TRUE | Confirmed | Low | PL-12 | `--control` only; :518 relaunches and polls for RetroArch without checking that it appeared, and exec.log is not removed before the relaunch (the only `rm` is at :340). :519 `grep -m1` can read the first launch's line. Note: a PASS is reachable onl |
| G-57 | Medium | TRUE | Confirmed | Low | PL-12 | two capture failures discarded; :459 `frames_after_exit exit-offline &` and :461 `wait` with no status (discarded). :523 `frames_after_exit exit-online` is unchecked. Only the reconnect capture is checked (:496-498). |
| G-58 | Medium | TRUE | Confirmed | Low | PL-18 | read-back checks non-empty, not equal; qa-accounts:112 `[ -n "$(get_setting $k)" ] && printf "%s " "$k"` checks the value is non-empty, not that it equals what was requested. :114 echoes `global.retroachievements=1` with no read-back. :155/:158 check ScreenScraper name |
| G-59 | High | TRUE | Confirmed | Medium | PL-13 | for `device-act` (the whole command is logged, `:39`); the other channels are leads under the same item; device-act:38 logs `cmd=%q "$CMD"`. signin-memory:109 puts the full `"url": url` and `"page": page` in the JSON (text mode strips the query, :115). The ra-offline-test:136 mask `'passw\|pass=\|pass:\|token=\|key='` misses `tok |
| G-60 | High | TRUE | Confirmed | Medium | PL-13 | logging failure does not stop the act; `recorded` printed regardless; device-act:35 `mkdir -p`, :38 and :42 `printf ... >> "$LOG"` are all unchecked (`set -u` only). :39 runs the command anyway, and :43 always prints `recorded in $LOG`. |
| G-61 | Low | TRUE | Narrowed | Low | PL-13 | the timeout's wording; device-act:39 `timeout "${DEVICE_ACT_TIMEOUT:-30}" ssh ...` kills only the local ssh (with `-n`, no tty), while the header (:10) says `The command is killed`. Nothing touches the remote process tree. |
| G-62 | Medium | TRUE | Confirmed | Low | PL-18 | an empty or off-image rectangle succeeds; png-blackout:69-71: a rectangle that is empty or off the image paints nothing, yet :78 prints `painted out`. :75 copies `tEXt`/`iTXt`/`zTXt` into the output. |
| G-63 | Medium | TRUE | Confirmed | Low | PL-18 | unreadable current sources skipped; es-untranslated:75-78 `except OSError: continue` skips unreadable files silently. :139-140 refuse an empty upstream source, but :143 `src = source_strings(a.es_src)` has no such guard, so an empty current source gives 0 fork strin |
| G-64 | Medium | TRUE | Confirmed | Low | PL-18 | fuzzy and context translations count; parse_po (:42) skips every `#` line, `#, fuzzy` included. A `msgctxt` sets mode "other" (:53-54), and the following msgid/msgstr is stored under the bare msgid, so a fuzzy or context-only msgstr counts as French. |
| G-65 | Medium | TRUE | Confirmed | Low | PL-18 | source substitution not verified; es-syntax-check:133 `sed -E "s#-c [^ ]+\.(cpp\|cc\|cxx)( \|\$)#-c ${abs} #..."`: nothing checks that the substitution happened (a quoted path or an @rsp file is left as it was). The farm's `cp -rs` (:89), `mkdir`/`ln -sfn` (:95 |
| G-66 | Medium | TRUE | Confirmed | Medium | PL-14 | `0 -> 0` backups pass; hashes, not sizes; vm-upgrade-rehearsal:96 runs `backuptool backup >/dev/null 2>&1` with the status unchecked. :97 BK0 counts files, and :154 compares counts only (0 → 0 passes). :73 counts hash lines (`grep -c '^[0-9a-f]\{64\} '` = 4), with no size |
| G-67 | Medium | TRUE | Confirmed | Low | PL-18 | the collector asserts before recording the event; raofflineproxy-consent-test:173-175 (`json.loads`/`assert`) and :180-183 run before `events.append(event)` (:186). A raise there leaves no event, and :210-213 compare the observed events with `expected=[]` for a declined case. |
| G-68 | Low | TRUE | Confirmed | Low | PL-18 | a bare-list response raises; ra-candidate-games:145 `listing.get("Results", listing if isinstance(listing, list) else [])`: the `.get` lookup on a list raises AttributeError before the fallback argument can apply. |
| G-69 | Low | TRUE | Narrowed | Low | PL-23 | measurement quality, no acceptance PASS; font-stems:174 `range(int(lo), int(hi)+1)`: a reversed range is empty, sizes=[] and rc 0. :114-115 `if ft.FT_Load_Char(...): continue` drops failed glyphs silently. :214-223 return 0. |
| G-70 | Medium | TRUE | Confirmed | Low | PL-08 | joins F-05: no new boot identity required; vm-qa:476-477 `systemctl reboot; sleep 6` then `pgrep -x emulationstation`. time-to-play:381-391 `sleep(8)`, `wait_alive` and `es_up`. ra-offline-test:188-189 `sleep 8` then pgrep. None of these compares the boot_id. |
| G-71 | Low | TRUE | Confirmed | Low | PL-17 | the report's minutes leave out bring-up (Q5 corrected); vm-qa:144-146 time only the command run_suite runs. The backend start (:118), the pair up (:119-122), ensure_remote (:341) and ensure_fixture/manager_fixture (:427-428) are untimed, and the `started` stamp (:139) comes after the p |
| G-72 | Low | TRUE | Narrowed | Low | PL-22 | rules: `vm-first.md:59` says four suites; the coordinator's; next:.claude/rules/vm-first.md:59 `` `tools/vm-qa` the runner with its four suites ``. vm-qa:63 SUITES lists 17 names. vm-qa:530-531 `No budget row exists yet, so nothing here fails the run`, while time-to-play:1293 `EXIT_SYNC_BUD |

### The seat's refutations of the first reader

| F | The seat | The lane's response |
| --- | --- | --- |
| F-01 | Agree, Medium; narrow to the exit code | Accepted. The four other suites did prove; the exit is the defect. Merged with G-01 and G-40 into PL-01. |
| F-02 | Agree, Low; narrow "nothing" | Accepted. Startup and conditions can still run. Joined by G-08, G-09, G-10 and G-12 into PL-02, now Medium. |
| F-03 | Agree, Low; effects still run | Accepted. With G-49, PL-03. |
| F-04 | Agree, Medium for the manager guard; narrow the class | Accepted. PL-10 is Medium for `vm-manager-system-check`; the class is listed, not graded. |
| F-05 | Agree with the fall-through, not with an unconditional PASS | Accepted. With G-70, PL-08. |
| F-06 | Agree, Medium | Accepted, re-graded Medium. With G-42, G-43 and G-44, PL-09. |
| F-07 | Agree, Low, a scope-reporting gap | Accepted. PL-16. |
| F-08 | Agree, Medium | Accepted, re-graded Medium. With G-37, G-34 and G-41, PL-07. |
| F-09 | Agree, Medium; the raw image is temporary | Accepted. The raw image is removed after conversion (`vm-pair:145`). The about-6-GB figure is the peak during `up`. PL-06. |
| F-10 | Agree, High on the shared default; the cycle did not use it | Accepted. `02`'s cell said "the cycle used it", meaning the isolation, and is corrected to "the cycle set both overrides by hand". Kept Medium in PL-06, because a High defect of the same class is G-27's disk deletion in PL-05. |
| F-11 | Agree; the root's absence is only reported | The lane ran `ls` on the host (`00` § Stage B): absent. Stands. |
| F-12 | Agree, Low | Accepted. PL-17. |
| F-13 | Narrow: the index is not in the packet | The lane read the index from `next` (`q7-descriptions.txt`). Stands as a lead, PL-22. |
| F-14 | Narrow to "no current operational caller found" | Accepted as the wording. PL-19. |
| F-15 | Narrow to the tested image | Accepted: "refuses on the image tested, `069fc2704421`; no recipe at the hash installs the binary". PL-19. |
| F-16 | Narrow: `exit` has a recorded positive | Accepted. `04` § Q6 and `02` now read "no catch; one recorded positive". PL-19. |
| F-17 | Agree, with G-30 and G-71 making the cost larger | Accepted. PL-20. |
| F-18 | Agree; narrow: a whole-frame claim cannot waive a size change or a missing frame | Accepted. PL-15. |
| F-19 | Agree, Low; quantity from `du` | Accepted (the lane's `du`). PL-20. |
| F-20 | Agree, Low; `ra-offline-test:67`'s override is for ROM inputs | Accepted. PL-21. |

**The Q3, Q5 and Q6 corrections the seat made,** applied in this file:
- ten suites under 3 seconds, not nine;
- the "host" column's meaning under a default run;
- `ra-offline`'s guest is a by default;
- #361 is `raofflineproxy-integration-test`'s origin, not a catch (`02`);
- the missing constructed inputs it listed are now items: G-01, G-07, G-03, G-63, G-56 and G-66.

### What the seat could not judge

As its § 3 says: the record's history (the 61 reports, the catches and the caller searches), which the packet summarises; the external tools the suites call; pixels and claim approvals; the full default run; and the image's digest. That digest was checked by the lane with `sha256sum -c`.
