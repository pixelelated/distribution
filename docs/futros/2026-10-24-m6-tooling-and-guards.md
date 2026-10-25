# Futro: the tooling-and-guards area epic (#903), at T9's kickoff (#656)

**Prepared:** 2026-10-24, by the M6 coordinator lane (D-WORKFLOW-189),
before T9's brief is written and before its dispatch; the epic #903 is filed
with it. **Inputs read, not recalled:** `docs/reviews/order.md` § T9, T10,
T12, T14, T15 and T45 on P1's `2174265e9c`; `slices.json` k 9 and the five
beside it; P1's inventory (the area: 194 rows, 66,258 lines; 192 fork-own,
2 upstream-carried; reach `n/a` 194); #644 (the build-path read); the retros
of T5, T6 and T8 on their branches (their *Adjustments for the next lane*);
the register rows D-WORKFLOW-141, 142, 143, 148 and D-INFRA-015, 018, 021,
022, 023; blindspot 73 and the guard-class entries 8, 14, 22, 26, 42; the
eighteen T9 files at `8ebaf8daad` with their headers, tests and guides; and
the host's own state, read this afternoon. Every figure below was produced by
a command on the tree at `8ebaf8daad`, on an export of it under
`/workspace/tmp/m6-coordinator/t9-hash/`, or on the host, and says which.

## 1. What do we know and what are we assuming?

**The plan, in the order's words:** T9 is *build supervision and host
maintenance*, id `tooling-build-supervision`, kind read, lens brittleness,
depth **Independent** (*an ordinary code slice*), interacting with the build
engine (T5, accepted). Its paths are
`tools/{watch-*,host-maintenance/**,build-preflight,fork-newdrive,fork-publish-release}`:
**18 paths, 3,795 lines** (`git ls-tree -r --name-only 8ebaf8daad tools |
grep -E ...` then `wc -l` per file, summed: 18 and 3,795, the order's own
figures), **12 Python, 3 bash, 3 Markdown** by shebang and suffix. The six
slices of the area are T9 (18 paths), T10 (31, Extended: the secret and
wordlist guards), T12 (60, the VM harness), T14 (32, the state tests), T15
(1 path of 14,238 lines, `tools/last-good-scripts-test`) and T45 (52, the
council toolchain, Local). T9 goes first because the build process is the
maintainer's weight (D-WORKFLOW-186) and these are the tools every build
enters.

**Assumptions the plan leans on and does not state:**

- **Every file is the fork's own and absent upstream.** Verified: `git
  cat-file -e upstream/next:<path>` fails for all 18. So there is no base
  merge to defer to, no bump to propose, no #585 row by default; every defect
  is ours.
- **The tools' behaviour is what their tests say, and the tests run.** On a
  bare export of the hash (no `.git`), the four `tools/host-maintenance/test-*`
  pass: `test-swap-reclaim` (`Ran 37 tests`, rc 0), `test-retention-report`
  (rc 0, 7 s), `test-build-admission` (rc 0, 18 s), `test-build-monitor` (rc 0,
  64 s: it runs the real entrypoint prefixes and the Makefile with isolated
  payloads). Of the four controls under `docs/qa-logs/`, two take an argument and one an option:
  `2026-10-03-watch-job/test-watch-job.py <watcher> [--baseline]`,
  `2026-10-04-watch-progress/test-progress.py <root>`,
  `2026-10-04-watch-progress/test-watch-build.py [--root ROOT]`,
  `2026-10-05-watch-submit/test-submit.py`; **three fail at the hash in any checkout** (`test-watch-build.py`,
  `test-progress.py`, `test-submit.py`): their fixtures copy `watch-build`
  and `watch-job` but not `build-admission`, which `watch-build:50-51` loads
  beside itself -- the stranger's proof read the cause from the receipts
  `test-submit.py` leaves; U-1 below is answered, and the answer is a
  finding.
- **The fork CI runs three of them**, `fork-checks.yml:42-44`:
  `test-watch-job.py tools/watch-job`, `test-build-monitor`,
  `test-build-admission`. "CI green" is a claim about those three only; the
  swap helper's and the retention report's tests, and the two qa-logs
  controls that take arguments, run nowhere but by hand.
- **The host is the substrate, and it is shared.** Read today on serval:
  `/usr/local/sbin/pixelelated-reclaim-swap` is installed (root, 0755);
  `/etc/sudoers.d/zz-pixelelated-reclaim-swap` is present beside
  `zz-fleet-hardening`; `sudo -n -l` lists the narrow grant
  (the helper's `--reclaim` alone, as root, without a password and with
  `NOSETENV`) **and, above it, the fleet's `(ALL : ALL) ALL` for `max`** --
  so the README's *"the sole added permission"* is true as *added* and the
  helper's boundary is the modes and ownership it checks, not the absence
  of other sudo; `/swap.img` is 8 GiB with **8 GiB used** (the cushion the
  preflight exists to see is gone right now; the next build is M7's, and so
  is the reclamation, D-INFRA-015); Docker 29.8.2; `.build-runs/` exists in
  45 M7 worktrees and the legacy checkout (2,022 run ids), read-only --
  version 1 said three, an `ls | head -3`. The host's Python is 3.14; the
  container's is 3.10 (#492): these tools run on the host.
- **Nothing in this slice may act on the host.** No build, no `--reclaim-swap`,
  no `install`, no `--stop-vms`, no `fork-newdrive` (it formats a disk and
  moves the worktrees; it has no dry run), no `fork-publish-release` past
  `--prepare` (a plan, never a tag or a release). The tests run in the lane's
  own worktree, after the host file is read and the census recorded; a watcher
  they arm is theirs and ends with them.
- **The record is on the issues the 35 fork commits cite:** `git log
  c445081a59..8ebaf8daad -- <the 18>` is 35 commits, citing #383 (6), #410
  (3), #489, #471, #461, #409, #395, #394, #393, #344, #265 (2 each), #597,
  #565, #532 -- the watcher (#393 to #395), the swap helper (#410), the
  retention and admission work (#461, #489, #493 through #597), the release
  identity (#532, #565), the result-ownership incident (#597).
- **Two files carry the legacy host layout** (#640's class, D-INFRA-026):
  `tools/fork-newdrive:20-21` (`WT_DIR=/workspace/repos/rocknix.worktrees`,
  `MAIN=/workspace/repos/rocknix` as defaults) and `tools/watch-job:36` (a
  comment naming `/workspace/tmp/rocknix-session/<job>.status`). Recorded,
  #640 named, not changed by this slice.
- **The entry points are outside the slice and read-only context:**
  `Makefile:40` and `:179`, and `scripts/{build,build_distro,image,install,build_compat}`
  each `exec ./tools/watch-build --entry -- "$0" "$@"` -- T5's accepted files.

**Substrate preconditions, and how each was verified:** the installed helper
(`ls -la /usr/local/sbin/pixelelated-reclaim-swap`); the sudoers entry
(`ls /etc/sudoers.d/`, `sudo -n -l`); the swap (`swapon --show`); Docker
(`docker --version`); the `.build-runs/` convention (`ls -d
/workspace/repos/rocknix.worktrees/*/.build-runs`); the Makefile hooks (`grep
-n watch-build Makefile scripts/*`); the CI lines (`grep -n host-maintenance
.github/workflows/*.yml`). Unverified and left so: what the recorded M7 runs'
status files say (read by the lane, A4); whether the two qa-logs controls that
failed on the export pass in a checkout (U-1).

**Build-vs-adopt:** not applicable; the maintainer chose these tools over a
monitoring stack (D-INFRA-016 parks SkyWalking); a read confirms or questions
the brittleness of what exists, it does not re-decide the choice.

**Base divergence:** the coordinator's branch ends at D-WORKFLOW-199 in the
register; a lane may take 200 (T4 runs beside T9). Blindspot entries run to
76.

## 2. What known unknowns need investigation?

- **U-1** Do `test-watch-build.py` (2026-10-04) and `test-submit.py` pass at
  the hash in a real checkout? They failed on a bare export. The lane's stage
  A runs all eight controls in its worktree with the exact command and
  argument each needs and records the exit of each; a control that fails at
  the hash in a checkout is a finding with its traceback (brittleness is the
  lens), never a nuisance to work around.
- **U-2** What does `watch-build --docker` do with a host-only `TMPDIR`
  (#549)? Read, not run: the lane traces the environment the container gets.
- **U-3** Is `test-build-monitor` safe beside live lanes? It arms a watcher
  and runs the Makefile with an isolated payload in the worktree it runs
  from; the host file is read first, the census recorded, and the run is the
  lane's own. Proceeding on that basis; the brief says so.
- **U-4** Can `fork-publish-release` and `fork-newdrive` be exercised at
  all? `--prepare` emits a plan only and `tools/build-identity-test` (T14's
  file) is its synthetic control; `fork-newdrive` has no dry run and is read
  only. Proceeding: a read with the tests that exist, and a punch item where a
  mutating tool has no safe control.
- **U-5** Does one GPT packet hold the slice? 18 files, 3,795 lines, 201,453
  bytes (197 KiB) at the hash: yes. The seat is asked first for the sudo helper (`reclaim-swap`,
  `install`) and the admission guard (`build-admission`), where a second
  lab's eye matters most.
- **U-6** Is the swap state a finding? 8 GiB used of 8 GiB is the host's
  state, not the tools'; the preflight reports it by design. The observation
  goes on the host coordination file for the M7 lane, not into T9's punch
  list.

## 3. What patterns from prior work apply that we haven't named?

- **T5's retro:** *run the real script over fixture files when its tools can
  be borrowed read-only*; *before a guard fails closed, read what the
  recorded builds show it would meet*; *count shapes per branch, not per
  file*. Here: the admission guard's and the watcher's refusals are read
  against the recorded M7 runs (`.build-runs/<id>/`, read-only) for what each
  guard met in practice.
- **T6's retro:** *run a lint over the whole tree before quoting what it
  should print*; *a fixture resolves its scratch path first*. Here: the
  controls' baselines are run before the brief quotes them (done, above, on
  the export; the lane repeats in its checkout).
- **T8's retro:** *run a fork script once at stage B when it can run*;
  *count processes by `/proc/*/comm` with a prefix, and expect a pipeline's
  subshell*. Here: the tests are the run; the watcher's process observations
  are read against #506 (a sandbox's `/proc` hides host PIDs).
- **Blindspot 73** (the monitor observed package completion instead of build
  activity) is the area's own: the fix (`--activity-dir`, `--build-progress`,
  D-WORKFLOW-141) has controls under `docs/qa-logs/2026-10-04-watch-progress/`;
  the lane reads whether a regression of that fix would fail one of them.
- **Blindspots 8, 14, 22, 26** (a guard whose failure changes nothing; a hook
  never seen to fire; a probe that cannot report absence; a hooks path that
  runs nothing) are the class every tool here belongs to. The evidence floor
  is each guard's constructed positive, by file and test.
- **#597** (result files belong to their producer) and **#506**: the lane
  never writes under an M7 `.build-runs/`, and reads host processes from the
  host namespace or says it could not.

## 4. What could we be missing?

**Agent-execution simulation, a fresh lane with the brief:**

- It runs `test-build-monitor` in its worktree. *What if* the Makefile at the
  hash requires `PIXELELATED_BUILD_ADMISSION` and the test's synthetic
  admission does not satisfy the guard at that hash? The test passed on the
  export, so it does today; the lane records the admission it used. *What if*
  it leaves `.build-runs/` behind in the worktree? `.gitignore` is read for
  it before the first commit (A1 names the check).
- It runs `tools/build-preflight` (report-only) and reads *swap full*.
  *What if* it reaches for `--reclaim-swap`? The brief forbids it; the
  observation is the host file's (U-6).
- It reads `fork-newdrive`'s legacy defaults and *fixes* them. No: #640 owns
  the drift; recorded, not changed (A5), as T4 does with the rules.
- The GPT seat proposes a redesign of the watcher's stall logic. A stream
  changes only what a control proves, and the watcher's contract is a set of
  register rows (D-WORKFLOW-141, 142, 143, 148), not the lane's to reopen;
  a redesign is a lead for the coordinator.
- It runs `fork-publish-release --prepare` against a real bundle. *What if*
  the plan it emits is mistaken for a publication step? The brief says
  `--prepare` is the end of what runs; `tools/build-identity-test` is the
  control, T14's.

**Pre-mortem.** A month on, the next M7 build dies at 02:00 and nothing says
so for hours, because a T9 stream changed `watch-job`'s stall or death logic
with only the synthetic controls green, and the real build's buffered logs
took a shape the fixture never had. The review would say: the brief let a
guard change land on fixtures alone. So **A7**: a stream on `watch-job` or
`watch-build` proves against a read-only copy of a recorded M7 run's logs
beside the synthetic control, and the retro names what the stream did to the
watcher's silence modes (`engineering-practices.md` § Say how the watch
fails).

**Blindspot check.** 73 directly (the area's own entry); 8, 14, 22, 26, 42
by class; 75 (a corpus read on the wrong tree) by the brief's figures, each
produced at the hash and marked so; 76 (a merge chain that does not stop) by
the lane-worktree merge, which now stops. A candidate not yet in the
register: *a control that needs an unstated argument or a checkout and fails
on a bare export*, seen twice today (the T30 fixtures that `git -C` their own
path; these two) -- noted, not promoted; three is the threshold.

**Replaced mechanism.** None: a read slice replaces nothing.

**Honesty check.** The simulation's archetype was the fresh lane; a second
run as *the coordinator two weeks on, merging T9's branch*: the branch's
streams touched `watch-build`, and `next` has since moved under the M7
candidate's merge, which also touched `watch-build` (M7's #597 recovery). The
conflict is real and foreseeable: **A8** names it in the merge notes.

## 5. What adjustments or investigations must happen BEFORE execution?

**Written into version 1 of the brief (before the stranger's proof):**

- **A1** § 1 states the host substrate as read today (the helper, the grant
  and the broad fleet grant beside it, the swap at 8 of 8 GiB, Docker, the
  the 45 M7 `.build-runs/`), and forbids every mutating run: no build, no
  `--reclaim-swap`, no `install`, no `--stop-vms`, no `fork-newdrive`, no
  `fork-publish-release` past `--prepare`; the tests run in the lane's
  worktree after the host file is read and the census recorded, and the lane
  reads `.gitignore` for `.build-runs` before its first commit.
- **A2** § 5's evidence floor is the eight controls with their exact
  commands and the export baseline (four PASS; four needing their argument
  or a checkout), each run at stage A in the lane's checkout with its exit
  recorded; a control that fails at the hash is a finding (U-1).
- **A3** § 4 Q6 (brittleness) is a table: for each guard the tools wire
  (`running`/`stalled`/`died`/`error`; the admission refusals; the busy, mode
  and priority refusals of the swap helper; the retention refusals; the
  submit launcher's receipts), the control that constructs its failure, by
  file and test name -- or *none*, which is a finding.
- **A4** § 2 and § 3: the record is the issues the 35 fork commits cite, and
  the recorded M7 runs under `/workspace/repos/rocknix.worktrees/*/.build-runs/`
  are read-only evidence of what the watcher met (`ls`, `cat` of status
  files through the credential filter); never written.
- **A5** § 4 Q1: `fork-newdrive:20-21` and `watch-job:36` carry the legacy
  layout; recorded with #640 named, unchanged here.
- **A6** § 1 and § 5: one GPT seat, one packet of the 18 files plus the six
  entry lines as read-only context, the seat asked first for `reclaim-swap`,
  `install` and `build-admission`.
- **A7** § 7: a stream on `watch-job` or `watch-build` proves on a read-only
  copy of a recorded M7 run's logs beside the synthetic control, and says
  what it did to the watcher's silence modes.
- **A8** § 9 merge notes: `watch-build` and `build-admission` are files the
  M7 lane also changed for #597; the branch's merge after the candidate
  resolves them in the coordinator's hands with the stream's paragraph
  re-applied, as T4's rules are.

**Filed or posted now:** the epic #903 with these as context; the swap
observation on the host coordination file for the M7 lane (U-6).

**Proceeding without:** U-1's answer until stage A; U-2 as a read.

**Errata from the stranger's proof of T9's brief, version 1 (2026-10-24,
15:3x UTC; 72 claims: 54 right, 4 wrong, 6 partial, 1 uncounted, 7
uncheckable), folded into version 2.** `.build-runs/` exists in **45** M7
worktrees and the legacy checkout (2,022 run ids; `conflict-resolution` alone
362), not three: the three were the first of an `ls | head -3`, this futro's
own § 1 included. The entry lines are **seven** (`Makefile:40`, `:179`, and
`build:9`, `build_distro:11`, `image:9`, `install:10`, `build_compat:7`), not
six. The 18 files weigh **201,453 bytes (197 KiB)** at the hash, not about 150
KB. The 35 fork commits also cite #530, #529, #493, #491, #490, #444, #413,
#412, #411, #371, #368, #367 and #310 once each. **U-1 is answered, and it is
a finding, not a `.git` artefact:** `test-watch-build.py` (2026-10-04),
`test-progress.py` and `test-submit.py` all fail at the hash in any checkout
because their fixture trees copy `watch-build` and `watch-job` without the
`build-admission` module `watch-build:50-51` loads beside itself;
`test-build-monitor` passes because its fixture copies it; `source-hashes.json`
in the 10-04 folder records an older `watch-build`. Three recorded controls
stopped running when the admission guard landed and nothing said so; the
lane's stage A records it, the fix is a stream. `test-submit.py` takes no
argument and leaks its `mkdtemp` under `/tmp`. `fork-newdrive` moves and
re-mounts (`sudo mv`, an `fstab` line, `mount`, `rsync`); its `parted` and
`mkfs` lines are header comments for the operator. § 4 Q6's guard list gains
`install`'s eleven checks, `watch-build`'s lock refusal and inherited-run
staleness checks, the submit launcher's duplicate-owner refusal,
`reclaim-swap`'s lock, hard-link, namespace and `fstab` refusals, and
`build-admission`'s identity refusals, all present in the code and absent from
version 1's list. #656's checklist is P1's five until the dispatch writes § 7
there. `build-preflight` in report mode exits 1 on this host today (the swap),
by design.

## Addendum: T10 at its kickoff (2026-10-24, from the brief `docs/reviews/briefs/tooling-guards.md` version 1)

**What we know and assume.** T10 is the area's second slice, **Extended**
(the security list: `.githooks/**`, the credential and wordlist guards),
over **31 paths, 6,676 lines; 29 fork-own and 2 upstream-carried (the two
`.github/scripts/*.sh`, ROCKNIX's); 14 Python, 11 shell, 4 YAML, 2 untagged;
reach `n/a` 31; 336,673 bytes** -- the three hooks with `guard-lib`,
`secret-patterns` and `hooks-test` (20 cases at the hash); the four fork
workflows; the sixteen checkers under `tools/`; and the three `renovation-*`
tools that exist only on P1's branch (read at `2174265e9c`). 92 fork commits
since the base over the 28 at the hash. **Three of the 31 changed after the
hash on other branches** (`ceremony-check` by the #905 packet,
`pre-commit` by the coordinator's marker refusal, `lint-audit-artifacts` by
#810's fix): read as deltas, named by commit. The fork's GitHub has **23
workflows active**, upstream's 19 among them (the build-engine area's). The
fork CI `fork-checks.yml` has **failed on `next` since 2026-10-22** on one
step, the W42 summary (M7's); `fork-wordlist.yml` passes and runs on every
push. The brace glob in `slices.json` is written out in the brief because a
naive glob-to-regex read one tool of nineteen (the coordinator's own first
pass, caught the same hour).

**Known unknowns.** U-1 whether any other reader shares `ceremony-check`'s
fail-open shape (a regex that skips what it does not fit): the hunt is Q3's.
U-2 whether a checker reads nothing and passes (#845's class) -- each
checker's empty-input behaviour. U-3 the `PERSONAL_PATTERNS` list against
`fork-workflow.md`'s *same list* claim, entry by entry (92 quoted entries in
the hook; the rule's prose is a different shape). U-4 what upstream's 19
active workflows do on the fork (a schedule that fires, a PR check that
runs): a lead for the coordinator, not this slice's row. U-5 Gemini's output
ceiling on a 328 KiB packet (T30's was larger and hit it once): D-WORKFLOW-195
answers it. U-6 whether `box-check`'s API cost (300 open issues) fits beside
the coordinator's monitors: the budget is read before and after.

**Patterns.** T4's F-02 (the friction reader), F-22, F-23 are this slice's
first leads and were found by reading the rule against the tool: the same
read in the other direction (the tool against its three descriptions) is Q7.
T6's #845 (`pkgcheck` exits 0 on an unknown name) is the class for Q3. The
pre-push's header carries its own proven refusals (2026-09-13), the model
for every guard's positive. Blindspot 67 (a fixture in history before any
guard read it) is why fixtures are built at run time and why the packet is
scanned before it is sent. Blindspot 76 is why `pre-commit` now refuses a
marker on the coordinator's branch -- a delta this slice reads, not a change
it makes.

**What could we be missing.** A fresh lane runs `tools/forbidden-terms-check`
and, reading its code, wants to see the list it reads: the brief forbids the
read (D-WORKFLOW-061); the constructed refusal uses a stand-in file as
`hooks-test` does. A lane runs `pr-stack-check` to see what it builds: it
builds a throwaway worktree in the repository -- `--help` only. A seat
proposes widening `SECRET_PATTERNS`: a stream adds the line it now catches
*and* the line it must still pass, in `hooks-test`, never a widening alone.
Pre-mortem: a month on, a push carries a listed word because a stream
"tidied" `guard_scan`'s regex and the only case that would have caught it
was never written -- so **a stream on a hook adds the `hooks-test` case that
fails on the unfixed hook, or it is not a stream**. Replaced mechanism: none
(a read).

**Adjustments written into version 1 of the brief:** A1 § 2 writes the tool
list out and names the three after-hash deltas by commit; A2 § 5 scans the
packet before it is sent and forbids every read of the wordlist and the
secret's value; A3 § 4 Q6 is a guard table with a positive or a case per
refusal and a caller per tool; A4 § 4 Q3 hunts the fail-open shape through
every reader by name; A5 § 7 records the CI's runs and the 23 active
workflows with one lead for the coordinator; A6 § 8 names the mutating modes
(`fork-worktree sync|remove|repair`, `pr-stack-check`, `gh workflow run`,
`gh secret set`) as stops; A7 § 10 runs `hooks-test` on the simulated merge,
since the coordinator's branch also changes a hook; A8 § 9 the merge order
(after T9's branch, before T4's).

### Errata from the stranger's proof of T10's brief (version 2, 2026-10-24)

A reader with no context reproduced the brief's claims read-only (8 API
calls, nothing written outside `/workspace/tmp/m6-coordinator/t10-proof/`):
most held; six were wrong and two partial, corrected in version 2:

- **The line counts.** The table's "Lines" column was the inventory's
  (computed on P1's tree): at the read refs `pre-push` is 470 (473 on P1's
  tip, which adds the three `renovation-*` personal patterns),
  `lint-audit-artifacts` 394 (426 on P1's: the renovation face,
  `fc88815ccb`) and `renovation-inventory` 1,597 (the inventory's 1,596
  predates `00ca350666`); the sum at the read refs is 6,642, the inventory's
  6,676. Both are now in the brief, labelled. The same fact corrects § 2's
  claim that the lane's branch differs from the hash on none of the 28: it
  differs on five (`pre-push`, `lint-audit-artifacts`, `register-check`,
  `pre-commit`, `hooks-test`), each with a known owner, now listed as the
  expected shape.
- **128 fork commits** since the base over the 28, not 92 (125 without
  merges); the citation ranks (#383 12, #344 and #258 7) were right. The
  addendum above carries the old figure.
- **`PERSONAL_PATTERNS`** spans `pre-push:62-188` with 115 quoted entries
  at the hash (84 `tools/`, 12 `scripts/`), not 62-160 and 92; 62-191 and
  118 on P1's tip. The rule's 84 `tools/` paths match the hook's 84 by
  count; the entry-by-entry read stands.
- **`register-check`** reads 644 IDs on the hash's export, 656 on P1's tip,
  666 on the coordinator's, 667 on the lane's branch after the merge -- not
  "667 on the export".
- **The fork CI** has been red on every run of `next` since 2026-10-19
  (last green 2026-10-18T11:00Z), not since 10-22; the 2026-10-24 run
  fails on *ceremonies are not overdue*, the 2026-10-21 run failed on the
  `box-check` step; 10-22 and 10-23 are the lane's to read.
- **`generate-changelog.sh`** is not byte-identical to `upstream/next`: one
  fork hunk (`8a7f33791d`, 2026-09-11) drops the author lookup through
  `gh api`; `generate-release-body.sh` is identical. The brief had left
  this as a read to make; it is now the answer, with the hunk's reason as
  a Q4 row.
- **Partial: `gh secret list`** fails for this token (`failed`), so the
  `FORBIDDEN_PATTERNS` secret's existence is inferred from the wordlist
  workflow's green runs; the brief's command and criterion say so.
- **Partial: `order.md`'s "6,400 read (6,014 fork-own)"** is P1's own
  derivation; the inventory's columns give fork-own 6,290 and
  upstream-carried 386. Quoted as P1's, with the inventory's figures beside.
- **Not an error:** the lane worktree existed when the proof ran (cut at
  `50137e3ee0` before the dispatch); the brief said so in the future tense
  and now says it in the present. `rules-check --help` runs the checks,
  `forbidden-terms-check --help` treats `--help` as a tree (rc 2): both
  reproduced, both Q7 rows for the lane.

### Errata from T10's stage A (16:31 UTC, lane tip `5611a4fb62`)

Three figures of version 2 corrected by the lane's own read, written into
the brief by the coordinator the same hour:

- **`generate-changelog.sh`'s diff against `upstream/next` is upstream's,
  not the fork's**: two upstream commits (`76693a738d`, `71d8932b33`,
  2026-10-13/14) are not yet in `next`; the stranger's proof saw the diff
  and the errata above called it a fork hunk without reading its direction
  (`git merge-base --is-ancestor` on the two commits settles it). The fork
  carries no hunk of its own on either upstream script.
- **`PERSONAL_PATTERNS` holds 14 `scripts/` entries**, not 12 (the 84
  `tools/` and the 115 total stand).
- **`hooks-test`'s 20 `expect` call sites print 27 results** at the hash
  (a site inside a loop runs more than once), 22 sites and 29 results in
  the worktree; version 2 called the sites "cases" and gave no result
  count.

Two leads the lane raised for its stage B, noted here because the
coordinator's own ceremonies lean on them: `box-check:83` reads
`gh issue list --limit 300` against 458 open issues and prints `0 fail`
(the checkbox gate in `fork-checks.yml` and `ceremony-check`'s line read a
third fewer issues than exist), and `forbidden-terms-check` skips the
tree's 180 tracked symlinks without comparing its scanned count with the
listed one. Both are Q3's shape (a guard that reads less than it claims);
the lane files them as bugs at stage D (D-WORKFLOW-187).

## Addendum: T12 at its kickoff (2026-10-24, from the brief `docs/reviews/briefs/tooling-vm-harness.md` version 1)

**What we know and assume.** T12 is the area's third slice, **Independent**
(one GPT-6 Astra seat), over **60 paths, 8,790 lines, all fork-own; 20
Python, 10 shell, 22 `.steps` walks, 3 text, 2 Markdown, 3 PNG fixtures;
484,627 bytes at the hash** -- `vm-qa` and its 17 suites, `vm-visual-qa` and
the walks, `time-to-play`, `frame-diff` with its 391 claims, the pair, the
serial shell, `vm-stop`, the rehearsal, the three RetroAchievements proofs
and the two proxy tests, the memory measurements, the QA-account carrier,
`device-act`, `es-syntax-check`, `es-untranslated`, `font-stems`,
`png-blackout`. 145 fork commits since the base; none on `upstream/next`;
the branch differs from the hash on none of them. Two of the 60 run in the
fork CI (`vm-pair-test`, `vm-upgrade-readiness-test`); `vm-qa` is the one
caller of most of the rest; eight candidates may have no caller at all. The
lens is **cost against value**: the record (`docs/vm-qa-log.md`, ten
`docs/qa-logs/` folders with reports, sixteen blindspots naming these tools)
is the value side, the reports' minutes and the host's guests the cost side.

**Known unknowns.** U-1 how each tool finds, waits for and stops a QEMU
(pidfile and owned disk, or pattern -- T9's F-03 shape in `build-preflight`
is the warning). U-2 which suites have caught nothing recorded (the value
table's `nothing recorded` rows are the lens's output). U-3 whether a
GENERIC_X64 image on the host still boots the harness as the tools expect
(the newest is 2026-10-02's; the M7 lane's QA images are newer). U-4 the
`/tmp` roots (`/tmp/rocknix-qemu-monitor-*.sock`, `/tmp/ttp`) against the
inode exhaustion of this morning. U-5 the 391 claims against the 17 walks
and 22 step files: claims no walk exercises, walks no claim owns. U-6 the
cost of one guest cycle on the lane's clock (T8's five cycles ran 14 to 30
minutes each).

**Patterns.** Blindspot 39 (a PASS over missing numbers) is the harness's
own founding lesson and the Q3 shape to hunt through every suite. T8's five
guest cycles on 2026-10-24 are the recorded shape of a cycle (host file,
pidfile, `vm-stop`, census, retirement). T9's `build-preflight` finding
(stop by pattern) is the Q2 shape. T10's class (a checker that reads less
than it reports) applies to a runner that folds a suite that could not run
into a pass -- `vm-qa` says it does not (`SKIPS=0`); the proof is a
constructed rc 3.

**What could we be missing.** A fresh lane reads "the VM harness" and
reaches for a full `vm-qa` run on a fresh pair (an hour of two guests): the
brief authorizes one bounded cycle with `--only` the suites the cost table
needs and names the image first. A lane finds a suite with no catch and
proposes deleting it: the brief says the lens is not a licence; the
coordinator decides with the maintainer. A seat proposes changing what
`time-to-play` measures: a contract lead (D-QA-022, D-CLOUD-122), not a
stream. Pre-mortem: a month on, a candidate passes `vm-qa` while a suite
silently skipped, because the SKIP accounting was never seen to fire -- so
the brief's Q3 asks for the constructed rc 3. Replaced mechanism: none (a
read).

**Adjustments written into version 1 of the brief:** A1 § 2 writes the
brace glob out as names and lists the eight no-caller candidates; A2 § 5
authorizes one guest cycle with its exact ritual and forbids the second
without a line; A3 § 4 makes Q5 and Q6 the two tables (cost, value) the
slice is for; A4 § 7 asks the claims-against-walks reconciliation and the
find/stop classification by name; A5 § 8 names the handheld, the QA account,
the pattern kill and `/tmp` as stops; A6 § 9 adds the cycle's own ritual
(`docs/vm-qa-log.md`); A7 § 10 includes the host checked for a payload left
behind.

### Errata from the stranger's proof of T12's brief (version 2, 2026-10-24)

A reader with no context reproduced the brief's claims read-only (4 API
calls; the three no-guest controls run from an export, rc 0 each):
most held; nine were wrong or partial, corrected in version 2:

- **The host held no image where version 1 pointed.** The `x64-*`
  directories live under `/workspace/artifacts/rocknix-images/`, not
  `/workspace/artifacts/`, and their payloads were retired on 2026-10-07
  (`RECORD.txt`, `SHA256SUMS` and the retirement JSON remain). The newest
  GENERIC_X64 image present is the M6 lanes' copy of the `069fc2704421`
  build under `/workspace/artifacts/m6-t1-20261023/` (2,122,289,964 bytes,
  with its `.identity.json`). A lane following version 1's § 5 would have
  found nothing to boot; the brief now names the file and its sidecar.
- **The at-hash line loop sums to 8,813**, not 8,790: `wc -l` counts 23
  newline bytes inside the three PNGs; the inventory's column, which stores
  no count for an image, sums to 8,790. Both figures are now in the brief.
- **Three walk files' last commits** were given as the directory's:
  `fixtures/system-selected.sh` is `d97f64ddfd` (2026-10-05),
  `cloud-epic/migration-protocol.sh` `083f4fad86` (2026-10-08),
  `cloud-epic/vnc-grab.py` `3b9a62d976` (2026-10-02).
- **`docs/vm-qa-log.md`'s five entries run 2026-10-06 to 2026-10-17**, not
  "since 2026-10-15"; 13 `### ` sub-entries sit under the 2026-10-09 one.
- **The report folders:** 27 top-level `docs/qa-logs/` folders hold a
  `vm-qa` report (61 reports) and 13 a `time-to-play.log`; "ten" was the
  `*-pixelelated-replacement-NN` subset.
- **Blindspot 65 names none of the 60** (the proxy's guest script and the
  shims); fifteen entries name the harness, not sixteen.
- **Three of the eight "no caller" candidates have callers** by the
  brief's own criterion: `png-blackout` (a skill instruction), `vm-serial`
  (rule commands; four callers in the 60), `device-act` (a rule
  instruction). Five remain: three with index mentions only, two with a
  descriptive rule paragraph.
- **`generic-x64-vm-testing.md` names 17 of the 30 scripts**, not "almost
  all"; the thirteen it does not name are listed in the brief.
- **The issue ranks hold under every-occurrence counting**; the method is
  now stated.

And one unknown answered early: **U-1** -- every `pgrep`, `pkill` and
`kill` in the 60 is guest-side over SSH or serial; no tool finds or stops a
host QEMU by pattern, and `vm-pair`, `vm-stop` and `vm-qa` carry no
host-side kill. The lane confirms it and reads `vm-pair down`'s stop path.

## Addendum: T14 at its kickoff (2026-10-24, from the brief `docs/reviews/briefs/tooling-state-tests.md` version 1)

**What we know and assume.** T14 is the area's fourth slice, **Independent**
(one GPT-6 Astra seat), over **32 paths, 6,911 lines, all fork-own; 20
Python, 2 shell, 10 Markdown; 396,588 bytes at the read refs** -- twenty-one
test tools (the `pixelelated-*` and `rasteratops-*` family, the settings,
wait-lock, melonDS, USB gadget, Nova LED, RetroArch wrapper, hardware
readings, build identity and candidate store tests, two retired stubs) and
eleven fixture files, ten of them the lint's fixtures that exist only on
P1's tip. 35 fork commits since the base; none on `upstream/next`; the
branch differs from the hash on none of them. **Who runs them:** every
default `vm-qa` run reaches five of them (the `wrapper` suite directly;
four through T15's `last-good-scripts-test`, the `scripts` suite, 13 of the
33 minutes by T12's table); the fork CI runs `rocknix-info-test`; the
release preparer calls two; `cloud-round-trip` one; T12's protocol walk one
that refuses today; **eleven nobody runs**, two of them retired by design.
No blindspot entry names any of the 21; three decision rows do. The lens is
**brittleness**: what each test depends on that is not the thing it proves,
what it caught, who runs it, what its positive is.

**Known unknowns.** U-1 the busybox fallback: `settings-modes-test` and
`melonds-upgrade-test` take candidate applets from a build root, and this
host has none for this lane (T9's and T10's worktrees build nothing) -- does
each say so, and is a PASS under the host's applets marked as the host's
(blindspot 34)? U-2 the real-rclone four's backend binding: could a host
`rclone.conf` leak into a test meant to be isolated? U-3 the two guest
tests: whether any claim needs the one authorized cycle, or the record (the
2026-10-08 and 10-11 qa-logs) answers. U-4 the eleven no-caller tools: which
have a caller in the record (a candidate's qa-log) rather than in the tree.
U-5 the two retired stubs: keep as refusing markers, or remove with their
index rows and list entries (the coordinator's call at the pause). U-6 how
T15 assumes these four behave (read, never edited: T15's brief follows).

**Patterns.** T9's F-13 (an `assert` as a final check; `python3 -O`) and
its #597 fixture (a fixture copied from the current tool cannot see a
regression); T10's five fail-open shapes and its `|| true` lesson; T12's
`--only X` passing with nothing run and `--repeat 0` with empty headlines;
blindspot 34 (the host's `tr` is not the guest's). Each is a stage-A grep
or a Q3 hunt here.

**What could we be missing.** A fresh lane runs the four real-rclone tests
without reading what backend they bind and touches a real `rclone.conf`: the
brief reads the binding first and names the local backends. A lane sees
eleven tools nobody runs and proposes deleting them: the lens is not a
licence; a caller in the record counts. A lane edits
`last-good-scripts-test` to fix how it calls a tool here: T15's file, never
edited here. Pre-mortem: a month on, a candidate's `scripts` suite passes
while `settings-modes-test` quietly took the host's applets because no build
root existed on the box that ran it -- so U-1 is asked in writing at stage
A. Replaced mechanism: none (a read).

**Adjustments written into version 1 of the brief:** A1 § 2 writes the globs
out, lists who runs each tool, and names the eleven no-caller ones and the
two stubs; A2 § 5 reads the real-rclone four's backend binding before any
run and marks a host-applet PASS as the host's; A3 § 4 makes Q6 the
brittleness table with four columns per tool; A4 § 1 and § 8 keep T15's file
out of reach; A5 § 5 authorizes one guest cycle under T12's ritual only if a
claim needs it; A6 § 7 asks the `|| true`, `assert` and host-path greps by
name; A7 § 10 includes the host checked for a payload left behind.

### Errata from the stranger's proof of T14's brief (version 2, 2026-10-24)

A reader with no context reproduced the brief's claims read-only (4 API
calls; seven of the tools run from an export): the membership, the counts,
the table's lines and commits, the 35 commits, the registers and the host
facts held; eight items were wrong or partial, corrected in version 2 -- and
two of them are findings, not errata:

- **`build-identity-test` fails at the hash** (exit 1, 21 passed, 2 failed):
  its plain-text firmware stand-in is refused by the `pixelelated-state-check`
  gate `fork-publish-release` gained at `d9f428e1a0` (2026-10-13, #565), two
  days after the test's last change; it also needs `scripts/` beside
  `tools/`. Version 1 listed it among the tests the coordinator re-runs
  expecting a pass. The same class as T9's three controls: a test broken by
  a guard added beside it, run by nobody since. A stage-D bug, found before
  the lane began (U-1's answer, in part).
- **`retroarch-wrapper-test` cannot run bare on this host:** its hardcoded
  roots `rocknix.worktrees/{devices,generic-x64}` are #640's and absent; it
  passes with a RetroArch source named, and leaves `t.c` in its temp dir
  (`:213`). `vm-qa`'s `wrapper` suite runs it bare on every default run.
- **Two callers were not callers:** `rasteratops-vm-cloud-epic` *sources*
  T12's `migration-protocol.sh` (`:149`), not the reverse; `cloud-round-trip`
  names `wait-lock-test`'s property in a docstring. By invocation, thirteen
  tools have no caller, not eleven.
- **Twenty `build.*` directories exist** under the M6 worktrees (three
  entries each, no busybox in any); version 1 expected none. The writer
  tests **require** `--busybox` and `--output`; they do not "say so when none
  does".
- **`rasteratops-identity-check`** is source-only with a required `--es`;
  version 1 said "in source and an image" and ran it bare.
- **Issue ranks:** `#356` and `#320` are also cited twice each.
- **The `--payload-tests` mode** of `pixelelated-state-check-test` invokes
  `fork-publish-release` and needs the squashfs and disk tools; the brief
  now runs `--self-test` and names the condition for the other.
- The stage-A greps' figures are now in the brief from the proof (`|| true`
  0; `assert` in two tools; 28 host-path lines in ten files).

## Addendum: T15 at its kickoff (2026-10-24, from the brief `docs/reviews/briefs/tooling-last-good-test.md` version 1)

**What we know and assume.** T15 is the area's fifth slice, **Independent**
(one GPT-6 Astra seat), over **one path, `tools/last-good-scripts-test`:
14,238 lines, 1,167,697 bytes, fork-own, shell, 408 fork commits since
2026-09-10, none upstream** -- the order's deliberate exception to the
8,000-to-12,000-line bound, because a test split across two sessions loses
its fixtures' context. Thirty-four sections `a` to `ah`, 120 `check` call
sites (a run counts about 1,300 to 1,400 checks), 85 `bwrap` sandboxes
from `y` onward, `set -u` only, eight `|| true`. **Who runs it:** `vm-qa`'s
`scripts` suite on every default run (13 of 33 minutes) and the release
procedure's step 3 through it; by hand with `--old` for its five historical
controls. **Its record this week:** the last PASS in a report is 2026-10-06
(qa-18, 1,719 PASS lines, the image's BusyBox 1.36.1 from a build root);
every run since from an M6 worktree resolved the host's 1.37.0 through
`image_tool_source`'s silent fallback and FAILed 319 checks whatever its
scratch (T12's three runs, Bug #1015; T14's run, 323 with two of its own
and two of its contract's). T14's accepted fixes make the two writer tests
this file calls refuse a busybox without provenance (#997), which this
file's two call sites do not yet give. The lens is **brittleness**: what
each section depends on that is not the thing it proves, what happens when
it is absent, what it caught, who runs it, its positive.

**Known unknowns.** U-1 the busybox split: of the 319 FAILs under the
host's busybox, which are the host's applets (`flock` absent in 1.37.0;
`tr`, `sed`, `stat` semantics) and which the tree's -- answered by two
stage-A runs at the hash, one with `QA_SYSTEM_ROOT` on an M7 root and one
without, and the diff of their verdict lines. U-2 the five `--old` recipes:
does each still FAIL as the header promises, or has a control stopped
controlling. U-3 the sandbox's host network (no `--unshare-net` in
`sa_run`): does any sandboxed script reach the network. U-4 the `check $?`
after compound tests and the `|| true` sites: which can pass on a failed
read. U-5 the split: what a split of `y` (4,683 lines) and `z` (541) out of
the file would cost in shared harness, and whether the order's invitation
stands. U-6 the seat's packet: a 1.1 MiB file exceeds a comfortable input,
so the packet is the harness, the helpers, the index, the call sites and
the verdict plus Q3's suspect sections whole, and the seat asks for more.

**Patterns.** Blindspot 34 (the host's `tr` is not the guest's), which is
this file's founding lesson and whose fallback undoes it; T14's S8 (a
busybox without provenance is CANNOT, or marked and exit 3); T12's
`--only X` and `--repeat 0` shapes (a selection that runs nothing and
passes); T10's five fail-open shapes and the `|| true` lesson; T9's #597
fixture (a fixture copied from the current tool cannot see a regression --
the `--old` recipes are this file's answer, if they still fire).

**What could we be missing.** A fresh lane runs the suite as a shell
background job and reads the SIGINT refusal (exit 2) as a defect: the
brief names `setsid -w`. A lane runs it from the worktree with `TMPDIR`
under the worktree and meets T12's seven `AF_UNIX path too long`: the brief
puts `TMPDIR` under `/workspace/tmp/m6-t15/`. A lane edits a script the
file proves because a check FAILs on the tree: the brief makes that a `bug`
for the script's lane. A lane edits T14's tools from T14's worktree to make
the call sites agree: the brief reads them from `7c1d729b57` and never
writes there. A lane treats a run under the host's busybox as the suite's
verdict: the brief keeps the two runs apart and names the banner line.
Pre-mortem: a month on, the release procedure's step 3 reads `scripts PASS`
from a box with no build root, under the host's applets, and the device's
`flock` path is untested -- so S1 of this slice makes the fallback refuse
or mark, and the call sites say their provenance. Replaced mechanism: none
(a read).

**Adjustments written into version 1 of the brief:** A1 § 1 names the two
M7 roots with their BusyBox version and BUILD_ID as the read-only source
for `QA_SYSTEM_ROOT`, and the host's 1.37.0 beside them; A2 § 5 runs the
suite twice at stage A (image and host busybox) and diffs the verdicts;
A3 § 5 runs each of the five `--old` recipes once; A4 § 7 makes the
fallback's refusal or marking and the two call sites' provenance flags the
slice's acceptance, not a coordinator edit; A5 § 1 sizes the seat's packet
by excerpt and lets the seat ask for more; A6 § 8 forbids a shell
background start and a worktree `TMPDIR` by name; A7 § 8 requires the
session pointer at every checkpoint (#1014).

### Errata from the stranger's proof of T15's brief (version 2, 2026-10-25)

A reader with no context reproduced the brief's claims read-only (4 API
calls; the suite not run; 89 claims: 67 verified, 8 wrong, 10 partial, 4
uncheckable): the file's size and history, the 34 sections' lines, the
helpers' lines, the eight `|| true`, `set -u` only, the call sites and
their flags, the two M7 roots and the host's busybox, the registers and
the issues held; the wrong and partial figures are corrected in version 2,
and three of them are findings, not errata:

- **`setsid` does not reset an ignored SIGINT.** Version 1 named `setsid -w`
  as the remedy for the suite's refusal to run as a shell background job
  (`:260-268`); the stranger tested `-w` and `-f` with SIGINT ignored in
  the parent and both children kept the bit, so the suite would exit 2
  either way. The file's own comment at `:264` names `setsid -f` and is
  wrong on the same point. The remedy is `vm-qa:158`'s launcher, a
  `python3 -c` that sets SIGINT and SIGPIPE to default and execs; the brief
  gives it, and § 7 quotes each run's `SIGINT ignored=0` line. The
  coordinator's two runs happened to start from a shell with SIGINT at
  default, which is why they ran.
- **The verdict has a fourth word.** `NOT APPLICABLE` (`:4558`, the
  retired `cloud_migrate_layout` group, #508) is reported at `:14235` and
  the run exits 0 `PASSED` when nothing failed or skipped: a group that
  did not run passes. Version 1 said the verdict already had D-QA-061's
  shape; Q3's first item now.
- **The no-busybox case is silent.** `image_tool_source`'s fallback is
  `command -v busybox || true`: a host with a busybox gets a copy of it
  and a banner line naming the source; a host with none gets no copy, no
  wrappers and no banner, and the run proceeds on the host's GNU tools
  with nothing said. Version 1 said the fallback was "said only in the
  banner".
- **Sandboxing starts at section `b`, not `y`:** 60 `bwrap` invocation
  lines (85 lines carry the word, 24 of them comments), 16 sections before
  `y` invoke it, `sa_run` is called 150 times, so a run opens more than
  200 sandboxes; four invocations do `--unshare-net` (`:6108`, `:11890`,
  `:12285`, `:12303`) where `sa_run` does not; the wrapper lists differ by
  section, and `flock` is shimmed only in `n` and `t` and called on the
  host at `:2345` and `:6765`.
- **`y` is 5,386 lines, not 4,683:** stream B's `y1` to `y4` at
  `:7796-8905` (1,110) and stream A's cases from `:8906` (4,276).
- **Twelve `--old` recipes, not five** (`:167-226`): the default
  `1d1503180d` and eleven more; version 1 named the last five. § 5 and § 7
  now run all twelve.
- **Line references:** `skip()` `:302`; the banner `:426`; `image_tool_source`
  `:381-401`; the copy's comment `:403-414`; the sandbox helpers
  `:8993-9029` (`sa_tail` and `sa_outcome` included).
- **The record's figures:** the last PASS ran 01:04-01:37 UTC on
  2026-10-06; `scripts_pass_lines: 1719` in `qa-18/counts.json` counts
  lines carrying the word PASS (1,721 by grep), not checks (1,374 in that
  log); `docs/vm-qa-log.md` names the tool in 8 lines (61 carry `scripts`);
  T12's worktree-scratch run FAILed 326, the other two 319; T12's compare
  file and T14's `02` are on their branches only until the merges, so the
  brief gives `git show` paths.
- **Unactionable for a stranger, now fixed:** the session pointer the first
  commands `cat` is seeded by the dispatch and absent before it (said);
  the `--old` loop covers all twelve.

And the coordinator's two runs of the suite at the hash (§ 2 of version 2):
under the image's busybox 1,303 PASS / 10 FAIL / 0 SKIP in 514 s; under the
host's 984 / 329 / 0 in 671 s; 319 checks flip between them (#1015's count),
and the ten that fail under both are the suite's own vacuous-fixture
detectors firing in `x` and `y` -- the first thing the lane sorts.
