# Analysis: M6.P2 T14, the last-good, settings and state tests (#661)

Read at `8ebaf8daad` (the 22) and `2174265e9c` (the ten lint fixtures). The lens is brittleness.
- **Sources of the per-tool facts:** two read-only research passes, both re-derived here (each claim below is either a line read in this session or a run recorded in `00`); the stage-A runs; and the constructed inputs recorded as `PROOF:` lines in `00`.
- **Legend:** *false PASS*, *false FAIL* and *fails closed* name what a missing dependency does to the verdict.

## Executive summary

- **The scope:** 21 test tools and 11 fixture files that prove the fork's OS scripts, cloud layout, settings writers, release identity and hardware quirks. They were read at `8ebaf8daad` (the ten lint fixtures at `2174265e9c`) through the brittleness lens, with one GPT-6 Astra seat at `max`.
- **What the slice found:** the family is the qualification record of M7's issues. Each test was written to qualify one fix, and most were never run again.
- **Failing at the hash with the package's own inputs, nobody noticing:** six tests (F-01 to F-05). In three, the test asserts a past state of the tree (a gate's input, a licence string, an rclone version). In one, the script got safer and the test did not follow. In one, the sandbox inherits the caller's `TMPDIR`.
- **The sandbox is wider than that:** the seat showed that the shared rclone sandbox passes every caller variable and keeps the host network (G-1, now F-04, High).
- **Passing without proving:** two constructed false PASSes (F-06, F-07), and twenty more cases the seat found in which a test can pass without exercising what it names.
- **No caller:** 14 of the 21 tools are run by nothing in the tree.
- **The punch list:** 23 items. 17 are bugs (#989 to #1005), 5 are Renovation items for the coordinator's disposition (the guest pair, the stubs, the no-caller class into #986, the index rows, the state check's stated guarantee), and 1 is conditional on T10's merge.
- **No guest cycle** was needed, and no tool was edited.

## Acceptance-criteria scorecard

#661's 18 criteria, at the end of stage D. The final state is the hand-back's.

| # | Criterion | State | Evidence |
| ---: | --- | --- | --- |
| 1 | 00 to 05 | written | this folder |
| 2 | lint PASS | pre-issue at stage D, resolution at close | `00` |
| 3 | review-plan.json, the seat's provenance, the packet's scan | done | `second-opinions/`; `00` § Stage C |
| 4 | the punch-list issue's items at an outcome | stage E onward | the audit issue |
| 5 | `reviewed-at` and `fixed-at` | `reviewed-at` `30da4853bb`; both are written at hand-back | #661 |
| 6 | `01` § Scope | done | `01` |
| 7 | the coverage table, 32 rows | done (the awk prints 32) | `02` § Coverage |
| 8 | § The runs | done | `02` |
| 9 | § The guest cycle | none needed, the reason recorded | `02` |
| 10 | `00`'s never-run list | holds | `00` |
| 11 | Q6's brittleness table | done, 21 rows | § Q6 |
| 12 | Q3's hunt | done, every tool | § Q3 |
| 13 | Q7's descriptions | done | § Q7 |
| 14 | Q5's costs | done | § Q5 |
| 15 | every proof with its cell; the counts equal | 8 = 8 | `02` § Proofs |
| 16 | `question:` on every item; the bugs pass box-check; no tool edited | 23 of 23 carry `question:`; 17 of 17 pass `box-check --issue`; no member changed | `05`; `00` |
| 17 | the retro | stage G | — |
| 18 | the six checkers and the lint | stage H | — |

## Risk assessment

- **The sandbox (F-04, High):** a caller's environment reaches every real-rclone test's scripts, and three of those tests keep the host network. A caller environment carrying a real remote's definition could point a test at a real cloud. No recorded run did: `vm-qa` runs T15 without such variables. This is the slice's one security-grade item.
- **Silent rot:** six tests fail today and nothing would have said so. Any of them used later for a candidate would have cost a round to diagnose.
- **The release preparer's tools:** the state check's readiness evidence (PL-16 in `05`, G-25) and the candidate store's path binding (G-38) are gate inputs, and changing what the gates require is the coordinator's (`release-candidates.md`).
- **Guests:** the guest pair cannot touch a guest on this tree (both refuse). Their historical path can kill an unowned QEMU by substring (G-2).

## Coverage boundary

- **Read:** the 32 files whole, at their read refs.
- **Read where they call or are called:** T15's four call sites (never edited), `vm-qa:185`, `fork-checks.yml:50` and `fork-publish-release`'s calls.
- **Not read:** the production scripts these tests drive, except where a trace needed a line (`backuptool:239`, `cloud_content_restore`'s refusal); `tools/vm-pair` and `tools/cloud-test-backend` (T12's).
- **Not run:**
  - the two guest tests past their refusal;
  - `pixelelated-state-check-test --payload-tests` (`mcopy` absent);
  - `fork-publish-release` beyond what `build-identity-test` calls;
  - the state gate and the candidate store against anything real.
- **The record searched:** `docs/qa-logs/`, the work logs and `git log` per tool. No blindspot entry names any of the 21.

## Findings (Phase 4)

| ID | Finding | Q | Draft severity | Evidence |
| --- | --- | --- | --- | --- |
| F-01 | `build-identity-test` fails at the hash: its firmware stand-in (`:132`, the bytes `SYNTHETIC FIRMWARE ONLY`) is refused by the `pixelelated-state-check` gate `fork-publish-release` gained at `d9f428e1a0`; 21 passed, 2 failed | Q3 | Medium | `00` § Stage A; `.qa-scratch/t14/out/build-identity` |
| F-02 | `rasteratops-identity-check` fails at the hash: `:143` expects `PKG_LICENSE == "MIT"`, and the recipe has said `MIT AND BSD-3-Clause` since `84ff94fb3d` (2026-10-13); 38 PASS, 1 FAIL | Q3 | Medium | `00` § Stage A |
| F-03 | `pixelelated-cloud-validator-test:58` and `pixelelated-duckstation-capture-test:178` require `rclone v1.75.1`. The pin is 1.75.2 since `a0f60255ab` (2026-10-11), so both refuse the package's own binary. The retired stub's docstring names the same version as current coverage (`pixelelated-cloud-folder-test`) | Q3, Q1 | Medium | `00` § Stage A |
| F-04 | The sandbox every rclone test shares, `rasteratops-cloud-layout-test`'s `Fixture.run` (`:138-147`), sets `HOME` and `PATH` and passes the caller's other variables through. A caller's `TMPDIR` names a path not mounted inside, so `backuptool`'s `mktemp` fails: 2 false FAILs (`T24-local-*-recovery`), 13 of 13 with `TMPDIR` unset. The validator's (`:326-335`) and DuckStation's (`:123-151`) sandboxes have no `--clearenv` either; `RCLONE_CONFIG` would pass the same way (inference, not seen) | Q2, Q3 | Medium | `00` § Stage B, trace 1 |
| F-05 | `pixelelated-content-scope-test` fails at the hash: `system-traversal-refused` and `content-pointer-traversal-refused` read `ctl/argv` unconditionally (`:132`, `:222`; `:121` belongs to the provider-failure helper, G-9), and the script now refuses `..` before calling rclone (`e6645cb5ea`), so the read raises before the assertion. It is a false FAIL over a property that holds, unseen because nothing calls the test | Q3 | Medium | `00` § Stage B, trace 2 |
| F-06 | `pixelelated-cloud-validator-test --case <a name that matches nothing>` returns early from every case and writes `{"result": "PASS", "cases": []}`, `PASS 0 controls`, rc 0 (`:63`, `:356-357`). It is a false PASS, T12's `--only` shape | Q3 | Low | `PROOF: P5` |
| F-07 | `rocknix-info-test`'s verdict is `assert` (`:29`) with an unconditional `PASS` print (`:58`). Under `python3 -O` a constructed regression (a quirk failure that no longer propagates) is recorded failed in `result.json` while the tool prints `PASS 12` and exits 0. CI runs it without `-O`, so this is latent. `nova-led-test:50` has the same shape for the ledcontrol exit | Q2 | Low | `PROOF: P4` |
| F-08 | `retroarch-wrapper-test` leaves `<tmp>/t` and `t.c` behind (`:213`). Its two default roots are #640's retired layout (`:42-43`), so it exits 2 bare. A missing `gcc` raises at `:216` and exits 1, the code its docstring reserves for *the command ran twice* (`:27`) | Q2, Q1 | Low | `00` § Stage A |
| F-09 | `pixelelated-vm-cloud-boundaries` stops its guests by scanning `/proc/*/cmdline` for its owned pair path and signalling (`:675-690`), not by `vm-stop` and the pidfile. Under a sandbox that hides host PIDs (#506) it would find none and record `all_absent: True` (inference) | Q2 | Low | the source, `:675-690` |
| F-10 | Both guest tests refuse every run against current source, because `cloud_migrate_layout` is absent at the hash. They accept a historical source tree, which is fail-closed behaviour, not a defect (G-14) (`pixelelated-vm-cloud-boundaries:709-710`, rc 1; `rasteratops-vm-cloud-epic:22-25`, rc 2). With the two retired stubs, four of the 21 tools refuse against current source, and the guest pair's index rows do not say so | Q6 | Renovation | `00` § Stage A |
| F-11 | 14 of the 21 tools are invoked by nothing in the tree. The first count, 13, missed `pixelelated-cloud-validator-test`, which the stubs only name (G-15). Confirmed by `git grep` over `tools`, `.github/workflows`, `.claude/skills` and `.githooks`, the personal-paths list not counted. Of these, 7 non-stub tools fail or refuse at the hash and nobody saw it: `build-identity-test`, `rasteratops-identity-check`, the two rclone-pin tests, content-scope, and the guest pair | Q6 | Renovation | § Q6 |
| F-12 | 13 of the 21 index rows name a *Detail in* rule that never names the tool. The two retired stubs' `fork-workflow.md` list entries carry no *retired* note | Q7 | Renovation | § Q7 |
| F-13 | `settings-modes-test` and `melonds-upgrade-test` take any `--busybox` and run it as the candidate's. T15's `image_tool_source` (`last-good-scripts-test:381-400`) ends in `command -v busybox \|\| true`, so with no build root a host's busybox passes as the image's, unmarked. This host has one (BusyBox 1.37.0), and both tests passed under it. `pixelelated-save-layout-test` without `--busybox` silently uses the host's `find` and `awk` (`:393`) | Q3 | Low | `00` § Stage A; `02` § T15's call sites |
| F-14 | `pixelelated-duckstation-capture-test`'s `package_install` case runs the installed synthetic payload on the host, outside its `bwrap` (`:334`) | Q2 | Low | the source |
| F-15 | *Withdrawn after the seat (G-19):* `check(True, ...)` follows a successful parse, and the USB header says host or guest. G-36 is the identity check's real defect | — | — | — |

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

**The seat:**
- **Probe:** 20:45:38 to 20:45:47Z. Served `openai/gpt-6-astra` by OpenAI at `max`; identity, effort and provider PASS.
- **Refutation:** 20:46:18 to 21:11:19Z, first attempt, `finish=stop`. 47,033 bytes, 146,499 prompt and 61,214 completion tokens (50,762 reasoning), 1,501,038 ms. Served `openai/gpt-6-astra` by OpenAI at `max`; verification, effort and provider PASS (`second-opinions/gpt-audit.md.provenance.json`).
- **Its output, scanned before it was read:** `forbidden-terms-check --stdin` 0 hits, and 0 credential-pattern lines.
- **What it returned:** 42 items, G-1 to G-42. Each is graded below against the line it cites, re-read in this session, or against a run. Where the seat could not see an artifact (the index, the caller grep, the commit history), the artifact named here decided it.

| Item | Grade | The artifact that decided it | Severity here | Into |
| --- | --- | --- | --- | --- |
| G-1 | **confirmed, and widens F-04.** `Fixture.run` asks only `--unshare-pid` (`rasteratops-cloud-layout-test:138`), so the host network is reachable. `/etc` is bound read-only, and every caller variable except `HOME` and `PATH` passes (`RCLONE_CONFIG`, `RCLONE_CONFIG_<REMOTE>_*`, `BASH_ENV`, exported functions). The validator's adoption sandbox (`:326-335`) is the same. Save-layout (`--unshare-net`, `:94`) and DuckStation (`--unshare-all`) do isolate the network | `:138-147` re-read | High | PL-04 |
| G-2 | confirmed | `pixelelated-vm-cloud-boundaries:674-694`, `:711-716` re-read: `cleanup()` runs from `finally` and signals any `qemu-system-*` whose argv contains the pair path as a substring; empty discovery writes `all_absent: True`. The epic's pidfile check is not bound to its socket or ports. **Latent:** the retirement `require` at `:709` comes before the `try`, so on this tree cleanup never runs | Medium | PL-09 |
| G-3 | confirmed, and narrows the claim | `pixelelated-state-check:100-112`, `:366-371`: raw `unsquashfs -cat` output goes to a private `TemporaryFile`, and payload copies go to a private scratch directory. No report path discloses a value. The accurate guarantee is "no value in reports" | Low | PL-17 |
| G-4 | confirmed (= F-13) | `settings-modes-test:9`, `:26`; `melonds-upgrade-test:43`; T15 `:381-400` | Medium | PL-13 |
| G-5 | confirmed (= F-01) | stage-A run; `build-identity-test:132`, `:145`, `:169` (the second FAIL is the harness line) | Medium | PL-01 |
| G-6 | confirmed (= F-02) | stage-A run; recipe history read in `00` | Medium | PL-02 |
| G-7 | confirmed (= F-03) | stage-A runs | Medium | PL-03 |
| G-8 | confirmed: F-04 understated | G-1's lines | High | PL-04 |
| G-9 | confirmed, with a line correction: `:132`, not `:121` | `pixelelated-content-scope-test:129-133` re-read | Medium | PL-05 |
| G-10 | confirmed (= F-06); severity raised | P5 | Medium | PL-06 |
| G-11 | confirmed (= F-07); `PYTHONOPTIMIZE` is a second trigger | P4; `rocknix-info-test:29`, `:58` | Medium | PL-07 |
| G-12 | confirmed (= F-08), with its qualifications | `retroarch-wrapper-test:213-219` | Low | PL-08 |
| G-13 | confirmed: F-09 understated (a substring kill, after a refusal) | G-2's lines | Medium (latent) | PL-09 |
| G-14 | **accepted: F-10 overstated.** The four refuse on current source and accept a historical one. That is fail-closed, not broken. F-10 is reworded | `pixelelated-vm-cloud-boundaries:699-710`; `rasteratops-vm-cloud-epic:20-25` | Renovation | PL-09, PL-10 |
| G-15 | **accepted: the counts were wrong.** By invocation `pixelelated-cloud-validator-test` has no caller either (the stubs only name it), so the no-caller tools are **14**. The broken or refusing non-stub tools among them are **7**: `build-identity-test`, `rasteratops-identity-check`, the two rclone-pin tests, content-scope, and the guest pair | P7's grep, rerun per tool for the validator | — | F-11 corrected; PL-11 |
| G-16 | partly accepted. The seat could not see the index; P8 read it (`.qa-scratch/t14/q7-index.txt`, 13 rows). The seat is right that a rule can govern a tool without naming it, so F-12 is a discoverability item, Low, not a correctness one | P8 | Renovation (Low) | PL-12 |
| G-17 | confirmed for the writers; save-layout narrowed (its header disclaims image qualification) | `pixelelated-save-layout-test:2-6` | Medium | PL-13 |
| G-18 | accepted: F-14 narrowed. The bytes executed must equal the fixed synthetic payload (`:325`, `:332`), so this is a host-exec dependency, not product code on the host | `pixelelated-duckstation-capture-test:324-342` | Low | PL-14 |
| G-19 | **accepted: F-15 refuted.** `check(True, ...)` is reached only after `ET.parse` succeeds, and the `except` calls `check(False, ...)` (`rasteratops-identity-check:103-111`). The USB header says *host or GENERIC_X64 guest* (`usb-gadget-test:6`). **F-15 is withdrawn**; G-36 replaces its identity half | both re-read | — | F-15 withdrawn |
| G-20 | confirmed, severity lowered. The fixture's `run()` drops `args[1]`, the stage, and calls `[module.RCLONE] + args[2:]`. The guard refuses only the exact pair real `subprocess` plus `/usr/bin/rclone` (`cloud_connections_fixture.py:22-27`). Every T15 application replaces `subprocess` with a table-answered fake (`last-good-scripts-test:5062-5067`), so it is latent | the fixture and T15 re-read | Medium | PL-15 |
| G-21 | confirmed on the historical path | `rasteratops-vm-cloud-epic:127-138` (no `set -e`; an unconditional `rm` after a failed setup) | Medium (latent) | PL-09 |
| G-22 | confirmed on the historical path | `pixelelated-vm-cloud-boundaries:352-355` (`test -s ...; rm -f ...` returns `rm`'s status) | Medium (latent) | PL-09 |
| G-23 | confirmed | content-scope `:249-252`; DuckStation `:181-183`; the epic `:11-15`, `:400-402` | Low | PL-05, PL-14, PL-09 |
| G-24 | confirmed | `pixelelated-cloud-validator-test:75` (`all()` over an unchecked list) | Medium | PL-06 |
| G-25 | **confirmed, in a release gate's evidence.** `pixelelated-state-check:839` accepts `/usr/bin/autostart` anywhere in `ExecStart`, an argument included. Changing the gate's readiness evidence is a lead for the coordinator (`release-candidates.md`); the bug states the counterexample | re-read | Medium | PL-16 |
| G-26 | confirmed | `pixelelated-cloud-validator-test:267-268` | Medium | PL-06 |
| G-27 | confirmed | `:175-178` (2.2 MB of `x` is not JSON); the timeout case measures no time | Medium | PL-06 |
| G-28 | confirmed | `rasteratops-cloud-layout-test:1036-1042` (`any()` over a suffix the input archive already satisfies) | Medium | PL-21 |
| G-29 | confirmed | `:295-301` (`settle_failure` asserts no nonzero caller rc); content-scope's fault not witnessed | Medium | PL-21, PL-05 |
| G-30 | confirmed, with the seat's correction to Q3 (a script with no rclone call at all fails at `:77`; local discovery followed by a no-op passes) | `pixelelated-content-scope-test:65-84` | Medium | PL-05 |
| G-31 | confirmed on the historical (migration) path | `rasteratops-cloud-layout-test:627-677`, `:889-907` | Low (historical) | PL-21 |
| G-32 | confirmed (= Q3's row, sharpened) | `pixelelated-state-check-test:125-137`, `:772` | Medium | PL-18 |
| G-33 | confirmed on the historical path | `rasteratops-vm-cloud-epic:65-70`, `:304`, `:334-340` | Medium (latent) | PL-09 |
| G-34 | confirmed | `retroarch-wrapper-test:111`, `:123`, `:203` (one global counter compared with the post count) | Medium | PL-08 |
| G-35 | confirmed | `wait-lock-test:59-64` (`wait_lock`'s status is not checked); no two-fresh-acquirer case | Medium | PL-20 |
| G-36 | confirmed (replaces F-15's identity half) | `rasteratops-identity-check:39-41`, `:103-109` (an empty `<gameList/>` passes; `value()` takes the first assignment) | Medium | PL-02 |
| G-37 | confirmed (= Q6's `.replace` note, made a finding) | `nova-led-test:35-41`; `rocknix-info-test:21-26` | Medium | PL-07 |
| G-38 | confirmed | `rasteratops-candidate-store:30`, `:57` (`verify(args.bundle.resolve())` compares the resolved name) | Medium | PL-19 |
| G-39 | confirmed | `settings-modes-test:10` (the busybox path unquoted in each wrapper) | Low | PL-13 |
| G-40 | confirmed | `pixelelated-save-layout-test:393-398` | Low | PL-22 |
| G-41 | confirmed as custody (not alleged in the recorded runs) | the cited receipt lines | Low | PL-13, PL-06, PL-22 |
| G-42 | conditional, and left open: T10's `run.sh` (`2444828e89`, off this branch) asserts named diagnostics, so whether the pair proves each guard independently depends on it | the two fixture folders | Low | PL-23 |

**The tally:**
- **Confirmed or confirmed-with-narrowing:** 37.
- **Accepted as corrections to the first reader:** 4 (G-14 and G-19 overturn F-10's wording and F-15; G-15 corrects F-11's counts; G-16 lowers F-12).
- **Left conditional:** 1 (G-42).

**The first reader's findings after the seat:**
- **Raised:** F-04 (High) and F-09 (Medium, latent).
- **Corrected:** F-05's line and F-11's counts (14 tools with no caller, 7 of them broken or refusing).
- **Reworded:** F-10, to *refuse on current source*.
- **Lowered:** F-12.
- **Withdrawn:** F-15.

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

**The no-caller tools, from the record:** fourteen, after the seat's G-15 (the brief's thirteen, plus `pixelelated-cloud-validator-test`, which the two stubs only name).
- **The brief's thirteen are confirmed by invocation, and the fourteenth is added.** Each is named only in `.githooks/pre-push`'s personal-paths list, a docstring or an index row: `build-identity-test`, `nova-led-test`, `pixelelated-content-scope-test`, `pixelelated-duckstation-capture-test`, `pixelelated-save-layout-test`, `pixelelated-state-check-test`, `pixelelated-vm-cloud-boundaries`, `rasteratops-identity-check`, `usb-gadget-test`, `rasteratops-vm-cloud-epic`, `wait-lock-test`, the two stubs and `pixelelated-cloud-validator-test`.
- **In the record, twelve have runs:** every one except the two stubs has a `docs/qa-logs/` folder from when its issue was qualified (column (b)). So they have callers in the record, not in the tree.
- **The cost of having no caller:** seven non-stub tools among the fourteen fail or refuse at the hash and nothing noticed (F-11).

**The fixture file** `tools/test-fixtures/cloud_connections_fixture.py`:
- **Its reader:** only `last-good-scripts-test`. It is copied in at `:5005` and `:11521` and imported at `:5050`, `:5241`, `:5393` and `:11557`, applied only `if hasattr(m, "connections")`.
- **What it fixes:** it redirects the connections module's CONFIG, ACTIVE, LOCK and SYSTEM paths into the fixture, and simulates `config create` by writing the section and `type`. It refuses only the exact combination of real `subprocess` and `RCLONE == '/usr/bin/rclone'` (`:84-85`).

**The ten lint fixture files** (P1's): read by `tools/lint-audit-artifacts`' fixtures, and since T10's `2444828e89` by `tools/test-fixtures/lint-audit-artifacts/run.sh` (on T10's branch). They fix the renovation face's pass and fail cases.

**Proposed dispositions, for the coordinator, who decides with the maintainer:**
- **The two retired stubs:** remove them, with their index rows and personal-path list entries. They refuse every run, nothing calls them, the history is in `git` and the `2026-10-07`/`-08` qa-logs, and one docstring now points at a stale rclone version as current coverage. The alternative is to keep them as refusing markers, with the docstring's version corrected and *retired* added to `fork-workflow.md`'s list entries.
- **The two guest tests:** treat them as the stubs were treated. They refuse every run since #508 retired the migration, and `rasteratops-vm-cloud-epic` says so itself. Retire them in place as markers or remove them; either way the index rows should say *retired*. The authorized guest cycle was not needed to show this (`02` § The guest cycle).
- **The other ten no-caller tools:** the nine the coordinator named (21:03 UTC) plus the validator. They are not retirement. Each proves a property the tree still has. The finding is that nothing runs them, so each could go into a suite that runs (`vm-qa`'s host suites or the fork CI) once its at-hash failure is fixed. Which ones, and where, is the coordinator's.

### Q7 Clarity: the three descriptions

- **The index rows:** all 21 tools have one in `instruction-files.md` at the hash.
- **The *Detail in* rule never names the tool (F-12, the class of T10's 31 pairs), for 13 of them:** `melonds-upgrade-test` (`upgrade-and-install.md`), `nova-led-test`, `pixelelated-cloud-folder-vm-test` and `rasteratops-vm-cloud-epic` (`generic-x64-vm-testing.md`), `pixelelated-cloud-folder-test`, `pixelelated-cloud-validator-test`, `pixelelated-content-scope-test`, `pixelelated-duckstation-capture-test` and `rasteratops-cloud-layout-test` (`rclone-cloud-sync.md`), and `pixelelated-state-check`, `pixelelated-state-check-test`, `rasteratops-candidate-store` and `rasteratops-identity-check` (`release-candidates.md`).
- **The two stubs' index rows** say *refuses execution*, which matches their behaviour (rc 2). Their `fork-workflow.md` list entries are plain, with no note.
- **Promises the code does not keep:** `usb-gadget-test`'s header promises the actual USB preparation functions and runs them under the host's `/bin/sh`. `rasteratops-identity-check`'s `:105` is a check that cannot fail (F-15). `retroarch-wrapper-test`'s docstring reserves exit 1 for *ran twice*, and a missing compiler also exits 1 (F-08).
- **The guest pair's rows** (`instruction-files.md`, *run promoted cloud and settings cases* and *prove explicit layout1 migration...*) describe suites that refuse every run (F-10).
- **Leads for the coordinator, not edits here:** the rule drift and the index rows.

## Quality self-check

- **Every finding has an artifact:** a line read at the hash, a run in `00`, or a constructed input (P4, P5). The research passes' leads were re-derived before use; one of their claims was corrected against `00` and two were withdrawn or demoted.
- **The seat's corrections were taken:** F-04 and F-09 raised; F-05's line; F-10's wording; F-11's counts (14 and 7); F-12 lowered; F-15 withdrawn.
- **Times:** each came from `date -u` or from a tool's own output, except where a heading in `00` was written in the same command as its timestamp.
- **Writes:** no tool, rule, register row or T15 file was edited. Every write was under `docs/audits/`, the work log and its index, the pointer, `.qa-scratch/` or `/workspace/tmp/m6-t14/`.
- **What could still be wrong:**
  - The *Detail in* reading (F-12) counts a rule as naming a tool only by exact name. A rule that governs a tool by its class is not counted (the seat's G-16).
  - The fixture-file rows of the coverage table answer Q6 and Q7 from their readers alone.
