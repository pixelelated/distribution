# Mini Retro: M6.P2 T45, the council toolchain and runner (#692)

**Completed:** 2026-10-25
**Scope of this retro:** the T45 lane at Local depth, covering:
- stage A, the slice's 52 paths, read at `8ebaf8daad`, with the branch's two council commits tabled as rows of their own;
- the provenance and currency tables (`docs/audits/2026_10_25-epic-m6-tooling-council/`);
- the audit issue #1046's 15 items;
- the close-out.

There was no stage E: the lane changes no member, and no item was a lane fix. Not retro'd here, because they are not this lane's: the coordinator's acceptance, the merge, and the Backlog work in #1043, #1044 and #1045.

**Commits:** `reviewed-at` `32a34393dd` (the dispatch tip), `fixed-at` `e1fa041488`.

## What the slice did to the two time-to-play numbers

**Nothing, on either number.** No member reaches an image (`reach: n/a` for all 52), and nothing in the slice ran on a device or a guest. The council toolchain runs on the build host, for audits.

## What the next export must carry

The table's leads for the export's owner are in **Backlog #1045**:

- **F-01:** the local Facilitator fork's reconciliation: #636's terminal content filter (exit 8) and #638's `gemini-argon` audit route. Either scaffold carries both, or the fork's row says why it keeps them.
- **F-02:** a way to retire a contract to the historical path when the Facilitator moves, so the 2026-09-30 runs under `1.14.0` read as historical, not as `council_roster_invalid`.
- **F-05, the export half:** the two council-research lints the integrity rule names.
- **F-07:** a keyed seat-efforts refresh, with a stamp no older than its newest entry.
- **F-09:** a refusal of an inactive member on a single `invoke`.
- **F-14:** a refresh that keeps the export's pristine, SUMS-verified bytes, so the fork's adaptations can be diffed against them.

The fork's own side (F-04, F-05's rule half, F-06, F-10, F-12, F-13, F-15) is **Backlog #1044**, and the committed seal keys are **#1043**.

## What worked well

- **Two trees, the same runs.** Running `verify-pins`, `drift`, the offline `efforts` and `test` on a clone at the hash and on the branch made the branch's delta visible as numbers: 109 against 127 routing tests, 7 against 8 seats. The commits' claims could then be checked against the run's counts and each evidence folder's logs, rather than taken on trust.
- **Keyless by construction.** `COUNCIL_ENV_FILE=/nonexistent` on every `tools/council/run` call, plus `env -u` on the session's one credential-named variable, kept every process the slice started away from a key without any guard needing to fire.
- **Reading a refusal at the code that makes it.** The four `rc 1` lint verdicts looked like a finding until `lint-council-run.ts:47-66` and `council-verification.ts:340-395` were read. Linting the two 09-30 runs at their own close-out commit turned *the lint fails* into *the runs are sound and the binding is by design*.
- **Generated tables.** `stage-b/provenance.py`, `stage-b/coverage.py` and `tools/punch-items.py` write the 52-row tables and the punch list from one source each, so the counts the lint and the coordinator re-run are the counts the prose cites.

## What was harder than expected

- **Three of this slice's own readings were wrong at first,** each corrected the same session, in place, on #692:
  - the lint called inconsistent with the verifiers (it keeps a historical path for discovery);
  - F-05 called a Medium mandate after every call (the rule's adoption note already gives the fallback);
  - a leads count of thirteen, not twelve.

  Each came from reading a part before the whole: a function before its caller's comment, a rule's numbered item before its preamble, a list's length by eye. *A summary is not the source* (`engineering-practices.md`) applied to my own drafts.
- **The export's bytes are not here.** A provenance table against a SUMS whose bytes no commit holds can account for a difference only by the adaptation list, and the list's own attribution drifted once (F-04).
- **The exit-code shape a third time.** `$?` read after a command substitution in the same `echo` reported `basename`'s 0 for four failing lints. It was caught at once, because the single run before it had printed 1. The coordinator is writing the rule into `engineering-practices.md` now (P1's rule-of-three trigger).
- **Two typed times** in edits to #692 and in a log heading. Each was replaced with the command's time the same minute.

## What we discovered

- **The local Facilitator fork is the toolchain every M6 audit used this week.** All ten seat records name `1.14.1-pixelelated.2`, not the hash's `1.14.0`, and no register row records the fork (F-01).
- **Two council-run seal keys were committed** before the export's ignore line arrived. They are on `next`, in a public repository, and the push guard's patterns let them through. Raised on #692 the moment they were found; now #1043.
- **A completed run can only be linted on the tree that sealed it,** once anything is re-pinned (F-02). Nothing in the fork's record said so.
- **One of the two npm dependencies serves only a seat in no profile:** the Bedrock SDK, for the Mistral backup route (F-08).

## Adjustments, Instruction-Recommendations mode

These are proposals for the coordinator; the lane edits no rule.

1. **`council-substrate-integrity.md`:** put the adoption note's manual fallback beside rules 4 and 5, and name exits 6, 7 and 8 beside exit 3 (#1044).
2. **`IMPORTED-FROM.md`, or a register row:** the local fork and its reconciliation condition, and the expectation that a completed run is linted at its own commit (#1045).
3. **`engineering-practices.md` § Guards must fail closed:** capture `rc=$?` on the line after the command. Being written by the coordinator.
4. **For briefs that ask for a table against an export:** say up front whether the export's own bytes are reachable. If they are not, the reconciliation reads the bytes against the adaptation list, and the brief should say so.

## Scoped audit (the close-out's own checks)

- **The lint:** `tools/lint-audit-artifacts docs/audits/2026_10_25-epic-m6-tooling-council` prints `PASS` in the pre-issue and resolution phases and with `--issue 1046`.
- **The counts:**
  - the coverage table has 52 rows;
  - SUMS 41/9/2 at the hash and 36/14/2 on the branch;
  - pins 27/30;
  - members against the hash: the two commits' ten files; since the dispatch tip: none (`stage-f/counts.txt`).
- **The review plan** is local, `reviewers: []`, with no provenance file in `second-opinions/`.
- **#1046:** 15 items, each at a Phase 7 outcome named by number: 13 Deferred to #1043, #1044 and #1045, and 2 recorded as designs. `box-check` 0 fail.
- **The runs on both trees at stage F** equal stage A's (`stage-f/runs.txt`).
- **What never ran:** no `tools/council/run invoke`, no `--refresh`, no credential file read, no guest, no build, and no write under `/tmp`, `/workspace/repos/rocknix*` or the scaffold checkout (`00`).
