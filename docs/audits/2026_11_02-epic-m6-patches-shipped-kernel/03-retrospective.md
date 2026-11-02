# Retrospective audit — M6 T41 (#688)

**Recorded:** 2026-11-02 17:37:15 UTC. **Reader:** Codex / GPT-6-Astra / xhigh, same observed-footer identity as 02. **Depth:** Local. **Scope:** source provenance and applicability, not release qualification.

## Architectural Assessment

The 107-row carve is coherent once its five non-kernel rows are explicit. The build engine resolves the override recipe, then ordered package/version/device patch globs; configuration selection is a separate first-existing-candidate mechanism. A successful patch application is evidence at that interface only. The pre-fix 0010 pointer defect survives in the final patched source despite successful application, demonstrating the boundary.

No code, pin, configuration or rule was changed. The audit artifacts retain the original mistaken dry-run model and its immutable refutation. The corrected engine promotes a disposable candidate only after complete success, which preserves intra-file series dependencies and prevents partial failure contaminating successors.

## Project conformance

| Face | Relevance | Finding |
| --- | --- | --- |
| Branch-owned instructions | High | M6 branch intentionally newer than next; coordinator rules and immutable method erratum used without merging next. |
| Packaging/patches | High | Header provenance and real override selection recorded; dead generic-directory sentence inherited coordinator. |
| VM-first / device boundaries | High | No guest answers source applicability; no runtime allocation or physical/cloud action occurred. |
| Engineering evidence | High | Identical-input refutation, real failed-candidate fixture and three generator mutations precede trusted status. |
| Issue tracking / ownership | High | #688 is the return route; Stage-D bug/questions not prematurely posted elsewhere. |
| Upgrade/install / preservation | Context | Product bytes untouched; no upgrade or clean-install claim is made. |
| Learning capture | High | Method disagreement became coordinator D-WORKFLOW-222 and a corrected guarded runner, with dated work-log entry. |
| Time to play | None exercised | Nothing. Neither interface-to-first-frame nor exit-to-next-first-frame changed. |

## Blindspot review

| Register entry | Recurrence challenged | Evidence |
| --- | --- | --- |
| 8, a guard passes because nothing happened | Failed candidate partly writes; prefix remains unchanged; successor is blocked | failed-candidate-guard.json |
| 14, no observed positive | Three malformed generator inputs and hygiene positives | generator-fail-first.json; validation.json |
| 47, pin mistaken for built image | Source application is explicitly not a built or booted image claim | 02 Coverage Boundary |
| 75, count from wrong tree | Immutable source/P1/seed equality, retained TSV and 120 exact indices | table assertions and validation.json |

## Project invariants

Progress is preserved in committed receipts, including the failed method. No stored player state, cloud allowlist or credential-bearing configuration was read or changed. No script was edited while its run was live. The 107 source paths are unchanged; no upgrade migration is introduced. Unknown origin remains unknown rather than inferred from filename or a heuristic rename history.

## Platform architecture conformance

| Check | Relevance | Finding |
| --- | --- | --- |
| Reference implementation / tenant zero | Not applicable | Distribution build/provenance task, no application tenancy. |
| Schema before code | Relevant | Existing 107-row carve and closed vocabularies precede table rendering; assertions reject drift. |
| Dogfooding gate | Source only | Actual cached-source commands and failed candidate exercised; no runtime claim. |
| API first | Not applicable | No new API or runtime surface. |

## Cross-System Interactions

| Interaction | Shared state / wipe risk | Coverage | Finding |
| --- | --- | --- | --- |
| unpack × inventory × recipe case × device dirs | Ordered source prefix and membership; wrong arch/glob could omit/apply a patch | TESTED at source level: C order 8/42/65; 107 carve | Safe within recorded immutable source boundary; inventory reach is not proof of compilation. |
| concatenated patch × dry-run × normal application | Later diff needs earlier same-file edits; skipping false failure changes all successor inputs | TESTED: H700 011 plus all corrected plans | Old method broken; corrected D-WORKFLOW-222 result verifies complete application. |
| partial failure × next patch | Candidate may be partially written; promoting it contaminates successors | TESTED: deliberate partial failure fixture | Failed candidate retained, prefix unchanged, successor blocked. |
| kernel recipe × configuration × DRM code | Config controls whether successfully applied code compiles | PARTIAL: CONFIG_DRM_MSM=y only SM8550; no compile | High 0010 defect survives source refutation; runtime reach not measured. |
| upstream merge × patch location × consumers | Polldev moves to RK3326; current inventory does not predict future recipe contents | PARTIAL: history/zero current consumers read | Integration and T27 own post-merge consumer verification. |
| ramoops × excluded H700 conf × boot memory | DTS reservation/config companion/physical retention | PARTIAL: source numbers and six lines; no board test | Source consistent; physical DRAM retention remains L29. |
| SM8550 config × arm userland | Nine-candidate resolver and aarch64 kernel architecture | TESTED by text resolution; runtime UNTESTED | Same config can serve both userlands; no oldconfig output claimed. |
| non-kernel carve × cache × empty extraction | All firmware target files are new; tar creates no root | TESTED: accounted missing paths, explicit empty root, complete apply rc=0 | Corrected runner handles creation-only patches. |
| generator × escaped path × secret scanner | Representation must compare to a real filename without leaking an unsafe scanner-shaped token | TESTED: normalize only comparisons/source reads; scanner positive and negative | Source filename and scanner unchanged. |

No concurrency, reload or deployment state exists in this audit. Copy/promotion operations touch only lane scratch; no original source, cache or other lane is a candidate destination.

## Spec fidelity and drift

Membership, pins and Local depth match v2. The only execution-method change is the explicit coordinator erratum, read in full at `4c8a118cfb`; it resolves the observed dry-run/complete-application disagreement. Old receipts are preserved. Pristine ramoops context appears at line 108 rather than approximately 117; current churn is 61 at the reviewed source rather than the brief's 64 at another hash. Both are recorded deltas, not hidden rewrites.

The 11 mailing-list probes are deliberately conservative: matching one common added line is not enough to call a complete patch superseded. Two positive substrings were refuted by their target contexts; the deletion-only patch still has its old check. No supersession/removal is inferred.

## Defect-class sweep (Site, Sibling, Adjacent)

| Class | Site / sibling / adjacent | Verdict | Rationale and owner |
| --- | --- | --- | --- |
| Uninitialized cstate write | 7.2/0010, 7.0/0010 | FILE-FOLLOWUP | Same pre-fix bytes; upstream 9416eec2c2 fixes both; Stage D bug, integration #563/#559. |
| Uninitialized cstate write | Final SM8550 dpu_crtc.c; H700/x86 configuration gates | FILE-FOLLOWUP / BY-DESIGN | Final patched function still dereferences before assignment; H700/x86 do not enable DRM_MSM. No broader driver audit claimed. |
| Diagnostic mistaken for execution | H700 concatenated 0002; other five plans | SAFE-AS-TESTED at source level | Complete candidates all succeed; sole diagnostic mismatch is H700 011; no six-product-bug claim. |
| Failed-candidate promotion | Deliberate partial failure and blocked successor | SAFE-AS-TESTED | One engine used for fixture and real rows; original prefix digest unchanged. |
| Creation-only archive extraction | Firmware two targets; other five tar lists | SAFE-AS-TESTED | Missing members individually matched to created paths; empty root supported. |
| Duplicate patch maintenance | Three kernel version pairs; two U-Boot DDR pairs | BY-DESIGN pending owner decision | All five byte-identical; no consolidation authorized. T11/T27 retain ownership. |

Sweep verdict: PARTIAL for product resolution because the known 0010 defect is not fixed or filed until Stage D; PASS for this source-audit enumeration. No Critical finding. One High source defect remains; method error is resolved within the authorized audit procedure.

## Missing Artifacts

Stage C formal `tools/t41-tables.py`, `second-opinions/review-plan.json` and pre-issue lint; Stage D `05`, audit/bug issues and two question comments; F resolution receipts; G final retro; H closing ledger/readback/merge/cleanup. These are procedure stages after this checkpoint, not silently claimed complete. The Stage-B 02/03/04 and corrected source packet are complete.

## Retrospective Summary

Architectural assessment: coherent source table with explicit build/runtime boundary. Cornerstone alignment: HIGH within source-only scope. Cross-system intersections were exercised where they concern bytes/order and recorded as untested where they require runtime. The methodological drift is approved and its evidence retained. Nothing was done to either time-to-play number.
