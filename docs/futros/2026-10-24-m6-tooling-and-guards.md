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
