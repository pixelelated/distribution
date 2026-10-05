# Remaining P3 criteria — #361, #168, #383

Reconciled against the selected source3036478 and frozen replacement12
55d8ee8, after QA17/proxy13/subset10. This records the scope of existing
evidence; it is not a new test run, an account-backed result, or P4 review.

| #361 criterion | Evidence and disposition |
| --- | --- |
| Owner's current-upstream direction | Recorded in D-WORKFLOW-138; complete. |
| Every downstream patch has a disposition and applies cleanly | The [current integration map](../../rasteratops/raofflineproxy-refresh.md) names all15 retained patches plus upstream replacements014/017. [Selected-source receipts](../2026-10-05-proxy-3036478/README.md) record zero-fuzz application; complete. |
| Whole-library readiness, interruption/retry and request pacing | The exact-source host02 integration logs cover indexed/unindexed125-game scans, queued-not-ready behavior, retry and persisted429 pause against actual7252fc and historical865e21 predecessors; complete within synthetic-provider scope. |
| Existing state survives and declined/unanswered telemetry never sends | [Proxy13](proxy-13/README.md) covers22 installed preservation assertions; [subset10](subset-10/README.md) covers35 installed HTTP refusal/reconnection/idempotence assertions. Exact-source host02 `patched.log` passes consent/version/decline/no-report tests. This combines installed state/HTTP evidence with host consent tests; it does not claim an installed telemetry-capture run. Retain the compound criterion open until that evidence scope is explicitly accepted or the installed gap is exercised. |
| Linux/fork suites, image build, ordinary offline award and UI/progress/flush | Exact-source815 host tests and11 integration assertions per predecessor pass; replacement12 build and scoped installed checks pass. Ordinary `tools/ra-offline-test` new-award proof and its account-backed UI/progress/flush evidence still require the dedicated QA-account prerequisite. Partial; keep open. |
| Frozen package freshness and cut record | Freshness03 returned0 on sealed candidate inputs; the immutable bundle retains the log/completion/input manifest. Complete. |
| General-purpose fixes reconciled with #168 | The current patch map and two focused draft contributions exist, but the complete older-audit mapping and per-item contribution dispositions are unfinished. Keep open. |

The immediately executable next task is #168's source/disposition mapping,
including PL-01, PL-02, PL-12, PL-20 and PL-22 from the September14 audit,
plus its related PL-25/PL-33 fixes. Read the issue through its latest comments
and compare the selected/current upstream source before marking items adopted
or preparing contributions. The existing image-publication and pixelelated
identity drafts remain prepared, not submitted. Upstream acceptance itself
does not block the locally qualified candidate.

Account-dependent work remains separate: obtain Tobu100359 reset or alternate
dedicated RA-account status and the dedicated Dropbox credential-file path.
No answer has arrived. Public sign-in, synthetic markers, already-earned
awards and hardcore mode do not satisfy those proofs. Then reconcile all P3
criteria, perform the approved primary plus Fable5.1/xhigh Facilitator review,
resolve/requalify findings, and build H700 arm before aarch64.

The [fresh-context reader](completed-resume-reader-proof.json) independently
verified source, bundle, retained receipts, current tracker order and absent
recorded processes. Its observation is a handoff proof, not the independent
P4 code audit. No RC designation, physical-device action, or cleanup follows
from this document.
