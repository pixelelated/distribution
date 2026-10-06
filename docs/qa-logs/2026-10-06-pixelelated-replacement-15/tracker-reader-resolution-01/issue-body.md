Independent M7 P4 review is complete; Phase7 remediation is being verified on rebuilt candidate15. The immutable candidate is not RC-ready. The primary independently examined261 criteria (204PASS/36PARTIAL/3FAIL/18SKIP), then compared123 prior conclusions. Both explicitly approved Fable5.1/xhigh calls passed identity, effort, digest and actual-process verification. Primary review of every external lead and fourteen installed target experiments retained eight actionable findings:0Critical/1High/6Medium/1Low.

Can this be done on the VM? Yes: every software fix and acceptance below is agent-verifiable on GENERIC_X64 with synthetic local endpoints. Physical/device gates remain later M7.P5 scope. No personal cloud or extra account reset is required for these fixes.

The explicit pre-issue artifact check passes; the default resolution check remains blocked by seven open acceptance outcomes. PL-008 is resolved at `ed5a6a51f5974deec8748fbf0dbd2f4984b690f5`: eight exact-value/archive and malformed-input installed cases, plus an actual old-source failure control, pass in reader-values04. Actual process/guest/backend cleanup and all input seals are verified. See [resolution evidence](https://github.com/pixelelated/distribution/blob/next/docs/audits/2026_10_06-milestone-m7-p4-fixes-383/08-installed-resolution.md). #470 corrects the tooling order without weakening the completion gate. This tracker stays open until all outcomes are verified; no blanket deferrals.

Acceptance criteria / live punch list:
- [ ] PL-001: Recognize usable content and offer the actual legacy root
- [ ] PL-002: Pointer-only transition failure can persist after successful retry
- [ ] PL-003: A current device treats a kept sibling discarded-save shelf as its unfinished move
- [ ] PL-004: A harmless provider-config change strands a pending migration record
- [ ] PL-005: Preserve truthful migration and timeout reasons
- [ ] PL-006: Content chooser offers ordinary folder names that its setter rejects
- [ ] PL-007: Implement the required French phone confirmation and finishing text
- [x] PL-008: Opening scan rejects a valid escaped config value accepted by the shared reader

# Punch List — M7 P4 fixes audit (#383)

**Audit tracker:** [M7.P4 #471](https://github.com/pixelelated/distribution/issues/471) — open; remediation required.

**Generated:** 2026-10-06
**Source audit:** [04-analysis.md](04-analysis.md)
**Total items:**8 (Critical:0, High:1, Medium:6, Low:1)
**State:** Phase7 remediation on rebuilt candidate15. PL-008 is resolved; seven installed acceptance outcomes remain open. No complete-audit or RC claim.

The two Fable calls are verified and their leads have been checked against
primary source and fourteen installed experiments. These eight items are
audit-discovered defects, including #467/#468/#469 filed during the primary
review. They are distinct from pre-existing uncompleted milestone scope.

## Instructions for the executing agent

Work in the order below under the existing remediation authority. Read each
artifact and the canonical rules, implement the bounded change, prove the
negative control and corrected behavior on the installed target, and record
the actual commit/integration and acceptance artifacts. Preserve stored player
state and include an `Already written:` disposition. Do not edit frozen14 or
claim its qualification covers changed product bytes. Rebuild and requalify the
changed candidate before P4 closure; all known bugs must be resolved before RC.

## PL-001: Recognize usable content and offer the actual legacy root

- **Severity:** High
- **Category:** Acceptance Criteria Gap
- **Source Finding:** F-01; B-01/B-02/R-01; I352-L32/L33/L44
- **Owner area:** cloud content discovery and ES chooser
- **What:** Use the supported tiered/legacy membership rules consistently at named folders and the explicit cloud root. Distinguish unrelated folders, absent data and listing refusal. Make an actually discovered legacy root reachable in the scan-first flow. Preserve the approved automatic found-folder behavior and explicit-root/custom-path contracts.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:490; cloud_content_restore:1235; ES es-app/src/guis/GuiMenu.cpp:5228
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** evidence/refutation-03: seven unchanged14 cases, three controls pass/four challenges fail; expected unrelated→empty and explicit valid root→ok, actual ok/empty respectively. reviewer-coverage-01 R01 finds root content but the actual scan reports cloud_bytes0.
- **Acceptance:** A rebuilt candidate passes all seven original controls/challenges plus stranded legacy-root selection/scan, failed-listing refusal and supported-system/empty-local cases; retain cloud hashes/pointers and EN/FR640px chooser/options frames. A deliberately old-source control must reproduce the misses.
- **Existing audit-discovery tracker:** #467 (open).

## PL-002: Pointer-only transition failure can persist after successful retry

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** G-03; B-07
- **Owner area:** cloud layout/configuration and setup
- **What:** Publish intended pointer sets atomically or retain retryable intent; verify failure at each boundary and preserve independent/custom/nonempty tier choices.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:656,878,922,948
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** Refuse the SETTINGS_REMOTE write after SAVES_REMOTE lands. All three transitions exit1; retry returns3 without completing settings/content pointers. Follow/settle scan report current for the mixed defaults. Cloud bytes unchanged. Re-grade Low to Medium because the installed failure survives retry. Artifact: evidence/reviewer-leads-03/artifacts/B07-{join,follow,settle}-observation.json
- **Acceptance:** Installed join/follow/settle with failures at every pointer-publication boundary either retain the entire old selection or recover the complete intended selection on retry; no false current state. Controls preserve custom content/root and nonempty backup tiers. Retain source/installed hashes, pointers and unchanged cloud bytes.

## PL-003: A current device treats a kept sibling discarded-save shelf as its unfinished move

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** G-01; B-05
- **Owner area:** cloud layout/configuration and setup
- **What:** Distinguish an active earlier-layout sibling from this device unfinished migration, while retaining real interrupted-RC2 shelf recovery.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:819,1239
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** With current marker/layout and another guest explicitly keeping ROCKNIX, state reports migration-pending; apply moves and deletes that live sibling shelf. Bytes survive at the new location and live saves/pointers are preserved; no data-loss claim. Artifact: evidence/reviewer-leads-03/artifacts/B05-kept-sibling-observation.json
- **Acceptance:** Two installed guests, one current and one KEEP on an earlier layout, leave the active earlier shelf in place and current state settled. The genuine recorded/inherited RC2 partial-migration recovery still completes all owned tiers without loss. Include unreadable-listing refusal and repeated scans.

## PL-004: A harmless provider-config change strands a pending migration record

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** G-02; B-06
- **Owner area:** cloud layout/configuration and setup
- **What:** Preserve endpoint/root binding and partial data; support harmless rewrites and a truthful, safe recovery route for changed bindings without silently rebinding an old record.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:1015,1056,1185; cloud_setup:744; ES cloud-folder error/recovery flow
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** Adding only a comment after an actual interrupted copy makes state/apply/seed all return5. The token field remains excluded and restoring provider/root config permits verified resume. Intentional binding protects data; unsupported recovery/overbroad binding is the defect, not fail-closed refusal. Artifact: evidence/reviewer-leads-03/artifacts/B06-record-fingerprint-observation.json
- **Acceptance:** An installed interrupted migration survives harmless provider-config rewrites and ordinary token refresh; genuinely changed endpoint/root remains safely refused with a truthful reason and a supported recovery route. No record is silently rebound to another cloud and all partial copies/source data are retained. Old-record compatibility is explicitly proved.

## PL-005: Preserve truthful migration and timeout reasons

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** F-02; B-03/R-03; I356-L76/I363-L76
- **Owner area:** cloud scan/application outcomes and ES startup card
- **What:** Keep migration application refusals separate from rclone transport return codes. Carry the true reason for unsupported/malformed layout, unreadable settings/record, failed writes and the outer scan timeout into the page/card.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_scan:93,163; cloud_migrate_layout:991; ES main.cpp:686; ThreadedCloudSync.cpp:80
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** Retained UI26 reports a missing folder for a present unsupported marker; full marker/pointer manifests are unchanged. reviewer-coverage-01 R03 returns124 after30.229s without a why line, reaching ES generic fallback.
- **Acceptance:** Installed future/malformed marker, config-read, record/write and outer-timeout challenges each stop safely, preserve state and emit the correct player reason. EN/FR640px page/card frames show those reasons; network refusal and genuine missing-folder controls remain distinct.
- **Existing audit-discovery tracker:** #468 (open).

## PL-006: Content chooser offers ordinary folder names that its setter rejects

- **Severity:** Medium
- **Category:** Acceptance Criteria Gap
- **Source Finding:** G-05; B-14
- **Owner area:** cloud layout/configuration and setup
- **What:** Accept representable folder names, reject actual traversal components and unsafe syntax, and retain successful installed selection/scan and UI proof.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:569; cloud_scan:243; ES GuiMenu.cpp:5256
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** Actual root scan offers MyGames, My Games and Games..old. Only MyGames can be selected; the other two return1 and retain the old path. No cloud mutation. Re-grade Low to Medium for an actual blocked selection of ordinary existing folders. Artifact: evidence/reviewer-leads-03/artifacts/B14-{control,space,dots}-observation.json
- **Acceptance:** Installed scan offers and successfully selects MyGames, My Games and Games..old, preserving cloud bytes and completing a content scan. A640px chooser frame and resulting options/selection frame prove the manual path. Traversal components, newlines and unsafe shell forms remain rejected with unchanged settings.

## PL-007: Implement the required French phone confirmation and finishing text

- **Severity:** Medium
- **Category:** Acceptance Criteria Gap
- **Source Finding:** F-03; B-13; I351-L62; D-CLOUD-164
- **Owner area:** phone sign-in and native finishing surface
- **What:** Implement the explicitly approved phone-close confirmation and native finishing strings in French with an explicit locale source, preserving done-marker and queued reconnect-card behavior. Keep the current local mock-provider QA path.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth; cloud-signin-window.c
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** The standalone HTML literals have no French selection; ES gettext strings cannot translate them. D-CLOUD-164 explicitly includes both surfaces. Existing EN proofs do not establish FR behavior.
- **Acceptance:** Installed EN/FR local-fixture proof retains390px phone confirmation and640px native finishing frames, correct locale text, persistence of finishing until the existing done marker and normal delayed reconnect-card dismissal. No Dropbox credential or additional account reset required.
- **Existing audit-discovery tracker:** #469 (open).

## PL-008: Opening scan rejects a valid escaped config value accepted by the shared reader

- **Severity:** Low
- **Category:** Code Quality
- **Source Finding:** G-04; B-09; D-CLOUD-149
- **Owner area:** cloud layout/configuration and setup
- **What:** Use the same supported non-executing configuration grammar and first-assignment semantics across readers; preserve malformed-input refusal.
- **Where:** projects/ROCKNIX/packages/network/rclone/sources/cloud_scan:60; cloud_migrate_layout:160; cloud_setup:131
- **Why:** Preserve usable cloud content, consistent stored selections and truthful recoverable outcomes under the cited contract.
- **Evidence:** Strict state reads /Custom/My$Backups successfully from the escaped double-quoted assignment; full scan exits1 at SETTINGS BACKUPS. Unsupported export is safely rejected before any wrong-root scan. Artifact: evidence/reviewer-leads-03/artifacts/B09-escaped-observation.json
- **Acceptance:** Installed state and full scan agree on every supported quoted/bare/escaped and duplicate-key fixture, including the escaped-dollar case; exported/malformed/control-character cases stop before listings or mutations. Keep first-assignment semantics and avoid evaluating config as shell.

## Pre-existing tracked scope (not punch items)

The exact missing artifacts in04 remain independently owed: #349 foreign-only
hostname, #352 successful end-to-end manual chooser, #379 settings-only setup,
#353 real mid-copy kill/retry and subsequent discarded-save sync, #377 literal
bucket backup retry, #361 installed125-game pacing, #354 exact mixed-pair
negative, #337/#344 updater network capture, final-candidate brand/secret/leak
sweeps and account metadata, #409 active naming/criteria reconciliation,
#344 licence/source artifacts, public docs and physical/device publication.
#395 disconnected notifications stay unconfigured. Dropbox #463 is optional;
#432 observability and #464 reset automation remain later work. The existing
scope is not silently waived or duplicated into PL IDs.

## Phase 7 resolution gate

PL-008 is resolved from landed source and installed positive/negative controls.
The remaining open rows await their named acceptance evidence; they are not
deferrals or passing gates. The audit tracker stays open. Detailed command and
state-preservation evidence is in [08-installed-resolution.md](08-installed-resolution.md).

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Open | Acceptance unproved on repaired bytes. |
| PL-002 | Open | Acceptance unproved on repaired bytes. |
| PL-003 | Open | Acceptance unproved on repaired bytes. |
| PL-004 | Open | Acceptance unproved on repaired bytes. |
| PL-005 | Open | Acceptance unproved on repaired bytes. |
| PL-006 | Open | Acceptance unproved on repaired bytes. |
| PL-007 | Open | Acceptance unproved on repaired bytes. |
| PL-008 | Resolved | `ed5a6a51f5974deec8748fbf0dbd2f4984b690f5`; reader-values04:8 installed cases, exact values/archive selection and old-source failure control; [resolution](08-installed-resolution.md). |

## Machine-readable index

```yaml
punch_index:

- id: PL-001
  severity: "High"
  category: "Acceptance Criteria Gap"
  source_finding: "F-01; B-01/B-02/R-01; I352-L32/L33/L44"
  owner_area: "cloud content discovery and ES chooser"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:490; cloud_content_restore:1235; ES es-app/src/guis/GuiMenu.cpp:5228"
  acceptance: "A rebuilt candidate passes all seven original controls/challenges plus stranded legacy-root selection/scan, failed-listing refusal and supported-system/empty-local cases; retain cloud hashes/pointers and EN/FR640px chooser/options frames. A deliberately old-source control must reproduce the misses."
  outcome: open

- id: PL-002
  severity: "Medium"
  category: "Interaction Defect"
  source_finding: "G-03; B-07"
  owner_area: "cloud layout/configuration and setup"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:656,878,922,948"
  acceptance: "Installed join/follow/settle with failures at every pointer-publication boundary either retain the entire old selection or recover the complete intended selection on retry; no false current state. Controls preserve custom content/root and nonempty backup tiers. Retain source/installed hashes, pointers and unchanged cloud bytes."
  outcome: open

- id: PL-003
  severity: "Medium"
  category: "Interaction Defect"
  source_finding: "G-01; B-05"
  owner_area: "cloud layout/configuration and setup"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:819,1239"
  acceptance: "Two installed guests, one current and one KEEP on an earlier layout, leave the active earlier shelf in place and current state settled. The genuine recorded/inherited RC2 partial-migration recovery still completes all owned tiers without loss. Include unreadable-listing refusal and repeated scans."
  outcome: open

- id: PL-004
  severity: "Medium"
  category: "Interaction Defect"
  source_finding: "G-02; B-06"
  owner_area: "cloud layout/configuration and setup"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout:1015,1056,1185; cloud_setup:744; ES cloud-folder error/recovery flow"
  acceptance: "An installed interrupted migration survives harmless provider-config rewrites and ordinary token refresh; genuinely changed endpoint/root remains safely refused with a truthful reason and a supported recovery route. No record is silently rebound to another cloud and all partial copies/source data are retained. Old-record compatibility is explicitly proved."
  outcome: open

- id: PL-005
  severity: "Medium"
  category: "Interaction Defect"
  source_finding: "F-02; B-03/R-03; I356-L76/I363-L76"
  owner_area: "cloud scan/application outcomes and ES startup card"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_scan:93,163; cloud_migrate_layout:991; ES main.cpp:686; ThreadedCloudSync.cpp:80"
  acceptance: "Installed future/malformed marker, config-read, record/write and outer-timeout challenges each stop safely, preserve state and emit the correct player reason. EN/FR640px page/card frames show those reasons; network refusal and genuine missing-folder controls remain distinct."
  outcome: open

- id: PL-006
  severity: "Medium"
  category: "Acceptance Criteria Gap"
  source_finding: "G-05; B-14"
  owner_area: "cloud layout/configuration and setup"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_setup:569; cloud_scan:243; ES GuiMenu.cpp:5256"
  acceptance: "Installed scan offers and successfully selects MyGames, My Games and Games..old, preserving cloud bytes and completing a content scan. A640px chooser frame and resulting options/selection frame prove the manual path. Traversal components, newlines and unsafe shell forms remain rejected with unchanged settings."
  outcome: open

- id: PL-007
  severity: "Medium"
  category: "Acceptance Criteria Gap"
  source_finding: "F-03; B-13; I351-L62; D-CLOUD-164"
  owner_area: "phone sign-in and native finishing surface"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth; cloud-signin-window.c"
  acceptance: "Installed EN/FR local-fixture proof retains390px phone confirmation and640px native finishing frames, correct locale text, persistence of finishing until the existing done marker and normal delayed reconnect-card dismissal. No Dropbox credential or additional account reset required."
  outcome: open

- id: PL-008
  severity: "Low"
  category: "Code Quality"
  source_finding: "G-04; B-09; D-CLOUD-149"
  owner_area: "cloud layout/configuration and setup"
  where: "projects/ROCKNIX/packages/network/rclone/sources/cloud_scan:60; cloud_migrate_layout:160; cloud_setup:131"
  acceptance: "Installed state and full scan agree on every supported quoted/bare/escaped and duplicate-key fixture, including the escaped-dollar case; exported/malformed/control-character cases stop before listings or mutations. Keep first-assignment semantics and avoid evaluating config as shell."
  outcome: resolved
  resolution_commit: "ed5a6a51f5974deec8748fbf0dbd2f4984b690f5"
  resolution_evidence: "08-installed-resolution.md; ../../qa-logs/2026-10-06-pixelelated-replacement-15/p4-reader-values-04/"
```
