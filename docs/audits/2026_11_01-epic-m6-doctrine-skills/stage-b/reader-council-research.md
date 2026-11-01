# The reader's pass: `council-research` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/council-research/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It read the files reachable by link from `SKILL.md`, every line; whether that is all 12 of the directory is checked by the lane (`02`). It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`. The council-research skill is the export's (ruling (d)), so every item is a lead for the inherited list, never an edit here.

---

I had no directory listing, since running commands was ruled out. So I read SKILL.md and the 11 reference files it links, every line. If a file in that folder has no link pointing to it, I haven't seen it.

**1. What I understood**
The skill runs a research pipeline with five model "members": an optional Phase 0 review of prior runs, then independent research, a neutral synthesis, adversarial review, a council vote and a deliverable with provenance. A session should open it when a high-stakes architectural question needs fresh research from several models first, not when the inputs already exist.

**2. Where I stumbled**

1. **Roster size.** SKILL.md 199-201 and model-roster.md 3-6 say "no fallback to four or three". But phase-1 150/154/285 and phase-3 584 say "fall back to (N-1)", phase-4 59 says "5, 4, or 3 members", and phase-5 172 says "3, 4, or 5". Can the roster ever shrink?
2. **Who does the member's bookkeeping?** phase-1 13-17 says members have "no filesystem… no tools". Yet SKILL.md 326-328 and provenance-schema 848-851 have the executor log hashes on "each time you call read_file". methodology-primitives 64-70 has members verify the manifest, and phase-1 259 has them read their own `.agent.md`. Who actually does these steps?
3. **How agents are invoked.** The frontmatter (SKILL.md 5) lists `runSubagent`, and line 208 says "invoking the relevant subagent(s)". phase-1 107-122 forbids `runSubagent` and requires `run_in_terminal`, which isn't in the tools list. And how is the Researcher Agent invoked?
4. **Phase 2.5.** SKILL.md 80 and 544-546 call it "repair-only". phase-3 104-111 says the orchestrator SHOULD start with it, and methodology-primitives 214-217 allows it on the first invocation. Line 125 says every phase has a reference file, but 2.5 has none. Which is right?
5. **Claim cards.** phase-3 41-47 projects corpora into claim cards on every run. Lines 349-351 and methodology-primitives 192-196 call them the "first replay repair", and phase-3 69-70 implies raw corpora are fine until a failure. What goes in a first, non-replay Phase 3 bundle?
6. **Prior runs.** Phase 0 triggers when Phase 1 sources sit under `research/**` (phase-0 16-19). But phase-1 266-268 says members "MUST NOT read" prior council-research directories. May they read prior runs or not?
7. **`phase` value.** provenance-schema 55 allows only phase-1 to phase-5, yet phase-0 222-224 requires a provenance file. What `phase` value do Phase 0 and Phase 2.5 artifacts use?
8. **Manifests and run ID.** There are two manifest shapes: `sources[]` (provenance-schema 304-322) and `files{}` (methodology-primitives 43-58). Both are named `.manifest.sha256.json`, which phase-1 133 passes to the Facilitator. The run ID is a UUID at schema 50 but a slug in the example at 307. Its file is `run-id.txt` in phase-1 131 but `.run-id` in the checklist at line 20. Which is canonical?
9. **Sequestered paths.** phase-3 216 and 240 use `.synthesis-redacted.md` and `claim-cards/`. provenance-schema 543 and 605 use `.sequestered-bundle/…`. Also, `claim-card-projection` (phase-3 241) isn't in the `derivation_kind` enum (schema 143-150).
10. **Phase 3 inputs.** provenance-schema 482 lists "EVERY Phase 1 corpus (including the member's own)" as a Phase 3 member's sources. phase-3 207-212 withholds the member's own raw prose, and line 551 says "only Phase 2 synthesis + corpora". What does a reviewer actually receive?
11. **Review target.** phase-3 330-333 requires reviewers to "critique every Corpus-X". Line 582 calls critiquing Phase 1 corpora attacking "the wrong target". Lines 288-291 cite "§1" and "§4", but the section list at 474-489 has no numbers.
12. **Phase 4 handle map.** phase-4 77-80 says the review handles are "re-randomized". provenance-schema 674-675 says the map is "the same map used for Phase-3". Which one?
13. **Phase 4 gate metric.** There are two: self-favouring at most 1/N (103-105) and pairwise vote agreement at most 1/(N-1)+0.10 (269). Under the second, members who vote together in a clean majority agree 100% of the time, so every clean majority seems to fail. Which metric gates?
14. **Undefined terms.** These are used before or without a definition: "Facilitator" (SKILL.md 214), "bedrock-adjacent" (44), "E5 deliverable" (145), "trio-\*" (phase-4 9), "Brake #5" (phase-1 224), "KU2" (schema 78), "new genesis" (model-roster 139), and "Neither seat" (model-roster 47). Also, model-roster 73-115 covers quirks for Foundry and Mistral, yet Mistral is no longer on the roster. Which members are still "Foundry members"?
15. **Versions and hooks.** SKILL.md 400 labels the allowlist rules "v1.1.0 — RC6", but line 22 places RC6 at v1.4.0. Lines 407-408 name two pre-commit hooks, while line 22 and provenance-schema 807 name a lint-summary hook. How many hooks exist?
