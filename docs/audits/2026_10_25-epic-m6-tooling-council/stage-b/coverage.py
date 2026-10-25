#!/usr/bin/env python3
"""T45 (#692): the 52 coverage rows for 02, written from the members' own header
lines and stage-b/refs.txt (who names each one at 8ebaf8daad).
    python3 -I coverage.py <worktree>  -> Markdown rows on stdout
"""
import json, sys
from pathlib import Path
W = Path(sys.argv[1])
rows = {r['path']: r for r in json.loads((W / '.qa-scratch/t45/provenance-table.json').read_text())}
RUN = '`tools/council/run`'
STAGED = 'the staged-capture library (`invoke --staged-*`, the `council-stage-*` CLIs)'
C = {
 'council-seat-efforts.json': ('the pinned catalogue snapshot: each seat model\'s accepted efforts, output ceiling and endpoints', 'the effort lint (`run efforts`), the roster, the pins, both test files', 'header, the branch hunk', 'equal at the hash; the branch adds the Argon entry without moving `refreshed_at` (F-07)'),
 'scripts/__tests__/council-invoke-routing.node-test.ts': ('routing and model-identity tests for the Facilitator (mocked provider data only)', f'{RUN} test (under `tsx`)', 'fixture shape, the branch hunks', 'item 3 accounts for its bytes; 109 at the hash, 127 on the branch, both pass'),
 'scripts/__tests__/lint-council-seat-efforts.node-test.ts': ('branch tests for the effort lint\'s output-ceiling classification', f'{RUN} test (plain `node --test`)', 'header, the branch hunk', 'item 2 accounts for its bytes, not item 3 (F-04); 19/19 on both'),
 'scripts/build-council-prompt.ts': ('composes a step prompt from a run manifest', f'{RUN} prompt; the skill\'s pipeline', 'header, pin', 'equal; scaffold\'s pin'),
 'scripts/check-stale-blob-drift.ts': ('refuses a council path that reverted to a superseded blob', f'{RUN} drift; `council-substrate-integrity.md`', 'header, pin, run', 'equal; rc 0 on both trees'),
 'scripts/council-count-mistral.mjs': ('measures a Mistral request locally with the pinned tokenizer; no dispatch', 'nothing at the hash (named by the corpus manifest only)', 'header, references', 'equal; a dead end for a seat in no profile (Q6, kept)'),
 'scripts/council-invoke.ts': ('the Facilitator: one member, one prompt, one output plus its provenance; the seat table `OPENROUTER_SEATS`', f'{RUN} invoke; every council and audit seat call; most members import it', 'header, seats, exit codes, `--member`/`--provider`, the 2026-10-04 and branch hunks', 'accounted for (item 2, re-pin); floor met on both trees; the branch adds the audit seat and exit 8'),
 'scripts/council-run-start.ts': ('anchors a run\'s genesis on the fork\'s repository (`ls-remote` read-back)', f'{RUN} start; the skill\'s pipeline', 'header, the 2026-10-04 hunks', 'accounted for (items 1 and 2, re-pin); the reason holds against its diff'),
 'scripts/council-run-summary.ts': ('writes `run-summary.{json,md}` from a run\'s provenance siblings', f'{RUN} summary', 'header, pin', 'equal; scaffold\'s pin'),
 'scripts/council-stage-attempt.mjs': ('CLI: prepare or capture one durable staged attempt', 'no wrapper route; run with `node` directly', 'header, references', 'equal; unpinned; reached only by hand (Q6 row, kept)'),
 'scripts/council-stage-controller.mjs': ('CLI: create, inspect and run a bounded staged-controller plan', 'no wrapper route; run with `node` directly', 'header', 'equal; unpinned; reached only by hand (Q6, kept)'),
 'scripts/council-stage-readings.mjs': ('CLI: create, accept and reverify bounded initial readings', 'no wrapper route; run with `node` directly', 'header', 'equal; unpinned; reached only by hand (Q6, kept)'),
 'scripts/council-stage-sources.mjs': ('CLI: prepare exact source slices without dispatching', 'no wrapper route; the other stage CLIs import it', 'header', 'equal; unpinned (Q6, kept)'),
 'scripts/council-toolchain.node-test.mjs': ('offline synthetic tests of the whole toolchain (no provider, keyring or forge)', f'{RUN} test (plain `node --test`)', 'fixture keys, the Forge assertions, the branch hunk', 'accounted for (items 1, 2, 3); 39/39 on both'),
 'scripts/forge-write-status.mjs': ('scaffold\'s Forge write check, with placeholder defaults', 'nothing: unimported since the fork\'s run-start (its pin reason)', 'header, pin reason', 'accounted for (item 2, re-pin); a dead end kept because the export carries it (Q6)'),
 'scripts/lib/council-mistral-counter.mjs': ('local Mistral token measurement; never capacity certification', '`council-count-mistral.mjs` only', 'header', 'equal; dead end (Q6, kept)'),
 'scripts/lib/council-mistral-requirements.txt': ('`mistral-common==1.11.7`, `numpy<2.4; python_version < "3.13"`', 'the setup script\'s install; `IMPORTED-FROM.md` says *not installed*', 'whole file, PyPI', 'equal; 1.11.7 against 1.12.0 (Q4); dead end (Q6, kept)'),
 'scripts/lib/council-mistral-tokenizer.py': ('the Mistral tokenizer bridge (Python)', 'the counter and the setup script', 'header', 'equal; dead end (Q6, kept)'),
 'scripts/lib/council-roster.ts': ('read-only projection of the Facilitator\'s recipes: `MEMBER_IDS`, profiles, `assertRunRoster`', 'the lints, the verifiers, run-start, prompt, summary', '`assertRunRoster` (`:292-330`)', 'equal; the contract check that refuses the 09-30 runs on the branch'),
 'scripts/lib/council-run-preflight.ts': ('the lifecycle gate the Facilitator loads lazily for staged attempts', 'the Facilitator', 'header, pin', 'equal; scaffold\'s pin'),
 'scripts/lib/council-staged-attempt-store.mjs': ('binds one staged dispatch and keeps its raw capture', STAGED, 'the branch hunk (+5)', 'equal at the hash; #636 adds `content_filtered_no_retry`'),
 'scripts/lib/council-staged-controller-store.mjs': ('frozen per-plan quotas and a reservation journal', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-controller.ts': ('accounts one frozen plan; admits only verified attempts', STAGED, 'the branch hunk (+1)', 'equal at the hash; #636 adds one line; pinned on the branch'),
 'scripts/lib/council-staged-derived-contract.mjs': ('binds derived packets to one preparation and controller', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-derived-readings.ts': ('reconstructs committed notes and pending rereads', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-derived-runtime.ts': ('recounts derived requests before accounting or dispatch', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-derived-store.mjs': ('publishes immutable derived packages', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-invocation.ts': ('binds one canonical invocation to a preparation and intent', STAGED + '; the Facilitator', 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-note-counter.mjs': ('requires pinned bounds for raw member-note bytes', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-notes.mjs': ('validates notes against frozen original bytes', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-pins.mjs': ('rechecks selected capability files without running them', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-reading-store.mjs': ('one frozen reading policy and raw-note bundles', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-readings.ts': ('accepts initial notes only from verified captures', STAGED, 'the branch hunk (+1)', 'equal at the hash; #636 adds one line; pinned on the branch'),
 'scripts/lib/council-staged-request.ts': ('exact-request assessment for offline source preparation', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-rereads.mjs': ('selects frozen bytes for one reread packet', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-sources.mjs': ('freezes UTF-8 sources into budget-verified slice plans', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-staged-store.mjs': ('persists immutable, scope-bound source preparation', STAGED, 'header', 'equal; unpinned'),
 'scripts/lib/council-verification.ts': ('genesis, ledger, seals and the historical-contract rule (`HISTORICAL_CONTRACTS`, #944)', 'the lints, the verifiers, run-start, prompt; `council-substrate-integrity.md`', '`:333-395`', 'equal; the rule the four lint verdicts are read against'),
 'scripts/lib/verifier-pins.ts': ('the pin verifier\'s library: the pinned set and the re-pin accounting', '`verify-pins`, run-start, the roster, the effort lint', 'header, pin', 'equal; scaffold\'s pin'),
 'scripts/lint-council-run.ts': ('a run directory\'s completeness, per step; historical inventory by discovery', f'{RUN} lint; the council skill', '`:47-66`, `:292-310`, `:400-450`', 'accounted for (item 2, re-pin); the four refusals read in § The runs'),
 'scripts/lint-council-seat-efforts.ts': ('every seat asks an effort its model accepts; `--refresh` needs the key', f'{RUN} efforts; `council-substrate-integrity.md`', 'flags (`:265-266`), refresh (`:279-316`), the branch hunk', 'equal at the hash; the branch folds the audit seats in; rc 0 offline on both'),
 'scripts/owner-queue-lint.mjs': ('scaffold\'s owner-decision-queue lint', '`forge-write-status.mjs` only', 'header, pin', 'equal; a dead end kept because the export carries it (Q6)'),
 'scripts/setup-council-mistral-tokenizer.mjs': ('installs the pinned tokenizer for offline counting', 'nothing (the corpus manifest and `fork-workflow.md` name it)', 'header', 'equal; dead end (Q6, kept)'),
 'scripts/verify-chain.ts': ('verifies a run\'s ledger chain; historical runs by their own contract', f'{RUN} verify-chain', '`:87`, `:161`, `:231`', 'equal; exempts historical runs, as the lint\'s discovery does'),
 'scripts/verify-pins.ts': ('the pin check\'s entry point', f'{RUN} verify-pins; `council-substrate-integrity.md`', 'run', 'equal; rc 0 on both trees'),
 'scripts/verify-seals.ts': ('verifies a run\'s step seals with its HMAC key', f'{RUN} verify-seals', '`:43-49`', 'equal; not run here (it reads a run\'s seal key)'),
 'scripts/write-step-seal.ts': ('seals a completed step', f'{RUN} seal', 'header, pin', 'equal; scaffold\'s pin'),
 'seed/corpus/banner.mjs': ('the single construction of the MANAGED-BY-SCAFFOLD banner', 'the pins only', 'whole file (12 lines)', 'equal; scaffold\'s pin'),
 'seed/corpus/manifest.json': ('the corpus manifest: version 4.29.1, generated 2026-09-29', 'the stage CLIs, the lints, the verifiers', '`corpusVersion`, `generated`, the swept paths', 'accounted for by item 2 (not checkable here); CANNOT against a newer export (Q4)'),
 'tools/council/package.json': ('the fork\'s npm manifest: `tsx ^4.22.4`, `@aws-sdk/client-bedrock-runtime ^3.1073.0`; no lockfile (`.gitignore:67`)', '`npm install --prefix tools/council`', 'whole file, `npm view`', 'unlisted (the fork\'s own); its description names the retired lineage (F-12)'),
 'tools/council/run': ('the fork\'s wrapper: sources the env file at mode 600, execs `tsx scripts/<s>`', 'every council and audit call; the skills and rules', 'whole file (51 lines)', 'unlisted (the fork\'s own); the env guard is one-sided (F-10); `test` stops at the first failing file (F-13)'),
 'verifier-pins.json': ('the pinned set: 27 pins at the hash (19 members, 8 agents), 30 on the branch', '`verify-pins`, the roster, run-start, the effort lint', 'every reason, both trees', 'accounted for; every re-pin\'s reason read against its diff'),
}
assert set(C) == set(rows), sorted(set(rows) ^ set(C))
for p in sorted(rows):
    a, b, c, d = C[p]
    print(f'| `{p}` | {a} | {b} | {c} | {d} |')
