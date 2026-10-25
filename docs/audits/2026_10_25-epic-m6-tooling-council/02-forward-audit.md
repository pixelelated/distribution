# Forward audit — M6.P2 T45, the council toolchain and runner (#692)

**The read:** the 52 members at `8ebaf8daad`. The lane's tree, `reviewed-at` `32a34393dd`, carries `0ceb2994c5` and `033eb7ed23` beyond the hash, and those ten files are tabled as rows of their own. **Depth:** Local, no reviewer seat; the lint and the counts are the check. Every `tools/council/run` call was made keyless (`COUNCIL_ENV_FILE=/nonexistent`); `00` records each one. The figures cite `stage-a/` and `stage-b/`, under this folder.

**Can this be done on the VM? Yes -- on the host.** This is a table of bytes, pins, versions and the toolchain's own tests on two trees. It needs no guest, no device and no provider. The only network was read-only and keyless: `npm view`, PyPI's JSON, and `npm install --prefix tools/council` in the worktree and the clone at the hash.

## Phase 2: #692's checklist at stage B

| # | Criterion (short) | State at stage B | Evidence |
| --- | --- | --- | --- |
| 1 | `00` and `01` to `05` exist | `00` to `04` written; `05` at stage D | this folder |
| 2 | the lint `PASS` (pre-issue before D, resolution at close) | run at stage C | -- |
| 3 | `review-plan.json` local, `reviewers: []`, *the lint and the counts are the check*; no provenance file | written | `second-opinions/review-plan.json`; `ls second-opinions/ \| grep -c provenance` is 0 |
| 4 | the punch-list issue's items at Phase 7 outcomes | stage D onward | -- |
| 5 | `reviewed-at`/`fixed-at`; members differ from the hash on the two commits' ten files | `reviewed-at` `32a34393dd`; `git log --format=%h 8ebaf8daad..32a34393dd -- <the 52>` prints `0ceb2994c5`, `033eb7ed23`; `git diff --stat` reads `10 files changed, 356 insertions(+), 28 deletions(-)` | `00` § Stage A |
| 6 | `01` § Scope | written | `01` |
| 7 | 52 coverage rows | written | § Coverage |
| 8 | § Provenance, § Reconciliation and the branch's delta | written | below |
| 9 | § The runs on both trees, and `lint` over the recorded council runs | written | § The runs |
| 10 | `00` shows keyless runs and no forbidden act | written | `00` |
| 11 | `04` § Q4 currency table | written | `04` |
| 12 | `04` § Q6 dead ends | written | `04` |
| 13 | `04` § Q7 descriptions | written | `04` |
| 14 | `proved:` cells; `question:`; no member changed by the lane | cells below; `git log --format=%h 32a34393dd..HEAD -- <the 52>` empty | § Proofs |
| 15 | the retro | stage G | -- |
| 16 | the five checkers | at hand-back | -- |

## Provenance

One row per member.

- **SUMS:** whether `COUNCIL-BUNDLE.SHA256SUMS` lists the path.
- **Byte-equal at the hash:** `git show 8ebaf8daad:<path> | sha256sum` against the SUMS (`stage-a/provenance-8ebaf8daad.txt`).
- **Pinned at the hash:** an entry in `verifier-pins.json` at `8ebaf8daad`, with its `repinned_at` and the reason's tag (scaffold's own issue, or the fork's decision).
- **IMPORTED-FROM:** the adaptation items of `.claude/skills/council/IMPORTED-FROM.md` (1 the anchor, 2 the wordlist sweep, 3 the fixture literals) that account for the difference.
- **Last fork commit:** the inventory's.
- **Branch:** equal to the hash, or changed by `033eb7ed23`/`0ceb2994c5`, with the branch's pin and SUMS verdict.

| Path | Lines | SUMS | Byte-equal at the hash | Pinned at the hash | IMPORTED-FROM | Last fork commit | Branch |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `council-seat-efforts.json` | 352 | listed | yes | yes, re-pinned 2026-09-28 (scaffold#917) | -- | `5f1b343d25` | changed by 0ceb2994c5 (pin: yes, re-pinned 2026-10-22 (pixelelated#638/#636); SUMS DIFFERS) |
| `scripts/__tests__/council-invoke-routing.node-test.ts` | 1087 | listed | no | no | 2, 3 | `5f1b343d25` | changed by 033eb7ed23, 0ceb2994c5 (pin: no; SUMS DIFFERS) |
| `scripts/__tests__/lint-council-seat-efforts.node-test.ts` | 447 | listed | no | no | 3 | `5f1b343d25` | changed by 0ceb2994c5 (pin: no; SUMS DIFFERS) |
| `scripts/build-council-prompt.ts` | 166 | listed | yes | yes, re-pinned 2026-09-25 (scaffold (no issue named)) | -- | `5f1b343d25` | equal to the hash |
| `scripts/check-stale-blob-drift.ts` | 171 | listed | yes | yes, re-pinned 2026-09-14 (scaffold#524) | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-count-mistral.mjs` | 84 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-invoke.ts` | 3701 | listed | no | yes, re-pinned 2026-10-04 (D-WORKFLOW-144, #409) | 2 | `a9af618398` | changed by 033eb7ed23, 0ceb2994c5 (pin: yes, re-pinned 2026-10-22 (pixelelated#638/#636); SUMS DIFFERS) |
| `scripts/council-run-start.ts` | 290 | listed | no | yes, re-pinned 2026-10-04 (D-WORKFLOW-144, #409) | 1, 2 | `a9af618398` | equal to the hash |
| `scripts/council-run-summary.ts` | 555 | listed | yes | yes, re-pinned 2026-09-29 (scaffold#943) | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-stage-attempt.mjs` | 155 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-stage-controller.mjs` | 208 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-stage-readings.mjs` | 87 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-stage-sources.mjs` | 223 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/council-toolchain.node-test.mjs` | 1450 | listed | no | no | 1, 2 | `5f1b343d25` | changed by 0ceb2994c5 (pin: no; SUMS DIFFERS) |
| `scripts/forge-write-status.mjs` | 268 | listed | no | yes, re-pinned 2026-09-30 (rocknix D-WORKFLOW-088/089) | 2 | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-mistral-counter.mjs` | 288 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-mistral-requirements.txt` | 4 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-mistral-tokenizer.py` | 225 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-roster.ts` | 386 | listed | yes | yes, re-pinned 2026-09-28 (scaffold#917) | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-run-preflight.ts` | 196 | listed | yes | yes, re-pinned 2026-09-28 (scaffold#917) | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-attempt-store.mjs` | 1362 | listed | yes | no | -- | `5f1b343d25` | changed by 033eb7ed23 (pin: yes, re-pinned 2026-10-22 (pixelelated#636); SUMS DIFFERS) |
| `scripts/lib/council-staged-controller-store.mjs` | 1507 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-controller.ts` | 919 | listed | yes | no | -- | `5f1b343d25` | changed by 033eb7ed23 (pin: yes, re-pinned 2026-10-22 (pixelelated#636); SUMS DIFFERS) |
| `scripts/lib/council-staged-derived-contract.mjs` | 894 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-derived-readings.ts` | 402 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-derived-runtime.ts` | 1156 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-derived-store.mjs` | 814 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-invocation.ts` | 688 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-note-counter.mjs` | 300 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-notes.mjs` | 581 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-pins.mjs` | 71 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-reading-store.mjs` | 604 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-readings.ts` | 887 | listed | yes | no | -- | `5f1b343d25` | changed by 033eb7ed23 (pin: yes, re-pinned 2026-10-22 (pixelelated#636); SUMS DIFFERS) |
| `scripts/lib/council-staged-request.ts` | 287 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-rereads.mjs` | 176 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-sources.mjs` | 977 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-staged-store.mjs` | 508 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/council-verification.ts` | 431 | listed | yes | yes, re-pinned 2026-09-29 (scaffold#944) | -- | `5f1b343d25` | equal to the hash |
| `scripts/lib/verifier-pins.ts` | 280 | listed | yes | yes, re-pinned 2026-09-28 (scaffold#915) | -- | `5f1b343d25` | equal to the hash |
| `scripts/lint-council-run.ts` | 483 | listed | no | yes, re-pinned 2026-09-30 (rocknix D-WORKFLOW-088/089) | 2 | `5f1b343d25` | equal to the hash |
| `scripts/lint-council-seat-efforts.ts` | 404 | listed | yes | yes, re-pinned 2026-09-28 (scaffold#917) | -- | `5f1b343d25` | changed by 0ceb2994c5 (pin: yes, re-pinned 2026-10-22 (pixelelated#638/#636); SUMS DIFFERS) |
| `scripts/owner-queue-lint.mjs` | 96 | listed | yes | yes, re-pinned 2026-09-14 (scaffold#524) | -- | `5f1b343d25` | equal to the hash |
| `scripts/setup-council-mistral-tokenizer.mjs` | 97 | listed | yes | no | -- | `5f1b343d25` | equal to the hash |
| `scripts/verify-chain.ts` | 239 | listed | yes | yes, re-pinned 2026-09-29 (scaffold#944) | -- | `5f1b343d25` | equal to the hash |
| `scripts/verify-pins.ts` | 45 | listed | yes | yes, re-pinned 2026-09-14 (scaffold#524) | -- | `5f1b343d25` | equal to the hash |
| `scripts/verify-seals.ts` | 140 | listed | yes | yes, re-pinned 2026-09-29 (scaffold#944) | -- | `5f1b343d25` | equal to the hash |
| `scripts/write-step-seal.ts` | 110 | listed | yes | yes, re-pinned 2026-09-14 (scaffold#524) | -- | `5f1b343d25` | equal to the hash |
| `seed/corpus/banner.mjs` | 12 | listed | yes | yes, re-pinned 2026-09-14 (scaffold#524) | -- | `5f1b343d25` | equal to the hash |
| `seed/corpus/manifest.json` | 807 | listed | no | no | 2 | `5f1b343d25` | equal to the hash |
| `tools/council/package.json` | 8 | unlisted | -- | no | -- | `b3e5c92559` | equal to the hash |
| `tools/council/run` | 51 | unlisted | -- | no | -- | `5f1b343d25` | equal to the hash |
| `verifier-pins.json` | 169 | listed | no | no | 2 (one pin reason); the re-pins | `a9af618398` | changed by 033eb7ed23, 0ceb2994c5 (pin: no; SUMS DIFFERS) |

**The counts:**
- At the hash: 50 listed, **41 byte-equal, 9 differ**, 2 unlisted. On the branch: **36, 14, 2**. Both agree with the coordinator's figures; no delta.
- Pinned members: 19 of the 52 at the hash, 22 on the branch.
  - The other 8 pins of the 27 (30 on the branch) are the eight `.claude/agents/council-member-*.agent.md`, which are not members.
  - Of the 19, 4 carry a fork reason (`council-invoke.ts`, `council-run-start.ts`, `forge-write-status.mjs`, `lint-council-run.ts`) and 15 carry scaffold's own reasons, written before the export. Those 15 are byte-equal to the export.

## Reconciliation

### The nine that differ at the hash

**The export's own bytes are in no commit of this repository.** For each of the 9, every commit holding the path (`git log --all -- <path>`, up to 40) was hashed against the SUMS, and none matched. The adaptations were applied in the same commit that imported the export (`5f1b343d25`). So no diff against the export can be made here, and each file is read as it is, against the adaptation list and the commits after `5f1b343d25`. The marker counts come from `git show 8ebaf8daad:<path>`.

| File | Accounted for by | Marks in the bytes at the hash | Verdict |
| --- | --- | --- | --- |
| `scripts/council-invoke.ts` | item 2 (both `HTTP-Referer` strings, the Azure Foundry default host, comments); the fork's re-pin of 2026-10-04 | 5 sweep phrases, 1 placeholder host, 2 identity URLs | accounted for; pinned with a reason |
| `scripts/council-run-start.ts` | item 1 (the anchor on the fork's repository: `ls-remote` read-back, no Forge helper); item 2; the 2026-10-04 re-pin | 2 `ls-remote`, 3 identity strings | accounted for; pinned with a reason |
| `scripts/forge-write-status.mjs` | item 2 (placeholder defaults); the re-pin of 2026-09-30 (*no longer imported by run-start here*) | 10 placeholder-host lines | accounted for; pinned with a reason |
| `scripts/lint-council-run.ts` | item 2 (*one comment reworded*); the re-pin of 2026-09-30 | 1 sweep phrase | accounted for; pinned with a reason |
| `scripts/council-toolchain.node-test.mjs` | item 1 (the two Forge assertions now assert the fork's remote); item 3 (one fixture key built at run time); item 2 (comments) | 1 `["synthetic", ...].join("-")` key; 2 placeholder hosts | accounted for; not pinned (a test) |
| `scripts/__tests__/council-invoke-routing.node-test.ts` | item 3 (fixture keys built at run time) | 6 `["synthetic", ...].join("-")` keys; 0 sweep phrases | accounted for; not pinned |
| `scripts/__tests__/lint-council-seat-efforts.node-test.ts` | item 2 (the sweep's *one test*: two comment lines) | 2 sweep phrases (`:7-8`); **0** run-time-built keys | accounted for by item 2, **not by item 3** |
| `seed/corpus/manifest.json` | item 2 (*five corpus-manifest paths*) | `estate-*` path names (`:217-249`); the original names are unrecoverable here | accounted for by the list; not checkable without the export's bytes; not pinned |
| `verifier-pins.json` | item 2 (*one pin reason*) and every fork re-pin since (2026-09-30, #372 on 2026-10-02, 2026-10-04) | cannot pin itself | accounted for |

**Every one of the 9 is accounted for by a re-pin reason or an `IMPORTED-FROM.md` entry. No difference was found that neither records.** One attribution drifts (F-04):

- `IMPORTED-FROM.md` item 3 says *"Ten fixture key literals in the two test files are built at run time (`join`)"*.
- The brief places them in *"the two `__tests__/` files"*.
- The bytes show 7 run-time-built keys, by the `["synthetic", ...].join` pattern: 6 in `__tests__/council-invoke-routing.node-test.ts` and 1 in `scripts/council-toolchain.node-test.mjs`. The `__tests__/lint-council-seat-efforts.node-test.ts` file has none; its difference is item 2's.
- Whether three more literals are built another way cannot be settled without the export's bytes.

**The 2026-10-04 re-pin judged against its diff** (`a9af618398`, reason *"D-WORKFLOW-144, #409: update only the project organization URLs/remote scope to pixelelated"*). The diff on the two pinned scripts changes exactly these:

- the two `HTTP-Referer` URLs in `council-invoke.ts` (`rasteratops` to `pixelelated`);
- the remote-scope regex in `council-run-start.ts`;
- its `[FAIL remote_scope]` message;
- one comment (`rasteratops (D-WORKFLOW-088)` to `pixelelated (D-WORKFLOW-144)`).

**The reason is true in substance.** Every hunk is the organization name in a URL, the regex that scopes the remote, or the text beside it. The comment's decision citation moved from 088 to 144, which the reason does not mention. That's a nit, not a finding.

### The branch's delta

| Row | At the hash | On the branch | Judged |
| --- | --- | --- | --- |
| members changed | -- | 10 files, +356/-28 (`git diff --stat 8ebaf8daad 32a34393dd -- <the 52>`) | exactly the two commits' files |
| SUMS counts | 41 / 9 / 2 | **36 / 14 / 2** | the 5 newly differing: `council-seat-efforts.json`, `lint-council-seat-efforts.ts`, `council-staged-{attempt-store.mjs,controller.ts,readings.ts}`. The SUMS file is unchanged (`git diff --quiet`) |
| pins | 27 | 30 | 3 added, 3 changed, 0 removed (`stage-a/pins-delta.out`) |
| `FACILITATOR_VERSION` | `council-facilitator@1.14.0` (`:844`) | `council-facilitator@1.14.1-pixelelated.2` (`:855`) | `033eb7ed23` set `.1`; `0ceb2994c5` set `.2` |
| the three added pins (`council-staged-*`), `2026-10-22T04:50:02` | absent | reason *"pixelelated#636: local Facilitator 1.14.1-pixelelated.1 stops explicit content_filter ... Models, efforts and routes unchanged"* | **true of its commit.** `033eb7ed23` sets `.1`, adds 1, 1 and 5 lines to the staged readers (`content_filtered_no_retry`, `finish_reason === "content_filter"`), and touches no seat |
| the three re-pins (`council-invoke.ts`, `council-seat-efforts.json`, `lint-council-seat-efforts.ts`), `2026-10-22T05:13:36` | 10-04 / 09-28 / 09-28 | reason *"pixelelated#638/#636: owner-selected separate Argon/high audit route, catalog-bound Google provider and synchronous output allowance ... Council profiles and current Gemini seat unchanged"* | **true of the diff.** `AUDIT_OPENROUTER_SEATS["gemini-argon"]` is added (`google/gemini-4-argon`, `high`, 65536 tokens, `google-vertex/global`, no fallbacks). The seat-efforts snapshot gains that model's entry, and the effort lint folds the audit seats in. `OPENROUTER_SEATS` is identical on both trees (`stage-a/roster-*.txt`) |
| the version sequence | -- | `.1` in #636's pins at 04:50, `.2` in the code after #638's at 05:13 | **a sequence, not a mismatch.** Each reason names the version its own commit set; `033eb7ed23` was committed at 04:59 and `0ceb2994c5` at 05:18 |
| `IMPORTED-FROM.md` (not a member) | 2 sections fewer | *Local retry correction -- October22 (#636)* (+11) and *Local audit route -- October22 (#638)* (+14) | they record the two versions and the evidence, and ask to *reconcile these scoped changes with a newer source-estate export* |
| the evidence folders (not members) | absent | `docs/qa-logs/2026-10-22-review-filter-636/` (13 files) and `docs/qa-logs/2026-10-22-argon-audit-route-638/` (14 files) | `sha256sum -c SHA256SUMS`: **12 of 12 and 13 of 13 OK**, and only `SHA256SUMS` itself is unlisted. The brief's *"30 files"* for the #636 folder is a delta: the two folders hold 27 between them |
| the commits' test claims | 39 / 109 / 19 by the run | 39 / 127 / 19 by the run | #636's message claims routing 119/119 and its `routing-final.log.gz` reads `tests 119 pass 119`. #638 added 81 routing lines, and its `routing-final.log.gz` reads `tests 127 pass 127`. **127 is #636's 119 plus #638's eight**, so the message was true of its own commit. #638's `tests-final03.log.gz` shows the effort suite at 18/19 (case `(h)`). Its README discloses that failure and records `effort-tests-final.log.gz` at 19/19, which this slice's run repeats on the branch |
| the seat-efforts `refreshed_at` | `2026-09-28T05:09:37Z` | the same | `0ceb2994c5` added the `google/gemini-4-argon` entry from a catalogue read on 2026-10-22 (its README) and left the snapshot's one timestamp unchanged, so that one entry is younger than the file says (F-07) |
| the register | -- | `grep -c -E '#636\|#638\|1\.14\.1-pixelelated' docs/decision-register.md` prints 0 | **the missing row is a lead for the coordinator** (F-01). The lane writes none |

## Coverage

One row per member: what it is, who reaches it at the hash, what was read, and the verdict. *Reached by* comes from `stage-b/refs.txt`, a `grep` of each stem over `scripts/`, `seed/`, `tools/council/`, `.claude/rules/` and `.claude/skills/` at the hash. It does not list the pins, the corpus manifest or the push guard's enumeration, which name every member.

| Path | What it is | Reached by | Read | Verdict |
| --- | --- | --- | --- | --- |
| `council-seat-efforts.json` | the pinned catalogue snapshot: each seat model's accepted efforts, output ceiling and endpoints | the effort lint (`run efforts`), the roster, the pins, both test files | header, the branch hunk | equal at the hash; the branch adds the Argon entry without moving `refreshed_at` (F-07) |
| `scripts/__tests__/council-invoke-routing.node-test.ts` | routing and model-identity tests for the Facilitator (mocked provider data only) | `tools/council/run` test (under `tsx`) | fixture shape, the branch hunks | item 3 accounts for its bytes; 109 at the hash, 127 on the branch, both pass |
| `scripts/__tests__/lint-council-seat-efforts.node-test.ts` | branch tests for the effort lint's output-ceiling classification | `tools/council/run` test (plain `node --test`) | header, the branch hunk | item 2 accounts for its bytes, not item 3 (F-04); 19/19 on both |
| `scripts/build-council-prompt.ts` | composes a step prompt from a run manifest | `tools/council/run` prompt; the skill's pipeline | header, pin | equal; scaffold's pin |
| `scripts/check-stale-blob-drift.ts` | refuses a council path that reverted to a superseded blob | `tools/council/run` drift; `council-substrate-integrity.md` | header, pin, run | equal; rc 0 on both trees |
| `scripts/council-count-mistral.mjs` | measures a Mistral request locally with the pinned tokenizer; no dispatch | nothing at the hash (named by the corpus manifest only) | header, references | equal; a dead end for a seat in no profile (Q6, kept) |
| `scripts/council-invoke.ts` | the Facilitator: one member, one prompt, one output plus its provenance; the seat table `OPENROUTER_SEATS` | `tools/council/run` invoke; every council and audit seat call; most members import it | header, seats, exit codes, `--member`/`--provider`, the 2026-10-04 and branch hunks | accounted for (item 2, re-pin); floor met on both trees; the branch adds the audit seat and exit 8 |
| `scripts/council-run-start.ts` | anchors a run's genesis on the fork's repository (`ls-remote` read-back) | `tools/council/run` start; the skill's pipeline | header, the 2026-10-04 hunks | accounted for (items 1 and 2, re-pin); the reason holds against its diff |
| `scripts/council-run-summary.ts` | writes `run-summary.{json,md}` from a run's provenance siblings | `tools/council/run` summary | header, pin | equal; scaffold's pin |
| `scripts/council-stage-attempt.mjs` | CLI: prepare or capture one durable staged attempt | no wrapper route; run with `node` directly | header, references | equal; unpinned; reached only by hand (Q6 row, kept) |
| `scripts/council-stage-controller.mjs` | CLI: create, inspect and run a bounded staged-controller plan | no wrapper route; run with `node` directly | header | equal; unpinned; reached only by hand (Q6, kept) |
| `scripts/council-stage-readings.mjs` | CLI: create, accept and reverify bounded initial readings | no wrapper route; run with `node` directly | header | equal; unpinned; reached only by hand (Q6, kept) |
| `scripts/council-stage-sources.mjs` | CLI: prepare exact source slices without dispatching | no wrapper route; the other stage CLIs import it | header | equal; unpinned (Q6, kept) |
| `scripts/council-toolchain.node-test.mjs` | offline synthetic tests of the whole toolchain (no provider, keyring or forge) | `tools/council/run` test (plain `node --test`) | fixture keys, the Forge assertions, the branch hunk | accounted for (items 1, 2, 3); 39/39 on both |
| `scripts/forge-write-status.mjs` | scaffold's Forge write check, with placeholder defaults | nothing: unimported since the fork's run-start (its pin reason) | header, pin reason | accounted for (item 2, re-pin); a dead end kept because the export carries it (Q6) |
| `scripts/lib/council-mistral-counter.mjs` | local Mistral token measurement; never capacity certification | `council-count-mistral.mjs` only | header | equal; dead end (Q6, kept) |
| `scripts/lib/council-mistral-requirements.txt` | `mistral-common==1.11.7`, `numpy<2.4; python_version < "3.13"` | the setup script's install; `IMPORTED-FROM.md` says *not installed* | whole file, PyPI | equal; 1.11.7 against 1.12.0 (Q4); dead end (Q6, kept) |
| `scripts/lib/council-mistral-tokenizer.py` | the Mistral tokenizer bridge (Python) | the counter and the setup script | header | equal; dead end (Q6, kept) |
| `scripts/lib/council-roster.ts` | read-only projection of the Facilitator's recipes: `MEMBER_IDS`, profiles, `assertRunRoster` | the lints, the verifiers, run-start, prompt, summary | `assertRunRoster` (`:292-330`) | equal; the contract check that refuses the 09-30 runs on the branch |
| `scripts/lib/council-run-preflight.ts` | the lifecycle gate the Facilitator loads lazily for staged attempts | the Facilitator | header, pin | equal; scaffold's pin |
| `scripts/lib/council-staged-attempt-store.mjs` | binds one staged dispatch and keeps its raw capture | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | the branch hunk (+5) | equal at the hash; #636 adds `content_filtered_no_retry` |
| `scripts/lib/council-staged-controller-store.mjs` | frozen per-plan quotas and a reservation journal | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-controller.ts` | accounts one frozen plan; admits only verified attempts | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | the branch hunk (+1) | equal at the hash; #636 adds one line; pinned on the branch |
| `scripts/lib/council-staged-derived-contract.mjs` | binds derived packets to one preparation and controller | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-derived-readings.ts` | reconstructs committed notes and pending rereads | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-derived-runtime.ts` | recounts derived requests before accounting or dispatch | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-derived-store.mjs` | publishes immutable derived packages | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-invocation.ts` | binds one canonical invocation to a preparation and intent | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs); the Facilitator | header | equal; unpinned |
| `scripts/lib/council-staged-note-counter.mjs` | requires pinned bounds for raw member-note bytes | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-notes.mjs` | validates notes against frozen original bytes | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-pins.mjs` | rechecks selected capability files without running them | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-reading-store.mjs` | one frozen reading policy and raw-note bundles | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-readings.ts` | accepts initial notes only from verified captures | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | the branch hunk (+1) | equal at the hash; #636 adds one line; pinned on the branch |
| `scripts/lib/council-staged-request.ts` | exact-request assessment for offline source preparation | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-rereads.mjs` | selects frozen bytes for one reread packet | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-sources.mjs` | freezes UTF-8 sources into budget-verified slice plans | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-staged-store.mjs` | persists immutable, scope-bound source preparation | the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs) | header | equal; unpinned |
| `scripts/lib/council-verification.ts` | genesis, ledger, seals and the historical-contract rule (`HISTORICAL_CONTRACTS`, #944) | the lints, the verifiers, run-start, prompt; `council-substrate-integrity.md` | `:333-395` | equal; the rule the four lint verdicts are read against |
| `scripts/lib/verifier-pins.ts` | the pin verifier's library: the pinned set and the re-pin accounting | `verify-pins`, run-start, the roster, the effort lint | header, pin | equal; scaffold's pin |
| `scripts/lint-council-run.ts` | a run directory's completeness, per step; historical inventory by discovery | `tools/council/run` lint; the council skill | `:47-66`, `:292-310`, `:400-450` | accounted for (item 2, re-pin); the four refusals read in § The runs |
| `scripts/lint-council-seat-efforts.ts` | every seat asks an effort its model accepts; `--refresh` needs the key | `tools/council/run` efforts; `council-substrate-integrity.md` | flags (`:265-266`), refresh (`:279-316`), the branch hunk | equal at the hash; the branch folds the audit seats in; rc 0 offline on both |
| `scripts/owner-queue-lint.mjs` | scaffold's owner-decision-queue lint | `forge-write-status.mjs` only | header, pin | equal; a dead end kept because the export carries it (Q6) |
| `scripts/setup-council-mistral-tokenizer.mjs` | installs the pinned tokenizer for offline counting | nothing (the corpus manifest and `fork-workflow.md` name it) | header | equal; dead end (Q6, kept) |
| `scripts/verify-chain.ts` | verifies a run's ledger chain; historical runs by their own contract | `tools/council/run` verify-chain | `:87`, `:161`, `:231` | equal; exempts historical runs, as the lint's discovery does |
| `scripts/verify-pins.ts` | the pin check's entry point | `tools/council/run` verify-pins; `council-substrate-integrity.md` | run | equal; rc 0 on both trees |
| `scripts/verify-seals.ts` | verifies a run's step seals with its HMAC key | `tools/council/run` verify-seals | `:43-49` | equal; not run here (it reads a run's seal key) |
| `scripts/write-step-seal.ts` | seals a completed step | `tools/council/run` seal | header, pin | equal; scaffold's pin |
| `seed/corpus/banner.mjs` | the single construction of the MANAGED-BY-SCAFFOLD banner | the pins only | whole file (12 lines) | equal; scaffold's pin |
| `seed/corpus/manifest.json` | the corpus manifest: version 4.29.1, generated 2026-09-29 | the stage CLIs, the lints, the verifiers | `corpusVersion`, `generated`, the swept paths | accounted for by item 2 (not checkable here); CANNOT against a newer export (Q4) |
| `tools/council/package.json` | the fork's npm manifest: `tsx ^4.22.4`, `@aws-sdk/client-bedrock-runtime ^3.1073.0`; no lockfile (`.gitignore:67`) | `npm install --prefix tools/council` | whole file, `npm view` | unlisted (the fork's own); its description names the retired lineage (F-12) |
| `tools/council/run` | the fork's wrapper: sources the env file at mode 600, execs `tsx scripts/<s>` | every council and audit call; the skills and rules | whole file (51 lines) | unlisted (the fork's own); the env guard is one-sided (F-10); `test` stops at the first failing file (F-13) |
| `verifier-pins.json` | the pinned set: 27 pins at the hash (19 members, 8 agents), 30 on the branch | `verify-pins`, the roster, run-start, the effort lint | every reason, both trees | accounted for; every re-pin's reason read against its diff |

## The runs

On each tree. The branch is `32a34393dd`, `node` v24.21.0 and npm 11.19.0. The clone is `/workspace/tmp/m6-t45/at-hash`, with `git rev-parse HEAD` giving `8ebaf8daad8eaac6331dff6fc048fb4411d7decb`. Every call went through `env -u FIREFLIES_API_KEY COUNCIL_ENV_FILE=/nonexistent` (`stage-a/runs.sh`).

| Run | Branch | At the hash | A FAIL would mean |
| --- | --- | --- | --- |
| `npm install --prefix tools/council` | rc 0, 1 s; 31 packages added from the cache | rc 0, 1 s | the toolchain could not be installed from its declared ranges, or the registry refused them |
| resolved (`npm ls --depth=0`) | `tsx@4.23.15`, `@aws-sdk/client-bedrock-runtime@3.1156.0` | the same | -- (a fact: both ranges resolve to the latest on 2026-10-25) |
| `verify-pins` | rc 0: *verifier pins match current files and every re-pin is accountable* | rc 0, the same | a pinned file's bytes differ from its pin, or a re-pin carries no reason |
| `drift` | rc 0: *no stale-blob regression detected* | rc 0, the same | a council path reverted to a superseded blob |
| `efforts` (offline; `--refresh` never passed) | rc 0: 8 seats, 6 provider-pinned, *every effort supported* | rc 0: 7 seats, 5 provider-pinned | a seat asks an effort its model does not advertise, a pin admits no catalogue endpoint, or a seat's model is missing from the snapshot. **A fresh reading needs `OPENROUTER_API_KEY` and was not run** |
| `test` | rc 0 in 28 s: toolchain 39/39, routing 127/127, efforts 19/19; 0 `✖` | rc 0 in 28 s: 39/39, 109/109, 19/19 | a toolchain behaviour the tests pin has regressed. Under `set -e` the first failing file also stops the later ones (F-13) |
| `lint`, the brief's original call (`docs/audits/2026_09_13-.../second-opinions`) | rc 1, `run_invalid` | -- | -- (a recorded refusal: not a run directory, no `council-run-manifest.json`; the brief was corrected at `2672582a01`) |
| `lint <run>`, each of the four `research/council-runs/` runs, named explicitly | **rc 1 on all four**: `council_roster_invalid` | **rc 1 on all four**: the 09-05/11 runs `council_roster_invalid`, the 09-30 runs `genesis_binding_mismatch` | read below. An explicitly named run is held to current admission |
| `lint` with no argument (default discovery) | rc 1: the two 09-30 runs `council_roster_invalid`; the 09-05/11 runs *historical inventory only (not current admission)* | rc 1: the two 09-30 runs `genesis_binding_mismatch`; the 09-05/11 runs historical inventory | a run under a current contract that no longer matches the installed configuration |
| `lint <r2>` at its own close-out commit `4fa6e04948` (in the clone, checked out and returned) | -- | rc 0: *OK - 1 run(s): declared artifacts checked* | the r2 run's own record would be broken on the tree that sealed it |
| `lint --at-step step1 <r1>` at `4fa6e04948` | -- | rc 0, OK | r1's one sealed step would be broken. r1 halted after Step 1 by its own setup probe (its README), so a full lint of it fails `output_missing`/`seal_missing` by design |

**The four rc 1 verdicts, read against the historical-contract rule** (`lint-council-run.ts:47-66`, `council-verification.ts:340-356`):

- **2026-09-05 and 2026-09-11** carry `provenance_contract` `council-facilitator@1.2.0`, which is in `HISTORICAL_CONTRACTS`, and none of the newer keys. Default discovery reports them as *historical inventory only*. Naming them explicitly applies current admission (`lintRun` → `assertRunRoster`), whose contract check cannot hold for `1.2.0`. **A recorded refusal by design, on both trees; not a finding.** This corrects a reading posted on #692 at 03:03 UTC, edited there at 03:05: the lint is not inconsistent with `verify-chain`/`verify-seals`, because it keeps its historical path for discovery, as the comment at `:47-49` says.
- **2026-09-30 r1 and r2** carry `council-facilitator@1.14.0`, the contract installed at the hash and not historical.
  - Their `verification/genesis.json` binds `verifier_pins_hash` `4088e315…`, the pins as of `5f1b343d25`.
  - At the hash, `verifier-pins.json` hashes `4818febe…`, after the fork's re-pins on 2026-10-02 (#372, `4bf31083c7`) and 2026-10-04 (`a9af618398`). So `assertGenesis` refuses: *run identity, coordinator, or verifier pins changed*.
  - At their own commit both runs hold: r2 in full, r1 at its one sealed step.
  - **The binding is by design** (a genesis anchors the reviewed configuration). **Its consequence is a lead (F-02):** any later re-pin leaves every completed current-contract run unlintable on the current tree, and nothing records that this is expected. On the branch the same two runs fail one check earlier, `council_roster_invalid`, because `1.14.0` is neither the installed `1.14.1-pixelelated.2` nor in `HISTORICAL_CONTRACTS`. The local Facilitator bump left `1.14.0` runs belonging to neither class.

## Leads recorded here, not fixed

- **F-03, the two committed seal keys:** `research/council-runs/2026-09-0{5,11}-*/verification/seal-key.local`, on `next` in a public repository, outside the 52. **Deferred to #1043** (the coordinator's, filed 03:06 UTC; the files removed on the coordinator's branch at `0fa5a20c5f`; the history question put to the maintainer). No bug is filed here. The guard gap is #1043's too: the push guard's credential patterns did not catch a bare-hex key file.

## Proofs

| Claim | Evidence | proved: |
| --- | --- | --- |
| The 52 and their counts (52 paths, 25,848 lines, 52 fork-own, 23/22/4/1/1/1 by language, 30 in other areas) | `stage-a/scope.out`, § 2's block at `2174265e9c` | proved: tree |
| 5 fork commits at the hash; the branch adds exactly `0ceb2994c5` and `033eb7ed23`; none since the dispatch tip | `git log` lines in `00` § Stage A | proved: history |
| SUMS 41/9/2 at the hash and 36/14/2 on the branch | `stage-a/provenance-8ebaf8daad.txt`, `stage-a/provenance-HEAD.txt` | proved: tree |
| The export's bytes for the 9 are in no commit here | the all-history hash search in § Reconciliation | proved: history |
| Each of the 9 is accounted for by an item or a re-pin; item 3's attribution drifts (7 run-time keys found, in the routing test and the toolchain test) | the marker counts above | proved: tree |
| The 2026-10-04 re-pin's reason is true of its diff | `git show a9af618398 -- scripts/council-invoke.ts scripts/council-run-start.ts` | proved: history |
| The branch's six pin reasons are true of their diffs; `.1`/`.2` is a sequence | `git show 033eb7ed23`, `git show 0ceb2994c5`, the reasons in `stage-a/pins.out` | proved: history |
| Both evidence folders' `SHA256SUMS` hold (12/12, 13/13) | `sha256sum -c` in each folder (`stage-b/evidence-sums.txt`) | proved: tool-run |
| 127 routing tests = #636's 119 + #638's 8; #638's effort 18/19 disclosed and superseded by 19/19 | the two folders' logs (`stage-b/evidence-sums.txt`) | proved: history |
| `verify-pins`, `drift`, offline `efforts` and `test` pass on both trees | `stage-a/runs-branch.txt`, `stage-a/runs-at-hash.txt` | proved: tool-run |
| The four lint refusals: two historical by design, two genesis-bound to `5f1b343d25`'s pins and holding at their own commit | `stage-a/lint-*.out`, `stage-b/lint-default-*.out`, `stage-b/lint-at-4fa6e04948-*.out` | proved: tool-run |
| The roster meets the floor on both trees; the branch adds one audit seat outside the five | `stage-a/roster-*.txt`; `adversarial-council.md:77-78` | proved: tree |
| The two seal keys are committed and on `next` | `git ls-files`, `git ls-tree -r next` (the files unread) | proved: history |
| No member file was changed by the lane | `git log --format=%h 32a34393dd..HEAD -- <the 52>` is empty | proved: history |
| The runs' keyless condition | the wrapper's `run:21-28` read; every call through `COUNCIL_ENV_FILE=/nonexistent` | proved: design |
