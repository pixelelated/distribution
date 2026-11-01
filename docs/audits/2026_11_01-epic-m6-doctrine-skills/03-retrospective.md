# Retrospective Audit — M6.P2 T38, the skills, agents and settings

**Auditor:** Code Auditor skill, Local depth (D-WORKFLOW-184)
**Date:** 2026-11-01
**Subject:** #685, the 52 paths of `.claude/**` less `.claude/rules/**`, at `87c2ab0fed`
**Spec:** `docs/reviews/briefs/doctrine-skills.md` version 2 (`fa4a9a5b0d`); #685's body

---

## 3.1 Architectural coherence

The 52 are two systems that happen to share a directory.
- **The six workflow skills** were imported from one external estate in one commit (`437ebd09af`). Since then they have been adapted in place, in about thirty commits, by appending: a section added, a rule inserted, a count left as it was.
- **The writing pair** is the fork's own, written in one commit (`9404f23c55`).
- **The council family** is a second estate's export, copied byte for byte and patched by a listed set of adaptations (`IMPORTED-FROM.md:15-50`).

The coherence problem is the first group's. Its adaptations are of two kinds:
- **Additive and clean:** the *pixelelated continuation* sections (D-WORKFLOW-140), the replaced-mechanism archetype, item 5 of Check 7, Step 1.7.
- **Additive and half done:** two floor rules inserted without the count (L-02), a fifth technique without the count (L-67), a lint mandated in `SKILL.md` while `phases.md` still says there is none (L-59), and #810's Local exception landed in the template while four procedure sentences still fail it closed (L-56).

The shape is the same each time: the new text is right and the old text beside it was not revisited. That is why every one of them is a *two texts that disagree* or a *count true once*, not a wrong rule.

## 3.2 Project conformance

- **Instruction files**, read at `3a9b0aec81`. The rules the slice's own leads cite were read at their lines (`01` § Pre-flight):
  - `adversarial-council.md` (`:49-58`, `:77-78`; the substrate paragraph `:36-38`);
  - `release-candidates.md:71-76`, `device-builds.md:596-597`, `ceremonies.md`'s marker table;
  - `learning-capture.md` § 4, `issue-tracking.md`, `worktrees.md`, `engineering-practices.md` (the four changed sections);
  - `working-principles.md` § Enforcement depth.

  Where a skill and a rule disagree, the rule is canonical (`code-auditor/SKILL.md:434-436`'s own sentence), and the disagreement is a skill fix (L-11, L-13, L-14, L-66) or a rule erratum for the coordinator (L-22, L-23, L-50). The lane made no rule edit.
- **Blindspot register**, read at its lines (`stage-b/floor-reads.out`):
  - **Entry 1 (*Assumed-undone*)** is the one `begin-delivery`'s Step 1.7 guards, and this read repeated it in miniature. L-19's *"the skill does not say it in other words either"* was the brief's; the sentence was there (`session-stash/SKILL.md:32`), so the record corrects it.
  - **Entry 27 (*Supersession that lives only in a comment*)** is L-56's shape: #810's fix lives in the template's example, while the procedure's four sentences still say the old thing.
  - **Entry 9 (*Treating futro predictions as decisions*):** the kickoff addendum's predictions are checked below as hypotheses, not taken as findings.
- **Project invariants:** the 52 carry no backup, sync or device path, so the cloud invariants do not apply. The one that does is *a fix answers what was already written*: each proposed `bug` carries its `Already written:` line at stage D, and the punch items whose old sentence produced artifacts (L-02's five briefs, L-69's canonical stash) say so in `02`.

## 3.3 Spec fidelity

- **The brief's leads against the tree:**
  - forty-seven of L-01 to L-51 hold as written;
  - **L-32 is withdrawn** (the sentence names its skill), **L-35 is narrowed** (each relative path is named with its skill in words);
  - **L-19 is corrected** (the stranger's proof is stated, not stepped), and **L-08 carries a delta** (`docs/retrospective` exists, holding one file, not a dated set).
- **The brief's counts:**
  - the dispatch tip's `12783`, the stale-names table and `BUNDLE match=52 diff=39 absent=3` reproduced exactly;
  - `register-check` reads `714 IDs` (the brief's `712` at `2f42ff5ddf`, plus -218 and the P1 branch's -188), and `refs scanned: 83` (this lane's branch is new);
  - `docs/retros/` holds `7` and `docs/futros/` `17` (R2's 6 and 16 at `926d1fbaee`), and the work logs name `council-research` on `3` lines (R2's 2).
  - Each is a tree difference, recorded beside the brief's figure, not argued.
- **The brief's open items:**
  - 2 settled: one real heading mismatch of three (L-60);
  - 4 settled: the three test files absent;
  - 5 read: no shadow-seat instruction in the 52's prose;
  - 6 read: one guest-behaviour sentence, `developer-relations:171-183`, recorded `[unverified]`;
  - 7 settled: the three checkers' lines.
  - Still open: 3 (L-29's pid) and 8 (the harness's description limit: not cited, so `t38-checks.sh` asserts no limit), questions for the pause; and 9, the coordinator's.

## 3.4 Platform conformance

`tools/rules-check` reads none of the 52 (`rc=0`, no evidence for them), and `register-check` reads the skills but not the agents. No check the fork runs reads a skill's text for meaning (§ 3 item 5), so every finding here is the read's, made mechanical at stage C by `tools/t38-checks.sh` and proposed to #1373.

## 3.5 Cross-system interaction audit

### Interaction: the skills x the renovation's procedure (the slice reviews the skills it runs on)

**State shared:** the code-auditor skill's artifact contract (`templates.md`, `phases.md`) and the plan § 6b procedure that every slice follows; this audit was itself written under the skill it judges.
**Wipe risk:** a lane that copies the template fails the lint on one heading (L-60) and writes a slug that is not the model's ID (L-51). A lane that reads Phase 4.6 as written halts a Local slice (L-56). A lane that runs the lint the skill's way before Phase 6 meets an issue that does not exist (L-52). This lane met all four and worked around each from the brief.
**Test coverage:** PARTIAL -- the lint is the contract's only check, and it checks the folder, not the skill's text.
**Finding:** risky: the briefs carry the corrections the skill lacks, so a lane without a brief would meet each defect for the first time.

### Interaction: the skills x the rules they cite

**State shared:** the rule names and sections the skills point at, and the facts they restate (the branch, the layout, the publish path, the audit seats).
**Wipe risk:** a renamed or rewritten rule leaves the skill's restatement behind, and the skill is read in the moment of acting:
- the Copilot-era `.instructions.md` names (L-12);
- `../rocknix.worktrees/` (L-04);
- the retired publish path (L-11);
- the `main` branch (L-09, L-66).
**Test coverage:** UNTESTED -- nothing reads a skill's citations against the rules (#1373's).
**Finding:** broken in five places, each a punch item or a bug.

### Interaction: the skills x the tools that read their artifacts (the lint, `ceremony-check`)

**State shared:** the markers and the sections. `lint-audit-artifacts` reads `ANALYSIS_SECTIONS` and the punch index; `ceremony-check` reads `docs/futros/`, `docs/retros/` and `audit-completion.json`.
**Wipe risk:** the skills tell a session to write the futro and the retro to a spec and an Epic comment (L-08), name no completion marker (L-06), and give a heading the lint does not accept (L-60). The record shows the sessions writing what the tools read, from the rule, not from the skill.
**Test coverage:** PARTIAL -- each tool fails its own missing artifact, so the gap surfaces as a DUE line or a FAIL, never as a wrong artifact.
**Finding:** risky, contained by the tools.

### Interaction: the export x its pins, its sums and the Facilitator

**State shared:** the agents' bytes (pinned), the bundle's checksum list (the import's record), the roster in three prose copies and the Facilitator's `OPENROUTER_SEATS` (T45's).
**Wipe risk:** an agent edited without a re-pin fails `verify-pins` at council Setup -- the pins match today (A-07). The sums are read by nothing, so their 39 differences go unnoticed (L-34). The prose rosters agree with each other and with the rule today (B-21), and nothing checks that they keep agreeing (L-44).
**Test coverage:** TESTED for the pins (offline here, by `verify-pins` at Setup); UNTESTED for the sums and the prose rosters.
**Finding:** safe today; the inherited list carries the two untested seams to #911 and #1373.

## The futro's predictions, checked

The doctrine futro's T38 kickoff addendum (`docs/futros/2026-10-24-m6-doctrine.md:472` on) predicted a lane's wrong turns and the record's patterns. Each, against what this lane's record shows:

| Prediction | What happened | Verdict |
| --- | --- | --- |
| a lane invokes the council skill to "verify the roster" | the roster read offline from the three sources (`stage-b/tables/q4.md` (e)) | did not happen |
| it deletes the three inactive agents as dead | kept and pinned (A-07); recorded with their cost (Q5) | did not happen |
| it edits `council-substrate-integrity.md` because L-50 is on #685 | no write under `.claude/rules/` (A-06) | did not happen |
| it cites `tools/rules-check` rc 0 as a check of the skills | recorded with the words *no evidence for the 52* (`02` § The runs) | did not happen |
| it rewrites an imported skill in place, or fixes before the pause | no edit under `.claude/` at stage B (`00`'s last line) | did not happen |
| it runs a session-stash block that writes under `.github/sessions/` | none run; the pointer is the lane's own | did not happen |
| it runs `scripts/verify-pins.ts` | the pins recomputed offline (A-07) | did not happen |
| it reads 12,734 as the dispatch tip's lines | both totals recorded (A-03) | did not happen |
| it copies the template's slug | the slug is L-51; the plan at stage C writes `anthropic/claude-opus-5-5` | did not happen |
| it keeps the literal coordinator's-tip placeholder | filled; the positive fired at `rc=1`, not `128` (A-04) | did not happen |
| it posts the `council-research` question on #807 | the question goes to the coordinator at the pause | did not happen |
| it writes a START in the host file | no line (`00` § The host file) | did not happen |
| **pattern:** a skill that names what does not exist | confirmed, widened: L-22, L-30, L-31, L-09, and the read's own L-55, L-65, L-73, L-75 | confirmed |
| **pattern:** a count true once | confirmed, widened: L-02, L-03, L-34, and L-63, L-64, L-67 | confirmed |
| **pattern:** a checker whose rc 0 covers nothing | confirmed (`rules-check`; `forbidden-terms-check` on empty input; `register-check` on the agents) | confirmed |
| **pattern:** a form a reader copies wrongly into an artifact a tool reads | confirmed (L-51, L-60) and widened by L-61 (the escaped fence) | confirmed |

Twelve of the twelve predicted wrong turns did not happen, which is what a brief that names them is for. The four patterns held, and each was widened by what the read found.
