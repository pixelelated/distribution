# The reader's pass: `session-stash` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/session-stash/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

The directory holds one file, /workspace/tmp/m6-t38/export/.claude/skills/session-stash/SKILL.md (163 lines). I read every line of it. All line numbers below refer to that file.

**1. What I understood**
The skill decides what session state to save, where to write it, and how to commit it so a fresh agent can resume. Writing it includes archiving the old copy and removing a copy inherited from `main`. A session should open it when the user asks to stash or hand off, when context is nearly full, before switching task, branch or repo, at the end of the day, or before a risky operation.

**2. Where I stumbled**

1. L24, L32, L41: The default path is `saved-session-state-{branch}.md`. "In this repository" it is `saved-session-state-next.md` plus "a pointer at each working branch's own path". Yet L41 says each branch carries "only its own" file. Which file holds the stash, what is a "pointer", and which file does session-resume read?
2. L32: "D-WORKFLOW-133" and "the recorded safe strategy". What are these, and where is the strategy recorded?
3. L32: "prove it by giving an agent with no context only the repository". No workflow step does this. Do I do it on every stash, and how?
4. L64 vs L32: "Use this exact template", but the template has no **Start here** section, which L32 requires. Where does that section go?
5. L30 vs L32: Do I "prefer that" (an existing directory convention), or the repository-specific rule? Which wins?
6. L36: The removal happens "before writing the new file", but it sits outside Steps 1–3. Does it come before Step 1, or between Steps 1 and 2? Does `next` count as "a branch other than main"?
7. L36 vs L38: The inherited copy is "a guaranteed modify/delete merge snag", and removing it "surfaces as a modify/delete conflict". Is that conflict the intended result?
8. L38 vs L127–128: "user-approved stash commit" vs "do not request a repeated confirmation". Who approves the commit, and when? Also, why does the removal go into a summary of "what was saved" (L123)?
9. L28: What format does `{timestamp}` use? The L49 format contains colons, which I am unsure are safe in filenames. Should I use plain `mv` or `git mv`, given the files are tracked?
10. L92: Item 3 is something the next agent "should resolve first", but it is listed third in an ordered list. How does it differ from Open Questions (L115)?
11. L127–129: "canonical stash", "the fork's commit convention" and "owning issue" are never defined. Which fork, and which issue?
12. L130–132: "live milestone", "evidence", "read back" and "checkpoint" are never defined. "The milestone holds priorities" seems to clash with the template's "highest-priority next action" (L90). Where do priorities belong?
