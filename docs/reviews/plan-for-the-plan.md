# Codebase renovation: the plan for the plan

**Issue:** #346 (M6.P0), under epic #339, milestone M6.
**Decisions:** D-WORKFLOW-083 (the whole codebase, in tiers), D-WORKFLOW-102
(in places, progressively, never one broad sweep; the first item is the
order and the method), D-WORKFLOW-056 (Fable plans to the line, another
model executes), D-WORKFLOW-137 (review depth), D-WORKFLOW-181 (this
widening). Written 2026-10-22 on `feature/m6-renovation-plan-346`.

This document decides **how the renovation of the whole codebase is planned**:
what is surveyed first, how the codebase is cut into slices, how the slices
are ordered, what one slice's work consists of, what a brief for the
executing model must carry, how the program survives feature work landing
beside it, and which ledgers it writes. It does not order the slices; that is
P1's output, `docs/reviews/order.md`, which #346's acceptance criteria name.
It reviews no code.

## 1. What the maintainer asked for

Maintainer, 2026-10-22, quoted as the requirement (D-QA-012):

> "This codebase was a hard fork from ROCKNIX, and that itself was a hard
> fork from a previous operating system. Over the years, I imagine that a
> lot of cruff has built up across the entire sprawl of the operating
> system. Now that we have a new fork, I'd like to have a parallel project
> that runs concurrently with our feature development to do a renovation of
> the codebase."

> "The very first task will be developing a plan for our plan, so that we
> know how we can break this down into increasingly bite-sized chunks."

> "The goal should be for us to develop a way of first surveying the entire
> codebase and understanding it, then breaking it down into a code review
> plan to go top to bottom across the entire codebase and work through it.
> I'd like to make sure that this plan is well defined so that it can be
> handed off in execution to an agent like Opus 5.5, as opposed to relying
> on Fable. I'd like to use Fable to develop all of the plan, the
> milestones, epics, issues, acceptance criteria, etc., and then be able to
> hand it off to a model like Opus 5.5."

> "We also do need to be cognizant of the fact that work will be happening
> in parallel, so there may be times where we need to go back and redo some
> of the review because new functionality may change the codebase. However,
> this should be a relatively small bit of work that needs to be redone
> compared to the sheer scope of the codebase."

> "The goal is to: modernize the codebase; ensure we're adhering to best
> practices, coding standards, and more; identify bugs; look for where
> packages may need to be updated; look for where there's room for
> efficiency in how it works (that's computational, memory management, user
> experience, etc.); find dead ends; make sure the code itself is clear,
> well structured, etc.; in general, try to streamline and improve the
> operating system top to bottom."

How this sits with what was already decided: D-WORKFLOW-083 asked for an
adversarial review of the whole codebase in three tiers; D-WORKFLOW-102
refined it to slices done in places and progressively, under a milestone of
its own, with the first item being the analysis that sets the order and the
method. This request keeps both (the slices still cover the whole, still
progressively, still never as one sweep) and **widens the lens** from finding
defects to renovating: the seven goals above become the seven questions every
slice answers (§ 4). It also fixes the division of labour: Fable writes the
plan, the survey, the order, the epics, the issues and their criteria; a
model such as Opus 5.5 executes a slice from its brief (§ 7), the shape
D-WORKFLOW-056 used for the fix round of 2026-09-28.

## 2. The shape of what is being renovated

Measured on `next` at `8ebaf8daad` (2026-10-22; 133,465 tracked paths; `upstream/next`
at `03d71e3217` in the fresh clone, merge base `c445081a59`) and from #339's
count of 2026-09-30. "Lines" are file lines including blanks; the survey (P1) replaces
these with exact, machine-generated numbers.

| Root | Files | What it is | How it is read |
| --- | ---: | --- | --- |
| `packages/` | 2,546 (1,040 `package.mk`) | generic recipes, grouped by function; 86,857 lines of recipe, script and config; 277 kernel patches, 88 addon patches | recipes by group; patches by provenance |
| `projects/` | 3,728 | SoC families and devices: `options`, overrides, `patches/`, `filesystem/` overlays; 439,514 lines of which most are kernel `.conf` and device trees; 885 patches under `projects/ROCKNIX` alone | the fork's own packages line by line; device files by device; configs by diff against their kernel's defaults |
| `projects/ROCKNIX/packages/` | 255 paths fork-own (from the merge base `c445081a59` with `upstream/next` to `next`) | the fork's product: `emulators` (86 paths), `network` (62, the cloud sync), `rocknix` (30, the OS scripts), `sysutils` (18), `hardware` (11), `graphics` (9), `ui` (8, the EmulationStation pin), `apps` (8); plus `devices/GENERIC_X64` (9), `tools/` (129), `scripts/` (54), `packages/` (21) | Tier 1: line by line, the full lens |
| `scripts/` | 76 | the build engine (`build`, `install`, `image`, `mkimage`, `build_distro`), 25,924 lines | line by line; it is small and everything depends on it |
| `config/` | 181 | the layered options and arch files | with `scripts/` |
| `distributions/` | 31 | the distro identity | with `scripts/` |
| `tools/` | 236 tracked (99 fork tools at the top level; the `node_modules` the council runner needs is gitignored and installed per checkout) | the fork's QA and process tooling, 53,802 lines | fork tools line by line |
| the council toolchain | 45 of `scripts/`' 76 tracked files, `seed/`, `verifier-pins.json`, `council-seat-efforts.json` | scaffold's export, committed byte for byte at its own paths (D-WORKFLOW-088) | by provenance and version only; it is refreshed by copying the next export over, never edited here |
| `.githooks/`, `.github/workflows/` | 6 + 6 | the guards and the fork CI | with `tools/` |
| EmulationStation (`pixelelated/emulationstation` at the pin in `projects/ROCKNIX/packages/ui/emulationstation/package.mk`, `16dbac52`) | 482 files in `es-app/src` and `es-core/src`, 184,891 lines; the fork's own +42,180 | the interface the player uses | Tier 3: the fork's pages line by line first; the launch path before #336 Step 1 (D-WORKFLOW-102) |
| `docs/`, `research/`, `.github/sessions/` | 125,258 + 695 + ~350 | the fork's records, QA evidence and frames | **not code**; reviewed only for records that mislead (§ 5, the "records" slice) |
| `.claude/rules/`, `.claude/skills/`, `CLAUDE.md`, `AGENTS.md` | 30 rules, 10 skills | the doctrine that binds every session | the "doctrine" slice: are the rules current, enforced at the stage they claim, and free of hardcoded host paths (#640) |

Three provenance tiers run through every root, and the tier decides the lens
(§ 4):

- **Fork-own**: written here since the fork (from the merge base with
  `upstream/next` to `next` on the distribution, 126,855 paths of which 125,225
  are records under `docs/`; from the merge base with `rocknix/master` to the
  pin on EmulationStation). A path upstream changed since the merge base and
  the fork never touched is upstream-carried, not fork-own: the two-way diff
  `upstream/next..next` would mislabel 912 of them. About 121,000 lines
  across both (#339). Everything applies: bugs, standards, structure,
  efficiency, dead ends.
- **Upstream-carried**: ROCKNIX's and its upstreams' (JELOS, LibreELEC,
  CoreELEC) code that the image runs. About 140,000 lines of shell and
  recipes (#339). The first questions are different: is it still reached by
  any image we build; is it current with upstream; did upstream fix it since;
  do we carry a local change that upstream has since superseded.
- **Vendor-carried**: patches to third-party sources (kernels, emulators,
  libraries) and kernel configurations. Half a million lines of patches and a
  quarter million of configuration (#339). Never read line by line: one
  provenance row per patch (origin, merged upstream or not, the reason we
  carry it, the version it was made against, whether it still applies), and
  one diff per kernel config against its base.

## 3. Three principles the method rests on

1. **Provenance decides the lens, size decides the slice.** A fork-own file
   gets the full seven questions; an upstream-carried file gets the
   reachability and currency questions first and the rest only if it stays;
   a vendor-carried patch gets a table row. Slices are then cut to a size one
   executing session finishes (§ 5).
2. **A review is a fact about a tree hash.** Every slice issue records the
   paths it covers and the commit it was read at. Drift is then `git diff
   <reviewed-at>..next -- <paths>`: a diff, measurable and small, never a
   re-read (§ 8). This is what makes "work happening in parallel" cost a
   diff and not a slice.
3. **The brief is the unit of handoff.** Fable's output for a slice is a
   brief an executing model can run without this conversation (§ 7). The
   proof that a brief is good enough is the one D-WORKFLOW-133 uses for the
   session stash: a model with no context is given the repository and the
   brief and its first hour is compared with what the brief intended.

## 4. The seven questions a slice answers

The maintainer's goals, each turned into a question with the evidence that
answers it. These are the **renovation face** added to the code-auditor
skill's Phase 3 (§ 6, stage B); the skill's own faces (instruction files,
blindspot register, invariants, cross-system interactions) stay.

| # | Goal | The question the executor answers, per file or unit | Evidence that answers it |
| --- | --- | --- | --- |
| Q1 | Modernize | Is this written against an interface, language level, tool or convention that has a current replacement in this tree or upstream (bash idioms the rest of the tree has moved past, `systemd` units written the old way, Python 2 remnants, hand-rolled JSON, a library two majors behind)? | the replacement named with where the tree already uses it; `git log -S` showing when the old form stopped being written |
| Q2 | Standards and best practices | Does it meet the rules in `.claude/rules/` whose `paths:` match it, `packages/README.md` for recipes, and the conventions of its own kind (`set -euo pipefail` and quoting in shell, late binding in `package.mk`, the ES rules for the interface)? | the rule and section cited; `tools/pkgcheck` output for a recipe; `shellcheck` output where it runs |
| Q3 | Bugs | Where does it fail: the unhandled branch, the race, the wrong default, the path that works on the host and not on the device? | a reproduction on the VM or a trace with file:line; the code-auditor evidence floor applies (host reasoning about device behaviour is a lead, not evidence) |
| Q4 | Package currency | Is the pinned version current, and if pinned on purpose does the recipe say why? Does upstream ROCKNIX carry a newer recipe we have not merged? | `tools/fork-package-freshness` for fork-introduced packages; for the rest, the pin against the project's releases with the date checked |
| Q5 | Efficiency | What does it cost at run time: on the launch path (time to play, D-CLOUD-098), at boot, in memory on a 1 GiB handheld, in a loop that runs every exit; and what does it cost the player in steps? | a measurement on the VM (`tools/time-to-play`, `tools/es-launch-memory`, `tools/signin-memory`) or the named absence of one; the player-facing path counted in presses |
| Q6 | Dead ends | Is it reached at all: by any image we build (the device `options`, the package dependency graph), by any caller (`grep` for the symbol, the unit, the script name), by any player path? Is it a half-finished feature, a retired mechanism still carried, a compatibility alias with no retirement condition (NAMING.md)? | the reachability search recorded as a command and its output; `engineering-practices.md` § Before deleting a duplicate applies before any removal |
| Q7 | Clarity and structure | Can a reader new to it tell what it does and why in one pass: naming, one responsibility per unit, no copy of logic that lives elsewhere, comments that match the code, a header that says where it came from? | the specific unit named with what a reader stumbles on; a duplicate named with its original |

A finding is one of the seven with its evidence; the classification is the
code-auditor skill's (severity, category) with `Renovation` added as a
category for Q1, Q5, Q6 and Q7 items that are not defects. Every removal
proposed under Q6 carries the `Already written:` question (D-WORKFLOW-050):
what the retired code left on devices and in clouds, and how the removal
treats it.

## 5. Slicing

**A slice is a set of paths one executing session reviews to a finished
punch list.** Its size is bounded two ways:

- about 8,000 to 12,000 lines of code read line by line, or one package
  group, or one device; #339's packets (about 500 KB a seat) and the fix
  round's briefs (D-WORKFLOW-056) are the precedent for what a session
  finishes;
- the paths that share runtime state stay together, because interaction
  defects live at the seam (code-auditor § Cross-system interaction audit):
  the cloud scripts and the ES pages that call them; `runemu.sh` and the
  emulator wrappers; `backuptool` and the settings archives; the proxy and
  its consumers.

Each slice has one issue, attached as a sub-issue of #339 until its area's
epic is filed at that area's first dispatch (then re-parented, the epic's body
and the title updated with a comment, as `milestone-phase-naming.md` says).
All slices are one declared phase, P2, ordered by `order.md`; the title is
`M6.P2 E339/T<k>: <area>: <slice>` (`T`, verification, from the closed sub-id
set; `k` sequential), becoming `E<epic>/T<k>` under the area epic. It carries: the paths (so `tools/box-check` can read them), the
provenance tier, the line count, the lens questions that apply, the
interacting subsystems, the review depth (§ 6, stage C), the reading
prerequisite if any (the launch-path slices before #336 Step 1; no slice
gates a release, D-WORKFLOW-187), and the `reviewed-at` field left empty
until stage H fills it.

**Areas become epics.** The survey (P1) proposes them; the first cut, from
the shape in § 2, is:

| Epic (area) | Tier | What it holds | Why it is one epic |
| --- | --- | --- | --- |
| Build engine | upstream-carried, small fork delta | `scripts/`, `config/`, `distributions/`, the `Makefile`, `tools/mkpkg`, the Docker path | everything else is built by it; 26,000 lines read once; where the maintainer puts the renovation's value, ahead of any device, with the harness and the package currency beside it (D-WORKFLOW-186; #644 reads ROCKNIX's documented build path against ours) |
| OS scripts and launch path | fork-own on upstream | `projects/ROCKNIX/packages/rocknix/` (the OS scripts, `runemu.sh`), `sysutils/` (busybox, systemd units, the quirks), `hardware/` | the launch path is read before #336 Step 1 replaces it (D-WORKFLOW-102 as D-WORKFLOW-187 refines it: a reading order, not a release gate) |
| Cloud sync and saves | fork-own | `projects/ROCKNIX/packages/network/rclone/`, the cloud tools under `tools/`, `backuptool` | one state model, one filter allowlist, the invariants in `rclone-cloud-sync.md` |
| Offline achievements | fork-own | the proxy package, its consumers in RetroArch and the emulators, the ES pages | one protocol, one queue |
| Emulators and cores | upstream-carried with fork patches | `projects/ROCKNIX/packages/emulators/` (276 differing paths), the RetroArch patches, the wrappers | the largest group; split by family (libretro cores, standalone, RetroArch itself) |
| Devices | upstream-carried | `projects/ROCKNIX/devices/*` for the devices we ship (H700 and SM8550; GENERIC_X64 as the test image, D-WORKFLOW-185), their kernels and quirks; every other target is a row | one slice per device we ship; one row per device we do not; RK3566 and RK3326 are the recorded first widening, each a device build with its own issue when the maintainer opens it |
| Generic packages | upstream-carried | `packages/*` by group | reachability first: a group no image we build reaches is a table, not a reading |
| Patches and configs | vendor-carried | every `.patch` under `packages/` and `projects/`, every kernel `.conf` | the provenance table (#339 criterion 2): one row per patch, count equal to `find -name '*.patch' | wc -l` |
| Interface | fork-own on batocera and ROCKNIX | the EmulationStation fork: the fork's pages first, then the launch path, then `es-core` | the launch-path slice is read before #336 Step 1 (D-WORKFLOW-102) |
| Tooling and guards | fork-own | the 99 fork tools, `.githooks/`, the fork workflows, `tools/vm-walks/` | the harness that proves everything else; #640's hardcoded paths live here |
| Doctrine and records | fork-own | `.claude/rules/`, `.claude/skills/`, `CLAUDE.md`, `AGENTS.md`, the registers, the indexes | a rule that lies is cruft of the most expensive kind; records are reviewed only where they mislead a reader today |

A slice an executing session cannot finish is two slices; P1 cuts, the
executor does not re-cut mid-slice (the swarm rule in `ceremonies.md`: a
scope under audit is not mutated from elsewhere, and not re-scoped from
inside).

## 6. The phases

The milestone body (M6) carries the live order and current/next work
(D-WORKFLOW-139); this is the shape it orders.

### P0, the plan for the plan (this document; #346)

Exit: this document on `next`; D-WORKFLOW-181 in the register; M6's body
rewritten to this shape; #339 and #346 retitled under the naming rule and
their bodies pointing here; the P1 brief written (§ 7) and the P1 issue
filed; the lane's worktree and branch in place (#640 for the checkout move).

### P1, the survey (next; its own issue under #339)

The inventory and the order, produced by the multi-pass
iterative analysis the maintainer uses for collections (seven passes, N-to-N
cross-reference, a tracking file; the copy lives outside the tree, see the
memory `maintainer-meta-process-multi-pass`), at its comprehensive rigour
because this is the first analysis of the scope:

1. **Inventory** (pass 1): `tools/renovation-inventory` walks the tree and
   the ES checkout and writes `docs/reviews/inventory.json`: for every path,
   its root, provenance tier (fork-own is `git diff --name-only $(git merge-base
   upstream/next next) next`; on EmulationStation the merge base with
   `rocknix/master` to the pin; upstream-only changes since the merge base
   are upstream-carried), language, line count, patch count, last fork
   commit, last upstream commit, and reachability (which built images include
   it, from the device `options` and `PKG_DEPENDS_*`). The verification is
   the count: the tool's total equals `git ls-files | wc -l` on both trees,
   and the patch rows equal `find -name '*.patch' | wc -l`.
2. **Clustering** (pass 2): paths into the areas of § 5, written to
   `docs/reviews/inventory.md` with the per-area totals; an area whose read
   size exceeds a session is split here.
3. **Assessment** (pass 3): each area scored on the ordering lenses of § 6a,
   with the evidence for each score (the friction log's and blindspot
   register's entries for brittleness; `git log --since` churn; the open
   issues touching it; the planned changes it is nearest).
4. **Cross-reference** (pass 4): every area against every other for shared
   state and call edges, so the slice boundaries of § 5 are drawn from the
   edges and not from the directory tree.
5. **Classification and reconciliation** (passes 5 and 6): the order, with
   the lens that put each slice where it is, written to
   `docs/reviews/order.md` in the shape #346's first criterion names.
6. **Action** (pass 7): the proposed order and slice list posted on the P1
   issue and the maintainer's yes recorded there (the pattern's pass 7 is
   interactive by its own rule); then the slice issues filed by the
   coordinator lane (D-WORKFLOW-189: the definition of work items is the
   coordinator's; P1's renderer produces the bodies) as sub-issues of
   #339, each with its brief's scope block (area epics are filed lazily at
   each area's first dispatch, so each owes its futro at its own kickoff); the preliminary three-model review of the
   order (`.claude/skills/council/references/review-formats.md`, advisory)
   or the recorded reason it was not run; the register row for the order;
   the M6 body updated.

P1's tools, built in P1 because a procedure becomes a tool
(`learning-capture.md` § 3): `tools/renovation-inventory` (above),
`tools/renovation-drift` (§ 8), `tools/renovation-status` (one table: slice,
area, lines, depth, state, reviewed-at, drift since), and the renovation face
added to `tools/lint-audit-artifacts` (§ 6b) with a fixture that proves it
fails a folder without the seven questions answered. P1 opens with a futro
(the skill) because it is the first execution epic of the program.

### P2 onward, the slices

In the order `order.md` sets, each slice runs the per-slice procedure (§ 6b)
to its resolution gate. Slices in different areas may run in parallel in
their own worktrees; two slices never share a path. A slice's punch list is
resolved in the same cycle (D-WORKFLOW-054: everything found is fixed or
withdrawn with its reason, not only the Critical and High), which is where
the renovation actually happens.

### Standing, drift re-review

Runs at every slice close (§ 8), on the renovation's own cadence and never as
a release step (D-WORKFLOW-187). It is a phase with no end, listed in the
milestone body as such.

### 6a. Ordering lenses

The four the maintainer named in #346, with two the renovation adds. The
survey scores each area on all six and the order is argued from the scores,
not from the directory listing.

| Lens | Puts first | Evidence for the score |
| --- | --- | --- |
| Security | code that handles credentials, network input, archives it unpacks, anything that runs as root on a device | the sign-in broker, `rclone.conf` handling, the updater, backup/restore, the proxy's listener |
| Brittleness | the parts that have failed most | entries in `docs/blindspot-register.md` and `docs/friction-log.md` per path; bug issues closed per path; `git log --since=2026-06-01` churn |
| Nearest new functionality | what the fork has changed most since the fork | `git diff --stat $(git merge-base upstream/next next) next` per area; the M7 change log |
| Nearest planned change | what is about to be replaced or extended | #336 (the libretro runner under ES), #576 (GTK4), #509 (the remaining old names), #585 (upstream contributions) |
| Cost against value | small, central, read once | the build engine; the OS scripts; a device we ship |
| Reachability | what no image reaches at all | the inventory's reachability column: unreached code is a dead-end slice reviewed as a table, cheap and early, because removal shrinks every later slice |

The renovation gates no release (D-WORKFLOW-187, refining D-WORKFLOW-102):
a finding that is a defect is a bug issue and holds or clears a release the
way every bug does (D-QA-051). One reading order stands regardless of the
scores: the OS launch, control and state slice and the interface's launch-path
slice are read before #336 Step 1 replaces what they read.

### 6b. The per-slice procedure

One executing session, serial, document-as-you-go, under the code-auditor
skill's lifecycle with the renovation face added. The stages are the brief's
sections (§ 7).

| Stage | What | Output |
| --- | --- | --- |
| A. Scope | the slice's inventory rows re-derived from the tree at the branch's `next` (counts match the issue); the interacting subsystems listed; the rules whose `paths:` match, read from `next` | `00-running-log.md` opened; `01-research-notes.md` § Scope |
| B. Read | code-auditor Phases 1 to 4 over the paths, with Phase 2's criteria being the slice issue's checklist and Phase 3 carrying the seven questions of § 4 as its renovation face beside the skill's own faces | `02-forward-audit.md`, `03-retrospective.md`, `04-analysis.md` |
| C. Second opinion | Phase 4.5 self-refutation, then Phase 4.6 at the slice's depth (§ 6c) through the Facilitator; the served model verified | `04-analysis.md` § Second opinion, `second-opinions/` |
| D. Punch list | Phase 5 and 6: `05-punch-list.md` with the YAML index, every item with its question (Q1 to Q7), severity, category, where, acceptance; the punch-list issue with one checkbox per item | the audit issue, `audit`, `punch-list` labels |
| E. Remediation | the executing lane pauses after stage D; the **coordinator** writes one brief per stream of related items (the D-WORKFLOW-056 shape: the verdict's lines, the fix as a specification, the test first, the `Already written:` line, the files owned, the commit shape; and, from T1's retro (#648, 2026-10-24): commits are cut from intermediate trees only after a green run of the whole harness, so a fault the passing run finds never reaches history, and a stub or a fixture is part of the claim -- a guest proof prints each stub's call count and each bound file's hash beside the tree's before its verdict (#797); a brief is planning, D-WORKFLOW-189) and names the branch each stream lands on (the slice's own branch by default, one commit series per stream); the executor works each stream and delivers the branch, never a build | `streams/briefs/*.md`; the slice branch, or `feature/m6-<slice>-<stream>` where the coordinator says so | **A commit names its paths** (`git add -- <the stream's files>` or `git status --short` read before each commit, not only after): T3's S5 swept a staged deletion into the wrong commit on 2026-10-24. **A host regeneration runs under `env -i` in the C locale**, as the build does: `mk_es_systems` sorts with `ls | sort`, and an `en_US` shell regenerated a table that matched no image (T3's S2). **A time is produced, never typed**: from `date -u` in the same command, and from the tool #843 proposes once it lands. **A fixture runs the real script over fixture files where its tools can be borrowed read-only from a build root** (T5's E1 used the SM8550 root's mtools); a lifted block proves the block, not the route. **A fixture lifts by marker lines and takes a commit or `WORKTREE` argument**, so before and after are one command. **Before a guard fails closed, the recorded builds are read for what it would meet**: a new failure on a path every build takes is a regression, not a guard (T5's E1 and E6 read 26 and 3 recorded roots). **A count that goes into a decision row is taken per shape, not per file** (D-WORKFLOW-194: five archive versions, not eight recipes). **A tree export or a simulated merge is made under `/workspace/tmp/<lane>/`, never in the session's scratch directory on `/tmp`**, after `df -i`: that tmpfs has about a million inodes, and two lanes unpacking trees there in the same minutes ran it out on 2026-10-24 while `df -h` showed 22 GB free. **Prose goes into a running log or a note through a quoted heredoc (`<<'EOF'`) or the Write tool, never an unquoted one**: an unquoted heredoc expands every backticked name in the prose as a command, and on 2026-10-24 at 10:44 T7's log entry ran `scripts/update_packages` -- on the brief's never-run list -- which rewrote a recipe in the worktree and fetched an archive before the lane reverted it (#654, its running log § Incident).
| F. Verification | every behaviour claim proven on the VM (`vm-first.md`), every mechanical check run (`tools/pkgcheck`, `tools/vm-qa` suites that cover the paths, `tools/es-syntax-check` for ES, or its proven recipe while #699 is open); Phase 7 outcomes re-derived from commands | the outcomes in the audit issue; `audit-completion.json` |
| G. Learning | the mini-retro skill over the slice; findings that recur become a rule edit, a tool, a blindspot entry with its guard, or a work-log entry (`learning-capture.md`); Instruction-Recommendations mode runs because the scope is epic tier | `docs/retros/<date>-m6-<slice>.md`; rule and register edits |
| H. Close | the executor posts the hand-back on the slice issue with `reviewed-at:` (the lane's commit the read was made at, its slice bytes equal to `next`'s named hash) and `fixed-at:` (the lane's tip when the fixes are complete) written in the issue's body; the **coordinator** accepts, closes the issue `completed` with the commits named, writes `reviewed_at` and `fixed_at` into `slices.json`, and after the branch merges to `next` regenerates the inventory, `tools/renovation-status` and `tools/renovation-drift` (a drift diff means something only once `fixed-at` is an ancestor of `next`) and moves the M6 body's current/next (D-WORKFLOW-189) **A slice with a fix only an image can show** (every interface slice, whose fixes need a pin bump to reach a binary, `fixed-at-es:` set; and an OS slice's fix to a recipe or a unit as installed, such as a seeded file's mode or a unit's timeout) is accepted at hand-back, its branches merged in their turn by the coordinator (the ES branch into `test/qa-integration` with the pin bumped), and closed only when the first image carrying the fix proves it on the guest; the lane lists each such fix as a `proved: fix-walk-pending-image` or `fix-pending-image` row in `02-forward-audit.md`, and `tools/renovation-status` lists the slice as `remediating` in between (2026-10-23, #700's futro and T1's S5; which build carries the renovation's fixes is D-WORKFLOW-191, open) | the issue closed `completed` with the commits named |

`tools/lint-audit-artifacts` runs before stage D and again before stage H;
the renovation face is added to its checks in P1 so a slice without the seven
questions answered fails the lint rather than a reader's attention.

### 6c. Review depth per slice

From the code-auditor review levels (D-WORKFLOW-137), chosen in P1 and
recorded on the slice issue before dispatch:

| Slice | Depth |
| --- | --- |
| a dead-end table, a provenance table, a doctrine read | Local: the executor alone; the lint and the counts are the check |
| an ordinary code slice | Independent: the executor plus one reviewer from another lab |
| a security, state-preservation or launch-path slice; the cloud sync; the updater | Extended: two reviewers from two other labs |

The executor is an Anthropic model, so the reviewer is not: GPT-6 Astra
(`--member gpt --provider openrouter`, `max`) is the default second lab, and
Gemini 4 Argon, verified operational on #638/#639, is the third for extended
depth. Fable cannot be a reviewer of Opus's work under this rule: same lab.
The five-seat council is not a slice's reviewer; it is the escalation a
release may be assigned (`adversarial-council.md`). The preliminary review of
the order in P1 is a different thing again: its three seats (Claude, Gemini,
GPT) are fixed by the format's own contract
(`.claude/skills/council/references/review-formats.md`) and it is advisory,
so the lab exclusion above does not apply to it, and a seat that fails
verification is recorded, never substituted.

## 7. The brief: what the executor receives

A brief is a Markdown file under `docs/reviews/briefs/<slice>.md`, written
by the planner and committed before dispatch, that an executing session runs
start to finish without this conversation. Its sections, in order, each
mandatory:

1. **Identity**: the slice issue, the epic, the milestone phase, the branch
   and worktree (`feature/m6-<slice>-<issue>` under
   `/workspace/repos/pixelelated/distribution.worktrees/m6-<slice>-<issue>`,
   the issue number appended, as T1 #648 and T2 #649 do; an interface
   slice adds an EmulationStation worktree
   `emulationstation-next.worktrees/m6-<slice>-<issue>` on
   `feature/m6-<slice>-<issue>` from the pin), the model
   and effort the maintainer selected, the review depth and reviewer
   recipes.
2. **Scope**: the paths, the tree hash they are read at, the line count per
   path (the executor re-counts; a count that differs is recorded as a delta
   beside the brief's, and the stop is a hash that is not the one named, a
   count that cannot be produced, or two commands for one quantity that
   disagree), the provenance tier, the interacting subsystems and their paths (read-only
   context).
3. **Read first**: the rule files in scope by name, read from `next`; the
   blindspot entries that touch these paths by number; the prior audits of
   these paths under `docs/audits/` (as provenance; the skill has no Phase 2.5 at
   epic tier, so the verdicts are read after the slice's own Phase 2 is
   written, compared then, and never transcribed into it); the decisions by ID that settle questions the slice
   might otherwise re-open.
4. **The questions**: § 4's table restated for this slice, with the questions
   that do not apply struck and the reason (a provenance table has no Q5).
5. **The evidence floor**: the code-auditor's rules as its SKILL.md § Evidence
   floor lists them; what runs on the VM and how (`generic-x64-vm-testing.md`
   § headless), with every tool the brief names run with `--help` and every
   host path it names listed before the brief is committed (the first
   slice brief had six such claims wrong, futro 2026-10-23); what never
   runs (no device, no cloud, no build in a build worktree, no edit to a tool
   that is in flight, no `pkill -f`).
6. **Outputs**: the audit folder name, the six phase files, the YAML index,
   the audit issue's title shape, the retro's path, the fields to fill on the
   slice issue at close.
7. **Acceptance**: the slice issue's checklist, every item agent-verifiable
   (D-QA-044): the lint's PASS line, the counts, the issue's checkboxes, the
   `reviewed-at` hash present.
8. **Stop conditions**: completion; an explicit maintainer pause; a blocker
   named with what is needed; a hash mismatch at stage A (a differing count
   is a delta, not a stop). A checkpoint is not a stop (D-WORKFLOW-149). Nothing else ends the session
   early, and an idle session reports itself idle.
9. **Ceremonies owed**: the work-log entry per session, headed by the issue;
   `tools/work-log-index --write`; a friction line the moment something
   slows; the retro at close; the register row for any decision the slice
   forces; the ceremony check before the push.
10. **Hand-back**: what the planner reads to accept the slice: the audit
    issue's checkboxes all ticked with their outcomes, the lint PASS, the
    status table's row, the retro's four answers.

**The planner keeps** the order, the cutting, the briefs, the acceptance of
a slice against its brief, the register, and the milestone body. The planner
does not re-review a slice the executor finished; it reads the artifacts the
brief named and runs the lint. A brief that needed the planner's help
mid-slice is a defect in the brief, logged as friction and fixed in the brief
template here.

## 8. Parallel work and drift

Feature work (M7 and after) lands on `next` while slices run. The rules:

- **Every slice records its hash.** Stage A reads at a commit; stage H writes
  `reviewed-at: <hash>` and `fixed-at: <hash>` on the slice issue and in the
  inventory. A review is a fact about that tree.
- **Drift is a diff, found by a tool.** `tools/renovation-drift` (built in
  P1) lists, for every closed slice, `git diff --stat <fixed-at>..next --
  <paths>`: files touched, lines changed, and whether any touched file is on
  the security, state-preservation or launch-path list. It runs at every
  slice close, on the renovation's own cadence and not as a release step
  (D-WORKFLOW-187).
- **A small drift is re-reviewed at issue tier.** Under 20 % of the slice's
  lines and no listed file: a local, issue-tier pass over the diff only, by
  the executor, with its own short audit folder (`issue-<slice>-drift-<date>`)
  and no second opinion. The slice's `reviewed-at` moves forward.
- **A large drift re-opens the slice** at its original depth over the diff
  and the files the diff touches, not the whole slice. Over 20 %, or any
  listed file touched, or an interacting subsystem replaced (the libretro
  runner replacing the RetroArch launch path is the known case).
- **The swarm rule holds in both directions.** A slice issue says which
  paths are under review and from when; a feature branch that must touch
  them either waits for stage H or announces itself on the slice issue, and
  the slice re-baselines at stage A on the merged tree rather than reading a
  moving one (code-auditor § Execution discipline). Slices are cut to days,
  not weeks, so this costs little.
- **Two lanes, one tree.** Slice worktrees are cut from `next` and merged to
  `next`; they never merge another lane's feature history to refresh rules
  (`session-resume`, D-WORKFLOW-140). Where two lanes append to the same
  ledger (the register, a day's work log, the index), the merge keeps both
  appends and regenerates the index; neither lane edits the other's rows.
- **One coordinator lane, one session per worktree** (D-WORKFLOW-183,
  2026-10-22). `feature/m6-renovation-plan-346` is the program's coordinator
  lane, as `m7-player-setup` is M7's: it plans, writes briefs, accepts at
  gates and integrates. Each executing phase or slice is one worktree with
  one session; a second session never shares a checkout (one index per
  worktree, the 2026-09-14 mixed-image failure), and fan-out inside a lane is
  read-only research subagents whose leads the lane re-derives. There is no
  long-lived M6 integration branch: `next` is the roll-up, because
  remediation must be built and VM-tested there; a slice stacks on the P1
  chain only while `next` is gated, and merges in order afterwards.
- **The canonical stash is one file with two writers**, which the M7 lane
  and this lane will both reach for. Until the maintainer settles it, this
  lane keeps its state in its branch pointer
  (`.github/sessions/saved-session-state-feature-m6-renovation-plan-346.md`)
  and does not edit `saved-session-state-next.md` while M7 owns it; the
  question is recorded on #346.

## 9. Ledgers and tools

| Ledger | Where | Written by |
| --- | --- | --- |
| The order and the method | `docs/reviews/order.md`, this file | P0, P1 |
| The inventory | `docs/reviews/inventory.json`, `inventory.md` | `tools/renovation-inventory`, re-run at every stage H |
| The status table | `docs/reviews/status.md` | `tools/renovation-status`, from the inventory and the slice issues |
| Drift | `tools/renovation-drift --write docs/reviews/drift.md`, its table also pasted on the slice issue | the coordinator, after every slice's branch merges to `next` |
| The briefs | `docs/reviews/briefs/<slice>.md` | the planner, before dispatch |
| The audits | `docs/audits/<date>-epic-m6-<slice>/` | the executor, per slice |
| Decisions | `docs/decision-register.md` | the session that makes one, same session |
| Learnings | `docs/work-logs/`, `docs/retros/`, `.claude/rules/`, `docs/blindspot-register.md` | per the ceremonies rule |
| Milestone body | M6 on GitHub | the planner at every state change (D-WORKFLOW-139) |

The three tools are fork-only and go on the personal-paths list in
`fork-workflow.md` and `.githooks/pre-push` when built. The inventory is
generated, never hand-edited; a hand edit is a bug in the generator.

## 10. Acceptance criteria for P0

- [ ] This file exists on `next` at `docs/reviews/plan-for-the-plan.md`, and `docs/reviews/README.md` names it, `order.md`, the inventory, the status table and the briefs directory with what writes each.
- [ ] `docs/decision-register.md` carries D-WORKFLOW-181 (the widening, quoting the maintainer, citing #346, #339, D-WORKFLOW-083, D-WORKFLOW-102, D-WORKFLOW-056) and D-INFRA-025 (the fresh clone and its layout, citing #640), and `tools/register-check` passes.
- [ ] Milestone 6 is named `M6: Codebase renovation` and its body opens with the current/next order of § 6 and the acceptance of its former body; #339's title carries `M6:` and #346's carries `M6.P0`, and each body links this file (read back from GitHub, not from the prepared text).
- [ ] The P1 issue exists under #339, titled `M6.P1 E339: The survey`, with § 6's six steps as its checklist, the three tools named, and the futro owed at its kickoff named.
- [ ] The P1 brief exists at `docs/reviews/briefs/p1-survey.md` with the ten sections of § 7, and a session with no context given only the repository and that brief reaches step 1 of P1 without a question to the planner (the D-WORKFLOW-133 proof, recorded on #346 with the session's first ten commands).
- [ ] `tools/forbidden-terms-check` on the tree exits 0; `tools/work-log-index --check` passes; `tools/ceremony-check` reports nothing newly owed by this lane.

The last three criteria are P0's remaining work after this document lands:
the milestone and issue edits are made the same session as this file; the
P1 issue and brief follow from § 6 and § 7 and are the next commits on this
branch.

## 11. Open questions for the maintainer

None blocks P1; each is answered by a register row when settled.

1. **The milestone's name.** It was "The adversarial review, in places";
   this document calls it `M6: Codebase renovation`. A different name is a
   one-line edit.
2. **The executor and effort.** The request names Opus 5.5 as the kind of
   model; the brief carries the model and effort the maintainer selects. The
   default this document assumes is Opus 5.5 at high effort for a slice and
   the same model for its remediation streams.
3. **Depth defaults.** § 6c proposes Independent as the ordinary depth and
   Extended for the listed slices, with Astra and Argon as the other labs.
   Review depth has cost in OpenRouter credit (D-WORKFLOW-049); the
   maintainer may prefer Local for more of the upstream-carried slices.
   Settled 2026-10-22: the defaults stand (D-WORKFLOW-184).
4. **Where the EmulationStation fork's survey runs.** The ES tree is a
   separate repository; the inventory tool reads both, and ES slices run in
   an ES worktree with the distribution checkout's rules (D-WORKFLOW-010).
5. **The canonical stash with two lanes** (§ 8, last rule).
6. **The legacy checkout** (#640): when M7's build worktrees move and the
   old directory is retired.
7. **Which build carries the renovation's EmulationStation pin bumps**
   (D-WORKFLOW-191, from #700's futro on 2026-10-23): the renovation's
   pins ride the M7 lane's next build, or the coordinator asks the
   maintainer for a GENERIC_X64 build per batch of interface slices.
   Until the answer, an interface slice is `remediating` from hand-back
   to the first image that proves its fixes (§ 6b stage H).
