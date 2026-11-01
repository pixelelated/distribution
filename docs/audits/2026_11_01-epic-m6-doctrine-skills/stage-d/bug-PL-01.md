Found by the M6 renovation's T38 slice, the skills, agents and settings (#685; audit [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`](https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills), L-56, punch item PL-01). D-WORKFLOW-187: a defect the renovation finds is a bug like any other; ruling (c) of the slice's brief: a sentence a reader acts on wrongly is a `bug`.

The lines are at the dispatch tip `87c2ab0fed`, whose `.claude/` the slice branch has not changed.

## Code trace

- **How it was found:** L-56 in `02-forward-audit.md`, the auditor's read of `code-auditor` (`stage-b/notes-code-auditor.md`, `stage-b/checks-code-auditor.out`). Phase 4.6 is described in several places, and they disagree with the template and the lint.
- **The defect at its source (the sentence):** a lane that runs the procedure as written stops at Phase 4.6 on a Local epic-tier slice. These sentences require a second opinion at Epic tier or fail closed without one, and none names D-WORKFLOW-184's exception for a slice whose plan row says Local:
  - `code-auditor/SKILL.md:247`: the phase table, *"Independent review (selected depth; required for Epic/Milestone)"*;
  - `SKILL.md:508`: *"mandatory at Epic and Milestone tiers, fails closed without the seat"*;
  - `references/phases.md:439`: *"(mandatory at Epic and Milestone tiers)"*;
  - `references/phases.md:486-491`: *"**Fails closed:** ... Do not proceed to Phase 5 ... Local-only Issue audits explicitly record Phase 4.6 as not applicable; they do not claim independent review or satisfy an Epic/Milestone ... gate"*;
  - `references/review-levels.md:9`: Local is *"A bounded Issue/PR check during implementation"*;
  - `references/templates.md:94` and `:164`: the analysis template's Second opinion row and its checklist line.
- **The artifact it misdescribes:** two things contradict these sentences.
  - `references/templates.md:144-146` says *"Use `depth: local`, `reviewers: []` only for an explicitly local Issue audit, or for an Epic-tier slice whose plan row says Local (D-WORKFLOW-184) with `tier_exception` and `reason` in the plan file"*. That half was added under #810, whose checkbox named `templates.md` alone.
  - `tools/lint-audit-artifacts` passes such a plan: proof A-01, `rc=0` `PASS`, and `local-only cannot satisfy Epic/Milestone` once `tier_exception` is removed.
- **The fix's shape:** each sentence above names the exception as `templates.md:144-146` does. A slice whose plan row says Local records Phase 4.6 as *not applicable at Local depth*, with its `review-plan.json`, and proceeds. The Epic and Milestone requirement stands for every other plan.
- **Sibling sites, hunted** (`stage-d/siblings.out`): no other skill of the 52 names Phase 4.6. In `code-auditor`, `fails closed`, `mandatory at Epic` and `required for Epic` match only the lines above.
- **What reading cannot prove:** whether a session outside these records stopped at 4.6. Transcripts are not in the tree, and every Local slice's brief carried the exception itself.
- **Already written:** nothing inherited. The eight earlier Local epic-tier folders on this repository's local refs each record Phase 4.6 as not applicable, or the depth as Local by the slice's plan, in `04` § Second opinion, and none holds it pending (`stage-d/checks-bugs.out`). The fix changes the sentence a later lane reads; no folder needs rewriting.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it: the skill's text against `templates.md:144-146`, `tools/lint-audit-artifacts` and D-WORKFLOW-184.

## Acceptance criteria

- [ ] At the fix's commit, every line named under *The defect at its source* either names the D-WORKFLOW-184 exception or points to `references/templates.md:144-146`. The fix's commit records `git grep -n -i -E 'D-WORKFLOW-184' -- .claude/skills/code-auditor` before and after, and the after shows a line in each of `SKILL.md`, `references/phases.md` and `references/review-levels.md`.
- [ ] `tools/lint-audit-artifacts` on `docs/audits/2026_11_01-epic-m6-doctrine-skills/` still passes the Local plan, and still refuses it with `tier_exception` removed (proof A-01's two lines, re-run at stage F).
- [ ] The fix's commit cites this issue and #685, and lands only in `.claude/skills/code-auditor/`.
