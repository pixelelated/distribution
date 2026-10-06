# RAOfflineProxy contribution reconciliation

Mapping reviewed at upstream b09d604ecaba7c973028a659b69106b72d3c9514; seven additional drafts qualified directly against candidate source879b158995d412af434301ebdae581f66b8b6d57, 2026-10-06. The latter changes Android only; reviewed Linux/native bytes are identical.
Owner #168; integration #361. Current source mapping; preparation/submission status remains explicit below. Nothing here means a contribution has been submitted or accepted.

The current full-series disposition is maintained in
[full patch disposition](../../rasteratops/raofflineproxy-refresh.md):16 retained patches, retired006,
014 and017. Tests of the combined fork series do not automatically qualify an
upstream-only patch. Keep local fixes until adoption plus integration proof.

| Patch | General-purpose contribution / dependency |
| --- | --- |
|001|[HTTP client errors](client-errors/README.md): standalone draft; 3 targeted tests and 26 related-suite executions pass; pristine client-error cases fail.|
|002|[Warning achievement sets](warning-sets/README.md): standalone draft; 4 targeted tests and 27 related-suite executions pass; 3 pristine tests fail, including old-cache serving.|
|003|Consumable award-flush event; agree interface with upstream. Android pending-award automation added in b09 is not a Linux flush event.|
|004|Explicit whole-library preparation without the background100-game budget; API/policy discussion first, retain locks/pacing/429 pause. Old total-library-cap removal proposal is obsolete.|
|005|[Refresh resilience](refresh-resilience/README.md): standalone draft; 6 targeted tests and 57 related-suite executions pass. Pristine has 2 assertion failures and an escaping pass exception. Old50-game/24-hour selection remains obsolete.|
|007|[Configured cached sign-in](configured-login/README.md): standalone draft; 7 real-storage/config tests pass, 5 fail pristine. Explicit-token and unconfigured fallback controls pass.|
|008|[Log-upload consent](log-consent/README.md): standalone draft; default no-consent upload fails pristine; 6 fixed tests pass, including explicit-true/invalid-value subcases. Usage consent is separate; installed reporting belongs to #457/#361.|
|009|Concurrent image publication; standalone draft applies on b09; before fails, fixed passes (1 concurrent-publication test).|
|010|Local-store-only request contract; coordinate API with upstream before sending the fork's interface policy.|
|011|Response provenance header; coordinate with consumers/upstream, preserving response body.|
|012|Immediate offline/store-only image miss; depends on agreed010 contract.|
|013|[Image completeness](image-completeness/README.md): independent draft; 6 targeted tests and 16 related-suite executions pass. Pristine publishes corrupt images/accepts short bodies; 7 negative subcase assertions fail.|
|015|[Bounded DNS](bounded-dns/README.md): standalone draft; 8 targeted/30 related-suite tests pass. Pristine connection refusal control fails; worker deadline/release, answer reuse/expiry and IPv6 behavior covered. Process-wide resolver wrapper is explicit for upstream review.|
|016|Image outcome API for absent versus transient failures; coordinate API with callers.|
|018|pixelelated platform/account discovery; standalone draft applies on b09; before fails, fixed passes (16 platform tests).|
|019|Initial consent-cache observation before uptime30; standalone failing-before/passing-after tests and draft prepared.|

## Older audit and discussion items

| Earlier item | Current source and disposition |
| --- | --- |
|PL-01|`proxy_service.py` PeriodicRefresh uses seven-day recently-played selection and due checks. Do not resubmit the superseded whole-library hourly selection fix; exception resilience remains005/PL-25.|
|PL-02 /006|`storage.py` protects permanent prefixes during eviction; `test_linux_refresh_scope.py` covers SQLite/JSON retention. Do not resubmit old game-lifetime eviction patch.|
|PL-12|`usage_stats.py`/`usage_report.py` have usage opt-in; `proxy_service.py:retry_storage_corruption_report` still lacks independent log consent without008. Separate contracts.|
|PL-20 / item11|`utils.py` query regex[tp] and form keys{t,p} leave username u. Upstream redaction suggestion remains; no claim this is newly introduced by the fork refresh.|
|PL-22 / item12|`storage.py` has no consumer schema-version row. Propose a versioned consumer contract rather than inventing an incompatible local marker. Fork SQL review note and actual-Storage tests remain the guard.|
|PL-23|Configured-account selection remains007; whole-game readiness/cache keys are exercised by fork integration.|
|PL-25|005 still isolates per-game and per-pass failures; retain.|
|PL-33|009 remains a distinct concurrent-writer fix; connection reuse014 does not resolve shared temporary paths.|
|Item5|GitHub source archives still omit submodule contents. Current upstream CI explicitly checks out recursive submodules and builds the native library (`.github/workflows/tests.yml`, `linux/build_rchash.sh`). Treat as packager documentation, not a claim current Linux releases cannot hash ROMs. Fork recipes consume both exact gitlinks.|
|Items6/10|Current `rom_browser.py` uses local game-id answers, caches valid no-match responses, skips already cached game downloads and records a source ROM path. `test_linux_refresh_scope.py` covers these cases. Historical blanket claim is superseded.|
|Item7|Current `main.py` choices include cache-rom/cache-roms, not cache-indexed. Propose an indexed entrypoint using existing `cache_game`; fork helper integration proves125-game preparation, not a generic CLI contract.|
|Item8|SDL cached-games labels include the full list and viewport scrolling; no dedicated filter/paging in this view. Enhancement idea for upstream; this fork does not ship/use the SDL menu.|
|Item9|`ua::last` is still written and preserved from eviction; repository-wide symbol search finds no read for outgoing requests. Keep as an upstream cleanup question; request/award-specific user agents remain meaningful and must not be removed with it.|
|Item13 /PL-17|SDL recursive scanner still stops at MAX_SCAN_ENTRIES5000 before cache filtering. Fork ctl uses its own resumable walk and tested cursor; upstream SDL enhancement is separate from fork readiness.|
|014|Current image code reuses per-thread/host connections; retired, do not resubmit.|
|017|Current subset-aware award mapping and award-parity tests cover each set's game ID; retired, do not resubmit.|

System toggle, hardcore explanation, native achievement pages, scan progress and
sync-card wording are downstream UI integrations. Offer architecture ideas only;
do not send EmulationStation presentation code as a Linux-proxy fix.

The two earlier drafts were rechecked on b09: their unchanged patches apply
with fuzz0, pristine production code fails the regression, fixed code passes.
[Retained receipts](../../qa-logs/2026-10-06-proxy-consent/upstream-draft-recheck/).
The early-consent draft has its separate8-test before/after proof. The other
rows name why a standalone submission is not yet ready (API agreement or an
independent regression). No row claims a PR exists. Prior D-RA-016 requests
maintainer go before outward contributions; this map and the ten concrete
drafts prepare that review. #168 remains open for the remaining preparations
and submission/disposition record.
No CONTRIBUTING/AGENTS/SKILL file was found in the exact source archive. Recheck
current upstream open PRs before any outward submission to avoid duplicates.

Source anchors at the exact reviewed commit:
[Linux source](https://github.com/misantronic/RAOfflineProxy/tree/b09d604ecaba7c973028a659b69106b72d3c9514/linux/raofflineproxy),
[refresh regressions](https://github.com/misantronic/RAOfflineProxy/blob/b09d604ecaba7c973028a659b69106b72d3c9514/linux/tests/test_linux_refresh_scope.py),
[native-build CI](https://github.com/misantronic/RAOfflineProxy/blob/b09d604ecaba7c973028a659b69106b72d3c9514/.github/workflows/tests.yml).


## Additional standalone preparation — 2026-10-06

Seven more focused drafts cover001/002/005/007/008/013/015. Their40 targeted tests
pass independently; related suites total169 test executions (including repeated
award-parity coverage), with no skips. Negative controls exercise pristine
production code. Distribution patches are regenerated against879 and reapplied
at fuzz0 in fresh source copies. [Evidence](../../qa-logs/2026-10-06-upstream-drafts/README.md).
A sandbox-only socket failure and the initial005 context-rebase failure are
retained; neither is asserted as a product failure or passing test.

015 now has timeout, answer-reuse and worker-lifecycle controls; its
process-wide socket wrapper remains explicit in the proposed review.
003/004/010/011/012/016 and the older API/CLI/SDL ideas still
need interface/policy agreement. Existing map rows name the scope and reason;
they are not submitted or accepted. No candidate source pin or image changed.

Live upstream remains879b158. Open PRs206/84 concern SteamOS/RetroDECK discovery
and packaging; retained bodies/file lists show no duplicate of these seven
behavioral drafts. Recheck shared config.py context for identity/consent work
before opening or rebasing. No outward contribution has been made.
