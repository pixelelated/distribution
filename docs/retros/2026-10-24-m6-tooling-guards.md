# Mini Retro: M6.P2 T10, the guards: hooks, the fork CI and the checkers (#657)

**Completed:** 2026-10-24.
**Scope:** the 31 member paths of slice T10 (`docs/reviews/briefs/tooling-guards.md` v2, `2a4be1006b`), at Extended depth.
- Stages A to D: the audit folder `docs/audits/2026_10_24-epic-m6-tooling-guards/`, punch list PL-01 to PL-44, audit issue #958, bugs #929 to #957.
- Stage E: ten streams under `docs/reviews/briefs/t10-streams.md` (`9e0718eeb5`, corrected at `cc46c1112a`).

**Branch:** `feature/m6-tooling-guards-657`.
**Delta:** stage E is 44 commits; the guarded paths (`.githooks`, `.github`, `tools`) changed in 37 files, +1,490/-316.

**Outcome:**
- 40 punch items Resolved, each by its commit; 4 Deferred to #959, #960, #640 and #585.
- `hooks-test` went from 41 to 67 `ok` lines (29 to 44 `expect` results).
- The lint on the folder prints PASS at its default phase.

## What worked well

- **The test first, against the unfixed tool, every time.** Each stream wrote its control and ran it against the tool before the fix. A fix commit then cites a count: S9's twelve controls fail 52 of 67 cases on the unfixed tools and pass 67 at the fixes. Two controls' expectations turned out wrong on that run (the drift shares), and the run showed which side was wrong.
- **Throwaway repositories with shims, never the fork's own.** Three controls ran this way:
  - `pr-stack-check`'s, in a two-line-map repository with a `git` shim logging every call, proved the `--force` fallback gone without running the tool on the fork;
  - the drift and status control, a stub `gh` with four slice issues;
  - the hooks', a stand-in wordlist assembled from `printf` pieces.
- **Measuring a tightened reader against the real corpus.** `rc-preflight`'s new trace reader was run over all 294 listed bugs beside the old one, and that is how its first cut's 10 false positives were found.
- **The coordinator's rulings, cited rather than re-argued.** The decisions came as rows: D-WORKFLOW-200, 201, 202, 204 and 205. The lane cited each in the code and recorded the MISSING lines until the hand-back merge, as it was told to.

## What was harder than expected

- **A result written before it was read, twice in one day** (stage C's folder scan; S4's checkpoint, which said `register-check` passed when it had printed FAILED). Both are friction lines. From S5 on, every result sentence was written only after its command's output had been read.
- **A list shared across three files.** S2 removed a `PERSONAL_PATTERNS` entry without running `rules-check`, which ties the hook's list to two rule files. S2's follow-up removed the two entries. From then on, the whole check set ran after every stream.
- **A reader that is stricter in one place is looser in another.** The first cut of `rc-preflight`'s one trace reader asked for words *under* a heading and missed traces on the heading's own line. Its control had no such case, and only the real corpus showed it (friction line, 2026-10-24).
- **A control can be vacuous too.** A case ended `|| true` and could not fail. It was replaced before the commit (friction line).
- **Bytecode left behind.** `py_compile` and `renovation-status`'s module loader write `tools/__pycache__/`, which is gitignored but is still a write in the tree. It was removed by name each time.
- **The session's `grep` is a ugrep function** with `-I --ignore-files`. Every count used `command grep`.

## Discoveries that affect future slices

- **Several fail-open shapes recur across the readers:**
  - a fixed `--limit` read as the whole set (`box-check`, `ceremony-check`, `rc-preflight`);
  - a regular expression that takes a heading for an answer (`rc-preflight`);
  - a count compared where a set was meant (`renovation-inventory`, `forbidden-terms-check`);
  - a `\b` after punctuation (`prose-check`);
  - a two-space key where records use one (`release-catalog`).

  Each is now a case in a control. The next slice that reads the tracker or a ledger should look for these first.
- **Ledger and tracker problems the fixed tools now report**, all the coordinator's:
  - `register-check`: 12 SHAPE rows and 42 EDITED rows;
  - `rules-check`: 31 Detail-in pairs;
  - `es-menu-map-check`: 21 computed-title pages, plus `SystemView.cpp:552` outside its reach (#965);
  - `release-catalog`: 395 kept folders without a RECORD.txt (#964);
  - `rc-preflight`: four acceptance rows that do not name their item (#963).
- **`renovation-status` had read every accepted-but-open slice as `unreviewed`.** It now has `fixed` and `withdrawn` (D-WORKFLOW-204): 11 slices read `fixed`.
- **The ES fork carries its own `guard-lib` (#961).** The history counts of listed words before the guard are with the maintainer on #312.

## Adjustments to remaining work

- **The coordinator's hand-back merge** brings D-WORKFLOW-201/204 and the twelve SHAPE fixes. `register-check` (MISSING 3, SHAPE 12 here) and `ceremony-check`'s register line clear only after it.
- **fix-pending-ci (#944):** the first red run on `next` after T9's merge and this branch's should show every step `success` or `failure`, none `skipped`. The coordinator reads it with `gh run view`.
- No other change to the order.

## What the slice did to time to play

Nothing. Every change is to a build-host hook, checker or workflow; no file on an image or a launch path was touched (D-CLOUD-098: interface to a game's first frame, and game to game, unchanged).

## What each stream did to a guard's refusals

| Stream | Guard | Refuses now that it did not | Allows now that it refused |
| --- | --- | --- | --- |
| S1 | `pre-commit`, `pre-push` (`guard-lib`) | a listed word or credential in a file git calls binary, in a `.po` file, or on an added `++ b/` line after a deleted `-- ` line; a personal path git quotes, refused as personal | none |
| S1 | `commit-msg` | a `#` line carrying a listed word given with `-m` | none |
| S2 | `pre-push` | a word in a parent dated after its child on a new branch; an annotated tag's annotation; a `pr/*` push with no `upstream/next` (no `origin/next` fallback) | none; a line with a credential and a listed word is refused and now prints neither |
| S3 | `guard-lib`, `secret-patterns` | a lowercase `pass`/`password =` assignment; a token value carrying `/`; a listed word in a file's name | none |
| S4 | `fork-worktree` | `remove` forces only on `--force`; a failed `--preserve` move stops; `--preserve` without a directory is a usage error; `repair` and `sync` report failures | none |
| S5 | `box-check`, `ceremony-check` | a short or failed tracker read is exit 2, not a pass; a marker that is not one no longer resets a clock | none |
| S6 | `forbidden-terms-check` | a listed word in a symlink's target or a file's name; a scanned count below the tracked count | none |
| S7 | `lint-audit-artifacts`, `ceremony-check` | a seat index cut short by a quoted heading; a hyphen-dated folder read like an underscore one | none |
| S8 | `fork-package-freshness` | a missing base ref is exit 2 | upstream's deletions no longer enter the set |
| S9 | the record checkers | `register-check`: shape and unreadable files. `work-log-index`: a duplicate date. `archaeology`: a failed search. `vocabulary-check`: an unreadable script. `prose-check`: a line-end sign-off. `release-catalog`: an empty artifacts directory. `pr-stack-check`: a renamed file's old path, an existing `pr-stack/N`. `rc-preflight`: an unknown acceptance kind, a hollow trace, a list at its limit. `renovation-inventory`: a set mismatch, with nothing written | `rules-check` no longer counts a name inside a path as a mention |
| S10 | `fork-checks.yml` | none: every check step now runs after a failure, so a red run shows every verdict (`!cancelled()`) | none |

## Scoped audit findings (Step 2.5)

- **AC conformance:** each bug's criteria are answered in `02` § Stage E with its control and real run.
- **Cornerstone spot-check:** PASS, on five checks.
  - No `--no-verify`.
  - No push beyond the branch.
  - No `fork-worktree sync|remove|repair`.
  - No `pr-stack-check` past `--help` on the fork.
  - No `gh workflow run`.

  `00-running-log.md` records none of these.
- **Interaction defects:** status and drift now share one fixed-at reader, which was the one interaction the slice found.
- **Housekeeping:** `register-check` rc 1 and `ceremony-check` rc 1, both explained; the W42 summary is the M7 lane's.
- **Harness self-coverage:** each new control was seen to fail on the unfixed tool, and S9 checked every new control for `|| true`.

## Practice adjustments

- When a check is tightened, measure it against the real corpus as well as the fixture, before the commit. This is recorded as a friction line and as case 9 of `rc-preflight`'s control; it is not yet a rule.
- `grep -c '|| true'` over a new control before it is committed.

## Code-verifiable state

| Bug | Fix | Control |
| --- | --- | --- |
| #929-#938 | `a00b0ac7bb`, `d55d34d6e1`, `32cb3a903e`, `db8ad3958a`, `148cee2a31` | `.githooks/hooks-test` (44 `expect`) |
| #939, #940 | `4b8419002d`, `0c0be666eb`, `d0c88f4528` | `tools/fork-worktree-test` (19) |
| #941-#946 | `66b08a6672`, `811e7f7d2f`, `66b324d1cd`, `34f32b28e6`, `2444828e89`, `917f91677b` | `docs/qa-logs/2026-10-24-box-check/`, `-forbidden-terms/`, `-package-freshness/`, `tools/test-fixtures/lint-audit-artifacts/run.sh` |
| #947-#957 | `4228bf4daa` to `4acaf55ceb`, `d78f422212`, `38306d3123` | `docs/qa-logs/2026-10-24-record-checkers/`, `docs/qa-logs/2026-10-02-candidate-preflight/rc-preflight-t10.py` |
| #944, PL-31 | `f4381c3501`, `f22b989ab1`, `22f9ae0d5e` | the parse and read-back; the run is fix-pending-ci |
