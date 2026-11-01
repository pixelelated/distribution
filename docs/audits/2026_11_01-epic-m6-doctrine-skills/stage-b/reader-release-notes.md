# The reader's pass: `release-notes` (T38, #685)

One no-context read-only subagent (Explore type), given only `.claude/skills/release-notes/` of the export at the dispatch tip (`/workspace/tmp/m6-t38/export/`), asked what it would have had to ask (brief § 5 rule 5). Its report, verbatim. It is a lead, never evidence: each item is re-read by the lane before it becomes a row of `02`.

---

The directory holds one file, SKILL.md (130 lines). I read every line.

**1. What I understood:** The skill sets the shape and rules for two things written by hand: a release note for pixelelated/distribution's releases page, and the description and commit message of a `pr/*` branch going to ROCKNIX. The rules are outcome first, first person singular, no plumbing in the prose and no trace of an assistant. A session should open it whenever it writes either one.

**2. Where I stumbled:**

1. L3 against L97-102: the description says both get "the plumbing (commits, issues, runs) in a details block underneath", but the PR section bans headings, issue numbers and run numbers. Does a PR description get a details block?
2. L83 says "three or four short paragraphs", but only three are listed (L86-89). What is the fourth?
3. L66 says "`tools/prose-check` fails a plural", but L125 adds "`PROSE_FIRST_PERSON=fail` for a PR description". Does a plural fail a release note without that flag?
4. L27/L51, "at most ten across all sections": does "Devices and how to install" count toward the ten? Can it be dropped like other sections (L52)? And is "most player-visible first" ordered within What's new or across all sections?
5. L43 says "kept whole", but L7 lists "the glyph sections" and the template has no glyphs. The first-person rule (L61) also comes from a later decision, not the changelog skill. What was kept and what changed?
6. L36, "the H700 choice (the regulator read)": what is the choice, what gets read, and for which devices does it "apply"?
7. L39/L68/L128 use "the heads", "(vm-qa, the proofs, the rehearsal)", "as RC1 has", then "more than one build". Is a head the same as a build? What are those three runs?
8. L15, "the site's" voice: which site? `developer-relations` is named but never described.
9. L54 says every bullet traces to `docs/cloud-sync-changelog.md`. Is every release only about cloud sync? Where does a fix that is not about sync trace to?
10. L50, "where the reviewer looks": L12 says the reader of a release note is a player. Which reviewer is meant?
11. Terms never defined: "the maintainer's estate" (L7/L43), "D-WORKFLOW-0xx" (L7, L61), "register vocabulary" (L101), `fork-workflow.md` with no path (L77), "from the closing" (L108), "the interface work" and "the review guide's buckets" (L118), "the drafts' scan" (L126). What are these, and where do they live?
12. L76 "72 characters" and L112 "72 columns": a maximum or a wrap width? L120-121, "refuses a description that carries any of the above": all five "never carries" items, or only the ones a script can detect? L123, "Before it is shown": shown to whom, and do the checks run in a set order?
