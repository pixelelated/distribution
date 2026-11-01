# The reader's pass: `council` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/council/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim; it says it ran one read-only `find` to list the directory and nothing else. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`. The council skill is the export's (ruling (d)), so every item is a lead for the inherited list, never an edit here.

---

I read all 15 files in the directory in full. To find them I ran one read-only directory listing (`find`), which was a command; I ran nothing else.

**1. What I understood**
The skill picks one winning plan out of five: five pinned models (Claude, Gemini, GPT, Kimi, Muse) each analyse the same problem, review each other's analyses, revise their own plans and vote, and then an issue is opened for the work. A session should open it for a contested design or method decision, or when the user asks for a council.

**2. Where I stumbled**

1. SKILL.md 3 against 44-45: "run a trio process" is listed as a trigger, but "legacy 'trio' wording never authorizes reducing" the council. Does "trio" open the five-seat council or the three-model preliminary review?
2. SKILL.md 78 says "one at a time", but pipeline.md 155-156 says that guidance was "retired". Do I call the members one after another or all at once?
3. SKILL.md 82-84 and 162-164 say to lint before the next step. pipeline.md 202-206 says the lint "fails with `seal-missing`" unless the step is sealed first, and SKILL.md never mentions the seal. Which order do I follow?
4. model-verification.md 16 and member-roster.md 119 both say "Direct-API is the substrate-of-record". member-roster.md 11-16 makes OpenRouter the default, and pipeline.md 120-121 says direct records are "not proof". Which one is it, and may a new run use `--provider direct`?
5. model-verification.md 63-69 and 211-212 name gpt-5.5, Kimi-K2.6, Mistral and Azure keys, and leave out Muse. Is this the current setup or history?
6. model-verification.md 382-384 and output-conventions.md 394-396 take the declared model from the agent file's `model:` array. member-roster.md 35-36 says the `OPENROUTER_SEATS` table is the authority. If the two differ, which do I compare against?
7. pipeline.md 416-417 lists "2-1-1" and "5-0". voting-rules.md 57-58 calls 5-0 impossible, and five ballots cannot add up to 2-1-1. Are these typos?
8. voting-rules.md 30 says to "Recurse once" on a 1-1-1-1-1 tie. tie-breaking-recursion.md 74-76 allows rounds "at most through r5". Which limit applies?
9. tie-breaking-recursion.md 28-30: in round N, Step 2 reads the "current-round revised plans … NOT the previous round's". But round-N plans are only written at Step 3 of that round. Which files does Step 2 read?
10. pipeline.md 62-64 "requires the in-tree Forge preflight", and 458-460 creates a "Forge issue". IMPORTED-FROM.md 28-29 says the Forge write preflight is "gone". Where does the Step 5 issue go? And what is the "`product-specs` skill" (pipeline.md 468)?
11. pipeline.md 80-83 bans members from three directories. context-loading.md 120-126 lists only two and leaves out `research/council-runs/`, then 198-199 says to search that directory. Is it banned or not?
12. The tools list in SKILL.md 5 has no shell tool, yet every step runs scripts. pipeline.md runs `node scripts/…`, while IMPORTED-FROM.md 79-81 says to use the `tools/council/run` wrapper. How am I meant to run them?
13. pipeline.md 173 passes a `source-manifest.json`, but no Setup step creates it. member-roster.md 142-144 runs probe calls at Setup, but pipeline.md's numbered Setup list has no probe step. Do the probes come before or after the run start (genesis) step?
14. model-verification.md 485-492 shows a log with four member rows and then "PASS — advancing". output-conventions.md 452 says the README lists the roster as "(3, 4, or 5)". Is a roster smaller than five ever valid?
15. output-conventions.md 131 says "1.6.0 for this adoption", but IMPORTED-FROM.md 106 says the Facilitator is "1.14.1-pixelelated.1". Which version should a new run's manifest show?
