# Retrospective (Phase 3) — M6.P2 T10, the guards (#657)

Phase 3 of the code-auditor skill, read over the 31 paths at the two hashes, with the renovation face's questions answered in `04`. This file is the history: how the guards came to be the shape they are, what each fix round left, and the seams where two of them meet.

## 3.1 How the guards were built

- **The push guard first** (`f51d081c04`, 2026-09-05): the credential scan at the tip, for the two secrets GitHub's push protection does not know (a ScreenScraper `devpassword=` and a RetroAchievements key).

  **The `.po`/`.pot` exemption arrived in that same commit**, with no reason in its message (F-02). Every later rewrite carried it forward: `17dbb85b88` (PL-08, #151), `3e70ef9239` (the guard library), `9e104c65f3` (the pre-commit). None re-read why it was there. That is the shape `engineering-practices.md` § Verify design intent warns about, the other way round: a constraint whose reason was never written, preserved by every round because it looked deliberate.
- **Every commit in the push, not only the tip** (`17dbb85b88`, 2026-09-13, audit #151 PL-08), with the three proven refusals in the hook's header.
- **The pre-commit and the wordlist** (2026-09-28, #307 and #312): a fixture committed as a literal cost a history rewrite (blindspot 67). The guard library followed, failing closed on every read (PL-011), judging a line after its label (PL-026), and with no path exempt (PL-012).

  The fix round's audit (claude G3-E-01/02/07, gpt G3-E-05/06) found three scan-skipping shapes: `diff.noprefix`, a `++ ` content line, a quoted name. Each became a `hooks-test` case.

  **The binary file is the fourth shape of the same family (F-01).** Each of the three was a way an added line reached `guard_added_lines` in a form it did not read; the binary file is a way an added line never reaches it at all. No round constructed a file git does not diff as text, nor the fifth shape the second opinion found: a deleted `-- ` line in the same hunk, after which an added `++ b/` line is read as a header (F-35).
- **The checkers as a state machine** (`ceremony-check`, D-WORKFLOW-028, 2026-09-23), the push guard's gate and the fork CI's red badge. Audit #258 then moved the gate onto the primary checkout's tools (PL-004), so that a stale worktree could not skip it. That move also changed *which tree the gate reads* (F-16), and no record says that was weighed.
- **The renovation tools** (P1, 2026-10-22/23): the newest, and the only ones with a `--self-test`. The self-tests cover the parsing, not the counts the tools assert (F-27).

## 3.2 What each fix round left

| Round | What it fixed | What it left, found here |
| --- | --- | --- |
| #151 PL-08 (2026-09-13) | the range scan; `pr/*` keyed on the remote ref; failing closed on no base | F-10 (a quoted name in the personal-path match) |
| #307 / #312 (2026-09-28) | the pre-commit, the wordlist, three skip shapes | F-01 (binary), F-02 (`.po`), F-03 (`-m` `#` lines); the CI's lack of a credential scan (F-30) |
| #258 (2026-09-24/29) | the gate on the primary's tools; the retro marker anchored; the positives rule | F-16 (the gate reads the primary's tree); F-15 (the futro marker not anchored like the retro's) |
| #905 (2026-10-24, off this branch) | the friction reader reads every dated entry | F-15's residual: non-entry lines named, never owed |
| #646 (2026-10-22/23) | `register-check`'s `MISPLACED`, on this lane's branch (`f00ab3e163`), not yet on `next` | F-17 (slash shorthand, seven docs outside `LIVE`, T4's three) |

## 3.3 The class this slice hunted

T4's F-02 (`ceremony-check`'s friction reader skipping every line its regex did not match) and T6's #845 (`pkgcheck` exiting 0 on a name that matches nothing) are one class: **a checker that reads less than it reports, and passes.** Here it had 11 members at stage B; after the second opinion it has 10 (F-04, F-05, F-07, F-08, F-09, F-19, F-20, F-21, F-22, F-23). F-06 was removed on gpt's reason: a red run that hides a later verdict is not a pass.

- **A limit with no assertion:** F-04 (`box-check`, 300 of 458), F-05 (`ceremony-check`'s hygiene, 200 of 331).
- **A skip with no count:** F-07 (180 symlinks), F-19 (14 level-3 entries), F-20 (29 blindspot rows).
- **A boundary found by substring:** F-08 (the lint's `find`).
- **A pattern that cannot see the shape:** F-21 (22 computed titles), F-22 (five scripts not listed), F-23 (the sign-off).
- **An input diffed the wrong way:** F-09 (two trees, no merge base).
- **A failure read as success:**
  - F-09 (a missing ref, rc 0);
  - F-05 (`gh failed`, not counted);
  - F-20 (git and grep failures read as zero hits);
  - F-06 (a red step hiding the verdicts after it).

The guards on the security list proper (the hooks) belong to it once, through their callers: F-01, git's binary diff.

The rule that would have caught most of these is already written: `engineering-practices.md` § Guards must fail closed, *prefer a positive assertion over the absence of an error: collect what exists and check the count*. What is missing is its general use. The technique exists in three places, as gpt pointed out: `renovation-status:77-84` and `renovation-inventory:943-946` refuse a saturated issue list, and `rules-check` compares the file set with the index. The other readers here assert nothing about what they read.

## 3.4 What the record says the guards have been seen to do

The positives are counted in `04` § Q6.
- **The hooks:** one `hooks-test` case per refusal for every shape the fix rounds named (27 `expect` results at the hash).
- **The checkers:** a first run or a constructed failure in the work logs for `box-check`, `es-menu-map-check`, `register-check` (`MISPLACED`), `rc-preflight`, `pr-stack-check` and `lint-audit-artifacts`.
- **The CI:** a dispatch input built as its own positive (`ceremony_today`, #258 PL-020).

No positive is recorded for `forbidden-terms-check`'s tree scan with a hit, `fork-worktree remove`'s refusal, `work-log-index --check`'s STALE, `vocabulary-check`'s failure, `release-catalog --check`, or `rules-check`'s `count`/`mention`. A guard whose positive nobody can point at is the Q6 row `engineering-practices.md` names.

## 3.5 The seams

| Seam | Shared state | What crosses it | What this read found there |
| --- | --- | --- | --- |
| **The hooks × the fork CI** | the same two lists (the wordlist; the credential patterns), two runners | the wordlist: both sides (the hooks locally, `fork-wordlist.yml` on GitHub). The credential patterns: the hooks only | F-30: a credential pushed past the hooks (`--no-verify`, a clone without the hooks path) meets no fork check on GitHub. F-07: the CI's tree scan skips symlinks the pre-commit would have seen as a diff line |
| **`ceremony-check` × the push guard × `fork-checks.yml`** | one tool, three callers, three trees | the push guard runs it on the primary checkout's tree; the CI on a fresh checkout of `next`; `rc-preflight` on its own `ROOT` | F-16: the push gate judges a tree other than the one pushed. F-06: the CI's verdict for the ceremonies disappears on any day an earlier step fails. F-05: `box-check`'s and the hygiene line's limits pass into the gate's answer |
| **`rules-check` × the two entry files × the index** | `CLAUDE.md`, `AGENTS.md`, `instruction-files.md`'s tables, `fork-workflow.md`'s list, `PERSONAL_PATTERNS` | counts, names, tool rows | F-18: `mention` passes on a substring; the index's tool-to-rule direction unchecked (T4's F-22). P2: the personal-path lists agree today, entry by entry |
| **`lint-audit-artifacts` × every slice's close** | the audit folder contract; `audit-completion.json`; `ceremony-check`'s audit line | every slice's stage D and H run it; `ceremony-check` runs it on a completed folder | F-08: a real milestone folder passed with three High seat findings never required. The renovation face (`fc88815ccb`) checks headings, not answers; its fail fixture fails two checks at once |
| **The `renovation-*` tools × the dead-end tables and the status ledger** | `inventory.json`, `slices.json`, the slice issues' bodies | the inventory's reach column, which T24's and T5's dead-end tables trusted; `slices.json`'s `fixed_at`, which drift reads; the issue body's, which status reads | F-27: a failing inventory run rewrites the ledger. F-29: drift and status read `fixed_at` from two places. F-28: status's column and its `drifted` state. #898's reach gap is filed and stays its own |
| **`fork-worktree` × every lane's worktree** | the build roots no clone can rebuild (D-WORKFLOW-005) | `remove`, `repair`, `sync` on any worktree of the primary repository | F-11 (preserve, then destroy), F-12 (repair's `rm -rf`), F-13 (the loop); F-32's hint pointing at the legacy checkout's hooks |
