# T46 punch list — one Low documentary item resolved

Current outcome recorded 2026-11-03T13:28:54.671752+00:00: PL-001 Resolved in `45d455adccb0b2fc418f6442c4ca16a983430617`. The following finding account preserves D’s historical Open state; the existing machine index and first canonical Phase7 row below now record the later resolution. Both owning issues remain open for root acceptance/integration.

## PL-001 — Current audit README names the obsolete rule key

Severity: Low. Category: Documentation Gap. Source finding L-01. Question Q2 (also Q1/Q3/Q7). Owner area records.

At reviewed-at d707c82ab8c48b674acc1f95a9571f0cb24d226a, docs/audits/README.md:19 says the instruction files whose `applyTo` matches changed paths define the rubric. The canonical .claude/rules/instruction-files.md:9,27,37–47 defines `paths:` plus the no-key/every-session behavior. The surrounding README is current instructions, not a preserved command example.

Consequence: an auditor following the literal key can select the wrong instructions or omit applicable ones. Self-refutation: the canonical guide remains reachable, limiting severity; historical #314 methodology explains provenance but does not govern current rules. T39’s retained46 outcome routes and bounded issue searches assign no existing correction for this key. Source unchanged; no Phase7 outcome chosen.

Already written: documentation has not written device/cloud state; no user-data migration is implicated. Historical receipts and author identities must remain byte-exact.

Can this be done on the VM? Documentary source comparison and current rule checks need no runtime; no device fact or guest behavior is claimed.

Acceptance: a separately authorized current-doc correction names the actual `paths:` convention and every-session behavior, with a bounded source trace and rules/record checks showing the wording agrees with instruction-files.md. Exact changed-path evidence must show historical receipts untouched. Root owns that stream disposition; this audit does not apply the correction.

Evidence: 02-forward-audit.md L-01, stage-b/table.json finding_trace, stage-b/read-00/stdout, stage-b/inherited-and-duplicates.json. Reactive issue assigned in Stage D summary/readback.

## Machine index

```yaml
punch_index:
  - id: PL-001
    severity: Low
    category: Documentation Gap
    source_finding: L-01
    question: Q2
    owner_area: records
    where: docs/audits/README.md:19
    acceptance: Current instruction names paths and every-session behavior with bounded source and rule-check evidence; historical receipts unchanged.
    outcome: resolved
    fix_commit: 45d455adccb0b2fc418f6442c4ca16a983430617
    proof_class: tree
    evidence: stage-e/disposition.md
```

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Resolved | Current documentary correction in `45d455adccb0b2fc418f6442c4ca16a983430617`; exact813-byte README and new red/green proof, stage-e/disposition.md. Root acceptance/integration pending. |

## Stage D tracker links

Audit [#1417](https://github.com/pixelelated/distribution/issues/1417), actual child of #693 in M6. Reactive Low bug [#1416](https://github.com/pixelelated/distribution/issues/1416), no parent/milestone. Both remain open; no Phase7 outcome selected. Exact linkage/body readbacks: stage-d/tracker/.

## F outcome evidence

Resolved for the current documentary correction in S1 `45d455adccb0b2fc418f6442c4ca16a983430617`, after its actual normal commit. Authority: #693 comment6604790499 / immutable2aea545afb746ab002e755cf301f4aa89930e1e9 stream v2. Only docs/audits/README.md’s final paragraph changed:666→813 bytes, after SHA256410e4432c01a38cda578a68fdaa730129c15a8e3e60c7305001bb40bd5a71b6c. It names paths, no-key/every-session and wildcard behavior, links the existing canonical guide and cites #1416.

PROOF tree: exact current README and unchanged prefix/canonical target; stage-e/source-candidate-pass/receipt.json.
PROOF fixture: new old-source desired-wording refusal, then candidate positive; stage-e/source-before-refusal/receipt.json. New guard v2 has13 refusals and1 positive, including the3 index-only cases; stage-e/scope-proof-summary.json. Original failed guard v1 stays retained and is not counted as isolated proof.
PROOF tool-run: stage-e/gates-s1/ binds current04/05/Local plan/source/checker snapshots. Rules/register/index/ceremony/pre-issue/checkbox/scope checks exited0; ceremony’s nonblocking warning remains. New F resolution runs follow with current inputs.

Already written: documentary guidance and historical audit records exist; no device/cloud state or migration affected. Source cutoff d707c82 and execution seed8710 remain separate from D and S1. The305 frozen D artifacts/17 tools/29 transports remain exact, including their failures and incomplete historical bindings. Historical Open at D remains true; this is a dated later outcome.

Audit1417 and bug1416 remain open for root acceptance/integration; their criteria are checked only against committed evidence. The18 #693 criteria stay root-owned. No marker, closure, merge, cleanup, accepted replay or runtime action.

## G/H completion record — 2026-11-03T13:36:37.199371+00:00

G retro6605203841 has exact body readback SHA25625105181b4ee0944212bd32d68800d10747ad0d72ff07e0c8ecfd682d05cafef. H retained the two named D roots and new tiny-fixture root; current ordinary-file counts3/38/783 and bytes7447/29410/479141, one synthetic symlink not followed. No deletion/global census; publication packets retained separately. Stage-h/handback.md names complete current result, qualifications and next owner. Both resolution forms and checked/open tracker readbacks passed at F; final-current gates and exact final publication observation have their own later receipts. PL-001 remains Resolved documentary correction;1417/1416 open,693 criteria unchanged. Root acceptance/integration/marker/closure remain pending.
