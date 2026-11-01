# Punch List — M6.P2 T38, the skills, agents and settings

**Generated:** 2026-11-01, by `tools/t38-punch.py` from one list (the items, the Phase 7 table and the index cannot disagree)
**Source Audit:** `04-analysis.md`; the leads are `02` § The leads
**Total Items:** 57 (Critical: 0, High: 0, Medium: 16, Low: 41)

---

## Instructions for the executing stream

Every item is **Open**: the stage-D pause's stream brief (`docs/reviews/briefs/t38-streams.md`, the coordinator's) decides each.
Items whose proposal reads `bug` are filed at stage D with their trace, their `Already written:` line and their VM line, *"Can this be done on
the VM? No -- the tree, the tool or the register shows it"*. A fix lands only in the fork-adapted skills, never in the council family
(ruling (d)); each fix's commit records its acceptance line before and after and `tools/t38-checks.sh`'s exit.

---

## PL-01: Phase 4.6 fails a Local epic-tier slice closed in four sentences and a table row

- **Severity:** Medium
- **Category:** Spec Drift
- **Question:** Q3
- **Source finding:** L-56
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:247`, `:508`; `references/phases.md:439`, `:486-491`; `references/review-levels.md:9`; `references/templates.md:94`, `:164` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each names D-WORKFLOW-184's Local epic-tier exception as `templates.md:144-146` does; `grep -c 'D-WORKFLOW-184'` over the five files prints a count in each
- **Ladder:** written -> audited by `tools/skills-check`'s contract step (#1373)
- **Proposed:** bug (stage D)

## PL-02: scoped-audit's pre-existing check pops the shared stash and fetches vitest

- **Severity:** Medium
- **Category:** Code Quality
- **Question:** Q3
- **Source finding:** L-10
- **Owner area:** mini-retro
- **Where:** `mini-retro/references/scoped-audit.md:347-359`, `:292-321` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the block uses a detached scratch worktree at `<base_sha>` and the repository's own checks; `sed -n '340,365p' | grep -c -E 'git stash( |$)|npx vitest'` prints `0`
- **Ladder:** written -> audited by `tools/skills-check`'s stale step (a bare `git stash` and `npx` as terms)
- **Proposed:** bug (stage D)

## PL-03: release-notes says fork-publish-release uploads the files

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q3
- **Source finding:** L-11
- **Owner area:** release-notes
- **Where:** `release-notes/SKILL.md:19-21` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the sentence says the tool prepares a plan (`--prepare`) and that publication waits on #265, #344 and #528; `sed -n '19,20p' | grep -c uploads` prints `0`
- **Ladder:** written -> no tool can (a sentence about another tool's behaviour)
- **Proposed:** bug (stage D)

## PL-04: code-auditor runs the lint with --issue before the issue exists, and never names --phase pre-issue

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q3
- **Source finding:** L-52
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:252-256` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the paragraph runs `--phase pre-issue` before Phase 6 and the default phase with `--issue <n>` after Phase 7; `git grep -c 'pre-issue'` over the skill prints a count
- **Ladder:** written -> audited by `tools/skills-check`'s contract step
- **Proposed:** bug (stage D)

## PL-05: futro's comment read uses gh api {owner}/{repo}

- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q3
- **Source finding:** L-13
- **Owner area:** futro
- **Where:** `futro/SKILL.md:479` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the command names `repos/pixelelated/distribution`; `grep -c -F '{owner}/{repo}'` prints `0`
- **Ladder:** written -> audited by `tools/skills-check`'s stale step
- **Proposed:** bug (stage D)

## PL-06: the evidence floor says three rules and numbers five 1, 2, 3, 4, 3

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-02
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:159`, `:161`-`:191`, `:370`; `references/phases.md:60` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** five rules numbered 1 to 5, the count said, both citations of the subagent rule moved; `sed -n '157,200p' | grep -c -E '^3\. \*\*'` prints `1`
- **Ladder:** written -> audited by `tools/skills-check` (a numbered list's count against its sentence)
- **Proposed:** punch

## PL-07: templates.md's scorecard heading fails the lint

- **Severity:** Medium
- **Category:** Spec Drift
- **Question:** Q3
- **Source finding:** L-60
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/templates.md:23` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** `## Acceptance-criteria scorecard`; `tools/t38-checks.sh`'s contract step passes without its allow-findings entry
- **Ladder:** evidenced -> audited by `tools/t38-checks.sh`'s contract step, then #1373's
- **Proposed:** punch

## PL-08: the scoped audit's checks are counted ten, nine, six, nine and five

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-63
- **Owner area:** mini-retro, begin-delivery
- **Where:** `mini-retro/SKILL.md:199-252`, `:353-358`; `mini-retro/references/template.md:71-79`; `begin-delivery/SKILL.md:168-171` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one count; the format and the template list the ten checks; `tools/t38-tables.py q4` (c) prints `yes` for each row
- **Ladder:** written -> audited by `tools/t38-tables.py q4`'s counts, then #1373's
- **Proposed:** punch

## PL-09: phases.md says Epic tier trusts the retros while SKILL.md says re-derive two

- **Severity:** Medium
- **Category:** Spec Drift
- **Question:** Q7
- **Source finding:** L-57
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/phases.md:71-72` against `SKILL.md:110` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** `phases.md` states the re-derivation quota as `SKILL.md` does
- **Ladder:** written -> no tool can (two texts' meanings)
- **Proposed:** punch

## PL-10: phases.md says the repo has no artifact lint, so verify by hand

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-59
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/phases.md:574-577`; `references/anti-patterns.md:26` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** Phase 5's final step runs `tools/lint-audit-artifacts --phase pre-issue`; `grep -c 'none today'` prints `0`
- **Ladder:** written -> audited by `tools/skills-check`'s stale step
- **Proposed:** punch

## PL-11: Phase 0's stale-copy check reads SKILL.md alone

- **Severity:** Medium
- **Category:** Test Gap
- **Question:** Q3
- **Source finding:** L-53
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:278-281` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the check compares the whole skill directory, and says a renovation lane reads the dispatch tip's skill; the block at this tip prints the `templates.md` difference
- **Ladder:** written -> no tool can until #1373 checks the block
- **Proposed:** punch

## PL-12: futro MUSTs a git fetch origin main this repository cannot run

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q3
- **Source finding:** L-66
- **Owner area:** futro
- **Where:** `futro/SKILL.md:207-230` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the base-divergence check compares against `next` with no fetch; `grep -c 'origin/main'` prints `0`
- **Ladder:** written -> audited by `tools/skills-check`'s stale step (`origin/main`)
- **Proposed:** punch

## PL-13: session-stash's exact template has no Start here

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q2
- **Source finding:** L-69
- **Owner area:** session-stash
- **Where:** `session-stash/SKILL.md:64-117` against `:32` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the template opens with `## Start here`; `grep -c '^## Start here'` over the skill prints `1`
- **Ladder:** written -> audited by `tools/skills-check` (the template's headings against learning-capture.md § 4)
- **Proposed:** punch

## PL-14: release-notes' description promises PR bodies a details block the body forbids

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q5
- **Source finding:** L-70
- **Owner area:** release-notes
- **Where:** `release-notes/SKILL.md:3` against `:97-102` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the description says the details block is the release note's only; its length recorded before and after
- **Ladder:** written -> no tool can (the description's meaning)
- **Proposed:** punch

## PL-15: mini-retro's order of Step 2.5 and its two closing lists

- **Severity:** Medium
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-81
- **Owner area:** mini-retro
- **Where:** `mini-retro/SKILL.md:187-189`, `:152`, `:351`, `:461-462`; `references/scoped-audit.md:3-6`; `references/template.md:137-152` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one order for Step 2.5, one closing list, no self-referring Step 7
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-16: code-auditor names no completion marker and no held-reply sidecar

- **Severity:** Medium
- **Category:** Missing Artifact
- **Question:** Q2
- **Source finding:** L-06, L-07
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:555-617`; `references/templates.md` (second-opinions layout) (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** Phase 7 names `docs/audits/<scope>/audit-completion.json` (#540) and the layout names `<reply>.held.json` (#1308); the stage-A check prints a line each
- **Ladder:** written -> audited by `tools/ceremony-check`'s completed-audit marker
- **Proposed:** punch

## PL-17: futro and mini-retro write their artifacts to homes the ceremonies do not read

- **Severity:** Medium
- **Category:** Missing Artifact
- **Question:** Q2
- **Source finding:** L-08, L-20
- **Owner area:** futro, mini-retro
- **Where:** `futro/SKILL.md:379-388`; `futro/references/template.md:3-4`; `mini-retro/SKILL.md:310-320`; `mini-retro/references/template.md:3-4`; `session-stash/SKILL.md:60` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each artifact step names `docs/futros/<date>-<scope>.md` or `docs/retros/<date>-<scope>.md` (or the work-log heading) and `tools/ceremony-check`
- **Ladder:** written -> audited by `tools/ceremony-check`
- **Proposed:** punch

## PL-18: code-auditor's Twelve recorded failure modes

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-03
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:420` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** no number, or one a command prints; `grep -c 'Twelve recorded'` prints `0`
- **Ladder:** written -> audited by `tools/t38-tables.py q4`'s counts
- **Proposed:** punch

## PL-19: code-auditor's legacy worktree layout

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-04
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:711` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the layout the lanes use, #640 named; `grep -c 'rocknix\.worktrees'` prints `0`
- **Ladder:** written -> audited by `tools/skills-check`'s stale step
- **Proposed:** punch

## PL-20: durations used as estimates

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q2
- **Source finding:** L-05
- **Owner area:** code-auditor, mini-retro, begin-delivery, futro
- **Where:** the widened pattern's 10 lines (stage A) and `code-auditor/SKILL.md:612`, `begin-delivery/SKILL.md:256`, `mini-retro/SKILL.md:189`, `scoped-audit.md:8-9`, `futro/SKILL.md:377`, `futro/references/blindspot-register.md:74-78` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** every estimate gone or an ordering (D-WORKFLOW-091); the widened pattern prints `0`; `code-auditor/SKILL.md:3`'s length before and after
- **Ladder:** written -> audited by `tools/skills-check`'s stale step (#342)
- **Proposed:** punch

## PL-21: a main branch this repository has not

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-09
- **Owner area:** session-stash, session-resume
- **Where:** `session-stash/SKILL.md:7`, `:34-41`; `session-resume/SKILL.md:7`, `:30` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the main rules gone; `git grep -c 'saved-session-state-main'` prints `0`
- **Ladder:** written -> audited by `tools/t38-checks.sh`'s stale step (`state-main`)
- **Proposed:** punch

## PL-22: Copilot-era rule-file names and a missing agent-terminal-safety rule

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-12, L-73
- **Owner area:** code-auditor, mini-retro, begin-delivery
- **Where:** `code-auditor/SKILL.md:366`, `:425`, `:432`; `scoped-audit.md:209`; `begin-delivery/SKILL.md:466` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each points at its `.claude/rules/` successor or is dropped
- **Ladder:** written -> audited by `tools/skills-check`'s refs step
- **Proposed:** punch

## PL-23: Copilot's mcp_github_* names and the advice to avoid gh

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-14, L-21
- **Owner area:** all six imported skills
- **Where:** `futro/SKILL.md:79-81`, `:112`; `mini-retro/SKILL.md:116-118`; `begin-delivery/SKILL.md:136-141`, `:154`, `:284`, `:384`, `:440`; `code-auditor/SKILL.md:365`; `phases.md:31`, `:587`; `anti-patterns.md:20`; `session-resume/SKILL.md:49`; `session-stash/SKILL.md:57`; `futro/references/techniques.md:28`, `:35`; `futro/references/template.md:72` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one shared sentence with `mcp__github__*` and `gh --repo pixelelated/distribution`; the stale step's `copilot` count over the fork-adapted skills prints `0`
- **Ladder:** written -> audited by `tools/t38-checks.sh`'s stale step
- **Proposed:** punch

## PL-24: the source estate's checks, stacks and examples kept as this repository's

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-15
- **Owner area:** all six imported skills
- **Where:** `02` § The leads, L-15's row (mini-retro, scoped-audit, code-auditor, futro, begin-delivery, session-resume, session-stash) (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each replaced with this repository's checks and examples or dropped, one stream per skill
- **Ladder:** written -> audited by `tools/skills-check`'s stale step (the estate's terms)
- **Proposed:** punch

## PL-25: another estate's issue numbers cited as this tracker's

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q6
- **Source finding:** L-58
- **Owner area:** code-auditor, mini-retro, futro, begin-delivery
- **Where:** `02` § The leads, L-58's row; `futro/SKILL.md:163-164` (`audit #203`) (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each citation names its estate or is dropped; `#203` no longer cited as an audit
- **Ladder:** written -> audited by `tools/skills-check` (a `#N` above the tracker's highest)
- **Proposed:** punch

## PL-26: version histories inside procedures

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q5
- **Source finding:** L-16
- **Owner area:** begin-delivery, code-auditor
- **Where:** `begin-delivery/SKILL.md:541-609`; `code-auditor/SKILL.md:8-9` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the histories in the commit log; the front matter's note shortened, its length recorded
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-27: futro's blindspot register 'when created'

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-17
- **Owner area:** futro
- **Where:** `futro/SKILL.md:426-435`, `:480` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the sentence names `docs/blindspot-register.md`; the starter stays a starter
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-28: session-stash's stranger's proof is stated in no step

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q2
- **Source finding:** L-19
- **Owner area:** session-stash
- **Where:** `session-stash/SKILL.md:32` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** Step 3 carries the proof as a step
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-29: templates.md's Local example writes anthropic/claude-opus-5.5

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q3
- **Source finding:** L-51
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/templates.md:136` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** `anthropic/claude-opus-5-5`; `grep -c -F 'anthropic/claude-opus-5.5'` prints `0`
- **Ladder:** written -> audited by `tools/skills-check`'s stale step
- **Proposed:** punch

## PL-30: subagents do not inherit terminal access

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q1
- **Source finding:** L-54
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:369`, `:682`; `phases.md:61`, `:593`; `anti-patterns.md:18` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the sentence says what the harness does
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-31: Phase Z.6, PZ, Outcome A/B and P7, defined nowhere

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q6
- **Source finding:** L-55
- **Owner area:** code-auditor, mini-retro
- **Where:** `code-auditor/SKILL.md:659-661`; `mini-retro/SKILL.md:269`; `scoped-audit.md:39`, `:703`, `:519-520`, `:576-577`; `mini-retro/references/template.md:105` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each defined or replaced with this repository's words
- **Ladder:** written -> audited by `tools/skills-check` (an undefined token list)
- **Proposed:** punch

## PL-32: templates.md's escaped fences

- **Severity:** Low
- **Category:** Code Quality
- **Question:** Q7
- **Source finding:** L-61
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/templates.md:236`, `:247` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** a nested fence that copies as one
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-33: the criterion entry 'reproduced' in templates.md has drifted

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-62
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/templates.md:268-295` against `phases.md:146-172` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one copy, or `tools/t38-tables.py q7` prints no difference
- **Ladder:** evidenced -> audited by `tools/t38-tables.py q7`
- **Proposed:** punch

## PL-34: the full 6-phase methodology

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-64
- **Owner area:** mini-retro, code-auditor
- **Where:** `mini-retro/SKILL.md:547-548`; `code-auditor/SKILL.md:84-85` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the phases named, not counted
- **Ladder:** written -> audited by `tools/t38-tables.py q4`'s counts
- **Proposed:** punch

## PL-35: scoped-audit's reference/template.md and cornerstone-conformance.md

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q6
- **Source finding:** L-65
- **Owner area:** mini-retro
- **Where:** `mini-retro/references/scoped-audit.md:71`, `:176` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each path resolves or is dropped; `tools/t38-checks.sh`'s refs step without the entry
- **Ladder:** evidenced -> audited by `tools/t38-checks.sh`'s refs step
- **Proposed:** punch

## PL-36: futro's four techniques, five listed, three in the template

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-67
- **Owner area:** futro
- **Where:** `futro/SKILL.md:288`; `futro/references/techniques.md:3-5`, `:264`; `futro/references/template.md:68` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one list and its count
- **Ladder:** written -> audited by `tools/t38-tables.py q4`'s counts
- **Proposed:** punch

## PL-37: review-levels.md's status line for #375

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-71
- **Owner area:** code-auditor
- **Where:** `code-auditor/references/review-levels.md:41-44` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the status line gone (#375 is closed)
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-38: code-auditor's list of the checks that exist here

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-72
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:171-177` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the list points at `instruction-files.md`'s tool table
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-39: the audit issue's checkbox shape (D-QA-044, #268)

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q2
- **Source finding:** L-74
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:541-552` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** Phase 6 gives `- [ ] <behaviour> -- <artifact>` and `tools/box-check --issue N`
- **Ladder:** written -> audited by `tools/box-check`
- **Proposed:** punch

## PL-40: register sections futro and begin-delivery cite and no register has

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q6
- **Source finding:** L-75
- **Owner area:** futro, begin-delivery
- **Where:** `futro/SKILL.md:141-143`, `:258-259`; `begin-delivery/SKILL.md:491-492` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each cites an entry `docs/blindspot-register.md` holds, or drops the citation
- **Ladder:** written -> audited by `tools/skills-check` (a register section named)
- **Proposed:** punch

## PL-41: developer-relations' dash, split list and walk counts

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-79
- **Owner area:** developer-relations
- **Where:** `developer-relations/SKILL.md:103-104`, `:116-135`, `:178`, `:181-183` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each read once by a no-context reader without the stumble
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-42: release-notes' claims about its tools, and RC1

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source finding:** L-80
- **Owner area:** release-notes
- **Where:** `release-notes/SKILL.md:66`, `:68`, `:119-121`, `:125` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each claim the tool's own (`prose-check`'s strict paths; `pr-stack-check`'s `BANNED`)
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-43: futro's thresholds, the committed comment and the heading levels

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-82
- **Owner area:** futro
- **Where:** `futro/SKILL.md:339-341`, `:401-413`, `:462-464`; `futro/references/template.md:10`, `:20` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one threshold; the commit step said; the template's `## 1.` as the futros use
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-44: begin-delivery's own history and step order

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-83
- **Owner area:** begin-delivery
- **Where:** `begin-delivery/SKILL.md:207`, `:212-215`, `:392`, `:401`, `:469` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** one order, the history consistent
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-45: the session skills' stat, staleness tiers and approval

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-84
- **Owner area:** session-resume, session-stash
- **Where:** `session-resume/SKILL.md:40`, `:42`, `:45`, `:112`; `session-stash/SKILL.md:30`, `:38` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each sentence a reader can act on
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-46: code-auditor's tiers, mode trigger and phase counts

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q7
- **Source finding:** L-85
- **Owner area:** code-auditor
- **Where:** `code-auditor/SKILL.md:77`, `:92`, `:612`, `:623`, `:665`; `phases.md:3`, `:353`, `:412` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** each said once
- **Ladder:** written -> no tool can
- **Proposed:** punch

## PL-47: begin-exploration: write the skill or sweep the references

- **Severity:** Medium
- **Category:** Improvement
- **Question:** Q6
- **Source finding:** L-22
- **Owner area:** the maintainer, the coordinator
- **Where:** 19 lines of the 52 (`02` § The leads, L-22's row); `adversarial-council.md:36-38` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the maintainer's answer recorded on #685, then the stream that applies it
- **Ladder:** routed -> audited by `tools/t38-checks.sh`'s refs step once swept
- **Proposed:** question (the pause)

## PL-48: the renovation face in code-auditor or in the plan

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q7
- **Source finding:** L-24
- **Owner area:** the coordinator
- **Where:** `code-auditor/**` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator's ruling recorded
- **Ladder:** written -> no tool can
- **Proposed:** question (the pause)

## PL-49: the levels' third lab and D-WORKFLOW-195

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q4
- **Source finding:** L-28
- **Owner area:** the coordinator
- **Where:** `code-auditor/references/review-levels.md:11`, `:48-51` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator's ruling recorded
- **Ladder:** written -> no tool can
- **Proposed:** question (the pause)

## PL-50: the continuity section and the payload's pid

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q2
- **Source finding:** L-29
- **Owner area:** the coordinator
- **Where:** `code-auditor/SKILL.md:28-57` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator's ruling recorded
- **Ladder:** written -> no tool can
- **Proposed:** question (the pause)

## PL-51: a working branch's session file: pointer or state

- **Severity:** Low
- **Category:** Spec Drift
- **Question:** Q7
- **Source finding:** L-68
- **Owner area:** the coordinator
- **Where:** `session-resume/SKILL.md:26`; #1014 (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator's ruling recorded, then the stream
- **Ladder:** written -> audited by #1014's freshness check
- **Proposed:** question (the pause)

## PL-52: #645's checkbox against D-WORKFLOW-078

- **Severity:** Low
- **Category:** Spec Drift
- **Question:** Q2
- **Source finding:** L-27
- **Owner area:** the coordinator
- **Where:** #645 `:25`; `release-notes/SKILL.md:93-99` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator's ruling on #645 recorded
- **Ladder:** written -> no tool can
- **Proposed:** question (the pause)

## PL-53: the export's refresh list

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q6
- **Source finding:** L-30 to L-50, L-76 to L-78
- **Owner area:** #911
- **Where:** `02` § The leads and § What ... inherit (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** #911 carries the list; the export refreshed by copying
- **Ladder:** written -> audited by `tools/skills-check` over the export (#1373)
- **Proposed:** inherit:#911

## PL-54: council-research kept or retired

- **Severity:** Low
- **Category:** Improvement
- **Question:** Q5
- **Source finding:** L-47
- **Owner area:** the maintainer, #911
- **Where:** `council-research/**` (4,150 lines) (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the maintainer's answer on #807, then #911's refresh
- **Ladder:** written -> no tool can
- **Proposed:** inherit:#911

## PL-55: the rule errata

- **Severity:** Low
- **Category:** Spec Drift
- **Question:** Q1
- **Source finding:** L-22's rule half, L-23, L-50, D-QA-040, worktrees.md, the lost spaces
- **Owner area:** the coordinator
- **Where:** `02` § What ... inherit (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator's sweep
- **Ladder:** written -> audited by `tools/archaeology --reversal`
- **Proposed:** inherit:coordinator

## PL-56: tools/skills-check's inputs

- **Severity:** Low
- **Category:** Test Gap
- **Question:** Q2
- **Source finding:** the checker's steps; register-check's LIVE
- **Owner area:** #1373
- **Where:** `tools/t38-checks.sh`, `tools/allow-*.txt`; `tools/register-check:49` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** #1373 carries them
- **Ladder:** evidenced -> audited once #1373 is wired
- **Proposed:** inherit:#1373

## PL-57: Backlog leads: the stash archive's tool and the roster's prose copies

- **Severity:** Low
- **Category:** Test Gap
- **Question:** Q6
- **Source finding:** L-18, L-44
- **Owner area:** the coordinator
- **Where:** `session-stash/SKILL.md:28`; `council/references/member-roster.md:19-25` (lines at the dispatch tip `87c2ab0fed`)
- **Acceptance:** the coordinator files them
- **Ladder:** written -> audited by the tool each Backlog asks for
- **Proposed:** inherit:coordinator

## Pre-existing tracked scope (NOT punch items -- exempt from the Phase 7 gate)

- #810 -- the lint's Local epic tier; closes when `templates.md`'s fix reaches `next` (PL-01 is outside its checkbox)
- #342 -- time-free estimates; PL-20 answers it for the fork-adapted skills
- #640 -- the layout's drift; PL-19 names it
- #1044, #1045 -- the export's toolchain and refresh; PL-53 carries the export's list

- #314, #287 -- L-26: neither checkbox is met by the skill's text; each stays with its issue or goes to the stream brief

## Leads with no item of their own

Every one of the 85 leads in `02` § The leads is cited by an item above or listed here; the generator refuses otherwise.

- L-01 -- the drift overview; its in-scope halves are PL-07 (L-60) and PL-29 (L-51), its council half #911's (PL-53)
- L-25 -- a positive: no `TOTAL:` a reader would compute by hand (`02` § Positives)
- L-26 -- #314 `:14` and #287 `:16`: each issue's own checkbox, pre-existing tracked scope below

## Phase 7 resolution gate

| Item | Outcome | Proposed at stage B/C |
| --- | --- | --- |
| PL-01 | Open | bug (stage D) |
| PL-02 | Open | bug (stage D) |
| PL-03 | Open | bug (stage D) |
| PL-04 | Open | bug (stage D) |
| PL-05 | Open | bug (stage D) |
| PL-06 | Open | punch |
| PL-07 | Open | punch |
| PL-08 | Open | punch |
| PL-09 | Open | punch |
| PL-10 | Open | punch |
| PL-11 | Open | punch |
| PL-12 | Open | punch |
| PL-13 | Open | punch |
| PL-14 | Open | punch |
| PL-15 | Open | punch |
| PL-16 | Open | punch |
| PL-17 | Open | punch |
| PL-18 | Open | punch |
| PL-19 | Open | punch |
| PL-20 | Open | punch |
| PL-21 | Open | punch |
| PL-22 | Open | punch |
| PL-23 | Open | punch |
| PL-24 | Open | punch |
| PL-25 | Open | punch |
| PL-26 | Open | punch |
| PL-27 | Open | punch |
| PL-28 | Open | punch |
| PL-29 | Open | punch |
| PL-30 | Open | punch |
| PL-31 | Open | punch |
| PL-32 | Open | punch |
| PL-33 | Open | punch |
| PL-34 | Open | punch |
| PL-35 | Open | punch |
| PL-36 | Open | punch |
| PL-37 | Open | punch |
| PL-38 | Open | punch |
| PL-39 | Open | punch |
| PL-40 | Open | punch |
| PL-41 | Open | punch |
| PL-42 | Open | punch |
| PL-43 | Open | punch |
| PL-44 | Open | punch |
| PL-45 | Open | punch |
| PL-46 | Open | punch |
| PL-47 | Open | question (the pause) |
| PL-48 | Open | question (the pause) |
| PL-49 | Open | question (the pause) |
| PL-50 | Open | question (the pause) |
| PL-51 | Open | question (the pause) |
| PL-52 | Open | question (the pause) |
| PL-53 | Open | inherit:#911 |
| PL-54 | Open | inherit:#911 |
| PL-55 | Open | inherit:coordinator |
| PL-56 | Open | inherit:#1373 |
| PL-57 | Open | inherit:coordinator |

## Machine-readable index

```yaml
punch_index:
- id: PL-01
  severity: Medium
  category: Spec Drift
  question: Q3
  source_finding: "L-56"
  owner_area: "code-auditor"
  outcome: open
  proposed: "bug (stage D)"
- id: PL-02
  severity: Medium
  category: Code Quality
  question: Q3
  source_finding: "L-10"
  owner_area: "mini-retro"
  outcome: open
  proposed: "bug (stage D)"
- id: PL-03
  severity: Medium
  category: Documentation Gap
  question: Q3
  source_finding: "L-11"
  owner_area: "release-notes"
  outcome: open
  proposed: "bug (stage D)"
- id: PL-04
  severity: Low
  category: Documentation Gap
  question: Q3
  source_finding: "L-52"
  owner_area: "code-auditor"
  outcome: open
  proposed: "bug (stage D)"
- id: PL-05
  severity: Low
  category: Code Quality
  question: Q3
  source_finding: "L-13"
  owner_area: "futro"
  outcome: open
  proposed: "bug (stage D)"
- id: PL-06
  severity: Medium
  category: Documentation Gap
  question: Q7
  source_finding: "L-02"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-07
  severity: Medium
  category: Spec Drift
  question: Q3
  source_finding: "L-60"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-08
  severity: Medium
  category: Documentation Gap
  question: Q4
  source_finding: "L-63"
  owner_area: "mini-retro, begin-delivery"
  outcome: open
  proposed: "punch"
- id: PL-09
  severity: Medium
  category: Spec Drift
  question: Q7
  source_finding: "L-57"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-10
  severity: Medium
  category: Documentation Gap
  question: Q1
  source_finding: "L-59"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-11
  severity: Medium
  category: Test Gap
  question: Q3
  source_finding: "L-53"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-12
  severity: Medium
  category: Documentation Gap
  question: Q3
  source_finding: "L-66"
  owner_area: "futro"
  outcome: open
  proposed: "punch"
- id: PL-13
  severity: Medium
  category: Documentation Gap
  question: Q2
  source_finding: "L-69"
  owner_area: "session-stash"
  outcome: open
  proposed: "punch"
- id: PL-14
  severity: Medium
  category: Documentation Gap
  question: Q5
  source_finding: "L-70"
  owner_area: "release-notes"
  outcome: open
  proposed: "punch"
- id: PL-15
  severity: Medium
  category: Documentation Gap
  question: Q7
  source_finding: "L-81"
  owner_area: "mini-retro"
  outcome: open
  proposed: "punch"
- id: PL-16
  severity: Medium
  category: Missing Artifact
  question: Q2
  source_finding: "L-06, L-07"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-17
  severity: Medium
  category: Missing Artifact
  question: Q2
  source_finding: "L-08, L-20"
  owner_area: "futro, mini-retro"
  outcome: open
  proposed: "punch"
- id: PL-18
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: "L-03"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-19
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-04"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-20
  severity: Low
  category: Improvement
  question: Q2
  source_finding: "L-05"
  owner_area: "code-auditor, mini-retro, begin-delivery, futro"
  outcome: open
  proposed: "punch"
- id: PL-21
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-09"
  owner_area: "session-stash, session-resume"
  outcome: open
  proposed: "punch"
- id: PL-22
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-12, L-73"
  owner_area: "code-auditor, mini-retro, begin-delivery"
  outcome: open
  proposed: "punch"
- id: PL-23
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-14, L-21"
  owner_area: "all six imported skills"
  outcome: open
  proposed: "punch"
- id: PL-24
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-15"
  owner_area: "all six imported skills"
  outcome: open
  proposed: "punch"
- id: PL-25
  severity: Low
  category: Documentation Gap
  question: Q6
  source_finding: "L-58"
  owner_area: "code-auditor, mini-retro, futro, begin-delivery"
  outcome: open
  proposed: "punch"
- id: PL-26
  severity: Low
  category: Improvement
  question: Q5
  source_finding: "L-16"
  owner_area: "begin-delivery, code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-27
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-17"
  owner_area: "futro"
  outcome: open
  proposed: "punch"
- id: PL-28
  severity: Low
  category: Documentation Gap
  question: Q2
  source_finding: "L-19"
  owner_area: "session-stash"
  outcome: open
  proposed: "punch"
- id: PL-29
  severity: Low
  category: Documentation Gap
  question: Q3
  source_finding: "L-51"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-30
  severity: Low
  category: Documentation Gap
  question: Q1
  source_finding: "L-54"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-31
  severity: Low
  category: Documentation Gap
  question: Q6
  source_finding: "L-55"
  owner_area: "code-auditor, mini-retro"
  outcome: open
  proposed: "punch"
- id: PL-32
  severity: Low
  category: Code Quality
  question: Q7
  source_finding: "L-61"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-33
  severity: Low
  category: Documentation Gap
  question: Q7
  source_finding: "L-62"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-34
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: "L-64"
  owner_area: "mini-retro, code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-35
  severity: Low
  category: Documentation Gap
  question: Q6
  source_finding: "L-65"
  owner_area: "mini-retro"
  outcome: open
  proposed: "punch"
- id: PL-36
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: "L-67"
  owner_area: "futro"
  outcome: open
  proposed: "punch"
- id: PL-37
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: "L-71"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-38
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: "L-72"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-39
  severity: Low
  category: Improvement
  question: Q2
  source_finding: "L-74"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-40
  severity: Low
  category: Documentation Gap
  question: Q6
  source_finding: "L-75"
  owner_area: "futro, begin-delivery"
  outcome: open
  proposed: "punch"
- id: PL-41
  severity: Low
  category: Documentation Gap
  question: Q7
  source_finding: "L-79"
  owner_area: "developer-relations"
  outcome: open
  proposed: "punch"
- id: PL-42
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: "L-80"
  owner_area: "release-notes"
  outcome: open
  proposed: "punch"
- id: PL-43
  severity: Low
  category: Documentation Gap
  question: Q7
  source_finding: "L-82"
  owner_area: "futro"
  outcome: open
  proposed: "punch"
- id: PL-44
  severity: Low
  category: Documentation Gap
  question: Q7
  source_finding: "L-83"
  owner_area: "begin-delivery"
  outcome: open
  proposed: "punch"
- id: PL-45
  severity: Low
  category: Documentation Gap
  question: Q7
  source_finding: "L-84"
  owner_area: "session-resume, session-stash"
  outcome: open
  proposed: "punch"
- id: PL-46
  severity: Low
  category: Documentation Gap
  question: Q7
  source_finding: "L-85"
  owner_area: "code-auditor"
  outcome: open
  proposed: "punch"
- id: PL-47
  severity: Medium
  category: Improvement
  question: Q6
  source_finding: "L-22"
  owner_area: "the maintainer, the coordinator"
  outcome: open
  proposed: "question (the pause)"
- id: PL-48
  severity: Low
  category: Improvement
  question: Q7
  source_finding: "L-24"
  owner_area: "the coordinator"
  outcome: open
  proposed: "question (the pause)"
- id: PL-49
  severity: Low
  category: Improvement
  question: Q4
  source_finding: "L-28"
  owner_area: "the coordinator"
  outcome: open
  proposed: "question (the pause)"
- id: PL-50
  severity: Low
  category: Improvement
  question: Q2
  source_finding: "L-29"
  owner_area: "the coordinator"
  outcome: open
  proposed: "question (the pause)"
- id: PL-51
  severity: Low
  category: Spec Drift
  question: Q7
  source_finding: "L-68"
  owner_area: "the coordinator"
  outcome: open
  proposed: "question (the pause)"
- id: PL-52
  severity: Low
  category: Spec Drift
  question: Q2
  source_finding: "L-27"
  owner_area: "the coordinator"
  outcome: open
  proposed: "question (the pause)"
- id: PL-53
  severity: Low
  category: Improvement
  question: Q6
  source_finding: "L-30 to L-50, L-76 to L-78"
  owner_area: "#911"
  outcome: open
  proposed: "inherit:#911"
- id: PL-54
  severity: Low
  category: Improvement
  question: Q5
  source_finding: "L-47"
  owner_area: "the maintainer, #911"
  outcome: open
  proposed: "inherit:#911"
- id: PL-55
  severity: Low
  category: Spec Drift
  question: Q1
  source_finding: "L-22's rule half, L-23, L-50, D-QA-040, worktrees.md, the lost spaces"
  owner_area: "the coordinator"
  outcome: open
  proposed: "inherit:coordinator"
- id: PL-56
  severity: Low
  category: Test Gap
  question: Q2
  source_finding: "the checker's steps; register-check's LIVE"
  owner_area: "#1373"
  outcome: open
  proposed: "inherit:#1373"
- id: PL-57
  severity: Low
  category: Test Gap
  question: Q6
  source_finding: "L-18, L-44"
  owner_area: "the coordinator"
  outcome: open
  proposed: "inherit:coordinator"
```
