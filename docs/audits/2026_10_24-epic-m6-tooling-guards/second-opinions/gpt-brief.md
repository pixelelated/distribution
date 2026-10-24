# Second opinion on a code audit: M6.P2 T10, the guards (hooks, the fork CI and the checkers), epic tier

You are a second reader of a code audit at the end of its reading stage. You cannot run commands or open the repository. Everything you may cite is in the packet below, and every claim you make names the packet's `file:line` (the line numbers printed in each file) or the section it rests on. The first reader's verdicts are in its `02-forward-audit.md`, `03-retrospective.md` and `04-analysis.md`, reproduced whole below.

**The scope:** 31 files of a Linux distribution fork's own guards.
- **Three git hooks:** `pre-commit`, `commit-msg` and `pre-push`. They refuse a credential-shaped line (patterns in `.githooks/secret-patterns`) and any word from a wordlist that lives outside every tree (never in this packet).
- **Their shared library and suite:** `guard-lib` and `hooks-test`.
- **The four fork CI workflows.**
- **Two upstream release scripts.**
- **Nineteen checker tools:** a ceremony state machine, a decision-register lint, an audit-artifact lint, a worktree remover that must never destroy build output, a package-currency checker, an RC preflight, and others.

The first reader's main claims to test: **F-01** (binary files are never diff-scanned by the hooks) and **F-11** (`fork-worktree remove --preserve` destroys build output after a failed `mv`), both High; and the class of eleven findings where a checker reads less than it reports and passes (`03` § 3.3).

**Read these first, in this order:** `.githooks/pre-push`, `.githooks/guard-lib` and `.githooks/secret-patterns` (the two guards), then `tools/forbidden-terms-check` and `tools/fork-worktree`. Then the rest.

**Rules for your answer:**
- **Never reproduce a credential-shaped string.** The packet's fixtures build their values from `printf` pieces; describe a shape in words, never by writing a value.
- **The wordlist is not in the packet.** Do not guess at its contents.

Answer in three parts, in this order:

1. **Your own findings first.** List every defect, gap or unsafe seam in the 31 files that is not already one of the first reader's F-01 to F-34. Give each one line: an id (G-01, G-02, ...), a severity (Critical / High / Medium / Low), the `file:line`, the constructed input that shows it, and the wrong behaviour that results. Start with the two guards and the two tools named above.
2. **Refute the first reader.** For every High and Medium finding, and any Low you think mis-graded:
   - agree, disagree, re-grade or narrow;
   - in each case, say what would make the finding false and whether the packet shows it.

   Say also whether `04` § Q6's guard table misses a refusal the code wires, and whether § Q3's hunt missed a reader.
3. **What you could not judge.** The claims the packet does not let you verify, so the orchestrator knows where its evidence was thin.


# The packet


## The first reader's 02-forward-audit.md (whole)

# Forward audit — M6.P2 T10, the guards: hooks, the fork CI and the checkers (#657)

Written 2026-10-24 at stage B, from the read trees `.qa-scratch/t10/at-hash/` (`8ebaf8daad`, 28 files) and `.qa-scratch/t10/at-p1/` (`2174265e9c`, the three `renovation-*` tools). Line numbers are those trees' unless a finding says otherwise.

Every finding is a lead until `04` § Finding Verification and § Second opinion grade it; the punch list (`05`) takes them from there. A finding about the wordlist names a file and a line, never a word. A credential-shaped value appears nowhere in this folder: the constructed inputs were built from `printf` pieces at run time, and their outputs were never printed (`tools/t10-guard-gaps.sh`).

**A method note, recorded because it changed what a count means.** In this harness the interactive shell's `grep` is a shell function: it runs ugrep with `-I` (binary files skipped) and `--ignore-files` (gitignored paths skipped), so a count taken with it is not GNU grep's. The hooks and the tools run `/usr/bin/grep`, GNU grep 3.12 (`type grep`, `bash -c 'grep --version'`). Every count from here on is taken with `command grep`; the counts before it was noticed were re-taken. The one that differed was a regex the function would not compile (`exceeds complexity limits`). It was not a finding.

## Phase 2: #657's checklist at stage B

| # | Criterion (short) | State at stage B | Artifact |
| ---: | --- | --- | --- |
| 1 | the folder holds 00 to 05 | 00, 01 and 02 written; 03 and 04 next; 05 at stage D | this folder |
| 2 | the lint PASS (pre-issue before D, resolution at close) | not yet run | stage C to D |
| 3 | review-plan.json Extended; both seats' provenance; the packet manifest and its scan | not yet run | stage C |
| 4 | every punch item at a Phase 7 outcome | stage F | the audit issue |
| 5 | reviewed-at and fixed-at, both hashes named | `a82d784216` (stage A) | #657's body at hand-back |
| 6 | 01 § Scope: hashes, filter output, provenance, branch diff, after-hash deltas | **done** | `01-research-notes.md` § Scope |
| 7 | the coverage table, 31 rows, Q1 to Q7 answered | **done** | § Coverage below |
| 8 | § The suites, each with command, exit, summary, *a FAIL would mean* | **done** | § The suites |
| 9 | § The CI: runs, failing steps, 23 workflows, the secret inferred | **done** | § The CI |
| 10 | no push beyond the lane's branch, no forbidden run, no credential line, no listed word | so far: one push, the lane's own (`5611a4fb62`) | `00`; the folder's scan at stage C |
| 11 | 04 Q6: the guard table and the tool-caller table | the evidence is here (§ Callers, § The suites, F-rows); the tables are `04`'s | `04` § Q6 |
| 12 | 04 Q3: the fail-open hunt through the named readers | the evidence is here (F-01 to F-30); the table is `04`'s | `04` § Q3 |
| 13 | 04 Q7: the personal-path diff entry by entry; three descriptions per guard | P2 (the diff); the description rows are `04`'s | `04` § Q7 |
| 14 | proof cells in § Proofs = proof lines in 00 | 16 = 16 | § Proofs; `command grep -c` |
| 15 | every item `question:`; bugs pass box-check; no member edited before a stream | stage D; `git diff --stat a82d784216 HEAD -- .githooks .github tools` empty | `05` |
| 16 | the retro | stage G | `docs/retros/` |
| 17 | the six checks pass before the merge; the lint PASS | stage H | the hand-back |

## The suites

Every command was run in this worktree at stage A (16:28-16:31 UTC), with its output kept under `/workspace/tmp/m6-t10/baseline/`. The at-hash `hooks-test` was run from the export.

| Command | Exit | Summary | A FAIL would mean |
| --- | ---: | --- | --- |
| run `.githooks/hooks-test` (the worktree: the hash's hooks plus #696's marker refusal) | 0 | `PASS`, 41 `ok` lines: **29** `expect` results (refused/allowed) and 12 `says`/`silent` checks | a hook allowed a shape it exists to refuse, refused a clean one, or printed a value or a listed word |
| run `.qa-scratch/t10/at-hash/.githooks/hooks-test` (the hash; what the primary checkout runs today) | 0 | `PASS`, 38 `ok` lines: **27** `expect` results and 11 `says`/`silent` checks | the same, for the copy every lane's commits actually run |
| run `tools/register-check` | 0 | `667 IDs, each once; every citation in the live documents names a row` | a duplicate ID, a citation naming no row, a placeholder row, or a decided row under the open table |
| run `tools/rules-check --quiet` | 0 | (silent) | a rule without its front matter, an unindexed rule, a count in `CLAUDE.md`/`AGENTS.md` wrong, `AGENTS.md` over budget |
| run `tools/work-log-index --check` | 0 | `work-log index: current` | the index not regenerated after a log entry |
| run `tools/prose-check --self-test` | 0 | the maintainer's page passes; the machine draft fails (its last tell: *a closing summary or sign-off*); `self-test: PASS` | a tell no longer caught, or the reference page flagged |
| run `tools/ceremony-check` | 1 | `DUE weekly OVERDUE: 2026-W42 summary missing`, the other ten lines `ok` (W42 is the M7 lane's to pay) | any other line `DUE` |
| run `python3 -I tools/lint-audit-artifacts <P1>/fixture-epic-m6-renovation-pass` | 0 | `PASS` | the renovation face rejecting a folder that answers it |
| run `python3 -I tools/lint-audit-artifacts <P1>/fixture-epic-m6-renovation-fail` | 1 | `2 CONTRACT FAILURE(S)` (the face and `question:`, both at once: see F-08) | — this is the FAIL; a PASS would mean the face is not checked |
| run `tools/box-check --quiet` | 0 | `300 issue(s), 762 open checkbox(es), 0 fail` (core 4,976 → 4,976; GraphQL 4,999) | an open checkbox naming a person or a device without a fact — **among the 300 it read** (F-04) |
| run `tools/forbidden-terms-check` (the tree) | 0 | `0 hits in 133409 tracked files`, 147 s | a tracked file carrying a listed word — **outside the 180 symlinks it skips** (F-07) |
| run `tools/fork-worktree list` | 0 | read only; one worktree `HOLDS BUILD OUTPUT (2.6G)` | — (list has no failing verdict) |
| run `tools/{es-menu-map-check,rc-preflight,archaeology,pr-stack-check} --help` | 0 each | usage only; each parser read before the call | — |

**`ceremony-check` against #905's packet.** The #905 tool is not on this branch (`9e12014623` is not an ancestor). It was read as a diff (`git diff 8ebaf8daad 9e12014623 -- tools/ceremony-check`, +55/-9), not run from a detached checkout, because its friction line reads `docs/friction-log.md` from its own `ROOT`. Its own before/after fixture is the packet's evidence (`docs/qa-logs/2026-10-24-905-ceremony-friction/`, on that branch). The diff closes the shape the hash fails open on (`ceremony-check:250-252`: `if not m: continue`). It leaves the residual that F-15 names.

## The CI

Read through the API only (core 4,967 → 4,958), never re-triggered.

- **`fork-checks.yml` on `next`:** six runs, `failure`, from 2026-10-19T13:07Z to 2026-10-24T10:54Z. All are `schedule` runs at `8ebaf8daad`. The last success was 2026-10-18T11:00:07Z, and the last push-triggered run 2026-10-17T06:03Z.

  | Run | Created | Failing step | Later steps |
  | --- | --- | --- | --- |
  | 40087768497 | 10-24 10:54 | *ceremonies are not overdue* | — (last step) |
  | 39947006860 | 10-23 11:34 | *ceremonies are not overdue* | — |
  | 39773227474 | 10-22 11:47 | *every open acceptance checkbox is agent-verifiable (D-QA-044)* | *ceremonies are not overdue*: **skipped** |
  | 39594189379 | 10-21 11:44 | the same | **skipped** |
  | 39415615874 | 10-20 11:31 | the same | **skipped** |
  | 39257547676 | 10-19 13:07 | the same | **skipped** |

  The 10-24 run took 2 min 41 s; its 11 steps are listed in `00`. **On four of the six red days the ceremony check never ran** (F-06).
- **`fork-wordlist.yml`:** green on every branch push read, the lane's two of today among them. Its last run on `next` was 2026-10-17T06:03Z, a success.
- **The workflows GitHub lists:** 23, all `active` (`gh api repos/pixelelated/distribution/actions/workflows`). Four are the fork's (this slice's four files). The other 19 are upstream's (`build-*.yml`, `build-nightly.yml`, `validate-pull-request.yml`, `check-freeze-period.yml`, `update-mirror-sources.yml`, ...), the build-engine area's, upstream-carried.

  **One lead for the coordinator:** `build-nightly.yml`'s jobs that call the two `.github/scripts` are gated on `github.repository_owner == 'ROCKNIX'`, and its scheduled triggers on `ROCKNIX/distribution` (R3's read; `.github/workflows/build-nightly.yml:85,169,177,206,285`). Whether every scheduled upstream workflow is so gated on the fork is the build-engine area's question, named once here.
- **The secret:** `gh secret list` prints `failed` for this token. `FORBIDDEN_PATTERNS`'s existence is inferred from `fork-wordlist.yml`'s green runs: its header (`:4-5`) says the job is red without the secret. Its value was never read.

## Callers

Who runs each of the 31, read from the tree with `command grep` for each name in `.githooks/`, `.github/workflows/`, `.claude/rules/`, `.claude/skills/` and the other tools (R1 to R4's tables, re-read).

| File | Run by | Flags |
| --- | --- | --- |
| `pre-commit`, `commit-msg`, `pre-push` | git, through `core.hooksPath` (absolute, the primary checkout) | — |
| `guard-lib`, `secret-patterns` | sourced by the three hooks | — |
| `hooks-test` | nobody automatically: a rule's instruction (`fork-workflow.md` § Safety net, *run it after any change here*) | — |
| `fork-checks.yml` | GitHub: push of `next`, daily schedule, dispatch | `ceremony_today` |
| `fork-wordlist.yml` | GitHub: every branch push, dispatch | — |
| `fork-mirror-build-container.yml` | dispatch only | `source`, `tag` |
| `fork-generic-x64.yml` | dispatch only, and its one job is `if: ${{ false }}` | — |
| `generate-changelog.sh`, `generate-release-body.sh` | `build-nightly.yml:251,326`, gated to ROCKNIX: **never in this fork** | — |
| `archaeology` | rules only (`decision-register.md`, `ceremonies.md`) | — |
| `box-check` | `fork-checks.yml:54`, `ceremony-check:344`, `rc-preflight:389` | `--quiet` |
| `ceremony-check` | `fork-checks.yml:59`, `pre-push:338` (`--gate`), `rc-preflight:395,397` | `--gate` |
| `es-menu-map-check` | `vm-qa` (the `menumap` suite) | — |
| `forbidden-terms-check` | `fork-wordlist.yml:28,40` | `--stdin` |
| `fork-package-freshness` | `rc-preflight:171` | — |
| `fork-worktree` | rules (`worktrees.md`); `pr-stack-check`'s EXIT trap (`remove`) | `list`, `remove`, `repair`, `sync` |
| `lint-audit-artifacts` | `ceremony-check:374` (`--phase resolution` on a completed folder); the code-auditor skill | `--phase`, `--issue` |
| `pr-stack-check` | the release-notes skill | — |
| `prose-check` | the developer-relations and release-notes skills | `--self-test` |
| `rc-preflight` | rules only (`release-candidates.md`) | `--tree`, `--only`, `--allow-unchecked` |
| `register-check` | `fork-checks.yml:37`, `ceremony-check:306`, `vm-qa` | — |
| `release-catalog` | `rc-preflight:390` | `--check` |
| `rules-check` | `fork-checks.yml:39`, `ceremony-check:312` | `--quiet` |
| `vocabulary-check` | `vm-qa` (the `vocabulary` suite) | — |
| `work-log-index` | `fork-checks.yml:35`, `ceremony-check:300`; `pre-push:329` names it in a warning | `--check`, `--write` |
| `renovation-inventory` | nobody automatically: `docs/reviews/README.md`; imported by the other two | many |
| `renovation-drift` | `renovation-status:106` | `--pretend` |
| `renovation-status` | nobody automatically: `docs/reviews/README.md` | `--write` |

Nothing runs `hooks-test`, the lint's fixtures, `renovation-inventory --self-test` or `renovation-drift --self-test` automatically. Each guard's own proof waits on someone remembering it (`04` § Q6).

## Findings

The draft severities are this reader's, before `04` grades them. "Positive" names the constructed input that proves the shape (a `PROOF:` line in `00`) or the line read that shows it.

### The hooks and their library (the security list)

**F-01 — A file git treats as binary is never scanned in a diff: a credential or a listed word committed there passes the pre-commit, and the push guard too when it is gone again at the tip.** *Draft: High. Q3.*
- **Where:** `pre-commit:13` runs `git diff --cached -U0 ...` without `--text`. `pre-push:268,272` run `git log -p ...` without `--text`. For a binary file git prints `Binary files a/x and b/x differ` and no `+` lines, so `guard_added_lines` (`guard-lib:57-81`) sees nothing to judge and nothing unknown to refuse.
- **What still catches it:** the push guard's tip scan (`pre-push:299`, `git show | guard_numbered`, then `grep -a`) reads a binary file whole. So the gap is a value committed in one commit and removed inside the same push, plus the pre-commit's whole reason for existing: *"so the push guard never meets one in history"* (`pre-commit:2-3`).
- **Positive:** P1. pre-commit rc 0 on a NUL-bearing file with a credential and with a listed word; the text control rc 1. pre-push rc 0 on the binary middle commit; the text control rc 1.

**F-02 — `.po` and `.pot` files are exempt from every hook scan.** *Draft: Medium. Q3, Q7.*
- **Where:** `pre-commit:13` and `pre-push:267,268,271,272` all end in `':!*.po' ':!*.pot'`. A credential or a listed word in a translation catalog passes all three hooks. `fork-wordlist.yml`'s tree scan still finds a listed word there; nothing finds a credential.
- **Why it is a finding:** the exemption arrived with the first credential scan (`f51d081c04`, 2026-09-05), whose message gives no reason. It contradicts `guard-lib:20` (*no path is exempt*) and `fork-workflow.md` § Safety net (*no path is exempt*).
- **Positive:** P1. rc 0 at pre-commit and at the push tip for both shapes.

**F-03 — `commit-msg` drops every line beginning `#`, but `git commit -m` keeps them, so a listed word or a credential on such a line passes the hook and is refused only at push, after it is in history.** *Draft: Low. Q3.*
- **Where:** `commit-msg:11` (`grep -v -a -E '^#'`) assumes git's default cleanup strips comments. With `-m` git does not run the editor, its cleanup is `whitespace`, and `#` lines stay in the message. `hooks-test`'s case *a clean message (git drops the # comment)* constructs the editor path only.
- **What still catches it:** the push guard's message scan keeps every line (`pre-push:265`), so the cost is the rewrite the hook exists to avoid (`commit-msg:3-5`).
- **Positive:** P1. A real `git commit -m tidy -m "# ..."` with the hooks path set: rc 0, the stored message keeps the line, and the pushed branch is refused (rc 1).

**F-04 — `box-check` reads `--limit 300` of the fork's 458 open issues, prints `0 fail` and exits 0; the CI step and `ceremony-check`'s `checkboxes` line read the same truncated answer.** *Draft: Medium. Q3. The coordinator's ruling: a `bug`, filed at stage D.*
- **Where:** `box-check:83`. The open count was 458 at 16:29Z and 473 at 16:47Z, as other lanes filed. Nothing compares the count returned with the limit; `box-check:102` prints the count it got. The same tool also feeds `rc-preflight:389`.
- **Positive:** P4.

**F-05 — `ceremony-check`'s hygiene line reads `--limit 200` of the 331 issues closed as completed since 2026-09-21, and a `gh` failure in its futro or hygiene line is reported but never counted.** *Draft: Medium. Q3.*
- **Where:** `ceremony-check:423` (the limit) and `:402-403`, `:425-426`. `report(False, ...)` without `overdue.append`, so the run prints `DUE ... gh failed` and still exits 0 when nothing else is owed. The stage-A run's `hygiene ... no issue closed completed since 2026-09-21 carries an open checkbox` is a statement about 200 of 331.
- **Positive:** P5.

**F-06 — In `fork-checks.yml` a failing step skips every step after it, so a red day hides the verdicts it did not reach: on 2026-10-19 to 10-22 the ceremony check never ran.** *Draft: Medium. Q3, Q6.*
- **Where:** `fork-checks.yml:34-59`: eight steps with no `if: always()` and no final aggregation. The record says only *the first failure*, and the badge is red for whichever step failed first.
- **Positive:** P7 (§ The CI's table).

**F-07 — `forbidden-terms-check` skips every tracked symlink (180 in this tree) and never compares the count it scanned with the count it listed, so a checkout whose files are absent prints `0 hits in 0 tracked files` and exits 0.** *Draft: Medium. Q3. The coordinator's ruling: a `bug`, filed at stage D.*
- **Where:** `forbidden-terms-check:37` (`[ -f "${p}" ] && [ ! -L "${p}" ] || continue`) and `:46-50`. A symlink's target is a string in the repository and is pushed. The pre-commit sees it as a diff line; the CI's tree scan (`fork-wordlist.yml:28`) does not. The CI runs on a fresh full checkout, so the absent-file case is a sparse or partial checkout's, not the CI's today.
- **Positive:** P1 (1 hit of 2; `0 hits in 0 tracked files`, rc 0) and P6.

**F-10 — The push guard's personal-path match reads `git diff --name-only` as given, so a path git quotes (a non-ASCII name under `docs/`) is not matched. Today such a push is still refused, by the tip scan failing to read the quoted name.** *Draft: Low. Q3.*
- **Where:** `pre-push:395-409`, with `core.quotePath` unset; the tip scan at `:271,299` is what catches it.
- **Positive:** P1. Refused as *could not be read*; with `core.quotePath=false`, refused as *personal artifacts*. The defence is an accident of a second check.

**F-30 — The CI scans no credential shape: `fork-wordlist.yml` checks the wordlist only, so a credential pushed with `--no-verify`, or from a clone without the hooks path, reaches GitHub with only GitHub's own push protection between it and the history.** *Draft: Low. Q6. A contract question (D-WORKFLOW-061's CI half): a lead for the coordinator.*
- **Also:** a new branch's message scan reads its last fifty commits (`fork-wordlist.yml:36`).
- **Positive:** the tree. `fork-wordlist.yml:27-40`; `command grep -c SECRET .github/workflows/fork-*.yml` gives 0.

### `fork-worktree` (the one that can destroy build output)

**F-11 — `remove --preserve <dir>` ignores a failed `mv` and then force-removes the worktree, destroying the build output it was told to keep.** *Draft: High. Q3. D-WORKFLOW-005 is this tool's whole contract.*
- **Where:** `fork-worktree:190-201`. `mv ... && echo "preserved"` has no `||`; the loop goes on, and `git worktree remove --force` runs with the unmoved `build.*` still inside. The refusal at `:177` is skipped because `preserve` is set.
- **Input:** a preserve directory that exists but is not writable, or a cross-filesystem move that fails part-way (disk full).
- **Positive:** the tree, read. The fixture is the stream's: a scratch repository, a worktree holding `build.x`, and a read-only preserve directory. It is not run here, because `fork-worktree remove` is on § 8's list.

**F-12 — `repair` carries back only top-level entries that the fresh checkout does not have. Everything inside a tracked top-level directory (every untracked file under `docs/`, `tools/`, `projects/`) is then removed with `rm -rf "${orphan}"`.** *Draft: Medium. Q3.*
- **Where:** `fork-worktree:231-238`. The header and `worktrees.md` say it *carries every untracked file back*.
- **Positive:** the tree, read. The fixture is the stream's.

**F-13 — `remove <path> --preserve` with no directory loops forever.** *Draft: Low. Q3.*
- **Where:** `fork-worktree:160`. `shift 2` with one argument left fails without shifting.
- **Positive:** P11 (the same `while`/`case`/`shift 2` shape, lifted with a timeout: still looping after 100,001 passes, rc 3).

**F-14 — `sync` always returns 0, whatever it skipped or failed; its `rc` is never set.** *Draft: Low. Q2.*
- **Where:** `fork-worktree:255,300`. The loop also runs in a pipeline's subshell, so a set would not reach the return either.
- **Positive:** the tree.

### The record checkers

**F-15 — `ceremony-check`'s clocks can be reset or frozen by a marker that is not one.** *Draft: Low. Q3.*
- **The futro marker is unanchored.** `:405` uses `\bfutro\b`, where the retro's (`:229`) was anchored by audit #258 PL-004 for exactly this reason: a heading that says *skipped the futro* resets the clock.
- **A future-dated retro or audit folder freezes its clock** (`last_marker`, `:159-163`; the audit glob, `:363-367`).
- **The #905 diff's residual:** the lines under `## Entries` that are not entries are named, never owed.
- **Positive:** the tree and the #905 diff, read. R1's leads, re-derived at the lines named.

**F-16 — The push guard's ceremony gate judges the primary checkout's working tree, not the tree being pushed.** *Draft: Medium. Q3. A contract question (D-WORKFLOW-028, #258 PL-004): a lead for the coordinator.*
- **Where:** `pre-push:60,331,338` run `"$hooks_root/tools/ceremony-check" --gate`, whose `ROOT` is the primary checkout (`ceremony-check:51`).
- **Effect:** a push of `next` from a lane worktree carrying a new summary is judged by whether the primary checkout, still at the old `next`, has it. The audit chose the primary's tools so that a stale worktree could not skip the gate. It also moved what the gate reads.
- **Positive:** the tree.

**F-17 — `register-check` does not see the second ID of a slash shorthand, reads seven live documents that cite IDs nowhere, and has T4's three gaps.** *Draft: Medium. Q3, Q6.*
- **Slash shorthand:** `CITE='D-[A-Z]+-[0-9]+\b'` (`:32`), so `D-WORKFLOW-155/156`'s 156 is never looked up. It is written that way in `es-ui-style-guide.md`, `least-surprise.md`, `es-player-text.md` and `upgrade-and-install.md` (R1).
- **Documents outside `LIVE`** (`:46-59`): `docs/conflict-wizard-ia.md`, `NAMING.md`, `docs/releases/device-facts.md` and four others (R1's list).
- **T4's leads on #657:** the open table's header against its cells; an in-place edit of a decided row (D-RA-006 is the control: `git log -G'\| D-RA-006 \|'` shows its cell changed in `82880e51bd`, `c6241cf223` and `e5065e18ee`); unescaped pipes in decided rows.
- **Positive:** the tree and the history.

**F-18 — `rules-check`'s `mention` is a substring test, and it does not check that an index row's *Detail in* rule names the tool (T4's lead, 31 of 85 pairs at the hash).** *Draft: Low. Q3, Q6.*
- **Where:** `rules-check:231`, `f[:-3] not in t`. `worktrees` is satisfied by `../rocknix.worktrees/` in `CLAUDE.md`.
- **A delta from R1:** R1 also said the count sentence matches nothing in `AGENTS.md`. It matches 1 there as in `CLAUDE.md` (`command grep -c -i -E '\bAll ([0-9]+)( of them|,)'`), so that half is withdrawn.
- **Positive:** the tree.

**F-19 — `work-log-index` indexes only `## ` headings; the 14 `### HH:MM UTC` entries at the hash are in no index, and `--check` passes.** *Draft: Low. Q3.*
- **Where:** `work-log-index:40`. The 14 are in `2026_10_02` (1), `2026_10_14` (3) and `2026_10_15` (10). `ceremony-check`'s day reader has the same blindness, in the safe direction.
- **Positive:** P8.

**F-20 — `archaeology` never searches blindspots 1 to 29, which are table rows before the first `## N.` heading; a failed `git` or `grep` reads as zero hits, and the tool always exits 0.** *Draft: Medium. Q3. It is the tool the rules say to run before anything is called pending (blindspot 52).*
- **Where:** `archaeology:76-91` (`flush` needs a `## ` head), `:161`, `:228`, `:286`.
- **Positive:** P9. `archaeology --no-gh "busybox unzip"` prints `The blindspot register (0)`; the register carries it twice, in row 7.

**F-08 — `lint-audit-artifacts` bounds the seats' findings index with `str.find("## Verification")`, so a table cell quoting that heading ends the index early. In the 2026-09-28 fix-round audit, the cell at line 192 did, and every row from 192 to 881 (three High gpt findings among them) was never required to have a verification entry.** *Draft: Medium. Q3.*
- **More of the same shape:**
  - an indented YAML index is read as one entry (`:351` at the hash);
  - a folder with no `punch_index:` is passed with an `ok` at any date (`:349`);
  - the seat filter requires entries only for `claude` and `gpt` (`:189`);
  - `"Resolved" in cell` accepts *Not Resolved* (`:317`).
- **The fixtures:** the fail fixture fails two checks at once, so neither is proven alone, and nothing runs the fixtures automatically.
- **Positive:** P10, the record, read at the lines; plus R2's leads re-derived at `:182` and in the folder.

**F-21 — `es-menu-map-check` sees a settings page only when its title is a `_("...")` literal: 22 of the 75 `new GuiSettings(` calls at the ES pin `16dbac5211` pass a computed title and are never checked.** *Draft: Medium. Q3.*
- **Where:** `es-menu-map-check:50-56`. The fork's own pages are among them: `CONTENT TO BACK UP` / `CONTENT TO RESTORE`, `cloudSetupTitle(mode)`.
- **Positive:** P12.

**F-22 — `vocabulary-check` reads a hard-coded list of seven cloud scripts and `backuptool`.** *Draft: Low. Q3, Q7.*
- **Where:** `vocabulary-check:111`.
- **What it misses:** `cloud_scan`, `cloud_content_transfer`, `cloud_capture`, `cloud_oauth` and `cloud_sync_helper`, all in `rclone/sources/` and all printing player text. Its header says *every sentence the cloud scripts print*. It also reads only `es-app/src`.
- **Positive:** P13.

**F-23 — `prose-check`'s sign-off pattern cannot match a sign-off followed by a space or the line's end, and its repeated-opener check computes and then `pass`es.** *Draft: Low. Q3.*
- **Where:** `prose-check:29` (`overall,\b`, `that's it!\b`) and `:74-75`. Its self-test reads samples outside the tree (`/workspace/tmp/rocknix-session`).
- **Positive:** P10b. A draft ending *That's it!* passes (rc 0); the *Happy gaming!* control fails (rc 1).

**F-24 — `release-catalog` parses `KEY  value` with two or more spaces only, so a record written with one space loses its fields silently, and a kept folder with no `RECORD.txt` is reported nowhere.** *Draft: Low. Q3.*
- **Where:** `release-catalog:39,86`. The real case: `h700-rc-20260920-77e7e97515` (R2).
- **Positive:** the tree.

**F-25 — `pr-stack-check` claims a stack whose last head equals `next`; the code resets every PR to the base and never compares a final tree.** *Draft: Medium. Q3, Q7.*
- **The claim:** the header (`:11-13,21-23`) and `docs/pr-series/map.txt`.
- **The code:**
  - `:132` resets each PR to `BASE`, and no final tree comparison exists;
  - its EXIT trap removes the throwaway worktree with `git worktree remove --force`, against `worktrees.md`;
  - the worktree path is the legacy `../rocknix.worktrees/pr-stack-check` (`:122`);
  - with today's `upstream/next` it exits 2 at its base check, because two upstream commits are unmerged (R3).
- **Positive:** the tree, read; not run past `--help` (§ 8).

**F-26 — `rc-preflight` accepts an acceptance line whose kind it never checks, against any decided row, and reads a bug's "Code trace" two ways.** *Draft: Low. Q3.*
- **Where:**
  - acceptances, `:104-126`;
  - the two trace readers: comments only and no bullet at `:255`, body plus comments at `:274,287`;
  - a `box-check` outage reads as a checkbox FAIL, not as CANNOT (`:336-337`, with `box-check:53` exiting 1);
  - a freshness exit 1 is parsed as findings even after a crash (`:172`).
- **Positive:** the tree.

### `fork-package-freshness` (T8's lead)

**F-09 — `fork-package-freshness` diffs two trees without their merge base and takes added files only.** *Draft: Medium. Q3.*
- **The set** against today's `upstream/next` holds 47 rows. **22 are recipes upstream deleted later, not the fork's** (`libfmt`, `strace`, `cargo`, the three rust snapshots, `glslang`, ...), and one fork-added recipe is missing (`gstreamer`).
- **What it never sees:** the 63 recipes the fork *edited* since the merge base, 8 of which change `PKG_VERSION`.
- **A failed `git diff` passes:** with a missing base ref the list is rclone alone, and the exit is 0 (`done < <(packages)`, `:163`).
- **The verdicts T8 named** (LOCAL for a command-substituted version with a `case`-only `PKG_URL`; INHERITED for a `case`-branch override) are located at `:113-118` (R3 re-derived).
- **Positive:** P14.

### The renovation tools (P1's)

**F-27 — `renovation-inventory` rewrites `inventory.json` and `inventory.md` on a run whose counts disagree, before returning 1; its staged-path check compares counts, not sets; none of its subprocesses has a timeout.** *Draft: Low. Q3.*
- **Where:** `:1567-1593`, `:185-188` and throughout, at `2174265e9c`. #898 (its reach omits `PKG_DEPENDS_UNPACK`) is confirmed at `:357-362` and stays #898's.
- **Positive:** the tree.

**F-28 — `renovation-status`'s *Drift since* column prints the drift table's eighth cell, which is *Sensitive touched*; a closed slice reads `drifted` when any other slice in the ledger re-opens; and `closed` ignores the close reason.** *Draft: Low. Q3.*
- **Where:** `renovation-status:104,112-113`, against `renovation-drift:163`'s header.
- **Positive:** the tree.

**F-29 — `renovation-drift` reads `fixed_at` from `slices.json`, which no slice carries (0 of 46), while `renovation-status` reads the issue's field.** *Draft: Low. Q7.*
- **Effect:** run alone, drift says *no slice has a fixed_at yet* and exits 0.
- **Expected state or not:** the plan has the coordinator write the field at acceptance, so the absence is expected until a slice closes. The two readers of one fact are the finding.
- **Positive:** the tree and `slices.json`.

### Currency, layout and clarity

**F-31 — `fork-mirror-build-container.yml:34` puts `${{ secrets.GITHUB_TOKEN }}` into a `run:` script by expression; GitHub masks it, but the documented form is an `env:` variable.** *Draft: Low. Q2.*
- **Also:** its `runs-on: ubuntu-latest` (`:28`) is the one floating runner image of the four.
- **Positive:** the tree.

**F-32 — The legacy layout (#640) in twelve lines of the 31:**
- `pre-push:7,11,381,416`;
- `fork-worktree:9,72,74`;
- `pr-stack-check:122`;
- `archaeology:221`, `vocabulary-check:37`, `rc-preflight:345`;
- `renovation-drift:51` and `renovation-inventory:1506`, at `2174265e9c`.

`fork-worktree:72,74`'s remediation hint names `/workspace/repos/rocknix/.githooks`, which **exists**: it is the M7 lane's legacy checkout, so following the hint would point this clone at another checkout's hooks. `renovation-inventory`'s default `--es` does not exist (it fails closed). *Draft: Low (Q1), deferred to #640.*
- **Positive:** the tree; the paths tested with `test -e`.

**F-33 — The two upstream release scripts are two upstream commits behind** (`76693a738d`, `71d8932b33`; stage A), **and nothing in this fork runs them.** *Draft: Low (Q4, Q6).* They are upstream-carried, and the merge of `upstream/next` is the build-engine area's.
- **Positive:** stage A's provenance; the callers table.

**F-34 — `pre-push:337` is `if true; then`, a conditional with no condition; its header still teaches `../rocknix.worktrees/` (F-32).** *Draft: Low. Q7.*
- **Positive:** the tree.

### Leads not in this slice's paths

- **`tools/pkgcheck`** (T6's and T8's leads on #657: the heredoc `}` and Lua tables read as functions; the duplicate-function check across an `if`'s two arms) is not one of the 31. It is upstream's tool, and the inventory puts it in no T10 row. The coordinator's leads say *a T10 row*. This slice records them here and asks once on #657 whether `pkgcheck` joins the scope or goes to its own slice. The rows are not graded here.

## Coverage

One row per path. A cell names the finding or says `none` with what was read; `n/a` carries its reason.

| Path | Q1 Modernize | Q2 Standards | Q3 Bugs | Q4 Currency | Q5 Efficiency | Q6 Dead ends | Q7 Clarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.githooks/commit-msg` | none (bash, `pipefail`) | fails closed on every read (`:8-15`) | F-03 | n/a: no pin | one grep pair per commit | run by git; no case for `-m` `#` lines | header true but for F-03's assumption |
| `.githooks/guard-lib` | none | fails closed (`:14-22`); sources its lists (`. "${f}"`) | F-01 (no `--text` in its callers); redaction proven with a `/` in a class (P3b) | n/a | one awk per diff | sourced by three hooks | header claims *no path is exempt* against F-02 |
| `.githooks/hooks-test` | none | fixtures built at run time (`:13-16`) | none of its own; it has no case for F-01, F-02, F-03, F-10 | n/a | 0.71 s (16:47Z) | nobody runs it automatically (`04` § Q6) | case count 29/27, not the brief's 22/20 |
| `.githooks/pre-commit` | none | fails closed | F-01, F-02 | n/a | one diff of the index | run by git | the marker refusal is on lane branches only |
| `.githooks/pre-push` | F-32 (`:7,11,381,416`) | `pipefail`; `|| true` swallows the console-first diff's failure (`:456-459`) | F-01, F-02, F-10, F-16 | n/a | P3: 0.07 s to 9.82 s | the index warning only warns | F-34; header's *proven* refusals true (P1 controls) |
| `.githooks/secret-patterns` | none | one definition (`:8`), 15 alternatives | none (P3b) | n/a | n/a: data | sourced | true |
| `.github/scripts/generate-changelog.sh` | n/a: upstream's | upstream's | a bad range gives an empty changelog, rc 0 (R3) | F-33 | n/a | F-33: never run here | upstream's |
| `.github/scripts/generate-release-body.sh` | n/a: upstream's | upstream's | ignores the changelog's exit (R3) | identical to `upstream/next` | n/a | F-33 | upstream's |
| `.github/workflows/fork-checks.yml` | `actions/checkout@v4`, `ubuntu-24.04`: current | read-only permissions | F-06 | the pins named | 2 min 41 s a run | n/a: runs daily | header lists five checks of eight steps |
| `.github/workflows/fork-generic-x64.yml` | n/a | `if: ${{ false }}` | none | n/a | none | disabled on purpose (D-WORKFLOW-119/120) | header says so |
| `.github/workflows/fork-mirror-build-container.yml` | `ubuntu-latest` floats (F-31) | F-31 | none: the digest is checked (`:48`) | `skopeo` from apt, unpinned | n/a | dispatch only | true |
| `.github/workflows/fork-wordlist.yml` | `checkout@v4` | `pipefail` in its message step | F-30 (fifty messages on a new branch) | the pins | not read | n/a | header true |
| `tools/archaeology` | F-32 (`:221`) | always exit 0 | F-20 | n/a | 15 git hits a term, unannounced cap | rules only | header says `-S`; code uses `-G` |
| `tools/box-check` | none | `gh` failure exits 1 (`:53`) | F-04 | n/a | one GraphQL call, 2 s | CI, ceremony, preflight | header true for 300 |
| `tools/ceremony-check` | none | F-05's uncounted reports | F-05, F-15, F-16 (and #905's fixed reader) | n/a | 7.95 s with `box-check` (2.02 s of it), core 4,925 → 4,924 (16:47Z) | CI, push guard, preflight | `--no-gh` still runs `box-check` (`:18`, `:344`) |
| `tools/es-menu-map-check` | none | exits 2 when it cannot run | F-21 | n/a | reads one pin | `vm-qa` | docstring's *not merely mention* against shape 6 |
| `tools/forbidden-terms-check` | none | fails closed on the list | F-07 | n/a | 147 s for the tree, one grep a file | CI only | `--help` is a tree named `--help` |
| `tools/fork-package-freshness` | none | `eval`s recipe lines (`:136`) | F-09 | it is the currency tool | network per recipe | `rc-preflight` | header's *fork-added* set is a two-tree diff |
| `tools/fork-worktree` | F-32 (`:9,72,74`) | F-14 | F-11, F-12, F-13 | n/a | `du` capped at 10 s | rules; `pr-stack-check` | `remove` uses the cwd's git, against its header (`:27-31`) |
| `tools/lint-audit-artifacts` | none | broad `except` ends in `bad()` | F-08 | n/a | small | `ceremony-check`, the skill | fixtures prove two checks at once |
| `tools/pr-stack-check` | F-32 (`:122`) | EXIT trap `--force` | F-25 | n/a | not run | the release-notes skill | F-25: header claims a stack |
| `tools/prose-check` | none | self-test needs out-of-tree files | F-23 | n/a | small | two skills | the dead check |
| `tools/rc-preflight` | F-32 (`:345`) | exit codes defined | F-26 | it reads currency | network | rules only | header calls the audit *step 6* (step 4) |
| `tools/register-check` | none | fails closed at top level only | F-17 | n/a | grep over the live docs | CI, ceremony, `vm-qa` | header says *the two ways*; it has four |
| `tools/release-catalog` | none | `--write` with no artifacts writes 0 rows | F-24 | n/a | small | `rc-preflight` | footer's *forbid* has no code |
| `tools/renovation-drift` | F-32 (`:51`) | exit 1 shared by re-open and a gate field | F-29 | n/a | one numstat a slice | `renovation-status` | header's *Extended* re-open against plan § 8's *original depth* |
| `tools/renovation-inventory` | F-32 (`:1506`) | no timeouts | F-27 (and #898) | n/a | the plans in 4 workers | manual | three duplicated sizers |
| `tools/renovation-status` | none | exit 1 through uncaught `SystemExit` | F-28 | n/a | one drift call a closed slice | manual | README's *drift since* column, F-28 |
| `tools/rules-check` | none | crashes closed on a missing file | F-18 | n/a | small | CI, ceremony | header claims both entry files' counts: true |
| `tools/vocabulary-check` | F-32 (`:37`) | a missing checkout exits 1, not 2 | F-22 | n/a | small | `vm-qa` | header's *every sentence*, F-22 |
| `tools/work-log-index` | none | none | F-19 | n/a | small | CI, ceremony | header's *every timestamped entry*, F-19 |

## Proofs

| Proof | What it shows | Proved |
| --- | --- | --- |
| P1 | the constructed guard gaps: binary and `.po` pass the hooks, `#` lines pass `commit-msg`, a quoted personal path is caught by accident, the wordlist scan skips symlinks and passes an empty checkout | proved: tool-run |
| P2 | the personal-path lists agree entry by entry (115 at the hash, 118 at HEAD) | proved: tool-run |
| P3 | the push guard's cost over 1, 164 and 247 commits | proved: tool-run |
| P3b | the redaction survives the `/` inside a bracket class of `secret-patterns`' fifteenth alternative (GNU sed 4.9); the lead is withdrawn | proved: tool-run |
| P4 | `box-check`'s limit against the open count | proved: tool-run |
| P5 | `ceremony-check`'s hygiene limit against the closed-completed count | proved: tool-run |
| P6 | the tree's tracked symlinks | proved: tool-run |
| P7 | the CI's failing and skipped steps | proved: history |
| P8 | the level-3 work-log entries no index reads | proved: tool-run |
| P9 | `archaeology` on a term only blindspot row 7 carries | proved: tool-run |
| P10 | the lint's boundary in the 2026-09-28 folder | proved: tree |
| P10b | `prose-check` on a draft ending in a sign-off | proved: tool-run |
| P11 | the `--preserve` argument shape loops | proved: tool-run |
| P12 | `es-menu-map-check`'s visible and invisible settings pages at the pin | proved: tool-run |
| P13 | `vocabulary-check`'s script list against the cloud scripts that print player text | proved: tree |
| P14 | `fork-package-freshness`'s set against the merge base, the edited recipes, and a missing base ref | proved: tool-run |


## The first reader's 03-retrospective.md (whole)

# Retrospective (Phase 3) — M6.P2 T10, the guards (#657)

Phase 3 of the code-auditor skill, read over the 31 paths at the two hashes, with the renovation face's questions answered in `04`. This file is the history: how the guards came to be the shape they are, what each fix round left, and the seams where two of them meet.

## 3.1 How the guards were built

- **The push guard first** (`f51d081c04`, 2026-09-05): the credential scan at the tip, for the two secrets GitHub's push protection does not know (a ScreenScraper `devpassword=` and a RetroAchievements key).

  **The `.po`/`.pot` exemption arrived in that same commit**, with no reason in its message (F-02). Every later rewrite carried it forward: `17dbb85b88` (PL-08, #151), `3e70ef9239` (the guard library), `9e104c65f3` (the pre-commit). None re-read why it was there. That is the shape `engineering-practices.md` § Verify design intent warns about, the other way round: a constraint whose reason was never written, preserved by every round because it looked deliberate.
- **Every commit in the push, not only the tip** (`17dbb85b88`, 2026-09-13, audit #151 PL-08), with the three proven refusals in the hook's header.
- **The pre-commit and the wordlist** (2026-09-28, #307 and #312): a fixture committed as a literal cost a history rewrite (blindspot 67). The guard library followed, failing closed on every read (PL-011), judging a line after its label (PL-026), and with no path exempt (PL-012).

  The fix round's audit (claude G3-E-01/02/07, gpt G3-E-05/06) found three scan-skipping shapes: `diff.noprefix`, a `++ ` content line, a quoted name. Each became a `hooks-test` case.

  **The binary file is the fourth shape of the same family (F-01).** Each of the three was a way an added line reached `guard_added_lines` in a form it did not read; the binary file is a way an added line never reaches it at all. No round constructed a file git does not diff as text.
- **The checkers as a state machine** (`ceremony-check`, D-WORKFLOW-028, 2026-09-23), the push guard's gate and the fork CI's red badge. Audit #258 then moved the gate onto the primary checkout's tools (PL-004), so that a stale worktree could not skip it. That move also changed *which tree the gate reads* (F-16), and no record says that was weighed.
- **The renovation tools** (P1, 2026-10-22/23): the newest, and the only ones with a `--self-test`. The self-tests cover the parsing, not the counts the tools assert (F-27).

## 3.2 What each fix round left

| Round | What it fixed | What it left, found here |
| --- | --- | --- |
| #151 PL-08 (2026-09-13) | the range scan; `pr/*` keyed on the remote ref; failing closed on no base | F-10 (a quoted name in the personal-path match) |
| #307 / #312 (2026-09-28) | the pre-commit, the wordlist, three skip shapes | F-01 (binary), F-02 (`.po`), F-03 (`-m` `#` lines); the CI's lack of a credential scan (F-30) |
| #258 (2026-09-24/29) | the gate on the primary's tools; the retro marker anchored; the positives rule | F-16 (the gate reads the primary's tree); F-15 (the futro marker not anchored like the retro's) |
| #905 (2026-10-24, off this branch) | the friction reader reads every dated entry | F-15's residual: non-entry lines named, never owed |
| #646 (2026-10-22/23) | `register-check`'s `MISPLACED` | F-17 (slash shorthand, seven docs outside `LIVE`, T4's three) |

## 3.3 The class this slice hunted

T4's F-02 (`ceremony-check`'s friction reader skipping every line its regex did not match) and T6's #845 (`pkgcheck` exiting 0 on a name that matches nothing) are one class: **a checker that reads less than it reports, and passes.** Here it has 11 members (F-04, F-05, F-06, F-07, F-08, F-09, F-19, F-20, F-21, F-22, F-23; `command grep -o` over this list):

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

The rule that would have caught most of these is already written: `engineering-practices.md` § Guards must fail closed, *prefer a positive assertion over the absence of an error: collect what exists and check the count*. What is missing is its tool: **no checker here asserts that it read what exists.**

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


## The first reader's 04-analysis.md (whole)

# Analysis (Phase 4) — M6.P2 T10, the guards: hooks, the fork CI and the checkers (#657)

## Executive summary

The fork's guards do what their own suites say. `hooks-test` passes at the hash and in the worktree, and every refusal it constructs is refused. The record checkers pass on today's tree. The two lists that must agree (`PERSONAL_PATTERNS` and `fork-workflow.md` § Personal paths) agree entry by entry.

What the read found is one class, in eleven findings: **a checker that reads less than it reports, and passes**. The other findings around it are bugs of other shapes, Q6 gaps and Q1/Q7 rows.

**On the security list proper,** two findings matter:
- **F-01, High:** a file git treats as binary is never diff-scanned, so a credential or a listed word committed there passes the pre-commit. It passes the push guard too when it is removed again inside the push.
- **F-02:** `.po` and `.pot` files are exempt from every hook scan, with no recorded reason.

**`fork-worktree`**, the tool whose contract is never destroying build output:
- **F-11, High:** `remove --preserve` force-removes after a failed `mv`.
- **F-12:** `repair` deletes every untracked file inside a tracked directory.

**The fork CI:** a failing step hides every verdict after it (F-06), and it carries no credential scan (F-30, a contract lead).

`02` carries **34 findings** (F-01 to F-34), with draft severities counted from their headings:
- **2 High:** F-01, F-11.
- **13 Medium:** F-02, F-04, F-05, F-06, F-07, F-12, F-16, F-17, F-20, F-08, F-21, F-25, F-09. F-16 and F-30 are also contract leads for the coordinator.
- **19 Low:** F-03, F-10, F-30, F-13, F-14, F-15, F-18, F-19, F-22, F-23, F-24, F-26, F-27, F-28, F-29, F-31, F-32, F-33, F-34.

The punch list's size is stage D's: an item may carry more than one finding, and a withdrawn lead carries none.

These grades are this reader's before § Second opinion; the seats' pass is graded there.

## Acceptance-criteria scorecard

#657's 17 criteria, at the end of stage C. The final state is the hand-back's.

| # | Criterion | State | Evidence |
| ---: | --- | --- | --- |
| 1 | 00 to 05 | 00 to 04 written; 05 at stage D | this folder |
| 2 | lint PASS | pre-issue at stage C, resolution at close | `00` |
| 3 | review-plan.json Extended, both seats, packet manifest and scan | § Second opinion | `second-opinions/` |
| 4 | every punch item at a Phase 7 outcome | stage F | the audit issue |
| 5 | reviewed-at, fixed-at | `a82d784216` (both hashes named); fixed-at at hand-back | #657 |
| 6 | 01 § Scope | done | `01` |
| 7 | the coverage table, 31 rows | done | `02` § Coverage |
| 8 | § The suites | done, *a FAIL would mean* for each | `02` |
| 9 | § The CI | done | `02` |
| 10 | no forbidden run, no credential line, no listed word | so far; the folder's scan is in § Second opinion | `00` |
| 11 | Q6's guard table and tool-caller table | done | § Q6 |
| 12 | Q3's fail-open hunt | done | § Q3 |
| 13 | Q7's personal-path diff and three descriptions | done | § Q7 |
| 14 | proof cells = proof lines | 16 = 16 | `02` § Proofs, `00` |
| 15 | `question:` on every item; bugs pass box-check; no member edited before a stream | stage D | `05` |
| 16 | the retro | stage G | — |
| 17 | the six checks before merge | stage H | — |

## Risk assessment

- **The highest risk is to the history, and it is small in likelihood.** A credential reaches history through a binary file (F-01) or a `.po` file (F-02). Both need a value to land in such a file, which none of today's 133,409 scanned files shows for the wordlist (stage A). F-01's cost when it happens is the cost the pre-commit was written to remove: a rewrite of pushed history (blindspot 67).
- **The highest risk to work is `fork-worktree`** (F-11, F-12), the tool the rules send every agent to for removing a worktree. Its failure mode is the one D-WORKFLOW-005 exists to prevent: hours of build output, or a lane's uncommitted records, gone without a refusal.
- **The quiet risk is the record's own trust.** The class's eleven findings (`03` § 3.3) are checkers answering *nothing owed* about inputs they did not read (§ Q3). The tracker has outgrown two of their limits today (F-04, F-05). The ceremony state machine (D-WORKFLOW-028) and the RC preflight (D-WORKFLOW-047) are only as complete as those reads.
- **No risk to a player, and none to the two time-to-play numbers.** Nothing here runs on a device or in an image.

## Coverage boundary

- **Read whole in this session:** the three hooks, `guard-lib`, `secret-patterns` (as shapes and alternatives, never with a value) and `hooks-test`; the four workflows; `forbidden-terms-check` and `fork-worktree`; the two upstream scripts' diff.
- **Read by four read-only readers, with every lead that became a finding re-read here at its line or re-run:** `ceremony-check` (and #905's diff), `register-check`, `rules-check`, `work-log-index`, `box-check`, `lint-audit-artifacts`, `archaeology`, `es-menu-map-check`, `vocabulary-check`, `prose-check`, `release-catalog`, `rc-preflight`, `fork-package-freshness`, `pr-stack-check` and the three `renovation-*` tools.

  Their unverified items (gh's sort order, git's `-G` dialect, Claude Code loading nested rules, the grep locale) are not findings.
- **Not run, by § 8:** `fork-worktree remove|repair|sync`, `pr-stack-check` past `--help`, `fork-package-freshness` and `rc-preflight` over the network, `renovation-*` (they would rewrite ledgers).

  F-11, F-12 and F-25 are therefore proven by reading. Their fixtures are the streams'.
- **Not this slice's:** `tools/pkgcheck` (two coordinator leads on #657, recorded in `02` § Leads not in this slice's paths); the 19 upstream workflows; #898's reach gap; #905's fix (read as a diff).
- **The record:** the CI's runs read through the API, never re-triggered. The secret's value was never read.

## Finding Verification (Phase 4.5)

Each finding re-read against the artifact that would make it false.

| Finding | What would make it false | Checked | Verdict |
| --- | --- | --- | --- |
| F-01 | git diffing the file as text (an `.gitattributes` `diff` rule, `--text`) | `pre-commit:13`, `pre-push:268,272` carry no `--text`; no `.gitattributes` in the scratch; P1's controls refuse the text twin | confirmed |
| F-02 | a reason recorded for the exemption, or a scan elsewhere covering `.po` | `git show -s f51d081c04`: none; `fork-wordlist.yml` covers the wordlist only | confirmed |
| F-03 | git stripping `#` lines under `-m` | P1: the stored message keeps the line | confirmed; Low (the push guard catches it) |
| F-04 | `gh issue list` returning all issues past the limit | P4: 300 printed against 458/473 | confirmed |
| F-05 | the hygiene search under 200 results; the gh-failure branch appending to `overdue` | P5: 331; `:402-403`, `:425-426` read | confirmed |
| F-06 | `if: always()` or `continue-on-error` on the steps | `fork-checks.yml:34-59` carries neither; P7 | confirmed |
| F-07 | a symlink's target scanned elsewhere in the CI | `fork-wordlist.yml:28` is the tree scan; P1, P6 | confirmed |
| F-08 | the 2026-09-28 folder's seat rows verified by another route | P10: rows 192-881 outside the index the lint reads | confirmed |
| F-09 | the set being the fork's own additions | P14: 22 upstream deletions, 1 fork addition missing, a missing ref rc 0 | confirmed |
| F-10 | the personal-path match unquoting | P1: refused only for *could not be read* | confirmed; Low (caught by another check) |
| F-11 | an `mv` failure stopping the removal | `fork-worktree:190-201` read: `mv ... && echo`, no `||`, then `--force` | confirmed by reading; the fixture is the stream's |
| F-12 | repair descending into directories | `:231-238` read: top-level entries only, then `rm -rf` | confirmed by reading |
| F-13 | `shift 2` with one argument shifting | P11 | confirmed |
| F-14 | `rc` set anywhere | `:255-300` | confirmed |
| F-15 | the futro marker anchored | `:229` (anchored) against `:405` (unanchored) | confirmed |
| F-16 | the gate reading the pushed tree | `ceremony-check:51` (`ROOT` from its own file), `pre-push:60` | confirmed by reading; contract lead |
| F-17 | the slash second ID looked up | `register-check:32`; T4's control D-RA-006's history | confirmed |
| F-18 | `mention` matching a whole name | `rules-check:231`; R1's AGENTS.md half withdrawn | confirmed in part |
| F-19 | `###` entries indexed | P8 | confirmed |
| F-20 | the table rows searched | P9 | confirmed |
| F-21 | computed titles caught by another pattern | P12, `:50-56` | confirmed |
| F-22 | the five scripts printing no player text | `cloud_scan` prints through `why()` (R2; the scripts exist, P13) | confirmed in shape; which strings, the stream's |
| F-23 | the pattern matching at a line's end | P10b | confirmed |
| F-24 | the real record parsed | R2 names `h700-rc-20260920-77e7e97515`; `release-catalog:39` read | confirmed by reading |
| F-25 | a final tree comparison anywhere | `pr-stack-check:132` resets to `BASE`; no comparison found | confirmed by reading |
| F-26 | the acceptance kind validated | `rc-preflight:104-126`, `:255`, `:274` | confirmed by reading |
| F-27 | the write gated on `failed` | `renovation-inventory:1567-1593` | confirmed |
| F-28 | column 7 being the share | `renovation-drift:163`'s header | confirmed |
| F-29 | `slices.json` carrying `fixed_at` | 0 of 46 | confirmed as Q7 (expected until a close) |
| F-30 | a credential scan in a fork workflow | `command grep -c SECRET .github/workflows/fork-*.yml`: 0 in all four | confirmed; contract lead |
| F-31 | the secret passed through `env:` | `fork-mirror-build-container.yml:34` | confirmed; Low |
| F-32 | the paths current | `test -e`: the hint's path exists and is the legacy checkout's | confirmed; #640 |
| F-33 | the scripts merged and run | stage A; `build-nightly.yml`'s owner gate | confirmed |
| F-34 | the conditional doing something | `pre-push:337` | confirmed |
| R1–R4 leads not carried | — | R4's D2 withdrawn (the plan measures the same way); R1's AGENTS.md count withdrawn; the `secret-patterns` slash withdrawn (P3b) | withdrawn |

## Second opinion

*Pending stage C*: the two seats (GPT-6 Astra at `max`, Gemini 4 Argon at `high`), their probes and refutations, and each item graded with the artifact that decided it. The packet's manifest and its scan are recorded here before it is sent.

## Renovation face

### Q1 Modernize

- **The legacy layout (#640), F-32:** twelve lines, in four files at the hash and two at P1's tip. The one that is more than a stale word is `fork-worktree:72,74`: its remediation hint names `/workspace/repos/rocknix/.githooks`, which exists, as the M7 lane's legacy checkout. Following it would point this clone's hooks at another checkout's copy.
- **The workflows:** `actions/checkout@v4` and `ubuntu-24.04` are current. One runner floats (`ubuntu-latest`, F-31). `skopeo` comes from apt, unpinned.
- **The Python is 3.12-safe:** R2's compile under `-W error`; `ceremony-check:113`'s `hashlib.file_digest` needs 3.11+, and the runner has 3.12. **The bash needs 4+** (`mapfile`, `declare -A`).

### Q2 Standards

- **Fail-closed is the house shape and mostly kept.** `guard-lib` refuses on every unreadable or uncompilable input, and `hooks-test` proves each case.

  The departures:
  - `pre-push:456-459` (`|| true` swallows the console-first diff's failure);
  - `fork-worktree sync`'s return (F-14);
  - `vocabulary-check`'s missing checkout, which exits 1 like a finding rather than 2;
  - `renovation-status`'s exit 1 through an uncaught `SystemExit`;
  - `archaeology`'s unconditional 0 (F-20).
- **Lists sourced as shell:** `guard-lib:33,37` and `forbidden-terms-check:17` source their list files (`. "${f}"`). The files are the owner's, mode 0600 for the wordlist; the shape is noted, not a finding.
- **Recipe text evaluated:** `fork-package-freshness:136` `eval`s recipe lines, in a subshell with `set +u` (R3).
- **A secret by expression:** F-31.

### Q3 Bugs

The fail-open hunt the brief names, through every reader. For each: the line read, and a constructed input that is skipped while the reader passes, or why none can be.

| Reader | Line read | Constructed input skipped while it passes | Proof |
| --- | --- | --- | --- |
| `ceremony-check`'s friction reader (T4's F-02) | `:250-252` at the hash | `- 2026-10-20 10:00 UTC -- x -- issue: pending`, and any line without the field: fixed by #905's diff. The residual: a `### 2026-...` or `* 2026-...` line under `## Entries` is named as a non-entry, never owed (F-15) | the #905 diff and its fixture |
| `register-check`'s row and citation regexes | `:32`, `:35`, `:42` | the second ID of `D-WORKFLOW-155/156`; a duplicate row written `|  D-...` with two leading spaces; any document outside `LIVE` (F-17) | tree |
| `rules-check`'s front matter, count and mention | `:198`, `:231`, `:151` | a rule dropped from `CLAUDE.md`'s table while its name survives in a path (`worktrees` in `../rocknix.worktrees/`); a rule under `.claude/rules/sub/` (F-18) | tree |
| `box-check`'s issue list and checkbox regex | `:83`, `:47` | the 158 (now 173) oldest open issues; a `* [ ]` or `1. [ ]` checkbox; a curly apostrophe in *maintainer’s* (F-04) | P4 |
| `work-log-index`'s heading regex | `:40` | the 14 `### HH:MM UTC` entries (F-19) | P8 |
| `pre-push`'s personal-path match | `:395-409` | a path git quotes (`docs/<non-ASCII>.md`): unmatched, refused only by the tip scan's read failure (F-10) | P1 |
| `guard_added_lines`'s diff parser | `guard-lib:57-81` | **none that reaches it.** Every header it cannot read is refused (`unknown`, `orphan`), and the three shapes the fix round named are `hooks-test` cases. The skip is upstream of it: a binary file sends it no lines (F-01) | P1, `hooks-test` |
| `forbidden-terms-check`'s file loop | `:37`, `:46-50` | the 180 tracked symlinks; a checkout with its files absent passes as `0 hits in 0 tracked files` (F-07) | P1, P6 |
| the lint's index boundary and YAML reader | `:182`, `:351` (hash) | a table cell quoting `## Verification`; an indented `punch_index` (F-08) | P10 |
| `archaeology`'s blindspot reader | `:76-91` | blindspots 1 to 29 (F-20) | P9 |
| `es-menu-map-check`'s screen patterns | `:50-56` | the 22 computed titles (F-21) | P12 |
| `fork-package-freshness`'s set | `:91`, `:163` | the 63 edited recipes; a missing base ref (F-09) | P14 |

Beside the hunt, the other bugs:
- the two hook gaps that are not reader skips (F-02, F-03);
- the CI's step order (F-06);
- `fork-worktree` (F-11 to F-14);
- the release and renovation tools (F-24 to F-29).

### Q4 Package currency

Not a package slice. One table:

| Item | State | Source |
| --- | --- | --- |
| `generate-release-body.sh` | identical to `upstream/next` | stage A |
| `generate-changelog.sh` | two upstream commits behind (`76693a738d`, `71d8932b33`), not a fork hunk | stage A, F-33 |
| `actions/checkout` | `@v4` in two workflows | tree |
| runner images | `ubuntu-24.04` in three; `ubuntu-latest` in one (F-31) | tree |
| `skopeo` | `apt-get install`, unpinned | `fork-mirror-build-container.yml:31` |
| what GitHub reports | 23 workflows, all `active` | `02` § The CI |

### Q5 Efficiency

| Cost | Figure | Source |
| --- | --- | --- |
| the push guard, on this branch | 0.07 s (1 commit), 0.76 s (164), 9.82 s (247) | P3 |
| the pre-commit | one `git diff --cached` and two greps a commit; `hooks-test` whole in 0.71 s | stage B |
| `ceremony-check` | 7.95 s, `box-check` 2.02 s of it; one GraphQL call; core 4,925 → 4,924 | stage B |
| `box-check` | one GraphQL call, 2 s, 300 issues | P4 |
| `forbidden-terms-check` on the tree | 147 s, one `grep` process per tracked file (133,409) | stage A |
| `fork-checks.yml` | 2 min 41 s a run | the CI |

`forbidden-terms-check`'s one-grep-per-file loop is the only figure here that a reader would notice. A single `git grep` over the tree (which still honours symlinks, F-07) is the obvious form; it is the stream's to weigh with F-07.

### Q6 Dead ends and brittleness

**The guard table.** One row per refusal the code wires, with its positive: a `hooks-test` case by name, a recorded run, or **none**, which is a punch item.

| Guard | Refusal | Positive |
| --- | --- | --- |
| `pre-commit` | a credential-shaped added line | `hooks-test` *a credential-shaped line* |
| `pre-commit` | a listed word | *a listed word*; *a listed word in another case, on line 2* |
| `pre-commit` | an audit-packet path, not exempt | *the same line under an audit packet* |
| `pre-commit` | a header the scan cannot read (noprefix, `++ `, quoted name) | *with diff.noprefix set*; *a content line beginning ++*; *a file name git prints in quotes* |
| `pre-commit` | a credential list that does not compile | *a credential list that does not compile* |
| `pre-commit` | no wordlist | *no wordlist at all* |
| `pre-commit` | an unreadable index | *an index that cannot be read* |
| `pre-commit` | a conflict marker (lane branches only, #696) | *a leftover conflict marker* (worktree's suite) |
| `pre-commit` | `mktemp` failing | **none** (not constructible without a full tmp; named, not a punch item) |
| `commit-msg` | a listed word | *a listed word in the message* |
| `commit-msg` | a credential-shaped line | *a credential-shaped line in the message* |
| `commit-msg` | an unreadable message file | *a message file that cannot be read* |
| `commit-msg` | no wordlist | *a message with no wordlist to judge it by* |
| `pre-push` | a listed word in a middle commit | *a listed word in a middle commit, gone at the tip* |
| `pre-push` | a credential in a middle commit | *a credential in a middle commit, gone at the tip* |
| `pre-push` | an older line in a touched file (the tip scan) | *an older line in a file the range only touches beside* |
| `pre-push` | a listed word in a message | *a listed word in a commit message* |
| `pre-push` | a credential-shaped line in a message | **none**: no `hooks-test` case constructs it |
| `pre-push` | a quoted name with noprefix | *a credential in a file git prints in quotes, pushed from a clone with diff.noprefix* |
| `pre-push` | a list not compiling; no wordlist; a tip the clone lacks (a range it cannot diff) | three cases by those names |
| `pre-push` | a file unreadable at the tip | **none** in `hooks-test`; met by accident in P1 (the quoted name) |
| `pre-push` | personal paths on a `pr/*` destination | the header's 2026-09-13 proof (`pre-push:39-42`); **none** in `hooks-test` |
| `pre-push` | `pr/*` with no base | the header's 2026-09-13 proof; **none** in `hooks-test` |
| `pre-push` | more than one commit on `pr/*` (D-WORKFLOW-079) | **none** |
| `pre-push` | an assistant named in a `pr/*` message (D-WORKFLOW-078) | **none** |
| `pre-push` | dev/VM wording in product scripts (console-first) | **none** |
| `pre-push` | the ceremony gate refusing | **none** in `hooks-test`; `ceremony-check`'s own (below) |
| `pre-push` | `ceremony-check` missing | **none** |
| `guard_load` | an unreadable or empty list | *no wordlist at all* (both hooks) |
| `register-check` | DUPLICATE, MISSING, PLACEHOLDER | **none found** by this session's search (a work-log line naming the tool beside a positive word) |
| `register-check` | MISPLACED | its constructed failure, 2026-10-23 work log `:250` (#646) |
| `rules-check` | front, index, tools, agents, count, budget, list, mention | **none found** in the record by tool name and a positive word (stage B search); the brief cites D-WORKFLOW-045's adoption only |
| `box-check` | a person or device checkbox without a fact | its constructed positive on each side, 2026-09-25 work log `:25`; the first run's *46 of 479* is the brief's § 3, not re-found by the phrase |
| `ceremony-check` | its eleven lines | the CI dispatch input `ceremony_today` (#258 PL-020); #905's fixture for the friction line (off branch) |
| `lint-audit-artifacts` | its contract failures | the P1 pass/fail fixtures (two checks proven at once, F-08); *seen to fire on seven*, 2026-09-28 work log `:62` |
| `archaeology` | — (no failing verdict; exit 0 always) | `--reversal`'s constructed case (audit #258 P-02, brief § 3) |
| `es-menu-map-check` | MISSING, STALE | first run 2026-09-18 (30 of 51 screens), work log `:204` |
| `vocabulary-check` | a vocabulary failure | **none found** |
| `prose-check` | its tells | `--self-test` (stage A, rc 0) |
| `release-catalog` | `--check` stale | **none found** |
| `rc-preflight` | its items | 2026-09-25 work log `:231` (*each item seen to fail*); `already written`, 2026-09-26 (#289, brief § 3) |
| `fork-package-freshness` | BEHIND, UNKNOWN | **none found** for BEHIND by this search |
| `pr-stack-check` | its failures | 2026-09-29 work log `:236` (*seen to fail three ways*) |
| `work-log-index` | `--check` STALE | **none found** |
| `forbidden-terms-check` | a hit in the tree; an unreadable list | **none found** for a tree hit; the unreadable-list refusal is constructed by `hooks-test`'s stand-in only for the hooks |
| `fork-worktree` | `remove`'s refusal on build output | **none found** |
| the `renovation-*` tools | counts disagree; re-open | `--self-test` for parsing; **none** for the count assertions (F-27) |

**The tools nobody runs automatically** (from `02` § Callers):
- `hooks-test`;
- the lint's fixtures;
- `archaeology` and `rc-preflight` (rules only);
- `renovation-inventory` and `renovation-status` (README only);
- the two upstream scripts (never in this fork);
- `fork-generic-x64.yml` (disabled on purpose, D-WORKFLOW-119/120).

Each is a `Renovation` item with the coordinator's disposition pending, except the disabled workflow and the upstream scripts, which are recorded rows.

**What the guard table says, in one line:** every hook refusal the fix rounds named has a `hooks-test` case. **The rest of the push guard's refusals do not:** the six `pr/*` refusals, the message-credential scan, and the gate. Neither do most checkers' failing verdicts, outside a first run in a work log.

### Q7 Clarity and structure

**`fork-workflow.md` § Personal paths against `PERSONAL_PATTERNS`, entry by entry** (P2):
- At the hash, all 115 hook entries are in the rule's section. Every path-shaped token of the section is a hook entry except four prose mentions (`.githooks/pre-push`, `packages/`, `projects/`, `tools/`), which are not list entries.
- At HEAD it is the same with 118 (P1's three `renovation-*` tools on both sides).

**Entries on one side only: none.** The stage-A delta (14 `scripts/` entries against the brief's 12) is 12 under `scripts/` and 2 under `scripts/lib/`.

**The three descriptions per guard** (the header, the rule, the index row in `instruction-files.md`), against the code:

| Guard | Header | Rule | Index | Drift |
| --- | --- | --- | --- | --- |
| `pre-commit` | *refuse a commit that would ADD a credential-shaped line* | `fork-workflow.md` § Safety net: *no path is exempt* | (not indexed; hooks are in the rule) | the `.po` exemption against *no path is exempt* (F-02, a Q3 bug) |
| `commit-msg` | *Comment lines are dropped as git drops them* | the same | — | git keeps them under `-m` (F-03) |
| `pre-push` | *every branch is scanned ... in every commit the push carries* | the same | — | binary files (F-01); the header's `../rocknix.worktrees/` (F-32) |
| `guard-lib` | *no path is exempt* (`:20`) | the same | — | F-02 |
| `forbidden-terms-check` | *every tracked file of a tree* | `fork-workflow.md`: *reads a whole tree* | *does a tree ... carry a word from the list* | symlinks skipped (F-07) |
| `box-check` | *every open issue on the fork* (`:9`) | `issue-tracking.md`: *reads every open issue* | *is every open acceptance checkbox on the fork agent-verifiable* | 300 of 458 (F-04) |
| `ceremony-check` | `--no-gh`: *without the tracker* (`:18`) | `ceremonies.md`'s table | *which ceremony is owed* | `--no-gh` still runs `box-check` (`:344`); the gate's tree (F-16) |
| `work-log-index` | *every timestamped entry* (`:7`) | `learning-capture.md` | *the day, week and month table of contents* | `###` entries (F-19) |
| `archaeology` | *`git log -S`* (`:22`) | `decision-register.md`: *reads ... every work-log entry* | *what the record already says* | `-G`, not `-S`; OR, not AND; blindspots 1-29 (F-20) |
| `vocabulary-check` | *every sentence the cloud scripts print* (`:20-22`) | `es-player-text.md`: *reads every `_("")` string and every sentence the scripts print* | *back up / backup, and the rest* | seven of twelve scripts; `es-app` only (F-22) |
| `es-menu-map-check` | *not merely mention its words* (`:135`) | `es-native-ui.md`: *reads every screen title* | *does the map still describe the menus* | computed titles (F-21); shape 6 accepts a mention |
| `register-check` | *refuses the two ways* (`:5-6`) | `decision-register.md` | *every decision ID once, every citation naming a real row* | four checks, not two; slash shorthand (F-17) |
| `rules-check` | checks both entry files' counts | `instruction-files.md` | *the counts in CLAUDE.md and AGENTS.md true* | true; `mention` a substring (F-18) |
| `pr-stack-check` | *stacks one commit per PR ... the last head equals next* | `fork-workflow.md` | *prove the last head equals next on every upstream-bound path* | no stack, no final comparison (F-25) |
| `rc-preflight` | the upstream audit *step 6* (`:51-53`) | `release-candidates.md`: step 4 | — | a step number (Low, in F-26) |
| `fork-worktree` | *Every git read below is about the repository this tool lives in* (`:27-31`) | `worktrees.md` | *list / remove / repair / sync, refusing to destroy build output* | `remove` runs `git worktree remove` in the caller's cwd, without `-C "${ROOT}"` (`:201`); F-11, F-12 |
| `release-catalog` | footer: a folder without a record is *forbid* | `issue-tracking.md` | *what each kept cut carried* | no code lists such folders (F-24) |
| `renovation-drift` | a sensitive file re-opens *at Extended depth* | plan § 8: *at its original depth* | *exits 1 when one must re-open* | the depth (F-29's file; Q7 row) |
| `renovation-status` | README: a *drift since* column | plan § 9 | *one table of the renovation* | the column shows *Sensitive touched* (F-28) |

**Structure:** `renovation-inventory`'s `build()` holds three jobs, and slice-membership sizing is written four times across the three tools (R4). `pre-push:337` is `if true; then` (F-34).

Each drift in a rule's text is a lead for the coordinator (T4 is accepted; a rule edit is a stream only with #657's dispatch), and each drift that hides a failure is the Q3 bug named in its row.

## Quality self-check

- **Every finding names its file and line at the read hash**, and its positive (a `PROOF:` line) or the line read.

  The leads that did not hold are withdrawn by name:
  - R1's AGENTS.md count;
  - R4's D2;
  - the `secret-patterns` slash.
- **Counts were taken by command, and five typed figures were caught before commit:**
  - the skipped-file count (*56*, then 180);
  - two runtimes (*about 3 s*, *about 10 s*, then measured);
  - the class size (*fourteen*, then 11);
  - the proof count (*14*, then 16).

  Each is recorded in `00`. Two pattern errors of my own were re-run (P8, P14).
- **The harness's `grep` function** (ugrep with `-I --ignore-files`) was noticed at 16:39, and every count after it uses `command grep`.
- **The security list held:**
  - no value and no listed word was printed, in the transcript or in this folder;
  - the constructed values were built from pieces, and the stand-in list is `hooks-test`'s own.

  The folder's own scan is part of the packet's, at stage C.
- **What this read cannot prove:**
  - F-11 and F-12 as runs (§ 8);
  - F-22's exact strings;
  - F-24 beyond R2's named record;
  - the tracker's sort order behind F-04's *oldest* (R1, unverified).


## Context: fork-workflow.md § Personal paths (next)

**Personal paths** (must never reach an upstream PR). This list and `PERSONAL_PATTERNS`
in `.githooks/pre-push` are the same list; change one and change the other.

- **Agent context** — `.claude/`, `CLAUDE.md`, `AGENTS.md`, `.githooks/`,
  `.github/sessions/`, `.github/workflows/fork-*`
- **Personal writing** — `docs/`, `plans/`
- **Fork-only tools** — `tools/fork-publish-release`, `tools/pixelelated-state-check`, `tools/pixelelated-state-check-test`, `tools/cloud-test-backend`, `tools/cloud-connections-test`, `tools/cloud-input-test`, `tools/test-fixtures/`, `tools/cloud-round-trip`, `tools/cloud-save-integrity`, `tools/cloud-save-integrity-test`, `tools/cloud-capture-stamp-test`, `tools/wait-lock-test`, `tools/last-good-scripts-test`, `tools/settings-modes-test`, `tools/melonds-upgrade-test`, `tools/lint-audit-artifacts`, `tools/vm-visual-qa`, `tools/vm-serial`, `tools/vm-pair`, `tools/vm-pair-test`, `tools/vm-stop`, `tools/vm-stop-test`, `tools/vm-manager-system-check`, `tools/cloud-pair-migration`, `tools/rasteratops-cloud-layout-test`, `tools/pixelelated-content-scope-test`, `tools/pixelelated-cloud-folder-test`, `tools/pixelelated-cloud-folder-vm-test`, `tools/pixelelated-cloud-validator-test`, `tools/pixelelated-save-layout-test`, `tools/pixelelated-duckstation-capture-test`, `tools/rasteratops-identity-check`, `tools/rasteratops-candidate-store`, `tools/rasteratops-vm-cloud-epic`, `tools/pixelelated-vm-cloud-boundaries`, `tools/cloud-census`, `tools/emulator-exit-test`, `tools/vm-qa`, `tools/time-to-play`, `tools/vocabulary-check`, `tools/forbidden-terms-check`, `tools/register-check`, `tools/rules-check`, `tools/box-check`, `tools/release-catalog`, `tools/rc-preflight`, `tools/device-act`, `tools/ra-offline-test`, `tools/ra-ui-test`, `tools/raofflineproxy-integration-test`, `tools/raofflineproxy-installed-native-test`, `tools/raofflineproxy-consent-test`, `tools/qa-accounts`, `tools/vm-walks/`, `tools/fork-worktree`, `tools/fork-package-freshness`, `tools/vm-upgrade-rehearsal`, `tools/vm-upgrade-readiness-test`, `tools/frame-diff`, `tools/archaeology`, `tools/work-log-index`, `tools/ceremony-check`, `tools/es-syntax-check`, `tools/png-blackout`, `tools/fork-newdrive`, `tools/es-untranslated`, `tools/font-stems`, `tools/signin-memory`, `tools/es-launch-memory`, `tools/nova-led-test`, `tools/build-identity-test`, `tools/rocknix-info-test`, `tools/usb-gadget-test`, `tools/es-menu-map-check`, `tools/ra-candidate-games`, `tools/retroarch-wrapper-test`, `tools/build-preflight`, `tools/host-maintenance/`, `tools/watch-job`, `tools/watch-build`, `tools/watch-build-submit`, `tools/pr-stack-check`, `tools/prose-check`, `tools/council/` (the council runner), and the council toolchain at scaffold's own paths (`scripts/council-*`, `scripts/lint-council-*`, `scripts/build-council-prompt.ts`, `scripts/write-step-seal.ts`, `scripts/verify-{pins,chain,seals}.ts`, `scripts/check-stale-blob-drift.ts`, `scripts/setup-council-mistral-tokenizer.mjs`, `scripts/forge-write-status.mjs`, `scripts/owner-queue-lint.mjs`, `scripts/lib/council-*`, `scripts/lib/verifier-pins.ts`, `scripts/__tests__/`, `seed/`, `verifier-pins.json`, `council-seat-efforts.json`; #70, D-WORKFLOW-088). One entry per tool, the same entries as `PERSONAL_PATTERNS`; the 2026-09-12 audit found the prose three short
- **Council artifacts** — `research/`
- **Copilot-era leftovers** — `.github/copilot-instructions.md`, `.github/instructions/`,
  `.github/shared-copilot-knowledge/`, `tmp/shared-copilot-knowledge/`,
  `compare-prompt-versions.sh`. Retired from `next`, but branches and worktrees cut
  before the retirement still contain them, so the guard still watches for them.

`tools/` is **not** disjoint from the feature areas — most of it is upstream's, and only
the five entries above are ours. That is why fork-only tools are enumerated rather than
matched by prefix, and why a new one has to be added to the guard by hand. The guard
warns about any `next`-only file outside `packages/` and `projects/` that it does not
recognise; that warning is the reminder.



## Context: fork-workflow.md § Safety net (next)

## Safety net: pre-push guard, and the pre-commit scan

Three hooks share one library, `.githooks/guard-lib`, and two lists.
`.githooks/pre-commit` refuses a commit that would add a credential-shaped
line (the patterns in `.githooks/secret-patterns`), because the push guard
reads history and a line that reaches history costs a rewrite to remove
(2026-09-28, #307). `.githooks/commit-msg` reads the message the same way.
The second list is a **wordlist the fork must not carry anywhere** -- tree,
commit messages, tracker -- and it lives **outside every tree**, at
`~/.config/rocknix/forbidden-terms` (mode 0600; the fork CI reads the
repository secret `FORBIDDEN_PATTERNS` instead), because a list of the words a
tree must not hold would itself hold them. It is not reproduced, quoted or
described in anything the fork carries, the maintainer's request included
(#312, D-WORKFLOW-061): a refusal names the file and the line, never the word.
`tools/forbidden-terms-check` reads a whole tree (or `--stdin`) against it.
The runner half is `.github/workflows/fork-wordlist.yml`: every push of every
branch, the tree and the pushed messages, red without the secret.

Every scan fails closed: a list that cannot be read, a pattern that does not
compile, a grep that dies, a diff or a message that cannot be read each
refuses. A line is judged after its label, so a file's *name* is never a
credential, and no path is exempt -- an audit packet that carries a
credential-shaped line is redacted in the packet. `.githooks/hooks-test` is
the guards' own proof, with a stand-in list and a run-time fixture; run it
after any change here, and the ES fork's `.githooks/pre-push-test` after a
change there. The hooks run in every worktree because the hooks path is
absolute (below); a machine without the wordlist file cannot commit until it
has one, which is the point.

`.githooks/pre-push` blocks pushing any `pr/*` branch that still differs from `upstream/next`
in a personal path (e.g. you forgot to rebase). Enable it once per clone — the setting is
shared by every worktree, so it does not need repeating per worktree:

```bash
git config core.hooksPath "$(git rev-parse --show-toplevel)/.githooks"
```

**The absolute path is the point.** A relative `core.hooksPath=.githooks` resolves against
whichever working tree you push from, and a correctly built `pr/*` branch contains no
`.githooks/` — excluding it is what the `--onto` rebase is for. Check that branch out in a
worktree and the hook file is simply absent, so git runs no hook and the guard silently
does not apply. The better the PR branch, the less the guard exists. Pointing at the main
checkout by absolute path pins the hook to something every branch can see.

Only `pr/*` branches are guarded for personal paths; **every** branch is scanned
for credential-shaped lines (below).

The guard also enforces the **console-first content rule** on `pr/*` branches: added
lines in product-surface scripts (`projects/ROCKNIX/packages/network/rclone/sources/`,
`projects/ROCKNIX/packages/rocknix/sources/scripts/`) must not mention QEMU/VMs,
user-mode networking, port forwards, or loopback QA addresses.

The guard also scans **every** pushed branch — not only `pr/*` — for lines
shaped like credentials (`SECRET_PATTERNS` in the hook: a ScreenScraper
`devpassword=` with a real value, a RetroAchievements `&y=KEY`, GitHub/AWS/Slack
token formats, private-key blocks, `TOKEN=`/`PASSWORD=` with a long literal).
Placeholders in `<angle brackets>` never match, so documentation passes and a
pasted secret does not. GitHub's own push protection is on for both public
repos but knows only its catalogue of token formats, which is why the hook
carries the two this fork actually handles.

**Check the hook can run at all.** `ls "$(git config core.hooksPath)"` must list
`pre-push`. A `core.hooksPath` naming a directory that no longer exists runs
nothing and says nothing — that was the state for a day after the 2026-09-04
move to `/workspace` (blindspot 26). `tools/fork-worktree list` and `sync` now
warn when the path is unset, relative, or missing.



## Context: ceremonies.md's table (next)

| Ceremony | Marker the tool reads | Cadence (D-QA-040) | When overdue |
| --- | --- | --- | --- |
| Friction entry | a line in `docs/friction-log.md` with `issue: #N` or `guard` | an issue or a guard within 3 days of the line | **refuses a push of next** |
| Mini-retro (phase tier) | `docs/retros/<date>-<scope>.md`, or a work-log heading that says retro | every 5 active days, grace 2 | refuses a push |
| Weekly summary | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy>-W<ww>-summary.md` | by the Tuesday after the week | refuses a push |
| Monthly summary | `docs/work-logs/<yyyy_mm>-work_logs/SUMMARY.md` | by the 3rd of the next month | refuses a push |
| Work-log index | `tools/work-log-index --check` | with every log entry | refuses a push |
| Register lint | `tools/register-check` | always | refuses a push |
| Issue ownership citation | fork commits on `next` after `bf121ce876` cite `#N`; upstream and pre-adoption history excluded (D-WORKFLOW-132) | every new fork commit, including merges | refuses a push |
| Blindspot guard | an entry from 52 on names a `tools/…`, `.githooks/…` or `.claude/rules/…` that exists | with the entry | refuses a push |
| Code audit (epic/milestone tier) | an issue titled `Audit:` / `Code audit`, or `docs/audits/<date>-*/` | after 12 completed closures or 14 days | **CI red**, the push goes through |
| Futro | `docs/futros/<date>-<scope>.md`, or a work-log heading that says futro | within 3 days of a new `epic` issue | CI red |
| Open checkboxes agent-verifiable | `tools/box-check`: no open `- [ ]` names a person or a device without a physical fact (D-QA-044) | always | CI red -- the fix is a tracker edit, as with issue hygiene |



## File: .githooks/pre-push (at 8ebaf8daad, 470 lines)

```text
    1  #!/usr/bin/env bash
    2  # pre-push guard for the pixelelated/distribution fork.
    3  #
    4  # Blocks pushing a PR branch (pr/*) that carries personal fork artifacts which
    5  # must never reach an upstream pull request. Build clean PR branches by
    6  # content, from upstream/next (.claude/rules/fork-workflow.md):
    7  #   git worktree add --detach ../rocknix.worktrees/pr-<name> upstream/next
    8  #   git switch -c pr/<name> && git checkout next -- <the feature paths> && git commit
    9  #
   10  # INSTALL WITH AN ABSOLUTE PATH:
   11  #   git config core.hooksPath /path/to/rocknix/.githooks
   12  #
   13  # A *relative* `core.hooksPath=.githooks` looks right and silently does nothing
   14  # where it matters most. The path resolves against whichever working tree you
   15  # are pushing from, and a correctly built pr/* branch has no `.githooks/` in it
   16  # - excluding it is the whole point of building it by content. Check out such a
   17  # branch in a worktree and the hook file is simply absent, so git runs no hook
   18  # and every check below is skipped. The better the PR branch, the less the
   19  # guard exists. An absolute path pins the hook to the main checkout, so it runs
   20  # regardless of which branch or worktree is being pushed.
   21  #
   22  # Only pushes whose DESTINATION is refs/heads/pr/* are guarded for personal
   23  # paths -- `git push origin feature/x:pr/x` lands on pr/x and is judged as
   24  # pr/x; every branch is scanned for credential-shaped lines and for the
   25  # wordlist kept outside the tree (.githooks/guard-lib says where), in every
   26  # commit the push carries and its message, not only at its tip.
   27  #
   28  # Fails closed: a pr/* push with no upstream/next or origin/next to compare
   29  # against is refused, not waved through with a warning, and so is any push
   30  # whose range this hook cannot diff. Proven on 2026-09-13 (audit #151 PL-08)
   31  # in a scratch repo with `core.hooksPath` pointing at this directory, one
   32  # refusal each -- the commands, then the hook's answer:
   33  #
   34  #   # a value committed in the middle of the push and removed again at its tip
   35  #   #   (devpassword=<sixteen letters spelling nothing>; a tip-only scan passes it)
   36  #   git push scratch feature/x
   37  #     -> "refusing to push feature/x: it carries lines shaped like credentials:"
   38  #        "  7a9d1d2:notes.txt:+[REDACTED]" (the middle commit, named), exit 1
   39  #   # a personal path pushed to a pr/* destination under another local name
   40  #   git push scratch feature/p:refs/heads/pr/p
   41  #     -> "pre-push blocked: pr/p (pushed from feature/p) carries personal artifacts
   42  #         that must not go upstream:  docs/note.md", exit 1
   43  #   # a pr/* push with no upstream/next and no origin/next in the repo
   44  #   git push scratch pr/y
   45  #     -> "refusing to push pr/y: no upstream/next or origin/next to compare a pr/* branch against", exit 1
   46  #
   47  # The hook at next 6e09b6fcca let all three through (the first two silently,
   48  # the third with a warning); the same three shapes without their fault push
   49  # through this one, and a range git cannot diff at all is refused too.
   50  
   51  set -uo pipefail
   52  
   53  # Personal paths that must never appear in an upstream PR branch.
   54  # Keep this in step with `.claude/rules/fork-workflow.md` § "Personal paths".
   55  # The checkout this hook lives in: the tools the guard runs live beside it.
   56  # core.hooksPath is an absolute path into the primary checkout, so this is
   57  # the primary's tools/ whichever worktree pushes -- it used to be the
   58  # pushing worktree's, and a worktree cut before a tool existed pushed next
   59  # with that gate silently skipped (audit #258 PL-004).
   60  hooks_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." 2>/dev/null && pwd)"
   61  
   62  PERSONAL_PATTERNS=(
   63    # Agent context, rules and skills
   64    '.claude/'
   65    'CLAUDE.md'
   66    'AGENTS.md'
   67    '.githooks/'
   68    '.github/sessions/'
   69    '.github/workflows/fork-'
   70    # Personal documentation and planning
   71    'docs/'
   72    'plans/'
   73    # Fork-only tooling. `tools/` as a whole is upstream's, so these are listed
   74    # one by one; a new fork-only tool must be added here by hand (the unlisted
   75    # check below is what reminds you).
   76    'tools/fork-publish-release'
   77    'tools/pixelelated-state-check'
   78    'tools/pixelelated-state-check-test'
   79    'tools/cloud-test-backend'
   80    'tools/cloud-connections-test'
   81    'tools/cloud-input-test'
   82    'tools/test-fixtures/'
   83    'tools/cloud-round-trip'
   84    'tools/cloud-save-integrity'
   85    'tools/cloud-save-integrity-test'
   86    'tools/cloud-capture-stamp-test'
   87    'tools/wait-lock-test'
   88    'tools/last-good-scripts-test'
   89    'tools/settings-modes-test'
   90    'tools/melonds-upgrade-test'
   91    'tools/lint-audit-artifacts'
   92    'tools/es-untranslated'
   93    'tools/font-stems'
   94    'tools/signin-memory'
   95    'tools/nova-led-test'
   96    'tools/usb-gadget-test'
   97    'tools/build-identity-test'
   98    'tools/rocknix-info-test'
   99    'tools/es-launch-memory'
  100    'tools/es-menu-map-check'
  101    'tools/ra-candidate-games'
  102    'tools/retroarch-wrapper-test'
  103    'tools/build-preflight'
  104    'tools/host-maintenance/'
  105    'tools/watch-job'
  106    'tools/watch-build'
  107    'tools/watch-build-submit'
  108    'tools/vm-visual-qa'
  109    'tools/vm-serial'
  110    'tools/vm-pair'
  111    'tools/vm-pair-test'
  112    'tools/vm-stop'
  113    'tools/vm-stop-test'
  114    'tools/vm-manager-system-check'
  115    'tools/cloud-pair-migration'
  116    'tools/rasteratops-cloud-layout-test'
  117    'tools/pixelelated-content-scope-test'
  118    'tools/pixelelated-cloud-folder-test'
  119    'tools/pixelelated-cloud-folder-vm-test'
  120    'tools/pixelelated-cloud-validator-test'
  121    'tools/pixelelated-save-layout-test'
  122    'tools/pixelelated-duckstation-capture-test'
  123    'tools/rasteratops-identity-check'
  124    'tools/rasteratops-candidate-store'
  125    'tools/rasteratops-vm-cloud-epic'
  126    'tools/pixelelated-vm-cloud-boundaries'
  127    'tools/cloud-census'
  128    'tools/emulator-exit-test'
  129    'tools/vm-qa'
  130    'tools/time-to-play'
  131    'tools/vocabulary-check'
  132    'tools/forbidden-terms-check'
  133    'tools/register-check'
  134    'tools/rules-check'
  135    'tools/box-check'
  136    'tools/release-catalog'
  137    'tools/rc-preflight'
  138    'tools/prose-check'
  139    'tools/pr-stack-check'
  140    'tools/device-act'
  141    'tools/qa-accounts'
  142    'tools/ra-offline-test'
  143    'tools/ra-ui-test'
  144    'tools/raofflineproxy-integration-test'
  145    'tools/raofflineproxy-installed-native-test'
  146    'tools/raofflineproxy-consent-test'
  147    'tools/vm-walks/'
  148    'tools/fork-worktree'
  149    'tools/fork-package-freshness'
  150    'tools/vm-upgrade-rehearsal'
  151    'tools/vm-upgrade-readiness-test'
  152    'tools/frame-diff'
  153    'tools/archaeology'
  154    'tools/work-log-index'
  155    'tools/ceremony-check'
  156    'tools/es-syntax-check'
  157    'tools/png-blackout'
  158    'tools/fork-newdrive'
  159    'tools/council/'
  160    # The council toolchain, scaffold's export at its own paths (.claude/skills/council/COUNCIL-BUNDLE.md)
  161    'scripts/council-'
  162    'scripts/lint-council-'
  163    'scripts/build-council-prompt.ts'
  164    'scripts/write-step-seal.ts'
  165    'scripts/verify-chain.ts'
  166    'scripts/verify-seals.ts'
  167    'scripts/verify-pins.ts'
  168    'scripts/check-stale-blob-drift.ts'
  169    'scripts/setup-council-mistral-tokenizer.mjs'
  170    'scripts/forge-write-status.mjs'
  171    'scripts/owner-queue-lint.mjs'
  172    'scripts/lib/council-'
  173    'scripts/lib/verifier-pins.ts'
  174    'scripts/__tests__/'
  175    'seed/'
  176    'verifier-pins.json'
  177    'council-seat-efforts.json'
  178    # The council's deliberation artifacts (fork issue #70)
  179    'research/'
  180    # Copilot-era artifacts. Retired from `next`, but feature branches and
  181    # worktrees cut before the retirement still contain them, and a PR branch
  182    # built from one of those would carry them upstream. Keep guarding them.
  183    '.github/copilot-instructions.md'
  184    '.github/instructions/'
  185    '.github/shared-copilot-knowledge/'
  186    'tmp/shared-copilot-knowledge/'
  187    'compare-prompt-versions.sh'
  188  )
  189  
  190  zero='0000000000000000000000000000000000000000'
  191  empty_tree="$(git hash-object -t tree /dev/null)"
  192  status=0
  193  
  194  # Lines shaped like credentials, on EVERY branch. GitHub's push protection
  195  # knows its own catalogue of token formats; it does not know a ScreenScraper
  196  # developer password (`devid=..&devpassword=..`) or a RetroAchievements web API
  197  # key (`z=user&y=KEY`), and those are the secrets this fork actually handles
  198  # (~/.ROCKNIX/options, device-builds.md § Build credentials). Names are not
  199  # enough -- `export SCREENSCRAPER_DEV_LOGIN="devid=<id>&devpassword=<..>"` is
  200  # documentation -- so every pattern demands a real-looking value; placeholders
  201  # in <angle brackets> never match.
  202  . "$(dirname "$(readlink -f "$0")")/guard-lib" || exit 1
  203  guard_load pre-push || exit 1
  204  
  205  # A relative hooksPath means pr/* pushes from a worktree run unguarded. We can
  206  # only say so from a push that did reach the hook, which is the point: say it
  207  # here rather than let a silent gap persist.
  208  hooks_path="$(git config --get core.hooksPath || true)"
  209  case "$hooks_path" in
  210    ''|/*) ;;
  211    *) echo "⚠ pre-push: core.hooksPath is relative ('${hooks_path}'), so this guard does" >&2
  212       echo "  not run when pushing a pr/* branch (those branches contain no .githooks/)." >&2
  213       echo "  Fix with: git config core.hooksPath \"\$(git rev-parse --show-toplevel)/.githooks\"" >&2 ;;
  214  esac
  215  
  216  # Pick a clean base to compare PR branches against.
  217  base_ref=''
  218  for cand in upstream/next origin/next; do
  219    if git rev-parse --verify --quiet "${cand}^{commit}" >/dev/null; then
  220      base_ref="$cand"
  221      break
  222    fi
  223  done
  224  
  225  # Do not re-judge commits already published on this destination's other
  226  # branches (#371). An unrelated remote is not evidence that the destination
  227  # has them: excluding every remote used to let unpublished history escape on
  228  # a new branch. A push by URL without a configured remote stays conservative.
  229  history_excludes=()
  230  if [ -n "${1:-}" ] && git remote get-url "$1" >/dev/null 2>&1; then
  231    history_excludes=(--not "--remotes=$1")
  232  fi
  233  
  234  while read -r local_ref local_sha remote_ref remote_sha; do
  235    # Skip branch deletions.
  236    [ "$local_sha" = "$zero" ] && continue
  237  
  238    pushed="${local_ref#refs/heads/}"
  239  
  240    # --- credentials, every branch -------------------------------------------
  241    # Two scans. (1) The files this push adds or changes, read whole at the
  242    # pushed tip, so a secret that slipped in earlier blocks the next push that
  243    # touches its file. (2) Every line ADDED by every commit in the range: a
  244    # value committed and removed again inside one push is in the history being
  245    # pushed and invisible at the tip (audit #151 PL-08). A range this hook
  246    # cannot diff is refused -- a scan that did not run has not passed.
  247    whole=0
  248    if [ "$remote_sha" = "$zero" ]; then
  249      oldest="$(git rev-list "$local_sha" "${history_excludes[@]}" 2>/dev/null | tail -1)"
  250      if [ -n "$oldest" ] && git rev-parse --verify --quiet "${oldest}^" >/dev/null; then
  251        range="${oldest}^..${local_sha}"
  252      elif [ -n "$oldest" ]; then
  253        whole=1                      # the remotes have none of this history: scan all of it
  254      elif git rev-parse --verify --quiet "${local_sha}^" >/dev/null; then
  255        range="${local_sha}^..${local_sha}"
  256      else
  257        whole=1
  258      fi
  259    else
  260      range="${remote_sha}..${local_sha}"
  261    fi
  262    names="$(mktemp)"; added="$(mktemp)"; lines="$(mktemp)"; blob="$(mktemp)"; msgs="$(mktemp)"
  263    trap 'rm -f "${names:-}" "${added:-}" "${lines:-}" "${blob:-}" "${msgs:-}"' EXIT   # an interrupted push leaves nothing behind (the audit of the fixes, claude G3-E-07)
  264    scan_ok=1
  265    msgawk='/^commit [0-9a-f]+$/ { c = $2; n = 0; next } { n++; print c ":message:" n t $0 }'
  266    if [ "$whole" = 1 ]; then
  267      git diff --name-only --no-renames --diff-filter=AM "$empty_tree" "$local_sha" -- . ':!*.po' ':!*.pot' > "$names" 2>/dev/null || scan_ok=0
  268      git log -p --src-prefix=a/ --dst-prefix=b/ --root --no-renames --diff-merges=first-parent --format='commit %h' "$local_sha" "${history_excludes[@]}" -- . ':!*.po' ':!*.pot' > "$added" 2>/dev/null || scan_ok=0
  269      git log --root --format='commit %h%n%B' "$local_sha" "${history_excludes[@]}" 2>/dev/null | awk -v t="$guard_tab" "$msgawk" > "$msgs" || scan_ok=0
  270    else
  271      git diff --name-only --no-renames --diff-filter=AM "$range" -- . ':!*.po' ':!*.pot' > "$names" 2>/dev/null || scan_ok=0
  272      git log -p --src-prefix=a/ --dst-prefix=b/ --no-renames --diff-merges=first-parent --format='commit %h' "$range" "${history_excludes[@]}" -- . ':!*.po' ':!*.pot' > "$added" 2>/dev/null || scan_ok=0
  273      git log --format='commit %h%n%B' "$range" "${history_excludes[@]}" 2>/dev/null | awk -v t="$guard_tab" "$msgawk" > "$msgs" || scan_ok=0
  274    fi
  275    guard_added_lines < "$added" > "$lines" || scan_ok=0
  276    if [ "$scan_ok" != 1 ]; then
  277      rm -f "$names" "$added" "$lines" "$blob" "$msgs"
  278      echo "✗ pre-push: refusing to push ${pushed}: could not diff ${range:-$local_sha} to scan it." >&2
  279      status=1
  280      continue
  281    fi
  282    # Three scans, each against both lists, each failing closed in guard-lib.
  283    # (1) The files this push touches, whole at the tip: a line that reached
  284    #     history before the guard existed blocks the next push that touches
  285    #     its file. (2) Every line ADDED by every commit in the range, merges
  286    #     against their first parent so a conflict resolution is read too. (3)
  287    #     Every commit message in the range. A line is judged after its label
  288    #     -- a file's NAME is not a credential: on 2026-09-25 merging upstream
  289    #     brought an H616 eMMC kernel patch whose file name carried "sk-" and
  290    #     twenty-odd word characters after it (ma-sk-DATA0-...), the OpenAI key
  291    #     shape, and every line of the file was refused for its name; the first
  292    #     cut of this comment spelled the name out and was refused too -- and no
  293    #     path is exempt: the audit-packet exemption of 2026-09-28 went with
  294    #     the audit of the fix round (PL-011, PL-012, PL-026).
  295    hook="pre-push (${pushed})"
  296    refused=0
  297    while IFS= read -r f; do
  298      [ -n "$f" ] || continue
  299      if ! git show "${local_sha}:${f}" 2>/dev/null | guard_numbered "$f" > "$blob"; then
  300        echo "✖ ${hook}: ${f} could not be read at ${local_sha}; nothing was scanned, so nothing is allowed" >&2
  301        refused=1
  302        continue
  303      fi
  304      guard_scan "$hook" "$blob" "${f} carries a credential-shaped line at the pushed tip" '' "$SECRET_PATTERNS" redact || refused=1
  305      guard_scan "$hook" "$blob" "${f} carries a listed word at the pushed tip (the wordlist outside the tree)" -i "$FORBIDDEN_PATTERNS" where || refused=1
  306    done < "$names"
  307    guard_scan "$hook" "$lines" "a commit in this push adds a credential-shaped line" '' "$SECRET_PATTERNS" redact || refused=1
  308    guard_scan "$hook" "$lines" "a commit in this push adds a listed word (the wordlist outside the tree)" -i "$FORBIDDEN_PATTERNS" where || refused=1
  309    guard_scan "$hook" "$msgs" "a commit message in this push carries a credential-shaped line" '' "$SECRET_PATTERNS" redact || refused=1
  310    guard_scan "$hook" "$msgs" "a commit message in this push carries a listed word" -i "$FORBIDDEN_PATTERNS" where || refused=1
  311    rm -f "$names" "$added" "$lines" "$blob" "$msgs"
  312    if [ "$refused" = 1 ]; then
  313      echo "✗ pre-push: refusing to push ${pushed}. Placeholders belong in <angle brackets>; a real value, and a listed word, have to come out of history before this pushes." >&2
  314      status=1
  315      continue
  316    fi
  317  
  318    # --- the ceremonies, next only ---------------------------------------------
  319    # The integration branch carries the record, so a push of it is where the
  320    # record's own checks run: the work-log index current (tools/work-log-index),
  321    # and tools/ceremony-check's blocking set -- a friction entry without an
  322    # issue, a retro past its grace, a missing weekly or monthly summary, a
  323    # blindspot without a guard, the register lint. The long ceremonies (an
  324    # audit, a futro) are reported here and enforced by the fork's CI, so a fix
  325    # can still be pushed while one is owed (#254, D-WORKFLOW-028).
  326    if [ "$remote_ref" = "refs/heads/next" ]; then
  327      if [ "$whole" = 0 ] && git diff --name-only "$range" -- 'docs/work-logs/' 2>/dev/null | grep -qE 'work_log\.md$' \
  328         && ! git diff --name-only "$range" -- 'docs/work-logs/INDEX.md' 2>/dev/null | grep -q .; then
  329        echo "⚠ pre-push: this push changes work logs without docs/work-logs/INDEX.md -- run tools/work-log-index --write and amend." >&2
  330      fi
  331      if [ ! -x "$hooks_root/tools/ceremony-check" ]; then
  332        # A gate that cannot run has not passed (engineering-practices.md).
  333        echo "✗ pre-push: refusing to push next: $hooks_root/tools/ceremony-check is missing or not executable, so the ceremony gate cannot run." >&2
  334        status=1
  335        continue
  336      fi
  337      if true; then
  338        if ! gate_out="$("$hooks_root/tools/ceremony-check" --gate 2>&1)"; then
  339          {
  340            echo "✗ pre-push: refusing to push next: a ceremony is overdue past its grace."
  341            printf '%s\n' "$gate_out" | sed 's/^/    /'
  342            echo "  Write the artifact it names (docs/friction-log.md, docs/retros/, the summary, the index), then push again."
  343          } >&2
  344          status=1
  345          continue
  346        elif [ -n "$gate_out" ]; then
  347          printf '%s\n' "$gate_out" | sed 's/^/  ⚠ pre-push: /' >&2
  348        fi
  349      fi
  350    fi
  351  
  352    # --- personal paths, pr/* only -------------------------------------------
  353    # Keyed on where the push LANDS. `git push origin feature/x:pr/x` used to
  354    # pass here because the local name was not pr/*.
  355    case "$remote_ref" in
  356      refs/heads/pr/*) ;;
  357      *) continue ;;
  358    esac
  359  
  360    dest="${remote_ref#refs/heads/}"
  361    branch="$dest"
  362    [ "$dest" = "$pushed" ] || branch="${dest} (pushed from ${pushed})"
  363  
  364    if [ -z "$base_ref" ]; then
  365      echo "✗ pre-push: refusing to push ${branch}: no upstream/next or origin/next to compare a pr/* branch against." >&2
  366      echo "  git fetch upstream, then push again." >&2
  367      status=1
  368      continue
  369    fi
  370  
  371    # One commit per PR, on the base by itself (D-WORKFLOW-079, #333): the
  372    # ROCKNIX developers closed a series whose tenth branch carried ten
  373    # commits. A count the guard cannot read is a refusal, not a pass.
  374    if ! count="$(git rev-list --count "${base_ref}..${local_sha}" 2>/dev/null)"; then
  375      echo "✗ pre-push: refusing to push ${branch}: git rev-list ${base_ref}..${local_sha} failed, so the one-commit rule could not be checked." >&2
  376      status=1
  377      continue
  378    fi
  379    if [ "$count" != 1 ]; then
  380      echo "✖ pre-push blocked: ${branch} carries ${count} commits past ${base_ref}; a PR branch is one commit built by content (D-WORKFLOW-079)." >&2
  381      echo "  Rebuild it: git worktree add --detach ../rocknix.worktrees/pr-tmp ${base_ref} && git switch -c ${dest} && git checkout next -- <the paths> && git commit" >&2
  382      status=1
  383      continue
  384    fi
  385    # Nothing upstream-bound names an assistant (D-WORKFLOW-078, #333): the
  386    # commit message is scanned here; the PR body is the drafts' scan in
  387    # tools/pr-stack-check, since it is not in the tree the branch carries.
  388    if git log --format=%B "${base_ref}..${local_sha}" 2>/dev/null | grep -q -i -E 'claude|anthropic|generated with|co-authored-by'; then
  389      echo "✖ pre-push blocked: ${branch}'s commit message names an assistant or carries a trailer; nothing upstream-bound may (D-WORKFLOW-078)." >&2
  390      status=1
  391      continue
  392    fi
  393  
  394    # Files that differ between clean upstream and this PR branch tip.
  395    if ! changed="$(git diff --name-only "$base_ref" "$local_sha" 2>/dev/null)"; then
  396      echo "✗ pre-push: refusing to push ${branch}: git diff ${base_ref} ${local_sha} failed, so the personal-path guard could not run." >&2
  397      status=1
  398      continue
  399    fi
  400  
  401    hits=''
  402    while IFS= read -r f; do
  403      [ -z "$f" ] && continue
  404      for pat in "${PERSONAL_PATTERNS[@]}"; do
  405        case "$f" in
  406          "$pat"|"$pat"*) hits+="    $f"$'\n' ;;
  407        esac
  408      done
  409    done <<< "$changed"
  410  
  411    if [ -n "$hits" ]; then
  412      {
  413        echo "✖ pre-push blocked: ${branch} carries personal artifacts that must not go upstream:"
  414        printf '%s' "$hits"
  415        echo "  Rebuild the PR branch from upstream by content, not by commit:"
  416        echo "    git worktree add --detach ../rocknix.worktrees/pr-tmp upstream/next"
  417        echo "    git switch -c ${dest} && git checkout next -- <the feature paths> && git commit"
  418      } >&2
  419      status=1
  420    fi
  421  
  422    # Unlisted-artifact check. Anything that exists only on `next` and lives
  423    # outside the feature areas is very likely a personal artifact nobody
  424    # remembered to add above - today every such file is one. This warns instead
  425    # of blocking, because a genuinely upstream-bound new file reaches a PR
  426    # branch by exactly the same route: features merge into `next` before they
  427    # are PR'd, so being next-only is not proof of being personal.
  428    if git rev-parse --verify --quiet "${base_ref}^{commit}" >/dev/null; then
  429      unlisted=''
  430      while IFS= read -r f; do
  431        [ -z "$f" ] && continue
  432        printf '%s\n' "$changed" | grep -Fxq -- "$f" || continue
  433        listed=0
  434        for pat in "${PERSONAL_PATTERNS[@]}"; do
  435          case "$f" in "$pat"|"$pat"*) listed=1; break ;; esac
  436        done
  437        [ "$listed" -eq 1 ] && continue
  438        unlisted+="    $f"$'\n'
  439      done <<< "$(git diff --name-only --diff-filter=A "$base_ref" next -- \
  440                  . ':!packages' ':!projects' 2>/dev/null)"
  441  
  442      if [ -n "$unlisted" ]; then
  443        {
  444          echo "⚠ pre-push: ${branch} touches files that exist only on next and are not listed"
  445          echo "  in PERSONAL_PATTERNS:"
  446          printf '%s' "$unlisted"
  447          echo "  Personal? Add them to PERSONAL_PATTERNS in .githooks/pre-push."
  448          echo "  Genuinely upstream-bound? Nothing to do."
  449        } >&2
  450      fi
  451    fi
  452  
  453    # Console-first content guard: product surfaces (user-visible script text in
  454    # the cloud/backup tooling) must never mention QA/dev environments. QEMU/VM
  455    # guidance belongs in dev docs and release notes only.
  456    content_hits="$(git diff "$base_ref" "$local_sha" -- \
  457        'projects/ROCKNIX/packages/network/rclone/sources/' \
  458        'projects/ROCKNIX/packages/rocknix/sources/scripts/' \
  459      | grep -E '^\+' | grep -inE 'qemu|virtual machine|user-mode network|port forward|127\.0\.0\.1:15' || true)"
  460    if [ -n "$content_hits" ]; then
  461      {
  462        echo "✖ pre-push blocked: ${branch} adds dev/VM wording to product surfaces (console-first rule):"
  463        printf '%s\n' "$content_hits" | sed 's/^/    /'
  464        echo "  Move QA guidance to dev docs or release notes; product text is handheld+phone only."
  465      } >&2
  466      status=1
  467    fi
  468  done
  469  
  470  exit $status
```

## File: .githooks/guard-lib (at 8ebaf8daad, 107 lines)

```text
    1  # guard-lib -- the scans shared by .githooks/pre-commit, commit-msg and
    2  # pre-push. Sourced, never run. The same file is carried in the
    3  # EmulationStation fork's .githooks/; change both together.
    4  #
    5  # Two lists. SECRET_PATTERNS lives beside this file (.githooks/secret-patterns;
    6  # SECRET_PATTERNS_FILE points a test elsewhere). FORBIDDEN_PATTERNS is a
    7  # wordlist the fork must not carry anywhere -- tree, commit messages, tracker
    8  # -- and it lives OUTSIDE every tree: ~/.config/rocknix/forbidden-terms
    9  # (FORBIDDEN_TERMS_FILE for a test), or FORBIDDEN_PATTERNS already in the
   10  # environment (the fork CI's repository secret). A list of words a tree must
   11  # not hold would itself hold them, so it is never copied into a tree, and a
   12  # refusal names the file and the line, never the word (2026-09-28).
   13  #
   14  # Everything here fails closed (audit of the fix round, PL-011: the first cut
   15  # piped each scan through `|| true`, and a pattern that did not compile let
   16  # every commit through): a list that cannot be read, a pattern that does not
   17  # compile, a grep that exits above 1, a diff or a message that cannot be read
   18  # -- each is a refusal, never an empty scan. A line is judged after its label
   19  # (a path, a commit: PL-026 -- a kernel patch named `...sk-...` was once
   20  # refused for its file name), and no path is exempt (PL-012: an audit packet
   21  # that carries a credential-shaped line is redacted in the packet, as its
   22  # seat outputs were).
   23  
   24  guard_here="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
   25  guard_tab=$'\t'
   26  
   27  # guard_load <hook>: SECRET_PATTERNS and FORBIDDEN_PATTERNS set and compiling,
   28  # or a line on stderr and 1.
   29  guard_load() {
   30    local hook="$1" f p rc
   31    f="${SECRET_PATTERNS_FILE:-${guard_here}/secret-patterns}"
   32    SECRET_PATTERNS=''
   33    [ -r "${f}" ] && . "${f}"
   34    [ -n "${SECRET_PATTERNS:-}" ] || { echo "✖ ${hook}: no credential patterns (${f} missing or empty); nothing is scanned, so nothing is allowed" >&2; return 1; }
   35    if [ -z "${FORBIDDEN_PATTERNS:-}" ]; then
   36      f="${FORBIDDEN_TERMS_FILE:-${HOME}/.config/rocknix/forbidden-terms}"
   37      [ -r "${f}" ] && . "${f}"
   38      [ -n "${FORBIDDEN_PATTERNS:-}" ] || { echo "✖ ${hook}: no wordlist (${f} missing or empty, and FORBIDDEN_PATTERNS unset); nothing is scanned, so nothing is allowed" >&2; return 1; }
   39    fi
   40    for p in "${SECRET_PATTERNS}" "${FORBIDDEN_PATTERNS}"; do
   41      printf '' | grep -E -e "${p}" >/dev/null 2>&1; rc=$?
   42      [ "${rc}" -le 1 ] || { echo "✖ ${hook}: a pattern list does not compile (grep exited ${rc}); nothing is scanned, so nothing is allowed" >&2; return 1; }
   43    done
   44    return 0
   45  }
   46  
   47  # guard_added_lines: stdin is a unified diff (git diff -U0, or git log -p with
   48  # --format='commit %h'); stdout is one "<commit:><path>:<line>TAB<+added line>"
   49  # per added line, the line number the file's after the change. A label never
   50  # holds a tab, so a pattern can only match after it.
   51  # The "+++" header is one only after a "---" header (a content line that
   52  # begins "++ " looks like one otherwise); a quoted path ("b/odd\"name") is
   53  # taken as git prints it; any other header with added lines after it fails
   54  # the scan rather than dropping them (the audit of the fixes, claude G3-E-01,
   55  # gpt G3-E-06). The callers force a/ and b/ prefixes, so diff.noprefix
   56  # cannot blank every path.
   57  guard_added_lines() {
   58    awk -v t="${guard_tab}" '
   59      /^commit [0-9a-f]+$/ { pre = $2 ":"; next }
   60      /^--- / { minus = 1; next }
   61      /^\+\+\+ / {
   62        if (minus) {
   63          minus = 0
   64          if ($0 ~ /^\+\+\+ b\//) f = substr($0, 7)
   65          else if ($0 ~ /^\+\+\+ "b\//) { f = substr($0, 8); sub(/"$/, "", f) }
   66          else if ($0 == "+++ /dev/null") f = ""
   67          else { f = ""; unknown++ }
   68          next
   69        }
   70      }
   71      /^@@ / { minus = 0; match($0, /\+[0-9]+/); n = substr($0, RSTART + 1, RLENGTH - 1) + 0; next }
   72      /^\+/ { minus = 0; if (f != "") print pre f ":" n t $0; else orphan++; n++; next }
   73      /^-/ { next }
   74      /^ / { minus = 0; n++ }
   75      END {
   76        if (unknown || orphan) {
   77          print "guard: " orphan+0 " added line(s) under a header the scan does not read (" unknown+0 " such header(s)); refused rather than skipped" > "/dev/stderr"
   78          exit 1
   79        }
   80      }'
   81  }
   82  
   83  # guard_numbered <label>: stdin is a file; stdout "<label>:<n>TAB<line>".
   84  guard_numbered() {
   85    awk -v t="${guard_tab}" -v l="$1" '{ print l ":" NR t $0 }'
   86  }
   87  
   88  # guard_scan <hook> <file> <what> <-i|''> <patterns> <redact|where>: the text
   89  # after the label of every line of <file>, against the patterns. Returns 0
   90  # when nothing matched; 1 with the first hits on stderr (redact: the match
   91  # replaced by [REDACTED]; where: the label alone -- a listed word is never
   92  # printed); 1 with a note when grep could not run.
   93  guard_scan() {
   94    local hook="$1" file="$2" what="$3" ci="$4" patterns="$5" show="$6" out rc
   95    out="$(grep -a ${ci:+-i} -E -e "^([^${guard_tab}]*${guard_tab})+.*(${patterns})" "${file}" 2>&1)"; rc=$?
   96    case "${rc}" in
   97      1) return 0 ;;
   98      0) echo "✖ ${hook}: ${what}:" >&2
   99         if [ "${show}" = redact ]; then
  100           printf '%s\n' "${out}" | sed -E "s/(${patterns})/[REDACTED]/Ig; s/${guard_tab}/: /" | head -5 | sed 's/^/    /' >&2
  101         else
  102           printf '%s\n' "${out}" | sed -E "s/${guard_tab}.*//" | head -5 | sed 's/^/    /' >&2
  103         fi
  104         return 1 ;;
  105      *) echo "✖ ${hook}: the scan for ${what} could not run (grep exited ${rc}: ${out}); nothing was scanned, so nothing is allowed" >&2; return 1 ;;
  106    esac
  107  }
```

## File: .githooks/secret-patterns (at 8ebaf8daad, 8 lines)

```text
    1  # The credential shapes the fork's guards refuse, one place for both hooks:
    2  # .githooks/pre-commit reads the lines a commit would add, .githooks/pre-push
    3  # reads every line every pushed commit added. A placeholder in <angle brackets>
    4  # never matches by construction -- every pattern demands a real-looking value.
    5  # A test fixture for a scanner is built at run time (printf pieces), never
    6  # written as a literal (2026-09-28, #307: three fixtures a fix stream wrote
    7  # reached history and the range had to be rewritten to push).
    8  SECRET_PATTERNS='devpassword=[A-Za-z0-9._%-]{4,}|[?&]y=[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY|"(access|refresh)_token" *: *"[A-Za-z0-9._-]{16,}|sk-[A-Za-z0-9_-]{24,}|(API_?KEY|TOKEN|SECRET|PASSWORD|PASSWD)[A-Z_]* *[:=] *["'"'"']?[A-Za-z0-9+/=_-]{16,}'
```

## File: .githooks/pre-commit (at 8ebaf8daad, 21 lines)

```text
    1  #!/bin/bash
    2  # pre-commit: refuse a commit that would ADD a credential-shaped line -- so
    3  # the push guard never meets one in history (2026-09-28, #307: a fixture
    4  # written as a literal cost a history rewrite) -- or a word from the wordlist
    5  # the fork must not carry (kept outside the tree; .githooks/guard-lib says
    6  # where). Reads the index, not the working tree, so what is refused is exactly
    7  # what would be committed. The scans are guard-lib's and fail closed there.
    8  set -uo pipefail
    9  . "$(dirname "$(readlink -f "$0")")/guard-lib" || exit 1
   10  guard_load pre-commit || exit 1
   11  added="$(mktemp)" || { echo "✖ pre-commit: mktemp failed; nothing was scanned, so nothing is allowed" >&2; exit 1; }
   12  trap 'rm -f "${added}"' EXIT
   13  if ! git diff --cached -U0 --no-color --src-prefix=a/ --dst-prefix=b/ --diff-filter=ACMRT -- . ':!*.po' ':!*.pot' | guard_added_lines > "${added}"; then
   14    echo "✖ pre-commit: could not read the index (git diff --cached failed); nothing was scanned, so nothing is allowed" >&2
   15    exit 1
   16  fi
   17  status=0
   18  guard_scan pre-commit "${added}" "this commit would add a credential-shaped line" '' "${SECRET_PATTERNS}" redact || status=1
   19  guard_scan pre-commit "${added}" "this commit would add a listed word (the wordlist outside the tree; the file and line above)" -i "${FORBIDDEN_PATTERNS}" where || status=1
   20  [ "${status}" -eq 0 ] || echo "  A placeholder belongs in <angle brackets>; a scanner's fixture is built at run time (printf pieces), never written as a literal; a listed word is reworded, never exempted." >&2
   21  exit "${status}"
```

## File: .githooks/commit-msg (at 8ebaf8daad, 25 lines)

```text
    1  #!/bin/bash
    2  # commit-msg: the message, against the same two lists as the tree. A message
    3  # is in history for good and is the one place pre-commit does not reach; the
    4  # push guard reads the messages of a range too, but a refusal here costs one
    5  # edit and there it costs a rewrite. Comment lines are dropped as git drops
    6  # them. Fails closed in .githooks/guard-lib (2026-09-28).
    7  set -uo pipefail
    8  . "$(dirname "$(readlink -f "$0")")/guard-lib" || exit 1
    9  guard_load commit-msg || exit 1
   10  lines="$(mktemp)" || { echo "✖ commit-msg: mktemp failed; refused" >&2; exit 1; }
   11  trap 'rm -f "${lines}"' EXIT
   12  # The message file must be readable (an unreadable one passed, the audit of
   13  # the fixes, claude G3-E-02 / gpt G3-E-05); grep's 1 means "only comments or
   14  # empty", which git refuses on its own -- anything else is a failure, refused.
   15  [ -r "${1:-}" ] || { echo "✖ commit-msg: the message file is unreadable; refused" >&2; exit 1; }
   16  filtered="$(mktemp)" || { echo "✖ commit-msg: mktemp failed; refused" >&2; exit 1; }
   17  trap 'rm -f "${lines}" "${filtered}"' EXIT
   18  grep -v -a -E '^#' -- "$1" > "${filtered}"; grc=$?
   19  [ "${grc}" -le 1 ] || { echo "✖ commit-msg: grep could not read the message (exit ${grc}); refused" >&2; exit 1; }
   20  [ "${grc}" -eq 1 ] && exit 0
   21  guard_numbered message < "${filtered}" > "${lines}" || { echo "✖ commit-msg: the message could not be numbered; refused" >&2; exit 1; }
   22  status=0
   23  guard_scan commit-msg "${lines}" "the commit message carries a credential-shaped line" '' "${SECRET_PATTERNS}" redact || status=1
   24  guard_scan commit-msg "${lines}" "the commit message carries a listed word (the wordlist outside the tree)" -i "${FORBIDDEN_PATTERNS}" where || status=1
   25  exit "${status}"
```

## File: .githooks/hooks-test (at 8ebaf8daad, 120 lines)

```text
    1  #!/bin/bash
    2  # hooks-test -- the fork guards' own test: pre-commit, commit-msg and pre-push
    3  # against the shapes they exist to refuse, in a scratch repository, with a
    4  # stand-in wordlist (FORBIDDEN_TERMS_FILE) and a credential fixture built at
    5  # run time -- neither the real list nor a literal secret is in this file, so
    6  # the guards can commit their own proof (2026-09-28, #312; the ES fork's is
    7  # .githooks/pre-push-test).
    8  #   .githooks/hooks-test          # every case ok, then PASS (exit 0), or FAIL (1)
    9  set -u
   10  HOOKS="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
   11  SCRATCH="$(mktemp -d)" || exit 2
   12  trap 'rm -rf "${SCRATCH}"' EXIT
   13  FAKE="$(printf 'dev%s=%s' password QwErTyUiOpAsDfGh)"       # credential-shaped, means nothing
   14  KEYNAME="sk-$(printf 'A%.0s' $(seq 1 24)).patch"             # a FILE NAME shaped like a key
   15  printf "FORBIDDEN_PATTERNS='zebrafish[ ]quartet|qzx-estate'\\n" > "${SCRATCH}/wordlist"
   16  printf "SECRET_PATTERNS='['\\n" > "${SCRATCH}/badlist"
   17  export FORBIDDEN_TERMS_FILE="${SCRATCH}/wordlist"
   18  unset FORBIDDEN_PATTERNS SECRET_PATTERNS_FILE
   19  ZERO=0000000000000000000000000000000000000000
   20  fail=0
   21  mkdir -p "${SCRATCH}/nohooks"
   22  g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${SCRATCH}/nohooks" "$@"; }
   23  
   24  # expect <refused|allowed> <case> <command...>
   25  expect() {
   26    local want="$1" name="$2" rc; shift 2
   27    "$@" >"${SCRATCH}/out" 2>&1; rc=$?
   28    if { [ "${want}" = refused ] && [ "${rc}" -ne 0 ]; } || { [ "${want}" = allowed ] && [ "${rc}" -eq 0 ]; }; then
   29      echo "  ok    ${name}: ${want}"
   30    else
   31      echo "  FAIL  ${name}: expected ${want}, exited ${rc}"; sed 's/^/          /' "${SCRATCH}/out"; fail=1
   32    fi
   33  }
   34  says()   { if grep -q -F -- "$2" "${SCRATCH}/out"; then echo "  ok    $1: says \"$2\""; else echo "  FAIL  $1: expected \"$2\""; sed 's/^/          /' "${SCRATCH}/out"; fail=1; fi; }
   35  silent() { if grep -q -i -F -- "$2" "${SCRATCH}/out"; then echo "  FAIL  $1: the output carries \"$2\""; sed 's/^/          /' "${SCRATCH}/out"; fail=1; else echo "  ok    $1: never prints the word"; fi; }
   36  push_line() { printf '%s\n' "$1" | "${HOOKS}/pre-push" origin "file://${SCRATCH}/remote.git"; }
   37  
   38  cd "${SCRATCH}" && git init -q -b main work && cd work || exit 2
   39  git init -q --bare "${SCRATCH}/remote.git" && git remote add origin "${SCRATCH}/remote.git"
   40  
   41  echo '--- pre-commit'
   42  echo 'plain line' > a.txt; g add a.txt
   43  expect allowed "a clean file" "${HOOKS}/pre-commit"
   44  g commit -q -m base
   45  echo "${FAKE}" > b.txt; g add b.txt
   46  expect refused "a credential-shaped line" "${HOOKS}/pre-commit"
   47  says "the value is redacted" "[REDACTED]"
   48  silent "the refusal" "QwErTyUiOpAsDfGh"
   49  g reset -q; rm b.txt
   50  mkdir -p docs/audits/x/seats; echo "${FAKE}" > docs/audits/x/seats/y.diff; g add docs
   51  expect refused "the same line under an audit packet (no path is exempt)" "${HOOKS}/pre-commit"
   52  g reset -q; rm -r docs
   53  echo 'the zebrafish quartet played' > c.txt; g add c.txt
   54  expect refused "a listed word" "${HOOKS}/pre-commit"
   55  says "the refusal names the file and line" "c.txt:1"
   56  silent "the refusal" "zebrafish"
   57  g reset -q; rm c.txt
   58  printf 'one\nThe Zebrafish Quartet\n' > d.txt; g add d.txt
   59  expect refused "a listed word in another case, on line 2" "${HOOKS}/pre-commit"
   60  says "line 2 is named" "d.txt:2"
   61  g reset -q; rm d.txt
   62  # The three shapes the audit of the fixes found the scan skipping (claude
   63  # G3-E-01, gpt G3-E-06): a repository with diff.noprefix, a content line
   64  # that begins "++ ", and a file name git prints in quotes.
   65  g config diff.noprefix true; echo "${FAKE}" > f.txt; g add f.txt
   66  expect refused "a credential-shaped line with diff.noprefix set (the scan forces its prefixes)" "${HOOKS}/pre-commit"
   67  g config --unset diff.noprefix; g reset -q; rm f.txt
   68  printf '++ note\n%s\n' "${FAKE}" > h.txt; g add h.txt
   69  expect refused "a content line beginning ++ does not end the file's scan" "${HOOKS}/pre-commit"
   70  says "line 2 is named" "h.txt:2"
   71  g reset -q; rm h.txt
   72  echo "${FAKE}" > 'odd"name.txt'; g add 'odd"name.txt'
   73  expect refused "a file name git prints in quotes is still scanned" "${HOOKS}/pre-commit"
   74  g reset -q; rm 'odd"name.txt'
   75  echo 'clean content' > "${KEYNAME}"; g add "${KEYNAME}"
   76  expect allowed "a file NAMED like a key, clean inside (the label is not scanned)" "${HOOKS}/pre-commit"
   77  g commit -q -m named
   78  echo 'plain' > e.txt; g add e.txt
   79  SECRET_PATTERNS_FILE="${SCRATCH}/badlist" expect refused "a credential list that does not compile" "${HOOKS}/pre-commit"
   80  says "it says so" "does not compile"
   81  FORBIDDEN_TERMS_FILE="${SCRATCH}/absent" expect refused "no wordlist at all" "${HOOKS}/pre-commit"
   82  FORBIDDEN_TERMS_FILE="${SCRATCH}/absent" FORBIDDEN_PATTERNS='zebrafish[ ]quartet' expect allowed "the wordlist from the environment instead (CI)" "${HOOKS}/pre-commit"
   83  GIT_DIR="${SCRATCH}/no-such-repo" expect refused "an index that cannot be read" "${HOOKS}/pre-commit"
   84  g reset -q; rm e.txt
   85  
   86  echo '--- commit-msg'
   87  printf 'tidy the qzx-estate notes\n' > "${SCRATCH}/msg"
   88  expect refused "a listed word in the message" "${HOOKS}/commit-msg" "${SCRATCH}/msg"
   89  silent "the refusal" "qzx-estate"
   90  printf 'tidy the notes\n\n# a comment line naming the zebrafish quartet is not the message\n' > "${SCRATCH}/msg"
   91  expect allowed "a clean message (git drops the # comment)" "${HOOKS}/commit-msg" "${SCRATCH}/msg"
   92  printf 'note\n\n%s\n' "${FAKE}" > "${SCRATCH}/msg"
   93  expect refused "a credential-shaped line in the message" "${HOOKS}/commit-msg" "${SCRATCH}/msg"
   94  expect refused "a message file that cannot be read (claude G3-E-02 / gpt G3-E-05)" "${HOOKS}/commit-msg" "${SCRATCH}/no-such-msg"
   95  FORBIDDEN_TERMS_FILE="${SCRATCH}/absent" expect refused "a message with no wordlist to judge it by" "${HOOKS}/commit-msg" "${SCRATCH}/msg"
   96  
   97  echo '--- pre-push'
   98  g push -q origin main; remote="$(git rev-parse HEAD)"
   99  g checkout -q -b mid "${remote}"; echo 'zebrafish quartet' > f.txt; g add f.txt; g commit -q -m mid; rm f.txt; g add -A; g commit -q -m tip
  100  expect refused "a listed word in a middle commit, gone at the tip" push_line "refs/heads/mid $(git rev-parse HEAD) refs/heads/mid ${ZERO}"
  101  silent "the refusal" "zebrafish"
  102  g checkout -q -b msg "${remote}"; g commit -q --allow-empty -m 'about the qzx-estate'
  103  expect refused "a listed word in a commit message" push_line "refs/heads/msg $(git rev-parse HEAD) refs/heads/msg ${ZERO}"
  104  says "the message is named" ":message:1"
  105  g checkout -q -b sec "${remote}"; echo "${FAKE}" > s.txt; g add s.txt; g commit -q -m s; echo clean > s.txt; g add s.txt; g commit -q -m s2
  106  expect refused "a credential in a middle commit, gone at the tip" push_line "refs/heads/sec $(git rev-parse HEAD) refs/heads/sec ${ZERO}"
  107  says "the value is redacted" "[REDACTED]"
  108  g checkout -q -b old "${remote}"; echo 'zebrafish quartet' > t.txt; g add t.txt; g commit -q -m old; g push -q origin old; prev="$(git rev-parse HEAD)"
  109  echo more >> t.txt; g add t.txt; g commit -q -m touch
  110  expect refused "an older line in a file the range only touches beside (the tip scan)" push_line "refs/heads/old $(git rev-parse HEAD) refs/heads/old ${prev}"
  111  g checkout -q -b quoted "${remote}"; g config diff.noprefix true; echo "${FAKE}" > 'odd"name.txt'; g add 'odd"name.txt'; g commit -q -m quoted
  112  expect refused "a credential in a file git prints in quotes, pushed from a clone with diff.noprefix" push_line "refs/heads/quoted $(git rev-parse HEAD) refs/heads/quoted ${ZERO}"
  113  g config --unset diff.noprefix
  114  g checkout -q -b clean "${remote}"; echo more >> a.txt; echo more >> "${KEYNAME}"; g add -A; g commit -q -m clean
  115  expect allowed "a clean commit, touching the file named like a key" push_line "refs/heads/clean $(git rev-parse HEAD) refs/heads/clean ${ZERO}"
  116  SECRET_PATTERNS_FILE="${SCRATCH}/badlist" expect refused "a credential list that does not compile" push_line "refs/heads/clean $(git rev-parse HEAD) refs/heads/clean ${ZERO}"
  117  FORBIDDEN_TERMS_FILE="${SCRATCH}/absent" expect refused "no wordlist at all" push_line "refs/heads/clean $(git rev-parse HEAD) refs/heads/clean ${ZERO}"
  118  expect refused "a tip this clone does not have" push_line "refs/heads/clean 1234567890123456789012345678901234567890 refs/heads/clean ${ZERO}"
  119  
  120  if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
```

## File: tools/forbidden-terms-check (at 8ebaf8daad, 50 lines)

```text
    1  #!/bin/bash
    2  # forbidden-terms-check: every tracked file of a tree, or the lines on stdin,
    3  # against the wordlist the fork must not carry (2026-09-28). The list lives
    4  # outside every tree -- ~/.config/rocknix/forbidden-terms (FORBIDDEN_TERMS_FILE),
    5  # or FORBIDDEN_PATTERNS in the environment (the fork CI's repository secret) --
    6  # because a list of words a tree must not hold would itself hold them. A hit is
    7  # printed as path:line, never the text.
    8  #   tools/forbidden-terms-check                     # this tree
    9  #   tools/forbidden-terms-check <dir>               # another git tree (the ES fork)
   10  #   git log --format=%B a..b | tools/forbidden-terms-check --stdin   # commit messages
   11  # Exit 0 with no hit; 1 with hits; 2 when it could not run -- the list
   12  # unreadable or not compiling, git ls-files failing, a grep dying. Fails closed.
   13  set -uo pipefail
   14  if [ -z "${FORBIDDEN_PATTERNS:-}" ]; then
   15    f="${FORBIDDEN_TERMS_FILE:-${HOME}/.config/rocknix/forbidden-terms}"
   16    [ -r "${f}" ] || { echo "forbidden-terms-check: no wordlist (${f} unreadable, FORBIDDEN_PATTERNS unset)" >&2; exit 2; }
   17    . "${f}"
   18  fi
   19  [ -n "${FORBIDDEN_PATTERNS:-}" ] || { echo "forbidden-terms-check: FORBIDDEN_PATTERNS is empty" >&2; exit 2; }
   20  printf '' | grep -i -E -e "${FORBIDDEN_PATTERNS}" >/dev/null 2>&1; rc=$?
   21  [ "${rc}" -le 1 ] || { echo "forbidden-terms-check: the pattern does not compile (grep exited ${rc})" >&2; exit 2; }
   22  
   23  if [ "${1:-}" = --stdin ]; then
   24    n="$(grep -a -i -c -E -e "${FORBIDDEN_PATTERNS}" -)"; rc=$?
   25    [ "${rc}" -le 1 ] || { echo "forbidden-terms-check: could not read stdin (grep exited ${rc})" >&2; exit 2; }
   26    if [ "${n}" -gt 0 ]; then echo "forbidden-terms-check: ${n} line(s) on stdin carry a listed word"; exit 1; fi
   27    echo "forbidden-terms-check: 0 hits on stdin"; exit 0
   28  fi
   29  
   30  TREE="${1:-$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)}"
   31  list="$(mktemp)" || exit 2
   32  trap 'rm -f "${list}"' EXIT
   33  git -C "${TREE}" ls-files -z > "${list}" || { echo "forbidden-terms-check: git ls-files failed in ${TREE}" >&2; exit 2; }
   34  hits=0; scanned=0
   35  while IFS= read -r -d '' f; do
   36    p="${TREE}/${f}"
   37    [ -f "${p}" ] && [ ! -L "${p}" ] || continue        # a submodule, a symlink, a path deleted but tracked
   38    scanned=$((scanned + 1))
   39    out="$(grep -a -i -n -E -e "${FORBIDDEN_PATTERNS}" -- "${p}" 2>&1)"; rc=$?
   40    case "${rc}" in
   41      1) ;;
   42      0) while IFS= read -r ln; do echo "${f}:${ln%%:*}"; hits=$((hits + 1)); done <<< "${out}" ;;
   43      *) echo "forbidden-terms-check: grep failed on ${f} (rc ${rc})" >&2; exit 2 ;;
   44    esac
   45  done < "${list}"
   46  if [ "${hits}" -gt 0 ]; then
   47    echo "forbidden-terms-check: ${hits} hit(s) in ${scanned} tracked files (path:line above; the words are never printed)"
   48    exit 1
   49  fi
   50  echo "forbidden-terms-check: 0 hits in ${scanned} tracked files"
```

## File: tools/fork-worktree (at 8ebaf8daad, 309 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Remove a worktree without destroying a build root.
    6  #
    7  # `git worktree remove --force` treats every worktree alike. In this repo they
    8  # are not alike: a feature worktree is a few hundred MB of checkout, while a
    9  # build worktree holds build.ROCKNIX-<DEVICE>.<ARCH> directories that cost
   10  # hours each and are not in git. The command that cleans up the first silently
   11  # targets the second, and --force is the flag you reach for when the first
   12  # attempt complains.
   13  #
   14  # It is also not reliably atomic. Told to force-remove a worktree holding
   15  # hundreds of GB, git unregistered it and left the contents behind - a
   16  # directory that is no longer a worktree, whose build roots are now orphaned,
   17  # reported only as a non-zero exit nobody reads in a loop.
   18  #
   19  #   ./tools/fork-worktree list                    # what each worktree is holding
   20  #   ./tools/fork-worktree remove <path>           # refuses if build output is present
   21  #   ./tools/fork-worktree remove <path> --preserve <dir>   # move build output out first
   22  #   ./tools/fork-worktree remove <path> --force   # destroy it anyway, having been told
   23  #   ./tools/fork-worktree repair <path>           # re-register an orphaned directory
   24  #   ./tools/fork-worktree sync                    # fast-forward every build/* worktree to next
   25  set -uo pipefail
   26  
   27  # Every git read below is about the repository this tool lives in, never the
   28  # one the shell happens to be standing in. Run with the shell inside the
   29  # EmulationStation repo (2026-09-12) it read that repo's config, warned that
   30  # the pre-push guard was unset, listed that repo's worktrees and synced
   31  # nothing -- while saying nothing untrue about the repo it looked at.
   32  ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
   33  
   34  # The gitignored build outputs, per CLAUDE.md. Presence of any of these means
   35  # the directory is worth more than the checkout it sits in.
   36  is_build_artifact() {
   37      case "${1}" in
   38          build.*|target|sources|release) return 0 ;;
   39          *) return 1 ;;
   40      esac
   41  }
   42  
   43  # du over a 345 GB tree is slow and cold-cache slower. The refusal does not
   44  # depend on the number, so treat it as a nicety that is allowed to give up.
   45  cheap_size() {
   46      local out
   47      out="$(timeout 10 du -sh "${1}" 2>/dev/null | cut -f1)"
   48      [ -n "${out}" ] && echo "${out}" || echo "too large to measure in 10s"
   49  }
   50  
   51  artifacts_in() {
   52      local wt="${1}" found=""
   53      for entry in "${wt}"/* ; do
   54          [ -e "${entry}" ] || continue
   55          local base; base="$(basename "${entry}")"
   56          is_build_artifact "${base}" && found+="${base}"$'\n'
   57      done
   58      printf '%s' "${found}"
   59  }
   60  
   61  git_dir() { git -C "${ROOT}" rev-parse --git-common-dir 2>/dev/null; }
   62  
   63  # The pre-push guard is installed by absolute path (see .githooks/pre-push for
   64  # why). Git says nothing when that path stops existing -- it just runs no
   65  # hooks -- which is what happened for a day after the tree moved to /workspace.
   66  # This runs from the two subcommands people actually use, so the gap is loud.
   67  check_hooks_path() {
   68      local hp
   69      hp="$(git -C "${ROOT}" config --get core.hooksPath 2>/dev/null || true)"
   70      case "${hp}" in
   71          '')  echo "⚠ core.hooksPath is not set: the pre-push guard is not running." >&2
   72               echo "  git config core.hooksPath /workspace/repos/rocknix/.githooks" >&2 ;;
   73          /*)  [ -d "${hp}" ] || { echo "⚠ core.hooksPath names a directory that does not exist (${hp}): the pre-push guard is not running." >&2
   74                                   echo "  git config core.hooksPath /workspace/repos/rocknix/.githooks" >&2; } ;;
   75          *)   echo "⚠ core.hooksPath is relative (${hp}); pr/* pushes from a worktree run unguarded." >&2 ;;
   76      esac
   77  }
   78  
   79  cmd_list() {
   80      check_hooks_path
   81      git -C "${ROOT}" worktree list --porcelain | awk '/^worktree /{print $2}' | while read -r wt; do
   82          local_art="$(artifacts_in "${wt}")"
   83          if [ -n "${local_art}" ]; then
   84              echo "  ${wt}"
   85              echo "      HOLDS BUILD OUTPUT ($(cheap_size "${wt}")):"
   86              printf '%s\n' "${local_art}" | sed 's/^/        /'
   87          else
   88              echo "  ${wt}"
   89              echo "      checkout only"
   90          fi
   91      done
   92  }
   93  
   94  # Go's downloaded modules contain owner-owned 0555 directories. Git starts
   95  # deleting before it encounters them, then unregisters the partially removed
   96  # tree even on failure (#460). Inspect the entire directory tree first, then
   97  # grant only the directory owner's write/search bits needed for this removal.
   98  # File permissions and symlink targets are never changed.
   99  prepare_forced_removal() {
  100      python3 - "${1}" <<'PY'
  101  import os
  102  import stat
  103  import sys
  104  import time
  105  
  106  def fail(error):
  107      raise error
  108  
  109  root = os.open(sys.argv[1], os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
  110  try:
  111      device = os.fstat(root).st_dev
  112      pending = {}
  113      count = 0
  114      last = time.monotonic()
  115      for path, dirs, files, fd in os.fwalk('.', dir_fd=root,
  116                                           follow_symlinks=False, onerror=fail):
  117          info = os.fstat(fd)
  118          if info.st_dev != device:
  119              raise RuntimeError('refusing removal across a filesystem: ' + path)
  120          # An empty directory is removed through its parent; its own write bit
  121          # is irrelevant. Docker may leave an empty root-owned sources mountpoint.
  122          if (dirs or files) and not os.access('.', os.W_OK | os.X_OK, dir_fd=fd):
  123              if info.st_uid != os.geteuid():
  124                  raise PermissionError('directory is not writable or owned by this user: ' + path)
  125              pending[path] = (info.st_dev, info.st_ino, stat.S_IMODE(info.st_mode))
  126          count += 1
  127          if time.monotonic() - last >= 10:
  128              print('  inspected removal permissions:', count, 'directories', flush=True)
  129              last = time.monotonic()
  130      changed = 0
  131      if pending:
  132          for path, dirs, files, fd in os.fwalk('.', dir_fd=root,
  133                                               follow_symlinks=False, onerror=fail):
  134              if path not in pending:
  135                  continue
  136              info = os.fstat(fd)
  137              expected = pending.pop(path)
  138              if (info.st_dev, info.st_ino, stat.S_IMODE(info.st_mode)) != expected:
  139                  raise RuntimeError('directory changed during permission inspection: ' + path)
  140              if info.st_uid != os.geteuid():
  141                  raise PermissionError('directory ownership changed: ' + path)
  142              os.fchmod(fd, expected[2] | stat.S_IWUSR | stat.S_IXUSR)
  143              changed += 1
  144          if pending:
  145              raise RuntimeError('directories disappeared during permission inspection')
  146      print('  removal permissions:', count, 'directories checked;', changed,
  147            'owner-write/search repairs', flush=True)
  148  except (OSError, RuntimeError) as error:
  149      print('error: removal permission preflight failed:', error, file=sys.stderr)
  150      sys.exit(1)
  151  finally:
  152      os.close(root)
  153  PY
  154  }
  155  
  156  cmd_remove() {
  157      local wt="" preserve="" force=0
  158      while [ $# -gt 0 ]; do
  159          case "${1}" in
  160              --preserve) preserve="${2:-}"; shift 2 ;;
  161              --force) force=1; shift ;;
  162              *) wt="${1}"; shift ;;
  163          esac
  164      done
  165      [ -n "${wt}" ] || { echo "usage: fork-worktree remove <path> [--preserve <dir>] [--force]" >&2; exit 1; }
  166      wt="$(cd "${wt}" 2>/dev/null && pwd)" || { echo "error: no such directory" >&2; exit 1; }
  167  
  168      # Refusing to delete the ground you are standing on: the shell's cwd would
  169      # vanish mid-command and every later step would fail for an unrelated-looking
  170      # reason.
  171      local here; here="$(pwd -P)"
  172      case "${here}/" in
  173          "${wt}"/*) echo "error: you are inside ${wt}; run this from elsewhere" >&2; exit 1 ;;
  174      esac
  175  
  176      local art; art="$(artifacts_in "${wt}")"
  177      if [ -n "${art}" ] && [ -z "${preserve}" ] && [ "${force}" -eq 0 ]; then
  178          {
  179              echo "refusing: ${wt} holds build output that is not in git ($(cheap_size "${wt}")):"
  180              printf '%s\n' "${art}" | sed 's/^/    /'
  181              echo "  Each build.* directory is hours of work and cannot be recovered from a clone."
  182              echo "  Keep it:     fork-worktree remove ${wt} --preserve <dir>"
  183              echo "  Destroy it:  fork-worktree remove ${wt} --force"
  184          } >&2
  185          exit 1
  186      fi
  187  
  188      if [ -n "${preserve}" ]; then
  189          mkdir -p "${preserve}" || exit 1
  190          while IFS= read -r base; do
  191              [ -n "${base}" ] || continue
  192              mv "${wt}/${base}" "${preserve}/${base}" && echo "  preserved: ${base} -> ${preserve}/"
  193          done <<< "${art}"
  194      elif [ -n "${art}" ]; then
  195          echo "  destroying build output as instructed:"; printf '%s\n' "${art}" | sed 's/^/    /'
  196      fi
  197  
  198      if [ "${force}" -eq 1 ]; then
  199          prepare_forced_removal "${wt}" || exit 1
  200      fi
  201      git worktree remove --force "${wt}"
  202      local rc=$?
  203  
  204      # git can unregister and still leave the directory. Say so plainly rather
  205      # than letting a non-zero exit disappear into a loop.
  206      if [ -d "${wt}" ]; then
  207          echo "warning: ${wt} still exists on disk after removal (git exit ${rc})." >&2
  208          echo "  It is no longer a registered worktree. Re-register it with:" >&2
  209          echo "    fork-worktree repair ${wt}" >&2
  210          exit 1
  211      fi
  212      [ "${rc}" -eq 0 ] || exit "${rc}"
  213      echo "  removed: ${wt}"
  214  }
  215  
  216  # The recovery for a directory git unregistered but did not delete: stand up a
  217  # fresh worktree at the same path and carry every untracked thing back.
  218  cmd_repair() {
  219      local wt="${1:-}" ref="${2:-next}"
  220      [ -n "${wt}" ] || { echo "usage: fork-worktree repair <path> [ref]" >&2; exit 1; }
  221      wt="$(cd "${wt}" 2>/dev/null && pwd)" || { echo "error: no such directory" >&2; exit 1; }
  222      if git -C "${ROOT}" worktree list --porcelain | awk '/^worktree /{print $2}' | grep -qxF "${wt}"; then
  223          echo "  ${wt} is already a registered worktree; nothing to repair"; exit 0
  224      fi
  225      local orphan="${wt}.orphan.$$"
  226      mv "${wt}" "${orphan}" || exit 1
  227      if ! git worktree add -q --detach "${wt}" "${ref}"; then
  228          mv "${orphan}" "${wt}"; echo "error: could not create worktree; directory restored" >&2; exit 1
  229      fi
  230      local moved=0
  231      for entry in "${orphan}"/* "${orphan}"/.[!.]*; do
  232          [ -e "${entry}" ] || continue
  233          local base; base="$(basename "${entry}")"
  234          [ "${base}" = ".git" ] && continue
  235          [ -e "${wt}/${base}" ] && continue          # tracked file the checkout just restored
  236          mv "${entry}" "${wt}/${base}" && moved=$((moved + 1))
  237      done
  238      rmdir "${orphan}" 2>/dev/null || rm -rf "${orphan}"
  239      echo "  repaired: ${wt} at ${ref}, ${moved} untracked item(s) carried over"
  240  }
  241  
  242  # Bring every build worktree up to next. A branch does not follow next by
  243  # itself any more than a detached HEAD does, so this is the step that would
  244  # otherwise be three manual checkouts nobody remembers to run before a build.
  245  #
  246  # Only build/* branches are touched. A feature branch has work on it and is
  247  # nobody's to fast-forward; next itself is the thing being followed.
  248  cmd_sync() {
  249      check_hooks_path
  250      # No target argument on purpose. This walks every build worktree, so an
  251      # arbitrary ref moves all of them at once -- which is exactly how, while
  252      # testing this function, a throwaway commit was fast-forwarded onto two real
  253      # build checkouts without anyone noticing. The only ref worth following here
  254      # is next; testing against something else is not worth that edge.
  255      local target="next" rc=0
  256      git -C "${ROOT}" worktree list --porcelain | awk '/^worktree /{print $2}' | while read -r wt; do
  257          local br; br="$(git -C "${wt}" branch --show-current)"
  258          case "${br}" in
  259              build/*) ;;
  260              "")  echo "  skip ${wt##*/}: detached HEAD, not a build worktree"; continue ;;
  261              *)   echo "  skip ${wt##*/}: on ${br}, not a build/* branch"; continue ;;
  262          esac
  263          # A build rewrites a tracked doc as one of its outputs
  264          # (documentation/PER_DEVICE_DOCUMENTATION/<DEVICE>/SUPPORTED_EMULATORS_AND_CORES.md),
  265          # so every build worktree is "dirty" after every build, and the skip
  266          # below refused to move both of them on 2026-09-11 -- the next image
  267          # was built from the old tree, and only noticed because BUILD_ID did
  268          # not change. That file is not a change anyone made here: put it
  269          # back before asking whether the tree is clean. Never run under a
  270          # build (see the header) -- the build would rewrite it again anyway.
  271          git -C "${wt}" checkout -q -- 'documentation/PER_DEVICE_DOCUMENTATION/*/SUPPORTED_EMULATORS_AND_CORES.md' 2>/dev/null || true
  272          if [ -n "$(git -C "${wt}" status --porcelain=v1 --untracked-files=no)" ]; then
  273              # Name the files: the skip read as a mystery until someone ran
  274              # git status by hand (2026-09-07).
  275              echo "  SKIP ${wt##*/}: uncommitted changes on ${br} - resolve them first:" >&2
  276              git -C "${wt}" status --porcelain=v1 --untracked-files=no | sed 's/^/        /' >&2
  277              continue
  278          fi
  279          # --ff-only: if someone committed on the build branch it has diverged,
  280          # and quietly rewriting it would lose that work.
  281          local before; before="$(git -C "${wt}" rev-parse HEAD)"
  282          if git -C "${wt}" merge --ff-only "${target}" >/dev/null 2>&1; then
  283              local after; after="$(git -C "${wt}" rev-parse HEAD)"
  284              if [ "${before}" = "${after}" ]; then
  285                  # Either already at target, or ahead of it. Say so: reporting a
  286                  # move that did not happen is how a stale checkout gets built.
  287                  if git -C "${wt}" merge-base --is-ancestor "${target}" HEAD 2>/dev/null &&
  288                     [ "$(git -C "${wt}" rev-parse "${target}")" != "${after}" ]; then
  289                      echo "  ${wt##*/}: ${br} is AHEAD of ${target}; left alone"
  290                  else
  291                      echo "  ${wt##*/}: ${br} already at ${target}"
  292                  fi
  293              else
  294                  echo "  ${wt##*/}: ${br} fast-forwarded to $(git -C "${wt}" rev-parse --short HEAD)"
  295              fi
  296          else
  297              echo "  FAILED ${wt##*/}: ${br} has diverged from ${target}; not fast-forwarding" >&2
  298          fi
  299      done
  300      return ${rc}
  301  }
  302  
  303  case "${1:-}" in
  304      list)   shift; cmd_list "$@" ;;
  305      remove) shift; cmd_remove "$@" ;;
  306      repair) shift; cmd_repair "$@" ;;
  307      sync)   cmd_sync ;;
  308      *) echo "usage: ${0##*/} {list|sync|remove <path> [--preserve <dir>] [--force]|repair <path> [ref]}" >&2; exit 1 ;;
  309  esac
```

## File: .github/scripts/generate-changelog.sh (at 8ebaf8daad, 98 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
    4  
    5  set -o pipefail
    6  
    7  GIT_RANGE="${1}"
    8  MAX_COUNT="${2}"
    9  
   10  if [ -z "${GIT_RANGE}" ]; then
   11    echo "ERROR: no git range provided" >&2
   12    exit 1
   13  fi
   14  
   15  # Category order
   16  categories=(
   17    "🐧 Kernel & Boot"
   18    "🎮 Emulators & Frontend"
   19    "🖥️ Graphics"
   20    "📦 Multimedia"
   21    "🔊 Audio"
   22    "🌐 Network"
   23    "📱 Device Support"
   24    "⚙️ CI & Workflows"
   25    "🔧 System"
   26    "📚 Documentation"
   27    "🔩 Other"
   28    "↩️ Reverts"
   29  )
   30  
   31  log_args=(--format="%s%x1f%an%x1f%H")
   32  if [ -n "${MAX_COUNT}" ]; then
   33    log_args+=(--max-count="${MAX_COUNT}")
   34  fi
   35  
   36  tmpdir=$(mktemp -d)
   37  
   38  while IFS=$'\x1f' read -r subject author commit_hash; do
   39    [[ -z "$subject" ]] && continue
   40    short_hash="${commit_hash:0:7}"
   41    line="- ${subject} (${author}) ([${short_hash}](https://github.com/ROCKNIX/distribution/commit/${commit_hash}))"
   42    category="🔩 Other"
   43    if [[ "$subject" == *:* ]]; then
   44    prefix=$(echo "$subject" | cut -d: -f1 | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]//g')
   45    case "$prefix" in
   46      # Reverts
   47      revert*)
   48        category="↩️ Reverts" ;;
   49      # Kernel & Boot
   50      linux|u-boot*|kernel*|dtc|dt-overlays|rkbin|atf|mkbootimg|grub|syslinux|amlogic-boot-fip|exynos-boot-fip|crust|bootloader|installer|qcom-abl|rocknix-abl|device-tree-overlays|mali-bifrost|rocknix-joypad|dtbocfg|generic-dsi|ap6256-firmware|ap6611s-firmware|esp8089-firmware|extra-firmware|g610-mali-csffw|ibt-firmware|iwlwifi-firmware|kernel-firmware|rtl8188fu-firmware|rtl8812au|rtl8814au|rtl8821au|rtl8821cu|rtl8851bu|rtl88x2bu|rtw88|arm-efi|patches|linux-drivers|linux-firmware|abl)
   51        category="🐧 Kernel & Boot" ;;
   52      # Emulators & Frontend
   53      *-sa|*-lr|retroarch|emulationstation|gamecontrollerdb|rocknix-systems|hypseus*|openbor*|pico-8*|heroic*|amiberry*|mednafen*|steam*|box64|box86|fex-emu|wine|portmaster*|moonlight*|lowerdeck*|themes*|es-themes*|oga*|m8c*|supersnes9x|pcsx2)
   54        category="🎮 Emulators & Frontend" ;;
   55      # Audio
   56      pipewire|wireplumber|alsa*|pulseaudio|opus|flac|libvorbis|libsndfile|wavpack|sbc|speex*|openal*|fdk-aac|ldacbt*|libldac|fluidsynth|libopenmpt|soxr|libogg|lame|libfreeaptx|libmodplug|sidplay*|taglib|espeak*|sdl2_mixer|libao|sndio|libxmp)
   57        category="🔊 Audio" ;;
   58      # Graphics
   59      mesa|mesa-demos|gamescope|mangohud|vulkan*|*-shaders|glsl*|slang*|librashader|libdrm|libglvnd|libepoxy|libmali*|librga|gpudriver|spirv*|glew|glfw|glslang|glm|glu|cairo|libpng|libjpeg*|libwebp|pango|harfbuzz|gdk-pixbuf|libheif|libraw|libde265|lcms2|tiff|libprojectm*|sdl2*|sdl3*|waffle|wxwidgets|qt6|imagemagick|fbgrab|grim|gtk2|gtk3|capsimg|xserver|libclc)
   60        category="🖥️ Graphics" ;;
   61      # Multimedia
   62      ffmpeg|libva|dav1d|aom|libass|libdvd*|libbluray|bento4|libbdplus|libmpeg2|libvdpau|rtmpdump|zvbi|nvidia-vaapi-driver|nv-codec-headers|media-driver|intel-vaapi-driver|libudfread|libaacs|gmmlib|mpv|vlc|gstreamer|libvpx|libplacebo|gmu|libdvbpsi|opusfile|rkmpp)
   63        category="📦 Multimedia" ;;
   64      # Network
   65      connman|iwd|networkmanager|bluez|openssh|samba|nfs*|avahi|syncthing|rclone|tailscale|zerotier*|wireguard*|openvpn|sixaxis|iw|iptables|wsdd2|wireless-regdb|libpcap|enet|libndp|libnl|libtirpc|libssh|nss-mdns|ap6611s|simple-http-server|fping|speedtest-cli|curl|libslirp|wifi)
   66        category="🌐 Network" ;;
   67      # Device Support
   68      h700*|rk3326*|rk3399*|rk3566*|rk3576*|rk3588*|s922x*|sm6115*|sm4450*|sm8250*|sm8550*|sm8650*|sm8750*|amd64*|quirks)
   69        category="📱 Device Support" ;;
   70      # CI & Workflows
   71      ci|workflows|validate-commit)
   72        category="⚙️ CI & Workflows" ;;
   73      # Documentation
   74      documentation|docs)
   75        category="📚 Documentation" ;;
   76      # System
   77      busybox|systemd*|deviceinfo|post-update|updateabl|options|lib32|install*|build|rocknix*|wayland*|libinput|libxkbcommon|weston*|mtdev|dbus|udevil|parted|util-linux|e2fsprogs|dosfstools|kmod|libusb*|usbutils|fuse*|procps*|nano|evrepeat|emmctool|wait-time-sync|inputplumber*|bash|btop|btrfs-progs|drm_tool|gptfdisk|i2c-tools|lsof|nvtop|powerstate|squashfs*|squashfuse|system-utils|umtprd|usb-modeswitch|openssl|libgpg-error|libarchive|libzip|p7zip|gzip|xz|cabextract|expat|icu|jsoncpp|libxml2|libcroco|libiconv|boost|glib|glibc|ncurses|readline|cmake|joyutils|gamepadcalibration|entware|socat|rocknix-splash|coreutils|dialog|freeimage|pyudev|miniupnpc|sound|poppler|grep|file|sleep|avfs|libiio|bin2c|libserialport|swig|llvm|gcc*|go|lua*|nasm|rust*|cargo*|cbindgen|textviewer|dejavu|spleen*|apitrace|strace|at-spi2-atk|at-spi2-core|autostart|config|profiled|sources|sysctld|udevd|bdf2psf|shared-mime-info|ccache|ecm|gnulib|inih|json-glib|libaio|libcom-err|libdatrie|libfmt|libpthread-stubs|libthai|make|patchelf|six|xa|commander|control-gen|device-switch|gamepadtester|jstest-sdl|list-guid|mako-osd|qterminal|sdljoytest|sdltouchtest|compositor|swaywm-env|empty|modules|pyfdt|qemu|synctools|usbgadget|panel|input_sense)
   78        category="🔧 System" ;;
   79    esac
   80    fi
   81    echo "$line" >> "${tmpdir}/${category}"
   82  done < <(
   83    git log "${log_args[@]}" "${GIT_RANGE}" 2>/dev/null \
   84      | grep -v "Merge pull request" \
   85      | grep -v "Merge branch" \
   86      | grep -v "Merge remote-tracking branch" \
   87      | grep -v "^$"
   88  )
   89  
   90  for cat in "${categories[@]}"; do
   91    if [ -f "${tmpdir}/${cat}" ]; then
   92      printf "\n### %s\n\n" "${cat}"
   93      cat "${tmpdir}/${cat}"
   94    fi
   95  done
   96  
   97  rm -rf "${tmpdir}"
   98  
```

## File: .github/scripts/generate-release-body.sh (at 8ebaf8daad, 288 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
    4  # Generate release body with dynamic device tables from config.xml
    5  # Usage: generate-release-body.sh <DATE> <LAST_TAG>
    6  
    7  DATE="${1}"
    8  LAST_TAG="${2}"
    9  CHANGELOG_MAX_COUNT="${CHANGELOG_MAX_COUNT:-200}"
   10  REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
   11  CONFIG_XML="${REPO_ROOT}/projects/ROCKNIX/config.xml"
   12  
   13  if [ ! -f "${CONFIG_XML}" ]; then
   14    echo "ERROR: config.xml not found at ${CONFIG_XML}" >&2
   15    exit 1
   16  fi
   17  
   18  # Parse config.xml to get devices and their subdevices
   19  # Returns lines like: DEVICE:SUBDEVICE (or DEVICE: if no subdevice)
   20  get_image_variants() {
   21    local device="$1"
   22    # Check if device has subdevices with mkimage_options (these produce separate images)
   23    local subdevices
   24    subdevices=$(xmlstarlet sel -t -m "//rocknix/${device}/*[@mkimage_options]" -v "name()" -n "${CONFIG_XML}" 2>/dev/null | tr '\n' ' ')
   25  
   26    if [ -n "${subdevices}" ]; then
   27      for sub in ${subdevices}; do
   28        echo "${device}:${sub}"
   29      done
   30    else
   31      echo "${device}:"
   32    fi
   33  }
   34  
   35  # Get human-readable device names from file elements
   36  get_device_names() {
   37    local device="$1"
   38    local subdevice="$2"
   39  
   40    if [ -n "${subdevice}" ]; then
   41      # Get full names from files with @full attribute, or derive from dtb filename
   42      local names
   43      names=$(xmlstarlet sel -t -m "//rocknix/${device}/${subdevice}/file[@full]" -v "@full" -n "${CONFIG_XML}" 2>/dev/null)
   44      if [ -z "${names}" ]; then
   45        names=$(xmlstarlet sel -t -m "//rocknix/${device}/${subdevice}/file" -v "." -n "${CONFIG_XML}" 2>/dev/null)
   46      fi
   47    else
   48      local names
   49      names=$(xmlstarlet sel -t -m "//rocknix/${device}/file[@full]" -v "@full" -n "${CONFIG_XML}" 2>/dev/null)
   50      if [ -z "${names}" ]; then
   51        names=$(xmlstarlet sel -t -m "//rocknix/${device}/file" -v "." -n "${CONFIG_XML}" 2>/dev/null)
   52      fi
   53    fi
   54    echo "${names}"
   55  }
   56  
   57  # Format dtb name to human-readable
   58  format_dtb_name() {
   59    local dtb="$1"
   60    # Remove known SoC prefixes: sun50i-h700-, rk3326-, rk3566-, rk3399-, rk3576-, rk3588s-, rk3568-, meson-g12b-, sm8250-, sm8650-, qcs8550-, cq8725s-, sm6115-
   61    local name
   62    name=$(echo "${dtb}" | sed -E 's/^(sun50i-h700|rk33[0-9]{2}|rk35[0-9]{2}s?|meson-g12b|sm[0-9]+|qcs[0-9]+|cq[0-9]+s?)-//')
   63    echo "${name}" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g'
   64  }
   65  
   66  # Generate image filename
   67  get_image_filename() {
   68    local device="$1"
   69    local subdevice="$2"
   70    local suffix=""
   71  
   72    if [ -n "${subdevice}" ]; then
   73      suffix="-${subdevice}"
   74    fi
   75  
   76    echo "ROCKNIX-${device}.aarch64-${DATE}${suffix}.img.gz"
   77  }
   78  
   79  get_update_filename() {
   80    local device="$1"
   81    echo "ROCKNIX-${device}.aarch64-${DATE}.tar"
   82  }
   83  
   84  # Build device description string
   85  get_device_description() {
   86    local device="$1"
   87    local subdevice="$2"
   88    local names
   89  
   90    # Try to get full attribute names first
   91    if [ -n "${subdevice}" ]; then
   92      names=$(xmlstarlet sel -t -m "//rocknix/${device}/${subdevice}/file[@full]" -v "@full" -n "${CONFIG_XML}" 2>/dev/null)
   93      if [ -z "${names}" ]; then
   94        names=$(xmlstarlet sel -t -m "//rocknix/${device}/${subdevice}/file" -v "." -n "${CONFIG_XML}" 2>/dev/null | grep -v -E "rev[0-9]|v2-panel")
   95        names=$(echo "${names}" | while read -r line; do [ -n "$line" ] && format_dtb_name "$line"; done)
   96      fi
   97    else
   98      names=$(xmlstarlet sel -t -m "//rocknix/${device}/file[@full]" -v "@full" -n "${CONFIG_XML}" 2>/dev/null)
   99      if [ -z "${names}" ]; then
  100        names=$(xmlstarlet sel -t -m "//rocknix/${device}/file" -v "." -n "${CONFIG_XML}" 2>/dev/null | grep -v -E "rev[0-9]|v2-panel")
  101        names=$(echo "${names}" | while read -r line; do [ -n "$line" ] && format_dtb_name "$line"; done)
  102      fi
  103    fi
  104  
  105    echo "${names}" | paste -sd "," - | sed 's/,/, /g'
  106  }
  107  
  108  # Determine documentation path
  109  get_doc_path() {
  110    local device="$1"
  111    local subdevice="$2"
  112    local doc_dir="${REPO_ROOT}/documentation/PER_DEVICE_DOCUMENTATION"
  113  
  114    if [ -n "${subdevice}" ] && [ -d "${doc_dir}/${device}-${subdevice}" ]; then
  115      echo "/documentation/PER_DEVICE_DOCUMENTATION/${device}-${subdevice}/"
  116    elif [ -d "${doc_dir}/${device}" ]; then
  117      echo "/documentation/PER_DEVICE_DOCUMENTATION/${device}/"
  118    else
  119      echo ""
  120    fi
  121  }
  122  
  123  # --- Generate the release body ---
  124  
  125  cat << 'HEADER'
  126  &nbsp;&nbsp;<img src="https://raw.githubusercontent.com/ROCKNIX/distribution/next/distributions/ROCKNIX/logos/rocknix-logo.png" width=192>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Latest Version](https://img.shields.io/github/release/ROCKNIX/distribution.svg?color=5998FF&label=latest%20version&style=flat-square)](https://github.com/ROCKNIX/distribution/releases/latest) [![Activity](https://img.shields.io/github/commit-activity/m/ROCKNIX/distribution?color=5998FF&style=flat-square)](https://github.com/ROCKNIX/distribution/commits) [![Pull Requests](https://img.shields.io/github/issues-pr-closed/ROCKNIX/distribution?color=5998FF&style=flat-square)](https://github.com/ROCKNIX/distribution/pulls) [![Discord Server](https://img.shields.io/discord/948029830325235753?color=5998FF&label=chat&style=flat-square)](https://discord.gg/seTxckZjJy)
  127  #
  128  ROCKNIX is a community developed Linux distribution for handheld gaming devices.  Our goal is to produce an operating system that has the features and capabilities that we need, and to have fun as we develop it.
  129  
  130  ## Licenses
  131  ROCKNIX is a Linux distribution that is made up of many open-source components.  Components are provided under their respective licenses.  This distribution includes components licensed for non-commercial use only.
  132  
  133  ### ROCKNIX Branding
  134  ROCKNIX branding and images are licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
  135  
  136  #### You are free to
  137  * Share — copy and redistribute the material in any medium or format
  138  * Adapt — remix, transform, and build upon the material
  139  
  140  #### Under the following terms
  141  * Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
  142  * NonCommercial — You may not use the material for commercial purposes.
  143  * ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
  144  
  145  ### ROCKNIX Software
  146  HEADER
  147  
  148  echo "Copyright (C) $(date +%Y) ROCKNIX (https://github.com/ROCKNIX)"
  149  
  150  cat << 'HEADER2'
  151  
  152  Licensed under the Apache License, Version 2.0 (the "License");
  153  you may not use this file except in compliance with the License.
  154  You may obtain a copy of the License at
  155  
  156  http://www.apache.org/licenses/LICENSE-2.0
  157  
  158  Unless required by applicable law or agreed to in writing, software
  159  distributed under the License is distributed on an "AS IS" BASIS,
  160  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  161  See the License for the specific language governing permissions and
  162  limitations under the License.
  163  
  164  ## Installation
  165  * Download the latest version of ROCKNIX.
  166  * Decompress the image.
  167  * Write the image to an SDCARD using an imaging tool.  Common imaging tools include [Balena Etcher](https://www.balena.io/etcher/), [Raspberry Pi Imager](https://www.raspberrypi.com/software/), and [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/).  If you're skilled with the command line, dd works fine too.
  168  
  169  ### Installation Package Downloads
  170  HEADER2
  171  
  172  # Generate installation table
  173  echo "| **Device/Platform** | **Download Package** | **Documentation** |"
  174  echo "|---------------------|----------------------|-------------------|"
  175  
  176  # Get all top-level devices
  177  devices=$(xmlstarlet sel -t -m "//rocknix/*" -v "name()" -n "${CONFIG_XML}" 2>/dev/null | sort -u)
  178  
  179  for device in ${devices}; do
  180    variants=$(get_image_variants "${device}")
  181    for variant in ${variants}; do
  182      dev="${variant%%:*}"
  183      sub="${variant#*:}"
  184  
  185      description=$(get_device_description "${dev}" "${sub}")
  186      img_file=$(get_image_filename "${dev}" "${sub}")
  187      doc_path=$(get_doc_path "${dev}" "${sub}")
  188  
  189      doc_link=""
  190      if [ -n "${doc_path}" ]; then
  191        doc_link="[documentation](${doc_path})"
  192      fi
  193  
  194      echo "| **${description}** | [${img_file}](https://github.com/ROCKNIX/distribution/releases/download/${DATE}/${img_file}) | ${doc_link} |"
  195    done
  196  done
  197  
  198  cat << 'MIDDLE'
  199  
  200  ## Upgrading
  201  * Download and install the update online via the System Settings menu.
  202  * If you are unable to update online
  203    * Download the latest version of ROCKNIX from Github
  204    * Copy the update to your device over the network to your device's update share.
  205    * Reboot the device, and the update will begin automatically.
  206  
  207  ### Update Package Downloads
  208  | **Device/Platform** | **Download Package** |
  209  |---------------------|----------------------|
  210  MIDDLE
  211  
  212  for device in ${devices}; do
  213    # For update table, collect all device names across all subdevices
  214    variants=$(get_image_variants "${device}")
  215    all_descriptions=""
  216    for variant in ${variants}; do
  217      dev="${variant%%:*}"
  218      sub="${variant#*:}"
  219      desc=$(get_device_description "${dev}" "${sub}")
  220      if [ -n "${all_descriptions}" ] && [ -n "${desc}" ]; then
  221        all_descriptions="${all_descriptions}, ${desc}"
  222      elif [ -n "${desc}" ]; then
  223        all_descriptions="${desc}"
  224      fi
  225    done
  226    update_file=$(get_update_filename "${device}")
  227    echo "| **${all_descriptions}** | [${update_file}](https://github.com/ROCKNIX/distribution/releases/download/${DATE}/${update_file}) |"
  228  done
  229  
  230  cat << FOOTER
  231  
  232  ## Documentation
  233  
  234  ### Contribute
  235  
  236  * [Building ROCKNIX](https://rocknix.org/contribute/build/)
  237  * [Code of Conduct](https://rocknix.org/contribute/code-of-conduct/)
  238  * [Contributing to ROCKNIX](https://rocknix.org/contribute/)
  239  * [Modifying ROCKNIX](https://rocknix.org/contribute/modify/)
  240  * [Adding Hardware Quirks](https://rocknix.org/contribute/quirks/)
  241  * [Creating Packages](https://rocknix.org/contribute/packages/)
  242  * [Pull Request Template](/PULL_REQUEST_TEMPLATE.md)
  243  
  244  ### Play
  245  
  246  * [Installing ROCKNIX](https://rocknix.org/play/install/)
  247  * [Updating ROCKNIX](https://rocknix.org/play/update/)
  248  * [Controls](https://rocknix.org/play/controls/)
  249  * [Netplay](https://rocknix.org/play/netplay/)
  250  * [Configuring Moonlight](https://rocknix.org/systems/moonlight/)
  251  * [Device Specific Documentation](/documentation/PER_DEVICE_DOCUMENTATION)
  252  
  253  ### Configure
  254  
  255  * [Optimizations](https://rocknix.org/configure/optimizations/)
  256  * [Shaders](https://rocknix.org/configure/shaders/)
  257  * [Cloud Sync](https://rocknix.org/configure/cloud-sync/)
  258  * [VPN](https://rocknix.org/configure/vpn/)
  259  
  260  ### Other
  261  
  262  * [Frequently Asked Questions](https://rocknix.org/faqs/)
  263  * [Donating to ROCKNIX](https://rocknix.org/donations/)
  264  
  265  
  266  **Full Changelog**: https://github.com/ROCKNIX/distribution/compare/${LAST_TAG}...${DATE}
  267  FOOTER
  268  
  269  if [ -n "${LAST_TAG}" ]; then
  270    printf "\n## Changelog\n"
  271    if [[ "${CHANGELOG_MAX_COUNT}" =~ ^[0-9]+$ ]] && [ "${CHANGELOG_MAX_COUNT}" -gt 0 ]; then
  272      total_commits=$(git rev-list --count "${LAST_TAG}..HEAD" 2>/dev/null || echo 0)
  273      bash "$(dirname "$0")/generate-changelog.sh" "${LAST_TAG}..HEAD" "${CHANGELOG_MAX_COUNT}"
  274      if [ "${total_commits}" -gt "${CHANGELOG_MAX_COUNT}" ] 2>/dev/null; then
  275        omitted_commits=$((total_commits - CHANGELOG_MAX_COUNT))
  276        printf -- "\n- %s commits omitted\n" "${omitted_commits}"
  277        printf -- "- Full changelog: https://github.com/ROCKNIX/distribution/compare/%s...%s\n" "${LAST_TAG}" "${DATE}"
  278      fi
  279    else
  280      bash "$(dirname "$0")/generate-changelog.sh" "${LAST_TAG}..HEAD"
  281    fi
  282  else
  283    printf "\n## Changelog\n\n- No previous tag found\n"
  284  fi
  285  
  286  
  287  
  288  
```

## File: .github/workflows/fork-checks.yml (at 8ebaf8daad, 59 lines)

```text
    1  # The fork's record checks, run on every push of next and once a day: the
    2  # work-log index current, the decision register sound, no friction entry
    3  # left without an issue, the retro / weekly / monthly cadence kept, every
    4  # recent blindspot naming a guard, an audit and a futro when they are owed.
    5  # Red until each overdue ceremony has its artifact (#254, D-WORKFLOW-028).
    6  # Fork-only (`fork-*`): never part of an upstream PR.
    7  name: fork record checks
    8  
    9  on:
   10    push:
   11      branches: [next]
   12    schedule:
   13      - cron: '17 6 * * *'
   14    workflow_dispatch:
   15      inputs:
   16        ceremony_today:
   17          description: "Run the ceremony check as of this date (yyyy-mm-dd) -- the guard's constructed positive: a far date makes an audit or a futro overdue and the run red (audit #258 PL-020)"
   18          required: false
   19          default: ""
   20  
   21  permissions:
   22    contents: read
   23    issues: read
   24  
   25  jobs:
   26    record:
   27      runs-on: ubuntu-24.04
   28      steps:
   29        - uses: actions/checkout@v4
   30          with:
   31            fetch-depth: 0
   32        - name: identify upstream history for the fork issue-coverage check
   33          run: git fetch --no-tags https://github.com/ROCKNIX/distribution.git next:refs/remotes/upstream/next
   34        - name: work-log index is current
   35          run: ./tools/work-log-index --check
   36        - name: decision register is a lookup table
   37          run: ./tools/register-check
   38        - name: the instruction files are what their index says
   39          run: ./tools/rules-check
   40        - name: builds always enter the shared watcher and retain lifecycle evidence
   41          run: |
   42            python3 docs/qa-logs/2026-10-03-watch-job/test-watch-job.py tools/watch-job
   43            python3 tools/host-maintenance/test-build-monitor
   44            python3 tools/host-maintenance/test-build-admission
   45        - name: VM launch failures cannot report a guest as running
   46          run: |
   47            ./tools/vm-pair-test
   48            ./tools/vm-upgrade-readiness-test
   49        - name: optional hardware readings are valid or explicitly unavailable
   50          run: ./tools/rocknix-info-test
   51        - name: every open acceptance checkbox is agent-verifiable (D-QA-044)
   52          env:
   53            GH_TOKEN: ${{ github.token }}
   54          run: ./tools/box-check --quiet
   55        - name: ceremonies are not overdue
   56          env:
   57            GH_TOKEN: ${{ github.token }}
   58            CEREMONY_TODAY: ${{ inputs.ceremony_today }}
   59          run: ./tools/ceremony-check
```

## File: .github/workflows/fork-generic-x64.yml (at 8ebaf8daad, 13 lines)

```text
    1  # D-WORKFLOW-119/120: disabled until isolated runners and immutable candidate
    2  # qualification exist. CI output must never be attached directly to a release.
    3  name: fork candidate automation (disabled)
    4  on:
    5    workflow_dispatch:
    6  permissions:
    7    contents: read
    8  jobs:
    9    qualification-required:
   10      if: ${{ false }}
   11      runs-on: ubuntu-24.04
   12      steps:
   13        - run: echo "Build and qualify an immutable candidate locally."
```

## File: .github/workflows/fork-mirror-build-container.yml (at 8ebaf8daad, 49 lines)

```text
    1  # Mirror the build container under the fork's own registry (#344 P1,
    2  # D-WORKFLOW-119/120). Runs only by hand, on GitHub's own runner, with the
    3  # workflow's built-in token: no personal access token exists for this and
    4  # none lives on the build host. The copy preserves the manifest and its
    5  # digest (skopeo --preserve-digests), and the job fails if the digest it
    6  # reads back differs from the one it was given, so the Makefile can pin the
    7  # mirror by @sha256: and a build-log line can prove which bytes it ran in.
    8  name: fork-mirror-build-container
    9  
   10  on:
   11    workflow_dispatch:
   12      inputs:
   13        source:
   14          description: "Source image by digest"
   15          required: true
   16          default: "ghcr.io/rocknix/rocknix-build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39"
   17        tag:
   18          description: "Tag under ghcr.io/pixelelated/build"
   19          required: true
   20          default: "20260925-988c0ba5"
   21  
   22  permissions:
   23    contents: read
   24    packages: write
   25  
   26  jobs:
   27    mirror:
   28      runs-on: ubuntu-latest
   29      steps:
   30        - name: Install skopeo
   31          run: sudo apt-get update -q && sudo apt-get install -y -q skopeo
   32  
   33        - name: Sign in to the organisation's registry with the workflow token
   34          run: echo "${{ secrets.GITHUB_TOKEN }}" | skopeo login ghcr.io -u "${{ github.actor }}" --password-stdin
   35  
   36        - name: Copy by digest, preserving it
   37          env:
   38            SRC: ${{ inputs.source }}
   39            TAG: ${{ inputs.tag }}
   40          run: |
   41            set -euo pipefail
   42            case "$SRC" in *@sha256:*) ;; *) echo "source must be pinned by digest"; exit 2;; esac
   43            want="${SRC##*@}"
   44            skopeo copy --all --preserve-digests "docker://$SRC" "docker://ghcr.io/pixelelated/build:$TAG"
   45            got="sha256:$(skopeo inspect --raw "docker://ghcr.io/pixelelated/build:$TAG" | sha256sum | cut -d' ' -f1)"
   46            echo "source digest: $want"
   47            echo "mirror digest: $got"
   48            [ "$want" = "$got" ] || { echo "DIGEST MISMATCH: the mirror is not the source"; exit 1; }
   49            echo "pin: ghcr.io/pixelelated/build@$got" | tee -a "$GITHUB_STEP_SUMMARY"
```

## File: .github/workflows/fork-wordlist.yml (at 8ebaf8daad, 40 lines)

```text
    1  # Every push of every branch of the fork, checked in a runner once it reaches
    2  # GitHub (maintainer, 2026-09-28, #312): the tree and the pushed commits'
    3  # messages against the wordlist the fork must not carry. The list is the
    4  # repository secret FORBIDDEN_PATTERNS, never a file in the tree; without it
    5  # tools/forbidden-terms-check exits 2 and this job is red, which is the point.
    6  # The local half is .githooks/ (pre-commit, commit-msg, pre-push).
    7  # Fork-only (`fork-*`): never part of an upstream PR.
    8  name: fork wordlist check
    9  
   10  on:
   11    push:
   12      branches: ['**']
   13    workflow_dispatch:
   14  
   15  permissions:
   16    contents: read
   17  
   18  jobs:
   19    wordlist:
   20      runs-on: ubuntu-24.04
   21      env:
   22        FORBIDDEN_PATTERNS: ${{ secrets.FORBIDDEN_PATTERNS }}
   23      steps:
   24        - uses: actions/checkout@v4
   25          with:
   26            fetch-depth: 0
   27        - name: the tree carries no listed word
   28          run: ./tools/forbidden-terms-check
   29        - name: no pushed commit message carries a listed word
   30          env:
   31            BEFORE: ${{ github.event.before }}
   32            AFTER: ${{ github.sha }}
   33          run: |
   34            set -uo pipefail
   35            case "${BEFORE:-}" in
   36              ''|0000000000000000000000000000000000000000) range="-n 50 ${AFTER}" ;;   # a new branch: its last fifty
   37              *) if git cat-file -e "${BEFORE}^{commit}" 2>/dev/null; then range="${BEFORE}..${AFTER}"; else range="-n 50 ${AFTER}"; fi ;;
   38            esac
   39            # shellcheck disable=SC2086
   40            git log --format=%B ${range} | ./tools/forbidden-terms-check --stdin
```

## File: tools/archaeology (at 8ebaf8daad, 290 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # What does the record already say about this? One command over every place
    6  # a decision or a lesson can live in this fork, printed as dated lines, so
    7  # "have we settled this before?" is answered by reading, not by asking.
    8  #
    9  #   tools/archaeology <term>...            # each term a case-insensitive regex
   10  #   tools/archaeology --issue 209          # the issue's own trail as well
   11  #   tools/archaeology --since 2026-09-01 webkit gstreamer
   12  #   tools/archaeology --no-gh ...          # offline: skip the tracker
   13  #   tools/archaeology --reversal 'left running|in the background'   # the sweep list after a reversal
   14  #
   15  # --reversal prints every line in this tree (outside build output), the
   16  # EmulationStation checkout (ES_SRC) and docs/ that carries the old words, so
   17  # a row that reverses, renames or re-pins can list what it made stale and the
   18  # sweep can land with it (decision-register.md, audit #258 P-01).
   19  #
   20  # It reads the decision register (decided rows and the open table), the
   21  # blindspot register, every dated work-log entry, the rule files, the git
   22  # history (`git log -S`), and the fork's issues and comments (`gh`). A hit
   23  # is one line: where, when, what. Run it before listing anything as
   24  # "pending" or "undecided" for the maintainer -- on 2026-09-23 four
   25  # decisions were put to them that the register, the issues and the logs
   26  # had already settled (blindspot 52), and each would have shown up here.
   27  
   28  import os
   29  import re
   30  import subprocess
   31  import sys
   32  import json
   33  
   34  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   35  REPO = 'pixelelated/distribution'
   36  
   37  
   38  def rx(term):
   39      return re.compile(term, re.I)
   40  
   41  
   42  def clip(s, n=150):
   43      s = ' '.join(s.split())
   44      return s if len(s) <= n else s[:n - 1] + '…'
   45  
   46  
   47  def register(terms, since):
   48      """Decided rows and open rows of docs/decision-register.md."""
   49      path = os.path.join(ROOT, 'docs/decision-register.md')
   50      if not os.path.exists(path):
   51          return []
   52      hits = []
   53      section = 'decided'
   54      for line in open(path, encoding='utf-8'):
   55          if line.startswith('## Open decisions'):
   56              section = 'open'
   57          if not line.startswith('| D-'):
   58              continue
   59          cells = [c.strip() for c in line.strip().strip('|').split('|')]
   60          if len(cells) < 3:
   61              continue
   62          did = cells[0]
   63          date = cells[1] if re.match(r'\d{4}-\d\d-\d\d', cells[1]) else '(open)'
   64          text = cells[2] if date != '(open)' else cells[1]
   65          blob = line
   66          if all(t.search(blob) for t in terms):
   67              if since and date != '(open)' and date < since:
   68                  continue
   69              tag = 'OPEN' if section == 'open' or date == '(open)' else 'decided'
   70              hits.append((date, 'register %s %s' % (tag, did), clip(text.replace('**', ''), 170)))
   71      return hits
   72  
   73  
   74  def blindspots(terms, since):
   75      path = os.path.join(ROOT, 'docs/blindspot-register.md')
   76      if not os.path.exists(path):
   77          return []
   78      hits = []
   79      head = None
   80      body = []
   81  
   82      def flush():
   83          if head and all(t.search(head + '\n' + '\n'.join(body)) for t in terms):
   84              m = re.search(r'\((\d{4}-\d\d-\d\d)\)', head)
   85              date = m.group(1) if m else ''
   86              if not (since and date and date < since):
   87                  hits.append((date, 'blindspot', clip(head.lstrip('# '), 150)))
   88      for line in open(path, encoding='utf-8'):
   89          if line.startswith('## '):
   90              flush()
   91              head, body = line.strip(), []
   92          else:
   93              body.append(line)
   94      flush()
   95      return hits
   96  
   97  
   98  def work_logs(terms, since):
   99      base = os.path.join(ROOT, 'docs/work-logs')
  100      hits = []
  101      for d, _, files in os.walk(base):
  102          for f in sorted(files):
  103              m = re.match(r'(\d{4})_(\d\d)_(\d\d)-work_log\.md$', f)
  104              if not m:
  105                  continue
  106              date = '%s-%s-%s' % m.groups()
  107              if since and date < since:
  108                  continue
  109              head, body = None, []
  110  
  111              def flush():
  112                  if head is None:
  113                      return
  114                  blob = head + '\n' + '\n'.join(body)
  115                  if all(t.search(blob) for t in terms):
  116                      hm = re.match(r'## (\d\d:\d\d) UTC\s*[—–-]+\s*(.*)', head)
  117                      when, title = (hm.group(1), hm.group(2)) if hm else ('', head.lstrip('# '))
  118                      hits.append((date, 'work-log %s' % when, clip(title, 150)))
  119              for line in open(os.path.join(d, f), encoding='utf-8'):
  120                  if line.startswith('## '):
  121                      flush()
  122                      head, body = line.strip(), []
  123                  else:
  124                      body.append(line)
  125              flush()
  126      return hits
  127  
  128  
  129  def rules(terms):
  130      base = os.path.join(ROOT, '.claude/rules')
  131      hits = []
  132      if not os.path.isdir(base):
  133          return hits
  134      for f in sorted(os.listdir(base)):
  135          if not f.endswith('.md'):
  136              continue
  137          head, body = f, []
  138  
  139          def flush():
  140              blob = head + '\n' + '\n'.join(body)
  141              if all(t.search(blob) for t in terms):
  142                  hits.append(('', 'rule %s' % f, clip(head.lstrip('# '), 150)))
  143          for line in open(os.path.join(base, f), encoding='utf-8'):
  144              if line.startswith('## '):
  145                  flush()
  146                  head, body = line.strip(), []
  147              else:
  148                  body.append(line)
  149          flush()
  150      return hits
  151  
  152  
  153  def git_history(terms, since, limit=15):
  154      hits = []
  155      for t in terms:
  156          # -G takes a regex over the diff's lines (-S wants a literal string)
  157          cmd = ['git', '-C', ROOT, 'log', '--date=short', '--format=%ad %h %s', '--regexp-ignore-case', '-G' + t.pattern, '--', '.']
  158          if since:
  159              cmd.insert(4, '--since=' + since)
  160          try:
  161              out = subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
  162          except Exception as e:  # noqa: BLE001
  163              hits.append(('', 'git', 'git log failed: %s' % e))
  164              continue
  165          for line in out.splitlines()[:limit]:
  166              date, sha, subj = line.split(' ', 2)
  167              hits.append((date, 'git %s' % sha, clip(subj, 150)))
  168      return hits
  169  
  170  
  171  def gh_json(args):
  172      try:
  173          out = subprocess.run(['gh'] + args, capture_output=True, text=True, timeout=60)
  174      except Exception as e:  # noqa: BLE001
  175          return None, str(e)
  176      if out.returncode != 0:
  177          return None, out.stderr.strip()
  178      try:
  179          return json.loads(out.stdout), None
  180      except ValueError:
  181          return None, 'gh returned no JSON'
  182  
  183  
  184  def issues(terms, since):
  185      hits = []
  186      for t in terms:
  187          data, err = gh_json(['issue', 'list', '--repo', REPO, '--state', 'all', '--limit', '30',
  188                               '--search', t.pattern, '--json', 'number,title,state,createdAt,closedAt'])
  189          if err:
  190              hits.append(('', 'gh', 'issue search failed: %s' % clip(err, 100)))
  191              continue
  192          for it in data:
  193              date = it['createdAt'][:10]
  194              if since and date < since:
  195                  continue
  196              closed = (' closed %s' % it['closedAt'][:10]) if it.get('closedAt') else ''
  197              hits.append((date, 'issue #%d %s%s' % (it['number'], it['state'].lower(), closed), clip(it['title'], 150)))
  198      return hits
  199  
  200  
  201  def issue_trail(n):
  202      data, err = gh_json(['issue', 'view', str(n), '--repo', REPO, '--json', 'title,state,createdAt,body,comments'])
  203      if err:
  204          return [('', 'gh', 'issue %s: %s' % (n, clip(err, 100)))]
  205      hits = [(data['createdAt'][:10], 'issue #%s %s' % (n, data['state'].lower()), clip(data['title'], 150))]
  206      ids = sorted(set(re.findall(r'\bD-[A-Z]+-\d+\b', data.get('body') or '')))
  207      if ids:
  208          hits.append((data['createdAt'][:10], 'issue #%s body cites' % n, ' '.join(ids)))
  209      for c in data.get('comments') or []:
  210          date = c['createdAt'][:10]
  211          body = c.get('body') or ''
  212          cids = sorted(set(re.findall(r'\bD-[A-Z]+-\d+\b', body)))
  213          first = clip(body.strip().split('\n', 1)[0].replace('**', ''), 140)
  214          hits.append((date, 'issue #%s comment' % n, first + ((' [' + ' '.join(cids) + ']') if cids else '')))
  215      return hits
  216  
  217  
  218  def reversal(pattern):
  219      """Every line carrying the old words: this tree, the ES checkout, docs/."""
  220      roots = [ROOT]
  221      es = os.environ.get('ES_SRC') or os.path.expanduser('~/Development/emulationstation-next.worktrees/qa-integration')
  222      if os.path.isdir(es):
  223          roots.append(es)
  224      total = 0
  225      for r in roots:
  226          cmd = ['grep', '-rnIE', '--exclude-dir=.git', '--exclude-dir=build.*', '--exclude-dir=sources', '--exclude-dir=target',
  227                 '--exclude-dir=build-tests', '--exclude-dir=node_modules', pattern, r]
  228          out = subprocess.run(cmd, capture_output=True, text=True).stdout
  229          for line in out.splitlines():
  230              print(line[:220])
  231              total += 1
  232      print('\n%d line(s) carry the old words; each is a comment, a doc or a box to sweep in the same change as the row.' % total)
  233      return 0
  234  
  235  
  236  def main():
  237      args = sys.argv[1:]
  238      if len(args) >= 2 and args[0] == '--reversal':
  239          return reversal(args[1])
  240      if not args or args[0] in ('-h', '--help'):
  241          print(open(__file__).read().split('\n\n')[0].replace('# ', '').replace('#', ''))
  242          return 0
  243      since = None
  244      issue = None
  245      use_gh = True
  246      terms = []
  247      i = 0
  248      while i < len(args):
  249          if args[i] == '--since':
  250              since = args[i + 1]
  251              i += 2
  252          elif args[i] == '--issue':
  253              issue = args[i + 1]
  254              i += 2
  255          elif args[i] == '--no-gh':
  256              use_gh = False
  257              i += 1
  258          else:
  259              terms.append(args[i])
  260              i += 1
  261      if issue and not terms:
  262          terms = ['#%s\\b' % issue]
  263      if not terms:
  264          sys.exit('archaeology: give a term, or --issue N')
  265      trx = [rx(t) for t in terms]
  266      groups = [
  267          ('The decision register', register(trx, since)),
  268          ('The blindspot register', blindspots(trx, since)),
  269          ('Work logs', work_logs(trx, since)),
  270          ('Rules', rules(trx)),
  271          ('Git history (-G, on this checkout)', git_history(trx, since)),
  272      ]
  273      if use_gh:
  274          groups.append(('Issues', issues(trx, since)))
  275          if issue:
  276              groups.append(('Issue #%s, its trail' % issue, issue_trail(issue)))
  277      total = 0
  278      print('archaeology: %s%s' % (' AND '.join(terms), (' since ' + since) if since else ''))
  279      for title, hits in groups:
  280          hits = sorted(set(hits), key=lambda h: (h[0] or '9999', h[1]))
  281          print('\n== %s (%d)' % (title, len(hits)))
  282          for date, where, what in hits:
  283              print('  %-10s  %-28s  %s' % (date or '', where, what))
  284          total += len(hits)
  285      print('\n%d line(s). A decision listed as pending without a register OPEN row above is a claim to check.' % total)
  286      return 0
  287  
  288  
  289  if __name__ == '__main__':
  290      sys.exit(main())
```

## File: tools/box-check (at 8ebaf8daad, 107 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Is every open acceptance checkbox agent-verifiable? (D-QA-044, #268)
    6  # The checkbox checker: its output says "checkbox", never a bare "box",
    7  # which here means a machine (D-QA-045); the script keeps its name.
    8  #
    9  #   tools/box-check                 # every open issue on the fork; exit 1 when a checkbox fails
   10  #   tools/box-check --issue 266     # one issue
   11  #   tools/box-check --quiet         # failures only (CI)
   12  #
   13  # A checkbox fails when it names a person or a device as the thing that ticks it
   14  # ("the maintainer's word", "on the H700", "your yes", "RG SP:") and names no
   15  # physical fact the GENERIC_X64 guest cannot have (vm-first.md's list: a
   16  # radio, a battery, a board's boot, a panel, a tailnet, a LAN, hours on the
   17  # hardware). A checkbox whose artifact is a register row -- the maintainer's
   18  # call, recorded -- passes too: a decision is theirs to make, and the row is
   19  # the artifact (D-QA-044: their feedback dictates the work). It has to say
   20  # so ("register row", "decision-register"): a decision ID cited in passing is
   21  # not an artifact, and until 2026-09-25 any ID let a checkbox through --
   22  # "One real captive network on a handheld (maintainer's yes, D-QA-015)" passed
   23  # on the ID alone and named no fact (#158). A failing
   24  # checkbox asks a person for a re-observation of what the VM can frame, which
   25  # is how 35 issues came to wait on the maintainer on 2026-09-24 (#266). A
   26  # checkbox that names the fact passes: it asks for a device on purpose.
   27  #
   28  # It also notes, without failing, an open checkbox on an issue that a decided
   29  # register row cites: the row may have settled what the checkbox still asks
   30  # (blindspot 52; the hotspot drop and the Tailscale restart, 2026-09-25), so
   31  # the checkbox is re-derived against the row before it is put to anyone.
   32  #
   33  # Reads the tracker with gh; the fork only (issue-tracking.md).
   34  
   35  import json
   36  import os
   37  import re
   38  import subprocess
   39  import sys
   40  
   41  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   42  REPO = 'pixelelated/distribution'
   43  
   44  PERSON = re.compile(r"maintainer'?s? (own |)(word|yes|confirmation|call|device|library|account)|\byour (word|yes|own|device|library)\b|\btheir word\b|per-device yes|\(the maintainer'?s?\.?\)|the maintainer (switches|sees|reports|confirms|does|tries|opens|starts|plays)", re.I)
   45  DEVICE = re.compile(r"\bon (the |a |your )?(H700|RG35XX SP|RG SP|RG351M|RG353M|Nova|device|handheld|handhelds|hardware)\b|\b(RG SP|RG35XX SP|H700|Nova|The RG SP|The RG35XX SP):", re.I)
   46  FACT = re.compile(r"\bradio\b|wi-?fi (switch|join|radio|network)|hotspot|battery|\bboot(loader|s|ing)?\b|\bboard\b|\bpanel\b|tailnet|tailscale|\bLAN\b|multicast|mDNS|\bGPU\b|DRAM|DDR[34]|\bcard\b|flash|\bsleep\b|watchdog|ramoops|hours of|\bsoak\b|real (pad|panel|provider|hotspot)|SM8550|device tree|power[- ]cycle|physical|router|on one network|two (same-family |)(handhelds|units)|the (VM|guest) (has|cannot|can't)|register row|decision-register", re.I)
   47  BOX = re.compile(r'^\s*- \[ \] (.*)$')
   48  
   49  
   50  def gh(args):
   51      out = subprocess.run(['gh'] + args, capture_output=True, text=True)
   52      if out.returncode != 0:
   53          sys.exit('box-check: gh failed: %s' % out.stderr.strip()[:200])
   54      return json.loads(out.stdout)
   55  
   56  
   57  def register_refs():
   58      """issue number -> [decided row IDs whose text or refs cite it]."""
   59      path = os.path.join(ROOT, 'docs/decision-register.md')
   60      refs = {}
   61      if not os.path.exists(path):
   62          return refs
   63      open_section = False
   64      for line in open(path, encoding='utf-8'):
   65          if line.startswith('## Open decisions'):
   66              open_section = True
   67          if open_section or not line.startswith('| D-'):
   68              continue
   69          did = line.split('|')[1].strip()
   70          for n in set(re.findall(r'#(\d+)\b', line)):
   71              refs.setdefault(int(n), []).append(did)
   72      return refs
   73  
   74  
   75  def main():
   76      quiet = '--quiet' in sys.argv
   77      one = None
   78      if '--issue' in sys.argv:
   79          one = sys.argv[sys.argv.index('--issue') + 1]
   80      if one:
   81          issues = [gh(['issue', 'view', one, '--repo', REPO, '--json', 'number,title,body,state'])]
   82      else:
   83          issues = gh(['issue', 'list', '--repo', REPO, '--state', 'open', '--limit', '300', '--json', 'number,title,body,state'])
   84      refs = register_refs()
   85      fails, notes, boxes = [], [], 0
   86      for it in issues:
   87          n = it['number']
   88          body = it.get('body') or ''
   89          open_boxes = [m.group(1) for m in (BOX.match(l) for l in body.split('\n')) if m]
   90          boxes += len(open_boxes)
   91          for text in open_boxes:
   92              asks_person = bool(PERSON.search(text) or DEVICE.search(text))
   93              if asks_person and not FACT.search(text):
   94                  fails.append((n, text))
   95          if open_boxes and n in refs:
   96              notes.append((n, refs[n], len(open_boxes)))
   97      for n, text in fails:
   98          print('FAIL  #%d: names a person or a device and no physical fact: %s' % (n, ' '.join(text.split())[:150]))
   99      if not quiet:
  100          for n, ids, k in notes:
  101              print('note  #%d: %d open checkbox(es); decided rows cite it: %s -- re-derive against them' % (n, k, ' '.join(ids[:6])))
  102      print('box-check: %d issue(s), %d open checkbox(es), %d fail, %d issue(s) with rows to re-derive against' % (len(issues), boxes, len(fails), len(notes)))
  103      return 1 if fails else 0
  104  
  105  
  106  if __name__ == '__main__':
  107      sys.exit(main())
```

## File: tools/ceremony-check (at 8ebaf8daad, 461 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Did the ceremonies happen? The record says, and this reads it: the last
    6  # retro, futro and audit, the friction log's entries without an issue, the
    7  # weekly and monthly summaries, the work-log index, the register, and whether
    8  # each recent blindspot names a guard that exists. A ceremony that is due is
    9  # a line; one that is overdue past its grace fails the run. The cheap ones
   10  # (the friction log, the index, the register, the summaries, a retro, a
   11  # blindspot's guard) refuse a push of next through the guard; the long ones
   12  # (an audit, a futro) keep the fork's CI red until they happen, so the fixes
   13  # can still be pushed while the ceremony is owed (#254, D-WORKFLOW-028;
   14  # D-QA-040 is the maintainer's call on the cadences and on which ones block).
   15  #
   16  #   tools/ceremony-check            # report; exit 1 when something is overdue
   17  #   tools/ceremony-check --gate     # the same, terse, for the push guard
   18  #   tools/ceremony-check --no-gh    # without the tracker (audits and closures come from gh)
   19  #   tools/ceremony-check --issues-only # only next's commit-to-issue coverage
   20  #
   21  # The cadences are the constants below (D-QA-040 is the maintainer's call on
   22  # them). The clock starts at SINCE: nothing before it is demanded, so the
   23  # gate begins clean and demands from the day it was adopted rather than
   24  # refusing every push over a backlog nobody can pay at once.
   25  #
   26  # Markers, all in the record, none in anybody's memory:
   27  #   retro     docs/retros/<yyyy-mm-dd>-*.md, or a work-log entry whose heading says retro
   28  #   futro     docs/futros/<yyyy-mm-dd>-*.md, or a work-log entry whose heading says futro
   29  #   audit     an issue whose title starts "Audit" or "Code audit" (gh), or docs/audits/<yyyy-mm-dd>-*/
   30  #   friction  docs/friction-log.md entries: `- <yyyy-mm-dd> HH:MM -- ... -- issue: #N|none`
   31  #   weekly    docs/work-logs/<yyyy_mm>-work_logs/<yyyy>-W<ww>-summary.md
   32  #   monthly   docs/work-logs/<yyyy_mm>-work_logs/SUMMARY.md
   33  #   index     tools/work-log-index --check
   34  #   issues    fork commits on next after D-WORKFLOW-132 cite an issue
   35  #   hygiene   no issue closed as completed since the clock carries an open checkbox (audit #258 P-03; CI red)
   36  #   register  tools/register-check
   37  #   rules     tools/rules-check --quiet (the instruction files, D-WORKFLOW-045)
   38  #   checkboxes tools/box-check --quiet (agent-first criteria, D-QA-044/045; CI red)
   39  #   guards    docs/blindspot-register.md entries >= GUARD_FROM name a guard that exists
   40  
   41  import datetime as dt
   42  import glob
   43  import hashlib
   44  import json
   45  import os
   46  from pathlib import Path
   47  import re
   48  import subprocess
   49  import sys
   50  
   51  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   52  REPO = 'pixelelated/distribution'
   53  
   54  SINCE = dt.date(2026, 9, 21)       # the gate's clock starts here (the RC round; blindspot 51)
   55  RETRO_ACTIVE_DAYS = 5              # a phase retro every five days with a work-log entry
   56  RETRO_GRACE_DAYS = 2               # ... due at five, blocking at seven
   57  FUTRO_AFTER_EPIC_DAYS = 3          # a futro within three days of a new epic or milestone issue
   58  AUDIT_CLOSED_ISSUES = 12           # an audit after twelve issues closed as completed ...
   59  AUDIT_DAYS = 14                    # ... or fourteen days, whichever first
   60  FRICTION_ISSUE_DAYS = 3            # a friction entry gets an issue (or a guard) within three days
   61  WEEKLY_GRACE_DAYS = 2              # the week's summary by Tuesday
   62  MONTHLY_GRACE_DAYS = 3             # the month's summary by the 3rd
   63  GUARD_FROM = 52                    # blindspot entries from this number on must name a guard
   64  ISSUE_BASELINE = 'bf121ce8766258c06765d230d7a18efd23809ef1'  # D-WORKFLOW-132, #367
   65  
   66  
   67  def sh(cmd, timeout=120):
   68      try:
   69          p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
   70          return p.returncode, p.stdout.strip(), p.stderr.strip()
   71      except Exception as e:  # noqa: BLE001
   72          return 99, '', str(e)
   73  
   74  
   75  def gh_json(args):
   76      rc, out, err = sh(['gh'] + args, timeout=60)
   77      if rc != 0:
   78          return None, err or ('gh exit %d' % rc)
   79      try:
   80          return json.loads(out), None
   81      except ValueError:
   82          return None, 'gh returned no JSON'
   83  
   84  
   85  def completed_audit_marker(marker, root, now):
   86      """Validate an exact Phase 7 completion receipt before it resets cadence."""
   87      root = Path(root).resolve()
   88      marker = Path(marker)
   89      audit = marker.parent.resolve()
   90      if not audit.is_relative_to(root / 'docs/audits') or marker.is_symlink():
   91          raise ValueError('completion marker outside audit directory')
   92      data = json.loads(marker.read_text())
   93      if not isinstance(data, dict):
   94          raise ValueError('completion marker must be a JSON object')
   95      if data.get('schema') != 1 or type(data.get('issue')) is not int:
   96          raise ValueError('invalid completed-audit schema')
   97      if not isinstance(data['completed_at'], str):
   98          raise ValueError('completion time must be a string')
   99      ended = dt.datetime.fromisoformat(data['completed_at'].replace('Z', '+00:00'))
  100      if ended.tzinfo is None or ended > now:
  101          raise ValueError('completion time is unzoned or in the future')
  102      required = {str((audit / name).relative_to(root)) for name in ['04-analysis.md', '05-punch-list.md']}
  103      required.update([data['tracker_readback'], data['tracker_completion']])
  104      if not isinstance(data['evidence'], dict):
  105          raise ValueError('completion evidence must be a JSON object')
  106      if not required.issubset(data['evidence']):
  107          raise ValueError('completion receipt omits required evidence')
  108      for name, expected in data['evidence'].items():
  109          path = root / name
  110          if Path(name).is_absolute() or path.is_symlink() or not path.resolve().is_relative_to(root):
  111              raise ValueError('unsafe completion evidence path')
  112          with path.open('rb') as stream:
  113              if hashlib.file_digest(stream, 'sha256').hexdigest() != expected:
  114                  raise ValueError('completion evidence changed: ' + name)
  115      issue = json.loads((root / data['tracker_readback']).read_text())
  116      if not isinstance(issue, dict):
  117          raise ValueError('audit tracker readback must be a JSON object')
  118      if (issue.get('number') != data['issue'] or issue.get('state') != 'closed'
  119              or issue.get('state_reason') != 'completed'
  120              or not re.search(r'^\s*- \[x\]', issue.get('body', ''), re.M)
  121              or re.search(r'^\s*- \[ \]', issue.get('body', ''), re.M)):
  122          raise ValueError('audit issue is not checked and completed')
  123      receipt = json.loads((root / data['tracker_completion']).read_text())
  124      if not isinstance(receipt, dict):
  125          raise ValueError('tracker completion receipt must be a JSON object')
  126      if (receipt.get('result') != 'PASS' or not receipt.get('exact_bodies_and_states')
  127              or data['issue'] not in receipt.get('closed_completed', [])
  128              or receipt.get('verified_utc') != data['completed_at']):
  129          raise ValueError('completion time is not the exact verified tracker receipt')
  130      return ended, data['issue']
  131  
  132  
  133  def closures_after(rows, cutoff):
  134      """Do not count findings that were closed before the audit completed."""
  135      return sum(dt.datetime.fromisoformat(row['closedAt'].replace('Z', '+00:00')) > cutoff
  136                 for row in rows)
  137  
  138  
  139  def work_log_days():
  140      """{date: [(hh:mm, title)]} for every day file."""
  141      days = {}
  142      for path in glob.glob(os.path.join(ROOT, 'docs/work-logs/*/*-work_log.md')):
  143          m = re.search(r'(\d{4})_(\d\d)_(\d\d)-work_log\.md$', path)
  144          if not m:
  145              continue
  146          d = dt.date(*map(int, m.groups()))
  147          items = []
  148          for line in open(path, encoding='utf-8'):
  149              if line.startswith('## '):
  150                  hm = re.match(r'## (\d\d:\d\d) UTC\s*[—–-]+\s*(.*)', line.strip())
  151                  items.append((hm.group(1), hm.group(2)) if hm else ('', line.strip().lstrip('# ')))
  152          days[d] = items
  153      return days
  154  
  155  
  156  def last_marker(days, word, folder):
  157      """The latest date of a docs/<folder>/<date>-*.md file or a work-log heading containing word."""
  158      best = None
  159      for path in glob.glob(os.path.join(ROOT, 'docs', folder, '*.md')):
  160          m = re.match(r'(\d{4})-(\d\d)-(\d\d)', os.path.basename(path))
  161          if m:
  162              d = dt.date(*map(int, m.groups()))
  163              best = d if best is None or d > best else best
  164      rx = re.compile(word, re.I)
  165      for d, items in days.items():
  166          if any(rx.search(t) for _, t in items):
  167              best = d if best is None or d > best else best
  168      return best
  169  
  170  
  171  def issue_coverage(ref='next', baseline=ISSUE_BASELINE, upstream='upstream/next'):
  172      """Check post-adoption fork commits, including merge messages; fail closed."""
  173      for name in (ref, baseline, upstream):
  174          rc, _, _ = sh(['git', 'rev-parse', '--verify', name + '^{commit}'])
  175          if rc:
  176              return False, 'cannot resolve required history: ' + name
  177      rc, _, _ = sh(['git', 'merge-base', '--is-ancestor', baseline, ref])
  178      if rc:
  179          return False, 'issue-policy baseline is not an ancestor of ' + ref
  180      rc, adopted, _ = sh(['git', 'show', '-s', '--format=%ct', baseline])
  181      if rc or not adopted.isdigit():
  182          return False, 'cannot read issue-policy adoption time'
  183      rc, text, _ = sh(['git', 'log', baseline + '..' + ref, '--not', upstream,
  184                        '--format=%H%x00%ct%x00%B%x00'])
  185      if rc:
  186          return False, 'cannot read fork commit messages on ' + ref
  187      fields = text.split('\0')
  188      missing = []
  189      checked = 0
  190      for i in range(0, len(fields) - 1, 3):
  191          if i + 2 >= len(fields) or not fields[i + 1].isdigit():
  192              return False, 'could not parse fork commit history'
  193          if int(fields[i + 1]) < int(adopted):
  194              continue  # old feature history merged later predates the policy
  195          checked += 1
  196          if not re.search(r'#[1-9][0-9]*\b', fields[i + 2]):
  197              missing.append(fields[i].strip()[:12])
  198      if missing:
  199          return False, 'fork commits without an issue citation: ' + ', '.join(missing)
  200      return True, '%d post-adoption fork commits on %s cite an issue' % (checked, ref)
  201  
  202  
  203  def main():
  204      if '--issues-only' in sys.argv:
  205          ok, message = issue_coverage()
  206          print(('ok' if ok else 'FAIL') + ' issues: ' + message)
  207          return 0 if ok else 1
  208      gate = '--gate' in sys.argv
  209      use_gh = '--no-gh' not in sys.argv
  210      # CEREMONY_TODAY=<yyyy-mm-dd> moves the clock, for proving a gate fires (the guard's positive)
  211      today = dt.date.fromisoformat(os.environ['CEREMONY_TODAY']) if os.environ.get('CEREMONY_TODAY') else dt.date.today()
  212      days = work_log_days()
  213      active = sorted(d for d in days if d >= SINCE)
  214      lines = []
  215      overdue = []   # (level, text): 'block' refuses a push of next; 'ci' fails the fork's CI only
  216  
  217      def report(ok, name, text):
  218          lines.append('%s  %-9s %s' % ('ok  ' if ok else 'DUE ', name, text))
  219  
  220      ok, message = issue_coverage()
  221      report(ok, 'issues', message)
  222      if not ok:
  223          overdue.append(('block', 'issues: ' + message))
  224  
  225      # 1. mini-retro: every RETRO_ACTIVE_DAYS active days
  226      # A heading counts as a retro when it *is* one -- it begins with the
  227      # ceremony's name -- not when it mentions one ("notes for the retro
  228      # later" reset the clock until audit #258 PL-004).
  229      last_retro = last_marker(days, r'^(mini-?)?retro(spective)?\b', 'retros')
  230      start = max(SINCE, last_retro) if last_retro else SINCE
  231      since_retro = [d for d in active if d > start]
  232      n = len(since_retro)
  233      if n >= RETRO_ACTIVE_DAYS + RETRO_GRACE_DAYS:
  234          overdue.append(('block', 'retro: %d active days since %s (cadence %d, grace %d) -- run the mini-retro skill; docs/retros/<date>-<scope>.md' % (n, start, RETRO_ACTIVE_DAYS, RETRO_GRACE_DAYS)))
  235          report(False, 'retro', 'OVERDUE: %d active days since %s' % (n, start))
  236      elif n >= RETRO_ACTIVE_DAYS:
  237          report(False, 'retro', 'due: %d active days since %s (blocks at %d)' % (n, start, RETRO_ACTIVE_DAYS + RETRO_GRACE_DAYS))
  238      else:
  239          report(True, 'retro', 'last %s; %d of %d active days' % (last_retro or 'none since the clock started', n, RETRO_ACTIVE_DAYS))
  240  
  241      # 2. friction log
  242      fl = os.path.join(ROOT, 'docs/friction-log.md')
  243      if not os.path.exists(fl):
  244          overdue.append(('block', 'friction: docs/friction-log.md is missing'))
  245          report(False, 'friction', 'no docs/friction-log.md')
  246      else:
  247          open_entries = []
  248          guard_rx = re.compile(r'`(tools/[A-Za-z0-9_./-]+|\.githooks/[A-Za-z0-9_./-]+|\.claude/rules/[A-Za-z0-9_./-]+\.md)`')
  249          for line in open(fl, encoding='utf-8'):
  250              m = re.match(r'- (\d{4}-\d\d-\d\d) .*issue:\s*(#\d+|none|guard)', line.strip(), re.I)
  251              if not m:
  252                  continue
  253              d = dt.date.fromisoformat(m.group(1))
  254              what = m.group(2).lower()
  255              # `issue: guard` is a claim that a tool, hook or rule now catches
  256              # the shape; it holds only when the line names one, in backticks,
  257              # that exists -- as a blindspot entry must (audit #258 PL-004).
  258              if what == 'guard' and not any(os.path.exists(os.path.join(ROOT, g)) for g in guard_rx.findall(line)):
  259                  what = 'none'
  260              if what == 'none' and (today - d).days > FRICTION_ISSUE_DAYS and d >= SINCE:
  261                  open_entries.append(line.strip()[:110])
  262          if open_entries:
  263              overdue.append(('block', 'friction: %d entrie(s) older than %d days without an issue or a guard' % (len(open_entries), FRICTION_ISSUE_DAYS)))
  264              report(False, 'friction', 'OVERDUE: %d entrie(s) without an issue past %d days' % (len(open_entries), FRICTION_ISSUE_DAYS))
  265              for e in open_entries[:5]:
  266                  lines.append('             %s' % e)
  267          else:
  268              report(True, 'friction', 'every entry since %s has an issue or a guard within %d days' % (SINCE, FRICTION_ISSUE_DAYS))
  269  
  270      # 3. weekly and monthly summaries
  271      last_week_end = today - dt.timedelta(days=today.isoweekday())      # last Sunday
  272      if last_week_end >= SINCE + dt.timedelta(days=6):
  273          iso = last_week_end.isocalendar()
  274          wk = '%04d-W%02d' % (iso[0], iso[1])
  275          wpath = os.path.join(ROOT, 'docs/work-logs/%04d_%02d-work_logs/%s-summary.md' % (last_week_end.year, last_week_end.month, wk))
  276          if os.path.exists(wpath):
  277              report(True, 'weekly', '%s summary present' % wk)
  278          elif (today - last_week_end).days > WEEKLY_GRACE_DAYS:
  279              overdue.append(('block', 'weekly: %s summary missing (%s)' % (wk, os.path.relpath(wpath, ROOT))))
  280              report(False, 'weekly', 'OVERDUE: %s summary missing' % wk)
  281          else:
  282              report(False, 'weekly', 'due: %s summary by %s' % (wk, last_week_end + dt.timedelta(days=WEEKLY_GRACE_DAYS)))
  283      else:
  284          report(True, 'weekly', 'the first full week since the clock started has not ended')
  285      first_of_month = today.replace(day=1)
  286      prev_month_end = first_of_month - dt.timedelta(days=1)
  287      if prev_month_end >= SINCE:
  288          mpath = os.path.join(ROOT, 'docs/work-logs/%04d_%02d-work_logs/SUMMARY.md' % (prev_month_end.year, prev_month_end.month))
  289          if os.path.exists(mpath):
  290              report(True, 'monthly', '%04d-%02d summary present' % (prev_month_end.year, prev_month_end.month))
  291          elif (today - prev_month_end).days > MONTHLY_GRACE_DAYS:
  292              overdue.append(('block', 'monthly: %04d-%02d summary missing' % (prev_month_end.year, prev_month_end.month)))
  293              report(False, 'monthly', 'OVERDUE: %04d-%02d summary missing' % (prev_month_end.year, prev_month_end.month))
  294          else:
  295              report(False, 'monthly', 'due: %04d-%02d summary by the %dth' % (prev_month_end.year, prev_month_end.month, MONTHLY_GRACE_DAYS))
  296      else:
  297          report(True, 'monthly', 'no month has ended since the clock started')
  298  
  299      # 4. the index and the register
  300      rc, out, _ = sh([os.path.join(ROOT, 'tools/work-log-index'), '--check'])
  301      if rc == 0:
  302          report(True, 'index', out or 'current')
  303      else:
  304          overdue.append(('block', 'index: ' + (out or 'stale')))
  305          report(False, 'index', out or 'stale')
  306      rc, out, err = sh([os.path.join(ROOT, 'tools/register-check')])
  307      if rc == 0:
  308          report(True, 'register', (out or 'ok').splitlines()[-1][:100])
  309      else:
  310          overdue.append(('block', 'register: ' + ((out or err).splitlines() or ['failed'])[-1][:120]))
  311          report(False, 'register', 'FAIL')
  312      rc, out, err = sh([os.path.join(ROOT, 'tools/rules-check'), '--quiet'])
  313      if rc == 0:
  314          report(True, 'rules', 'every rule file front-mattered and indexed')
  315      else:
  316          overdue.append(('block', 'rules: ' + ((out or err).splitlines() or ['failed'])[-1][:120]))
  317          report(False, 'rules', (out or err).strip().replace('\n', '; ')[:160])
  318  
  319      # 5. blindspot guards
  320      bs = os.path.join(ROOT, 'docs/blindspot-register.md')
  321      unguarded = []
  322      if os.path.exists(bs):
  323          text = open(bs, encoding='utf-8').read()
  324          parts = re.split(r'^## (\d+)\. ', text, flags=re.M)
  325          for i in range(1, len(parts), 2):
  326              num = int(parts[i])
  327              body = parts[i + 1]
  328              if num < GUARD_FROM:
  329                  continue
  330              names = re.findall(r'`(tools/[A-Za-z0-9_./-]+|\.githooks/[A-Za-z0-9_./-]+|\.claude/rules/[A-Za-z0-9_./-]+\.md)`', body)
  331              found = [n for n in names if os.path.exists(os.path.join(ROOT, n))]
  332              if not found:
  333                  unguarded.append(num)
  334          if unguarded:
  335              overdue.append(('block', 'guards: blindspot entries %s name no guard that exists in the tree' % unguarded))
  336              report(False, 'guards', 'blindspots without a guard: %s' % unguarded)
  337          else:
  338              report(True, 'guards', 'every entry from %d names a guard in the tree' % GUARD_FROM)
  339  
  340      # 5b. the open checkboxes (D-QA-044; needs gh). CI red, not push-blocking,
  341      # like the hygiene check below: the fix is a tracker edit, not a file.
  342      # Blocking since 2026-09-25, when #268's sweep reached 0; a checker that
  343      # cannot run (gh down) has not passed either.
  344      rc, out, err = sh([os.path.join(ROOT, 'tools/box-check'), '--quiet'])
  345      last = ((out or err).strip().splitlines() or ['box-check did not run'])[-1]
  346      report(rc == 0, 'checkboxes', last[:140])
  347      if rc != 0:
  348          overdue.append(('ci', 'checkboxes: %s -- tick each with its evidence or reword it to the VM or a named physical fact (issue-tracking.md, D-QA-044)' % last[:100]))
  349  
  350      # 6. audits and futros (the tracker)
  351      if use_gh:
  352          data, err = gh_json(['issue', 'list', '--repo', REPO, '--state', 'all', '--limit', '100', '--search',
  353                               'Audit in:title', '--json', 'number,title,createdAt'])
  354          last_audit = None
  355          if err:
  356              report(False, 'audit', 'gh failed: %s' % err[:80])
  357              overdue.append(('ci', 'audit: the tracker did not answer (%s)' % err[:60]))
  358          else:
  359              for it in data or []:
  360                  if re.match(r'(Audit|Code audit)\b', it['title']):
  361                      d = dt.date.fromisoformat(it['createdAt'][:10])
  362                      last_audit = d if last_audit is None or d > last_audit else last_audit
  363              for path in glob.glob(os.path.join(ROOT, 'docs/audits/*')):
  364                  m = re.match(r'(\d{4})-(\d\d)-(\d\d)', os.path.basename(path))
  365                  if m:
  366                      d = dt.date(*map(int, m.groups()))
  367                      last_audit = d if last_audit is None or d > last_audit else last_audit
  368              start = max(SINCE, last_audit) if last_audit else SINCE
  369              cutoff = dt.datetime.combine(start, dt.time.min, tzinfo=dt.timezone.utc)
  370              completed_by = None
  371              for marker in glob.glob(os.path.join(ROOT, 'docs/audits/*/audit-completion.json')):
  372                  try:
  373                      ended, issue = completed_audit_marker(marker, ROOT, dt.datetime.now(dt.timezone.utc))
  374                      rc, out, err = sh([os.path.join(ROOT, 'tools/lint-audit-artifacts'),
  375                                         os.path.dirname(marker), '--phase', 'resolution'])
  376                      if rc:
  377                          raise ValueError('resolution lint failed: ' + (out or err)[-160:])
  378                      if ended > cutoff:
  379                          cutoff, completed_by = ended, '#%d %s' % (issue, os.path.relpath(marker, ROOT))
  380                  except (OSError, ValueError, KeyError, TypeError) as error:
  381                      overdue.append(('ci', 'audit: invalid completion marker %s: %s' % (marker, error)))
  382              start = cutoff.date()
  383              closed, err2 = gh_json(['issue', 'list', '--repo', REPO, '--state', 'closed', '--limit', '200',
  384                                      '--search', 'closed:>=%s reason:completed' % start.isoformat(), '--json', 'number,closedAt'])
  385              if err2:
  386                  overdue.append(('ci', 'audit: closure tracker did not answer (%s)' % err2[:80]))
  387              try:
  388                  nclosed = closures_after(closed or [], cutoff)
  389              except (KeyError, TypeError, ValueError) as error:
  390                  overdue.append(('ci', 'audit: invalid closure timestamp (%s)' % error))
  391                  nclosed = 0
  392              ndays = (today - start).days
  393              if nclosed >= AUDIT_CLOSED_ISSUES or ndays >= AUDIT_DAYS:
  394                  overdue.append(('ci', 'audit: %d issues closed and %d days since %s (cadence %d issues or %d days) -- run the code-auditor skill' % (nclosed, ndays, start, AUDIT_CLOSED_ISSUES, AUDIT_DAYS)))
  395                  report(False, 'audit', 'OVERDUE: %d closed, %d days since %s' % (nclosed, ndays, start))
  396              else:
  397                  report(not err2, 'audit', 'last %s%s; %d of %d closed issues, %d of %d days' % (
  398                      cutoff.isoformat(), ' via ' + completed_by if completed_by else '',
  399                      nclosed, AUDIT_CLOSED_ISSUES, ndays, AUDIT_DAYS))
  400          epics, err = gh_json(['issue', 'list', '--repo', REPO, '--state', 'open', '--label', 'epic', '--limit', '50',
  401                                '--json', 'number,title,createdAt'])
  402          if err:
  403              report(False, 'futro', 'gh failed: %s' % err[:80])
  404          else:
  405              last_futro = last_marker(days, r'\bfutro\b', 'futros')
  406              missing = []
  407              for it in epics or []:
  408                  d = dt.date.fromisoformat(it['createdAt'][:10])
  409                  if d < SINCE:
  410                      continue
  411                  if (last_futro is None or last_futro < d) and (today - d).days > FUTRO_AFTER_EPIC_DAYS:
  412                      missing.append('#%d' % it['number'])
  413              if missing:
  414                  overdue.append(('ci', 'futro: epics %s opened since %s with no futro within %d days' % (' '.join(missing), SINCE, FUTRO_AFTER_EPIC_DAYS)))
  415                  report(False, 'futro', 'OVERDUE for %s' % ' '.join(missing))
  416              else:
  417                  report(True, 'futro', 'last %s; no epic since %s without one' % (last_futro or 'none', SINCE))
  418          # 7. issue hygiene (audit #258 PL-008, P-03): an issue closed as completed
  419          # with a checkbox still open is a delivered item nobody ticked, or a
  420          # criterion nobody struck -- #225 closed with five of them. Read from
  421          # the tracker since the clock; CI red, not push-blocking, since the fix
  422          # is a tracker edit and not a file.
  423          closed_bodies, err = gh_json(['issue', 'list', '--repo', REPO, '--state', 'closed', '--limit', '200',
  424                                        '--search', 'closed:>=%s reason:completed' % SINCE.isoformat(), '--json', 'number,body'])
  425          if err:
  426              report(False, 'hygiene', 'gh failed: %s' % err[:80])
  427          else:
  428              with_open = ['#%d' % it['number'] for it in closed_bodies or []
  429                           if re.search(r'^\s*- \[ \]', it.get('body') or '', re.M)]
  430              if with_open:
  431                  overdue.append(('ci', 'hygiene: closed as completed with an open checkbox: %s -- tick it with its evidence or strike it with the decision (issue-tracking.md)' % ' '.join(with_open)))
  432                  report(False, 'hygiene', 'closed-completed issues with an open checkbox: %s' % ' '.join(with_open))
  433              else:
  434                  report(True, 'hygiene', 'no issue closed completed since %s carries an open checkbox' % SINCE)
  435      else:
  436          report(True, 'audit', 'not checked (--no-gh)')
  437          report(True, 'futro', 'not checked (--no-gh)')
  438          report(True, 'hygiene', 'not checked (--no-gh)')
  439  
  440      blocking = [t for lv, t in overdue if lv == 'block']
  441      ci_only = [t for lv, t in overdue if lv == 'ci']
  442      if gate:
  443          for t in blocking:
  444              print('ceremony-check: BLOCK ' + t)
  445          for t in ci_only:
  446              print('ceremony-check: overdue (CI is red, the push goes through) ' + t)
  447          return 1 if blocking else 0
  448      print('ceremony-check (clock since %s, today %s)' % (SINCE, today))
  449      for l in lines:
  450          print('  ' + l)
  451      if overdue:
  452          print('\n%d overdue. %d refuse a push of next; every one keeps the fork CI red until its artifact exists:' % (len(overdue), len(blocking)))
  453          for lv, t in overdue:
  454              print('  - [%s] %s' % ('push+CI' if lv == 'block' else 'CI', t))
  455          return 1
  456      print('\nnothing overdue.')
  457      return 0
  458  
  459  
  460  if __name__ == '__main__':
  461      sys.exit(main())
```

## File: tools/es-menu-map-check (at 8ebaf8daad, 200 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # es-menu-map-check -- does docs/es-menu-map.md still describe the menus that ship?
    6  #
    7  # The map is how a new feature gets placed rather than invented, and
    8  # .claude/rules/es-native-ui.md has asked since 2026-08-19 that a row added,
    9  # moved or renamed updates it in the same change. That promise did not hold:
   10  # on 2026-09-18 twenty-eight of the forty-one page titles in the shipped
   11  # binary were absent from the map, among them screens this fork wrote itself
   12  # (FINISH RESTORE SETUP, CLOUD REMOTE SETUP, WHICH REMOTE?). A practice that
   13  # nothing checks is a practice that decays silently, which is the whole
   14  # argument of engineering-practices.md -- so this is the check.
   15  #
   16  # It reads the EmulationStation source at the commit the image actually
   17  # ships (PKG_VERSION in the emulationstation package), not a working tree,
   18  # because the working tree is usually someone's feature branch and the
   19  # question is about what players have.
   20  #
   21  #   tools/es-menu-map-check [--es-src DIR] [--ref COMMIT] [--quiet]
   22  #
   23  # A screen this fork deliberately does not map -- an upstream page ROCKNIX
   24  # hides, a Kodi or Batocera-store leftover -- is declared in the map itself,
   25  # under "## Not mapped", as `- TITLE -- why`. The declaration lives beside
   26  # the map rather than in this tool so the reader of the map sees the same
   27  # list the check enforces, and so a reason is written down once.
   28  #
   29  # Exits 0 when every screen is mapped or declared, 1 when something is
   30  # neither -- or when a declaration names a screen that no longer exists --
   31  # and 2 when the check could not run at all (no source, no map, an
   32  # unreadable ref), because a check that cannot run has not passed.
   33  
   34  from __future__ import annotations
   35  
   36  import argparse
   37  import os
   38  import re
   39  import subprocess
   40  import sys
   41  from pathlib import Path
   42  
   43  REPO = Path(__file__).resolve().parent.parent
   44  MAP = REPO / "docs" / "es-menu-map.md"
   45  PKG = REPO / "projects/ROCKNIX/packages/ui/emulationstation/package.mk"
   46  DEFAULT_SRC = Path.home() / "Development" / "emulationstation-next"
   47  
   48  # Where a screen's title is written. Each pattern's one group is the title.
   49  SCREEN_PATTERNS = [
   50      # new GuiSettings(window, _("TITLE")) -- the ordinary settings page
   51      re.compile(r'new\s+GuiSettings\s*\(\s*\w+\s*,\s*_\("([^"]+)"\)'),
   52      # auto s = GuiSettings(mWindow, _("TITLE")) -- constructed directly
   53      re.compile(r'(?<!new )\bGuiSettings\s*\(\s*m?[Ww]indow\s*,\s*_\("([^"]+)"\)'),
   54      # MenuComponent(window, _("TITLE")) -- a page built on the menu component
   55      re.compile(r'MenuComponent\s*\(\s*\w+\s*,\s*_\("([^"]+)"\)'),
   56  ]
   57  
   58  SOURCE_DIRS = ["es-app/src/guis", "es-core/src/guis"]
   59  
   60  
   61  def die(message: str) -> None:
   62      print(f"es-menu-map-check: {message}", file=sys.stderr)
   63      raise SystemExit(2)
   64  
   65  
   66  def shipped_ref() -> str:
   67      """The commit the image ships, from the package recipe."""
   68      try:
   69          text = PKG.read_text(encoding="utf-8")
   70      except OSError as exc:
   71          die(f"cannot read {PKG}: {exc}")
   72      match = re.search(r'^PKG_VERSION="([0-9a-f]{7,40})"', text, re.M)
   73      if not match:
   74          die(f"no PKG_VERSION commit in {PKG}")
   75      return match.group(1)
   76  
   77  
   78  def source_files(src: Path, ref: str) -> dict[str, str]:
   79      """Every guis/*.cpp at `ref`, as {path: text}."""
   80      try:
   81          listing = subprocess.run(
   82              ["git", "-C", str(src), "ls-tree", "-r", "--name-only", ref, *SOURCE_DIRS],
   83              capture_output=True, text=True, check=True,
   84          ).stdout.split()
   85      except (OSError, subprocess.CalledProcessError) as exc:
   86          die(f"cannot list {ref} in {src}: {exc}")
   87      files = {}
   88      for path in listing:
   89          if not path.endswith(".cpp"):
   90              continue
   91          try:
   92              files[path] = subprocess.run(
   93                  ["git", "-C", str(src), "show", f"{ref}:{path}"],
   94                  capture_output=True, text=True, check=True,
   95              ).stdout
   96          except (OSError, subprocess.CalledProcessError) as exc:
   97              die(f"cannot read {path} at {ref}: {exc}")
   98      if not files:
   99          die(f"no {' or '.join(SOURCE_DIRS)} sources at {ref} in {src}")
  100      return files
  101  
  102  
  103  def screens(files: dict[str, str]) -> dict[str, str]:
  104      """{title: the file it is built in} for every screen in the source."""
  105      found: dict[str, str] = {}
  106      for path, text in files.items():
  107          for pattern in SCREEN_PATTERNS:
  108              for match in pattern.finditer(text):
  109                  found.setdefault(match.group(1), path.rsplit("/", 1)[-1])
  110      return found
  111  
  112  
  113  def map_text_and_exclusions() -> tuple[str, dict[str, str]]:
  114      """The map's prose, and the screens it declares it does not cover."""
  115      try:
  116          text = MAP.read_text(encoding="utf-8")
  117      except OSError as exc:
  118          die(f"cannot read {MAP}: {exc}")
  119      exclusions: dict[str, str] = {}
  120      section = re.search(r"^## Not mapped\b.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
  121      if section:
  122          for line in section.group(1).splitlines():
  123              # Split on the first " -- " (or em dash), not on a character
  124              # class: a title may itself contain a hyphen (WI-FI PASSWORD),
  125              # and a parser that cannot hold the titles we actually use is
  126              # a parser that silently drops declarations.
  127              entry = re.match(r"\s*-\s+(.+?)\s+(?:--|—)\s+(.+)$", line)
  128              if entry:
  129                  title = entry.group(1).strip().strip("*").strip("`").strip()
  130                  exclusions[title] = entry.group(2).strip()
  131      return text, exclusions
  132  
  133  
  134  def names_screen(text: str, title: str) -> bool:
  135      """Does the map name this screen as a screen -- not merely mention its words?
  136  
  137      A heading, a bold token, a backticked token, a mermaid node label, or a
  138      line that begins with the title. Until audit #258 PL-021 the test was a
  139      case-insensitive substring of the whole document, so a screen called
  140      TOOLS was "mapped" by any sentence with the word tools in it. Exact
  141      case: the map writes screen titles as the interface does, in capitals,
  142      and a title in running prose is lower-case by the same convention.
  143      """
  144      t = re.escape(title)
  145      shapes = [
  146          r"^#{1,6}\s+.*\b" + t + r"\b",              # a heading naming it
  147          r"\*\*" + t + r"\*\*",                     # **TITLE**
  148          r"`" + t + r"`",                             # `TITLE`
  149          r"[\[{(]\s*" + t + r"(?:<br/>|[\]})>])",     # a mermaid node label
  150          r"^\s*[-*]?\s*" + t + r"\b",                # a line, or a list item, that begins with it
  151          r"\b" + t + r"\b",                           # the title as a whole token, its own capitals
  152      ]
  153      return any(re.search(shape, text, re.M) for shape in shapes)
  154  
  155  
  156  def main() -> int:
  157      parser = argparse.ArgumentParser(add_help=True)
  158      parser.add_argument("--es-src", default=os.environ.get("ES_SRC", str(DEFAULT_SRC)))
  159      parser.add_argument("--ref", default=None, help="default: the shipped PKG_VERSION")
  160      parser.add_argument("--quiet", action="store_true")
  161      args = parser.parse_args()
  162  
  163      src = Path(args.es_src).expanduser()
  164      if not (src / ".git").exists():
  165          die(f"{src} is not an EmulationStation checkout (--es-src or ES_SRC)")
  166      ref = args.ref or shipped_ref()
  167  
  168      found = screens(source_files(src, ref))
  169      text, exclusions = map_text_and_exclusions()
  170  
  171      missing = {}
  172      for title, where in sorted(found.items()):
  173          if title in exclusions:
  174              continue
  175          if names_screen(text, title):
  176              continue
  177          missing[title] = where
  178  
  179      # An exclusion for a screen that no longer exists is stale: it was
  180      # written for something that has since been renamed or removed, and it
  181      # will silently excuse a future screen that happens to reuse the name.
  182      stale = sorted(set(exclusions) - set(found))
  183  
  184      if not args.quiet:
  185          print(f"{len(found)} screen(s) at {ref[:9]}, "
  186                f"{len(found) - len(missing) - len(exclusions)} in the map, "
  187                f"{len(exclusions)} declared unmapped, {len(missing)} missing")
  188          for title, where in missing.items():
  189              print(f"  MISSING  {title}  ({where})")
  190          for title in stale:
  191              print(f"  STALE    {title} is declared unmapped but no longer exists")
  192  
  193      # A stale declaration counts as a failure too. It is not cosmetic: it
  194      # sits there excusing a title that no longer exists, and will silently
  195      # excuse the next screen that reuses the name. Fail closed.
  196      return 1 if (missing or stale) else 0
  197  
  198  
  199  if __name__ == "__main__":
  200      sys.exit(main())
```

## File: tools/fork-package-freshness (at 8ebaf8daad, 164 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # fork-package-freshness -- are the packages this fork introduces at their
    6  # current upstream release?
    7  #
    8  #   tools/fork-package-freshness              # every fork-introduced package
    9  #   tools/fork-package-freshness rclone ...   # only these
   10  #   tools/fork-package-freshness --list       # name the packages and stop
   11  #
   12  # Exit 0 when every package is CURRENT, PINNED on purpose, INHERITED or
   13  # LOCAL; 1 when any is BEHIND; 2 when any could not be checked (UNKNOWN):
   14  # a check that cannot run has not passed (engineering-practices.md).
   15  #
   16  # Which packages: every package.mk on HEAD_REF (next) that is absent on
   17  # BASE_REF (upstream/next) -- the fork added it -- plus EXTRA_PACKAGES,
   18  # recipes the fork owns although upstream carries a copy. Maintainer,
   19  # 2026-09-20 (fork #227, D-WORKFLOW-024): "we should also make sure that
   20  # packages we're introducing into the system are up to date ... it's a good
   21  # idea to have everything as up to date as possible when we submit it."
   22  #
   23  # How "latest" is found, by the host PKG_URL points at:
   24  #   github.com               the latest release, else the newest release-shaped tag
   25  #   codeberg.org             the newest stable version among repository tags
   26  #   download.gnome.org       cache.json, even minor versions only (GNOME stable)
   27  #   ftp.gnu.org / savannah   the directory listing
   28  #   webkitgtk.org            the release listing, even minor versions only
   29  #   cache.ruby-lang.org      ruby/ruby tags in the minor series the recipe names
   30  #                            (# freshness: series X.Y -- <why>), else the version's own
   31  #   downloads.rclone.org     rclone/rclone's latest release
   32  #   dotat.at                 the directory listing, else fanf2/unifdef on GitHub
   33  # A PKG_VERSION that is a commit hash is compared with the default branch of
   34  # the repository PKG_SITE names and reported as commits behind it. A recipe
   35  # that must stay where it is says what it follows:
   36  #   # freshness: pinned -- <why>
   37  # and is reported PINNED. A recipe with no PKG_VERSION of its own sources
   38  # upstream's generic recipe (INHERITED); one with no PKG_URL is ours (LOCAL).
   39  set -uo pipefail
   40  
   41  ROOT=$(cd "$(dirname "$0")/.." && pwd)
   42  HEAD_REF=${FRESHNESS_HEAD:-next}
   43  BASE_REF=${FRESHNESS_BASE:-upstream/next}
   44  EXTRA_PACKAGES="projects/ROCKNIX/packages/network/rclone"
   45  
   46  var() { grep -m1 "^${2}=" "$1" | cut -d'"' -f2; }
   47  newest() { sort -V | tail -1; }
   48  release_only() { grep -E '^[0-9]+(\.[0-9]+)+$'; }          # no rc, alpha, beta
   49  tag_version() { sed -E 's/^[^0-9]*//; s/_/./g'; }          # v1.2.0, libpsl-0.21.0, v3_3_12
   50  github_repo() { sed -nE 's#^https?://github\.com/([^/]+/[^/#?]+).*#\1#p' <<<"$1" | sed 's/\.git$//'; }
   51  
   52  latest_github() {  # <owner/repo>
   53      local v
   54      v=$(gh api "repos/$1/releases/latest" --jq .tag_name 2>/dev/null | tag_version | release_only)
   55      [ -n "$v" ] && { echo "$v"; return; }
   56      gh api "repos/$1/tags?per_page=50" --jq '.[].name' 2>/dev/null | tag_version | release_only | newest
   57  }
   58  latest_codeberg() {  # <owner/repo>
   59      local tags
   60      tags=$(curl -fsSL --max-time 30 "https://codeberg.org/api/v1/repos/$1/tags?limit=50" 2>/dev/null) || return 1
   61      python3 -c 'import json, sys; print("\n".join(tag["name"] for tag in json.load(sys.stdin)))' <<<"$tags" 2>/dev/null \
   62          | tag_version | release_only | newest
   63  }
   64  latest_gnome() {  # <module>
   65      curl -fsSL --max-time 30 "https://download.gnome.org/sources/$1/cache.json" 2>/dev/null | python3 -c '
   66  import json, sys, re
   67  d = json.load(sys.stdin); p = sys.argv[1]
   68  vs = [v for v in d[2].get(p, []) if re.fullmatch(r"\d+\.\d+(\.\d+)?", v)]
   69  vs = [v for v in vs if int(v.split(".")[1]) % 2 == 0]
   70  vs.sort(key=lambda s: [int(x) for x in s.split(".")])
   71  print(vs[-1] if vs else "")' "$1"
   72  }
   73  latest_listing() {  # <directory url> <name>
   74      curl -fsSL --max-time 30 "$1" 2>/dev/null | grep -oE "$2-[0-9]+(\.[0-9]+)+\.tar" | sed -E "s/^$2-//; s/\.tar$//" | newest
   75  }
   76  latest_webkitgtk() {
   77      curl -fsSL --max-time 30 https://webkitgtk.org/releases/ 2>/dev/null \
   78          | grep -oE 'webkitgtk-2\.[0-9]*[02468]\.[0-9]+\.tar\.xz' | sed -E 's/^webkitgtk-//; s/\.tar\.xz$//' | newest
   79  }
   80  latest_ruby() {  # <recipe version, or a series X.Y> -- newest in that minor series
   81      local series=$1
   82      [[ $series =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] && series=${series%.*}
   83      gh api "repos/ruby/ruby/tags?per_page=100" --jq '.[].name' 2>/dev/null | grep -E "^v${series//./_}_[0-9]+$" | tag_version | newest
   84  }
   85  commits_behind() {  # <owner/repo> <sha>
   86      gh api "repos/$1/compare/$2...HEAD" --jq 'if .ahead_by == 0 then "0 behind"
   87          else "\(.ahead_by) behind \(.commits[-1].sha[0:10]) (\(.commits[-1].commit.committer.date[0:10]))" end' 2>/dev/null
   88  }
   89  packages() {
   90      # Only build-engine recipe roots; docs/ holds immutable historical fixtures.
   91      git -C "$ROOT" diff --name-only --diff-filter=A "$BASE_REF" "$HEAD_REF" -- packages projects | sed -n 's|/package.mk$||p'
   92      for p in $EXTRA_PACKAGES; do echo "$p"; done
   93  }
   94  
   95  if [ "${1:-}" = "--list" ]; then packages; exit 0; fi
   96  
   97  rc=0
   98  printf '%-26s %-14s %-14s %s\n' PACKAGE RECIPE LATEST VERDICT
   99  while read -r d; do
  100      name=$(basename "$d")
  101      if [ $# -gt 0 ]; then case " $* " in *" $name "*) ;; *) continue ;; esac; fi
  102      f="$ROOT/$d/package.mk"
  103      if [ ! -f "$f" ]; then printf '%-26s %-14s %-14s %s\n' "$name" - - "UNKNOWN: no package.mk in the working tree"; rc=2; continue; fi
  104      ver=$(var "$f" PKG_VERSION); url=$(var "$f" PKG_URL); site=$(var "$f" PKG_SITE)
  105      pinned=$(grep -m1 -E '^# freshness: pinned -- ' "$f" | sed 's/^# freshness: pinned -- //')
  106      # A recipe held to a minor series says so in the same place, and the tool
  107      # follows the recipe rather than carrying the rule itself (audit #258 PL-027).
  108      series_line=$(grep -m1 -E '^# freshness: series [0-9]+\.[0-9]+ -- ' "$f")
  109      series=${series_line#\# freshness: series }; series=${series%% -- *}
  110      series_why=${series_line#* -- }
  111      [ -n "$series_line" ] || { series=""; series_why=""; }
  112      latest=""; verdict=""
  113      if [ -z "$ver" ] && grep -qE '^\. .*/package\.mk' "$f"; then
  114          verdict="INHERITED"
  115      elif [ -z "$url" ]; then
  116          verdict="LOCAL"
  117      elif [ -z "$ver" ]; then
  118          verdict="UNKNOWN: PKG_URL without a PKG_VERSION"; rc=2
  119      elif [[ "$ver" =~ ^[0-9a-f]{40}$ ]]; then
  120          repo=$(github_repo "$site")
  121          if [ -z "$repo" ]; then
  122              verdict="UNKNOWN: PKG_SITE is not a GitHub repository"; rc=2
  123          else
  124              behind=$(commits_behind "$repo" "$ver"); latest=${behind%% *}
  125              case "$behind" in
  126                  "")   verdict="UNKNOWN: compare failed for $repo"; rc=2 ;;
  127                  0\ *) verdict="CURRENT (the pin is HEAD)" ;;
  128                  *)    if [ -n "$pinned" ]; then verdict="PINNED: $pinned ($behind)"
  129                        else verdict="BEHIND: $behind"; [ $rc -lt 1 ] && rc=1; fi ;;
  130              esac
  131          fi
  132      else
  133          # the recipe's own URL pattern, with its version; variables a recipe sets
  134          # elsewhere (rclone's RCLONE_ARCH) expand empty, the host survives
  135          eurl=$( set +u; PKG_VERSION=$ver; PKG_NAME=$name; SOURCEFORGE_SRC=https://downloads.sourceforge.net/project
  136                  eval "$(grep -E '^PKG_(NAME|SITE)=' "$f")"; eval "$(grep -m1 '^PKG_URL=' "$f")"; echo "$PKG_URL" )
  137          host=$(sed -E 's#^[a-z]+://([^/]+).*#\1#' <<<"$eurl")
  138          case "$eurl" in
  139              https://downloads.rclone.org/*) latest=$(latest_github rclone/rclone) ;;
  140              *cache.ruby-lang.org/*)         latest=$(latest_ruby "${series:-$ver}") ;;
  141              *webkitgtk.org/*)               latest=$(latest_webkitgtk) ;;
  142              *download.gnome.org/sources/*)  latest=$(latest_gnome "$(sed -nE 's#.*/sources/([^/]+)/.*#\1#p' <<<"$eurl")") ;;
  143              *ftp.gnu.org/gnu/*|*savannah.gnu.org/releases/*)
  144                                              latest=$(latest_listing "$(dirname "${eurl/#http:/https:}")/" "$name") ;;
  145              *dotat.at/*)                    latest=$(latest_listing "$(dirname "$eurl")/" "$name")
  146                                              [ -n "$latest" ] || latest=$(latest_github fanf2/unifdef) ;;   # dotat.at is often down; same author, same tags
  147              *github.com/*)                  latest=$(latest_github "$(github_repo "$eurl")") ;;
  148              https://codeberg.org/*)         latest=$(latest_codeberg "$(sed -nE 's#^https://codeberg\.org/([^/]+/[^/]+).*#\1#p' <<<"$eurl")") ;;
  149          esac
  150          if [ -z "$latest" ]; then
  151              if [ -n "$pinned" ]; then verdict="PINNED: $pinned (latest not resolvable)"
  152              else verdict="UNKNOWN: no resolver for $host, or it did not answer"; rc=2; fi
  153          elif [ "$latest" = "$ver" ]; then
  154              verdict="CURRENT"; [ -n "$series" ] && verdict="CURRENT in series $series: $series_why"
  155          elif [ "$(printf '%s\n%s\n' "$ver" "$latest" | newest)" = "$latest" ]; then
  156              if [ -n "$pinned" ]; then verdict="PINNED: $pinned (latest $latest)"
  157              else verdict="BEHIND"; [ $rc -lt 1 ] && rc=1; fi
  158          else
  159              verdict="AHEAD of upstream's latest"
  160          fi
  161      fi
  162      printf '%-26s %-14s %-14s %s\n' "$name" "${ver:0:14}" "${latest:0:14}" "$verdict"
  163  done < <(packages)
  164  exit $rc
```

## File: tools/lint-audit-artifacts (at 8ebaf8daad, 394 lines)

```text
    1  #!/usr/bin/env python3
    2  """Check a code-auditor audit folder against the artifact contract.
    3  
    4      tools/lint-audit-artifacts docs/audits/<folder> [--issue N]
    5      tools/lint-audit-artifacts docs/audits/<folder> --phase pre-issue
    6  
    7  SKILL.md § Phase 6 says to run an artifact-contract lint before creating the
    8  punch-list issue, and to verify the contract by hand where none exists. The
    9  2026-08-24 run did it by hand and missed two things, so this exists instead:
   10  
   11  * a punch item recorded Resolved/Deferred with no commit or issue to point at
   12    (PL-01 claimed a merge that had not happened - asserted from memory),
   13  * the audit issue created with prose headings and no tickable list, so the
   14    Phase 7 gate lived in the file and not in the tracker.
   15  
   16  Both are mechanically checkable. Manual verification is not.
   17  The explicit pre-issue phase permits honestly open findings before Phase 6
   18  creates their tracker. The default resolution phase still requires outcomes;
   19  pre-issue success never certifies a completed audit or release gate (#470).
   20  """
   21  import argparse, hashlib, json, pathlib, re, subprocess, sys
   22  
   23  REQUIRED = ["01-research-notes.md", "02-forward-audit.md", "03-retrospective.md",
   24              "04-analysis.md", "05-punch-list.md"]
   25  ANALYSIS_SECTIONS = ["Executive summary", "Acceptance-criteria scorecard",
   26                       "Risk assessment", "Coverage boundary", "Quality self-check"]
   27  
   28  
   29  def check_review_plan(d, milestone, bad, ok):
   30      """D-WORKFLOW-137: validate declared diversity against actual call receipts."""
   31  
   32      def require(condition, detail):
   33          if not condition:
   34              raise ValueError(detail)
   35      root = d / 'second-opinions'
   36      try:
   37          plan = json.loads((root / 'review-plan.json').read_text())
   38          primary = plan['primary']
   39          depth, reviewers = (plan['depth'], plan['reviewers'])
   40          count = {'local': 0, 'independent': 1, 'extended': 2}[depth]
   41          require(plan['schema_version'] == 1, 'unsupported review-plan schema')
   42          require(isinstance(reviewers, list) and len(reviewers) == count, 'reviewer count does not match selected depth')
   43          require(all(isinstance(primary[k], str) and primary[k].strip()
   44                      for k in ('harness', 'model', 'lab', 'identity_source')),
   45                  'primary identity metadata is incomplete')
   46          require(primary['lab'] not in ('unknown', ''), 'primary model lab is unknown')
   47          if primary['model'] != 'unknown':
   48              require(primary['model'].split('/', 1)[0] == primary['lab'], 'primary model and lab disagree')
   49          if depth == 'local':
   50              require('-issue-' in d.name, 'local-only cannot satisfy Epic/Milestone')
   51          labs, members, outputs = ({primary['lab']}, set(), set())
   52          for reviewer in reviewers:
   53              member, model, lab = (reviewer[k] for k in ('member', 'model', 'lab'))
   54              require(member in ('claude', 'gpt', 'gemini', 'kimi', 'muse'), 'reviewer is not an installed active member')
   55              require(member not in members and lab not in labs, 'reviewers must be from distinct labs')
   56              member_labs = {'claude': 'anthropic', 'gpt': 'openai', 'gemini': 'google',
   57                             'kimi': 'moonshotai', 'muse': 'meta'}
   58              require(member_labs[member] == lab, 'reviewer member and lab disagree')
   59              require(isinstance(model, str) and model.startswith(lab + '/'), 'reviewer model and lab disagree')
   60              require(isinstance(reviewer['effort'], str) and reviewer['effort'], 'reviewer effort is missing')
   61              labs.add(lab)
   62              members.add(member)
   63              calls = reviewer['calls']
   64              required_phases = ['blind', 'refutation'] if milestone else ['refutation']
   65              require([c['phase'] for c in calls] == required_phases,
   66                      'missing or reordered review pass')
   67              for call in calls:
   68                  name = call['output']
   69                  require(isinstance(name, str) and pathlib.Path(name).name == name
   70                          and name.endswith('.md'), 'output must be one Markdown filename')
   71                  require(name not in outputs, 'review passes must have distinct output files')
   72                  outputs.add(name)
   73                  output = root / name
   74                  require(output.resolve().parent == root.resolve(), 'output escaped evidence folder')
   75                  pf = root / (name + '.provenance.json')
   76                  require(pf.resolve().parent == root.resolve(), 'receipt escaped evidence folder')
   77                  receipt = json.loads(pf.read_text())
   78                  final = receipt['final']
   79                  verification = final['verification']
   80                  require(receipt['facilitator_version'].startswith('council-facilitator@'), 'missing Facilitator version')
   81                  require(receipt['member'] == member, 'receipt belongs to another reviewer')
   82                  require(receipt['declared_model'].split(' ', 1)[0] == model, 'declared model differs from review plan')
   83                  require(final['outcome'] == 'success' and verification['result'] == 'PASS', 'review call did not succeed and verify')
   84                  require(verification['model_identity_source'] == 'provider_response', 'model identity is not provider-observed')
   85                  observed = verification['observed']
   86                  # Allow the dated alias only after the Facilitator's semantic PASS.
   87                  require(re.fullmatch(re.escape(model) + r'(?:-\d{8})?', observed),
   88                          'served model differs from review plan')
   89                  effort = final['effort_verification']
   90                  require(effort['result'] == 'PASS' and effort['declared'] == reviewer['effort'], 'effort differs from plan or did not verify')
   91                  if member == 'gpt':
   92                      provider = final['provider_verification']
   93                      require(provider['result'] == 'PASS', 'GPT provider pin did not verify')
   94                      require(provider['observed_providers'] == ['OpenAI'], 'GPT served outside its OpenAI provider pin')
   95                  content = output.read_bytes()
   96                  require(content.strip(), 'empty reviewer output')
   97                  digest = hashlib.sha256(content).hexdigest()
   98                  require(receipt['output_file_sha256'] == digest == final['file_artifact_sha256'],
   99                          'review output digest differs')
  100          ok(f'review plan: {depth}, {1 + count} model perspectives, {len(outputs)} verified external calls')
  101      except (OSError, ValueError, KeyError, TypeError, AttributeError, AssertionError) as e:
  102          bad(f"second-opinions/review-plan.json or its call evidence is invalid: {e or 'contract mismatch'}")
  103  
  104  
  105  def main():
  106      ap = argparse.ArgumentParser()
  107      ap.add_argument("folder")
  108      ap.add_argument("--issue", type=int, help="audit issue number to check the task list")
  109      ap.add_argument("--repo", default="pixelelated/distribution")
  110      ap.add_argument("--phase", choices=("pre-issue", "resolution"), default="resolution",
  111                      help="pre-issue validates open review artifacts; default resolution requires every outcome")
  112      args = ap.parse_args()
  113      d = pathlib.Path(args.folder)
  114      fails = []
  115  
  116      def bad(msg):
  117          fails.append(msg)
  118          print(f"  FAIL  {msg}")
  119  
  120      def ok(msg):
  121          print(f"  ok    {msg}")
  122  
  123      print(f"== {d}")
  124      if not d.is_dir():
  125          print("  FAIL  not a directory"); return 2
  126  
  127      for f in REQUIRED:
  128          (ok if (d / f).exists() else bad)(f)
  129      milestone = "-milestone-" in d.name
  130      if milestone:
  131          (ok if (d / "00-running-log.md").exists() else bad)(
  132              "00-running-log.md (mandatory at milestone tier)")
  133  
  134      analysis = (d / "04-analysis.md").read_text() if (d / "04-analysis.md").exists() else ""
  135      for sec in ANALYSIS_SECTIONS:
  136          if sec.lower() in analysis.lower():
  137              ok(f"04 § {sec}")
  138          else:
  139              bad(f"04-analysis.md missing section: {sec}")
  140  
  141      # v1.12 (2026-10-02): cross-lab plans and all selected passes are verified.
  142      # Completed older audits retain v1.11's historical GPT-only contract;
  143      # their evidence is not rewritten to claim a different review occurred.
  144      m = re.match(r"(\d{4})_(\d\d)_(\d\d)-(milestone|epic|issue)-", d.name)
  145      current_contract = (d / "second-opinions/review-plan.json").exists() or (
  146          m and m.group(4) in ("milestone", "epic")
  147          and m.group(1, 2, 3) >= ("2026", "10", "02"))
  148      if current_contract:
  149          check_review_plan(d, milestone, bad, ok)
  150          if not re.search(r"^##+ Second opinion", analysis, re.M):
  151              bad("04-analysis.md has no Second opinion section recording the selected depth/outcome")
  152      elif m and m.group(4) in ("milestone", "epic") and m.group(1, 2, 3) >= ("2026", "09", "24"):
  153          if re.search(r"^##+ Second opinion", analysis, re.M):
  154              ok("04 § Second opinion (Phase 4.6)")
  155          else:
  156              bad("04-analysis.md has no § Second opinion: Phase 4.6 (the GPT seat) was skipped or not recorded")
  157          prov = list((d / "second-opinions").glob("*.provenance.json")) if (d / "second-opinions").is_dir() else []
  158          if prov:
  159              served = []
  160              for pf in prov:
  161                  try:
  162                      j = json.loads(pf.read_text())
  163                      served.append(str(j.get("declared_model", "")) + " / " + str((j.get("final") or {}).get("verification", {}).get("observed", "")))
  164                  except Exception as e:  # noqa: BLE001
  165                      served.append(f"unreadable ({e})")
  166              if all("gpt-6-astra" in x for x in served):
  167                  ok(f"second-opinions/: {len(prov)} provenance file(s), the served model gpt-6-astra")
  168              else:
  169                  bad(f"second-opinions/: a provenance file names another model or none: {served}")
  170          else:
  171              bad("second-opinions/ has no *.provenance.json: the seat's run left no record")
  172  
  173      # Every Critical/High row of the findings index has a verification entry of
  174      # its own, keyed by seat and number, not by number. On 2026-09-28 the GPT
  175      # seat's F-CS-02 (Critical: a match could delete N64 .fla saves) shared its
  176      # number with the Claude seat's F-CS-02 (High, a different defect); the
  177      # pass listed ids, saw a mention, and moved on. Stream A found and fixed it
  178      # because the file was its own (blindspot 66). An entry names its seat in
  179      # the parenthesis after the id -- `F-CS-02 (gpt, ...)`, `(claude and gpt`,
  180      # `(both seats` -- or sits under a seat heading such as `### 3-rclone-setup (gpt):`.
  181      forward = (d / "02-forward-audit.md").read_text() if (d / "02-forward-audit.md").exists() else ""
  182      fi, vi = forward.find("## Findings index"), forward.find("## Verification")
  183      if fi >= 0 and vi > fi:
  184          index, ver = forward[fi:vi], forward[vi:]
  185          need = set()
  186          for row in index.splitlines():
  187              if row.startswith("| ") and not row.startswith("| bucket") and not re.match(r"^\|\s*-", row):
  188                  c = [x.strip() for x in row.strip("|").split("|")]
  189                  if len(c) > 3 and c[3] in ("Critical", "High") and re.match(r"G?[FG]2?-[A-Z][A-Z0-9-]*?-\d+$", c[2]) and c[1] in ("claude", "gpt"):
  190                      need.add((c[1], c[2]))
  191          have = set()
  192          ctx = None
  193          for line in ver.splitlines():
  194              if line.startswith("### ") and not re.search(r"\bG?[FG]2?-[A-Z][A-Z0-9-]*?-\d+\b", line):
  195                  m = re.search(r"\((claude|gpt)\)", line)
  196                  ctx = m.group(1) if m else None
  197                  continue
  198              if not (line.startswith("### ") or re.match(r"- \*\*G?[FG]2?-", line)):
  199                  continue
  200              for m in re.finditer(r"\b(G?[FG]2?-[A-Z][A-Z0-9-]*?-\d+)\b\**\s*(?:\(([^)]*)\))?", line):
  201                  fid, par = m.group(1), (m.group(2) or "").lower()
  202                  seats = [x for x in ("claude", "gpt") if x in par]
  203                  if "both seats" in par:
  204                      seats = ["claude", "gpt"]
  205                  if not seats and ctx:
  206                      seats = [ctx]
  207                  for x in seats:
  208                      have.add((x, fid))
  209          short = sorted(need - have)
  210          if need and not short:
  211              ok(f"every Critical/High of the index has a verification entry for its seat ({len(need)} seat-and-number pairs)")
  212          for seat, fid in short:
  213              bad(f"02 § Verification has no entry for {fid} ({seat}) -- a number two seats used is two findings")
  214  
  215      punch = (d / "05-punch-list.md").read_text() if (d / "05-punch-list.md").exists() else ""
  216  
  217      # Every finding § Verification confirms is carried into 05 -- as an item's
  218      # Source Finding or in the leads table -- or the confirmation was written
  219      # and then lost. On 2026-09-28 G2-B-05 (gpt) was re-graded from High to
  220      # "confirmed, Medium" with its fix stated, and reached neither the punch
  221      # list nor a lead; the blind second opinion found it (S-06), this lint did
  222      # not. A confirmed verdict is a `### <id> (<seat>...)` block whose
  223      # `**Verdict:**` starts `**confirmed`, or a triage-table row whose grade
  224      # cell does. 05's short forms are expanded: `G2-E-core-02, -03` names two
  225      # ids, `G2-I-05..09` five.
  226      if fi >= 0 and vi > fi:
  227          confirmed = set()
  228          for b in re.split(r"^(?=### )", ver, flags=re.M):
  229              if b.startswith("### ") and re.search(r"^\*\*Verdict:\*\* \*\*confirmed", b, re.M):
  230                  for m in re.finditer(r"\b(G?[FG]2?-[A-Z][A-Za-z0-9-]*?-\d+|BS-\d+)\b", b.splitlines()[0]):
  231                      confirmed.add(m.group(1))
  232          for row in ver.splitlines():
  233              if row.startswith("| ") and "**confirmed" in row:
  234                  c = [x.strip() for x in row.strip("|").split("|")]
  235                  if len(c) >= 2 and c[-1].startswith("**confirmed"):
  236                      for m in re.finditer(r"\b(G?[FG]2?-[A-Z][A-Za-z0-9-]*?-\d+|BS-\d+)\b", c[0]):
  237                          confirmed.add(m.group(1))
  238          carried = set()
  239          for m in re.finditer(r"\b(G?[FG]2?-[A-Z][A-Za-z0-9-]*?-)(\d+)(?:\.\.(\d+))?((?:,\s*-\d+(?:\.\.\d+)?)*)", punch):
  240              pre, a, b, more = m.group(1), m.group(2), m.group(3), m.group(4) or ""
  241              nums = [(a, b)] + [(x.group(1), x.group(2)) for x in re.finditer(r"-(\d+)(?:\.\.(\d+))?", more)]
  242              for lo, hi in nums:
  243                  for n in range(int(lo), int(hi or lo) + 1):
  244                      carried.add(f"{pre}{n:0{len(lo)}d}")
  245          carried |= set(re.findall(r"\bBS-\d+\b", punch))
  246          lost = sorted(confirmed - carried)
  247          if confirmed and not lost:
  248              ok(f"every confirmed verdict of 02 § Verification is carried in 05 ({len(confirmed)} ids)")
  249          for fid in lost:
  250              bad(f"02 § Verification confirms {fid} and 05 carries it nowhere -- neither an item's Source Finding nor a lead")
  251      # A table whose last row is **Total** is the sum of the rows above it. The
  252      # seat's G-11 under #258 (2026-09-24): the scorecard's printed total
  253      # disagreed with its own rows by five boxes and eleven PASS verdicts, and
  254      # the forward audit's per-section subtotals disagreed with both. Arithmetic
  255      # is the one claim in an audit a tool can settle outright.
  256      for tbl in re.findall(r"((?:^\|.*\n)+)", analysis + "\n", re.M):
  257          rows = [r for r in tbl.strip().splitlines() if not re.match(r"^\|\s*:?-", r)]
  258          tot = [r for r in rows if re.match(r"^\|\s*\*\*Total\*\*", r)]
  259          if not tot:
  260              continue
  261  
  262          def nums(r):
  263              return [int(c) if re.fullmatch(r"\d+", c) else None
  264                      for c in [x.strip().strip("*").strip() for x in r.strip().strip("|").split("|")]]
  265          body = [nums(r) for r in rows if r not in tot]
  266          printed = nums(tot[-1])
  267          off = []
  268          for i, v in enumerate(printed):
  269              if v is None:
  270                  continue
  271              got = sum(r[i] for r in body if i < len(r) and r[i] is not None)
  272              if got != v:
  273                  off.append(f"column {i}: printed {v}, the rows sum to {got}")
  274          if off:
  275              bad("04-analysis.md: a **Total** row is not the sum of its table -- " + "; ".join(off))
  276          else:
  277              ok(f"04-analysis.md: the **Total** row sums from its {len(body)} rows")
  278  
  279      items = re.findall(r"^## (PL-\d+)\b.*$", punch, re.M)
  280      if not items:
  281          bad("05-punch-list.md declares no PL- items")
  282      else:
  283          ok(f"{len(items)} punch item(s): {', '.join(items)}")
  284  
  285      # Every item needs a recorded outcome, and the outcome must cite something.
  286      # Slice from the gate *heading*, not the first "Phase 7" mention: the
  287      # instructions and the tracked-scope section may name it earlier, and a
  288      # slice from there matches each item's own heading instead of its outcome.
  289      # The gate's own heading, not the first heading that names Phase 7: #258's
  290      # PL-015 item was titled "...its Phase 7 outcomes table..." and the slice
  291      # began there, reading the item bodies as the gate (2026-09-24).
  292      m = re.search(r"^#+ .*Phase 7 resolution gate.*$", punch, re.M) or re.search(r"^#+ .*Phase 7.*$", punch, re.M)
  293      gate = punch[m.start():] if m else ""
  294      if not gate:
  295          bad("05-punch-list.md has no Phase 7 resolution gate")
  296      # The outcome in force is the LAST cell that carries an outcome word: a
  297      # table may grow a column per gate (2026-09-14's "Deferred -- fix stream",
  298      # then 2026-09-24's "Resolved `abc`"), and the first word found would read
  299      # the old one; the older tables put the word in a middle cell and the
  300      # evidence after it (`| PL-01 | **Resolved** | 2b626195d8; ... |`), so the
  301      # evidence is looked for from that cell to the row's end.
  302      def outcome_cell(row):
  303          cells = [c.strip() for c in row.strip().strip("|").split("|")]
  304          idx = [i for i, c in enumerate(cells) if re.search(r"Resolved|Deferred|Withdrawn", c)]
  305          return " | ".join(cells[idx[-1]:]) if idx else (cells[-1] if cells else row)
  306  
  307      table_words = {}
  308      for pl in items:
  309          # A table row for the item first (`| PL-003 | ...`); a prose mention
  310          # of the id -- the gate's lead may say which cut carried PL-003 --
  311          # is not its outcome.
  312          row = next((l for l in gate.splitlines() if re.match(r"^\|\s*" + re.escape(pl) + r"\s*\|", l)), None) \
  313              or next((l for l in gate.splitlines() if re.search(r"\b" + re.escape(pl) + r"\b", l)), None)
  314          if row is None:
  315              bad(f"{pl} has no Phase 7 outcome"); continue
  316          cell = outcome_cell(row)
  317          if "Resolved" in cell and not re.search(r"`[0-9a-f]{7,40}`|#\d+", cell):
  318              # A resolution can land as a commit or as a tracker edit; either is
  319              # evidence, memory is not.
  320              bad(f"{pl} marked Resolved but cites neither a commit nor an issue")
  321          elif "Deferred" in cell and not re.search(r"#\d+|`[0-9a-f]{7,40}`", cell):
  322              bad(f"{pl} marked Deferred but names no follow-up issue or commit")
  323          elif not re.search(r"Resolved|Deferred|Withdrawn", cell):
  324              # Only an explicit Open outcome cell is valid at this earlier
  325              # gate. An absent/unknown outcome is never silently made open.
  326              open_row = re.match(r"^\|\s*" + re.escape(pl) + r"\s*\|\s*Open\s*\|", row)
  327              if args.phase == "pre-issue" and open_row:
  328                  table_words[pl] = "open"
  329                  ok(f"{pl} explicitly open; resolution remains required")
  330              else:
  331                  bad(f"{pl} outcome is not one of Resolved/Deferred/Withdrawn")
  332          else:
  333              ok(f"{pl} outcome recorded with evidence")
  334          for w in ("Resolved", "Deferred", "Withdrawn"):
  335              if w in cell:
  336                  table_words[pl] = w.lower(); break
  337  
  338      # The YAML index is what begin-delivery parses; the Phase 7 table is what
  339      # a reader sees. #186's index said `open` for 32 items while its table
  340      # said Deferred and the issue said done (audit #258 PL-015), and this
  341      # lint read the table alone. Each id's index outcome must agree with the
  342      # table's word: resolved/deferred/withdrawn against Resolved/Deferred/
  343      # Withdrawn; `open` only where the table has no outcome yet.
  344      idx = re.search(r"^punch_index:\s*$(.*?)^```", punch, re.M | re.S)
  345      indexed = set()
  346      if not idx:
  347          # The YAML index arrived with the 2026-09-12 audit; the two folders
  348          # before it have a table alone, which is what the checks above read.
  349          ok("no punch_index YAML block (an audit from before the index; the table alone is checked)")
  350      else:
  351          for m in re.finditer(r"id:\s*(PL-\d+)\b(.*?)(?=\n-\s*(?:\{)?\s*id:|\Z)", idx.group(1), re.S):
  352              pl, body = m.group(1), m.group(2)
  353              indexed.add(pl)
  354              # `outcome: deferred:#144`, `deferred (#N)`, `resolved (abc)`: the word is the first token
  355              om = re.search(r"outcome:\s*['\"]?([A-Za-z]+)", body)
  356              index_word = om.group(1).lower() if om else ""
  357              table_word = table_words.get(pl, "")
  358              if not index_word:
  359                  bad(f"{pl} has no outcome in the punch_index")
  360              elif table_word and index_word != table_word:
  361                  bad(f"{pl} punch_index says {index_word!r} while the Phase 7 table says {table_word!r}")
  362              elif not table_word and index_word != "open":
  363                  bad(f"{pl} punch_index says {index_word!r} while the Phase 7 table records no outcome")
  364              else:
  365                  ok(f"{pl} index and table agree ({index_word})")
  366  
  367      if args.phase == "pre-issue":
  368          for pl, word in table_words.items():
  369              if word == "open" and pl not in indexed:
  370                  bad(f"{pl} is open but has no matching punch_index entry")
  371  
  372      if args.issue:
  373          try:
  374              body = json.loads(subprocess.run(
  375                  ["gh", "issue", "view", str(args.issue), "--repo", args.repo, "--json", "body"],
  376                  capture_output=True, text=True, check=True).stdout)["body"]
  377          except Exception as e:
  378              bad(f"could not read issue #{args.issue}: {e}"); body = ""
  379          boxes = re.findall(r"^- \[[ x]\]", body, re.M)
  380          if len(boxes) < len(items):
  381              bad(f"issue #{args.issue} has {len(boxes)} checkbox(es) for {len(items)} punch items")
  382          else:
  383              ok(f"issue #{args.issue} carries a task list ({len(boxes)} items)")
  384          for pl in items:
  385              (ok if pl in body else bad)(f"issue #{args.issue} references {pl}")
  386  
  387      success = ("PASS pre-issue artifacts (does not certify resolution)"
  388                 if args.phase == "pre-issue" else "PASS")
  389      print(f"\n{success if not fails else f'{len(fails)} CONTRACT FAILURE(S)'}")
  390      return 1 if fails else 0
  391  
  392  
  393  if __name__ == "__main__":
  394      sys.exit(main())
```

## File: tools/pr-stack-check (at 8ebaf8daad, 167 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # pr-stack-check - build the upstream series by content and prove it is whole.
    6  #
    7  #   tools/pr-stack-check [--map FILE] [--keep] [--base REF] [--from REF] [--repo DIR] [--roots "a b"] [--drafts DIR]
    8  #
    9  # Reads docs/pr-series/map.txt (one `## title` per PR, in order, then the
   10  # paths `git checkout <from> -- <path>` takes; `#` comments), makes a throwaway
   11  # worktree on --base (default upstream/next), and stacks one commit per PR by
   12  # content from --from (default next): a path that exists on next is checked
   13  # out, a path next deleted is removed. Then it fails unless
   14  #
   15  #   0. every PR title obeys upstream's CI rule (`package: text`, 72 chars);
   16  #   1. every path the map names differs from the base somewhere (a dead line
   17  #      in the map is a PR that claims what it does not carry);
   18  #   2. no personal path (the push guard's PERSONAL_PATTERNS, read from
   19  #      .githooks/pre-push) is named;
   20  #   3. every upstream-bound file that differs between the base and next is
   21  #      carried by exactly one PR -- an uncovered file fails, and so does one
   22  #      two PRs both name;
   23  #   4. the last head equals next on every upstream-bound path: zero files
   24  #      differing under packages/, projects/, scripts/, config/, distributions/,
   25  #      Makefile and tools/ minus the personal tools.
   26  #
   27  # It prints each PR's file list with counts. --keep leaves the worktree and
   28  # its pr-stack/N branches for cutting the real pr/* branches from; without it
   29  # the worktree and branches go (tools/fork-worktree remove, which refuses
   30  # build output, of which a fresh worktree has none). Exit 0 only on PASS;
   31  # 1 on any failure; 2 on usage or a base next does not contain (merge
   32  # upstream first, or the diff is not the fork's).
   33  #
   34  # Why by content and not by commit: fork-workflow.md. Why a tool: #322's
   35  # rule that the series must leave upstream with exactly the tree that was
   36  # built and proven; a hand-made stack has no such proof (blindspot 47's
   37  # shape, seen from the other side).
   38  set -u
   39  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
   40  MAP="${ROOT}/docs/pr-series/map.txt"; BASE=upstream/next; FROM=next; KEEP=0
   41  # --repo: the checkout the branches are built in (default: this one); --roots: the
   42  # upstream-bound roots there (default: the distribution's; "." for another repo);
   43  # --drafts: where the PR descriptions live, NN-*.md per map entry (D-WORKFLOW-078's scan).
   44  REPO="${ROOT}"; ROOTS_ARG=""; DRAFTS="${ROOT}/docs/releases/pr"
   45  while [ $# -gt 0 ]; do
   46    case "$1" in
   47      --map) MAP="$2"; shift 2 ;;
   48      --base) BASE="$2"; shift 2 ;;
   49      --repo) REPO="$(cd "$2" && pwd)"; shift 2 ;;
   50      --roots) ROOTS_ARG="$2"; shift 2 ;;
   51      --drafts) DRAFTS="$2"; shift 2 ;;
   52      --from) FROM="$2"; shift 2 ;;
   53      --keep) KEEP=1; shift ;;
   54      -h|--help) sed -n '5,40p' "$0"; exit 0 ;;
   55      *) echo "pr-stack-check: unknown argument $1" >&2; exit 2 ;;
   56    esac
   57  done
   58  cd "${ROOT}" || exit 2
   59  [ -f "${MAP}" ] || { echo "pr-stack-check: no map at ${MAP}" >&2; exit 2; }
   60  g() { git -C "${REPO}" "$@"; }
   61  g rev-parse --verify -q "${BASE}" >/dev/null || { echo "pr-stack-check: no ref ${BASE} in ${REPO}" >&2; exit 2; }
   62  g rev-parse --verify -q "${FROM}" >/dev/null || { echo "pr-stack-check: no ref ${FROM} in ${REPO}" >&2; exit 2; }
   63  if ! g merge-base --is-ancestor "${BASE}" "${FROM}"; then
   64    echo "pr-stack-check: ${FROM} does not contain ${BASE}: merge it first, or the diff below is not only the fork's" >&2; exit 2
   65  fi
   66  FAIL=0; fail() { echo "FAIL: $*"; FAIL=1; }
   67  
   68  # The upstream-bound roots, and the personal patterns the push guard refuses.
   69  if [ -n "${ROOTS_ARG}" ]; then read -r -a ROOTS <<< "${ROOTS_ARG}"; elif [ "${REPO}" = "${ROOT}" ]; then ROOTS=(packages projects scripts config distributions Makefile tools); else ROOTS=(.); fi
   70  mapfile -t PERSONAL < <(sed -n '/^PERSONAL_PATTERNS=(/,/^)/p' "${ROOT}/.githooks/pre-push" | grep -o "^\s*'[^']*'" | tr -d " '")
   71  [ "${#PERSONAL[@]}" -gt 5 ] || { echo "pr-stack-check: could not read PERSONAL_PATTERNS from .githooks/pre-push" >&2; exit 2; }
   72  is_personal() { local p; for p in "${PERSONAL[@]}"; do case "$1" in "${p}"*) return 0 ;; esac; done; return 1; }
   73  
   74  # Every upstream-bound file that differs between the base and FROM.
   75  mapfile -t DIFF < <(g diff --name-only "${BASE}" "${FROM}" -- "${ROOTS[@]}" | while read -r f; do is_personal "$f" || echo "$f"; done)
   76  [ "${#DIFF[@]}" -gt 0 ] || { echo "pr-stack-check: nothing differs between ${BASE} and ${FROM} on the upstream-bound roots"; exit 1; }
   77  
   78  # Parse the map: titles and paths, in order.
   79  declare -a TITLES; declare -A PATHS_OF; n=-1; CEIL_FILES=0; CEIL_INS=0
   80  while IFS= read -r line; do
   81    case "$line" in
   82      '# ceiling:'*) CEIL_FILES="$(printf '%s' "$line" | grep -o 'files=[0-9]*' | cut -d= -f2)"; CEIL_INS="$(printf '%s' "$line" | grep -o 'insertions=[0-9]*' | cut -d= -f2)"; CEIL_FILES="${CEIL_FILES:-0}"; CEIL_INS="${CEIL_INS:-0}" ;;
   83      '## '*) n=$((n+1)); TITLES[$n]="${line#\#\# }"; PATHS_OF[$n]=""
   84         # upstream's CI title rule (validate-pull-request.yml): `package: text`, 72 chars at most
   85         if ! printf '%s' "${TITLES[$n]}" | grep -q -E '^[a-zA-Z0-9_*./-]+:[[:space:]].+$' || [ "${#TITLES[$n]}" -gt 72 ]; then
   86           fail "PR $((n+1))'s title breaks the CI rule (package: text, 72 chars at most): ${TITLES[$n]}"
   87         fi ;;
   88      '#'*|'') ;;
   89      *) [ "$n" -ge 0 ] || { echo "pr-stack-check: a path before the first ## title: $line" >&2; exit 2; }
   90         PATHS_OF[$n]+="${line}"$'\n' ;;
   91    esac
   92  done < "${MAP}"
   93  [ "$n" -ge 0 ] || { echo "pr-stack-check: the map names no PR" >&2; exit 2; }
   94  
   95  # Which diff files each map path covers (a directory covers what is under it).
   96  declare -A OWNER   # file -> PR index
   97  declare -a FILES_OF
   98  for i in $(seq 0 "$n"); do
   99    FILES_OF[$i]=""
  100    while IFS= read -r p; do
  101      [ -n "$p" ] || continue
  102      is_personal "$p" && fail "PR $((i+1)) names a personal path: $p"
  103      hit=0
  104      for f in "${DIFF[@]}"; do
  105        if [ "$f" = "$p" ] || [ "${f#"$p"/}" != "$f" ]; then
  106          hit=1
  107          # A file two PRs need rides whole in each (D-WORKFLOW-079): identical content merges cleanly whichever lands first.
  108          if [ -n "${OWNER[$f]:-}" ] && [ "${OWNER[$f]}" != "$i" ]; then echo "   shared: $f (PR $((OWNER[$f]+1)) and PR $((i+1)))"; fi
  109          OWNER[$f]="$i"; FILES_OF[$i]+="${f}"$'\n'
  110        fi
  111      done
  112      [ "$hit" = 1 ] || fail "PR $((i+1)) names a path that does not differ from ${BASE}: $p"
  113    done <<< "${PATHS_OF[$i]}"
  114  done
  115  for f in "${DIFF[@]}"; do [ -n "${OWNER[$f]:-}" ] || fail "no PR carries $f"; done
  116  
  117  # Build each PR on the base by itself, in a throwaway worktree: one commit per
  118  # branch (D-WORKFLOW-079, #333: the ROCKNIX developers closed a series whose
  119  # tenth branch carried ten commits). The worktree is reset to the base before
  120  # every PR, so nothing of PR 1 is in PR 2.
  121  WT="${REPO}/../$(basename "${REPO}").worktrees/pr-stack-check"
  122  [ "${REPO}" = "${ROOT}" ] && WT="${ROOT}/../rocknix.worktrees/pr-stack-check"
  123  if [ -e "${WT}" ]; then echo "pr-stack-check: ${WT} exists; remove it with tools/fork-worktree remove first" >&2; exit 2; fi
  124  for i in $(seq 0 "$n"); do g branch -D "pr-stack/$((i+1))" >/dev/null 2>&1 || true; done
  125  g worktree add -q --detach "${WT}" "${BASE}" || { echo "pr-stack-check: could not add the worktree" >&2; exit 2; }
  126  cleanup() { if [ "${KEEP}" = 0 ]; then "${ROOT}/tools/fork-worktree" remove "${WT}" >/dev/null 2>&1 || g worktree remove --force "${WT}" >/dev/null 2>&1; for i in $(seq 0 "$n"); do g branch -D "pr-stack/$((i+1))" >/dev/null 2>&1 || true; done; fi; }
  127  trap cleanup EXIT
  128  BANNED='[Cc]laude|[Aa]nthropic|Generated with|Co-Authored-By|D-[A-Z]+-[0-9]+|tools/[a-z]'
  129  PLURAL='\b([Ww]e|[Ww]e'"'"'re|[Ww]e'"'"'ve|[Ww]e'"'"'ll|[Oo]ur|[Oo]urs)\b'
  130  for i in $(seq 0 "$n"); do
  131    echo "== PR $((i+1)): ${TITLES[$i]}"
  132    git -C "${WT}" checkout -q --detach "${BASE}" || { fail "PR $((i+1)): could not reset the worktree to ${BASE}"; continue; }
  133    count=0
  134    while IFS= read -r f; do
  135      [ -n "$f" ] || continue
  136      if g cat-file -e "${FROM}:${f}" 2>/dev/null; then
  137        git -C "${WT}" checkout -q "${FROM}" -- "$f" || fail "PR $((i+1)): could not check out $f"
  138      else
  139        git -C "${WT}" rm -q -f -- "$f" 2>/dev/null || fail "PR $((i+1)): $f is deleted on ${FROM} and could not be removed"
  140      fi
  141      count=$((count+1)); echo "   $f"
  142    done <<< "${FILES_OF[$i]}"
  143    if [ "$count" = 0 ]; then fail "PR $((i+1)) carries no file"; continue; fi
  144    git -C "${WT}" commit -q --allow-empty -m "${TITLES[$i]}" || fail "PR $((i+1)): commit failed"
  145    git -C "${WT}" branch -f "pr-stack/$((i+1))" HEAD
  146    # exactly one commit past the base, and the size a reviewer meets
  147    c="$(git -C "${WT}" rev-list --count "${BASE}..HEAD")"; [ "$c" = 1 ] || fail "PR $((i+1)) is $c commits past ${BASE}, not one"
  148    stat="$(git -C "${WT}" diff --shortstat "${BASE}" HEAD)"; files="$(printf '%s' "$stat" | grep -o '[0-9]* file' | cut -d' ' -f1)"; ins="$(printf '%s' "$stat" | grep -o '[0-9]* insertion' | cut -d' ' -f1)"
  149    echo "   ($count files named; ${files:-0} files, ${ins:-0} insertions past ${BASE})"
  150    [ "${CEIL_FILES}" -gt 0 ] && [ "${files:-0}" -gt "${CEIL_FILES}" ] && fail "PR $((i+1)) touches ${files} files, over the map's ceiling of ${CEIL_FILES}"
  151    [ "${CEIL_INS}" -gt 0 ] && [ "${ins:-0}" -gt "${CEIL_INS}" ] && fail "PR $((i+1)) adds ${ins} lines, over the map's ceiling of ${CEIL_INS}"
  152    # the description a reviewer reads (D-WORKFLOW-078, D-WORKFLOW-074): present, titled as the map, in the maintainer's voice
  153    d="$(ls "${DRAFTS}"/$(printf '%02d' $((i+1)))-*.md 2>/dev/null | head -1)"
  154    if [ -z "$d" ]; then fail "PR $((i+1)) has no description under ${DRAFTS} (NN-*.md)"; continue; fi
  155    t="$(sed -n 's/^Title: //p' "$d" | head -1)"; [ "$t" = "${TITLES[$i]}" ] || fail "PR $((i+1))'s description is titled '$t', the map says '${TITLES[$i]}'"
  156    body="$(sed '1{/^Title: /d}' "$d")"
  157    h="$(printf '%s\n' "$body" | grep -n -E "${BANNED}" | head -3)"; [ -z "$h" ] || fail "PR $((i+1))'s description names an assistant, a decision ID or a fork tool:"$'\n'"$h"
  158    h="$(printf '%s\n' "$body" | grep -n -E "${PLURAL}" | head -3)"; [ -z "$h" ] || fail "PR $((i+1))'s description is in the plural (the maintainer writes as I):"$'\n'"$h"
  159    h="$(printf '%s\n' "$body" | grep -n -E '^\*\*[^*]+\*\*|^#+ |^- ' | head -3)"; [ -z "$h" ] || fail "PR $((i+1))'s description carries a template (bold labels, headings or bullets):"$'\n'"$h"
  160  done
  161  
  162  if [ "${FAIL}" = 0 ]; then
  163    echo "pr-stack-check: PASS -- $((n+1)) PRs carry all ${#DIFF[@]} upstream-bound files, each one commit on ${BASE} with a description in the maintainer's voice"
  164    [ "${KEEP}" = 1 ] && echo "kept: ${WT}; branches pr-stack/1..$((n+1)), each on ${BASE} by itself"
  165    exit 0
  166  fi
  167  echo "pr-stack-check: FAIL"; exit 1
```

## File: tools/prose-check (at 8ebaf8daad, 131 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0-or-later
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # prose-check -- does a rocknix.org page read as one of the site's writers wrote it?
    6  #
    7  #   tools/prose-check <page.md> [<page.md>...]     # fails on the first list in
    8  #                                                  # .claude/skills/developer-relations/SKILL.md § Tells,
    9  #                                                  # warns on the second
   10  #   tools/prose-check --self-test                  # the site's own pages pass; a machine-sounding draft fails
   11  #
   12  # The lists are the skill's (#323, D-WORKFLOW-068), grown page by page in its
   13  # loop; a tell added there is added here. Front matter, fenced code, inline
   14  # code and URLs are not prose and are skipped. Exit 0 = no fail (warnings
   15  # printed), 1 = a fail, 2 = usage or an unreadable file. Fork-only.
   16  import re, sys, os
   17  
   18  FAIL = [
   19      (r"—", "an em dash (the site punctuates with a comma, a colon or a spaced hyphen)"),
   20      (r"\s–\s", "a spaced en dash used as punctuation"),
   21      (r"\b(delve|delving|leverag(e|es|ed|ing)|robust(ly)?|seamless(ly)?|streamlin(e|es|ed|ing)|utiliz(e|es|ed|ing)|empower(s|ed|ing)?|elevat(e|es|ed|ing)|game-changer|supercharg(e|es|ed|ing))\b", "a word the site's writers never reach for"),
   22      (r"\b(best-in-class|world-class|cutting-edge|state-of-the-art|unlock the power)\b", "marketing"),
   23      (r"\b(it's|it is) worth noting\b|\bit is important to note\b|\bkeep in mind that\b|\bremember that\b|\bplease note\b", "filler framing: if it is worth noting, note it"),
   24      (r"(^|[.!?]\s+)note that\b", "'Note that' opening a sentence"),
   25      (r"\bwhether you're\b.*\bor\b|\bnot just\b.*,?\s*but\b", "a flourish the site does not use"),
   26      (r"\?\s*$", "a rhetorical question"),
   27      (r"[^`]![^\[\]\(=]", "an exclamation mark in body text"),
   28      (r"(^|[.!?]\s+)let's\b", "'Let's'"),
   29      (r"\b(in summary|to sum up|in conclusion|overall,|that's it!|you're all set|happy gaming)\b", "a closing summary or sign-off"),
   30  ]
   31  # First person plural (D-WORKFLOW-074): the fork posts as one person. A fail under
   32  # docs/releases/ (notes, PR descriptions) and with PROSE_FIRST_PERSON=fail; a warning
   33  # on a page, where another contributor's "we" is theirs and the writer's own is not.
   34  PLURAL = (r"\b(we|we're|we've|we'll|we'd|our|ours|ourselves)\b", "first person plural: the fork posts as one person, so 'I' and 'my' (D-WORKFLOW-074)")
   35  WARN = [
   36      (r"\bdue to the fact that\b|\bat this point in time\b|\ba number of\b", "padding ('because', 'now', a count)"),
   37      (r"\bin order to\b", "'in order to' ('to' does it; the site's RetroAchievements page says it twice, so a warning)"),
   38      (r"\b\w+, \w+, and \w+\b(?![^`]*`)", "a three-item list: fine for three things (the maintainer's 'saves, states, and screenshots'), a tell when the three are adjectives for rhythm"),
   39      (r"\b(simply|just|easy|easily|quickly)\b", "the site's writers use this, once; a step is not made easier by saying so"),
   40      (r"\bensure( that)?\b", "'ensure' (the maintainer's word, once)"),
   41      (r"\bplease\b", "'please' outside a request for help"),
   42  ]
   43  
   44  def prose_lines(text):
   45      """Yield (lineno, line) for prose only: no front matter, fenced code, HTML blocks; inline code and URLs blanked."""
   46      lines = text.split("\n"); infm = lines and lines[0].strip() == "---"; fence = False
   47      for i, l in enumerate(lines, 1):
   48          s = l.strip()
   49          if infm:
   50              if i > 1 and s == "---": infm = False
   51              continue
   52          if s.startswith("```") or s.startswith("~~~"): fence = not fence; continue
   53          if fence or s.startswith("<") or s.startswith("!!!") or s.startswith("|"): continue
   54          l2 = re.sub(r"`[^`]*`", "`x`", l); l2 = re.sub(r"https?://\S+", "URL", l2); l2 = re.sub(r"\+\+\"[^\"]*\"\+\+", "BUTTON", l2)
   55          yield i, l2
   56  
   57  def check(path, text):
   58      fails, warns = [], []
   59      strict = "docs/releases/" in path.replace("\\", "/") or os.environ.get("PROSE_FIRST_PERSON") == "fail"
   60      body = list(prose_lines(text)); prev_first = None
   61      for i, l in body:
   62          low = l.lower()
   63          for pat, why in FAIL:
   64              if re.search(pat, low if pat[0] != "[" else l):
   65                  fails.append((i, why, l.strip()[:90]))
   66          if re.search(PLURAL[0], low):
   67              (fails if strict else warns).append((i, PLURAL[1], l.strip()[:90]))
   68          for pat, why in WARN:
   69              if re.search(pat, low):
   70                  warns.append((i, why, l.strip()[:90]))
   71          for sent in re.split(r"(?<=[.!?])\s+", l.strip()):
   72              if len(sent.split()) > 35: warns.append((i, "a sentence over 35 words", sent[:90]))
   73              first = sent.split()[0].lower() if sent.split() else None
   74              if first and first == prev_first and first not in ("the", "a", "an", "if", "in", "on", "to", "for", "you", "this", "it", "select", "press"):
   75                  pass
   76              prev_first = first
   77          if l.strip().startswith("#") and l.strip().endswith("?"):
   78              warns.append((i, "a heading that is a question", l.strip()[:90]))
   79      # bold-label bullets: more than five in one list is a warning -- the maintainer's own variable
   80      # reference is eleven of them, and a reference list is that shape; a page of explanation is not
   81      run = 0
   82      for i, l in body:
   83          if re.match(r"\s*[-*]\s+\*\*[^*]+\*\*:", l): run += 1
   84          else:
   85              if run > 5: warns.append((i, "a list of more than five '**Label**: sentence' bullets (a reference list is this shape; explanation is not)", "(the list above)"))
   86              run = 0
   87      if run > 5: warns.append((len(body), "a list of more than five '**Label**: sentence' bullets", "(the list above)"))
   88      return fails, warns
   89  
   90  BAD = """# :material-cloud: Cloud Sync
   91  
   92  Whether you're a casual player or a hardcore collector, ROCKNIX's robust cloud sync seamlessly keeps your saves in sync — across every device you own! Let's delve into how to leverage it.
   93  
   94  ## Setup
   95  
   96  1. Navigate to the settings in order to enable the feature.
   97  2. It's worth noting that you should ensure your device is online.
   98  
   99  In summary, cloud sync is fast, simple, and secure. Happy gaming!
  100  """
  101  
  102  def main(argv):
  103      if len(argv) >= 2 and argv[1] == "--self-test":
  104          S = "/workspace/tmp/rocknix-session"
  105          ok = True
  106          for f in ("prose-sample-maintainer-rclone.md", "prose-sample-update.md", "prose-sample-ra.md"):
  107              p = os.path.join(S, f)
  108              if not os.path.exists(p): print(f"self-test: missing sample {p}"); return 2
  109              fails, warns = check(p, open(p, encoding="utf-8").read())
  110              print(f"{'ok  ' if not fails else 'FAIL'}  sample {f}: {len(fails)} fail, {len(warns)} warn")
  111              for i, why, s in fails: print(f"        {i}: {why}: {s}")
  112              ok = ok and not fails
  113          fails, warns = check("bad-draft", BAD)
  114          print(f"{'ok  ' if fails else 'FAIL'}  the machine-sounding draft: {len(fails)} fail (seen to fail: {len(fails) >= 5})")
  115          for i, why, s in fails: print(f"        {i}: {why}: {s}")
  116          ok = ok and len(fails) >= 5
  117          print("self-test: PASS" if ok else "self-test: FAIL"); return 0 if ok else 1
  118      if len(argv) < 2: print(__doc__ or "usage: tools/prose-check <page.md>..."); return 2
  119      rc = 0
  120      for p in argv[1:]:
  121          try: text = open(p, encoding="utf-8").read()
  122          except OSError as e: print(f"prose-check: {p}: {e}"); return 2
  123          fails, warns = check(p, text)
  124          for i, why, s in warns: print(f"{p}:{i}: warn: {why}: {s}")
  125          for i, why, s in fails: print(f"{p}:{i}: FAIL: {why}: {s}")
  126          print(f"prose-check: {p}: {'PASS' if not fails else 'FAIL'} ({len(fails)} fail, {len(warns)} warn)")
  127          rc = rc or (1 if fails else 0)
  128      return rc
  129  
  130  if __name__ == "__main__":
  131      sys.exit(main(sys.argv))
```

## File: tools/rc-preflight (at 8ebaf8daad, 420 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # rc-preflight -- may this tree be cut as a release candidate? (#271,
    6  # D-WORKFLOW-047 step 0, release-candidates.md)
    7  #
    8  #   tools/rc-preflight                       # the tree this checkout is on
    9  #   tools/rc-preflight --tree <worktree>     # a build worktree
   10  #   tools/rc-preflight --es <checkout>       # the EmulationStation checkout
   11  #   tools/rc-preflight --no-fetch            # the remotes as last fetched (said so)
   12  #   tools/rc-preflight --allow-unchecked device-facts
   13  #   tools/rc-preflight --only proxy-schema   # quick, offline pin-note check
   14  #
   15  # D-WORKFLOW-168 (#344): owner-only engineering testing and public publication
   16  # have separate readiness lists. This tool retains the RC checks below; it
   17  # does not implement #528 source/notice publication delivery or authorize a
   18  # device action. Private handoff still requires its audit, applicable fixes,
   19  # artifact/VM qualification and preservation checks. No runtime bypass added.
   20  #
   21  # One verdict per item, printed and then summed:
   22  #
   23  #   packages       every package the fork introduces at its author's current
   24  #                  release (tools/fork-package-freshness on the tree): PINNED
   25  #                  and BEHIND are findings here, where freshness itself lets a
   26  #                  stated pin pass -- a reason that held for a round in progress
   27  #                  is not a reason for a build going upstream (#271)
   28  #   base: distribution   the tree's HEAD against upstream/next, in commits
   29  #   base: emulationstation  the ES pin against ROCKNIX's master, in commits
   30  #   bugs           open issues labelled bug on the fork; an accepted one must
   31  #                  carry a "Code trace" comment on its issue -- how it was
   32  #                  found, the defect at source, the fix read in the candidate,
   33  #                  the siblings hunted, what reading cannot prove (#273,
   34  #                  maintainer 2026-09-25: "at a minimum, do code exploration of
   35  #                  every bug to see if we can track the source and validate it
   36  #                  just that way") -- or the acceptance is a finding
   37  #   already written  every bug fixed since the rule's clock (2026-09-26 02:45 UTC)
   38  #                  -- open with a code trace, or closed as completed -- answers in
   39  #                  its trace what the code before the fix had already written on
   40  #                  devices and in their clouds and how the fix treats it, as a
   41  #                  line "Already written: ... -- read both | migrated: how |
   42  #                  nothing inherited: why" (#289, D-WORKFLOW-050; maintainer,
   43  #                  2026-09-26: "when we push a fix, we ensure parity for the
   44  #                  existing system"); a trace without the line, or a bug closed
   45  #                  as completed since the clock with no trace, is a finding
   46  #   checkboxes     tools/box-check: every open checkbox agent-verifiable
   47  #   catalog        tools/release-catalog --check
   48  #   device facts   no tool reads docs/releases/device-facts.md yet (#270):
   49  #                  UNCHECKED, which is not a pass unless the caller says
   50  #                  --allow-unchecked device-facts, having read it by hand
   51  #   ceremonies     tools/ceremony-check --gate refuses: a finding; owed only
   52  #                  at the CI level (an audit, a futro): noted, not a finding,
   53  #                  since the upstream audit is step 6 of the same procedure
   54  #
   55  # A finding is accepted for this candidate by a line in
   56  # docs/releases/rc-accept.txt naming it and a decided register row:
   57  #
   58  #   package <name> <register ID> -- why this candidate ships with the pin
   59  #   base emulationstation <register ID> -- why it is cut behind ROCKNIX
   60  #   bug #<number> <register ID> -- why this candidate ships with the bug
   61  #
   62  # (#271: "a PINNED line is a finding the maintainer accepts for this candidate
   63  # by a register row naming it, or the bump is done first"). A line whose ID is
   64  # not a decided row accepts nothing, and says so.
   65  #
   66  # Exit 0 when every item is current or accepted; 1 when any finding is not
   67  # accepted; 2 when any item could not be answered -- a remote that did not
   68  # answer is not "current" (engineering-practices.md, guards fail closed).
   69  # Fork-only.
   70  
   71  import argparse
   72  import json
   73  import os
   74  import re
   75  import subprocess
   76  import sys
   77  
   78  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   79  # RC_ACCEPT names another acceptance file, for proving the check (the guard's positive).
   80  ACCEPT = os.environ.get("RC_ACCEPT") or os.path.join(ROOT, "docs", "releases", "rc-accept.txt")
   81  REGISTER = os.path.join(ROOT, "docs", "decision-register.md")
   82  ES_PKG = "projects/ROCKNIX/packages/ui/emulationstation/package.mk"
   83  PROXY_PKG = "projects/ROCKNIX/packages/network/raofflineproxy"
   84  STATES = ("CURRENT", "PINNED", "BEHIND", "INHERITED", "LOCAL", "UNKNOWN")
   85  
   86  
   87  def run(cmd, cwd=None, timeout=600):
   88      try:
   89          p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
   90          return p.returncode, p.stdout, p.stderr
   91      except (OSError, subprocess.TimeoutExpired) as exc:
   92          return None, "", str(exc)
   93  
   94  
   95  def decided_ids():
   96      try:
   97          text = open(REGISTER, encoding="utf-8").read()
   98      except OSError:
   99          return None
  100      decided = text.split("\n## Open decisions", 1)[0]
  101      return set(re.findall(r"^\| (D-[A-Z]+-\d+) \|", decided, re.M))
  102  
  103  
  104  def acceptances(ids):
  105      """{(kind, item): id} for every line whose ID is a decided row; and the
  106      lines that accepted nothing, with why."""
  107      ok, bad = {}, []
  108      try:
  109          lines = open(ACCEPT, encoding="utf-8").read().splitlines()
  110      except FileNotFoundError:
  111          return ok, bad
  112      for n, raw in enumerate(lines, 1):
  113          line = raw.strip()
  114          if not line or line.startswith("#"):
  115              continue
  116          line = line.split(" -- ", 1)[0]
  117          parts = line.split()
  118          if len(parts) < 3:
  119              bad.append("line %d: '%s' names no register row" % (n, line.strip()))
  120              continue
  121          kind, item, rid = parts[0], parts[1], parts[2]
  122          if ids is None or rid not in ids:
  123              bad.append("line %d: %s %s cites %s, which is not a decided register row" % (n, kind, item, rid))
  124              continue
  125          ok[(kind, item.lstrip("#"))] = rid
  126      return ok, bad
  127  
  128  
  129  class Report:
  130      def __init__(self):
  131          self.rows = []
  132  
  133      def add(self, verdict, item, text):
  134          self.rows.append((verdict, item, text))
  135          print("%-9s %-24s %s" % (verdict, item, text), flush=True)
  136  
  137  
  138  def check_proxy_schema(r, tree):
  139      """Catch a stale review note before building; this is not a schema test.
  140  
  141      The full scripts suite still reads a database written by current Storage.
  142      A pin refresh requires reading that schema, not automatically stamping a
  143      new hash into the comment (#414, F-RA-07/28).
  144      """
  145      package = os.path.join(tree, PROXY_PKG)
  146      try:
  147          with open(os.path.join(package, "package.mk"), encoding="utf-8") as f:
  148              recipe = f.read()
  149          with open(os.path.join(package, "sources", "raofflineproxy-ctl"), encoding="utf-8") as f:
  150              script = f.read()
  151      except (OSError, UnicodeError) as exc:
  152          r.add("CANNOT", "proxy schema note", "cannot read selected tree: %s" % type(exc).__name__)
  153          return
  154      pins = re.findall(r'^PKG_VERSION="([0-9a-f]{40})"\s*$', recipe, re.M)
  155      assignments = re.findall(r'^PKG_VERSION=', recipe, re.M)
  156      header, boundary, _ = script.partition("\n. /etc/profile\n")
  157      notes = re.findall(r'^# package\.mk pins \(([0-9a-f]{40}), storage\.py$', header, re.M)
  158      claims = re.findall(r'^# package\.mk pins', header, re.M)
  159      if len(pins) != 1 or len(assignments) != 1 or not boundary or len(notes) != 1 or len(claims) != 1:
  160          r.add("FAIL", "proxy schema note", "missing, malformed or ambiguous package pin/schema note")
  161      elif notes[0] != pins[0]:
  162          r.add("FAIL", "proxy schema note", "review note %s differs from package pin %s" % (notes[0], pins[0]))
  163      else:
  164          r.add("PASS", "proxy schema note", "review note matches %s; runtime schema proof remains separate" % pins[0])
  165  
  166  
  167  def check_packages(r, tree, acc):
  168      tool = os.path.join(tree, "tools", "fork-package-freshness")
  169      if not os.access(tool, os.X_OK):
  170          tool = os.path.join(ROOT, "tools", "fork-package-freshness")
  171      rc, out, err = run([tool], cwd=tree, timeout=900)
  172      if rc is None or rc == 2:
  173          r.add("CANNOT", "packages", "fork-package-freshness did not answer (rc %s): %s" % (rc, (err or out).strip().splitlines()[-1:] or ""))
  174          return
  175      counts, findings = {}, []
  176      for line in out.splitlines():
  177          m = re.match(r"^(\S+)\s+.*?\b(%s)\b" % "|".join(STATES), line)
  178          if not m:
  179              continue
  180          name, state = m.group(1), m.group(2)
  181          counts[state] = counts.get(state, 0) + 1
  182          if state in ("PINNED", "BEHIND"):
  183              rid = acc.get(("package", name))
  184              findings.append((name, state, rid))
  185      if not counts:
  186          r.add("CANNOT", "packages", "fork-package-freshness printed no package rows")
  187          return
  188      if counts.get("UNKNOWN"):
  189          r.add("CANNOT", "packages", "%d package(s) UNKNOWN to fork-package-freshness" % counts["UNKNOWN"])
  190          return
  191      open_ = [f for f in findings if not f[2]]
  192      summary = ", ".join("%d %s" % (v, k.lower()) for k, v in sorted(counts.items()))
  193      accepted = ", ".join("%s (%s)" % (n, rid) for n, _, rid in findings if rid)
  194      if open_:
  195          r.add("FAIL", "packages", "%s; not accepted: %s%s" % (summary, ", ".join("%s %s" % (n, s) for n, s, _ in open_),
  196                                                               "; accepted: " + accepted if accepted else ""))
  197      else:
  198          r.add("PASS", "packages", summary + ("; accepted: " + accepted if accepted else ""))
  199  
  200  
  201  def commits_behind(repo, base, target):
  202      rc, out, err = run(["git", "-C", repo, "rev-list", "--count", "%s..%s" % (base, target)])
  203      if rc != 0:
  204          return None, (err or out).strip()
  205      n = int(out.strip() or 0)
  206      age = ""
  207      if n:
  208          rc2, out2, _ = run(["git", "-C", repo, "log", "--reverse", "--format=%cs", "%s..%s" % (base, target)])
  209          first = (out2.split() or [""])[0] if rc2 == 0 else ""
  210          age = ", the oldest from %s" % first if first else ""
  211      return n, age
  212  
  213  
  214  def check_base(r, name, repo, base, target, acc, fetch_cmd, fetched):
  215      if fetch_cmd and fetched:
  216          rc, out, err = run(fetch_cmd, timeout=300)
  217          if rc != 0:
  218              r.add("CANNOT", "base: " + name, "the fetch did not answer (%s)" % (err or out).strip().splitlines()[-1:])
  219              return
  220      n, detail = commits_behind(repo, base, target)
  221      if n is None:
  222          r.add("CANNOT", "base: " + name, "git could not count %s..%s: %s" % (base[:12], target, detail))
  223          return
  224      note = "" if fetched else " (remotes as last fetched: --no-fetch)"
  225      if n == 0:
  226          r.add("PASS", "base: " + name, "level with %s%s" % (target, note))
  227      elif acc.get(("base", name)):
  228          r.add("PASS", "base: " + name, "%d behind %s%s -- accepted (%s)%s" % (n, target, detail, acc[("base", name)], note))
  229      else:
  230          r.add("FAIL", "base: " + name, "%d behind %s%s%s" % (n, target, detail, note))
  231  
  232  
  233  def check_bugs(r, acc):
  234      rc, out, err = run(["gh", "issue", "list", "--repo", "pixelelated/distribution", "--state", "open", "--label", "bug",
  235                          "--limit", "300", "--json", "number,title"], timeout=120)
  236      if rc != 0:
  237          r.add("CANNOT", "bugs", "the tracker did not answer: %s" % (err or out).strip().splitlines()[-1:])
  238          return
  239      try:
  240          issues = json.loads(out)
  241      except ValueError:
  242          r.add("CANNOT", "bugs", "the tracker's answer was not JSON")
  243          return
  244      open_ = [i for i in issues if not acc.get(("bug", str(i["number"])))]
  245      accepted = ["#%d (%s)" % (i["number"], acc[("bug", str(i["number"]))]) for i in issues if acc.get(("bug", str(i["number"])))]
  246      untraced = []
  247      for i in issues:
  248          if not acc.get(("bug", str(i["number"]))):
  249              continue
  250          rc2, out2, err2 = run(["gh", "api", "--paginate", "repos/pixelelated/distribution/issues/%d/comments" % i["number"],
  251                                 "--jq", ".[].body"], timeout=120)
  252          if rc2 != 0:
  253              r.add("CANNOT", "bugs", "the tracker did not answer for #%d's comments: %s" % (i["number"], (err2 or out2).strip().splitlines()[-1:]))
  254              return
  255          if not re.search(r"^\s*(#+\s*|\*\*)?code trace\b", out2 or "", re.I | re.M):
  256              untraced.append("#%d" % i["number"])
  257      if untraced:
  258          r.add("FAIL", "bugs", "%d accepted bug(s) whose issue carries no \"Code trace\" comment (#273): %s%s" % (
  259              len(untraced), " ".join(untraced), "; without a disposition: " + " ".join("#%d" % i["number"] for i in open_) if open_ else ""))
  260          return
  261      if open_:
  262          r.add("FAIL", "bugs", "%d open bug(s) with no disposition for this candidate: %s%s" % (
  263              len(open_), " ".join("#%d" % i["number"] for i in sorted(open_, key=lambda i: i["number"])),
  264              "; accepted: " + ", ".join(accepted) if accepted else ""))
  265      else:
  266          r.add("PASS", "bugs", "no open bug without a disposition" + ("; accepted: " + ", ".join(accepted) if accepted else ""))
  267  
  268  
  269  # D-WORKFLOW-050's clock: nothing closed before it is demanded, as ceremonies.md
  270  # starts its clock on 2026-09-21 -- a backlog nobody can pay at once is how a
  271  # gate gets switched off. The four device-round bugs closed at 01:25-01:31 UTC
  272  # that day predate it; #280's missing answer is #288.
  273  ALREADY_WRITTEN_SINCE = "2026-09-26T02:45:00Z"
  274  CODE_TRACE_RE = re.compile(r"^\s*(?:#+\s*|\*\*|[-*]\s*)?code trace\b", re.I | re.M)
  275  ALREADY_WRITTEN_RE = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?already written(?:\*\*)?\s*[:.]", re.I | re.M)
  276  
  277  
  278  def issue_text(number):
  279      """The issue's body and every comment as one text, or (None, why)."""
  280      rc, out, err = run(["gh", "api", "repos/pixelelated/distribution/issues/%d" % number, "--jq", ".body"], timeout=120)
  281      if rc != 0:
  282          return None, (err or out).strip().splitlines()[-1:]
  283      rc2, out2, err2 = run(["gh", "api", "--paginate", "repos/pixelelated/distribution/issues/%d/comments" % number,
  284                             "--jq", ".[].body"], timeout=120)
  285      if rc2 != 0:
  286          return None, (err2 or out2).strip().splitlines()[-1:]
  287      return (out or "") + "\n" + (out2 or ""), ""
  288  
  289  
  290  def check_already_written(r):
  291      listed = []
  292      for state in ("open", "closed"):
  293          rc, out, err = run(["gh", "issue", "list", "--repo", "pixelelated/distribution", "--state", state, "--label", "bug",
  294                              "--limit", "300", "--json", "number,closedAt,stateReason"], timeout=120)
  295          if rc != 0:
  296              r.add("CANNOT", "already written", "the tracker did not answer: %s" % (err or out).strip().splitlines()[-1:])
  297              return
  298          try:
  299              issues = json.loads(out)
  300          except ValueError:
  301              r.add("CANNOT", "already written", "the tracker's answer was not JSON")
  302              return
  303          for i in issues:
  304              if state == "closed" and (i.get("stateReason") != "COMPLETED" or (i.get("closedAt") or "") < ALREADY_WRITTEN_SINCE):
  305                  continue
  306              listed.append((state, i["number"]))
  307      missing, untraced, read = [], [], 0
  308      for state, n in sorted(listed, key=lambda t: t[1]):
  309          text, why = issue_text(n)
  310          if text is None:
  311              r.add("CANNOT", "already written", "the tracker did not answer for #%d: %s" % (n, why))
  312              return
  313          if not CODE_TRACE_RE.search(text):
  314              if state == "closed":
  315                  untraced.append("#%d" % n)   # an open bug without a trace is the bugs item's finding
  316              continue
  317          read += 1
  318          if not ALREADY_WRITTEN_RE.search(text):
  319              missing.append("#%d" % n)
  320      if missing or untraced:
  321          parts = []
  322          if missing:
  323              parts.append("%d code trace(s) with no \"Already written\" line: %s" % (len(missing), " ".join(missing)))
  324          if untraced:
  325              parts.append("%d bug(s) closed as completed since %s with no code trace: %s" % (len(untraced), ALREADY_WRITTEN_SINCE[:10], " ".join(untraced)))
  326          r.add("FAIL", "already written", "; ".join(parts) + " (#289, D-WORKFLOW-050)")
  327      else:
  328          r.add("PASS", "already written", "%d code trace(s) since %s answer what the old code had already written" % (read, ALREADY_WRITTEN_SINCE[:10]))
  329  
  330  
  331  def check_tool(r, item, cmd, fail_text):
  332      rc, out, err = run(cmd, cwd=ROOT, timeout=600)
  333      last = ((out or err).strip().splitlines() or [""])[-1][:160]
  334      if rc == 0:
  335          r.add("PASS", item, last)
  336      elif rc == 1:
  337          r.add("FAIL", item, "%s: %s" % (fail_text, last))
  338      else:
  339          r.add("CANNOT", item, "did not answer (rc %s): %s" % (rc, last))
  340  
  341  
  342  def main():
  343      ap = argparse.ArgumentParser()
  344      ap.add_argument("--tree", default=ROOT, help="the tree about to be cut (default: this checkout)")
  345      ap.add_argument("--es", default=os.path.expanduser("~/Development/emulationstation-next"))
  346      ap.add_argument("--no-fetch", action="store_true")
  347      ap.add_argument("--allow-unchecked", action="append", default=[], choices=["device-facts"])
  348      ap.add_argument("--only", choices=["proxy-schema"], help="run only the named offline check; not an RC verdict")
  349      a = ap.parse_args()
  350      tree = os.path.abspath(a.tree)
  351      fetch = not a.no_fetch
  352      head = run(["git", "-C", tree, "rev-parse", "--short=10", "HEAD"])[1].strip() or "?"
  353      branch = run(["git", "-C", tree, "branch", "--show-current"])[1].strip() or "(detached)"
  354      print("rc-preflight: %s at %s (%s)" % (tree, head, branch), flush=True)
  355  
  356      r = Report()
  357      check_proxy_schema(r, tree)
  358      if a.only:
  359          # Deliberately no MAY BE CUT verdict for a scoped source check.
  360          return 2 if any(row[0] == "CANNOT" for row in r.rows) else int(any(row[0] == "FAIL" for row in r.rows))
  361      ids = decided_ids()
  362      acc, bad = acceptances(ids)
  363      for b in bad:
  364          r.add("NOTE", "rc-accept.txt", b)
  365  
  366      check_packages(r, tree, acc)
  367      check_base(r, "distribution", tree, "HEAD", "upstream/next", acc,
  368                 ["git", "-C", tree, "fetch", "-q", "upstream", "next"], fetch)
  369      pin = ""
  370      try:
  371          m = re.search(r'^PKG_VERSION="([0-9a-f]{7,40})"', open(os.path.join(tree, ES_PKG), encoding="utf-8").read(), re.M)
  372          pin = m.group(1) if m else ""
  373      except OSError:
  374          pass
  375      if not pin:
  376          r.add("CANNOT", "base: emulationstation", "no PKG_VERSION commit in %s" % ES_PKG)
  377      elif not os.path.isdir(os.path.join(a.es, ".git")) and not os.path.isfile(os.path.join(a.es, ".git")):
  378          r.add("CANNOT", "base: emulationstation", "no EmulationStation checkout at %s (--es)" % a.es)
  379      else:
  380          if fetch:
  381              run(["git", "-C", a.es, "fetch", "-q", "origin"], timeout=300)
  382          if run(["git", "-C", a.es, "cat-file", "-e", pin + "^{commit}"])[0] != 0:
  383              r.add("CANNOT", "base: emulationstation", "the pin %s is not in %s" % (pin[:10], a.es))
  384          else:
  385              check_base(r, "emulationstation", a.es, pin, "rocknix/master", acc,
  386                         ["git", "-C", a.es, "fetch", "-q", "rocknix", "master"], fetch)
  387      check_bugs(r, acc)
  388      check_already_written(r)
  389      check_tool(r, "checkboxes", [os.path.join(ROOT, "tools", "box-check"), "--quiet"], "open checkboxes that are not agent-verifiable")
  390      check_tool(r, "catalog", [os.path.join(ROOT, "tools", "release-catalog"), "--check"], "docs/releases/catalog.md is stale")
  391      if "device-facts" in a.allow_unchecked:
  392          r.add("UNCHECKED", "device facts", "no tool reads docs/releases/device-facts.md (#270); read by hand, --allow-unchecked given")
  393      else:
  394          r.add("CANNOT", "device facts", "no tool reads docs/releases/device-facts.md yet (#270): read it by hand, then --allow-unchecked device-facts")
  395      rc, out, err = run([os.path.join(ROOT, "tools", "ceremony-check"), "--gate"], cwd=ROOT, timeout=300)
  396      if rc == 0:
  397          rc2, out2, _ = run([os.path.join(ROOT, "tools", "ceremony-check")], cwd=ROOT, timeout=300)
  398          owed = [l.strip()[len("- [CI] "):] for l in (out2 or "").splitlines() if l.strip().startswith("- [CI] ")]
  399          r.add("PASS", "ceremonies", "the push gate passes" + ("; owed at the CI level: " + "; ".join(o[:90] for o in owed) if rc2 == 1 and owed else ""))
  400      elif rc == 1:
  401          blocks = [l[len("ceremony-check: BLOCK "):] for l in (out or "").splitlines() if l.startswith("ceremony-check: BLOCK ")]
  402          r.add("FAIL", "ceremonies", "the push gate refuses: %s" % ("; ".join(blocks) or ((out or err).strip().splitlines() or [""])[-1])[:200])
  403      else:
  404          r.add("CANNOT", "ceremonies", "ceremony-check did not answer (rc %s)" % rc)
  405  
  406      fails = [x for x in r.rows if x[0] == "FAIL"]
  407      cannot = [x for x in r.rows if x[0] == "CANNOT"]
  408      unchecked = [x for x in r.rows if x[0] == "UNCHECKED"]
  409      if cannot:
  410          verdict, code = "CANNOT ANSWER: %s" % ", ".join(x[1] for x in cannot), 2
  411      elif fails:
  412          verdict, code = "NOT A CANDIDATE: %s" % ", ".join(x[1] for x in fails), 1
  413      else:
  414          verdict, code = "MAY BE CUT" + (" (unchecked by tool: %s)" % ", ".join(x[1] for x in unchecked) if unchecked else ""), 0
  415      print("rc-preflight: %s at %s -- %s" % (branch, head, verdict), flush=True)
  416      return code
  417  
  418  
  419  if __name__ == "__main__":
  420      sys.exit(main())
```

## File: tools/register-check (at 8ebaf8daad, 105 lines)

```text
    1  #!/bin/bash
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # register-check - the decision register is a lookup table; this refuses the
    6  # two ways it stops being one (D-WORKFLOW-013, audit #129 PL-08):
    7  #
    8  #   1. an ID issued twice: `D-INFRA-008` named two decisions for a week, and a
    9  #      citation of it resolved to whichever the reader found first;
   10  #   2. a citation that names no row: the live documents, the rule files, the
   11  #      two script trees and (when ES_SRC points at a checkout) EmulationStation's
   12  #      sources may cite `D-<AREA>-<n>` only for a row that exists.
   13  #
   14  # A citation is any `D-<LETTERS>-<DIGITS>` at a word boundary -- any area, any
   15  # width. It was `D-(CLOUD|UI|...)-[0-9]{3}`, so a citation under an area not in
   16  # that list (a THEME row, say) was never looked up, and a four-digit ID was
   17  # read as its first three digits and passed (audit #151 PL-11). This file is
   18  # itself an input, which is why the two examples are not spelled out here.
   19  #
   20  # Dated records are not checked for citations -- audit artifacts, work logs and
   21  # dated reports describe the register as it was -- but the register itself is
   22  # always checked whole. Every input listed below has to be readable: a document
   23  # that cannot be read has not been checked, and this says so and fails rather
   24  # than passing over it (engineering-practices.md, guards fail closed). Runs on
   25  # the host as tools/vm-qa's `register` suite, beside `vocabulary`.
   26  # Exit 0 when clean, 1 with every problem listed.
   27  set -u
   28  ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
   29  REG="${ROOT}/docs/decision-register.md"
   30  [ -r "${REG}" ] || { echo "register-check: no ${REG}" >&2; exit 2; }
   31  FAIL=0
   32  CITE='D-[A-Z]+-[0-9]+\b'
   33  
   34  # 1. every ID once, across both tables
   35  dups=$(grep -o -E '^\| D-[A-Z]+-[0-9]+ ' "${REG}" | tr -d '| ' | sort | uniq -d)
   36  if [ -n "${dups}" ]; then
   37      for d in ${dups}; do
   38          echo "DUPLICATE ${d}: $(grep -n -E "^\| ${d} \|" "${REG}" | cut -d: -f1 | tr '\n' ' ')lines"
   39      done
   40      FAIL=1
   41  fi
   42  ids=$(grep -o -E '^\| D-[A-Z]+-[0-9]+ ' "${REG}" | tr -d '| ' | sort -u)
   43  
   44  # 2. every citation resolves. Live documents only; the register's own rows
   45  #    cite earlier rows and are included.
   46  LIVE=(
   47      "${REG}"
   48      "${ROOT}/CLAUDE.md" "${ROOT}/AGENTS.md"
   49      "${ROOT}/.claude/rules" "${ROOT}/.claude/skills"
   50      "${ROOT}/docs/blindspot-register.md" "${ROOT}/docs/cloud-sync-changelog.md"
   51      "${ROOT}/docs/es-menu-map.md" "${ROOT}/docs/device-testing-policy.md"
   52      "${ROOT}/docs/device-flashing-runbook.md"
   53      "${ROOT}/projects/ROCKNIX/packages/network/rclone/sources"
   54      "${ROOT}/projects/ROCKNIX/packages/network/raofflineproxy/sources"
   55      "${ROOT}/projects/ROCKNIX/packages/network/raofflineproxy/patches"
   56      "${ROOT}/projects/ROCKNIX/packages/rocknix/sources/scripts"
   57      "${ROOT}/projects/ROCKNIX/packages/sysutils/systemd/scripts"
   58      "${ROOT}/tools"
   59  )
   60  # EmulationStation's sources are optional -- the checkout is not part of this
   61  # tree -- but once ES_SRC names one, it is an input like the others.
   62  if [ -n "${ES_SRC:-}" ]; then
   63      LIVE+=("${ES_SRC}/es-app/src" "${ES_SRC}/es-core/src")
   64  fi
   65  for p in "${LIVE[@]}"; do
   66      if [ ! -r "${p}" ]; then
   67          echo "UNREADABLE ${p#${ROOT}/}: it is a live document and was not checked"
   68          FAIL=1
   69      fi
   70  done
   71  missing=0
   72  while IFS=: read -r file line cite; do
   73      [ -n "${cite}" ] || continue
   74      case "${cite}" in *-000) continue ;; esac            # a placeholder in prose ("D-CLOUD-000")
   75      if ! grep -qx "${cite}" <<< "${ids}"; then
   76          echo "MISSING ${cite}: ${file#${ROOT}/}:${line}"
   77          missing=$((missing + 1))
   78      fi
   79  done < <(grep -rn -o -E "${CITE}" "${LIVE[@]}" 2>/dev/null \
   80           | grep -v -F "${REG}:" \
   81           | sed -E 's/^([^:]+):([0-9]+):(.*)$/\1:\2:\3/' | sort -u)
   82  # the register's own cross-references (a row citing an earlier row)
   83  while IFS= read -r cite; do
   84      grep -qx "${cite}" <<< "${ids}" || { echo "MISSING ${cite}: cited inside the register"; missing=$((missing + 1)); }
   85  done < <(grep -o -E "${CITE}" "${REG}" | sort -u)
   86  # 3. a placeholder that was never filled in: an ID ending in "0" and two
   87  # letters shipped in the image-cache helper's header for six days, because
   88  # letters after the digit are not [0-9]+\b and the citation pattern walked
   89  # past it (audit #258 PL-011). A letter where the number goes is a row
   90  # somebody meant to write; name it. (The shape is not spelled out here: this
   91  # file is one of the inputs.)
   92  while IFS=: read -r file line cite; do
   93      [ -n "${cite}" ] || continue
   94      echo "PLACEHOLDER ${cite}: ${file#${ROOT}/}:${line} -- a decision ID with letters where its number goes"
   95      missing=$((missing + 1))
   96  done < <(grep -rn -o -E 'D-[A-Z]+-[0-9]*[a-z?]+[0-9a-z?]*\b' "${LIVE[@]}" 2>/dev/null | grep -v -F "${REG}:" | sort -u)
   97  [ "${missing}" -eq 0 ] || FAIL=1
   98  
   99  n_rows=$(printf '%s\n' "${ids}" | grep -c .)
  100  if [ "${FAIL}" -eq 0 ]; then
  101      echo "register-check: ${n_rows} IDs, each once; every citation in the live documents names a row"
  102      exit 0
  103  fi
  104  echo "register-check: FAILED"
  105  exit 1
```

## File: tools/release-catalog (at 8ebaf8daad, 107 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # What did each cut carry, what was proven on it, and where is it now? One
    6  # generated page from the RECORD.txt beside every kept image, so the question
    7  # is a lookup and not an archaeology (#267, D-WORKFLOW-044).
    8  #
    9  #   tools/release-catalog --write        # regenerate docs/releases/catalog.md
   10  #   tools/release-catalog --check        # exit 1 when the page is stale (serval only:
   11  #                                        #   the artifacts live outside the repo)
   12  #   tools/release-catalog                # print the table
   13  #
   14  # Reads /workspace/artifacts/rocknix-images/*/RECORD.txt (ARTIFACTS overrides).
   15  # A RECORD.txt is `KEY<spaces>value` lines with continuation lines indented;
   16  # the keys this reads: BUILD_ID, Built, Replaces, Delta, Proof, Device, Files,
   17  # Superseded. The standing device facts are the hand-kept page beside the
   18  # catalog, docs/releases/device-facts.md, which this tool does not write.
   19  
   20  import glob
   21  import os
   22  import re
   23  import sys
   24  
   25  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   26  ARTIFACTS = os.environ.get('ARTIFACTS', '/workspace/artifacts/rocknix-images')
   27  PAGE = os.path.join(ROOT, 'docs/releases/catalog.md')
   28  KEYS = ('BUILD_ID', 'Built', 'Replaces', 'Delta', 'Proof', 'Device', 'Files', 'Superseded')
   29  
   30  
   31  def parse(path):
   32      rec = {'title': '', 'folder': os.path.basename(os.path.dirname(path))}
   33      key = None
   34      for line in open(path, encoding='utf-8', errors='replace'):
   35          line = line.rstrip('\n')
   36          if not rec['title'] and not key:
   37              rec['title'] = line.strip()
   38              continue
   39          m = re.match(r'^([A-Za-z_]+)\s{2,}(.*)$', line)
   40          if m and m.group(1) in KEYS:
   41              key = m.group(1)
   42              rec[key] = m.group(2).strip()
   43          elif key and line.startswith(' '):
   44              rec[key] += ' ' + line.strip()
   45      return rec
   46  
   47  
   48  def clip(s, n):
   49      s = ' '.join((s or '').split())
   50      return s if len(s) <= n else s[:n - 1] + '…'
   51  
   52  
   53  def state(rec):
   54      d = rec.get('Device', '')
   55      if rec.get('Superseded'):
   56          return 'superseded'
   57      if re.search(r'^On the|since \d{4}-\d\d-\d\d', d):
   58          return 'on a device'
   59      if 'Not staged' in d:
   60          return 'not staged'
   61      return d[:20] or '-'
   62  
   63  
   64  def render(recs):
   65      out = ['# Release catalog', '',
   66             'Generated by `tools/release-catalog --write` from the `RECORD.txt` beside every kept',
   67             'image under `/workspace/artifacts/rocknix-images/`; do not edit by hand. One row per',
   68             'cut, newest first; the full RECORD.txt is the row\'s evidence. The standing device',
   69             'facts -- what only a handheld can show, and when each was last seen -- are',
   70             '[device-facts.md](device-facts.md), kept by hand (D-WORKFLOW-044, #267).', '',
   71             '| Kept as | Cut | BUILD_ID | Built | Where it is | What it carried | Proof |',
   72             '| --- | --- | --- | --- | --- | --- | --- |']
   73      for r in recs:
   74          cut = re.search(r'([a-z]+(?:-[a-z]+)? cut)', r.get('title', '')) or re.search(r'(RC-\d+)', r.get('title', ''))
   75          out.append('| `%s` | %s | `%s` | %s | %s | %s | %s |' % (
   76              r['folder'], cut.group(1) if cut else clip(r.get('title', ''), 40),
   77              (r.get('BUILD_ID', '') or '-').split(' ')[0], clip(r.get('Built', ''), 40),
   78              clip(r.get('Device', '') if state(r) != 'superseded' else 'superseded: ' + r.get('Superseded', ''), 140),
   79              clip(r.get('Delta', ''), 220), clip(r.get('Proof', ''), 220)))
   80      out += ['', '%d cuts with a RECORD.txt. A folder without one is an image nobody recorded, which is the' % len(recs),
   81              'shape #257 and the runbook forbid: write the RECORD.txt before the copy.', '']
   82      return '\n'.join(out)
   83  
   84  
   85  def main():
   86      paths = glob.glob(os.path.join(ARTIFACTS, '*', 'RECORD.txt'))
   87      recs = [parse(p) for p in paths]
   88      recs.sort(key=lambda r: (r.get('Built', ''), r['folder']), reverse=True)
   89      text = render(recs)
   90      if '--write' in sys.argv:
   91          os.makedirs(os.path.dirname(PAGE), exist_ok=True)
   92          open(PAGE, 'w', encoding='utf-8').write(text)
   93          print('wrote %s (%d cuts)' % (os.path.relpath(PAGE, ROOT), len(recs)))
   94          return 0
   95      if '--check' in sys.argv:
   96          cur = open(PAGE, encoding='utf-8').read() if os.path.exists(PAGE) else ''
   97          if cur != text:
   98              print('release-catalog: docs/releases/catalog.md is stale; run tools/release-catalog --write')
   99              return 1
  100          print('release-catalog: current (%d cuts)' % len(recs))
  101          return 0
  102      print(text)
  103      return 0
  104  
  105  
  106  if __name__ == '__main__':
  107      sys.exit(main())
```

## File: tools/renovation-drift (at 2174265e9c, 212 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """renovation-drift -- what changed under each closed renovation slice since its fixes merged
    5  (plan § 8; M6.P1, #641).
    6  
    7    tools/renovation-drift [--write docs/reviews/drift.md] [--target next]
    8                           [--pretend SLICE=HASH[,es=HASH] ...]
    9    tools/renovation-drift --self-test
   10  
   11  For every slice in docs/reviews/slices.json with a `fixed_at` (written at the
   12  slice's stage H as {"distribution": <commit>, "es": <commit>}, the `es` key
   13  for a slice with EmulationStation paths; a bare string is a distribution
   14  commit), it diffs from the baseline to `<target>` over the slice's paths. The
   15  baseline is `drift_checked_at` when a drift review has accepted the changes
   16  since (it then advances, so reviewed drift is not reported again), else
   17  `fixed_at`; a dependency replaced under a slice (an interacting subsystem,
   18  not its own paths) is the planner's call, recorded on the slice issue, not
   19  this tool's
   20  (the slice's rows of docs/reviews/inventory.json, the same membership
   21  `tools/renovation-inventory --order` uses) and reports the files touched, the
   22  lines changed, that as a share of the slice's lines, and whether a file on
   23  slices.json's `sensitive` lists (security, state, launch-path) was touched.
   24  The EmulationStation target is the pin `<target>` carries in
   25  projects/ROCKNIX/packages/ui/emulationstation/package.mk.
   26  
   27  Plan § 8: a slice whose drift is under 20 % of its lines and touches no
   28  sensitive file is re-reviewed at issue tier (`small`); one at 20 % or more, or
   29  touching a sensitive file, re-opens (`re-open`), and a sensitive file
   30  re-opens at Extended depth whatever the slice's own (order.md). A table
   31  slice's share is counted in rows (paths changed of its paths), since its
   32  work is rows, not lines.
   33  
   34  Exit 0 when no slice needs re-opening, 1 when one does, 2 when it cannot run
   35  (an unreadable ledger, a missing commit, a git command failing).
   36  `--pretend` sets a fixed_at for this run only, so the report can be seen to
   37  fire before any slice has closed.
   38  """
   39  
   40  import argparse
   41  import importlib.machinery
   42  import importlib.util
   43  import json
   44  import os
   45  import re
   46  import subprocess
   47  import sys
   48  
   49  EX_FAIL, EX_CANNOT = 1, 2
   50  SMALL_SHARE = 0.20  # plan § 8
   51  ES_DEFAULT = "/home/max/Development/emulationstation-next"
   52  PIN_FILE = "projects/ROCKNIX/packages/ui/emulationstation/package.mk"
   53  
   54  
   55  def load_inventory_module(dist):
   56      path = os.path.join(dist, "tools/renovation-inventory")
   57      loader = importlib.machinery.SourceFileLoader("renovation_inventory", path)
   58      spec = importlib.util.spec_from_loader("renovation_inventory", loader)
   59      mod = importlib.util.module_from_spec(spec)
   60      loader.exec_module(mod)
   61      return mod
   62  
   63  
   64  def git(repo, *args):
   65      r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
   66      if r.returncode != 0:
   67          raise RuntimeError("git %s: %s" % (" ".join(args[:3]), r.stderr.strip()[:300]))
   68      return r.stdout
   69  
   70  
   71  _NUMSTAT = {}
   72  
   73  
   74  def numstat(repo, base, target, paths):
   75      """{path: lines changed} over paths between two commits; deletions count. One whole-tree diff per
   76      (repo, base, target), filtered by the path set: git diff takes no --pathspec-from-file."""
   77      key = (repo, base, target)
   78      if key not in _NUMSTAT:
   79          out = git(repo, "-c", "core.quotePath=false", "diff", "--numstat", "--no-renames", "-z", base, target)
   80          res = {}
   81          for rec in out.split("\0"):
   82              if rec:
   83                  a, d, p = rec.split("\t", 2)
   84                  res[p] = (0 if a == "-" else int(a)) + (0 if d == "-" else int(d))
   85          _NUMSTAT[key] = res
   86      want = set(paths)
   87      return {p: n for p, n in _NUMSTAT[key].items() if p in want}
   88  
   89  
   90  def verdict(changed, slice_lines, sensitive_hits, table_paths=None):
   91      """small | re-open | none, by plan § 8. A table slice's share is in rows (paths), not lines."""
   92      if not changed:
   93          return "none"
   94      share = len(changed) / max(table_paths, 1) if table_paths else sum(changed.values()) / max(slice_lines, 1)
   95      return "re-open" if sensitive_hits or share >= SMALL_SHARE else "small"  # under 20 % small; 20 % or more re-opens
   96  
   97  
   98  def run(args):
   99      dist = os.path.realpath(args.distribution)
  100      inv_mod = load_inventory_module(dist)
  101      with open(os.path.join(dist, "docs/reviews/inventory.json")) as f:
  102          inv = json.load(f)
  103      rows = [dict(zip(inv["columns"], r)) for r in inv["rows"]]
  104      doc, slices = inv_mod.load_slices(dist)
  105      pretend = {}
  106      for p in args.pretend or []:
  107          sid, _, rest = p.partition("=")
  108          parts = rest.split(",")
  109          fx = {"distribution": parts[0]}
  110          for x in parts[1:]:
  111              k, _, v = x.partition("=")
  112              fx[k] = v
  113          pretend[sid] = fx
  114      members = {sl["id"]: {"distribution": [], "es": [], "lines": 0} for sl, _ in slices}
  115      for r in rows:
  116          hits = inv_mod.slice_of(r, slices)
  117          if len(hits) == 1:
  118              m = members[hits[0]]
  119              m[r["tree"]].append(r["path"])
  120              m["lines"] += r["lines"] or 0
  121      sens = inv_mod.load_areas([{"area": k, "globs": g} for k, g in doc.get("sensitive", {}).items()])
  122      target = git(dist, "rev-parse", args.target).strip()
  123      es_pin = None
  124      report, worst = [], 0
  125      for sl, _ in slices:
  126          fixed = pretend.get(sl["id"]) or sl.get("drift_checked_at") or sl.get("fixed_at")
  127          if not fixed:
  128              continue
  129          if isinstance(fixed, str):
  130              fixed = {"distribution": fixed}
  131          m = members[sl["id"]]
  132          changed, hit = {}, []
  133          if m["distribution"]:
  134              base = fixed.get("distribution")
  135              if not base:
  136                  raise RuntimeError("slice %s has distribution paths and no distribution fixed_at" % sl["id"])
  137              git(dist, "cat-file", "-e", base + "^{commit}")
  138              for p, n in numstat(dist, base, target, m["distribution"]).items():
  139                  changed[p] = n
  140                  hit += [k for k, inc, _ in sens if any(x.match(p) for x in inc.get("distribution", []))]
  141          if m["es"]:
  142              base = fixed.get("es")
  143              if not base:
  144                  raise RuntimeError("slice %s has EmulationStation paths and no es fixed_at" % sl["id"])
  145              if es_pin is None:
  146                  text = git(dist, "show", "%s:%s" % (args.target, PIN_FILE))
  147                  es_pin = re.search(r'^PKG_VERSION="([0-9a-f]{40})"', text, re.M).group(1)
  148              git(args.es, "cat-file", "-e", base + "^{commit}")
  149              for p, n in numstat(args.es, base, es_pin, m["es"]).items():
  150                  changed["es:" + p] = n
  151                  hit += [k for k, inc, _ in sens if any(x.match(p) for x in inc.get("es", []))]
  152          table = sl.get("kind") == "table"
  153          npaths = len(m["distribution"]) + len(m["es"])
  154          v = verdict(changed, m["lines"], hit, npaths if table else None)
  155          worst = max(worst, {"none": 0, "small": 0, "re-open": 1}[v])
  156          report.append((sl, fixed, len(changed), sum(changed.values()), npaths if table else m["lines"],
  157                         sorted(set(hit)), v, "pretend" if sl["id"] in pretend else "slices.json", table))
  158      lines = ["# Renovation drift", "",
  159               "Generated by `tools/renovation-drift` against `%s` (`%s`); never hand-edited. Plan § 8: under 20 %% of a "
  160               "slice's lines and no sensitive file is `small` (an issue-tier pass over the diff); over 20 %%, or any "
  161               "security, state or launch-path file, is `re-open` (the slice at its depth, over the diff)." % (
  162                   args.target, target[:10]), "",
  163               "| k | Slice | fixed-at | Files | Lines changed | Share of slice | Sensitive touched | Verdict | Source |",
  164               "| ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- |"]
  165      for sl, fixed, files, changed, total, hit, v, src, table in report:
  166          lines.append("| %d | %s | %s | %d | %d | %.1f %%%s | %s | %s | %s |" % (
  167              sl["k"], sl["id"], ", ".join("%s `%s`" % (k, h[:10]) for k, h in fixed.items()), files, changed,
  168              100.0 * (files if table else changed) / max(total, 1), " of rows" if table else "",
  169              ", ".join(hit) or "--", v, src))
  170      if not report:
  171          lines.append("| -- | no slice has a `fixed_at` yet | | | | | | | |")
  172      text = "\n".join(lines) + "\n"
  173      print(text, end="")
  174      if args.write:
  175          with open(os.path.join(dist, args.write), "w") as f:
  176              f.write(text)
  177      return worst
  178  
  179  
  180  def self_test():
  181      cases = [({}, 1000, [], None, "none"), ({"a": 10}, 1000, [], None, "small"), ({"a": 201}, 1000, [], None, "re-open"),
  182               ({"a": 1}, 1000, ["launch-path"], None, "re-open"), ({"a": 199}, 1000, [], None, "small"), ({"a": 200}, 1000, [], None, "re-open"),
  183               ({"a": 5000, "b": 1}, 0, [], 100, "small"), ({str(i): 1 for i in range(21)}, 0, [], 100, "re-open")]
  184      bad = 0
  185      for changed, total, hit, rows, want in cases:
  186          got = verdict(changed, total, hit, rows)
  187          bad += got != want
  188          print("%s %s of %d, sensitive %s -> %s (want %s)" % ("PASS" if got == want else "FAIL", changed, total, hit, got, want))
  189      print("self-test: %s" % ("PASS" if not bad else "FAIL (%d)" % bad))
  190      return 0 if not bad else EX_FAIL
  191  
  192  
  193  def main():
  194      ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  195      ap.add_argument("--distribution", default=".")
  196      ap.add_argument("--es", default=ES_DEFAULT)
  197      ap.add_argument("--target", default="next")
  198      ap.add_argument("--write", help="also write the table here (docs/reviews/drift.md)")
  199      ap.add_argument("--pretend", action="append", help="SLICE=HASH[,es=HASH]: a fixed_at for this run only")
  200      ap.add_argument("--self-test", action="store_true")
  201      args = ap.parse_args()
  202      if args.self_test:
  203          return self_test()
  204      try:
  205          return run(args)
  206      except (RuntimeError, OSError, ValueError, KeyError, AttributeError) as e:
  207          print("renovation-drift: cannot run: %s" % e, file=sys.stderr)
  208          return EX_CANNOT
  209  
  210  
  211  if __name__ == "__main__":
  212      sys.exit(main())
```

## File: tools/renovation-inventory (at 2174265e9c, 1597 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """renovation-inventory -- every tracked path of the distribution and of the
    5  EmulationStation fork, with its area, provenance tier, language, lines, last
    6  commits and reachability by the images the Makefile builds (M6.P1, #641).
    7  
    8    tools/renovation-inventory [--distribution DIR] [--es DIR]
    9        [--areas docs/reviews/areas.json] [--plans DIR]
   10        [--out docs/reviews/inventory.json] [--markdown docs/reviews/inventory.md]
   11        [--inject-path PATH ...] [--no-write]
   12    tools/renovation-inventory --self-test
   13  
   14  Prints, and exits 1 unless each pair agrees and both counters are 0:
   15    paths: N (git ls-files: N)
   16    es-paths: N (git ls-files: N)
   17    patches: N (find: N)
   18    unassigned: N
   19    ambiguous: N
   20  
   21  Exit 2 when it cannot run (a git command, a plan, a missing input).
   22  
   23  Rules (docs/reviews/README.md, the futro of 2026-10-22):
   24  
   25  - The inventory reads committed trees: the distribution at its HEAD, the ES
   26    checkout at its HEAD (a detached worktree at the pin). Each total is checked
   27    against `git ls-files` there, so staged-but-uncommitted paths fail the run.
   28  - Areas: a glob is relative to the distribution unless prefixed `es:`; a glob
   29    prefixed `!` excludes within its own area; `**` crosses `/`, `*` and `?`
   30    stay inside a segment, `{a,b}` alternates globs (no nesting). A path must match
   31    exactly one area: none counts as `unassigned`, two or more as `ambiguous`.
   32    A bare `**` on the distribution is refused, since it would make
   33    `unassigned` 0 whatever the tree held.
   34  - Tiers: fork-own is `git diff --name-only <merge-base> HEAD` (the merge base
   35    with upstream/next, or on ES with rocknix/master); a fork-own path that
   36    upstream also changed since the base carries `overlap`. Every other path is
   37    upstream-carried. Every `*.patch` and kernel `linux*.conf` under packages/
   38    or projects/ is vendor-carried, `tier_note: fork-written` when fork-own.
   39  - Reachability: `tools/viewplan` per device and arch the Makefile builds,
   40    `image` for the 64-bit plans and `arm` (projects/ROCKNIX/packages/virtual/arm)
   41    for 32-bit where the device's ENABLE_32BIT is true, with PROJECT, DEVICE
   42    and ARCH always set, run by default in the build image the Makefile pins
   43    by digest (it must be local; `--runner host` is the explicit alternative,
   44    recorded in the header): the host lacks xmlstarlet, which
   45    distributions/ROCKNIX/config/functions needs for SUBDEVICES, and a host plan
   46    silently drops every subdevice bootloader. The checkout is mounted
   47    read-only and BUILD_DIR sits in the container's /tmp; on the host BUILD_DIR
   48    is a directory this tool owns. Either way the run fails if the checkout's
   49    ignored set changes. Each package in a plan is
   50    then sourced with config/functions' `source_package`, and its PKG_DIR,
   51    PKG_VERSION and PKG_PATCH_DIRS give the patch directories scripts/unpack
   52    would apply, by unpack's own rules. A path inside a package directory is
   53    reached when that directory is a plan package's PKG_DIR (a patch only when
   54    its directory is selected); a generic package.mk sourced by a reached
   55    override is reached with it; a device's own files are reached by that
   56    device's plans; projects/ROCKNIX's bootloader, filesystem, options and
   57    config.xml by every plan; ES by the plans that build emulationstation; the
   58    other projects/ and distributions/ (DISTRO is always ROCKNIX) by none.
   59    `reach` is `shipped` (a shipped device's plan), `test` (the test image's
   60    plan and no shipped device's), `unshipped` (only other devices' plans),
   61    `unreached` (a package or project path no plan reaches),
   62    or `n/a` (a path no image plan can hold: the engine, tools, doctrine,
   63    records). Reachability errs toward reached: a file in a reached package is
   64    reached even if its recipe installs it only for some devices.
   65  """
   66  
   67  import argparse
   68  import concurrent.futures
   69  import json
   70  import os
   71  import re
   72  import shutil
   73  import subprocess
   74  import sys
   75  import tempfile
   76  import time
   77  from collections import Counter, defaultdict
   78  
   79  EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
   80  SHIPPED = ("H700", "SM8550")  # D-WORKFLOW-185: the devices the fork ships
   81  TEST = ("GENERIC_X64",)  # D-WORKFLOW-185: the test image, built and proven on, never shipped
   82  EX_FAIL, EX_CANNOT = 1, 2
   83  COLUMNS = ["tree", "path", "area", "tier", "tier_note", "overlap", "language",
   84             "lines", "patches", "last_fork_commit", "last_upstream_commit",
   85             "reach", "reachable_by", "buildable_by", "shadowed_by"]
   86  
   87  SOURCE_HELPER = r'''
   88  . config/options "" >/dev/null 2>&1 || { echo "META-FAIL config/options"; exit 0; }
   89  printf 'META\t%s\t%s\n' "${ENABLE_32BIT}" "${ROOT}"
   90  while read -r name; do
   91    [ -n "${name}" ] || continue
   92    exited=0
   93    exit() { exited=1; }
   94    if source_package "${name}" >/dev/null 2>&1 && [ ${exited} -eq 0 ]; then
   95      if [ "${TARGET_ARCH}" = "x86_64" ]; then
   96        PATCH_ARCH="x86"
   97      elif [ "${PKG_IS_KERNEL_PKG}" = "yes" ]; then
   98        PATCH_ARCH="${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}"
   99      else
  100        PATCH_ARCH="${TARGET_PATCH_ARCH:-${TARGET_ARCH}}"
  101      fi
  102      printf 'PKG\t%s\t%s\t%s\t%s\t%s\t%s\n' "${name}" "${PKG_NAME}" "${PKG_DIR}" \
  103        "${PKG_VERSION}" "${PATCH_ARCH}" "${PKG_PATCH_DIRS}"
  104    else
  105      printf 'SKIP\t%s\n' "${name}"
  106    fi
  107    unset -f exit
  108  done
  109  '''
  110  
  111  
  112  class CannotRun(Exception):
  113      pass
  114  
  115  
  116  def git(repo, *args, text=True):
  117      r = subprocess.run(["git", "-C", repo, "-c", "core.quotePath=false", *args],
  118                         capture_output=True, text=text)
  119      if r.returncode != 0:
  120          raise CannotRun("git %s: %s" % (" ".join(args[:3]), (r.stderr or "").strip()[:300]))
  121      return r.stdout
  122  
  123  
  124  def zsplit(out):
  125      return [p for p in out.split("\0") if p]
  126  
  127  
  128  # ---- globs and areas -------------------------------------------------------
  129  
  130  def glob_re(g):
  131      return re.compile(glob_body(g) + r"\Z")
  132  
  133  
  134  def glob_body(g):
  135      out, i = "", 0
  136      while i < len(g):
  137          if g.startswith("**/", i):
  138              out += "(?:.*/)?"
  139              i += 3
  140          elif g.startswith("**", i):
  141              out += ".*"
  142              i += 2
  143          elif g[i] == "*":
  144              out += "[^/]*"
  145              i += 1
  146          elif g[i] == "?":
  147              out += "[^/]"
  148              i += 1
  149          elif g[i] == "{":  # each alternative is itself a glob (no nested braces)
  150              j = g.index("}", i)
  151              out += "(?:" + "|".join(glob_body(x) for x in g[i + 1:j].split(",")) + ")"
  152              i = j + 1
  153          else:
  154              out += re.escape(g[i])
  155              i += 1
  156      return out
  157  
  158  
  159  def load_areas(areas):
  160      """[(name, {tree: [include re]}, {tree: [exclude re]})]; refuses a catch-all."""
  161      compiled = []
  162      for a in areas:
  163          inc, exc = defaultdict(list), defaultdict(list)
  164          for g in a["globs"]:
  165              neg = g.startswith("!")
  166              g = g[1:] if neg else g
  167              tree = "es" if g.startswith("es:") else "distribution"
  168              g = g[3:] if tree == "es" else g
  169              if not neg and tree == "distribution" and g == "**":
  170                  raise CannotRun("area %s: a bare ** on the distribution would hide every unassigned path" % a["area"])
  171              (exc if neg else inc)[tree].append(glob_re(g))
  172          compiled.append((a["area"], inc, exc))
  173      return compiled
  174  
  175  
  176  def assign(compiled, tree, path):
  177      hits = [name for name, inc, exc in compiled
  178              if any(r.match(path) for r in inc.get(tree, ()))
  179              and not any(r.match(path) for r in exc.get(tree, ()))]
  180      return hits
  181  
  182  
  183  # ---- per-tree facts ----------------------------------------------------------
  184  
  185  def tracked(repo):
  186      head = zsplit(git(repo, "ls-tree", "-r", "-z", "--name-only", "HEAD"))
  187      index = zsplit(git(repo, "ls-files", "-z"))
  188      return head, len(index)
  189  
  190  
  191  def line_counts(repo):
  192      lines = {}
  193      out = zsplit(git(repo, "diff-tree", "-r", "--numstat", "-z", "--no-renames", EMPTY_TREE, "HEAD"))
  194      for rec in out:
  195          added, _deleted, path = rec.split("\t", 2)
  196          lines[path] = None if added == "-" else int(added)
  197      return lines
  198  
  199  
  200  def last_commits(repo, rev):
  201      """{path: "<hash10> <yyyy-mm-dd>"} for the newest commit in rev touching it."""
  202      out = git(repo, "log", "--no-renames", "--format=%x01%H %cs", "--name-only", rev)
  203      seen, current = {}, None
  204      for line in out.split("\n"):
  205          if line.startswith("\x01"):
  206              h, d = line[1:].split(" ", 1)
  207              current = "%s %s" % (h[:10], d)
  208          elif line and current:
  209              if line.startswith('"') and line.endswith('"'):
  210                  line = line[1:-1].encode("latin-1", "backslashreplace").decode("unicode_escape").encode("latin-1").decode("utf-8", "replace")
  211              seen.setdefault(line, current)
  212      return seen
  213  
  214  
  215  SHEBANGS = (("python", "python"), ("bash", "shell"), ("/sh", "shell"), ("busybox", "shell"),
  216              ("env sh", "shell"), ("node", "javascript"), ("perl", "perl"), ("tsx", "typescript"))
  217  EXT = {
  218      ".sh": "shell", ".bash": "shell", ".py": "python", ".mk": "make", ".patch": "patch",
  219      ".diff": "patch", ".c": "c", ".h": "c-header", ".cpp": "c++", ".cc": "c++", ".hpp": "c++-header",
  220      ".dts": "devicetree", ".dtsi": "devicetree", ".md": "markdown", ".json": "json", ".yml": "yaml",
  221      ".yaml": "yaml", ".xml": "xml", ".conf": "config", ".cfg": "config", ".ini": "config",
  222      ".service": "systemd", ".timer": "systemd", ".target": "systemd", ".mount": "systemd",
  223      ".socket": "systemd", ".path": "systemd", ".rules": "udev", ".ts": "typescript", ".mjs": "javascript",
  224      ".js": "javascript", ".html": "html", ".css": "css", ".txt": "text", ".po": "translation",
  225      ".pot": "translation", ".png": "image", ".jpg": "image", ".jpeg": "image", ".svg": "image",
  226      ".gif": "image", ".ttf": "font", ".otf": "font", ".log": "log", ".csv": "data", ".tsv": "data",
  227      ".cmake": "cmake", ".glsl": "shader", ".lua": "lua", ".toml": "config", ".rs": "rust", ".go": "go",
  228      ".java": "java", ".kt": "kotlin", ".asm": "assembly", ".s": "assembly", ".S": "assembly",
  229  }
  230  NAMES = {"package.mk": "recipe", "Makefile": "make", "Dockerfile": "docker", "CMakeLists.txt": "cmake",
  231           "options": "shell", "Kconfig": "kconfig"}
  232  
  233  
  234  def language(root, path):
  235      base = path.rsplit("/", 1)[-1]
  236      if base in NAMES:
  237          return NAMES[base]
  238      if re.match(r"linux.*\.conf\Z", base) and (path.startswith("packages/") or path.startswith("projects/")):
  239          return "kernel-config"
  240      stem, dot, ext = base.rpartition(".")
  241      if dot and stem and ext:
  242          lang = EXT.get("." + ext) or EXT.get("." + ext.lower())
  243          if lang:
  244              return lang
  245      full = os.path.join(root, path)
  246      try:
  247          if os.path.islink(full):
  248              return "symlink"
  249          with open(full, "rb") as f:
  250              head = f.read(96)
  251      except OSError:
  252          return "unknown"
  253      if head.startswith(b"#!"):
  254          first = head.split(b"\n", 1)[0].decode("utf-8", "replace")
  255          for key, lang in SHEBANGS:
  256              if key in first:
  257                  return lang
  258          return "script"
  259      return "other" if dot else "none"
  260  
  261  
  262  def is_vendor(path):
  263      if not (path.startswith("packages/") or path.startswith("projects/")):
  264          return False
  265      base = path.rsplit("/", 1)[-1]
  266      return base.endswith(".patch") or bool(re.match(r"linux.*\.conf\Z", base))
  267  
  268  
  269  # ---- reachability ------------------------------------------------------------
  270  
  271  def makefile_configs(dist):
  272      """[(device, arch)] in Makefile order, from its PROJECT=ROCKNIX DEVICE= ARCH= build_distro lines."""
  273      with open(os.path.join(dist, "Makefile")) as f:
  274          text = f.read()
  275      seen = []
  276      for dev, arch in re.findall(r"PROJECT=ROCKNIX DEVICE=(\S+) ARCH=(\S+) \./scripts/build_distro", text):
  277          if (dev, arch) not in seen:
  278              seen.append((dev, arch))
  279      return seen
  280  
  281  
  282  def plan_env(dist, device, arch, build_dir):
  283      env = {k: v for k, v in os.environ.items()
  284             if k not in ("PROJECT", "DEVICE", "ARCH", "DEVICE_ROOT", "BUILD_DIR", "DISTRO")
  285             and not k.startswith("_CACHE_PACKAGE") and not k.startswith("_DEBUG_")}
  286      env.update(PROJECT="ROCKNIX", DEVICE=device, ARCH=arch, BUILD_DIR=build_dir)
  287      for var in ("PROJECT", "DEVICE", "ARCH"):  # config/options defaults DEVICE to SM8550 when unset
  288          if not env.get(var):
  289              raise CannotRun("%s unset for a plan run" % var)
  290      return env
  291  
  292  
  293  def pinned_image(dist):
  294      """The build container the Makefile pins, by digest; it must already be local (never pulled here)."""
  295      with open(os.path.join(dist, "Makefile")) as f:
  296          m = re.search(r"DOCKER_IMAGE_DIGEST\s*:=\s*(sha256:[0-9a-f]{64})", f.read())
  297      if not m:
  298          raise CannotRun("no DOCKER_IMAGE_DIGEST in the Makefile")
  299      r = subprocess.run(["docker", "image", "inspect", "--format", "{{.Id}}", m.group(1)], capture_output=True, text=True)
  300      if r.returncode != 0 or r.stdout.strip() != m.group(1):
  301          raise CannotRun("the pinned build image %s is not local (make docker-image-pull), or use --runner host" % m.group(1))
  302      return m.group(1)
  303  
  304  
  305  class Runner:
  306      """Runs a command in the build's own environment: the pinned container (default) or this host.
  307  
  308      The container gets the checkout and the main repository's .git read-only at their own paths,
  309      no network, the caller's uid, and BUILD_DIR in its own /tmp, so nothing it does can land in
  310      the checkout. The host runner sets BUILD_DIR to a directory this tool owns."""
  311  
  312      def __init__(self, mode, dist, scratch):
  313          self.mode, self.dist, self.scratch = mode, dist, scratch
  314          if mode == "container":
  315              self.image = pinned_image(dist)
  316              common = git(dist, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()
  317              self.mounts = ["-v", "%s:%s:ro" % (dist, dist), "-v", "%s:%s:ro" % (common, common)]
  318          else:
  319              self.image = None
  320  
  321      def run(self, device, arch, argv, stdin=""):
  322          if self.mode == "container":
  323              env = plan_env(self.dist, device, arch, "/tmp/renovation-plan")
  324              cmd = ["docker", "run", "--rm", "-i", "--network", "none", "--user", "%d:%d" % (os.getuid(), os.getgid()),
  325                     *self.mounts, "-w", self.dist, "-e", "HOME=/tmp"]
  326              for k in ("PROJECT", "DEVICE", "ARCH", "BUILD_DIR"):
  327                  cmd += ["-e", "%s=%s" % (k, env[k])]
  328              return subprocess.run(cmd + [self.image] + argv, input=stdin, capture_output=True, text=True)
  329          build_dir = tempfile.mkdtemp(prefix="plan-%s-%s-" % (device, arch), dir=self.scratch)
  330          env = plan_env(self.dist, device, arch, build_dir)
  331          return subprocess.run(argv, cwd=self.dist, env=env, input=stdin, capture_output=True, text=True)
  332  
  333  
  334  def one_plan(dist, device, arch, runner, plans_dir):
  335      meta = runner.run(device, arch, ["bash", "-c", SOURCE_HELPER], "")
  336      m = [l.split("\t") for l in meta.stdout.splitlines() if l.startswith("META")]
  337      if not m or m[0][0] != "META":
  338          raise CannotRun("config/options for %s-%s: %s" % (device, arch, meta.stdout[:200]))
  339      enable32, root = m[0][1], m[0][2]
  340      if os.path.realpath(root) != dist:  # PKG_DIR is reported under ROOT; a different ROOT reaches nothing
  341          raise CannotRun("config/options ROOT %s is not the distribution %s" % (root, dist))
  342      if arch == "arm" and enable32 != "true":
  343          return {"config": "%s-%s" % (device, arch), "skipped": "ENABLE_32BIT=%s" % enable32}
  344      root_pkg = "arm" if arch == "arm" else "image"
  345      plan_file = os.path.join(plans_dir, "plan-%s-%s.txt" % (device, arch)) if plans_dir else None
  346      if plan_file and os.path.exists(plan_file):
  347          with open(plan_file) as f:
  348              plan_text = f.read()
  349      else:
  350          r = runner.run(device, arch, ["tools/viewplan", root_pkg])
  351          if r.returncode != 0:
  352              raise CannotRun("viewplan %s for %s-%s exited %d: %s" % (root_pkg, device, arch, r.returncode, r.stderr[-300:]))
  353          plan_text = r.stdout
  354          if plan_file:
  355              with open(plan_file, "w") as f:
  356                  f.write(plan_text)
  357      names, actions = set(), Counter()
  358      for line in plan_text.splitlines():
  359          parts = line.split()
  360          if len(parts) >= 2 and parts[0] in ("build", "install", "unpack"):
  361              names.add(parts[1].split(":", 1)[0])  # "build openssl:host", "install rclone"
  362              actions[parts[0]] += 1
  363      if root_pkg not in names:  # "install image" in a 64-bit plan; "build arm" in a 32-bit one
  364          raise CannotRun("plan for %s-%s has no install of %s (actions %s)" % (device, arch, root_pkg, dict(actions)))
  365      r = runner.run(device, arch, ["bash", "-c", SOURCE_HELPER], "\n".join(sorted(names)) + "\n")
  366      pkgs, skipped = {}, []
  367      for line in r.stdout.splitlines():
  368          f = line.split("\t")
  369          if f[0] == "PKG":
  370              if not f[3].startswith(dist + "/"):
  371                  raise CannotRun("%s-%s: PKG_DIR %s is outside the distribution" % (device, arch, f[3]))
  372              pkgs[f[1]] = {"pkg_name": f[2], "dir": f[3], "version": f[4], "patch_arch": f[5], "patch_dirs": f[6].split()}
  373          elif f[0] == "SKIP":
  374              skipped.append(f[1])
  375      if not pkgs:
  376          raise CannotRun("no package of %s-%s could be sourced" % (device, arch))
  377      return {"config": "%s-%s" % (device, arch), "device": device, "arch": arch,
  378              "root": root_pkg, "packages": pkgs, "unsourced": sorted(skipped),
  379              "plan_lines": len(plan_text.splitlines())}
  380  
  381  
  382  def selected_patch_dirs(info, device, root):
  383      """The directories scripts/unpack globs *.patch in, as tree-relative paths."""
  384      d, name = info["dir"], info["pkg_name"]
  385      v, pa = info["version"], info["patch_arch"]
  386      prj = os.path.join(root, "projects", "ROCKNIX")
  387      dirs = [d + "/patches", d + "/patches/" + pa, d + "/patches/" + v, d + "/patches/%s/%s" % (v, pa),
  388              prj + "/patches/" + name, prj + "/patches/%s/%s" % (name, pa), prj + "/patches/%s/%s" % (name, v),
  389              prj + "/devices/%s/patches/%s" % (device, name)]
  390      for p in info["patch_dirs"]:
  391          if p.startswith("/"):
  392              dirs.append(p)
  393          else:
  394              dirs += [d + "/patches/" + p, prj + "/patches/%s/%s" % (name, p),
  395                       prj + "/devices/%s/patches/%s/%s" % (device, name, p)]
  396      out = set()
  397      for x in dirs:
  398          x = os.path.normpath(x)
  399          if x.startswith(root + "/"):
  400              out.add(x[len(root) + 1:])
  401      return out
  402  
  403  
  404  def package_dirs(paths):
  405      return {p[:-len("/package.mk")] for p in paths if p.endswith("/package.mk")}
  406  
  407  
  408  def owning_dir(path, pkgdirs):
  409      parts = path.split("/")
  410      for i in range(len(parts) - 1, 0, -1):
  411          cand = "/".join(parts[:i])
  412          if cand in pkgdirs:
  413              return cand
  414      return None
  415  
  416  
  417  SOURCED = re.compile(r"\$\{?ROOT\}?/((?:packages|projects)/[^\s\"']*?)/package\.mk")
  418  
  419  
  420  def compute_reach(dist, paths, plans, devices):
  421      """{path: set(configs)} for distribution paths; None for n/a paths."""
  422      pkgdirs = package_dirs(paths)
  423      sourced = {}
  424      for d in pkgdirs:
  425          try:
  426              with open(os.path.join(dist, d, "package.mk"), errors="replace") as f:
  427                  sourced[d] = {m for m in SOURCED.findall(f.read()) if m in pkgdirs and m != d}
  428          except OSError:
  429              sourced[d] = set()
  430      built = defaultdict(set)          # package name -> the PKG_DIRs plans resolved it to
  431      reached_dir = defaultdict(set)    # package dir -> configs (non-patch files)
  432      reached_pdir = defaultdict(set)   # patch directory -> configs
  433      project_wide, by_device, es_configs = set(), defaultdict(set), set()
  434      for p in plans:
  435          if p.get("skipped"):
  436              continue
  437          cfg = p["config"]
  438          project_wide.add(cfg)
  439          by_device[p["device"]].add(cfg)
  440          for name, info in p["packages"].items():
  441              d = info["dir"]
  442              rel = d[len(dist) + 1:] if d.startswith(dist + "/") else d
  443              reached_dir[rel].add(cfg)
  444              built[name].add(rel)
  445              for s in sourced.get(rel, ()):
  446                  reached_dir[s + "/package.mk"].add(cfg)  # only the sourced recipe itself
  447              for pd in selected_patch_dirs(info, p["device"], dist):
  448                  reached_pdir[pd].add(cfg)
  449              if name == "emulationstation":
  450                  es_configs.add(cfg)
  451      reach = {}
  452      for path in paths:
  453          if path.startswith("distributions/") and not path.startswith("distributions/ROCKNIX/"):
  454              reach[path] = set()  # config/options: DISTRO defaults to ROCKNIX and nothing sets another
  455              continue
  456          if not (path.startswith("packages/") or path.startswith("projects/")):
  457              reach[path] = None
  458              continue
  459          if path.startswith("projects/") and not path.startswith("projects/ROCKNIX/"):
  460              reach[path] = set()  # other projects: no Makefile target sets their PROJECT
  461              continue
  462          if path.endswith(".patch"):
  463              reach[path] = set(reached_pdir.get(path.rsplit("/", 1)[0], ()))
  464              continue
  465          own = owning_dir(path, pkgdirs)
  466          if own:
  467              got = set(reached_dir.get(own, ())) | set(reached_dir.get(path, ()))
  468              reach[path] = got
  469              continue
  470          m = re.match(r"projects/ROCKNIX/devices/([^/]+)/", path)
  471          if m:
  472              reach[path] = set(by_device.get(m.group(1), ())) if m.group(1) in devices else set()
  473              continue
  474          if re.match(r"projects/ROCKNIX/(bootloader/|filesystem/|options\Z|config\.xml\Z)", path):
  475              reach[path] = set(project_wide)
  476              continue
  477          reach[path] = None  # README, templates and other non-package paths under packages/
  478      # A package directory whose name a plan builds from another directory is shadowed: the package
  479      # is live, this copy of it is not (get_pkg_directory resolves the override). Removing a shadowed
  480      # copy is a duplicate's removal (engineering-practices.md § Before deleting a duplicate).
  481      shadow = {d: sorted(built[d.rsplit("/", 1)[-1]])[0] for d in pkgdirs
  482                if built.get(d.rsplit("/", 1)[-1]) and d not in built[d.rsplit("/", 1)[-1]]}
  483      return reach, es_configs, shadow
  484  
  485  
  486  def split_reach(configs):
  487      """reach, reachable_by (the shipped and test configs), buildable_by (the rest)."""
  488      shipped = sorted(c for c in configs if c.rsplit("-", 1)[0] in SHIPPED)
  489      test = sorted(c for c in configs if c.rsplit("-", 1)[0] in TEST)
  490      other = sorted(c for c in configs if c.rsplit("-", 1)[0] not in SHIPPED + TEST)
  491      if shipped:
  492          return "shipped", sorted(shipped + test), other
  493      if test:
  494          return "test", test, other
  495      if other:
  496          return "unshipped", [], other
  497      return "unreached", [], []
  498  
  499  
  500  def ignored_set(repo):
  501      return git(repo, "status", "--porcelain", "--ignored", "-z")
  502  
  503  
  504  # ---- assembly ---------------------------------------------------------------
  505  
  506  def build(args):
  507      dist = os.path.realpath(args.distribution)
  508      es = os.path.realpath(args.es)
  509      with open(os.path.join(dist, args.areas) if not os.path.isabs(args.areas) else args.areas) as f:
  510          compiled = load_areas(json.load(f))
  511      t0 = time.time()
  512  
  513      upstream = "upstream/next"
  514      mb = git(dist, "merge-base", "HEAD", upstream).strip()
  515      head = git(dist, "rev-parse", "HEAD").strip()
  516      dpaths, d_index = tracked(dist)
  517      dlines = line_counts(dist)
  518      fork = set(zsplit(git(dist, "diff", "--name-only", "-z", "--no-renames", mb, "HEAD")))
  519      up_only = set(zsplit(git(dist, "diff", "--name-only", "-z", "--no-renames", mb, upstream)))
  520      d_last_fork = last_commits(dist, "%s..HEAD" % mb)
  521      d_last_up = last_commits(dist, upstream)
  522  
  523      es_head = git(es, "rev-parse", "HEAD").strip()
  524      es_up = "rocknix/master"
  525      emb = git(es, "merge-base", es_up, "HEAD").strip()
  526      epaths, e_index = tracked(es)
  527      elines = line_counts(es)
  528      efork = set(zsplit(git(es, "diff", "--name-only", "-z", "--no-renames", emb, "HEAD")))
  529      eup_only = set(zsplit(git(es, "diff", "--name-only", "-z", "--no-renames", emb, es_up)))
  530      e_last_fork = last_commits(es, "%s..HEAD" % emb)
  531      e_last_up = last_commits(es, es_up)
  532      t_git = time.time() - t0
  533  
  534      # reachability
  535      configs = makefile_configs(dist)
  536      devices = sorted({d for d, _ in configs})
  537      before = ignored_set(dist)
  538      scratch = tempfile.mkdtemp(prefix="renovation-inventory-")
  539      plans = []
  540      t1 = time.time()
  541      try:
  542          runner = Runner(args.runner, dist, scratch)
  543          with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
  544              futs = [ex.submit(one_plan, dist, d, a, runner, args.plans) for d, a in configs]
  545              for fu in futs:
  546                  plans.append(fu.result())
  547      finally:
  548          shutil.rmtree(scratch, ignore_errors=True)
  549      t_plans = time.time() - t1
  550      if ignored_set(dist) != before:
  551          raise CannotRun("the checkout's ignored set changed across the plan runs: something wrote into it")
  552      reach, es_configs, shadow = compute_reach(dist, dpaths, plans, devices)
  553      dirs_for_shadow = package_dirs(dpaths)
  554  
  555      rows, unassigned, ambiguous = [], [], []
  556      injected = list(args.inject_path or [])
  557      for tree, paths, lines, forkset, uponly, lf, lu, root in (
  558              ("distribution", dpaths + injected, dlines, fork, up_only, d_last_fork, d_last_up, dist),
  559              ("es", epaths, elines, efork, eup_only, e_last_fork, e_last_up, es)):
  560          for path in paths:
  561              hits = assign(compiled, tree, path)
  562              if not hits:
  563                  unassigned.append((tree, path))
  564              elif len(hits) > 1:
  565                  ambiguous.append((tree, path, hits))
  566              area = hits[0] if len(hits) == 1 else None
  567              vendor = tree == "distribution" and is_vendor(path)
  568              fork_own = path in forkset
  569              tier = "vendor-carried" if vendor else ("fork-own" if fork_own else "upstream-carried")
  570              note = "fork-written" if vendor and fork_own else None
  571              if tree == "es":
  572                  rs, rb, bb = split_reach(es_configs)
  573              else:
  574                  cfgs = reach.get(path)
  575                  if cfgs is None:
  576                      rs, rb, bb = "n/a", [], []
  577                  else:
  578                      rs, rb, bb = split_reach(cfgs)
  579              sh = None
  580              if tree == "distribution" and rs == "unreached":
  581                  own = owning_dir(path, dirs_for_shadow)
  582                  sh = shadow.get(own) if own else None
  583              rows.append([tree, path, area, tier, note, bool(fork_own and path in uponly),
  584                           language(root, path), lines.get(path), None, lf.get(path), lu.get(path),
  585                           rs, rb, bb, sh])
  586  
  587      # patches per package.mk: count of *.patch under its own directory
  588      patch_paths = [r[1] for r in rows if r[0] == "distribution" and r[1].endswith(".patch")
  589                     and (r[1].startswith("packages/") or r[1].startswith("projects/"))]
  590      pkgdirs = package_dirs(dpaths)
  591      per_dir = Counter()
  592      for p in patch_paths:
  593          own = owning_dir(p, pkgdirs)
  594          if own:
  595              per_dir[own] += 1
  596      for r in rows:
  597          if r[0] == "distribution" and r[1].endswith("/package.mk"):
  598              r[8] = per_dir.get(r[1][:-len("/package.mk")], 0)
  599  
  600      found = 0
  601      for base in ("packages", "projects"):
  602          for dp, _dn, fn in os.walk(os.path.join(dist, base)):
  603              found += sum(1 for n in fn if n.endswith(".patch"))
  604  
  605      header = {
  606          "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
  607          "generator": "tools/renovation-inventory",
  608          "distribution": {"head": head, "upstream": upstream, "upstream_head": git(dist, "rev-parse", upstream).strip(),
  609                           "merge_base": mb},
  610          "es": {"head": es_head, "upstream": es_up, "upstream_head": git(es, "rev-parse", es_up).strip(),
  611                 "merge_base": emb, "batocera_master": git(es, "rev-parse", "batocera/master").strip()},
  612          "configs": [{k: v for k, v in p.items() if k != "packages"} | ({"packages": len(p["packages"])} if "packages" in p else {})
  613                      for p in plans],
  614          "shipped_devices": list(SHIPPED),
  615          "test_devices": list(TEST),
  616          "plan_runner": {"mode": args.runner, "image": runner.image},
  617          "seconds": {"git": round(t_git, 1), "plans": round(t_plans, 1)},
  618      }
  619      counts = {"paths": (len(dpaths) + len(injected), d_index), "es-paths": (len(epaths), e_index),
  620                "patches": (len(patch_paths), found), "unassigned": len(unassigned), "ambiguous": len(ambiguous)}
  621      return header, rows, counts, unassigned, ambiguous
  622  
  623  
  624  def secret_patterns(dist):
  625      """The pre-commit and push guards' own credential patterns (.githooks/secret-patterns)."""
  626      r = subprocess.run(["bash", "-c", '. .githooks/secret-patterns && printf %s "$SECRET_PATTERNS"'],
  627                         cwd=dist, capture_output=True, text=True)
  628      if r.returncode != 0 or not r.stdout:
  629          raise CannotRun("cannot read .githooks/secret-patterns")
  630      return re.compile(r.stdout)
  631  
  632  
  633  def json_rows(rows, guard):
  634      """One JSON line per row. A tracked path whose name happens to match a credential
  635      pattern (a kernel patch "ma-sk-..." name read as an API key) is written with its
  636      hyphens as \\u002d: decoded, the path is byte-identical; at rest, no guard misreads a
  637      file name as a secret. A line that still matches fails the run."""
  638      out, escaped = [], []
  639      for r in sorted(rows, key=lambda r: (r[0], r[1])):
  640          line = json.dumps(r, separators=(",", ":"))
  641          if guard.search(line):
  642              line = line.replace("-", "\\u002d")
  643              if guard.search(line) or json.loads(line) != r:
  644                  raise CannotRun("row %s:%s matches a credential pattern even escaped" % (r[0], r[1]))
  645              escaped.append("%s:%s" % (r[0], r[1]))
  646          out.append(line)
  647      return out, escaped
  648  
  649  
  650  def write_json(path, header, lines, guard):
  651      head = json.dumps(header, sort_keys=True)
  652      if guard.search(head):  # escaped_rows names those paths too
  653          head = head.replace("-", "\\u002d")
  654          if guard.search(head) or json.loads(head) != json.loads(json.dumps(header)):
  655              raise CannotRun("the header matches a credential pattern even escaped")
  656      with open(path, "w") as f:
  657          f.write('{"header": %s,\n "columns": %s,\n "rows": [\n' % (head, json.dumps(COLUMNS)))
  658          f.write(",\n".join(lines))
  659          f.write("\n]}\n")
  660  
  661  
  662  def unit_of(row):
  663      tree, path = row[0], row[1]
  664      if tree == "es":
  665          return "es:" + "/".join(path.split("/")[:2])
  666      parts = path.split("/")
  667      if parts[0] == "projects" and len(parts) > 2 and parts[1] != "ROCKNIX":
  668          return "/".join(parts[:2])
  669      if path.endswith(".patch"):
  670          return path.rsplit("/", 1)[0]
  671      return None
  672  
  673  
  674  CODE = {"shell", "python", "recipe", "c", "c++", "c-header", "c++-header", "javascript", "typescript", "make",
  675          "cmake", "systemd", "udev", "script", "perl", "lua", "rust", "go", "assembly", "shader", "docker",
  676          "kconfig", "html", "css"}
  677  
  678  
  679  def read_unit(row, pkg_unit):
  680      """The unit a slice is cut from: a package directory, a device, a tool, an ES source directory."""
  681      tree, path = row[0], row[1]
  682      parts = path.split("/")
  683      if tree == "es":
  684          return "es:" + "/".join(parts[:3]) if len(parts) > 3 else "es:" + path
  685      if parts[0] in ("packages", "projects"):
  686          if parts[0] == "projects" and len(parts) > 1 and parts[1] != "ROCKNIX":
  687              return "/".join(parts[:2])
  688          if len(parts) > 3 and parts[2] == "devices" and not pkg_unit.get(path):
  689              return "/".join(parts[:4])
  690          return pkg_unit.get(path) or "/".join(parts[:-1])
  691      if parts[0] in ("tools", "scripts", ".github", ".claude", "docs", "config", "distributions", "research"):
  692          return "/".join(parts[:2]) if len(parts) > 2 else path
  693      return path
  694  
  695  
  696  def write_markdown(path, header, rows, counts, pkg_unit):
  697      fmt = lambda n: "{:,}".format(n)
  698      areas = defaultdict(lambda: Counter())
  699      for r in rows:
  700          a = r[2] or "(unassigned)"
  701          c = areas[a]
  702          c["paths"] += 1
  703          ln = r[7] or 0
  704          c["lines"] += ln
  705          c["lines:" + r[3]] += ln
  706          if r[7] is None:
  707              c["binaries"] += 1
  708          if r[1].endswith(".patch") and r[0] == "distribution":
  709              c["patches"] += 1
  710          c["reach:" + r[11]] += 1
  711          c["reachlines:" + r[11]] += ln
  712          if r[5]:
  713              c["overlap"] += 1
  714      out = []
  715      w = out.append
  716      w("# Renovation inventory: the summary")
  717      w("")
  718      w("Generated by `tools/renovation-inventory` at %s; never hand-edited (a hand edit is a bug in the "
  719        "generator). The full table is `docs/reviews/inventory.json`, one row per tracked path." % header["generated"])
  720      w("")
  721      d, e = header["distribution"], header["es"]
  722      w("| Tree | HEAD | Upstream | Merge base |")
  723      w("| --- | --- | --- | --- |")
  724      w("| distribution | `%s` | `%s` at `%s` | `%s` |" % (d["head"][:10], d["upstream"], d["upstream_head"][:10], d["merge_base"][:10]))
  725      w("| EmulationStation | `%s` | `%s` at `%s` (batocera/master `%s`) | `%s` |" % (
  726          e["head"][:10], e["upstream"], e["upstream_head"][:10], e["batocera_master"][:10], e["merge_base"][:10]))
  727      w("")
  728      w("The tool's own checks, as printed:")
  729      w("")
  730      w("```")
  731      for k in ("paths", "es-paths"):
  732          w("%s: %d (git ls-files: %d)" % (k, *counts[k]))
  733      w("patches: %d (find: %d)" % counts["patches"])
  734      w("unassigned: %d" % counts["unassigned"])
  735      w("ambiguous: %d" % counts["ambiguous"])
  736      w("```")
  737      w("")
  738      w("## Per area")
  739      w("")
  740      w("Lines are file lines including blanks (git's numstat against the empty tree); a binary has none. "
  741        "`shipped`, `test`, `unshipped`, `unreached` and `n/a` count paths; their lines are in the sets below. *Overlap* counts fork-own paths "
  742        "that upstream also changed since the merge base (each still belongs to one area). *Patches* counts `*.patch` "
  743        "files wherever they sit; the `patches:` check above compares those under `packages/` and `projects/` with "
  744        "`find packages projects -name '*.patch'`, so the records' and doctrine's patches are outside it.")
  745      w("")
  746      w("| Area | Paths | Lines | fork-own | upstream-carried | vendor-carried | Patches | Binaries | shipped | test | unshipped | unreached | n/a | Overlap |")
  747      w("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
  748      tot = Counter()
  749      for a in sorted(areas):
  750          c = areas[a]
  751          tot.update(c)
  752          w("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
  753              a, fmt(c["paths"]), fmt(c["lines"]), fmt(c["lines:fork-own"]), fmt(c["lines:upstream-carried"]),
  754              fmt(c["lines:vendor-carried"]), fmt(c["patches"]), fmt(c["binaries"]), fmt(c["reach:shipped"]),
  755              fmt(c["reach:test"]), fmt(c["reach:unshipped"]), fmt(c["reach:unreached"]), fmt(c["reach:n/a"]), fmt(c["overlap"])))
  756      w("| **total** | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
  757          fmt(tot["paths"]), fmt(tot["lines"]), fmt(tot["lines:fork-own"]), fmt(tot["lines:upstream-carried"]),
  758          fmt(tot["lines:vendor-carried"]), fmt(tot["patches"]), fmt(tot["binaries"]), fmt(tot["reach:shipped"]),
  759          fmt(tot["reach:test"]), fmt(tot["reach:unshipped"]), fmt(tot["reach:unreached"]), fmt(tot["reach:n/a"]), fmt(tot["overlap"])))
  760      w("")
  761      w("## Read size per area")
  762      w("")
  763      w("What a slice reads line by line is code (`%s`); configuration, data, translations and Markdown are "
  764        "read where a slice's questions need them. *Reached* is `shipped`, `test` or `n/a`; vendor-carried lines are the "
  765        "provenance table's, never read." % "`, `".join(sorted(CODE)))
  766      w("")
  767      w("| Area | Code, fork-own | Code, upstream-carried, reached | Code, unshipped | Code, unreached | Other text | Vendor-carried |")
  768      w("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
  769      rs = defaultdict(Counter)
  770      for r in rows:
  771          c, ln = rs[r[2] or "(unassigned)"], r[7] or 0
  772          if r[3] == "vendor-carried":
  773              c["vendor"] += ln
  774          elif r[6] not in CODE:
  775              c["other"] += ln
  776          elif r[11] == "unreached":
  777              c["unreached"] += ln
  778          elif r[11] == "unshipped":
  779              c["unshipped"] += ln
  780          elif r[3] == "fork-own":
  781              c["fork"] += ln
  782          else:
  783              c["up"] += ln
  784      for a in sorted(rs):
  785          c = rs[a]
  786          w("| %s | %s | %s | %s | %s | %s | %s |" % (a, fmt(c["fork"]), fmt(c["up"]), fmt(c["unshipped"]),
  787                                                     fmt(c["unreached"]), fmt(c["other"]), fmt(c["vendor"])))
  788      w("")
  789      w("## Largest units per area (code lines)")
  790      w("")
  791      w("A unit is a package directory, a device directory, a tool or script, another project, or an "
  792        "EmulationStation source directory (`es:` and its first three path parts). Fifteen per area by code lines; "
  793        "the records area is not read and is left out.")
  794      units = defaultdict(lambda: defaultdict(Counter))
  795      for r in rows:
  796          if r[2] == "records":
  797              continue
  798          u = units[r[2] or "(unassigned)"][read_unit(r, pkg_unit)]
  799          u["paths"] += 1
  800          u["lines"] += r[7] or 0
  801          if r[6] in CODE and r[3] != "vendor-carried":
  802              u["code"] += r[7] or 0
  803              if r[3] == "fork-own":
  804                  u["fork"] += r[7] or 0
  805          u["reach:" + r[11]] += 1
  806      for a in sorted(units):
  807          items = sorted(units[a].items(), key=lambda kv: (-kv[1]["code"], -kv[1]["lines"], kv[0]))
  808          w("")
  809          w("### %s (%s units)" % (a, fmt(len(items))))
  810          w("")
  811          w("| Unit | Paths | Lines | Code | of which fork-own | Reach |")
  812          w("| --- | ---: | ---: | ---: | ---: | --- |")
  813          for k, c in items[:15]:
  814              reach = ", ".join("%s %d" % (x.split(":", 1)[1], n) for x, n in sorted(c.items()) if x.startswith("reach:"))
  815              w("| `%s` | %s | %s | %s | %s | %s |" % (k, fmt(c["paths"]), fmt(c["lines"]), fmt(c["code"]), fmt(c["fork"]), reach))
  816          rest = items[15:]
  817          if rest:
  818              w("| (%d more) | %s | %s | %s | %s | |" % (len(rest), fmt(sum(c["paths"] for _, c in rest)),
  819                                                       fmt(sum(c["lines"] for _, c in rest)),
  820                                                       fmt(sum(c["code"] for _, c in rest)), fmt(sum(c["fork"] for _, c in rest))))
  821      w("")
  822      w("## Languages per area (lines)")
  823      w("")
  824      lang = defaultdict(Counter)
  825      for r in rows:
  826          lang[r[2] or "(unassigned)"][r[6]] += r[7] or 0
  827      w("| Area | Largest five |")
  828      w("| --- | --- |")
  829      for a in sorted(lang):
  830          w("| %s | %s |" % (a, ", ".join("%s %s" % (k, fmt(v)) for k, v in lang[a].most_common(5))))
  831      w("")
  832      w("## The plans")
  833      w("")
  834      w("| Config | Root | Plan lines | Packages sourced | Unsourced | Note |")
  835      w("| --- | --- | ---: | ---: | ---: | --- |")
  836      for c in header["configs"]:
  837          if c.get("skipped"):
  838              w("| %s | -- | -- | -- | -- | skipped: %s |" % (c["config"], c["skipped"]))
  839          else:
  840              w("| %s | `%s` | %d | %d | %d | %s |" % (c["config"], c["root"], c["plan_lines"], c["packages"],
  841                                                    len(c["unsourced"]), "shipped" if c["device"] in SHIPPED else "test image" if c["device"] in TEST else ""))
  842      for label, key in (("unreached", "unreached"), ("unshipped", "unshipped")):
  843          units = defaultdict(lambda: [0, 0, set(), set()])
  844          for r in rows:
  845              if r[11] != key:
  846                  continue
  847              u = unit_of(r) or pkg_unit.get(r[1]) or r[1].rsplit("/", 1)[0]
  848              units[u][0] += 1
  849              units[u][1] += r[7] or 0
  850              units[u][2].add(r[2])
  851              if len(r) > 14 and r[14]:
  852                  units[u][3].add(r[14])
  853          w("")
  854          w("## The %s set (%s paths, %s lines, %s units)" % (
  855              label, fmt(sum(v[0] for v in units.values())), fmt(sum(v[1] for v in units.values())), fmt(len(units))))
  856          w("")
  857          if key == "unreached":
  858              w("A package or project path no plan reaches. A patch is listed by its directory, which `scripts/unpack` "
  859                "never selects for any plan; a package by its directory; another project by its name. **A unit with a "
  860                "*Shadowed by* entry is a copy of a package that is built**: every plan resolves that name to the override "
  861                "named, so this copy's files are unused, and the package itself must not be removed (a duplicate's "
  862                "removal, `engineering-practices.md` § Before deleting a duplicate).")
  863          else:
  864              w("Reached only by devices the fork neither ships nor tests on (D-WORKFLOW-185: it ships %s; %s is the "
  865                "test image)." % (" and ".join(SHIPPED), ", ".join(TEST)))
  866          w("")
  867          w("| Unit | Area | Paths | Lines | Shadowed by (the package is built from) |")
  868          w("| --- | --- | ---: | ---: | --- |")
  869          for u, (n, ln, a, sh) in sorted(units.items(), key=lambda kv: (-kv[1][1], kv[0])):
  870              w("| `%s` | %s | %s | %s | %s |" % (u, ", ".join(sorted(x or "(unassigned)" for x in a)), fmt(n), fmt(ln),
  871                                               ", ".join("`%s`" % x for x in sorted(sh)) or "--"))
  872      with open(path, "w") as f:
  873          f.write("\n".join(out) + "\n")
  874  
  875  
  876  SECURITY_TOKENS = [  # brief § 4: the security lens's token grep
  877      ("password", re.compile(r"password", re.I)), ("token", re.compile(r"token", re.I)),
  878      ("secret", re.compile(r"secret", re.I)), ("key=", re.compile(r"key=")),
  879      ("rclone.conf", re.compile(r"rclone\.conf")), ("curl", re.compile(r"\bcurl\b")),
  880      ("wget", re.compile(r"\bwget\b")), ("tar x", re.compile(r"\btar\s+-?[a-zA-Z]*x")),
  881      ("unzip", re.compile(r"\bunzip\b")), ("chmod", re.compile(r"\bchmod\b")),
  882      ("sudo", re.compile(r"\bsudo\b")), ("systemctl", re.compile(r"\bsystemctl\b")),
  883      ("nc -l", re.compile(r"\bnc\s+-[a-zA-Z]*l")), ("http.server", re.compile(r"http\.server")),
  884      ("/dev/", re.compile(r"/dev/")),
  885  ]
  886  STOP_IDS = {"package", "Makefile", "CMakeLists", "config", "options", "install", "sources", "common", "default",
  887              "README", "utils", "index", "update", "settings", "system", "service", "scripts", "patches", "start",
  888              "script", "linux", "files", "modules", "launch", "functions", "global", "device", "devices", "build",
  889              "image", "tools", "network", "storage", "release", "version", "source", "systemd", "target", "plugins",
  890              "drivers", "firmware", "manual", "platform", "helper", "license", "LICENSE", "CHANGELOG", "debian",
  891              "Config", "include", "support", "android", "windows", "assets", "bootloader", "filesystem", "testing",
  892              # names too common to be an edge (pass 4's first matrix): ES and recipe file names, the project's name
  893              "CMakeLists.txt", "export", "format", "memory", "assert", "extract", "unpack", "generate", "banner",
  894              "services", "resources", "volume", "dialog", "toolchain", "achievements", "pixelelated", "wordmark",
  895              "headphones", "emulators", "EmulationStation", "RetroAchievements"}
  896  
  897  
  898  def gh_json(args):
  899      r = subprocess.run(["gh", *args, "--repo", "pixelelated/distribution"], capture_output=True, text=True)
  900      if r.returncode != 0:
  901          raise CannotRun("gh %s: %s" % (" ".join(args[:3]), r.stderr.strip()[:200]))
  902      return json.loads(r.stdout)
  903  
  904  
  905  def commits_by_path(repo, since):
  906      """{path: set(commit)} from one git log pass."""
  907      out = git(repo, "log", "--no-renames", "--since=" + since, "--format=%x01%H", "--name-only", "HEAD")
  908      touched, cur = defaultdict(set), None
  909      for line in out.split("\n"):
  910          if line.startswith("\x01"):
  911              cur = line[1:]
  912          elif line and cur:
  913              touched[line].add(cur)
  914      return touched
  915  
  916  
  917  def numstat_by_path(repo, base):
  918      """{path: (insertions, deletions)} from one git diff pass; binaries count 0."""
  919      res = {}
  920      for rec in zsplit(git(repo, "diff", "--numstat", "-z", "--no-renames", base, "HEAD")):
  921          a, d, path = rec.split("\t", 2)
  922          res[path] = (int(a) if a != "-" else 0, int(d) if d != "-" else 0)
  923      return res
  924  
  925  
  926  def assess(args):
  927      """docs/reviews/assessment.md: the six ordering lenses' evidence per area (plan § 6a, brief § 4)."""
  928      dist, es = os.path.realpath(args.distribution), os.path.realpath(args.es)
  929      with open(os.path.join(dist, args.out)) as f:
  930          inv = json.load(f)
  931      cols = inv["columns"]
  932      rows = [dict(zip(cols, r)) for r in inv["rows"]]
  933      mb, emb = inv["header"]["distribution"]["merge_base"], inv["header"]["es"]["merge_base"]
  934      pkgdirs = package_dirs([r["path"] for r in rows if r["tree"] == "distribution"])
  935      pkg_unit = {r["path"]: owning_dir(r["path"], pkgdirs) for r in rows if r["tree"] == "distribution"}
  936      with open(os.path.join(dist, "docs/blindspot-register.md")) as f:
  937          reg = f.read()
  938      blind = [(m.group(1), m.group(0)) for m in re.finditer(r"(?m)^\| (\d+) \|.*$", reg)]
  939      for m in re.finditer(r"(?ms)^## (\d+)\. .*?(?=^## \d+\. |\Z)", reg):
  940          blind.append((m.group(1), m.group(0)))
  941      with open(os.path.join(dist, "docs/friction-log.md")) as f:
  942          friction = [l for l in f if l.startswith("- 20")]
  943      bugs = gh_json(["issue", "list", "--label", "bug", "--state", "closed", "--limit", "500", "--json", "number,title,body"])
  944      opens = gh_json(["issue", "list", "--state", "open", "--limit", "300", "--json", "number,title,body"])
  945      if len(bugs) >= 500 or len(opens) >= 300:
  946          raise CannotRun("an issue list reached its --limit; raise it")
  947      named = {n: next((i for i in opens if i["number"] == n), None) for n in (336, 576, 509, 585)}
  948      scratch = tempfile.mkdtemp(prefix="renovation-assess-")
  949      out = []
  950      touched = {"distribution": commits_by_path(dist, "2026-06-01"), "es": commits_by_path(es, "2026-06-01")}
  951      numstat = {"distribution": numstat_by_path(dist, mb), "es": numstat_by_path(es, emb)}
  952      try:
  953          for area in sorted({r["area"] for r in rows}):
  954              if area == "records":  # brief § 2: inventoried, never read for content, so not scored
  955                  continue
  956              ar = [r for r in rows if r["area"] == area]
  957              code = [r for r in ar if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached"]
  958              ids = set()
  959              for r in code:
  960                  leaf = read_unit([r["tree"], r["path"]], pkg_unit).rsplit("/", 1)[-1]
  961                  stem = r["path"].rsplit("/", 1)[-1].split(".")[0]
  962                  for x in (leaf, stem):
  963                      if len(x) >= 6 and x not in STOP_IDS and re.match(r"[A-Za-z][\w.-]*\Z", x):
  964                          ids.add(x)
  965              idre = re.compile(r"(?<![\w-])(?:%s)(?![\w-])" % "|".join(re.escape(i) for i in sorted(ids, key=len, reverse=True))) if ids else None
  966              hit = lambda t: bool(idre and idre.search(t))
  967              sec = Counter()
  968              secfiles = set()
  969              for r in code:
  970                  root = es if r["tree"] == "es" else dist
  971                  try:
  972                      with open(os.path.join(root, r["path"]), errors="replace") as f:
  973                          text = f.read()
  974                  except OSError:
  975                      continue
  976                  for name, rx in SECURITY_TOKENS:
  977                      if rx.search(text):
  978                          sec[name] += 1
  979                          secfiles.add(r["path"])
  980              dpaths = [r["path"] for r in ar if r["tree"] == "distribution"]
  981              commits, stat = set(), Counter()
  982              for r in ar:
  983                  commits |= {(r["tree"], c) for c in touched[r["tree"]].get(r["path"], ())}
  984                  ins, dels = numstat[r["tree"]].get(r["path"], (0, 0))
  985                  stat["insertion"] += ins
  986                  stat["deletion"] += dels
  987              churn = len(commits)
  988              top = sorted(Counter(read_unit([r["tree"], r["path"]], pkg_unit) for r in code).items(),
  989                           key=lambda kv: -sum(x["lines"] or 0 for x in code if read_unit([x["tree"], x["path"]], pkg_unit) == kv[0]))[:10]
  990              callers = 0
  991              names = [u.rsplit("/", 1)[-1] for u, _ in top if len(u.rsplit("/", 1)[-1]) >= 5]
  992              if names:
  993                  g = subprocess.run(["git", "-C", dist, "grep", "-l", "-F", *sum((["-e", n] for n in names), []),
  994                                      "--", "packages", "projects", "scripts", "tools", "config"], capture_output=True, text=True)
  995                  if g.returncode not in (0, 1):
  996                      raise CannotRun("git grep for callers failed")
  997                  inarea = set(dpaths)
  998                  callers = sum(1 for l in g.stdout.splitlines() if l not in inarea)
  999              readlines = sum(r["lines"] or 0 for r in code)
 1000              out.append({
 1001                  "area": area, "paths": len(ar), "code_files": len(code), "read_lines": readlines,
 1002                  "security_files": len(secfiles), "security_tokens": dict(sec),
 1003                  "blindspots": sorted({n for n, t in blind if hit(t)}, key=int),
 1004                  "friction": sum(1 for l in friction if hit(l)),
 1005                  "bugs_closed": [i["number"] for i in bugs if hit((i["title"] or "") + "\n" + (i["body"] or ""))],
 1006                  "churn_since_2026_06_01": churn,
 1007                  "since_merge_base": "+%d -%d" % (stat["insertion"], stat["deletion"]),
 1008                  "open_issues": [i["number"] for i in opens if hit((i["title"] or "") + "\n" + (i["body"] or ""))],
 1009                  "named_planned": [n for n, i in named.items() if i and hit((i["title"] or "") + "\n" + (i["body"] or ""))],
 1010                  "callers_of_top_units": callers, "top_units": [u for u, _ in top[:5]],
 1011                  "unreached_paths": sum(1 for r in ar if r["reach"] == "unreached"),
 1012                  "unreached_lines": sum(r["lines"] or 0 for r in ar if r["reach"] == "unreached"),
 1013                  "unshipped_paths": sum(1 for r in ar if r["reach"] == "unshipped"),
 1014                  "unshipped_lines": sum(r["lines"] or 0 for r in ar if r["reach"] == "unshipped"),
 1015                  "identifiers": len(ids),
 1016              })
 1017      finally:
 1018          shutil.rmtree(scratch, ignore_errors=True)
 1019      fmt = lambda n: "{:,}".format(n)
 1020      w = []
 1021      w.append("# Renovation assessment: the six lenses' evidence per area")
 1022      w.append("")
 1023      w.append("Generated by `tools/renovation-inventory --assess` from `inventory.json` (distribution `%s`, ES `%s`) "
 1024               "and the tracker at %s; never hand-edited. Pass 3 of the survey scores each area from these numbers "
 1025               "(`p1-tracking.md`); a slice read confirms or overturns a score." % (
 1026                   inv["header"]["distribution"]["head"][:10], inv["header"]["es"]["head"][:10],
 1027                   time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
 1028      w.append("")
 1029      w.append("How each column is produced. Over the area's **code files** (code languages, not vendor-carried, not "
 1030               "unreached): *security* is the number of files matching any of the brief's tokens (%s); the area's "
 1031               "**identifiers** are its units' and code files' names (six characters or more, generic names excluded), "
 1032               "and *blindspots*, *friction*, *closed bugs* and *open issues* count the register entries, friction lines "
 1033               "and issues (`gh issue list --repo pixelelated/distribution`, closed `bug` limit 500 returned %d, open "
 1034               "limit 300 returned %d) naming one of them as a whole word -- a search, so a lead; *churn* is the commits since 2026-06-01 (`git log --since=2026-06-01 "
 1035               "--name-only HEAD`, one pass per tree) touching one of the area's paths; *since base* sums `git diff "
 1036               "--numstat <merge base> HEAD` over them; *callers* counts files outside the area under packages, projects, scripts, "
 1037               "tools and config naming one of its ten largest units." % (
 1038                   ", ".join("`%s`" % n for n, _ in SECURITY_TOKENS), len(bugs), len(opens)))
 1039      w.append("")
 1040      w.append("| Area | Read lines | Security files | Blindspots | Friction | Closed bugs | Churn | Since base | Open issues | #336/#576/#509/#585 | Callers | Unreached | Unshipped |")
 1041      w.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | --- | --- |")
 1042      for a in out:
 1043          w.append("| %s | %s | %d of %d | %d | %d | %d | %d | %s | %d | %s | %d | %s paths, %s lines | %s paths, %s lines |" % (
 1044              a["area"], fmt(a["read_lines"]), a["security_files"], a["code_files"], len(a["blindspots"]), a["friction"],
 1045              len(a["bugs_closed"]), a["churn_since_2026_06_01"], a["since_merge_base"], len(a["open_issues"]),
 1046              ", ".join("#%d" % n for n in a["named_planned"]) or "--", a["callers_of_top_units"],
 1047              fmt(a["unreached_paths"]), fmt(a["unreached_lines"]), fmt(a["unshipped_paths"]), fmt(a["unshipped_lines"])))
 1048      w.append("| records | not assessed: inventoried and never read for content (brief § 2) | | | | | | | | | | | |")
 1049      for a in out:
 1050          w.append("")
 1051          w.append("## %s" % a["area"])
 1052          w.append("")
 1053          w.append("- Identifiers searched: %d; largest units: %s" % (a["identifiers"], ", ".join("`%s`" % u for u in a["top_units"]) or "--"))
 1054          w.append("- Security tokens (files): %s" % (", ".join("`%s` %d" % kv for kv in sorted(a["security_tokens"].items(), key=lambda kv: -kv[1])) or "none"))
 1055          w.append("- Blindspot entries: %s" % (", ".join(a["blindspots"]) or "none"))
 1056          w.append("- Closed bugs: %s" % (", ".join("#%d" % n for n in a["bugs_closed"]) or "none"))
 1057          w.append("- Open issues: %s" % (", ".join("#%d" % n for n in a["open_issues"]) or "none"))
 1058      path = os.path.join(dist, "docs/reviews/assessment.md")
 1059      with open(path, "w") as f:
 1060          f.write("\n".join(w) + "\n")
 1061      print("wrote docs/reviews/assessment.md (%d areas; closed bugs %d, open issues %d, friction lines %d, blindspot entries %d)" % (
 1062          len(out), len(bugs), len(opens), len(friction), len(blind)))
 1063      return 0
 1064  
 1065  
 1066  SHARED_STATE = [  # pass 4: state several areas may read or write (from the product's /storage paths and setting calls)
 1067      ("system.cfg / get_setting / set_setting", re.compile(r"system\.cfg|\b[gs]et_setting\b|SystemConf::")),
 1068      ("es_settings.cfg", re.compile(r"es_settings\.cfg|Settings::getInstance")),
 1069      ("cloud_sync.conf and its rules", re.compile(r"cloud_sync\.conf|cloud_sync-rules\.txt")),
 1070      ("cloud sync stamps and lock", re.compile(r"\.cache/cloud_sync|cloud_sync\.lock|last-sync-")),
 1071      ("rclone.conf", re.compile(r"rclone\.conf")),
 1072      ("retroarch.cfg and core options", re.compile(r"retroarch\.cfg|retroarch-core-options")),
 1073      ("raofflineproxy state", re.compile(r"\.config/raofflineproxy|raofflineproxy")),
 1074      ("backuptool.conf and settings archives", re.compile(r"backuptool\.conf|backuptool\b")),
 1075      ("/storage/.cache/services", re.compile(r"\.cache/services")),
 1076      ("the game-end and game-start hooks", re.compile(r"game-end|game-start|fireEvent")),
 1077      ("/storage/.cache/log and evidence", re.compile(r"\.cache/log|rocknix-evidence")),
 1078  ]
 1079  
 1080  
 1081  def area_texts(rows, dist, es, pkg_unit):
 1082      """{area: [(path, text)]} over reached, non-vendor code files; {area: identifiers}."""
 1083      texts, ids = defaultdict(list), defaultdict(set)
 1084      for r in rows:
 1085          if r["area"] == "records" or r["language"] not in CODE or r["tier"] == "vendor-carried" or r["reach"] == "unreached":
 1086              continue
 1087          root = es if r["tree"] == "es" else dist
 1088          try:
 1089              with open(os.path.join(root, r["path"]), errors="replace") as f:
 1090                  texts[r["area"]].append((r["path"], f.read()))
 1091          except OSError:
 1092              continue
 1093          leaf = read_unit([r["tree"], r["path"]], pkg_unit).rsplit("/", 1)[-1]
 1094          stem = r["path"].rsplit("/", 1)[-1].split(".")[0]
 1095          for x in (leaf, stem):
 1096              if len(x) >= 6 and x not in STOP_IDS and re.match(r"[A-Za-z][\w.-]*\Z", x):
 1097                  ids[r["area"]].add(x)
 1098      return texts, ids
 1099  
 1100  
 1101  def cross(args):
 1102      """docs/reviews/cross-reference.md: every area against every other (pass 4)."""
 1103      dist, es = os.path.realpath(args.distribution), os.path.realpath(args.es)
 1104      with open(os.path.join(dist, args.out)) as f:
 1105          inv = json.load(f)
 1106      rows = [dict(zip(inv["columns"], r)) for r in inv["rows"]]
 1107      pkgdirs = package_dirs([r["path"] for r in rows if r["tree"] == "distribution"])
 1108      pkg_unit = {r["path"]: owning_dir(r["path"], pkgdirs) for r in rows if r["tree"] == "distribution"}
 1109      texts, ids = area_texts(rows, dist, es, pkg_unit)
 1110      areas = sorted(texts)
 1111      owner = defaultdict(set)
 1112      for a in areas:
 1113          for i in ids[a]:
 1114              owner[i].add(a)
 1115      own = {a: {i for i in ids[a] if owner[i] == {a}} for a in areas}  # an identifier two areas share proves no edge
 1116      rx = {a: re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(i) for i in sorted(own[a], key=len, reverse=True)))
 1117            for a in areas if own[a]}
 1118      matrix, evidence = {}, {}
 1119      for a in areas:
 1120          for b in areas:
 1121              if a == b or b not in rx:
 1122                  continue
 1123              files, names = 0, Counter()
 1124              for path, text in texts[a]:
 1125                  found = set(rx[b].findall(text))
 1126                  if found:
 1127                      files += 1
 1128                      names.update(found)
 1129              matrix[(a, b)] = files
 1130              evidence[(a, b)] = [n for n, _ in names.most_common(3)]
 1131      # doctrine -> area: each rule's paths: globs resolved against the inventory (no paths: = every area)
 1132      area_of = {(r["tree"], r["path"]): r["area"] for r in rows}
 1133      rule_edges = Counter()
 1134      rules_dir = os.path.join(dist, ".claude/rules")
 1135      for fn in sorted(os.listdir(rules_dir)):
 1136          if not fn.endswith(".md"):
 1137              continue
 1138          with open(os.path.join(rules_dir, fn)) as f:
 1139              head = f.read().split("\n---", 1)[0]
 1140          globs = re.findall(r'(?m)^\s*-\s*"([^"]+)"', head) if "paths:" in head else []
 1141          hit_areas = set()
 1142          if not globs or "**" in globs:
 1143              hit_areas = set(areas)
 1144          else:
 1145              res = [glob_re(g) for g in globs]
 1146              hit_areas = {area_of[k] for k in area_of if k[0] == "distribution" and any(x.match(k[1]) for x in res)} & set(areas)
 1147          for a in hit_areas:
 1148              rule_edges[a] += 1
 1149      # patches -> area of the package they patch
 1150      patch_edges = Counter()
 1151      pkg_area = {r["path"][:-len("/package.mk")]: r["area"] for r in rows if r["tree"] == "distribution" and r["path"].endswith("/package.mk")}
 1152      for r in rows:
 1153          if r["tree"] == "distribution" and r["area"] == "patches-and-configs":
 1154              own = owning_dir(r["path"], pkgdirs)
 1155              m = re.match(r"projects/ROCKNIX/patches/([^/]+)/", r["path"])
 1156              if own:
 1157                  patch_edges[pkg_area.get(own, "(unknown)")] += 1
 1158              elif m:  # projects/ROCKNIX/patches/<package>/: the area of that package's local or global recipe
 1159                  cand = [d for d in pkg_area if d.rsplit("/", 1)[-1] == m.group(1)]
 1160                  local = [d for d in cand if d.startswith("projects/ROCKNIX/")]
 1161                  patch_edges[pkg_area[(local or cand)[0]] if cand else "(unknown)"] += 1
 1162              else:  # a device's or another project's own patch directory, or its kernel config
 1163                  patch_edges["devices"] += 1
 1164      state = {}
 1165      for label, srx in SHARED_STATE:
 1166          state[label] = {a: sum(1 for _, t in texts[a] if srx.search(t)) for a in areas}
 1167      fmt = lambda n: "{:,}".format(n)
 1168      short = {a: a.split("-")[0] for a in areas}
 1169      w = ["# Renovation cross-reference: every area against every other", "",
 1170           "Generated by `tools/renovation-inventory --cross` from `inventory.json` (distribution `%s`, ES `%s`); never "
 1171           "hand-edited. Pass 4 of the survey draws slice boundaries from these edges (`p1-tracking.md`)." % (
 1172               inv["header"]["distribution"]["head"][:10], inv["header"]["es"]["head"][:10]), "",
 1173           "**Call edges.** A cell is the number of the row area's code files (reached, not vendor-carried) that name, "
 1174           "as a whole word, an identifier only the column area owns: its units' and code files' names, six characters "
 1175           "or more, generic names excluded, and an identifier two areas share dropped. A search, so a lead.", "",
 1176           "| from \\ to | " + " | ".join(short[b] for b in areas) + " |",
 1177           "| --- | " + " | ".join("---:" for _ in areas) + " |"]
 1178      for a in areas:
 1179          w.append("| %s | " % a + " | ".join("--" if a == b else fmt(matrix.get((a, b), 0)) for b in areas) + " |")
 1180      w += ["", "Column keys: " + ", ".join("`%s` %s" % (short[b], b) for b in areas) + ".", "",
 1181            "**The strongest edges**, each with the identifiers named most:", "",
 1182            "| From | To | Files | Named most |", "| --- | --- | ---: | --- |"]
 1183      for (a, b), n in sorted(matrix.items(), key=lambda kv: -kv[1]):
 1184          if n >= 3:
 1185              w.append("| %s | %s | %d | %s |" % (a, b, n, ", ".join("`%s`" % x for x in evidence[(a, b)])))
 1186      w += ["", "**Shared state.** Code files per area touching each piece of state several areas may read or write.", "",
 1187            "| State | " + " | ".join(short[a] for a in areas) + " |", "| --- | " + " | ".join("---:" for _ in areas) + " |"]
 1188      for label, _ in SHARED_STATE:
 1189          w.append("| %s | " % label + " | ".join(fmt(state[label][a]) or "0" for a in areas) + " |")
 1190      w += ["", "**Doctrine to area.** Rule files under `.claude/rules/` whose `paths:` globs match the area's paths "
 1191            "(a rule with no `paths:`, or `**`, governs every area):", "",
 1192            "| Area | Rules |", "| --- | ---: |"]
 1193      for a in areas:
 1194          w.append("| %s | %d |" % (a, rule_edges[a]))
 1195      w += ["", "**Patches to area.** Each `*.patch` and kernel config counted against the area of the package directory "
 1196            "it sits in:", "", "| Area of the patched package | Patches and configs |", "| --- | ---: |"]
 1197      for a, n in sorted(patch_edges.items(), key=lambda kv: -kv[1]):
 1198          w.append("| %s | %s |" % (a, fmt(n)))
 1199      w += ["", "**Areas with no edge either way:** %s" % (
 1200          ", ".join(a for a in areas if not any(matrix.get((a, b), 0) or matrix.get((b, a), 0) for b in areas if b != a)) or "none")]
 1201      with open(os.path.join(dist, "docs/reviews/cross-reference.md"), "w") as f:
 1202          f.write("\n".join(w) + "\n")
 1203      print("wrote docs/reviews/cross-reference.md (%d areas, %d directed pairs with an edge)" % (
 1204          len(areas), sum(1 for v in matrix.values() if v)))
 1205      return 0
 1206  
 1207  
 1208  ORDER_BEGIN, ORDER_END = "<!-- renovation-inventory --order: begin -->", "<!-- renovation-inventory --order: end -->"
 1209  
 1210  
 1211  def load_slices(dist, path="docs/reviews/slices.json"):
 1212      """slices.json: {"sensitive": {kind: [globs]}, "slices": [{k, id, area, title, lens, select, ...}]}.
 1213  
 1214      A row belongs to a slice when its area is in select.areas (default: the slice's area), it
 1215      matches one of select.globs (default: all; `es:` for the ES tree; `!` excludes), its reach
 1216      is in select.reach and its tier in select.tier when those are given. select may be a list,
 1217      read as a union; a `rest` selector takes only rows no other selector claims."""
 1218      with open(os.path.join(dist, path)) as f:
 1219          doc = json.load(f)
 1220      out = []
 1221      for sl in doc["slices"]:
 1222          if "gate" in sl:  # D-WORKFLOW-187: the renovation gates no release; a stale field is refused, not dropped
 1223              sys.exit("renovation-inventory: slice %s carries a release gate; D-WORKFLOW-187 retired them "
 1224                       "(a reading-order prerequisite is `read_before`)" % sl.get("id"))
 1225          sels = sl.get("select", {})
 1226          compiled = []
 1227          for sel in (sels if isinstance(sels, list) else [sels]):  # a list is a union of selectors
 1228              globs = sel.get("globs")
 1229              compiled.append((set(sel.get("areas", [sl["area"]])),
 1230                               load_areas([{"area": sl["id"], "globs": globs}])[0] if globs else None,
 1231                               set(sel["reach"]) if sel.get("reach") else None, bool(sel.get("rest")),
 1232                               set(sel["tier"]) if sel.get("tier") else None))
 1233          out.append((sl, compiled))
 1234      return doc, out
 1235  
 1236  
 1237  def slice_of(row, slices):
 1238      """The slices a row belongs to. A `rest` selector takes, within its areas, only rows no other selector claims."""
 1239      def match(areas, comp, reach, tier):
 1240          if row["area"] not in areas or (reach and row["reach"] not in reach) or (tier and row["tier"] not in tier):
 1241              return False
 1242          return not comp or bool(assign([comp], row["tree"], row["path"]))
 1243      hits = [sl["id"] for sl, sels in slices if any(not rest and match(a, c, r, t) for a, c, r, rest, t in sels)]
 1244      if hits:
 1245          return hits
 1246      return [sl["id"] for sl, sels in slices if any(rest and match(a, c, r, t) for a, c, r, rest, t in sels)]
 1247  
 1248  
 1249  def order(args):
 1250      """Size every slice from inventory.json, check the slices partition the tree, render order.md's table."""
 1251      dist = os.path.realpath(args.distribution)
 1252      with open(os.path.join(dist, args.out)) as f:
 1253          inv = json.load(f)
 1254      rows = [dict(zip(inv["columns"], r)) for r in inv["rows"]]
 1255      doc, slices = load_slices(dist)
 1256      ks = [sl["k"] for sl, _ in slices]
 1257      if ks != list(range(1, len(ks) + 1)) or len({sl["id"] for sl, _ in slices}) != len(ks):
 1258          raise CannotRun("slices must be numbered 1..N in order, with unique ids")
 1259      size = defaultdict(Counter)
 1260      paths = defaultdict(list)
 1261      unassigned, ambiguous = [], []
 1262      for r in rows:
 1263          hits = slice_of(r, slices)
 1264          if not hits:
 1265              unassigned.append(r)
 1266              continue
 1267          if len(hits) > 1:
 1268              ambiguous.append((r, hits))
 1269              continue
 1270          c = size[hits[0]]
 1271          ln = r["lines"] or 0
 1272          c["paths"] += 1
 1273          c["lines"] += ln
 1274          if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached":
 1275              c["read"] += ln
 1276              c["read:" + r["tier"]] += ln
 1277          if r["tier"] == "vendor-carried":
 1278              c["vendor"] += 1
 1279              c["vendor_lines"] += ln
 1280          c["reach:" + r["reach"]] += 1
 1281          paths[hits[0]].append(r["path"])
 1282      fmt = lambda n: "{:,}".format(n)
 1283      print("slices: %d" % len(slices))
 1284      print("rows: %d (inventory: %d)" % (sum(c["paths"] for c in size.values()), len(rows)))
 1285      print("unassigned: %d" % len(unassigned))
 1286      print("ambiguous: %d" % len(ambiguous))
 1287      for r in unassigned[:10]:
 1288          print("  unassigned %s %s:%s" % (r["area"], r["tree"], r["path"]))
 1289      for r, h in ambiguous[:10]:
 1290          print("  ambiguous %s:%s -> %s" % (r["tree"], r["path"], ", ".join(h)))
 1291      over, empty = [], []
 1292      for sl, _ in slices:
 1293          c, kind = size[sl["id"]], sl.get("kind", "read")
 1294          bound = {"read": c["read"], "currency": c["read:fork-own"], "prose": c["lines"]}.get(kind, 0)
 1295          print("%3d %-34s %-22s %6d paths %9s lines %8s read %8s fork-own %8s patch  %-8s%s" % (
 1296              sl["k"], sl["id"], sl["area"], c["paths"], fmt(c["lines"]), fmt(c["read"]), fmt(c["read:fork-own"]),
 1297              fmt(c["vendor_lines"]), kind, "  OVER 12,000" if bound > 12000 else ""))
 1298          if bound > 12000 and sl["k"] <= 3:
 1299              over.append(sl["id"])
 1300          if not c["paths"]:
 1301              empty.append(sl["id"])
 1302      for x in over:
 1303          print("  first-three slice %s reads more than 12,000 lines" % x)
 1304      for x in empty:
 1305          print("  slice %s holds no path" % x)
 1306      lines = [ORDER_BEGIN, "",
 1307               "Generated by `tools/renovation-inventory --order` from `slices.json` and `inventory.json` "
 1308               "(distribution `%s`, ES `%s`); edit `slices.json`, never this block. Every tracked path is in exactly one "
 1309               "slice: `unassigned: %d`, `ambiguous: %d` over %s rows. *Read* is code lines a slice reads line by line "
 1310               "(code languages, not vendor-carried, not unreached); a *currency* slice reads its fork-own files line by line "
 1311               "and checks the rest for reachability and currency (plan § 2), so its size is its fork-own lines; a table "
 1312               "slice reads rows, one per path, not lines; a *prose* slice (the doctrine) reads its text, so its size is its "
 1313               "lines. *Patch and config lines* are the vendor-carried files the slice "
 1314               "holds (fork-written ones are read with their code, the rest by provenance), counted apart from *Read*." % (
 1315                   inv["header"]["distribution"]["head"][:10], inv["header"]["es"]["head"][:10],
 1316                   len(unassigned), len(ambiguous), fmt(len(rows))), "",
 1317               "| k | Slice | Area | Kind | Lens | Paths | Lines | Read (fork-own) | Patch and config lines | Depth |",
 1318               "| ---: | --- | --- | --- | --- | ---: | ---: | --- | ---: | --- |"]
 1319      for sl, _ in slices:
 1320          c, kind = size[sl["id"]], sl.get("kind", "read")
 1321          lines.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
 1322              sl["k"], sl["title"], sl["area"], kind, sl["lens"], fmt(c["paths"]), fmt(c["lines"]),
 1323              "-- (%s rows)" % fmt(c["paths"]) if kind == "table" else "%s of prose" % fmt(c["lines"]) if kind == "prose"
 1324              else "%s (%s)" % (fmt(c["read"]), fmt(c["read:fork-own"])),
 1325              fmt(c["vendor_lines"]), sl["depth"]))
 1326      def describe(sl):
 1327          sels = sl.get("select", {})
 1328          parts = []
 1329          for sel in (sels if isinstance(sels, list) else [sels]):
 1330              parts.append("areas %s; globs %s%s%s" % (
 1331                  ", ".join("`%s`" % a for a in sel.get("areas", [sl["area"]])),
 1332                  ", ".join("`%s`" % g for g in sel.get("globs", ["(all)"])),
 1333                  ("; reach %s" % ", ".join("`%s`" % x for x in sel["reach"])) if sel.get("reach") else "",
 1334                  "; the rest of these areas" if sel.get("rest") else ""))
 1335          return " **plus** ".join(parts)
 1336      for sl, _ in slices:
 1337          c = size[sl["id"]]
 1338          lines += ["", "### T%d. %s: %s" % (sl["k"], sl["area"], sl["title"]), "",
 1339                    "- **id**: `%s`; **kind**: %s; **lens**: %s" % (sl["id"], sl.get("kind", "read"), sl["lens"]),
 1340                    "- **why here**: %s" % sl["why"],
 1341                    "- **paths** (%s paths, %s lines, %s read, of which %s fork-own; %s patch and config lines; reach %s): %s" % (
 1342                        fmt(c["paths"]), fmt(c["lines"]),
 1343                        "--" if sl.get("kind") == "table" else fmt(c["read"]),
 1344                        "--" if sl.get("kind") == "table" else fmt(c["read:fork-own"]), fmt(c["vendor_lines"]),
 1345                        ", ".join("%s %d" % (x.split(":", 1)[1], n) for x, n in sorted(c.items()) if x.startswith("reach:")),
 1346                        describe(sl)),
 1347                    "- **read before**: %s" % ("%s (a reading order, D-WORKFLOW-187)" % sl["read_before"] if sl.get("read_before") else "none"),
 1348                    "- **depth**: %s -- %s" % (sl["depth"], sl["depth_reason"]),
 1349                    "- **interacting subsystems** (read-only context): %s" % sl["interacting"],
 1350                    "- **closing evidence**: %s" % sl["closing"]]
 1351      lines += ["", "### The security, state-preservation and launch-path files", "",
 1352                "`tools/renovation-drift` reads these globs from `slices.json` (`sensitive`): a closed slice whose drift "
 1353                "touches one re-opens at its depth, whatever its size (plan § 8)."]
 1354      for kind, globs in doc.get("sensitive", {}).items():
 1355          n = sum(1 for r in rows if any(x.match(r["path"]) for x in load_areas([{"area": kind, "globs": globs}])[0][1].get(
 1356              "es" if r["tree"] == "es" else "distribution", [])))
 1357          lines.append("- **%s** (%d paths): %s" % (kind, n, ", ".join("`%s`" % g for g in globs)))
 1358      lines += ["", ORDER_END]
 1359      target = os.path.join(dist, "docs/reviews/order.md")
 1360      if not args.no_write:
 1361          with open(target) as f:
 1362              text = f.read()
 1363          if ORDER_BEGIN not in text or ORDER_END not in text:
 1364              raise CannotRun("order.md has no generated block markers")
 1365          a, b = text.index(ORDER_BEGIN), text.index(ORDER_END) + len(ORDER_END)
 1366          with open(target, "w") as f:
 1367              f.write(text[:a] + "\n".join(lines) + text[b:])
 1368          print("wrote the generated block of docs/reviews/order.md")
 1369      return EX_FAIL if unassigned or ambiguous or over or empty else 0
 1370  
 1371  
 1372  ISSUE_BODY = """Slice T{k} of the renovation order: `docs/reviews/order.md` § T{k}, id `{id}` in `docs/reviews/slices.json`. Phase M6.P2, under epic #339 until this area's epic is filed at its first dispatch (then re-parented and retitled `E<epic>/T{k}`, `milestone-phase-naming.md`). Proposed by the survey (#641); the order is {order_row}. Run under the per-slice procedure of `docs/reviews/plan-for-the-plan.md` § 6b, from the brief the planner writes before dispatch (§ 7).
 1373  
 1374  ## Scope
 1375  
 1376  - **Area:** {area}; **kind:** {kind}; **lens:** {lens}
 1377  - **Why here:** {why}
 1378  - **Paths:** {desc}. {paths} paths, {lines} lines; {read} lines read, {fork} of them fork-own (inventory at `{head}`). The exact list is `tools/renovation-inventory --order`'s membership of `{id}`.
 1379  - **Provenance tiers:** {tiers}
 1380  - **Read before:** {read_before}
 1381  - **Review depth:** {depth} -- {reason}
 1382  - **Interacting subsystems (read-only context):** {inter}
 1383  
 1384  reviewed-at:
 1385  fixed-at:
 1386  
 1387  {vm}
 1388  
 1389  ## Acceptance criteria
 1390  
 1391  - [ ] `docs/audits/<date>-epic-m6-{id}/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
 1392  - [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-{id}/` prints `PASS`, the renovation face included: Q1 to Q7 answered in `04-analysis.md`, and every punch item's `question:` in the index.
 1393  - [ ] {opinion}
 1394  - [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue, or withdrawn with its reason.
 1395  - [ ] `reviewed-at:` and `fixed-at:` above carry the commits the read and the fixes were made at (with `fixed-at-es:` for EmulationStation paths), and `tools/renovation-status` lists this slice as `closed`.
 1396  """
 1397  
 1398  
 1399  def slice_issues(args, out):
 1400      """Write T<k>.title and T<k>.md for every slice: the slice issues' titles and bodies (pass 7; no tracker)."""
 1401      dist = os.path.realpath(args.distribution)
 1402      os.makedirs(out, exist_ok=True)
 1403      with open(os.path.join(dist, args.out)) as f:
 1404          inv = json.load(f)
 1405      rows = [dict(zip(inv["columns"], r)) for r in inv["rows"]]
 1406      doc, slices = load_slices(dist)
 1407      size = defaultdict(Counter)
 1408      for r in rows:
 1409          h = slice_of(r, slices)
 1410          if len(h) == 1:
 1411              c = size[h[0]]
 1412              ln = r["lines"] or 0
 1413              c["paths"] += 1
 1414              c["lines"] += ln
 1415              c["tier:" + r["tier"]] += 1
 1416              if r["language"] in CODE and r["tier"] != "vendor-carried" and r["reach"] != "unreached":
 1417                  c["read"] += ln
 1418                  if r["tier"] == "fork-own":
 1419                      c["fork"] += ln
 1420      fmt = lambda n: "{:,}".format(n)
 1421      head = inv["header"]["distribution"]["head"][:10]
 1422      for sl, _ in slices:
 1423          c = size[sl["id"]]
 1424          sels = sl.get("select", {})
 1425          desc = []
 1426          for sel in (sels if isinstance(sels, list) else [sels]):
 1427              desc.append("areas %s; globs %s%s%s" % (
 1428                  ", ".join("`%s`" % a for a in sel.get("areas", [sl["area"]])),
 1429                  ", ".join("`%s`" % g for g in sel.get("globs", ["(all)"])),
 1430                  ("; reach %s" % ", ".join("`%s`" % x for x in sel["reach"])) if sel.get("reach") else "",
 1431                  "; the rest of these areas" if sel.get("rest") else ""))
 1432          kind = sl.get("kind", "read")
 1433          vm = ("Can this be done on the VM? Yes -- every behaviour claim this slice makes is proven on the GENERIC_X64 "
 1434                "guest (`vm-first.md`, `generic-x64-vm-testing.md` § headless); reading and tables need no guest."
 1435                if kind != "table" else
 1436                "Can this be done on the VM? No test is proposed: a table slice is host analysis of the tree; a removal "
 1437                "it proposes is proven on the GENERIC_X64 guest before it is a punch item.")
 1438          if sl["depth"] == "Local":
 1439              opinion = ("The review depth is recorded as Local in `second-opinions/review-plan.json` (no reviewer: the "
 1440                         "lint and the counts are the check, plan § 6c).")
 1441          elif sl["depth"] == "Independent":
 1442              opinion = ("`second-opinions/review-plan.json` records Independent depth and one reviewer from another lab, "
 1443                         "and that reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).")
 1444          else:
 1445              opinion = ("`second-opinions/review-plan.json` records Extended depth and two reviewers from two other labs, "
 1446                         "and each reviewer's provenance names its served model (plan § 6c, D-WORKFLOW-137).")
 1447          title = "M6.P2 E339/T%d: %s: %s" % (sl["k"], sl["area"], sl["title"])
 1448          body = ISSUE_BODY.format(
 1449              k=sl["k"], id=sl["id"], area=sl["area"], kind=kind, lens=sl["lens"], why=sl["why"],
 1450              desc=" **plus** ".join(desc), paths=fmt(c["paths"]), lines=fmt(c["lines"]), read=fmt(c["read"]),
 1451              fork=fmt(c["fork"]), head=head,
 1452              tiers=", ".join("%s %s" % (k.split(":", 1)[1], fmt(n)) for k, n in sorted(c.items()) if k.startswith("tier:")),
 1453              read_before=("%s (a reading order; the renovation gates no release, D-WORKFLOW-187)" % sl["read_before"]
 1454                           if sl.get("read_before") else "none (the renovation gates no release, D-WORKFLOW-187)"), depth=sl["depth"], reason=sl["depth_reason"], inter=sl["interacting"],
 1455              vm=vm, opinion=opinion, order_row=args.order_row)
 1456          with open(os.path.join(out, "T%d.title" % sl["k"]), "w") as f:
 1457              f.write(title)
 1458          with open(os.path.join(out, "T%d.md" % sl["k"]), "w") as f:
 1459              f.write(body)
 1460      print("wrote %d slice issue bodies to %s" % (len(slices), out))
 1461      return 0
 1462  
 1463  
 1464  def self_test():
 1465      """The counters can fail: a path in no area, a path in two, a catch-all refused."""
 1466      areas = [{"area": "a", "globs": ["x/**", "!x/skip/**"]}, {"area": "b", "globs": ["x/both/*", "es:**"]}]
 1467      c = load_areas(areas)
 1468      cases = [("distribution", "y/none", 0), ("distribution", "x/skip/f", 0), ("distribution", "x/both/f", 2),
 1469               ("distribution", "x/one/f", 1), ("es", "anything/at/all", 1)]
 1470      bad = 0
 1471      for tree, p, want in cases:
 1472          got = len(assign(c, tree, p))
 1473          ok = got == want
 1474          bad += not ok
 1475          print("%s %s:%s -> %d area(s), want %d" % ("PASS" if ok else "FAIL", tree, p, got, want))
 1476      try:
 1477          load_areas([{"area": "all", "globs": ["**"]}])
 1478          print("FAIL a bare ** was accepted")
 1479          bad += 1
 1480      except CannotRun:
 1481          print("PASS a bare ** is refused")
 1482      g = glob_re("scripts/{council-*,verify-*.ts,owner-queue-lint.mjs}")
 1483      for p, want in (("scripts/council-invoke.ts", True), ("scripts/verify-pins.ts", True),
 1484                      ("scripts/owner-queue-lint.mjs", True), ("scripts/build", False)):
 1485          ok = bool(g.match(p)) == want
 1486          bad += not ok
 1487          print("%s brace glob %s" % ("PASS" if ok else "FAIL", p))
 1488      g = glob_re("{packages,projects}/**/linux*.conf")
 1489      for p, want in (("projects/ROCKNIX/devices/H700/linux/linux.aarch64.conf", True),
 1490                      ("packages/linux.conf", True), ("packages/a/linuxish.txt", False)):
 1491          ok = bool(g.match(p)) == want
 1492          bad += not ok
 1493          print("%s glob %s" % ("PASS" if ok else "FAIL", p))
 1494      for cfgs, want in ((["H700-aarch64", "GENERIC_X64-x86_64", "RK3566-aarch64"], "shipped"),  # D-WORKFLOW-185
 1495                         (["GENERIC_X64-x86_64", "RK3326-aarch64"], "test"), (["RK3566-aarch64"], "unshipped"), ([], "unreached")):
 1496          ok = split_reach(cfgs)[0] == want
 1497          bad += not ok
 1498          print("%s reach %s -> %s" % ("PASS" if ok else "FAIL", ",".join(cfgs) or "(no plan)", want))
 1499      print("self-test: %s" % ("PASS" if not bad else "FAIL (%d)" % bad))
 1500      return 0 if not bad else EX_FAIL
 1501  
 1502  
 1503  def main():
 1504      ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
 1505      ap.add_argument("--distribution", default=".")
 1506      ap.add_argument("--es", default="/home/max/Development/emulationstation-next.worktrees/m6-p1-survey")
 1507      ap.add_argument("--areas", default="docs/reviews/areas.json")
 1508      ap.add_argument("--plans", help="read plan-<DEVICE>-<ARCH>.txt from here when present, write them when not")
 1509      ap.add_argument("--out", default="docs/reviews/inventory.json")
 1510      ap.add_argument("--markdown", default="docs/reviews/inventory.md")
 1511      ap.add_argument("--runner", choices=("container", "host"), default="container",
 1512                      help="where plans are computed: the Makefile's pinned build image (default), or this host, "
 1513                           "whose missing tools (xmlstarlet) silently shrink a plan")
 1514      ap.add_argument("--inject-path", action="append", help="a synthetic distribution path (the unassigned fixture)")
 1515      ap.add_argument("--no-write", action="store_true")
 1516      ap.add_argument("--self-test", action="store_true")
 1517      ap.add_argument("--assess", action="store_true", help="write docs/reviews/assessment.md from inventory.json")
 1518      ap.add_argument("--order", action="store_true", help="size the slices in slices.json, check they partition the "
 1519                      "tree, render order.md's generated block (--no-write: print only)")
 1520      ap.add_argument("--slice-issues", metavar="DIR", help="write each slice issue's title and body (T<k>.title, "
 1521                      "T<k>.md) into DIR from slices.json and inventory.json; touches no tracker")
 1522      ap.add_argument("--order-row", default="the order's register row",
 1523                      help="--slice-issues: the register row that records the order (pass it once the row exists)")
 1524      ap.add_argument("--cross", action="store_true", help="write docs/reviews/cross-reference.md from inventory.json")
 1525      args = ap.parse_args()
 1526      if args.self_test:
 1527          return self_test()
 1528      if args.slice_issues:
 1529          try:
 1530              return slice_issues(args, args.slice_issues)
 1531          except (CannotRun, OSError, ValueError, KeyError) as e:
 1532              print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1533              return EX_CANNOT
 1534      if args.order:
 1535          try:
 1536              return order(args)
 1537          except (CannotRun, OSError, ValueError, KeyError) as e:
 1538              print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1539              return EX_CANNOT
 1540      if args.cross:
 1541          try:
 1542              return cross(args)
 1543          except (CannotRun, OSError, ValueError) as e:
 1544              print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1545              return EX_CANNOT
 1546      if args.assess:
 1547          try:
 1548              return assess(args)
 1549          except (CannotRun, OSError, ValueError) as e:
 1550              print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1551              return EX_CANNOT
 1552      try:
 1553          header, rows, counts, unassigned, ambiguous = build(args)
 1554      except (CannotRun, OSError, ValueError) as e:
 1555          print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1556          return EX_CANNOT
 1557      for k in ("paths", "es-paths"):
 1558          print("%s: %d (git ls-files: %d)" % (k, *counts[k]))
 1559      print("patches: %d (find: %d)" % counts["patches"])
 1560      print("unassigned: %d" % counts["unassigned"])
 1561      print("ambiguous: %d" % counts["ambiguous"])
 1562      for tree, p in unassigned[:20]:
 1563          print("  unassigned %s:%s" % (tree, p))
 1564      for tree, p, hits in ambiguous[:20]:
 1565          print("  ambiguous %s:%s -> %s" % (tree, p, ", ".join(hits)))
 1566      print("seconds: git %.1f, plans %.1f" % (header["seconds"]["git"], header["seconds"]["plans"]))
 1567      failed = (counts["paths"][0] != counts["paths"][1] or counts["es-paths"][0] != counts["es-paths"][1]
 1568                or counts["patches"][0] != counts["patches"][1] or counts["unassigned"] or counts["ambiguous"])
 1569      if not args.no_write and not args.inject_path:
 1570          dist = os.path.abspath(args.distribution)
 1571          pkgdirs = package_dirs([r[1] for r in rows if r[0] == "distribution"])
 1572          pkg_unit = {r[1]: owning_dir(r[1], pkgdirs) for r in rows if r[0] == "distribution"}
 1573          try:
 1574              guard = secret_patterns(dist)
 1575              lines, escaped = json_rows(rows, guard)
 1576          except CannotRun as e:
 1577              print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1578              return EX_CANNOT
 1579          header["escaped_rows"] = escaped
 1580          print("escaped: %d (rows whose path matches a credential pattern, hyphens written as \\u002d)" % len(escaped))
 1581          try:
 1582              write_json(os.path.join(dist, args.out), header, lines, guard)
 1583          except CannotRun as e:
 1584              print("renovation-inventory: cannot run: %s" % e, file=sys.stderr)
 1585              return EX_CANNOT
 1586          write_markdown(os.path.join(dist, args.markdown), header, rows, counts, pkg_unit)
 1587          with open(os.path.join(dist, args.markdown)) as f:
 1588              hits = [i + 1 for i, l in enumerate(f) if guard.search(l)]
 1589          if hits:
 1590              print("renovation-inventory: %s lines %s match a credential pattern" % (args.markdown, hits[:5]), file=sys.stderr)
 1591              return EX_CANNOT
 1592          print("wrote %s (%d bytes), %s" % (args.out, os.path.getsize(os.path.join(dist, args.out)), args.markdown))
 1593      return EX_FAIL if failed else 0
 1594  
 1595  
 1596  if __name__ == "__main__":
 1597      sys.exit(main())
```

## File: tools/renovation-status (at 2174265e9c, 147 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """renovation-status -- one table of the renovation: every slice, its size, depth, state and drift
    5  (plan § 9; M6.P1, #641).
    6  
    7    tools/renovation-status [--write docs/reviews/status.md] [--no-issues]
    8  
    9  Reads docs/reviews/slices.json (the order), docs/reviews/inventory.json (the
   10  slices' sizes, by the membership `tools/renovation-inventory --order` uses),
   11  docs/reviews/order.md (the preliminary review's status line) and the slice
   12  issues on pixelelated/distribution (one bounded `gh issue list` on milestone
   13  "M6: Codebase renovation", titles `M6.P2 E<epic>/T<k>: ...`, with `reviewed-at:`,
   14  `fixed-at:` and, for EmulationStation paths, `fixed-at-es:` lines in the body;
   15  the run fails if the list reaches its limit). A slice's state:
   16  
   17    unreviewed   no issue yet, or an issue with no audit folder and no reviewed-at
   18    reading      an audit folder docs/audits/*-epic-m6-<slice id>/ exists, reviewed-at empty
   19    remediating  reviewed-at set, fixed-at empty
   20    closed       the issue closed with fixed-at set
   21    drifted      closed, and `tools/renovation-drift` says re-open for it
   22  
   23  The first row is `order: reviewed|unreviewed|pending`, from order.md.
   24  Exit 0 on success, 2 when it cannot run. `--no-issues` skips the tracker
   25  (every slice then reads `unreviewed` unless an audit folder exists) and says so.
   26  """
   27  
   28  import argparse
   29  import importlib.machinery
   30  import importlib.util
   31  import json
   32  import os
   33  import re
   34  import subprocess
   35  import sys
   36  from collections import Counter
   37  
   38  EX_CANNOT = 2
   39  LIMIT = 400
   40  
   41  
   42  def load(dist, name, path):
   43      loader = importlib.machinery.SourceFileLoader(name, os.path.join(dist, path))
   44      spec = importlib.util.spec_from_loader(name, loader)
   45      mod = importlib.util.module_from_spec(spec)
   46      loader.exec_module(mod)
   47      return mod
   48  
   49  
   50  def field(body, name):
   51      m = re.search(r"(?im)^[-*\s`]*%s:\s*`?([0-9a-f]{7,40})?`?\s*$" % re.escape(name), body or "")
   52      return m.group(1) if m and m.group(1) else None
   53  
   54  
   55  def run(args):
   56      dist = os.path.realpath(args.distribution)
   57      inv_mod = load(dist, "renovation_inventory", "tools/renovation-inventory")
   58      with open(os.path.join(dist, "docs/reviews/inventory.json")) as f:
   59          inv = json.load(f)
   60      rows = [dict(zip(inv["columns"], r)) for r in inv["rows"]]
   61      doc, slices = inv_mod.load_slices(dist)
   62      size = Counter()
   63      for r in rows:
   64          hits = inv_mod.slice_of(r, slices)
   65          if len(hits) == 1:
   66              size[hits[0]] += r["lines"] or 0
   67      with open(os.path.join(dist, "docs/reviews/order.md")) as f:
   68          text = f.read()
   69      sec = text.split("## The preliminary review of this order", 1)
   70      m = re.search(r"Status: \*\*(reviewed|unreviewed|pending)\*\*", sec[1] if len(sec) > 1 else "")
   71      order_state = m.group(1) if m else "unknown"
   72      issues = {}
   73      note = ""
   74      if args.no_issues:
   75          note = "The tracker was not read (`--no-issues`)."
   76      else:
   77          r = subprocess.run(["gh", "issue", "list", "--repo", "pixelelated/distribution", "--milestone",
   78                              "M6: Codebase renovation", "--state", "all", "--limit", str(LIMIT),
   79                              "--json", "number,title,state,body"], capture_output=True, text=True)
   80          if r.returncode != 0:
   81              raise RuntimeError("gh issue list: %s" % r.stderr.strip()[:200])
   82          got = json.loads(r.stdout)
   83          if len(got) >= LIMIT:
   84              raise RuntimeError("the issue list reached its limit of %d" % LIMIT)
   85          for i in got:
   86              t = re.match(r"M6\.P2 E\d+/T(\d+): ", i["title"])
   87              if t:
   88                  issues[int(t.group(1))] = i
   89          note = "Slice issues read from the tracker: %d of %d M6 issues." % (len(issues), len(got))
   90      audits = os.listdir(os.path.join(dist, "docs/audits"))
   91      out = ["# Renovation status", "",
   92             "Generated by `tools/renovation-status`; never hand-edited. %s Lines are the slice's lines in "
   93             "`inventory.json` (`%s`)." % (note, inv["header"]["distribution"]["head"][:10]), "",
   94             "| Row | Value |", "| --- | --- |", "| order | %s |" % order_state, "",
   95             "| k | Area | Slice | Lines | Depth | State | Issue | reviewed-at | fixed-at | Drift since |",
   96             "| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |"]
   97      states = Counter()
   98      for sl, _ in slices:
   99          i = issues.get(sl["k"])
  100          body = i["body"] if i else ""
  101          rev, fix = field(body, "reviewed-at"), field(body, "fixed-at")
  102          folder = any(a.endswith("-epic-m6-" + sl["id"]) for a in audits)
  103          drift = "--"
  104          if i and i["state"] == "CLOSED" and fix:
  105              fix_es = field(body, "fixed-at-es")  # an EmulationStation slice also records the ES commit
  106              d = subprocess.run([os.path.join(dist, "tools/renovation-drift"), "--distribution", dist,
  107                                  "--pretend", "%s=%s%s" % (sl["id"], fix, ",es=" + fix_es if fix_es else "")],
  108                                 capture_output=True, text=True)
  109              if d.returncode == 2:
  110                  raise RuntimeError("renovation-drift for %s: %s" % (sl["id"], d.stderr.strip()[:200]))
  111              line = [l for l in d.stdout.splitlines() if l.startswith("| %d |" % sl["k"])]
  112              drift = line[0].split("|")[7].strip() if line else "--"
  113              state = "drifted" if d.returncode == 1 else "closed"
  114          elif rev and not fix:
  115              state = "remediating"
  116          elif folder:
  117              state = "reading"
  118          else:
  119              state = "unreviewed"
  120          states[state] += 1
  121          out.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
  122              sl["k"], sl["area"], sl["id"], "{:,}".format(size[sl["id"]]), sl["depth"], state,
  123              "#%d" % i["number"] if i else "--", rev or "", fix or "", drift))
  124      out += ["", "States: " + ", ".join("%s %d" % kv for kv in sorted(states.items())) + "."]
  125      text = "\n".join(out) + "\n"
  126      print(text, end="")
  127      if args.write:
  128          with open(os.path.join(dist, args.write), "w") as f:
  129              f.write(text)
  130      return 0
  131  
  132  
  133  def main():
  134      ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
  135      ap.add_argument("--distribution", default=".")
  136      ap.add_argument("--write", help="also write the table here (docs/reviews/status.md)")
  137      ap.add_argument("--no-issues", action="store_true")
  138      args = ap.parse_args()
  139      try:
  140          return run(args)
  141      except (RuntimeError, OSError, ValueError, KeyError) as e:
  142          print("renovation-status: cannot run: %s" % e, file=sys.stderr)
  143          return EX_CANNOT
  144  
  145  
  146  if __name__ == "__main__":
  147      sys.exit(main())
```

## File: tools/rules-check (at 8ebaf8daad, 245 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # Are the instruction files what instruction-files.md says they are?
    6  #
    7  #   tools/rules-check            # every check, one line each; exit 1 on any failure
    8  #   tools/rules-check --quiet    # failures only (the push guard and the fork CI)
    9  #   tools/rules-check --write-agents   # regenerate the rule list in AGENTS.md from the front matter
   10  #
   11  # Checks, each a thing that was found wrong on 2026-09-25 (#269, D-WORKFLOW-045):
   12  #   front    every .claude/rules/*.md opens with front matter: `---`, a one-line
   13  #            `description:` first, then an optional `paths:` list (with `#`
   14  #            comments), then `---`; nothing before it. ceremonies.md had none.
   15  #   always   a rule with no `paths:` says so in its first paragraph (the word
   16  #            "session"), as the front-matter standard asks.
   17  #   index    the index table in instruction-files.md names every file in the
   18  #            directory and nothing that is not there. Three files were missing.
   19  #   count    a sentence in CLAUDE.md or AGENTS.md that says "All N" of the rules
   20  #            says the number the directory has. Both said 24 of 27.
   21  #   agents   AGENTS.md and CLAUDE.md exist, and AGENTS.md is within Codex's
   22  #            project-doc budget (32 KiB) so it is read whole.
   23  #   list     the block between the rules-index markers in AGENTS.md is exactly
   24  #            what --write-agents generates from the front matter (Codex loads
   25  #            no rule on its own, so the list is how it learns they exist).
   26  #   mention  every rule file is named in CLAUDE.md as well.
   27  #   tools    fork-only tool names agree in the hook and both rule inventories.
   28  #
   29  # The guard for the shape "an instruction file nobody can find is one nobody
   30  # applies" (instruction-files.md § The index); run by tools/ceremony-check
   31  # --gate and .github/workflows/fork-checks.yml.
   32  
   33  import os
   34  import re
   35  import sys
   36  
   37  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   38  RULES = os.path.join(ROOT, '.claude', 'rules')
   39  INDEX = os.path.join(RULES, 'instruction-files.md')
   40  CODEX_DOC_BUDGET = 32 * 1024
   41  BEGIN = '<!-- rules-index:begin (generated by tools/rules-check --write-agents; do not edit by hand) -->'
   42  END = '<!-- rules-index:end -->'
   43  
   44  
   45  def rules_block(files):
   46      """The generated list: every-session rules first, then scoped, each with its description."""
   47      every, scoped = [], []
   48      for f in files:
   49          desc, paths, _, err = front_matter(os.path.join(RULES, f))
   50          if err:
   51              continue
   52          if paths is None or paths == ['**']:
   53              every.append((f, desc))
   54          else:
   55              scoped.append((f, desc, paths))
   56      out = ['**Every session** (no `paths:` glob, or `**`):', '']
   57      for f, d in every:
   58          out.append('- `%s` -- %s' % (f, d))
   59      out += ['', '**Scoped** (open before touching the paths):', '']
   60      for f, d, p in scoped:
   61          out.append('- `%s` -- %s (paths: %s)' % (f, d, ', '.join('`%s`' % x for x in p)))
   62      return '\n'.join(out)
   63  
   64  
   65  def front_matter(path):
   66      """(description, paths_or_None, body_lines, error)."""
   67      lines = open(path, encoding='utf-8').read().split('\n')
   68      if not lines or lines[0].strip() != '---':
   69          return None, None, lines, 'no front matter (the file must open with ---)'
   70      if len(lines) < 2 or not lines[1].startswith('description:'):
   71          return None, None, lines, 'description is not the first key of the front matter'
   72      desc = lines[1][len('description:'):].strip().strip('"\'')
   73      i = 2
   74      paths = None
   75      while i < len(lines) and lines[i].strip() != '---':
   76          s = lines[i]
   77          if s.startswith('paths:'):
   78              paths = []
   79          elif s.strip().startswith('#'):
   80              pass
   81          elif s.startswith('  - ') or s.startswith('- '):
   82              if paths is None:
   83                  return desc, None, lines, 'a list item outside paths: in the front matter'
   84              paths.append(s.strip()[2:].strip('"\''))
   85          elif s.strip() == '':
   86              pass
   87          else:
   88              return desc, paths, lines, 'front matter line is not description/paths/comment: %r' % s[:60]
   89          i += 1
   90      if i >= len(lines):
   91          return desc, paths, lines, 'front matter never closes'
   92      if not desc:
   93          return desc, paths, lines, 'description is empty'
   94      if paths is not None and not paths:
   95          return desc, paths, lines, 'paths: is present but lists nothing'
   96      return desc, paths, lines[i + 1:], None
   97  
   98  
   99  def first_paragraph(body):
  100      out = []
  101      started = False
  102      for l in body:
  103          if not started:
  104              if l.strip() == '' or l.startswith('#'):
  105                  continue
  106              started = True
  107          if l.strip() == '':
  108              break
  109          out.append(l)
  110      return ' '.join(out)
  111  
  112  
  113  
  114  def tool_inventory_errors(index_text, workflow_text, hook_text):
  115      """Compare the three documented inventories, including grouped table cells."""
  116      workflow = re.search(r'^- \*\*Fork-only tools\*\*.*$', workflow_text, re.M)
  117      table = index_text.partition("## The fork's own tools")[2]
  118      if not workflow or not table:
  119          return ['missing fork tool inventory section']
  120      expected = set(re.findall(r'`tools/([^`]+)`', workflow.group()))
  121      hooked = set(re.findall(r"^  'tools/([^']+)'", hook_text, re.M))
  122      indexed = set()
  123      for line in table.splitlines():
  124          if line.startswith('| `'):
  125              indexed.update(re.findall(r'`([^`]+)`', line.split('|')[1]))
  126      indexed.discard('pkgcheck')  # explicitly documented as upstream's
  127      errors = []
  128      if not expected or not hooked or not indexed:
  129          errors.append('empty fork tool inventory')
  130      for label, names in [('hook', hooked), ('index', indexed)]:
  131          for name in sorted(expected - names):
  132              errors.append(f'{label} missing tools/{name}')
  133          for name in sorted(names - expected):
  134              errors.append(f'{label} names tools/{name} absent from fork-workflow')
  135      return errors
  136  
  137  
  138  def main():
  139      quiet = '--quiet' in sys.argv
  140      fails = []
  141      notes = []
  142  
  143      def ok(msg):
  144          if not quiet:
  145              print('ok    ' + msg)
  146  
  147      def fail(msg):
  148          fails.append(msg)
  149          print('FAIL  ' + msg)
  150  
  151      files = sorted(f for f in os.listdir(RULES) if f.endswith('.md'))
  152      # front + always
  153      for f in files:
  154          desc, paths, body, err = front_matter(os.path.join(RULES, f))
  155          if err:
  156              fail('front   %s: %s' % (f, err))
  157              continue
  158          ok('front   %s' % f)
  159          if paths is None:
  160              para = first_paragraph(body).lower()
  161              if 'session' not in para:
  162                  fail('always  %s has no paths: and its first paragraph does not say it loads every session' % f)
  163              else:
  164                  ok('always  %s says it loads every session' % f)
  165      # index
  166      text = open(INDEX, encoding='utf-8').read()
  167      m = re.search(r'^## The index\n(.*?)^## ', text, re.S | re.M)
  168      section = m.group(1) if m else ''
  169      rows = re.findall(r'^\| `([a-z0-9-]+\.md)` \|', section, re.M)
  170      listed = set(rows)
  171      have = set(files)
  172      for f in sorted(have - listed):
  173          fail('index   %s is in .claude/rules/ and not in the index table of instruction-files.md' % f)
  174      for f in sorted(listed - have):
  175          fail('index   the index names %s, which is not in .claude/rules/' % f)
  176      dup = sorted(r for r in listed if rows.count(r) > 1)
  177      for f in dup:
  178          fail('index   %s appears twice in the index' % f)
  179      if have == listed and not dup:
  180          ok('index   %d files, %d rows, the same set' % (len(have), len(rows)))
  181      # tools: a new tool must be discoverable and protected from upstream PRs.
  182      with open(os.path.join(RULES, 'fork-workflow.md'), encoding='utf-8') as f:
  183          workflow_text = f.read()
  184      with open(os.path.join(ROOT, '.githooks', 'pre-push'), encoding='utf-8') as f:
  185          hook_text = f.read()
  186      inventory_errors = tool_inventory_errors(text, workflow_text, hook_text)
  187      for error in inventory_errors:
  188          fail('tools   ' + error)
  189      if not inventory_errors:
  190          ok('tools   hook, fork-workflow and instruction index agree')
  191      # count
  192      for name in ('CLAUDE.md', 'AGENTS.md'):
  193          p = os.path.join(ROOT, name)
  194          if not os.path.exists(p):
  195              fail('agents  %s is missing' % name)
  196              continue
  197          t = open(p, encoding='utf-8').read()
  198          for n in re.findall(r'\bAll (\d+)(?: of them|,)', t, re.I):
  199              if int(n) != len(files):
  200                  fail('count   %s says "All %s" of the rules; the directory holds %d' % (name, n, len(files)))
  201              else:
  202                  ok('count   %s says All %s, and there are %d' % (name, n, len(files)))
  203          if name == 'AGENTS.md':
  204              size = os.path.getsize(p)
  205              if size > CODEX_DOC_BUDGET:
  206                  fail('agents  AGENTS.md is %d bytes, over the %d-byte project-doc budget Codex reads whole' % (size, CODEX_DOC_BUDGET))
  207              else:
  208                  ok('agents  AGENTS.md is %d bytes (budget %d)' % (size, CODEX_DOC_BUDGET))
  209      # list: the generated block in AGENTS.md
  210      ap = os.path.join(ROOT, 'AGENTS.md')
  211      if os.path.exists(ap):
  212          t = open(ap, encoding='utf-8').read()
  213          want = rules_block(files)
  214          if BEGIN in t and END in t:
  215              head, rest = t.split(BEGIN, 1)
  216              cur, tail = rest.split(END, 1)
  217              if '--write-agents' in sys.argv:
  218                  open(ap, 'w', encoding='utf-8').write(head + BEGIN + '\n' + want + '\n' + END + tail)
  219                  print('wrote the rule list into AGENTS.md (%d rules)' % len(files))
  220                  cur = '\n' + want + '\n'
  221              if cur.strip('\n') != want:
  222                  fail('list    the rule list in AGENTS.md is stale: run tools/rules-check --write-agents')
  223              else:
  224                  ok('list    AGENTS.md carries the generated rule list')
  225          else:
  226              fail('list    AGENTS.md has no rules-index markers')
  227      # mention: CLAUDE.md names every rule too
  228      cp = os.path.join(ROOT, 'CLAUDE.md')
  229      if os.path.exists(cp):
  230          t = open(cp, encoding='utf-8').read()
  231          missing = [f for f in files if f[:-3] not in t]
  232          if missing:
  233              fail('mention CLAUDE.md does not name: %s' % ', '.join(missing))
  234          else:
  235              ok('mention CLAUDE.md names every rule')
  236      if fails:
  237          print('rules-check: %d failure(s)' % len(fails))
  238          return 1
  239      if not quiet:
  240          print('rules-check: %d rule files, every one front-mattered and indexed' % len(files))
  241      return 0
  242  
  243  
  244  if __name__ == '__main__':
  245      sys.exit(main())
```

## File: tools/vocabulary-check (at 8ebaf8daad, 132 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  """vocabulary-check - the player-facing words, held to the rules a reader would apply.
    5  
    6    ./tools/vocabulary-check [--es <emulationstation checkout>] [--scripts <dir>] [--show]
    7  
    8  Three rules, from es-player-text.md and player-language.md (D-UI-022/045,
    9  #148): "back up" is two words as a verb (BACK UP SAVES TO THE CLOUD, back up
   10  your settings) and one word as a noun or adjective (RESTORE FROM BACKUP, the
   11  settings backup, a backup file); "save state" is two words (the directory is
   12  savestates, the label is not); "Wi-Fi" keeps its hyphen. The maintainer asked
   13  for the first to be checked mechanically across the interface and the scripts
   14  (2026-09-12), after a sweep by hand found one string each way; #148 added the
   15  other two after a hand count found fourteen SAVESTATE labels. A reader applies
   16  a rule once; this applies them on every run of tools/vm-qa (the `vocabulary`
   17  suite).
   18  
   19  What it reads: every _("...") string in the EmulationStation checkout
   20  (default: the qa-integration worktree, or $ES_SRC), and every sentence the
   21  cloud scripts print for a player -- log_message ... "true", note, say_why,
   22  echo -- plus the whole of backuptool's notes. Comments are skipped. It exits
   23  1 with each offending string and the file it came from; 0 when clean.
   24  
   25  Heuristics, so an allowlist carries the few strings that are right and
   26  still match (upstream's hidden BACKUP USER DATA page, for one):
   27    verb written as one word: BACKUP followed by TO / YOUR / MY / THE SAVES /
   28        SAVES / SETTINGS / EVERYTHING / IT / THEM / NOW / USER DATA / ROMS
   29    noun written as two words: A / THE / YOUR / LAST / FIRST / NEWEST / NO /
   30        SETTINGS / CLOUD / MY  BACK UP  not followed by a verb's object
   31    the hyphen: BACK-UP anywhere
   32  """
   33  import argparse, os, re, sys
   34  
   35  HERE = os.path.dirname(os.path.abspath(__file__))
   36  ROOT = os.path.dirname(HERE)
   37  DEFAULT_ES = os.environ.get("ES_SRC") or os.path.expanduser("~/Development/emulationstation-next.worktrees/qa-integration")
   38  SCRIPTS = os.path.join(ROOT, "projects/ROCKNIX/packages/network/rclone/sources")
   39  BACKUPTOOL = os.path.join(ROOT, "projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool")
   40  
   41  # Strings that match a heuristic and are nonetheless right, or are not ours to
   42  # change (upstream's, on pages ROCKNIX does not show). Each with its reason.
   43  ALLOW = {
   44      "BACKUP USER DATA": "upstream batocera GuiBackupStart, hidden on ROCKNIX (no ApiSystem::BACKUP); its msgid keys translations",
   45  }
   46  
   47  VERB_AS_ONE = re.compile(r"\bBACKUP (TO|YOUR|MY|THE SAVES|SAVES|SETTINGS|EVERYTHING|IT|THEM|NOW|USER DATA|ROMS|GAME)\b", re.I)
   48  # A word that makes the BACKUP before an object a noun after all: "your
   49  # settings backup to the cloud" is a noun phrase with a destination, not an
   50  # order to back up. Checked on the word before each VERB_AS_ONE match.
   51  NOUN_MARKERS = {"YOUR", "THE", "A", "AN", "SETTINGS", "LAST", "FIRST", "NEWEST", "OLDEST", "CLOUD", "NO", "THIS", "THAT", "MY", "EACH", "EVERY", "SAVES", "DEVICE", "OWN", "NEW", "OLD", "SAME", "ONE"}
   52  NOUN_AS_TWO = re.compile(r"\b(A|THE|YOUR|LAST|FIRST|NEWEST|NO|SETTINGS|CLOUD|MY|EACH|EVERY|THIS|THAT) BACK UP\b(?! (TO|YOUR|MY|SAVES|SETTINGS|EVERYTHING|IT|THEM|NOW|ROMS|GAME|WHAT|THIS|THESE|THE|A|AGAIN|NOTHING|SOME|ANY|ALL))", re.I)
   53  HYPHEN = re.compile(r"\bBACK-UP\b", re.I)
   54  # es-player-text / es-native-ui § Conventions: a snapshot of the running machine
   55  # is a "save state", two words -- the directory is savestates, the label is
   56  # not (#148: fourteen shipped labels said SAVESTATE). And "Wi-Fi", hyphenated,
   57  # in every player-visible string; the settings keys stay wifi.*.
   58  ONE_WORD_STATE = re.compile(r"\bSAVESTATES?\b", re.I)
   59  UNHYPHENATED_WIFI = re.compile(r"\bWIFI\b", re.I)
   60  
   61  def judge(text):
   62      t = text.replace("\\n", " ")
   63      hits = []
   64      for m in VERB_AS_ONE.finditer(t):
   65          before = t[:m.start()].rstrip().split()
   66          if before and before[-1].upper().strip("'\",.:;()") in NOUN_MARKERS:
   67              continue
   68          hits.append("verb written as one word"); break
   69      if NOUN_AS_TWO.search(t): hits.append("noun written as two words")
   70      if HYPHEN.search(t): hits.append("hyphenated")
   71      if ONE_WORD_STATE.search(t): hits.append("save state written as one word")
   72      if UNHYPHENATED_WIFI.search(t): hits.append("Wi-Fi without its hyphen")
   73      return hits
   74  
   75  def es_strings(es):
   76      pat = re.compile(r'_\("((?:[^"\\]|\\.)*)"\)')
   77      for dirpath, _, files in os.walk(os.path.join(es, "es-app", "src")):
   78          for f in files:
   79              if not f.endswith((".cpp", ".h")): continue
   80              p = os.path.join(dirpath, f)
   81              try: src = open(p, encoding="utf-8", errors="replace").read()
   82              except OSError: continue
   83              # drop line comments so a commented-out string is not judged
   84              src = re.sub(r"//[^\n]*", "", src)
   85              for m in pat.finditer(src):
   86                  yield os.path.relpath(p, es), m.group(1)
   87  
   88  def script_lines(paths):
   89      say = re.compile(r'\b(log_message|note|say_why|echo)\s+"((?:[^"\\]|\\.)*)"(.*)')
   90      for p in paths:
   91          try: lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
   92          except OSError: continue
   93          for line in lines:
   94              s = line.strip()
   95              if s.startswith("#"): continue
   96              m = say.search(s)
   97              if not m: continue
   98              fn, text, rest = m.groups()
   99              if fn == "log_message" and '"false"' in rest: continue   # a log line, not a screen line
  100              yield os.path.relpath(p, ROOT), text
  101  
  102  def main():
  103      ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  104      ap.add_argument("--es", default=DEFAULT_ES)
  105      ap.add_argument("--scripts", default=SCRIPTS)
  106      ap.add_argument("--show", action="store_true", help="also list every string that was judged")
  107      a = ap.parse_args()
  108      if not os.path.isdir(os.path.join(a.es, "es-app", "src")):
  109          print(f"vocabulary-check: no EmulationStation checkout at {a.es} (set ES_SRC or --es)", file=sys.stderr)
  110          return 1
  111      paths = [os.path.join(a.scripts, n) for n in ("cloud_backup", "cloud_restore", "cloud_content_backup", "cloud_content_restore", "cloud_setup", "cloud_saves_root", "cloud_net_ready")] + [BACKUPTOOL]
  112      judged = failures = 0
  113      seen = set()
  114      for origin, text in list(es_strings(a.es)) + list(script_lines(paths)):
  115          if not re.search(r"\bBACK(ING|ED)? ?-?UPS?\b|\bSAVE ?STATES?\b|\bWI-?FI\b", text, re.I): continue
  116          judged += 1
  117          if a.show: print(f"  {origin}: {text[:110]}")
  118          hits = judge(text)
  119          if not hits: continue
  120          key = text.replace("\\n", " ").strip()
  121          if key in ALLOW:
  122              if key not in seen:
  123                  print(f"  allowed  {origin}: {key[:90]}  -- {ALLOW[key]}")
  124                  seen.add(key)
  125              continue
  126          failures += 1
  127          print(f"  FAIL  {origin}: {text[:120]}  -- {', '.join(hits)}")
  128      print(f"vocabulary-check: {judged} string(s) with back up / backup, save state or Wi-Fi judged, {failures} wrong")
  129      return 1 if failures else 0
  130  
  131  if __name__ == "__main__":
  132      sys.exit(main())
```

## File: tools/work-log-index (at 8ebaf8daad, 106 lines)

```text
    1  #!/usr/bin/env python3
    2  # SPDX-License-Identifier: GPL-2.0
    3  # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
    4  #
    5  # The work logs at a day's, a week's and a month's distance: one index over
    6  # docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md, listing every
    7  # timestamped entry's title under its day, the days under their ISO week, the
    8  # weeks under their month. The day files stay the record; this is the table
    9  # of contents that lets a month be read in a minute and a settled question be
   10  # found before it is asked again (#253, D-QA-039's rule).
   11  #
   12  #   tools/work-log-index            # print the index
   13  #   tools/work-log-index --write    # write docs/work-logs/INDEX.md
   14  #   tools/work-log-index --check    # exit 1 when INDEX.md is not what --write would produce
   15  #
   16  # Regenerate after appending an entry; the pre-push guard warns when a
   17  # work-log change is pushed without the index.
   18  
   19  import datetime
   20  import os
   21  import re
   22  import sys
   23  
   24  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   25  BASE = os.path.join(ROOT, 'docs/work-logs')
   26  OUT = os.path.join(BASE, 'INDEX.md')
   27  
   28  
   29  def entries():
   30      days = {}
   31      for d, _, files in os.walk(BASE):
   32          for f in files:
   33              m = re.match(r'(\d{4})_(\d\d)_(\d\d)-work_log\.md$', f)
   34              if not m:
   35                  continue
   36              date = datetime.date(*map(int, m.groups()))
   37              rel = os.path.relpath(os.path.join(d, f), BASE)
   38              items = []
   39              for line in open(os.path.join(d, f), encoding='utf-8'):
   40                  if not line.startswith('## '):
   41                      continue
   42                  hm = re.match(r'## (\d\d:\d\d) UTC\s*[—–-]+\s*(.*)', line.strip())
   43                  if hm:
   44                      items.append((hm.group(1), hm.group(2).strip()))
   45                  else:
   46                      items.append(('', line.strip().lstrip('# ').strip()))
   47              days[date] = (rel, items)
   48      return days
   49  
   50  
   51  def render(days):
   52      out = ['# Work-log index', '',
   53             'Generated by `tools/work-log-index --write` from the day files under this directory; '
   54             'regenerate after appending an entry. One line per timestamped entry, days under their ISO week, weeks under their month. '
   55             'The day file is the record; this is where a month is read in a minute.', '']
   56      total = sum(len(v[1]) for v in days.values())
   57      months = {}
   58      for date in days:
   59          months.setdefault((date.year, date.month), []).append(date)
   60      out.append('%d entries over %d days in %d months: %s.' % (
   61          total, len(days), len(months),
   62          ', '.join('%04d-%02d' % k for k in sorted(months))))
   63      out.append('')
   64      for (y, mo) in sorted(months, reverse=True):
   65          mdays = sorted(months[(y, mo)], reverse=True)
   66          mcount = sum(len(days[d][1]) for d in mdays)
   67          out.append('## %04d-%02d (%d entries over %d days)' % (y, mo, mcount, len(mdays)))
   68          out.append('')
   69          weeks = {}
   70          for d in mdays:
   71              iso = d.isocalendar()
   72              weeks.setdefault((iso[0], iso[1]), []).append(d)
   73          for (wy, wn) in sorted(weeks, reverse=True):
   74              wdays = sorted(weeks[(wy, wn)], reverse=True)
   75              wcount = sum(len(days[d][1]) for d in wdays)
   76              out.append('### Week %04d-W%02d, %s to %s (%d entries over %d days)' % (
   77                  wy, wn, wdays[-1].strftime('%b %d'), wdays[0].strftime('%b %d'), wcount, len(wdays)))
   78              out.append('')
   79              for d in wdays:
   80                  rel, items = days[d]
   81                  out.append('#### [%s](%s) (%d)' % (d.isoformat(), rel, len(items)))
   82                  for when, title in items:
   83                      out.append('- %s%s' % ((when + ' ') if when else '', title))
   84                  out.append('')
   85      return '\n'.join(out).rstrip('\n') + '\n'
   86  
   87  
   88  def main():
   89      text = render(entries())
   90      if '--write' in sys.argv:
   91          open(OUT, 'w', encoding='utf-8').write(text)
   92          print('wrote %s (%d lines)' % (os.path.relpath(OUT, ROOT), text.count('\n')))
   93          return 0
   94      if '--check' in sys.argv:
   95          cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
   96          if cur == text:
   97              print('work-log index: current')
   98              return 0
   99          print('work-log index: STALE -- run tools/work-log-index --write')
  100          return 1
  101      sys.stdout.write(text)
  102      return 0
  103  
  104  
  105  if __name__ == '__main__':
  106      sys.exit(main())
```

## The constructed cases: t10-guard-gaps.sh

```text
#!/bin/bash
# t10-guard-gaps.sh -- T10's constructed inputs for the shapes the guards'
# own suite (.githooks/hooks-test) does not construct. It runs a hooks
# directory and a forbidden-terms-check against a scratch repository,
# using hooks-test's method:
#   - the wordlist is a stand-in (FORBIDDEN_TERMS_FILE), never the real list;
#   - the credential-shaped value is built at run time from printf pieces,
#     so this file at rest carries no line a scanner would match;
#   - an output is never printed: only each case's exit code, and whether
#     the refusal redacted and stayed silent about the value.
#
#   t10-guard-gaps.sh <hooks-dir> <forbidden-terms-check> [scratch-parent]
#
# Each case prints `CASE <name>: rc=<n> <allowed|refused> [notes]`. A case
# the guard should refuse that prints `allowed` is a gap. Exit 0 when every
# case ran (whatever the verdicts); 2 when the scratch could not be made.
set -u
HOOKS="$(cd "${1:?hooks dir}" && pwd)"; FTC="$(readlink -f "${2:?forbidden-terms-check}")"
PARENT="${3:-/workspace/tmp}"
SCRATCH="$(mktemp -d -p "${PARENT}" t10-gaps.XXXXXX)" || exit 2
trap 'rm -rf "${SCRATCH}"' EXIT
FAKE="$(printf 'dev%s=%s' password QwErTyUiOpAsDfGh)"
WORD="$(printf 'zebra%s quartet' fish)"
printf "FORBIDDEN_PATTERNS='zebrafish[ ]quartet|qzx-estate'\\n" > "${SCRATCH}/wordlist"
export FORBIDDEN_TERMS_FILE="${SCRATCH}/wordlist"
unset FORBIDDEN_PATTERNS SECRET_PATTERNS_FILE
ZERO=0000000000000000000000000000000000000000
mkdir -p "${SCRATCH}/nohooks"
g() { git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${SCRATCH}/nohooks" "$@"; }
report() {  # report <name> <rc>
  local v=allowed n=""; [ "$2" -ne 0 ] && v=refused
  grep -q -F -- "QwErTyUiOpAsDfGh" "${SCRATCH}/out" && n="${n} VALUE-PRINTED"
  grep -q -i -F -- "zebrafish" "${SCRATCH}/out" && n="${n} WORD-PRINTED"
  grep -q -F -- "[REDACTED]" "${SCRATCH}/out" && n="${n} redacted"
  grep -q -F -- "could not be read" "${SCRATCH}/out" && n="${n} (reason: a file could not be read)"
  grep -q -F -- "personal artifacts" "${SCRATCH}/out" && n="${n} (reason: personal artifacts)"
  grep -q -F -- "listed word" "${SCRATCH}/out" && n="${n} (reason: a listed word)"
  grep -q -F -- "credential-shaped" "${SCRATCH}/out" && n="${n} (reason: credential-shaped)"
  echo "CASE $1: rc=$2 ${v}${n}"
}
run() { local name="$1"; shift; "$@" >"${SCRATCH}/out" 2>&1; report "${name}" "$?"; }
push_line() { printf '%s\n' "$1" | "${HOOKS}/pre-push" origin "file://${SCRATCH}/remote.git"; }

cd "${SCRATCH}" && git init -q -b main work && cd work || exit 2
git init -q --bare "${SCRATCH}/remote.git" && git remote add origin "${SCRATCH}/remote.git"
echo base > a.txt; g add a.txt; g commit -q -m base; g push -q origin main; remote="$(git rev-parse HEAD)"

# --- pre-commit
printf 'x\0y\n%s\n' "${FAKE}" > b.bin; g add b.bin
run "pre-commit: a credential in a file git treats as binary (a NUL byte)" "${HOOKS}/pre-commit"
g reset -q; rm b.bin
printf 'x\0y\n%s\n' "${WORD}" > w.bin; g add w.bin
run "pre-commit: a listed word in a file git treats as binary" "${HOOKS}/pre-commit"
g reset -q; rm w.bin
printf 'msgid "x"\nmsgstr "%s"\n' "${FAKE}" > fr.po; g add fr.po
run "pre-commit: a credential in a .po file" "${HOOKS}/pre-commit"
g reset -q; rm fr.po
printf 'msgid "x"\nmsgstr "%s"\n' "${WORD}" > fr.po; g add fr.po
run "pre-commit: a listed word in a .po file" "${HOOKS}/pre-commit"
g reset -q; rm fr.po
printf '%s\n' "${FAKE}" > c.txt; g add c.txt
run "pre-commit: control, the same credential in a text file" "${HOOKS}/pre-commit"
g reset -q; rm c.txt

# --- commit-msg, through a real commit as git runs it (-m, default cleanup)
git checkout -q -b msg
echo m > m.txt; git add m.txt
git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${HOOKS}" commit -q -m 'tidy' -m "# the ${WORD} notes" >"${SCRATCH}/out" 2>&1; rc=$?
report "commit-msg: a listed word on a # line given with git commit -m" "${rc}"
echo "  the stored message keeps the # line: $(git log -1 --format=%B | grep -c '^# ') line(s)"
git -c user.name=t -c user.email=t@t -c commit.gpgsign=false -c "core.hooksPath=${HOOKS}" commit -q --allow-empty -m 'tidy' -m "the ${WORD} notes" >"${SCRATCH}/out" 2>&1; rc=$?
report "commit-msg: control, the same word on an ordinary line" "${rc}"
run "pre-push: the branch carrying the # line, pushed" push_line "refs/heads/msg $(git rev-parse HEAD~0) refs/heads/msg ${ZERO}"
git checkout -q main

# --- pre-push
g checkout -q -b bin "${remote}"; printf 'x\0y\n%s\n' "${FAKE}" > s.bin; g add s.bin; g commit -q -m s; g rm -q s.bin; g commit -q -m gone
run "pre-push: a credential in a binary file in a middle commit, gone at the tip" push_line "refs/heads/bin $(git rev-parse HEAD) refs/heads/bin ${ZERO}"
g checkout -q -b bintxt "${remote}"; printf '%s\n' "${FAKE}" > s.txt; g add s.txt; g commit -q -m s; g rm -q s.txt; g commit -q -m gone
run "pre-push: control, the same in a text file" push_line "refs/heads/bintxt $(git rev-parse HEAD) refs/heads/bintxt ${ZERO}"
g checkout -q -b po "${remote}"; printf 'msgid "x"\nmsgstr "%s"\n' "${FAKE}" > fr.po; g add fr.po; g commit -q -m po
run "pre-push: a credential in a .po file at the tip" push_line "refs/heads/po $(git rev-parse HEAD) refs/heads/po ${ZERO}"
g checkout -q -b powd "${remote}"; printf 'msgid "x"\nmsgstr "%s"\n' "${WORD}" > fr.po; g add fr.po; g commit -q -m po
run "pre-push: a listed word in a .po file at the tip" push_line "refs/heads/powd $(git rev-parse HEAD) refs/heads/powd ${ZERO}"
# a pr/* branch, one commit on upstream/next, adding a personal path whose name git quotes
g update-ref refs/remotes/upstream/next "${remote}"
g checkout -q -b pr/x "${remote}"; mkdir -p docs; echo note > "docs/$(printf 'caf\303\251').md"; g add docs; g commit -q -m 'x: a note'
run "pre-push: a pr/* branch adding docs/<non-ASCII name>.md (a personal path git quotes)" push_line "refs/heads/pr/x $(git rev-parse HEAD) refs/heads/pr/x ${ZERO}"
g -c core.quotePath=false log -1 >/dev/null
git config core.quotePath false
run "pre-push: the same with core.quotePath=false" push_line "refs/heads/pr/x $(git rev-parse HEAD) refs/heads/pr/x ${ZERO}"
git config --unset core.quotePath
g checkout -q -b pr/y "${remote}"; mkdir -p docs; echo note > docs/plain.md; g add docs; g commit -q -m 'y: a note'
run "pre-push: control, a pr/* branch adding docs/plain.md" push_line "refs/heads/pr/y $(git rev-parse HEAD) refs/heads/pr/y ${ZERO}"

# --- forbidden-terms-check
cd "${SCRATCH}" && git init -q -b main ftc && cd ftc || exit 2
ln -s "notes-on-the-${WORD// /-}" link; printf '%s\n' "${WORD}" > plain.txt; g add link plain.txt; g commit -q -m f
FORBIDDEN_PATTERNS='zebrafish[ -]quartet' run "forbidden-terms-check: a tree with a listed word in a file and one in a symlink's target" "${FTC}" "${SCRATCH}/ftc"
echo "  hits named: $(grep -c -E '^(link|plain\.txt):' "${SCRATCH}/out") ($(grep -o -E '^(link|plain\.txt)' "${SCRATCH}/out" | sort -u | tr '\n' ' '))"
rm plain.txt link
FORBIDDEN_PATTERNS='zebrafish[ -]quartet' run "forbidden-terms-check: the same tree with its tracked files deleted from the checkout" "${FTC}" "${SCRATCH}/ftc"
echo "  says: $(grep -o -E '[0-9]+ hits? in [0-9]+ tracked files' "${SCRATCH}/out")"
exit 0

```

## The constructed cases: gaps-hash.txt

```text
CASE pre-commit: a credential in a file git treats as binary (a NUL byte): rc=0 allowed
CASE pre-commit: a listed word in a file git treats as binary: rc=0 allowed
CASE pre-commit: a credential in a .po file: rc=0 allowed
CASE pre-commit: a listed word in a .po file: rc=0 allowed
CASE pre-commit: control, the same credential in a text file: rc=1 refused redacted (reason: a listed word) (reason: credential-shaped)
CASE commit-msg: a listed word on a # line given with git commit -m: rc=0 allowed
  the stored message keeps the # line: 1 line(s)
CASE commit-msg: control, the same word on an ordinary line: rc=1 refused (reason: a listed word)
CASE pre-push: the branch carrying the # line, pushed: rc=1 refused (reason: a listed word)
CASE pre-push: a credential in a binary file in a middle commit, gone at the tip: rc=0 allowed
CASE pre-push: control, the same in a text file: rc=1 refused redacted (reason: a listed word) (reason: credential-shaped)
CASE pre-push: a credential in a .po file at the tip: rc=0 allowed
CASE pre-push: a listed word in a .po file at the tip: rc=0 allowed
CASE pre-push: a pr/* branch adding docs/<non-ASCII name>.md (a personal path git quotes): rc=1 refused (reason: a file could not be read) (reason: a listed word)
CASE pre-push: the same with core.quotePath=false: rc=1 refused (reason: personal artifacts)
CASE pre-push: control, a pr/* branch adding docs/plain.md: rc=1 refused (reason: personal artifacts)
CASE forbidden-terms-check: a tree with a listed word in a file and one in a symlink's target: rc=1 refused
  hits named: 1 (plain.txt )
CASE forbidden-terms-check: the same tree with its tracked files deleted from the checkout: rc=0 allowed
  says: 0 hits in 0 tracked files

```