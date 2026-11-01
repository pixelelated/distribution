Found by the M6 renovation's T38 slice, the skills, agents and settings (#685; audit [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`](https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills), L-52, punch item PL-04). D-WORKFLOW-187: a defect the renovation finds is a bug like any other; ruling (c) of the slice's brief: a sentence a reader acts on wrongly is a `bug`.

The lines are at the dispatch tip `87c2ab0fed`, whose `.claude/` the slice branch has not changed.

**fixed-at:** `7066c9f299` (stage E of T38, #685; the record `docs/audits/2026_11_01-epic-m6-doctrine-skills/stage-e/S1-PL-10.txt`). Each checkbox below is ticked from its check line, quoted under it.

## Code trace

- **How it was found:** L-52 in `02-forward-audit.md`, the auditor's read of `code-auditor`. `pre-issue` and `--phase` appear nowhere in the skill (B-04: `grep rc=1`).
- **The defect at its source (the sentence):** `code-auditor/SKILL.md:252-256`: *"**Before Phase 6, RUN `tools/lint-audit-artifacts <folder> --issue <n>`.** It checks the required files, the mandatory `04-analysis.md` sections, that every punch item has a Phase 7 outcome, ... and that the audit issue carries one checkbox per punch item."*
- **The artifact it misdescribes:** the lint (`tools/lint-audit-artifacts:4-5`, `:177-180`).
  - Its default phase, `resolution`, requires every item at an outcome, so it cannot pass before Phase 7.
  - `--issue N` reads an audit issue that Phase 6 has not yet created.
  - The run that belongs before Phase 6 is `--phase pre-issue`, which *"permits honestly open findings before Phase 6"* and *"never certifies a completed audit"* (#470). This slice ran it at stage C: C-07, `PASS pre-issue artifacts (does not certify resolution)`.
- **The fix's shape:** before Phase 6, run `--phase pre-issue`. After Phase 7, run the default phase with `--issue <n>` against the audit issue. The checks the paragraph lists are split between the two runs.
- **Sibling sites, hunted** (`stage-d/siblings.out`): the lint is also named at `SKILL.md:9` (the front matter's version note) and `references/phases.md:575`, which says to *"run it and fix every finding before Phase 6"*. That is the same defect and is fixed with it; L-59, PL-10, is the same paragraph's *"none today"*.
- **What reading cannot prove:** how many sessions ran the default phase before Phase 6, failed, and moved on outside the records read.
- **Already written:** nothing inherited.
  - The lint opens no file for writing (`stage-d/checks-bugs.out`: `grep rc=1 (1 = none)`), so a run at the wrong phase left only its output.
  - The completed audits carry their own completion markers (`6` under `docs/audits/*/audit-completion.json` in this tree), the record of their close; the fix does not touch them.
  - `2` folders here record a `--phase pre-issue` run.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it: the paragraph against the lint's own usage and options.

## Acceptance criteria

- [x] At the fix's commit, `LC_ALL=C grep -c -F -- '--phase pre-issue' .claude/skills/code-auditor/SKILL.md` prints a count above `0`, and no line of the skill runs `--issue <n>` before Phase 6.
  - at the parent `09384b54fe`: `0`; at the fix `144b5bc6de`: `code-auditor/SKILL.md names pre-issue ; 1`
- [x] `references/phases.md:575`'s sentence says the same as `SKILL.md`, recorded before and after in the fix's commit.
  - PL-10's `7066c9f299`: at the parent `91f3095280`: `none today: 1 ; phases.md runs pre-issue: 0 ; anti-patterns.md names the tool: 0`; at the fix: `none today: 0 ; phases.md runs pre-issue: 1 ; anti-patterns.md names the tool: 1`
- [x] The fix's commit cites this issue and #685, and lands only in `.claude/skills/code-auditor/`.
  - `144b5bc6de` cites #685 and #1392, and its `git show --stat` names only `.claude/skills/code-auditor/SKILL.md`

