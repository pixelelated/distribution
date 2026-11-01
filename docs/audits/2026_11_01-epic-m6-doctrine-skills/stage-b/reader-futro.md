# The reader's pass: `futro` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/futro/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

I read all four files under the futro directory, every line: SKILL.md (483 lines), references/techniques.md (320), references/template.md (143) and references/blindspot-register.md (105). I read nothing else.

**1. What I understood:** Before work starts, the skill decides which traps, unverified assumptions and blindspots a plan has, and which plan edits or investigations must happen first. A session should open it at the start of a phase, an Execution Epic, or a sub-issue with tangled dependencies (it is `begin-delivery`'s second step), but not for Discovery Epics or mechanical fixes.

**2. Where I stumbled:**

1. SKILL.md 288–325: "Apply four techniques" is followed by five bullets. techniques.md 4 says "Four complementary techniques" but lists a different four, and template.md 68 names only three. Which set is the real one?
2. techniques.md 4–5 says "Run them all" for question 4, but line 264 says technique 4 is "used for question 3, not question 4". Should I run it during question 4 or not?
3. SKILL.md 133–192: "PE", "AD11", "AD6", "P7 PE7", "E253", "PL-04", "BS-5" and "M64 P1.5 E2/E3/E5/E4" are never defined. What is a PE?
4. SKILL.md 199 says the `### N. ...` (H3) style failed MD001, yet template.md 20 uses `### 1. What do we know…`. Also, SKILL.md 384 puts the futro in a `### Futro: Phase N` placeholder, while template.md 10 starts with `## Futro:`. Which heading levels are right?
5. SKILL.md 141–143 and 258–259 point to register sections ("Schema-`required[]`-enumeration miss", "Substrate-precondition assumption…") that the shipped blindspot-register.md doesn't have. SKILL.md 377 says "register entry #2" and 321 says "Blindspot 23", but the template's entries have no numbers. Where are these entries?
6. The rule for adding a blindspot disagrees with itself: SKILL.md 340 says "promoted at 2 instances", 462 says "Rule of three", and 430 plus blindspot-register.md 27–31 add an entry the first time it shows up. Which threshold applies?
7. SKILL.md 219–221 (branch freshness "MUST" go in question 1), 248 ("mandatory" substrate sub-question) and 263 (build-vs-adopt) have no slot in template.md's question 1 (lines 20–34). The template's "Confidence" line isn't in SKILL.md. Where do these go?
8. SKILL.md 179 says "`node scripts/<the platform probe> …`". I can't run a placeholder. Line 182 mentions "The manifest" and "The MCP phase" with no definition. Line 261 says "multi-surface probe transcript required above", but which mandate above requires multi-surface?
9. SKILL.md 404–405 says the "Epic comment MUST be committed". How do you commit a tracker comment? Neither Steps 4–6 nor template.md 136–143 has a commit step, so when does the commit happen?
10. SKILL.md 8 ("scaffold"), 26 and 468 ("pixelelated"), 229 ("scaffold has no such gate yet") and 318 ("rocknix"): which project is this, and does line 229 apply here?
11. SKILL.md 32–33 says "confirmation steps below apply only when…", but I found no confirmation steps below. Which ones are meant? And what are "receipts" (line 30)?
12. SKILL.md 21–22 says sub-agents are allowed "only where a stage explicitly says so", and no step says so. Yet line 188 ("A sub-agent's platform finding is a lead only") assumes sub-agents are in use. Are they allowed? Also, are "stages" the same thing as the "Steps"?
13. SKILL.md 131 places the "Verification mandates at futro authoring time" inside Step 1 ("Gather inputs"), but most of them govern writing PEs and ACs later. When do I apply them?
14. SKILL.md 411–412: "Step 2 (futro)… Step 3 (load tasks)" uses `begin-delivery`'s step numbers, which clash with this skill's own Step 2 and Step 3. I had to read it twice.
15. SKILL.md 440 ("produces prose / - issue edits + investigation tasks") renders "issue edits" as a sub-bullet of prose. Is that intended? And line 460 ("Proportional planning… short futro") sits beside a page of MUST mandates. Which of them can a small futro skip?
