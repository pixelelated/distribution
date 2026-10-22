# Brief: M6.P1, the survey (#641)

A session with no other context runs this brief start to finish. It is the
unit of handoff the plan defines (`docs/reviews/plan-for-the-plan.md` § 7);
read that document whole before the first command. Every section below is
mandatory; a section that does not apply says so and why. Where this brief
and the checklist on #641 differ, #641 wins and the brief is corrected in the
same session. Version 2, after the stranger's proof of 2026-10-22 (its
sixteen questions are answered in the text below).

## 1. Identity

- **Issue:** #641 `M6.P1 E339: The survey`. **Epic:** #339. **Milestone:**
  M6 (`M6: Codebase renovation`); its body holds the live order, read it
  first and update it last. **Predecessor:** #346 (M6.P0, the plan); its
  order-and-method criteria are carried into #641 and must be met here.
- **Branch and worktree:** `feature/m6-p1-survey-641` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641`,
  cut from `next` in the primary checkout
  `/workspace/repos/pixelelated/distribution` (D-INFRA-025). **`worktrees.md`,
  `device-builds.md`, `CLAUDE.md` and `AGENTS.md` still name the legacy
  layout (`/workspace/repos/rocknix`, `rocknix.worktrees/`); D-INFRA-025 and
  #640 supersede them for this lane, and this brief's paths are the ones to
  use.** The legacy checkout is another lane's: read from it, never write to
  it.
- **Model and effort:** the ones the maintainer selected on #641 when
  dispatching; absent a selection, Opus 5.5 at high effort. Record what
  actually ran in the tracking file's header.
- **Review depth:** Local for the survey's own analysis (an inventory is
  checked by its counts, not by a reviewer). The **order** gets the advisory
  three-model preliminary review exactly as
  `.claude/skills/council/references/review-formats.md` § Preliminary-review
  procedure prescribes: its seats are Claude, Gemini and GPT, fixed by
  `readPreliminaryReviewContract()`; the contract is written to
  `research/preliminary-reviews/<run-id>/review-contract.json` and validated
  with `assertPreliminaryReviewContract()`; each seat is called through
  `tools/council/run invoke --member <claude|gemini|gpt> --provider openrouter
  --prompt-file <brief> --output <file> --source-manifest <manifest>`
  (D-WORKFLOW-049; the key is sourced from `~/.config/council/env`, never
  printed); the served model of each call is verified from its provenance
  file before the next call. It is advisory: no vote, no approval, not an
  audit, not a council. The executor's lab is not excluded here, because the
  format fixes the seats (plan § 6c); D-WORKFLOW-137's exclusion applies to
  the slices' audits. **Fail closed, never substitute:** a seat that is
  unavailable or fails verification is not replaced and the roster is not
  shrunk (`adversarial-council.md` rule 4); record in `order.md` that the
  review did not run and why, mark `order: unreviewed` in `status.md`, and
  continue the survey (#346's third criterion allows a recorded reason); the
  first slice's dispatch then waits for the maintainer's word on #641.

First commands:

```bash
cd /workspace/repos/pixelelated/distribution
git fetch origin && git fetch upstream --no-tags
git switch next && git merge --ff-only origin/next
test -f docs/reviews/plan-for-the-plan.md || { echo "P0 not merged to next: stop"; exit 1; }
git worktree add /workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641 -b feature/m6-p1-survey-641 next
cd /workspace/repos/pixelelated/distribution.worktrees/m6-p1-survey-641
git diff --quiet next -- .claude CLAUDE.md AGENTS.md || echo STALE   # must print nothing
```

## 2. Scope

Two trees, read at recorded hashes; the survey touches every tracked path
of both and reads none of them line by line.

**Hashes to record** in the tracking file's header before anything else:
the worktree `HEAD`; `upstream/next`; the merge base of `next` and
`upstream/next`; the EmulationStation pin; `rocknix/master`;
`batocera/master`; the merge base of the pin and `rocknix/master`; the
model and effort actually running.

**The distribution.** Re-derive these at the start and write them beside
the recorded values. **A count that differs from the recorded one is not a
stop**: record yours, the recorded one and the delta, and go on. The stop is
a count that cannot be produced, or two commands for the same quantity that
disagree with each other. Recorded at `8ebaf8daad` on 2026-10-22 in the
fresh clone:

```bash
git rev-parse HEAD
git ls-files | wc -l                                   # 133,465
find packages projects -name package.mk | wc -l        # 1,607 (1,040 under packages/, 567 under projects/)
find packages projects -name '*.patch' | wc -l         # 1,709
git rev-parse --short upstream/next                    # 03d71e3217 at the clone's fetch of 2026-10-22; moves with every fetch
MB=$(git merge-base next upstream/next); echo $MB      # c445081a59
git diff --name-only $MB next | wc -l                  # 126,855 fork-own, of which 125,225 under docs/
git diff --name-only $MB upstream/next | wc -l         # 912 upstream-only since the merge base
```

**Provenance tiers** (plan § 2), a three-way split from the merge base,
never the two-way `upstream/next..next` (which would label the 912
upstream-only paths fork-own):

- fork-own: `git diff --name-only $MB next`; a path also in `git diff
  --name-only $MB upstream/next` stays fork-own with `overlap: true`;
- upstream-carried: every other tracked path, the 912 upstream-only ones
  included;
- vendor-carried: every `*.patch` and every kernel `*.conf` under
  `packages/` and `projects/`, whichever tier the diff puts it in (a
  fork-written patch is vendor-carried with `tier_note: fork-written`).

**The interface** (EmulationStation) at the pin `PKG_VERSION` in
`projects/ROCKNIX/packages/ui/emulationstation/package.mk`
(`16dbac5211eea7e70db7394372033be2be7df829` on 2026-10-22). The checkout on
this host is `/home/max/Development/emulationstation-next` (`origin` =
`pixelelated/emulationstation`; `rocknix` = `ROCKNIX/emulationstation-next`,
the fork's upstream; `batocera` = the vendor base, recorded for provenance
only). Read it from a detached worktree of its own, never from that
checkout's current branch; its tiers are fork-own and upstream-carried only
(ES carries no patches):

```bash
ES=/home/max/Development/emulationstation-next
PIN=$(sed -n 's/^PKG_VERSION="\(.*\)"/\1/p' projects/ROCKNIX/packages/ui/emulationstation/package.mk)
git -C $ES cat-file -t $PIN                            # "commit"; else: git -C $ES fetch origin
git -C $ES remote get-url rocknix >/dev/null 2>&1 || git -C $ES remote add rocknix https://github.com/ROCKNIX/emulationstation-next.git
git -C $ES fetch rocknix --no-tags
git -C $ES worktree add --detach $ES.worktrees/m6-p1-survey $PIN
git -C $ES.worktrees/m6-p1-survey ls-files | wc -l                               # 1,114 at the pin
find $ES.worktrees/m6-p1-survey/es-app/src $ES.worktrees/m6-p1-survey/es-core/src -type f | wc -l   # 486
EMB=$(git -C $ES merge-base rocknix/master $PIN); git -C $ES diff --name-only $EMB $PIN | wc -l      # 236 fork-own
```

At the end, the ES worktree is removed with `git -C $ES worktree remove
$ES.worktrees/m6-p1-survey` (an ES worktree holds no build output;
`tools/fork-worktree` is the distribution's tool and only reads its own
repository).

**Reachability** (the inventory's column that feeds the dead-end lens).
The build system computes which packages a device image builds:
`config/multithread` pipes `scripts/pkgjson` into `scripts/genbuildplan.py`,
and `tools/viewplan [package]` is the read-only form of the same pipe
(default `image`). It sources every `package.mk` and compiles nothing. Run
it once per device and architecture the `Makefile` builds (its device targets
are the list: most ARM devices build `arm` and `aarch64`; `GENERIC_X64` and
`AMD64` build `x86_64`; `SM8650`/`SM8750` `aarch64` only), with all three
variables set explicitly every time, because `config/options` **defaults
`DEVICE=SM8550` when it is unset** and a forgotten variable silently gives
another device's plan; the inventory tool asserts all three before sourcing
anything:

```bash
PROJECT=ROCKNIX DEVICE=H700 ARCH=aarch64 tools/viewplan image > <scratch>/plan-H700-aarch64.txt
```

"Devices we ship" is `device-builds.md` § Our devices: `RK3566`, `H700`,
`RK3326`, `SM8550`, `GENERIC_X64`. A package in a shipped device's plan is
`reachable_by: [<device>-<arch>, ...]`; one only in other devices' plans is
`buildable_by: [...]` and `unshipped`; one in no plan is `unreached`. A
script, unit or overlay file is reached when its package is. Run every
device's plans; if the runs exceed ten minutes in all, record the time and
the devices done and continue with those. Do not build.

**Out of scope for reading:** `docs/`, `research/`, `.github/sessions/` are
inventoried (they are tracked paths and the counts must match) and assigned
to the "records" area; nothing in them is read for content.

## 3. Read first

From `next`, in this order, before any analysis:

- `.github/sessions/saved-session-state-next.md` (the M7 lane's canonical
  checkpoint; read for what runs on this host, not for a work queue) and
  this lane's own pointer when it exists.
- Rules: `engineering-practices.md` (verify the artifact, guards fail
  closed, never edit a tool in flight), `worktrees.md` (its removal rules;
  its layout is superseded for this lane, § 1), `fork-workflow.md` (the
  personal-paths list the three new tools join), `issue-tracking.md`
  (agent-first criteria, sub-issues, D-WORKFLOW-132),
  `milestone-phase-naming.md` (titles, the closed sub-id set, the milestone
  body), `learning-capture.md` and `ceremonies.md` (what this phase owes),
  `decision-register.md`, `vm-first.md`, `packaging-and-patches.md` (what a
  recipe and a patch directory are), `instruction-files.md` § The fork's own
  tools (a new tool is added to its table too), `adversarial-council.md` and
  `council-substrate-integrity.md` (the preliminary review's only route).
  Known stale facts in the rules, so they do not cost an hour:
  `device-builds.md` § Iterating on EmulationStation names an old `origin`
  for the ES checkout (the brief's is current); `device-builds.md` § Our
  devices is the shipped list and is current.
- `docs/blindspot-register.md` whole, once; entries 13 (assumed done), 51
  (an open checkbox is a claim) and 64 (read the cause before lengthening a
  wait) are the ones a survey repeats.
- `docs/audits/` folder names and each `05-punch-list.md` header, as
  provenance only: which paths have been audited, when, at what tier
  (`2026_09_10-graceful-degradation/` has no punch list; its README is the
  record). Do not transcribe verdicts; the slice audits sequester them.
- Decisions by ID, cited and not re-argued: D-WORKFLOW-083, -102, -181 (the
  program), -137 (depth), -139 (the milestone body), -132 and D-QA-012 (an
  issue first, the maintainer's words quoted), -133 (a stash a stranger can
  resume), -149 (a checkpoint is not a stop), -050 (`Already written:`),
  -049 (every seat through the Facilitator), -005 (worktree removal),
  D-INFRA-022 and -025 (what stays on disk, where the lane lives), D-QA-044
  and -045 (criteria an agent can tick; say checkbox).
- `docs/reviews/plan-for-the-plan.md` § 2, § 5, § 6, § 6a: the first-cut
  areas, the slicing bounds, the six steps and the six lenses this phase
  executes.
- The maintainer's multi-pass pattern: the seven passes, rigour levels and
  tracking-file template are summarised in plan § 6 (P1); the full text is
  kept outside the tree at `~/.config/rocknix/mpia.instructions.md`. Read it
  there; never copy it into the tree or name its origin. Its pass 7 is
  interactive by its own rule; § 8 below says where that pause falls.

## 4. The questions

P1 answers none of the seven slice questions (Q1 to Q7) for any file; that
is the slices' work. P1 scores every **area** on the six ordering lenses of
plan § 6a. At survey depth the accepted evidence is a search, not a
reading; the slice read is where a score is confirmed or overturned:

| Lens | Evidence the score cites |
| --- | --- |
| Security | a token grep over the area, the token list recorded in the tracking file (at least: `password`, `token`, `secret`, `key=`, `rclone.conf`, `curl`, `wget`, `tar x`, `unzip`, `chmod`, `sudo`, `systemctl`, `nc -l`, `http.server`, `/dev/`), with the matching paths listed by name and their count |
| Brittleness | `docs/blindspot-register.md` and `docs/friction-log.md` entries per path; closed `bug` issues per path; `git log --since=2026-06-01 --format=%h -- <paths> \| wc -l` |
| Nearest new functionality | `git diff --stat $MB next -- <paths>` totals (the merge base, § 2) |
| Nearest planned change | #336, #576, #509, #585 and any open issue whose body names the paths (`gh issue list --limit 300 --json number,body` grepped, bounded) |
| Cost against value | lines to read from the inventory; callers as `grep -rlF '<unit or script name>' packages projects scripts tools \| wc -l`; position in the build (the engine first) |
| Reachability | the inventory's `reachable_by` and `buildable_by` columns; the `unreached` and `unshipped` sets are their own early slices |

Q6 (dead ends) is the one question P1 partly answers, because reachability
is produced here: the unreached and unshipped sets are listed in
`inventory.md` with their line counts, and `order.md` places them as table
slices early (plan § 6a).

## 5. The evidence floor

The code-auditor skill's rules apply to every number in this phase: tracker
state is never sole evidence; a mechanical check that exists is run and its
output recorded; a claim about device behaviour is a lead, not evidence (no
device behaviour is claimed in P1); subagent output is a lead, re-derived by
the orchestrator before it enters a file. Every count in the tracking file is
the output of a command written beside it.

Never, in this phase: build an image or a package; touch a device, a cloud
or a QA guest; edit a tool while any run of it is in flight; `pkill -f`
anything; `git worktree remove --force` or `rm -rf` a worktree (the
distribution's worktrees go through `tools/fork-worktree remove`; the ES
worktree through `git -C $ES worktree remove`); bare `git stash` (the stash
stack is shared); call a model outside `tools/council/run`; print a
credential or the wordlist; merge another lane's feature branch to refresh
rules (read them from `next`); write to `/workspace/repos/rocknix` or to the
ES checkout's current branch; edit
`.github/sessions/saved-session-state-next.md` while the M7 lane owns it
(keep this lane's state in
`.github/sessions/saved-session-state-feature-m6-p1-survey-641.md`); read
`docs/`, `research/` or `.github/sessions/` for content; answer Q1 to Q7 for
any file.

## 6. Outputs

All under the worktree, committed on the branch with messages that cite
#641; each of the three tools is fork-only and joins, in the commit that
adds it, the three places a fork tool must appear: `.claude/rules/fork-workflow.md`
§ Personal paths, `PERSONAL_PATTERNS` in `.githooks/pre-push`, and the table
in `.claude/rules/instruction-files.md` § The fork's own tools;
`.githooks/hooks-test` and `tools/rules-check --quiet` pass after each.

| Output | Path | Shape |
| --- | --- | --- |
| Tracking file | `docs/reviews/p1-tracking.md` | the multi-pass template: the header of § 2's hashes and the model/effort run; progress per pass with counts; the item table; relationships discovered; opened before pass 1, updated after every pass |
| Futro | `docs/futros/<yyyy-mm-dd>-m6-p1-survey.md`, and the same text as a comment on #641 | the futro skill's template; written before the first inventory commit |
| Area map (the one hand-written input) | `docs/reviews/areas.json` | `[{"area": "...", "epic": null, "globs": ["..."]}]`, first cut from plan § 5 with two changes: "doctrine and records" is split into **doctrine** (`.claude/`, `CLAUDE.md`, `AGENTS.md`, the registers, the indexes, `docs/*.md` at the top level) and **records** (`docs/qa-logs/`, `docs/qa-frames/`, `docs/audits/`, `docs/work-logs/`, `docs/retros/`, `docs/futros/`, `research/`, `.github/sessions/`), so records do not dominate every total; every tracked path matches exactly one area's globs |
| Inventory tool | `tools/renovation-inventory` | `tools/renovation-inventory [--distribution DIR] [--es DIR] [--areas docs/reviews/areas.json] [--plans DIR] [--out docs/reviews/inventory.json] [--markdown docs/reviews/inventory.md]`; asserts `PROJECT`, `DEVICE`, `ARCH` before any `viewplan` run it makes; prints `paths: N (git ls-files: N)`, `es-paths: N (git ls-files: N)`, `patches: N (find: N)`, `unassigned: N`; exits 1 when any pair differs or `unassigned` is not 0 |
| Inventory | `docs/reviews/inventory.json` | a header (both hashes, the merge bases, the pin, `rocknix/master`, `batocera/master`, the generation time) and one record per tracked path: `tree`, `path`, `area`, `tier`, `overlap`, `language`, `lines` (null for a binary: git's numstat `-`), `patches` (for a directory of patches), `last_fork_commit`, `last_upstream_commit` (null for a path upstream never had; "upstream" is `upstream/next` for the distribution and `rocknix/master` for ES), `reachable_by`, `buildable_by`. Last-commit columns come from one pass over `git log --format=%H%x09%ct --name-only` per tree and per side, never one `git log` per path |
| Inventory summary | `docs/reviews/inventory.md` | per-area totals (paths, lines by tier, patches, binaries, unreached, unshipped), the unreached and unshipped sets with line counts, the overlap count |
| Order | `docs/reviews/order.md` | per slice, in order: number `k`, area, the lens that placed it, paths with line counts, release gate (D-WORKFLOW-102) or none, depth with reason, interacting subsystems, closing evidence; the security, state-preservation and launch-path file list the drift tool reads; then the preliminary review's status (`reviewed` with the run-id, or `unreviewed` with the reason), its objections and the answers by name |
| Status tool and table | `tools/renovation-status`, `docs/reviews/status.md` | a row `order: reviewed\|unreviewed`, then one row per slice: `k`, area, lines, depth, state (`unreviewed`, `reading`, `remediating`, `closed`, `drifted`), `reviewed-at`, `fixed-at`, drift since; reads `order.md` and the slice issues (`gh ... --json`, bounded with `--limit`) |
| Drift tool | `tools/renovation-drift [--write docs/reviews/drift.md]` | for every slice with a `fixed-at`: `git diff --stat <fixed-at>..next -- <paths>`, the percentage of the slice's lines, and whether a file on `order.md`'s security/state/launch-path list is touched; prints the table and exits 1 when any slice crosses plan § 8's thresholds |
| Lint face | `tools/lint-audit-artifacts` | for a folder named `*-epic-m6-*`: every item in `05-punch-list.md`'s YAML index carries `question: Q1..Q7` or `question: none` with a reason, and `04-analysis.md` has a `## Renovation face` section with one subsection per question; a fixture folder under `tools/test-fixtures/` proves the lint fails without them and passes with them |
| Slice issues | GitHub, sub-issues of #339 | filed only after the pass-7 gate (§ 8); title `M6.P2 E339/T<k>: <area>: <slice>` (all slices are phase P2, ordered by `order.md`; `T` from the closed sub-id set; re-parented and retitled `E<epic>/T<k>` when the area epic is filed at first dispatch); body: paths, tier, line count, lens, interacting subsystems, depth, release gate, `reviewed-at:` and `fixed-at:` empty, and the acceptance checklist (the audit folder `docs/audits/<date>-epic-m6-<slice>/` with its six files, `tools/lint-audit-artifacts` PASS including the renovation face, the punch-list issue with every item at a Phase 7 outcome, `reviewed-at` and `fixed-at` set); attached with `gh api -X POST repos/pixelelated/distribution/issues/339/sub_issues -F sub_issue_id=<REST id>` |
| Area epics | GitHub, label `epic` | **not filed in P1**: an area's epic is filed when its first slice is dispatched, so each owes its futro at its own kickoff (`ceremonies.md`) |
| Register row | `docs/decision-register.md` | the chosen order, citing #641 and #346. The ID: one above the highest `D-WORKFLOW` on `next`, on every pushed branch (`git grep -ho 'D-WORKFLOW-[0-9]*' $(git branch -r --format='%(refname)') -- docs/decision-register.md`), and in the M7 lane's unpushed worktree (`grep -o 'D-WORKFLOW-[0-9]*' /workspace/repos/rocknix.worktrees/m7-player-setup/docs/decision-register.md \| sort -t- -k3 -n \| tail -1`); on 2026-10-22 that is **D-WORKFLOW-182** |
| Lane stash | `.github/sessions/saved-session-state-feature-m6-p1-survey-641.md` | a pointer in the shape of `saved-session-state-feature-m6-renovation-plan-346.md`: start here, current focus, next commands, merge notes |
| Milestone body | M6 on GitHub | current/next moved to the first slice; read back after the write |
| #339 body | GitHub | a line linking `docs/reviews/order.md` |
| Work log | `docs/work-logs/2026_10-work_logs/<yyyy_mm_dd>-work_log.md`, then `tools/work-log-index --write` | an entry per session headed `#641` and the thing decided |

## 7. Acceptance

The checklist on #641 is the contract and is identical to this list. Each
item names the artifact that ticks it.

- [ ] `docs/futros/<date>-m6-p1-survey.md` exists, its adding commit precedes the first inventory commit (`git log --format=%cI --diff-filter=A -- <each>`), and the same text is a comment on #641.
- [ ] `tools/renovation-inventory` exists, is listed in the three places of § 6, and its four printed counts match (`git ls-files` on both trees, `find` for patches, `unassigned: 0`); the commands and outputs pasted on #641.
- [ ] `docs/reviews/inventory.md` lists every area with its totals and the unreached and unshipped sets with line counts.
- [ ] `docs/reviews/p1-tracking.md` carries the header hashes and the model/effort run, shows all seven passes complete with counts, and the cross-reference pass records at least one edge per area.
- [ ] `docs/reviews/order.md` has every slice with the fields of § 6; the first three slices are each under about 12,000 read lines or one package group; Tier 1's launch, control and state slice and the interface's launch-path slice are among the first three; the review status line is present.
- [ ] The proposed order and slice list were posted on #641 and the maintainer's yes is recorded there before any slice issue was filed.
- [ ] Every slice has its issue as a sub-issue of #339, titled `M6.P2 E339/T<k>: <area>: <slice>`, paths named, `reviewed-at` and `fixed-at` empty; `tools/box-check` passes on all of them, output pasted on #641.
- [ ] The preliminary review ran per `review-formats.md` (the contract under `research/preliminary-reviews/<run-id>/`, three seats verified) or `order.md` records why not and `status.md` shows `order: unreviewed`; each material objection is answered by name.
- [ ] `tools/renovation-drift` and `tools/renovation-status` exist, are listed in the three places, and `docs/reviews/status.md` has the `order:` row and one `unreviewed` row per slice.
- [ ] `tools/lint-audit-artifacts` carries the renovation face check and its fixture proves it fails a folder without the seven questions and passes one with them.
- [ ] The register row exists with the ID rule of § 6 followed; #339 links `order.md`; the M6 body names the first slice as NEXT, read back.
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch; the five exit codes pasted on #641.

## 8. Stop conditions

Stop only on: every item of § 7 ticked and the branch pushed; the **pass-7
gate** (passes 1 to 6 are authorized by the dispatch; before filing the
slice issues and the order's register row, post the proposed order and the
slice list on #641 and wait for the maintainer's yes, continuing any
independent work meanwhile); an explicit maintainer pause on #641; a
blocker, named on #641 with what is needed (a count that cannot be produced
or two commands that disagree, a rule that forbids a step); or an execution
limit, stated as such with the tracking file current. A checkpoint is not a
stop (D-WORKFLOW-149): write it and take the next pass. A seat failing
verification is not a stop (§ 1). An idle session says it is idle.

## 9. Ceremonies owed

- The futro before pass 1 (§ 6), in the file and on #641.
- A work-log entry per session, headed by #641; `tools/work-log-index
  --write` after it; the weekly summary if the lane's week falls due
  (`ceremonies.md`).
- A friction line in `docs/friction-log.md` the moment something slows,
  with `issue: #641` or the guard.
- The mini-retro skill at the phase's close, posted on #641, with its scoped
  audit; findings that recur become a rule edit, a tool or a blindspot entry
  with its guard.
- The register row for the order (§ 6); any other decision the phase forces
  gets its row the same session.
- `tools/ceremony-check` before the push; what it reports as owed by this
  lane is paid before the push, what the other lane owes is noted on #641.
- Commit messages: the fork's style (`docs: ...`, `tools: ...`), `Refs
  #641` while any criterion is open, never a closing keyword.

## 10. Hand-back

The planner accepts P1 by reading, in this order, without re-running the
survey: the M6 body (current/next moved); `docs/reviews/status.md` (the
`order:` row and one row per slice, all `unreviewed`); `docs/reviews/order.md`
(the first three slices and their gates); the four counts and the five
checker exit codes pasted on #641; the tracking file's header and seven
passes; the retro's four answers. A brief that needed the planner's help
mid-phase is a defect in this brief: log the friction, and the planner fixes
the template in plan § 7 before the next brief is written.
