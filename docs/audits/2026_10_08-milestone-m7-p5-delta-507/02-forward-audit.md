# Forward Audit — M7.P5 delta #507

**Auditor:** Code Auditor skill; `/root/m7_fresh_audit_owner`.
**Date:** 2026-10-08
**Subject:** Frozen post-candidate16 Milestone delta.
**Spec:** Exact criteria in `inputs/criteria.json`; source identities in `inputs/source-manifest.json`.

## Running Notes

Phase 2 started 2026-10-08T08:10:31.729930+00:00. Primary evidence is read independently; prior per-AC audit grades remain sequestered. Historical target receipts are evaluated at their actual source identities; fresh host controls supplement them and do not certify a new image. Audit-self completion criteria will be classified honestly at the forward-audit boundary.

### 2026-10-08T08:14:49.201244+00:00: host/retention primary evidence

`checks/host-controls01` completed17 commands rc0, including15 cadence,19 retention and8 disposable cleanup controls. All four result channels match; actual host runner/watcher/command processes exited. Primary planner code rejects changed/unreadable/active/protected/referenced disks and classifies only protected exact archive members; full-root historical reports retain24 candidates,22 eligible,64 source fixtures and no unresolved errors. The fixed historical #491 executor binds a fresh report, explicit proposal digest and all22 targets before unlink, then rechecks preserved inputs. `checks/retention-receipt-readback.json` independently rehashes46 retained files and verifies exact removed-set/current absence, measured-recovery arithmetic and historical ARM budget. Historical accepted payloads need not still exist under later D-INFRA-022; no deletion or capacity replay occurred.

### AC-461-01: Canonical worktree/build instructions describe the qualification trigger, protected set and capacity review; a decision row and M7 link make the follow-up findable.

**Source:** #461; `inputs/issues/461.json`, body line19.
**Recorded:** 2026-10-08T08:16:24.786654+00:00
**Verdict:** PASS ✓

**Evidence:** .claude/rules/worktrees.md:136–177; docs/decision-register.md D-INFRA-018/019/021/022; checks/host-controls01/rules.log; inputs/milestone7.json

**Refutation attempted:** Checked current policy against its older register rows: D-INFRA-022 expressly supersedes generic fallback retention, while review, measured capacity and explicit permission remain. Current rule/index check rc0.

**Notes:** Policy is discoverable and correctly distinguishes retention review from automatic cleanup.

### AC-461-02: A repeatable read-only retention report binds proposed removals and retained dependencies to exact paths/identities and states whether the next scheduled build fits.

**Source:** #461; `inputs/issues/461.json`, body line20.
**Recorded:** 2026-10-08T08:16:24.786821+00:00
**Verdict:** PASS ✓

**Evidence:** tools/host-maintenance/retention-report:22–65,70–207,267–291; docs/qa-logs/2026-10-07-pixelelated-replacement-16/retention-review-02/artifacts/report.json; checks/host-controls01/retention.log

**Refutation attempted:** Checked capacity false as well as eligible cases: historical available160252882944 is less than ARM required199695544320; aarch64 headroom remains negative. Planner only reads and tests assert disk still exists. Fresh19 controls rc0.

**Notes:** Exact identities, hashes, retained dependencies and explicit fit status are output; no capacity guarantee for a later build is inferred.

### AC-461-03: Planner controls reject active, unreadable, unclassified or referenced candidates, including qcow2 backing chains and cross-store objects; logs retain each rejection.

**Source:** #461; `inputs/issues/461.json`, body line21.
**Recorded:** 2026-10-08T08:16:24.786876+00:00
**Verdict:** PASS ✓

**Evidence:** tools/host-maintenance/retention-report:70–265; checks/host-controls01/retention.log; checks/host-controls01/results.json

**Refutation attempted:** Executed actual unreadable file/tree, cross-store QCOW, symlink/JSON, hardlink, live-owner, changed-identity and tampered-evidence controls. Each invalid candidate was held and eligible controls succeeded.

**Notes:** 19 synthetic host controls rc0, using actual temporary QCOW/process facts rather than a mocked eligibility result.

### AC-461-04: The first later authorized batch records preservation checks, watcher completion, actual path/registration removal, measured recovery and unchanged protected inputs. Until then, no automatic deletion is claimed.

**Source:** #461; `inputs/issues/461.json`, body line22.
**Recorded:** 2026-10-08T08:16:24.786918+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-pixelelated-replacement-16/approved-retirement-01/{execution,owner-verification}.json; approved-retirement-01/artifacts/retention-verification.json; checks/retention-receipt-readback.json

**Refutation attempted:** Checked the first two-file batch has an explicit D-INFRA-019 authorization and exact two-path output, four matching0 channels, 53 unchanged evidence hashes and15 protected metadata observations. Later22-file batch has separate #491 approval and independent exact-set/digest verification.

**Notes:** Historical removal/custody evidence establishes the scoped completed batches. These are files, so worktree registration removal is not applicable; automatic deletion remains unimplemented.

### AC-489-01: A complete validated receipt advances the audit clock to its actual
  completion time, with the qualifying artifacts and issue named in output.

**Source:** #489; `inputs/issues/489.json`, body line20.
**Recorded:** 2026-10-08T08:16:24.786953+00:00
**Verdict:** PASS ✓

**Evidence:** tools/ceremony-check:85–121,349–389; checks/host-controls01/cadence.log

**Refutation attempted:** Fresh positive control returned the exact zoned completion timestamp and issue471; a changed completion timestamp without matching tracker receipt was rejected. The printed live receipt names the path and issue.

**Notes:** 15 controls rc0. Validated completion, not folder creation date, advances the cutoff.

### AC-489-02: Controls reject incomplete, stale/tampered, future-dated and malformed
  receipts, and count only closures after completion without changing cadence.

**Source:** #489; `inputs/issues/489.json`, body line22.
**Recorded:** 2026-10-08T08:16:24.786987+00:00
**Verdict:** PASS ✓

**Evidence:** tools/ceremony-check:85–128; docs/qa-logs/2026-10-07-audit-cadence/test-cadence.py:35–76; checks/host-controls01/cadence.log

**Refutation attempted:** Ran missing/tampered/future/unbound/naive/wrong-issue/open/unchecked/unverified/schema/unsafe-path/malformed controls. Exact cutoff equality is excluded and only later closure counts; constants remain12/14.

**Notes:** Every adversarial receipt rejected; positive receipt accepted. No cadence-policy change.

### AC-489-03: The live checker recognizes the completed #471 audit, with its output
  retained; normal rules/register/index checks remain green.

**Source:** #489; `inputs/issues/489.json`, body line24.
**Recorded:** 2026-10-08T08:16:24.787016+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-audit-cadence/live-after.log:1–18; checks/host-controls01/{rules,register,work-log-index}.log; tools/ceremony-check:362–381

**Refutation attempted:** Read the actual historical output: #471 completed2026-10-07T02:53:02.029760+00:00,0/12 closures,0/14 days. Fresh rules/register/index checks all rc0; helper receipt controls run against frozen tool.

**Notes:** This criterion concerns the retained #489 live acceptance, not a claim the current closure count is below cadence. The present audit itself is the owed audit.

### AC-490-01: The report records each exact archive-verified source fixture while
  preserving all real disk, backing-chain and cross-store checks.

**Source:** #490; `inputs/issues/490.json`, body line17.
**Recorded:** 2026-10-08T08:16:24.787048+00:00
**Verdict:** PASS ✓

**Evidence:** tools/host-maintenance/retention-report:41–66,90–129; docs/qa-logs/2026-10-07-pixelelated-replacement-16/retention-review-02/artifacts/{fixture-provenance,report}.json; checks/retention-receipt-readback.json

**Refutation attempted:** Verified exact retained source archive SHA32dc32ae…992 and64 listed protected fixtures. Source bypass requires identity, protected ancestry, noncandidate status, regular archive member and matching file/member SHA; real QCOW discovery/reference checks remain after that branch.

**Notes:** No filename-only exemption. Primary code and report establish archive-specific classification.

### AC-490-02: Controls reject a changed fixture, changed archive, unprotected fixture
  or unclassified disk; the existing active/use/preservation controls pass.

**Source:** #490; `inputs/issues/490.json`, body line19.
**Recorded:** 2026-10-08T08:16:24.787078+00:00
**Verdict:** PASS ✓

**Evidence:** checks/host-controls01/retention.log; tools/host-maintenance/test-retention-report:73–94

**Refutation attempted:** Fresh controls changed fixture bytes, archive bytes and protected scope separately: all held; unclassified truncated QCOW held; restoring the exact archive fixture returned eligible. Existing active/use/cross-store controls also ran.

**Notes:** 19 controls rc0, including both valid and invalid fixture classification.

### AC-490-03: A fresh full-root report records actual eligible/held candidates and
  H700 capacity, with original refusals and all source/evidence hashes retained.

**Source:** #490; `inputs/issues/490.json`, body line21.
**Recorded:** 2026-10-08T08:16:24.787104+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-pixelelated-replacement-16/retention-review-02/artifacts/{report,plan,fixture-provenance}.json; h700-retirement-proposal/{proposal,acceptance}.json; checks/retention-receipt-readback.json

**Refutation attempted:** Checked actual report:24 candidates,22 eligible,2 held,73 references,64 source fixtures,0 unresolved errors. Forecast explicitly says ARM does not fit before cleanup and aarch64 does not fit after this small batch. #491 independently binds the full report/plan SHA.

**Notes:** Report is a historical read-only capacity observation, not current deletion authority. Original unclassified-source rejection is retained and replicated by the fresh control.

### AC-491-01: The fixed-scope helper's verification-only result matches all 22 exact
  identities/hashes, independent evidence and retained base disks; no mutation.

**Source:** #491; `inputs/issues/491.json`, body line20.
**Recorded:** 2026-10-08T08:16:24.787130+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-retirement-proposal/execute.py:7–58; retirement-verification-01/{verification,owner-verification}.json; checks/retention-receipt-readback.json

**Refutation attempted:** Read default verification-only branch, fixed22-name set, exact file/plan/tool/hash/identity checks and independent preserved-evidence loop. Rehashed the retained verification packet; result explicitly deletion_performed=false.

**Notes:** The actual historical verification matched proposalab03cbbb…a39c9. No destructive helper was rerun.

### AC-491-02: After separate authorization, a fresh full-root dependency report has
  no unresolved observations and still accepts every named file; four result
  channels and exact source/input seals are retained for execution.

**Source:** #491; `inputs/issues/491.json`, body line22.
**Recorded:** 2026-10-08T08:16:24.787157+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-qa-retirement-01/{approval,fresh-report,verification,owner-verification,seal}.json; checks/retention-receipt-readback.json

**Refutation attempted:** Verified approved proposal SHA equals execution and verification SHA; fresh report digest59021987…a40 matches bytes, contains0 errors/active observations and same22 eligible names. All retained result channels match0; packet46 files rehashed across verification/execution owners.

**Notes:** The report was refreshed after explicit batch approval. Historical owner exits are recorded in their host receipt; no sandbox PID inference is used.

### AC-491-03: Only the named files are absent, all preserved evidence hashes and
  protected identities remain unchanged, and actual free space meets the
  H700 arm budget; retain the execution and recovery receipt.

**Source:** #491; `inputs/issues/491.json`, body line25.
**Recorded:** 2026-10-08T08:16:24.787184+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-pixelelated-replacement-16/h700-qa-retirement-01/{execution,acceptance}.json; checks/retention-receipt-readback.json

**Refutation attempted:** Independently compared removed set to22 exact proposal targets, checked those paths currently absent, recomputed recovery45146042368=after−before and ARM205386608640>=199695544320. Executor postchecks protected7,held2 and2695 evidence hashes before successful terminal status.

**Notes:** Historical proof is sealed and consistent. Later policy may retire formerly held payloads; no current claim that those historical large files remain is made.

### 2026-10-08T08:17:26.837764+00:00: build and broad-retention primary reads

Read complete affected recipe/lifecycle diffs: six ARM consumers and build_distro change generated paths from DISTRO to DISTRONAME; configuration namespace is unchanged. SPIRV host-only hook demotes only GCC12 free-nonheap-object error; original/repair/unoptimized/equivalent-loop/unrelated-warning controls retain rc1/0/0/0/1. Actual installed shader proof has9 commands including expected invalid-layout rc1, with independent matching tool/stamp hashes; its stage explicitly does not claim full arm04 success. FEX patch removes only the rebased standard include alongside /usr/include.

Broad-retention primary preservation records charge59297792 allocated bytes against464527437824 gross bytes, independently hash14489 objects and4 source inventories. Dependency review originally retained196 unreadable processes and required administrator refresh. The later execution record and explicit14-loose-file administrator-scope gap must be assessed together; a generic PASS in original acceptance cannot erase that limitation. Fresh8 cleanup controls already reproduce/refute the prospective root-coverage guard.

### 2026-10-08T08:18:48.386336+00:00: H700 proof chain and fresh install controls

Direct primary records distinguish failed arm03 hash observer, successful SPIRV stage in arm04, later arm04 box86 failure, preserved six interrupted scopes and fresh arm05 acceptance. Arm05 binds43d0bc3b,7866 files/797 symlinks/938 ARM ELF objects/244 stamps and four0 channels. Historical H700 firmware binds185 ARM handoff files and independently different DDR3/DDR4 bootloaders with common SYSTEM/KERNEL. SM8550 final receipt binds0553c019,187 handoff files,14 FEX ELF objects, exact bundle97367c…fb18 and terminal build/acceptance/sequence custody. This defeats a source-integration-only inference but does not establish current #508 image inclusion.

Prepared fresh isolated42-case install/lifecycle controls from the retained harness. Seven fixed inputs are byte-equal to current frozen source, with historical originals as negative controls. These execute only disposable fixture install hooks and stubbed build lifecycle, not a package or image build.

### 2026-10-08T08:20:47.739761+00:00: FEX and install-control observations

Fresh42 current recipe/lifecycle controls pass, including collisions with deliberately wrong older ROCKNIX siblings and missing payload cases. Historical FEX paired compiler argv differ only by the ARM64 standard include; original Wayland/GL fail and isolated removal succeeds. Exact Nix2.35.2/nixpkgs/Clang21.1.8/rootfs/toolchains are retained; final14-ELF package has five32-bit and eight64-bit x86 guest libraries plus native AArch64 FEX. The original verifier failure is explicitly guest-libs/build.ninja; corrected Guest/Guest_32 check observes actual generated include lines and14 installed ELF identities. No source features or pins were weakened by the two-line CMake correction. Remaining verification checks raw packet seals, recovery and sequence ownership before verdict.

### 2026-10-08T08:24:36.555832+00:00: retained byte seals and cloud finite completion

Independently rehashed compact FEX/header controls, failed02, final04 and historical migration-copy SHA256SUMS (311 files); all match. Verified #499 exact feature commit changes exactly the two recorded lines/files, before/after digests and absence from frozen next without exposing protected wording. `checks/build-evidence-readback.json` retains the metadata. Fresh cloud controls complete rc0:30 validator,39 save-layout,21 selected-content,31 DuckStation and24 integrity controls. All four result channels and host process exits were consumed; target-runtime claims still depend on their exact retained VM receipts.

### 2026-10-08T08:26:19.404148+00:00: historical build preflight and tracker lead

Read and retained three bounded nonprivate runtime receipts missing from the compact public build packet: original/final SM8550 capacity passes and the watched H700-prerequisite acceptance hash. Original SM8550 capacity at09:09:55 follows H700 acceptance09:08:34; final retry16:14:07 retains ample measured margin. No full local inventory or personal record was opened. Independently queried exact hosted success/failure runs for #499 and preserved the returned head/conclusion/status. #497 latest body still calls H700 firmware actively compiling and actual handoff pending despite later sealed185-file H700/187-file SM8550 handoff evidence; this is a confirmed tracker-reconciliation lead, separate from image evidence. #492 explicitly preserves earlier sections as history and keeps source/licence/per-image mapping open.

Evidence abbreviations for the following entries: **B**=`docs/qa-logs/2026-10-07-device-builds`; **S**=`docs/qa-logs/2026-10-07-storage-retention`. These always resolve within the frozen audit worktree.

### AC-492-01: Frozen input manifests show the qualified product-source comparison, distribution/ES pins, actual pinned container digest, source cache and concurrency for each target.

**Source:** #492; `inputs/issues/492.json`, body line19.
**Recorded:** 2026-10-08T08:29:51.997304+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** B/h700-firmware01/inputs-summary.json; B/h700-arm05/runtime-start.json; B/sm8550-resume04/terminal/readback.json; inputs/extra-primary/

**Refutation attempted:** Compared actual historical pins: H70043d0bc3b/ES72494bc7 and SM85500553c019/ES5d2fcb9b differ from current ES4e410; container988c0ba5, cache and concurrency are explicitly bound.

**Notes:** Historical input manifests exist. Full current product-to-image qualification mapping remains expressly open in #492/#508; pre-existing scope, not a discovered regression.

**Gaps:** Historical input manifests exist. Full current product-to-image qualification mapping remains expressly open in #492/#508; pre-existing scope, not a discovered regression.

### AC-492-02: H700 arm compatibility build has matching terminal result channels, unchanged input seals and verified builder exit; retain its output/stamp manifest.

**Source:** #492; `inputs/issues/492.json`, body line20.
**Recorded:** 2026-10-08T08:29:51.997384+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm05-acceptance/artifacts/acceptance.json; B/h700-arm05/{runtime-start.json,artifacts/output-manifest.json}

**Refutation attempted:** Read all four zero channels, seven seals, actual exited container identity,938 ARM ELF objects and244 stamps. Output manifest SHA11631473…3e18 matches the subsequent firmware input binding.

**Notes:** Historical arm stage only:7866 files/797 symlinks, not firmware or physical acceptance.

### AC-492-03: H700 aarch64 firmware build follows a measured capacity pass and has verified terminal results, raw/update identity and hashed DDR3/DDR4 artifacts.

**Source:** #492; `inputs/issues/492.json`, body line21.
**Recorded:** 2026-10-08T08:29:51.997431+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-firmware01/{capacity,inputs-summary}.json; B/rg35xxsp-adoption01/{h700-artifact-acceptance,h700-acceptance-owner}.json

**Refutation attempted:** Checked positive post-cleanup capacity after earlier negative post-arm gate; accepted DDR3/DDR4 raw hashes differ and bootloader hashes differ, while SYSTEM/KERNEL match.185 ARM handoff files; four0 channels/four seals/exits.

**Notes:** Historical bundle d89b067a…af710 and43d0bc3b; new product image remains separate.

### AC-492-04: SM8550 compilation follows completed H700 artifact verification and a measured capacity pass; retain verified terminal results and hashed image/update artifacts.

**Source:** #492; `inputs/issues/492.json`, body line22.
**Recorded:** 2026-10-08T08:29:51.997475+00:00
**Verdict:** PASS ✓

**Evidence:** inputs/extra-primary/{sm8550-initial-capacity,sm8550-final-capacity,sm8550-h700-prerequisite}.json; B/sm8550-resume04/terminal/{readback.json,acceptance/artifacts/acceptance.json,sequence/controller-result.json}

**Refutation attempted:** Initial capacity09:09:55 follows H700 acceptance09:08:34 and exact prerequisite digest. Both capacity margins are positive. Checked final build/acceptance four0 results,13/3 seals, controller PASS and separate raw/update hashes.

**Notes:** Historical SM8550 bundle97367c…fb18 at0553c019; failed01/02/03 remain distinct.

### AC-492-05: Artifact inspection records lowercase pixelelated identity, expected qualified source pins and source/licence inventory; release/publication and separately authorized hardware facts remain explicit in the milestone.

**Source:** #492; `inputs/issues/492.json`, body line23.
**Recorded:** 2026-10-08T08:29:51.997510+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** B/sm8550-resume04/terminal/{readback.json,acceptance/artifacts/acceptance.json}; inputs/issues/492.json; inputs/milestone7.json

**Refutation attempted:** Historical output has lowercase names, nativeAArch64 inspection and qualified English/French ES copy. Compared current source change and explicit remaining source/licence/per-image inventory gate.

**Notes:** Source/licence inventory and final image mapping remain pre-existing open work; no RC/publication or newly installed product claim.

**Gaps:** Source/licence inventory and final image mapping remain pre-existing open work; no RC/publication or newly installed product claim.

### AC-494-01: Exact tree/branch/head, dirty diff, allocation, source and historical references are recorded in the accepted review and current prepared plan.

**Source:** #494; `inputs/issues/494.json`, body line26.
**Recorded:** 2026-10-08T08:29:51.997543+00:00
**Verdict:** PASS ✓

**Evidence:** B/retention-review01/report.json; B/retention-preservation01/artifacts/result.json; S/review-plan.json; S/prepare-plan.py:98–115

**Refutation attempted:** Checked all four named trees carry branch/head, dirty-diff digest, source inventory, allocation and custody manifest. Preparer rechecks git HEAD/branch/diff and source inventory before binding the execution plan.

**Notes:** Exact reviewed worktree identity exists independently of tracker state.

### AC-494-02: Independent verification accepts all 14,489 preservation objects and required source inventories; preservation cost is charged against potential recovery.

**Source:** #494; `inputs/issues/494.json`, body line27.
**Recorded:** 2026-10-08T08:29:51.997571+00:00
**Verdict:** PASS ✓

**Evidence:** B/retention-preservation01/artifacts/result.json; B/retention-acceptance01/artifacts/acceptance.json; S/execute-cleanup.py:241–247,305; S/completed/acceptance.json

**Refutation attempted:** Compared14489 objects across independent acceptance and post-action acceptance; four zero-error source inventories. Recomputed464527437824−59297792=464468140032 net bytes; source objects are hashed again before and after mutation.

**Notes:** Primary retained mechanical receipts establish historical custody, not a claim the original build trees still exist.

### AC-494-03: Completed QA16/QA17 source links are mapped to exact retained source and terminal evidence under the revised policy.

**Source:** #494; `inputs/issues/494.json`, body line28.
**Recorded:** 2026-10-08T08:29:51.997604+00:00
**Verdict:** UNTESTABLE ?

**Evidence:** S/prepare-plan.py:116–135; S/review-plan.json historical_source_links=14; B/retention-classification01/artifacts/classification.json

**Refutation attempted:** Source explicitly checks completed QA16/QA17, exact link/commit/path and completion digests; public compact plan reports14 links. Full exact mapping resides in a deliberately private operational plan.

**Notes:** The public record supports the process and count, but this scope does not open/export that full private inventory. Exact per-link completion binding cannot be independently graded PASS from public compact evidence alone.

### AC-494-04: The four worktrees are covered by the administrator snapshot and current host/container checks; their receipts resolve active-use dependencies before removal.

**Source:** #494; `inputs/issues/494.json`, body line29.
**Recorded:** 2026-10-08T08:29:51.997637+00:00
**Verdict:** UNTESTABLE ?

**Evidence:** S/completed/{administrator-readback-summary,initial-live,before-removal-live,reference-refresh-summary,administrator-scope-gap}.json

**Refutation attempted:** Read UID0/no-unreadable summary, current visible references and process-birth rule; explicit14 loose-file omission is preserved. The complete administrator roots/member inventory is private and absent from this public packet.

**Notes:** No new administrator observation is authorized or needed. Public receipts describe coverage of the four trees, but exact membership is not independently inspectable within this audit boundary; do not manufacture a new historical PASS.

### AC-494-05: The standard helper removed all four exact worktrees; watched terminal results and post-action verification establish absence, actual recovery and preserved inputs.

**Source:** #494; `inputs/issues/494.json`, body line30.
**Recorded:** 2026-10-08T08:29:51.997665+00:00
**Verdict:** PASS ✓

**Evidence:** S/execute-cleanup.py:288–308; S/completed/{execution-summary,acceptance,owner-verification}.json

**Refutation attempted:** Executor calls the standard guarded helper separately for each tree, verifies path absence and git registration absence, then hashes preserved records/objects. Historical884-target terminal record has all four0 channels and exact measured2117325385728-byte recovery.

**Notes:** Four-tree removal is included in the accepted broader batch. Administrator omission for14 other loose files remains explicit under #498, not retroactively fixed.

### AC-495-01: Retained original failing compiler control, source history and diagnostics establish the cause and show the repaired compile passes without weakening unrelated warnings or changing coupled source pins without evidence.

**Source:** #495; `inputs/issues/495.json`, body line11.
**Recorded:** 2026-10-08T08:29:51.997693+00:00
**Verdict:** PASS ✓

**Evidence:** projects/ROCKNIX/packages/graphics/spirv-tools/package.mk:26–35; B/spirv-host-control01/artifacts/{original,warning-only,unoptimized,equivalent-loop,unrelated-warning}.log and result.json

**Refutation attempted:** Original optimized GCC12 diagnostic is error; scoped demotion leaves it visible as warning. Equivalent loop/O0 pass; unrelated unused-variable remains error. Diff changes neither coupled source pins nor target flags.

**Notes:** Narrow host-only workaround is evidence-backed. Frozen package lint rc0 under checks/host-controls01/pkgcheck-spirv-tools.log.

### AC-495-02: The selected package builds under the pinned container, its installed host executables pass representative SPIR-V assembly/validation/disassembly, and package lint passes; retain logs and hashes.

**Source:** #495; `inputs/issues/495.json`, body line12.
**Recorded:** 2026-10-08T08:29:51.997721+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm04-start/spirv-host/{result,compile-commands}.json; B/h700-arm04-start/{spirv-host-smoke.py,stage-acceptance.json}; checks/host-controls01/pkgcheck-spirv-tools.log

**Refutation attempted:** The real installed spirv tools process valid/invalid nested-struct shaders; invalid validation returns1, other eight commands0. Independent tool/stamp hashes match. Probe asserts SPIRV_WERROR still ON and actual compile includes both flags.

**Notes:** Historical pinned-container package proof, nine shader operations; package lint freshly rerun rc0. No whole image inferred.

### AC-495-03: All interrupted build scopes are enumerated and preserved before recovery; a fresh watched H700 arm run passes the formerly failing package using sealed, committed inputs. Full device-image completion remains #492.

**Source:** #495; `inputs/issues/495.json`, body line13.
**Recorded:** 2026-10-08T08:29:51.997753+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm01-failure/{recovery-plan,recovery,owner-verification}.json; B/h700-arm04-start/{freeze-receipt,runtime-start,stage-acceptance}.json

**Refutation attempted:** Recovery preserves GCC/glib/lxml/spirv outputs and incomplete llvm unpack/stamps by rename, with0 deletions and source-fixture classification. Fresh committed f5f815fa stage succeeds; later arm04 failure is retained separately.

**Notes:** All enumerated interrupted scopes are accounted for; full build acceptance belongs to #492.

### AC-496-01: Preserve arm03 original traceback, shader logs, sealed script, terminal channels and exited owner evidence.

**Source:** #496; `inputs/issues/496.json`, body line7.
**Recorded:** 2026-10-08T08:29:51.997786+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm03-failed/console.log; B/h700-arm03-failed/{owner-verification,seal}.json; B/h700-arm03-failed/console.log:517–523

**Refutation attempted:** Read actual AttributeError for hashlib.file_digest after shader work and all four2 terminal channels; seven input seals and owner exits remain failed history.

**Notes:** No successful package build was mislabeled a successful proof writer.

### AC-496-02: A fresh owner uses a streaming SHA256 implementation available in the pinned Python and passes the identical positive and negative shader controls, producing independently verified executable/stamp hashes.

**Source:** #496; `inputs/issues/496.json`, body line8.
**Recorded:** 2026-10-08T08:29:51.997816+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm04-start/spirv-host-smoke.py:4–9; B/h700-arm04-start/spirv-host/result.json; B/h700-arm04-start/stage-acceptance.json

**Refutation attempted:** New hash function streams4MiB blocks through hashlib.sha256, available in pinned Python; actual fresh9 shader operations include the same invalid-layout rejection and independent tool/stamp hashes match.

**Notes:** Observer portability fix is proved on actual pinned environment, not a changed current host Python assumption.

### AC-496-03: The H700 compatibility build resumes only after that successful result; retain the new watched owner in #492.

**Source:** #496; `inputs/issues/496.json`, body line9.
**Recorded:** 2026-10-08T08:29:51.997845+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm04-start/{runtime-start,stage-acceptance}.json; B/h700-arm04-failed-acceptance/artifacts/acceptance.json; B/h700-arm05-acceptance/artifacts/acceptance.json

**Refutation attempted:** Trace stage ordering: successful shader acceptance04:20 precedes later package-path failure04:41; new arm05 completes04:50. Every owner remains distinct with actual terminal state.

**Notes:** No failed owner reused or renamed successful; handoff preserves later #497 cause.

### AC-497-01: Isolated install/lifecycle controls fail against the recorded original recipes where applicable, pass with the repair, preserve the ROCKNIX configuration namespace and do not alter unrelated paths; package lint passes for each affected recipe.

**Source:** #497; `inputs/issues/497.json`, body line11.
**Recorded:** 2026-10-08T08:29:51.997873+00:00
**Verdict:** PASS ✓

**Evidence:** checks/build-root-controls01/{artifacts/result.json,seal.json,owner-readback.json}; scripts/build_distro:41–87; six affected recipe diffs in inputs/distribution-product-diff.patch

**Refutation attempted:** Fresh42 controls execute actual hooks/lifecycle against old/fixed sources, ROCKNIX/pixelelated, colliding old siblings and missing payloads. Seven fixed files byte-equal frozen source; six recipe lints rc0.

**Notes:** Results verify actual installed witness bytes, not command return alone: original recipes can return0 with wrong/missing payload and are correctly rejected.

### AC-497-02: Preserve failed arm04 logs, stamps and every interrupted package scope before resuming from committed repaired inputs with a new watched owner.

**Source:** #497; `inputs/issues/497.json`, body line12.
**Recorded:** 2026-10-08T08:29:51.997903+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm04-failed-acceptance/artifacts/acceptance.json; B/h700-arm04-recovery/artifacts/{recovery,recovery-plan}.json; B/h700-arm05/runtime-start.json

**Refutation attempted:** Six interrupted packages are named, failed owner four2 preserved, recovery archive3ad02972…6bcf and every changed recipe scope retained before advance to43d0bc3b. New arm05 container/owner differs.

**Notes:** No cleanup silently discarded the interrupted outputs.

### AC-497-03: The repaired H700 arm stage has verified terminal results and actual ARM compatibility artifacts; the aarch64 handoff retains required32-bit programs/cores/libraries rather than silently omitting them.

**Source:** #497; `inputs/issues/497.json`, body line13.
**Recorded:** 2026-10-08T08:29:51.997930+00:00
**Verdict:** PASS ✓

**Evidence:** B/h700-arm05-acceptance/artifacts/acceptance.json; B/rg35xxsp-adoption01/h700-artifact-acceptance.json; B/sm8550-resume04/terminal/acceptance/artifacts/arm-handoff.json

**Refutation attempted:** Inspected real ARM ELF acceptance and185-file H700 handoff; SM8550 records187 exact installed mappings including retroarch32,box86,gpSP,DeSmuME and ARM loader/libraries. Source paths useDISTRONAME while namespace staysROCKNIX.

**Notes:** Historical actual target payload evidence satisfies the handoff criterion despite its stale unchecked tracker state.

### AC-497-04: Reconcile H700/SM8550 input manifests, live M7 order, work/friction logs and retained evidence. Capacity, device smoke and release publication retain their existing separate gates.

**Source:** #497; `inputs/issues/497.json`, body line14.
**Recorded:** 2026-10-08T08:29:51.997957+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** inputs/issues/497.json Current state2026-10-07 07:02; B/rg35xxsp-adoption01/h700-artifact-acceptance.json; B/sm8550-resume04/terminal/readback.json; inputs/milestone7.json

**Refutation attempted:** Later H700/SM8550 receipts and live M7 show acceptance, but the issue still explicitly says actively compiling/actual handoff pending and retains unchecked completion. Unlike #492 it has no superseding terminal header.

**Notes:** Discovered tracker drift: reconcile #497 body/criteria to accepted historical artifacts while preserving current-image/physical/release gates. Product evidence is sound; current issue handoff is stale.

**Gaps:** Discovered tracker drift: reconcile #497 body/criteria to accepted historical artifacts while preserving current-image/physical/release gates. Product evidence is sound; current issue handoff is stale.

### AC-498-01: The published cleanup record distinguishes the 14 omitted files from targets covered by the administrator snapshot; original receipts are retained.

**Source:** #498; `inputs/issues/498.json`, body line8.
**Recorded:** 2026-10-08T08:29:51.997996+00:00
**Verdict:** PASS ✓

**Evidence:** S/completed/{administrator-scope-gap,administrator-readback-summary,execution-summary,acceptance}.json

**Refutation attempted:** Counted14 exact omitted loose targets and read the explicit limitation on both amended summaries; original accepted receipt remains unchanged and is not represented as complete root coverage.

**Notes:** Historical omission is acknowledged rather than hidden by the later correction.

### AC-498-02: The corrected executor refuses any target not equal to or below an administrator scan root, before any mutation.

**Source:** #498; `inputs/issues/498.json`, body line9.
**Recorded:** 2026-10-08T08:29:51.998026+00:00
**Verdict:** PASS ✓

**Evidence:** S/execute-cleanup.py:62–77; checks/host-controls01/cleanup-guards.log

**Refutation attempted:** Coverage check is called at live_check entry before mutation; uses component-boundary ancestry. Fresh omitted loose target raises; covering parent succeeds.

**Notes:** Prospective guard only; no additional removal ran.

### AC-498-03: Eight isolated controls pass, including a loose-file omission failure and a covering-parent success, plus changed-file, digest, symlink, extra-entry and directory-permission boundaries.

**Source:** #498; `inputs/issues/498.json`, body line10.
**Recorded:** 2026-10-08T08:29:51.998057+00:00
**Verdict:** PASS ✓

**Evidence:** S/test-cleanup-guards.py; checks/host-controls01/{cleanup-guards.log,results.json}

**Refutation attempted:** Executed all8 controls on disposable temporary data, including wrong digest, changed file, substituted symlink, extra entry and readonly directory with preserved external link sentinel.

**Notes:** 8 PASS rc0, not just inspection of assertions.

### AC-498-04: The correction, historical limitation and control receipt are committed to next through normal checks.

**Source:** #498; `inputs/issues/498.json`, body line11.
**Recorded:** 2026-10-08T08:29:51.998084+00:00
**Verdict:** PASS ✓

**Evidence:** B/cleanup-publication16/publication.json; B/feature-ci-correction01/failed-ci-summary.json; checks/host-controls01/{rules,register,work-log-index}.log; frozen git history

**Refutation attempted:** Next9e8cfeff publication includes36 equal paths and normal hooks; exact next hosted record/wordlist checks succeed. Separate feature failure is retained under #499. Fresh frozen rule/register/index checks rc0.

**Notes:** Correction and original limitation are already in frozen next; no source edit made by this audit.

### AC-499-01: Redact exactly the two identified archive lines under D-WORKFLOW-061 without adding those feature-only archives to next.

**Source:** #499; `inputs/issues/499.json`, body line6.
**Recorded:** 2026-10-08T08:29:51.998111+00:00
**Verdict:** PASS ✓

**Evidence:** B/feature-ci-correction01/redactions.json; checks/build-evidence-readback.json

**Refutation attempted:** Read git objects silently and compared before/after SHA, line counts and changed line numbers52/57. Exact feature commit alters only two files; neither archive exists in frozen next. Protected wording was not printed or retained.

**Notes:** No divergent feature archives were imported into next.

### AC-499-02: The full feature-tree wordlist check and normal commit/push hooks pass; retain the exact-head hosted check result.

**Source:** #499; `inputs/issues/499.json`, body line7.
**Recorded:** 2026-10-08T08:29:51.998137+00:00
**Verdict:** PASS ✓

**Evidence:** B/feature-ci-correction01/publication.json; B/feature-ci-verification01/result.json; checks/feature-ci-live-readback.json

**Refutation attempted:** Fresh bounded GitHub query confirms completed success37586286848 atfe471bde, matching public publication receipt and retained full-tree wordlist verification. Normal hooks are recorded with exact ref readback.

**Notes:** Historical exact-head hosted result verified rather than substituting current next CI.

### AC-499-03: Preserve the failed CI result and record why checking only next did not cover both pushed branches.

**Source:** #499; `inputs/issues/499.json`, body line8.
**Recorded:** 2026-10-08T08:29:51.998164+00:00
**Verdict:** PASS ✓

**Evidence:** B/feature-ci-correction01/failed-ci-summary.json; checks/feature-ci-live-readback.json

**Refutation attempted:** Fresh query confirms failed run37584510495 atc1bd2040; two next runs passed at9e8cfeff. The feature-only paths explain why a next-only wordlist pass did not cover the second pushed branch.

**Notes:** Failure and correction remain distinguishable without disclosing protected text.

### AC-503-01: Preserve the original failure/thread logs and enumerate interrupted packages before any cleanup or retry; compact evidence identifies the frozen input and failed owners.

**Source:** #503; `inputs/issues/503.json`, body line21.
**Recorded:** 2026-10-08T08:29:51.998195+00:00
**Verdict:** PASS ✓

**Evidence:** B/sm8550-fex-controls01/README.md; B/sm8550-resume02/recovery/{recovery,recovery-plan,owner-verification}.json; checks/build-evidence-readback.json

**Refutation attempted:** Preserved730 original thread logs are hash-bound before retry; recovery names eight interrupted packages including FEX with only host stamp complete, archive0df747b4…e19, and0 deleted payloads.

**Notes:** Failed01 remains failed; exact stopped-tree refreeze40f80c51→6b627a38 is retained.

### AC-503-02: A compiler/header control reproduces the failure and distinguishes ARM64-header contamination from an intrinsic i686 compiler/library incompatibility, recording exact versions and include provenance.

**Source:** #503; `inputs/issues/503.json`, body line22.
**Recorded:** 2026-10-08T08:29:51.998228+00:00
**Verdict:** PASS ✓

**Evidence:** B/sm8550-fex-controls01/headers/{inputs,control-result}.json and four raw compiler logs; checks/build-evidence-readback.json

**Refutation attempted:** Original Wayland/GL compiler commands fail with ARM64 floatn and bit_cast size error; removing only the standard ARM include yields0 and no ARMfloatn. Exact Nix2.35.2/nixpkgs/Clang21.1.8/rootfs identities match both sides.

**Notes:** Distinguishes contamination from intrinsic i686 incompatibility; no moving-channel substitute.

### AC-503-03: A scoped fix passes its unfixed/fixed controls and package/patch checks, preserves all FEX features, and yields both32-bit and64-bit guest libraries plus the target package.

**Source:** #503; `inputs/issues/503.json`, body line23.
**Recorded:** 2026-10-08T08:29:51.998256+00:00
**Verdict:** PASS ✓

**Evidence:** projects/ROCKNIX/packages/compat/fex-emu/patches/0006-guest-thunks-exclude-rebased-system-headers.patch; B/sm8550-fex-controls01/libraries/control-result.json; B/sm8550-resume04/build/fex-package.json; checks/host-controls01/pkgcheck-fex-emu.log

**Refutation attempted:** Patch removes only rebased/usr/include in guest helper. Actual CMake/Ninja original32 fails; fixed32/fixed64 succeed without ARMinclude, with6/9 isolated ELF libraries. Final target package contains nativeAArch64 plus all5/8 installed guest thunks. Fresh pkgcheck rc0; source feature/pin diff unchanged.

**Notes:** Historical exact compiler/package proof retained; native game execution is not claimed.

### AC-503-04: Resume under fresh watched build/acceptance owners; terminal results and actual artifacts pass #492's SM8550 verification. Preserve source custody and any still-open physical/publication gates.

**Source:** #503; `inputs/issues/503.json`, body line24.
**Recorded:** 2026-10-08T08:29:51.998285+00:00
**Verdict:** PASS ✓

**Evidence:** B/sm8550-resume04/terminal/{readback.json,custody.json,acceptance/artifacts/acceptance.json,sequence/controller-result.json}; checks/build-evidence-readback.json

**Refutation attempted:** Fresh distinct build04/acceptance04/controller finish with four0 channels,13/3/26 sealed inputs, actual exits, raw/update comparison and independent bundle. Failed02 wrong verifier and03 readonly Nix cache are preserved separately.

**Notes:** Physical/source-publication gates remain explicit; no new device run.

### AC-506-01: Preserve the failed verifier and terminal receipts, reproduce its wrong-path failure, and prove the corrected helper against the actual completed FEX package.

**Source:** #506; `inputs/issues/506.json`, body line13.
**Recorded:** 2026-10-08T08:29:51.998313+00:00
**Verdict:** PASS ✓

**Evidence:** B/sm8550-resume02/sequence/controller-result.json; B/sm8550-resume04/build/{original-verifier.py,proof-controls.py,proof-controls.json}; checks/build-evidence-readback.json

**Refutation attempted:** Exact original helper returns1 with FileNotFoundError guest-libs/build.ninja and writes no package receipt; corrected helper returns0 against actual Guest/Guest_32. Failed02 terminal acceptance remains1.

**Notes:** Control observes the prior failure rather than merely asserting the corrected path exists.

### AC-506-02: Both actual guest build files exclude the rebased ARM64 standard include; the exact Nix version/rootfs/toolchains and all14 installed ELF identities pass.

**Source:** #506; `inputs/issues/506.json`, body line14.
**Recorded:** 2026-10-08T08:29:51.998342+00:00
**Verdict:** PASS ✓

**Evidence:** B/sm8550-resume04/build/verify-fex.py:14–33; B/sm8550-resume04/build/fex-package.json; B/sm8550-resume04/terminal/acceptance/artifacts/fex-installed.json

**Refutation attempted:** Verifier requires nonempty INCLUDES lines from both actual Ninja files and rejects exact rebasedARMinclude; exact Nix/toolchain hashes checked. Fourteen files carry ELF class/machine, size and digest; later installed image inspection matches.

**Notes:** A successful FEX package stamp alone is insufficient and was not used as sole evidence.

### AC-506-03: A fresh watched build/acceptance owner reuses the complete FEX package and unchanged ARM output, continues firmware assembly, and records terminal results without relabeling failed02.

**Source:** #506; `inputs/issues/506.json`, body line15.
**Recorded:** 2026-10-08T08:29:51.998372+00:00
**Verdict:** PASS ✓

**Evidence:** B/sm8550-resume04/build/run.py; B/sm8550-resume04/terminal/{readback.json,build/owner-verification.json,sequence/controller-result.json}; inputs/extra-primary/sm8550-final-capacity.json

**Refutation attempted:** New owner reuses accepted package with corrected verification before assembly; final native14FEX/187ARM installed checks and four-channel acceptance hold. Failed02/03 retain original failure results.

**Notes:** Historical firmware sequence complete without relabeling failures; no current-product image claim.

## Historical device/public migration receipt read — 2026-10-08T08:35:16.288551+00:00

Directly read #500 stage input/result, reboot acceptance, and journal disposition: transfer SHA agrees before reboot; distinct boot identities and installed source43d0bc3 are retained. This is historical authorized update/physical boot evidence, with no gameplay, screenshot or deliberate cloud-test inference. Public #504 summary explicitly reports incomplete migration with insufficient terminal diagnostics, so it cannot establish provider equality or a current runtime defect. No private operational records were opened. Continue through raw filtered readbacks and scripts before criterion verdicts.

### AC-500-01: Credential-filtered preflight records the physical model/DTB, RAM voltage, predecessor BUILD_ID, boot ID, power, idle state, mounted storage and empty queue.

**Source:** #500; `inputs/issues/500.json`, body line15.
**Recorded:** 2026-10-08T08:36:47.907202+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-device-builds/rg35xxsp-adoption01/stage-preflight.txt; stage.py:34–74; inputs/issues/500.json VM-first scope

**Refutation attempted:** Read actual preflight rather than its summary: predecessor69e6039f, physical SP/DT ID,1100000 microvolts, distinct boot, charging/external power, idle process list, storage mounts and empty queue are present. Credential exclusion is implemented before retained output.

**Notes:** Named hardware fact justifies historical physical evidence. No new device read/action.

### AC-500-02: Host and device SHA256 values match the accepted update `a419dc33e1f3be2c422cac4b89d85cf104f363c3da6ed7059e0a8aa531bfd014`; device-act records transfer and checksum-gated queueing.

**Source:** #500; `inputs/issues/500.json`, body line16.
**Recorded:** 2026-10-08T08:36:47.907296+00:00
**Verdict:** PASS ✓

**Evidence:** B/rg35xxsp-adoption01/{stage-input.json,stage-transfer.log,stage-stage-result.json,stage-owner-verification.json}; stage.py:49–102

**Refutation attempted:** Host helper hashes accepted bundle before transfer; raw device output repeats exact a419dc33…014 digest and1320970240 bytes before queue rename. device-act names transfer and retains rc0/unchanged boot. Empty queue is rechecked before move.

**Notes:** Stage evidence alone does not establish installation.

### AC-500-03: The authorized device-act reboot has a subsequent changed boot ID and readback of pixelelated 0.0.1 / BUILD_ID `43d0bc3bf47fd858ba8d5c55fbdf52535a0db2aa`, expected model/DTB, LPDDR4 voltage, storage mounts, exact installed binary hashes and empty update queue.

**Source:** #500; `inputs/issues/500.json`, body line17.
**Recorded:** 2026-10-08T08:36:47.907338+00:00
**Verdict:** PASS ✓

**Evidence:** B/rg35xxsp-adoption01/{reboot-reboot.log,reboot-installed-readback.txt,reboot-acceptance.json,reboot-owner-verification.json}; reboot-verify.py:31–104

**Refutation attempted:** One device-act reboot follows power/idle/queue/hash checks. Raw installed readback has new bf8756cd boot, exact43d0bc3 source, seven payload/bootloader hashes bound to accepted DDR4 artifact, original mounts, queue0 and active interface. Does not reuse staging boot or infer success from SSH alone.

**Notes:** Physical boot/update proof only, not current ES4e410 firmware.

### AC-500-04: Compact evidence, standing hardware fact and work log record the actual outcome; broader device smoke and release gates remain separately identified.

**Source:** #500; `inputs/issues/500.json`, body line18.
**Recorded:** 2026-10-08T08:36:47.907376+00:00
**Verdict:** PASS ✓

**Evidence:** B/rg35xxsp-adoption01/{request.md,README.md,journal-disposition.json}; docs/releases/device-facts.md H700 row; docs/work-logs/2026_10-work_logs/2026_10_07-work_log.md:912,926

**Refutation attempted:** Journal disposition compares existing scheduler/audio warnings to predecessor; no failed units or service restarts. Standing fact/work log name physical fact and explicit gameplay/cloud/RC exclusions.

**Notes:** Broader smoke/release obligations remain separate.

### AC-501-01: Record the complete initial legacy-folder dialog text and buttons from the shipped ES pin.

**Source:** #501; `inputs/issues/501.json`, body line13.
**Recorded:** 2026-10-08T08:36:47.907404+00:00
**Verdict:** PASS ✓

**Evidence:** ES72494bc72:es-app/src/guis/GuiMenu.cpp:5364–5412; inputs/issues/501.json Findings

**Refutation attempted:** Direct git-show of shipped pin matches both paragraphs and all three buttons in source order, with paths produced from current/source state. No separate heading is introduced by this GuiMsgBox call.

**Notes:** Requested historical wording inventory only; current source later retires dialog.

### AC-501-02: Trace the dynamic text after TRANSFERRING and compare full-screen backup/restore with automatic-sync cards.

**Source:** #501; `inputs/issues/501.json`, body line14.
**Recorded:** 2026-10-08T08:36:47.907431+00:00
**Verdict:** PASS ✓

**Evidence:** ES72494bc72:CloudTransferJob.cpp:535–558, GuiCloudTransfer.cpp:939–984, ThreadedCloudSync.cpp:380–430; inputs/issues/501.json Findings

**Refutation attempted:** Parser keeps basename case and separates file progress; shared full-screen renderer tries progressively smaller filename/stat segments. Automatic card instead builds sending/receiving file-count labels. Comparison correctly avoids claiming all cards have identical copy.

**Notes:** Source tracing suffices for requested copy comparison; no frame geometry claim.

### AC-501-03: Compare capitalization and vocabulary against canonical rules; keep this a review without changing player-facing strings.

**Source:** #501; `inputs/issues/501.json`, body line15.
**Recorded:** 2026-10-08T08:36:47.907456+00:00
**Verdict:** PASS ✓

**Evidence:** .claude/rules/es-player-text.md; .claude/rules/es-ui-style-guide.md; inputs/issues/501.json Findings; git diff for subsequent#502 change

**Refutation attempted:** Capitalized labels/status and lowercase brand exception agree with rules; player filename remains data. Original request remains review-only, with implementation authorized separately in#502.

**Notes:** No new wording change made by this audit.

## Historical copy frame observation — 2026-10-08T08:37:28.772648+00:00

Directly viewed#502 EN/FR640×480 retained prompt frames. Complete previous-OS question, lowercase brand/quoted paths, conditional other-device sentence, remaining-files exception and all three buttons fit. This verifies historical5d2fcb9 copy surface only; current#508 retires it. Source diff is exactly GuiMenu string plus French catalog; no behavior change. Required device-act receipts are in stage-transfer.log/reboot-reboot.log rather than nonexistent guessed JSON filenames.

### AC-502-01: Source trace distinguishes the move, upgrade prerequisite, automatic following, and residual-file merge: cloud_migrate_layout relocate(), layout_follow(), and merge_into().

**Source:** #502; `inputs/issues/502.json`, body line57.
**Recorded:** 2026-10-08T08:39:05.262003+00:00
**Verdict:** PASS ✓

**Evidence:** candidate16:projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:498–578,583–648,948–984; inputs/issues/502.json

**Refutation attempted:** Direct historical code requires copy/check/pointer success before list-bound deletion; follow refuses residual files or explicit keep and preserves independent content selection. Merge shelves differing data before newer-wins copy. Thus conditional switching and remaining-files confirmation are distinct.

**Notes:** Historical trace; automatic migration/follow are retired from frozen current product.

### AC-502-02: Renderer/font evidence answers the clarified styling question: Markdown is unsupported in this dialog; literal quotation marks have font coverage.

**Source:** #502; `inputs/issues/502.json`, body line58.
**Recorded:** 2026-10-08T08:39:05.262116+00:00
**Verdict:** PASS ✓

**Evidence:** ES72494:es-core/src/guis/GuiMsgBox.cpp and components/TextComponent.cpp:342–413; docs/qa-logs/2026-10-07-migration-copy/source-diff.patch; actual EN/FR640 prompt frames

**Refutation attempted:** GuiMsgBox uses ordinary TextComponent font text cache; no Markdown parsing step. Viewed literal curly quotes render on both target frames rather than relying on host font coverage alone.

**Notes:** C++ Unicode escapes work around actual xgettext raw-comment/string issue without adding a parser.

### AC-502-03: Capture PREVIOUS OS / MOVE THE FOLDER, automatic switching once running pixelelated and online, and the residual-file confirmation exception (D-UI-122, D-UI-123).

**Source:** #502; `inputs/issues/502.json`, body line59.
**Recorded:** 2026-10-08T08:39:05.262158+00:00
**Verdict:** PASS ✓

**Evidence:** docs/decision-register.md D-UI-122/123; inputs/issues/502.json exact request; docs/qa-logs/2026-10-07-migration-copy/source-diff.patch

**Refutation attempted:** Diff preserves previous-OS/move terminology, explicit pixelelated/network condition and remaining-files exception. The wording specifies folder switching, not automatic OS installation.

**Notes:** Superseded by later authorized retirement, not silently reverted.

### AC-502-04: Revised English/French source uses PREVIOUS OS / MOVE THE FOLDER and explains automatic cloud-folder switching once running pixelelated and online, with the residual-file confirmation exception; /pixelelated, existing behavior, and all choices stay unchanged. Syntax/localization checks pass. Sweep the old prompt in GuiMenu.cpp and the French catalog; no Markdown parser is introduced.

**Source:** #502; `inputs/issues/502.json`, body line60.
**Recorded:** 2026-10-08T08:39:05.262190+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-migration-copy/source-diff.patch; runs/pixelelated-m7-migration-copy02/artifacts/{syntax,vocabulary,msgfmt,xgettext}.log; runs/pixelelated-m7-migration-copy03/watcher/20261007T151900Z-083996c5/build.rc and artifacts/link.log; checks/build-evidence-readback.json

**Refutation attempted:** Exact historical diff changes one prompt and its French msgstr, preserving callbacks/choices; source/catalog compile checks retained. Failed02 final link is preserved and subsequent03 successful link separately identified. No migration behavior source change or Markdown parser.

**Notes:** Historical changed-source check evidence; no pointless rebuild of now-retired UI. Packet hashes independently reverified.

### AC-502-05: VM frames at640x480 show complete English/French prompts and buttons without clipping; changed-image qualification is scoped separately from already accepted candidate16 evidence.

**Source:** #502; `inputs/issues/502.json`, body line61.
**Recorded:** 2026-10-08T08:39:05.262219+00:00
**Verdict:** PASS ✓

**Evidence:** docs/qa-logs/2026-10-07-migration-copy/runs/pixelelated-m7-migration-copy-vm04/artifacts/{640x480-en_US,640x480-fr_FR}/01-prompt.png; acceptance.json; checks/build-evidence-readback.json

**Refutation attempted:** Direct frame review shows complete sentences and all buttons without clipping in both640×480 locales. Frame hashes match retained acceptance; candidate16 base vs5d2fcb9 source-overlay qualification remain distinct.

**Notes:** No claim that candidate16 image already contained revised copy.

### AC-504-01: A compact, credential-filtered local readback records boot identity, service state, migration process presence/absence, migration status and relevant local pointer fields, with capture time.

**Source:** #504; `inputs/issues/504.json`, body line13.
**Recorded:** 2026-10-08T08:39:05.262257+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/504.json; B/rg35xxsp-migration-review01/PUBLIC-SUMMARY.md

**Refutation attempted:** Public scope identifies raw local state as private; this audit explicitly excludes personal operational inventory. No public summary promoted to independent raw-readback evidence.

**Notes:** Private historical observation intentionally outside this audit's disclosure/access boundary, not a new product failure.

### AC-504-02: Retained local migration/scan/sync logs establish success, ongoing work, or a named uncertainty; an absent process alone never counts as success, and provider contents are not asserted without evidence.

**Source:** #504; `inputs/issues/504.json`, body line14.
**Recorded:** 2026-10-08T08:39:05.262283+00:00
**Verdict:** SKIP ○

**Evidence:** B/rg35xxsp-migration-review01/PUBLIC-SUMMARY.md; inputs/issues/504.json

**Refutation attempted:** Summary explicitly says incomplete and cause unknown; absent process or discarded tier marker is not treated as success. Private logs not opened.

**Notes:** Preserve named uncertainty; no provider-state inference.

### AC-504-03: Existing upgrade warnings are compared against #500/predecessor evidence; findings and limitations identify any actionable issue and durable learning.

**Source:** #504; `inputs/issues/504.json`, body line15.
**Recorded:** 2026-10-08T08:39:05.262310+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** B/rg35xxsp-adoption01/journal-disposition.json; B/rg35xxsp-migration-review01/PUBLIC-SUMMARY.md; inputs/issues/504.json

**Refutation attempted:** Public predecessor journal confirms known scheduler/audio warnings, while migration cause remains unknown and#505 owns diagnostics. Private later readbacks cannot be independently compared within current boundary.

**Notes:** Public claim limits are sound; private comparison excluded.

**Gaps:** Independent verification of later private warning comparison is outside authorized public audit scope; retain no product-bug inference.

### AC-504-04: Sanitized evidence and its source-reading commands are retained under `docs/qa-logs/2026-10-07-device-builds/rg35xxsp-migration-review01/`; the issue records the outcome and links any required follow-up.

**Source:** #504; `inputs/issues/504.json`, body line16.
**Recorded:** 2026-10-08T08:39:05.262336+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** B/rg35xxsp-migration-review01/PUBLIC-SUMMARY.md and actual directory inventory; inputs/issues/504.json follow-up

**Refutation attempted:** Source/public summary preserves outcome and#505 link, but body criterion still describes a fuller sanitized repository packet while current packet deliberately withholds private commands/readbacks/screens. Historical source custody is private, not proved by public path alone.

**Notes:** Track literal criterion/public-custody wording in Phase3 with private-boundary constraints.

**Gaps:** Reconcile criterion to intentional private custody and public summary; do not publish private payload to satisfy stale wording.

### AC-504-05: `power-readback.txt` and `power-counters-readback.txt` correlate the migration with existing suspend/resume/network evidence and state explicitly what cannot be inferred.

**Source:** #504; `inputs/issues/504.json`, body line32.
**Recorded:** 2026-10-08T08:39:05.262361+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/504.json; B/rg35xxsp-migration-review01/PUBLIC-SUMMARY.md

**Refutation attempted:** Private power/network readbacks are not opened. Public statement differentiates process sleep/screensaver from physical suspend and does not assert historical charging state from current state.

**Notes:** Private observation excluded; no new physical action authorized.

## Validator source observation — 2026-10-08T08:39:36.331136+00:00

Read cloud_folder_validate lines1–210: bounded drain/time/process-group cleanup, selected-root-only rclone listings, strict entry validation, recognized deeper save subtrees, ordinary progress allowlist, category-aware content exclusions and deliberate readiness-not-integrity wording. Broad historical filename inventory accidentally returned many paths but no old per-AC verdict content was opened. Limited subsequent searches to product subtree. Historical copy link03 evidence path corrected to actual watcher rc/link.log.

## Validator completion and scan observation — 2026-10-08T08:39:57.084705+00:00

Remaining validator source retains per-category unreadable state, bucket empty-presence uncertainty, deeper-unchecked guards and before/after config identity. Scan diff introduces run/config/result-bound completion records and a parent-held flock with child descriptor closed; retires automatic join/follow and account-root discovery. Need inspect setup creation lock and actual content selection code next; truncated combined diff is not complete evidence.

## Setup/create and progress separation observation — 2026-10-08T08:40:26.892533+00:00

Read validation_context and selected-category seeding: only config digest exported, category allowlist rejects duplicates, explicit creation names only selected roots and preserves existing README via ignore-existing. Seeding snapshots paths; no automatic create follows link. Current product search finds no migration/repair symbol in runtime rclone/helper sources. Content backup adds PSP progress exclusions in ordinary and special gamelist passes; N64 native states are limited to system root. Check scanner/restore callers and target regressions before grading.

## Restore/save boundary observation — 2026-10-08T08:40:52.977530+00:00

Directly read selected content-root validation, shared PSP and root-only N64 exclusions, dedicated gamelist filters, normal restore loop and ordinary progress allowlist. Both copy and media passes carry progress exclusion; per-system exclusions reset each iteration. Remaining runtime assertions require sealed VM readback; current-host145 controls alone are not target proof.

## DuckStation implementation observation — 2026-10-08T08:41:18.518446+00:00

Read full screenshot-path helper and game launcher. Helper modifies only absent/empty/exact default screenshot setting, preserves custom and old-default symlink choice, bounds config, verifies real target write, atomically replaces unchanged config identity and never relocates old captures. Existing launcher emits warning and continues on helper refusal. Recipe explicitly installs executable AppImage and declares Python3/libcom-err. Actual-image applet packet explicitly uses image find/awk plus host bash/Python/rclone; it is not a whole guest test.

## Cloud packet integrity readback — 2026-10-08T08:41:51.084674+00:00

Independently rehashed all three UI SHA256SUMS packets and host capture packet, and compared26 integrated product paths/modes to frozen tree; all match checks/cloud-packet-readback.json. Direct raw guest mode refusal is126, after chmod distinct loader failure127 missinglibcom_err.so.2; neither is mislabeled native screenshot success.

## Native screenshot and selected-root target receipt observation — 2026-10-08T08:42:36.334325+00:00

Read actual capture/default/custom/roundtrip receipts: native640×480 PNG created by Guide+B, exact bytes restored after separate synthetic cloud backup, historical/custom files preserved, settings/content pointers unchanged. This is a synthetic rendering ROM, not gameplay proof. Read target libcom_err ELF: x86_64 SONAME libcom_err.so.2,14480 bytes SHA043101a8…938a3 installed via existing project package. Read current#520 guest validation and source/binary/catalog hashes; selected saves present and progress-only ROMs empty, both scan stamps valid.

## Target visual observation — 2026-10-08T08:43:13.374302+00:00

Viewed actual PSP and beyond-depth640×480 cloud check frames: full readiness caveat, per-category paths, present/empty vs unreadable states fit. Viewed DuckStation default hotkey frame showing saved-PNG OSD over synthetic rendering. Native PNG path guessed under frames was absent; consult index before asserting direct native-image review. Read upgrade rules merge: custom active rules preserved first, historically inert rules stay inert, defaults appended atomically and catch-all verified.

## Writer primary source readback — 2026-10-08T08:45:03.625144+00:00

Verified exact-tag cached DuckStation source digests and directly read settings/default-relative screenshot/card resolution and SaveScreenshot writer. Read pinned PPSSPP savedata prefix and ms0 mount plus shipped patch; read pinned Mupen64Plus slot filenames and0–9 bound with current launcher/config chain. Direct native PNG is uniform synthetic orange640×480, distinct from screenshot OSD frame. No gameplay compatibility claim.

### AC-520-01: A full writer/launcher/config source chain and synthetic path table confirm actual current paths/extensions; historical and currently supported layouts are distinguished. A helper name alone does not establish runtime behavior.

**Source:** #520; `inputs/issues/520.json`, body line24.
**Recorded:** 2026-10-08T08:45:03.643588+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md C1–C10; coverage/writer-trace.json; checks/writer-source-readback.json; pinned PPSSPP SavedataParam.cpp:49 and sceIo.cpp:667; Mupen64Plus savestates.c:80–145; DuckStation settings.cpp:2489–2510,2730

**Refutation attempted:** Followed real writer prefixes through mount/config/launcher, rather than relying on PPSSPP DIRECTORY_SAVEDATA helper name. Native states have bounded0–9 suffixes; DuckStation .mcd native and .mcr compatibility distinguished.

**Notes:** Finite supported writer inventory, not exhaustive emulator compatibility audit.

### AC-520-02: Real-rclone unfixed controls demonstrate each confirmed omission/misclassification. Fault/input witnesses prevent a sandbox/startup failure from counting as the expected failure.

**Source:** #520; `inputs/issues/520.json`, body line25.
**Recorded:** 2026-10-08T08:45:03.643670+00:00
**Verdict:** PASS ✓

**Evidence:** S2/coverage/{unfixed02,unfixed-n64-01,media-gap01}/summary.json and per-case raw operation/fixture-check logs; checks/cloud-controls01/save-layout.log

**Refutation attempted:** Unfixed PSP/Duck controls have rc0 fixture and filter invocation then missing expected payload, not startup failure. Separate N64 five failures and media two failures survive input witnesses; current39 controls pass, including actual real-rclone outputs.

**Notes:** Earlier unfixed01 startup failure is explicitly excluded as a product-failure witness.

### AC-520-03: Both rules/defaults and upgrade merge preserve existing custom rules while admitting the supported save paths; intended ROM/BIOS/database exclusions remain intact and compatibility paths still work.

**Source:** #520; `inputs/issues/520.json`, body line26.
**Recorded:** 2026-10-08T08:45:03.643712+00:00
**Verdict:** PASS ✓

**Evidence:** rclone/sources/cloud_sync-rules.txt:45–61 and defaults; cloud_sync_helper:47–183; checks/cloud-controls01/save-layout/upgrade-custom-rules; S2/coverage/final03/upgrade-custom-rules

**Refutation attempted:** Current real-rclone fixture verifies active custom rules and supported defaults after merge, preserving database/ROM/BIOS exclusions and compatibility paths. Existing inert-after-catch-all rules are not awakened. Atomic candidate checks preserve catch-all.

**Notes:** rclone shorthand denotes projects/ROCKNIX/packages/network/rclone.

### AC-520-04: Save backup/restore preserve synthetic payload bytes at the correct paths; content backup/restore/list/count/match do not copy, overwrite or remove those progress files. Colliding/stale remote content copies cannot replace local progress.

**Source:** #520; `inputs/issues/520.json`, body line27.
**Recorded:** 2026-10-08T08:45:03.643754+00:00
**Verdict:** PASS ✓

**Evidence:** checks/cloud-controls01/save-layout.log and save-layout cases; S2/coverage/final03/save-backup-restore; content-{upload,restore,match} cases; coverage/image-applets02; ui/receipts/content02/{validation.json,after.txt,scan-readback.txt}

**Refutation attempted:** Positive payloads and hostile stale/colliding remote progress are populated before both directions;39 current controls preserve progress and legitimate unrelated content. Image find/awk nine controls guard host-tool divergence; actual guest selected-root scan sees saves present/ROMs empty with unchanged inventories. Neither empty transfers nor summary-only success suffices.

**Notes:** Source-overlay/finite synthetic behavior established; assembled final firmware remains#508 CF10.

### AC-520-05: Validator classification uses the same supported layout, honors bounded depth without claiming unseen bytes were verified, and remains read-only. Applicable canonical flow/reference and unchanged/affected UI evidence accompany the final source.

**Source:** #520; `inputs/issues/520.json`, body line28.
**Recorded:** 2026-10-08T08:45:03.643783+00:00
**Verdict:** PASS ✓

**Evidence:** rclone/sources/cloud_folder_validate:24–278; checks/cloud-controls01/{validator,save-layout}.log; S2/ui/evidence-index.json and frames/psp-en640.png,depth-bound-en640.png; docs/pixelelated/cloud-folder-flow-review.md

**Refutation attempted:** Bounded named subtrees accept ordinary PSP/card depth but deeper unknown folders produce unreadable. Fresh timeout/entry/byte/subtree failure controls pass. Direct actual frames show caveat and unreadable branch; target read-only config/provider hashes retained.

**Notes:** Present is readiness only, never completeness or loadability.

### AC-520-06: #515's case table and #508/#507 scope reference the qualified fix, with compact source-bound receipts and explicitly remaining firmware inclusion/adoption gates.

**Source:** #520; `inputs/issues/520.json`, body line29.
**Recorded:** 2026-10-08T08:45:03.643809+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md final disposition; S2/integration/prepared-product-inputs.json; inputs/issues/{515,508,507}.json; checks/cloud-packet-readback.json

**Refutation attempted:** 26 exact integrated paths/modes match frozen tree and ES4e410 pin; current-image/public-adoption gates remain explicitly open. No obsolete source-overlay source name used as installed firmware claim.

**Notes:** S2 denotes docs/qa-logs/2026-10-08-save-repair-cases.

### AC-521-01: Exact pinned action/writer/config/launcher evidence identifies the default path on GENERIC_X64 and H700; a synthetic old-launcher control demonstrates exclusion from the normal screenshot/save scope.

**Source:** #521; `inputs/issues/521.json`, body line23.
**Recorded:** 2026-10-08T08:45:03.643838+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md DuckStation screenshot chain; checks/writer-source-readback.json; DuckStation config/H700,InputPlumber; S2/duckstation-captures/old02/clean-game-InputPlumber/{01-operation.json,final.json}

**Refutation attempted:** Pinned writer resolves unset/relative screenshots against redirected data root, while shipped controls bind real action. Old launcher fixture genuinely creates synthetic capture outside save scope and preserves historical capture; four expected failures separately retained.

**Notes:** Native screenshot test later confirms actual action, not just helper naming.

### AC-521-02: A bounded, reviewed implementation directs new default screenshots into the covered tree on clean and retained default configurations, preserves explicit custom paths and all existing screenshot bytes, and remains safe on repeated launch, conflicting/unwritable paths and failure.

**Source:** #521; `inputs/issues/521.json`, body line24.
**Recorded:** 2026-10-08T08:45:03.643863+00:00
**Verdict:** PASS ✓

**Evidence:** duckstation-sa/scripts/duckstation_screenshot_path:15–137; both launcher call sites; checks/cloud-controls01/duckstation.log

**Refutation attempted:** Fresh31 controls include missing/retained defaults, explicit custom paths, repeated launch, duplicate/invalid config, conflicting or unwritable target and preserved history. Helper probes write, checks config identity and atomically replaces only known default; no old capture relocation.

**Notes:** Launcher continues with clear stderr on refusal; arbitrary custom capture paths deliberately remain outside default save coverage.

### AC-521-03: Source-derived fixtures prove actual launcher/config behavior and old-capture retention, rather than only testing a mirrored helper; backup/restore coverage is shown with real rclone.

**Source:** #521; `inputs/issues/521.json`, body line25.
**Recorded:** 2026-10-08T08:45:03.643889+00:00
**Verdict:** PASS ✓

**Evidence:** tools/pixelelated-duckstation-capture-test; checks/cloud-controls01/duckstation; S2/duckstation-captures/vm-ui/receipts/capture-roundtrip01/results.json and native-receipts01/roundtrip

**Refutation attempted:** Tests run actual launcher/package hook with executable stub boundary, then real guest executes actual AppImage hotkey separately. Native PNG roundtrip hash0f2f266e…46b3, historical/custom hashes preserved; no mirrored helper substituted as runtime proof.

**Notes:** Fresh host controls31/31; historical actual guest roundtrip independently read and sealed packet rehashed.

### AC-521-04: Applicable target-runtime screenshot/flow proof and canonical reference/changelog disposition accompany the source, with exact inputs and limits. No whole-library operation or private-device/cloud action is needed.

**Source:** #521; `inputs/issues/521.json`, body line26.
**Recorded:** 2026-10-08T08:45:03.643918+00:00
**Verdict:** PASS ✓

**Evidence:** S2/duckstation-captures/vm-ui/evidence-index.json,frames/default-hotkey.png,captures/native-default.png,receipts/capture-{default01,custom01}/capture.json; docs/pixelelated/cloud-folder-flow-review.md DuckStation section; docs/cloud-sync-changelog.md

**Refutation attempted:** Direct target OSD/native PNG review and actual pad events prove screenshot writer on exact AppImage/helper/library overlay. Custom destination emits separate native capture without moving default/history. Synthetic rendering restriction explicit, no commercial gameplay or full image claim.

**Notes:** Source/binary/panel/source-overlay references accompany affected flow.

### AC-521-05: #515 case disposition and #508/#507 final scope include the qualified change and explicitly remaining firmware inclusion gates.

**Source:** #521; `inputs/issues/521.json`, body line27.
**Recorded:** 2026-10-08T08:45:03.643942+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md; S2/integration/prepared-product-inputs.json; inputs/issues/{508,507,515}.json; checks/cloud-packet-readback.json

**Refutation attempted:** Final manifest includes helper/config/launchers, mode and dependency recipe at052771; integratede6645 contained in frozenac64. Future firmware inclusion remains open.

**Notes:** Capture implementation qualified without inventing a generic repair API.

### AC-522-01: Retained actual-image readback proves the original pinned bytes/mode and direct execution refusal; source trace identifies the mode-preserving package operation.

**Source:** #522; `inputs/issues/522.json`, body line22.
**Recorded:** 2026-10-08T08:46:05.519698+00:00
**Verdict:** PASS ✓

**Evidence:** S2/duckstation-captures/installed-mode-and-refusal.txt; frozen-inputs.json; candidate16 duckstation-sa/package.mk makeinstall_target

**Refutation attempted:** Actual guest exact AppImage SHA b204886b…f7b had0644 mode, test executable1 and direct entrypoint126 Permission denied. Original recipe cp preserved mode; this is distinct from later library127 failure.

**Notes:** No inference from source mode alone.

### AC-522-02: A package install fixture starts with mode0644 and proves final mode0755 plus byte identity, with an unfixed recipe control that fails the same assertion. Package lint passes.

**Source:** #522; `inputs/issues/522.json`, body line23.
**Recorded:** 2026-10-08T08:46:05.519813+00:00
**Verdict:** PASS ✓

**Evidence:** duckstation-sa/package.mk:28; tools/pixelelated-duckstation-capture-test package-executable-mode; checks/cloud-controls01/duckstation.log; checks/host-controls01/pkgcheck-duckstation-sa.log

**Refutation attempted:** Actual recipe hook starts from0644 artifact and current install-m0755 preserves hash; unfixed copied mode fails executable assertion. Fresh31-case suite and pkgcheck return0.

**Notes:** No AppImage stripping introduced.

### AC-522-03: The actual guest receives the qualified packaged file/mode and can execute the real AppImage entrypoint. Record any distinct downstream runtime prerequisite honestly; permission repair alone is not screenshot/gameplay proof.

**Source:** #522; `inputs/issues/522.json`, body line24.
**Recorded:** 2026-10-08T08:46:05.519857+00:00
**Verdict:** PASS ✓

**Evidence:** S2/duckstation-captures/runtime-loader-refusal.txt; vm-ui/receipts/native-receipts01/final-readback.txt and native-default.log; capture-default01/capture.json

**Refutation attempted:** After mode repair raw guest shows755 same bytes, then honest missinglibcom_err refusal. Final exact target library overlay runs real AppImage and produces native screenshot; permission fix alone never used as screenshot evidence.

**Notes:** Synthetic display proof; gameplay and assembled-image inclusion separate.

### AC-522-04: #521 proof and #508/#507 scope include the fixed package input; final firmware inclusion remains separately gated.

**Source:** #522; `inputs/issues/522.json`, body line25.
**Recorded:** 2026-10-08T08:46:05.519897+00:00
**Verdict:** PASS ✓

**Evidence:** S2/integration/prepared-product-inputs.json; S2/duckstation-captures/dependency-final-inputs.json; inputs/issues/{521,508,507}.json; checks/cloud-packet-readback.json

**Refutation attempted:** Manifest byte/mode comparison binds packaged executable correction and downstream dependency at final052771, integrated intoe6645/ac64. Final firmware gate remains open.

**Notes:** No current firmware falsely certified.

### AC-523-01: Original actual-guest failure, exact artifact and loader dependency/source trace are retained, separating executable permission from loader readiness.

**Source:** #523; `inputs/issues/523.json`, body line22.
**Recorded:** 2026-10-08T08:46:05.519925+00:00
**Verdict:** PASS ✓

**Evidence:** S2/duckstation-captures/{runtime-loader-refusal.txt,runtime-initial-elf-closure.json,dependency-final-inputs.json}

**Refutation attempted:** Actual entrypoint returns127 missinglibcom_err with executable bit fixed. Five of121 bundled ELF dependency chains report that library absent; original artifact identity retained, preventing permission/library failures being conflated.

**Notes:** Loader closure inspected beyond only main executable.

### AC-523-02: Recipe declares the required runtime closure using project packages; pkgcheck and target package/install evidence prove library bytes/architecture/SONAME and placement. Existing frozen build owners and global source caches are unchanged.

**Source:** #523; `inputs/issues/523.json`, body line23.
**Recorded:** 2026-10-08T08:46:05.519955+00:00
**Verdict:** PASS ✓

**Evidence:** duckstation-sa/package.mk:8; S2/duckstation-captures/dependency-build/{build_target,install_target,target-artifacts.json}; dependency-toolchain-inputs.json; checks/host-controls01/pkgcheck-duckstation-sa.log

**Refutation attempted:** Existing project libcom-err package produced x86_64 ELF SONAMElibcom_err.so.2 at six package/image paths, exact043101a8…938a3. Isolated dependency owner and recorded toolchain/source identities avoid mutating frozen device owners. Fresh pkgcheck0.

**Notes:** Actual target build/install evidence, not host library copy.

### AC-523-03: Actual owned GENERIC_X64 proof starts the real AppImage with the qualified target libraries and no missing required dependencies; #521's screenshot writer proof resumes on that exact overlay. Any unrelated runtime restriction is named, not silently passed.

**Source:** #523; `inputs/issues/523.json`, body line24.
**Recorded:** 2026-10-08T08:46:05.519987+00:00
**Verdict:** PASS ✓

**Evidence:** S2/duckstation-captures/vm-ui/receipts/duck-deps01/all-elf-closure-complete.json; native-receipts01/{final-readback.txt,native-default.log}; vm-ui/terminal-channels.json; pinned-help-exit.json

**Refutation attempted:** All121 final bundled ELF closures have exit0 and no missing issues. Actual native default/custom capture owners have four0channels. Help returns1 by exact source design; failed aggregate preserved. Synthetic display provides only native writer proof, no commercial game or BIOS compatibility claim.

**Notes:** Source overlay and all input hashes retained.

### AC-523-04: #508 integration/#507 audit/final firmware inclusion manifest name the dependency inputs and preserve separate source-overlay versus assembled-image qualification.

**Source:** #523; `inputs/issues/523.json`, body line25.
**Recorded:** 2026-10-08T08:46:05.520016+00:00
**Verdict:** PASS ✓

**Evidence:** S2/integration/prepared-product-inputs.json; S2/duckstation-captures/dependency-final-inputs.json; inputs/issues/{508,507}.json; checks/cloud-packet-readback.json

**Refutation attempted:** Manifest exact recipe adds project dependency and records accepted library identity; frozen source comparison matches. Future firmware assembly/inclusion explicitly pending rather than borrowed from accepted candidate16.

**Notes:** No new build launched by audit.

## ES protocol/source observation — 2026-10-08T08:48:07.987500+00:00

Read CloudFolderValidation parser and actual folder selection/result handlers: strict JSON/selected/run/config identity, bounded65KiB output, unreadable cannot become completed, explicit category choice and two stale-context checks around creation consent. Current folder validator suite exercises explicit creation; old pixelelated-cloud-folder-test retains obsolete no-argument seeding assumptions, so its unsupported unadapted suite is not a current contract oracle. Prepared finite exact4e410 unit/syntax/catalog/menu checks under fresh watched owner.

## Integrity tool/code and ES check observation — 2026-10-08T08:49:17.389565+00:00

Read complete offline integrity verifier and public protocol: bounded manifests/payloads/decompression, stable identity/hash requirement, failure-discriminating per-file outcomes and always-unverified playability. It intentionally cannot prove collector scope/truthfulness; private collection remains outside this audit. Exact4e410 host ES checks completed rc0 with unchanged source hashes; four terminal channels/host exits retained.

### AC-517-01: A scoped inventory binds current cloud size/hash/identity before and after reads; bounds, unsupported hashes, changed files, download failures and exclusions cannot be reported as passes. Raw records remain private.

**Source:** #517; `inputs/issues/517.json`, body line17.
**Recorded:** 2026-10-08T08:50:18.295855+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/517.json; docs/cloud-save-integrity.md; tools/cloud-save-integrity:147–183

**Refutation attempted:** Private collection/inventories explicitly excluded. Public verifier rejects identity drift and unsupported hashes but expressly cannot prove collector scope; no private inventory claim inferred from24 synthetic passes.

**Notes:** Operational private criterion outside selected disclosure boundary.

### AC-517-02: Downloaded save-tree bytes match provider hashes; compare local counterparts read-only and distinguish equal, differing, absent and unreadable. No direction/winner is inferred from timestamps alone.

**Source:** #517; `inputs/issues/517.json`, body line18.
**Recorded:** 2026-10-08T08:50:18.295965+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/517.json; docs/cloud-save-integrity.md procedure3–5

**Refutation attempted:** Neither private payloads nor local counterparts opened. Source protocol distinguishes bytes, structure and desired progress without timestamp winner inference.

**Notes:** No new personal cloud/device reads.

### AC-517-03: Recognized file types receive structural checks with explicit limits. Raw/core-specific saves without a parser remain unverified for game semantics; per-file outcomes separate byte integrity, structural integrity and playability.

**Source:** #517; `inputs/issues/517.json`, body line19.
**Recorded:** 2026-10-08T08:50:18.296023+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** tools/cloud-save-integrity:48–145,179–201; checks/cloud-controls01/integrity.log; docs/cloud-save-integrity.md

**Refutation attempted:** Read all PNG/RZIP/RASTATE parsers and bounded decompression; raw/core semantics and playability remain unverified. Fresh24 synthetic cases include invalid supported containers and hash failures. Private per-file outcomes are intentionally not independently re-read.

**Notes:** Reusable verifier semantics verified; private invocation result outside scope.

**Gaps:** No independent public-audit assertion about private files' structural outcomes.

### AC-517-04: Disposable synthetic controls prove the verifier accepts valid data and rejects changed/truncated/missing files, incorrect hashes and invalid supported containers. No corruption is injected into personal originals.

**Source:** #517; `inputs/issues/517.json`, body line20.
**Recorded:** 2026-10-08T08:50:18.296061+00:00
**Verdict:** PASS ✓

**Evidence:** tools/cloud-save-integrity-test; checks/cloud-controls01/integrity.log and results.json; tools/cloud-save-integrity

**Refutation attempted:** Fresh24 synthetic controls accept valid data and reject missing/truncated/changed/hash-mismatch/container defects, including independent real-rclone Dropbox hash boundary controls. Uses only disposable local data.

**Notes:** No personal original corrupted or replaced.

### AC-517-05: Exact installed-source tracing lists local config/recovery state written by the migration and any local payload effects. A concrete proposed alignment names files/keys and old/new behavior; no device mutation, reboot or sync occurs without separately named approval.

**Source:** #517; `inputs/issues/517.json`, body line21.
**Recorded:** 2026-10-08T08:50:18.296089+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/{517,519}.json; docs/cloud-save-integrity.md Carry-forward

**Refutation attempted:** Private installed-state trace/alignment values are outside audit boundary. Public#519 correctly requires concrete plan and separate device authority, no completed alignment inferred.

**Notes:** Generic deployment gate reviewed under#519 below.

### AC-517-06: A redacted report and private per-file evidence explain findings and remaining limits, retaining the earlier log checks. Large-library verification remains outside this small-save scope and requires separate explicit planning; independent backup redundancy is tracked in #518; no product validator readiness result is mislabeled a full-content check.

**Source:** #517; `inputs/issues/517.json`, body line22.
**Recorded:** 2026-10-08T08:50:18.296119+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** docs/qa-logs/2026-10-08-save-integrity/README.md; docs/cloud-save-integrity.md; inputs/issues/517.json

**Refutation attempted:** Public report/protocol expressly distinguish readiness, current bytes, historical progress and independent redundancy; private per-file evidence is not inspected. Large library verification/redundancy stay separate.

**Notes:** Public claim boundaries hold.

**Gaps:** Private report outcomes deliberately excluded from independent verdict; do not republish inventory to manufacture PASS.

### AC-517-07: Useful manual findings become host synthetic controls and a documented protocol; #515/#508 explicitly carry the relevant repair/adoption cases without personal fixtures or expanding setup into full-library verification.

**Source:** #517; `inputs/issues/517.json`, body line28.
**Recorded:** 2026-10-08T08:50:18.296145+00:00
**Verdict:** PASS ✓

**Evidence:** tools/cloud-save-integrity and cloud-save-integrity-test; docs/cloud-save-integrity.md; S2/source-cases.md:210; inputs/issues/{515,508}.json; checks/cloud-controls01/integrity.log

**Refutation attempted:** Manual learning is concretely a public offline tool/protocol with24 fresh controls. Carry-forward explicitly requires source-derived layouts and preservation; no personal fixture or whole-library product validation feature introduced.

**Notes:** No ES visual change owed for offline host tool.

### AC-519-01: A source-cited private state/residue manifest and concrete per-key/per-path plan distinguishes keep/archive/remove and preserves personal saves, credentials, active metadata and recovery copies. #516's relevant classification is incorporated; unknown residue is not silently deleted.

**Source:** #519; `inputs/issues/519.json`, body line21.
**Recorded:** 2026-10-08T08:50:18.296171+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/519.json purpose/work order; docs/qa-logs/2026-10-08-preupgrade-alignment/freeze.json

**Refutation attempted:** Personal state manifest/values are explicitly private and outside#507; unknown residue preservation is prescribed, not treated as an already executed action.

**Notes:** Pre-existing owner-specific deployment work remains open.

### AC-519-02: A synthetic rehearsal proves the pre-upgrade order, automatic-consumer isolation, no unintended transfer/migration reactivation, interruption/failure behavior, rollback and unchanged save payload hashes. Commands and terminal receipts identify what was actually exercised.

**Source:** #519; `inputs/issues/519.json`, body line22.
**Recorded:** 2026-10-08T08:50:18.296196+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** docs/qa-logs/2026-10-08-preupgrade-alignment/{old-helper-proof.py,qualification.json}; inputs/issues/519.json source-derived preparation

**Refutation attempted:** 13 finite old-helper controls exercise real historical scripts and prove a held transfer lease does not stop join/follow pointer changes; keep guard does. They do not execute full transaction, service quiescence, interruption/rollback or exact private plan.

**Notes:** Correctly unresolved criterion, not newly discovered implementation defect.

**Gaps:** Full synthetic pre-upgrade sequence still required before owner-device alignment; no product compatibility branch implied.

### AC-519-03: Named authorized device actions complete before the next update transfer/reboot. Exact readback proves aligned selected roots and intended auto-sync state, obsolete records handled as planned, no unintended writer active and preserved payload/recovery hashes. No claim of completion rests on intent alone.

**Source:** #519; `inputs/issues/519.json`, body line23.
**Recorded:** 2026-10-08T08:50:18.296221+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/519.json unchecked criterion and action boundary; inputs/milestone7.json

**Refutation attempted:** No current authorization for named device writes/upgrade and no sealed completed action receipt in scope. Audit performs none and retains hard gate before next owner update/reboot.

**Notes:** Future private operational gate, not a public release-runtime bug.

### AC-519-04: A sealed private acceptance receipt and redacted tracker/handoff status block upgrade until completion and invalidate on relevant state drift. Subsequent upgrade and first deliberate sync retain separate action authority and post-upgrade readback.

**Source:** #519; `inputs/issues/519.json`, body line24.
**Recorded:** 2026-10-08T08:50:18.296245+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** inputs/issues/519.json purpose/work order5; inputs/milestone7.json; canonical checkpoint at frozenac64

**Refutation attempted:** Tracker/checkpoint correctly prohibit this owner's next upgrade without acceptance and fresh drift check, while permitting host/commonVM/audit work. No private completed acceptance receipt claimed or inspected.

**Notes:** Open pre-existing operational requirement remains distinct from#508 firmware qualification.

**Gaps:** Actual sealed private acceptance and bound deployment readback still owed before owner upgrade.

## UI corrections source observation — 2026-10-08T08:50:57.089556+00:00

Directly read exact#512/#513/#514 commit diffs: scan lock outcome alone gets check-specific language while ordinary sync remains unchanged; three emitted reasons gain localization; short save instruction heading moves all category meaning to wrapped prose; content path title loses only redundant folder word; empty restore explicitly says selected folder and points all category types to check guidance. Current183unit cases/4752assertions pass, six syntax units/catalog/vocabulary/menu checks pass. Retained evidence index carries99 entries across source revisions, so affected/reused/rejected identities must remain differentiated.

### AC-512-01: Exact source trace and actual failing French frames retain the observed behavior: check-busy mislabeled as sync, plus actual changed-config/create rendering; do not infer raw-English display solely from table omission.

**Source:** #512; `inputs/issues/512.json`, body line15.
**Recorded:** 2026-10-08T08:51:23.420139+00:00
**Verdict:** PASS ✓

**Evidence:** ES1d5397 diff; V/ui/supplemental/frames/walk-fr640-unfixed-scan-busy-02-scan-busy-untranslated.png; fault-settings-changed03-settings-changed-fixed.png; walk-fr640-create-settings-failure-01-create-settings-failure.png

**Refutation attempted:** Direct original frame shows a scan mislabeled synchronization, not raw-English fallback. Direct changed-config/create-failure frames show actual rendered French messages on their real routed outcome surfaces. Source-table omission alone was not evidence.

**Notes:** V denotes docs/qa-logs/2026-10-07-cloud-validator.

### AC-512-02: All three reasons use the established localized reason table and complete French catalog; Scan+75 describes another check while ordinary sync75 behavior is preserved; focused catalog/unit checks cite exact committed source and result.

**Source:** #512; `inputs/issues/512.json`, body line16.
**Recorded:** 2026-10-08T08:51:23.420260+00:00
**Verdict:** PASS ✓

**Evidence:** ES4e410:CloudText.cpp:407–437; GuiCloudTransfer.cpp:458; checks/es-controls01/{unit-run,syntax,catalog}.log

**Refutation attempted:** Fresh183cases/4752assertions include scan-vs-sync lock wording and three protocol reasons. lockHeldOutcome branches only Scan; other sync75 wording preserved. Final French catalog compiles and six actual target-flag syntax checks return0.

**Notes:** Exact ES source hashes bound before/after current checks.

### AC-512-03: Actual affected French failure frames pass review with source/binary/locale/panel hashes in the #510 evidence index; canonical flow rows link them. Existing unaffected evidence keeps explicit provenance.

**Source:** #512; `inputs/issues/512.json`, body line17.
**Recorded:** 2026-10-08T08:51:23.420302+00:00
**Verdict:** PASS ✓

**Evidence:** V/ui/evidence-index.json; supplemental/frames/walk-fr640-fixed-scan-busy-fit-01-scan-busy-fixed-fit.png and named changed-config/create-failure frames; docs/pixelelated/cloud-folder-flow-review.md CF12/13; checks/cloud-packet-readback.json

**Refutation attempted:** Direct reviewed frames fit640 width and name check/settings/create accurately. Index preserves original source/binary/catalog/panel and rejected frame; unchanged later inputs do not relabel earlier diagnostic frames as newly captured.

**Notes:** No assembled-image assertion.

### AC-512-04: The final qualified ES source is included in #508 integration/pin tracking; close only with that commit/evidence readback.

**Source:** #512; `inputs/issues/512.json`, body line18.
**Recorded:** 2026-10-08T08:51:23.420333+00:00
**Verdict:** PASS ✓

**Evidence:** inputs/issues/508.json; S2/integration/prepared-product-inputs.json; checks/cloud-packet-readback.json; git ancestry1d5397→4e410

**Refutation attempted:** Final4e410 contains correction, distribution pin equals4e410 and exact26path manifest matches integrated source. Parent firmware/adoption scope remains open.

**Notes:** Tracked source resolution distinct from parent firmware qualification.

### AC-513-01: Rejected original frames and exact tested identities remain in the #510 packet.

**Source:** #513; `inputs/issues/513.json`, body line19.
**Recorded:** 2026-10-08T08:52:00.644823+00:00
**Verdict:** PASS ✓

**Evidence:** V/ui/supplemental/frames/walk-fr640-help-paths-{01-saves-instructions,03-content-path-editor}.png; V/ui/evidence-index.json; checks/cloud-packet-readback.json

**Refutation attempted:** Direct original save-help frame visibly truncates screenshot category; retained original editor source/frame indexed separately from corrected source. Packet hashes intact.

**Notes:** Rejected originals preserved, not overwritten.

### AC-513-02: English/French source and catalog checks pass on the committed correction, with no loss of category meaning or folder-selection behavior.

**Source:** #513; `inputs/issues/513.json`, body line20.
**Recorded:** 2026-10-08T08:52:00.644988+00:00
**Verdict:** PASS ✓

**Evidence:** ES6b473c26 diff GuiMenu.cpp; ES4e410 French catalog; checks/es-controls01/{syntax,catalog,vocabulary,unit-run}.log

**Refutation attempted:** Only heading/title/prose strings change: complete game save/state/capture categories move to wrapped body; editor removes redundant folder word. Folder command/callback behavior unchanged. Exact current syntax/catalog/unit checks0.

**Notes:** No silent category narrowing.

### AC-513-03: Actual corrected small-panel frames show both full category scope and readable editor title without ellipsis; affected large-panel coverage or explicit unchanged-input justification is indexed.

**Source:** #513; `inputs/issues/513.json`, body line21.
**Recorded:** 2026-10-08T08:52:00.645030+00:00
**Verdict:** PASS ✓

**Evidence:** V/ui/supplemental/frames/walk-fr640-fit-final-{02-saves-help-fixed,03-content-title-fixed}.png; walk-fr1280-fit-proof02-{01-saves-help-fixed,02-content-title-fixed}.png; evidence-index.json

**Refutation attempted:** Direct640 help/title and1280 title review shows complete category scope and no ellipsis. Source identities distinguish6b473 corrected fit from later unchanged4e410copy elsewhere.

**Notes:** Panel and locale evidence explicitly indexed.

### AC-513-04: Canonical flow/reference and exact-source screenshot index are updated together before completion/pin promotion, under D-WORKFLOW-156.

**Source:** #513; `inputs/issues/513.json`, body line22.
**Recorded:** 2026-10-08T08:52:00.645062+00:00
**Verdict:** PASS ✓

**Evidence:** docs/pixelelated/cloud-folder-flow-review.md CF04/CF05; docs/es-menu-map.md visual evidence; V/ui/evidence-index.json; checks/es-controls01/menu-map.log

**Refutation attempted:** Canonical affected flow rows link exact-source changed and retained original proof before integration; map check finds0missing among53screens. Map lint alone is corroboration; actual corrected frames were viewed.

**Notes:** No new screen/component introduced.

### AC-513-05: Qualified final source is included in #508 integration tracking; existing unaffected #512 diagnostic proof keeps precise provenance.

**Source:** #513; `inputs/issues/513.json`, body line23.
**Recorded:** 2026-10-08T08:52:00.645104+00:00
**Verdict:** PASS ✓

**Evidence:** S2/integration/prepared-product-inputs.json; inputs/issues/508.json; V/ui/evidence-index.json; checks/cloud-packet-readback.json

**Refutation attempted:** 4e410includes6b473; exact pin/integratedpath bytes verified. Older#512diagnostic frames retain original1d5397/6b473 identities and unchanged-input explanation.

**Notes:** Firmware inclusion remains parent gate.

## Empty-selected-folder direct visual review — 2026-10-08T08:52:18.964295+00:00

Viewed rejected original French1280 account-wide assertion and corrected English/French640 plus French1280 frames. Current text explicitly scopes selected folder, fits entirely, and directs category-specific location guidance rather than telling BIOS/media to use ROMs indiscriminately. Final source changes only this sentence/catalog; selected-root backend behavior unchanged. Read exact raw preservation receipt next.

### AC-514-01: The empty restore headline explicitly scopes its finding to the selected cloud folder, in English and French; it does not claim an account-wide search or absence.

**Source:** #514; `inputs/issues/514.json`, body line15.
**Recorded:** 2026-10-08T08:52:58.417860+00:00
**Verdict:** PASS ✓

**Evidence:** ES4e410 GuiMenu.cpp:4478; French catalog; V/ui/supplemental/frames/walk-{fr640-empty514-final,en640-empty-help514}-01-selected-folder-empty-fixed.png

**Refutation attempted:** Direct EN/FR640 and French1280 frames clearly name selected folder, unlike retained rejected account-wide original. No selected-root behavior change hidden in copy-only diff.

**Notes:** No account-wide absence claim.

### AC-514-02: Adjacent setup guidance is accurate for the categories that reach this branch, including BIOS/game-content boundaries; it does not direct unrelated file types into the wrong folder or silently change selection.

**Source:** #514; `inputs/issues/514.json`, body line16.
**Recorded:** 2026-10-08T08:52:58.417971+00:00
**Verdict:** PASS ✓

**Evidence:** ES4e410 GuiMenu.cpp:4478–4482,cloudFolderInstructions; V/ui/evidence-index.json CF04/14; docs/pixelelated/cloud-folder-flow-review.md

**Refutation attempted:** New generic guidance points to expected locations for chosen category; BIOS keeps required subfolders and media keeps system folder. It no longer directs every category to ROMs; no pointer callback changed.

**Notes:** Current syntax/unit/catalog checks pass.

### AC-514-03: Source/catalog checks and actual corrected frame review pass with exact committed source identity. The empty-selected/populated-unselected fixture retains all original file hashes and independent pointers.

**Source:** #514; `inputs/issues/514.json`, body line17.
**Recorded:** 2026-10-08T08:52:58.418028+00:00
**Verdict:** PASS ✓

**Evidence:** checks/es-controls01; V/ui/supplemental/receipts/ui04-empty-{before,after-fr640,after-fr1280}.txt; final-source-receipt.json; checks/cloud-packet-readback.json

**Refutation attempted:** Exact final4e410source tests pass; raw before/after include independent selected roots and populated unselected OtherLibrary witness, with preserved original hashes. Actual reviewed corrected frames come from exact source overlay, not candidate16 firmware.

**Notes:** Existing larger-panel EN proof is indexed with precise source.

### AC-514-04: CF14 canonical flow and screenshot index link the corrected evidence and preserve the rejected original before completion/pin promotion.

**Source:** #514; `inputs/issues/514.json`, body line18.
**Recorded:** 2026-10-08T08:52:58.418060+00:00
**Verdict:** PASS ✓

**Evidence:** docs/pixelelated/cloud-folder-flow-review.md CF14; V/ui/evidence-index.json and supplemental/frames/walk-fr1280-scan-retry-options-03-selected-empty-systems.png

**Refutation attempted:** Rejected original remains indexed alongside corrected4e410 variants. Canonical flow records selected-root scope, no transfer and unchanged pointers; source/reference/evidence precede integration.

**Notes:** No dead QR link introduced.

## Current installation and retirement observation — 2026-10-08T08:54:59.616918+00:00

Fresh isolated actual rclone install hook copies23 current files at expected modes/bytes and no migration engine. Exact runtime distro and ES symbol sweeps find no old migrate/repair/tidy path; public predecessor config/filter bytes directly read. Note for Phase3 refutation: create UI checks context before consent and again on confirmation, but backend seed API takes categories alone; inspect whether a settings change between UI check and child startup can redirect creation despite path-consent comment. This is an unconfirmed interaction lead, not a runtime finding.

### AC-508-01: Final source/install/ES call-site sweep proves there is no installed automatic migration engine, legacy autojoin/follow, startup migration prompt or TIDY move action; syntax/package/catalog checks pass. Local draft evidence exists; integrated source/install inclusion is still required.

**Source:** #508; `inputs/issues/508.json`, body line34.
**Recorded:** 2026-10-08T08:56:47.177425+00:00
**Verdict:** PASS ✓

**Evidence:** checks/retirement-source-sweep.json; checks/rclone-install01/result.json; checks/es-controls01; checks/host-controls01/pkgcheck-{rclone,emulationstation}.log; S2/integration/prepared-product-inputs.json

**Refutation attempted:** Exact current distro/ES runtime sweep has zero migration/repair/tidy symbols, and actual package hook installs23 current files with no old engine. Fresh syntax/catalog/package checks0. Manifest matches integrated26paths/modes and4e410pin; current assembled image is not inferred.

**Notes:** Source/install integration complete; final firmware remains separate.

### AC-508-02: Synthetic clean linking creates nothing; separately confirmed selected-category CREATE FOLDERS creates only the chosen folders/notes and preserves other trees. Source-overlay before/after hashes/pointer receipts pass; assembled-image CF10 proves the final firmware.

**Source:** #508; `inputs/issues/508.json`, body line35.
**Recorded:** 2026-10-08T08:56:47.177551+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** checks/cloud-controls01/validator.log; V/validator/runs/final04.json; V/ui/evidence-index.json CF01/03; checks/rclone-install01/result.json

**Refutation attempted:** Fresh30validator controls include implicit-seeding refusal, selected creation, unchanged pointers/other bytes and preserved notes; source/UI call only category-scoped explicit creation after consent. Source-overlay receipts support behavior, but no final assembled CF10 exists.

**Notes:** Pre-existing firmware gate, not audit-discovered bug.

**Gaps:** Assembled-image CF10 clean-link/selected-create proof still required.

### AC-508-03: Public ROCKNIX configurations retain credentials, independent pointers and cloud bytes through adoption/scans/setup unless explicit selection changes a pointer. Clean installs are proved separately. Unpublished experimental states do not add compatibility requirements.

**Source:** #508; `inputs/issues/508.json`, body line36.
**Recorded:** 2026-10-08T08:56:47.177600+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** checks/retirement-source-sweep.json public_predecessor; rclone/sources/cloud_sync_helper:460; checks/cloud-controls01/validator.log public config cases; docs/pixelelated/cloud-folder-flow-review.md Who is upgrading

**Refutation attempted:** Publicc445081a config is /GAMES and/GAMES/backup, without fork content key; current conversion preserves existing keys and assigns only missing content default. Synthetic controls distinguish clean/public/custom roots and unchanged credentials/provider bytes. No final firmware public adoption receipt yet.

**Notes:** Unpublished owner layouts are not new product compatibility obligations.

**Gaps:** Current assembled firmware public predecessor adoption and separate clean-install proof pending#508 CF10.

### AC-508-04: Final firmware's validation and restore discovery stay within selected roots; ordinary save/settings/content, partial-library restore and missing/unreadable/supported-format handling retain their applicable controls. Unchanged tests keep their exact input identity; changed inputs receive affected proof.

**Source:** #508; `inputs/issues/508.json`, body line37.
**Recorded:** 2026-10-08T08:56:47.177636+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** cloud_folder_validate; cloud_scan; cloud_content_restore; checks/cloud-controls01; S2/ui/receipts/content02; V/ui/receipts and source-bound ordinary WebDAV/SFTP packets

**Refutation attempted:** Current30validator/39save-layout/21content-scope controls plus target overlay readbacks establish selected-root preservation and bounded errors. Exact-source changes have affected proof; historical broader results retain original identities. Current final firmware is not assembled.

**Notes:** Existing source-overlay assurance cannot close literal final-firmware criterion.

**Gaps:** Affected installed-image inclusion/adoption/ordinary transfer proof remains planned; preserve accepted candidate16 baseline.

### AC-508-05: #515's supported case/action or evidence-backed instructions-only disposition is explicitly mapped to the integrated source and #507 scope. Each implemented repair has consent, bounded transport, collision/stale/interruption/refusal proof and leaves ROMs/BIOS/unknown files untouched.

**Source:** #508; `inputs/issues/508.json`, body line38.
**Recorded:** 2026-10-08T08:56:47.177667+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md C1–C10 and final disposition; docs/pixelelated/cloud-folder-flow-review.md:350–406; S2/integration/prepared-product-inputs.json; inputs/issues/507.json

**Refutation attempted:** Finite supported writer layouts are preserved and omissions fixed; ambiguous flat/wrapped save identity cannot establish a unique relocation. No repair API/action exists or is counted as completed. Source-bound39+31controls and current manifest cover delivered behavior.

**Notes:** No implemented relocation means no fabricated repair consent/screenshot proof.

### AC-508-06: Canonical menu/IA/flow and reviewed EN/FR640×480/1280×800 affected frames match final source; current source-overlay proof is complete above. Any added repair screen requires its own frames. No dead QR destination ships.

**Source:** #508; `inputs/issues/508.json`, body line39.
**Recorded:** 2026-10-08T08:56:47.177694+00:00
**Verdict:** PASS ✓

**Evidence:** docs/es-menu-map.md; docs/conflict-wizard-ia.md; docs/pixelelated/cloud-folder-flow-review.md; V/ui/evidence-index.json; S2/ui/evidence-index.json; native capture index; checks/es-controls01/menu-map.log; checks/cloud-packet-readback.json

**Refutation attempted:** Reviewed affected final script/translation/fit/selected-root frames and exact source/binary/catalog identities. Reused older frames keep source and unchanged-input explanation; rejected originals and pendingCF10 stay explicit. Actual runtime source has local instructions and no new QR destination.

**Notes:** No repair screens because none implemented. Separate website task does not block local guidance.

### AC-508-07: New full pins/package installation and final artifact inclusion are mapped; source-overlay results are never called installed release firmware. CF10 and final inclusion remain open until an engineering image supplies proof.

**Source:** #508; `inputs/issues/508.json`, body line40.
**Recorded:** 2026-10-08T08:56:47.177719+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** S2/integration/prepared-product-inputs.json; checks/cloud-packet-readback.json; checks/rclone-install01/result.json; inputs/issues/508.json

**Refutation attempted:** Full4e410pin,26product paths/modes and package installation match frozen integration; scope says source overlay, not installed release. Exact dependency library/launcher identity mapped. Final engineering image/inclusion is absent and not claimed.

**Notes:** Correctly open pre-existing release work.

**Gaps:** Final assembled input/inclusion manifest and CF10 must come from engineering image.

### AC-510-01: The canonical review records the public release/tag and actual config/filter/package references, separated from unpublished experiments; see Who is upgrading in the linked flow review.

**Source:** #510; `inputs/issues/510.json`, body line33.
**Recorded:** 2026-10-08T08:56:47.177743+00:00
**Verdict:** PASS ✓

**Evidence:** docs/pixelelated/cloud-folder-flow-review.md:17–40; checks/retirement-source-sweep.json public_predecessor

**Refutation attempted:** Directly read publicc445081a config/filter source; /GAMES origins and absence of fork setup/migration separate from unpublished experiments. No generic Rasteratops adoption gate substituted.

**Notes:** Historical official release identity, not a claim to currently latest remote release.

### AC-510-02: D-CLOUD-178/179 and the implemented diagram define selected-category checks/creation, independent paths and manual content guidance; prospective repairs are separately identified with #515 ownership.

**Source:** #510; `inputs/issues/510.json`, body line34.
**Recorded:** 2026-10-08T08:56:47.177770+00:00
**Verdict:** PASS ✓

**Evidence:** docs/decision-register.md D-CLOUD-178/179; docs/pixelelated/cloud-folder-flow-review.md implemented/future diagrams; ES4e410GuiMenu category handler

**Refutation attempted:** Current action source matches explicit selected-category check/create and independent paths; manual ROM/BIOS guidance present. Future repair contract remains labeled prospective and not invoked by current source.

**Notes:** Settled design preserved without asking owner again.

### AC-510-03: Required flow/screenshot maintenance is published in both agent entrypoints, the canonical UI rule and evidence-index schema (D-WORKFLOW-155/156; f6037a9133). The final source-overlay CF01–CF15 table links reviewed happy/branch frames and explicitly pending CF10.

**Source:** #510; `inputs/issues/510.json`, body line35.
**Recorded:** 2026-10-08T08:56:47.177796+00:00
**Verdict:** PASS ✓

**Evidence:** AGENTS.md; CLAUDE.md; .claude/rules/es-ui-style-guide.md; docs/es-menu-map.md evidence schema; V/ui/evidence-index.json; checks/host-controls01/rules.log

**Refutation attempted:** Both agent entrypoints carry source/reference/frame requirement and rules-check0. Index links happy/error/stale/cancel branches, preserves rejected frames and explicitly marks CF10pending rather than treating a directory of screenshots as coverage.

**Notes:** Current source-bound affected supplement extends earlier evidence without rewriting identities.

### AC-510-04: #515 records source-proven repair cases, exact preview/consent/count/bytes/collision/source-retention/stale-plan/interruption/verification contracts and qualified supported actions, or an evidence-backed unsupported disposition. No unsupported repair is counted as delivered.

**Source:** #510; `inputs/issues/510.json`, body line36.
**Recorded:** 2026-10-08T08:56:47.177822+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md; docs/pixelelated/cloud-folder-flow-review.md:350–406; inputs/issues/515.json; checks/cloud-controls01/save-layout.log

**Refutation attempted:** Ten-case source evidence distinguishes valid layouts, coverage omissions and ambiguous relocation. Final finite instructions-only disposition states no supported generic repair, with future contract retained. No nonexistent implementation counted as delivered.

**Notes:** Separate stale#510 current-state wording is evaluated below.

### AC-510-05: #508 final integration/adoption criteria are met on coordinated source and then actual assembled firmware; missing/unreadable and unrelated-file preservation remain proved. Foundation proof is complete above, final pin/image proof is not.

**Source:** #510; `inputs/issues/510.json`, body line37.
**Recorded:** 2026-10-08T08:56:47.177846+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** S2/integration/prepared-product-inputs.json; checks/rclone-install01/result.json; checks/cloud-controls01; inputs/issues/508.json

**Refutation attempted:** Source/pin/install inclusion now coordinated and exact bytes verified, exceeding old local-only snapshot. Actual final assembled firmware/public adoption still missing; foundation or candidate16 history cannot substitute.

**Notes:** Expected in-flight parent gate, not newPL.

**Gaps:** Final engineering image andCF10 acceptance remain open.

### AC-510-06: Live M7, #508/#507/#515 and the canonical checkpoint agree on this implementation order and remaining gates; published in next `b115af8d4cebbb8845edf32f519b3d00580c9ff1` with exact GitHub/readback receipts under docs/qa-logs/2026-10-08-cloud-plan. Personal review remains separate #516.

**Source:** #510; `inputs/issues/510.json`, body line38.
**Recorded:** 2026-10-08T08:56:47.177873+00:00
**Verdict:** FAIL ✗

**Evidence:** inputs/issues/510.json Ordered implementation and Current qualification; inputs/issues/{508,507,515}.json; inputs/milestone7.json; frozen canonical checkpoint; S2/integration/prepared-product-inputs.json

**Refutation attempted:** Read whole body: it still labels#515/#520/#521active, both source branches local/unintegrated and product pin unchanged, plus owned guest active. Other frozen records/source show052771 integratede6645,4e410pin, closures and runtime retirement. These are current assertions, not labeled historical sections.

**Notes:** Tracker-only contradiction, primary code/evidence unaffected. Keep as lead for serial punch-list disposition; root does not alter frozen source.

**Gaps:** Reconcile complete#510current body to exact integrated inputs, finite no-action disposition, closed source work and remainingCF10/firmware gates; exact readback required.

### AC-515-01: A source-cited case table separates supported repairs, valid layouts and unsupported/ambiguous findings; synthetic fixtures reproduce each classification, including legitimate standalone-emulator saves.

**Source:** #515; `inputs/issues/515.json`, body line36.
**Recorded:** 2026-10-08T08:56:47.177901+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md C1–C10; coverage/writer-trace.json; checks/writer-source-readback.json; checks/cloud-controls01/save-layout.log

**Refutation attempted:** Actual pinned writer/mount/launcher chain distinguishes valid standalone paths from unknown wrappers/flat media; fresh39controls reproduce supported classifications. Names/extensions alone do not establish intended core/system destination.

**Notes:** Finite case set explicitly bounded, no exhaustive emulator promise.

### AC-515-02: Every supported repair has an exact plan/consent/size/transport/source-retention/collision contract and fixture; if none is supportable, the evidence-backed disposition is explicit in #510, the flow reference and M7, with no claimed repair completion.

**Source:** #515; `inputs/issues/515.json`, body line37.
**Recorded:** 2026-10-08T08:56:47.177927+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** S2/source-cases.md final disposition; docs/pixelelated/cloud-folder-flow-review.md:350–406; inputs/milestone7.json; inputs/issues/510.json

**Refutation attempted:** Source/flow/M7explicitly conclude no safe generic relocation in finite cases and preserve manual instructions; source offers no repair. However literal required#510current-state disposition remains stale active implementation wording despite actual closure.

**Notes:** Same tracker contradiction asAC-510-06, not a second product defect.

**Gaps:** Update#510body to carry evidence-backed no-action outcome explicitly and retain future repair contract as future.

### AC-515-03: For every implemented repair, failing controls prove stale-plan refusal, preservation of conflicting versions/originals, bounded transfer/verification costs, cancellation/retry safety and exclusion of ROMs, BIOS, settings archives, game content and unknown files. Before/after inventories and hashes show unselected files unchanged.

**Source:** #515; `inputs/issues/515.json`, body line38.
**Recorded:** 2026-10-08T08:56:47.177951+00:00
**Verdict:** SKIP ○

**Evidence:** checks/retirement-source-sweep.json; S2/source-cases.md; docs/pixelelated/cloud-folder-flow-review.md final disposition

**Refutation attempted:** No repair implementation exists; conditional criterion therefore has no action to exercise. Existing filter/default capture changes are separately tested under#520/#521 and do not relocate old data.

**Notes:** Do not manufacture repair failure/consent proof or mark itPASS.

### AC-515-04: For every implemented repair, actual VM frames and operation receipts prove separate preview/confirmation, decline/no-op, interruption/failure, retry, result and recheck; canonical IA/diagram/evidence index match the source, with EN/FR and both panel layouts reviewed for affected content. If no repair case is supportable, record the evidence-backed no-action disposition and reuse unchanged instruction-flow proof explicitly; do not require or fabricate repair screens.

**Source:** #515; `inputs/issues/515.json`, body line39.
**Recorded:** 2026-10-08T08:56:47.177977+00:00
**Verdict:** PASS ✓

**Evidence:** S2/source-cases.md; docs/pixelelated/cloud-folder-flow-review.md; V/ui CF04frames/index; S2/ui/evidence-index.json; checks/cloud-packet-readback.json

**Refutation attempted:** Evidence-backed no-action branch is explicit; manual instruction frames retain exact source and unchanged-input justifications, with new supported-save classification supplement. No nonexistent repair screen is claimed.

**Notes:** Affected EN/FR and panel variants retained; default screenshot action has its separate actual writer proof.

### AC-515-05: #508's integration manifest and #507's frozen scope name the final supported implementation or evidence-backed instructions-only disposition; no new build or release claim relies on an unproved repair.

**Source:** #515; `inputs/issues/515.json`, body line40.
**Recorded:** 2026-10-08T08:56:47.178005+00:00
**Verdict:** PASS ✓

**Evidence:** inputs/issues/{508,507,515}.json; S2/integration/prepared-product-inputs.json; checks/cloud-packet-readback.json

**Refutation attempted:** Frozen audit source includes qualified coverage/default capture fixes and explicitly finite instructions-only placement disposition. No release/firmware claim relies on an unimplemented repair.

**Notes:** Full firmware adoption remains#508.

### AC-507-01: The dated running log and input manifest bind the exact baseline, changed source, selected issue criteria and terminal build/proof receipts; coverage explicitly separates preserved candidate16 evidence from newly verified delta behavior.

**Source:** #507; `inputs/issues/507.json`, body line20.
**Recorded:** 2026-10-08T08:56:47.178028+00:00
**Verdict:** PASS ✓

**Evidence:** 00-running-log.md; inputs/source-manifest.json; inputs/criteria.json; checks/*/owner-readback.json;01-research-notes.md

**Refutation attempted:** Exact candidate16/current distro/ES identities,130verbatim criteria and30public issue snapshots retained. Source checks/host runs have primary outputs and terminal lifecycle receipts. Historical qualification boundaries remain explicit.

**Notes:** Audit's initial evidence-binding criterion is met at this Phase2checkpoint; completion gates below are not yet due.

### AC-507-02: Primary forward/retrospective findings cite code and executed evidence for the changed behaviors and interactions; every finding has a disposition and unresolved claims are not counted as passes.

**Source:** #507; `inputs/issues/507.json`, body line21.
**Recorded:** 2026-10-08T08:56:47.178050+00:00
**Verdict:** PARTIAL ⚠

**Evidence:** 02-forward-audit.md; inputs/verdicts.jsonl; checks/;00-running-log.md

**Refutation attempted:** Independent forward findings cite primary files and executed controls with required refutations, but Phase3retrospective and final finding dispositions must occur serially after this checkpoint.

**Notes:** Self-referential audit lifecycle work, not audit-discovered product defect.

**Gaps:** Complete remaining gated audit phases and record dispositions; no final audit completion yet.

### AC-507-03: Facilitator receipts verify the required cross-lab reviewer identity and both Milestone passes against the frozen safe payload; the final analysis independently verifies proposed findings.

**Source:** #507; `inputs/issues/507.json`, body line22.
**Recorded:** 2026-10-08T08:56:47.178073+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/source-manifest.json external_dispatch;00-running-log.md; .claude/skills/code-auditor/references/phases.md Phase4.6

**Refutation attempted:** Facilitator Milestone calls must follow independent phases; no early provider call or unrestricted inherited disclosure inferred. Safe payload/authority review remains prescribedPhase4.6.

**Notes:** Deferred self-gate to later serial phase, not exempt from final completion.

### AC-507-04: The punch-list index, audit artifact lint and completed marker agree; fixes have affected installed/source verification and no completion is inferred from reviewer prose alone.

**Source:** #507; `inputs/issues/507.json`, body line23.
**Recorded:** 2026-10-08T08:56:47.178100+00:00
**Verdict:** SKIP ○

**Evidence:** .claude/skills/code-auditor/references/phases.md Phases5–7;00-running-log.md

**Refutation attempted:** Punch-list index/lint/marker are later dependent outputs and do not yet exist. No self-issued completed marker or unverified fix claim.

**Notes:** Must be satisfied before eventual#507completion; not a productPLfor normal phase ordering.

### AC-507-05: M7, affected issue bodies and the canonical checkpoint record the resulting readiness and remaining publication/device gates; a fresh exact-head hosted record check consumes the completed audit honestly.

**Source:** #507; `inputs/issues/507.json`, body line24.
**Recorded:** 2026-10-08T08:56:47.178125+00:00
**Verdict:** SKIP ○

**Evidence:** inputs/issues/507.json;00-running-log.md; parent ownership publication reported separately from frozen source

**Refutation attempted:** Delivery records can say audit active but cannot yet record final readiness. Final tracker/checkpoint/exact-head hosted readback belongs to completion publication after review, with root coordinating to avoid conflicts.

**Notes:** Later audit self-gate remains mandatory; no completion inferred from progress handoff.

## Forward Audit Summary

Completed independently at 2026-10-08T08:57:31.918709+00:00 before prior per-criterion verdicts are opened.

| Verdict | Count | Criteria |
|---|---:|---|
|PASS|99|AC-461-01, AC-461-02, AC-461-03, AC-461-04, AC-489-01, AC-489-02, AC-489-03, AC-490-01, AC-490-02, AC-490-03, AC-491-01, AC-491-02, AC-491-03, AC-492-02, AC-492-03, AC-492-04, AC-494-01, AC-494-02, AC-494-05, AC-495-01, AC-495-02, AC-495-03, AC-496-01, AC-496-02, AC-496-03, AC-497-01, AC-497-02, AC-497-03, AC-498-01, AC-498-02, AC-498-03, AC-498-04, AC-499-01, AC-499-02, AC-499-03, AC-503-01, AC-503-02, AC-503-03, AC-503-04, AC-506-01, AC-506-02, AC-506-03, AC-500-01, AC-500-02, AC-500-03, AC-500-04, AC-501-01, AC-501-02, AC-501-03, AC-502-01, AC-502-02, AC-502-03, AC-502-04, AC-502-05, AC-520-01, AC-520-02, AC-520-03, AC-520-04, AC-520-05, AC-520-06, AC-521-01, AC-521-02, AC-521-03, AC-521-04, AC-521-05, AC-522-01, AC-522-02, AC-522-03, AC-522-04, AC-523-01, AC-523-02, AC-523-03, AC-523-04, AC-517-04, AC-517-07, AC-512-01, AC-512-02, AC-512-03, AC-512-04, AC-513-01, AC-513-02, AC-513-03, AC-513-04, AC-513-05, AC-514-01, AC-514-02, AC-514-03, AC-514-04, AC-508-01, AC-508-05, AC-508-06, AC-510-01, AC-510-02, AC-510-03, AC-510-04, AC-515-01, AC-515-04, AC-515-05, AC-507-01|
|PARTIAL|16|AC-492-01, AC-492-05, AC-497-04, AC-504-03, AC-504-04, AC-517-03, AC-517-06, AC-519-02, AC-519-04, AC-508-02, AC-508-03, AC-508-04, AC-508-07, AC-510-05, AC-515-02, AC-507-02|
|FAIL|1|AC-510-06|
|SKIP|12|AC-504-01, AC-504-02, AC-504-05, AC-517-01, AC-517-02, AC-517-05, AC-519-01, AC-519-03, AC-515-03, AC-507-03, AC-507-04, AC-507-05|
|UNTESTABLE|2|AC-494-03, AC-494-04|

**Overall Assessment:** PASS WITH FINDINGS for qualified source delta; no current firmware/RC or completed audit claim. Tracker contradictions require disposition. Later audit self-gates stay phase-gated.

## Coverage Boundary

**Examined:** exact current/candidate16 distro and ES source/diffs,130criteria/30public issues, historical build/physical receipts, public proof packets and actual frames, fresh15cadence/19retention/8cleanup/42installation/145cloud-integrity controls, current183ESunitcases/4752assertions,6syntaxunits,catalog/vocabulary/menu and11package lints, actual isolated23-file rclone install hook. Levels and precise commands are retained per criterion/check owner.

**Deliberately not examined:** private personal cloud/device inventories, credentials, private alignment manifests; complete candidate16matrix replay; new physical/provider actions; commercial game compatibility; prior per-AC audit verdicts until now. Historical source overlay is distinct from newly assembled firmware.

**Dimensions not exercised:** current full engineering image/CF10clean-public adoption, new physical acceptance, private operational alignment, whole library integrity or emulator playability. External review is laterPhase4.6, not yet performed.

## Prior-verdict cross-check

Opened prior per-AC/punch-list grades only after all130 independent entries, at 2026-10-08T08:59:03.586834+00:00. Prior Milestone scope contains51issue IDs; none directly overlap this post-candidate16issue set. The261criterion baseline is preserved, not replayed. Each new criterion has no prior independent same-AC verdict:

| Current criterion | Prior same-AC verdict | Comparison |
|---|---|---|
|AC-461-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-461-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-461-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-461-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-489-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-489-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-489-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-490-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-490-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-490-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-491-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-491-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-491-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-492-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-492-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-492-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-492-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-492-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-494-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-494-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-494-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-494-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-494-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-495-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-495-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-495-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-496-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-496-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-496-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-497-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-497-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-497-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-497-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-498-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-498-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-498-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-498-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-499-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-499-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-499-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-500-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-500-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-500-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-500-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-501-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-501-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-501-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-502-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-502-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-502-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-502-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-502-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-503-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-503-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-503-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-503-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-504-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-504-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-504-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-504-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-504-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-506-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-506-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-506-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-507-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-507-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-507-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-507-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-507-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-06|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-508-07|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-510-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-510-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-510-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-510-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-510-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-510-06|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-512-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-512-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-512-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-512-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-513-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-513-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-513-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-513-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-513-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-514-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-514-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-514-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-514-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-515-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-515-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-515-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-515-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-515-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-06|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-517-07|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-519-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-519-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-519-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-519-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-520-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-520-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-520-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-520-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-520-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-520-06|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-521-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-521-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-521-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-521-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-521-05|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-522-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-522-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-522-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-522-04|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-523-01|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-523-02|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-523-03|None; new post-baseline issue|No direct agreement/disagreement available|
|AC-523-04|None; new post-baseline issue|No direct agreement/disagreement available|

### Prior punch continuity and affected interactions

Read prior05-punch-list, resolution headings/terminal reconciliation and completion receipt. All eight are resolved on accepted candidate16; all five completion-bound artifact digests independently match checks/prior-completion-readback.json.

| Prior item | Current independently verified disposition |
|---|---|
|PL001 content discovery|Former automatic discovery contract intentionally retired byD-CLOUD-175/178/179. Explicit selected-root code/current21controls/targetframes replace it; no regression against obsolete contract.|
|PL002 pointer transitions|Join/follow/settle removed; current explicit independent selection preserved. Existing stored owner state is separately#519, not an invented public compatibility path.|
|PL003 sibling shelf|Automatic migration engine removed; no current scan/apply shelf operation. Historical accepted resolution preserved.|
|PL004 migration fingerprint|Pending migration consumer removed; no current auto-rebind. Private legacy residue remains#519.|
|PL005 truthful reasons|Current scan/category failure translations reviewed and freshES183cases pass; missing/unreadable/timeout differentiation retained.|
|PL006 folder names|Independent path editor remains; source grammar and current synthetic namespace/path controls preserve representable names. Automatic account-root chooser deliberately removed.|
|PL007 French sign-in|No current delta to OAuth/window producer bytes; prior acceptedEN/FRbaseline preserved with current post-link category-flow proof distinct.|
|PL008 reader grammar|Nonexecuting first-assignment readers retained; fresh validator/content/config controls cover changed interactions. No claim to replay prior full matrix.|

No direct same-criterion disagreement exists. Intentional retirement of earlier automatic-migration/discovery contracts is recorded as changed design, not silent loss or reopened historical bug. No unresolved prior punch item requires carryover.

## Post-forward correction at Phase4.5 — 2026-10-08T09:21:24.754830+00:00

AC-504-04: original independent PARTIAL is superseded by UNTESTABLE within this audit boundary. Full #504 body explicitly identifies retained local evidence, not an already-published commit. The criterion says retained under a path, not publicly committed. A public publication requirement was inferred incorrectly. Private source-reading commands/outputs remain unopened, so the criterion is UNTESTABLE within this audit boundary, not a documentation defect. Original130entry ledger is retained unchanged for independence/order; effective scorecard99PASS/15PARTIAL/1FAIL/12SKIP/3UNTESTABLE is derived with inputs/post-forward-regrades.json. F-02 withdrawn.
