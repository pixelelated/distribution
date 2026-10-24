# Forward audit: M6.P2 T14, the last-good, settings and state tests (#661)

Read at `8ebaf8daad` (the 22) and `2174265e9c` (the ten lint fixtures); `reviewed-at` is `30da4853bb`.

## Phase 2: #661's checklist

| # | Criterion (#661 body, brief § 7) | State at stage B | Where |
| ---: | --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00`, `01`, `02` exist | this folder |
| 2 | the lint prints `PASS` (pre-issue before D, default at close) | not yet run | `00` |
| 3 | `review-plan.json`, the seat's provenance, the packet's scan | not yet | `second-opinions/` |
| 4 | the punch-list issue's items all at an outcome | stage D onward | — |
| 5 | `reviewed-at` and `fixed-at` in #661's body | `reviewed-at` known (`30da4853bb`); written at hand-back | #661 |
| 6 | `01` § Scope | done | `01-research-notes.md` |
| 7 | the coverage table, 32 rows | stage B | § Coverage |
| 8 | § The runs | done for stage A | § The runs |
| 9 | § The guest cycle | no cycle so far | § The guest cycle |
| 10 | `00` shows none of the never-run actions | so far | `00` |
| 11 | `04` Q6's brittleness table | stage B | `04` |
| 12 | `04` Q3's hunt | stage B | `04` |
| 13 | `04` Q7's descriptions | stage B | `04` |
| 14 | `04` Q5's costs | the stage-A walls recorded | § The runs, `04` |
| 15 | every proof with its proof-kind cell; the counts equal | running | § Proofs |
| 16 | `question:` on every item; the bugs pass `box-check --issue`; no tool edited before a stream | stage D onward | `05` |
| 17 | the retro | stage G | — |
| 18 | the six checkers and the lint at hand-back | stage H | — |

## The runs

Every run is in this worktree with `TMPDIR=/workspace/tmp/m6-t14/tmp`, except the two marked as run with `TMPDIR` unset. Each output is in `.qa-scratch/t14/`, and each exit is in `00` § Stage A.

| Run | Exit | Wall | Summary | A FAIL would mean |
| --- | ---: | ---: | --- | --- |
| `tools/wait-lock-test` | 0 | 7.5 s | `PASSED` | `wait_lock()` in `001-functions` waited past its bound, returned success without the lock, or let a second holder in |
| `tools/rocknix-info-test` | 0 | 0.5 s | `PASS 12 full-script positive/negative controls` | a hardware reading printed when its source was absent, or a quirk failure reported as a value |
| `tools/nova-led-test` | 0 | 0.2 s | `14 PASS, 0 FAIL` | an LED node, the saved brightness or the battery writer misbehaving under the real scripts |
| `usb-gadget-test --output ...` | 0 | 0.3 s | `18 cases, 72/72 checks` | a USB descriptor identity (`bcdDevice`, D-WORKFLOW-160) or a mode link wrong after preparation |
| `pixelelated-state-check-test --self-test` | 0 | 9.1 s | `status: pass`, 183 controls | the state check accepted a contaminated root, or disclosed a value |
| `pixelelated-state-check-test --payload-tests` | CANNOT | — | `mcopy` is absent on this host (`mksquashfs`, `unsquashfs` and `sfdisk` are present) | — |
| `build-identity-test --output ...` | **1** | 0.2 s | 21 passed, 2 failed: the state-check gate refuses the firmware stand-in | this is the FAIL. A product defect would show as an identity block or a plan that no longer carries the version, timestamp or source; here the test's own input is refused |
| `retroarch-wrapper-test <source>` | 0 | 0.1 s | `PASS: every command ran exactly once` (the source is the M7 root `m7-pixelelated-replacement20`'s `retroarch-bdba046fa...`) | the threaded video wrapper ran a posted command twice or not at all |
| `retroarch-wrapper-test` (bare) | 2 | — | no source given and none under #640's roots | — (cannot run; not a verdict) |
| `rasteratops-identity-check --tree <wt> --es <ES clone at the pin>` | **1** | 0.1 s | 38 PASS, 1 FAIL `ES licence matches its source` | this is the FAIL. It expects `MIT`, and the recipe says `MIT AND BSD-3-Clause` since `84ff94fb3d` |
| `settings-modes-test`, a build root's applets (BusyBox 1.36.1 from `m7-pixelelated-replacement20`, image `BUILD_ID 1a026648442321609b2288c2c9c06803817f9df2`; the effective pin is 1.36.1) | 0 | 0.4 s | `PASS refuse-rename` | a shell settings writer lost a file's private mode or published a failed staging file under the image's applets |
| `settings-modes-test`, the host's applets (BusyBox 1.37.0, Ubuntu): **a PASS of the host** | 0 | 0.4 s | `PASS refuse-rename` | the same, under the host's applets |
| `melonds-upgrade-test`, a build root's applets | 0 | 0.1 s | `PASS temp-failure` | post-update erased an owner's melonDS setting or added a hotkey non-atomically |
| `melonds-upgrade-test`, the host's applets: **a PASS of the host** | 0 | 0.1 s | `PASS temp-failure` | the same, under the host's applets |
| `rasteratops-cloud-layout-test` without `--archives-only` | 1 | 0.1 s | it refuses: the migration matrix was retired by #508 | — (a usage refusal) |
| `rasteratops-cloud-layout-test --archives-only`, `TMPDIR` set | **1** | 9.2 s | 11 PASS, 2 FAIL (`T24-local-*-recovery`): the sandbox inherits `TMPDIR` | this is the FAIL, and it is the test's (`00` § Stage B, trace 1) |
| the same, `TMPDIR` unset | 0 | 19.8 s | 13 PASS, 0 FAIL | an archive selected, written or read wrongly, or a missing remote not refused |
| `pixelelated-cloud-validator-test --rclone <image rclone 1.75.2>` | **1** | 0.1 s | it refuses: `Use the package-pinned rclone1.75.1` | this is the FAIL: the hardcoded version is stale against the pin |
| `pixelelated-content-scope-test` (`TMPDIR` set, and again unset) | **1** | 3.4 s / 3.3 s | 19 PASS, 2 FAIL (`system-traversal-refused`, `content-pointer-traversal-refused`) | this is the FAIL, and it is the test's (`00` § Stage B, trace 2) |
| `pixelelated-save-layout-test` (a build root's busybox) | 0 | 29.2 s | `39 PASS, 0 FAIL` | a standalone emulator's save path missing from the save coverage, or swept into a library transfer |
| `pixelelated-duckstation-capture-test` | **1** | 0.1 s | it refuses: `use package-pinned rclone` (1.75.1 hardcoded) | this is the FAIL: the same stale version |
| `tools/pixelelated-cloud-folder-test` | 2 | — | `Retired historical folder-contract control (#524 PL-002).` | — (a refusal by design) |
| `tools/pixelelated-cloud-folder-vm-test` | 2 | — | `Retired historical folder-overlay control (#524 PL-002).` | — (a refusal by design) |
| `tools/rasteratops-vm-cloud-epic` (bare) | 2 | — | `This migration suite is retired. ...` | — (a refusal) |
| `--help` of the other eight | 0 each | — | usage only | — |

**The three greps:**
- **`|| true`:** 0 lines in the 21 tools.
- **`^\s*assert `:** `nova-led-test` 1 and `pixelelated-vm-cloud-boundaries` 1.
- **Host paths:** 28 lines in 10 files (`.qa-scratch/t14/hostpaths.txt`).

## T15's call sites (read, not edited)

`tools/last-good-scripts-test` (T15's slice) calls four of these tools:

- `rasteratops-cloud-layout-test`, at `:252` (`--cloud-layout` execs it) and `:14175-14189` (`--output`, `--source-root`, `--rclone "${SA_RCLONE_SRC}"`, and `--archives-only` once `MIGRATION_AVAILABLE=0`);
- `settings-modes-test`, at `:14224`, with `TMPDIR="${TMP}"`, `--busybox "${BB_HOST}"`;
- `melonds-upgrade-test`, at `:14231`, the same way;
- `wait-lock-test`'s functions, lifted the same way at `:148` and `:8608`; the tool itself is not invoked.

**For T15 (#662, through the coordinator):** `image_tool_source` (`:381-400`) looks for a build root's binary and otherwise ends in `command -v "${name}" || true`. So with no root, it hands the host's busybox or rclone to every callee, which accept it. The run prints the busybox's source (`:426`), but no verdict marks the result as the host's.

**The recorded runs used build roots:**
- `docs/qa-logs/2026-10-08-pixelelated-replacement-18/qa21/.../scripts.log:3` and `2026-10-04-pixelelated-57cbc-qualification/qa-07/.../scripts.log:3` show `BusyBox v1.36.1 ... a copy of /workspace/repos/rocknix.worktrees/m7-pixelelated-replacement...`.
- Their cloud-layout sections pass: `13 PASS, 0 FAIL` (2026-10-08) and `316 PASS, 0 FAIL` (2026-10-04, migration still available).
- Their artifacts are under `/tmp/cloud-layout-*`, so `vm-qa` ran T15 without a `TMPDIR` that would leak into the sandbox.

## Coverage

One row per path. The Q cells are short; `04` carries the evidence for each.

| Path | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 (who reads it; what it caught) | Q7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tools/build-identity-test` | current | no assert; refusals accept any nonzero (F-01) | fails at the hash: the state gate refuses its stand-in (F-01) | n/a: no package | 0.2 s, fails early | nobody; caught nothing recorded beyond its harness (§ Q6) | row names `device-builds.md`, which names it |
| `tools/melonds-upgrade-test` | current | shims cover every external; no assert | accepts any busybox (F-13) | busybox 1.36.1 pin vs the applets given | 0.1 s | T15 `:14231`; #526's 15 old FAILs | `upgrade-and-install.md` never names it (F-12) |
| `tools/nova-led-test` | current | one assert on ledcontrol's exit (F-07) | `-O` drops `:50` (F-07) | n/a | 0.2 s | nobody; #332's run | `generic-x64-vm-testing.md` never names it (F-12) |
| `tools/pixelelated-cloud-folder-test` | a retired stub kept in place (F-10) | refuses before work | docstring names stale rclone 1.75.1 as current coverage (F-03) | n/a | 0 s | nobody, by design; disposition proposed | row says *refuses execution*: matches; list entry carries no note (F-12) |
| `tools/pixelelated-cloud-folder-vm-test` | a retired stub kept in place (F-10) | refuses before work | n/a: refuses | n/a | 0 s | nobody, by design; disposition proposed | row says *refuses execution*: matches; `generic-x64-vm-testing.md` never names it |
| `tools/pixelelated-cloud-validator-test` | rclone 1.75.1 hardcoded (F-03) | no `--clearenv` in its sandbox (F-04) | fails at the hash (F-03); empty `--case` false PASS (F-06) | rclone 1.75.1 against the pin 1.75.2 | 0.1 s, refused | nobody; `2026-10-07-cloud-validator` root-old01 | `rclone-cloud-sync.md` never names it |
| `tools/pixelelated-content-scope-test` | current | inherits the caller's environment (F-04) | fails at the hash: a stale `argv` read (F-05) | rclone required, unversioned | 3.3 s | nobody; `2026-10-07-cloud-validator/content-scope` | `rclone-cloud-sync.md` never names it |
| `tools/pixelelated-duckstation-capture-test` | rclone 1.75.1 hardcoded (F-03) | payload runs on the host (F-14); no `--clearenv` | fails at the hash (F-03); `--cases` drops unknown names | rclone 1.75.1 against 1.75.2 | 0.1 s, refused | nobody; `2026-10-08-save-repair-cases/duckstation-captures/old02` | `rclone-cloud-sync.md` never names it |
| `tools/pixelelated-save-layout-test` | current | `--unshare-net`; no `--clearenv` | without `--busybox`, the host's applets unmarked (F-13) | rclone required; busybox optional | 29.2 s | nobody; `2026-10-08-save-repair-cases/coverage` | `rclone-cloud-sync.md` names it |
| `tools/pixelelated-state-check` | current | fails closed on every missing reader | none found (fails closed) | the host's readers | n/a (run by its test) | `fork-publish-release`; no contamination caught recorded | `release-candidates.md` never names it |
| `tools/pixelelated-state-check-test` | current | `control_count` unasserted | expected-2 cases pass on any error | `mcopy` absent here: `--payload-tests` CANNOT | 9.1 s | nobody; `2026-10-13-clean-state-runtime` pix565 | `release-candidates.md` never names it |
| `tools/pixelelated-vm-cloud-boundaries` | a retired migration suite in place (F-10) | one assert; stops by `/proc` scan (F-09) | refuses at the hash (F-10) | n/a | refuses at once | nobody; `2026-10-06-...replacement-15` | row describes a suite that refuses every run (F-10) |
| `tools/rasteratops-candidate-store` | current | no assert | `verify` proves self-consistency only | n/a | n/a (not run for real) | `fork-publish-release`; candidate-store.log's constructed corruption | `release-candidates.md` never names it |
| `tools/rasteratops-cloud-layout-test` | the migration matrix retired (#508) | sandbox passes the caller's env (F-04) | false FAIL under a caller's `TMPDIR` (F-04) | rclone printed, not asserted | 19.8 s | T15 `:14188`; partial-retry-host01 | `rclone-cloud-sync.md` never names it |
| `tools/rasteratops-identity-check` | current | `check(True, ...)` cannot fail (F-15) | fails at the hash: the ES licence string (F-02) | n/a | 0.1 s | nobody; `2026-10-04-es-identity-export` | `release-candidates.md` never names it |
| `tools/rasteratops-vm-cloud-epic` | a retired migration suite; `/tmp` pidfile (#640) | 9 host-path lines | refuses at the hash (F-10); negated probes if it ran | n/a | refuses at once | nobody; only negative controls | row describes a suite that refuses (F-10) |
| `tools/retroarch-wrapper-test` | #640's roots (F-08) | leaves `t.c` (F-08) | `gcc` absent reads as *ran twice* (F-08) | the build root's RetroArch source, not the tree's patch | 0.1 s | `vm-qa` `wrapper`; `e5d14d4220` | `engineering-practices.md` names it |
| `tools/rocknix-info-test` | current | the verdict on `assert` (F-07) | `-O` false PASS (F-07, P4) | n/a | 0.5 s | the fork CI; #548 | `generic-x64-vm-testing.md` names it |
| `tools/settings-modes-test` | current | host `grep`/`sort`/`mktemp` from PATH | accepts any busybox (F-13); refuse-cases pass on rc 127 | busybox pin 1.36.1 vs the applets given | 0.4 s | T15 `:14224`; #421 | `generic-x64-vm-testing.md` names it |
| `tools/test-fixtures/cloud_connections_fixture.py` | current | no credential literal at rest | applied only `if hasattr(m, "connections")`; old sources skip it silently | n/a | n/a | read by `last-good-scripts-test` (`:5005`, `:11521`); fixes the connections module's paths and `config create` | the fixture's purpose is stated in its header |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/01-research-notes.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's fail case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/02-forward-audit.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's fail case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/03-retrospective.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's fail case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/04-analysis.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's fail case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/05-punch-list.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's fail case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/01-research-notes.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's pass case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/02-forward-audit.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's pass case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/03-retrospective.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's pass case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/04-analysis.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's pass case | its folder name says which case |
| `tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/05-punch-list.md` | current | n/a: Markdown fixture | n/a: a fixture, not a test | n/a | n/a | read by `lint-audit-artifacts`' fixture cases (and T10's `run.sh`, `2444828e89`); fixes the renovation face's pass case | its folder name says which case |
| `tools/usb-gadget-test` | current | the host's `/bin/sh` (F-15) | none found | n/a | 0.3 s | nobody; `2026-10-11-usb-revision` | header promises image functions, runs host `sh` (F-15) |
| `tools/wait-lock-test` | GNU `date +%s%N` unchecked | no assert | none found | n/a | 7.5 s | nobody; #98 | `generic-x64-vm-testing.md` names it |

## Mechanical checks

- **The packet scan** (brief § 5, before the seat): pending.
- **`tools/lint-audit-artifacts --phase pre-issue`:** pending, before stage D.
- **The greps:** `|| true` 0; `assert` 2 files; host paths 28 lines in 10 files (§ The runs).

## The guest cycle

**None was needed.** Both guest tests refuse before any guest on this tree, so a cycle would show only the refusal:
- `pixelelated-vm-cloud-boundaries:709-710` requires `sources/cloud_migrate_layout`;
- `rasteratops-vm-cloud-epic:22-25` refuses without it, rc 2.

`cloud_migrate_layout` is absent at `8ebaf8daad` (P6). The claims that would have needed a cycle are each classified from the source and proved from the tree:
- the boundaries test's guest start (`vm-pair up` with an owned pair directory, refusing if any `qemu-system-*` exists, `:270-276`) and stop (a `/proc` cmdline scan for the owned path, `:675-690`);
- the epic's use of a pre-existing guest's pidfile (`:48-50`).

No host file line was written, because no guest started. The census was 0 throughout.

## Proofs

| Proof | What it shows | Proved |
| --- | --- | --- |
| P1 | the membership and the two read hashes (32 paths, 6,911 lines, both diffs empty) | proved: tool-run |
| P2 | the stage-A runs: five tools fail at the hash with the package's own inputs | proved: tool-run |
| P3 | the two traces: cloud-layout's `TMPDIR` inheritance, content-scope's stale `argv` read | proved: tool-run |
| P4 | `rocknix-info-test` under `python3 -O` passes a constructed regression | proved: tool-run |
| P5 | `pixelelated-cloud-validator-test --case no-such-case` passes with 0 controls | proved: tool-run |
| P6 | the guest pair refuses every run on this tree | proved: tree |
| P7 | the no-caller tools by invocation (thirteen, then fourteen after G-15) | proved: tree |
| P8 | the index rows and their *Detail in* rules: 13 never name the tool | proved: tree |

## The streams' positives

| Stream | Case | At the stage-D tip `7aa8eac253` | Fixed | Commits |
| --- | --- | --- | --- | --- |
| S2 (#992, #999) | `docs/qa-logs/2026-10-24-state-tests-s2/sandbox-case.py`: the caller exports `TMPDIR`, `RCLONE_CONFIG`, an `RCLONE_CONFIG_QA_TYPE` remote, `BASH_ENV` and a function; a probe through `Fixture.run`; the whole `--archives-only`; a real rclone copied elsewhere through the connections fixture on a stand-in `HOME` | 9 of 10 FAIL: everything inside, `BASH_ENV` sourced, `mktemp` failing, 39 interfaces, cloud-layout 0/13, the copy admitted and the stand-in default config written | 10 of 10: nothing inside, loopback only, cloud-layout 13/13, the copy refused, nothing written, `--config` passed, the FakeSP shape intact | `2e6639ec57`, `89efee384c` |
| S1 (#989, #990) | `build-identity-test` on its own run; `docs/qa-logs/2026-10-24-state-tests-s1/identity-reasons-case.sh` (a preparer and an identity policy that refuse for a wrong reason); `identity-check-case.sh` (the tree, an empty gamelist, a shadowed `PKG_LICENSE`) | identity test rc 1, 21/2; any-non-zero credits a wrong reason (57/57); identity check FAIL / PASS / PASS | identity test rc 0, 57/57; a wrong reason fails 2 checks; identity check PASS / FAIL / FAIL | `3c9730bc78`, `648e9ca228` |
| S3 (#991, #994, #998) | the stage-A refusals and a 9.9.9 scratch recipe; `docs/qa-logs/2026-10-24-state-tests-s3/validator-controls-case.sh` (four product mutations); `--case no-such-case`; `duckstation-case.sh` (a payload that writes a host marker; a `--cases` typo) | both refuse rclone 1.75.2; the four mutations credited; `PASS 0 controls` rc 0; the payload on the host; the typo dropped | both pass with 1.75.2 (30, 31) and refuse 9.9.9; the four failed; rc 2; no host marker; rc 2 | `2f614eef1f`, `6b5cd16160`, `fe41fca9a9` |
| S4 (#993) | the tree; `docs/qa-logs/2026-10-24-state-tests-s4/scope-cases.sh` (a no-op script, an early-exit script, a `--cases` typo) | 19 PASS, 2 FAIL (the traversals); both mutations credited; the typo dropped | 21 PASS; both mutations failed; rc 2 | `6b41f05962` |
| S5 (#1004, #1005) | `docs/qa-logs/2026-10-24-state-tests-s5/layout-cases.sh` (a no-op backup; a seeder that never settles; a restore that swallows its listing failure); `save-layout-cases.sh` (a pure-rclone selection with `--busybox`; `--ref` before a current source) | each mutation credited (rc 0); both save-layout runs rc 1 | each mutation failed; both rc 0; the historical matrix 398/0 | `c25f69d19a`, `15bce9aa23` |
| S5 follow-up (#1004) | `docs/qa-logs/2026-10-24-state-tests-s5/backup-contract-cases.sh` (a backup that exits 0 silently after the faulted listing; one that copies into `/pixelelated/Saves/`) | at `c25f69d19a`, the test before the follow-up: both credited (rc 0) | both failed (no `COMPLETED`; the derived folder named); the unmutated backup passes; T18 17/0 | `ef31b4bf22` |
| S6 (#995) | `docs/qa-logs/2026-10-24-state-tests-s6/info-cases.sh` (an appended `exit 0` under `PYTHONOPTIMIZE=1`; an unadapted `/tmp/battery.percent`); `nova-cases.sh` (an EXIT trap under `PYTHONOPTIMIZE=1`; a hardcoded `LED_PATH` at a stand-in tree) | all four credited (rc 0); the stand-in's 8 files written | all four failed, the pattern or line named; no stand-in file written | `359dd435ce`, `081f19d2f0` |
| S6 follow-up (#995) | `docs/qa-logs/2026-10-24-state-tests-s6/info-cleanup-case.sh` (a failing run and a passing run, each with a fresh `TMPDIR`) | at `359dd435ce`: the failing run leaves its scratch | nothing left after either | `84a2b73140` |
| S7 (#996) | `docs/qa-logs/2026-10-24-state-tests-s7/wrapper-cases.sh` (a `send_packet` that keeps the first method; the plain copy; no `gcc`; SIGTERM mid-build; the bare run) | the mutation credited (rc 0, total 2000); `t.c` left; rc 1 without `gcc`; the scratch left when killed | per-site FAIL (site 1 ran 0 times); nothing left; rc 2 naming `gcc`; nothing left when killed; rc 2 with the usage line | `0037b04172` |
| S8 (#997) | `docs/qa-logs/2026-10-24-state-tests-s8/settings-cases.sh` (the host busybox; `--unverified-busybox`; the build root's; a stand-in root; a TMPDIR with a space; a `settings_base` using `cat --squeeze-blank`); `melonds-cases.sh` (host, unverified, root, stand-in, declared) | the host busybox passes both as the candidate's (29/29, 15/15), no origin recorded; the GNU-only writer 29/29; the space 5/24 | the host refused (exit 2); exit 3 with every line marked; the BUILD_ID or origin in each receipt; the GNU-only writer 13/16; the space 29/29 | `929355c417`, `30d9339ea3` |
| S9 #1000 | `docs/qa-logs/2026-10-24-state-tests-s9/ready-cases.sh` with `ready-probe.py` (`/usr/bin/autostart` as another command's argument; the shipped wrapper; a tree whose unit drifted) | at `4e94ccd833`: the argument passes the ExecStart check; the drifted unit passes the test (183) | refused at `runs_autostart`; the wrapper passes; the drifted unit fails the test, the restored tree passes (190) | `3657e0e801` |
| S9 #1001 | `control-cases.sh` (a gate whose `text()` crashes on a NUL; a deleted `case("clean-image")` registration) | at `3657e0e801`: both pass (190, 189) | both rc 2; the plain pair 190 | `b74dcaa78b` |
| S9 #1002 | `store-cases.sh` (a symlink named for bundle A pointing at bundle B, in a scratch store) | verifies, rc 0 | refused, rc 1, naming both; B verifies by its own path | `64ea405f3f` |
| S9 PL-17 | `scratch-cases.sh` (SIGTERM while a synthetic update tar's SYSTEM is in the scratch) | at `b74dcaa78b`: rc 143, the scratch left | rc 2, the error JSON, nothing left | `a5397e2e9f` |
| S10 (#1003) | `docs/qa-logs/2026-10-24-state-tests-s10/lock-cases.sh` (a `wait_lock` that returns 1 after taking the lock; check-then-create in place of `ln -T`, a 0.1 s sleep in the window; the tree's file under the image busybox) | both mutations PASSED | 7 and 2 checks fail; the turns overlap; the tree's file PASSED under BusyBox 1.36.1 | `bcf5a013ad` |
| S11 #1011 | `docs/qa-logs/2026-10-24-state-tests-s11/pair-cases.sh` with `cleanup-probe.py` (a disposable `qemu-system-fixture` beside a refused start; a started run's cleanup with a pidfile naming an invisible pid) | the fixture signalled, `all_absent: True`; `all_absent: true` from no pidfile | the fixture alive, no `all_absent`, the derived runtime uncreated; an `observation_error`, no `vm-pair down` | `6016f57a75` |
| S11 PL-10 | `grep -c '1.75.1'` over the two cloud-folder stubs | 1 | 0; `--help` rc 0, a run rc 2 | `8816d078fa` |
| S12 PL-23 | `docs/qa-logs/2026-10-24-state-tests-s12/fixture-cases.sh` (the coupled fail fixture; two split fixtures; each with its guard disabled in a scratch lint) | the coupled fixture names both failures in one run | each split fixture names exactly one, and passes with only its own guard disabled | `7679426e48` |
| S2 follow-up (#999) | `sandbox-case.py`'s two new checks (a shim's argv; a T15-shaped shim reading `$1 $2`) | at `89efee384c`'s fixture: argv `--config <stage> listremotes`, no refusal | `listremotes --config <stage>`; the create refused | `9df25309f3` |

| Proof | What it shows | Proved |
| --- | --- | --- |
| P9 | S2's control fails at the stage-D tip and passes fixed | proved: fix-case |
| P10 | S1's controls fail at the stage-D tip and pass fixed | proved: fix-case |
| P11 | S3's controls fail at the stage-D tip and pass fixed | proved: fix-case |
| P12 | S4's control fails at the stage-D tip and passes fixed | proved: fix-case |
| P13 | S5's controls fail at the stage-D tip and pass fixed | proved: fix-case |
| P14 | S6's controls fail at the stage-D tip and pass fixed | proved: fix-case |
| P15 | S5's follow-up control fails before the follow-up and passes after it | proved: fix-case |
| P16 | S7's control fails at the stage-D tip and passes fixed | proved: fix-case |
| P17 | S6's cleanup control fails before the follow-up and passes after it | proved: fix-case |
| P18 | S8's controls fail at the stage-D tip and pass fixed | proved: fix-case |
| P19 | #1000's control fails before the fix and passes after it | proved: fix-case |
| P20 | #1001's control fails before the fix and passes after it | proved: fix-case |
| P21 | #1002's control fails at the stage-D tip and passes fixed | proved: fix-case |
| P22 | PL-17's control fails before the fix and passes after it | proved: fix-case |
| P23 | S10's control fails at the stage-D tip and passes fixed | proved: fix-case |
| P24 | #1011's control fails before the fix and passes after it | proved: fix-case |
| P25 | the stubs' stale version count goes 1 to 0 | proved: fix-case |
| P26 | S12's split fixtures each prove one guard | proved: fix-case |
| P27 | the fixture follow-up's two checks fail on 89efee384c's fixture and pass at 9df25309f3 | proved: fix-case |

**The busybox this host offers (S8, for reading the record):** `readlink -f $(command -v busybox)` is `/usr/bin/busybox`, `BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1)`. The image's is the M7 root `m7-pixelelated-replacement20`'s `image/system/usr/bin/busybox`, `BusyBox v1.36.1`, BUILD_ID `1a026648442321609b2288c2c9c06803817f9df2`, 182 applets, every one but `sh` a busybox link on the image. The record's earlier `settings-modes-test` and `melonds-upgrade-test` passes name no busybox; from `929355c417` and `30d9339ea3` on, each receipt carries `busybox_origin`.

## The suites at the fixed tip

Every one of the 21 tools, at `b968264c8d` (no file under `tools/` had changed since `7679426e48`, S12's commit; the one change after, `9df25309f3`, is the connections fixture, below), run by `docs/qa-logs/2026-10-24-state-tests-close/suites.sh`. `TMPDIR` is set throughout to `.qa-scratch/t14/close/tmp`, the condition that failed cloud-layout at stage A. The outputs are in `.qa-scratch/t14/close/<n>.txt`.

| Run | Exit | Wall | Last line |
| --- | ---: | ---: | --- |
| wait-lock-test --busybox <image> | 0 | 10.8 s | PASSED |
| wait-lock-test (host tools) | 0 | 10.9 s | PASSED |
| rocknix-info-test | 0 | 0.5 s | PASS 12 full-script positive/negative controls |
| nova-led-test | 0 | 0.1 s | 14 PASS, 0 FAIL |
| usb-gadget-test --output | 0 | 0.3 s | PASS USB descriptor fixture: 18 cases, 72/72 checks |
| pixelelated-state-check-test --self-test | 0 | 9.4 s | } |
| pixelelated-state-check-test --payload-tests (no mcopy here) | 2 | 0.0 s | {"schema":1,"status":"error","category":"fixture-or-reader-failure"} |
| pixelelated-state-check --help | 0 | 0.0 s |                         only for --root / --mode first-boot |
| build-identity-test --output | 0 | 1.4 s | PASS build identity: 57 passed, 0 failed |
| retroarch-wrapper-test <source> | 0 | 0.1 s | PASS: every command ran exactly once at its own site |
| retroarch-wrapper-test (bare) | 2 | 0.0 s | usage: tools/retroarch-wrapper-test <video_thread_wrapper.c> [--gated], or RETROARCH_SRC=<a tree holding gfx/v |
| rasteratops-identity-check --tree --es | 0 | 0.0 s | identity source contracts: 0 failure(s); image qualification still required |
| settings-modes-test --busybox <image> | 0 | 0.3 s | PASS refuse-rename |
| settings-modes-test --busybox <host> (refused) | 2 | 0.0 s | settings-modes-test: CANNOT -- /usr/bin/busybox is not under a build root's image/system/; name its origin wit |
| melonds-upgrade-test --busybox <image> | 0 | 0.1 s | PASS temp-failure |
| melonds-upgrade-test --busybox <host> (refused) | 2 | 0.0 s | melonds-upgrade-test: CANNOT -- /usr/bin/busybox is not under a build root's image/system/; name its origin wi |
| rasteratops-cloud-layout-test --archives-only, TMPDIR set | 0 | 20.0 s | cloud-layout-test: 13 PASS, 0 FAIL; artifacts: /workspace/repos/pixelelated/distribution.worktrees/m6-tooling- |
| rasteratops-cloud-layout-test --ref 22571b47d2 (the historical matrix) | 0 | 400.8 s | cloud-layout-test: 398 PASS, 0 FAIL; artifacts: /workspace/repos/pixelelated/distribution.worktrees/m6-tooling |
| pixelelated-cloud-validator-test --rclone <image> | 0 | 15.7 s | PASS 30 controls |
| pixelelated-content-scope-test | 0 | 3.3 s | PASS absolute-root-unreadable-bounded |
| pixelelated-save-layout-test --busybox <image> | 0 | 29.3 s | save-layout: 39 PASS, 0 FAIL |
| pixelelated-duckstation-capture-test | 0 | 5.0 s | DuckStation captures: 31 PASS, 0 FAIL |
| pixelelated-cloud-folder-test (bare) | 2 | 0.0 s | --help exits 0; every attempted run exits 2 before starting any work. |
| pixelelated-cloud-folder-vm-test (bare) | 2 | 0.0 s | --help exits 0; every attempted run exits 2 before starting any work. |
| rasteratops-vm-cloud-epic --output (refuses current source) | 2 | 0.0 s | This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manu |
| pixelelated-vm-cloud-boundaries (bare) | 1 | 0.0 s | FAIL: tree, image, build-id and output required |
| pixelelated-vm-cloud-boundaries --tree <current> (refuses, #508) | 1 | 0.0 s | FAIL: migration suite retired by #508; use a historical source checkout and firmware |
| rasteratops-candidate-store --help | 0 | 0.0 s |   -h, --help    show this help message and exit |
| S2 environment case (sandbox-case.py, fixed tools) | 0 | 19.8 s | PASS |

**Against stage A (`02` § The runs):**
- **The six that failed now pass:** `build-identity-test` 57/0 (was 21/2), `rasteratops-identity-check` 0 failures (was 1), the validator 30 controls and DuckStation 31/0 (both had refused rclone 1.75.2), content-scope 21/0 (was 19/2), and cloud-layout 13/0 with `TMPDIR` set (was 11/2).
- **The new refusals are the designed ones:**
  - the host's busybox, given bare to either writer test, is CANNOT, exit 2 (#997);
  - `retroarch-wrapper-test` bare exits 2 with its usage line (#996);
  - `--payload-tests` is still CANNOT here (no `mcopy`, #1010).
- **The historical cloud-layout matrix:** 398/0 in 400.8 s.
- **The state check's self-test:** 190 controls, against 183 at stage A; the seven `exec-start-*` are #1000's.

**The S2 environment case:** `sandbox-case.py` against the fixed tools, with the caller's `TMPDIR`, `RCLONE_CONFIG`, an `RCLONE_CONFIG_QA_TYPE` remote, `BASH_ENV` and a function exported. All 10 checks pass:
- nothing leaked; no function; `BASH_ENV` not sourced; `mktemp` works; loopback only;
- cloud-layout 13/13;
- the copied real rclone refused, the stand-in default configuration never written, `--config` passed, and the FakeSP shape intact.

**After `9df25309f3`:** the S2 case, re-run with the fixture's argument order fixed, passes every check. That includes its new one, a T15-shaped shim that reads `$1 $2` refusing `config create`.

**`tools/last-good-scripts-test`, once, on the host, read-only (T15's file, unchanged, sha256 `b8495055873e4ce5…`):**
- **The run:** bare, with `QA_SYSTEM_ROOT` unset and `TMPDIR=/workspace/tmp/m6-t14/lgst-tmp`, at `b968264c8d`. **rc 1, 671.7 s, 990 PASS, 323 FAIL.**
- **The busybox it resolved:** its own line reads `sed/mv/cp/tr/head/wc/cut/awk: BusyBox v1.37.0 (Ubuntu 1:1.37.0-7ubuntu1) multi-call binary. -- a copy of /usr/bin/busybox`. That is **the host's**: `image_tool_source` finds no build root beside this worktree and falls back silently (`:400`), which is #662's lead.
- **The 323 FAIL, attributed as far as they were traced:**
  - **2 were this slice's, a regression from S2:** section C's broker cases. `89efee384c` put `--config <stage>` before the command, and T15's `load_remote` shims read the command from `$1 $2`. **Fixed in `9df25309f3`**, with the case added to `sandbox-case.py`. The whole suite was not re-run after the fix.
  - **2 were this slice's, from S8's contract:** sections ag (#421) and ah (#526). T15 passes `--busybox "${BB_HOST}"`, a **copy** in its temp root, so `settings-modes-test` and `melonds-upgrade-test` refuse it: CANNOT, exit 2, *not under a build root's image/system/*. A copy is refused even when T15 resolved a build root's busybox. **Not fixed here:** T15's call is #662's file. It is put to the coordinator on #661.
  - **The other 319 are in sections that call none of this slice's tools.** Section CF uses the connections fixture, and its failures read rc 75. 61 FAIL lines print `flock: applet not found`: the host's BusyBox 1.37.0 has no `flock` applet, and the image's 1.36.1 has one (both read). The rest were not traced; they are #662's.
  - **Section ae** (cloud-layout `--archives-only`, T15's call of S5's tool) passed.

**The busybox provenance:** `BusyBox v1.36.1 (2026-10-05 03:37:19 UTC)` from the M7 root `m7-pixelelated-replacement20`'s `image/system/usr/bin/busybox`, sha256 `79e7b20ddbe5abb6…`, the image's BUILD_ID `1a026648442321609b2288c2c9c06803817f9df2`. The rclone is `v1.75.2`, the image's copy at `/workspace/tmp/m6-t14/rclone-image`. No `tools/__pycache__` was written.
