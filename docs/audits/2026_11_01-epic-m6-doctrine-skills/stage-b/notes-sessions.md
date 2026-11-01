# Stage B, the auditor's read: `session-resume` and `session-stash` (T38, #685)

Read at the dispatch tip's bytes, from the export, after the reader's pass (`reader-session-resume.md`, `reader-session-stash.md`). Line numbers are each file's at `87c2ab0fed`. Each note is a lead until its check line is run (`stage-b/checks-sessions.out`).

## session-resume/SKILL.md (121 lines)

- **L-09:** `:30` *"When the current branch is not `main`, ignore `saved-session-state-main.md`"*, and `:7`'s v1.2.0 note. This repository has no `main` (`worktrees.md`). To check: whether any `saved-session-state-main.md` is tracked.
- **New lead -- what a working branch's file is:** `:26` *"a working branch's own file is a pointer to it [the canonical `next` stash]. Read the canonical one"*. The renovation's lane pointers are not pointers: this lane's `.github/sessions/saved-session-state-feature-m6-doctrine-skills-685.md` carries the lane's whole state and says *"the executor updates this file at every checkpoint (#1014)"*. A session resuming a lane by this skill reads `next`'s stash -- T46's file, another lane's -- before the lane's own. To check: #1014 and any register row on lane pointers.
- **Q7, from the reader:**
  - `:42` *"`stat` the file"*, when `:26` reads the canonical one through `git show` and there is no file (item 6);
  - `:112` *"at ANY staleness tier, including `< 1 h`"*, with no tiers defined (item 7);
  - `:40` the `Branch:` check, which warns on every read of `next`'s stash from a lane (item 5);
  - `:45` *"(if referenced)"* against `:47` and `:105`'s every-resume tracker read (item 10).
- **L-14:** `:49` *"prefer the GitHub MCP tools (`mcp_github_search_issues`, `mcp_github_issue_read`). Avoid `gh` CLI list/search for bulk queries"*.
- **L-15's family:** `:112`, the production hardgate's examples (`tofu apply`/`import`, *"Caddy/Keycloak op"*), the source estate's stack.
- **Positives read:** `:44` the rules check against `next` (#367); `:86-101` continue the authorized work, never end on a menu (D-WORKFLOW-140); `:103-108` the snapshot's timestamp is not its authority; `:114-121` repository headings such as *Start here* are valid.

## session-stash/SKILL.md (163 lines)

- **L-09:** `:34-41`, the *"Shed inherited `main` state"* section, and `:7`'s note. This repository has no `main`, so the section's rule fires on nothing and its warning (*"`main` keeps editing its copy"*) describes another repository.
- **L-18:** `:28` *"you MUST move the old copy to `.github/sessions/archived/...` before overwriting -- this is the most-skipped step"*; nothing in `tools/` or `.githooks/` refuses an overwrite without the archive (R2 C24, re-read by the check below).
- **A delta against the brief's L-19:** `:32` **does** state the stranger's proof: *"then prove it by giving an agent with no context only the repository and asking it to resume."* The brief's v2 grep (`stranger|fresh|never seen|new agent|D-WORKFLOW-133`) did not include *no context*, and so reported *"the skill does not say it in other words either"*. The reader saw the sentence (item 3) and asked where its step is. The finding is narrower than L-19 states: the proof is a sentence in the *In this repository* paragraph, and none of Steps 1 to 3 carries it. Recorded beside the brief's line, not argued.
- **New lead -- "Use this exact template" without the section the repository requires:** `:32` requires the stash to open *"with a **Start here** section for an agent new to the project"* (`learning-capture.md` § 4, D-WORKFLOW-133). `:64` says *"Use this exact template"*, and the template (`:66-117`) has no *Start here*. A reader who follows Step 2 as written produces a stash `learning-capture.md` § 4 calls incomplete. Reader item 4. To check: the canonical stash on `next` opens with *Start here* (the sessions who wrote it followed the rule, not the template).
- **Q7, from the reader:** `:30` *"If the repo has a different convention ... prefer that"* against `:32`'s *In this repository* (item 5); `:38` *"rides the user-approved stash commit"* against `:126-128` *"do not request a repeated confirmation"* (item 8); `:92`'s third *Next Steps* item, a blocker to resolve first, listed third (item 10).
- **L-14:** `:57` the `mcp_github_*` names and *"Avoid `gh` CLI for list/search"*.
- **L-08's neighbour:** `:60` *"look for `docs/planning/<feature>/*-spec.md`, `specs/`, `RFCs/`"*: none exists here.
- **L-15's family:** `:141` *"so we can swap Keycloak for a test double"*.
- **Positives read:** `:49` *"run `date -u ...`; never guess the date"*; `:126-133` commit with the authorized work, update and read back the milestone (the fork's Step 3 items 4 and 5).

## What the checks settled (`stage-b/checks-sessions.out`, 03:11:25Z)

- **L-09:** no `saved-session-state-main.md` is tracked (`0` of the `20` state files under `.github/sessions/`); `334` archived stashes. The `main` rules fire on nothing here: dead text, not a wrong instruction (ruling (c): a punch item).
- **L-18:** `0` files under `tools/` or `.githooks/` name `saved-session-state` or `sessions/archived`.
- **The canonical stash on `next` opens `## Start here` at `:8`:** its writers followed `learning-capture.md` § 4, not the skill's exact template. Already written: the canonical stash is correct, so the template's gap has not reached it; a stash written by the template alone would lack the section.
- **The stranger's proof:** the sentence at `:32` came with `d8df0877a4` (2026-10-02, *"sessions, rules, skills: one stash on next for an agent new to the project"*), D-WORKFLOW-133's change. The brief's L-19 is corrected in `02`: stated, not stepped.
- **The lane pointers:** #1014 (OPEN, *"Backlog: a session-pointer freshness check -- two lanes' pointers lagged twelve and thirteen streams"*) is the record that lane pointers carry their lane's whole state. No register row says a working branch's file is a full state file, and `session-resume:26` says it is a pointer. A question for the coordinator at the pause (which text is right for a lane), not a bug filed by the lane.
