# Forward audit — M6.P2 T12, the VM harness (#659)

The 60 paths are read at `8ebaf8daad`'s bytes. The lens is cost against value (brief § 2), and the questions are plan § 4's Q1 to Q7. Line numbers are at the hash unless a row says otherwise.

## Phase 2: #659's checklist at stage B

| # | Criterion (abridged) | State at stage B | Artifact |
| --- | --- | --- | --- |
| 1 | the folder with `00` to `05` | `00` to `04` in progress; `05` at stage D | this folder |
| 2 | the lint `PASS` | before stage D, `--phase pre-issue` | stage C |
| 3 | `review-plan.json`, provenance, and the packet scanned | at stage C | `second-opinions/` |
| 4 | every item at a Phase 7 outcome | stage F | `05` |
| 5 | `reviewed-at` and `fixed-at` | `reviewed-at` `facb2ae523` (`00`) | #659's body at close |
| 6 | `01` § Scope | written | `01` |
| 7 | the coverage table, 60 rows | written below | § Coverage |
| 8 | § The controls | written below | § The controls |
| 9 | § The guest cycle | written below; the cycle was accepted on #659 at 19:33 | § The guest cycle |
| 10 | `00` shows nothing never-run | the cycle, the probes and the deviation are recorded | `00` |
| 11 | Q5's cost table | `04` § Q5 | `04` |
| 12 | Q6's value table | `04` § Q6 | `04` |
| 13 | Q3 hunted per suite | `04` § Q3 | `04` |
| 14 | Q7's three descriptions | `04` § Q7 | `04` |
| 15 | every proof with its class cell | below; equal to `00`'s PROOF count | § Proofs |
| 16 | `question:` on every item; no `tools/` change before a brief | stage D; `git diff --stat facb2ae523 HEAD -- tools` is empty | `05` |
| 17 | the retro, the checkers | stages G and H | — |

## Mechanical checks

| Check | Command | Exit | Summary |
| --- | --- | ---: | --- |
| Membership | brief § 2's block over `docs/reviews/inventory.json` | 0 | `paths 60 lines 8790`, 60 fork-own, reach `n/a` 60; 20 Python, 10 shell, 22 `.steps`, 3 text, 2 Markdown, 3 PNG |
| Lines at the hash | `git show 8ebaf8daad:<p> \| wc -l`, summed | 0 | 8,813, the 23 newline bytes in the PNGs included |
| Bytes | `git cat-file -s`, summed | 0 | 484,627 |
| Provenance | `git cat-file -e upstream/next:<p>`; `git log c445081a59..8ebaf8daad -- <the 60>` | 0 | 0 of 60 upstream; 145 commits (144 without merges) |
| Branch against hash | `git diff --stat 8ebaf8daad HEAD -- <the 60>` | 0 | empty |
| Find/stop by pattern | § 5's `pgrep\|pkill\|kill` grep over eight tools | 0 | 41 lines, all guest-side (P3) |
| `/tmp` roots | § 5's `/tmp/` grep over the 60 | 0 | 84 lines; the host-side ones are F-09 and the Q1 rows |
| Legacy paths | `git grep` for `rocknix.worktrees` or `/workspace/repos/rocknix` in the 60 | 0 | one: `es-syntax-check:53` (F-11, #640) |
| `assert` as a check | `git grep -c '^\s*assert '` over the Python | 0 | 7 tools (F-04's class) |
| Claims reconciliation | `/workspace/tmp/m6-t12/walks-reconcile.txt` | 0 | P5 |
| Q7 descriptions | `/workspace/tmp/m6-t12/q7-descriptions.txt` | 0 | the owning rule names 17 of 30; the index points six more at it (F-13) |
| Host versions | `qemu-system-x86_64 --version`; `python3 --version` | 0 | QEMU 10.2.1; Python 3.14.4 |

## The controls

Run at stage A in this worktree, 19:05:45 to 19:05:46 UTC, census 0 before and after. The logs are in `.qa-scratch/t12/controls/`.

| Control | Exit | Summary | A FAIL would mean |
| --- | ---: | --- | --- |
| `python3 -I tools/vm-pair-test` | 0 | `PASS 9 VM launch controls` | `vm-pair` could claim a guest up without its own PID owning its disk, or a launch failure could read as up |
| `python3 -I tools/vm-upgrade-readiness-test` | 0 | `PASS 7 storage-readiness controls` | the rehearsal's wait could accept a guest whose storage is not ready in the expected boot |
| `python3 -I tools/vm-stop-test` | 0 | `PASS 7 vm-stop controls` | `vm-stop` could signal a process that is not the owned QEMU, or report a stop before the exit |
| `./tools/vm-manager-system-check --help` | 1 | `FAIL manager system: not enough values to unpack` | (no `--help`; it fails closed, which is correct) |
| `./tools/raofflineproxy-integration-test --help` | 0 | the usage | (a usage line; not a test run) |
| `./tools/vm-qa --list` | 0 | 17 names | a suite added to or dropped from `SUITES` without the list moving |
| `./tools/time-to-play --help` | 0 | the usage | (a usage line) |
| `./tools/frame-diff --help` | 0 | the usage | (a usage line) |
| `./tools/vm-visual-qa --help` | 0 | the usage | (a usage line) |
| `./tools/vm-pair` | 2 | the usage | (a usage line) |
| `./tools/es-syntax-check` | 2 | `name at least one .cpp` | **not a pass**: it exits 2 without a build root, and its default root is absent (F-11) |
| `.githooks/hooks-test` | — | not run at stage A | (criterion 17's checker, at close) |

## The guest cycle

The one authorized cycle, 19:23 to 19:30 UTC; the full record is in `00` § The guest cycle and `cycle/`.

- **The image:** `069fc2704421`, sha256 `6b4c3079bdee2f47bd1149aac07b11714c591b847f22157fcd6d85f39a7e08fb`, read from the `.img.gz.sha256` sidecar, since the `.identity.json` carries no digest (criterion 9 was edited on #659 at 19:33).
- **The guest and the host:** one guest; pidfile `/workspace/tmp/m6-t12/cycle/rocknix-qemu.pid`; census 0 before and after. The host file's lines at 19:23:39Z and 19:30:19Z are quoted in `00`.
- **The run:** `vm-qa --skip-up --only fresh,round-trip,exit,time-to-play,frame-diff`, rc 0 in 3 min 6 s. Minutes per suite, against the record's medians (P4):

| Suite | This cycle | The record's median |
| --- | ---: | ---: |
| fresh | 1 s | 0 s |
| round-trip | 84 s | 84.5 s |
| exit | 27 s | 28 s |
| time-to-play | 72 s | 69 s |
| frame-diff | SKIP, 0 s | 1 s |

- **The verdict:** `**PASSED with 1 suite(s) SKIPPED**`, rc 0.
- **Time to play:** 0.74 / 1.59 / 1.01 s.
- **The probes:** `time-to-play --repeat 0` rc 0 (P8); `emulator-exit-test --only X` rc 0 (P9).
- **The stop:** `tools/vm-stop` rc 0 in 0.25 s.
- **Retired:** the disk (sha256 `230153933c0d…`) and the image copy (`cycle/RETIRED.txt`). No frame is kept: none is needed by a claim.

## The record

**The vm-qa reports** (P4; re-derived in `/workspace/tmp/m6-t12/q5-rederived.txt`; the research helper's per-report tables are in `/workspace/tmp/m6-t12/research-q5.md`):
- **Count:** 61 reports whose first line is `# vm-qa on`, in 27 folders under `docs/qa-logs/`. Two pairs are byte-identical, so there are 59 distinct runs, from 2026-10-03 to 10-15.
- **Full 15-suite runs:** 19, median 33 min (28 to 35).
- **`docs/vm-qa-log.md`:** 44 September run windows, median 25 min; its October rows carry no durations.
- **`time-to-play.log` files:** 16, in 13 folders.

**The value side** (`04` § Q6): read by a second helper and spot-checked by the lane (`00`).

## Proofs

| # | Claim | Evidence | Class |
| --- | --- | --- | --- |
| P1 | The 60 equal the brief at `8ebaf8daad`, and the branch's diff over them is empty | `.qa-scratch/t12/membership.txt`, `lines-at-hash.txt` | proved: tree |
| P2 | The three controls pass; `vm-qa --list` gives 17; `es-syntax-check` exits 2 without a root | `.qa-scratch/t12/controls/` | proved: tool-run |
| P3 | Every `pgrep`, `pkill` and `kill` in the eight guest-touching tools is guest-side; `vm-pair down` stops through `vm-stop` | `controls/kill-grep.txt`; `vm-pair:124-130` | proved: tree |
| P4 | The 61 reports' per-suite seconds and verdicts (59 distinct runs) | `/workspace/tmp/m6-t12/q5-rederived.txt` | proved: history |
| P5 | The claims reconciliation: no orphan claim and no unowned walk; 8 step files outside `suite.txt`; every key checked | `walks-reconcile.txt`, `steps-profile.txt` | proved: tree |
| P6 | `vm-manager-system-check` passes under `PYTHONOPTIMIZE=1` what it refuses without it | `.qa-scratch/t12/probes/manager-check-optimize.txt` | proved: tool-run |
| P7 | `vm-qa` exits 0 over a SKIP | `cycle/vm-qa/report.md`, `cycle/t-vmqa.txt` | proved: guest |
| P8 | `time-to-play --repeat 0` exits 0 with every headline cell empty | `cycle/ttp-repeat0/time-to-play.json` | proved: guest |
| P9 | `emulator-exit-test --only X` prints `PASSED` with no check run | `cycle/exit-onlyX.out` | proved: guest |
| P10 | The image ships no `cloud_migrate_layout`, so `migration-protocol.sh` refuses | `cycle/guest-checks.txt` | proved: guest |
| P11 | `vm-stop` stops the owned QEMU in 0.25 s; the guest held 2.54 GiB resident on the host | `cycle/guest-checks.txt`; `00` | proved: guest |
| S1 | `vm-qa`: a SKIP exits 3; an unknown or empty selection exits 2; `--help` is whole; the report root is checked before the guest; two runs get two directories (#966, #982). Seven `vm-harness-test` cases fail at `facb2ae523` and pass at `3c0b9d53c6`; the directory claim passed there by luck, corrected below | `streams/s1-unfixed.txt`, `streams/s1-fixed.txt` | proved: fix-case |
| S1-claim | The report directory's claim is an O_EXCL file, because this host's mkdir (uutils 0.10.0) answers 0 to two racing calls; `report-dir-claimed` and `two-runs-one-minute` fail at `facb2ae523` and `3c0b9d53c6` and pass at `fc8754b29b` | `streams/s1-claim-correction.txt` | proved: fix-case |
| S2 | `vm-qa` reads `down` and `up`, compares the guest's BUILD_ID with the image's build, takes the pair down at the end; `fresh` reads the selected port (#969, #981). Four cases fail at `facb2ae523` and pass at `813e4dd270` | `streams/s2-unfixed.txt`, `streams/s2-fixed.txt` | proved: fix-case |
| S3 | The walks need a new boot id and an answering interface, a checked seeding, the QA cloud as the active remote and a manifest; the ES suites judge only the pinned source (#973, #974, #981). Seven cases fail at `facb2ae523` and pass at `ca0bf841d2` | `streams/s3-unfixed.txt`, `streams/s3-fixed.txt` | proved: fix-case |
| S4 | `vm-pair` refuses to remove a held disk, rolls a partial `up` back and `down` stops both; `vm-stop` exits 3 on a missing pidfile and keeps a replaced one (#970). Five cases fail at `facb2ae523` and pass at `eddd21d7a2` | `streams/s4-unfixed.txt`, `streams/s4-fixed.txt` | proved: fix-case |
| S5 | The pair's state, the runtime directory, the QA cloud's state and the run's scratch belong to the checkout; held ports are refused; the rehearsal reads `ROCKNIX_ARTIFACTS` (#971, #979; D-INFRA-031). Five cases fail at `facb2ae523` and pass at `f1331aba83` | `streams/s5-unfixed.txt`, `streams/s5-fixed.txt` | proved: fix-case |
| S6 | `time-to-play` refuses `--repeat 0` and an empty `--only`, times the exit sync only on a completed stamp, needs g2g's stamp, judges every cell that ran, and fails an unread panel (#967, #983; D-QA-062). Six cases fail at `facb2ae523` and pass at `a09bfc5718` | `streams/s6-unfixed.txt`, `streams/s6-fixed.txt` | proved: fix-case |
| S7 | `emulator-exit-test` takes only parts A to D and refuses D alone; `device-act` acts only with its BEGIN written, fails on a lost END, and masks the command in its log (#968, #978). Five cases fail at `facb2ae523` and pass at `c1569b7bc6` | `streams/s7-unfixed.txt`, `streams/s7-fixed.txt` | proved: fix-case |

## The streams' positives

Each stream's `vm-harness-test` case, run against the unfixed tool (`git archive facb2ae523 tools`, through `--tools-from`) and then against the fix. The quotes are the control's own lines.

| Stream | Case | Unfixed (`facb2ae523`) | Fixed |
| --- | --- | --- | --- |
| S1 | `exit-skip` | `rc 0, SKIP row True` | `rc 3, SKIP row True` (`0ecbbb9339`) |
| S1 | `only-unknown` | `rc 0, stderr ''` | `rc 2, stderr 'vm-qa: unknown suite nosuch (vm-qa --list names them)'` |
| S1 | `only-empty` | `rc 0` | `rc 2` |
| S1 | `walk-empty` | `rc 0` | `rc 2` |
| S1 | `help-whole` | `missing from --help: ['link', 'ra-offline', 'walks', 'frame-diff']` | `missing from --help: []` (`3c0b9d53c6`) |
| S1 | `report-unwritable` | `rc 1, guest calls 3` | `rc 1, guest calls 0` |
| S1 | `two-runs-one-minute` | `1 report directories` | `2 report directories` |
| S1 | `two-runs-one-minute`, from `fc8754b29b` (3 runs at once, 5 rounds) | `round 0: 1 directories, 1 distinct reports; ...`; at `3c0b9d53c6`: `round 0: 2 directories, 2 distinct reports` | `5 rounds of 3 concurrent runs, 3 directories and 3 reports each` |
| S1 | `report-dir-claimed` (an mkdir double answering as this host's did) | `report in qa-...-2111`; at `3c0b9d53c6`: `report in qa-...-211154` | `report in qa-...-211154-2` (`fc8754b29b`) |
| S2 | `up-fails-guest-answers` | `rc 0, green report True` | `rc 1, green report False`, stderr `... exited 1; nothing was judged` (`9df1c65c68`) |
| S2 | `build-id-mismatch` | `rc 0, stderr ''` | `rc 1`, stderr `... is build fedcba987654: another guest answered` |
| S2 | `down-at-end` | `vm-pair calls ['down', 'up'], tear-down line False` | `vm-pair calls ['down', 'up', 'down'], tear-down line True` |
| S2 | `fresh-port` | `5 fresh reads at ports ['10022']` | `5 fresh reads at ports ['10023']` (`813e4dd270`) |
| S3 | `reboot-same-boot-id` | `rc 0, walked 1` | `rc 1, walked 0, "no new boot" in walks.log True` (`a68bfadcd5`) |
| S3 | `reboot-es-silent` | `rc 0, walked 1` | `rc 1, walked 0, the reason in walks.log True` |
| S3 | `seed-scp-fails` | `rc 0, walked 1` | `rc 1, walked 0, the copy failure in walks.log True` (`5edb265e59`) |
| S3 | `remote-not-qa` | `rc 0, walked 1` | `rc 1, walked 0, seeded 0, refusal in walks.log True, stand-in value leaked False` |
| S3 | `reseed-manifest` | `seed-device calls 0, manifest written False` | `seed-device calls 1, manifest written True, walked 1` |
| S3 | `overwrite-refused` | `copies 1, cloud resets 1, walked 1, named False` | `rc 1, copies 0, cloud resets 0, walked 0, named True` |
| S3 | `es-src-mismatch` | `rc 0, SKIP row with both hashes False, check ran True` | `rc 3, SKIP row with both hashes True, check ran False` (`ca0bf841d2`) |
| S4 | `disk-held-no-pidfile` (vm-pair-test) | `rc 9, disk kept False, holder named False` | `rc 1, disk kept True, holder named True` (`33b1bb8845`) |
| S4 | `partial-up-rollback` (vm-pair-test) | `rc 9, guest a started True, still running True` | `rc 9, guest a started True, still running False` |
| S4 | `down-stops-both` (vm-pair-test) | `rc 1, guest b stopped False` | `rc 1, guest b stopped True` |
| S4 | `missing-pidfile-exit-3` (vm-stop-test) | `rc 0` | `exits 3, says nothing was stopped, removes nothing` (`eddd21d7a2`) |
| S4 | `pidfile-changed-under-us` (vm-stop-test) | `returncode=0`, `down: owned QEMU exited`, the replaced pidfile removed | `reports a pidfile replaced during the stop and keeps it` |
| S5 | `two-checkouts-two-states` | `paths shared by the two checkouts ['/tmp/rocknix-qemu-monitor-b.sock', ...]` | `paths shared by the two checkouts [], paths under /tmp []` (`3f5998bbaf`) |
| S5 | `runtime-recorded` | `up rc 0, RUNTIME recorded ''` | `up rc 0, recorded True, down rc 0, guests 2, still running 0` |
| S5 | `port-held-refused` | `rc 0, launches 2, holder named False` | `rc 1, launches 0, holder named True` |
| S5 | `no-tmp-writes` | `aimed at /tmp: ['/tmp/', '/tmp/rocknix-vm-pair/qa-key']` | `2 temp files asked for, ... aimed at /tmp: []` (`373a366e40`) |
| S5 | `rehearsal-artifacts-root` | `/workspace/artifacts/rocknix-images/qa-0123456789-upgrade-from-previous-...` | under the case's `ROCKNIX_ARTIFACTS` (`f1331aba83`) |
| S6 | `repeat-zero` | `rc 1, ['OSError: AF_UNIX path too long']` (ran on into the guest; P8 is rc 0 on one) | `rc 2, --repeat must be at least 1, not 0` (`7c5d15b2d8`) |
| S6 | `only-empty-cells` | `rc 1`, ran on into the guest | `rc 2, --only names no cell` |
| S6 | `sync-stamp-failed` | `judged [], over budget ["... took 9.00 s ..."]` | `an exit sync's stamp did not complete (rc 5, YOUR_CLOUD_STOPPED_ANSWERING)`, over budget `[]` |
| S6 | `g2g-no-stamp` | `judged []` | `a game-to-game row has no exit sync stamp` |
| S6 | `cell-ran-unmeasured` | `judged []` | each of launch, exit and g2g named |
| S6 | `scaled-none` | `judged []` | `... could not be compared with the panel ...` (`a09bfc5718`) |
| S7 | `exit-only-unknown` | `rc 0, ['PASSED'], guest calls 17` | `rc 2, guest calls 0` (`00b8760457`) |
| S7 | `exit-only-d-alone` | `rc 0, ['PASSED']` | `rc 2` (D runs only beside A, B or C) |
| S7 | `act-begin-unwritable` | `rc 0, the act reached the fixture 1 time(s)` | `rc 2, ... 0 time(s), ssh calls 0` (`c1569b7bc6`) |
| S7 | `act-end-fails` | `rc 0, "recorded nothing" said False` | `rc 1, "recorded nothing" said True` |
| S7 | `act-masked` | `stand-in in the log True` | `key=*** in the log True, stand-in in the log False` |

S1's files: `streams/s1-unfixed.txt` (0 PASS, 7 FAIL) and `streams/s1-fixed.txt` (7 PASS, 0 FAIL). The claim correction: `streams/s1-claim-correction.txt`. S2's: `streams/s2-unfixed.txt` (0 PASS, 4 FAIL) and `streams/s2-fixed.txt` (4 PASS, 0 FAIL); the whole control, `streams/s1-s2-full.txt` (12 PASS). S3's: `streams/s3-unfixed.txt` (0 PASS, 7 FAIL) and `streams/s3-fixed.txt` (7 PASS, 0 FAIL); the whole control, `streams/s1-s3-full.txt` (19 PASS). S4's: `streams/s4-unfixed.txt` and `streams/s4-fixed.txt` (vm-pair-test and vm-stop-test, rc 0). S5's: `streams/s5-unfixed.txt` (0 PASS, 5 FAIL) and `streams/s5-fixed.txt` (5 PASS); every control after S5, `streams/s1-s5-full.txt`. S6's: `streams/s6-unfixed.txt` (0 PASS, 6 FAIL) and `streams/s6-fixed.txt` (6 PASS). S7's: `streams/s7-unfixed.txt` (0 PASS, 5 FAIL) and `streams/s7-fixed.txt` (5 PASS). `rules-check --quiet` rc 0 and `hooks-test` PASS after `ea2377f1ce`.

## Findings (stage B)

Severity and the punch list come at stage D. The coordinator's 19:33 reading makes F-01, F-02 and F-03 stage-D bugs, with their inputs.

| ID | Q | Finding | Where | Proof |
| --- | --- | --- | --- | --- |
| F-01 | Q3 | `vm-qa` exits 0 when a suite SKIPs: a run that has not passed reads green to a caller (`frame-diff` with no baseline; `scripts` with skipped checks, which exits 3) | `vm-qa:141-148`, `:528`, `:541` | P7 |
| F-02 | Q3 | `time-to-play` passes with nothing measured when `--repeat` is below 1 or `--only` names no headline cell: blindspot 39's shape, reachable outside `--quick` | `time-to-play:994-996`, `:1306-1332` | P8 |
| F-03 | Q3 | `emulator-exit-test --only` with none of A to D runs no check and prints `PASSED` | `emulator-exit-test:38`, `:145-196` | P9 |
| F-04 | Q2/Q3 | `vm-manager-system-check`'s refusals are `assert` statements, stripped by `-O` or `PYTHONOPTIMIZE`; six more tools, mostly controls, check with `assert` | `vm-manager-system-check:12-15` | P6 |
| F-05 | Q3 | After `systemctl reboot` the walks' wait for EmulationStation falls through after 45 tries without failing, and the walk runs anyway | `vm-qa:476-477` | tree |
| F-06 | Q2 | The walks' fixture seeding is unchecked: `reset` and `seed-content` go to `/dev/null` with no exit check, and `ensure_remote`'s return is ignored | `vm-qa:389`, `:397-398`, `:408`, `:341` | tree |
| F-07 | Q3 | `register` passes having checked less when the EmulationStation checkout is absent (its log says so) | `vm-qa:210-212` | tree |
| F-08 | Q3 | A failed screendump only warns, so a walk that captured no frame exits 0; `frame-diff` catches it only when a baseline exists | `vm-visual-qa:524-530` | tree |
| F-09 | Q1/Q2/Q5 | `vm-pair up` keeps the raw image and two qcow2 disks under `/tmp/rocknix-vm-pair` by default, on this host a 31 GB RAM tmpfs (about 6 GB per `up`); the key, sockets and pidfiles default to `/tmp` too | `vm-pair:37`, `:137-145`; `vm-qa:98-99` | tree; host `findmnt` |
| F-10 | Q2/Q6 | The QA cloud's state `~/.cache/rocknix-cloud-qa` is per user, so shared with the M7 lane, and the walks `reset` it; isolation exists (`CLOUD_QA_STATE`, `CLOUD_QA_PORT`) but nothing sets it | `vm-qa:397`; `cloud-test-backend:93` | tree (the cycle set both overrides by hand) |
| F-11 | Q1 | `es-syntax-check`'s default build root is the legacy `rocknix.worktrees` path, absent on the host (#640) | `es-syntax-check:53` | tree |
| F-12 | Q7 | `vm-qa --help` prints lines 5 to 38, cutting the descriptions of `link`, `ra-offline`, `walks` and `frame-diff` | `vm-qa:81` | tree |
| F-13 | Q7 | The index points six tools at `generic-x64-vm-testing.md`, which never names them (`png-blackout`, `vm-pair-test`, `signin-memory`, `es-launch-memory`, `ra-candidate-games`, `raofflineproxy-integration-test`); the three walk scripts have no index row | `instruction-files.md` on `next` | `q7-descriptions.txt` |
| F-14 | Q6 | Five tools nobody runs: `ra-candidate-games`, `es-launch-memory` and `signin-memory` have index mentions only; `font-stems` and `raofflineproxy-installed-native-test` have descriptive paragraphs only | `04` § Q6 | research, re-derived for the three |
| F-15 | Q6 | `vm-walks/cloud-epic/migration-protocol.sh` serves a retired migration and refuses on every current image | `:9-12`; `rasteratops-vm-cloud-epic:149` | P10 |
| F-16 | Q6 | Suites with no recorded catch of a product defect: `exit` (no catch; one recorded positive), `wrapper` (none of its own), and `lifetime`, `pair-identity`, `time-to-play` and `ra-offline` (only their own failures) | `04` § Q6 | research, spot-checked |
| F-17 | Q5 | Cost concentrates: `walks` (16.7 min) and `scripts` (13.0 min) are about 90 % of a 33-minute default run; the default holds the pair (2 × 8 GiB) for the whole run while only `pair-identity` needs guest b | `vm-qa:119-122`, `:270` | P4 |
| F-18 | Q3 | All 391 claims are against `d72084ccad`'s baseline (2026-09-26), a month older than the newest image; three whole-frame claims exempt `manager-gb`'s first three screens while it stands | `claims.txt:38-40` | P5 |
| F-19 | Q5 | `frame-diff accept` keeps every previous baseline and nothing retires them (six kept, about 70 MB) | `frame-diff:399-403` | host `du` |
| F-20 | Q2 | `vm-upgrade-rehearsal` writes under `/workspace/artifacts` whatever `ROCKNIX_ARTIFACTS` says; `vm-qa` and `ra-offline-test` honour it | `vm-upgrade-rehearsal:30` | tree |

## Coverage

One row per path, at the hash. The Q columns answer plan § 4. `n/a` means the question does not apply to that kind of file. For a `.steps` file, Q2 counts its checked keys, Q5 its shots, Q6 who replays it, and Q7 whether a claim owns its frames.

| Path | Lines | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `tools/device-act` | 44 | log default under `/workspace/artifacts` | records boot id before and after | read only (D-QA-015) | bash | not run | rule instruction `engineering-practices.md:814-815` (on `next`) | index points to `engineering-practices.md` |
| `tools/emulator-exit-test` | 196 | none | `set -u`; checks fail closed on no answer | `--only` naming no part passes (P9) F-03 | bash | 28 s median (P4), 27 s on the cycle | called by `vm-qa` (`:296`); rule command; nothing recorded as a catch (`04` § Q6) | agree |
| `tools/es-launch-memory` | 166 | none | validates cycles and both bounds (`:39-42`) | none: bounds required for acceptance | host Python | 7.0 min for 50 cycles (research) | **nobody**: index only (F-16); caught #310 | the owning rule never names it F-13 |
| `tools/es-syntax-check` | 153 | default build root a legacy path (`:53`), absent F-11 | rc 2 without a root: not a pass (P2) | none | bash | seconds with a root | rule instruction (`es-native-ui.md`); blindspot 49 | index points to `es-native-ui.md` |
| `tools/es-untranslated` | 159 | ES_SRC default exists | rc 2 when it cannot read | none constructed | host Python | 0-1 s (P4) | `vm-qa` french (`:188`); caught #152 | the owning rule never names it (index points to `es-native-ui.md`) |
| `tools/font-stems` | 227 | none | host FreeType | not run | host Python | not recorded | **nobody** runs it: descriptive mention only (F-16); blindspot 54 | agree |
| `tools/frame-diff` | 433 | none | missing claims or masks read as empty (strict) | no baseline rc 2 (vm-qa SKIP); MISSING and size change FAIL; three whole-frame claims F-19 | host Python stdlib | 1-2 s per compare (P4); `accept` keeps every old baseline, 6 kept (~70 MB) F-20 | called by `vm-qa` (`:525`); `release-candidates.md` step 3; 5 FAIL rows in the record (`04` § Q6) | agree |
| `tools/png-blackout` | 81 | none | refuses unsupported PNGs | none | host Python stdlib | not recorded | `developer-relations/SKILL.md:175`; `vm-walks/docs/README.md:20` | the owning rule never names it F-13 |
| `tools/qa-accounts` | 159 | `~/.ROCKNIX/qa-accounts` | prints no value (read, never run) | read only | bash | not run | `ra-offline-test:259`; D-QA-016 | agree |
| `tools/ra-candidate-games` | 223 | none | read-only | not run | host Python | not recorded | **nobody**: index only (F-16) | the owning rule never names it; the index points there F-13 |
| `tools/ra-offline-test` | 524 | defaults under `/tmp` (`:65-66`); host `/tmp/ra-offline-acct.$$` (`:259`), `.steps` (`:345`) | `FAILS` with cleanup (`:287` ...) | preconditions FAIL when missing; not run here (opt-in, spends an achievement) | bash | 5.7 min and about 4 min standalone (research); never in a `vm-qa` report | opt-in in `vm-qa` (`:358`); `release-candidates.md` step 3; blindspot 50 | agree |
| `tools/ra-ui-test` | 225 | none | asserts as checks (F-04 class) | fixture-only; not run | host Python | 7.7-8.6 min, 4 runs (research) | rule mention only; #465 | agree |
| `tools/raofflineproxy-consent-test` | 230 | none | asserts as checks (F-04 class) | not run | host Python | 0.8 min with a guest boot (research) | caught #457 (`04` § Q6) | agree |
| `tools/raofflineproxy-installed-native-test` | 70 | none | refuses any skip (`:59-69`) | not run | host Python | not recorded | **nobody** runs it: a descriptive rule paragraph only (F-16) | agree |
| `tools/raofflineproxy-integration-test` | 247 | none | `unittest` result | needs an unpacked proxy; not run | host Python | 0.3 min (research) | `release-candidates.md` proxy proof; #361 is its origin, not a catch (nothing recorded) | the owning rule never names it F-13 |
| `tools/signin-memory` | 129 | reads `/tmp/signin-memory.*` on the guest only | exits 1 on each FAIL (`:120-125`) | none constructed | host Python | 1.4-1.5 min standalone (research) | **nobody**: index only (F-16); decided D-WORKFLOW-038 | the owning rule never names it F-13 |
| `tools/time-to-play` | 1593 | host `/tmp/ttp-cm-<pid>` control socket (`:158`) | `headline_missing`, `over_budget` (`:1268-1283`) | `--repeat 0` or an `--only` with no headline cell passes measuring nothing (P8) F-02 | host Python | 69 s median as a suite (P4), 72 s on the cycle | called by `vm-qa` (`:342`); `time-to-play.md`; blindspots 39, 54, 55, 56, 74 | agree |
| `tools/vm-manager-system-check` | 19 | none | `assert` as the check (`:12-15`) F-04 | passes under `PYTHONOPTIMIZE=1` (P6) F-04; no `--help` (rc 1, fail closed) | host Python | milliseconds | called by `vm-qa` (`:483`) for manager walks | agree |
| `tools/vm-pair` | 185 | `DIR` default `/tmp/rocknix-vm-pair` (`:37`), a RAM tmpfs here F-09 | `set -euo pipefail`; PID verified against its disk (`:81-95`) | stop by `vm-stop` (pidfile, disk) (`:124-130`): no pattern; P3 | QEMU 10.2.1 host, `qemu-img` | two 8 GiB guests and about 6 GB of `/tmp` per `up` (P4, P11) F-09 | called by `vm-qa` (`:120-121`), `vm-upgrade-rehearsal`; `vm-pair-test` its control; recorded in blindspot 41 | header matches the code |
| `tools/vm-pair-test` | 75 | none | asserts as checks (F-04 class) | controlled launch failures, 9 cases (P2) | host Python | seconds, host only | **fork CI** `fork-checks.yml:47` | the owning rule never names it; the index points there F-13 |
| `tools/vm-qa` | 541 | host `/tmp` defaults for key, sockets, pidfiles (`:98-99`); ES_SRC default exists at the pin | `set -u`, no `pipefail`; fixture seeding unchecked (`:389`, `:397-398`, `:408`) F-06 | exits 0 over a SKIP (`:541`) F-01, P7; walks wait falls through (`:477`) F-05; `register` checks less without ES (`:210-212`) F-07 | bash only | one default run: median 33 min, the pair held throughout (P4) F-18 | callers: rules (`release-candidates.md` step 3, `generic-x64-vm-testing.md`); no CI; value per suite in `04` § Q6 | `--help` prints `:5-38` only, cutting four suites F-12; header list equals `SUITES` |
| `tools/vm-serial` | 133 | none | socket client; rc 2 on a bad call | `wait --up-to` bounded | host Python | 15 s to serial on the cycle | called by `vm-pair` (`:108`, `:110`, `:181`), `ra-offline-test:116`, `cloud-round-trip:240`; rule command `generic-x64-vm-testing.md:112-114` | agree |
| `tools/vm-stop` | 77 | none | pidfd, identity re-check, bounded wait; fail closed | timeout keeps the pidfile, rc 1, no escalation: loud; none constructed | Python 3.14 host (`pidfd_open` 3.9+) | 0.25 s on the cycle (P11) | called by `vm-pair` (`:129`); control `vm-stop-test` 7 PASS (P2) | three descriptions agree |
| `tools/vm-stop-test` | 66 | none | asserts as checks (F-04 class) | constructs delayed exit, timeout, wrong disk, wrong process | host Python | seconds, host only | not in CI; rule names it (`generic-x64-vm-testing.md`) | agree |
| `tools/vm-upgrade-readiness-test` | 87 | none | asserts as checks (F-04 class) | synthetic states, 7 cases (P2) | host Python | seconds, host only | **fork CI** `fork-checks.yml:48`; called by `last-good-scripts-test` | agree |
| `tools/vm-upgrade-rehearsal` | 170 | none | `RESULT PASS|FAIL`, exits `$fail` | fail closed on each piece | bash | 96-159 s, 19 runs (research) | `release-candidates.md` step 3; `upgrade-and-install.md` | output root ignores `ROCKNIX_ARTIFACTS` (`:30`) F-21 |
| `tools/vm-visual-qa` | 677 | none | a failed screendump only warns (`:524-530`) F-08 | eaten key: re-send then exit 3 (`:587-671`); frames missing pass F-08 | host Python stdlib | the walks suite median 1,000 s (P4) | called by `vm-qa` walks (`:498`), `ra-offline-test:346`, `es-launch-memory` | agree |
| `tools/vm-walks/README.md` | 194 | `/tmp` monitor path in its example | n/a | n/a | n/a | n/a | read by people | describes `settle` and `wait-for-change` as the code does |
| `tools/vm-walks/back-up-page.steps` | 8 | n/a | 1 keys, 1 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `back-up-page`, `continue-to-systems`, `run-transfer`, `run-transfer-frames`, `tick-game-content`, `tick-roms`, `tick-settings` | claims via its walks (P5) |
| `tools/vm-walks/claims.txt` | 564 | n/a | n/a | 391 claims, all against `d72084ccad`; three whole-frame (`:38-40`) F-19 | n/a | n/a | read by `frame-diff` (`vm-qa:525`); every claim matches a walk (P5) | n/a |
| `tools/vm-walks/cloud-epic/migration-protocol.sh` | 165 | needs `cloud_migrate_layout`, absent from the image (P10) | refuses rc 2 before any write (`:9-12`) | refuses on every current image | n/a | not reached | sourced by `rasteratops-vm-cloud-epic:149` only; dead on current images F-15 | no index row |
| `tools/vm-walks/cloud-epic/vnc-grab.py` | 83 | none | stdlib RFB | n/a | host Python | not recorded | `rasteratops-vm-cloud-epic:67` | no index row |
| `tools/vm-walks/confirm-cloud-folder.steps` | 13 | n/a | 2 keys, 2 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `confirm-cloud-folder` | claims via its walks (P5) |
| `tools/vm-walks/continue-to-systems.steps` | 21 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `continue-to-systems`, `run-transfer`, `run-transfer-frames` | claims via its walks (P5) |
| `tools/vm-walks/docs/README.md` | 22 | n/a | n/a | n/a | n/a | n/a | read by people (#323) | agrees with the four `docs/*.steps` |
| `tools/vm-walks/docs/cloud-sync.steps` | 84 | n/a | 28 keys, 28 `wait-for-change` | every key is checked (P5) | n/a | 4 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/docs/main-menu-up-probe.steps` | 22 | n/a | 5 keys, 5 `wait-for-change` | every key is checked (P5) | n/a | 6 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/docs/networking.steps` | 79 | n/a | 22 keys, 22 `wait-for-change` | every key is checked (P5) | n/a | 5 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/docs/retro-achievements.steps` | 69 | n/a | 22 keys, 22 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by hand for rocknix.org (#323); no `vm-qa` caller | no claim (not a suite walk) |
| `tools/vm-walks/fixtures/arcade-vertical-raw-left.png` | 8 | n/a | n/a | n/a | n/a | n/a | copied by `vm-qa` (`:382`, `:385`); the #288 session control | n/a |
| `tools/vm-walks/fixtures/gb-160x144.png` | 3 | n/a | n/a | n/a | n/a | n/a | copied by `vm-qa` (`:381`, `:384`) for the manager walks; #243 | n/a |
| `tools/vm-walks/fixtures/nes-256x240-right.png` | 12 | n/a | n/a | n/a | n/a | n/a | copied by `vm-qa` (`:380`, `:383`); the #288 session control | n/a |
| `tools/vm-walks/fixtures/system-selected.sh` | 3 | none | writes one guest file | n/a | n/a | milliseconds | installed by `vm-qa` (`:473`) for manager walks | no index row (fixture) |
| `tools/vm-walks/m7-cloud-sync.steps` | 52 | n/a | 17 keys, 17 `wait-for-change` | every key is checked (P5) | n/a | 6 shot(s) | replayed by hand (M7); no `suite.txt` walk | no claim (not a suite walk) |
| `tools/vm-walks/m7-retro-achievements.steps` | 36 | n/a | 11 keys, 11 `wait-for-change` | every key is checked (P5) | n/a | 4 shot(s) | replayed by hand (M7); no `suite.txt` walk | no claim (not a suite walk) |
| `tools/vm-walks/manager.steps` | 33 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 5 shot(s) | replayed by `vm-qa` walks: `manager-fbn`, `manager-gb`, `manager-nes` | claims via its walks (P5) |
| `tools/vm-walks/masks.txt` | 12 | n/a | n/a | 7 masks, each explained | n/a | n/a | read by `frame-diff` | n/a |
| `tools/vm-walks/match-dialog.steps` | 26 | n/a | 4 keys, 4 `wait-for-change` | every key is checked (P5) | n/a | 3 shot(s) | replayed by `vm-qa` walks: `match-dialog` | claims via its walks (P5) |
| `tools/vm-walks/reset.steps` | 18 | n/a | 0 keys, 0 `wait-for-change` | every key is checked (P5) | n/a | 0 shot(s) | a utility leg; no `suite.txt` walk | no claim (not a suite walk) |
| `tools/vm-walks/restore-page.steps` | 12 | n/a | 2 keys, 2 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `restore-page` | claims via its walks (P5) |
| `tools/vm-walks/run-transfer-frames.steps` | 60 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 17 shot(s) | replayed by `vm-qa` walks: `run-transfer-frames` | claims via its walks (P5) |
| `tools/vm-walks/run-transfer.steps` | 58 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 3 shot(s) | replayed by `vm-qa` walks: `run-transfer` | claims via its walks (P5) |
| `tools/vm-walks/suite.txt` | 100 | n/a | n/a | 16 walks (brief: 17) and `default-pre` | n/a | n/a | read by `vm-qa` walks (`:437`) | comments match the compositions |
| `tools/vm-walks/tick-game-content.steps` | 15 | n/a | 5 keys, 5 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `tick-game-content` | claims via its walks (P5) |
| `tools/vm-walks/tick-roms.steps` | 16 | n/a | 3 keys, 3 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `continue-to-systems`, `run-transfer`, `run-transfer-frames`, `tick-roms` | claims via its walks (P5) |
| `tools/vm-walks/tick-settings.steps` | 21 | n/a | 7 keys, 7 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `tick-settings` | claims via its walks (P5) |
| `tools/vm-walks/to-change-cloud-folder.steps` | 39 | n/a | 9 keys, 9 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `confirm-cloud-folder`, `to-change-cloud-folder` | claims via its walks (P5) |
| `tools/vm-walks/to-manage-cloud-storage.steps` | 28 | n/a | 6 keys, 6 `wait-for-change` | every key is checked (P5) | n/a | 1 shot(s) | replayed by `vm-qa` walks: `back-up-page`, `confirm-cloud-folder`, `continue-to-systems`, `match-dialog`, `restore-page`, `run-transfer`, `run-transfer-frames`, `tick-game-content`, `tick-roms`, `tick-settings`, `to-change-cloud-folder`, `to-manage-cloud-storage` | claims via its walks (P5) |
| `tools/vm-walks/ui-settings-toggle.steps` | 41 | n/a | 7 keys, 7 `wait-for-change` | every key is checked (P5) | n/a | 2 shot(s) | replayed by `vm-qa` walks: `ui-settings-toggle` | claims via its walks (P5) |
| `tools/vm-walks/wake.steps` | 7 | n/a | 0 keys, 0 `wait-for-change` | every key is checked (P5) | n/a | 0 shot(s) | a utility leg; no `suite.txt` walk | no claim (not a suite walk) |
