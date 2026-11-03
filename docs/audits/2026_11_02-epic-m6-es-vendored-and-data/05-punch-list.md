# T44 punch list — D checkpoint

One Low currency/documentation item; no Critical, High or Medium item and no new reactive bug. Root retains stream disposition and planning. This opening description records the accepted D checkpoint. The current E/S1 documentary outcome follows below.

## PL-001: Record the doctest carry-or-update decision against the observed release

- **Severity:** Low
- **Category:** Documentation Gap
- **Question:** Q4
- **Source Finding:** T44-CUR-01
- **Owner area:** #700 coordinator disposition; T18 and existing test owners for any later executable compatibility proof. T44 supplies this provenance decision input only.
- **What:** The exact unchanged doctest2.4.12 import is now compared with the primary release page showing2.5.3 on2026-11-02. The import explains its then-current2.4 choice but the named accepted records supply no current carry/update decision for2.5.3.
- **Where:** external/doctest/doctest.h:7-51 at ES55158d2a6; import324f9c483d9b4a11249c47888b40fb5cc691be7f; stage-b/history.json and vendor-groups.json.
- **proved:** tree/history/design
- **PROOF:** Unchanged header SHA25694029a7d32da24a56249658147dbd2b33ff0b9ed665295cbbaf19aafff5b0ced; https://github.com/doctest/doctest/releases/tag/v2.5.3 (dated read; displayed date year not inferred).
- **Already written:** Existing #649/#681/#682 accepted test records mention doctest and allowed failures, not a prospective2.5.3 decision. Narrow live issue searches for doctest/release references returned accepted owner issues; this is not an exhaustive global absence claim. No existing behavior finding is refiled and no reactive bug is opened.
- **Consequence/refutation:** A future updater lacks a current rationale/retirement condition. Newer release alone proves neither incompatibility nor security harm. A justified retain decision may be correct; existing test results must retain their original pins and allowed failures.
- **Can this be done on the VM?** No runtime is required to decide/document carrying policy. A later update's compatibility proof belongs to a separately dispatched owner and GENERIC_X64/its authorized pure tests. No such run is proposed here.
- **Ladder:** source/history and dated primary metadata; no executable compatibility or installed-image rung claimed.
- **Next mechanism:** Root records a scoped carry decision with rationale and revisit trigger, or creates a follow-up brief naming exact update target, consumers, negative controls and source/permission boundaries. No update is selected by this item.
- **Acceptance:** The Phase7 outcome cites the coordinator's exact decision/comment or a numbered follow-up, identifies2.4.12/observed2.5.3 and all affected test owners, and states the rationale plus revisit trigger or the bounded next brief. No accepted receipt is replayed or rewritten.

## Pre-existing tracked scope (NOT punch items — exempt from Phase 7 gate)

- T20 #667 R13→T44 #691: rcheevos12.2.1/10.7.0 dual markers, 02:183 at the exact T20 ref in stage-b/prior-record-identities.json. Current12.5.0 metadata does not settle import mapping or applicability. Root retains disposition; excluded hash/RVZ source changes and three-hasher obligations stay T20. No duplicate bug.
- T2 #649 PL-024/025 resolved: exact shared key and French3; companion additions6/1/1/0 remain #700's integration obligation.
- T18 #665 root AsyncNotification fake behavior; T35 #682 core CMake and T21 #668 five-registration integration debt; T36 #683 core zip_file/han and #256 vendored-header bucket; T37 #684 recipe/installed context. No owner transfer.
- libretro-common/NanoSVG exact upstream mapping and id3v2lib current revision are explicit missing currency inputs in the group table, not inferred bugs. Retain until root defines any further scope.

## Phase 7 resolution gate

| Item | Outcome | Evidence / next owner |
| --- | --- | --- |
| PL-001 | Resolved | Carrying-decision documentation only; #691 comment6591582676, #1414 five-group follow-up, stage-e/disposition.md; source and compatibility work remain separately owned |

## Machine-readable index

```yaml
punch_index:
- id: PL-001
  severity: Low
  category: Documentation Gap
  question: Q4
  source_finding: T44-CUR-01
  owner_area: interface; coordinator #700 with T18 and existing harness owners
  where: external/doctest/doctest.h:7-51 at 55158d2a64c69fe295fb4e67fd174424a71b1b4d
  ladder: source/history and dated primary metadata; compatibility and installed proof absent
  next_mechanism: coordinator carry decision with revisit trigger or separately scoped update brief
  acceptance: exact dated decision or numbered follow-up binds versions, rationale, trigger and owners without accepted replay
  outcome: resolved
```

## E/S1 current outcome — 2026-11-03

PL-001 is Resolved for the carrying-decision documentation only. [stage-e/disposition.md](stage-e/disposition.md) records the exact carry decision, rationale, trigger, owner links and preserved D qualifications. #1413 stays open for root acceptance. #1414 remains open, five criteria unchecked. The historical D finding above remains the reason this decision was required; it is not a source defect closure.
