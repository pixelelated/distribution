# The reader's pass: `code-auditor` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/code-auditor/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

I read all five files in full: SKILL.md (724 lines), references/phases.md (593), references/templates.md (348), references/anti-patterns.md (68) and references/review-levels.md (60).

**1. What the skill decides, as I understood it:** It decides, with evidence and a check from a second model, whether work claimed complete at an Epic or Milestone boundary (and maybe a single issue) really meets its stated acceptance criteria and project rules, and turns the gaps into a punch list, a GitHub issue and a gate on what happens next. A session should open it when work is claimed done and needs adversarial checking before merge, deploy or the next phase, but not at every phase boundary.

**2. Where I stumbled:**

1. SKILL.md 159–191: it says "Three hard rules", but the list is numbered 1, 2, 3, 4, 3. Line 370 and phases.md 60 then cite "Evidence floor rule 3". Which rule 3 is meant?
2. SKILL.md 77–79 says the skill "operates at two of the three" tiers, and the table has no Issue row. Line 92 then adds an "**Issue**" tier, and line 301 lists `issue` as a scope. Is Issue a tier of this skill or not?
3. SKILL.md 623 says the mode is "invoked by: … explicit user request". Line 665 says "Always run it for milestone-scope and epic-scope audits." Is it optional or mandatory?
4. SKILL.md 252 says "RUN `tools/lint-audit-artifacts`… This is not optional". phases.md 574–577 says "scaffold has none today, so verify … manually". Does the lint exist?
5. SKILL.md 252–256: the lint runs "Before Phase 6" with `--issue <n>`. It checks that "every punch item has a Phase 7 outcome" and that the issue has checkboxes, but Phase 6 is the step that creates that issue and Phase 7 records the outcomes. What order is actually meant?
6. Which repo is this? SKILL.md 9 says "maxengel/rocknix", 548 says "pixelelated/distribution", 143/192/446 say "scaffold", and 712 says "../rocknix.worktrees/".
7. "Cornerstone conformance" (SKILL.md 504; templates.md 51, 161; phases.md 389) is never defined. Line 411 says the repo has "no single conformance rubric". What is Cornerstone?
8. SKILL.md 421 says the register holds "Twelve recorded failure modes", yet line 598 cites "blindspot 13" and templates.md 34 cites "blindspot 53". Which count is right?
9. SKILL.md 110 says Epic tier must "re-derive at least 2 randomly-chosen … PASS findings". phases.md 71–72 says "Trust them; do not re-derive." Which one applies?
10. Phase 4.6 is "mandatory at Epic and Milestone tiers" and "Fails closed" (phases.md 439, 486). templates.md 129–146 allows `depth: local` for an Epic-tier slice. When does that exception apply?
11. phases.md 132–134 ("vitest", "`kno:validate`", "`npm run check`"), 279–284 ("tenant zero", "Dogfooding Gate"), 312–317 ("caddy reload", "OpenBao") and 329 ("`.kno` entity files") don't match the repo's own check list in SKILL.md 171–177. Are these meant to apply here?
12. phases.md 353 says "every finding flagged in passes 1–3" and 412 says "all three passes". What are the passes: Phases 1–3, or forward, retrospective and something else?
13. IDs and labels used but never assigned or defined: "F-NN" (SKILL.md 629; templates.md 89, 326) and "P3 items" (SKILL.md 612), while severity is Critical/High/Medium/Low (line 520). What do they map to?
14. phases.md 3 promises "phases 0–7", but the file ends at Phase 6. SKILL.md 266 calls phases.md "the spec", yet phases.md hands Phases 0 and 6 back to SKILL.md. Also, the criterion entry "Reproduced here" (templates.md 270–295) orders its sections differently from phases.md 148–172 and drops the "Command evidence" line. Which one is authoritative?
15. Terms used without definition: "Facilitator" and "fresh owners" (SKILL.md 44), "`next`" and "`<main-checkout>`" (280), "Phase Z.6" (661), "the seat" (phases.md 441 on), "Tier B" (SKILL.md 142), and "the 3+ instances rule" (line 92, defined only at 630). Also, line 415 says rules live in `.claude/rules/*.md`, but line 426 names "`rclone-cloud-sync.instructions.md`". Where do these live, and what are they?
