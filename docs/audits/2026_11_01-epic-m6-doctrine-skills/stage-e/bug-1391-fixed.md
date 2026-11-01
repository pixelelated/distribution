Found by the M6 renovation's T38 slice, the skills, agents and settings (#685; audit [`docs/audits/2026_11_01-epic-m6-doctrine-skills/`](https://github.com/pixelelated/distribution/tree/feature/m6-doctrine-skills-685/docs/audits/2026_11_01-epic-m6-doctrine-skills), L-11, punch item PL-03). D-WORKFLOW-187: a defect the renovation finds is a bug like any other; ruling (c) of the slice's brief: a sentence a reader acts on wrongly is a `bug`.

The lines are at the dispatch tip `87c2ab0fed`, whose `.claude/` the slice branch has not changed.

**fixed-at:** `29b6e04aec` (stage E of T38, #685; the record `docs/audits/2026_11_01-epic-m6-doctrine-skills/stage-e/S7-PL-03.txt`). Each checkbox below is ticked from its check line, quoted under it.

## Code trace

- **How it was found:** L-11 in `02-forward-audit.md`, the auditor's read of the writing pair (`stage-b/checks-writing-pair*.out`).
- **The defect at its source (the sentence):** `release-notes/SKILL.md:19-21`: *"The body of a release on `pixelelated/distribution` (`tools/fork-publish-release` uploads the files; the note is written by hand and pasted with `gh release edit --notes-file`)."*
- **The artifact it misdescribes:** the tool itself. `tools/fork-publish-release:6` reads *"No upload, tag creation, asset replacement or publication occurs."*, and its one mode is `--prepare <BUNDLE>`, a checked local plan. Publication waits on #265, #344 and #528 (`device-builds.md` § Publishing).
  - The sentence was true when written: `9404f23c55`, 2026-09-29.
  - It became false ten days later: `f10eec1306`, 2026-10-09 (B-24).
- **The fix's shape:** the sentence says the tool prepares a release plan from exact candidate bytes and never publishes, and that publication waits on those issues. The note's own guidance (written by hand, pasted as the release body) stays.
- **Sibling sites, hunted** (`stage-d/siblings.out`): `fork-publish-release` is named nowhere else in the 52.
- **What reading cannot prove:** whether a session expected an upload from the tool and was misled outside the records read.
- **Already written:** nothing inherited. The fork's newest release is `rc1-20260929` (`gh release list`, `stage-d/checks-bugs.out`), published while the sentence was true. No release has been made since the tool stopped uploading, so no release body or asset was written under the false sentence.

**Can this be done on the VM?** No -- the tree, the tool or the register shows it: the sentence against `tools/fork-publish-release`'s own text and the tracker's release list.

## Acceptance criteria

- [x] At the fix's commit, `sed -n '17,24p' .claude/skills/release-notes/SKILL.md | LC_ALL=C grep -c uploads` prints `0`, and those lines name `--prepare` and #528.
  - at the parent `5662446a8a`: `the criterion lines 17-24, uploads: 1 ; --prepare and #528 there: 0 ; the tool says: 1`; at the fix `29b6e04aec`: `the criterion lines 17-24, uploads: 0 ; --prepare and #528 there: 2 ; the tool says: 1`
- [x] The fix's commit cites this issue and #685, records the grep before and after, and lands only in `.claude/skills/release-notes/`.
  - `29b6e04aec` cites #685 and #1391, records the grep before and after, and its `git show --stat` names only `.claude/skills/release-notes/SKILL.md`

