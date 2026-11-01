# The reader's pass: `mini-retro` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/mini-retro/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

1. This skill works out what a finished phase taught: four fixed questions plus a scoped audit of about 30 minutes, each finding turned into an edit, issue or comment in the same session. A session should open it when a phase inside an Epic is code-complete, before the next kickoff or a hand-off.

2. Stumbles:

1. Order. SKILL.md 187-188 says "After Step 1 ... and Step 2 (writing the four questions)", but scoped-audit.md 4-5 says "before the four retro questions are answered". SKILL.md 163-164 has the audit feeding §3. Does the audit run before or after the questions?
2. Number of checks. scoped-audit.md 621 adds "Check 10 — Decision-propagation scan". The SKILL.md summary (199-252) and template.md 71-79 list nine checks, and the SKILL.md format (353-358) lists six. How many checks are there, and where does Check 10's verdict go?
3. "~5 spot checks" (SKILL.md 208; scoped-audit.md 183) sits above a table with eight rows (186-195). Which five?
4. "Optional." (SKILL.md 351; template.md 64) against "run the checks" (SKILL.md 271) and "All three are required" (582). Is the audit section optional?
5. "exactly these four sections. Do not invent new ones" (SKILL.md 152; template.md 5), yet the format adds four more sections. Which sections are allowed?
6. "captured in Step 7 below" (SKILL.md 461-462) appears inside Step 7, and nothing follows it. Also, Step 4 says "Write both" (320), but Step 7 (448-452) treats "Issue-comment milestones" and "Spec-doc milestones" as alternatives. Where is the full rule, and do addenda go to both homes?
7. Terms that are never defined: "PZ" (SKILL.md 269; scoped-audit.md 39, 703), "P7" (scoped-audit.md 318; template.md 105), "Outcome A / Outcome B" (scoped-audit.md 519-520, 576-577), "PL-06 / Z-3" (97), "page-scale mode" (SKILL.md 214). What do they mean?
8. "cornerstone violations" (SKILL.md 192) and "doctrine §1" (243) are not explained; line 8 only says "bedrock→cornerstone". What is a cornerstone here?
9. Which repo is this? The files say "scaffold" (SKILL.md 8, 220, 603) and also "pixelelated" (26, 597). scoped-audit.md 305-306 hard-codes `cd services/example-api && npx vitest run`, and 271 has ESM checks for `.ts` files. Is scaffold this repo, and what is its full-suite command?
10. scoped-audit.md 349 says "git stash", but the prerequisites require "commits landed" (SKILL.md 105). If the work is already committed, what does stashing do? And is a bare `stash pop` (358) safe if other sessions share the stash?
11. Two closing lists disagree. Step 5 (SKILL.md 396-407) includes filing follow-up issues and editing skills. template.md 139-150 "After writing" leaves both out and adds "Close the Mini Retro issue", a term never defined (also SKILL.md 434). Which list wins, and what is a Mini Retro issue?
12. "post an AC reconciliation comment **before** the closeout comment" (SKILL.md 204-205; scoped-audit.md 128-129). No step names a closeout comment. Which comment is it?
13. "confirmation steps below apply only when ... not already been authorized" (SKILL.md 32-33). The only one I found is "requires user approval" (428). Which steps are meant?
14. The description (line 3) says the retro runs "at Epic close", but SKILL.md 72-73 says "This skill covers the **Phase** tier. For **Epic** ... defer to the `code-auditor` skill". Lines 84-86 only partly settle this. At Epic close, do I run this skill, code-auditor, or both?
15. Smaller points:
    - "full 6-phase methodology" (SKILL.md 547-548) names only five phases.
    - "add to the running base rate" (scoped-audit.md 274): where is that rate kept?
    - "plan edits in §5 + investigations in §2" (272): which document's sections are these?
    - "reference/template.md" (71) does not match `references/`. Is that the same file?
