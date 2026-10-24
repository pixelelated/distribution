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
