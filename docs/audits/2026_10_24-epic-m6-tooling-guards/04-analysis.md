# Analysis (Phase 4) — M6.P2 T10, the guards: hooks, the fork CI and the checkers (#657)

## Executive summary

The fork's guards do what their own suites say. `hooks-test` passes at the hash and in the worktree, and every refusal it constructs is refused. The record checkers pass on today's tree. The two lists that must agree (`PERSONAL_PATTERNS` and `fork-workflow.md` § Personal paths) agree entry by entry.

What the read found is one class, in eleven findings: **a checker that reads less than it reports, and passes**. The other findings around it are bugs of other shapes, Q6 gaps and Q1/Q7 rows.

**On the security list proper,** four High findings matter: F-01 and F-02 below, F-35 (the diff parser takes an added `++ b/` line for a header after a deleted `-- ` line) and F-36 (a date-ordered range boundary leaves the oldest pushed commit unscanned):
- **F-01, High:** a file git treats as binary is never diff-scanned, so a credential or a listed word committed there passes the pre-commit. It passes the push guard too when it is removed again inside the push.
- **F-02, High after the second opinion:** `.po` and `.pot` files are exempt from every hook scan, with no recorded reason.

**`fork-worktree`**, the tool whose contract is never destroying build output:
- **F-11, High:** `remove --preserve` force-removes after a failed `mv`.
- **F-42, High:** `remove` always passes `--force` to git, so uncommitted work outside the build directories is destroyed without a refusal.
- **F-12:** `repair` deletes every untracked file inside a tracked directory.

**The fork CI:** a failing step hides every verdict after it (F-06), and it carries no credential scan (F-30, a contract lead).

`02` carries **44 findings** (F-01 to F-44). F-35 to F-44 were found by the second opinion and re-derived here. After § Second opinion's grading:
- **6 High:** F-01, F-02, F-11, F-35, F-36, F-42.
- **25 Medium:** F-04, F-05, F-07, F-08, F-09, F-10, F-12, F-14, F-15, F-16, F-17, F-20, F-21, F-25, F-26, F-27, F-28, F-30, F-32, F-37, F-38, F-39, F-40, F-41, F-44. F-16 and F-30 are the coordinator's recorded leads, not streams (16:57 UTC ruling).
- **13 Low:** F-03, F-06, F-13, F-18, F-19, F-22, F-23, F-24, F-29, F-31, F-33, F-34, F-43.

The punch list's size is stage D's: an item may carry more than one finding, and a withdrawn lead carries none.

The draft grades in `02`'s headings are the first reader's; the outcome above is § Second opinion's.

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
| F-35 to F-44 | the seat's construction failing here | P15, P16 and the lines named in § Second opinion | confirmed (§ Second opinion) |
| R1–R4 leads not carried | — | R4's D2 withdrawn (the plan measures the same way); R1's AGENTS.md count withdrawn; the `secret-patterns` slash withdrawn (P3b) | withdrawn |

## Second opinion

**Depth: Extended** (D-WORKFLOW-184), with two reviewers from two labs other than the primary's (Anthropic), through the Facilitator on OpenRouter with `allow_fallbacks: false`. `second-opinions/review-plan.json` carries the plan; each output has its `.provenance.json` beside it.

| Seat | Probe | Refutation | Served | Verification |
| --- | --- | --- | --- | --- |
| `gpt` | 16:55, `READY unknown` (the provider's field is the identity) | 16:56:51 → 17:33:42, 37,745 bytes, `finish=stop`, first attempt | `openai/gpt-6-astra`, OpenAI, effort `max` | identity PASS (semantic, `provider_response`), effort PASS, provider PASS |
| `gemini-argon` | 16:55, `READY Gemini 4 Argon` | 16:56:51 → 17:04:49 (its start plus its 477,771 ms), 23,188 bytes, `finish=stop`, first attempt, under its 6,000-word bound | `google/gemini-4-argon`, Google, effort `high` | identity PASS, effort PASS, provider PASS |

**The packet:** one body of 479,616 bytes for both (`packet-manifest.json`: 39 sources with their sha256, the 31 files at their read refs among them, plus `fork-workflow.md`'s *Personal paths* and *Safety net* and `ceremonies.md`'s table from `next`). Gemini's ask was bounded (D-WORKFLOW-195).

**The packet's own scan, before it was sent:** both briefs gave `forbidden-terms-check --stdin` `0 hits on stdin` (rc 0), and 0 lines matched the pre-commit's credential patterns. Both outputs were scanned the same way before they were read: 0 and 0.

### What the seats found, and what decided each

Constructed claims ran in `tools/t10-guard-gaps-2.sh` (P15), with a stand-in list and a throwaway repository; the rest were re-read at the line the seat named.

| Seat claim | Verdict | Decided by |
| --- | --- | --- |
| gpt G-02 / gemini G-01: the parser's header state | **confirmed, High: F-35** | P15 (rc 0 twice; the control refused) |
| gpt G-04: the date-ordered range boundary | **confirmed, High: F-36** | P15 |
| gpt G-05: an annotated tag | **confirmed, Medium: F-37** | P15; `fork-wordlist.yml:10-13` |
| gpt G-07 / gemini G-03: both shapes on one line print the word | **confirmed, Medium: F-38** | P15 (`WORD-PRINTED`) |
| gemini G-02: lowercase assignment; slash-bearing refresh token | **confirmed, Medium: F-39** | P15 |
| gpt G-08: a listed word in a file name | **confirmed, Medium: F-40** | P15 |
| gpt G-06: the `origin/next` fallback base | **confirmed, Medium: F-41** | P15 |
| gpt G-18 / gemini G-07: `remove` always forces | **confirmed, High: F-42** | `fork-worktree:201` |
| gpt G-15, G-16, G-17, G-19; gemini G-08, G-09: preserve into the worktree, overwrite, repair's failed `mv`, the caller's repository | **confirmed, folded into F-42** | `fork-worktree:188-238` read |
| gemini G-12, G-16; gpt G-39: the dated-folder conventions | **confirmed in part, Low: F-43**. Gemini's *folders use hyphens* is false (0 of 23) | P16 |
| gpt G-28; gemini G-16: the completion marker's truthy string, the `* [ ]` checkbox, the clock reset by an `Audit:` issue | **confirmed, Medium: F-44** | `ceremony-check:118-129,359-362` |
| gpt G-01: a credential hidden by history simplification across a merge | **refuted** | P15: refused (rc 1, `cred`) in both shapes |
| gpt (on Q6): `hooks-test`'s quoted-name push case may pass for the wrong reason | **refuted** | P15: refused with the `cred` tag as well as `unread` |
| gemini G-11: `register-check` has no `MISPLACED` | **narrowed: true of the packet's hash copy, not of this branch.** `MISPLACED` is `f00ab3e163`, on this branch, not on `next`; the CI on `next` runs the hash's copy without it. `02`, `03` and § Q6 now say so | `git diff 8ebaf8daad HEAD -- tools/register-check` (+17) |
| gpt G-10: SIGPIPE under `pipefail` in the assistant-name scan (`pre-push:388`) | **confirmed by reading, Low**: needs a message over the pipe buffer; folded into F-34's row | the line |
| gpt G-11 (= the Q2 note on `pre-push:456-459`), G-12, G-13; gemini G-04, G-05; gpt G-03, G-09, G-14, G-22, G-23 | **Low, recorded under the nearest finding** (F-34 for the push guard's shapes, F-07 for the list loaders). Each depends on a configuration this repository does not set (`diff.external`, textconv, a submodule, an anchored list entry) or on the owner's own file | read; the configuration absent here |
| gpt G-24, G-25; gemini G-06: the CI reads the tip and the messages, not the history, and a clean `pr/*` branch carries no workflow | **confirmed, folded into F-30**, which the coordinator holds as a lead | `fork-wordlist.yml:27-40` |
| gpt G-26, G-27: the upstream scripts' empty-success paths | **confirmed by reading, Low, folded into F-33**: upstream-carried, and never run here; a contribution candidate for #585 | read |
| gpt G-29 to G-33; gemini G-17, G-18 | **folded into F-15** (R1's leads 8, 10, 13 and G-31's epic limit) and **F-05** (the unasserted limits) | `ceremony-check:270-297,320-338,352,383,400` |
| gpt G-34, G-35; gemini (on F-17) | **folded into F-17** | `register-check:65-96` |
| gpt G-36; gemini G-24 | **folded into F-18** | `rules-check:65-96,114-125` |
| gpt G-37 | **folded into F-19** | `work-log-index:31-47` |
| gpt G-38, G-40, G-41; gemini G-13, G-14, G-15 | **folded into F-08**: this audit's own `02` has no `## Findings index`, so the seat-verification machinery does not read it either | `lint-audit-artifacts:182-213,279-336,379-385` |
| gpt G-42; gemini G-19 | **folded into F-21**: a title ending in `?` fails the trailing `\b` | `es-menu-map-check:144-153` |
| gpt G-43 to G-47, G-50; gemini G-21 | **folded into F-09** | `fork-package-freshness:46,54-62,95-103,132-136,153-164`; `rc-preflight:168-171` |
| gpt G-48, G-49; gemini G-22 | **folded into F-26**, re-graded Medium: `--limit 300` on both bug readers, unasserted | `rc-preflight:234-328` |
| gpt G-51 to G-53; gemini G-23 | **folded into F-25** | `pr-stack-check:75,104-159` |
| gpt G-54, G-55; gemini G-26 | **folded into F-23** | `prose-check:44-59,120-127` |
| gpt G-56, G-57; gemini G-20 | **folded into F-22**: `//` stripping eats URLs inside `_("...")` | `vocabulary-check:76-100` |
| gpt G-58 to G-72; gemini G-28 | **folded into F-27, F-28 and F-29**, which both seats re-grade Medium | the three tools' lines |

### The seats' re-grades of the first reader, and the outcome

| Finding | gpt | gemini | Outcome, with the reason |
| --- | --- | --- | --- |
| F-01 | agree High; narrow (type changes escape the tip scan too) | agree High | **High**, the narrowing added |
| F-02 | High | High | **re-graded High**: a credential stays at the pushed tip, and no CI scan exists (F-30) |
| F-06 | Low: an observability gap on a run already red, not a pass | agree Medium | **re-graded Low and removed from the class** (gpt's reason holds: a red run is not a pass); the class is now ten |
| F-09 | narrow: edited recipes are outside the tool's declared scope (*packages the fork introduces*, D-WORKFLOW-024) | agree | **narrowed**: the two-tree diff, the missing ref and the verdict misreads stand; the edited-recipe count is a scope question for the coordinator, not a defect |
| F-10 | Medium: a quoted personal `.po` path composes the two gaps into an allowed push | — | **re-graded Medium**: P15 shows the allowed push |
| F-14, F-15 | Medium | — | **re-graded Medium** |
| F-16 | agree; widen (`ref='next'` at `ceremony-check:171`) | agree | **Medium, widened**; a lead for the coordinator, as ruled |
| F-17 | narrow (the hash copy has no `MISPLACED`) | narrow | **narrowed**, as above |
| F-20 | narrow: exit 0 after a *successful* empty search is right; after an unread one it is not | agree | **narrowed** |
| F-25 | narrow: the reset to `BASE` implements D-WORKFLOW-079's one commit per PR; the header is stale, not the algorithm. The `--force` fallback and the rename gap stand | agree | **narrowed** |
| F-26, F-27, F-28 | Medium | F-27, F-28 Medium | **re-graded Medium** |
| F-30 | — | Medium | **Medium**, held as the coordinator's lead |
| F-32 | — | Medium for the hint into the legacy checkout | **re-graded Medium for `fork-worktree:72,74`**; the other lines stay Low under #640 |
| F-33 | the heading overstates (only `generate-changelog.sh` is behind) | — | **wording corrected** |
| `03` § 3.3 | *no checker asserts completeness* is false: `renovation-status:77-84` and `renovation-inventory:943-946` refuse a saturated list, and `rules-check` compares sets | — | **corrected**: the technique exists in three places and is missing in the rest |
| § Q6 | omissions (commit-count failure, zero commits, `guard_scan`'s run-time grep failure, the message's temp-file and numbering failures, `rules-check`'s `always`, `fork-worktree`'s inside-the-worktree and permission refusals); `mktemp` is constructible with an unusable `TMPDIR` | omissions (the mirror workflow's digest refusals, `ceremony-check`'s marker and coverage refusals, `register-check`'s UNREADABLE, the renovation refusals) | **added to the table**; the `mktemp` row corrected |
| § Q3 | `guard_added_lines` cleared wrongly; the receipt, blindspot, coverage and RC readers missed | the same, plus the per-tool readers | **corrected**: F-35 replaces the *none*, and the missed readers have rows |

**What the seats could not judge** (gpt § 3, gemini § 3): the real wordlist (never in the packet); the effective git configuration; the counts behind P4 to P14, whose artifacts were not in the packet; #905's diff; and the destructive paths as runs. The last is this lane's limit too: F-11, F-12 and F-42 are confirmed by reading, and their fixtures in a throwaway repository are the bugs' acceptance (the coordinator's 16:57 ruling).

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
| `guard_added_lines`'s diff parser | `guard-lib:57-81` | **an added `++ b/...` line after a deleted `-- ` line in the same hunk** is taken for a header and skipped (F-35, both seats). This stage-B row first said *none that reaches it*; the second opinion refuted it, and P15 shows it. A binary file sends the parser no lines at all (F-01) | P15 |
| `forbidden-terms-check`'s file loop | `:37`, `:46-50` | the 180 tracked symlinks; a checkout with its files absent passes as `0 hits in 0 tracked files` (F-07) | P1, P6 |
| the lint's index boundary and YAML reader | `:182`, `:351` (hash) | a table cell quoting `## Verification`; an indented `punch_index` (F-08) | P10 |
| `archaeology`'s blindspot reader | `:76-91` | blindspots 1 to 29 (F-20) | P9 |
| `es-menu-map-check`'s screen patterns | `:50-56` | the 22 computed titles (F-21) | P12 |
| `fork-package-freshness`'s set | `:91`, `:163` | 22 upstream deletions in and one fork addition out; a missing base ref (F-09). The 63 edited recipes are outside its declared scope (D-WORKFLOW-024), narrowed by the second opinion | P14 |
| `commit-msg`'s comment filter | `commit-msg:11` | a `#` line given with `git commit -m` (F-03) | P1 |
| `pre-push`'s range and message readers | `:249-251`, `:265` | the parent of a child dated earlier than it (F-36); an annotated tag's annotation (F-37). `msgawk` keeps every message line: none | P15 |
| `fork-wordlist.yml`'s range reader | `:35-40` | intermediate commits' lines; a new branch's 51st message; a tag (F-30, F-37) | tree |
| `ceremony-check`'s completion-marker, blindspot-guard and coverage readers | `:85-130`, `:320-338`, `:171-200` | a receipt's truthy-string flag and a `* [ ]` checkbox (F-44); a heading the splitter misses and a guard path that always exists (F-15); a commit back-dated past the baseline (`%ct`, F-15) | tree |
| `rc-preflight`'s bug and trace readers | `:234-328` | the bugs past `--limit 300`; a bare *Code trace* heading or *Already written:* line (F-26) | tree |

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
| `pre-commit` | `mktemp` failing | **none**; constructible with an unusable `TMPDIR` (gpt's correction) |
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
| `register-check` (this branch only) | MISPLACED | its constructed failure, 2026-10-23 work log `:250` (#646); `f00ab3e163` is on this lane's branch, **not at the hash and not on `next`**, so the CI on `next` does not run it (gemini G-11's narrowing) |
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
| the `renovation-*` tools | counts disagree; re-open; a bare `**`; a changed ignored set; a credential match; a retired `gate` field; an oversize or empty slice | `--self-test` for parsing; **none** for the count assertions and the other refusals (F-27) |
| `pre-push` | `rev-list --count` failing; zero commits on `pr/*`; the personal-path diff failing | **none** |
| `guard_scan` | grep failing at run time (rc > 1), not at compile | **none** |
| `commit-msg` | the temp file, the filter and the numbering failing | **none** |
| `rules-check` | `always` (a no-`paths:` rule not saying so) | **none found** |
| `register-check` | UNREADABLE (a top-level `LIVE` path) | **none found** |
| `ceremony-check` | the completion marker refused; issue coverage | the #540 marker controls (`ceremonies.md` § The completed-audit marker); **none found** for coverage |
| `fork-worktree` | inside the target worktree; the permission preflight's refusals | **none found** |
| `fork-mirror-build-container.yml` | an unpinned source; a digest mismatch | **none** (dispatch only) |
| `fork-wordlist.yml` | a listed word in the tree; in a message | its green runs show the pass; **none recorded** for a red one |

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
