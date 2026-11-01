# Stage B, the auditor's read: `begin-delivery` (T38, #685)

Read at the dispatch tip's bytes, from the export, after the reader's pass (`reader-begin-delivery.md`). Line numbers are the file's at `87c2ab0fed`. Each note is a lead until its check line is run.

## SKILL.md (620 lines)

- **L-05:** `:398` (`~10 min`, twice), `:429` (*"Cost: ~20 min/batch"*). **New, beyond the pattern:** `:256` *"they are usually <15min admin cleanups"* (`code-auditor/SKILL.md:612`'s twin).
- **L-16:** `:541-609`, a `## Change log` of 69 lines inside the procedure (R2 C26 counted `:541-610`, 70, with the blank line after it), ending `:609` *"Initial conversion from `.github/prompts/begin-phase.prompt.md`"*. Each entry cites the source estate's issues (`:559` M64.P1.5 E6 #2952, `:577` #2635, `:578` #2647/#2648, `:595` #2630, `:600` #2390).
- **L-22:** `:3` (the description, every session's listing: *"use a Discovery-Epic kickoff path (e.g. `begin-exploration`) instead"*), `:50`, `:68`, `:557`, `:562`.
  - Beside it, the hedge covers skills that **are** present: `:54` *"(e.g. a `council-research` skill, if present)"*, `:55` *"(e.g. a `council` skill, if present)"* -- both ship here.
  - And it covers ones that are absent: `:57` *"a `design-reviewer` skill, if present"*, `:80-82` and `:357-372` *"a `work-start-notice` skill"*.
- **L-14:** `:136-141` (`mcp_github_issue_read` and three more, *"Avoid the `gh` CLI for list/search operations -- bulk output has destabilised agent runners"*); `:154` `get_comments`; `:284` `mcp_github_search_issues`; `:384` `manage_todo_list` (the Copilot runtime's todo tool); `:440` `mcp_github_sub_issue_write method=add`. Against `issue-tracking.md`'s `gh api -X POST repos/.../issues/<epic>/sub_issues` for sub-issues.
- **L-12's family:** `:466` *"(or silently follow it if the repo's `.instructions.md` already codifies it)"* -- the Copilot-era file name for what is `.claude/rules/*.md` here (reader item 13).
- **L-15's family:**
  - `:193-194` and `:209` `logs/audits/` (here `docs/audits/`);
  - `:127-128` a prerequisite *"A spec / plan document exists for the feature (e.g. `docs/planning/<feature>/<feature>-spec.md`)"* -- no `docs/planning/` here, and `code-auditor/SKILL.md:708` says so;
  - `:403` *"re-query live state (Azure, DB, OpenBao, etc.)"*; `:484-487` `kcadm`, `psql`, `.well-known`;
  - `:66`, `:453`, `:470` *"cornerstone"* (reader item 14);
  - `:617` *"Grounding (doctrine + Accepted ADRs + development principles)"* (no ADR tier here).
- **A citation to a register section this tree has not:** `:491-492` *"(Origin: blindspot-register § "Substrate-precondition assumption inherited from issue body".)"* -- `0` matches in `docs/blindspot-register.md` (`stage-b/checks-futro.out`, the same heading futro cites).
- **L-58's family:** `:59` *"(from M64.P1.5 E6 #2952)"*, `:332` *"M26 P1 mini-retro 2026-05-08"*, `:444` *"2026-05-12 mid-Epic #2635"*, with the change log's numbers. None is this tracker's (its highest is 1385; #2952 resolves to nothing, `stage-b/checks-code-auditor.out`).
- **New lead -- a count true once:** `:168-171` *"a Mini Retro (as of `mini-retro` v2.0.0) includes a § Scoped audit findings subsection -- ... It contains the five phase-tier audit spot-check verdicts"*. `mini-retro` is at v2.7.0 with nine checks in its procedure and ten in its reference (`stage-b/checks-mini-retro.out`); `:518-519` itself cites *"Step 2.5 Check 6"*. Reader item 6.
- **Q7, an internal history that contradicts itself:** `:392` *"**Supersedes** the 2026-05-11 lazy-drafting rule (this skill, v2.3.0)"*, while the change log's 2.3.0 (`:589-594`) is the punch-list gate and 2.5.0 (`:573-577`) says the lazy approach *"was never merged"*. Yet `:436` retrofits Epics *"started under the lazy-drafting rule"*. Reader item 11.
- **Q7, from the reader:**
  - `:207` *"do **not** advance to Step 2 if the user defers"* against `:212-215`'s futro entry for a deferred audit (item 3);
  - `:209-210` P0/P1 items as futro inputs, after `:248`'s Step 1.6 has fixed them (item 4);
  - `:401`, the pre-futro audit, written inside Step 3 but run before Step 2 (item 8);
  - `:469` *"Critical and foundational -- the implications are far-reaching"*, a checkbox with nothing to tick (item 13).
- **Positives read:**
  - `:130-132`: the fork's rules take precedence over this skill for per-issue protocol.
  - `:265-311`, Step 1.7, the prior-work grounding against *assumed-undone*. This is the register's entry 1 (*"Assumed-undone"*, `docs/blindspot-register.md:10`, the brief's § 3 item 3) as a step.
  - `:317-334`: no silent futro skip.
  - `:28-37`: the fork's continuation section (`:34-35` *"Existing authorization remains effective"* is what reconciles `:501`'s *"Ask before committing"* with a lane's authorized commits).
- **Reachability (Q6, to be tabled):** the renovation plan names this skill nowhere and the 80 briefs on 0 lines (R1 § 7). What has run it, by record, is the Q6 generator's read of the work logs.
