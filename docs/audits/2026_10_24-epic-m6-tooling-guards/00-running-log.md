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
- **The full-tree wordlist scan:** `tools/forbidden-terms-check` (no argument, so this worktree) exits 0 with `forbidden-terms-check: 0 hits in 133409 tracked files`, in **147 s** of wall time from its start at 16:28:4x. `git ls-files | wc -l` is **133,589** (read after the commit `5611a4fb62` carried this line with a typed *56*, corrected here), so **180** tracked paths are skipped: symlinks, submodules or deleted files (`[ -f ] && [ ! -L ] || continue`, `forbidden-terms-check:37`); they are a stage-B read (Q3: what the skip lets through, and that the scanned count is never compared with the listed count).

### [Stage B] 16:33-16:38 — The security files read: the hooks, guard-lib, the workflows, fork-worktree; the CI record; the constructed gaps

- **The coordinator's post on #657 at 16:33 UTC** accepts the three deltas of stage A (written into the brief on its branch at `ac6dd7b205`). It rules that `box-check`'s `--limit 300` and `forbidden-terms-check`'s skipped symlinks are **Q3 bugs, filed at stage D** with constructed positives against a stand-in list.
- **Readers:** four read-only research subagents were given the checkers in four groups, with no tool run, no `gh`, and no read of the wordlist or a credential file:
  - R1: `ceremony-check` and #905's diff, `register-check`, `rules-check`, `work-log-index`, `box-check`;
  - R2: `lint-audit-artifacts`, `archaeology`, `es-menu-map-check`, `vocabulary-check`, `prose-check`, `release-catalog`;
  - R3: `rc-preflight`, `fork-package-freshness`, `pr-stack-check`, the two upstream scripts;
  - R4: the three `renovation-*` tools.

  Their reports are leads, re-derived here before any becomes a finding. The security list's files (the three hooks, `guard-lib`, `secret-patterns`, `forbidden-terms-check`, the four workflows, `fork-worktree`) are read in this session, not delegated.
- **The primary checkout's `.githooks/`** (`diff -r` against the worktree's) is the **hash's** copy. It lacks #696's marker refusal and P1's three personal patterns, both of which are only on lane branches. So every lane's commits and pushes today run the hooks at `8ebaf8daad`, and the at-hash read is the read of what runs.
- **The CI's record** (read only, core 4,967 → 4,958):
  - `fork-checks.yml` on `next`: six `failure` runs from 2026-10-19T13:07Z to 2026-10-24T10:54Z, all `schedule`, all at `8ebaf8daad`, and the last success 2026-10-18T11:00:07Z. No push to `next` has run it since 2026-10-17T06:03Z.
  - The failing steps: 10-19, 10-20, 10-21 and 10-22 fail on *every open acceptance checkbox is agent-verifiable (D-QA-044)*, **with *ceremonies are not overdue* `skipped`**; 10-23 and 10-24 fail on *ceremonies are not overdue*.
  - The 10-24 run took 2 min 41 s (10:54:38Z → 10:57:19Z).
  - `fork-wordlist.yml`: success on every branch push read, the lane's two today among them; the last run on `next` was 2026-10-17T06:03Z, a success.
  - `gh api .../actions/workflows`: **23 workflows, 23 `active`**.
  - `gh secret list` prints `failed` for this token, so the `FORBIDDEN_PATTERNS` secret's existence is inferred from `fork-wordlist.yml`'s green runs, whose header says the job is red without it. Its value was never read.
- **A lead from the record (Q3):** a red step skips every later step. On the four days `box-check` failed, the ceremony check never ran, so the record holds no ceremony verdict for 10-19 to 10-22.
- **`.po` and `.pot` are exempt from every hook scan:** `pre-commit:13` and `pre-push:267,268,271,272` pass `':!*.po' ':!*.pot'`. The exemption came with the push guard's first credential scan (`f51d081c04`, 2026-09-05), whose message gives no reason, and it contradicts `guard-lib:20` (*no path is exempt*). `git log -S"--diff-filter=ACMRT" -- .githooks` names `9e104c65f3` (2026-09-28) for the pre-commit's filter.
PROOF: P1 the constructed guard gaps at the hash -- `docs/audits/2026_10_24-epic-m6-tooling-guards/tools/t10-guard-gaps.sh .qa-scratch/t10/at-hash/.githooks .qa-scratch/t10/at-hash/tools/forbidden-terms-check /workspace/tmp/m6-t10` (16:36:51Z, rc 0; output kept at /workspace/tmp/m6-t10/gaps-hash.txt) with a stand-in wordlist and a credential value built from printf pieces, nothing printed but the exits: pre-commit ALLOWS a credential and a listed word in a file git treats as binary (rc 0, rc 0) and in a `.po` file (rc 0, rc 0), and REFUSES the same credential in a text file (rc 1, redacted); `commit-msg` through a real `git commit -m tidy -m "# ..."` ALLOWS a listed word on a `#` line (rc 0) and the stored message keeps the line (1), the control on an ordinary line is refused (rc 1), and the push guard then REFUSES that branch (rc 1); pre-push ALLOWS a credential in a binary file committed and removed inside the push (rc 0; the text control rc 1) and a credential and a listed word in a `.po` file at the tip (rc 0, rc 0); a pr/* branch adding `docs/<a non-ASCII name>.md` is refused only because the tip scan cannot read the quoted name (`could not be read`), not as a personal path -- with `core.quotePath=false` it is refused as `personal artifacts`, and the ASCII control is too; `forbidden-terms-check` names `plain.txt` and not the symlink whose target carries the word (1 hit of 2), and on the same tree with its tracked files deleted from the checkout prints `0 hits in 0 tracked files` and exits 0. The script's reason tags are loose -- the pre-commit's closing hint names "a listed word" on every refusal -- so a refusal's reason is read from the specific tag, not from that one.
PROOF: P2 the personal-path lists agree -- `python3 -I .qa-scratch/t10/pp-diff.py 8ebaf8daad HEAD`: at the hash the hook's 115 entries are all in `fork-workflow.md` § Personal paths and every path-shaped token of that section is a hook entry except four prose mentions (`.githooks/pre-push`, `packages/`, `projects/`, `tools/`); at HEAD the same with 118. The stage-A delta resolves: the 14 `scripts/` entries are 12 directly under `scripts/` and 2 under `scripts/lib/` (`council-`, `verifier-pins.ts`), so the brief's 12 counts the first group.
PROOF: P3 the push guard's cost -- the hash's `pre-push` fed this branch's tip over remote states `HEAD~1`, `HEAD~20`, `HEAD~100` (first parent; remote ref `refs/heads/t10-timing-probe`, so neither the ceremony gate nor the pr/* checks run; nothing is sent): 1 commit 0.07 s, 164 commits 0.76 s, 247 commits 9.82 s, each rc 0 with no output. The range's commits already on `origin`'s remotes are excluded from the line scan (`--not --remotes=origin`), so the cost is the tip scan of every file the range changes, read whole.

### [Stage B] 16:38-16:48 — The readers' leads re-derived; the proofs

- **The four readers' reports** arrived 16:41-16:44. Each lead that became a finding in `02` was re-read here at its line, or re-run.
- **Withdrawn:**
  - R1's claim that `AGENTS.md` carries no count sentence (it has one);
  - R4's D2 (drift counts a modified line twice), because plan § 8 itself measures with `git diff --stat`, which counts the same way.
- **Corrected:** R2's *21 of 74* became 22 of 75 under this session's own command.
- **A method finding about this harness, not the tree:** the interactive shell's `grep` is a function running ugrep with `-I --ignore-files`, while the hooks and tools run GNU grep 3.12 (`type grep`; `bash -c 'grep --version'`). Every count after 16:39 was taken with `command grep`, and the earlier ones were re-taken. One ugrep run refused a pattern (*exceeds complexity limits*); the GNU run of the same test is P3b.
- **Two of my own errors, caught before commit:**
  - a `-work_log` file pattern written as `_work_log` gave a count of 0;
  - a freshness `--list` run from the export's copy resolved `ROOT` into `.qa-scratch`.

  Both were re-run (P8, P14).
- **Two runtimes in `02` were first typed as estimates** (*about 3 s*, *about 10 s*). They were replaced by measurements before commit: `hooks-test` 0.71 s, `ceremony-check` 7.95 s (16:47Z).
PROOF: P3b the redaction survives the slash -- `secret-patterns`' fifteenth alternative carries `/` inside a bracket class; a constructed line built from pieces (`printf 'PASS%s=%s' WD ...`), matched by `command grep -a -E` with the guard's own label regex (1 match, rc 0), then `sed -E "s/(${SECRET_PATTERNS})/[REDACTED]/Ig"` (GNU sed 4.9): rc 0, the value survives 0 times, `[REDACTED]` 1. The lead (a `/` breaking the `s///`) is withdrawn.
PROOF: P4 box-check's limit -- `box-check:83` is `--limit 300`; `gh api graphql ... issues(states: OPEN) { totalCount }` = 458 at 16:29Z and 473 at 16:47Z; `box-check --quiet` printed `300 issue(s) ... 0 fail` rc 0 at 16:29:04Z.
PROOF: P5 ceremony-check's hygiene limit -- `ceremony-check:423` is `--limit 200`; `gh api graphql search(query: "repo:pixelelated/distribution is:issue is:closed reason:completed closed:>=2026-09-21")` issueCount = 331 (run between the 16:38Z and 16:47Z reads; its own time was not recorded); the stage-A run's hygiene line was `ok`.
PROOF: P6 the tracked symlinks -- `git ls-files -s | awk '$1=="120000"' | wc -l` = 180, `$1=="160000"` (submodules) = 0, `git ls-files --deleted` = 0; `git ls-files | wc -l` 133,589 against the scan's 133,409 = 180.
PROOF: P7 the CI's skipped steps -- `gh run view <id> --json jobs` for the six red runs on `next` (40087768497, 39947006860, 39773227474, 39594189379, 39415615874, 39257547676): the four of 10-19 to 10-22 fail on the D-QA-044 step with `ceremonies are not overdue: skipped`; the two of 10-23 and 10-24 fail on the ceremony step; 39121456626 (10-18) green.
PROOF: P8 the level-3 entries -- `git ls-tree -r --name-only 8ebaf8daad -- docs/work-logs/ | command grep -E -- '-work_log\.md$'` = 74 day files; `^### [0-9]{2}:[0-9]{2} UTC` lines: 1 in 2026_10_02, 3 in 2026_10_14, 10 in 2026_10_15, total 14; `work-log-index:40` reads `## ` only; `--check` rc 0 at stage A.
PROOF: P9 archaeology's blindspot gap -- `tools/archaeology --no-gh "busybox unzip"` rc 0 prints `== The blindspot register (0)`; `command grep -c 'busybox unzip' docs/blindspot-register.md` = 2, in row 7 of the table before `## 29.` (line 40); 29 `| N |` table rows precede it.
PROOF: P10 the lint's boundary -- in `docs/audits/2026_09_28-milestone-audit-of-the-fix-round/02-forward-audit.md`, `command grep -n '## Verification'` finds line 192 (a table cell quoting the lint's own `forward.find("## Verification")`) before the real heading at 882; `## Findings index` is at 14; `lint-audit-artifacts:182` at the hash is `fi, vi = forward.find("## Findings index"), forward.find("## Verification")`, so the index it reads is lines 14-191.
PROOF: P10b prose-check's sign-off -- a draft whose last line is `That's it!` (`/workspace/tmp/m6-t10/prose-draft.md`): `tools/prose-check` rc 0, `PASS (0 fail, 0 warn)`; the control ending `Happy gaming!` rc 1.
PROOF: P11 the --preserve loop -- the shape of `fork-worktree:158-164` (`while [ $# -gt 0 ]; case --preserve) p="${2:-}"; shift 2`) lifted into `bash -c` with `set -- /x --preserve` under `timeout 3`: `still looping after 100001 passes`, rc 3. The tool itself was not run (§ 8).
PROOF: P12 es-menu-map-check's invisible pages -- at the ES pin `16dbac5211` (`~/Development/emulationstation-next`, read with `git grep` at the commit): `new GuiSettings(` 75 occurrences in `es-app/src` and `es-core/src`; with a `_("...")` literal as the title argument 53; so 22 titles are computed and invisible to `es-menu-map-check:50-56`'s three patterns.
PROOF: P13 vocabulary-check's script list -- `vocabulary-check:111` names `cloud_backup cloud_restore cloud_content_backup cloud_content_restore cloud_setup cloud_saves_root cloud_net_ready` and `backuptool`; `ls projects/ROCKNIX/packages/network/rclone/sources/` also holds `cloud_capture`, `cloud_content_transfer`, `cloud_oauth`, `cloud_scan`, `cloud_sync_helper`.
PROOF: P14 fork-package-freshness's set -- the worktree's copy (`git diff --quiet 8ebaf8daad HEAD -- tools/fork-package-freshness`: identical) `--list`: 47 rows against `upstream/next` (`481c9d0d75`), 26 against the merge base `c445081a59`; 22 only in the first (libfreeaptx opus strace libfmt aethersx2-sa glslang spirv-headers vulkan-headers cargo cargo-snapshot cbindgen rustc-snapshot rust-std-snapshot file i2c-tools grub miniupnpc qemu rocknix-abl tllist mtdev swaybg), 1 only in the second (`projects/ROCKNIX/packages/multimedia/gstreamer/gstreamer`); `comm` warned of unsorted input under the shell's locale, so the two lists are re-compared under `LC_ALL=C` in the stream; `git diff --name-only --diff-filter=M c445081a59 8ebaf8daad -- packages projects` gives 63 `package.mk`, 8 of whose diffs touch a `PKG_VERSION=` line; `FRESHNESS_BASE=refs/heads/no-such-ref tools/fork-package-freshness --list` prints `fatal: bad revision` on stderr, 1 row (rclone) and rc 0.

### [Stage C] 16:54-16:57 — Phase 4.6: the Facilitator, the probes, the packet, the refutations started

- 16:54:30 `npm install --prefix tools/council`: rc 0. It warned that install scripts were not run, which the earlier slices' runs also met. `tools/council/run verify-pins`: `OK - verifier pins match current files and every re-pin is accountable.` rc 0. `tools/council/run test`: rc 0, with 39/39, 127/127 and 19/19 passing and 0 failing. `run` sources `~/.config/council/env` itself; the file was not read here.
- **Probes**, 16:55:41 to 16:55:50, with `--provider openrouter` and T30's one-line prompt (`*-probe-prompt.md`):
  - `gpt`: served `openai/gpt-6-astra` by `OpenAI`, effort `max`. Identity source `provider_response`; verification PASS, effort PASS, provider PASS. The model's own reply was `READY unknown`; the provider's field is the identity.
  - `gemini-argon`: served `google/gemini-4-argon` by `Google`, effort `high`, all three PASS. Its reply: `READY Gemini 4 Argon`.
- **The packet** (`tools/t10-packet.py`, the manifest `second-opinions/packet-manifest.json`): 39 sources, the 31 files among them, each with its sha256 at its read ref.
  - The body is 479,616 bytes: `02`, `03` and `04` whole; `fork-workflow.md`'s *Personal paths* and *Safety net* and `ceremonies.md`'s table, from `next`; the 31 files line-numbered; and the constructed cases with their 16:36:51Z output.
  - The two briefs share the body. Gemini's ask is bounded to 6,000 words, with parts 1 and 2 first, because T30's Gemini seat was cut at its output ceiling (D-WORKFLOW-195).
- **The packet's scan, before it was sent:** both briefs, `tools/forbidden-terms-check --stdin` `0 hits on stdin` rc 0, and 0 lines matching the pre-commit's `SECRET_PATTERNS` (`/usr/bin/grep -a -c -E`).
- **Refutations started** at 16:56:51 (the logs' mtime), both seats in parallel, with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000` passed explicitly.
  - **What watches them:** the harness background task, which waits on both and delivers their end.
  - **Its silent mode:** a hung seat is ended only by those timeouts, 1 h per attempt and 3 h in total. The failed-seat rule holds: hold, diagnose, one same-slug retry on a transient cause, never one seat.

### [Stage C] 17:33-17:38 — The two refutations returned; their claims constructed or re-read; the grading

- **Both seats returned on their first attempt, with `finish=stop`** (the background task's lines, 16:56:51Z → 17:33:42Z):
  - `gpt`: 37,745 bytes in 2,210,853 ms, 146,966 prompt and 90,082 completion tokens (81,171 of them reasoning). Served `openai/gpt-6-astra` by OpenAI at effort `max`; identity, effort and provider PASS.
  - `gemini-argon`: 23,188 bytes in 477,771 ms, 165,358 prompt and 47,632 completion tokens. Served `google/gemini-4-argon` by Google at `high`; all PASS. It stayed under its 6,000-word bound.
- **Both outputs were scanned before being read:** `forbidden-terms-check --stdin` 0 hits each, and 0 credential-pattern lines each.
- **The claims constructible with a stand-in list and a throwaway repository** went into `tools/t10-guard-gaps-2.sh`. The rest were re-read at their lines, and the grading is `04` § Second opinion.
- **The coordinator's post on #657 at 16:57 UTC** keeps `pkgcheck` out of this slice (bug #928 under #800) and gives `fork-package-freshness`'s half of T8's row to this lane (F-09). It names F-01 and F-11 as stage-D bugs with constructed positives built from a stand-in list and a throwaway repository, and F-16 and F-30 as recorded leads, not streams. `02` § Leads not in this slice's paths points at #928.
PROOF: P15 the seats' constructed cases at the hash -- `docs/audits/2026_10_24-epic-m6-tooling-guards/tools/t10-guard-gaps-2.sh .qa-scratch/t10/at-hash/.githooks /workspace/tmp/m6-t10` (17:36:36Z, rc 0; output /workspace/tmp/m6-t10/gaps2-hash.txt), stand-in list, values from pieces, exits and tags only: a deleted `-- ` line replaced by an added `++ b/<credential>` line ALLOWED by pre-commit (rc 0), the same with a listed word rc 0, the hooks-test-shaped control `++ <credential>` refused (rc 1), the `++ b/` credential in a middle commit gone at the tip ALLOWED by pre-push (rc 0); a credential added and removed on a merged side branch REFUSED (rc 1, cred) in both shapes -- gpt G-01 refuted; `rev-list`'s last for the new branch is the child `D`, and the parent `C` whose message carries the stand-in word is ALLOWED (rc 0); an annotated tag whose annotation carries the word ALLOWED (rc 0); a line with a credential and the word REFUSED but `WORD-PRINTED`; a lowercase `password = <20 characters>` ALLOWED (rc 0) and a slash-bearing JSON refresh token ALLOWED (rc 0); a clean file whose name carries the word ALLOWED (rc 0); a pr/* branch adding `docs/<non-ASCII>.po` ALLOWED (rc 0); hooks-test's quoted-name credential case REFUSED with both the `cred` and `unread` tags, so the range scan does detect it -- gpt's doubt about that case refuted; a pr/* branch carrying `docs/plan.md` with only an `origin/next` that holds it ALLOWED (rc 0).
PROOF: P16 the audit folders' date format -- `ls docs/audits`: 23 entries, 22 matching `^[0-9]{4}_[0-9]{2}_[0-9]{2}-`, 0 matching `^[0-9]{4}-[0-9]{2}-[0-9]{2}-` (the 23rd is `README.md`); `ceremony-check:364` matches `(\d{4})-(\d\d)-(\d\d)` and `lint-audit-artifacts:144` matches `(\d{4})_(\d\d)_(\d\d)`.
- **Grading done** (`04` § Second opinion): 44 findings, 6 High, 25 Medium, 13 Low (`.qa-scratch/t10/grades.json`, asserted against `02`'s headings).
  - **Confirmed new:** F-35 to F-44.
  - **Refuted:** gpt G-01 (history simplification) and gpt's doubt about `hooks-test`'s quoted case.
  - **Narrowed:** gemini G-11 (`MISPLACED` is this branch's) and F-09, F-17, F-20, F-25.
  - **Re-graded:** F-02 to High; F-06 to Low and out of the class; F-10, F-14, F-15, F-26, F-27, F-28, F-30 and F-32's hint to Medium.
- `tools/lint-audit-artifacts <folder> --phase pre-issue`: 4 contract failures, every one `05-punch-list.md`'s (absent until stage D), and `ok review plan: extended, 3 model perspectives, 2 verified external calls`, `ok 04 § Renovation face answers Q1 to Q7`.
- **The folder's scan, corrected:** this line first said criterion 10's grep summed to 0. It was written into the same command as the grep, before the result was read, and was committed and pushed in `a4f478cd5c`. The command had printed **9**, and that statement was false.
  - **What the 9 are,** located by file and line with the values elided: 1 in this log (the line quoting the criterion's own pattern, which matches itself) and 1 in `03` (prose naming ScreenScraper's developer-password field). The other 4 in each brief are the packet's copies of the slice's own files: `03`'s line, `fork-workflow.md` § Safety net's prose, `pre-push:196`'s comment, and `secret-patterns:8`'s pattern.
  - **None is a credential value.** The guard's own scan (`SECRET_PATTERNS`, `grep -a -c -E`) over every file of the folder gives 0, and `forbidden-terms-check --stdin` gives 0 hits.
  - **Fixed:** the two hits in this lane's prose were reworded (this line and `03:7`).
  - **Left as sent:** the briefs' 8 are the exact bytes sent to the seats and hashed in the manifest. So criterion 10's literal grep cannot print 0 while the packet holds the slice's own hooks. That is a question for the coordinator, put on #657.

### [Stage D] 17:44-17:50 — The coordinator's 17:44 ruling; the bugs; the punch list; the audit issue

- **The coordinator's post on #657 at 17:44 UTC:**
  - criterion 10 reads the guards' own scans over the folder, and the briefs stay (now quoted in `02` § Phase 2, row 10);
  - read F-42's intent before filing it;
  - name the `rev-list` fix in F-36's bug;
  - keep constructed inputs as recipes, never bytes.
- **F-42's intent:** `git log -S'--force' -- tools/fork-worktree` names one commit, `bcf03f7338` (2026-08-26), the tool's first. Its `:111` already forced unconditionally. Its message names only the build-output and cwd refusals and says `--force` means *destroy it anyway, having been told*. It is registered as blindspot 15, a `--force` applied uniformly. No reason is recorded for overriding git's own refusal, so F-42 is filed as a bug, with this trace in its body.
- **F-36's bug names its fix:** scan the exclusion set `"$local_sha" "${history_excludes[@]}"` directly, as the `whole=1` path does, with no `oldest^` boundary.
- **29 `bug` issues, #929 to #957,** in milestone M6, their bodies generated by `.qa-scratch/t10/bugs.py`. Each was scanned before filing: 0 listed words and 0 credential-pattern lines each. All 29 bodies, labels and milestones read back equal to their files. `tools/box-check --issue N` gives 0 failures of 29.
- **`05-punch-list.md`:** 44 items (PL-nn for F-nn), 6 High, 25 Medium, 13 Low, with its YAML index and a pre-issue gate of `Open` rows, written by `tools/t10-punch.py` from `02`'s headings, `tools/t10-grades.json` and the bugs.
  - 38 items are tracked by the 29 bugs.
  - PL-16 and PL-30 are the coordinator's leads; PL-31 and PL-34 Renovation items; PL-32 #640's; PL-33 the build-engine area's and #585's.
- **A parser slip, caught by the generator's own assertion:** a non-greedy `re.S` heading match let F-32 swallow F-33 (43 of 44). Fixed by reading headings one line each.
- `tools/lint-audit-artifacts <folder> --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.
- **The audit issue #958:** `Audit: M6 T10 the guards -- 44 findings (0 critical, 6 high)`, labels `audit` and `punch-list`, milestone M6, 44 checkboxes, attached as a sub-issue of #657 (`sub_issues` lists 958).
  - Its body's *track 38 of them* was first typed and then counted (38) before filing.
  - `box-check --issue 958`: 44 open checkboxes, 0 fail. The lint with `--issue 958` passes.
- **The stage-D pause starts here:** the coordinator writes the stream briefs (stage E).

### [Stage E] 18:01-18:08 — S1: the diff reader (#929, #930, #931, #937, #938)

- **The stage-E dispatch** (#657, 18:01 UTC) was read, and the brief `docs/reviews/briefs/t10-streams.md` at `9e0718eeb5` read whole (491 lines) from the coordinator's worktree. There are ten streams, run S1 to S10. Criterion 15 now reads over the 31 member paths.
- **The tests first:** five new `hooks-test` cases were added and run on the unfixed hooks (`.qa-scratch/t10/s1/before.txt`). All five failed:
  - *a listed word in a file git treats as binary (#929): expected refused, exited 0*;
  - *... in a .po file (#930)*, exited 0;
  - *an added '++ b/' line after a deleted '-- ' line is content, not a header (#931)*, exited 0;
  - *a # line carrying a listed word, given with git commit -m, is refused (#938)*, exited 0;
  - *... binary-detected file in a middle commit, gone at the tip (#929)*, exited 0;
  - *a pr/\* branch adding a personal path git quotes (#937)*: refused, but its `says ... "personal artifacts"` check FAILED.
- **The fix:**
  - **the reader:** `guard_added_lines` reads a header only between `diff --git` and the first `@@`, and a `Binary files` line refuses;
  - **the callers:** they diff with `--text --no-ext-diff --no-textconv`, with no `.po`/`.pot` exemption, and the tip names use `--diff-filter=AMT`;
  - **the name lists:** every one in `pre-push` is read `-z`, the personal-path match through an associative array;
  - **`commit-msg`:** it scans every line. The existing case that allowed a listed word on a `#` line now carries a clean one, as the brief's decision directs.
- **The commits:**
  - `a00b0ac7bb` (the reader, #929, #930, #931) was cut from an intermediate tree with the `-z`, `commit-msg` and two cases withheld: `hooks-test` PASS, 33 `expect` results;
  - `d55d34d6e1` (#937, #938) was committed on the final tree: PASS, **35 `expect` results, 51 `ok` lines** (stage A: 29 and 41).

  `mapfile`'s refusal path was checked under `set -u`: a failing diff leaves `rc=1` as the last element, and an empty diff `rc=0`.
- **Not this lane's:** the EmulationStation fork's `.githooks/guard-lib`, which carries the same reader (its header: *change both together*). It is named for the coordinator; that repository is outside this lane.
PROOF: P17 S1's cases -- `.githooks/hooks-test` with the five new cases on the unfixed hooks: rc 1, the five named FAIL lines (`.qa-scratch/t10/s1/before.txt`); on the intermediate tree (`a00b0ac7bb`): rc 0, PASS, 33 expect results; on the final tree (`d55d34d6e1`): rc 0, PASS, 35 expect results, 51 ok lines (`.qa-scratch/t10/s1/final.txt`).
PROOF: P18 S1's history read -- `docs/audits/2026_10_24-epic-m6-tooling-guards/tools/t10-history-scan.sh <worktree> c445081a59..8ebaf8daad /workspace/tmp/m6-t10/history-s1` (18:05:07Z, rc 0, 14 s), the fixed reader with the real lists through `guard_load`, counts and labels only: 27,038,430 added lines and 32,333 message lines; added lines 3 credential-shaped and 77 with a listed word, messages 1 and 3. Every commit carrying a hit predates the guard that would have refused it: the 77 word lines and 3 word messages are in 13 commits dated 2026-08-19 to 2026-09-28T13:58Z, before the wordlist guard `3e70ef9239` (2026-09-28T15:44Z); the credential lines are `9c9305eabf` (2026-08-22, before any scan) and two audit-packet seat diffs of 2026-09-28 (04:25Z, 13:58Z) committed under the audit-packet exemption that `3e70ef9239` removed; the credential message `06846da9ef` (2026-09-28T02:36Z) predates any message scan. No hit is a guard escape. The labels (commit:path:line) are in /workspace/tmp/m6-t10/history-s1/ and in `02` § Stage E for the coordinator.

### [Stage E] 18:14 — S2: the range, the base, tags, one redaction (#932, #937, #933, #934; D-WORKFLOW-200)

- **The tests first:** four new `hooks-test` cases on the S1-fixed, S2-unfixed hooks (`.qa-scratch/t10/s2/before.txt`), all failing:
  - *a listed word in a parent dated after its child, on a new branch (#932)*: exited 0;
  - *a pr/\* push with no upstream/next is refused (#937)*: exited 0, and *the fetch is named* FAILED;
  - *an annotated tag whose annotation carries a listed word (#933)*: exited 0;
  - *a line carrying a credential shape and a listed word (#934)*: refused, but its `silent` check FAILED (the word was printed).
- **The fix** (`32cb3a903e`):
  - a new branch's set is `"$local_sha" --not --remotes=<remote>`, read whole with `--topo-order`; the tip scan takes the files the set touches that are still at the tip;
  - `base_ref` is `upstream/next` only, and a `pr/*` push without it is refused with the fetch named;
  - a tag object's message joins the messages;
  - `guard_scan`'s redaction prints a line that also carries a listed word as its label and `[REDACTED]`.

  The last lives in `guard-lib`, which all three hooks share, so the stream touched it beside the brief's two files; the commit says so. `hooks-test` PASS, **39 `expect` results**.
- **`db8ad3958a`:**
  - `if true; then` removed and its body dedented. It was left by `d52e3d81c7` (audit #258) when `if [ -x ... ]` moved up as a refusal, so the condition is checked above it.
  - `'tools/fork-newdrive'` out of `PERSONAL_PATTERNS` (D-INFRA-030).

  `hooks-test` PASS, 39. The gate path itself (a push to `next`) is not exercised by `hooks-test`; `bash -n` passes.
- **A method check:** `git log --name-only -z --format=` emits pure NUL-separated names with no newline between commits (a scratch repository under `.qa-scratch/t10/s2/`), so the first cut's `tr '\n' '\0'` was dropped before commit; it would have split a name holding a newline.
- **Already written (tags):**
  - **The first attempt was refused** by the harness's safety check: an `rm` inside a `bash -c` script. Nothing ran.
  - **Re-run with no removal and no file:** `git ls-remote --tags origin` lists 7 tags. They were fetched into a throwaway namespace (`refs/t10-origin-tags/*`) and **all 7 are lightweight** (0 annotated), so there are 0 annotation lines and 0 hits. The namespace was then deleted ref by ref, 0 left.
  - **A delta:** the brief expected 0 tags; there are 7, none annotated.
PROOF: P19 S2's cases -- `.githooks/hooks-test` with the four new cases on the hooks before `32cb3a903e`: rc 1, five FAIL lines (`.qa-scratch/t10/s2/before.txt`); at `32cb3a903e` and at `db8ad3958a`: rc 0, PASS, 39 expect results (`.qa-scratch/t10/s2/after.txt`, `after2.txt`); origin's 7 tags, 0 annotated, 0 annotation lines scanned (counts through `guard_load`'s real lists).

### [Stage E] 18:21 — S3: two credential shapes; a listed word in a file name (#935, #936)

- **The coordinator's posts:**
  - 18:16 UTC: S1 and S2 accepted; the header example at `pre-push:44-46` to be aligned (done in S3's commit); the history finding with the maintainer on #312; the ES fork's `guard-lib` is #961.
  - 18:18 UTC: S5 gains the streamed sha256 loop for `ceremony-check:113`.
- **The measure before the widening:** a first form (any of `pass`, `secret`, `token`, `api_key`, separator `:` or `=`) matched **205** tree lines in 190 files, mostly a `pass:` label with a 16-character hash-like value. It was narrowed to the brief's scope: `[Pp]ass(word|wd)?` with `=`, a value of 16 or more characters, ending at a quote, a space or the line's end.
- **Two slips:**
  - an intermediate measure dropped the length floor (31 lines) and was re-run;
  - the first edit wrote the quote class as `[""'"'"]`, so the list no longer parsed as shell. Every hook then refused everything (`guard_load` failing closed, 13 FAIL lines in `hooks-test`), and it was corrected to the file's own `["'"'"']`.
- **The tests first:** five new cases on the S2 hooks (`.qa-scratch/t10/s3/before.txt`). The four that must refuse failed: the lowercase assignment, the slash-bearing refresh token, and a listed word in a file name at commit and at push. The control (a placeholder, a prose sentence, a short value) was allowed before and after.
- **The fix** (`148cee2a31`):
  - **The two shapes:** `secret-patterns` gains the lowercase assignment and `/` in the JSON token value; 19 alternatives, and `grep -E` compiles them (rc 1 on empty input).
  - **The name scan:** `guard_scan_names` judges added path names against the wordlist and refuses with a count, never a name; the pre-commit and all three `pre-push` paths call it.
  - **The coordinator's hunk:** the header example now carries S2's refusal text.

  `hooks-test` PASS, **44 `expect` results**.
- **Already written:**
  - **Today's tree:** the old list matches 0 lines and the widened one **10** (path:line in `02` § Stage E S3, posted on #935). Among them are 4 `rclone.conf.saved` files under `docs/qa-logs/`, each holding a `pass =` value of 36 mixed characters, the shape rclone writes for an obscured password, and two fixture literals in live tools.
  - **History, widened:** credential-shaped added lines rise from 3 to **15**, every one a lowercase assignment the old list could not match.
  - **Names:** 0 of the 126,890 distinct paths ever added carry a listed word.
PROOF: P20 S3's cases and reads -- `.githooks/hooks-test` on the S2 hooks with S3's cases: rc 1, four FAIL lines (`.qa-scratch/t10/s3/before.txt`); at `148cee2a31`: rc 0, PASS, 44 expect results (`after.txt`); `git grep -I -c -E` over the tree with the hash's list 0 lines, with the widened list 10 (`/workspace/tmp/m6-t10/s3-new-tree-hits.txt`); `t10-history-scan.sh` with the widened list: 15 credential-shaped added lines (was 3), 77 listed-word lines, messages 1 and 3; `git log --name-only -z --diff-filter=AC c445081a59..8ebaf8daad`: 126,890 distinct paths, 0 carrying a listed word (counted through `guard_load`'s list).

### [Stage E] 18:27 — S4: fork-worktree (#939, #940; D-WORKFLOW-201)

- **The coordinator's post at 18:24 UTC:** S3 accepted; its ten tree lines are bug #962 and the history count is with the maintainer on #312, neither this lane's.
- **How the tool finds its repository, read first:** `ROOT` comes from the tool's own location (`$0/..`), but `remove` and `repair` called `git worktree` in the caller's directory. A copy placed in a throwaway repository's `tools/` resolves to that repository, so the control needs no change to the resolution. The fix also points those two calls at `-C "${ROOT}"`.
- **A git fact, checked in a throwaway** (git 2.53.0): `git worktree remove` without `--force` removes a worktree holding only ignored files (a gitignored `build.x` deleted silently), and refuses one with an untracked file or a tracked edit (rc 128). So under D-WORKFLOW-201 an ordinary worktree still removes, and the tool's build-output refusal must still run first.
- **The control first:** `tools/fork-worktree-test`, 19 cases, run on the tool at `8ebaf8daad` (`.qa-scratch/t10/s4/before.txt`). The positives FAILED:
  - the uncommitted edit was destroyed (rc 0);
  - `--preserve` to an unwritable directory removed the worktree;
  - the bare `--preserve` looped until the timeout (rc 124);
  - repair lost a file three levels deep and a `..dotted` name;
  - sync exited 0 with a skipped worktree.

  Later FAILs cascade from those (the worktree already gone). Every case runs with the current directory inside the throwaway's `main/`, so a refusal is the tool's and not a `cd`'s.
- **The fixes:**
  - `4b8419002d` (remove forces only on `--force`; `--preserve` checks each move, refuses a destination inside the worktree and an existing name; `pwd -P`), cut from an intermediate tree. `hooks-test` PASS there; the control's remove cases passed, its four remaining FAILs being commit 2's.
  - `0c0be666eb` (repair's recursive carry, keeping the orphan when anything cannot be carried; sync's rc; the usage error), with the control: **19 of 19 ok, PASS**.
  - `d0c88f4528` (the three lists).
- **`rules-check` fails on this branch, since S2's `db8ad3958a`:** *hook missing tools/fork-newdrive*. S2 removed the hook pattern (D-INFRA-030), and the `fork-workflow.md` entry and index row remain. On T9's branch (`bf4445a13c`) the index row reads *this row leaves with the hook's pattern (#657)*, and T9 keeps all three. So the two rule entries' removal belongs with S2's, a rule edit S2's brief did not name. The question is on #657.

  This is my miss: `rules-check` was not run after S2. Every later stream now runs it.
- `worktrees.md` § Removing a worktree, read against the fixed tool: its sentences hold (*refuses if build output is present*, *`--force` only after it has told you what dies*). Left unchanged.
PROOF: P21 S4's control -- `tools/fork-worktree-test <the tool at 8ebaf8daad> .qa-scratch/t10/s4`: rc 1, the positives FAIL (`.qa-scratch/t10/s4/before.txt`); on the intermediate tool of `4b8419002d`: rc 1 with only repair, sync and the bare-`--preserve` cases failing (`inter.txt`), `hooks-test` PASS; `tools/fork-worktree-test` at `0c0be666eb`: rc 0, 19 ok, PASS (`final.txt`); the throwaway repositories under `.qa-scratch/t10/s4/`, never the fork's.

### [Stage E] 18:34 — S2 follow-up; S5: the tracker readers (#941, #943)

- **A slip, corrected:** S4's checkpoint said `register-check` passed. The sentence was written in the same command as the check, which printed `FAILED`: `MISSING D-WORKFLOW-201` at `tools/fork-worktree:219` and `tools/fork-worktree-test:3`. D-WORKFLOW-200 to 202 are rows on the coordinator's branch, and `register-check` reads `tools/` (not `.githooks/`). The comment was corrected in place at 18:28:31Z, with the correction visible; a friction line records it.
- **The coordinator's 18:30 UTC post:**
  - (1) S2's follow-up removes the `fork-newdrive` list item and index row here. Done in `9f6c9b56f9`, after which `rules-check` exits 0.
  - (2) The D-WORKFLOW-200/201/202 citations stay, since the coordinator merges its branch in at hand-back before criterion 17's checkers run. `register-check` reports the two MISSING lines until then.
  - (3) My `--force` reading is the documented contract, and the brief is corrected at `cc46c1112a`.
- **S5, the tests first:**
  - `docs/qa-logs/2026-10-24-box-check/run.sh`, 4 cases through `gh-double`. All four FAILED on the unfixed tool: it read 300 of 458, passed with the failing checkbox at 350 unseen (rc 0), accepted 458 against a total of 473, and exited 1 on a failing tracker.
  - `docs/qa-logs/2026-10-24-ceremony-check-tracker/run.py`, 11 cases. On the unfixed tool, 9 FAILED: the `"false"` receipt and the `* [ ]` body accepted, no streamed digest helper, the 2099 futro and *skipped the futro* setting the clock, the hygiene line `ok` over 200 of 250, over a short read and over a failing tracker, and futro and hygiene not counted overdue.
- **The fixes:**
  - `66b08a6672` (`box-check`): reads with a ceiling of 1,000 against `totalCount` before and after; exit 2 on a short or failed read. **4/4.**
  - `811e7f7d2f` (`ceremony-check`):
    - `gh_all` for the four reads, with a failed `gh` counted;
    - the receipt typed `is True`, and `[-*+] [ ]` counted;
    - an `Audit:` issue needs the `audit` label;
    - `FUTRO_MARKER` anchored; markers after today ignored, with `last_marker` taking main's `today`;
    - `--no-gh` skips `box-check`;
    - `file_sha256` streamed (the coordinator's 18:18 hunk).

    **11/11.** The friction reader is untouched (#905's packet).
- **The live runs** (18:33:32Z to 18:33:53Z; core 4,981 → 4,981, GraphQL 4,907 → 4,897):
  - `box-check --quiet`: rc 0, `507 issue(s), 1568 open checkbox(es), 0 fail` (300 before the fix). **No newly visible failing checkbox**, so there is nothing to list for the coordinator.
  - `ceremony-check`: rc 1 on W42 (M7's) and `register` (the recorded MISSING). Hygiene read every closed-completed issue since 2026-09-21: none with an open checkbox.
- **The open count moved during the slice:** 458 (16:29Z), 473 (16:47Z), 507 (18:33Z).
PROOF: P22 S5's controls and live runs -- `docs/qa-logs/2026-10-24-box-check/run.sh`: the unfixed tool 4 FAIL, the fixed 4 ok PASS; `docs/qa-logs/2026-10-24-ceremony-check-tracker/run.py`: the unfixed tool 9 FAIL of 11, the fixed 11 ok PASS (`.qa-scratch/t10/s5/`); live at 18:33Z: `box-check --quiet` rc 0, 507 issues, 1568 open checkboxes, 0 fail; `ceremony-check` rc 1 on W42 and the recorded register MISSING, hygiene ok over the full read; budget core 4,981 to 4,981, GraphQL 4,907 to 4,897.

### [Stage E] 18:39 — S6: forbidden-terms-check (#942, #936)

- **The test first:** `docs/qa-logs/2026-10-24-forbidden-terms/run.sh`, 8 cases, a stand-in list in `FORBIDDEN_PATTERNS`, throwaway trees under `.qa-scratch/t10/s6/`. On the unfixed tool five FAILED:
  - a clean tree with a symlink read 1 of 2 files;
  - a word in a symlink's link text was missed (rc 0);
  - a word in a file's name was missed (rc 0);
  - a checkout with its tracked files absent exited 0;
  - a tree with nothing tracked exited 0.

  The two silence checks and `--stdin` passed before and after.
- **The fix** (`34f32b28e6`): every tracked path is read.
  - **What is read:** the link text and the in-tree target of a symlink, a gitlink by name, and every name once.
  - **How a hit prints:** `path:line`, or `ls-files:<n>` where the path's own name carries a word.
  - **The count:** read must equal listed, and nothing tracked is exit 2.

  The first cut ran two extra `grep`s per file; before commit they became an associative array and a label computed only on a hit. **8/8.**
- **The real run** over this worktree, with the real list read by the tool alone: rc 0, **`0 hits in 133619 tracked files`**, equal to `git ls-files | wc -l` (133,619), in 149 s (147 s at stage A). So the 180 symlinks and every name carry no listed word, and the stream did not stop.
PROOF: P23 S6's control and real run -- `docs/qa-logs/2026-10-24-forbidden-terms/run.sh`: the unfixed tool 5 FAIL of 8, the fixed 8 ok PASS (`.qa-scratch/t10/s6/`); the fixed `tools/forbidden-terms-check` over the worktree with the real list: rc 0, 0 hits in 133619 tracked files, `git ls-files | wc -l` 133619, 149 s.

### [Stage E] 18:44 — S7: the lint's boundary; the folder date (#945)

- **The tests first:**
  - `tools/test-fixtures/lint-audit-artifacts/run.sh`, 5 cases. On the lint before the fix, the boundary fixture passed (rc 0) and the hyphen-dated copy without a review plan passed (rc 0); the pass and fail fixtures and the underscore copy already behaved.
  - `docs/qa-logs/2026-10-24-ceremony-check-tracker/run.py` gained three folder-date cases, which FAILED on the tool before the fix (no helper).
- **The fix** (`2444828e89`):
  - **the boundary:** `^## Findings index` and `^## Verification` found at the start of a line;
  - **the folder dates:** the lint's `(\d{4})([-_])(\d\d)\2(\d\d)-` gives two plain values, `dated` and `tier`, after a first cut that faked `match.group` with a lambda was replaced before commit, as unreadable;
  - **`ceremony-check`:** `audit_folder_date`, the same two forms, with future dates ignored;
  - **the hyphen form** is accepted, not dropped.

  Lint fixtures **5/5**; `ceremony-check` control **14/14**; `hooks-test` and `rules-check` rc 0 after.
- **The 2026-09-28 fix-round folder** under the fixed lint requires **14** seat-and-number pairs, against 11, and has all 14. Its one failure, *PL-029 outcome is not one of Resolved/Deferred/Withdrawn*, is the same under the lint at the hash and at the previous tip: a coordinator's item.
PROOF: P24 S7's controls -- `tools/test-fixtures/lint-audit-artifacts/run.sh` on the lint before `2444828e89`: 2 FAIL of 5 (`.qa-scratch/t10/s7/before.txt`), at it 5 ok PASS (`after.txt`); `run.py`'s three folder-date cases FAIL before, 14 of 14 ok after (`cc-after.txt`); the 2026-09-28 fix-round folder: 14 seat-and-number pairs required and present (11 before), the PL-029 failure the same under the lint at `8ebaf8daad` (`fixround-hash.txt`).

### [Stage E] 18:47 — S8: fork-package-freshness (#946)

- **The coordinator's 18:46 UTC post:** S5 to S7 accepted; the 2026-09-28 folder's PL-029 outcome is recorded as a historical fact, not rewritten.
- **The test first:** `docs/qa-logs/2026-10-24-package-freshness/run.sh`, a throwaway repository with a known merge base. On the unfixed tool:
  - the set was **`b f`**, upstream's deletion counted in and the shared addition `g` out;
  - a missing base ref exited **0**.

  The third case (a missing ref without `--list`) exited 2 unfixed too, but because the fixture has no `rclone` recipe, not because of the ref, so it is no positive and is recorded as such.
- **The fix** (`917f91677b`):
  - the set is `git diff --diff-filter=A <merge-base> HEAD`, with `HEAD` as the default head;
  - an unresolved ref, no merge base, or a failed diff exits 2 before any network read;
  - the header describes the set it now reads.

  **3/3.** The real `--list` is **26 rows, identical** to stage B's merge-base list (P14).
- **The real run** (18:46:27Z to 18:46:49Z, core 4,967 → 4,959): rc 1. The verdicts: 10 CURRENT, 4 INHERITED (`gstreamer` among them), 1 LOCAL, 6 PINNED, and BEHIND for `brotli` (1.2.0 → 1.2.1), `ruby` (3.3.12 → 3.3.13), `glib-networking` (2.90.0 → 2.90.1), `webkitgtk` (2.54.1 → 2.54.2) and `raofflineproxy` (15 commits behind `45726b18c6`).
- **Against `docs/releases/rc-accept.txt`:** six package acceptances still match PINNED rows. `zip` and `spirv-headers` are accepted there but are **not in the fixed set**: `spirv-headers` was counted only because upstream deleted it, and `zip` is not a fork addition since the merge base.
PROOF: P25 S8's control and runs -- `docs/qa-logs/2026-10-24-package-freshness/run.sh`: the unfixed tool's set `b f`, a missing ref rc 0 (2 FAIL); fixed: `f g`, rc 2, 3 ok PASS (`.qa-scratch/t10/s8/`); the real `--list`: 26 rows, `cmp` equal to stage B's merge-base list; the real run rc 1, five BEHIND rows (/workspace/tmp/m6-t10/s8-real.txt).

### [Stage E] 19:20 — S9: the record checkers (#947 to #957)

- **The coordinator's posts:** 18:49 UTC, S8 accepted and its freshness findings Backlog #963; 18:56 UTC, S9's first three accepted and the twelve SHAPE rows the coordinator's, fixed on its branch and merged into this one at hand-back.
- **The tests first:** one control per tool, under `docs/qa-logs/2026-10-24-record-checkers/` (`rc-preflight`'s under `docs/qa-logs/2026-10-02-candidate-preflight/`). Each runs against the tool copied into a throwaway root under `.qa-scratch/t10/s9/`, or imported with its tracker stubbed. Run against the tool as it stood before its fix commit:

  | Tool (bug) | Unfixed | Fixed |
  | --- | --- | --- |
  | `register-check` (#947) | 5 FAIL of 6 | 6 ok |
  | `work-log-index` (#949) | 3 FAIL of 5 | 5 ok |
  | `rules-check` (#948) | 3 FAIL of 3 | 3 ok |
  | `archaeology` (#950) | 4 FAIL of 6 | 6 ok |
  | `es-menu-map-check` (#951) | 2 FAIL of 3 | 3 ok |
  | `vocabulary-check` (#952) | 3 FAIL of 4 | 4 ok |
  | `prose-check` (#953) | 4 FAIL of 5 | 5 ok |
  | `release-catalog` (#954) | 6 FAIL of 6 | 6 ok |
  | `pr-stack-check` (#955) | 5 FAIL of 5 | 5 ok |
  | `rc-preflight` (#956) | 6 FAIL of 10 | 10 ok |
  | `renovation-inventory` (#957) | 3 FAIL of 5 | 5 ok |
  | `renovation-drift` and `-status` (#957) | 8 FAIL of 9 | 9 ok |

  All twelve controls together, on the fixed tools: 67 cases, PASS (`/workspace/tmp/m6-t10/s9-controls.txt`).
- **The fixes:** one commit per tool, `4228bf4daa` to `4acaf55ceb`, plus the reviews README (`d78f422212`); `02` § S9 has each.
- **Corrected before it stood:**
  - `rc-preflight`'s first cut of the one trace reader missed a trace written on its heading's own line. Over the tracker's 294 listed bugs it disagreed with the old reader on 10 closed ones (#305, #306, #315, #325, #529, #548 to #552). After the fix the two agree on all 294, and the control carries the case.
  - The drift and status control expected shares counted in changed lines; drift counts added plus deleted lines. Its expectations were corrected to the tool's documented arithmetic.
  - A check added to that control could not fail (`|| true`). It was replaced by an assertion on drift's own output before the commit.
  - `py_compile` and `renovation-status`'s module loader wrote `tools/__pycache__/` (gitignored). The files were removed by name.
- **The real runs:**
  - `register-check`: MISSING 2, SHAPE 12, EDITED 42, rc 1. Unchanged; the coordinator's.
  - `work-log-index`: `INDEX.md` +21 lines.
  - `rules-check`: 31 Detail-in pairs, notes.
  - `es-menu-map-check`: 21 computed-title pages under `guis/`, exit 0.
  - `vocabulary-check`: 10 scripts, 164 strings judged (the old list 163), 0 wrong.
  - `prose-check`: over the 35 tracked release and upstream pages, 53 fails before and after; 25 new same-word warnings.
  - `release-catalog`: two rows changed (`h700-rc-20260920-77e7e97515`'s BUILD_ID, `h700-all-20260924-a84fce38a6`'s Superseded); 395 kept folders without a RECORD.txt.
  - `rc-preflight`, offline: 9 acceptances, 4 rows that do not name their item.
  - `renovation-drift`: no slice issue closed.
  - `renovation-status`: fixed 11, reading 1, unreviewed 34 (45 unreviewed before).
  - API budget read first: core 4,932 of 5,000 before the tracker reads.
- **After the stream:** `hooks-test` PASS, `rules-check` rc 0, `register-check` rc 1 as recorded.
PROOF: P26 S9's controls and runs -- the twelve controls under `docs/qa-logs/2026-10-24-record-checkers/` and `docs/qa-logs/2026-10-02-candidate-preflight/rc-preflight-t10.py`: each fails on its tool before the fix commit (52 FAIL of 67 cases in all) and passes at it (67 ok, `/workspace/tmp/m6-t10/s9-controls.txt`); the real runs above (`/workspace/tmp/m6-t10/s9-*.txt`).

### [Stage E] 19:24 — S10: the fork CI (#944, #913, PL-31)

- **The fix:**
  - `fork-checks.yml` (`f4381c3501`): `if: always()` on all eight check steps (the checkout and the upstream fetch keep the default). The three watcher controls join the lifecycle step: `test-progress.py .`, `test-watch-build.py` and `test-submit.py`.
  - `fork-mirror-build-container.yml` (`22f9ae0d5e`): the token and the actor pass through `env:` (`REGISTRY_TOKEN`, `REGISTRY_USER`), and the token reaches skopeo on stdin through `printf '%s'`.
- **The test:** both files parse (`yaml.safe_load`: 10 and 3 steps), and each step's `if` was read back. Across the four `fork-*` workflows, 0 steps carry an expression inside `run:` (1 before, the mirror's sign-in).
- **Not run:** no `gh workflow run`. The three controls were not run on this branch, since their fixed bodies arrive with T9's merge. Whether the first red run on `next` shows every step's conclusion is the coordinator's read (`fix-pending-ci`).
- **After the stream:**
  - `hooks-test` PASS, 67 ok lines (`/workspace/tmp/m6-t10/s10-hooks.txt`);
  - `rules-check --quiet` rc 0;
  - `register-check` rc 1, as recorded (MISSING 2, SHAPE 12).
PROOF: P27 S10's parse and read-back -- `yaml.safe_load` on `.github/workflows/fork-checks.yml` (10 steps, `always()` on the eight check steps) and `fork-mirror-build-container.yml` (3 steps); the expression-in-run scan over the four `fork-*` workflows, 0 after and 1 before; the diffs in `/workspace/tmp/m6-t10/s10-checks.diff` and `s10-mirror.diff`; the CI run itself fix-pending-ci.

### [Stage E] 19:28 — S10's follow-up and the close-out

- **The coordinator's posts:**
  - 19:25 UTC: S9 accepted. Both new `renovation-status` states stay (D-WORKFLOW-204); the docstring cites it at `38306d3123`. The four rc-accept rows are #963's. #964 and #965 take the catalog folders and the computed-title pages.
  - 19:27 UTC: S10 accepted, and `!cancelled()` in place of `always()` (D-WORKFLOW-205).
- **The follow-up (`f22b989ab1`):** `if: ${{ !cancelled() }}` on the eight check steps. Re-parsed (10 steps) and each condition read back. P27's text is updated to match.
- **The Phase 7 table and `punch_index` (`38eff70b01`):** 40 Resolved, each row with its commit and bug, and 4 Deferred: PL-16 to #959, PL-30 to #960, PL-32 to #640, PL-33 to #585. The lint on the folder at its default phase: PASS.

### [Stage H] 19:49 — accepted; the completion marker

- **The coordinator's post (19:47 UTC):** T10 accepted at `afdce9a65b` (this lane's tip with the coordinator's branch merged), every checker passing there; 16 of 17 criteria ticked, criterion 5's merge clause open until `next`; #958 closed as completed. The worktree was fast-forwarded to `afdce9a65b`.
- **The marker:** `audit-completion.json`, `tracker-completion.json` and `tracker-final-readback.json`, written by `tools/write-completion.py` (T3's writer, copied) from #958 read back closed/completed with 44 ticked and 0 open.
- **The checks:** the full `tools/lint-audit-artifacts` on the folder: PASS. `tools/ceremony-check` reports the audit line `ok` via #958; its one DUE is W42, the M7 lane's.
