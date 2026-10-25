---
slice: T15
id: tooling-last-good-test
issue: "#662"
epic: "#903"
area: tooling-and-guards
kind: read
lens: brittleness
depth: Independent
version: 2
written: 2026-10-24 (version 1); 2026-10-25 (version 2, after the stranger's proof and the coordinator's two runs at the hash)
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
---

# T15: the last-good scripts test (`tools/last-good-scripts-test`)

**Version 2, 2026-10-25, by the coordinator** (version 1 on 2026-10-24; a stranger's proof found 8 wrong and 10 partial figures, corrected here and listed in the futro's errata). A brief for a lane that
has never seen this project, in the shape of T14's
(`docs/reviews/briefs/tooling-state-tests.md`): identity, scope, what to
read first, the questions, the evidence floor, the outputs, the
acceptance checklist, the stop conditions, the ceremonies, the hand-back.
The order's § T15 (`docs/reviews/order.md`, P1's `2174265e9c`) is the
slice's definition; this brief is the work. Every figure here was produced
by a command run at the hash named beside it; a stranger's proof of this
brief precedes dispatch, and version 2 records what it found.

## 1. Identity

- **Issue:** #662 `M6.P2 E903/T15: tooling-and-guards: the last-good scripts
  test`, slice `tooling-last-good-test` (`k: 15`) in `docs/reviews/slices.json`,
  fifteenth in `docs/reviews/order.md` (its row: *1 | 14,238 | 14,238 (14,238) |
  0 | Independent*; its `why`: *one file of 14,238 lines that proves the
  scripts under the image's busybox (blindspot 34). An explicit exception to
  plan § 5, which bounds a slice by about 8,000 to 12,000 lines: a test split
  across two sessions loses its fixtures' context. The brief invites the
  file's split as a Q7 finding; read before the code it proves under
  D-WORKFLOW-186*). **Epic:** #903 (the tooling and guards: T9, T10, T12 and
  T14 accepted today; this slice; then T45 #692). **Milestone:** M6; its body
  holds the live order; read it first. **Predecessors that bear on this file
  directly:** **T14 #661** (accepted 23:33: its four tools this file calls --
  `wait-lock-test`, `rasteratops-cloud-layout-test`, `settings-modes-test`,
  `melonds-upgrade-test` -- were fixed on `feature/m6-tooling-state-tests-661`;
  its S8 contract makes the two writer tests **refuse a busybox that is not
  a build root's** unless told `--busybox-from <BUILD_ID>` or
  `--unverified-busybox`, which this file's calls at `:14224` and `:14231`
  do not yet say -- #997's two-line change is **this slice's first stream**,
  not a coordinator edit; its connections fixture now passes `--config`
  after the command because this file's shims read `$1 $2`, #999), **T12
  #659** (accepted 23:39: `vm-qa`'s `scripts` suite runs this file, 13 of a
  default run's 33 minutes; its two stage-E cycles found the suite FAILing
  319 checks from a worktree with no build root, **Bug #1015**, under this
  slice), **T10 #657** (its retro's five fail-open shapes are this slice's
  first checklist; `tools/lint-audit-artifacts`'s fixtures), **T9 #656** (the
  model of a control with constructed positives). **Beside it:** nothing
  running; T45 waits.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #662, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for every defect it finds (D-WORKFLOW-187). Nothing else.
- **One worktree, one session.** Branch `feature/m6-tooling-last-good-test-662`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-last-good-test-662`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #662). **Before that
  comment exists nothing runs in it.** The session is the T3 lane's
  (`m6-t3-emulators`), which ran T3, T30, T24, T4, T10 and T14; those
  worktrees stay beside this one, idle, until their merges, and nothing is
  written there -- **T14's fixed tools are read from its branch
  (`git show 7c1d729b57:tools/<name>`), never run from its worktree.** The
  primary checkout `/workspace/repos/pixelelated/distribution` stays on
  `next` (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*` are the
  M7 lane's, **read only -- and this slice reads one thing there: a build
  root's `image/system/usr/bin/busybox`, through `QA_SYSTEM_ROOT`, which the suite copies into its own run directory before any sandbox binds it (the file's own comment at `:403-414`)**. **The rules in this worktree are
  `next`'s except the paths the dispatch comment lists.**
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Independent** (plan § 6c, `slices.json` k 15: *an ordinary
  code slice*): one reviewer from another lab through the Facilitator
  (`tools/council/run invoke --member gpt --provider openrouter`): **GPT-6
  Astra at `max`**, a probe first, then one refutation pass over one packet,
  as T12's and T14's Phase 4.6 did. `npm install --prefix tools/council`,
  `verify-pins` and `test` first; the key is `~/.config/council/env`, sourced
  by `run`, never read into a transcript. **A failed seat is a hold**, never
  a self-grading; a seat cut by its output ceiling re-runs on a trimmed
  packet (D-WORKFLOW-195). **The packet is one file of 1,167,697 bytes
  (1.11 MiB) at the hash**, which is over any seat's comfortable input: the
  packet is **the file's section index** (the 34 `echo "  <letter>. ..."`
  lines with their line numbers), **the harness (`:1-430`: the header, the dispatch, the busybox source and the shims), the `check`/`skip`/`src_of` helpers, the sandbox helpers (`sa_new`, `sa_script`, `sa_run`, `sa_tail`, `sa_outcome`, `:8993-9029`),
  the four call sites (`:14188`, `:14224`, `:14231`, `:252`) and the verdict
  (`:14236-14238`)**, plus the sections the lane's Q3 names as suspect, each
  whole; the seat is told the file's size and asked which other sections it
  wants, and gets them in a second packet if it asks. The packet is scanned
  with `tools/forbidden-terms-check --stdin` and the pre-commit's patterns
  before it is sent (T10's rule; this file carries a credential-shaped
  fixture literal at `:8004`, #962 -- the scan decides whether the packet
  may carry it or must redact it as PL-012 says). `review-plan.json`
  records depth `independent`, scope `epic`, primary
  `anthropic/claude-opus-5-5` / lab `anthropic`, one reviewer `gpt`
  (`openai/gpt-6-astra`, `openai`, `max`), provider `openrouter`,
  `allow_fallbacks: false`.
- **The host, read on 2026-10-24 by the coordinator:** M6's since M7's
  23:04 final return (its installer VM02 passed); census qemu 0; no M6 guest
  queued. **Two M7 build roots on this host carry a GENERIC_X64 image
  busybox, read only:**
  `/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20/build.pixelelated-GENERIC_X64.x86_64/image/system`
  (BusyBox v1.36.1, BUILD_ID `1a0266484423…`, the one T14 used) and
  `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system`
  (BusyBox v1.36.1, BUILD_ID `069fc2704421…`, **the image T12 booted**). The
  host's own `/usr/bin/busybox` is **BusyBox v1.37.0 (Ubuntu
  1:1.37.0-7ubuntu1)**, which lacks the `flock` applet the image's has
  (T14's hand-back, 23:28: 61 of its FAILs printed `flock: applet not found`).
  **No M6 worktree has a build root with a busybox** (twenty `build.*`
  directories, none with `image/system/usr/bin/busybox`), so from any M6
  worktree `image_tool_source` falls to the host's busybox and says so only
  in its banner line.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-last-good-test-662
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-tooling-last-good-test-662
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists, nothing else
cat .github/sessions/saved-session-state-feature-m6-tooling-last-good-test-662.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l   # the host file's last lines and the live census, before anything
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git show 8ebaf8daad:tools/last-good-scripts-test | wc -l -c          # 14238 1167697
git diff --stat 8ebaf8daad HEAD -- tools/last-good-scripts-test      # empty: the file is at the hash on this branch
ls /workspace/repos/rocknix.worktrees/*/build.*GENERIC_X64*/image/system/usr/bin/busybox   # the two read-only roots above
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-tooling-last-good-test-662
```

## 2. Scope

**One path, `tools/last-good-scripts-test`: 14,238 lines, 1,167,697 bytes
at `8ebaf8daad` (`git show 8ebaf8daad:tools/last-good-scripts-test | wc -l -c`);
fork-own, shell, reach `n/a`; 408 fork commits from `52c4249759`
(2026-09-10, *tools: last-good-scripts-test -- device-less proof that the
writers keep the last good state*) to `37d26a203e` (2026-10-14, the
inventory's `last_fork_commit`); none on `upstream/next`.** The membership
is the one glob; the inventory row (`docs/reviews/inventory.json`, columns
`tree, path, area, tier, ..., lines, last_fork_commit, reach`) is:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys
inv=json.load(sys.stdin); cols=inv["columns"]
for r in inv["rows"]:
    d=dict(zip(cols,r))
    if d["path"]=="tools/last-good-scripts-test": print(d)'
# {'tree': 'distribution', 'path': 'tools/last-good-scripts-test', 'area': 'tooling-and-guards', 'tier': 'fork-own', 'language': 'shell', 'lines': 14238, 'last_fork_commit': '37d26a203e 2026-10-14', 'reach': 'n/a', ...}
```

**What the file is** (read at the hash): a bash suite of **34 sections,
`a` to `ah`** (`grep -n -E '^echo "  [a-z]{1,2}\. ' tools/last-good-scripts-test`:
`a` at `:429` ... `x` at `:3113`, **`y` at `:7796` (5,386 lines to `:13181`: audit #307/#308 stream B's cases `y1` to `y4` at `:7796-8905`, 1,110 lines, then stream A's `A`-cases from `:8906`, 4,276 lines)**, **`z` at `:13182` (the fix round's audit, 541 lines)**, `aa`
to `ah` at `:13723-14229`), each a group of `check` calls (`check()` at
`:309`: `PASS` or `FAIL` and a counter; 120 `check` call sites, many inside
loops -- T14's run counted 1,313 checks and T12's 1,378 on their branches'
copies, so the count is a property of a run, not of the text), with `skip()` at `:302` (`SKIPPED`, exit 3 at the end: *a check that did not run has not passed* -- the verdict at `:14236-14238` has D-QA-061's three words, **and a fourth: `NOT APPLICABLE` (`:4558`, the retired `cloud_migrate_layout` group, #508) is reported at `:14235` and the run then exits 0 `PASSED` when nothing failed or skipped -- a group that did not run passes, Q3's first item**). The harness (`:1-430`): the header lists every section's claim with
its issue; the dispatch refuses an unknown option (exit 2) and a run with
SIGINT ignored (exit 2, `:260-268`); `set -u` only (`:270`; **no `-e`, no
`pipefail` at the top**); `src_of` (`:320`) lifts each script under test
from the working tree or, under `--old`, from `BASE_REF` (default
`1d1503180d`), exit 2 when it cannot; **`image_tool_source` (`:381-401`)**
takes `QA_SYSTEM_ROOT` when set (an unusable one is an error, exit 2), else
globs three distro-named build-root layouts (`${ROOT}/../*/build.{ROCKNIX,RASTERATOPS,pixelelated}-*`, `${ROOT}.worktrees/*/build.{...}-*`, `${ROOT}/build.{...}-*`), **else `command -v busybox || true` -- the host's busybox if it has one, silently, named only by the banner at `:426` (`-- a copy of /usr/bin/busybox`); and a host with no busybox at all gets no copy, no wrappers and no banner line, and the run proceeds on the host's GNU tools with nothing said**; the busybox is **copied** into the run (`:416-418`; the comment at `:403-414`) so an image step beside the harness cannot pull it (the 2026-09-25 case the comment records, #272) and wrappers for `sed mv cp tr head wc cut awk stat chmod cat` are generated (`:420-422`) -- **the wrapper list differs by section: `flock`, which the host's 1.37.0 lacks, is shimmed only in `n` and `t` and called on the host at `:2345` and `:6765`**. **Scripts run whole in `bwrap` sandboxes from section `b` on** (16 sections before `y` invoke it; 60 invocation lines in the file, 85 lines carrying the word; `sa_run` at `:9010` -- `--tmpfs /`, `--ro-bind /usr`, `/etc`, the fixture's `/storage`, `/cloud`, `/ctl`, `/repo`, `/var/log`, `/var/run` -- is called 150 times, so a run opens more than 200 sandboxes); **`sa_run` has no `--unshare-net`**, so the host network is reachable from every script it runs (T14's S2 found the same shape in the four tools this file calls), while four other invocations do unshare it (`:6108`, `:11890`, `:12285`, `:12303`) and `:12312` skips without the namespace. The file **calls four of T14's
tools**: `rasteratops-cloud-layout-test` at `:14188` (and `--cloud-layout`
execs it at `:252`), `settings-modes-test` at `:14224` and
`melonds-upgrade-test` at `:14231` -- **both with `--busybox "${BB_HOST}"`,
the run's own copy of whatever busybox it resolved**, which T14's S8 now
refuses unless told its provenance -- and `wait-lock-test` is named only in
a comment (`:148`, `:8608`: the lifting pattern it shares). The sandbox helpers (`sa_new`, `sa_script`, `sa_run`, `sa_tail`, `sa_outcome`) are `:8993-9029`. It embeds Python (`:5244-5252`: the connections fixture's `configure`, a shim rclone that prints an auth URL and sleeps). Eight `|| true` sites (`:400` the fallback;
`:10409`, `:13871`, `:13908` counts and greps; the rest in comments or
guarded).

**Who runs it:** `tools/vm-qa`'s `scripts` suite (`vm-qa:158`: through a
`python3 -c` wrapper that resets SIGINT and SIGPIPE before exec, PL-025 of
the fix round's audit), on every default run -- **13 of a default run's 33
minutes** (T12's Q5 table) -- and the release procedure's step 3 through
`vm-qa`; by hand with `--old` against a `BASE_REF` for its failing controls (**the header lists twelve recipes, `:167-226`: the default `1d1503180d` and `53f390b1e9`, `c15050c897`, `8707919349`, `34aca64afd`, `0f7785e6ed`, `d79281066c`, `cee1656c33`, `28a80357ed`, `3387cf5da0`, `655f103cc5`, `70b6c70ca7`**). **Its record:** `docs/vm-qa-log.md` names `last-good-scripts-test` in 8 lines (61 carry the word `scripts`); the last PASS in a `vm-qa` report is **2026-10-06, qa-18 (started 01:04, finished 01:37 UTC), under the image's BusyBox 1.36.1 from a build root** (#1015's comment; `docs/qa-logs/2026-10-06-pixelelated-replacement-14/qa-18/counts.json` says `scripts_pass_lines: 1719`, which counts lines carrying the word PASS -- 1,721 by grep -- while that log's `    PASS  ` check lines number 1,374, so the figure is not a check count); every run since from an M6 worktree resolved the host's 1.37.0 and FAILed 319 checks at every scratch outside the worktree (326 under the worktree's own; T12's three `TMPDIR` runs, #1015; T14's run, 323 FAIL with two of S2's and two of S8's). **Blindspot 34** (*a check written for the device,
proven only under the host's tools*, 2026-09-10) is this file's founding
lesson: `tr -d '[:print:][:space:]'` under GNU tr vs busybox tr; the file
runs `sed mv cp tr head wc cut awk` through the image's busybox for that
reason, and its own fallback to the host's busybox is the lesson undone.

**The coordinator's two runs at the hash (2026-10-24, 23:4x-00:0x UTC, from an export of `8ebaf8daad` under `/workspace/tmp/m6-coordinator/t15-hash/`, each started with `setsid -w` from a shell whose SIGINT was at its default -- the runs' first line reads `SIGINT ignored=0`; `setsid` itself resets nothing -- and `TMPDIR` under the export):**

| busybox | source | rc | wall | PASS | FAIL | SKIP | FAILs by section |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| the image's, v1.36.1 | `QA_SYSTEM_ROOT` = the `069fc2704421` root (`m7-signin-build-20261022-07`), read only | 1 | 514 s | 1,303 | 10 (the export's, see below; the tree's is 0) | 0 | `x` 5, `y` 5 (all history reads) |
| the host's, v1.37.0 (Ubuntu) | the fallback at `:400` | 1 | 671 s | 984 | 329 | 0 | `y` 185, `t` 42, `x` 38, `z` 36, `k` 11, `n` 7, `af` 6, `ad` 4 |

The suite counted 1,313 checks in both runs; **319 checks FAIL under the host's busybox and PASS under the image's** (`diff` of the two runs' verdict lines) -- #1015's count exactly, so the host-busybox run judges the host, not the tree, and 61 of its lines read `flock: applet not found`. **Ten checks FAILed under the image's busybox in the coordinator's run, and they were the coordinator's export's, not the tree's** (corrected 2026-10-25 00:3x after the lane's stage A): the export was a fresh `git init` with one commit and no history, and the `F1.`, `F1r.` and `C.` fixtures read earlier builds' files from git (`f1_tree_at`, `:3274`; `:4271`'s `git show 417dcd8610:...`), silently, so each came up empty and the suite's own vacuous-fixture detectors fired ten checks later (*the fixture proves nothing* / *the take-back boot's journal: ''* / *the downgrade wrote 0 file(s)*). **The lane's run from the worktree, with the history present, is the tree's figure: 1,313 PASS / 0 FAIL / 0 SKIP, rc 0, in 517 s.** The read that fails open -- an `exit 2` inside a pipeline's subshell and a `2>/dev/null` read -- is a stage-D `bug` of this file (the coordinator's ruling on #662, 00:3x); the detectors stay as the second guard. Section `ae`'s historical migration matrix reads NOT APPLICABLE (the engine retired by #508; its archive contracts still run). Checks per section (the image run): `y` 448, `x` 350, `z` 92, `t` 80, `p` 38, `k` 25, `ab` 24, `m` 23, the rest under 20 -- `y` and `x` are 61 % of the suite. These are the numbers § 7 expects the lane's stage-A runs to reproduce within the drift of its branch.

**What this slice does not touch:** the scripts the file proves (the OS and
cloud scripts under `projects/ROCKNIX/packages/`; a defect in one of them
found here is a `bug` for its owning lane with the file's check as the
evidence, never a fix here); T14's four tools (read from their branch;
their fixes merge before this slice's); `tools/vm-qa` (T12's; the `scripts`
row's words are a lead); the two M7 build roots (read).

## 3. Read first

1. `next:AGENTS.md`; the every-session rules; **`engineering-practices.md`
   § Guards must fail closed** (the whole section: *a check that cannot run
   has not passed*; the pipeline's status; the `ls A B` case; *success
   reported over a no-op*; *a suite is not wired in until it has been seen to
   FAIL once*) and **`upgrade-and-install.md` § Verify on a device, not on
   the host** (blindspot 34: *and under the device's tools, not the host's*)
   -- the two rules this file exists to serve.
2. `docs/reviews/plan-for-the-plan.md` whole; `docs/reviews/order.md` § T15
   and § T14; this brief whole.
3. The live M6 body; #662 (with its comments; its session pointer is seeded by the dispatch and absent before it); #903 (the epic, its futro
   comment and the T15 addendum: U-1 to U-6 and A1 to A7); #339; #346 (the
   maintainer's channel: what is open there is not this lane's to decide);
   **#1015** (T12's bug: the 319 FAILs, the busybox lead, the three `TMPDIR`
   runs); **#997** (T14's writer-test contract and the two-line change this
   slice makes); **#999** (the fixture's `--config` placement, fixed by T14
   for this file's shims); **#661** (T14 accepted: its `02` § The suites at
   the fixed tip ran this file once, rc 1, 990 PASS / 323 FAIL, under the
   host's busybox; its retro's brittleness after-column); **#659** (T12
   accepted: the `scripts` row, cycle 1's FAIL (1) 675 s); #657 (T10's retro:
   the five fail-open shapes); #105, #151, #272, #307, #308, #163, #176,
   #188, #189, #191, #196, #199, #209, #350, #353, #363, #365, #383, #401,
   #421, #526 (the sections' own issues, as the header names them); #640 (the
   legacy paths); #962 (the credential-shaped fixture literal at `:8004`).
4. The file itself, in this order: the header (`:1-258`), the harness (`:259-430`), one small section whole (`a`, `:429-517`), the first sandboxed section (`b`, `:518-606`), the sandbox helpers (`:8993-9029`), one of stream A's cases under `y` (from `:8906`),
   the four call sites and the verdict (`:14177-14238`); then every section
   for Q6's table.
5. `docs/qa-logs/2026-10-06-pixelelated-replacement-14/qa-18/defaults/scripts.log` (the last PASS, under the image's busybox: its banner line names the source; `qa-18/counts.json` beside it) beside T12's `git show d9991735d8:docs/audits/2026_10_24-epic-m6-tooling-vm-harness/streams/scripts-tmpdir-compare.txt` (on `feature/m6-tooling-vm-harness-659` only until its merge) and T14's `02` § The suites at the fixed tip (`git show 7c1d729b57:docs/audits/2026_10_24-epic-m6-tooling-state-tests/02-forward-audit.md`; the FAILs under the host's).

## 4. The questions

The seven renovation questions of plan § 4, with **brittleness** as the
lens (what the suite depends on that is not the thing it proves; what
happens when each is absent; what it caught; who runs it; its positives):

- **Q1 Modernize:** host paths and roots the file assumes
  (`${ROOT}/../*/build.*`, `rocknix.worktrees`, `/tmp`, `HOME`); the
  busybox applet list (`sed mv cp tr head wc cut awk stat chmod cat`) against
  what the scripts call (`flock`, which the host's 1.37.0 lacks and the
  image's has, is not in the list: is it shimmed, or does a sandboxed script
  reach the host's?); `BASE_REF` defaults and the `--old` recipes' commits.
- **Q2 Standards:** fail-open shapes by name -- the `|| true` fallback at
  `:400`; `set -u` without `-e`/`pipefail` in a 14,000-line script (which
  pipelines' first stages can fail silently); `check $?` after a compound
  `[ ] && [ ] && grep` (the last command's status: T10's rule); counts
  compared where sets were meant; a `grep -c` that reads 0 as "nothing
  differs"; the sandbox's host network; the SIGINT refusal; the embedded
  Python's imports.
- **Q3 Bugs -- the pass-without-proving hunt, per section:** which checks
  pass under the host's busybox that would fail under the image's, and the
  reverse (the 319 FAILs of #1015 sorted into *the host's applets* vs *the
  tree*); which checks pass against an empty or absent script (the `src_of`
  exit 2 guards that against the whole file, but a case's own `grep -q` on a
  missing fixture?); which `--old` recipes still fail as the header promises
  (each `BASE_REF` recipe run once: a historical control that now passes is
  a control that has stopped controlling); the `skip()` paths (what makes a
  SKIP, and does a SKIP ever hide a FAIL); the four call sites' contracts
  against T14's fixed tools (`--busybox "${BB_HOST}"` refused by #997's
  contract; the `--config` order #999 fixed).
- **Q4 Package currency:** none (no package); the rclone the sandboxes bind
  (`/sa/rclone.real`) and its version against the recipe's pin (1.75.2),
  since T14's two cloud tests hard-coded 1.75.1 and refused the package's
  own.
- **Q5 Efficiency:** the suite's minutes by section (13 minutes in `vm-qa`;
  which sections carry them -- `y`'s 85 sandboxes?), what the host holds,
  whether the sandboxed sections could run beside the guest suites (T12's
  #987 lead), and the cost of a run that resolves the wrong busybox (13
  minutes to a verdict that judged the host).
- **Q6 Dead ends -- the brittleness table:** one row per section (34), each
  with (a) what it depends on that is not the thing it proves -- the busybox
  source, a build root's presence, the host's rclone, `bwrap`, the network,
  a fixture's bytes, `BASE_REF`'s reachability -- and what happens when each
  is absent (a FAIL, a SKIP, a silent PASS, an exit 2); (b) its last recorded
  catch (the issue or blindspot the header names; `nothing recorded` when
  the record shows none); (c) its caller (`vm-qa`'s `scripts` suite for all;
  `--cloud-layout` for `ae`; the `--old` recipes); (d) its positive (a
  `BASE_REF` recipe that FAILs, a constructed input, or `none`). Then the
  file's split as a Q7 finding, invited by the order: a 14,238-line file whose sections `y` (5,386 lines: stream B's `y1` to `y4` and stream A's cases) and `z` (541) are audit streams' cases pasted in -- what a split by section would cost (the shared harness, the
  shared sandbox helpers, the one busybox copy) and gain.
- **Q7 Clarity and structure:** the header's 34 claims against the code
  (each section's `echo` line against what its checks assert); the three
  descriptions (`--help`, the rule that names it --
  `generic-x64-vm-testing.md` and `vm-qa`'s header row -- and the index row
  in `instruction-files.md`) against the code; the split proposal.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`), a run with its exit, a recorded report
   (`docs/qa-logs/`), or a `BASE_REF` recipe's own output.
2. Mechanical evidence outranks reading: a section's behaviour is its run
   and its exit, not the header's claim above it.
3. **The bench is the host.** No guest: every section runs in a `bwrap`
   sandbox or against temp paths on the build host; nothing here needs a
   device, a provider, a QA account or a GENERIC_X64 guest. **Can this be
   done on the VM? Yes -- on the host, which is where the suite runs by
   design; the one thing the host lacks (a build root's busybox) is read
   from an M7 root through `QA_SYSTEM_ROOT`, a read of one file the suite
   copies.** A run that resolved the host's busybox is a run that judged
   the host, and is said so in `02` (blindspot 34) -- the two runs below are
   kept apart by that fact.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.

**The runs, with what the coordinator read on 2026-10-24** (the lane runs
each at stage A in its worktree and records the exit, the wall time, the
banner line naming the busybox, and the PASS/FAIL/SKIP counts; a run is started **with SIGINT at its default** (`:260-268`: a shell background job inherits SIGINT ignored and the suite refuses, exit 2; **`setsid` does not reset an ignored SIGINT -- the stranger tested `-w` and `-f` with it ignored in the parent and both children kept the bit, and the file's own comment at `:264` naming `setsid -f` is wrong on that point** -- so a run that cannot be foreground is started as `vm-qa:158` starts it: `python3 -c 'import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); signal.signal(signal.SIGPIPE, signal.SIG_DFL); os.execv(sys.argv[1], sys.argv[1:])' tools/last-good-scripts-test`, and the run's first output line, `signals: SigIgn=... SIGINT ignored=0`, is quoted);
`TMPDIR` under `/workspace/tmp/m6-t15/`, never `/tmp` and never a path
under the worktree (T12's seven `AF_UNIX path too long`, #659 S5b):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-last-good-test-662
cd "$D"; export TMPDIR=/workspace/tmp/m6-t15/tmp; mkdir -p "$TMPDIR" .qa-scratch/t15
R7=/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/build.pixelelated-GENERIC_X64.x86_64/image/system   # the 069fc2704421 image's root, read only
"$R7/usr/bin/busybox" | head -1; sed -n 's/^BUILD_ID=//p' "$R7/../../etc/os-release" 2>/dev/null || sed -n 's/^BUILD_ID=//p' "$R7/etc/os-release"   # BusyBox v1.36.1; 069fc2704421...
SIGDFL='import os, signal, sys; signal.signal(signal.SIGINT, signal.SIG_DFL); signal.signal(signal.SIGPIPE, signal.SIG_DFL); os.execv(sys.argv[1], sys.argv[1:])'   # vm-qa:158's launcher: SIGINT and SIGPIPE at default, then exec
# run 1: the image's busybox (the suite's design); the coordinator's run at the hash: 1,303 PASS / 10 FAIL / 0 SKIP in 514 s (§ 2)
s=$(date +%s); QA_SYSTEM_ROOT="$R7" python3 -c "$SIGDFL" tools/last-good-scripts-test > .qa-scratch/t15/run-image.out 2>&1; echo "image rc=$? $(( $(date +%s) - s ))s $(tail -1 .qa-scratch/t15/run-image.out | cut -c1-80)"; grep -m1 'a copy of' .qa-scratch/t15/run-image.out | cut -c1-160
# run 2: the host's busybox (the fallback every M6 worktree takes); the coordinator's run at the hash: 984 / 329 / 0 in 671 s (§ 2)
s=$(date +%s); python3 -c "$SIGDFL" tools/last-good-scripts-test > .qa-scratch/t15/run-host.out 2>&1; echo "host rc=$? $(( $(date +%s) - s ))s $(tail -1 .qa-scratch/t15/run-host.out | cut -c1-80)"; grep -m1 -E 'a copy of|busybox' .qa-scratch/t15/run-host.out | cut -c1-160
grep -c '    PASS  ' .qa-scratch/t15/run-image.out; grep -c '    FAIL  ' .qa-scratch/t15/run-image.out; grep -c '    SKIP  ' .qa-scratch/t15/run-image.out
grep -c '    PASS  ' .qa-scratch/t15/run-host.out;  grep -c '    FAIL  ' .qa-scratch/t15/run-host.out;  grep -c '    SKIP  ' .qa-scratch/t15/run-host.out
diff <(grep -E '^    (PASS|FAIL)' .qa-scratch/t15/run-image.out | sed 's/^    //') <(grep -E '^    (PASS|FAIL)' .qa-scratch/t15/run-host.out | sed 's/^    //') | grep -c '^[<>]'   # the checks whose verdict depends on the busybox: Q3's first list
# the twelve --old recipes the header promises FAIL (:167-226): each once, with the image's busybox; a recipe that passes is a finding
for ref in 1d1503180d 53f390b1e9 c15050c897 8707919349 34aca64afd 0f7785e6ed d79281066c cee1656c33 28a80357ed 3387cf5da0 655f103cc5 70b6c70ca7; do s=$(date +%s); QA_SYSTEM_ROOT="$R7" BASE_REF=$ref python3 -c "$SIGDFL" tools/last-good-scripts-test --old > ".qa-scratch/t15/old-$ref.out" 2>&1; echo "--old $ref rc=$? $(( $(date +%s) - s ))s FAIL=$(grep -c '    FAIL  ' ".qa-scratch/t15/old-$ref.out")"; done
tools/last-good-scripts-test --help | head -3; tools/last-good-scripts-test --nosuch; echo "rc=$?"   # 0 and 2
grep -n '|| true' tools/last-good-scripts-test | cut -c1-120                                            # the eight
grep -n -E '^set -|pipefail' tools/last-good-scripts-test | head                                        # set -u only
grep -c -E '^\s*check ' tools/last-good-scripts-test                                                    # 120 call sites
grep -n -E 'flock' tools/last-good-scripts-test | head -5                                               # the applet the host lacks: shimmed, or reached?
grep -n -E '/tmp/|rocknix\.worktrees|/workspace/repos/rocknix|HOME' tools/last-good-scripts-test | cut -c1-120 | head -30   # Q1
```

**The reading, per section:** Q6's row (dependencies, absence effects, last
catch, caller, positive), from the section's own checks and the record;
every section whose verdict differed between the two runs is read for *which applet* made the difference (the coordinator's diff: 319 checks, § 2); the ten that FAIL under the image's busybox too (`x` 5, `y` 5, all *the fixture proves nothing* / an empty journal) are sorted into the tree's and the fixture's first; `y` and `z` read as what they are (the
two audits' punch items as cases) with their item ids mapped to the
original issues; the four call sites read against T14's fixed tools (`git
show 7c1d729b57:tools/settings-modes-test`, etc.) for what the contract now
requires of this file.

**The seat (Phase 4.6, one seat):** `npm install --prefix tools/council`,
`tools/council/run verify-pins`, `tools/council/run test`; the packet
(`gpt-brief.md`: the harness, the helpers, the index, the call sites, the
verdict and Q3's suspect sections whole, with `packet-manifest.json`
carrying the sha256 of the whole file and of each excerpt by line range)
**scanned before it is sent** (`tools/forbidden-terms-check --stdin` 0
hits; the pre-commit's patterns 0 lines -- `:8004` is the known one, #962;
a hit redacts as PL-012 says and is recorded); the probe (`gpt-probe.md`
with its `.provenance.json`); the refutation (`gpt-audit.md` with its
`.provenance.json`), the seat asked first for the busybox fallback and its
banner, the sandbox's network, the `check $?` after compound tests, the
`--old` controls' standing, and the file's split; each item graded in `04`
§ Second opinion with the artifact that decided it; a seat cut by its
ceiling re-runs on a trimmed packet (D-WORKFLOW-195). The call runs plainly
with a harness waiter.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#662`
(`Refs #662`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-last-good-test/00-running-log.md` | the flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, the host file's last line and the live census at stage A, the two runs with their banners, exits, wall times and counts, every `--old` recipe's exit, every later command with its exit | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the one path re-derived with § 2's block and its output, the provenance (408 fork commits, none upstream), the branch's diff from the hash (empty), the 34 sections by line; § Who runs it; § The record (the last PASS and the FAILs since, by busybox) | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #662's checklist, plus **a coverage table with one row per section under its own `## Coverage` heading** (34; the first cell the section's letter and its first line number), § The runs (the two runs and the twelve `--old` recipes, each with *a FAIL would mean ...*), § The checks that depend on the busybox (the diff of the two runs' verdict lines, sorted by applet), § Proofs with `proved:` cells | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: this file x `vm-qa`'s `scripts` suite x the four T14 tools x the scripts it proves x the busybox source | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5), § Second opinion (4.6), **§ Renovation face** Q1 to Q7, **Q6 carrying the brittleness table** (34 rows) and **the split proposal**, § Instruction File Recommendations | B, C |
| Second opinions | `.../second-opinions/` | `review-plan.json` (independent; `gpt` at `max`), the brief, `packet-manifest.json`, the probe prompt, the probe and the refutation with their `.provenance.json`, the packet's scan result | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` with `review plan: independent, 2 model perspectives, 1 verified external calls` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where (file:line at the hash), acceptance, `Already written:` and the VM line; the YAML `punch_index`; generated from one list | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #662 | `Audit: M6 T15 the last-good scripts test -- N findings (...)`; one checkbox per item, agent-first | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect in this file, with its code trace, `Already written:`, the VM line and the case that will prove the fix; a defect in a script the file proves is a `bug` for that script's lane, named so; no bug body quotes a credential-shaped value | D |
| Streams | the coordinator's brief `docs/reviews/briefs/t15-streams.md` | one per fix the coordinator briefs at the stage-D pause; **S1 is #997's two lines (`--busybox-from`/`--unverified-busybox` at `:14224`, `:14231`) and the fallback's refusal or marking (#1015's fix)**, whatever else the audit finds | E |
| Retro | `docs/retros/<date>-m6-tooling-last-good-test.md`, posted on #662 | the mini-retro, Instruction-Recommendations mode; what the slice did to the two time-to-play numbers (nothing); what each stream did to the suite's refusals; the brittleness after-column | G |

## 7. Acceptance

The checklist on #662 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #662 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-tooling-last-good-test/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-tooling-last-good-test/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`).
- [ ] `second-opinions/review-plan.json` records `depth: independent`, one reviewer (`gpt`, `openai/gpt-6-astra`, `max`), and the probe and refutation outputs have a `.provenance.json` beside them whose served model, effort and provider are those; `packet-manifest.json` records the scan of the packet (0 listed-word hits; the `:8004` literal's disposition named).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#640 for a legacy path; a `bug` for a defect in a script this file proves, for that script's lane; the coordinator's lead for a rule or a `vm-qa` row), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes: `git diff --stat 8ebaf8daad <reviewed-at> -- tools/last-good-scripts-test` empty).
- [ ] `01-research-notes.md` § Scope records the read hash, § 2's inventory block with its output (1 path, 14,238 lines, 1,167,697 bytes, fork-own, shell, `n/a`), the 408 fork commits (`git log --oneline 8ebaf8daad -- tools/last-good-scripts-test | wc -l`) and the 34 sections with their first line numbers (`grep -n -E '^echo "  [a-z]{1,2}\. '`).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per section under its own `## Coverage` heading, the section's letter in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `[a-z]{1,2}`'`` prints `34`.
- [ ] `02-forward-audit.md` § The runs records both stage-A runs (`QA_SYSTEM_ROOT` set to a named M7 root's `image/system`, and unset) with command, exit, wall time, the banner line naming the busybox and its source, the PASS/FAIL/SKIP counts, and each with *a FAIL would mean ...*; and § The checks that depend on the busybox lists every check whose verdict differed between the two runs, each with the applet named (`flock` among them if the diff shows it).
- [ ] `02-forward-audit.md` § The runs records each of the twelve `--old` recipes of the header (`:167-226`: `1d1503180d`, `53f390b1e9`, `c15050c897`, `8707919349`, `34aca64afd`, `0f7785e6ed`, `d79281066c`, `cee1656c33`, `28a80357ed`, `3387cf5da0`, `655f103cc5`, `70b6c70ca7`) run once under the image's busybox with its exit and FAIL count, and names any recipe whose promised FAILs did not fire (a control that stopped controlling is a finding).
- [ ] `00-running-log.md` shows no handheld action, no real provider or real account touched, no guest, no build, no edit to a script this file proves, no edit to T14's four tools, no write under `/workspace/repos/rocknix*` or `/tmp`, and every suite run started with SIGINT at its default (each run's first output line `signals: SigIgn=... SIGINT ignored=0` quoted).
- [ ] `04-analysis.md` § Renovation face Q6 carries the brittleness table: one row per section (34), each with (a) its dependencies that are not the thing it proves and what happens when each is absent, (b) its last recorded catch or `nothing recorded`, (c) its caller, (d) its positive or `none`; and § Q6 carries the split proposal with what a split by section would cost and gain, as a lead for the coordinator.
- [ ] `04-analysis.md` § Q3 hunts the pass-without-proving shape through every section by letter, each with the line read and a constructed input that would pass wrongly or the statement that none can; the eight `|| true` sites, every `check $?` after a compound test, the `skip()` paths, **the `NOT APPLICABLE` outcome that exits 0 (`:4558`, `:14235`)**, and **the no-busybox case that runs on the host's GNU tools with no banner line** each dispositioned by line; the ten checks that FAIL at the hash under the image's busybox (§ 2) each sorted into the tree's (a `bug` for its script's lane) or the fixture's (a finding here).
- [ ] `04-analysis.md` § Q7 reads the header's 34 claims against the code (each `echo` line against its checks), the three descriptions (`--help`, `generic-x64-vm-testing.md`'s and `vm-qa`'s words, the index row) against the code, with each drift named as a lead; a rule or index row is never edited here.
- [ ] `04-analysis.md` § Q5 carries the suite's wall time by section from the stage-A runs (the section `echo` lines' timestamps, or `date` lines the lane adds to its own copy of the output), names which sections carry the 13 minutes, and what a run that resolved the wrong busybox costs.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fix-tree`, `fix-case` (a fix proved by a new or re-run case that failed on the unfixed file and passes on the fixed one, both quoted) or `design`; every cell is one of those six words.
- [ ] Every punch item carries `question:`; every `bug` this lane files passes `tools/box-check --issue N`; no file under `tools/` is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <stage-D tip> -- tools/` empty); `tools/last-good-scripts-test` at the fixed tip calls T14's two writer tests with `--busybox-from <BUILD_ID>` when `QA_SYSTEM_ROOT` or a build root supplied the busybox and `--unverified-busybox` when the host did (`grep -n -E 'busybox-from|unverified-busybox' tools/last-good-scripts-test` prints both call sites).
- [ ] At the fixed tip, a run from a worktree with no build root and no `QA_SYSTEM_ROOT` **does not pass as the image's**: it refuses (exit 2, naming what it lacks) or marks every line and exits 3 as T14's S8 does -- the run's output quoted; and a run with `QA_SYSTEM_ROOT` set to a named M7 root passes or fails on the tree (its verdict line and counts quoted, the FAILs each a `bug` for its script's lane or a fixed check here).
- [ ] The retro exists at `docs/retros/<date>-m6-tooling-last-good-test.md`, is posted on #662, and says what the slice did to the two time-to-play numbers (nothing) and, per stream, what it did to the suite's refusals; the brittleness after-column.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge); `tools/vm-qa --skip-up --only scripts` is not run here (it needs a guest), but the fixed file's exit codes are read by `vm-qa:148`'s rule (0 PASS, 3 SKIP, else FAIL) and stated in `02`.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #662; a blocker named on #662 with what is needed (the seat failed, a
run that cannot start for a reason outside the tree, the M7 roots gone);
a branch that differs from `8ebaf8daad` on the file at stage A; or an
execution limit, stated as such with the running log current. A checkpoint
is not a stop; a differing count is a delta; `next` moving is drift. An
idle session says it is idle on #662, **and does not end a turn on a post
that asks nothing**, and **updates its session pointer at every checkpoint**
(#1014: two lanes' pointers lagged twelve and thirteen streams tonight).

**What never runs in this slice:** a handheld action of any kind
(D-QA-015); a cloud test against a real provider or a real account (the
sandboxes' shim rclone and local fixtures only); any read of a credential
file (`~/.config/council/env`, `~/.ROCKNIX/options`,
`~/.config/rocknix/forbidden-terms`, a real `rclone.conf`); a push to any
branch but the lane's own; a guest of any kind (nothing here needs one); a
build; `fork-worktree sync|remove|repair`; an edit to a script this file
proves (a `bug` for its lane), to T14's four tools (their fixes are on
`feature/m6-tooling-state-tests-661`), to `tools/vm-qa` (T12's), to a rule,
`CLAUDE.md`, `AGENTS.md`, a decided register row or
`.github/sessions/saved-session-state-next.md`; a write under
`/workspace/repos/rocknix*` (the M7 roots are read: `QA_SYSTEM_ROOT`
copies one file out) or `/tmp` (use `/workspace/tmp/m6-t15/`); a suite run started with SIGINT ignored (`cmd &` in a non-interactive shell: the suite refuses, exit 2; `setsid` does not reset it -- a run that cannot be foreground is started through `vm-qa:158`'s `python3 -c` launcher that sets SIGINT and SIGPIPE to default and execs); a credential-shaped
literal written anywhere (a fixture is built at run time); `--no-verify`;
bare `git stash`; `git worktree remove --force` or `rm -rf` on a worktree;
`rm -rf` on a bare variable path (`"${X:?}"`, or a literal).

## 9. Ceremonies owed

- A work-log entry per session headed `#662`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #662` or the
  guard.
- The VM question written before any proof (§ 5: the host is the bench; no
  guest; the M7 root read through `QA_SYSTEM_ROOT`).
- The mini-retro at stage G, posted on #662, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 at 23:5x the highest Decided rows are D-WORKFLOW-205, D-QA-062
  and D-INFRA-031, the coordinator's); it goes at the end of `## Decided`,
  and a row is never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next` into
  this branch, never between stage A and stage D; the coordinator merges its
  own branch into this one at hand-back before the last criterion's checkers
  run (as for T9, T10, T12 and T14); T14's branch merges before this one, so
  the four tools this file calls are T14's fixed ones on `next` by then --
  until the merge, read them from `7c1d729b57`; a merge with conflicts is
  checked for leftover markers before it is committed (#696), and the
  ledgers are united by whole entries.
- Commit messages `docs: ...` for the audit, `last-good-scripts-test: ...`
  for a stream's fix, each with `Refs #662` and the attribution line; `git
  add -A` only after `git status --short` shows nothing a run left behind
  (`.qa-scratch/` is gitignored; the suite's temp root is under
  `/workspace/tmp/m6-t15/`, and a run that leaves bytes in the tree is a Q2
  finding).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#662's checkboxes against their artifacts; the lint's `PASS` line; the
seat's `review-plan.json` and provenance and the packet's recorded scan; the
audit issue's checkboxes all at an outcome (the ticked and open counts read
by name); the coverage table's row count (34) and the brittleness table's
rows against § 7; **re-running on an export of the tip under
`/workspace/tmp`: the inventory block, the file's line and byte counts at
the hash, the diff of the file against the dispatch tip (every hunk a
stream's), `--help` rc 0 and `--nosuch` rc 2, the two call sites' flags, one
run of the fixed suite with `QA_SYSTEM_ROOT` set to the `069fc2704421` root
(its verdict, counts and banner) and one with it unset from a tree with no
build root (the refusal or the marked exit 3), each started with SIGINT at its default;** `register-check` and `rules-check` on a simulated merge with the
coordinator's tip (the ledgers united); the retro's answers; the exit codes.
The lane posts one hand-back comment naming the tip and each artifact by
path, writes `reviewed-at:` and `fixed-at:` into #662's body, then says it
is idle. After acceptance the coordinator closes the audit issue, prompts
the lane for `audit-completion.json` and the full lint, merges the branch
in its turn after the M7 candidate (after T14's, before T4's), regenerates
the ledgers, and closes #662 when every row is proven.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#903) carries this slice's kickoff addendum, and a stranger's proof of
this brief is run by a reader with no context before dispatch; version 2
records what each found.
