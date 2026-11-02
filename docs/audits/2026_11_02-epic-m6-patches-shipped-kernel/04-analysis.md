# Audit Analysis — M6 T41 shipped kernel patches and configuration

**Date:** 2026-11-02 17:42:20 UTC. **Spec:** `docs/reviews/briefs/patches-shipped-kernel.md` v2 plus the complete Stage-B method erratum at coordinator `4c8a118cfb4efa8d13c1b41b72ef7a205da5f766`. **Issue:** #688. **Source commit:** `02aab33bd9842610b0d466c9c186454dc14373ee`; Stage-A artifact `cffe3f869c`, original method blocker `3cd9ca140a`.

## Executive Summary

All **120 complete patch applications over 106 patch paths succeeded** against the same cached pins: 43 applies, 48 applies with offset and 29 fuzz. Zero production candidates failed and zero successors were blocked. The deliberately failing fixture verifies that a partial candidate cannot advance the sequence. H700 011 remains the sole diagnostic disagreement: dry-run rc=1 but complete apply rc=0; the coordinator's D-WORKFLOW-222 resolves that method error without changing product source or discarding old receipts.

The 107-row provenance/coverage table is complete, including the SM8550 configuration and five non-kernel rows. Currency dispositions are **101 keep, 4 upstream-changed, 1 upstream-moved, 1 #585**. The known High source defect in both `0010-msm-resource-cleanup.patch` copies survives refutation: final patched SM8550 code writes through `cstate` before assignment. Upstream `9416eec2c2` supplies the fix; Stage D filed bug #1408 and audit #1409 PL-001; the integration owns landing it. Application success does not certify compilation, boot, runtime behavior or the rest of the 40,474 lines.

This is the Stage-D filing analysis, not final acceptance of #688. C formal tool/reader-plan/pre-issue lint is complete. D files audit #1409 and bug #1408 and posts both questions; PL-001 remains open for coordinator stream disposition. Local depth used one actual Codex reader and no reviewer or provider call.

## Acceptance-criteria scorecard

The exact current 28 criteria are retained in `stage-b/corrected/issue-688-body.txt`; 02 supplies criterion-level evidence and refutation. The scorecard includes future stages so no later obligation disappears at this checkpoint.

| ID | Criterion | Verdict | Evidence / remaining stage |
| --- | --- | --- | --- |
| AC-01 | Complete audit-folder contract | PASS | 00–07, formal audit-local tools and sole Local plan are present; all accepted receipt generations retained; no guest-cycle. |
| AC-02 | Artifact lint and Q1–Q7 contract | PARTIAL | C pre-issue lint PASS and D pre-issue validation; resolution lint/outcomes remain F/H. |
| AC-03 | Actual Local reader and review plan | PASS | Actual Codex/OpenAI Local plan, empty reviewers, D-WORKFLOW-184 and observed-footer/historical identity distinction; no external calls. |
| AC-04 | Punch issue outcomes and coordinator closure | PARTIAL | Audit #1409 has one open PL-001 and no closure; stream disposition and Phase-7 outcomes remain owed. |
| AC-05 | Issue commit headers and protected-source/register guards | PARTIAL | Protected-source diff empty; reviewed-at/fixed-at issue fields remain for final hand-back. |
| AC-06 | Exact membership and both line totals | PASS | Accepted 99-line P1/seed receipts retained; rows and source bytes asserted again by table draft. |
| AC-07 | Stage-A Local positive/negative lint | PASS | Original lint-local-pass.out rc=0 and lint-local-fail.out rc=1 retained, not rerun. |
| AC-08 | 107 complete provenance rows and dispositions | PASS | Generated table below; no empty cells; five non-kernel rows identify T27/T11; dispositions total 107. |
| AC-09 | 107 exact coverage paths with escaped-name normalization | PASS | Coverage table generated from retained P1 rows; comparison decodes literal filename escape only. |
| AC-10 | Corrected 120-application packet and failure guard | PASS | 120 actual apply_rc=0, zero blocked; H700 011 dry_rc=1/apply_rc=0; failure fixture refuses promotion. |
| AC-11 | Generator three FAIL-first mutations then asserted tip output | PASS | Formal generator: three negatives rc=1 before five modes rc=0; all outputs byte-equal to accepted B tables; stage-c/validation.json. |
| AC-12 | Ramoops node/config/upstream/pristine context | PASS | 38-line read, six numbered config lines, context at 108 instead of expected near 117, zero pristine ramoops. |
| AC-13 | Two #585 lines, including quoted regex, never sent | PASS | Both draft contributions below; five no-match output lines retained; no #585 write. |
| AC-14 | 0010 currency rows and filed bug | PASS | Both 0010 rows upstream-changed; High bug #1408 has trace, upstream fix, Already written/VM and base-merge criterion; box-check 2 open/0 fail. |
| AC-15 | Four configuration comparisons and method | PASS | 2609 / 3827 / 17 / 7-7 reproduced; helpers and oldconfig were read, not run. |
| AC-16 | 12 additions, move and four upstream changes | PASS | Exact name-status table below; 101 SAME/4 CHANGED/2 ABSENT, integration owns all changes. |
| AC-17 | Command/output/exit/time and hygiene evidence | PASS | AC17 correction 721d6e7049 quotes retained hygiene.out verbatim in 02, including positive controls; no replay. |
| AC-18 | 31 leads and sixteen rulings | PASS | Each appears once in its indexed table below, with evidence and owner. |
| AC-19 | Renovation Q4 counts and Q3 bug numbers | PASS | Q4 counts preserved by value; Q3 names bug #1408; Q5 struck and Q7 inherited; no timing effect. |
| AC-20 | Two maintainer questions posted at Stage D | PASS | Question comments 6585346506 and 6585347732 posted on #688; exact gh API body readbacks retained and 07 quotes them. |
| AC-21 | All inherited leads by owner | PASS | Owner/line matrix below; no lane or integration source modified. |
| AC-22 | Bug/punch ladder and every take-up disposition | PASS | Bug #1408 trace and box-check pass; PL-001 has owner, ladder, Already written and VM; all inherited take-up rows remain in 01/02. Outcome remains open under AC04. |
| AC-23 | Matching classified proof and running-log entries | PASS | Twelve classified proof records below, with twelve corresponding running-log lines. |
| AC-24 | Closing host-ledger no-write evidence | PARTIAL | No host action or write in command census; closing ledger delta check belongs to H, not repeated here. |
| AC-25 | Closing execution census and Stage-H scratch retirement | PARTIAL | Source-only Stage-B census complete; scratch intentionally retained until H. |
| AC-26 | Final retro and its posted timestamp | PARTIAL | 03 is the audit retrospective; final docs/retros artifact and post belong to G. |
| AC-27 | Branch and simulated-merge final checks | PARTIAL | New C/D record checks are retained; final resolution and coordinator simulated-merge checks remain F/H. |
| AC-28 | Single final hand-back and issue box-check | PARTIAL | This is the Stage-D checkpoint, not final hand-back or issue acceptance; final header/closure work remains H. |

**Stage-D record assessment:** 20/28 full-slice criteria covered here (71.4%); 8 PARTIAL, 0 FAIL. These are artifact/evidence verdicts, not coordinator ticks or final slice acceptance. The accepted 14/14 Stage-B scorecard remains unchanged in stage-b/corrected/scorecard.json. The partial rows name stream/outcome and F–H obligations.

## Code Quality Assessment

### Strengths

Exact P1 membership, complete source bytes and current recipe pins agree. Commands retain timestamps, both outputs, return codes and digests; source promotion is explicit. The real negative fixture exercises the same engine as the production sequence. Table assertions reject missing membership, altered reach and stripped headers before table output is trusted.

### Concerns

F-01 (High): the duplicated 0010 series carries an uninitialized-pointer write. F-02 (Low, renovation): three duplicated kernel pairs require coordinated edits across two version directories; no consolidation choice is made here. F-03 (Low, renovation): 19 patches lack From headers, 17 lack Subject too, and several retained subjects describe only the first part of a concatenated series. F-04 (Low, documentation): canonical rules still name a dead generic kernel-patch directory, inherited by the coordinator. F-05 (resolved method finding): dry-run-only advancement cannot model dependent diffs in one patch; D-WORKFLOW-222 and the positive/negative receipts resolve it for this audit.

### Complexity Hotspots

H700's 0002 concatenation contains 31 file sections and 84 hunks; its multiple edits of the same file caused the diagnostic mismatch. SM8550 carries 55 device patches and prefix collisions; ordered dependencies include the Synaptics driver/kconfig pair and haptics driver/follow-ups. Configuration resolution has nine candidates plus build-time rewriting. These are maintenance seams, not evidence that each runtime subsystem was functionally audited.

## Cornerstone Conformance

**Overall: HIGH within source-only scope.** The actual reader, historical identities, immutable source and method refinement are named. Original receipts and all product bytes are preserved. No build, guest, fetch, physical/cloud action, runtime allocation, host-ledger line or historical launch-tree edit occurred. Unknown attribution is retained; a matching line is not silently called an upstream merge. The existing device/rule/integration owners keep their work.

## Spec Fidelity

### Aligned

107 rows, 40,474 split lines / 40,473 newlines, 106 patches / one configuration, reach 103 shipped / four test, nine directory groups and seven reachable-by groups. Pins remain 7.1.2, 7.2, v2026.01 and 20260309. All 31 leads and rulings a–p have recorded dispositions. The five non-kernel rows retain v2's T27/T11 recipe ownership.

### Explicit refinements and deltas

The full coordinator method erratum was read at `4c8a118cfb` and is retained separately; no merge/fetch was required. Actual application is authoritative; dry-run remains diagnostic. The original incomplete runner's absent completion JSON is not invented. Pristine ramoops context is line 108 rather than approximately 117; churn is 61 at this source rather than 64 at the brief's different hash. Firmware extraction of two new files produces no archive-root directory, so the corrected runner explicitly creates the empty root. These are stated with producer receipts, not hidden as expected-output changes.

## Missing Artifacts

Stages C/D artifacts are present: formal generator and reader plan, pre-issue lint, 05, audit #1409, bug #1408, 06/07 and exact question/issue readbacks. Phase-7 disposition/outcomes, final resolution lint, G retro and H hand-back/scratch retirement remain later work. No audit-completion receipt is fabricated.

## Risk Assessment

| Risk | Severity | Impact | Mitigation / owner |
| --- | --- | --- | --- |
| F-01 pre-fix cstate write | High | Undefined behavior on the source path; SM8550 enables the relevant DRM driver | Bug #1408 filed; integration #563/#559 carries 9416eec2c2; no fork patch edit here |
| Successful application mistaken for built/runtime correctness | Medium | False release confidence, especially for device-specific DRM/DT/firmware | Explicit source boundary; compile/guest/device owners retain qualification |
| Duplicate versions diverge | Low | A later fix can update one version only | T11 choice at Stage D; proposed cmp guard or one-file/symlink policy |
| Unknown or squashed provenance | Low | Readers may overstate origin/target version | Unknown cells, adding history and files/hunks metadata preserved |
| Drift at future base merge | Medium | New patches, moved polldev and configuration changes need integration review | Exact pinned delta table and inherited-owner matrix |
| Dry-run failure skips an applicable predecessor | Resolved for this audit | Contaminated successor verdicts | Complete candidate promotion, identical-input positive, failed-candidate fixture |

## Coverage Boundary

**Examined:** source metadata/history for all 107 rows; exact 120 complete applications and diagnostic receipts; one config's resolution and four comparisons; all 38 ramoops lines; targeted final-source refutation of the High finding; all leads/ownership rules. `path-metadata.json`, the commands census and `02` identify what was actually read or run.

**Deliberately not examined:** full functional review of all vendor-carried source lines, external header-linked projects, compiler/build output, fielded images, cloud/user data, physical device state, or other lanes' mutable work. No patch was deleted, renamed, updated or cherry-picked.

**Dimensions not exercised:** compilation/boot/runtime, device memory retention, panel/radio/battery/suspend correctness, clean install/upgrade preservation, security beyond audit-artifact hygiene, or timing measurements. Nothing changed interface-to-first-frame or exit-to-next-first-frame.

## Finding Verification (Phase 4.5)

| Finding | Severity | Survived refutation? | What was checked |
| --- | --- | --- | --- |
| F-01: 0010 cstate write before initialization | High | **yes** | Read the complete final patched `dpu_crtc_assign_resources` function, retained in `0010-final-function.txt`: declaration at 1441, write at 1453, first assignment at 1470. No earlier assignment or guard initializes the local pointer; the global-state error return is not a mitigation for successful calls. Compared both byte-identical carried copies and upstream 9416eec2c2's relocation of assignment before the write, with 28+/22- stat. Rechecked final SM8550 sequence (not only the original patch) and CONFIG_DRM_MSM=y at conf:4461. H700/x86 do not enable that driver; no runtime occurrence is claimed. |

**F-01 trace and already-written state:** the immutable patch set carries the pre-fix bytes; builds using that set consume them, while this audit did not inspect built images. Corrected source application retains the defective statement. Upstream fix `9416eec2c200ad969d9e421e686fc7cbfdaca36a` says the previous version writes through an uninitialized pointer. The patch's reason was resource deallocation on modeset failure; history supports that intent but does not justify using an uninitialized pointer. **Can this be done on the VM?** No guest is needed for this source/history claim; actual runtime effects are outside this slice. **Stage-D acceptance draft:** once the base merge lands, diff of the two carried copies against the then-current upstream base is empty; name the fix and verify both siblings, plus `tools/box-check` for the filed bug. Bug #1408 carries this trace and the base-merge criterion; audit #1409 PL-001 remains open.

The former six-failure H700 claim did **not** survive refutation: all corrected complete applications return 0. It is recorded as a resolved audit-method finding, not retained as six product defects. No Critical finding remains unexamined.

## Renovation face

### Q1 Modernize

No complete patch was proved superseded at the current pin. Eleven dated-import probes include two superficial matches refuted by target context and a deletion-only patch whose old condition still exists. Upstream's polldev move and version-directory symlinks are future integration/T11/T43 work. The ramoops node matches current source and policy; its contribution layer remains a Stage-D decision.

### Q2 Standards

87 From / 89 Subject headers over 106 patches; 17 have neither header and two are stripped exports. Original authorship remains unknown when neither content nor carrying history establishes it. First-target/files/hunks columns expose concatenated series. Prefix collisions are deterministic under C locale; no rename is needed to prove application. GENERIC_X64 config regeneration remains #1084; SM8550's header matches its 7.2 pin.

### Q3 Bugs

F-01 is the confirmed High source defect; Stage D filed the required bug with upstream fix, already-written statement, VM rationale and two-copy acceptance. Its reactive issue is **#1408**, with audit #1409 PL-001; both remain open for coordinator disposition. No true application failure was found; no additional patch-application bug is warranted from the 120 receipts. Upstream's quoted =~ is a never-sent #585 draft, not a new fork defect.

### Q4 Currency

Counts below are generated from actual row/application values, not hand-copied totals. Application counts are **120 plan applications**; upstream/backport/disposition counts are **107 paths**, including the configuration. A header SHA/date is provenance, not a verified release tag. The one `a backport` value is the patch's explicit Upstream-Status claim, not a network-verified merge.

| Currency dimension | Value | Count |
| --- | --- | --- |
| application_status | fuzz | 29 |
| application_status | applies with offset | 48 |
| application_status | applies | 43 |
| upstream_status | carried | 101 |
| upstream_status | fork-written | 1 |
| upstream_status | changed upstream | 4 |
| upstream_status | moved upstream | 1 |
| backport_status | unknown | 106 |
| backport_status | a backport | 1 |
| dispositions | keep | 101 |
| dispositions | #585 | 1 |
| dispositions | upstream-changed | 4 |
| dispositions | upstream-moved | 1 |
| application_status | fails | 0 |
| application_status | open item / blocked | 0 |
| dispositions | superseded at this pin | 0 |
| dispositions | bug | 0 |
| dispositions | open item | 0 |

Disposition sum: **107**. Application sum: **120**. Configuration applicability is a source-resolution `open item`, not a blocked patch application.

| Plan | Current pin / archive SHA256 prefix | Applications |
| --- | --- | --- |
| GENERIC_X64 | 7.1.2 (37198c93727be247) | 8 |
| H700 | 7.2 (f9fef3d14c0df538) | 42 |
| SM8550 | 7.2 (f9fef3d14c0df538) | 65 |
| UBOOT-DDR3 | v2026.01 (03bb43c58d2343ee) | 2 |
| UBOOT-DDR4 | v2026.01 (03bb43c58d2343ee) | 2 |
| FIRMWARE | 20260309 (28fb1b57fa9531ed) | 1 |

Target provenance values by kind (sum 107):

| Kind | Target provenance value | Rows |
| --- | --- | --- |
| patch | eca6838fbfeb815582a6118acefbeb5fbd5bca25 | 1 |
| patch | e455e1333985180431dc6de43d3ab97a2f608edc | 1 |
| patch | c2907f97fc1e40f41093f96e252b826d2e0e702b | 1 |
| patch | Tue, 04 Aug 2026 15:27:23 -0600 | 1 |
| patch | e82b0cfa996e55f6e5f70815ac04cda0b58bf9c4 | 1 |
| patch | 8e7f804d1f1aedf946b229b3f59501ddee840149 | 1 |
| patch | Wed, 26 Feb 2025 20:25:48 +0900 | 1 |
| patch | 2f1e85a50e10b7e0eb200c2c2face6b398cd644d | 1 |
| patch | hand-made | 17 |
| patch | Fri, 18 Oct 2024 11:06:14 -0500 | 1 |
| patch | 72bcec4fc7f6f9da929ac8d0037033e02c409e66 | 1 |
| patch | a0e931952dc69378bb50fcf673ac94c4fb4fc78c | 1 |
| patch | eb89c9384eacd92611c9c839589b721c3ae45a0c | 1 |
| patch | c4d3dd13dcc318924c16bfe561af823bbaa5ff1a | 1 |
| patch | 914fa33237bafdea2281e410b0cd363a3b49e781 | 1 |
| patch | 046e4ac968cfd9daf6c913bd074a24231b2a10d8 | 1 |
| patch | 40f91520dc917c7fca6b13c0caea8c0ea213ba6a | 1 |
| patch | f1f834beae9b9b76e9ef0ccc1c28ed0cc50ed9d9 | 1 |
| patch | unknown | 15 |
| patch | f49b9365ee046df3173ff6a444f8568e1bec0988 | 1 |
| patch | 8bc70e0547259a102dfd335e93d391e8215968ce | 1 |
| patch | 0f776f8abf6a2a2267154388706008b6d61198f1 | 1 |
| patch | 2974d421bb6e5ab6994cd8923180a9c1da7ad035 | 1 |
| patch | 25094d7a39d28c1410d37dbb126bb795cb2f3e41 | 1 |
| patch | d1b22aca1ce00713ff1cd26f47800368d34169e5 | 1 |
| patch | 23b054596a266e21a4fc9915138b49d5cfe9f6a7 | 1 |
| patch | cdcd4a5981e9aca951601d8e254fc0904fc1ae97 | 1 |
| patch | b175ff8ef938557010d163de6c5b264e28810816 | 1 |
| patch | 95440d92bc884d831117f634234d7efe5050c7ab | 1 |
| patch | dc0296918d672985a2bfd24c32d4ebfa52b61dbe | 1 |
| patch | 281e515520b7a95dad1cb9afa0b56485bf5a06ad | 1 |
| patch | 16b15f428ed49d00e334cd80f9654ab21526633a | 1 |
| patch | c1a1f1d0c9d7c23992cf44e74669b5cd9c7d9afd | 1 |
| patch | 1f6b8b9a7112f1c1c50a6e0cc744c92e16da80ea | 1 |
| patch | e154c5ad47302417a1ef134bb9e8ed3155061c70 | 1 |
| patch | 480b00c14cdc3d0a25b1138a2927470fa3df710a | 1 |
| patch | Sun, 15 Jun 2025 00:00:00 +0000 | 1 |
| patch | 36b977cf1f34d9255d88bac5ac63218a1b2f2ba3 | 1 |
| patch | 72a36f7a0239dbc5b52526d11d28da0f37228712 | 1 |
| patch | d8b86c47b60709049b32ef72a96eb21727e1facc | 1 |
| patch | 4c5e76e974db7cca853619ca138eecd8f004622f | 1 |
| patch | d0ff75b09e66023c5f88992706dee4601aa7a437 | 1 |
| patch | 36b23d2e44b4c350adaa34a5bc57967ab1baef41 | 1 |
| patch | 88703f392f3da6256746854f07546f4f83ad92ee | 1 |
| patch | d9d50c0a2ea16ee03a127b08680907b4bf5c6e60 | 1 |
| patch | 9529125aa38fea0d925f439ee28b46242b598a8e | 1 |
| patch | 16568c4bf8f724594b5ae0c7e32f64f095a85d8e | 1 |
| patch | Fri, 15 May 2026 11:16:53 +0000 | 1 |
| patch | 894e7c87039d9eacc00188250aa6454907b91874 | 1 |
| patch | 8ff6265532de3b7a5156df47923df87803934317 | 1 |
| patch | Thu, 10 Sep 2026 22:00:00 +0200 | 1 |
| patch | Thu, 10 Sep 2026 23:00:00 +0200 | 1 |
| patch | Mon, 28 Jul 2025 18:16:22 +0200 | 1 |
| patch | 37189f32371721818b99bba1f42cde9e7eaf2c45 | 1 |
| patch | 7f1ce3a44393fee4288db81a5d0432abe16ca8f5 | 1 |
| patch | ef5a3345d6af58fbfa5d9b1ae2df11d6ac259498 | 1 |
| patch | 835401d628f5e5850900be90a061271fb817a73e | 1 |
| patch | 897560fd00e1add63a9973c31fc437b006855680 | 1 |
| patch | 6f5f1aa6cc762e28c2602fb2d64d87ce89627153 | 1 |
| patch | Fri, 15 Aug 2026 14:30:00 +0800 | 1 |
| patch | Fri, 24 Apr 2026 11:07:55 +0200 | 1 |
| patch | Tue, 10 Feb 2026 11:44:37 +0530 | 1 |
| patch | Tue, 7 Jul 2026 14:00:00 +0200 | 1 |
| patch | 2f02429bcbd2dc0235d9654456db87c6f5e9122a | 2 |
| patch | 0c569e22020f53ddfac0099b0aa193907bfbcd6f | 1 |
| patch | d858770e86e75bf78429b9f5210b7556ef431033 | 1 |
| patch | d03ac59196d7a5f38a03c20b1f8aeba5d5ba14a7 | 1 |
| patch | 742af2c4e58156315dd5347190cabdd40b0d0c18 | 1 |
| patch | a810ab7012cfe8b4703a3eb0b32a2fdd4aaa26d2 | 1 |
| patch | 656d871541b30fff1342f20a9cf61904579b94d2 | 1 |
| conf | Linux/arm64 7.2.0 header | 1 |
| non-kernel | e79ba5f211f9ec8869ed2e506a4b1562437f4d6e | 2 |
| non-kernel | Sun, 21 Sep 2026 19:40:00 +0530 | 2 |
| non-kernel | 1e6e0b28cd5b3e621e012169563d45748734b721 | 1 |

### Q5 Efficiency

~~A provenance table has no Q5; nothing here changes either interface-to-first-frame or exit-to-next-first-frame.~~

### Q6 Dead ends

Applied does not mean built: Qualcomm DRM is enabled only in SM8550 among the three config reads. Empty recipe words/directories, two disabled siblings and excluded configurations are named without expanding membership. All six reach-gap issues remain OPEN; the retained container inventory avoids #1053's host-plan omission, which could otherwise drop the four non-kernel U-Boot rows. No present member is re-tiered or reclassified by this lane.

### Q7 Clarity

The table distinguishes kernel/non-kernel/config, known header claims, exact application indices and the fork-written tier note. `packaging-and-patches.md:91` and `CLAUDE.md:148–149` remain the coordinator's dead-directory erratum. Both line totals identify the one unterminated file. Source filenames and secret scanner remain unchanged; committed H700 0158 path text keeps its literal escape.

## Stage-D questions (posted on #688)

1. **The three 7.0 copies that equal 7.2's: keep two files, or one file and a symlink, as upstream's 7.2.6 does?** A fix to only one copy leaves the other behind; upstream fixed both 0010 copies by hand. T11 owns any recipe-tree change after the base merge; no change here. Evidence: five duplicate checks in `remaining-reads.json`, including the three kernel pairs.
2. **The ramoops patch's contribution layer: ROCKNIX's distribution, or a mainline sun50i-h616.dtsi change?** D-SYS-004 says a distribution reservation is unlikely to belong in the mainline SoC dtsi; #369 is parked. The queue line is drafted either way and **never sent**. The layer decides its intended recipient. Evidence: full 38-line read, six config companions and pristine context.

Posted with exact readbacks: question 1 [6585346506](https://github.com/pixelelated/distribution/issues/688#issuecomment-6585346506); question 2 [6585347732](https://github.com/pixelelated/distribution/issues/688#issuecomment-6585347732). Full posted wording is in 07; question 2 preserves D-SYS-004 as settled and asks confirmation of the contribution-queue target, not an implicit policy reversal. No Stage-A or method approval is re-asked.

## Instruction File Recommendations

Coordinator: correct the generic kernel-patch directory sentence in the two canonical rule locations and keep AGENTS parity. T11: consider an executable duplicate-pair guard if independent copies remain. Coordinator/acceptance tooling: consume corrected apply_rc, explicit blocked rows, normal-output offset/fuzz and actual reader identity. The method lesson already became D-WORKFLOW-222 and the guarded candidate runner; no rule/root-tool edit is performed by T3.

## Tier B visual-QA consolidation

Not applicable: no UI, display content or product behavior changed; no screenshots or guest-cycle evidence were created. The audit does not imply any device display or boot result.

## Second opinion (Phase 4.6)

**Not applicable at Local depth (plan § 6c).** Primary: Codex, `openai/gpt-6-astra`, lab `openai`, xhigh; identity source is the observed live Herdr footer for session `01a19d12-29e3-7fe0-9f41-038dac0a5deb`, not provider-attested identity. The formal `second-opinions/review-plan.json` preserves Opus 5.5 Stage-A execution and Argon Stage-A write-up in identity_source; its primary is the actual OpenAI/Codex reader. Reviewers: zero; provider/Facilitator/council calls: zero. D-WORKFLOW-184 remains the explicit Local exception.

## Quality Self-Check

| Item | Status |
| --- | --- |
| Acceptance scorecard matches 02 and current 28 criteria | Present; current D counts: 20 PASS / 8 PARTIAL; accepted B table retained |
| Three conformance faces / interaction table | Present in 03, summarized here |
| Coverage Boundary in 02 and 04 | Present; no runtime or full-code-review overclaim |
| Every Critical/High refuted | One High, survived; no Critical |
| Second opinion / actual identity | Local exception explicit; formal actual-reader plan completed at C |
| Instruction recommendations | Present with existing owners |
| Visual-QA consolidation | Not applicable, reason stated |
| Defined verdict vocabulary | PASS/PARTIAL/FAIL only in scorecard; source status uses closed application/disposition vocabularies |
| Traceable / evidence-backed / reproducible / actionable / complete for Stage B | Verified against paths, exact receipts, guarded runner and explicit later-stage obligations |

## Stage-C formalization — 2026-11-02T18:35:39.091488+00:00

The accepted Stage-B findings and 120 application receipts are carried forward without replay. `tools/t41-tables.py` is now the audit-local generator, adapted from T40 at `e863379cec`; its current-HEAD reads assert equality to the source used by those receipts. Only its relocation/current-source binding and duplicate assertions changed from the retained draft. Three mutated-input checks and five output modes validate this newly placed program. The Local plan names the actual reader, empty reviewers and D-WORKFLOW-184. `05-punch-list.md` is the open pre-filing draft needed by the pre-issue lint; Stage D supplies its tracker. The scorecard above remains the accepted Stage-B assessment until the dated Stage-D update. No later-stage acceptance is claimed.
