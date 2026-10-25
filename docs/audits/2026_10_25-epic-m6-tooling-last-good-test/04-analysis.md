# Analysis: M6.P2 T15, the last-good scripts test (#662)

Read at `8ebaf8daad`; the branch `HEAD` at stage A, `60d7f6a5b2`, does not differ on the file. The lens is brittleness: what the suite depends on that is not the thing it proves, and what happens when each is absent. The runs are `02` § The runs. The section reads were made by three read-only agents and re-derived here: each lead marked *re-derived* was read from its lines by the lane, and the rest are cited by line for the seat and stage D.

## Executive summary

- **At the hash, the suite passes on the tree:** 1,313 PASS, 0 FAIL, 0 SKIP under the M7 image's BusyBox 1.36.1, given through `QA_SYSTEM_ROOT`. That is the tree's baseline (the coordinator, 00:36). The coordinator's ten FAILs at the hash were its export's missing `.git`.
- **From any M6 worktree without `QA_SYSTEM_ROOT`, it judges the host instead, and says so only in a banner, never in its verdict.** It takes the host's BusyBox 1.37.0 and rclone 1.60.1-DEV. 319 checks FAIL, every one the busybox's (`bbhost` 319, `rchost` 0); `flock`, missing from the host's busybox, is the only refusal named. A host with no busybox at all would run on GNU tools with no banner, which is blindspot 34, silently. **F-01, High.**
- **Its failing controls do not run.** None of the header's twelve `--old` recipes reaches a verdict:
  - two refs are gone;
  - the other ten stop when `src_of` meets a script the ref predates (`s` or `x`);
  - one fires for a reason other than the one it names;
  - the twenty sections from `s` (or `x`) to `ah` have no control that runs (F-04 to F-06).
- **Many of its checks can pass without proving anything.** The common shape is *rc non-zero, and nothing written*, which a script that never ran satisfies (F-10). With it come a `;`-chained `check` (F-11), skips and silent omissions behind a missing download (F-09), sleep-ordered races (G-04, G-08) and a driver whose crash drops checks unseen (G-06).
- **The seat** (one GPT-6 Astra call, plus a second for the sections it asked for) confirmed 20 of the 21 findings, 13 of them narrowed. It refuted F-08, now withdrawn: `NOT APPLICABLE` is a retirement outside the count, and its gate's fragility is G-05. It added G-01 to G-10, all re-derived and accepted. The three `--old` items are bugs of this file (the coordinator, 02:24 UTC).
- **Its two calls into T14's writer tests are now refused** (F-07, #997's two flags, stream S1).

## Acceptance-criteria scorecard

#662's 19 criteria at the end of stage B. The final state is the hand-back's.

| # | Criterion (short) | State | Artifact |
| --- | --- | --- | --- |
| 1 | the folder holds 00 to 05 | 00 to 04 written; 05 at stage D | this folder |
| 2 | the lint prints PASS | pre-issue at stage C | `tools/lint-audit-artifacts` |
| 3 | the review plan, the seat's provenance and the packet's scan | stage C | `second-opinions/` |
| 4 | the punch-list issue at its outcomes | stage D onward | the audit issue |
| 5 | `reviewed-at` / `fixed-at` | `reviewed-at: 60d7f6a5b2` | #662's body at hand-back |
| 6 | `01` § Scope | done | `01` |
| 7 | 34 coverage rows | done (34) | `02` § Coverage |
| 8 | both runs; the busybox-dependent checks with their applet | done: 319, with `flock` named where shown | `02` |
| 9 | the twelve `--old` recipes | done: all exit 2, each stop named | `02` § The runs |
| 10 | no forbidden action; `SIGINT ignored=0` on every run | holds; one write under `/tmp` made and removed (`00`) | `00` |
| 11 | Q6's 34-row table and the split proposal | done below | § Q6 |
| 12 | Q3 by section; the eight `\|\| true`; `check $?`; `skip()`; NOT APPLICABLE; no-busybox; the ten | done below | § Q3 |
| 13 | Q7 | done below | § Q7 |
| 14 | Q5 by section | done below | § Q5 |
| 15 | `proved:` cells | P1 to P5 in `02` | `02` § Proofs |
| 16 | `question:`; `box-check`; no `tools/` change before a stream; the call sites' flags | no `tools/` change; the rest at D and E | the branch |
| 17 | the fixed tip refuses or marks a host-busybox run | stage E | — |
| 18 | the retro | stage G | — |
| 19 | the checkers; `vm-qa:148`'s rule stated | `vm-qa:148` stated in `01` and § Q2; the checkers at hand-back | `01` |

## Risk assessment

- **The suite's verdict is only as good as its busybox source, and that source is chosen silently.** A worktree with no build root is every M6 worktree today. There, `vm-qa`'s `scripts` row reads `FAIL (1)` over 319 FAILs about the host. Worse, a host whose own busybox happened to carry `flock` would pass the host's applets as the image's, under a `PASSED` verdict. Blindspot 34 is exactly a check passed under the wrong tools.
- **The failing controls are the suite's evidence that its guards fire, and they have decayed.** Sections `x` to `ah` (933 of 1,313 checks, including the three audits' streams) have no runnable positive at all.
- **Absence is often indistinguishable from success** where a check asserts *nothing was written*. A sandbox that cannot start, a script that is not lifted, or a fixture that never ran each passes such checks. The paired positive usually fails beside it, but not always (F-10's list).
- **What this does not risk:** no device, no cloud and no player data. The suite runs on the host against fixtures, and its sandboxes bind the fixture's directories only, but they **share the host's network and the caller's environment** (F-16).

## Coverage boundary

- **Read:** the one path at `8ebaf8daad` (14,238 lines): the harness `:1-430` whole; sections `a`, `b`, the sandbox helpers and the `F1.` history helpers by the lane; every section by the three agents; their leads re-derived where marked.
- **Run:**
  - the suite fourteen times at stage A (the image's busybox, the host's, and the twelve `--old` recipes);
  - three more (`bbhost`, `rchost`, and the timed run);
  - `--help` and `--nosuch`.
- **Not run:** the positive refs the later groups name in comments (`417dcd8610`, `f3d19dc8fb`, `320d2b2bea`, `286759eb6d`, `a06539d8ec`). Each would stop where `src_of` meets a script it predates. Not run either: `--payload-tests`-style host gaps such as a host without `jq` or `node`, read from the code only.
- **Not touched:** the scripts it proves, T14's four tools (read at `7c1d729b57` for the call sites) and `tools/vm-qa`.

## Findings (Phase 4)

| ID | Finding | Where | Severity | Q |
| --- | --- | --- | --- | --- |
| F-01 | `image_tool_source` falls back to the host's busybox (`command -v busybox \|\| true`), named only by the banner at `:426` and never by the verdict, and to none at all: no copy, no wrappers, no banner, GNU tools. The verdict never says whose applets judged the scripts (narrowed from *silently* by the seat). From every M6 worktree it takes the host's 1.37.0, and 319 checks FAIL (`flock`). #1015's root cause | `:381-401`, `:400`, `:416-426` | High | Q2 |
| F-02 | The rclone stream A runs is chosen the same way (`:8908`): the host's 1.60.1-DEV silently. Its version is printed (`:8914`) and never asserted, and no case depends on it (`rchost`: 1,313 / 0 with 1.60.1) | `:8906-8914` | Medium | Q4 |
| F-03 | The history read fails open. `f1_tree_at`'s `git ls-tree ... 2>/dev/null \| while ...` with its `exit 2` inside the pipeline subshell, and `:4271`'s `git show 417dcd8610:... 2>/dev/null`, make an empty fixture without a word, caught only by a downstream vacuity detector (the coordinator's ten). Ruled a bug, 00:36 | `:3205-3215`, `:4271` | Medium | Q2 |
| F-04 | Two `--old` refs are dead: `0f7785e6ed` (q) and `d79281066c` (p's pending and flushed) exist nowhere in the repository. Likely meant: `717bc04449` (`1a5c066623^`) and `51e2acece6` (`67a89cb623^`) | `:185`, `:191` | Medium | Q3 |
| F-05 | Under `--old`, `src_of` exits 2 for the whole run at the first script a ref predates. No recipe reaches a verdict, and sections `s` (or `x`) to `ah` never run as controls | `:320-325` | Medium | Q3 |
| F-06 | `70b6c70ca7`'s control fires on patch application, not on its `012` checks. Section `t` takes the client pin from the working tree (`:2051`) and the patches from `BASE_REF`, which no longer apply | `:2051-2086`, `:219-225` | Medium | Q3 |
| F-07 | `ag` and `ah` call T14's writer tests with `--busybox "${BB_HOST}"`, the run's copy, which T14's S8 contract refuses (CANNOT, exit 2) without `--busybox-from` or `--unverified-busybox`. They FAIL on every host until S1 | `:14224`, `:14231` | High | Q3 |
| F-08 | **Withdrawn (the seat's refutation, accepted):** a fourth verdict word, `NOT APPLICABLE` (the retired migration group, #508), is reported, and the run then exits 0 `PASSED`: a group that did not run passes, and `vm-qa:148` reads it as PASS | `:4558`, `:14235-14238` | Medium | Q3 |
| F-09 | **Missing downloads hide or drop checks, by three rules.** (1) One SKIP stands in for every webkit patch (`:6491`), where F2-4 (`:4008`) and F2-6 (`:4297`) count the same absence as a FAIL. (2) Section `D`'s 21 SKIPs and seven `if DT_OK` blocks with no `else` (A's D22-D31) depend on `t`'s client tarball, so on a host without the cache `D`'s 33 `flock` FAILs would read as SKIPs (exit 3). (3) `F1r-d` (no `qemu-img`) and the G-B-15 banner probes (no busybox) vanish with no SKIP | `:6491`, `:6649`, `:10128-10358`, `:11180`, `:8777-8811` | Medium | Q3 |
| F-10 | *rc non-zero, and nothing written* passes when the script never ran: a sandbox that cannot start (rc 1 from `bwrap`, or 127 hidden by `2>/dev/null`), a missing applet path, or an unlifted function. 30-odd sites (§ Q3) | § Q3 | Medium | Q3 |
| F-11 | `v`'s START NEW GAME check chains three runs with `;` and `&&`, so `check $?` reads only the last `is`, against output an earlier failure may have left | `:3051` | Medium | Q3 |
| F-12 | `check` called with two arguments: a FAIL aborts the run under `set -u` with no FAIL counted (historical refs only) | `:13826` | Low | Q2 |
| F-13 | `q`'s *the boot pass ran (rc 0)* reads `wait`'s status, and its *still there* checks test markers the fixture made | `:1803-1846` | Low | Q3 |
| F-14 | `t`'s PASS text says *each compiled*, while `py_compile`'s failure only changes that text | `:2086` | Low | Q7 |
| F-15 | `! tar ... \| grep -q` with no `pipefail` passes on a missing archive or member; each has a paired existence check | `:548`, `:803`, `:1036-1047` | Low | Q2 |
| F-16 | `sa_run`'s sandbox has no `--clearenv` and no `--unshare-net`: the caller's environment (`RCLONE_*`, `BASH_ENV`) and the host network reach every script it runs (150 calls). Four other invocations do unshare the network | `:9010-9022` | Medium | Q2 |
| F-17 | Some checks ignore `--old` and grade the working tree among the expected FAILs: `g` `:845-851` (re-derived), `h`'s fallback `:887-891`, `i` `:903-928`, `t` `:2427`, `C7` `:6506` | as named | Low | Q3 |
| F-18 | **The descriptions drift from the code.** `--help`: *"with the image's busybox"*. The header's claims stop at `w`, and its recipes at `v`. `:264` and `:266` advise `setsid -f`, which keeps an ignored SIGINT. The index row's Detail-in rule never describes the file | `:239-250`, `:7-226`, `:264-266` | Low | Q7 |
| F-19 | S3F's canaries write to the host's `/tmp/s3f-*` if the guard fails, and a stale one from another run FAILs the check | `:13672-13678` | Low | Q2 |
| F-20 | `y4`'s G-B-15 banner probes accept any `BusyBox` banner, so the host's 1.37.0 passes as *the image's*; and they are silently absent with no busybox | `:8777-8779`, `:8809-8811` | Medium | Q3 |
| F-21 | `z`'s PL-022 measures *the image's busybox unzip* with whatever busybox ran; its skip tests only `-n BB` | `:13400-13424` | Low | Q3 |
| G-01 | (the seat) Section `b` runs `backuptool` whole with PATH `/shim:/usr/bin:/bin` and binds no busybox or wrappers: its kill and restore tests are host-tools tests even after F-01 is fixed | `:522`, `:536-541`, `:566`, `:586-590` | Medium | Q2 |
| G-02 | (the seat) `ag` runs `${ROOT}/tools/settings-modes-test` (the subject checkout's), and `ah` `${HARNESS_ROOT}`'s: `LAST_GOOD_SOURCE_ROOT` replaces a verifier, against `--help`'s promise | `:14224`, `:14231`, `:248-249` | Medium | Q3 |
| G-03 | (the seat) `q` enumerates the working tree's fragments, so one present only at `BASE_REF` never runs | `:1781-1789` | Low | Q3 |
| G-04 | (the seat) The corekeeper contention test orders its two handlers by `sleep`, not a barrier | `:8852-8860` | Medium | Q3 |
| G-05 | (the seat) The retirement gate recognizes one spelling (`cp cloud_migrate_layout`), and any other install line reads as retired | `:4553-4559` | Low | Q2 |
| G-06 | (the seat) D13b and D13c replay the Python driver's verdict lines and ignore its exit, so a crash after one PASS drops the rest unseen | `:7320-7357`, `:7370-7432` | Medium | Q3 |
| G-07 | (the seat) S3F's absent-function paths: empty `conf_valid` extracts compare equal; an absent `sort_settings` is 127 with its status dropped; `rc=1` matches `rc=127` | `:13668-13715` | Low | Q3 |
| G-08 | (the seat) D29's poll for the helper's start is never asserted, so the concurrent-marker scenario need not occur | `:10326-10333` | Medium | Q3 |
| G-09 | (the seat) D21 rejects only `100644` and `none`, not every mode but `100755` | `:7771-7776` | Low | Q3 |
| G-10 | (the seat) A child's CANNOT (2) or unverified (3) from the writer tests is flattened to FAIL by `check $?`, so S1's flags alone are not enough | `:14224-14233`, `:310` | Medium | Q3 |

## Finding Verification (Phase 4.5)

Each Medium or above, by the artifact that decided it:

- **F-01:** run 2 and `bbhost` (319 FAIL, `diff` 0 against each other), `rchost` (0), and `:400` read. *Re-derived.*
- **F-02:** `rchost`'s 1,313 / 0 with `rclone v1.60.1-DEV` (its own `rclone:` banner line), and `:8914` read. *Re-derived.*
- **F-03:** the coordinator's export run (no `.git`; its `run-image.out` lines 428-431, 524-525 and 1150-1156) against this worktree's run (all ten pass), and `:3205-3215` and `:4271` read. *Re-derived.*
- **F-04:** `git cat-file -t` on both refs (*Not a valid object name*), `git branch -a --contains` empty, and `git log -S` naming the commits that wrote them. *Re-derived.*
- **F-05:** the twelve `--old` outputs, each ending `cannot read <script> at <ref>`, rc 2. *Re-derived.*
- **F-06:** `old-70b6c70ca7.out`'s `t`: 0 lines naming `012` against 5 PASS in the baseline, and four FAILs *patch does not apply to the pinned client*. *Re-derived.* The working-tree pin at `:2051` is the agent's reading, not re-derived (inference).
- **F-07:** T14's `settings-modes-test` at `7c1d729b57` refuses a path not under a build root's `image/system/`, and `:14224` and `:14231` pass `${BB_HOST}` (`${TMP}/busybox`). T14's own run on 2026-10-24 showed both refused. *Re-derived.*
- **F-08:** run 1's `1 HISTORICAL FEATURE GROUP(S) NOT APPLICABLE -- no checks counted as PASS` then `PASSED`, rc 0. *Re-derived.*
- **F-09:** `:6488-6492` read (re-derived); `:6649` and D's skips from the agent's table; `:4008` and `:4297` from the agent.
- **F-10:** the shape read at `:548` and `:8583` (re-derived); the other sites cited by line from the agents, for the seat.
- **F-11:** `:3051` read. *Re-derived.*
- **F-16:** `:9010-9022` read. *Re-derived.*
- **F-20:** from the agent's reading of `:8777-8811` (not re-derived; cited for the seat).

## Second opinion (Phase 4.6)

**One GPT-6 Astra seat at `max`** through the Facilitator (`second-opinions/review-plan.json`).
- **The probe:** PASS.
- **The refutation:** two calls, the second carrying the sections the first asked for under `## Sections I need`, as the brief allows.
  - `gpt-audit.md`: 02:02:52 to 02:15:31Z, 33,590 reasoning tokens.
  - `gpt-audit2.md`: 02:16:37 to 02:24:14Z, 21,576 reasoning tokens.
- **Each served `openai/gpt-6-astra` by OpenAI,** with verification, effort and provider PASS in its `.provenance.json`.
- **Each packet** was scanned before it was sent, and each reply before it was read: 0 listed words, and 0 credential lines under three pattern sets.

**The grading.** "Accepted" means the lane re-read the seat's lines and agrees; the artifact that decided each is named.

| Item | The seat | The lane's grade, and the artifact |
| --- | --- | --- |
| Q1 (the fallback) | F-01 real; *silently* is inaccurate when a busybox is found (the banner `:426` names it); recommends exit 2 by default, a host-diagnostic mode exiting 3 that ends **NOT DEVICE EVIDENCE**, and provenance in the verdict | **accepted**: `:426` read. F-01 is narrowed to *unqualified*: the banner names the host's busybox, and the verdict never does. The exit-2 default goes to S1's brief as a lead |
| Q2 (network and environment) | F-16 right; launcher sanitization too | **accepted**: `:9010-9022` read |
| Q3 (`check $?`) | F-11 and F-15 right; `pipefail` alone does not repair a negated pipeline; `:547` weaker than claimed; adds `:8784` and `:599`; `:3053` and `:3329` corrections | **accepted**: `:3053`, `:3061-3062` and `:3326-3329` re-read, and both corrections are right (§ Q3 amended). `:8784` and `:599` are carried into F-15's list |
| Q4 (`--old`) | broken recipes, not worthless controls (FAILs before the stop still count); against a blanket per-section NOT APPLICABLE: invalid ref → CANNOT; absent historical feature → a presence-contract FAIL; an unrelated newer section → not applicable; a selected check that cannot run → incomplete, never PASS | **accepted as to the facts**: the twelve outputs show FAILs before each stop. **The fix's shape is the coordinator's** (02:24 UTC: NOT APPLICABLE per section, the run goes on). The seat's four-way distinction is carried into that bug's acceptance as a lead |
| Q5 (the split) | agrees with a split by subject; the 2,166 lines are stream A's, not the cloud file's; `ae` is not wholly retired | **accepted**: § Q6's proposal amended |
| F-01 | confirmed with narrowing (not literally silent) | accepted; reworded |
| F-02 | confirmed with narrowing (compatible behaviour across versions is not itself a defect) | accepted: the finding is the unqualified selection and the unasserted version, not the absence of a version-sensitive case |
| F-03 | confirmed | accepted |
| F-04 | confirmed with narrowing (refs unresolved in this checkout; replacements not established) | accepted: the replacements are proven by running at stage E (the coordinator, 02:24) |
| F-05 | confirmed with narrowing (the refusal is intentional; automatic N/A is not a general fix) | accepted; the fix shape is the coordinator's ruling |
| F-06 | confirmed | accepted |
| F-07 | confirmed with narrowing: against T14's `7c1d729b57` contract (the `8ebaf8daad` callees only copy the binary) | accepted: both revisions were read in packet 2 |
| F-08 | refuted as a hidden PASS: N/A is excluded from the count (`:14235`), and the gate reads the selected source's recipe (`:4553-4556`); narrowed to G-05 | **accepted**. F-08 is withdrawn as written: the run's exit 0 after a group that is out of scope by retirement is design. What remains is G-05's fragile gate |
| F-09 | confirmed with narrowing: a dependency SKIP is not a PASS (`t`'s SKIP prevents exit 0); one of `D`'s skips depends on `p` (`:7227`) | accepted |
| F-10 | confirmed with narrowing (individual assertions, not whole-suite success; `:3053` wrong) | accepted |
| F-11 | confirmed | accepted |
| F-12 | confirmed | accepted |
| F-13 | confirmed with narrowing (`:1846-1854`'s positive log checks reject a wholesale no-op) | accepted; Low stands |
| F-14 | confirmed | accepted |
| F-15 | confirmed with narrowing (`:547` checks another member); adds `:8784` | accepted |
| F-16 | confirmed with narrowing (PATH and HOME overridden, TMPDIR removed, no external access shown) | accepted |
| F-17 | confirmed; adds `:3999`, `:4291`, `:10344` and `:6481-6485` | accepted |
| F-18 | confirmed with narrowing: a foreground `setsid -f` from a clean parent avoids the inheritance; it cannot reset an ignored SIGINT | accepted: the advice is incomplete, not wrong |
| F-19 | confirmed with narrowing: construction runs nothing; a regression that evaluated them writes the host's `/tmp`; stale files are not reset | accepted (`:13668-13678` read) |
| F-20 | confirmed with narrowing: the host's 1.37.0 does not pass these probes (no `flock`); provenance is F-01's | accepted; folded under F-01, Low |
| F-21 | confirmed | accepted |
| G-01 | Medium: section `b` never runs the busybox (PATH `/shim:/usr/bin:/bin`, no wrappers) | **accepted**: `:522`, `:536-541` read |
| G-02 | Medium: `ag` runs `${ROOT}`'s `settings-modes-test`, `ah` `${HARNESS_ROOT}`'s | **accepted**: `:14224`, `:14231` read |
| G-03 | Low: `q` enumerates the working tree's fragments | **accepted**: `:1781-1789` read |
| G-04 | Medium: the corekeeper contention orders by `sleep` | **accepted**: `:8852-8860` read |
| G-05 | Low: the retirement gate matches one spelling | **accepted**: `:4553-4559` read |
| G-06 | Medium: D13b and D13c replay verdict lines and ignore the driver's status | **accepted**: `:7320-7357` read |
| G-07 | Low: S3F's absent-function PASS paths | accepted (`:13668-13715`, from packet 2) |
| G-08 | Medium: D29's poll is not asserted | **accepted**: `:10326-10333` read |
| G-09 | Low: D21 rejects only `100644` and `none` | **accepted**: `:7771-7776` read |
| G-10 | Medium: a child's CANNOT (2) or unverified (3) is flattened to FAIL by `check $?` | **accepted**: `:14224-14233` and `:310` read; S1 must keep the distinction |

**Agreement:** of the first reader's 21 findings, the seat confirmed 20 (7 outright and 13 with narrowing) and refuted 1 (F-08, withdrawn). It added 10, all accepted. The two Q3 errors it found are corrected.

## Renovation face

### Q1 Modernize

- **The busybox roots it searches** (`:392-394`) name three distro layouts under `${ROOT}/..`, `${ROOT}.worktrees` and `${ROOT}`. None reaches `/workspace/repos/rocknix.worktrees/`, where the M7 roots are. `rocknix.worktrees` and `/workspace/repos/rocknix` appear 0 times in the file.
- **`$HOME`** appears twice, both as string fixtures (`:4673`, `:11376`), never read.
- **Absolute host binaries:** `/usr/bin/grep` 4, `busybox` 4, `tar` 3, `mv` 3, `sleep` 2, `rm` 2, `python3` 2, `env` 2, `date` 2, `sed`, `rsync`, `find` 1 each. Only `bwrap` and `setsid` are checked up front (`:286-287`), and `rsync`, `python3`, `jq`, `node`, `gcc` and `qemu-img` are found by failure.
- **The `BASE_REF` default `1d1503180d` and the twelve recipes** predate every section from `s` on (F-04, F-05).
- **`flock` is not in the top-level wrapper list** (`:422`: `sed mv cp tr head wc cut awk stat chmod cat`). It is shimmed in `n` (`:1484`), `t` (`:2097`), `y1` (`:7811`) and stream A (`:8983`), and called on the host directly at `:2345` and `:6765`, where it is util-linux's.

### Q2 Standards

- **`set -u` only** (`:270`): no `-e`, no `pipefail`. The pipeline-first-stage failures that matter are F-03 (`ls-tree ... 2>/dev/null \| while`) and F-15 (`tar ... \| grep -q`).
- **The eight `|| true` sites:**
  - `:400`: the fallback, F-01, a finding.
  - `:1102`: a comment (#151 PL-14's history).
  - `:2086`: `py_compile ... || true` feeds only the PASS text, F-14.
  - `:4376`: a comment.
  - `:9633`: inside a FAIL message's text.
  - `:10409`: sound. `grep -c` prints 0, an error leaves `DLEFT` empty, `-eq` then errors, and the check FAILs.
  - `:13871` and `:13908`: sound against a missing file (`src_of` guarantees it); a call through a variable verb evades the regex (inference).
- **`check $?` after a compound test:** `[ ] && [ ] && grep` returns the first failing status, which is sound throughout. The exception is the `;`-joined chain at `:3051` (F-11).
- **The SIGINT refusal** (`:265-268`) fails closed, exit 2. Its advice (`setsid -f`) is wrong (F-18). `vm-qa:158`'s launcher is the right way in.
- **Exit codes:** 0 PASS (including after `NOT APPLICABLE`, F-08), 1 FAIL, 2 cannot run, 3 SKIP. `vm-qa:148` reads 3 as SKIP and any other non-zero as FAIL.
- **The sandboxes** share the host's network and the caller's environment (F-16).

### Q3 Bugs: the pass-without-proving hunt, section by section

Each line read, with a constructed input that would pass wrongly, or the statement that none was found:

- **`a`:** with no busybox, `bbin` is empty and the text checks run on GNU `tr`, blindspot 34's exact case (F-01). Constructed: a host with no busybox and a `chksysconfig` whose text test only GNU `tr` passes. The `[ ] && [ ]` chains are sound.
- **`b`:** `:548` `! tar -xzOf "${first}" ... 2>/dev/null | grep -q SECRET` passes on a missing archive; `:547` catches it (F-15). `:573` and `:594` pass when the run never started (F-10).
- **`c`:** `:621` counts exact spellings, so a `set_setting` that appends with `printf >>` passes. `:644` passes if `sort_settings` is not lifted; `:647` catches it.
- **`d`:** `:681`, `:687` and `:688` confirm files the fixture wrote, with the helper's rc unchecked: a helper that never runs passes. `:719` passes if `record_last_run` is missing; `:720` catches it.
- **`e`:** `:747-751` scans only `echo`, `log_message`, `fail`, `note` and `why` lines with a leading literal, so a `printf 'exit code 3\n'` passes.
- **`f`:** `:803` (F-15). `:800`: the #537 check runs only if a grep of `backuptool` matches, and is otherwise dropped with no SKIP.
- **`g`:** grades the working tree under `--old` (F-17). None found at default.
- **`h`:** `:887-891` ignore `--old` (F-17). None found at default.
- **`i`:** ignores `--old` (F-17). None found at default.
- **`j`:** `:947` and `:959`: the helper's rc is unchecked (as `d`).
- **`k`:** `:1036-1047` (F-15). The skip-less `LL_SCOPED` branches belong to `l` (`:1171`, `:1195`, `:1215`).
- **`l`:** checks are dropped by scope with no SKIP (`:1171`, `:1195`, `:1215`).
- **`m`:** `:1385` matches `hostnamectl` only at a line's start, and the shim at `:1273` exits 0, so `x && hostnamectl` passes.
- **`n`:** `:1510` and `:1523` pass when the run never started; `:1507`'s rc check also passes when `bwrap` or `timeout` itself fails (F-10).
- **`o`:** none found (it reuses `a`'s, `c`'s and `m`'s fixtures).
- **`p`:** `:1692` and `:1745`: a failed `pdb` (no `python3`) leaves no store, which reads as empty, and both PASS.
- **`q`:** `:1842` reads `wait`'s rc, and `:1843`/`:1845` test markers the fixture made at `:1840` (F-13, re-derived).
- **`r`:** `:1895`, `:1908` and `:1938` are absence checks that pass when the log was never written; their positive partners fail.
- **`s`:** `:2025` and `:2030`, the same shape as `r`.
- **`t`:**
  - `:2086` (F-14);
  - `:2847-2853` grade only the verdict lines printed, so a block that throws (`:2658`, `:2681`, `:2734`) suppresses later verdicts unseen;
  - `:2090`'s `unittest discover` on a missing file exits 0 on Python before 3.12 (inference);
  - `:2059` is the section's one skip (the client tarball).
- **`u`:** none found.
- **`v`:** `:3051` (F-11, re-derived). `:3061-3062`: `sa`'s status is dropped by the `;`, so a `set_autosave` that errors prints nothing and *no -e* PASSes. (The first reader also cited `:3053`; the seat showed every `sa` there is in the `&&` chain, and the lane re-read it: `:3053` is sound.)
- **`w`:** `:3096`: *no Token of its own* is never grepped; `:3095` checks only the second run's rc.
- **`x`:**
  - before `F1.`, none found;
  - `F1.`: `:3303-3307` pass on an empty journal if the quirk directory is missing; `:3329` was cited as passing on an empty `F1_WROTE`: **wrong** (the seat, re-derived at `:3326-3329`: the here-string makes one empty line, so `F1_LEFT` is non-empty and the check FAILs, and `:3326` catches the empty set first); `:3381`→`:3394` takes the `else check 0` branch when `git cat-file` fails;
  - `:3441`, `:3478`, `:3540` and `:3565` pass when the launcher dies at start; `:3535`'s `qemu-img create` is unchecked; `F1g` and `F1h`'s *left alone* checks pass if the quirk never runs;
  - `:3866` checks rc only; `:4121` passes on an empty result when `python3` is absent;
  - `:4283` is re-derived: a no-op repair leaves both copies equal;
  - `:4433-4434`'s `-le 1` accepts zero;
  - `C.`: about twenty negatives (`:4616`, `:4675`, `:4703` to `:4884`) pass when `cloud_setup` never runs, because the sandbox's 127 is hidden by `2>/dev/null` (`:4610`); `:5627-5631` reports `result(True)` with no `node`; `:6120`'s and `:6431`'s `END n` sentinels never compare n; `:6483` takes any line as a description; `:6491` (F-09);
  - `D.`: `:6765` (re-derived): `kill -0 1` fails as a non-root user, and `flock -n` creates a missing lock, so both halves PASS when the helper never started; `:7302`, `:7351` and `:7426` pass on one verdict line; the `DT_OK` omissions (F-09).
- **`y`:**
  - `y1` to `y4`, A, A-fix and z: the *rc non-zero, nothing written* list (F-10): `:7912`, `:7934`, `:8246`, `:8258`, `:8271`, `:8352`, `:8583` (`RC -eq 1`, which is `bwrap`'s own failure code; re-derived), `:8787`, `:9172`, `:9744`, `:9951`, `:9957`, `:10085`, `:10580`, `:10727`, `:11050`, `:13270`, `:13508`;
  - negatives over possibly-absent output: `:8065`, `:8215`, `:9407`, `:10883`, `:10965`, `:13333`, `:13555`;
  - empty producers: `:8672`, `:8828`, `:10245`, `:10346`, `:13122`, `:13539`;
  - `y4`'s banner probes (F-20);
  - stream A's argv checks (`:9159`, `:9466`, `:9477`, `:9905`, `:9909`, `:10667`) assert what the script asked for, not what rclone did (F-02);
  - `CF`: `:11902` accepts `END 0`, and `:12061` counts groups above 0 only.
- **`z`:**
  - `:13423` (F-21);
  - `:13672`: `cmp` of three empty extracts;
  - `:13690`: `sort_settings` absent;
  - `:13710`: `grep -q 'rc=1'` matches `rc=127`;
  - S315's `! sz_fn` checks (`:13652-13660`) pass when the function is absent (exit 127);
  - S3F (F-19).
- **`aa`:** does not run at the hash (`MIGRATION_AVAILABLE=0`) except the D-CLOUD-170 loop (`:13904-13910`). `:13826` (F-12).
- **`ab`:** `:14003` to `:14112`: `! sc_valid` passes if `--stamp-valid` cannot run.
- **`ac`:** none found.
- **`ad`:** none found. One FAIL at `:8910` without any rclone.
- **`ae`:** `--archives-only` only (`:14183`), with no SKIP for the matrix. The `NOT APPLICABLE` line at `:14186` is F-08's.
- **`af`:** none found; it FAILs on the host's busybox (`flock`).
- **`ag`, `ah`:** F-07.

**The `skip()` paths:** 30 calls. One SKIP never hides a FAIL by itself, but three rules let absence change the count (F-09).
- **The calls:** 22 in `x` (`:6491`, and 21 behind `DT_OK`); `t` `:2059`; `y`'s `:10174`, `:10350`, `:12158`, `:12221`, `:12265` and `:12312`; `z` `:13423`.
- **Where a FAIL is hidden:**
  - one SKIP stands for N patch checks at `:6491`;
  - D's `flock` FAILs become SKIPs on a host without the sources cache;
  - `:13423` runs with any busybox.

**`NOT APPLICABLE`:** printed at `:4558`, `:9486`, `:10461`, `:10670`, `:13899` and `:14186`; counted once at `:4558`; the run exits 0 (F-08).

**The no-busybox case:** `BB_SRC` empty (`:402`) → no copy (`:416`), no wrappers (`:421`), no banner (`:426`). Every wrapper list then falls to GNU tools, and sections `b`, `d`, `f`, `h`, `i`, `j`, `l`, `w`, `aa`, `ab` and `ac` use host tools even with a busybox (no wrapper at all). It was not run (this host has a busybox); it is read from the code. **The ten:** the fixture's (F-03), sorted at stage A.

### Q4 Currency

- **No package.** The rclone stream A binds (`/sa/rclone.real`) is whatever `image_tool_source` finds (F-02): v1.75.2 from the M7 root, 1.60.1-DEV from the host. The recipe pins 1.75.2, and no case would notice the difference.
- **The busybox:** 1.36.1 is the image's (the M7 roots), and 1.37.0 the host's.

### Q5 Efficiency

The timed image run, 515 s:

| Section | Seconds | Share |
| --- | ---: | ---: |
| `y` | 248.3 | 48 % |
| `x` | 82.1 | 16 % |
| `n` | 41.6 | 8 % |
| `af` | 33.7 | 7 % |
| `t` | 33.6 | 7 % |
| `ae` | 19.8 | 4 % |
| `z` | 17.4 | 3 % |
| `i` | 14.3 | 3 % |
| `h` | 6.3 | 1 % |
| the other 25 | 17.9 | 3 % |

- **By group:** `y/A` 137.2, `y/CF` 65.9, `y1`-`y4` 36.4, `x/C` 45.3, `x/D` 31.7, `z/S315` 9.1, `y/F1r` 8.8, `x/F1` 4.9, `z/S3F` 0.3.
- **What carries the time:** stream A's 143 `sa_run` calls (`y` makes 145) and CF's shimmed runs. `n`'s, `af`'s and `t`'s waits are mostly real timeouts by design: stall ceilings and inactivity windows.
- **`vm-qa`'s 13 minutes** (T12's Q5 table) is this suite's 8.6 minutes plus `vm-qa`'s own setup, not measured here.
- **The wrong busybox costs** 677 s, 162 s more, to a verdict that judged the host.
- **The sandboxed sections could run beside the guest suites** (T12's #987 lead): they share nothing with a guest but the host's CPU (inference).

### Q6 Dead ends and brittleness: the table

(a) What each section depends on that is not the thing it proves, and what its absence does. (b) Its last recorded catch. (c) Its caller. (d) Its positive. The caller is `vm-qa`'s `scripts` suite (`vm-qa:158`) for every section, plus `--cloud-layout` (`:252`) for `ae`'s tool. "BB" is the busybox copy, and "no wrapper" means the section never uses it.

| Section | (a) dependencies, and what each one's absence does | (b) last recorded catch | (c) caller | (d) positive |
| --- | --- | --- | --- | --- |
| `a` | BB (`:459`): absent → GNU tools, a silent pass of blindspot 34's case. `/usr/bin/rsync` (`:453`): absent → FAIL. Host `tar` (`:501`) | blindspot 34, busybox `tr` (2026-09-10, `:158-160`); KILL18 (`:497`) | `vm-qa` | `1d1503180d` and `c15050c897`: FAIL as promised |
| `b` | `bwrap`, `setsid`; host `/usr/bin/tar` (`:566`, `:586`); no wrapper | D-CLOUD-078, #105 | `vm-qa` | `1d1503180d` (FAIL 7); dying-`tar` shims (`:556`, `:583`) |
| `c` | BB (`:614`): absent → GNU, silent | `sed -i '$a'` lost a last-line key (`:618-620`); #106 | `vm-qa` | `1d1503180d` (FAIL 4) |
| `d` | `bwrap`; host `/usr`; no wrapper | nothing recorded | `vm-qa` | `1d1503180d` (FAIL 9); a killing `mv` (`:714`) |
| `e` | `python3` (`:735`): absent → FAIL | the FORBIDDEN regex (`:724`) | `vm-qa` | `1d1503180d` (FAIL 1) |
| `f` | `bwrap`; host `tar`; no wrapper | #52, #64, #274, #307 PL-005, #221, #537 | `vm-qa` | `1d1503180d` (FAIL 5); a planted `leaky.conf` (`:810`) |
| `g` | the working tree's files only | 2026-09-12 F-03, #146 | `vm-qa` | none: `--old` has no effect (F-17) |
| `h` | host `sleep`, `timeout`, `date`; no wrapper | #153 | `vm-qa` | `8707919349` (FAIL 3) |
| `i` | the working tree's `cloud_net_ready`; host shell | RG SP 2026-09-12; #192 | `vm-qa` | none: ignores `--old` (F-17) |
| `j` | `d`'s sandbox | #107, #282 | `vm-qa` | `1d1503180d` (FAIL 4) |
| `k` | `bwrap`; BB `tar`/`unzip` (`:1015`): absent → GNU tar and Info-ZIP, silent; `python3` (`:1087`) | #45, #169, #165; #151 PL-03, PL-10, PL-14 | `vm-qa` | `1d1503180d` (19), `53f390b1e9` (17), `34aca64afd` (8); a grep shim (`:1103`) |
| `l` | host `timeout` (`:1164`); `bwrap`; no wrapper | #142; #151 PL-14; #273's trace of #113 | `vm-qa` | `1d1503180d` (14), `53f390b1e9` (14) |
| `m` | `bwrap`; host `md5sum`; a build root's avahi unit (`:1393-1399`), else the source unit, said | #50; #151 PL-01/02/04/14 | `vm-qa` | `1d1503180d` (17), `53f390b1e9` (17) |
| `n` | `bwrap`, `setsid`, `timeout`; BB with `flock` (`:1484`): the host's lacks it → 7 FAIL | #153; LINK5 on MinIO (`4d7eb1f303`) | `vm-qa` | `8707919349` (FAIL 7) |
| `o` | the fixtures of `a`, `c` and `m` | #154, guest b | `vm-qa` | `8707919349` (FAIL 5) |
| `p` | `bwrap`; host `python3` for `pdb` (`:1670`), rc unchecked (§ Q3) | #165, #173, #180, #186 PL-16/26/32 | `vm-qa` | `34aca64afd` (1: no ctl); `d79281066c` **dead**; `cee1656c33` (5) |
| `q` | `bwrap`; the fragment list from the working tree (`:1789`) | #166; `smb.conf` at every ref (`:1762`) | `vm-qa` | `0f7785e6ed` **dead**; FAILs at the older refs (2 each) |
| `r` | BB `sed` (`:1893`) | #176; #186 PL-29 | `vm-qa` | `28a80357ed` (6), `cee1656c33` (2) |
| `s` | `bwrap`; `r`'s helper (`:1964`) | #176 | `vm-qa` | `28a80357ed` (7); an emptied helper (`:2023`) |
| `t` | the sources cache's client tarball (`:2053`): absent → SKIP, and every `D.` group behind `DT_OK` goes with it; `patch`; host `python3`; BB `flock` (`:2097`): the host's lacks it → 42 FAIL | #186's PLs, #188, #189, #190, #194, #199, #241, #258, #299, #306 | `vm-qa` | `cee1656c33` (44), `3387cf5da0` (46); `70b6c70ca7` fires on patches (F-06) |
| `u` | `bwrap`; BB (`:2926`) | #191; #308 F-WF-07/12 | `vm-qa` | `655f103cc5` (19 of 19) |
| `v` | BB `sed` (`:3040`) | #196 | `vm-qa` | `655f103cc5` (FAIL 2) |
| `w` | `bwrap`; host tools; no wrapper | #170; #273's trace | `vm-qa` | none |
| `x` | `bwrap`; BB with `flock` via `t`'s wrappers: the host's lacks it → 34 FAIL; host `python3`, `node`, `cc`/`gcc`, `qemu-img`, `jq`; the sources cache (retroarch, ppsspp-lr, webkitgtk, the client); git history (`417dcd8610` `:3316`, `:4271`): absent → an empty fixture, caught downstream (F-03). Groups: the sub-group table | #307/#308 streams C, D, F1 and F2; #209, #198, #247 | `vm-qa` | `417dcd8610 --old` named (`:3194`, `:4500`, `:6636`), not run; no header recipe reaches `x` |
| `y` | the sandbox (`sa_run`, F-16); BB `nbin` with `flock`: the host's lacks it → 180 FAIL; rclone (F-02); `jq`, `python3`, `node`; `t`'s client (`DT_OK`/`DF_OK`). Groups: the sub-group table | #307/#308 streams A and B; the fix round; #352, #467, #315 | `vm-qa` | named in comments: `417dcd8610` (`:8905`), `f3d19dc8fb` (`:11068`, `:12089`), `a06539d8ec` (`:8593`); none run, none in the header |
| `z` | `y`'s harness; host `python3`; the BB copy (`BB_HOST unzip`, `:13402`); the host's `/tmp` (S3F). Groups: the sub-group table | the fix round's stream B; #315; the audit of #313's fixes | `vm-qa` | `f3d19dc8fb` (`:13172`), `320d2b2bea` (`:13586`), `286759eb6d` (`:13663`), named, not run |
| `aa` | the retired `cloud_migrate_layout` (`:4547-4559`): absent at the hash → skipped except `:13904-13910` | #354 phase 5; blindspot 72 | `vm-qa` | none runnable |
| `ab` | `bwrap`, `setsid`; `cloud_scan` | #350, D-CLOUD-169, #508 | `vm-qa` | none: `cloud_scan` is absent at every header ref |
| `ac` | host `timeout`, `grep`, `cut` | #332 | `vm-qa` | none |
| `ad` | rclone (`:8908`); BB `flock`: the host's lacks it → 4 FAIL | run 100 case E | `vm-qa` | none |
| `ae` | `tools/rasteratops-cloud-layout-test` (`:14188`): absent → FAIL | #365, #383 | `vm-qa`; `--cloud-layout` | none here; that tool's own (T14) |
| `af` | rclone; BB `flock`: the host's lacks it → 6 FAIL | #401 | `vm-qa` | none |
| `ag` | `${ROOT}/tools/settings-modes-test` (the source checkout's); `--busybox "${BB_HOST}"`: refused by T14's S8 (F-07) | #421 | `vm-qa` | none here; that tool's own |
| `ah` | host `python3`; `tools/melonds-upgrade-test`; the same `--busybox` (F-07) | #526 | `vm-qa` | none here; that tool's own |

**The sub-groups** of `x`, `y` and `z` that carry verdicts (the coordinator, 00:27 and 00:33). The echoed groups are named in a run's output, and the comment-headed ones (`y1`-`y4`, D-fix, F2-20..24, A-fix) only by line range. The same four columns:

| Group | Lines | Checks (image) | (a) dependencies and absence | (b) catch | (d) positive |
| --- | --- | ---: | --- | --- | --- |
| `x/F1.` (with F2-1..13, F1i/j) | `:3198-4539` | — | `bwrap`; `python3`; `qemu-img`: absent → 1 FAIL for ~17 checks; `gcc`; the retroarch and ppsspp-lr tarballs: absent → FAIL (`:4008`, `:4297`); uid 0 → FAIL; git `417dcd8610`: absent → empty, caught downstream (F-03) | #307 PL-019 to PL-076; #308 F-VM, F-EM, F-PB; G-F1, G-F2 | `417dcd8610 --old` (`:3194-3196`); a planted `.partial`; vacuity detectors |
| `x/C.` | `:4540-6634` | — | `bwrap` (127 hidden by `2>/dev/null`, `:4610`); `python3`; `node`; `cc`; `timeout`; the webkit tarball → one SKIP (`:6491`); the git index (`:6506`) | PL-015 to PL-074; G-C; #308 F-RS; #508, #352, #330, #380 | `417dcd8610` (`:4500`: *54 FAIL and 25 PASS*); constructed (`:4723`, `:4879`, `:4951`) |
| `x/D.` | `:6635-7795` | — | `t`'s client (`DT_OK`): absent → 21 SKIPs and 4 silent omissions; BB `flock`: the host's lacks it → 33 FAIL; `python3` | PL-013, PL-055, PL-057 to PL-060; #308 F-RA | `417dcd8610` (`:6636`) |
| `y/y1` | `:7799-8396` | 65 (agent) | BB (`/p7bb`): absent → the `tar` shims exit 127, and `:7912` passes silently; `python3`; host `tar`; `/usr/bin/grep` | #307 PL-004 to PL-010, PL-035 to PL-039, PL-077; G-B; #537 | none named |
| `y/y2` | `:8397-8606` | 17 | BB; `bwrap`; an `nmcli` shim | #307 PL-003, PL-031; #308 F-WF; #318 | `a06539d8ec` (`:8593`), #318's two checks only |
| `y/y3` | `:8607-8683` | 10 | host-lifted functions; host `flock` (not in `bbin`); `timeout` | #307 PL-011, PL-040, PL-041; #308 F-PB | none |
| `y/y4` | `:8684-8905` | 21 | BB; host `mountpoint` without it; banner probes accept any busybox (F-20); `python3` | #307 PL-044 to PL-077, G-B-15 | none |
| `y/A.` | `:8906-11071` | 212 (agent) | rclone (F-02); BB `nbin` with `flock`: the host's lacks it → 95 FAIL; `jq`; `python3`; `t`'s client (`DT_OK` blocks with no `else`) | #307 PL-001 to PL-070; #308 F-CS; G-A; G-D | `417dcd8610` (`:8905`), not run |
| `y/F1r.` | `:11072-11223` | 15 | `python3` and `tools/vm-upgrade-readiness-test`; git `417dcd8610`, `73b20caf86`: absent → empty, `:11131` passes silently; `qemu-img`: absent → 4 checks dropped | #309 PL-024; #546; #551 | `f3d19dc8fb` (`:11068`), not run |
| `y/CF.` | `:11224-12093` | 32 | a shell rclone shim only; `cf_src` drops a missing file silently; CF4 `--unshare-net` unprobed; `node` | PL-009, PL-014, PL-021, PL-032; G2-C | named without a ref (`:11217`) |
| `y/D-fix` | `:12094-12343` | 12 | `t`'s client (`DF_OK`): absent → 4 SKIPs; the `--unshare-net` probe (`:12285`) | G2-D; S-24; S-26 | `f3d19dc8fb` (`:12089`) |
| `y/F2-20..24` | `:12344-12604` | 16 | `python3`; `gcc`; the RetroArch tarball: absent → FAIL | PL-020; G2-F2 | `f3d19dc8fb` (`:12321`) |
| `y/A-fix` | `:12605-13181` | 38 | as A | PL-001 to PL-034; G2-A | `f3d19dc8fb` (`:12603`) |
| `z/S315.` | `:13592-13664` | 25 | the sandbox; rclone never executed (`/ctl/fail` answers everything) | #315 | `320d2b2bea` (`:13586`) |
| `z/S3F.` | `:13665-13722` | 15 | the host shell, no sandbox; the host's `/tmp` (F-19) | the audit of #313's fixes | `286759eb6d` (`:13663`) |

**The split proposal (a lead for the coordinator).** A split by section would make 34 files, or about six by subject: the settings writers (`a`, `c`, `o`, `y3`), backuptool (`b`, `f`, `k`, `y1`, `z`), the cloud scripts (`d`, `g`, `h`, `i`, `j`, `l`, `n`, `ad`, `af`, stream A, CF, S315), the network (`m`, `q`, `u`, `y2`), the proxy (`p`, `t`, `D.`, D-fix), and the boot quirks (`F1.`, `F1r.`, F2), with the retired `aa` apart and `ae`'s live archive contracts (`:14183-14189`) with the cloud file, since `ae` is not wholly retired (the seat).
- **What it would cost:** the harness (`:259-430`), `src_of`, the busybox copy and the sandbox helpers would have to become a sourced library, which is one place to fix F-01, F-05 and F-16, but one more file `vm-qa` must keep beside the suite. A section-local fixture reused later (`o` reuses `a`'s, `c`'s and `m`'s; `D.` and A depend on `t`'s `DT_OK`) would become an explicit dependency between files. And the 30 skips and `NOT APPLICABLE` would need a verdict carried across files.
- **What it would gain:** an `--old` run per file, so a ref that predates `x` would still prove `a` to `w` (F-05); a failure attributable by file in `vm-qa`'s report; files a reader can hold whole (stream A alone is 2,166 lines; the combined cloud file would be larger, the seat notes); and a section's positive written beside it rather than in a header that stopped at `v`.
- **The cheaper half first:** F-05's fix, a script absent at `BASE_REF` making its section NOT APPLICABLE rather than ending the run, delivers the `--old` gain without a split.

### Q7 Clarity and structure

- **The header's claims** (`:7-148`) cover `a` to `w`; `x` to `ah` (933 of 1,313 checks) have none. Each section's `echo` line matches what its checks assert, except `t`'s *each compiled* (F-14) and `q`'s *the boot pass ran* (F-13).
- **`--help`** (`:239-250`): *Run the host script regression suite with the image's busybox* is false from every M6 worktree (F-01). It says an unusable **explicit** `QA_SYSTEM_ROOT` is an error, which is true, but not that an absent one falls back silently.
- **`vm-qa:22`:** *the scripts under busybox shims, on the host*: true, without saying whose.
- **`upgrade-and-install.md:216-221`:** *the test now runs every command that is a busybox applet on the device ... through the image's busybox from the build root*: true only where a build root is found (F-01). A rule: a lead, not edited here.
- **`instruction-files.md:175`:** the index row's Detail-in rule, `generic-x64-vm-testing.md`, names the file twice (`:1040`, `:1307`) and never describes it, T14's PL-12 shape. A lead for #1007's kind.
- **`:264` and `:266`** advise `setsid -f`, which does not reset an ignored SIGINT (F-18).
- **The split:** § Q6.

## Instruction File Recommendations

Leads for the coordinator; no rule is edited by this lane.
- `upgrade-and-install.md` § Verify on a device: add that a test which falls back to the host's tools must say so in its verdict (F-01's fix makes it true).
- `generic-x64-vm-testing.md`: describe this file under its index row, or move the row's Detail-in to a rule that does.
- `engineering-practices.md` § Guards must fail closed: the `2>/dev/null` on a read inside a pipeline (F-03) as a named shape, beside `ls A B`.

## Quality self-check

- Every finding cites a line at the hash, and every Medium or higher has its deciding artifact in § 4.5.
- The agents' leads not re-derived are marked as theirs or as inference.
- No count is given without its command: the 319 by `diff` of the verdict lines; the 1,313 by `grep -c`; the seconds by the timed run.
- **What reading cannot prove:**
  - whether `flock` causes all 131 flips that name no applet;
  - whether a host without `jq` or `node` behaves as read (not run);
  - the `--old` refs `717bc04449` and `51e2acece6` as the intended controls (not run).
