# Brief: M6.P2 T6, upstream's helper tools and the other distributions (#653)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command, then this brief whole.
Every section below is mandatory; a section that does not apply says so and
why. Where this brief and the checklist on #653 differ, #653 wins and the
coordinator corrects the brief in the same session. **Version 1
(2026-10-24):** written after T1 to T5's briefs had each been through a
futro and a stranger's proof (plan § 3, principle 3), and after T5's audit of
the engine these tools belong to (#837, closed 2026-10-24), so the shapes
those found wrong -- a count from the wrong tree, a tool absent from the
host, a line number from memory, a command whose variables do not survive a
Bash call -- are answered from the start, and every figure below was
produced by a command at `8ebaf8daad` unless it says *branch*. It goes
through a stranger's proof before dispatch; version 2 records what it found.
**Each command block sets its own variables** (`D`): a Bash call in this
harness starts a fresh shell. **This is a table slice**: it reads rows, one
per path, for reachability; it reads no file line by line unless a row needs
it, and it removes nothing upstream carries.

## 1. Identity

- **Issue:** #653 `M6.P2 E800/T6: build-engine: upstream's helper tools and
  the other distributions`, slice `build-engine-upstream-tools` (`k: 6`) in
  `docs/reviews/slices.json`, sixth in `docs/reviews/order.md` (its sizing
  row: `| 6 | upstream's helper tools and the other distributions |
  build-engine | table | reachability | 135 | 7,369 | -- (135 rows) | 0 |
  Local |`; the slice's `why`: *"upstream tools (`distro-tool`, `mkpkg`, ...)
  the fork may never run, and `distributions/LibreELEC` and `LEIoT`, which
  nothing selects; with the build engine, so the engine is read whole before
  anything it builds (D-WORKFLOW-186 ...)"*). **Epic:** #800 (the build
  engine: T5 #652 accepted 2026-10-24, this slice), whose futro
  (`docs/futros/2026-10-24-m6-build-engine.md`) covers T6's order and gains
  a kickoff addendum with this brief's version 2. **Milestone:** M6; its body
  holds the live order; read it first. **Predecessors:** #346 (the plan),
  #641 (the survey), #644 (the build-path read: its finding **24** is this
  slice's -- *"LibreELEC's `tools/update-scan`, `update-pkg`, `distro-tool`,
  `refresh-patches` are carried and unused by any ROCKNIX workflow"*, marked
  *candidate*), **T5 #652** (the engine, accepted: its audit folder
  `docs/audits/2026_10_24-epic-m6-build-engine/` on
  `feature/m6-build-engine-652` at `52e6794ba7` is this slice's nearest
  reading -- its coverage table, its Q6 tables and its E8 stream touched
  `tools/mtstats.py`'s caller and `scripts/update_packages`, which calls
  `tools/update-functions`). **Beside it:** T30 (#677, the standalone
  emulators) runs in the other lane (D-WORKFLOW-190); the two share no path.
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, or decide a
  question of scope: those are the coordinator's, reached through #653, one
  question at a time. What it does file: its own audit punch-list issue
  (stage D) and a `bug` issue for every defect it finds (D-WORKFLOW-187).
  Nothing else.
- **One worktree, one session.** Branch `feature/m6-build-engine-upstream-tools-653`
  at `/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the two hashes are in the dispatch comment on #653). **Before that
  comment exists there is no worktree at that path and none of the first
  commands can run.** The session is the T5 lane's (`m6-t5-build-engine`,
  pane `wN:p7`), which knows the engine; its T5 worktree stays beside this
  one, idle, until the merge, and nothing is written there. The primary
  checkout `/workspace/repos/pixelelated/distribution` stays on `next`
  (D-INFRA-025); the legacy checkout and `rocknix.worktrees/*` are the M7
  lane's, read only; the T1 to T5 worktrees are other lanes', `git -C` only.
  **The rules in this worktree are `next`'s except six files** (P1's
  `fork-workflow.md` and `instruction-files.md`; the coordinator's
  `generic-x64-vm-testing.md` paragraph `8c9b1d4721` and
  `engineering-practices.md` bullet `ab8f750784`; M7's
  `.claude/skills/council/IMPORTED-FROM.md`; and `tools/lint-audit-artifacts`
  with `templates.md` from #810, which this slice's lint needs). Known stale
  facts in the rules (the legacy layout in eight files, #640) do not cost an
  hour here: every rule the work touches is named in § 3.
- **Model and effort:** Opus 5.5 at high effort (the maintainer, 2026-10-22).
  Record what ran in `00-running-log.md`'s header.
- **Review depth: Local** (plan § 6c: *"a dead-end table ... Local: the
  executor alone; the lint and the counts are the check"*; D-WORKFLOW-184).
  No external reviewer, no `npm install`, no Facilitator call.
  `second-opinions/review-plan.json` is still written: depth `local`,
  primary `anthropic/claude-opus-5-5`, lab `anthropic`, reviewers `[]`,
  **`"tier_exception": "D-WORKFLOW-184"` and `"reason": "plan § 6c: a
  reachability table is Local"`** -- the two keys #810 taught
  `tools/lint-audit-artifacts` to accept in an `-epic-` folder (its line
  prints `review-plan: local at epic tier under D-WORKFLOW-184 (...)`).
  Phase 4.6 is recorded as not applicable with the plan's row cited; Phase
  4.5 is done in full, and § 5's rule 4 -- what result would have produced
  a FAIL -- is asked of every PASS, because nobody else asks it here.

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-build-engine-upstream-tools-653
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: this is not the lane's worktree (stacked on P1): stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # the six files § 1 names, nothing else
mkdir -p .qa-scratch/t6/at-hash && git archive 8ebaf8daad tools distributions | tar -x -C .qa-scratch/t6/at-hash   # the read tree: every row is this tree's unless marked branch (A1)
ls tools/renovation-inventory tools/renovation-status tools/renovation-drift docs/reviews/slices.json docs/reviews/cross-reference.md   # P1's
"$D/tools/rules-check"; echo "rc=$?"; "$D/tools/register-check"; echo "rc=$?"; "$D/tools/ceremony-check"; echo "rc=$?"   # rc 1 on 2026-10-24: W42 OVERDUE (M7's week), a retro DUE; neither is this lane's
git push -u origin feature/m6-build-engine-upstream-tools-653
test -f docs/reviews/briefs/build-engine-upstream-tools.md || { echo "the brief is not in this tree: stop"; exit 1; }
cat .github/sessions/saved-session-state-feature-m6-build-engine-upstream-tools-653.md
tail -3 /tmp/m7-m6-host-coordination-20261023.txt                   # the host's state: this slice needs no runtime, but the protocol is read
df -i /tmp | tail -1                                                 # never export a tree under /tmp: the tmpfs ran out of inodes on 2026-10-24
```

## 2. Scope

**135 paths, 7,369 lines; 134 upstream-carried and 1 fork-own; 108
`reach: n/a` and 27 `unreached`; every row read, no line read unless a row
needs it.** The membership is the inventory's at P1's `eb4763e3cc`, with
the slice's rule (`k: 6`): the rows of the `build-engine` area under
`tools/**` and `distributions/**` less `distributions/ROCKNIX/**`. **The
area filter is what keeps the fork's own tools out**: `tools/` holds 139
entries at `8ebaf8daad`, of which the inventory assigns the fork-only ones
(`tools/vm-qa`, `tools/cloud-*`, `tools/council/`, ... -- the list in
`fork-workflow.md` § Personal paths) to `tooling-and-guards` (T9/T10) and
upstream's to `build-engine`; a path under `tools/` that is not in this
slice's 135 is not this slice's, however much it looks like a tool. The
re-derivation:

```bash
python3 -I - <<'PY'
import json, re, collections
inv = json.load(open("docs/reviews/inventory.json")); cols = inv["columns"]
rows = [dict(zip(cols, r)) for r in inv["rows"]]
def gm(p, g): return re.fullmatch(re.escape(g).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*"), p) is not None
t6 = [r for r in rows if r["tree"] == "distribution" and r["area"] == "build-engine"
      and any(gm(r["path"], g) for g in ["tools/**", "distributions/**"]) and not gm(r["path"], "distributions/ROCKNIX/**")]
L = lambda rs: sum(r["lines"] or 0 for r in rs)
print("paths", len(t6), "lines", L(t6), dict(collections.Counter(r["tier"] for r in t6)), dict(collections.Counter(r["reach"] for r in t6)))
print(dict(collections.Counter(r["language"] for r in t6)))
for r in sorted(t6, key=lambda r: r["path"]): print(r["reach"], r["tier"], r["lines"], r["path"])
PY
git ls-tree -r --name-only 8ebaf8daad -- tools distributions | grep -v '^distributions/ROCKNIX/' | wc -l    # every tracked path under the two roots less ROCKNIX's; the slice's 135 are those the inventory puts in build-engine
```

Recorded (2026-10-24, at `eb4763e3cc`'s inventory, the tree at
`8ebaf8daad`): **135 paths, 7,369 lines**; tiers upstream-carried 134,
fork-own 1 (`tools/pkgcheck` -- the inventory's tier, where `CLAUDE.md` and
`instruction-files.md` call it *upstream's*: the first row to settle, by
`git log` on the file against `upstream/next`); reach `n/a` 108, `unreached`
27 (the 27 are every file of `distributions/LEIoT/` (11) and
`distributions/LibreELEC/` (16): nothing selects a `DISTRO` but ROCKNIX);
languages shell 37, none 66, image 17, docker 6, python 3, other 2, config
1, font 1, markdown 1, symlink 1. **The groups:** `tools/update-functions/`
62 files (LibreELEC's per-package update helpers, read by
`tools/update-pkg`/`update-scan`, which nothing here calls), `tools/mkpkg/`
10, `tools/docker/` 7 (six Dockerfiles for other distributions' containers
and a README; the fork's own container is the root `Dockerfile`, T5's),
`distributions/LibreELEC/` 16, `distributions/LEIoT/` 11, and 29 single
tools (`adjust_kernel_config`, `change_addon_version`,
`check_kernel_config`, `checkunpack`, `dashboard`, `distro-tool`,
`download-cleaner`, `download-tool`, `ffmpeg/gen-patches.sh`,
`find_build_warnings.sh` with its `.conf`, `fixlecode.py`, `icon-generate`,
`imgburn.sh`, `moby/gen-patches.sh`, `mtstats.py`, `packages-checker`,
`pkgcheck`, `pkginfo`, `podman-bin/gen-patches.sh`, `refresh-patches`,
`repo-tool`, `RPi/gen-rpi-kodi-patch.sh`, `RPi/rpi-kodi-rebase.sh`,
`update-pkg`, `update-scan`, `upload_to_filebin`, `viewconfig`,
`viewplan`). **A first caller count the slice redoes properly** (`git grep
-l -F "tools/<name>"` over `Makefile scripts config .github distributions
projects packages`, at the hash): `refresh-patches` 1, `pkgcheck` 1,
`adjust_kernel_config` 2, `mtstats.py` 1; `distro-tool`, `mkpkg`,
`update-scan`, `update-pkg`, `viewplan`, `dashboard` 0 -- a count by one
pattern over one set of roots, which is the lead, not the row; the row's
search is § 4 Q6's.

**The hash.** The slice's bytes are `8ebaf8daad`'s; `reviewed-at:` is the
branch `HEAD` at stage A; the read is made on the at-hash tree
(`.qa-scratch/t6/at-hash`, the first block). The branch differs from the
hash on none of the 135 on 2026-10-24 (T5's streams touched `scripts/` and
`config/`, not `tools/` or the other distributions -- the lane confirms with
`git diff --stat 8ebaf8daad HEAD -- tools distributions ':!distributions/ROCKNIX'`,
and a non-empty result is the first lead).

**Where these run.** A tool under `tools/` runs when something calls it:
the `Makefile` (none of the 135 on 2026-10-24 by the first count),
`scripts/*` (`scripts/build` calls `tools/pkgcheck`? -- the row says;
`config/multithread` pipes to `tools/mtstats.py`, T5's E8 made that
step's failure harmless; `scripts/update_packages` calls
`tools/update-functions/<pkg>` by name when a recipe has one), a kernel
recipe (`adjust_kernel_config`, `check_kernel_config` from
`packages/linux/package.mk` or a device's), a workflow under
`.github/workflows/` (upstream's -- `update-kernel-configs-docs.yml` is
T10's PL-15 of T5's list), a developer by hand (documented in
`CLAUDE.md`, `AGENTS.md`, a rule, `packages/README.md`, `tools/docker/README.md`
-- a documented hand-run tool is *reached by a document*, a row class of
its own), or nothing. `distributions/<name>/` is read by `config/options`
when `DISTRO=<name>`; the fork sets `DISTRO=ROCKNIX` everywhere
(`distributions/ROCKNIX/options`, the `Makefile`), so LibreELEC's and
LEIoT's files are reached by no build the fork can make, and by upstream's
only where upstream builds those distributions -- which ROCKNIX does not.

**The policy on removal (plan § 5, D-UI-079's spirit for the engine):**
**an upstream-carried file is not removed by this slice.** Every base merge
would re-raise it, and `#644` finding 24 marks the class *candidate*: a
proposal to ROCKNIX (#585, D-WORKFLOW-164) to drop the tools no ROCKNIX
workflow runs, carried by the fork only after upstream takes it. The table
therefore says for each row *reached by X* or *unreached*, and for an
unreached upstream-carried row its disposition is `kept: upstream's; #585
candidate` with an `Already written:` line (what a developer who has run it
by hand left behind -- usually nothing). **A fork-own row** (one today) is
read line by line and dispositioned as a code row: kept with its callers
named, or changed under a stream brief.

**Drift.** `next` is `8ebaf8daad`; the M7 candidate's merge moves it after
this slice; the coordinator merges `next` into the branch never between
stage A and stage D, and re-baselines after. `tools/renovation-drift` is
the coordinator's; this lane runs it to read.

## 3. Read first

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; what runs on this host, not a work queue) and this lane's own
  pointer.
- **The rules this work touches** (`working-principles.md` § Pre-flight:
  open them, say which were read): `engineering-practices.md` (§ Verify the
  artifact; § A name is not a behaviour; § Before deleting a duplicate --
  the test for every *unreached* verdict: what the file guarded, stamped or
  documented that nothing else does; § Consider contributing every
  applicable fix upstream, D-WORKFLOW-164/165), `device-builds.md` (§ After
  rebasing items 2 and 3 are T4's to correct, #651; the `make` targets and
  what they call), `packaging-and-patches.md` (what `tools/pkgcheck` checks
  and why every `package.mk` edit runs it), `fork-workflow.md` (§ Personal
  paths: the fork-only tools, which are *not* this slice's), `instruction-files.md`
  (§ The fork's own tools: the table that says `pkgcheck` is upstream's),
  `bugs-are-agent-first.md` (rule 6: an upstream defect contained is ours
  to close), `upgrade-and-install.md` (`Already written:` for every
  disposition), `issue-tracking.md`, `vm-first.md` (§ 5 answers it: no, a
  table runs no guest), `worktrees.md` (the layout, superseded by § 1).
- The code-auditor skill whole (`SKILL.md`, `references/phases.md`,
  `review-levels.md`, `templates.md`, `anti-patterns.md`); the renovation
  face is plan § 6b; the Local depth plan file is § 1's.
- **T5's audit** (`docs/audits/2026_10_24-epic-m6-build-engine/` at
  `52e6794ba7`, read with `git -C` or `git show`): its `02-forward-audit.md`
  coverage rows for `scripts/update_packages` (E6 changed it: it keeps
  checksums and refreshes one from a verified fetch; it calls
  `tools/update-functions/<pkg>` -- the row that decides whether the 62
  helpers are reached), `config/multithread` (E8: `tools/mtstats.py`),
  `scripts/build` (does it call `tools/pkgcheck`?), its Q6 tables
  (`q6-tables.md`) for anything under `tools/` it already dispositioned,
  and PL-15 (`update-kernel-configs-docs.yml`, deferred to #657) and PL-26
  (`scripts/test-audit-review.py` in the wrong area). **T3's audit** for
  `tools/retroarch-wrapper-test` (#799, fork-only: not this slice's) as the
  shape of a tool row. **T1's** for nothing here.
- **`docs/reviews/build-path-read.md`** (#644): finding 24 whole, and its
  table's column for *both carry dead tooling*; the other 25 findings named
  with their carriers so none is taken here.
- `docs/blindspot-register.md` whole once (75 entries on the branch, 74 at
  the hash under the numbers 1 to 73 and 74), then **13** (assumed done),
  **22** (a probe that cannot report absence: a caller search that returns
  nothing because the pattern was wrong is this shape -- every zero is
  searched a second way before it is a row), **46** (a name read as a
  behaviour: a tool's name is not its reach), **51**, **75** (a corpus read
  on the wrong tree).
- Decisions by ID: D-WORKFLOW-184 (Local for a table), D-WORKFLOW-186 (the
  engine first), D-WORKFLOW-187 (no release gate; every defect a bug),
  D-WORKFLOW-164/165 (upstream contributions prepared, submissions held),
  D-WORKFLOW-024 (`tools/fork-package-freshness`: the fork's own packages
  current -- not this slice's packages, but its tool is T9's), D-UI-079
  (change inside the fork's lanes: the engine's upstream tools are outside
  them, which is why the policy above is *table, propose, do not delete*),
  D-INFRA-025/026, D-WORKFLOW-193/194 (T5's fetch policy: `tools/update-pkg`
  and `update-scan` write checksums -- do they still agree with it?).
- Issues: #653 (this), #652 (T5, accepted), #644/#645, #657 (T10: the
  fork's tooling slice, where a fork-only tool's defect goes), #585 (the
  contribution queue: finding 24's row lands there), #226 (a build that
  fetched its own dependency: the class `tools/update-*` touch), #810 (the
  lint's Local-at-epic rule), #809 (the inventory's renderings). Every `gh`
  call carries `--repo pixelelated/distribution`.

## 4. The questions

All seven apply (plan § 4); for a reachability table Q6 is the spine and
Q1, Q4 and Q7 hang off it; Q2, Q3 and Q5 apply in full to the one fork-own
row and to every row a search finds reached.

| # | Question, for this slice | Evidence |
| --- | --- | --- |
| Q1 Modernize | A reached tool that runs a retired mechanism: a `tools/docker/*/Dockerfile` for a container the fork never builds (its own is the root `Dockerfile`); `tools/update-*` writing a recipe shape (`PKG_SHA256` handling) that T5's E6 changed under it; a tool calling a `scripts/*` entry point T5 renamed or guarded | the caller's line and the callee's current shape, side by side |
| Q2 Standards | For the fork-own row and every reached shell tool: `bash -n`, shellcheck where the host has it (it does not: record *not runnable*), the late-binding rule where a tool sources `package.mk` (`tools/pkgcheck` is the tool that enforces it on others: does it obey it?), upstream's own header conventions kept | the command and its output per row |
| Q3 Bugs | A reached tool that lies: `tools/pkgcheck` passing a shape it should fail (T3's S1 found it does catch global-scope `PKG_BUILD`; the slice names what it does not catch, as a lead for #657, not a rewrite here); `adjust_kernel_config` or `check_kernel_config` mis-reading a config under the kernels the fork builds; `tools/mtstats.py` on a `history` file T5's E8 now tolerates failing; a tool that `set -e` leaves half-run | the artifact: a fixture under `.qa-scratch/t6/` that shows the wrong answer, and the one that will show the right one; every finding a `bug` with its VM line (*No -- the tree and a fixture show it*) |
| Q4 Currency | Against upstream, for every upstream-carried row: `git diff --stat upstream/next -- <path>` (identical, or the fork changed it -- and if changed, why: `git log <path>` on both sides); against the fork's own record for the fork-own row; `tools/pkgcheck`'s tier settled (fork-own by the inventory, upstream's by two rules) | one table: path, identical/differs, the fork's commits if any |
| Q5 Efficiency | What a reached tool costs a build (`tools/pkgcheck` runs where? `mtstats.py` after every multithread build) and what an unreached one costs a reader (7,369 lines carried, 27 files of two distributions in every checkout); no time-to-play question: nothing here is on an image | the lines per group; a sentence per reached tool on when it runs |
| Q6 Dead ends | **The table**: one row per path (135) -- or one per tool with its files grouped where a tool is a directory (`mkpkg/`, `update-functions/`, `docker/`, `RPi/`, the three `gen-patches.sh` dirs), with the per-file count in the row -- each with its callers searched **two ways** (fixed-string `git grep -F` for the path and for the bare name, over `Makefile scripts config .github distributions projects packages docs .claude CLAUDE.md AGENTS.md packages/README.md`; a zero on the first pattern is re-searched with the second before it stands, blindspot 22), its verdict (`reached by <callers>` / `reached by a document only` / `unreached`), its tier, its upstream state (Q4), and its disposition: `kept: called by ...`, `kept: upstream's, unreached; #585 candidate`, `kept: documented hand-run tool`, or for the fork-own row a code disposition. **Every `unreached` row carries `Already written:`**: what a developer who ran it left in a tree or a cache (`tools/download-tool` writes to `sources/`; `distro-tool` to `release/`?) and whether anything in a build root today was made by it | `04` § Q6 holds the table; `02`'s coverage table has the same 135 rows with Q1 to Q7 cells |
| Q7 Clarity | Two tools that do one job (`update-pkg` and `update-scan` against `scripts/update_packages`; `pkgcheck` against `packages-checker`); a tool whose header says what it no longer does; `tools/docker/README.md` against the fork's `make docker-*` route (`device-builds.md`) | the pair named with the diff of their claims |

A finding is one question with its evidence; `Renovation` is the category
for Q1, Q5, Q6 and Q7 items that are not defects. A Q3 finding is a `bug`
(D-WORKFLOW-187).

**The ladder (`working-principles.md` § Enforcement depth):** the table's
own guard is #838's cousin -- *is there a check that a tool the table calls
unreached has stayed unreached?* -- which the slice proposes (an issue, the
coordinator files) rather than builds.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor; the file numbers its fifth rule `3.`, #685's lead):

1. Tracker state is never sole evidence: every verdict cites the tree
   (`git grep`, `git log`, `git diff`), a fixture's run, or a document's
   line.
2. Mechanical evidence outranks reading: a caller is a `git grep` hit with
   its file:line, not a memory of how the build works.
3. **For a table, the target is the tree and the record**: a tool is
   *reached* when a line in the tree calls it; a tool is *run by a document*
   when a rule or README tells a person to run it; the build roots on the
   host are read for what a tool left (`release/`, `sources/`, a stamp) --
   **read only, from the M7 roots, through the filter, never a process
   started there**. No guest: a table runs nothing on a guest, and nothing
   here is on an image (§ 2). No build.
4. An assertion that cannot fail is not evidence: before a row says
   *unreached*, the two patterns were run and one of them found something
   somewhere (the row names a reached tool found by the same command, as
   its own positive control).
5. Subagent output is a lead, never evidence; fan-out is read-only
   research only (D-WORKFLOW-183).

**What runs on the VM, and how.** Can this be done on the VM? **No** -- the
slice is a reachability table over tools and files that are not on an
image; its bench is the tree, the record and the M7 build roots read-only.
Nothing here touches a handheld, a person's cloud, a shared QA backend, a
QA guest or a build. The host handoff file is read for the protocol alone.

- **The host-side checks**, each run with its command, exit status and
  summary line in `02-forward-audit.md`; a check that cannot run is
  recorded as such, never as a pass:
  ```bash
  D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-upstream-tools-653
  cd "$D"; mkdir -p .qa-scratch/t6
  git diff --stat 8ebaf8daad HEAD -- tools distributions ':!distributions/ROCKNIX'          # empty on 2026-10-24: the branch carries the hash's bytes for the 135
  for p in $(git ls-tree -r --name-only 8ebaf8daad -- tools distributions | grep -v '^distributions/ROCKNIX/'); do printf '%s %s\n' "$p" "$(git diff --quiet upstream/next 8ebaf8daad -- "$p" && echo identical || echo differs)"; done > .qa-scratch/t6/q4-upstream.txt; grep -c differs .qa-scratch/t6/q4-upstream.txt   # Q4: which of the two roots' files the fork changed; the slice keeps the 135 of them
  for t in distro-tool mkpkg update-scan update-pkg refresh-patches pkgcheck adjust_kernel_config check_kernel_config mtstats.py viewplan viewconfig dashboard download-tool download-cleaner pkginfo packages-checker checkunpack repo-tool fixlecode.py icon-generate imgburn.sh upload_to_filebin change_addon_version find_build_warnings.sh; do printf '%-24s path:%s name:%s\n' "$t" "$(git grep -l -F "tools/$t" 8ebaf8daad -- Makefile scripts config .github distributions projects packages docs .claude CLAUDE.md AGENTS.md | wc -l)" "$(git grep -l -w -F "$t" 8ebaf8daad -- Makefile scripts config .github distributions projects packages | wc -l)"; done   # the two-way caller count per single tool; the directories (mkpkg, update-functions, docker, RPi, the gen-patches dirs) by their callers' names
  git grep -n -F 'tools/update-functions' 8ebaf8daad -- scripts config | head          # the 62 helpers are reached through update_packages or not at all
  git grep -n -E 'DISTRO=|DISTRO:=' 8ebaf8daad -- Makefile config scripts distributions | head   # what selects a distribution: the two others are reached by nothing the fork runs
  for f in $(git ls-tree -r --name-only 8ebaf8daad -- tools | grep -v '^tools/update-functions/' ); do case "$f" in *.py) python3 -I -m py_compile "$f" >/dev/null 2>&1 && echo "py ok $f" || echo "py FAIL $f";; *) head -1 "$f" | grep -q 'sh$' && { bash -n "$f" >/dev/null 2>&1 && echo "sh ok $f" || echo "sh FAIL $f"; };; esac; done | grep -c ok   # Q2 over the shell and python tools of the slice (only those the inventory lists; the fork-only ones are T10's)
  ls /workspace/repos/rocknix.worktrees/*/release 2>/dev/null | head; ls /workspace/repos/rocknix.worktrees/*/sources 2>/dev/null | head -3   # read only: what a hand-run tool left in the M7 roots, for Already written:
  ```
- **A read is free and goes through the filter** (`grep -v -i -E
  'key|pass|token|user|psk|login'` on any log or config read from an M7
  root). The wordlist (`~/.config/rocknix/forbidden-terms`) is never read.

**What never runs in this slice:** a build; a guest; a command on a
handheld, a cloud or a shared backend; a process in an M7 worktree; a
model call outside `tools/council/run` (none expected: Local); `npm
install`; a deletion of an upstream-carried file (§ 2's policy: table,
propose on #585, do not delete); an edit at stage B (a finding is a row;
the edit waits for its stream brief); `--no-verify`; bare `git stash`;
`git worktree remove --force` or `rm -rf` of any worktree; a write in
another lane's worktree or under `/workspace/repos/rocknix*`; a tree export
under `/tmp` (use `/workspace/tmp/m6-t6/` after `df -i`); a change to the
order, the slices, the plan, this brief, #653's criteria or the M6 body
(D-WORKFLOW-189); a GitHub issue other than the audit punch-list issue and
`bug` issues.

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#653`
(`Refs #653`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-build-engine-upstream-tools/00-running-log.md` | the skill's flight recorder: the model and effort, `reviewed-at` with `8ebaf8daad` beside it, every command with its exit status and time (stamped from `date -u`, never typed), each stage's entry; **every check that stands as a proof on a line that begins `PROOF:`** (criterion 12's token); each stage-B session's last line records `git status --short -- tools distributions` empty | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 135 re-derived with § 2's filter and its output, the branch's deltas from the hash (none expected), the Q4 upstream-state count; § Phase 1: #644 finding 24 whole, T5's rows that touch this slice (`update_packages`, `multithread`, `build`), the two rules' *upstream's* against the inventory's *fork-own* for `pkgcheck` | A, B |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #653's checklist, plus **a coverage table with one row per path** (135; the first cell the path in backticks so ``grep -c -E '^\| `(tools/|distributions/)' 02-forward-audit.md`` prints 135; Q1 to Q7 each answered or `n/a` with a reason); § Mechanical checks (every check of § 5 with command, exit status, summary); § The #644 finding (24 with its disposition; the other 25 named with their carriers); § Proofs with a `proved:` cell each | B onward |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: `tools/update-*` x `scripts/update_packages` (T5's E6) x D-WORKFLOW-193; `tools/mtstats.py` x `config/multithread` (E8); `tools/pkgcheck` x `packages/README.md` x `packaging-and-patches.md`; `tools/docker/*` x the root `Dockerfile` x the `Makefile`'s pinned digest; the futro's predictions checked | B |
| Analysis | `.../04-analysis.md` | Phase 4, § Finding Verification (4.5 in full), **§ Renovation face** Q1 to Q7 (all seven required), **Q6 carrying the reachability table** (one row per path or per tool-directory with its file count, the two-way search per row, the verdict, the tier, the Q4 state, the disposition, `Already written:` on every unreached row); § Second opinions reads *not applicable at Local depth (plan § 6c, D-WORKFLOW-184)* | B, C |
| Second opinions | `.../second-opinions/review-plan.json` | § 1's Local plan file with `tier_exception` and `reason`; no call, no provenance file | C |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts`, with the line `review-plan: local at epic tier under D-WORKFLOW-184 (...)` in its output, both recorded | C to D |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category (`Renovation` where not a defect), where (file:line at `8ebaf8daad`), acceptance; the YAML `punch_index`; the #585 candidates grouped (finding 24's tools) as one `Renovation` item whose outcome is *proposed on #585*; a defect in a fork-only tool is not this slice's and is routed to #657 as a lead | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #653 | `Audit: M6 T6 upstream's helper tools and the other distributions -- N findings (...)`; one checkbox per item, agent-verifiable; `tools/box-check --issue N` once | D |
| Bug issues | GitHub, label `bug`, `Bug:` title, milestone-less | one per defect (D-WORKFLOW-187): the code trace shape, `Already written:`, the VM line (*No -- the tree and a fixture show it*), an agent-verifiable criterion | D |
| **The stage-D pause** | #653 | the punch list posted with the audit issue's and the bugs' numbers; the lane waits for the coordinator's stream briefs (plan § 6b E; D-WORKFLOW-189) -- meanwhile it drafts the retro's four answers and edits nothing of the 135 | D to E |
| Remediation | the branches the stream briefs name | each stream as its brief says; **no upstream-carried file deleted**; a fork-own change with the test first | E |
| Verification | `02-forward-audit.md` appended; `audit-completion.json` after the coordinator closes the audit issue | every proof's `proved:` cell one of `tree`, `history`, `fixture`, `fix-tree`, `fix-pending-session`; `grep -c 'proved:' 02` = `grep -c '^PROOF:' 00` | F |
| Retro | `docs/retros/<yyyy-mm-dd>-m6-build-engine-upstream-tools.md`, posted on #653 | the mini-retro's four answers with its scoped audit; **what the slice did to the two time-to-play numbers** (nothing: no path here is on an image; in those words) | G |
| Hand-back | #653 | `reviewed-at:` and `fixed-at:` in the body; one comment: the tip, each artifact by path, the six checker exit codes, each fix's `proved:` class | H |
| Lane pointer | `.github/sessions/saved-session-state-feature-m6-build-engine-upstream-tools-653.md` | seeded by the coordinator; updated at every checkpoint | every checkpoint |
| Work log | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#653`, stamped from the clock | every session |

## 7. Acceptance

The checklist on #653 is the contract (its body carries these sixteen,
written there with version 2 in place of the five generated ones; where
the two differ, #653 wins and the coordinator corrects the brief). Each
names the artifact that ticks it; the coordinator ticks at hand-back.

- [ ] `docs/audits/<date>-epic-m6-build-engine-upstream-tools/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-build-engine-upstream-tools/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included and the line `review-plan: local at epic tier under D-WORKFLOW-184` in its output.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []`, `tier_exception: D-WORKFLOW-184` and a `reason` naming plan § 6c's row.
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (#585 for the upstream candidates, #657 for a fork-only tool's defect), or withdrawn with its reason.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits the read and the fixes were made at (the read on `8ebaf8daad`'s bytes; no EmulationStation path), and, after the coordinator closes this issue and the branch merges to `next`, `tools/renovation-status` lists this slice as `closed`.
- [ ] `01-research-notes.md` § Scope records the read hash, the filter of brief § 2 with its output (135 paths, 7,369 lines; 134 upstream-carried, 1 fork-own; 108 `n/a`, 27 `unreached`, or the deltas beside them), and `git diff --stat 8ebaf8daad HEAD -- tools distributions ':!distributions/ROCKNIX'` (empty, or each hunk listed with its owner).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path, the path in backticks as the first cell: ``grep -c -E '^\| `(tools/|distributions/)' 02-forward-audit.md`` prints 135; each row's Q1 to Q7 cells answered or `n/a` with a reason.
- [ ] `02-forward-audit.md` § Mechanical checks records, with command, exit status and summary line, each of: the branch-vs-hash diff on the two roots, the Q4 upstream-state loop with its `differs` count, the two-way caller count for every single tool, the `tools/update-functions` and `DISTRO=` greps, and the `bash -n`/`py_compile` sweep with its ok count; a check that could not run (shellcheck) is recorded with the reason, never as a pass.
- [ ] `04-analysis.md` § Renovation face Q6 carries the reachability table: one row per path (or per tool directory with its file count, the sum 135), each with the two search commands' hit counts, the verdict (`reached by <file:line>` / `reached by a document only <file:line>` / `unreached`), the tier, the Q4 state, and the disposition; **every `unreached` row carries an `Already written:` line**, and no upstream-carried row's disposition is a deletion.
- [ ] `04-analysis.md` § Renovation face Q4 carries the upstream-state table (135 rows: identical to `upstream/next` at `8ebaf8daad`, or differing with the fork's commits named) and settles `tools/pkgcheck`'s tier with the commands that decide it (`git log --oneline upstream/next..8ebaf8daad -- tools/pkgcheck`, `git diff --stat upstream/next 8ebaf8daad -- tools/pkgcheck`), naming which document is wrong if the rules and the inventory disagree.
- [ ] `02-forward-audit.md` § The #644 finding carries finding 24 with its disposition (the tools it names, each row's verdict, the #585 proposal's text) and names the other 25 findings with their carriers so none is taken here.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `fixture`, `fix-tree` or `fix-pending-session`; ``grep -c 'proved:' 02-forward-audit.md`` equals ``grep -c '^PROOF:' 00-running-log.md``.
- [ ] Every punch item carries `question:`; the upstream candidates of finding 24's class are one `Renovation` item whose outcome names the #585 comment; every `bug` this lane files passes `tools/box-check --issue N`; no file under `tools/` or `distributions/` is changed on this branch before a stream brief (`git diff --stat 8ebaf8daad <fixed-at> -- tools distributions` shows only stage-E commits).
- [ ] No upstream-carried file is deleted on this branch (`git diff --diff-filter=D --name-only 8ebaf8daad <fixed-at> -- tools distributions` is empty, or every deleted path is fork-own with its `Already written:` on the punch list).
- [ ] The retro exists at `docs/retros/<date>-m6-build-engine-upstream-tools.md`, is posted on #653, and says in those words that the slice did nothing to the two time-to-play numbers.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge, and `tools/lint-audit-artifacts` prints `PASS` on the folder; the six exit codes pasted on #653.

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #653; a blocker named on #653 with what is needed (a count that cannot
be produced, two commands that disagree, a tool that will not run); a
branch that differs from `8ebaf8daad` on one of the 135 at stage A in a
hunk the dispatch comment did not name; or an execution limit, stated as
such with the running log current. A checkpoint is not a stop; a differing
count is a delta; `next` moving is drift. An idle session says it is idle
on #653, **and does not end a turn on a post that asks nothing**.

## 9. Ceremonies owed

- A work-log entry per session headed `#653`, its time from `date -u` in
  the same command; `tools/work-log-index --write` after it.
- A friction line the moment something slows, with `issue: #653` or the
  guard.
- The VM question written before any proof (§ 5: no; the tree and the
  record are the bench).
- The mini-retro at stage G, posted on #653, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator (D-WORKFLOW-189).
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-24 the highest Decided row is D-WORKFLOW-194, the coordinator's;
  T30 runs beside this lane and may take 195); it goes at the end of `##
  Decided`.
- `tools/ceremony-check` before every push; what another lane owes (the
  W42 summary, M7's) is noted, not paid. Never `--no-verify`. A merge with
  conflicts is checked for markers (#696); the ledgers are united by whole
  entries. **A commit names its paths** (`git add -- <files>`, `git status
  --short` read before each commit as well as after); **a tree export goes
  under `/workspace/tmp/m6-t6/` after `df -i`, never under `/tmp`**.
- Commit messages `docs: ...` for the audit and `<tool>: ...` for a tool
  change, with `Refs #653`.

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#653's checkboxes against their artifacts; the lint's `PASS` line with the
`D-WORKFLOW-184` line beside it; `review-plan.json`; the audit issue's
checkboxes all at an outcome; the coverage table's row count (135); the Q6
table's `unreached` rows each with `Already written:` and no upstream
deletion; **re-running the two-way caller count for five tools and the Q4
upstream-state loop once on an export of the tip made under
`/workspace/tmp`**, and `register-check` on a simulated merge with the
coordinator's tip; the retro's four answers; the six exit codes. The lane
posts one hand-back comment naming the tip and each artifact by path,
writes `reviewed-at:` and `fixed-at:` into #653's body, then says it is
idle. After acceptance the coordinator closes the audit issue, prompts the
lane for `audit-completion.json` and the full lint, writes the hashes into
`slices.json`, merges the branch in its turn after the M7 candidate (after
T5's, before T4's), regenerates the ledgers, posts finding 24's proposal on
#585 in the shape the lane wrote, and closes #653 when every row is proven.
A brief that needed the coordinator's help mid-slice beyond the stage-D
pause is a defect in this brief: log the friction; the coordinator fixes
the template.

**The readings before dispatch** (plan § 3, principle 3): the epic's futro
(#800) gains a T6 kickoff addendum, and a stranger's proof of this brief is
run by a reader with no context; version 2 records what each found.
