# Session pointer: M6.P2 T45, the council toolchain and runner (#692)

> **Seeded:** 2026-10-25 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch:** `feature/m6-tooling-council-692`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch); the coordinator's tips merged in (`dc81388432` at `337bf46ede`, then `b2caa5ee28` at `e2fdca688b`, `fe43e15058` at `e787bc6939`)
> **Worktree:** `/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-council-692`; the T5, T6, T7, T8, T9 and T12 worktrees beside it (`m6-build-engine-652`, `m6-build-engine-upstream-tools-653`, `m6-generic-packages-reached-654`, `m6-image-packages-655`, `m6-tooling-build-supervision-656`, `m6-tooling-vm-harness-659`) are this session's earlier slices, accepted and idle: read only, until their merges
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there; `/home/max/Development/scaffold` is a scaffold checkout older than the export: read only
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort (the T5 session, `m6-t5-build-engine`), unless #692 says otherwise
> **Epic:** #903 (the tooling and guards: T9, T10, T12 and T14 accepted, T15 running in the T3 session, this slice is the area's last); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Local -- **no reviewer seat**; `review-plan.json` records depth `local`, reviewers `[]`, *the lint and the counts are the check*; **`tools/council/run invoke` is never run** (the toolchain is the subject, not the instrument)
> **The lens:** package currency -- the provenance table (52 rows: the bytes against the export's SUMS, the pins and their reasons, `IMPORTED-FROM.md`'s list, the last fork commit) and the currency table (the two npm dependencies, the Python requirements, the seat-efforts snapshot's age, the corpus version against any reachable export, the roster against the floor); the dead ends kept because the export carries them (D-WORKFLOW-088); nothing is edited or removed
> **The host:** M6's; this slice runs **no guest**, no build, no provider call; `npm install --prefix tools/council` only (`node_modules` there is gitignored, `.gitignore:66`); `TMPDIR` under `/workspace/tmp/m6-t45/`, never `/tmp`
> **The lane's tree beyond the hash (brief § 1, v2):** this branch carries `0ceb2994c5` and `033eb7ed23` (2026-10-22, #636/#638), which `next` does not; they change ten members (`FACILITATOR_VERSION` `1.14.0` at `8ebaf8daad`, `1.14.1-pixelelated.2` here; 27 pins against 30; the SUMS comparison 41/9/2 against 36/14/2). The read stays at `8ebaf8daad`; the delta is tabled as § Provenance rows and the missing register row is a lead for the coordinator; the lane changes none of it; the toolchain's checks run on both trees (a clone at the hash under `/workspace/tmp/m6-t45/at-hash`); every `tools/council/run` call carries `COUNCIL_ENV_FILE=/nonexistent`; `efforts --refresh` is never passed.

## Start here

1. Read `next:AGENTS.md` and the every-session rules under `.claude/rules/`;
   this worktree's rules are `next`'s except the paths the dispatch comment
   on #692 lists: `git diff --stat next -- .claude CLAUDE.md AGENTS.md tools/lint-audit-artifacts`
   prints exactly those; anything else is STALE. `adversarial-council.md`
   (the model floor) and `council-substrate-integrity.md` (the Facilitator
   as the only route) are the two rules this toolchain serves.
2. Read `docs/reviews/plan-for-the-plan.md` whole, then
   `docs/reviews/briefs/tooling-council.md` whole (version 2). The brief is
   the work; its § 7 is the contract, identical to the checklist on #692;
   its § 5 gives the runs; its § 8 names what is never run here.
3. Read `.claude/skills/council/IMPORTED-FROM.md`, `COUNCIL-BUNDLE.md` and
   `COUNCIL-BUNDLE.SHA256SUMS`; `verifier-pins.json`'s note and reasons;
   `tools/council/run` whole; the live
   [M6 ordered plan](https://github.com/pixelelated/distribution/milestone/6),
   #692 (with its comments), #903 (the epic, its futro comment and the T45
   addendum: U-1 to U-6 and A1 to A7), #339, #346 (the maintainer's channel:
   what is open there is not this lane's to decide), #70, #372, #409.
4. Run the brief's first commands (§ 1), then open
   `docs/audits/<yyyy_mm_dd>-epic-m6-tooling-council/00-running-log.md` and
   write stage A -- the hash, the counts, the host file's last line and the
   live census, the bytes comparison's four counts, `npm install`'s result
   and the resolved versions, `verify-pins`, `drift`, `test`, `lint` --
   before reading a file for its row.

## Current focus

**Stage B complete; stage C next** (the punch list drafted and the lint run with `--phase pre-issue`, then the stage-D audit issue and the pause). Updated 2026-10-25, 03:15 UTC.
- **`reviewed-at`:** `32a34393dd`. **The audit folder:** `docs/audits/2026_10_25-epic-m6-tooling-council/`. It holds `00`, `01`, `02`, `03`, `04`, `second-opinions/review-plan.json`, `stage-a/` and `stage-b/`.
- **The findings** (`04` § Finding Verification): F-01 to F-15, none a proven bug.
  - Leads for the coordinator or the export's owner: F-01, F-02, F-04, F-05, F-06, F-07, F-09, F-10, F-12, F-13, F-14, F-15.
  - Designs: F-08, F-11.
  - F-03 (the seal keys) is deferred to the coordinator's #1043, with no bug filed.
- **The lint verdicts:** read in `02` § The runs.
- **The coordinator's answers:** the four `research/council-runs/*` runs are criterion 9's (the brief corrected at `2672582a01`); the seal keys are #1043.
- **Running for this lane:** nothing. The clone at the hash is back at `8ebaf8daad8eaac6…`.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-tooling-council-692; A=$D/docs/audits/2026_10_25-epic-m6-tooling-council
cd "$D" && git status --short && git log --oneline -1
# Stage B: 02's Provenance (52 rows, a branch column), Reconciliation (the 9 at the hash; the branch's 10), Coverage (52),
# The runs (copy stage A's table), Proofs; 03 (seams); 04 (Q1 to Q7, Q4 currency, Q6 dead ends); second-opinions/review-plan.json (local).
# Then the lint with --phase pre-issue (stage C), the punch list and audit issue (stage D, a pause).
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets (#877, #890; #887, #889; #905), T5, T6, T7, T8, T9, T10, T12,
T14, T15, **then this branch**, then T4's last. When `next` moves, the
**coordinator** merges `next` into this branch, and never between stage A
and stage D; the coordinator merges its own branch into this one at
hand-back, before the last criterion's checkers run. Never merge another
lane's feature branch here. Every lane and the M7 lane append to
`docs/decision-register.md`, the day's work log and `docs/work-logs/INDEX.md`:
keep every append, regenerate the index, never edit another lane's rows; a
merge with conflicts is checked for leftover markers before it is committed
(#696), and a union of two ledgers is made by whole entries. The highest
Decided register IDs on 2026-10-25 at the dispatch are D-WORKFLOW-205,
D-QA-062 and D-INFRA-031 (the coordinator's); T15 runs beside this lane;
a new row goes at the end of `## Decided`, and a row is never edited.
Nothing here builds, touches a device, a cloud account, a provider, a key
file, the host's swap, another lane's worktree, or a guest.
