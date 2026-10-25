# Analysis — M6.P2 T45, the council toolchain and runner (#692)

## Executive summary

The council toolchain on this fork is scaffold's export, and it is accounted for:

- **The members:** 52, read at `8ebaf8daad`. 41 are byte-equal to the export's SUMS. The 9 that differ are each explained by an adaptation item or a re-pin reason. The 2 the SUMS does not list are the fork's own wrapper and manifest.
- **The checks:** `verify-pins`, `drift`, the offline `efforts` check and the 185 tests pass on both the hash and the lane's tree.
- **The seats:** the five sit on `adversarial-council.md`'s floor on both trees.
- **The record:** all ten seat calls of this week verify identity, effort and provider.

No defect was proven, so this slice files no `bug`. Every finding is either a lead for the coordinator or the export's owner, or a design recorded with its sentence. The one that matters most, with a smaller drift beside it:

- **F-01: the lane's tree carries a local Facilitator fork** (`1.14.1-pixelelated.2`, #636/#638) that no register row records, while D-WORKFLOW-088 describes the toolchain as scaffold's, refreshed only by copying.
- **F-05 is a Low drift, not a missing check.** `council-substrate-integrity.md`'s rules 4 and 5 still read as unconditional and name two council-research lints that exist in no commit here. Its own adoption note (`:42-46`) says those lints are carried by the source estate only, and gives the manual check that replaces them.

Outside the slice, two committed council-run seal keys went to the coordinator as #1043 (F-03).

## Acceptance-criteria scorecard

| # | Criterion | Stage B |
| --- | --- | --- |
| 1 | the folder holds `00` to `05` | `00` to `04` here; `05` at stage D |
| 2 | the lint `PASS` | stage C (`--phase pre-issue`), then close |
| 3 | the local review plan; no provenance file | met: `second-opinions/review-plan.json`; 0 provenance files |
| 4 | the punch list at Phase 7 outcomes | stage D onward |
| 5 | `reviewed-at` `32a34393dd`; members differ on exactly the two commits' ten files | met (`00` § Stage A) |
| 6 | `01` § Scope | met |
| 7 | 52 coverage rows | met (`02` § Coverage; the `awk` count prints 52) |
| 8 | § Provenance, § Reconciliation, the branch's delta | met (`02`) |
| 9 | § The runs on both trees, and `lint` over the recorded runs | met (`02` § The runs) |
| 10 | keyless runs; no forbidden act | met (`00`) |
| 11 | Q4 currency table | met (below) |
| 12 | Q6 dead-end rows | met (below) |
| 13 | Q7 descriptions | met (below) |
| 14 | `proved:` cells; no member changed by the lane | met (`02` § Proofs) |
| 15 | the retro | stage G |
| 16 | the five checkers | at hand-back |

## Risk assessment

- **Low runtime risk.** Nothing here reaches an image (`reach: n/a`, 52 of 52), so a regression would show in a review seat's call, not on a device. The Facilitator's per-call verification fails closed on identity, effort and provider (exits 3, 7, 6), and the routing tests pin that behaviour.
- **Provenance risk (F-01).** The fork's council differs from its source estate in behaviour (a stop, a route) with no register row. A refresh that copies scaffold's next export over the tree would remove #636 and #638 unless that export carries them. `IMPORTED-FROM.md` asks to *reconcile these scoped changes with a newer source-estate export before upstream contribution*. That is a sentence, not a mechanism.
- **Currency risk (F-06, F-07).** With no lockfile, each `npm install` takes the registry's latest within the ranges, and no seat record names what ran. The seat-efforts snapshot is 27 days old, and a fresh reading needs the key.
- **Record risk (F-02).** Completed runs cannot be linted on the current tree after any re-pin, and nothing says that this is expected.

## Coverage boundary

- **Read:** the 52 members at `8ebaf8daad`, and the ten changed files on the branch. Read for context and not as members: `IMPORTED-FROM.md`, `COUNCIL-BUNDLE.md` and the SUMS; the two 2026-10-22 evidence folders; the four recorded council runs' manifests and genesis files; the ten seat provenance records of T9, T10, T12 and T14; the eight agent descriptions' headers; the two council rules and the `instruction-files.md` rows.
- **Run:**
  - `npm install`, `verify-pins`, `drift`, the offline `efforts` and `test` on both trees;
  - `lint` over the four recorded runs, explicit and by discovery, on both trees;
  - `lint` at the 09-30 runs' own close-out commit.
- **Not run:**
  - `invoke` (any provider call);
  - `efforts --refresh` (it needs the key);
  - `verify-seals` (it reads a run's seal key);
  - `verify-chain`: it needs no key, but it was not needed for the table;
  - the Mistral tokenizer's Python setup (`IMPORTED-FROM.md`: not installed).
- **Unreadable here:**
  - the export's own bytes for the 9 differing members (in no commit);
  - any export newer than `7be6721b` (the scaffold checkout on this host is older: `20c0a77`, corpus 3.29.1).
- **Never read:** the key file, `~/.ROCKNIX/options`, the forbidden-terms list, and the two committed seal keys (their names were listed, their contents never opened).

## Second opinion

**Depth: Local, by the slice's plan** (`slices.json` k 45, *a provenance table*; plan § 6c; D-WORKFLOW-184 tier exception). There is no reviewer seat and no provider call, and `second-opinions/` holds only `review-plan.json`. **The lint and the counts are the check:** the four SUMS counts on both trees, the pins' counts, the 52 coverage rows and the toolchain's own runs, each re-runnable by the coordinator on an export of the tip.

## Finding Verification

Every finding was checked against the artifact named, not against the brief's or a commit message's words.

| Id | Finding | Severity | Question | Verified by | Verdict | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | the lane's tree carries a local Facilitator fork (`1.14.1-pixelelated.2`, #636/#638) that no register row records; D-WORKFLOW-088 describes only copying the export | Medium | Q7 | `grep -c -E '#636\|#638\|1\.14\.1-pixelelated' docs/decision-register.md` prints 0; `FACILITATOR_VERSION` at `:855` | confirmed | lead for the coordinator (the D-WORKFLOW-088 question to #346); the lane writes no row |
| F-02 | a completed current-contract run is unlintable on the current tree after any re-pin (genesis binds the pins), and the local version bump left `1.14.0` runs neither installed nor historical | Low | Q3 | the four lint runs, explicit and by discovery, on both trees; the 09-30 runs pass at `4fa6e04948` | confirmed as a consequence of a design | lead for the export's owner (a way to retire a contract, or the written expectation that a run is linted at its own commit) |
| F-03 | two council-run HMAC seal keys committed, on `next`, public; outside the 52 | Medium | Q2 | `git ls-files`, `git ls-tree -r next` (unread) | confirmed | deferred to **#1043** (the coordinator's; removed on its branch at `0fa5a20c5f`) |
| F-04 | `IMPORTED-FROM.md` item 3: *ten literals in the two test files*; the bytes show 7 run-time-built keys, in the routing test and the toolchain test, and none in the seat-efforts test | Low | Q7 | marker counts at the hash (`02` § Reconciliation) | confirmed (7 found; 3 unresolvable without the export's bytes) | lead for the coordinator (a skill file; the lane edits none) |
| F-05 | `council-substrate-integrity.md` rules 4 and 5 tell the orchestrator to run `scripts/lint-council-research-provenance.ts` and `scripts/lint-council-research-digests.ts` in a council-research run; neither exists in any commit, and the `council-research` skill names them too. The rule's adoption note (`:42-46`) says they are carried by the source estate only and gives the manual fallback, so the drift is that rules 4 and 5 read as unconditional | Low | Q7 | `git cat-file -e` at the hash and on the branch; `git log --all -- <path>` empty; the adoption note read | confirmed; first stated as Medium and *a mandate after every call* at stage B (posted 03:15), corrected | lead for the coordinator (the rules carry their own fallback, or the lints come with the next export) |
| F-06 | no lockfile (by policy, `.gitignore:67`), and no seat provenance record names the `tsx` or Bedrock SDK version that ran | Low | Q4 | `.gitignore:66-67`; `grep -c -i 'tsx\|npm\|bedrock'` of a record prints 0 | confirmed | lead for the export's owner |
| F-07 | the seat-efforts snapshot is 27 days old (`refreshed_at` `2026-09-28T05:09:37Z`); the branch added the Argon entry from a 2026-10-22 catalogue without moving it | Low | Q4 | the file on both trees; `0ceb2994c5`'s README | confirmed | lead (a fresh reading needs the key) |
| F-08 | the Mistral counter chain and its requirements, the Bedrock dependency (a Mistral-only backup route), `forge-write-status.mjs` and `owner-queue-lint.mjs`, and the four `council-stage-*` CLIs with no wrapper route | -- | Q6 | the references map (`stage-b/refs.txt`); `council-invoke.ts:108-111`, `:1552-1563` | confirmed | design: kept because the export carries it (D-WORKFLOW-088) |
| F-09 | `invoke` accepts `--member grok\|deepseek\|mistral` and `--provider azure\|bedrock`; only the agents' prose and the rules say not to | Low | Q6 | the usage text (`council-invoke.ts:2877-2885`); no profile check on the argument path | confirmed by reading (no call made) | lead for the coordinator |
| F-10 | the wrapper's env guard is one-sided (an absent or unreadable file is skipped in silence; a readable one at another mode is refused), and `COUNCIL_ENV_FILE` is not in its header | Low | Q2 | `run:21-28` | confirmed by reading | lead (a member; the lane changes none) |
| F-11 | npm 11 skipped esbuild's postinstall under `allowScripts`; `tsx` worked (`test` rc 0) | -- | Q2 | `stage-a/branch/npm-install.out` | confirmed | design: no effect observed; recorded so a later failure has its first clue |
| F-12 | `tools/council/package.json`'s description names the retired `pfi/pfi-collaboration` lineage | Low | Q7 | the file | confirmed | lead |
| F-13 | `run test` runs three files under `set -e`, so the first failing file hides the later two verdicts | Low | Q3 | `run:18`, `:44-48` | confirmed by reading | lead |
| F-14 | the refresh is prose (*"A refresh re-applies these adaptations"*), with no recorded procedure or tool; the export's pristine bytes are not kept, so our adaptations cannot be diffed against them here | Low | Q1 | `IMPORTED-FROM.md`; the all-history search | confirmed | lead for the coordinator |
| F-15 | `council-substrate-integrity.md` names exit 3 alone as the halt; the Facilitator also stops on exits 6 and 7, and exit 8 on the branch | Low | Q7 | the exit table (`council-invoke.ts:75-94`) and the branch's exit 8 | confirmed | lead |

**Withdrawn at stage B:** the reading that `lint-council-run.ts` is inconsistent with `verify-chain`/`verify-seals` on historical runs. Its discovery path reports them as historical inventory (`02` § The runs). Posted on #692 at 03:03 and corrected there at 03:05 UTC.

## Renovation face

### Q1 Modernize

- **The cost of the mirror.** The export's paths sit at the repository root (`scripts/`, `seed/`, two root JSON files) beside the build engine's own `scripts/`, so the slice's globs also catch 30 build-engine rows (`stage-a/others.txt`). The push guard and `fork-workflow.md` carry a second copy of the council path set (18 pattern hits in `.githooks/pre-push`), which a refresh adding a path must update by hand.
- **No recorded refresh procedure (F-14).** *"Refreshed by copying the next export"* is prose in `IMPORTED-FROM.md`. The five adaptations are re-applied by hand, and the export's pristine bytes are not kept anywhere here to diff against. Lead.

### Q2 Standards

- **The wrapper** (`tools/council/run`): `set -euo pipefail`; the env file is sourced only when readable at mode 600; `exec` into `tsx`. The guard is one-sided (F-10). Every run in this slice set `COUNCIL_ENV_FILE=/nonexistent`, which is the guard's silent branch working as intended.
- **`npm install` without a lockfile**, by policy (F-06). npm 11 skipped esbuild's postinstall (F-11).
- **The provenance records against `adversarial-council.md`:**
  - All ten records carry `facilitator_version`, the declared model, `final.verification.observed` with `model_identity_source` `provider_response` and PASS, `final.effort_verification` PASS (evidence `reasoning_tokens`), and `final.provider_verification` PASS (observed `OpenAI`, or `Google` for the Argon route).
  - `allow_fallbacks: false` is in the recipe (`stage-a/roster-*.txt`), not in the record; the record's provider check is what shows its effect.
- **The seal keys** (F-03, #1043).

### Q3 Bugs

**None proven.** Every check the toolchain ships passes on both trees. The 185 tests are the run's own count: 39 + 127 + 19 on the branch, and 39 + 109 + 19 at the hash, which equals the export commit's claim. The pins match and every re-pin is accountable; no stale blob was found; every effort is supported offline. The four lint refusals are read in `02` § The runs: two are historical by design, and two are genesis-bound and pass at their own commit. Leads: F-02 (the binding's consequence) and F-13 (`run test` stops at the first failing file).

### Q4 Package currency

| Item | Declared / pinned | Resolved here | Latest (read 2026-10-25) | Gap |
| --- | --- | --- | --- | --- |
| `tsx` (dev) | `^4.22.4` (2026-05-31) | 4.23.15 on both trees | 4.23.15 (2026-09-20) | none resolved; the range floor is 112 days behind the latest. No lockfile, so the resolved version is never recorded (F-06) |
| `@aws-sdk/client-bedrock-runtime` | `^3.1073.0` (2026-06-19) | 3.1156.0 on both trees | 3.1156.0 (2026-10-22) | none resolved; the floor 3.1073.0 is four months older than the latest 3.1156.0. It serves only the Mistral Bedrock backup route (F-08) |
| `mistral-common` | `==1.11.7` (2026-07-23) | not installed (`IMPORTED-FROM.md`) | 1.12.0 (2026-09-22) | one minor release; for a seat in no profile |
| `numpy` | `<2.4; python_version < "3.13"` (no bound on 3.13 and later) | not installed | 2.5.4 (2026-10-10) | the bound applies only below 3.13 |
| the seat-efforts snapshot | `refreshed_at` `2026-09-28T05:09:37Z` | -- | -- | **27 days** at 2026-10-25. Offline validation: rc 0, *every effort supported* (8 seats on the branch, 7 at the hash). **A fresh reading needs `OPENROUTER_API_KEY` and was not run.** The Argon entry is younger than the stamp (F-07) |
| the corpus | 4.29.1, generated 2026-09-29 (`7be6721b`) | -- | **CANNOT: no export newer than `7be6721b` is reachable here.** The scaffold checkout on this host is `20c0a77` (2026-08-29), corpus 3.29.1, and lacks the export commit | the maintainer's agent on marvin is the bundles' source |

**The roster against the floor** (`OPENROUTER_SEATS`, `council-invoke.ts:1351` at the hash and `:1362` on the branch; identical in slug, effort and pin on both):

| Seat | Slug | Effort | Provider pin | `adversarial-council.md` | Verdict |
| --- | --- | --- | --- | --- | --- |
| claude | `anthropic/claude-fable-5.1` | `xhigh` | -- | `anthropic/claude-fable-5.1`, `xhigh` (`:77`) | on the floor |
| gpt | `openai/gpt-6-astra` | `max` | `openai`, `allow_fallbacks: false` | `openai/gpt-6-astra`, `max`, OpenAI, no fallbacks (`:78`) | on the floor |
| gemini | `google/gemini-3.8-flash` | `high` | -- | the five-seat roster (`IMPORTED-FROM.md` item 5) | as installed |
| kimi | `moonshotai/kimi-k3` | `max` | four providers, `allow_fallbacks: false` | the roster | as installed |
| muse | `meta/muse-spark-1.3` | `max` | `meta`, `allow_fallbacks: false` | the fifth seat since scaffold#915 | as installed |
| gemini-argon (branch only, `AUDIT_OPENROUTER_SEATS`) | `google/gemini-4-argon` | `high` | `google-vertex/global`, `allow_fallbacks: false` | not a seat: an audit route outside every profile (#638) | outside the floor by design |

### Q5 Efficiency

- **A seat call's cost** (`stage-b/seat-records.md`, ten records):
  - five refutations of 478 to 2,211 s, at $0.81 to $6.34;
  - five probes of 5 to 10 s, at about $0.01 each;
  - **$18.54 over the week's ten calls.**

  | Slice | Call | Tokens in / out | Seconds | USD |
  | --- | --- | --- | ---: | ---: |
  | T9 | gpt-audit | 80,367 / 51,800 | 1,200 | 3.59 |
  | T10 | gemini-argon-audit | 165,358 / 47,632 | 478 | 0.81 |
  | T10 | gpt-audit | 146,966 / 90,082 | 2,211 | 6.34 |
  | T12 | gpt-audit | 221,398 / 52,369 | 2,067 | 2.84 |
  | T14 | gpt-audit | 146,499 / 61,214 | 1,501 | 4.89 |

- **`npm install` per tree:** 1 to 2 s from npm's cache (31 packages); `test` 28 s on each tree.

### Q6 Dead ends

| Candidate | What still imports or names it | Disposition |
| --- | --- | --- |
| `scripts/lib/council-mistral-tokenizer.py`, `council-mistral-counter.mjs`, `council-count-mistral.mjs`, `setup-council-mistral-tokenizer.mjs` | each other only (`count-mistral` → `counter` → `tokenizer`; `setup` → `tokenizer`); otherwise the corpus manifest and `fork-workflow.md`'s enumeration. No Facilitator path | kept because the export carries it (D-WORKFLOW-088) |
| `scripts/lib/council-mistral-requirements.txt` | `IMPORTED-FROM.md` (*not installed*) | kept because the export carries it |
| `@aws-sdk/client-bedrock-runtime` (a dependency in the fork's `package.json`) | `council-invoke.ts:2243`, imported lazily for the Mistral Bedrock backup only (`:108-111`) | a lead for the coordinator: the fork installs it on every `npm install` for a route no profile uses |
| `scripts/forge-write-status.mjs` | the pins, `COUNCIL-BUNDLE.md`, `IMPORTED-FROM.md`; nothing imports it (its pin reason) | kept because the export carries it |
| `scripts/owner-queue-lint.mjs` | `forge-write-status.mjs`, the pins | kept because the export carries it |
| the four `council-stage-*.mjs` CLIs | each other and the staged library; no `run` subcommand | kept because the export carries it |
| `.claude/agents/council-member-deepseek.agent.md`, `-grok.agent.md` (not members) | the pins (*required by the imported pin verifier*, `IMPORTED-FROM.md` item 5); descriptions *Historical ... Inactive ... do not invoke* | kept because the export carries it |
| `.claude/agents/council-member-mistral.agent.md` (not a member) | the pins; *outside every run profile since scaffold#915* | kept because the export carries it |
| `--member grok\|deepseek\|mistral`, `--provider azure\|bedrock\|direct` | accepted by `invoke` (usage `:2877-2885`); no rule names them as usable; Azure and Bedrock are *Mistral-only backups* | a lead for the coordinator (F-09): nothing in code refuses them |

Nothing is removed.

### Q7 Clarity and structure

**The provenance table** is `02` § Provenance (52 rows), with § Reconciliation: every difference accounted for; the 2026-10-04 reason true of its diff; the branch's six reasons true of theirs. **The descriptions against the code:**

| Description | Says | The code | Drift |
| --- | --- | --- | --- |
| `tools/council/run` header (`:2-17`) | loads keys from `~/.config/council/env` (0600); the subcommand list; `test` makes no provider calls | the list matches the `case`; `test` is offline | `COUNCIL_ENV_FILE` is not mentioned; the silent skip is not mentioned (F-10) |
| `tools/council/package.json` `description` | *imported from pfi/pfi-collaboration* | scaffold's export since 2026-09-30 | stale (F-12) |
| `adversarial-council.md` | the Facilitator at `scripts/council-invoke.ts`, OpenRouter route; the floor | matches; the floor holds on both trees | none on the floor; the branch's audit route is described by `IMPORTED-FROM.md`, not by this rule |
| `council-substrate-integrity.md` | rules 4 and 5: run `scripts/lint-council-research-provenance.ts` and `-digests.ts` in a council-research run; HALT on exit 3; the adoption note (`:42-46`): those lints are the source estate's only, check by hand where absent | neither script exists in any commit; the Facilitator also stops on 6, 7 and (branch) 8 | F-05 (the rules read as unconditional; the fallback is only in the preamble), F-15 |
| `instruction-files.md` rows | `council/`: *verified external reviewer invocation and retained receipts*; the integrity rule's glob names `scripts/council-invoke.ts` and `scripts/lib/council-verification.ts` | matches | none |
| `IMPORTED-FROM.md` item 3 | ten literals in the two test files | 7 found, in the routing test and the toolchain test | F-04 |

Each drift is a lead; no rule or index row is edited by the lane.

## Instruction File Recommendations

These are proposals for the coordinator; the lane edits no rule.

1. **`council-substrate-integrity.md`:** put the adoption note's manual fallback beside rules 4 and 5 (or bring the two research lints with the next export), and name the Facilitator's other no-retry stops (6, 7, 8) beside exit 3 (F-05, F-15).
2. **`IMPORTED-FROM.md`, or a register row:** record the local Facilitator fork (#636/#638) as a decision, with its reconciliation condition and the expectation that 1.14.0 runs are linted at their own commit (F-01, F-02).
3. **`engineering-practices.md` § Guards must fail closed:** *capture `rc=$?` on the line after the command, before any substitution.* This is the third instance (friction 2026-10-25 02:59 UTC), meeting the P1 retro's trigger.
4. **The refresh:** a short procedure, or a check, that re-applies the five adaptations and keeps the export's pristine SUMS-verified bytes outside the tree for the next diff (F-14).

## Quality self-check

- **Every count re-derived by a command and kept in `stage-a/` or `stage-b/`:** the 52, the four SUMS counts on both trees, the pins (27/30), the test counts (39/109/19, 39/127/19), the 52 coverage rows (the `awk` count).
- **Three of this slice's readings were wrong at first and are corrected:** the lint/verifier inconsistency (withdrawn; #692 edited at 03:05), F-05's severity and wording (Medium, *after every call*, corrected to Low after reading the rule's adoption note), and a loop's `rc=0` (friction line).
- **Unverifiable here, and stated as such:** the export's bytes for the 9 (F-04's remaining three literals), any newer export (CANNOT), and a fresh seat-efforts reading (it needs the key).
- **No member file changed:** `git log --format=%h 32a34393dd..HEAD -- <the 52>` is empty.
