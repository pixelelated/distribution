# T41 final acceptance evidence — 2026-11-02

Coordinator reader/executor: Codex / GPT-6-Astra / xhigh, observed footer,
session `01a19d11-f5c8-7bb0-80f3-49ad28732af2`, wN:p2. This packet supports
the coordinator's live #688 acceptance; the live comment records that action.

Accepted candidate: `e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0`.
Reviewed seed: `d7dd76665983cb87dba62397691500fcf409fafe`.
Simulated coordinator: `afdec2bf8b88135befcb7ec56efb3a7ea327bd73`.
The simulation does not merge the lane into the coordinator or `next`.

The new full final run started 20:23:50 UTC and ended 20:29:27 UTC:
**53 PASS, one FAIL, rc1**, no CANNOT or ABSENT. The failure was an actual
reader defect: an anywhere-substring search mistook the issue's prose saying
“no `fixed-at-es:`” for an ES header. That result remains unchanged.
T2 corrected exactly one guard line, anchoring actual ES field lines, with
28 passing pure positive/refusal controls. The coordinator verified the
one-line-only source difference and executed only the corrected live
`issue-body` predicate: **PASS**, with the live title/body unchanged from
the full run. The other 53 predicates and their evidence are unchanged.
This is reconciliation of one corrected gate, not a claim of a second full
54-PASS run. No source/application/generator producer was replayed.

The original runner SHA256 is
`df37931df0fda970728af49698f189f17b263a7d5515af732f6041fdcd6efe9f`;
the corrected runner is
`c77152190c8fbd0b9660b30702a9c9ca84c4a339e0eed95909220f0aa745da09`.
See `t41-final-runner/root-final-run/manifest.json`, the exact verdicts and
driver result, and `t41-final-runner/issue-body-live/result.json`.
The JSONL packet preserves all **4,892** command JSON receipts and their
masked stdout/stderr bytes, including original hashes and actual exits;
its SHA256 is `29939223f31ed84605de318069f8820e040215bbf9cc3dcf2122925a47f7548b`.
The retention script verifies every masked output hash. Author and actual
executor are distinct fields. No completion receipt was pre-filled.

## Criterion mapping

Numbers are the 28 current #688 criteria. Section names refer to the
retained verdicts; immutable audit inputs are at the candidate above.

| Criterion | Verified evidence |
| --- | --- |
| 1 | `folder`, `handback`: required audit files/stages/tools, no guest-cycle |
| 2 | `lint`, `analysis-face`: new default and issue resolution PASS |
| 3 | `review-plan-local`, `no-compile`: actual OpenAI reader, Local, no external reviewers |
| 4 | `punch-list`, `audit-boxes`: PL-001 Deferred to open #1408; coordinator closes #1409 in the acceptance transaction |
| 5 | corrected `issue-body`, `product-paths`, `patch-untouched`: exact headers, source protection and exact two D228 fixtures |
| 6 | `membership`, `scope-record`, `tree-counts`: accepted source/output identities, 107/40,474/40,473 |
| 7 | `lint-proof`: historical T4 capability positive/negative identities reconciled |
| 8 | `tables`, `generated`, `non-kernel`: 107 provenance rows, five non-kernel owners |
| 9 | `tables`, `membership`: 107 exact coverage keys and escaped filename normalization |
| 10 | `runs`, `applies-record`: 120/106, normal authority, prefix failure guard, H700-011 dry1/apply0 |
| 11 | `checker-run`, `checker-record`: historical receipt reconciliation plus sealed new D228 input proof; old input identities remain unavailable |
| 12 | `record-lines`, `fork-written`: ramoops node/config numbers and unsent distribution-layer draft |
| 13 | `record-lines`, `fork-written`: quoted-regex comparison and both never-sent lines |
| 14 | `fixes-record`, `bug-bodies`, `bug-boxes`: exact 0010 source defect, upstream trace, open High #1408 |
| 15 | `record-lines`, `analysis`: conf comparisons and static method, no config execution |
| 16 | `upstream-status`: 101/4/2 identity summary and inherited integration additions/move |
| 17 | `pins-read`, `record-lines`, `headers`, `tarball-hashes`, `device-groups`: corrected literal quotations and retained command output/exit evidence |
| 18 | `read-order`, `rulings`: 31 leads and a–p routing |
| 19 | `analysis-face`, `analysis`: Q1–Q7, currency counts, time-to-play limits |
| 20 | `question-comments`: both complete posted questions read back |
| 21 | `inherited-record`: T27/T11/T43/integration/coordinator ownership, firmware T11 |
| 22 | `ladder`, `bug-bodies`, `bug-boxes`: trace, Already written, VM rationale, next mechanisms |
| 23 | `proof-lines`, `proved`: classified proof/PROOF equality |
| 24 | `no-compile`: retained lane host census, zero lane matches; no fresh host-file inspection for acceptance |
| 25 | `running-log`, `no-compile`, `scratch-retired`: command census and retired owned source directory |
| 26 | `retro`, `last-comments`: final posted retro and unchanged time-to-play |
| 27 | `checkers`, `merge`, `forbidden`, `secret`, `lint`: new lane and disposable integration gates |
| 28 | `pointer`, `dist-tip`, `handback`, `lane-boxes`: one published candidate, complete checkpoint and zero issue-check failures |

Both lane and simulated integration returned rc0 for rules, register,
work-log index, ceremony, hooks and full-tree forbidden checks; both default
and issue resolution lints returned PASS/0. Full-tree scans reported zero
hits over 134,448 lane and 134,728 integrated paths. Positive/refusal outputs
retain their expected nonzero exits. The merge initially conflicted in the
shared log; the strict append resolver preserved all three coordinator and
ten lane entries byte-for-byte, then regenerated the index. Its merged-log
SHA256 is `06049d878ced96160ddce89d6e28470ce62b2167c5059bb31c27588b179d2f23`.

Full whitespace checks returned **rc2**, confined to the exact four accepted
A-stage records and two D228 header fixtures previously specified in the
contract. Each mode/blob/hash matched; all other paths returned rc0.
`whitespace-{cached,tips}.json` retains the six identities and diagnostics.
Historical whitespace was neither normalized nor represented as a full rc0.

## Outcome and completion boundary

T41 is a completed source-provenance audit with one **Deferred, unfixed High**
finding. #1408 remains open with both source-fix criteria unchecked, owned by
base integration #563/#559. Closing audit #1409 records that disposition;
it does not fix or waive the defect. T11 retains the duplicate-storage choice.
D-SYS-004 and the two never-sent #585 drafts remain unchanged.

After live acceptance, the existing T3 lane may write only its normal
completion marker, closed-audit readback, pointer and log, run new record
checks, commit/push normally, and return one clean records-only tip. No
source change, accepted execution replay, new integration merge or runtime.
#688's accepted source headers remain seed/e481 and the issue stays open
until the area's ordered actual integration. All historical model identities
and the original failed final-run result remain intact.
