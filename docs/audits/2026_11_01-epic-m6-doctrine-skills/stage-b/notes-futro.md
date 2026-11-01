# Stage B, the auditor's read: `futro` (T38, #685)

Read at the dispatch tip's bytes, from the export, after the reader's pass (`reader-futro.md`). Line numbers are the file's at `87c2ab0fed`. Each note is a lead until its check line is run (`stage-b/checks-*.out`).

## SKILL.md (484 lines)

- **L-08:** Step 4 (`:379-388`) gives the futro two homes -- a spec's `### Futro: Phase N` placeholder and a comment on the Epic -- and neither is `ceremonies.md`'s marker (`docs/futros/<date>-<scope>.md`, or a work-log heading that says futro). The 17 entries of `docs/futros/` were written from the rule, not from this skill.
- **L-13 confirmed by reading:** `:479` *"discover via `gh api repos/{owner}/{repo}/issues/{number}/comments --paginate ..."*. `gh` fills `{owner}/{repo}` from the checkout's default repository, which `issue-tracking.md` says is the upstream remote, and upstream has Issues disabled. To check: `gh repo set-default --view` in the lane's worktree, a read.
- **L-14:** `:79-81` (`mcp_github_issue_read` and four more), `:112` (`mcp_github_issue_read on the parent epic + get_comments`).
- **L-17:** `:480` *"Blindspot register (when created) conventionally lives under `docs/`."* and `:433-435` *"Copy it to your project's docs directory ... when your first futro surfaces a blindspot"* -- `docs/blindspot-register.md` has existed since well before this skill was read; its last numbered heading is `## 76.`.
- **L-22:** `:3`, in the description every session lists, *"(e.g. begin-exploration) deliberately does NOT invoke it"*; `:457`.
- **New lead -- a command that cannot run here, in a MUST:** `:207-230`, the *"Base-divergence check"* -- *"the Step-1 inputs MUST include a divergence check against the integration target: `git fetch origin main` then compare ... on `origin/main`"*, and the question-1 sentence it requires (*"this branch is N commits behind `origin/main`"*). This repository has no `main` (`worktrees.md`: `origin` and `upstream` both default to `next`), so the fetch fails, and for a renovation lane a fetch is itself forbidden. The same family as L-09 (`saved-session-state-main.md`). To check: `git rev-parse --verify origin/main`.
- **L-15's family, the verification mandates (`:131-230`):** written against the source estate.
  - Each cites its incidents by the source estate's names: *"P5+P7+P8 retros"*, *"#2545 Phase B AD11"*, *"E253 retro ... deferred PL-04 of audit #203"*, *"scaffold#246; Birdwork BS-5"*, *"M64 P1.5 E2/E3/E5/E4"*.
  - `:179` names a placeholder tool, *"`node scripts/<the platform probe> verb ...`"*, and `:199-200` a path in another repository, *"`docs/planning/m55-platform-contract-surface/...`"*.
  - Their *rules* (grep before a count, inspect the artifact, verify a hash by command) are this repository's practice too (`engineering-practices.md`). Their *origins* name nothing here (reader item 3).
- **A citation to register sections this tree has not:** `:141-143` *"blindspot register § "Schema-`required[]`-enumeration miss""*, `:258-259` *"blindspot-register § "Substrate-precondition assumption inherited from issue body" ... (Epic #2647 / S1 #2648)"*. To check: both headings in `docs/blindspot-register.md` and in this skill's starter template. Reader item 5.
- **New lead -- "Apply four techniques", then five:** `:288` *"Apply four techniques, in order of primacy"*, followed by agent-execution simulation, pre-mortem, blindspot check, the replaced-mechanism archetype and the honesty check. `techniques.md` says four and `template.md` three (to read). The replaced-mechanism bullet is the fork's (`:318` *"Origin: 2026-09-04, rocknix"*, blindspot 23). To check: `git log -S'Replaced-mechanism archetype'` -- a fifth added without the count, as at L-02.
- **Q7, two thresholds:** `:339-341` *"promoted at 2 instances per the E4 retro's threshold"* against `:462-464` *"Rule of three ... promote it to the blindspot register"*, and `:430-431` *"Each futro that surfaces a NEW blindspot adds an entry."* Reader item 6.
- **Q7:** `:401-409`, *"the futro spec edit + Epic comment MUST be committed BEFORE the first task-execution commit"*: a tracker comment is not committed (reader item 9). `:411-413` uses `begin-delivery`'s step numbers inside this skill's own Step 5 (item 14).
- **L-05's neighbour:** `:377` *"factor 1.5× time"*, inside the *Specific* column's example. It is a time multiplier, not a duration, so the widened pattern cannot reach it; recorded with L-05 for the stream to read.
- **L-16:** `:8`, the origin note; the description is 909 characters by R2's count (Q5).
- **Q7, the duplicate:** `:26-35` *pixelelated continuation* = `mini-retro/SKILL.md:26-35`, byte for byte (`stage-b/checks-mini-retro.out`).
- **Positives read:** `:232-235` *"A futro written without reading the plan is worse than no futro"*; `:313-322` the replaced-mechanism archetype (the fork's, sound); `:466-480` the fork's integration paragraph naming the rules that exist.

## references/techniques.md (320 lines)

- **The techniques, two different fours:**
  - `:3-5` *"Four complementary techniques, ordered by primacy. Run them all"*. Its four are simulation (`:9`), pre-mortem (`:196`), blindspot check (`:235`) and pattern analysis (`:264`). `:264` then says pattern analysis is *"used for question 3, not question 4"*, so question 4 gets three.
  - `SKILL.md:288`'s "four" are five, and a different five.
  - Reader items 1 and 2.
- **L-21:** `:28` *"Fresh-context AI agent (Crush, Claude Code, Copilot)"*, `:35` *"via `/copilot` or similar"* (the Copilot surface `instruction-files.md` says is gone).
- **L-15's family:**
  - `:94-121`, the network-reachability what-ifs (Key Vault, OpenBao, `tofu apply`, `bypass = "AzureServices"`, *"the Three-Axis Grant Integrity reframe"*);
  - `:123-142`'s origin (*"Epic #2373 mini retro ... Maven"*);
  - `:63` `capability_type`, `:223-231` the XRI example, `:293-304` `services/example-api/src/a2a/capability-helpers.ts`.
- **L-58's family:** `:167` and `:230` *"#1558"*, `:177` and `:300-302` *"#1556"*, `:138` *"Epic #2373"*. All three are above this tracker's 1385 and resolve to nothing here (`stage-b/checks-futro.out`). An earlier version of this note said the two below 1385 would name other issues here; 1556 and 1558 are not below 1385, and that note was wrong. The sharp case is in `SKILL.md`, below.
- **Positive:** `:180-192` *"name the specific agent archetype you simulated ... If you can't name the archetype, you simulated a fictional perfect executor"*.

## references/template.md (143 lines)

- **L-08:** `:3-4` *"Copy this into the spec document phase section AND into the Epic issue comment"*; `:138-143`'s *After writing* names neither `docs/futros/` nor a work-log heading.
- **Q7, the heading levels:** `:10` `## Futro:` (H2) and `:20` `### 1. What do we know ...` (H3), against `SKILL.md:384`'s `### Futro: Phase N` placeholder and `:192-206`'s mandate that a futro match its siblings' heading convention -- which in the source estate was `## N — ...` (H2) and failed on `### N.` (reader item 4).
- **Q7:** `:68` *"Primary technique: agent-execution simulation. Complementary: pre-mortem, blindspot check."* -- three, the third count. `:32-34`'s **Confidence** line has no instruction in `SKILL.md` (reader item 7).
- **L-21:** `:72` *"A parallel-channel Copilot CLI agent handed #F as a background task"*.
- **L-15 and L-58's family:** `:46` `pg_advisory_xact_lock`, `:58` `example-api/secrets-lifecycle`, `:104` *"Added AC to #1558"*, `:109` `postgres.js`, `:114` *"external capability endpoints"*.

## references/blindspot-register.md (105 lines)

- **L-17, the template's fate:** a starter (*"Copy it to your project's docs directory ... when your first futro surfaces a blindspot"*, `:3-6`), with two illustrative entries and no table rows. The project's register exists (`docs/blindspot-register.md`, numbered headings to `## 76.` and a table) in a shape this starter does not have. It states the starter's job truly, so this is not a stale copy (R4 item 64's reading). Its first instruction, though, is one this repository finished long ago. What it costs (Q5): 105 lines, loaded only if opened; nothing loads it by itself.
- **L-05's neighbour:** `:77-78` *"multiply the estimate by at least 2× in question 1"* and `:74-75` *"run 50–200% over estimate"*: time estimates inside an example entry (D-WORKFLOW-091).
- **The sections `SKILL.md` cites** (`:141-143`, `:258-259`) are not in this starter: it has only *"<Example> Migration time is underestimated"* and *"<Example> Environment-specific configuration drifts silently"*.

## What the checks settled (`stage-b/checks-futro.out`, 03:10:12Z)

- **L-13:** `gh repo set-default --view` prints *"No default remote repository has been set"*. The checkout has three remotes (`origin`, `origin-https` -> `pixelelated/distribution`; `upstream` -> `ROCKNIX/distribution`), so `{owner}/{repo}` is filled by `gh`'s own resolution, which `issue-tracking.md` says lands on upstream, where Issues are disabled. **Not run:** resolving it by calling `gh api` would read another repository through `gh api`, which the never-run list forbids. The finding stands on the rule and the configuration, `proved: tree` with the read named; the sentence's fix is `--repo`-free `gh api repos/pixelelated/distribution/...`.
- **The base-divergence MUST:** `origin/main rc=1`, `main rc=1`; `origin/HEAD` is `refs/remotes/origin/next`. The block cannot run here as written.
- **The fifth technique:** *"Apply four techniques"* and the honesty check came with the import (`437ebd09af`); the replaced-mechanism archetype was added by the fork in `3624e2e329` (2026-09-04, *"docs: retro propagation -- D-CLOUD-026, the futro archetype, the claims rule"*), which did not move the count. The same shape as L-02.
- **The register sections `SKILL.md:141-143` and `:258-259` cite:** `0` in `docs/blindspot-register.md` and `0` in the starter. Dead references.
- **Another estate's issue numbers:** #1556, #1558, #2373, #2545, #2647 and #2648 resolve to nothing here. **And `SKILL.md:163-164`'s *"deferred PL-04 of audit #203"* resolves to this tracker's #203** (*"Launching a game while saves sync: ask to stop it and play, or keep waiting"*, CLOSED), which is not an audit. A reader who follows the citation reads an unrelated issue.
- **The futros' heading convention:** the six newest of `docs/futros/` use `## 1.` (H2) for question 1, so `template.md:20`'s `### 1.` would fail `SKILL.md:192-206`'s own pre-grep mandate.
