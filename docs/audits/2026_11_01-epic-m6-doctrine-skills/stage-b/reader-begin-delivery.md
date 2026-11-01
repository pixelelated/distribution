# The reader's pass: `begin-delivery` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/begin-delivery/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

The directory has one file, SKILL.md (619 lines), and I read all of it.

**1. What it decides and when to open it.** The skill decides whether an Execution Epic (work whose outcomes are fixed in advance) may start and what it starts with. Before tasks are loaded and the pre-flight checklist runs, it requires the prior retro, any Epic/Milestone audit, a settled punch list, a check of work already done, and a futro. A session opens it when the user asks to begin the next phase or epic, or right after a phase's mini-retro, but not for Discovery Epics.

**2. Where I stumbled**

1. Lines 13, 186, 201, 390: "next Execution Epic", "last phase of an Epic", "at each batch start". Is a phase an Epic, a part of one, or a batch? If every run starts a new Epic, does the signal on line 201 ("names a NEW Epic") fire every time?
2. Lines 32–35: "audit receipts", "Existing authorization remains effective". What is a receipt? What counts as prior authorization against the confirm/ask steps on lines 207, 249, 331, 386 and 501?
3. Line 207 vs line 212: "do not advance to Step 2 if the user defers" vs "the futro in Step 2 must include an explicit 'deferred upward-tier audit'". Does a deferral block Step 2 or not? And what is "the kickoff comment"?
4. Lines 209–210 vs 226–228 and 248: P0/P1 items "become inputs to the futro", yet Step 1.6 settles every item, fixing them by default, before the futro runs. What is left for the futro to use?
5. Line 237 vs line 594: "Phase 6 GitHub issue" vs "pairs with `code-auditor` Phase 7". Which is it? "Phase" here also clashes with the project's own phases.
6. Line 170 vs lines 518–519: "five phase-tier audit spot-check verdicts" vs "Step 2.5 Check 6". How is there a sixth check out of five?
7. Line 319 vs lines 86 and 93: "Phase N−1 didn't get one", while the diagram numbers the phases N and N+1. Does the single allowed skip (line 317) still need the approval asked for on line 330?
8. Line 401: the pre-futro audit is "run before invoking the `futro` skill at Step 2", but it is written inside Step 3 and is missing from the chain diagram (lines 98–116). Does it run before or after Step 1.7?
9. Lines 353, 361 and 410: the futro "signals ready", the notice comes "after the futro has updated the issue context", and the post-futro audit comes "before loading tasks at Step 3". Which runs first, the post-futro audit or Step 2.5?
10. Lines 476–490 vs line 585: Step 4 says "Do not let the gap travel into the granular task list", but Step 3 has already loaded that list, and line 585 says "before granular tasks load". Does this check belong before Step 3?
11. Line 392 vs lines 589 and 576–577: "lazy-drafting rule (this skill, v2.3.0)", but the 2.3.0 entry is the punch-list gate and the 2.5.0 entry says the lazy approach was "never merged". Line 436 still retrofits Epics "started under the lazy-drafting rule". Did that rule ever exist?
12. Line 390: "drafted **upfront** at Epic creation", but this skill runs at kickoff, not creation. Am I checking for those drafts here or creating them? Lines 408 and 416 say "comment on the sub-issue". Is that one comment per issue or one per batch?
13. Line 466 vs lines 614–617: "the repo's `.instructions.md`" vs the rule files listed later. Which file decides whether I confirm with the user or follow silently? On line 469, "Critical and foundational — the implications are far-reaching": what exactly am I ticking?
14. Terms used without definition:
   - "cornerstone" (lines 66, 470; the only hint is "bedrock→cornerstone" on line 8)
   - "R2" (line 68)
   - "Phase-1 prompt" (line 64)
   - "AC0" (lines 290, 310)
   - "micro-retro" (line 493): is it the same as mini-retro?
   - "M64.P1.5 E6 #2952" (line 59)
   - project names: "pixelelated" (line 28) vs "birdwork-preflight" and "scaffold" (line 8)
15. Line 23 vs lines 7 and 543: "origin: 2026-07-08" is later than the version (3.2.0) and the newest change-log entry (2026-06-09). There is also no 3.1.0 entry. Which version added the serial rule?
