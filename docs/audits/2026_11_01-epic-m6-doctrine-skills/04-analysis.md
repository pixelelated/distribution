# Analysis — M6.P2 T38, the skills, agents and settings

**Date:** 2026-11-01
**Spec:** `docs/reviews/briefs/doctrine-skills.md` version 2 (`fa4a9a5b0d`) with its errata; #685's body (22 criteria)
**Issues:** #685 (the slice), #807 (the doctrine epic), #911 (the export's refresh), #1373 (`tools/skills-check`)
**Commits:** read at the dispatch tip `87c2ab0fed`; the stage-A record at `98019cea9f`; stage B's record on top of it

---

## Executive summary

T38 read the 52 paths of `.claude/**` less `.claude/rules/**`: ten skills and eight agent definitions, 12,783 lines at the dispatch tip and 12,734 at the P1 hash. Each was read first by a no-context reader, then by the lane, in ruling (j)'s order. The lens was cost against value. Nothing under `.claude/` was edited; stage B proposes, and the coordinator's stream brief decides.

**The fork-adapted skills are right where the fork wrote them and wrong where it did not revisit what was beside them.** Of the read's 85 leads:
- **The 50 whose owner is the T38 stream** (`02` § The leads, counted by `stage-b/summary-figures.sh`) fall into four families:
  - counts left as they were when a rule was added: L-02, L-63, L-64, L-67;
  - an exception landed in one file and refused in four others: L-56;
  - the source estate's names, stacks and incident numbers kept as if they were this repository's: L-15, L-58;
  - sentences true when written and retired since: L-11, L-09, L-66.
- **Five are proposed as bugs** under ruling (c) -- sentences a reader acts on wrongly:
  - L-10: the stash block;
  - L-11: the publish path;
  - L-13: `gh api {owner}/{repo}`;
  - L-52: the lint's two phases;
  - L-56: Phase 4.6 against Local depth.
- **The council family's findings,** L-30 to L-50 and L-76 to L-78, are the export's, inherited for #911 and never edited. L-32 is withdrawn and L-35 narrowed by reading.

**What the slice costs a session is mostly the council family's.** Its 35 files are 7,234 lines of the 12,783 and ten of the eighteen descriptions every session lists (`stage-b/tables/q5.md`, summed by `stage-b/summary-figures.sh`). `council-research` (4,150 lines, 752 characters of description) has kept no run. The six workflow skills are what the renovation's own procedure runs on, and they carry its two highest-yield faults: the template and the lint disagree on one heading (L-60), and the procedure halts a Local slice at Phase 4.6 (L-56). Every brief has worked around both. **Time to play is untouched**: the 52 load in an agent's session, never on an image.

## Acceptance-criteria scorecard

#685's 22 criteria at the end of stage E (stage B's verdicts are in `168bbba783`, stage C's in `8c76ca62d3`, stage D's in `e93c13457e`). Each is ticked by the coordinator at acceptance, from its artifact.

| Criterion | Verdict at stage E | Notes |
| --- | --- | --- |
| 1 the folder's files | PARTIAL ⚠ | `00` to `05`, `second-opinions/`, `stage-a/` to `stage-e/` and `tools/` exist; `audit-completion.json` is stage F's |
| 2 the lint `PASS`, Q1 to Q7, `question:` | PASS ✓ | the default phase `PASS`, and with `--issue 1394` (`stage-e/S0-closing-lint.out`, E-S0); every item with its `question:` |
| 3 the Local plan | PASS ✓ | `review-plan.json` `local`, no reviewer, `tier_exception` `D-WORKFLOW-184` (C-01); no keyed call (`00`'s census) |
| 4 the punch-list issue at Phase 7 | PARTIAL ⚠ | every item at a Phase 7 outcome in `05` (51 Resolved, 6 Deferred); #1394 `box-check` `0 fail`; its checkboxes and its close are the coordinator's, at acceptance |
| 5 `reviewed-at:` / `fixed-at:` | PARTIAL ⚠ | `05` carries `reviewed-at: 87c2ab0fed` and `fixed-at: 420b845656`; #685's header is the hand-back's |
| 6 `01` § Scope, the block and both totals | PASS ✓ | A-02, A-03 |
| 7 `01` § Scope, the drift; § Read order | PASS ✓ | A-03, `stage-a/moved-commits.out`; `01` § Read order |
| 8 `00`, the lint's Local proof first | PASS ✓ | A-01 |
| 9 `02` § Coverage, 52 rows with origin | PASS ✓ | the `awk` of the criterion prints `52` |
| 10 `02` § The runs | PASS ✓ | every run with its line and exit; `rules-check` *no evidence for the 52* |
| 11 `tools/t38-checks.sh`, its four runs | PARTIAL ⚠ | runs 1 to 3 at stage C; exit 0 at every stage-E commit, `TOTAL: 962 of 962` at `fixed-at`; run 4 (`--withhold findings`) is stage F's |
| 12 `02` § The names and the references | PASS ✓ | the tip's counts, the class counts, the three allowlists and the counts after stage E (`stage-e/S0-closing-stale-counts.txt`) |
| 13 `04` Q4's tables by a script | PASS ✓ | `tools/t38-tables.py q4`, its drift seen (B-19) |
| 14 Q5, Q6, the two questions posted | PASS ✓ | the tables and the two questions are below; posted as `6553169705` on #685 and `6553118160` on #807, cited in `02` and read back (D-06) |
| 15 every fix's lines in § The streams | PASS ✓ | eight stream rows and 60 fix-table rows, each lead FAIL at its parent and PASS at its fix (E-S0 to E-S7) |
| 16 § What ... inherit | PASS ✓ | `02`'s table, each row naming its owner |
| 17 the bugs, the ladder, the take-up rows, the rulings | PASS ✓ | #1389 to #1393, each with its trace, `Already written:` and VM line, `box-check` `0 fail` (D-01, D-02, D-07); the ladder in `05`; the take-up rows and the rulings in `02` |
| 18 `proved:` equals `PROOF:` | PASS ✓ | `58` and `58` at this commit |
| 19 no host-file line of this lane's | PASS ✓ | 689 lines at 02:44, `0` of this lane's; re-counted at the hand-back |
| 20 the retro | PARTIAL ⚠ | `docs/retros/2026-11-01-m6-doctrine-skills.md`, written at the amendment and posted on #685 after its commit, named in the second hand-back |
| 21 the checkers on the branch and the simulated merge | SKIP ○ | the hand-back's |
| 22 the hand-back, one tip, `box-check --issue 685` | SKIP ○ | stage H |

**Pass rate:** 15 of 22 met at stage E's amendment; 5 partial, each with its later stage named; 2 skipped as later stages' work (counted from the table by the command that wrote this line).

## Code Quality Assessment

### Strengths

- The fork's own additions are precise and current:
  - the *pixelelated continuation* sections (D-WORKFLOW-140);
  - item 5 of Check 7 (#1067);
  - the replaced-mechanism archetype (blindspot 23);
  - Step 1.7 against *assumed-undone* (blindspot 1);
  - the writing pair's first person singular (D-WORKFLOW-074) and its ban on any assistant upstream (D-WORKFLOW-078).
- The export's rules on its own seats are consistent: five or none, never a substitute, every call through the Facilitator. The roster agrees across three copies (B-21).

### Concerns

- A count or a cross-reference left behind each time a rule was added (L-02, L-56, L-59, L-63, L-67).
- The source estate's vocabulary throughout the six imported skills (L-15, L-58): *cornerstone*, `logs/audits/`, `example-api`, `vitest`, issues in the 2000s.
- Two reference copies of one passage that have drifted (L-62), and one passage shared word for word by three skills (`stage-b/tables/q7.md`).

### Complexity Hotspots

- `mini-retro/references/scoped-audit.md` (716 lines): ten checks, of which the format lists six.
- `council-research` (4,150 lines in 12 files), with a front-matter `origin` of several thousand characters (L-46).

## Cornerstone Conformance

This repository has no cornerstone rubric. Its doctrine is the rules under `.claude/rules/`, the blindspot register and the decision register (`code-auditor/SKILL.md:409-436`, read as the skill's own description of itself). **Overall: MEDIUM.** The rules the skills cite exist and are read at `3a9b0aec81`; the skills restate several of them in forms the rules have since changed (L-04, L-09, L-11, L-13, L-66); the three rule errata are the coordinator's (L-22, L-23, L-50).

## Spec Fidelity

### Aligned

Forty-seven of the brief's 51 leads hold as written. Every figure of the brief's § 5 reproduced at the dispatch tip, or differs by a recorded tree difference (`03` § 3.3).

### Diverged

- L-32 withdrawn; L-35 narrowed; L-19 corrected.
- L-08 carries a delta: `docs/retrospective` exists.
- L-47 carries one too: 3 work-log lines.

Each is recorded beside the brief's line in `02`, for the coordinator's correction of the brief (D-WORKFLOW-189).

## Missing Artifacts

At stage B, by design:
- `05-punch-list.md`;
- `second-opinions/review-plan.json`;
- `tools/t38-checks.sh` and its allowlists;
- `stage-c/` to `stage-e/`.

Each is its stage's (§ 6).

## Risk Assessment

| Risk | Severity | Impact | Mitigation |
| --- | --- | --- | --- |
| A Local slice that reads Phase 4.6 as written halts (L-56) | Medium | a lane blocks on a sentence the lint and the plan contradict | the stream's edit of the four sentences; until then every Local brief states the exception |
| A reader runs `scoped-audit.md`'s stash block (L-10) | Medium | another session's stash popped into this worktree; a registry fetch | the stream's replacement with a detached scratch worktree and the repository's own checks |
| A release is published by `release-notes`' sentence (L-11) | Medium | the tool refuses; the reader looks for a path that is retired | the stream's sentence naming `--prepare` and #265, #344, #528 |
| The lint is run the skill's way before Phase 6 (L-52) | Low | a FAIL on every open item, or no `--issue` to pass | the stream's sentence naming `--phase pre-issue` |
| The template's heading fails the lint (L-60) | Low | one failed run, the lint naming the fix | the stream's heading |
| The export drifts further from the tree (L-34, L-76, L-77) | Low | a council run follows a reduced-roster sentence | #911's refresh |

## Coverage Boundary

**Examined:**
- **The reader's pass:** all 52, by one no-context reader per skill and one for the agents, whole (`stage-b/reader-*.md`).
- **The lane's read, whole:** cluster 2's six and the writing pair; in the council family, both `SKILL.md`, the eight agents (`claude` whole and the others as their diffs against it), `IMPORTED-FROM.md`, `COUNCIL-BUNDLE.md` and `member-roster.md`.
- **The lane's read, at the lines the leads and the readers name:** the council family's other references (`stage-b/council-lines.out`).
- **Every claim checked** by a command over the tree, the record or the tracker (`stage-b/checks-*.out`).

**Deliberately not examined:**
- what a provider, a seat or the Facilitator would do (ruling (k): never run);
- the source estates' trees (unreachable: L-50's defences are `CANNOT`);
- rocknix.org's pages (T39's and the site's);
- the Facilitator's and the roster library's code beyond the lines the leads read (T45's);
- the guest behaviour of `developer-relations`' walk (recorded `[unverified]`).

**Dimensions not exercised:**
- runtime behaviour of any skill;
- the harness's description limit (not cited; no limit asserted).

## Finding Verification (Phase 4.5)

No finding is graded Critical or High. The five proposed bugs and the Medium punch items were each re-read at their lines and checked by the artifact that would refute them:

| Finding | Severity | Survived refutation? | What was checked |
| --- | --- | --- | --- |
| L-56 | Medium | yes | the four sentences and the table row re-read; #810's checkbox names `templates.md` only; the lint's `tier_exception` read (A-01) |
| L-10 | Medium | yes | the block re-read at `:347-359`; no record of it run (B-06); `CLAUDE.md`'s *"no unit-test suite"* |
| L-11 | Medium | yes | the tool's source (B-02) and the two dates (B-24) |
| L-52 | Low | yes | the lint's `--phase` choices and its docstring (#470); the skill names neither (B-04) |
| L-13 | Low | yes | `gh repo set-default --view` (B-07); the resolution itself not run (a `gh api` of another repository) |
| L-60 | Low | yes, narrowed | the lint's comparison read: one heading of three fails, two pass by case (B-05) |
| L-02 | Medium | yes | the numbering and its history (B-01); the five briefs' re-numberings |
| L-63 | Medium | yes | the four counts recomputed (B-15) |
| L-57 | Medium | yes | both sentences from the import; `SKILL.md`'s is the one the skill's own *Why* column argues for |
| L-32 | (lead) | **no**: withdrawn | the sentence's subject read at `:188` (B-11) |
| L-35 | (lead) | narrowed | the agents' sentences read (B-12) |
| L-19 | (lead) | narrowed | `session-stash/SKILL.md:32` read (B-13) |

## Renovation face

The seven questions of plan § 4, as the brief's § 4 turns them on skills and agents. Each answer cites its leads (`02` § The leads) and its evidence. The tables are written by `tools/t38-tables.py`, each subcommand seen to exit 1 on a constructed drift (`stage-b/tables/drift.out`, B-19).

### Q1 Modernize

A skill written against a mechanism the tree retired or never had:
- **The Copilot surface:** the `mcp_github_*` names and `.instructions.md` files (L-12, L-14, L-21; the export's L-38).
- **A `main` branch:** L-09, L-66.
- **A spec in `docs/planning/`:** L-08.
- **The retired publish path:** L-11.
- **The legacy worktree layout:** L-04.
- **`research/trio-runs/` and origin pointers:** L-42, L-43.
- **The source estate's stacks, checks and incident numbers:** L-15, L-58 -- the largest by lines. Four of the eleven readers asked *"Which repo is this?"*.
- **A count true once:** L-02, L-03, L-63, L-64, L-67, L-71, L-72.

The retiring record for each is cited in `02`'s row: `worktrees.md`, `device-builds.md:596-597`, `f10eec1306`, `instruction-files.md`, D-WORKFLOW-086.

### Q2 Standards

**There is no fork front-matter standard for a skill:** `instruction-files.md`'s standard is for rules. The shape as it stands:
- every `SKILL.md` carries `name` equal to its directory and a `description`;
- six carry `metadata` with `version` and `origin`;
- the council pair carry VS Code's `tools`, `agents`, `model` and `argument-hint`;
- every agent carries `name`, `description`, `tools`, `model` as a one-item list, and `argument-hint`.

A proposal is #1373's, from `t38-checks.sh`'s `front` step.

The rules a skill must itself obey:
- `issue-tracking.md`'s `--repo` (L-13, L-14);
- `engineering-practices.md`'s shared-stash and *a total is the tool's line* (L-10; L-25 read);
- D-WORKFLOW-091's time (L-05);
- D-WORKFLOW-144's lowercase name (L-45, the export's);
- `ceremonies.md`'s markers and tool (L-06, L-07, L-08, L-20);
- D-WORKFLOW-133's stranger (L-19, stated, not stepped);
- D-QA-044's checkbox shape (L-74).

The open checkboxes about the skills' own text (L-26, L-27) are read in `02`.

### Q3 Bugs

**A skill that lies,** by its kind:
- **A path that does not exist:** L-31, L-33, L-65, L-73, L-75 (L-32 withdrawn, L-35 narrowed).
- **A command that does not run as written, or runs to another's cost:** L-10, L-13, L-52, L-53, L-61, L-66.
- **A count wrong today:** L-02, L-03, L-63.
- **A form copied wrongly into an artifact a tool reads:** L-51, L-60.
- **A gate a skill says a tool enforces, and nothing does:** L-30, with the two pre-commit hooks.
- **A publish step the tree retired:** L-11.
- **Two texts that contradict:** L-56, L-57; the rule erratum L-23.
- **A roster that would send a run to a retired seat:** none; L-44 agrees today.

Every one of the 28 shell blocks has a verdict in `02` § Command blocks. Five sentences are proposed as `bug` at stage D, each with its trace, its `Already written:` line and *"Can this be done on the VM? No -- the tree, the tool or the register shows it"*: L-10, L-11, L-13, L-52 and L-56.

### Q4 Currency

The six sub-questions' tables, written by `tools/t38-tables.py q4` (`stage-b/tables/q4.md`):

<!-- include: stage-b/tables/q4.md lang markdown -->
```markdown
#### (a) Every decision ID the 52 cite, at the coordinator's tip `3a9b0aec81`

| ID | Decided rows | Open rows | Files citing it |
| --- | ---: | ---: | --- |
| D-WORKFLOW-003 | 1 | 0 | `skills/council/IMPORTED-FROM.md` |
| D-WORKFLOW-009 | 1 | 0 | `skills/council/IMPORTED-FROM.md` |
| D-WORKFLOW-068 | 1 | 0 | `skills/developer-relations/SKILL.md`, `skills/release-notes/SKILL.md` |
| D-WORKFLOW-074 | 1 | 0 | `skills/developer-relations/SKILL.md`, `skills/release-notes/SKILL.md` |
| D-WORKFLOW-078 | 1 | 0 | `skills/release-notes/SKILL.md` |
| D-WORKFLOW-079 | 1 | 0 | `skills/release-notes/SKILL.md` |
| D-WORKFLOW-088 | 1 | 0 | `skills/council/IMPORTED-FROM.md` |
| D-WORKFLOW-089 | 1 | 0 | `skills/council/IMPORTED-FROM.md` |
| D-WORKFLOW-090 | 1 | 0 | `skills/council/IMPORTED-FROM.md` |
| D-WORKFLOW-102 | 1 | 0 | `skills/code-auditor/references/review-levels.md` |
| D-WORKFLOW-109 | 1 | 0 | `agents/council-member-deepseek.agent.md`, `agents/council-member-grok.agent.md`, `skills/council/IMPORTED-FROM.md`, `skills/council/SKILL.md` |
| D-WORKFLOW-133 | 1 | 0 | `skills/session-resume/SKILL.md`, `skills/session-stash/SKILL.md` |
| D-WORKFLOW-135 | 1 | 0 | `agents/council-member-claude.agent.md`, `agents/council-member-deepseek.agent.md`, `agents/council-member-gemini.agent.md`, `agents/council-member-gpt.agent.md`, `agents/council-member-grok.agent.md`, `agents/council-member-kimi.agent.md`, `agents/council-member-mistral.agent.md`, `agents/council-member-muse.agent.md`, `skills/council/IMPORTED-FROM.md`, `skills/council/SKILL.md`, `skills/council/references/member-roster.md`, `skills/council/references/pipeline.md` |
| D-WORKFLOW-137 | 1 | 0 | `skills/code-auditor/SKILL.md`, `skills/code-auditor/references/phases.md`, `skills/code-auditor/references/review-levels.md` |
| D-WORKFLOW-149 | 1 | 0 | `skills/code-auditor/SKILL.md` |
| D-WORKFLOW-184 | 1 | 0 | `skills/code-auditor/references/templates.md` |

16 IDs, each in one decided row and no open row.

#### (b) Every `tools/...` the 52 name, at HEAD

| Tool | At HEAD | Files naming it |
| --- | --- | --- |
| `tools/call` | absent | 1 |
| `tools/cloud-round-trip` | present | 1 |
| `tools/cloud-test-backend` | present | 1 |
| `tools/council/` | present | 1 |
| `tools/council/node_modules` | absent | 1 |
| `tools/council/run` | present | 3 |
| `tools/fork-publish-release` | present | 1 |
| `tools/lint-audit-artifacts` | present | 1 |
| `tools/list` | absent | 1 |
| `tools/pkgcheck` | present | 1 |
| `tools/png-blackout` | present | 1 |
| `tools/pr-stack-check` | present | 1 |
| `tools/prose-check` | present | 2 |
| `tools/vm-visual-qa` | present | 1 |
| `tools/vm-walks/docs/` | present | 1 |
| `tools/watch-build` | present | 1 |
| `tools/watch-build-submit` | present | 1 |
| `tools/watch-job` | present | 1 |

18 named, 15 present, 3 absent: `tools/call`, `tools/council/node_modules`, `tools/list` (MCP method names and an untracked install directory).

#### (c) Every count the read found a skill stating, recomputed

| Where | Stated | Recomputed | Holds |
| --- | --- | --- | --- |
| `code-auditor/SKILL.md` § Evidence floor: *"Three hard rules"* | 3 | 5 (numbered 1, 2, 3, 4, 3) | no |
| `code-auditor/SKILL.md`: *"Twelve recorded failure modes"* | 12 | 76 (the last numbered heading; 48 numbered headings) | no |
| `mini-retro/SKILL.md`: *"the full 6-phase methodology"* | 6 | 11 (`code-auditor`'s lifecycle rows: 0, 1, 2, 2.5, 3, 4, 4.5, 4.6, 5, 6, 7) | no |
| `mini-retro/SKILL.md` Step 2.5's procedure, its checks | 9 | 10 (`### Check` headings in `scoped-audit.md`) | no |
| `mini-retro/SKILL.md` § format, *Scoped audit findings* lines | 6 | 10 | no |
| `mini-retro/references/template.md`, `Check N` lines | 9 | 10 | no |
| `begin-delivery/SKILL.md`: *"the five phase-tier audit spot-check verdicts"* | 5 | 10 | no |
| `futro/SKILL.md` question 4: *"Apply four techniques"* | 4 | 5 | no |
| `release-notes/SKILL.md`: *"three or four short paragraphs"* | 3 or 4 | 3 | yes |
| `council/COUNCIL-BUNDLE.md:4`: *"Files: 94, byte-identical to that commit"* | 94 | 94 entries; 52 match the tree, 39 differ, 3 absent | yes |

#### (e) The roster: the rule, `member-roster.md` and the agents

| Seat | Agent's `model:` | `member-roster.md` | `adversarial-council.md:77-78` | Agree |
| --- | --- | --- | --- | --- |
| claude | `anthropic/claude-fable-5.1` `xhigh` | `anthropic/claude-fable-5.1` `xhigh` | `anthropic/claude-fable-5.1` `xhigh` | yes |
| gemini | `google/gemini-3.8-flash` `high` | `google/gemini-3.8-flash` `high` | -- (not a rule row) | yes |
| gpt | `openai/gpt-6-astra` `max` | `openai/gpt-6-astra` `max` | `openai/gpt-6-astra` `max` | yes |
| kimi | `moonshotai/kimi-k3` `max` | `moonshotai/kimi-k3` `max` | -- (not a rule row) | yes |
| muse | `meta/muse-spark-1.3` `max` | `meta/muse-spark-1.3` `max` | -- (not a rule row) | yes |

#### (f) The pins: each agent's sha256 against `verifier-pins.json` at HEAD

| Agent file | Pin | Bytes | Match |
| --- | --- | --- | --- |
| `.claude/agents/council-member-claude.agent.md` | `dce34ed4cb3b864d` | `dce34ed4cb3b864d` | MATCH |
| `.claude/agents/council-member-deepseek.agent.md` | `5b33fcc8ade298ec` | `5b33fcc8ade298ec` | MATCH |
| `.claude/agents/council-member-gemini.agent.md` | `7b19b9269406691a` | `7b19b9269406691a` | MATCH |
| `.claude/agents/council-member-gpt.agent.md` | `5790193074f0d8a4` | `5790193074f0d8a4` | MATCH |
| `.claude/agents/council-member-grok.agent.md` | `59faf8d4dbba9a72` | `59faf8d4dbba9a72` | MATCH |
| `.claude/agents/council-member-kimi.agent.md` | `5cc1ee6fa277e51e` | `5cc1ee6fa277e51e` | MATCH |
| `.claude/agents/council-member-mistral.agent.md` | `963dfd3f63170b1f` | `963dfd3f63170b1f` | MATCH |
| `.claude/agents/council-member-muse.agent.md` | `93f10a7b61891033` | `93f10a7b61891033` | MATCH |
```

- **(d), every path named, resolved in its class:** the `refs` step of `tools/t38-checks.sh` at stage C, with the three allowlists. At stage B the read resolved the paths the leads name (`02` § The names and the references).
- **The tool count, by method:** the generator counts distinct `tools/...` tokens -- `18` named, `15` present, the three known non-tools absent. R3 C20 counted `35` named by another extractor; the absent three are the same.

### Q5 Efficiency -- the lens

**What the slice costs a session, and what it earns.** Every session lists each skill's and each agent's description; a skill's body loads when it runs. The table (`tools/t38-tables.py q5`, `stage-b/tables/q5.md`) states its unit: the description's characters as the YAML scalar parses, its surrounding quotes removed, so the brief's quoted counts (90, 78, 317 for the inactive three) read here as 88, 76, 315.

<!-- include: stage-b/tables/q5.md lang markdown -->
```markdown
| Skill or agent | Files | Lines | Description (characters) | Records under | Entries | Commits there | Plan lines | Brief lines |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `code-auditor` | 5 | 1793 | 878 | `docs/audits/` | 24 | 176 | 1 | 60 |
| `mini-retro` | 3 | 1477 | 985 | `docs/retros/` | 7 | 9 | 1 | 25 |
| `futro` | 4 | 1051 | 906 | `docs/futros/` | 17 | 92 | 0 | 8 |
| `session-resume` | 1 | 121 | 299 | -- | 0 | 0 | 1 | 2 |
| `session-stash` | 1 | 163 | 430 | `.github/sessions/archived/` | 334 | 242 | 0 | 5 |
| `begin-delivery` | 1 | 619 | 909 | -- | 0 | 0 | 0 | 6 |
| `developer-relations` | 1 | 195 | 270 | -- | 0 | 0 | 0 | 4 |
| `release-notes` | 1 | 130 | 277 | `docs/releases/pr/` | 11 | 3 | 0 | 7 |
| `council` | 15 | 2750 | 917 | `research/council-runs/` | 5 | 34 | 2 | 41 |
| `council-research` | 12 | 4150 | 752 | `research/council-research/` | 0 | 0 | 0 | 14 |
| `council-member-claude` | 1 | 56 | 255 | -- | -- | -- | -- | -- |
| `council-member-deepseek` | 1 | 19 | 88 | -- | -- | -- | -- | -- |
| `council-member-gemini` | 1 | 50 | 255 | -- | -- | -- | -- | -- |
| `council-member-gpt` | 1 | 49 | 249 | -- | -- | -- | -- | -- |
| `council-member-grok` | 1 | 19 | 76 | -- | -- | -- | -- | -- |
| `council-member-kimi` | 1 | 46 | 261 | -- | -- | -- | -- | -- |
| `council-member-mistral` | 1 | 48 | 315 | -- | -- | -- | -- | -- |
| `council-member-muse` | 1 | 47 | 314 | -- | -- | -- | -- | -- |
| **Total** | 52 | 12783 | | | | | | |
```

- **The records** are the directories each skill writes to:
  - `docs/audits/` for `code-auditor` (24 entries, 176 commits);
  - `docs/retros/` for `mini-retro` (7, 9);
  - `docs/futros/` for `futro` (17, 92);
  - `.github/sessions/archived/` for `session-stash` (334, 242);
  - `research/council-runs/` for `council` (5, 34);
  - `research/council-research/` for `council-research` (0, 0);
  - `docs/releases/pr/` for `release-notes` (11, 3).
- **The procedure's use** is the plan's and the 80 briefs' lines naming the skill.
- **T4's table of every path a rule or register line cites** (`6ec78bbf8c:.../04-analysis.md:705-892`) names the 52 on `15` rows, every one a tracked file: the rules cite the council family and `code-auditor`, and none of the rest.

**The questions the lens puts:**
1. **`council-research`: 4,150 lines and 752 characters of description, with no run kept** -- § 4's first question for the maintainer (below).
2. **`mini-retro`: 1,477 lines, 716 of them the scoped audit, against 7 retros**, while `ceremonies.md` also accepts a work-log heading. Proposed as a Renovation item: the format lists the ten checks (L-63), and the source estate's spot checks go (L-15). The size follows from those, not from a cut.
3. **`council`: 2,750 lines, 94 of them a digest list and 127 an import record.** The export's to carry; #911's refresh decides.
4. **The three inactive agents' descriptions** (88, 76 and 315 characters): kept by ruling (e), their cost stated.
5. **The version histories inside procedures:** `begin-delivery`'s 69-line change log (L-16), `code-auditor`'s front-matter `adapted:` note, `council-research`'s `origin` (L-46). A Renovation item for the stream, and for #911 respectively.
6. **The cheapest skill by record, `session-stash`** (163 lines, 334 archives), without the tool its most-skipped step needs (L-18).
7. **A description changed is a load changed:** L-05's `~30 min` at `code-auditor/SKILL.md:3`, L-70's `release-notes` description and L-22's three descriptions. Each stream edit records the length before and after.

**The two time-to-play numbers are untouched:** interface to a game's first frame, and a game's exit to the next game's first frame. The 52 load in an agent's session, never on an image, so this slice does nothing to either.

**§ 4's first question for the maintainer, in the shape § 4 gives** (the coordinator posts it on #807 with its two options; `02`'s row cites the comment's id):

> **Does `council-research` earn its place, or is it retired at the export's next refresh?** Today every session's skill listing carries its description (752 characters). Running it as written would stop at Phase 2, which names an agent the tree does not have (L-31). Its gates name lints the tree does not have, and two hooks it says enforce them do not exist (L-30). It is 4,150 lines in 12 files, the largest skill of the ten, with no run kept under `research/council-research/` and 3 work-log lines. Keeping it is the export as copied; retiring it is a choice at the refresh, under #911 (PL-17), not a T38 edit.

### Q6 Dead ends

Everything the 52 point at that the tree lacks:
- `begin-exploration`, `work-start-notice` and `retro-sweep` (L-22);
- `researcher.agent.md` (L-31);
- the scaffold tooling paths and the two hooks (L-30);
- `research/council-research/` with no run (L-47);
- `shadow-experiments.md` in the sums (L-34);
- the shadow profiles that still reach the inactive seats (L-36);
- the register sections futro and begin-delivery cite (L-75);
- `agent-terminal-safety` (L-73);
- `reference/template.md` and `cornerstone-conformance.md` (L-65);
- Phase Z.6, PZ and *Outcome A/B* (L-55);
- the stash archive's tool (L-18).

The reachability table (`tools/t38-tables.py q6`, `stage-b/tables/q6.md`) gives each skill's trigger, who names it and what the record keeps. Each row with no record kept carries its `Already written:` line:

<!-- include: stage-b/tables/q6.md lang markdown -->
```markdown
| Skill or agent | Trigger in the description | Other skills naming it | Plan lines | Brief lines | Work-log lines | Records | Reachable by record | Already written (rows with no record) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `code-auditor` | Use when | 38 | 1 | 60 | 8 | 24 | yes |  |
| `mini-retro` | Use when | 23 | 1 | 25 | 2 | 7 | yes |  |
| `futro` | Use when | 27 | 0 | 8 | 2 | 17 | yes |  |
| `session-resume` | Use when | 1 | 1 | 2 | 1 | -- | no record kept | Already written: sessions resumed from the pointers and the canonical stash; the skill's own pointer rule (L-68) is what a lane would have read. |
| `session-stash` | Use when | 0 | 0 | 5 | 0 | 334 | yes |  |
| `begin-delivery` | Use when | 22 | 0 | 6 | 6 | -- | no record kept | Already written: no kickoff comment or plan names it; every session's listing carried its description, and its `begin-exploration` hedges reach readers through `mini-retro` and `futro` (L-22). |
| `developer-relations` | Use for | 1 | 0 | 4 | 3 | -- | no record kept | Already written: rocknix.org pages drafted under it (#323, D-WORKFLOW-068); its records live in the site's repository, not here. |
| `release-notes` | Use for | 1 | 0 | 7 | 5 | 11 | yes |  |
| `council` | Use when | 85 | 2 | 41 | 7 | 5 | yes |  |
| `council-research` | Use when | 12 | 0 | 14 | 2 | 0 | no record kept | Already written: nothing a run left -- `research/council-research/` holds 0 entries; three work-log lines name the skill; every session's listing carried its description. |
| `council-member-claude` | Use when | -- | -- | -- | -- | -- | pinned; profiles: definitive, grok-shadow, deepseek-shadow |  |
| `council-member-deepseek` | inactive: says do not invoke | -- | -- | -- | -- | -- | pinned; profiles: deepseek-shadow | Already written: kept and pinned, ruling (e); its description is in every listing |
| `council-member-gemini` | Use when | -- | -- | -- | -- | -- | pinned; profiles: definitive, grok-shadow, deepseek-shadow |  |
| `council-member-gpt` | Use when | -- | -- | -- | -- | -- | pinned; profiles: definitive, grok-shadow, deepseek-shadow |  |
| `council-member-grok` | inactive: says do not invoke | -- | -- | -- | -- | -- | pinned; profiles: grok-shadow | Already written: kept and pinned, ruling (e); its description is in every listing |
| `council-member-kimi` | Use when | -- | -- | -- | -- | -- | pinned; profiles: definitive, grok-shadow, deepseek-shadow |  |
| `council-member-mistral` | inactive: says do not invoke | -- | -- | -- | -- | -- | pinned; profiles: the env override (`:87-90`) | Already written: kept and pinned, ruling (e); its description is in every listing |
| `council-member-muse` | Use when | -- | -- | -- | -- | -- | pinned; profiles: definitive |  |
```

**§ 4's second question, in the shape § 4 gives** (raised by the lane on #685 at the pause):

> **`begin-exploration`: write the skill, or sweep the references?** Today 19 lines of the 52 tell a session to use a skill that no tree has, hedged *"if present"*. Three of them are in descriptions every session lists (`mini-retro`, `futro`, `begin-delivery`). `adversarial-council.md:36-38` says it ships. Writing it is new work with its own issue; sweeping is an edit in the fork-adapted skills under a stream brief. The rule's line is the coordinator's erratum either way.

### Q7 Clarity and structure

**Can a reader new to it tell what each skill decides and when to open it, in one pass?** The eleven readers answered the first half for every skill (`stage-b/reader-*.md`, item 1 of each). Their stumbles are the evidence for the second, at `01` § The reader's pass. What the read made of them:
- **The evidence floor's count (L-02):** a sentence quoted, wrongly, around five times.
- **The procedures carrying their own histories:** L-16, L-46.
- **The duplicated sections:** `futro`, `mini-retro` and `begin-delivery` share *pixelelated continuation* word for word. The four *Execution discipline* sections differ only in their last sentence (`code-auditor`'s describes a moving target; the other three link `ceremonies.md`).
- **The drifted copy of the criterion entry:** L-62.
- **A comment against its own line:** L-40, the export's.
- **Each skill's internal contradictions:** L-81 to L-85.
- **Sentences a stranger read twice:** the readers' items, each cited at its lead.

The duplicates and their diffs (`tools/t38-tables.py q7`, `stage-b/tables/q7.md`):

<!-- include: stage-b/tables/q7.md lang markdown -->
```markdown
#### `## pixelelated continuation`

- `futro` and `mini-retro`: identical, 10 lines
- `futro` and `begin-delivery`: identical, 10 lines

#### `## Execution discipline — SERIAL (hard gate)`

- `code-auditor` and `futro`: differ on 4 line(s)
  - `-scope, do not mutate that scope from elsewhere - an audit of a moving target`
  - `-proves nothing about either state.`
  - `+scope, other agents pause mutations on that scope until it completes`
  - `+([ceremony execution discipline](../../rules/ceremonies.md#execution-discipline)).`
- `code-auditor` and `mini-retro`: differ on 4 line(s)
  - `-scope, do not mutate that scope from elsewhere - an audit of a moving target`
  - `-proves nothing about either state.`
  - `+scope, other agents pause mutations on that scope until it completes`
  - `+([ceremony execution discipline](../../rules/ceremonies.md#execution-discipline)).`
- `code-auditor` and `begin-delivery`: differ on 4 line(s)
  - `-scope, do not mutate that scope from elsewhere - an audit of a moving target`
  - `-proves nothing about either state.`
  - `+scope, other agents pause mutations on that scope until it completes`
  - `+([ceremony execution discipline](../../rules/ceremonies.md#execution-discipline)).`

#### The criterion entry: `phases.md` § Phase 2 against `templates.md`'s *"Reproduced here"*

- 9 line(s) differ:
  - `-- [Command evidence: executed check + exit status + counts, when a mechanical check enforces this AC]`
  - `+`
  - `+**Notes:**`
  - `+`
  - `+- [What was found, any concerns, quality observations]`
  - `-**Notes:**`
  - `-`
  - `-- [What was found, any concerns, quality observations]`
  - `-`
```

**The clusters**: by path, the council family names itself; by name, `begin-delivery` <-> `futro` <-> `mini-retro` <-> `code-auditor`, joined to the council family by a handful of lines (R1 § 6, `01` § Read order). This is the fact behind the order's *"kept whole because the skills cross-reference each other"*. T38 is not split (ruling (j)); the record is for the next order.

## Instruction File Recommendations

The epic-tier mode (`code-auditor/SKILL.md:621-665`). Recommendations only: the rules are the coordinator's (ruling (l)).

### Coverage Gaps (would-have-prevented)

| Finding | Would have been caught by | Uncovered? |
| --- | --- | --- |
| L-02, L-63, L-67 (a count left behind) | `engineering-practices.md` § A name is not a behaviour (*a count ... is a claim about one tree*), had the editing session recomputed the count | -- |
| L-11, L-66, L-09 (a fact retired under the skill) | `decision-register.md` § A reversal, a rename or a re-pin sweeps its old words (`tools/archaeology --reversal`), had the sweep reached `.claude/skills` | -- |
| L-56 (an exception landed in one of five places) | the same § of `decision-register.md` | -- |
| L-15, L-58 (another estate's words) | (none) | **YES** |

### Codification Gaps (needs-new-rule)

| Pattern | Instances | Recommendation |
| --- | --- | --- |
| P-01: an imported skill keeps its source estate's names, stacks and incident numbers | L-15, L-58, L-12, L-21, L-55 | **Extend** `instruction-files.md` with a short section on imported skills: what an adaptation must sweep (paths, tools, issue numbers, examples) and that `tools/skills-check` (#1373) carries the check |
| P-02: a rule added to a skill without its count or its cross-references | L-02, L-56, L-59, L-63, L-67 | **Extend** `working-principles.md` § Enforcement depth's ladder note: a skill edit that adds an item recounts its list and greps its citations, and #1373's `contract` and `refs` steps hold it |

### Recommended Action Sequence

1. The stream brief takes the five proposed bugs and the Medium punch items first (L-56, L-10, L-11, L-52, L-13, L-60, L-02, L-63, L-57, L-59, L-53, L-66, L-69, L-70, L-81, L-06, L-08).
2. Then the Low items per skill, one stream each, so a description change is one commit with its length.
3. The coordinator's rule errata (L-22, L-23, L-50 and the lost-space shape) in its own sweep; P-01 and P-02 there.
4. #911 carries the export's list; #1373 takes `t38-checks.sh`.

## Second opinion (Phase 4.6)

**Not applicable at Local depth** (plan § 6c: *"a doctrine read | Local: the executor alone; the lint and the counts are the check"*; D-WORKFLOW-184).
- No reviewer, no Facilitator call, no `tools/council/run`, no `npm install`, no keyed call.
- `second-opinions/review-plan.json` records `local` with `tier_exception` `D-WORKFLOW-184` (stage C), and the lint's acceptance of that shape was proved before anything else (A-01).
- Phase 4.5 above is the only verification pass, and § 5's rule 4 was asked of every PASS (each `PROOF:` line in `00` names what would have been a FAIL).

## Quality Self-Check

| Item | Status |
| --- | --- |
| Acceptance-criteria scorecard present, IDs match #685's 22 | present |
| Cornerstone conformance (this repository: the rules and the registers) | present |
| Coverage boundary present (02's runs and this file) | present |
| Finding verification recorded for every Critical/High | present: none graded so; the five proposed bugs and the Medium items re-read |
| Second opinion recorded | present: not applicable at Local depth, with its reason |
| Instruction file recommendations (epic tier) | present |
| Tier B visual-QA consolidation | absent: no design-review process here, and no UI surface in the 52 |
| Verdicts use the defined vocabulary only | yes |
| Traceability / Evidence / Reproducible / Actionable / Complete | self-checked: every lead at its lines, every check a script with its output under `stage-b/` |
