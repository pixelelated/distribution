# The reader's pass: the eight agent files (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/agents/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim; it says it ran one `ls` on the directory and nothing else. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`. The agents are the export's (ruling (d)), so every item is a lead for the inherited list, never an edit here.

---

I needed one `ls` on that directory and nothing else. The names I guessed did not exist, because the files are `*.agent.md`. I read all eight files in full and ran nothing more.

**1.** These eight files each pin one provider model to a seat in a five-model "council" and give every seat the same reviewer prompt. A session never picks a seat directly; it would only reach one by running the `council` or `council-research` skill, which goes through `scripts/council-invoke.ts`. The ones to use are claude, gemini, gpt, kimi and muse. The ones not to use are deepseek, grok and mistral, which are historical.

**2. Stumbles**

1. gemini L5–13 vs L15: the comment says "direct-API identity", "`ai-studio`… NOT Vertex AI", literal match on `modelVersion`, "§ Substrate A". The line under it says "(OpenRouter, effort=high)". Which substrate and which matching rule are real?
2. claude L10, gemini L10, gpt L9: `modelMatches()` is "SEMANTIC" in claude but "literal" in gemini, and gpt names `openRouterModelMatches()` for the same "§ Substrate C". Which function, with which rule?
3. claude L3 "Use when running multi-model analysis" vs L25–31 "MUST be invoked via… refuse the task". Is a session ever meant to pick this agent from its description?
4. claude L3/L56 "Invoked by the `council` skill" vs L17 "only permitted invocation path is the Council Facilitator". How do the skill and the script relate?
5. claude L5, L16, L19: "Single-element prioritized list", "R8 substrate-collapse incident", "silent picker leakage". None of these is defined. And why "prioritized" when there is one element?
6. claude L31 "emit a halt signal naming #3059". In what form, and to whom?
7. claude L37: "run manifest's locked profile" and "installed definitive profile (D-WORKFLOW-135)". Are these the same thing? How does a member model "use" a profile? And who counts as "other active members" when all five are required? kimi/muse L3 also say "required members… failed seat" where the others say "verified members… missing seat". Is that a real difference?
8. claude L44–45 "location specified by the user", "(Step 6 only)", with tools `[readFile, edit, search]` (L4). Who is "the user" when a script calls the agent? What is Step 6? Does a provider call even get these tools?
9. mistral L3 "Kept for runs sealed before that change" vs L21 "do not invoke in pixelelated". May it be invoked to re-run a sealed run?
10. mistral L21 says "text below… is not an active member instruction". Yet L13–19 carry the mandatory banner, L29 lists "(Claude, Gemini, GPT, Kimi, Mistral)", and L48 says "invokes this agent at Phase 1". If this file is loaded, which of these does the model obey?
11. mistral L9 "OpenRouter primary… via mistral/eu" vs L23, an Azure AI Foundry probe saying "NOT `max_completion_tokens` like GPT/Kimi". GPT and Kimi are on OpenRouter in their own files. Which endpoint is meant? And what is the "source estate"?
12. kimi L21 gives "1.05M context" and also "the seat's 262144 ceiling". Mistral L21 and muse L21 say a 262,144 window "could not take a complete council request". Is Kimi's 262144 an output cap? "Reasoning preamble consumes short token budgets" also took me two reads.
13. kimi L9/L21 list four providers in order, "modal → sail-research → together → moonshotai", "with fallbacks off". With fallbacks off, what does the order do?
14. muse L34 "Do not manufacture disagreement or adopt an assigned national/cultural persona" appears only here, next to L31 "Be… opinionated". Does it apply to the other four seats?
15. deepseek/grok L13–19 use "D-WORKFLOW-109", "pin verifier", "imported", "the other projects" and `IMPORTED-FROM.md`, and mistral/muse L3 use "scaffold#915". None is explained. These two inactive files also lack the facilitator banner that inactive mistral has. Does the pin verifier reading them count as "invoking"?
