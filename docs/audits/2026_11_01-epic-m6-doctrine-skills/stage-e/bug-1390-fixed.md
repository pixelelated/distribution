Found by the M6 renovation's T38 slice, the skills, agents and settings (#685; audit [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`](https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills), L-10, punch item PL-02). D-WORKFLOW-187: a defect the renovation finds is a bug like any other; ruling (c) of the slice's brief: a sentence a reader acts on wrongly is a `bug`.

The lines are at the dispatch tip `87c2ab0fed`, whose `.claude/` the slice branch has not changed.

**fixed-at:** `f95a86a878` (stage E of T38, #685; the record `docs/audits/2026_11_01-epic-m6-doctrine-skills/stage-e/S2-PL-02.txt`). Each checkbox below is ticked from its check line, quoted under it.

## Code trace

- **How it was found:** L-10 in `02-forward-audit.md`, the auditor's read of `mini-retro`. The block is § Command blocks' `mini-retro/references/scoped-audit.md:347`, recorded *not run: it writes to the shared stash and the working tree and fetches from the registry*.
- **The defect at its source (the sentence):** `mini-retro/references/scoped-audit.md:347-359`, *"The mechanical verification is:"*, then:
  1. `git stash`;
  2. `git checkout <base_sha> -- <files_touched_by_phase>`;
  3. `npx vitest run <failing_test_files>`;
  4. `git checkout HEAD -- <files_touched>`;
  5. `git stash pop`.

  With it are the runner examples at `:292-321` (`npx vitest run`, `cd services/example-api && npx vitest run`).
- **The artifact it misdescribes:** this repository and this machine.
  - The stash is shared with the main checkout and every other worktree, and other sessions push and pop it. A bare `git stash pop` can apply another session's changes, which is why the renovation's briefs list a bare `git stash` among the commands that never run (`docs/reviews/briefs/doctrine-skills.md:1756`).
  - The repository has no vitest suite and no `services/` (`0` under `services`, § Command blocks).
  - `npx` fetches from a registry.
  - `git checkout <base_sha> -- <files>` overwrites the working tree's copies.
- **The fix's shape:** check the pre-existing failure in a detached scratch worktree at `<base_sha>`. Run the repository's own checks there (the suite the phase's tests belong to, `tools/vm-qa` where it applies), then remove that worktree with `tools/fork-worktree remove`. No stash, no checkout over the working tree, no `npx`. The runner examples at `:292-321` name this repository's checks or are dropped.
- **Sibling sites, hunted** (`stage-d/siblings.out`): `git stash` appears nowhere else in the 52. `npx` appears in the fork-adapted skills only at `scoped-audit.md:293`, `:306` and `:353`.
- **What reading cannot prove:** whether a session ran the block and popped another session's stash outside the records read. Transcripts are not in the tree.
- **Already written:** nothing inherited. No work log, friction-log line, retro, futro or other audit folder names `git stash pop` or `npx vitest` (`0`, `stage-d/checks-bugs.out`; B-06 at stage B), so no record shows the block run and no stash entry or overwritten tree is known to need repair.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it: the block's commands against the repository's layout and the shared-stash rule; running the block to show the harm is exactly what must not be done.

## Acceptance criteria

- [x] At the fix's commit, `sed -n '340,365p' .claude/skills/mini-retro/references/scoped-audit.md | LC_ALL=C grep -c -E 'git stash( |$)|npx'` prints `0`, and the block names a detached worktree at `<base_sha>` removed with `tools/fork-worktree remove`.
  - at the parent `82de4931a7`: `the criterion range 340-365: 3 ; git stash lines: 2 ; npx in mini-retro: 3 ; a detached worktree: 0 ; fork-worktree remove: 0`; at the fix `f95a86a878`: `the criterion range 340-365: 0 ; git stash lines: 0 ; npx in mini-retro: 0 ; a detached worktree: 1 ; fork-worktree remove: 1`
- [x] `LC_ALL=C grep -rn -E '\bnpx\b' .claude/skills/mini-retro` prints no line, or each line it prints is marked as another stack's example.
  - the same record: `npx in mini-retro: 3` at the parent, `0` at the fix
- [x] The fix's commit cites this issue and #685, records the two greps before and after, and lands only in `.claude/skills/mini-retro/`.
  - `f95a86a878` cites #685 and #1390, records both greps before and after, and its `git show --stat` names only `.claude/skills/mini-retro/references/scoped-audit.md`

