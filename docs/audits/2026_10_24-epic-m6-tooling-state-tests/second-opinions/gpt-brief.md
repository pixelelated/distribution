# Independent review: M6.P2 T14, the fork's state tests (pixelelated/distribution #661)

You are the independent second reviewer (another lab) of a code audit. The first reader is Claude Opus 5.5. Below are the first reader's forward audit (`02`), retrospective (`03`) and analysis (`04`), two rule sections the tests promise to live by, the 32 files under review at their read commits (line-numbered), and the stage-A run lines.

The slice: 21 test tools and 11 fixture files that prove the OS scripts, the cloud layout, the settings writers, the release identity and the hardware quirks, using synthetic roots, busybox applets, real rclone inside bubblewrap, and, for two of them, a VM guest. **The lens is brittleness:** what each test depends on that is not the thing it proves, and whether a test can pass without proving.

**Answer first, in this order:**
1. **The four real-rclone tests' isolation** (`rasteratops-cloud-layout-test`'s `Fixture.run`, which `pixelelated-cloud-validator-test`, `-content-scope-test` and `-save-layout-test` import, plus the validator's and DuckStation's own sandboxes). Can a host's real rclone configuration, a real remote, the network, or a caller's environment variable reach the scripts under test? Cite the lines. The first reader found `TMPDIR` passing through (F-04); look for what else does.
2. **The two guest tests' guest handling** (`pixelelated-vm-cloud-boundaries`, `rasteratops-vm-cloud-epic`): how they find, wait for and stop a guest. Can either kill, reuse or report on a process it does not own?
3. **`pixelelated-state-check`'s non-disclosure:** can any path print, log or write a selected value (a credential, an account name) it inspects? Cite the lines.
4. **The two writer tests' busybox fallback** (`settings-modes-test`, `melonds-upgrade-test`, and T15's caller): can either pass under the host's applets while claiming the image's?

**Then refute** the first reader's findings F-01 to F-15 in `04`: for each, say confirmed, refuted (with the line that refutes it), or overstated or understated, with the severity you would give.

**Then add what was missed:** above all, any test case that can pass without proving its property (an empty selector, a check that cannot fail, a fixture copied from the current source, an exception swallowed, a count not asserted, a fallback that still says PASS).

**Output format:** numbered items `G-1`, `G-2`, ... Each item gives:
- a severity (Critical, High, Medium, Low);
- the file and line(s) at the read commit;
- a concrete failure scenario: the input or state, and the wrong result.

Keep claims you could not verify from the text marked as *inference*. Do not repeat the packet back. There is no word limit, but put parts 1 to 4 first.


## The first reader's 02-forward-audit.md (whole)

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
| P7 | the thirteen no-caller tools, by invocation | proved: tree |
| P8 | the index rows and their *Detail in* rules: 13 never name the tool | proved: tree |


## The first reader's 03-retrospective.md (whole)

# Retrospective: M6.P2 T14, the last-good, settings and state tests (#661)

Phase 3: the slice's tests read against what they were written to prove, and against the tree that has moved since.

## 3.1 What the tests were for

- **The family is the qualification record of M7's issues:** #365 (the cloud epic), #421 and #526 (the writers), #508, #510, #520, #521 and #524 (the folder contracts), #531 and #532 (the gadget and identity), #565 (the state check), #337 and #383 (the identity).
- **Each was written to qualify one fix** and has a `docs/qa-logs/` folder from that day.
- **Five are called afterwards:**
  - T15's `last-good-scripts-test` calls four;
  - `vm-qa` calls one;
  - the fork CI calls one;
  - the release preparer calls two.
- **The rest were run once for their issue and not again.**

## 3.2 What drifted

- **Three tools hold a value the tree also holds,** and the tree moved:
  - `build-identity-test`'s stand-in against a gate added after it (`d9f428e1a0`);
  - `rasteratops-identity-check`'s licence string against `84ff94fb3d`;
  - the two rclone-pin tests against `a0f60255ab`.

  Each failure is a test asserting a past state of the tree as if it were a property.
- **One script got safer:** `cloud_content_restore` now refuses `..` before rclone, and its test (content-scope) did not follow.
- **The migration was retired (#508),** and the two guest tests that proved it now refuse every run.

## 3.3 What none of them noticed

The six at-hash failures sit in tools with no caller (F-11). The four called through T15, the one in `vm-qa` and the one in CI all pass at the hash, the one in CI only without `-O`. A test nobody runs ages silently, which is the brittleness this slice was ordered to measure.

## 3.4 What the record says about catches

Every tool with a qa-log folder has a recorded failure on purpose (an old source, a negative control), so all but two have a seen positive. What none records is a regression caught in a later candidate after its own issue closed, except:
- `retroarch-wrapper-test` (`e5d14d4220`);
- the cloud-layout test's partial-retry control (2026-10-06).

## 3.5 The seams

| Seam | What crosses it | What breaks at it |
| --- | --- | --- |
| the four callees × T15's `last-good-scripts-test` × `vm-qa`'s `scripts` | T15 passes `--busybox "${BB_HOST}"`, `--rclone "${SA_RCLONE_SRC}"`, `--archives-only` and its own `TMPDIR` | `image_tool_source` falls back to the host's binary unmarked (F-13), and the callees accept it. `vm-qa` runs T15 without a `TMPDIR` that would leak into the sandbox, so F-04 has not shown there. A caller that sets one gets a false FAIL |
| the real-rclone four × `cloud-test-backend` × the host's `rclone.conf` | none use `cloud-test-backend`: each has its own `alias` remote to a local `/cloud` inside `bwrap`, `HOME=/storage` | the host's home is never mounted, so a real `rclone.conf` cannot be read. The caller's environment does pass (F-04): `TMPDIR` breaks it today, and an `RCLONE_CONFIG` would reach it (inference) |
| the release preparer's two × `release-candidates.md`'s gates | `fork-publish-release --prepare` calls `rasteratops-candidate-store` and `pixelelated-state-check` | the state gate was added after `build-identity-test` (F-01): the gate's contract held, and the test that exercises the preparer broke. The contract is not this slice's to change; the test's stand-in is |
| the guest two × T12's harness | `vm-pair`, `cloud-test-backend`, `vm-visual-qa`; T12's `vm-walks/cloud-epic/migration-protocol.sh` is sourced by the epic | both refuse on this tree (F-10). The boundaries test stops its guests by a `/proc` scan, not `vm-stop` (F-09) |
| the writer tests × the busybox rule × a build root's presence | `--busybox` | no M6 root holds a busybox. The M7 root's (1.36.1, the effective pin) and the host's (1.37.0) both pass, and neither test can tell them apart (F-13) |


## The first reader's 04-analysis.md (whole)

# Analysis: M6.P2 T14, the last-good, settings and state tests (#661)

Read at `8ebaf8daad` (the 22) and `2174265e9c` (the ten lint fixtures). The lens is brittleness.
- **Sources of the per-tool facts:** two read-only research passes, both re-derived here (each claim below is either a line read in this session or a run recorded in `00`); the stage-A runs; and the constructed inputs recorded as `PROOF:` lines in `00`.
- **Legend:** *false PASS*, *false FAIL* and *fails closed* name what a missing dependency does to the verdict.

## Findings (Phase 4)

| ID | Finding | Q | Draft severity | Evidence |
| --- | --- | --- | --- | --- |
| F-01 | `build-identity-test` fails at the hash: its firmware stand-in (`:132`, the bytes `SYNTHETIC FIRMWARE ONLY`) is refused by the `pixelelated-state-check` gate `fork-publish-release` gained at `d9f428e1a0`; 21 passed, 2 failed | Q3 | Medium | `00` § Stage A; `.qa-scratch/t14/out/build-identity` |
| F-02 | `rasteratops-identity-check` fails at the hash: `:143` expects `PKG_LICENSE == "MIT"`, and the recipe has said `MIT AND BSD-3-Clause` since `84ff94fb3d` (2026-10-13); 38 PASS, 1 FAIL | Q3 | Medium | `00` § Stage A |
| F-03 | `pixelelated-cloud-validator-test:58` and `pixelelated-duckstation-capture-test:178` require `rclone v1.75.1`. The pin is 1.75.2 since `a0f60255ab` (2026-10-11), so both refuse the package's own binary. The retired stub's docstring names the same version as current coverage (`pixelelated-cloud-folder-test`) | Q3, Q1 | Medium | `00` § Stage A |
| F-04 | The sandbox every rclone test shares, `rasteratops-cloud-layout-test`'s `Fixture.run` (`:138-147`), sets `HOME` and `PATH` and passes the caller's other variables through. A caller's `TMPDIR` names a path not mounted inside, so `backuptool`'s `mktemp` fails: 2 false FAILs (`T24-local-*-recovery`), 13 of 13 with `TMPDIR` unset. The validator's (`:326-335`) and DuckStation's (`:123-151`) sandboxes have no `--clearenv` either; `RCLONE_CONFIG` would pass the same way (inference, not seen) | Q2, Q3 | Medium | `00` § Stage B, trace 1 |
| F-05 | `pixelelated-content-scope-test` fails at the hash: `system-traversal-refused` and `content-pointer-traversal-refused` read `ctl/argv` unconditionally (`:121`, `:222`), and the script now refuses `..` before calling rclone (`e6645cb5ea`), so the read raises before the assertion. It is a false FAIL over a property that holds, unseen because nothing calls the test | Q3 | Medium | `00` § Stage B, trace 2 |
| F-06 | `pixelelated-cloud-validator-test --case <a name that matches nothing>` returns early from every case and writes `{"result": "PASS", "cases": []}`, `PASS 0 controls`, rc 0 (`:63`, `:356-357`). It is a false PASS, T12's `--only` shape | Q3 | Low | `PROOF: P5` |
| F-07 | `rocknix-info-test`'s verdict is `assert` (`:29`) with an unconditional `PASS` print (`:58`). Under `python3 -O` a constructed regression (a quirk failure that no longer propagates) is recorded failed in `result.json` while the tool prints `PASS 12` and exits 0. CI runs it without `-O`, so this is latent. `nova-led-test:50` has the same shape for the ledcontrol exit | Q2 | Low | `PROOF: P4` |
| F-08 | `retroarch-wrapper-test` leaves `<tmp>/t` and `t.c` behind (`:213`). Its two default roots are #640's retired layout (`:42-43`), so it exits 2 bare. A missing `gcc` raises at `:216` and exits 1, the code its docstring reserves for *the command ran twice* (`:27`) | Q2, Q1 | Low | `00` § Stage A |
| F-09 | `pixelelated-vm-cloud-boundaries` stops its guests by scanning `/proc/*/cmdline` for its owned pair path and signalling (`:675-690`), not by `vm-stop` and the pidfile. Under a sandbox that hides host PIDs (#506) it would find none and record `all_absent: True` (inference) | Q2 | Low | the source, `:675-690` |
| F-10 | Both guest tests refuse every run on this tree, because `cloud_migrate_layout` is absent at the hash (`pixelelated-vm-cloud-boundaries:709-710`, rc 1; `rasteratops-vm-cloud-epic:22-25`, rc 2). With the two retired stubs, four of the 21 tools cannot run at all today, and two of them are not marked retired in their index rows | Q6 | Renovation | `00` § Stage A |
| F-11 | 13 of the 21 tools are invoked by nothing in the tree. Confirmed by `git grep` over `tools`, `.github/workflows`, `.claude/skills` and `.githooks`, the personal-paths list not counted. Of these, 6 fail or refuse at the hash and nobody saw it: `build-identity-test`, `rasteratops-identity-check`, the two rclone-pin tests, content-scope, and the guest pair | Q6 | Renovation | § Q6 |
| F-12 | 13 of the 21 index rows name a *Detail in* rule that never names the tool. The two retired stubs' `fork-workflow.md` list entries carry no *retired* note | Q7 | Renovation | § Q7 |
| F-13 | `settings-modes-test` and `melonds-upgrade-test` take any `--busybox` and run it as the candidate's. T15's `image_tool_source` (`last-good-scripts-test:381-400`) ends in `command -v busybox \|\| true`, so with no build root a host's busybox passes as the image's, unmarked. This host has one (BusyBox 1.37.0), and both tests passed under it. `pixelelated-save-layout-test` without `--busybox` silently uses the host's `find` and `awk` (`:393`) | Q3 | Low | `00` § Stage A; `02` § T15's call sites |
| F-14 | `pixelelated-duckstation-capture-test`'s `package_install` case runs the installed synthetic payload on the host, outside its `bwrap` (`:334`) | Q2 | Low | the source |
| F-15 | Two descriptions disagree with the code. `rasteratops-identity-check:105`'s `check(True, ...)` cannot fail. `usb-gadget-test` defaults `--shell` to the host's `/bin/sh` (`:118`, dash here) where the docstring promises the image's functions | Q7, Q2 | Low | the source |

## Finding Verification (Phase 4.5)

Each finding was re-derived in this session, not taken from the research passes:

- **F-01, F-02, F-03 and F-05 (stage-D bugs):** each is the tool's own exit at the hash (`00` § Stage A) plus the commit that moved the tree past it. The coordinator accepted them as stage-D bugs on #661 at 20:28 and 20:31 UTC, F-03 as one bug.
- **F-04:** the same run with `TMPDIR` set (2 FAIL) and unset (13 of 13), with the host's `/tmp` entry count unchanged.
- **F-06 and F-07:** each constructed and run (`PROOF: P5`, `P4`).
- **F-08:** the wrapper test's leftover was listed by `find` after the run; the bare exit is recorded.
- **Read in the source, not run:** F-09, F-14 and F-15. F-09's consequence is marked as inference.
- **F-10:** both refusals recorded, and `git cat-file -e 8ebaf8daad:.../cloud_migrate_layout` fails.
- **F-11:** the caller grep, and § Q6's column (c).
- **F-12:** `instruction-files.md` read at the hash, row by row (the command in `00`).
- **F-13:** both runs, and T15's lines read.
- **Withdrawn after reading:**
  - the research pass's `RCLONE_CONFIG` leak is kept only as an inference inside F-04, not a finding;
  - the `rasteratops-vm-cloud-epic` negated probes that pass on an ssh failure (`:304`, `:334`, `:340`) are unreachable on this tree, which refuses first. They become one sentence of F-10 and not a finding.

## Second opinion (Phase 4.6)

Pending: the one GPT-6 Astra seat at `max`, a probe and one refutation over the packet (brief § 5).

## Renovation face

### Q1 Modernize

- **#640's retired layout:** `retroarch-wrapper-test:42-43` (`/workspace/repos/rocknix.worktrees/{devices,generic-x64}`), and 28 host-path lines in 10 tools (`.qa-scratch/t14/hostpaths.txt`). `rasteratops-vm-cloud-epic` has 9 of them, including `/tmp/rocknix-qemu-d.pid`. They are named for #640 and not changed.
- **A tool version the tree moved past:** rclone 1.75.1 in two tests and one stub's docstring (F-03).
- **The retired family:** the two `pixelelated-cloud-folder*` stubs, and the two guest tests that refuse (F-10).

### Q2 Standards

- **`|| true`:** 0 lines.
- **`assert`:** 2 tools carry one each (`nova-led-test:50`, `pixelelated-vm-cloud-boundaries`), and `rocknix-info-test`'s verdict rides on one (F-07).
- **Caller environment:** every sandbox passes it through (F-04).
- **Writes outside the temp root:** none, except the wrapper's leftover inside its own temp root (F-08).
- **Credential-shaped literals:** none in the 32 (the packet scan in `02` is the mechanical check).
- **Dictionary order and the host's `HOME`:** no test depends on either. The rclone sandboxes set `HOME=/storage`.

### Q3 Bugs: the pass-without-proving hunt, tool by tool

| Tool | The line read | A constructed input that would pass wrongly, or why none can |
| --- | --- | --- |
| `wait-lock-test` | every check unconditional; the absence checks (`:115`, `:156`) paired with a HELD check | none found. The 21 is not asserted, but each check is |
| `rocknix-info-test` | `:29` assert, `:58` unconditional PASS | **`python3 -O` over a regression: PASS, rc 0 (F-07, P4)**. Without `--baseline` the comparison `(not a or ...)` is vacuous (`:42`, `:44`) and CI never passes one |
| `nova-led-test` | `:50` assert on ledcontrol's exit; `:35-39` silent `.replace` | under `-O` a nonzero ledcontrol exit no longer fails, though the value checks still do (F-07) |
| `usb-gadget-test` | the whole attribute tree compared (`:106`) | none found. It runs under the host's `/bin/sh` (F-15) |
| `settings-modes-test` | function regexes (`:11-12`) never asserted to have matched; refuse-cases judge `rc != 0` plus unchanged files (`:41`) | a profile missing the functions gives rc 127, which satisfies the five refuse-cases. The main cases still FAIL, so the run fails overall. **The busybox fallback: classified as accepts any applets** (F-13) |
| `melonds-upgrade-test` | shims cover every external (`:43`); legacy mode exits 1, the same as a regression (`:116`) | none found for the verdict. The legacy negative and a regression share an exit code, and only the JSON tells them apart. **The busybox fallback: accepts any applets** (F-13) |
| `retroarch-wrapper-test` | `:216` gcc raise, exit 1; `:61` ValueError, exit 1 | a host without `gcc` exits 1, read as *ran twice* (a false FAIL, F-08). The doubled call is a race, so a PASS is probabilistic (inference) |
| `build-identity-test` | every refusal check accepts any nonzero exit (`:79`, `:83`, `:135`, `:143`, `:165`, `:167`) | a refusal for the wrong reason, such as the state gate refusing the stand-in, satisfies the rejection cases. Today the run stops at rc1 first (F-01) |
| `rasteratops-identity-check` | `:105` `check(True, ...)`; substring checks (`:115`, `:131-136`, `:150-153`); `not stale` (`:109`) vacuous on an empty gamelist | `:105` cannot fail (F-15). An empty gamelist passes `:109` |
| `rasteratops-candidate-store` | `verify` checks that the name equals the manifest digest (`:187`) | a re-manifested and renamed bundle verifies. Binding to the expected digest is the caller's (`fork-publish-release`) |
| `pixelelated-state-check` | every missing reader becomes exit 2 (`:108-109`, `:897`) | none found: it fails closed. An absent optional file reads as clear by design (`:394`) |
| `pixelelated-state-check-test` | `control_count` printed, never asserted (`:772`); expected-2 cases pass on any error (`:125-139`) | a payload control that errors for an unrelated reason satisfies its expected 2 |
| `rasteratops-cloud-layout-test` | per-case `except` catches only AssertionError and TimeoutExpired (`:1210`); `--case` matching nothing fails (`:1187`) | none found for a false PASS. False FAIL: F-04 |
| `pixelelated-cloud-validator-test` | `:63` early return per case; `:356-357` unconditional PASS | **`--case no-such-case`: PASS 0, rc 0 (F-06, P5)** |
| `pixelelated-content-scope-test` | `:121`, `:222` unconditional reads; `absent()` cases loop only over `lsf`/`copy`/`sync` lines | False FAIL: F-05. A script that exits 0 having done nothing passes the `missing-*` cases (inference; the case asserts what did not happen) |
| `pixelelated-save-layout-test` | `--cases` exact-set and non-empty (`:385-386`) | none for the selection. Without `--busybox` it uses the host's `find` and `awk`, unmarked (F-13) |
| `pixelelated-duckstation-capture-test` | `--cases` drops unknown names (`:182`) and fails only if none match (`:348`) | `--cases real,typo` runs `real` and passes, with `typo` silently skipped |
| `pixelelated-vm-cloud-boundaries` | `--case` matching nothing fails (`:653`) | none for the selection. **Guest handling: classified as pattern, by owned path in `/proc` cmdline (F-09), not pidfile-and-`vm-stop`**; it refuses at the hash anyway (F-10) |
| `rasteratops-vm-cloud-epic` | refuses first (`:22-25`) | unreachable today. **Guest handling: a pre-existing guest's pidfile (`/tmp/rocknix-qemu-d.pid`, cmdline checked, `:48-50`); in-guest `pgrep -f` with bracketed patterns.** The negated probes (`:304`, `:334`, `:340`) would pass on an ssh failure if it ran |
| the two stubs | refuse before work (rc 2) | nothing runs |

### Q4 Currency

| What | The tests assume | The tree pins | The host has |
| --- | --- | --- | --- |
| rclone | 1.75.1 (two tests, F-03); printed only in cloud-layout (`:1198`) | 1.75.2 (`a0f60255ab`) | `/usr/bin/rclone` v1.60.1-DEV; the M7 roots' image has v1.75.2 |
| busybox | the candidate's applets, by `--busybox` | 1.36.1 (`projects/ROCKNIX/packages/sysutils/busybox/package.mk:7`; the generic recipe's 1.38.0 is overridden) | v1.37.0 (Ubuntu); the M7 GENERIC_X64 root's image has v1.36.1 |
| Python | 3, `-I` | — | 3.14 |

### Q5 Efficiency

| Tool | Wall (stage A, this host) | Temp footprint |
| --- | ---: | --- |
| `wait-lock-test` | 7.5 s | none left |
| `rocknix-info-test` | 0.5 s | none left without `--output` |
| `nova-led-test` | 0.2 s | none left |
| `usb-gadget-test` | 0.3 s | the 20 KB report |
| `pixelelated-state-check-test --self-test` | 9.1 s | none left |
| `build-identity-test` | 0.2 s (fails early) | the 3 KB report |
| `retroarch-wrapper-test` | 0.1 s | **`t` and `t.c` left** |
| `rasteratops-identity-check` | 0.1 s | — |
| `settings-modes-test` | 0.4 s | the report |
| `melonds-upgrade-test` | 0.1 s | the report |
| `rasteratops-cloud-layout-test --archives-only` | 19.8 s (`TMPDIR` unset) | the artifacts directory |
| `pixelelated-content-scope-test` | 3.3 s | the artifacts |
| `pixelelated-save-layout-test` | 29.2 s | the artifacts |
| the validator and DuckStation tests | 0.1 s (refused) | — |
| the two guest tests | refuse at once on this tree; no recorded wall at the hash | — |

**The four T15 callees** in T12's 13-minute `scripts` suite:
- `last-good-scripts-test` prints no per-section timing, so their share is unmeasured from its own lines.
- Their standalone walls bound it at about 20 s, about 3 % of 13 minutes: settings 0.4 s, melonDS 0.1 s and cloud-layout 19.8 s. `wait-lock-test`'s functions are lifted, so the tool's 7.5 s is not paid.

### Q6 Dead ends and brittleness: the table

(a) is what each depends on that is not what it proves, and what its absence does. (b) is the last recorded catch. (c) is the caller by invocation. (d) is the positive control.

| Tool | (a) dependencies, and what absence does | (b) last recorded catch | (c) caller | (d) positive |
| --- | --- | --- | --- | --- |
| `wait-lock-test` | `001-functions` unreadable or no `wait_lock()`: exit 2 (`:35`, `:40`). No `timeout`: exit 2 (`:41`). GNU `date +%s%N` (`:50`) is not checked, so under a busybox `date` it errors (inference) | #98, 2026-09-09 work log: the old function 13 FAIL, the new 21/21 (`f13cf9f001`) | nobody (T15 lifts the functions, `:148`, `:8608`) | none in the tool. The manual negative is `git show 8ccc244dfa` (`:24-25`) |
| `rocknix-info-test` | the script missing: traceback, exit 1 (`:15`). Silent path `.replace` (`:24`). `--baseline` absent: the original's comparisons are vacuous. `-O`: a false PASS (F-07) | `docs/qa-logs/2026-10-11-optional-hardware/` (#548): the original exits 127 | **the fork CI** (`fork-checks.yml:50`, without `--baseline`) | the quirk-failure case (`:55-56`). The original-absent case only with `--baseline` |
| `nova-led-test` | the sources missing: traceback (`:16`). The `.replace` calls (`:35-39`) fail silently if production text changes, and an unreplaced path would address the host's `/sys` (inference). `-O` drops `:50` | `docs/qa-logs/2026-10-03-led/` (#332): HEAD's scripts 6 PASS, 8 FAIL | nobody | none |
| `usb-gadget-test` | `--source` missing: traceback. `--shell` defaults to the host's `/bin/sh` (`:118`, dash). Not exactly one `devversion=`: exit 2 (`:123-125`) | `docs/qa-logs/2026-10-11-usb-revision/`: the old source 40/72 | nobody | none in the tool; an old `--source` |
| `settings-modes-test` | `--busybox` required. Shims cover 11 applets, and `grep`, `sort`, `rm`, `cat` and `mktemp` are the host's (`:26`). Any busybox accepted (F-13) | #421, 2026-10-04 work log 19:22: the original 22 FAIL, corrected 29 PASS | T15 (`last-good-scripts-test:14224`) | the five refuse-cases (`:33-42`) |
| `melonds-upgrade-test` | `--busybox` required. The shims cover every external (`:43`). Any busybox accepted (F-13) | `docs/qa-logs/2026-10-08-pixelelated-replacement-17/cf10/melonds526-vm01/`: 15 old FAIL | T15 (`:14231`) | four failure injections (`:84-88`) and the legacy negative |
| `retroarch-wrapper-test` | a RetroArch source: none gives exit 2 (#640's roots, `:42-54`). `gcc` absent: exit 1, read as *ran twice* (`:216`). The build root's unpacked copy, not the tree's patch 0015, decides | `e5d14d4220`, 2026-09-19: the shipped source ran 2017 times for 2000 posts | `vm-qa`'s `wrapper` suite (`vm-qa:185`, default) | none (`--gated` parsed and unused at the hash) |
| `build-identity-test` | `config/build-identity`, `git`, the `scripts/image` slices (`:50-91`), and `fork-publish-release`, hence the state gate: **its stand-in refused, a false FAIL at the hash (F-01)** | `docs/qa-logs/2026-10-11-release-policy/`: 21/2, a harness defect then; no product catch recorded | nobody | the qualifier, mutation and tamper rejects (`:77-83`, `:156-167`), each accepting any nonzero exit |
| `rasteratops-identity-check` | `--es` required. `bwrap` absent: FAIL (`:96`). `git` absent: traceback (`:139`). The ES licence string (`:143`): **a false FAIL at the hash (F-02)** | `docs/qa-logs/2026-10-04-es-identity-export/`: the original profile 1 failure | nobody | none in the tool; the template negative takes the caller's `--tree` |
| `rasteratops-candidate-store` | Python only. An uncaught AttributeError on a malformed manifest is still nonzero | `docs/qa-logs/2026-10-02-candidate-preflight/candidate-store.log`: a constructed corruption refused | `fork-publish-release` (`:22-23`, `:113`) | none in the tool |
| `pixelelated-state-check` | `unsquashfs`, `e2fsck`, `debugfs`, `sfdisk`, `mcopy` and `systemctl`: each missing gives exit 2 (`:108-109`). It fails closed | only fixes to the gate refusing correct input (`cc0f8b0aa7` and the #565 runs); no contamination caught in a candidate is recorded | `fork-publish-release` (`:85-108`) | its test's contaminated roots |
| `pixelelated-state-check-test` | the gate, `fork-publish-release`, and for `--payload-tests` the host's `mksquashfs`, `unsquashfs`, `sfdisk` and `mcopy` (`mcopy` absent here: CANNOT). The caller's `TMPDIR` | `docs/qa-logs/2026-10-13-clean-state-runtime/pix565-payload-20261013`, rc 2: the gate refused `lost+found` | nobody (a qa-log README records a run) | about 155 root cases and the payload controls; `control_count` unasserted |
| `rasteratops-cloud-layout-test` | `bwrap` and an rclone (default: a sibling worktree's GENERIC_X64 root, else the host's `which`, version printed not asserted, `:1053-1054`, `:1198`). **The caller's environment: `TMPDIR` gives a false FAIL (F-04)** | 2026-10-06 work log, `partial-retry-host01`: a missing-record control failed and blocked an unready repair | T15 (`:14188`, `vm-qa`'s `scripts`); fixture for three others | `--inject-failure` (`:1182`), seen in `2026-10-04-pixelelated-source/cloud-layout-negative.log` |
| `pixelelated-cloud-validator-test` | an rclone (default: the host's `which`). **`rclone v1.75.1` hardcoded: a false FAIL at the hash (F-03)**. `git` for `c445081a59` | `docs/qa-logs/2026-10-07-cloud-validator/validator/runs/root-old01.json`: an unreadable root reported ready at `583c1b4d` | nobody | none; `--case` matching nothing is a false PASS (F-06) |
| `pixelelated-content-scope-test` | an rclone (required), the layout fixture, the caller's environment. **The stale `argv` read: a false FAIL at the hash (F-05)** | `docs/qa-logs/2026-10-07-cloud-validator/content-scope/pixelelated-content-root-unfixed-01` | nobody | the `fixture-check` witness only |
| `pixelelated-save-layout-test` | an rclone, `git` for `6f89bc7cec`, `--busybox` optional: without it, the host's `find` and `awk` unmarked (F-13) | `docs/qa-logs/2026-10-08-save-repair-cases/coverage/unfixed01`, `-02`, `-n64-01`: 15 old FAIL | nobody | none in the tool; `--ref` |
| `pixelelated-duckstation-capture-test` | an rclone. **`rclone v1.75.1` hardcoded: a false FAIL at the hash (F-03)**. The host's `bash` and `python3`. The payload runs on the host (F-14) | `docs/qa-logs/2026-10-08-save-repair-cases/duckstation-captures/old02`: four expected failures | nobody | none; `--cases` drops unknown names |
| `pixelelated-vm-cloud-boundaries` | `vm-pair`, `cloud-test-backend` (WebDAV 9040), ssh 10022 and 10023, an image and BUILD_ID. **`cloud_migrate_layout` absent: refuses every run (F-10)**. A host with any `qemu-system-*` running: refuses (`:270-276`) | `docs/qa-logs/2026-10-06-pixelelated-replacement-15/p4-installed-fixes-01`: 3 FAIL, the observer's, per that audit | nobody | `--inject-failure` (`:706`), seen in `2026-10-05-p3-reconciliation/cloud-boundaries-01/negative-control.log` |
| `rasteratops-vm-cloud-epic` | a pre-existing guest d (its pidfile `/tmp/rocknix-qemu-d.pid`), `cloud-test-backend`, `vm-visual-qa`, `socat`, VNC. **`cloud_migrate_layout` absent: refuses every run (F-10)** | only its negative controls (`2026-10-03-cloud-epic/negative-control.log`, `2026-10-05-p3-reconciliation/guest-negative.json`) | nobody (`vm-walks/cloud-epic/migration-protocol.sh` names it; it sources that file, not the reverse) | `--inject-failure` (`:32`), which bypasses the refusal |
| `pixelelated-cloud-folder-test` | none: it refuses before work | retired at `2cc6ce30e3` (2026-10-08); old runs in `2026-10-07-explicit-cloud-folders/distro` | nobody (by design) | — |
| `pixelelated-cloud-folder-vm-test` | none: it refuses before work | retired at `2cc6ce30e3` | nobody (by design) | — |

**The thirteen no-caller tools, from the record:**
- **Confirmed by invocation for all thirteen.** Each is named only in `.githooks/pre-push`'s personal-paths list, a docstring or an index row: `build-identity-test`, `nova-led-test`, `pixelelated-content-scope-test`, `pixelelated-duckstation-capture-test`, `pixelelated-save-layout-test`, `pixelelated-state-check-test`, `pixelelated-vm-cloud-boundaries`, `rasteratops-identity-check`, `usb-gadget-test`, `rasteratops-vm-cloud-epic`, `wait-lock-test` and the two stubs.
- **In the record, eleven have runs:** every one except the two stubs has a `docs/qa-logs/` folder from when its issue was qualified (column (b)). So they have callers in the record, not in the tree.
- **The cost of having no caller:** six of the thirteen fail or refuse at the hash and nothing noticed (F-11).

**The fixture file** `tools/test-fixtures/cloud_connections_fixture.py`:
- **Its reader:** only `last-good-scripts-test`. It is copied in at `:5005` and `:11521` and imported at `:5050`, `:5241`, `:5393` and `:11557`, applied only `if hasattr(m, "connections")`.
- **What it fixes:** it redirects the connections module's CONFIG, ACTIVE, LOCK and SYSTEM paths into the fixture, and simulates `config create` by writing the section and `type`. It refuses only the exact combination of real `subprocess` and `RCLONE == '/usr/bin/rclone'` (`:84-85`).

**The ten lint fixture files** (P1's): read by `tools/lint-audit-artifacts`' fixtures, and since T10's `2444828e89` by `tools/test-fixtures/lint-audit-artifacts/run.sh` (on T10's branch). They fix the renovation face's pass and fail cases.

**Proposed dispositions, for the coordinator, who decides with the maintainer:**
- **The two retired stubs:** remove them, with their index rows and personal-path list entries. They refuse every run, nothing calls them, the history is in `git` and the `2026-10-07`/`-08` qa-logs, and one docstring now points at a stale rclone version as current coverage. The alternative is to keep them as refusing markers, with the docstring's version corrected and *retired* added to `fork-workflow.md`'s list entries.
- **The two guest tests:** treat them as the stubs were treated. They refuse every run since #508 retired the migration, and `rasteratops-vm-cloud-epic` says so itself. Retire them in place as markers or remove them; either way the index rows should say *retired*. The authorized guest cycle was not needed to show this (`02` § The guest cycle).
- **The other nine no-caller tools:** not retirement. Each proves a property the tree still has. The finding is that nothing runs them, so each could go into a suite that runs (`vm-qa`'s host suites or the fork CI) once its at-hash failure is fixed. Which ones, and where, is the coordinator's.

### Q7 Clarity: the three descriptions

- **The index rows:** all 21 tools have one in `instruction-files.md` at the hash.
- **The *Detail in* rule never names the tool (F-12, the class of T10's 31 pairs), for 13 of them:** `melonds-upgrade-test` (`upgrade-and-install.md`), `nova-led-test`, `pixelelated-cloud-folder-vm-test` and `rasteratops-vm-cloud-epic` (`generic-x64-vm-testing.md`), `pixelelated-cloud-folder-test`, `pixelelated-cloud-validator-test`, `pixelelated-content-scope-test`, `pixelelated-duckstation-capture-test` and `rasteratops-cloud-layout-test` (`rclone-cloud-sync.md`), and `pixelelated-state-check`, `pixelelated-state-check-test`, `rasteratops-candidate-store` and `rasteratops-identity-check` (`release-candidates.md`).
- **The two stubs' index rows** say *refuses execution*, which matches their behaviour (rc 2). Their `fork-workflow.md` list entries are plain, with no note.
- **Promises the code does not keep:** `usb-gadget-test`'s header promises the actual USB preparation functions and runs them under the host's `/bin/sh`. `rasteratops-identity-check`'s `:105` is a check that cannot fail (F-15). `retroarch-wrapper-test`'s docstring reserves exit 1 for *ran twice*, and a missing compiler also exits 1 (F-08).
- **The guest pair's rows** (`instruction-files.md`, *run promoted cloud and settings cases* and *prove explicit layout1 migration...*) describe suites that refuse every run (F-10).
- **Leads for the coordinator, not edits here:** the rule drift and the index rows.


## Context: engineering-practices.md § Guards must fail closed (next)

## Guards must fail closed

A check that cannot run has not passed. Three defects in one day's work shared
this shape, and all three were invisible because the failure mode was silence.
A fourth, later, had the same shape and the opposite outcome:

- A pipeline's status is its **last** command's. `if ! producer | consumer`
  tests the consumer, so a producer that exits 1 — an unreadable input, a full
  disk — is discarded and the guard never fires. `backuptool` wrote short
  archives and announced them as successes.
- An **unquoted** list expanded into a command's arguments. A member name with
  a space split into two names that did not exist, the tool errored into
  `2>/dev/null`, and those members went unscanned — a *credential* scan
  quietly checking less than it claimed.
- **`ls A B` exits non-zero when either glob is unmatched.** Gating on it meant
  that once only one archive format was present — the normal state after a
  format change — the whole verification block was skipped, disabling the guard
  added for a shipped data-loss bug.
- **A check that reads a fixed position in another tool's output.** Verifying
  a Dropbox merge with `rclone check ... | tail -1 | grep -q "0 differences
  found"` looked exact, and matched nothing: rclone prints `N matching files`
  last, and the differences line second to last. This one happened to fail in
  the safe direction — it kept every directory it could not confirm, so the
  cost was a re-run rather than 489 MiB — and that is the whole argument for
  the rule. Grep the output, not a line of it, and let the safe branch be the
  one a broken check falls into.

Each reads as a reasonable check. Each defaults to "proceed" when its own
machinery breaks, which in a subsystem whose signature failure is *reporting
success while doing nothing* is precisely backwards. (The fourth defaulted to
"stop", which is what the rule asks for and why it cost nothing.)

So:

- **Prefer a positive assertion over the absence of an error.** Collect what
  exists and check the count, rather than branching on a command's exit status
  that also means "one of your arguments was empty".
- **`set -o pipefail`** (a subshell keeps it local) wherever a pipeline's first
  stage can fail.
- **Quote every expansion** that becomes another command's arguments, or pass
  the list some other way.
- **`ssh -n` inside a `while read` loop** (or redirect `< /dev/null`). ssh
  reads the loop's stdin, so the loop processes one item and exits having
  reported success; the count is the only thing that shows it. The same is
  true of any command in the loop body that reads stdin.
- **Prove the guard fires.** Construct the violation it exists to catch and
  watch it fail, then fix it and watch it pass. A guard with no observed
  positive is a guard with no evidence — the same rule blindspot 14 states for
  hooks, applied to checks inside a script.

An assertion that cannot fail is not evidence. Ask what input would produce a
FAIL; if you cannot name one, the check proves nothing.

**A fixture for a secret scanner is built at run time, never written as a
literal (2026-09-28, #307).** `tools/last-good-scripts-test`'s cases for the
credential scan and the redaction feed values that look like a private key,
an OAuth token and a `devpassword=`; three were committed as literals by a
fix stream, the push guard read them in history, and the unpushed range had
to be rewritten by the maintainer before `next` could move. So a fixture is
assembled when the case runs -- `printf '%s' 'OPENSSH PRIVATE KEY'` into a
format string, a value passed through `$(printf ...)` -- and the file at rest
carries no line the guard would match. `.githooks/pre-commit` (both
repositories) now refuses such a line at commit time with the same patterns
the push guard uses (`.githooks/secret-patterns`, one definition); a
refusal there costs one edit, at push time it costs a rewrite.

**The positive is recorded where the guard is wired (audit #258, P-02).** A
hook line, a CI step, a suite line or a `check` in a script is committed
with a work-log line naming the constructed failure it was seen to catch,
the date, and the command -- five guards in the RC round had none (the
build's `--wrap-mode=nodownload`, the push guard's index warning, a red
`fork-checks.yml` run, `tools/retroarch-wrapper-test`, `tools/archaeology`'s
own constructed case), and each was proven in an afternoon once asked. A
guard whose positive nobody can point at is a guard whose first real firing
will be argued with. No tool audits this yet: `tools/ceremony-check` proves
blindspot entries name a guard that exists, not that the guard has fired;
extending it to the fork tools is #254's, and until then this paragraph is
the whole enforcement.

**Success reported over a no-op is the same defect with a friendlier face
(audit #258, P-04).** Four shapes from one round, each green:

- **A count echoed is not a floor.** `echo "USING: $(wc -l < table) games"`
  printed `0 games` and the build went on; assert the number, and fail under
  the floor.
- **An exit code named must be defined.** `exit ${EX_USAGE}` with no
  `EX_USAGE=` anywhere is `exit`, the last command's status -- the usage
  `echo`'s 0. `set -u` does not catch it in a script that never enables it.
  Define the constants in one block at the top and grep `exit \$\{` against
  it.
- **A success log line is written from the artifact, not the exit status.**
  `save state copy recorded` on rc 0 recorded nothing when the script had
  exited 0 with a WARN; the script now exits a distinct code and the caller
  says "recorded nothing".
- **A lint reads every copy of the claim it checks.** `lint-audit-artifacts`
  read the Phase 7 table and never the YAML index beside it, which said
  `open` for 32 resolved items; it compares them now.

**And a suite is not wired in until it has been seen to FAIL once, on the
runner's own guest.** "Prove the guard fires" applies to a whole check as
much as to a branch inside one. The time-to-play cell (#135) was written and
measured on a guest whose RetroArch had been set to GL by hand months
earlier; its first dispatch by `tools/vm-qa` on a guest running the image's
default Vulkan driver -- which a QEMU guest cannot draw with -- printed
`time-to-play: PASS in 581s` over a table in which every headline number was
`-`. The tool judged its run by whether it *ran*, not by whether it
*measured*. Three rules came out of it, and they generalise past that suite
(blindspot 39, D-QA-022):

- **A tool that reports numbers fails when the numbers are missing**, and
  says which (`headline_missing()` in `tools/time-to-play`; the report ends
  "Not a pass").
- **A tool that needs the guest in a state the image does not ship puts it
  there for the run and restores it** (`--vm`), rather than depending on a
  condition that happened to be true where it was written.
- **The first PASS of anything new is the one to distrust.** Construct the
  failure, watch the runner report it, then trust the green.

A fifth, of the same family (2026-09-10): the picker's scan named the one
failure it anticipated -- the network gone, exit 69 -- and let every other
failed listing fall through to the success path, so a cloud that refused the
connection was presented as an empty one. A branch for the failure you
expect is not a guard; the guard is that the success path is reached only by
success (`rc -eq 0`, or the one other code that genuinely means "nothing
there"), and every other value is a failure whether or not you have a name
for it.

Two more shapes, the fourth and fifth instances of blindspot 22 (a probe
that cannot report absence), promoted here on 2026-09-06:

- **A missing tool is a failing guard.** `comm … | wc -l` on the image's
  busybox — which has no `comm` — read 0, and 0 meant "nothing differs".
  A count built on a command that may not exist must fail loudly when it
  does not (`command -v` first), and any script that reaches for a
  coreutils name runs on the VM before the host's answer is believed
  (`generic-x64-vm-testing.md` § What the guest's busybox lacks).
- **A kill by pattern reaches the shell that runs it.** `pkill -f
  'vm76[.]qcow2'` killed its own shell because the same command text held
  the literal in an `rm` three lines down, and `bash -c` carries the whole
  script in its argv. Long-lived processes get a pidfile; a kill goes by
  PID; when a pattern is unavoidable, filter the hits by
  `/proc/<pid>/comm` before signalling.



## Context: upgrade-and-install.md § Verify on a device, not on the host (next)

## Verify on a device, not on the host

**And on the VM before the device** (`engineering-practices.md` § "If the VM
can test it, the VM tests it first"). The VM is a device for this purpose — the
same busybox, scripts and binary — and it is the one you can afford to break.

Host tools are not the tools on the device, and the difference hides real
failures. Info-ZIP on a desktop silently replaces a symlink and returns success;
busybox on the device refuses and aborts. The bug was invisible until it ran on
the target.

The cheap way to cover both paths, per
[`generic-x64-vm-testing`](generic-x64-vm-testing.md):

- **Clean install** — boot the built image in a fresh VM.
- **Upgrade** — boot a VM from the *previous* image, use it enough to create
  state (a backup, a config change, a save), then update it in place and confirm
  that state still works.

`tools/vm-upgrade-rehearsal <previous img.gz> <new tar> <new BUILD_ID>` runs the
upgrade half end to end and fails closed on any piece of state that did not
survive (first run 2026-09-20, build 15 to `77e7e97515`, 20 of 20). The clean
install is what `tools/vm-qa` boots from the image every run.

**And under the device's tools, not the host's.** `tr -d '[:print:][:space:]'`
deletes every printable byte under GNU tr and eight literal characters under
busybox tr, so a text check that passed in `tools/last-good-scripts-test`
rejected every real `system.cfg` on every device and the last-good record
was never written (2026-09-10, blindspot 34). The test now runs every
command that is a busybox applet on the device (`sed mv cp tr head wc cut
awk`) through the image's busybox from the build root, and its fixtures are
the image's own files, not three lines typed for the test. When a script
will run under busybox, ask of every external command it calls whether the
host's is the same program -- `readlink -f $(command -v tr)` on the device
answers it -- and shim the ones that are not, not only the ones already known
to differ.


## File: tools/rasteratops-cloud-layout-test (at 8ebaf8daad, 1224 lines)

```text
    1  #!/usr/bin/env python3
    2  """Production cloud scripts against isolated, real rclone filesystems (#365).
    3  
    4  Host regressions, not image qualification. Each case gets new cloud, config,
    5  cache and logs. --ref supplies old production bytes to the same assertions;
    6  --source-root supplies another checkout's working bytes. --archives-only keeps
    7  the ordinary settings archive checks usable after migration retirement.
    8  --output retains command transcripts, final pointers and synthetic cloud bytes.
    9  """
   10  import argparse
   11  import hashlib
   12  import io
   13  import json
   14  import os
   15  from pathlib import Path
   16  import re
   17  import shutil
   18  import subprocess
   19  import sys
   20  import tarfile
   21  import tempfile
   22  
   23  ROOT = Path(__file__).resolve().parent.parent
   24  SOURCES = Path('projects/ROCKNIX/packages/network/rclone/sources')
   25  NEW = '/pixelelated'
   26  OLD = '/ROCKNIX'
   27  ARCHIVE = '2026_10_01-120000-QA-ROCKNIX_SETTINGS.tar.gz'
   28  DEVICE = 'QA-deadbeef01'
   29  
   30  
   31  def put(path, data, executable=False):
   32      path.parent.mkdir(parents=True, exist_ok=True)
   33      path.write_text(data)
   34      if executable:
   35          path.chmod(0o755)
   36  
   37  
   38  class Fixture:
   39      def __init__(self, path, args):
   40          self.path, self.args, self.seq = path, args, 0
   41          source_root = getattr(args, 'source_root', None) or ROOT
   42          path.mkdir()
   43          for folder in ['repo', 'shim', 'storage/.config/rclone', 'storage/roms/backup',
   44                         'storage/.cache/cloud_sync', 'cloud', 'ctl', 'log', 'run']:
   45              (path / folder).mkdir(parents=True, exist_ok=True)
   46          if args.ref:
   47              # Deleted helpers still belong to a historical --ref. Enumerating
   48              # today's working tree silently omitted them after #508.
   49              listing = subprocess.run(['git', '-C', str(ROOT), 'ls-tree', '-r',
   50                                        '--name-only', args.ref, '--', str(SOURCES)],
   51                                       check=True, capture_output=True, text=True)
   52              sources = [Path(name) for name in listing.stdout.splitlines()
   53                         if Path(name).parent == SOURCES]
   54          else:
   55              sources = [SOURCES / src.name for src in (source_root / SOURCES).iterdir()
   56                         if src.is_file()]
   57          for src in sources:
   58              dest = path / 'repo' / src.name
   59              if args.ref:
   60                  r = subprocess.run(['git', '-C', str(ROOT), 'show', f'{args.ref}:{src}'],
   61                                     check=True, capture_output=True)
   62                  dest.write_bytes(r.stdout)
   63              else:
   64                  shutil.copyfile(source_root / src, dest)
   65              dest.chmod(0o755)
   66          put(path / 'profile', 'export PATH=/shim:/repo:/usr/bin:/bin\nexport HOME=/storage\nexport OS_NAME=ROCKNIX\n')
   67          put(path / 'storage/.config/rclone/rclone.conf', '[qa]\ntype = alias\nremote = /cloud\n')
   68          put(path / 'repo/cloud_device_id', '''#!/bin/sh
   69  case "$1" in
   70   --label) echo QA;; --legacy) cat /ctl/legacy 2>/dev/null;;
   71   --previous) cat /ctl/previous 2>/dev/null;; *) echo QA-deadbeef01;;
   72  esac
   73  ''', True)
   74          for name, body in {
   75              'logger': 'printf "%s\\n" "$*" >> /ctl/journal',
   76              'ip': '[ -e /ctl/offline ] || echo "default via 10.0.2.2 dev eth0"',
   77              'ping': '[ ! -e /ctl/offline ]',
   78              'systemd-tmpfiles': 'exit 0',
   79          }.items():
   80              put(path / 'shim' / name, '#!/bin/sh\n' + body + '\n', True)
   81          put(path / 'shim/rclone', '''#!/bin/bash
   82  printf '%s\\n' "$*" >> /ctl/argv
   83  if [ -f /ctl/faults ]; then
   84   while IFS=$'\\t' read -r pattern code; do
   85    [[ "$*" =~ $pattern ]] && { printf '%s\\n' "$*" >> /ctl/fault-fired; echo 'injected provider failure' >&2; exit "$code"; }
   86   done < /ctl/faults
   87  fi
   88  if [ -e /ctl/bucket ]; then
   89   if [ "$1 $2" = 'backend features' ]; then
   90    printf '{"Hashes":["md5"],"Features":{"BucketBased":true}}\\n'; exit 0
   91   fi
   92   # Bucket prefixes can return successful empty lsd for a missing prefix.
   93   if [ "$1" = lsd ]; then exit 0; fi
   94  fi
   95  exec /rclone.real "$@"
   96  ''', True)
   97          bt_rel = Path('projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool')
   98          bt = subprocess.run(['git', '-C', str(ROOT), 'show', f'{args.ref}:{bt_rel}'], capture_output=True, check=True).stdout if args.ref else (source_root/bt_rel).read_bytes()
   99          (path/'repo/backuptool').write_bytes(bt)
  100          (path/'repo/backuptool').chmod(0o755)
  101          put(path/'shim/systemctl', '#!/bin/sh\nexit 0\n', True)
  102          self.conf()
  103          put(path / 'storage/.config/cloud_sync-rules.txt', '+ /**/*.srm\n- /**\n')
  104  
  105      def conf(self, saves=NEW+'/Saves', backups=NEW+'/Backups', content=NEW+'/Content', keep=''):
  106          values = dict(SAVESPATH='/storage/roms', SAVES_REMOTE=saves,
  107                        SETTINGS_BACKUPS='/storage/roms/backup', SETTINGS_REMOTE=backups,
  108                        BACKUPMETHOD='copy', RESTOREMETHOD='copy', BACKUPFILE_BACKUP_OPTION='no',
  109                        BACKUPFILE_RESTORE_OPTION='no', LOG_LEVEL='INFO', LAYOUT_KEEP=keep,
  110                        RCLONEOPTS='--progress --log-file /var/log/cloud_sync.log --filter-from /storage/.config/cloud_sync-rules.txt',
  111                        RCLONE_NET_OPTS='--contimeout 1s --timeout 2s --low-level-retries 1 --retries 1')
  112          if content is not None:
  113              values['CONTENT_REMOTE'] = content
  114          put(self.path / 'storage/.config/cloud_sync.conf', ''.join(f'{k}="{v}"\n' for k,v in values.items()))
  115  
  116      def pointers(self):
  117          return dict(re.findall(r'^(\w+)="([^"\n]*)"$', (self.path / 'storage/.config/cloud_sync.conf').read_text(), re.M))
  118  
  119      def file(self, name, data='sentinel\n'):
  120          put(self.path / 'cloud' / name.lstrip('/'), data)
  121  
  122      def directory(self, name):
  123          (self.path / 'cloud' / name.lstrip('/')).mkdir(parents=True, exist_ok=True)
  124  
  125      def archive(self, name, sentinel=b'settings sentinel\n', local=False):
  126          path = self.path / ('storage/roms/backup' if local else 'cloud') / name.lstrip('/')
  127          path.parent.mkdir(parents=True, exist_ok=True)
  128          with tarfile.open(path, 'w:gz') as tar:
  129              info = tarfile.TarInfo('storage/.config/proof-sentinel'); info.size = len(sentinel)
  130              tar.addfile(info, io.BytesIO(sentinel))
  131          return path
  132  
  133      def fault(self, pattern, rc=5):
  134          put(self.path / 'ctl/faults', f'{pattern}\t{rc}\n')
  135  
  136      def run(self, script, *argv):
  137          self.seq += 1
  138          cmd = ['bwrap', '--die-with-parent', '--unshare-pid', '--tmpfs', '/', '--ro-bind', '/usr', '/usr',
  139                 '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/lib', '/lib', '--symlink', 'usr/lib64', '/lib64',
  140                 '--ro-bind', '/etc', '/etc', '--ro-bind', str(self.path/'profile'), '/etc/profile',
  141                 '--ro-bind', self.args.rclone, '/rclone.real', '--dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp']
  142          for folder, guest in [('repo','/repo'),('shim','/shim'),('storage','/storage'),('cloud','/cloud'),
  143                                ('ctl','/ctl'),('log','/var/log'),('run','/var/run')]:
  144              cmd += ['--bind', str(self.path/folder), guest]
  145          cmd += ['--chdir', '/storage', '--setenv', 'HOME', '/storage', '--setenv', 'PATH', '/shim:/repo:/usr/bin:/bin',
  146                  'bash', '/repo/'+script, *argv]
  147          r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120,
  148                             start_new_session=True)
  149          stem = self.path / f'{self.seq:02d}-{script}'
  150          stem.with_suffix('.log').write_text(r.stdout)
  151          stem.with_suffix('.json').write_text(json.dumps(dict(argv=[script,*argv], rc=r.returncode, pointers=self.pointers()), indent=2))
  152          require(r.returncode not in (126,127), f'fixture could not execute {script}: {r.stdout[-500:]}')
  153          return r
  154  
  155  
  156  def require(condition, message):
  157      if not condition:
  158          raise AssertionError(message)
  159  
  160  
  161  def read_facts(path):
  162      return dict(line.split('=',1) for line in path.read_text().splitlines() if '=' in line) if path.exists() else {}
  163  
  164  
  165  def scan(f):
  166      r = f.run('cloud_scan')
  167      require(r.returncode == 0, f'scan rc={r.returncode}: {r.stdout[-300:]}')
  168      return read_facts(f.path/'storage/.cache/cloud_sync/scan/settings')
  169  
  170  
  171  def archive_roundtrip(f):
  172      src = f.archive(ARCHIVE, local=True)
  173      digest = hashlib.sha256(src.read_bytes()).hexdigest()
  174      r = f.run('cloud_backup', '--system-only', '--yes')
  175      sent = f.path/'cloud/pixelelated/Backups'/DEVICE/ARCHIVE
  176      require(r.returncode == 0 and sent.exists(), f'production writer rc={r.returncode}; no per-device archive: {r.stdout[-400:]}')
  177      require(hashlib.sha256(sent.read_bytes()).hexdigest() == digest, 'writer changed archive bytes')
  178      facts = scan(f)
  179      # Continue through restore even when discovery is broken: preserve evidence of both endpoints.
  180      src.unlink()
  181      r = f.run('cloud_restore', '--system-only', '--yes')
  182      require(r.returncode == 0 and src.exists() and hashlib.sha256(src.read_bytes()).hexdigest() == digest,
  183              f'production restore failed to recover exact writer archive rc={r.returncode}')
  184      require(facts.get('MINE') == ARCHIVE, f'scan missed the real writer archive: {facts}')
  185  
  186  
  187  def archive_selection(f, kind, branded=False):
  188      folders = {'current': DEVICE, 'legacy': 'qa-old', 'healed': 'QA-ee5013fc56', 'flat': '', 'foreign': 'Other-beef'}
  189      folder = folders[kind]
  190      if kind == 'legacy': put(f.path/'ctl/legacy', folder+'\n')
  191      if kind == 'healed': put(f.path/'ctl/previous', folder+'\n')
  192      f.archive(f'pixelelated/Backups/{folder}/{ARCHIVE}')
  193      if branded:
  194          put(f.path/'profile', 'export PATH=/shim:/repo:/usr/bin:/bin\nexport HOME=/storage\nexport OS_NAME=pixelelated\n')
  195      facts = scan(f)
  196      expected = '' if kind == 'foreign' else ARCHIVE
  197      require(facts.get('MINE') == expected, f'{kind} branded={branded}: {facts}')
  198  
  199  
  200  def state_case(f, saves, state, files=(), dirs=(), keep=''):
  201      backups = '/GAMES/backup' if saves == '/GAMES' else saves.rsplit('/',1)[0]+'/Backups'
  202      f.conf(saves, backups, keep=keep)
  203      for name in files: f.file(name, 'layout=2\n' if name.endswith('/.layout') else 'sentinel\n')
  204      for name in dirs: f.directory(name)
  205      before = f.pointers()
  206      r = f.run('cloud_migrate_layout', '--state')
  207      facts = dict(line.split('=',1) for line in r.stdout.splitlines() if '=' in line)
  208      require(r.returncode == 0 and facts.get('STATE') == state, f'expected {state}: rc={r.returncode}, {r.stdout}')
  209      require(f.pointers() == before, 'read-only state changed pointers')
  210      for name in files:
  211          expected = 'layout=2\n' if name.endswith('/.layout') else 'sentinel\n'
  212          require((f.path/'cloud'/name.lstrip('/')).read_text() == expected, 'state changed cloud bytes')
  213  
  214  
  215  def actor_case(f, cell, actor, saves, files, dirs, keep):
  216      """Exercise the script boundary each UI actor uses, with independent oracles.
  217  
  218      These are host call-path checks. The guest runner proves that ES actually
  219      invokes them in the right order and presents the corresponding outcome.
  220      """
  221      parent = '/GAMES' if saves == '/GAMES' else saves.rsplit('/', 1)[0]
  222      backups = '/GAMES/backup' if saves == '/GAMES' else parent+'/Backups'
  223      f.conf(saves, backups, '' if cell=='T21' else parent+'/Content', keep)
  224      for name in files:
  225          if name.endswith('_SETTINGS.tar.gz'): f.archive(name)
  226          else: f.file(name, 'layout=2\n' if name.endswith('/.layout') else name+' payload\n')
  227      for name in dirs:
  228          f.directory(name)
  229      put(f.path/'storage/roms/gb/Local.srm', 'local progress\n')
  230      before = cloud_hashes(f)
  231      initial = f.pointers()
  232      scanned = {'T03': OLD+'/Saves', 'T10': OLD+'/Saves',
  233                 'T11': OLD+'/Saves', 'T12': NEW+'/Saves', 'T20':NEW+'/Saves'}.get(cell, saves)
  234      eligible = cell in ('T04','T05','T06','T07','T08','T09','T10','T11','T12','T20','T21','T22')
  235      target = saves
  236      if actor in ('boot', 'startup-restore', 'startup-backup'):
  237          gate = f.run('cloud_migrate_layout', '--needs-step')
  238          require(gate.returncode == (0 if eligible else 1), f'{cell}: wrong boot eligibility: {gate.returncode}')
  239          if eligible:
  240              r = f.run('cloud_scan', '--folder')
  241              require(r.returncode == 0, f'{cell}: boot preparation failed: {r.stdout[-300:]}')
  242              target = scanned
  243      elif actor in ('wizard', 'transfer'):
  244          r = f.run('cloud_scan', '--folder')
  245          require(r.returncode == 0, f'{cell}: folder scan failed: {r.stdout[-300:]}')
  246          target = scanned
  247      if actor == 'wizard':
  248          # NOT NOW on MOVE; finishing the wizard still seeds its settled paths.
  249          r = f.run('cloud_setup', '--seed-folders')
  250          require(r.returncode == 0, f'{cell}: wizard seeding failed: {r.stdout[-300:]}')
  251          if cell in ('T07','T08','T09'):
  252              target = NEW+'/Saves'
  253          require((f.path/'cloud'/target.lstrip('/')).is_dir(), 'wizard did not seed its chosen saves folder')
  254      elif actor in ('startup-restore','saves-restore'):
  255          args = ['--yes','--method=copy','--update','--saves-only']
  256          if actor == 'startup-restore': args += ['--automatic']
  257          r = f.run('cloud_restore', *args)
  258          present = (f.path/'cloud'/target.lstrip('/')).is_dir()
  259          if present:
  260              require(r.returncode == 0, f'{cell}: restore of present folder failed: {r.stdout[-300:]}')
  261          else:
  262              require(r.returncode != 0 or '>>> offer create-saves-folder' in r.stdout,
  263                      f'{cell}: absent folder reported successful restore without an offer')
  264          for name in files:
  265              if name.startswith(target+'/') and name.endswith('.srm'):
  266                  dest = f.path/'storage/roms'/name[len(target)+1:]
  267                  require(dest.exists() and dest.read_text() == name+' payload\n', f'{cell}: restore missed {name}')
  268          require((f.path/'storage/roms/gb/Local.srm').read_text() == 'local progress\n', 'restore removed local progress')
  269      elif actor in ('startup-backup','exit','saves-backup'):
  270          args = ['--yes','--saves-only']
  271          if actor == 'startup-backup': args += ['--method=copy','--update','--automatic']
  272          if actor == 'exit': args += ['--recent','--automatic']
  273          present = (f.path/'cloud'/target.lstrip('/')).is_dir()
  274          writes = present or target not in ('/GAMES',OLD+'/Saves')
  275          r = f.run('cloud_backup', *args)
  276          require(r.returncode == 0, f'{cell}: backup rc={r.returncode}: {r.stdout[-300:]}')
  277          dest = f.path/'cloud'/target.lstrip('/')/'gb/Local.srm'
  278          require(dest.exists() == writes, f'{cell}: backup wrote={dest.exists()}, permitted={writes}, target={target}')
  279          if writes:
  280              require(dest.read_text() == 'local progress\n', 'backup changed local save bytes')
  281          else:
  282              require('>>> offer create-saves-folder' in r.stdout, 'absent earlier folder did not produce an offer')
  283      require(f.pointers()['SAVES_REMOTE'] == target, f'{cell}/{actor}: expected {target}, got {f.pointers()["SAVES_REMOTE"]}')
  284      require(f.pointers()['LAYOUT_KEEP'] == keep, 'actor changed the deliberate keep choice')
  285      if cell == 'T20': require(f.pointers()['SETTINGS_REMOTE']==backups, 'actor abandoned independently populated settings tier')
  286      if cell == 'T21': require(f.pointers()['CONTENT_REMOTE']=='', 'actor replaced explicitly selected content root')
  287      after = cloud_hashes(f)
  288      require(all(after.get(name) == digest for name,digest in before.items()), 'actor changed existing cloud payloads')
  289      if actor in ('boot','transfer','startup-restore','saves-restore'):
  290          require(after == before, 'read/selection actor changed cloud bytes')
  291      if actor in ('exit','saves-backup','saves-restore'):
  292          require(f.pointers() == initial, 'direct saves actor performed an unrequested pointer transition')
  293  
  294  
  295  def settle_failure(f, rc):
  296      f.conf('/GAMES','/GAMES/backup', None)
  297      put(f.path/'repo/cloud_migrate_layout', f'#!/bin/sh\n[ "$1" = --settle ] && exit {rc}\nprintf "/GAMES\\n/ROCKNIX/Saves\\n"\n', True)
  298      before = f.pointers()
  299      r = f.run('cloud_setup', '--seed-folders')
  300      require(not any((f.path/'cloud').rglob('*')), f'failed settlement rc={rc} seeded cloud; caller={r.returncode}')
  301      require(f.pointers() == before, 'failed settlement changed pointers')
  302  
  303  
  304  def backup_tier(f, mode, root='/ROCKNIX', custom=False):
  305      saves = '/GAMES' if root == '/GAMES' else root+'/Saves'
  306      backups = '/Mine/Backups' if custom else root+('/backup' if root == '/GAMES' else '/Backups')
  307      f.conf(saves,backups,root+'/Content')
  308      archive = f.archive(f'{backups}/{DEVICE}/{ARCHIVE}')
  309      f.directory(NEW+'/Saves')
  310      r = f.run('cloud_migrate_layout', mode)
  311      require(r.returncode in (0,3), f'{mode}: {r.stdout}')
  312      pointer = f.pointers()['SETTINGS_REMOTE']
  313      found = f.path/'cloud'/pointer.lstrip('/')/DEVICE/ARCHIVE
  314      require(found.exists() and found.read_bytes() == archive.read_bytes(), f'archive abandoned by {mode}: {pointer}')
  315  
  316  
  317  def apply_other_source(f, custom=False):
  318      backups = '/Mine/Backups' if custom else '/GAMES/backup'
  319      f.conf('/GAMES', backups, '')
  320      archive = f.archive(f'{backups}/{DEVICE}/{ARCHIVE}')
  321      original = archive.read_bytes()
  322      f.file(OLD+'/Saves/gb/A.srm')
  323      r=f.run('cloud_migrate_layout','--apply')
  324      require(r.returncode==0, f'apply discovered source failed: {r.stdout[-600:]}')
  325      found=f.path/'cloud'/f.pointers()['SETTINGS_REMOTE'].lstrip('/')/DEVICE/ARCHIVE
  326      require(found.exists() and found.read_bytes()==original, 'discovered saves source abandoned the separate backup tier')
  327      require((f.path/'cloud/pixelelated/Saves/gb/A.srm').read_text()=='sentinel\n', 'save bytes lost')
  328      require(f.pointers()['CONTENT_REMOTE']=='', 'explicit root changed')
  329  
  330  
  331  def content_choice(f, mode, content):
  332      saves = NEW+'/Saves' if mode == '--join' else OLD+'/Saves'
  333      f.conf(saves, OLD+'/Backups', content)
  334      if mode == '--join': f.file(OLD+'/Saves/gb/A.srm')
  335      if mode == '--follow': f.directory(NEW+'/Saves')
  336      if content == '': f.file('/ROMs/gb/Root.gb')
  337      r = f.run('cloud_migrate_layout', mode)
  338      require(r.returncode in (0,3), f'{mode} rc={r.returncode}: {r.stdout[-300:]}')
  339      target = OLD+'/Content' if mode == '--join' else NEW+'/Content'
  340      expected = target if content is None or content == OLD+'/Content' else content
  341      require(f.pointers().get('CONTENT_REMOTE') == expected,
  342              f'{mode}, original={content!r}, got={f.pointers().get("CONTENT_REMOTE")!r}, expected={expected!r}')
  343      if content == '': require((f.path/'cloud/ROMs/gb/Root.gb').read_text() == 'sentinel\n', 'root content changed')
  344  
  345  
  346  def provider_failure(f, script, fault_rc=5, features=False, argv=('--yes',)):
  347      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  348      f.directory(OLD+'/Saves'); f.file(OLD+'/Saves/gb/A.srm')
  349      put(f.path/'storage/roms/gb/A.srm','sentinel\n')
  350      put(f.path/'ctl/bucket','1')
  351      f.fault(r'^backend features ' if features else r'^lsf --dirs-only qa:/ROCKNIX/?( |$)', fault_rc)
  352      before = (f.path/'cloud/ROCKNIX/Saves/gb/A.srm').read_bytes()
  353      r = f.run(script, *argv)
  354      require((f.path/'ctl/fault-fired').exists(), 'fault did not reach production call')
  355      require('>>> offer create-saves-folder' not in r.stdout, f'failed listing became absence in {script}')
  356      require((f.path/'cloud/ROCKNIX/Saves/gb/A.srm').read_bytes() == before, 'provider failure changed sentinel')
  357  
  358  
  359  def failure_actor(f, cell, actor):
  360      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  361      f.file(OLD+'/Saves/gb/A.srm')
  362      put(f.path/'storage/roms/gb/Local.srm','local progress\n')
  363      if cell == 'T19':
  364          put(f.path/'storage/.config/rclone/rclone.conf','')
  365      else:
  366          # Provider reads and writes fail, while local remote discovery works.
  367          f.fault(r'^(lsf|lsd|copy|mkdir|rcat) ')
  368      before=cloud_hashes(f),f.pointers()
  369      if actor == 'wizard':
  370          r=f.run('cloud_setup','--seed-folders')
  371      elif actor in ('transfer','boot','startup-restore','startup-backup'):
  372          if actor != 'transfer':
  373              gate=f.run('cloud_migrate_layout','--needs-step')
  374              require(gate.returncode==(1 if cell=='T19' else 0), 'wrong eligibility on missing/unreadable remote')
  375              if actor == 'boot' and cell == 'T19':
  376                  require((cloud_hashes(f),f.pointers())==before, 'unlinked boot changed state')
  377                  return
  378          # Startup's preflight failure prevents both transfer halves.
  379          if cell != 'T19' or actor in ('transfer','boot'):
  380              r=f.run('cloud_scan','--folder')
  381          else:
  382              script='cloud_restore' if actor=='startup-restore' else 'cloud_backup'
  383              r=f.run(script,'--yes','--saves-only','--automatic')
  384      else:
  385          script='cloud_restore' if actor=='saves-restore' else 'cloud_backup'
  386          argv=['--yes','--saves-only']+(['--automatic','--recent'] if actor=='exit' else [])
  387          r=f.run(script,*argv)
  388      require(r.returncode != 0, f'{cell}/{actor}: unavailable cloud reported success: {r.stdout[-300:]}')
  389      require('>>> offer create-saves-folder' not in r.stdout, 'unreadable/unlinked cloud became an absent-folder offer')
  390      require((cloud_hashes(f),f.pointers())==before, 'failed actor changed bytes/pointers')
  391  
  392  
  393  def bucket_layout_actor(f, actor):
  394      put(f.path/'ctl/bucket','1')
  395      f.fault(r'^lsf --dirs-only qa:/ROCKNIX/?( |$)')
  396      actor_case(f,'T04',actor,OLD+'/Saves',[OLD+'/Saves/gb/A.srm'],[],'')
  397      require(not (f.path/'ctl/fault-fired').exists(), 'layout actor unexpectedly required the direct-transfer parent probe')
  398  
  399  
  400  def unreadable(f):
  401      f.conf('/GAMES','/GAMES/backup',None)
  402      f.directory('/ROCKNIX')
  403      f.fault(r'^lsf .*qa:/ROCKNIX')
  404      before=f.pointers()
  405      r=f.run('cloud_migrate_layout','--settle')
  406      require(r.returncode not in (0,3) and f.pointers()==before, 'unreadable cloud became empty/changed pointers')
  407  
  408  
  409  def follow_read_failure(f):
  410      f.conf(OLD+'/Saves',OLD+'/Backups',OLD+'/Content')
  411      f.file(NEW+'/Saves/gb/A.srm')
  412      f.archive(f'{OLD}/Backups/{DEVICE}/{ARCHIVE}')
  413      f.fault(r'^lsf .*qa:/ROCKNIX/Backups/')
  414      before=f.pointers()
  415      r=f.run('cloud_scan','--folder')
  416      require((f.path/'ctl/fault-fired').exists(), 'follow read fault was not exercised')
  417      require(r.returncode != 0 and f.pointers()==before, 'failed follow was reported as a successful scan')
  418  
  419  
  420  def follow_call_failure(f):
  421      f.conf(OLD+'/Saves',OLD+'/Backups',OLD+'/Content')
  422      f.file(NEW+'/Saves/gb/A.srm')
  423      tool=f.path/'repo/cloud_migrate_layout'
  424      tool.rename(tool.with_name('cloud_migrate_layout.real'))
  425      put(tool, '#!/bin/sh\nif [ "$1" = --follow ]; then echo follow > /ctl/fault-fired; exit 5; fi\nexec /repo/cloud_migrate_layout.real "$@"\n',True)
  426      before=f.pointers()
  427      r=f.run('cloud_scan','--folder')
  428      require((f.path/'ctl/fault-fired').exists(), 'follow call fault was not exercised')
  429      require(r.returncode != 0 and f.pointers()==before, 'failed follow call was reported as a successful scan')
  430  
  431  
  432  def note_only(f):
  433      f.conf('/GAMES','/GAMES/backup',None)
  434      f.file('/GAMES/README.txt','setup note\n')
  435      f.file(OLD+'/Saves/gb/A.srm')
  436      r=f.run('cloud_scan','--folder')
  437      require(r.returncode==0, f'scan failed: {r.stdout}')
  438      require(f.pointers()['SAVES_REMOTE']==OLD+'/Saves', 'setup note outranked the real saves')
  439      require((f.path/'cloud/GAMES/README.txt').read_text()=='setup note\n', 'old note deleted')
  440      require((f.path/'cloud/ROCKNIX/Saves/gb/A.srm').read_text()=='sentinel\n', 'real saves changed')
  441  
  442  
  443  def no_remote(f):
  444      put(f.path/'storage/.config/rclone/rclone.conf','')
  445      r=f.run('cloud_scan')
  446      require(r.returncode != 0 and not (f.path/'storage/.cache/cloud_sync/scan/done').exists(), 'unlinked scan succeeded')
  447  
  448  
  449  def no_remote_local_path(f, script, failed_read=False):
  450      put(f.path/'storage/.config/rclone/rclone.conf','')
  451      f.conf('/storage/not-a-cloud','/storage/not-settings','')
  452      put(f.path/'storage/not-a-cloud/gb/Remote.srm','local-only sentinel\n')
  453      put(f.path/'storage/roms/gb/Local.srm','local progress\n')
  454      if failed_read: f.fault(r'^listremotes( |$)')
  455      r=f.run(script,'--yes','--saves-only')
  456      require(r.returncode != 0 and "YOUR CLOUD STORAGE ISN'T SET UP YET" in r.stdout,
  457              'empty/failed remote discovery did not refuse with its setup outcome')
  458      require(not (f.path/'storage/not-a-cloud/gb/Local.srm').exists() and
  459              not (f.path/'storage/roms/gb/Remote.srm').exists(), 'unlinked transfer used a local path as its cloud')
  460      require((f.path/'storage/not-a-cloud/gb/Remote.srm').read_text()=='local-only sentinel\n', 'unlinked transfer changed local-only bytes')
  461  
  462  
  463  def collision(f):
  464      f.conf(OLD+'/Saves',OLD+'/Backups',OLD+'/Content')
  465      f.file(OLD+'/Saves/gb/A.srm'); f.file(OLD+'/Content/ROMs/gb/A.gb')
  466      f.file(NEW+'/Content/ROMs/gb/A.gb','unrelated\n')
  467      r=f.run('cloud_migrate_layout','--apply')
  468      require(r.returncode != 0, 'unmarked content collision not refused')
  469      require((f.path/'cloud/pixelelated/Content/ROMs/gb/A.gb').read_text()=='unrelated\n', 'unrelated content overwritten')
  470      # Record partially advanced pointers for the recovery proof, rather than assuming atomic migration.
  471  
  472  
  473  def cloud_hashes(f):
  474      root = f.path/'cloud'
  475      return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
  476              for p in sorted(root.rglob('*')) if p.is_file()}
  477  
  478  
  479  def marker_refusal(f, marker, mode):
  480      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  481      f.file(NEW+'/.layout', marker)
  482      f.file(NEW+'/Saves/gb/Fleet.srm', 'fleet progress\n')
  483      if mode == '--apply':
  484          f.file(OLD+'/Saves/gb/A.srm')
  485      before = cloud_hashes(f), f.pointers()
  486      script, arg = {'seed':('cloud_setup','--seed-folders'),
  487                     'scan':('cloud_scan','--folder')}.get(mode, ('cloud_migrate_layout',mode))
  488      r = f.run(script, arg)
  489      require(r.returncode not in (0,3), f'unsupported marker was accepted by {mode}')
  490      require((cloud_hashes(f), f.pointers()) == before,
  491              f'unsupported marker {marker!r} changed bytes/pointers through {mode}: rc={r.returncode}')
  492      require('Done.' not in r.stdout, 'unsupported marker reported completion')
  493  
  494  
  495  def truncated_migration_retry(f, stage='Backups', kind='prefix'):
  496      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  497      names = {'Backups': "QA/Kid's settings.tar.gz", 'Saves': "gb/Kid's Game.srm",
  498               'Saves-replaced': "gb/Kid's Game.srm", 'Content': "ROMs/gb/Kid's Game.gb"}
  499      payloads = {tier+'/'+name: 'original '+tier+' payload, every byte survives\n' for tier,name in names.items()}
  500      sibling = stage+'/'+names[stage]+'.complete'
  501      payloads[sibling] = 'completed sibling witness\n'
  502      for name,data in payloads.items(): f.file(OLD+'/'+name,data)
  503      f.fault(r'^copy qa:/ROCKNIX/'+re.escape(stage)+r'/? ')
  504      first=f.run('cloud_migrate_layout','--apply')
  505      require(first.returncode!=0 and (f.path/'ctl/fault-fired').exists(),'initial copy fault not reached')
  506      record=f.path/'storage/.config/cloud-layout-migration.json'
  507      require(record.is_file(),'production did not retain original binding')
  508      (f.path/'ctl/faults').unlink();(f.path/'ctl/fault-fired').unlink()
  509      name=stage+'/'+names[stage];full=payloads[name]
  510      partial=full[:9] if kind!='empty' else ''
  511      if kind=='different':partial='DIFFERENT'
  512      if kind=='longer':partial=full+'foreign tail'
  513      if kind=='same-size':partial='X'*len(full)
  514      if kind=='complete':partial=full
  515      f.file(NEW+'/'+name,partial);f.file(NEW+'/'+sibling,payloads[sibling])
  516      if kind=='extra':f.file(NEW+'/'+stage+'/foreign.srm','another player\n')
  517      if kind=='missing':(f.path/'cloud/ROCKNIX'/name).unlink()
  518      if kind=='changed-complete':f.file(NEW+'/'+sibling,'X'*len(payloads[sibling]))
  519      if kind=='no-record':record.unlink()
  520      if kind=='wrong-binding':
  521          data=json.loads(record.read_text());data['fingerprint']='0'*64;record.write_text(json.dumps(data)+'\n')
  522      if kind in ('read-source','read-destination','list-source','list-destination'):
  523          root=OLD if kind.endswith('source') else NEW
  524          prefix='cat qa:'+root+'/'+name if kind.startswith('read-') else 'lsjson qa:'+root+'/'+stage
  525          f.fault('^'+re.escape(prefix)+' ')
  526      before=cloud_hashes(f),f.pointers()
  527      second=f.run('cloud_migrate_layout','--apply')
  528      if kind not in ('prefix','empty','complete'):
  529          require(second.returncode!=0 and (cloud_hashes(f),f.pointers())==before,
  530                  kind+' changed bytes/pointers or accepted a foreign/unreadable destination')
  531          if kind.startswith(('read-','list-')):require((f.path/'ctl/fault-fired').exists(),kind+' did not reach the read failure')
  532          return
  533      require(second.returncode==0,'truncated retry did not complete: '+second.stdout[-500:])
  534      for name,data in payloads.items():
  535          target=f.path/'cloud/pixelelated'/name
  536          require(target.is_file() and target.read_text()==data,'retry lost '+name)
  537          require(not (f.path/'cloud/ROCKNIX'/name).exists(),'retry left old '+name)
  538      require(not record.exists() and (f.path/'cloud/pixelelated/.layout').read_text()=='layout=2\n',
  539              'retry did not finish recovery record/marker')
  540  
  541  
  542  def truncated_fresh_content(f):
  543      f.conf(OLD+'/Saves',OLD+'/Backups',OLD+'/Content')
  544      f.file(OLD+'/Saves/gb/A.srm','original save\n')
  545      f.file(OLD+'/Backups/QA/settings.tar.gz','original settings\n')
  546      f.file(OLD+'/Content/ROMs/gb/A.gb','original game bytes\n')
  547      f.file(NEW+'/Content/ROMs/gb/A.gb','original')
  548      before=cloud_hashes(f),f.pointers()
  549      for attempt in range(2):
  550          r=f.run('cloud_migrate_layout','--apply')
  551          require(r.returncode!=0 and (cloud_hashes(f),f.pointers())==before,
  552                  'fresh content prefix collision changed bytes/pointers on attempt '+str(attempt))
  553          require(not (f.path/'storage/.config/cloud-layout-migration.json').exists(),
  554                  'refused foreign prefix created recovery authority for a later retry')
  555  
  556  
  557  def migration_retry(f, stage, operation='copy', legacy_record=False):
  558      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  559      payloads = {'Backups/QA/settings.tar.gz': 'settings bytes\n',
  560                  'Saves/gb/A.srm': 'save bytes\n',
  561                  'Saves-replaced/gb/A.srm': 'previous progress\n',
  562                  'Content/ROMs/gb/A.gb': 'game bytes\n'}
  563      for name, data in payloads.items():
  564          f.file(OLD+'/'+name, data)
  565      pattern = r'^rcat qa:/pixelelated/\.layout ' if stage == 'marker' else (
  566          r'^'+operation+r' qa:/ROCKNIX/'+re.escape(stage)+r'/? ')
  567      f.fault(pattern)
  568      first = f.run('cloud_migrate_layout', '--apply')
  569      require((f.path/'ctl/fault-fired').exists(), f'{stage} fault never reached production call')
  570      require(first.returncode != 0, f'{stage} failure reported success: {first.stdout[-400:]}')
  571      require(not (f.path/'cloud/pixelelated/.layout').exists(), 'incomplete migration published marker')
  572      if legacy_record:
  573          record=f.path/'storage/.config/cloud-layout-migration.json'
  574          data=json.loads(record.read_text())
  575          data['source'].pop('discarded',None)
  576          record.write_text(json.dumps(data)+'\n')
  577      for name, data in payloads.items():
  578          copies = [f.path/'cloud'/root/name for root in ['ROCKNIX', 'pixelelated']]
  579          require(any(p.exists() and p.read_text()==data for p in copies), f'{stage} lost {name} before retry')
  580      pending = f.run('cloud_migrate_layout', '--needs-step')
  581      state = f.run('cloud_scan', '--folder')
  582      require(pending.returncode==0 and state.returncode==0 and
  583              'STATE=migration-pending' in (f.path/'storage/.cache/cloud_sync/scan/state').read_text(),
  584              f'{stage} interrupted move is not offered for retry')
  585      (f.path/'ctl/faults').unlink()
  586      before=cloud_hashes(f),f.pointers()
  587      seeded=f.run('cloud_setup','--seed-folders')
  588      require(seeded.returncode != 0 and (cloud_hashes(f),f.pointers())==before,
  589              'wizard seeded over an unfinished migration')
  590      # A completed tier remains usable after a failed move. All direct actors
  591      # keep the selected pointer; neither a retry record nor startup preparation
  592      # may make them change the marker or delete an old tier behind the mover.
  593      for script,argv in [
  594          ('cloud_restore',['--yes','--saves-only','--method=copy','--update','--automatic']),
  595          ('cloud_backup',['--yes','--saves-only','--method=copy','--update','--automatic']),
  596          ('cloud_backup',['--yes','--saves-only','--recent','--automatic']),
  597          ('cloud_restore',['--yes','--saves-only']),('cloud_backup',['--yes','--saves-only'])]:
  598          r=f.run(script,*argv)
  599          require(r.returncode in (0,9) and (cloud_hashes(f),f.pointers())==before,
  600                  f'{stage}: direct {script} altered an unfinished layout: {r.stdout[-250:]}')
  601      # An OAuth refresh can rewrite this field without changing the cloud.
  602      with (f.path/'storage/.config/rclone/rclone.conf').open('a') as config:
  603          refreshed = {'access' + '_token': '<synthetic-refreshed>'}
  604          config.write('token = ' + json.dumps(refreshed) + '\n')
  605      second = f.run('cloud_migrate_layout', '--apply')
  606      require(second.returncode in (0,3), f'{stage} retry failed: {second.stdout[-500:]}')
  607      require((f.path/'cloud/pixelelated/.layout').is_file() and
  608              (f.path/'cloud/pixelelated/.layout').read_text()=='layout=2\n', f'{stage} retry did not commit marker')
  609      for name, data in payloads.items():
  610          p = f.path/'cloud/pixelelated'/name
  611          require(p.is_file() and p.read_text()==data, f'{stage} retry abandoned {name}')
  612          require(not (f.path/'cloud/ROCKNIX'/name).exists(), f'{stage} retry left duplicate {name}')
  613      before = cloud_hashes(f), f.pointers()
  614      again = f.run('cloud_migrate_layout', '--apply')
  615      require(again.returncode in (0,3) and (cloud_hashes(f), f.pointers())==before,
  616              f'{stage} repeated completed migration changed data')
  617      # A separate device has only its old pointers, none of the mover's local state.
  618      shutil.rmtree(f.path/'storage/.cache/cloud_sync')
  619      (f.path/'storage/.cache/cloud_sync').mkdir()
  620      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  621      follower = f.run('cloud_migrate_layout', '--follow')
  622      require(follower.returncode==0 and f.pointers()['SAVES_REMOTE']==NEW+'/Saves',
  623              f'{stage} second device could not follow committed layout')
  624      require(cloud_hashes(f)==before[0], 'following the completed migration changed cloud data')
  625  
  626  
  627  def predecessor_retry(f, stage, interrupt_again=False):
  628      """The old script creates the inherited state; never hand-draw its pointers."""
  629      predecessor, ref = 'RC2', '69e6039f8f'
  630      source = '/GAMES'
  631      backups = '/GAMES/backup'
  632      content = '/GAMES/Content'
  633      f.conf(source, backups, content)
  634      payloads = {backups+'/QA/settings.tar.gz':'settings bytes\n',
  635                  source+'/gb/A.srm':'save bytes\n', content+'/ROMs/gb/A.gb':'game bytes\n',
  636                  source+'-replaced/stamp/gb/A.srm':'historical progress\n'}
  637      for name,data in payloads.items(): f.file(name,data)
  638      tool = f.path/'repo/cloud_migrate_layout'
  639      candidate = tool.read_bytes()
  640      old = subprocess.run(['git','-C',str(ROOT),'show',f'{ref}:{SOURCES}/cloud_migrate_layout'],
  641                           capture_output=True,check=True).stdout
  642      tool.write_bytes(old)
  643      targets = {'backups':backups, 'saves':source, 'discarded':source+'-replaced', 'content':content}
  644      if stage != 'complete':
  645          pattern = r'^rcat qa:/pixelelated/\.layout ' if stage == 'marker' else r'^copy qa:'+re.escape(targets[stage])+r'/? '
  646          f.fault(pattern)
  647      first = f.run('cloud_migrate_layout','--apply')
  648      if stage != 'complete':
  649          require((f.path/'ctl/fault-fired').exists(), f'{predecessor}/{stage}: fault was not reached')
  650          (f.path/'ctl/faults').unlink()
  651      (f.path/'predecessor.json').write_text(json.dumps(dict(ref=ref,
  652          script_sha256=hashlib.sha256(old).hexdigest(), rc=first.returncode,
  653          pointers=f.pointers(), cloud=cloud_hashes(f)),indent=2)+'\n')
  654      require(not (f.path/'storage/.config/cloud-layout-migration.json').exists(), 'old binary unexpectedly wrote new-format recovery state')
  655      tool.write_bytes(candidate)
  656      if interrupt_again:
  657          f.fault(r'^rcat qa:/pixelelated/\.layout ')
  658          failed=f.run('cloud_migrate_layout','--apply')
  659          require(failed.returncode != 0 and (f.path/'storage/.config/cloud-layout-migration.json').exists(),
  660                  'interrupted predecessor recovery lost its record')
  661          (f.path/'ctl/faults').unlink()
  662      retry = f.run('cloud_migrate_layout','--apply')
  663      require(retry.returncode in (0,3), f'{predecessor}/{stage}: upgrade retry failed: {retry.stdout[-500:]}')
  664      expected = {'Backups/QA/settings.tar.gz':'settings bytes\n','Saves/gb/A.srm':'save bytes\n',
  665                  'Content/ROMs/gb/A.gb':'game bytes\n',
  666                  'Saves-replaced/stamp/gb/A.srm':'historical progress\n'}
  667      for name,data in expected.items():
  668          path=f.path/'cloud/pixelelated'/name
  669          require(path.is_file() and path.read_text()==data, f'{predecessor}/{stage}: upgrade left {name} behind')
  670      require((f.path/'cloud/pixelelated/.layout').read_text()=='layout=2\n'
  671              if (f.path/'cloud/pixelelated/.layout').exists() else False,
  672              f'{predecessor}/{stage}: completed upgrade has no current marker')
  673      before=cloud_hashes(f),f.pointers()
  674      require(not (f.path/'cloud/GAMES-replaced/stamp/gb/A.srm').exists(),
  675              f'{predecessor}/{stage}: successful first apply left historical saves behind')
  676      again=f.run('cloud_migrate_layout','--apply')
  677      require(again.returncode in (0,3) and (cloud_hashes(f),f.pointers())==before, 'repeated upgraded migration changed bytes/pointers')
  678  
  679  
  680  def historical_shelves(f, kind):
  681      """Real migration with both owned generations of discarded saves."""
  682      f.conf(OLD+'/Saves', OLD+'/Backups', OLD+'/Content')
  683      f.file(OLD+'/Saves/gb/Live.srm', 'live progress\n')
  684      f.file(OLD+'/Backups/QA/settings.tar.gz', 'settings bytes\n')
  685      f.file(OLD+'/Content/ROMs/gb/A.gb', 'game bytes\n')
  686      f.file(OLD+'/Saves-replaced/stamp/gb/A.srm', 'earlier ROCKNIX progress\n')
  687      f.file('/GAMES-replaced/stamp/gb/A.srm', 'earlier GAMES progress\n')
  688      before=cloud_hashes(f),f.pointers()
  689      if kind=='foreign':
  690          f.file(NEW+'/Saves-replaced/foreign.srm', 'unselected foreign history\n')
  691          before=cloud_hashes(f),f.pointers()
  692      elif kind=='active':
  693          f.file('/GAMES/gb/Other.srm', 'active earlier sibling\n')
  694      elif kind=='unreadable':
  695          # The real parent listing must prove this directory exists; otherwise
  696          # the product correctly classifies the failed child lookup as absent.
  697          f.directory('/GAMES')
  698          f.fault(r'^lsf .*qa:/GAMES/? ')
  699      elif kind in ('copy','delete'):
  700          f.fault(r'^'+kind+r' qa:/GAMES-replaced/? ')
  701      first=f.run('cloud_migrate_layout','--apply')
  702      if kind in ('foreign','unreadable'):
  703          require(first.returncode!=0 and (cloud_hashes(f),f.pointers())==before,
  704                  'unreadable source or unowned destination did not refuse before mutation')
  705          if kind=='unreadable': require((f.path/'ctl/fault-fired').exists(), 'listing fault never fired')
  706          return
  707      if kind in ('copy','delete'):
  708          record=f.path/'storage/.config/cloud-layout-migration.json'
  709          require(first.returncode!=0 and (f.path/'ctl/fault-fired').exists() and record.exists(),
  710                  'interrupted later history did not retain recovery state')
  711          retained=json.loads(record.read_text())
  712          require(retained['source']['discarded']=='/GAMES-replaced' and
  713                  retained['configured']['saves']==OLD+'/Saves',
  714                  'history retry lost its pending source or original selection binding')
  715          require((f.path/'cloud/GAMES-replaced/stamp/gb/A.srm').read_text()=='earlier GAMES progress\n',
  716                  'interrupted history lost source bytes')
  717          (f.path/'ctl/faults').unlink()
  718          first=f.run('cloud_migrate_layout','--apply')
  719      require(first.returncode==0, f'history move failed: {first.stdout[-600:]}')
  720      values=[p.read_text() for p in (f.path/'cloud/pixelelated').rglob('*.srm')]
  721      require('live progress\n' in values and 'earlier ROCKNIX progress\n' in values,
  722              'current live or historical progress lost')
  723      if kind=='active':
  724          require((f.path/'cloud/GAMES-replaced/stamp/gb/A.srm').read_text()=='earlier GAMES progress\n' and
  725                  (f.path/'cloud/GAMES/gb/Other.srm').read_text()=='active earlier sibling\n',
  726                  'active earlier sibling history moved')
  727      else:
  728          require('earlier GAMES progress\n' in values and
  729                  not (f.path/'cloud/GAMES-replaced/stamp/gb/A.srm').exists(),
  730                  'successful apply abandoned or overwrote the earlier history')
  731      require(not (f.path/'storage/.config/cloud-layout-migration.json').exists(), 'completed move retains pending record')
  732      before=cloud_hashes(f),f.pointers()
  733      again=f.run('cloud_migrate_layout','--apply')
  734      require(again.returncode in (0,3) and (cloud_hashes(f),f.pointers())==before,
  735              'completed history migration is not idempotent')
  736  
  737  
  738  def predecessor_boundaries(f, kind, active=False):
  739      # Current primary pointers with an inherited shelf; a chosen content
  740      # location remains independent even when its spelling ends in /Content.
  741      content = '' if kind == 'root' else '/Mine/Content'
  742      f.conf(content=content)
  743      f.file(NEW+'/Saves/gb/A.srm','current progress\n')
  744      # Distinguish an orphaned predecessor shelf from a live sibling's history.
  745      if active: f.file(OLD+'/Saves/gb/Other.srm','another device save\n')
  746      f.file(OLD+'/Backups/QA/other.tar.gz','another device backup\n')
  747      f.file(OLD+'/Saves-replaced/gb/A.srm','earlier progress\n')
  748      f.file((content or '')+'/ROMs/gb/A.gb','chosen content\n')
  749      if kind in ('foreign','fleet'):
  750          f.file(NEW+'/Saves-replaced/gb/A.srm','foreign progress\n')
  751      if kind == 'fleet': f.file(NEW+'/.layout','layout=2\n')
  752      before=cloud_hashes(f),f.pointers()
  753      state=f.run('cloud_scan','--folder')
  754      if active:
  755          require(state.returncode==0 and 'STATE=current' in
  756                  (f.path/'storage/.cache/cloud_sync/scan/state').read_text(), 'active sibling shelf was offered as this device recovery')
  757          for _ in range(2):
  758              applied=f.run('cloud_migrate_layout','--apply')
  759              require(applied.returncode in (0,3), 'settled current layout refused')
  760              after=cloud_hashes(f)
  761              require(all(after.get(name)==digest for name,digest in before[0].items()) and
  762                      set(after)-set(before[0]) <= {'pixelelated/.layout'} and f.pointers()==before[1],
  763                      'current device moved its active sibling history')
  764          f.fault(r'^lsf .*qa:/ROCKNIX/Saves/? ')
  765          refused=f.run('cloud_migrate_layout','--state')
  766          require(refused.returncode != 0 and (f.path/'ctl/fault-fired').exists(), 'unreadable earlier saves became an orphaned shelf')
  767          return
  768      require(state.returncode==0 and 'STATE=migration-pending' in
  769              (f.path/'storage/.cache/cloud_sync/scan/state').read_text(), 'inherited shelf is not offered through transfer recovery')
  770      r=f.run('cloud_migrate_layout','--apply')
  771      if kind == 'foreign':
  772          require(r.returncode != 0 and (cloud_hashes(f),f.pointers())==before,
  773                  'unmarked conflicting recovery shelf was overwritten')
  774          return
  775      require(r.returncode in (0,3), f'{kind}: recovery failed: {r.stdout[-400:]}')
  776      require(f.pointers()['CONTENT_REMOTE']==content, 'recovery changed an independent content choice')
  777      for name,data in [('Backups/QA/other.tar.gz','another device backup\n')]:
  778          require((f.path/'cloud/ROCKNIX'/name).is_file() and
  779                  (f.path/'cloud/ROCKNIX'/name).read_text()==data,
  780                  'recovering the shelf moved an unselected live tier')
  781          require(not (f.path/'cloud/pixelelated'/name).exists(),
  782                  'recovering the shelf copied an unselected live tier')
  783      require((f.path/'cloud'/((content or '')+'/ROMs/gb/A.gb').lstrip('/')).read_text()=='chosen content\n',
  784              'recovery moved independent content bytes')
  785      values=[p.read_text() for p in (f.path/'cloud/pixelelated').rglob('*.srm')]
  786      require('current progress\n' in values and 'earlier progress\n' in values, 'recovery lost a progress version')
  787      if kind == 'fleet': require('foreign progress\n' in values, 'marked merge lost the other progress version')
  788  
  789  
  790  def content_discovery(f, kind):
  791      layouts={
  792          'empty':('/Mine',[],'empty',''),
  793          'unrelated':('/Mine',['Mine/Photos/x.jpg'],'empty',''),
  794          'fallback':('/Mine',['Mine/Photos/x.jpg','pixelelated/Content/ROMs/gb/A.gb'],'found-elsewhere',NEW+'/Content'),
  795          'tiered':('/Mine',['Mine/ROMs/gb/A.gb'],'ok',''),
  796          'root-tiered':('', ['ROMs/gb/A.gb'],'ok',''),
  797          'root-flat':('', ['gb/A.gb'],'ok',''),
  798          'root-unrelated':('', ['Photos/x.jpg'],'empty',''),
  799          'stranded':('/Mine',['gb/A.gb'],'stranded-at-root','/'),
  800          'refused':('/Mine',['Mine/ROMs/gb/A.gb'],'unreadable',None),
  801      }
  802      content,files,state,found=layouts[kind]
  803      f.conf(content=content)
  804      put(f.path/'storage/.config/emulationstation/es_systems.cfg', '<systemList>\n<path>/storage/roms/gb</path>\n</systemList>\n')
  805      for name in files: f.file(name,'game\n')
  806      if kind=='refused': f.fault(r'^lsf --dirs-only qa:Mine ')
  807      before=cloud_hashes(f),f.pointers()
  808      result=f.run('cloud_setup','--content-location')
  809      facts=dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
  810      require(facts.get('STATE')==state and (found is None or facts.get('FOUND')==found), f'{kind}: {result.stdout}')
  811      require((cloud_hashes(f),f.pointers())==before,'classification mutated state')
  812      require((result.returncode != 0)==(kind=='refused'), 'wrong classification status')
  813      if kind=='stranded':
  814          chosen=f.run('cloud_setup','--use-content-root')
  815          require(chosen.returncode==0 and f.pointers()['CONTENT_REMOTE']=='', 'root choice did not persist')
  816      if kind in ('root-flat','stranded'):
  817          scanned=f.run('cloud_content_restore','--scan')
  818          require(scanned.returncode==0 and re.search(r'^gb\|5\|1\|',scanned.stdout,re.M), 'root game missing or incorrectly unsupported in actual scan: '+scanned.stdout)
  819          require(cloud_hashes(f)==before[0], 'selection or scan changed cloud bytes')
  820  
  821  
  822  def legacy_content_support(f, kind):
  823      f.conf(content='')
  824      put(f.path/'storage/.config/emulationstation/es_systems.cfg',
  825          '<systemList>\n<path>/storage/roms/gb</path>\n</systemList>\n')
  826      name='gb' if kind in ('supported','tiered') else 'bios' if kind=='bios' else 'unsupported_qa'
  827      if kind in ('unsupported','bios'): (f.path/'storage/roms'/name).mkdir()
  828      prefix='ROMs/' if kind=='tiered' else ''
  829      filename='firmware.bin' if kind=='bios' else 'A.gb'
  830      f.file(prefix+name+'/'+filename,'game\n')
  831      before=cloud_hashes(f),f.pointers()
  832      scanned=f.run('cloud_content_restore','--scan')
  833      rows=[line.split('|') for line in scanned.stdout.splitlines() if line.startswith(name+'|')]
  834      matches=[row for row in rows if row[1]=='5']
  835      require(scanned.returncode==0 and len(matches)==1 and matches[0][2]==('0' if kind=='unsupported' else '1'),
  836              f'{kind}: incorrect system compatibility: {scanned.stdout}')
  837      require((cloud_hashes(f),f.pointers())==before,'read-only content scan changed state')
  838      if kind in ('supported','tiered'):
  839          chosen=f.run('cloud_content_restore','--set-systems','gb')
  840          restored=f.run('cloud_content_restore','--selected')
  841          target=f.path/'storage/roms/gb/A.gb'
  842          require(chosen.returncode==0 and restored.returncode==0 and target.is_file() and target.read_text()=='game\n',
  843                  'selected supported content did not restore its actual bytes')
  844          require(cloud_hashes(f)==before[0], 'restore changed source cloud bytes')
  845  
  846  
  847  def content_folder_names(f, name):
  848      f.file(name+'/ROMs/gb/A.gb','game\n')
  849      initial=cloud_hashes(f)
  850      listing=f.run('cloud_scan')
  851      require(listing.returncode==0 and name in (f.path/'storage/.cache/cloud_sync/scan/root-dirs').read_text().splitlines(), 'chooser does not offer existing folder')
  852      selected=f.run('cloud_setup','--set-content-remote',name)
  853      require(selected.returncode==0 and f.pointers()['CONTENT_REMOTE']=='/'+name, 'offered folder was refused')
  854      scanned=f.run('cloud_scan','--content')
  855      require(scanned.returncode==0 and re.search(r'^gb\|5\|',(f.path/'storage/.cache/cloud_sync/scan/scan').read_text(),re.M), 'selected game is not scanned')
  856      require(cloud_hashes(f)==initial, 'choosing folder changed cloud bytes')
  857      config=f.path/'storage/.config/cloud_sync.conf';before=config.read_bytes()
  858      for bad in ['/a/../b','/a/./b','/a//b','/two\nlines','/trailing\n','/tab\tname','/$HOME','/`id`','/quote"']:
  859          refused=f.run('cloud_setup','--set-content-remote',bad)
  860          require(refused.returncode != 0 and config.read_bytes()==before,'unsafe path changed settings: '+repr(bad))
  861  
  862  
  863  def scan_reason(f, kind):
  864      expected="YOUR CLOUD FOLDER COULDN'T BE READ"
  865      if kind in ('future','malformed'):
  866          f.file(NEW+'/.layout','layout=999\n' if kind=='future' else 'layout=2\nextra\n')
  867      elif kind=='config':
  868          with (f.path/'storage/.config/cloud_sync.conf').open('a') as stream: stream.write('export SETTINGS_REMOTE="/Other"\n')
  869          expected="YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  870      elif kind=='record':
  871          put(f.path/'storage/.config/cloud-layout-migration.json','{invalid')
  872      elif kind=='write':
  873          f.file(OLD+'/Saves/gb/A.srm')
  874          put(f.path/'shim/mv','#!/bin/sh\nexit 1\n',True)
  875          expected="YOUR CLOUD SYNC SETTINGS COULDN'T BE SAVED"
  876      elif kind=='network':
  877          f.fault(r'^lsd qa: ',5); expected='YOUR CLOUD STOPPED ANSWERING'
  878      elif kind=='timeout':
  879          put(f.path/'shim/timeout','#!/bin/sh\nexit 124\n',True)
  880          expected='YOUR CLOUD STOPPED ANSWERING'
  881      before=cloud_hashes(f),(f.path/'storage/.config/cloud_sync.conf').read_bytes()
  882      result=f.run('cloud_scan','--folder')
  883      require(result.returncode != 0 and '>>> why '+expected in result.stdout,
  884              f'{kind}: lost application reason: {result.stdout}')
  885      require("COULDN'T FIND YOUR CLOUD FOLDER" not in result.stdout,'application failure mapped to missing directory')
  886      require((cloud_hashes(f),(f.path/'storage/.config/cloud_sync.conf').read_bytes())==before,'refusal changed cloud/settings')
  887  
  888  
  889  def reader_grammar(f, kind):
  890      forms={'escaped': 'SETTINGS_REMOTE="/Custom/My\\$Backups"',
  891             'single': "SETTINGS_REMOTE='/Custom/Backups' # comment",
  892             'bare': 'SETTINGS_REMOTE=/Custom/Backups # comment',
  893             'double': 'SETTINGS_REMOTE="/Custom/Backups" # comment',
  894             'duplicate': 'SETTINGS_REMOTE="/Custom/Backups"\nSETTINGS_REMOTE="/Other/Backups"',
  895             'export': 'export SETTINGS_REMOTE="/Custom/Backups"',
  896             'trailing': 'SETTINGS_REMOTE="/Custom/Backups" invalid',
  897             'control': 'SETTINGS_REMOTE="/Custom/Backups"\r'}
  898      config=f.path/'storage/.config/cloud_sync.conf'
  899      config.write_text(re.sub(r'^SETTINGS_REMOTE=.*$',lambda m:forms[kind],config.read_text(),flags=re.M))
  900      before=config.read_bytes(),cloud_hashes(f)
  901      for script,args in [('cloud_migrate_layout',['--state']),('cloud_scan',[])]:
  902          result=f.run(script,*args)
  903          require((result.returncode != 0)==(kind in ('export','trailing','control')), f'{kind}/{script}: {result.stdout[-400:]}')
  904      require((config.read_bytes(),cloud_hashes(f))==before, 'reader changed state')
  905      if kind in ('export','trailing','control'):
  906          argv=(f.path/'ctl/argv').read_text()
  907          require(not re.search(r'^(lsf|lsd|copy|rcat|mkdir) ',argv,re.M),'invalid settings reached provider')
  908  
  909  
  910  def atomic_pointers(f, mode, boundary):
  911      f.conf(NEW+'/Saves' if mode=='--join' else OLD+'/Saves',
  912             NEW+'/Backups' if mode=='--join' else OLD+'/Backups',
  913             NEW+'/Content' if mode=='--join' else OLD+'/Content')
  914      if mode=='--join': f.file(OLD+'/Saves/gb/A.srm')
  915      if mode=='--follow': f.file(NEW+'/Saves/gb/A.srm')
  916      config=f.path/'storage/.config/cloud_sync.conf'
  917      config.chmod(0o640)
  918      before=config.read_bytes(),cloud_hashes(f)
  919      command='mv' if boundary=='publish' else 'sed'
  920      match='[ "${!#}" = /storage/.config/cloud_sync.conf ]' if command=='mv' else f'[[ "$*" == *"^{boundary}="* ]]'
  921      put(f.path/'shim'/command, '#!/bin/bash\nif '+match+'; then echo fired > /ctl/pointer-fault; exit 1; fi\nexec /usr/bin/'+command+' "$@"\n', True)
  922      first=f.run('cloud_migrate_layout',mode)
  923      require(first.returncode != 0 and (f.path/'ctl/pointer-fault').exists(), 'pointer fault not reached')
  924      require((config.read_bytes(),cloud_hashes(f))==before, 'failed transition published part of its settings')
  925      (f.path/'shim'/command).unlink()
  926      retry=f.run('cloud_migrate_layout',mode)
  927      target=OLD if mode=='--join' else NEW
  928      require(retry.returncode==0, 'retry did not complete the transition')
  929      for key,suffix in [('SAVES_REMOTE','Saves'),('SETTINGS_REMOTE','Backups'),('CONTENT_REMOTE','Content')]:
  930          require(f.pointers()[key]==target+'/'+suffix, 'retry left mixed pointers: '+key)
  931      require(cloud_hashes(f)==before[1] and config.stat().st_mode & 0o777 == 0o640, 'transition changed cloud bytes or config permissions')
  932  
  933  
  934  def binding_rewrite(f, kind):
  935      f.conf(OLD+'/Saves',OLD+'/Backups',OLD+'/Content')
  936      f.file(OLD+'/Saves/gb/A.srm','save\n'); f.file(OLD+'/Content/ROMs/gb/A.gb','game\n')
  937      f.fault(r'^copy qa:/ROCKNIX/Content/? ')
  938      first=f.run('cloud_migrate_layout','--apply')
  939      record=f.path/'storage/.config/cloud-layout-migration.json'
  940      require(first.returncode != 0 and record.is_file() and (f.path/'ctl/fault-fired').exists(), 'move did not stop with recovery state')
  941      (f.path/'ctl/faults').unlink()
  942      config=f.path/'storage/.config/rclone/rclone.conf'; original=config.read_text()
  943      if kind.startswith('legacy'):
  944          data=json.loads(record.read_text());data.pop('fingerprint_format',None)
  945          data['fingerprint']=hashlib.sha256((original.rstrip('\n')+'\n').encode()).hexdigest()
  946          record.write_text(json.dumps(data)+'\n')
  947      before=cloud_hashes(f),f.pointers(),record.read_bytes()
  948      if kind=='endpoint':
  949          f.directory('/another-cloud'); config.write_text('[qa]\ntype = alias\nremote = /cloud/another-cloud\n')
  950      elif kind in ('comments','legacy-comments'):
  951          config.write_text(original+'\n# harmless comment\n')
  952      elif kind=='format':
  953          config.write_text('; harmless header\n[qa]\nremote=/cloud\n\ntype=alias\n')
  954      elif kind=='token':
  955          config.write_text(original+'token = {"access_token":"synthetic"}\n')
  956      state=f.run('cloud_migrate_layout','--state')
  957      if kind in ('endpoint','legacy-comments'):
  958          require(state.returncode==5 and 'NEEDS ITS ORIGINAL CONNECTION' in state.stdout, 'changed binding was not explained/refused')
  959          refused=f.run('cloud_migrate_layout','--apply')
  960          require(refused.returncode==5 and (cloud_hashes(f),f.pointers(),record.read_bytes())==before,
  961                  'changed binding changed data or rebound its record')
  962          seeded=f.run('cloud_setup','--seed-folders')
  963          require(seeded.returncode==5 and 'NEEDS ITS ORIGINAL CONNECTION' in seeded.stdout
  964                  and (cloud_hashes(f),f.pointers(),record.read_bytes())==before,
  965                  'seeding lost the binding reason or changed pending state')
  966          config.write_text(original) # Existing connection repair restores the original binding.
  967      else:
  968          require(state.returncode==0 and 'STATE=migration-pending' in state.stdout, 'harmless rewrite stranded pending move')
  969      resumed=f.run('cloud_migrate_layout','--apply')
  970      require(resumed.returncode==0, 'original binding could not resume: '+resumed.stdout[-300:])
  971      require((f.path/'cloud/pixelelated/Saves/gb/A.srm').read_text()=='save\n' and
  972              (f.path/'cloud/pixelelated/Content/ROMs/gb/A.gb').read_text()=='game\n', 'resume lost progress/content')
  973  
  974  
  975  def predecessor_content_only(f, empty=False):
  976      f.conf(content='/GAMES/Content')
  977      f.file(NEW+'/Saves/gb/A.srm','current save\n')
  978      f.file('/GAMES/gb/Other.srm','another device save\n')
  979      f.file('/GAMES/backup/QA/other.tar.gz','another device backup\n')
  980      if not empty: f.file('/GAMES/Content/ROMs/gb/A.gb','inherited content\n')
  981      before=cloud_hashes(f)
  982      preview=f.run('cloud_migrate_layout','--check')
  983      require(preview.returncode==0 and f'>>> plan {"none" if empty else "content"} /pixelelated' in preview.stdout,
  984              'current primary pointers planned unselected old live tiers')
  985      require(cloud_hashes(f)==before, 'preview changed cloud bytes')
  986      applied=f.run('cloud_migrate_layout','--apply')
  987      require(applied.returncode==0, 'content-only recovery failed')
  988      after=cloud_hashes(f)
  989      for name,digest in before.items():
  990          if '/Content/' not in name:
  991              require(after.get(name)==digest, 'content-only recovery changed an unselected live tier')
  992      require(f.pointers()['CONTENT_REMOTE']==NEW+'/Content', 'content pointer did not advance')
  993      if not empty:
  994          require((f.path/'cloud/pixelelated/Content/ROMs/gb/A.gb').read_text()=='inherited content\n',
  995                  'content-only recovery lost bytes')
  996  
  997  
  998  def restricted(f):
  999      f.file(NEW+'/Saves/gb/A.srm')
 1000      f.fault(r'^lsf .*qa: --')
 1001      r=f.run('cloud_scan','--folder')
 1002      require(r.returncode == 0, f'folder-only scan required root-list permission: {r.stdout}')
 1003  
 1004  
 1005  def restricted_actor(f, actor):
 1006      f.fault(r'^lsf .*qa: --')
 1007      actor_case(f,'T01',actor,NEW+'/Saves',[NEW+'/Saves/gb/A.srm'],[],'')
 1008      if actor == 'transfer':
 1009          # The folder scan does not need root directory enumeration. The full
 1010          # transfer scan also fills the content chooser; that request can fail,
 1011          # but must never change the saved pointer or cloud bytes.
 1012          before=cloud_hashes(f),f.pointers()
 1013          r=f.run('cloud_scan')
 1014          require((f.path/'ctl/fault-fired').exists() and r.returncode != 0,
 1015                  'full content chooser scan hid a restricted root-list failure')
 1016          require((cloud_hashes(f),f.pointers())==before, 'restricted full scan changed bytes/pointers')
 1017  
 1018  
 1019  def marker_direct_actor(f, actor):
 1020      f.file(NEW+'/.layout','layout=999\n')
 1021      actor_case(f,'T04',actor,OLD+'/Saves',[OLD+'/Saves/gb/A.srm'],[],'')
 1022      require((f.path/'cloud/pixelelated/.layout').read_text()=='layout=999\n', 'direct transfer rewrote a marker')
 1023  
 1024  
 1025  def local_archive(f, suffix):
 1026      put(f.path/'profile', 'export PATH=/shim:/repo:/usr/bin:/bin\nexport HOME=/storage\nexport OS_NAME=pixelelated\n')
 1027      put(f.path/'storage/.config/backuptool.conf', 'LOCATIONS=( /storage/.config/proof-sentinel )\n')
 1028      put(f.path/'storage/.config/proof-sentinel', 'before restore\n')
 1029      archive = f.archive(ARCHIVE.replace('ROCKNIX_SETTINGS', suffix+'_SETTINGS'), local=True)
 1030      original = archive.read_bytes()
 1031      r=f.run('backuptool','restore')
 1032      require(r.returncode==0, f'local {suffix} restore rc={r.returncode}: {r.stdout[-500:]}')
 1033      require((f.path/'storage/.config/proof-sentinel').read_text()=='settings sentinel\n', 'local restore sentinel mismatch')
 1034      snapshots=list((f.path/'storage/roms/backup/archive').glob('*PRE_RESTORE*'))
 1035      require(snapshots, 'pre-restore recovery snapshot absent')
 1036      with tarfile.open(snapshots[0]) as tar:
 1037          require(tar.extractfile('storage/.config/proof-sentinel').read()==b'before restore\n', 'snapshot lost previous bytes')
 1038      require(archive.read_bytes()==original, 'restore altered inherited archive')
 1039      r=f.run('backuptool','backup')
 1040      require(r.returncode==0, f'new local backup failed: {r.stdout[-400:]}')
 1041      names=list((f.path/'storage/roms/backup').glob('*_SETTINGS.tar.gz'))
 1042      require(any(n.name.endswith('-ROCKNIX_SETTINGS.tar.gz') for n in names), 'display rename changed persisted writer identity')
 1043  
 1044  
 1045  def main():
 1046      p=argparse.ArgumentParser(description=__doc__)
 1047      source = p.add_mutually_exclusive_group()
 1048      source.add_argument('--ref')
 1049      source.add_argument('--source-root',type=Path,help='checkout supplying actual working source bytes')
 1050      p.add_argument('--output',type=Path)
 1051      p.add_argument('--case',default='',help='substring of case name')
 1052      p.add_argument('--archives-only',action='store_true',help='only ordinary settings archive checks; no migration cases')
 1053      candidates = sorted(ROOT.parent.glob('*/build.*GENERIC_X64.x86_64/image/system/usr/bin/rclone'))
 1054      p.add_argument('--rclone',default=str(candidates[0]) if candidates else shutil.which('rclone'))
 1055      p.add_argument('--inject-failure',action='store_true')
 1056      p.add_argument('--list',action='store_true',help='list matching executable cases without running them')
 1057      args=p.parse_args()
 1058      if args.source_root:
 1059          args.source_root=args.source_root.resolve()
 1060      cases=[('T24-production-backup-scan-restore',archive_roundtrip),
 1061             ('T24-local-legacy-recovery',lambda f:local_archive(f,'ROCKNIX')),
 1062             ('T24-local-renamed-recovery',lambda f:local_archive(f,'pixelelated'))]
 1063      for kind in ['current','legacy','healed','flat','foreign']:
 1064          for branded in [False,True]:
 1065              cases.append((f'T24-{kind}-'+('renamed' if branded else 'legacy-os'),lambda f,k=kind,b=branded: archive_selection(f,k,b)))
 1066      archive_cases={name for name,fn in cases}
 1067      rows=[
 1068        ('T01',NEW+'/Saves','current',[NEW+'/Saves/gb/A.srm'],[],''),
 1069        ('T02',NEW+'/Saves','current',[],[],''),
 1070        ('T03',NEW+'/Saves','current',[OLD+'/Saves/gb/A.srm'],[],''),
 1071        ('T04',OLD+'/Saves','superseded-with-files',[OLD+'/Saves/gb/A.srm'],[],''),
 1072        ('T05',OLD+'/Saves','superseded-with-files',[OLD+'/Saves/gb/A.srm',NEW+'/.layout'],[NEW+'/Saves'],''),
 1073        ('T06',OLD+'/Saves','superseded-with-files',[OLD+'/Saves/gb/A.srm',NEW+'/Saves/gb/B.srm'],[],''),
 1074        ('T07','/GAMES','superseded-empty',[],[],''),
 1075        ('T08',OLD+'/Saves','superseded-empty',[],[],''),
 1076        ('T09','/GAMES','superseded-empty',[],['/GAMES'],''),
 1077        ('T10','/GAMES','superseded-with-files',[OLD+'/Saves/gb/A.srm'],[],''),
 1078        ('T11','/GAMES','superseded-with-files',[OLD+'/Saves/gb/A.srm'],['/GAMES'],''),
 1079        ('T12',OLD+'/Saves','superseded-empty',[NEW+'/Saves/gb/A.srm'],[],''),
 1080        ('T13',OLD+'/Saves','kept',[OLD+'/Saves/gb/A.srm'],[],OLD+'/Saves'),
 1081        ('T14',OLD+'/Saves','kept',[],[],OLD+'/Saves'),
 1082        ('T15','/Mine/Saves','own',['/Mine/Saves/gb/A.srm'],[],''),
 1083        ('T16','/Mine/Saves','own',[],[],''),
 1084        ('T20',OLD+'/Saves','superseded-empty',[OLD+'/Backups/'+DEVICE+'/'+ARCHIVE],[NEW+'/Saves'],''),
 1085        ('T21',OLD+'/Saves','superseded-with-files',[OLD+'/Saves/gb/A.srm','/ROMs/gb/A.gb'],[],''),
 1086        ('T22','/GAMES','superseded-with-files',['/GAMES/gb/A.srm',OLD+'/Saves/gb/B.srm'],[],''),
 1087        ('T24',NEW+'/Saves','current',[NEW+'/Saves/gb/A.srm',NEW+'/Backups/'+DEVICE+'/'+ARCHIVE],[],''),
 1088      ]
 1089      for cell,saves,state,files,dirs,keep in rows:
 1090          cases.append((cell+'-classification',lambda f,s=saves,t=state,fs=files,ds=dirs,k=keep: state_case(f,s,t,fs,ds,k)))
 1091          for actor in ['wizard','transfer','boot','startup-restore','startup-backup','exit','saves-restore','saves-backup']:
 1092              cases.append((cell+'-actor-'+actor,
 1093                            lambda f,c=cell,a=actor,s=saves,fs=files,ds=dirs,k=keep: actor_case(f,c,a,s,fs,ds,k)))
 1094      cases += [('T11-note-only',note_only),('T17-follow-call-failure',follow_call_failure),('T17-follow-read-failure',follow_read_failure),('T17-unreadable',unreadable),('T17-seed-timeout',lambda f:settle_failure(f,124)),
 1095                ('T17-seed-failed',lambda f:settle_failure(f,1)),
 1096                ('T18-bucket-backup-unknown',lambda f:provider_failure(f,'cloud_backup')),
 1097                ('T18-bucket-restore-unknown',lambda f:provider_failure(f,'cloud_restore')),
 1098                ('T19-no-remote',no_remote),('T23-content-collision',collision),('T25-restricted-prefix',restricted)]
 1099      for cell in ['T17','T19']:
 1100          for actor in ['wizard','transfer','boot','startup-restore','startup-backup','exit','saves-restore','saves-backup']:
 1101              cases.append((f'{cell}-actor-{actor}',lambda f,c=cell,a=actor:failure_actor(f,c,a)))
 1102      for actor,script,argv in [
 1103          ('startup-restore','cloud_restore',('--yes','--saves-only','--method=copy','--update','--automatic')),
 1104          ('startup-backup','cloud_backup',('--yes','--saves-only','--method=copy','--update','--automatic')),
 1105          ('exit','cloud_backup',('--yes','--saves-only','--automatic','--recent')),
 1106          ('saves-restore','cloud_restore',('--yes','--saves-only')),
 1107          ('saves-backup','cloud_backup',('--yes','--saves-only'))]:
 1108          cases.append((f'T18-actor-{actor}',lambda f,s=script,a=argv:provider_failure(f,s,argv=a)))
 1109      for actor in ['wizard','transfer','boot']:
 1110          cases.append((f'T18-actor-{actor}',lambda f,a=actor:bucket_layout_actor(f,a)))
 1111      for actor in ['wizard','transfer','boot','startup-restore','startup-backup','exit','saves-restore','saves-backup']:
 1112          cases.append((f'T25-actor-{actor}',lambda f,a=actor:restricted_actor(f,a)))
 1113      for script in ['cloud_backup','cloud_restore']:
 1114          for failed_read in [False,True]:
 1115              cases.append((f'T19-local-path-{script}-'+('failed-discovery' if failed_read else 'empty-config'),
 1116                            lambda f,s=script,e=failed_read:no_remote_local_path(f,s,e)))
 1117      for script in ['cloud_backup','cloud_restore']:
 1118          for rc in [3,4,7]:
 1119              cases.append((f'T18-{script}-parent-error-{rc}',lambda f,s=script,r=rc:provider_failure(f,s,r)))
 1120      cases.append(('T18-restore-features-error',lambda f:provider_failure(f,'cloud_restore',5,True)))
 1121      for mode in ['--follow','--settle']:
 1122          for root in [OLD,'/GAMES']:
 1123              cases.append((f'T20-{mode[2:]}-{root[1:]}',lambda f,m=mode,r=root:backup_tier(f,m,r)))
 1124          cases.append((f'T20-{mode[2:]}-custom',lambda f,m=mode:backup_tier(f,m,custom=True)))
 1125      cases += [('T20-apply-other-source-default',apply_other_source),
 1126                ('T20-apply-other-source-custom',lambda f:apply_other_source(f,True))]
 1127      for label, marker in [('malformed','layout=banana\n'), ('future','layout=999\n'),
 1128                            ('trailing','layout=2\nextra=unrecognized\n')]:
 1129          for mode in ['--apply','--follow','--settle','--join','--state','seed','scan']:
 1130              cases.append((f'T26-marker-{label}-{mode.lstrip("-")}',
 1131                            lambda f,m=marker,a=mode:marker_refusal(f,m,a)))
 1132      for actor in ['exit','saves-restore','saves-backup']:
 1133          cases.append((f'T26-direct-{actor}',lambda f,a=actor:marker_direct_actor(f,a)))
 1134      for stage in ['Backups','Saves','Saves-replaced','Content','marker']:
 1135          cases.append((f'T23-retry-{stage}',lambda f,s=stage:migration_retry(f,s)))
 1136      for stage in ['Backups','Saves','Saves-replaced','Content']:
 1137          cases.append((f'PL003-truncated-prefix-{stage}',lambda f,s=stage:truncated_migration_retry(f,s)))
 1138          if stage!='Backups':
 1139              cases.append((f'PL003-truncated-no-record-{stage}',lambda f,s=stage:truncated_migration_retry(f,s,kind='no-record')))
 1140      cases.append(('PL003-truncated-fresh-content',truncated_fresh_content))
 1141      for kind in ['empty','complete','different','longer','same-size','extra','missing',
 1142                   'changed-complete','no-record','wrong-binding','read-source','read-destination',
 1143                   'list-source','list-destination']:
 1144          cases.append((f'PL003-truncated-{kind}',lambda f,k=kind:truncated_migration_retry(f,kind=k)))
 1145      for stage in ['Backups','Saves','Saves-replaced','Content']:
 1146          cases.append((f'T23-retry-delete-{stage}',lambda f,s=stage:migration_retry(f,s,'delete')))
 1147      cases.append(('T23-retry-legacy-record',lambda f:migration_retry(f,'Saves-replaced',legacy_record=True)))
 1148      # D-WORKFLOW-144: only ROCKNIX RC2 is a fielded adoption predecessor.
 1149      # Unshipped run101 -> /Rasteratops cases remain in historical evidence;
 1150      # new-layout interruption/marker/discarded-shelf controls above stay active.
 1151      for stage in ['backups','saves','content','complete']:
 1152          cases.append((f'T23-predecessor-RC2-{stage}',
 1153                        lambda f,s=stage: predecessor_retry(f,s)))
 1154      cases.append(('T23-predecessor-RC2-reinterrupted',
 1155                    lambda f:predecessor_retry(f,'content',True)))
 1156      for kind in ['complete','copy','delete','active','foreign','unreadable']:
 1157          cases.append((f'PL003-historical-shelves-{kind}',lambda f,k=kind:historical_shelves(f,k)))
 1158      for kind in ['root','custom','foreign','fleet']:
 1159          cases.append((f'T23-predecessor-boundary-{kind}',lambda f,k=kind:predecessor_boundaries(f,k)))
 1160          cases.append((f'PL003-active-sibling-{kind}',lambda f,k=kind:predecessor_boundaries(f,k,True)))
 1161      for mode in ['--join','--follow','--settle']:
 1162          for boundary in ['SAVES_REMOTE','SETTINGS_REMOTE','CONTENT_REMOTE','publish']:
 1163              cases.append((f'PL002-atomic-{mode[2:]}-{boundary}',lambda f,m=mode,b=boundary:atomic_pointers(f,m,b)))
 1164      for kind in ['comments','format','token','endpoint','legacy','legacy-comments']:
 1165          cases.append((f'PL004-binding-{kind}',lambda f,k=kind:binding_rewrite(f,k)))
 1166      for kind in ['empty','unrelated','fallback','tiered','root-tiered','root-flat','root-unrelated','stranded','refused']:
 1167          cases.append((f'PL001-discovery-{kind}',lambda f,k=kind:content_discovery(f,k)))
 1168      for kind in ['supported','tiered','bios','unsupported']:
 1169          cases.append((f'PL001-legacy-support-{kind}',lambda f,k=kind:legacy_content_support(f,k)))
 1170      for name in ['MyGames','My Games','Games..old',"Kid's Games"]:
 1171          cases.append((f'PL006-folder-{name}',lambda f,n=name:content_folder_names(f,n)))
 1172      for kind in ['escaped','single','bare','double','duplicate','export','trailing','control']:
 1173          cases.append((f'PL008-reader-{kind}',lambda f,k=kind:reader_grammar(f,k)))
 1174      for kind in ['future','malformed','config','record','write','network','timeout']:
 1175          cases.append((f'PL005-reason-{kind}',lambda f,k=kind:scan_reason(f,k)))
 1176      for empty in (False,True):
 1177          cases.append((f'T23-predecessor-content-only-{"empty" if empty else "populated"}',
 1178                        lambda f,e=empty:predecessor_content_only(f,e)))
 1179      for mode in ['--join','--follow','--settle','--apply']:
 1180          for choice,value in [('missing',None),('root',''),('derived',OLD+'/Content'),('custom','/Mine/ROMs')]:
 1181              cases.append((f'T21-{mode[2:]}-{choice}',lambda f,m=mode,c=value:content_choice(f,m,c)))
 1182      if args.inject_failure:
 1183          cases=[('constructed-failure',lambda f:require(False,'deliberately false assertion'))]
 1184      if args.archives_only:
 1185          cases=[(name,fn) for name,fn in cases if name in archive_cases]
 1186      cases=[(name,fn) for name,fn in cases if not args.case or args.case in name]
 1187      require(cases,'no cases matched')
 1188      if args.list:
 1189          print('\n'.join(name for name,fn in cases))
 1190          return 0
 1191      if not args.ref and not args.inject_failure:
 1192          source_root=args.source_root or ROOT
 1193          require(all(name in archive_cases for name,fn in cases) or
 1194                  (source_root / SOURCES / 'cloud_migrate_layout').is_file(),
 1195                  'migration matrix retired by #508; use --ref for historical source or --archives-only for ordinary archive checks')
 1196      require(args.rclone is not None and shutil.which('bwrap'), 'requires rclone and bwrap')
 1197      args.rclone=str(Path(args.rclone).resolve())
 1198      version = subprocess.run([args.rclone, 'version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]
 1199      print(f'rclone: {version} ({args.rclone})', flush=True)
 1200      owned = args.output is None
 1201      output = args.output or Path(tempfile.mkdtemp(prefix='cloud-layout-'))
 1202      output.mkdir(parents=True,exist_ok=True)
 1203      results=[]
 1204      try:
 1205          for name,fn in cases:
 1206              fixture=Fixture(output/name,args)
 1207              try:
 1208                  fn(fixture)
 1209                  result=dict(case=name,status='PASS')
 1210              except (AssertionError,subprocess.TimeoutExpired) as error:
 1211                  result=dict(case=name,status='FAIL',why=str(error))
 1212              results.append(result)
 1213              print(result['status'],name,result.get('why',''),flush=True)
 1214          require(results,'no cases matched')
 1215          (output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 1216          failed=sum(r['status']=='FAIL' for r in results)
 1217          print(f'cloud-layout-test: {len(results)-failed} PASS, {failed} FAIL; artifacts: {output}',flush=True)
 1218          return int(failed>0)
 1219      finally:
 1220          if owned: shutil.rmtree(output)
 1221  
 1222  
 1223  if __name__=='__main__':
 1224      sys.exit(main())
```

## File: tools/pixelelated-cloud-validator-test (at 8ebaf8daad, 359 lines)

```text
    1  #!/usr/bin/env python3
    2  """Real local-rclone controls for bounded category validation (#508/#510).
    3  
    4  Synthetic host fixtures only; image/VM qualification remains a separate gate.
    5  Retains raw command results, literal rclone argv and immutable source hashes.
    6  """
    7  import argparse
    8  import hashlib
    9  import importlib.machinery
   10  import importlib.util
   11  import json
   12  from pathlib import Path
   13  import shutil
   14  import subprocess
   15  import time
   16  import sys
   17  
   18  ROOT = Path(__file__).resolve().parent.parent
   19  loader = importlib.machinery.SourceFileLoader('layout_fixture', str(ROOT/'tools/rasteratops-cloud-layout-test'))
   20  spec = importlib.util.spec_from_loader(loader.name, loader)
   21  legacy = importlib.util.module_from_spec(spec)
   22  loader.exec_module(legacy)
   23  require, put = legacy.require, legacy.put
   24  
   25  
   26  def snapshot(f):
   27      return {str(p.relative_to(f.path)): hashlib.sha256(p.read_bytes()).hexdigest()
   28              for area in ('storage', 'cloud') for p in sorted((f.path/area).rglob('*')) if p.is_file()}
   29  
   30  
   31  def request(f, categories='saves,settings,roms,bios,media', run='proof01', rc=0):
   32      before = snapshot(f)
   33      r = f.run('cloud_setup', '--validate-folders', categories, run)
   34      require(r.returncode == rc, f'rc={r.returncode}, expected {rc}: {r.stdout}')
   35      value = json.loads(r.stdout)
   36      require(snapshot(f) == before, 'validation changed local/cloud bytes')
   37      require(value['run_id'] == run, 'run identity absent')
   38      return value
   39  
   40  
   41  def rows(value):
   42      return {r['category']:r for r in value['categories']}
   43  
   44  
   45  def initial(f):
   46      put(f.path/'storage/roms/gb/.fixture', 'local known system\n')
   47      put(f.path/'storage/roms/snes/.fixture', 'local known system\n')
   48  
   49  
   50  def main():
   51      p=argparse.ArgumentParser()
   52      p.add_argument('--output', type=Path, required=True)
   53      p.add_argument('--rclone', default=shutil.which('rclone'))
   54      p.add_argument('--case', action='append')
   55      p.add_argument('--ref', help='Read historical product sources from this commit')
   56      a=p.parse_args()
   57      version=subprocess.check_output([a.rclone,'version'],text=True).splitlines()[0]
   58      require(version == 'rclone v1.75.1', 'Use the package-pinned rclone1.75.1, not the host fallback: '+version)
   59      require(not a.output.exists(), 'use a new output directory')
   60      a.output.mkdir(parents=True)
   61      results=[]
   62      def case(name, work):
   63          if a.case and name not in a.case:return
   64          f=legacy.Fixture(a.output/name,a);initial(f)
   65          work(f)
   66          results.append(name);print('PASS '+name,flush=True)
   67  
   68      def complete(f):
   69          f.file('pixelelated/Saves/gb/progress.srm')
   70          f.file('pixelelated/Backups/QA-id/2026_10_01-QA-ROCKNIX_SETTINGS.tar.gz')
   71          f.file('pixelelated/Content/ROMs/gb/Game.gb')
   72          f.file('pixelelated/Content/ROMs/gb/images/Game.png')
   73          f.file('pixelelated/Content/BIOS/firmware.bin')
   74          result=request(f)
   75          require(result['complete'] and all(x['state']=='present' for x in result['categories']),str(result))
   76          argv=(f.path/'ctl/argv').read_text()
   77          require(not any(line.startswith(('copy','move','sync','cat ','mkdir','rcat','delete')) for line in argv.splitlines()),argv)
   78          require(not any(line.startswith('lsjson qa: ') or line.startswith('lsjson qa:/ ') for line in argv.splitlines()),argv)
   79      case('populated-read-only',complete)
   80  
   81      def filtered_content(f):
   82          excluded=['only.'+ext for ext in ['srm','sav','fs','state1','auto','dsv','eep','mpk','sra','fla','mcd','mcr']]
   83          excluded+=['only (a conflicted copy).gb','only.sync-conflict-01.gb','only.12345678.partial','save/game.bin','memcards/game.bin','PPSSPP/game.bin','shared/savefiles/game.bin','README.txt']
   84          for base in ('pixelelated/Content/ROMs/gb','pixelelated/Content/BIOS'):
   85              for name in excluded:f.file(base+'/'+name)
   86          result=request(f,'roms,bios')
   87          require(all(row['state']=='empty' for row in result['categories']),str(result))
   88          f.file('pixelelated/Content/ROMs/gb/Game.gb');f.file('pixelelated/Content/BIOS/firmware.bin')
   89          require(all(row['state']=='present' for row in request(f,'roms,bios')['categories']),'real ROM/BIOS not recognized')
   90      case('content-transfer-exclusions',filtered_content)
   91  
   92      def flat_roms(f):
   93          base='pixelelated/Content/ROMs/'
   94          for name in ['README.txt','.layout','gamelist.xml','only.srm','only.eep','only.mcr','only (a conflicted copy).gb','only.sync-conflict-01.gb','only.12345678.partial']:
   95              f.file(base+name)
   96          f.file(base+'gb/images/Game.png')
   97          initial_rows=rows(request(f,'roms,media'))
   98          require(initial_rows['roms']['state']=='empty' and initial_rows['media']['state']=='present',str(initial_rows))
   99          f.file(base+'qa.gb')
  100          misplaced=rows(request(f,'roms,media'))
  101          require(misplaced['roms']['state']=='misplaced' and misplaced['roms']['detail']=='files-outside-system-folders',str(misplaced))
  102          require(misplaced['media']['state']=='present','flat ROM obscured valid media')
  103          f.file(base+'gb/Game.gb')
  104          require(rows(request(f,'roms'))['roms']['state']=='misplaced','valid ROM hid out-of-folder payload')
  105          (f.path/'cloud'/base/'qa.gb').unlink()
  106          require(rows(request(f,'roms'))['roms']['state']=='present','proper system ROM not recognized')
  107      case('flat-rom-payload-location',flat_roms)
  108  
  109      def progress_allowlist(f):
  110          for name in ['savefiles/history.db','savestates/history.sqlite3','screenshots/history.db-wal','gb/UPPER.SAV','psx/not-memcards/card.mcd','n64/save/wrong.bin','backup/settings.zip']:
  111              f.file('pixelelated/Saves/'+name)
  112          require(rows(request(f,'saves'))['saves']['state']=='empty','excluded/database/archive counted as progress')
  113          for ext in ('eep','mpk','sra','fla'):
  114              f.file('pixelelated/Saves/n64/Game.'+ext)
  115          f.file('pixelelated/Saves/psx/memcards/card.mcr')
  116          require(rows(request(f,'saves'))['saves']['state']=='present','standalone progress not recognized')
  117      case('ordinary-progress-allowlist',progress_allowlist)
  118  
  119      def missing(f):
  120          f.file('Elsewhere/ROMs/gb/Game.gb')
  121          value=request(f);r=rows(value)
  122          require(all(x['state']=='missing' for x in r.values()),str(value))
  123          require('Elsewhere' not in (f.path/'ctl/argv').read_text(),'account traversal')
  124      case('missing-selected-only',missing)
  125  
  126      def empty(f):
  127          for path in ('Saves','Backups','Content/ROMs/gb','Content/BIOS'):f.directory('pixelelated/'+path)
  128          for path in ('Saves','Backups','Content/ROMs','Content/BIOS'):f.file('pixelelated/'+path+'/README.txt')
  129          require(all(x['state']=='empty' for x in request(f)['categories']),'README or empty system counted as payload')
  130      case('empty-and-notes',empty)
  131  
  132      def empty_physical(f):
  133          f.directory('pixelelated/Saves')
  134          require(rows(request(f,'saves'))['saves']['state']=='empty','path-based empty failed')
  135      case('empty-path-based',empty_physical)
  136  
  137      def empty_bucket(f):
  138          f.directory('pixelelated/Saves');put(f.path/'ctl/bucket','yes')
  139          r=rows(request(f,'saves',rc=5))['saves']
  140          require(r['state']=='unreadable' and r['detail']=='folder-presence-unconfirmed',str(r))
  141          f.file('pixelelated/Saves/README.txt')
  142          require(rows(request(f,'saves'))['saves']['state']=='empty','README prefix witness ignored')
  143          require('lsjson qa: ' not in (f.path/'ctl/argv').read_text(),'bucket parent outside scope listed')
  144      case('bucket-empty-prefix-uncertainty',empty_bucket)
  145  
  146  
  147      def misplaced(f):
  148          f.file('pixelelated/Content/gb/Game.gb');f.file('pixelelated/Content/bios/firmware.bin')
  149          f.file('pixelelated/Saves/Saves/gb/progress.srm')
  150          r=rows(request(f,'saves,roms,bios'))
  151          require(r['saves']['state']=='present' and r['roms']['state']=='misplaced' and r['bios']['state']=='misplaced',str(r))
  152      case('content-misplaced-progress-preserved',misplaced)
  153  
  154      def failures(f):
  155          f.directory('pixelelated/Saves');f.fault('^lsjson qa:/pixelelated/Saves ',5)
  156          result=request(f,'saves',rc=5)
  157          require(not result['complete'] and rows(result)['saves']['state']=='unreadable',str(result))
  158      case('provider-failure-not-empty',failures)
  159  
  160      def inject(f, body):
  161          original=(f.path/'shim/rclone').read_text()
  162          put(f.path/'shim/rclone',original.replace('exec /rclone.real "$@"',body+'\nexec /rclone.real "$@"'),True)
  163  
  164      def partial(f):
  165          inject(f,'''if [ "$1" = lsjson ]; then printf '[{"Path":"gb/progress.srm","IsDir":false}]'; exit 3; fi''')
  166          result=request(f,'saves',rc=5)
  167          require(rows(result)['saves']['state']=='unreadable',str(result))
  168      case('partial-failed-listing',partial)
  169  
  170      def overlimit(f):
  171          inject(f,'''if [ "$1" = lsjson ]; then python3 -c 'import json;print(json.dumps([dict(Path="f"+str(n),IsDir=False) for n in range(4097)]))'; exit 0; fi''')
  172          require(rows(request(f,'saves',rc=5))['saves']['state']=='unreadable','oversize entries accepted')
  173      case('entry-limit',overlimit)
  174  
  175      def byte_limit(f):
  176          inject(f,'''if [ "$1" = lsjson ]; then python3 -c 'print("x"*2200000)'; exit 0; fi''')
  177          require(rows(request(f,'saves',rc=5))['saves']['state']=='unreadable','oversize bytes accepted')
  178      case('byte-limit',byte_limit)
  179  
  180      def malformed(f):
  181          inject(f,'''if [ "$1" = lsjson ]; then printf '[{"Path":"../escape.srm","IsDir":false}]'; exit 0; fi''')
  182          require(rows(request(f,'saves',rc=5))['saves']['state']=='unreadable','unsafe listing accepted')
  183      case('malformed-listing',malformed)
  184  
  185      def context(f):
  186          one=json.loads(f.run('cloud_setup','--validation-context').stdout)
  187          f.conf('/Other/Saves','/Keep/Backups','Rel/Content')
  188          two=json.loads(f.run('cloud_setup','--validation-context').stdout)
  189          require(one['config_id']!=two['config_id'],'path change same ID')
  190          c=f.path/'storage/.config/rclone/rclone.conf';c.write_text(c.read_text()+'# reconfigured\n')
  191          three=json.loads(f.run('cloud_setup','--validation-context').stdout)
  192          require(two['config_id']!=three['config_id'],'remote config change same ID')
  193          require(three['paths']['roms']=='Rel/Content/ROMs',str(three))
  194          require(not any(l.startswith('ls') and not l.startswith('listremotes') for l in (f.path/'ctl/argv').read_text().splitlines()),'context made network calls')
  195      case('context-binding-local-only',context)
  196  
  197      def info_paths(f):
  198          f.conf('Chosen/Saves','Separate/Archives','/Library')
  199          put(f.path/'shim/get_setting','#!/bin/sh\nexit 0\n',True)
  200          r=f.run('cloud_setup','--info');require(r.returncode==0,r.stdout)
  201          require('SETTINGS_REMOTE=Separate/Archives\n' in r.stdout and 'CONTENT_REMOTE=/Library\n' in r.stdout,r.stdout)
  202      case('info-independent-paths',info_paths)
  203  
  204  
  205      def stale(f):
  206          inject(f,'''if [ "$1" = lsjson ]; then printf '\\n# concurrent configuration edit\\n' >> /storage/.config/cloud_sync.conf; fi''')
  207          r=f.run('cloud_setup','--validate-folders','saves','stale01');v=json.loads(r.stdout)
  208          require(r.returncode==5 and v['error']=='configuration-changed' and not v['complete'],str(v))
  209      case('stale-configuration-refused',stale)
  210  
  211      def invalid(f):
  212          before=snapshot(f)
  213          for categories,run in [('','a'),('saves,','a'),('saves,saves','a'),('invalid','a'),('saves','../a'),('saves','x'*65)]:
  214              r=f.run('cloud_setup','--validate-folders',categories,run)
  215              require(r.returncode==2,'invalid args accepted')
  216          require(snapshot(f)==before,'invalid args mutated state')
  217          for categories in ('settings\nroms','saves,saves','saves,','unknown',' saves'):
  218              r=f.run('cloud_setup','--seed-folders',categories)
  219              require(r.returncode==2,'invalid seed category accepted')
  220          require(snapshot(f)==before,'invalid seed mutated bytes')
  221          require(not (f.path/'ctl/argv').exists(),'invalid args invoked rclone')
  222      case('invalid-input-refused',invalid)
  223  
  224      def invalid_setters(f):
  225          before=snapshot(f)
  226          for setter in ('--set-saves-remote','--set-settings-remote','--set-content-remote'):
  227              for bad in ('.','..','./x','../x','x/../y','x//y','x\n','x$HOME'):
  228                  r=f.run('cloud_setup',setter,bad)
  229                  require(r.returncode!=0, 'unsafe setter accepted '+repr((setter,bad)))
  230          require(snapshot(f)==before, 'refused setter changed bytes')
  231      case('invalid-paths-refused',invalid_setters)
  232  
  233      def deep(f):
  234          f.file('pixelelated/Saves/nested/a/b/c/progress.srm')
  235          result=request(f,'saves',rc=5)
  236          require(rows(result)['saves']['detail']=='deeper-folders-not-checked',str(result))
  237      case('deeper-than-bound-not-empty',deep)
  238  
  239      def content_location(f):
  240          f.file('ROMs/gb/root-game.gb');f.file('pixelelated/Content/ROMs/gb/chosen.gb')
  241          before=snapshot(f)
  242          r=f.run('cloud_setup','--content-location');require(r.returncode==0 and 'STATE=ok' in r.stdout,r.stdout)
  243          require(snapshot(f)==before,'location mutated bytes')
  244          require('lsjson qa: ' not in (f.path/'ctl/argv').read_text(),'account-root discovery')
  245      case('content-location-selected-only',content_location)
  246  
  247  
  248      def independent(f):
  249          f.conf('/GAMES','/GAMES/backup','Different/Content')
  250          before=snapshot(f)
  251          r=f.run('cloud_setup','--set-saves-remote','New/Saves');require(r.returncode==0,r.stdout)
  252          q=f.pointers();require(q['SAVES_REMOTE']=='New/Saves' and q['SETTINGS_REMOTE']=='/GAMES/backup' and q['CONTENT_REMOTE']=='Different/Content',str(q))
  253          r=f.run('cloud_setup','--set-settings-remote','Settings');require(r.returncode==0,r.stdout)
  254          q=f.pointers();require(q['SETTINGS_REMOTE']=='Settings' and q['SAVES_REMOTE']=='New/Saves' and q['CONTENT_REMOTE']=='Different/Content',str(q))
  255          require(not any(k.startswith('cloud/') for k in snapshot(f)),'selection mutated cloud')
  256      case('independent-pointer-selection',independent)
  257  
  258      def seeds(f):
  259          f.file('pixelelated/Saves/gb/progress.srm','retained')
  260          before=snapshot(f)
  261          require(f.run('cloud_setup','--seed-folders').returncode==2,'implicit seeding allowed')
  262          r=f.run('cloud_setup','--seed-folders','settings');require(r.returncode==0,r.stdout)
  263          after=snapshot(f);require(all(after.get(k)==v for k,v in before.items()),'seed replaced bytes')
  264          require((f.path/'cloud/pixelelated/Backups/README.txt').exists(),'missing selected seed')
  265          require(not (f.path/'cloud/pixelelated/Content').exists(),'disabled content created')
  266          require(not (f.path/'cloud/pixelelated/Saves/savefiles').exists(),'disabled saves folders created')
  267          r=f.run('cloud_setup','--seed-folders','roms');require(r.returncode==0,r.stdout)
  268          require(not (f.path/'cloud/pixelelated/Content/BIOS').exists(),'disabled BIOS created')
  269      case('explicit-category-seeding',seeds)
  270  
  271      def namespace(f):
  272          f.conf('Mine/Saves','Mine/Settings','Mine/Content')
  273          r=f.run('cloud_setup','--seed-folders','saves,settings,roms,bios');require(r.returncode==0,r.stdout)
  274          result=request(f);require(result['complete'],str(result))
  275          argv=(f.path/'ctl/argv').read_text()
  276          require('qa:/Mine' not in argv,'relative namespace changed to absolute')
  277          require('lsjson qa: ' not in argv,'unselected root scanned')
  278      case('relative-namespace-preserved',namespace)
  279  
  280      def distinct_roots(f):
  281          # The real alias backend normalizes leading slash. Map the two rclone
  282          # namespaces to separate real local trees instead, as SFTP does.
  283          inject(f,'''mapped=()
  284  for arg in "$@"; do
  285   case "$arg" in
  286    qa:/*) mapped+=(":local:/cloud/absolute/${arg#qa:/}") ;;
  287    qa:*) mapped+=(":local:/cloud/relative/${arg#qa:}") ;;
  288    *) mapped+=("$arg") ;;
  289   esac
  290  done
  291  if [ "$1" = lsf ] && [ "$2" = qa:/ ] && { [ -e /ctl/absolute-unreadable ] || [ -e /ctl/root-seeded ]; }; then exit 5; fi
  292  /rclone.real "${mapped[@]}"; rc=$?
  293  if [ "$1" = copyto ] && [ "$rc" = 0 ] && [ -e /ctl/fail-seed-readback ]; then touch /ctl/root-seeded; fi
  294  exit "$rc"''')
  295          f.directory('absolute');f.file('relative/owner-note.txt','home namespace sentinel')
  296          f.conf('/','/','/Library')
  297          put(f.path/'ctl/absolute-unreadable','yes')
  298          r=f.run('cloud_setup','--folder-state')
  299          require(r.returncode!=0,'unreadable absolute root was reported ready by reading relative home: '+r.stdout)
  300          (f.path/'ctl/absolute-unreadable').unlink()
  301          r=f.run('cloud_setup','--folder-state');require(r.returncode==0 and 'STATE=ready' in r.stdout,r.stdout)
  302          put(f.path/'ctl/fail-seed-readback','yes')
  303          r=f.run('cloud_setup','--seed-folders','settings')
  304          require(r.returncode!=0 and (f.path/'ctl/root-seeded').exists(),'absolute-root readback used relative home: '+r.stdout)
  305          require((f.path/'cloud/absolute/README.txt').exists(),'absolute note was not created')
  306          require((f.path/'cloud/relative/owner-note.txt').read_text()=='home namespace sentinel','relative home was changed')
  307      case('absolute-relative-root-distinction',distinct_roots)
  308  
  309      def root(f):
  310          f.conf('/Saves','/Backups','')
  311          r=f.run('cloud_setup','--seed-folders','roms,bios');require(r.returncode==0,r.stdout)
  312          c=json.loads(f.run('cloud_setup','--validation-context').stdout)
  313          require(c['paths']['roms']=='ROMs',str(c))
  314          request(f,'roms,bios')
  315          argv=(f.path/'ctl/argv').read_text();require('lsjson qa: ' in argv,'explicit root not inspected')
  316          require('qa:/ROMs' not in argv,'relative root changed to absolute')
  317      case('explicit-root-allowed',root)
  318  
  319      def public_adoption(f, content=None):
  320          ref='c445081a59518f37d9776e5412dd7b14910696f7'
  321          public=subprocess.check_output(['git','-C',str(ROOT),'show',ref+':projects/ROCKNIX/packages/network/rclone/sources/cloud_sync.conf'])
  322          (f.path/'storage/.config/cloud_sync.conf').write_bytes(public + (('\nCONTENT_REMOTE="'+content+'"\n').encode() if content is not None else b''))
  323          before_credential=(f.path/'storage/.config/rclone/rclone.conf').read_bytes()
  324          f.file('GAMES/gb/progress.srm');f.file('GAMES/backup/existing.zip')
  325          before_cloud={k:v for k,v in snapshot(f).items() if k.startswith('cloud/')}
  326          cmd=['bwrap','--die-with-parent','--unshare-pid','--tmpfs','/',
  327               '--dir','/usr',
  328               '--ro-bind','/usr/bin','/usr/bin','--ro-bind','/usr/lib','/usr/lib','--ro-bind','/usr/lib64','/usr/lib64','--ro-bind','/usr/share','/usr/share',
  329               '--symlink','usr/bin','/bin','--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64',
  330               '--ro-bind','/etc','/etc','--ro-bind',str(f.path/'profile'),'/etc/profile',
  331               '--ro-bind',str(f.path/'repo'),'/usr/config',
  332               '--ro-bind',a.rclone,'/rclone.real','--dev','/dev','--proc','/proc','--tmpfs','/tmp']
  333          for folder,guest in [('repo','/repo'),('shim','/shim'),('storage','/storage'),('cloud','/cloud'),('ctl','/ctl'),('log','/var/log'),('run','/var/run')]:
  334              cmd+=['--bind',str(f.path/folder),guest]
  335          cmd+=['--setenv','HOME','/storage','--setenv','PATH','/shim:/repo:/usr/bin:/bin','bash','/repo/cloud_sync_helper']
  336          r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=15)
  337          (f.path/'adoption.log').write_text(r.stdout)
  338          (f.path/'adoption-result.json').write_text(json.dumps({'rc':r.returncode,'public_ref':ref,'public_conf_sha256':hashlib.sha256(public).hexdigest(),'pointers':f.pointers()},indent=2))
  339          require(r.returncode==0,r.stdout)
  340          q=f.pointers();require(q.get('SAVES_REMOTE')=='/GAMES' and q.get('SETTINGS_REMOTE')=='/GAMES/backup',str(q))
  341          require(q.get('CONTENT_REMOTE')==('/pixelelated/Content' if content is None else content),'content choice not preserved/defaulted: '+str(q.get('CONTENT_REMOTE')))
  342          require((f.path/'storage/.config/rclone/rclone.conf').read_bytes()==before_credential,'credentials changed')
  343          require({k:v for k,v in snapshot(f).items() if k.startswith('cloud/')}==before_cloud,'adoption relocated cloud bytes')
  344          result=request(f,'saves,settings')
  345          require(rows(result)['saves']['path']=='/GAMES' and rows(result)['settings']['path']=='/GAMES/backup',str(result))
  346      case('public-rocknix-config-adoption',public_adoption)
  347      case('public-rocknix-explicit-root-preserved',lambda f:public_adoption(f,''))
  348      case('public-rocknix-custom-library-preserved',lambda f:public_adoption(f,'Separate/Library'))
  349  
  350      def timeout(f):
  351          inject(f,'''if [ "$1" = lsjson ]; then sleep 12; fi''')
  352          require(rows(request(f,'saves',rc=5))['saves']['state']=='unreadable','unbounded request')
  353      case('request-timeout',timeout)
  354  
  355      sources=ROOT/'projects/ROCKNIX/packages/network/rclone/sources'
  356      (a.output/'result.json').write_text(json.dumps({'result':'PASS','cases':results,'rclone_version':version,'rclone_sha256':hashlib.sha256(Path(a.rclone).read_bytes()).hexdigest(),'source_sha256':{n:hashlib.sha256(subprocess.check_output(['git','-C',str(ROOT),'show',a.ref+':projects/ROCKNIX/packages/network/rclone/sources/'+n]) if a.ref else (sources/n).read_bytes()).hexdigest() for n in ['cloud_setup','cloud_folder_validate','cloud_content_restore','cloud_sync_helper']}},indent=2)+'\n')
  357      print(f'PASS {len(results)} controls')
  358  
  359  if __name__=='__main__':main()
```

## File: tools/pixelelated-content-scope-test (at 8ebaf8daad, 256 lines)

```text
    1  #!/usr/bin/env python3
    2  """Exercise selected-library boundaries with production scripts and real rclone.
    3  
    4  Host source controls for #508/#510, not firmware or VM qualification. Each
    5  case gets independent synthetic configuration, cloud files, and result logs.
    6  """
    7  import argparse
    8  import fcntl
    9  import hashlib
   10  import importlib.machinery
   11  import importlib.util
   12  import json
   13  from pathlib import Path
   14  import sys
   15  
   16  
   17  def main():
   18      parser = argparse.ArgumentParser(description=__doc__)
   19      parser.add_argument('--source-root', type=Path, required=True)
   20      parser.add_argument('--rclone', required=True)
   21      parser.add_argument('--output', type=Path, required=True)
   22      parser.add_argument('--cases', help='Comma-separated case names; use for unfixed controls')
   23      parser.add_argument('--fixture-tool', type=Path,
   24                          default=Path(__file__).with_name('rasteratops-cloud-layout-test'))
   25      args = parser.parse_args()
   26      args.source_root = args.source_root.resolve()
   27      args.rclone = str(Path(args.rclone).resolve(strict=True))
   28      args.ref = None
   29      args.output.mkdir(parents=True, exist_ok=False)
   30      loader = importlib.machinery.SourceFileLoader('layout_fixture', str(args.fixture_tool))
   31      spec = importlib.util.spec_from_loader(loader.name, loader)
   32      fixture = importlib.util.module_from_spec(spec)
   33      loader.exec_module(fixture)
   34      results = []
   35  
   36      def snapshot(path):
   37          return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
   38                  for p in path.rglob('*') if p.is_file()}
   39  
   40      def case(name, run):
   41          if args.cases and name not in args.cases.split(','):
   42              return
   43          f = fixture.Fixture(args.output / name, args)
   44          f.conf(content='/Chosen/Library')
   45          fixture.put(f.path / 'storage/roms/gb/.keep', '')
   46          # Independent distracting libraries, both flat and structured.
   47          for path in ['gb/Outside.gb', 'Other/ROMs/gb/Other.gb',
   48                       'Chosen/Library/gb/Flat.gb', 'bios/Outside.bin']:
   49              f.file(path, 'unselected ' + path)
   50          before = snapshot(f.path / 'cloud')
   51          try:
   52              fixture.put(f.path/'repo/fixture-check', "printf '%s\\n' isolated-fixture-ready\n")
   53              ready = f.run('fixture-check')
   54              fixture.require(ready.returncode == 0 and ready.stdout.strip() == 'isolated-fixture-ready',
   55                              'isolated fixture did not start: ' + ready.stdout)
   56              run(f)
   57              fixture.require(snapshot(f.path / 'cloud') == before,
   58                              'read/restore changed remote files')
   59              results.append({'case': name, 'result': 'PASS'})
   60              print('PASS', name, flush=True)
   61          except Exception as error:
   62              results.append({'case': name, 'result': 'FAIL', 'error': str(error)})
   63              print('FAIL', name, str(error), flush=True)
   64  
   65      def absent(f, mode):
   66          r = f.run('cloud_content_restore', mode)
   67          fixture.require(r.returncode == 0, r.stdout)
   68          if mode == '--list':
   69              fixture.require(not r.stdout.strip(), 'unselected folders were offered')
   70          if mode == '--scan':
   71              rows = [line.split('|') for line in r.stdout.splitlines() if '|' in line]
   72              fixture.require(all(row[1] == '0' for row in rows), 'unselected cloud bytes counted')
   73          fixture.require(not (f.path / 'storage/roms/gb/Flat.gb').exists(),
   74                          'flat library restored without selection')
   75          fixture.require(not (f.path / 'storage/roms/gb/Outside.gb').exists(),
   76                          'account-root library restored')
   77          calls = (f.path / 'ctl/argv').read_text().splitlines()
   78          for line in calls:
   79              if line.startswith(('lsf ', 'copy ', 'sync ')):
   80                  fixture.require('qa:/Chosen/Library' in line,
   81                                  'remote access escaped selected library: ' + line)
   82  
   83      for mode in ['--list', '--scan', '--all']:
   84          case('missing-' + mode[2:], lambda f, mode=mode: absent(f, mode))
   85  
   86      def selected(f):
   87          f.file('Chosen/Library/ROMs/gb/Chosen.gb', 'chosen ROM bytes')
   88          f.file('Chosen/Library/BIOS/Required.bin', 'chosen BIOS bytes')
   89          # Those are fixtures too; return them to the initial snapshot after
   90          # checking exact local bytes, so the common read-only oracle applies.
   91          before = snapshot(f.path / 'cloud')
   92          r = f.run('cloud_content_restore', '--all')
   93          fixture.require(r.returncode == 0, r.stdout[-1000:])
   94          fixture.require((f.path / 'storage/roms/gb/Chosen.gb').read_text() == 'chosen ROM bytes',
   95                          'selected ROM bytes missing')
   96          fixture.require((f.path / 'storage/roms/bios/Required.bin').read_text() == 'chosen BIOS bytes',
   97                          'selected BIOS bytes missing')
   98          fixture.require(snapshot(f.path / 'cloud') == before, 'restore changed cloud')
   99          (f.path / 'cloud/Chosen/Library/ROMs/gb/Chosen.gb').unlink()
  100          (f.path / 'cloud/Chosen/Library/BIOS/Required.bin').unlink()
  101          fixture.require(not (f.path / 'storage/roms/gb/Flat.gb').exists(), 'flat fallback used')
  102  
  103      case('selected-rom-bios-bytes', selected)
  104  
  105      def failed(f, mode, partial):
  106          if partial:
  107              shim = f.path / 'shim/rclone'
  108              text = shim.read_text()
  109              text = text.replace("printf '%s\\n' \"$*\" >> /ctl/argv",
  110                                  "printf '%s\\n' \"$*\" >> /ctl/argv\n"
  111                                  "if [ \"$1\" = lsf ]; then echo '99|gb/Partial.gb'; exit 3; fi")
  112              # Verify fault installation rather than a vacuous error case.
  113              fixture.require('Partial.gb' in text, 'could not install partial-list fault')
  114              shim.write_text(text)
  115          else:
  116              f.fault('^lsf ', 5)
  117          r = f.run('cloud_content_restore', mode)
  118          fixture.require(r.returncode != 0, 'provider failure looked like success: ' + r.stdout)
  119          fixture.require(not any(p.name.endswith('.gb') for p in (f.path/'storage/roms').rglob('*')),
  120                          'failure caused an unintended restore')
  121          calls = (f.path/'ctl/argv').read_text()
  122          fixture.require(not any(line.startswith(('copy ', 'sync ')) for line in calls.splitlines()),
  123                          'failed discovery started a transfer')
  124  
  125      for mode in ['--list', '--scan', '--all']:
  126          case('unreadable-' + mode[2:], lambda f, mode=mode: failed(f, mode, False))
  127          case('partial-' + mode[2:], lambda f, mode=mode: failed(f, mode, True))
  128  
  129      def traversal(f):
  130          r = f.run('cloud_content_restore', '../gb')
  131          fixture.require(r.returncode != 0, 'relative traversal accepted')
  132          calls = (f.path/'ctl/argv').read_text()
  133          fixture.require(not any(line.startswith(('copy ', 'sync ')) for line in calls.splitlines()),
  134                          'traversal started transfer')
  135      case('system-traversal-refused', traversal)
  136  
  137      def scan_binding(f):
  138          r = f.run('cloud_scan', '--content', '--run-id', 'scope-one')
  139          fixture.require(r.returncode == 0, r.stdout)
  140          stamp = json.loads((f.path/'storage/.cache/cloud_sync/scan/content-done').read_text())
  141          fixture.require(isinstance(stamp, dict), 'completion is not bound to a run/configuration')
  142          fixture.require(stamp['run_id'] == 'scope-one', 'wrong scan identity')
  143          fixture.require(f.run('cloud_scan', '--stamp-valid', 'content-done', 'scope-one').returncode == 0,
  144                          'current scan refused')
  145          fixture.require(f.run('cloud_scan', '--stamp-valid', 'content-done', 'other-run').returncode != 0,
  146                          'another scan was accepted')
  147          fixture.require(f.run('cloud_scan', '--stamp-valid', 'content-done', 'scope-one', '--media-only').returncode != 0,
  148                          'another category selection was accepted')
  149          rows = f.path/'storage/.cache/cloud_sync/scan/scan'
  150          rows.write_text(rows.read_text()+'gb|99|1|0|0|0|0|0\n')
  151          fixture.require(f.run('cloud_scan', '--stamp-valid', 'content-done', 'scope-one').returncode != 0,
  152                          'mutated cached output accepted')
  153  
  154      case('scan-run-mode-output-binding', scan_binding)
  155  
  156      def changed_configuration(f):
  157          r = f.run('cloud_scan', '--content', '--run-id', 'scope-two')
  158          fixture.require(r.returncode == 0, r.stdout)
  159          f.conf(content='/Different/Library')
  160          fixture.require(f.run('cloud_scan', '--stamp-valid', 'content-done', 'scope-two').returncode != 0,
  161                          'old result accepted after folder change')
  162  
  163      case('scan-folder-change-invalidates', changed_configuration)
  164  
  165      def changed_endpoint(f):
  166          r = f.run('cloud_scan', '--content', '--run-id', 'scope-three')
  167          fixture.require(r.returncode == 0, r.stdout)
  168          fixture.put(f.path/'storage/.config/rclone/rclone.conf', '[qa]\ntype = alias\nremote = /different-cloud\n')
  169          fixture.require(f.run('cloud_scan', '--stamp-valid', 'content-done', 'scope-three').returncode != 0,
  170                          'old result accepted after endpoint change')
  171  
  172      case('scan-endpoint-change-invalidates', changed_endpoint)
  173  
  174      def local_context(f):
  175          before = snapshot(f.path/'storage')
  176          r = f.run('cloud_scan', '--context')
  177          fixture.require(r.returncode == 0 and len(r.stdout.strip()) == 64, 'invalid local context')
  178          fixture.require(not (f.path/'ctl/argv').exists(), 'local context started rclone')
  179          fixture.require(snapshot(f.path/'storage') == before, 'local context changed config/cache')
  180          fixture.require(f.run('cloud_scan', '--stamp-valid', '../../outside', 'scope').returncode != 0,
  181                          'arbitrary stamp path accepted')
  182  
  183      case('scan-context-local-read-only', local_context)
  184  
  185      def scan_lock(f):
  186          cache = f.path/'storage/.cache/cloud_sync/scan'
  187          fixture.put(cache/'done', 'another owner\n')
  188          fixture.put(cache/'state', 'retained cache\n')
  189          before = snapshot(cache)
  190          with (f.path/'run/cloud_scan.lock').open('w') as lock:
  191              fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
  192              r = f.run('cloud_scan', '--run-id', 'second-owner')
  193          fixture.require(r.returncode == 75, 'concurrent scan was not refused')
  194          fixture.require(snapshot(cache) == before, 'refused scan altered another owner cache')
  195          fixture.require(not (f.path/'ctl/argv').exists(), 'refused scan contacted cloud')
  196  
  197      case('scan-concurrent-owner-refused', scan_lock)
  198  
  199      def unreadable_during_scan(f):
  200          shim = f.path/'shim/rclone'
  201          s = shim.read_text().replace('exec /rclone.real "$@"',
  202                                      "printf '\\n# changed while checking\\n' >> /storage/.config/cloud_sync.conf\n"
  203                                      'exec /rclone.real "$@"')
  204          shim.write_text(s)
  205          r = f.run('cloud_scan', '--content', '--run-id', 'changing-config')
  206          fixture.require(r.returncode != 0, 'configuration changed during scan but completion succeeded')
  207          fixture.require(not (f.path/'storage/.cache/cloud_sync/scan/content-done').exists(),
  208                          'failed scan wrote completion')
  209  
  210      case('scan-config-changes-during-run', unreadable_during_scan)
  211  
  212      def trailing_slash(f):
  213          f.conf(content='/Chosen/Library/')
  214          absent(f, '--list')
  215  
  216      case('selected-trailing-slash', trailing_slash)
  217  
  218      def pointer_traversal(f):
  219          f.conf(content='../Other')
  220          r = f.run('cloud_content_restore', '--list')
  221          fixture.require(r.returncode != 0, 'traversing content pointer accepted')
  222          calls = (f.path/'ctl/argv').read_text()
  223          fixture.require(not any(line.startswith(('lsf ', 'copy ', 'sync ')) for line in calls.splitlines()),
  224                          'traversing pointer read a cloud folder')
  225  
  226      case('content-pointer-traversal-refused', pointer_traversal)
  227  
  228      def root_refusal(f, root):
  229          f.conf(content=root)
  230          f.fault('^lsf ', 5)
  231          fixture.put(f.path/'repo/root-refusal', 'timeout 2 bash /repo/cloud_content_restore --list\n')
  232          r = f.run('root-refusal')
  233          fixture.require(r.returncode not in (0, 124),
  234                          'unreadable selected root did not refuse promptly: ' + str(r.returncode))
  235          calls = (f.path/'ctl/argv').read_text().splitlines()
  236          listing = [row.split()[2] for row in calls if row.startswith('lsf --dirs-only ')]
  237          selected = 'qa:' + root
  238          fixture.require(listing and all(p in (selected, selected+'ROMs/') for p in listing),
  239                          'selected namespace changed: ' + repr(listing))
  240      case('relative-root-unreadable-bounded', lambda f: root_refusal(f, ''))
  241      case('absolute-root-unreadable-bounded', lambda f: root_refusal(f, '/'))
  242  
  243      sources = args.source_root / fixture.SOURCES
  244      receipt = {'source_root': str(args.source_root),
  245                 'source_sha256': {name: hashlib.sha256((sources/name).read_bytes()).hexdigest()
  246                                   for name in ['cloud_content_restore', 'cloud_content_transfer', 'cloud_scan']},
  247                 'rclone_sha256': hashlib.sha256(Path(args.rclone).read_bytes()).hexdigest(),
  248                 'results': results}
  249      (args.output/'result.json').write_text(json.dumps(receipt, indent=2)+'\n')
  250      if not results:
  251          raise RuntimeError('No selected controls ran')
  252      return int(any(row['result'] != 'PASS' for row in results))
  253  
  254  
  255  if __name__ == '__main__':
  256      sys.exit(main())
```

## File: tools/pixelelated-save-layout-test (at 8ebaf8daad, 409 lines)

```text
    1  #!/usr/bin/env python3
    2  """Source-bound real-rclone controls for standalone progress coverage (#520).
    3  
    4  Disposable host fixtures only; this does not qualify installed firmware or UI.
    5  Use --ref with the same cases for an unfixed control. Each fixture must first
    6  execute its startup witness and the supplied real rclone successfully.
    7  """
    8  import argparse
    9  import hashlib
   10  import importlib.machinery
   11  import importlib.util
   12  import json
   13  import os
   14  import time
   15  from pathlib import Path
   16  import shutil
   17  import subprocess
   18  import sys
   19  import types
   20  
   21  SOURCES = Path('projects/ROCKNIX/packages/network/rclone/sources')
   22  PSP = 'psp/PSP/SAVEDATA/ULUS00001/DATA.BIN'
   23  DUCK = 'psx/duckstation/memcards/Example_1.mcd'
   24  N64 = ['n64/Example.st0', 'n64/Example.st9', 'n64/Example.pj0', 'n64/Example.pj9.zip']
   25  PROGRESS = N64 + [PSP, 'psp/PSP/SAVEDATA/ULUS00001/PARAM.SFO',
   26              'psp/PSP/SAVEDATA/ULUS00001/ICON0.PNG',
   27              'psp/PSP/SAVEDATA/ULUS00001/gamelist.xml', DUCK,
   28              'psx/duckstation/memcards/imported.mcr',
   29              'psx/memcards/legacy.mcd', 'psp/PPSSPP/legacy.bin',
   30              'n64/Legacy.eep', 'savefiles/control.srm',
   31              'savestates/psp/ppsspp-sa/Example.ppst', 'screenshots/Capture.png']
   32  
   33  
   34  def snapshot(path):
   35      return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
   36              for p in path.rglob('*') if p.is_file()}
   37  
   38  
   39  def main():
   40      parser = argparse.ArgumentParser(description=__doc__)
   41      parser.add_argument('--source-root', required=True, type=Path)
   42      parser.add_argument('--ref')
   43      parser.add_argument('--rclone', required=True, type=Path)
   44      parser.add_argument('--output', required=True, type=Path)
   45      parser.add_argument('--cases', help='Comma-separated exact case names')
   46      parser.add_argument('--keep-fixtures', action='store_true')
   47      parser.add_argument('--busybox', type=Path,
   48                          help='Use a private copy of this image BusyBox for find/awk')
   49      parser.add_argument('--fixture-tool', type=Path,
   50                          default=Path(__file__).with_name('rasteratops-cloud-layout-test'))
   51      args = parser.parse_args()
   52      args.source_root = args.source_root.resolve(strict=True)
   53      args.rclone = str(args.rclone.resolve(strict=True))
   54      args.output = args.output.resolve()
   55      args.output.mkdir(parents=True, exist_ok=False)
   56      busybox = None
   57      if args.busybox:
   58          args.busybox = args.busybox.resolve(strict=True)
   59          busybox = args.output/'runtime/busybox'
   60          busybox.parent.mkdir()
   61          shutil.copy2(args.busybox, busybox)
   62          # Fail before running controls if either requested image applet is absent.
   63          for applet in ('find', 'awk'):
   64              subprocess.run([str(busybox), applet, '--help'], check=True,
   65                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   66      loader = importlib.machinery.SourceFileLoader('save_layout_fixture', str(args.fixture_tool))
   67      spec = importlib.util.spec_from_loader(loader.name, loader)
   68      fixture = importlib.util.module_from_spec(spec)
   69      loader.exec_module(fixture)
   70      fixture.ROOT = args.source_root
   71  
   72      # Reuse the existing isolated production-script runner. Install the exact
   73      # templates at their real path too: an unavailable /usr/config silently
   74      # skips the upgrade merge and is not an upgrade control.
   75      def isolated_run(cmd, *pos, **kw):
   76          if isinstance(cmd, list) and cmd[0] == 'bwrap':
   77              cmd = list(cmd)
   78              index = cmd.index('/usr') - 1
   79              require_mount = cmd[index:index + 3] == ['--ro-bind', '/usr', '/usr']
   80              fixture.require(require_mount, 'fixture host tools mount changed')
   81              mounts = ['--tmpfs', '/usr']
   82              for name in ('bin', 'sbin', 'lib', 'lib64', 'share', 'local'):
   83                  source = '/usr/' + name
   84                  if Path(source).exists():
   85                      mounts.extend(['--ro-bind', source, source])
   86              cmd[index:index + 3] = mounts
   87              repo = None
   88              for index, value in enumerate(cmd):
   89                  if value == '--bind' and cmd[index + 2] == '/repo':
   90                      repo = cmd[index + 1]
   91                      break
   92              fixture.require(repo is not None, 'fixture repository mount missing')
   93              index = cmd.index('--chdir')
   94              cmd[index:index] = ['--unshare-net', '--ro-bind', repo, '/usr/config']
   95              if busybox:
   96                  cmd[index:index] = ['--dir', '/qa-tools', '--ro-bind', str(busybox), '/qa-tools/busybox']
   97          return subprocess.run(cmd, *pos, **kw)
   98      fixture.subprocess = types.SimpleNamespace(run=isolated_run, PIPE=subprocess.PIPE,
   99                                                 STDOUT=subprocess.STDOUT)
  100      require = fixture.require
  101      results = []
  102      sources = {}
  103  
  104      def good(f, script, *argv):
  105          result = f.run(script, *argv)
  106          require(result.returncode == 0, f'{script} rc={result.returncode}: {result.stdout[-700:]}')
  107          return result.stdout
  108  
  109      def case(name, test):
  110          if args.cases and name not in args.cases.split(','):
  111              return
  112          f = fixture.Fixture(args.output / name, args)
  113          f.conf(saves='/Chosen/Saves', content='/Chosen/Library')
  114          fixture.put(f.path/'storage/.config/emulationstation/es_systems.cfg',
  115                      '\n'.join('<path>/storage/roms/'+s+'</path>' for s in ('psp', 'psx', 'n64', 'gb')))
  116          rules = f.path/'storage/.config/cloud_sync-rules.txt'
  117          rules.write_bytes((f.path/'repo/cloud_sync-rules.txt').read_bytes())
  118          for script, body in {
  119              'fixture-check': "printf '%s\\n' isolated-fixture-ready\nrclone version\n",
  120              'filter-probe': 'exec rclone lsf /storage/roms -R --files-only --filter-from "$1"\n',
  121              'validator-call': 'exec python3 /repo/cloud_folder_validate "$@"\n',
  122          }.items():
  123              fixture.put(f.path/'repo'/script, body)
  124          if busybox:
  125              wrappers = {}
  126              for applet in ('find', 'awk'):
  127                  body = ('#!/bin/sh\n'
  128                          f'printf "%s\\n" "{applet}" >> /ctl/busybox-calls\n'
  129                          f'exec /qa-tools/busybox {applet} "$@"\n')
  130                  fixture.put(f.path/'shim'/applet, body, True)
  131                  wrappers[applet] = body
  132              (f.path/'busybox-wrappers.json').write_text(json.dumps(wrappers, indent=2)+'\n')
  133              with (f.path/'repo/fixture-check').open('a') as check:
  134                  check.write('command -v find awk\nsha256sum /qa-tools/busybox\n/qa-tools/busybox 2>&1 | head -1\n')
  135          original = snapshot(f.path/'repo')
  136          sources.update({k: v for k, v in original.items() if k.startswith('cloud_')})
  137          try:
  138              ready = good(f, 'fixture-check')
  139              require(ready.startswith('isolated-fixture-ready\nrclone v'), 'startup witness failed')
  140              if busybox:
  141                  require('/shim/find\n/shim/awk\n' in ready, 'image applet wrapper resolution failed')
  142                  require(hashlib.sha256(busybox.read_bytes()).hexdigest()+'  /qa-tools/busybox' in ready,
  143                          'mounted image applet bytes changed')
  144                  require('BusyBox v' in ready, 'image BusyBox did not execute')
  145              test(f)
  146              require(all(snapshot(f.path/'repo').get(k) == v for k, v in original.items()), 'production inputs changed during control')
  147              results.append({'case': name, 'result': 'PASS'})
  148              print('PASS', name, flush=True)
  149          except Exception as error:
  150              results.append({'case': name, 'result': 'FAIL', 'error': str(error)})
  151              print('FAIL', name, str(error), flush=True)
  152          finally:
  153              (f.path/'final-files.json').write_text(json.dumps({
  154                  'cloud': snapshot(f.path/'cloud'), 'storage': snapshot(f.path/'storage'),
  155                  'production_inputs': original}, indent=2)+'\n')
  156              if not args.keep_fixtures:
  157                  retired = []
  158                  for directory in ('repo', 'shim', 'storage', 'cloud', 'run', 'log'):
  159                      target = f.path/directory
  160                      retired.append({'directory': directory, 'files': sum(p.is_file() for p in target.rglob('*'))})
  161                      shutil.rmtree(target)
  162                  (f.path/'retired-fixtures.json').write_text(json.dumps(retired, indent=2)+'\n')
  163  
  164      def seed(f, progress=PROGRESS):
  165          for path in progress:
  166              fixture.put(f.path/'storage/roms'/path, 'current local progress '+path+'\n')
  167  
  168      def filter_path(f, path):
  169          seed(f, [path, 'savefiles/control.srm'])
  170          for template in ('cloud_sync-rules.txt', 'cloud_sync-rules.txt.defaults'):
  171              listed = good(f, 'filter-probe', '/repo/'+template).splitlines()
  172              require('savefiles/control.srm' in listed, 'real-rclone include witness missing')
  173              require(path in listed, f'{template} excludes valid progress: {path}')
  174      case('filter-psp', lambda f: filter_path(f, PSP))
  175      case('filter-duckstation', lambda f: filter_path(f, DUCK))
  176      for path in N64:
  177          case('filter-n64-'+path.rsplit('.', 1)[-1], lambda f, path=path: filter_path(f, path))
  178  
  179      def roundtrip(f):
  180          seed(f)
  181          deny = ['psp/Example.iso', 'psx/Example.chd', 'bios/Firmware.bin',
  182                  'psp/PSP/SAVEDATA/ULUS00001/history.db',
  183                  'psp/PSP/SAVEDATA/ULUS00001/history.db-wal',
  184                  'psx/duckstation/memcards/history.sqlite3']
  185          seed(f, deny)
  186          before = snapshot(f.path/'storage/roms')
  187          good(f, 'cloud_backup', '--yes', '--saves-only')
  188          sent = snapshot(f.path/'cloud/Chosen/Saves')
  189          require(sent == {p: before[p] for p in PROGRESS}, 'backup payload does not equal allowed progress')
  190          for path in PROGRESS:
  191              (f.path/'storage/roms'/path).unlink()
  192          good(f, 'cloud_restore', '--yes', '--saves-only')
  193          require(snapshot(f.path/'storage/roms') == before, 'restore lost progress or changed excluded payloads')
  194      case('save-backup-restore', roundtrip)
  195  
  196      def upgrade(f):
  197          old = subprocess.check_output(['git', '-C', str(args.source_root), 'show',
  198                                         '6f89bc7cecee5972909828103689e2c7c0711c30:'+str(SOURCES/'cloud_sync-rules.txt')], text=True)
  199          rules = f.path/'storage/.config/cloud_sync-rules.txt'
  200          rules.write_text('- /psp/PSP/SAVEDATA/Private/**\n+ /custom/progress.dat\n'+old+'\n+ /roms/**\n')
  201          seed(f, [PSP, DUCK, 'custom/progress.dat', 'psp/PSP/SAVEDATA/Private/DATA.BIN', 'roms/No.iso'])
  202          good(f, 'cloud_sync_helper')
  203          merged = rules.read_text()
  204          require('# inert: + /roms/**' in merged, 'old ineffective rule was activated')
  205          require(merged.index('- /psp/PSP/SAVEDATA/Private/**') < merged.index('+ /psp/PSP/SAVEDATA/**'), 'custom exclude lost precedence')
  206          require(rules.with_suffix('.txt.bak').read_text().startswith('- /psp/'), 'original custom rules not preserved')
  207          listed = set(good(f, 'filter-probe', '/storage/.config/cloud_sync-rules.txt').splitlines())
  208          require(listed == {PSP, DUCK, 'custom/progress.dat'}, 'upgrade coverage/custom precedence wrong: '+str(listed))
  209          first = rules.read_bytes()
  210          good(f, 'cloud_sync_helper')
  211          require(rules.read_bytes() == first, 'repeated merge changed rules')
  212      case('upgrade-custom-rules', upgrade)
  213  
  214      def content_setup(f):
  215          seed(f)
  216          for system, extension in [('psp', 'iso'), ('psx', 'chd'), ('n64', 'z64')]:
  217              fixture.put(f.path/'storage/roms'/system/('Kept.'+extension), 'ROM bytes\n')
  218              f.file('Chosen/Library/ROMs/'+system+'/Kept.'+extension, 'ROM bytes\n')
  219          for path in PROGRESS:
  220              if path.startswith(('psp/', 'psx/', 'n64/')):
  221                  f.file('Chosen/Library/ROMs/'+path, 'stale cloud progress '+path+'\n')
  222                  os.utime(f.path/'cloud/Chosen/Library/ROMs'/path, (time.time()+3600, time.time()+3600))
  223          f.directory('Chosen/Library/BIOS')
  224          return snapshot(f.path/'storage/roms'), snapshot(f.path/'cloud')
  225  
  226      def content_listing(f):
  227          content_setup(f)
  228          sizes = good(f, 'cloud_content_backup', '--list-sizes')
  229          rows = dict(line.split('|') for line in sizes.splitlines() if '|' in line)
  230          require(rows.get('psp') == '10' and rows.get('psx') == '10', 'local content counts progress: '+sizes)
  231          scan = good(f, 'cloud_content_restore', '--scan')
  232          rows = {line.split('|')[0]: line.split('|')[1:] for line in scan.splitlines() if '|' in line}
  233          for system in ('psp', 'psx', 'n64'):
  234              require(rows[system] == ['10', '1', '10', '0', '0', '0', '0'], 'content scan includes progress: '+scan)
  235          (f.path/'storage/roms/psp/Kept.iso').unlink()
  236          require('psp' not in good(f, 'cloud_content_backup', '--list').splitlines(), 'progress-only system offered as content')
  237      case('content-list-count-scan', content_listing)
  238  
  239      def content_backup(f, mode=None):
  240          before, _ = content_setup(f)
  241          shutil.rmtree(f.path/'cloud/Chosen/Library/ROMs')
  242          good(f, 'cloud_content_backup', '--all', *([mode] if mode else []))
  243          sent = snapshot(f.path/'cloud/Chosen/Library/ROMs')
  244          require(sent == {p: before[p] for p in ('psp/Kept.iso', 'psx/Kept.chd', 'n64/Kept.z64')}, 'content upload carried progress')
  245          require(snapshot(f.path/'storage/roms') == before, 'content upload changed local files')
  246      case('content-upload', content_backup)
  247      case('content-upload-with-media', lambda f: content_backup(f, '--with-media'))
  248  
  249      def content_restore(f, match=False, mode=None):
  250          before, cloud = content_setup(f)
  251          if match:
  252              fixture.put(f.path/'storage/roms/psp/Remove.iso', 'unwanted ROM\n')
  253              fixture.put(f.path/'storage/.cache/cloud_sync/content-systems', 'psp\npsx\nn64\n')
  254              good(f, 'cloud_content_restore', '--match')
  255              good(f, 'cloud_content_restore', '--match', '--apply')
  256          else:
  257              (f.path/'storage/roms/psp/Kept.iso').unlink()
  258              good(f, 'cloud_content_restore', '--all', *([mode] if mode else []))
  259          require(snapshot(f.path/'storage/roms') == before, 'content replaced or removed local progress')
  260          require(snapshot(f.path/'cloud') == cloud, 'content operation changed historical remote copies')
  261      case('content-restore', content_restore)
  262      case('content-restore-with-media', lambda f: content_restore(f, mode='--with-media'))
  263      case('content-match', lambda f: content_restore(f, True))
  264  
  265      def media_only(f):
  266          seed(f)
  267          progress_before = snapshot(f.path/'storage/roms')
  268          media = {'psp/gamelist.xml': '<gameList>valid content witness</gameList>\n',
  269                   'psp/images/Example.png': 'synthetic artwork bytes\n'}
  270          for path, value in media.items():
  271              fixture.put(f.path/'storage/roms'/path, value)
  272          good(f, 'cloud_content_backup', '--all', '--media-only')
  273          sent = snapshot(f.path/'cloud/Chosen/Library/ROMs')
  274          require(set(sent) == set(media), 'media-only upload included saves or missed game content')
  275          for path in media:
  276              (f.path/'storage/roms'/path).unlink()
  277          for path in (PSP, 'psp/PSP/SAVEDATA/ULUS00001/gamelist.xml'):
  278              f.file('Chosen/Library/ROMs/'+path, 'stale remote progress must stay remote\n')
  279              os.utime(f.path/'cloud/Chosen/Library/ROMs'/path, (time.time()+3600, time.time()+3600))
  280          cloud = snapshot(f.path/'cloud')
  281          good(f, 'cloud_content_restore', '--all', '--media-only')
  282          for path, value in media.items():
  283              require((f.path/'storage/roms'/path).read_text() == value, 'ordinary media not restored')
  284          restored = snapshot(f.path/'storage/roms')
  285          require({p: restored[p] for p in progress_before} == progress_before, 'media-only replaced progress')
  286          require(snapshot(f.path/'cloud') == cloud, 'media-only deleted historical copies')
  287          scan = good(f, 'cloud_content_restore', '--scan', '--media-only')
  288          row = next(line.split('|') for line in scan.splitlines() if line.startswith('psp|'))
  289          total = str(sum(len(value.encode()) for value in media.values()))
  290          require(row[1] == total and row[3] == total and row[4:6] == ['0', '0'], 'media-only counted savedata: '+scan)
  291      case('media-only-progress-boundary', media_only)
  292  
  293      def n64_scope(f):
  294          unrelated = ['psx/Other.st0', 'psp/Other.pj0.zip', 'n64/Other.st10',
  295                       'n64/subfolder/Other.st0']
  296          seed(f, unrelated + N64)
  297          listed = good(f, 'filter-probe', '/repo/cloud_sync-rules.txt').splitlines()
  298          require(set(listed) == set(N64), 'slot include escaped supported N64 root')
  299          good(f, 'cloud_content_backup', '--all')
  300          sent = snapshot(f.path/'cloud/Chosen/Library/ROMs')
  301          require(set(sent) == set(unrelated), 'content exclusions swallowed unrelated paths')
  302          local = snapshot(f.path/'storage/roms')
  303          for path in unrelated:
  304              (f.path/'storage/roms'/path).unlink()
  305          good(f, 'cloud_content_restore', '--all')
  306          require(snapshot(f.path/'storage/roms') == local, 'unrelated content no longer restores')
  307      case('n64-system-root-scope', n64_scope)
  308  
  309      def removed_system(f):
  310          before, cloud = content_setup(f)
  311          shutil.rmtree(f.path/'cloud/Chosen/Library/ROMs/n64')
  312          cloud = snapshot(f.path/'cloud')
  313          fixture.put(f.path/'storage/.cache/cloud_sync/content-systems', 'n64\n')
  314          good(f, 'cloud_content_restore', '--match')
  315          good(f, 'cloud_content_restore', '--match', '--apply')
  316          before.pop('n64/Kept.z64')
  317          require(snapshot(f.path/'storage/roms') == before, 'removed-system match removed progress')
  318          require(snapshot(f.path/'cloud') == cloud, 'removed-system match changed remote')
  319      case('content-match-removed-system', removed_system)
  320  
  321      def validate(f, path, state, detail=None):
  322          f.file('Chosen/Saves/'+path, 'synthetic save bytes\n')
  323          before = {'cloud': snapshot(f.path/'cloud'), 'storage': snapshot(f.path/'storage')}
  324          result = f.run('validator-call', 'saves', 'layout-proof')
  325          value = json.loads(result.stdout)
  326          row = value['categories'][0]
  327          require(result.returncode == (5 if state == 'unreadable' else 0), 'wrong validator outcome: '+result.stdout)
  328          require(row['state'] == state, 'wrong validator classification: '+result.stdout)
  329          if detail:
  330              require(row['detail'] == detail, 'wrong validator reason: '+result.stdout)
  331          require({'cloud': snapshot(f.path/'cloud'), 'storage': snapshot(f.path/'storage')} == before, 'validator wrote files')
  332          calls = (f.path/'ctl/argv').read_text().splitlines()
  333          require(all(line.startswith(('version', 'listremotes', 'config file', 'lsjson', 'backend features')) for line in calls), 'validator transferred payload')
  334          require(all('qa:/Chosen/Saves' in line for line in calls if line.startswith('lsjson')), 'validator escaped selected saves root')
  335          require(len([c for c in calls if c.startswith('lsjson')]) <= 3, 'unbounded listing count')
  336          require(value['scope']['max_seconds'] == 25 and value['scope']['max_entries_per_listing'] == 4096, 'existing bounds relaxed')
  337          return value
  338      case('validator-n64-state', lambda f: validate(f, N64[0], 'present'))
  339      case('validator-psp-depth5', lambda f: validate(f, PSP, 'present'))
  340      case('validator-duck-depth4', lambda f: validate(f, DUCK, 'present'))
  341      case('validator-unseen-deeper', lambda f: validate(f, 'psp/PSP/SAVEDATA/ID/deeper/DATA.BIN', 'unreadable', 'deeper-folders-not-checked'))
  342      case('validator-unrelated-depth', lambda f: validate(f, 'other/a/b/c/control.srm', 'unreadable', 'deeper-folders-not-checked'))
  343      case('validator-database', lambda f: validate(f, 'psp/PSP/SAVEDATA/ID/history.db', 'empty'))
  344  
  345      dispositions = {
  346          'canonical-state': ('savestates/nes/Example.state', 'present'),
  347          'canonical-auto-state': ('savestates/nes/Example.auto', 'present'),
  348          'canonical-screenshot': ('screenshots/Example.png', 'present'),
  349          'system-image-ambiguous': ('nes/images/Example.png', 'empty'),
  350          'system-screenshot-ambiguous': ('nes/screenshots/Example.png', 'empty'),
  351          'nds-dsv': ('nds/Example.dsv', 'present'),
  352          'nds-sav': ('nds/Example.sav', 'present'),
  353          'flat-srm': ('Example.srm', 'present'),
  354          'flat-state': ('Example.state', 'present'),
  355          'flat-image-ambiguous': ('Example.png', 'empty'),
  356          'card-in-savefiles': ('savefiles/Example_1.mcd', 'present'),
  357          'nested-state-unseen': ('saves/savestates/nes/Example.state', 'unreadable'),
  358      }
  359      for name, (path, state) in dispositions.items():
  360          case('validator-'+name, lambda f, path=path, state=state: validate(f, path, state))
  361  
  362      def failed_subtree(f):
  363          f.fault(r'^lsjson qa:/Chosen/Saves/psp/PSP/SAVEDATA ')
  364          validate(f, PSP, 'unreadable', 'listing-failed')
  365          require((f.path/'ctl/fault-fired').is_file(), 'subtree fault was not reached')
  366      case('validator-subtree-failure', failed_subtree)
  367      def subtree_bound(f, kind):
  368          shim = f.path/'shim/rclone'
  369          original = shim.read_text()
  370          code = {'entries': 'import json; print(json.dumps([{"Path":"ID/f"+str(i),"IsDir":False} for i in range(4097)]))',
  371                  'bytes': 'print("x" * (2 * 1024 * 1024 + 1))',
  372                  'timeout': 'import time; time.sleep(8)'}[kind]
  373          fixture.put(f.path/'repo/bound-output.py', code+'\n')
  374          hook = ('if [ "$1 $2" = "lsjson qa:/Chosen/Saves/psp/PSP/SAVEDATA" ]; then\n'
  375                  ' echo bound-fired >> /ctl/fault-fired\n'
  376                  ' exec python3 /repo/bound-output.py\nfi\n')
  377          shim.write_text(original.replace('exec /rclone.real "$@"', hook+'exec /rclone.real "$@"'))
  378          start = time.monotonic()
  379          validate(f, PSP, 'unreadable', 'listing-limit' if kind == 'entries' else 'time-or-listing-limit')
  380          require((f.path/'ctl/fault-fired').exists(), 'bound injection not reached')
  381          require(time.monotonic()-start < 9, 'bounded subtree command ran too long')
  382      for bound in ('entries', 'bytes', 'timeout'):
  383          case('validator-bound-'+bound, lambda f, bound=bound: subtree_bound(f, bound))
  384      if args.cases:
  385          require(set(args.cases.split(',')) == {r['case'] for r in results}, 'unknown selected case')
  386      require(results, 'no cases selected')
  387      summary = {'results': results, 'passed': sum(r['result'] == 'PASS' for r in results),
  388                 'failed': sum(r['result'] == 'FAIL' for r in results),
  389                 'source_root': str(args.source_root), 'source_ref': args.ref,
  390                 'fixture_source_sha256': sources,
  391                 'fixture_override': ['cloud_device_id'],
  392                 'source_sha256': {p.name: hashlib.sha256(subprocess.check_output(['git', '-C', str(args.source_root), 'show', args.ref+':'+str(SOURCES/p.name)]) if args.ref else p.read_bytes()).hexdigest() for p in (args.source_root/SOURCES).iterdir() if p.is_file()}, 'rclone_sha256': hashlib.sha256(Path(args.rclone).read_bytes()).hexdigest()}
  393      if busybox:
  394          counts = {applet: 0 for applet in ('find', 'awk')}
  395          for log in args.output.glob('*/ctl/busybox-calls'):
  396              for applet in log.read_text().splitlines():
  397                  counts[applet] += 1
  398          require(all(counts.values()), 'requested image applet was never invoked by the controls')
  399          summary['busybox'] = {'source': str(args.busybox),
  400                                'sha256': hashlib.sha256(busybox.read_bytes()).hexdigest(),
  401                                'invocations': counts,
  402                                'scope': 'Image find/awk applets; host bash/Python and pinned rclone fixture'}
  403      (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
  404      print(f"save-layout: {summary['passed']} PASS, {summary['failed']} FAIL", flush=True)
  405      return bool(summary['failed'])
  406  
  407  
  408  if __name__ == '__main__':
  409      sys.exit(main())
```

## File: tools/pixelelated-vm-cloud-boundaries (at 8ebaf8daad, 724 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Focused installed-image cloud boundaries and real pair recovery (#356/#365).
    5  
    6  Owns a fresh pair and local WebDAV backend. Run through watch-build-submit.
    7  Every case resets both guests and the cloud. No production binary is replaced;
    8  a selected rclone operation may be faulted through the supported profile path.
    9  """
   10  import argparse
   11  import datetime
   12  import hashlib
   13  import io
   14  import json
   15  import os
   16  from pathlib import Path
   17  import re
   18  import shlex
   19  import signal
   20  import subprocess
   21  import sys
   22  import tarfile
   23  import time
   24  
   25  CONF = '/storage/.config/cloud_sync.conf'
   26  QA = '/tmp/pixelelated-cloud-boundaries'
   27  SHIM = '/storage/.config/profile.d/999-cloud-boundaries-qa.sh'
   28  SOURCES = 'projects/ROCKNIX/packages/network/rclone/sources'
   29  
   30  
   31  def require(value, message):
   32      if not value:
   33          raise AssertionError(message)
   34  
   35  
   36  def sha(path):
   37      return hashlib.sha256(path.read_bytes()).hexdigest()
   38  
   39  
   40  def save(path, value):
   41      path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
   42  
   43  
   44  class Proof:
   45      def __init__(self, args):
   46          self.args = args
   47          self.tree = args.tree.resolve(strict=True)
   48          self.owner = args.output.resolve(strict=True)
   49          require(not any(self.owner.iterdir()), 'output must be a fresh empty directory')
   50          self.pair = self.owner / 'pair'
   51          self.cloud = self.owner / 'cloud'
   52          self.data = self.cloud / 'data'
   53          self.logs = self.owner / 'artifacts'
   54          for p in (self.pair, self.cloud, self.logs):
   55              p.mkdir(mode=0o700)
   56          self.env = dict(os.environ, VM_PAIR_DIR=str(self.pair), CLOUD_QA_STATE=str(self.cloud),
   57                          CLOUD_QA_BACKEND='webdav', CLOUD_QA_PORT='9040', VM_GL='none')
   58          self.seq = 0
   59          self.results = []
   60          self.case = 'setup'
   61          self.backend_started = False
   62          self.original_scripts = {}
   63  
   64      def local(self, tool, *args, **kwargs):
   65          return subprocess.run([str(self.tree / 'tools' / tool), *args],
   66                                env=self.env, cwd=self.tree, check=True, **kwargs)
   67  
   68      def on(self, guest, command, allowed=(0,), data=None):
   69          port = {'a': '10022', 'b': '10023'}[guest]
   70          result = subprocess.run(['ssh', '-i', str(self.pair / 'qa-key'), '-p', port,
   71              '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=no',
   72              '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR',
   73              '-o', 'ConnectTimeout=8', 'root@127.0.0.1',
   74              '. /etc/profile >/dev/null 2>&1; ' + command],
   75              input=data, capture_output=True, text=True, timeout=180)
   76          self.seq += 1
   77          # Only synthetic QA state is used. Do not log setup stdin/config values.
   78          text = result.stdout + result.stderr
   79          text = '\n'.join(x for x in text.splitlines()
   80                           if not re.search(r'key|passw|token|user|psk', x, re.I)) + '\n'
   81          prefix = self.logs / f'{self.seq:04d}-{self.case}-{guest}'
   82          prefix.with_suffix('.log').write_text(text)
   83          prefix.with_suffix('.rc').write_text(str(result.returncode) + '\n')
   84          require(allowed is None or result.returncode in allowed,
   85                  f'{self.case}/{guest}: rc{result.returncode}; see {prefix.name}.log')
   86          return result
   87  
   88      def pointers(self, guest='a'):
   89          text = self.on(guest, "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=|^LAYOUT_KEEP=' " + CONF).stdout
   90          return {k: v.strip('"') for k, v in (x.split('=', 1) for x in text.splitlines())}
   91  
   92      def conf(self, saves='/ROCKNIX/Saves', backups='/ROCKNIX/Backups', content='/ROCKNIX/Content', guest='a'):
   93          values = dict(SAVES_REMOTE=saves, SETTINGS_REMOTE=backups, CONTENT_REMOTE=content, LAYOUT_KEEP='')
   94          # Rewrite only named QA fields; None means genuinely omitted.
   95          script = "sed -i '/^SAVES_REMOTE=/d; /^SETTINGS_REMOTE=/d; /^CONTENT_REMOTE=/d; /^LAYOUT_KEEP=/d' " + CONF + '\n'
   96          for key, value in values.items():
   97              if value is not None:
   98                  script += 'printf "%s\\n" ' + shlex.quote(f'{key}="{value}"') + ' >> ' + CONF + '\n'
   99          self.on(guest, 'set -e; ' + script)
  100          actual = self.pointers(guest)
  101          require(all(actual.get(k) == v for k, v in values.items()), 'fixture pointers did not persist')
  102  
  103      def put(self, relative, data=b'sentinel\n'):
  104          path = self.data / relative.lstrip('/')
  105          path.parent.mkdir(parents=True, exist_ok=True)
  106          path.write_bytes(data)
  107          return path
  108  
  109      def hashes(self):
  110          return {str(p.relative_to(self.data)): sha(p)
  111                  for p in sorted(self.data.rglob('*')) if p.is_file()}
  112  
  113      def reset(self):
  114          self.cursors = {}
  115          for guest in ('a', 'b'):
  116              self.on(guest, f'set -e; rm -f {QA}/sed {QA}/mv {QA}/pointer-fired; '
  117                      f'cp {QA}/original-rclone.conf /storage/.config/rclone/rclone.conf; '
  118                      f'cp {QA}/original-sync.conf {CONF}')
  119              self.on(guest, f'set -e; rm -f {QA}/fault {QA}/fired /storage/.config/cloud-layout-migration.json; '
  120                      'rm -rf /storage/.cache/cloud_sync/scan')
  121              cursor = self.on(guest, 'journalctl -n 0 --show-cursor --no-pager').stdout
  122              self.cursors[guest] = next(x[11:] for x in cursor.splitlines() if x.startswith('-- cursor: '))
  123          self.local('cloud-test-backend', 'reset', stdout=subprocess.DEVNULL)
  124          for guest in ('a', 'b'):
  125              self.conf(guest=guest)
  126          save(self.logs / (self.case + '-reset.json'),
  127               {'cloud': self.hashes(), 'a': self.pointers(), 'b': self.pointers('b')})
  128          require(not self.hashes(), 'backend reset left payloads')
  129  
  130      def fault(self, operation, path):
  131          self.on('a', 'printf "%s\\n" ' + shlex.quote(operation + ' ' + path) + f' > {QA}/fault')
  132  
  133      def clear_fault(self):
  134          self.on('a', f'rm -f {QA}/fault')
  135  
  136      def migrate(self, mode='--apply', guest='a', allowed=(0,)):
  137          return self.on(guest, '/usr/bin/cloud_migrate_layout ' + shlex.quote(mode), allowed=allowed)
  138  
  139      def follower(self):
  140          before = self.hashes()
  141          self.on('b', 'test ! -e /storage/.config/cloud-layout-migration.json')
  142          cursor = self.on('b', "journalctl -n 0 --show-cursor --no-pager").stdout
  143          cursor = next(x[11:] for x in cursor.splitlines() if x.startswith('-- cursor: '))
  144          self.on('b', '/usr/bin/cloud_scan --folder')
  145          require(self.pointers('b')['SAVES_REMOTE'] == '/pixelelated/Saves', 'separate guest did not follow')
  146          self.on('b', 'grep -qx STATE=current /storage/.cache/cloud_sync/scan/state')
  147          self.migrate('--needs-step', guest='b', allowed=(1,))
  148          journal = self.on('b', 'journalctl -t cloud_migrate_layout --no-pager --after-cursor=' + shlex.quote(cursor)).stdout
  149          require('follow' in journal.lower(), 'separate guest has no follow journal')
  150          require(before == self.hashes(), 'separate follower changed cloud bytes')
  151          save(self.logs / (self.case + '-follower.json'),
  152               {'a': self.pointers(), 'b': self.pointers('b'), 'cloud': self.hashes(),
  153                'no_dialog_basis': 'folder state current and needs-step exit1', 'journal': journal})
  154  
  155      def migration_case(self, fault=None):
  156          payloads = {'Saves/gb/A.srm': b'save bytes\n', 'Backups/QA/settings.tar.gz': b'settings bytes\n',
  157                      'Saves-replaced/gb/A.srm': b'previous progress\n', 'Content/ROMs/gb/A.gb': b'game bytes\n'}
  158          for path, data in payloads.items():
  159              self.put('ROCKNIX/' + path, data)
  160          if fault is None:
  161              self.put('pixelelated/.layout', b'layout=1\n')
  162          save(self.logs / (self.case + '-initial.json'), {'cloud': self.hashes(), 'pointers': self.pointers()})
  163          if fault:
  164              operation, stage = fault
  165              path = self.remote + ('/pixelelated/.layout' if stage == 'marker' else '/ROCKNIX/' + stage)
  166              self.fault(operation, path)
  167              require(self.migrate(allowed=None).returncode != 0, 'faulted move reported success')
  168              self.on('a', f'test -s {QA}/fired')
  169              require(not (self.data / 'pixelelated/.layout').exists(), 'fault published success marker')
  170              for path, data in payloads.items():
  171                  require(any((self.data / root / path).is_file() and (self.data / root / path).read_bytes() == data
  172                              for root in ('ROCKNIX', 'pixelelated')), 'fault lost ' + path)
  173              save(self.logs / (self.case + '-interrupted.json'), {'cloud': self.hashes(), 'pointers': self.pointers()})
  174              self.clear_fault()
  175          self.migrate()
  176          for path, data in payloads.items():
  177              require((self.data / 'pixelelated' / path).read_bytes() == data, 'moved payload changed: ' + path)
  178              require(not (self.data / 'ROCKNIX' / path).exists(), 'old duplicate: ' + path)
  179          require((self.data / 'pixelelated/.layout').read_bytes() == b'layout=2\n', 'exact layout2 marker missing')
  180          self.on('a', 'test ! -e /storage/.config/cloud-layout-migration.json')
  181          journal = self.on('a', 'journalctl -t cloud_migrate_layout --no-pager --after-cursor=' +
  182                            shlex.quote(self.cursors['a'])).stdout
  183          for stage in ['begin', 'backups', 'saves', 'discarded', 'content', 'complete']:
  184              require('migration step=1 from=1 to=2 stage=' + stage in journal,
  185                      'numbered journal stage missing from this case: ' + stage)
  186          before = (self.hashes(), self.pointers())
  187          self.migrate(allowed=(0, 3))
  188          require((self.hashes(), self.pointers()) == before, 'repeat changed bytes/pointers')
  189          self.follower()
  190  
  191      def backup_choice(self, mode, root, custom):
  192          saves = '/GAMES' if root == '/GAMES' else root + '/Saves'
  193          backups = '/Mine/Backups' if custom else root + ('/backup' if root == '/GAMES' else '/Backups')
  194          self.conf(saves, backups, root + '/Content')
  195          path = 'QA/2026_10_01-120000-QA-ROCKNIX_SETTINGS.tar.gz'
  196          self.put(backups + '/' + path, b'independent settings sentinel\n')
  197          (self.data / 'pixelelated/Saves').mkdir(parents=True)
  198          before = self.hashes()
  199          self.migrate(mode, allowed=(0, 3))
  200          pointer = self.pointers()['SETTINGS_REMOTE']
  201          require((self.data / pointer.lstrip('/') / path).read_bytes() == b'independent settings sentinel\n',
  202                  'independent settings were abandoned')
  203          require(before == self.hashes(), 'pointer-only follow/settle changed payloads')
  204  
  205      def content_choice(self, mode, choice):
  206          saves = '/pixelelated/Saves' if mode == '--join' else '/ROCKNIX/Saves'
  207          self.conf(saves, '/ROCKNIX/Backups', choice)
  208          if mode == '--join':
  209              self.put('ROCKNIX/Saves/gb/A.srm')
  210          if mode == '--follow':
  211              (self.data / 'pixelelated/Saves').mkdir(parents=True)
  212          if choice == '':
  213              self.put('ROMs/gb/Root.gb', b'root content sentinel\n')
  214          self.migrate(mode, allowed=(0, 3))
  215          derived = '/ROCKNIX/Content' if mode == '--join' else '/pixelelated/Content'
  216          expected = derived if choice is None or choice == '/ROCKNIX/Content' else choice
  217          require(self.pointers().get('CONTENT_REMOTE') == expected, 'independent content choice changed')
  218          if choice == '':
  219              require((self.data / 'ROMs/gb/Root.gb').read_bytes() == b'root content sentinel\n', 'root content lost')
  220  
  221      def two_roots(self, configured):
  222          self.conf(configured, '/GAMES/backup' if configured == '/GAMES' else '/ROCKNIX/Backups', '')
  223          self.put('GAMES/gb/A.srm', b'games progress\n')
  224          self.put('ROCKNIX/Saves/gb/A.srm', b'rocknix progress\n')
  225          before = self.hashes()
  226          self.on('a', '/usr/bin/cloud_scan --folder')
  227          require(self.pointers()['SAVES_REMOTE'] == configured, 'configured-first choice changed')
  228          require(self.hashes() == before, 'discovery changed either populated root')
  229  
  230      def collision(self):
  231          self.put('ROCKNIX/Saves/gb/A.srm', b'local progress\n')
  232          self.put('ROCKNIX/Content/ROMs/gb/A.gb', b'old content\n')
  233          self.put('pixelelated/Content/ROMs/gb/A.gb', b'foreign content\n')
  234          before = self.audit_snapshot()
  235          record = '/storage/.config/cloud-layout-migration.json'
  236          self.on('a', 'test ! -e ' + record)
  237          refusals = []
  238          for attempt in range(2):
  239              result = self.migrate(allowed=None)
  240              require(result.returncode != 0, 'foreign content collision accepted')
  241              require('>>> why THE NEW FOLDER ALREADY HAS FILES IN IT' in result.stdout,
  242                      'collision returned an unrelated refusal')
  243              require(self.audit_snapshot() == before, 'collision refusal changed cloud data or settings')
  244              self.on('a', 'test ! -e ' + record)
  245              refusals.append({'attempt': attempt + 1, 'returncode': result.returncode})
  246          require((self.data / 'pixelelated/Content/ROMs/gb/A.gb').read_bytes() == b'foreign content\n', 'foreign content overwritten')
  247          require((self.data / 'ROCKNIX/Content/ROMs/gb/A.gb').read_bytes() == b'old content\n', 'old content lost')
  248          require((self.data / 'ROCKNIX/Saves/gb/A.srm').read_bytes() == b'local progress\n', 'original save changed')
  249          require(not (self.data / 'pixelelated/.layout').exists(), 'collision marked complete')
  250          require(self.pointers()['CONTENT_REMOTE'] == '/ROCKNIX/Content', 'refused content pointer advanced')
  251          save(self.logs / 'content-collision-refusal.json',
  252               {'before': before, 'after': self.audit_snapshot(), 'refusals': refusals,
  253                'recovery_record_absent': True})
  254  
  255      def restricted(self):
  256          self.conf('/pixelelated/Saves', '/pixelelated/Backups', '/pixelelated/Content')
  257          self.put('pixelelated/Saves/gb/A.srm')
  258          before = (self.hashes(), self.pointers())
  259          self.fault('lsf-root', self.remote)
  260          require(self.on('a', 'rclone lsf ' + shlex.quote(self.remote) + ' --dirs-only', allowed=None).returncode != 0,
  261                  'parent-list fault is not armed')
  262          self.on('a', f'test -s {QA}/fired; rm -f {QA}/fired')
  263          self.on('a', 'rclone lsf ' + shlex.quote(self.remote + '/pixelelated/Saves') + ' --recursive')
  264          self.on('a', '/usr/bin/cloud_scan --folder')
  265          require((self.hashes(), self.pointers()) == before, 'restricted folder scan changed bytes/pointers')
  266          require(self.on('a', '/usr/bin/cloud_scan', allowed=None).returncode != 0, 'full chooser hid denied parent listing')
  267          self.on('a', f'test -s {QA}/fired')
  268          require((self.hashes(), self.pointers()) == before, 'restricted full scan changed bytes/pointers')
  269  
  270      def start(self):
  271          for p in Path('/proc').glob('[0-9]*/cmdline'):
  272              try:
  273                  name = Path(p.read_bytes().split(b'\0', 1)[0].decode()).name
  274              except (FileNotFoundError, ProcessLookupError):
  275                  continue
  276              require(not name.startswith('qemu-system-'), 'another QEMU owns VM resources')
  277          self.local('vm-pair', 'up', str(self.args.image.resolve(strict=True)))
  278          self.backend_started = True
  279          self.local('cloud-test-backend', 'up')
  280          config = self.local('cloud-test-backend', 'rclone-conf', capture_output=True, text=True).stdout
  281          identities = []
  282          for guest in ('a', 'b'):
  283              self.on(guest, 'set -e; systemctl stop essway; set_setting cloudsaves.startup 0; '
  284                      'set_setting cloudsaves.gameexit 0; mkdir -p /storage/.config/rclone; '
  285                      'cat > /storage/.config/rclone/rclone.conf; chmod 600 /storage/.config/rclone/rclone.conf', data=config)
  286              self.on(guest, '/usr/bin/cloud_sync_helper')
  287              build = self.on(guest, 'sed -n \'s/^BUILD_ID="\\(.*\\)"/\\1/p\' /etc/os-release').stdout.strip()
  288              require(build == self.args.build_id, 'guest BUILD_ID differs from frozen candidate')
  289              identities.append({'guest': guest, 'build': build, 'boot_id': self.on(guest, 'cat /proc/sys/kernel/random/boot_id').stdout.strip(),
  290                                 'device_id': self.on(guest, '/usr/bin/cloud_device_id').stdout.strip()})
  291              for script in ['cloud_migrate_layout', 'cloud_scan', 'cloud_setup', 'cloud_content_restore']:
  292                  value = self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0]
  293                  require(value == sha(self.tree / SOURCES / script), 'installed source mismatch: ' + script)
  294                  self.original_scripts[guest + '/' + script] = value
  295              self.on(guest, f'test ! -e {QA} && test ! -e {SHIM}; mkdir -p {QA} /storage/.config/profile.d')
  296              self.on(guest, f'set -e; cp {CONF} {QA}/original-sync.conf; '
  297                      f'cp /storage/.config/rclone/rclone.conf {QA}/original-rclone.conf')
  298          require(identities[0]['boot_id'] != identities[1]['boot_id'] and
  299                  identities[0]['device_id'] != identities[1]['device_id'], 'pair is not two independent devices')
  300          save(self.logs / 'identities.json', identities)
  301          self.remote = self.on('a', '/usr/bin/rclone listremotes').stdout.strip()
  302          require(re.fullmatch(r'[A-Za-z0-9_-]+:', self.remote), 'expected exactly one QA remote')
  303          shim = f'''#!/bin/sh
  304  if [ -f {QA}/fault ]; then
  305   expected=$(cat {QA}/fault)
  306   matched=no
  307   [ "$1 $2" != "$expected" ] || matched=yes
  308   if [ "$1" = lsf ] && [ "$expected" = "lsf-root {self.remote}" ]; then
  309    for arg in "$@"; do [ "$arg" != "{self.remote}" ] || matched=yes; done
  310   fi
  311   if [ "$1" = lsf ]; then
  312    case "$expected" in
  313     'lsf-path '*)
  314      path=${{expected#lsf-path }}
  315      for arg in "$@"; do [ "${{arg%/}}" != "${{path%/}}" ] || matched=yes; done ;;
  316    esac
  317   fi
  318   if [ "$matched" = yes ]; then
  319    printf '%s\\n' "$*" >> {QA}/fired
  320    echo 'injected local QA provider refusal' >&2
  321    exit 5
  322   fi
  323  fi
  324  exec /usr/bin/rclone "$@"
  325  '''
  326          self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone', data=shim)
  327          self.on('a', 'printf "%s\\n" ' + shlex.quote(f'export PATH={QA}:$PATH') + f' > {SHIM}')
  328          require(self.on('a', 'command -v rclone').stdout.strip() == QA + '/rclone', 'provider shim not selected')
  329  
  330      def audit_snapshot(self):
  331          return dict(cloud=self.hashes(), pointers=self.pointers(),
  332                      config_sha256=self.on('a', 'sha256sum ' + CONF).stdout.split()[0])
  333  
  334      def audit_current(self, content='/pixelelated/Content'):
  335          self.conf('/pixelelated/Saves', '/pixelelated/Backups', content)
  336          self.put('pixelelated/Saves/gb/current.srm', b'current progress\n')
  337          self.put('pixelelated/.layout', b'layout=2\n')
  338  
  339      def audit_atomic(self, mode, boundary):
  340          root = '/pixelelated' if mode == '--join' else '/ROCKNIX'
  341          self.conf(root + '/Saves', root + '/Backups', root + '/Content')
  342          if mode == '--join':
  343              self.put('ROCKNIX/Saves/gb/A.srm')
  344          elif mode == '--follow':
  345              self.put('pixelelated/Saves/gb/A.srm')
  346          self.on('a', 'chmod 640 ' + CONF)
  347          before = self.audit_snapshot()
  348          command = 'mv' if boundary == 'publish' else 'sed'
  349          match = '[ "${!#}" = ' + CONF + ' ]' if command == 'mv' else f'[[ "$*" == *"^{boundary}="* ]]'
  350          shim = f'#!/bin/bash\nif {match}; then echo fired > {QA}/pointer-fired; exit 1; fi\nexec /usr/bin/{command} "$@"\n'
  351          self.on('a', f'cat > {QA}/{command}; chmod 755 {QA}/{command}', data=shim)
  352          interrupted = self.migrate(mode, allowed=None)
  353          self.on('a', f'test -s {QA}/pointer-fired; rm -f {QA}/{command}')
  354          require(interrupted.returncode != 0, 'pointer-publication fault reported success')
  355          require(self.audit_snapshot() == before, 'partial pointer set became live')
  356          self.migrate(mode)
  357          target = '/ROCKNIX' if mode == '--join' else '/pixelelated'
  358          require(all(self.pointers()[k] == target + '/' + suffix for k, suffix in
  359                      [('SAVES_REMOTE', 'Saves'), ('SETTINGS_REMOTE', 'Backups'), ('CONTENT_REMOTE', 'Content')]),
  360                  'retry left a mixed pointer set')
  361          require(self.hashes() == before['cloud'], 'pointer-only transition changed cloud bytes')
  362          require(self.on('a', "stat -c '%a' " + CONF).stdout.strip() == '640', 'config mode changed')
  363          save(self.logs / (self.case + '-publication.json'), dict(before=before, after=self.audit_snapshot()))
  364  
  365      def audit_sibling(self, content):
  366          self.audit_current(content)
  367          self.put('ROCKNIX/Saves/gb/kept.srm', b'sibling progress\n')
  368          self.put('ROCKNIX/Saves-replaced/stamp/gb/older.srm', b'sibling older progress\n')
  369          self.migrate('--keep', guest='b')
  370          before = self.audit_snapshot(), self.pointers('b')
  371          for _ in range(2):
  372              self.on('a', '/usr/bin/cloud_scan --folder')
  373              self.on('a', 'grep -qx STATE=current /storage/.cache/cloud_sync/scan/state')
  374              self.migrate(allowed=(0, 3))
  375              require((self.audit_snapshot(), self.pointers('b')) == before, 'active sibling shelf moved')
  376  
  377      def audit_binding(self, kind):
  378          self.put('ROCKNIX/Saves/gb/A.srm', b'save witness\n')
  379          self.put('ROCKNIX/Content/ROMs/gb/A.gb', b'content witness\n')
  380          self.fault('copy', self.remote + '/ROCKNIX/Content')
  381          if kind == 'legacy':
  382              ref = '7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2'
  383              old = subprocess.check_output(['git', '-C', str(self.tree), 'show', ref + ':' + SOURCES + '/cloud_migrate_layout'])
  384              self.on('a', f'cat > {QA}/predecessor; chmod 755 {QA}/predecessor', data=old.decode())
  385              first = self.on('a', f'{QA}/predecessor --apply', allowed=None)
  386              save(self.logs / (self.case + '-predecessor.json'), dict(ref=ref, sha256=hashlib.sha256(old).hexdigest()))
  387          else:
  388              first = self.migrate(allowed=None)
  389          require(first.returncode != 0, 'copy interruption did not fire')
  390          record = '/storage/.config/cloud-layout-migration.json'
  391          self.on('a', f'test -s {QA}/fired; test -s {record}')
  392          self.clear_fault()
  393          config = '/storage/.config/rclone/rclone.conf'
  394          if kind == 'legacy':
  395              self.on('a', f"jq -e 'has(\"fingerprint_format\") | not' {record} >/dev/null")
  396          if kind == 'endpoint':
  397              self.put('other-cloud/foreign-witness.txt', b'other connection\n')
  398          before = self.audit_snapshot()
  399          record_hash = self.on('a', 'sha256sum ' + record).stdout.split()[0]
  400          if kind == 'comments':
  401              self.on('a', "printf '\\n# harmless QA comment\\n' >> " + config)
  402          elif kind == 'token':
  403              self.on('a', "printf '\\ntoken = synthetic-unused\\n' >> " + config)
  404          elif kind == 'format':
  405              self.on('a', 'python3 -', data=f'''from pathlib import Path
  406  p=Path({config!r})
  407  lines=p.read_text().splitlines()
  408  header=[x for x in lines if x.startswith('[')]
  409  fields=[x for x in lines if '=' in x and not x.lstrip().startswith(('#',';'))]
  410  p.write_text('; harmless QA header\\n'+ '\\n'.join(header+list(reversed([x.replace(' = ', '=') for x in fields])))+'\\n')
  411  ''')
  412          elif kind == 'endpoint':
  413              self.on('a', 'python3 -', data=f'''from pathlib import Path
  414  import re
  415  p=Path({config!r})
  416  text,n=re.subn(r'^url\\s*=\\s*(.*?)\\s*$', lambda m:'url = '+m[1].rstrip('/')+'/other-cloud/', p.read_text(), flags=re.M)
  417  assert n==1
  418  p.write_text(text)
  419  ''')
  420          state = self.migrate('--state', allowed=None)
  421          if kind == 'endpoint':
  422              require(state.returncode == 5 and 'NEEDS ITS ORIGINAL CONNECTION' in state.stdout,
  423                      'changed binding was not truthfully refused')
  424              for command in ['/usr/bin/cloud_migrate_layout --apply', '/usr/bin/cloud_setup --seed-folders']:
  425                  result = self.on('a', command, allowed=None)
  426                  require(result.returncode != 0 and 'NEEDS ITS ORIGINAL CONNECTION' in result.stdout,
  427                          'recovery entry point lost the binding reason')
  428              require(self.audit_snapshot() == before, 'binding refusal changed cloud/settings')
  429              require(self.on('a', 'sha256sum ' + record).stdout.split()[0] == record_hash, 'record was rebound')
  430              self.on('a', f'cp {QA}/original-rclone.conf {config}')
  431          else:
  432              require(state.returncode == 0 and 'STATE=migration-pending' in state.stdout,
  433                      'harmless rewrite stranded the move')
  434          self.migrate()
  435          self.on('a', 'test ! -e ' + record)
  436          require((self.data / 'pixelelated/Saves/gb/A.srm').read_bytes() == b'save witness\n', 'save lost')
  437          require((self.data / 'pixelelated/Content/ROMs/gb/A.gb').read_bytes() == b'content witness\n', 'content lost')
  438  
  439      def audit_reader(self, kind):
  440          self.audit_current()
  441          forms = {
  442              'escaped': r'SETTINGS_REMOTE="/Custom/My\$Backups"',
  443              'single': "SETTINGS_REMOTE='/Custom/Backups' # comment",
  444              'bare': 'SETTINGS_REMOTE=/Custom/Backups # comment',
  445              'double': 'SETTINGS_REMOTE="/Custom/Backups" # comment',
  446              'duplicate': 'SETTINGS_REMOTE="/Custom/Backups"\nSETTINGS_REMOTE="/Other/Backups"',
  447              'export': 'export SETTINGS_REMOTE="/Custom/Backups"',
  448              'trailing': 'SETTINGS_REMOTE="/Custom/Backups" invalid',
  449              'control': 'SETTINGS_REMOTE="/Custom/Backups"\r',
  450          }
  451          self.on('a', "sed -i '/^SETTINGS_REMOTE=/d' " + CONF + '; printf "%s\\n" ' +
  452                  shlex.quote(forms[kind]) + ' >> ' + CONF)
  453          malformed = kind in ('export', 'trailing', 'control')
  454          expected = '/Custom/My$Backups' if kind == 'escaped' else '/Custom/Backups'
  455          if not malformed:
  456              label = self.on('a', '/usr/bin/cloud_device_id --label').stdout.strip()
  457              device = self.on('a', '/usr/bin/cloud_device_id').stdout.strip()
  458              require(re.fullmatch(r'[A-Za-z0-9_-]+', label) and
  459                      re.fullmatch(r'[A-Za-z0-9_-]+', device), 'unsafe fixture identity')
  460              archive = '2026_10_06-120000-' + label + '-ROCKNIX_SETTINGS.tar.gz'
  461              wrong_archive = '2026_10_06-130000-' + label + '-ROCKNIX_SETTINGS.tar.gz'
  462              payload = io.BytesIO()
  463              with tarfile.open(fileobj=payload, mode='w:gz') as tar:
  464                  info = tarfile.TarInfo('storage/.config/reader-sentinel')
  465                  witness = b'correct parsed settings directory\n'
  466                  info.size = len(witness)
  467                  tar.addfile(info, io.BytesIO(witness))
  468              self.put(expected + '/' + device + '/' + archive, payload.getvalue())
  469              wrong = '/Custom/My\\$Backups' if kind == 'escaped' else '/Other/Backups'
  470              self.put(wrong + '/' + device + '/' + wrong_archive, payload.getvalue())
  471          before = self.audit_snapshot()
  472          original_shim = None
  473          if malformed:
  474              # listremotes reads local rclone configuration. Faulting it made
  475              # prepare() stop before the malformed cloud config was read.
  476              # Observe calls without replacing their results; permit only that
  477              # local enumeration, and reject every provider operation.
  478              original_shim = self.on('a', f'cat {QA}/rclone').stdout
  479              observer = (f'#!/bin/sh\nprintf "%s\\n" "$1" >> {QA}/reader-calls\n'
  480                          'exec /usr/bin/rclone "$@"\n')
  481              self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone; : > {QA}/reader-calls',
  482                      data=observer)
  483          try:
  484              if malformed:
  485                  self.on('a', 'rclone lsf ' + shlex.quote(self.remote) + ' --max-depth 1 >/dev/null')
  486                  control = self.on('a', f'cat {QA}/reader-calls').stdout.splitlines()
  487                  require(control == ['lsf'], 'provider observer did not see its real negative control')
  488                  self.on('a', f': > {QA}/reader-calls')
  489              for command in ['/usr/bin/cloud_migrate_layout --state', '/usr/bin/cloud_scan']:
  490                  result = self.on('a', command, allowed=None)
  491                  require((result.returncode != 0) == malformed, 'reader disagreement: ' + kind)
  492                  if malformed:
  493                      require(">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ" in result.stdout,
  494                              'malformed config did not reach its own refusal: ' + kind)
  495                  elif command.endswith('--state'):
  496                      facts = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
  497                      require(facts.get('BACKUPS') == expected, 'state decoded the wrong settings value')
  498              if not malformed:
  499                  facts = dict(line.split('=', 1) for line in self.on(
  500                      'a', 'cat /storage/.cache/cloud_sync/scan/settings').stdout.splitlines() if '=' in line)
  501                  require(facts.get('MINE') == archive and
  502                          facts.get('SOURCE', '').rstrip('/') == self.remote + expected + '/' + device,
  503                          'full scan selected the wrong parsed directory or duplicate assignment')
  504                  save(self.logs / (self.case + '-value-selection.json'),
  505                       {'expected_directory': expected, 'expected_archive': archive,
  506                        'wrong_directory': wrong, 'wrong_archive': wrong_archive, 'scan': facts})
  507              require(self.audit_snapshot() == before, 'reader changed cloud/settings')
  508              if malformed:
  509                  calls = self.on('a', f'cat {QA}/reader-calls').stdout.splitlines()
  510                  require(all(call == 'listremotes' for call in calls),
  511                          'malformed configuration reached provider operations: ' + repr(calls))
  512                  save(self.logs / (self.case + '-provider-observation.json'),
  513                       {'control_calls': control, 'malformed_calls': calls,
  514                        'allowed_local_operation': 'listremotes', 'cloud_and_config_unchanged': True})
  515          finally:
  516              if original_shim is not None:
  517                  self.on('a', f'cat > {QA}/rclone; chmod 755 {QA}/rclone', data=original_shim)
  518  
  519      def audit_chooser(self, folder):
  520          self.audit_current()
  521          self.put(folder + '/ROMs/gb/Chosen.gb', b'chosen content\n')
  522          self.on('a', '/usr/bin/cloud_scan')
  523          listed = self.on('a', 'cat /storage/.cache/cloud_sync/scan/root-dirs').stdout.splitlines()
  524          require(folder in listed, 'ordinary folder not offered')
  525          before = self.hashes()
  526          self.on('a', '/usr/bin/cloud_setup --set-content-remote ' + shlex.quote('/' + folder))
  527          require(self.pointers()['CONTENT_REMOTE'] == '/' + folder, 'selection was not saved')
  528          self.on('a', '/usr/bin/cloud_scan --content')
  529          listing = self.on('a', 'cat /storage/.cache/cloud_sync/scan/scan').stdout
  530          require(re.search(r'^gb\|15\|', listing, re.M), 'chosen content missing from scan')
  531          require(self.hashes() == before, 'folder selection changed cloud bytes')
  532          selected = self.audit_snapshot()
  533          for invalid in ['/a/../b', '/a/./b', '/a//b', '/$HOME', '/`id`', '/two\nlines', '/trailing\n']:
  534              require(self.on('a', '/usr/bin/cloud_setup --set-content-remote ' + shlex.quote(invalid),
  535                              allowed=None).returncode != 0, 'unsafe name accepted')
  536              require(self.audit_snapshot() == selected, 'unsafe name changed settings')
  537  
  538      def audit_reason(self, kind):
  539          self.audit_current()
  540          expected = "YOUR CLOUD FOLDER COULDN'T BE READ"
  541          if kind in ('future', 'malformed'):
  542              self.put('pixelelated/.layout', b'layout=999\n' if kind == 'future' else b'layout=2\nextra\n')
  543          elif kind == 'record':
  544              self.on('a', "printf '{invalid' > /storage/.config/cloud-layout-migration.json")
  545          elif kind == 'config':
  546              self.on('a', "printf 'export SETTINGS_REMOTE=bad\\n' >> " + CONF)
  547              expected = "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
  548          before = self.audit_snapshot()
  549          result = self.on('a', '/usr/bin/cloud_scan --folder', allowed=None)
  550          require(result.returncode != 0 and '>>> why ' + expected in result.stdout,
  551                  'application refusal lost its reason')
  552          require("COULDN'T FIND YOUR CLOUD FOLDER" not in result.stdout, 'false missing-folder reason')
  553          require(self.audit_snapshot() == before, 'refusal changed cloud/settings')
  554  
  555      def audit_discovery(self, kind):
  556          layouts = {
  557              'empty': ('/Mine', [], 'empty', ''),
  558              'unrelated': ('/Mine', ['Mine/Photos/witness.jpg'], 'empty', ''),
  559              'fallback': ('/Mine', ['Mine/Photos/witness.jpg', 'pixelelated/Content/ROMs/gb/A.gb'], 'found-elsewhere', '/pixelelated/Content'),
  560              'tiered': ('/Mine', ['Mine/ROMs/gb/A.gb'], 'ok', ''),
  561              'root-tiered': ('', ['ROMs/gb/A.gb'], 'ok', ''),
  562              'root-flat': ('', ['gb/A.gb'], 'ok', ''),
  563              'root-unrelated': ('', ['Photos/witness.jpg'], 'empty', ''),
  564              'stranded': ('/Mine', ['gb/A.gb'], 'stranded-at-root', '/'),
  565              'refused': ('/Mine', ['Mine/ROMs/gb/A.gb'], 'unreadable', None),
  566          }
  567          content, paths, state, found = layouts[kind]
  568          self.audit_current(content)
  569          for path in paths:
  570              self.put(path, b'game\n')
  571          if kind == 'refused':
  572              self.fault('lsf-path', self.remote + 'Mine')
  573          before = self.audit_snapshot()
  574          result = self.on('a', '/usr/bin/cloud_setup --content-location', allowed=None)
  575          facts = dict(x.split('=', 1) for x in result.stdout.splitlines() if '=' in x)
  576          require(facts.get('STATE') == state and (found is None or facts.get('FOUND') == found),
  577                  'content classification disagrees: ' + repr(facts))
  578          require((result.returncode != 0) == (kind == 'refused'), 'content listing refusal hidden')
  579          require(self.audit_snapshot() == before, 'classification changed state')
  580          if kind == 'refused':
  581              self.on('a', f'test -s {QA}/fired')
  582          if kind == 'stranded':
  583              self.on('a', '/usr/bin/cloud_setup --use-content-root')
  584              require(self.pointers()['CONTENT_REMOTE'] == '', 'root selection not retained')
  585          if kind in ('stranded', 'root-flat', 'root-tiered', 'tiered'):
  586              result = self.on('a', '/usr/bin/cloud_content_restore --scan')
  587              require(re.search(r'^gb\|5\|', result.stdout, re.M), 'supported game absent from next scan')
  588              require(self.hashes() == before['cloud'], 'selection or scan changed cloud bytes')
  589  
  590      def audit_inherited(self, stage):
  591          ref = '69e6039f8f'
  592          self.conf('/GAMES', '/GAMES/backup', '/GAMES/Content')
  593          payloads = {'GAMES/gb/A.srm': b'save\n', 'GAMES/backup/QA/settings.tar.gz': b'settings\n',
  594                      'GAMES/Content/ROMs/gb/A.gb': b'game\n'}
  595          for path, value in payloads.items():
  596              self.put(path, value)
  597          old = subprocess.check_output(['git', '-C', str(self.tree), 'show', ref + ':' + SOURCES + '/cloud_migrate_layout'])
  598          self.on('a', f'cat > {QA}/predecessor; chmod 755 {QA}/predecessor', data=old.decode())
  599          paths = {'backups': '/GAMES/backup', 'saves': '/GAMES', 'content': '/GAMES/Content'}
  600          if stage != 'complete':
  601              self.fault('copy', self.remote + paths[stage])
  602          result = self.on('a', f'{QA}/predecessor --apply', allowed=None)
  603          if stage != 'complete':
  604              require(result.returncode != 0, 'predecessor interruption did not fire')
  605              self.on('a', f'test -s {QA}/fired')
  606          self.on('a', 'test ! -e /storage/.config/cloud-layout-migration.json')
  607          save(self.logs / (self.case + '-predecessor.json'), dict(ref=ref, sha256=hashlib.sha256(old).hexdigest(),
  608               rc=result.returncode, state=self.audit_snapshot()))
  609          self.clear_fault()
  610          self.migrate(allowed=(0, 3))
  611          for path, value in [('Saves/gb/A.srm', b'save\n'), ('Backups/QA/settings.tar.gz', b'settings\n'),
  612                              ('Content/ROMs/gb/A.gb', b'game\n')]:
  613              require((self.data / 'pixelelated' / path).read_bytes() == value, 'inherited payload lost: ' + path)
  614          require((self.data / 'pixelelated/.layout').read_bytes() == b'layout=2\n', 'inherited move did not settle')
  615          before = self.audit_snapshot()
  616          self.migrate(allowed=(0, 3))
  617          require(self.audit_snapshot() == before, 'inherited repeat changed state')
  618  
  619      def run_cases(self):
  620          cases = [('layout1-to2', lambda: self.migration_case())]
  621          for op, stages in [('copy', ['Backups', 'Saves', 'Saves-replaced', 'Content']),
  622                             ('delete', ['Backups', 'Saves', 'Saves-replaced', 'Content']), ('rcat', ['marker'])]:
  623              for stage in stages:
  624                  cases.append((f'pair-{op}-{stage}', lambda o=op, s=stage: self.migration_case((o, s))))
  625          for mode in ['--follow', '--settle']:
  626              for root, custom in [('/ROCKNIX', False), ('/GAMES', False), ('/ROCKNIX', True)]:
  627                  cases.append((f'T20-{mode[2:]}-{root[1:]}-{custom}', lambda m=mode, r=root, c=custom: self.backup_choice(m, r, c)))
  628          for mode in ['--join', '--follow', '--settle', '--apply']:
  629              for label, choice in [('missing', None), ('root', ''), ('derived', '/ROCKNIX/Content'), ('custom', '/Mine/ROMs')]:
  630                  cases.append((f'T21-{mode[2:]}-{label}', lambda m=mode, c=choice: self.content_choice(m, c)))
  631          for root in ['/GAMES', '/ROCKNIX/Saves']:
  632              cases.append(('T22-' + root.replace('/', '_'), lambda r=root: self.two_roots(r)))
  633          cases += [('T23-content-collision', self.collision), ('T25-restricted-parent', self.restricted)]
  634          for kind in ['empty', 'unrelated', 'fallback', 'tiered', 'root-tiered', 'root-flat', 'root-unrelated', 'stranded', 'refused']:
  635              cases.append(('PL001-discovery-' + kind, lambda k=kind: self.audit_discovery(k)))
  636          for mode in ['--join', '--follow', '--settle']:
  637              for boundary in ['SAVES_REMOTE', 'SETTINGS_REMOTE', 'CONTENT_REMOTE', 'publish']:
  638                  cases.append((f'PL002-{mode[2:]}-{boundary}', lambda m=mode, b=boundary: self.audit_atomic(m, b)))
  639          for label, content in [('root', ''), ('custom', '/Mine/Content'), ('current', '/pixelelated/Content')]:
  640              cases.append(('PL003-kept-sibling-' + label, lambda c=content: self.audit_sibling(c)))
  641          for stage in ['backups', 'saves', 'content', 'complete']:
  642              cases.append(('PL003-inherited-RC2-' + stage, lambda s=stage: self.audit_inherited(s)))
  643          for kind in ['comments', 'format', 'token', 'endpoint', 'legacy']:
  644              cases.append(('PL004-binding-' + kind, lambda k=kind: self.audit_binding(k)))
  645          for kind in ['future', 'malformed', 'config', 'record']:
  646              cases.append(('PL005-reason-' + kind, lambda k=kind: self.audit_reason(k)))
  647          for folder in ['MyGames', 'My Games', 'Games..old', "Kid's Games"]:
  648              cases.append(('PL006-chooser-' + folder, lambda f=folder: self.audit_chooser(f)))
  649          for kind in ['escaped', 'single', 'bare', 'double', 'duplicate', 'export', 'trailing', 'control']:
  650              cases.append(('PL008-reader-' + kind, lambda k=kind: self.audit_reader(k)))
  651          if self.args.case:
  652              cases = [(name, action) for name, action in cases if self.args.case in name]
  653          require(cases, 'no cases match the requested scope')
  654          for name, action in cases:
  655              self.case = name
  656              print('START ' + name, flush=True)
  657              try:
  658                  self.reset()
  659                  action()
  660                  save(self.logs / (name + '-final.json'), {'cloud': self.hashes(), 'a': self.pointers(), 'b': self.pointers('b')})
  661                  self.results.append({'case': name, 'status': 'PASS'})
  662                  print('PASS ' + name, flush=True)
  663              except (AssertionError, subprocess.SubprocessError, OSError, StopIteration) as error:
  664                  self.results.append({'case': name, 'status': 'FAIL', 'reason': str(error)})
  665                  print('FAIL ' + name + ': ' + str(error), flush=True)
  666              save(self.logs / 'results.json', self.results)
  667          self.case = 'final-custody'
  668          for key, value in self.original_scripts.items():
  669              guest, script = key.split('/')
  670              require(self.on(guest, 'sha256sum /usr/bin/' + script).stdout.split()[0] == value,
  671                      'installed script changed during proof')
  672          return 0 if all(x['status'] == 'PASS' for x in self.results) else 1
  673  
  674      def cleanup(self):
  675          # Stop only processes whose argv carries a disk beneath this fresh owner.
  676          stopped = []
  677          for p in Path('/proc').glob('[0-9]*/cmdline'):
  678              try:
  679                  argv = p.read_bytes().split(b'\0')
  680              except (FileNotFoundError, ProcessLookupError):
  681                  continue
  682              if Path(argv[0].decode()).name.startswith('qemu-system-') and any(str(self.pair).encode() in x for x in argv):
  683                  pid = int(p.parent.name)
  684                  os.kill(pid, signal.SIGTERM)
  685                  stopped.append(pid)
  686          for _ in range(100):
  687              if all(not Path('/proc', str(pid)).exists() for pid in stopped):
  688                  break
  689              time.sleep(.1)
  690          require(all(not Path('/proc', str(pid)).exists() for pid in stopped), 'owned guest failed to exit')
  691          if self.backend_started:
  692              self.local('cloud-test-backend', 'down')
  693          save(self.owner / 'cleanup.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  694                                          'qemu_pids': stopped, 'all_absent': True})
  695  
  696  
  697  def main():
  698      p = argparse.ArgumentParser(description=__doc__)
  699      p.add_argument('--tree', type=Path)
  700      p.add_argument('--image', type=Path)
  701      p.add_argument('--build-id')
  702      p.add_argument('--output', type=Path)
  703      p.add_argument('--case', help='run only cases containing this text; still owns a fresh pair')
  704      p.add_argument('--inject-failure', action='store_true')
  705      args = p.parse_args()
  706      if args.inject_failure:
  707          require(False, 'constructed failing assertion: expected exit1')
  708      require(all([args.tree, args.image, args.build_id, args.output]), 'tree, image, build-id and output required')
  709      require((args.tree / SOURCES / 'cloud_migrate_layout').is_file(),
  710              'migration suite retired by #508; use a historical source checkout and firmware')
  711      proof = Proof(args)
  712      try:
  713          proof.start()
  714          return proof.run_cases()
  715      finally:
  716          proof.cleanup()
  717  
  718  
  719  if __name__ == '__main__':
  720      try:
  721          sys.exit(main())
  722      except (AssertionError, OSError, subprocess.SubprocessError, StopIteration) as error:
  723          print('FAIL: ' + str(error), file=sys.stderr, flush=True)
  724          sys.exit(1)
```

## File: tools/rasteratops-vm-cloud-epic (at 8ebaf8daad, 402 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
    4  # The cloud epic's guest-d proof, promoted from run101 (#365).
    5  # Requires an isolated GENERIC_X64 guest d and the synthetic WebDAV backend.
    6  # Usage: tools/rasteratops-vm-cloud-epic --output DIR [--case CASE]
    7  # Cases: A B C D E F G H I J K L T08 T11 T12 T17 T19 T23 T26
    8  # --inject-failure exercises the exact assertion/exit path without a guest.
    9  set -uo pipefail
   10  R=$(cd "$(dirname "$0")/.." && pwd)
   11  P=""; requested="H A C D B E I J K L F G T08 T11 T12 T17 T19 T23 T26"; injected=0
   12  while [ $# -gt 0 ]; do
   13   case "$1" in
   14    --output) P="$2"; shift 2;; --case) requested="$2"; shift 2;;
   15    --inject-failure) injected=1; shift;;
   16    --help) sed -n '4,8p' "$0"; exit 0;;
   17    *) echo "unknown argument: $1" >&2; exit 2;;
   18   esac
   19  done
   20  # Historical migration proof only (D-CLOUD-175/#508). Refuse before
   21  # creating guests, changing their state or resetting a synthetic backend.
   22  if [ "$injected" != 1 ] && [ ! -f "${R}/projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout" ]; then
   23    echo 'This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manual cloud setup.' >&2
   24    exit 2
   25  fi
   26  [ -n "$P" ] || { echo '--output DIR is required' >&2; exit 2; }
   27  mkdir -p "$P/logs" "$P/frames"; P=$(cd "$P" && pwd)
   28  PASSES=0; FAILS=0; ITEM=cloud-epic; LOG="$P/logs/run.log"; FR="$P/frames"
   29  say() { printf '%s %s\n' "$(date -u +%T)" "$*" | tee -a "$LOG"; }
   30  check() { if [ "$1" = 0 ]; then say "PASS $2"; PASSES=$((PASSES+1)); else say "FAIL $2"; FAILS=$((FAILS+1)); fi; }
   31  done_line() { say "done: $PASSES PASS, $FAILS FAIL"; }
   32  if [ "$injected" = 1 ]; then check 1 'constructed assertion failure'; done_line; [ "$FAILS" -eq 0 ]; exit $?; fi
   33  # Every letter is a separate process and fresh fixture, so ordering cannot rescue a case.
   34  if [ -z "${PROOF_CASE:-}" ]; then
   35   total_rc=0
   36   for letter in $requested; do
   37    case "$letter" in A|B|C|D|E|F|G|H|I|J|K|L|T08|T11|T12|T17|T19|T23|T26) ;; *) echo "unknown case $letter" >&2; exit 2;; esac
   38    PROOF_CASE="$letter" "$0" --output "$P/$letter" --case "$letter" || total_rc=1
   39   done
   40   exit "$total_rc"
   41  fi
   42  CASES="$PROOF_CASE"
   43  PORT=10026; MON=/tmp/rocknix-qemu-monitor-d.sock; VNC=127.0.0.1:5912
   44  KEY="${VM_PAIR_DIR:-/tmp/rocknix-vm-pair}/qa-key"
   45  VQ="$R/tools/vm-visual-qa"
   46  DATA="${CLOUD_QA_STATE:-$HOME/.cache/rocknix-cloud-qa}/data"
   47  # The runner has no hostname flag: all writes are confined to guest d and the local QA backend.
   48  [ -S "$MON" ] && [ -s /tmp/rocknix-qemu-d.pid ] && [ -f "$KEY" ] || { say 'guest d prerequisites absent'; exit 2; }
   49  qa_pid=$(cat /tmp/rocknix-qemu-d.pid)
   50  [[ "$qa_pid" =~ ^[0-9]+$ ]] && [ -r "/proc/$qa_pid/cmdline" ] && tr '\0' '\n' < "/proc/$qa_pid/cmdline" | grep -q 'qemu-system-x86_64' || { say 'guest pidfile is not a QEMU process'; exit 2; }
   51  [ "${CLOUD_QA_BACKEND:-webdav}" = webdav ] && [ -d "$DATA" ] && [ ! -L "$DATA" ] || { say 'requires isolated WebDAV QA data'; exit 2; }
   52  GRABPID=""
   53  cleanup() {
   54   [ -z "$GRABPID" ] || { kill "$GRABPID" 2>/dev/null || :; wait "$GRABPID" 2>/dev/null || :; }
   55   if declare -F protocol_cleanup >/dev/null; then protocol_cleanup; fi
   56  }
   57  trap cleanup EXIT INT TERM
   58  walk() {
   59   local rc
   60   "$VQ" --monitor "$MON" run "$1" --outdir "$2" >> "$LOG" 2>&1; rc=$?
   61   check "$rc" "walk $(basename "$1")"
   62   [ "$rc" -eq 0 ] || { done_line; exit 1; }
   63  }
   64  settle() { "$VQ" --monitor "$MON" settle >> "$LOG" 2>&1; }
   65  grab_start() {
   66   mkdir -p "$FR/$1"; rm -f "$FR/$1.stop"
   67   python3 "$R/tools/vm-walks/cloud-epic/vnc-grab.py" "$VNC" "$FR/$1" "$1" "$FR/$1.stop" "${2:-0.7}" > "$FR/$1.capture.log" 2>&1 &
   68   GRABPID=$!; printf '%s\n' "$GRABPID" > "$FR/$1.capture.pid"
   69  }
   70  grab_stop() { touch "$FR/$1.stop"; [ -z "$GRABPID" ] || wait "$GRABPID"; GRABPID=""; }
   71  wait_card() {
   72   local i n
   73   for i in $(seq 1 60); do
   74    n=$(G_ "pgrep -f 'cloud_backu[p]|cloud_restor[e]|rclon[e] ' | wc -l") || return 1
   75    [ "$n" = 0 ] && break; sleep 1
   76   done
   77   sleep "${1:-6}"
   78  }
   79  
   80  mask() { grep -v -i -E 'key|pass|token|user|psk'; }                                   # config dumps
   81  maskl() { sed -E 's/((token|key|passw[a-z]*|psk|user|[?&]u|[?&]t|[?&]p)[=:])[^ &]*/\1***/Ig'; }   # the value masked, the key kept
   82  MONC() { printf '%s\n' "$1" | socat -t 1 - "UNIX-CONNECT:$MON" >/dev/null 2>&1; }
   83  G_() { ssh -n -i $KEY -p $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes -o ConnectTimeout=8 root@127.0.0.1 "$@"; }
   84  require_no_game() { G_ "! pgrep -f 'retroarc[h] -L' >/dev/null"; }
   85  boot_id() { G_ 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null; }
   86  reboot_guest() { local b0; b0=$(boot_id); G_ 'sync; reboot' >/dev/null 2>&1; sleep 20
   87    local i; for i in $(seq 1 60); do [ -n "$(boot_id)" ] && [ "$(boot_id)" != "$b0" ] && break; sleep 3; done
   88    [ "$(boot_id)" != "$b0" ] || { say "  reboot: boot id did not change"; return 1; }
   89    for i in $(seq 1 40); do G_ 'pgrep -x emulationstation >/dev/null && curl -s -o /dev/null -m 3 http://127.0.0.1:1234/caps' 2>/dev/null && break; sleep 3; done
   90    sleep 15; require_no_game
   91    # and the boot's own work done before a script walks: the hasher and the top-up (/isIdle), the startup sync's card
   92    # (wait_card), a still screen (settle) -- run 5's E2-pl062 pressed START into a fading card, E2-pl068 walked a page
   93    # that was still loading, E2-pl061 launched under the hasher (D-QA-057, blindspot 64)
   94    local j idle=no; for j in $(seq 1 120); do [ "$(G_ "curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1:1234/isIdle")" = 200 ] && { idle=yes; break; }; sleep 1; done
   95    echo "$(date +%T)   reboot_guest: /isIdle $idle after ${j}s" >> "$LOG"; wait_card 3; settle; sleep 3; }
   96  debug_reboot() { G_ 'systemctl stop essway; f=/storage/.config/emulationstation/es_settings.cfg; if grep -q "name=\"Debug\"" $f; then sed -i "s|<bool name=\"Debug\" value=\"[a-z]*\" />|<bool name=\"Debug\" value=\"true\" />|" $f; else sed -i "s|</config>|  <bool name=\"Debug\" value=\"true\" />\n</config>|" $f; fi; grep -c "name=\"Debug\" value=\"true\"" $f; sync' >/dev/null 2>&1; reboot_guest; }
   97  CONF=/storage/.config/cloud_sync.conf; LABEL=GENERIC-X64
   98  say "=== $ITEM on guest d, $(G_ 'grep -h ^BUILD_ID /etc/os-release; grep -c . /usr/bin/cloud_scan 2>/dev/null')"
   99  conf() { G_ "sed -i -e 's|^SAVES_REMOTE=.*|SAVES_REMOTE=\"$1\"|' -e 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE=\"$2\"|' -e 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE=\"$3\"|' -e 's|^LAYOUT_KEEP=.*|LAYOUT_KEEP=\"\"|' $CONF; rm -rf /storage/.cache/cloud_sync/scan; grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=|^LAYOUT_KEEP=' $CONF | tr '\n' ' '"; }
  100  # the walk to the hub: MAIN MENU opens on GAME SETTINGS, or on RETROACHIEVEMENTS when the guest is signed in (one down
  101  # first, guest-facts-that-break-proofs), then RESTORE or BACK UP, the scan page framed twice while it runs, then whatever
  102  # follows it
  103  RA_DOWN=$(G_ '. /etc/profile >/dev/null 2>&1; [ "$(get_setting global.retroachievements)" = 1 ] && printf "key down\nwait-for-change\n"')
  104  to_page() { # <restore|backup> <tag>
  105    local f=$P/epic-$2.steps
  106    { printf 'wake\ndismiss-dialogs\nkey ret\nwait-for-change\nsettle\n%skey x\nwait-for-change\nsettle\nkey up\nwait-for-change\nkey up\nwait-for-change\nkey up\nwait-for-change\nsettle\nkey x\nwait-for-change\nsettle\nshot %s-hub\n' "$RA_DOWN" "$2"
  107      [ "$1" = restore ] && printf 'key down\nwait-for-change\n'
  108      printf 'key x\nwait-for-change\nshot %s-scan-0\nwait 1.5\nshot %s-scan-1\nsettle 90 3\nshot %s-after-scan\n' "$2" "$2" "$2"; } > "$f"
  109    walk "$f" "$FR"
  110  }
  111  steps() { local f=$P/epic-$1.steps; shift; printf '%s\n' "$@" | sed '/^$/d' > "$f"; walk "$f" "$FR"; }
  112  host_tree() { (cd "$DATA" && find . -type f | sort | sed 's|^\./||' | tr '\n' ' '); }
  113  
  114  # CASES is one independently reset case.
  115  # The systems page remembers the picks (cloudsync.pick.restore.*), so a walk that ticks ROMS AND BIOS leaves it on
  116  # for the next; written with the interface stopped (it writes its settings back as it stops), then started again
  117  reset_picks() {
  118    G_ "systemctl stop essway; sleep 2; . /etc/profile >/dev/null 2>&1; for k in content media settings; do set_setting cloudsync.pick.restore.\$k 0; done; set_setting cloudsync.pick.restore.saves 1" >/dev/null 2>&1
  119    G_ 'systemctl start essway' >/dev/null 2>&1; sleep 25; require_no_game >/dev/null 2>&1; say "  picks reset: $(G_ '. /etc/profile >/dev/null 2>&1; echo content=$(get_setting cloudsync.pick.restore.content) saves=$(get_setting cloudsync.pick.restore.saves)')"; }
  120  want() { case " $CASES " in *" $1 "*) return 0;; esac; return 1; }
  121  # the interface's Info lines need Debug=true at that boot (debug_reboot); read before the next reboot wipes them
  122  esl() { G_ "grep -a -E \"$1\" /var/log/es_log.txt 2>/dev/null" | maskl; }
  123  # a boot with the step's frames: Debug set, the reboot, frames over VNC through the boot and the waiter's wait
  124  boot_frames() { # <tag> <seconds after the guest is idle>
  125    grab_start "$1" 0.7; debug_reboot; sleep "$2"; grab_stop "$1"; require_no_game >/dev/null 2>&1
  126    say "  $1: $(ls "$FR/$1" 2>/dev/null | wc -l) frames under $FR/$1"; }
  127  G_ 'systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; rm -f /storage/.config/.restore-finish-pending /storage/.config/cloud-layout-migration.json; rm -rf /storage/.cache/cloud_sync/scan; find /storage/roms -type f -name "*.srm" -delete' >/dev/null || exit 2
  128  say "== setup: the QA remote on the guest (the host backend's conf), then the QA cloud holds the fork's earlier layout with files in every folder of ours; the guest points at it"
  129  "$R/tools/cloud-test-backend" rclone-conf > $P/epic-rclone.conf && scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR $P/epic-rclone.conf root@127.0.0.1:/tmp/rclone.conf; rm -f $P/epic-rclone.conf
  130  G_ 'mkdir -p /storage/.config/rclone && mv /tmp/rclone.conf /storage/.config/rclone/rclone.conf && chmod 600 /storage/.config/rclone/rclone.conf && /usr/bin/cloud_sync_helper >/dev/null 2>&1; if test -f /usr/bin/cloud_connections.py; then name=$(rclone listremotes | head -1); cloud_remote select "${name%:}"; echo "remote: $(cloud_remote active)"; else echo "remote: $(rclone listremotes | head -1)"; fi' | tee -a "$LOG"
  131  "$R/tools/cloud-test-backend" reset >/dev/null || exit 2; mkdir -p "$DATA/ROCKNIX/Saves/nes" "$DATA/ROCKNIX/Backups" "$DATA/ROCKNIX/Content/ROMs/nes" "$DATA/ROCKNIX/Content/BIOS" "$DATA/ROCKNIX/Saves-replaced/nes"
  132  head -c 4000 /dev/urandom > "$DATA/ROCKNIX/Saves/nes/Probe.srm"; head -c 3000 /dev/urandom > "$DATA/ROCKNIX/Saves-replaced/nes/Probe.srm.1"
  133  head -c 9000 /dev/urandom > "$DATA/ROCKNIX/Content/ROMs/nes/Probe.nes"; head -c 500 /dev/urandom > "$DATA/ROCKNIX/Content/BIOS/disksys.rom"
  134  tar -czf "$DATA/ROCKNIX/Backups/2026_09_30-120000-$LABEL-ROCKNIX_SETTINGS.tar.gz" -C /tmp --files-from /dev/null 2>/dev/null || : > "$DATA/ROCKNIX/Backups/2026_09_30-120000-$LABEL-ROCKNIX_SETTINGS.tar.gz"
  135  : > "$DATA/ROCKNIX/Backups/2026_09_29-090000-Retroid-Pocket-Nova-ROCKNIX_SETTINGS.tar.gz"
  136  say "  cloud: $(host_tree)"
  137  say "  guest conf: $(conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)"
  138  G_ '. /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; /usr/bin/cloud_sync_helper >/dev/null 2>&1; echo "label=$(/usr/bin/cloud_device_id --label)"' | tee -a "$LOG"
  139  
  140  # The former chain assumed A had moved the cloud and B had left a held copy.
  141  # Each case now constructs exactly that initial state itself.
  142  case "$PROOF_CASE" in
  143   A|H) ;;
  144   *) mv "$DATA/ROCKNIX" "$DATA/pixelelated"; conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content >/dev/null;;
  145  esac
  146  if [ "$PROOF_CASE" = E ]; then cp -a "$DATA/pixelelated" "$DATA/_pixelelated_hold"; fi
  147  case "$PROOF_CASE" in
  148   T17|T19|T23|T26)
  149    . "$R/tools/vm-walks/cloud-epic/migration-protocol.sh"
  150    protocol_main "$PROOF_CASE"
  151    done_line; [ "$FAILS" -eq 0 ]; exit $?;;
  152  esac
  153  reset_picks
  154  G_ 'systemctl stop essway; rm -f /storage/.config/.restore-finish-pending; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; systemctl start essway' >/dev/null || exit 2
  155  sleep 20
  156  
  157  case "$PROOF_CASE" in
  158   T08|T11|T12)
  159    "$R/tools/cloud-test-backend" reset >/dev/null || exit 2
  160    if [ "$PROOF_CASE" = T11 ]; then
  161     mkdir -p "$DATA/GAMES" "$DATA/ROCKNIX/Saves/nes"
  162     printf 'earlier saves sentinel\n' > "$DATA/ROCKNIX/Saves/nes/Boot.srm"
  163     conf /GAMES /GAMES/backup '' >/dev/null
  164     expected=/ROCKNIX/Saves
  165    else
  166     conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content >/dev/null
  167     expected=/ROCKNIX/Saves
  168     if [ "$PROOF_CASE" = T12 ]; then
  169      mkdir -p "$DATA/pixelelated/Saves/nes"
  170      printf 'fleet saves sentinel\n' > "$DATA/pixelelated/Saves/nes/Boot.srm"
  171      printf 'layout=2\n' > "$DATA/pixelelated/.layout"
  172      expected=/pixelelated/Saves
  173     fi
  174    fi
  175    G_ 'mkdir -p /storage/roms/nes; printf "local backup sentinel\n" > /storage/roms/nes/Local.srm; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 1' >/dev/null || exit 2
  176    boot_frames "$PROOF_CASE-boot" 35
  177    G_ "grep -qx 'SAVES_REMOTE=\"$expected\"' $CONF"; check $? "$PROOF_CASE: boot scan points at $expected"
  178    if [ "$PROOF_CASE" = T11 ]; then
  179     [ ! -e "$DATA/GAMES/nes/Local.srm" ]; check $? 'T11: startup did not populate the empty old root before joining'
  180     [ "$(cat "$DATA/ROCKNIX/Saves/nes/Boot.srm")" = 'earlier saves sentinel' ]; check $? 'T11: earlier save bytes preserved'
  181    elif [ "$PROOF_CASE" = T12 ]; then
  182     [ "$(cat "$DATA/pixelelated/Saves/nes/Boot.srm")" = 'fleet saves sentinel' ]; check $? 'T12: fleet save bytes preserved'
  183     [ ! -e "$DATA/ROCKNIX/Saves/nes/Local.srm" ]; check $? 'T12: startup did not recreate the abandoned old root'
  184    else
  185     [ ! -e "$DATA/ROCKNIX" ]; check $? 'T08: startup did not recreate an absent old parent'
  186     esl 'offering to create it' | grep -q .; check $? 'T08: the setup step offers recovery after startup'
  187    fi
  188    done_line; [ "$FAILS" -eq 0 ]; exit $?;;
  189  esac
  190  
  191  if want H; then
  192  say "== H: a fresh device (on the current default) whose cloud holds its saves only under /ROCKNIX: the scan joins that folder and the move dialog names it (D-CLOUD-169)"
  193  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content)"
  194  to_page restore H
  195  say "  guest conf after the scan: $(G_ "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' $CONF | tr '\n' ' '")"
  196  G_ "grep -q '^SAVES_REMOTE=\"/ROCKNIX/Saves\"' $CONF && grep -q '^SETTINGS_REMOTE=\"/ROCKNIX/Backups\"' $CONF && grep -q '^CONTENT_REMOTE=\"/ROCKNIX/Content\"' $CONF"; check $? "H: the scan joined the folder the saves are in"
  197  [ ! -e "$DATA/pixelelated" ]; check $? "H: nothing was made at /pixelelated beside them"
  198  G_ 'journalctl -b -o short-iso -t cloud_migrate_layout -t cloud_scan 2>/dev/null | grep -i join | tail -3' | maskl | tee -a "$LOG"
  199  G_ 'journalctl -b -o short-iso -t cloud_migrate_layout 2>/dev/null | grep -q "joined the fleet at /ROCKNIX/Saves"'; check $? "H: the journal names the join"
  200  # B on the dialog is its last button, NOT NOW; the options page follows it
  201  steps H2 'key z' 'wait-for-change' 'settle' 'shot H-after-not-now' 'dismiss-dialogs'
  202  say "  guest conf after NOT NOW: $(G_ "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=' $CONF | tr '\n' ' '")"
  203  fi
  204  
  205  if want A; then
  206  say "== A: RESTORE FROM THE CLOUD opens on the scan page; an earlier /ROCKNIX with saves gets the move dialog; MOVE runs the move page"
  207  to_page restore A
  208  steps A2 'key x' 'wait-for-change' 'wait 2' 'shot A-move-running' 'settle 180 3' 'shot A-move-done' 'key x' 'wait-for-change' 'shot A-rescan' 'settle 90 3' 'shot A-options-after-move' 'dismiss-dialogs'
  209  say "  cloud after the move: $(host_tree)"
  210  say "  marker: $(cat "$DATA/pixelelated/.layout" 2>/dev/null || echo none)"
  211  say "  guest conf: $(G_ "grep -E '^(SAVES|SETTINGS|CONTENT)_REMOTE=|^LAYOUT_KEEP=' $CONF | tr '\n' ' '")"
  212  [ -f "$DATA/pixelelated/Saves/nes/Probe.srm" ] && [ -f "$DATA/pixelelated/Backups/2026_09_30-120000-$LABEL-ROCKNIX_SETTINGS.tar.gz" ] && [ -f "$DATA/pixelelated/Content/ROMs/nes/Probe.nes" ] && [ -f "$DATA/pixelelated/Saves-replaced/nes/Probe.srm.1" ]; check $? "A: the four folders of ours are under /pixelelated after MOVE (saves, settings backup, content, the set-aside)"
  213  [ ! -f "$DATA/ROCKNIX/Saves/nes/Probe.srm" ] && [ ! -f "$DATA/ROCKNIX/Saves-replaced/nes/Probe.srm.1" ]; check $? "A: nothing of ours remains under /ROCKNIX"
  214  [ "$(cat "$DATA/pixelelated/.layout" 2>/dev/null)" = "layout=2" ]; check $? "A: the layout marker is written"
  215  G_ "grep -q '^SAVES_REMOTE=\"/pixelelated/Saves\"' $CONF"; check $? "A: the guest now points at /pixelelated/Saves"
  216  G_ 'journalctl -b -o short-iso -t cloud_migrate_layout -t cloud_scan 2>/dev/null | tail -8' | maskl | tee -a "$LOG"
  217  fi
  218  
  219  if want C; then
  220  say "== C: the SETTINGS row by device label: offered with the device and date after the move (above); dimmed with only a foreign archive"
  221  rm -f "$DATA/pixelelated/Backups/2026_09_30-120000-$LABEL-ROCKNIX_SETTINGS.tar.gz"
  222  to_page restore C
  223  G_ "grep -qx 'MINE=' /storage/.cache/cloud_sync/scan/settings && test -s /storage/.cache/cloud_sync/scan/done"; check $? 'C: foreign-only scan disables settings with a completed scan'
  224  steps C2 'dismiss-dialogs'
  225  fi
  226  
  227  if want D; then
  228  say "== D: the content folder: nothing of ours at the configured root and nothing found -> the question and the chooser; found elsewhere -> used, then the content scan"
  229  mkdir -p "$DATA/Photos" "$DATA/Documents"; head -c 100 /dev/urandom > "$DATA/Photos/holiday.jpg"; : > "$DATA/Documents/notes.txt"
  230  mv "$DATA/pixelelated/Content" "$DATA/_content_hold"; mkdir -p "$DATA/pixelelated/Content"
  231  reset_picks
  232  to_page restore D
  233  # tick ROMS AND BIOS (row 2), then CONTINUE: up to SAVES, up to BACK, right to CONTINUE
  234  steps D2 'key down' 'wait-for-change' 'key x' 'wait-for-change 12 0' 'settle' 'shot D-roms-ticked' 'key up' 'wait-for-change' 'key up' 'wait-for-change' 'key right' 'wait-for-change' 'settle' 'shot D-continue' 'key x' 'wait-for-change' 'settle 30 2' 'shot D-question' 'key x' 'wait-for-change' 'settle' 'shot D-chooser' 'key z' 'wait-for-change' 'settle' 'dismiss-dialogs'
  235  rm -rf "$DATA/pixelelated/Content"; mv "$DATA/_content_hold" "$DATA/pixelelated/Content"
  236  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /Elsewhere)"
  237  reset_picks
  238  to_page restore D3
  239  steps D4 'key down' 'wait-for-change' 'key x' 'wait-for-change 12 0' 'settle' 'key up' 'wait-for-change' 'key up' 'wait-for-change' 'key right' 'wait-for-change' 'settle' 'key x' 'wait-for-change' 'shot D-content-scan-0' 'wait 1.5' 'shot D-content-scan-1' 'settle 90 3' 'shot D-systems' 'dismiss-dialogs'
  240  G_ "grep -E '^CONTENT_REMOTE=' $CONF"; G_ "grep -q '^CONTENT_REMOTE=\"/pixelelated/Content\"' $CONF"; check $? "D: the content root found under the cloud root was used without a question"
  241  fi
  242  
  243  if want B; then
  244  say "== B0: a carried /GAMES that holds saves and no current folder -> the move dialog names /GAMES; NOT NOW"
  245  mv "$DATA/pixelelated" "$DATA/_pixelelated_hold"
  246  mkdir -p "$DATA/GAMES/nes"; head -c 3000 /dev/urandom > "$DATA/GAMES/nes/Stock.srm"
  247  say "  guest conf: $(conf /GAMES /GAMES/backup '')"
  248  to_page restore B0
  249  steps B0b 'shot B0-move-question' 'key z' 'wait-for-change' 'settle' 'dismiss-dialogs'
  250  G_ "grep -q '^SAVES_REMOTE=\"/GAMES\"' $CONF"; check $? "B0: NOT NOW on the /GAMES move left the conf on /GAMES"
  251  rm -rf "$DATA/GAMES"
  252  say "== B: a carried /GAMES and no current folder -> the offer to create; CREATE IT re-points and seeds"
  253  say "  guest conf: $(conf /GAMES /GAMES/backup '')"
  254  to_page restore B
  255  steps B2 'key x' 'wait-for-change' 'wait 1' 'shot B-create-running' 'settle 120 3' 'shot B-rescan' 'settle 90 3' 'shot B-options-after-create' 'dismiss-dialogs'
  256  say "  cloud after CREATE IT: $(host_tree)"
  257  [ -d "$DATA/pixelelated/Saves" ] && [ -d "$DATA/pixelelated/Backups" ] && [ -d "$DATA/ROMs" ] && [ -d "$DATA/BIOS" ] && [ ! -e "$DATA/pixelelated/Content" ]; check $? "B: CREATE IT makes saves/backups and preserves the explicit cloud content root"
  258  G_ "grep -q '^SAVES_REMOTE=\"/pixelelated/Saves\"' $CONF && grep -q '^SETTINGS_REMOTE=\"/pixelelated/Backups\"' $CONF"; check $? "B: the carried /GAMES setting is re-pointed at the current layout"
  259  fi
  260  
  261  if want E; then
  262  say "== E: the startup sync with no saves folder in the cloud: the card says SKIPPED with the row to set it up; then the cloud folder step offers CREATE IT (D-CLOUD-170)"
  263  rm -rf "$DATA/pixelelated"
  264  # The boot with a stock-shaped conf, as a device updated from stock ROCKNIX carries it (/GAMES, a value nobody typed;
  265  # a substitute for that update, named: the conf is written here, not carried): the card's skip, then the step once
  266  # the card is done, nothing re-pointed until the player answers (D-CLOUD-166 for the card, D-CLOUD-170 for the step)
  267  say "  guest conf: $(conf /GAMES /GAMES/backup '')"
  268  G_ '. /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 1; echo startup=$(get_setting cloudsaves.startup)' | tee -a "$LOG"
  269  boot_frames E-boot 45
  270  G_ 'cat /storage/.cache/cloud_sync/last-sync-startup 2>/dev/null' | maskl | tee -a "$LOG"
  271  G_ 'grep -q " 78 no-folder" /storage/.cache/cloud_sync/last-sync-startup'; check $? "E: the startup stamp carries the third sentinel (78 no-folder)"
  272  esl 'cloud folder step|cloud folder:' | tail -4 | tee -a "$LOG"
  273  esl 'cloud folder step: checking the folder \(boot\)' | grep -q .; check $? "E: the step came up at boot once the card was done"
  274  esl 'offering to create it' | grep -q .; check $? "E: and offered CREATE IT for the carried /GAMES with nothing anywhere"
  275  steps E2 'shot E-step-offer' 'key z' 'wait-for-change' 'settle' 'shot E-after-not-now' 'dismiss-dialogs'
  276  G_ "grep -q '^SAVES_REMOTE=\"/GAMES\"' $CONF"; check $? "E: NOT NOW re-pointed nothing: the stock-shaped conf still names /GAMES"
  277  [ ! -e "$DATA/GAMES" ]; check $? "E: and the boot's startup sync made no /GAMES in the cloud (D-CLOUD-172)" "the cloud holds: $(cd "$DATA" && find GAMES -type f 2>/dev/null | head -3 | tr '\n' ' ')"
  278  G_ '. /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0' >/dev/null 2>&1
  279  mv "$DATA/_pixelelated_hold" "$DATA/pixelelated"
  280  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content)"
  281  fi
  282  
  283  if want I; then
  284  say "== I: the boot step on a device still on /ROCKNIX with saves there: after the startup card, CHECKING YOUR CLOUD, then MOVE; NOT NOW asks again next boot; after MOVE nothing"
  285  mv "$DATA/pixelelated" "$DATA/_pixelelated_hold"; mkdir -p "$DATA/ROCKNIX/Saves/nes"; head -c 4000 /dev/urandom > "$DATA/ROCKNIX/Saves/nes/Boot.srm"
  286  say "  cloud: $(host_tree)"
  287  say "  guest conf: $(conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)"
  288  G_ '/usr/bin/cloud_migrate_layout --needs-step >/dev/null 2>&1; echo "needs-step rc=$?"' | tee -a "$LOG"
  289  G_ '. /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 1' >/dev/null 2>&1
  290  boot_frames I-boot1 40
  291  esl 'cloud folder step|cloud folder:|startup' | tail -6 | tee -a "$LOG"
  292  esl 'cloud folder step: checking the folder \(boot\)' | grep -q .; check $? "I: the step came up at boot"
  293  esl 'offering the move' | grep -q .; check $? "I: and asked the move for /ROCKNIX"
  294  steps I1 'shot I-move-question' 'key z' 'wait-for-change' 'settle' 'shot I-after-not-now' 'dismiss-dialogs'
  295  G_ "grep -q '^SAVES_REMOTE=\"/ROCKNIX/Saves\"' $CONF"; check $? "I: NOT NOW left the conf on /ROCKNIX"
  296  boot_frames I-boot2 40
  297  esl 'offering the move' | grep -q .; check $? "I: the next boot asked again"
  298  steps I2 'shot I-move-question-again' 'key x' 'wait-for-change' 'wait 2' 'shot I-move-running' 'settle 180 3' 'shot I-move-done' 'key x' 'wait-for-change' 'settle' 'shot I-after-move' 'dismiss-dialogs'
  299  say "  cloud after the move: $(host_tree)"
  300  [ -f "$DATA/pixelelated/Saves/nes/Boot.srm" ] && [ ! -f "$DATA/ROCKNIX/Saves/nes/Boot.srm" ]; check $? "I: MOVE at boot moved the saves to /pixelelated and left nothing under /ROCKNIX"
  301  G_ "grep -q '^SAVES_REMOTE=\"/pixelelated/Saves\"' $CONF"; check $? "I: the conf points at /pixelelated/Saves"
  302  esl 'cloud folder step: settled' | grep -q .; check $? "I: and the step's own check after the move reads it settled"
  303  boot_frames I-boot3 40
  304  esl 'nothing to settle' | grep -q . && ! esl 'cloud folder step: checking the folder' | grep -q .; check $? "I: the boot after the move raises nothing (--needs-step 1)"
  305  steps I3 'shot I-boot3-quiet' 'dismiss-dialogs'
  306  G_ '. /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0' >/dev/null 2>&1
  307  rm -rf "$DATA/pixelelated"; mv "$DATA/_pixelelated_hold" "$DATA/pixelelated"
  308  fi
  309  
  310  if want J; then
  311  say "== J: the boot step offline (the guest's link cut on the monitor): FINISH CLOUD SETUP / YOU'RE NOT ONLINE ... with CONNECT TO WI-FI and NOT NOW"
  312  say "  guest conf: $(conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)"
  313  G_ 'systemctl stop essway; f=/storage/.config/emulationstation/es_settings.cfg; if grep -q "name=\"Debug\"" $f; then sed -i "s|<bool name=\"Debug\" value=\"[a-z]*\" />|<bool name=\"Debug\" value=\"true\" />|" $f; else sed -i "s|</config>|  <bool name=\"Debug\" value=\"true\" />\n</config>|" $f; fi; sync' >/dev/null 2>&1
  314  grab_start J-boot 0.7
  315  G_ 'sync; reboot' >/dev/null 2>&1; MONC "set_link net0 off"; say "  link off at $(date -u +%H:%M:%S)"
  316  sleep 55; sleep 55; grab_stop J-boot
  317  steps J1 'shot J-offline' 'key z' 'wait-for-change' 'settle' 'shot J-after-not-now'
  318  MONC "set_link net0 on"; for i in $(seq 1 60); do G_ true 2>/dev/null && break; sleep 2; done; say "  link on; ssh back after ${i} tries"
  319  esl 'cloud folder step' | tail -4 | tee -a "$LOG"
  320  esl 'a folder to settle and no network; asking to connect' | grep -q .; check $? "J: offline, the step asked to connect"
  321  esl 'NOT NOW; asked again at the next boot' | grep -q .; check $? "J: and NOT NOW put it off to the next boot"
  322  require_no_game >/dev/null 2>&1; steps J2 'dismiss-dialogs'
  323  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content)"
  324  fi
  325  
  326  if want K; then
  327  say "== K: a settings restore's marker and an earlier folder at the same boot (the marker written here, a named stand-in): FINISH RESTORE PROCESS first; LATER brings neither; FINISH brings the step"
  328  mv "$DATA/pixelelated" "$DATA/_pixelelated_hold"; mkdir -p "$DATA/ROCKNIX/Saves/nes"; head -c 4000 /dev/urandom > "$DATA/ROCKNIX/Saves/nes/Restore.srm"
  329  say "  guest conf: $(conf /ROCKNIX/Saves /ROCKNIX/Backups /ROCKNIX/Content)"
  330  G_ 'echo 1 > /storage/.config/.restore-finish-pending; ls -la /storage/.config/.restore-finish-pending' | tee -a "$LOG"
  331  boot_frames K-boot1 40
  332  steps K1 'shot K-restore-page' 'key up' 'wait-for-change' 'settle' 'shot K-later-focused' 'key x' 'wait-for-change' 'settle' 'wait 20' 'settle' 'shot K-after-later'
  333  esl 'cloud folder step' | tail -3 | tee -a "$LOG"
  334  ! esl 'cloud folder step: checking the folder' | grep -q .; check $? "K: with the restore page up and then LATER, the step did not come at this boot"
  335  G_ 'test -e /storage/.config/.restore-finish-pending'; check $? "K: LATER kept the restore's marker"
  336  boot_frames K-boot2 40
  337  steps K2 'shot K-restore-page-again' 'key up' 'wait-for-change' 'key right' 'wait-for-change' 'settle' 'shot K-finish-focused' 'key x' 'wait-for-change' 'settle 60 3' 'shot K-after-finish'
  338  esl 'cloud folder step|restore relink' | tail -5 | tee -a "$LOG"
  339  esl 'cloud folder step: checking the folder \(boot\)' | grep -q .; check $? "K: FINISH brought the step"
  340  ! G_ 'test -e /storage/.config/.restore-finish-pending'; check $? "K: and FINISH consumed the restore's marker"
  341  steps K3 'shot K-step-question' 'key z' 'wait-for-change' 'settle' 'dismiss-dialogs'
  342  rm -rf "$DATA/ROCKNIX"; mv "$DATA/_pixelelated_hold" "$DATA/pixelelated"
  343  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content)"
  344  fi
  345  
  346  if want L; then
  347  say "== L: the end of cloud setup (the repair route: USE A COMPUTER INSTEAD, REPAIR A CONNECTION, the three steps, CONTINUE): the step asks MOVE before CLOUD SETUP COMPLETE"
  348  # a fresh install's shape: the conf on the current default, the cloud's saves only under /ROCKNIX -- the step's
  349  # scan joins them and asks the move, before the seeding and the last page (D-CLOUD-169, D-CLOUD-170)
  350  mv "$DATA/pixelelated" "$DATA/_pixelelated_hold"; mkdir -p "$DATA/ROCKNIX/Saves/nes"; head -c 4000 /dev/urandom > "$DATA/ROCKNIX/Saves/nes/Setup.srm"
  351  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content)"
  352  debug_reboot; require_no_game >/dev/null 2>&1
  353  # the hub, then eight downs to CONNECT OR REPAIR CLOUD STORAGE (one past CHANGE CLOUD FOLDER's seven)
  354  f=$P/epic-L.steps
  355  { printf 'wake\ndismiss-dialogs\nkey ret\nwait-for-change\nsettle\n%skey x\nwait-for-change\nsettle\nkey up\nwait-for-change\nkey up\nwait-for-change\nkey up\nwait-for-change\nsettle\nkey x\nwait-for-change\nsettle\nshot L-hub\n' "$RA_DOWN"
  356    for n in 1 2 3 4 5 6 7 8; do printf 'key down\nwait-for-change\n'; done
  357    printf 'settle\nshot L-connect-row\nkey x\nwait-for-change\nsettle\nshot L-provider-list\n'
  358    # USE A COMPUTER INSTEAD is the list's last row: up from the first row is the button bar, up again the last row
  359    printf 'key up\nwait-for-change\nkey up\nwait-for-change\nsettle\nshot L-use-computer-row\nkey x\nwait-for-change\nsettle\nshot L-setup-page\n'
  360    # REPAIR A CONNECTION is the setup page's last row
  361    printf 'key up\nwait-for-change\nkey up\nwait-for-change\nsettle\nshot L-repair-row\nkey x\nwait-for-change\nsettle\nshot L-step1\n'
  362    # each step's CONTINUE: up to the button bar, right to CONTINUE
  363    for st in 1 2 3; do printf 'key up\nwait-for-change\nkey right\nwait-for-change\nsettle\nshot L-step%s-continue\nkey x\nwait-for-change 30\nsettle 60 3\nshot L-after-step%s\n' "$st" "$st"; done
  364  } > "$f"
  365  # step 2's CONTINUE needs an SSH session open to the guest, as the player's terminal is (cloud_setup --connected)
  366  ssh -n -i $KEY -p $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o BatchMode=yes root@127.0.0.1 'sleep 900' >/dev/null 2>&1 &
  367  SSHPID=$!; sleep 2; say "  an SSH session held open for the walk (pid $SSHPID): $(G_ '/usr/bin/cloud_setup --connected')"
  368  grab_start L-setup 0.5
  369  walk "$f" "$FR"
  370  grab_stop L-setup; say "  L-setup: $(ls "$FR/L-setup" 2>/dev/null | wc -l) frames under $FR/L-setup (the step's scan page between step 3 and the question)"
  371  kill "$SSHPID" 2>/dev/null
  372  esl 'cloud_setup wizard|cloud folder step|cloud folder:' | tail -8 | tee -a "$LOG"
  373  esl 'cloud folder step: checking the folder \(end of cloud setup\)' | grep -q .; check $? "L: the step ran at the end of cloud setup"
  374  esl 'offering the move' | grep -q .; check $? "L: and asked the move for the earlier folder holding the saves"
  375  G_ "grep -q '^SAVES_REMOTE=\"/ROCKNIX/Saves\"' $CONF"; check $? "L: the step's scan joined the folder the saves are in"
  376  steps L2 'shot L-move-question' 'key z' 'wait-for-change' 'settle 120 3' 'shot L-after-not-now'
  377  esl 'cloud_setup wizard: complete' | grep -q .; check $? "L: NOT NOW went on to the seeding and CLOUD SETUP COMPLETE"
  378  steps L3 'shot L-setup-complete' 'dismiss-dialogs'
  379  rm -rf "$DATA/ROCKNIX"; mv "$DATA/_pixelelated_hold" "$DATA/pixelelated"
  380  say "  guest conf: $(conf /pixelelated/Saves /pixelelated/Backups /pixelelated/Content)"
  381  fi
  382  
  383  if want F; then
  384  say "== F: a scan the cloud refuses (the dead port): COULDN'T FINISH with TRY AGAIN beside CLOSE"
  385  G_ 'cp /storage/.config/rclone/rclone.conf /tmp/rclone.conf.good'
  386  "$R/tools/cloud-test-backend" dead-conf > $P/epic-dead.conf; scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR $P/epic-dead.conf root@127.0.0.1:/storage/.config/rclone/rclone.conf; rm -f $P/epic-dead.conf
  387  to_page restore F
  388  G_ 'test ! -e /storage/.cache/cloud_sync/scan/done'; check $? 'F: failed opening scan leaves no success stamp'
  389  steps F2 'shot F-outcome' 'key z' 'wait-for-change' 'settle' 'dismiss-dialogs'
  390  G_ 'cp /tmp/rclone.conf.good /storage/.config/rclone/rclone.conf'
  391  fi
  392  
  393  if want G; then
  394  say "== G: BACK UP TO THE CLOUD opens on the scan page too, then its options"
  395  to_page backup G
  396  G_ 'test -s /storage/.cache/cloud_sync/scan/done && grep -qx STATE=current /storage/.cache/cloud_sync/scan/state'; check $? 'G: backup page completed its opening scan on the current folder'
  397  steps G2 'dismiss-dialogs'
  398  fi
  399  
  400  say "  frames: $(find "$FR" -maxdepth 1 -type f -name '*.png' | wc -l) under $FR (numbered walk captures); boot and continuous captures are in their named subdirectories"
  401  done_line
  402  [ "$FAILS" -eq 0 ]
```

## File: tools/pixelelated-state-check (at 8ebaf8daad, 909 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present pixelelated
    4  """Inspect selected image/default/first-boot state without disclosing values (#565).
    5  
    6  Read-only policy, not a universal secret scanner. Exit 0: selected policy passes;
    7  1: prohibited presence; 2: incomplete/unsupported/unreadable/malformed input.
    8  The JSON uses policy paths, never input-derived names, values, or content hashes.
    9  No config is sourced, provider contacted, state repaired, or release published.
   10  """
   11  import argparse
   12  import configparser
   13  from datetime import datetime
   14  import gzip
   15  import json
   16  import os
   17  from pathlib import Path, PurePosixPath
   18  import re
   19  import resource
   20  import shlex
   21  import stat
   22  import subprocess
   23  import sys
   24  import tarfile
   25  import tempfile
   26  import xml.etree.ElementTree as ET
   27  
   28  
   29  POLICY = "pixelelated-selected-state-v1"
   30  LIMIT = 16 * 1024 * 1024
   31  MAX_NODES = 100000
   32  MAX_SYSTEM = 4 * 1024**3
   33  MAX_DISK = 16 * 1024**3
   34  CORE = {"system/configs/system.cfg": "system",
   35          "emulationstation/es_settings.cfg": "es",
   36          "retroarch/retroarch.cfg": "retroarch",
   37          "cloud_sync.conf": "cloud"}
   38  OPTIONAL = {
   39      "duckstation/settings.ini": "emulator", "melonDS/melonDS.ini": "melonds",
   40      "flycast/emu.cfg": "emulator", "aethersx2/inis/PCSX2.ini": "emulator",
   41      "ARMSX2/inis/PCSX2.ini": "emulator", "ARMSX2/inis/secrets.ini": "emulator",
   42      "dolphin-emu/RetroAchievements.ini": "emulator",
   43      "ppsspp/PSP/SYSTEM/ppsspp.ini": "ppsspp",
   44      "ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat": "opaque-account",
   45      "SkyEmu/ra_token.txt": "opaque-account",
   46      "gopher64/retroachievements.json": "opaque-account",
   47      "rclone/rclone.conf": "remote", "rclone/active-connection": "selection",
   48      "cloud_sync-device-id": "device-identity",
   49      "cloud_sync-device-id.previous": "device-identity",
   50  }
   51  SUFFIXES = ("", ".backup", ".bak", ".last-good", ".new", ".tmp")
   52  PLAYER = {"username", "password", "token", "key", "apikey", "api_key", "apitoken"}
   53  ES_PLAYER = {"screenscraperuser", "screenscraperpass", "retroachievementsusername",
   54               "retroachievementspassword", "retroachievementstoken"}
   55  ES_SERVICE = {"screenscraperdevid", "screenscraperdevpass", "gamesdbapikey"}
   56  REMOTE_AUTH = {"user", "pass", "password", "token", "key", "access_token",
   57                 "refresh_token", "secret_access_key", "access_key_id"}
   58  SERVICE = {"client_id", "client_secret"}
   59  QA_NAME = re.compile(r"^(?:qa[-_]|\.qa[-_]|pixelelated-qa|rocknix-qa|test-fixture)", re.I)
   60  SCOPE = ["selected system, ES, RetroArch, standalone account files and recovery siblings",
   61           "rclone configuration and active selection; cloud device identity and activity cache",
   62           "zero-redaction startup scrub marker; only the exact current-boot no-adapter diagnostic may be inspected",
   63           "gamelist.xml under selected ES/config/ROM roots; playcount and lastplayed only",
   64           "known QA name prefixes, proxy state, token files and RetroArch history playlists",
   65           "ES ELF known compiled ScreenScraper/RetroAchievements URL-pair patterns; "
   66           "only the exact NUL-delimited shared JELOS developer pair is allowed (#566)",
   67           "img.gz: supported two-partition image and empty storage seed policy"]
   68  LIMITATIONS = ["not a whole-image or arbitrary-secret scan",
   69                 "no generic compiled GamesDB key detection or service identity provenance",
   70                 "no custom ES system paths, environment overrides, external media or arbitrary archives",
   71                 "no interpretation of operation success, bytes transferred, actor or metadata origin",
   72                 "scrub epoch bounds do not establish origin; clock steps can cause refusal",
   73                 "retained-upgrade permits runtime state; it does not prove upgrade preservation"]
   74  LOCALE_ALIAS = "/usr/config/emulationstation/locale"
   75  LOCALE_SHARED = "/usr/share/locale"
   76  LOCALE_RUNTIME = "/storage/.config/locale"
   77  SCRUB_MARKER = "/storage/.cache/cloud_sync/log-scrubbed"
   78  SCRUB_STARTUP_LOG = "/storage/.cache/log/cloud_sync.log"
   79  # cloud_device_id --if-present intentionally logs this before autostart when
   80  # no adapter exists yet (#151/D-NET-005). FILES counts inspected files, not
   81  # redactions; one such current-boot diagnostic is not prior player activity.
   82  NO_ADAPTER_DIAGNOSTIC = (
   83      b"no stored id and no adapter to derive one from yet; not seeding the identity "
   84      b"from machine-id at this caller's request (--if-present)"
   85  )
   86  
   87  
   88  class Invalid(Exception):
   89      """Carries no input-derived text."""
   90  
   91  
   92  def require(ok):
   93      if not ok:
   94          raise Invalid()
   95  
   96  
   97  def command(argv, limit=LIMIT, file_limit=None):
   98      # Child diagnostics can contain config values/filenames. Never forward them.
   99      # Bound stdout on disk rather than accumulating arbitrary child output in RAM.
  100      with tempfile.TemporaryFile() as output:
  101          try:
  102              def bounded_output():
  103                  ceiling = limit if file_limit is None else file_limit
  104                  resource.setrlimit(resource.RLIMIT_FSIZE, (ceiling, ceiling))
  105              proc = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=output,
  106                                    stderr=subprocess.DEVNULL, timeout=180,
  107                                    preexec_fn=bounded_output)
  108          except (OSError, subprocess.TimeoutExpired):
  109              raise Invalid() from None
  110          require(proc.returncode == 0 and output.tell() <= limit)
  111          output.seek(0)
  112          return output.read(limit + 1)
  113  
  114  
  115  def text(data):
  116      require(b"\0" not in data)
  117      return data.decode("utf-8-sig", errors="strict")
  118  
  119  
  120  def xml(data, tag):
  121      # No DTD/entities (including internally declared ones), or ambiguous fragments.
  122      require(not re.search(br"<!\s*(?:DOCTYPE|ENTITY)", data, re.I))
  123      root = ET.fromstring(text(data))
  124      require(root.tag == tag)
  125      return root
  126  
  127  
  128  def pairs(data, melonds=False, comment_only=False, ppsspp=False):
  129      """Strict non-executing key/value + INI subset used by selected configs."""
  130      result, seen, section = [], {}, ""
  131      source = text(data)
  132      require(bool(source.strip()))
  133      for line in source.splitlines():
  134          line = line.strip()
  135          # RetroArch's include directives look like comments but change effective
  136          # configuration. No silent pass for an input outside this policy.
  137          require(not re.match(r"^#\s*(?:include|reference)\b", line, re.I))
  138          if not line or line.startswith(("#", ";")):
  139              continue
  140          if line.startswith("["):
  141              require(re.fullmatch(r"\[[^\[\]\r\n]+\]", line))
  142              section = line[1:-1].lower()
  143              continue
  144          # PPSSPP IniFile::ParseLineKey preserves internal spaces/tabs, including
  145          # its declared "Enable Logging" key (#599). Keep other config grammars
  146          # strict; escaped/comment-bearing keys remain outside this small subset.
  147          pattern = (r"([^=\s#\\]+(?:[ \t]+[^=\s#\\]+)*)[ \t]*=[ \t]*(.*)"
  148                     if ppsspp else r"([^=\s]+)\s*=\s*(.*)")
  149          match = re.fullmatch(pattern, line)
  150          require(match is not None)
  151          key, value = match.groups()
  152          key = key.lower()
  153          # Shipped system.cfg repeats an identical unrelated scalar. Collapse only
  154          # exact repeats; conflicting duplicates cannot hide a populated account.
  155          if (section, key) in seen:
  156              require(seen[(section, key)] == value)
  157              continue
  158          seen[(section, key)] = value
  159          # cheevos_melonds.sh and AMD64 defaults use precisely these unquoted,
  160          # sectionless assignments for absent accounts. Do not generalize null
  161          # to other emulators, INI sections, key spellings or quoted strings.
  162          if melonds and not section and line in {
  163                  "RA_Username=null", "RA_Password=null", "RA_Token=null"}:
  164              value = ""
  165          # PPSSPP StripQuotes removes double quotes only: '' is a populated
  166          # literal there, so it must not become an empty account in this reader.
  167          quotes = ('"',) if ppsspp else ('"', "'")
  168          if value.startswith(quotes):
  169              quote = value[0]
  170              require(len(value) >= 2 and value.endswith(quote))
  171              value = value[1:-1]
  172          result.append((section, key, value))
  173      # Upstream /etc/retroarch.cfg may contain only # comments. Empty/blank files,
  174      # INI sections and semicolon-only content are not that supported format.
  175      require(bool(result) or comment_only and all(
  176          not line.strip() or line.lstrip().startswith("#") for line in source.splitlines()))
  177      return result
  178  
  179  
  180  class Local:
  181      """Only selected paths are read. Absolute links resolve inside the supplied root."""
  182      def __init__(self, root):
  183          self.root = root.resolve(strict=True)
  184          require(self.root.is_dir())
  185  
  186      def resolve(self, path):
  187          pending, done, links = list(PurePosixPath(path).parts[1:]), [], 0
  188          while pending:
  189              part = pending.pop(0)
  190              if part in ("", "."):
  191                  continue
  192              if part == "..":
  193                  require(bool(done))
  194                  done.pop()
  195                  continue
  196              candidate = self.root.joinpath(*done, part)
  197              try:
  198                  meta = candidate.lstat()
  199              except FileNotFoundError:
  200                  require(links == 0)
  201                  # The remaining suffix is absent, not an unreadable directory.
  202                  return candidate.joinpath(*pending)
  203              if stat.S_ISLNK(meta.st_mode):
  204                  links += 1
  205                  require(links <= 40)
  206                  target = PurePosixPath(os.readlink(candidate))
  207                  if target.is_absolute():
  208                      done = []
  209                      pending = list(target.parts[1:]) + pending
  210                  else:
  211                      pending = list(target.parts) + pending
  212              else:
  213                  done.append(part)
  214          return self.root.joinpath(*done)
  215  
  216      def info(self, path):
  217          p = self.resolve(path)
  218          try:
  219              meta = p.lstat()
  220          except FileNotFoundError:
  221              return None
  222          require(not stat.S_ISLNK(meta.st_mode))
  223          require(meta.st_mode & 0o444)  # root must not turn mode-000 into a pass
  224          if stat.S_ISDIR(meta.st_mode):
  225              require(meta.st_mode & 0o111)
  226              return "dir", meta.st_size
  227          require(stat.S_ISREG(meta.st_mode))
  228          return "file", meta.st_size
  229  
  230      def link(self, path):
  231          # Resolve the parent safely, but inspect the final component without
  232          # following it. Used only to recognize the shipped runtime locale alias.
  233          name = PurePosixPath(path)
  234          p = self.resolve(str(name.parent)) / name.name
  235          try:
  236              meta = p.lstat()
  237          except FileNotFoundError:
  238              return None
  239          return os.readlink(p) if stat.S_ISLNK(meta.st_mode) else None
  240  
  241      def children(self, path):
  242          require(self.info(path)[0] == "dir")
  243          return sorted(p.name for p in self.resolve(path).iterdir())
  244  
  245      def read(self, path, limit=LIMIT, *, with_mtime=False):
  246          info = self.info(path)
  247          require(info and info[0] == "file" and info[1] <= limit)
  248          fd = os.open(self.resolve(path), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
  249          with os.fdopen(fd, "rb") as stream:
  250              before = os.fstat(stream.fileno())
  251              require(stat.S_ISREG(before.st_mode))
  252              data = stream.read(limit + 1)
  253              after = os.fstat(stream.fileno())
  254          require(len(data) <= limit and len(data) == after.st_size)
  255          require((before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
  256                  (after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns))
  257          return (data, after.st_mtime_ns) if with_mtime else data
  258  
  259      def boot_window(self):
  260          # These two proc files have st_size=0 while containing kernel data, so
  261          # ordinary immutable-file size equality is inapplicable. Read only these
  262          # fixed paths with the same root containment, type and permission guards.
  263          # Offline roots must provide regular snapshot files; never borrow host
  264          # boot data to bless a different root's startup marker.
  265          def proc_read(path):
  266              info = self.info(path)
  267              require(info and info[0] == "file")
  268              fd = os.open(self.resolve(path), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
  269              with os.fdopen(fd, "rb") as stream:
  270                  meta = os.fstat(stream.fileno())
  271                  require(stat.S_ISREG(meta.st_mode) and meta.st_mode & 0o444)
  272                  data = stream.read(65537)
  273              require(len(data) <= 65536)
  274              return text(data)
  275  
  276          def boot_epoch():
  277              lines = [line for line in proc_read("/proc/stat").splitlines() if line.startswith("btime")]
  278              require(len(lines) == 1 and re.fullmatch(r"btime [1-9][0-9]{0,18}", lines[0]))
  279              return int(lines[0].split()[1])
  280  
  281          start = boot_epoch()
  282          uptime = re.fullmatch(r"([0-9]{1,12})\.[0-9]{2} [0-9]{1,16}\.[0-9]{2}\n",
  283                                proc_read("/proc/uptime"))
  284          require(uptime is not None and boot_epoch() == start)
  285          # btime and the writer's date +%s are whole seconds; uptime is hundredths.
  286          # Round the upper endpoint up one second, without a wider grace period.
  287          return start, start + int(uptime[1]) + 1
  288  
  289  
  290  class Squash:
  291      """Use listing/cat only: no filesystem is mounted or extracted as a tree."""
  292      def __init__(self, path):
  293          self.path, self.nodes = path, {}
  294          listing = text(command(["unsquashfs", "-processors", "1", "-mem", "64M",
  295                                  "-lln", "-d", "root", str(path)]))
  296          for line in listing.splitlines():
  297              if not line.strip() or line.startswith("Parallel unsquashfs:"):
  298                  continue
  299              m = re.fullmatch(r"([dlcbps-][rwxStTs-]{9})\s+\d+/\d+\s+\S+\s+"
  300                               r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s+root(?:/(.*))?", line)
  301              require(m is not None)
  302              mode, name = m.groups()
  303              name = name or ""
  304              target = None
  305              if mode[0] == "l":
  306                  require(" -> " in name)
  307                  name, target = name.split(" -> ", 1)
  308              path_name = "/" + name
  309              require(".." not in PurePosixPath(path_name).parts and path_name not in self.nodes)
  310              self.nodes[path_name] = (mode, target)
  311              require(len(self.nodes) <= MAX_NODES)
  312          require("/" in self.nodes)
  313          self.child_names = {}
  314          for name in self.nodes:
  315              if name != "/":
  316                  parent, leaf = name.rsplit("/", 1)
  317                  self.child_names.setdefault(parent or "/", []).append(leaf)
  318  
  319      def resolve(self, path):
  320          pending, done, links = list(PurePosixPath(path).parts[1:]), [], 0
  321          while pending:
  322              part = pending.pop(0)
  323              if part in ("", "."):
  324                  continue
  325              if part == "..":
  326                  require(bool(done))
  327                  done.pop()
  328                  continue
  329              name = "/" + "/".join(done + [part])
  330              item = self.nodes.get(name)
  331              if item and item[0][0] == "l":
  332                  links += 1
  333                  require(links <= 40)
  334                  link = PurePosixPath(item[1])
  335                  if link.is_absolute():
  336                      done = []
  337                      pending = list(link.parts[1:]) + pending
  338                  else:
  339                      pending = list(link.parts) + pending
  340              else:
  341                  done.append(part)
  342          result = "/" + "/".join(done)
  343          require(links == 0 or result in self.nodes)
  344          return result
  345  
  346      def info(self, path):
  347          item = self.nodes.get(self.resolve(path))
  348          if item is None:
  349              return None
  350          mode = item[0]
  351          require("r" in mode and mode[0] in "d-")
  352          if mode[0] == "d":
  353              require(any(bit in mode for bit in "xst"))
  354          return ("dir" if mode[0] == "d" else "file"), 0
  355  
  356      def link(self, path):
  357          name = PurePosixPath(path)
  358          parent = self.resolve(str(name.parent))
  359          item = self.nodes.get(parent.rstrip("/") + "/" + name.name)
  360          return item[1] if item and item[0][0] == "l" else None
  361  
  362      def children(self, path):
  363          require(self.info(path)[0] == "dir")
  364          return sorted(self.child_names.get(self.resolve(path), []))
  365  
  366      def read(self, path, limit=LIMIT):
  367          require(self.info(path) and self.info(path)[0] == "file")
  368          # The inventory names one exact file. Default cat globbing can substitute
  369          # a clean sibling for a contaminated name containing brackets, * or ?.
  370          return command(["unsquashfs", "-processors", "1", "-mem", "64M", "-no-wildcards", "-cat",
  371                          str(self.path), self.resolve(path).lstrip("/")], limit)
  372  
  373  
  374  class Check:
  375      def __init__(self, fs, mode):
  376          self.fs, self.mode, self.rows = fs, mode, []
  377  
  378      def row(self, path, category, count=0, present=True, error=False):
  379          retained = self.mode == "retained-upgrade" and path.startswith("/storage/")
  380          approved_service = (path == "/usr/bin/emulationstation" and
  381                              category == "approved-shared-developer-identity")
  382          if category == "unsupported-config-override" and count:
  383              error = True
  384          self.rows.append({"path": path, "category": category, "present": present,
  385                            "count": count, "status": "error" if error else
  386                            "allowed" if count and (retained or approved_service) else
  387                            "blocked" if count else "clear"})
  388  
  389      def file(self, path, kind, required=False, label=None):
  390          label = label or path
  391          try:
  392              info = self.fs.info(path)
  393              if info is None:
  394                  self.row(label, kind, present=False, error=required)
  395                  return
  396              require(info[0] == "file")
  397              if kind == "scrub-marker":
  398                  require(self.fs.link(path) is None)  # the writer atomically installs a regular file
  399              limit = 256 * 1024**2 if kind == "compiled-service" else 4096 if kind == "scrub-marker" else LIMIT
  400              data = self.fs.read(path, limit)
  401              counts = self.parse(kind, data)
  402              for category, count in counts.items():
  403                  self.row(label, category, count)
  404          except (Invalid, OSError, ValueError, ET.ParseError, configparser.Error):
  405              self.row(label, "input-invalid", error=True)
  406  
  407      def parse(self, kind, data):
  408          if kind == "compiled-service":
  409              require(len(data) >= 64 and data[:4] == b"\x7fELF" and data[4] in (1, 2))
  410              # Known compiled URL fragments only. Bare runtime fragments have no value.
  411              value = rb"[^\x00\s&\"'<>]+"
  412              patterns = [rb"devid=" + value + rb"&devpassword=" + value,
  413                          rb"z=" + value + rb"&y=" + value]
  414              matches = [match for pattern in patterns for match in re.finditer(pattern, data)]
  415              # D-WORKFLOW-166 permits this one public developer pair in the ELF,
  416              # never player accounts, RA keys or seeded runtime settings. Require
  417              # the complete C string: prefixes, suffixes and changed pairs refuse.
  418              shared = b"jelos"
  419              approved = b"devid=" + shared + b"&devpassword=" + shared
  420              allowed = sum(match.group() == approved and match.start() > 0 and
  421                            data[match.start() - 1:match.start()] == b"\0" and
  422                            data[match.end():match.end() + 1] == b"\0"
  423                            for match in matches)
  424              return {"developer-service-identity": len(matches) - allowed,
  425                      "approved-shared-developer-identity": allowed}
  426          if kind == "opaque-account":
  427              return {"player-account-file": int(bool(data.strip()))}
  428          if kind in ("selection", "device-identity"):
  429              text(data)
  430              return {"configured-remote" if kind == "selection" else kind: int(bool(data.strip()))}
  431          if kind == "stamp":
  432              require(re.fullmatch(r"\d+\s+-?\d+(?:\s+[^\r\n]+)?\s*", text(data)) is not None)
  433              return {"cloud-activity": 1}
  434          if kind == "scrub-marker":
  435              if self.mode == "clean-image":
  436                  return {"preseeded-log-scrub": 1}  # any seed predates the first boot
  437              number = rb"(0|[1-9][0-9]{0,18})"
  438              family = rb"=([1-9][0-9]{0,18}) files=" + number + rb" lines=" + number + rb"\n"
  439              if self.mode == "retained-upgrade":
  440                  # Either family may complete alone. record() preserves existing
  441                  # lines before appending, so a retry can put ES before cloud.
  442                  # Accept these historical states without calling them clean boot.
  443                  records, seen = data.splitlines(keepends=True), set()
  444                  require(1 <= len(records) <= 2)
  445                  for line in records:
  446                      item = re.fullmatch(rb"(scrubbed|es_log_scrubbed)" + family, line)
  447                      require(item is not None and item[1] not in seen)
  448                      seen.add(item[1])
  449                  return {"retained-log-scrub": 1}
  450              marker = re.fullmatch(rb"scrubbed" + family + rb"es_log_scrubbed" + family, data)
  451              require(marker is not None)
  452              first, files1, lines1, second, files2, lines2 = map(int, marker.groups())
  453              work = int(bool(files1 or lines1)) + int(bool(files2 or lines2))
  454              if work and (files1, lines1, files2, lines2) != (1, 0, 0, 0):
  455                  return {"cloud-log-scrub-activity": work}
  456              start, end = self.fs.boot_window()
  457              if not start <= first <= second <= end:
  458                  return {"log-scrub-outside-boot": 1}
  459              if work:
  460                  info = self.fs.info(SCRUB_STARTUP_LOG)
  461                  if info is None:
  462                      return {"cloud-log-scrub-activity": work}
  463                  require(info[0] == "file" and self.fs.link(SCRUB_STARTUP_LOG) is None)
  464                  # No rotation, partial scrub, extra line or arbitrary clean log
  465                  # gets this exception. ES logs remain covered by files2 == 0.
  466                  family = [name for name in self.fs.children("/storage/.cache/log")
  467                            if name == "cloud_sync.log" or name.startswith("cloud_sync.log.")]
  468                  log, mtime = self.fs.read(SCRUB_STARTUP_LOG, 4096, with_mtime=True)
  469                  line = re.fullmatch(rb"\[([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})\] "
  470                                      rb"\[INFO\] \[cloud_device_id\] " +
  471                                      re.escape(NO_ADAPTER_DIAGNOSTIC) + rb"\n", log)
  472                  if family != ["cloud_sync.log"] or line is None:
  473                      return {"cloud-log-scrub-activity": work}
  474                  datetime.strptime(line[1].decode("ascii"), "%Y-%m-%d %H:%M:%S")
  475                  # The log has no timezone suffix. Do not borrow the host's TZ
  476                  # to date an offline root: use the stable file read's epoch
  477                  # mtime, from this boot and no later than the scrub's second.
  478                  if not start * 1000000000 <= mtime < (first + 1) * 1000000000:
  479                      return {"log-scrub-outside-boot": 1}
  480                  return {"startup-no-adapter-log-scrub": 0}
  481              return {"startup-log-scrub": 0}
  482          if kind == "gamelist":
  483              root = xml(data, "gameList")
  484              counts = {"playcount": 0, "lastplayed": 0}
  485              for entry in root:
  486                  require(entry.tag in ("game", "folder"))
  487                  for key in counts:
  488                      nodes = entry.findall(key)
  489                      require(len(nodes) <= 1)
  490                      if not nodes:
  491                          continue
  492                      require(len(nodes[0]) == 0)
  493                      value = (nodes[0].text or "").strip()
  494                      if key == "playcount":
  495                          require(not value or re.fullmatch(r"[0-9]+", value))
  496                          # Accepted ES compares PlayCount as a string (not an integer).
  497                          counts[key] += int(value > "0")
  498                      else:
  499                          if value not in ("", "0", "00000000T000000"):
  500                              require(re.fullmatch(r"\d{8}T\d{6}", value))
  501                              datetime.strptime(value, "%Y%m%dT%H%M%S")
  502                              counts[key] += 1
  503              return counts
  504          if kind == "playlist":
  505              obj = json.loads(text(data))
  506              require(isinstance(obj, dict) and isinstance(obj.get("items"), list))
  507              return {"play-history": len(obj["items"])}
  508          if kind == "remote":
  509              parser = configparser.RawConfigParser(strict=True, interpolation=None)
  510              parser.read_string(text(data))
  511              require(not parser.defaults())
  512              counts = {"configured-remote": len(parser.sections()), "player-account": 0,
  513                        "developer-service-identity": 0}
  514              for section in parser.sections():
  515                  require(parser.has_option(section, "type") and parser.get(section, "type").strip())
  516                  for key, val in parser.items(section):
  517                      if val.strip():
  518                          counts["player-account"] += int(key in REMOTE_AUTH)
  519                          counts["developer-service-identity"] += int(key in SERVICE)
  520              return counts
  521          if kind == "es":
  522              root = xml(data, "config")
  523              items, seen = [], set()
  524              for child in root:
  525                  require(child.tag in ("string", "bool", "int", "float") and
  526                          set(child.attrib) == {"name", "value"} and len(child) == 0)
  527                  key = child.attrib["name"].lower()
  528                  require(key not in seen)
  529                  seen.add(key)
  530                  items.append(("", key, child.attrib["value"]))
  531          elif kind == "cloud":
  532              # Literal assignments only; shell expansion is never evaluated.
  533              source = text(data).replace("\\\n", "")
  534              items = []
  535              for _, key, val in pairs(source.encode()):
  536                  require(not any(s in val for s in ("`", "$(", "${", ";")))
  537                  items.append(("", key.removeprefix("default_"), val))
  538          else:
  539              items = pairs(data, melonds=kind == "melonds", comment_only=kind == "retroarch-default",
  540                            ppsspp=kind == "ppsspp")
  541          counts = {"player-account": 0, "developer-service-identity": 0}
  542          if kind == "cloud":
  543              counts["configured-remote"] = 0
  544              counts["unsupported-config-override"] = 0
  545              require({"savespath", "saves_remote", "settings_remote", "content_remote"} <=
  546                      {key for _, key, _ in items})
  547          for section, key, val in items:
  548              if not val.strip():
  549                  continue
  550              personal = (key in ES_PLAYER or key.startswith("global.retroachievements.") and
  551                          key.rsplit(".", 1)[-1] in PLAYER or
  552                          key.startswith(("cheevos_", "ra_")) and key.split("_", 1)[1] in PLAYER or
  553                          section in ("achievements", "retroachievements", "cheevos") and key in PLAYER or
  554                          # PPSSPP's actual case-insensitive keys. The token is
  555                          # usually opaque .dat state, but manual INI loading is
  556                          # supported too (Core/Config.cpp, #599).
  557                          kind == "ppsspp" and section == "achievements" and
  558                          key in {"achievementsusername", "achievementstoken"})
  559              counts["player-account"] += int(personal)
  560              counts["developer-service-identity"] += int(key in ES_SERVICE or key in SERVICE)
  561              if kind == "cloud":
  562                  counts["configured-remote"] += int(key in ("remote", "rclone_remote", "rclone_config"))
  563                  counts["unsupported-config-override"] += int(key == "rclone_config")
  564                  if key in ("rcloneopts", "rclone_net_opts", "rclone_sync_net_opts"):
  565                      # Custom rclone flags can redirect the effective credential input.
  566                      tokens = shlex.split(val)
  567                      allowed = {"--progress", "--log-file", "/var/log/cloud_sync.log", "--filter-from",
  568                                 "/storage/.config/cloud_sync-rules.txt", "--contimeout", "--timeout",
  569                                 "--low-level-retries", "--retries", "--max-duration", "--transfers"}
  570                      counts["unsupported-config-override"] += sum(
  571                          token not in allowed and not re.fullmatch(r"\d+[smh]?", token) for token in tokens)
  572          return counts
  573  
  574      def deferred_locale(self, path):
  575          # ES post_install ships this exact two-hop link; userconfig-setup creates
  576          # its storage target at first boot. Only this absent runtime target is
  577          # permitted in a clean image. Never relax either generic link resolver.
  578          if self.mode != "clean-image" or path != LOCALE_ALIAS:
  579              return False
  580          target = self.fs.link(path)
  581          if target is None:
  582              return False
  583          require(target == LOCALE_SHARED and self.fs.link(LOCALE_SHARED) == LOCALE_RUNTIME)
  584          if self.fs.link(LOCALE_RUNTIME) is not None or self.fs.info(LOCALE_RUNTIME) is not None:
  585              return False  # existing targets still undergo the ordinary walk
  586          self.row(LOCALE_ALIAS, "runtime-locale-deferred")
  587          return True
  588  
  589      def walk(self, path, label, callback, required=False):
  590          try:
  591              info = self.fs.info(path)
  592              if info is None:
  593                  self.row(label, "inventory", present=False, error=required)
  594                  return
  595              require(info[0] == "dir")
  596              pending, seen, count = [path], set(), 0
  597              while pending:
  598                  directory = pending.pop()
  599                  resolved = str(self.fs.resolve(directory))
  600                  require(resolved not in seen)
  601                  seen.add(resolved)
  602                  for name in self.fs.children(directory):
  603                      count += 1
  604                      require(count <= MAX_NODES)
  605                      item = directory + "/" + name
  606                      if self.deferred_locale(item):
  607                          continue
  608                      info = self.fs.info(item)
  609                      require(info is not None)
  610                      callback(item, name, info[0])
  611                      if info[0] == "dir":
  612                          pending.append(item)
  613              self.row(label, "inventory")
  614          except (Invalid, OSError, ValueError):
  615              self.row(label, "input-invalid", error=True)
  616  
  617      def run(self):
  618          for base in ("/usr/config", "/storage/.config"):
  619              runtime = base.startswith("/storage")
  620              required = not runtime or self.mode != "clean-image"
  621              for name, kind in {**CORE, **OPTIONAL}.items():
  622                  for suffix in SUFFIXES:
  623                      self.file(base + "/" + name + suffix, kind,
  624                                required=required and name in CORE and not suffix)
  625                  # Atomic/recovery writers also use PID/time suffixes. Inspect those
  626                  # without disclosing their input-derived names in the report.
  627                  path = base + "/" + name
  628                  parent, leaf = path.rsplit("/", 1)
  629                  try:
  630                      if self.fs.info(parent) is not None:
  631                          for sibling in self.fs.children(parent):
  632                              if sibling.startswith(leaf + ".") and sibling[len(leaf):] not in SUFFIXES:
  633                                  self.file(parent + "/" + sibling, kind, label=path + ".*")
  634                  except (Invalid, OSError, ValueError):
  635                      self.row(path + ".*", "input-invalid", error=True)
  636              if not runtime:
  637                  self.file(base + "/cloud_sync.conf.defaults", "cloud", required=True)
  638              def config_entry(path, name, typ):
  639                  label = base + "/**"
  640                  if QA_NAME.match(name):
  641                      self.row(label, "qa-residue", 1)
  642                  if typ == "file" and name == "gamelist.xml":
  643                      self.file(path, "gamelist", label=base + "/**/gamelist.xml")
  644                  if typ == "file" and name.startswith("content_") and name.endswith("history.lpl"):
  645                      self.file(path, "playlist", label=base + "/**/content_*history.lpl")
  646                  if typ == "file" and "/raofflineproxy/" in path:
  647                      self.row(base + "/raofflineproxy/**", "account-cache-residue", 1)
  648                  if typ == "file" and "/rclone/" in path and name not in {
  649                          n + s for n in ("rclone.conf", "active-connection") for s in SUFFIXES}:
  650                      self.row(base + "/rclone/**", "connection-residue", 1)
  651              # Skip unrelated default asset trees: only config directories named by policy.
  652              for folder in sorted({name.split("/")[0] for name in (*CORE, *OPTIONAL) if "/" in name} |
  653                                   {"raofflineproxy"}):
  654                  self.walk(base + "/" + folder, base + "/" + folder + "/**", config_entry)
  655          self.file("/etc/retroarch.cfg", "retroarch-default", required=True)
  656          self.file("/usr/bin/emulationstation", "compiled-service", required=True)
  657          def history(path, name, typ):
  658              if typ == "file" and name == "gamelist.xml":
  659                  self.file(path, "gamelist", label="/storage/roms/**/gamelist.xml")
  660              if QA_NAME.match(name):
  661                  self.row("/storage/roms/**", "qa-residue", 1)
  662          self.walk("/storage/roms", "/storage/roms/**", history,
  663                    required=self.mode != "clean-image")
  664          def activity(path, name, typ):
  665              if path == SCRUB_MARKER:
  666                  self.file(path, "scrub-marker")
  667              elif typ == "file" and name.startswith("last-"):
  668                  self.file(path, "stamp", label="/storage/.cache/cloud_sync/last-*")
  669              elif typ == "file":
  670                  self.row("/storage/.cache/cloud_sync/**", "cloud-state-residue", 1)
  671          self.walk("/storage/.cache/cloud_sync", "/storage/.cache/cloud_sync/**", activity)
  672          for base in ("/storage", "/storage/.config", "/storage/.cache", "/usr/config"):
  673              try:
  674                  if self.fs.info(base) is None:
  675                      continue
  676                  for name in self.fs.children(base):
  677                      if QA_NAME.match(name):
  678                          self.row(base + "/*", "qa-residue", 1)
  679              except (Invalid, OSError, ValueError):
  680                  self.row(base + "/*", "input-invalid", error=True)
  681          return self.report()
  682  
  683      def report(self):
  684          errors = sum(r["status"] == "error" for r in self.rows)
  685          blocked = sum(r["status"] == "blocked" for r in self.rows)
  686          return {"schema": 1, "policy": POLICY, "mode": self.mode,
  687                  "status": "error" if errors else "blocked" if blocked else "pass",
  688                  "error_count": errors, "blocked_count": blocked,
  689                  "scope": SCOPE, "limitations": LIMITATIONS, "checks": self.rows}
  690  
  691  
  692  def copy_bounded(source, destination, limit):
  693      count = 0
  694      with destination.open("xb") as out:
  695          while block := source.read(1024 * 1024):
  696              count += len(block)
  697              require(count <= limit)
  698              # Sparse zeros keep decompressed install images from allocating their empty space.
  699              if block.count(0) == len(block):
  700                  out.seek(len(block), 1)
  701              else:
  702                  out.write(block)
  703          out.truncate(count)
  704      return count
  705  
  706  
  707  def empty_ext4(path):
  708      command(["e2fsck", "-fn", str(path)])
  709      def listing(directory):
  710          raw = text(command(["debugfs", "-R", "ls -p " + directory, str(path)]))
  711          entries = {}
  712          for line in raw.splitlines():
  713              if not line.strip():
  714                  continue
  715              # debugfs 1.47.2 prints this exact unused directory slot for a freshly
  716              # allocated lost+found. It has no inode, name, ownership or content.
  717              # Every other zero-inode shape must still fail the live-entry checks.
  718              if line == "/0/000000/0/0//0/":
  719                  continue
  720              fields = line.split("/")
  721              require(len(fields) == 8 and fields[0] == fields[-1] == "")
  722              inode, mode, uid, gid, name, size = fields[1:-1]
  723              require(inode.isdigit() and int(inode) > 0 and re.fullmatch(r"[0-7]+", mode)
  724                      and uid.isdigit() and gid.isdigit() and name not in entries)
  725              entries[name] = (int(mode, 8), size)
  726          require("." in entries and ".." in entries)
  727          return entries
  728      entries = listing("/")
  729      residue = len(set(entries) - {".", "..", "lost+found", ".please_resize_me"})
  730      if "lost+found" in entries:
  731          require(stat.S_ISDIR(entries["lost+found"][0]))
  732          residue += len(set(listing("/lost+found")) - {".", ".."})
  733      if ".please_resize_me" in entries:
  734          mode, size = entries[".please_resize_me"]
  735          require(stat.S_ISREG(mode) and size == "0")
  736      return residue
  737  
  738  
  739  def payload(path):
  740      """Inspect actual final bytes; caller does not supply a reusable pass receipt."""
  741      require(path.is_file() and not path.is_symlink())
  742      with tempfile.TemporaryDirectory(prefix="pix-state-") as directory:
  743          scratch = Path(directory)
  744          system = scratch / "SYSTEM"
  745          storage_residue = None
  746          if path.name.endswith(".tar"):
  747              # No tar extraction: inspect member metadata, then copy exactly one regular SYSTEM.
  748              with tarfile.open(path, "r:") as archive:
  749                  seen, systems, roots = set(), [], set()
  750                  for member in archive:
  751                      name = PurePosixPath(member.name)
  752                      require(not name.is_absolute() and ".." not in name.parts and
  753                              str(name) not in seen and len(seen) < MAX_NODES)
  754                      seen.add(str(name))
  755                      require(name.parts and (member.isfile() or member.isdir()))
  756                      roots.add(name.parts[0])
  757                      if len(name.parts) == 3 and name.parts[1:] == ("target", "SYSTEM"):
  758                          require(member.isfile() and 0 < member.size <= MAX_SYSTEM)
  759                          systems.append(member)
  760                      # An update tar must not smuggle a storage/default payload beside SYSTEM.
  761                      require(not any(p in ("storage", "usr", ".config") for p in name.parts))
  762                  require(len(systems) == 1 and len(roots) == 1)
  763                  stream = archive.extractfile(systems[0])
  764                  require(stream is not None)
  765                  with stream:
  766                      require(copy_bounded(stream, system, MAX_SYSTEM) == systems[0].size)
  767          elif path.name.endswith(".img.gz"):
  768              disk = scratch / "disk.img"
  769              with gzip.open(path, "rb") as stream:
  770                  size = copy_bounded(stream, disk, MAX_DISK)
  771              table = json.loads(text(command(["sfdisk", "--json", str(disk)])))["partitiontable"]
  772              require(table["label"] in ("gpt", "dos") and table["unit"] == "sectors" and
  773                      table.get("sectorsize", 512) == 512 and len(table["partitions"]) == 2)
  774              first, second = table["partitions"]
  775              for part in (first, second):
  776                  require(type(part["start"]) is int and type(part["size"]) is int and
  777                          part["start"] > 0 and part["size"] > 0 and
  778                          (part["start"] + part["size"]) * 512 <= size)
  779              require(first["start"] + first["size"] <= second["start"])
  780              require(second["size"] * 512 <= 512 * 1024**2)
  781              storage = scratch / "storage.ext4"
  782              with disk.open("rb") as stream, storage.open("xb") as out:
  783                  stream.seek(second["start"] * 512)
  784                  remaining = second["size"] * 512
  785                  while remaining:
  786                      block = stream.read(min(1024 * 1024, remaining))
  787                      require(bool(block))
  788                      out.write(block)
  789                      remaining -= len(block)
  790              storage_residue = empty_ext4(storage)
  791              command(["mcopy", "-n", "-i", str(disk) + "@@" + str(first["start"] * 512),
  792                       "::/SYSTEM", str(system)], file_limit=MAX_SYSTEM)
  793              require(system.is_file() and 0 < system.stat().st_size <= MAX_SYSTEM)
  794          else:
  795              raise Invalid()
  796          check = Check(Squash(system), "clean-image")
  797          check.run()
  798          if storage_residue is not None:
  799              check.row("<install-storage>/**", "storage-seed-residue", storage_residue)
  800          result = check.report()
  801          result["input_kind"] = "install-image" if path.name.endswith(".img.gz") else "update-tar"
  802          return result
  803  
  804  
  805  def first_boot_ready():
  806      """Inspect effective unit execution, not is-active on one assumed unit name.
  807  
  808      The source unit retains its successful oneshot as active/exited; an installed
  809      variant can finish as inactive/dead. Result=success alone also describes a
  810      unit that never ran, so require actual execution and current-boot artifacts.
  811      """
  812      boot = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
  813      require(bool(re.fullmatch(r"[0-9a-f-]{36}", boot)))
  814      names = ("autostart.service", "rocknix-autostart.service")
  815      properties = ("Id", "LoadState", "Type", "ActiveState", "SubState", "Result",
  816                    "ExecMainCode", "ExecMainStatus", "ExecMainStartTimestampMonotonic",
  817                    "ExecMainExitTimestampMonotonic", "ConditionResult", "ExecStart")
  818      completed = set()
  819      for name in names:
  820          proc = subprocess.run(["systemctl", "show", "--no-pager",
  821                                 "--property=" + ",".join(properties), name],
  822                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
  823                                stderr=subprocess.DEVNULL, timeout=5)
  824          require(len(proc.stdout) <= 16384)
  825          fields = {}
  826          for line in text(proc.stdout).splitlines():
  827              key, separator, value = line.partition("=")
  828              require(separator and key in properties and key not in fields)
  829              fields[key] = value
  830          if fields.get("LoadState") == "not-found":
  831              continue
  832          require(proc.returncode == 0 and set(fields) == set(properties))
  833          require(fields["Id"] in names and fields["LoadState"] == "loaded" and
  834                  fields["Type"] == "oneshot" and fields["Result"] == "success" and
  835                  fields["ConditionResult"] == "yes" and
  836                  fields["ExecMainCode"] == "1" and fields["ExecMainStatus"] == "0")
  837          require((fields["ActiveState"], fields["SubState"]) in
  838                  (("active", "exited"), ("inactive", "dead")))
  839          require(re.search(r"/usr/bin/autostart(?:[\s;\"']|$)", fields["ExecStart"]))
  840          start = int(fields["ExecMainStartTimestampMonotonic"])
  841          end = int(fields["ExecMainExitTimestampMonotonic"])
  842          uptime = float(Path("/proc/uptime").read_text().split()[0]) * 1000000
  843          require(0 < start <= end <= uptime)
  844          completed.add(fields["Id"])
  845      # Aliases may resolve to the same Id. Two distinct runners need investigation.
  846      require(len(completed) == 1)
  847      with Path("/proc/self/mountinfo").open() as stream:
  848          mounts = stream.read(1024 * 1024 + 1)
  849      require(len(mounts) <= 1024 * 1024)
  850      points = {line.split()[4] for line in mounts.splitlines()}
  851      require({"/storage", "/storage/roms"} <= points)
  852      require(Path("/var/lock/start.games").is_file())
  853      frontend = 0
  854      for process in Path("/proc").iterdir():
  855          if process.name.isdigit():
  856              try:
  857                  frontend += os.readlink(process / "exe") == "/usr/bin/emulationstation"
  858              except FileNotFoundError:  # an unrelated process exited during listing
  859                  continue
  860      require(frontend == 1)
  861      require(Path("/proc/sys/kernel/random/boot_id").read_text().strip() == boot)
  862      return boot
  863  
  864  
  865  class Parser(argparse.ArgumentParser):
  866      def error(self, message):
  867          # argparse normally echoes supplied argument values.
  868          raise Invalid()
  869  
  870  
  871  def main():
  872      parser = Parser(description=__doc__)
  873      group = parser.add_mutually_exclusive_group(required=True)
  874      group.add_argument("--root", type=Path)
  875      group.add_argument("--payload", type=Path)
  876      parser.add_argument("--mode", choices=("clean-image", "first-boot", "retained-upgrade"))
  877      parser.add_argument("--require-ready", action="store_true",
  878                          help="require completed boot, mounted storage and live ES; only for --root / --mode first-boot")
  879      failure_category = "input-invalid"
  880      try:
  881          args = parser.parse_args()
  882          require((args.root is not None and args.mode is not None) or
  883                  (args.payload is not None and args.mode in (None, "clean-image")))
  884          boot = None
  885          if args.require_ready:
  886              require(args.root == Path("/") and args.mode == "first-boot")
  887              failure_category = "boot-not-ready"
  888              boot = first_boot_ready()
  889              failure_category = "input-invalid"
  890          result = (Check(Local(args.root), args.mode).run() if args.root is not None
  891                    else payload(args.payload))
  892          if boot is not None:
  893              failure_category = "boot-not-ready"
  894              require(Path("/proc/sys/kernel/random/boot_id").read_text().strip() == boot)
  895              result["checks"].append({"path": "<first-boot-readiness>", "category": "boot-ready",
  896                                       "status": "clear", "present": True, "count": 0})
  897      except Exception:
  898          # Privacy boundary: neither parser messages nor unexpected reader errors
  899          # may serialize input values. A bug here must refuse, never emit a traceback.
  900          result = {"schema": 1, "policy": POLICY, "status": "error",
  901                    "error_count": 1, "checks": [{"path": "<input>", "category": failure_category,
  902                                                  "status": "error", "count": 0}],
  903                    "scope": SCOPE, "limitations": LIMITATIONS}
  904      print(json.dumps(result, sort_keys=True, indent=2))
  905      return {"pass": 0, "blocked": 1, "error": 2}[result["status"]]
  906  
  907  
  908  if __name__ == "__main__":
  909      sys.exit(main())
```

## File: tools/settings-modes-test (at 8ebaf8daad, 44 lines)

```text
    1  #!/usr/bin/env python3
    2  """#421: real shell writer functions, scratch paths, candidate busybox applets."""
    3  import argparse, hashlib, json, os, re, shutil, subprocess, tempfile
    4  from pathlib import Path
    5  p=argparse.ArgumentParser();p.add_argument('--profile',type=Path,required=True);p.add_argument('--chksysconfig',type=Path,required=True);p.add_argument('--busybox',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    6  fn=a.profile.read_text();ck=a.chksysconfig.read_text();rows=[]
    7  with tempfile.TemporaryDirectory(prefix='pixelelated-settings-modes-') as tmp:
    8   root=Path(tmp);bb=root/'busybox';shutil.copy2(a.busybox,bb);bin=root/'bin';bin.mkdir()
    9   for applet in ['stat','chmod','cp','mv','awk','sed','head','tail','wc','tr','cut']:
   10    f=bin/applet;f.write_text('#!/bin/sh\nexec '+str(bb)+' '+applet+' "$@"\n');f.chmod(0o755)
   11   functions='\n'.join(re.findall(r'^function \w+\(\) \{.*?^\}',fn,re.M|re.S))
   12   functions+='\n'+'\n'.join(re.findall(r'^\w+\(\) \{.*?^\}',ck,re.M|re.S))
   13   for operation in ['set_setting','set_settings','del_setting','sort_settings','backup','restore']:
   14    for scenario in ['private_live','private_record','wide_temp','restricted_group']:
   15     case=root/(operation+'-'+scenario);configroot=case/'config';cfgdir=configroot/'system/configs';cfgdir.mkdir(parents=True)
   16     live=cfgdir/'system.cfg';record=Path(str(live)+'.backup')
   17     original=b'system.hostname=qa\nqa.setting=older\nqa.keep=kept\n';oldrecord=b'system.hostname=qa\nqa.setting=record\nqa.keep=kept\n'
   18     live.write_bytes(original);record.write_bytes(oldrecord)
   19     live.chmod(0o644 if scenario=='private_record' else 0o660 if scenario=='restricted_group' else 0o600)
   20     record.chmod(0o644 if scenario=='private_live' else 0o640 if scenario=='restricted_group' else 0o600)
   21     expectedmode=0o640 if scenario=='restricted_group' else 0o600
   22     if scenario=='wide_temp':
   23      for f in [Path(str(live)+'.tmp'),Path(str(record)+'.tmp')]:f.write_bytes(b'stale\n');f.chmod(0o666)
   24     commands={'set_setting':'set_setting qa.setting newer','set_settings':'set_settings qa.setting newer qa.other second','del_setting':'del_setting qa.setting','sort_settings':'sort_settings','backup':'backup','restore':'restore'}
   25     setup=functions.replace('/storage/.config',str(configroot))+f'\nJ_CONF="{live}"; J_CONF_LOCK="{case}/lock"; CFG="{live}"; BACKUP="{record}"; logger() {{ :; }}\numask 022\n'
   26     result=subprocess.run(['bash','-c',setup+commands[operation]],capture_output=True,text=True,timeout=15,env={**os.environ,'PATH':str(bin)+':/usr/bin:/bin'})
   27     target=record if operation=='backup' else live
   28     expected=oldrecord if operation=='restore' else original if operation=='backup' else b''.join(sorted(original.splitlines(keepends=True))) if operation=='sort_settings' else original.replace(b'qa.setting=older\n',b'')+(b'qa.setting=newer\n'+(b'qa.other=second\n' if operation=='set_settings' else b'') if operation!='del_setting' else b'')
   29     okay=result.returncode==0 and target.read_bytes()==expected and target.stat().st_mode&0o777==expectedmode
   30     rows.append({'case':case.name,'pass':okay,'rc':result.returncode,'expected_mode':oct(expectedmode),'actual_mode':oct(target.stat().st_mode&0o777),'bytes_match':target.read_bytes()==expected})
   31     print(('PASS ' if okay else 'FAIL ')+case.name,flush=True)
   32   # Every refused staging action leaves the published file and other file intact.
   33   for fault in ['symlink','chmod','stat','producer','rename']:
   34    case=root/('refuse-'+fault);configroot=case/'config';cfgdir=configroot/'system/configs';cfgdir.mkdir(parents=True)
   35    live=cfgdir/'system.cfg';live.write_bytes(b'system.hostname=qa\nqa.setting=older\n');live.chmod(0o600);original=live.read_bytes();victim=case/'other';victim.write_bytes(b'unchanged\n')
   36    if fault=='symlink':Path(str(live)+'.tmp').symlink_to(victim)
   37    injected={'symlink':'','chmod':'chmod() { return 1; }','stat':'stat() { return 1; }','producer':'settings_base() { printf "system.hostname=qa\\n"; return 1; }','rename':'mv() { return 1; }'}[fault]
   38    setup=functions.replace('/storage/.config',str(configroot))+f'\nJ_CONF="{live}"; J_CONF_LOCK="{case}/lock"; logger() {{ :; }}\numask 022\n'+injected+'\n'
   39    command='sort_settings' if fault=='rename' else 'set_setting qa.setting newer'
   40    result=subprocess.run(['bash','-c',setup+command],capture_output=True,text=True,timeout=15,env={**os.environ,'PATH':str(bin)+':/usr/bin:/bin'})
   41    okay=result.returncode!=0 and not live.is_symlink() and live.read_bytes()==original and live.stat().st_mode&0o777==0o600 and victim.read_bytes()==b'unchanged\n'
   42    rows.append({'case':'refuse-'+fault,'pass':okay,'rc':result.returncode});print(('PASS ' if okay else 'FAIL ')+'refuse-'+fault,flush=True)
   43  report={'pass':all(x['pass'] for x in rows),'checks':rows,'profile_sha256':hashlib.sha256(a.profile.read_bytes()).hexdigest(),'chksysconfig_sha256':hashlib.sha256(a.chksysconfig.read_bytes()).hexdigest(),'busybox_sha256':hashlib.sha256(a.busybox.read_bytes()).hexdigest()}
   44  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');raise SystemExit(0 if report['pass'] else 1)
```

## File: tools/melonds-upgrade-test (at 8ebaf8daad, 125 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  """#526: preserve melonDS configuration while adding missing hotkey defaults.
    4  
    5  Runs the actual post-update function with owned paths and candidate BusyBox
    6  applets. An older post-update runs its exact legacy tail with those paths
    7  relocated into the fixture; its failures are discriminating negative controls.
    8  """
    9  import argparse
   10  import hashlib
   11  import json
   12  import os
   13  from pathlib import Path
   14  import re
   15  import shlex
   16  import shutil
   17  import subprocess
   18  import tempfile
   19  
   20  
   21  def main():
   22      parser = argparse.ArgumentParser(description=__doc__)
   23      parser.add_argument('--post-update', required=True, type=Path)
   24      parser.add_argument('--busybox', required=True, type=Path)
   25      parser.add_argument('--output', required=True, type=Path)
   26      args = parser.parse_args()
   27      source = args.post_update.read_text()
   28      function = re.search(r'^update_melonds_hotkeys\(\) \{.*?^\}', source, re.M | re.S)
   29      legacy = re.search(r'^rm -rf /storage/\.config/melonDS\ncp -r /usr/config/melondDS /storage/\.config/\s*$', source, re.M)
   30      if not function and not legacy:
   31          parser.error('no recognized current function or historical update block')
   32      rows = []
   33      cases = ['missing-defaults', 'missing-config', 'empty-defaults', 'add-missing',
   34               'already-current', 'no-final-newline', 'empty-config', 'file-link',
   35               'directory-link', 'whitespace-key', 'non-hotkey-defaults',
   36               'copy-failure', 'producer-failure', 'rename-failure', 'temp-failure']
   37      with tempfile.TemporaryDirectory(prefix='pixelelated-melonds-') as temporary:
   38          root = Path(temporary)
   39          busybox = root / 'busybox'
   40          shutil.copy2(args.busybox, busybox)
   41          binary = root / 'bin'
   42          binary.mkdir()
   43          for applet in ['mktemp', 'cp', 'awk', 'mv', 'rm']:
   44              wrapper = binary / applet
   45              wrapper.write_text('#!/bin/sh\nexec ' + shlex.quote(str(busybox)) + ' ' + applet + ' "$@"\n')
   46              wrapper.chmod(0o700)
   47          for name in cases:
   48              case = root / (name + ' with spaces')
   49              defaults = case / 'usr/config/melonDS/melonDS.ini'
   50              config = case / 'storage/.config/melonDS/melonDS.ini'
   51              defaults.parent.mkdir(parents=True)
   52              config.parent.mkdir(parents=True)
   53              defaults.write_text('HKKey_New=-1\nHKJoy_Custom=5\nHKJoy_New=4\nScreenLayout=2\n')
   54              original = '# owner settings\nHKJoy_Custom=99\nScreenLayout=7\nOwnerUnknown=yes\n'
   55              config.write_text(original)
   56              config.chmod(0o600)
   57              sentinel = config.parent / 'owner-extra.txt'
   58              sentinel.write_text('keep extra file\n')
   59              expected = original + 'HKKey_New=-1\nHKJoy_New=4\n'
   60              injected = ''
   61              expected_rc = 0
   62              if name == 'missing-defaults':
   63                  defaults.unlink(); expected = original
   64              elif name == 'missing-config':
   65                  config.unlink(); expected = None
   66              elif name == 'empty-defaults':
   67                  defaults.write_text(''); expected = original
   68              elif name == 'already-current':
   69                  config.write_text(expected); original = expected
   70              elif name == 'no-final-newline':
   71                  config.write_text(original.rstrip('\n'))
   72              elif name == 'empty-config':
   73                  config.write_text(''); expected = 'HKKey_New=-1\nHKJoy_Custom=5\nHKJoy_New=4\n'
   74              elif name == 'file-link':
   75                  target = case / 'owner-target.ini'; config.rename(target); config.symlink_to(target); expected = original
   76              elif name == 'directory-link':
   77                  target = case / 'owner-directory'; config.parent.rename(target); config.parent.symlink_to(target); expected = original
   78              elif name == 'whitespace-key':
   79                  original = original.replace('HKJoy_Custom=99', ' HKJoy_Custom = 99')
   80                  config.write_text(original); expected = original + 'HKKey_New=-1\nHKJoy_New=4\n'
   81              elif name == 'non-hotkey-defaults':
   82                  defaults.write_text('ScreenLayout=2\n'); config.write_text(original.rstrip('\n')); expected = original.rstrip('\n')
   83              elif name.endswith('-failure'):
   84                  injected = {'copy-failure': 'cp() { return 1; }',
   85                              'producer-failure': 'awk() { printf "partial output\\n"; return 1; }',
   86                              'rename-failure': 'mv() { return 1; }',
   87                              'temp-failure': 'mktemp() { return 1; }'}[name]
   88                  expected = original; expected_rc = 1
   89              inode = config.stat().st_ino if config.exists() else None
   90              if function:
   91                  command = function.group() + '\n' + injected + '\nupdate_melonds_hotkeys ' + shlex.quote(str(defaults)) + ' ' + shlex.quote(str(config))
   92              else:
   93                  command = legacy.group().replace('/storage/', shlex.quote(str(case / 'storage')) + '/').replace('/usr/config/', shlex.quote(str(case / 'usr/config')) + '/')
   94              result = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
   95                                      timeout=15, env={**os.environ, 'PATH': str(binary) + ':/usr/bin:/bin'})
   96              actual = config.read_text() if config.exists() else None
   97              okay = result.returncode == expected_rc and actual == expected
   98              okay = okay and sentinel.exists() and sentinel.read_text() == 'keep extra file\n'
   99              okay = okay and not list(config.parent.glob('melonDS.ini.??????'))
  100              if config.exists():
  101                  okay = okay and config.stat().st_mode & 0o777 == 0o600
  102              if name == 'file-link':
  103                  okay = okay and config.is_symlink()
  104              if name == 'directory-link':
  105                  okay = okay and config.parent.is_symlink()
  106              if name in ['already-current', 'non-hotkey-defaults'] and config.exists():
  107                  okay = okay and config.stat().st_ino == inode
  108              if okay and name == 'add-missing':
  109                  after = config.stat().st_ino
  110                  repeat = subprocess.run(['bash', '-c', command], capture_output=True, text=True,
  111                                          timeout=15, env={**os.environ, 'PATH': str(binary) + ':/usr/bin:/bin'})
  112                  okay = repeat.returncode == 0 and config.read_text() == expected and config.stat().st_ino == after
  113              rows.append({'case': name, 'pass': okay, 'rc': result.returncode, 'stderr': result.stderr})
  114              print(('PASS ' if okay else 'FAIL ') + name, flush=True)
  115      report = {'pass': all(row['pass'] for row in rows), 'checks': rows,
  116                'legacy_negative_control': not bool(function),
  117                'post_update_sha256': hashlib.sha256(args.post_update.read_bytes()).hexdigest(),
  118                'busybox_sha256': hashlib.sha256(args.busybox.read_bytes()).hexdigest()}
  119      args.output.parent.mkdir(parents=True, exist_ok=True)
  120      args.output.write_text(json.dumps(report, indent=2) + '\n')
  121      return 0 if report['pass'] else 1
  122  
  123  
  124  if __name__ == '__main__':
  125      raise SystemExit(main())
```

## File: tools/build-identity-test (at 8ebaf8daad, 183 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present pixelelated
    4  """Exercise actual assembly identity blocks and offline release planning (#532).
    5  
    6  Only synthetic Git repositories, tiny firmware stand-ins and temporary outputs.
    7  No image build, tag, network, device or cloud action is performed.
    8  """
    9  import argparse
   10  import hashlib
   11  import json
   12  import os
   13  from pathlib import Path
   14  import shutil
   15  import subprocess
   16  import tempfile
   17  
   18  
   19  def main():
   20      parser = argparse.ArgumentParser(description=__doc__)
   21      parser.add_argument('--output', type=Path, required=True)
   22      args = parser.parse_args()
   23      if args.output.exists():
   24          parser.error('output already exists; retain original results')
   25      root = Path(__file__).resolve().parents[1]
   26      checks, examples = [], {}
   27  
   28      def run(argv, **kw):
   29          return subprocess.run(argv, text=True, capture_output=True, timeout=30, **kw)
   30  
   31      def check(name, condition):
   32          checks.append({'name': name, 'passed': bool(condition)})
   33          if not condition:
   34              raise AssertionError(name)
   35  
   36      def sha(p):
   37          return hashlib.sha256(p.read_bytes()).hexdigest()
   38  
   39      def require(argv, **kw):
   40          result = run(argv, **kw)
   41          if result.returncode:
   42              raise RuntimeError(result.stderr)
   43          return result.stdout
   44  
   45      try:
   46          with tempfile.TemporaryDirectory(prefix='pix-build-identity-') as temp:
   47              work = Path(temp)
   48              repo = work / 'repo'
   49              (repo / 'config').mkdir(parents=True)
   50              shutil.copyfile(root / 'config/build-identity', repo / 'config/build-identity')
   51              require(['git', 'init', '-q', str(repo)])
   52              require(['git', '-C', str(repo), 'add', '.'])
   53              require(['git', '-C', str(repo), '-c', 'user.name=QA', '-c',
   54                       'user.email=qa@example.invalid', 'commit', '-qm', 'Synthetic fixture'])
   55              require(['git', '-C', str(repo), 'remote', 'add', 'origin',
   56                       'https://github.com/pixelelated/distribution.git'])
   57              commit = require(['git', '-C', str(repo), 'rev-parse', 'HEAD']).strip()
   58              env = os.environ.copy()
   59              for name in ('BUILD_QUALIFIER', 'BUILD_TIMESTAMP', 'CUSTOM_GIT_HASH',
   60                           'CUSTOM_VERSION', 'CUSTOM_IMAGE_NAME'):
   61                  env.pop(name, None)
   62              env.update(ROOT=str(repo), OS_VERSION='0.0.1', BUILD_TIMESTAMP='20261011T120000Z',
   63                         DEVICE='H700', PROJECT='ROCKNIX', TARGET_ARCH='aarch64',
   64                         DISTRONAME='pixelelated', IMAGE_SUFFIX='from-ROCKNIX',
   65                         HOME_URL='https://pixelelated.com', GIT_ORGANIZATION='pixelelated',
   66                         GIT_REPO='distribution', ARCH='aarch64')
   67              identity = '. config/build-identity; pixelelated_build_identity || exit $?; '
   68              identity += "python3 -c 'import json,os; print(json.dumps({k:os.environ[k] for k in "
   69              identity += '("RELEASE_VERSION","BUILD_VERSION","BUILD_DATE","BUILD_TIMESTAMP","BUILD_DIRTY","GIT_HASH","OS_BUILD")}))' + "'"
   70  
   71              def derive(**changes):
   72                  return run(['bash', '-c', identity], cwd=repo, env={**env, **changes})
   73  
   74              default = derive()
   75              check('engineering default dev', default.returncode == 0 and
   76                    json.loads(default.stdout)['RELEASE_VERSION'] == '0.0.1-dev')
   77              for qualifier in ('alpha.1', 'beta.1', 'rc', 'rc.0', 'rc.01', 'rc.-1',
   78                                'rc.1.2', 'rc.1+extra', 'stable', 'bad/'):
   79                  check('reject qualifier ' + qualifier, derive(BUILD_QUALIFIER=qualifier).returncode != 0)
   80              for changes in ({'OS_VERSION': '01.0.1'}, {'BUILD_TIMESTAMP': '20260230T120000Z'},
   81                              {'CUSTOM_VERSION': 'bad'}, {'CUSTOM_IMAGE_NAME': 'bad'},
   82                              {'CUSTOM_GIT_HASH': 'a' * 40}):
   83                  check('reject override ' + repr(changes), derive(**changes).returncode != 0)
   84              (repo / 'dirty').write_text('untracked')
   85              check('dirty build identified', json.loads(derive().stdout)['BUILD_VERSION'].endswith('.dirty'))
   86              (repo / 'dirty').unlink()
   87  
   88              image = (root / 'scripts/image').read_text()
   89              block = image[image.index('# One identity'):image.index('# Setup fakeroot')]
   90              sidecar = image[image.index('# Record the identity'):image.index('# Create legacy sym links')]
   91              metadata = image[image.index('# Create /etc/os-release'):image.index('if [ -n "${HW_CPU}" ]')]
   92              prefix = 'die(){ echo "$*" >&2; exit 1; }; show_config(){ :; };\n'
   93  
   94              def bundle(stage):
   95                  manifest = {'schema': 1, 'inputs': {'distribution_commit': commit},
   96                              'files': {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
   97                                        for p in stage.iterdir() if p.is_file()}}
   98                  (stage / 'manifest.json').write_text(json.dumps(manifest, sort_keys=True))
   99                  destination = work / sha(stage / 'manifest.json')
  100                  stage.rename(destination)
  101                  return destination
  102  
  103              def plan(path):
  104                  return run([str(root / 'tools/fork-publish-release'), '--prepare', str(path)])
  105  
  106              bundles = {}
  107              for label, q, stamp, version in (
  108                      ('rc1', 'rc.1', '20261011T120000Z', '0.0.1'),
  109                      ('rc2', 'rc.2', '20261011T120001Z', '0.0.1'),
  110                      ('release', '', '20261011T130000Z', '0.0.1'),
  111                      ('patch', '', '20261011T140000Z', '0.0.2'),
  112                      ('dev', 'dev', '20261011T150000Z', '0.0.1')):
  113                  stage = work / label
  114                  (stage / 'etc').mkdir(parents=True)
  115                  case_env = {**env, 'BUILD_QUALIFIER': q, 'BUILD_TIMESTAMP': stamp,
  116                              'OS_VERSION': version, 'BUILD': str(stage),
  117                              'TARGET_IMG': str(stage), 'INSTALL': str(stage)}
  118                  script = prefix + block + sidecar + metadata
  119                  require(['bash', '-c', script], cwd=repo, env=case_env)
  120                  files = list(stage.glob('*.identity.json'))
  121                  check(label + ' one sidecar', len(files) == 1)
  122                  item = json.loads(files[0].read_text())
  123                  release = version + ('-' + q if q else '')
  124                  build = release + '+' + stamp + '.g' + commit[:12]
  125                  base = 'pixelelated-H700.aarch64-' + build + '-from-ROCKNIX'
  126                  fields = dict(line.split('=', 1) for line in (stage / 'etc/os-release').read_text().splitlines())
  127                  check(label + ' actual filename and sidecar', item['release_version'] == release and
  128                        item['build_version'] == build and item['image_name'] == base and files[0].name == base + '.identity.json')
  129                  check(label + ' installed metadata contract', fields['OS_VERSION'] == '"' + release + '"' and
  130                        fields['BUILD_VERSION'] == '"' + build + '"' and fields['BUILD_ID'] == '"' + commit + '"')
  131                  firmware = stage / (base + '-DDR4.img.gz')
  132                  firmware.write_bytes(b'SYNTHETIC FIRMWARE ONLY\n' + (stage / 'etc/os-release').read_bytes())
  133                  before = sha(firmware)
  134                  collision = run(['bash', '-c', prefix + block], cwd=repo, env=case_env)
  135                  check(label + ' duplicate output refused without replacement', collision.returncode != 0 and sha(firmware) == before)
  136                  (stage / (firmware.name + '.sha256')).write_text(before + '  ' + firmware.name + '\n')
  137                  metadata_text = (stage / 'etc/os-release').read_text()
  138                  shutil.rmtree(stage / 'etc')  # the candidate store accepts flat files only
  139                  path = bundle(stage)
  140                  bundles[label] = path
  141                  result = plan(path)
  142                  if q == 'dev':
  143                      check('engineering public plan refused', result.returncode != 0)
  144                      continue
  145                  check(label + ' public plan accepted: ' + result.stderr.strip(), result.returncode == 0)
  146                  data = json.loads(result.stdout)
  147                  check(label + ' thin tag/title and prerelease', data['tag'] == 'v' + release and
  148                        data['title'] == 'pixelelated ' + release and data['prerelease'] == bool(q))
  149                  check(label + ' bound draft only', data['target_commitish'] == commit and data['draft'] and
  150                        not data['publication_performed'] and data['qualification'] == 'not assessed')
  151                  examples[label] = {'identity': item, 'os_release': metadata_text,
  152                                     'plan': data, 'synthetic_firmware_sha256': before}
  153              check('same-day RC identities distinct', examples['rc1']['identity']['build_version'] != examples['rc2']['identity']['build_version'])
  154              check('release reassembly changes bytes and manifest', examples['rc1']['synthetic_firmware_sha256'] != examples['release']['synthetic_firmware_sha256'] and bundles['rc1'].name != bundles['release'].name)
  155              # A renamed/retagged identity and unbound/modified bytes cannot pass.
  156              for label, mutate in (
  157                      ('relabeled RC as release', lambda s: next(s.glob('*.identity.json')).write_text(json.dumps({**examples['rc1']['identity'], 'release_version': '0.0.1'}))),
  158                      ('unsupported alpha public version', lambda s: next(s.glob('*.identity.json')).write_text(json.dumps({**examples['rc1']['identity'], 'release_version': '0.0.1-alpha.1'}))),
  159                      ('bad checksum', lambda s: next(s.glob('*.sha256')).write_text('wrong\n')),
  160                      ('unbound firmware', lambda s: (s / 'extra.tar').write_bytes(b'wrong'))):
  161                  stage = work / ('bad-' + str(len(checks)))
  162                  shutil.copytree(bundles['rc1'], stage)
  163                  (stage / 'manifest.json').unlink()
  164                  mutate(stage)
  165                  check(label + ' refused', plan(bundle(stage)).returncode != 0)
  166              next(bundles['rc1'].glob('*.img.gz')).write_bytes(b'TAMPER')
  167              check('modified bundle refused', plan(bundles['rc1']).returncode != 0)
  168      except Exception as error:
  169          checks.append({'name': 'harness completed', 'passed': False, 'error': str(error)})
  170      report = {'checks': checks, 'passed': sum(c['passed'] for c in checks),
  171                'failed': sum(not c['passed'] for c in checks), 'examples': examples,
  172                'synthetic_only': True, 'assembled_image_tested': False,
  173                'source_sha256': {name: sha(root / name) for name in
  174                                  ('config/build-identity', 'scripts/image', 'tools/fork-publish-release', 'tools/build-identity-test')}}
  175      with args.output.open('x') as stream:
  176          json.dump(report, stream, indent=2)
  177          stream.write('\n')
  178      print(f"{'FAIL' if report['failed'] else 'PASS'} build identity: {report['passed']} passed, {report['failed']} failed")
  179      return int(bool(report['failed']))
  180  
  181  
  182  if __name__ == '__main__':
  183      raise SystemExit(main())
```

## File: tools/nova-led-test (at 8ebaf8daad, 68 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """#332: real Nova scripts with only profile/path/service boundaries adapted."""
    5  from pathlib import Path
    6  import os
    7  import argparse
    8  import subprocess
    9  import sys
   10  import tempfile
   11  
   12  parser = argparse.ArgumentParser(description=__doc__)
   13  parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[1])
   14  args = parser.parse_args()
   15  repo = args.source_root.resolve()
   16  source = repo/'projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin'
   17  failed = 0
   18  checked = 0
   19  with tempfile.TemporaryDirectory(prefix='m7-nova-led-') as temp:
   20      root=Path(temp); settings=root/'settings'; settings.touch()
   21      led=root/'sys'; battery=root/'battery'; battery.mkdir()
   22      (battery/'capacity').write_text('75\n'); (battery/'status').write_text('Discharging\n')
   23      dirs=[]
   24      for side in 'lr':
   25          for n in range(1,5):
   26              d=led/f'multi-led{side}{n}/leds/rgb:{side}{n}'; d.mkdir(parents=True); dirs.append(d)
   27              (d/'brightness').write_text('0\n'); (d/'multi_intensity').write_text('0 0 0\n')
   28      profile=root/'profile'
   29      profile.write_text('''get_setting() { grep -F "$1=" "$QA_SETTINGS" | tail -1 | cut -d= -f2-; }
   30  set_setting() { printf '%s=%s\\n' "$1" "$2" >> "$QA_SETTINGS"; }
   31  systemctl() { [ "$*" = "restart batteryledstatus.service" ] || return 9; bash "$QA_ROOT/battery_led_status"; }
   32  sleep() { cat "$LED_PATH"/multi-*/leds/*/brightness >> "$QA_ROOT/sleep-brightness"; QA_SLEEP_COUNT=$((${QA_SLEEP_COUNT:-0}+1)); [ "$QA_SLEEP_COUNT" -lt "${QA_SLEEP_STEPS:-1}" ] || exit 0; }
   33  ''')
   34      for name in ['ledcontrol','analog_sticks_ledcontrol','battery_led_status']:
   35          text=(source/name).read_text().replace('. /etc/profile',f'. "{profile}"')
   36          text=text.replace('/usr/bin/analog_sticks_ledcontrol',str(root/'analog_sticks_ledcontrol'))
   37          # Redirect immutable hardware paths only; run all production branches.
   38          text=text.replace('LED_PATH="/sys/devices/platform/"','LED_PATH="${LED_PATH:-/sys/devices/platform/}"')
   39          text=text.replace('/sys/class/power_supply/battery/',str(battery)+'/')
   40          (root/name).write_text(text); (root/name).chmod(0o755)
   41      env=dict(os.environ, LED_PATH=str(led), QA_ROOT=str(root), QA_SETTINGS=str(settings), BATTERY_PATH=str(battery))
   42      def set_setting(k,v):
   43          with settings.open('a') as f: f.write(f'{k}={v}\n')
   44      def values(field): return [p.joinpath(field).read_text().strip() for p in dirs]
   45      def check(label, test):
   46          global failed, checked
   47          checked+=1; ok=bool(test); failed+=not ok; print(('PASS ' if ok else 'FAIL ')+label)
   48      def run(*args):
   49          r=subprocess.run(['bash',str(root/'ledcontrol'),*args],env=env,text=True,capture_output=True,timeout=10)
   50          assert r.returncode==0,(args,r.stderr)
   51      for name,value in [('max','255'),('mid','128'),('min','32')]:
   52          run('brightness',name); check(f'{name}: all eight brightness files = {value}',values('brightness')==[value]*8)
   53      run('rgb'); check('unset custom RGB: actual helper writes white at saved min', values('brightness')==['32']*8 and values('multi_intensity')==['255 255 255']*8)
   54      set_setting('analogsticks.led','200 255 0 0 0 0 255'); run('rgb')
   55      check('explicit custom RGB tuple preserved',values('brightness')==['200']*8 and values('multi_intensity')==['255 0 0']*4+['0 0 255']*4)
   56      run('off'); check('off clears every brightness and color',values('brightness')==['0']*8 and values('multi_intensity')==['0 0 0']*8)
   57      for cap,status,color in [('75','Discharging','0 255 0'),('25','Discharging','0 20 255'),('35','Discharging','0 125 255'),('15','Discharging','0 0 255'),('50','Charging','0 20 255'),('98','Charging','0 255 0'),('5','Discharging','0 0 255')]:
   58          (battery/'capacity').write_text(cap+'\n'); (battery/'status').write_text(status+'\n')
   59          run('brightness','min'); run('battery')
   60          check(f'battery {cap}% {status}: saved min and expected color',values('brightness')==['32']*8 and values('multi_intensity')==[color]*8)
   61      # One complete critical-charge blink sequence: on/off five times.
   62      (battery/'capacity').write_text('5\n'); (battery/'status').write_text('Discharging\n')
   63      (root/'sleep-brightness').unlink(missing_ok=True)
   64      env['QA_SLEEP_STEPS']='10'; run('battery')
   65      blink=(root/'sleep-brightness').read_text().splitlines()
   66      check('critical battery: five min-brightness/on and zero/off pairs',blink==(['32']*8+['0']*8)*5)
   67  print(f'{checked-failed} PASS, {failed} FAIL')
   68  raise SystemExit(bool(failed))
```

## File: tools/pixelelated-cloud-folder-test (at 8ebaf8daad, 29 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Retired historical folder-contract control (#524 PL-002).
    5  
    6  This entrypoint tested implicit all-category seeding and derived sibling paths.
    7  Those contracts were removed by #508. It cannot qualify current source, even
    8  with --ref. No fixture or cloud operation starts from this retired entrypoint.
    9  
   10  Current host coverage: tools/pixelelated-cloud-validator-test with a fresh
   11  --output directory and package-pinned rclone 1.75.1 via --rclone.
   12  Current target qualification also uses tools/vm-qa, tools/cloud-round-trip and
   13  the cloud-folder flow in docs/pixelelated/cloud-folder-flow-review.md.
   14  
   15  Historical receipts stay unchanged. To reproduce one, use its exact recorded
   16  tool/source checkout; git history retains this entrypoint's original body.
   17  --help exits 0; every attempted run exits 2 before starting any work.
   18  """
   19  import sys
   20  
   21  
   22  def main():
   23      help_only = sys.argv[1:] in (["--help"], ["-h"])
   24      print(__doc__, file=sys.stdout if help_only else sys.stderr, end="")
   25      return 0 if help_only else 2
   26  
   27  
   28  if __name__ == "__main__":
   29      sys.exit(main())
```

## File: tools/pixelelated-cloud-folder-vm-test (at 8ebaf8daad, 30 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Retired historical folder-overlay control (#524 PL-002).
    5  
    6  This entrypoint overlaid the implicit-seeding/derived-pointer contract and
    7  omitted dependencies needed by current category validation. It cannot qualify
    8  current source. It never starts or reuses a guest, resets a backend, writes an
    9  owner directory, or treats an argument refusal as a passing negative case.
   10  
   11  Current target qualification uses tools/vm-qa and tools/cloud-round-trip with
   12  an owned current image, plus the source-bound cloud-folder cases documented in
   13  docs/pixelelated/cloud-folder-flow-review.md. The host category controls are in
   14  tools/pixelelated-cloud-validator-test; they do not claim VM qualification.
   15  
   16  Historical receipts stay unchanged. To reproduce one, use its exact recorded
   17  tool/source checkout; git history retains this entrypoint's original body.
   18  --help exits 0; every attempted run exits 2 before starting any work.
   19  """
   20  import sys
   21  
   22  
   23  def main():
   24      help_only = sys.argv[1:] in (["--help"], ["-h"])
   25      print(__doc__, file=sys.stdout if help_only else sys.stderr, end="")
   26      return 0 if help_only else 2
   27  
   28  
   29  if __name__ == "__main__":
   30      sys.exit(main())
```

## File: tools/pixelelated-duckstation-capture-test (at 8ebaf8daad, 361 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated
    4  """Exercise actual DuckStation launchers/configs in isolated host fixtures (#521).
    5  
    6  The AppImage boundary is a source-derived path/capture probe, not an emulator.
    7  Target-runtime screenshot proof is separate. Transfers use real package rclone.
    8  """
    9  import argparse
   10  import configparser
   11  import hashlib
   12  import json
   13  import os
   14  from pathlib import Path
   15  import shutil
   16  import subprocess
   17  import sys
   18  
   19  PACKAGE = Path('projects/ROCKNIX/packages/emulators/standalone/duckstation-sa')
   20  RULES = Path('projects/ROCKNIX/packages/network/rclone/sources/cloud_sync-rules.txt')
   21  DEFAULT = '/storage/roms/screenshots'
   22  LEGACY = '/storage/.config/duckstation/screenshots'
   23  
   24  
   25  def digest(data):
   26      return hashlib.sha256(data).hexdigest()
   27  
   28  
   29  def require(value, why):
   30      if not value:
   31          raise AssertionError(why)
   32  
   33  
   34  def put(path, data, mode=0o644):
   35      path.parent.mkdir(parents=True, exist_ok=True)
   36      path.write_bytes(data.encode() if isinstance(data, str) else data)
   37      path.chmod(mode)
   38  
   39  
   40  def inventory(root):
   41      result = {}
   42      for path in sorted(root.rglob('*')):
   43          if path.is_symlink():
   44              result[str(path.relative_to(root))] = {'link': os.readlink(path)}
   45          elif path.is_file():
   46              result[str(path.relative_to(root))] = {'bytes': path.stat().st_size,
   47                                                     'sha256': digest(path.read_bytes())}
   48      return result
   49  
   50  
   51  PROBE = '''#!/usr/bin/python3
   52  import configparser, json, os
   53  from pathlib import Path
   54  p=Path('/storage/.config/duckstation/settings.ini')
   55  c=configparser.ConfigParser(interpolation=None,strict=False)
   56  try:
   57   c.read(p)
   58   value=next((c[s].get('Screenshots','screenshots') for s in c.sections() if s.lower()=='folders'),'screenshots') or 'screenshots'
   59  except configparser.Error:
   60   value='screenshots'
   61  target=Path(value)
   62  if not target.is_absolute():target=p.parent/target
   63  receipt={'configured':value,'resolved':str(target.resolve()),'argv':__import__('sys').argv[1:]}
   64  Path('/ctl/probe.json').write_text(json.dumps(receipt))
   65  if os.environ.get('CAPTURE_PROBE')=='yes':
   66   target.mkdir(parents=True,exist_ok=True)
   67   (target/'synthetic-capture.png').write_bytes(b'fixture capture bytes, not a rendered image\\n')
   68  '''
   69  
   70  
   71  class Fixture:
   72      def __init__(self, args, name, entry='game', seed='InputPlumber'):
   73          self.args, self.path, self.seq = args, args.output/name, 0
   74          self.path.mkdir()
   75          for directory in ['source', 'storage/roms', 'storage/.config/duckstation', 'ctl', 'cloud']:
   76              (self.path/directory).mkdir(parents=True, exist_ok=True)
   77          self.entry = 'scripts/start_duckstation.sh' if entry == 'game' else 'sources/Start Duckstation.sh'
   78          self.source = {}
   79          for relative, target in [(self.entry, 'entry'), ('scripts/duckstation_screenshot_path', 'helper'),
   80                                   ('config/'+seed+'/settings.ini', 'seed')]:
   81              data = self.read_source(PACKAGE/relative, optional=target=='helper')
   82              if data is not None:
   83                  put(self.path/'source'/target, data, 0o755 if target != 'seed' else 0o644)
   84                  self.source[str(PACKAGE/relative)] = digest(data)
   85          rules = self.read_source(RULES)
   86          put(self.path/'source/rules', rules)
   87          self.source[str(RULES)] = digest(rules)
   88          put(self.path/'source/probe', PROBE, 0o755)
   89          put(self.path/'source/profile', '''export HOME=/storage PATH=/usr/bin:/bin
   90  set_kill() { :; }
   91  get_setting() { :; }
   92  fbwidth() { echo 640; }
   93  fbheight() { echo 480; }
   94  ''')
   95          put(self.path/'source/gamecontrollerdb.txt', 'synthetic controller database\n')
   96          # Existing launcher progress links are prepopulated so their unrelated
   97          # behavior cannot masquerade as screenshot migration preservation.
   98          for name, target in [('savestates','/storage/roms/savestates/psx'),
   99                               ('memcards','/storage/roms/psx/duckstation/memcards')]:
  100              put(self.guest(target)/'existing.bin', b'unselected progress\n')
  101              (self.path/'storage/.config/duckstation'/name).symlink_to(target)
  102          self.config = self.path/'storage/.config/duckstation/settings.ini'
  103          self.readonly = []
  104  
  105      def read_source(self, path, optional=False):
  106          if self.args.ref:
  107              result = subprocess.run(['git','-C',str(self.args.source_root),'show',self.args.ref+':'+str(path)],
  108                                      capture_output=True)
  109              if result.returncode and optional:
  110                  return None
  111              require(result.returncode == 0, 'missing source '+str(path))
  112              return result.stdout
  113          path = self.args.source_root/path
  114          if optional and not path.exists():
  115              return None
  116          return path.read_bytes()
  117  
  118      def guest(self, path):
  119          require(path.startswith('/storage/'), 'fixture path outside storage')
  120          return self.path/path.lstrip('/')
  121  
  122      def run(self, command=None, capture=False):
  123          cmd=['bwrap','--die-with-parent','--unshare-all','--new-session','--tmpfs','/',
  124               '--dir','/usr/bin','--symlink','usr/bin','/bin','--symlink','usr/lib','/lib']
  125          for directory in ['/usr/lib','/usr/lib64','/usr/share']:
  126              if Path(directory).exists():
  127                  cmd += ['--ro-bind',directory,directory]
  128          if Path('/usr/lib64').exists():
  129              cmd += ['--symlink','usr/lib64','/lib64']
  130          for binary in ['bash','env','mkdir','cp','rm','ln','sed','cat','install','python3']:
  131              source=Path(shutil.which(binary)).resolve()
  132              cmd += ['--ro-bind',str(source),'/usr/bin/'+binary]
  133          cmd += ['--ro-bind',str(self.path/'source/probe'),'/usr/bin/duckstation-sa',
  134                  '--ro-bind',str(self.path/'source/entry'),'/entry',
  135                  '--ro-bind',str(self.path/'source/profile'),'/etc/profile',
  136                  '--ro-bind',str(self.path/'source/seed'),'/usr/config/duckstation/settings.ini',
  137                  '--ro-bind',str(self.path/'source/gamecontrollerdb.txt'),'/usr/config/SDL-GameControllerDB/gamecontrollerdb.txt',
  138                  '--ro-bind',str(self.path/'source/rules'),'/rules',
  139                  '--ro-bind',str(self.args.rclone),'/rclone.real']
  140          if (self.path/'source/helper').exists():
  141              cmd += ['--ro-bind',str(self.path/'source/helper'),'/usr/bin/duckstation_screenshot_path']
  142          for directory in ['storage','ctl','cloud']:
  143              cmd += ['--bind',str(self.path/directory),'/'+directory]
  144          for directory in ['packagework','package-input']:
  145              if (self.path/directory).exists():
  146                  cmd += ['--bind',str(self.path/directory),'/'+directory]
  147          for path in self.readonly:
  148              cmd += ['--ro-bind',str(self.guest(path)),path]
  149          cmd += ['--dev','/dev','--proc','/proc','--tmpfs','/tmp','--chdir','/storage',
  150                  '--setenv','HOME','/storage','--setenv','PATH','/usr/bin:/bin',
  151                  '--setenv','CAPTURE_PROBE','yes' if capture else 'no']
  152          cmd += command or ['/bin/bash','/entry','/storage/roms/psx/fixture.chd','psx']
  153          before = inventory(self.path/'storage')
  154          result=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
  155          self.seq += 1
  156          receipt={'argv':cmd,'rc':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
  157                   'before':before,'after':inventory(self.path/'storage')}
  158          put(self.path/(str(self.seq).zfill(2)+'-operation.json'),json.dumps(receipt,indent=2)+'\n')
  159          require(result.returncode == 0, 'operation failed: '+result.stderr[-600:])
  160          return result
  161  
  162      def probe(self):
  163          return json.loads((self.path/'ctl/probe.json').read_text())
  164  
  165  
  166  def main():
  167      parser=argparse.ArgumentParser(description=__doc__)
  168      parser.add_argument('--source-root',type=Path,required=True)
  169      parser.add_argument('--ref')
  170      parser.add_argument('--rclone',type=Path,required=True)
  171      parser.add_argument('--output',type=Path,required=True)
  172      parser.add_argument('--cases')
  173      parser.add_argument('--keep-fixtures',action='store_true')
  174      args=parser.parse_args()
  175      args.source_root=args.source_root.resolve();args.rclone=args.rclone.resolve();args.output=args.output.resolve()
  176      args.output.mkdir(parents=True,exist_ok=False)
  177      version=subprocess.check_output([str(args.rclone),'version'],text=True).splitlines()[0]
  178      require(version == 'rclone v1.75.1','use package-pinned rclone: '+version)
  179      results=[];sources={}
  180  
  181      def case(name,test,entry='game',seed='InputPlumber'):
  182          if args.cases and name not in args.cases.split(','):
  183              return
  184          f=Fixture(args,name,entry,seed);sources.update(f.source)
  185          try:
  186              test(f)
  187              require(not list((f.path/'storage').rglob('.screenshots-*')),'partial config stage remained')
  188              results.append({'case':name,'result':'PASS'})
  189              print('PASS '+name,flush=True)
  190          except Exception as error:
  191              results.append({'case':name,'result':'FAIL','error':str(error)})
  192              print('FAIL '+name+': '+str(error),flush=True)
  193          finally:
  194              sources.update(f.source)
  195              put(f.path/'final.json',json.dumps({'storage':inventory(f.path/'storage'),
  196                  'cloud':inventory(f.path/'cloud'),'source_sha256':f.source},indent=2)+'\n')
  197              if not args.keep_fixtures:
  198                  retired=[]
  199                  for directory in ['storage','cloud','source','packagework','package-input']:
  200                      if (f.path/directory).exists():
  201                          shutil.rmtree(f.path/directory)
  202                          retired.append(directory)
  203                  put(f.path/'retired.json',json.dumps({'removed':retired})+'\n')
  204  
  205      def defaults(f, retained=None):
  206          if retained is not None:
  207              put(f.config,retained)
  208          put(f.guest(LEGACY)/'historical.png',b'old capture remains here\n')
  209          prior=inventory(f.path/'storage')
  210          f.run(capture=True)
  211          if f.probe()['resolved'] != DEFAULT:
  212              # The old-source control still reaches the actual allowlist copy:
  213              # retain evidence that its ordinary output is outside backup scope.
  214              f.run(['/rclone.real','copy','/storage/roms','/cloud','--filter-from','/rules'])
  215          require(f.probe()['resolved']==DEFAULT,'default capture remains outside save scope: '+str(f.probe()))
  216          after=inventory(f.path/'storage')
  217          for path, value in prior.items():
  218              if path != '.config/duckstation/settings.ini':
  219                  require(after.get(path)==value,'unselected file changed: '+path)
  220          config=f.config.read_bytes()
  221          f.run()
  222          require(f.config.read_bytes()==config,'second launch changed prepared configuration')
  223          f.run(['/rclone.real','copy','/storage/roms','/cloud','--filter-from','/rules'])
  224          captured=f.guest(DEFAULT)/'synthetic-capture.png'
  225          cloud=f.path/'cloud/screenshots/synthetic-capture.png'
  226          require(cloud.read_bytes()==captured.read_bytes(),'real rclone missed new default capture')
  227          require(not list((f.path/'cloud').rglob('historical.png')),'claimed historical captures automatically backed up')
  228          captured.unlink()
  229          f.run(['/rclone.real','copy','/cloud','/storage/roms','--filter-from','/rules'])
  230          require(captured.read_bytes()==cloud.read_bytes(),'capture restore changed bytes')
  231  
  232      for entry in ['game','tool']:
  233          for seed in ['InputPlumber','H700','AMD64']:
  234              case('clean-'+entry+'-'+seed,defaults,entry,seed)
  235          for label, conf in [('missing','[Main]\nPreserve = yes\n'),
  236                              ('empty','[Folders]\nScreenshots =\n'),
  237                              ('default','[Folders]\nScreenshots = screenshots\n'),
  238                              ('case-crlf','[folders]\r\nsCrEeNsHoTs = screenshots\r\nOther = keep\r\n')]:
  239              case('retained-'+entry+'-'+label,lambda f,c=conf:defaults(f,c),entry)
  240  
  241      def first_directory(f):
  242          shutil.rmtree(f.config.parent)
  243          f.run(capture=True)
  244          require(f.config.is_file() and f.probe()['resolved']==DEFAULT,'first configuration directory did not use covered default')
  245          config=f.config.read_bytes();f.run()
  246          require(f.config.read_bytes()==config,'repeated clean launch changed settings')
  247          f.run(['/rclone.real','copy','/storage/roms','/cloud','--filter-from','/rules'])
  248          require((f.path/'cloud/screenshots/synthetic-capture.png').read_bytes()==f.guest(DEFAULT).joinpath('synthetic-capture.png').read_bytes(),'first-directory capture missed backup')
  249      for entry in ['game','tool']:
  250          case('clean-directory-'+entry,first_directory,entry)
  251  
  252      def custom(f,value):
  253          content='[Folders]\nScreenshots = '+value+'\nOther = keep\n'
  254          put(f.config,content)
  255          target=value if value.startswith('/') else '/storage/.config/duckstation/'+value
  256          put(f.guest(target)/'historical.png','custom capture\n')
  257          before=inventory(f.path/'storage')
  258          f.run()
  259          require(f.config.read_text()==content,'custom setting rewritten')
  260          require(f.probe()['resolved']==target,'custom destination changed')
  261          after=inventory(f.path/'storage')
  262          require(all(after.get(k)==v for k,v in before.items()),'custom bytes changed')
  263      for entry in ['game','tool']:
  264          case('custom-absolute-'+entry,lambda f:custom(f,'/storage/custom-captures'),entry)
  265          case('custom-relative-'+entry,lambda f:custom(f,'other-captures'),entry)
  266  
  267      def old_link(f):
  268          put(f.config,'[Folders]\nScreenshots = screenshots\n')
  269          put(f.guest('/storage/custom-captures')/'old.png','custom symlink bytes\n')
  270          f.guest(LEGACY).symlink_to('/storage/custom-captures')
  271          before=f.config.read_bytes();f.run()
  272          require(f.config.read_bytes()==before and f.probe()['resolved']=='/storage/custom-captures','custom symlink overridden')
  273      case('custom-old-screenshot-symlink',old_link)
  274  
  275      def refused(f,kind):
  276          content='[Folders]\nScreenshots = screenshots\n'
  277          if kind=='duplicate':content+='Screenshots = /storage/custom\n'
  278          if kind=='duplicate-section':content+='[folders]\nScreenshots = screenshots\n'
  279          if kind=='oversize':content+=';'+'x'*(1024*1024)+'\n'
  280          put(f.config,content)
  281          put(f.guest(LEGACY)/'historical.png','retained capture\n')
  282          if kind=='file-target':put(f.guest(DEFAULT),'conflicting ordinary file\n')
  283          if kind=='symlink-target':
  284              f.guest('/storage/custom-captures').mkdir();f.guest(DEFAULT).symlink_to('/storage/custom-captures')
  285          if kind=='readonly-target':
  286              f.guest(DEFAULT).mkdir();f.readonly.append(DEFAULT)
  287          if kind=='readonly-config':f.readonly.append('/storage/.config/duckstation')
  288          if kind=='replace-failed':f.readonly.append('/storage/.config/duckstation/settings.ini')
  289          before=f.config.read_bytes()
  290          result=f.run()
  291          require(f.config.read_bytes()==before,'refused configuration changed')
  292          require("Couldn't prepare the screenshot folder" in result.stderr,'missing truthful refusal')
  293          require(f.guest(LEGACY).joinpath('historical.png').read_text()=='retained capture\n','old capture changed')
  294          # The emulator remains reachable; no coverage success is inferred.
  295          require((f.path/'ctl/probe.json').exists(),'failure blocked ordinary launch')
  296          f.run()
  297          require(f.config.read_bytes()==before,'repeated refusal changed configuration')
  298          if kind in ('readonly-config','replace-failed'):
  299              require(not f.guest(DEFAULT).exists(),'failed preparation left a new empty target')
  300      for kind in ['duplicate','duplicate-section','oversize','file-target','symlink-target','readonly-target','readonly-config','replace-failed']:
  301          case('refused-'+kind,lambda f,k=kind:refused(f,k))
  302  
  303      def nonregular(f):
  304          put(f.guest('/storage/custom-settings.ini'),'[Folders]\nScreenshots = screenshots\n')
  305          f.config.symlink_to('/storage/custom-settings.ini')
  306          before=f.guest('/storage/custom-settings.ini').read_bytes()
  307          # Tool entrypoint does not independently sed-edit config, isolating
  308          # the helper's refusal from existing game-launcher settings behavior.
  309          result=f.run()
  310          require(f.config.is_symlink() and f.guest('/storage/custom-settings.ini').read_bytes()==before,'nonregular config replaced')
  311          require("Couldn't prepare the screenshot folder" in result.stderr,'nonregular config not refused')
  312      case('refused-nonregular-config',nonregular,'tool')
  313  
  314      def package_install(f):
  315          package=f.path/'package-input'
  316          paths=['package.mk','scripts/start_duckstation.sh','sources/Start Duckstation.sh',
  317                 'config/InputPlumber/settings.ini','scripts/duckstation_screenshot_path']
  318          for relative in paths:
  319              data=f.read_source(PACKAGE/relative,optional=relative.endswith('duckstation_screenshot_path'))
  320              if data is not None:
  321                  put(package/relative,data,0o755 if relative.startswith('scripts/') else 0o644)
  322                  f.source[str(PACKAGE/relative)]=digest(data)
  323          (package/'config/GENERIC_X64').symlink_to('InputPlumber')
  324          app=f.path/'packagework/build/duckstation-sa-0.1-10998.AppImage'
  325          payload=b'#!/bin/sh\nprintf "%s\\n" synthetic-executable-permission-witness\n'
  326          put(app,payload,0o644)
  327          f.run(['/bin/bash','-c',
  328                 'export TARGET_ARCH=x86_64 DEVICE=GENERIC_X64 INSTALL=/packagework/install PKG_BUILD=/packagework/build PKG_DIR=/package-input; '
  329                 '. /package-input/package.mk; makeinstall_target'])
  330          installed=f.path/'packagework/install/usr/bin/duckstation-sa'
  331          require(app.stat().st_mode & 0o777 == 0o644,'source/cache mode changed')
  332          require(installed.read_bytes()==payload,'install altered AppImage bytes')
  333          try:
  334              execution=subprocess.run([str(installed)],capture_output=True,text=True,timeout=10)
  335              result={'rc':execution.returncode,'stdout':execution.stdout,'stderr':execution.stderr}
  336          except OSError as error:
  337              result={'errno':error.errno,'error':str(error)}
  338          put(f.path/'installed-execution.json',json.dumps({'source_mode':oct(app.stat().st_mode & 0o777),
  339              'installed_mode':oct(installed.stat().st_mode & 0o777),'sha256':digest(payload),'execution':result,
  340              'scope':'synthetic permission witness, not the AppImage runtime'},indent=2)+'\n')
  341          require(installed.stat().st_mode & 0o777 == 0o755,'installed AppImage is not executable0755')
  342          require(result.get('rc')==0 and 'synthetic-executable-permission-witness' in result.get('stdout',''),'installed direct execution failed')
  343          helper=f.path/'packagework/install/usr/bin/duckstation_screenshot_path'
  344          require(helper.is_file() and os.access(helper,os.X_OK),'screenshot helper not installed executable')
  345          require('Python3' in (package/'package.mk').read_text(),'runtime dependency absent')
  346      case('package-executable-mode',package_install)
  347  
  348      require(results,'no matching cases')
  349      summary={'passed':sum(r['result']=='PASS' for r in results),'failed':sum(r['result']=='FAIL' for r in results),
  350               'results':results,'source_ref':args.ref,'source_root':str(args.source_root),'source_sha256':sources,
  351               'harness_sha256':digest(Path(__file__).read_bytes()),
  352               'watcher_run':os.environ.get('RASTERATOPS_BUILD_RUN'),
  353               'rclone_sha256':digest(args.rclone.read_bytes()),'rclone_version':version,
  354               'scope':'actual shell entrypoints; synthetic emulator-boundary probe; no runtime screenshot claim'}
  355      put(args.output/'summary.json',json.dumps(summary,indent=2)+'\n')
  356      print(f"DuckStation captures: {summary['passed']} PASS, {summary['failed']} FAIL",flush=True)
  357      return bool(summary['failed'])
  358  
  359  
  360  if __name__=='__main__':
  361      sys.exit(main())
```

## File: tools/pixelelated-state-check-test (at 8ebaf8daad, 783 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present pixelelated
    4  """Disposable #565 controls. No imports of the gate, providers, or real accounts.
    5  
    6  --self-test runs root-policy subprocess controls. --payload-tests additionally
    7  creates tiny synthetic SYSTEM/update/install payloads and release bundles using
    8  installed filesystem tools (no distro build). Coordinator allocates these runs.
    9  --prepare-guest-script FILE only writes a first-boot read-only serial script.
   10  Fixtures are synthetic or public shipped defaults; no caller-supplied storage is seeded or cleaned.
   11  """
   12  import argparse
   13  import base64
   14  import gzip
   15  import hashlib
   16  import io
   17  import json
   18  import os
   19  from pathlib import Path
   20  import shutil
   21  import stat
   22  import subprocess
   23  import sys
   24  import tarfile
   25  import tempfile
   26  
   27  
   28  HERE = Path(__file__).resolve().parent
   29  GATE = HERE / "pixelelated-state-check"
   30  CANARY = "synthetic-" + "player-565-do-not-display"
   31  SCRUB_EPOCH = 2000000000  # synthetic clock, never the host/guest boot clock
   32  CLOUD = ('SAVESPATH="/storage/roms"\nSAVES_REMOTE="/pixelelated/Saves"\n'
   33           'SETTINGS_REMOTE="/pixelelated/Backups"\nCONTENT_REMOTE="/pixelelated/Content"\n'
   34           'RCLONEOPTS="--progress --filter-from /storage/.config/cloud_sync-rules.txt"\n')
   35  
   36  
   37  def require(ok):
   38      if not ok:
   39          raise RuntimeError("fixture assertion failed")
   40  
   41  
   42  def put(root, path, data):
   43      p = root / path.lstrip("/")
   44      p.parent.mkdir(parents=True, exist_ok=True)
   45      p.write_bytes(data.encode() if isinstance(data, str) else data)
   46      return p
   47  
   48  
   49  def clean(root, runtime=True):
   50      defaults = {
   51          "system/configs/system.cfg": 'global.retroachievements.username=\nglobal.retroachievements.password=\n',
   52          "emulationstation/es_settings.cfg": '<config/>\n',
   53          "retroarch/retroarch.cfg": 'cheevos_username = ""\ncheevos_password = ""\ncheevos_token = ""\n',
   54          "cloud_sync.conf": CLOUD,
   55      }
   56      for prefix in ("usr/config", "storage/.config") if runtime else ("usr/config",):
   57          for name, data in defaults.items():
   58              put(root, prefix + "/" + name, data)
   59      put(root, "usr/config/cloud_sync.conf.defaults",
   60          "".join("DEFAULT_" + line + "\n" for line in CLOUD.splitlines()))
   61      put(root, "etc/retroarch.cfg", 'video_driver = "gl"\n')
   62      # A parser fixture with an ELF header, not a functional ES executable.
   63      put(root, "usr/bin/emulationstation", b"\x7fELF\x02" + b"\0" * 59)
   64      if runtime:
   65          put(root, "storage/roms/synthetic/gamelist.xml",
   66              '<gameList><game><path>./synthetic.rom</path><name>Synthetic</name>'
   67              '<playcount>0</playcount></game></gameList>')
   68  
   69  
   70  def shipped_locale(root, first="/usr/share/locale", second="/storage/.config/locale"):
   71      # Exact ES post_install chain: absent storage target in an immutable SYSTEM.
   72      (root / "usr/share").mkdir(parents=True, exist_ok=True)
   73      (root / "usr/config/emulationstation/locale").symlink_to(first)
   74      (root / "usr/share/locale").symlink_to(second)
   75  
   76  
   77  def locale_target_escape(root):
   78      shipped_locale(root)
   79      (root / "storage/.config").mkdir(parents=True, exist_ok=True)
   80      (root / "storage/.config/locale").symlink_to("/../outside")
   81  
   82  
   83  def scrub_marker(root, first=SCRUB_EPOCH + 10, second=SCRUB_EPOCH + 11,
   84                   files1=0, lines1=0, files2=0, lines2=0, boot=True):
   85      if boot:
   86          put(root, "proc/stat", "cpu 0 0 0 0\nbtime " + str(SCRUB_EPOCH) + "\nprocesses 1\n")
   87          put(root, "proc/uptime", "100.00 175.00\n")
   88      return put(root, "storage/.cache/cloud_sync/log-scrubbed",
   89                 f"scrubbed={first} files={files1} lines={lines1}\n"
   90                 f"es_log_scrubbed={second} files={files2} lines={lines2}\n")
   91  
   92  
   93  def no_adapter_scrub(root, *, data=None, mtime=SCRUB_EPOCH + 9, **marker):
   94      scrub_marker(root, files1=1, **marker)
   95      # Public fixed diagnostic from cloud_device_id, with a synthetic calendar
   96      # value. Its file mtime, not the fixture host's timezone, binds the boot.
   97      normal = ("[2033-05-18 03:33:29] [INFO] [cloud_device_id] "
   98                "no stored id and no adapter to derive one from yet; not seeding the identity "
   99                "from machine-id at this caller's request (--if-present)\n")
  100      log = put(root, "storage/.cache/log/cloud_sync.log", normal if data is None else data)
  101      os.utime(log, ns=(mtime * 1000000000, mtime * 1000000000))
  102      return log
  103  
  104  
  105  def alter_scrub(root, rewrite):
  106      path = scrub_marker(root)
  107      path.write_text(rewrite(path.read_text()))
  108  
  109  
  110  def snapshot(root):
  111      # Compare synthetic fixture bytes directly in memory, never hash credentials.
  112      result = {}
  113      for p in root.rglob("*"):
  114          meta = p.lstat()
  115          if stat.S_ISLNK(meta.st_mode):
  116              value = os.readlink(p)
  117          elif stat.S_ISREG(meta.st_mode):
  118              value = p.read_bytes() if meta.st_mode & 0o444 else None
  119          else:
  120              value = None
  121          result[str(p.relative_to(root))] = (meta.st_mode, value)
  122      return result
  123  
  124  
  125  def invoke(args, expected, category=None, env=None):
  126      p = subprocess.run([sys.executable, "-B", str(GATE), *args], capture_output=True, timeout=45, env=env)
  127      require(p.returncode == expected and not p.stderr)
  128      output = p.stdout.decode()
  129      require(CANARY not in output)
  130      require(all(str(epoch) not in output for epoch in
  131                  (SCRUB_EPOCH, SCRUB_EPOCH + 10, SCRUB_EPOCH + 11)))
  132      report = json.loads(output)
  133      require(report["status"] == {0: "pass", 1: "blocked", 2: "error"}[expected])
  134      if category:
  135          require(any(row["category"] == category and row.get("count", 0) > 0
  136                      for row in report["checks"]))
  137      return report
  138  
  139  
  140  def root_controls(work):
  141      rows = []
  142      def case(name, mutate=None, expected=0, category=None, mode="first-boot", clear=None):
  143          root = work / name
  144          root.mkdir()
  145          clean(root)
  146          if mutate:
  147              mutate(root)
  148          before = snapshot(root)
  149          report = invoke(["--root", str(root), "--mode", mode], expected, category)
  150          if clear:
  151              require(any(row["category"] == clear and row["status"] == "clear" and
  152                          row["count"] == 0 and row["present"] for row in report["checks"]))
  153          require(snapshot(root) == before)
  154          rows.append({"case": name, "status": "pass", "state_unchanged": True})
  155  
  156      case("clean-first-boot")
  157      case("clean-image", mode="clean-image")
  158      comments = '# RetroArch defaults\n\n  # video_driver = "gl"\n# cheevos_token = "' + CANARY + '"\n'
  159      case("retroarch-comment-only-default", lambda r: put(r, "etc/retroarch.cfg", comments))
  160      case("retroarch-comment-only-image", lambda r: put(r, "etc/retroarch.cfg", comments), mode="clean-image")
  161      case("retroarch-comment-default-include", lambda r: put(r, "etc/retroarch.cfg",
  162           comments + '#include "/outside/' + CANARY + '"\n'), 2)
  163      case("retroarch-comment-default-reference", lambda r: put(r, "etc/retroarch.cfg",
  164           comments + '#reference "/outside/' + CANARY + '"\n'), 2)
  165      case("retroarch-comment-default-nul", lambda r: put(r, "etc/retroarch.cfg", comments + '\0'), 2)
  166      case("retroarch-comment-default-malformed-assignment", lambda r: put(r, "etc/retroarch.cfg",
  167           comments + 'video_driver="unterminated\n'), 2)
  168      case("retroarch-comment-default-active-account", lambda r: put(r, "etc/retroarch.cfg",
  169           comments + 'cheevos_token="' + CANARY + '"\n'), 1, "player-account")
  170      case("retroarch-empty-default", lambda r: put(r, "etc/retroarch.cfg", ""), 2)
  171      case("retroarch-blank-default", lambda r: put(r, "etc/retroarch.cfg", " \n\t\n"), 2)
  172      case("retroarch-section-only-default", lambda r: put(r, "etc/retroarch.cfg", "[empty]\n"), 2)
  173      case("retroarch-semicolon-only-default", lambda r: put(r, "etc/retroarch.cfg", "; unsupported\n"), 2)
  174      case("system-comment-only-still-refuses", lambda r: put(r, "usr/config/system/configs/system.cfg", comments), 2)
  175      case("cloud-comment-only-still-refuses", lambda r: put(r, "usr/config/cloud_sync.conf", comments), 2)
  176      case("runtime-retroarch-comment-only-still-refuses", lambda r: put(r, "storage/.config/retroarch/retroarch.cfg", comments), 2)
  177      case("shipped-locale-dangling-clean-image", shipped_locale, mode="clean-image")
  178      case("shipped-locale-dangling-first-boot", shipped_locale, 2)
  179      def materialized_locale(root):
  180          shipped_locale(root)
  181          put(root, "storage/.config/locale/en/translation.mo", b"synthetic translation")
  182      case("shipped-locale-materialized", materialized_locale)
  183      def locale_history(root):
  184          materialized_locale(root)
  185          put(root, "storage/.config/locale/gamelist.xml",
  186              '<gameList><game><playcount>1</playcount></game></gameList>')
  187      case("shipped-locale-materialized-history", locale_history, 1, "playcount", "clean-image")
  188      case("locale-altered-first-hop", lambda r: shipped_locale(r, first="/storage/.config/locale"),
  189           2, mode="clean-image")
  190      case("locale-altered-second-hop", lambda r: shipped_locale(r, second="/storage/.config/other"),
  191           2, mode="clean-image")
  192      case("locale-first-hop-escape", lambda r: shipped_locale(r, first="../../../../../outside"),
  193           2, mode="clean-image")
  194      case("locale-target-escape", locale_target_escape, 2, mode="clean-image")
  195      def unrelated_dangling_locale(root):
  196          shipped_locale(root)
  197          (root / "usr/config/emulationstation/other").symlink_to("/usr/share/locale")
  198      case("locale-unrelated-dangling", unrelated_dangling_locale, 2, mode="clean-image")
  199      case("never-played-zero", lambda r: put(r, "storage/roms/synthetic/gamelist.xml",
  200           '<gameList><game><playcount>0</playcount><lastplayed>0</lastplayed></game></gameList>'))
  201      case("identical-default-repeat", lambda r: put(r, "usr/config/system/configs/system.cfg",
  202           'global.retroachievements.username=\nuzebox.integerscale=1\nuzebox.integerscale=1\n'))
  203      case("es-lexical-playcount", lambda r: put(r, "storage/roms/synthetic/gamelist.xml",
  204           '<gameList><game><playcount>00</playcount></game></gameList>'), 1, "playcount")
  205      account = lambda root: put(root, "storage/.config/system/configs/system.cfg",
  206                                "global.retroachievements.username=" + CANARY + "\n")
  207      case("player-runtime", account, 1, "player-account")
  208      case("retained-player", account, mode="retained-upgrade")
  209      case("player-default", lambda r: put(r, "usr/config/retroarch/retroarch.cfg",
  210           'cheevos_token = "' + CANARY + '"\n'), 1, "player-account", "retained-upgrade")
  211      case("recovery-copy", lambda r: put(r, "storage/.config/system/configs/system.cfg.backup",
  212           "global.retroachievements.token=" + CANARY + "\n"), 1, "player-account")
  213      case("atomic-copy", lambda r: put(r, "storage/.config/system/configs/system.cfg.tmp.123",
  214           "global.retroachievements.key=" + CANARY + "\n"), 1, "player-account")
  215      case("runtime-service", lambda r: put(r, "storage/.config/emulationstation/es_settings.cfg",
  216           '<config><string name="ScreenScraperDevPass" value="' + CANARY + '"/></config>'),
  217           1, "developer-service-identity")
  218      def compiled(root):
  219          path = root / "usr/bin/emulationstation"
  220          path.write_bytes(path.read_bytes() + b"\0devid=" + CANARY.encode() +
  221                           b"&devpassword=" + CANARY.encode() + b"\0")
  222      case("compiled-service", compiled, 1, "developer-service-identity")
  223      def binary_fragments(root, fragment):
  224          path = root / "usr/bin/emulationstation"
  225          path.write_bytes(path.read_bytes() + fragment)
  226      case("bare-runtime-fragments", lambda r: binary_fragments(r,
  227           b"devid=\0&devpassword=\0z=\0&y=\0"))
  228      case("compiled-ra-service", lambda r: binary_fragments(r,
  229           b"z=" + CANARY.encode() + b"&y=" + CANARY.encode() + b"\0"), 1, "developer-service-identity")
  230      shared = b"jelos"
  231      approved = b"devid=" + shared + b"&devpassword=" + shared
  232      for mode in ("clean-image", "first-boot", "retained-upgrade"):
  233          case("compiled-shared-" + mode, lambda r: binary_fragments(r, b"\0" + approved + b"\0"),
  234               category="approved-shared-developer-identity", mode=mode)
  235      for name, fragment in (
  236              ("id", b"devid=" + CANARY.encode() + b"&devpassword=" + shared),
  237              ("password", b"devid=" + shared + b"&devpassword=" + CANARY.encode()),
  238              ("prefix", b"other" + approved), ("suffix", approved + b"other"),
  239              ("query", approved + b"&extra=value"), ("case", approved.upper().replace(b"DEVID", b"devid").replace(b"DEVPASSWORD", b"devpassword"))):
  240          case("compiled-shared-refuse-" + name,
  241               lambda r, fragment=fragment: binary_fragments(r, b"\0" + fragment + b"\0"),
  242               1, "developer-service-identity")
  243      case("compiled-shared-no-terminator", lambda r: binary_fragments(r, b"\0" + approved),
  244           1, "developer-service-identity")
  245      case("compiled-shared-with-private", lambda r: binary_fragments(r, b"\0" + approved +
  246           b"\0devid=" + CANARY.encode() + b"&devpassword=" + CANARY.encode() + b"\0"),
  247           1, "developer-service-identity")
  248      case("compiled-shared-with-ra", lambda r: binary_fragments(r, b"\0" + approved +
  249           b"\0z=" + CANARY.encode() + b"&y=" + CANARY.encode() + b"\0"),
  250           1, "developer-service-identity")
  251      case("shared-defaults-still-refused", lambda r: put(r, "usr/config/emulationstation/es_settings.cfg",
  252           '<config><string name="ScreenScraperDevId" value="jelos"/>'
  253           '<string name="ScreenScraperDevPass" value="jelos"/></config>'),
  254           1, "developer-service-identity")
  255      case("shared-player-still-refused", lambda r: put(r, "usr/config/emulationstation/es_settings.cfg",
  256           '<config><string name="ScreenScraperUser" value="jelos"/>'
  257           '<string name="ScreenScraperPass" value="jelos"/></config>'), 1, "player-account")
  258      def remote(root):
  259          put(root, "storage/.config/rclone/rclone.conf",
  260              "[synthetic]\ntype = webdav\nurl = http://127.0.0.1:1\npass = " + CANARY + "\n")
  261          put(root, "storage/.config/rclone/active-connection", "synthetic\n")
  262      case("configured-remote", remote, 1, "configured-remote")
  263      case("retained-remote", remote, mode="retained-upgrade")
  264      case("encrypted-remote", lambda r: put(r, "storage/.config/rclone/rclone.conf",
  265           "RCLONE_ENCRYPT_V0:\n" + CANARY), 2)
  266      case("remote-missing-type", lambda r: put(r, "storage/.config/rclone/rclone.conf",
  267           "[synthetic]\npass = " + CANARY + "\n"), 2)
  268      stamp = lambda r: put(r, "storage/.cache/cloud_sync/last-backup", "1234567890 0\n")
  269      case("completed-empty-stamp", stamp, 1, "cloud-activity")
  270      case("retained-stamp", stamp, mode="retained-upgrade")
  271      case("malformed-stamp", lambda r: put(r, "storage/.cache/cloud_sync/last-restore", CANARY), 2)
  272      case("scrub-zero-work-current-boot", scrub_marker, clear="startup-log-scrub")
  273      case("scrub-zero-work-boot-boundary", lambda r: scrub_marker(r, first=SCRUB_EPOCH), clear="startup-log-scrub")
  274      case("scrub-zero-work-stale", lambda r: scrub_marker(r, first=SCRUB_EPOCH - 1), 1, "log-scrub-outside-boot")
  275      case("scrub-zero-work-future", lambda r: scrub_marker(r, second=SCRUB_EPOCH + 102), 1, "log-scrub-outside-boot")
  276      case("scrub-zero-work-reversed-epochs", lambda r: scrub_marker(r, first=SCRUB_EPOCH + 12), 1, "log-scrub-outside-boot")
  277      case("scrub-cloud-files-present", lambda r: scrub_marker(r, files1=1), 1, "cloud-log-scrub-activity")
  278      case("scrub-no-adapter-current-boot", no_adapter_scrub, clear="startup-no-adapter-log-scrub")
  279      case("scrub-no-adapter-boot-boundary", lambda r: no_adapter_scrub(r, mtime=SCRUB_EPOCH),
  280           clear="startup-no-adapter-log-scrub")
  281      case("scrub-no-adapter-stale-log", lambda r: no_adapter_scrub(r, mtime=SCRUB_EPOCH - 1),
  282           1, "log-scrub-outside-boot")
  283      case("scrub-no-adapter-post-scrub-log", lambda r: no_adapter_scrub(r, mtime=SCRUB_EPOCH + 11),
  284           1, "log-scrub-outside-boot")
  285      case("scrub-no-adapter-stale-marker", lambda r: no_adapter_scrub(r, first=SCRUB_EPOCH - 1),
  286           1, "log-scrub-outside-boot")
  287      case("scrub-no-adapter-redactions", lambda r: no_adapter_scrub(r, lines1=1),
  288           1, "cloud-log-scrub-activity")
  289      case("scrub-no-adapter-es-history", lambda r: no_adapter_scrub(r, files2=1),
  290           1, "cloud-log-scrub-activity")
  291      case("scrub-no-adapter-other-content", lambda r: no_adapter_scrub(r, data=CANARY),
  292           1, "cloud-log-scrub-activity")
  293      def extra_no_adapter_line(root):
  294          path = no_adapter_scrub(root)
  295          path.write_bytes(path.read_bytes() + CANARY.encode() + b"\n")
  296      case("scrub-no-adapter-extra-line", extra_no_adapter_line, 1, "cloud-log-scrub-activity")
  297      def rotated_no_adapter(root):
  298          no_adapter_scrub(root)
  299          put(root, "storage/.cache/log/cloud_sync.log.1", CANARY)
  300      case("scrub-no-adapter-rotation", rotated_no_adapter, 1, "cloud-log-scrub-activity")
  301      def linked_no_adapter(root):
  302          path = no_adapter_scrub(root)
  303          path.rename(path.with_name("startup-log"))
  304          path.symlink_to("startup-log")
  305      case("scrub-no-adapter-linked-log", linked_no_adapter, 2)
  306      case("scrub-no-adapter-unreadable-log", lambda r: no_adapter_scrub(r).chmod(0), 2)
  307      def invalid_no_adapter_date(root):
  308          path = no_adapter_scrub(root)
  309          path.write_bytes(path.read_bytes().replace(b"2033-05-18", b"2033-99-99"))
  310      case("scrub-no-adapter-malformed-date", invalid_no_adapter_date, 2)
  311      def multiple_no_adapter_files(root):
  312          no_adapter_scrub(root)
  313          scrub_marker(root, files1=2)
  314      case("scrub-no-adapter-multiple-files", multiple_no_adapter_files, 1, "cloud-log-scrub-activity")
  315      case("scrub-no-adapter-clean-image-preseed", no_adapter_scrub, 1, "preseeded-log-scrub", "clean-image")
  316      case("scrub-no-adapter-retained", no_adapter_scrub, category="retained-log-scrub", mode="retained-upgrade")
  317      case("scrub-es-files-present", lambda r: scrub_marker(r, files2=1), 1, "cloud-log-scrub-activity")
  318      case("scrub-changed-lines-present", lambda r: scrub_marker(r, lines2=1), 1, "cloud-log-scrub-activity")
  319      case("scrub-missing-family", lambda r: alter_scrub(r, lambda s: s.splitlines(keepends=True)[0]), 2)
  320      case("scrub-duplicate-family", lambda r: alter_scrub(r, lambda s: s.replace("es_log_scrubbed", "scrubbed")), 2)
  321      case("scrub-unknown-trailing-data", lambda r: alter_scrub(r, lambda s: s + CANARY), 2)
  322      case("scrub-malformed-count", lambda r: alter_scrub(r, lambda s: s.replace("files=0", "files=-1")), 2)
  323      case("scrub-malformed-epoch", lambda r: scrub_marker(r, first=0), 2)
  324      case("scrub-no-boot-snapshot", lambda r: scrub_marker(r, boot=False), 2)
  325      def malformed_boot(root):
  326          scrub_marker(root)
  327          put(root, "proc/stat", "btime invalid\n")
  328      case("scrub-malformed-boot-snapshot", malformed_boot, 2)
  329      def duplicate_boot(root):
  330          scrub_marker(root)
  331          put(root, "proc/stat", ("btime " + str(SCRUB_EPOCH) + "\n") * 2)
  332      case("scrub-duplicate-boot-epoch", duplicate_boot, 2)
  333      def unreadable_uptime(root):
  334          scrub_marker(root)
  335          (root / "proc/uptime").chmod(0)
  336      case("scrub-unreadable-uptime", unreadable_uptime, 2)
  337      def malformed_uptime(root):
  338          scrub_marker(root)
  339          put(root, "proc/uptime", "-1.00 0.00\n")
  340      case("scrub-malformed-uptime", malformed_uptime, 2)
  341      def link_scrub(root):
  342          path = scrub_marker(root)
  343          target = root / "scrub-target"
  344          path.rename(target)
  345          path.symlink_to("/scrub-target")
  346      case("scrub-marker-symlink", link_scrub, 2)
  347      def renamed_scrub(root):
  348          path = scrub_marker(root)
  349          path.rename(path.with_name("log-scrubbed.tmp"))
  350      case("scrub-other-filename-still-residue", renamed_scrub, 1, "cloud-state-residue")
  351      case("scrub-clean-image-preseed", lambda r: scrub_marker(r, boot=False), 1, "preseeded-log-scrub", "clean-image")
  352      case("scrub-clean-image-empty-preseed", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed", ""),
  353           1, "preseeded-log-scrub", "clean-image")
  354      case("scrub-retained-history", lambda r: scrub_marker(r, first=1, second=2, files1=2, lines1=3, boot=False),
  355           category="retained-log-scrub", mode="retained-upgrade")
  356      case("scrub-retained-legacy-family", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed",
  357           "scrubbed=1 files=2 lines=3\n"), category="retained-log-scrub", mode="retained-upgrade")
  358      case("scrub-retained-es-only", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed",
  359           "es_log_scrubbed=1 files=2 lines=3\n"), category="retained-log-scrub", mode="retained-upgrade")
  360      case("scrub-retained-es-first-retry", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed",
  361           "es_log_scrubbed=1 files=2 lines=3\nscrubbed=2 files=4 lines=5\n"),
  362           category="retained-log-scrub", mode="retained-upgrade")
  363      case("scrub-retained-duplicate-family", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed",
  364           "es_log_scrubbed=1 files=2 lines=3\nes_log_scrubbed=2 files=4 lines=5\n"), 2, mode="retained-upgrade")
  365      case("scrub-retained-unknown-family", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed",
  366           "scrubbed=1 files=2 lines=3\nunknown_scrubbed=2 files=4 lines=5\n"), 2, mode="retained-upgrade")
  367      case("scrub-first-boot-es-only-refuses", lambda r: alter_scrub(r, lambda s: s.splitlines(keepends=True)[1]), 2)
  368      case("scrub-first-boot-es-first-refuses", lambda r: alter_scrub(r, lambda s: ''.join(reversed(s.splitlines(keepends=True)))), 2)
  369      case("scrub-retained-malformed", lambda r: put(r, "storage/.cache/cloud_sync/log-scrubbed", CANARY),
  370           2, mode="retained-upgrade")
  371      def history(root):
  372          put(root, "storage/roms/synthetic/gamelist.xml",
  373              '<gameList><game><path>./synthetic.rom</path><playcount>5</playcount>'
  374              '<lastplayed>20000101T010203</lastplayed></game></gameList>')
  375      case("imported-history", history, 1, "playcount")
  376      case("retained-history", history, mode="retained-upgrade")
  377      case("es-fallback-history", lambda r: put(r,
  378           "storage/.config/emulationstation/gamelists/synthetic/gamelist.xml",
  379           '<gameList><game><lastplayed>20000101T010203</lastplayed></game></gameList>'),
  380           1, "lastplayed")
  381      case("history-malformed-xml", lambda r: put(r, "storage/roms/synthetic/gamelist.xml",
  382           "<gameList>" + CANARY), 2)
  383      case("history-malformed-count", lambda r: put(r, "storage/roms/synthetic/gamelist.xml",
  384           '<gameList><game><playcount>not-a-count</playcount></game></gameList>'), 2)
  385      case("history-malformed-date", lambda r: put(r, "storage/roms/synthetic/gamelist.xml",
  386           '<gameList><game><lastplayed>20009999T010203</lastplayed></game></gameList>'), 2)
  387      case("qa-name-is-private", lambda r: put(r, "storage/qa-" + CANARY, CANARY), 1, "qa-residue")
  388      case("proxy-cache", lambda r: put(r, "storage/.config/raofflineproxy/cache.sqlite", CANARY),
  389           1, "account-cache-residue")
  390      case("standalone-token", lambda r: put(r,
  391           "storage/.config/ppsspp/PSP/SYSTEM/ppsspp_retroachievements.dat", CANARY),
  392           1, "player-account-file")
  393      # PPSSPP's shipped syntax and exact active account keys (#599). Every
  394      # profile file is a public repository default, never device state.
  395      psp = "ppsspp/PSP/SYSTEM/ppsspp.ini"
  396      default_root = HERE.parent / "projects/ROCKNIX/packages/emulators/standalone/ppsspp-sa/sources"
  397      default_files = sorted(default_root.glob("*/ppsspp.ini"))
  398      require({p.parent.name for p in default_files} >= {"H700", "SM8550"})
  399      for path in default_files:
  400          case("ppsspp-shipped-" + path.parent.name,
  401               lambda r, data=path.read_bytes(): put(r, "usr/config/" + psp, data), mode="clean-image")
  402      psp_empty = ('\ufeff[General]\r\nEnable Logging = False\r\n'
  403                   '[Achievements]\r\nAchievementsUserName = \r\nAchievementsToken = ""\r\n')
  404      case("ppsspp-empty-accounts", lambda r: put(r, "storage/.config/" + psp, psp_empty))
  405      case("ppsspp-spaced-key-private", lambda r: put(r, "storage/.config/" + psp,
  406           "[General]\nEnable Logging = False\nUnknown key = " + CANARY + "\n"))
  407      for key in ("AchievementsUserName", "AchievementsToken"):
  408          for prefix in ("usr/config/", "storage/.config/"):
  409              case("ppsspp-" + key.lower() + ("-default" if prefix == "usr/config/" else "-runtime"),
  410                   lambda r, key=key, prefix=prefix: put(r, prefix + psp,
  411                       "[Achievements]\n" + key + " = " + CANARY + "\n"), 1, "player-account")
  412      case("ppsspp-case-tabs-crlf", lambda r: put(r, "storage/.config/" + psp,
  413           "\t[aChIeVeMeNtS]\t\r\n\taChIeVeMeNtSuSeRnAmE\t =\t" + CANARY + "\t\r\n"),
  414           1, "player-account")
  415      case("ppsspp-internal-key-tab", lambda r: put(r, "storage/.config/" + psp,
  416           "[General]\nEnable\tLogging = False\n"))
  417      # Internal key/section spaces are significant upstream, not normalized away.
  418      case("ppsspp-distinct-spaced-account-key", lambda r: put(r, "storage/.config/" + psp,
  419           "[Achievements]\nAchievements UserName = " + CANARY + "\n"))
  420      case("ppsspp-wrong-section", lambda r: put(r, "storage/.config/" + psp,
  421           "[General]\nAchievementsToken = " + CANARY + "\n"))
  422      case("ppsspp-section-spaces-significant", lambda r: put(r, "storage/.config/" + psp,
  423           "[ Achievements ]\nAchievementsToken = " + CANARY + "\n"))
  424      case("ppsspp-duplicate-empty", lambda r: put(r, "storage/.config/" + psp,
  425           "[Achievements]\nAchievementsToken = \nachievementstoken\t=\t\n"))
  426      case("ppsspp-duplicate-populated", lambda r: put(r, "storage/.config/" + psp,
  427           "[Achievements]\nAchievementsToken = " + CANARY + "\nAchievementsToken = " + CANARY + "\n"),
  428           1, "player-account")
  429      for first, second, label in (("", CANARY, "empty-first"), (CANARY, "", "populated-first")):
  430          case("ppsspp-conflicting-duplicate-" + label,
  431               lambda r, first=first, second=second: put(r, "storage/.config/" + psp,
  432                   "[Achievements]\nAchievementsToken = " + first +
  433                   "\naChIeVeMeNtStOkEn\t=\t" + second + "\n"), 2)
  434      case("ppsspp-repeated-section-conflict", lambda r: put(r, "storage/.config/" + psp,
  435           "[Achievements]\nAchievementsUserName = \n[ACHIEVEMENTS]\nAchievementsUserName = " + CANARY), 2)
  436      case("ppsspp-single-quotes-are-literal", lambda r: put(r, "storage/.config/" + psp,
  437           "[Achievements]\nAchievementsToken = ''\n"), 1, "player-account")
  438      case("ppsspp-unterminated-double-quote", lambda r: put(r, "storage/.config/" + psp,
  439           '[Achievements]\nAchievementsToken = "' + CANARY + "\n"), 2)
  440      case("ppsspp-empty-key", lambda r: put(r, "storage/.config/" + psp,
  441           "[General]\n \t= " + CANARY + "\n"), 2)
  442      for directive in ("include", "reference"):
  443          case("ppsspp-" + directive, lambda r, directive=directive: put(r, "storage/.config/" + psp,
  444               '# ' + directive + ' "/outside/' + CANARY + '"\n' + psp_empty.lstrip("\ufeff")), 2)
  445      case("ppsspp-comment-key-unsupported", lambda r: put(r, "storage/.config/" + psp,
  446           "[Achievements]\nAchievementsToken#unsupported = " + CANARY + "\n"), 2)
  447      case("ppsspp-recovery-sibling", lambda r: put(r, "storage/.config/" + psp + ".new.123",
  448           "[Achievements]\nAchievementsToken = " + CANARY + "\n"), 1, "player-account")
  449      case("ppsspp-retained-account", lambda r: put(r, "storage/.config/" + psp,
  450           "[Achievements]\nAchievementsToken = " + CANARY + "\n"), mode="retained-upgrade")
  451      case("ppsspp-retained-default-account", lambda r: put(r, "usr/config/" + psp,
  452           "[Achievements]\nAchievementsToken = " + CANARY + "\n"), 1, "player-account", "retained-upgrade")
  453      case("ppsspp-spaces-not-global", lambda r: put(r, "storage/.config/flycast/emu.cfg",
  454           "[General]\nEnable Logging = False\n"), 2)
  455      case("standalone-ini", lambda r: put(r, "storage/.config/flycast/emu.cfg",
  456           "[achievements]\nToken = " + CANARY + "\n"), 1, "player-account")
  457      case("dolphin-apitoken-only", lambda r: put(r, "storage/.config/dolphin-emu/RetroAchievements.ini",
  458           "[Achievements]\nApiToken = " + CANARY + "\n"), 1, "player-account")
  459      case("dolphin-apitoken-default", lambda r: put(r, "usr/config/dolphin-emu/RetroAchievements.ini",
  460           "[Achievements]\nApiToken = " + CANARY + "\n"), 1, "player-account", "clean-image")
  461      case("dolphin-apitoken-retained", lambda r: put(r, "storage/.config/dolphin-emu/RetroAchievements.ini",
  462           "[Achievements]\nApiToken = " + CANARY + "\n"), mode="retained-upgrade")
  463      melon_empty = "RA_Enabled=0\nRA_Username=null\nRA_Password=null\nRA_Token=null\n"
  464      case("melonds-null-default", lambda r: put(r, "usr/config/melonDS/melonDS.ini", melon_empty),
  465           mode="clean-image")
  466      case("melonds-null-runtime", lambda r: put(r, "storage/.config/melonDS/melonDS.ini", melon_empty))
  467      case("melonds-token-only", lambda r: put(r, "storage/.config/melonDS/melonDS.ini",
  468           melon_empty.replace("RA_Token=null", "RA_Token=" + CANARY)), 1, "player-account")
  469      case("melonds-username-only", lambda r: put(r, "usr/config/melonDS/melonDS.ini",
  470           melon_empty.replace("RA_Username=null", "RA_Username=" + CANARY)), 1, "player-account")
  471      case("melonds-password-only", lambda r: put(r, "storage/.config/melonDS/melonDS.ini",
  472           melon_empty.replace("RA_Password=null", "RA_Password=" + CANARY)), 1, "player-account")
  473      case("melonds-quoted-null-is-populated", lambda r: put(r, "storage/.config/melonDS/melonDS.ini",
  474           'RA_Token="null"\n'), 1, "player-account")
  475      case("melonds-section-null-is-populated", lambda r: put(r, "storage/.config/melonDS/melonDS.ini",
  476           '[Achievements]\nRA_Token=null\n'), 1, "player-account")
  477      case("melonds-uppercase-null-is-populated", lambda r: put(r, "storage/.config/melonDS/melonDS.ini",
  478           'RA_Token=NULL\n'), 1, "player-account")
  479      case("melonds-other-key-case-null-is-populated", lambda r: put(r, "storage/.config/melonDS/melonDS.ini",
  480           'ra_token=null\n'), 1, "player-account")
  481      case("other-emulator-null-is-populated", lambda r: put(r, "storage/.config/flycast/emu.cfg",
  482           'RA_Token=null\n'), 1, "player-account")
  483      case("history-playlist", lambda r: put(r, "storage/.config/retroarch/content_history.lpl",
  484           json.dumps({"items": [{"path": CANARY}]})), 1, "play-history")
  485      case("missing-required", lambda r: (r / "usr/config/system/configs/system.cfg").unlink(), 2)
  486      case("empty-required", lambda r: put(r, "usr/config/system/configs/system.cfg", ""), 2)
  487      case("unreadable-required", lambda r: (r / "usr/config/system/configs/system.cfg").chmod(0), 2)
  488      case("malformed-es", lambda r: put(r, "usr/config/emulationstation/es_settings.cfg",
  489           '<config><string name="ScreenScraperPass"/></config>'), 2)
  490      case("xml-entity", lambda r: put(r, "usr/config/emulationstation/es_settings.cfg",
  491           '<!DOCTYPE config [<!ENTITY x "' + CANARY + '">]><config/>'), 2)
  492      case("duplicate-field", lambda r: put(r, "usr/config/system/configs/system.cfg",
  493           'global.retroachievements.username=\nglobal.retroachievements.username=' + CANARY), 2)
  494      case("effective-override", lambda r: put(r, "storage/.config/cloud_sync.conf",
  495           CLOUD.replace("--progress", "--config /outside/" + CANARY)), 2,
  496           "unsupported-config-override", "retained-upgrade")
  497      case("retroarch-include", lambda r: put(r, "storage/.config/retroarch/retroarch.cfg",
  498           '#include "/outside/' + CANARY + '"\ncheevos_username=""\n'), 2)
  499      def dangling(root):
  500          p = root / "usr/config/system/configs/system.cfg"
  501          p.unlink()
  502          p.symlink_to("/missing")
  503      case("dangling-required", dangling, 2)
  504      def cycle(root):
  505          p = root / "usr/config/system/configs/system.cfg"
  506          p.unlink()
  507          p.symlink_to("system.cfg")
  508      case("symlink-cycle", cycle, 2)
  509      def fifo(root):
  510          p = root / "usr/config/system/configs/system.cfg"
  511          p.unlink()
  512          os.mkfifo(p)
  513      case("fifo-required", fifo, 2)
  514      invoke(["--root", str(work / "absent"), "--mode", "first-boot"], 2)
  515      invoke(["--root", str(work), "--mode", CANARY], 2)
  516      invoke(["--root", str(work), "--mode", "first-boot", "--require-ready"], 2)
  517      rows.extend({"case": n, "status": "pass"} for n in
  518                  ("absent-root", "invalid-mode", "readiness-requires-guest-root"))
  519      return rows
  520  
  521  
  522  def run(argv, stdin=None):
  523      p = subprocess.run(argv, input=stdin, capture_output=True, timeout=180)
  524      require(p.returncode == 0)
  525      return p.stdout
  526  
  527  
  528  def make_tar(root, destination):
  529      system = destination.with_suffix(".system")
  530      run(["mksquashfs", str(root), str(system), "-noappend", "-processors", "1", "-no-progress"])
  531      with tarfile.open(destination, "w") as archive:
  532          archive.add(system, arcname="synthetic/target/SYSTEM", recursive=False)
  533      return system
  534  
  535  
  536  def make_image(system, destination, contaminated=False):
  537      disk = destination.with_suffix("")
  538      with disk.open("xb") as stream:
  539          stream.truncate(80 * 1024**2)
  540      run(["sfdisk", str(disk)], b"label: dos\nstart=2048,size=65536,type=c\nstart=67584,size=65536,type=83\n")
  541      fat = destination.with_suffix(".fat")
  542      with fat.open("xb") as stream:
  543          stream.truncate(32 * 1024**2)
  544      run(["mkfs.vfat", str(fat)])
  545      run(["mcopy", "-i", str(fat), str(system), "::/SYSTEM"])
  546      ext = destination.with_suffix(".ext4")
  547      seed = destination.with_suffix(".seed")
  548      seed.mkdir()
  549      (seed / ".please_resize_me").touch()
  550      if contaminated:
  551          (seed / "qa-state").write_text("synthetic")
  552      with ext.open("xb") as stream:
  553          stream.truncate(32 * 1024**2)
  554      run(["mkfs.ext4", "-F", "-q", "-d", str(seed), str(ext)])
  555      with disk.open("r+b") as output:
  556          for source, offset in ((fat, 2048 * 512), (ext, 67584 * 512)):
  557              output.seek(offset)
  558              with source.open("rb") as stream:
  559                  shutil.copyfileobj(stream, output)
  560      with disk.open("rb") as stream, gzip.open(destination, "wb") as output:
  561          shutil.copyfileobj(stream, output)
  562  
  563  
  564  def release_bundle(parent, payload_path):
  565      # Whole synthetic artifact hashes are required by the existing candidate store;
  566      # no credential-field hash is computed or written.
  567      commit, stamp, version = "1" * 40, "20261013T000000Z", "0.0.1-rc.1"
  568      build = version + "+" + stamp + ".g" + commit[:12]
  569      base = "pixelelated-GENERIC_X64.x86_64-" + build
  570      bundle = parent / "incoming"
  571      bundle.mkdir()
  572      name = base + ".tar"
  573      shutil.copyfile(payload_path, bundle / name)
  574      identity = {"schema": 1, "name": "pixelelated", "dirty": "no", "release_version": version,
  575                  "build_timestamp": stamp, "build_commit": commit, "build_version": build,
  576                  "image_name": base, "device": "GENERIC_X64", "arch": "x86_64"}
  577      put(bundle, base + ".identity.json", json.dumps(identity))
  578      digest = hashlib.sha256((bundle / name).read_bytes()).hexdigest()
  579      put(bundle, name + ".sha256", digest + "  " + name + "\n")
  580      files = {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
  581               for p in bundle.iterdir()}
  582      manifest = json.dumps({"schema": 1, "inputs": {"distribution_commit": commit}, "files": files})
  583      put(bundle, "manifest.json", manifest)
  584      dest = parent / hashlib.sha256(manifest.encode()).hexdigest()
  585      bundle.rename(dest)
  586      return dest
  587  
  588  
  589  def ext4_listing_controls(work, image):
  590      # Exercise the gate through its payload CLI, without importing it. Only the
  591      # debugfs listing response is synthetic; the image and other readers remain
  592      # real. Native clean/dirty image controls run separately before these cases.
  593      shim = put(work, "debugfs-shim/debugfs", "#!" + sys.executable + "\n" + '''import json
  594  import os
  595  from pathlib import Path
  596  import sys
  597  if len(sys.argv) != 4 or sys.argv[1] != "-R":
  598      sys.exit(2)
  599  responses = json.loads(Path(os.environ["PIX565_DEBUGFS_RESPONSE"]).read_text())
  600  if sys.argv[2] not in responses:
  601      sys.exit(2)
  602  sys.stdout.write(responses[sys.argv[2]])
  603  ''')
  604      shim.chmod(0o755)
  605      root = ("/2/040755/0/0/.//\n/2/040755/0/0/..//\n"
  606              "/11/040700/0/0/lost+found//\n/12/100644/0/0/.please_resize_me/0/\n")
  607      lost = "/11/040700/0/0/.//\n/2/040755/0/0/..//\n"
  608      slots = "/0/000000/0/0//0/\n" * 3
  609      cases = (
  610          ("unused-slots-lost-found", "ls -p /lost+found", lost + slots, 0),
  611          ("unused-slots-root", "ls -p /", root + slots, 0),
  612          ("unused-slots-without-dots", "ls -p /lost+found", slots, 2),
  613          ("zero-inode-named-entry", "ls -p /lost+found", lost + "/0/000000/0/0/" + CANARY + "/0/\n", 2),
  614          ("zero-inode-live-mode", "ls -p /lost+found", lost + "/0/100644/0/0//0/\n", 2),
  615          ("zero-inode-owner", "ls -p /lost+found", lost + "/0/000000/1/0//0/\n", 2),
  616          ("zero-inode-size", "ls -p /lost+found", lost + "/0/000000/0/0//1/\n", 2),
  617          ("zero-inode-short-record", "ls -p /lost+found", lost + "/0/000000/0//0/\n", 2),
  618          ("zero-inode-alternate-spelling", "ls -p /lost+found", lost + "/00/000000/0/0//0/\n", 2),
  619          ("unused-slot-trailing-data", "ls -p /lost+found", lost + "/0/000000/0/0//0/extra\n", 2),
  620          ("live-entry-beside-unused-slots", "ls -p /lost+found",
  621           lost + slots + "/13/100644/0/0/" + CANARY + "/0/\n", 1),
  622      )
  623      rows = []
  624      for name, directory, output, expected in cases:
  625          responses = {"ls -p /": root, "ls -p /lost+found": lost}
  626          responses[directory] = output
  627          response = put(work, "debugfs-shim/response.json", json.dumps(responses))
  628          env = {**os.environ, "PATH": str(shim.parent) + os.pathsep + os.environ.get("PATH", ""),
  629                 "PIX565_DEBUGFS_RESPONSE": str(response)}
  630          invoke(["--payload", str(image)], expected,
  631                 "storage-seed-residue" if expected == 1 else None, env=env)
  632          rows.append({"case": "debugfs-" + name, "status": "pass", "synthetic_reader_output": True})
  633      return rows
  634  
  635  
  636  def payload_controls(work):
  637      rows = []
  638      for name, contaminated in (("clean", False), ("contaminated", True)):
  639          root = work / (name + "-root")
  640          root.mkdir()
  641          clean(root, runtime=False)
  642          shipped_locale(root)
  643          put(root, "etc/retroarch.cfg", '# Synthetic upstream-style defaults\n# video_driver = "gl"\n')
  644          if contaminated:
  645              put(root, "usr/config/system/configs/system.cfg",
  646                  "global.retroachievements.username=" + CANARY + "\n")
  647          tar = work / (name + ".tar")
  648          system = make_tar(root, tar)
  649          report = invoke(["--payload", str(tar)], 1 if contaminated else 0,
  650                          "player-account" if contaminated else None)
  651          require(any(row["category"] == "runtime-locale-deferred" and row["status"] == "clear"
  652                      for row in report["checks"]))
  653          rows.append({"case": "tar-" + name + "-shipped-locale", "status": "pass"})
  654          if not contaminated:
  655              invoke(["--payload", str(tar)], 2, env={**os.environ, "PATH": "/nonexistent"})
  656              rows.append({"case": "missing-payload-reader", "status": "pass"})
  657          parent = work / (name + "-bundle")
  658          parent.mkdir()
  659          bundle = release_bundle(parent, tar)
  660          p = subprocess.run([sys.executable, "-B", str(HERE / "fork-publish-release"),
  661                              "--prepare", str(bundle)], capture_output=True, timeout=180)
  662          require(CANARY.encode() not in p.stdout + p.stderr)
  663          require(p.returncode == (1 if contaminated else 0))
  664          if not contaminated:
  665              plan = json.loads(p.stdout)
  666              require(plan["publication_performed"] is False and plan["draft"] is True)
  667              require(len(plan["selected_state_inspection"]) == 1)
  668              for dirty_storage in (False, True):
  669                  image = work / ("dirty-storage.img.gz" if dirty_storage else "clean.img.gz")
  670                  make_image(system, image, dirty_storage)
  671                  invoke(["--payload", str(image)], 1 if dirty_storage else 0,
  672                         "storage-seed-residue" if dirty_storage else None)
  673                  rows.append({"case": "image-dirty-storage" if dirty_storage else "image-clean",
  674                               "status": "pass"})
  675              rows += ext4_listing_controls(work, work / "clean.img.gz")
  676          rows.append({"case": "prepare-" + name, "status": "pass"})
  677      for name, mutate in (("locale-altered-second-hop", lambda r: shipped_locale(
  678              r, second="/storage/.config/other")), ("locale-target-escape", locale_target_escape)):
  679          root = work / (name + "-payload-root")
  680          root.mkdir()
  681          clean(root, runtime=False)
  682          mutate(root)
  683          path = work / (name + ".tar")
  684          make_tar(root, path)
  685          invoke(["--payload", str(path)], 2)
  686          rows.append({"case": "tar-" + name, "status": "pass"})
  687      root = work / "preseeded-scrub-root"
  688      root.mkdir()
  689      clean(root, runtime=False)
  690      shipped_locale(root)
  691      scrub_marker(root, boot=False)
  692      path = work / "preseeded-scrub.tar"
  693      make_tar(root, path)
  694      invoke(["--payload", str(path)], 1, "preseeded-log-scrub")
  695      rows.append({"case": "tar-zero-work-scrub-preseed-refused", "status": "pass"})
  696      # Regression for unsquashfs cat_scan fnmatch: bracketed and matching literal
  697      # sibling coexist, but only the bracketed file is contaminated. Reading the
  698      # clean match or skipping the unsupported spelling must not produce a pass.
  699      root = work / "literal-reader-root"
  700      root.mkdir()
  701      clean(root, runtime=False)
  702      shipped_locale(root)
  703      put(root, "usr/config/system/configs/system.cfg.bak[1]",
  704          "global.retroachievements.token=" + CANARY + "\n")
  705      put(root, "usr/config/system/configs/system.cfg.bak1",
  706          "global.retroachievements.token=\n")
  707      path = work / "literal-reader.tar"
  708      make_tar(root, path)
  709      report = invoke(["--payload", str(path)], 1, "player-account")
  710      require(any(row["path"] == "/usr/config/system/configs/system.cfg.*" and
  711                  row["category"] == "player-account" and row["count"] == 1 and
  712                  row["status"] == "blocked" for row in report["checks"]))
  713      rows.append({"case": "tar-literal-bracketed-recovery-file", "status": "pass"})
  714      parent = work / "literal-reader-bundle"
  715      parent.mkdir()
  716      bundle = release_bundle(parent, path)
  717      p = subprocess.run([sys.executable, "-B", str(HERE / "fork-publish-release"),
  718                          "--prepare", str(bundle)], capture_output=True, timeout=180)
  719      require(p.returncode == 1 and CANARY.encode() not in p.stdout + p.stderr)
  720      rows.append({"case": "prepare-literal-bracketed-recovery-file", "status": "pass"})
  721      for name, members in (("missing-system", [("synthetic/target/KERNEL", b"not-system")]),
  722                            ("invalid-squashfs", [("synthetic/target/SYSTEM", b"not-system")]),
  723                            ("traversal", [("../SYSTEM", b"not-system")]),
  724                            ("duplicate-system", [("synthetic/target/SYSTEM", b"x")] * 2)):
  725          path = work / (name + ".tar")
  726          with tarfile.open(path, "w") as archive:
  727              for member_name, data in members:
  728                  member = tarfile.TarInfo(member_name)
  729                  member.size = len(data)
  730                  archive.addfile(member, io.BytesIO(data))
  731          invoke(["--payload", str(path)], 2)
  732          rows.append({"case": name, "status": "pass"})
  733      bad = put(work, "invalid.img.gz", b"not-gzip")
  734      invoke(["--payload", str(bad)], 2)
  735      unknown = put(work, "unknown.bin", b"synthetic")
  736      invoke(["--payload", str(unknown)], 2)
  737      rows.extend({"case": n, "status": "pass"} for n in ("invalid-gzip", "unsupported-payload"))
  738      return rows
  739  
  740  
  741  def prepare_guest(path):
  742      # Source travels inline through the serial helper, leaving no fixture in /storage.
  743      encoded = base64.b64encode(GATE.read_bytes()).decode()
  744      script = """#!/bin/sh
  745  set -u
  746  python3 -B -c 'import base64; exec(compile(base64.b64decode(""" + json.dumps(encoded) + """), "<state-check>", "exec"))' --root / --mode first-boot --require-ready
  747  rc=$?
  748  echo "PIX_STATE_565_RC=$rc"
  749  exit "$rc"
  750  """
  751      with path.open("x") as stream:
  752          stream.write(script)
  753  
  754  
  755  def main():
  756      parser = argparse.ArgumentParser(description=__doc__)
  757      mode = parser.add_mutually_exclusive_group(required=True)
  758      mode.add_argument("--self-test", action="store_true")
  759      mode.add_argument("--payload-tests", action="store_true")
  760      mode.add_argument("--prepare-guest-script", type=Path)
  761      args = parser.parse_args()
  762      if args.prepare_guest_script:
  763          prepare_guest(args.prepare_guest_script)
  764          print("prepared first-boot script; not executed")
  765          return 0
  766      if args.payload_tests:
  767          require(all(shutil.which(name) for name in ("mksquashfs", "unsquashfs", "sfdisk", "mcopy",
  768                                                    "mkfs.vfat", "mkfs.ext4", "e2fsck", "debugfs")))
  769      with tempfile.TemporaryDirectory(prefix="pix565-controls-") as directory:
  770          work = Path(directory)
  771          rows = root_controls(work)
  772          if args.payload_tests:
  773              rows += payload_controls(work)
  774      print(json.dumps({"schema": 1, "status": "pass", "control_count": len(rows), "controls": rows}, indent=2))
  775      return 0
  776  
  777  
  778  if __name__ == "__main__":
  779      try:
  780          sys.exit(main())
  781      except Exception:
  782          print('{"schema":1,"status":"error","category":"fixture-or-reader-failure"}')
  783          sys.exit(2)
```

## File: tools/rasteratops-candidate-store (at 8ebaf8daad, 107 lines)

```text
    1  #!/usr/bin/env python3
    2  """Keep a candidate bundle by manifest digest, without overwriting it (#344).
    3  
    4  put --store DIR --inputs INPUTS.json FILE... copies images and evidence under
    5  DIR/sha256/<manifest digest> using a store lock and an atomic directory rename.
    6  verify BUNDLE checks every byte before and after QA. QA writes elsewhere.
    7  This is local candidate storage; it never creates or publishes a release.
    8  """
    9  import argparse
   10  import fcntl
   11  import hashlib
   12  import json
   13  import os
   14  from pathlib import Path
   15  import shutil
   16  import sys
   17  import tempfile
   18  
   19  
   20  def digest(path):
   21      h = hashlib.sha256()
   22      with path.open("rb") as stream:
   23          for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
   24              h.update(block)
   25      return h.hexdigest()
   26  
   27  
   28  def verify(bundle):
   29      manifest = bundle / "manifest.json"
   30      if manifest.is_symlink() or digest(manifest) != bundle.name:
   31          raise ValueError("manifest digest does not match the bundle name")
   32      data = json.loads(manifest.read_text())
   33      if data["schema"] != 1 or not data["files"]:
   34          raise ValueError("unsupported or empty manifest")
   35      for name, expected in data["files"].items():
   36          if Path(name).name != name or name in {".", "..", "manifest.json"}:
   37              raise ValueError("invalid artifact name")
   38          path = bundle / name
   39          if path.is_symlink() or not path.is_file() or digest(path) != expected["sha256"] or path.stat().st_size != expected["bytes"]:
   40              raise ValueError("artifact does not match: " + name)
   41      if set(p.name for p in bundle.iterdir()) != {*data["files"], "manifest.json"}:
   42          raise ValueError("bundle contains unrecorded files")
   43      print("PASS candidate bundle " + str(bundle))
   44  
   45  
   46  parser = argparse.ArgumentParser(description=__doc__)
   47  sub = parser.add_subparsers(dest="command", required=True)
   48  put = sub.add_parser("put")
   49  put.add_argument("--store", type=Path, required=True)
   50  put.add_argument("--inputs", type=Path, required=True)
   51  put.add_argument("files", type=Path, nargs="+")
   52  check = sub.add_parser("verify")
   53  check.add_argument("bundle", type=Path)
   54  args = parser.parse_args()
   55  try:
   56      if args.command == "verify":
   57          verify(args.bundle.resolve())
   58      else:
   59          inputs = json.loads(args.inputs.read_text())
   60          if not isinstance(inputs, dict) or not inputs:
   61              raise ValueError("input record must be a nonempty object")
   62          store = args.store.resolve()
   63          target = store / "sha256"
   64          target.mkdir(parents=True, exist_ok=True)
   65          with (store / ".lock").open("a") as lock:
   66              fcntl.flock(lock, fcntl.LOCK_EX)
   67              staging = Path(tempfile.mkdtemp(prefix=".incoming-", dir=target))
   68              try:
   69                  files = {}
   70                  for source in args.files:
   71                      if source.is_symlink() or not source.is_file() or source.name in {"manifest.json", *files}:
   72                          raise ValueError("invalid or duplicate source: " + str(source))
   73                      before = digest(source)
   74                      destination = staging / source.name
   75                      shutil.copyfile(source, destination)
   76                      after = digest(destination)
   77                      if before != after or digest(source) != after:
   78                          raise ValueError("source changed while copying: " + str(source))
   79                      files[source.name] = {"sha256": after, "bytes": destination.stat().st_size}
   80                  manifest = staging / "manifest.json"
   81                  manifest.write_text(json.dumps({"schema": 1, "inputs": inputs, "files": files}, sort_keys=True, indent=2) + "\n")
   82                  for path in staging.iterdir():
   83                      with path.open("rb") as stream:
   84                          os.fsync(stream.fileno())
   85                  bundle = target / digest(manifest)
   86                  if bundle.exists():
   87                      verify(bundle)
   88                  else:
   89                      # Finish writes before making the directory visible to QA.
   90                      for path in staging.iterdir():
   91                          path.chmod(0o444)
   92                      staging.chmod(0o555)
   93                      staging.rename(bundle)
   94                      for directory in [bundle, target]:
   95                          fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
   96                          try:
   97                              os.fsync(fd)
   98                          finally:
   99                              os.close(fd)
  100                      verify(bundle)
  101              finally:
  102                  if staging.exists():
  103                      staging.chmod(0o755)
  104                      shutil.rmtree(staging)
  105  except (OSError, ValueError, KeyError, TypeError) as error:
  106      print("FAIL candidate store: " + str(error), file=sys.stderr)
  107      sys.exit(1)
```

## File: tools/rasteratops-identity-check (at 8ebaf8daad, 157 lines)

```text
    1  #!/usr/bin/env python3
    2  """Check 0.0.1 identity inputs and retained RC2 contracts (#337, #383).
    3  
    4  This source check does not replace clean/upgrade VM frames and network proof.
    5  Use --tree to test a scratch tree, including a template-only negative control.
    6  """
    7  import argparse
    8  import hashlib
    9  import os
   10  from pathlib import Path
   11  import re
   12  import subprocess
   13  import sys
   14  import tempfile
   15  import xml.etree.ElementTree as ET
   16  
   17  parser = argparse.ArgumentParser(description=__doc__)
   18  parser.add_argument("--tree", type=Path, default=Path(__file__).resolve().parent.parent)
   19  parser.add_argument("--es", type=Path, required=True)
   20  args = parser.parse_args()
   21  root, es = args.tree.resolve(), args.es.resolve()
   22  failures = 0
   23  
   24  
   25  def check(ok, label):
   26      global failures
   27      print(("PASS " if ok else "FAIL ") + label)
   28      failures += not ok
   29  
   30  
   31  def read(path):
   32      try:
   33          return path.read_text()
   34      except OSError:
   35          check(False, "read " + str(path))
   36          return ""
   37  
   38  
   39  def value(text, name):
   40      match = re.search(r'^\s*' + re.escape(name) + r'="([^"]*)"', text, re.M)
   41      return match.group(1) if match else None
   42  
   43  
   44  options = read(root / "distributions/ROCKNIX/options")
   45  version = read(root / "distributions/ROCKNIX/version")
   46  for name, expected in [("DISTRONAME", "pixelelated"), ("OSNAME", "rocknix"),
   47                         ("DISTRO_BOOTLABEL", "ROCKNIX"), ("DISTRO_DISKLABEL", "STORAGE")]:
   48      check(value(options, name) == expected, name + " = " + expected)
   49  for name, expected in [("GIT_ORGANIZATION", "pixelelated"),
   50                         ("HOME_URL", "https://pixelelated.com"),
   51                         ("WIKI_URL", "https://github.com/pixelelated/distribution/tree/next/docs"),
   52                         ("BUG_REPORT_URL", "https://github.com/pixelelated/distribution/issues")]:
   53      check(value(options, name) == expected, name + " uses the current identity")
   54  check(value(version, "OS_VERSION") == "0.0.1", "semantic OS version")
   55  check(value(version, "IMAGE_SUFFIX") == "from-ROCKNIX", "RC2 adoption filename suffix")
   56  for file in ["packages/linux/package.mk", "projects/ROCKNIX/packages/linux/package.mk"]:
   57      check('--set-str CONFIG_DEFAULT_HOSTNAME "ROCKNIX"' in read(root / file),
   58            "retained kernel hostname: " + file)
   59  
   60  scripts = root / "projects/ROCKNIX/packages/rocknix/sources/scripts"
   61  with tempfile.TemporaryDirectory(prefix="rasteratops-identity-") as work:
   62      work = Path(work)
   63      marker = work / "external-call"
   64      # Observe old query paths without reaching the network. Unexpected commands
   65      # and nonzero statuses fail; no personal config is sourced by the new shims.
   66      for command in ["curl", "wget", "ping", "get_setting", "set_setting", "logger"]:
   67          stub = work / command
   68          stub.write_text('#!/bin/sh\nprintf called >> "$IDENTITY_CALL_MARKER"\nexit 99\n')
   69          stub.chmod(0o755)
   70      (work / "profile").write_text(":\n")
   71      env = {"PATH": "/work:/usr/bin:/bin", "HOME": "/work",
   72             "IDENTITY_CALL_MARKER": "/work/external-call"}
   73      sandbox = ["/usr/bin/bwrap", "--unshare-all", "--die-with-parent",
   74                 "--ro-bind", "/usr", "/usr", "--ro-bind", "/bin", "/bin",
   75                 "--ro-bind", "/lib", "/lib", "--ro-bind", "/lib64", "/lib64",
   76                 "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
   77                 "--dir", "/etc", "--ro-bind", str(work / "profile"), "/etc/profile",
   78                 "--dir", "/storage", "--ro-bind", str(scripts), "/source",
   79                 "--bind", str(work), "/work", "--chdir", "/work"]
   80      cases = [("rocknix-update", ["check"], 1),
   81               ("rocknix-update", ["--help"], 0),
   82               ("rocknix-update", ["force"], 1),
   83               ("rocknix-update", ["20261001"], 1),
   84               ("rocknix-report-stats", [], 0)]
   85      for script, argv, expected in cases:
   86          source = read(scripts / script)
   87          check(not re.search(r"https?://(?:update|stats)\.rocknix\.org", source),
   88                "retired endpoint absent: " + script + " " + " ".join(argv))
   89          try:
   90              run = subprocess.run([*sandbox, "/bin/sh", "/source/" + script, *argv], env=env,
   91                                   capture_output=True, text=True, timeout=5)
   92              silent = argv == ["check"] or script == "rocknix-report-stats"
   93              output_ok = not run.stdout if silent else "manual updates" in run.stdout
   94              check(run.returncode == expected and output_ok and not run.stderr
   95                    and not marker.exists(), "inert legacy entry point: " + script + " " + " ".join(argv))
   96          except (OSError, subprocess.TimeoutExpired):
   97              check(False, "entry point failed or timed out: " + script)
   98  timer = root / "projects/ROCKNIX/packages/rocknix/system.d/rocknix-report-stats.timer"
   99  check(timer.is_symlink() and os.readlink(timer) == "/dev/null", "statistics timer masked")
  100  
  101  # Tools descriptions are player text; paths and attribution are retained
  102  # compatibility/credit fields. Check the consumer fields, not a blanket grep.
  103  try:
  104      tools = ET.parse(root / "projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml")
  105      check(True, "Tools metadata is well-formed XML")
  106      stale = [game.findtext("path", "") for game in tools.getroot()
  107               if any(re.search(r"rocknix|rasteratops", game.findtext(field, ""), re.I)
  108                      for field in ("name", "desc"))]
  109      check(not stale, "Tools names and descriptions use the current identity")
  110  except (OSError, ET.ParseError):
  111      check(False, "Tools metadata is well-formed XML")
  112  
  113  api = read(es / "es-app/src/ApiSystem.cpp")
  114  menu = read(es / "es-app/src/guis/GuiMenu.cpp")
  115  check('GetEnv("OS_NAME")' in api, "ES reads the displayed OS identity")
  116  # #424: a shell variable in os-release is not an inherited process value.
  117  # Exercise the real export boundary with a clean environment and a child shell.
  118  export_profile = root / "projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export"
  119  try:
  120      child = subprocess.run(
  121          ["/bin/bash", "-c",
  122           'OS_NAME=pixelelated; OS_VERSION=0.0.1; OS_BUILD=community; '
  123           ". \"$1\"; exec /bin/sh -c 'printf \"%s\\n\" \"${OS_NAME-unset}\" \"${OS_VERSION-unset}\" \"${OS_BUILD-unset}\"'",
  124           "identity-export", str(export_profile)],
  125          env={"PATH": "/usr/bin:/bin"}, capture_output=True, text=True, timeout=5)
  126      check(child.returncode == 0 and not child.stderr
  127            and child.stdout.splitlines() == ["pixelelated", "0.0.1", "community"],
  128            "OS identity reaches a child through the installed export profile")
  129  except (OSError, subprocess.TimeoutExpired):
  130      check(False, "OS identity export boundary ran")
  131  check('if (getApplicationName() == "pixelelated")\n        return false;' in api,
  132        "ES refuses inherited automatic/forced update queries")
  133  check('_("MANUAL UPDATES")' in menu and '_("ENABLE pixelelated SCREENSHOT")' in menu,
  134        "manual update and screenshot rows")
  135  check('ENABLE ROCKNIX SCREENSHOT' not in menu, "old screenshot display literal removed")
  136  check(':/pixelelated-wordmark.svg' in read(es / "es-core/src/Splash.h"), "ES wordmark selected")
  137  recipe = read(root / "projects/ROCKNIX/packages/ui/emulationstation/package.mk")
  138  try:
  139      head = subprocess.check_output(["git", "-C", str(es), "rev-parse", "HEAD"], text=True).strip()
  140  except subprocess.CalledProcessError:
  141      head = None
  142  check(head is not None and value(recipe, "PKG_VERSION") == head, "ES recipe pins the checked commit")
  143  check(value(recipe, "PKG_LICENSE") == "MIT", "ES licence matches its source")
  144  
  145  art = root / "docs/pixelelated/art/pixelelated-wordmark.svg"
  146  theme = root / "projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next"
  147  paths = [art, es / "resources/pixelelated-wordmark.svg", theme / "sources/pixelelated-wordmark.svg"]
  148  digests = [hashlib.sha256(read(path).encode()).hexdigest() for path in paths]
  149  check(len(set(digests)) == 1 and art.is_file(), "ES and theme use the canonical wordmark bytes")
  150  check('+         <path>./pixelelated-wordmark.svg</path>' in read(theme / "patches/001-pixelelated-splash.patch"),
  151        "theme selects the wordmark, retaining custom splash support")
  152  check('cp ${PKG_DIR}/sources/pixelelated-wordmark.svg' in read(theme / "package.mk"),
  153        "theme installs its selected wordmark")
  154  for file in ["LICENSE.md", "TRADEMARK.md", "NAMING.md"]:
  155      check(bool(read(root / file).strip()), "identity policy present: " + file)
  156  print(f"identity source contracts: {failures} failure(s); image qualification still required")
  157  sys.exit(1 if failures else 0)
```

## File: tools/retroarch-wrapper-test (at 8ebaf8daad, 226 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """retroarch-wrapper-test -- does the threaded video wrapper run a posted
    5  command exactly once?
    6  
    7      tools/retroarch-wrapper-test [path/to/video_thread_wrapper.c] [--gated]
    8  
    9  It extracts send_packet, wait_reply, reply, send_and_wait_user_to_thread and
   10  the dequeue block of video_thread_loop VERBATIM from the file given (by
   11  default the H700 build root's), compiles them against small doubles --
   12  pthreads for slock/scond, a stub handle_packet carrying the real
   13  CUSTOM_COMMAND case -- and drives them: one thread posts a command whose data
   14  is a LOCAL, as every caller of video_thread_texture_handle does; another sets
   15  frame.updated, which wakes the loop in the window where cmd_data still holds
   16  the packet that has just completed.
   17  
   18  The method counts its calls. 2000 posts must produce exactly 2000 calls.
   19  
   20  Written after #211, where a doubled call dereferenced a returned stack frame
   21  and segfaulted RetroArch on a handheld -- four times over two weeks, once with
   22  a core dump. Against the unfixed source it fails in seconds:
   23  
   24      as shipped:   posted 2000 command(s); the method ran 2017 time(s)  FAIL
   25      with 0015:    posted 2000 command(s); the method ran 2000 time(s)  PASS
   26  
   27  Exit 0 when every command ran once, 1 when any ran twice, 2 when the fixture
   28  could not be built -- a check that cannot run has not passed.
   29  """
   30  import re, subprocess, sys, tempfile
   31  from pathlib import Path
   32  
   33  args = [a for a in sys.argv[1:] if not a.startswith("--")]
   34  if args:
   35      src_path = Path(args[0])
   36  else:
   37      # The source the image was built from: the H700 build root first (the
   38      # handheld's), else the GENERIC_X64 root's, else RETROARCH_SRC; the same
   39      # tree is unpacked in each (one PKG_VERSION), and the newest unpack wins.
   40      # It used to be the H700 root alone, which lives outside this tree and is
   41      # absent on a host that builds only the VM image (audit #258 PL-020).
   42      roots = [Path("/workspace/repos/rocknix.worktrees/devices/build.ROCKNIX-H700.aarch64"),
   43               Path("/workspace/repos/rocknix.worktrees/generic-x64/build.ROCKNIX-GENERIC_X64.x86_64")]
   44      import os
   45      if os.environ.get("RETROARCH_SRC"):
   46          roots.insert(0, Path(os.environ["RETROARCH_SRC"]))
   47      found = []
   48      for r in roots:
   49          found += sorted(r.glob("build/retroarch-*/gfx/video_thread_wrapper.c"), key=lambda p: p.stat().st_mtime, reverse=True)
   50          found += sorted(r.glob("gfx/video_thread_wrapper.c"))
   51      if not found:
   52          print("retroarch-wrapper-test: no video_thread_wrapper.c given and none under "
   53                + ", ".join(str(r) for r in roots) + " (RETROARCH_SRC names another tree)", file=sys.stderr)
   54          sys.exit(2)
   55      src_path = found[0]
   56  print(f"retroarch-wrapper-test: source {src_path}")
   57  gated = "--gated" in sys.argv
   58  source = src_path.read_text()
   59  
   60  def func(sig):
   61      start = source.index(sig)
   62      brace = source.index("{", start)
   63      depth, end = 1, brace + 1
   64      while depth:
   65          depth += (source[end] == "{") - (source[end] == "}")
   66          end += 1
   67      return source[start:end]
   68  
   69  send_packet = func("static void video_thread_send_packet(")
   70  wait_reply  = func("static void video_thread_wait_reply(")
   71  reply       = func("static void video_thread_reply(")
   72  send_wait   = func("static void video_thread_send_and_wait_user_to_thread(")
   73  
   74  # The dequeue is extracted from video_thread_loop in the file under test,
   75  # so this checks the real source rather than a model of it.
   76  loop = func("static void video_thread_loop(")
   77  start = loop.index("slock_lock(thr->lock);")
   78  end = loop.index("return;", loop.index("video_thread_handle_packet")) + len("return;")
   79  dequeue = loop[start:end]
   80  # the frame path is not under test; keep the loop from spinning on it
   81  dequeue = dequeue.replace("return;", "return NULL;")
   82  dequeue = dequeue.replace("updated = thr->frame.updated;",
   83                            "updated = thr->frame.updated; thr->frame.updated = false;")
   84  
   85  harness = r"""
   86  #include <pthread.h>
   87  #include <stdio.h>
   88  #include <stdlib.h>
   89  #include <stdbool.h>
   90  #include <string.h>
   91  #include <unistd.h>
   92  
   93  typedef pthread_mutex_t slock_t;
   94  typedef pthread_cond_t  scond_t;
   95  static void slock_lock(slock_t *l)   { pthread_mutex_lock(l); }
   96  static void slock_unlock(slock_t *l) { pthread_mutex_unlock(l); }
   97  static void scond_wait(scond_t *c, slock_t *l) { pthread_cond_wait(c, l); }
   98  static void scond_signal(scond_t *c) { pthread_cond_broadcast(c); }
   99  
  100  enum { CMD_VIDEO_NONE = 0, CMD_CUSTOM_COMMAND = 7 };
  101  typedef unsigned long uintptr_t_;
  102  typedef uintptr_t_ (*custom_command_method_t)(void*);
  103  
  104  typedef struct { int type; struct { struct { custom_command_method_t method;
  105     void *data; uintptr_t_ return_value; } custom_command; } data; } thread_packet_t;
  106  
  107  typedef struct { slock_t *lock, *user_lock; scond_t *cond_cmd, *cond_thread;
  108     int send_cmd, reply_cmd; thread_packet_t cmd_data;
  109     struct { bool updated; } frame; } thread_video_t;
  110  
  111  static int g_calls = 0;
  112  static bool video_thread_handle_packet(thread_video_t *thr, const thread_packet_t *incoming);
  113  __SEND_PACKET__
  114  __WAIT_REPLY__
  115  __REPLY__
  116  __SEND_WAIT__
  117  
  118  /* The wrap the drivers post: reads the caller's stack object. */
  119  typedef struct { void *gl; void *payload; } gl3_texture_cmd_t;
  120  static uintptr_t_ texture_wrap(void *data)
  121  {
  122     gl3_texture_cmd_t *cmd = (gl3_texture_cmd_t*)data;
  123     __sync_fetch_and_add(&g_calls, 1);
  124     return (uintptr_t_)(cmd->gl != NULL);   /* the read that faulted in #211 */
  125  }
  126  
  127  static bool video_thread_handle_packet(thread_video_t *thr, const thread_packet_t *incoming)
  128  {
  129     thread_packet_t pkt = *incoming;
  130     switch (pkt.type)
  131     {
  132        case CMD_VIDEO_NONE: break;
  133        case CMD_CUSTOM_COMMAND:
  134           if (pkt.data.custom_command.method)
  135              pkt.data.custom_command.return_value =
  136                 pkt.data.custom_command.method(pkt.data.custom_command.data);
  137           video_thread_reply(thr, &pkt);
  138           break;
  139     }
  140     return false;
  141  }
  142  
  143  static thread_video_t g_thr;
  144  static volatile bool g_stop = false;
  145  
  146  static void *video_thread(void *arg)
  147  {
  148     thread_video_t *thr = (thread_video_t*)arg;
  149     thread_packet_t pkt;
  150     bool updated; bool have_cmd = false; (void)have_cmd; (void)updated;
  151     while (!g_stop)
  152     {
  153  __DEQUEUE__
  154        if (g_stop) break;
  155     }
  156     return NULL;
  157  }
  158  
  159  /* gl3_load_texture's shape: the cmd is a local, and the frame dies on return. */
  160  static void post_one(void)
  161  {
  162     gl3_texture_cmd_t cmd;
  163     thread_packet_t pkt;
  164     cmd.gl = (void*)0x1; cmd.payload = (void*)0x2;
  165     pkt.type = CMD_CUSTOM_COMMAND;
  166     pkt.data.custom_command.method = texture_wrap;
  167     pkt.data.custom_command.data   = &cmd;
  168     video_thread_send_and_wait_user_to_thread(&g_thr, &pkt);
  169  }
  170  
  171  /* The frame that arrives in the reply window. */
  172  static void *frame_thread(void *arg)
  173  {
  174     (void)arg;
  175     while (!g_stop)
  176     {
  177        slock_lock(g_thr.lock);
  178        g_thr.frame.updated = true;
  179        scond_signal(g_thr.cond_thread);
  180        slock_unlock(g_thr.lock);
  181        usleep(200);
  182     }
  183     return NULL;
  184  }
  185  
  186  int main(void)
  187  {
  188     pthread_mutex_t l = PTHREAD_MUTEX_INITIALIZER, u = PTHREAD_MUTEX_INITIALIZER;
  189     pthread_cond_t  c = PTHREAD_COND_INITIALIZER,  t = PTHREAD_COND_INITIALIZER;
  190     pthread_t vt, ft;
  191     int posts = 2000;
  192     memset(&g_thr, 0, sizeof(g_thr));
  193     g_thr.lock = &l; g_thr.user_lock = &u; g_thr.cond_cmd = &c; g_thr.cond_thread = &t;
  194     pthread_create(&vt, NULL, video_thread, &g_thr);
  195     pthread_create(&ft, NULL, frame_thread, NULL);
  196     for (int i = 0; i < posts; i++) post_one();
  197     g_stop = true;
  198     /* wake the dequeue's inner wait, which tests neither stop flag */
  199     slock_lock(g_thr.lock); g_thr.frame.updated = true;
  200     scond_signal(g_thr.cond_thread); slock_unlock(g_thr.lock);
  201     pthread_join(ft, NULL); pthread_join(vt, NULL);
  202     printf("posted %d command(s); the method ran %d time(s)\n", posts, g_calls);
  203     if (g_calls != posts) { printf("FAIL: a posted command was executed more than once\n"); return 1; }
  204     printf("PASS: every command ran exactly once\n");
  205     return 0;
  206  }
  207  """
  208  harness = (harness.replace("__SEND_PACKET__", send_packet)
  209                    .replace("__WAIT_REPLY__", wait_reply)
  210                    .replace("__REPLY__", reply)
  211                    .replace("__SEND_WAIT__", send_wait)
  212                    .replace("__DEQUEUE__", dequeue))
  213  out = Path(tempfile.mkdtemp()) / "t.c"
  214  out.write_text(harness)
  215  exe = out.with_suffix("")
  216  cc = subprocess.run(["gcc", "-O1", "-g", "-fsanitize=address", "-fno-omit-frame-pointer",
  217                       str(out), "-o", str(exe), "-lpthread"], capture_output=True, text=True)
  218  if cc.returncode:
  219      print(cc.stderr[-2500:]); sys.exit(2)
  220  env = {"ASAN_OPTIONS": "detect_stack_use_after_return=1:abort_on_error=0", "PATH": "/usr/bin:/bin"}
  221  r = subprocess.run([str(exe)], capture_output=True, text=True, env=env, timeout=60)
  222  print(r.stdout.strip())
  223  if r.returncode != 0:
  224      tail = [l for l in r.stderr.splitlines() if "ERROR" in l or "stack-use-after" in l or "#0 " in l or "#1 " in l]
  225      print("\n".join(tail[:6]) if tail else r.stderr[-800:])
  226  sys.exit(r.returncode)
```

## File: tools/rocknix-info-test (at 8ebaf8daad, 60 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present pixelelated (https://github.com/pixelelated)
    4  from pathlib import Path
    5  import subprocess,tempfile,os,json,shutil,hashlib
    6  import argparse
    7  parser=argparse.ArgumentParser(description="Exercise optional hardware reporting with complete-script filesystem fixtures.")
    8  parser.add_argument('--baseline', type=Path, help='Optional original script for the failing control and valid-output comparison.')
    9  parser.add_argument('--output', type=Path, help='Retain original result channels and source digest in this directory.')
   10  args=parser.parse_args()
   11  P=args.output or Path(tempfile.mkdtemp(prefix='rocknix-info-test-'))
   12  P.mkdir(parents=True,exist_ok=True)
   13  ROOT=Path(__file__).resolve().parent.parent
   14  file='projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info'
   15  old=args.baseline.read_text() if args.baseline else None;new=(ROOT/file).read_text()
   16  results=[]
   17  with tempfile.TemporaryDirectory(prefix='hardware-',dir=P) as td:
   18   t=Path(td)
   19   def write(name,value):
   20    p=t/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value);return p
   21   def execute(source,arch='x86_64',label='new'):
   22    # Rewrite only OS filesystem roots into the disposable fixture. Keep the
   23    # complete script and real shell/awk/grep/arithmetic logic intact.
   24    code=source.replace('/etc/profile',str(t/'profile')).replace('/tmp/battery.percent',str(t/'battery.percent')).replace('/sys/',str(t/'sys')+'/').replace('/proc/cpuinfo',str(t/'proc/cpuinfo')).replace('/proc/meminfo',str(t/'proc/meminfo')).replace('/usr/lib/autostart/quirks',str(t/'quirks')).replace('/storage/games-internal',str(t/'storage')).replace('/storage/games-external',str(t/'storage'))
   25    env={**os.environ,'HW_ARCH':arch,'HW_DEVICE':'QA','HW_CPU':'QA CPU','OS_NAME':'pixelelated','OS_VERSION':'0.0.1-dev','BUILD_ID':'a0f60255ab','BUILD_BRANCH':'test','GPU_FREQ':str(t/'sys/gpu'),'DEVICE_GPU_CUR_FREQ':str(t/'sys/gpu/cur_freq'),'DEVICE_GPU_MAX_FREQ':str(t/'sys/gpu/clocks'),'DEVICE_TEMP_SENSOR':str(t/'sys/thermal/*/temp'),'DEVICE_GPU_TEMP_SENSOR':str(t/'sys/gpu/temp'),'DEVICE_HAS_FAN':'false'}
   26    r=subprocess.run(['bash'],input=code,text=True,env=env,capture_output=True)
   27    (P/(label+'.json')).write_text(json.dumps({'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2)+'\n');return r
   28   def check(name,condition):
   29    results.append({'case':name,'passed':bool(condition)});assert condition,name
   30   write('profile','');write('proc/cpuinfo','processor\t: 0\nmodel name\t: QA CPU\n');write('proc/meminfo','MemTotal: 1000000 kB\nMemAvailable: 500000 kB\n');(t/'storage').mkdir()
   31   write('sys/class/dmi/id/sys_vendor','QA\n');write('sys/class/dmi/id/product_name','VM\n');(t/'sys/class/net').mkdir(parents=True)
   32   a=execute(old,label='original-absent') if old else None;b=execute(new,label='fixed-absent')
   33   if a:check('original absent interfaces reproduce arithmetic error and nonzero status',a.returncode!=0 and 'arithmetic syntax error' in a.stderr)
   34   check('absent optional metrics succeed quietly',b.returncode==0 and not b.stderr)
   35   check('unknown CPU frequencies are explicit, GPU and temperature rows omitted','CPU CURRENT FREQUENCY: Not Available' in b.stdout and 'CPU MAXIMUM FREQUENCY: Not Available' in b.stdout and 'GPU CURRENT' not in b.stdout and 'TEMPERATURE:' not in b.stdout)
   36   base='sys/devices/system/cpu/cpufreq/policy0/'
   37   write(base+'scaling_cur_freq','1234000\n');write(base+'cpuinfo_max_freq','2400000\n');write(base+'scaling_max_freq','2400000\n');write(base+'related_cpus','0 1 2 3\n')
   38   write('sys/gpu/cur_freq','650000000\n');write('sys/gpu/max_freq','900000000\n');write('sys/gpu/clocks','SCLK: 0 900Mhz\n');write('sys/thermal/zone0/temp','43000\n');write('sys/thermal/zone1/temp','47000\n');write('sys/gpu/temp','55000\n')
   39   a=execute(old,label='original-valid') if old else None;b=execute(new,label='fixed-valid')
   40   # Ignore live IP/hostname/disk values only by selecting the hardware rows.
   41   rows=lambda r:[x for x in r.stdout.splitlines() if x.startswith(('CPU ','GPU ','THREADS','CURRENT FREQUENCY','MAXIMUM FREQUENCY'))]
   42   check('valid x86 hardware presentation unchanged',(not a or rows(a)==rows(b)) and b.returncode==0 and not b.stderr and all(x in b.stdout for x in ['CPU CURRENT FREQUENCY: 1234 MHz','CPU MAXIMUM FREQUENCY: 2400 MHz','GPU CURRENT FREQUENCY: 650 MHz','GPU MAXIMUM FREQUENCY: 900 MHz','CPU TEMPERATURE: 45°','GPU TEMPERATURE: 55°']))
   43   a=execute(old,arch='aarch64',label='original-arm-valid') if old else None;b=execute(new,arch='aarch64',label='fixed-arm-valid')
   44   check('valid ARM clusters/GPU/temperature presentation unchanged',(not a or rows(a)==rows(b)) and b.returncode==0 and not b.stderr and all(x in b.stdout for x in ['THREADS 0-3: 1234MHz','THREADS 0-3: 2400MHz','GPU CURRENT FREQUENCY: 650 MHz','GPU MAXIMUM FREQUENCY: 900 MHz','CPU TEMPERATURE: 45°','GPU TEMPERATURE: 55°']))
   45   for n,v in [('empty',''),('malformed','unavailable\n'),('expression','1+2\n'),('overflow','9'*30+'\n')]:
   46    write(base+'scaling_cur_freq',v);write('sys/gpu/cur_freq',v);b=execute(new,label='fixed-'+n)
   47    check(n+' optional frequencies are unavailable without errors',b.returncode==0 and not b.stderr and 'CPU CURRENT FREQUENCY: Not Available' in b.stdout and 'GPU CURRENT' not in b.stdout)
   48   write(base+'scaling_cur_freq','0001234000\n');write('sys/gpu/cur_freq','0\n');b=execute(new,label='fixed-leading-zero')
   49   check('leading zeros remain decimal; measured zero is retained','CPU CURRENT FREQUENCY: 1234 MHz' in b.stdout and 'GPU CURRENT FREQUENCY: 0 MHz' in b.stdout and b.returncode==0 and not b.stderr)
   50   for n in ['sys/thermal/zone0/temp','sys/thermal/zone1/temp','sys/gpu/temp']:write(n,'not-a-reading\n')
   51   b=execute(new,label='fixed-invalid-temperatures');check('invalid temperatures omitted without division by zero',b.returncode==0 and not b.stderr and 'TEMPERATURE:' not in b.stdout)
   52   q=write('quirks/platforms/QA/info.d/10-good','#!/bin/sh\necho "QA QUIRK: executed"\n');q.chmod(0o755)
   53   write('quirks/platforms/QA/info.d/20-not-executable','should not run\n');(t/'quirks/platforms/QA/info.d/30-directory').mkdir()
   54   b=execute(new,label='fixed-quirks');check('valid quirk executes; missing and non-executable entries skip',b.returncode==0 and not b.stderr and 'QA QUIRK: executed' in b.stdout)
   55   q=write('quirks/platforms/QA/info.d/05-failing','#!/bin/sh\nexit 23\n');q.chmod(0o755)
   56   b=execute(new,label='fixed-quirk-failure');check('real quirk failure survives later success',b.returncode==23 and 'QA QUIRK: executed' in b.stdout)
   57  (P/'result.json').write_text(json.dumps({'source_sha256':hashlib.sha256(new.encode()).hexdigest(),'cases':results},indent=2)+'\n')
   58  print('PASS',len(results),'full-script positive/negative controls',flush=True)
   59  
   60  if not args.output:shutil.rmtree(P)
```

## File: tools/test-fixtures/cloud_connections_fixture.py (at 8ebaf8daad, 45 lines)

```text
    1  # SPDX-License-Identifier: GPL-2.0-or-later
    2  # Copyright (C) 2026-present pixelelated
    3  """External-rclone adapter for the historical OAuth race fixtures.
    4  
    5  The production transaction, locks, state guards and atomic writes run unchanged.
    6  Only the fixture rclone's successful config-create side effect is simulated.
    7  Real-rclone transactions are covered separately by cloud-connections-test.
    8  """
    9  import configparser
   10  import io
   11  from pathlib import Path
   12  import sys
   13  import subprocess
   14  
   15  def configure(module, directory):
   16      c = module.connections
   17      root = Path(directory)
   18      c.CONFIG = root / 'rclone.conf'
   19      c.ACTIVE = root / 'active-connection'
   20      c.LOCK = root / 'cloud.lock'
   21      c.SYSTEM = root / 'system.cfg'
   22      def run(args):
   23          stage = Path(args[1])
   24          command = args[2:]
   25          if module.subprocess is subprocess and module.RCLONE == '/usr/bin/rclone':
   26              raise RuntimeError('OAuth fixture needs its fake provider')
   27          answer = module.subprocess.run([module.RCLONE] + command, capture_output=True, text=True)
   28          if answer.returncode:
   29              raise c.Refused('The connection could not be verified. Your settings were not changed.')
   30          if command[:2] == ['config', 'create']:
   31              parser = configparser.RawConfigParser()
   32              parser.read(stage)
   33              parser.add_section(command[2])
   34              parser.set(command[2], 'type', command[3])
   35              with stage.open('w') as stream: parser.write(stream)
   36          return answer.stdout
   37      c.run = run
   38      if hasattr(module, 'main'):
   39          original = module.main
   40          def main(argv):
   41              try: return original(argv)
   42              except c.Refused as error:
   43                  sys.stderr.write(str(error) + '\n')
   44                  return 2
   45          module.main = main
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/01-research-notes.md (at 2174265e9c, 3 lines)

```text
    1  # 01-research-notes
    2  
    3  A fixture for the renovation face of tools/lint-audit-artifacts (#641).
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/02-forward-audit.md (at 2174265e9c, 3 lines)

```text
    1  # 02-forward-audit
    2  
    3  A fixture for the renovation face of tools/lint-audit-artifacts (#641).
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/03-retrospective.md (at 2174265e9c, 3 lines)

```text
    1  # 03-retrospective
    2  
    3  A fixture for the renovation face of tools/lint-audit-artifacts (#641).
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/04-analysis.md (at 2174265e9c, 16 lines)

```text
    1  # 04 Analysis (fixture)
    2  
    3  ## Executive summary
    4  One finding.
    5  
    6  ## Acceptance-criteria scorecard
    7  The fixture's single criterion is met.
    8  
    9  ## Risk assessment
   10  None; a fixture.
   11  
   12  ## Coverage boundary
   13  The fixture's own files.
   14  
   15  ## Quality self-check
   16  The lint is the check.
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-fail/05-punch-list.md (at 2174265e9c, 18 lines)

```text
    1  # 05 Punch list (fixture)
    2  
    3  ## PL-01 Quote an expansion
    4  
    5  A fixture item.
    6  
    7  ## Phase 7 resolution gate
    8  
    9  | Item | Outcome |
   10  | --- | --- |
   11  | PL-01 | Resolved `abc1234` |
   12  
   13  ```yaml
   14  punch_index:
   15  - id: PL-01
   16    severity: low
   17    outcome: resolved
   18  ```
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/01-research-notes.md (at 2174265e9c, 3 lines)

```text
    1  # 01-research-notes
    2  
    3  A fixture for the renovation face of tools/lint-audit-artifacts (#641).
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/02-forward-audit.md (at 2174265e9c, 3 lines)

```text
    1  # 02-forward-audit
    2  
    3  A fixture for the renovation face of tools/lint-audit-artifacts (#641).
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/03-retrospective.md (at 2174265e9c, 3 lines)

```text
    1  # 03-retrospective
    2  
    3  A fixture for the renovation face of tools/lint-audit-artifacts (#641).
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/04-analysis.md (at 2174265e9c, 33 lines)

```text
    1  # 04 Analysis (fixture)
    2  
    3  ## Executive summary
    4  One finding.
    5  
    6  ## Acceptance-criteria scorecard
    7  The fixture's single criterion is met.
    8  
    9  ## Risk assessment
   10  None; a fixture.
   11  
   12  ## Coverage boundary
   13  The fixture's own files.
   14  
   15  ## Quality self-check
   16  The lint is the check.
   17  
   18  ## Renovation face
   19  
   20  ### Q1 Modernize
   21  Nothing to modernize in the fixture.
   22  ### Q2 Standards and best practices
   23  PL-01 is a quoting fix.
   24  ### Q3 Bugs
   25  PL-01.
   26  ### Q4 Package currency
   27  No package.
   28  ### Q5 Efficiency
   29  Nothing on the launch path.
   30  ### Q6 Dead ends
   31  None found.
   32  ### Q7 Clarity and structure
   33  None found.
```

## File: tools/test-fixtures/lint-audit-artifacts/fixture-epic-m6-renovation-pass/05-punch-list.md (at 2174265e9c, 19 lines)

```text
    1  # 05 Punch list (fixture)
    2  
    3  ## PL-01 Quote an expansion
    4  
    5  A fixture item.
    6  
    7  ## Phase 7 resolution gate
    8  
    9  | Item | Outcome |
   10  | --- | --- |
   11  | PL-01 | Resolved `abc1234` |
   12  
   13  ```yaml
   14  punch_index:
   15  - id: PL-01
   16    severity: low
   17    question: Q3
   18    outcome: resolved
   19  ```
```

## File: tools/usb-gadget-test (at 8ebaf8daad, 147 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
    4  """Exercise actual USB preparation functions in a disposable configfs fixture.
    5  
    6  Runs on the host or GENERIC_X64 guest; never invokes the script's hardware
    7  dispatch, a UDC, modprobe, network configuration, or an MTP daemon. The fixture
    8  models automatically created configfs directories, not kernel write semantics
    9  or USB enumeration. Pass an old --source to retain the failing control.
   10  """
   11  import argparse
   12  import hashlib
   13  import json
   14  import os
   15  from pathlib import Path
   16  import re
   17  import shlex
   18  import subprocess
   19  import tempfile
   20  
   21  
   22  VERSIONS = ("20241025", "20260901", "0.0.1", "0.0.1-dev", "0.0.1-rc.1",
   23              "0.0.1+20261011T000000Z.g123456789abc", "12.34.56", "rolling", "")
   24  SERIAL = "123456789abcdef0123456789abcdef012"
   25  
   26  
   27  def function(source, name):
   28      matches = re.findall(r"^" + re.escape(name) + r"\(\) \{\n.*?^\}",
   29                           source, re.M | re.S)
   30      if len(matches) != 1:
   31          raise ValueError("expected one complete function: " + name)
   32      return matches[0]
   33  
   34  
   35  FIXTURE = r'''
   36  # Model only configfs's automatic directories/attributes under the temp root.
   37  mkdir() {
   38      command mkdir "$@" || return $?
   39      for fixture_path do
   40          case "$fixture_path" in
   41              "$g_cdc"|"$g_mtp")
   42                  command mkdir -p "$fixture_path/strings" "$fixture_path/configs" \
   43                      "$fixture_path/functions" "$fixture_path/os_desc"
   44                  : > "$fixture_path/UDC"
   45                  : > "$fixture_path/max_speed"
   46                  ;;
   47              */configs/c.1)
   48                  command mkdir "$fixture_path/strings"
   49                  ;;
   50              */functions/ncm.usb0)
   51                  command mkdir -p "$fixture_path/os_desc/interface.ncm"
   52                  ;;
   53          esac
   54      done
   55  }
   56  '''
   57  
   58  
   59  def prepare(source, assignment, shell, version, mode, parent):
   60      root = parent / mode
   61      name = "prepare_usb_network" if mode == "cdc" else "prepare_usb_mtp"
   62      # Do not source the whole script: its prologue and dispatch touch hardware.
   63      script = "\n".join([
   64          "set -e", "verbose=0", "OS_NAME=pixelelated", "PRODUCT='Synthetic QA panel'",
   65          "SERIAL=" + shlex.quote(SERIAL), "OS_VERSION=" + shlex.quote(version),
   66          "g_cdc=" + shlex.quote(str(parent / "cdc")),
   67          "g_mtp=" + shlex.quote(str(parent / "mtp")), assignment,
   68          FIXTURE, function(source, name), name,
   69      ]) + "\n"
   70      result = subprocess.run([shell, "-c", script], capture_output=True, text=True,
   71                              timeout=15)
   72      values = {}
   73      for file in sorted(root.rglob("*")):
   74          relative = str(file.relative_to(root))
   75          if file.is_symlink():
   76              values[relative] = "->" + os.readlink(file).replace(str(parent), "$FIXTURE")
   77          elif file.is_file():
   78              values[relative] = file.read_text().strip()
   79      expected = {
   80          "bcdUSB": "0x0200", "bDeviceClass": "2" if mode == "cdc" else "0",
   81          "idVendor": "0x1d6b", "idProduct": "0x0104" if mode == "cdc" else "0x0100",
   82          "strings/0x409/manufacturer": "pixelelated",
   83          "strings/0x409/product": "Synthetic QA panel",
   84          "strings/0x409/serialnumber": SERIAL,
   85          "configs/c.1/bmAttributes": "0xC0", "configs/c.1/MaxPower": "0xfe",
   86          "configs/c.1/strings/0x409/configuration": "CDC" if mode == "cdc" else "mtp",
   87          "UDC": "", "max_speed": "" if mode == "cdc" else "high-speed",
   88      }
   89      if mode == "cdc":
   90          expected.update({
   91              "functions/ncm.usb0/os_desc/interface.ncm/compatible_id": "WINNCM",
   92              "functions/ncm.usb0/dev_addr": "82ba1c9278b1",
   93              "functions/ncm.usb0/host_addr": "123456789abc",
   94              "os_desc/use": "1", "os_desc/b_vendor_code": "0xcd",
   95              "os_desc/qw_sign": "MSFT100",
   96              "configs/c.1/ncm.usb0": "->$FIXTURE/cdc/functions/ncm.usb0",
   97          })
   98      else:
   99          expected["configs/c.1/ffs.mtp"] = "->$FIXTURE/mtp/functions/ffs.mtp"
  100      revision = values.pop("bcdDevice", "")
  101      valid_bcd = re.fullmatch(r"0x[0-9]{4}", revision) is not None
  102      checks = {
  103          "function_exited_zero": result.returncode == 0,
  104          "four_digit_bcd": valid_bcd,
  105          "descriptor_revision_1_00": revision == "0x0100",
  106          "other_descriptor_bytes_and_links_preserved": values == expected,
  107      }
  108      return {"version": version, "mode": mode, "bcdDevice": revision,
  109              "checks": checks, "returncode": result.returncode,
  110              "stdout": result.stdout, "stderr": result.stderr,
  111              "attributes_without_revision": values}
  112  
  113  
  114  def main():
  115      parser = argparse.ArgumentParser(description=__doc__)
  116      parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1]
  117                          / "projects/ROCKNIX/packages/rocknix/sources/scripts/usbgadget")
  118      parser.add_argument("--shell", default="/bin/sh")
  119      parser.add_argument("--output", type=Path, required=True)
  120      args = parser.parse_args()
  121      data = args.source.read_bytes()
  122      source = data.decode()
  123      assignments = re.findall(r"^devversion=.*$", source, re.M)
  124      if len(assignments) != 1:
  125          parser.error("expected one shared revision assignment")
  126      rows = []
  127      for version in VERSIONS:
  128          with tempfile.TemporaryDirectory(prefix="pix-usb-fixture-") as directory:
  129              for mode in ("cdc", "mtp"):
  130                  rows.append(prepare(source, assignments[0], args.shell, version,
  131                                      mode, Path(directory)))
  132      failed = sum(not passed for row in rows for passed in row["checks"].values())
  133      report = {"source_sha256": hashlib.sha256(data).hexdigest(),
  134                "shell": args.shell, "shell_resolved": str(Path(args.shell).resolve()),
  135                "cases": rows, "checks": len(rows) * 4, "failed": failed,
  136                "fixture_only": True, "physical_enumeration_tested": False}
  137      # Exclusive output prevents overwriting the original failed control.
  138      with args.output.open("x") as stream:
  139          json.dump(report, stream, indent=2)
  140          stream.write("\n")
  141      print(f"{'FAIL' if failed else 'PASS'} USB descriptor fixture: "
  142            f"{len(rows)} cases, {len(rows) * 4 - failed}/{len(rows) * 4} checks")
  143      return 1 if failed else 0
  144  
  145  
  146  if __name__ == "__main__":
  147      raise SystemExit(main())
```

## File: tools/wait-lock-test (at 8ebaf8daad, 159 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # wait-lock-test - a device-less check of wait_lock() in
    6  # projects/ROCKNIX/packages/rocknix/profile.d/001-functions, the settings lock
    7  # every get_setting/set_setting, runemu.sh, backuptool and the cloud scripts
    8  # share (fork #98):
    9  #
   10  #   - a STALE lock (its pid is dead, or the file is empty or not a pid) is
   11  #     removed, logged with the pid, and the caller proceeds within two seconds;
   12  #   - a LIVE holder is honoured for as long as it lives, and never stolen;
   13  #   - a long live wait is logged once, naming the holder, not every second.
   14  #
   15  # It lifts wait_lock() (and wait_lock_say(), where the copy has one) out of
   16  # the 001-functions it is given, points J_CONF_LOCK at a temp file, and runs
   17  # what set_setting does -- `wait_lock; rm -f "$J_CONF_LOCK"` -- in a fresh
   18  # bash under `timeout`, so a function that spins forever is a FAIL here and
   19  # not a hung test. `logger` is shadowed by a function so the line that would
   20  # reach syslog is read back; one case removes logger from PATH to see the
   21  # stderr fallback. To watch the guard fire, point it at the function from
   22  # before the change:
   23  #
   24  #     git show 8ccc244dfa:projects/ROCKNIX/packages/rocknix/profile.d/001-functions > /tmp/old
   25  #     tools/wait-lock-test /tmp/old      # FAILs: a stale lock hangs until the timeout
   26  #     tools/wait-lock-test               # PASSED
   27  #
   28  # Host tool: needs GNU `date +%s%N` and coreutils `timeout`. The functions
   29  # under test are the ones that run on the device, unchanged.
   30  #
   31  # Exit 0 when every check passes, 1 otherwise, 2 when it cannot run.
   32  set -u
   33  
   34  SCRIPT="${1:-$(dirname "$(readlink -f "$0")")/../projects/ROCKNIX/packages/rocknix/profile.d/001-functions}"
   35  [ -r "${SCRIPT}" ] || { echo "cannot read ${SCRIPT}" >&2; exit 2; }
   36  
   37  # wait_lock() as the file defines it, and its helper if it has one. It reads
   38  # J_CONF_LOCK and calls sleep, rm, cat (in the trap), kill, read, logger.
   39  FUNCS="$(sed -n '/^function wait_lock_say() {/,/^}/p; /^function wait_lock() {/,/^}/p' "${SCRIPT}")"
   40  grep -q '^function wait_lock() {' <<<"${FUNCS}" || { echo "no wait_lock() found in ${SCRIPT}" >&2; exit 2; }
   41  command -v timeout >/dev/null || { echo "needs coreutils timeout" >&2; exit 2; }
   42  
   43  TMP="$(mktemp -d)"; trap 'rm -rf "${TMP}"' EXIT
   44  LOCK="${TMP}/system.cfg.lock"
   45  FAIL=0
   46  
   47  check() { # <0|nonzero> ok-text bad-text
   48      if [ "$1" -eq 0 ]; then echo "    PASS  $2"; else echo "    FAIL  $3"; FAIL=$((FAIL + 1)); fi
   49  }
   50  now_ms() { echo $(( $(date +%s%N) / 1000000 )); }
   51  
   52  # What set_setting does: take the lock, do the work, release it. Prints HELD
   53  # when the file names this shell after wait_lock returns -- the lock was taken,
   54  # not merely waited past. PREAMBLE is eval'd first so a case can shadow
   55  # logger or sleep, or narrow PATH.
   56  {
   57      printf '%s\n' "${FUNCS}"
   58      printf 'J_CONF_LOCK=%q\n' "${LOCK}"
   59      cat <<'EOF'
   60  eval "${PREAMBLE:-}"
   61  wait_lock
   62  if [ "$(cat "${J_CONF_LOCK}" 2>/dev/null)" = "$$" ]; then echo HELD; else echo "NOT-HELD:$(cat "${J_CONF_LOCK}" 2>/dev/null)"; fi
   63  rm -f "${J_CONF_LOCK}"
   64  EOF
   65  } > "${TMP}/take.sh"
   66  
   67  # take <timeout-s> <preamble>: runs take.sh; stdout to $OUT, stderr to $ERR,
   68  # rc in $RC (124 is timeout's "it hung"), wall time in $MS.
   69  OUT="${TMP}/out"; ERR="${TMP}/err"
   70  take() {
   71      local t0 t1
   72      t0=$(now_ms)
   73      PREAMBLE="$2" timeout "$1" bash "${TMP}/take.sh" >"${OUT}" 2>"${ERR}"
   74      RC=$?
   75      t1=$(now_ms)
   76      MS=$((t1 - t0))
   77  }
   78  FAKE_LOGGER='logger() { echo "logger $*" >&2; }'
   79  
   80  # A pid that is not running: start high and walk down until kill -0 fails.
   81  DEAD=$(( (1 << 22) - 1 ))
   82  while kill -0 "${DEAD}" 2>/dev/null; do DEAD=$((DEAD - 1)); done
   83  
   84  echo "wait-lock-test: wait_lock() from ${SCRIPT}"
   85  
   86  echo "  1. a stale lock -- the file names pid ${DEAD}, which is not running"
   87  echo "${DEAD}" > "${LOCK}"
   88  take 4 "${FAKE_LOGGER}"
   89  [ "${RC}" -eq 0 ] && grep -qx HELD "${OUT}"; check $? "wait_lock returned and the lock was taken (rc 0, HELD)" "rc ${RC} (124 = hung until the timeout), stdout '$(cat "${OUT}")'"
   90  [ "${MS}" -lt 2000 ]; check $? "in under two seconds (${MS} ms)" "took ${MS} ms"
   91  [ ! -e "${LOCK}" ]; check $? "the lock file is gone afterwards" "the lock file is still there"
   92  grep -q -- "-t wait_lock .*stale.*${DEAD}" "${ERR}"; check $? "one syslog line, tagged wait_lock, says the stale lock held by ${DEAD} was removed" "no such line; stderr: '$(tr '\n' '|' < "${ERR}")'"
   93  [ "$(grep -c 'stale' "${ERR}")" = 1 ]; check $? "and exactly one" "$(grep -c 'stale' "${ERR}") stale lines"
   94  
   95  # A holder that behaves like a real caller: writes its pid, works, releases.
   96  hold_and_release() { # <seconds>
   97      bash -c 'echo $$ > "$1"; sleep "$2"; rm -f "$1"' _ "${LOCK}" "$1" &
   98      HOLDER=$!
   99  }
  100  
  101  echo "  2. a live holder -- a caller that owns the file for 3 s and then releases it; the wait must outlive it and never steal it"
  102  rm -f "${LOCK}"
  103  hold_and_release 3
  104  until [ -s "${LOCK}" ]; do sleep 0.05; done
  105  t0=$(now_ms)
  106  PREAMBLE="${FAKE_LOGGER}" timeout 8 bash "${TMP}/take.sh" >"${OUT}" 2>"${ERR}" & TAKER=$!
  107  sleep 1.5
  108  kill -0 "${TAKER}" 2>/dev/null; check $? "1.5 s in, the caller is still waiting" "the caller had already returned 1.5 s in"
  109  [ "$(cat "${LOCK}" 2>/dev/null)" = "${HOLDER}" ]; check $? "and the live holder still owns the lock (not stolen)" "the lock file reads '$(cat "${LOCK}" 2>/dev/null)', not the holder's ${HOLDER}"
  110  wait "${TAKER}"; RC=$?
  111  MS=$(( $(now_ms) - t0 ))
  112  wait "${HOLDER}" 2>/dev/null
  113  [ "${RC}" -eq 0 ] && grep -qx HELD "${OUT}"; check $? "the caller took the lock once the holder released it (rc 0, HELD)" "rc ${RC} (124 = hung until the timeout), stdout '$(cat "${OUT}")'"
  114  [ "${MS}" -ge 2500 ]; check $? "after waiting at least 2.5 s (${MS} ms)" "returned after only ${MS} ms"
  115  ! grep -q 'stale' "${ERR}"; check $? "nothing was reported as stale" "a live holder was reported stale: '$(tr '\n' '|' < "${ERR}")'"
  116  
  117  echo "  3. a holder killed mid-wait (SIGKILL, so it cannot release) -- the caller must proceed within a poll of the kill"
  118  rm -f "${LOCK}"
  119  bash -c 'echo $$ > "$1"; exec sleep 30' _ "${LOCK}" & HOLDER=$!
  120  until [ -s "${LOCK}" ]; do sleep 0.05; done
  121  t0=$(now_ms)
  122  PREAMBLE="${FAKE_LOGGER}" timeout 8 bash "${TMP}/take.sh" >"${OUT}" 2>"${ERR}" & TAKER=$!
  123  sleep 1.5
  124  [ "$(cat "${LOCK}" 2>/dev/null)" = "${HOLDER}" ] && kill -0 "${TAKER}" 2>/dev/null; check $? "1.5 s in, the live holder still owns the lock and the caller is waiting" "lock reads '$(cat "${LOCK}" 2>/dev/null)' (holder ${HOLDER}); caller alive: $(kill -0 "${TAKER}" 2>/dev/null && echo yes || echo no)"
  125  kill -9 "${HOLDER}" 2>/dev/null; wait "${HOLDER}" 2>/dev/null
  126  tk=$(now_ms)
  127  wait "${TAKER}"; RC=$?
  128  MS=$(( $(now_ms) - tk ))
  129  [ "${RC}" -eq 0 ] && grep -qx HELD "${OUT}"; check $? "the caller took the lock after the holder was killed (rc 0, HELD)" "rc ${RC} (124 = hung until the timeout), stdout '$(cat "${OUT}")'"
  130  [ "${MS}" -lt 2000 ]; check $? "within two seconds of the kill (${MS} ms)" "took ${MS} ms after the kill"
  131  grep -q -- "-t wait_lock .*stale.*${HOLDER}" "${ERR}"; check $? "one syslog line says the stale lock held by ${HOLDER} was removed" "no such line; stderr: '$(tr '\n' '|' < "${ERR}")'"
  132  
  133  echo "  4. an empty lock file is stale; with no logger on PATH the line goes to stderr"
  134  mkdir -p "${TMP}/bin"
  135  for t in rm sleep cat; do ln -s "$(command -v "${t}")" "${TMP}/bin/${t}"; done
  136  : > "${LOCK}"
  137  take 4 "PATH=${TMP}/bin"
  138  [ "${RC}" -eq 0 ] && grep -qx HELD "${OUT}"; check $? "wait_lock returned and the lock was taken (rc 0, HELD)" "rc ${RC} (124 = hung until the timeout), stdout '$(cat "${OUT}")'"
  139  [ "${MS}" -lt 2000 ]; check $? "in under two seconds (${MS} ms)" "took ${MS} ms"
  140  grep -q '^wait_lock: removed stale lock' "${ERR}"; check $? "the removal was said on stderr, prefixed wait_lock:" "no fallback line; stderr: '$(tr '\n' '|' < "${ERR}")'"
  141  
  142  echo "  5. a file whose content is not a pid is stale"
  143  echo "not-a-pid" > "${LOCK}"
  144  take 4 "${FAKE_LOGGER}"
  145  [ "${RC}" -eq 0 ] && grep -qx HELD "${OUT}" && [ "${MS}" -lt 2000 ]; check $? "removed and taken in under two seconds (${MS} ms)" "rc ${RC} after ${MS} ms, stdout '$(cat "${OUT}")'"
  146  
  147  echo "  6. a long live wait is logged once, naming the holder (the caller's sleep shadowed, so 30 polls take no time)"
  148  rm -f "${LOCK}"
  149  hold_and_release 2
  150  until [ -s "${LOCK}" ]; do sleep 0.05; done
  151  take 8 "${FAKE_LOGGER}; sleep() { :; }"
  152  wait "${HOLDER}" 2>/dev/null
  153  [ "${RC}" -eq 0 ] && grep -qx HELD "${OUT}"; check $? "the caller took the lock once the holder released it (rc 0, HELD)" "rc ${RC} (124 = hung until the timeout), stdout '$(cat "${OUT}")'"
  154  n=$(grep -c -- "-t wait_lock .*${HOLDER}" "${ERR}")
  155  [ "${n}" = 1 ]; check $? "exactly one syslog line names the live holder ${HOLDER}" "${n} line(s) name the holder; stderr: '$(tr '\n' '|' < "${ERR}" | cut -c1-300)'"
  156  ! grep -q 'stale' "${ERR}"; check $? "and it was never called stale" "a live holder was reported stale"
  157  
  158  echo
  159  if [ "${FAIL}" -eq 0 ]; then echo "PASSED"; exit 0; else echo "${FAIL} CHECK(S) FAILED"; exit 1; fi
```

## The stage-A run lines (exit, wall, last line)

```text
wait-lock-test rc=0 7.5s | PASSED
rocknix-info-test rc=0 0.5s | PASS 12 full-script positive/negative controls
nova-led-test rc=0 0.2s | 14 PASS, 0 FAIL
usb-gadget-test rc=0 0.3s | PASS USB descriptor fixture: 18 cases, 72/72 checks
state-check-self rc=0 9.1s | }
build-identity rc=1 0.2s | FAIL build identity: 21 passed, 2 failed
retroarch-wrapper-test rc=0 0.1s | PASS: every command ran exactly once
retroarch-wrapper-test (bare) rc=2 | retroarch-wrapper-test: no video_thread_wrapper.c given and none under /workspace/repos/rocknix.worktrees/devi
rasteratops-identity-check rc=1 0.1s | identity source contracts: 6 failure(s); image qualification still required
rasteratops-identity-check rc=1 0.1s | identity source contracts: 1 failure(s); image qualification still required
settings-modes-test (image busybox) rc=0 0.4s | PASS refuse-rename
melonds-upgrade-test (image busybox) rc=0 0.1s | PASS temp-failure
settings-modes-test (host busybox) rc=0 0.4s | PASS refuse-rename
melonds-upgrade-test (host busybox) rc=0 0.1s | PASS temp-failure
cloud-layout rc=1 0.1s | AssertionError: migration matrix retired by #508; use --ref for historical source or --archives-only for ordin
cloud-validator rc=1 0.1s | AssertionError: Use the package-pinned rclone1.75.1, not the host fallback: rclone v1.75.2
content-scope rc=1 3.4s | PASS absolute-root-unreadable-bounded
save-layout rc=0 29.2s | save-layout: 39 PASS, 0 FAIL
duckstation rc=1 0.1s | AssertionError: use package-pinned rclone: rclone v1.75.2
cloud-layout --archives-only rc=1 9.2s | cloud-layout-test: 11 PASS, 2 FAIL; artifacts: /workspace/tmp/m6-t14/out/cloud-layout
cloud-layout --archives-only, TMPDIR unset, rc=0 19.8s | cloud-layout-test: 13 PASS, 0 FAIL; artifacts: /workspace/tmp/m6-t14/out-notmp/cloud-layou
content-scope, TMPDIR unset, rc=1 3.3s | PASS 19 FAIL 2

```