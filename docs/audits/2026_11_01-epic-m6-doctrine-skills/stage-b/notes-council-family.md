# Stage B, the auditor's read: the council family -- `council`, `council-research`, the eight agents (T38, #685)

The export's (ruling (d)): read, never edited here. Every finding is an inherited item for #911's refresh or a #585 line (D-WORKFLOW-088, -164, -165). Read after the reader's pass (`reader-council.md`, `reader-council-research.md`, `reader-agents.md`).

**Every read of the family's text went through § 5's mask `M`** where a line was printed through the shell. A credential's variable is named here, never its value, and no line of the family is credential-shaped (A-09).

**What the auditor read whole, and what at its lines:**
- **Read whole:** `council/SKILL.md`, `council/IMPORTED-FROM.md`, `council/COUNCIL-BUNDLE.md`, `council/references/member-roster.md`, `council-research/SKILL.md`, and the eight agent files.
- **Read at the lines the leads (L-30 to L-50) and the readers name:** the other references of both skills, `council-research`'s 11 and `council`'s remaining 9 with the checksum list. The reader's pass read every line of all of them; the lines read here are recorded with each note.

## council/SKILL.md (193 lines)

- **L-32 withdrawn by reading:** `:188-190` *"**Wrapped by:** `council-research` skill (...). See its `references/phase-4-council-deliberation.md` for the handoff shape."* -- *its* is council-research's, whose file it is (`council-research/references/phase-4-council-deliberation.md`, present). The path is right; only a line-at-a-time checker reads `:190` alone and misses `:188`'s subject. So `t38-checks.sh`'s `refs` step allowlists the line with that reason, and L-32 goes to `02` as withdrawn with this read.
- **L-38:**
  - `:5` `tools: [readFile, edit, search, runSubagent, todos]`, the VS Code tool names;
  - `:17-21` the VS Code Copilot profile, `model: - "Claude Fable 5.1 (copilot)"`;
  - `:3`'s triggers *"trio analysis"*, *"run a trio process"*, against `:44-45` *"Ambiguous legacy "trio" wording never authorizes reducing a formal council"* (reader item 1).
- **L-39:** `:121-125`, the coordinator table, *"Claude Code | Claude Opus 5"*, *"Codex | GPT-5.6 Sol"*. A coordinator role, not a seat, so `adversarial-council.md`'s seat floor does not bind it; but this session is Claude Code on Opus 5.5, so the row is a fact true once.
- **L-43:**
  - `:26` (*"Promoted from `.github/agents/trio-council.agent.md`"*) and `:191-192` (*"**Replaces:** `.github/agents/trio-council.agent.md` (retained as a thin deprecation pointer per M64.P1.5 Epic 3 / #2825)"*);
  - the pointer is not in this tree (`stage-b/checks-council.out`), and #2825 and #2826 are the source estate's.
- **L-45:** `:25` *"Rasteratops v1.4.1"*.
- **Q7:**
  - `:78` *"one at a time"* against `pipeline.md:155-156` (*"retired"*, reader item 2);
  - `:83-84` and `:162-164` lint before advancing, against `pipeline.md:202-206`'s seal-first order (item 3);
  - `:95-97` *"Source case: the 2026-05-22 / the 2026-05-22 council run step-5 meta-retrospective (the source estate's repository, research/council-runs/)"*, the date doubled -- an editing artifact of the import, the same shape as R3's *"redaction artifact"* in `COUNCIL-BUNDLE.md`;
  - `:134-135` *"until council runs move to Tursi"*, Tursi defined nowhere in the 52.
- **Positives read:**
  - `:107-112` the five installed seats (D-WORKFLOW-109, -135);
  - `:157-161` every member call through the Facilitator, never a direct provider call;
  - `:179-184` a failed member halts the run, never four.

## The eight agents (334 lines)

How they were read: `council-member-claude.agent.md` whole, the four other active seats and `mistral` as their `diff` against it (each line read once, in claude's file or in the diff), and `deepseek` and `grok` whole. All through the mask.

- **L-40 confirmed:** `council-member-gemini.agent.md:5-13`'s comment says *"declares the direct-API identity ... the substrate (`ai-studio`, i.e. Google's Generative Language API -- NOT Vertex AI ...) The Facilitator's `modelMatches()` predicate uses literal matching against the response-body `modelVersion` field ... § Substrate A"*. The line under it, `:15`, reads `"google/gemini-3.8-flash (OpenRouter, effort=high)"`. A comment that contradicts its own line (reader item 1).
- **Q7, the predicate named three ways:** claude `:9-12` `modelMatches()` *SEMANTIC* (§ Substrate C), gemini `modelMatches()` *literal* (§ Substrate A), gpt `openRouterModelMatches()` *semantic* (§ Substrate C) (reader item 2). Which function the Facilitator runs is T45's file to say; the agents' comments disagree among themselves either way.
- **L-38:**
  - `claude :25-31` -- shared word for word by gemini, gpt, kimi, muse and mistral, absent from deepseek and grok -- is the *FACILITATOR-MANDATORY* block;
  - it links `../../.github/instructions/council-substrate-integrity.instructions.md`, which is twice wrong: the Copilot-era name, and a relative path that climbs out of the repository from `.claude/agents/`;
  - it names issue #3059 (`:15`, `:28`, `:31`), the source estate's.
- **L-41:** every description opens *"... Use when running multi-model analysis"* (claude, gemini, gpt, kimi, muse) while `claude :25-31` says *"refuse the task"* without the Facilitator. Every file declares `tools: [readFile, edit, search]`, VS Code names. This session's own agent listing shows all eight as invocable types, deepseek's and grok's descriptions reading *"Historical imported ... Inactive in pixelelated; do not invoke."* -- a harness observation, recorded so.
- **L-35 narrowed by reading:** where the path is relative, the sentence names its skill in words, so a reader resolves it.
  - `claude :37` (shared by gemini and gpt) reads *"see the council skill's `references/member-roster.md`"*, and `deepseek :17`, `grok :17` *"Use the council skill's `references/member-roster.md`"*.
  - `kimi`, `muse` and `mistral` `:7` write the repo-rooted `.claude/skills/council/references/member-roster.md`.
  - R3 § 2.7's check, which FAILed all 8, resolved the path from `.claude/agents/` alone. The brief's own `refs` rule (*"or under the skill the same line names"*) resolves each.
  - What remains is a checker rule (`allow-legit.txt`'s class, for #1373), not a dead path.
- **The inactive three, as written (ruling (e)):**
  - `deepseek` and `grok` say *"Do not invoke it or substitute it"* (`:12-13`) and *"retains the imported model declaration for the pin verifier"* (`:13-15`).
  - `mistral`'s description says it is outside every run profile, and its body says *"Historical recipe; do not invoke"* (`:21`). Yet its `:29` still lists the roster as *"(Claude, Gemini, GPT, Kimi, Mistral)"*, and it carries the mandatory banner (reader item 10).
  - Kept, pinned. Their cost is Q5's (the descriptions' lengths in every listing).
- **Q7, the seats' instructions differ:** `muse :34` adds *"Do not manufacture disagreement or adopt an assigned national/cultural persona"*, which no other seat carries (reader item 14). `kimi :21`'s *"1.05M context"* beside *"the seat's 262144 ceiling"* (item 12).
- **The roster lines (L-44, for the `roster` step):** claude `anthropic/claude-fable-5.1 (OpenRouter, effort=xhigh)`, gpt `openai/gpt-6-astra (OpenRouter, via openai, effort=max)`, gemini `google/gemini-3.8-flash (OpenRouter, effort=high)`, kimi `moonshotai/kimi-k3 (... effort=max)`, muse `meta/muse-spark-1.3 (OpenRouter, via meta, effort=max)`. Claude's and GPT's slugs and efforts equal `adversarial-council.md:77-78`'s rows (A-02's runs, chunk 20).

## council/IMPORTED-FROM.md (127 lines)

- **L-48, read whole:** the refresh procedure **is** here, in six lines -- `:92-97` *"## Refreshing / Ask for a fresh export (`COUNCIL-BUNDLE.md` says how it was made), check its `SHA256SUMS`, copy it over the same paths, re-apply the adaptations above, re-pin what changed with a reason, run `verify-pins`, `efforts --strict` and `test`, then probe the five seats (`research/seat-probes/`). Never relocate the files again."* -- with `:52-54`'s re-application of the wordlist sweep and `:99-102`'s roster-change rule.
  - So #343 `:14`'s expectation (*"the refresh procedure in `.claude/skills/council/IMPORTED-FROM.md"*) is met in outline.
  - #850 `:14` (*"records the local change against the import"*) is met by `:15-50` and the two October 22 sections.
  - What #1045 says is missing is read from its body (`stage-b/checks-council.out`) before the Q1 row is written.
- **L-37:** `:104-113` *"## Local retry correction -- October22 (#636)"* and `:115-127` *"## Local audit route -- October22 (#638)"*, the 25 lines `next` lacks. To check: a register row naming #636 or #638.
- **L-34, half answered here:** `:12-13` *"The bundle record and its checksums describe the original delivery. Current `verifier-pins.json` entries account for local changes to pinned files."* -- the true statement of what the sums are, which `COUNCIL-BUNDLE.md:4` (below) does not make.
- **Command blocks:** `:83-90` -- `tools/council/run verify-pins`, `efforts --strict`, `test`, `invoke --member muse ...`, `start --run-dir ...`, `lint --at-step 1 --strict ...`. Every one is a call of the wrapper the never-run list forbids, `test` included, though it says *"no provider calls"*. Checked for the wrapper's subcommands in its source, never run.
- **Q7, the spaces lost:** `:104` and `:115` *"October22"*, `:106` *"now1.14.1-pixelelated.1"* and *"with exit8"*; the same as `worktrees.md`'s *"October12"* and `device-builds.md`'s *"about138 GB"*. Each reads as a missing space, likely a non-breaking space stripped in an edit.
- **Provenance read:** `:68` *"from the `pfi/pfi-collaboration` lineage via marvin's clone"*; `:72-73` the runner *"loads `~/.config/council/env`"* (the file named, never opened; `:78` names `OPENROUTER_API_KEY`, a variable, never a value).

## council/COUNCIL-BUNDLE.md (34 lines)

- **L-34:** `:4` *"**Files:** 94, byte-identical to that commit, at their scaffold paths."* -- true of the import, not of the tree (`BUNDLE match=52 diff=39 absent=3`). `:11` names `node scripts/verify-pins.ts` as the check.
- **The redaction artifacts R3 § 7 item 7 saw, located:**
  - `:26` *"They name the source estate.space and scaffold's custody paths."* -- the wordlist sweep (`IMPORTED-FROM.md:34-38`) replaced a name inside a domain and left `.space`;
  - `:9` ends mid-sentence, *"Unpacked into an existing project, commit them there"*, no stop.
- **Command blocks:** `:11-14` -- `node scripts/verify-pins.ts`, `node --test ...`, `npm exec --yes --package=tsx@4.22.4 -- tsx --test ...` (a registry fetch), `node --test ...`. All forbidden here; the bundle's own record of how it was checked standalone, not an instruction to this tree.

## council/references/member-roster.md (207 lines, read whole)

- **L-44, the roster table:** `:21-25`, as follows:
  - claude `anthropic/claude-fable-5.1` `xhigh` 1,000,000;
  - gemini `google/gemini-3.8-flash` `high` 1,048,576;
  - gpt `openai/gpt-6-astra`, OpenAI provider, `max`, 1,050,000;
  - kimi `moonshotai/kimi-k3` `max` 1,048,576;
  - muse `meta/muse-spark-1.3` `max` 1,048,576.

  Claude's and GPT's rows equal `adversarial-council.md:77-78` (slug, effort, context, GPT's provider pin), and all five equal the agents' `model:` lines. They agree today (a positive), and nothing checks that they keep agreeing. `:35-36` names the Facilitator's `OPENROUTER_SEATS` table as *"the authority and this table mirrors it"*.
- **L-39:** `:84-85` *"Claude Code → Claude Opus 5, Codex → GPT-5.6 Sol"*, the coordinator mapping again.
- **L-38, two texts:** `:11-16` *"All five members are invoked ... on the all-member **OpenRouter** route by default ... Direct-provider APIs remain an explicit max-independence fallback"* against `:119` *"Direct-API is the substrate-of-record."* (reader item 4); `:114`'s *"Copilot subagent (legacy)"* row.
- **Editing artifacts of the wordlist sweep:** `:93-95` *"September 25 controls isolated shared-pool 429s on `mistral/zdr` (the canonical recovery record (scaffold's forge, docs/planning/council-five-seat-794/recovery-20260924.md))."*, a sentence that lost its verb; `:27-31`'s *"the source estate's PR #4453"*.
- **Command block:** `:146-151`, `node scripts/council-invoke.ts --member <...> --provider openrouter --prompt "Reply with exactly the single word PONG ..." ...` -- a provider call; never run. Its options are checked against the Facilitator's source in `stage-b/checks-council.out`.
- **Positives:** `:128-138` five seats or none, the coordinator non-voting; `:161-183` failure recovery never shrinks the denominator.

## council-research/SKILL.md (562 lines, read whole)

- **L-30:**
  - `:22` names `scripts/lint-council-research-digests.ts`, `scripts/summarize-council-research-lints.ts`, `scripts/lint-council-research-provenance.ts` and the three `scripts/__tests__/` files (the six `MISSING` of A-08's loop and the three test files, stage A);
  - `:233` `scripts/lint-council-research-digests.ts`, `:243` and `:392` `npx tsx scripts/summarize-council-research-lints.ts`, `:373` `npx tsx scripts/lint-council-research-gates.ts`;
  - `:145`, `:189-190`, `:539-540` *"the Tier-3 enforcement file `council-research.instructions.md` (E5 deliverable)"*, *"provides the enforcement layer for authored artifacts"*;
  - **`:407-411` *"The two existing pre-commit hooks (`council-research-provenance`, `council-research-digests`) already enforce this gate at commit time"*** -- to check: no such hook under `.githooks/`. The enforcement layer is claimed as present, in the tense `working-principles.md` calls worse than an honest absence.
- **L-31:** `:13` `Researcher Agent` in the `agents:` list, `:35`, `:98-100`, with no definition under `.claude/agents/` (`researcher agent rc=128`, stage A).
- **L-38, the Copilot surface and its dead links:**
  - `:5` `tools: [readFile, edit, search, runSubagent, todos]`;
  - the five `.instructions.md` names: `:145`/`:190`/`:539` `council-research.instructions.md`, `:147` `silent-failure-discipline.instructions.md`, `:165` `research-versioning.instructions.md`, `:229` `../../../.github/instructions/subagent-orchestration.instructions.md`, `:296` `subagent-output-verification.instructions.md`.
- **L-39:** `:17` `model: - "Claude Opus 4.8 (copilot)"` -- a model `adversarial-council.md`'s *Deprecated* bullet bars from the seats (the coordinator's profile here, not a seat).
- **L-42:** `:490-492` *"the path-collision rationale with the council skill's `research/trio-runs/` path"*.
- **L-46 and the front matter's weight:** `:21` `revision_note` and `:22` `origin`, one YAML value of several thousand characters -- a version history (v1.1.0 to v1.5.0 with every RC) loaded with the description's file. Q5 measures it.
- **L-47:** `:196-197` the output root `research/council-research/` (0 entries, stage A), and `:183-185` *"The canonical retrofitted example is R2-210 (`research/council-research/2026-05-24-researcher-federation-substrate/phase-0-prior-run-evaluation/` ...)"* -- to check: absent, the source estate's.
- **Q7, from the reader:** `:5`'s `runSubagent` against `phase-1-independent-research.md:107-122`'s ban on it (item 3); `:80`/`:544-546` *"repair-only"* Phase 2.5 against `phase-3-adversarial-review.md:104-111` (item 4); `:199-201`'s *"never a reduced roster"* against the references' *"fall back to (N-1)"* (item 1, to check); `:3`'s *"bedrock-adjacent"*, defined nowhere (item 14).
- **Positives read:** `:128-148` the clinical-synthesis invariant; `:315-318` a hash mismatch is investigated, not smoothed; `:552-557` a failed gate is preserved and replayed, never rewritten.

## The references at their lines (`stage-b/council-lines.sh` and `.out`; `stage-b/checks-council.sh` and `.out`, 03:16:59Z)

- **Confirmed:**
  - **L-30:** `methodology-primitives.md:224` and `phase-3-adversarial-review.md:170` (`scripts/lint-council-research-replay-metadata.ts`), `phase-1-independent-research.md:142` (`scripts/lint-council-research-provenance.ts`), `model-verification.md:542` (`scripts/lint-agent-model-arrays.ts`). `.githooks/` holds no council-research hook (`0`), against `council-research/SKILL.md:407-411`.
  - **L-31:** `phase-2-clinical-synthesis.md:110`, `:246` and `model-roster.md:26-27` link `.claude/agents/researcher.agent.md`.
  - **L-33:** `provenance-schema.md:594` names `council/references/step-prompts/step2-peer-review.md`. That file is absent; `prompt-templates/step2-template.md` is present.
  - **L-36:** `scripts/lib/council-roster.ts:25-26` (`"grok-shadow"`, `"deepseek-shadow"`), `:35-36` (`decisionAuthority` -> `"non-binding"`), `:87-90` (the Mistral override through `OPENROUTER_MISTRAL_MODEL`, a variable named, its value never read).
  - **L-37:** `0` register rows name #636 or #638.
  - **L-39:** `provenance-schema.md:424`, `:587`, `:640` `"council-research orchestrator (Claude Opus 4.8 (copilot))"`; `model-verification.md:63-69`, a provider table of `gpt-5.5` and `Kimi-K2.6` on Azure deployments and `mistral-large-3` (no Muse); `:385` the `gpt-5.5-2026-04-24` PASS example.
  - **L-42:** `research/trio-runs/` named at `context-loading.md:124`, `output-conventions.md:25`, `pipeline.md:82`, five council-research lines; absent from the tree, while `research/council-runs/` holds `5` entries.
  - **L-43:** `.github/agents/trio-council.agent.md` absent; `context-loading.md:47`, `:60` and `phase-5-deliverable.md:118` name `docs/architecture/bedrock/`, absent.
- **L-48, read against #1045:** #1045's F-14 says *"no refresh procedure is written, and the export's pristine bytes are not kept"*, and its checkbox asks for a procedure *"naming: where the bundle comes from, the pristine bytes kept ..., the adaptations re-applied in order"*. `IMPORTED-FROM.md:92-97` is an outline that names where the bundle comes from and the order, not where pristine bytes are kept. So: #1045's *"no procedure"* is too strong, its *"no pristine bytes"* stands. The inherited row says both.
- **L-47, a delta:** `3` work-log lines in `3` files name `council-research` at HEAD (the brief's *"2 work-log lines over 2 days"* was R2's at `926d1fbaee`).
- **New, for #911's list (the export's, never edited here):**
  - **The roster that shrinks in the references, against the skill that forbids it.** *"consider falling back to (N-1) roster"* (`phase-1-independent-research.md:150`, `:154`); *"if Phase 1 used 5, 4, or 3 members"* (`phase-4-council-deliberation.md:59`); *"Active roster (3, 4, or 5 members"* (`phase-5-deliverable.md:172`, `council/references/output-conventions.md:452`). Against `council-research/SKILL.md:199-201`, `model-roster.md:3-6` (*"there is no fallback to four or three"*) and D-WORKFLOW-135. Reader item 1. A reader of Phase 1's failure table acts against the five-seat rule.
  - **The vote shapes:** `pipeline.md:416-417` names *"2-1-1"* (four ballots of five) and *"5-0"*, which `voting-rules.md:57-58` calls *"impossible without a self-vote"*. Reader item 7.
  - **The seal order:** `pipeline.md:202-206` puts the seal before the lint, which `council/SKILL.md:83-84` and `:162-164` never mention (reader item 3); and `pipeline.md:155-157` retired the *"one at a time"* guidance that `SKILL.md:78` still gives.
  - **The Forge:** `pipeline.md:62-64` (*"requires the in-tree Forge preflight"*) and `:458-460` (a *"Forge issue"*) against `IMPORTED-FROM.md:27-33` (*"the Forge write preflight ... gone"*); `pipeline.md:468` names a `product-specs` skill, absent.
  - **The substrate of record:** `model-verification.md:16` *"direct-API"* against `member-roster.md:11-16`'s OpenRouter default (L-38's family).
  - **`output-conventions.md:131`** *"New runs use the installed `FACILITATOR_VERSION` (1.6.0 for this adoption)"* against `IMPORTED-FROM.md:106`'s *"1.14.1-pixelelated.1"*. Reader item 15.
  - **`phase-1-independent-research.md:107-122`** forbids `runSubagent`, while both skills' `tools:` lists offer it (reader item 3).
- **Command blocks checked, never run:**
  - `tools/council/run`'s subcommands (`invoke`, `lint`, `start`, `prompt`, `seal`, `summary`, `verify-pins`, `verify-chain`, `verify-seals`, `efforts`, `drift`, `test`) cover every one `IMPORTED-FROM.md:84-89` uses.
  - `scripts/council-invoke.ts` declares every option the blocks name (`--member`, `--provider`, `--prompt-file`, `--prompt`, `--output`, `--max-tokens`, `--max-retries`, `--source-manifest`, `--council-research-run-id`, `--phase`, `--invoker-agent-name`), and `scripts/lint-council-run.ts` declares `--at-step`.
  - The six scripts L-30 names are absent, so their blocks cannot run anywhere.
