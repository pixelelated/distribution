# Forward audit — completed M7 handoff (#603)

**Frozen record:** cdd92f10605517e789e09d13b6f4ba68573c2617. **Contract:** criteria.json (67 literal criteria).

All entries are independent source/original-artifact reads. Existing target execution receipts are inspected directly; no runtime was replayed in this lane. Archive citations use `repository/archive :: exact/member:line`; extracted-members.json binds copies and hashes. Prior per-AC reports stay sequestered through the end of this forward pass.

## Primary packet citation keys

- S602: `docs/qa-logs/2026-10-15-sm8550-abl-format/source/source-packet.tar.gz`, member prefix `source-packet/`.
- A602: `docs/qa-logs/2026-10-15-sm8550-abl-format/accepted/originals.tar.gz`.
- F602: `docs/qa-logs/2026-10-15-sm8550-abl-format/failure/originals.tar.gz`.

A key followed by `::member` names exact original bytes; unless a line is given the whole compact JSON/receipt was read.

### AC-01: Retain the original failed channels and ordinary consumption, actual owner/container exit evidence, and exact upstream-member/package/staged header/hash/size/mode characterization.

**Source:** Issue #602, literal body line 13.
**Written:** 2026-10-15T10:44:02.724102+00:00
**Verdict:** PASS ✓

**Evidence:** A602::failed-producer/runner-result.json and owner/launcher-result.json retain command/monitor/runner1/0/1 and launcher1 at09:00:07. Its admission-consumed.json retains ordinary failed-investigated consumption. A602::failed-producer/investigation.json records exact recorded PIDs gone/container-inspect1; F602::failure-originals/container-inspect.stderr corroborates absence. S602::payload-header-readback.json records unpacked/package/staged258048B,0644,SHA8c27a70961476b327071ada2fd9b9c55dd2dcdc913eff3d33f2576133d7e398c and ELF32/little-endian/EM_ARM40; originals/archive-readback.json binds the official member.

**Refutation attempted:** Searched for rewritten producer0, missing package/staged witnesses, or an ELF64 characterization. Original1, exact three-way identity and the original failing named-member traceback remain.

**Notes:** Historical host observations only; no current process state or native boot is inferred.

### AC-02: Prepare a minimal named-ABL validation branch with fail-closed positive/negative header, digest and unexpected-path controls; preserve the generic userland architecture check and all existing equality checks.

**Source:** Issue #602, literal body line 14.
**Written:** 2026-10-15T10:44:02.724163+00:00
**Verdict:** PASS ✓

**Evidence:** S602::verify-additions.py.diff:1 and templates/verify-additions.py:101 require the one named SM8550 ABL path, device,258048B,exactSHA,ELF32/little-endian/EM_ARM. Generic ELF64/AArch64 remains. format-controls.py, format-controls-result.json and control-invocation.json retain12 actual controls/original0. Wrong digest/size/device/class/endian/magic/machine/path reject; original branch rejects the real member; generic ELF64 succeeds and ELF32 rejects. Full templates/verify-additions.py and templates/acceptance/verify-firmware.py preserve all five source/package/staged/SYSTEM/update/raw equality paths.

**Refutation attempted:** Read the full surrounding mapping and acceptance code. The exemption is exact identity, not a folder-wide relaxation. Inconsistent synthetic header rows are explicitly controls, not artifact receipts.

**Notes:** Existing executed controls inspected directly; no replay or target execution.

### AC-03: Review and run a fresh read-only installed/source reader against the already assembled SM05 artifacts with fresh resources and ordinary admission; retain the failed original producer and actual new result channels separately.

**Source:** Issue #602, literal body line 15.
**Written:** 2026-10-15T10:44:02.724194+00:00
**Verdict:** PASS ✓

**Evidence:** A602::runs/reader/runner-result.json, owner/launcher-result.json and owner/{inner,outer,tool-wrapper}.rc retain all0 for20261015T092225Z-e7702372. runs/reader/admission-consumed.json binds clean9aa7 source, fresh owner and current capacity/retention receipts; eb71b6e5 consumption is09:23:08. owner/reader-consumption.json explicitly preserves producer1. S602::templates/reader.py and prepare-reader.py bind fresh source/verifier inputs to assembled outputs.

**Refutation attempted:** Compared run/owner/admission against failed081827Z; distinct identities and both original result families survive. Read each wrapper result directly instead of inferring zero from a summary.

**Notes:** Source/installed-artifact stage only; no recompilation or native execution claim.

### AC-04: Complete independent raw/update/GPT/five-ABL/FEX/selected-state acceptance and consume its actual original-zero result before dependent runtime. Record exact firmware/source hashes and reconcile #555/#600/#599/M7 with actual completion timestamps; preserve the reporting-order deviation below.

**Source:** Issue #602, literal body line 16.
**Written:** 2026-10-15T10:44:02.724231+00:00
**Verdict:** PASS ✓

**Evidence:** A602::owner/acceptance/verify-firmware.py traces actual raw/update SYSTEM+KERNEL, GPT, five ABL,188ARM,14FEX and48affected mappings. artifacts/{acceptance,payload-equality,partition-table}.json and selected-state.stdout retain actual results(blocked0/error0). runs/acceptance/runner-result.json and owner/acceptance/{launcher-result.json,inner.rc,outer.rc,tool-wrapper.rc} are0. runs/acceptance/admission-consumed.json records40d2d16b consumption09:24:25.904399 after09:23:58.758581 completion. #602 body plus work-log:791 and friction-log:788 preserve the missed original reporting order and later reconciliation.

**Refutation attempted:** Checked that technical acceptance/consumption is separate from failed producer and precedes recorded09:26:39 Steam continuation. The body admits later tracker reporting and retains original wording instead of backdating it.

**Notes:** Current criterion explicitly distinguishes retrospective reporting. Consumer original receipt is also examined under Steam criteria. No physical or publication clearance.

### AC-05: Retain the finite review, evidence and work/friction records. No recompilation, physical operation, new RC or publication clearance is inferred.

**Source:** Issue #602, literal body line 17.
**Written:** 2026-10-15T10:44:02.724254+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-15-sm8550-abl-format/source/{source-packet.tar.gz,review-originals.tar.gz,source-seal.SHA256SUMS,peer-seal.SHA256SUMS,member-manifest.json} retain finite source/control/review inputs. docs/friction-log.md:786,:788 and docs/work-logs/2026_10-work_logs/2026_10_15-work_log.md:735,:760,:791 record failure, correction and reporting deviation. A602::owner/acceptance/artifacts/acceptance.json explicitly limits scope and preserves producer_combined_run_returncode1.

**Refutation attempted:** Read scoped work/friction and acceptance records for invented successful producer, physical operation or clearance. All preserve original failures and outstanding holds.

**Notes:** This criterion verifies review retention; earlier per-AC conclusions remain unopened until Phase2.5.

Additional packet keys: **C600**=`docs/qa-logs/2026-10-15-device-refresh/abl-checksum-fix/originals.tar.gz`; **P599**=`docs/qa-logs/2026-10-15-ppsspp-state-check/originals.tar.gz`; **H599**=`docs/qa-logs/2026-10-15-device-refresh/h70004/originals.tar.gz`.

### AC-06: Preserve original failed channels, owner/container exit evidence and ordinary failed-investigated consumption; keep all prior cache results and no successful build claim.

**Source:** Issue #600, literal body line 17.
**Written:** 2026-10-15T10:46:40.210829+00:00
**Verdict:** PASS ✓

**Evidence:** C600::failed-watch/runner-result.json is2/0/2 at07:23:39.556141; failed-investigation/{00-launcher-result.json,01-tool-wrapper.rc,02-inner.rc,03-outer.rc} retain2. investigation.json and container-inspect records bind actual owners/exact container absence; failed-watch/admission-consumed.json retains failed-investigated outcome. Cache-ready/consumption and original source seal are separately retained.

**Refutation attempted:** Compared original failure to later602 reader failure and successful reader. It remains a distinct checksum refusal before accepted assembly, not relabelled0.

**Notes:** Exact failed originals; no claim that a failed guard was a successful build.

### AC-07: Retain official correction, release/asset metadata and exact local archive digest/member evidence; establish whether a replacement is evidenced and distinguish unrelated current upstream changes.

**Source:** Issue #600, literal body line 18.
**Written:** 2026-10-15T10:46:40.210916+00:00
**Verdict:** PASS ✓

**Evidence:** C600::source-review/upstream-fix.patch is official15123b29517ad92be1f6cbcc3924a92705887d12, one expected-digest replacement. metadata/release-v1.2.json binds asset603983682,1411543B,SHA64034fb076ea0bb858beaa2f29dbef635e97d29f3e3d32c13bce61bd4af4cff7; updated/published October1 metadata and archive-reader/result.json independently match12members,including SM8550 member8c27a709 and companion checksum. execution-observation.json preserves failed first API read and later successful official metadata requests.

**Refutation attempted:** Looked for version/URL/packaging or unrelated OpenABL changes. Actual patch changes only expected digest; current OpenABL metadata is separately retained and excluded. Official archive hash and member evidence agree.

**Notes:** The asset metadata supports the current replacement; it cannot reconstruct old unavailable archive bytes. LinuxLoader source-custody lookup limits stay open under528/601.

### AC-08: Apply only the verified upstream checksum correction; pkgcheck and finite diff/source review pass with unchanged version, URL, packaged files and checksum enforcement.

**Source:** Issue #600, literal body line 19.
**Written:** 2026-10-15T10:46:40.210964+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** Current package SHA6b07c262b11e8cc3fd45e8097b7fdb06a1f612cb31008daafdc3ecf68f892b3c equals retained upstream-fixed recipe; exact supplied git diff changes only checksum. However docs/qa-logs/2026-10-15-device-refresh/abl-checksum-fix/source-commit-readback.json explicitly records independently_executed=false, producer_receipt_retained_here=false and only root_reported_status0 for pkgcheck.

**Refutation attempted:** Read source/readback and searched the scoped checksum packet for pkgcheck. No observed original pkgcheck status was present in that packet. Requested exact existing receipt or bounded root-run check, not a build.

**Notes:** Evidence gap pending root response; source fix is verified but a report alone does not satisfy observed mechanical-check evidence. Preserve this initial assessment if fresh proof later resolves it.

### AC-09: Publish the correction and freeze a new reviewed SM source/owner; explain the exact delta from accepted VM/H700, preserve original failed source/results and bind cache provenance/resources before retry.

**Source:** Issue #600, literal body line 20.
**Written:** 2026-10-15T10:46:40.211008+00:00
**Verdict:** PASS ✓

**Evidence:** Root-supplied git-evidence/vm-sm-product.diff is the one-field checksum delta. source-commit-readback.json binds9aa7. docs/qa-logs/2026-10-15-device-refresh/sm8550-abl-retry-source/publication-originals.tar.gz::evidence.json and e32-hosted-complete.json retain publication ancestry to e32e8c6f and three successful exact-record checks. A602::owner/source-delta.json, cache-parent-baseline.json and original input seal bind prior f863 copy and new9aa7 owner; original cache-ready/consumption remain independent.

**Refutation attempted:** Compared VM/H700f863 and SM9aa7 product diff, actual record publication identities and cache parent. No wholesale upstream intake or proof rebinding to a different product is present.

**Notes:** Publication is source-record publication only; product/RC public distribution holds remain separate.

### AC-10: Complete normal SM8550 build and independent raw/update/GPT/five-ABL/FEX/selected-state acceptance with original results and consumed receipts; update #555/#528/M7 and readiness records.

**Source:** Issue #600, literal body line 21.
**Written:** 2026-10-15T10:46:40.211047+00:00
**Verdict:** PASS ✓

**Evidence:** A602::failed-producer/owner/build.py executes canonical make with check=True before installed verifier; retained failure-context.txt shows verifier reached after image stage and original failing1. A602::owner/acceptance/artifacts/acceptance.json and underlying raw/update/GPT/five-ABL/FEX/selected-state receipts (AC04) qualify assembled9aa7 outputs, all corrected stage originals0 and ordinary consumption. Captured #600/#602 bodies and work-log:760,:791,:806 retain current linked reconciliation.

**Refutation attempted:** Traced whether post-build failure could conceal compiler failure. check=True ordering prevents verifier entry after a failing canonical make, while original trace places failure inside verifier. No combined producer0 is invented.

**Notes:** Normal compilation/image creation completed; combined producer1 is preserved. Separate fresh qualification satisfies artifact scope, not physical boot or release designation.

### AC-11: Retain pinned/upstream PPSSPP parser and account-key evidence, all shipped default-profile syntax characterization, and the original failed reader receipt; distinguish shipped default state from owner data.

**Source:** Issue #599, literal body line 11.
**Written:** 2026-10-15T10:46:40.211089+00:00
**Verdict:** PASS ✓

**Evidence:** P599::source/pinned-source/IniFile.cpp:26-95 and Config.cpp:371-376 identify spaced key syntax, double-quote semantics and actual AchievementsUserName/AchievementsToken. Fourteen shipped-default originals are retained with source inventory. H599::source/originals/failure/12-selected-state.stdout reports blocked0/error1 on PPSSPP; investigation.json preserves native child2 and outer1.

**Refutation attempted:** Looked for owner data being mistaken for defaults or successful acceptance inferred from blocked0. Actual error1 remains; public shipped defaults and pinned component source are explicitly separate.

**Notes:** No inference of personal data from an invalid-input failure.

### AC-12: Accept supported PPSSPP spaced keys in its scoped parser while other configuration formats keep their strict syntax; regression output proves all supported shipped defaults parse without ignoring unexpected lines.

**Source:** Issue #599, literal body line 12.
**Written:** 2026-10-15T10:46:40.211129+00:00
**Verdict:** PASS ✓

**Evidence:** tools/pixelelated-state-check:128-180 applies spaced-key grammar only for kind=ppsspp (OPTIONAL path mapping), keeps other grammar strict, and raises Invalid for unsupported lines/duplicates. P599::runs/03/owner/command.stdout is actual212-control JSON with40PPSSPP cases/all14default profiles; original runner0/0/0 at06:38:46.866576. Current checker65ab515e and suite6e0b2eb9 hashes equal retained source.

**Refutation attempted:** Examined spaces-not-global negative, include/reference/malformed lines, exact duplicate policy and double-quote-only distinction against upstream. No broad skip or parser relaxation outside PPSSPP is present.

**Notes:** Scope is supported strict syntax subset; unknown unsupported syntax fails closed, rather than full PPSSPP parser equivalence.

### AC-13: Detect populated PPSSPP achievement username/token values and opaque account files; preserve conflicting-duplicate, malformed/include, recovery-sibling, privacy-output and retained-storage controls. Exact host suite and focused positive/negative fixture originals pass.

**Source:** Issue #599, literal body line 13.
**Written:** 2026-10-15T10:46:40.211168+00:00
**Verdict:** PASS ✓

**Evidence:** tools/pixelelated-state-check:541-560 adds actual case-insensitive PPSSPP account keys only in achievements; opaque-account path remains in OPTIONAL. tools/pixelelated-state-check-test:390-458 asserts populated username/token, duplicate conflicts both orders, single quotes, recovery siblings, wrong section/spaces, retained/default and format isolation; original212-result records each control with state_unchanged=true. Original prerequisite failures runs01/02 remain2/0/2; run03 is0/0/0.

**Refutation attempted:** Inspected expected error/account classifications in fixture source, not only case names. Empty exact keys pass; populated exact keys and opaque files block. Conflicting duplicates and malformed/includes cannot hide populated values.

**Notes:** Privacy-output controls and retained policy remain; this is selected-state detection, not arbitrary-secret scanning.

### AC-14: A fresh original-zero selected-state read of the exact H700 update archive passes; preserve the earlier failure, bind the corrected host tool separately from unchanged f863 product bytes, and complete fresh independent firmware acceptance. Apply the same bound checker to SM8550 qualification.

**Source:** Issue #599, literal body line 14.
**Written:** 2026-10-15T10:46:40.211210+00:00
**Verdict:** PASS ✓

**Evidence:** H599::owner/artifacts/{acceptance.json,selected-state.stdout} and watch/{runner-result.json,admission-consumed.json} bind unchangedf863,H700DDR3/4,checker65ab515e,blocked0/error0,original0/0/0 and4ebc249f consumption06:48:24.688814. A602::owner/acceptance/artifacts/{acceptance.json,selected-state.stdout} binds9aa7 SM,identical checker and blocked0/error0,original0/0/0 with40d2d16b consumption. The earlier H700 failure and current correction are separate originals.

**Refutation attempted:** Compared actual checker hash, archive/source identity and original results across H700 and SM; inspected original failure error1. No inherited success is substituted for either concrete archive read.

**Notes:** No firmware mutation or whole-image arbitrary-account absence claim; exact selected-state policy only.

### AC-15: Publish the bounded host-tool delta, local Issue review and precise results; update #555/M7 and the work/friction records without rewriting the completed product audit or claiming a new RC/publication clearance.

**Source:** Issue #599, literal body line 15.
**Written:** 2026-10-15T10:46:40.211251+00:00
**Verdict:** PASS ✓

**Evidence:** Root-supplied post-audit history includes8794630e8f host-checker publication; current tool/suite bytes match P599 source. P599 retains source/pinned syntax,40PPSSPP+172other controls and failed prerequisites; local-review.md exists as bounded local review. Work-log:586 and friction-log:775,:777 retain scope/learning; final #599 body names both accepted artifacts and prior failures.

**Refutation attempted:** Verified delta is host tool/suite, not firmware source and that accepted prior audit/product sources retain original identities. Current body explicitly denies RC/publication clearance.

**Notes:** Prior review conclusions remain sequestered; existence/custody and original control results are independently verified.

### AC-08 fresh verification amendment — current verdict PASS ✓

The initial PARTIAL above is preserved. Root allocated one host-only recipe lint. `checks/pkgcheck-current/invocation.json`, `stdout`, and `stderr` retain the actual `tools/pkgcheck rocknix-abl` invocation at 2026-10-15T10:47:08.477596+00:00, completion 10:47:08.591408, exit 0, exact recipe SHA-256 `6b07c262b11e8cc3fd45e8097b7fdb06a1f612cb31008daafdc3ecf68f892b3c`, and checker SHA-256 `dea8addbc2a0a3c3d70da227d2be27f705e7d813ee129d0e43a5781215c04e18`. This is a new independent check, not recovery of a missing historical receipt. The unchanged published recipe now has direct passing lint evidence.

### AC-16: Exact source and before/after frames explain every new claim; update the canonical flow/frame reference without erasing historical evidence.

**Source:** Issue #591, literal body line 17.
**Written:** 2026-10-15T10:53:45.223228+00:00
**Verdict:** PASS ✓

**Evidence:** Direct ES16dbac Settings.cpp:321 sets favorites,recent; CollectionSystemManager.cpp:40,383–387,1291–1296 requires enabled recent and permits empty. Exact original pixel-inventory.json contains78 hash pairs,65 affected frames,348 documented rectangles in proposed-578-background-regions.json. All78 rows have zero outside_carousel_change_support and common_overlay_alpha_nonfit. Viewed original before/after NES carousel and cloud-hub pairs; the narrow left NES sliver and exposed modal backdrop agree with the source-linked claim. docs/es-menu-map.md:953 records this exact flow without baseline replacement.

**Refutation attempted:** Inspected source that could make an empty recent collection an unintended fixture effect; it is explicitly displayIfEmpty and enabled by the corrected default. The foreground labels and NES title are outside the new background claims. Original review.txt is a source/diagnosis artifact, not a prior audit verdict.

**Notes:** Visual sampling was two exact pairs, not all78; all78 numerical diagnosis records were inspected. Historical foreground claims retain their original limits.

### AC-17: Adjacent independently claimed regions pass while a single uncovered changed pixel, stale claim, missing screen or unclaimed dimension change still fails; retain original control outputs.

**Source:** Issue #591, literal body line 18.
**Written:** 2026-10-15T10:53:45.223392+00:00
**Verdict:** PASS ✓

**Evidence:** tools/frame-diff:168–220,279–352 assigns each changed unmasked pixel to the first matching live claim and clusters only remaining pixels. controls-result.json has20 original expected/actual outcomes; old-control-result.json retains old adjacent-case child1; execution retains wrapper0, candidate-controls0 with exact arguments.

**Refutation attempted:** Uncovered connector, bounding rectangle gap, stale/mixed claims, wrongscreen, missing screen, dimensional change, half-open edges and foreground-label controls all retain child1; overlapping covered pixels count once. NEW screens still need one whole claim. Default minimum remains1.

**Notes:** No new comparator execution; direct original control receipts and code inspected.

### AC-18: The original78 retained VM frame pairs pass the corrected comparison with narrow documented claims and no new blanket mask or baseline replacement; original failure stays unchanged.

**Source:** Issue #591, literal body line 19.
**Written:** 2026-10-15T10:53:45.223456+00:00
**Verdict:** PASS ✓

**Evidence:** execution/retained-comparison.json records original child0,11.7498s, timeoutfalse against the same retained78-frame run, original baseline and unchanged mask SHA64c817d443a15585e194451772424e89ffcb7ad64f83aa3d2b799f0ecbb63a00. continuation01.md actual terminal line:389 claimed,0unclaimed,0missing. Original failure65unclaimed remains recorded and original baseline02 packet retained.

**Refutation attempted:** Actual argv has compare, no accept or minimum-pixel override. prepare_claims.py composes only baseline-specific per-screen regions and preserves old claims. No mask mutation or baseline promotion is present.

**Notes:** Passing comparison is separate from original failed aggregate; it does not recast the original result.

### AC-19: Record the actual matcher/claim/source identities, original result channels and remaining limits in M7 qualification evidence.

**Source:** Issue #591, literal body line 20.
**Written:** 2026-10-15T10:53:45.223505+00:00
**Verdict:** PASS ✓

**Evidence:** handoff-hashes.json and execution/inputs.json bind matcher49cdaf5275dceef5ae3bfa06f71c4adb7f35a3b285abf9b1200f0323fec57330, controls96631be5bee6881a8dd83bc8e0c60f258fc276586c87b1027c20bfe39458de79, composedclaims7764b6824a8489b1e22d793ac8adcbf90b559d3235e9d65189c55e618101cf5e; execution/result.json retains all three actual stages0 with inputs_unchangedtrue; original-packet watcher terminal0.

**Refutation attempted:** The earlier source-only UNRUN handoff was not treated as execution. Only later execution receipts establish comparison/control completion.

**Notes:** Historical source and frame references remain fac608ff/3178b832; no claim of a new VM run or arbitrary UI behavior.

### AC-20: Preserve the original seven failures and exact source/process evidence in a compact published packet; identify exited adopted children separately from live work.

**Source:** Issue #589, literal body line 13.
**Written:** 2026-10-15T10:53:45.223552+00:00
**Verdict:** PASS ✓

**Evidence:** baseline-correction.tar.gz/evidence/original-scripts.log retains7 CHECK(S) FAILED,0SKIPPED, including six liveness failures and empty PL016 text; original-host-proc.json separately retains four exited zombie identities. baseline02 original-records retains original process identities and scripts log.

**Refutation attempted:** Read actual seven failure lines and process census. Four PID-backed zombie cases are direct evidence; the other two same-cause explanations are inference, not invented process records.

**Notes:** Original failed run remains failed; no product behavior was inferred from kill-0 alone.

### AC-21: Correct observation-time reaping without consuming the active Popen wait or signaling live descendants; preserve original adopted wait statuses and normal cleanup evidence.

**Source:** Issue #589, literal body line 14.
**Written:** 2026-10-15T10:53:45.223602+00:00
**Verdict:** PASS ✓

**Evidence:** baseline-correction/run.py.diff changes observe(active) to nonblocking waitpid(WNOHANG) for direct adopted children, explicitly skipping active.pid. Fresh baseline-continuation/result.json records71 observation reaps with statuses[-15,-9,0,143,255]; none overlap commanded active PIDs.72 total reaped entries includes final cleanup.

**Refutation attempted:** Direct code preserves Popen poll/wait ownership and sends no signals in observation. Actual cleanup_errors, remaining_children, surviving_owned_processes and qemu_still_live are empty; host-exits records original seven channels0 and OWNERS_GONE.

**Notes:** Do not count final cleanup as an observation reap; negative child statuses remain negative.

### AC-22: Read PL-016 waiting prose from the current status-message element with the historical-template fallback; retain the assertion that the text is nonempty and does not name an absent button.

**Source:** Issue #589, literal body line 15.
**Written:** 2026-10-15T10:53:45.223649+00:00
**Verdict:** PASS ✓

**Evidence:** baseline-correction/last-good-scripts-test.diff chooses byId[status-message] || byId.state, then retains waiting.length>0 and absence of send button. The actual fresh scripts.log ends PASSED and original empty-text failure remains retained.

**Refutation attempted:** Read precise assertion: fallback changes lookup only; neither empty string nor a nonexistent-button instruction is accepted.

**Notes:** Historical template fallback is retained; no product source change required.

### AC-23: Run the existing scripts row on the same frozen image under a fresh watched owner; retain its original PASS result and actual owner cleanup. Carry the other successful same-image standard rows without repeating them. Complete the separately pending SFTP and local S3 rows under #344.

**Source:** Issue #589, literal body line 16.
**Written:** 2026-10-15T10:53:45.223692+00:00
**Verdict:** PASS ✓

**Evidence:** baseline-continuation/original-records.tar.gz image-inputs.original.json binds same fac608ff image d816d36abc66b292500b0719e672c98c33eb0cd4fc7fc0bf19f7e26e4108bb16 and ES3178b832. Three actual report.md originals show scripts PASS521s, SFTP roundtrip PASS67s and S3 PASS111s. runner-result has command/monitor/runner0 at00:21:39; host-exits all seven channels0 and owners gone.

**Refutation attempted:** Fresh owner runs only scripts and the two pending backend rows; prior successful rows are carried, not claimed rerun. Original scripts log explicitly says one historical feature group N/A and no checks counted PASS. Cleanup lists empty and backend absent.

**Notes:** These receipts close the retained-baseline correction, not a new full final-image qualification.

### AC-24: Exact source/current-upstream comparison and raw-setting/listener contract are recorded, including explicit contribution disposition.

**Source:** Issue #584, literal body line 29.
**Written:** 2026-10-15T10:57:03.448175+00:00
**Verdict:** PASS ✓

**Evidence:** Captured raw research/rocknix-3038.json and proxy-50.json under2026-10-14-dolphin-proxy-routing-source identify merged customhost and upstream CLI patching behavior; receipts.json binds exact calls/time/hash at02:49UTC. Current helper reads customhost but additionally gates the distro run-service path with raw toggle/hardcore/listener. docs/upstream/README.md and raofflineproxy/contribution-map.md separately retain deferred #585 contribution disposition.

**Refutation attempted:** Upstream customhost support alone does not select this distro offline toggle or patch run-service; existing support was not claimed absent. No live upstream lookup or submission performed.

**Notes:** Comparison is frozen October14 captured evidence, not a statement about future upstream state.

### AC-25: A minimal launcher change routes only the enabled, non-hardcore, verified-listener case and preserves fallback customhost behavior.

**Source:** Issue #584, literal body line 30.
**Written:** 2026-10-15T10:57:03.448365+00:00
**Verdict:** PASS ✓

**Evidence:** Read full shipped cheevos_dolphin.sh. Only saved offlineproxy==1, hardcore_raw==0 and proxy_listening status0 changes hosturl to127.0.0.1:8080. Predicate accepts listening IPv4 loopback/wildcard or mappedIPv4 at1F90 and rejects IPv6-only. Disabled/no-token publishes inactive credentials atomically; saved settings are read-only.

**Refutation attempted:** Unknown/empty hardcore becomes displayFalse but raw gate still rejects proxy routing. Missing/unreadable listener leaves configured customhost. Listener presence expressly does not authenticate service or readiness.

**Notes:** Later #594 inactive publication is part of final composition; no personal credentials read.

### AC-26: Synthetic VM full-script controls cover toggle0/1, hardcore0/1/empty/unknown, customhost empty/nonempty, IPv4/mapped IPv6/IPv6-only/unreadable tables, missing token and disabled achievements; receipt verifies generated INI and unchanged input settings.

**Source:** Issue #584, literal body line 31.
**Written:** 2026-10-15T10:57:03.448448+00:00
**Verdict:** PASS ✓

**Evidence:** Original routing-result.json contains126 before/after full-script cases, all PASS;11or13 protected files unchanged; actual guest Bash/cat identities recorded. Table inputs cover empty/established/IPv4/loopback6/mapped6/missing/other-address/unreadable/wildcard4/wildcard6/wrongport; raw gates and early-disabled/missing-token branches retained. No remaining children/signals/observation errors.

**Refutation attempted:** Verified complete case arrays rather than summary count; per-case original exits and INI digests remain distinguishable from harness PASS. Original initial fixture error remains in packet.

**Notes:** Synthetic routing/configuration proof, not live account authentication.

### AC-27: Installed dependency/service and Dolphin host interpretation are verified; distinguish configuration proof from full offline login/cache/award/reconnect behavior.

**Source:** Issue #584, literal body line 32.
**Written:** 2026-10-15T10:57:03.448517+00:00
**Verdict:** PASS ✓

**Evidence:** Installed startup original-results.tar.gz payload records actual raofflineproxy.service run-service, installed identity unchanged, original child0, empty cleanup and inactive final service, preserved signed queue/worker shutdown and natural next15s reconnect probe. Installed Dolphin case-result.json binds binary5cb5dacafbcd2227627ef687a65318e61890ef343e5c6553f07c0fb11231fea5: enabled init1/request1/shutdown1, disabled0/0/0, failedboot original1 with init/shutdown1; all badge-load errors0. Read018-nogui-achievements-lifecycle.patch ScopeGuard ordering.

**Refutation attempted:** Exact HTTP POST is login2 to127.0.0.1:8080 with synthetic invalid identity; this establishes HostUrl interpretation, not successful authentication/award. Installed proxy result retains source_pins_verifiedfalse historical boundary and its separate actual installed identity binding.

**Notes:** Final clean/retained original affected exports bind same final helper01473794 and recipe-transformed launchers; four cases each retain23 protected files and no temporary credentials. They use explicit engine markers, not emulator login.

### AC-28: Canonical flow/limitations and combined #574/#583 qualification reflect the tested behavior before the next candidate.

**Source:** Issue #584, literal body line 33.
**Written:** 2026-10-15T10:57:03.448572+00:00
**Verdict:** PASS ✓

**Evidence:** docs/es-menu-map.md:835–864 names raw route predicate, inactive publication, original126 configuration cases, separate installed native lifecycle and explicit no-account-award limits. Current #574/#584 bodies bind finalf863/ES16dbac while retaining original failures and subsequent provenance correction.

**Refutation attempted:** Checked canonical language does not turn service startup into successful account login or native game awards; exact native exit1 remains1. Earlier unchanged ES presentation remains source-bound; new #594 refusal presentation is separate.

**Notes:** Combined hashing/format proof is reviewed separately underAC56–59; no blanket runtime pass inferred here.

### AC-29: Preserve old-source failed decoder/function exits, before/after manifests and the one deliberate retry showing incomplete state skipped as installed; separately prove valid existing-client preservation.

**Source:** Issue #582, literal body line 29.
**Written:** 2026-10-15T10:58:59.737407+00:00
**Verdict:** PASS ✓

**Evidence:** 2026-10-14-offline-components/guest/steam-partial02-result.json records exact old installer a7a67c6b…, original client-function exits[1,0], all preexisting entries preserved and zero descendants; steam-existing01-result.json records separate valid-client control0. Both bind actual guest Bash and BusyBox decoder.

**Refutation attempted:** The wrapper PASS labels successful reproduction; it does not relabel failed decoder/function1 or misleading retry0 as repaired behavior. Original earlier partial fixture failure remains archived.

**Notes:** Old function-only reproduction, distinct from later complete caller.

### AC-30: Missing/incomplete state cannot report installed. Exact-source controls preserve valid client/channel/aliases/custom files and refuse ambiguous existing layouts before writes.

**Source:** Issue #582, literal body line 30.
**Written:** 2026-10-15T10:58:59.737604+00:00
**Verdict:** PASS ✓

**Evidence:** Current Install Steam.sh:1332–1376 bootstrap validates four bounded ARM64 ELF headers/program segments;1570–1595 rejects partial legacy siblings and unknown staging.1661–1696 preserves existing channel/alias/custom types and requires fresh conflicts to refuse. Original remaining14 cases06–09 retain installer1; valid existing/alias/profile/self-updated cases retain0 and all13–18 protected entriestrue.

**Refutation attempted:** A directory or marker alone cannot pass bootstrap; missing core and partial-before-profile original controls fail before setup writes. Existing self-update bytes are not compared to old content hashes; structural inspection preserves them.

**Notes:** Structural bootstrap acceptance is not native readiness or genuine self-update execution.

### AC-31: Failure/interruption controls for acquisition, extraction, validation, activation and metadata preserve existing client/SDK and unrelated runtime/FEX/Proton/library/game/save entries. Fresh failure leaves no misleading installed state.

**Source:** Issue #582, literal body line 31.
**Written:** 2026-10-15T10:58:59.737698+00:00
**Verdict:** PASS ✓

**Evidence:** Direct transaction source1887–2364 binds stage/root/journal identities, journals transfers/external intents, checks ownership before removal, exclusively publishes and retains unknown/uncommitted changed state. Original continuation cases10–14 each retain[1,0], all protected roots true and descendants empty. Targeted census-error retains[1,1]; timeout[1]; interrupt-published and committed-self-update[1,0]; CRC corrected-events[1,0].

**Refutation attempted:** Original targeted attempt01 and CRC attempt10 remain FAIL. Unknown census or transfer quiescence cannot authorize cleanup. Nonempty directories are removed only with rmdir and exact recorded inode; entire Steam root never removed. Interrupted published client is verified before commit/recovery.

**Notes:** Synthetic signal interruption and committed-update controls do not establish sudden-power durability or real consumer quiescence.

### AC-33: Review repaired full-caller fresh, retained and allowed-alias VM receipts against exact source; record installed-image, native ARM64/self-update/quiescence and power-loss limits explicitly before closure.

**Source:** Issue #582, literal body line 33.
**Written:** 2026-10-15T10:58:59.737774+00:00
**Verdict:** PASS ✓

**Evidence:** Read full-client ownership, transfer, extraction, metadata and recovery source plus original9 targeted accepted cases and14 continuation receipts. Final selected-artifact bridge fixture-records/result.json binds124399-byte module1694f7a9b892988a67a3445c8f51031c5a5c8be02628b0be8031f233b512ad3b (current source samehash), complete caller0, all18 protected rootstrue, no descendants, native execution explicitly DENIED.

**Refutation attempted:** Prior source-only qa/source.json remains UNRUN historical input; separate later result establishes execution. GENERIC_X64 executes transported unchanged packaged script using actual installed interpreter/tools and synthetic boundaries; it does not ship this ARM module.

**Notes:** Native ARM64, real Steam self-update/consumer quiescence and abrupt-power behavior remain unproved as current issue explicitly states; no RC approval.

### AC-32: Establish real archive layout and owned paths; verify finite transport/decompression/space limits, owned staging cleanup and deterministic retry. Never replace or delete the whole Steam root.

**Source:** Issue #582, literal body line 32.
**Written:** 2026-10-15T10:59:53.262830+00:00
**Verdict:** PASS ✓

**Evidence:** Actual evidence/steam-inspection.json SHA f2fd32e894124470f68f68193ba2b6225f8e3b45fc3ca1a14051055d316bd0a6 records55 members, archive8b31d0b0…110373661bytes,339635561decodedbytes, required ELF structure PASS and0created files/links/executed payloads; original transport0. Current decoder1968–2090 enforces exact55canonical names, supported ZIP headers/attributes, CRC/length, bounded deflate,128MiBZIP/384MiBexpanded/128MiBmember,90sdecode and360soverall. transfer1833–1873 enforces HTTPS,10sconnect,30smanifest/180sarchive,resource limit and65KiBstderr.

**Refutation attempted:** Contract proposal alone was not accepted as runtime; inspected separately retained original receipt. Activation uses RENAME_NOREPLACE, metadata preserves preexisting paths, exact identity cleanup removes only owned nodes; fresh ambiguous metadata refuses. Signature authentication and external dependency/native readiness remain explicitly unproved.

**Notes:** No real archive bytes executed by this audit or historical inspector; deterministic retry supported within documented ownership journal states.

### AC-34: Reproduce and preserve the original source's retained-directory failure in an allocated disposable fixture; bind both exact launcher sources and file/type/hash inventories.

**Source:** Issue #581, literal body line 24.
**Written:** 2026-10-15T11:01:25.710996+00:00
**Verdict:** PASS ✓

**Evidence:** dolphin-results/baseline-receipts.tar.gz result.json retains8 original preservation failures: real StateSaves,GC region/card conflict/shared data for GC/Wii. Exact old launcher hashes e2888606…/b6cedc30…; fragments exit0 but preservation assertions1 and engine marker1. Retained path/file inventories identify actual lost synthetic bytes.

**Refutation attempted:** A successful launcher exit did not mean preservation. Original baseline failures are explicitly EXPECTED_BASELINE_FAILURE, separate from candidate results; no owner save-loss attribution is inferred.

**Notes:** Disposable source-fragment reproduction only, not native save behavior.

### AC-35: Repair preparation so retained real save/state data, existing canonical data, conflicting names and unrelated targets survive. Preserve valid current symlinks, including intentional GameCube/Wii state-link switching. Any ambiguous conversion fails without deleting data and gives an actionable outcome.

**Source:** Issue #581, literal body line 25.
**Written:** 2026-10-15T11:01:25.711183+00:00
**Verdict:** PASS ✓

**Evidence:** Read complete346-line dolphin-save-paths: plan rejects real source paths/conflicting cards/unknown links before writes, recognizes GC↔Wii state symlink destinations, rejects nested mounts and unwritable roots. Copy is absent-target only with bounded resources/RENAME_NOREPLACE; state switch RENAME_EXCHANGE retains unexpected displaced objects. Actual mounted eight-case receipts preserve each preexisting before/after byte/inode/mode entry; six synthetic card writes through links retained.

**Refutation attempted:** Real or even equal-looking retained data is refused, not guessed-owned; only exact private staging inode can be recursively removed and no saved canonical path is deleted. Unexpected concurrent contents remain for explicit recovery.

**Notes:** Does not reconstruct historical data already lost; supports known paths, not arbitrary hostile concurrent mutation.

### AC-36: Exercise fresh, retained, existing/dangling/unexpected links, conflicts, unavailable/unwritable destination and interrupted preparation; assertions cover original bytes/types, no follow-through deletion and no emulator launch after a refused preparation.

**Source:** Issue #581, literal body line 26.
**Written:** 2026-10-15T11:01:25.711266+00:00
**Verdict:** PASS ✓

**Evidence:** Candidate originals104 helper cases plus6 launcher guards and13 native-error ownership cases all retain original expected results. Actual mounted controls cover fresh,systemswitch,retainedreal,nestedmount,readonly and absentmount. Interrupted cases preserve SIGKILL-9 or refusal250; killed copy retry250, recognized state-link interrupted retries0. Complete v4 caller originals retain refusal250/enginecalls0 and success0/enginecalls1 with all assertions true.

**Refutation attempted:** Checked actual original helper/launcher statuses, no-follow-through guards and nonlaunch assertions, not only aggregate PASS. Failed first fixture and incomplete historical cases stay in original packets.

**Notes:** Engine calls in these controls are recording markers; ordinary and native state behavior separately reviewed.

### AC-37: Verify installed script/package identity, clean and retained upgrade paths, and any changed player-facing copy with canonical flow and exact-source frames before promotion. Keep ordinary saves, native states and frontend manager eligibility distinct.

**Source:** Issue #581, literal body line 27.
**Written:** 2026-10-15T11:01:25.711326+00:00
**Verdict:** PASS ✓

**Evidence:** Final clean original records/final-result.json maps helper507ccc96245bfc7aaca5e154ef0567cacccd0cbc9d0f999761d2fdee1fc245e8 and transformed GCdd2cb058/Wii08fccbde launchers to exactf863 source. Final clean/retained VM channels all0, retained previous d6a/updatef863 tar1e00415c… and original lifecycle/cleanup retained. Canonical docs/es-menu-map.md:379 maps staged EN/FR1280 and later640 refusal/return frames; independently viewed actual FR retained-state refusal and EN return.

**Refutation attempted:** Historical frame ESbb9e/staged callers were not renamed final installed proof. Later source verifier and actual clean/retained receipts provide continuity. Ordinary saves, native manual/auto states and frontend-manager eligibility remain explicitly separate.

**Notes:** Two frames visually sampled here; all index identities/caller assertions checked. Broader native proof reviewed underAC52–55.

### AC-38: Exact-source synthetic controls retain original exits and manifests for failed download/extraction and incomplete existing destination.

**Source:** Issue #580, literal body line 42.
**Written:** 2026-10-15T11:04:04.721527+00:00
**Verdict:** PASS ✓

**Evidence:** Original steam-results component Proton56 cases retain download/extract failure1 with retries0, incomplete-existing1 and before/after manifests. Direct read of download-failure manifests shows every preexisting entry unchanged; only persistent lock added. Exact source helper5513e6cd…/stdin18d2bed3… matches final.

**Refutation attempted:** Corrupt/footer/traversal/escaping-link/specialfile/wrongELF failures all retain1; current target existence invokes payload validation rather than blind success. Original combined FEX failure does not invalidate independently recorded Proton suite0, but combined report remains FAIL.

**Notes:** Synthetic component receipts, later full-caller evidence separate.

### AC-39: Stage and validate the requested variant before activation or retirement; failures/interruption preserve the usable previous variant and successful replacement has a validated manifest/required payload.

**Source:** Issue #580, literal body line 43.
**Written:** 2026-10-15T11:04:04.721671+00:00
**Verdict:** PASS ✓

**Evidence:** Current Install Steam.sh:2470–2644 validates required manifests, executable Wine/wineserver ARM64 headers and confined paths before activation. Full compressed footer read and member validation precede staging extraction; renameat2NOREPLACE protects existing target. Original56case array covers activation failure/race,kill-download/extracted/activated-9 and retries0,complete-existing0,wrongpayload1.

**Refutation attempted:** Existing versions in both families are retained even after success; no broad old-version cleanup. An incomplete same-name destination is preserved/refused, never erased as retry cleanup.

**Notes:** Usable here means required payload/manifest contract, not native Proton game execution.

### AC-40: Retry and space/time bounds use one owned staging area, respect distinct Proton families and preserve all game/save/client data; receipts prove cleanup scope.

**Source:** Issue #580, literal body line 44.
**Written:** 2026-10-15T11:04:04.721743+00:00
**Verdict:** PASS ✓

**Evidence:** Single .proton-variant work path binds owner hardlink to persistent locked inode; cleanup rejects unknown children,symlink/mount ownership. Source bounds2GiBarchive,16GiBexpanded,250000members,900sdownload and whole alarm; original controls cover lowspace before download/extract,member/outputbounds,concurrency,unknownstage,familysequence and cleanup failure/retry.

**Refutation attempted:** Before/download-failure after manifests preserve client,game/save and both previous families. Source keeps old target unmodified and removes only recognized work; two-family successful sequence preserved.

**Notes:** Synthetic interruption does not prove abrupt power durability; explicit nonnative limit retained.

### AC-41: Candidate-source installed VM proof and review are linked before #563 acceptance; native Proton/Steam usability is separately identified.

**Source:** Issue #580, literal body line 45.
**Written:** 2026-10-15T11:04:04.721808+00:00
**Verdict:** PASS ✓

**Evidence:** Final selected-artifact bridge original fixture-records/result.json binds unchanged module1694f7a9… and embedded helper stdin hashes (FEX2381da57…,runtime1c6edbf4…,Proton18d2bed3… independently recomputed). Full caller original0,18protected rootstrue, descendants empty. Native execution denial returns EACCES13/child126 within the synthetic route; no native qualification. Current #580 body and completed #563-linked bridge distinguish transported module behavior from selected SM8550 artifact acceptance.

**Refutation attempted:** Source-only input manifests were not graded as execution; actual bridge fixture and host completion consumption carry it. No GENERIC_X64 native ARM installation claimed.

**Notes:** No public release/RC/native usability approval follows.

### AC-42: Exact-source synthetic failing control records original exits and before/after manifests for failed download/extraction or missing required overlay; distinguish source reasoning from executed reproduction.

**Source:** Issue #579, literal body line 32.
**Written:** 2026-10-15T11:04:04.721868+00:00
**Verdict:** PASS ✓

**Evidence:** Corrected FEX compact-receipts result retains baseline-download/extract/overlay original1 and actual before/after manifests, source9e1ce7b…; baseline download reduces17paths to16. Original combined FEX suite1 and incomplete guardian record remain. Separate corrected FEX suite0 has43verified case exits.

**Refutation attempted:** Source reasoning alone was not used; actual baseline expected-destructive flag and missing prior runtime entry were inspected. Corrected null-sink fixture did not rewrite failed original.

**Notes:** Synthetic component reproduction with actual guest interpreter.

### AC-43: Staged validated replacement preserves the prior complete environment and required files on download, extraction, validation, activation and interruption failure; manifests and retry receipts prove it.

**Source:** Issue #579, literal body line 33.
**Written:** 2026-10-15T11:04:04.721929+00:00
**Verdict:** PASS ✓

**Evidence:** Read FexUpdate.stage/recover/activate: separate RootFS+config staging, four required overlays,validation and old/new identities; prepared journal precedes each rename, previous root/config restored on failure, committed state validated before retirement. Original failure/activation/kill cases retain1/-9 and recovery0/retry0. Direct before==after_recovery checks true for fetch-error,activation-error4,kill-rename2.

**Refutation attempted:** Nonzero fetch,exit0-noextract,unexpectedrootfs,missingoverlay,wrongELF,configcopy,ENOSPC and four activation errors are distinct controls; foreign live identity refuses cleanup.

**Notes:** Controlled process interruption, not real sudden-power proof.

### AC-44: Space/time bounds, owned cleanup and recovery are verified without touching Steam games/saves or unrelated FEX roots. Existing intended RootFS refresh remains supported.

**Source:** Issue #579, literal body line 34.
**Written:** 2026-10-15T11:04:04.722001+00:00
**Verdict:** PASS ✓

**Evidence:** Source FEX limits2GiBfile,16GiBtree,64MiBconfig,250000entries,256MiBreserve,900sfetch/1800stotal. Guardian owns inherited lock, observes pipe EOF, kills/waits known fetch group before recovery.43corrected controls include timeout,ownerKILL/TERM,guardnonzero and unknownjournal/foreignlive refusal. Existing fresh/refreshsuccess0 retained.

**Refutation attempted:** Other-root,similar-root,existingarchive and Steam sentinels are present in before/after manifests; staged fetch uses isolated HOME/config/data. No glob cleanup of unrelated RootFS paths.

**Notes:** Guardian signals recorded owned synthetic children only; no new execution in this audit.

### AC-45: Candidate-source installed VM proof and review are linked before #563 acceptance; native execution limits are explicit.

**Source:** Issue #579, literal body line 35.
**Written:** 2026-10-15T11:04:04.722060+00:00
**Verdict:** PASS ✓

**Evidence:** Final selected-artifact bridge original fixture-records/result.json binds unchanged module1694f7a9… and embedded helper stdin hashes (FEX2381da57…,runtime1c6edbf4…,Proton18d2bed3… independently recomputed). Full caller original0,18protected rootstrue, descendants empty. Native execution denial returns EACCES13/child126 within the synthetic route; no native qualification. Original complete caller records expected nine-helper ordering and installed-tool identities; original component failures and later successful bridge distinct.

**Refutation attempted:** Native FEX dependency/emulator usability is not established by transported script plus synthetic fetcher; current body explicitly limits that claim.

**Notes:** Selected SM8550 module custody is independently closed by AC01–10, without turning GENERIC_X64 into an ARM run.

### AC-60: A source-bound failing control shows the new function loses the prior runtime on download failure while the accepted predecessor preserves it.

**Source:** Issue #564, literal body line 42.
**Written:** 2026-10-15T11:04:04.722119+00:00
**Verdict:** PASS ✓

**Evidence:** Original2026-10-12-upstream-adoption/steam-failure-control.json binds predecessor source20f23b8…/function05f85cb… and stable20261001sourceb88672…/function82c3e994…. Both actual exits1; predecessor working_runtime_preservedtrue,adoptedfunctionfalse.

**Refutation attempted:** Receipt expressly labels adapted host/no-network control and installed VM pending at that historical point; no host fixture was upgraded to VM evidence. Later39runtimeVM cases supply repaired behavior.

**Notes:** The criterion asks source-bound failing control; that original remains intact.

### AC-61: A staged replacement preserves the complete working runtime and library links on download, extraction, validation and activation failure; successful replacement retires superseded runtime only after the new one is usable. Original return codes and before/after manifests prove each case.

**Source:** Issue #564, literal body line 43.
**Written:** 2026-10-15T11:04:04.722180+00:00
**Verdict:** PASS ✓

**Evidence:** RuntimeUpdate:878–1045 stages runtime, saves both library aliases/files and complete prepared rollback description before renames; validates candidate and final links before committed journal permits cleanup.39original cases retain failures1 for download/extract/missinglibs/wrongELF/backup/oldnew/linkrename/validation; actual download-failure before and after-first dictionaries identical.

**Refutation attempted:** Old runtime is restored by identity, unexpected live or link modifications retain recovery data. Success and firstinstall0; old directory removed only after validated committed state.

**Notes:** Payload usability contract is structural; actual ARM runtime not executed here.

### AC-62: Interruption/retry recovery and available-space handling are bounded, and saves/games outside the runtime are unchanged in VM fixtures.

**Source:** Issue #564, literal body line 44.
**Written:** 2026-10-15T11:04:04.722239+00:00
**Verdict:** PASS ✓

**Evidence:** Runtime39case originals include SIGKILL-9 at staging,old/new rename,each librarylink,commit; retry original1 preserved for intentionally failing next download while rollback state remains correct. Source locks persistent inode, bounds2GiBarchive/16GiBexpanded/250000members, capacity/reserve and900sdownload/1800stotal; cleanup checks mounts and known recovery identity.

**Refutation attempted:** Retry1 is not reported as successful installation; preservation/recovery assertions distinguish restored old state from later failed acquisition. Unrelated client,Proton,games and saves remain in original manifests.

**Notes:** No uncontrolled power-loss/disk-full durability claim.

### AC-63: New-source installed VM proof and review are recorded before #563's changed image is accepted. User-facing flow/copy evidence is updated if presentation changes.

**Source:** Issue #564, literal body line 45.
**Written:** 2026-10-15T11:04:04.722301+00:00
**Verdict:** PASS ✓

**Evidence:** Final selected-artifact bridge original fixture-records/result.json binds unchanged module1694f7a9… and embedded helper stdin hashes (FEX2381da57…,runtime1c6edbf4…,Proton18d2bed3… independently recomputed). Full caller original0,18protected rootstrue, descendants empty. Native execution denial returns EACCES13/child126 within the synthetic route; no native qualification. Current #564 body links original baseline regression,39component cases and final bridge before changed-image completion; module1694… matches accepted SM SYSTEM source binding.

**Refutation attempted:** Existing command-line/module flow remains; bridge uses a recording transport and rejects native client execution. Earlier wrapper successes do not overwrite installernegative exits or unknown census.

**Notes:** No new UI flow introduced by this preservation repair; claimed runtime flow is the actual staged installer chain.

### AC-46: Same-source VM frame sequences show unchanged dialog/list/footer bounds before, during and after initial/refresh scans, with search status within the list area; cover 640×480 and 1280×800, English and French.

**Source:** Issue #577, literal body line 49.
**Written:** 2026-10-15T11:10:50.689823+00:00
**Verdict:** PASS

**Evidence:** GuiWifi.cpp39–187 fixes menu/list/status geometry once; setup-qualification/installed/results/wifi-{en,fr}{640,1280}-{initial,branches}/result.json original rc0, unchanged frontend identity. Selected frame index binds a7dc source and f6fd61 binary. Directly viewed French640 initial/results and English1280 pending frames; same title/list/footer bounds and in-list search. Subsequent bb9e French matrix and final ES16dbac frames remain separately bound.

**Refutation attempted:** Compared pending/result geometry and old short-dialog baseline; did not treat historical untranslated French hint as final copy. Fixed dimensions and reserved two-line status explain stable placement.

**Notes:** Synthetic enumeration and render proof, not physical radio. Exact-source sequences are component proof; final clean/retained lifecycle/installed binding separately recorded below.

### AC-47: The delayed initial scan has an in-list searching state; a delayed refresh preserves the last list and safe focus. Completed zero results and failed scans have distinct outcomes and an actionable retry, proved by fixture transcript and reviewed branch frames.

**Source:** Issue #577, literal body line 50.
**Written:** 2026-10-15T11:10:50.690024+00:00
**Verdict:** PASS

**Evidence:** GuiWifi.cpp preserves prior rows while pending and distinguishes successful empty from failed enumeration. Original four locale/size branches record failed enumeration retaining rows, successful zero replacing rows, duplicate refresh blocked. Directly viewed French640 failure (prior results shown with retry) and empty (no networks) frames; refresh remains visible. Installed wifi-followup original scan exits0,8,0 prove actual backend propagation/retry.

**Refutation attempted:** Challenged false-empty conflation and stale-row activation. Pending action guards reject selection/manual input; failure retains known rows, distinct status, and retry. Prior failed controller-as-keyboard fixture remains rc1.

**Notes:** No account or real-radio assertion.

### AC-48: A long list scrolls within the stable viewport without clipping the buttons; repeat refresh preserves the selected network when present and deterministically selects a valid row when it disappears, proved by input walk and frames.

**Source:** Issue #577, literal body line 51.
**Written:** 2026-10-15T11:10:50.690143+00:00
**Verdict:** PASS

**Evidence:** GuiWifi.cpp load path retains unchanged list/scroll and restores selected SSID when present; otherwise clamps former row index and gives refresh focus for empty results. All four original long-list branch walks rc0. Direct French640 long-scroll completion shows list within viewport and footer visible. wifi-remaining original disappearance continuation chooses QA network02 deterministically.

**Refutation attempted:** Examined same-result shortcut and missing-selection fallback; empty list cannot retain an invalid selectable row. The visible partially clipped upper scroll row is within list viewport and does not clip footer controls.

**Notes:** Evidence proves defined synthetic long-list/selection cases; no blanket arbitrary-list claim.

### AC-49: Repeated refresh, back/exit during a pending scan, late completion and retry do not duplicate jobs, access a destroyed screen or activate stale rows; bounded fixture transcript records the outcome and all worker exits.

**Source:** Issue #577, literal body line 52.
**Written:** 2026-10-15T11:10:50.690252+00:00
**Verdict:** PASS

**Evidence:** WifiScanProcess.h and GuiWifi shared process-owned worker have bounded output/time, group ownership, cancellation/join and no worker capture of screen this. main.cpp calls shutdownScans. Original normal-exit controls: baseline driver0 but observer1 with two surviving children; candidate explicit/atexit/complete observers0, no forced cleanup. Original Back timing0.059060466s and reopen same PGID/one enumeration. Final clean/retained wifi-candidate/result.json installed ES76f18d97... driver/observer/final0, one stop/join, unchanged calls, no errors/survivors.

**Refutation attempted:** Tested evidentiary counterexamples: driver0 alone did not pass baseline; inherited prior outer1 and candidate overlay are retained separately. Final installed records replace overlay-only uncertainty. Scan subprocess exit may be killed during normal cancellation and is not mislabeled naturally successful.

**Notes:** Normal ES exit only; fatal/SIGTERM containment and physical radios excluded. No new runtime was run.

### AC-50: Saved/connected/open/protected/unknown/manual-input/profile-choice/forget flows retain their behavior in the VM regression transcript, including no password prompt for confirmed open networks.

**Source:** Issue #577, literal body line 53.
**Written:** 2026-10-15T11:10:50.690361+00:00
**Verdict:** PASS

**Evidence:** GuiWifi.cpp186–415 routes chosen profile explicitly, saved/current via join, confirmed open via connectOpenWifi without key popup, protected/unknown via key editor, manual SSID unchanged and multiple profiles explicit. Original wifi-routes initial open subcase0/connect-open once, overall failed walk1; corrected02 protected/unknown/manual/saved/profiles0 with expected zero or one mutation. wifi-remaining original connected Home join and CafeA forget preserve sibling CafeB; cancel/confirmed cases and frame custody recorded.

**Refutation attempted:** Kept failed overall owner separate from successful open subcase; protected/unknown cancellation never treated as connection proof. Inspected profile-name routing and confirmation callback rather than assuming SSID equals profile.

**Notes:** Synthetic VM mutation only; no owner credentials or radio association claim.

### AC-56: Record source and installed-artifact evidence for standalone/core selection, RA compile support, launch configuration and relevant runtime gates without credentials.

**Source:** Issue #574, literal body line 24.
**Written:** 2026-10-15T11:14:15.705509+00:00
**Verdict:** PASS

**Evidence:** Dolphin package explicitly enables USE_RETRO_ACHIEVEMENTS. Current cheevos_dolphin.sh gate and NoGUI lifecycle patch inspected under AC24–28; actual installed5cb5dac... binary records enabled init/request/shutdown, disabled no-request and failed-boot cleanup. Native02 installed-inputs.json binds same final executable, launcher/helper and ES76f18... to f863 SYSTEM2c69f653...; selected frontend/core frames distinguish standalone Dolphin and core contracts.

**Refutation attempted:** Did not equate compile flag/generated HostUrl/listener with successful authentication. Original baseline startup omission remains reproduced; disabled case makes no network request.

**Notes:** Credential-free synthetic loopback, no owner account/award/game association claim; libretro is a separate runtime.

### AC-57: Trace GameCube recognition through ES/offline indexing separately from Dolphin in-game support, including the reported format and a supported test fixture.

**Source:** Issue #574, literal body line 25.
**Written:** 2026-10-15T11:14:15.705716+00:00
**Verdict:** PASS

**Evidence:** ES external/libcheevos/cheevos.cpp dispatches GameCube RVZ to bounded rvz_hash.cpp; ThreadedHasher.cpp forces only failed RVZ retry while preserving valid indexed hashes. Read full RVZ parser: header/table/digest/version/type/size/compression bounds, exact short reads, 128MiB hash reads and512MiB decoded budget; NONE/Zstd only. Original format02 independent Dolphin conversions:5 decodes,2 encodes,2 roundtrips,2 candidate hashes all0, same ISO83c6dacc.... Actual installed Python/native ISO/NONE/Zstd all return118545082f24fc195a446d1ee7bbf816; records bind installed native library6c484a... and d6a source.

**Refutation attempted:** Separated frontend recognition, proxy native hash and in-game AchievementManager startup. Synthetic independent encoder avoids accepting only self-generated parser fixtures; unsupported formats remain failures.

**Notes:** Earlier owner nine failed RVZ entries are not replayed or claimed matched. Supported fixture scope is synthetic GameCube NONE/Zstd.

### AC-58: Reproduce any confirmed defect in a disposable VM; repair it with source-bound regression evidence, or document a verified upstream/format limitation with accurate player guidance.

**Source:** Issue #574, literal body line 26.
**Written:** 2026-10-15T11:14:15.705842+00:00
**Verdict:** PASS

**Evidence:** Original md5-result.json records264 digest comparisons per repaired baseline/candidate plus format/repeat/Wii short-read helpers. Compile owner1/container0 and recovery acceptance retained rather than overwritten. Original proxy-original.json fails outside-fixture guard after source126 padding mismatches vs candidate0; corrected fixture preserves those counterexamples and completes scanner controls. Independent format02 worker original0/cleanup0/no forced cleanup; installed-native result binds actual libraries and matching hashes.

**Refutation attempted:** Checked baseline failure/control distinction and independent encoder plus later installed library proof. Format01, sanitizer, fixture and compile cleanup failures remain historical failures. Parser rejects unsupported codec/Wii geometry and short/truncated bytes rather than accepting a placeholder hash.

**Notes:** No full-disc corpus, commercial-ROM, Wii AES-data or award proof; literal confirmed defect is repaired within documented supported format.

### AC-59: Record the disposition and any necessary flow/screenshot documentation; distinguish absent sets, unmatched ROMs and unsupported runtime instead of silently presenting them as equivalent.

**Source:** Issue #574, literal body line 27.
**Written:** 2026-10-15T11:14:15.705965+00:00
**Verdict:** PASS

**Evidence:** Canonical es-menu-map.md offline-achievement/Dolphin routing flow explicitly separates configuration, installed startup and normal game flow. Current RVZ dispatch/failed-only retry preserve valid unmatched hashes and unrelated roots. #574 captured disposition distinguishes absent set, unmatched valid hash, unreadable/unsupported ROM and unsupported runtime; #583/#584 retain separate repairs. Existing exact-source settings/game-launch frame presentation remains unchanged for nonvisual hash repair.

**Refutation attempted:** Challenged diagnosis collapse: a zero failure sentinel is eligible for targeted retry; a valid hash with no achievement ID is not treated as a read failure. Runtime enabled startup is not an achievement award.

**Notes:** Nonvisual flow documented; no owner data conversion, credential mutation or automatic broad reindex inferred.

### AC-64: Writer-shaped/current/legacy/flat/foreign archive controls pass: replacement18 scripts.log T24-production-backup-scan-restore through T24-foreign-renamed, 13 PASS/0 FAIL.

**Source:** Issue #349, literal body line 15.
**Written:** 2026-10-15T11:14:15.706081+00:00
**Verdict:** PASS

**Evidence:** Original replacement18 qa21/artifacts/rocknix-images/qa-7f58b7b1c5-webdav-a-20261008-1950/scripts.log1437–1449 has all13 literal T24 cases, production backup/scan/restore through foreign-renamed, each PASS; next line records13 PASS/0 FAIL. Actual writer/reader suite uses installed rclone1.75.1.

**Refutation attempted:** Read the original log, including explicit historical migration NOT APPLICABLE beside separately executed current archive controls. Did not turn that N/A into a pass or substitute later continuation for the requested replacement18 run.

**Notes:** Historical source/runtime proof retained; final applicability and installed offered/foreign branch proof are separate criteria.

### AC-65: Canonical menu states and current dimmed settings presentation are retained in docs/es-menu-map.md and #527's composed standard frame proof.

**Source:** Issue #349, literal body line 16.
**Written:** 2026-10-15T11:16:22.144620+00:00
**Verdict:** PASS

**Evidence:** Canonical es-menu-map.md267 and installed replacement19 section retain model/date versus dimmed reason. Exact ES16dbac GuiMenu.cpp4889–4913 reads MINE, disables/unticks invalid absence, otherwise formats model/date. Actual replacement19 offered/foreign frames personally viewed; #527 final composed standard frame continuity is also represented by original78 comparisons under AC16–19.

**Refutation attempted:** Checked absence does not hide SETTINGS or leave it enabled; source and visible row agree. Historical composition qualifications are not replaced by future prose.

**Notes:** No new UI behavior; current source retains the accepted compatibility contract.

### AC-66: On the next installed candidate, retain paired640×480 offered `<DEVICE>, <DATE>` and foreign-only disabled-row frames, with exact same-model/foreign fixture inventories, selected archive/journal and unchanged foreign-case settings hashes. Bind to the image/source manifest.

**Source:** Issue #349, literal body line 17.
**Written:** 2026-10-15T11:16:22.144870+00:00
**Verdict:** PASS

**Evidence:** Original ui19e installed writer/upload receipts and inventories contain two compatible archives and newer foreign archive. same-model-scan MINE selects2026_10_11-190000-GENERIC-X64-pixelelated_SETTINGS.tar.gz despite NEWEST foreign; selected-archive hash958224fa... matches original uploaded/downloaded bytes and journal actual restore exit0. Personally viewed paired640x480 offered GENERIC X64,10/11/2026 and disabled foreign-only frames. Corrected foreign-proof.py/log compare four actual configuration-file hashes before/after with MINE empty. Evidence index binds image0.0.1-dev+20261011T174137Z.ga0f60255abfe,ESc8dc,bundleee8e263... no overlays. Restoration completion source-readback original gitdiff0 proves cloud writer/scan/restore bytes unchanged through f863.

**Refutation attempted:** Retained initial settings-proof failure on wrong /storage/.config/system.cfg path; it proves no foreign preservation. Separate foreign-proof uses actual /storage/.config/system/configs/system.cfg and completes. Foreign file is intentionally newer so passing cannot be explained by latest-all selection.

**Notes:** This is the requested next installed replacement19 proof with continuity, not a fabricated final replay. Device model label, not unique-owner identity, is the compatibility boundary.

### AC-67: Publish the same-model/newest/disabled-state explanation with #344/#511 release/setup documentation; cite the retrieved page or docs change.

**Source:** Issue #349, literal body line 18.
**Written:** 2026-10-15T11:16:22.145002+00:00
**Verdict:** PASS

**Evidence:** Restoration-completion/originals.tar.gz retains raw merge-response mergedtrue SHA6aac689..., successful PR/main/deploy run originals38717338495/38717686667/38717686819 and HTTP200 readback2026-10-15T10:07:16.363444Z. Independently hashed23180B public-cloud-guide.html to4891f14feaf0bd78694fbca1cb27f123cdba0f670f16a7ccbe51107e6d7c9d18 and read actual restore-settings HTML: newest compatible same-model, model/date, exclude newer foreign, visible dimmed SETTINGS and exact reason.

**Refutation attempted:** Verified retained publication bytes rather than relying on source proposal or deployment status alone. Website merge receipt and page content agree.

**Notes:** This closes #349 documentation criterion only; other #511 site/QR/help and #344 release gates are not inferred complete.

### AC-52: Bind the observed systems to selected emulator/core and effective automatic save/load settings; artifact/source receipt separates global preference, runtime implementation, and manager support.

**Source:** Issue #575, literal body line 29.
**Written:** 2026-10-15T11:16:22.145112+00:00
**Verdict:** PASS

**Evidence:** Exact source SaveStateRepository::isEnabled requires emulator retroarch and configured system; GuiMenu resolves per-game/system AUTO through actual selection and adds native limitation dialog for dolphin/flycast. Native02 installed-inputs binds f863/ES16dbac and exact Dolphin/Flycast launchers. Original capability matrix has20 successful locale/size selection cases plus system/collection/global controls, settings preserved; previous gc fixture failures remain1. Actual native-selection/global frames and native state inventories distinguish selected engine, global preference and independent native facilities.

**Refutation attempted:** Checked AUTO and explicit per-game override, not system name alone. No owner Nova selection inferred from failed owner read. Existing incremental0→2 equivalent-Off normalization is not claimed byte-identical.

**Notes:** Global preference does not constitute implemented standalone manager support.

### AC-54: If the current UI implies unsupported behavior, correct capability gating or help text with EN/FR flow references and exact-source screenshots; do not silently promise session preservation.

**Source:** Issue #575, literal body line 31.
**Written:** 2026-10-15T11:16:22.145223+00:00
**Verdict:** PASS

**Evidence:** GuiMenu5796–5840 changes global guidance to supported emulators only and manager RetroArch only;10861+ resolves actual emulator before native support dialog. SaveStateRepository keeps explicit retroarch gate. Original EN/FR640/1280 capability cases rc0 with settings unchanged; later French replacement frames personally viewed at640 and1280 show concise supported-emulator/RetroArch guidance. Native02 actual installed640 support dialog personally viewed and correctly separates ordinary saves.

**Refutation attempted:** Preserved original long/old French text and earlier failed fixture records; accepted replacement copy frames are distinct. Verified help does not mutate automatic-state settings or promise session preservation.

**Notes:** Rendered long manager label may ellipsize, while clear explanatory description remains visible; no new layout guarantee beyond recorded sizes.

### AC-55: Any proposed standalone integration proves exit/load/slot/path handling, clean and retained-storage behavior, existing state preservation and relevant hardcore restrictions; otherwise record the supported limitation explicitly and scope enhancement separately.

**Source:** Issue #575, literal body line 32.
**Written:** 2026-10-15T11:16:22.145335+00:00
**Verdict:** PASS

**Evidence:** Captured #575 explicitly takes limitation route. Source adds informational help/gating only; standalone launchers do not acquire global autosave or frontend-manager integration. Actual native state observations confirm separate engine behavior; final clean/retained installed composition binds unchanged preferences and selected storage.

**Refutation attempted:** Rejected inference that a successful native state load supplies new ES integration, power-loss durability, every native slot or hardcore matrix. Such proposed integration would require its own criteria.

**Notes:** No standalone integration proposed; accurate supported limitation is the literal alternative required here.

### AC-51: Canonical flow/reference and reviewed exact-source happy/branch frame index accompany the final source; syntax checks and affected VM checks pass before pin promotion. Public setup documentation receives the corresponding follow-up.

**Source:** Issue #577, literal body line 54.
**Written:** 2026-10-15T11:18:17.821580+00:00
**Verdict:** PASS

**Evidence:** Canonical es-menu-map Wi-Fi flow references exact source/branch frame indexes; source16dbac normal-exit raw compiler packet (supplements/wifi-compiler-result) syntax.json original_exit0 ended02:39:56, link.json0 ended02:40:35, candidate binary067def..., baseline3178/candidate16dbac named in container/target artifact originals. Candidate and final installed affected VM checks are independently verified in AC46–50. Original tracker-completion.tar.gz packet/root-receipts/511-body-readback-response.json records the corresponding Wi-Fi setup-guide follow-up and its agent-verifiable behavior/frame/check receipts.

**Refutation attempted:** Read raw syntax/link/identity records without prior auditor readback verdict; actual output is initially candidate overlay, followed by final clean/retained installed proof. Follow-up requirement does not imply whole #511 guide/site work already delivered.

**Notes:** Pin/source/frame order is supported by timestamped compiler and subsequent normal-exit/final-image originals. No new compilation or external action.

### AC-53: Document and verify behavior for RetroArch, standalone Dolphin and standalone Flycast using disposable VM fixtures: ordinary in-game save, manual state, exit auto-state and manager visibility are separate observations.

**Source:** Issue #575, literal body line 30.
**Written:** 2026-10-15T11:21:27.258664+00:00
**Verdict:** PASS

**Evidence:** RetroArch ordinary-save original baseline02 archive exit.log has runemu0 and actual .srm first byte55 on normal/debounced exit; current baseline-continuation scripts.log383–401 verifies numbered slot, AUTO SAVE, START NEW GAME and effective auto-load/save. Personally viewed original #196 before/after640 frames: numbered02:16 tile persists, AUTO SAVE advances02:08 to02:17; dated QA ledger/work log bind original loaded slot and quit, not a new run. Native03 original cold frames plus exported415B Wii save93c59... contain entered r1c2=4 and VMU131072B5f72... decoded CRC-verified score164; directly viewed cold score164 and Wii continued31-empty scene. Native02 final f863 installed inputs and inventories separate native states: Wii .s01 unchanged3732..., visible timer00:31→paused01:00→restored00:30; Flycast manual4666... unchanged hash/mtime with globalOn/nativeOff, native autoOn/globalOff creates376c... and fourth cold scene matches before any manual load. Supervisor original0/native children absent, raw engine wait explicitly unknown.

**Refutation attempted:** Did not use state-file presence alone as load proof: viewed scene restoration and paired snapshots. Ordinary-save data is distinct from .s01/.state. Kept native03 failed export-wrapper1 and first state fixture failure separate; native02 supplies missing completed state behavior. Historical RetroArch full raw launch transcript is not re-created from ledger prose; retained frames and unchanged current launcher controls are its inherited evidence boundary.

**Notes:** No new RetroArch replay, no standalone frontend integration, no power-loss claim or owner configuration inference. Wii cold-frame warnings partially obscure top row; binary save content provides the entered-cell witness rather than pretending that pixel is clearly visible.

## Prior-verdict cross-check

**Opened after forward completion:** 2026-10-15T11:22:58.079783+00:00. Compared by literal criterion text, never by colliding IDs. Prior #596 frozen scorecard and all original failures remain untouched. Its final appendices independently resolved six findings and named final composition/native-state continuations; this audit independently re-read those originals before opening those verdicts.

| Current | Issue | Prior initial verdict | Current | Reconciliation |
| --- | --- | --- | --- | --- |
| AC-01 | #602 | — | PASS | New cadence scope; no matching prior criterion |
| AC-02 | #602 | — | PASS | New cadence scope; no matching prior criterion |
| AC-03 | #602 | — | PASS | New cadence scope; no matching prior criterion |
| AC-04 | #602 | — | PASS | New cadence scope; no matching prior criterion |
| AC-05 | #602 | — | PASS | New cadence scope; no matching prior criterion |
| AC-06 | #600 | — | PASS | New cadence scope; no matching prior criterion |
| AC-07 | #600 | — | PASS | New cadence scope; no matching prior criterion |
| AC-08 | #600 | — | PASS | New cadence scope; no matching prior criterion |
| AC-09 | #600 | — | PASS | New cadence scope; no matching prior criterion |
| AC-10 | #600 | — | PASS | New cadence scope; no matching prior criterion |
| AC-11 | #599 | — | PASS | New cadence scope; no matching prior criterion |
| AC-12 | #599 | — | PASS | New cadence scope; no matching prior criterion |
| AC-13 | #599 | — | PASS | New cadence scope; no matching prior criterion |
| AC-14 | #599 | — | PASS | New cadence scope; no matching prior criterion |
| AC-15 | #599 | — | PASS | New cadence scope; no matching prior criterion |
| AC-16 | #591 | — | PASS | New cadence scope; no matching prior criterion |
| AC-17 | #591 | — | PASS | New cadence scope; no matching prior criterion |
| AC-18 | #591 | — | PASS | New cadence scope; no matching prior criterion |
| AC-19 | #591 | — | PASS | New cadence scope; no matching prior criterion |
| AC-20 | #589 | AC-108 PASS | PASS | Agreement with prior PASS |
| AC-21 | #589 | AC-109 PASS | PASS | Agreement with prior PASS |
| AC-22 | #589 | AC-110 PASS | PASS | Agreement with prior PASS |
| AC-23 | #589 | AC-111 PASS | PASS | Agreement with prior PASS |
| AC-24 | #584 | AC-099 PASS | PASS | Agreement with prior PASS |
| AC-25 | #584 | AC-100 FAIL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-26 | #584 | AC-101 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-27 | #584 | AC-102 FAIL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-28 | #584 | AC-103 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-29 | #582 | AC-089 PASS | PASS | Agreement with prior PASS |
| AC-30 | #582 | AC-090 PASS | PASS | Agreement with prior PASS |
| AC-31 | #582 | AC-091 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-32 | #582 | AC-092 PASS | PASS | Agreement with prior PASS |
| AC-33 | #582 | AC-093 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-34 | #581 | AC-085 PASS | PASS | Agreement with prior PASS |
| AC-35 | #581 | AC-086 PASS | PASS | Agreement with prior PASS |
| AC-36 | #581 | AC-087 PASS | PASS | Agreement with prior PASS |
| AC-37 | #581 | AC-088 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-38 | #580 | AC-081 PASS | PASS | Agreement with prior PASS |
| AC-39 | #580 | AC-082 PASS | PASS | Agreement with prior PASS |
| AC-40 | #580 | AC-083 FAIL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-41 | #580 | AC-084 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-42 | #579 | AC-077 PASS | PASS | Agreement with prior PASS |
| AC-43 | #579 | AC-078 PASS | PASS | Agreement with prior PASS |
| AC-44 | #579 | AC-079 PASS | PASS | Agreement with prior PASS |
| AC-45 | #579 | AC-080 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-46 | #577 | AC-067 PASS | PASS | Agreement with prior PASS |
| AC-47 | #577 | AC-068 PASS | PASS | Agreement with prior PASS |
| AC-48 | #577 | AC-069 PASS | PASS | Agreement with prior PASS |
| AC-49 | #577 | AC-070 PASS | PASS | Agreement with prior PASS |
| AC-50 | #577 | AC-071 PASS | PASS | Agreement with prior PASS |
| AC-51 | #577 | AC-072 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-52 | #575 | AC-063 PASS | PASS | Agreement with prior PASS |
| AC-53 | #575 | AC-064 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-54 | #575 | AC-065 PASS | PASS | Agreement with prior PASS |
| AC-55 | #575 | AC-066 PASS | PASS | Agreement with prior PASS |
| AC-56 | #574 | AC-059 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-57 | #574 | AC-060 PASS | PASS | Agreement with prior PASS |
| AC-58 | #574 | AC-061 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-59 | #574 | AC-062 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-60 | #564 | AC-022 PASS | PASS | Agreement with prior PASS |
| AC-61 | #564 | AC-023 PASS | PASS | Agreement with prior PASS |
| AC-62 | #564 | AC-024 PASS | PASS | Agreement with prior PASS |
| AC-63 | #564 | AC-025 PARTIAL | PASS | Later source/installed/supplemental evidence resolves original gap; prior frozen verdict retained |
| AC-64 | #349 | AC-001 SKIP | PASS | Prior scoped exclusion; independently verified inherited originals and later publication |
| AC-65 | #349 | AC-002 SKIP | PASS | Prior scoped exclusion; independently verified inherited originals and later publication |
| AC-66 | #349 | AC-003 SKIP | PASS | Prior scoped exclusion; independently verified inherited originals and later publication |
| AC-67 | #349 | AC-004 SKIP | PASS | Prior scoped exclusion; independently verified inherited originals and later publication |

48 criteria match the previous115-criterion scope;19 are newly added cadence scope. Differences from its frozen PARTIAL/FAIL rows are time/source/evidence changes, not a claim that the earlier auditor was wrong. #349 was deliberately SKIP there and its documentation was subsequently published. AC08 historical lint uncertainty is preserved with a new check, not a retrospective fabricated result. No unresolved contradictory verdict was established.
