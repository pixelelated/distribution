# Stage B, the auditor's read: `mini-retro` (T38, #685)

Read at the dispatch tip's bytes, from the export, after the reader's pass (`reader-mini-retro.md`). Line numbers are the file's at `87c2ab0fed`. Each note is a lead until its check line is run (`stage-b/checks-*.out`).

## SKILL.md (610 lines)

- **L-05:** `:67-70`, the Timebox column (`~30 min`, `~2–4 hr`, `~4–8 hr`, `~1 day`). **New, beyond the pattern:** `:189` *"The scoped audit is a 30-minute adversarial check"* (`30-minute`, hyphenated, which `[0-9]+ (seconds|minutes)` cannot match).
- **L-08:** Step 4 (`:310-320`) gives the retro two homes -- a spec in `docs/planning/<feature>/<feature>-spec.md` *"or similar"* and a comment on the Epic -- and neither is `ceremonies.md`'s marker (`docs/retros/<date>-<scope>.md`, or a work-log heading that says retro). A retro written to the skill's two homes leaves `ceremony-check`'s `retro` line DUE.
- **L-20:** `:598` *"the local cadence is in `ceremonies.md`"* is the skill's one line naming the ceremony rule; it names no marker, no cadence and not `tools/ceremony-check`.
- **L-15:** `logs/audits/` at `:68`, `:69`, `:261`, `:275`, `:281`, `:549`, `:557` (here `docs/audits/`); `:220-221` *"(scaffold today is docs + bootstrap scripts, so this is usually a skip)"*; `:242` *"scaffold's doctrine §1"*; `:300-305` the source estate's examples (`X.test.ts`, `services/example-api/package-lock.json`); `:602-603` *"(scaffold does not today)"*; `:8` the origin note (*"adapted for scaffold (bedrock→cornerstone ...)"*). With the reader's *"Which repo is this?"* (item 9).
- **L-22:** `:3` -- in the **description**, which every session lists -- *"(as does `begin-exploration` for Discovery Epics, if present)"*; then `:364`, `:385`, `:466`, `:479`, `:499`, `:504`, `:528`.
- **L-08's other half, `:70`:** a `docs/retrospective/` dated set and the `retro-sweep` skill, *"(optional external skill, absent here)"* at `:76` -- the skill says itself that it is absent.
- **L-14:** `:116-118` `mcp_github_add_issue_comment`, `mcp_github_issue_read`, `mcp_github_issue_write` (the Copilot names).
- **L-58's family (another estate's history):** `:148` *"(Origin: Possibility Collaboration v1 Phase 11.7 retro ...)"*; `:293` *"Origin: M22 FOUND-P4 (#2510, 2026-05-14)"* (to check: #2510 on this tracker).
- **L-55's family:** `:269` *"(final phase before PZ)"*: PZ is defined nowhere in the skill (reader item 7).
- **New lead -- the scoped audit's checks, three counts:** the procedure lists nine (`:199-252`), the format's *Scoped audit findings* lists six (`:353-358`), and `scoped-audit.md` has ten (its `Check 10`, to read). A retro written from the format drops checks 6 to 9 (and 10). Reader item 2.
- **New lead -- the audit's place in the order:** `:187-189` *"After Step 1 (evidence gathering) and Step 2 (writing the four questions), run a lightweight scoped audit"*, while `:163-164` says the audit's findings feed § 3 of Step 2, and `scoped-audit.md`'s opening (to read) says before. Reader item 1.
- **Q7, from the reader:** `:152` *"Every retro has exactly these four sections. Do not invent new ones."* against the format's added sections (item 5); `:351` *"Optional."* against `:271` *"For all other phases, run the checks"* and `:578-583` *"All three are required for a phase"* (item 4); `:461-462` *"captured in Step 7 below"*, written inside Step 7 (item 6); `:434` *"Close the Mini Retro issue on the tracker (if the milestone uses one)"* (item 11).
- **New lead -- "the full 6-phase methodology":** `:547-548` *"Runs the full 6-phase methodology (research / forward audit / retrospective / analysis / punch list)"* names five, and `code-auditor/SKILL.md:84-85` says the same six, while its lifecycle table runs phases 0 to 7 with 2.5, 4.5 and 4.6 (eleven rows). A count true once (Q4 (c)).
- **Q7, a duplicate:** `:26-35`, *pixelelated continuation*, is `futro/SKILL.md:26-35`'s section word for word (the brief's Q7; the diff written at Q7 by a script).
- **Positives read:** `:39-58` a finding without an artifact has not run; `:111-112` a fresh agent reads the commits first; `:180` the rule of three; `:597-606`, the fork's own integration paragraph, naming `ceremonies.md`, `issue-tracking.md`, `fork-workflow.md`, `milestone-phase-naming.md`, `working-principles.md` and `decision-register.md`, each a rule that exists.

## references/scoped-audit.md (716 lines)

- **The order, confirmed as two texts:** `:3-6` *"runs as **Step 2.5** ... after evidence is gathered but before the four retro questions are answered. Its findings feed into questions 3 ... and 4"* against `SKILL.md:187-188` *"After Step 1 ... and Step 2 (writing the four questions)"*. A reader of the reference runs it before; a reader of the skill, after. Reader item 1.
- **L-05:** `:69` *"Each check takes ~5 minutes"*, `:184` *"Each should take 30 seconds to 2 minutes."* **New, beyond the pattern:** `:8-9` *"It is a ~30-minute spot-check"* (`~30-minute`: the pattern wants a unit right after the number or a space).
- **L-10 confirmed:** `:347-359`, the "pre-existing" verification block -- `git stash` (`:349`), `git checkout <base_sha> -- <files_touched_by_phase>` (`:351`), `npx vitest run <failing_test_files>` (`:353`), `git checkout HEAD -- <files_touched>` (`:357`), `git stash pop` (`:358`). Also `:292-309`, Check 5's *"full project test suite"*, *"`npx vitest run` with no filename arguments for example-api"*, *"`cd services/example-api && npx vitest run`"*, and `:313-321`'s *"verified by stashing the phase's edits"*. What a reader running it does here:
  - the stash stack is shared by every worktree and session, so `git stash pop` can apply another session's entry;
  - `git checkout <base_sha> -- <files>` overwrites the working tree with no way back but the stash;
  - this repository has no unit-test suite (`CLAUDE.md`), so `npx vitest run` would fetch a package from the registry, a fetch the renovation's lanes may never make.

  To check for the `Already written:` line: whether any session's record shows the block run (`git stash pop` or `vitest` in the work logs, the friction log and the retros).
- **L-15 confirmed, wider than the brief's lines:**
  - `:22-23` *"scaffold's `.mjs` script conventions"*;
  - `:46`, `:54`, `:700` `logs/audits/`;
  - `:172-211` Check 2 whole -- `:176`'s link to `../../../../docs/architecture/cornerstone-conformance.md` (to check: absent?) and the eight spot checks of `:188-195`, all the source estate's (ESM-not-CJS under `services/example-api/src/`, `postgres.camel`, XRI `kno://`, `validation.rules.*` with #2289), with `:204-211` admitting they are *"origin-project-specific"* and asking that they be replaced *"For scaffold"* -- never done here;
  - `:230-249` the risky pairs (*"origin-project examples -- adapt to your stack"*: TerminusDB, `pg_advisory_xact_lock`, OpenBao, Key Vault);
  - `:399-400` *"scaffold today is docs + bootstrap scripts with no UI surface"* (this repository has EmulationStation's interface and the VM's frames);
  - `:612` *"record the reversal as an ADR"*.
- **L-12:** `:209` `scaffold-platform.instructions.md`.
- **L-58's family (another estate's history as this tracker's):**
  - `:65` *"#2510"*, `:97` *"PL-06 / Z-3"*, `:132` *"M22 #2674 Phase B"*, `:155` *"R2 #2302"*;
  - `:193` *"(see #2289)"*, `:296` *"the M33 P3 retro (2026-04-25)"*, `:340` *"(#2387 Bucket I)"*;
  - `:463` *"M26 P1 (2026-05-08)"*.

  This tracker's numbers run to 1385, so each `#NNNN` above it names nothing here, and a lower one names another issue. The one the fork wrote, `:509` (#1067, T13, item 5 of Check 7), is this tracker's own.
- **L-55's family:** `:39` and `:703` *"PZ"*; `:519-520` and `:576-577` *"Outcome A / Outcome B"*, never defined (reader item 7).
- **A path that does not resolve:** `:71` *"See `reference/template.md`"*: the directory is `references/` (reader item 15).
- **The check count:** ten here (`### Check 1` to `### Check 10`, `:85` to `:621`), against `SKILL.md`'s nine and its format's six (`notes-mini-retro.md` above). `:659-691` *After the checks* routes all ten.
- **Q2, Check 10 (`:621-655`):** written against the source estate's ADR process and *"development-principles' ... (MET-1)"*. This repository's equivalent is `decision-register.md` (append-only rows, `tools/archaeology` before calling anything open), which `SKILL.md:604-606` names as Check 2's grounding and which Check 10 does not cite.
- **L-01, the fork's own lines:** `:505-511`, item 5 of Check 7 (`161effca8f`, #660), naming #1067 on this tracker. It reads correctly, and its origin is this repository's (T13).
- **Positives read:** `:361-362` a "pre-existing" label needs its mechanical verification (the method is L-10's, the rule is sound); `:407-409` a skipped check says so; `:709-716` the self-improvement hook.

## references/template.md (153 lines)

- **The check count, a fourth:** `:71-79` lists Check 1 to Check 9; the reference has ten.
- **L-08:** `:3-4` *"Copy this into the spec document phase section AND into the Epic issue comment"*: neither is `ceremonies.md`'s marker.
- **L-22:** `:90-93` (*"begin-exploration ... (If a skill named below isn't installed -- e.g. begin-exploration -- treat its mention as conditional.)"*) and `:133` (twice).
- **L-15:** `:27` *"example-api went 4244 → 4293 passing tests (+49)"*; `:97-98` the ESM spot-check as the example; `:105` *"a dedicated P7 housekeeping task"* (P7 undefined; reader item 7).
- **Q7, two closing lists:** `:137-152` *After writing* (post, update the spec, edit issue bodies, comment, update the milestone, close the Mini Retro issue) against `SKILL.md:396-407`'s Step 5 (which also files follow-up issues and edits skills, and has no Mini Retro issue). Reader item 11.
- **Positive:** `:4-6` *"Do not leave placeholders"*; `:60` an empty Adjustments section is not an answer.

## What the checks settled (`stage-b/checks-mini-retro.out`, 03:08:18Z)

- **L-02's history:** the import `437ebd09af` had **three** rules, numbered 1 to 3, the subagent rule third (`93:`, `95:`, `100:`, `116:` at that hash). `9a09b76dd9` (2026-08-24, *"skills: adapt code-auditor to this repo before running it"*) inserted *"Run it on a device"* and *"An assertion that cannot fail"* as 3 and 4, and renumbered neither the old 3 nor the count. A defect of the fork's own adaptation.
- **The scoped audit's checks, counted:** `10` headings in `scoped-audit.md`, `9` in `SKILL.md`'s procedure, `6` in its format, `9` in `template.md`.
- **Paths:** `docs/architecture/cornerstone-conformance.md` absent; `references/template.md` present and `reference/template.md` absent; `docs/planning` and `logs/audits` absent.
- **A delta against the brief's L-08 (R2 L-04): `docs/retrospective` is present.** It holds one file, `carry-forward.md`, since `19ba2e03a3` (2026-09-11), at the P1 tip, at `next` and at the coordinator's tip alike. It is not *"a `docs/retrospective/` dated set"*: the directory exists and the dated set the skill describes does not. Recorded beside the brief's line, not argued.
- **Another estate's issues:** #2510, #2674, #2302, #2289 and #2387 resolve to nothing on this tracker (its highest is 1385).
- **The record of the markers:** `docs/retros/` holds `7` entries and `docs/futros/` `17` at HEAD (R2 C20's 6 and 16 were read at `926d1fbaee`). Sessions wrote the markers `ceremonies.md` names, though neither skill tells them to.
- **L-10's Already written:** the work logs, the friction log, the retros, the futros and the audit folders name `git stash pop` or `npx vitest` nowhere but this slice's own stage-A output. No session's record shows the block run, so *nothing inherited*, argued from the record.
- **Q7's duplicate:** `futro :26-35 = mini-retro :26-35`, byte for byte.
