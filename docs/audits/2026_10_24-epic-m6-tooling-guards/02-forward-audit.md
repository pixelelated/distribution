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
| 10 | no push beyond the lane's branch, no forbidden run, no credential line, no listed word, read as the guards' own scans (the coordinator's 17:44 ruling) | every push the lane's own branch; every commit passed the primary checkout's pre-commit; `guard_scan`'s patterns (`SECRET_PATTERNS`) over every file of the folder: **0 lines**; `forbidden-terms-check --stdin` over the folder: **0 hits** (`00`, stage C). The briefs stay in the folder as sent; criterion 10's literal grep counts their copies of the slice's own hooks (8 lines) | `00` § Stage C |
| 11 | 04 Q6: the guard table and the tool-caller table | the evidence is here (§ Callers, § The suites, F-rows); the tables are `04`'s | `04` § Q6 |
| 12 | 04 Q3: the fail-open hunt through the named readers | the evidence is here (F-01 to F-30); the table is `04`'s | `04` § Q3 |
| 13 | 04 Q7: the personal-path diff entry by entry; three descriptions per guard | P2 (the diff); the description rows are `04`'s | `04` § Q7 |
| 14 | proof cells in § Proofs = proof lines in 00 | 25 = 25 | § Proofs; `command grep -c` |
| 15 | every item `question:`; bugs pass box-check; no member edited before a stream | stage D; `git diff --stat a82d784216 HEAD -- .githooks .github tools` empty | `05` |
| 16 | the retro | stage G | `docs/retros/` |
| 17 | the six checks pass before the merge; the lint PASS | stage H | the hand-back |

## The suites

Every command was run in this worktree at stage A (16:28-16:31 UTC), with its output kept under `/workspace/tmp/m6-t10/baseline/`. The at-hash `hooks-test` was run from the export.

| Command | Exit | Summary | A FAIL would mean |
| --- | ---: | --- | --- |
| run `.githooks/hooks-test` (the worktree: the hash's hooks plus #696's marker refusal) | 0 | `PASS`, 41 `ok` lines: **29** `expect` results (refused/allowed) and 12 `says`/`silent` checks | a hook allowed a shape it exists to refuse, refused a clean one, or printed a value or a listed word |
| run `.qa-scratch/t10/at-hash/.githooks/hooks-test` (the hash; what the primary checkout runs today) | 0 | `PASS`, 38 `ok` lines: **27** `expect` results and 11 `says`/`silent` checks | the same, for the copy every lane's commits actually run |
| run `tools/register-check` | 0 | `667 IDs, each once; every citation in the live documents names a row` | a duplicate ID, a citation naming no row, a placeholder row, or (this branch's copy only, `f00ab3e163`; not the hash's) a decided row under the open table |
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

**F-33 — One of the two upstream release scripts (`generate-changelog.sh`) is two upstream commits behind (`76693a738d`, `71d8932b33`; stage A), `generate-release-body.sh` is identical, and nothing in this fork runs either.** *Draft: Low (Q4, Q6).* They are upstream-carried, and the merge of `upstream/next` is the build-engine area's.
- **Positive:** stage A's provenance; the callers table.

**F-34 — `pre-push:337` is `if true; then`, a conditional with no condition; its header still teaches `../rocknix.worktrees/` (F-32).** *Draft: Low. Q7.*
- **Positive:** the tree.

### Found by the second opinion, re-derived here at stage C

Each of these is a seat's claim (`second-opinions/gpt-audit.md` G-nn, `gemini-argon-audit.md` G-nn) that this lane constructed or re-read before it became a finding. The seats' claims that did not hold are in `04` § Second opinion.

**F-35 — The diff parser takes an added line for a file header when the hunk deleted a line beginning `-- `: a credential or a listed word on an added line beginning `++ b/` passes the pre-commit, and the push guard when it is gone at the tip.** *Draft: High. Q3. Both seats (gpt G-02, gemini G-01).*
- **Where:** `guard-lib:60`. A deleted `-- note` prints as `--- note` and sets `minus`, and `:73` (`/^-/ { next }`) never resets it. The added `++ b/...` prints as `+++ b/...`, matches `:64` and becomes the label `f`, and `next` skips it. No `unknown` or `orphan` is counted, so the scan does not refuse.
- **What this refutes:** `04` § Q3's *none that reaches it*. `hooks-test`'s case *a content line beginning ++* has no preceding `--- ` deletion and no `b/`.
- **Positive:** P15 (pre-commit rc 0 for both shapes; the hooks-test-shaped control rc 1; the push of the middle commit rc 0).

**F-36 — The push guard sets a new branch's range from the last commit `rev-list` prints, which is the oldest by date, not the root of what is new: a commit dated after one of its own children falls outside the range, and neither its lines nor its message are scanned.** *Draft: High. Q3. gpt G-04.*
- **Where:** `pre-push:249-251` (`oldest=... | tail -1`, then `range="${oldest}^..${local_sha}"`). Committer dates are the committer's to set, and a rebase or an `--amend` sequence can produce them.
- **Positive:** P15 (`rev-list`'s last is the child `D`; the parent `C`, whose message carries the stand-in word, is unscanned; rc 0).

**F-37 — An annotated tag's annotation is never scanned: the push guard reads the commits a tag points at, and `fork-wordlist.yml` does not run on tags.** *Draft: Medium. Q3. gpt G-05.*
- **Where:** `pre-push:234-310` (no `git cat-file tag` read) and `fork-wordlist.yml:10-13` (`push: branches:` only).
- **Positive:** P15 (rc 0).

**F-38 — A line carrying both a credential and a listed word prints the listed word: the credential scan runs first and redacts only its own match.** *Draft: Medium. Q3. Both seats (gpt G-07, gemini G-03).*
- **Where:** `guard-lib:98-100`, called first at `pre-commit:18`, `commit-msg:23` and `pre-push:304,307,309`. This breaks `guard-lib:12` (*a refusal names the file and the line, never the word*).
- **Positive:** P15 (`WORD-PRINTED`, with the stand-in word).

**F-39 — The credential patterns miss a lowercase assignment (`password = <a long value>`) and a JSON refresh token whose value carries `/` (a Google OAuth refresh token begins `1//`), which is the shape `rclone.conf` writes for a Google Drive remote.** *Draft: Medium. Q3. gemini G-02.*
- **Where:** `secret-patterns:8`. The assignment alternative is upper-case only, and the scans pass `ci=''`. The token alternative's value class has no `/`.
- **The bound on a fix:** a stream widens a pattern only with the constructed line it then catches *and* the line it must still pass (brief § 2's policy). `device-builds.md` and the docs carry lowercase prose about passwords, which a careless widening would refuse.
- **Positive:** P15 (rc 0 for both, built from pieces).

**F-40 — A listed word in a file's name passes every guard: the hooks judge a line after its label (`guard-lib:18-19`), and `forbidden-terms-check` reads file contents only.** *Draft: Medium. Q3, Q7. gpt G-08.*
- **Where:** a path is in the tree, and D-WORKFLOW-061 says the fork must not carry the words *anywhere*. The label rule exists for credentials (PL-026: a kernel patch's name carried the key shape), not for the wordlist.
- **Positive:** P15 (rc 0).

**F-41 — The push guard's `pr/*` base falls back to `origin/next`, which is the fork's `next` and holds the personal overlay: with no `upstream/next` in the clone, a `pr/*` branch carrying a personal path is compared against a base that has it, and the push is allowed.** *Draft: Medium. Q3. gpt G-06.*
- **Where:** `pre-push:216-223`. The header (`:28-29`) treats `origin/next` as a clean base.
- **Positive:** P15 (rc 0, with `docs/plan.md` on both).

**F-42 — `fork-worktree remove` always runs `git worktree remove --force`, whether or not `--force` was given, so a feature worktree's uncommitted edits and untracked non-build files are destroyed without the refusal plain `git worktree remove` would give.** *Draft: High. Q3. Both seats (gpt G-18, gemini G-07).*
- **Where:** `fork-worktree:198-201`. The tool's own refusal covers only `build.*`, `target`, `sources` and `release` (`:38`). The rules send every agent to this tool *instead of* `git worktree remove --force` (`worktrees.md` § Removing a worktree).
- **Widened by the seats on F-11 and F-12**, with each piece re-read at its line:
  - preserving into a directory inside the worktree succeeds and is then removed with it (gpt G-15);
  - `mv` onto an existing name overwrites it (gpt G-16);
  - `repair` ignores a failed `mv` before its `rm -rf` (gpt G-17, gemini G-09);
  - `remove` and `repair` call git in the caller's repository, not `ROOT` (gpt G-19, gemini G-09).
- **Positive:** the tree. `:201` carries `--force` unconditionally.

**F-43 — The two readers of a dated audit folder disagree on its date format: `lint-audit-artifacts` matches underscores (`:144`), `ceremony-check`'s folder clock hyphens (`:364`), and all 23 folders use underscores.** *Draft: Low. Q7, Q6. gemini G-12, G-16; gpt G-39.*
- **Effect:** `ceremony-check`'s folder branch never fires, and the lint's current-contract test would skip the review-plan checks on a hyphen-dated folder.
- **What the seats got wrong:** gemini said the folders use hyphens. None does.
- **Positive:** P16.

**F-44 — `ceremony-check` accepts a completion marker whose receipt says `"exact_bodies_and_states": "false"` (any truthy string) or whose issue body has an unticked `* [ ]` checkbox, and an `Audit:`-titled issue resets the audit clock without a marker.** *Draft: Medium. Q3. gpt G-28; gemini G-16.*
- **Where:** `ceremony-check:118-129` (`not receipt.get(...)`, and the `^\s*- \[ \]` test only) and `:359-362`.
- **Positive:** the tree.

### Leads not in this slice's paths

- **`tools/pkgcheck`** (T6's and T8's leads on #657: the heredoc `}` and Lua tables read as functions; the duplicate-function check across an `if`'s two arms) is not one of the 31.
  - It is upstream's tool, the build-engine area's.
  - The coordinator's ruling on #657 (16:57 UTC, answering this lane's question of 2026-10-24T16:54:17Z, issuecomment-6386952155): `pkgcheck` does not join this slice, and its two leads are **bug #928** under #800.
  - They stay here as out-of-path leads pointing at #928, and are not graded.
  - T8's row's other half, `fork-package-freshness`, is this slice's: F-09.

## Coverage

One row per path. A cell names the finding or says `none` with what was read; `n/a` carries its reason.

| Path | Q1 Modernize | Q2 Standards | Q3 Bugs | Q4 Currency | Q5 Efficiency | Q6 Dead ends | Q7 Clarity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.githooks/commit-msg` | none (bash, `pipefail`) | fails closed on every read (`:8-15`) | F-03 | n/a: no pin | one grep pair per commit | run by git; no case for `-m` `#` lines | header true but for F-03's assumption |
| `.githooks/guard-lib` | none | fails closed (`:14-22`); sources its lists (`. "${f}"`) | F-35, F-38, F-40; F-01 (no `--text` in its callers); redaction proven with a `/` in a class (P3b) | n/a | one awk per diff | sourced by three hooks | header claims *no path is exempt* against F-02 |
| `.githooks/hooks-test` | none | fixtures built at run time (`:13-16`) | none of its own; it has no case for F-01, F-02, F-03, F-10 | n/a | 0.71 s (16:47Z) | nobody runs it automatically (`04` § Q6) | case count 29/27, not the brief's 22/20 |
| `.githooks/pre-commit` | none | fails closed | F-01, F-02, F-35, F-38, F-39, F-40 | n/a | one diff of the index | run by git | the marker refusal is on lane branches only |
| `.githooks/pre-push` | F-32 (`:7,11,381,416`) | `pipefail`; `|| true` swallows the console-first diff's failure (`:456-459`) | F-01, F-02, F-10, F-16, F-35, F-36, F-37, F-41 | n/a | P3: 0.07 s to 9.82 s | the index warning only warns | F-34; header's *proven* refusals true (P1 controls) |
| `.githooks/secret-patterns` | none | one definition (`:8`), 15 alternatives | F-39 (P3b: the redaction survives its slash) | n/a | n/a: data | sourced | true |
| `.github/scripts/generate-changelog.sh` | n/a: upstream's | upstream's | a bad range gives an empty changelog, rc 0 (R3) | F-33 | n/a | F-33: never run here | upstream's |
| `.github/scripts/generate-release-body.sh` | n/a: upstream's | upstream's | ignores the changelog's exit (R3) | identical to `upstream/next` | n/a | F-33 | upstream's |
| `.github/workflows/fork-checks.yml` | `actions/checkout@v4`, `ubuntu-24.04`: current | read-only permissions | F-06 | the pins named | 2 min 41 s a run | n/a: runs daily | header lists five checks of eight steps |
| `.github/workflows/fork-generic-x64.yml` | n/a | `if: ${{ false }}` | none | n/a | none | disabled on purpose (D-WORKFLOW-119/120) | header says so |
| `.github/workflows/fork-mirror-build-container.yml` | `ubuntu-latest` floats (F-31) | F-31 | none: the digest is checked (`:48`) | `skopeo` from apt, unpinned | n/a | dispatch only | true |
| `.github/workflows/fork-wordlist.yml` | `checkout@v4` | `pipefail` in its message step | F-30 (fifty messages on a new branch); F-37 (no tags) | the pins | not read | n/a | header true |
| `tools/archaeology` | F-32 (`:221`) | always exit 0 | F-20 | n/a | 15 git hits a term, unannounced cap | rules only | header says `-S`; code uses `-G` |
| `tools/box-check` | none | `gh` failure exits 1 (`:53`) | F-04 | n/a | one GraphQL call, 2 s | CI, ceremony, preflight | header true for 300 |
| `tools/ceremony-check` | none | F-05's uncounted reports | F-05, F-15, F-16, F-43, F-44 (and #905's fixed reader) | n/a | 7.95 s with `box-check` (2.02 s of it), core 4,925 → 4,924 (16:47Z) | CI, push guard, preflight | `--no-gh` still runs `box-check` (`:18`, `:344`) |
| `tools/es-menu-map-check` | none | exits 2 when it cannot run | F-21 | n/a | reads one pin | `vm-qa` | docstring's *not merely mention* against shape 6 |
| `tools/forbidden-terms-check` | none | fails closed on the list | F-07 | n/a | 147 s for the tree, one grep a file | CI only | `--help` is a tree named `--help` |
| `tools/fork-package-freshness` | none | `eval`s recipe lines (`:136`) | F-09 | it is the currency tool | network per recipe | `rc-preflight` | header's *fork-added* set is a two-tree diff |
| `tools/fork-worktree` | F-32 (`:9,72,74`) | F-14 | F-11, F-12, F-13, F-42 | n/a | `du` capped at 10 s | rules; `pr-stack-check` | `remove` uses the cwd's git, against its header (`:27-31`) |
| `tools/lint-audit-artifacts` | none | broad `except` ends in `bad()` | F-08, F-43 | n/a | small | `ceremony-check`, the skill | fixtures prove two checks at once |
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
| P15 | the seats' constructed cases: the parser's header state, the date-ordered range, a tag, both shapes on one line, the lowercase and slash-bearing credentials, a listed word in a name, the quoted personal `.po`, the `origin/next` base | proved: tool-run |
| P16 | the audit folders' date format | proved: tool-run |

## Stage E: the streams

Each stream is from `docs/reviews/briefs/t10-streams.md` at `9e0718eeb5`, with its tests run on the unfixed tool first. Every constructed input is a recipe (a stand-in list, `printf` pieces, a throwaway repository under `.qa-scratch/t10/`).

### S1: the diff reader (#929, #930, #931, #937, #938) -- `a00b0ac7bb`, `d55d34d6e1`

| Case (`.githooks/hooks-test`) | Unfixed (`8ebaf8daad`'s hooks) | Fixed |
| --- | --- | --- |
| a listed word in a file git treats as binary (#929) | FAIL: expected refused, exited 0 | ok: refused |
| a listed word in a binary-detected file in a middle commit, gone at the tip (#929) | FAIL: exited 0 | ok: refused, never prints the word |
| a listed word in a .po file (#930) | FAIL: exited 0 | ok: refused |
| an added '++ b/' line after a deleted '-- ' line is content, not a header (#931) | FAIL: exited 0 | ok: refused |
| a # line carrying a listed word, given with git commit -m, is refused (#938) | FAIL: exited 0 | ok: refused |
| a pr/* branch adding a personal path git quotes (#937) | refused, but *says "personal artifacts"* FAIL (refused only as unreadable) | ok: refused as a personal path |

`hooks-test`: PASS with 35 `expect` results and 51 `ok` lines (stage A: 29 and 41). The case that allowed a listed word on a `#` line now carries a clean one.

**The history read** (`tools/t10-history-scan.sh`, P18): over `c445081a59..8ebaf8daad`, the fixed reader with the real lists, counts and labels only:
- **Added lines:** 3 credential-shaped and 77 with a listed word. **Messages:** 1 and 3.
- **No hit is a guard escape.** Every commit carrying one predates the guard that would have refused it:
  - the wordlist guard is `3e70ef9239`, 2026-09-28T15:44Z;
  - the audit-packet exemption it removed covered the two seat diffs;
  - no message scan existed before it.
- **For the coordinator, by label** (commit:path:line, never the line):
  - **The credential lines:**
    - `9c9305eabf:tools/cloud-test-backend:27` (2026-08-22);
    - `46d7cd00b5:docs/audits/2026_09_28-milestone-audit-of-the-fix-round/seats/E-tests.diff:189`;
    - `d047546616:docs/audits/2026_09_28-milestone-audit-of-the-fixes-307/seats/E1.diff:142`.
  - **The credential message:** `06846da9ef:message:12`.
  - **The listed-word lines:**
    - 8 lines each in `46d7cd00b5`, `d047546616` and `cfb861dacd` (seat plans and stream briefs);
    - 23 in `437ebd09af`, 11 in `b3e5c92559`, 6 in `3f92ab553d`, 3 in `41b4071e92`, 3 in `df316365e6`, 2 in `25cd0cd7ff`, 2 in `a371bb77f8`;
    - 1 each in `4796a78983`, `62507a4d2f` and `9852981d72`.
  - **The listed-word messages:** `41b4071e92:message:11`, `a371bb77f8:message:3`, `a371bb77f8:message:4`.

  The full label lists are in `/workspace/tmp/m6-t10/history-s1/`. These lines are in pushed history; whether any is rewritten is the maintainer's, under #312's decision.

| Proof | What it shows | Proved |
| --- | --- | --- |
| P17 | S1's five cases fail on the unfixed hooks and pass on the fixed, and the suite stays green on the intermediate tree | proved: fix-case |
| P18 | the fixed reader over the fork's history: no guard escape | proved: tool-run |

### S2: the range, the base, tags, one redaction (#932, #937, #933, #934; D-WORKFLOW-200) -- `32cb3a903e`, `db8ad3958a`

| Case (`.githooks/hooks-test`) | Before (S1's hooks) | Fixed |
| --- | --- | --- |
| a listed word in a parent dated after its child, on a new branch (#932) | FAIL: exited 0 | ok: refused |
| a pr/* push with no upstream/next is refused, never judged against origin/next (#937) | FAIL: exited 0; *the fetch is named* FAIL | ok: refused, `git fetch upstream` named |
| an annotated tag whose annotation carries a listed word (#933) | FAIL: exited 0 | ok: refused, never prints the word |
| a line carrying a credential shape and a listed word (#934) | refused, but *the output carries "zebrafish"* FAIL | ok: refused, prints neither |

`hooks-test`: PASS with 39 `expect` results.
- **The empty conditional:** `if true; then` is removed, and its body runs as before. `d52e3d81c7` left it when the `-x` test moved up as a refusal.
- **`tools/fork-newdrive`** leaves `PERSONAL_PATTERNS` (D-INFRA-030).
- **The tags on `origin`:** 7, none annotated, so there were 0 annotations to scan. The brief expected 0 tags.
- **A deviation from the brief's file list:** the redaction fix is in `guard-lib`'s `guard_scan`, which all three hooks share.

| Proof | What it shows | Proved |
| --- | --- | --- |
| P19 | S2's four cases fail before the fix and pass after; the tags read | proved: fix-case |

### S3: two credential shapes; a listed word in a file name (#935, #936) -- `148cee2a31`

| Case (`.githooks/hooks-test`) | Before (S2's hooks) | Fixed |
| --- | --- | --- |
| a lowercase 'password = <a long value>' assignment (#935) | FAIL: exited 0 | ok: refused, the value never printed |
| a JSON refresh token whose value carries a slash (#935) | FAIL: exited 0 | ok: refused |
| a placeholder, a sentence and a short value still pass (#935's controls) | ok: allowed | ok: allowed |
| a clean file whose name carries a listed word, at commit (#936) | FAIL: exited 0 | ok: refused, the name never printed |
| a clean file whose name carries a listed word, at push (#936) | FAIL: exited 0 | ok: refused |

`hooks-test`: PASS with 44 `expect` results.

**For the coordinator (#935's third criterion):** the widened list matches these **10** tracked lines that the hash's list did not, by path and line, values never printed. The push guard's tip scan will refuse the next push that touches any of these files.
- **Four `rclone.conf.saved` files**, each with a `pass =` value of 36 mixed characters (rclone's obscured-password shape, the QA WebDAV backends'):
  - `docs/qa-logs/2026-10-06-pixelelated-replacement-15/qa19/artifacts/rocknix-images/qa-ed5a6a51f5-webdav-a-20261006-2003/time-to-play/rclone.conf.saved:6`
  - `docs/qa-logs/2026-10-07-pixelelated-replacement-16/qa-20/artifacts/rocknix-images/qa-ee01490913-webdav-a-20261007-0152/time-to-play/rclone.conf.saved:6`
  - `docs/qa-logs/2026-10-08-pixelelated-replacement-18/qa21/artifacts/rocknix-images/qa-7f58b7b1c5-webdav-a-20261008-1950/time-to-play/rclone.conf.saved:6`
  - `docs/qa-logs/2026-10-11-pixelelated-replacement-19/retained/artifacts/rocknix-images/qa-a0f60255ab-webdav-a-20261011-1841/time-to-play/rclone.conf.saved:6`
- **Two fixture literals in live tools**, against the run-time-fixture rule:
  - `tools/last-good-scripts-test:8004` (`Password=`, 25 characters);
  - `tools/cloud-connections-test:37` (`password='...'`, 24 lowercase letters).
- **Their copies:**
  - `docs/audits/2026_10_11-epic-m7-network-cloud-344/inputs/source/distribution/tools/last-good-scripts-test:7994`
  - `docs/audits/2026_10_11-epic-m7-network-cloud-344/inputs/source/distribution/tools/cloud-connections-test:35`
  - `docs/audits/2026_10_11-epic-m7-network-cloud-344/second-opinions/claude-brief.md:12960`
  - `docs/audits/2026_09_28-milestone-audit-of-the-fixes-307/seats/B.harness.txt:220`

**History, widened:** credential-shaped added lines rise from 3 to **15**. The 12 new ones are the lines above plus `46d7cd00b5:docs/audits/2026_09_28-milestone-audit-of-the-fix-round/seats/B.diff:2821`, `ce9f306c61:tools/last-good-scripts-test:6727` and `fed919f1c3:tools/last-good-scripts-test:3251` (labels only, `/workspace/tmp/m6-t10/history-s3/`). **File names:** 0 of 126,890 distinct paths ever added carry a listed word.

| Proof | What it shows | Proved |
| --- | --- | --- |
| P20 | S3's cases fail before the fix and pass after; the tree, history and name reads | proved: fix-case |

### S4: fork-worktree (#939, #940; D-WORKFLOW-201) -- `4b8419002d`, `0c0be666eb`, `d0c88f4528`

| Case (`tools/fork-worktree-test`, a throwaway repository) | The tool at `8ebaf8daad` | Fixed |
| --- | --- | --- |
| an uncommitted edit, remove without --force: refused; the edit is intact | FAIL: removed (rc 0), the edit destroyed | ok: refused (rc 128), intact |
| the same with --force: removed | FAIL (the worktree already gone) | ok |
| build output, no --force: refused by the tool; intact | ok | ok |
| --preserve to a directory the move cannot write: refused, the path named; nothing removed | FAIL: removed (rc 0) | ok |
| --preserve into the worktree itself: refused | FAIL (cascade) | ok |
| --preserve onto a name already there: refused, neither overwritten | FAIL (cascade) | ok |
| --preserve to a clean directory: moved, then removed | FAIL (cascade) | ok |
| --preserve with no directory: a usage error, exit 2, within a second | FAIL: rc 124 (the loop) | ok: rc 2 |
| remove from inside the target: refused | ok | ok |
| repair: re-registered; a file three levels deep, the build directory and a `..dotted` name are back; no orphan left | FAIL: the deep file and the `..dotted` name lost | ok |
| sync with one build worktree skipped for uncommitted changes: exit non-zero; all clean: exit 0 | FAIL: rc 0 | ok: rc 1, then 0 |

The control passes 19 of 19. **`rules-check` reports one failure since S2:** *hook missing tools/fork-newdrive*. The two rule entries' removal is the open question on #657 (T9's index row: *leaves with the hook's pattern (#657)*).

| Proof | What it shows | Proved |
| --- | --- | --- |
| P21 | S4's control fails on the unfixed tool and passes on the fixed, the intermediate commit's harness green | proved: fix-case |

### S2's follow-up -- `9f6c9b56f9`

The `tools/fork-newdrive` item in `fork-workflow.md` § Personal paths and its row in `instruction-files.md`'s index are removed, as the coordinator ruled at 18:30 UTC. `rules-check --quiet` exits 0; it had failed since `db8ad3958a`.

`register-check` reports `MISSING D-WORKFLOW-201` at `tools/fork-worktree:219` and `tools/fork-worktree-test:3` until the coordinator's branch, which carries the row, is merged in at hand-back.

### S5: the tracker readers (#941, #943) -- `66b08a6672`, `811e7f7d2f`

| Case | Unfixed | Fixed |
| --- | --- | --- |
| `box-check`: 458 open issues, a failing checkbox at 350 | FAIL: rc 0, 300 read | ok: rc 1, `FAIL  #650`, 458 read |
| `box-check`: a total of 473, a read of 458 | FAIL: rc 0 | ok: rc 2, `read 458 of 473` |
| `box-check`: the tracker does not answer | FAIL: rc 1 | ok: rc 2 |
| marker: a receipt with `"false"` as a string | FAIL: accepted | ok: refused |
| marker: a readback body with `* [ ]` | FAIL: accepted | ok: refused |
| the streamed digest equals `hashlib.sha256` (the 18:18 hunk) | FAIL: no helper | ok |
| a futro file dated 2099 | FAIL: the clock at 2099-01-01 | ok: none |
| only a heading that mentions a futro | FAIL: the clock at 2026-10-20 | ok: none |
| hygiene over 250 closed, an open checkbox at 230 | FAIL: `ok` (200 read) | ok: `DUE`, `#1770` named |
| hygiene with a total of 999, a read of 250 | FAIL: `ok` | ok: `DUE`, `read 250 of 999` |
| the tracker does not answer: futro and hygiene counted overdue | FAIL, FAIL | ok, ok |

**The live runs** at 18:33Z read all **507** open issues (1,568 open checkboxes, 0 fail) and every closed-completed issue since 2026-09-21, with no open checkbox among them. **Newly visible failing checkboxes for the coordinator: none.**

| Proof | What it shows | Proved |
| --- | --- | --- |
| P22 | S5's controls fail on the unfixed tools and pass on the fixed; the live full reads | proved: fix-case |

### S6: forbidden-terms-check (#942, #936) -- `34f32b28e6`

| Case (`docs/qa-logs/2026-10-24-forbidden-terms/run.sh`, stand-in list) | Unfixed | Fixed |
| --- | --- | --- |
| a clean tree with a symlink: 0 hits in 2 tracked files | FAIL: 1 file read | ok |
| a symlink whose link text carries a listed word: a hit | FAIL: rc 0 | ok: rc 1 |
| the hit is named by place, never by word | ok | ok |
| a clean file whose name carries a listed word: a hit | FAIL: rc 0 | ok: rc 1, `ls-files:<n>:name` |
| the name is never printed | ok | ok |
| a checkout whose tracked files are absent: exit 2 | FAIL: rc 0 | ok |
| a tree with no tracked files: exit 2 | FAIL: rc 0 | ok |
| --stdin, unchanged | ok | ok |

**The real run** (the real list, through the tool only): `0 hits in 133619 tracked files`, equal to `git ls-files | wc -l`, in 149 s. **No hit, so nothing goes to the coordinator.**

| Proof | What it shows | Proved |
| --- | --- | --- |
| P23 | S6's control fails on the unfixed tool and passes on the fixed; the real run's count equals the listed count | proved: fix-case |
