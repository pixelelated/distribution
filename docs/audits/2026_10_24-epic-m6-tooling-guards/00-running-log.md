# Epic Audit Running Log — M6.P2 T10, the guards: hooks, the fork CI and the checkers

**Auditor:** the code-auditor skill, with the renovation face of `docs/reviews/plan-for-the-plan.md` § 4.
**Primary model:** Claude Opus 5.5 (`claude-opus-5-5`, lab Anthropic) at high effort, in Claude Code. The identity comes from the coordinator's dispatch on #657 (issuecomment-6386632699, 2026-10-24T16:26:15Z) and from the session's own metadata.
**Session:** herdr agent `m6-t3-emulators`, session `a6d65411-5a44-4596-9a6c-337855905c17`, pane `wN:p6`. The same session ran T3, T30, T24 and T4. Those four worktrees are accepted and idle beside this one, and nothing is written in them.
**Started:** 2026-10-24 16:26 UTC (`date -u` gave 16:26:47 at the first commands).
**Scope:** the slice `tooling-guards` (#657, `M6.P2 E903/T10`), under the area epic #903 (the tooling and guards) and the renovation epic #339, in milestone M6. Its membership is the inventory's `tooling-and-guards` rows under brief § 2's globs: 31 paths.
**Spec:** `docs/reviews/briefs/tooling-guards.md`, version 2 (`2a4be1006b`). Its § 7 is #657's checklist, and #657 wins where the two differ. The plan, `docs/reviews/plan-for-the-plan.md`, was read whole in this lane's worktree before the first command.
**Depth:** Extended (plan § 6c; D-WORKFLOW-184, 195). At Phase 4.6, GPT-6 Astra at `max` and Gemini 4 Argon at `high` are called through the Facilitator. `npm install` runs only under `tools/council`.
**Branch / worktree:** `feature/m6-tooling-guards-657`, at `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-guards-657`.
**Read hashes:**
- The 28 at-hash files are read at `next`'s `8ebaf8daad`, from `.qa-scratch/t10/at-hash/`.
- The three `renovation-*` tools are read at P1's `2174265e9c`, from `.qa-scratch/t10/at-p1/`, together with the lint's fixtures.
- `reviewed-at` is the branch `HEAD` at stage A, `a82d784216`, and names both hashes.

**Proof tokens:** a line in this log that records a proof begins with the proof token. Criterion 14 counts those lines against the `proved:` cells of `02-forward-audit.md`. This header names the token without starting a line with it.
**The security list:**
- The wordlist and every credential file are never read into this folder.
- No credential-shaped line and no listed word is written here.
- A hit is named by `path:line` only, and a credential value by the hooks' `[REDACTED]`.

---

## Log Entries

### [Phase 0] 16:26-16:28 — The dispatch read; the brief's first commands (`date -u` 16:26:47)

- **The dispatch** (issuecomment-6386632699, 16:26:15Z) was read first, then the pointer, the plan whole and the brief whole.
- `git fetch origin` and `git fetch upstream --no-tags`: rc 0. `upstream/next` is `481c9d0d75`. `next` and `origin/next` are both `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`, so the read hash is still `next`.
- **The branch and the stack:** the branch is `feature/m6-tooling-guards-657` and `HEAD` is `a82d784216f5bc4f39ce1490dee95cd96beb887e`, the dispatch's hash. `git merge-base --is-ancestor 2174265e9c HEAD` exits 0, so the branch is stacked on P1. `docs/reviews/inventory.json` is present.
- `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts` lists **8 files, +127/-11**, exactly the dispatch's eight paths, and nothing else is stale:
  - `device-builds.md` +9;
  - `engineering-practices.md` +10;
  - `fork-workflow.md` +1/-1;
  - `generic-x64-vm-testing.md` +7;
  - `instruction-files.md` +4/-1;
  - `code-auditor/references/templates.md` +18/-1;
  - `council/IMPORTED-FROM.md` +25;
  - `tools/lint-audit-artifacts` +55/-6.
- **The hooks path:** `git config core.hooksPath` is `/workspace/repos/pixelelated/distribution/.githooks`, which is absolute and points at the primary checkout. `ls` of it lists `commit-msg guard-lib hooks-test pre-commit pre-push secret-patterns`, with `pre-push` among them. This lane runs the primary's copy at every commit and never edits it.
- `test -r ~/.config/rocknix/forbidden-terms`: true. The wordlist is present and was not read.
- `df -i /tmp` 40 % (417,543 of 1,048,576 inodes); `df -i /workspace` 21 %. Exports and scratch go to `/workspace/tmp/m6-t10/` and the gitignored `.qa-scratch/t10/` (`git check-ignore` confirms the latter).
- **The read trees:**
  - `git archive 8ebaf8daad <the 28> | tar -x -C .qa-scratch/t10/at-hash`: rc 0, **28 files**.
  - `git archive 2174265e9c tools/renovation-{inventory,drift,status} tools/test-fixtures/lint-audit-artifacts | tar -x -C .qa-scratch/t10/at-p1`: rc 0, **13 files** (the three tools and ten fixture files).
- **The host file's last block** is the M6 coordinator's at 16:06 UTC: M7's resource window closed early, and M6 holds the host. `pgrep -c -x qemu-system-x86` prints 0. This slice starts no guest and no build.

### [Stage A] 16:28-16:31 — Scope re-derived; the deltas; every suite's exit (`date -u` 16:28:52, 16:29:38)

- **The membership** (brief § 2's block, run unchanged under `python3 -I`; the list is kept in `.qa-scratch/t10/paths.txt`):
  - **31 paths and 6,676 lines** by the inventory's column. 29 are `fork-own` (6,290 lines) and 2 `upstream-carried` (386).
  - Reach is `n/a` for all 31.
  - By language: 14 `python`, 11 `shell`, 4 `yaml`, 2 `none`.

  The glob also selects 375 paths in other areas (`.github/ISSUE_TEMPLATE`, the PR template, `.github/sessions`), which are not this slice's. **No delta from the brief.**
- **Lines at the read refs:** `git show <ref>:<path> | wc -l` per path gives **6,642**, with the three `renovation-*` tools at `2174265e9c` and the 28 at `8ebaf8daad`. The table is in `.qa-scratch/t10/lines.txt`. This equals the brief's figure, so there is no delta.
- **Provenance:**
  - `git cat-file -e upstream/next:<path>` succeeds for exactly the two `.github/scripts/*.sh` files.
  - `generate-release-body.sh` is byte-identical to `upstream/next`.
  - `generate-changelog.sh` differs by **+1/-8**. **Delta from the brief, a stage-B lead:** the brief reads this as a fork hunk (`8a7f33791d`), but `git log c445081a59..upstream/next -- generate-changelog.sh` shows the two commits that make the difference are **upstream's**, after the fork's last merge: `76693a738d` (2026-10-13, *ci: add github username to release*) and `71d8932b33` (2026-10-14, *openabl: introduce package*). `next`'s only commit on the file in the range is the merge `7bd7f31312`. The minus lines are upstream additions the fork has not merged, not fork deletions. This is a Q4 currency row, read at stage B.
  - **128 fork commits** since `c445081a59` over the 28 at-hash files, **125 without merges**. No delta.
- **The branch against the hash over the 28** (`git diff --stat 8ebaf8daad HEAD`) touches **5 files, +92/-9**, the five the brief names:
  - `hooks-test` +7 and `pre-commit` +13/-1, from `1b8ac30421` (#696);
  - `pre-push` +3, from P1's `9966dbcd12` and `af24589b1c`;
  - `register-check` +17, from `f00ab3e163`;
  - `tools/lint-audit-artifacts` +61/-9, from `fc88815ccb`, `6874394d49`, `fa6bcdafa8`/`18747fbc52` and the merge `50137e3ee0`.

  **A delta in the commit list, not in the hunks:** the brief names `fc88815ccb` and `18747fbc52` for the lint, but its +61/-9 also carries **`6874394d49`** (2026-10-22, *audit: verify explicit Argon reviewer receipts*, +13/-7 in the lint). That commit is in the coordinator's tip `69fcce37b3`, which the dispatch names as merged at `50137e3ee0`. So it is not a stop (stop condition § 8 is *a hunk the dispatch comment did not name*, and the file is named); it is recorded in `01` § Scope. The branch against P1's `2174265e9c` over the three `renovation-*` tools is empty.
- **The after-hash delta off this branch:** `9e12014623` (2026-10-24 15:26:33Z, `ceremony-check` +55/-9, #905) is not an ancestor of `HEAD`. It is read as a delta at stage B.
- **`PERSONAL_PATTERNS` at the hash:** `pre-push:62` opens it and `:188` closes it, with **115 quoted entries**, 84 of them beginning `tools/`. That agrees with the brief. **A delta:** **14** entries begin `scripts/` against the brief's 12. This is re-derived at stage B in the entry-by-entry diff.
- **The suites and self-tests,** run in this worktree with each output kept under `/workspace/tmp/m6-t10/baseline/`:

  | Command | rc | Summary line |
  | --- | ---: | --- |
  | `.githooks/hooks-test` (the worktree) | 0 | `PASS`; 41 `ok` lines: **29** `expect` results (refused or allowed) and 12 `says`/`silent` checks |
  | `.qa-scratch/t10/at-hash/.githooks/hooks-test` (the hash) | 0 | `PASS`; 38 `ok` lines: **27** `expect` results and 11 `says`/`silent` checks |
  | `tools/register-check` | 0 | `667 IDs, each once; every citation in the live documents names a row` |
  | `tools/rules-check --quiet` | 0 | (silent) |
  | `tools/work-log-index --check` | 0 | `work-log index: current` |
  | `tools/prose-check --self-test` | 0 | `self-test: PASS` |
  | `tools/ceremony-check` | 1 | `DUE weekly OVERDUE: 2026-W42 summary missing`; the other ten lines `ok` |
  | `python3 -I tools/lint-audit-artifacts <P1 fixture>/fixture-epic-m6-renovation-pass` | 0 | `PASS` |
  | `python3 -I tools/lint-audit-artifacts <P1 fixture>/fixture-epic-m6-renovation-fail` | 1 | `2 CONTRACT FAILURE(S)` |
  | `tools/box-check --quiet` | 0 | `300 issue(s), 762 open checkbox(es), 0 fail, 24 issue(s) with rows to re-derive against` |
  | `tools/fork-worktree list` | 0 | read only. `m6-renovation-plan-346` `HOLDS BUILD OUTPUT (2.6G)`; this worktree and T9's are `checkout only` |
  | `tools/es-menu-map-check --help`, `rc-preflight --help`, `archaeology --help`, `pr-stack-check --help` | 0 each | usage only. Each tool's argument parsing was read first: `pr-stack-check` handles `-h|--help` in its argument loop before `cd` or any `git` call |

  The W42 week is the M7 lane's to pay, as the brief says.
- **The case counts, a delta:** the brief says 22 `expect` cases in the worktree and 20 at the hash. Counted as `ok` lines that end in `: refused` or `: allowed`, the runs give **29 and 27**. The difference between the two runs is two in both counts (#696's marker case and its setext control), so the brief's own figures are short by seven on each side. This is re-counted case by case for `02` § The suites.
- **The API budget, and a slip in the order:**
  - `tools/ceremony-check` runs `box-check` inside it, so the tracker was read **before** the budget. That inverts § 8's *no `box-check` before the API budget is read*.
  - The first budget read, right after, was core **4,977 / 5,000** at 16:28:52Z (reset 17:20:33Z).
  - The explicit `box-check --quiet` then ran with the budget read on both sides: **4,976 → 4,976** (16:29:04Z → 16:29:06Z). GraphQL stood at 4,999 / 5,000 after it. `box-check` reads through `gh issue list`, which is GraphQL and costs no core requests.

  The slip is a friction line.
- **A lead from the baseline itself, for stage B (Q3):** `box-check:83` calls `gh issue list ... --state open --limit 300`. The fork has **458 open issues** (GraphQL `issues(states: OPEN) { totalCount }` at 16:29Z), so a run reads 300 of them and still prints `0 fail` and exits 0. The ceremony line and `fork-checks.yml`'s step read the same output. This is the #845 class (a checker that reads less than it reports and passes); it is graded at stage B.
- **The full-tree wordlist scan** (`tools/forbidden-terms-check` over this worktree) runs in the background, with its output in `/workspace/tmp/m6-t10/ftc-tree.out` and a waiter armed on the process. Its result and duration are recorded in the next entry.
- `git push -u origin feature/m6-tooling-guards-657` follows this entry's commit.
- **The full-tree wordlist scan:** `tools/forbidden-terms-check` (no argument, so this worktree) exits 0 with `forbidden-terms-check: 0 hits in 133409 tracked files`, in **147 s** of wall time from its start at 16:28:4x. `git ls-files | wc -l` would give the tracked total. The 56 tracked paths the scan skips are symlinks, submodules or deleted files (`[ -f ] && [ ! -L ] || continue`, `forbidden-terms-check:37`); they are a stage-B read (Q3: what the skip lets through, and that the scanned count is never compared with the listed count).
