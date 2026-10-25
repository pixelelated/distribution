# Mini Retro: M6.P2 T13, the cloud test harness (#660)

**Completed:** 2026-10-25
**Scope of this retro:** T13 from dispatch (`e1d51b3a04`, 04:58 UTC) to the
end of stage F (`4cbbe3e515`). Stages A to D were the read, the seat and
the punch list. Stage E was three streams of fixes to the nine tools. Stage
F was the fixes the guest cycles found. Three guest windows were granted on
#660. The audit itself is
`docs/audits/2026_10_25-epic-m6-cloud-harness/`. Its Phase 3 retrospective
(`03-retrospective.md`) is about the *harness*; this one is about the
*slice*.

**Branch:** `feature/m6-cloud-harness-660`. 45 non-merge commits since
dispatch, 21 of them touching `tools/`, and only four of the nine tools
changed (`cloud-test-backend`, `cloud-round-trip`, `cloud-connections-test`,
`cloud-census`). No file on the image path changed (`git diff --name-only
e1d51b3a04 HEAD -- projects packages distributions scripts config`: 0).
**Delta:** 26 punch-list items (18 resolved, 8 deferred to the coordinator's
Backlogs, 0 open). 17 `bug` issues filed and fixed (#1057-#1070, #1081,
#1092, #1093), every checkbox ticked from an artifact. 12 positives kept as
drivers under `stage-e/`, each run both ways and crossed. Three guest
windows: 07:52-08:09 (one guest), 08:19-08:23 (a pair), 08:35-08:41 (one
guest), each with START, RETURN and a leftover check of zero. Both scratch
retirements are recorded in 00 under D-INFRA-022: 4,418 MiB, then 2,212 MiB.

## The two questions the brief asks the retro to answer

**What the slice did to time to play:** nothing. It changed host-side test
tools and documents only. No script, package or image file moved, so
neither number (interface to a game's first frame; one game's exit to the
next one's first frame) can have changed.

**What T16 inherits:**

- **The assertion-shape table:** 02 § Assertion shapes, 79 rows, generated
  and checked against the AST and the registries. After the seat: 24 rows
  read both ends, 46 plant an input, 8 judge by the device's own report,
  and `CONTRACT` is marked apart.
- **Verdicts T16 may trust at `fixed-at` (`3a653eaec4`) or later:**
  - every *both ends* row;
  - the suite's PASS line, which now carries its counts and exits 3 when
    nothing was checked (#1059, D-QA-063);
  - the SFTP endpoint's content tier (#1067);
  - KILL1 (#1062, #1092), A15 (#1093), CAP13 (#1065) and KILL5 (#1070),
    each seen to reach its verdict on a guest;
  - A5 and RETENTION, which SKIP while there is no reconciler (#1057).
- **Verdicts T16 may not trust:**
  - the 8 *device report* rows as evidence about the code under test (they
    certify it by its own output);
  - any run before `fixed-at` of KILL1 (NameError), A5/RETENTION (vacuous
    PASS lines), A15 and CAP13 (needles that could not match), or the SFTP
    content tier between `94c050ed5a` and `7a71af7671` (the directory
    cache);
  - KILL1's drained-re-run SKIP, which has been seen on the host only;
  - anything a deferred item names: fixed waits (#1078), unpinned backend
    images (#1077), the host's rclone (#1076), the rule's drift (#909).

## What worked well

- **A positive is a file, not a sentence.** Each fix's case is a driver
  under `stage-e/` that takes the tool and `unfixed|fixed` and prints one
  verdict line. A crossed run prints `UNEXPECTED`. Rerunning all twelve at
  the end took seconds, and it showed that #1092's change to `fx_kill1`
  had not broken pos1062's AST check of the same function.
- **The host first, as a table.** #1067's guest regression was diagnosed on
  the host in four minutes with two servers by two conditions (fixtures
  there at start, or written after). The coordinator's version hypothesis
  died in one row: both 1.60.1 and 1.75.2 hid the late fixtures and both
  showed them at 1 s. The ruling's fallback (`CLOUD_QA_RCLONE`) was not
  needed and was not built.
- **Short, bounded windows.** The three windows used 17, 4 and 6 minutes of
  their 45, 25 and 15. Each had a written plan, a START and RETURN on #660,
  a stop by owned pid, and a leftover check. Nothing was left running.
- **Fixes that make a cell say more when it fails.** KILL1's after-re-run
  failure names each file's state, the suite's verdict line names its
  counts, and the backend refuses a misplaced option with exit 2. A failure
  that names its state is the next diagnosis already half done.

## What was harder than expected

- **The first guest cycle found four defects** (G-1 to G-4), because stage
  E's fixes let cells run further than any recorded run had: KILL1 had
  stopped at a `NameError` since `931a413457`, and A15 and CAP13 had not
  run since their needles went stale. That cost two more windows. The
  futro predicted that the harness is not run (*"seven tools have no
  caller"*); it did not predict what a cell that has never reached its
  verdict holds behind the first failure.
- **#1067's fix regressed the function it secured.** The host positive
  proved confinement (`/etc` refused, the host's keys refused) and never
  listed a file put after start. That is the one thing the content tier
  does. A backend change's positive must exercise the backend's job as
  well as its property.
- **My own slips, each recorded where it happened:**
  - The first guest clone held `tools/` only, which cost a KILL1 rerun.
  - The first host proof of the cache fix listed inside the 1 s window and
    read rc 3 on the fixed tool.
  - G-1 quoted `rclone exit 5` from a guest log that was never kept.
  - The first cycle did not pass `--dump`, so KILL1 1a's re-run output went
    with the guest disk and that case cannot be read.

  The last two share a shape: **a window's record kept the verdicts and not
  the outputs the verdicts were read from.** The third window kept
  `dump-kill1/` and the guest's log lines.

## What we discovered

- **A log-wording check goes stale silently.** CAP13 and A15 both looked for
  sentences the scripts had stopped printing (A15's since `f864baac02`, three
  weeks), and nothing ran them. That is two instances in one slice, the
  rule-of-three's second.
- **Every `rclone serve` endpoint caches listings for five minutes** unless
  told otherwise. WebDAV had been told since 2026-09; the new SFTP endpoint
  had not. `settle_cache` now covers both, and the comment says why.
- **KILL1 1a on the first cycle:** the cut file was whole v2 after the kill
  and not v2 after a 124 re-run. It did not recur on the third window. It is
  a *keep an eye on* on #1092, not a known bug (`bugs-are-agent-first.md`
  rule 4): seen once, with no retained evidence that explains it.

## Adjustments (proposals for the coordinator)

1. **A needle check for the harness.** Every string literal a
   `cloud-round-trip` cell looks for in a script's output or log
   (`... in tail`, `... in out`) should occur in the shipped sources it
   reads, or be marked as the harness's own. A host lint like that would
   have caught both G-3 and G-4 the day `f864baac02` landed. It belongs to
   the deferred harness work (#1078's neighbourhood) or to T16's brief. I
   have not filed it; filing is the coordinator's call.
2. **A window's record keeps the outputs, not only the verdicts.** Every
   KILL/LINK run passes `--dump` into the window's record directory, and
   any guest log line quoted in the audit is copied there before the guest
   stops. This is a line for the next brief's § guest cycle, not a rule
   edit.
3. **A backend change's positive exercises the backend's job.** For a
   storage endpoint, that means "put after start, then list" beside the
   security property. `stage-e/pos1067cache/run.sh` is that case now.
4. **No changes to T16's order.** Its brief inherits the two lists above.

## Scoped audit (Step 2.5)

- **AC conformance:** PASS. Every checkbox on the 17 bugs is ticked with
  its artifact quoted on the issue, and the audit issue's are all at an
  outcome. #660's own checkboxes are the hand-back's.
- **Cornerstone spot-check:** PASS for the slice's rules:
  - only the nine tools changed under `tools/` (0 file lines outside them);
  - no credential literal (the fixture is assembled at run time, #1061; the
    pre-commit scan passed on every commit);
  - removals only as a literal path, in their own command;
  - no closing keyword in any commit.
- **Interaction-defect scan:** PARTIAL. The harness and the QA backends
  shared state that only a guest exercised: the SFTP cache (G-1). The
  combination was found and fixed. The S3 path of KILL1's judge is proven
  on the host only.
- **Futro prediction verification:** 7 of 8 confirmed.
  - Confirmed: `cloud-pair-migration` exits 2; `cloud_reconcile` was never
    added; seven tools have no caller; positives were unrecorded; #909's
    drift; `:latest` images; the host's rclone.
  - Refuted: the pre-mortem's MinIO `cat` of a missing key exiting 0 (stage
    A: rc 1 on all three backends).
  - Missed: the two High bugs (#1066's deletion of an occupied
    `/storage/roms`, #1067's unconfined endpoint) and every defect a cell
    hid behind its first failure.
- **Housekeeping:** PASS. All twelve positives pass at `3a653eaec4`;
  `lint-audit-artifacts` passes at pre-issue and resolution. No
  `__pycache__`, and no scratch under `/workspace/tmp/`.
- **Harness self-coverage:** PASS. Each new check was seen to fail on the
  unfixed tool (the drivers' unfixed arm) and to report `UNEXPECTED` when
  crossed.
- **Documentation freshness:** PARTIAL. The rule `rclone-cloud-sync.md`
  still carries the stale no-network sentence (#909, T4's fix), and nothing
  in the rules mentions `rclone serve`'s cache. That is a candidate line for
  the rule's next edit under #909, which this lane may not make.

## Practice adjustments

- The mini-retro's "harness self-coverage" check asks whether a new guard
  covers the failures met while landing it. Here the relevant question was
  sharper: *did the positive exercise the thing the fix could break?*
  #1067's did not. That question is worth a line in the scoped-audit
  reference. This lane did not edit the skill, so it is offered to the
  coordinator.
