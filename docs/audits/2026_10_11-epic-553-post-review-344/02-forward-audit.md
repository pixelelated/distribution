# Forward audit — #553

**Auditor:** code-auditor, Codex/OpenAI primary.
**Date:** 2026-10-11
**Subject:** #553 bounded Epic under #344.
**Spec:** inputs/issues.json.

## AC-528-01: Every selected image and ARM compatibility profile has a component inventory tied to its immutable bundle and original input-manifest hash, with a source/licence disposition per component, including embedded/vendored dependencies.

**Source:** #528, criterion1. **Verdict:** PARTIAL.

**Evidence:** `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:26`; docs/qa-logs/2026-10-11-component-inputs/dispositions.json (historical); docs/qa-logs/2026-10-11-component-inputs/rclone-1.75.2-binding.json (current, publication held); docs/qa-logs/2026-10-11-component-inputs/README.md; checks/pkgcheck.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Attempted to treat declaration existence as complete clearance: the retained disposition explicitly keeps every publication_clearance false and identifies five aggregate gaps. The real immutable archive is the prior installed archive; recipe now copies checksum-verified bytes.

**Notes:** Engineering subset is delivered and all14 recipe files selected by13 package names lint successfully; the full publication obligation is not satisfied. Five publication criteria remain pre-existing #528 scope, outside this audit completion gate.

**Gap:** pre-existing #528 publication work remains open; this is not audit-discovered and is not a new punch item.

## AC-528-02: The 17 missing declarations and special inputs above have source-cited dispositions and retained exact notices; no recipe-header licence is substituted for the shipped third-party work's licence. Any required product change has its own rebuilt/requalified artifact before release.

**Source:** #528, criterion2. **Verdict:** PARTIAL.

**Evidence:** `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:26`; docs/qa-logs/2026-10-11-component-inputs/dispositions.json (historical); docs/qa-logs/2026-10-11-component-inputs/rclone-1.75.2-binding.json (current, publication held); docs/qa-logs/2026-10-11-component-inputs/README.md; checks/pkgcheck.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Attempted to treat declaration existence as complete clearance: the retained disposition explicitly keeps every publication_clearance false and identifies five aggregate gaps. The real immutable archive is the prior installed archive; recipe now copies checksum-verified bytes.

**Notes:** Engineering subset is delivered and all14 recipe files selected by13 package names lint successfully; the full publication obligation is not satisfied. Five publication criteria remain pre-existing #528 scope, outside this audit completion gate.

**Gap:** pre-existing #528 publication work remains open; this is not audit-discovered and is not a new punch item.

## AC-528-03: A fork-owned corresponding-source bundle retains exact fetched source archives/git/submodules, fork patches and build scripts, with machine-readable hashes and a complete component-to-member map. Prebuilt rclone/ABL/shareware assets and Nix inputs are explicitly assessed rather than silently counted as source.

**Source:** #528, criterion3. **Verdict:** PARTIAL.

**Evidence:** `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:26`; docs/qa-logs/2026-10-11-component-inputs/dispositions.json (historical); docs/qa-logs/2026-10-11-component-inputs/rclone-1.75.2-binding.json (current, publication held); docs/qa-logs/2026-10-11-component-inputs/README.md; checks/pkgcheck.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Attempted to treat declaration existence as complete clearance: the retained disposition explicitly keeps every publication_clearance false and identifies five aggregate gaps. The real immutable archive is the prior installed archive; recipe now copies checksum-verified bytes.

**Notes:** Engineering subset is delivered and all14 recipe files selected by13 package names lint successfully; the full publication obligation is not satisfied. Five publication criteria remain pre-existing #528 scope, outside this audit completion gate.

**Gap:** pre-existing #528 publication work remains open; this is not audit-discovered and is not a new punch item.

## AC-528-04: Independent retrieval and hash verification of the source bundle pass, and the required backup custody is evidenced; local source-cache existence and public repository visibility alone do not close this criterion.

**Source:** #528, criterion4. **Verdict:** PARTIAL.

**Evidence:** `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:26`; docs/qa-logs/2026-10-11-component-inputs/dispositions.json (historical); docs/qa-logs/2026-10-11-component-inputs/rclone-1.75.2-binding.json (current, publication held); docs/qa-logs/2026-10-11-component-inputs/README.md; checks/pkgcheck.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Attempted to treat declaration existence as complete clearance: the retained disposition explicitly keeps every publication_clearance false and identifies five aggregate gaps. The real immutable archive is the prior installed archive; recipe now copies checksum-verified bytes.

**Notes:** Engineering subset is delivered and all14 recipe files selected by13 package names lint successfully; the full publication obligation is not satisfied. Five publication criteria remain pre-existing #528 scope, outside this audit completion gate.

**Gap:** pre-existing #528 publication work remains open; this is not audit-discovered and is not a new punch item.

## AC-528-05: #344, M7, the release manifest/notes and canonical checkpoint link the final inventory, bundle and any remaining physical/publication gates. Publication is not claimed while an unresolved disposition remains.

**Source:** #528, criterion5. **Verdict:** PARTIAL.

**Evidence:** `projects/ROCKNIX/packages/emulators/libretro/idtech-lr/package.mk:26`; docs/qa-logs/2026-10-11-component-inputs/dispositions.json (historical); docs/qa-logs/2026-10-11-component-inputs/rclone-1.75.2-binding.json (current, publication held); docs/qa-logs/2026-10-11-component-inputs/README.md; checks/pkgcheck.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Attempted to treat declaration existence as complete clearance: the retained disposition explicitly keeps every publication_clearance false and identifies five aggregate gaps. The real immutable archive is the prior installed archive; recipe now copies checksum-verified bytes.

**Notes:** Engineering subset is delivered and all14 recipe files selected by13 package names lint successfully; the full publication obligation is not satisfied. Five publication criteria remain pre-existing #528 scope, outside this audit completion gate.

**Gap:** pre-existing #528 publication work remains open; this is not audit-discovered and is not a new punch item.

## AC-541-01: Exact upstream commit/tag/archive hashes and Linux/native/submodule/file-change review are recorded, with every retained fork patch applying and no silent loss of whole-library preparation, opt-in behavior, saved state or offline queue behavior.

**Source:** #541, criterion1. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed:71`; docs/qa-logs/2026-10-11-dependency-refresh/fetch.json; checks/proxy-fixed.log; checks/proxy-negative.log; checks/installed-rclone-version.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched retained patches and current queue/watcher consumers for removed budget/429/lock guards, silent watched-folder activation and changed store schema. budgeted defaults true; missing watched_folders returns empty. Current helper calls and preserved pause controls cover the deliberate exception. Wrong-duration helper fails one of12 tests. Rehashed both ZIPs against retained upstream sums; fresh installed binary reports1.75.2.

**Notes:** Fresh fixed12/0, negative12/1; retained866 upstream tests,18 installed native cases/legacyCHD,22 offline-service assertions and consent controls supply distinct runtime predicates. Protocol108×3 runs are real local endpoints, not hosted-provider authentication. Source/bundle and prior posted freshness verdict remain timestamp-bound.

## AC-541-02: rclone1.75.2 archive hashes and version output are verified; local WebDAV/SFTP/S3 protocol regressions pass with that binary.

**Source:** #541, criterion2. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed:71`; docs/qa-logs/2026-10-11-dependency-refresh/fetch.json; checks/proxy-fixed.log; checks/proxy-negative.log; checks/installed-rclone-version.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched retained patches and current queue/watcher consumers for removed budget/429/lock guards, silent watched-folder activation and changed store schema. budgeted defaults true; missing watched_folders returns empty. Current helper calls and preserved pause controls cover the deliberate exception. Wrong-duration helper fails one of12 tests. Rehashed both ZIPs against retained upstream sums; fresh installed binary reports1.75.2.

**Notes:** Fresh fixed12/0, negative12/1; retained866 upstream tests,18 installed native cases/legacyCHD,22 offline-service assertions and consent controls supply distinct runtime predicates. Protocol108×3 runs are real local endpoints, not hosted-provider authentication. Source/bundle and prior posted freshness verdict remain timestamp-bound.

## AC-541-03: Proxy upstream tests and fork-relevant state/rate-limit/consent/recovery controls pass on the proposed source; changed assumptions and installed-image follow-up are explicit.

**Source:** #541, criterion3. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed:71`; docs/qa-logs/2026-10-11-dependency-refresh/fetch.json; checks/proxy-fixed.log; checks/proxy-negative.log; checks/installed-rclone-version.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched retained patches and current queue/watcher consumers for removed budget/429/lock guards, silent watched-folder activation and changed store schema. budgeted defaults true; missing watched_folders returns empty. Current helper calls and preserved pause controls cover the deliberate exception. Wrong-duration helper fails one of12 tests. Rehashed both ZIPs against retained upstream sums; fresh installed binary reports1.75.2.

**Notes:** Fresh fixed12/0, negative12/1; retained866 upstream tests,18 installed native cases/legacyCHD,22 offline-service assertions and consent controls supply distinct runtime predicates. Protocol108×3 runs are real local endpoints, not hosted-provider authentication. Source/bundle and prior posted freshness verdict remain timestamp-bound.

## AC-541-04: Freshness fixture proves active package/project recipes are included while archived evidence is excluded; the final source freshness check exits0 with intentional coupled pins documented.

**Source:** #541, criterion4. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed:71`; docs/qa-logs/2026-10-11-dependency-refresh/fetch.json; checks/proxy-fixed.log; checks/proxy-negative.log; checks/installed-rclone-version.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched retained patches and current queue/watcher consumers for removed budget/429/lock guards, silent watched-folder activation and changed store schema. budgeted defaults true; missing watched_folders returns empty. Current helper calls and preserved pause controls cover the deliberate exception. Wrong-duration helper fails one of12 tests. Rehashed both ZIPs against retained upstream sums; fresh installed binary reports1.75.2.

**Notes:** Fresh fixed12/0, negative12/1; retained866 upstream tests,18 installed native cases/legacyCHD,22 offline-service assertions and consent controls supply distinct runtime predicates. Protocol108×3 runs are real local endpoints, not hosted-provider authentication. Source/bundle and prior posted freshness verdict remain timestamp-bound.

## AC-541-05: Source commits, M7 ordered plan and a new combined-image freeze cite the final input set; combined installed/clean/retained QA remains under #344/#537. No RC designation or publication clearance follows from a dependency bump.

**Source:** #541, criterion5. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-cache-indexed:71`; docs/qa-logs/2026-10-11-dependency-refresh/fetch.json; checks/proxy-fixed.log; checks/proxy-negative.log; checks/installed-rclone-version.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched retained patches and current queue/watcher consumers for removed budget/429/lock guards, silent watched-folder activation and changed store schema. budgeted defaults true; missing watched_folders returns empty. Current helper calls and preserved pause controls cover the deliberate exception. Wrong-duration helper fails one of12 tests. Rehashed both ZIPs against retained upstream sums; fresh installed binary reports1.75.2.

**Notes:** Fresh fixed12/0, negative12/1; retained866 upstream tests,18 installed native cases/legacyCHD,22 offline-service assertions and consent controls supply distinct runtime predicates. Protocol108×3 runs are real local endpoints, not hosted-provider authentication. Source/bundle and prior posted freshness verdict remain timestamp-bound.

## AC-542-01: Preserve the original nonzero results and bind the repaired checks to the exact product-source bytes used by replacement19.

**Source:** #542, criterion1. **Verdict:** PASS.

**Evidence:** `docs/es-menu-map.md:278`; inputs/es-test-only.diff; inputs/es-source-binding.json; checks/es-lifetime.log; docs/qa-logs/2026-10-11-qualification-gaps/menumap.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-report.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared ES test-only diff: one rendering-double method is added; no product callbacks changed. Fresh ASan executions cover all four routes. Original compile/map failures retained. Current installed standard lifetime/governor/map results independently pass.

**Notes:** Four ASan routes passed again. Existing six governor controls and55-screen inventory are original primary receipts; this does not infer full UI behavior from a no-op rendering double.

## AC-542-02: The corrected rendering double compiles the unchanged callbacks; all four lifetime routes pass under ASan, with the governor check passing too.

**Source:** #542, criterion2. **Verdict:** PASS.

**Evidence:** `docs/es-menu-map.md:278`; inputs/es-test-only.diff; inputs/es-source-binding.json; checks/es-lifetime.log; docs/qa-logs/2026-10-11-qualification-gaps/menumap.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-report.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared ES test-only diff: one rendering-double method is added; no product callbacks changed. Fresh ASan executions cover all four routes. Original compile/map failures retained. Current installed standard lifetime/governor/map results independently pass.

**Notes:** Four ASan routes passed again. Existing six governor controls and55-screen inventory are original primary receipts; this does not infer full UI behavior from a no-op rendering double.

## AC-542-03: The canonical map explicitly includes CONNECTION SAVED, its retained active selection and NC08 frame links; inventory check reports no missing/stale screens.

**Source:** #542, criterion3. **Verdict:** PASS.

**Evidence:** `docs/es-menu-map.md:278`; inputs/es-test-only.diff; inputs/es-source-binding.json; checks/es-lifetime.log; docs/qa-logs/2026-10-11-qualification-gaps/menumap.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-report.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared ES test-only diff: one rendering-double method is added; no product callbacks changed. Fresh ASan executions cover all four routes. Original compile/map failures retained. Current installed standard lifetime/governor/map results independently pass.

**Notes:** Four ASan routes passed again. Existing six governor controls and55-screen inventory are original primary receipts; this does not infer full UI behavior from a no-op rendering double.

## AC-542-04: Test/reference-only commits, regression results, friction/work-log entries and M7 continuation are delivered without relabelling the original aggregate VM result.

**Source:** #542, criterion4. **Verdict:** PASS.

**Evidence:** `docs/es-menu-map.md:278`; inputs/es-test-only.diff; inputs/es-source-binding.json; checks/es-lifetime.log; docs/qa-logs/2026-10-11-qualification-gaps/menumap.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-report.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared ES test-only diff: one rendering-double method is added; no product callbacks changed. Fresh ASan executions cover all four routes. Original compile/map failures retained. Current installed standard lifetime/governor/map results independently pass.

**Notes:** Four ASan routes passed again. Existing six governor controls and55-screen inventory are original primary receipts; this does not infer full UI behavior from a no-op rendering double.

## AC-543-01: Retain original 11-test receipts and document the mismatch without relabelling them.

**Source:** #543, criterion1. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-integration-test:235`; checks/proxy-fixed.log; checks/proxy-negative.log; docs/qa-logs/2026-10-11-proxy-test-discovery/original74.log; docs/qa-logs/2026-10-11-proxy-test-discovery/source.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Looked for omitted classes and assertions that could not fail. Module discovery includes named PreparationCadence; fresh zero-duration mutation fails exactly one of12 cases while real helper12/0 succeeds. Original11-case receipts remain11.

**Notes:** No firmware bytes changed for discovery; helper digest remains sealed. Counts are taken from actual output, not manually inferred.

## AC-543-02: Discover all declared test cases, including the actual 50/100-game pause boundaries and 30-second duration assertion; final native integration output names the pacing case and reports 12 tests with no failures/skips.

**Source:** #543, criterion2. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-integration-test:235`; checks/proxy-fixed.log; checks/proxy-negative.log; docs/qa-logs/2026-10-11-proxy-test-discovery/original74.log; docs/qa-logs/2026-10-11-proxy-test-discovery/source.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Looked for omitted classes and assertions that could not fail. Module discovery includes named PreparationCadence; fresh zero-duration mutation fails exactly one of12 cases while real helper12/0 succeeds. Original11-case receipts remain11.

**Notes:** No firmware bytes changed for discovery; helper digest remains sealed. Counts are taken from actual output, not manually inferred.

## AC-543-03: A negative control that omits the required pacing behavior fails that named assertion; production helper bytes stay unchanged.

**Source:** #543, criterion3. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-integration-test:235`; checks/proxy-fixed.log; checks/proxy-negative.log; docs/qa-logs/2026-10-11-proxy-test-discovery/original74.log; docs/qa-logs/2026-10-11-proxy-test-discovery/source.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Looked for omitted classes and assertions that could not fail. Module discovery includes named PreparationCadence; fresh zero-duration mutation fails exactly one of12 cases while real helper12/0 succeeds. Original11-case receipts remain11.

**Notes:** No firmware bytes changed for discovery; helper digest remains sealed. Counts are taken from actual output, not manually inferred.

## AC-543-04: Deliver the harness/evidence corrections and reconcile #541/M7/source notes before any next device build.

**Source:** #543, criterion4. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-integration-test:235`; checks/proxy-fixed.log; checks/proxy-negative.log; docs/qa-logs/2026-10-11-proxy-test-discovery/original74.log; docs/qa-logs/2026-10-11-proxy-test-discovery/source.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Looked for omitted classes and assertions that could not fail. Module discovery includes named PreparationCadence; fresh zero-duration mutation fails exactly one of12 cases while real helper12/0 succeeds. Original11-case receipts remain11.

**Notes:** No firmware bytes changed for discovery; helper digest remains sealed. Counts are taken from actual output, not manually inferred.

## AC-544-01: Retain the original six-region failure, reviewed current/baseline frames and exact source/hash references.

**Source:** #544, criterion1. **Verdict:** PASS.

**Evidence:** `tools/vm-walks/claims.txt:57`; docs/qa-logs/2026-10-11-frame-claims/review.json; docs/qa-logs/2026-10-11-frame-claims/missing-claim-control.log; docs/qa-logs/2026-10-11-frame-claims/corrected.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-frame-diff.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared claims diff against original6-region failure and missing-claim refusal; searched for mask/baseline changes in the same git range and found none. Every new claim names the approved cloud row or CLEAR change; no blanket screen mask added.

**Notes:** Original reviewed frames and exact78-frame comparisons remain the visual evidence. Pixel acceptance is limited to documented regions, not an inference that all possible UI states were tested.

## AC-544-02: Each accepted difference maps to the approved cloud-management or CLEAR behavior; no baseline move or additional blind mask.

**Source:** #544, criterion2. **Verdict:** PASS.

**Evidence:** `tools/vm-walks/claims.txt:57`; docs/qa-logs/2026-10-11-frame-claims/review.json; docs/qa-logs/2026-10-11-frame-claims/missing-claim-control.log; docs/qa-logs/2026-10-11-frame-claims/corrected.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-frame-diff.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared claims diff against original6-region failure and missing-claim refusal; searched for mask/baseline changes in the same git range and found none. Every new claim names the approved cloud row or CLEAR change; no blanket screen mask added.

**Notes:** Original reviewed frames and exact78-frame comparisons remain the visual evidence. Pixel acceptance is limited to documented regions, not an inference that all possible UI states were tested.

## AC-544-03: All 78 frames compare successfully with the corrected claims, with no unclaimed/missing screens; a missing-claim control still fails.

**Source:** #544, criterion3. **Verdict:** PASS.

**Evidence:** `tools/vm-walks/claims.txt:57`; docs/qa-logs/2026-10-11-frame-claims/review.json; docs/qa-logs/2026-10-11-frame-claims/missing-claim-control.log; docs/qa-logs/2026-10-11-frame-claims/corrected.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-frame-diff.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared claims diff against original6-region failure and missing-claim refusal; searched for mask/baseline changes in the same git range and found none. Every new claim names the approved cloud row or CLEAR change; no blanket screen mask added.

**Notes:** Original reviewed frames and exact78-frame comparisons remain the visual evidence. Pixel acceptance is limited to documented regions, not an inference that all possible UI states were tested.

## AC-544-04: Deliver the claim/reference correction and update M7 before H700/SM8550 builds.

**Source:** #544, criterion4. **Verdict:** PASS.

**Evidence:** `tools/vm-walks/claims.txt:57`; docs/qa-logs/2026-10-11-frame-claims/review.json; docs/qa-logs/2026-10-11-frame-claims/missing-claim-control.log; docs/qa-logs/2026-10-11-frame-claims/corrected.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-standard-frame-diff.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Compared claims diff against original6-region failure and missing-claim refusal; searched for mask/baseline changes in the same git range and found none. Every new claim names the approved cloud row or CLEAR change; no blanket screen mask added.

**Notes:** Original reviewed frames and exact78-frame comparisons remain the visual evidence. Pixel acceptance is limited to documented regions, not an inference that all possible UI states were tested.

## AC-545-01: Original error/result channels remain recorded; absent guest processes and stopped local endpoints verified.

**Source:** #545, criterion1. **Verdict:** PASS.

**Evidence:** `tools/vm-pair:67`; checks/vm-pair.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/run.py; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json; checks/result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh9 launch controls include exit17, missing/dead/wrong process, wrong disk and owned disk, failed serial and unwritable/writable runtime roots. Random re-verification inspected hash-sealed actual upgrade owner runtime override and successful real reboot/save-hash evidence; no current VM boot is invented.

**Notes:** Source rc propagation is independent from grep output. Runtime writes use an owned /workspace path; cleanup authority is not inferred for unreadable unrelated files. The original fake-up failure remains preserved.

## AC-545-02: vm-pair preserves launch failure and verifies a live owned PID before printing up; an injected failure control fails promptly and the successful launch path is tested.

**Source:** #545, criterion2. **Verdict:** PASS.

**Evidence:** `tools/vm-pair:67`; checks/vm-pair.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/run.py; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json; checks/result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh9 launch controls include exit17, missing/dead/wrong process, wrong disk and owned disk, failed serial and unwritable/writable runtime roots. Random re-verification inspected hash-sealed actual upgrade owner runtime override and successful real reboot/save-hash evidence; no current VM boot is invented.

**Notes:** Source rc propagation is independent from grep output. Runtime writes use an owned /workspace path; cleanup authority is not inferred for unreadable unrelated files. The original fake-up failure remains preserved.

## AC-545-03: Use an owned writable runtime directory outside /tmp, document the quota boundary, and replay the upgrade from a fresh watched owner. No unreadable dependency is a cleanup approval; broader obsolete payload retirement remains #493.

**Source:** #545, criterion3. **Verdict:** PASS.

**Evidence:** `tools/vm-pair:67`; checks/vm-pair.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/run.py; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json; checks/result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh9 launch controls include exit17, missing/dead/wrong process, wrong disk and owned disk, failed serial and unwritable/writable runtime roots. Random re-verification inspected hash-sealed actual upgrade owner runtime override and successful real reboot/save-hash evidence; no current VM boot is invented.

**Notes:** Source rc propagation is independent from grep output. Runtime writes use an owned /workspace path; cleanup authority is not inferred for unreadable unrelated files. The original fake-up failure remains preserved.

## AC-545-04: Deliver tool, regression and work-log evidence before new device builds. Existing #493 retention scope owns broader historical cleanup.

**Source:** #545, criterion4. **Verdict:** PASS.

**Evidence:** `tools/vm-pair:67`; checks/vm-pair.log; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/run.py; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json; checks/result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh9 launch controls include exit17, missing/dead/wrong process, wrong disk and owned disk, failed serial and unwritable/writable runtime roots. Random re-verification inspected hash-sealed actual upgrade owner runtime override and successful real reboot/save-hash evidence; no current VM boot is invented.

**Notes:** Source rc propagation is independent from grep output. Runtime writes use an owned /workspace path; cleanup authority is not inferred for unreadable unrelated files. The original fake-up failure remains preserved.

## AC-546-01: Original failed hashes and later file inventory retained with timestamps and source identity.

**Source:** #546, criterion1. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-rehearsal:39`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh7 states verify boot identity and service status with exact poll bounds; original three mutations reject ignored boot, ignored state and wrong unit. Both wait call sites precede seed/hash reads; no stale appended boot.log can satisfy the query.

**Notes:** Actual19→20 upgrade passes with two current-boot readiness lines and identical four save hashes. This is a host observation ordering repair; it introduces no firmware data migration.

## AC-546-02: Both pre-seed and post-reboot checks wait for the same boot's completed autostart and fail if readiness never arrives; a negative control proves a stale/different boot cannot satisfy readiness.

**Source:** #546, criterion2. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-rehearsal:39`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh7 states verify boot identity and service status with exact poll bounds; original three mutations reject ignored boot, ignored state and wrong unit. Both wait call sites precede seed/hash reads; no stale appended boot.log can satisfy the query.

**Notes:** Actual19→20 upgrade passes with two current-boot readiness lines and identical four save hashes. This is a host observation ordering repair; it introduces no firmware data migration.

## AC-546-03: Fresh actual upgrade preserves all four save hashes and existing settings, with the remaining installed checks allowed to proceed only after that proof.

**Source:** #546, criterion3. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-rehearsal:39`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh7 states verify boot identity and service status with exact poll bounds; original three mutations reject ignored boot, ignored state and wrong unit. Both wait call sites precede seed/hash reads; no stale appended boot.log can satisfy the query.

**Notes:** Actual19→20 upgrade passes with two current-boot readiness lines and identical four save hashes. This is a host observation ordering repair; it introduces no firmware data migration.

## AC-546-04: Deliver the repaired rehearsal and evidence before new device builds.

**Source:** #546, criterion4. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-rehearsal:39`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/actual-rehearsal.raw.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh7 states verify boot identity and service status with exact poll bounds; original three mutations reject ignored boot, ignored state and wrong unit. Both wait call sites precede seed/hash reads; no stale appended boot.log can satisfy the query.

**Notes:** Actual19→20 upgrade passes with two current-boot readiness lines and identical four save hashes. This is a host observation ordering repair; it introduces no firmware data migration.

## AC-547-01: Retain original failure and bind the unchanged upstream tests, installed modules and native library.

**Source:** #547, criterion1. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-installed-native-test:33`; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native.log; docs/qa-logs/2026-10-11-installed-proxy/artifacts/proxy-service-assertions.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/consent.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Read adapter end-to-end: installed path and actual /proc mapping/digest checks precede aliasing; discovered zero/skipped/error cases refuse completion. Original source-tree import failure is preserved, with the new owner carrying unchanged upstream test bytes.

**Notes:** Retained real guest18 native/0skip plus four legacyCHD cases,22 offline service assertions and consent/restart HTTP witnesses; no product overlay. Loopback service evidence is not a live account-award proof.

## AC-547-02: Runner resolves source-tree test imports to the actual installed package; every discovered native test executes with no skips, and legacy CHD controls pass.

**Source:** #547, criterion2. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-installed-native-test:33`; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native.log; docs/qa-logs/2026-10-11-installed-proxy/artifacts/proxy-service-assertions.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/consent.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Read adapter end-to-end: installed path and actual /proc mapping/digest checks precede aliasing; discovered zero/skipped/error cases refuse completion. Original source-tree import failure is preserved, with the new owner carrying unchanged upstream test bytes.

**Notes:** Retained real guest18 native/0skip plus four legacyCHD cases,22 offline service assertions and consent/restart HTTP witnesses; no product overlay. Loopback service evidence is not a live account-award proof.

## AC-547-03: Finish synthetic installed offline-service/consent qualification from a new watched owner; record every original return code and actual process cleanup.

**Source:** #547, criterion3. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-installed-native-test:33`; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native.log; docs/qa-logs/2026-10-11-installed-proxy/artifacts/proxy-service-assertions.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/consent.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Read adapter end-to-end: installed path and actual /proc mapping/digest checks precede aliasing; discovered zero/skipped/error cases refuse completion. Original source-tree import failure is preserved, with the new owner carrying unchanged upstream test bytes.

**Notes:** Retained real guest18 native/0skip plus four legacyCHD cases,22 offline service assertions and consent/restart HTTP witnesses; no product overlay. Loopback service evidence is not a live account-award proof.

## AC-547-04: Deliver the reusable runner and evidence before further device builds.

**Source:** #547, criterion4. **Verdict:** PASS.

**Evidence:** `tools/raofflineproxy-installed-native-test:33`; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native-result.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/native.log; docs/qa-logs/2026-10-11-installed-proxy/artifacts/proxy-service-assertions.json; docs/qa-logs/2026-10-11-installed-proxy/artifacts/consent.log. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Read adapter end-to-end: installed path and actual /proc mapping/digest checks precede aliasing; discovered zero/skipped/error cases refuse completion. Original source-tree import failure is preserved, with the new owner carrying unchanged upstream test bytes.

**Notes:** Retained real guest18 native/0skip plus four legacyCHD cases,22 offline service assertions and consent/restart HTTP witnesses; no product overlay. Loopback service evidence is not a live account-award proof.

## AC-548-01: Original script reproduces missing-hardware errors/unsuccessful status; corrected script has a successful quiet default, no blank or fabricated frequency values, and preserved valid CPU/GPU/temperature conversions.

**Source:** #548, criterion1. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info:27`; checks/optional-info.log; checks/info/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/evidence-index.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-information/script.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/retained-information/script.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh13 full-script controls reproduce original errors, test malformed/empty/overflow/expression/decimal-zero readings, preserve valid x86/ARM/thermal output and retain executed quirk failure. Directly inspected two exact-image640 frames: unknown frequencies explicit, correct identity after real upgrade.

**Notes:** All eight indexed image20 frames rehash; actual clean/retained script exits0 with empty stderr. No physical sensor-accuracy or complete ARM-device runtime claim is made.

## AC-548-02: Optional quirk discovery skips absent/nonexecutable entries, executes valid quirks and retains failures from an executed quirk.

**Source:** #548, criterion2. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info:27`; checks/optional-info.log; checks/info/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/evidence-index.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-information/script.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/retained-information/script.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh13 full-script controls reproduce original errors, test malformed/empty/overflow/expression/decimal-zero readings, preserve valid x86/ARM/thermal output and retain executed quirk failure. Directly inspected two exact-image640 frames: unknown frequencies explicit, correct identity after real upgrade.

**Notes:** All eight indexed image20 frames rehash; actual clean/retained script exits0 with empty stderr. No physical sensor-accuracy or complete ARM-device runtime claim is made.

## AC-548-03: Source-bound VM INFORMATION/CPU frames and canonical references cover the affected missing-data behavior; meaningful positive/negative controls and local review are retained.

**Source:** #548, criterion3. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info:27`; checks/optional-info.log; checks/info/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/evidence-index.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-information/script.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/retained-information/script.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh13 full-script controls reproduce original errors, test malformed/empty/overflow/expression/decimal-zero readings, preserve valid x86/ARM/thermal output and retain executed quirk failure. Directly inspected two exact-image640 frames: unknown frequencies explicit, correct identity after real upgrade.

**Notes:** All eight indexed image20 frames rehash; actual clean/retained script exits0 with empty stderr. No physical sensor-accuracy or complete ARM-device runtime claim is made.

## AC-548-04: The corrected script is included and verified in the next GENERIC_X64 qualification before H700 and SM8550 builds.

**Source:** #548, criterion4. **Verdict:** PASS.

**Evidence:** `projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-info:27`; checks/optional-info.log; checks/info/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/evidence-index.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-information/script.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/retained-information/script.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Fresh13 full-script controls reproduce original errors, test malformed/empty/overflow/expression/decimal-zero readings, preserve valid x86/ARM/thermal output and retain executed quirk failure. Directly inspected two exact-image640 frames: unknown frequencies explicit, correct identity after real upgrade.

**Notes:** All eight indexed image20 frames rehash; actual clean/retained script exits0 with empty stderr. No physical sensor-accuracy or complete ARM-device runtime claim is made.

## AC-549-01: Preserve the original failure and demonstrate the host-only temporary path refusal versus a container-local temporary path using the same pinned image and nonroot user.

**Source:** #549, criterion1. **Verdict:** PASS.

**Evidence:** `docs/qa-logs/2026-10-11-container-temporary-path/README.md:3`; docs/qa-logs/2026-10-11-container-temporary-path/pixelelated-m7-build20-verify/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/result.json; .claude/rules/device-builds.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Refuted the claim that a successful independent observer made original wrappers successful: original build20 remains2 and build20b wrapper remains1. Actual container0, cid/runtime/tmp/mktemp observations and three altered-input refusals provide the explicitly composed acceptance.

**Notes:** Host/container TMPDIR boundaries are documented. No image is accepted merely because its watcher says done; original container and installed artifact channels are retained separately.

## AC-549-02: A fresh watched build owner explicitly scopes its container TMPDIR, records the actual running container environment and consumes original command/outer/launcher results. No frozen product source or existing result is overwritten.

**Source:** #549, criterion2. **Verdict:** PASS.

**Evidence:** `docs/qa-logs/2026-10-11-container-temporary-path/README.md:3`; docs/qa-logs/2026-10-11-container-temporary-path/pixelelated-m7-build20-verify/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/result.json; .claude/rules/device-builds.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Refuted the claim that a successful independent observer made original wrappers successful: original build20 remains2 and build20b wrapper remains1. Actual container0, cid/runtime/tmp/mktemp observations and three altered-input refusals provide the explicitly composed acceptance.

**Notes:** Host/container TMPDIR boundaries are documented. No image is accepted merely because its watcher says done; original container and installed artifact channels are retained separately.

## AC-549-03: Work log, friction record and build instructions capture the host/container temporary-path boundary; the corrected assembled image still proceeds through #548 qualification.

**Source:** #549, criterion3. **Verdict:** PASS.

**Evidence:** `docs/qa-logs/2026-10-11-container-temporary-path/README.md:3`; docs/qa-logs/2026-10-11-container-temporary-path/pixelelated-m7-build20-verify/result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/result.json; .claude/rules/device-builds.md. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Refuted the claim that a successful independent observer made original wrappers successful: original build20 remains2 and build20b wrapper remains1. Actual container0, cid/runtime/tmp/mktemp observations and three altered-input refusals provide the explicitly composed acceptance.

**Notes:** Host/container TMPDIR boundaries are documented. No image is accepted merely because its watcher says done; original container and installed artifact channels are retained separately.

## AC-550-01: Actual host compiler and patch controls fail with unusable scratch and pass with owned scratch; a bubblewrap device fixture still uses its private /tmp, with a recorded log.

**Source:** #550, criterion1. **Verdict:** PASS.

**Evidence:** `tools/last-good-scripts-test:290`; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/final-result.json; docs/qa-logs/2026-10-11-regression-fixtures/original-failures.txt. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched every gcc/cc/patch invocation including embedded package shell; all host calls use owned scratch. Global TMPDIR remains unset for private guest namespaces. Original unusable-scratch compiler/patch failures and namespace refusal prove the controls can fail.

**Notes:** Final sealed host run1378PASS/0FAIL/0SKIP against exact frozen firmware and installed applets. No repeat of the full run was needed after the same tool digests were reverified; focused audit checks are separately retained.

## AC-550-02: All host compiler/patch invocations in this harness use owned scratch; the full corrected frozen-source regression run has zero failures and zero skips, with original QA20 failures retained.

**Source:** #550, criterion2. **Verdict:** PASS.

**Evidence:** `tools/last-good-scripts-test:290`; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/final-result.json; docs/qa-logs/2026-10-11-regression-fixtures/original-failures.txt. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched every gcc/cc/patch invocation including embedded package shell; all host calls use owned scratch. Global TMPDIR remains unset for private guest namespaces. Original unusable-scratch compiler/patch failures and namespace refusal prove the controls can fail.

**Notes:** Final sealed host run1378PASS/0FAIL/0SKIP against exact frozen firmware and installed applets. No repeat of the full run was needed after the same tool digests were reverified; focused audit checks are separately retained.

## AC-550-03: Source, work/friction log and compact proof are delivered; exact-source checks pass.

**Source:** #550, criterion3. **Verdict:** PASS.

**Evidence:** `tools/last-good-scripts-test:290`; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/final-result.json; docs/qa-logs/2026-10-11-regression-fixtures/original-failures.txt. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Searched every gcc/cc/patch invocation including embedded package shell; all host calls use owned scratch. Global TMPDIR remains unset for private guest namespaces. Original unusable-scratch compiler/patch failures and namespace refusal prove the controls can fail.

**Notes:** Final sealed host run1378PASS/0FAIL/0SKIP against exact frozen firmware and installed applets. No repeat of the full run was needed after the same tool digests were reverified; focused audit checks are separately retained.

## AC-551-01: The reusable regression invokes the actual wait and guest query, passing ready and delayed current boots and refusing stale boot, failed service, absent answer, never-ready service and empty identity; logs show expected polling bounds.

**Source:** #551, criterion1. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-readiness-test:15`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/final-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Checked actual query execution through cat/systemctl shims rather than a hardcoded expected echo. Wrong query, ignored boot and ignored service mutations fail; ready/delayed pass with exact poll bounds. Historical source is selected via src_of, not silently substituted with current source.

**Notes:** New fresh7-state test and original3mutations support the replacement for obsolete AUTOSTARTED extraction; full1378 result is source-bound. No new hosted namespace dependency.

## AC-551-02: Negative mutations removing boot identity or service readiness are rejected; the old stale extraction failure is preserved, and the integrated corrected full suite passes.

**Source:** #551, criterion2. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-readiness-test:15`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/final-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Checked actual query execution through cat/systemctl shims rather than a hardcoded expected echo. Wrong query, ignored boot and ignored service mutations fail; ready/delayed pass with exact poll bounds. Historical source is selected via src_of, not silently substituted with current source.

**Notes:** New fresh7-state test and original3mutations support the replacement for obsolete AUTOSTARTED extraction; full1378 result is source-bound. No new hosted namespace dependency.

## AC-551-03: Source, work/friction log and compact proof are delivered; exact-source checks pass.

**Source:** #551, criterion3. **Verdict:** PASS.

**Evidence:** `tools/vm-upgrade-readiness-test:15`; checks/readiness.log; docs/qa-logs/2026-10-11-regression-fixtures/final-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/final-result.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Checked actual query execution through cat/systemctl shims rather than a hardcoded expected echo. Wrong query, ignored boot and ignored service mutations fail; ready/delayed pass with exact poll bounds. Historical source is selected via src_of, not silently substituted with current source.

**Notes:** New fresh7-state test and original3mutations support the replacement for obsolete AUTOSTARTED extraction; full1378 result is source-bound. No new hosted namespace dependency.

## AC-552-01: Exact named suite rows are parsed without the header/separator; failed, missing and duplicate-suite controls are refused with retained results.

**Source:** #552, criterion1. **Verdict:** PASS.

**Evidence:** `docs/qa-logs/2026-10-11-regression-fixtures/suite_parser.py:1`; docs/qa-logs/2026-10-11-regression-fixtures/parser-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/accept-corrected-run.py; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/clean-qualification.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Read exact name-set, row-count, separator and result predicates. Failed/missing/duplicate variants are refused. Composer insists original scripts failed exactly as recorded and corrected source/tools match; it cannot merely count table separators or erase original status.

**Notes:** Run-specific acceptance02 ends0, then actual upgrade consumes its sealed receipt. This evidence helper is not claimed as a reusable acceptance gate for future reports.

## AC-552-02: A fresh supervised acceptance consumes original QA20 failure and corrected regression success, checks all remaining suites/protocols/frames and actual shutdown, and permits upgrade only with explicit passing composed evidence. Original failures remain unchanged.

**Source:** #552, criterion2. **Verdict:** PASS.

**Evidence:** `docs/qa-logs/2026-10-11-regression-fixtures/suite_parser.py:1`; docs/qa-logs/2026-10-11-regression-fixtures/parser-controls.json; docs/qa-logs/2026-10-11-regression-fixtures/accept-corrected-run.py; docs/qa-logs/2026-10-11-pixelelated-replacement-20/clean-composed-result.json; docs/qa-logs/2026-10-11-pixelelated-replacement-20/upgrade/clean-qualification.json. Delivery is b990d32c93/earlier cited source; exact tracker readbacks are in docs/qa-logs/2026-10-11-pixelelated-replacement-20/tracker-reconciliation.

**Refutation attempted:** Read exact name-set, row-count, separator and result predicates. Failed/missing/duplicate variants are refused. Composer insists original scripts failed exactly as recorded and corrected source/tools match; it cannot merely count table separators or erase original status.

**Notes:** Run-specific acceptance02 ends0, then actual upgrade consumes its sealed receipt. This evidence helper is not claimed as a reusable acceptance gate for future reports.

## Forward audit summary

- PASS: 44
- PARTIAL: 5
- FAIL: 0
- UNTESTABLE: 0
- SKIP: 0

Primary implementation criteria survive the bounded checks; publication scope remains partial. Independent review is adjudicated in04-analysis.md; the four resulting repairs and command evidence are tracked under #554. Publication criteria remain PARTIAL.

## Coverage boundary

Examined:33 changed distribution product/QA files, ES test-double delta, unchanged proxy queue/watcher/schema consumers, original source/target execution receipts and exact frame indexes. Host controls were executed afresh; current-run clean/retained VM evidence was re-read without pretending it ran again. #528 publication obligations remain explicitly partial. Not examined: real achievement-account award/reconnect, hosted OAuth, physical sensor/GPU/panel behavior, complete third-party legal clearance or release-wide source custody. No broader-M7 audit claim.
