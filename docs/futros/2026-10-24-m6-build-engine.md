# Futro: the build-engine area epic (#800), at T5's kickoff (#652)

**Prepared:** 2026-10-24, by the M6 coordinator lane (D-WORKFLOW-189), from
the brief `docs/reviews/briefs/build-engine.md` version 1 (`d2da1e2c3c`)
and the tree at `next` = `8ebaf8daad`.
**Scope of this futro:** the area epic #800 (the build engine: T5 #652 the
engine, T6 #653 upstream's helper tools and the other distributions) at
the kickoff of its first slice, T5. It covers T5's execution under its
brief and T6's order after it. It does not cover T6's brief (its own
reading at its dispatch), T7 to T9 (the packages' and the tooling's
epics), the container pin's refresh (the coordinator's act, recorded when
it moves), or the integration merges (the coordinator's, plan § 8).

**Upstream retros consulted:** T1's mini-retro (#648,
`docs/retros/2026-10-24-m6-os-launch-control-state.md` on the T1 branch at
`d3aa6a19c5`); T2's (#649, `docs/retros/2026-10-23-m6-es-launch-path.md` at
`7041b0d710`); P1's (`docs/retros/2026-10-23-m6-p1-survey.md`). T3 is at
its stage B and has no retro yet; its stage-A post (#650, 02:49) is read.
**Inputs considered:** the brief; #652's body; #800's body; #644's
`docs/reviews/build-path-read.md` (26 findings, nine T5's, one T6's); the
plan (§ 3, § 4, § 6a to § 8, § 11); `docs/reviews/order.md` § 3 and the
sizing rows (`| 5 | the build engine | ... | 242 | 13,910 | 6,776 (2,419)
| 0 | Extended |`; `| 6 | ... | 135 | 7,369 | -- (135 rows) | 0 | Local |`);
`slices.json` entries 5, 6, 9 and 10; `areas.json`'s `build-engine` and
`tooling-and-guards` entries; P1's `inventory.json` filtered by the slice's
rule; the two sibling futros (#798, #700) and their errata;
`docs/blindspot-register.md` (74 entries); the artifacts inspected below.

## 1. What do we know and what are we assuming?

**The plan (as written).** T5 reads the engine -- the 30 scripts, the
configuration, the identity, the Makefile and the container recipe, the
139 system fragments, the 19 upstream workflows the fork carries -- under
the code-auditor lifecycle with the renovation face; its kind is **read**
and its lens *cost against value* (everything else is built by it); the 18
fork-own paths and the upstream-carried engine core get all seven
questions, the fragments, the other configuration trees and the workflows
Q4 and Q6 first; nine of #644's findings are carried as rows with the
dispositions the brief names; the evidence is recorded runs, sandboxed
calls and the install tree, never a build; Extended depth because
`scripts/get_env` handles credentials. Then the stage-D pause, the
coordinator's stream briefs, remediation, stage F, the retro, the
hand-back.

**Explicit assumptions we are relying on, each with its evidence:**

- **The membership is the inventory's rows of the `build-engine` area under
  the slice's globs, and the area filter is what keeps three other areas
  out.** Evidence: the brief's filter run on 2026-10-24 against `git show
  2174265e9c:docs/reviews/inventory.json` reproduces the order row's `242
  paths 13,910 lines`; without the area, the globs sweep in 46 council
  scripts under `scripts/` (`tooling-and-guards`), 6 `fork-*.yml` workflows
  (`tooling-and-guards`) and 353 `.github/sessions/**` files (`records`):
  `scripts/council-invoke.ts`, `.github/workflows/fork-checks.yml` and
  `.github/sessions/saved-session-state-next.md` read those areas in the
  inventory by command.
- **The order row's `6,776 (2,419)` is the inventory's code classes, as it
  was for T3.** Evidence: the same `read_lines` rule (`tools/renovation-inventory`
  line 999, the code classes by `language`); the brief's own fork-own figure
  is 3,266 lines (the 18 paths' `lines` summed) and the difference is
  `config/functions` (1,936, `none`), the `distributions/ROCKNIX`
  configuration, `config/graphic` and the `config/arch.*` files, which the
  tool does not count as code and the brief reads whole.
- **No M7 delta touches the membership.** Evidence: `git -C
  /workspace/repos/rocknix log next..069fc2704421 -- scripts config
  distributions/ROCKNIX Makefile Dockerfile .gitignore .github` prints one
  commit (`d2257675fe`) whose files are three `.github/sessions/**`
  checkpoints, the `records` area. T3's stage-A correction (the M7 hunk
  `6101242e14` is on no `origin` branch) applies to its file, not to this
  slice's.
- **The recorded runs exist and are readable.** Evidence (artifact
  inspection, 2026-10-24 02:55): `/workspace/repos/rocknix.worktrees/m7-signin-build-20261022-07/.build-runs/`
  lists run directories (`20261022T235650Z-bfce2199`, `20261024T001923Z-637a26eb`,
  `20261024T001928Z-e02569d9`, an `active.lock`); one run holds
  `build.log build.pid build.rc build.start build.status build.status.pid
  command.pid runner-result.json watch-job watcher.err watcher.interval
  watcher.pid`, its `build.rc` reads `1` and its `build.status` the
  watcher's `state: finished`, `written: 2026-10-22 23:57:25 UTC`,
  `progress: none matched`. Read-only; the M7 lane's.
- **The host has what the sandbox and the checks need, except two tools.**
  Evidence (`command -v`, 2026-10-24 02:58): `bash`, `python3`, `gh`, `git`,
  `jq` present; `docker` 29.8.2 present and **`docker manifest inspect`
  reads both images without a pull** (upstream's
  `ghcr.io/rocknix/rocknix-build:latest` answers with a manifest list whose
  amd64 image digest is `sha256:a81b63a53612…`; the fork's pinned
  `ghcr.io/pixelelated/build@sha256:988c0ba5…` answers too, so the brief's
  Q4 (b) read is feasible anonymously); **`shellcheck` and `actionlint`
  absent** (shellcheck downloaded as T1 did; the workflows are read).
- **The engine's shell and Python parse today.** Evidence: `bash -n` over
  the 24 membership scripts with a `bash`/`sh` shebang: 0 failures (the
  other six are Python or have no shebang: `get_archive`, `get_file`
  classed `none`); `python3 -I -m py_compile` over `pkgbuilder.py`,
  `genbuildplan.py`, `uboot_helper`, `test-audit-review.py`: all four
  compile.
- **`tools/build-identity-test` fails today, and not on the engine's
  half.** Evidence: `python3 -I tools/build-identity-test --output
  <scratch>/result.json` on `c73f43c028` → `FAIL build identity: 21
  passed, 2 failed`, rc 1; the two failing checks are `rc1 public plan
  accepted` (error: `release preparation: selected-state inspection refused
  a firmware asset`) and `harness completed`, the release-plan half that
  calls `tools/fork-publish-release --prepare`, which now runs #565's
  selected-state inspection over the test's *"tiny firmware stand-ins"*;
  the 21 identity checks of `config/build-identity` and `scripts/image`
  pass. Filed as **#801** before any fix (D-WORKFLOW-132); the fix is T9's
  or T10's (the fork tools), and the brief's § 5 trial line must say what
  to expect (§ 5 below).
- **The reviewer route is in the tree and the key is on the host.**
  Evidence: as for T3 (`033eb7ed23`, `0ceb2994c5`, `6874394d49`; T1's and
  T2's provenance files; `~/.config/council/env` present, never read).
- **The register's next Decided ID is 193.** Evidence (base-divergence
  check, 2026-10-24 02:59): this branch's register has 189, 190, 192
  Decided and 191 Open; P1's 188 and 189; T1's and T2's 188 to 191; T3's
  branch at `origin/feature/m6-emulators-libretro-650` carries no
  D-WORKFLOW-193. No collision; 193 is free on every branch.
- **T3 runs beside T5 and shares one function file by reference only.**
  Evidence: `distributions/ROCKNIX/config/functions` is a `build-engine`
  row (T5's); T3's brief § 2 names it as T5's and its stage-A post says
  the same; T3 posts a lead, never a fix, on it.
- **Build-vs-adopt:** not applicable; an audit slice adopts nothing. One
  line, as the skill allows.

**Confidence:** mixed. The counts, the areas, the hashes, the parse checks
and the manifest reads are verified by command; the identity test's
failure is understood at the level of its error line and filed, not yet
traced to a line; the ccache question (#644 finding 8) and the `created`
dates of the two container images may be unmeasurable without a build or
a pull, and § 2 treats both.

## 2. What known unknowns need investigation?

| Unknown | Treatment | Owner / task |
| --- | --- | --- |
| Whether the two container images' `created` dates can be read without a pull (`docker manifest inspect -v` gives the config blob's digest, not its content; `gh run list --repo ROCKNIX/distribution --workflow build-docker-image.yml` printed nothing on 2026-10-24) | Proceed; the Q4 (b) table carries the two **digests** (the pin's and upstream's current manifest list and per-platform image digests) as the comparison that proves same-or-different, and the dates as `not read` with the commands tried where the registry gives none; the Makefile's commit date (`2c349c6d51`, 2026-10-01) and #644's dating of the mirrored image (2026-09-25) stand in | the lane, Q4 |
| Whether the ccache comparison (#644 finding 8) can be measured without a build: `ccache --show-stats` with `CCACHE_DIR` pointed at an M7 root's `.ccache/` is a read, but the roots are the M7 lane's | Proceed; the brief's § 5 allows `ls`/`cat` under the M7 worktrees and nothing else; a `ccache --show-stats` there is a process started in the M7 lane's tree, so **not run**; the measurement is `not measured` with the reason, and the comparison is of the settings' text against CI's `build-*.yml` and the `.build-runs/` logs' timings | the lane, Q5 |
| Whether sourcing `config/options` in the sandbox creates directories (`config/path` derives `BUILD`, `TARGET_IMG`, `SOURCES` from `ROOT`) or otherwise writes outside the scratch | Investigate at stage A as the first sandbox trial: `bash -x` the sourcing with every variable set to the scratch, the trace to a file, and `grep -E 'mkdir|> |>>|cp |mv |touch' trace` read; any path outside `.qa-scratch/` is a FAIL of the sandbox and the variable list grows until none remains | the lane, stage A; version 2 says so |
| Whether `calculate_stamp` can be exercised on a fixture tree without the rest of the engine's environment (`config/functions` 961 reads `PKG_DIR` and the stamp inputs; its helpers may read `BUILD` or `PKG_BUILD`) | Investigate at stage A: read the function and its helpers first, list every variable, then the fixture; if it cannot run in isolation, the finding is made by reading with the line cited and the device-builds.md record (`device-builds.md` § After rebasing, item 3: 35 stale packages on 2026-08-19) as the recorded evidence | the lane, stage A |
| Which `.build-runs/<id>/` records hold a full image run's log (`scripts/image`'s identity lines and timings) rather than a package or QA run | Proceed; the lane lists the M7 worktrees' `.build-runs/` directories with `ls` and reads `build.status`'s first lines to pick the runs (the 2026-10-22 GENERIC_X64 image run and the 2026-10-24 H700 and SM8550 runs), read-only | the lane, stage B |
| Whether the fork CI runs `tools/build-identity-test` (if so, `fork record checks` should already be red for #801's reason; if not, the test has had no runner since `40bc5469b9`) | **Resolved at writing:** `grep -n build-identity-test .github/workflows/fork-checks.yml` prints nothing; the fork CI does not run it, so the test has had no runner since 2026-10-11 and nobody saw it fail. Recorded on #801; the brief's § 5 trial line says so | coordinator; done 2026-10-24 03:05 |
| Whether T3 will post a lead on `mk_es_systems` before T5 reaches it (T3's brief § 5 regenerates the table on the host and will meet the empty formatted file) | Proceed; whichever lane meets it first records it; the fix is T5's by the membership and the brief says so; the coordinator routes T3's lead to #652 | coordinator |

## 3. What patterns from prior work apply that we haven't named?

- **T1's method for scripts without a device**: a failing case before every
  fix under the tools that will run the script (the image's bash and
  busybox for T1; the host's bash for the engine, which the container also
  runs it under), the fixture built at run time with no credential-shaped
  literal (`engineering-practices.md` § Guards must fail closed's fixture
  rule; the push guard rewrote history once, #307), commits cut from
  intermediates after a green run. The brief's `get_env` sandbox is that
  method applied to the engine's one credential-handling line.
- **The retroarch-wrapper-test lesson, twice**: a fork tool whose defaults
  name retired paths (#699 for `es-syntax-check`, #799 for the wrapper
  test, both found by a brief's stranger or a lane's stage A) -- and now
  #801, a fork tool failing because another fork tool grew a gate. The
  pattern is *a tool with no runner decays*; T10's fork CI is where the
  runner belongs, and the brief's § 5 asks which tools the CI runs.
- **T3's host regeneration of the table** (its brief § 5, from its futro):
  the pre-format file through `ElementTree` because `xmlstarlet` is absent;
  T5 reuses the recipe for the same function and adds the `bash -x` trace
  for every sandbox (§ 2 above).
- **#644's method** (`docs/reviews/build-path-read.md` § 5): verify by
  command what a subagent's read claimed, and say which claims were not
  verified; the brief's § 3 inherits the nine findings with their
  dispositions rather than re-deriving them.
- **The 2026-09-19 cold build and blindspot 73** (a monitor of completion,
  not activity): the watcher's design is T9's, but the engine's entry
  points are where it is armed; a reading of `scripts/build` 9 to 12 is a
  reading of D-WORKFLOW-142's mechanism, and the recorded runs are the
  proof it armed.
- **#226 and blindspot 47**: `--wrap-mode=nodownload` is the engine's one
  line against a fetched dependency; #585's candidate contribution
  (D-WORKFLOW-164); T5 keeps it and T3 greps the cores' build systems for
  the cmake equivalent.
- **The release-candidate round of 2026-09-25** (D-WORKFLOW-047): the
  container pin behind upstream's `latest` is the same shape as the
  packages behind their releases that round met; #644's finding 1 names
  the refresh as the coordinator's first act at a base merge. The brief
  records the digests and leaves the move to the coordinator.

## 4. What could we be missing?

**Agent-execution simulation ("what if?" walkthrough):**

> Archetype simulated: a fresh Opus 5.5 lane with the brief, the tree and
> #652, starting with the host free and T3 running beside it.

- **Step: the counts (§ 2).** What if the lane runs the filter in a tree
  without P1's `docs/reviews/inventory.json`? The worktree is stacked on P1
  and the first commands `ls` the file; the brief says so. What if it runs
  `--order` without `--no-write`? The brief forbids it; #652's scope
  paragraph gets the sentence at version 2.
- **Step: the recorded runs.** What if the lane greps a `build.log` for a
  configure line and pastes it into `02-forward-audit.md`? The line carries
  `-DSCREENSCRAPER_DEV_LOGIN=`; the pre-commit scan refuses the commit and
  the transcript holds it. **Plan change:** the brief's filter rule gains
  `LOGIN` (done in version 1) and version 2 adds that every log read goes
  through a shell function the lane defines once (`readlog() { grep -v -i
  -E 'key|pass|token|user|psk|login' "$@"; }`) so no raw `cat` of a log
  reaches an artifact.
- **Step: the sandbox.** What if sourcing `config/options` with `ROOT=$D`
  makes `config/path` compute `BUILD=$D/build.pixelelated-GENERIC_X64.x86_64`
  and a helper `mkdir -p`s it in the lane's worktree? A write in the lane's
  own tree, gitignored, but the next `git status` and the stamp logic are
  confused by it. **Plan change:** § 2's `bash -x` trial, every variable to
  the scratch, any path outside it a FAIL; version 2 writes it.
- **Step: `get_env`'s failing case.** What if the lane's fixture names a
  variable `MY_API_KEY` with the value `hunter2`? The value is harmless but
  the *line* `MY_API_KEY=hunter2` is credential-shaped for the pre-commit
  scan if it lands in a committed script. **Plan change:** the fixture's
  values are the words `fixture-a`, `fixture-b` and the names are built at
  run time (`printf 'MY_API_%s' KEY`), as `engineering-practices.md` § Guards
  must fail closed says; the brief says so, version 2 says it louder.
- **Step: the identity test.** What if the lane runs
  `tools/build-identity-test`, sees `21 passed, 2 failed`, and files the
  engine's identity as broken? **Plan change:** the brief's § 5 trial line
  names the expected result on 2026-10-24 (`21 passed, 2 failed`, the two
  the release-plan half, #801) so the lane's row reads *as expected, #801*
  and the 21 passes are the engine's evidence; a different result is the
  finding.
- **Step: Q4 (b).** What if the lane runs `docker pull` to get the `created`
  label? Forbidden; a pull is a runtime and a multi-gigabyte write. **Plan
  change:** § 2's treatment (digests as the comparison; dates `not read`
  with the commands tried).
- **Step: Q6's call graph.** What if the lane counts callers with `git grep
  -E '\bname\b'` and gets zero for `get_git` because git's default regex
  has no `\b`? The coordinator's own quick scan did exactly that on
  2026-10-24 (zero callers for `get_git`, `get_archive`, `get_file`,
  `uboot_helper`, which `scripts/get` and `scripts/unpack` call through
  `${SCRIPTS}/`). **Plan change:** the brief's Q6 row already prescribes
  `git grep -n -F -e "scripts/<name>" -e "SCRIPTS}/<name>"`; version 2 adds
  `-e "/<name>\""` and says a zero is re-checked with a second pattern
  before it is a row's verdict (blindspot 39's shape: a count that cannot
  fail).
- **Step: the 19 workflows.** What if the lane proposes disabling the
  failing `Build` workflow? That is T10's call (#644 finding 19). **Plan
  change:** none; the brief says so; the lane's row records trigger, state
  and last conclusions and stops.
- **Step: a clarity fix to `scripts/build`.** What if the stream brief
  authorizes a refactor of the hook order or of `config/functions`'s
  helpers "for clarity" and the next M7 build breaks on a package that
  relied on the old order? **Plan change (the pre-mortem below):** version
  2's § 5 never-run list says that a change altering what a build does is
  applied only when the stream brief names the build that proves it and
  the coordinator has scheduled that build; the lane's branch carries
  behaviour-preserving changes with a sandbox proof of equivalence, and
  everything else as `fix-pending-image` rows the stream brief decides.
- **Step: the host window.** What if an M7 window opens while the lane is
  mid-sandbox? The sandbox is a few shell processes, not a compiler or a
  guest; the brief says the window costs this lane nothing but a guest it
  does not expect. **Plan change:** version 2 says a sandbox run that is
  not a compile continues through a window; `npm install` and any compile
  wait.

> Second archetype: the coordinator at integration, two weeks on.

- **Step: merging T5 after T3.** What if T5's fixes to `scripts/build` or
  `config/functions` conflict with the M7 candidate's merge? The M7 delta
  on the membership is none today; the candidate's merge touches
  `projects/` and `.github/sessions/`. What if T3's and T5's branches both
  touch `distributions/ROCKNIX/config/functions`? T3's brief forbids it
  (the file is T5's); the coordinator checks T3's diff at its acceptance.
  **Plan change:** none; recorded here.
- **Step: the first build after the merge.** T5's `fix-pending-image` rows
  are proven at the same build as T1's nine, T2's walks and T3's rows; a
  change to the engine is the one that could break *that* build. **Plan
  change:** the coordinator's integration plan (the pointer's merge notes)
  takes engine fixes last, after the slices whose proofs the build carries,
  so a failing build is attributable; version 2's § 10 names the order.

**Pre-mortem (imagine the work failed 30 days out):**

- **Imagined failure:** on 2026-11-18 the first integration build fails in
  `scripts/build` on a package whose `pre_make_target` ran before its
  `configure` under a hook order T5 "clarified"; three device builds wait
  on a bisect. Root cause: a Q7 finding treated as a fix on a slice branch
  whose only proof was reading; nobody could build. **Plan change:** the
  never-run list above; a behaviour-preserving change proves equivalence by
  a sandbox that runs both versions over the same fixture (`diff` of the
  traces), and a behaviour change waits for a scheduled build.
- **Imagined failure 2:** on 2026-11-05 the punch list has forty shellcheck
  items across the 30 scripts and the 139 fragments were never read against
  the tables; the ccache row says `not measured` and nothing else. Root
  cause: the tool's output taken as the reading. **Plan change:** version
  2's § 4 Q2 says shellcheck's lines are leads read at their site (as T1's
  `02` did) and that a finding needs the site's reading, not the tool's
  code; and § 4 opening keeps the fragments' Q6 first.

**Blindspot check (against `docs/blindspot-register.md`, 74 entries):**

- **14** (a hook proven by a constructed failure) and **26** (a hooks path
  that runs nothing): the fork's `.githooks` are T10's, but the engine's
  entry points' watch marker is a guard too -- the recorded runs are its
  constructed positive (a run that arms; `build.status` exists).
- **39** (a suite passing over a table of dashes): the Q6 call graph's
  zero-caller trap above; the identity test's own `passed`/`failed` JSON
  is the shape done right.
- **47** and **48**: `--wrap-mode=nodownload` and the webkitgtk option log;
  the brief's § 3 cites both.
- **73** (a monitor of completion, not activity): the watcher's design is
  T9's; the engine arms it.
- **74** (a fixture or a stub that silently did not engage): the sandbox's
  `bash -x` trace is the engagement check; a sandbox whose trace shows no
  call of the function under test is a FAIL.
- **13, 46, 51**: the general ones; the brief's § 5 rule 1.
- **No new entry** from this futro: #801's shape (a tool with no runner
  decays) is blindspot 14's and 26's family and is tracked by the issue;
  if T9's reading finds a third fork tool in the same state, the entry is
  written then.

**Replaced-mechanism archetype:** nothing in T5 replaces a mechanism; the
watcher replaced direct entry in October (D-WORKFLOW-142), and that
replacement's record is T9's. Not applicable, said so.

## 5. What adjustments or investigations must happen BEFORE execution?

**Plan edits applied (version 2 of the brief, before dispatch):**

- § 5: the `tools/build-identity-test` trial line names the expected result
  on 2026-10-24 (`21 passed, 2 failed`, the release-plan half, #801) and
  that the engine's 21 identity checks are the evidence; a different result
  is the finding.
- § 5: every log read goes through a `readlog` function with the `LOGIN`
  term; no raw `cat` of a build log reaches an artifact.
- § 5: the sandbox's first run is a `bash -x` trace with every variable set
  to the scratch; any path outside `.qa-scratch/` is a FAIL and grows the
  variable list; a sandbox whose trace shows no call of the function under
  test is a FAIL (blindspot 74).
- § 5: `get_env`'s fixture names are built at run time and its values are
  the words `fixture-a`, `fixture-b`.
- § 4 Q4 (b): the digests are the comparison; the `created` dates are `not
  read` with the commands tried where the registry gives none; never a
  pull.
- § 4 Q5: the ccache row's measurement is `not measured` unless a recorded
  run's log carries ccache statistics; `ccache --show-stats` is never run
  against an M7 root.
- § 4 Q6: the caller search uses fixed strings and a second pattern before a
  zero is a verdict.
- § 5 never-run list and § 10: a change that alters what a build does is
  applied only under a stream brief that names the build proving it; the
  integration order takes engine fixes last.
- § 5: a sandbox run that is not a compile continues through a host window.
- #652's body: the scope paragraph gets the two never-run switches of
  `tools/renovation-inventory`; the criteria replaced by the brief's § 7 as
  version 2 leaves them.

**Investigation tasks opened (the coordinator, before version 2):**

- Whether `fork-checks.yml` runs `tools/build-identity-test` (§ 2 row 6):
  done, above -- it does not.

**Documented unresolved assumptions (proceeding without resolving):**

- The container images' `created` dates may stay unread; the digests
  decide same-or-different and the Makefile's commit and #644's dating
  stand in. Rationale: the refresh is the coordinator's act either way.
- The ccache comparison may stay a reading of settings. Rationale: a
  measurement needs a build the program does not run.
- T3 and T5 run beside each other with one function file shared by
  reference; T3's brief forbids its edit. Rationale: D-WORKFLOW-190's
  "two slices never share a path" holds by the membership; the
  coordinator checks T3's diff at acceptance.

**Blindspot register updates:**

- None. #801 tracks the tool-without-a-runner shape; an entry is written
  if T9's reading finds the shape a third time.
