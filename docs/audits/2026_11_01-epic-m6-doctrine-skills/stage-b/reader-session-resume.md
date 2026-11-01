# The reader's pass: `session-resume` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/session-resume/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

The directory holds one file, SKILL.md (121 lines), and I read all of it.

1. My understanding: the skill decides which saved session-state file counts as the real handoff, how far to trust it against git and the live tracker, and what to do next. A session should open it when the user asks to resume or continue, or when a new session starts and a `saved-session-state-*.md` file exists.

2. Where I stumbled:

1. L24, L26, L28: first "Default path … `{branch}.md`", then "canonical … `-next.md`", then "If not found". Not found means which file, and which do I try first? Is the "pointer" a file's contents or a symlink?
2. L26 "D-WORKFLOW-133" and L44 "(#367)" are never defined. Where do I look them up? L26 "has not merged `next` since": since what?
3. L7 "version: 1.3.0", but the note only explains "v1.2.0". What changed in 1.3.0?
4. L30 "ignore `saved-session-state-main.md`" when not on `main`. In this repo the canonical file is the `next` one, so does the rule change? If every branch holds a pointer, won't "if multiple, list them" fire every time?
5. L40 "`Branch:` in the state file": if I read the `next` file from a working branch, doesn't this always warn?
6. L42 "`stat` the file": when I read it through `git show` (L26) there is no file to stat. Does the checkout time count as the time it was written?
7. L112 "any staleness tier, including `< 1 h`": no tiers are defined anywhere, and the Staleness section (L103–108) has none. What are they?
8. L44 says "Read the rules from `next`", then "a session loads the rules of the worktree it starts in". Which rules do I follow? Where is the "recorded safe strategy" kept?
9. L41/65/69/79 name the headings "Key Files Modified", "Current Focus", "Next Steps" and "Notes for Next Session". L117–118 say "Start here" and "Current priorities" are also valid. Which matches which? Which field holds `<last-known-commit>` (L75)?
10. L45 says "Issue tracker state (if referenced)", but L47 and L105 ("At every resume … live tracker") make it always. Is the tracker check optional or required?
11. The trigger "what was I doing" (L3) and "status alone does not authorize" (L94) pull against "execute the next unblocked action … Do not end with a menu" (L88–89) and "offer to help them scope" (L32). When a user asks "what was I doing", do I only report, or carry on with the work? Where is "authorized" written down?
12. Terms used before they are defined:
   - "checkpoint" (L47, L96, L121): is it the state file?
   - "live milestone queue" (L12)
   - "issue numbers and checkpoint age are not priority" (L47)
   - "source readiness, image qualification, RC designation" and "completed ceremonies" (L99–101)

   L97 "Record the issue…": record it where? L121 "refresh the canonical checkpoint": does a resume skill write to `next`'s file?
