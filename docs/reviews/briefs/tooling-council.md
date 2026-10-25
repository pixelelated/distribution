---
slice: T45
id: tooling-council
issue: "#692"
epic: "#903"
area: tooling-and-guards
kind: table
lens: package currency
depth: Local
version: 2
written: 2026-10-25
lane_tree_beyond_hash: "0ceb2994c5 033eb7ed23 (ten members, 2026-10-22, #636/#638)"
author: the M6 coordinator (Fable 5.1, D-WORKFLOW-189)
read_refs:
  distribution: 8ebaf8daad
  p1: 2174265e9c
---

# T45: the council toolchain and runner (a provenance and currency table)

**Version 2, 2026-10-25, by the coordinator**, after the stranger's proof of version 1 (a read-only reader with no context, 48 rows: 35 verified, 4 wrong, 6 partial, 1 uncheckable; the corrections are marked **(v2)** where they land and listed in the area futro's errata). The largest: the lane's tree carries two council commits that `next` does not (§ 1), so the read stays at the hash and the branch's delta becomes the table's own rows. Version 1 was written 2026-10-25 by the coordinator. A brief for a lane that has never seen this project, in the shape of T15's
(`docs/reviews/briefs/tooling-last-good-test.md`) cut to a **table slice at
Local depth**: no reviewer seat, no fix streams unless the table finds a
defect; the output is two tables and their reconciliation. The order's
§ T45 (`docs/reviews/order.md`, P1's `2174265e9c`) is the slice's
definition; this brief is the work. Every figure here was produced by a
command run at the hash named beside it; a stranger's proof precedes
dispatch, and version 2 records what it found.

## 1. Identity

- **Issue:** #692 `M6.P2 E903/T45: tooling-and-guards: the council toolchain
  and runner`, slice `tooling-council` (`k: 45`) in `docs/reviews/slices.json`,
  forty-fifth in `docs/reviews/order.md` (its row: *52 | 25,848 | -- | 0 |
  Local*; its `why`: *scaffold's export, committed byte for byte
  (D-WORKFLOW-088): by provenance and version only, refreshed by copying the
  next export (plan § 2)*; its `depth_reason`: *a provenance table*).
  **Epic:** #903 (the tooling and guards: T9, T10, T12 and T14 accepted; T15
  running in the T3 session; this slice is the area's last). **Milestone:**
  M6; its body holds the live order; read it first. **Predecessors that
  bear on these files:** every Independent slice this week ran this
  toolchain's `invoke` for its seat (T9 #656, T10 #657, T12 #659, T14 #661:
  their `second-opinions/*.provenance.json` are the runner's recent record);
  **#372** (the instructions kept on the five installed seats); **#409 / D-WORKFLOW-144** (the identity re-pin of 2026-10-04, the last fork commit on these paths at `8ebaf8daad` and on `next`; the lane's tree carries two later ones, the next bullet but one -- v2); **D-WORKFLOW-088, 089, 090, 135** (the export, its
  re-pin rule, the wordlist sweep); `adversarial-council.md` (the model
  floor: Fable 5.1 at `xhigh`, GPT-6 Astra at `max`, Muse Spark 1.3 the
  fifth seat; Opus 4.8 and GPT-5.5 deprecated) and
  `council-substrate-integrity.md` (every member call through the
  Facilitator). **Beside it:** T15, in the T3 session, on a different file
  set (D-WORKFLOW-190).
- **The division of labour (D-WORKFLOW-189).** This lane executes. It does
  not re-cut the slice, change a criterion, write a brief, move the M6 body,
  edit `slices.json`, `areas.json`, `order.md` or the plan, file a Backlog
  issue, edit a rule or a decided register row, or decide a question of
  scope: those are the coordinator's, reached through #692, one question at
  a time. What it does file: its own audit punch-list issue (stage D) and a
  `bug` issue for a defect it proves (D-WORKFLOW-187). **It never refreshes
  the export, re-pins a file or edits a council script**: D-WORKFLOW-088
  makes the toolchain scaffold's, refreshed by copying the next export over;
  a drift this table finds is a lead for the coordinator and the
  maintainer's agent that delivers the bundles.
- **One worktree, one session.** Branch `feature/m6-tooling-council-692` at
  `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-council-692`,
  created by the coordinator, **stacked on `feature/m6-p1-survey-641` at
  `2174265e9c`** with the coordinator's tip merged in and the lane's pointer
  seeded (the hashes are in the dispatch comment on #692). **Before that
  comment exists nothing runs in it.** The session is the T5 lane's
  (`m6-t5-build-engine`), which ran T5, T6, T7, T8, T9 and T12; those
  worktrees stay beside this one, idle, until their merges, and nothing is
  written there. The primary checkout stays on `next` (D-INFRA-025); the
  legacy checkout and `rocknix.worktrees/*` are the M7 lane's, read only.
  **The rules in this worktree are `next`'s except the paths the dispatch comment lists.**
- **What the lane's tree carries beyond the hash (v2).** The coordinator's tip,
  merged into the lane's worktree, holds **two council commits that `next`
  does not**: `0ceb2994c5` and `033eb7ed23` (2026-10-22, blitterbot; *council:
  add explicit Argon audit route and refusal diagnostics* for #638, *council:
  stop retrying explicitly filtered responses* for #636), which reached the
  coordinator's branch through the merge `18747fbc52` of 2026-10-24 and sit on
  every M6 lane branch; `git merge-base --is-ancestor 0ceb2994c5 next` fails.
  They change **ten members** (+356/-28): `scripts/council-invoke.ts`
  (`FACILITATOR_VERSION` is `council-facilitator@1.14.0` at the hash,
  `council-facilitator@1.14.1-pixelelated.2` on the branch, `:855`),
  `verifier-pins.json` (**27 pins at the hash, 30 on the branch**: three added
  for `scripts/lib/council-staged-{attempt-store.mjs,controller.ts,readings.ts}`
  and three re-pinned -- `council-invoke.ts`, `council-seat-efforts.json`,
  `lint-council-seat-efforts.ts` -- at `2026-10-22T05:13:36` with reasons
  citing `pixelelated#638/#636`; the three added pins' reasons name *local
  Facilitator 1.14.1-pixelelated.1* where the code says `.2`),
  `council-seat-efforts.json`, `scripts/lint-council-seat-efforts.ts`, the
  three tests (`council-toolchain.node-test.mjs` and the two under
  `__tests__/`) and the three `council-staged-*` files. So the SUMS comparison
  on the lane's tree reads **36 equal, 14 differ, 2 unlisted** against the
  hash's 41/9/2 -- the five newly differing are `council-seat-efforts.json`,
  `lint-council-seat-efforts.ts` and the three `council-staged-*` files; the
  SUMS file itself is unchanged. **The slice reads the 52 at `8ebaf8daad`**
  (the read ref: what `next` carries and what the renovation integrates
  against) **and tables this delta as rows of its own § Provenance**: a local
  Facilitator fork that D-WORKFLOW-088 (*the toolchain is scaffold's, refreshed
  by copying the next export over*) does not describe and that **no register
  row records** (`grep -c -E '#636|#638|1\.14\.1-pixelelated'
  docs/decision-register.md` printed 0 on 2026-10-25). The pins were re-pinned
  with reasons, as D-WORKFLOW-089 asks; the decision to fork locally was not
  written down. That is a lead for the coordinator, who carries the
  D-WORKFLOW-088 question -- does the local fork stand until scaffold's next
  export carries #636/#638, and under which row -- to the maintainer on #346;
  **the lane changes none of it.** The four Independent slices' provenance
  records this week were written by that branch's Facilitator (T9's
  `second-opinions/gpt-probe.md.provenance.json` at `995e7f869f` reads
  `facilitator_version` `council-facilitator@1.14.1-pixelelated.2`), not by
  the hash's bytes: the record the table cites is the fork's, and the table
  says so.
- **Model and effort:** Opus 5.5 (the maintainer, 2026-10-22: *"the work
  will be Opus 5.5"*) at high effort. Record what ran in `00-running-log.md`'s
  header.
- **Review depth: Local** (plan § 6c; `slices.json` k 45: *a provenance
  table*): **no reviewer seat**. `second-opinions/review-plan.json` records
  depth `local`, scope `epic`, primary `anthropic/claude-opus-5-5` / lab
  `anthropic`, reviewers `[]`, and the sentence *the lint and the counts are
  the check*; **`tools/council/run invoke` is never run in this slice** --
  the toolchain is the subject, not the instrument, and a provider call
  would spend the maintainer's key on a table.
- **The host, read on 2026-10-25 by the coordinator:** M6's; census qemu 0
  (the M7 lane holds a granted single-guest window of 00:09 that this slice
  does not touch: nothing here needs a guest). **A scaffold checkout exists
  on this host at `/home/max/Development/scaffold`, read only, and it is
  older than the export:** its HEAD `20c0a77` (2026-08-29) does not hold the export's commit `7be6721be24458910e75ca639f318d25ffe7e8d5` (2026-09-30) at all (`git cat-file -e` fails on the object, so the checkout cannot even name it -- v2), and its `seed/corpus/manifest.json` reads `corpusVersion`
  **3.29.1** against our **4.29.1** -- so *is there a newer export than ours*
  cannot be answered from this host; it is a line the table carries as
  `CANNOT: no export newer than 7be6721b is reachable here` with the
  maintainer's agent on marvin named as the source of bundles
  (`IMPORTED-FROM.md`).

First commands:

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-council-692
cd "$D"
git fetch origin && git fetch upstream --no-tags
git branch --show-current                                            # feature/m6-tooling-council-692
git merge-base --is-ancestor 2174265e9c HEAD || echo "not stacked on the P1 tip: stop"
test -f docs/reviews/inventory.json || echo "no inventory.json: stop"
git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts   # exactly the paths the dispatch comment lists
cat .github/sessions/saved-session-state-feature-m6-tooling-council-692.md      # seeded by the dispatch
tail -3 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
df -i /tmp | tail -1                                                 # never export a tree under /tmp
git show 8ebaf8daad:.claude/skills/council/COUNCIL-BUNDLE.SHA256SUMS | wc -l   # 94
git show 8ebaf8daad:verifier-pins.json | python3 -I -c 'import json,sys; print(len(json.load(sys.stdin)["pins"]))'   # 27
python3 -I -c 'import json; print(len(json.load(open("verifier-pins.json"))["pins"]))'                       # 30 on this tree (v2, § 1)
# after § 2's block has written paths.txt: git log --format='%h %ad %s' --date=short 8ebaf8daad..HEAD -- $(cat .qa-scratch/t45/paths.txt)   # exactly 0ceb2994c5 and 033eb7ed23 (v2, § 1)
node --version                                                       # v24.21.0 on 2026-10-25: `run test` needs type stripping (v2)
"$D/tools/rules-check" --quiet; echo "rc=$?"; "$D/tools/register-check" | tail -1
git push -u origin feature/m6-tooling-council-692
```

## 2. Scope

**52 paths, 25,848 lines (the inventory's column); all 52 fork-own; 23
TypeScript, 22 JavaScript, 4 JSON, 1 text, 1 Python, 1 shell; reach `n/a`
52.** The membership is the inventory's rows in area `tooling-and-guards`
matching the five globs -- `scripts/**`, `seed/**`, `verifier-pins.json`,
`council-seat-efforts.json`, `tools/council/**` -- and **30 more rows match
the globs in other areas** (the build engine's `scripts/`), which are not
members. The block, at `2174265e9c`:

```bash
git show 2174265e9c:docs/reviews/inventory.json | python3 -I -c '
import json,sys,collections
inv=json.load(sys.stdin); cols=inv["columns"]; rows=[dict(zip(cols,r)) for r in inv["rows"]]
globs=["scripts/**","seed/**","verifier-pins.json","council-seat-efforts.json","tools/council/**"]
def sel(p):
    for g in globs:
        if g.endswith("/**"):
            if p.startswith(g[:-3]+"/"): return True
        elif p==g: return True
    return False
t=[r for r in rows if r["tree"]=="distribution" and r["area"]=="tooling-and-guards" and sel(r["path"])]
print("paths",len(t),"lines",sum(r["lines"] or 0 for r in t), dict(collections.Counter(r["tier"] for r in t)), dict(collections.Counter(r["language"] for r in t)), dict(collections.Counter(r["reach"] for r in t)))
print("in other areas:", sum(1 for r in rows if r["tree"]=="distribution" and sel(r["path"]) and r["area"]!="tooling-and-guards"))
import os; os.makedirs(".qa-scratch/t45", exist_ok=True)
open(".qa-scratch/t45/paths.txt","w").write("".join(r["path"]+"\n" for r in sorted(t,key=lambda r:r["path"])))'
# paths 52 lines 25848 {'fork-own': 52} {'json': 4, 'typescript': 23, 'javascript': 22, 'text': 1, 'python': 1, 'shell': 1} {'n/a': 52}
# in other areas: 30
```

**By place:** `scripts/` 20 files (the Facilitator `council-invoke.ts`,
3,701 lines; `council-run-start.ts`; the stage controller `.mjs` set; the
lints and verifiers; `forge-write-status.mjs`, pinned and unimported),
`scripts/lib/` 24 (the staged stores, the roster, the verification,
`verifier-pins.ts`, the Mistral tokenizer `.py` with its 4-line
`council-mistral-requirements.txt`), `scripts/__tests__/` 2, `seed/corpus/`
2 (`manifest.json`, 807 lines, `corpusVersion` 4.29.1 generated
2026-09-29; `banner.mjs`), the two root JSON files (`verifier-pins.json`,
169 lines, `schema_version` `council-verifier-pins@2.0.0` (the field; `jq .schema` is null -- v2), **27 pins** at the hash (30 on the lane's tree, § 1);
`council-seat-efforts.json`, 352 lines, `refreshed_at` 2026-09-28 from
`https://openrouter.ai/api/v1/models`), and `tools/council/` 2 (the fork's
own: `run`, 51 lines, the wrapper that sources `~/.config/council/env` only
at mode 600 and execs `tsx scripts/<s>`; `package.json`, 8 lines:
`devDependencies.tsx ^4.22.4`, `dependencies.@aws-sdk/client-bedrock-runtime ^3.1073.0`, **no lockfile committed, by policy: `.gitignore:67` ignores `tools/council/package-lock.json`** and `:66` its `node_modules/`, so a resolved version is never recorded and the currency lead is about that line, not about an omission -- v2).

**Provenance, read at the hash.** `IMPORTED-FROM.md` and
`COUNCIL-BUNDLE.md` (both under `.claude/skills/council/`, not members)
record the delivery: scaffold `main` at `7be6721be24458910e75ca639f318d25ffe7e8d5`
(2026-09-30, corpus 4.29.1 plus #976), **94 files, byte-identical to that
commit, SHA-256 of each in `COUNCIL-BUNDLE.SHA256SUMS`**, with the fork's **five adaptations** listed (1: the anchor landing on the fork's repository in `council-run-start.ts`, and the two tests *inside* `council-toolchain.node-test.mjs` that asserted the Forge helper and remote now asserting the fork's; 2: the wordlist sweep over 22 delivered files; 3: ten fixture key literals in the two `__tests__/` files built at run time with `join`; 4: one line of the mistral agent; 5: the five-seat description) and each adapted pinned file re-pinned with a `repin_reason` (D-WORKFLOW-089). The rules' front matter, which version 1 listed as an adaptation, is a row of the file's location table (`.github/instructions/*.instructions.md` to `.claude/rules/*.md`): a relocation, with no re-pin (v2). **The coordinator's comparison of the 52
members' bytes at `8ebaf8daad` with the SUMS:** 50 members are listed in
the SUMS, **41 are byte-equal to the export, 9 differ**
(`scripts/__tests__/council-invoke-routing.node-test.ts`,
`scripts/__tests__/lint-council-seat-efforts.node-test.ts`,
`scripts/council-invoke.ts`, `scripts/council-run-start.ts`,
`scripts/council-toolchain.node-test.mjs`, `scripts/forge-write-status.mjs`,
`scripts/lint-council-run.ts`, `seed/corpus/manifest.json`,
`verifier-pins.json`), and 2 are not in the SUMS at all (`tools/council/run`,
`tools/council/package.json`: the fork's own wrapper, D-WORKFLOW-088's one
addition). Of the 9 that differ, **4 carry a `repin_reason` in
`verifier-pins.json`** (`council-invoke.ts` and `council-run-start.ts`,
re-pinned 2026-10-04 by blitterbot for D-WORKFLOW-144/#409;
`forge-write-status.mjs` and `lint-council-run.ts`, 2026-09-30 for
D-WORKFLOW-088/089), and **5 are not pinned** (the two `__tests__/` tests -- `IMPORTED-FROM.md`'s item 3, the ten fixture literals, plus the sweep's *one test*; `council-toolchain.node-test.mjs` -- item 1's two Forge assertions and the sweep's comments (version 1 put the Forge assertions on all three; they are in the `.mjs` alone -- v2); `seed/corpus/manifest.json` -- five paths swept; `verifier-pins.json` itself, which cannot pin itself). **The table this slice writes reconciles those three ledgers --
the SUMS, the pins, `IMPORTED-FROM.md`'s list -- against the bytes, file by
file.** Fork commits on the 52 at the hash: **5** by § 7's own command (`git log --oneline 8ebaf8daad -- <the 52> | wc -l`): `b3e5c92559` 2026-09-05 (the first import of the skill and its Facilitator, #70), `4796a78983` the same day (the verification toolchain pinned beside the scripts), `5f1b343d25` 2026-09-30 (the scaffold export at its own paths), `4bf31083c7` 2026-10-02 (#372) and `a9af618398` 2026-10-04 (the identity: the inventory's `last_fork_commit` for `council-invoke.ts`, `council-run-start.ts` and `verifier-pins.json`; **48** members' is `5f1b343d25` and `tools/council/package.json`'s is `b3e5c92559`). Version 1 said 8 and named 7: that was `tools/council/`'s own log, six commits including `b4d0fc4da6`, `1633cbcac2` and `d430818548`, of which the first two touch none of the 52 at the hash -- a count over the wrong set (v2). None on `upstream/next`; the lane's tree adds § 1's two.

**Currency, read on 2026-10-25:** `npm view tsx version` **4.23.15** against
`^4.22.4`; `npm view @aws-sdk/client-bedrock-runtime version` **3.1156.0**
against `^3.1073.0` -- both ranges admit the latest, and with no lockfile
every `npm install --prefix tools/council` takes whatever the registry
serves that day, which the four slices' provenance records do not name;
`council-seat-efforts.json` is 27 days old at dispatch (`refreshed_at`
2026-09-28) and its refresh is `tools/council/run efforts --refresh` (`lint-council-seat-efforts.ts`), **which needs `OPENROUTER_API_KEY`**: it sends `Authorization: Bearer` to OpenRouter's models and endpoints routes (`:279-316` at the hash) and prints `[FAIL refresh_no_key]` without the key; there is no key-free refresh and no `--help` (the flags are `--strict` and `--refresh`, `:265-266`; anything else validates). So **the slice never passes `--refresh`**: it runs the offline validation (`run efforts` with no flag -- the snapshot against the pins, no network) and records the snapshot's age and that a fresh reading needs the key (v2; version 1 said *reads the public models list*). `mistral-common==1.11.7` (PyPI's latest 1.12.0 on 2026-10-25) and `numpy<2.4; python_version < "3.13"` (unconstrained on 3.13 and later; PyPI's latest 2.5.4 -- v2) in `council-mistral-requirements.txt` pin a tokenizer for a seat that left the
roster on 2026-09-27 (scaffold#915, `adversarial-council.md`); the agents
beside the export (`.claude/agents/council-member-*.agent.md`, 8 files, not
members) carry two marked *Historical ... Inactive ... do not invoke*
(deepseek, grok) and one *outside every run profile* (mistral).

**Who runs it:** every Independent-depth slice's Phase 4.6 through
`tools/council/run invoke --member gpt --provider openrouter` (four this
week); the `council` and `council-research` skills; the code-auditor
skill's phases and templates; `adversarial-council.md` and
`council-substrate-integrity.md` name it as the only route to a member.
**Its record:** the four slices' `second-opinions/` (probe and refutation provenance, each naming the served model, effort and provider: `declared_model`, `served_provider`, `model_identity_source = provider_response`, tokens, `usage.cost`, `duration_ms`, and `facilitator_version` -- the branch's `1.14.1-pixelelated.2`, § 1, not the hash's `1.14.0` -- v2), and `research/` (council artifacts, a personal path).

**What this slice does not touch:** the council scripts' bytes (a refresh is
a copy of the next export, the maintainer's agent's; a local fix is a
D-WORKFLOW-088 question for the coordinator); the agents and skills (not
members; read for Q6 and Q7); the key file; any provider.

## 3. Read first

1. `next:AGENTS.md`; the every-session rules; **`adversarial-council.md`**
   (the model floor and the deprecated seats) and
   **`council-substrate-integrity.md`** (the Facilitator as the only route);
   `engineering-practices.md` § A name is not a behaviour (a pin's reason is
   a claim about one tree).
2. `docs/reviews/plan-for-the-plan.md` whole (§ 2 on tables and refreshed
   exports; § 6c on Local depth); `docs/reviews/order.md` § T45; this brief
   whole.
3. `.claude/skills/council/IMPORTED-FROM.md`, `COUNCIL-BUNDLE.md` and
   `COUNCIL-BUNDLE.SHA256SUMS` (the delivery's record); `verifier-pins.json`
   (its `note` and every `repin_reason`); `council-seat-efforts.json`'s
   header; `tools/council/run` whole.
4. The live M6 body; #692 (with its comments); #903 (the epic, its futro
   comment and the T45 addendum); #339; #346 (the maintainer's channel);
   #70, #372, #409 (the toolchain's own issues); the four slices'
   `second-opinions/review-plan.json` and one `*.provenance.json` each
   (`git show <tip>:docs/audits/<folder>/second-opinions/<file>`: T9
   `995e7f869f`, T10 `7182f743ea`, T12 `d9991735d8`, T14 `7c1d729b57`).
5. The register rows D-WORKFLOW-088, 089, 090, 135, 144, 184, 195 and
   D-QA-048, D-WORKFLOW-049 (which audits go through the Facilitator and
   why).

## 4. The questions

The seven renovation questions of plan § 4, with **package currency** as
the lens and the table as the answer:

- **Q1 Modernize:** the export's paths mirrored at the repository root
  (`scripts/`, `seed/`, two root JSON files) beside the build engine's own
  `scripts/`: what the mirror costs (the 30 non-member rows the globs catch;
  `rules-check`'s and the push guard's enumerations of these paths) and
  whether the plan's "refreshed by copying the next export" has a recorded
  procedure (a lead if not).
- **Q2 Standards:** `tools/council/run`'s guards (the env file's mode 600,
  the `set -euo pipefail`, the exec); `npm install` without a lockfile; the
  provenance records' fields against what `adversarial-council.md` demands
  (served model, effort, provider, `allow_fallbacks: false`).
- **Q3 Bugs:** the toolchain's own tests on both trees (`tools/council/run test`, which runs the toolchain test and the seat-efforts test under plain `node --test` on files importing `./lib/*.ts` -- so a Node with type stripping, the host's `v24.21.0` -- and the routing test under `tsx`; at the hash the three files hold 37, 34 and 19 top-level `test(` calls by grep, and the export commit's message claims 39, 109 and 19 with generated cases: the run's own count is the figure -- v2), `verify-pins` (every pin matches; every re-pin accountable),
  `drift` (`check-stale-blob-drift.ts`), `lint` over one of the four slices'
  run directories; a test that fails, a pin that does not match, or a drift
  the checker misses is a finding.
- **Q4 Package currency -- the table's second half:** the two npm
  dependencies (declared range, resolved version on this host after
  `npm install`, latest on the registry, the gap in versions and days);
  the Python requirements (pinned version, latest on PyPI, read-only); the seat-efforts snapshot's age, the offline validation's verdict (`run efforts`, no flag), and the sentence that a fresh reading needs `OPENROUTER_API_KEY` and was not run (v2); the corpus version against any
  reachable export (CANNOT here, said with the scaffold checkout's version
  beside it); the roster against the model floor: every active seat's slug and effort in `scripts/council-invoke.ts`'s `OPENROUTER_SEATS` (`:1404-1481` at the hash; `scripts/lib/council-roster.ts` imports it and holds `MEMBER_IDS` at `:21` and no slug -- v2) equal to `adversarial-council.md`'s, read at the hash **and on the branch** (the two commits changed the routing; a seat moved off the floor is a finding).
- **Q5 Efficiency:** what a seat call costs in the record (the four slices'
  provenance: tokens, seconds, USD where recorded) and what `npm install`
  per slice costs (the lane times its own).
- **Q6 Dead ends:** the Mistral tokenizer and its requirements (a seat
  outside every run profile since scaffold#915); `forge-write-status.mjs`
  (pinned, unimported, placeholder defaults); the inactive agents (deepseek,
  grok) and the mistral agent; the `--provider` and `--member` values the
  Facilitator accepts that no rule names -- each a row with *kept because
  the export carries it* (D-WORKFLOW-088: nothing is deleted from an
  export) or a lead for the coordinator to carry to the export's owner.
- **Q7 Clarity and structure -- the table's first half:** the provenance
  table, 52 rows: path, lines, listed in the SUMS (yes/no), byte-equal to
  the export (yes/no), pinned (yes/no, `repinned_at`, `repin_reason`),
  named in `IMPORTED-FROM.md`'s adaptations (yes/no), last fork commit --
  and the reconciliation: every differing file accounted for by a re-pin or
  the IMPORTED-FROM list, or a drift nobody recorded (a finding); every
  re-pin's reason true of the bytes (the 2026-10-04 identity re-pin's
  *update only the project organization URLs* checked against the diff);
  the three descriptions of the toolchain (the `run` header, the two rules,
  the index rows in `instruction-files.md`) against the code.

## 5. The evidence floor

The code-auditor skill's rules apply to every verdict (`SKILL.md` § Evidence
floor):

1. Tracker state is never sole evidence: every cell cites a command's
   output (`sha256sum` against the SUMS, `git log`, `npm view`, the tests'
   exits) or a file's field.
2. Mechanical evidence outranks reading: a pin's `repin_reason` is a claim;
   the diff against the export's bytes is the evidence.
3. **The bench is the host; no guest, no provider.** **Can this be done on
   the VM? Yes -- on the host: a table of bytes, pins, versions and the
   toolchain's own tests, none of which needs a guest, a device or a
   provider; the network uses are read-only and keyless** -- `npm view`, PyPI's JSON, and `npm install --prefix tools/council` for the tests; **no OpenRouter call at all: a seat-efforts refresh needs the key** (v2). `tools/council/run invoke` is never run.
4. **What result would have produced a FAIL** is asked of every PASS, in
   writing, in `02`.
5. **Every `tools/council/run` call in this slice is made with
   `COUNCIL_ENV_FILE=/nonexistent`, and the running log says so (v2).** The
   wrapper sources `$HOME/.config/council/env` for every subcommand when the
   file is readable at mode 600 (`run:21-28`) and skips an absent one in
   silence, so the variable keeps the key out of every process the slice
   starts. That the guard is one-sided -- a readable file at another mode is
   refused, an absent file is a silent bypass -- is itself a Q2 row.
6. **Two trees, each run (v2).** The toolchain's checks run on the lane's
   tree (the branch's bytes, the local Facilitator) and on a clone checked
   out at `8ebaf8daad` under `/workspace/tmp/m6-t45/at-hash` (a clone, never
   `git archive`: the tests spawn git). Each run names its tree.

**The runs, with what the coordinator read** (the lane runs each at stage A
in its worktree and records the exit, the wall time and the summary line;
`TMPDIR` under `/workspace/tmp/m6-t45/`):

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-council-692
cd "$D"; export TMPDIR=/workspace/tmp/m6-t45/tmp; mkdir -p "$TMPDIR" .qa-scratch/t45
# the bytes against the export (the coordinator's figures: 50 listed, 41 equal, 9 differ, 2 unlisted)
git show 8ebaf8daad:.claude/skills/council/COUNCIL-BUNDLE.SHA256SUMS > .qa-scratch/t45/sums.txt
while read -r p; do h=$(git show 8ebaf8daad:"$p" | sha256sum | cut -d' ' -f1); s=$(awk -v p="$p" '$2==p{print $1}' .qa-scratch/t45/sums.txt); printf '%s %s %s\n' "$p" "${s:+listed}" "$([ -n "$s" ] && { [ "$s" = "$h" ] && echo equal || echo DIFFERS; } || echo unlisted)"; done < .qa-scratch/t45/paths.txt | sort -k3 | tee .qa-scratch/t45/provenance.txt | awk '{print $3}' | sort | uniq -c
# the pins and their reasons (27 at the hash; 30 on this tree, v2)
for ref in 8ebaf8daad HEAD; do echo "== $ref"; git show $ref:verifier-pins.json | python3 -I -c 'import json,sys; d=json.load(sys.stdin); [print(k, v.get("repinned_at","")[:10], (v.get("repin_reason") or "")[:80]) for k,v in d["pins"].items()]'; done
# the branch's delta against the hash (v2): exactly two commits, ten files
git log --format='%h %ad %s' --date=short 8ebaf8daad..HEAD -- $(cat .qa-scratch/t45/paths.txt) | cut -c1-100
git diff --stat 8ebaf8daad HEAD -- $(cat .qa-scratch/t45/paths.txt) | tail -1    # 10 files changed, 356 insertions(+), 28 deletions(-)
grep -n 'export const FACILITATOR_VERSION' scripts/council-invoke.ts; git show 8ebaf8daad:scripts/council-invoke.ts | grep -n 'export const FACILITATOR_VERSION'
# the clone at the hash (v2): the second tree the checks run on
mkdir -p /workspace/tmp/m6-t45 && git clone -q --no-checkout "$D" /workspace/tmp/m6-t45/at-hash && git -C /workspace/tmp/m6-t45/at-hash checkout -q 8ebaf8daad && git -C /workspace/tmp/m6-t45/at-hash rev-parse HEAD
# the toolchain's own checks, on each tree (npm install first, under tools/council only; no provider;
# every run call with COUNCIL_ENV_FILE=/nonexistent so the wrapper sources no key -- v2)
export COUNCIL_ENV_FILE=/nonexistent
for T in "$D" /workspace/tmp/m6-t45/at-hash; do ( cd "$T"; O="$D/.qa-scratch/t45/$(basename "$T")"; mkdir -p "$O"; echo "== $T at $(git rev-parse --short HEAD)"
  s=$(date +%s); npm install --prefix tools/council > "$O/npm-install.out" 2>&1; echo "npm install rc=$? $(( $(date +%s) - s ))s"; ls tools/council/node_modules/.bin/tsx && npm ls --prefix tools/council --depth=0 2>/dev/null | tail -4   # the resolved versions
  tools/council/run verify-pins > "$O/verify-pins.out" 2>&1; echo "verify-pins rc=$? $(tail -1 "$O/verify-pins.out" | cut -c1-100)"
  tools/council/run drift > "$O/drift.out" 2>&1; echo "drift rc=$? $(tail -1 "$O/drift.out" | cut -c1-100)"
  tools/council/run efforts > "$O/efforts.out" 2>&1; echo "efforts (offline validation; never --refresh, it needs the key) rc=$? $(tail -1 "$O/efforts.out" | cut -c1-100)"
  s=$(date +%s); tools/council/run test > "$O/test.out" 2>&1; echo "test rc=$? $(( $(date +%s) - s ))s $(grep -c -E '^ok ' "$O/test.out") ok lines, $(grep -c -E '^not ok ' "$O/test.out") not ok"
); done
tools/council/run lint "$(ls -d docs/audits/*/second-opinions 2>/dev/null | head -1)" > .qa-scratch/t45/lint.out 2>&1; echo "lint rc=$? $(tail -1 .qa-scratch/t45/lint.out | cut -c1-100)"   # a run directory the lint can read, or the refusal and why (the branch's tree)
# currency, read-only (the coordinator's: tsx 4.23.15, bedrock-runtime 3.1156.0 on 2026-10-25)
for p in tsx @aws-sdk/client-bedrock-runtime; do printf '%s latest %s\n' "$p" "$(timeout 30 npm view "$p" version 2>/dev/null)"; done
curl -s --max-time 20 https://pypi.org/pypi/mistral-common/json | python3 -I -c 'import json,sys; print("mistral-common latest", json.load(sys.stdin)["info"]["version"])'
# the scaffold checkout on this host (read only): older than the export
git -C /home/max/Development/scaffold log -1 --format='%h %ad' --date=short; git -C /home/max/Development/scaffold show HEAD:seed/corpus/manifest.json | python3 -I -c 'import json,sys; print("scaffold here corpusVersion", json.load(sys.stdin)["corpusVersion"])'
git show 8ebaf8daad:seed/corpus/manifest.json | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print("ours", d["corpusVersion"], d["generated"])'
# the roster against the floor: the slugs and efforts live in council-invoke.ts's OPENROUTER_SEATS, not in the roster file (v2)
for ref in 8ebaf8daad HEAD; do echo "== $ref"; git show $ref:scripts/council-invoke.ts | grep -n -E 'anthropic/claude-fable-5.1|openai/gpt-6-astra|meta/muse-spark|moonshotai/kimi|google/gemini|allow_fallbacks|effort: "' | head -24 | cut -c1-120; done
grep -n -E 'MEMBER_IDS|OPENROUTER_SEATS' scripts/lib/council-roster.ts | head -4 | cut -c1-120
grep -n -E 'claude-fable-5.1|gpt-6-astra|Muse Spark' .claude/rules/adversarial-council.md | head -6 | cut -c1-120
```

**The reading, per file:** each of the 52 gets its provenance row from the
commands above; the 9 that differ are read against `IMPORTED-FROM.md`'s
list and the pins' reasons, hunk by hunk (`git diff` between the export's
bytes -- reconstructed from the SUMS where only a hash exists, the file is
read as it is and the difference described -- and the hash's); the four provenance records are read for the fields the rule demands; **the ten files of the branch's delta are read hunk by hunk against the two commits' messages and the three re-pin reasons** (a reason's claims against its diff, as for the 2026-10-04 re-pin -- v2); the dead-end candidates are read for what still imports them (`grep -rn` over the
members and the skills).

## 6. Outputs

All in the worktree, committed on its branch with messages that cite `#692`
(`Refs #692`, never a closing keyword); the stage letters are plan § 6b's.

| Output | Path | Shape | Stage |
| --- | --- | --- | --- |
| Running log | `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-council/00-running-log.md` | the flight recorder: model and effort, `reviewed-at` with `8ebaf8daad`, the host file's last line and census at stage A, every run with exit and wall time | A onward |
| Research notes | `.../01-research-notes.md` | § Scope: the 52 re-derived with § 2's block, the 30 non-members named, the provenance (5 fork commits at the hash, none upstream; the branch's two beyond it), the delivery's record | A |
| Forward audit | `.../02-forward-audit.md` | Phase 2 over #692's checklist; **§ Provenance: the 52-row table** (path, lines, SUMS, byte-equal at the hash, pinned/repin, IMPORTED-FROM, last commit, **and a `branch` column: equal to the hash, or changed by `0ceb2994c5`/`033eb7ed23` -- v2**) and § Reconciliation (every difference accounted for or a finding; the branch's delta as its own rows); **a coverage table with one row per path under `## Coverage`** (52); § The runs, at the hash and on the branch; § Proofs with `proved:` cells | B |
| Retrospective | `.../03-retrospective.md` | Phase 3 with § 3.5 for the seams: the export x the fork's adaptations x the pins x the push guard's personal paths x the four slices' runs | B |
| Analysis | `.../04-analysis.md` | Phase 4 § Finding Verification; **§ Renovation face Q1 to Q7, Q4 carrying the currency table and Q6 the dead-end rows**; § Instruction File Recommendations | B |
| Second opinions | `.../second-opinions/review-plan.json` | depth `local`, reviewers `[]`, the sentence *the lint and the counts are the check* | B |
| Lint, before D | `tools/lint-audit-artifacts <folder> --phase pre-issue` | `PASS pre-issue artifacts (...)` | C |
| Punch list | `.../05-punch-list.md` | Phase 5: every item with `question:`, severity, category, where, acceptance, `Already written:`, the VM line; the YAML `punch_index` | D |
| Audit issue | GitHub, labels `audit`, `punch-list`, milestone M6, a sub-issue of #692 | `Audit: M6 T45 the council toolchain -- N findings (...)` | D |
| Bugs | GitHub, label `bug`, milestone M6 | one per defect proven by a run (a failing toolchain test, a pin that does not match, a drift the checker misses); a currency gap is a lead, not a bug | D |
| Retro | `docs/retros/<date>-m6-tooling-council.md`, posted on #692 | the mini-retro; what the slice did to the two time-to-play numbers (nothing); what the table says the next export must carry | G |

## 7. Acceptance

The checklist on #692 becomes this section at dispatch, written there by the
coordinator in place of P1's five generated ones (until then #692 carries
those five). Every checkbox names the artifact that ticks it (D-QA-044); the
coordinator ticks at acceptance, from the artifacts, never from the
hand-back's words.

- [ ] `docs/audits/<date>-epic-m6-tooling-council/` holds `00-running-log.md` and `01-research-notes.md` to `05-punch-list.md`.
- [ ] `tools/lint-audit-artifacts docs/audits/<date>-epic-m6-tooling-council/` prints `PASS` (its default `resolution` phase, at close; before stage D the same command with `--phase pre-issue` prints `PASS pre-issue artifacts`), the renovation face included.
- [ ] `second-opinions/review-plan.json` records `depth: local`, `reviewers: []` and the sentence *the lint and the counts are the check*; no `*.provenance.json` from a provider call exists in the folder (`ls second-opinions/ | grep -c provenance` is 0).
- [ ] The slice's punch-list issue has every item at a Phase 7 outcome: resolved with its commit, deferred to a named issue (a lead for the coordinator or the export's owner), or recorded as a design with its sentence; `tools/box-check --issue <N>` 0 fail; the ticked and open counts read back by name.
- [ ] `reviewed-at:` and `fixed-at:` above carry the lane's commits; the read is on `8ebaf8daad`'s bytes for the 52, and the lane's tree differs from the hash on exactly the ten files of `0ceb2994c5` and `033eb7ed23`: `git log --format=%h 8ebaf8daad..<reviewed-at> -- $(cat .qa-scratch/t45/paths.txt)` prints exactly those two hashes, and `git diff --stat 8ebaf8daad <reviewed-at> -- $(cat .qa-scratch/t45/paths.txt) | tail -1` reads `10 files changed, 356 insertions(+), 28 deletions(-)`.
- [ ] `01-research-notes.md` § Scope records § 2's block with its output (52 paths, 25,848 lines, 52 fork-own, 23/22/4/1/1/1 by language, 30 in other areas), the 5 fork commits at the hash (`git log --oneline 8ebaf8daad -- <the 52> | wc -l`), the two the branch adds (`git log --format=%h 8ebaf8daad..HEAD -- <the 52>`) and the delivery's record (`7be6721be2…`, 94 files, corpus 4.29.1).
- [ ] `02-forward-audit.md` carries a coverage table with exactly one row per path under its own `## Coverage` heading, the path in backticks as the first cell: ``awk '/^## Coverage/{p=1;next} /^## /{p=0} p' 02-forward-audit.md | grep -c -E '^\| `'`` prints `52`.
- [ ] `02-forward-audit.md` § Provenance carries 52 rows with the columns listed in § 6 and its counts agree with the coordinator's (50 listed in the SUMS, 41 byte-equal, 9 differ, 2 unlisted) or state the delta with the command that produced it; § Reconciliation accounts for each of the 9 by a re-pin reason or an `IMPORTED-FROM.md` entry, names any difference neither records, and judges the 2026-10-04 re-pin's reason against its diff; **and the branch's delta has its own rows**: the ten files, the tree's count (36 equal, 14 differ, 2 unlisted), the three added and three re-pinned pins with their reasons judged against their diffs, `FACILITATOR_VERSION` at the hash (`1.14.0`) and on the branch (`1.14.1-pixelelated.2`), the `.1`/`.2` mismatch between the added pins' reasons and the code, and the missing register row, named as a lead for the coordinator (never fixed by the lane).
- [ ] `02-forward-audit.md` § The runs records, **for each of the two trees** (the clone at `8ebaf8daad` under `/workspace/tmp/m6-t45/at-hash`, named by `git rev-parse HEAD`, and the branch), `npm install` (exit, wall time, the resolved `tsx` and `@aws-sdk/client-bedrock-runtime` versions from `npm ls`), `verify-pins`, `drift`, `efforts` (the offline validation; `--refresh` never passed) and `test` (the three test files' `ok`/`not ok` counts; `node --version`), and `lint` over one recorded run directory on the branch, each with exit and summary line and *a FAIL would mean ...*; a run that cannot be made is `CANNOT` with its reason, never a pass.
- [ ] `00-running-log.md` shows every `tools/council/run` call made with `COUNCIL_ENV_FILE=/nonexistent` (so the wrapper sourced no key), no `tools/council/run invoke`, no `--refresh`, no other read of `~/.config/council/env` or any credential file, no guest, no build, no edit to a member file, no write under `/workspace/repos/rocknix*`, `/home/max/Development/scaffold*` or `/tmp`.
- [ ] `04-analysis.md` § Q4 carries the currency table: the two npm dependencies (declared, resolved, latest, gap), `mistral-common` and `numpy` (pinned, with numpy's `python_version < "3.13"` marker; latest), the seat-efforts snapshot (age in days; the offline validation's verdict; the sentence that a fresh reading needs `OPENROUTER_API_KEY` and was not run), the corpus version against the scaffold checkout on this host (`CANNOT: no export newer than 7be6721b is reachable here`, with 3.29.1 and 4.29.1 named), and every active seat's slug and effort in `council-invoke.ts`'s `OPENROUTER_SEATS`, at the hash and on the branch, against `adversarial-council.md`'s floor.
- [ ] `04-analysis.md` § Q6 carries a row for each dead-end candidate (the Mistral tokenizer and its requirements, `forge-write-status.mjs`, the deepseek, grok and mistral agents, any `--provider`/`--member` value no rule names), each with what still imports or names it and the disposition *kept because the export carries it* or *a lead for the coordinator*; nothing is removed.
- [ ] `04-analysis.md` § Q7 reads the three descriptions (the `run` header, `adversarial-council.md` and `council-substrate-integrity.md`, the `instruction-files.md` rows for `council/`) against the code, with each drift named as a lead; no rule or index row is edited.
- [ ] Every proof in `02-forward-audit.md` carries a `proved:` cell reading `tree`, `history`, `tool-run`, `fix-tree`, `fix-case` or `design`; every punch item carries `question:`; every `bug` passes `tools/box-check --issue N`; no member file is changed **by the lane** (`git log --format=%h <dispatch tip>..<tip> -- $(cat .qa-scratch/t45/paths.txt)` is empty, the dispatch tip being the one the dispatch comment names).
- [ ] The retro exists at `docs/retros/<date>-m6-tooling-council.md`, is posted on #692, says what the slice did to the two time-to-play numbers (nothing) and what the next export must carry (the table's leads).
- [ ] `tools/register-check`, `tools/work-log-index --check`, `tools/rules-check --quiet`, `tools/forbidden-terms-check` and `.githooks/hooks-test` pass on the branch before its merge (after the coordinator's hand-back merge).

## 8. Stop conditions

Stop only on: every item of § 7 that is this lane's ticked and the branch
pushed (the hand-back); **the stage-D pause**; an explicit maintainer pause
on #692; a blocker named on #692 with what is needed; a branch that differs from `8ebaf8daad` on a member **other than the ten files of `0ceb2994c5` and `033eb7ed23`** at stage A (v2); or an execution limit, stated as
such with the running log current. A checkpoint is not a stop; a differing
count is a delta; `next` moving is drift. An idle session says it is idle on
#692, **does not end a turn on a post that asks nothing**, and **updates its
session pointer at every checkpoint** (#1014).

**What never runs in this slice:** `tools/council/run invoke` or any
provider call (the toolchain is the subject); any read of a credential file
(`~/.config/council/env`, `~/.ROCKNIX/options`,
`~/.config/rocknix/forbidden-terms`); a refresh of the export, a re-pin, or
an edit to any member file (D-WORKFLOW-088: a drift is a lead, a fix is a
copy of the next export); an edit to the agents or skills beside it; a
push to any branch but the lane's own; a guest; a build; `fork-worktree
sync|remove|repair`; an edit to a rule, `CLAUDE.md`, `AGENTS.md`, a decided
register row or `.github/sessions/saved-session-state-next.md`; a write
under `/workspace/repos/rocknix*`, `/home/max/Development/scaffold*` (read
only) or `/tmp` (use `/workspace/tmp/m6-t45/`); `npm install` anywhere but `--prefix tools/council` (in the worktree and in the clone at the hash); `tools/council/run efforts --refresh`, or any `tools/council/run` call without `COUNCIL_ENV_FILE=/nonexistent` (v2); a credential-shaped literal written anywhere;
`--no-verify`; bare `git stash`; `git worktree remove --force` or `rm -rf`
on a worktree or a bare variable path.

## 9. Ceremonies owed

- A work-log entry per session headed `#692`, its time from `date -u` in
  the same command, its prose through a quoted heredoc or the Write tool;
  `tools/work-log-index --write` after it (in this worktree only).
- A friction line the moment something slows, with `issue: #692` or the
  guard.
- The VM question written before any proof (§ 5: the host; no guest; the
  read-only network uses named).
- The mini-retro at stage G, posted on #692, Instruction-Recommendations
  mode; its *adjustments* are proposals for the coordinator.
- A register row the same session for any decision the slice forces; the
  next Decided ID is checked on every pushed branch at the time (on
  2026-10-25 the highest Decided rows are D-WORKFLOW-205, D-QA-062 and
  D-INFRA-031, the coordinator's; T15 runs beside this lane); it goes at
  the end of `## Decided`, and a row is never edited.
- The merge notes: when `next` moves, the **coordinator** merges `next`
  into this branch, never between stage A and stage D; the coordinator
  merges its own branch into this one at hand-back before the last
  criterion's checkers run; a merge with conflicts is checked for leftover
  markers before it is committed (#696), and the ledgers are united by
  whole entries.
- Commit messages `docs: ...` (this slice edits no tool), each with `Refs
  #692` and the attribution line; `git add -A` only after `git status
  --short` shows nothing a run left behind (`.qa-scratch/` is gitignored;
  `tools/council/node_modules/` is gitignored -- check with `git
  check-ignore -v tools/council/node_modules/x` before the first `npm
  install`, and if it is not ignored, say so on #692 before anything is
  installed).

## 10. Hand-back

The coordinator accepts by reading, in this order, without re-reviewing:
#692's checkboxes against their artifacts; the lint's `PASS` line; the
review plan (local, no reviewer, no provenance file); the audit issue's
checkboxes all at an outcome; the coverage table's row count (52) and the
provenance table's counts against § 2; **re-running on an export of the tip
under `/workspace/tmp`: the inventory block, the bytes against the SUMS
(the four counts), the pins' count on both trees, the members' diff against the hash (exactly the two commits' ten files) and against the dispatch tip (empty), `npm install --prefix tools/council` then `verify-pins`, `drift`, `efforts` and `test` on both trees with `COUNCIL_ENV_FILE=/nonexistent` (their exits and the test counts), `npm view` for the two
dependencies;** `register-check` and `rules-check` on a simulated merge
with the coordinator's tip (the ledgers united); the retro's answers. The
lane posts one hand-back comment naming the tip and each artifact by path,
writes `reviewed-at:` and `fixed-at:` into #692's body, then says it is
idle. After acceptance the coordinator closes the audit issue, prompts the
lane for `audit-completion.json` and the full lint, merges the branch in
its turn after the M7 candidate (after T15's, before T4's), regenerates the
ledgers, and closes #692 when every row is proven; the table's leads go to
the maintainer and the export's owner on #346.

**The readings before dispatch** (plan § 3, principle 3): the area's futro
(#903) carries this slice's kickoff addendum, and a stranger's proof of
this brief is run by a reader with no context before dispatch; version 2
records what each found.
