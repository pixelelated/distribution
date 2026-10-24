# Punch list (Phases 5 and 6) — M6.P2 T10, the guards (#657)

One item per finding of `02` (PL-nn for F-nn), with the severities graded in `04` § Second opinion. A `bug` carries every defect the coordinator has not held as a lead (D-WORKFLOW-187). Five bugs carry more than one item each: #937 (PL-41, PL-10), #940 (PL-42, PL-12, PL-13, PL-14), #943 (PL-05, PL-15, PL-44), #945 (PL-08, PL-43) and #957 (PL-27, PL-28, PL-29).

Every constructed input is a recipe, never bytes: a stand-in list, values built from `printf` pieces, a throwaway repository (the coordinator's 17:44 ruling). Every item answers *Can this be done on the VM?* No: the hooks, the tools and the CI run on the build host or on GitHub, and their proof is a suite, a fixture or a run record (brief § 5).

## PL-01: A file git treats as binary is never scanned in a diff: a credential or a listed word committed there passes the pre-commit, and the push guard too when it is gone again at the tip.
- **Severity:** High
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-01
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-01 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #929
- **Tracked:** #929

## PL-02: `.po` and `.pot` files are exempt from every hook scan.
- **Severity:** High
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-02
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-02 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #930
- **Tracked:** #930

## PL-03: `commit-msg` drops every line beginning `#`, but `git commit -m` keeps them, so a listed word or a credential on such a line passes the hook and is refused only at push, after it is in history.
- **Severity:** Low
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-03
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-03 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #938
- **Tracked:** #938

## PL-04: `box-check` reads `--limit 300` of the fork's 458 open issues, prints `0 fail` and exits 0; the CI step and `ceremony-check`'s `checkboxes` line read the same truncated answer.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-04
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-04 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #941
- **Tracked:** #941

## PL-05: `ceremony-check`'s hygiene line reads `--limit 200` of the 331 issues closed as completed since 2026-09-21, and a `gh` failure in its futro or hygiene line is reported but never counted.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-05
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-05 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #943
- **Tracked:** #943

## PL-06: In `fork-checks.yml` a failing step skips every step after it, so a red day hides the verdicts it did not reach: on 2026-10-19 to 10-22 the ceremony check never ran.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Source Finding:** F-06
- **Owner area:** the fork CI and its tools
- **Where:** `02-forward-audit.md` § Findings, F-06 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #944
- **Tracked:** #944

## PL-07: `forbidden-terms-check` skips every tracked symlink (180 in this tree) and never compares the count it scanned with the count it listed, so a checkout whose files are absent prints `0 hits in 0 tracke…
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-07
- **Owner area:** the fork CI and its tools
- **Where:** `02-forward-audit.md` § Findings, F-07 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #942
- **Tracked:** #942

## PL-08: `lint-audit-artifacts` bounds the seats' findings index with `str.find("## Verification")`, so a table cell quoting that heading ends the index early. In the 2026-09-28 fix-round audit, the cell at li…
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-08
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-08 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #945
- **Tracked:** #945

## PL-09: `fork-package-freshness` diffs two trees without their merge base and takes added files only.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-09
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-09 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #946
- **Tracked:** #946

## PL-10: The push guard's personal-path match reads `git diff --name-only` as given, so a path git quotes (a non-ASCII name under `docs/`) is not matched. Today such a push is still refused, by the tip scan fa…
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-10
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-10 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #937
- **Tracked:** #937

## PL-11: `remove --preserve <dir>` ignores a failed `mv` and then force-removes the worktree, destroying the build output it was told to keep.
- **Severity:** High
- **Category:** Data Safety
- **Question:** Q3
- **Source Finding:** F-11
- **Owner area:** `tools/fork-worktree`
- **Where:** `02-forward-audit.md` § Findings, F-11 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #939
- **Tracked:** #939

## PL-12: `repair` carries back only top-level entries that the fresh checkout does not have. Everything inside a tracked top-level directory (every untracked file under `docs/`, `tools/`, `projects/`) is then …
- **Severity:** Medium
- **Category:** Data Safety
- **Question:** Q3
- **Source Finding:** F-12
- **Owner area:** `tools/fork-worktree`
- **Where:** `02-forward-audit.md` § Findings, F-12 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #940
- **Tracked:** #940

## PL-13: `remove <path> --preserve` with no directory loops forever.
- **Severity:** Low
- **Category:** Data Safety
- **Question:** Q3
- **Source Finding:** F-13
- **Owner area:** `tools/fork-worktree`
- **Where:** `02-forward-audit.md` § Findings, F-13 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #940
- **Tracked:** #940

## PL-14: `sync` always returns 0, whatever it skipped or failed; its `rc` is never set.
- **Severity:** Medium
- **Category:** Data Safety
- **Question:** Q2
- **Source Finding:** F-14
- **Owner area:** `tools/fork-worktree`
- **Where:** `02-forward-audit.md` § Findings, F-14 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #940
- **Tracked:** #940

## PL-15: `ceremony-check`'s clocks can be reset or frozen by a marker that is not one.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-15
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-15 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #943
- **Tracked:** #943

## PL-16: The push guard's ceremony gate judges the primary checkout's working tree, not the tree being pushed.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-16
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-16 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** recorded; the next rung is the coordinator's
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** nothing on a device or in a cloud; a record or a hint, read where it is
- **Acceptance:** the disposition recorded on #657
- **Tracked:** the coordinator's recorded lead (#657, 16:57 UTC ruling: a contract question under D-WORKFLOW-028 and #258 PL-004; not a stream)

## PL-17: `register-check` does not see the second ID of a slash shorthand, reads seven live documents that cite IDs nowhere, and has T4's three gaps.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-17
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-17 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #947
- **Tracked:** #947

## PL-18: `rules-check`'s `mention` is a substring test, and it does not check that an index row's *Detail in* rule names the tool (T4's lead, 31 of 85 pairs at the hash).
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-18
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-18 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #948
- **Tracked:** #948

## PL-19: `work-log-index` indexes only `## ` headings; the 14 `### HH:MM UTC` entries at the hash are in no index, and `--check` passes.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-19
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-19 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #949
- **Tracked:** #949

## PL-20: `archaeology` never searches blindspots 1 to 29, which are table rows before the first `## N.` heading; a failed `git` or `grep` reads as zero hits, and the tool always exits 0.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-20
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-20 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #950
- **Tracked:** #950

## PL-21: `es-menu-map-check` sees a settings page only when its title is a `_("...")` literal: 22 of the 75 `new GuiSettings(` calls at the ES pin `16dbac5211` pass a computed title and are never checked.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-21
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-21 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #951
- **Tracked:** #951

## PL-22: `vocabulary-check` reads a hard-coded list of seven cloud scripts and `backuptool`.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-22
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-22 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #952
- **Tracked:** #952

## PL-23: `prose-check`'s sign-off pattern cannot match a sign-off followed by a space or the line's end, and its repeated-opener check computes and then `pass`es.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-23
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-23 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #953
- **Tracked:** #953

## PL-24: `release-catalog` parses `KEY value` with two or more spaces only, so a record written with one space loses its fields silently, and a kept folder with no `RECORD.txt` is reported nowhere.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-24
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-24 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #954
- **Tracked:** #954

## PL-25: `pr-stack-check` claims a stack whose last head equals `next`; the code resets every PR to the base and never compares a final tree.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-25
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-25 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #955
- **Tracked:** #955

## PL-26: `rc-preflight` accepts an acceptance line whose kind it never checks, against any decided row, and reads a bug's "Code trace" two ways.
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-26
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-26 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #956
- **Tracked:** #956

## PL-27: `renovation-inventory` rewrites `inventory.json` and `inventory.md` on a run whose counts disagree, before returning 1; its staged-path check compares counts, not sets; none of its subprocesses has a …
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-27
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-27 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #957
- **Tracked:** #957

## PL-28: `renovation-status`'s *Drift since* column prints the drift table's eighth cell, which is *Sensitive touched*; a closed slice reads `drifted` when any other slice in the ledger re-opens; and `closed` …
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-28
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-28 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #957
- **Tracked:** #957

## PL-29: `renovation-drift` reads `fixed_at` from `slices.json`, which no slice carries (0 of 46), while `renovation-status` reads the issue's field.
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q7
- **Source Finding:** F-29
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-29 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #957
- **Tracked:** #957

## PL-30: The CI scans no credential shape: `fork-wordlist.yml` checks the wordlist only, so a credential pushed with `--no-verify`, or from a clone without the hooks path, reaches GitHub with only GitHub's own…
- **Severity:** Medium
- **Category:** Security
- **Question:** Q6
- **Source Finding:** F-30
- **Owner area:** the fork CI and its tools
- **Where:** `02-forward-audit.md` § Findings, F-30 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** recorded; the next rung is the coordinator's
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** nothing on a device or in a cloud; a record or a hint, read where it is
- **Acceptance:** the disposition recorded on #657
- **Tracked:** the coordinator's recorded lead (#657, 16:57 UTC ruling: the CI half of D-WORKFLOW-061; not a stream)

## PL-31: `fork-mirror-build-container.yml:34` puts `${{ secrets.GITHUB_TOKEN }}` into a `run:` script by expression; GitHub masks it, but the documented form is an `env:` variable.
- **Severity:** Low
- **Category:** Security
- **Question:** Q2
- **Source Finding:** F-31
- **Owner area:** the fork CI and its tools
- **Where:** `02-forward-audit.md` § Findings, F-31 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** recorded; the next rung is the coordinator's
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** nothing on a device or in a cloud; a record or a hint, read where it is
- **Acceptance:** the disposition recorded on #657
- **Tracked:** a Renovation item with the coordinator's disposition pending (#657)

## PL-32: The legacy layout (#640) in twelve lines of the 31:
- **Severity:** Medium
- **Category:** Renovation
- **Question:** Q1
- **Source Finding:** F-32
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-32 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #640 (the legacy layout's cutover), with `fork-worktree:72,74`'s hint named first
- **Tracked:** #640 (the legacy layout's cutover), with `fork-worktree:72,74`'s hint named first

## PL-33: One of the two upstream release scripts (`generate-changelog.sh`) is two upstream commits behind (`76693a738d`, `71d8932b33`; stage A), `generate-release-body.sh` is identical, and nothing in this for…
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q4
- **Source Finding:** F-33
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-33 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** recorded; the next rung is the coordinator's
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** nothing on a device or in a cloud; a record or a hint, read where it is
- **Acceptance:** the disposition recorded on #657
- **Tracked:** the coordinator's lead for the build-engine area (the merge of `upstream/next`), and #585 for the empty-success paths as a contribution candidate

## PL-34: `pre-push:337` is `if true; then`, a conditional with no condition; its header still teaches `../rocknix.worktrees/` (F-32).
- **Severity:** Low
- **Category:** Renovation
- **Question:** Q7
- **Source Finding:** F-34
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-34 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** recorded; the next rung is the coordinator's
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** nothing on a device or in a cloud; a record or a hint, read where it is
- **Acceptance:** the disposition recorded on #657
- **Tracked:** a Renovation item with the coordinator's disposition pending (#657)

## PL-35: The diff parser takes an added line for a file header when the hunk deleted a line beginning `-- `: a credential or a listed word on an added line beginning `++ b/` passes the pre-commit, and the push…
- **Severity:** High
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-35
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-35 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #931
- **Tracked:** #931

## PL-36: The push guard sets a new branch's range from the last commit `rev-list` prints, which is the oldest by date, not the root of what is new: a commit dated after one of its own children falls outside th…
- **Severity:** High
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-36
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-36 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #932
- **Tracked:** #932

## PL-37: An annotated tag's annotation is never scanned: the push guard reads the commits a tag points at, and `fork-wordlist.yml` does not run on tags.
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-37
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-37 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #933
- **Tracked:** #933

## PL-38: A line carrying both a credential and a listed word prints the listed word: the credential scan runs first and redacts only its own match.
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-38
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-38 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #934
- **Tracked:** #934

## PL-39: The credential patterns miss a lowercase assignment (`password = <a long value>`) and a JSON refresh token whose value carries `/` (a Google OAuth refresh token begins `1//`), which is the shape `rclo…
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-39
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-39 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #935
- **Tracked:** #935

## PL-40: A listed word in a file's name passes every guard: the hooks judge a line after its label (`guard-lib:18-19`), and `forbidden-terms-check` reads file contents only.
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-40
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-40 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #936
- **Tracked:** #936

## PL-41: The push guard's `pr/*` base falls back to `origin/next`, which is the fork's `next` and holds the personal overlay: with no `upstream/next` in the clone, a `pr/*` branch carrying a personal path is c…
- **Severity:** Medium
- **Category:** Security
- **Question:** Q3
- **Source Finding:** F-41
- **Owner area:** the hooks: `.githooks/`
- **Where:** `02-forward-audit.md` § Findings, F-41 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #937
- **Tracked:** #937

## PL-42: `fork-worktree remove` always runs `git worktree remove --force`, whether or not `--force` was given, so a feature worktree's uncommitted edits and untracked non-build files are destroyed without the …
- **Severity:** High
- **Category:** Data Safety
- **Question:** Q3
- **Source Finding:** F-42
- **Owner area:** `tools/fork-worktree`
- **Where:** `02-forward-audit.md` § Findings, F-42 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #940
- **Tracked:** #940

## PL-43: The two readers of a dated audit folder disagree on its date format: `lint-audit-artifacts` matches underscores (`:144`), `ceremony-check`'s folder clock hyphens (`:364`), and all 23 folders use under…
- **Severity:** Low
- **Category:** Correctness
- **Question:** Q7
- **Source Finding:** F-43
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-43 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #945
- **Tracked:** #945

## PL-44: `ceremony-check` accepts a completion marker whose receipt says `"exact_bodies_and_states": "false"` (any truthy string) or whose issue body has an unticked `* [ ]` checkbox, and an `Audit:`-titled is…
- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q3
- **Source Finding:** F-44
- **Owner area:** the record checkers: `tools/`
- **Where:** `02-forward-audit.md` § Findings, F-44 (its file:line at `8ebaf8daad`, or `2174265e9c` for a `renovation-*` tool)
- **Ladder:** written (the tool's header or its rule claims it); next rung: audited, by the failing case the tracked issue's criteria name
- **Can this be done on the VM?** No: the tree, a suite run in a scratch repository, or the CI's record shows it
- **Already written:** the tracked issue's *Already written:* line
- **Acceptance:** the criteria of #943
- **Tracked:** #943

## Index

```yaml
punch_index:
- id: PL-01
  severity: High
  category: Security
  question: Q3
  source_finding: "F-01"
  tracked: "#929"
  outcome: "open"
- id: PL-02
  severity: High
  category: Security
  question: Q3
  source_finding: "F-02"
  tracked: "#930"
  outcome: "open"
- id: PL-03
  severity: Low
  category: Security
  question: Q3
  source_finding: "F-03"
  tracked: "#938"
  outcome: "open"
- id: PL-04
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-04"
  tracked: "#941"
  outcome: "open"
- id: PL-05
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-05"
  tracked: "#943"
  outcome: "open"
- id: PL-06
  severity: Low
  category: Correctness
  question: Q6
  source_finding: "F-06"
  tracked: "#944"
  outcome: "open"
- id: PL-07
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-07"
  tracked: "#942"
  outcome: "open"
- id: PL-08
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-08"
  tracked: "#945"
  outcome: "open"
- id: PL-09
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-09"
  tracked: "#946"
  outcome: "open"
- id: PL-10
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-10"
  tracked: "#937"
  outcome: "open"
- id: PL-11
  severity: High
  category: Data Safety
  question: Q3
  source_finding: "F-11"
  tracked: "#939"
  outcome: "open"
- id: PL-12
  severity: Medium
  category: Data Safety
  question: Q3
  source_finding: "F-12"
  tracked: "#940"
  outcome: "open"
- id: PL-13
  severity: Low
  category: Data Safety
  question: Q3
  source_finding: "F-13"
  tracked: "#940"
  outcome: "open"
- id: PL-14
  severity: Medium
  category: Data Safety
  question: Q2
  source_finding: "F-14"
  tracked: "#940"
  outcome: "open"
- id: PL-15
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-15"
  tracked: "#943"
  outcome: "open"
- id: PL-16
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-16"
  tracked: "the coordinator's recorded lead (#657, 16:57 UTC ruling: a contract question und"
  outcome: "open"
- id: PL-17
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-17"
  tracked: "#947"
  outcome: "open"
- id: PL-18
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-18"
  tracked: "#948"
  outcome: "open"
- id: PL-19
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-19"
  tracked: "#949"
  outcome: "open"
- id: PL-20
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-20"
  tracked: "#950"
  outcome: "open"
- id: PL-21
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-21"
  tracked: "#951"
  outcome: "open"
- id: PL-22
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-22"
  tracked: "#952"
  outcome: "open"
- id: PL-23
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-23"
  tracked: "#953"
  outcome: "open"
- id: PL-24
  severity: Low
  category: Correctness
  question: Q3
  source_finding: "F-24"
  tracked: "#954"
  outcome: "open"
- id: PL-25
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-25"
  tracked: "#955"
  outcome: "open"
- id: PL-26
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-26"
  tracked: "#956"
  outcome: "open"
- id: PL-27
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-27"
  tracked: "#957"
  outcome: "open"
- id: PL-28
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-28"
  tracked: "#957"
  outcome: "open"
- id: PL-29
  severity: Low
  category: Correctness
  question: Q7
  source_finding: "F-29"
  tracked: "#957"
  outcome: "open"
- id: PL-30
  severity: Medium
  category: Security
  question: Q6
  source_finding: "F-30"
  tracked: "the coordinator's recorded lead (#657, 16:57 UTC ruling: the CI half of D-WORKFL"
  outcome: "open"
- id: PL-31
  severity: Low
  category: Security
  question: Q2
  source_finding: "F-31"
  tracked: "a Renovation item with the coordinator's disposition pending (#657)"
  outcome: "open"
- id: PL-32
  severity: Medium
  category: Renovation
  question: Q1
  source_finding: "F-32"
  tracked: "#640 (the legacy layout's cutover), with `fork-worktree:72,74`'s hint named firs"
  outcome: "open"
- id: PL-33
  severity: Low
  category: Renovation
  question: Q4
  source_finding: "F-33"
  tracked: "the coordinator's lead for the build-engine area (the merge of `upstream/next`),"
  outcome: "open"
- id: PL-34
  severity: Low
  category: Renovation
  question: Q7
  source_finding: "F-34"
  tracked: "a Renovation item with the coordinator's disposition pending (#657)"
  outcome: "open"
- id: PL-35
  severity: High
  category: Security
  question: Q3
  source_finding: "F-35"
  tracked: "#931"
  outcome: "open"
- id: PL-36
  severity: High
  category: Security
  question: Q3
  source_finding: "F-36"
  tracked: "#932"
  outcome: "open"
- id: PL-37
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-37"
  tracked: "#933"
  outcome: "open"
- id: PL-38
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-38"
  tracked: "#934"
  outcome: "open"
- id: PL-39
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-39"
  tracked: "#935"
  outcome: "open"
- id: PL-40
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-40"
  tracked: "#936"
  outcome: "open"
- id: PL-41
  severity: Medium
  category: Security
  question: Q3
  source_finding: "F-41"
  tracked: "#937"
  outcome: "open"
- id: PL-42
  severity: High
  category: Data Safety
  question: Q3
  source_finding: "F-42"
  tracked: "#940"
  outcome: "open"
- id: PL-43
  severity: Low
  category: Correctness
  question: Q7
  source_finding: "F-43"
  tracked: "#945"
  outcome: "open"
- id: PL-44
  severity: Medium
  category: Correctness
  question: Q3
  source_finding: "F-44"
  tracked: "#943"
  outcome: "open"
```

## Phase 7 resolution gate

Pre-issue: every item is open until the coordinator's stage-E dispositions. Each row names what tracks the item.

| Item | Outcome | Tracked |
| --- | --- | --- |
| PL-01 | Open | #929 |
| PL-02 | Open | #930 |
| PL-03 | Open | #938 |
| PL-04 | Open | #941 |
| PL-05 | Open | #943 |
| PL-06 | Open | #944 |
| PL-07 | Open | #942 |
| PL-08 | Open | #945 |
| PL-09 | Open | #946 |
| PL-10 | Open | #937 |
| PL-11 | Open | #939 |
| PL-12 | Open | #940 |
| PL-13 | Open | #940 |
| PL-14 | Open | #940 |
| PL-15 | Open | #943 |
| PL-16 | Open | the coordinator's recorded lead (#657, 16:57 UTC ruling: a contract question under D-WORKFLOW-028 and #258 PL-004; not a stream) |
| PL-17 | Open | #947 |
| PL-18 | Open | #948 |
| PL-19 | Open | #949 |
| PL-20 | Open | #950 |
| PL-21 | Open | #951 |
| PL-22 | Open | #952 |
| PL-23 | Open | #953 |
| PL-24 | Open | #954 |
| PL-25 | Open | #955 |
| PL-26 | Open | #956 |
| PL-27 | Open | #957 |
| PL-28 | Open | #957 |
| PL-29 | Open | #957 |
| PL-30 | Open | the coordinator's recorded lead (#657, 16:57 UTC ruling: the CI half of D-WORKFLOW-061; not a stream) |
| PL-31 | Open | a Renovation item with the coordinator's disposition pending (#657) |
| PL-32 | Open | #640 (the legacy layout's cutover), with `fork-worktree:72,74`'s hint named first |
| PL-33 | Open | the coordinator's lead for the build-engine area (the merge of `upstream/next`), and #585 for the empty-success paths as a contribution candidate |
| PL-34 | Open | a Renovation item with the coordinator's disposition pending (#657) |
| PL-35 | Open | #931 |
| PL-36 | Open | #932 |
| PL-37 | Open | #933 |
| PL-38 | Open | #934 |
| PL-39 | Open | #935 |
| PL-40 | Open | #936 |
| PL-41 | Open | #937 |
| PL-42 | Open | #940 |
| PL-43 | Open | #945 |
| PL-44 | Open | #943 |
