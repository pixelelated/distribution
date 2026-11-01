# Stream: the lint accepts Local depth at epic tier (#810)

A narrow remediation stream, written by the coordinator on 2026-10-24
(D-WORKFLOW-189) from the stranger's proof of T4's brief, in the
D-WORKFLOW-056 shape. **Lane:** T1's (`m6-t1-os-launch`, #648, accepted and
idle), as for #806: the tool has no lane of its own until T10 (#657), and
every Local slice of the renovation (T4 first) is blocked at plan § 6b's
criterion 2 until this lands. **No runtime, no build, no guest**; the host
hold is M7's.

- **Files owned:** `tools/lint-audit-artifacts` (its `check_review_plan`,
  lines 49 to 50 today) and
  `.claude/skills/code-auditor/references/templates.md` (the sentence at
  line 129 and the example `review-plan.json` block above it). Nothing else.
- **The branch:** `fix/m6-810-lint-local-epic` cut from `next` at
  `8ebaf8daad` in its own worktree `../m6-810-lint-local-epic`
  (`worktrees.md`); never on the slice branch.
- **The test first (the failing control and the passing case), run before
  the change and after**, in the fix worktree, with two synthetic folders
  under `.qa-scratch/810/` built by a short script committed with the fix
  (`tools/lint-audit-artifacts` reads a folder; the synthetic folder needs
  only what `check_review_plan` reads -- look at the function and give it
  the minimum, and if the pre-issue phase needs the five artifact files,
  write empty-but-well-formed ones and say so):
  1. `.qa-scratch/810/2026_10_24-epic-m6-synthetic-a/second-opinions/review-plan.json`
     with `"depth": "local"`, `"reviewers": []`, no `tier_exception`: the
     lint fails with `local-only cannot satisfy Epic/Milestone` before
     **and after** (the control).
  2. the same with `"tier_exception": "D-WORKFLOW-184"` and
     `"reason": "plan § 6c: a doctrine read is Local"`: fails before,
     **passes after** (the case).
  Paste both runs' lines in the hand-back.
- **The change:** in `check_review_plan`, replace the unconditional
  `require('-issue-' in d.name, ...)` with: Local is accepted in an
  `-issue-` folder as today, or in any folder when
  `plan.get('tier_exception') == 'D-WORKFLOW-184'` and
  `isinstance(plan.get('reason'), str) and plan['reason'].strip()`; else
  the same failure message as today. Record the exception in the lint's
  `ok` line (`review-plan: local at epic tier under D-WORKFLOW-184`), so a
  reader of the output sees the exception was taken. In `templates.md`,
  the sentence at line 129 becomes: Local is for an explicitly local Issue
  audit, or for an Epic-tier slice whose plan row says Local
  (D-WORKFLOW-184) with `tier_exception` and `reason` in the plan file;
  the example block gains the two optional keys with a one-line comment.
- **Regression:** `for d in docs/audits/*/; do tools/lint-audit-artifacts "$d" >/dev/null 2>&1; echo "$? $d"; done`
  before and after, identical (paste both lists or their diff, which is
  empty).
- **Already written:** no audit folder has recorded `depth: local` at epic
  tier; nothing to migrate.
- **Commit:** `lint-audit-artifacts: accept Local depth at epic tier under D-WORKFLOW-184 (#810)`,
  committed as `git -c user.name=blitterbot`, body with `Refs #810` (the
  criteria close on the regression list and T4's first use), ending
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; `git status
  --short` empty; `git push -u origin fix/m6-810-lint-local-epic`.
- **Hand-back:** one comment on #810: the branch, the hash, `git show
  --stat`, the two synthetic runs' lines before and after, the regression
  list, and what the stream could not prove (T4's real plan file, written
  at T4's stage C). Update the lane pointer; say the lane's state.
- **The coordinator** reads the diff, runs the two synthetic cases from an
  export of the commit, comments *reviewed*, and takes the branch into the
  coordinator's branch (the lint is the program's tool and T4 needs it
  before dispatch): `git merge --no-ff` there, with the merge named on #810.
