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

**The cost table.** Minutes are medians from the 59 distinct reports (P4), with the cycle's figure where it ran. "Host" is what the suite holds while it runs. "Cadence" is from `vm-qa:64` and `release-candidates.md` step 3.

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
| ra-offline | none in any report; standalone 4 to 5.7 | guest d, serial, the QA account | opt-in (0 runs in `vm-qa`) |
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
- Nine suites take under 3 seconds each.
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
| exit | **nothing recorded** | the debounce-stripped copy, `6b95a93d2f` | `vm-qa`; rule command |
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

At stage C.
