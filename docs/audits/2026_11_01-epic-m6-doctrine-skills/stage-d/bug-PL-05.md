Found by the M6 renovation's T38 slice, the skills, agents and settings (#685; audit [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`](https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills), L-13, punch item PL-05). D-WORKFLOW-187: a defect the renovation finds is a bug like any other; ruling (c) of the slice's brief: a sentence a reader acts on wrongly is a `bug`.

The lines are at the dispatch tip `87c2ab0fed`, whose `.claude/` the slice branch has not changed.

## Code trace

- **How it was found:** L-13 in `02-forward-audit.md`, the auditor's read of `futro` (`stage-b/checks-futro.out`).
- **The defect at its source (the sentence):** `futro/SKILL.md:479`: *"Prior retros accumulate as issue comments on Epic umbrellas; discover via `gh api repos/{owner}/{repo}/issues/{number}/comments --paginate -q '.[] | {author: .user.login, body: .body[0:300]}'`."*
- **The artifact it misdescribes:** this checkout's `gh` configuration and the repository's own rule.
  - `gh` fills `{owner}/{repo}` from the default repository. None is set here: `gh repo set-default --view` prints *"No default remote repository has been set"* (B-07, `stage-d/checks-bugs.out`).
  - The remote `gh` would fall back on is `upstream`, ROCKNIX's, which has Issues disabled.
  - `issue-tracking.md` requires `--repo pixelelated/distribution` (or its path) on every call.
- **The fix's shape:** the command names `repos/pixelelated/distribution/issues/{number}/comments`.
- **Sibling sites, hunted** (`stage-d/siblings.out`): `{owner}/{repo}` appears nowhere else in the 52. `futro/SKILL.md:255`'s `gh api …` is an example inside a list of probes, with no path. The Copilot-era `mcp_github_*` names beside these lines are PL-23's (L-14, L-21), not this bug's.
- **What reading cannot prove:** whether a session ran the read against the wrong repository and took an empty answer as *no prior retros*, outside the records read.
- **Already written:** nothing inherited. The command is a read and writes nothing to the tracker or the tree. No futro, retro or work log cites another repository's issue comments (`0`, `stage-d/checks-bugs.out`), so no record is known to rest on a wrong-repository read.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it: the command against `gh`'s configuration here and `issue-tracking.md`.

## Acceptance criteria

- [ ] At the fix's commit, `LC_ALL=C grep -c -F '{owner}/{repo}' .claude/skills/futro/SKILL.md` prints `0`, and `:479`'s command names `pixelelated/distribution`.
- [ ] The fix's commit cites this issue and #685, records the grep before and after, and lands only in `.claude/skills/futro/`.
