# T15's remediation streams (#662, audit issue #1040)

Written by the coordinator on 2026-10-25 at T15's stage-D pause
(D-WORKFLOW-189), in the shape of `t14-streams.md`: six streams, each with
the files it owns (one file: every stream edits `tools/last-good-scripts-test`
and nothing else, so the streams are ordered and never concurrent), the
test first, its `Already written:` line, its acceptance and its commits;
then the dispositions that are not streams; then the order and the
hand-back. The lane executes in its worktree
(`/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-last-good-test-662`,
branch `feature/m6-tooling-last-good-test-662`, stage-D tip `2eface0727`).
**Review depth per stream: Local** (plan § 6c). The file is its own test, so
**a stream lands with a new or re-run check whose constructed input fails
on the unfixed file and passes on the fixed one, or it is not a stream** --
the positive produced by running the case against an export of the stage-D
tip **made with `git worktree add --detach` or a clone, never `git archive`**
(the coordinator's own export carried no history and reported ten false
FAILs; the brief's erratum), or against a copy of the file with its other
sections cut, and quoted in `02` § The streams' positives. Every run that
judges the scripts starts with `QA_SYSTEM_ROOT` on the `069fc2704421` M7
root's `image/system` (a read of one file the suite copies) and **with
SIGINT at its default** (the `python3 -c` launcher from `vm-qa:158` when a
run cannot be foreground; `setsid` resets nothing -- the brief's § 5);
`TMPDIR` under `/workspace/tmp/m6-t15/`; the fallback cases run with
`QA_SYSTEM_ROOT` unset on purpose and say so.

**Nothing here runs a guest, a provider, a handheld action, a build,
`fork-worktree sync|remove|repair`, an edit to a script the file proves (a
`bug` for its lane), to T14's four tools (`7c1d729b57`; they merge before
this branch), to `tools/vm-qa` (T12's), to a rule or a decided register row,
or a write under `/workspace/repos/rocknix*` or `/tmp`.** `rm -rf` only as
`"${X:?}"/...` or a literal path, in its own short command.

**The lane's two questions, answered first.** (1) **PL-06's shape: the
seat's three distinctions are written into #1023's acceptance**, replacing
the coordinator's blanket per-section NOT APPLICABLE -- an invalid ref or an
unreadable required input is CANNOT (exit 2, at once, naming it); an absent
historical feature that the header promises as a FAIL is that FAIL (the
promise fires); a selected check that cannot run and is not promised is
counted as not run (NOT APPLICABLE by name), never PASS; and the run goes
on to a verdict that says which promises fired. The lane edits #1023's
acceptance to that text under this ruling (its own bug, filed under the
coordinator's earlier words). (2) **Q6's table keeps the 15 rows**: the
three comment-headed groups the read found carry verdicts, and the rule is
the one applied at 00:33 -- the rows follow where the runs attribute their
verdicts.

**What the lane found, in one sentence each, so the streams read in order:**
the suite judges the scripts with whatever busybox and rclone it can find
and never says whose, and its two calls into T14's writer tests hand them a
copy T14 now refuses while flattening their CANNOT and unverified exits into
FAIL (PL-01, PL-02: the two Highs; PL-03, PL-12, PL-21); its history reads
fail open and its twelve historical controls cannot reach a verdict (PL-04
to PL-07, PL-18, PL-22); a family of checks passes on a script that never
ran, a chain that reads only its last member, a negated pipeline, a race
ordered by `sleep`, a driver whose crash drops verdicts, a canary in the
host's `/tmp` (PL-09, PL-10, PL-14 to PL-17, PL-19, PL-20); a missing
download is a FAIL, one SKIP or a silent omission depending on the section
(PL-08); the sandbox passes the caller's environment and the host network
(PL-11); and `ag` runs the subject checkout's verifier, not the harness's
(PL-13). Two leads (PL-23, PL-24) are the coordinator's, below.

## S1. The tools' provenance: the fallback refuses or marks, the verdict says whose applets judged, stream A's rclone is the root's, section `b` and the PL-022 case use the copy, and the two writer-test calls carry their provenance and their children's exits (PL-01, PL-02, PL-03, PL-12, PL-21; #1018, #1019, #1020, #1029, #1038) -- `fix-case`

- **Why a stream:** the two Highs and #1015's root cause. Every run from an
  M6 worktree has judged the host's busybox 1.37.0 (319 FAILs, `flock`
  absent) and the host's rclone 1.60.1, and said so only in a banner line
  nobody reads; the suite's founding section `b` never used the copy at
  all; the two calls at `:14224` and `:14231` are refused by T14's S8 and
  their refusal is counted as a regression.
- **Files owned:** `tools/last-good-scripts-test` (`image_tool_source`
  `:381-401`; the copy and wrappers `:416-426`; the G-B-15 probes
  `:8777-8811`; stream A's rclone `:8906-8914`; section `b`'s profile and
  sandbox `:522-590`; the PL-022 case `:13399-13424`; `ag`/`ah`
  `:14221-14233`; `check` `:309-310` and the verdict `:14235-14238`).
- **The shape:** with `QA_SYSTEM_ROOT` set, the busybox and rclone come
  from it (an unusable one is exit 2, as today); with it unset, the three
  build-root globs are tried and, when none yields a busybox, **the run
  refuses with exit 2** naming what it lacks and how to supply it
  (`QA_SYSTEM_ROOT=<root>/image/system`, or a build root beside the
  checkout) -- **unless `--host-diagnostic` was given**, in which case the
  run proceeds on the host's tools with every result line marked `HOST`,
  and ends with a verdict that says NOT DEVICE EVIDENCE and exits **3 when no case failed, 1 when any case failed** (D-QA-063, the lattice every fork suite shares: a FAIL is never hidden behind the marked verdict; this sentence read `exits 3` until 02:42 UTC, when the lane asked on #662 whether to match T14's `--unverified-busybox` split -- it does); the verdict's final lines name
  the busybox's path, version and the root's BUILD_ID (from its
  `etc/os-release`) and the rclone's path and version; the G-B-15 probes
  check that provenance, not the word BusyBox; stream A's rclone is taken
  from the same root and `rclone version`'s first line is asserted equal to
  the recipe's `PKG_VERSION` (read from
  `projects/ROCKNIX/packages/network/rclone/package.mk` through `src_of`,
  so `--old` reads the ref's); section `b`'s sandbox binds the busybox copy
  and its wrappers first on PATH; the PL-022 case runs only under verified
  provenance and is a counted SKIP otherwise; `ag` and `ah` pass
  `--busybox-from <BUILD_ID>` when the root supplied the busybox and
  `--unverified-busybox` under `--host-diagnostic`, and a `check_child`
  helper carries a child's 2 as CANNOT and 3 as unverified (each counted
  and named in the verdict), 0 as PASS, else FAIL.
- **The test first** (in `02` § The streams' positives): from a worktree
  with no build root and `QA_SYSTEM_ROOT` unset, the unfixed file runs and prints `319 CHECK(S) FAILED` naming no applet set (the positive; the coordinator's `329` was read from a history-less export, ten of them the false FAILs of the 00:35 erratum -- the lane's clone with history gives 319, 03:01 UTC);
  the fixed one exits 2 at once with the message, and with `--host-diagnostic` exits 3 (or 1 when a case failed under the host's tools) with every line marked and the verdict NOT DEVICE EVIDENCE; a constructed root whose `rclone` is the host's
  1.60.1 (the lane's `rchost` root) is refused or marked by stream A
  (unfixed: 1,313/0, the positive); a constructed root whose busybox
  lacks an applet section `b` needs shows `b` reaching it (unfixed: host
  tools, the positive); a child double for `settings-modes-test` exiting
  2, then 3: the suite's verdict reads CANNOT / unverified, not FAIL
  (unfixed: FAIL, the positive); a run with `QA_SYSTEM_ROOT` on the M7
  root: `ag` and `ah` PASS with T14's tools read from `7c1d729b57` (the
  lane may stage T14's two fixed tools beside a copy of this file under
  `.qa-scratch/t15/` for the case; the tools themselves are never edited),
  and the verdict's final lines name the provenance.
- **Already written:** every recorded run from an M6 worktree (T12's
  three, T14's, this slice's run 2) judged the host's busybox and is read
  as host evidence (#1015); the record is not rewritten; `vm-qa`'s
  `scripts` row reads the new exit 2 as FAIL and 3 as SKIP by its rule at
  `:148` (T12's), which is the right reading; nothing on a device.
- **Acceptance (#1018, #1019, #1020, #1029, #1038):** the cases named with
  their positives; the full suite under `QA_SYSTEM_ROOT` on the M7 root
  at the stream's tip: its verdict, counts and provenance lines quoted.
- **Commits:** `last-good-scripts-test: no silent host tools -- refuse without a root, or --host-diagnostic marked, exit 1 on a failing case else 3; the verdict names the provenance (#1018)`,
  `last-good-scripts-test: stream A's rclone from the root, its version asserted (#1020)`,
  `last-good-scripts-test: section b binds the busybox copy; the PL-022 case needs verified provenance (#1029, #1038)`,
  `last-good-scripts-test: ag and ah carry --busybox-from or --unverified-busybox; a child's 2 and 3 reach the verdict (#1019)`.

## S2. History and the historical controls: the git reads fail closed, the two dead refs are the parents they meant, `--old` reaches a verdict with the three distinctions, `70b6c70ca7`'s `t` builds what it promises or retires, `--old` grades the ref, the header claims every section (PL-04, PL-05, PL-06, PL-07, PL-18, PL-22; #1021, #1022, #1023, #1024, #1035, #1039) -- `fix-case`

- **Why a stream:** twelve controls the header promises and none reaches
  a verdict (two refs dead, ten stopping at the first script the ref
  predates, one failing on patches instead of its checks); a history read
  that returns an empty fixture silently; `--old` grading the working tree
  in nine places; a header that claims `a` to `w` of 34 sections.
- **Files owned:** `tools/last-good-scripts-test` (`f1_tree_at`
  `:3205-3215`; `:4271`; the header `:7-148`, `:162-226`; `src_of`
  `:320-325`; section `t` `:2051-2086`; the `--old` reads at `:845-851`,
  `:887-890`, `:903-928`, `:2427`, `:3999`, `:4291`, `:10344`, `:6481-6507`;
  `--help` `:239-250`; the SIGINT comment `:264-266`).
- **The shape:** a git read a fixture needs ends the run at the read when
  it fails (exit 2, naming the ref and the path; no `2>/dev/null`, no exit
  inside a pipeline's subshell: read into a variable with its status
  checked); the header's two dead refs become `717bc04449` and
  `51e2acece6` once each is run and its promised sections FAIL; under
  `--old`, #1023's three distinctions (above): an invalid ref or
  unreadable input exit 2 at once, a promised historical absence a FAIL,
  an unpromised absent script a counted NOT APPLICABLE by name, and the
  run continues to a verdict that lists which promises fired;
  `70b6c70ca7`'s `t` builds the client pinned at `BASE_REF` (patches and
  pin from the ref) so the `012` checks run, or the recipe is removed from
  the header with its reason beside the others; every `--old` read goes
  through `src_of` or the ref's index; the header claims all 34 sections
  with each section's positive (a recipe, a constructed case, or `none`),
  and `--help` and the SIGINT refusal say what the code does (the launcher
  that resets SIGINT, not `setsid`).
- **The test first:** from an export made with `git archive` (the
  coordinator's shape): the unfixed file reports ten vacuity FAILs (the
  positive, already recorded); the fixed one exits 2 at the first read,
  naming `417dcd8610` or the ls-tree ref; `BASE_REF=0f7785e6ed --old` on
  the unfixed file: `invalid object name` (the positive), on the fixed
  header the replaced ref's run FAILs `q`'s promised checks; `BASE_REF=1d1503180d
  --old` unfixed: exit 2 at `s` (the positive), fixed: a verdict with `s`
  onward NOT APPLICABLE by name and the promised FAILs counted;
  `BASE_REF=70b6c70ca7 --old` unfixed: 43 patch FAILs and no `012` line
  (the positive), fixed: `t`'s `012` checks FAIL by name, or the recipe
  gone and the header saying why; `BASE_REF=1d1503180d --old`: `g` and
  `i` FAIL or NOT APPLICABLE rather than PASS; the twelve recipes re-run at
  the stream's tip, their verdicts and FAIL counts in the table in `02`.
- **Already written:** nothing on a device; the coordinator's history-less
  export is retired; the record's `--old` outputs from stage A are the
  before column of the table.
- **Acceptance (#1021 to #1024, #1035, #1039):** the cases named with
  their positives; the twelve-recipe table at the tip; the header's 34
  claims each pointing at a positive.
- **Commits:** `last-good-scripts-test: a history read fails closed at the read (#1021)`,
  `last-good-scripts-test: the --old refs the header meant (#1022)`,
  `last-good-scripts-test: --old reaches a verdict: CANNOT, a promised FAIL, or NOT APPLICABLE by name (#1023)`,
  `last-good-scripts-test: 70b6c70ca7's t builds the pinned client, or the recipe retires with its reason (#1024)`,
  `last-good-scripts-test: --old grades the ref everywhere (#1035)`,
  `last-good-scripts-test: the header claims every section with its positive; --help and the SIGINT advice say what the code does (#1039)`.

## S3. The fail-open check shapes, one commit per bug (PL-09, PL-10, PL-14, PL-15, PL-16, PL-17, PL-19, PL-20; #1026, #1027, #1031, #1032, #1033, #1034, #1036, #1037) -- `fix-case`

- **Why a stream:** eight shapes in which a check passes without its
  subject having run or its claim having held, each named by line in `05`;
  T10's five fail-open shapes and `engineering-practices.md` § Guards must
  fail closed are the checklist.
- **Files owned:** `tools/last-good-scripts-test` at the lines each item
  names.
- **The shape, per bug:** #1026 every *rc non-zero and nothing written*
  check also requires a witness that the script started and reached the
  guarded step (a marker the shim writes; the representative set named in
  `02`, the rest by the same helper); #1027 each case at `:3051` its own
  `check`, and `:3061` requires `sa`'s status; #1031 each race holds the
  first party at a barrier until the second reaches the contended step and
  asserts it did; #1032 each driver's exit required 0 and its verdict ids
  equal to the expected set; #1033 every `check` call carries three
  arguments (a static count); #1034 each negated pipeline extracts into an
  owned file with its status required, then tests grep's 1 exactly; #1036
  the five predicates match their claims (the pass's own status; the ref's
  fragment list; compilation required for *each compiled*; the retirement
  gate reading the stated contract -- the seat's G-05, the fragile gate
  behind the withdrawn F-08; D21 requiring `100755` exactly); #1037 the
  canaries under the run's own temp root, each function's presence and
  exact status asserted.
- **The test first:** one constructed input per bug, as its acceptance
  names (a sandbox that cannot start; a `set_autosave` that writes the
  third case's output first; a broken lock; a driver that raises after its
  first verdict; a two-argument `check` found by the static count; a
  missing archive member; a violation of each of the five predicates; an
  absent `sort_settings`), each failing on the unfixed file (the positive)
  and passing on the fixed one; the full suite under the M7 root after the
  last commit (its counts quoted: the fixed checks that now FAIL on the
  tree, if any, are `bug`s for the scripts' lanes, named).
- **Already written:** nothing on a device; `/tmp/s3f-*` is absent after
  the slice's runs (`ls`, recorded in `05`).
- **Acceptance:** each bug's criteria from its own case.
- **Commits:** one per bug, `last-good-scripts-test: <the fix> (#N)`.

## S4. A missing download takes one rule, counted per dependent check (PL-08; #1025) -- `fix-case`

- **Why a stream:** the same absence is a FAIL here, one SKIP standing in
  for many checks there, and a silent omission elsewhere; on a host
  without the sources cache, section `D`'s 33 busybox FAILs would read as
  SKIPs.
- **Files owned:** `tools/last-good-scripts-test` (`:4004-4008`,
  `:4296-4297`, `:6490-6491`, `:6649`, `:7040-7078`, `:10128-10358`,
  `:11180`).
- **The shape:** one rule -- a dependency the host lacks makes each
  dependent check a counted SKIP by name (D-QA-061's word: the run exits
  3 if nothing failed), never a FAIL that blames the script and never an
  `if` with no counted branch; the dependency and the way to supply it
  named once at the first SKIP.
- **The test first:** the client tarball hidden (a constructed empty
  sources cache): the unfixed file drops `D`'s checks uncounted and
  SKIPs the webkit patches as one (the positive); the fixed one counts
  each dependent check as SKIP and exits 3 with the dependency named.
- **Already written:** nothing on a device.
- **Acceptance (#1025):** the case with its positive; `grep` over the
  guarded blocks shows each with its counted branch.
- **Commits:** `last-good-scripts-test: a missing download is a counted SKIP per dependent check (#1025)`.

## S5. The sandbox allowlists its environment and unshares the network (PL-11; #1028) -- `fix-case`

- **Why a stream:** `sa_run` (150 calls) passes `RCLONE_*`, `BASH_ENV`
  and exported functions and keeps the host network; T14's S2 closed the
  same shape in its four tools with `--clearenv --unshare-net` and named
  variables.
- **Files owned:** `tools/last-good-scripts-test` (`sa_run` `:9010-9022`;
  the four invocations that already unshare, `:6108`, `:11890`, `:12285`,
  `:12303`, aligned; `:12312`).
- **The shape:** `--clearenv`, `--unshare-net`, `--setenv` for `PATH`,
  `HOME`, `LANG=C`, `TERM=dumb` and the case's own variables, each named;
  a case that needs loopback or an inherited variable says so beside its
  `sa_run` with the reason (the lane reads the 150 call sites' needs first
  and lists the exceptions in `02`).
- **The test first:** the caller exports `RCLONE_CONFIG`, an
  `RCLONE_CONFIG_QA_TYPE` remote, `BASH_ENV` and a function; a probe
  script through `sa_run` on the unfixed file sees all of them and the
  host's interfaces (the positive, as T14's `sandbox-case.py`); on the
  fixed file none of them and `lo` only; the full suite under the M7
  root passes as before.
- **Already written:** nothing on a device; no external connection is in
  the record.
- **Acceptance (#1028):** the case with its positive; the exceptions
  listed.
- **Commits:** `last-good-scripts-test: sa_run clears its environment and unshares the network (#1028)`.

## S6. `ag` runs the harness's own verifier (PL-13; #1030) -- `fix-case`

- **Why a stream:** with `LAST_GOOD_SOURCE_ROOT` set, `ag` runs the subject
  checkout's `settings-modes-test` against `--help`'s promise that the
  harness is not replaced; `ae` and `ah` already use `${HARNESS_ROOT}`.
- **Files owned:** `tools/last-good-scripts-test:14224`.
- **The shape:** `${HARNESS_ROOT}/tools/settings-modes-test`.
- **The test first:** `LAST_GOOD_SOURCE_ROOT` naming a checkout without the
  tool: the unfixed `ag` fails to find it (the positive); the fixed one
  runs the harness's.
- **Already written:** nothing on a device.
- **Acceptance (#1030):** the case with its positive; `grep -n
  settings-modes-test` shows `${HARNESS_ROOT}`.
- **Commits:** `last-good-scripts-test: ag runs the harness's settings-modes-test (#1030)`.

## Dispositions that are not streams (the coordinator's, written into the Phase 7 table by the lane)

- **PL-23 (the rules and the index):** the coordinator adds the two rows
  to **#1007** at this pause (`upgrade-and-install.md:216-221`'s sentence
  that the test runs the image's busybox from the build root -- true only
  where one is found, and after S1, true or refused; `instruction-files.md:175`'s
  pointer at a rule that never describes the file); rule edits at
  integration, never by the lane.
- **PL-24 (the split):** a **Backlog the coordinator files at this pause**:
  the split by subject behind a shared harness library, the seat's
  agreement, the cost and gain from `04` § Q6, and the cheaper half (S2's
  `--old` shape) landing first; a design for the coordinator and the
  maintainer, not this slice's.
- **F-08 (withdrawn):** `NOT APPLICABLE` marks a retirement and is not
  counted as a pass; its fragile gate (G-05) is in #1036 (S3).
- **The 15-row sub-group table** stands (the lane's question 2).
- **For the maintainer, on #346 (the coordinator posts at this pause):**
  the `--host-diagnostic` contract (a run on the host's tools is marked and exits 3, or 1 when a case failed, never a bare PASSED -- D-QA-063) as the shape every host-side suite in
  the fork follows from here -- a register row if it is contested.

## Order and hand-back

S1 first (it changes what every later run reports, and S2's recipe runs
need its provenance lines); S2; then S3 (one commit per bug, in the order
listed), S4, S5, S6. One file, so the streams are serial and each commit
is a working suite: after every stream the full suite runs once under
`QA_SYSTEM_ROOT` on the M7 root and its verdict and counts go in `00`
(the tree's figure is 1,313 / 0 / 0 at the hash; a check that now FAILs
on the tree because its predicate got stronger is a `bug` for the script's
lane, named in `02`, never softened). Each commit cites its bug (`Refs #N,
#662`, no closing keyword) and carries the attribution line; `git status
--short` before every `git add -A` (`.qa-scratch/` is gitignored; the
suite's temp root is under `/workspace/tmp/m6-t15/`).

After S6: the Phase 7 table and the `punch_index` at their outcomes
(`fixed`, `deferred` with its issue, `design` with its sentence), `02`
§ The suites re-run (the full suite under the root; the `--host-diagnostic`
run; the twelve recipes' table; the fallback refusal), § The streams'
positives, the lint on the folder (`PASS`, the default phase), `fixed-at:`
in #662's body, the retro (stage G, posted on #662: what the slice did to
the two time-to-play numbers -- nothing; what each stream did to the
suite's refusals; the brittleness after-column), then the hand-back
comment naming the tip and each artifact by path. The coordinator accepts
by `AUDIT_ISSUE=1040 $S/t15-accept.sh <tip> <coordinator tip>` on an export
**made from a clone of the lane's branch** (the inventory block, the file at
the hash against the dispatch tip, `--help`/`--nosuch`, the two call sites'
flags, one run of the fixed suite with `QA_SYSTEM_ROOT` on the M7 root and
one without it -- the refusal -- and one with `--host-diagnostic` -- the marked exit 3, or 1 on a failing case -- each started through the launcher, `register-check` and
`rules-check` on a simulated merge), reads every stream's diff and
positives, ticks #662 and #1040 from the artifacts, closes #1040 when its
checkboxes read back ticked by name, and merges the branch in its turn
(after T14's, before T4's and T45's); the `vm-qa` `scripts` row's words
(T12's) and the rules' sentences (#1007) are the coordinator's at the
merge.

## Root change, 2026-10-25 05:41 UTC (the coordinator's)

Every "the M7 root" above -- the `069fc2704421` root's `image/system` that
stage A and the S1 runs judged with -- reads, for every run from 05:30 UTC,
as M6's retained donor `/workspace/artifacts/m6-donor/1a0266484423/image/system`:
the busybox (`79e7b20ddbe5abb6d18690dacc9b31803eb72cea949fce0a52cd9c2888829346`, BusyBox v1.36.1 built 2026-10-05 03:37:19 UTC, 574456
bytes, with its 146 applet links), `usr/bin/rclone` v1.75.2 (`ed887da83d3e2c07ff8acc60cb5b56dbe7bb4d73cc445b6ff71988f164c0558a`) and
`etc/os-release` (`f537766379be27c18708a87bae0495170f83b7fc966a69f5c1c5d84480f0d31d`; BUILD_ID `1a026648442321609b2288c2c9c06803817f9df2`),
each a byte-equal copy (`cmp`) read once at 05:38 from
`m7-pixelelated-replacement20`'s GENERIC_X64 root while no process referenced
it; `RECORD.txt` and `SHA256SUMS` two levels up. The M7 lane renamed the
`069fc2704421` root to `m7-signin-generic-build-20261025-01` at about 05:33
for its `bcc866f1` rebuild, which replaces that `image/system`; T15 had
stopped its five shells and the run in flight at 05:30 under the 05:22 grant
(#662, 05:32), and the runs it recorded before then stand under
`069fc2704421`. The busybox's identity with the old file is argued from its
version string, build time and size (the old file is gone, so no `cmp`),
never claimed. No M6 run sets `QA_SYSTEM_ROOT` under
`/workspace/repos/rocknix.worktrees/` again; the coordinator's acceptance run
A uses the same donor. The artifact's owning issue is #662; it is retired,
with a work-log line naming the path and the hashes, when no open M6 slice or
acceptance script names it (D-INFRA-022).
