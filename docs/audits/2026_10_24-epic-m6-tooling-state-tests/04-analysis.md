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
