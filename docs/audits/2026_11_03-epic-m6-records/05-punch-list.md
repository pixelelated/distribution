# T46 punch list — one Low item, disposition pending

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
    outcome: open
```

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Open | Stage D finding only; awaiting root stream disposition. No correction, deferral or withdrawal selected. |

## Stage D tracker links

Audit [#1417](https://github.com/pixelelated/distribution/issues/1417), actual child of #693 in M6. Reactive Low bug [#1416](https://github.com/pixelelated/distribution/issues/1416), no parent/milestone. Both remain open; no Phase7 outcome selected. Exact linkage/body readbacks: stage-d/tracker/.
