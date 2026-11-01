# Stage B, the auditor's read: the writing pair, `developer-relations` and `release-notes` (T38, #685)

Read at the dispatch tip's bytes, from the export, after the reader's pass (`reader-developer-relations.md`, `reader-release-notes.md`). Both are the fork's own (`9404f23c55`, 2026-09-29, #323, D-WORKFLOW-068). Line numbers are each file's at `87c2ab0fed`. Each note is a lead until its check line is run (`stage-b/checks-writing-pair.out`).

## developer-relations/SKILL.md (195 lines)

- **L-27:** the open checkboxes of #333, #326, #341, #645, #953, #955 and #268 read against this text: the check below prints each.
- **The site checkout** (`:36`, `~/Development/rocknix.org`, branch `main`): present by R2 C18. The lane does not open it: rocknix.org's pages are T39's and the site's, not the 52.
- **Paths and tools named:**
  - `:20` and `:158` `tools/prose-check`, `:175` `tools/png-blackout` and `:119` `tools/pr-stack-check` exist (R3 C20's tool line);
  - `:172` `tools/vm-walks/docs/<page>.steps`: to check the directory;
  - `:174` `generic-x64-vm-testing.md` (a rule), `:65` and `:194` `es-player-text.md` (a rule; the reader asked where, item 5).
- **Q7, from the reader:**
  - `:103-104` fails *"An em dash or a spaced en dash ... (the site uses ... a plain hyphen with spaces ...)"*, while the file writes ` -- ` throughout (item 8). That is the fork's ASCII double hyphen, which `es-code-traps.md` asks for in comments, and it is neither tell; one line saying so would settle it.
  - `:116-135`, the *Warn* list, split by a blank line at `:129` into two lists, so whether `:130-135` are warns too is read from position alone (item 9).
  - `:178` *"two walks counted it as a row"* and `:181` *"lost one press in each of three walks"*: two facts about different walks, written so they read as one count (item 12).
  - `:182-183` *"the tool's re-send was never the fault, a miscount was"*, after a sentence about the re-send (item 12).
- **The skill edits itself as it is used:** `:159-164`, step 4 of the loop, has the writer add the phrase to § Tells and to `tools/prose-check`'s list. A design choice the file states (`:187-188`), and the reason a renovation lane may only touch it under a stream brief.
- **Positives read:**
  - `:18-22` the site's voice is the bar;
  - `:88-93` the first person singular (D-WORKFLOW-074) with the other contributors' *we* left as theirs;
  - `:165-170` others' sections are reported, never fixed in passing;
  - `:171-175` screenshots by a walk on the VM, a frame with an account's name through `tools/png-blackout` (`vm-first.md`, `engineering-practices.md`'s device rule);
  - `:187-188` the file knows the check fails it.

## release-notes/SKILL.md (130 lines)

- **L-11 confirmed by reading:** `:19-21` *"The body of a release on `pixelelated/distribution` (`tools/fork-publish-release` uploads the files; the note is written by hand and pasted with `gh release edit --notes-file`)"*. Against `device-builds.md:596-597` at the tip: *"`tools/fork-publish-release --prepare <immutable-bundle>` emits a checked local GitHub naming/asset plan only. The old date/newest-file/clobber/undraft path is retired."* Publication waits on #265, #344 and #528. To check: the tool's own usage, read from its source (never run), and the releases this repository has published.
- **New lead -- the description says what the body forbids:** `:3`, the description every session lists, says both a release note and a PR description carry *"the plumbing (commits, issues, runs) in a details block underneath"*. `:100-102` forbid any plumbing in a PR description (*"No decision IDs, no `tools/…` names, no fork issue numbers, no run numbers"*), and `:97-99` any heading or label (reader item 1). A session that picks the skill by its description and writes the PR body by it puts in a details block the body bans. The fix is a description edit, so a load change (Q5) with its length before and after.
- **Q7, from the reader:**
  - `:83` *"three or four short paragraphs"*, three listed (item 2);
  - `:66` *"`tools/prose-check` fails a plural"* against `:125`'s `PROSE_FIRST_PERSON=fail` for a PR description (item 3; to check: the tool's default);
  - `:36` *"the H700 choice (the regulator read)"*, a term of art with no gloss (item 6);
  - `:54` *"Every bullet traces to an entry in `docs/cloud-sync-changelog.md`"* when a release carries more than cloud sync (item 9).
- **A status true once:** `:68` *"Two heads in one release (as RC1 has)"*.
- **Tool options the skill states, to check against each tool's source:** `:119-121` `tools/pr-stack-check` *"refuses a description that carries any of the above"* (#955 is an open bug against that tool's header); `:125` `PROSE_FIRST_PERSON=fail`.
- **Positives read:**
  - `:93-96` no assistant anywhere upstream-bound (D-WORKFLOW-078, #333);
  - `:111-113` the commit message is the title and the first paragraph, no trailer;
  - `:115-121` one PR, one commit (D-WORKFLOW-079);
  - `:128-130` the harness's footer removed before `gh pr create`.

## What the checks settled (`stage-b/checks-writing-pair.out`, 03:13:15Z, and `checks-writing-pair-2.out`)

- **L-11:** `tools/fork-publish-release:6-7` at the tip says *"No upload, tag creation, asset replacement or publication occurs. The previous newest-file/date/undraft path is retired (#265, #530)."*, and its one option is `--prepare` (`:130`). The skill's *"`tools/fork-publish-release` uploads the files"* is false of the tool. The retirement and the skill's sentence are dated in `checks-writing-pair-2.out`. **Already written:** the one release published while the sentence was true is `rc1-20260929` (2026-09-29, the day both skills were written), and the four before it are older than the skill. No release has been published since the path was retired, so nothing a reader did on the sentence's strength reached the releases page.
- **`prose-check`:** strict only under `docs/releases/` or with `PROSE_FIRST_PERSON=fail` (`:59`). Elsewhere a plural is a warning, so `release-notes:66`'s *"fails a plural"* holds for a note drafted under `docs/releases/` and not otherwise.
- **`pr-stack-check`:** its `BANNED` pattern (`:128`) is assistant names, `Generated with`, `Co-Authored-By`, decision IDs and `tools/` names. `release-notes:119-121`'s *"refuses a description that carries any of the above"* names five things, of which the tool checks the assistant and the plumbing; headings, labels, the plural and sales it does not.
- **L-27, each checkbox against the text:**
  - **#333 `:17`** asks for `developer-relations` to carry a *"PR descriptions and commit messages"* section. That section lives in `release-notes` (§ The PR description, `:73-121`): the checkbox names the other skill. Its owner's to re-word; read, not a T38 fix.
  - **#326 `:25`:** the skills' half holds -- `developer-relations:88-93` and `release-notes:61-66` state the first person singular -- and `prose-check` fails a plural where the note lives (above). The live note's half is #326's own (the count of plural words in `rc1-20260929`'s body is in `checks-writing-pair-2.out`).
  - **#341 `:19`:** a future relaxation after the repositories' transfer; nothing in the skills to read yet.
  - **#645 `:25`** asks that *"The `release-notes` skill's PR-description shape carries the template's sections and the disclosure"*, and the skill forbids both (`:93-99`: no assistant anywhere, no headings or bold labels). A tracker checkbox against a decided rule (D-WORKFLOW-078): the coordinator's, at the pause.
  - **#953 `:11`, #955 `:12`:** *"Every sibling hunted"* lines in their traces, naming these skills as the tools' callers; no change to the skills' text follows.
  - **#268 `:17`** asks for *"the skill that writes issues"* to carry `- [ ] <behaviour> -- <artifact that ticks it>`. The skill in the 52 that writes issues is `code-auditor`, whose Phase 6 asks for one checkbox per punch item (`SKILL.md:541-552`) and not the artifact shape. A lead for `code-auditor` (Q2), in D-QA-044's words.
- **The dates (`checks-writing-pair-2.out`):** the skill's sentence came with `9404f23c55` (2026-09-29), and the tool's *"No upload ..."* with `f10eec1306` (2026-10-09, *"image: identify rolling builds by version, UTC time and source"*). True when written, false ten days later: the family *a count or a name true once*, and a sentence a reader acts on wrongly since 2026-10-09. `rc1-20260929`'s body carries `0` first-person-plural words, so #326's live-note half reads as done (its own to tick).
