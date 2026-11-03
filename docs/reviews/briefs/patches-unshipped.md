# T43 — patches and configurations classified unshipped (#690)

Version 2, coordinator brief, 2026-11-02. The bounded stranger proof and
its manifest-citation correction are retained below. Execution starts only
from the explicit live dispatch naming the published seed and worktree.
T43 follows T42 in the milestone order; preparation may run in parallel.

## 1. Identity

M6.P2, area epic #1054, slice #690, canonical ID `patches-unshipped`.
Kind table, lens reachability; Local depth under D-WORKFLOW-184 and plan
§6c. One actual primary reader, reviewers `[]`, no provider/council call.
Intended executor: existing T1 `m6-t1-os-launch`, wN:p4, Codex /
GPT-6-Astra / xhigh, session `01a19d12-0c07-7ba3-88b8-ab9d609f4d67`.
Record the executor's observed identity at start; preserve historical T39
provenance. T39 is complete and is not reopened.

Branch `feature/m6-patches-unshipped-690`, worktree
`/workspace/repos/pixelelated/distribution.worktrees/m6-patches-unshipped-690`.
The coordinator creates it after proof from the published dispatch commit;
the live dispatch supplies the full seed. It does not exist by implication
of this candidate. Always use that absolute workdir, never the pane's
historical launch tree. No ES tree is required.

Source baseline `afdec2bf8b88135befcb7ec56efb3a7ea327bd73`; P1
`2174265e9cc1b248c0fbe27fa101875984d46d6b`; fixed upstream comparison
`651150fc88` (resolve its full local object once and retain it); fork base
`c445081a59518f37d9776e5412dd7b14910696f7`. No fetch or moving-ref comparison.
The seed must preserve selected sources, selectors, referents and the31
source recipes. Unexpected identity drift returns to the coordinator;
the executor never silently recuts ownership.

## 2. Scope and runnable membership

Own exactly **432 path rows / 328,516 logical Git-blob lines**, all
vendor-carried, all classified `unshipped`, none `n/a`. The inventory is a
fixed survey snapshot, not a newly executed build graph. There are
328,512 newline bytes and10,690,267 literal blob bytes. Counts comprise
346 Linux-source patches/222,494 lines,12 configurations/101,229 lines,
and74 other-source patches/4,793 lines. The latter include nine
mali-bifrost module patches; package boundaries differ from kernel relevance.

420 patch-suffixed paths are418 regular patches and two symlinks. Total
modes:428×100644,2×100755,2×120000. Preserve the two executable modes;
never execute those patch files. `tier_note` has **zero fork-written
members**, and the selected net diff against the fork base is empty.
This is a verified inventory/base-delta set, not a claim to have established
every upstream author's identity. No328,516-line code review is claimed.
The125,129-line RK3588 Mali patch remains one vendor-carried table member.

Path-list SHA256:
`8ec78172f80d28d28117eaf1efefe2c769ea58d07a57c3a16616b595fb429912`.
The retained `t43-preparation/members.tsv` has 83,282 stored bytes, SHA256
`d89d6fe612587635c2bb6d1101362242f03b9f0c3c391015f5344c2357eb1c49`.
It contains exactly one literal `\u002d` path escape. For path comparison
only, decode that single escape to a hyphen: the resulting 83,277 bytes
have SHA256 `ccbbe1543349e51f56545afc3e96aadc3fc3e965e19b1fdb18731ee809cc083e`.
Preserve the historical stored file; never confuse its hash with the
decoded comparison identity or alter source names to match escaped text.
There are72 containing directories,31 prefix groups and28 overlapping
buildable-by combinations over21 target/architecture configurations.
Per-consumer totals overlap; do not sum them as membership.

Physical target directories contain377 paths/324,591 lines:
AMD64 4/12,529; RK3326 25/27,895; RK3399 10/7,604; RK3566 41/11,164;
RK3576 24/15,132; RK3588 18/143,156; S922X 46/17,004;
SM4450 45/16,993; SM6115 47/15,427; SM8250 37/19,034;
SM8650 21/12,407; SM8750 59/26,246.
Another55 paths/3,925 lines are in19 project-package prefixes. These are
directory groups, not final image coverage. All members are under
`projects/ROCKNIX/`.

The two MangoHud SM8650 link rows reach SM8750 member referents of34 and37
lines. T42 separately owns the SM8550 battery link to that same37-line
T43 referent. Thus **unshipped describes path classification, not absence
of a shipped consumer of its bytes**. Preserve link mode, literal target,
referent mode/blob/hash and consumer ownership separately. T40/T41/T42
membership intersections are empty. Shared patches used by unshipped
targets may belong to those other tables; read necessary siblings as
context only. T11 owns GENERIC_X64's conf, T27 H700's, T41 SM8550's.
T42's50 inherited comparisons never become T43 members.

Run this block from the proof clone or dispatched repository:

```bash
set -eu
export LC_ALL=C
SOURCE_REF=afdec2bf8b88135befcb7ec56efb3a7ea327bd73
INPUT_HELPER=docs/qa-logs/2026-11-02-m6-resume/t43-brief-inputs.py
INPUT_OUT=$(mktemp -d /tmp/m6-t43-inputs.XXXXXX)
python3 "$INPUT_HELPER" --repo "$PWD" --ref "$SOURCE_REF" --out "$INPUT_OUT/source"
python3 "$INPUT_HELPER" --repo "$PWD" --ref HEAD --out "$INPUT_OUT/seed"
```

The helper uses immutable Git reads and five inspected pure P1 selector
functions, never the inventory CLI or config evaluation. It writes only
small text/JSON inputs. The two summaries must match apart from `ref`;
tree/row/path/link outputs match byte-for-byte. Expected432/328516/328512,
10,690,267 bytes,430 regular/two links,zero fork-written,reach432 unshipped.
It binds six survey/selector files and all31 direct source recipe identities
to P1. Save actual argv, times, exits, raw output and helper hash in A.
The proof checks the candidate; execution checks the actual seed.

## 3. Read first and research sequence

Read the complete live #690 thread, #1054, current M6 order, plan §§4–8,
this brief and the current coordinator rules. This branch is newer than
next; no refresh merge merely to read rules. Applicable rules include
engineering-practices, packaging-and-patches, worktrees, issue-tracking,
adversarial-council, decision-register, ceremonies, upgrade-and-install,
vm-first and handheld-evidence. Read code-auditor's Local methodology and
evidence floor; record actual OpenAI identity rather than an old default.
Blindspots13/47/51/75 are relevant: evidence versus claims, source pin
versus installed behavior, already-completed work, and wrong-tree counts.

Settled D-WORKFLOW-184/185/187/188/189 govern depth, shipped set, no release
gate, order and coordinator ownership. D-WORKFLOW-209 prohibits removals;
D-WORKFLOW-231 owns this table; D-WORKFLOW-221/222/225 settle
neighboring ownership and normal-application
authority. RK3326/RK3566 remain the held first widening, not shipped now.
Do not reopen the class-removal choice (#1048/#346) or send a #585 draft.

Planning facts are in
`docs/qa-logs/2026-11-02-m6-resume/t43-preparation/`:
report.md, members.tsv, results.json, recipes.json and context-inputs.json.
Historical scripts name their original private paths; use committed inputs.
Write this slice's first header/target/reach observations before reading
prior audit verdicts. Then compare the named immutable contexts, never
rerun their producers:

| Context | Immutable accepted source and owner |
| --- | --- |
| T25 | `9b9be6a9481e4e9ee5b9d97f6c7bb72eda3ca3b4`, devices-unshipped02; #672; unpack edges #1101, RK3576 cellwise match, SM8750 hostname lead |
| T11 | `47672fe4a04fc3b69dee9f0381fbc9f076b891e5`, device-generic-x64-and-kernel02; #658; kernel/config/firmware ownership, historical built-config findings |
| T27 | `0ac98afe434c0429bace5f239482e5de0e0bc394`, device-h70002; #674; source/config ownership and ATF URL/hash pairing |
| T41 | `e481e4a4a5c296c8f12e9654b6a45c4fb27bd3b0`, patches-shipped-kernel02; #688; accepted107 rows/120 normal applications, inherited unshipped additions/move, no T43 application claim |
| T42 | `4cf8c8820791624dbddad3eb3664101a03953a82`, patches-shipped02; #689; native384 separate from inherited50, shared MangoHud referent, source/open-input qualifications |

The preparation report gives full audit paths and specific lines. Existing
T8 #655, T30 #677 and T23 #670 own other source recipes. The31 direct
recipes map to T25 12/25, T8 10/36, T30 3/3, T23 5/10, T11 1/358
(recipes/member rows). Do not edit these recipes or manufacture new owners.

Read `scripts/unpack`, `config/functions`, actual recipe resolution and
patch-directory selectors statically. Inventory reach identifies selected
directories; it does not prove application or non-use. `PATCH_ARCH=x86`
for x86_64 is distinct from literal arch naming. Context worth answering:

- Kernel source pins at the source baseline:7.1.2 AMD64/RK3326;
  6.18.49 RK3399/S922X;7.0.2 RK3566/RK3576; vendor commit
  b8e62bed74766b6c8c423a767b35495e78b64caf RK3588;7.2 Qualcomm.
  RK3588 resets patch directories; do not add mainline-rockchip blindly.
- RK3566 loader Generic/Specific source recipes pin v2026.01. Their
  source-free wrapper's1.0 is not the source pin.
- mali-bifrost module source39da994bb6fc8819e5e8c1873907dd21d17e53c1;
  libmali's default/next pins and wlroots0.19.3-rk are conditional.
  RK3399 ATF uses2.10.0, not H7002.12.0. Keep URL/hash pairs together.
- The12 conf headers describe source inputs, not final built .config.
  Static recipe writers include hostname and forced/disabled symbols.
  SM8750's literal hostname is an inherited source lead, not a proven
  installed defect. Never run oldconfig or either config-writing helper.
- At fixed upstream651150fc88,7.2.6 is a patch-directory selector while
  RK3566/RK3576/S922X source is7.2.11; RK3399 is6.18.54. These are
  comparison facts, not silent new source pins. Integration #563/#559 owns
  additions, moves and source uptake, including the polldev move to RK3326.

## 4. Questions and required tables

Q1 modernization: target interfaces and carried replacements visible in
source. Q2 standards: header/origin/backport/license claims and consistency,
without inventing authorship from a filename. Q3 defects: exact source
trace, consequence and refutation; application success is not correctness.
Q4 currency: fixed-base/upstream comparison, actual selected source pin and
specific absorbed/moved/changed evidence. Q5 efficiency: source-visible
cost implications and missing runtime measurements; no boot/memory/player
latency PASS. Q6 reachability: selected consumers, shared referents and
known inventory limitations; no removal proposal. Q7 clarity/structure:
ambiguous provenance, duplication, carrying reasons and exact next owners.
Both interface→first-frame and exit→next-first-frame remain unmeasured.

02 contains **Provenance** and **Coverage**, each with432 unique native
keys. Provenance columns: path, kind, mode/link/referent, inventory lines,
recorded consumers, source recipe/owner/full pin per plan, selected stack,
origin/header evidence, target summary, application/config evidence and
limits, fixed-upstream identity/status, backport status, carrying reason,
disposition, next owner/action and receipt links. Coverage states what was
actually read; do not claim line-by-line reading of vendor bodies.
No empty cells: unknown/open-item requires the precise missing evidence.

Disposition vocabulary: keep, upstream-changed, upstream-moved,
superseded-at-pin, inherited, bug, contribution-draft, open-item.
Every non-keep row names evidence and an owner. No counterpart or unused
directory alone proves obsolescence. One row per path remains even when
several share a recipe/target. Configuration rows never use patch-apply
status. A12-row configuration table records header, source/recipe pin,
base/upstream differences, selected config path, static writers and the
missing built-config/runtime evidence. A31-row recipe-context table and
two-link table retain identity/pin/ownership seams. Record the zero
fork-written set explicitly; no fabricated contribution is required.

## 5. Evidence floor and permitted source checks

Can this be done on the VM? Provenance, selection and source application
are immutable-source facts; no runtime behavior is tested here. No guest,
build, compiler, device, cloud, provider or host allocation is requested.
The separate M7 window does not grant this lane any runtime.

Git comparisons and static recipe/selector reads establish the table.
For a positive patch-application claim, establish exact selected source,
recipe URL/hash, safe archive identity, pre-patch transformations, context
stack/order, architecture and feature values. Use only already-cached
archives under `/workspace/cache/rocknix-sources/`; no filename-based trust.
Missing archives/hashes/hooks, ambiguous members or unresolvable selectors
remain explicit open inputs with their owner. Linking a URL does not mean
it was read. No web/provider verification is assigned.

Only necessary safe archive members may be projected under
`/workspace/tmp/m6-t43/`, never a repository or /tmp. Reject absolute,
parent-traversal and escaping link paths; account for patch-created files.
No wholesale extraction or source export. The tiny /tmp helper output is
text/JSON only. Record a source-only package/plan census before each group.
Read any pre_patch/post_unpack transformation and establish its exact
input statically; never execute a recipe/config or `scripts/unpack`.

Use the actual build backend and render its substitutions from proved
TARGET_CPU/DEVICE values. Retain literal/rendered patch identities and
selected values. D-WORKFLOW-222 makes complete normal application into a
disposable candidate authoritative; dry/check is diagnostic on an equivalent
successful prefix. Promote only normalrc0, retaining argv/version/locale/
times/exits/stdout/stderr hashes and input/output/stack digests. Failed
prefixes block successors without invented calls. Distinguish applies,
offset, fuzz, fails, blocked and open-item. Prove non-promotion after a
partial failure before trusting a new runner. For git-apply triggers use
the build's exact semantics and safe relative paths; unsupported inputs
stay open. No unsafe-path override is authorized.

Accepted neighboring application results can be read as context; do not
rerun their producers or transfer PASS to different T43 inputs. Application
is not a prerequisite to state a proved selection/header/identity fact;
its absence is a specific qualification, never a blanket success. No
128k-line patch application is required merely to fill time when its source
cannot be proved. Defects must distinguish constructed mechanism fixtures,
exact-pin source proof and installed effects. Existing owner findings are
inherited, not refiled as newly discovered duplicates.

Only audit-local tools/receipts, lane pointer, its timestamped log/index and
retro may change. No product patch/config/recipe/tool/script, source mode,
symlink, rule, register or survey-ledger edits; no removal, fetch, config
sourcing, build/cache copying, private-held read, host-ledger write or
another agent's permission answer. Source/record subprocesses use CPUs8–23
during M7's exclusive compiler window.

## 6. Outputs and continuous stages

Audit root `docs/audits/2026_11_02-epic-m6-patches-unshipped/`.
A writes00-running-log,01-research-notes and stage-a/ seed/input bindings,
scope counts, command exits and execution census. Prove Local-lint support
with a tiny isolated positive/negative plan fixture; no accepted audit replay.
Report A and continue on matching inputs.

B writes02-forward-audit,03-retrospective,04-analysis and stage-b/ receipts.
First observations precede comparison with prior verdicts. Answer Q1–Q7,
spec/doctrine/interaction/refutation and the tables above. No runtime claim.
C writes05-punch-list, audit-local asserted generator/checkers and stage-c/;
one second-opinions/review-plan.json with actual primary/lab/source of
identity, Local, reviewers[], D-WORKFLOW-184 and plan§6c reason. Test a
dropped member, wrong config kind, changed link/referent identity and
fabricated known header attribution: each must fail its own assertion,
then the positive432-row output passes. Bind exact fixture inputs as well
as programs/argv/outputs/exits from the outset. Pre-issue lint must print
its literal PASS pre-issue line; it does not certify resolution.

D files the audit child of690 in M6, with actual severity/count, complete
prioritized punch list, YAML index/question/ladder/next mechanism and
acceptance criteria. Actual reactive bugs have trace, Already written and
VM rationale, no milestone/parent, and no duplicated existing owner.
Write06-audit-summary,07-questions-for-the-maintainer and stage-d/readbacks.
Questions arise from actual unresolved choices; do not invent a preference
when the record already settles it. Post one clean published D checkpoint
and stop for coordinator stream disposition. A–D are continuous; successful
intermediate checkpoints are not approval gates.

After disposition, E records outcomes; F runs new resolution/final record
checks; G writes/posts `docs/retros/<date>-m6-patches-unshipped.md`; H retires
only receipt-bound owned projections and returns one clean published tip.
Never delete caches or another owner's data. Preserve ordinary external
final commit/push/remote/status receipts bound to the handback commit;
no receipt-only commit loop. Completion marker/audit closure await root's
explicit final acceptance. No new coordinator merge into the lane unless
explicitly dispatched; root simulates integration separately.

## 7. Acceptance criteria

The coordinator installs these in live690 before dispatch.

1. 00–07, A–D receipts/tools and the one-file Local review-plan exist; no guest-cycle/build artifact.
2. Exact432 keys/328,516 logical lines, line/mode/link distinctions, zero fork-written and seed/source/P1 identity bindings verify with the helper.
3. Provenance and coverage each contain all432 unique keys and nonempty evidence/owner fields, with no invented whole-body reading.
4. The346 Linux patches/12 configs/74 other patches and72/31/28 directory/prefix/consumer groups reconcile without summing overlapping reach.
5. Both links and referents, executable modes and T42's separate shipped consumer retain exact identities/ownership; all neighboring membership intersections are empty.
6. All31 recipe contexts bind their actual conditional pins and existing owners; wrapper/source and module/kernel distinctions are correct.
7. The12 config rows separate source headers/static writers from built config/runtime; no config tool was executed.
8. Base and fixed651150fc88 currency statuses have exact source evidence; selector7.2.6 is not mislabeled source7.2.11, and integration owns moves/additions.
9. Every positive application has exact source/preimage/rendering/backend/stack/normal-result evidence; missing inputs remain specific open items. Partial-failure control refuses promotion and blocks successors.
10. All four table-generator negatives fail before its positive432-row output; program/input/output hashes and command exits are retained.
11. 03/04 cover conformance, doctrine, interactions/refutation and Q1–Q7, with classified proof/PROOF agreement and explicit unmeasured efficiency/time-to-play.
12. Actual primary/lab/identity source and historical identities are honest; Local reviewers[]/D-WORKFLOW-184, with no external-review claim.
13. Pre-issue lint and final normal/issue resolution lint print the appropriate PASS; each punch item reaches a recorded Phase-7 outcome with evidence/owner.
14. Bugs have trace, Already written, VM rationale and observable criteria; issue checks return0fail; unresolved bugs remain open.
15. Tree and per-commit guards protect all source/context/selector/rule/register paths and reject a planted source edit; no product or removal change.
16. Inherited and contribution rows retain exact owners/actions; #585 drafts remain unsent and class removal stays #1048/#346.
17. Closing census records no forbidden execution/allocation; owned source projections retire only after receipt custody is proved, caches preserved with the actual evidence strength stated.
18. Current rules/register/index/ceremony/forbidden/hooks and issue checks pass with real exits; final publication receipts bind the clean final tip.
19. Final posted retro and handback name one clean published tip, actual outcomes/friction/next owners and both untouched time-to-play quantities.
20. Live reviewed-at/fixed-at bind seed/final; root verifies integration and acceptance. Audit completion marker follows explicit acceptance; slice closure/status waits for actual ordered integration.

## 8. Stops and delivery

Stop for immutable-input mismatch, a failed required predicate without an
authorized correction, an out-of-scope action, explicit owner pause, or the
published D/authorized final-H boundary. Report a concrete blocker early;
missing optional source inputs are honest open rows. Continue useful
authorized work rather than waiting at each successful stage. No execution
starts from this candidate before the explicit coordinator dispatch.

## 9. Ceremonies and custody

Coordinator owns brief/criteria/ownership/register/milestone/acceptance.
Lane owns its single worktree and audit records. Append a timestamped log,
regenerate INDEX, capture friction when observed, retain whole historical
entries and record actual identity. Run required record checks and normal
hooks; use Refs #690, never an automatic-closing keyword for partial work.
New raw inputs and producer exits belong to their producer, never pre-fill
them. No source change follows from an audit finding without its own brief.

## 10. Coordinator handback read

Read actual tables/receipts/identities/outcomes against live criteria,
including specific qualifications and publication custody. Reuse accepted
A–D evidence by immutable identity reconciliation. Run only new final
records/integration gates or a concrete changed predicate; no blanket
producer replay. Simulate the exact lane/coordinator merge in disposable
scratch, preserve whole log entries and regenerate INDEX. Record original
failures and any narrow correction separately. Close the audit only after
all outcomes and final criteria verify; bugs/area integration retain their
own remaining obligations.


## Version 2 corrections from the stranger proof

T2, a separate existing lane (wN:p5), ran the literal membership block in
one shell invocation from private Git state, reconciled all stated source
figures and recipe/selector interfaces, and retained 49 failing drift
controls. The coordinator independently reproduced the immutable metadata
reader byte-for-byte. This is handoff proof, not application/audit acceptance.

One correction: §2 previously labeled the decoded manifest SHA256 as the
stored file hash. Both identities, lengths and the single-escape comparison
are now explicit. Neither the historical manifest nor any source changed.
Original literal-hash/raw-key failures remain in the proof packet, together
with the normalization proof. No helper or execution method changed.

Evidence: `docs/qa-logs/2026-11-02-m6-resume/t43-brief-proof/RETURN.md`,
`manifest-normalization.json`, `coordinator-verification.json` and the
lossless `proof-records.jsonl` (196 source/receipt files; private Git object
store excluded). Header/version/ownership wording now records dispatch
readiness; the source population and 20 criteria remain the proved contract.

## Final acceptance errata — 2026-11-02

Root final assessment accepts8282cbcade3be32b437f7391be7e216d9a6b1074 within the existing source-only contract. D evidence is reused without producer replay; new final records and disposable integration against749e5c7f2df2c8444b07f8521493d12b7f7a962b pass. The exact20-criterion map and raw checks are under docs/qa-logs/2026-11-02-m6-resume/t43-final/.

PL-001 resolves custody only; all93source-input gaps remain open, with224consumers188open/36positive. H records881retired/eightretained/zero partial after the committed plan. Four empty prefixes used nonrecursive rmdir; cache preservation is metadata-only and inaccessiblePID2389 prevents any all-same-UID clean claim. No further cleanup follows automatically.

Four early F controls bind an older final-confinement.py hash45612b79. Removing the one later retirement-owner-scope.py allowlist entry reconstructs that exact hash; the reconstructed copy is labelled derived, not recovered historical evidence. Final receipts bind currentb7ee4e57; earlier controls are not relabeled as final-code tests.

The root log resolver originally rejected time-only seconds and one exact historical heading without UTC/dash. New audit-local resolution validates seconds and accepts only that whole legacy entry's pinned hash, preserving all bytes and each branch's entry order. The first conflict fixture changed the heading and therefore correctly represented two distinct entries; its failed expectation remains retained. A corrected same-heading/body-conflict fixture refuses, all six new controls pass, logs/INDEX reconcile and remaining integrated gates pass. Shared historical helpers are unchanged. No actual area merge or accepted-stage replay occurred.

All20criteria are accepted with these scoped evidentiary meanings, not as source correctness or runtime proof. Audit closure/completion marker follow explicit live acceptance; #690 stays open until actual ordered area integration.
