# Independent Epic audit refutation — M7 #535–539 under #344

You are the independent Anthropic reviewer of an OpenAI-led source-delta audit.
This is two model perspectives total, not a five-seat council. Source is frozen,
uncommitted, identified by attached SHA256 manifest. No source changes during
review. There is no claim of new installed-image or RC readiness.

First give your own findings from the supplied source/evidence, with severity,
concrete trigger, file:line and why an existing guard does not mitigate it.
Then independently refute/narrow/re-grade each primary Medium-or-higher finding.
Finally identify specific coverage limits. Do not treat tracker or prose PASS
as proof; no browser image bytes are included, only reviewed-frame receipts.
You cannot run tools. Distinguish source leads from runtime proof. Quote exact
file:line for every actionable lead. Prefer concrete bugs to speculative style.

Frozen primary findings are F-01 stale scan account identity, F-02 folder-seed
writer outside shared cloud lock, F-03 destructive preview lacks account binding.
The local VM reproductions use actual rclone aliases and tiny synthetic files.
Frame/copy/index delivery and assembled clean/retained-image qualification are
already tracked scope, not new audit-discovered punch items.

Public source, synthetic evidence, and sanitized project notes only. No owner
cloud/device data, live provider tokens, credentials or private keys included.
Numbered code uses original source line numbers. Source snippets are bounded
explicitly; complete diff supplements large files. Review requested at xhigh.


# FILE 01-research-notes.md

# Research — M7 network and cloud feedback #344

**Auditor:** Code Auditor skill, Codex/OpenAI primary (exact served ID unknown)
**Date:** 2026-10-11
**Started:** 2026-10-11T06:52:20.880763+00:00
**Scope:** Epic, bounded issue chain #535–#539 under #344. Independent depth.
**Spec:** inputs/issues.json; docs/pixelelated/cloud-folder-flow-review.md;
D-CLOUD-183/184, D-UI-125, D-WORKFLOW-155/156.

## Phase 0 — source freeze

Skill copy matches primary next. Product/test bytes are frozen in
inputs/source-manifest.json and source/. Primary and ES branches are still
uncommitted; the snapshot identifies bytes, not an imaginary commit. One serial
orchestrator owns this review. No other agent is changing this scope. The owned
VM screen matrix and later local protocol checks supply evidence on frozen bytes;
no implementation changes occur during review without an explicit new revision.

This is one issue chain inside #344, not a review across two epics and not the
release-wide M7 audit. One Fable5.1/xhigh refutation call follows Phases1–4.5.
Two perspectives, no five-seat council. External call has not run. Source-overlay
qualification is separate from #537/#344's installed clean/retained-image gate.

## Phase 1 — authoritative requests and implementation history

All five live issue bodies were read through the Blitterbot GitHub connector;
#536/#537 comments were read separately. None is closed. #535 preserves saved,
protected, unknown and forget behavior while skipping an open-network password.
#536 records Dropbox's first page but does not establish a universal failure or
any tablet UA. Exact owner capture stays private. Known mechanisms are delayed
phone input ordering and blocked authentication navigation. #537 adds explicit
single-active connection lifecycle and replaces ambiguous failed-pairing actions.
#538/#539 were discovered by actual frame/browser QA during this implementation.

Baseline distribution a1b0c65165 and ES1d76b3da7 include earlier #507/#524 fixes.
Recent cloud history includes ed5a6a51f5 (independent-audit repairs), a9af618398
(identity), and earlier phone-input corrections. Preserve session ownership and
state locks; do not reintroduce the old late-create/late-delete rollback race.

The in-scope rules require VM-first proof, byte-preserving progress/credentials,
explicit active-account selection, device-only secrets, target-tool verification,
public flow references and exact-source reviewed frames. Existing selected paths
remain independent; connection changes never relocate cloud files. Public-site
wording is a separate follow-up; no live site deployment or upstream PR is claimed.

## Tier B coverage and lower-tier findings

This is the first independent review of this delta. Implementation checks are
primary evidence, not a prior independent audit. Prior #507/#524 review remains
accepted for unchanged baseline, with its completed fixes present in the base.
The current observed defects (chooser callback lifetime, runtime locale inode,
rollback selection, Clear overlap, Back navigation and stale add-name editor)
were repaired before this source freeze; original failures are retained. Inspect
final frames and runtime receipts, rather than deriving PASS from this summary.

## Research summary

Scope is Wi-Fi selection, browser/phone input, saved cloud connections, their
backup/restore consumers and QA plumbing. Changed core text-editor labels are
caption-only; the new add-name callback reads current draft. Review the seams:
preview versus connection change, OAuth publication versus cancellation, config
versus selection rollback, settings restore versus device-only credentials, and
UI callback destruction/refresh. Firmware install and live-provider sign-in are
explicitly outside this source-delta proof. Final matrix is still being observed;
its unreviewed captures are not accepted evidence.



# FILE 02-forward-audit.md

# Forward audit — M7 network/cloud feedback #344

**Auditor:** Code Auditor skill, Codex/OpenAI
**Date:** 2026-10-11
**Spec:** inputs/issues.json; frozen inputs/source-manifest.json.

## Running notes — 06:57 UTC

### F-01 — scan identity omits the active connection

**Severity:** High. **Status:** confirmed on the actual VM at 07:01 UTC;
checks/target-original/scan.json has scan rc0 and stamp rc0 before AND after alpha→beta.

`cloud_scan:171–191` hashes rclone.conf, paths/rules/system lists but omits
active-connection. Selection changes only that sidecar. `--stamp-valid:233–244`
therefore accepts the same configuration ID across a selected-account change.
The new parent refresh compares the remote list but does not amend this fingerprint.
`checks/scan-context-original.json` proves alpha→beta leaves the hash identical.

Refutation: `cloud_setup validation_context:548–563` already hashes selection,
but this is a separate consumer and does not feed cloud_scan. Search
`rg -n 'context_id|active-connection|sCloudScanRun' cloud_scan GuiMenu.cpp`
confirmed that no selection input reaches this scan identity. Changing credentials
would invalidate it; selecting another already-saved account does not. This is an
introduced cross-system integration gap, not a live-provider inference.

Required repair: include ACTIVE presence/bytes in scan context, retaining distinct
missing versus explicitly empty shapes. Prove old completion invalidation across
selection and guard a change while scanning, on the guest.

### F-02 — folder creation and connection writers do not share exclusion

`cloud_setup --seed-folders:791+` reads a remote name once, then launches several
rclone mkdir/list/copyto calls. `rg -n 'lock|flock' cloud_setup` finds no transfer
lock. GuiMenu7027 invokes the script directly. New select/remove/replace writers
hold cloud_sync.lock, so this particular cloud writer is outside their exclusion.
Source indicates a renewal/removal could change the target or interrupt creation
between calls. Target proof checks/target-original/seed.json has the real seed process alive inside
a synthetic blocked mkdir while cloud_remote select beta returns0. Severity High:
the shared exclusion claim is false; credential replacement/removal shares that
same gate and can split a multi-command writer across account state.

### F-03 — destructive content-match preview lacks account binding

`cloud_content_restore:798–811,889–927` stores timestamp and rows. Its apply
recomputes rows and compares counts/bytes, not source-configuration identity.
The new same-process REMOTENAME recheck at856 only compares a name captured at
that apply's start; a different account selected since the earlier preview can
pass it. Actual target checks/target-original/match.json: preview alpha rc0, switch beta rc0,
apply rc0 deleted local.rom and downloaded beta.rom. The save.srm sentinel survived.
Severity High: consent described a different source account. No physical or owner data used.

## Criterion evaluation

### AC-535-01: Source-bound security classification distinguishes open, protected and unknown/unsupported scan records, including escaped SSIDs, with controls proving unknown security never bypasses the protected flow.

**Source:** #535. **Verdict:** PASS ✓

**Evidence:** WifiText security/profile classification; wifictl security/open-connect paths. checks/input.log: 9 controls rc0, including escaped SSID, mixed/absent/unknown and saved-renamed cases; ES unit receipt:185 cases/4793 assertions.

**Refutation attempted / boundary:** Mixed security and scan failure explicitly refuse open-connect; no empty-password inference.

### AC-535-02: Choosing an unsaved open network reaches connection/progress/outcome without a Wi-Fi password prompt; backend argv contains no invented or stale password. A VM fixture and reviewed frame sequence prove the path.

**Source:** #535. **Verdict:** PASS ✓

**Evidence:** GuiWifi.cpp:249–303 and ApiSystem open-connect argv. VM en640/full-happy and en1280/full-happy open-connected frames; state-fixture manifests and host actual-script argv control.

**Refutation attempted / boundary:** Protected/unknown feed the distinct key path; failed open join does not delete or borrow stored credentials. VM radio is a named nmcli fixture, not physical radio qualification.

### AC-535-03: Protected networks retain the password prompt and success/failure behavior; saved/connected/forget paths remain intact, verified with fixture assertions and affected branch frames. No existing stored credential is overwritten by a failed/open join.

**Source:** #535. **Verdict:** PASS ✓

**Evidence:** Actual VM protected-success, failed, saved-choice, forget and multiple-profiles walks in pix535-ui07/ui08/ui10. Saved profile lifetime old-source ASan fails, corrected pass receipt is retained.

**Refutation attempted / boundary:** Renamed and duplicate profiles were adversarial inputs: a chooser avoids guessing, callback values survive page close. Host explicit-empty key control passes.

### AC-535-04: docs/es-menu-map.md and canonical Wi-Fi IA/flow references include the open/protected/unknown branches, with exact-source EN/FR screenshots at640×480 and the larger supported QA size; current copy/translations and syntax/pin checks accompany the ES change.

**Source:** #535. **Verdict:** PARTIAL ⚠

**Evidence:** Canonical menu/flow and FR strings updated; syntax results rc0; EN/FR640/1280 captures exist. Shared editor reviewed final frames in QA editor/review.json.

**Refutation attempted / boundary:** Final full Wi-Fi frame-index promotion remains delivery work; earlier RESET overlap is rejected, not counted as final proof. ES pin has not moved.

### AC-536-01: The exact page, client/control surface and interaction that fails are recorded; source trace identifies actual user-agent configuration and pointer/click routing without assuming either caused the failure.

**Source:** #536. **Verdict:** PASS ✓

**Evidence:** Existing owner-feedback sanitized trace records Dropbox first page, hand cursor and three refused Microsoft-host navigations. Current browser source has no explicit tablet UA; phone is a relative-input surface.

**Refutation attempted / boundary:** A hand cursor alone is not a failed click; no universal provider outage or speculative UA cause is claimed.

### AC-536-02: A credential-free VM reproduction records pointer hover plus down/up/click events and actual link/button activation, distinguishing the normal hand cursor from lost input/focus. Original failure and backend/browser logs are retained with exact source/image binding.

**Source:** #536. **Verdict:** PASS ✓

**Evidence:** QA browser/result.json and events.jsonl: actual target WebKit receives mouseover/down/up/click, activates button/link. installed.json binds browser04. input.log old-source delayed-move negative control fails as intended.

**Refutation attempted / boundary:** Real WebKit provider fixture proves event behavior, not a mocked browser API. The synthetic local provider supplies no credentials or real Dropbox account.

### AC-536-03: A confirmed fix has an old-source negative control and passing link/button/input/drag/scroll/keyboard/back/cancel cases; otherwise retain the precise unresolved assertion rather than declaring a cause or changing the UA speculatively.

**Source:** #536. **Verdict:** PASS ✓

**Evidence:** checks/input.log 9 rc0 includes movement/drag/key ordering and old-source failure; actual VM browser15 has16 true controls including typing, scrolling, Back, popup return and Close.

**Refutation attempted / boundary:** Provider-handled and modified Back keys remain intact. No real-provider identity/token acceptance claim.

### AC-536-04: Any player-facing or input-flow change updates canonical flow/menu references and reviewed exact-source happy/branch screenshots, EN/FR where text changes, with syntax/package checks before pin promotion. Physical verification requires its named action and device-facts row if needed.

**Source:** #536. **Verdict:** PARTIAL ⚠

**Evidence:** Menu/flow/changelog reference input and popup branches; three final browser frames reviewed and source-bound. Package crosscompile browser04 passed.

**Refutation attempted / boundary:** Full consolidated frame index/public-doc follow-up still precedes pin promotion; no new physical action was needed.

### AC-537-01: Exact-source trace and current UI frames establish what a second setup does, how names are allocated, which paths are selected, and what management actions exist today; distinguish stored from authenticated/reachable connections.

**Source:** #537. **Verdict:** PASS ✓

**Evidence:** cloud_remote list emits stored entries plus explicit active state; GuiMenu.cpp:7915–8016 exposes details. VM lifecycle receipts show two connections and active removal without fallback.

**Refutation attempted / boundary:** A stored listing is not labeled authenticated; separate CHECK CONNECTION performs a bounded listing. Duplicate addition is refused, no silent overwrite.

### AC-537-02: Canonical menu/IA/flow contract clearly separates add, use existing, sign in again, edit and remove; reviewed happy/branch frames show existing provider/account ambiguity, cancellation and actionable failures, at target sizes and supported locales where changed.

**Source:** #537. **Verdict:** PARTIAL ⚠

**Evidence:** GuiMenu.cpp connection/add/form/failure routes and canonical Mermaid; actual EN/FR640/1280 management/forms frames, EN/FR guard11 refusals and editor final review.

**Refutation attempted / boundary:** Final assembled-image and consolidated evidence publication are pending; F-01/F-03 show a stale-result interaction beyond the displayed manager.

### AC-537-03: VM fixtures prove reauthorization preserves the selected remote and folders, new connection creation never overwrites another, failed/cancelled authentication leaves the prior working configuration intact, and edited identity/account changes require an explicit path/usage decision.

**Source:** #537. **Verdict:** PARTIAL ⚠

**Evidence:** Guest transactions21 result.log:21 tests rc0 covers renewal/add/failure/cancel, external writes, config and selection rollback, encryption and preserved paths; actual UI edit confirmations retain folders.

**Refutation attempted / boundary:** F-01/F-03: account switch invalidates neither scan stamp nor destructive preview. Do not treat transactional config tests as whole-operation consent safety.

### AC-537-04: VM before/after manifests prove local removal leaves cloud bytes and unrelated connections intact, handles selected saves/settings/content references and automatic-sync state explicitly, and cannot race an active cloud job into an invalid configuration.

**Source:** #537. **Verdict:** FAIL ✗

**Evidence:** Local removal and selection tests preserve fixture payload, refuse lock contention/auto-sync, reject wrapper dependency. However target-original/seed.json proves a real cloud writer outside the shared lock.

**Refutation attempted / boundary:** F-02: cloud_setup --seed-folders does not participate in cloud_sync.lock. A locked test alone missed this unguarded writer.

### AC-537-05: Installed-image clean and retained-configuration tests cover this flow alongside normal backup/restore and manual folder creation; source/pin, syntax, applicable audit and exact-source screenshot evidence are recorded before completion.

**Source:** #537. **Verdict:** PARTIAL ⚠

**Evidence:** Crossbuilt ES/browser and installed source overlay tested on retained GENERIC_X64; package lint, syntax and host controls pass.

**Refutation attempted / boundary:** Pre-existing #537/#344 installed clean/retained image and normal WebDAV/SFTP round-trip remain open; this audit is not an assembled firmware gate.

### AC-537-06: The installed failure flow has explicitly named outcomes; VM evidence proves retry starts a fresh owned attempt/code, cancellation closes and releases only its own session, old callbacks cannot overwrite the new state, and failed/duplicate-name cases preserve existing credentials/paths. EN/FR reviewed failure/retry/cancel frames and the canonical flow reflect the actual actions.

**Source:** #537. **Verdict:** PASS ✓

**Evidence:** Actual VM oauth07 EN/FR640 and oauth10 EN1280 results: fresh attempt/session/PIN, cancel idle, authorize child ended, config/path/payload hashes unchanged. GuiMenu7779 names TRY AGAIN / CANCEL SIGN-IN. Guest ownership tests pass.

**Refutation attempted / boundary:** Old callback publication, cancel during verification and success-record failure injected; rollback/ownership survives. Auth provider itself is a named rclone-authorize fixture.

### AC-538-01: The two text editors label their existing empty-string action CLEAR / EFFACER; other RESET actions and action callbacks are unchanged, verified by source diff and syntax checks.

**Source:** #538. **Verdict:** PASS ✓

**Evidence:** ES core diff only RESET captions/comparisons/help→CLEAR for the existing empty-string action; FR EFFACER. core syntax09 rc0 and es09 build rc0; final es11 relink preserves units.

**Refutation attempted / boundary:** Unrelated RESET controls untouched; callback implementation preserved.

### AC-538-02: Reviewed EN/FR640/1280 VM frames show clear and cancel labels separately; actual clear and cancel callbacks preserve the established behavior.

**Source:** #538. **Verdict:** PASS ✓

**Evidence:** QA editor/review.json: all8 EN/FR640/1280 plain/OSK variants reviewed. Clear focused on nonempty draft then actual cancel returns to empty saved draft. Matrix17 rc0.

**Refutation attempted / boundary:** Original overlapping FR RESET and stale reopened name retained as rejected frames. Final empty field after cancelled edit is a falsifiable visual check, not only rc0.

### AC-538-03: Canonical flow/frame references, changelog and source-bound receipts accompany the next ES pin. Original rejected overlap frame stays recorded.

**Source:** #538. **Verdict:** PARTIAL ⚠

**Evidence:** Canonical flow/changelog changed and final editor hashes/frames retained; rejected originals retained in QA/rejected.

**Refutation attempted / boundary:** Pin promotion and final whole-flow index remain pending integration work, not a claim already delivered.

### AC-539-01: Actual local-provider navigation goes back on B/Backspace when no editable control owns the key; the original failure and corrected result are retained.

**Source:** #539. **Verdict:** PASS ✓

**Evidence:** Browser15 actual history_back true; original browser12 lacked navigation. Production window key listener handles unmodified Backspace outside editors; final provider-after-back frame reviewed.

**Refutation attempted / boundary:** The old-source failure provides the negative control; a second provider page and its history entry are required to make the assertion meaningful.

### AC-539-02: Text fields retain ordinary character deletion, provider-handled keys and modified shortcuts are not repurposed, and Close/popup return continue to work.

**Source:** #539. **Verdict:** PASS ✓

**Evidence:** Browser15 event receipts: typing_and_backspace, provider_handled_back_preserved, modified_back_preserved, popup_return, parent_usable, close_page true.

**Refutation attempted / boundary:** Editable fields, handled events and modified keys are explicit exclusions, not a general hotkey override.

### AC-539-03: Source/binary binding, runtime events and reviewed flow frames update #536's canonical evidence before the next pin.

**Source:** #539. **Verdict:** PARTIAL ⚠

**Evidence:** Source/binary binding browser04→browser15 and reviewed final frames are in QA/browser; canonical flow updated.

**Refutation attempted / boundary:** Final evidence index and next pin await review/integration; no device image has this fix yet.


## Forward Audit Summary

| Verdict | Count | Criteria |
| --- | ---: | --- |
| PASS ✓ | 12 | AC-535-01, AC-535-02, AC-535-03, AC-536-01, AC-536-02, AC-536-03, AC-537-01, AC-537-06, AC-538-01, AC-538-02, AC-539-01, AC-539-02 |
| PARTIAL ⚠ | 7 | AC-535-04, AC-536-04, AC-537-02, AC-537-03, AC-537-05, AC-538-03, AC-539-03 |
| FAIL ✗ | 1 | AC-537-04 |
| SKIP ○ | 0 |  |
| UNTESTABLE ? | 0 |  |

**Overall Assessment:** FAIL — three confirmed integration defects need correction.

## Coverage Boundary

**Examined:** frozen source/diffs, host script/unit/syntax checks, target transaction tests, actual target WebKit, synthetic ES radio/auth flows and frame review.

**Deliberately not examined:** personal clouds/devices, live account sign-in, new firmware installation; none required for the three confirmed reproductions.

**Dimensions not exercised:** real Wi-Fi radio behavior, provider account policy, cold installed-image/retained-storage qualification and final protocol suites after remediation. Those remain in existing issues.



# FILE 03-retrospective.md

# Retrospective — M7 network/cloud feedback

Date:2026-10-11. Frozen source in inputs/source-manifest.json.

## Architectural coherence and spec fidelity

The shared connection module deliberately introduces one selected account, not
simultaneous multi-cloud sync. Missing sidecar preserves legacy alphabetical
first selection; empty tombstone prevents accidental fallback after removal.
Config staging/verification/publication and OAuth cancellation use compatible
lock order (connection lock then state lock); existing ownership tests exercise
cancel/supersede/success-publication failures. No new cloud relocation appears.

The gaps are consumers outside the new identity/exclusion contract: scan stamps,
folder seed writer and destructive preview. These are integration defects.

## Project conformance

| Rule area | Relevance | Finding |
| --- | --- | --- |
| engineering-practices / es-code-traps | all changed sources and UI lifetime | stack-copy fix and sanitizer negative control; actual target tests retained |
| rclone-cloud-sync / least-surprise / time-to-play | one active account, explicit actions, bounded calls | F-01–03 violate identity/consent/exclusion; staged credential verification bounded |
| vm-first / generic-x64-vm-testing / device-testing-policy | runtime proof | owned guest only; nmcli/authorize fixtures named; actual WebKit/rclone used where available |
| es-native-ui / es-ui-style-guide / es-player-text / player-language | manager/editor/retry/cancel | reviewed EN/FR layouts; no missing expiry inference; final frame-index/pin delivery still pending |
| packaging-and-patches | Python module installed beside CLI | pkgcheck rclone exit0; Python available in image and guest tests execute it |
| upgrade-and-install / release-candidates / bugs-are-agent-first | next installed image | no release claim; image qualification stays #537/#344 |
| documentation-accuracy / change-log | public and canonical flows | local docs updated; separate public-site follow-up must accompany delivery |
| fork-workflow / worktrees / milestone-phase-naming | isolated work and ordered plan | feature worktrees, unchanged next; M7 body lists #535–539 then #528 |
| decision-register / learning-capture / ceremonies | decisions and findings | D-CLOUD-184, D-UI-125, timestamped log and friction entries; final ceremony gate still owed |
| instruction-files / working-principles | canonical rules | next rules loaded, stale harness untouched; rules/register/index gates exit0 |
| adversarial-council / substrate-integrity | independent Epic audit | external phase follows settled primary findings through Facilitator only |
| handheld-evidence | docs/runtime evidence | no personal device action or unredacted private capture published |

## Blindspot review

Applied the register's recurring failure classes: summary versus artifact,
subshell failure loss, no-op assertions, first-source versus final-source proof,
real target tools versus host tools, callback lifetime, inherited lock ownership,
already-written data, default-name drift, watcher completion and seat identity.
The three new findings were proved with actual target scripts; hypothetical
account changes are no longer the only evidence. Rejected frames and failed
fixtures remain rejected. Credentials/private owner images never enter this packet.
No prior audit PASS was imported as proof of this new selected-account seam.

## Interaction: connection manager × scans

**State shared:** active-connection and rclone.conf. **Wipe risk:** stale options
describe a different account. **Test coverage:** TESTED. **Finding:** broken F-01.
cloud_setup validation_context includes the sidecar but cloud_scan does not.

## Interaction: connection manager × cloud writers

**State shared:** config and cloud_sync.lock. **Wipe risk:** changing/removing
credentials during a multi-command operation. **Test coverage:** TESTED seed
writer plus transactional busy refusal. **Finding:** broken F-02 at seed writer;
saved-data/content transfers already hold the shared lock during transfers.

## Interaction: destructive preview × selected account

**State shared:** match plan, config/selection/paths. **Wipe risk:** local content
removed/downloaded from an account not described by the confirmed preview.
**Test coverage:** TESTED two actual local aliases. **Finding:** broken F-03.

## Sibling-site search

Commands: `rg -n 'listremotes.*head|first_remote|active-connection|cloud_sync.lock'
projects/ROCKNIX/packages/network/rclone/sources/*`; `rg -n 'MATCH_PLAN|context_id|validation_context|take_cloud_lock'`
in the same tree; `git log -S active-connection --all --oneline -- projects/ROCKNIX/packages/network/rclone`.

| Class / site | Disposition | Basis |
| --- | --- | --- |
| F-01 scan context | FIX-NOW | add selection presence/bytes to fingerprint |
| Adjacent setup validation context | SAFE-AS-TESTED/code-read | already hashes active selection; unchanged-context tests needed after repair |
| F-02 seed writer | FIX-NOW | hold shared transfer lock before resolving target through final write/readback |
| Adjacent saves backup/restore | SAFE-AS-TESTED/code-read | resolve first_remote inside locked transfer body; staged connection tests refuse same lock |
| F-03 match preview/apply | FIX-NOW | bind plan to configuration identity, reject old unbound plans |
| Adjacent content copy preflight | FIX-NOW | current name-only recheck misses same-name account/credential edits; bind full context across preflight/lock |
| Adjacent settings backup/restore | SAFE-AS-TESTED/code-read | resolves selected remote under cloud lock; active-connection is device-only backup exclusion |
| External manual rclone config | BY-DESIGN boundary | outside cooperative lock protocol; writer compares current config before publication; no global process ban promised |

## Missing artifacts and tracked scope

Final whole-flow index, public documentation follow-up and installed-image
qualification were already open delivery work in #535–539/#344, not newly
discovered punch items. Search `rg --files docs/qa-logs/2026-10-11-network-cloud-management`
finds receipts/editor/browser and rejected frames; no final whole-flow index yet.

## Instruction File Recommendations

No new rule required: current shared-state, consent and exact-source evidence
rules already cover all three findings. Add executable target controls to avoid
another general prose rule. This is one issue chain, not evidence of three
independent process violations warranting a new instruction.

## Tier B visual-QA consolidation

Editor8-mode final review passed. Manager/form/refusal/source receipts and final
browser3-frame review exist. Original FR RESET overlap, stale name reopen and
long form hint are retained as rejected. Wi-Fi guard and manager flows keep
their actual es07/es08 sources, with final es11 editor delta stated separately.
Final index must not relabel old captures as the new binary.

## Retrospective Summary

Architecture is coherent but incomplete at three shared-state boundaries.
No extra provider or firmware scope is introduced. Resolve these defects,
then finish final proof/delivery and the already-tracked assembled-image gate.



# FILE 04-analysis.md

# Audit Analysis — M7 network/cloud feedback #344

Date:2026-10-11. Issues:#535–539. Scope:Epic issue chain under #344.
Source:uncommitted frozen snapshots, inputs/source-manifest.json.

## Executive summary

The UI and transactional connection changes have substantial target proof,
including rejected-original controls. The change is not ready to integrate:
three High interaction defects survive actual VM reproduction. Nothing here
certifies a new installed firmware image or a release candidate.

## Acceptance-criteria scorecard

| ID | Verdict | Evidence/gap |
| --- | --- | --- |
| AC-535-01 | PASS ✓ | Primary artifact in02 |
| AC-535-02 | PASS ✓ | Primary artifact in02 |
| AC-535-03 | PASS ✓ | Primary artifact in02 |
| AC-535-04 | PARTIAL ⚠ | Repair/remaining delivery described in02 |
| AC-536-01 | PASS ✓ | Primary artifact in02 |
| AC-536-02 | PASS ✓ | Primary artifact in02 |
| AC-536-03 | PASS ✓ | Primary artifact in02 |
| AC-536-04 | PARTIAL ⚠ | Repair/remaining delivery described in02 |
| AC-537-01 | PASS ✓ | Primary artifact in02 |
| AC-537-02 | PARTIAL ⚠ | Repair/remaining delivery described in02 |
| AC-537-03 | PARTIAL ⚠ | Repair/remaining delivery described in02 |
| AC-537-04 | FAIL ✗ | Repair/remaining delivery described in02 |
| AC-537-05 | PARTIAL ⚠ | Repair/remaining delivery described in02 |
| AC-537-06 | PASS ✓ | Primary artifact in02 |
| AC-538-01 | PASS ✓ | Primary artifact in02 |
| AC-538-02 | PASS ✓ | Primary artifact in02 |
| AC-538-03 | PARTIAL ⚠ | Repair/remaining delivery described in02 |
| AC-539-01 | PASS ✓ | Primary artifact in02 |
| AC-539-02 | PASS ✓ | Primary artifact in02 |
| AC-539-03 | PARTIAL ⚠ | Repair/remaining delivery described in02 |

Counts: 12 PASS, 7 PARTIAL, 1 FAIL,
0 SKIP, 0 UNTESTABLE; 20 criteria. Partial image/index delivery remains
under existing issue owners, separate from the three new defects.

## Code quality assessment

Private staging and owner-checked publication improve credential safety.
Single active selection avoids hidden fallback. Complexity remains in shared
shell transfer consumers and callback ownership; those require intersection
tests rather than only isolated manager tests.

## Cornerstone conformance

03 records applicable rule areas, invariants, blindspots and sibling sites.
No owner data/device used; no upstream fork migration reintroduced. Shared
state identity/exclusion does not yet satisfy progress preservation and consent.

## Spec fidelity

Add/use/renew/edit/remove and retry/cancel follow the accepted flow. Existing
paths stay explicit and no cloud content is moved by management. Cross-operation
consent fails at F-01–03. No undocumented version/release policy change.

## Missing artifacts

Already tracked: final flow index, public documentation follow-up, protocol
qualification after remediation, and clean/retained installed image #537/#344.

## Risk assessment

| Finding | Severity | Impact | Required repair |
| --- | --- | --- | --- |
| F-01 | High | stale scan accepted for another selected account | add ACTIVE presence/bytes to context and test completed/in-flight invalidation |
| F-02 | High | seed writer can interleave with connection update/remove | use shared lock before target resolution until final folder writes/readback |
| F-03 | High | destructive apply uses different account from preview | bind preview to full context, recheck under lock, reject old unbound plans; cover adjacent copy preflight |

## Finding Verification (Phase 4.5)

| Finding | Severity | Survived refutation? | What was checked |
| --- | --- | --- | --- |
| F-01 | High | yes | Full cloud_scan context/result/completion path re-read; actual VM scan rc0 and stamp valid both before/after switch. Separate setup validation hash is not consumed by scan. |
| F-02 | High | yes | Full seed branch and direct GuiCloudTransfer invocation re-read; no outer lock. Actual blocked mkdir permits cloud_remote select rc0 while seed process alive. |
| F-03 | High | yes | Full preview/apply spend/verb/count guards re-read. Real rclone dry-run/apply removes local.rom and pulls beta.rom after alpha preview. Same-verb/count guard does not bind account. Save sentinel preserved. |

The original-function host lead was independently reproduced on the guest.
Probes in checks/target-original/ include exact installed script hashes and
raw sanitized outcomes. No finding depends on a mocked cloud mutation.

## Coverage boundary

Examined: exact-source diff/code, host syntax/unit/script controls, guest
transactions, actual WebKit provider fixture, synthetic ES input/auth/radio
walks and real local-rclone identity/race/preview probes. Personal data excluded.
Not examined: live provider login policy, physical radios and newly assembled
firmware install/upgrade; those are outside this source-delta gate.

## Second opinion (Phase 4.6)

Pending. Primary Codex/OpenAI, exact model unknown. Independent depth:2 model
perspectives,1 external reviewer,1 Epic refutation call. Selected installed
Fable5.1/xhigh via OpenRouter Facilitator; no call or verification claimed yet.
Review plan is second-opinions/review-plan.json. The source freeze stays in force.

## Instruction File Recommendations

No new doctrine: existing shared-state rules apply. Add target regression
controls for selection, seed exclusion and preview account binding.

## Quality self-check

| Item | Status |
| --- | --- |
| Scorecard IDs match02 | yes; computed counts |
| Conformance and sibling tables | present in03 |
| Coverage boundary | present02/04 |
| Critical/High verification | all3 High reproduced on actual guest |
| Second opinion | pending runnable Phase4.6 |
| Instruction recommendations | present; no unnecessary new rule |
| Tier B review | editor/browser accepted; full-index delivery still open |
| Evidence/reproducible/actionable | fixtures/hashes/results retained; no release claim |



# FILE inputs/source-manifest.json

[
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c",
    "sha256": "39af3e041d9871c4fb636cff71934ddf3ea13c690002e77af5ea6d82d8fff4f8",
    "size": 47987
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/package.mk",
    "sha256": "5edae1ba9d9cb5576b187be65829896a071839279368a1a4422a4ca9932bac5c",
    "size": 5417
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_backup",
    "sha256": "7b6e49223f750f92e28a2f6eb6f2895d3b840c89c7c4eb73860d896a1d742dd9",
    "size": 129546
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_connections.py",
    "sha256": "c010965b42840f8c2c8f946bfc0a61787784531dead4199e5d625d53d00573e8",
    "size": 10133
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup",
    "sha256": "e66c86e1e8cad3b0b6a875741ff9774c8b2e7af5a389391aafb52d99cfa048b0",
    "size": 39237
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore",
    "sha256": "a5321380835815ca023fd1afe357403db3d2eb46e044503937aa18c37c36e9b4",
    "size": 81879
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth",
    "sha256": "0d40129169b34bd5caad3515dffa75a1a5f9b620eee3f7a4d6a15ebb58be240e",
    "size": 117159
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_remote",
    "sha256": "24777687a1d48d98e9797aae89851d49425ba11c330750dbf806549b70c0b365",
    "size": 13942
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_restore",
    "sha256": "1881c490f4b68f5587b1697beeb6fd04edcd4d2fb3f576555a85e5ee83b99580",
    "size": 115558
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_scan",
    "sha256": "17afba1861701b20d1590a10d2c3797f208879e04ca98ab73128e8c8aadeb3d4",
    "size": 16003
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/network/rclone/sources/cloud_setup",
    "sha256": "32d8696ce4ea467b62223fa17977a474e06d04ba5fa80f702e82cc2eea82d067",
    "size": 46618
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool",
    "sha256": "cd5c7b1b7c75efc295ef3004cf0c26f4b0b176d02ff162a770a83d6f69e2e277",
    "size": 102360
  },
  {
    "repository": "distribution",
    "path": "projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl",
    "sha256": "32d43774637fed12b6ed083ce3f9c0dcc63d97850f0d515fc670b620a36fe2d4",
    "size": 23854
  },
  {
    "repository": "distribution",
    "path": "tools/cloud-connections-test",
    "sha256": "5f8e62411dfa4c756ece72ee358f4e7dc5a38c79ea16884675fe944da90578f3",
    "size": 11052
  },
  {
    "repository": "distribution",
    "path": "tools/cloud-input-test",
    "sha256": "3cac55d3fc3321026ad1fed4f0a3cd7d33c1d976e8a379e297d070f0c0e1aac4",
    "size": 7832
  },
  {
    "repository": "distribution",
    "path": "tools/cloud-round-trip",
    "sha256": "9fe3545b19c62cffd016b298a9d25f04c145caed495dca0a29b04d955deb78c3",
    "size": 473280
  },
  {
    "repository": "distribution",
    "path": "tools/cloud-test-backend",
    "sha256": "c5d404e9a868dd0918c53d80cb860fab9af3e6ecaade72e3462158181debf358",
    "size": 41389
  },
  {
    "repository": "distribution",
    "path": "tools/last-good-scripts-test",
    "sha256": "0b01ab6e30cd60afe0593d092b35267d647008cc7e68dfbef4f4d85711aad5d8",
    "size": 1171199
  },
  {
    "repository": "distribution",
    "path": "tools/rasteratops-vm-cloud-epic",
    "sha256": "fa7a93363d61cc03bc9e7521ead5a38ccadac6b682e1c6dc58136912b19aad6e",
    "size": 32291
  },
  {
    "repository": "distribution",
    "path": "tools/test-fixtures/cloud_connections_fixture.py",
    "sha256": "5780d75a3e3ff17a7052f5e6818c50bfcac8cd8c5ee7140af6ad3550421d4a8d",
    "size": 1692
  },
  {
    "repository": "distribution",
    "path": "tools/vm-qa",
    "sha256": "7b3d7d25e21381ae1aa5749c62bebfb4e03287d383c467a0a569cfdd695c956a",
    "size": 40488
  },
  {
    "repository": "distribution",
    "path": "tools/vm-upgrade-rehearsal",
    "sha256": "26cd4be98fed7c733da92dfc1bc63a7fff820c6598c4b023dbad0e1dd70079ab",
    "size": 13312
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/ApiSystem.cpp",
    "sha256": "0618194ab89ff74b8673fc00b11ee2b5984dd026a76611644e23eb3d5cdd0913",
    "size": 99789
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/ApiSystem.h",
    "sha256": "ab7aff676e5db21e86383c4cc45cb498e802e286c08be9e6efadd623c04932f8",
    "size": 16290
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/WifiText.cpp",
    "sha256": "ce4aa9abb3a57edd897ceeebec8ec8f201a4092efd9f5ff06e6e4f699d71be7a",
    "size": 8214
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/WifiText.h",
    "sha256": "9a3370dad382231f93c29aa0bf627b61cae40a4bbb28d3f2f9c215dd0e9dd39b",
    "size": 8030
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/guis/GuiMenu.cpp",
    "sha256": "2d200fdf3ec930ef93b446bc08b009de8113f454e958b68bb4e6e1215e16aa27",
    "size": 506517
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/guis/GuiMenu.h",
    "sha256": "827c369d015ed2f0675e4ab6ff92eacc6f4dc3c1141a3069a1c8532ebffda49b",
    "size": 6699
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/guis/GuiWifi.cpp",
    "sha256": "73487c14809b9f88356f0777165a05b2882d5a9ee0b8f8f3198895f83b9502ed",
    "size": 15761
  },
  {
    "repository": "emulationstation",
    "path": "es-app/src/guis/GuiWifi.h",
    "sha256": "5a1029523c464d5e34b629c5f697b6e594615ffea4e090435c66b3080b5599b9",
    "size": 2737
  },
  {
    "repository": "emulationstation",
    "path": "es-app/tests/unit/WifiTextTests.cpp",
    "sha256": "15521905977d9ef6f5d541ca833812012cc3062f666b9dd004fe1bfc71d14a46",
    "size": 15744
  },
  {
    "repository": "emulationstation",
    "path": "es-core/src/guis/GuiTextEditPopup.cpp",
    "sha256": "cfc616dcb6f9dbd0a02e868f10dfa6046a6a5cb7e7c1e2ef75db9b78f838c804",
    "size": 3155
  },
  {
    "repository": "emulationstation",
    "path": "es-core/src/guis/GuiTextEditPopupKeyboard.cpp",
    "sha256": "6eeb14b1a3bb003b512281af4bd61a245e44354857326c121292a65814689e8f",
    "size": 18254
  },
  {
    "repository": "emulationstation",
    "path": "locale/lang/fr/LC_MESSAGES/emulationstation2.po",
    "sha256": "b4383dde69bfb6ef5bb91ba5a53997b5067aed18b8e0e0fcad0f48ec0c37d575",
    "size": 183112
  },
  {
    "repository": "emulationstation",
    "path": "tests/wifi-profile-lifetime.py",
    "sha256": "76353bd9ab6810e0189a7e1af5e8d8794314ddd79f91d923446e78a59fda762b",
    "size": 1802
  }
]



# FILE inputs/base-heads.json

{
  "distribution": "a1b0c651654bbe550fec522c591fbfdb73c220a0",
  "emulationstation": "1d76b3da7da75794066df1c089931b890304da7a"
}



# FILE inputs/distribution.diff

diff --git a/projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c b/projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c
index 24888d4c75..99beb6ef18 100644
--- a/projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c
+++ b/projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c
@@ -41,6 +41,14 @@ static gboolean host_permitted(const char *host)
         return TRUE;
     if (!allowed_host)
         return TRUE;
+    /* Dropbox offers these identity providers on its sign-in page. They
+     * are exact authentication hosts, not a general browsing exception. */
+    if (g_ascii_strcasecmp(allowed_host, "dropbox.com") == 0 &&
+        (g_ascii_strcasecmp(host, "accounts.google.com") == 0 ||
+         g_ascii_strcasecmp(host, "appleid.apple.com") == 0 ||
+         g_ascii_strcasecmp(host, "login.microsoftonline.com") == 0 ||
+         g_ascii_strcasecmp(host, "login.live.com") == 0))
+        return TRUE;
     /* the host itself, or any subdomain of it: providers bounce sign-ins
      * through their own auth and CDN subdomains constantly. */
     size_t hl = strlen(host), al = strlen(allowed_host);
@@ -379,6 +387,11 @@ static void on_probe(GObject *source, GAsyncResult *result, gpointer data)
         return;
     }
 
+    /* A reply from the covered parent must not change the popup's caret. */
+    if (osk && source != G_OBJECT(osk->view)) {
+        g_object_unref(value);
+        return;
+    }
     char *text = jsc_value_to_string(value);
     if (g_getenv("CLOUD_SIGNIN_DEBUG"))
         g_message("probe %s", text);
@@ -665,12 +678,24 @@ static int page_worth_recording(const char *uri)
 static void on_load_changed(WebKitWebView *view, WebKitLoadEvent event,
                             gpointer data)
 {
-    if (event != WEBKIT_LOAD_FINISHED)
+    Osk *osk = data;
+    if (event != WEBKIT_LOAD_FINISHED || (osk && osk->view != view))
         return;
 
     GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
     if (stack)
-        gtk_stack_set_visible_child_name(GTK_STACK(stack), "page");
+        gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(view));
+
+    /* WebKitGTK does not map Backspace to history navigation. Handle the
+     * bubbled DOM event, respecting editable fields, already-handled keys and
+     * modified shortcuts. Window listeners see provider document handlers first. */
+    webkit_web_view_evaluate_javascript(view,
+        "if(!window.__pixelelatedBackKey){window.__pixelelatedBackKey=true;"
+        "window.addEventListener('keydown',function(e){"
+        "if(e.key!=='Backspace'||e.defaultPrevented||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;"
+        "var t=e.target;if(t&&(t.isContentEditable||(t.closest&&t.closest('input,textarea,select'))))return;"
+        "e.preventDefault();history.back();});}",
+        -1, NULL, NULL, NULL, NULL, NULL);
 
     /* Every page starts at the top. A provider's sign-in runs several steps
      * through one window, and arriving at the next one already scrolled --
@@ -826,14 +851,70 @@ static gboolean on_decide_policy(WebKitWebView *view,
     if (!webkit_navigation_action_is_user_gesture(action))
         return FALSE;
 
-    if (!host_permitted(g_uri_get_host(parsed))) {
-        g_message("refused navigation to %s", uri);
+    const char *host = g_uri_get_host(parsed);
+    if (!host_permitted(host)) {
+        g_message("refused navigation to host %s", host ? host : "(none)");
         webkit_policy_decision_ignore(decision);
         return TRUE;
     }
     return FALSE;
 }
 
+/* OAuth providers can open a related window and send a result to opener.
+ * Keep that relationship, but show only one authentication surface at a time
+ * in the existing window. No extra tabs, address bar, or general browsing. */
+static void on_auth_close(WebKitWebView *view, gpointer data)
+{
+    Osk *osk = data;
+    GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
+    WebKitWebView *parent = g_object_get_data(G_OBJECT(view), "auth-parent");
+    if (!parent || !stack)
+        return;
+    osk->view = parent;
+    g_object_set_data(G_OBJECT(stack), "auth-popup", NULL);
+    gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(parent));
+    gtk_widget_grab_focus(GTK_WIDGET(parent));
+    on_load_changed(parent, WEBKIT_LOAD_FINISHED, osk);
+    gtk_widget_destroy(GTK_WIDGET(view));
+}
+
+static void on_auth_ready(WebKitWebView *view, gpointer data)
+{
+    Osk *osk = data;
+    GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
+    osk->view = view;
+    gtk_widget_show(GTK_WIDGET(view));
+    gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(view));
+    gtk_revealer_set_reveal_child(GTK_REVEALER(osk->revealer), FALSE);
+    gtk_widget_grab_focus(GTK_WIDGET(view));
+}
+
+static GtkWidget *on_auth_create(WebKitWebView *view,
+                                 WebKitNavigationAction *action, gpointer data)
+{
+    GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
+    const char *uri = webkit_uri_request_get_uri(webkit_navigation_action_get_request(action));
+    g_autoptr(GUri) parsed = g_uri_parse(uri, G_URI_FLAGS_NONE, NULL);
+    if (!stack || g_object_get_data(G_OBJECT(stack), "auth-popup") || !parsed)
+        return NULL;
+    const char *scheme = g_uri_get_scheme(parsed);
+    gboolean network = g_strcmp0(scheme, "https") == 0 || g_strcmp0(scheme, "http") == 0;
+    gboolean blank = g_strcmp0(uri, "about:blank") == 0 && webkit_navigation_action_is_user_gesture(action);
+    if ((!network || !host_permitted(g_uri_get_host(parsed))) && !blank)
+        return NULL;
+    GtkWidget *popup = webkit_web_view_new_with_related_view(view);
+    webkit_web_view_set_settings(WEBKIT_WEB_VIEW(popup), webkit_web_view_get_settings(view));
+    g_object_set_data(G_OBJECT(popup), "stack", stack);
+    g_object_set_data(G_OBJECT(popup), "auth-parent", view);
+    g_object_set_data(G_OBJECT(stack), "auth-popup", popup);
+    g_signal_connect(popup, "decide-policy", G_CALLBACK(on_decide_policy), NULL);
+    g_signal_connect(popup, "load-changed", G_CALLBACK(on_load_changed), data);
+    g_signal_connect(popup, "ready-to-show", G_CALLBACK(on_auth_ready), data);
+    g_signal_connect(popup, "close", G_CALLBACK(on_auth_close), data);
+    gtk_stack_add_named(GTK_STACK(stack), popup, "auth-popup");
+    return popup;
+}
+
 int main(int argc, char **argv)
 {
     if (argc < 2) {
@@ -894,6 +975,7 @@ int main(int argc, char **argv)
 
     g_signal_connect(view, "decide-policy", G_CALLBACK(on_decide_policy), NULL);
     g_signal_connect(view, "load-changed", G_CALLBACK(on_load_changed), &osk);
+    g_signal_connect(view, "create", G_CALLBACK(on_auth_create), &osk);
     g_signal_connect(window, "key-press-event", G_CALLBACK(on_key), &osk);
 
     /* Something to look at while the provider's page loads. Six seconds of
diff --git a/projects/ROCKNIX/packages/network/rclone/package.mk b/projects/ROCKNIX/packages/network/rclone/package.mk
index ca357f13ab..f3bd2b3572 100644
--- a/projects/ROCKNIX/packages/network/rclone/package.mk
+++ b/projects/ROCKNIX/packages/network/rclone/package.mk
@@ -65,6 +65,7 @@ makeinstall_target() {
   cp cloud_setup ${INSTALL}/usr/bin/
   cp cloud_folder_validate ${INSTALL}/usr/bin/
   cp cloud_remote ${INSTALL}/usr/bin/
+  cp cloud_connections.py ${INSTALL}/usr/bin/
   cp cloud_device_id ${INSTALL}/usr/bin/
   cp cloud_oauth ${INSTALL}/usr/bin/
   cp cloud_content_restore ${INSTALL}/usr/bin/
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup b/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
index 0f1eea46bc..66e9d98ee4 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup
@@ -468,19 +468,11 @@ take_cloud_lock() {
     done
 }
 
-# The configured remote, by the same rule as `rclone listremotes | head -1`
-# -- the first section name in sorted order -- read from the config file
-# rather than by starting rclone, which costs close to a second on a
-# handheld. rclone remains the fallback if the file yields nothing.
+# The shared explicit selection, with legacy first-name behavior only when
+# the sidecar is absent. Empty or missing selected names never fall back to
+# another account (D-CLOUD-184). Keep the internal function name for callers.
 first_remote() {
-    local name
-    name=$(grep -o '^\[[^]]*\]' /storage/.config/rclone/rclone.conf 2>/dev/null \
-           | tr -d '[]' | sort | head -1)
-    if [ -n "${name}" ]; then
-        printf '%s:\n' "${name}"
-    else
-        rclone listremotes 2>/dev/null | head -1
-    fi
+    "$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null
 }
 
 # Does the remote compare files by size alone? rclone decides equality by
@@ -962,7 +954,7 @@ check_internet() {
     log_message "Checking cloud storage reachability..." "false"
 
     local remote probe_rc=1
-    remote=$(rclone listremotes 2>/dev/null | head -1)
+    remote=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
     if [ -n "${remote}" ]; then
         rclone lsd "${remote}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1; probe_rc=$?
         if [ "${probe_rc}" -eq 0 ]; then
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
index 5cc3fd5559..5d8a08642d 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup
@@ -194,7 +194,7 @@ case "${CONTENT_REMOTE}" in
         exit 1 ;;
 esac
 
-REMOTENAME=$(rclone listremotes | head -1)
+REMOTENAME=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active)
 if [ -z "${REMOTENAME}" ]; then
     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
@@ -682,6 +682,13 @@ take_cloud_lock
 # the change: it adds no subshell, so exits, traps and variables behave
 # exactly as they did.
 {
+# Settings may change while the interactive preview is open. Re-check under
+# the transfer lock before sending anything to the previously named cloud.
+if [ "$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)" != "${REMOTENAME}" ]; then
+    echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
+    echo "Your cloud connection changed. Start this operation again."
+    exit 1
+fi
 UNIT_N=${#DIRS[@]}; UNIT_I=0
 for DIR in "${DIRS[@]}"; do
     set_system_save_excludes "${DIR}"
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
index b928cfec18..28e4c27ff5 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore
@@ -231,7 +231,7 @@ case "${CONTENT_REMOTE}" in
         exit 1 ;;
 esac
 
-REMOTENAME=$(rclone listremotes | head -1)
+REMOTENAME=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active)
 if [ -z "${REMOTENAME}" ]; then
     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
@@ -852,7 +852,10 @@ match_run() {
     fi
 
     # The preview is read-only and may run beside a transfer; applying is one.
-    [ "${apply}" = "1" ] && take_cloud_lock
+    if [ "${apply}" = "1" ]; then
+        take_cloud_lock
+        [ "$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)" = "${REMOTENAME}" ] || return 1
+    fi
     # As at the foot of the script: the rest of the run cannot leak the
     # lock into rclone. Closing a descriptor that was never opened (the
     # preview, which takes no lock) is a no-op.
@@ -1476,6 +1479,13 @@ take_cloud_lock
 # the change: it adds no subshell, so exits, traps and variables behave
 # exactly as they did.
 {
+# Settings may change while the interactive preview is open. Re-check under
+# the transfer lock before sending anything to the previously named cloud.
+if [ "$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)" != "${REMOTENAME}" ]; then
+    echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
+    echo "Your cloud connection changed. Start this operation again."
+    exit 1
+fi
 UNIT_N=${#DIRS[@]}; UNIT_I=0
 tree_record_take
 for DIR in "${DIRS[@]}"; do
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth b/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
index bb49701782..4284fc751a 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth
@@ -61,6 +61,7 @@ import socket
 import struct
 import subprocess
 import sys
+import cloud_connections as connections
 import threading
 import time
 import shlex
@@ -513,9 +514,9 @@ class Session:
             return self._config_result
 
     def _create_remote(self):
-        # One create at a time within the serve: an attempt that finishes
-        # late removes what it made (below) before a newer one asks whether
-        # that name is taken.
+        # One create at a time within the serve. An obsolete attempt never
+        # publishes its staged credentials; cancellation and publication
+        # use the same state lock below.
         with _CREATE_LOCK:
             return self._create_remote_locked()
 
@@ -526,77 +527,26 @@ class Session:
         if self.superseded:
             log("the sign-in was closed before its remote was saved; nothing was saved")
             return False, CLOSED_EARLY
-        # Which remotes exist, or no create at all: a listing that failed
-        # read as "none of that name" and the create went ahead over
-        # whatever was there (#308 gpt F-RS-23).
-        listed = subprocess.run([RCLONE, "listremotes"],
-                                capture_output=True, text=True)
-        if listed.returncode != 0:
-            log("could not list the configured remotes (exit %d); not creating one"
-                % listed.returncode)
-            return False, ("The sign-in worked, but your handheld's cloud "
-                           "settings couldn't be read.")
-        if "%s:" % name in listed.stdout.split():
-            return False, "a remote called '%s' already exists" % name
-
-        result = subprocess.run(
-            [RCLONE, "config", "create", name, self.backend,
-             "token=%s" % self.token, "--non-interactive"],
-            capture_output=True, text=True)
-        if result.returncode != 0:
-            # A fixed sentence, and rclone's exit code in the log -- never its
-            # words. They went to cloud_sync.log as "could not finish the
-            # sign-in: <rclone's stderr>" and into the page, and an rclone
-            # that echoed a parameter would have put the token there (audit
-            # #307 PL-074).
-            log("rclone could not save the remote (exit %d)" % result.returncode)
-            return False, ("The sign-in worked, but it couldn't be saved on "
-                           "your handheld.")
-
-        # Prove it before saying so. A token that parses is not a token that
-        # works, and cloud_remote takes the same posture.
-        check = subprocess.run(
-            [RCLONE, "lsd", "%s:" % name, "--contimeout", "10s",
-             "--timeout", "20s", "--low-level-retries", "1", "--retries", "1"],
-            capture_output=True, text=True)
-        if check.returncode != 0:
-            gone = subprocess.run([RCLONE, "config", "delete", name],
-                                  capture_output=True)
-            if gone.returncode != 0:
-                log("remote %s did not respond and could not be removed either "
-                    "(rclone config delete exited %d); it stays until the next "
-                    "sign-in replaces it" % (name, gone.returncode))
-            return False, "signed in, but the remote did not respond"
-
-        # Published only while this attempt still speaks for the state, and
-        # only from starting or waiting. The write's answer used to be
-        # dropped: an attempt a restart had replaced, or one the serve had
-        # already closed -- its timeout's failed, a cancel's idle -- went on
-        # to return success, and its caller stopped the pad and wrote the
-        # signed-in marker `wait` returns on, over a state that said
-        # otherwise; a remote no screen had reported stayed, and the next
-        # sign-in of that name was refused as already there (the audit of
-        # the fix round, PL-032: gpt G2-C-03, the blind pass's S-25, claude
-        # G2-C-03). Refused, the remote this attempt made is taken away
-        # again, so what the device holds is what the state says.
-        if not write_owned(self.attempt, owner=self.gen,
-                           from_status=(None, "starting", "waiting"),
-                           status="signed-in", remote=name):
-            # Checked, not assumed (the audit of the fixes, gpt G3-D-06): a
-            # delete that fails leaves the remote installed, and the log
-            # said it was gone.
-            gone = subprocess.run([RCLONE, "config", "delete", name],
-                                  capture_output=True)
-            if gone.returncode == 0:
-                log("the sign-in finished after it had been closed or replaced; "
-                    "the remote it made was removed")
-            else:
-                log("the sign-in finished after it had been closed or replaced; "
-                    "the remote it made could NOT be removed (rclone config "
-                    "delete exited %d) and stays until the next sign-in "
-                    "replaces it" % gone.returncode)
-            return False, CLOSED_EARLY
-        log("remote %s created for %s" % (name, self.backend))
+        def publish(commit):
+            # Hold the same cross-process state lock as cancellation until
+            # both the config and its success record have been published.
+            with _state_locked():
+                state = read_state()
+                if (self.superseded or
+                    (self.attempt is not None and state.get("attempt") != self.attempt) or
+                    (self.gen is not None and state.get("session") != self.gen) or
+                    state.get("status") not in (None, "starting", "waiting")):
+                    raise connections.Refused(CLOSED_EARLY)
+                commit()
+                state.update(status="signed-in", remote=name)
+                _write_whole(state)
+        try:
+            connections.save(name, self.backend, [("token", self.token)],
+                             replace=getattr(self, "replace", False), publish=publish)
+        except (connections.Refused, OSError) as exc:
+            log("the sign-in could not be saved; previous settings retained")
+            return False, str(exc) if isinstance(exc, connections.Refused) else "Your cloud settings could not be saved."
+        log("remote %s verified and saved for %s" % (name, self.backend))
         return True, name
 
 
@@ -1078,7 +1028,11 @@ window.onerror = function (message) {
   var ready = false;
   var page = null;
   var queue = Promise.resolve();
+  var pendingMove = null;
   function send(body) {
+    // Seal any queued movement before this key/click. Later drags start a
+    // new batch behind it, so a tap cannot overtake its final pointer move.
+    pendingMove = null;
     queue = queue.then(function () {
       return fetch("/" + pin, {
         method: "POST",
@@ -1226,29 +1180,24 @@ window.onerror = function (message) {
   var restX = 0, restY = 0;
   function at(e) { var t = e.touches ? e.touches[0] : e; return {x: t.clientX, y: t.clientY}; }
 
-  // Movement is coalesced, not queued. A finger produces about sixty events a
-  // second and each request takes longer than that to complete, so putting
-  // them in the same strict queue as keystrokes built a backlog that kept
-  // draining after the finger stopped -- the pointer carried on travelling on
-  // its own. At most one move is ever in flight; whatever arrives meanwhile
-  // is added up and sent as a single delta when it returns. Keystrokes still
-  // go through the ordered queue, because for them order is the point.
-  var pendX = 0, pendY = 0, inFlight = false;
-  function flushMove() {
-    if (inFlight || (!pendX && !pendY)) return;
-    var dx = pendX, dy = pendY;
-    pendX = 0; pendY = 0;
-    inFlight = true;
-    fetch("/" + pin, {
-      method: "POST",
-      headers: {"Content-Type": "application/x-www-form-urlencoded"},
-      body: "move=" + dx + "," + dy + "&pin=" + encodeURIComponent(pin)
-    }).catch(function () {}).then(function () {
-      inFlight = false;
-      flushMove();
+  // Coalesce only adjacent, unsent moves in the same input queue as taps
+  // and keys. A separate move queue plus a 60 ms timer raced on slow links.
+  function pushMove(dx, dy) {
+    if (pendingMove) {
+      pendingMove.x += dx; pendingMove.y += dy;
+      return;
+    }
+    var batch = {x: dx, y: dy};
+    pendingMove = batch;
+    queue = queue.then(function () {
+      if (pendingMove === batch) pendingMove = null;
+      return fetch("/" + pin, {
+        method: "POST",
+        headers: {"Content-Type": "application/x-www-form-urlencoded"},
+        body: "move=" + batch.x + "," + batch.y + "&pin=" + encodeURIComponent(pin)
+      }).catch(function () {});
     });
   }
-  function pushMove(dx, dy) { pendX += dx; pendY += dy; flushMove(); }
   function down(e) {
     var p = at(e); px = p.x; py = p.y; moved = 0; tracking = true;
     restX = 0; restY = 0;
@@ -1271,7 +1220,7 @@ window.onerror = function (message) {
     pad.classList.remove("live");
     // Let any outstanding movement land first, so the click happens where
     // the finger finished rather than where it was a moment earlier.
-    if (moved < 8) setTimeout(function () { send("click=1"); }, 60);
+    if (moved < 8) send("click=1");
     e.preventDefault();
   }
   pad.addEventListener("touchstart", down, {passive: false});
@@ -1956,9 +1905,10 @@ class SessionHolder:
     built from it, and neither can be re-issued from here.
     """
 
-    def __init__(self, backend, remote_name, label, timeout):
+    def __init__(self, backend, remote_name, label, timeout, replace=False):
         self.backend = backend
         self.remote_name = remote_name
+        self.replace = replace
         self.name = display_name(backend, label)
         self.timeout = timeout
         self.pin = "%04d" % secrets.randbelow(10000)
@@ -1974,6 +1924,7 @@ class SessionHolder:
 
     def start(self):
         session = Session(self.backend, self.remote_name, self.timeout)
+        session.replace = self.replace
         # When the sign-in finishes on the device, take the page away rather
         # than leaving rclone's own "All done, go back to rclone" sitting
         # there -- a sentence about a program the player has never heard of,
@@ -2405,7 +2356,7 @@ def make_handler(holder, shutdown):
     return Handler
 
 
-def cmd_serve(backend, remote_name, label, port, timeout):
+def cmd_serve(backend, remote_name, label, port, timeout, replace=False):
     if not shutil.which("rclone") and not os.path.exists(RCLONE):
         sys.stderr.write("rclone is not installed\n")
         return 2
@@ -2413,7 +2364,7 @@ def cmd_serve(backend, remote_name, label, port, timeout):
     # Nothing from the last attempt survives into this one -- including a
     # serve still holding the port.
     stop_other_serves()
-    holder = SessionHolder(backend, remote_name, label, timeout)
+    holder = SessionHolder(backend, remote_name, label, timeout, replace)
     # The state is this serve's from here, stamped with its attempt id; every
     # write this serve makes afterwards is conditional on still owning it
     # (write_owned, G-C-02).
@@ -2587,7 +2538,7 @@ def main(argv):
                 port = int(rest[i + 1])
             elif arg == "--timeout" and i + 1 < len(rest):
                 timeout = int(rest[i + 1])
-        return cmd_serve(backend, name, label, port, timeout)
+        return cmd_serve(backend, name, label, port, timeout, "--replace" in rest)
 
     if command == "url":
         print(read_state().get("url", ""))
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_remote b/projects/ROCKNIX/packages/network/rclone/sources/cloud_remote
index a5d26b7699..8a25a78165 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_remote
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_remote
@@ -27,7 +27,10 @@
 #                        can pick an input widget without fetching them.
 #   choices <type> <field> [prov]  TSV: value, label
 #   create <name> <type> [key=value ...]    create, verify, roll back on failure
-#   list                 TSV: name, type
+#   update <name> <type> [key=value ...]  verify and replace saved settings
+#   active               selected name with trailing colon; empty is failure
+#   select/remove <name> change local selection or remove local credentials
+#   list                 STATE line, then TSV: name, type, active/saved, provider
 #
 # Tiers:
 #   keys      no OAuth at all - a form is enough
@@ -40,6 +43,7 @@ import json
 import os
 import subprocess
 import sys
+import cloud_connections as connections
 
 RCLONE = "/usr/bin/rclone"
 LOG_FILE = "/var/log/cloud_sync.log"
@@ -237,131 +241,31 @@ def cmd_choices(backend_type, field, subprovider=""):
     return 1
 
 
-def existing_remotes():
-    """Configured remote names, without the trailing colon -- or None when
-    rclone could not say. A listing that failed used to read as "no remotes",
-    and cmd_create's refusal to touch an existing remote fell open exactly
-    when rclone could not be asked (#308 gpt F-RS-23)."""
-    code, out, _ = rclone("listremotes", check=False)
-    if code != 0:
-        return None
-    return [line.strip().rstrip(":") for line in out.splitlines() if line.strip()]
-
-
 def cmd_list():
-    code, out, _ = rclone("config", "dump", check=False)
-    if code != 0:
-        return 0
+    _, config = connections.read_config()
     try:
-        config = json.loads(out or "{}")
-    except json.JSONDecodeError:
-        return 0
-    for name in sorted(config):
-        print("%s\t%s" % (name, config[name].get("type", "")))
+        selected = connections.active(config)
+    except connections.Refused:
+        selected = ""
+    print("STATE=" + ("active" if selected else "unselected"))
+    for name in sorted(config.sections()):
+        print("%s\t%s\t%s\t%s" % (name, config.get(name, "type", fallback=""),
+                                    "active" if name == selected else "saved", config.get(name, "provider", fallback="")))
     return 0
 
 
-def cmd_create(name, backend_type, settings):
-    """Create a remote from already-answered values, then prove it works.
-
-    Refuses to touch a remote that already exists. A device that is already
-    syncing has a working configuration and possibly cloud data laid out to
-    match it; silently rewriting that is how someone loses access to their
-    own files (see fork issue #51).
-    """
-    existing = existing_remotes()
-    if existing is None:
-        sys.stderr.write("could not read the configured remotes; not creating one\n")
-        return 2
-    if name in existing:
-        sys.stderr.write(
-            "remote '%s' already exists; not modifying it\n" % name)
-        return 1
-
+def cmd_create(name, backend_type, settings, replace=False):
     providers = load_providers()
-    known = {t.get("Name") for t in providers}
-    if backend_type not in known:
-        sys.stderr.write("unknown backend type: %s\n" % backend_type)
-        return 1
-    # The values of this backend's password options, to be taken out of
-    # anything of rclone's this passes on (see below).
-    secret_names = {opt.get("Name") for t in providers if t.get("Name") == backend_type
-                    for opt in (t.get("Options") or []) if opt.get("IsPassword")}
-    secret_values = [value for key, value in settings if key in secret_names and value]
-
-    args = ["config", "create", name, backend_type]
-    for key, value in settings:
-        args.append("%s=%s" % (key, value))
-    # Bucket-based clouds have no directories: a folder is a prefix on
-    # object names, so an empty one does not exist and mkdir makes nothing.
-    # rclone's answer (v1.63+) is a directory marker -- the zero-byte "name/"
-    # object the AWS and MinIO consoles write for "Create folder" -- behind
-    # directory_markers, off by default. On, mkdir and the folder seeding
-    # behave on a bucket as on Dropbox and an empty folder survives; the
-    # restore judges a folder by its parent's listing either way
-    # (D-CLOUD-120, 2026-09-12). Only where rclone documents the option.
-    if backend_type in ("s3", "gcs", "azureblob") and not any(k == "directory_markers" for k, _ in settings):
-        args.append("directory_markers=true")
-    # --non-interactive so rclone reports a question as data instead of
-    # blocking on stdin that no one is attached to. --obscure so passwords
-    # are stored the way rclone expects rather than in the clear.
-    args += ["--non-interactive", "--obscure"]
-
-    log("creating remote %s (type %s) with %d option(s)"
-        % (name, backend_type, len(settings)))
-    code, out, err = rclone(*args)
-    if code != 0:
-        # rclone's reason goes on to the interface, which shows it under THE
-        # CONNECTION COULDN'T BE SAVED so a mistyped key can be fixed -- with
-        # any password value it echoed taken out first (the audit of stream
-        # C, G-C-09: the log was cleaned in PL-074, this channel was not).
-        said = err.strip()
-        for value in secret_values:
-            said = said.replace(value, "<hidden>")
-        sys.stderr.write((said or "rclone config create failed") + "\n")
-        return 2
-
-    # rclone --non-interactive answers with a JSON blob when it still needs
-    # something. Exit 0 there would otherwise look like success while leaving
-    # a half-configured remote behind.
-    question = None
-    try:
-        parsed = json.loads(out or "{}")
-        if isinstance(parsed, dict) and parsed.get("State"):
-            question = parsed.get("Option") or {}
-    except json.JSONDecodeError:
-        pass
-    if question:
-        remove_remote(name)
-        sys.stderr.write(
-            "backend needs more input: %s\n" % (question.get("Name") or "unknown"))
-        return 2
-
-    # Prove it before telling anyone it worked. A remote that lists is a
-    # remote the sync tools can use; an exit code from create only says the
-    # file got written.
-    code, _, err = rclone("lsd", "%s:" % name,
-                          "--contimeout", "10s", "--timeout", "20s",
-                          "--low-level-retries", "1", "--retries", "1",
-                          check=False)
-    if code != 0:
-        log("remote %s failed verification, rolling back" % name)
-        remove_remote(name)
-        sys.stderr.write(
-            "the remote was created but could not be reached; it has been "
-            "removed so nothing half-working is left behind\n")
-        return 3
-
-    log("remote %s created and verified" % name)
+    if backend_type not in {p.get("Name") for p in providers}:
+        raise connections.Refused("Unknown provider.")
+    if not replace and backend_type in ("s3", "gcs", "azureblob") and not any(k == "directory_markers" for k, _ in settings):
+        settings.append(("directory_markers", "true"))
+    log("updating remote " + name if replace else "creating remote " + name)
+    connections.save(name, backend_type, settings, replace=replace)
     print("OK=%s" % name)
     return 0
 
 
-def remove_remote(name):
-    """Undo a failed create. Best effort - never mask the original error."""
-    rclone("config", "delete", name, check=False)
-
-
 def usage():
     sys.stderr.write(
         "usage: cloud_remote providers\n"
@@ -369,6 +273,9 @@ def usage():
         "       cloud_remote fields <type> [subprovider]\n"
         "       cloud_remote choices <type> <field> [subprovider]\n"
         "       cloud_remote create <name> <type> [key=value ...]\n"
+        "       cloud_remote update <name> <type> [key=value ...]\n"
+        "       cloud_remote active\n"
+        "       cloud_remote select|remove <name>\n"
         "       cloud_remote list\n")
     return 1
 
@@ -399,7 +306,19 @@ def main(argv):
     if command == "list":
         return cmd_list()
 
-    if command == "create":
+    if command == "active":
+        name = connections.active()
+        if name:
+            print(name + ":")
+            return 0
+        return 1
+
+    if command in ("select", "remove") and len(argv) == 3:
+        (connections.select if command == "select" else connections.remove)(argv[2])
+        print("OK=" + argv[2])
+        return 0
+
+    if command in ("create", "update"):
         if len(argv) < 4:
             return usage()
         settings = []
@@ -409,10 +328,14 @@ def main(argv):
                 return 1
             key, value = pair.split("=", 1)
             settings.append((key, value))
-        return cmd_create(argv[2], argv[3], settings)
+        return cmd_create(argv[2], argv[3], settings, replace=(command == "update"))
 
     return usage()
 
 
 if __name__ == "__main__":
-    sys.exit(main(sys.argv))
+    try:
+        sys.exit(main(sys.argv))
+    except (connections.Refused, OSError) as exc:
+        sys.stderr.write(str(exc) + "\n" if isinstance(exc, connections.Refused) else "Cloud settings could not be read or saved.\n")
+        sys.exit(2)
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore b/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
index 67ce8b2a25..6f8f99282f 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore
@@ -925,20 +925,11 @@ clean_exit() {
     exit ${exit_code}
 }
 
-# The configured remote, by the same rule as `rclone listremotes | head -1`
-# -- the first section name in sorted order -- read from the config file
-# rather than by starting rclone, which costs close to a second on a
-# handheld. rclone remains the fallback if the file yields nothing. The
-# same function as cloud_backup's (#308 claude F-CS-04).
+# The shared explicit selection, with legacy first-name behavior only when
+# the sidecar is absent. Empty or missing selected names never fall back to
+# another account (D-CLOUD-184). Keep the internal function name for callers.
 first_remote() {
-    local name
-    name=$(grep -o '^\[[^]]*\]' /storage/.config/rclone/rclone.conf 2>/dev/null \
-           | tr -d '[]' | sort | head -1)
-    if [ -n "${name}" ]; then
-        printf '%s:\n' "${name}"
-    else
-        rclone listremotes 2>/dev/null | head -1
-    fi
+    "$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null
 }
 
 # Does the remote compare files by size alone? rclone decides equality by
@@ -1016,7 +1007,7 @@ check_internet() {
     log_message "Checking cloud storage reachability..." "false"
 
     local remote probe_rc=1
-    remote=$(rclone listremotes 2>/dev/null | head -1)
+    remote=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
     if [ -n "${remote}" ]; then
         rclone lsd "${remote}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1; probe_rc=$?
         if [ "${probe_rc}" -eq 0 ]; then
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan b/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
index 85b560e194..4eac16acc6 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan
@@ -136,7 +136,7 @@ prepare() {
         log "scan: no default route; skipped"
         exit "${EXIT_NO_NETWORK}"
     fi
-    REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+    REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
     if [ -z "${REMOTE}" ]; then
         why "YOUR CLOUD STORAGE ISN'T SET UP YET"
         exit 1
diff --git a/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup b/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
index ff72e38bda..75c6c0d64e 100755
--- a/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
+++ b/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup
@@ -548,8 +548,7 @@ syncpath_problem() {
 validation_context() {
     folder_values >/dev/null || return 2
     local remotes config_file config_id
-    remotes=$(timeout 3 rclone listremotes 2>/dev/null) || return 2
-    REMOTE=$(printf '%s\n' "${remotes}" | head -1)
+    REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null) || return 2
     [ -n "${REMOTE}" ] || return 2
     config_file=$(timeout 3 rclone config file 2>/dev/null | tail -1)
     [ -f "${config_file}" ] && [ -r "${config_file}" ] || return 2
@@ -557,6 +556,9 @@ validation_context() {
     config_id=$( set -o pipefail; { printf '%s\0' "${REMOTE}" "${SAVES}" "${BACKUPS}" "${CONTENT}";
         sha256sum "${config_file}" || exit 1
         if [ -f "${SYNC_CONF}" ]; then sha256sum "${SYNC_CONF}" || exit 1; fi
+        if [ -f /storage/.config/rclone/active-connection ]; then
+            sha256sum /storage/.config/rclone/active-connection || exit 1
+        fi
     } | sha256sum) || return 2
     config_id="${config_id%% *}"
     jq -n --arg id "${config_id}" --arg remote "${REMOTE}" \
@@ -592,7 +594,7 @@ case "$1" in
         exec "${tool}" "$2" "$3"
     ;;
     --folder-state)
-        REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+        REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
         [ -n "${REMOTE}" ] || { echo "STATE=no-remote"; exit 1; }
         folder_values || exit $?
         folder_marker_read || exit $?
@@ -641,10 +643,14 @@ case "$1" in
         # into the name the player picked it by. Until this, nothing on any
         # screen said who the cloud was -- the setup page offered to connect
         # one and never mentioned the one already there (fork #110).
-        remote_name="$(rclone listremotes 2>/dev/null | head -1)"
+        remote_name="$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)"
         remote_name="${remote_name%:}"
         echo "REMOTE_NAME=${remote_name}"
-        echo "REMOTE_TYPE=$(rclone config show "${remote_name}" 2>/dev/null | sed -n 's/^[[:space:]]*type[[:space:]]*=[[:space:]]*//p' | head -1)"
+        remote_type=""
+        if [ -n "${remote_name}" ]; then
+            remote_type=$(rclone config show "${remote_name}" 2>/dev/null | sed -n 's/^[[:space:]]*type[[:space:]]*=[[:space:]]*//p' | head -1)
+        fi
+        echo "REMOTE_TYPE=${remote_type}"
         exit 0
     ;;
     --content-location)
@@ -718,7 +724,7 @@ case "$1" in
             # (the audit of the fixes, claude G3-D-07).
             CAND="${CAND%/}"
         fi
-        REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+        REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
         if [ -z "${REMOTE}" ]; then
             echo "No cloud remote configured."
             exit 2
@@ -748,7 +754,7 @@ case "$1" in
         fi
         # Refuse a path this remote cannot use. The literal path checks also
         # hold with no remote; existing independent pointers are preserved.
-        SP_REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+        SP_REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
         if ! syncpath_problem "${NEWPATH}" "${SP_REMOTE}"; then
             exit 1
         fi
@@ -784,7 +790,7 @@ case "$1" in
     ;;
     --seed-folders)
         [ "$#" -eq 2 ] && seed_categories "$2" || { echo "Choose which cloud folders to create."; exit 2; }
-        REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+        REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
         [ -n "${REMOTE}" ] || { echo "ERROR no remote"; exit 2; }
         folder_values || exit $?
         seed_failed=0
@@ -873,7 +879,7 @@ case "$1" in
         # plain-text verdict on stdout, exit 0 = working, 1 = missing,
         # 2 = configured but unreachable.
         REMOTE="$2"
-        [ -z "${REMOTE}" ] && REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+        [ -z "${REMOTE}" ] && REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
         if [ -z "${REMOTE}" ]; then
             echo "NONE"
             log_message "Cloud setup check: no remotes configured"
@@ -937,7 +943,7 @@ echo "Press any button here when you are done (or to cancel)."
 wait_for_button
 
 echo
-REMOTE=$(rclone listremotes 2>/dev/null | head -1)
+REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
 if [ -z "${REMOTE}" ]; then
     echo -e "\e[33mNo cloud remote configured yet.\e[0m"
     echo "Run this again once you have completed 'rclone config'."
diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool b/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
index fd19f0e018..850ed70c68 100755
--- a/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
+++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool
@@ -718,18 +718,21 @@ RATOKENSETTINGS=(
 # back on a restore. Not in the default LOCATIONS; a custom list such as
 # /storage/.config sweeps it in. The toggle itself
 # (global.retroachievements.offlineproxy) is a line in system.cfg and travels.
-RATOKENDIRS=(
+# Connection transactions and interrupted atomic writes can leave private
+# staging files beside rclone.conf. The entire directory stays on this device.
+DEVICEONLYDIRS=(
+    /storage/.config/rclone/
     /storage/.config/raofflineproxy/
 )
 # The same folders as restore patterns, each with its own wildcard. Written
-# inline as "${RATOKENDIRS[@]#/}"'*' the '*' joined the LAST element only, so
+# inline as "${DEVICEONLYDIRS[@]#/}"'*' the '*' joined the LAST element only, so
 # a second folder in the list would have left the first as a bare name --
 # which busybox unzip -x matches against nothing (busybox tar -X happens to
 # take a folder's subtree from its bare name; unzip does not, probed on the
 # image's binary), and that folder's token cache would come back from a zip
 # (#308 claude F-BR-13).
-RATOKENDIR_PATTERNS=()
-for D in "${RATOKENDIRS[@]}"; do RATOKENDIR_PATTERNS+=("${D#/}*"); done
+DEVICEONLYDIR_PATTERNS=()
+for D in "${DEVICEONLYDIRS[@]}"; do DEVICEONLYDIR_PATTERNS+=("${D#/}*"); done
 # This device's cloud sign-in and its name in the cloud: never in an archive,
 # never put back from one, whichever archive it is (#307 PL-010). rclone.conf
 # is live OAuth tokens (#52); cloud_device_id's record is the name this
@@ -742,6 +745,7 @@ for D in "${RATOKENDIRS[@]}"; do RATOKENDIR_PATTERNS+=("${D#/}*"); done
 # rclone.conf over this one's and the restore reported success.
 DEVICEONLY=(
     /storage/.config/rclone/rclone.conf
+    /storage/.config/rclone/active-connection
     /storage/.config/cloud_sync-device-id
     /storage/.config/cloud_sync-device-id.previous
 )
@@ -1064,11 +1068,11 @@ write_archive() {
                 hold_back_line "${CANDIDATE}"
             fi
         done
-        # The proxy's folder, every file under it (#165). grep -F on the
+        # Device-only identity folders, every file under them (#165, #537). grep -F on the
         # prefix: the list holds absolute paths, so the prefix matches a file
         # under that folder and nothing else.
         HELD=0
-        for CANDIDATE in "${RATOKENDIRS[@]}"
+        for CANDIDATE in "${DEVICEONLYDIRS[@]}"
         do
             while IFS= read -r F
             do
@@ -1076,7 +1080,7 @@ write_archive() {
                 HELD=$((HELD + 1))
             done < <(grep -F "${CANDIDATE}" "${FILELIST}" || true)
         done
-        [ "${HELD}" -gt 0 ] && logger -t backuptool "held back ${HELD} file(s) under the offline RetroAchievements proxy's folder: its token cache and award queue never travel (#165)"
+        [ "${HELD}" -gt 0 ] && logger -t backuptool "held back ${HELD} file(s) under device-only identity folders: credentials and award queues never travel (#165, #537)"
         # The copies a writer keeps beside a file that is stripped or held
         # back carry the same keys: chksysconfig's and the interface's
         # last-good record (system.cfg.backup, es_settings.cfg.backup), a
@@ -1535,7 +1539,7 @@ case "${VERB}" in
                     /storage/.config/ppsspp/assets/*|/storage/.config/ppsspp/PSP/SYSTEM/CACHE/*) continue ;;
                 esac
                 for CANDIDATE in "${DEVICEONLY[@]}" "${RATOKENFILES[@]}"; do [ "/storage/.config/${REL}" = "${CANDIDATE}" ] && continue 2; done
-                for CANDIDATE in "${RATOKENDIRS[@]}"; do case "/storage/.config/${REL}" in "${CANDIDATE}"*) continue 2 ;; esac; done
+                for CANDIDATE in "${DEVICEONLYDIRS[@]}"; do case "/storage/.config/${REL}" in "${CANDIDATE}"*) continue 2 ;; esac; done
                 if [ -f "/usr/config/${REL}" ] && [ ! -L "/storage/.config/${REL}" ]
                 then
                     printf '%s\n' "${REL}" 2>/dev/null >> "${SEEDS}" || { SEED_RC=1; break; }
@@ -1641,7 +1645,7 @@ case "${VERB}" in
         # restore's own: its control files, the settings backups folder that
         # holds the copy just taken, and that copy by name (RESTORE_CONTROL;
         # #307, the audit of the fix round, PL-007).
-        SKIPS=('storage/.config/ppsspp/assets/*' 'storage/.config/ppsspp/PSP/SYSTEM/CACHE/*' "${RATOKENFILES[@]#/}" "${RATOKENDIR_PATTERNS[@]}" "${DEVICEONLY[@]#/}" "${SEEDLIST#/}" "${LINKS[@]}")
+        SKIPS=('storage/.config/ppsspp/assets/*' 'storage/.config/ppsspp/PSP/SYSTEM/CACHE/*' "${RATOKENFILES[@]#/}" "${DEVICEONLYDIR_PATTERNS[@]}" "${DEVICEONLY[@]#/}" "${SEEDLIST#/}" "${LINKS[@]}")
         for C in "${RESTORE_CONTROL[@]}"; do SKIPS+=("$(glob_literal "${C#/}")"); done
         SKIPS+=("$(glob_literal "${SETTINGS_BACKUPS#/}")/*")
         [ -n "${SNAPSHOT}" ] && SKIPS+=("$(glob_literal "${SNAPSHOT#/}")")
diff --git a/projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl b/projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl
index 930c8a84e6..33d754de08 100755
--- a/projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl
+++ b/projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl
@@ -41,13 +41,18 @@ ADHOC_CLIENT_ID=$(get_setting wifi.adhoc.id)
 NETPLAY_SSID="NETPLAY_AP"
 WIFI_DEV="$(ls /sys/class/net | grep -m1 ^wlan)"
 
+# Typed security/join callers must not read an unavailable radio as success.
+if [ "${1}" = security ] || [ "${1}" = connect-open ]; then
+  [ -n "${WIFI_DEV}" ] && [ -d "/sys/class/net/${WIFI_DEV}" ] && [ -n "${NMCLI}" ] || exit 2
+fi
+
 # Exit the script if the WiFi device isn't available
 [ -z "${WIFI_DEV}" ] && exit 0
 [ ! -d "/sys/class/net/${WIFI_DEV}" ] && exit 0
 [ -z "${NMCLI}" ] && exit 0
 
 SSID="${2:-$(get_setting wifi.ssid 2>/dev/null)}"
-PSK="${3:-$(get_setting wifi.key 2>/dev/null)}"
+PSK="${3-$(get_setting wifi.key 2>/dev/null)}"
 COUNTRY="${4:-$(get_setting wifi.country | tr -d '[:space:]' 2>/dev/null)}"
 
 if [ "${WIFI_TYPE}" = "1" ]; then
@@ -81,6 +86,46 @@ list_wifi() {
   "${NMCLI}" -t -f SSID dev wifi list ifname "${WIFI_DEV}" 2>/dev/null | nm_unescape | sed '/^$/d' | sort -u
 }
 
+# Only an explicit, unanimous open result may skip the key prompt. SECURITY
+# has no colons; SSIDs do, escaped by nmcli. Unknown/mixed scans fail closed.
+wifi_security() {
+  local wanted="${1}" rows line name security found=0 open=0 protected=0
+  rows=$(LC_ALL=C "${NMCLI}" -t -f SSID,SECURITY device wifi list ifname "${WIFI_DEV}" --rescan no 2>/dev/null) || { echo unknown; return 1; }
+  while IFS= read -r line; do
+    [[ "${line}" == *:* ]] || continue
+    name=$(printf '%s\n' "${line%:*}" | nm_unescape)
+    [ "${name}" = "${wanted}" ] || continue
+    found=1
+    security="${line##*:}"
+    case "${security}" in
+      ''|--) open=1 ;;
+      *WPA*|*WEP*|*802.1X*|*OWE*) protected=1 ;;
+      *) echo unknown; return 1 ;;
+    esac
+  done <<< "${rows}"
+  if [ "${found}" = 0 ] || { [ "${open}" = 1 ] && [ "${protected}" = 1 ]; }; then
+    echo unknown; return 1
+  fi
+  if [ "${open}" = 1 ]; then echo open; else echo protected; fi
+}
+
+# An unsaved open network never borrows wifi.key or deletes a saved profile.
+# Check again at the mutation boundary, including profiles renamed by NM.
+connect_open_wifi() {
+  local name="${1}" rows line profile saved_ssid
+  [ "${WIFI_TYPE}" != 1 ] && [ -n "${name}" ] || return 1
+  [ "$(wifi_security "${name}")" = open ] || return 1
+  rows=$(saved_wifi) || return 1
+  while IFS= read -r line; do
+    [ -n "${line}" ] || continue
+    profile="${line%$'\t'*}"
+    saved_ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${profile}" 2>/dev/null) || return 1
+    [ "${profile}" != "${name}" ] && [ "${saved_ssid}" != "${name}" ] || return 1
+  done <<< "${rows}"
+  wait_for_wifi
+  "${NMCLI}" -w 90 device wifi connect "${name}" ifname "${WIFI_DEV}" >/dev/null 2>&1
+}
+
 connect_wifi() {
   wait_for_wifi
   # Ensure NM has the device ready and has scanned
@@ -425,6 +470,12 @@ case "${1}" in
   pin)
     pin_wifi
     ;;
+  security)
+    wifi_security "${2}"
+    ;;
+  connect-open)
+    connect_open_wifi "${2}"
+    ;;
   connect)
     if [ "${WIFI_TYPE}" = "1" ] && \
        [ "${ADHOC_CLIENT_ID}" = "1" ]; then
diff --git a/tools/cloud-round-trip b/tools/cloud-round-trip
index ddefcd48c9..0be352fdfe 100755
--- a/tools/cloud-round-trip
+++ b/tools/cloud-round-trip
@@ -69,9 +69,9 @@ reads (the three outcome words are asserted by default; --no-vocabulary skips th
 
 Two guards, both load-bearing:
 
-* Every cloud_* script picks its remote with `rclone listremotes | head -1`.
-  If the device has another remote sorting earlier, the tests would sync a
-  real cloud account instead. The remote is asserted, never assumed.
+* Cloud tools use the explicit active connection (legacy images use their
+  first remote). The suite preserves that selection and asserts the QA
+  connection before any transfer; another saved account is never assumed safe.
 * Restore is destructive by design. The suite works in a scratch tree by
   default and only touches /storage/roms with --real-roms, so pointing this
   at a device with real saves cannot quietly delete them.
@@ -288,11 +288,19 @@ class Prepared:
         self.settings = {}
         self.prev_paths = {}
         self.prev_rclone_conf = ""
+        self.prev_active = None
         # A capture-only run (prepare_local) reads no rclone.conf and asks the
         # backend for nothing; restore_device must then put back neither.
         self.local_only = False
 
 
+# Only images predating explicit selection may use the historical fallback.
+ACTIVE_COMMAND = 'if test -f "$(dirname "$(command -v cloud_remote)")/cloud_connections.py"; then cloud_remote active; else rclone listremotes 2>/dev/null | head -1; fi'
+
+def active_remote(dev):
+    return dev.run(ACTIVE_COMMAND).strip()
+
+
 def prepare_device(dev, remote, root, args, prepared, which=""):
     """Point one device at the QA endpoint. It is appended to `prepared` as
     soon as its previous state is captured -- before anything is written --
@@ -311,16 +319,20 @@ def prepare_device(dev, remote, root, args, prepared, which=""):
     # The device's own remote comes back at the end: a device the suite has
     # finished with has the remote it started with (Gate 0, #35).
     p.prev_rclone_conf = dev.run(f"cat {RCLONE_CONF} 2>/dev/null || true")
+    if dev.run(f"test -f {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection && echo present", check=False).strip() == "present":
+        p.prev_active = dev.run(f"cat {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection")
     for key in ("SAVESPATH", "SETTINGS_BACKUPS", "SAVES_REMOTE", "SETTINGS_REMOTE", "CONTENT_REMOTE",
                 "BACKUPPATH", "BACKUPFOLDER", "SYNCPATH", "SYNCPATH_BACKUP", "CONTENTPATH"):
         p.prev_paths[key] = dev.run(f"grep -m1 '^{key}=' {CONF} 2>/dev/null || true").strip()
     prepared.append(p)
     dev.run(f"mkdir -p {os.path.dirname(RCLONE_CONF)}")
     dev.write(RCLONE_CONF, backend("rclone-conf").encode())
-    first = dev.run("rclone listremotes 2>/dev/null | head -1").strip().rstrip(":")
+    dev.write(RCLONE_CONF.rsplit("/", 1)[0] + "/active-connection", (remote + "\n").encode())
+    dev.run(f"chmod 600 {RCLONE_CONF} {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection")
+    first = active_remote(dev).rstrip(":")
     if not check(first == remote,
-                 f"first remote is {remote!r}, which is what the scripts will use",
-                 f"first remote is {first!r}, not {remote!r} - refusing to sync "
+                 f"active remote is {remote!r}, which is what the scripts will use",
+                 f"active remote is {first!r}, not {remote!r} - refusing to sync "
                  f"someone else's account"):
         raise Fail("refusing to sync someone else's account")
 
@@ -946,10 +958,7 @@ def run_steps(dev, root, remote, args, settings, prev_paths):
                           f"the user rule sits above the catch-all in the merged file (lines {' < '.join(order) if order else '?'})",
                           f"rules order was {order}")
     saves_remote = dev.run(f"grep -m1 '^SAVES_REMOTE=' {CONF} | cut -d'\"' -f2").strip()
-    # The scripts fall back to the first configured remote when REMOTENAME is
-    # blank in the conf, and so must this.
-    remote_name = dev.run(f"grep -m1 '^REMOTENAME=' {CONF} | cut -d'\"' -f2").strip() \
-        or dev.run("rclone listremotes 2>/dev/null | head -1").strip()
+    remote_name = active_remote(dev)
     listing = dev.run(f"rclone lsf -R --files-only {shlex.quote(remote_name + saves_remote)} 2>/dev/null || true")
     failures += not check("keep-off-the-cloud.probe" not in listing and "game1.srm" in listing,
                           "the excluded file stayed home while the ordinary save travelled",
@@ -2380,7 +2389,7 @@ def fx_a5(p):
     store = p.saves_remote.rstrip("/") + "-discarded"
     # The reader, on b: the store listed and every record read as one line;
     # nothing local consulted.
-    reader = ("R=$(rclone listremotes 2>/dev/null | head -1); S=" + shlex.quote(store) + "; "
+    reader = ("R=$(" + ACTIVE_COMMAND + "); S=" + shlex.quote(store) + "; "
               "rclone lsf -R --files-only \"${R}${S}\" 2>/dev/null | while IFS= read -r r; do "
               "case \"$r\" in */record.json|record.json) rclone cat \"${R}${S}/${r}\" | jq -c . ;; "
               "*) echo \"MEMBER $r\" ;; esac; done")
@@ -4622,7 +4631,7 @@ class Transport:
             f.write(f"$ {cmd}\n# exit {rc}\n{out}")
 
     def remote(self, dev):
-        return dev.run("rclone listremotes 2>/dev/null | head -1").strip() + self.p.saves_remote
+        return active_remote(dev) + self.p.saves_remote
 
     def clear(self, dev):
         dev.run(f"rm -rf {BISYNC_STATE} {AGREED}", check=False)
@@ -7779,6 +7788,10 @@ def restore_device(p, args, archive):
             dev.write(RCLONE_CONF, prev_rclone_conf.encode())
         else:
             dev.run(f"rm -f {RCLONE_CONF}", check=False)
+        if p.prev_active is None:
+            dev.run(f"rm -f {RCLONE_CONF.rsplit('/', 1)[0]}/active-connection", check=False)
+        else:
+            dev.write(RCLONE_CONF.rsplit("/", 1)[0] + "/active-connection", p.prev_active.encode())
         backend("reset")
         print("    scratch tree and bucket emptied; the device's own remote, paths and "
               "settings-backup setting restored")
diff --git a/tools/cloud-test-backend b/tools/cloud-test-backend
index d3cb756655..ec08e7faac 100755
--- a/tools/cloud-test-backend
+++ b/tools/cloud-test-backend
@@ -65,6 +65,9 @@ case "${BACKEND}" in
   webdav|s3|sftp|smb|ftp) ;;
   *) echo "error: unknown backend '${BACKEND}' (webdav, s3, sftp, smb, ftp)" >&2; exit 2 ;;
 esac
+# Nested helper calls (seed-device, status and endpoint notes) must keep the
+# explicit CLI selection, even when the incoming environment named another.
+export CLOUD_QA_BACKEND="${BACKEND}"
 
 # One port each, so more than one backend can be up at a time: a matrix run
 # that had to take the previous endpoint down between rows would test the
@@ -102,10 +105,9 @@ else
 fi
 CONFDIR="$(dirname "${PIDFILE}")"
 
-# The remote name the device will use. Every cloud_* script selects its
-# remote with `rclone listremotes | head -1` - first alphabetically - so this
-# name decides whether the tests act on the test endpoint or on whatever else
-# the device has configured. The driver asserts it rather than trusting it.
+# The QA connection name. The driver explicitly selects it, verifies the
+# active reader and restores prior selection with credentials after testing.
+# Historical images use their first-remote rule, asserted at the same boundary.
 REMOTE="${CLOUD_QA_REMOTE:-qa-cloud}"
 
 GUEST_HOST="${CLOUD_QA_GUEST_HOST:-10.0.2.2}"
@@ -884,6 +886,8 @@ mkdir -p /storage/.config/rclone
 cat > /storage/.config/rclone/rclone.conf <<'RC'
 $("$0" --backend "${BACKEND}" rclone-conf)
 RC
+printf '%s\n' '${REMOTE}' > /storage/.config/rclone/active-connection
+chmod 600 /storage/.config/rclone/rclone.conf /storage/.config/rclone/active-connection
 /usr/bin/cloud_sync_helper >/dev/null 2>&1
 grep -q '^CONTENT_REMOTE="${cr}"' /storage/.config/cloud_sync.conf || sed -i 's|^CONTENT_REMOTE=.*|CONTENT_REMOTE="${cr}"|' /storage/.config/cloud_sync.conf
 /usr/bin/cloud_setup --check
diff --git a/tools/last-good-scripts-test b/tools/last-good-scripts-test
index 4947e53402..c19e993456 100755
--- a/tools/last-good-scripts-test
+++ b/tools/last-good-scripts-test
@@ -322,6 +322,17 @@ src_of() { # <repo-relative path> <destination>
     else
         cp "${ROOT}/${1}" "${2}" || { echo "cannot read ${1}" >&2; exit 2; }
     fi
+    # Ship the real reader and transaction module beside the script, as the
+    # package does. Historical --old scripts without that dependency stay old.
+    if grep -q 'cloud_connections as connections\|/cloud_remote" active' "${2}"; then
+        local connection_dir
+        connection_dir="$(dirname "$2")"
+        if [[ "${1}" != */cloud_remote ]]; then
+            src_of "${RCLONE_REL}/cloud_remote" "${connection_dir}/cloud_remote"
+            chmod +x "${connection_dir}/cloud_remote"
+        fi
+        src_of "${RCLONE_REL}/cloud_connections.py" "${connection_dir}/cloud_connections.py"
+    fi
     case "${1}" in
         */cloud_setup)
             # Discovery shares the restore scanner's local membership.
@@ -758,13 +769,17 @@ printf '#!/bin/sh\nexit 0\n' > "${B2}/shim/sleep"
 chmod +x "${B2}/shim"/*
 printf 'system.hostname=X\n' > "${ST2}/.config/system/configs/system.cfg"
 printf '[qa]\ntype = dropbox\ntoken = {"access_token":"QA-SECRET-TOKEN","refresh_token":"QA-REFRESH"}\n' > "${ST2}/.config/rclone/rclone.conf"
+mkdir -p "${ST2}/.config/rclone/.connection-qa"
+printf 'token = STAGED-QA-CREDENTIAL\n' > "${ST2}/.config/rclone/.connection-qa/rclone.conf"
+printf 'token = ATOMIC-QA-CREDENTIAL\n' > "${ST2}/.config/rclone/.rclone.conf-qa"
+printf 'qa\n' > "${ST2}/.config/rclone/active-connection"
 echo plain > "${ST2}/.config/test/plain.txt"
 # es_settings.cfg is XML, which the line-anchored leak scan cannot read, so the
 # strip at the archive is its only guard: the ScreenScraper passwords (#64)
 # and the IGDB client secret (#274, found by #221's trace). No harness case
 # read this strip before 2026-09-25.
 printf '<?xml version="1.0"?>\n<config>\n<string name="ScreenScraperUser" value="qa-user" />\n<string name="ScreenScraperPass" value="QA-SECRET-SS" />\n<string name="ScreenScraperDevPass" value="QA-SECRET-DEV" />\n<string name="IGDBClientID" value="qa-client" />\n<string name="IGDBSecret" value="QA-SECRET-IGDB" />\n<string name="ThemeSet" value="art-book-next" />\n</config>\n' > "${ST2}/.config/emulationstation/es_settings.cfg"
-printf 'LOCATIONS=(\n  /storage/.config/system/configs/system.cfg\n  /storage/.config/test/*\n  /storage/.config/rclone/*\n  /storage/.config/emulationstation/*\n)\n' > "${ST2}/.config/backuptool.conf"
+printf 'LOCATIONS=(\n  /storage/.config/system/configs/system.cfg\n  /storage/.config/test/*\n  /storage/.config/rclone/*\n  /storage/.config/rclone/.connection-qa/*\n  /storage/.config/rclone/.rclone.conf-qa\n  /storage/.config/emulationstation/*\n)\n' > "${ST2}/.config/backuptool.conf"
 OUT2="${B2}/out"
 RC2=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
     --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
@@ -775,6 +790,9 @@ RC2=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
 arc=$(ls "${ST2}/roms/backup"/*.tar.gz 2>/dev/null | head -1)
 [ "${RC2}" -eq 0 ] && [ -n "${arc}" ]; check $? "a backup with rclone.conf in LOCATIONS completes (rc ${RC2})" "rc ${RC2}, archive: '${arc}'"
 ! tar -tzf "${arc}" 2>/dev/null | grep -q 'rclone/rclone.conf$'; check $? "rclone.conf is not in the archive" "the archive lists rclone.conf"
+if grep -q '/storage/.config/rclone/' "${BT}"; then
+    ! tar -tzf "${arc}" 2>/dev/null | grep -q 'storage/.config/rclone/'; check $? "connection selection and interrupted private credential staging never travel in a settings backup (#537)" "a device-only connection file entered the archive"
+fi
 ! tar -xzOf "${arc}" 2>/dev/null | grep -q 'QA-SECRET-TOKEN'; check $? "and no token travelled in any member" "a member carries the token"
 tar -tzf "${arc}" 2>/dev/null | grep -q 'test/plain.txt$'; check $? "files that are not held back are archived as before" "plain.txt missing"
 grep -q 'rclone.conf held back' "${OUT2}"; check $? "the log says rclone.conf was held back" "no held-back line: $(grep logger "${OUT2}" | tail -2 | tr '\n' ' ')"
@@ -1020,7 +1038,7 @@ echo "${klist}" | grep -q 'duckstation/settings.ini$' && echo "${klist}" | grep
 ! grep -rqF "${KTOK}" "${KX}" 2>/dev/null; check $? "and the planted token appears in no member of the archive" "the token is in: $(grep -rlF "${KTOK}" "${KX}" 2>/dev/null | sed "s|${KX}/||" | tr '\n' ' ')"
 grep -q 'held back 5 file(s) that hold only a RetroAchievements token' "${OUT}" && grep -q 'blanked the RetroAchievements token in 4 emulator settings file(s)' "${OUT}"; check $? "and the log counts five held back and four blanked" "log: $(grep -oE '(held back|blanked)[^|]*' "${OUT}" | tr '\n' ' ')"
 ! echo "${klist}" | grep -q 'storage/.config/raofflineproxy/'; check $? "the offline RetroAchievements proxy's folder travels in no shape: none of its five files is in the archive (#165)" "the archive carries: $(echo "${klist}" | grep 'raofflineproxy/' | tr '\n' ' ')"
-grep -q "held back 5 file(s) under the offline RetroAchievements proxy's folder" "${OUT}"; check $? "and the log counts the five held back under it" "log: $(grep -o "held back [0-9]* file(s) under the offline[^|]*" "${OUT}" | head -1 | grep . || echo silent)"
+grep -qE "held back 5 file\(s\) under (the offline RetroAchievements proxy's folder|device-only identity folders)" "${OUT}"; check $? "and the log counts the five held back under it" "log: $(grep -o "held back [0-9]* file(s) under the offline[^|]*" "${OUT}" | head -1 | grep . || echo silent)"
 # A Token = line in a file the strip does not know, with a value of its own.
 # Since #307 PL-005 the scanner's hit ends the backup before the archive is
 # named, so it is planted for a second run: that run is refused, the log
@@ -1201,6 +1219,9 @@ grep -q 'absent_not_broken "${ROOT}ROMs/"' "${LL}/src/cloud_content_restore" &&
 # pages, the shape #113 bounded for the syncs (#273's trace of #113).
 LC="${LL}/check"; mkdir -p "${LC}/shim" "${LC}/rec" "${LC}/repo"
 cp "${LL}/src/cloud_setup" "${LC}/repo/cloud_setup"
+mkdir -p "${LC}/storage/.config/rclone"
+printf '[qa]\ntype = local\n' > "${LC}/storage/.config/rclone/rclone.conf"
+if [ -f "${LL}/src/cloud_connections.py" ]; then cp "${LL}/src/cloud_remote" "${LL}/src/cloud_connections.py" "${LC}/repo/"; fi
 printf 'export PATH=/shim:/usr/bin:/bin\n' > "${LC}/profile"
 printf '#!/bin/sh\necho "logger $*" >&2\n' > "${LC}/shim/logger"
 cat > "${LC}/shim/rclone" <<'EOR'
@@ -1215,7 +1236,7 @@ RCC=$( ( setsid -w bwrap --die-with-parent --tmpfs / --ro-bind /usr /usr \
     --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
     --ro-bind /etc /etc --ro-bind "${LC}/profile" /etc/profile \
     --ro-bind "${LC}/shim" /shim --bind "${LC}/rec" /rec --ro-bind "${LC}/repo" /repo \
-    --dev /dev --proc /proc --tmpfs /tmp --tmpfs /storage \
+    --dev /dev --proc /proc --tmpfs /tmp --bind "${LC}/storage" /storage --dir /var/log \
     bash /repo/cloud_setup --check > "${OUTC}" 2>&1; echo $? ) 2>/dev/null )
 [ "${RCC}" -eq 0 ] && grep -q '^OK qa:' "${OUTC}"; check $? "cloud_setup --check verifies the one remote the shim lists (rc ${RCC})" "rc ${RCC}; out: $(head -2 "${OUTC}" | tr '\n' ' ' | cut -c1-120)"
 LSD=$(grep '^lsd ' "${LC}/rec/argv" 2>/dev/null | head -1)
@@ -4544,6 +4565,7 @@ if [ -n "${BB}" ]; then CSBB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST
 # path-based and holds no folder yet (lsd answers "directory not found").
 C1="${CS}/c1"; mkdir -p "${C1}/shim" "${C1}/repo" "${C1}/storage/.config"
 cp "${CS}/src/cloud_setup" "${C1}/repo/cloud_setup"
+if [ -f "${CS}/src/cloud_connections.py" ]; then cp "${CS}/src/cloud_remote" "${CS}/src/cloud_connections.py" "${C1}/repo/"; fi
 if [ "${VALIDATOR_AVAILABLE}" -eq 1 ]; then
     cp "${CS}/src/cloud_folder_validate" "${C1}/repo/cloud_folder_validate"
     chmod +x "${C1}/repo/cloud_folder_validate" "${C1}/repo/cloud_setup"
@@ -4971,6 +4993,8 @@ fi
 # reached. `drive` runs cloud_oauth's own main() with those patches, for the
 # groups that need a serve as a process of its own.
 C3="${CS}/c3"; mkdir -p "${C3}/scratch"; cp "${CS}/src/cloud_oauth" "${C3}/cloud_oauth"; cp "${CS}/src/cloud_remote" "${C3}/cloud_remote"
+if [ -f "${CS}/src/cloud_connections.py" ]; then cp "${CS}/src/cloud_connections.py" "${C3}/"; fi
+cp "${ROOT}/tools/test-fixtures/cloud_connections_fixture.py" "${C3}/"
 cat > "${C3}/cloud_oauth_test.py" <<'EOPY'
 #!/usr/bin/env python3
 # cloud_oauth, graded in-process and as processes, inside a bwrap sandbox with
@@ -5008,11 +5032,15 @@ def load(tag="t"):
     loader = importlib.machinery.SourceFileLoader("cloud_oauth_" + tag, REPO)
     spec = importlib.util.spec_from_loader(loader.name, loader)
     m = importlib.util.module_from_spec(spec)
+    sys.path.insert(0, __import__("os").path.dirname(loader.path))
     loader.exec_module(m)
     d = tempfile.mkdtemp(dir=WORK, prefix=tag + ".")
     m.STATE_DIR = os.path.join(d, "state")
     os.makedirs(m.STATE_DIR)
     m.LOG_FILE = os.path.join(d, "cloud_sync.log")
+    if hasattr(m, "connections"):
+        from cloud_connections_fixture import configure
+        configure(m, d)
     m.UINPUT = "/nonexistent/uinput"
     return m, d
 
@@ -5197,9 +5225,13 @@ def driver():
     loader = importlib.machinery.SourceFileLoader("cloud_oauth", REPO)
     spec = importlib.util.spec_from_loader(loader.name, loader)
     m = importlib.util.module_from_spec(spec)
+    sys.path.insert(0, __import__("os").path.dirname(loader.path))
     loader.exec_module(m)
     m.STATE_DIR = os.path.join(d, "state")
     m.LOG_FILE = os.path.join(d, "cloud_sync.log")
+    if hasattr(m, "connections"):
+        from cloud_connections_fixture import configure
+        configure(m, d)
     m.UINPUT = "/nonexistent/uinput"
     shim = os.path.join(d, "rclone")
     with open(shim, "w") as h:
@@ -5345,9 +5377,13 @@ def load_remote(tag="r"):
     loader = importlib.machinery.SourceFileLoader("cloud_remote_" + tag, path)
     spec = importlib.util.spec_from_loader(loader.name, loader)
     m = importlib.util.module_from_spec(spec)
+    sys.path.insert(0, __import__("os").path.dirname(loader.path))
     loader.exec_module(m)
     d = tempfile.mkdtemp(dir=WORK, prefix=tag + ".")
     m.LOG_FILE = os.path.join(d, "cloud_sync.log")
+    if hasattr(m, "connections"):
+        from cloud_connections_fixture import configure
+        configure(m, d)
     shim = os.path.join(d, "rclone")
     with open(shim, "w") as h:
         h.write('#!/bin/bash\n'
@@ -5780,6 +5816,9 @@ def listremotes_failure_is_not_absence():
     m, d = load("rs23")
     sp = FakeSP([(["listremotes"], lambda a: completed(a, 1, "", "config file unreadable"))])
     m.subprocess = sp
+    if hasattr(m, "connections"):
+        m.connections.CONFIG.write_bytes(b"[broken")
+        m.connections.RCLONE = "/bin/false"
     s = m.Session("dropbox", "qa", 60)
     s.token = '{"access_token":"t"}'
     ok, detail = s._write_config()
@@ -5793,6 +5832,9 @@ def remote_listremotes_failure_is_not_absence():
     """#308 gpt F-RS-23 (the cloud_remote half)."""
     m, d = load_remote("rs23r")
     open(os.path.join(d, "listremotes-fails"), "w").close()
+    if hasattr(m, "connections"):
+        m.connections.CONFIG.write_bytes(b"[broken")
+        m.connections.RCLONE = "/bin/false"
     rc = m.main(["cloud_remote", "create", "saves", "webdav", "url=https://dav.example"])
     argv = open(os.path.join(d, "argv")).read() if os.path.exists(os.path.join(d, "argv")) else ""
     result(rc != 0 and "config create" not in argv,
@@ -5959,8 +6001,8 @@ def remote_create_stderr_holds_no_password():
     with contextlib.redirect_stderr(buf):
         rc = m.main(["cloud_remote", "create", "qa", "webdav", "url=https://dav.example", "pass=SECRETPASS9"])
     said = buf.getvalue()
-    result(rc != 0 and "SECRETPASS9" not in said and "bad option" in said,
-           "a failed create passes rclone's reason on with the password taken out: %r" % said.strip(),
+    result(rc != 0 and "SECRETPASS9" not in said and ("could not be verified" if hasattr(m, "connections") else "bad option") in said,
+           "a failed create reports a useful sanitized reason without the password: %r" % said.strip(),
            "rc %r; cloud_remote said %r -- a password value reaches the interface's dialog (G-C-09 claude)" % (rc, said.strip()))
 EOPY
 # G-C-01 (claude): the serve's side of the phone's Close page -- a guard.
@@ -6082,6 +6124,7 @@ import importlib.machinery, importlib.util, sys
 loader = importlib.machinery.SourceFileLoader("cloud_oauth_page", sys.argv[1])
 spec = importlib.util.spec_from_loader(loader.name, loader)
 m = importlib.util.module_from_spec(spec)
+sys.path.insert(0, __import__("os").path.dirname(loader.path))
 loader.exec_module(m)
 sys.stdout.write(m.REMOTE_PAGE % {"style": m.STYLE, "name": "Dropbox", "pin": "1234"})
 EOPY
@@ -8011,6 +8054,19 @@ echo this-device > "${P7S}/.config/cloud_sync-device-id"
 p7bt backup
 [ "${RC}" -eq 0 ] && ! p7list | grep -q 'cloud_sync-device-id'; check $? "#307 PL-010: and a backup of /storage/.config does not carry the device id" "#307 PL-010: rc ${RC}; archive: $(p7list | grep device-id)"
 
+# #537: neither restore format imports staged credentials or another active selection.
+if grep -q 'DEVICEONLYDIRS=' "${ROOT}/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool"; then
+for p537format in tar zip; do
+    p7reset '  /storage/.config/test/*'
+    mkdir -p "${P7S}/.config/rclone"
+    echo mine > "${P7S}/.config/rclone/active-connection"
+    p537members=("storage/.config/test/f1=RESTORED" "storage/.config/rclone/active-connection=other" "storage/.config/rclone/.connection-qa/rclone.conf=STAGED SECRET" "storage/.config/rclone/.rclone.conf-qa=TEMP SECRET")
+    if [ "${p537format}" = tar ]; then p7tar 2026_01_01-000000-ROCKNIX_SETTINGS.tar.gz "${p537members[@]}"; else p7zip 20260101000000-ROCKNIX_BACKUP.zip "${p537members[@]}"; fi
+    p7bt restore --no-restart
+    [ "${RC}" -eq 0 ] && [ "$(cat "${P7S}/.config/test/f1")" = RESTORED ] && [ "$(cat "${P7S}/.config/rclone/active-connection")" = mine ] && [ ! -e "${P7S}/.config/rclone/.connection-qa" ] && [ ! -e "${P7S}/.config/rclone/.rclone.conf-qa" ]; check $? "#537: ${p537format} restore excludes staged credentials and active selection" "#537: ${p537format} credential directory changed (rc ${RC})"
+done
+fi
+
 # == PL-037: a file left out as the image's own is reset on restore
 p7reset '  /storage/.config/emulationstation/es_settings.cfg
   /storage/.config/test/*'
@@ -11238,6 +11294,7 @@ if [ -n "${BB}" ]; then CFBB=(--ro-bind "${TMP}/bbin" /bbin --ro-bind "${BB_HOST
 # path-based and empty, every call it gets written down.
 CF1="${CF}/1"; mkdir -p "${CF1}/shim" "${CF1}/repo" "${CF1}/storage/.config"
 cp "${CF}/src/cloud_setup" "${CF1}/repo/cloud_setup"
+if [ -f "${CF}/src/cloud_connections.py" ]; then cp "${CF}/src/cloud_remote" "${CF}/src/cloud_connections.py" "${CF1}/repo/"; fi
 if [ "${VALIDATOR_AVAILABLE}" -eq 1 ]; then
     cp "${CF}/src/cloud_folder_validate" "${CF1}/repo/cloud_folder_validate"
     chmod +x "${CF1}/repo/cloud_folder_validate" "${CF1}/repo/cloud_setup"
@@ -11512,6 +11569,8 @@ cf_cap=$(grep -n '/usr/bin/cloud_capture' "${cf_auto}" | head -1 | cut -d: -f1)
 # and network namespaces as C3's groups run (the script's pkill and its
 # binds reach nothing outside it). Each group prints P or F lines.
 CF4="${CF}/4"; mkdir -p "${CF4}/scratch"
+if [ -f "${CF}/src/cloud_connections.py" ]; then cp "${CF}/src/cloud_connections.py" "${CF4}/"; fi
+cp "${ROOT}/tools/test-fixtures/cloud_connections_fixture.py" "${CF4}/"
 [ -e "${CF}/src/cloud_oauth" ] && cp "${CF}/src/cloud_oauth" "${CF4}/cloud_oauth"
 cat > "${CF4}/cf_oauth_test.py" <<'EOPY'
 #!/usr/bin/env python3
@@ -11540,11 +11599,15 @@ def load(tag):
     loader = importlib.machinery.SourceFileLoader("cf_oauth_" + tag, REPO)
     spec = importlib.util.spec_from_loader(loader.name, loader)
     m = importlib.util.module_from_spec(spec)
+    sys.path.insert(0, __import__("os").path.dirname(loader.path))
     loader.exec_module(m)
     d = tempfile.mkdtemp(dir=WORK, prefix=tag + ".")
     m.STATE_DIR = os.path.join(d, "state")
     os.makedirs(m.STATE_DIR)
     m.LOG_FILE = os.path.join(d, "cloud_sync.log")
+    if hasattr(m, "connections"):
+        from cloud_connections_fixture import configure
+        configure(m, d)
     m.UINPUT = "/nonexistent/uinput"
     m.provider_url = lambda local: "https://www.dropbox.com/oauth2/authorize?state=abc"
     m.lan_address = lambda: "127.0.0.1"
@@ -11745,7 +11808,7 @@ def late_success(tag, close):
     time.sleep(0.3)                             # the create is under way
     close(m, holder, s)
     t.join(10)
-    deleted = any(c[1:3] == ["config", "delete"] for c in sp.calls)
+    deleted = (not m.connections.CONFIG.exists()) if hasattr(m, "connections") else any(c[1:3] == ["config", "delete"] for c in sp.calls)
     return m.read_state(), os.path.exists(m.state_path("signed-in")), deleted
 
 
@@ -11903,6 +11966,7 @@ import importlib.machinery, importlib.util, sys
 loader = importlib.machinery.SourceFileLoader("cloud_oauth_page", sys.argv[1])
 spec = importlib.util.spec_from_loader(loader.name, loader)
 m = importlib.util.module_from_spec(spec)
+sys.path.insert(0, __import__("os").path.dirname(loader.path))
 loader.exec_module(m)
 sys.stdout.write(m.REMOTE_PAGE % {"style": m.STYLE, "name": "Dropbox", "pin": "1234"})
 EOPY
@@ -13904,6 +13968,8 @@ echo "  ab. cloud_scan (#350, D-CLOUD-156): the opening scan's three items, the
 # archive listing, ip answering a route unless told not to.
 SC="${TMP}/sc"; mkdir -p "${SC}/shim" "${SC}/rec" "${SC}/repo" "${SC}/storage/.config" "${SC}/storage/.cache"
 src_of "projects/ROCKNIX/packages/network/rclone/sources/cloud_scan" "${SC}/repo/cloud_scan"
+mkdir -p "${SC}/storage/.config/rclone"
+printf '[qa]\ntype = local\n' > "${SC}/storage/.config/rclone/rclone.conf"
 SC_BOUND=0; SC_RUN_SEQ=0; SC_RUN_ID=""
 grep -q -- '--stamp-valid' "${SC}/repo/cloud_scan" && SC_BOUND=1
 printf 'export PATH=/shim:/usr/bin:/bin\n' > "${SC}/profile"
@@ -14006,9 +14072,11 @@ if [ "${SC_BOUND}" -eq 1 ]; then
 else
 [ "${SCRC}" = 69 ] && ! grep -q '>>> unit' "${SC}/out" && [ ! -f "${SCO}/done" ]; check $? "no default route: exit 69, nothing announced, no done stamp (rc ${SCRC})" "$(sc_out)"
 fi
-rm -f "${SC}"/rec/*; touch "${SC}/rec/noremote"; sc_run
+rm -f "${SC}"/rec/*; touch "${SC}/rec/noremote"
+: > "${SC}/storage/.config/rclone/active-connection"
+sc_run
 [ "${SCRC}" = 1 ] && grep -q "^>>> why YOUR CLOUD STORAGE ISN'T SET UP YET" "${SC}/out"; check $? "no remote: exit 1 with its why (rc ${SCRC})" "$(sc_out)"
-rm -f "${SC}"/rec/*; touch "${SC}/rec/scan-fail"; sc_run
+rm -f "${SC}"/rec/* "${SC}/storage/.config/rclone/active-connection"; touch "${SC}/rec/scan-fail"; sc_run
 [ "${SCRC}" = 0 ] && [ -f "${SCO}/done" ]; check $? "a content listing is not the opening scan's to fail: the scan-fail flag leaves the opening scan at 0 (rc ${SCRC})" "$(sc_out)"
 rm -f "${SC}"/rec/*; sc_run --content --with-media
 [ "${SCRC}" = 0 ] && [ "$(grep '^>>> unit' "${SC}/out" | tr '\n' ' ')" = ">>> unit ROMS, BIOS, AND GAME CONTENT|| " ] && grep -q '^>>> doing compare' "${SC}/out" \
@@ -14019,7 +14087,7 @@ if [ "${SC_BOUND}" -eq 1 ]; then
 fi
 rm -f "${SC}"/rec/*; sc_run --content --media-only
 [ "${SCRC}" = 0 ] && grep -q '^>>> unit GAME CONTENT||' "${SC}/out" && grep -qx -- '--scan --media-only' "${SC}/rec/argv"; check $? "--content --media-only is the GAME CONTENT item with --scan --media-only (rc ${SCRC})" "$(sc_out)"
-rm -f "${SC}"/rec/*; touch "${SC}/rec/scan-fail"; sc_run --content
+rm -f "${SC}"/rec/* "${SC}/storage/.config/rclone/active-connection"; touch "${SC}/rec/scan-fail"; sc_run --content
 [ "${SCRC}" = 5 ] && grep -q '^>>> why YOUR CLOUD STOPPED ANSWERING' "${SC}/out" && [ ! -f "${SCO}/content-done" ] && grep -q '^>>> unit ROMS AND BIOS||' "${SC}/out"; check $? "a content listing the cloud refused (5): the ROMS AND BIOS item, the why, no content stamp (rc ${SCRC})" "$(sc_out)"
 if [ "${MIGRATION_AVAILABLE}" -eq 1 ]; then
 rm -f "${SC}"/rec/*; touch "${SC}/rec/superseded"; sc_run
diff --git a/tools/rasteratops-vm-cloud-epic b/tools/rasteratops-vm-cloud-epic
index 360df6ef52..5aa2f36e69 100755
--- a/tools/rasteratops-vm-cloud-epic
+++ b/tools/rasteratops-vm-cloud-epic
@@ -127,7 +127,7 @@ boot_frames() { # <tag> <seconds after the guest is idle>
 G_ 'systemctl stop essway; . /etc/profile >/dev/null 2>&1; set_setting cloudsaves.startup 0; set_setting cloudsaves.gameexit 0; rm -f /storage/.config/.restore-finish-pending /storage/.config/cloud-layout-migration.json; rm -rf /storage/.cache/cloud_sync/scan; find /storage/roms -type f -name "*.srm" -delete' >/dev/null || exit 2
 say "== setup: the QA remote on the guest (the host backend's conf), then the QA cloud holds the fork's earlier layout with files in every folder of ours; the guest points at it"
 "$R/tools/cloud-test-backend" rclone-conf > $P/epic-rclone.conf && scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR $P/epic-rclone.conf root@127.0.0.1:/tmp/rclone.conf; rm -f $P/epic-rclone.conf
-G_ 'mkdir -p /storage/.config/rclone && mv /tmp/rclone.conf /storage/.config/rclone/rclone.conf && chmod 600 /storage/.config/rclone/rclone.conf && /usr/bin/cloud_sync_helper >/dev/null 2>&1; echo "remote: $(rclone listremotes | head -1)"' | tee -a "$LOG"
+G_ 'mkdir -p /storage/.config/rclone && mv /tmp/rclone.conf /storage/.config/rclone/rclone.conf && chmod 600 /storage/.config/rclone/rclone.conf && /usr/bin/cloud_sync_helper >/dev/null 2>&1; if test -f /usr/bin/cloud_connections.py; then name=$(rclone listremotes | head -1); cloud_remote select "${name%:}"; echo "remote: $(cloud_remote active)"; else echo "remote: $(rclone listremotes | head -1)"; fi' | tee -a "$LOG"
 "$R/tools/cloud-test-backend" reset >/dev/null || exit 2; mkdir -p "$DATA/ROCKNIX/Saves/nes" "$DATA/ROCKNIX/Backups" "$DATA/ROCKNIX/Content/ROMs/nes" "$DATA/ROCKNIX/Content/BIOS" "$DATA/ROCKNIX/Saves-replaced/nes"
 head -c 4000 /dev/urandom > "$DATA/ROCKNIX/Saves/nes/Probe.srm"; head -c 3000 /dev/urandom > "$DATA/ROCKNIX/Saves-replaced/nes/Probe.srm.1"
 head -c 9000 /dev/urandom > "$DATA/ROCKNIX/Content/ROMs/nes/Probe.nes"; head -c 500 /dev/urandom > "$DATA/ROCKNIX/Content/BIOS/disksys.rom"
diff --git a/tools/vm-qa b/tools/vm-qa
index 9e49adc738..13e80f1fc9 100755
--- a/tools/vm-qa
+++ b/tools/vm-qa
@@ -300,8 +300,14 @@ case ",$ONLY," in *,exit,*)       run_suite exit       "$OUT/exit.log"       "$R
 # while the same suite had read PASS on the image before, whose fixed-wait
 # walks passed whenever the tool ran (#125). Seed the QA remote when there is
 # none, the way seed-device does, and the folders the transfer page expects.
+ACTIVE_READER='if test -f "$(dirname "$(command -v cloud_remote)")/cloud_connections.py"; then cloud_remote active; else rclone listremotes 2>/dev/null | head -1; fi'
 ensure_remote() {
-  [ -n "$(SSH 'rclone listremotes 2>/dev/null' 2>/dev/null)" ] && return 0
+  [ -n "$(SSH "$ACTIVE_READER" 2>/dev/null)" ] && return 0
+  # A saved account or an explicit no-selection is not a fresh guest.
+  if SSH 'test -s /storage/.config/rclone/rclone.conf || test -e /storage/.config/rclone/active-connection' 2>/dev/null; then
+    echo "vm-qa: choose the QA connection explicitly; saved connection state is present" >&2
+    return 1
+  fi
   local conf; conf=$(mktemp)
   "$ROOT/tools/cloud-test-backend" rclone-conf > "$conf"
   SSH 'mkdir -p /storage/.config/rclone' 2>/dev/null
@@ -317,7 +323,7 @@ shipped_folders_cmd() {
   local saves backups
   saves=$("$ROOT/tools/cloud-test-backend" shipped-default SAVES_REMOTE) || exit 2
   backups=$("$ROOT/tools/cloud-test-backend" shipped-default SETTINGS_REMOTE) || exit 2
-  printf 'r=$(rclone listremotes 2>/dev/null | head -1); rclone mkdir "${r}%s" >/dev/null 2>&1; rclone mkdir "${r}%s" >/dev/null 2>&1' "$saves" "$backups"
+  printf 'r=$(%s); [ -n "$r" ] || exit 1; rclone mkdir "${r}%s" >/dev/null 2>&1; rclone mkdir "${r}%s" >/dev/null 2>&1' "$ACTIVE_READER" "$saves" "$backups"
 }
 # Time to play (#135). --quick is the bounded form -- one repeat of the
 # launch, the exit sync and a game-to-game, no reboot and no host fixtures --
@@ -409,7 +415,7 @@ folder_walk_witness() {
   SSH 'sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf && stat -c "%a %n" /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf' > "$dest/config.txt" || rc=1
   SSH '/usr/bin/cloud_setup --validation-context' > "$dest/paths.json" || rc=1
   SSH "bash -o pipefail -c 'find /storage/roms -type f -print0 | xargs -0 -r sha256sum'" > "$dest/local.unsorted" || rc=1
-  SSH 'r=$(rclone listremotes) || exit; [ "$(printf "%s\n" "$r" | wc -l)" = 1 ] && [ -n "$r" ] || exit 1; timeout 60 rclone hashsum SHA256 --download --retries 1 --contimeout 5s --timeout 10s "$r"' > "$dest/cloud.unsorted" || rc=1
+  SSH "r=\$($ACTIVE_READER); [ -n \"\$r\" ] || exit 1; timeout 60 rclone hashsum SHA256 --download --retries 1 --contimeout 5s --timeout 10s \"\$r\"" > "$dest/cloud.unsorted" || rc=1
   LC_ALL=C sort "$dest/local.unsorted" > "$dest/local.txt" || rc=1
   LC_ALL=C sort "$dest/cloud.unsorted" > "$dest/cloud.txt" || rc=1
   printf '%s\n' "$rc" > "$dest/result"
diff --git a/tools/vm-upgrade-rehearsal b/tools/vm-upgrade-rehearsal
index b9989e92ae..b07d8876d9 100755
--- a/tools/vm-upgrade-rehearsal
+++ b/tools/vm-upgrade-rehearsal
@@ -59,7 +59,11 @@ ssha "cat > /storage/.config/rclone/rclone.conf <<'RC'
 $CONF
 RC
 chmod 600 /storage/.config/rclone/rclone.conf" >>"$LOG" 2>&1
-REM0=$(ssha 'rclone listremotes 2>/dev/null | head -1'); echo "remote: $REM0" >> "$LOG"
+ACTIVE_READER='if test -f "$(dirname "$(command -v cloud_remote)")/cloud_connections.py"; then cloud_remote active; else rclone listremotes 2>/dev/null | head -1; fi'
+QA_REMOTE=$(./tools/cloud-test-backend remote-name)
+ssha "if test -e /storage/.config/rclone/active-connection; then printf '%s\n' '$QA_REMOTE' > /storage/.config/rclone/active-connection; fi" >>"$LOG" 2>&1
+ACTIVE0=$(ssha 'if test -e /storage/.config/rclone/active-connection; then sha256sum /storage/.config/rclone/active-connection; else echo absent; fi')
+REM0=$(ssha "$ACTIVE_READER"); echo "remote: $REM0" >> "$LOG"
 check "guest sees one remote" "$([ -n "$REM0" ] && echo yes)" "yes"
 ssha "rclone mkdir ${REM0}Rehearsal/Saves 2>>/dev/null; cloud_setup --set-saves-remote /Rehearsal/Saves" >>"$LOG" 2>&1
 CONFPATH=$(ssha 'ls /storage/.config/cloud_sync.conf 2>/dev/null || find /storage/.config -maxdepth 2 -name cloud_sync.conf | head -1')
@@ -120,7 +124,8 @@ SUMS1=$(ssha 'cd /storage/roms && sha256sum savestates/nes/Rehearsal.state.auto
 check "saves and save states byte-identical" "$SUMS1" "$SUMS0"
 check "marker file kept" "$(ssha 'cat /storage/.config/rehearsal-marker')" "rehearsal-marker"
 check "setting kept" "$(ssha 'get_setting rehearsal.marker')" "$WANT"
-check "rclone remote kept" "$(ssha 'rclone listremotes 2>/dev/null | head -1')" "$REM0"
+check "active rclone remote kept" "$(ssha "$ACTIVE_READER")" "$REM0"
+check "active selection bytes/presence kept" "$(ssha 'if test -e /storage/.config/rclone/active-connection; then sha256sum /storage/.config/rclone/active-connection; else echo absent; fi')" "$ACTIVE0"
 check "rclone (new) lists the remote" "$(ssha "rclone lsd ${REM0} >/dev/null 2>&1 && echo ok")" "ok"
 check "saves remote kept" "$(ssha "grep -E '^SAVES_REMOTE=' $CONFPATH 2>/dev/null")" "$SR0"
 check "cloud conf gained the new defaults, kept the old values" "$(ssha "grep -cE '^(CONTENT_REMOTE|SAVES_REMOTE)=' $CONFPATH")" "2"



# FILE inputs/emulationstation.diff

diff --git a/es-app/src/ApiSystem.cpp b/es-app/src/ApiSystem.cpp
index 323267a82..9abd29fca 100644
--- a/es-app/src/ApiSystem.cpp
+++ b/es-app/src/ApiSystem.cpp
@@ -637,6 +637,22 @@ bool ApiSystem::enableWifi(std::string ssid, std::string key)
 }
 #endif
 
+// Only the exact positive protocol answer authorizes the open-network path.
+std::string ApiSystem::getWifiSecurity(const std::string& ssid)
+{
+	std::vector<std::string> lines;
+	auto answer = executeScript("timeout 15 wifictl security " + Utils::String::shellQuote(ssid),
+		[&lines](const std::string line) { lines.push_back(line); });
+	if (answer.second == 0 && lines.size() == 1 && (lines[0] == "open" || lines[0] == "protected"))
+		return lines[0];
+	return "unknown";
+}
+
+bool ApiSystem::connectOpenWifi(const std::string& ssid)
+{
+	return executeScript("timeout 120 wifictl connect-open " + Utils::String::shellQuote(ssid));
+}
+
 bool ApiSystem::disableWifi() 
 {
 	return executeScript("timeout 30 wifictl disable");
@@ -664,8 +680,15 @@ bool ApiSystem::getCurrentWifiSsid(std::string& ssid)
 bool ApiSystem::getSavedWifiNetworks(std::vector<WifiText::SavedNetwork>& networks)
 {
 	std::vector<std::string> lines;
-	auto result = executeScript("timeout 15 wifictl saved", [&lines](const std::string line) { lines.push_back(line); });
-	networks = WifiText::parseSaved(lines);
+	auto result = executeScript("timeout 15 wifictl saved --ssid", [&lines](const std::string line) { lines.push_back(line); });
+	networks.clear();
+	for (const auto& line : lines)
+	{
+		if (line.empty()) continue;
+		WifiText::SavedNetwork network;
+		if (!WifiText::parseSavedDetailsLine(line, network)) { networks.clear(); return false; }
+		networks.push_back(network);
+	}
 	if (result.second != 0)
 	{
 		networks.clear();
diff --git a/es-app/src/ApiSystem.h b/es-app/src/ApiSystem.h
index d1833bb9c..9881e7bea 100644
--- a/es-app/src/ApiSystem.h
+++ b/es-app/src/ApiSystem.h
@@ -251,6 +251,8 @@ public:
 	bool enableWifi(std::string ssid, std::string key);
 #endif
     bool disableWifi();
+	std::string getWifiSecurity(const std::string& ssid);
+	bool connectOpenWifi(const std::string& ssid);
 
 	// The network the device is joined to now, from NetworkManager (wifictl
 	// current) -- not wifi.ssid, which is the one configured last and, once
diff --git a/es-app/src/WifiText.cpp b/es-app/src/WifiText.cpp
index db5d061be..0f83797f2 100644
--- a/es-app/src/WifiText.cpp
+++ b/es-app/src/WifiText.cpp
@@ -31,6 +31,55 @@ bool WifiText::parseSavedLine(const std::string& rawLine, SavedNetwork& network)
 	return true;
 }
 
+static std::string savedField(const std::string& field)
+{
+	std::string result;
+	for (size_t i = 0; i < field.size(); ++i)
+		if (field[i] == '\\' && i + 1 < field.size() && (field[i + 1] == '\\' || field[i + 1] == 't'))
+			result += field[++i] == 't' ? '\t' : '\\';
+		else result += field[i];
+	return result;
+}
+
+bool WifiText::parseSavedDetailsLine(const std::string& rawLine, SavedNetwork& network)
+{
+	const std::string line = withoutCR(rawLine);
+	const size_t first = line.find('\t'), last = line.rfind('\t');
+	if (first == std::string::npos || first == last || line.find('\t', first + 1) != last)
+		return false;
+	const auto flag = line.substr(last + 1);
+	if (flag != "active" && flag != "saved") return false;
+	network.name = savedField(line.substr(0, first));
+	network.ssid = savedField(line.substr(first + 1, last - first - 1));
+	network.inUse = flag == "active";
+	return !network.name.empty() && !network.ssid.empty();
+}
+
+std::vector<WifiText::SavedNetwork> WifiText::profilesForSsid(const std::string& ssid, const std::vector<SavedNetwork>& saved)
+{
+	std::vector<SavedNetwork> result;
+	for (const auto& profile : saved)
+		if ((profile.ssid.empty() ? profile.name : profile.ssid) == ssid)
+			result.push_back(profile);
+	return result;
+}
+
+std::string WifiText::preferredProfile(const std::string& ssid, const std::vector<SavedNetwork>& saved)
+{
+	const auto matching = profilesForSsid(ssid, saved);
+	if (matching.size() == 1) return matching.front().name;
+	int active = 0;
+	std::string name, namesake;
+	for (const auto& profile : matching)
+	{
+		if (profile.name == ssid) namesake = profile.name;
+		if (profile.inUse) { ++active; name = profile.name; }
+		if (profile.inUse && profile.name == ssid) return profile.name;
+	}
+	if (active == 1) return name;
+	return active == 0 ? namesake : "";
+}
+
 std::vector<WifiText::SavedNetwork> WifiText::parseSaved(const std::vector<std::string>& lines)
 {
 	std::vector<SavedNetwork> networks;
@@ -64,17 +113,15 @@ std::vector<WifiText::PickerRow> WifiText::pickerRows(const std::vector<std::str
 		for (const auto& network : saved)
 			if (network.inUse)
 			{
-				joinedNow = network.name;
+				joinedNow = network.ssid.empty() ? network.name : network.ssid;
 				break;
 			}
 
-	auto isSaved = [&saved](const std::string& name)
-	{
-		for (const auto& network : saved)
-			if (network.name == name)
-				return true;
+	const bool detailed = [&saved] {
+		for (const auto& profile : saved) if (!profile.ssid.empty()) return true;
 		return false;
-	};
+	}();
+	auto isSaved = [&saved](const std::string& name) { return !profilesForSsid(name, saved).empty(); };
 
 	std::vector<PickerRow> rows;
 	auto listed = [&rows](const std::string& name)
@@ -102,7 +149,7 @@ std::vector<WifiText::PickerRow> WifiText::pickerRows(const std::vector<std::str
 	// profile known not to be this connection -- and the row joins by its
 	// name, as before.
 	std::string joinedProfile;
-	if (!joinedNow.empty() && savedKnown)
+	if (!joinedNow.empty() && savedKnown && !detailed)
 	{
 		int up = 0;
 		bool namedUp = false;
@@ -123,6 +170,8 @@ std::vector<WifiText::PickerRow> WifiText::pickerRows(const std::vector<std::str
 			joinedProfile = joinedNow;
 	}
 
+	if (detailed && savedKnown) joinedProfile = preferredProfile(joinedNow, saved);
+
 	if (!joinedNow.empty())
 	{
 		PickerRow row{ joinedNow, !joinedProfile.empty(), true, savedKnown };
@@ -137,7 +186,7 @@ std::vector<WifiText::PickerRow> WifiText::pickerRows(const std::vector<std::str
 			continue;
 		PickerRow row{ name, savedKnown && isSaved(name), false, savedKnown };
 		if (row.saved)
-			row.profile = name;
+			row.profile = preferredProfile(name, saved);
 		rows.push_back(row);
 	}
 	return rows;
@@ -186,7 +235,7 @@ WifiText::PressAction WifiText::manualAction(const std::string& name, const std:
 	if (!name.empty() && name == current)
 		return PressAction::Join;
 	for (const auto& network : saved)
-		if (network.name == name)
+		if ((network.ssid.empty() ? network.name : network.ssid) == name)
 			return PressAction::Join;
 	if (!savedKnown)
 		return PressAction::CheckAgain;
diff --git a/es-app/src/WifiText.h b/es-app/src/WifiText.h
index b7f5bb0ae..330382168 100644
--- a/es-app/src/WifiText.h
+++ b/es-app/src/WifiText.h
@@ -25,6 +25,7 @@ namespace WifiText
 	{
 		std::string name;
 		bool inUse = false;
+		std::string ssid; // optional for legacy two-column readers
 	};
 
 	// One line of `wifictl saved`. False for a line that is not a network:
@@ -34,6 +35,11 @@ namespace WifiText
 	// the flag is read after the last tab, so a tab inside a name still
 	// leaves the flag whole.
 	bool parseSavedLine(const std::string& line, SavedNetwork& network);
+	// Current wifictl saved --ssid: escaped profile, escaped SSID, state.
+	bool parseSavedDetailsLine(const std::string& line, SavedNetwork& network);
+	std::vector<SavedNetwork> profilesForSsid(const std::string& ssid, const std::vector<SavedNetwork>& saved);
+	std::string preferredProfile(const std::string& ssid, const std::vector<SavedNetwork>& saved);
+
 
 	// Every network in the lines, in the order given (nmcli puts the one in
 	// use first); lines that are not networks are passed over.
diff --git a/es-app/src/guis/GuiMenu.cpp b/es-app/src/guis/GuiMenu.cpp
index 8dd10b122..622d60ee4 100644
--- a/es-app/src/guis/GuiMenu.cpp
+++ b/es-app/src/guis/GuiMenu.cpp
@@ -5569,10 +5569,40 @@ static void cloudAddTransferRow(GuiSettings* s, Window* window, bool configured,
 // meant knowing which half of the split you wanted before you could start.
 // Direction first, then what moves -- the split the system actually keeps is
 // the one the player is shown.
+// A connection can change on a child page. Refresh its parent on return,
+// after the input callback has unwound; never rebuild a live button bar.
+class CloudConnectionsPage : public GuiSettings
+{
+public:
+	CloudConnectionsPage(Window* window, const std::string& title, const std::function<void()>& refresh)
+		: GuiSettings(window, title), mRefresh(refresh), mAlive(std::make_shared<bool>(true)),
+		  mSnapshot(Utils::Platform::GetShOutput("/usr/bin/cloud_remote list")) { }
+	~CloudConnectionsPage() override { *mAlive = false; }
+	void topWindow(bool isTop) override
+	{
+		GuiSettings::topWindow(isTop);
+		if (!isTop) return;
+		auto alive = mAlive;
+		mWindow->postToUiThread([this, alive]
+		{
+			if (!*alive || mWindow->peekGui() != this) return;
+			const auto current = Utils::Platform::GetShOutput("/usr/bin/cloud_remote list");
+			if (current == mSnapshot) return;
+			mSnapshot = current;
+			mRefresh();
+			close();
+		});
+	}
+private:
+	std::function<void()> mRefresh;
+	std::shared_ptr<bool> mAlive;
+	std::string mSnapshot;
+};
+
 void GuiMenu::openCloud(Window* window, bool onFolderRow)
 {
 	const bool configured = Utils::FileSystem::exists("/storage/.config/rclone/rclone.conf", false);
-	auto s = new GuiSettings(window, _("CLOUD"));
+	auto s = new CloudConnectionsPage(window, _("CLOUD"), [window] { GuiMenu::openCloud(window); });
 
 	// The three rows follow the current transfer's outcome (D-UI-070; the
 	// page is sat in since D-UI-078): see cloudAddTransferRow and the
@@ -5673,7 +5703,7 @@ void GuiMenu::openCloud(Window* window, bool onFolderRow)
 							text = _("NO CLOUD STORAGE IS SET UP ON THIS DEVICE YET.");
 						else
 							text = _("COULDN'T REACH") + " " + who + ".\n\n"
-								+ _("CHECK WI-FI, THEN TRY AGAIN. IF IT KEEPS FAILING, SIGN IN AGAIN UNDER CONNECT OR REPAIR CLOUD STORAGE.");
+								+ _("CHECK WI-FI, THEN TRY AGAIN. IF IT KEEPS FAILING, SIGN IN AGAIN UNDER CLOUD CONNECTIONS.");
 						window->pushGui(new GuiMsgBox(window, text, _("OK")));
 					}));
 			}, "", false, true);
@@ -5689,10 +5719,9 @@ void GuiMenu::openCloud(Window* window, bool onFolderRow)
 		s->addWithDescription(_("CHECK CLOUD FOLDERS"), _("CHECK THE FOLDERS YOU CHOOSE."), nullptr,
 			[window] { cloudSetupShowDoneStep(window, "", nullptr); }, "", false, true);
 	}
-	s->addWithDescription(_("CONNECT OR REPAIR CLOUD STORAGE"),
-		configured ? _("CHANGE THE FOLDER, ADD A PROVIDER, OR RENEW A SIGN-IN.")
-		           : _("SET UP A PROVIDER WITH RCLONE, FROM THE HANDHELD. NO COMPUTER NEEDED."),
-		nullptr, [window] { GuiMenu::openCloudAddRemote(window); }, "", false, true);
+	s->addWithDescription(_("CLOUD CONNECTIONS"),
+		_("ADD, CHOOSE, OR MANAGE YOUR CONNECTIONS."),
+		nullptr, [window] { GuiMenu::openCloudConnections(window); }, "", false, true);
 
 	// Only while there is a restore to finish.
 	// Read uncached: exists() remembers its answer for the session, and this
@@ -7014,6 +7043,15 @@ static void cloudShowFolderSelection(Window* window, GuiSettings* prev, const st
 }
 static void cloudSetupShowDoneStep(Window* window, const std::string& remote, GuiSettings* prev)
 {
+	const auto active = Utils::String::trim(Utils::Platform::GetShOutput("/usr/bin/cloud_remote active"));
+	if (!remote.empty() && remote + (remote.back() == ':' ? "" : ":") != active)
+	{
+		auto s = new GuiSettings(window, _("CONNECTION SAVED"));
+		cloudSetupAddProse(s, window, remote,
+			_("YOUR CURRENT CONNECTION HAS NOT CHANGED. CHOOSE THIS CONNECTION UNDER CLOUD CONNECTIONS WHEN YOU WANT TO USE IT."));
+		cloudSetupPresent(window, s, prev);
+		return;
+	}
 	cloudShowFolderSelection(window, prev, {"saves", "settings"});
 }
 
@@ -7041,6 +7079,7 @@ struct CloudBackend
 	std::string name;         // rclone's backend id, e.g. "sftp"
 	std::string label;        // human name, e.g. "SSH/SFTP Connection"
 	std::string subprovider;  // vendor within the backend, where it has one
+	bool reauthorize = false;
 };
 
 struct CloudBackendField
@@ -7083,6 +7122,23 @@ static std::vector<std::string> cloudRemoteLines(const std::string& args)
 	return lines;
 }
 
+static std::string cloudConnectionError(const std::string& output)
+{
+	if (output.find("A cloud operation is running.") != std::string::npos)
+		return _("A CLOUD OPERATION IS RUNNING. WAIT FOR IT TO FINISH, THEN TRY AGAIN.");
+	if (output.find("Turn off both automatic") != std::string::npos)
+		return _("TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS UNDER MANAGE CLOUD STORAGE BEFORE CHANGING THIS CONNECTION.");
+	if (output.find("different connection name") != std::string::npos)
+		return _("CHOOSE A DIFFERENT CONNECTION NAME.");
+	if (output.find("Another connection uses") != std::string::npos)
+		return _("ANOTHER CONNECTION USES THIS ONE. CHANGE THAT CONNECTION FIRST.");
+	if (output.find("additional setup") != std::string::npos)
+		return _("THIS PROVIDER NEEDS ADDITIONAL SETUP. USE A COMPUTER TO FINISH CONNECTING IT.");
+	if (output.find("could not be verified") != std::string::npos || output.find("stopped answering") != std::string::npos)
+		return _("THE CONNECTION DIDN'T ANSWER. CHECK ITS DETAILS AND YOUR NETWORK, THEN TRY AGAIN. YOUR SETTINGS HAVE NOT CHANGED.");
+	return _("YOUR CLOUD SETTINGS COULD NOT BE READ OR SAVED. TRY AGAIN.");
+}
+
 // Split a TSV record, keeping empty fields. removeEmptyEntries would drop
 // them, and most rows have an empty column somewhere -- a backend option with
 // no default, or no help text -- which shifts every later field left and
@@ -7179,7 +7235,13 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 		(*values)["__name__"] = backend.name;
 
 	s->addGroup(_("NAME"));
-	s->addInputTextRow(_("CONNECTION NAME"), (*values)["__name__"], false,
+	if (values->count("__edit__"))
+	{
+		cloudSetupAddFact(s, window, _("CONNECTION NAME"), (*values)["__name__"]);
+		cloudSetupAddProse(s, window, _("EDIT CONNECTION"),
+			_("BLANK FIELDS KEEP THEIR CURRENT VALUES."));
+	}
+	else s->addInputTextRow(_("CONNECTION NAME"), (*values)["__name__"], false,
 		cloudRemoteEditor(values, "__name__"),
 		[values](const std::string& newVal) { (*values)["__name__"] = newVal; });
 
@@ -7205,7 +7267,7 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 			// only rule that never leaves a key on screen. Opening the row
 			// still shows the value, which is the reveal.
 			bool mask = f.password || f.sensitive;
-			if (!values->count(f.name) && !f.deflt.empty())
+			if (!values->count("__edit__") && !values->count(f.name) && !f.deflt.empty())
 				(*values)[f.name] = f.deflt;
 			std::string current = values->count(f.name) ? (*values)[f.name] : "";
 			// The rclone name is the key the value is stored under; the row
@@ -7215,7 +7277,7 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 			// Match the widget to the option. Everything was a text box before,
 			// which meant typing "true" for a switch, and guessing that the
 			// answer for a generic WebDAV server is the literal string "other".
-			if (f.type == "bool")
+			if (f.type == "bool" && !values->count("__edit__"))
 			{
 				auto sw = std::make_shared<SwitchComponent>(window);
 				sw->setState(current == "true");
@@ -7230,7 +7292,7 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 			// Only offer a list when it is short enough to scroll on a handheld.
 			// s3's endpoint carries 351 suggestions and its region 150; those are
 			// effectively free-form and stay as text.
-			if (f.choices > 0 && f.choices <= 12)
+			if (f.choices > 0 && f.choices <= 12 && !values->count("__edit__"))
 			{
 				std::string choicesArgs = "choices " + cloudShellQuote(backend.name)
 					+ " " + cloudShellQuote(fieldName);
@@ -7290,7 +7352,7 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 	}
 
 	s->addGroup(_("FINISH"));
-	s->addEntry(_("CONNECT"), true, [window, backend, values, s]
+	s->addEntry(values->count("__edit__") ? _("SAVE CONNECTION") : _("CONNECT"), true, [window, backend, values, s]
 	{
 		std::string name = Utils::String::trim((*values)["__name__"]);
 		if (name.empty())
@@ -7300,33 +7362,34 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 			return;
 		}
 
-		std::string cmd = "create " + cloudShellQuote(name) + " "
+		std::string cmd = std::string(values->count("__edit__") ? "update " : "create ") + cloudShellQuote(name) + " "
 			+ cloudShellQuote(backend.name);
 		// The sub-provider is a real config value, not just a filter.
 		if (!backend.subprovider.empty())
 			cmd += " " + cloudShellQuote("provider=" + backend.subprovider);
 		for (auto& kv : *values)
 		{
-			if (kv.first == "__name__" || Utils::String::trim(kv.second).empty())
+			if (Utils::String::startsWith(kv.first, "__") || Utils::String::trim(kv.second).empty())
 				continue;
 			cmd += " " + cloudShellQuote(kv.first + "=" + kv.second);
 		}
 
 		window->pushGui(new GuiMsgBox(window,
-			_("CONNECT TO THIS PROVIDER NOW?\n\nTHE CONNECTION IS ONLY SAVED IF IT ANSWERS."),
-			_("YES"), [window, cmd, s]
+			values->count("__edit__")
+				? _("UPDATE THIS CONNECTION AND KEEP YOUR SELECTED FOLDERS?\n\nYOUR CURRENT SETTINGS ARE KEPT UNTIL THE NEW ONES WORK.")
+				: _("CONNECT TO THIS PROVIDER NOW?\n\nTHE CONNECTION IS ONLY SAVED IF IT ANSWERS."),
+			values->count("__edit__") ? _("UPDATE CONNECTION") : _("CONNECT"), [window, cmd, s]
 			{
-				// cloud_remote verifies the remote -- an rclone listing it
-				// bounds at 10 s to connect and 20 s to answer -- and removes
-				// it again if it cannot be reached, so a failure here leaves
-				// nothing behind. Behind GuiLoading, because that round trip
+				// cloud_remote verifies private staged settings before publication;
+				// failure keeps the existing connection. Its two subprocesses
+				// are each bounded to 40 seconds, below this outer deadline. Behind GuiLoading, because that round trip
 				// ran in this callback on the interface thread (fork #103);
 				// the outer box is for an rclone that outlives its own flags.
 				window->pushGui(new GuiLoading<std::string>(window, _("CONNECTING..."),
 					[cmd](IGuiLoadingHandler*)
 					{
 						std::string out = Utils::Platform::GetShOutput(
-							"timeout 60 /usr/bin/cloud_remote " + cmd + " 2>&1");
+							"timeout 100 /usr/bin/cloud_remote " + cmd + " 2>&1");
 						// Masked: the command carries the form's pass=, key= and
 						// token= values, and a script that echoes its arguments
 						// in a usage or an error would put them in es_log.txt
@@ -7349,7 +7412,7 @@ static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
 						// "it failed".
 						window->pushGui(new GuiMsgBox(window,
 							_("THE CONNECTION COULDN'T BE SAVED.") + std::string("\n\n") +
-								Utils::String::trim(out),
+								cloudConnectionError(out),
 							_("OK"), nullptr));
 					}));
 			},
@@ -7421,7 +7484,7 @@ static void cloudOAuthPresentChoice(Window* window, const CloudBackend& backend,
 	const std::string& remoteName, GuiSettings* prev,
 	const CloudOAuthReady& ready);
 static void cloudOAuthShowConnected(Window* window, const CloudBackend& backend,
-	GuiSettings* prev);
+	const std::string& remoteName, GuiSettings* prev);
 static void cloudOAuthChooseInput(Window* window, const CloudBackend& backend,
 	const std::string& remoteName, GuiSettings* prev);
 
@@ -7447,6 +7510,7 @@ static void cloudOAuthStart(Window* window, const CloudBackend& backend,
 		"/usr/bin/cloud_oauth serve " + cloudShellQuote(backend.name)
 		+ " --name " + cloudShellQuote(remoteName)
 		+ " --label " + cloudShellQuote(backend.label)
+		+ (backend.reauthorize ? " --replace" : "")
 		+ " --timeout 900 >/dev/null 2>&1") + " </dev/null >/dev/null 2>&1 &";
 	Utils::Platform::runSystemCommand(cmd, "", nullptr);
 
@@ -7707,15 +7771,15 @@ static void cloudOAuthShowSignIn(Window* window, const CloudBackend& backend,
 
 		if (status == "signed-in")
 		{
-			cloudOAuthShowConnected(window, backend, s);
+			cloudOAuthShowConnected(window, backend, remoteName, s);
 			return;
 		}
 		if (status == "failed")
 		{
 			window->pushGui(new GuiMsgBox(window,
-				_("THE SIGN-IN DID NOT COMPLETE.\n\nCODES ARE SINGLE-USE AND EXPIRE QUICKLY - START AGAIN TO GET A NEW ONE."),
-				_("OK"), nullptr,
-				_("EXIT"), [s] { s->close(); }));
+				_("THE SIGN-IN DID NOT COMPLETE. TRY AGAIN TO START A NEW SIGN-IN."),
+				_("TRY AGAIN"), [window, backend, remoteName, s] { cloudOAuthStart(window, backend, remoteName, s); },
+				_("CANCEL SIGN-IN"), [s] { s->close(); }));
 			return;
 		}
 		window->pushGui(new GuiMsgBox(window,
@@ -7746,54 +7810,46 @@ static void cloudOAuthShowSignIn(Window* window, const CloudBackend& backend,
 // the player could go and do. Somebody who has just finished a sign-in on a
 // handheld deserves to be told what they now have.
 static void cloudOAuthShowConnected(Window* window, const CloudBackend& backend,
-	GuiSettings* prev)
+	const std::string& remoteName, GuiSettings* prev)
 {
-	auto s = new GuiSettings(window, _("CONNECTED"));
-	s->setSubTitle(CloudText::providerSubtitle(backend.name, backend.label));
-
-	cloudSetupAddProse(s, window,
-		Utils::String::format(_("%s IS CONNECTED").c_str(),
-		                      Utils::String::toUpper(backend.label).c_str()),
-		_("YOUR GAME SAVES, SAVE STATES, AND SCREENSHOTS CAN NOW BE KEPT IN THE CLOUD AND PICKED UP ON ANOTHER DEVICE."));
-
-	// A named menu rather than a vague "it is all available now" -- and one
-	// name, because there is one page. This said two, which was accurate when
-	// cloud was split across two menus and became a way to send somebody to
-	// the wrong half of a page that no longer exists.
-	//
-	// The rows are numbered and named exactly as that page names them, under
-	// an "in" line, so the list reads as what you can do once you are there
-	// rather than as three unrelated facts (maintainer, 2026-09-06).
-	s->addGroup(_("WHAT YOU CAN DO NOW"));
-	cloudSetupAddInfoRow(s, window, _("IN GAME SETTINGS:"), true);
-	cloudSetupAddInfoRow(s, window, "1.  " + _("SYNC SAVES WITH THE CLOUD"));
-	cloudSetupAddInfoRow(s, window, "2.  " + _("BACK UP SAVES TO THE CLOUD, OR RESTORE THEM"));
-	cloudSetupAddInfoRow(s, window, "3.  " + _("MANAGE CLOUD STORAGE"));
-
-	// Which is true of this device: what syncs on its own is two switches
-	// under MANAGE CLOUD STORAGE (SYNC SAVES DURING STARTUP, WHEN EXITING A
-	// GAME), not systems, and a device whose settings were restored may have
-	// them on already -- its next exit syncs to the cloud just connected. The
-	// page said NOTHING SYNCS YET whatever the switches said, told the player
-	// to turn on systems, and said ROMs and BIOS are never included, which
-	// the ROMS AND BIOS tier has not been true of since D-UI-022 (#308 8a gpt
-	// F-ES-19).
-	const bool syncsOnItsOwn = SystemConf::getInstance()->get("cloudsaves.startup") == "1"
-		|| SystemConf::getInstance()->get("cloudsaves.gameexit") == "1";
-	if (syncsOnItsOwn)
-		cloudSetupAddProse(s, window, _("YOUR SAVES ALREADY SYNC"),
-			_("THIS DEVICE WAS SET TO SYNC THEM, SO FROM NOW ON THEY GO TO THIS CLOUD."));
-	else
-		cloudSetupAddProse(s, window, _("NOTHING SYNCS YET"),
-			_("CONNECTING ONLY GIVES THIS DEVICE SOMEWHERE TO PUT THINGS. TO SYNC SAVES ON THEIR OWN, TURN IT ON UNDER MANAGE CLOUD STORAGE."));
+	cloudSetupShowDoneStep(window, remoteName, prev);
+}
 
-	// Continue to folder setup using the same selected paths as normal transfers.
-	s->getMenu().clearButtons();
-	s->getMenu().addButton(_("CONTINUE"), _("continue"), [window, s, backend]
+// Adding and renewing are distinct before a sign-in begins. A new name is
+// editable and never overwrites an existing connection at the backend.
+static void cloudOAuthAdd(Window* window, const CloudBackend& backend, GuiSettings* prev)
+{
+	auto s = new GuiSettings(window, _("ADD CONNECTION"));
+	auto name = std::make_shared<std::string>(backend.name);
+	std::set<std::string> existing;
+	for (const auto& line : cloudRemoteLines("list"))
 	{
-		cloudSetupShowDoneStep(window, backend.name, s);
+		auto cols = Utils::String::splitAny(line, "\t", false);
+		if (cols.size() >= 2) existing.insert(cols[0]);
+	}
+	for (int suffix = 2; existing.count(*name); ++suffix)
+		*name = backend.name + std::to_string(suffix);
+	s->addInputTextRow(_("CONNECTION NAME"), *name, false,
+		[name](Window* w, std::string title, std::string /*initial*/,
+			const std::function<void(std::string)>& save)
+		{
+			if (Settings::getInstance()->getBool("UseOSK"))
+				w->pushGui(new GuiTextEditPopupKeyboard(w, title, *name, save, false));
+			else
+				w->pushGui(new GuiTextEditPopup(w, title, *name, save, false));
+		},
+		[name](const std::string& value) { *name = Utils::String::trim(value); });
+	cloudSetupAddProse(s, window, _("ADD A SEPARATE CONNECTION"),
+		_("THIS KEEPS YOUR EXISTING CONNECTIONS. TO RENEW A SIGN-IN, CHOOSE THAT CONNECTION UNDER CLOUD CONNECTIONS."));
+	s->addEntry(_("SIGN IN"), true, [window, backend, name, existing, s]
+	{
+		if (name->empty() || existing.count(*name))
+		{
+			window->pushGui(new GuiMsgBox(window, _("CHOOSE A DIFFERENT CONNECTION NAME."), _("OK")));
+			return;
+		}
+		cloudOAuthStart(window, backend, *name, s);
 	});
-
 	cloudSetupPresent(window, s, prev);
 }
 
@@ -7838,7 +7894,7 @@ static void cloudRemoteShowList(Window* window, const std::string& title,
 			// says what kind of sign-in it is and nothing about where.
 			s->addWithDescription(Utils::String::toUpper(b.label),
 				_("OPENS THE PROVIDER'S SIGN-IN PAGE."), nullptr,
-				[window, backend, s] { cloudOAuthStart(window, backend, backend.name, s); },
+				[window, backend, s] { cloudOAuthAdd(window, backend, s); },
 				"", false, true);
 		}
 		else
@@ -7856,6 +7912,110 @@ static void cloudRemoteShowList(Window* window, const std::string& title,
 	cloudSetupPresent(window, s, nullptr);
 }
 
+static bool cloudConnectionManual(Window* window)
+{
+	if (SystemConf::getInstance()->get("cloudsaves.startup") != "1" &&
+		SystemConf::getInstance()->get("cloudsaves.gameexit") != "1") return true;
+	window->pushGui(new GuiMsgBox(window,
+		_("TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS UNDER MANAGE CLOUD STORAGE BEFORE CHANGING THIS CONNECTION."), _("OK")));
+	return false;
+}
+
+static void cloudConnectionChange(Window* window, const std::string& command, GuiSettings* page)
+{
+	window->pushGui(new GuiLoading<std::string>(window, _("SAVING CONNECTION"),
+		[command](IGuiLoadingHandler*) { return Utils::Platform::GetShOutput("timeout 60 /usr/bin/cloud_remote " + command + " 2>&1"); },
+		[window, page](const std::string& result)
+		{
+			if (!Utils::String::startsWith(result, "OK="))
+			{
+				window->pushGui(new GuiMsgBox(window,
+					_("THE CONNECTION COULDN'T BE CHANGED.") + std::string("\n\n") + cloudConnectionError(result), _("OK")));
+				return;
+			}
+			page->close();
+		}));
+}
+
+static void cloudConnectionDetails(Window* window, const std::string& name, const std::string& type, const std::string& subprovider)
+{
+	auto s = new GuiSettings(window, _("CLOUD CONNECTION"));
+	cloudSetupAddFact(s, window, _("CONNECTION NAME"), name);
+	cloudSetupAddFact(s, window, _("PROVIDER"), CloudText::providerLabel(type));
+	s->addEntry(_("CHECK CONNECTION"), true, [window, name]
+	{
+		cloudSetupRunCheck(window, name + ":", [window](int rc, const std::string&)
+		{
+			window->pushGui(new GuiMsgBox(window, rc == 0 ? _("THE CONNECTION ANSWERED.") : _("COULDN'T REACH THIS CONNECTION. CHECK WI-FI OR SIGN IN AGAIN."), _("OK")));
+		});
+	});
+	s->addEntry(_("USE THIS CONNECTION"), true, [window, name, s]
+	{
+		if (!cloudConnectionManual(window)) return;
+		window->pushGui(new GuiMsgBox(window,
+			_("USE THIS CONNECTION FOR CLOUD TOOLS? YOUR SELECTED FOLDER PATHS WILL STAY THE SAME. CHECK THEM BEFORE YOUR NEXT BACKUP OR RESTORE."),
+			_("USE CONNECTION"), [window, name, s] { cloudConnectionChange(window, "select " + cloudShellQuote(name), s); }, _("CANCEL"), nullptr));
+	});
+	for (auto backend : cloudRemoteBackends())
+	{
+		if (backend.name != type) continue;
+		backend.subprovider = subprovider;
+		if (backend.tier == "oauth")
+		{
+			backend.reauthorize = true;
+			s->addEntry(_("SIGN IN AGAIN"), true, [window, backend, name, s]
+			{
+				if (!cloudConnectionManual(window)) return;
+				window->pushGui(new GuiMsgBox(window,
+					_("SIGN IN TO THE SAME CLOUD ACCOUNT AGAIN. YOUR CURRENT SIGN-IN IS KEPT UNTIL THE NEW ONE WORKS. YOUR SELECTED FOLDERS WILL STAY THE SAME."),
+					_("SIGN IN"), [window, backend, name, s] { cloudOAuthStart(window, backend, name, s); }, _("CANCEL"), nullptr));
+			});
+		}
+		else
+			s->addEntry(_("EDIT CONNECTION"), true, [window, backend, name, s]
+			{
+				if (!cloudConnectionManual(window)) return;
+				auto values = std::make_shared<std::map<std::string, std::string>>();
+				(*values)["__name__"] = name;
+				(*values)["__edit__"] = "1";
+				cloudRemoteShowForm(window, backend, values, s);
+			});
+		break;
+	}
+	s->addEntry(_("REMOVE CONNECTION"), true, [window, name, s]
+	{
+		if (!cloudConnectionManual(window)) return;
+		window->pushGui(new GuiMsgBox(window,
+			_("REMOVE THIS CONNECTION FROM THIS DEVICE? YOUR CLOUD FILES STAY WHERE THEY ARE. IF THIS IS YOUR ACTIVE CONNECTION, CHOOSE ANOTHER BEFORE USING CLOUD TOOLS."),
+			_("REMOVE CONNECTION"), [window, name, s] { cloudConnectionChange(window, "remove " + cloudShellQuote(name), s); }, _("CANCEL"), nullptr));
+	});
+	cloudSetupPresent(window, s, nullptr);
+}
+
+void GuiMenu::openCloudConnections(Window* window)
+{
+	auto s = new CloudConnectionsPage(window, _("CLOUD CONNECTIONS"), [window] { GuiMenu::openCloudConnections(window); });
+	const auto rows = cloudRemoteLines("list");
+	const bool readable = !rows.empty() && Utils::String::startsWith(rows.front(), "STATE=");
+	if (!readable)
+		cloudSetupAddProse(s, window, _("CONNECTIONS UNAVAILABLE"), _("YOUR CLOUD CONNECTIONS COULDN'T BE READ. TRY AGAIN."));
+	else if (rows.front() != "STATE=active")
+		cloudSetupAddProse(s, window, _("NO CONNECTION IN USE"), _("CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS."));
+	for (const auto& line : rows)
+	{
+		auto cols = Utils::String::splitAny(line, "\t", false);
+		if (cols.size() < 3) continue;
+		const auto name = cols[0], type = cols[1];
+		const std::string subprovider = cols.size() > 3 ? cols[3] : "";
+		const auto detail = CloudText::providerLabel(type) + (cols[2] == "active" ? " - " + _("IN USE") : "");
+		s->addWithDescription(name, detail, nullptr,
+			[window, name, type, subprovider] { cloudConnectionDetails(window, name, type, subprovider); }, "", false, true);
+	}
+	if (readable) s->addEntry(_("ADD CONNECTION"), true, [window] { GuiMenu::openCloudAddRemote(window); });
+	s->addEntry(_("USE A COMPUTER INSTEAD"), true, [window] { GuiMenu::openCloudSetup(window); });
+	cloudSetupPresent(window, s, nullptr);
+}
+
 void GuiMenu::openCloudAddRemote(Window* window)
 {
 	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
@@ -7888,7 +8048,7 @@ void GuiMenu::openCloudAddRemote(Window* window)
 			s->addEntry(_(want.second.c_str()), true, [window, backend, s]
 			{
 				if (backend.tier == "oauth")
-					cloudOAuthStart(window, backend, backend.name, s);
+					cloudOAuthAdd(window, backend, s);
 				else
 					cloudRemoteChooseBackend(window, backend);
 			});
diff --git a/es-app/src/guis/GuiMenu.h b/es-app/src/guis/GuiMenu.h
index d3c97ae9d..557cc76db 100644
--- a/es-app/src/guis/GuiMenu.h
+++ b/es-app/src/guis/GuiMenu.h
@@ -47,6 +47,7 @@ public:
 	// found the configured folder missing beside one with a near name (#127).
 	static void openCloudFolderEditor(Window* window, const std::string& current);
         static void openCloudAddRemote(Window* window);
+	static void openCloudConnections(Window* window);
         // MANAGE NETWORKS: the networks NetworkManager remembers, the one in
         // use marked, A to forget one (fork #191). Fetches the list behind a
         // spinner, then pushes the page.
diff --git a/es-app/src/guis/GuiWifi.cpp b/es-app/src/guis/GuiWifi.cpp
index 9c53623c1..819eec475 100644
--- a/es-app/src/guis/GuiWifi.cpp
+++ b/es-app/src/guis/GuiWifi.cpp
@@ -1,6 +1,7 @@
 #include "guis/GuiWifi.h"
 #include "guis/GuiMenu.h"
 #include "guis/GuiMsgBox.h"
+#include "guis/GuiSettings.h"
 #include "guis/GuiTextEditPopup.h"
 #include "guis/GuiTextEditPopupKeyboard.h"
 #include "components/TextComponent.h"
@@ -94,16 +95,41 @@ void GuiWifi::addRow(const WifiText::PickerRow& network)
 // NetworkManager holds -- it answers at once, or comes back if it had
 // dropped (#308 F-WF-05: this used to close on the list's snapshot); a
 // saved one is offered CONNECT / FORGET / CANCEL (#318, D-UI-118); any
-// other is asked for its key; one whose profile could not be asked about
+// unsaved open network connects without a key; protected or unknown ones ask
+// for their key. One whose profile could not be asked about
 // is asked about again first (F-WF-03/06). WifiText::pressAction decides.
 void GuiWifi::onSelect(const WifiText::PickerRow& row)
 {
 	if (mWaitingLoad)
 		return;
 
+	if (row.savedKnown && WifiText::profilesForSsid(row.name, mSaved).size() > 1 && row.profile.empty())
+	{
+		chooseProfile(row.name);
+		return;
+	}
 	act(WifiText::pressAction(row), row.name, WifiText::joinName(row));
 }
 
+// Several profiles can name one SSID. The player chooses a profile before
+// CONNECT or FORGET; neither operation guesses which stored key they meant.
+void GuiWifi::chooseProfile(const std::string& name)
+{
+	auto page = new GuiSettings(mWindow, _("SAVED NETWORKS"));
+	for (const auto& profile : WifiText::profilesForSsid(name, mSaved))
+		page->addEntry(profile.name, true, [this, name, profile, page]
+		{
+			// Closing page destroys this row's callback and its captures.
+			// Keep the values on the stack before opening the next dialog.
+			GuiWifi* picker = this;
+			const std::string networkName = name;
+			const std::string profileName = profile.name;
+			page->close();
+			picker->act(WifiText::PressAction::ChooseSaved, networkName, profileName);
+		});
+	mWindow->pushGui(page);
+}
+
 // A join goes by the profile's name, which need not be the SSID the row
 // shows (#308 claude F-WF-12, gpt F-WF-03): the connected row joined by its
 // SSID, which is no profile's name for a renamed one, and the player read
@@ -136,7 +162,7 @@ void GuiWifi::act(WifiText::PressAction action, const std::string& name, const s
 		break;
 	}
 	case WifiText::PressAction::AskKey:
-		askKeyAndConnect(name);
+		checkSecurityAndConnect(name);
 		break;
 	case WifiText::PressAction::CheckAgain:
 		// Never taken for a network with no profile: the key path rebuilds a
@@ -159,8 +185,14 @@ void GuiWifi::onManualInput()
 	{
 		if (name.empty())
 			return;
+		const auto profile = WifiText::preferredProfile(name, mSaved);
+		if (mSavedKnown && WifiText::profilesForSsid(name, mSaved).size() > 1 && profile.empty())
+		{
+			chooseProfile(name);
+			return;
+		}
 		act(WifiText::manualAction(name, mCurrent, mSaved, mSavedKnown), name,
-			WifiText::manualJoinName(name, mCurrent, mCurrentProfile));
+			profile.empty() ? WifiText::manualJoinName(name, mCurrent, mCurrentProfile) : profile);
 	};
 
 	if (Settings::getInstance()->getBool("UseOSK"))
@@ -214,6 +246,21 @@ void GuiWifi::join(const std::string& name, const std::string& profile)
 // next time. On success the settings take the network and its key, as they
 // did when the row edited them: the network configured last, for the paths
 // that connect from the settings.
+void GuiWifi::checkSecurityAndConnect(const std::string& name)
+{
+	mWaitingLoad = true;
+	mWindow->pushGui(new GuiLoading<std::string>(mWindow, _("CHECKING WI-FI NETWORK"),
+		[name](IGuiLoadingHandler*) { return ApiSystem::getInstance()->getWifiSecurity(name); },
+		[this, name](const std::string& security)
+		{
+			mWaitingLoad = false;
+			if (security == "open")
+				connect(name, "", true);
+			else
+				askKeyAndConnect(name);
+		}));
+}
+
 void GuiWifi::askKeyAndConnect(const std::string& name)
 {
 	auto onKey = [this, name](const std::string& key) { connect(name, key); };
@@ -224,26 +271,26 @@ void GuiWifi::askKeyAndConnect(const std::string& name)
 		mWindow->pushGui(new GuiTextEditPopup(mWindow, _("WI-FI KEY"), "", onKey, false));
 }
 
-void GuiWifi::connect(const std::string& name, const std::string& key)
+void GuiWifi::connect(const std::string& name, const std::string& key, bool openNetwork)
 {
 	Window* window = mWindow;
 	mWaitingLoad = true;
 	LOG(LogInfo) << "wifi picker: connecting to " << name;
 #if !WIN32
 	const std::string country = SystemConf::getInstance()->get("wifi.country");
-	auto apply = [name, key, country](IGuiLoadingHandler*) { return ApiSystem::getInstance()->enableWifi(name, key, country); };
+	auto apply = [name, key, country, openNetwork](IGuiLoadingHandler*) { return openNetwork ? ApiSystem::getInstance()->connectOpenWifi(name) : ApiSystem::getInstance()->enableWifi(name, key, country); };
 #else
-	auto apply = [name, key](IGuiLoadingHandler*) { return ApiSystem::getInstance()->enableWifi(name, key); };
+	auto apply = [name, key, openNetwork](IGuiLoadingHandler*) { return openNetwork ? ApiSystem::getInstance()->connectOpenWifi(name) : ApiSystem::getInstance()->enableWifi(name, key); };
 #endif
 	window->pushGui(new GuiLoading<bool>(window, _("CONNECTING TO WI-FI"), apply,
-		[this, window, name, key](bool ok)
+		[this, window, name, key, openNetwork](bool ok)
 		{
 			mWaitingLoad = false;
 			if (!ok)
 			{
 				LOG(LogWarning) << "wifi picker: could not connect to " << name;
 				window->pushGui(new GuiMsgBox(window,
-					Utils::String::format(_("COULDN'T CONNECT TO %s.").c_str(), name.c_str()) + "\n\n" + _("CHECK THE KEY AND TRY AGAIN."), _("OK")));
+					Utils::String::format(_("COULDN'T CONNECT TO %s.").c_str(), name.c_str()) + "\n\n" + (openNetwork ? _("REFRESH THE NETWORK LIST AND TRY AGAIN.") : _("CHECK THE KEY AND TRY AGAIN.")), _("OK")));
 				return;
 			}
 			SystemConf::getInstance()->set("wifi.ssid", name);
diff --git a/es-app/src/guis/GuiWifi.h b/es-app/src/guis/GuiWifi.h
index a92ed57c8..867c22438 100644
--- a/es-app/src/guis/GuiWifi.h
+++ b/es-app/src/guis/GuiWifi.h
@@ -44,14 +44,16 @@ private:
 	void load(const std::vector<WifiText::PickerRow>& rows);
 	void addRow(const WifiText::PickerRow& row);
 	void onSelect(const WifiText::PickerRow& row);
+	void chooseProfile(const std::string& name);
 	// name is the network as the player sees it; joinAs the name `wifictl
 	// join` takes (WifiText::joinName, manualJoinName).
 	void act(WifiText::PressAction action, const std::string& name, const std::string& joinAs);
 	void onManualInput();
 	void onRefresh(bool rescan = true);
 	void join(const std::string& name, const std::string& profile);
+	void checkSecurityAndConnect(const std::string& name);
 	void askKeyAndConnect(const std::string& name);
-	void connect(const std::string& name, const std::string& key);
+	void connect(const std::string& name, const std::string& key, bool openNetwork = false);
 	void joined(const std::string& name);
 
 	MenuComponent mMenu;
diff --git a/es-app/tests/unit/WifiTextTests.cpp b/es-app/tests/unit/WifiTextTests.cpp
index 622ba1518..919a4bdb9 100644
--- a/es-app/tests/unit/WifiTextTests.cpp
+++ b/es-app/tests/unit/WifiTextTests.cpp
@@ -320,3 +320,33 @@ TEST_CASE("a join's answer is not a truth value (#308 F-WF-03/06; audit G-E2-01)
 	CHECK_FALSE(JoinAnswer().joined());
 	CHECK(joinFailure(JoinAnswer{ 2 }.code) == JoinFailure::ServiceNotAnswering);
 }
+
+TEST_CASE("saved SSIDs preserve renamed profiles and escaped fields (#535)")
+{
+	SavedNetwork profile;
+	REQUIRE(parseSavedDetailsLine("Remembered\tCafe\\tGuest\\\\room\tsaved", profile));
+	CHECK(profile.name == "Remembered");
+	CHECK(profile.ssid == "Cafe\tGuest\\room");
+	CHECK_FALSE(parseSavedDetailsLine("Name\tactive", profile));
+	CHECK_FALSE(parseSavedDetailsLine("Name\tSSID\tother", profile));
+	CHECK_FALSE(parseSavedDetailsLine("Name\t\tsaved", profile));
+	std::vector<SavedNetwork> saved = { { "Remembered", false, "Cafe" } };
+	auto rows = pickerRows({"Cafe", "Open"}, saved, "");
+	REQUIRE(rows.size() == 2);
+	CHECK(rows[0].saved);
+	CHECK(joinName(rows[0]) == "Remembered");
+	CHECK(pressAction(rows[0]) == PressAction::ChooseSaved);
+	CHECK_FALSE(rows[1].saved);
+	CHECK(manualAction("Cafe", "", saved, true) == PressAction::Join);
+	CHECK(preferredProfile("Cafe", saved) == "Remembered");
+	// An active profile on another radio/network cannot claim this row.
+	saved.push_back({ "Other", true, "Office" });
+	rows = pickerRows({"Cafe"}, saved, "Cafe");
+	CHECK(rows[0].profile == "Remembered");
+	saved.push_back({ "Another", false, "Cafe" });
+	CHECK(profilesForSsid("Cafe", saved).size() == 2);
+	CHECK(preferredProfile("Cafe", saved).empty());
+	rows = pickerRows({"Cafe"}, saved, "");
+	CHECK(rows[0].saved);
+	CHECK(rows[0].profile.empty()); // requires the explicit profile chooser
+}
diff --git a/es-core/src/guis/GuiTextEditPopup.cpp b/es-core/src/guis/GuiTextEditPopup.cpp
index 4e7109b27..da31c2648 100644
--- a/es-core/src/guis/GuiTextEditPopup.cpp
+++ b/es-core/src/guis/GuiTextEditPopup.cpp
@@ -31,7 +31,7 @@ GuiTextEditPopup::GuiTextEditPopup(Window* window, const std::string& title, con
 
 	std::vector< std::shared_ptr<ButtonComponent> > buttons;
 	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, acceptBtnText, acceptBtnText, [this, okCallback] { okCallback(mText->getValue()); delete this; }));
-	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("RESET"), _("RESET"), [this, okCallback] { okCallback(""); delete this; }));
+	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CLEAR"), _("CLEAR"), [this, okCallback] { okCallback(""); delete this; }));
 	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CANCEL"), _("DISCARD CHANGES"), [this] { delete this; })); 
 
 	mButtonGrid = makeButtonGrid(mWindow, buttons);
diff --git a/es-core/src/guis/GuiTextEditPopupKeyboard.cpp b/es-core/src/guis/GuiTextEditPopupKeyboard.cpp
index 5f7555d29..2bb2384bf 100644
--- a/es-core/src/guis/GuiTextEditPopupKeyboard.cpp
+++ b/es-core/src/guis/GuiTextEditPopupKeyboard.cpp
@@ -36,10 +36,10 @@ std::vector<std::vector<const char*>> kbUs {
 	{ "€", "", "", "", "", "", "", "", "", "", "", "ALT", "-colspan-" },
 	{ "€", "", "", "", "", "", "", "", "", "", "", "ALT", "-colspan-" },
 
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" }
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
 };
 
 std::vector<std::vector<const char*>> kbFr {
@@ -63,10 +63,10 @@ std::vector<std::vector<const char*>> kbFr {
 	{ "€", "[", "]", "{", "}", "", "", "", "", "", "", "ALT", "-colspan-" },
 	{ "€", "[", "]", "{", "}", "", "", "", "", "", "", "ALT", "-colspan-" },
 
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" }
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
 };
 
 std::vector<std::vector<const char*>> kbKr{
@@ -90,10 +90,10 @@ std::vector<std::vector<const char*>> kbKr{
 	{ "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "`", "ALT", "-colspan-" },
 	{ "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "~", "ALT", "-colspan-" },
 
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" },
-	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "RESET", "-colspan-", "CANCEL", "-colspan-" }
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
+	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
 };
 
 GuiTextEditPopupKeyboard::GuiTextEditPopupKeyboard(Window* window, const std::string& title, const std::string& initValue,
@@ -451,7 +451,7 @@ std::vector<HelpPrompt> GuiTextEditPopupKeyboard::getHelpPrompts()
 	std::vector<HelpPrompt> prompts = mGrid.getHelpPrompts();
 
 	if (mOkCallback != nullptr)
-		prompts.push_back(HelpPrompt("x", _("RESET")));
+		prompts.push_back(HelpPrompt("x", _("CLEAR")));
 
 	prompts.push_back(HelpPrompt("y", _("SHIFT")));
 	prompts.push_back(HelpPrompt("start", _("OK")));
@@ -488,7 +488,7 @@ std::shared_ptr<ButtonComponent> GuiTextEditPopupKeyboard::makeButton(const std:
 			mText->startEditing(); mText->textInput(" "); mText->stopEditing();
 			return;
 		}
-		else if (key == _("RESET"))
+		else if (key == _("CLEAR"))
 		{
 			mOkCallback(""); 
 			delete this;
diff --git a/locale/lang/fr/LC_MESSAGES/emulationstation2.po b/locale/lang/fr/LC_MESSAGES/emulationstation2.po
index f6adeac4d..d13f85dbd 100644
--- a/locale/lang/fr/LC_MESSAGES/emulationstation2.po
+++ b/locale/lang/fr/LC_MESSAGES/emulationstation2.po
@@ -6758,3 +6758,168 @@ msgstr "VOS PARAMÈTRES CLOUD N’ONT PAS PU ÊTRE ENREGISTRÉS. RÉESSAYEZ."
 #. cloud folder path refusal (#524 PL-003)
 msgid "CHECK THE PATH AND YOUR CONNECTION, THEN TRY AGAIN."
 msgstr "VÉRIFIEZ LE CHEMIN ET LA CONNEXION, PUIS RÉESSAYEZ."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CHECKING WI-FI NETWORK"
+msgstr "VÉRIFICATION DU RÉSEAU WI-FI"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "REFRESH THE NETWORK LIST AND TRY AGAIN."
+msgstr "ACTUALISEZ LA LISTE DES RÉSEAUX ET RÉESSAYEZ."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CLOUD CONNECTIONS"
+msgstr "CONNEXIONS AU CLOUD"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "ADD, CHOOSE, OR MANAGE YOUR CONNECTIONS."
+msgstr "AJOUTEZ, CHOISISSEZ OU GÉREZ VOS CONNEXIONS."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CHECK WI-FI, THEN TRY AGAIN. IF IT KEEPS FAILING, SIGN IN AGAIN UNDER CLOUD CONNECTIONS."
+msgstr "VÉRIFIEZ LE WI-FI, PUIS RÉESSAYEZ. SI LE PROBLÈME PERSISTE, RECONNECTEZ-VOUS DANS CONNEXIONS AU CLOUD."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CONNECTION SAVED"
+msgstr "CONNEXION ENREGISTRÉE"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "YOUR CURRENT CONNECTION HAS NOT CHANGED. CHOOSE THIS CONNECTION UNDER CLOUD CONNECTIONS WHEN YOU WANT TO USE IT."
+msgstr "VOTRE CONNEXION ACTUELLE N’A PAS CHANGÉ. CHOISISSEZ CETTE CONNEXION DANS CONNEXIONS AU CLOUD LORSQUE VOUS VOULEZ L’UTILISER."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "EDIT CONNECTION"
+msgstr "MODIFIER LA CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "BLANK FIELDS KEEP THEIR CURRENT VALUES."
+msgstr "LES CHAMPS VIDES GARDENT LEURS VALEURS ACTUELLES."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "THE SIGN-IN DID NOT COMPLETE. TRY AGAIN TO START A NEW SIGN-IN."
+msgstr "LA CONNEXION N’A PAS ABOUTI. RÉESSAYEZ POUR DÉMARRER UNE NOUVELLE CONNEXION."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "ADD CONNECTION"
+msgstr "AJOUTER UNE CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "ADD A SEPARATE CONNECTION"
+msgstr "AJOUTER UNE AUTRE CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "THIS KEEPS YOUR EXISTING CONNECTIONS. TO RENEW A SIGN-IN, CHOOSE THAT CONNECTION UNDER CLOUD CONNECTIONS."
+msgstr "VOS CONNEXIONS EXISTANTES SONT CONSERVÉES. POUR VOUS RECONNECTER, CHOISISSEZ LA CONNEXION DANS CONNEXIONS AU CLOUD."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CHOOSE A DIFFERENT CONNECTION NAME."
+msgstr "CHOISISSEZ UN AUTRE NOM DE CONNEXION."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "SIGN IN"
+msgstr "SE CONNECTER"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS UNDER MANAGE CLOUD STORAGE BEFORE CHANGING THIS CONNECTION."
+msgstr "DÉSACTIVEZ LES DEUX OPTIONS DE SYNCHRONISATION AUTOMATIQUE DANS GÉRER LE STOCKAGE CLOUD AVANT DE MODIFIER CETTE CONNEXION."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "SAVING CONNECTION"
+msgstr "ENREGISTREMENT DE LA CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "THE CONNECTION COULDN'T BE CHANGED."
+msgstr "LA CONNEXION N’A PAS PU ÊTRE MODIFIÉE."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CLOUD CONNECTION"
+msgstr "CONNEXION AU CLOUD"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "PROVIDER"
+msgstr "FOURNISSEUR"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "THE CONNECTION ANSWERED."
+msgstr "LA CONNEXION A RÉPONDU."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "COULDN'T REACH THIS CONNECTION. CHECK WI-FI OR SIGN IN AGAIN."
+msgstr "CETTE CONNEXION N’A PAS RÉPONDU. VÉRIFIEZ LE WI-FI OU RECONNECTEZ-VOUS."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "USE THIS CONNECTION"
+msgstr "UTILISER CETTE CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "USE THIS CONNECTION FOR CLOUD TOOLS? YOUR SELECTED FOLDER PATHS WILL STAY THE SAME. CHECK THEM BEFORE YOUR NEXT BACKUP OR RESTORE."
+msgstr "UTILISER CETTE CONNEXION POUR LE CLOUD ? LES CHEMINS DES DOSSIERS CHOISIS RESTERONT LES MÊMES. VÉRIFIEZ-LES AVANT VOTRE PROCHAINE SAUVEGARDE OU RESTAURATION."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "USE CONNECTION"
+msgstr "UTILISER LA CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "SIGN IN AGAIN"
+msgstr "SE RECONNECTER"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "SIGN IN TO THE SAME CLOUD ACCOUNT AGAIN. YOUR CURRENT SIGN-IN IS KEPT UNTIL THE NEW ONE WORKS. YOUR SELECTED FOLDERS WILL STAY THE SAME."
+msgstr "RECONNECTEZ-VOUS AU MÊME COMPTE CLOUD. VOTRE CONNEXION ACTUELLE EST CONSERVÉE JUSQU’À CE QUE LA NOUVELLE FONCTIONNE. LES DOSSIERS CHOISIS RESTERONT LES MÊMES."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "REMOVE CONNECTION"
+msgstr "SUPPRIMER LA CONNEXION"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "REMOVE THIS CONNECTION FROM THIS DEVICE? YOUR CLOUD FILES STAY WHERE THEY ARE. IF THIS IS YOUR ACTIVE CONNECTION, CHOOSE ANOTHER BEFORE USING CLOUD TOOLS."
+msgstr "SUPPRIMER CETTE CONNEXION DE CET APPAREIL ? VOS FICHIERS CLOUD RESTENT À LEUR PLACE. SI CETTE CONNEXION EST ACTIVE, CHOISISSEZ-EN UNE AUTRE AVANT D’UTILISER LES OUTILS CLOUD."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CONNECTIONS UNAVAILABLE"
+msgstr "CONNEXIONS INDISPONIBLES"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "YOUR CLOUD CONNECTIONS COULDN'T BE READ. TRY AGAIN."
+msgstr "VOS CONNEXIONS AU CLOUD N’ONT PAS PU ÊTRE LUES. RÉESSAYEZ."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "NO CONNECTION IN USE"
+msgstr "AUCUNE CONNEXION UTILISÉE"
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS."
+msgstr "CHOISISSEZ UNE CONNEXION AVANT D’UTILISER LES OUTILS CLOUD."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "A CLOUD OPERATION IS RUNNING. WAIT FOR IT TO FINISH, THEN TRY AGAIN."
+msgstr "UNE OPÉRATION CLOUD EST EN COURS. ATTENDEZ QU’ELLE SE TERMINE, PUIS RÉESSAYEZ."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "ANOTHER CONNECTION USES THIS ONE. CHANGE THAT CONNECTION FIRST."
+msgstr "UNE AUTRE CONNEXION UTILISE CELLE-CI. MODIFIEZ D’ABORD CETTE AUTRE CONNEXION."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "THIS PROVIDER NEEDS ADDITIONAL SETUP. USE A COMPUTER TO FINISH CONNECTING IT."
+msgstr "CE FOURNISSEUR NÉCESSITE DES RÉGLAGES SUPPLÉMENTAIRES. UTILISEZ UN ORDINATEUR POUR TERMINER LA CONNEXION."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "THE CONNECTION DIDN'T ANSWER. CHECK ITS DETAILS AND YOUR NETWORK, THEN TRY AGAIN. YOUR SETTINGS HAVE NOT CHANGED."
+msgstr "LA CONNEXION N’A PAS RÉPONDU. VÉRIFIEZ SES INFORMATIONS ET VOTRE RÉSEAU, PUIS RÉESSAYEZ. VOS RÉGLAGES N’ONT PAS CHANGÉ."
+
+#: es-app/src/guis/GuiMenu.cpp
+msgid "YOUR CLOUD SETTINGS COULD NOT BE READ OR SAVED. TRY AGAIN."
+msgstr "VOS RÉGLAGES CLOUD N’ONT PAS PU ÊTRE LUS OU ENREGISTRÉS. RÉESSAYEZ."
+
+msgid "SAVE CONNECTION"
+msgstr "ENREGISTRER LA CONNEXION"
+
+msgid "UPDATE CONNECTION"
+msgstr "METTRE À JOUR LA CONNEXION"
+
+msgid "UPDATE THIS CONNECTION AND KEEP YOUR SELECTED FOLDERS?\n\nYOUR CURRENT SETTINGS ARE KEPT UNTIL THE NEW ONES WORK."
+msgstr "METTRE À JOUR CETTE CONNEXION EN GARDANT LES DOSSIERS CHOISIS ?\n\nLES RÉGLAGES ACTUELS SONT CONSERVÉS JUSQU’À CE QUE LES NOUVEAUX FONCTIONNENT."
+
+#: es-core/src/guis/GuiTextEditPopup.cpp es-core/src/guis/GuiTextEditPopupKeyboard.cpp
+msgid "CLEAR"
+msgstr "EFFACER"



# FILE checks/target-original/scan.json

{
  "alpha": {
    "rc": 0,
    "stdout": "de8d13ff72ef1d54479671a68fbd765a0502dd22f51ff93c0cbba3adf30ed0ac\n",
    "stderr": ""
  },
  "beta": {
    "rc": 0,
    "stdout": "de8d13ff72ef1d54479671a68fbd765a0502dd22f51ff93c0cbba3adf30ed0ac\n",
    "stderr": ""
  },
  "scan": {
    "rc": 0,
    "stdout": ">>> unit CLOUD FOLDER||\n>>> doing scan\n>>> unit SETTINGS BACKUPS||\n>>> doing scan\n>>> unit GAME CONTENT||\n>>> doing scan\n",
    "stderr": ""
  },
  "valid_before": {
    "rc": 0,
    "stdout": "",
    "stderr": ""
  },
  "switch": {
    "rc": 0,
    "stdout": "OK=beta\n",
    "stderr": ""
  },
  "valid_after": {
    "rc": 0,
    "stdout": "",
    "stderr": ""
  }
}



# FILE checks/target-original/seed.json

{
  "while_seed_alive": true,
  "select_during_seed": {
    "rc": 0,
    "stdout": "OK=beta\n",
    "stderr": ""
  }
}



# FILE checks/target-original/match.json

{
  "preview": {
    "rc": 0,
    "stdout": "qa537audit|sync|1|14\n",
    "stderr": ""
  },
  "plan": "plan 1791702063\nqa537audit|sync|1|14\n",
  "switch": {
    "rc": 0,
    "stdout": "OK=beta\n",
    "stderr": ""
  },
  "apply": {
    "rc": 0,
    "stdout": ">>> unit qa537audit|1|1\nMatching qa537audit to the cloud...\nTransferred:   \t         13 B / 13 B, 100%, 0 B/s, ETA -\nChecks:                 1 / 1, 100%, Listed 2\nDeleted:                1 (files), 0 (dirs), 14 B (freed)\nTransferred:            1 / 1, 100%\nElapsed time:         0.0s\n>>> removed 1|14|qa537audit:1:14\n",
    "stderr": ""
  },
  "local_after": {
    "beta.rom": "89b75aa55ddd01c162e0ea98dc6bb4cd78574d2d7adc3f3972880efae7333b21",
    "save.srm": "bdd8009076dc7a2810afb14550ea599fff610ba5a52f58871892acd9edc129d0"
  }
}



# FILE checks/target-original/installed.json

[
  {
    "name": "cloud_connections.py",
    "sha256": "c010965b42840f8c2c8f946bfc0a61787784531dead4199e5d625d53d00573e8"
  },
  {
    "name": "cloud_remote",
    "sha256": "24777687a1d48d98e9797aae89851d49425ba11c330750dbf806549b70c0b365"
  },
  {
    "name": "cloud_setup",
    "sha256": "32d8696ce4ea467b62223fa17977a474e06d04ba5fa80f702e82cc2eea82d067"
  },
  {
    "name": "cloud_scan",
    "sha256": "17afba1861701b20d1590a10d2c3797f208879e04ca98ab73128e8c8aadeb3d4"
  },
  {
    "name": "cloud_content_restore",
    "sha256": "a5321380835815ca023fd1afe357403db3d2eb46e044503937aa18c37c36e9b4"
  }
]



# FILE checks/target-original/guest.py


from pathlib import Path
import subprocess,json,hashlib,time,os
P=Path('/storage/qa537/audit18');P.mkdir(exist_ok=True)
def run(*args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=90)
 return {'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def save(name,x): (P/name).write_text(json.dumps(x,indent=2)+'\n')
cfg=Path('/storage/.config/rclone/rclone.conf');active=cfg.with_name('active-connection')
sync=Path('/storage/.config/cloud_sync.conf');selected=Path('/storage/.cache/cloud_sync/content-systems')
backups={str(p):p.read_bytes() if p.exists() else None for p in [cfg,active,sync,selected]}
try:
 for remote in ['alpha','beta']:
  p=P/remote/'Content/ROMs/qa537audit';p.mkdir(parents=True,exist_ok=True)
  (p/(remote+'.rom')).write_text(remote+' content\n')
  (P/remote/'Backups').mkdir(exist_ok=True)
  (P/remote/'Saves').mkdir(exist_ok=True)
  (P/remote/'.layout').write_text('layout=2\n')
 cfg.write_text('[alpha]\ntype = alias\nremote = '+str(P/'alpha')+'\n\n[beta]\ntype = alias\nremote = '+str(P/'beta')+'\n');cfg.chmod(0o600)
 active.write_text('alpha\n');active.chmod(0o600)
 sync.write_text('SAVES_REMOTE="/Saves"\nSETTINGS_REMOTE="/Backups"\nCONTENT_REMOTE="/Content"\nRCLONE_NET_OPTS="--contimeout 2s --timeout 3s --low-level-retries 1 --retries 1"\n')
 selected.parent.mkdir(exist_ok=True);selected.write_text('qa537audit\n')
 a=run('cloud_scan','--context');scan=run('cloud_scan','--run-id','audit18-alpha')
 valid_before=run('cloud_scan','--stamp-valid','done','audit18-alpha')
 switched=run('cloud_remote','select','beta');b=run('cloud_scan','--context');valid_after=run('cloud_scan','--stamp-valid','done','audit18-alpha')
 save('scan.json',dict(alpha=a,beta=b,scan=scan,valid_before=valid_before,switch=switched,valid_after=valid_after))
 print('SCAN',a['rc'],b['rc'],'identity_equal',a['stdout']==b['stdout'],'scan_rc',scan['rc'],'stamp_before_after',valid_before['rc'],valid_after['rc'],flush=True)
 # A blocked synthetic mkdir exposes the actual exclusion window without network I/O.
 run('cloud_remote','select','alpha')
 shim=Path('/usr/bin/rclone');shim.write_text('#!/bin/sh\nif [ "$1" = mkdir ] && [ ! -e /storage/qa537/audit18/mkdir-entered ]; then\n touch /storage/qa537/audit18/mkdir-entered\n while [ ! -e /storage/qa537/audit18/release ]; do sleep 0.1; done\nfi\nexec /storage/qa537/rclone-real "$@"\n');shim.chmod(0o755)
 with (P/'seed.log').open('w') as log:
  child=subprocess.Popen(['cloud_setup','--seed-folders','settings'],stdout=log,stderr=subprocess.STDOUT)
  try:
   for _ in range(100):
    if (P/'mkdir-entered').exists():break
    if child.poll() is not None:raise RuntimeError('seed finished before controlled mkdir')
    time.sleep(.1)
   else:raise RuntimeError('no blocked mkdir')
   change=run('cloud_remote','select','beta')
   save('seed.json',{'while_seed_alive':child.poll() is None,'select_during_seed':change})
   print('SEED live',child.poll() is None,'selection_rc',change['rc'],flush=True)
  finally:
   (P/'release').touch();child.wait(timeout=30)
 subprocess.run(['cp','/storage/qa537/rclone-real','/usr/bin/rclone'],check=True)
 run('cloud_remote','select','alpha')
 local=Path('/storage/roms/qa537audit');local.mkdir(exist_ok=True)
 (local/'local.rom').write_text('local content\n');(local/'save.srm').write_text('preserve progress\n')
 preview=run('cloud_content_restore','--match');plan=Path('/storage/.cache/cloud_sync/content-match-plan').read_text()
 change=run('cloud_remote','select','beta');apply=run('cloud_content_restore','--match','--apply')
 files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in local.iterdir() if p.is_file()}
 save('match.json',dict(preview=preview,plan=plan,switch=change,apply=apply,local_after=files))
 print('MATCH preview',preview['rc'],'apply',apply['rc'],'files',list(files),flush=True)
finally:
 subprocess.run(['cp','/storage/qa537/rclone-real','/usr/bin/rclone'],check=True)
 for name,data in backups.items():
  p=Path(name)
  if data is None:p.unlink(missing_ok=True)
  else:p.write_bytes(data)
 print('RESTORED synthetic configuration',flush=True)



# FILE checks/target-original/launcher-result.json

{
  "utc": "2026-10-11T07:01:09.595309+00:00",
  "pid": 3423229,
  "runner_returncode": 0,
  "submission_is_not_completion": true
}



# FILE checks/connections.log

test_add_keeps_legacy_selection (__main__.Connections.test_add_keeps_legacy_selection) ... ok
test_automatic_sync_requires_deliberate_disable (__main__.Connections.test_automatic_sync_requires_deliberate_disable) ... ok
test_blank_edit_preserves_existing_values (__main__.Connections.test_blank_edit_preserves_existing_values) ... ok
test_busy_transfer_refuses_management (__main__.Connections.test_busy_transfer_refuses_management) ... ok
test_cancelled_attempt_does_not_install (__main__.Connections.test_cancelled_attempt_does_not_install) ... ok
test_dependency_refuses_removal (__main__.Connections.test_dependency_refuses_removal) ... ok
test_duplicate_keeps_old_bytes (__main__.Connections.test_duplicate_keeps_old_bytes) ... ok
test_encrypted_config_stays_encrypted_through_management (__main__.Connections.test_encrypted_config_stays_encrypted_through_management) ... ok
test_external_write_refuses_commit (__main__.Connections.test_external_write_refuses_commit) ... ok
test_failed_first_publication_restores_absence (__main__.Connections.test_failed_first_publication_restores_absence) ... ok
test_failed_renewal_keeps_old_bytes (__main__.Connections.test_failed_renewal_keeps_old_bytes) ... ok
test_first_connection_and_manual_empty_selection (__main__.Connections.test_first_connection_and_manual_empty_selection) ... ok
test_missing_selection_never_falls_back (__main__.Connections.test_missing_selection_never_falls_back) ... ok
test_object_store_defaults_only_apply_to_new_connections (__main__.Connections.test_object_store_defaults_only_apply_to_new_connections) ... ok
test_remove_write_failure_restores_selection (__main__.Connections.test_remove_write_failure_restores_selection) ... ok
test_selection_and_removal_never_move_files (__main__.Connections.test_selection_and_removal_never_move_files) ... ok
test_success_record_failure_rolls_back (__main__.Connections.test_success_record_failure_rolls_back) ... ok
test_verified_update_keeps_other_connections (__main__.Connections.test_verified_update_keeps_other_connections) ... ok
test_cancel_during_verification_prevents_commit (__main__.OAuthOwnership.test_cancel_during_verification_prevents_commit) ... ok
test_success_publishes_matching_connection_and_state (__main__.OAuthOwnership.test_success_publishes_matching_connection_and_state) ... ok
test_superseded_session_cannot_replace_credentials (__main__.OAuthOwnership.test_superseded_session_cannot_replace_credentials) ... ok

----------------------------------------------------------------------
Ran 21 tests in 1.068s

OK



# FILE checks/input.log

test_delayed_movement_and_click (__main__.Phone.test_delayed_movement_and_click) ... ok
test_drag_moves_without_click_and_keys_stay_ordered (__main__.Phone.test_drag_moves_without_click_and_keys_stay_ordered) ... ok
test_original_source_negative_control (__main__.Phone.test_original_source_negative_control) ... ok
test_explicit_empty_key_never_borrows_old_key (__main__.Wifi.test_explicit_empty_key_never_borrows_old_key) ... ok
test_mixed_and_absent_fail_closed (__main__.Wifi.test_mixed_and_absent_fail_closed) ... ok
test_open_escaped_name_connects_without_key_or_delete (__main__.Wifi.test_open_escaped_name_connects_without_key_or_delete) ... ok
test_protected_and_unknown_do_not_connect_open (__main__.Wifi.test_protected_and_unknown_do_not_connect_open) ... ok
test_renamed_saved_profile_is_preserved (__main__.Wifi.test_renamed_saved_profile_is_preserved) ... ok
test_service_failure_does_not_connect (__main__.Wifi.test_service_failure_does_not_connect) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.940s

OK



# FILE checks/gate-pkgcheck.log

projects/ROCKNIX/packages/network/rclone/package.mk...



# FILE checks/gate-register-check.log

register-check: 628 IDs, each once; every citation in the live documents names a row



# FILE QA/browser/result.json

{
  "mouseover": true,
  "mousedown": true,
  "mouseup": true,
  "click": true,
  "button": true,
  "typing_and_backspace": true,
  "wheel_scroll": true,
  "auth_link": true,
  "provider_handled_back_preserved": true,
  "modified_back_preserved": true,
  "browser_back": true,
  "popup_loaded": true,
  "popup_return": true,
  "parent_usable": true,
  "unrelated_blocked": true,
  "close_page": true
}



# FILE QA/browser/installed.json

{
  "browser_sha256": "408480959f05132e7fb5cdf5013bb0f4ea4b98cfb178cb85f6dfb712519e1170",
  "oauth_sha256": "0d40129169b34bd5caad3515dffa75a1a5f9b620eee3f7a4d6a15ebb58be240e",
  "source": "browser04; live synthetic provider15; source overlay, not firmware"
}



# FILE QA/editor/review.json

[
  {
    "flow": "en640-osk",
    "binding": "editor/en640-osk/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "en640-plain",
    "binding": "editor/en640-plain/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "fr640-osk",
    "binding": "editor/fr640-osk/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "fr640-plain",
    "binding": "editor/fr640-plain/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "en1280-osk",
    "binding": "editor/en1280-osk/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "en1280-plain",
    "binding": "editor/en1280-plain/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "fr1280-osk",
    "binding": "editor/fr1280-osk/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  },
  {
    "flow": "fr1280-plain",
    "binding": "editor/fr1280-plain/binding.json",
    "reviewed": [
      "clear-focus/01-clear-focus.png",
      "actions/04-remains-clear.png"
    ],
    "verdict": "PASS: clear and cancel fit separately; reopening after clear then cancelled edit stays empty",
    "runtime_checks": "result.json: persistent configuration unchanged"
  }
]



# FILE QA/receipts/guest-transactions/result.log

test_add_keeps_legacy_selection (__main__.Connections.test_add_keeps_legacy_selection) ... ok
test_automatic_sync_requires_deliberate_disable (__main__.Connections.test_automatic_sync_requires_deliberate_disable) ... ok
test_blank_edit_preserves_existing_values (__main__.Connections.test_blank_edit_preserves_existing_values) ... ok
test_busy_transfer_refuses_management (__main__.Connections.test_busy_transfer_refuses_management) ... ok
test_cancelled_attempt_does_not_install (__main__.Connections.test_cancelled_attempt_does_not_install) ... ok
test_dependency_refuses_removal (__main__.Connections.test_dependency_refuses_removal) ... ok
test_duplicate_keeps_old_bytes (__main__.Connections.test_duplicate_keeps_old_bytes) ... ok
test_encrypted_config_stays_encrypted_through_management (__main__.Connections.test_encrypted_config_stays_encrypted_through_management) ... ok
test_external_write_refuses_commit (__main__.Connections.test_external_write_refuses_commit) ... ok
test_failed_first_publication_restores_absence (__main__.Connections.test_failed_first_publication_restores_absence) ... ok
test_failed_renewal_keeps_old_bytes (__main__.Connections.test_failed_renewal_keeps_old_bytes) ... ok
test_first_connection_and_manual_empty_selection (__main__.Connections.test_first_connection_and_manual_empty_selection) ... ok
test_missing_selection_never_falls_back (__main__.Connections.test_missing_selection_never_falls_back) ... ok
test_object_store_defaults_only_apply_to_new_connections (__main__.Connections.test_object_store_defaults_only_apply_to_new_connections) ... ok
test_remove_write_failure_restores_selection (__main__.Connections.test_remove_write_failure_restores_selection) ... ok
test_selection_and_removal_never_move_files (__main__.Connections.test_selection_and_removal_never_move_files) ... ok
test_success_record_failure_rolls_back (__main__.Connections.test_success_record_failure_rolls_back) ... ok
test_verified_update_keeps_other_connections (__main__.Connections.test_verified_update_keeps_other_connections) ... ok
test_cancel_during_verification_prevents_commit (__main__.OAuthOwnership.test_cancel_during_verification_prevents_commit) ... ok
test_success_publishes_matching_connection_and_state (__main__.OAuthOwnership.test_success_publishes_matching_connection_and_state) ... ok
test_superseded_session_cannot_replace_credentials (__main__.OAuthOwnership.test_superseded_session_cannot_replace_credentials) ... ok

----------------------------------------------------------------------
Ran 21 tests in 2.899s

OK



# FILE QA/receipts/pix537-oauth-lifetime.log

PASS phone
PASS keyboard
PASS no-browser
PASS failed-start



# FILE QA/receipts/pix535-es-unit-results.log

[doctest] doctest version is "2.4.12"
[doctest] run with "--help" for options
===============================================================================
[doctest] test cases:  185 |  185 passed | 0 failed | 0 skipped
[doctest] assertions: 4793 | 4793 passed | 0 failed |
[doctest] Status: SUCCESS!



# FILE distribution/projects/ROCKNIX/packages/network/cloud-signin-window/sources/cloud-signin-window.c


## Original lines 1–1052
1: /* SPDX-License-Identifier: GPL-2.0
2:  * Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
3:  *
4:  * cloud-signin-window - one fullscreen web view, for one job.
5:  *
6:  * A cloud provider's OAuth redirect goes to http://localhost:<port>, which
7:  * resolves on whichever machine is running the browser. If that is the
8:  * player's phone, nothing is listening and they land on an error page they
9:  * have to copy an address out of. So the browser runs here instead, where
10:  * rclone's authorize listener actually is, and the player drives it with the
11:  * handheld's own buttons -- cloud_oauth turns them into keys -- or types into
12:  * it from their phone, whose keystrokes arrive as a keyboard (cloud_oauth's
13:  * RemoteKeyboard). Nothing is mirrored. (This said "over VNC", the design
14:  * the keyboard replaced; #308 claude F-RS-14.)
15:  *
16:  * This is deliberately not a browser. There is no address bar, no tabs, no
17:  * downloads, and navigation is refused outside the provider's own host and
18:  * the loopback redirect -- a handheld should not become a way to browse the
19:  * web because we needed somebody to sign in to Dropbox.
20:  *
21:  *   cloud-signin-window <url> <allowed-host> [--exit-hint TEXT]
22:  *                       [--no-auto-keyboard]
23:  */
24: 
25: #include <gtk/gtk.h>
26: #include <glib/gstdio.h>
27: #include <webkit2/webkit2.h>
28: #include <string.h>
29: #include <strings.h>
30: 
31: #define OSK_ROWS 4
32: #define OSK_COLS 11
33: 
34: static const char *allowed_host = NULL;
35: 
36: static gboolean host_permitted(const char *host)
37: {
38:     if (!host)
39:         return FALSE;
40:     if (g_strcmp0(host, "localhost") == 0 || g_strcmp0(host, "127.0.0.1") == 0)
41:         return TRUE;
42:     if (!allowed_host)
43:         return TRUE;
44:     /* Dropbox offers these identity providers on its sign-in page. They
45:      * are exact authentication hosts, not a general browsing exception. */
46:     if (g_ascii_strcasecmp(allowed_host, "dropbox.com") == 0 &&
47:         (g_ascii_strcasecmp(host, "accounts.google.com") == 0 ||
48:          g_ascii_strcasecmp(host, "appleid.apple.com") == 0 ||
49:          g_ascii_strcasecmp(host, "login.microsoftonline.com") == 0 ||
50:          g_ascii_strcasecmp(host, "login.live.com") == 0))
51:         return TRUE;
52:     /* the host itself, or any subdomain of it: providers bounce sign-ins
53:      * through their own auth and CDN subdomains constantly. */
54:     size_t hl = strlen(host), al = strlen(allowed_host);
55:     if (hl == al && g_ascii_strcasecmp(host, allowed_host) == 0)
56:         return TRUE;
57:     return hl > al && host[hl - al - 1] == '.'
58:         && g_ascii_strcasecmp(host + hl - al, allowed_host) == 0;
59: }
60: 
61: /* An on-screen keyboard, because the handheld has no touchscreen and typing
62:  * from a phone is meant to be optional rather than required. Consoles solve
63:  * this the same way: a grid walked with the d-pad and pressed with A. GTK
64:  * moves focus between the buttons on its own, so the d-pad drives it with no
65:  * extra handling.
66:  *
67:  * Keys go in as GDK key events rather than being written into the DOM. A
68:  * provider's login form watches keystrokes -- validating an address as it is
69:  * typed, enabling the button, moving focus -- and text poked straight into a
70:  * field arrives with none of that having happened.
71:  */
72: typedef struct {
73:     GtkWidget *revealer;
74:     GtkWidget *hints;
75:     const char *exit_hint;
76:     gboolean auto_raise;
77:     WebKitWebView *view;
78:     GtkWidget *keys[OSK_ROWS + 1][OSK_COLS];   /* +1: the extras row */
79:     int row, col;
80:     gboolean shift;
81:     gboolean symbols;
82:     char last_field[256];
83:     /* Whether this page's field record (CLOUD_SIGNIN_FIELD_FILE) has been
84:      * written; each new page starts without one. */
85:     gboolean field_recorded;
86: } Osk;
87: 
88: /* Two layouts rather than a modifier: a sign-in needs capitals for an address
89:  * and punctuation for a password, and a shift that only latches for one key is
90:  * a mechanism to explain on a screen with no room to explain it. */
91: static const char *OSK_LOWER[OSK_ROWS] = {
92:     "1234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm.-_",
93: };
94: static const char *OSK_UPPER[OSK_ROWS] = {
95:     "!@#$%^&*()", "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM+?/",
96: };
97: /* The rest of printable ASCII. The two layouts above lacked
98:  * = : ; ' " , < > [ ] { } \ | ` and ~, so a password holding any of them
99:  * could not be typed on the handheld at all (#308 gpt F-RS-12). A third
100:  * layout, reached from its own key, rather than a longer shift cycle: the
101:  * letters stay one press from wherever you are. Each row is as long as the
102:  * lower-case one, because the keys are built from that one and relabelled;
103:  * the last row repeats the punctuation an address or a password reaches
104:  * for most. */
105: static const char *OSK_SYMBOLS[OSK_ROWS] = {
106:     "!@#$%^&*()", "-_=+[]{}\\|", ";:'\",.<>/", "?~`.,-_@/:",
107: };
108: #define OSK_TO_SYMBOLS "#+="
109: #define OSK_TO_LETTERS "abc"
110: static const char *OSK_EXTRAS[] = { "shift", "space", "@", "del", "enter", "hide",
111:                                     OSK_TO_SYMBOLS };
112: 
113: /* Sized for a four-inch screen held at arm's length, and dark because it sits
114:  * under a page that is usually white -- a keyboard that flashes the screen
115:  * bright every time it appears is the thing people turn the brightness down
116:  * to avoid. The selected key is drawn by osk-sel, not by GTK's focus ring:
117:  * nothing here ever holds focus. */
118: static const char *OSK_CSS =
119:     "#osk { background: #14171c; padding: 6px; }"
120:     "#osk button {"
121:     "  background-image: none; background-color: #262b33;"
122:     "  color: #e8ecf2; border: 1px solid #333a45; border-radius: 5px;"
123:     "  padding: 6px 2px; margin: 0; min-height: 30px; min-width: 20px;"
124:     "  font-size: 16px; text-shadow: none;"
125:     "}"
126:     "#osk button.osk-sel {"
127:     "  background-color: #f0f3f8; color: #14171c;"
128:     "  border: 2px solid #ffffff; font-weight: bold;"
129:     "}"
130:     "#hints { background: #0d1014; color: #93a0b4; font-size: 12px;"
131:     "         padding: 4px 8px; }";
132: 
133: static void osk_type(Osk *osk, guint keyval)
134: {
135:     /* The WebView holds GTK focus the whole time the keyboard is up -- the
136:      * keys never take it. A WebView that loses focus blurs the field the
137:      * player is typing into, and a character delivered to a blurred field
138:      * goes nowhere; the d-pad is intercepted in on_key instead, which is
139:      * what makes keeping focus here possible. */
140:     GtkWidget *target = GTK_WIDGET(osk->view);
141:     GdkWindow *gdkwin = gtk_widget_get_window(target);
142:     if (!gdkwin)
143:         return;
144: 
145:     for (int press = 1; press >= 0; press--) {
146:         GdkEvent *event = gdk_event_new(press ? GDK_KEY_PRESS : GDK_KEY_RELEASE);
147:         event->key.window = g_object_ref(gdkwin);
148:         event->key.send_event = TRUE;
149:         event->key.time = GDK_CURRENT_TIME;
150:         event->key.keyval = keyval;
151:         event->key.state = 0;
152:         gtk_main_do_event(event);
153:         gdk_event_free(event);
154:     }
155: }
156: 
157: static void osk_relabel(Osk *osk);
158: static void osk_highlight(Osk *osk);
159: static void osk_type(Osk *osk, guint keyval);
160: 
161: /* Y found no overlay, so it does what it says on the help bar and steps to
162:  * the next control. Answering in the callback rather than sending Tab up
163:  * front matters: sending both would skip a control every time an overlay was
164:  * present. */
165: static void on_jump_done(GObject *source, GAsyncResult *result, gpointer data)
166: {
167:     JSCValue *value = webkit_web_view_evaluate_javascript_finish(
168:         WEBKIT_WEB_VIEW(source), result, NULL);
169:     if (!value)
170:         return;
171: 
172:     char *text = jsc_value_to_string(value);
173:     if (g_strcmp0(text, "none") == 0)
174:         osk_type((Osk *) data, GDK_KEY_Tab);
175:     g_free(text);
176:     g_object_unref(value);
177: }
178: 
179: /* The help bar has to describe the buttons as they behave at this moment. It
180:  * said "B back" while the keyboard was up, where B closes the keyboard and
181:  * goes nowhere -- a help line that is wrong is worse than no help line, since
182:  * it is believed. */
183: static void osk_hints(Osk *osk)
184: {
185:     gboolean up = gtk_revealer_get_reveal_child(GTK_REVEALER(osk->revealer));
186:     char *text = up
187:         ? g_strdup_printf("A press key     B or X close keyboard     "
188:                           "L1/R1 scroll     %s to exit", osk->exit_hint)
189:         : g_strdup_printf("A select     B back     X keyboard     "
190:                           "Y next     L1/R1 scroll     %s to exit",
191:                           osk->exit_hint);
192:     if (osk->hints)
193:         gtk_label_set_text(GTK_LABEL(osk->hints), text);
194:     g_free(text);
195: }
196: 
197: static void osk_hide(Osk *osk)
198: {
199:     gtk_revealer_set_reveal_child(GTK_REVEALER(osk->revealer), FALSE);
200:     gtk_widget_grab_focus(GTK_WIDGET(osk->view));
201:     osk_hints(osk);
202: }
203: 
204: static void osk_show(Osk *osk)
205: {
206:     gtk_revealer_set_reveal_child(GTK_REVEALER(osk->revealer), TRUE);
207:     gtk_widget_grab_focus(GTK_WIDGET(osk->view));
208:     osk_highlight(osk);
209:     osk_hints(osk);
210: }
211: 
212: /* One entry point for a key, whether it arrived from the d-pad or from a
213:  * finger. Touchscreen handhelds exist and the buttons stay clickable; they
214:  * are set can-focus=FALSE so a tap cannot steal focus from the page. */
215: static void osk_press(Osk *osk, const char *label)
216: {
217:     if (g_strcmp0(label, "hide") == 0)       { osk_hide(osk); return; }
218:     if (g_strcmp0(label, "shift") == 0)      { if (osk->symbols)
219:                                                    osk->symbols = FALSE;
220:                                                else
221:                                                    osk->shift = !osk->shift;
222:                                                osk_relabel(osk); return; }
223:     if (g_strcmp0(label, OSK_TO_SYMBOLS) == 0
224:         || g_strcmp0(label, OSK_TO_LETTERS) == 0) {
225:         osk->symbols = !osk->symbols;
226:         osk_relabel(osk);
227:         return;
228:     }
229:     if (g_strcmp0(label, "space") == 0)      { osk_type(osk, GDK_KEY_space); return; }
230:     if (g_strcmp0(label, "del") == 0)        { osk_type(osk, GDK_KEY_BackSpace); return; }
231:     if (g_strcmp0(label, "enter") == 0)      { osk_type(osk, GDK_KEY_Return); return; }
232:     if (!*label)
233:         return;
234:     osk_type(osk, gdk_unicode_to_keyval((guint) g_utf8_get_char(label)));
235: }
236: 
237: static void on_osk_clicked(GtkButton *button, gpointer data)
238: {
239:     osk_press(data, gtk_button_get_label(button));
240: }
241: 
242: static void osk_relabel(Osk *osk)
243: {
244:     const char **rows = osk->symbols ? OSK_SYMBOLS
245:                       : osk->shift ? OSK_UPPER : OSK_LOWER;
246:     for (int r = 0; r < OSK_ROWS; r++)
247:         for (int c = 0; c < OSK_COLS && osk->keys[r][c]; c++) {
248:             const char *src = rows[r];
249:             if ((int) strlen(src) <= c)
250:                 continue;
251:             char label[2] = { src[c], 0 };
252:             gtk_button_set_label(GTK_BUTTON(osk->keys[r][c]), label);
253:         }
254:     /* The layout key says where it goes: to the symbols, or back. */
255:     for (int c = 0; c < OSK_COLS && osk->keys[OSK_ROWS][c]; c++) {
256:         const char *now = gtk_button_get_label(GTK_BUTTON(osk->keys[OSK_ROWS][c]));
257:         if (g_strcmp0(now, OSK_TO_SYMBOLS) == 0 || g_strcmp0(now, OSK_TO_LETTERS) == 0)
258:             gtk_button_set_label(GTK_BUTTON(osk->keys[OSK_ROWS][c]),
259:                                  osk->symbols ? OSK_TO_LETTERS : OSK_TO_SYMBOLS);
260:     }
261: }
262: 
263: /* The selected key is drawn by us, not by GTK's focus ring, because nothing
264:  * in the keyboard ever holds focus. */
265: static void osk_highlight(Osk *osk)
266: {
267:     for (int r = 0; r < OSK_ROWS + 1; r++)
268:         for (int c = 0; c < OSK_COLS; c++) {
269:             GtkWidget *w = osk->keys[r][c];
270:             if (!w)
271:                 continue;
272:             GtkStyleContext *ctx = gtk_widget_get_style_context(w);
273:             if (r == osk->row && c == osk->col)
274:                 gtk_style_context_add_class(ctx, "osk-sel");
275:             else
276:                 gtk_style_context_remove_class(ctx, "osk-sel");
277:         }
278: }
279: 
280: static int osk_row_len(Osk *osk, int row)
281: {
282:     int n = 0;
283:     for (int c = 0; c < OSK_COLS && osk->keys[row][c]; c++)
284:         n++;
285:     return n;
286: }
287: 
288: static void osk_move(Osk *osk, int dr, int dc)
289: {
290:     int rows = OSK_ROWS + 1;
291:     osk->row = (osk->row + dr + rows) % rows;
292:     int len = osk_row_len(osk, osk->row);
293:     if (len == 0)
294:         return;
295:     if (dr != 0 && osk->col >= len)
296:         osk->col = len - 1;
297:     if (dc != 0)
298:         osk->col = (osk->col + dc + len) % len;
299:     osk_highlight(osk);
300: }
301: 
302: static GtkWidget *osk_build(Osk *osk)
303: {
304:     GtkWidget *box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 4);
305:     gtk_widget_set_name(box, "osk");
306: 
307:     for (int r = 0; r < OSK_ROWS; r++) {
308:         GtkWidget *row = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 4);
309:         int c = 0;
310:         for (const char *p = OSK_LOWER[r]; *p && c < OSK_COLS; p++, c++) {
311:             char label[2] = { *p, 0 };
312:             GtkWidget *b = gtk_button_new_with_label(label);
313:             gtk_widget_set_can_focus(b, FALSE);
314:             g_signal_connect(b, "clicked", G_CALLBACK(on_osk_clicked), osk);
315:             gtk_box_pack_start(GTK_BOX(row), b, TRUE, TRUE, 0);
316:             osk->keys[r][c] = b;
317:         }
318:         gtk_box_pack_start(GTK_BOX(box), row, FALSE, FALSE, 0);
319:     }
320: 
321:     GtkWidget *row = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 4);
322:     for (guint i = 0; i < G_N_ELEMENTS(OSK_EXTRAS) && i < OSK_COLS; i++) {
323:         GtkWidget *b = gtk_button_new_with_label(OSK_EXTRAS[i]);
324:         gtk_widget_set_can_focus(b, FALSE);
325:         g_signal_connect(b, "clicked", G_CALLBACK(on_osk_clicked), osk);
326:         gtk_box_pack_start(GTK_BOX(row), b, TRUE, TRUE, 0);
327:         osk->keys[OSK_ROWS][i] = b;
328:     }
329:     gtk_box_pack_start(GTK_BOX(box), row, FALSE, FALSE, 0);
330:     return box;
331: }
332: 
333: /* Raise the keyboard when the page puts the caret in a text field, and do it
334:  * once per field. A handheld with a touchscreen focuses a field by being
335:  * tapped and one without does it by pressing A on it; neither is a moment
336:  * where the player should have to know that X exists. */
337: /* GtkSpinner draws from the icon theme, and this image ships no pixbuf
338:  * loaders for it -- "Could not load a pixbuf from .../process-working-
339:  * symbolic.png". It renders nothing at all, silently, which is why the
340:  * loading screen was a line of text on an empty page. Cairo is always
341:  * there. */
342: typedef struct { double phase; } Spin;
343: 
344: static gboolean on_spin_draw(GtkWidget *widget, cairo_t *cr, gpointer data)
345: {
346:     Spin *spin = data;
347:     int w = gtk_widget_get_allocated_width(widget);
348:     int h = gtk_widget_get_allocated_height(widget);
349:     double r = (MIN(w, h) / 2.0) - 4.0;
350: 
351:     cairo_set_line_width(cr, 4.0);
352:     cairo_set_line_cap(cr, CAIRO_LINE_CAP_ROUND);
353: 
354:     cairo_set_source_rgba(cr, 0.0, 0.0, 0.0, 0.10);
355:     cairo_arc(cr, w / 2.0, h / 2.0, r, 0, 2 * G_PI);
356:     cairo_stroke(cr);
357: 
358:     cairo_set_source_rgba(cr, 0.10, 0.12, 0.15, 0.85);
359:     cairo_arc(cr, w / 2.0, h / 2.0, r, spin->phase, spin->phase + G_PI / 2.0);
360:     cairo_stroke(cr);
361:     return FALSE;
362: }
363: 
364: static gboolean on_spin_tick(gpointer widget)
365: {
366:     Spin *spin = g_object_get_data(G_OBJECT(widget), "spin");
367:     spin->phase += 0.22;
368:     if (spin->phase > 2 * G_PI)
369:         spin->phase -= 2 * G_PI;
370:     gtk_widget_queue_draw(GTK_WIDGET(widget));
371:     return G_SOURCE_CONTINUE;
372: }
373: 
374: static void on_probe(GObject *source, GAsyncResult *result, gpointer data)
375: {
376:     Osk *osk = data;
377:     GError *error = NULL;
378:     JSCValue *value = webkit_web_view_evaluate_javascript_finish(
379:         WEBKIT_WEB_VIEW(source), result, &error);
380: 
381:     if (!value) {
382:         if (error) {
383:             if (g_getenv("CLOUD_SIGNIN_DEBUG"))
384:                 g_message("probe failed: %s", error->message);
385:             g_error_free(error);
386:         }
387:         return;
388:     }
389: 
390:     /* A reply from the covered parent must not change the popup's caret. */
391:     if (osk && source != G_OBJECT(osk->view)) {
392:         g_object_unref(value);
393:         return;
394:     }
395:     char *text = jsc_value_to_string(value);
396:     if (g_getenv("CLOUD_SIGNIN_DEBUG"))
397:         g_message("probe %s", text);
398: 
399:     if (osk && text && g_str_has_prefix(text, "text:")) {
400:         const char *field = text + 5;
401:         /* A field on this page has the caret: say so, once per page, for
402:          * the phone. Its text goes across from here -- not from the moment
403:          * this window's process started, while the page was still loading
404:          * and nothing could take a keystroke (the audit of the fix round,
405:          * claude G2-C-01). The load of the next page takes the record away. */
406:         if (!osk->field_recorded) {
407:             const char *field_file = g_getenv("CLOUD_SIGNIN_FIELD_FILE");
408:             if (field_file && g_file_set_contents(field_file, field, -1, NULL))
409:                 osk->field_recorded = TRUE;
410:         }
411:         /* Only on a change of field. Re-raising a keyboard the player just
412:          * dismissed, every half second (probe_tick), would be worse than
413:          * never raising it. */
414:         if (g_strcmp0(field, osk->last_field) != 0) {
415:             g_strlcpy(osk->last_field, field, sizeof(osk->last_field));
416:             /* Not for somebody who chose to type on their phone: they asked
417:              * for the other keyboard, and this one only takes up the screen
418:              * they are reading the form on. X still summons it. */
419:             if (osk->auto_raise
420:                 && !gtk_revealer_get_reveal_child(GTK_REVEALER(osk->revealer)))
421:                 osk_show(osk);
422:         }
423:     } else if (osk) {
424:         osk->last_field[0] = 0;
425:     }
426: 
427:     g_free(text);
428:     g_object_unref(value);
429: }
430: 
431: /* Shown while EmulationStation rebuilds itself behind this window.
432:  * Rebuilding takes a few seconds -- it reloads every resource it had
433:  * released -- and closing first left the player looking at a black screen
434:  * immediately after a sign-in that had just succeeded, which reads as a
435:  * crash rather than as progress.
436:  *
437:  * In the phone page's own style (cloud_oauth's STYLE: the dark card, the
438:  * heading, the note), reading as a success and saying what happens next
439:  * (fork #351 section 4; the approved words, D-CLOUD-164 string 13). It was
440:  * one unstyled line, which the maintainer read as "a 404 page or something
441:  * incredibly basic" (2026-09-30). A data: URL, so # is %23 and the page
442:  * needs no file the window would have to find. */
443: static const char *FINISHING_PAGE =
444:     "data:text/html,<meta name=viewport content='width=device-width'>"
445:     "<style>body{font:16px/1.5 system-ui,sans-serif;margin:0;padding:20px;"
446:     "background:%23111;color:%23eee;min-height:100vh;box-sizing:border-box;"
447:     "display:flex;align-items:center;justify-content:center}"
448:     ".card{max-width:34rem;text-align:center}"
449:     "h1{font-size:1.6rem;margin:0 0 .5rem;color:%232d7}"
450:     ".note{color:%23aaa;font-size:1rem}</style>"
451:     "<body><div class=card><h1>Connected</h1>"
452:     "<p class=note>Finishing up on your handheld&hellip;</p></div></body>";
453: 
454: /* The broker passes the handheld's ES locale, shared with the phone's close
455:  * confirmation. HTML entities keep this data URL independent of encoding. */
456: static const char *FINISHING_PAGE_FR =
457:     "data:text/html,<meta name=viewport content='width=device-width'>"
458:     "<style>body{font:16px/1.5 system-ui,sans-serif;margin:0;padding:20px;"
459:     "background:%23111;color:%23eee;min-height:100vh;box-sizing:border-box;"
460:     "display:flex;align-items:center;justify-content:center}"
461:     ".card{max-width:34rem;text-align:center}"
462:     "h1{font-size:1.6rem;margin:0 0 .5rem;color:%232d7}"
463:     ".note{color:%23aaa;font-size:1rem}</style>"
464:     "<body><div class=card lang=fr><h1>Connect&eacute;</h1>"
465:     "<p class=note>Finalisation sur votre console&hellip;</p></div></body>";
466: 
467: static gboolean probe_tick(gpointer data)
468: {
469:     Osk *osk = data;
470: 
471:     /* cloud_oauth says the sign-in landed. Nothing on the provider's page
472:      * matters from here, and this window is the only thing on the screen
473:      * until EmulationStation is back. */
474:     const char *done_file = g_getenv("CLOUD_SIGNIN_DONE_FILE");
475:     if (done_file && g_file_test(done_file, G_FILE_TEST_EXISTS)) {
476:         webkit_web_view_load_uri(osk->view,
477:             g_strcmp0(g_getenv("CLOUD_SIGNIN_LANGUAGE"), "fr") == 0 ? FINISHING_PAGE_FR : FINISHING_PAGE);
478:         if (osk->hints)
479:             gtk_widget_hide(osk->hints);
480:         gtk_revealer_set_reveal_child(GTK_REVEALER(osk->revealer), FALSE);
481:         return G_SOURCE_REMOVE;
482:     }
483:     static const char *script =
484:         "(function () {"
485:         "  var a = document.activeElement;"
486:         /* A provider moves from email to password without loading a page, and
487:          * leaves focus on the body. Nothing then has the caret, so the
488:          * on-screen keyboard has nowhere to type and spatial navigation has
489:          * no anchor to move from -- the password box cannot be selected at
490:          * all, which is where a real sign-in stopped. Adopt a field when the
491:          * page has abandoned focus, never when something else holds it. */
492:         "  if (!a || a === document.body || a.tagName === 'BODY') {"
493:         "    var boxes = document.querySelectorAll("
494:         "      'input[type=text],input[type=email],input[type=password],"
495:         "       input[type=tel],input[type=url],input:not([type]),textarea');"
496:         "    for (var i = 0; i < boxes.length; i++) {"
497:         "      var b = boxes[i], r = b.getBoundingClientRect();"
498:         "      if (!r.width || !r.height || b.disabled || b.readOnly) continue;"
499:         "      if (r.bottom < 0 || r.top > innerHeight) continue;"
500:         "      b.focus();"
501:         "      a = document.activeElement;"
502:         "      break;"
503:         "    }"
504:         "  }"
505:         "  if (!a) return 'none';"
506:         "  var t = (a.tagName || '').toUpperCase();"
507:         "  var ty = (a.type || 'text').toLowerCase();"
508:         "  var typed = t === 'TEXTAREA' || a.isContentEditable ||"
509:         "              (t === 'INPUT' && ['text','email','password','search',"
510:         "               'url','tel','number'].indexOf(ty) >= 0);"
511:         "  if (!typed) return 'other:' + t;"
512:         "  return 'text:' + t + '/' + ty + '/' + (a.id || a.name || '?');"
513:         "})();";
514: 
515:     /* Asked every half second, keyboard up or not. What keeps this from
516:      * oscillating -- a page can report a different active element the
517:      * moment the caret moves -- is on_probe acting only on a change of
518:      * field, not a pause while the keyboard is driven (this said there was
519:      * one; #308 claude F-RS-14). */
520:     webkit_web_view_evaluate_javascript(osk->view, script, -1,
521:                                         NULL, NULL, NULL, on_probe, osk);
522:     return G_SOURCE_CONTINUE;
523: }
524: 
525: /* Instrumentation, kept deliberately. Keystrokes arriving from the phone go
526:  * uinput -> kernel -> libinput -> sway -> here, and when they stopped landing
527:  * every hop but the last could be proven individually. Without this line
528:  * there is no way to tell "sway never delivered it" from "the page had
529:  * nothing focused". */
530: static gboolean on_key(GtkWidget *widget, GdkEventKey *event, gpointer data)
531: {
532:     if (g_getenv("CLOUD_SIGNIN_DEBUG"))
533:         g_message("key %s (%u)", event->string && *event->string ? event->string : "?",
534:                   event->keyval);
535: 
536:     /* A way out, always. The handheld's buttons are not a keyboard -- sway
537:      * reports the gamepad as a tablet_pad -- so without something mapping
538:      * them, this window covers the screen, cannot be driven from the device
539:      * and cannot be closed. Escape is what the phone's "Close page" sends,
540:      * and a keyboard plugged in; the pad's Select + Start ends the window
541:      * from cloud_oauth's side (GAMEPAD_QUIT -> stop_browser) and never
542:      * arrives here. (This said cloud_oauth mapped Start to Escape; #308
543:      * claude F-RS-14.) */
544:     if (event->keyval == GDK_KEY_Escape) {
545:         gtk_main_quit();
546:         return TRUE;
547:     }
548: 
549:     Osk *osk = data;
550:     if (!osk)
551:         return FALSE;
552: 
553:     /* Y. Tab reaches everything the page can focus, but a consent banner is
554:      * pinned to the viewport and sits at the end of the document, so getting
555:      * to it costs about ten presses -- and the d-pad never gets there at all,
556:      * because spatial navigation will not descend into a fixed-position
557:      * element. Measured on Dropbox's own sign-in page: Down stops on the
558:      * language picker just above the banner.
559:      *
560:      * So Y goes to the overlay first if there is one, and behaves as Tab
561:      * afterwards. Overlays are found by what they are rather than by who
562:      * published them -- a visible control inside a fixed or sticky box --
563:      * because a rule per provider is a rule that rots. */
564:     if (event->keyval == GDK_KEY_F4) {
565:         static const char *jump =
566:             "(function () {"
567:             "  var all = document.querySelectorAll("
568:             "    'button,[role=button],a[href],input,select,textarea');"
569:             "  var ov = [];"
570:             "  for (var i = 0; i < all.length; i++) {"
571:             "    var e = all[i], r = e.getBoundingClientRect();"
572:             "    if (!r.width || !r.height) continue;"
573:             "    if (r.bottom < 0 || r.top > innerHeight) continue;"
574:             "    var n = e, fixed = false;"
575:             "    while (n && n !== document.body) {"
576:             "      var pos = getComputedStyle(n).position;"
577:             "      if (pos === 'fixed' || pos === 'sticky') { fixed = true; break; }"
578:             "      n = n.parentElement;"
579:             "    }"
580:             "    if (fixed) ov.push(e);"
581:             "  }"
582:             "  if (!ov.length) return 'none';"
583:             "  var at = ov.indexOf(document.activeElement);"
584:             "  var next;"
585:             "  if (at >= 0) {"
586:             "    next = ov[(at + 1) % ov.length];"
587:             "  } else {"
588:             "    next = ov.find(function (e) {"
589:             "      return e.tagName === 'BUTTON'"
590:             "          || e.getAttribute('role') === 'button';"
591:             "    }) || ov[0];"
592:             "  }"
593:             "  next.focus();"
594:             "  return 'overlay';"
595:             "})();";
596:         webkit_web_view_evaluate_javascript(osk->view, jump, -1,
597:                                             NULL, NULL, NULL,
598:                                             on_jump_done, osk);
599:         return TRUE;
600:     }
601: 
602:     /* L1 and R1, mapped to F2/F3 by cloud_oauth. Scrolling is done in the
603:      * page rather than by sending Page_Up, because Page_Up does nothing at
604:      * all while a text field has the caret -- which is most of the time on a
605:      * sign-in form, and exactly when the button below the fold is the thing
606:      * that cannot be reached. */
607:     if (event->keyval == GDK_KEY_F2 || event->keyval == GDK_KEY_F3) {
608:         const char *js = event->keyval == GDK_KEY_F2
609:             ? "window.scrollBy({top: -Math.round(innerHeight*0.7), behavior:'smooth'});"
610:             : "window.scrollBy({top:  Math.round(innerHeight*0.7), behavior:'smooth'});";
611:         webkit_web_view_evaluate_javascript(osk->view, js, -1,
612:                                             NULL, NULL, NULL, NULL, NULL);
613:         return TRUE;
614:     }
615: 
616:     /* X on the handheld, mapped to F1. */
617:     gboolean showing = gtk_revealer_get_reveal_child(GTK_REVEALER(osk->revealer));
618:     if (event->keyval == GDK_KEY_F1) {
619:         if (showing)
620:             osk_hide(osk);
621:         else
622:             osk_show(osk);
623:         return TRUE;
624:     }
625: 
626:     /* While the keyboard is up the d-pad walks its keys and A presses one.
627:      * These are intercepted here, before the page sees them, which is what
628:      * lets the WebView keep focus throughout -- see osk_type. B closes the
629:      * keyboard rather than navigating back, because with a keyboard open
630:      * that is what B means everywhere else. */
631:     if (showing) {
632:         switch (event->keyval) {
633:         case GDK_KEY_Up:    osk_move(osk, -1,  0); return TRUE;
634:         case GDK_KEY_Down:  osk_move(osk,  1,  0); return TRUE;
635:         case GDK_KEY_Left:  osk_move(osk,  0, -1); return TRUE;
636:         case GDK_KEY_Right: osk_move(osk,  0,  1); return TRUE;
637:         case GDK_KEY_Return:
638:         case GDK_KEY_KP_Enter: {
639:             GtkWidget *key = osk->keys[osk->row][osk->col];
640:             if (key)
641:                 osk_press(osk, gtk_button_get_label(GTK_BUTTON(key)));
642:             return TRUE;
643:         }
644:         case GDK_KEY_BackSpace:
645:             osk_hide(osk);
646:             return TRUE;
647:         default:
648:             break;
649:         }
650:     }
651:     return FALSE;
652: }
653: 
654: /* Whether an address goes in the page file. Not rclone's loopback redirect:
655:  * http://127.0.0.1:53682/?state=...&code=... carries the OAuth code, a
656:  * credential even once redeemed, and the file is read by another process
657:  * and lives in /var/run with whatever mode the umask gives it (#308 claude
658:  * F-RS-20). The phone loses nothing -- the window turns to "Finishing up"
659:  * there. Plain C, host by host, so it can be tested without GTK. */
660: static int page_worth_recording(const char *uri)
661: {
662:     const char *host = uri ? strstr(uri, "://") : NULL;
663:     if (!host)
664:         return 1;
665:     host += 3;
666:     size_t n = strcspn(host, ":/?#");
667:     if (n == 9 && (strncmp(host, "127.0.0.1", 9) == 0
668:                    || strncasecmp(host, "localhost", 9) == 0))
669:         return 0;
670:     return 1;
671: }
672: 
673: /* WebKit only routes keys to the page when the WebView itself holds GTK
674:  * focus. A window can be focused by the compositor -- sway reported
675:  * focused=true -- while the widget inside it never took focus, which looks
676:  * exactly like the keyboard not working. The page may also move focus during
677:  * load, so this reasserts once the load settles. */
678: static void on_load_changed(WebKitWebView *view, WebKitLoadEvent event,
679:                             gpointer data)
680: {
681:     Osk *osk = data;
682:     if (event != WEBKIT_LOAD_FINISHED || (osk && osk->view != view))
683:         return;
684: 
685:     GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
686:     if (stack)
687:         gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(view));
688: 
689:     /* WebKitGTK does not map Backspace to history navigation. Handle the
690:      * bubbled DOM event, respecting editable fields, already-handled keys and
691:      * modified shortcuts. Window listeners see provider document handlers first. */
692:     webkit_web_view_evaluate_javascript(view,
693:         "if(!window.__pixelelatedBackKey){window.__pixelelatedBackKey=true;"
694:         "window.addEventListener('keydown',function(e){"
695:         "if(e.key!=='Backspace'||e.defaultPrevented||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;"
696:         "var t=e.target;if(t&&(t.isContentEditable||(t.closest&&t.closest('input,textarea,select'))))return;"
697:         "e.preventDefault();history.back();});}",
698:         -1, NULL, NULL, NULL, NULL, NULL);
699: 
700:     /* Every page starts at the top. A provider's sign-in runs several steps
701:      * through one window, and arriving at the next one already scrolled --
702:      * because the last one was scrolled to reach a button below the fold --
703:      * puts the player somewhere in the middle of a page they have not seen
704:      * the start of. */
705:     webkit_web_view_evaluate_javascript(view, "window.scrollTo(0, 0);", -1,
706:                                         NULL, NULL, NULL, NULL, NULL);
707: 
708:     /* Say which page this is, for the phone. Whatever is half-typed in the
709:      * box over there belongs to the field on the page that was showing when
710:      * it was typed; once the provider moves on, it is text about nothing.
711:      * A file rather than a socket because the only reader is cloud_oauth,
712:      * which is already watching this directory. */
713:     const char *page_file = g_getenv("CLOUD_SIGNIN_PAGE_FILE");
714:     const char *uri = webkit_web_view_get_uri(view);
715:     if (page_file && uri && page_worth_recording(uri)) {
716:         /* A new page has nothing with the caret yet. The last page's field
717:          * record goes first, so the phone never reads this page's name
718:          * beside that page's caret (claude G2-C-01); the probe writes a new
719:          * one when a field here has it. */
720:         const char *field_file = g_getenv("CLOUD_SIGNIN_FIELD_FILE");
721:         if (field_file)
722:             g_remove(field_file);
723:         if (data)
724:             ((Osk *) data)->field_recorded = FALSE;
725:         GError *werr = NULL;
726:         if (!g_file_set_contents(page_file, uri, -1, &werr)) {
727:             if (werr) {
728:                 g_message("could not record the page: %s", werr->message);
729:                 g_error_free(werr);
730:             }
731:         }
732:     }
733: 
734:     gtk_widget_grab_focus(GTK_WIDGET(view));
735: 
736:     /* Focusing the widget is not enough: the page itself has to have an
737:      * element focused or the characters go nowhere, which is exactly what a
738:      * broken keyboard looks like. Putting the cursor in the first real field
739:      * is also what somebody would expect on opening a sign-in page -- they
740:      * should be able to start typing without hunting for the box, whether
741:      * they are typing on the handheld or from their phone.
742:      *
743:      * Skipped for hidden, disabled and consent-banner fields, and the page is
744:      * left alone if it has already focused something itself. */
745:     /* Poll from inside the page rather than focusing once. LOAD_FINISHED
746:      * fires when the document is done, but a provider's sign-in form is
747:      * rendered by script after that -- so a single querySelector at load
748:      * time finds nothing, focuses nothing, and every keystroke afterwards
749:      * goes into a page with no cursor in it. That looked exactly like a
750:      * broken keyboard and cost a debugging session.
751:      *
752:      * Gives up after ten seconds so a page that genuinely has no field does
753:      * not keep a timer alive for the life of the window.
754:      *
755:      * "Left alone" means anything but the body holding the focus. It used to
756:      * mean only a text field, so a control the player had just reached -- a
757:      * consent banner's Accept, with Y -- lost the focus to the first field
758:      * the moment a script-rendered form appeared, and the next A submitted
759:      * an empty form (#308 claude F-RS-17). */
760:     static const char *focus_first =
761:         "(function poll(n) {"
762:         "  var a = document.activeElement;"
763:         "  if (a && a !== document.body && a !== document.documentElement) return;"
764:         "  var f = document.querySelector("
765:         "    'input[type=email],input[type=text],input[type=password],"
766:         "     input:not([type]),input[type=tel]');"
767:         "  if (f && f.offsetParent !== null && !f.disabled) { f.focus(); return; }"
768:         "  if (n > 0) setTimeout(function () { poll(n - 1); }, 500);"
769:         "})(20);";
770:     g_message("load finished, asking the page for a field to focus");
771:     webkit_web_view_evaluate_javascript(view, focus_first, -1, NULL, NULL,
772:                                         NULL, NULL, NULL);
773: 
774:     /* This poll does two jobs. It raises the keyboard when the caret lands in
775:      * a text field, and under CLOUD_SIGNIN_DEBUG it reports what the page
776:      * actually holds rather than what it looks like it holds -- keystroke
777:      * delivery has three places it can fail silently, and a screenshot only
778:      * shows the last one, since an empty box looks identical whether nothing
779:      * arrived, something arrived and was rejected, or the caret is in a
780:      * different element than the one drawing a focus ring. Two earlier
781:      * attempts at that reported through document.title, which never reaches
782:      * the compositor without a notify::title handler and so said nothing at
783:      * all. Asking the page and printing the answer is what settled it.
784:      *
785:      * A page can finish loading several times (a redirect, a form post), so
786:      * the timer is started once rather than once per load. */
787:     static gboolean probing = FALSE;
788:     if (data && !probing) {
789:         probing = TRUE;
790:         g_timeout_add(500, probe_tick, data);
791:     }
792: }
793: 
794: static gboolean on_decide_policy(WebKitWebView *view,
795:                                  WebKitPolicyDecision *decision,
796:                                  WebKitPolicyDecisionType type,
797:                                  gpointer data)
798: {
799:     if (type != WEBKIT_POLICY_DECISION_TYPE_NAVIGATION_ACTION)
800:         return FALSE;
801: 
802:     WebKitNavigationAction *action =
803:         webkit_navigation_policy_decision_get_navigation_action(
804:             WEBKIT_NAVIGATION_POLICY_DECISION(decision));
805:     WebKitURIRequest *request = webkit_navigation_action_get_request(action);
806:     const char *uri = webkit_uri_request_get_uri(request);
807: 
808:     g_autoptr(GUri) parsed = g_uri_parse(uri, G_URI_FLAGS_NONE, NULL);
809:     if (!parsed)
810:         return FALSE;
811: 
812:     /* Only network navigation is filtered. about:, data: and blob: have no
813:      * host and are not somewhere the player could be led -- they are how a
814:      * page builds its own subframes and documents. Refusing them broke the
815:      * provider's form from the inside: the log filled with "refused
816:      * navigation to about:srcdoc" while keystrokes arrived at GTK correctly
817:      * and landed nowhere, which reads as a broken keyboard and is not one.
818:      *
819:      * The point of this policy is that a sign-in window cannot become a way
820:      * to browse the web. That is about http(s) going somewhere else, and
821:      * nothing else. */
822:     const char *scheme = g_uri_get_scheme(parsed);
823:     if (g_strcmp0(scheme, "http") != 0 && g_strcmp0(scheme, "https") != 0)
824:         return FALSE;
825: 
826:     /* Only where the *player* would end up, not what the page loads.
827:      *
828:      * A sign-in page is assembled from other origins by design: Dropbox's
829:      * form needs dropboxcaptcha.com, the "Continue with Google" button needs
830:      * accounts.google.com. Filtering those refused the captcha, the form
831:      * never became usable, and keystrokes that arrived correctly all the way
832:      * to WebKit went nowhere -- which looked like a broken keyboard through
833:      * four wrong diagnoses.
834:      *
835:      * What this is actually for is stopping the window becoming a way to
836:      * browse the web: the player following Terms, or Privacy, and never
837:      * coming back. That is a top-level navigation, and it is the only thing
838:      * worth refusing. Subframes and resources load freely; the ephemeral
839:      * context means none of it outlives the sign-in.
840:      */
841:     /* A user gesture is the thing worth filtering: the player tapping Terms
842:      * or Privacy and browsing away. Everything a page loads for itself --
843:      * dropboxcaptcha.com for the form's captcha, accounts.google.com for the
844:      * "Continue with Google" button, analytics nobody asked for -- arrives
845:      * without one.
846:      *
847:      * Not frame_name: an iframe with no name attribute reports NULL exactly
848:      * as the main frame does, so that test refused the captcha anyway and
849:      * the form stayed unusable.
850:      */
851:     if (!webkit_navigation_action_is_user_gesture(action))
852:         return FALSE;
853: 
854:     const char *host = g_uri_get_host(parsed);
855:     if (!host_permitted(host)) {
856:         g_message("refused navigation to host %s", host ? host : "(none)");
857:         webkit_policy_decision_ignore(decision);
858:         return TRUE;
859:     }
860:     return FALSE;
861: }
862: 
863: /* OAuth providers can open a related window and send a result to opener.
864:  * Keep that relationship, but show only one authentication surface at a time
865:  * in the existing window. No extra tabs, address bar, or general browsing. */
866: static void on_auth_close(WebKitWebView *view, gpointer data)
867: {
868:     Osk *osk = data;
869:     GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
870:     WebKitWebView *parent = g_object_get_data(G_OBJECT(view), "auth-parent");
871:     if (!parent || !stack)
872:         return;
873:     osk->view = parent;
874:     g_object_set_data(G_OBJECT(stack), "auth-popup", NULL);
875:     gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(parent));
876:     gtk_widget_grab_focus(GTK_WIDGET(parent));
877:     on_load_changed(parent, WEBKIT_LOAD_FINISHED, osk);
878:     gtk_widget_destroy(GTK_WIDGET(view));
879: }
880: 
881: static void on_auth_ready(WebKitWebView *view, gpointer data)
882: {
883:     Osk *osk = data;
884:     GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
885:     osk->view = view;
886:     gtk_widget_show(GTK_WIDGET(view));
887:     gtk_stack_set_visible_child(GTK_STACK(stack), GTK_WIDGET(view));
888:     gtk_revealer_set_reveal_child(GTK_REVEALER(osk->revealer), FALSE);
889:     gtk_widget_grab_focus(GTK_WIDGET(view));
890: }
891: 
892: static GtkWidget *on_auth_create(WebKitWebView *view,
893:                                  WebKitNavigationAction *action, gpointer data)
894: {
895:     GtkWidget *stack = g_object_get_data(G_OBJECT(view), "stack");
896:     const char *uri = webkit_uri_request_get_uri(webkit_navigation_action_get_request(action));
897:     g_autoptr(GUri) parsed = g_uri_parse(uri, G_URI_FLAGS_NONE, NULL);
898:     if (!stack || g_object_get_data(G_OBJECT(stack), "auth-popup") || !parsed)
899:         return NULL;
900:     const char *scheme = g_uri_get_scheme(parsed);
901:     gboolean network = g_strcmp0(scheme, "https") == 0 || g_strcmp0(scheme, "http") == 0;
902:     gboolean blank = g_strcmp0(uri, "about:blank") == 0 && webkit_navigation_action_is_user_gesture(action);
903:     if ((!network || !host_permitted(g_uri_get_host(parsed))) && !blank)
904:         return NULL;
905:     GtkWidget *popup = webkit_web_view_new_with_related_view(view);
906:     webkit_web_view_set_settings(WEBKIT_WEB_VIEW(popup), webkit_web_view_get_settings(view));
907:     g_object_set_data(G_OBJECT(popup), "stack", stack);
908:     g_object_set_data(G_OBJECT(popup), "auth-parent", view);
909:     g_object_set_data(G_OBJECT(stack), "auth-popup", popup);
910:     g_signal_connect(popup, "decide-policy", G_CALLBACK(on_decide_policy), NULL);
911:     g_signal_connect(popup, "load-changed", G_CALLBACK(on_load_changed), data);
912:     g_signal_connect(popup, "ready-to-show", G_CALLBACK(on_auth_ready), data);
913:     g_signal_connect(popup, "close", G_CALLBACK(on_auth_close), data);
914:     gtk_stack_add_named(GTK_STACK(stack), popup, "auth-popup");
915:     return popup;
916: }
917: 
918: int main(int argc, char **argv)
919: {
920:     if (argc < 2) {
921:         g_printerr("usage: cloud-signin-window <url> [allowed-host]\n");
922:         return 1;
923:     }
924:     /* Which two buttons leave is not the same on every handheld -- the
925:      * RG35XX SP has a Mode button and ES maps its hotkey to it, smaller pads
926:      * have none. cloud_oauth reads the pad and passes what it found, because
927:      * naming a button the player does not have is worse than naming none. */
928:     const char *exit_hint = "SELECT + START";
929:     gboolean auto_raise = TRUE;
930:     for (int i = 2; i < argc; i++) {
931:         if (g_strcmp0(argv[i], "--exit-hint") == 0 && i + 1 < argc)
932:             exit_hint = argv[++i];
933:         else if (g_strcmp0(argv[i], "--no-auto-keyboard") == 0)
934:             auto_raise = FALSE;
935:         else if (!allowed_host && argv[i][0] != '-')
936:             allowed_host = argv[i];
937:     }
938: 
939:     /* WebKitGTK 2.54 renders through its DMABuf path once GStreamer GL is
940:      * built (fork #228), and on a guest with 1 GB -- the handhelds' size --
941:      * that path never finished loading even example.org and left the guest
942:      * unanswering, while 2.52.6 loaded it. With the DMABuf renderer off,
943:      * 2.54 takes the shared-memory path 2.52.6 took: example.org loaded on
944:      * the 1 GB guest with the window at 87 MB and the web process at 35 MB,
945:      * and on 8 GB the three processes came to 285 MB against 666 MB with it
946:      * on (2026-09-25). A sign-in page gains nothing from GPU buffers; the
947:      * memory it keeps is the game's. An environment that sets the variable
948:      * keeps its own value, so the other path stays one export away. */
949:     g_setenv("WEBKIT_DISABLE_DMABUF_RENDERER", "1", FALSE);
950: 
951:     gtk_init(&argc, &argv);
952: 
953:     static Osk osk;
954: 
955:     GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
956:     gtk_window_set_title(GTK_WINDOW(window), "Sign in");
957:     gtk_window_fullscreen(GTK_WINDOW(window));
958:     g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
959: 
960:     /* Ephemeral: nothing this window does should outlive the sign-in. The
961:      * session cookie belongs to the player's provider account, not to the
962:      * handheld, and the next person to open cloud setup starts clean. */
963:     WebKitWebContext *context =
964:         webkit_web_context_new_ephemeral();
965:     WebKitWebView *view =
966:         WEBKIT_WEB_VIEW(webkit_web_view_new_with_context(context));
967: 
968:     /* Spatial navigation: the arrow keys move focus to whatever is in that
969:      * direction, which is what a d-pad means. Tab order on a provider's
970:      * login page wanders through cookie banners and footer links before it
971:      * reaches the password field. */
972:     WebKitSettings *settings = webkit_web_view_get_settings(view);
973:     webkit_settings_set_enable_spatial_navigation(settings, TRUE);
974:     webkit_settings_set_enable_tabs_to_links(settings, TRUE);
975: 
976:     g_signal_connect(view, "decide-policy", G_CALLBACK(on_decide_policy), NULL);
977:     g_signal_connect(view, "load-changed", G_CALLBACK(on_load_changed), &osk);
978:     g_signal_connect(view, "create", G_CALLBACK(on_auth_create), &osk);
979:     g_signal_connect(window, "key-press-event", G_CALLBACK(on_key), &osk);
980: 
981:     /* Something to look at while the provider's page loads. Six seconds of
982:      * a blank screen on a handheld reads as a crash, and the player has no
983:      * other feedback that anything is happening. */
984:     GtkWidget *stack = gtk_stack_new();
985:     GtkWidget *loading = gtk_box_new(GTK_ORIENTATION_VERTICAL, 12);
986:     static Spin spin;
987:     GtkWidget *spinner = gtk_drawing_area_new();
988:     gtk_widget_set_size_request(spinner, 48, 48);
989:     gtk_widget_set_halign(spinner, GTK_ALIGN_CENTER);
990:     g_object_set_data(G_OBJECT(spinner), "spin", &spin);
991:     g_signal_connect(spinner, "draw", G_CALLBACK(on_spin_draw), &spin);
992:     g_timeout_add(60, on_spin_tick, spinner);
993:     gtk_widget_set_valign(loading, GTK_ALIGN_CENTER);
994:     gtk_box_pack_start(GTK_BOX(loading), spinner, FALSE, FALSE, 0);
995:     gtk_box_pack_start(GTK_BOX(loading),
996:                        gtk_label_new("Opening the sign-in page\u2026"),
997:                        FALSE, FALSE, 0);
998:     gtk_stack_add_named(GTK_STACK(stack), loading, "loading");
999:     gtk_stack_add_named(GTK_STACK(stack), GTK_WIDGET(view), "page");
1000:     gtk_stack_set_visible_child_name(GTK_STACK(stack), "loading");
1001:     g_object_set_data(G_OBJECT(view), "stack", stack);
1002: 
1003:     /* Page on top, keyboard underneath it when asked for. A revealer rather
1004:      * than show/hide so the page resizes around it instead of being covered:
1005:      * a keyboard over the field you are typing into is worse than no
1006:      * keyboard. */
1007:     GtkCssProvider *css = gtk_css_provider_new();
1008:     gtk_css_provider_load_from_data(css, OSK_CSS, -1, NULL);
1009:     gtk_style_context_add_provider_for_screen(gdk_screen_get_default(),
1010:                                               GTK_STYLE_PROVIDER(css),
1011:                                               GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);
1012:     g_object_unref(css);
1013: 
1014:     osk.view = view;
1015:     osk.exit_hint = exit_hint;
1016:     osk.auto_raise = auto_raise;
1017:     osk.revealer = gtk_revealer_new();
1018:     gtk_revealer_set_transition_type(GTK_REVEALER(osk.revealer),
1019:                                      GTK_REVEALER_TRANSITION_TYPE_SLIDE_UP);
1020:     gtk_container_add(GTK_CONTAINER(osk.revealer), osk_build(&osk));
1021:     gtk_revealer_set_reveal_child(GTK_REVEALER(osk.revealer), FALSE);
1022: 
1023:     /* The player arrives here from a menu, with no way to find out what the
1024:      * buttons do -- the page is the provider's and says nothing about a
1025:      * handheld. Every other screen on this device carries a help bar; this
1026:      * is that. It is also the answer to "nothing brings up the keyboard":
1027:      * the keyboard raises itself on a text field, and this says how to ask
1028:      * for it the rest of the time. */
1029:     GtkWidget *hints = gtk_label_new("");
1030:     gtk_widget_set_name(hints, "hints");
1031:     gtk_label_set_xalign(GTK_LABEL(hints), 0.5f);
1032:     osk.hints = hints;
1033:     osk_hints(&osk);
1034: 
1035:     GtkWidget *outer = gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);
1036:     gtk_box_pack_start(GTK_BOX(outer), stack, TRUE, TRUE, 0);
1037:     gtk_box_pack_start(GTK_BOX(outer), osk.revealer, FALSE, FALSE, 0);
1038:     gtk_box_pack_start(GTK_BOX(outer), hints, FALSE, FALSE, 0);
1039: 
1040:     gtk_container_add(GTK_CONTAINER(window), outer);
1041:     gtk_widget_set_can_focus(GTK_WIDGET(view), TRUE);
1042:     webkit_web_view_load_uri(view, argv[1]);
1043:     gtk_widget_show_all(window);
1044: 
1045:     /* present, then focus: the window has to be mapped and activated before
1046:      * the widget inside it can take keyboard focus. */
1047:     gtk_window_present(GTK_WINDOW(window));
1048:     gtk_widget_grab_focus(GTK_WIDGET(view));
1049: 
1050:     gtk_main();
1051:     return 0;
1052: }



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_backup


## Original lines 420–490
420: # One cloud transfer at a time, whoever asked for it.
421: #
422: # Three callers can start one: EmulationStation at boot (the startup sync,
423: # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
424: # after a game exits, and a person in the menu. Until
425: # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
426: # into ES kept the visible progress and dropped the guard, so exiting a game
427: # during the boot sync started a second rclone against the same remote. Two
428: # writers on one folder is how a mirror deleted another handheld's saves
429: # (D-CLOUD-014); two copies racing is milder, and still nothing anybody asked
430: # for.
431: #
432: # The lock lives here, in the script, so no caller has to know about the
433: # others. /var/run is tmpfs, so a lock cannot survive a reboot and go stale.
434: # Non-blocking, because a request that queues silently behind a twenty-minute
435: # transfer looks exactly like one that hung. Exit EXIT_LOCK_HELD (75) means
436: # "skipped: another sync is running" -- the UI names it, and no last-run stamp
437: # is written for work that did not happen.
438: #
439: # The descriptor is this shell's and nothing else's. A shell redirection
440: # carries no close-on-exec, so `exec 9>` hands fd 9 to every child the
441: # script starts, and rclone then holds the lock for the whole of a transfer
442: # (watched in /proc on the VM, #124). While the script outlives its
443: # children that is invisible, because bash waits for each of them before it
444: # exits. The moment it does not -- killed or orphaned while rclone is still
445: # copying, a child left in the background -- the lock outlives the run that
446: # took it and every sync afterwards is refused with "another cloud sync is
447: # running" when nothing is running at all. So the body runs with fd 9
448: # closed ("9>&-"): bash keeps the lock on a descriptor of its own, which it
449: # does mark close-on-exec, and nothing this script starts can see it.
450: #
451: # The refusal also waits a moment before saying no, as belt and braces for
452: # a holder this script does not own: a descriptor leaked by an older build,
453: # or a process in the act of exiting, frees itself in milliseconds, while a
454: # real concurrent transfer does not. One second of patience turns a raced
455: # skip into a run that works and costs a genuinely blocked run one second.
456: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
457: take_cloud_lock() {
458:     local tries=0
459:     exec 9>"${CLOUD_SYNC_LOCK}"
460:     while ! flock -n 9; do
461:         if [ "${tries}" -ge 4 ]; then
462:             echo "Skipped: another cloud sync is already running. Try again when it's done."
463:             log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}" "false"
464:             exit "${EXIT_LOCK_HELD}"
465:         fi
466:         tries=$((tries + 1))
467:         sleep 0.25
468:     done
469: }
470: 
471: # The shared explicit selection, with legacy first-name behavior only when
472: # the sidecar is absent. Empty or missing selected names never fall back to
473: # another account (D-CLOUD-184). Keep the internal function name for callers.
474: first_remote() {
475:     "$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null
476: }
477: 
478: # Does the remote compare files by size alone? rclone decides equality by
479: # size, then modtime, then hash. Plain WebDAV supports neither modification
480: # times nor hashes; rclone supports both only on Fastmail Files, ownCloud
481: # (and its Infinite Scale), Nextcloud and its own serve (rclone.org/webdav,
482: # "Modification times and hashes"; the vendor names from `rclone help
483: # backend webdav`). On every other WebDAV vendor -- SharePoint, `other`,
484: # none -- the modtime is "not supported" and never consulted, so two files
485: # of one size are equal to it whatever their bytes: a battery save, the
486: # same size every time it is written, never moved again after its first
487: # upload (#315, D-CLOUD-153; measured on 8196071ff5, `Sizes identical` at
488: # -vv, `backend features` Precision 3153600000000000000, Hashes []). A
489: # crypt or alias remote over such a WebDAV inherits it, so one hop through
490: # its `remote =` is followed (audit of the fix, F-SS-04). Read from the

## Original lines 2310–2470
2310:         fi
2311: 
2312:         # Keep a bounded history of THIS device's archives. Names lead with
2313:         # the date, so sorting them is ordering them by age and no metadata
2314:         # call is needed.
2315:         #
2316:         # After the size check, not before it. Until 2026-09-10 this ran on
2317:         # the strength of an upload not yet proven whole, so the previous
2318:         # records went while the new one might be short -- obligation (3)
2319:         # before obligation (1) (D-CLOUD-078, #105). The check above sets
2320:         # BACKUP_SYSTEM_STATUS to 1 when the bytes do not match, and this
2321:         # then does nothing.
2322:         #
2323:         # Where this runs: device_dest is SETTINGS_REMOTE/<device id>/, the
2324:         # folder cloud_device_id names this device (Anbernic-RG-SP-f058e3e9e8).
2325:         # A folder this device wrote under a healed-away id (#86) is not
2326:         # device_dest and nothing here reaches it either.
2327:         # A different device's own archives are in a different folder, and
2328:         # nothing here reaches them. Within this folder, the newest
2329:         # CLOUD_BACKUP_KEEP archives carrying this device's label
2330:         # (<stamp>-<label>-ROCKNIX_SETTINGS.tar.gz) are kept and the rest of
2331:         # those removed. An archive carrying no label -- every one from before
2332:         # names carried a device: ROCKNIX_SETTINGS, ROCKNIX_BACKUP, the
2333:         # undated zip -- or another device's label is left alone. Until
2334:         # 2026-09-08 the newest CLOUD_BACKUP_KEEP of everything here survived
2335:         # and the rest went, so one device's backup could evict another's.
2336:         #
2337:         # An archive carrying this device's label but made by another device
2338:         # can be in this folder in exactly two ways, and is counted with this
2339:         # device's own in both, because the label cannot tell them apart: it
2340:         # was restored here from that device's folder and sent up again by the
2341:         # loop above (the fresh-device journey, #26); or the two devices share
2342:         # an id and so share this folder (a cloned id, fork #86 -- the RG SP
2343:         # and the RG35XX SP shared the hash ee5013fc56, the constant a
2344:         # sit-tunnel kernel produced, until cloud_device_id healed it on
2345:         # 2026-09-08; two devices of one model on a build from before that
2346:         # still do). The id is deliberately not in the archive name.
2347:         #
2348:         # The unlabelled ones are bounded: the older rule had already trimmed
2349:         # them to CLOUD_BACKUP_KEEP, and no new ones are written, so they cost
2350:         # at most that many archives per folder until the owner removes them.
2351:         # Deleting what cannot be attributed is the failure this exists to
2352:         # stop, so the guard fails closed: no label, no deletion.
2353:         if [ ${BACKUP_SYSTEM_STATUS} -eq 0 ] && [ ${sent_any} -eq 1 ]; then
2354:             local keep="${CLOUD_BACKUP_KEEP:-3}"
2355:             case "${keep}" in
2356:                 ''|*[!0-9]*) keep=3 ;;
2357:             esac
2358:             local label
2359:             label=$(device_label)
2360:             if [ -z "${label}" ]; then
2361:                 log_message "Cannot tell this device's archives from another device's (cloud_device_id gave no name); nothing removed from ${device_dest}" "false" "WARN"
2362:             else
2363:                 local osn listing mine total_n mine_n old_archive
2364:                 osn=$(os_name)
2365:                 listing=$(rclone lsf --files-only --include "*.{zip,tar.gz}" "${device_dest}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null)
2366:                 mine=$(printf '%s\n' "${listing}" \
2367:                        | grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" | sort -r)
2368:                 total_n=$(printf '%s\n' "${listing}" | grep -c .)
2369:                 mine_n=$(printf '%s\n' "${mine}" | grep -c .)
2370:                 if [ "${total_n}" -gt "${mine_n}" ]; then
2371:                     log_message "Leaving $((total_n - mine_n)) archive(s) not named for this device (${label}) alone in ${device_dest}" "false"
2372:                 fi
2373:                 # The archives this run uploaded are kept by name, whatever
2374:                 # the others' names say: a date is the clock of the device
2375:                 # that wrote it, and three archives stamped by a clock that
2376:                 # ran ahead used to leave this run's upload as the one past
2377:                 # the count (audit #307 PL-021). The rest are kept by count,
2378:                 # newest name first, to CLOUD_BACKUP_KEEP in all.
2379:                 local others left
2380:                 others=$(printf '%s\n' "${mine}" | grep -v '^$' | grep -vxF -f <(printf '%s\n' "${uploaded_names[@]}"))
2381:                 left=$(( keep - ${#uploaded_names[@]} )); [ "${left}" -ge 0 ] || left=0
2382:                 printf '%s\n' "${others}" | grep -v '^$' | tail -n +$((left + 1)) | while read -r old_archive
2383:                 do
2384:                     [ -n "${old_archive}" ] || continue
2385:                     log_message "Removing old cloud backup ${old_archive}" "false"
2386:                     rclone deletefile "${device_dest}/${old_archive}" "${RCLONE_NET_OPTS_ARRAY[@]}" 2>/dev/null
2387:                 done
2388:             fi
2389:         fi
2390: 
2391:         return $BACKUP_SYSTEM_STATUS
2392:     else
2393:         log_message "Backing up settings to the cloud is turned off, so it was skipped." "true"
2394:         BACKUP_SYSTEM_STATUS=0
2395:     fi
2396:     
2397:     return $BACKUP_SYSTEM_STATUS
2398: }
2399: 
2400: # Main script execution
2401: # The follow check that ran here before every sync (D-CLOUD-160's "your
2402: # other devices will follow") is the cloud folder step's now, which runs
2403: # where the player first meets the cloud -- the end of cloud setup, and the
2404: # first boot of this build on a device linked to an earlier folder -- and on
2405: # the transfer pages' scan (D-CLOUD-170, #363). Every sync paid for it before.
2406: 
2407: main() {
2408:     check_network_link
2409:     check_rclone_config
2410:     load_config
2411:     # backup_game_saves proves the remote reachable with the mkdir it needs
2412:     # anyway; only the system-only path has no such step of its own. After
2413:     # load_config, which sets an automatic run's deadline: the probe ran
2414:     # before it, outside the ceiling (#308 gpt F-CS-34).
2415:     
2416:     # An existing config file can contain no remote (#392). Without the
2417:     # prefix, rclone interprets SAVES_REMOTE as a local path. Refuse before
2418:     # any path operation instead of offering to create a "cloud" locally.
2419:     REMOTENAME=$(first_remote)
2420:     case "${REMOTENAME}" in
2421:         ?*:) ;;
2422:         *) log_message "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first." "true" "ERROR"
2423:            say_why "YOUR CLOUD STORAGE ISN'T SET UP YET"
2424:            clean_exit 1 ;;
2425:     esac
2426:     [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
2427:     
2428:     # Begin main script operations with user-friendly header
2429:     log_message "=> ${OS_NAME} CLOUD BACKUP\n"
2430:     
2431:     # Execute Part 1: Game saves backup
2432:     # This performs the primary save file backup operation using the configured method
2433:     if [ "${SYSTEM_ONLY}" -eq 1 ]; then
2434:         log_message "Skipped game saves this time - settings only." "true"
2435:         SAVES_OUTCOME="SKIPPED - SETTINGS ONLY"
2436:         BACKUP_STATUS=0
2437:     else
2438:         backup_game_saves
2439:         BACKUP_STATUS=$?
2440:     fi
2441:     
2442:     # Add a pause for better visual separation between operations
2443:     pause 2
2444:     
2445:     # Execute Part 2: Settings backup file transfer
2446:     # This backs up settings backup files (zip files) if enabled in configuration
2447:     if [ "${SAVES_ONLY}" -eq 1 ]; then
2448:         log_message "Skipped settings this time - saves only." "true"
2449:         SETTINGS_OUTCOME="SKIPPED - SAVES ONLY"
2450:         BACKUP_SYSTEM_STATUS=0
2451:     else
2452:         backup_system_files
2453:         BACKUP_SYSTEM_STATUS=$?
2454:     fi
2455:     
2456:     # Add a pause before summary
2457:     pause 2
2458:     
2459:     # Add a line break for better visual separation
2460:     echo
2461:     
2462:     # The run's exit, decided by both phases (the note below the summary
2463:     # says why); computed here because the outcome line reads it.
2464:     # rclone's 9 -- nothing needed moving -- is a completion wherever a
2465:     # phase is judged (outcome_word, run_outcome_line), so it is here too: a
2466:     # saves phase that returned 9 used to keep a settings phase's failure
2467:     # out of the exit and the stamp, and the run said Completed. over an
2468:     # archive that never moved (audit #307 PL-028).
2469:     local overall=${BACKUP_STATUS}
2470:     case "${overall}" in



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_connections.py


## Original lines 1–243
1: # SPDX-License-Identifier: GPL-2.0
2: # Copyright (C) 2026 pixelelated
3: """Local connection transactions. No cloud mutations; only bounded listings.
4: 
5: One active connection is persisted separately from credentials. Missing selection
6: preserves the legacy first remote; an explicit empty selection never falls back.
7: All writers share the transfer lock. New credentials are verified in a private
8: config and only then installed; failed/cancelled attempts leave old bytes intact.
9: """
10: import configparser
11: import contextlib
12: import fcntl
13: import os
14: from pathlib import Path
15: import re
16: import subprocess
17: import tempfile
18: 
19: RCLONE = '/usr/bin/rclone'
20: CONFIG = Path('/storage/.config/rclone/rclone.conf')
21: ACTIVE = CONFIG.with_name('active-connection')
22: LOCK = Path('/var/run/cloud_sync.lock')
23: SYSTEM = Path('/storage/.config/system/configs/system.cfg')
24: 
25: class Refused(Exception):
26:     pass
27: 
28: 
29: def read_config(path= None):
30:     path = CONFIG if path is None else path
31:     raw = path.read_bytes() if path.exists() else b''
32:     parser = configparser.RawConfigParser(strict=True)
33:     parser.optionxform = str
34:     try:
35:         parser.read_string(raw.decode('utf-8'))
36:     except (UnicodeError, configparser.Error):
37:         # rclone can read encrypted configurations using its normal password
38:         # mechanism. Keep that existing capability; never echo the dump.
39:         import json
40:         try:
41:             result = subprocess.run([RCLONE, '--config', str(path), 'config', 'dump'],
42:                                     capture_output=True, text=True, timeout=8)
43:             if result.returncode:
44:                 raise ValueError()
45:             data = json.loads(result.stdout)
46:             parser = configparser.RawConfigParser(interpolation=None)
47:             parser.optionxform = str
48:             parser.read_dict(data)
49:         except (ValueError, configparser.Error, subprocess.TimeoutExpired):
50:             raise Refused('Cloud connection settings could not be read.')
51:     return raw, parser
52: 
53: 
54: def active(config=None):
55:     if config is None:
56:         _, config = read_config()
57:     if ACTIVE.exists():
58:         value = ACTIVE.read_text().removesuffix('\n')
59:         if value and not config.has_section(value):
60:             raise Refused('The selected connection is missing. Choose a connection first.')
61:         return value
62:     return next(iter(sorted(config.sections())), '')
63: 
64: 
65: def atomic(path, data):
66:     path.parent.mkdir(parents=True, exist_ok=True)
67:     fd, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
68:     try:
69:         with os.fdopen(fd, 'wb') as handle:
70:             handle.write(data)
71:             handle.flush()
72:             os.fsync(handle.fileno())
73:         os.replace(name, path)
74:         directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
75:         try:
76:             os.fsync(directory)
77:         finally:
78:             os.close(directory)
79:     finally:
80:         if os.path.exists(name):
81:             os.unlink(name)
82: 
83: 
84: def restore_selection(previous, written):
85:     # Only undo our write; never clobber an outside settings writer.
86:     if written is None or not ACTIVE.exists() or ACTIVE.read_bytes() != written:
87:         return
88:     if previous is not None:
89:         atomic(ACTIVE, previous)
90:     else:
91:         ACTIVE.unlink()
92:         directory = os.open(ACTIVE.parent, os.O_RDONLY | os.O_DIRECTORY)
93:         try:
94:             os.fsync(directory)
95:         finally:
96:             os.close(directory)
97: 
98: 
99: @contextlib.contextmanager
100: def locked():
101:     LOCK.parent.mkdir(parents=True, exist_ok=True)
102:     with LOCK.open('a') as handle:
103:         try:
104:             fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
105:         except BlockingIOError:
106:             raise Refused('A cloud operation is running. Wait for it to finish, then try again.')
107:         yield
108: 
109: 
110: def require_manual():
111:     # Same literal keys as ES. Read text, never execute system.cfg.
112:     values = {}
113:     if SYSTEM.exists():
114:         for line in SYSTEM.read_text().splitlines():
115:             key, sep, value = line.partition('=')
116:             if sep:
117:                 values[key.strip()] = value.strip()
118:     if any(values.get(k) == '1' for k in ('cloudsaves.startup', 'cloudsaves.gameexit')):
119:         raise Refused('Turn off both automatic save sync options before changing this connection.')
120: 
121: 
122: def run(args):
123:     try:
124:         result = subprocess.run([RCLONE] + args, capture_output=True, text=True, timeout=40)
125:     except subprocess.TimeoutExpired:
126:         raise Refused('The connection stopped answering. Your settings were not changed.')
127:     if result.returncode:
128:         # Never forward provider diagnostics: they may contain credentials.
129:         raise Refused('The connection could not be verified. Your settings were not changed.')
130:     return result.stdout
131: 
132: 
133: def save(name, backend, settings, replace=False, publish=None):
134:     if not name or name != name.strip() or any(c in name for c in ':[]\r\n\t') or name.startswith('-'):
135:         raise Refused('Give the connection a name without colons or brackets.')
136:     with locked():
137:         existed = CONFIG.exists()
138:         original, config = read_config()
139:         exists = config.has_section(name)
140:         if replace != exists:
141:             raise Refused('Choose a different connection name.' if exists else 'This connection no longer exists.')
142:         if replace:
143:             require_manual()
144:             if config.get(name, 'type', fallback='') != backend:
145:                 raise Refused('The connection provider changed. Open its settings again.')
146:         selected = active(config)
147:         previous_selection = ACTIVE.read_bytes() if ACTIVE.exists() else None
148:         written_selection = None
149:         CONFIG.parent.mkdir(parents=True, exist_ok=True)
150:         with tempfile.TemporaryDirectory(prefix='.connection-', dir=CONFIG.parent) as directory:
151:             staged = Path(directory) / 'rclone.conf'
152:             staged.write_bytes(original)
153:             staged.chmod(0o600)
154:             args = ['--config', str(staged), 'config', 'update' if replace else 'create', name]
155:             if not replace:
156:                 args.append(backend)
157:             args.extend('%s=%s' % pair for pair in settings)
158:             args += ['--non-interactive', '--obscure']
159:             out = run(args)
160:             import json
161:             try:
162:                 answer = json.loads(out or '{}')
163:             except ValueError:
164:                 answer = {}
165:             if isinstance(answer, dict) and answer.get('State'):
166:                 raise Refused('This provider needs additional setup. Use a computer to finish connecting it.')
167:             run(['--config', str(staged), 'lsd', name + ':', '--contimeout', '10s', '--timeout', '20s', '--low-level-retries', '1', '--retries', '1'])
168:             updated, result = read_config(staged)
169:             if not result.has_section(name):
170:                 raise Refused('The connection was not saved.')
171: 
172:             def commit():
173:                 nonlocal written_selection
174:                 # Refuse an outside writer instead of overwriting its update.
175:                 current = CONFIG.read_bytes() if CONFIG.exists() else b''
176:                 if current != original:
177:                     raise Refused('Cloud settings changed during sign-in. Try again.')
178:                 # Pin the old selection BEFORE making another name visible.
179:                 # On a first connection the legacy fallback selects only it.
180:                 if not ACTIVE.exists() and config.sections():
181:                     written_selection = (selected + '\n').encode()
182:                     atomic(ACTIVE, written_selection)
183:                 atomic(CONFIG, updated)
184: 
185:             try:
186:                 if publish:
187:                     publish(commit)
188:                 else:
189:                     commit()
190:             except Exception:
191:                 # A failed success-record write must not install credentials
192:                 # that the interface reports as unsaved.
193:                 if CONFIG.exists() and CONFIG.read_bytes() == updated:
194:                     if existed:
195:                         atomic(CONFIG, original)
196:                     else:
197:                         CONFIG.unlink()
198:                 restore_selection(previous_selection, written_selection)
199:                 raise
200:     return name
201: 
202: 
203: def select(name):
204:     with locked():
205:         require_manual()
206:         _, config = read_config()
207:         if not config.has_section(name):
208:             raise Refused('This connection no longer exists.')
209:         atomic(ACTIVE, (name + '\n').encode())
210: 
211: 
212: def remove(name):
213:     with locked():
214:         require_manual()
215:         original, config = read_config()
216:         if not config.has_section(name):
217:             raise Refused('This connection no longer exists.')
218:         # Removing a wrapper's underlying connection would break the wrapper.
219:         for other in config.sections():
220:             if other != name and any(re.search(r'(?<![\w.-])' + re.escape(name) + ':', v) for _, v in config.items(other)):
221:                 raise Refused('Another connection uses this one. Change that connection first.')
222:         selected = active(config)
223:         with tempfile.TemporaryDirectory(prefix='.connection-', dir=CONFIG.parent) as directory:
224:             staged = Path(directory) / 'rclone.conf'
225:             staged.write_bytes(original)
226:             staged.chmod(0o600)
227:             run(['--config', str(staged), 'config', 'delete', name])
228:             updated, result = read_config(staged)
229:             if result.has_section(name):
230:                 raise Refused('The connection settings could not be changed safely.')
231:         if CONFIG.read_bytes() != original:
232:             raise Refused('Cloud settings changed. Open this page again.')
233:         # Empty selection is a tombstone: never silently use another account.
234:         previous_selection = ACTIVE.read_bytes() if ACTIVE.exists() else None
235:         written_selection = (('' if selected == name else selected) + '\n').encode()
236:         try:
237:             atomic(ACTIVE, written_selection)
238:             atomic(CONFIG, updated)
239:         except Exception:
240:             if CONFIG.exists() and CONFIG.read_bytes() == updated:
241:                 atomic(CONFIG, original)
242:             restore_selection(previous_selection, written_selection)
243:             raise



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_backup


## Original lines 1–786
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_content_backup - push game content (ROMs, BIOS, ...) to the cloud.
6: #
7: # Mirror of cloud_content_restore: an explicit, user-initiated copy of chosen
8: # local directories from /storage/roms to the cloud content root. Copy-only -
9: # it never deletes anything on the remote. Save/state/screenshot directories
10: # are excluded here; they travel via the saves sync.
11: #
12: # Usage:
13: #   cloud_content_backup --list           print local content directories
14: #   cloud_content_backup --list-sizes     print them as name|bytes
15: #   cloud_content_backup <dir> [<dir>..]  copy local dirs to the cloud
16: #   cloud_content_backup --all            copy all local content directories
17: #
18: # The remote content root defaults to the remote's root; set CONTENT_REMOTE in
19: # /storage/.config/cloud_sync.conf to point somewhere else (e.g. "GAMES").
20: 
21: . /etc/profile
22: 
23: LOG_FILE="/var/log/cloud_sync.log"
24: SCRIPT_NAME=$(basename "$0")
25: DEST="/storage/roms"
26: 
27: # The exit that means "nothing ran: another cloud sync holds the lock", which
28: # EmulationStation names (SKIPPED - ANOTHER CLOUD SYNC IS RUNNING). It was 3
29: # until 2026-09-09, which is also rclone's "directory not found", so a failed
30: # unit carrying rclone's code to the final exit read as a sync that was never
31: # running (#99, blindspot 33). sysexits.h's EX_TEMPFAIL sits above everything
32: # rclone returns (0-9) and below the 128+signal range, so nothing this script
33: # forwards can produce it. The same two numbers (75, and 69 for no network --
34: # raised here when the link goes away under a running unit, see
35: # stop_no_network) are what EmulationStation reads; scripts and ES ship
36: # together.
37: readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
38: 
39: log_message() {
40:     echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO] [${SCRIPT_NAME}] ${1}" >> ${LOG_FILE}
41: }
42: 
43: # One cloud transfer at a time, whoever asked for it.
44: #
45: # Three callers can start one: EmulationStation at boot (the startup sync,
46: # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
47: # after a game exits, and a person in the menu. Until
48: # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
49: # into ES kept the visible progress and dropped the guard, so exiting a game
50: # during the boot sync started a second rclone against the same remote. Two
51: # writers on one folder is how a mirror deleted another handheld's saves
52: # (D-CLOUD-014); two copies racing is milder, and still nothing anybody asked
53: # for.
54: #
55: # The lock lives here, in the script, so no caller has to know about the
56: # others. /var/run is tmpfs, so a lock cannot survive a reboot and go stale.
57: # Non-blocking, because a request that queues silently behind a twenty-minute
58: # transfer looks exactly like one that hung. Exit EXIT_LOCK_HELD (75) means
59: # "skipped: another sync is running" -- the UI names it, and no last-run stamp
60: # is written for work that did not happen.
61: #
62: # The descriptor is this shell's and nothing else's. A shell redirection
63: # carries no close-on-exec, so `exec 9>` hands fd 9 to every child the
64: # script starts, and rclone then holds the lock for the whole of a transfer
65: # (watched in /proc on the VM, #124). While the script outlives its
66: # children that is invisible, because bash waits for each of them before it
67: # exits. The moment it does not -- killed or orphaned while rclone is still
68: # copying, a child left in the background -- the lock outlives the run that
69: # took it and every sync afterwards is refused with "another cloud sync is
70: # running" when nothing is running at all. So the body runs with fd 9
71: # closed ("9>&-"): bash keeps the lock on a descriptor of its own, which it
72: # does mark close-on-exec, and nothing this script starts can see it.
73: #
74: # The refusal also waits a moment before saying no, as belt and braces for
75: # a holder this script does not own: a descriptor leaked by an older build,
76: # or a process in the act of exiting, frees itself in milliseconds, while a
77: # real concurrent transfer does not. One second of patience turns a raced
78: # skip into a run that works and costs a genuinely blocked run one second.
79: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
80: take_cloud_lock() {
81:     local tries=0
82:     exec 9>"${CLOUD_SYNC_LOCK}"
83:     while ! flock -n 9; do
84:         if [ "${tries}" -ge 4 ]; then
85:             echo "Skipped: another cloud sync is already running. Try again when it's done."
86:             log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}"
87:             exit "${EXIT_LOCK_HELD}"
88:         fi
89:         tries=$((tries + 1))
90:         sleep 0.25
91:     done
92: }
93: 
94: if [ ! -e "/storage/.config/rclone/rclone.conf" ]; then
95:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
96:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
97:     exit 1
98: fi
99: 
100: # The two values this script needs from cloud_sync.conf, read as text and
101: # never sourced (audit #307 PL-051's script half): a folder value an earlier
102: # build wrote with "$(...)" in it ran on every `source`. A CONTENT_REMOTE
103: # that carries a $, a backtick, a backslash or a control character is not a
104: # folder name, and the run refuses it rather than use it as a path.
105: #
106: # Read in the forms `source` reads (the audit of the fixes, G-A-06/G-A-02):
107: # the value double quoted, single quoted or bare; after it nothing, or
108: # blanks and a # comment. The first cut took only KEY=value or KEY="value"
109: # whole: a trailing comment or single quotes gave an empty CONTENT_REMOTE --
110: # the cloud's root -- where the folder had been, and the backup went there.
111: # A line it cannot read as plain text exits 2, and CONTENT_REMOTE's refuses
112: # the run; nothing is read as the root that did not say the root. Of two
113: # lines for one key, the first: every saves run EmulationStation starts is
114: # --yes, which runs cloud_sync_cleanup_duplicates.sh, which keeps the first,
115: # so that is the value the saves scripts run with and the file is left with.
116: #
117: # And a file with a control character but a tab anywhere in it is
118: # unreadable here as it is to the saves scripts' conf_valid (the audit of
119: # the fix round, PL-002): this reader never sources the file, but a blank
120: # is a space or a tab to both, so the tiers run with one reading of one
121: # file -- a carriage return after a value used to pass here as a blank.
122: #
123: # The key set in a form `source` reads and this does not -- indented,
124: # exported, declared, appended to, or with a blank before the = -- is
125: # unreadable, never absent (the audit of the fix round, lead G2-A-03):
126: # read as absent it was the cloud's root, and a content backup went there.
127: # The saves scripts' conf_valid refuses such a file whole.
128: conf_get() { # <KEY>: its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
129:     [ -f /storage/.config/cloud_sync.conf ] || return 0
130:     awk -v k="$1" '
131:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
132:         index($0, k "=") != 1 && !other \
133:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
134:         index($0, k "=") == 1 {
135:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
136:             c = substr(s, 1, 1)
137:             if (c == "\"") {
138:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
139:                 # character each (PL-015), and so does this; an unescaped $
140:                 # or backtick is an expansion this reader does not make, and
141:                 # any other backslash is refused as conf_valid refuses it.
142:                 n = length(s); i = 2; closed = 0
143:                 while (i <= n) {
144:                     d = substr(s, i, 1)
145:                     if (d == "\"") { closed = 1; break }
146:                     if (d == "\\") {
147:                         e = substr(s, i + 1, 1)
148:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
149:                         ok = 0
150:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
151:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
152:                         break
153:                     }
154:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
155:                     v = v d; i++
156:                 }
157:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
158:                 if (ok) r = substr(s, i + 1)
159:             } else if (c == "'"'"'") {
160:                 j = index(substr(s, 2), c)
161:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
162:             } else {
163:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
164:             }
165:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
166:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
167:         }
168:         END {
169:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
170:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
171:             if (found && !firstok) { print firstwhy; exit 2 }
172:             if (found) print first
173:         }
174:     ' /storage/.config/cloud_sync.conf
175: }
176: if ! CONTENT_REMOTE=$(conf_get CONTENT_REMOTE); then
177:     # On a refusal conf_get says why, for the log: the line and its shape,
178:     # never the value (PL-015).
179:     log_message "cloud_sync.conf was not read: ${CONTENT_REMOTE}"
180:     echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
181:     echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
182:     exit 1
183: fi
184: # The bound falls back to the shipped value below when this is empty; a
185: # line it cannot read is that too, and the log says so.
186: if ! RCLONE_NET_OPTS=$(conf_get RCLONE_NET_OPTS); then
187:     log_message "RCLONE_NET_OPTS was not read (${RCLONE_NET_OPTS}); the shipped bound stands in"
188:     RCLONE_NET_OPTS=""
189: fi
190: case "${CONTENT_REMOTE}" in
191:     *[\$\`\\]*|*[[:cntrl:]]*)
192:         echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
193:         echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
194:         exit 1 ;;
195: esac
196: 
197: REMOTENAME=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active)
198: if [ -z "${REMOTENAME}" ]; then
199:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
200:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
201:     exit 1
202: fi
203: 
204: ROOT="${REMOTENAME}${CONTENT_REMOTE:+${CONTENT_REMOTE}/}"
205: 
206: # The bound on every rclone command below that opens a socket: RCLONE_NET_OPTS
207: # from cloud_sync.conf, or the same shipped values when the config has no
208: # such line yet -- this script reads the config without running
209: # cloud_sync_helper, so on the first run after an update it may not, and the
210: # bound is a guard that a missing line must not switch off. The reasoning
211: # for the numbers is beside the option in cloud_sync.conf.defaults; the
212: # short version is that rclone's own defaults (60 s connect, 5 min idle, 10
213: # low-level retries, 3 whole-run retries) hold a run for over ten minutes
214: # on a link that drops mid-run (#101, #102, #103). Keep the fallback in step
215: # with the default.
216: RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
217: _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
218: [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
219: read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
220: # Installed beside this script, also when the host fixtures copy it.
221: . "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
222: # A probe is a single listing that exists to answer quickly: one attempt,
223: # tighter than the transfers (the same values the saves scripts probe with).
224: readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
225: # A listing's bound (#143): three low-level retries, not a transfer's ten --
226: # rclone's S3 backend hands the count to the AWS SDK as attempts with
227: # exponential backoff (see cloud_backup for the measurement).
228: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
229: 
230: # Whole or not at all: to a temporary name beside the stamp, then renamed
231: # over it, as ThreadedCloudSync::recordOutcome does. A kill mid-write leaves
232: # the previous stamp; it used to leave an empty file (D-CLOUD-078, #105).
233: # LAST_WHY, when a `>>> why` line was printed, becomes the stamp's third
234: # field as a token (spaces to underscores) for the row to read (D-UI-028).
235: LAST_WHY=""
236: write_stamp() {
237:     local file="$1" line="$2" tmp
238:     mkdir -p "$(dirname "${file}")" 2>/dev/null
239:     tmp="${file}.tmp.$$"
240:     { printf '%s\n' "${line}" > "${tmp}"; } 2>/dev/null \
241:         && mv -f "${tmp}" "${file}" 2>/dev/null \
242:         || rm -f "${tmp}" 2>/dev/null
243: }
244: record_outcome() { # <stamp-name> <rc>
245:     local why=""
246:     case "$2" in
247:         0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
248:         *) [ -n "${LAST_WHY}" ] && why=" $(printf '%s' "${LAST_WHY}" | tr ' ' '_')" ;;
249:     esac
250:     write_stamp "/storage/.cache/cloud_sync/last-$1" "$(date +%s) $2${why}"
251: }
252: 
253: # Why a unit did not finish, in the player's words (D-UI-028, D-CLOUD-077):
254: # one `>>> why <SENTENCE>` protocol line per failing unit, which the page
255: # and the card read; rclone's code stays in the log. The sentences are the
256: # vocabulary table's in es-native-ui.md.
257: say_why() {
258:     LAST_WHY="$1"
259:     echo ">>> why $1"
260:     log_message "why: $1"
261: }
262: why_for() {
263:     case "$1" in
264:         3|4) echo "COULDN'T FIND YOUR CLOUD FOLDER" ;;
265:         5|124) echo "YOUR CLOUD STOPPED ANSWERING" ;;
266:         6)   echo "SOME FILES DIDN'T FINISH" ;;
267:         7|8) echo "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
268:         130) echo "IT WAS STOPPED" ;;
269:         *)   echo "SOMETHING WENT WRONG" ;;
270:     esac
271: }
272: 
273: has_default_route() {
274:     ip -4 route show default 2>/dev/null | grep -q . \
275:         || ip -6 route show default 2>/dev/null | grep -q .
276: }
277: 
278: # Is the network gone? Asked after rclone failed, so the run can say why it
279: # ended rather than hand up a code that reads as FAILED and sends somebody
280: # to a log. Gone: no default route, or a route through which neither the
281: # remote nor anything else answers a bounded probe. Not gone: the remote
282: # answers again (a blip rclone did not survive), or the internet answers
283: # while the remote does not (the provider, or the sign-in) -- that is
284: # rclone's failure to report, and the caller passes rclone's code through
285: # as before. The same three questions cloud_backup asks (#101, #103).
286: network_gone() {
287:     has_default_route || return 0
288:     rclone lsd "${REMOTENAME}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1 && return 1
289:     ping -q -c1 -W 3 1.1.1.1 >/dev/null 2>&1 && return 1
290:     ping -q -c1 -W 3 8.8.8.8 >/dev/null 2>&1 && return 1
291:     return 0
292: }
293: 
294: # The network went away under a running unit. Says so, records that the run
295: # did not complete -- never a 0, which would read as a backup that happened
296: # -- and exits EXIT_NO_NETWORK, which EmulationStation names (SKIPPED - NO
297: # NETWORK CONNECTION on the card, SKIPPED, NO NETWORK on the row). No
298: # further unit is attempted: each would stall for another minute against
299: # the same dead link. rclone copy writes each file under a temporary name
300: # and renames it when complete, so nothing partial is left in the cloud.
301: #
302: # SKIPPED means nothing was touched (#308 claude F-CS-24): once a unit has
303: # completed, a run the network then ends stamps "69 gaps <why>", which the
304: # rows read as COULDN'T FINISH; the exit stays 69.
305: # Did this run's rclone move a file since <offset> into the log? Progress,
306: # for the stamp stop_no_network writes, is what rclone logged moving --
307: # "<path>: Copied (...)", "Moved (...)", "Deleted" -- not a unit that
308: # completed (the audit of the fixes, G-A-08/G-A-13): files a unit moved
309: # before its own failure did not count, and a unit that moved nothing did.
310: # Every transfer here logs at INFO to LOG_FILE, and the transfer lock
311: # keeps any other cloud script from writing it meanwhile.
312: log_offset() { stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0; }
313: moved_since() { # <byte offset into LOG_FILE>
314:     local now
315:     now=$(stat -c %s "${LOG_FILE}" 2>/dev/null) || return 1
316:     [ "${now}" -gt "$1" ] 2>/dev/null || return 1
317:     tail -c +$(( $1 + 1 )) "${LOG_FILE}" 2>/dev/null | grep -qE ': (Copied|Moved) \(|: Deleted$'
318: }
319: PROGRESS_MADE=0
320: stop_no_network() {
321:     local rc="$1" unit="$2"
322:     echo "Couldn't finish: lost the network while backing up ${unit}. Try again when you're online."
323:     log_message "stopped: the network went away while backing up ${unit} (rclone exit ${rc}); exit ${EXIT_NO_NETWORK}"
324:     if [ "${PROGRESS_MADE}" = 1 ]; then
325:         write_stamp "/storage/.cache/cloud_sync/last-content-backup" "$(date +%s) ${EXIT_NO_NETWORK} gaps YOU WENT OFFLINE PART-WAY THROUGH"
326:     else
327:         record_outcome content-backup "${EXIT_NO_NETWORK}"
328:     fi
329:     exit "${EXIT_NO_NETWORK}"
330: }
331: 
332: # What this device calls a game system.
333: #
334: # EmulationStation declares one <path> per system, and on a handheld those are
335: # the /storage/roms subdirectories that hold games. Deriving the list from the
336: # device's own config means it is right per device -- an H700 has 122, a
337: # Snapdragon target has more -- and it never drifts, because the image that
338: # adds a system also adds it here.
339: #
340: # Match on <path>, not <name>: they differ for a dozen systems (ES calls the
341: # folder "coleco" and the system "colecovision", "fbneo"/"fbn", "pc88"/"pc-88"),
342: # and matching names silently drops those folders from the backup.
343: ES_SYSTEMS=""
344: for c in /storage/.config/emulationstation/es_systems.cfg \
345:          /usr/config/emulationstation/es_systems.cfg; do
346:     [ -r "${c}" ] && { ES_SYSTEMS="${c}"; break; }
347: done
348: 
349: system_folders() {
350:     [ -n "${ES_SYSTEMS}" ] || return 0
351:     sed -n 's:.*<path>/storage/roms/\([^</]*\).*:\1:p' "${ES_SYSTEMS}" | sort -u
352: }
353: 
354: # Local content directories, by allowlist.
355: #
356: # This used to be a denylist -- everything under /storage/roms except four
357: # names -- so any directory that appeared there was uploaded as though it were
358: # a game system. That is the same shape of mistake as a denylist sync filter:
359: # what gets included is decided by what happens to be on the disk rather than
360: # by anything anyone chose. bezels, themes, music and a stray scummvm folder
361: # were all being swept up that way, none of them systems (ES keeps scummvm's
362: # games in /storage/.config/scummvm/games and music's playlists in
363: # /storage/.config/gmu/playlists -- the /storage/roms folders of those names
364: # are leftovers).
365: #
366: # In scope: the systems ES declares, and bios. Everything else is out, and
367: # stays out until somebody decides otherwise.
368: # The content-tier files under a directory, as one find(1) definition.
369: #
370: # Extra find arguments are appended, so a caller can list them, count them or
371: # total their sizes without restating the exclusions. "Does this hold
372: # anything?" and "how much does it hold?" answering about different file sets
373: # is exactly how a badge ends up contradicting the size printed next to it.
374: #
375: # Kept in step with SAVE_EXCLUDES and CONFLICT_EXCLUDES below by hand -- there
376: # is no shared parser, and a pattern added there must be added here. The
377: # conflict patterns matter as much as the save ones: without them --list-sizes
378: # counts another sync client's duplicate as content this device holds, and the
379: # picker's badge reports a size the cloud will never agree with.
380: content_files() {
381:     local dir="$1"; shift
382:     # One rule for both sides (D-CLOUD-048), set by MEDIA_MODE (D-CLOUD-050):
383:     #   roms  -- ROMs and BIOS only: the scraper's folders and the game list
384:     #            are neither listed nor moved
385:     #   with  -- ROMs and game content together
386:     #   only  -- game content alone: the scraper's folders and gamelist.xml
387:     # The game list is game content (D-CLOUD-049): the scraper writes it
388:     # beside the artwork, and a restored-then-scraped device must read as
389:     # matching its cloud under ROMs alone. At any depth, as the transfers
390:     # move it (the ROMs pass excludes "**/gamelist.xml", the game-list pass
391:     # includes it): a list below a system's own folder was counted as a ROM
392:     # (the audit of the fixes, G-A-10).
393:     local -a media=()
394:     local d
395:     case "${MEDIA_MODE:-roms}" in
396:         roms) for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( ! -path "${dir%/}/${d}/*" ); done
397:               media+=( ! -name gamelist.xml ) ;;
398:         only) media+=( "(" -name gamelist.xml )
399:               for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( -o -path "${dir%/}/${d}/*" ); done
400:               media+=( ")" ) ;;
401:     esac
402:     local -a native_states=()
403:     if [ "${dir%/}" = "${DEST}/n64" ]; then
404:         native_states=( "(" -path "${dir%/}/*/*" -o "(" ! -name '*.st[0-9]' ! -name '*.pj[0-9]' ! -name '*.pj[0-9].zip' ")" ")" )
405:     fi
406:     find "${dir}" -type f \
407:         ! -name '*.srm' ! -name '*.sav' ! -name '*.fs' ! -name '*.state*' \
408:         ! -name '*.auto' ! -name '*.dsv*' ! -name '*.eep' ! -name '*.mpk' \
409:         ! -name '*.sra' ! -name '*.fla' ! -name '*.mcd' ! -name '*.mcr' \
410:         ! -path '*/save/*' ! -path '*/memcards/*' \
411:         ! -path '*/shared/savefiles/*' ! -path '*/PPSSPP/*' \
412:         ! -path '*/PSP/SAVEDATA/*' \
413:         ! -path '*conflicted copy*' ! -name '*.sync-conflict-*' \
414:         ! -name '*.????????.partial' \
415:         ! -path "${dir%/}/README.txt" \
416:         "${native_states[@]}" "${media[@]}" "$@" 2>/dev/null
417: }
418: 
419: # Does this directory hold anything the content tier would actually transfer?
420: has_content() {
421:     content_files "$1" | head -1 | grep -q .
422: }
423: 
424: # How many bytes of it. Compared against the cloud's own total to answer
425: # whether a system on this device matches what is stored -- an equal total is
426: # not proof of identical files (see #53), so the caller must not phrase it as
427: # one, but a different total is proof they differ, which is the case worth
428: # flagging.
429: content_bytes() {
430:     content_files "$1" -exec stat -c '%s' {} + \
431:         | awk '{ t += $1 } END { print t+0 }'
432: }
433: 
434: list_local_dirs() {
435:     local allow
436:     allow=$(system_folders)
437:     for d in "${DEST}"/*/; do
438:         [ -d "${d}" ] || continue
439:         base=$(basename "${d}")
440:         # The saves sync owns these, and ES declares screenshots and
441:         # savestates as systems of its own -- so the allowlist alone lets them
442:         # through, and content sync would upload the same files the saves sync
443:         # is already keeping, into a second place, under different rules.
444:         # Membership of the content tier is the intersection: a system ES
445:         # declares, and not something another tier already owns.
446:         case "${base}" in
447:             savefiles|savestates|screenshots|backup) continue ;;
448:         esac
449:         if [ "${base}" != "bios" ]; then
450:             printf '%s\n' "${allow}" | grep -qxF "${base}" || continue
451:         fi
452:         # Skip a directory with nothing this tier would carry.
453:         #
454:         # "Not empty" is the wrong test: RetroArch writes .srm and .state next
455:         # to the ROM, so a system whose only contents are saves looks populated
456:         # while a content transfer would send nothing from it. That made --list
457:         # claim the device "has" GBA when what it had was GBA saves, and the
458:         # picker's badge repeated the claim.
459:         #
460:         has_content "${d}" || continue
461:         echo "${base}"
462:     done
463: }
464: 
465: # Where a local directory belongs in the cloud.
466: #
467: # The cloud layout is for a person looking at it on a computer, not a mirror of
468: # the device's storage. There, "bios" is just another folder beside the game
469: # systems, which is an accident of how the handheld stores things and tells a
470: # reader nothing. Two named folders do: ROMs and BIOS.
471: remote_for() {
472:     case "$1" in
473:         bios) echo "${ROOT}BIOS" ;;
474:         *)    echo "${ROOT}ROMs/$1" ;;
475:     esac
476: }
477: 
478: # The systems this device syncs, chosen once and changeable. See
479: # cloud_content_restore for why this lives in /storage/.cache rather than in
480: # anything the settings backup captures. A device that does not want PS2 coming
481: # down does not want it going up either, so both directions read the same file.
482: SELECTION="/storage/.cache/cloud_sync/content-systems"
483: 
484: # Only a system folder's name is ever acted on (audit #307 PL-030):
485: # --set-systems refuses any other since that change, and a selection an
486: # earlier build wrote without the check is read past a line that is not
487: # one, never with it.
488: selected_systems() {
489:     [ -r "${SELECTION}" ] || return 0
490:     grep -E '^[A-Za-z0-9_][A-Za-z0-9._-]*$' "${SELECTION}" 2>/dev/null
491: }
492: 
493: # --with-media: include scraped game content (D-CLOUD-048). Off by default:
494: # the scraper's folders under a system are neither moved nor counted unless
495: # the switch is on, so a restored-then-scraped device does not read as
496: # "different" from its cloud copy. Taken from anywhere on the command line.
497: MEDIA_MODE=roms
498: _ARGS=()
499: for _a in "$@"; do
500:     case "${_a}" in
501:         --with-media) MEDIA_MODE=with ;;
502:         --media-only) MEDIA_MODE=only ;;
503:         *) _ARGS+=("${_a}") ;;
504:     esac
505: done
506: set -- "${_ARGS[@]}"
507: MEDIA_DIRS="images videos manuals screenshots fanart boxart wheel mix maps media"
508: # What the main rclone pass carries, per mode. The game list never rides the
509: # main pass: it has its own --update pass below (newest wins), which runs
510: # only when game content is in scope.
511: MEDIA_EXCLUDES=()
512: case "${MEDIA_MODE}" in
513:     roms) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--exclude "/${_d}/**"); done ;;
514:     only) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--include "/${_d}/**"); done ;;
515: esac
516: 
517: case "${1}" in
518:     --selected)
519:         # Only the selected systems that this device actually has content for.
520:         mapfile -t ALLDIRS < <(list_local_dirs)
521:         DIRS=()
522:         for d in "${ALLDIRS[@]}"; do
523:             selected_systems | grep -qxF "${d}" && DIRS+=("${d}")
524:         done
525:         # BIOS is not a system and not a pick (D-CLOUD-043): it comes with
526:         # the ROMs tier whenever this device holds any, exactly as restore
527:         # brings it whenever the cloud does. Found in the VM on 2026-09-06:
528:         # a device's BIOS folder never went up once the picker stopped
529:         # listing it. Not with game content alone -- BIOS is not that.
530:         if [ "${MEDIA_MODE}" != only ] && printf '%s\n' "${ALLDIRS[@]}" | grep -qx bios \
531:             && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
532:             DIRS+=("bios")
533:         fi
534:         # Nothing here to send is nothing to do -- a run that completed, not
535:         # one that failed (#308 claude F-CS-15): it exited 1, and the page
536:         # read COULDN'T FINISH - SOMETHING WENT WRONG. Exit 0, the sentence,
537:         # and the stamp saying the last press completed.
538:         if [ ${#DIRS[@]} -eq 0 ]; then
539:             echo "Nothing to back up: none of the systems you picked have anything on this device."
540:             record_outcome content-backup 0
541:             exit 0
542:         fi
543:     ;;
544:     --list)
545:         list_local_dirs
546:         exit $?
547:     ;;
548:     --list-sizes)
549:         # name|bytes for what this device holds, the mirror of
550:         # cloud_content_restore --scan. The picker needs both sides to say
551:         # whether a system here matches the copy in the cloud.
552:         while IFS= read -r base; do
553:             [ -n "${base}" ] || continue
554:             printf '%s|%s\n' "${base}" "$(content_bytes "${DEST}/${base}")"
555:         done < <(list_local_dirs)
556:         exit 0
557:     ;;
558:     --all)
559:         mapfile -t DIRS < <(list_local_dirs)
560:         if [ ${#DIRS[@]} -eq 0 ]; then
561:             echo "Nothing to back up: there are no ROMs or BIOS files on this device."
562:             record_outcome content-backup 0
563:             exit 0
564:         fi
565:     ;;
566:     "")
567:         echo "Usage: ${SCRIPT_NAME} --list | --list-sizes | --all | <dir> [<dir>...]" >&2
568:         exit 1
569:     ;;
570:     *)
571:         DIRS=("$@")
572:     ;;
573: esac
574: 
575: # Another sync client's unresolved dispute is not our content.
576: #
577: # Dropbox and Nextcloud rename the losing side of a concurrent write to
578: # "X (Someone's conflicted copy 2026-09-03)"; Syncthing appends
579: # ".sync-conflict-<date>". Carrying those onto a handheld doubles the storage
580: # for no benefit -- the player cannot resolve a conflict from a games menu --
581: # and it makes the artifacts immortal: a device that downloaded them uploads
582: # them again on the next backup, so deleting them in the cloud looks like the
583: # provider putting them back. That happened here, to 271 directories of BIOS
584: # (2026-09-04).
585: #
586: # Resolution belongs on the computer where both sides can be seen. We decline
587: # to move them in either direction, which is also the only way a cleanup on
588: # one side stays done.
589: CONFLICT_EXCLUDES=(
590:     --exclude "**conflicted copy**"
591:     --exclude "**.sync-conflict-**"
592:     --exclude "*.????????.partial"
593: )
594: 
595: # gamelist.xml travels on its own terms.
596: #
597: # It is the scraping payload -- names, descriptions, genres, ratings, media
598: # paths and the cheevos hashes that cost a hash of every ROM -- and all of that
599: # is device-independent, so sharing it means scraping once rather than once per
600: # handheld. Paths inside it are relative ("./Mega Man 3 (USA).zip"), so it
601: # carries across devices unchanged.
602: #
603: # It degrades well in both directions, which is why this is safe at all:
604: #
605: #   * Reading, EmulationStation builds its list from the filesystem first and
606: #     skips any entry whose ROM is absent ("does not exist ... Ignoring"), so a
607: #     52-entry list on a handheld holding 10 of those games shows 10 games and
608: #     no phantoms. That holds while ParseGamelistOnly is false, which is the
609: #     default.
610: #   * Writing, updateGamelist re-reads the file and rewrites only the entries
611: #     whose metadata changed, preserving entries for ROMs this device does not
612: #     have -- deliberately, per its own comment.
613: #
614: # What neither of those protects against is rclone, which replaces a file
615: # wholesale. A device that scans its own ROMs and uploads before it has ever
616: # restored would push a thin list over a rich one. That is an ordering problem,
617: # not a merge problem, and --update solves it: skip when the destination is
618: # newer, so the freshest list wins rather than the last writer.
619: #
620: # Hence a separate pass. --update on the whole content transfer would also
621: # apply to ROMs, where "destination is newer" is not a reason to skip a file
622: # somebody deliberately re-uploaded.
623: #
624: # Three fields remain genuinely per-device -- playcount, lastplayed and
625: # gametime, which EmulationStation itself marks isStatistic and refuses to let
626: # a scrape overwrite. A file-level sync cannot make that distinction, so those
627: # are last-writer-wins across devices. Everything else in the file is authored
628: # or scraped, and favorite is explicitly not a statistic in ES's model.
629: # A save directory can contain arbitrary filenames, including gamelist.xml.
630: # Ordered filters keep that progress out of this separate media pass too.
631: GAMELIST_ONLY=(
632:     --filter "- save/**" --filter "- memcards/**"
633:     --filter "- shared/savefiles/**" --filter "- PPSSPP/**"
634:     --filter "- PSP/SAVEDATA/**"
635:     --filter "+ gamelist.xml" --filter "+ **/gamelist.xml" --filter "- **"
636: )
637: 
638: # What the saves tier owns, and content must never carry.
639: #
640: # A system directory holds more than games: RetroArch writes .srm and .state
641: # next to the ROM, and several systems keep memory cards in a subfolder. The
642: # saves allowlist claims all of it ("+ /**/*.srm" and friends in
643: # cloud_sync-rules.txt), so uploading a system folder wholesale puts saves
644: # in a second cloud location under different rules -- two writers and no
645: # reconciliation, which is exactly how 70 files were deleted on 2026-09-01.
646: #
647: # Worse in the other direction: a content restore would then copy stale saves
648: # back over live ones.
649: #
650: # The earlier allowlist fix (d77d4ea44d) covered directories another tier
651: # owns. This is the same rule one level down, for files. Kept in step with
652: # cloud_sync-rules.txt by hand -- there is no shared parser, and a pattern
653: # added there must be added here. .fla was added there (#89, N64's flash
654: # saves beside the ROM) and not here, so a content backup uploaded it and
655: # a match removed it as content (the audit's gpt F-CS-02).
656: SAVE_EXCLUDES=(
657:     --exclude "*.srm" --exclude "*.sav" --exclude "*.fs"
658:     --exclude "*.state*" --exclude "*.auto" --exclude "*.dsv*"
659:     --exclude "*.eep" --exclude "*.mpk" --exclude "*.sra" --exclude "*.fla"
660:     --exclude "*.mcd" --exclude "*.mcr"
661:     --exclude "save/**" --exclude "memcards/**"
662:     --exclude "shared/savefiles/**" --exclude "PPSSPP/**"
663:     --exclude "PSP/SAVEDATA/**"
664: )
665: 
666: # These state names belong to the N64 writer at its system root, not to
667: # similarly named content in other systems or nested library directories.
668: SYSTEM_SAVE_EXCLUDES=()
669: set_system_save_excludes() {
670:     SYSTEM_SAVE_EXCLUDES=()
671:     if [ "$1" = n64 ]; then
672:         SYSTEM_SAVE_EXCLUDES=(--exclude "/*.st[0-9]" --exclude "/*.pj[0-9]" --exclude "/*.pj[0-9].zip")
673:     fi
674: }
675: 
676: 
677: STATUS=0
678: take_cloud_lock
679: # Everything from here to the end of the script runs with the lock
680: # descriptor closed, so no child of this run can hold the lock once this
681: # shell is gone -- see take_cloud_lock. The brace group is the whole of
682: # the change: it adds no subshell, so exits, traps and variables behave
683: # exactly as they did.
684: {
685: # Settings may change while the interactive preview is open. Re-check under
686: # the transfer lock before sending anything to the previously named cloud.
687: if [ "$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)" != "${REMOTENAME}" ]; then
688:     echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
689:     echo "Your cloud connection changed. Start this operation again."
690:     exit 1
691: fi
692: UNIT_N=${#DIRS[@]}; UNIT_I=0
693: for DIR in "${DIRS[@]}"; do
694:     set_system_save_excludes "${DIR}"
695:     # Local -> remote. This script uploads; cloud_content_restore is the one
696:     # that brings content back down.
697:     SRC="${DEST}/${DIR}"
698:     TARGET="$(remote_for "${DIR}")"
699:     UNIT_I=$((UNIT_I + 1))
700:     log_message "Content backup: ${SRC} -> ${TARGET}"
701:     # The marker the transfer page reads: what is being copied, and which of
702:     # how many. Restore has emitted it since D-UI-024; backup never did, so
703:     # the page kept the previous script's last label -- SETTINGS BACKUP --
704:     # through every system it uploaded (maintainer, 2026-09-06).
705:     echo ">>> unit ${DIR:-everything}|${UNIT_I}|${UNIT_N}"
706:     echo "Backing up ${DIR:-everything} to the cloud..."
707:     # --progress is what puts the stats on stdout. With only --log-file they
708:     # go to the log and the caller sees nothing -- which is why the progress
709:     # card sat at "0 B / 0 B, -, 0 B/s" through a restore that was in fact
710:     # copying Mega Drive ROMs the whole time. The saves path has always passed
711:     # it; these two never did.
712:     #
713:     # And NOT --stats-one-line: that collapses the display to a totals line,
714:     # losing the per-file block. A transfer of a thousand small BIOS files
715:     # spends minutes between percentage changes, and the only thing that says
716:     # it is alive rather than stuck is the name of the file it is on right
717:     # now. --stats 1s keeps that moving.
718:     #
719:     # No --progress-terminal-width: the flag does not exist on every rclone we
720:     # ship against (the saves scripts test for it with "rclone help | grep"
721:     # before using it), and an unknown flag is a usage error that transfers
722:     # nothing. rclone pads the file name out to a guessed width; the reader
723:     # trims it, so the flag bought nothing worth a version check.
724:     #
725:     # The folder first, on its own. rclone creates a missing destination as
726:     # part of a copy, but only after listing it, and a server that answers a
727:     # missing folder with an error rather than "not found" (an FTP server's
728:     # 501 where the standard reply is 550) fails that listing. Under
729:     # --retries 1 that one attempt is the whole run: reported as failed,
730:     # with files that may or may not have landed (#142, from the #133
731:     # matrix: 2 of 3). mkdir is one round trip, idempotent, and on a bucket
732:     # under directory markers it writes the marker the folder's parent then
733:     # lists (D-CLOUD-120). Its own failure is left to the copy to report.
734:     rclone mkdir "${TARGET}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null
735:     UNIT_LOG0=$(log_offset)
736:     # The setup's note at a unit's root (BIOS/README.txt, cloud_setup
737:     # --seed-folders) is not content, and neither side counts it (#308 gpt
738:     # F-CS-30): it came down into /storage/roms/bios and read ever after as a
739:     # file this device has and the cloud does not.
740:     bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
741:         "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${MEDIA_EXCLUDES[@]}" \
742:         --exclude "gamelist.xml" --exclude "**/gamelist.xml" --exclude "/README.txt" \
743:         --progress --stats 1s \
744:         --log-file "${LOG_FILE}" --log-level INFO
745:     RC=$?
746: 
747:     # The game list: newest wins, rather than whoever ran last. Game content
748:     # only (D-CLOUD-049) -- under ROMs alone the file stays where it is. Its
749:     # result is the unit's, by the same 0|9 rule (audit #307 PL-066): it
750:     # was discarded with `|| true`, so a game list that did not move left a
751:     # unit, a stamp and a page that said the unit had.
752:     if [ "${MEDIA_MODE}" != roms ] && { [ "${RC}" -eq 0 ] || [ "${RC}" -eq 9 ]; }; then
753:         bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
754:             "${GAMELIST_ONLY[@]}" --update \
755:             --stats 0 \
756:             --log-file "${LOG_FILE}" --log-level INFO
757:         GL_RC=$?
758:         case "${RC}" in
759:             0|9) case "${GL_RC}" in 0|9) ;; *) RC=${GL_RC} ;; esac ;;
760:         esac
761:     fi
762: 
763:     # What moved in this unit, whatever its result (G-A-08/G-A-13).
764:     moved_since "${UNIT_LOG0}" && PROGRESS_MADE=1
765:     if [ ${RC} -ne 0 ] && [ ${RC} -ne 9 ]; then
766:         # A failed unit says why: the network gone ends the run as 69 here,
767:         # anything else carries rclone's own code up as before.
768:         network_gone && stop_no_network "${RC}" "${DIR:-everything}"
769:         log_message "backup of ${DIR:-everything}: rclone exit ${RC}"
770:         echo "Couldn't finish backing up ${DIR:-everything}: $(why_for "${RC}" | tr 'A-Z' 'a-z')."
771:         say_why "$(why_for "${RC}")"
772:         STATUS=${RC}
773:     else
774:         echo "Backed up ${DIR:-everything}."
775:     fi
776: done
777: 
778: # The progress card is gone by the time somebody who walked away comes back, so
779: # leave the outcome where the menu can read it later. Device-local state, so it
780: # lives under /storage/.cache and not in the settings backup.
781: record_outcome content-backup "${STATUS}"
782: 
783: # A failed unit leaves with rclone's own code, unremapped: nothing rclone
784: # returns can read as the lock sentinel now that it is 75 (#99).
785: exit ${STATUS}
786: } 9>&-



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore


## Original lines 1–1574
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_content_restore - pull game content (ROMs, BIOS, ...) from the cloud.
6: #
7: # Unlike the saves sync (allowlist-filtered, never touches ROMs/BIOS), this is
8: # an explicit, user-initiated copy of a chosen remote directory into
9: # /storage/roms. It never deletes anything locally (rclone copy) and skips
10: # files that already exist unless they differ.
11: #
12: # Usage:
13: #   cloud_content_restore --known-directories  print local/supported directory names
14: #   cloud_content_restore --list           print top-level remote directories
15: #   cloud_content_restore <dir> [<dir>..]  copy remote dirs into /storage/roms
16: #   cloud_content_restore --all            copy the whole remote content root
17: #   cloud_content_restore --match          preview making this device match;
18: #                                          writes the plan --apply is held to
19: #   cloud_content_restore --match --apply  do what the preview planned, no
20: #                                          more (the only mode that deletes)
21: #
22: # CONTENT_REMOTE selects the only cloud library this script reads. ROMs live
23: # under ROMs/<system>, and BIOS under BIOS. Choosing a path moves no files.
24: 
25: . /etc/profile
26: 
27: LOG_FILE="/var/log/cloud_sync.log"
28: SCRIPT_NAME=$(basename "$0")
29: DEST="/storage/roms"
30: 
31: # Local directory membership shared with cloud_setup discovery. This read-only
32: # mode needs neither credentials nor a nonempty local library: a fresh device
33: # still recognizes every system in its installed EmulationStation config.
34: legacy_dirs() {
35:     local d base
36:     for d in "${DEST}"/*/; do
37:         [ -d "${d}" ] || continue
38:         base=$(basename "${d}")
39:         case "${base}" in savefiles|savestates|screenshots|backup) continue ;; esac
40:         echo "${base}"
41:     done
42: }
43: 
44: # Match installed paths, not system labels: several labels differ from the
45: # actual directory a game uses. The same functions drive --scan below.
46: es_systems_file() {
47:     for c in /storage/.config/emulationstation/es_systems.cfg \
48:              /usr/config/emulationstation/es_systems.cfg; do
49:         [ -r "${c}" ] && { echo "${c}"; return 0; }
50:     done
51: }
52: 
53: supported_systems() {
54:     local c; c=$(es_systems_file)
55:     [ -n "${c}" ] || return 0
56:     sed -n 's:.*<path>/storage/roms/\([^</]*\).*:\1:p' "${c}" | sort -u
57: }
58: 
59: if [ "${1:-}" = --known-directories ]; then
60:     { legacy_dirs; supported_systems; echo bios; } | sort -u
61:     exit 0
62: fi
63: 
64: # The exit that means "nothing ran: another cloud sync holds the lock", which
65: # EmulationStation names (SKIPPED - ANOTHER CLOUD SYNC IS RUNNING). It was 3
66: # until 2026-09-09, which is also rclone's "directory not found", so a failed
67: # unit carrying rclone's code to the final exit read as a sync that was never
68: # running (#99, blindspot 33). sysexits.h's EX_TEMPFAIL sits above everything
69: # rclone returns (0-9) and below the 128+signal range, so nothing this script
70: # forwards can produce it. The same two numbers (75, and 69 for no network --
71: # raised here when the link goes away under a running unit, see
72: # stop_no_network) are what EmulationStation reads; scripts and ES ship
73: # together.
74: readonly EXIT_LOCK_HELD=75 EXIT_NO_NETWORK=69
75: 
76: log_message() {
77:     echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO] [${SCRIPT_NAME}] ${1}" >> ${LOG_FILE}
78: }
79: 
80: # One cloud transfer at a time, whoever asked for it.
81: #
82: # Three callers can start one: EmulationStation at boot (the startup sync,
83: # which ran headless from autostart/102-cloud-saves until #94), EmulationStation
84: # after a game exits, and a person in the menu. Until
85: # 2026-09-04 the game-exit path was an OS hook with a pgrep guard; moving it
86: # into ES kept the visible progress and dropped the guard, so exiting a game
87: # during the boot sync started a second rclone against the same remote. Two
88: # writers on one folder is how a mirror deleted another handheld's saves
89: # (D-CLOUD-014); two copies racing is milder, and still nothing anybody asked
90: # for.
91: #
92: # The lock lives here, in the script, so no caller has to know about the
93: # others. /var/run is tmpfs, so a lock cannot survive a reboot and go stale.
94: # Non-blocking, because a request that queues silently behind a twenty-minute
95: # transfer looks exactly like one that hung. Exit EXIT_LOCK_HELD (75) means
96: # "skipped: another sync is running" -- the UI names it, and no last-run stamp
97: # is written for work that did not happen.
98: #
99: # The descriptor is this shell's and nothing else's. A shell redirection
100: # carries no close-on-exec, so `exec 9>` hands fd 9 to every child the
101: # script starts, and rclone then holds the lock for the whole of a transfer
102: # (watched in /proc on the VM, #124). While the script outlives its
103: # children that is invisible, because bash waits for each of them before it
104: # exits. The moment it does not -- killed or orphaned while rclone is still
105: # copying, a child left in the background -- the lock outlives the run that
106: # took it and every sync afterwards is refused with "another cloud sync is
107: # running" when nothing is running at all. So the body runs with fd 9
108: # closed ("9>&-"): bash keeps the lock on a descriptor of its own, which it
109: # does mark close-on-exec, and nothing this script starts can see it.
110: #
111: # The refusal also waits a moment before saying no, as belt and braces for
112: # a holder this script does not own: a descriptor leaked by an older build,
113: # or a process in the act of exiting, frees itself in milliseconds, while a
114: # real concurrent transfer does not. One second of patience turns a raced
115: # skip into a run that works and costs a genuinely blocked run one second.
116: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
117: take_cloud_lock() {
118:     local tries=0
119:     exec 9>"${CLOUD_SYNC_LOCK}"
120:     while ! flock -n 9; do
121:         if [ "${tries}" -ge 4 ]; then
122:             echo "Skipped: another cloud sync is already running. Try again when it's done."
123:             log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}"
124:             exit "${EXIT_LOCK_HELD}"
125:         fi
126:         tries=$((tries + 1))
127:         sleep 0.25
128:     done
129: }
130: 
131: if [ ! -e "/storage/.config/rclone/rclone.conf" ]; then
132:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
133:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
134:     exit 1
135: fi
136: 
137: # The two values this script needs from cloud_sync.conf, read as text and
138: # never sourced (audit #307 PL-051's script half): a folder value an earlier
139: # build wrote with "$(...)" in it ran on every `source`. A CONTENT_REMOTE
140: # that carries a $, a backtick, a backslash or a control character is not a
141: # folder name, and the run refuses it rather than use it as a path.
142: #
143: # Read in the forms `source` reads (the audit of the fixes, G-A-06/G-A-02):
144: # the value double quoted, single quoted or bare; after it nothing, or
145: # blanks and a # comment. The first cut took only KEY=value or KEY="value"
146: # whole: a trailing comment or single quotes gave an empty CONTENT_REMOTE --
147: # the cloud's root -- where the folder had been, and the backup went there.
148: # A line it cannot read as plain text exits 2, and CONTENT_REMOTE's refuses
149: # the run; nothing is read as the root that did not say the root. Of two
150: # lines for one key, the first: every saves run EmulationStation starts is
151: # --yes, which runs cloud_sync_cleanup_duplicates.sh, which keeps the first,
152: # so that is the value the saves scripts run with and the file is left with.
153: #
154: # And a file with a control character but a tab anywhere in it is
155: # unreadable here as it is to the saves scripts' conf_valid (the audit of
156: # the fix round, PL-002): this reader never sources the file, but a blank
157: # is a space or a tab to both, so the tiers run with one reading of one
158: # file -- a carriage return after a value used to pass here as a blank.
159: #
160: # The key set in a form `source` reads and this does not -- indented,
161: # exported, declared, appended to, or with a blank before the = -- is
162: # unreadable, never absent (the audit of the fix round, lead G2-A-03):
163: # read as absent it was the cloud's root, and a content backup went there.
164: # The saves scripts' conf_valid refuses such a file whole.
165: conf_get() { # <KEY>: its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
166:     [ -f /storage/.config/cloud_sync.conf ] || return 0
167:     awk -v k="$1" '
168:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
169:         index($0, k "=") != 1 && !other \
170:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
171:         index($0, k "=") == 1 {
172:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
173:             c = substr(s, 1, 1)
174:             if (c == "\"") {
175:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
176:                 # character each (PL-015), and so does this; an unescaped $
177:                 # or backtick is an expansion this reader does not make, and
178:                 # any other backslash is refused as conf_valid refuses it.
179:                 n = length(s); i = 2; closed = 0
180:                 while (i <= n) {
181:                     d = substr(s, i, 1)
182:                     if (d == "\"") { closed = 1; break }
183:                     if (d == "\\") {
184:                         e = substr(s, i + 1, 1)
185:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
186:                         ok = 0
187:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
188:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
189:                         break
190:                     }
191:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
192:                     v = v d; i++
193:                 }
194:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
195:                 if (ok) r = substr(s, i + 1)
196:             } else if (c == "'"'"'") {
197:                 j = index(substr(s, 2), c)
198:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
199:             } else {
200:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
201:             }
202:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
203:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
204:         }
205:         END {
206:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
207:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
208:             if (found && !firstok) { print firstwhy; exit 2 }
209:             if (found) print first
210:         }
211:     ' /storage/.config/cloud_sync.conf
212: }
213: if ! CONTENT_REMOTE=$(conf_get CONTENT_REMOTE); then
214:     # On a refusal conf_get says why, for the log: the line and its shape,
215:     # never the value (PL-015).
216:     log_message "cloud_sync.conf was not read: ${CONTENT_REMOTE}"
217:     echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
218:     echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
219:     exit 1
220: fi
221: # The bound falls back to the shipped value below when this is empty; a
222: # line it cannot read is that too, and the log says so.
223: if ! RCLONE_NET_OPTS=$(conf_get RCLONE_NET_OPTS); then
224:     log_message "RCLONE_NET_OPTS was not read (${RCLONE_NET_OPTS}); the shipped bound stands in"
225:     RCLONE_NET_OPTS=""
226: fi
227: case "${CONTENT_REMOTE}" in
228:     *[\$\`\\]*|*[[:cntrl:]]*)
229:         echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
230:         echo "Your cloud sync settings couldn't be read. Set up cloud storage again under GAME SETTINGS > MANAGE CLOUD STORAGE."
231:         exit 1 ;;
232: esac
233: 
234: REMOTENAME=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active)
235: if [ -z "${REMOTENAME}" ]; then
236:     echo ">>> why YOUR CLOUD STORAGE ISN'T SET UP YET"
237:     echo "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first."
238:     exit 1
239: fi
240: 
241: CHECK_CONTENT="${CONTENT_REMOTE%/}"
242: if [ -n "${CHECK_CONTENT}" ]; then
243:     case "/${CHECK_CONTENT#/}/" in
244:         *//*|*/./*|*/../*)
245:             echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
246:             exit 1 ;;
247:     esac
248: fi
249: ROOT="${REMOTENAME}${CONTENT_REMOTE:+${CONTENT_REMOTE%/}/}"
250: 
251: # The bound on every rclone command below that opens a socket: RCLONE_NET_OPTS
252: # from cloud_sync.conf, or the same shipped values when the config has no
253: # such line yet -- this script reads the config without running
254: # cloud_sync_helper, so on the first run after an update it may not, and the
255: # bound is a guard that a missing line must not switch off. The reasoning
256: # for the numbers is beside the option in cloud_sync.conf.defaults; the
257: # short version is that rclone's own defaults (60 s connect, 5 min idle, 10
258: # low-level retries, 3 whole-run retries) hold a run for over ten minutes
259: # on a link that drops mid-run (#101, #102, #103). Keep the fallback in step
260: # with the default. The two rclone calls that touch only this device --
261: # `rclone size` and `rclone delete` on a local folder in the match flow --
262: # open no socket and carry none of this.
263: RCLONE_NET_OPTS_FALLBACK="--contimeout 15s --timeout 30s --low-level-retries 10 --retries 1"
264: _net_opts=$(echo "${RCLONE_NET_OPTS:-}" | tr '\n\\' '  ' | tr -s ' ' | sed 's/^ //; s/ $//')
265: [ -n "${_net_opts}" ] || _net_opts="${RCLONE_NET_OPTS_FALLBACK}"
266: read -r -a RCLONE_NET_OPTS_ARRAY <<< "${_net_opts}"
267: # Installed beside this script, also when the host fixtures copy it.
268: . "$(dirname "${BASH_SOURCE[0]}")/cloud_content_transfer" || exit 1
269: # A probe is a single listing that exists to answer quickly: one attempt,
270: # tighter than the transfers (the same values the saves scripts probe with).
271: readonly -a RCLONE_PROBE_OPTS=(--contimeout 10s --timeout 20s --low-level-retries 1 --retries 1)
272: # A listing's bound (#143): three low-level retries, not a transfer's ten --
273: # rclone's S3 backend hands the count to the AWS SDK as attempts with
274: # exponential backoff (see cloud_backup for the measurement).
275: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
276: 
277: # Whole or not at all: to a temporary name beside the stamp, then renamed
278: # over it, as ThreadedCloudSync::recordOutcome does. A kill mid-write leaves
279: # the previous stamp; it used to leave an empty file (D-CLOUD-078, #105).
280: # LAST_WHY, when a `>>> why` line was printed, becomes the stamp's third
281: # field as a token (spaces to underscores) for the row to read (D-UI-028).
282: LAST_WHY=""
283: write_stamp() {
284:     local file="$1" line="$2" tmp
285:     mkdir -p "$(dirname "${file}")" 2>/dev/null
286:     tmp="${file}.tmp.$$"
287:     { printf '%s\n' "${line}" > "${tmp}"; } 2>/dev/null \
288:         && mv -f "${tmp}" "${file}" 2>/dev/null \
289:         || rm -f "${tmp}" 2>/dev/null
290: }
291: record_outcome() { # <stamp-name> <rc>
292:     local why=""
293:     case "$2" in
294:         0|9|"${EXIT_NO_NETWORK}"|"${EXIT_LOCK_HELD}") ;;
295:         *) [ -n "${LAST_WHY}" ] && why=" $(printf '%s' "${LAST_WHY}" | tr ' ' '_')" ;;
296:     esac
297:     write_stamp "/storage/.cache/cloud_sync/last-$1" "$(date +%s) $2${why}"
298: }
299: 
300: # Why a unit did not finish, in the player's words (D-UI-028, D-CLOUD-077):
301: # one `>>> why <SENTENCE>` protocol line per failing unit, which the page
302: # and the card read; rclone's code stays in the log. The sentences are the
303: # vocabulary table's in es-native-ui.md.
304: say_why() {
305:     LAST_WHY="$1"
306:     echo ">>> why $1"
307:     log_message "why: $1"
308: }
309: why_for() {
310:     case "$1" in
311:         3|4) echo "COULDN'T FIND YOUR CLOUD FOLDER" ;;
312:         5|124) echo "YOUR CLOUD STOPPED ANSWERING" ;;
313:         6)   echo "SOME FILES DIDN'T FINISH" ;;
314:         7|8) echo "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
315:         130) echo "IT WAS STOPPED" ;;
316:         *)   echo "SOMETHING WENT WRONG" ;;
317:     esac
318: }
319: 
320: has_default_route() {
321:     ip -4 route show default 2>/dev/null | grep -q . \
322:         || ip -6 route show default 2>/dev/null | grep -q .
323: }
324: 
325: # Is the network gone? Asked after rclone failed, so the run can say why it
326: # ended rather than hand up a code that reads as FAILED and sends somebody
327: # to a log. Gone: no default route, or a route through which neither the
328: # remote nor anything else answers a bounded probe. Not gone: the remote
329: # answers again (a blip rclone did not survive), or the internet answers
330: # while the remote does not (the provider, or the sign-in) -- that is
331: # rclone's failure to report, and the caller passes rclone's code through
332: # as before. The same three questions cloud_backup asks (#101, #103).
333: network_gone() {
334:     has_default_route || return 0
335:     rclone lsd "${REMOTENAME}" "${RCLONE_PROBE_OPTS[@]}" >/dev/null 2>&1 && return 1
336:     ping -q -c1 -W 3 1.1.1.1 >/dev/null 2>&1 && return 1
337:     ping -q -c1 -W 3 8.8.8.8 >/dev/null 2>&1 && return 1
338:     return 0
339: }
340: 
341: # The network went away under a running unit. Says so, records that the run
342: # did not complete -- never a 0, which would read as a restore that happened
343: # -- under the stamp the action keeps (last-content-restore, or
344: # last-content-match for --match --apply), and exits EXIT_NO_NETWORK, which
345: # EmulationStation names (SKIPPED - NO NETWORK CONNECTION on the card,
346: # SKIPPED, NO NETWORK on the row). No further unit is attempted: each would
347: # stall for another minute against the same dead link. rclone copy and sync
348: # write each file under a temporary name and rename it when complete, so
349: # nothing partial is left on the card; a match's deletions had already
350: # happened when the sync ran, and they are final -- a match removes only
351: # what the cloud does not have (D-CLOUD-023; #308 gpt F-CS-26: this said
352: # the cloud still held them).
353: #
354: # SKIPPED means nothing was touched (#308 claude F-CS-24): when something had
355: # already moved -- a unit completed, a match removed files -- before the
356: # network went, the stamp still carries 69 and adds the gaps token and a why,
357: # "<epoch> 69 gaps YOU WENT OFFLINE PART-WAY THROUGH", which the rows read as
358: # COULDN'T FINISH (CloudText::parseLastRun takes the token before the code).
359: # The exit stays 69; the page reads a 69 after progress the same way.
360: # Did this run's rclone move a file since <offset> into the log? Progress,
361: # for the stamp stop_no_network writes, is what rclone logged moving --
362: # "<path>: Copied (...)", "Moved (...)", "Deleted" -- not a unit that
363: # completed (the audit of the fixes, G-A-08/G-A-13): files a unit moved
364: # before its own failure did not count, and a unit that moved nothing did.
365: # Every transfer here logs at INFO to LOG_FILE, and the transfer lock
366: # keeps any other cloud script from writing it meanwhile.
367: log_offset() { stat -c %s "${LOG_FILE}" 2>/dev/null || echo 0; }
368: moved_since() { # <byte offset into LOG_FILE>
369:     local now
370:     now=$(stat -c %s "${LOG_FILE}" 2>/dev/null) || return 1
371:     [ "${now}" -gt "$1" ] 2>/dev/null || return 1
372:     tail -c +$(( $1 + 1 )) "${LOG_FILE}" 2>/dev/null | grep -qE ': (Copied|Moved) \(|: Deleted$'
373: }
374: PROGRESS_MADE=0
375: stop_no_network() {
376:     local stamp="$1" rc="$2" doing="$3"
377:     echo "Couldn't finish: lost the network while ${doing}. Try again when you're online."
378:     log_message "stopped: the network went away while ${doing} (rclone exit ${rc}); exit ${EXIT_NO_NETWORK}"
379:     if [ "${PROGRESS_MADE}" = 1 ]; then
380:         write_stamp "/storage/.cache/cloud_sync/last-content-${stamp}" "$(date +%s) ${EXIT_NO_NETWORK} gaps YOU WENT OFFLINE PART-WAY THROUGH"
381:     else
382:         record_outcome "content-${stamp}" "${EXIT_NO_NETWORK}"
383:     fi
384:     exit "${EXIT_NO_NETWORK}"
385: }
386: 
387: # D-CLOUD-177/178: public ROCKNIX did not ship this content layout.
388: # Only the selected structured library is read or written. A missing folder
389: # must never select another folder, inside or outside that library.
390: 
391: # Where a local directory lives in the current cloud layout.
392: #
393: # ROMs and BIOS are named folders rather than a mirror of /storage/roms,
394: # because the person filling them in is looking at a file manager on a
395: # computer, where "bios sitting beside snes" is an accident of how a handheld
396: # stores things. The local name is what everything else here uses, so the
397: # mapping stays in one place: bios lives under BIOS, everything else under
398: # ROMs.
399: remote_for() {
400:     case "$1" in
401:         bios) echo "${ROOT}BIOS" ;;
402:         *)    echo "${ROOT}ROMs/$1" ;;
403:     esac
404: }
405: 
406: # Backup and restore share exactly the same selected-root mapping.
407: resolve_src() {
408:     remote_for "$1"
409: }
410: 
411: # Does a remote path exist?
412: #
413: # NOT `rclone lsjson --stat`, which is what this used to be. On bucket-based
414: # remotes (S3, B2, Minio) stat synthesises a directory entry for *any* path --
415: # verified against Minio on rclone 1.60 and 1.74, where
416: # "utterly-bogus-never-created" reports success with IsDir true. So it can
417: # never report absence there, and every caller that branched on it took the
418: # "exists" path unconditionally.
419: #
420: # A listing can report absence. Two questions, because a directory can be real
421: # without holding files: does it contain anything, or does its parent list it
422: # (which is what an --s3-directory-markers marker object produces)?
423: exists_remote() {
424:     [ -n "$(rclone lsf "$1" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | head -1)" ] && return 0
425:     local parent name
426:     parent="${1%/}"; name="${parent##*/}"; parent="${parent%/*}"
427:     [ -n "${name}" ] || return 1
428:     rclone lsf --dirs-only "${parent}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -qx "${name}/"
429: }
430: 
431: # Is this remote path missing, rather than unreadable? rclone answers "not
432: # found" (exit 3) when the server's reply is the one it maps to that, and a
433: # plain error (exit 1) when the words differ: an FTP server that answers a
434: # missing folder with 501 "No such directory." where the standard reply is
435: # 550 makes every "is it there yet?" branch read as "the cloud is broken"
436: # (#142, from the #133 matrix). The parent settles it, whatever the words:
437: # walk up until a level lists. A level that lists and lacks the next name is
438: # a path not created yet (0); one that lists and holds it means the failure
439: # was something else (1); a remote whose root will not list is broken (1).
440: # On a bucket an absent prefix lists as empty, which is the same answer
441: # (D-CLOUD-120). Called only after a listing has already failed with a code
442: # other than 3, so the everyday path costs nothing extra.
443: absent_not_broken() {
444:     local path="$1" boundary="${ROOT}" remote rel parent name listing
445:     # Keep remote:/ (absolute root) distinct from remote: (relative home).
446:     case "${path}" in *:/) ;; *) path="${path%/}" ;; esac
447:     case "${boundary}" in *:/) ;; *) boundary="${boundary%/}" ;; esac
448:     # Ancestors beyond the selected library do not establish that an
449:     # unreadable library is missing. Each failed probe must shorten the path.
450:     while [ "${path}" != "${boundary}" ]; do
451:         case "${path}" in "${ROOT}"*) ;; *) return 1 ;; esac
452:         remote="${path%%:*}:"; rel="${path#*:}"
453:         name="${rel##*/}"
454:         case "${rel}" in
455:             */*) parent="${rel%/*}"; [ -n "${parent}" ] || parent=/ ;;
456:             *) parent="" ;;
457:         esac
458:         parent="${remote}${parent}"
459:         [ "${parent}" != "${path}" ] || return 1
460:         if listing=$(rclone lsf --dirs-only "${parent}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
461:             printf '%s\n' "${listing}" | grep -qFx -- "${name}/" && return 1
462:             return 0
463:         fi
464:         path="${parent}"
465:     done
466:     return 1
467: }
468: 
469: # An entire successful metadata result or no result. Partial provider output
470: # is never evidence of an empty library, even with a final not-found code.
471: list_content_dirs() {
472:     local path="$1" rc
473:     LISTED=$(rclone lsf --dirs-only "${path}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); rc=$?
474:     [ "${rc}" -ne 0 ] || return 0
475:     [ -z "${LISTED}" ] || { LISTED=""; return 5; }
476:     { [ "${rc}" -eq 3 ] || absent_not_broken "${path}"; } && return 0
477:     return "${rc}"
478: }
479: 
480: # Which systems this device syncs.
481: #
482: # One cloud library, many handhelds, and they are not interchangeable: an H700
483: # cannot run GameCube, and a 3:2 panel makes a device a Game Boy Advance
484: # machine by preference rather than by limit. So the set is a per-device
485: # choice.
486: #
487: # Kept in /storage/.cache, deliberately. The obvious homes -- cloud_sync.conf,
488: # or ES's system.cfg -- are both captured by the settings backup, and restoring
489: # one device's selection onto another would silently change what that device
490: # syncs. That is the same defect shape as the CONTENT_REMOTE split (6717e0b348),
491: # and once was enough.
492: #
493: # No file means no selection means everything, so a device that has never
494: # opened the picker behaves exactly as it did before.
495: SELECTION="/storage/.cache/cloud_sync/content-systems"
496: 
497: # Only a system folder's name is ever acted on (audit #307 PL-030):
498: # --set-systems refuses any other since that change, and a selection an
499: # earlier build wrote without the check is read past a line that is not
500: # one, never with it.
501: selected_systems() {
502:     [ -r "${SELECTION}" ] || return 0
503:     grep -E '^[A-Za-z0-9_][A-Za-z0-9._-]*$' "${SELECTION}" 2>/dev/null
504: }
505: 
506: # --- make this device match the cloud ------------------------------------
507: #
508: # Backup and restore are both copy-only, deliberately, so a system removed
509: # from the cloud stays on the device forever and a card can never be made to
510: # match the library. This is the third action, and the only one here that
511: # deletes.
512: #
513: # Five rules, each of which has already cost something in this subsystem:
514: #
515: #  1. --delete-excluded NEVER appears. Save files live inside system
516: #     directories; with the excludes in place rclone leaves excluded
517: #     destination files alone, and that one flag inverts it into a save wipe.
518: #  2. Only ROMs/<selected system> and BIOS. /storage/roms also holds
519: #     savefiles, savestates, screenshots, backup, bezels, themes and music --
520: #     other tiers' or nobody's.
521: #  3. An empty or failed listing must never mean "delete everything". A wifi
522: #     drop, a lapsed token and a renamed cloud folder all look exactly like an
523: #     empty cloud, so the content root is positively confirmed to hold
524: #     something before any deletion is considered.
525: #  4. Cloud -> device only. The mirror direction is what deleted another
526: #     handheld's whole save library on 2026-09-01 (D-CLOUD-014).
527: #  5. Saves survive a removed system. Its content goes; the .srm and .state
528: #     files stay, leaving the directory holding only those -- which
529: #     has_content() correctly reports as no content.
530: #
531: # Deletions are final on the device: no local backup-dir. The space reclaimed
532: # is the entire point of syncing ROMs selectively, and the cloud is the backup
533: # by definition, since this only ever removes what the cloud does not have
534: # (D-CLOUD-023). Preview first, then apply.
535: 
536: # Defined here, above every consumer.
537: #
538: # They used to sit below the case statement, which was fine while the only
539: # consumer was the transfer loop at the end of the file -- and silently
540: # catastrophic the moment --match started calling them from inside the case.
541: # Bash expands an unset array to nothing, so rclone ran with no save
542: # excludes at all and a match would have deleted .srm and .state files. It
543: # was invisible in the output: fewer exclusions simply means more deletions,
544: # and the preview reported them as ordinary work.
545: 
546: # What the saves tier owns, and content must never carry.
547: #
548: # A system directory holds more than games: RetroArch writes .srm and .state
549: # next to the ROM, and several systems keep memory cards in a subfolder. The
550: # saves allowlist claims all of it ("+ /**/*.srm" and friends in
551: # cloud_sync-rules.txt), so uploading a system folder wholesale puts saves
552: # in a second cloud location under different rules -- two writers and no
553: # reconciliation, which is exactly how 70 files were deleted on 2026-09-01.
554: #
555: # Worse in the other direction: a content restore would then copy stale saves
556: # back over live ones.
557: #
558: # The earlier allowlist fix (d77d4ea44d) covered directories another tier
559: # owns. This is the same rule one level down, for files. Kept in step with
560: # cloud_sync-rules.txt by hand -- there is no shared parser, and a pattern
561: # added there must be added here. .fla was added there (#89, N64's flash
562: # saves beside the ROM) and not here, so a content backup uploaded it and
563: # a match removed it as content (the audit's gpt F-CS-02).
564: SAVE_EXCLUDES=(
565:     --exclude "*.srm" --exclude "*.sav" --exclude "*.fs"
566:     --exclude "*.state*" --exclude "*.auto" --exclude "*.dsv*"
567:     --exclude "*.eep" --exclude "*.mpk" --exclude "*.sra" --exclude "*.fla"
568:     --exclude "*.mcd" --exclude "*.mcr"
569:     --exclude "save/**" --exclude "memcards/**"
570:     --exclude "shared/savefiles/**" --exclude "PPSSPP/**"
571:     --exclude "PSP/SAVEDATA/**"
572: )
573: 
574: # These state names belong to the N64 writer at its system root, not to
575: # similarly named content in other systems or nested library directories.
576: SYSTEM_SAVE_EXCLUDES=()
577: set_system_save_excludes() {
578:     SYSTEM_SAVE_EXCLUDES=()
579:     if [ "$1" = n64 ]; then
580:         SYSTEM_SAVE_EXCLUDES=(--exclude "/*.st[0-9]" --exclude "/*.pj[0-9]" --exclude "/*.pj[0-9].zip")
581:     fi
582: }
583: 
584: 
585: # Another sync client's unresolved dispute is not our content.
586: #
587: # Dropbox and Nextcloud rename the losing side of a concurrent write to
588: # "X (Someone's conflicted copy 2026-09-03)"; Syncthing appends
589: # ".sync-conflict-<date>". Carrying those onto a handheld doubles the storage
590: # for no benefit -- the player cannot resolve a conflict from a games menu --
591: # and it makes the artifacts immortal: a device that downloaded them uploads
592: # them again on the next backup, so deleting them in the cloud looks like the
593: # provider putting them back. That happened here, to 271 directories of BIOS
594: # (2026-09-04).
595: #
596: # Resolution belongs on the computer where both sides can be seen. We decline
597: # to move them in either direction, which is also the only way a cleanup on
598: # one side stays done.
599: CONFLICT_EXCLUDES=(
600:     --exclude "**conflicted copy**"
601:     --exclude "**.sync-conflict-**"
602:     --exclude "*.????????.partial"
603: )
604: 
605: # gamelist.xml travels on its own terms.
606: #
607: # It is the scraping payload -- names, descriptions, genres, ratings, media
608: # paths and the cheevos hashes that cost a hash of every ROM -- and all of that
609: # is device-independent, so sharing it means scraping once rather than once per
610: # handheld. Paths inside it are relative ("./Mega Man 3 (USA).zip"), so it
611: # carries across devices unchanged.
612: #
613: # It degrades well in both directions, which is why this is safe at all:
614: #
615: #   * Reading, EmulationStation builds its list from the filesystem first and
616: #     skips any entry whose ROM is absent ("does not exist ... Ignoring"), so a
617: #     52-entry list on a handheld holding 10 of those games shows 10 games and
618: #     no phantoms. That holds while ParseGamelistOnly is false, which is the
619: #     default.
620: #   * Writing, updateGamelist re-reads the file and rewrites only the entries
621: #     whose metadata changed, preserving entries for ROMs this device does not
622: #     have -- deliberately, per its own comment.
623: #
624: # What neither of those protects against is rclone, which replaces a file
625: # wholesale. A device that scans its own ROMs and uploads before it has ever
626: # restored would push a thin list over a rich one. That is an ordering problem,
627: # not a merge problem, and --update solves it: skip when the destination is
628: # newer, so the freshest list wins rather than the last writer.
629: #
630: # Hence a separate pass. --update on the whole content transfer would also
631: # apply to ROMs, where "destination is newer" is not a reason to skip a file
632: # somebody deliberately re-uploaded.
633: #
634: # Three fields remain genuinely per-device -- playcount, lastplayed and
635: # gametime, which EmulationStation itself marks isStatistic and refuses to let
636: # a scrape overwrite. A file-level sync cannot make that distinction, so those
637: # are last-writer-wins across devices. Everything else in the file is authored
638: # or scraped, and favorite is explicitly not a statistic in ES's model.
639: # A save directory can contain arbitrary filenames, including gamelist.xml.
640: # Ordered filters keep that progress out of this separate media pass too.
641: GAMELIST_ONLY=(
642:     --filter "- save/**" --filter "- memcards/**"
643:     --filter "- shared/savefiles/**" --filter "- PPSSPP/**"
644:     --filter "- PSP/SAVEDATA/**"
645:     --filter "+ gamelist.xml" --filter "+ **/gamelist.xml" --filter "- **"
646: )
647: 
648: # What EmulationStation owns, which a content match must never delete.
649: #
650: # gamelist.xml carries <playcount>, <lastplayed> and <favorite> -- per-device
651: # facts that exist nowhere else -- and images/, videos/ and manuals/ hold
652: # scraped artwork that can represent hours of scraping. None of it is content
653: # the cloud is authoritative about, so "the cloud does not have it" is not a
654: # reason to remove it.
655: #
656: # Found the only way these things are ever found: reading a real dry run,
657: # which listed "gamelist.xml: Skipped delete" for every system on the device.
658: #
659: # Deliberately scoped to the match path. Whether backup should *upload* a
660: # gamelist is a separate and open question (#61) -- but deleting one locally
661: # is wrong under every answer to it.
662: METADATA_EXCLUDES=(
663:     --exclude "gamelist.xml"
664:     --exclude "**/gamelist.xml"
665:     --exclude "images/**"
666:     --exclude "videos/**"
667:     --exclude "manuals/**"
668:     --exclude "magazines/**"
669:     --exclude "media/**"
670: )
671: 
672: # rclone reports sizes in a NOTICE line using human units ("6.090Ki", "64Ki")
673: # when the destination is local, and bare bytes for a small local-to-local
674: # copy. Parsing only digits silently produced zero for every real transfer.
675: to_bytes() {
676:     awk '{ n = $0 + 0; u = $0; gsub(/[0-9.]/, "", u)
677:            if (u == "Ki") n *= 1024
678:            else if (u == "Mi") n *= 1048576
679:            else if (u == "Gi") n *= 1073741824
680:            else if (u == "Ti") n *= 1099511627776
681:            printf "%d\n", n }'
682: }
683: 
684: # Does the content root actually hold anything? Rule 3.
685: cloud_root_populated() {
686:     local n
687:     n=$(rclone lsf --dirs-only "${ROOT}ROMs/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -c . )
688:     [ "${n}" -gt 0 ] && return 0
689:     rclone lsf --files-only "${ROOT}BIOS/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null | grep -q . && return 0
690:     return 1
691: }
692: 
693: # What one system would gain and lose. Prints "<sys>|<verb>|<files>|<bytes>",
694: # or "<sys>|fail|<rclone exit>|0" when it cannot be told.
695: #
696: # The counting uses rclone against the local path with the very same exclude
697: # arrays the transfer uses, rather than a second hand-written find predicate:
698: # a deletion predicate that can drift from the transfer predicate is how saves
699: # get deleted by a tool that believes it is only touching ROMs.
700: #
701: # Absent is something the cloud says, never something a failure implies
702: # (rule 3, audit #307 PL-001). The system's listing is read apart from its
703: # emptiness: exit 0 with nothing listed, or rclone's 3/4 ("not found"), is a
704: # system the cloud does not have. Any other exit -- a 429 after rclone's own
705: # retries, the link dropping between two calls -- is asked of the parent
706: # (absent_not_broken, #142's walk, for a server whose "missing" rclone does
707: # not map to 3); a parent that lists the system, or will not list at all,
708: # makes the answer "could not tell", and a system that cannot be told is
709: # neither planned nor touched. The listing used to be `lsf | grep -q .`,
710: # which read a failed call as an empty folder and planned `remove`; apply
711: # then deleted the whole system on a transient error. The dry run and the
712: # local count are read the same way: a count that failed is not a zero.
713: match_plan_one() {
714:     local sys="$1" src local_dir n b out listing lrc
715:     set_system_save_excludes "${sys}"
716:     src="$(remote_for "${sys}")"
717:     local_dir="${DEST}/${sys}"
718: 
719:     [ -d "${local_dir}" ] || { printf '%s|none|0|0\n' "${sys}"; return 0; }
720: 
721:     listing=$(rclone lsf "${src}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); lrc=$?
722:     case "${lrc}" in
723:         0|3|4) ;;
724:         *)
725:             if absent_not_broken "${src}"; then
726:                 log_message "match: ${sys} listing failed (rclone exit ${lrc}); its parent lists and lacks it, so it is absent"
727:                 lrc=3
728:             else
729:                 log_message "match: ${sys} could not be listed (rclone exit ${lrc}); not planned"
730:                 printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
731:                 return 0
732:             fi ;;
733:     esac
734: 
735:     if [ "${lrc}" -eq 0 ] && [ -n "${listing}" ]; then
736:         # Present in the cloud: sync reconciles both directions of difference.
737:         out=$(bounded_content_rclone sync "${src}" "${local_dir}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
738:                 "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
739:                 --dry-run --stats 0 2>&1)
740:         lrc=$?
741:         if [ "${lrc}" -ne 0 ]; then
742:             log_message "match: ${sys} dry run failed (rclone exit ${lrc}); not planned"
743:             printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
744:             return 0
745:         fi
746:         # "NOTICE: Game3.zip: Skipped delete as --dry-run is set (size 5)" --
747:         # the exact wording on rclone 1.75.0, read off the real output rather
748:         # than taken from the documentation. The size in the tail is what lets
749:         # the confirmation say how much space comes back.
750:         n=$(printf '%s\n' "${out}" | grep -c "Skipped delete")
751:         b=$(printf '%s\n' "${out}" | sed -n 's/.*Skipped delete.*(size \([0-9.KMGTi]*\)).*/\1/p' \
752:               | to_bytes | awk '{ t += $1 } END { print t+0 }')
753:         printf '%s|sync|%s|%s\n' "${sys}" "${n}" "${b}"
754:     else
755:         # Absent from the cloud entirely: its content goes, its saves stay.
756:         out=$(rclone size "${local_dir}" \
757:                 "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" 2>/dev/null)
758:         lrc=$?
759:         n=$(printf '%s\n' "${out}" | sed -n 's/^Total objects: *\([0-9]*\).*/\1/p' | head -1)
760:         b=$(printf '%s\n' "${out}" | sed -n 's/^Total size: .*(\([0-9]*\) Byte).*/\1/p' | head -1)
761:         if [ "${lrc}" -ne 0 ] || [ -z "${n}" ]; then
762:             log_message "match: ${sys} could not be counted on this device (rclone exit ${lrc}); not planned"
763:             printf '%s|fail|%s|0\n' "${sys}" "${lrc}"
764:             return 0
765:         fi
766:         [ -n "${b}" ] || b=0
767:         [ "${n}" -eq 0 ] && { printf '%s|none|0|0\n' "${sys}"; return 0; }
768:         printf '%s|remove|%s|%s\n' "${sys}" "${n}" "${b}"
769:     fi
770: }
771: 
772: # The saves restore's record that the tree under it holds no leftover of a
773: # cut transfer (cloud_restore's PARTIALS_CLEAN, #308 claude F-CS-08): this
774: # script writes into the same tree, so it takes the record down while it
775: # writes and puts it back only when it ended by itself with nothing of its
776: # own left over -- a failed unit's folder is swept for rclone's
777: # <name>.<8>.partial before that. A run of this cut part-way leaves the
778: # record down, and the next saves restore walks the tree (the audit of the
779: # fixes, claude G-A-07: the record said clean across a content restore
780: # that was cut, and the next content backup sent the leftover as a ROM).
781: TREE_CLEAN=/storage/.cache/cloud_sync/restore-tree-clean
782: TREE_CLEAN_AT_START=0
783: tree_record_take() { [ -e "${TREE_CLEAN}" ] && TREE_CLEAN_AT_START=1; rm -f "${TREE_CLEAN}" 2>/dev/null; }
784: tree_record_give() { [ "${TREE_CLEAN_AT_START}" = 1 ] && : > "${TREE_CLEAN}" 2>/dev/null; return 0; }
785: sweep_partials() { [ -d "$1" ] || return 0; find "$1" -type f -name '*.????????.partial' -exec rm -f {} + 2>/dev/null; }
786: 
787: # The plan the player agreed to (audit #307 PL-001, F-CS-03). The preview
788: # writes one line per system it checked -- "<sys>|<verb>|<files>|<bytes>",
789: # none included -- under a header naming the moment, whole or not at all,
790: # and only when every system could be told; apply reads it and holds each
791: # system to it: the same verb, no more to remove than the preview counted,
792: # and that count, not its own, is --max-delete. A system the plan does not
793: # name, or whose verb changed since, is refused rather than recomputed and
794: # run. The plan is spent by the apply that reads it, so each apply stands on
795: # the preview that immediately led to it. Device-local, under /storage/.cache
796: # like the stamps: a plan restored onto another device would describe
797: # another card.
798: MATCH_PLAN="/storage/.cache/cloud_sync/content-match-plan"
799: match_plan_write() { # <plan lines>
800:     mkdir -p "$(dirname "${MATCH_PLAN}")" 2>/dev/null
801:     { printf 'plan %s\n' "$(date +%s)"; printf '%s\n' "$1" | grep '|'; } > "${MATCH_PLAN}.tmp.$$" 2>/dev/null \
802:         && mv -f "${MATCH_PLAN}.tmp.$$" "${MATCH_PLAN}" 2>/dev/null \
803:         || { rm -f "${MATCH_PLAN}.tmp.$$" 2>/dev/null; return 1; }
804: }
805: match_plan_of() { # <sys>: its line from the plan, or nothing
806:     [ -n "${MATCH_PLAN_TEXT}" ] || return 1
807:     printf '%s\n' "${MATCH_PLAN_TEXT}" | awk -F'|' -v s="$1" '$1 == s { print; exit }'
808: }
809: 
810: # What a match removed, as rclone reports it (#308 gpt F-CS-26). Before a
811: # system runs, its content files are listed with their sizes by the same
812: # excludes the run uses; its rclone writes a log of its own, whose
813: # "<path>: Deleted" lines name what went; the count and the bytes are
814: # those names looked up in the list, added to the run's totals. The log is
815: # then appended to the script's own.
816: MATCH_LOG=""
817: MATCH_BEFORE=""
818: match_before() { # <sys>
819:     MATCH_LOG=$(mktemp /tmp/cloud-match-log.XXXXXX 2>/dev/null) || MATCH_LOG="/tmp/cloud-match-log.$$"
820:     MATCH_BEFORE=$(mktemp /tmp/cloud-match-before.XXXXXX 2>/dev/null) || MATCH_BEFORE="/tmp/cloud-match-before.$$"
821:     : > "${MATCH_LOG}"
822:     rclone lsf -R --files-only --format "sp" --separator "|" "${DEST}/$1" \
823:         "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" > "${MATCH_BEFORE}" 2>/dev/null
824: }
825: match_count() { # <sys>: adds what the log says went to the totals
826:     local counted cfiles cbytes
827:     counted=$(awk -F'|' -v L="${MATCH_BEFORE}" '
828:         BEGIN { while ((getline x < L) > 0) { i = index(x, "|"); sz[substr(x, i + 1)] = substr(x, 1, i - 1) } }
829:         / : .*: Deleted$/ { p = $0; sub(/^.* : /, "", p); sub(/: Deleted$/, "", p); n++; b += sz[p] }
830:         END { print n + 0 "|" b + 0 }' "${MATCH_LOG}" 2>/dev/null)
831:     IFS='|' read -r cfiles cbytes <<< "${counted:-0|0}"
832:     [ "${cfiles}" -gt 0 ] 2>/dev/null && PROGRESS_MADE=1
833:     # A sync's copies down are progress too (G-A-08).
834:     grep -qE ': (Copied|Moved) \(' "${MATCH_LOG}" 2>/dev/null && PROGRESS_MADE=1
835:     total_removed=$((total_removed + cfiles))
836:     total_bytes=$((total_bytes + cbytes))
837:     removed_detail="${removed_detail}${removed_detail:+,}$1:${cfiles}:${cbytes}"
838:     cat "${MATCH_LOG}" >> "${LOG_FILE}" 2>/dev/null
839:     rm -f "${MATCH_LOG}" "${MATCH_BEFORE}"
840: }
841: 
842: match_run() {
843:     local apply="$1" sys line verb files bytes rc=0 sync_rc=0 del_rc=0 total_removed=0
844: 
845:     # The exclusions are the only thing standing between this and somebody's
846:     # saves, so assert they exist rather than trusting the file's layout. An
847:     # unset array expands to nothing and rclone would happily proceed.
848:     if [ ${#SAVE_EXCLUDES[@]} -eq 0 ] || [ ${#METADATA_EXCLUDES[@]} -eq 0 ]; then
849:         echo "Refusing: the rules that keep your saves safe aren't loaded."
850:         log_message "match: refused, exclusion arrays empty"
851:         return 1
852:     fi
853: 
854:     # The preview is read-only and may run beside a transfer; applying is one.
855:     if [ "${apply}" = "1" ]; then
856:         take_cloud_lock
857:         [ "$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)" = "${REMOTENAME}" ] || return 1
858:     fi
859:     # As at the foot of the script: the rest of the run cannot leak the
860:     # lock into rclone. Closing a descriptor that was never opened (the
861:     # preview, which takes no lock) is a no-op.
862:     {
863: 
864:     if ! cloud_root_populated; then
865:         echo "Refusing to change anything: your cloud's ROMs and BIOS folder looks empty."
866:         echo "That looks the same whether it really is empty, you're offline, or the"
867:         echo "folder was renamed - so nothing is removed."
868:         log_message "match: refused, content root lists nothing"
869:         # One of the three it can tell apart: with the network gone the
870:         # refusal is the no-network skip, and says so with the code
871:         # EmulationStation names. Nothing ran, so no stamp.
872:         if network_gone; then
873:             echo "Skipped: there's no network connection. Try again when you're online."
874:             log_message "match: skipped, no network"
875:             exit "${EXIT_NO_NETWORK}"
876:         fi
877:         return 1
878:     fi
879: 
880:     mapfile -t SYS < <(selected_systems)
881:     if [ ${#SYS[@]} -eq 0 ]; then
882:         echo "You haven't picked any systems for this device yet."
883:         return 1
884:     fi
885: 
886:     # The plan (PL-001): a preview starts from none and writes its own at the
887:     # end; an apply reads the one the preview left and spends it before
888:     # anything runs, so a second apply cannot stand on the same agreement.
889:     MATCH_PLAN_TEXT=""
890:     local plan_lines="" pverb pfiles pbytes
891:     if [ "${apply}" = "1" ]; then
892:         if [ -s "${MATCH_PLAN}" ] && head -1 "${MATCH_PLAN}" | grep -q '^plan [0-9][0-9]*$'; then
893:             MATCH_PLAN_TEXT=$(tail -n +2 "${MATCH_PLAN}")
894:         fi
895:         rm -f "${MATCH_PLAN}" 2>/dev/null
896:         # Spent means gone (the audit of the fix round, lead G2-A-04): a
897:         # plan the cache would not let go stayed for the next apply, which
898:         # then stood on a preview it did not follow. One that cannot be
899:         # removed is not used.
900:         if [ -e "${MATCH_PLAN}" ]; then
901:             echo "Nothing was removed: something went wrong on this device. Try again."
902:             log_message "match: refused, the preview plan ${MATCH_PLAN} could not be removed, so it could not be spent"
903:             say_why "SOMETHING WENT WRONG"
904:             record_outcome content-match 1
905:             return 1
906:         fi
907:         if [ -z "${MATCH_PLAN_TEXT}" ]; then
908:             # No check behind this apply at all -- run on its own, or run
909:             # again after the apply that spent the plan -- is not a change
910:             # since a check; the why names what is missing (vm-qa run 68:
911:             # the round-trip ran --apply alone and was told SOMETHING
912:             # CHANGED SINCE YOU CHECKED).
913:             echo "Nothing was removed: check what would change first, then try again."
914:             log_message "match: refused, no preview plan to apply"
915:             say_why "CHECK WHAT WOULD CHANGE FIRST"
916:             record_outcome content-match 1
917:             return 1
918:         fi
919:         # It writes into the saves restore's tree (G-A-07).
920:         tree_record_take
921:     else
922:         rm -f "${MATCH_PLAN}" 2>/dev/null
923:     fi
924: 
925:     # What the page that runs this shows when it is done. A match is mostly
926:     # deletion, and rclone's own totals for a deletion read "0 B / 0 B" --
927:     # true and useless (maintainer, 2026-09-07). So each system is announced
928:     # as a unit while it runs, and the summary at the end names what went:
929:     # the numbers the confirmation showed, per system, so the last screen
930:     # answers the first one.
931:     local total_bytes=0 removed_detail="" unit_i=0 unit_n=${#SYS[@]} planned
932:     for sys in "${SYS[@]}"; do
933:         set_system_save_excludes "${sys}"
934:         unit_i=$((unit_i + 1))
935:         # Every chosen system is an item on the page, announced before its
936:         # own dry run -- so the page names what is being checked while the
937:         # check runs -- and announced whether or not it turns out to need
938:         # anything. The page shows ITEM i OF n with this script's n, so n has
939:         # to be the number of announcements the run makes and i their running
940:         # count; until 2026-09-09 a system with nothing to do was skipped
941:         # without one, and a run over three systems ended on ITEM 2 OF 3
942:         # (#95). "Already matches the cloud" is that item's outcome, not a
943:         # reason to hide it, and counting the work first would have held the
944:         # page on WORKING with no item through one dry run per system. The
945:         # preview (apply=0) prints plan lines for the confirmation and no
946:         # markers, as before.
947:         [ "${apply}" = "1" ] && echo ">>> unit ${sys}|${unit_i}|${unit_n}"
948:         planned=$(match_plan_one "${sys}")
949:         IFS='|' read -r _ verb files bytes <<< "${planned}"
950:         if [ "${apply}" = "1" ] && [ "${verb}" != "fail" ] && [ "${verb}" != "none" ]; then
951:             # Held to the preview: the same verb, and no more to remove than
952:             # it counted -- a ROM added since, or a system gone from the
953:             # cloud since, is not what the player agreed to. The preview's
954:             # count, not this one, is what --max-delete is given.
955:             pverb=""; pfiles=""; pbytes=""
956:             IFS='|' read -r _ pverb pfiles pbytes <<< "$(match_plan_of "${sys}")"
957:             if [ -z "${pverb}" ] || [ "${verb}" != "${pverb}" ] \
958:                || ! [ "${files}" -le "${pfiles:-0}" ] 2>/dev/null; then
959:                 echo "Nothing was removed from ${sys}: it changed since you checked. Check again to see what would change."
960:                 log_message "match: ${sys} refused: previewed ${pverb:-nothing}|${pfiles:--}, now ${verb}|${files}"
961:                 say_why "SOMETHING CHANGED SINCE YOU CHECKED"
962:                 rc=1
963:                 continue
964:             fi
965:             files="${pfiles}"; bytes="${pbytes}"
966:         fi
967:         [ "${apply}" = "1" ] || plan_lines="${plan_lines}${planned}"$'\n'
968:         case "${verb}" in
969:             fail)
970:                 # A system that could not be told is neither planned nor
971:                 # touched (PL-001). With the network gone the run is the
972:                 # no-network skip, as everywhere else here; otherwise the
973:                 # preview says so and plans nothing, and an apply says why.
974:                 if [ "${apply}" = "1" ]; then
975:                     echo "Couldn't check ${sys} against your cloud, so nothing was removed from it."
976:                 else
977:                     echo "Couldn't check ${sys} against your cloud. Try again."
978:                 fi
979:                 if network_gone; then
980:                     if [ "${apply}" = "1" ]; then
981:                         echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
982:                         stop_no_network match "${files}" "checking ${sys} against the cloud"
983:                     fi
984:                     echo "Skipped: there's no network connection. Try again when you're online."
985:                     exit "${EXIT_NO_NETWORK}"
986:                 fi
987:                 [ "${apply}" = "1" ] && say_why "$(why_for "${files}")"
988:                 rc=${files}
989:                 [ "${rc}" -ne 0 ] 2>/dev/null || rc=1
990:                 continue
991:             ;;
992:             none)
993:                 [ "${apply}" = "1" ] && echo "Nothing to remove from ${sys}: it already matches the cloud."
994:                 continue
995:             ;;
996:             remove)
997:                 if [ "${apply}" = "1" ]; then
998:                     echo "Removing ${files} files from ${sys} that aren't in your cloud..."
999:                     match_before "${sys}"
1000:                     rclone delete "${DEST}/${sys}" \
1001:                         "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
1002:                         --max-delete "${files}" \
1003:                         --log-file "${MATCH_LOG}" --log-level INFO
1004:                     del_rc=$?
1005:                     match_count "${sys}"
1006:                     if [ ${del_rc} -ne 0 ]; then
1007:                         rc=${del_rc}
1008:                         log_message "match: removing ${sys}: rclone exit ${del_rc}"
1009:                         echo "Couldn't finish removing files from ${sys}: $(why_for "${del_rc}" | tr 'A-Z' 'a-z')."
1010:                         say_why "$(why_for "${del_rc}")"
1011:                     fi
1012:                     rmdir "${DEST}/${sys}" 2>/dev/null
1013:                 else
1014:                     echo "${sys}|remove|${files}|${bytes}"
1015:                 fi
1016:             ;;
1017:             sync)
1018:                 if [ "${apply}" = "1" ]; then
1019:                     echo "Matching ${sys} to the cloud..."
1020:                     # --max-delete is the fail-closed half: if reality has
1021:                     # drifted from the preview the player agreed to, this
1022:                     # aborts rather than deleting more than they saw.
1023:                     #
1024:                     # It is a cap, not a transaction. Measured on rclone
1025:                     # 1.75.0: given three deletions and --max-delete 2, it
1026:                     # exits 7 having already removed two. So it bounds the
1027:                     # damage to what was previewed and does not undo it --
1028:                     # the removals are final (D-CLOUD-023), which is why a
1029:                     # count above the preview's is refused before this runs.
1030:                     match_before "${sys}"
1031:                     bounded_content_rclone sync "$(remote_for "${sys}")" "${DEST}/${sys}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
1032:                         "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${METADATA_EXCLUDES[@]}" \
1033:                         --max-delete "${files}" \
1034:                         --progress --stats 1s \
1035:                         --log-file "${MATCH_LOG}" --log-level INFO
1036:                     sync_rc=$?
1037:                     match_count "${sys}"
1038:                     if [ ${sync_rc} -ne 0 ]; then
1039:                         rc=${sync_rc}
1040:                         sweep_partials "${DEST}/${sys}"
1041:                         # A failed unit says why: the network gone ends the
1042:                         # run as 69 here, anything else carries rclone's own
1043:                         # code up as before. Before the 69 exit, the running
1044:                         # totals go out on the same `>>> removed` line the
1045:                         # completed run prints, so the page can report the
1046:                         # deletions that did happen -- a match is mostly
1047:                         # deletion, and it had already run for every system
1048:                         # before this one (D-UI-028; #105). The totals are
1049:                         # what rclone reports removed (match_count), within
1050:                         # what the player agreed to; what was removed is what
1051:                         # the cloud does not have, so it is gone (D-CLOUD-023).
1052:                         if network_gone; then
1053:                             echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
1054:                             stop_no_network match "${sync_rc}" "matching ${sys} to the cloud"
1055:                         fi
1056:                         log_message "match: matching ${sys}: rclone exit ${sync_rc}"
1057:                         echo "Couldn't finish matching ${sys} to the cloud: $(why_for "${sync_rc}" | tr 'A-Z' 'a-z')."
1058:                         say_why "$(why_for "${sync_rc}")"
1059:                     fi
1060:                 else
1061:                     # The bytes the dry run counted, so the confirmation and
1062:                     # the done page agree (the preview said 78 KB where the
1063:                     # page then said 224 KB, 2026-09-07).
1064:                     echo "${sys}|sync|${files}|${bytes}"
1065:                 fi
1066:             ;;
1067:             *)
1068:                 # match_plan_one prints none, remove or sync; anything else
1069:                 # is a failure to plan, and an announced item must not end
1070:                 # in silence.
1071:                 [ "${apply}" = "1" ] && echo "Couldn't check ${sys} against the cloud."
1072:                 log_message "match: no plan for ${sys} (${planned})"
1073:                 rc=1
1074:             ;;
1075:         esac
1076:     done
1077: 
1078:     # The preview's plan, only when every system could be told: a preview
1079:     # that could not see one system offers nothing to apply.
1080:     if [ "${apply}" != "1" ] && [ "${rc}" -eq 0 ]; then
1081:         if ! match_plan_write "${plan_lines}"; then
1082:             echo "Couldn't keep track of what would change, so nothing can be removed yet. Try again."
1083:             log_message "match: the plan could not be written to ${MATCH_PLAN}"
1084:             rc=1
1085:         fi
1086:     fi
1087: 
1088:     if [ "${apply}" = "1" ]; then
1089:         # ">>> removed 14|314572800|snes:12:300000000,gb:2:14572800" -- the
1090:         # page renders it on its last screen. The counts are the files rclone
1091:         # reports it removed, with the sizes listed before it ran (#308 gpt
1092:         # F-CS-26); they were the preview's, and a system one of whose
1093:         # deletions failed was reported as though all of them had happened.
1094:         # --max-delete holds each system to the preview's count.
1095:         echo ">>> removed ${total_removed}|${total_bytes}|${removed_detail}"
1096:         log_message "match: applied, removed ${total_removed} files, rc=${rc}"
1097:         tree_record_give
1098:         # The page that ran it fades; the row in the menu has to be able to
1099:         # answer "did that work?" afterwards, like every other cloud action.
1100:         record_outcome content-match "${rc}"
1101:     fi
1102:     return ${rc}
1103:     } 9>&-
1104: }
1105: 
1106: content_files() {
1107:     local dir="$1"; shift
1108:     # One rule for both sides (D-CLOUD-048), set by MEDIA_MODE (D-CLOUD-050):
1109:     #   roms  -- ROMs and BIOS only: the scraper's folders and the game list
1110:     #            are neither listed nor moved
1111:     #   with  -- ROMs and game content together
1112:     #   only  -- game content alone: the scraper's folders and gamelist.xml
1113:     # The game list is game content (D-CLOUD-049): the scraper writes it
1114:     # beside the artwork, and a restored-then-scraped device must read as
1115:     # matching its cloud under ROMs alone. At any depth, as the transfers
1116:     # move it (the ROMs pass excludes "**/gamelist.xml", the game-list pass
1117:     # includes it): a list below a system's own folder was counted as a ROM
1118:     # (the audit of the fixes, G-A-10).
1119:     local -a media=()
1120:     local d
1121:     case "${MEDIA_MODE:-roms}" in
1122:         roms) for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( ! -path "${dir%/}/${d}/*" ); done
1123:               media+=( ! -name gamelist.xml ) ;;
1124:         only) media+=( "(" -name gamelist.xml )
1125:               for d in ${MEDIA_DIRS:-images videos manuals screenshots fanart boxart wheel mix maps media}; do media+=( -o -path "${dir%/}/${d}/*" ); done
1126:               media+=( ")" ) ;;
1127:     esac
1128:     local -a native_states=()
1129:     if [ "${dir%/}" = "${DEST}/n64" ]; then
1130:         native_states=( "(" -path "${dir%/}/*/*" -o "(" ! -name '*.st[0-9]' ! -name '*.pj[0-9]' ! -name '*.pj[0-9].zip' ")" ")" )
1131:     fi
1132:     find "${dir}" -type f \
1133:         ! -name '*.srm' ! -name '*.sav' ! -name '*.fs' ! -name '*.state*' \
1134:         ! -name '*.auto' ! -name '*.dsv*' ! -name '*.eep' ! -name '*.mpk' \
1135:         ! -name '*.sra' ! -name '*.fla' ! -name '*.mcd' ! -name '*.mcr' \
1136:         ! -path '*/save/*' ! -path '*/memcards/*' \
1137:         ! -path '*/shared/savefiles/*' ! -path '*/PPSSPP/*' \
1138:         ! -path '*/PSP/SAVEDATA/*' \
1139:         ! -path '*conflicted copy*' ! -name '*.sync-conflict-*' \
1140:         ! -name '*.????????.partial' \
1141:         ! -path "${dir%/}/README.txt" \
1142:         "${native_states[@]}" "${media[@]}" "$@" 2>/dev/null
1143: }
1144: # Local systems that hold content, for the union scan.
1145: local_content_dirs() {
1146:     local d base
1147:     for d in "${DEST}"/*/; do
1148:         [ -d "${d}" ] || continue
1149:         base=$(basename "${d}")
1150:         case "${base}" in savefiles|savestates|screenshots|backup) continue ;; esac
1151:         content_files "${d}" | head -1 | grep -q . && printf '%s\n' "${base}"
1152:     done
1153: }
1154: # What a copy from side $1 to side $2 would move, as "count|bytes". Both
1155: # files are "size|relpath" listings, and a line matches only when the far
1156: # side has the same name at the same size -- so a file absent over there
1157: # counts, and so does one present at a different size, which is what
1158: # `rclone copy` compares (size, then modtime where the backend keeps one).
1159: # A same-size file is NOT counted whatever changed inside it: these listings
1160: # carry name and size only, so a file rewritten to the same length -- a
1161: # patched ROM, a re-saved config -- reads as present, though a copy would
1162: # move it on modtime or hash. The figure here can therefore run under what
1163: # a copy moves, never over. The caller also strips the game list from both
1164: # listings first (see --scan): its direction is decided by a modtime these
1165: # listings do not carry, so a differing size is not a direction. The count
1166: # and the bytes describe one set, so a page can put them on one line without
1167: # contradicting itself; until 2026-09-08 the count compared names alone and
1168: # would have read "0 FILES" beside a non-zero size for a ROM re-uploaded at
1169: # a new size.
1170: # Not comm(1): the image's busybox has no comm, and `comm ... | wc -l` then
1171: # reads 0 -- "nothing differs" -- which is the wrong way for a count to fail
1172: # (found in the VM, 2026-09-06). awk is what this script already runs on;
1173: # the getline form is safe when either file is empty, where the NR==FNR
1174: # idiom is not.
1175: delta_of() {
1176:     awk -F'|' -v L="$2" 'BEGIN { while ((getline x < L) > 0) a[x] = 1 }
1177:         !($0 in a) { n++; b += $1 } END { print n+0 "|" b+0 }' "$1"
1178: }
1179: # Drop from a cloud "size|path" listing what content_files drops locally, so
1180: # the two sides are counted by one rule.
1181: #
1182: # The same set content_files and the transfers describe (#308 gpt F-CS-30):
1183: # a save folder at any depth -- save/, memcards/, PPSSPP/ and dc's
1184: # shared/savefiles/, as the local find and the unanchored rclone excludes
1185: # have them -- and the setup's note at a unit's root (a README.txt directly
1186: # in a system's folder), which neither side carries. A README deeper in a
1187: # game's folder is that game's, and is content on both sides. This used to
1188: # look for save folders one level down only, missed shared/savefiles, and
1189: # dropped every README at any depth, so a restored system read as differing
1190: # from its own cloud copy.
1191: cloud_content_filter() {
1192:     local dirs; dirs="^($(echo ${MEDIA_DIRS} | tr ' ' '|'))$"
1193:     awk -F'|' -v dirs="${dirs}" -v mode="${MEDIA_MODE}" '
1194:         { n = split($2, seg, "/"); if (n < 2) next
1195:           f = seg[n]
1196:           if (seg[1] == "n64" && n == 2 && f ~ /\.(st[0-9]|pj[0-9](\.zip)?)$/) next
1197:           game = (n > 2 && seg[2] ~ dirs) || f == "gamelist.xml"
1198:           if (mode == "roms" && game) next
1199:           if (mode == "only" && !game) next
1200:           if (f ~ /\.(srm|sav|fs|auto|eep|mpk|sra|fla|mcd|mcr)$/ || f ~ /\.state/ || f ~ /\.dsv/) next
1201:           if ($2 ~ /conflicted copy/ || f ~ /\.sync-conflict-/) next
1202:           if (f ~ /\.[^.\/][^.\/][^.\/][^.\/][^.\/][^.\/][^.\/][^.\/]\.partial$/) next
1203:           if (n == 2 && f == "README.txt") next
1204:           for (i = 2; i < n; i++) {
1205:               if (seg[i] == "save" || seg[i] == "memcards" || seg[i] == "PPSSPP") next
1206:               if (seg[i] == "shared" && i + 1 < n && seg[i + 1] == "savefiles") next
1207:               if (seg[i] == "PSP" && i + 1 < n && seg[i + 1] == "SAVEDATA") next
1208:           }
1209:           print }'
1210: }
1211: # --with-media: include scraped game content (D-CLOUD-048). Off by default:
1212: # the scraper's folders under a system are neither moved nor counted unless
1213: # the switch is on, so a restored-then-scraped device does not read as
1214: # "different" from its cloud copy. Taken from anywhere on the command line.
1215: MEDIA_MODE=roms
1216: _ARGS=()
1217: for _a in "$@"; do
1218:     case "${_a}" in
1219:         --with-media) MEDIA_MODE=with ;;
1220:         --media-only) MEDIA_MODE=only ;;
1221:         *) _ARGS+=("${_a}") ;;
1222:     esac
1223: done
1224: set -- "${_ARGS[@]}"
1225: MEDIA_DIRS="images videos manuals screenshots fanart boxart wheel mix maps media"
1226: # What the main rclone pass carries, per mode. The game list never rides the
1227: # main pass: it has its own --update pass below (newest wins), which runs
1228: # only when game content is in scope.
1229: MEDIA_EXCLUDES=()
1230: case "${MEDIA_MODE}" in
1231:     roms) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--exclude "/${_d}/**"); done ;;
1232:     only) for _d in ${MEDIA_DIRS}; do MEDIA_EXCLUDES+=(--include "/${_d}/**"); done ;;
1233: esac
1234: 
1235: case "${1}" in
1236:     --match)
1237:         # Preview by default; --apply is what deletes.
1238:         if [ "${2}" = "--apply" ]; then
1239:             match_run 1
1240:         else
1241:             match_run 0
1242:         fi
1243:         exit $?
1244:     ;;
1245:     --scan)
1246:         # One line per system in the union of cloud and device:
1247:         #   name|cloud_bytes|supported|device_bytes|files_in_cloud_not_here|files_here_not_in_cloud|bytes_in_cloud_not_here|bytes_here_not_in_cloud
1248:         # Both sides listed by the same rule (D-CLOUD-048) as "size|relpath"
1249:         # and compared by name and size (delta_of), because totals cannot say
1250:         # whether one side has what the other has. Fields 7 and 8 are what a
1251:         # copy in that direction would send; fields 5 and 6 count the same
1252:         # set. The game list is in the totals and never in the comparison
1253:         # (below). They arrived 2026-09-08; the first six keep their position
1254:         # and type, so a page built against six still reads this line.
1255:         SUP=$(supported_systems)
1256:         TMP=$(mktemp -d /tmp/cloud-scan.XXXXXX); trap 'rm -rf "${TMP}"' EXIT
1257:         rclone lsf -R --files-only --format "sp" --separator "|" "${ROOT}ROMs/" "${RCLONE_LIST_OPTS[@]}" > "${TMP}/cloud.raw" 2>/dev/null
1258:         scan_rc=$?
1259:         if [ "${scan_rc}" -ne 0 ] && [ -s "${TMP}/cloud.raw" ]; then
1260:             echo "Couldn't finish reading your cloud. Try again." >&2
1261:             exit 5
1262:         fi
1263:         cloud_content_filter < "${TMP}/cloud.raw" > "${TMP}/cloud"
1264:         # A code other than 3 from a folder that is simply not there yet
1265:         # (a server whose "missing" rclone does not map to "not found",
1266:         # #142) is an empty cloud, not one that could not be read.
1267:         if [ "${scan_rc}" -ne 0 ] && [ "${scan_rc}" -ne 3 ] && absent_not_broken "${ROOT}ROMs/"; then
1268:             log_message "scan: ROMs is not there yet (rclone exit ${scan_rc}; its nearest listable parent lacks it)"
1269:             scan_rc=3
1270:         fi
1271:         # BIOS is the ROMs tier's, never game content's: under --media-only it
1272:         # is not listed, so the union does not carry a line the page would
1273:         # skip and the log would puzzle over (3608 cloud BIOS files "not on
1274:         # this device" under game content alone, RG35XX SP, 2026-09-06).
1275:         if [ "${MEDIA_MODE}" != only ]; then
1276:             rclone lsf -R --files-only --format "sp" --separator "|" "${ROOT}BIOS/" "${RCLONE_LIST_OPTS[@]}" > "${TMP}/bios.raw" 2>/dev/null
1277:             bios_rc=$?
1278:             if [ "${bios_rc}" -ne 0 ] && [ -s "${TMP}/bios.raw" ]; then
1279:                 echo "Couldn't finish reading your cloud. Try again." >&2
1280:                 exit 5
1281:             fi
1282:             grep -v '^[0-9]*|README\.txt$' "${TMP}/bios.raw" | sed 's/|/|bios\//' >> "${TMP}/cloud"
1283:             if [ "${bios_rc}" -ne 0 ] && [ "${bios_rc}" -ne 3 ] && absent_not_broken "${ROOT}BIOS/"; then
1284:                 log_message "scan: BIOS is not there yet (rclone exit ${bios_rc}; its nearest listable parent lacks it)"
1285:                 bios_rc=3
1286:             fi
1287:             # Keep the code that says the most. A missing folder is rclone's
1288:             # 3 and the one code an empty cloud gives, so a ROMs listing the
1289:             # cloud refused (5, 7) must not be overwritten by a BIOS folder
1290:             # that merely is not there yet.
1291:             if [ "${bios_rc}" -ne 0 ] && { [ "${scan_rc}" -eq 0 ] || [ "${scan_rc}" -eq 3 ]; }; then
1292:                 scan_rc=${bios_rc}
1293:             fi
1294:         fi
1295:         # A listing that failed with the network gone is not an empty cloud,
1296:         # and the page must not be handed one: every system on the device
1297:         # would read as "not in your cloud yet". Say why, print no lines,
1298:         # and exit the code EmulationStation names. A listing that failed
1299:         # with the network up -- no ROMs folder yet, rclone's 3 -- is an
1300:         # empty cloud, and goes on as before.
1301:         if [ "${scan_rc}" -ne 0 ] && network_gone; then
1302:             log_message "scan: skipped, no network (rclone exit ${scan_rc})"
1303:             echo "Skipped: there's no network connection. Try again when you're online." >&2
1304:             exit "${EXIT_NO_NETWORK}"
1305:         fi
1306:         # A listing that failed with the network up is not an empty cloud
1307:         # either, unless the failure is that the folder is not there: rclone's
1308:         # 3, "directory not found", is what a cloud nothing has been backed up
1309:         # to yet answers, and goes on as before. Anything else -- the cloud
1310:         # refused the connection, rejected the sign-in, or answered with an
1311:         # error -- is a cloud that could not be read, and the page must say
1312:         # so rather than list every system on the device as "not yet in your
1313:         # cloud" (a refused port exited 5 and the picker offered the whole
1314:         # device for upload, 2026-09-10; D-CLOUD-077). rclone's code goes up
1315:         # unchanged: the sentinels are 75 and 69, which rclone never returns.
1316:         if [ "${scan_rc}" -ne 0 ] && [ "${scan_rc}" -ne 3 ]; then
1317:             log_message "scan: the cloud could not be read (rclone exit ${scan_rc})"
1318:             echo "Couldn't finish reading your cloud. Try again." >&2
1319:             exit "${scan_rc}"
1320:         fi
1321:         {
1322:             cut -d'|' -f2 "${TMP}/cloud" | cut -d/ -f1
1323:             local_content_dirs
1324:         } | sort -u | while IFS= read -r name; do
1325:             [ -n "${name}" ] || continue
1326:             # This system's cloud side, "size|relpath" under the system.
1327:             awk -F'|' -v n="${name}" '{ split($2, seg, "/"); if (seg[1] == n) print $1 "|" substr($2, length(n) + 2) }' "${TMP}/cloud" > "${TMP}/c"
1328:             # The device side by the same rule. One find per system: stat
1329:             # supplies the sizes, so the total needs no second pass. The
1330:             # prefix is cut by length, not by pattern, so a system name
1331:             # holding a regex character cannot mis-strip.
1332:             if [ -d "${DEST}/${name}" ]; then
1333:                 content_files "${DEST}/${name}" -exec stat -c '%s|%n' {} + \
1334:                     | awk -v p="${DEST}/${name}/" '{ i = index($0, "|"); print substr($0, 1, i) substr($0, i + 1 + length(p)) }' > "${TMP}/l"
1335:             else
1336:                 : > "${TMP}/l"
1337:             fi
1338:             cbytes=$(awk -F'|' '{ t += $1 } END { print t+0 }' "${TMP}/c")
1339:             lbytes=$(awk -F'|' '{ t += $1 } END { print t+0 }' "${TMP}/l")
1340:             # The game list is in those totals and out of the comparison.
1341:             # Under game content it travels in its own pass, --update, newest
1342:             # wins (the transfer below); these listings carry no modtime to
1343:             # say which side that is, so a size that differs is not a
1344:             # direction, and a page that counted it read "1 FILE TO RESTORE"
1345:             # on whichever side's list was older -- and kept reading it,
1346:             # since a run moves nothing that way (found in review,
1347:             # 2026-09-08). Any depth, as the transfer's "**/gamelist.xml".
1348:             # Under ROMs alone a system's own list is on neither side, so
1349:             # there the strip touches only a list nested in a subfolder.
1350:             grep -vE '[|/]gamelist\.xml$' "${TMP}/c" > "${TMP}/cd"
1351:             grep -vE '[|/]gamelist\.xml$' "${TMP}/l" > "${TMP}/ld"
1352:             IFS='|' read -r cnl cnl_bytes <<< "$(delta_of "${TMP}/cd" "${TMP}/ld")"
1353:             IFS='|' read -r lnc lnc_bytes <<< "$(delta_of "${TMP}/ld" "${TMP}/cd")"
1354:             if [ "${name}" = "bios" ] || printf '%s\n' "${SUP}" | grep -qxF "${name}"; then sup=1; else sup=0; fi
1355:             echo "${name}|${cbytes}|${sup}|${lbytes}|${cnl}|${lnc}|${cnl_bytes}|${lnc_bytes}"
1356:         done
1357:         exit 0
1358:     ;;
1359:     --systems)
1360:         selected_systems
1361:         exit 0
1362:     ;;
1363:     --set-systems)
1364:         shift
1365:         # System folder names, and nothing else (audit #307 PL-030). The
1366:         # picker passes the names it read from the cloud, joined by spaces,
1367:         # and every one of them goes on to name a folder under /storage/roms
1368:         # and in the cloud; one that is not a folder's name -- a character
1369:         # the shell would act on, a glob, "..", a leading dash a later grep
1370:         # would take as an option -- is refused, and the whole selection
1371:         # with it, so nothing is half-written. The names are split with
1372:         # globbing off: `printf $*` expanded "*" against the working folder.
1373:         local_names=()
1374:         set -f
1375:         read -r -a local_names <<< "$*"
1376:         set +f
1377:         for _n in "${local_names[@]}"; do
1378:             if ! [[ "${_n}" =~ ^[A-Za-z0-9_][A-Za-z0-9._-]*$ ]]; then
1379:                 echo "Nothing was changed: \"${_n}\" isn't the name of a system folder."
1380:                 log_message "set-systems: refused, not a system folder name: ${_n}"
1381:                 exit 1
1382:             fi
1383:         done
1384:         mkdir -p "$(dirname "${SELECTION}")" 2>/dev/null
1385:         # An empty selection is a real answer ("none"), distinct from never
1386:         # having chosen; the file exists either way. Which is exactly why it
1387:         # is written whole or not at all: a kill mid-write left an empty
1388:         # file, and an empty file is a different valid choice -- every later
1389:         # --selected then said no systems were selected (D-CLOUD-078, #105).
1390:         { [ ${#local_names[@]} -eq 0 ] || printf '%s\n' "${local_names[@]}"; } > "${SELECTION}.tmp.$$" 2>/dev/null
1391:         mv -f "${SELECTION}.tmp.$$" "${SELECTION}" 2>/dev/null || rm -f "${SELECTION}.tmp.$$"
1392:         echo "OK $(selected_systems | wc -l) selected"
1393:         exit 0
1394:     ;;
1395:     --selected)
1396:         mapfile -t DIRS < <(selected_systems)
1397:         # BIOS is not a system and is no longer a pick (maintainer, 2026-09-06):
1398:         # it comes with the tier whenever the cloud has it. The tier's own
1399:         # switch already says ROMS AND BIOS; nothing runs without them. A
1400:         # "bios" line in the selection -- the placeholder the interface wrote
1401:         # so that BIOS alone was not refused -- is the same thing: remote_for
1402:         # sends it to BIOS/, one unit, never to a system folder under ROMs/.
1403:         if [ "${MEDIA_MODE}" != only ] && exists_remote "${ROOT}BIOS" && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
1404:             DIRS+=("bios")
1405:         fi
1406:         # Refused only when there is nothing at all -- after BIOS is added,
1407:         # not before: "BIOS and no system" is a selection, and was refused
1408:         # as none (coordinator's row under audit #307 PL-012).
1409:         if [ ${#DIRS[@]} -eq 0 ]; then
1410:             echo "You haven't picked any systems for this device."
1411:             exit 1
1412:         fi
1413:     ;;
1414:     --list)
1415:         list_content_dirs "${ROOT}ROMs/" || exit $?
1416:         printf '%s\n' "${LISTED}" | sed 's:/$::; /^$/d' | sort -u
1417:         exit 0
1418:     ;;
1419:     --all)
1420:         # Only the selected structured library; every listing must succeed
1421:         # before any transfer. Missing folders never select another library.
1422:         all_listing() { # <path>: LISTED=its folders; the run stops when it cannot be read
1423:             local path="$1" lrc
1424:             list_content_dirs "${path}"; lrc=$?
1425:             [ "${lrc}" -eq 0 ] && return 0
1426:             log_message "restore --all: ${path} could not be listed (rclone exit ${lrc})"
1427:             if network_gone; then
1428:                 echo "Skipped: there's no network connection. Try again when you're online."
1429:                 exit "${EXIT_NO_NETWORK}"
1430:             fi
1431:             echo "Couldn't finish: your cloud couldn't be read, so nothing was restored. Try again."
1432:             say_why "$(why_for "${lrc}")"
1433:             record_outcome content-restore "${lrc}"
1434:             exit "${lrc}"
1435:         }
1436:         all_listing "${ROOT}ROMs/"
1437:         ALL_ROMS=$(printf '%s\n' "${LISTED}" | sed 's:/$::')
1438:         all_listing "${ROOT}"
1439:         # BIOS is there when the content root lists it (a folder with files,
1440:         # or a directory marker) -- what exists_remote asked, from the same
1441:         # listing, read fail-closed.
1442:         ALL_BIOS=0; printf '%s\n' "${LISTED}" | grep -qx 'BIOS/' && ALL_BIOS=1
1443:         mapfile -t DIRS < <(printf '%s\n' "${ALL_ROMS}" | grep -v '^$' | sort -u)
1444:         # BIOS as --selected brings it: whenever the cloud has it, and not
1445:         # with game content alone.
1446:         if [ "${MEDIA_MODE}" != only ] && [ "${ALL_BIOS}" -eq 1 ] && ! printf '%s\n' "${DIRS[@]}" | grep -qx bios; then
1447:             DIRS+=("bios")
1448:         fi
1449:         if [ ${#DIRS[@]} -eq 0 ]; then
1450:             echo "Nothing to restore: your cloud has no ROMs or BIOS files yet."
1451:             log_message "restore --all: nothing in the cloud's ROMs or BIOS folders"
1452:             record_outcome content-restore 0
1453:             exit 0
1454:         fi
1455:     ;;
1456:     "")
1457:         echo "Usage: ${SCRIPT_NAME} --list | --all | <dir> [<dir>...]" >&2
1458:         exit 1
1459:     ;;
1460:     *)
1461:         DIRS=("$@")
1462:     ;;
1463: esac
1464: 
1465: 
1466: 
1467: for DIR in "${DIRS[@]}"; do
1468:     if ! [[ "${DIR}" =~ ^[A-Za-z0-9_][A-Za-z0-9._-]*$ ]]; then
1469:         echo "That system folder name can't be used. Nothing was restored."
1470:         exit 1
1471:     fi
1472: done
1473: 
1474: STATUS=0
1475: take_cloud_lock
1476: # Everything from here to the end of the script runs with the lock
1477: # descriptor closed, so no child of this run can hold the lock once this
1478: # shell is gone -- see take_cloud_lock. The brace group is the whole of
1479: # the change: it adds no subshell, so exits, traps and variables behave
1480: # exactly as they did.
1481: {
1482: # Settings may change while the interactive preview is open. Re-check under
1483: # the transfer lock before sending anything to the previously named cloud.
1484: if [ "$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)" != "${REMOTENAME}" ]; then
1485:     echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
1486:     echo "Your cloud connection changed. Start this operation again."
1487:     exit 1
1488: fi
1489: UNIT_N=${#DIRS[@]}; UNIT_I=0
1490: tree_record_take
1491: for DIR in "${DIRS[@]}"; do
1492:     set_system_save_excludes "${DIR}"
1493:     SRC="$(resolve_src "${DIR}")"
1494:     TARGET="${DEST}/${DIR}"
1495:     UNIT_I=$((UNIT_I + 1))
1496:     log_message "Content restore: ${SRC} -> ${TARGET}"
1497:     # The marker the transfer page reads: what is being copied, and which of
1498:     # how many. rclone's own block totals that follow are this system's.
1499:     echo ">>> unit ${DIR:-everything}|${UNIT_I}|${UNIT_N}"
1500:     echo "Restoring ${DIR:-everything} from the cloud..."
1501:     # --progress is what puts the stats on stdout. With only --log-file they
1502:     # go to the log and the caller sees nothing -- which is why the progress
1503:     # card sat at "0 B / 0 B, -, 0 B/s" through a restore that was in fact
1504:     # copying Mega Drive ROMs the whole time. The saves path has always passed
1505:     # it; these two never did.
1506:     #
1507:     # And NOT --stats-one-line: that collapses the display to a totals line,
1508:     # losing the per-file block. A transfer of a thousand small BIOS files
1509:     # spends minutes between percentage changes, and the only thing that says
1510:     # it is alive rather than stuck is the name of the file it is on right
1511:     # now. --stats 1s keeps that moving.
1512:     #
1513:     # No --progress-terminal-width: the flag does not exist on every rclone we
1514:     # ship against (the saves scripts test for it with "rclone help | grep"
1515:     # before using it), and an unknown flag is a usage error that transfers
1516:     # nothing. rclone pads the file name out to a guessed width; the reader
1517:     # trims it, so the flag bought nothing worth a version check.
1518:     # The setup's note at a unit's root (BIOS/README.txt, cloud_setup
1519:     # --seed-folders) is not content, and neither side counts it (#308 gpt
1520:     # F-CS-30): it came down into /storage/roms/bios and read ever after as a
1521:     # file this device has and the cloud does not.
1522:     UNIT_LOG0=$(log_offset)
1523:     bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
1524:         "${SAVE_EXCLUDES[@]}" "${SYSTEM_SAVE_EXCLUDES[@]}" "${CONFLICT_EXCLUDES[@]}" "${MEDIA_EXCLUDES[@]}" \
1525:         --exclude "gamelist.xml" --exclude "**/gamelist.xml" --exclude "/README.txt" \
1526:         --progress --stats 1s \
1527:         --log-file "${LOG_FILE}" --log-level INFO
1528:     RC=$?
1529: 
1530:     # The game list: newest wins, rather than whoever ran last. Game content
1531:     # only (D-CLOUD-049) -- under ROMs alone the file stays where it is. Its
1532:     # result is the unit's, by the same 0|9 rule (audit #307 PL-066): it
1533:     # was discarded with `|| true`, so a game list that did not move left a
1534:     # unit, a stamp and a page that said the unit had.
1535:     if [ "${MEDIA_MODE}" != roms ] && { [ "${RC}" -eq 0 ] || [ "${RC}" -eq 9 ]; }; then
1536:         bounded_content_rclone copy "${SRC}" "${TARGET}" "${RCLONE_NET_OPTS_ARRAY[@]}" \
1537:             "${GAMELIST_ONLY[@]}" --update \
1538:             --stats 0 \
1539:             --log-file "${LOG_FILE}" --log-level INFO
1540:         GL_RC=$?
1541:         case "${RC}" in
1542:             0|9) case "${GL_RC}" in 0|9) ;; *) RC=${GL_RC} ;; esac ;;
1543:         esac
1544:     fi
1545: 
1546:     # What moved in this unit, whatever its result (G-A-08/G-A-13).
1547:     moved_since "${UNIT_LOG0}" && PROGRESS_MADE=1
1548:     if [ ${RC} -ne 0 ] && [ ${RC} -ne 9 ]; then
1549:         # What a failed transfer may have left in this unit's folder goes
1550:         # now (G-A-07).
1551:         sweep_partials "${TARGET}"
1552:         # A failed unit says why: the network gone ends the run as 69 here,
1553:         # anything else carries rclone's own code up as before.
1554:         network_gone && stop_no_network restore "${RC}" "restoring ${DIR:-everything}"
1555:         log_message "restore of ${DIR:-everything}: rclone exit ${RC}"
1556:         echo "Couldn't finish restoring ${DIR:-everything}: $(why_for "${RC}" | tr 'A-Z' 'a-z')."
1557:         say_why "$(why_for "${RC}")"
1558:         STATUS=${RC}
1559:     else
1560:         echo "Restored ${DIR:-everything}."
1561:     fi
1562: done
1563: 
1564: tree_record_give
1565: 
1566: # The progress card is gone by the time somebody who walked away comes back, so
1567: # leave the outcome where the menu can read it later. Device-local state, so it
1568: # lives under /storage/.cache and not in the settings backup.
1569: record_outcome content-restore "${STATUS}"
1570: 
1571: # A failed unit leaves with rclone's own code, unremapped: nothing rclone
1572: # returns can read as the lock sentinel now that it is 75 (#99).
1573: exit ${STATUS}
1574: } 9>&-



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth


## Original lines 1–2679
1: #!/usr/bin/env python3
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_oauth - sign in to a cloud provider from the handheld and a phone.
6: #
7: # rclone's OAuth already works; what it needs is somewhere to happen. Its
8: # `authorize` command runs a web server on 127.0.0.1:53682 and waits for the
9: # provider to redirect a browser back to it -- which assumes the browser is on
10: # the same machine. On a handheld there is no browser at all, so the shipped
11: # path was an SSH session from a computer, tunnelling that port back, and that
12: # is the flow that has failed everyone who has tried it.
13: #
14: # Nothing about the OAuth needs to change. The bytes just have to move:
15: #
16: #   1. `rclone authorize <backend>` starts and prints a local URL.
17: #   2. Following that URL from here yields the provider's real sign-in URL,
18: #      carrying rclone's own client id and its state parameter.
19: #   3. This serves that link on the LAN, so a phone can open it.
20: #   4. The player signs in. The provider redirects the phone to
21: #      localhost:53682, which the phone cannot load -- but the address bar
22: #      now holds ?code=...&state=...
23: #   5. They paste that back here, and this replays it to rclone's waiting
24: #      server, which completes the exchange and prints a token.
25: #   6. The token goes into rclone.conf.
26: #
27: # So no OAuth application is registered by ROCKNIX, no client secret ships, and
28: # no provider-specific code exists here: every backend rclone can authorize
29: # goes through the same six steps. Verified against dropbox, drive, onedrive,
30: # box, pcloud and yandex, which resolve to their own providers unchanged.
31: #
32: #   cloud_oauth serve <backend> [--name NAME] [--port N] [--timeout SECONDS]
33: #   cloud_oauth url                     the full link, PIN included, for a QR
34: #   cloud_oauth info                    URL/ADDRESS/PIN, one KEY=VALUE per line
35: #   cloud_oauth status                  waiting | signed-in | failed | idle
36: #   cloud_oauth cancel
37: #
38: # `url` and `info` differ in what they are for. The QR carries the PIN, so
39: # scanning it skips a step; the handheld's screen shows the bare address and
40: # the PIN apart, because those are read off a small panel and typed on a
41: # phone -- and "?pin=7677" in a URL bar is where that goes wrong.
42: #
43: # The listener binds the LAN only while a sign-in is running, times out on its
44: # own, and requires a PIN shown on the handheld -- so reaching it takes the
45: # device in your hands, not merely a seat on the wifi.
46: 
47: import contextlib
48: import errno
49: import fcntl
50: import hashlib
51: import http.server
52: import itertools
53: import json
54: import os
55: import re
56: import secrets
57: import select
58: import shutil
59: import signal
60: import socket
61: import struct
62: import subprocess
63: import sys
64: import cloud_connections as connections
65: import threading
66: import time
67: import shlex
68: import urllib.parse
69: import urllib.request
70: 
71: STATE_DIR = "/var/run/cloud_oauth"
72: RCLONE = "/usr/bin/rclone"
73: LOCAL_AUTH = "http://127.0.0.1:53682"
74: # How long `rclone authorize` has to print its local link.
75: AUTHORIZE_WAIT = 20
76: LOG_FILE = "/var/log/cloud_sync.log"
77: 
78: 
79: def log(message):
80:     import datetime
81:     stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
82:     try:
83:         with open(LOG_FILE, "a") as handle:
84:             handle.write("[%s] [INFO] [cloud_oauth] %s\n" % (stamp, message))
85:     except OSError:
86:         pass
87: 
88: 
89: def state_path(name):
90:     return os.path.join(STATE_DIR, name)
91: 
92: 
93: def signin_language():
94:     """Use the handheld locale inherited from ES, never the phone's locale.
95: 
96:     EsLocale::changeLocale exports LANGUAGE to its child processes. The locale
97:     environment is the fallback for a sign-in started outside the interface.
98:     Both companion confirmation and native finishing page use this selection.
99:     """
100:     value = next((os.environ[key] for key in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG")
101:                   if os.environ.get(key)), "en")
102:     primary = value.split(":", 1)[0].replace("-", "_").split("_", 1)[0].split(".", 1)[0].lower()
103:     return "fr" if primary == "fr" else "en"
104: 
105: 
106: def phone_page(name, pin):
107:     page = REMOTE_PAGE % {"style": STYLE, "name": name, "pin": pin}
108:     if signin_language() == "fr":
109:         for before, after in (
110:             ("id=leave-ask>Close page", "id=leave-ask>Fermer la page"),
111:             ("<span>Close the sign-in page on your handheld?</span>",
112:              "<span>Fermer la page de connexion sur votre console ?</span>"),
113:             ("id=leave-keep>Keep", "id=leave-keep>Garder ouverte"),
114:             ("id=leave-close>Close", "id=leave-close>Fermer"),
115:         ):
116:             page = page.replace(before, after)
117:     return page
118: 
119: 
120: # session.json is written by three threads of the serve (the collector, the
121: # request handlers, the main thread) and read by other processes (`status`,
122: # `info`, the interface). It was truncated and rewritten in place, and
123: # read_state turns a half-written file into {} -- a status that read idle
124: # for a moment while a sign-in was completing, and a merge that could write
125: # that emptiness back (#308 claude F-RS-23, gpt F-RS-17). So: one writer at
126: # a time within the process, and every write a whole file renamed over the
127: # old one, which a reader in any process sees before or after, never during.
128: #
129: # And one writer across processes too: a serve being cancelled and the one
130: # replacing it write the same file, so a read-modify-write holds an flock on
131: # session.lock as well (the audit of stream C, G-C-02). flock is bound here,
132: # not looked up through the fcntl module, so a test that stands in for the
133: # module's ioctl leaves it alone.
134: _STATE_LOCK = threading.Lock()
135: _flock, _LOCK_EX = fcntl.flock, fcntl.LOCK_EX
136: 
137: 
138: @contextlib.contextmanager
139: def _state_locked():
140:     with _STATE_LOCK:
141:         os.makedirs(STATE_DIR, exist_ok=True)
142:         fd = os.open(state_path("session.lock"), os.O_RDWR | os.O_CREAT, 0o600)
143:         try:
144:             _flock(fd, _LOCK_EX)
145:             yield
146:         finally:
147:             os.close(fd)
148: 
149: 
150: def _write_whole(data):
151:     os.makedirs(STATE_DIR, exist_ok=True)
152:     path = state_path("session.json")
153:     tmp = "%s.%d.tmp" % (path, os.getpid())
154:     with open(tmp, "w") as handle:
155:         json.dump(data, handle)
156:     os.replace(tmp, path)
157: 
158: 
159: def write_state(**fields):
160:     with _state_locked():
161:         existing = read_state()
162:         existing.update(fields)
163:         _write_whole(existing)
164: 
165: 
166: def write_owned(attempt, owner=None, from_status=None, **fields):
167:     """write_state, if the state still belongs to this serve's attempt.
168: 
169:     Each serve stamps the state with an attempt id of its own (cmd_serve's
170:     reset_state). A collector from a serve that has since been replaced --
171:     its rclone killed by the replacement, or dying as the old serve tears
172:     down -- would otherwise write its failure over the new attempt's state,
173:     and the merge kept that error beside the new attempt's "waiting" (G-C-02
174:     claude). An attempt of None owns whatever is there: a Session made
175:     outside a serve.
176: 
177:     owner, when given, is the session within the serve that must still be
178:     the one the state names (SessionHolder.start writes it): a restart
179:     replaces the session and keeps the serve. from_status, when given, is
180:     the statuses this write may move the state from. Together they keep the
181:     state moving forward: a dead attempt is not republished as waiting, and
182:     an attempt that was replaced, cancelled or timed out is not reopened as
183:     signed-in (the audit of the fix round, PL-032). A state with no status
184:     yet -- a Session made outside a serve -- counts as None. Checked and
185:     written under the state's lock. Returns whether it wrote.
186:     """
187:     with _state_locked():
188:         existing = read_state()
189:         if attempt is not None and existing.get("attempt") != attempt:
190:             return False
191:         if owner is not None and existing.get("session") != owner:
192:             return False
193:         if from_status is not None and existing.get("status") not in from_status:
194:             return False
195:         existing.update(fields)
196:         _write_whole(existing)
197:         return True
198: 
199: 
200: def reset_state(**fields):
201:     """Replace the state, rather than merging into it.
202: 
203:     write_state merges, which is right while one sign-in is running and wrong
204:     between two: a finished attempt leaves its address, PIN and provider link
205:     behind, and the next page to read them shows a previous session's code as
206:     though it were live. Anyone typing it in gets a flat refusal from a
207:     listener that is waiting for a different number.
208:     """
209:     os.makedirs(STATE_DIR, exist_ok=True)
210:     # The markers are part of the state. A completion marker left by the last
211:     # attempt would tell the next one's window to show "Finishing up" before
212:     # anybody had signed in to anything.
213:     for name in ("open-browser", "close-browser", "signed-in", "page",
214:                  "phone-keyboard", "field"):
215:         try:
216:             os.unlink(state_path(name))
217:         except OSError:
218:             pass
219:     with _state_locked():
220:         _write_whole(dict(fields))
221: 
222: 
223: def read_state():
224:     try:
225:         with open(state_path("session.json")) as handle:
226:             return json.load(handle)
227:     except (OSError, ValueError):
228:         return {}
229: 
230: 
231: def lan_address():
232:     """The address a phone on the same network would use.
233: 
234:     Asks the routing table which source address reaches the outside world,
235:     without sending anything -- a connected UDP socket only picks a route.
236:     """
237:     probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
238:     try:
239:         probe.connect(("192.0.2.1", 9))  # TEST-NET-1: routable, never answers
240:         return probe.getsockname()[0]
241:     except OSError:
242:         return "127.0.0.1"
243:     finally:
244:         probe.close()
245: 
246: 
247: def provider_url(local_url):
248:     """Turn rclone's local auth URL into the provider's real sign-in URL.
249: 
250:     rclone answers /auth with a redirect carrying its own client id, scopes
251:     and state. Following it here rather than in the player's browser is the
252:     whole trick: the phone then goes straight to the provider and never needs
253:     to reach this device.
254:     """
255:     request = urllib.request.Request(local_url)
256: 
257:     class NoRedirect(urllib.request.HTTPRedirectHandler):
258:         def redirect_request(self, *args, **kwargs):
259:             return None
260: 
261:     opener = urllib.request.build_opener(NoRedirect)
262:     try:
263:         opener.open(request, timeout=10)
264:     except urllib.error.HTTPError as exc:
265:         location = exc.headers.get("Location")
266:         if location:
267:             return location
268:     except OSError:
269:         pass
270:     return None
271: 
272: 
273: class Session:
274:     """One sign-in attempt: rclone's process, its URL, and the result."""
275: 
276:     def __init__(self, backend, remote_name, timeout):
277:         self.backend = backend
278:         self.remote_name = remote_name
279:         self.timeout = timeout
280:         self.proc = None
281:         self.provider = None
282:         self.token = None
283:         # Set by the holder, so a sign-in that finishes on the device can
284:         # close the window without this needing to know what a window is.
285:         self.on_signed_in = None
286:         # True once the remote exists and has answered -- never earlier (see
287:         # _write_config).
288:         self.configured = False
289:         self._config_lock = threading.Lock()
290:         self._config_result = None
291:         # Set by the holder when this attempt stops speaking for the state:
292:         # another attempt replaced it (whose start kills this one's rclone),
293:         # or the serve is ending (holder.end kills it). Either way this
294:         # one's collector is woken by a death it must not report as a
295:         # failed sign-in (PL-050, G-C-02).
296:         self.superseded = False
297:         # The serve's attempt id, which the state carries (write_owned), and
298:         # this session's own within it (SessionHolder.start): a restart keeps
299:         # the serve and replaces the session (PL-032).
300:         self.attempt = None
301:         self.gen = None
302:         # The thread that collects rclone's output and finishes the job;
303:         # SessionHolder.end lets one that is saving a remote finish.
304:         self.collector = None
305:         self.error = None
306:         # rclone's own last words. It exits fatally when the exchange fails,
307:         # and what it says -- "code doesn't exist or has expired" against
308:         # anything else -- is the difference between "you were too slow, here
309:         # is another link" and "something is actually wrong". Reporting a
310:         # generic failure for both sent the tester back to the handheld when
311:         # one tap would have done.
312:         self.rclone_says = ""
313: 
314:     def finished(self):
315:         return self.proc is not None and self.proc.poll() is not None
316: 
317:     def start(self):
318:         # A previous attempt still holding 53682 would make this one fail with
319:         # "address already in use", which reads as a provider problem.
320:         subprocess.run(["pkill", "-f", "rclone authorize"],
321:                        capture_output=True)
322:         time.sleep(1)
323: 
324:         self.proc = subprocess.Popen(
325:             [RCLONE, "authorize", self.backend, "--auth-no-open-browser"],
326:             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
327: 
328:         # The wait for the link is bounded by the clock, not by rclone. It
329:         # was a readline() under a deadline checked between lines, so an
330:         # authorize that printed nothing held this -- and the interface's
331:         # sign-in page -- for as long as it cared to (#308 gpt F-RS-19).
332:         # Raw reads under select(), then: whatever arrived after the link
333:         # goes to the collector with the rest.
334:         deadline = time.time() + AUTHORIZE_WAIT
335:         fd = self.proc.stdout.fileno()
336:         pending = b""
337:         local = None
338:         while local is None:
339:             left = deadline - time.time()
340:             if left <= 0:
341:                 break
342:             ready, _, _ = select.select([fd], [], [], left)
343:             if not ready:
344:                 break
345:             chunk = os.read(fd, 4096)
346:             if not chunk:
347:                 break
348:             pending += chunk
349:             match = re.search(rb"(http://127\.0\.0\.1:53682/auth\?state=\S+)\s", pending)
350:             if match:
351:                 local = match.group(1).decode()
352:         self.early_output = pending.decode("utf-8", "replace")
353:         if not local:
354:             self.error = "rclone did not offer a sign-in link"
355:             if self.proc.poll() is None:
356:                 self.proc.terminate()
357:                 try:
358:                     self.proc.wait(timeout=3)
359:                 except subprocess.TimeoutExpired:
360:                     self.proc.kill()
361:             return False
362: 
363:         self.provider = provider_url(local)
364:         if not self.provider:
365:             self.error = "could not read the provider's sign-in address"
366:             return False
367: 
368:         # Everything after this point is rclone waiting for the redirect, so
369:         # collect its output off-thread; the token appears there when the
370:         # replay lands.
371:         self.collector = threading.Thread(target=self._collect, daemon=True)
372:         self.collector.start()
373:         log("sign-in started for %s" % self.backend)
374:         return True
375: 
376:     def _collect(self):
377:         # What start() read past the link comes first, through the same
378:         # checks: a provider that refuses at once puts rclone's last words in
379:         # that first read, and they went into the buffer without being looked
380:         # at, so the failure said nothing of why (the audit of stream C,
381:         # G-C-10).
382:         buffer = ""
383:         early = getattr(self, "early_output", "")
384:         for line in itertools.chain(early.splitlines(True), self.proc.stdout):
385:             buffer += line
386:             if line.startswith("Error: ") or "Fatal error:" in line:
387:                 self.rclone_says = line.split("error: ")[-1].strip() or line.strip()
388:             if "<---End paste" in buffer or "Paste the following" in buffer:
389:                 match = re.search(r"(\{.*\})", buffer, re.S)
390:                 if match:
391:                     self.token = match.group(1).strip()
392:                     break
393:         self.proc.wait()
394: 
395:         # Finish the job. rclone's own server takes the redirect when the page
396:         # is on the handheld, so nothing is ever pasted back and submit() --
397:         # which was the only caller of _write_config -- never runs. The token
398:         # arrived, was collected here, and stopped: no remote was created and
399:         # the status stayed "waiting", so a sign-in that had actually
400:         # succeeded was reported as unfinished and had to be started again.
401:         if self.token and not self.configured:
402:             ok, detail = self._write_config()
403:             if ok:
404:                 log("sign-in completed on the device")
405:                 if self.on_signed_in:
406:                     try:
407:                         self.on_signed_in()
408:                     except Exception as exc:      # never take the thread down
409:                         log("post-sign-in step failed: %s" % exc)
410:             else:
411:                 log("could not finish the sign-in: %s" % detail)
412:                 # Only while this attempt still speaks for the state: a
413:                 # restart may have replaced it while its remote was being
414:                 # created (G-C-02 gpt).
415:                 if not self.superseded:
416:                     self._fail_owned(detail, ("starting", "waiting", "failed"))
417:         elif not self.token and not self.superseded:
418:             # rclone ended without a token: the provider refused, the
419:             # exchange failed, or it was killed. Nothing else is going to
420:             # finish this attempt, and the on-device path has no page to
421:             # say so -- the status stayed "waiting" until the serve timed
422:             # out, and the interface's STILL WAITING told the player to
423:             # finish an attempt that was already dead (audit #307 PL-050).
424:             if self._fail_owned(self.failure_reason(), ("starting", "waiting")):
425:                 log("the sign-in ended without a token")
426: 
427:     def _fail_owned(self, error, from_status):
428:         """Mark the attempt failed -- only while this serve's attempt owns
429:         the state and the status is one of from_status, checked and written
430:         under the state's lock."""
431:         with _state_locked():
432:             existing = read_state()
433:             if self.attempt is not None and existing.get("attempt") != self.attempt:
434:                 return False
435:             if self.gen is not None and existing.get("session") != self.gen:
436:                 return False
437:             if existing.get("status") not in from_status:
438:                 return False
439:             existing.update(status="failed", error=error)
440:             _write_whole(existing)
441:             return True
442: 
443:     def failure_reason(self):
444:         """Why the attempt died, in words a player can act on."""
445:         said = self.rclone_says
446:         if "expired" in said or "invalid_grant" in said:
447:             return ("That address had already expired — they are only good "
448:                     "for a couple of minutes.")
449:         if said:
450:             return "The provider refused it: %s" % said[:160]
451:         return "The provider did not accept that address."
452: 
453:     def submit(self, pasted):
454:         """Replay the provider's redirect to rclone's waiting server.
455: 
456:         Accepts the whole failed URL or just the code, because the player is
457:         copying from a phone's address bar on a page that did not load, and
458:         which of the two they manage to grab is not something to be strict
459:         about.
460:         """
461:         pasted = pasted.strip()
462:         query = None
463:         if "code=" in pasted:
464:             parsed = urllib.parse.urlparse(pasted)
465:             query = parsed.query or pasted.split("?", 1)[-1]
466:         elif pasted:
467:             state = urllib.parse.parse_qs(
468:                 urllib.parse.urlparse(self.provider).query).get("state", [""])[0]
469:             query = urllib.parse.urlencode({"code": pasted, "state": state})
470:         if not query:
471:             # Nothing was replayed, so the attempt is still alive and they can
472:             # simply paste again -- worth distinguishing from the dead-session
473:             # case below.
474:             return False, ("Nothing was pasted. Go to the page that failed "
475:                            "to load, copy its whole address from the browser "
476:                            "bar, and paste it here.")
477: 
478:         try:
479:             urllib.request.urlopen("%s/?%s" % (LOCAL_AUTH, query), timeout=15).read()
480:         except urllib.error.HTTPError:
481:             pass  # rclone answers the redirect with its own page; not an error
482:         except OSError as exc:
483:             return False, "could not hand the code back to rclone: %s" % exc
484: 
485:         for _ in range(40):
486:             if self.token:
487:                 return self._write_config()
488:             if self.proc.poll() is not None and not self.token:
489:                 # rclone's authorize server serves exactly one redirect and
490:                 # then exits, so a wrong or expired code ends the attempt
491:                 # rather than allowing another go. Say that, because the
492:                 # player is looking at a page that still has a working-looking
493:                 # form on it and would otherwise keep pasting into a session
494:                 # that no longer exists.
495:                 return False, self.failure_reason()
496:             time.sleep(0.5)
497:         return False, "Timed out waiting for the provider."
498: 
499:     def _write_config(self):
500:         """Create the remote, once per attempt, and say how it went.
501: 
502:         Two paths can reach this -- the redirect landing on rclone directly
503:         (the collector) and a code pasted back from a phone (submit) -- and
504:         they can overlap. The first does the work; the second waits for it
505:         and is handed the same answer. `configured` used to be set on the
506:         way in, so a second caller was told "Connected" while the first was
507:         still creating and checking the remote, and even when that then
508:         failed (audit #307 PL-048). It is set now only from the result.
509:         """
510:         with self._config_lock:
511:             if self._config_result is None:
512:                 self._config_result = self._create_remote()
513:                 self.configured = bool(self._config_result[0])
514:             return self._config_result
515: 
516:     def _create_remote(self):
517:         # One create at a time within the serve. An obsolete attempt never
518:         # publishes its staged credentials; cancellation and publication
519:         # use the same state lock below.
520:         with _CREATE_LOCK:
521:             return self._create_remote_locked()
522: 
523:     def _create_remote_locked(self):
524:         name = self.remote_name or self.backend
525:         # Replaced or closed before its token could be saved: nothing is
526:         # made (PL-032).
527:         if self.superseded:
528:             log("the sign-in was closed before its remote was saved; nothing was saved")
529:             return False, CLOSED_EARLY
530:         def publish(commit):
531:             # Hold the same cross-process state lock as cancellation until
532:             # both the config and its success record have been published.
533:             with _state_locked():
534:                 state = read_state()
535:                 if (self.superseded or
536:                     (self.attempt is not None and state.get("attempt") != self.attempt) or
537:                     (self.gen is not None and state.get("session") != self.gen) or
538:                     state.get("status") not in (None, "starting", "waiting")):
539:                     raise connections.Refused(CLOSED_EARLY)
540:                 commit()
541:                 state.update(status="signed-in", remote=name)
542:                 _write_whole(state)
543:         try:
544:             connections.save(name, self.backend, [("token", self.token)],
545:                              replace=getattr(self, "replace", False), publish=publish)
546:         except (connections.Refused, OSError) as exc:
547:             log("the sign-in could not be saved; previous settings retained")
548:             return False, str(exc) if isinstance(exc, connections.Refused) else "Your cloud settings could not be saved."
549:         log("remote %s verified and saved for %s" % (name, self.backend))
550:         return True, name
551: 
552: 
553: # What a closed or replaced attempt's own late ending says, on the phone and
554: # in the log, when it has one to say.
555: CLOSED_EARLY = "That sign-in was closed before it finished."
556: 
557: # One remote created at a time in this process (Session._create_remote).
558: _CREATE_LOCK = threading.Lock()
559: 
560: 
561: # rclone's backend names are lowercase identifiers ("dropbox", "onedrive").
562: # They are not what the provider calls itself, and a page headed "Connect
563: # dropbox" reads like a typo on the one screen where the player is deciding
564: # whether to trust us with their storage. The handheld passes the curated name
565: # it already shows in its own menu; this map is the fallback for a backend
566: # reached some other way, and title-casing is the fallback for that.
567: DISPLAY_NAMES = {
568:     "acd": "Amazon Drive", "box": "Box", "drive": "Google Drive",
569:     "dropbox": "Dropbox", "gcs": "Google Cloud Storage",
570:     "gphotos": "Google Photos", "hidrive": "HiDrive", "jottacloud": "Jottacloud",
571:     "mailru": "Mail.ru Cloud", "onedrive": "Microsoft OneDrive",
572:     "opendrive": "OpenDrive", "pcloud": "pCloud",
573:     "premiumizeme": "premiumize.me", "putio": "put.io",
574:     "sharefile": "Citrix ShareFile", "sugarsync": "SugarSync",
575:     "yandex": "Yandex Disk", "zoho": "Zoho WorkDrive",
576:     "filefabric": "Enterprise File Fabric",
577: }
578: 
579: 
580: def display_name(backend, label=None):
581:     # Our curated name wins where we have one: rclone's descriptions are
582:     # written for its documentation ("Google Cloud Storage (this is not Google
583:     # Drive)"), which is accurate and wrong as a page heading. The passed
584:     # label -- rclone's description, by way of the handheld's menu -- covers
585:     # everything else, and title-casing covers a backend reached from a shell.
586:     if backend in DISPLAY_NAMES:
587:         return DISPLAY_NAMES[backend]
588:     if label:
589:         return label
590:     return backend.replace("_", " ").title()
591: 
592: 
593: # Single %, not %%: this is substituted into the templates as a *value*
594: # (%(style)s), so its percent signs are never seen by the formatter. Escaping
595: # them the way the templates do shipped "width:100%%" as literal CSS, which
596: # every browser discards -- which is how a four-character PIN box ended up
597: # rendering at its default twenty-character width with wide letter spacing,
598: # overflowing the card on a phone.
599: STYLE = """
600: body{font:16px/1.5 system-ui,sans-serif;margin:0;padding:20px;background:#111;color:#eee}
601: .card{max-width:34rem;margin:0 auto}
602: h1{font-size:1.3rem;margin:0 0 .25rem}
603: h2{font-size:1rem;margin:1.5rem 0 .5rem;color:#9cf;text-transform:uppercase;
604:    letter-spacing:.05em}
605: ol{padding-left:1.3rem;margin:.5rem 0}li{margin:.4rem 0}
606: a.go{display:block;background:#2d7;color:#000;padding:14px;border-radius:8px;
607:      text-align:center;font-weight:600;text-decoration:none;margin:.5rem 0}
608: input{width:100%;padding:12px;font-size:16px;border-radius:8px;border:1px solid #555;
609:       background:#1c1c1c;color:#eee;box-sizing:border-box}
610: /* Four characters do not need the width of a phone. Sized in ch so it tracks
611:    the font rather than assuming one, and capped against the card so it still
612:    shrinks rather than overflowing on a narrow screen. */
613: input.pin{font-size:24px;letter-spacing:.5em;text-align:center;
614:           width:7ch;max-width:100%;padding-left:.6em}
615: form.narrow{text-align:center}
616: form.narrow button{width:auto;min-width:9rem}
617: button{margin-top:10px;padding:12px 20px;font-size:16px;border-radius:8px;
618:        border:0;background:#4af;color:#000;font-weight:600;width:100%}
619: button.minor{background:#333;color:#ddd;font-weight:500}
620: .note{color:#aaa;font-size:.9rem}
621: /* The connection line sits between the heading and the field; without
622:    margins of its own it read as part of both (fork #351). */
623: #state{margin:.75rem 0}
624: /* The way off the handheld's page lives at the very bottom, under the note,
625:    with room above it, so a drag on the pad that runs off its edge lands
626:    on text and not on Close (fork #351, D-CLOUD-163). Its two-step
627:    confirmation replaces the row in place. */
628: [hidden]{display:none!important}
629: .leave{margin-top:2rem}
630: .leave .ask{display:flex;gap:8px;align-items:center}
631: .leave .ask span{flex:1 1 auto;color:#aaa;font-size:.9rem}
632: .leave .ask button{flex:0 0 auto;width:auto;padding:12px 18px;margin-top:0}
633: .err{background:#722;padding:12px;border-radius:8px;margin:1rem 0}
634: .ok{background:#272;padding:12px;border-radius:8px;margin:1rem 0}
635: .box{border:1px solid #444;border-radius:10px;padding:14px;margin:1rem 0}
636: .big{font-size:1.6rem;text-align:center;margin:1rem 0}
637: /* Five buttons on a phone's 350 px share the row from a basis of nothing
638:    (flex:1 1 0) and may shrink below their words (min-width:0, which flex
639:    items refuse by default); width:auto undoes the block rule's 100%, which
640:    as a basis put every button on a row of its own. Show sat off the right
641:    edge of an iPhone's screen (fork #330). */
642: .keys{display:flex;gap:8px;margin-top:10px}
643: .keys button{flex:1 1 0;min-width:0;width:auto;padding:12px 6px;margin-top:0}
644: /* The trackpad. Tall enough to drag across a four-inch screen's worth of
645:    page without lifting a finger, and touch-action:none so the browser does
646:    not steal the gesture to scroll its own page. */
647: .pad{height:11rem;margin-top:12px;border:1px dashed #555;border-radius:10px;
648:      background:#181818;touch-action:none;display:flex;align-items:center;
649:      justify-content:center;color:#666;font-size:.85rem;user-select:none}
650: .pad.live{border-color:#4af;color:#4af}
651: """
652: 
653: # The paste field sits ABOVE the sign-in button on purpose. Somebody arriving
654: # here for the first time reads the numbered steps and goes down to the button;
655: # somebody arriving the *second* time -- back from the provider, holding an
656: # address that expires in about two minutes -- needs the box to be the first
657: # thing on the screen, not something below a large green button that looks like
658: # the action. Getting that wrong cost a real sign-in: the tester approved
659: # access, could not see where the address went, and by the time they found it
660: # the code had expired (fork #51).
661: PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
662: <title>Connect %(name)s</title>
663: <style>%(style)s</style>
664: <div class=card>
665: <h1>Connect %(name)s</h1>
666: <p class=note>Keep this page open. You will come back to it.</p>
667: %(message)s
668: 
669: %(here)s
670: <h2>1. Sign in and approve access</h2>
671: <a class=go href="%(provider)s" target="_blank" rel="noopener">Sign in to %(name)s</a>
672: <p class=note>Opens in a new tab, so <strong>this page stays where it
673: is</strong>. Approve access, then come straight back here — what you bring
674: back is only good for a couple of minutes.</p>
675: 
676: <h2>2. Paste the address it lands on</h2>
677: <p class=note>Approving sends the browser to an address it cannot open, so it
678: shows an error — <em>"Safari cannot open the page"</em>, <em>"This site can't
679: be reached"</em>, or similar. <strong>That error page is the point: its
680: address is what we need.</strong> Tap its address bar, copy the whole thing,
681: come back to this tab and paste it below.</p>
682: <form method=post id=f>
683: <input name=code placeholder="Paste here" autofocus
684:        autocapitalize=off autocorrect=off spellcheck=false inputmode=url>
685: <input type=hidden name=pin value="%(pin)s">
686: <button type=submit>Confirm</button>
687: </form>
688: <script>
689: // Paste and it goes -- what was pasted expires in about two minutes, and the
690: // tester who lost one spent them looking for the button.
691: document.querySelector("input[name=code]").addEventListener("paste", function () {
692:   var f = document.getElementById("f");
693:   setTimeout(function () { if (this.value.indexOf("code=") >= 0) f.submit(); }.bind(this), 50);
694: });
695: </script>
696: 
697: <form method=post>
698: <input type=hidden name=pin value="%(pin)s">
699: <input type=hidden name=restart value="1">
700: <button class=minor type=submit>Lost the address? Start over</button>
701: </form>
702: </div>
703: """
704: 
705: # Typing an address into a phone is the fallback for a phone that cannot scan,
706: # and it has to stay short enough to type -- so the PIN is asked for here
707: # rather than carried in the address. Scanning the QR skips this page, because
708: # the QR encodes the PIN.
709: PIN_PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
710: <title>pixelelated cloud sign-in</title>
711: <style>%(style)s</style>
712: <div class=card>
713: <h1>Almost there</h1>
714: %(message)s
715: <p>The address on the handheld ends in four digits. Type them here.</p>
716: <form method=get action="/" class=narrow>
717: <input class=pin name=pin inputmode=numeric pattern="[0-9]*" maxlength=4 autofocus
718:        autocomplete=off placeholder="0000" value="%(pin)s">
719: <button type=submit>Continue</button>
720: </form>
721: <p class=note>They are a PIN. This page is open to everyone on your network
722: while setup is running, and the PIN is what stops somebody else finishing the
723: sign-in with their own account. Scanning the code on the handheld fills it in
724: for you.</p>
725: </div>
726: """
727: 
728: DONE_PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
729: <title>Connected</title>
730: <style>%(style)s</style>
731: <div class=card>
732: <h1>Connected</h1>
733: <div class=ok>%(name)s is set up on your handheld as <strong>%(remote)s</strong>.</div>
734: <div class=big>Go back to the handheld<br>and choose CONTINUE</div>
735: <p class=note>You can close this page.</p>
736: </div>
737: """
738: 
739: 
740: SIGNIN_WINDOW = "/usr/bin/cloud-signin-window"
741: UINPUT = "/dev/uinput"
742: 
743: 
744: def sway_env():
745:     """Enough environment to talk to the running sway over its IPC socket."""
746:     session = running_session()
747:     if not session:
748:         return {}
749:     runtime, display = session
750:     env = {"XDG_RUNTIME_DIR": runtime, "WAYLAND_DISPLAY": display}
751:     for name in sorted(os.listdir(runtime)):
752:         if name.startswith("sway-ipc.") and name.endswith(".sock"):
753:             env["SWAYSOCK"] = os.path.join(runtime, name)
754:             break
755:     return env
756: 
757: 
758: def running_session():
759:     """The Wayland session EmulationStation is already using.
760: 
761:     The sign-in window runs as a client of *that* compositor rather than in
762:     one of its own. A nested compositor cannot have the GPU -- the session
763:     that owns the display holds it -- so it falls back to software
764:     rasterisation, and the provider's page took about 150 seconds to paint
765:     instead of two. Joining the existing session is both faster and simpler:
766:     no second compositor, no mirroring, and the page appears on the screen
767:     the player is already holding.
768:     """
769:     for entry in os.listdir("/proc"):
770:         if not entry.isdigit():
771:             continue
772:         try:
773:             with open("/proc/%s/cmdline" % entry, "rb") as handle:
774:                 argv = handle.read().split(b"\0")
775:             if not argv or not argv[0].endswith(b"/sway"):
776:                 continue
777:             with open("/proc/%s/environ" % entry, "rb") as handle:
778:                 env = dict(
779:                     kv.split(b"=", 1) for kv in handle.read().split(b"\0")
780:                     if b"=" in kv)
781:         except OSError:
782:             continue
783:         runtime = env.get(b"XDG_RUNTIME_DIR", b"").decode()
784:         if not runtime or not os.path.isdir(runtime):
785:             continue
786:         for name in sorted(os.listdir(runtime)):
787:             if name.startswith("wayland-") and not name.endswith(".lock"):
788:                 return runtime, name
789:     return None, None
790: 
791: 
792: def stop_other_serves():
793:     """End any other `cloud_oauth serve`, so this one can have the port.
794: 
795:     cancel only ever killed rclone; a serve left running kept port 8080 and
796:     the next attempt died on EADDRINUSE before writing any state -- so the
797:     handheld showed a blank address and nothing said why.
798: 
799:     Walks /proc rather than calling pkill: `pkill -f "cloud_oauth serve"`
800:     matches its own command line, and has killed the calling shell repeatedly
801:     in this project's history.
802:     """
803:     me = os.getpid()
804:     for entry in os.listdir("/proc"):
805:         if not entry.isdigit() or int(entry) == me:
806:             continue
807:         try:
808:             with open("/proc/%s/cmdline" % entry, "rb") as handle:
809:                 argv = handle.read().split(b"\0")
810:         except OSError:
811:             continue
812:         if any(b"cloud_oauth" in a for a in argv) and b"serve" in argv:
813:             try:
814:                 os.kill(int(entry), signal.SIGTERM)
815:             except OSError:
816:                 pass
817:     time.sleep(1)
818: 
819: 
820: def browser_stack_available():
821:     """Whether this image can show a provider's page on the device itself."""
822:     runtime, display = running_session()
823:     return os.path.exists(SIGNIN_WINDOW) and runtime is not None
824: 
825: 
826: class BrowserSession:
827:     """The provider's sign-in page, on this device's screen."""
828: 
829:     def __init__(self, url, host):
830:         self.url = url
831:         self.host = host
832:         self.proc = None
833:         self.log_file = None
834:         self.log_path = None
835:         self.error = None
836:         # Whether start() turned sway's pointer hiding off, so stop() knows
837:         # to turn it back on whatever became of the window.
838:         self.cursor_overridden = False
839: 
840:     def is_running(self):
841:         return self.proc is not None and self.proc.poll() is None
842: 
843:     def start(self):
844:         runtime, display = running_session()
845:         if not runtime:
846:             self.error = "no display session to show the sign-in page on"
847:             return False
848: 
849:         os.makedirs(STATE_DIR, exist_ok=True)
850:         self.log_path = state_path("window.log")
851:         # Kept rather than discarded: a window that fails to start otherwise
852:         # looks exactly like one that started and was never asked for.
853:         self.log_file = open(self.log_path, "w")
854: 
855:         env = dict(os.environ)
856:         # Where the window records the address it is showing, so the phone can
857:         # tell when the provider has moved on.
858:         env["CLOUD_SIGNIN_PAGE_FILE"] = state_path("page")
859:         env["CLOUD_SIGNIN_DONE_FILE"] = state_path("signed-in")
860:         env["CLOUD_SIGNIN_LANGUAGE"] = signin_language()
861:         # And where it records that a field on that page has had the caret,
862:         # which is when the phone's text can go across (the probe below). A
863:         # record a previous window left says nothing about this one.
864:         env["CLOUD_SIGNIN_FIELD_FILE"] = state_path("field")
865:         try:
866:             os.unlink(state_path("field"))
867:         except OSError:
868:             pass
869:         env.update({
870:             "XDG_RUNTIME_DIR": runtime,
871:             "WAYLAND_DISPLAY": display,
872:             "GDK_BACKEND": "wayland",
873:         })
874:         self.proc = subprocess.Popen(
875:             [SIGNIN_WINDOW, self.url, registrable_domain(self.host),
876:              "--exit-hint", exit_hint()]
877:             + (["--no-auto-keyboard"]
878:                if os.path.exists(state_path("phone-keyboard")) else []),
879:             env=env, stdout=self.log_file, stderr=subprocess.STDOUT)
880:         # Somebody may be about to drag a pointer at this page from their
881:         # phone, and cannot aim what they cannot see.
882:         BrowserSession._cursor_timeout(0)
883:         self.cursor_overridden = True
884:         log("sign-in window opened on %s for %s" % (display, self.host))
885:         return True
886: 
887:     @staticmethod
888:     def _cursor_timeout(ms):
889:         """How long sway waits before hiding the pointer.
890: 
891:         ROCKNIX ships `seat * hide_cursor 1000`, which is right for a handheld
892:         with no mouse and wrong while somebody is dragging one from their
893:         phone: the pointer disappears a second after they stop moving, so the
894:         tap that follows is aimed at something they cannot see. Zero means
895:         never hide. Restored when the window closes, because the rest of the
896:         time the original setting is the correct one.
897:         """
898:         try:
899:             subprocess.run(["swaymsg", "seat", "*", "hide_cursor", str(ms)],
900:                            capture_output=True, timeout=5,
901:                            env=dict(os.environ, **sway_env()))
902:         except (OSError, subprocess.SubprocessError) as exc:
903:             log("could not set the cursor timeout: %s" % exc)
904: 
905:     def stop(self):
906:         # Restored whenever start() set it -- also when the window has
907:         # already gone by itself (Escape, a crash). It used to sit inside
908:         # the still-running test, so a window that ended on its own left
909:         # sway never hiding the pointer (#308 claude F-RS-19, gpt F-RS-25).
910:         if self.cursor_overridden:
911:             BrowserSession._cursor_timeout(1000)
912:             self.cursor_overridden = False
913:         if self.proc and self.proc.poll() is None:
914:             self.proc.terminate()
915:             try:
916:                 self.proc.wait(timeout=5)
917:             except subprocess.TimeoutExpired:
918:                 self.proc.kill()
919:         self.proc = None
920:         if self.log_file:
921:             try:
922:                 self.log_file.close()
923:             except OSError:
924:                 pass
925:             self.log_file = None
926: 
927: 
928: def registrable_domain(host):
929:     """dropbox.com from www.dropbox.com.
930: 
931:     Providers bounce a sign-in through their own subdomains -- Dropbox goes
932:     via marketing.dropbox.com -- so pinning navigation to the exact host the
933:     authorize URL used refuses legitimate steps of the flow. Two labels is a
934:     blunt rule that is wrong for co.uk and right for every provider rclone
935:     talks to; the window treats it as a suffix, not an exact match.
936:     """
937:     parts = [p for p in (host or "").split(".") if p]
938:     return ".".join(parts[-2:]) if len(parts) > 2 else (host or "")
939: 
940: 
941: # Shown when the sign-in page is open on the handheld itself. That is the good
942: # path: the redirect completes on its own and nothing has to be copied.
943: #
944: # The keyboard below is an option, not a requirement. On a 6" handheld with a
945: # touchscreen, typing on the device is perfectly reasonable and this page is
946: # unnecessary; on a 3.5" screen driven by a d-pad it is the difference between
947: # a minute of misery and a few seconds. Both work, because the page is on the
948: # device's screen either way -- so the choice is the player's, not ours.
949: REMOTE_PAGE = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
950: <title>Keyboard for %(name)s</title>
951: <style>%(style)s</style>
952: <div class=card>
953: <h1>Keyboard for %(name)s</h1>
954: 
955: <div id=state class=note>Checking&hellip;</div>
956: 
957: <input id=kb type=password placeholder="Type here" autocapitalize=off
958:        autocorrect=off spellcheck=false autofocus>
959: <div id=warn class=err hidden></div>
960: <div class=keys>
961: <button type=button class=minor data-key=backspace>Back</button>
962: <button type=button class=minor data-key=tab>Tab</button>
963: <button type=button class=minor data-key=enter>Enter</button>
964: <button type=button class=minor id=clear>Clear</button>
965: <button type=button class=minor id=show>Show</button>
966: </div>
967: 
968: 
969: <div class=keys>
970: <button type=button class=minor data-key=left>&larr;</button>
971: <button type=button class=minor data-key=up>&uarr;</button>
972: <button type=button class=minor data-key=down>&darr;</button>
973: <button type=button class=minor data-key=right>&rarr;</button>
974: </div>
975: <div class=keys>
976: <button type=button class=minor data-key=f2>Page up</button>
977: <button type=button class=minor data-key=f3>Page down</button>
978: </div>
979: <h2>Pointer</h2>
980: <div class=pad id=pad>drag to move &middot; tap to click</div>
981: 
982: <p class=note>The sign-in page is on your handheld&rsquo;s screen, not here.
983: This types for it, so you can more easily retrieve and type your login
984: info. What you type crosses your network unencrypted, so use this on a
985: network you trust.</p>
986: 
987: <!-- A way off the handheld's page that does not depend on its gamepad: a
988:      pad the bridge cannot read (#308 gpt F-RS-16) leaves this, and the
989:      window quits on Escape. At the bottom, under the note, because it sat
990:      right above the drag pad and a thumb found it by accident (fork #351);
991:      and asked once, in place, before Escape is sent (D-CLOUD-163). -->
992: <div class=leave id=leave>
993: <button type=button class=minor id=leave-ask>Close page</button>
994: <div class=ask id=leave-confirm hidden><span>Close the sign-in page on your handheld?</span>
995: <button type=button class=minor id=leave-keep>Keep</button><button type=button id=leave-close>Close</button></div>
996: </div>
997: </div>
998: 
999: <script>
1000: // A script that dies before it starts leaves the page saying Checking... for
1001: // as long as it is open, its taps dead (fork #330). Said on the page, with
1002: // the browser's words for the ROCKNIX team, instead of nothing.
1003: window.onerror = function (message) {
1004:   var state = document.getElementById("state");
1005:   if (!state) return;
1006:   state.className = "err";
1007:   state.textContent = "This page stopped working. Reload it; if it happens again, report it to the pixelelated project: " + message;
1008: };
1009: (function () {
1010:   var pin = "%(pin)s";
1011:   var box = document.getElementById("kb");
1012:   var warn = document.getElementById("warn");
1013:   var state = document.getElementById("state");
1014:   var pad = document.getElementById("pad");
1015: 
1016:   // One request at a time, in order. Backspaces and characters that overtake
1017:   // each other arrive as scrambled text in the field on the handheld.
1018:   //
1019:   // Two states from the probe: winUp, the window is on the handheld's
1020:   // screen (the named keys drive it -- Tab is how a field the page did not
1021:   // focus is reached); ready, a field on its page has had the caret, so
1022:   // text has somewhere to go. It was `up` until fork #330 -- the same name
1023:   // as the pad's up(e) below, and a var assigned false over a hoisted
1024:   // function makes addEventListener("touchend", up) throw before poll()
1025:   // ever runs: the page sat on Checking... with its taps dead on every
1026:   // browser, while drags moved the pointer (their handler was bound first).
1027:   var winUp = false;
1028:   var ready = false;
1029:   var page = null;
1030:   var queue = Promise.resolve();
1031:   var pendingMove = null;
1032:   function send(body) {
1033:     // Seal any queued movement before this key/click. Later drags start a
1034:     // new batch behind it, so a tap cannot overtake its final pointer move.
1035:     pendingMove = null;
1036:     queue = queue.then(function () {
1037:       return fetch("/" + pin, {
1038:         method: "POST",
1039:         headers: {"Content-Type": "application/x-www-form-urlencoded"},
1040:         body: body + "&pin=" + encodeURIComponent(pin)
1041:       }).catch(function () {});
1042:     });
1043:     return queue;
1044:   }
1045: 
1046:   // Two different strings, which is the distinction the first cut missed.
1047:   // `shown` is what is in the box; `sent` is what has actually reached the
1048:   // handheld. They differ whenever somebody types before the page is open --
1049:   // the order this flow asks for, since the QR is on the screen the sign-in
1050:   // page replaces.
1051:   var sent = "";
1052: 
1053:   function deliver(v) {
1054:     if (v === sent) return;
1055:     if (v.length > sent.length && v.indexOf(sent) === 0) {
1056:       send("type=" + encodeURIComponent(v.slice(sent.length)));
1057:     } else if (v.length < sent.length && sent.indexOf(v) === 0) {
1058:       for (var i = 0; i < sent.length - v.length; i++) send("key=backspace");
1059:     } else {
1060:       for (var j = 0; j < sent.length; j++) send("key=backspace");
1061:       if (v) send("type=" + encodeURIComponent(v));
1062:     }
1063:     sent = v;
1064:   }
1065: 
1066:   // Every named key -- from the buttons below and from the phone's own
1067:   // keyboard alike -- goes through here, so the box and the handheld's field
1068:   // never part. The buttons used to post their key and nothing else: Back
1069:   // deleted on the handheld and left the box as it was, and every later
1070:   // keystroke was reckoned against a box one character off, so a password
1071:   // typed with one correction went across altered (audit #307 PL-017).
1072:   //
1073:   // The box holds what has been typed into the handheld's field since the
1074:   // focus last moved there. Back trims it, and with it empty still deletes
1075:   // on the handheld -- text that was there already. Enter submits the field,
1076:   // and Tab, the arrows and Close move away from it: what the box holds was
1077:   // for the field left behind, so it starts again. Page up and down only
1078:   // scroll.
1079:   function act(named) {
1080:     if (named === "backspace") {
1081:       if (box.value) {
1082:         box.value = box.value.slice(0, -1);
1083:         if (ready) deliver(box.value);
1084:       } else if (winUp) {
1085:         send("key=backspace");
1086:       }
1087:       return;
1088:     }
1089:     if (!winUp) return;
1090:     send("key=" + named);
1091:     if (named !== "f2" && named !== "f3") { box.value = ""; sent = ""; dropped = []; warnSay(); }
1092:   }
1093: 
1094:   // Only what the handheld can type goes in the box: printable ASCII,
1095:   // [ -~], the US layout cloud_oauth types with. Anything else used to be
1096:   // sent, dropped at the other end without a word, and left showing here
1097:   // -- a credential altered in silence (#308 claude F-RS-16, gpt F-RS-13).
1098:   // It is taken out of the box instead, and the page says which.
1099:   //
1100:   // The line names the characters only while Show is on. With the box
1101:   // masked it counts them: a password's characters written out under a
1102:   // box that hides them is the box's masking undone (G-C-05, the audit of
1103:   // stream C).
1104:   var dropped = [];
1105:   function warnSay() {
1106:     if (!dropped.length) { warn.hidden = true; return; }
1107:     var many = dropped.length > 1;
1108:     warn.textContent = box.type === "password"
1109:       ? "The handheld can't type " + (many ? dropped.length + " of the characters you entered"
1110:           : "one of the characters you entered") + ", so " + (many ? "they were" : "it was") + " left out."
1111:       : "The handheld can't type " + dropped.join(" ") + ", so "
1112:           + (many ? "they were" : "it was") + " left out.";
1113:     warn.hidden = false;
1114:   }
1115:   function typable() {
1116:     var v = box.value, kept = v.replace(/[^ -~]/g, "");
1117:     if (kept === v) return;
1118:     dropped = v.replace(/[ -~]/g, "").split("");
1119:     box.value = kept;
1120:     warnSay();
1121:   }
1122: 
1123:   // What you typed stays visible. Clearing the box after every keystroke made
1124:   // a keyboard that looked broken -- you type and nothing appears anywhere
1125:   // you can see.
1126:   box.addEventListener("input", function () {
1127:     typable();
1128:     if (ready) deliver(box.value);
1129:   });
1130:   box.addEventListener("keydown", function (e) {
1131:     var named = {Enter: "enter", Backspace: "backspace", Tab: "tab"}[e.key];
1132:     if (!named) return;
1133:     e.preventDefault();
1134:     act(named);
1135:   });
1136: 
1137:   // Masked, because what goes through this box is mostly a password, and
1138:   // it stayed readable on the phone's screen after it was sent (#308 gpt
1139:   // F-RS-14). Show reveals it for checking; it hides again on a second
1140:   // press.
1141:   var show = document.getElementById("show");
1142:   show.addEventListener("click", function () {
1143:     var hidden = box.type === "password";
1144:     box.type = hidden ? "text" : "password";
1145:     show.textContent = hidden ? "Hide" : "Show";
1146:     warnSay();
1147:   });
1148: 
1149:   // Local only: the handheld has moved to another field and this box still
1150:   // holds what went into the last one.
1151:   document.getElementById("clear").addEventListener("click", function () {
1152:     box.value = ""; sent = ""; dropped = []; warnSay(); box.focus();
1153:   });
1154: 
1155:   // Close page asks once, in place, in the words approved for it (D-CLOUD-164
1156:   // string 12): the button gives way to the question with Keep and Close;
1157:   // Keep puts the button back, Close sends Escape as the old button did.
1158:   // Static markup toggled by hidden, nothing built at run time: the page's
1159:   // load test under node has no createElement, and a browser's confirm()
1160:   // cannot carry these words.
1161:   var leaveAsk = document.getElementById("leave-ask"), leaveConfirm = document.getElementById("leave-confirm");
1162:   function leaveShow(asking) { leaveAsk.hidden = asking; leaveConfirm.hidden = !asking; }
1163:   leaveAsk.addEventListener("click", function () { leaveShow(true); });
1164:   document.getElementById("leave-keep").addEventListener("click", function () { leaveShow(false); });
1165:   document.getElementById("leave-close").addEventListener("click", function () { act("escape"); leaveShow(false); });
1166:   Array.prototype.forEach.call(document.querySelectorAll("[data-key]"), function (b) {
1167:     b.addEventListener("click", function () { act(b.dataset.key); });
1168:   });
1169: 
1170:   // Drag to move, tap to click. Deltas rather than absolute positions,
1171:   // because the pointer belongs to the handheld's screen and this pad has no
1172:   // idea how big that is.
1173:   var px = 0, py = 0, moved = 0, tracking = false;
1174:   // 1:1 with the finger. Anything else has to be learned, and the pointer is
1175:   // already moving on a screen the hand holding it is not touching.
1176:   var SPEED = 1.0;
1177:   // Whatever is left after rounding is carried, not dropped. Discarding it
1178:   // every event loses a fraction of a pixel per move, which over a drag is a
1179:   // pointer that slides away from where the finger went.
1180:   var restX = 0, restY = 0;
1181:   function at(e) { var t = e.touches ? e.touches[0] : e; return {x: t.clientX, y: t.clientY}; }
1182: 
1183:   // Coalesce only adjacent, unsent moves in the same input queue as taps
1184:   // and keys. A separate move queue plus a 60 ms timer raced on slow links.
1185:   function pushMove(dx, dy) {
1186:     if (pendingMove) {
1187:       pendingMove.x += dx; pendingMove.y += dy;
1188:       return;
1189:     }
1190:     var batch = {x: dx, y: dy};
1191:     pendingMove = batch;
1192:     queue = queue.then(function () {
1193:       if (pendingMove === batch) pendingMove = null;
1194:       return fetch("/" + pin, {
1195:         method: "POST",
1196:         headers: {"Content-Type": "application/x-www-form-urlencoded"},
1197:         body: "move=" + batch.x + "," + batch.y + "&pin=" + encodeURIComponent(pin)
1198:       }).catch(function () {});
1199:     });
1200:   }
1201:   function down(e) {
1202:     var p = at(e); px = p.x; py = p.y; moved = 0; tracking = true;
1203:     restX = 0; restY = 0;
1204:     pad.classList.add("live"); e.preventDefault();
1205:   }
1206:   function move(e) {
1207:     if (!tracking) return;
1208:     var p = at(e);
1209:     var dx = (p.x - px) * SPEED + restX, dy = (p.y - py) * SPEED + restY;
1210:     px = p.x; py = p.y;
1211:     var ix = Math.trunc(dx), iy = Math.trunc(dy);
1212:     restX = dx - ix; restY = dy - iy;
1213:     moved += Math.abs(ix) + Math.abs(iy);
1214:     if (ix || iy) pushMove(ix, iy);
1215:     e.preventDefault();
1216:   }
1217:   function up(e) {
1218:     if (!tracking) return;
1219:     tracking = false;
1220:     pad.classList.remove("live");
1221:     // Let any outstanding movement land first, so the click happens where
1222:     // the finger finished rather than where it was a moment earlier.
1223:     if (moved < 8) send("click=1");
1224:     e.preventDefault();
1225:   }
1226:   pad.addEventListener("touchstart", down, {passive: false});
1227:   pad.addEventListener("touchmove", move, {passive: false});
1228:   pad.addEventListener("touchend", up, {passive: false});
1229:   pad.addEventListener("mousedown", down);
1230:   window.addEventListener("mousemove", move);
1231:   window.addEventListener("mouseup", up);
1232: 
1233:   // This page is scanned before the window exists -- the QR is on the screen
1234:   // the sign-in page then replaces -- so it has to come alive by itself.
1235:   //
1236:   // A probe that fails is counted; five in a row (ten seconds) and the line
1237:   // says the handheld cannot be reached and what to look at, instead of
1238:   // Checking... for as long as the page is open (fork #330: an iPhone with a
1239:   // VPN badge in its status bar showed Checking... for two minutes while
1240:   // its taps went nowhere). The polling goes on: the moment an answer comes
1241:   // the line changes to what it says.
1242:   var failed = 0;
1243:   function unreachable() {
1244:     state.className = "err";
1245:     state.textContent = "Your phone can't reach your handheld. Both need to be "
1246:       + "on the same Wi-Fi, and a VPN on your phone can get in the way.";
1247:   }
1248:   function poll() {
1249:     fetch("/" + pin + "?probe=1", {cache: "no-store"}).then(function (r) {
1250:         if (!r.ok) throw new Error("status " + r.status);
1251:         failed = 0;
1252:         return r.text();
1253:       })
1254:       .then(function (t) {
1255:         // "open <page>" -- the page token changes when the handheld
1256:         // navigates, which is when what is in this box stopped being
1257:         // relevant to what is on that screen.
1258:         var parts = t.trim().split(" ");
1259:         var open = parts[0] === "open";
1260:         var isUp = open || parts[0] === "loading";
1261:         // A new page: what is in the box was for the one before. Noticed
1262:         // while the new one loads too, so what is typed meanwhile is kept
1263:         // for it.
1264:         if (isUp && parts[1] && parts[1] !== page) {
1265:           if (page !== null) { box.value = ""; sent = ""; }
1266:           page = parts[1];
1267:         }
1268:         winUp = isUp;
1269:         state.className = open ? "ok" : "note";
1270:         state.textContent = open
1271:           ? "Connected."
1272:           : isUp
1273:           ? "Opening on your handheld. You can keep typing here; it goes "
1274:             + "across once a box on that page is ready."
1275:           : "Not open yet -- choose CONTINUE on your handheld. You can type "
1276:             + "or paste here meanwhile; it goes across when the page opens.";
1277:         // The box is never disabled. It was, until this said the handheld was
1278:         // ready -- so somebody who scanned the QR first, which is the order
1279:         // this flow asks for, could not type at all and saw nothing appear.
1280:         // Re-asserting disabled every two seconds also dismisses a phone
1281:         // keyboard in the middle of typing.
1282:         //
1283:         // And what was typed meanwhile goes across the moment it opens. The
1284:         // box only ever sent on an input event, so text typed while the page
1285:         // said "not open yet" -- the order this flow asks for -- was never
1286:         // delivered at all, and the next keystroke added only itself (audit
1287:         // #307 PL-016). The window opens on an empty field, so nothing has
1288:         // been sent to it yet: `sent` starts again from nothing. And not
1289:         // before a field has the caret -- open is that, not the window's
1290:         // process starting (claude G2-C-01) -- and again on each new page.
1291:         var opened = open && !ready;
1292:         ready = open;
1293:         if (opened) { sent = ""; deliver(box.value); }
1294:       })
1295:       .catch(function () { if (++failed >= 5) unreachable(); })
1296:       .then(function () { setTimeout(poll, 2000); });
1297:   }
1298:   poll();
1299: })();
1300: </script>
1301: """
1302: 
1303: 
1304: # Linux input constants, from include/uapi/linux/input-event-codes.h.
1305: EV_SYN, EV_KEY = 0x00, 0x01
1306: SYN_REPORT = 0
1307: UI_SET_EVBIT, UI_SET_KEYBIT = 0x40045564, 0x40045565
1308: UI_SET_RELBIT = 0x40045566
1309: EV_REL = 0x02
1310: REL_X, REL_Y, REL_WHEEL = 0x00, 0x01, 0x08
1311: BTN_LEFT = 0x110
1312: # vendor:product:name, as sway forms it -- 0x1209/0x0002 and the device name
1313: # with spaces turned into underscores.
1314: POINTER_ID = "4617:2:ROCKNIX_cloud_pointer"
1315: UI_DEV_CREATE, UI_DEV_DESTROY = 0x5501, 0x5502
1316: 
1317: # US layout, which is what the on-screen keyboard and the browser both assume.
1318: # Only what a sign-in needs: an address, a password, and the keys to correct
1319: # and submit them.
1320: KEYMAP = {}
1321: for _i, _c in enumerate("abcdefghijklmnopqrstuvwxyz"):
1322:     KEYMAP[_c] = ((30, 48, 46, 32, 18, 33, 34, 35, 23, 36, 37, 38, 50,
1323:                    49, 24, 25, 16, 19, 31, 20, 22, 47, 17, 45, 21, 44)[_i], False)
1324: for _i, _c in enumerate("1234567890"):
1325:     KEYMAP[_c] = (2 + _i, False)
1326: KEYMAP.update({
1327:     " ": (57, False), "-": (12, False), "=": (13, False), "[": (26, False),
1328:     "]": (27, False), "\\": (43, False), ";": (39, False), "'": (40, False),
1329:     "`": (41, False), ",": (51, False), ".": (52, False), "/": (53, False),
1330: })
1331: for _plain, _shifted in zip("1234567890-=[]\\;',./`", '!@#$%^&*()_+{}|:"<>?~'):
1332:     KEYMAP[_shifted] = (KEYMAP[_plain][0], True)
1333: for _c in "abcdefghijklmnopqrstuvwxyz":
1334:     KEYMAP[_c.upper()] = (KEYMAP[_c][0], True)
1335: 
1336: NAMED_KEYS = {"enter": 28, "backspace": 14, "tab": 15, "escape": 1,
1337:               "left": 105, "right": 106, "up": 103, "down": 108,
1338:               "home": 102, "end": 107, "delete": 111,
1339:               "pageup": 104, "pagedown": 109,
1340:               "f1": 59, "f2": 60, "f3": 61, "f4": 62}
1341: KEY_LEFTSHIFT = 42
1342: 
1343: # How long a key is held, and the gap before the next one. Roughly 130 words
1344: # per minute -- faster than anyone types, slow enough that a page's own input
1345: # handling sees each keystroke as a separate event.
1346: KEY_HOLD = 0.012
1347: KEY_GAP = 0.022
1348: 
1349: 
1350: class RemoteMouse:
1351:     """A pointer the phone can drag, for the page on the handheld.
1352: 
1353:     A real uinput pointer rather than a cursor we draw: sway renders it and
1354:     WebKit receives genuine pointer events, so hovering, clicking and
1355:     dismissing work on anything a page can put on screen -- including a
1356:     cross-origin iframe, whose contents no amount of focus traversal can
1357:     reach. That is what a consent banner and a "sign in with Google" prompt
1358:     turned out to be, between them covering most of a four-inch screen with
1359:     no way to dismiss either.
1360: 
1361:     The phone is the natural surface to drag it from: it has the touchscreen
1362:     the handheld does not.
1363:     """
1364: 
1365:     def __init__(self):
1366:         self.fd = None
1367: 
1368:     def open(self):
1369:         if self.fd is not None:
1370:             return True
1371:         try:
1372:             fd = os.open(UINPUT, os.O_WRONLY | os.O_NONBLOCK)
1373:         except OSError as exc:
1374:             log("no virtual pointer: %s" % exc)
1375:             return False
1376:         try:
1377:             fcntl.ioctl(fd, UI_SET_EVBIT, EV_REL)
1378:             fcntl.ioctl(fd, UI_SET_EVBIT, EV_KEY)
1379:             fcntl.ioctl(fd, UI_SET_EVBIT, EV_SYN)
1380:             for axis in (REL_X, REL_Y, REL_WHEEL):
1381:                 fcntl.ioctl(fd, UI_SET_RELBIT, axis)
1382:             fcntl.ioctl(fd, UI_SET_KEYBIT, BTN_LEFT)
1383:             name = b"ROCKNIX cloud pointer".ljust(80, b"\0")
1384:             os.write(fd, name + struct.pack("HHHHi", 0x03, 0x1209, 0x0002, 1, 0)
1385:                      + b"\0" * (4 * 64 * 4))
1386:             fcntl.ioctl(fd, UI_DEV_CREATE)
1387:         except OSError as exc:
1388:             log("could not create the virtual pointer: %s" % exc)
1389:             os.close(fd)
1390:             return False
1391:         time.sleep(0.5)
1392:         self.fd = fd
1393: 
1394:         # Flat profile, no acceleration. libinput's default adapts to speed,
1395:         # which is right for a hand on a desk and wrong for a finger on a
1396:         # phone driving somebody else's screen: the same drag covers a
1397:         # different distance depending how fast it was, so the pointer feels
1398:         # to pull towards things and to drift. Flat makes a delta a delta.
1399:         for setting in (["accel_profile", "flat"], ["pointer_accel", "0"]):
1400:             try:
1401:                 subprocess.run(["swaymsg", "input", POINTER_ID] + setting,
1402:                                capture_output=True, timeout=5,
1403:                                env=dict(os.environ, **sway_env()))
1404:             except (OSError, subprocess.SubprocessError) as exc:
1405:                 log("could not flatten the pointer: %s" % exc)
1406:         log("virtual pointer ready")
1407:         return True
1408: 
1409:     def _emit(self, etype, code, value):
1410:         now = time.time()
1411:         os.write(self.fd, struct.pack("llHHi", int(now),
1412:                                       int((now % 1) * 1000000),
1413:                                       etype, code, value))
1414: 
1415:     def move(self, dx, dy):
1416:         if self.fd is None and not self.open():
1417:             return False
1418:         if dx:
1419:             self._emit(EV_REL, REL_X, int(dx))
1420:         if dy:
1421:             self._emit(EV_REL, REL_Y, int(dy))
1422:         self._emit(EV_SYN, SYN_REPORT, 0)
1423:         return True
1424: 
1425:     def click(self):
1426:         if self.fd is None and not self.open():
1427:             return False
1428:         # Press and release as separate reports, for the same reason the
1429:         # keyboard does: a page's own handlers read one fused report as a
1430:         # single indivisible event and often ignore it.
1431:         self._emit(EV_KEY, BTN_LEFT, 1)
1432:         self._emit(EV_SYN, SYN_REPORT, 0)
1433:         time.sleep(0.03)
1434:         self._emit(EV_KEY, BTN_LEFT, 0)
1435:         self._emit(EV_SYN, SYN_REPORT, 0)
1436:         return True
1437: 
1438:     def scroll(self, clicks):
1439:         if self.fd is None and not self.open():
1440:             return False
1441:         self._emit(EV_REL, REL_WHEEL, int(clicks))
1442:         self._emit(EV_SYN, SYN_REPORT, 0)
1443:         return True
1444: 
1445:     def close(self):
1446:         if self.fd is None:
1447:             return
1448:         try:
1449:             fcntl.ioctl(self.fd, UI_DEV_DESTROY)
1450:         except OSError:
1451:             pass
1452:         os.close(self.fd)
1453:         self.fd = None
1454: 
1455: 
1456: class RemoteKeyboard:
1457:     """A keyboard the phone can type on, for the window on the handheld.
1458: 
1459:     The player reads the provider's page on the device's own screen and types
1460:     on the keyboard they already know how to use. Nothing is mirrored, so the
1461:     only thing crossing the network is a keystroke -- which is why this
1462:     replaced streaming the display.
1463: 
1464:     uinput rather than the Wayland virtual-keyboard protocol: it needs no
1465:     Wayland client of our own, and sway picks the device up through libinput
1466:     exactly as it would a keyboard someone plugged in.
1467:     """
1468: 
1469:     def __init__(self):
1470:         self.fd = None
1471: 
1472:     def open(self):
1473:         if self.fd is not None:
1474:             return True
1475:         try:
1476:             fd = os.open(UINPUT, os.O_WRONLY | os.O_NONBLOCK)
1477:         except OSError as exc:
1478:             log("no virtual keyboard: %s" % exc)
1479:             return False
1480:         try:
1481:             fcntl.ioctl(fd, UI_SET_EVBIT, EV_KEY)
1482:             fcntl.ioctl(fd, UI_SET_EVBIT, EV_SYN)
1483:             for code in set(list(NAMED_KEYS.values())
1484:                             + [c for c, _ in KEYMAP.values()] + [KEY_LEFTSHIFT]):
1485:                 fcntl.ioctl(fd, UI_SET_KEYBIT, code)
1486:             # struct uinput_user_dev: name[80], id{bustype,vendor,product,
1487:             # version}, ff_effects_max, then the absmin/max/fuzz/flat arrays.
1488:             name = b"pixelelated cloud sign-in".ljust(80, b"\0")
1489:             os.write(fd, name + struct.pack("HHHHi", 0x03, 0x1209, 0x0001, 1, 0)
1490:                      + b"\0" * (4 * 64 * 4))
1491:             fcntl.ioctl(fd, UI_DEV_CREATE)
1492:         except OSError as exc:
1493:             log("could not create the virtual keyboard: %s" % exc)
1494:             os.close(fd)
1495:             return False
1496:         # udev and libinput need a moment to notice a new device.
1497:         time.sleep(0.5)
1498:         self.fd = fd
1499:         log("virtual keyboard ready")
1500:         return True
1501: 
1502:     def _emit(self, etype, code, value):
1503:         now = time.time()
1504:         os.write(self.fd, struct.pack("llHHi", int(now),
1505:                                       int((now % 1) * 1000000), etype, code, value))
1506: 
1507:     def _tap(self, code, shift=False):
1508:         """One keypress, reported the way a real keyboard reports it.
1509: 
1510:         Each state change is its own SYN_REPORT, and press and release are
1511:         separated in time. Sending press and release in a single report, with
1512:         zero timestamps, is not what any hardware does: libinput and the
1513:         page's own input handling both read it as one indivisible blur, and a
1514:         typed address arrived truncated -- six characters of sixteen. The
1515:         delays below are what a fast typist produces, and cost nothing that
1516:         matters when the whole point is to save somebody a minute on a d-pad.
1517:         """
1518:         if shift:
1519:             self._emit(EV_KEY, KEY_LEFTSHIFT, 1)
1520:             self._emit(EV_SYN, SYN_REPORT, 0)
1521:             time.sleep(KEY_GAP)
1522:         self._emit(EV_KEY, code, 1)
1523:         self._emit(EV_SYN, SYN_REPORT, 0)
1524:         time.sleep(KEY_HOLD)
1525:         self._emit(EV_KEY, code, 0)
1526:         self._emit(EV_SYN, SYN_REPORT, 0)
1527:         if shift:
1528:             time.sleep(KEY_GAP)
1529:             self._emit(EV_KEY, KEY_LEFTSHIFT, 0)
1530:             self._emit(EV_SYN, SYN_REPORT, 0)
1531: 
1532:     def type_text(self, text):
1533:         """Send printable characters. Returns how many were sent."""
1534:         if not self.open():
1535:             return 0
1536:         sent = 0
1537:         for char in text:
1538:             entry = KEYMAP.get(char)
1539:             if entry is None:
1540:                 continue        # not on a US layout; silently skipped
1541:             self._tap(*entry)
1542:             time.sleep(KEY_GAP)
1543:             sent += 1
1544:         return sent
1545: 
1546:     def press(self, name):
1547:         code = NAMED_KEYS.get(name)
1548:         if code is None or not self.open():
1549:             return False
1550:         self._tap(code)
1551:         return True
1552: 
1553:     def close(self):
1554:         if self.fd is None:
1555:             return
1556:         try:
1557:             fcntl.ioctl(self.fd, UI_DEV_DESTROY)
1558:         except OSError:
1559:             pass
1560:         os.close(self.fd)
1561:         self.fd = None
1562: 
1563: 
1564: # The handheld's controls, as the kernel reports them. A gamepad is not a
1565: # keyboard: sway classifies this one as a tablet_pad, so GTK and WebKit
1566: # receive nothing at all from it. Without this bridge the sign-in page is
1567: # visible on the device and cannot be touched from the device -- and, worse,
1568: # cannot be left.
1569: BTN_SOUTH, BTN_EAST, BTN_NORTH, BTN_WEST = 304, 305, 307, 308
1570: BTN_TL, BTN_TR, BTN_SELECT, BTN_START, BTN_MODE = 310, 311, 314, 315, 316
1571: BTN_DPAD_UP, BTN_DPAD_DOWN, BTN_DPAD_LEFT, BTN_DPAD_RIGHT = 544, 545, 546, 547
1572: # A d-pad is not always four buttons. HID and xpad-class pads report it as a
1573: # hat -- two axes that read -1, 0 or 1 -- and the bridge used to find only
1574: # pads with BTN_DPAD_UP and to drop every EV_ABS event, so on such a pad the
1575: # page could not be driven and Select+Start never reached it (#308 gpt
1576: # F-RS-16, claude F-RS-06).
1577: EV_ABS = 0x03
1578: ABS_HAT0X, ABS_HAT0Y = 0x10, 0x11
1579: HAT_KEYS = {(ABS_HAT0X, -1): "left", (ABS_HAT0X, 1): "right",
1580:             (ABS_HAT0Y, -1): "up", (ABS_HAT0Y, 1): "down"}
1581: SYS_INPUT = "/sys/class/input"
1582: DEV_INPUT = "/dev/input"
1583: 
1584: # Arrows rather than Tab: WebKit's spatial navigation moves focus in the
1585: # direction pressed, which is what a d-pad means. Tab order on a login page
1586: # wanders through cookie banners and footer links.
1587: # BTN_EAST is the button labelled A on this hardware, not BTN_SOUTH. These
1588: # handhelds use the Nintendo layout, where A sits in the east position --
1589: # EmulationStation's own es_input.cfg maps a=button 1 (BTN_EAST) and
1590: # b=button 0 (BTN_SOUTH). Taking the Xbox reading meant the player pressed A
1591: # and got a backspace.
1592: GAMEPAD_KEYS = {
1593:     BTN_DPAD_UP: "up", BTN_DPAD_DOWN: "down",
1594:     BTN_DPAD_LEFT: "left", BTN_DPAD_RIGHT: "right",
1595:     BTN_EAST: "enter",             # A activates what is focused
1596:     BTN_SOUTH: "backspace",        # B goes back, as it does everywhere else
1597:     # Y reaches a consent banner first, then behaves as Tab. The d-pad
1598:     # cannot get to one at all -- spatial navigation will not descend into a
1599:     # fixed-position element -- and Tab alone costs about ten presses.
1600:     BTN_NORTH: "f4",
1601:     BTN_WEST: "f1",                # X shows and hides the on-screen keyboard
1602:     # L1/R1 scroll the page. The window turns these into a scroll in the
1603:     # page rather than page-up/page-down, which do nothing while a text
1604:     # field has the caret -- which is most of a sign-in form, and exactly
1605:     # when the button below the fold is what cannot be reached.
1606:     BTN_TL: "f2", BTN_TR: "f3",
1607: }
1608: 
1609: # Select held, then Start: the same combination RetroArch uses to leave a
1610: # game on this hardware, so it is already in players' fingers.
1611: # A combination rather than any single button. Select alone is far too easy
1612: # to catch while reaching across a small handheld, and losing a half-typed
1613: # password to a stray thumb is worse than needing two buttons to leave.
1614: #
1615: # Either Select or Mode holds it, because which one is "the hotkey" is not
1616: # the same on every handheld. On the RG35XX SP, ES's own es_input.cfg maps
1617: # hotkeyenable to button 8, which is BTN_MODE on that pad -- not Select. A
1618: # player whose muscle memory is Mode+Start would find Select+Start does
1619: # nothing, and a player who knows Select+Start would find the same. Both
1620: # are two-button combinations and neither is reachable by a stray thumb,
1621: # so accepting both costs nothing and guesses at nothing.
1622: GAMEPAD_HOLD = (BTN_SELECT, BTN_MODE)
1623: GAMEPAD_QUIT = BTN_START
1624: 
1625: 
1626: def find_gamepad():
1627:     """The device node for the handheld's controls, and the buttons it has.
1628: 
1629:     Named lookups would need a table per device -- "H700 Gamepad" on one
1630:     handheld is something else on the next. A device carrying BTN_SOUTH and a
1631:     d-pad is a gamepad whatever it calls itself.
1632: 
1633:     Returns (node, codes) so callers can ask what the pad actually has
1634:     rather than assume. Nothing here is uniform across handhelds: the
1635:     RG35XX SP has a Mode button and ES maps its hotkey to it, while smaller
1636:     pads have no such button at all.
1637:     """
1638:     try:
1639:         entries = sorted(os.listdir(SYS_INPUT))
1640:     except OSError:
1641:         return None, set()
1642:     for entry in entries:
1643:         if not entry.startswith("event"):
1644:             continue
1645:         codes = _capabilities(entry, "key")
1646:         if codes is None:
1647:             continue
1648:         axes = _capabilities(entry, "abs") or set()
1649:         if not (BTN_SOUTH in codes and (BTN_DPAD_UP in codes or ABS_HAT0Y in axes)):
1650:             continue
1651:         node = DEV_INPUT + "/" + entry
1652:         # sysfs lists a pad whose node is gone: on the Retroid Pocket Nova
1653:         # InputPlumber hides the physical "AYN Odin2 Gamepad" (event3) behind
1654:         # its own virtual controller (event7), and the first match could not
1655:         # be opened -- so the bridge ran with no pad and SELECT + START could
1656:         # not leave the window (fork #331). A candidate that cannot be
1657:         # opened is passed over, and the log says which one and why.
1658:         try:
1659:             os.close(os.open(node, os.O_RDONLY))
1660:         except OSError as exc:
1661:             log("gamepad: %s (%s) cannot be opened: %s; trying the next"
1662:                 % (node, _device_name(entry), exc.strerror or exc))
1663:             continue
1664:         return node, codes
1665:     return None, set()
1666: 
1667: 
1668: def _device_name(entry):
1669:     """The kernel's name for an input device, for the log; empty when unreadable."""
1670:     try:
1671:         with open("%s/%s/device/name" % (SYS_INPUT, entry)) as handle:
1672:             return handle.read().strip()
1673:     except OSError:
1674:         return ""
1675: 
1676: 
1677: def _capabilities(entry, kind):
1678:     """The codes an input device reports for one event type, from sysfs's
1679:     bitmap (hex words, most significant first), or None when unreadable."""
1680:     try:
1681:         with open("%s/%s/device/capabilities/%s" % (SYS_INPUT, entry, kind)) as handle:
1682:             words = handle.read().split()
1683:     except (OSError, ValueError):
1684:         return None
1685:     codes = set()
1686:     for index, word in enumerate(reversed(words)):
1687:         value = int(word, 16)
1688:         codes |= {index * 64 + bit for bit in range(value.bit_length())
1689:                   if value >> bit & 1}
1690:     return codes
1691: 
1692: 
1693: def exit_hint():
1694:     """What the page and the window call the exit combination: one string,
1695:     the same on every handheld. It reads nothing from the pad.
1696: 
1697:     Either Select or Mode holds it (GAMEPAD_HOLD), because which one a player
1698:     reaches for differs by device -- the RG351M and RG353M have no Mode
1699:     button, the RG35XX SP does and ES maps its own hotkey to it. The words
1700:     name only the pair every handheld has (#308 claude F-RS-14: this said it
1701:     read the pad).
1702:     """
1703:     # One combination on screen, always. "MODE OR SELECT + START" read as
1704:     # though Mode alone were a way out, and a help line that has to be parsed
1705:     # is worse than one that covers fewer of the buttons that happen to work.
1706:     # Mode is still accepted -- see GAMEPAD_HOLD -- it is simply not what we
1707:     # tell people, because Select and Start are labelled on every handheld we
1708:     # ship for and Mode is not.
1709:     return "SELECT + START"
1710: 
1711: 
1712: # _IOW('E', 0x90, int) -- take a device exclusively, so nobody else sees it.
1713: EVIOCGRAB = 0x40044590
1714: 
1715: 
1716: def signin_window_running():
1717:     """Is the sign-in window up?
1718: 
1719:     Matched on argv[0], not on comm: comm truncates at 15 characters, so
1720:     "cloud-signin-window" appears there as "cloud-signin-wi". A pattern that
1721:     looks right and matches nothing has already cost this project a cleanup
1722:     loop that silently did nothing.
1723:     """
1724:     for entry in os.listdir("/proc"):
1725:         if not entry.isdigit():
1726:             continue
1727:         try:
1728:             with open("/proc/%s/cmdline" % entry, "rb") as handle:
1729:                 argv = handle.read().split(b"\0")
1730:         except OSError:
1731:             continue
1732:         if argv and argv[0].decode("utf-8", "replace") == SIGNIN_WINDOW:
1733:             return True
1734:     return False
1735: 
1736: 
1737: def pad_is_free():
1738:     """Can somebody else open the gamepad exclusively?
1739: 
1740:     This is the condition EmulationStation needs before it re-initialises:
1741:     SDL re-opens the joystick on init, and if our bridge still held the grab
1742:     ES would come back with no gamepad at all until it was restarted. Testing
1743:     the grab directly beats sleeping and hoping.
1744:     """
1745:     node, _codes = find_gamepad()
1746:     if not node:
1747:         return True
1748:     try:
1749:         fd = os.open(node, os.O_RDONLY)
1750:     except OSError:
1751:         return True
1752:     try:
1753:         fcntl.ioctl(fd, EVIOCGRAB, 1)
1754:         fcntl.ioctl(fd, EVIOCGRAB, 0)
1755:         return True
1756:     except OSError:
1757:         return False
1758:     finally:
1759:         os.close(fd)
1760: 
1761: 
1762: class GamepadBridge:
1763:     """Turn the handheld's buttons into keystrokes for the sign-in page.
1764: 
1765:     Reads the gamepad's event node and replays each press through the same
1766:     virtual keyboard the phone types on.
1767: 
1768:     It takes the pad **exclusively** (EVIOCGRAB) for as long as the window is
1769:     up. EmulationStation is still running behind this page and holds the same
1770:     node open; SDL joystick events are not gated on window focus the way
1771:     keyboard events are, and `InputManager::parseEvent` runs for every event
1772:     with no foreground check. So without the grab every d-pad press and every
1773:     A meant for the provider's page is also driving the menu behind it --
1774:     scrolling it, and activating whatever row happens to be selected.
1775: 
1776:     Typing was never affected: keys reach the compositor, which delivers them
1777:     to the focused surface only.
1778: 
1779:     A grab that outlived the window would leave the player holding a handheld
1780:     whose buttons do nothing, so the loop watches the browser process and
1781:     releases the moment it is gone -- see the select() timeout below, which
1782:     exists to make that check happen even when nobody is pressing anything.
1783:     """
1784: 
1785:     def __init__(self, keyboard, on_quit, alive=None):
1786:         self.keyboard = keyboard
1787:         self.on_quit = on_quit
1788:         self.alive = alive
1789:         self.thread = None
1790:         self.stop_flag = threading.Event()
1791: 
1792:     def start(self):
1793:         node, _codes = find_gamepad()
1794:         if not node:
1795:             log("no gamepad found; the sign-in page can only be driven from a phone")
1796:             return False
1797:         # Opened here, so the log says "reading" only once it is (the Nova's
1798:         # log read "could not read the gamepad" and then "gamepad bridge
1799:         # reading /dev/input/event3", in that order; fork #331).
1800:         try:
1801:             fd = os.open(node, os.O_RDONLY)
1802:         except OSError as exc:
1803:             log("could not read the gamepad %s: %s; the sign-in page can only be driven from a phone"
1804:                 % (node, exc.strerror or exc))
1805:             return False
1806:         self.thread = threading.Thread(target=self._run, args=(fd, node), daemon=True)
1807:         self.thread.start()
1808:         log("gamepad bridge reading %s (%s)" % (node, _device_name(os.path.basename(node))))
1809:         return True
1810: 
1811:     def _run(self, fd, node):
1812:         grabbed = False
1813:         try:
1814:             fcntl.ioctl(fd, EVIOCGRAB, 1)
1815:             grabbed = True
1816:         except OSError as exc:
1817:             # Not fatal: the page is still drivable, EmulationStation just
1818:             # sees the same presses. Worth saying so in the log, because the
1819:             # symptom is a menu that moved on its own.
1820:             log("could not take the gamepad exclusively: %s" % exc)
1821: 
1822:         size = struct.calcsize("llHHi")
1823:         held = set()
1824:         hat = {}
1825:         try:
1826:             while not self.stop_flag.is_set():
1827:                 # The timeout is the watchdog's heartbeat, not a poll for
1828:                 # input: without it this blocks in read() and a window that
1829:                 # died would leave the pad grabbed until someone pressed a
1830:                 # button.
1831:                 ready, _, _ = select.select([fd], [], [], 0.5)
1832:                 if self.alive is not None and not self.alive():
1833:                     log("sign-in window is gone; releasing the gamepad")
1834:                     self.on_quit()
1835:                     return
1836:                 if not ready:
1837:                     continue
1838:                 data = os.read(fd, size)
1839:                 if len(data) < size:
1840:                     continue
1841:                 _, _, etype, code, value = struct.unpack("llHHi", data)
1842:                 if etype == EV_ABS:
1843:                     # A hat moving off centre is the arrow's press; back to
1844:                     # centre, or on to the same side again, is nothing.
1845:                     name = HAT_KEYS.get((code, value))
1846:                     if name and hat.get(code) != value:
1847:                         self.keyboard.press(name)
1848:                     if code in (ABS_HAT0X, ABS_HAT0Y):
1849:                         hat[code] = value
1850:                     continue
1851:                 if etype != EV_KEY:
1852:                     continue
1853: 
1854:                 if value == 0:
1855:                     held.discard(code)
1856:                     continue
1857:                 if value != 1:            # 2 is autorepeat; ignore
1858:                     continue
1859:                 held.add(code)
1860: 
1861:                 # Either order, so it does not matter which thumb gets there
1862:                 # first.
1863:                 held_any = any(h in held for h in GAMEPAD_HOLD)
1864:                 if ((code == GAMEPAD_QUIT and held_any)
1865:                         or (code in GAMEPAD_HOLD and GAMEPAD_QUIT in held)):
1866:                     log("player ended the sign-in from the handheld")
1867:                     self.on_quit()
1868:                     return
1869: 
1870:                 # A hold button does not type on its own.
1871:                 if code in GAMEPAD_HOLD:
1872:                     continue
1873:                 name = GAMEPAD_KEYS.get(code)
1874:                 if name:
1875:                     self.keyboard.press(name)
1876:         except OSError:
1877:             pass
1878:         finally:
1879:             if grabbed:
1880:                 try:
1881:                     fcntl.ioctl(fd, EVIOCGRAB, 0)
1882:                 except OSError:
1883:                     pass
1884:             os.close(fd)
1885: 
1886:     def stop(self):
1887:         self.stop_flag.set()
1888:         # Wait for the reader to actually leave, because it releases the
1889:         # gamepad on its way out and the caller's next move may be to hand
1890:         # the pad back to EmulationStation.
1891:         thread, self.thread = self.thread, None
1892:         if thread and thread is not threading.current_thread():
1893:             thread.join(timeout=2)
1894: 
1895: 
1896: class SessionHolder:
1897:     """The server outlives any one sign-in attempt.
1898: 
1899:     rclone's authorize server answers exactly one redirect and then exits, so
1900:     a code that arrives expired -- which is the normal way this fails, the
1901:     window being a couple of minutes -- ends the attempt. Without somewhere to
1902:     start another, the player is sent back to the handheld to redo a flow they
1903:     had almost finished. So the attempt is replaceable and the *server* is what
1904:     persists, along with the PIN: the handheld is showing that PIN and a QR
1905:     built from it, and neither can be re-issued from here.
1906:     """
1907: 
1908:     def __init__(self, backend, remote_name, label, timeout, replace=False):
1909:         self.backend = backend
1910:         self.remote_name = remote_name
1911:         self.replace = replace
1912:         self.name = display_name(backend, label)
1913:         self.timeout = timeout
1914:         self.pin = "%04d" % secrets.randbelow(10000)
1915:         # Which serve the shared state belongs to (write_owned).
1916:         self.attempt = secrets.token_hex(6)
1917:         self.pin_attempts = 0
1918:         self.lock = threading.Lock()
1919:         self.session = None
1920:         self.browser = None
1921:         self.keyboard = RemoteKeyboard()
1922:         self.mouse = RemoteMouse()
1923:         self.gamepad = None
1924: 
1925:     def start(self):
1926:         session = Session(self.backend, self.remote_name, self.timeout)
1927:         session.replace = self.replace
1928:         # When the sign-in finishes on the device, take the page away rather
1929:         # than leaving rclone's own "All done, go back to rclone" sitting
1930:         # there -- a sentence about a program the player has never heard of,
1931:         # on a screen with no way out but a button combination.
1932:         session.on_signed_in = self.signed_in
1933:         session.attempt = self.attempt
1934:         # The state names this session from here, and moves to starting:
1935:         # the old session's collector can write nothing more, whatever
1936:         # wakes it, and this one's own failure -- its rclone dying before
1937:         # anybody says waiting -- is recorded where the caller's waiting
1938:         # write will find it (PL-032). Not over a sign-in that has landed,
1939:         # a cancel's idle, or another serve's state.
1940:         session.gen = secrets.token_hex(4)
1941:         if not write_owned(self.attempt, from_status=(None, "starting", "waiting", "failed"),
1942:                            status="starting", session=session.gen, error=""):
1943:             if read_state().get("status") == "signed-in":
1944:                 return False, "You're signed in already."
1945:             return False, "Another sign-in has taken over from this one."
1946:         # Before the new attempt kills the old one's rclone (Session.start),
1947:         # so the old collector knows its end is not a failure to report.
1948:         if self.session:
1949:             self.session.superseded = True
1950:         if not session.start():
1951:             # Said in the state as well as to the caller: a restart whose
1952:             # rclone offered no link left the handheld reading waiting, with
1953:             # the old rclone killed and nothing able to finish it (claude
1954:             # G2-C-04).
1955:             write_owned(self.attempt, owner=session.gen, status="failed",
1956:                         error=session.error)
1957:             return False, session.error
1958:         with self.lock:
1959:             self.stop_browser()
1960:             self.session = session
1961:         return True, None
1962: 
1963:     def signed_in(self):
1964:         """The sign-in landed.
1965: 
1966:         The window is deliberately left open. EmulationStation is suspended
1967:         while the page owns the screen and takes several seconds to rebuild
1968:         everything it released; closing here put a black screen in front of
1969:         the player at the moment their sign-in had just succeeded, which
1970:         reads as a crash rather than as progress. The window switches itself
1971:         to "Finishing up" when it sees this marker, and is closed once ES is
1972:         drawing again and asks for it.
1973: 
1974:         The pad is handed back first, though, before the marker exists.
1975:         "Finishing up" takes no input, and `wait` returns on this marker --
1976:         after which EmulationStation re-opens the joystick, which it cannot
1977:         do while the bridge holds EVIOCGRAB (pad_is_free). The bridge used to
1978:         let go only when the window died, which is after that re-open (audit
1979:         #307 PL-018).
1980:         """
1981:         gamepad, self.gamepad = self.gamepad, None
1982:         if gamepad:
1983:             gamepad.stop()
1984:         os.makedirs(STATE_DIR, exist_ok=True)
1985:         try:
1986:             open(state_path("signed-in"), "w").close()
1987:         except OSError:
1988:             self.stop_browser()
1989: 
1990:     def start_browser(self):
1991:         """Open the provider's page here, for the handheld or a phone to drive."""
1992:         if not browser_stack_available() or not self.session:
1993:             return False
1994:         self.stop_browser()
1995:         host = urllib.parse.urlparse(self.session.provider).hostname or ""
1996:         browser = BrowserSession(self.session.provider, host)
1997:         if not browser.start():
1998:             return False
1999:         with self.lock:
2000:             self.browser = browser
2001: 
2002:         # The handheld's own controls, and with them a way back out. Without
2003:         # this the page is on the screen, cannot be driven from the device,
2004:         # and cannot be closed -- which strands the handheld in a browser.
2005:         self.keyboard.open()
2006:         self.mouse.open()
2007:         self.gamepad = GamepadBridge(self.keyboard, self.stop_browser,
2008:                                      alive=browser.is_running)
2009:         self.gamepad.start()
2010:         return True
2011: 
2012:     def end(self):
2013:         """Take everything this serve started down: the window, and rclone.
2014: 
2015:         The session is marked first: killing its rclone wakes its collector,
2016:         and a serve ending -- cancelled, timed out, finished -- is not a
2017:         sign-in that failed (G-C-02 claude). What the serve had to say about
2018:         how it ended it has already written.
2019:         """
2020:         if self.session:
2021:             self.session.superseded = True
2022:         self.stop_browser()
2023:         if self.session and self.session.proc \
2024:                 and self.session.proc.poll() is None:
2025:             self.session.proc.send_signal(signal.SIGTERM)
2026:         # A collector that had its token and is saving the remote is let
2027:         # finish -- bounded by rclone's own create and the check's 20 s --
2028:         # so what it made is published or taken away again (PL-032), not
2029:         # left half made by a process that exits under it. One without a
2030:         # token ends as soon as its rclone does.
2031:         collector = self.session.collector if self.session else None
2032:         if collector and collector is not threading.current_thread():
2033:             collector.join(timeout=45)
2034: 
2035:     def stop_browser(self):
2036:         gamepad, self.gamepad = self.gamepad, None
2037:         if gamepad:
2038:             gamepad.stop()
2039:         browser, self.browser = self.browser, None
2040:         if browser:
2041:             browser.stop()
2042:         self.keyboard.close()
2043:         self.mouse.close()
2044: 
2045:     def pin_exhausted(self):
2046:         with self.lock:
2047:             return self.pin_attempts >= 10
2048: 
2049:     def pin_failed(self):
2050:         with self.lock:
2051:             self.pin_attempts += 1
2052:             return self.pin_attempts >= 10
2053: 
2054:     def authorised(self, pin):
2055:         return secrets.compare_digest(str(pin), self.pin)
2056: 
2057: 
2058: # What an unauthenticated client on the LAN can make this spend before the
2059: # PIN is checked. The body was read whole, whatever Content-Length said, on
2060: # a thread per connection with no read deadline and no limit on threads --
2061: # memory and threads that WebKit, on a 1 GB handheld, needs more (#308 gpt
2062: # F-RS-18). The keyboard's largest request is a paste of a few hundred
2063: # bytes.
2064: MAX_BODY = 64 * 1024
2065: REQUEST_TIMEOUT = 15
2066: MAX_CONNECTIONS = 16
2067: 
2068: 
2069: class BoundedHTTPServer(http.server.ThreadingHTTPServer):
2070:     """ThreadingHTTPServer with a cap on connections handled at once: one
2071:     past the cap is closed on arrival rather than given a thread."""
2072: 
2073:     daemon_threads = True
2074: 
2075:     def __init__(self, *args, **kwargs):
2076:         self.slots = threading.BoundedSemaphore(MAX_CONNECTIONS)
2077:         super().__init__(*args, **kwargs)
2078: 
2079:     def process_request(self, request, client_address):
2080:         if not self.slots.acquire(blocking=False):
2081:             self.shutdown_request(request)
2082:             return
2083:         try:
2084:             super().process_request(request, client_address)
2085:         except Exception:
2086:             self.slots.release()
2087:             raise
2088: 
2089:     def process_request_thread(self, request, client_address):
2090:         try:
2091:             super().process_request_thread(request, client_address)
2092:         finally:
2093:             self.slots.release()
2094: 
2095: 
2096: def make_server(address, port, holder, shutdown):
2097:     """The listener, bound -- OSError when the address or port cannot be."""
2098:     server = BoundedHTTPServer((address, port), None)
2099:     server.RequestHandlerClass = make_handler(holder, shutdown)
2100:     return server
2101: 
2102: 
2103: def make_handler(holder, shutdown):
2104:     class Handler(http.server.BaseHTTPRequestHandler):
2105:         # Applied to the socket by StreamRequestHandler.setup: a request
2106:         # that stalls -- mid-headers or mid-body -- is dropped at this.
2107:         timeout = REQUEST_TIMEOUT
2108: 
2109:         def log_message(self, *args):
2110:             pass  # its default writes request lines to stderr
2111: 
2112:         def _send(self, body, status=200):
2113:             encoded = body.encode()
2114:             self.send_response(status)
2115:             self.send_header("Content-Type", "text/html; charset=utf-8")
2116:             self.send_header("Content-Length", str(len(encoded)))
2117:             self.end_headers()
2118:             self.wfile.write(encoded)
2119: 
2120:         def _render(self, message=""):
2121:             # A phone is a keyboard for the page on the handheld, and nothing
2122:             # else. It used to be offered the whole sign-in -- a link to the
2123:             # provider and a box to paste the redirect back into -- which is
2124:             # what a tester did on scanning the QR, because it was there. That
2125:             # flow only ever existed because the handheld could not show the
2126:             # page itself; where it can, offering both is offering a wrong
2127:             # turn.
2128:             if browser_stack_available():
2129:                 self._send(phone_page(holder.name, holder.pin))
2130:                 return
2131: 
2132:             self._send(PAGE % {
2133:                 "style": STYLE,
2134:                 "name": holder.name,
2135:                 "provider": holder.session.provider if holder.session else "",
2136:                 "pin": holder.pin,
2137:                 "message": message,
2138:                 "here": "",
2139:             })
2140: 
2141:         def _render_pin(self, message="", supplied=""):
2142:             self._send(PIN_PAGE % {
2143:                 "style": STYLE,
2144:                 "message": message,
2145:                 # Pre-fills the box. Every caller passes nothing: a wrong PIN
2146:                 # is not echoed back, so a guess learns nothing from the page
2147:                 # (#308 claude F-RS-14: this said a mistyped digit was
2148:                 # carried back).
2149:                 "pin": supplied,
2150:             })
2151: 
2152:         def _render_done(self, remote):
2153:             self._send(DONE_PAGE % {
2154:                 "style": STYLE, "name": holder.name, "remote": remote,
2155:             })
2156: 
2157:         def _gate(self, pin):
2158:             """True when the request may proceed; renders the refusal if not."""
2159:             if holder.pin_exhausted():
2160:                 self.send_error(403, "Too many wrong PINs. Start again on "
2161:                                      "the handheld.")
2162:                 return False
2163:             if holder.authorised(pin):
2164:                 return True
2165:             # No PIN at all is somebody typing the bare address, which is the
2166:             # documented fallback -- ask, do not refuse. A wrong one is either
2167:             # a typo or a guess, and both are answered the same way so neither
2168:             # learns anything the other does not.
2169:             if not pin:
2170:                 self._render_pin()
2171:             elif holder.pin_failed():
2172:                 self.send_error(403, "Too many wrong PINs. Start again on "
2173:                                      "the handheld.")
2174:             else:
2175:                 self._render_pin('<div class=err>That PIN did not match.</div>',
2176:                                  supplied="")
2177:             return False
2178: 
2179:         def _supplied(self):
2180:             """The PIN, from wherever this request carries it.
2181: 
2182:             The address shown on the handheld is http://<device>:8080/7677 --
2183:             the PIN is the tail of the one thing on screen, rather than a
2184:             second number displayed beside it that only the minority who type
2185:             the address rather than scanning it will ever need. ?pin= is still
2186:             accepted: it is what the prompt below submits, and what an older
2187:             QR still in somebody's camera roll would carry.
2188:             """
2189:             parsed = urllib.parse.urlparse(self.path)
2190:             from_query = urllib.parse.parse_qs(parsed.query).get("pin", [""])[0]
2191:             if from_query:
2192:                 return from_query
2193:             return parsed.path.strip("/").split("/")[0]
2194: 
2195:         def do_GET(self):
2196:             if not self._gate(self._supplied()):
2197:                 return
2198: 
2199:             # Is the page actually up on the handheld yet? The keyboard page
2200:             # asks every couple of seconds, because it is scanned before the
2201:             # window exists and has to start working by itself when it does.
2202:             query = urllib.parse.parse_qs(
2203:                 urllib.parse.urlparse(self.path).query)
2204:             if query.get("probe"):
2205:                 # The page token is a short hash of the address the window is
2206:                 # showing: enough for the phone to notice a change, without
2207:                 # putting a provider URL with its state parameter into a
2208:                 # response anybody on the LAN could ask for.
2209:                 token = ""
2210:                 try:
2211:                     with open(state_path("page")) as handle:
2212:                         token = hashlib.sha256(
2213:                             handle.read().encode()).hexdigest()[:8]
2214:                 except OSError:
2215:                     pass
2216:                 # open once a field on the window's page has had the caret
2217:                 # (the window's field record); loading while it is up and
2218:                 # nothing has. The window's process starting was open, and
2219:                 # the phone sent what it held at once, while the provider's
2220:                 # page was still loading and focus_first had placed no
2221:                 # caret: the text went nowhere and, being counted as sent,
2222:                 # was never resent (the audit of the fix round, claude
2223:                 # G2-C-01).
2224:                 # A sign-in that has landed stays open: the window shows its
2225:                 # own "Finishing up" page, which has no field.
2226:                 if not holder.browser:
2227:                     body = b"waiting"
2228:                 elif os.path.exists(state_path("field")) \
2229:                         or os.path.exists(state_path("signed-in")):
2230:                     body = ("open " + token).strip().encode()
2231:                 else:
2232:                     body = ("loading " + token).strip().encode()
2233:                 self.send_response(200)
2234:                 self.send_header("Content-Type", "text/plain; charset=utf-8")
2235:                 self.send_header("Content-Length", str(len(body)))
2236:                 self.end_headers()
2237:                 self.wfile.write(body)
2238:                 return
2239: 
2240:             self._render()
2241: 
2242:         def do_POST(self):
2243:             # Checked before a byte of the body is read.
2244:             try:
2245:                 length = int(self.headers.get("Content-Length", 0))
2246:             except ValueError:
2247:                 length = -1
2248:             if length < 0 or length > MAX_BODY:
2249:                 self.send_response(413 if length > MAX_BODY else 400)
2250:                 self.send_header("Content-Length", "0")
2251:                 self.send_header("Connection", "close")
2252:                 self.end_headers()
2253:                 self.close_connection = True
2254:                 return
2255:             fields = urllib.parse.parse_qs(
2256:                 self.rfile.read(length).decode("utf-8", "replace"))
2257:             if not self._gate(fields.get("pin", [""])[0] or self._supplied()):
2258:                 return
2259: 
2260:             if fields.get("move") or fields.get("click") or fields.get("wheel"):
2261:                 if not holder.browser:
2262:                     self.send_response(409)
2263:                     self.send_header("Content-Length", "0")
2264:                     self.end_headers()
2265:                     return
2266:                 moved = fields.get("move", [""])[0]
2267:                 if moved:
2268:                     try:
2269:                         dx, dy = (int(float(v)) for v in moved.split(",", 1))
2270:                     except ValueError:
2271:                         dx = dy = 0
2272:                     holder.mouse.move(dx, dy)
2273:                 wheel = fields.get("wheel", [""])[0]
2274:                 if wheel:
2275:                     try:
2276:                         holder.mouse.scroll(int(float(wheel)))
2277:                     except ValueError:
2278:                         pass
2279:                 if fields.get("click"):
2280:                     holder.mouse.click()
2281:                 self.send_response(204)
2282:                 self.send_header("Content-Length", "0")
2283:                 self.end_headers()
2284:                 return
2285: 
2286:             if fields.get("type") or fields.get("key"):
2287:                 if not holder.browser:
2288:                     # 409 rather than a rendered page: the keyboard posts by
2289:                     # fetch and throwing HTML at it would replace nothing and
2290:                     # tell nobody. Its own poll is what reports this state.
2291:                     self.send_response(409)
2292:                     self.send_header("Content-Length", "0")
2293:                     self.end_headers()
2294:                     return
2295:                 text = fields.get("type", [""])[0]
2296:                 named = fields.get("key", [""])[0]
2297:                 sent = holder.keyboard.type_text(text) if text else 0
2298:                 if named:
2299:                     holder.keyboard.press(named)
2300:                 self.send_response(204)
2301:                 self.send_header("Content-Length", "0")
2302:                 self.end_headers()
2303:                 # Counts only: what was typed may be a password.
2304:                 log("typed %d characters%s%s" % (
2305:                     sent, " + " + named if named else "",
2306:                     ", %d not on the keyboard" % (len(text) - sent) if len(text) > sent else ""))
2307:                 return
2308: 
2309:             if fields.get("restart"):
2310:                 ok, error = holder.start()
2311:                 # Waiting only from the starting the new attempt began with:
2312:                 # its rclone may already have died, and its collector said
2313:                 # so, before this line ran (PL-032, gpt G2-C-02).
2314:                 if ok and write_owned(holder.attempt, owner=holder.session.gen,
2315:                                       from_status=("starting",),
2316:                                       status="waiting",
2317:                                       provider=holder.session.provider):
2318:                     self._render('<div class=ok>Ready for another go. '
2319:                                  'Sign in below.</div>')
2320:                     return
2321:                 if ok:
2322:                     error = read_state().get("error") or \
2323:                         "That sign-in ended before it could start."
2324:                 again = ""
2325:                 if read_state().get("status") != "signed-in":
2326:                     again = ('<form method=post>'
2327:                              '<input type=hidden name=pin value="%s">'
2328:                              '<input type=hidden name=restart value="1">'
2329:                              '<button class=minor type=submit>'
2330:                              'Start a new sign-in</button></form>' % holder.pin)
2331:                 self._render('<div class=err>%s</div>%s' % (error, again))
2332:                 return
2333: 
2334:             session = holder.session
2335:             if session is None:
2336:                 self._render('<div class=err>No sign-in is running.</div>')
2337:                 return
2338: 
2339:             ok, detail = session.submit(fields.get("code", [""])[0])
2340:             if ok:
2341:                 self._render_done(detail)
2342:                 threading.Timer(2.0, shutdown).start()
2343:                 return
2344: 
2345:             # A dead attempt gets a way forward on this page rather than an
2346:             # instruction to walk back to the handheld and redo the flow.
2347:             restart = ""
2348:             if session.finished():
2349:                 restart = ('<form method=post>'
2350:                            '<input type=hidden name=pin value="%s">'
2351:                            '<input type=hidden name=restart value="1">'
2352:                            '<button class=minor type=submit>'
2353:                            'Start a new sign-in</button></form>' % holder.pin)
2354:             self._render('<div class=err>%s</div>%s' % (detail, restart))
2355: 
2356:     return Handler
2357: 
2358: 
2359: def cmd_serve(backend, remote_name, label, port, timeout, replace=False):
2360:     if not shutil.which("rclone") and not os.path.exists(RCLONE):
2361:         sys.stderr.write("rclone is not installed\n")
2362:         return 2
2363: 
2364:     # Nothing from the last attempt survives into this one -- including a
2365:     # serve still holding the port.
2366:     stop_other_serves()
2367:     holder = SessionHolder(backend, remote_name, label, timeout, replace)
2368:     # The state is this serve's from here, stamped with its attempt id; every
2369:     # write this serve makes afterwards is conditional on still owning it
2370:     # (write_owned, G-C-02).
2371:     reset_state(status="starting", backend=backend, attempt=holder.attempt)
2372: 
2373:     # SIGTERM is how `cancel` and the next serve end this one
2374:     # (stop_other_serves). With no handler Python died on it at once: the
2375:     # teardown below never ran, and the fullscreen window -- a plain child
2376:     # with no death signal -- stayed on the screen with the gamepad bridge
2377:     # gone, nothing left on the device to drive it or close it (audit #307
2378:     # PL-049). Raising here unwinds through the finally instead; a second
2379:     # SIGTERM while the teardown runs is ignored so that it finishes.
2380:     def on_term(signum, frame):
2381:         signal.signal(signal.SIGTERM, signal.SIG_IGN)
2382:         raise SystemExit(128 + signum)
2383:     signal.signal(signal.SIGTERM, on_term)
2384: 
2385:     try:
2386:         return serve_with(holder, backend, port, timeout)
2387:     finally:
2388:         holder.end()
2389: 
2390: 
2391: def serve_with(holder, backend, port, timeout):
2392:     ok, error = holder.start()
2393:     if not ok:
2394:         sys.stderr.write("%s\n" % error)
2395:         write_owned(holder.attempt, status="failed", error=error)
2396:         return 2
2397: 
2398:     address = lan_address()
2399:     # Listen on the address the page is served at, not on every interface
2400:     # (#308 claude F-RS-18). A VPN or tethering interface no longer takes
2401:     # the keyboard; and the port is shared with the offline achievements
2402:     # proxy, which listens on 127.0.0.1:8080 -- a wildcard bind cannot share
2403:     # a port with a socket on a specific address, so with offline
2404:     # achievements on, every sign-in ended in EADDRINUSE. 127.0.0.1 is
2405:     # lan_address's answer when there is no route, and it is bound as it is:
2406:     # the wildcard it used to keep for that case listened on every
2407:     # interface while advertising loopback, which no phone can reach anyway
2408:     # (the audit of stream C, G-C-06). With no route there is no provider to
2409:     # sign in to either.
2410:     listen = address
2411:     # A port something else holds used to end the serve with a traceback and
2412:     # the status left at "starting", rclone's authorize still running, and
2413:     # the interface waiting on a sign-in that could never be reached (audit
2414:     # #307 PL-050, claude F-RS-22).
2415:     server = None
2416: 
2417:     def shutdown():
2418:         if server is not None:
2419:             threading.Thread(target=server.shutdown, daemon=True).start()
2420: 
2421:     try:
2422:         server = make_server(listen, port, holder, shutdown)
2423:     except OSError as exc:
2424:         why = "port %d is already in use on this device" % port \
2425:             if exc.errno == errno.EADDRINUSE else "could not listen on port %d" % port
2426:         log("sign-in could not start: %s (%s)" % (why, exc.strerror or exc))
2427:         sys.stderr.write("%s\n" % why)
2428:         # The port and the errno stay in the log; the state carries words
2429:         # (G-C-03, the audit of stream C).
2430:         write_owned(holder.attempt, status="failed",
2431:                     error="Something else on this handheld is using the "
2432:                           "sign-in's connection. Restart it and try again.")
2433:         return 2
2434: 
2435:     bare = "http://%s:%d" % (address, port)
2436:     url = "%s/%s" % (bare, holder.pin)
2437:     # Waiting only from starting, and only while this session is the one
2438:     # the state names. Authorize can print its link and die at once; its
2439:     # collector records failed while this was still binding, and this write
2440:     # used to put waiting over it -- a dead attempt republished, the
2441:     # handheld reading STILL WAITING until the serve's timeout (PL-032, gpt
2442:     # G2-C-02). What the state says then stands, and the serve ends.
2443:     if not write_owned(holder.attempt, owner=holder.session.gen,
2444:                        from_status=("starting",), status="waiting",
2445:                        backend=backend, url=url, address=bare,
2446:                        provider=holder.session.provider, pin=holder.pin,
2447:                        name=holder.name):
2448:         log("the sign-in ended before it could be offered")
2449:         server.server_close()
2450:         return 2
2451: 
2452:     # The window is not opened here. It covers the screen the moment it
2453:     # appears, and the address and QR the handheld is showing are how
2454:     # somebody gets a phone keyboard onto it -- opening it immediately means
2455:     # that screen flashes past before it can be read or scanned. The handheld
2456:     # asks for it when the player is ready.
2457:     #
2458:     # Best effort throughout: an image without the browser stack falls
2459:     # through to the paste flow rather than failing the sign-in, and the page
2460:     # says which one you are looking at.
2461:     def open_when_asked():
2462:         # Loops rather than opening once: pressing Start closes the window
2463:         # and gives the handheld back, and the player may well want it again
2464:         # -- to correct an address, or because they closed it by accident.
2465:         flag = state_path("open-browser")
2466:         shut = state_path("close-browser")
2467:         deadline = time.time() + timeout
2468:         while time.time() < deadline:
2469:             if os.path.exists(shut):
2470:                 try:
2471:                     os.unlink(shut)
2472:                 except OSError:
2473:                     pass
2474:                 holder.stop_browser()
2475:             if os.path.exists(flag):
2476:                 try:
2477:                     os.unlink(flag)
2478:                 except OSError:
2479:                     pass
2480:                 if holder.start_browser():
2481:                     log("sign-in window opened for %s" % backend)
2482:             time.sleep(0.4)
2483: 
2484:     if browser_stack_available():
2485:         threading.Thread(target=open_when_asked, daemon=True).start()
2486: 
2487:     # stdout is the contract for the caller (the ES page reads these).
2488:     print("URL=%s" % url)
2489:     print("ADDRESS=%s" % bare)
2490:     print("PIN=%s" % holder.pin)
2491:     print("NAME=%s" % holder.name)
2492:     print("PROVIDER=%s" % holder.session.provider)
2493:     print("EXIT_HINT=%s" % exit_hint())
2494:     sys.stdout.flush()
2495: 
2496:     # The listener is only open while someone is actually signing in.
2497:     timer = threading.Timer(timeout, shutdown)
2498:     timer.daemon = True
2499:     timer.start()
2500:     try:
2501:         server.serve_forever()
2502:     finally:
2503:         timer.cancel()
2504:         server.server_close()
2505: 
2506:     # One write, checked under the lock: failed only from starting or
2507:     # waiting, so a sign-in that lands between a read and the write is not
2508:     # turned back (PL-032).
2509:     if write_owned(holder.attempt, from_status=("starting", "waiting"),
2510:                    status="failed", error="sign-in did not complete"):
2511:         return 1
2512:     return 0 if read_state().get("status") == "signed-in" else 1
2513: 
2514: 
2515: def main(argv):
2516:     if len(argv) < 2:
2517:         sys.stderr.write(
2518:             "usage: cloud_oauth serve <backend> [--name NAME] "
2519:             "[--label 'Dropbox'] [--port N] [--timeout SECONDS]\n"
2520:             "       cloud_oauth url | info | status | open [--phone] "
2521:             "| wait | close | cancel\n")
2522:         return 1
2523: 
2524:     command = argv[1]
2525: 
2526:     if command == "serve":
2527:         if len(argv) < 3:
2528:             return main([argv[0]])
2529:         backend = argv[2]
2530:         name, label, port, timeout = None, None, 8080, 600
2531:         rest = argv[3:]
2532:         for i, arg in enumerate(rest):
2533:             if arg == "--name" and i + 1 < len(rest):
2534:                 name = rest[i + 1]
2535:             elif arg == "--label" and i + 1 < len(rest):
2536:                 label = rest[i + 1]
2537:             elif arg == "--port" and i + 1 < len(rest):
2538:                 port = int(rest[i + 1])
2539:             elif arg == "--timeout" and i + 1 < len(rest):
2540:                 timeout = int(rest[i + 1])
2541:         return cmd_serve(backend, name, label, port, timeout, "--replace" in rest)
2542: 
2543:     if command == "url":
2544:         print(read_state().get("url", ""))
2545:         return 0
2546: 
2547:     if command == "open":
2548:         # Asked for by the handheld once the player has had a chance to read
2549:         # the address and scan the code.
2550:         os.makedirs(STATE_DIR, exist_ok=True)
2551: 
2552:         # Which keyboard the player chose. Raising the on-screen one for
2553:         # somebody who asked to type on their phone covers the form they are
2554:         # reading with a keyboard they did not ask for.
2555:         marker = state_path("phone-keyboard")
2556:         if "--phone" in argv:
2557:             open(marker, "w").close()
2558:         elif os.path.exists(marker):
2559:             try:
2560:                 os.unlink(marker)
2561:             except OSError:
2562:                 pass
2563: 
2564:         open(state_path("open-browser"), "w").close()
2565: 
2566:         # Return once the window is actually up, not once the request is
2567:         # filed. The caller's next act is to tear down its own renderer, and
2568:         # doing that before there is anything to look at leaves the player
2569:         # staring at the wallpaper for the seconds WebKit takes to start.
2570:         deadline = time.time() + 20
2571:         while time.time() < deadline:
2572:             if signin_window_running():
2573:                 return 0
2574:             time.sleep(0.2)
2575:         log("sign-in window did not appear")
2576:         return 1
2577: 
2578:     if command == "wait":
2579:         # Block until the page is finished with, so a caller can bracket this
2580:         # with its own suspend/resume. Bounded well past the session timeout
2581:         # so a serve that died without tidying up cannot strand the caller.
2582:         deadline = time.time() + 1800
2583:         while time.time() < deadline and signin_window_running():
2584:             # A finished sign-in releases the caller without waiting for the
2585:             # window: it stays up saying so while the caller rebuilds itself,
2586:             # and asks for it to be closed afterwards. Waiting for the window
2587:             # to go first is what produced a black screen. Not without the
2588:             # pad, though -- the settle below runs on this path too (PL-018).
2589:             if os.path.exists(state_path("signed-in")):
2590:                 break
2591:             time.sleep(0.3)
2592: 
2593:         # And not a moment before the pad is handed back -- see pad_is_free.
2594:         settle = time.time() + 5
2595:         while time.time() < settle and not pad_is_free():
2596:             time.sleep(0.1)
2597:         return 0
2598: 
2599:     if command == "close":
2600:         # Asked for once the caller is drawing again, so there is something
2601:         # behind the window when it goes.
2602:         os.makedirs(STATE_DIR, exist_ok=True)
2603:         open(state_path("close-browser"), "w").close()
2604:         deadline = time.time() + 10
2605:         while time.time() < deadline and signin_window_running():
2606:             time.sleep(0.2)
2607: 
2608:         # The serve process is what normally takes the window away, and it may
2609:         # not be there to do it -- it times out on its own, and a sign-in that
2610:         # finished near that deadline leaves the window with nobody to close
2611:         # it. That is a fullscreen page reading "Finishing up" sitting on top
2612:         # of an EmulationStation that has already come back, escapable only by
2613:         # a button combination. Close it here rather than depending on
2614:         # somebody else being alive.
2615:         if signin_window_running():
2616:             log("sign-in window outlived its server; closing it directly")
2617:             for signum in (signal.SIGTERM, signal.SIGKILL):
2618:                 for entry in os.listdir("/proc"):
2619:                     if not entry.isdigit():
2620:                         continue
2621:                     try:
2622:                         with open("/proc/%s/cmdline" % entry, "rb") as handle:
2623:                             argv = handle.read().split(b"\0")
2624:                     except OSError:
2625:                         continue
2626:                     if argv and argv[0].decode("utf-8", "replace") == SIGNIN_WINDOW:
2627:                         try:
2628:                             os.kill(int(entry), signum)
2629:                         except OSError:
2630:                             pass
2631:                 for _ in range(15):
2632:                     if not signin_window_running():
2633:                         break
2634:                     time.sleep(0.2)
2635:                 if not signin_window_running():
2636:                     break
2637:             # The serve that set the pointer's hide timeout to never is not
2638:             # there to set it back (#308 claude F-RS-19).
2639:             BrowserSession._cursor_timeout(1000)
2640: 
2641:         settle = time.time() + 5
2642:         while time.time() < settle and not pad_is_free():
2643:             time.sleep(0.1)
2644:         # Honest about the outcome: a window still standing means the screen
2645:         # is not handed back, whatever the caller does next.
2646:         return 0 if not signin_window_running() else 1
2647: 
2648:     if command == "info":
2649:         # One KEY=VALUE per line. `url` stays exactly as it was: the ES page
2650:         # reads whichever of the two the running image provides, so an older
2651:         # script and a newer page still agree on something.
2652:         state = read_state()
2653:         state["on_device"] = "yes" if browser_stack_available() else "no"
2654:         # The window's own words for the way back (exit_hint): Select and
2655:         # Start, which every handheld we ship for has and labels.
2656:         state["exit_hint"] = exit_hint()
2657:         for key in ("url", "address", "pin", "name", "provider", "status",
2658:                     "on_device", "exit_hint"):
2659:             print("%s=%s" % (key.upper(), state.get(key, "")))
2660:         return 0
2661: 
2662:     if command == "status":
2663:         print(read_state().get("status", "idle"))
2664:         return 0
2665: 
2666:     if command == "cancel":
2667:         stop_other_serves()
2668:         subprocess.run(["pkill", "-f", "rclone authorize"], capture_output=True)
2669:         # Clears the address, PIN and provider link as well as the status --
2670:         # a dead session's details are not something to leave lying in
2671:         # /var/run for the next page to pick up and display.
2672:         reset_state(status="idle")
2673:         return 0
2674: 
2675:     return main([argv[0]])
2676: 
2677: 
2678: if __name__ == "__main__":
2679:     sys.exit(main(sys.argv))



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_remote


## Original lines 1–341
1: #!/usr/bin/env python3
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_remote - configure rclone remotes without rclone's interactive TUI.
6: #
7: # `rclone config` asks its questions in a terminal, which on a handheld means
8: # an SSH session from another computer. That flow fails in ways the player
9: # cannot act on: rclone's own prompt tells them to answer N at "Use auto
10: # config?" (correct advice for a headless machine, fatal here), the auth link
11: # only exists in terminal scrollback, and the whole thing needs a machine that
12: # can reach the handheld over the LAN. See fork issue #51.
13: #
14: # rclone supports being configured programmatically -- `rclone config create`
15: # writes a remote non-interactively, and every OAuth backend accepts a finished
16: # token as a plain config value. So we ask the questions ourselves, in a UI the
17: # player already has in their hands, and hand rclone the answers.
18: #
19: # Commands (all output is machine-readable, for the ES front end):
20: #   providers            TSV: tier, name, label
21: #   subproviders <type>  TSV: value, label -- the sub-provider choice a few
22: #                        backends make before their other options mean anything
23: #   fields <type> [prov] TSV: name, required, password, sensitive, type,
24: #                        default, help, choices -- filtered to the options
25: #                        that apply to sub-provider `prov`. `choices` is how
26: #                        many suggested values the option has, so the caller
27: #                        can pick an input widget without fetching them.
28: #   choices <type> <field> [prov]  TSV: value, label
29: #   create <name> <type> [key=value ...]    create, verify, roll back on failure
30: #   update <name> <type> [key=value ...]  verify and replace saved settings
31: #   active               selected name with trailing colon; empty is failure
32: #   select/remove <name> change local selection or remove local credentials
33: #   list                 STATE line, then TSV: name, type, active/saved, provider
34: #
35: # Tiers:
36: #   keys      no OAuth at all - a form is enough
37: #   oauth     needs a provider sign-in, which cloud_oauth handles on-device
38: #   plumbing  not a storage provider at all - see NOT_PROVIDERS
39: #
40: # Exit codes: 0 ok, 1 usage/arguments, 2 rclone failed, 3 verification failed.
41: 
42: import json
43: import os
44: import subprocess
45: import sys
46: import cloud_connections as connections
47: 
48: RCLONE = "/usr/bin/rclone"
49: LOG_FILE = "/var/log/cloud_sync.log"
50: 
51: # Every OAuth backend goes through cloud_oauth, which wraps rclone's own
52: # `authorize` rather than reimplementing any provider's flow, so nothing here
53: # is per-provider: the "oauth" tier is whatever rclone can authorize. (A
54: # DRIVABLE_OAUTH constant and a table of device-flow and PKCE-paste backends
55: # described a design that was not built; nothing read them, and they went in
56: # #308, claude F-RS-14.) That a provider's authorize link resolves to the
57: # provider was probed for dropbox, drive, onedrive, box, pcloud and yandex;
58: # that its sign-in completes on the device is proved per provider.
59: 
60: # rclone's backend list is not a list of cloud services. These wrap or
61: # transform another remote, or are not remote at all, and offering them as
62: # "where your saves go" ranges from meaningless to harmful: `local` would
63: # have someone back their saves up onto the same storage the saves are on,
64: # which is not a backup and only looks like one.
65: NOT_PROVIDERS = {
66:     "alias", "cache", "chunker", "combine", "compress", "crypt", "hasher",
67:     "local", "memory", "union",
68: }
69: 
70: 
71: def log(message):
72:     """Append to the shared cloud-sync log, matching the other tools' format."""
73:     import datetime
74:     stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
75:     try:
76:         with open(LOG_FILE, "a") as handle:
77:             handle.write("[%s] [INFO] [cloud_remote] %s\n" % (stamp, message))
78:     except OSError:
79:         # A full or read-only /var/log must not take the setup flow down.
80:         pass
81: 
82: 
83: def rclone(*args, check=True):
84:     """Run rclone and return (exit code, stdout, stderr)."""
85:     proc = subprocess.run(
86:         [RCLONE] + list(args),
87:         capture_output=True, text=True,
88:     )
89:     if check and proc.returncode != 0:
90:         # The verb and the exit code -- never the arguments, never rclone's
91:         # words. `config create` carries every key=value the player typed,
92:         # passwords among them, and this line put them in cloud_sync.log in
93:         # the clear whenever a create failed (audit #307, gpt F-RS-04: the
94:         # finding the audit refuted for cloud_oauth holds here).
95:         verb = " ".join(args[:2]) if args[:1] == ("config",) else (args[0] if args else "")
96:         log("rclone %s failed (%d)" % (verb, proc.returncode))
97:     return proc.returncode, proc.stdout, proc.stderr
98: 
99: 
100: def load_providers():
101:     """rclone's own backend catalogue, as a list of dicts."""
102:     code, out, err = rclone("config", "providers")
103:     if code != 0:
104:         sys.stderr.write("could not read rclone's provider list\n")
105:         sys.exit(2)
106:     try:
107:         return json.loads(out)
108:     except json.JSONDecodeError as exc:
109:         sys.stderr.write("rclone's provider list was not valid JSON: %s\n" % exc)
110:         sys.exit(2)
111: 
112: 
113: def tier_of(provider):
114:     """Which setup path this backend can use."""
115:     if provider.get("Name") in NOT_PROVIDERS:
116:         return "plumbing"
117:     names = {opt.get("Name") for opt in provider.get("Options") or []}
118:     if "token" not in names:
119:         return "keys"
120:     return "oauth"
121: 
122: 
123: def option_applies(opt, subprovider):
124:     """Is this option relevant once `subprovider` has been chosen?
125: 
126:     Several backends gate their options on a sub-provider: koofr carries
127:     three separate options all named `password`, one each for Koofr,
128:     Digi Storage and "other", and only one of them is ever real. S3 goes
129:     further, with 51 sub-providers and options like ibm_api_key that mean
130:     nothing unless you picked IBMCOS. Rendering them all gives duplicate
131:     fields and questions about vendors the player is not using.
132:     """
133:     constraint = (opt.get("Provider") or "").strip()
134:     if not constraint:
135:         return True
136:     if constraint.startswith("!"):
137:         excluded = {p.strip() for p in constraint[1:].split(",") if p.strip()}
138:         return subprovider not in excluded
139:     allowed = {p.strip() for p in constraint.split(",") if p.strip()}
140:     return subprovider in allowed
141: 
142: 
143: def cmd_subproviders(backend_type):
144:     """The sub-provider choice, where a backend has one."""
145:     for provider in load_providers():
146:         if provider.get("Name") != backend_type:
147:             continue
148:         for opt in provider.get("Options") or []:
149:             if opt.get("Name") != "provider":
150:                 continue
151:             for example in opt.get("Examples") or []:
152:                 help_text = (example.get("Help") or "").splitlines()
153:                 print("%s\t%s" % (
154:                     example.get("Value") or "",
155:                     help_text[0] if help_text else (example.get("Value") or ""),
156:                 ))
157:             return 0
158:         return 0
159:     sys.stderr.write("unknown backend type: %s\n" % backend_type)
160:     return 1
161: 
162: 
163: def cmd_providers():
164:     """Every backend with the setup path it can use. Sorted for a stable UI."""
165:     rows = []
166:     for provider in load_providers():
167:         name = provider.get("Name") or ""
168:         label = (provider.get("Description") or name).splitlines()[0]
169:         rows.append((tier_of(provider), name, label))
170:     for tier, name, label in sorted(rows, key=lambda r: (r[0], r[1])):
171:         print("%s\t%s\t%s" % (tier, name, label))
172:     return 0
173: 
174: 
175: def cmd_fields(backend_type, subprovider=""):
176:     """The options a player actually has to answer for one backend.
177: 
178:     rclone exposes every knob a backend has, most of which are advanced
179:     tuning nobody should meet during setup. Show the non-advanced ones, and
180:     let the caller decide how to render required vs optional.
181:     """
182:     for provider in load_providers():
183:         if provider.get("Name") != backend_type:
184:             continue
185:         for opt in provider.get("Options") or []:
186:             if opt.get("Advanced") or opt.get("Hide"):
187:                 continue
188:             # The sub-provider choice itself is made on its own screen.
189:             if opt.get("Name") == "provider":
190:                 continue
191:             if not option_applies(opt, subprovider):
192:                 continue
193:             # These are two different things and must not be collapsed.
194:             # IsPassword means the value is a credential: mask the input and
195:             # let rclone obscure it on the way in. Sensitive only means "do
196:             # not echo this into logs" -- rclone marks sftp's host and user
197:             # that way, and password-masking a hostname would leave the
198:             # player unable to see what they typed.
199:             help_text = (opt.get("Help") or "").splitlines()
200:             print("%s\t%d\t%d\t%d\t%s\t%s\t%s\t%d" % (
201:                 opt.get("Name") or "",
202:                 1 if opt.get("Required") else 0,
203:                 1 if opt.get("IsPassword") else 0,
204:                 1 if opt.get("Sensitive") else 0,
205:                 opt.get("Type") or "string",
206:                 opt.get("DefaultStr") or "",
207:                 help_text[0] if help_text else "",
208:                 len(opt.get("Examples") or []),
209:             ))
210:         return 0
211:     sys.stderr.write("unknown backend type: %s\n" % backend_type)
212:     return 1
213: 
214: 
215: def cmd_choices(backend_type, field, subprovider=""):
216:     """The suggested values for one option.
217: 
218:     rclone marks none of these Exclusive, so they are suggestions rather than
219:     a closed set -- but for something like webdav's `vendor` the player has
220:     no way to guess "other", so offering the list is the difference between
221:     a form they can fill in and one they cannot.
222:     """
223:     for provider in load_providers():
224:         if provider.get("Name") != backend_type:
225:             continue
226:         for opt in provider.get("Options") or []:
227:             if opt.get("Name") != field:
228:                 continue
229:             if not option_applies(opt, subprovider):
230:                 continue
231:             for example in opt.get("Examples") or []:
232:                 help_text = (example.get("Help") or "").splitlines()
233:                 value = example.get("Value")
234:                 if value is None:
235:                     continue
236:                 label = help_text[0] if help_text else str(value)
237:                 print("%s\t%s" % (value, label))
238:             return 0
239:         return 0
240:     sys.stderr.write("unknown backend type: %s\n" % backend_type)
241:     return 1
242: 
243: 
244: def cmd_list():
245:     _, config = connections.read_config()
246:     try:
247:         selected = connections.active(config)
248:     except connections.Refused:
249:         selected = ""
250:     print("STATE=" + ("active" if selected else "unselected"))
251:     for name in sorted(config.sections()):
252:         print("%s\t%s\t%s\t%s" % (name, config.get(name, "type", fallback=""),
253:                                     "active" if name == selected else "saved", config.get(name, "provider", fallback="")))
254:     return 0
255: 
256: 
257: def cmd_create(name, backend_type, settings, replace=False):
258:     providers = load_providers()
259:     if backend_type not in {p.get("Name") for p in providers}:
260:         raise connections.Refused("Unknown provider.")
261:     if not replace and backend_type in ("s3", "gcs", "azureblob") and not any(k == "directory_markers" for k, _ in settings):
262:         settings.append(("directory_markers", "true"))
263:     log("updating remote " + name if replace else "creating remote " + name)
264:     connections.save(name, backend_type, settings, replace=replace)
265:     print("OK=%s" % name)
266:     return 0
267: 
268: 
269: def usage():
270:     sys.stderr.write(
271:         "usage: cloud_remote providers\n"
272:         "       cloud_remote subproviders <type>\n"
273:         "       cloud_remote fields <type> [subprovider]\n"
274:         "       cloud_remote choices <type> <field> [subprovider]\n"
275:         "       cloud_remote create <name> <type> [key=value ...]\n"
276:         "       cloud_remote update <name> <type> [key=value ...]\n"
277:         "       cloud_remote active\n"
278:         "       cloud_remote select|remove <name>\n"
279:         "       cloud_remote list\n")
280:     return 1
281: 
282: 
283: def main(argv):
284:     if len(argv) < 2:
285:         return usage()
286:     command = argv[1]
287: 
288:     if command == "providers":
289:         return cmd_providers()
290: 
291:     if command == "subproviders":
292:         if len(argv) != 3:
293:             return usage()
294:         return cmd_subproviders(argv[2])
295: 
296:     if command == "choices":
297:         if len(argv) not in (4, 5):
298:             return usage()
299:         return cmd_choices(argv[2], argv[3], argv[4] if len(argv) == 5 else "")
300: 
301:     if command == "fields":
302:         if len(argv) not in (3, 4):
303:             return usage()
304:         return cmd_fields(argv[2], argv[3] if len(argv) == 4 else "")
305: 
306:     if command == "list":
307:         return cmd_list()
308: 
309:     if command == "active":
310:         name = connections.active()
311:         if name:
312:             print(name + ":")
313:             return 0
314:         return 1
315: 
316:     if command in ("select", "remove") and len(argv) == 3:
317:         (connections.select if command == "select" else connections.remove)(argv[2])
318:         print("OK=" + argv[2])
319:         return 0
320: 
321:     if command in ("create", "update"):
322:         if len(argv) < 4:
323:             return usage()
324:         settings = []
325:         for pair in argv[4:]:
326:             if "=" not in pair:
327:                 sys.stderr.write("expected key=value, got: %s\n" % pair)
328:                 return 1
329:             key, value = pair.split("=", 1)
330:             settings.append((key, value))
331:         return cmd_create(argv[2], argv[3], settings, replace=(command == "update"))
332: 
333:     return usage()
334: 
335: 
336: if __name__ == "__main__":
337:     try:
338:         sys.exit(main(sys.argv))
339:     except (connections.Refused, OSError) as exc:
340:         sys.stderr.write(str(exc) + "\n" if isinstance(exc, connections.Refused) else "Cloud settings could not be read or saved.\n")
341:         sys.exit(2)



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_restore


## Original lines 415–475
415: # for.
416: #
417: # The lock lives here, in the script, so no caller has to know about the
418: # others. /var/run is tmpfs, so a lock cannot survive a reboot and go stale.
419: # Non-blocking, because a request that queues silently behind a twenty-minute
420: # transfer looks exactly like one that hung. Exit EXIT_LOCK_HELD (75) means
421: # "skipped: another sync is running" -- the UI names it, and no last-run stamp
422: # is written for work that did not happen.
423: #
424: # The descriptor is this shell's and nothing else's. A shell redirection
425: # carries no close-on-exec, so `exec 9>` hands fd 9 to every child the
426: # script starts, and rclone then holds the lock for the whole of a transfer
427: # (watched in /proc on the VM, #124). While the script outlives its
428: # children that is invisible, because bash waits for each of them before it
429: # exits. The moment it does not -- killed or orphaned while rclone is still
430: # copying, a child left in the background -- the lock outlives the run that
431: # took it and every sync afterwards is refused with "another cloud sync is
432: # running" when nothing is running at all. So the body runs with fd 9
433: # closed ("9>&-"): bash keeps the lock on a descriptor of its own, which it
434: # does mark close-on-exec, and nothing this script starts can see it.
435: #
436: # The refusal also waits a moment before saying no, as belt and braces for
437: # a holder this script does not own: a descriptor leaked by an older build,
438: # or a process in the act of exiting, frees itself in milliseconds, while a
439: # real concurrent transfer does not. One second of patience turns a raced
440: # skip into a run that works and costs a genuinely blocked run one second.
441: CLOUD_SYNC_LOCK=/var/run/cloud_sync.lock
442: take_cloud_lock() {
443:     local tries=0
444:     exec 9>"${CLOUD_SYNC_LOCK}"
445:     while ! flock -n 9; do
446:         if [ "${tries}" -ge 4 ]; then
447:             echo "Skipped: another cloud sync is already running. Try again when it's done."
448:             log_message "skipped: another cloud sync holds ${CLOUD_SYNC_LOCK}" "false"
449:             exit "${EXIT_LOCK_HELD}"
450:         fi
451:         tries=$((tries + 1))
452:         sleep 0.25
453:     done
454: }
455: 
456: # Exit EXIT_NO_NETWORK (69) means "skipped: no network". Answered locally,
457: # before any remote probe: with no default route there is nothing to restore
458: # from, and nobody should wait for rclone to time out learning that. `ip
459: # route` reads the kernel's table and sends nothing. The same test, the same
460: # code and the same "no stamp, nothing ran" as cloud_backup's; until
461: # 2026-09-09 this script had no such step and an offline restore reached
462: # check_internet, which exited 1 -- FAILED on the card, for a device that
463: # was simply not connected.
464: has_default_route() {
465:     ip -4 route show default 2>/dev/null | grep -q . \
466:         || ip -6 route show default 2>/dev/null | grep -q .
467: }
468: 
469: check_network_link() {
470:     if ! has_default_route; then
471:         echo "Skipped: there's no network connection. Try again when you're online."
472:         log_message "skipped: no default route, nothing to restore from" "false"
473:         exit "${EXIT_NO_NETWORK}"
474:     fi
475: }

## Original lines 2190–2260
2190:         
2191:         return $RESTORE_SYSTEM_STATUS
2192:     else
2193:         log_message "Restoring settings from the cloud is turned off, so it was skipped." "true"
2194:         RESTORE_SYSTEM_STATUS=0
2195:     fi
2196:     
2197:     return $RESTORE_SYSTEM_STATUS
2198: }
2199: 
2200: # Main script execution
2201: # The follow check that ran here before every sync (D-CLOUD-160's "your
2202: # other devices will follow") is the cloud folder step's now, which runs
2203: # where the player first meets the cloud -- the end of cloud setup, and the
2204: # first boot of this build on a device linked to an earlier folder -- and on
2205: # the transfer pages' scan (D-CLOUD-170, #363). Every sync paid for it before.
2206: 
2207: main() {
2208:     check_network_link
2209:     check_rclone_config
2210:     load_config
2211:     # restore_game_saves proves the remote reachable with the listing it
2212:     # needs anyway, and network_lost_during_run words a failure there; only
2213:     # the settings-only path has no such step of its own -- cloud_backup's
2214:     # shape (#308 claude F-CS-04), one remote round trip fewer per run. After
2215:     # load_config, which sets an automatic run's deadline (#308 gpt F-CS-34).
2216:     # An existing config file can contain no remote (#392). Without the
2217:     # prefix, rclone interprets SAVES_REMOTE as a local path. Refuse before
2218:     # any path operation instead of treating local files as cloud storage.
2219:     REMOTENAME=$(first_remote)
2220:     case "${REMOTENAME}" in
2221:         ?*:) ;;
2222:         *) log_message "Your cloud storage isn't set up yet. Set it up under GAME SETTINGS > MANAGE CLOUD STORAGE first." "true" "ERROR"
2223:            say_why "YOUR CLOUD STORAGE ISN'T SET UP YET"
2224:            clean_exit 1 ;;
2225:     esac
2226:     [ "${SYSTEM_ONLY}" -eq 1 ] && check_internet
2227:     
2228:     # Begin main script operations with user-friendly header
2229:     log_message "=> ${OS_NAME} CLOUD RESTORE\n"
2230:     
2231:     # Execute Part 1: Game saves restore
2232:     # This performs the primary save file restoration operation using the configured method
2233:     # --system-only was parsed and then ignored here, so it restored game saves
2234:     # anyway -- the opposite of what it says, over the top of local saves.
2235:     if [ "${SYSTEM_ONLY}" -eq 1 ]; then
2236:         log_message "Skipped game saves this time - settings only." "true"
2237:         SAVES_OUTCOME="SKIPPED - SETTINGS ONLY"
2238:         RESTORE_STATUS=0
2239:     else
2240:         restore_game_saves
2241:         RESTORE_STATUS=$?
2242:     fi
2243:     
2244:     # Add a pause for better visual separation between operations
2245:     pause 2
2246:     
2247:     # Execute Part 2: System restore
2248:     # This restores settings backup files (zip files) if enabled in configuration
2249:     if [ "${SAVES_ONLY}" -eq 1 ]; then
2250:         log_message "Skipped settings this time - saves only." "true"
2251:         SETTINGS_OUTCOME="SKIPPED - SAVES ONLY"
2252:         RESTORE_SYSTEM_STATUS=0
2253:     else
2254:         restore_system_files
2255:         RESTORE_SYSTEM_STATUS=$?
2256:     fi
2257:     
2258:     # Create empty missing system directories if removed during restore
2259:     # Only necessary when using sync method which can delete files
2260:     if [ "${RESTOREMETHOD}" == "sync" ]; then



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_scan


## Original lines 1–359
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present rasteratops (https://github.com/rasteratops)
4: 
5: # cloud_scan - what the cloud holds for this device, before anything is offered.
6: #
7: # The transfer pages scan first and offer only what the scan found
8: # (D-CLOUD-156, fork #350): the folder's state, the settings archives by
9: # device label, where the content is, and -- once the player has ticked
10: # what to move -- the content listing in those classes. This runs those
11: # reads and talks to the scan page in the protocol every cloud page reads
12: # (">>> unit", ">>> doing", ">>> why"), writing each result to a file the
13: # options page builds from.
14: #
15: #   cloud_scan                   the opening scan: the folder, the settings
16: #                                archives, where the content is (three items)
17: #   cloud_scan --content [--with-media|--media-only]
18: #                                the content listing for the systems page,
19: #                                in the classes ticked (one item)
20: #   cloud_scan --folder          configured folder availability (one item)
21: #
22: # Read-only: scans never adopt another device's folders, rewrite settings,
23: # move files, or offer migration. Folder changes use explicit setup choices.
24: #
25: # Results, under /storage/.cache/cloud_sync/scan/:
26: #   state             cloud_setup --folder-state, one fact per line
27: #   archives          every settings archive in the Backups folder, one per line
28: #   settings          LABEL= (this device's), MINE= (its newest), NEWEST= (overall), COUNT=
29: #   content-location  cloud_setup --content-location, key=value
30: #   done              JSON binding the opening result to its run/configuration
31: #   scan              cloud_content_restore --scan's rows        (--content)
32: #   systems           the systems this device syncs (--systems)  (--content)
33: #   content-done      equivalent binding for the selected content mode
34: #
35: # Exit: 0 all read; 69 no network (the page says SKIPPED - YOU'RE NOT
36: # ONLINE); 1 no cloud storage set up; otherwise the failing read's code,
37: # with a ">>> why" in the player's words before it (D-UI-028).
38: 
39: . /etc/profile 2>/dev/null
40: 
41: OUT=/storage/.cache/cloud_sync/scan
42: SYNC_CONF=/storage/.config/cloud_sync.conf
43: readonly EXIT_NO_NETWORK=69
44: # Every listing here is bounded as the other readers' are (#308 claude F-RS-13).
45: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
46: 
47: say() { echo "$@"; }
48: log() { logger -t cloud_scan "$*" 2>/dev/null; }
49: why() { echo ">>> why $*"; }
50: 
51: # The shared reader (cloud_setup's, the content scripts', D-CLOUD-149): a
52: # value in a form the sync does not read is nothing here, never a folder.
53: conf_get() { # <KEY> (the content scripts' reader, mirrored so every reader agrees, D-CLOUD-149): its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
54:     [ -f ${SYNC_CONF} ] || return 0
55:     awk -v k="$1" '
56:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
57:         index($0, k "=") != 1 && !other \
58:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
59:         index($0, k "=") == 1 {
60:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
61:             c = substr(s, 1, 1)
62:             if (c == "\"") {
63:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
64:                 # character each (PL-015), and so does this; an unescaped $
65:                 # or backtick is an expansion this reader does not make, and
66:                 # any other backslash is refused as conf_valid refuses it.
67:                 n = length(s); i = 2; closed = 0
68:                 while (i <= n) {
69:                     d = substr(s, i, 1)
70:                     if (d == "\"") { closed = 1; break }
71:                     if (d == "\\") {
72:                         e = substr(s, i + 1, 1)
73:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
74:                         ok = 0
75:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
76:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
77:                         break
78:                     }
79:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
80:                     v = v d; i++
81:                 }
82:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
83:                 if (ok) r = substr(s, i + 1)
84:             } else if (c == "'"'"'") {
85:                 j = index(substr(s, 2), c)
86:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
87:             } else {
88:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
89:             }
90:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
91:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
92:         }
93:         END {
94:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
95:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
96:             if (found && !firstok) { print firstwhy; exit 2 }
97:             if (found) print first
98:         }
99:     ' ${SYNC_CONF}
100: }
101: 
102: sibling() { # <name>: the script beside this one, else the installed one
103:     local t; t="$(dirname "$(readlink -f "$0")")/$1"
104:     [ -x "${t}" ] || t="/usr/bin/$1"
105:     echo "${t}"
106: }
107: device_label() {
108:     local tool; tool=$(sibling cloud_device_id)
109:     [ -x "${tool}" ] && "${tool}" --label 2>/dev/null | tr -cd 'A-Za-z0-9_-'
110: }
111: os_name() {
112:     local name="${OS_NAME}"
113:     [ -z "${name}" ] && name=$(sed -n 's/^OS_NAME="\{0,1\}\([^"]*\)"\{0,1\}$/\1/p' /etc/os-release 2>/dev/null | head -1)
114:     [ -z "${name}" ] && name="ROCKNIX"
115:     printf '%s\n' "${name}" | tr -cd 'A-Za-z0-9_-'
116: }
117: 
118: # What an rclone exit means to a player: the sentences the card and the
119: # rows already carry for these codes (ThreadedCloudSync::whyForCode), so
120: # one code is never called two things and the French reaches them.
121: why_for_rc() {
122:     case "$1" in
123:         3|4) why "COULDN'T FIND YOUR CLOUD FOLDER" ;;
124:         5|124) why "YOUR CLOUD STOPPED ANSWERING" ;;   # 124: a bounded read timed out
125:         7|8) why "YOUR CLOUD WOULDN'T TAKE THE FILES" ;;
126:         *)   why "SOMETHING WENT WRONG" ;;
127:     esac
128: }
129: 
130: # Before any read: a place to write, a route, a remote.
131: prepare() {
132:     mkdir -p "${OUT}" || { log "scan: cannot make ${OUT}"; why "SOMETHING WENT WRONG"; exit 1; }
133:     # No route, nothing tried: the page says SKIPPED - YOU'RE NOT ONLINE from
134:     # the code alone (D-CLOUD-072, D-CLOUD-112).
135:     if ! ip route show default 2>/dev/null | grep -q .; then
136:         log "scan: no default route; skipped"
137:         exit "${EXIT_NO_NETWORK}"
138:     fi
139:     REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
140:     if [ -z "${REMOTE}" ]; then
141:         why "YOUR CLOUD STORAGE ISN'T SET UP YET"
142:         exit 1
143:     fi
144: }
145: 
146: # A read that failed ends the run with its why; 69 is the page's own sentinel.
147: stop_on() { # <rc> <what> [application output file]
148:     [ "$1" -eq 0 ] && return 0
149:     log "scan: $2 exited $1"
150:     [ "$1" -eq "${EXIT_NO_NETWORK}" ] && exit "$1"
151:     if [ -n "${3:-}" ]; then
152:         local reason
153:         reason=$(sed -n 's/^>>> why //p' "$3" 2>/dev/null | tail -1)
154:         if [ -n "${reason}" ]; then
155:             why "${reason}"
156:         elif [ "$1" -eq 124 ]; then
157:             why "YOUR CLOUD STOPPED ANSWERING"
158:         else
159:             # Application codes are not rclone's codes. A refused layout
160:             # or invalid record does not mean that a folder is missing.
161:             why "YOUR CLOUD FOLDER COULDN'T BE READ"
162:         fi
163:     else
164:         why_for_rc "$1"
165:     fi
166:     exit "$1"
167: }
168: 
169: # Local-only identity: no rclone invocation and no configuration merge. A
170: # changed endpoint, folder, rule or selection invalidates every old result.
171: context_id() {
172:     local file fingerprint="" value
173:     for file in /storage/.config/cloud_sync.conf \
174:                 /storage/.config/rclone/rclone.conf \
175:                 /storage/.config/cloud_sync-rules.txt \
176:                 /storage/.cache/cloud_sync/content-systems \
177:                 /storage/.config/emulationstation/es_systems.cfg \
178:                 /usr/config/emulationstation/es_systems.cfg; do
179:         if [ -f "${file}" ]; then
180:             value=$(sha256sum "${file}") || return 1
181:         elif [ -e "${file}" ]; then
182:             return 1
183:         else
184:             value="absent ${file}"
185:         fi
186:         fingerprint+="${value}"$'\n'
187:     done
188:     printf '%s' "${fingerprint}" | sha256sum | cut -d' ' -f1
189: }
190: result_id() {
191:     local file value fingerprint=""; local -a names
192:     case "$1" in
193:         done) names=(state archives settings content-location) ;;
194:         content-done) names=(scan systems) ;;
195:         *) return 1 ;;
196:     esac
197:     for file in "${names[@]}"; do
198:         [ -f "${OUT}/${file}" ] || return 1
199:         value=$(sha256sum "${OUT}/${file}") || return 1
200:         fingerprint+="${value}"$'\n'
201:     done
202:     printf '%s' "${fingerprint}" | sha256sum | cut -d' ' -f1
203: }
204: content_mode() {
205:     local flag
206:     for flag in "$@"; do
207:         case "${flag}" in --with-media|--media-only) ;; *) return 1 ;; esac
208:     done
209:     case " $* " in
210:         *" --with-media "*" --media-only "*|*" --media-only "*" --with-media "*) return 1 ;;
211:         *" --with-media "*) echo content:all ;;
212:         *" --media-only "*) echo content:media ;;
213:         *) echo content:roms ;;
214:     esac
215: }
216: write_completion() {
217:     local stamp="$1" mode="$2" current digest tmp
218:     current=$(context_id) && [ "${current}" = "${CONFIG_ID}" ] || {
219:         why "YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN"; return 1;
220:     }
221:     digest=$(result_id "${stamp}") || return 1
222:     tmp="${OUT}/${stamp}.tmp.$$"
223:     jq -n --arg run "${RUN_ID}" --arg config "${CONFIG_ID}" \
224:         --arg mode "${mode}" --arg result "${digest}" \
225:         '{schema_version:1,run_id:$run,config_id:$config,mode:$mode,result_id:$result}' > "${tmp}" \
226:         && mv -f "${tmp}" "${OUT}/${stamp}"
227: }
228: if [ "$1" = --context ]; then
229:     [ $# -eq 1 ] || exit 2
230:     context_id; exit $?
231: elif [ "$1" = --stamp-valid ]; then
232:     STAMP="$2"; EXPECTED_RUN="$3"; shift 3 || exit 2
233:     [[ "${EXPECTED_RUN}" =~ ^[A-Za-z0-9_.-]{1,96}$ ]] || exit 2
234:     case "${STAMP}" in
235:         done) [ $# -eq 0 ] || exit 2; MODE=opening ;;
236:         content-done) MODE=$(content_mode "$@") || exit 2 ;;
237:         *) exit 2 ;;
238:     esac
239:     CURRENT=$(context_id) && DIGEST=$(result_id "${STAMP}") || exit 1
240:     jq -e --arg run "${EXPECTED_RUN}" --arg config "${CURRENT}" \
241:         --arg mode "${MODE}" --arg result "${DIGEST}" \
242:         '.schema_version == 1 and .run_id == $run and .config_id == $config and .mode == $mode and .result_id == $result' \
243:         "${OUT}/${STAMP}" >/dev/null 2>&1
244:     exit $?
245: fi
246: RUN_ID=""; ARGS=()
247: while [ $# -gt 0 ]; do
248:     case "$1" in
249:         --run-id) [ -z "${RUN_ID}" ] && [ $# -ge 2 ] || exit 2; RUN_ID="$2"; shift 2 ;;
250:         --content|--folder|--with-media|--media-only) ARGS+=("$1"); shift ;;
251:         *) echo "Unknown scan option" >&2; exit 2 ;;
252:     esac
253: done
254: RUN_ID="${RUN_ID:-$(date +%s)-$$}"
255: [[ "${RUN_ID}" =~ ^[A-Za-z0-9_.-]{1,96}$ ]] || exit 2
256: set -- "${ARGS[@]}"
257: CONFIG_ID=$(context_id) || exit 1
258: 
259: # --content: the listing the systems page is built from, in the classes
260: # the player ticked (cloud_content_restore --scan's own flags), and the
261: # systems this device syncs. One item; the page's row 3 says it is
262: # comparing.
263: scan_content() {
264:     local label="ROMS AND BIOS" rc
265:     case " $* " in
266:         *" --with-media "*) label="ROMS, BIOS, AND GAME CONTENT" ;;
267:         *" --media-only "*) label="GAME CONTENT" ;;
268:     esac
269:     prepare
270:     rm -f "${OUT}"/scan "${OUT}"/scan.err "${OUT}"/systems "${OUT}"/content-done
271:     echo ">>> unit ${label}||"
272:     echo ">>> doing compare"
273:     "$(sibling cloud_content_restore)" --scan "$@" > "${OUT}/scan" 2> "${OUT}/scan.err"; rc=$?
274:     [ "${rc}" -eq 0 ] || log "scan: --scan $* exited ${rc}: $(head -1 "${OUT}/scan.err" 2>/dev/null)"
275:     stop_on "${rc}" "--scan"
276:     "$(sibling cloud_content_restore)" --systems > "${OUT}/systems" 2>/dev/null; rc=$?
277:     stop_on "${rc}" "--systems"
278:     mode=$(content_mode "$@") || exit 2
279:     write_completion content-done "${mode}" || exit 1
280:     log "scan: content done ($(grep -c . "${OUT}/scan") rows, ${label})"
281:     exit 0
282: }
283: 
284: # 1. Availability of the configured saves folder. It is not a reason to
285: # reselect paths: other selected tiers may still hold their own files.
286: read_folder() {
287:     local setup
288:     echo ">>> unit CLOUD FOLDER||"
289:     echo ">>> doing scan"
290:     setup=$(sibling cloud_setup)
291:     "${setup}" --folder-state > "${OUT}/state" 2>/dev/null
292:     stop_on $? "--folder-state" "${OUT}/state"
293: }
294: 
295: scan_main() {
296: case "$1" in
297:     --content) shift; scan_content "$@" ;;
298:     --folder)
299:         # The step reads state alone; the opening scan's other files are
300:         # left as they were, and are rewritten by the next opening scan.
301:         prepare
302:         rm -f "${OUT}"/state "${OUT}"/done
303:         read_folder
304:         log "scan: folder done ($(sed -n 's/^STATE=//p' "${OUT}/state"))"
305:         exit 0 ;;
306:     "") ;;
307:     *) echo "usage: cloud_scan [--content [--with-media|--media-only] | --folder]" >&2; exit 2 ;;
308: esac
309: 
310: prepare
311: rm -f "${OUT}"/state "${OUT}"/archives "${OUT}"/settings "${OUT}"/content-location "${OUT}"/root-dirs "${OUT}"/done
312: date +%s > "${OUT}/started"
313: read_folder
314: 
315: # 2. The settings archives, by the device that wrote each (the label in the
316: #    name, cloud_restore's rule): this device's newest first, else the newest
317: #    overall, else none -- the row is offered or dimmed from this (D-CLOUD-162).
318: echo ">>> unit SETTINGS BACKUPS||"
319: echo ">>> doing scan"
320: settings_remote=$(conf_get SETTINGS_REMOTE) || { why "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"; exit 1; }
321: settings_remote="${settings_remote%/}"
322: # Use the restore reader's directory priority, including inherited device IDs.
323: archive_tool=$(sibling rasteratops-settings-archive)
324: [ -r "${archive_tool}" ] || { why "SOMETHING WENT WRONG"; exit 1; }
325: . "${archive_tool}"
326: select_settings_archives "${REMOTE}${settings_remote}" "$(sibling cloud_device_id)"; rc=$?
327: stop_on "${rc}" "archives listing"
328: listing="${SETTINGS_ARCHIVE_LISTING}"
329: printf '%s\n' "${listing}" | sed '/^$/d' > "${OUT}/archives"
330: label=$(device_label); osn=$(os_name); mine=""; newest=""
331: if [ -n "${label}" ]; then
332:     mine=$(grep -E "^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-${label}-(${osn}|ROCKNIX|RASTERATOPS)_SETTINGS\.tar\.gz$" "${OUT}/archives" | sort | tail -1)
333: fi
334: newest=$(grep -E '^[0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6}-' "${OUT}/archives" | sort | tail -1)
335: {
336:     echo "SOURCE=${SETTINGS_ARCHIVE_SOURCE}"
337:     echo "LABEL=${label}"
338:     echo "MINE=${mine}"
339:     echo "NEWEST=${newest}"
340:     echo "COUNT=$(grep -c . "${OUT}/archives")"
341: } > "${OUT}/settings"
342: 
343: # 3. Availability at the explicitly selected library. Account-root browsing
344: # and discovery of another library are not part of a transfer preview.
345: echo ">>> unit GAME CONTENT||"
346: echo ">>> doing scan"
347: "$(sibling cloud_setup)" --content-location > "${OUT}/content-location" 2>/dev/null; rc=$?
348: stop_on "${rc}" "--content-location" "${OUT}/content-location"
349: 
350: write_completion done opening || exit 1
351: log "scan: done ($(grep -c . "${OUT}/archives") archives, $(sed -n 's/^STATE=//p' "${OUT}/state"), content $(sed -n 's/^STATE=//p' "${OUT}/content-location"))"
352: exit 0
353: 
354: }
355: # The lock protects shared cache files. The function runs with the descriptor
356: # closed; children cannot retain a stale lock after this owner exits.
357: exec 8>/var/run/cloud_scan.lock || exit 1
358: flock -n 8 || { why "ANOTHER CLOUD CHECK IS RUNNING"; exit 75; }
359: scan_main "$@" 8>&-



# FILE distribution/projects/ROCKNIX/packages/network/rclone/sources/cloud_setup


## Original lines 1–967
1: #!/bin/bash
2: # SPDX-License-Identifier: GPL-2.0
3: # Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
4: 
5: # cloud_setup - configure the rclone cloud remote.
6: #
7: # Walks the player through rclone's own interactive configuration over SSH:
8: # it is the only flow that handles every provider completely (OAuth sign-in,
9: # folder choices, provider-specific questions). This screen supplies the
10: # connection details in big text, waits, then verifies the remote actually
11: # works before declaring success.
12: #
13: # The native UI wizard drives the same flow through three flags:
14: #   --info       key=value connection facts (IP, SSH command, override
15: #                state, password, sshd state, OAuth-port state,
16: #                configured remotes)
17: #   --free-auth-port  clear a stale sign-in webserver holding rclone's
18: #                OAuth port 53682
19: #   --set-content-remote <path>  change the content root alone (CONTENT_REMOTE;
20: #                the chooser's, fork #352); nothing moves
21: #   --set-saves-remote <path>  change the cloud folder (SAVES_REMOTE) the sync
22: #                (--set-syncpath is accepted as the older spelling)
23: #                tools use, preserving settings and content choices; refuses a
24: #                path the remote cannot use
25: #   --accept-saves-root  the saves folder is on a different card than the last
26: #                sync and that is intended (cloud_saves_root)
27: #   --check-syncpath [path]  validate a cloud folder against the remote's
28: #                shape without changing anything (default: the current one)
29: #   --folder-state  read configured folder availability; never change pointers
30: #   --validation-context  local config identity and exact selected category paths
31: #   --validate-folders <categories csv> <run-id>  bounded read-only JSON findings
32: #   --seed-folders <categories csv>  create only explicitly selected folders
33: #   --set-settings-remote <path>  change only the settings archive location
34: #   --content-location  report where this device's ROMs/BIOS actually are in
35: #                the selected cloud folder (key=value; STATE=ok|empty;
36: #                unreadable, exit 1, when its value is not in a form the
37: #                sync reads)
38: #   --use-content-root  point content back at the remote root, moving nothing
39: #   --connected  exit 0 when an inbound SSH session is established, so the
40: #                connect step can be verified rather than taken on faith
41: #   --check [remote]  verify a remote (default: first); exit 0 working,
42: #                1 missing, 2 configured but unreachable
43: 
44: . /etc/profile
45: 
46: SCRIPT_NAME=$(basename "$0")
47: LOG_FILE="/var/log/cloud_sync.log"
48: SYNC_CONF="/storage/.config/cloud_sync.conf"
49: 
50: log_message() {
51:     local message="$1"
52:     local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
53:     echo "[${timestamp}] [INFO] [${SCRIPT_NAME}] ${message}" >> ${LOG_FILE}
54: }
55: 
56: # The config is shell: every cloud script sources it. So a value is written
57: # as text between double quotes, never through a sed replacement -- where &
58: # is the matched line and | ends the expression, so "/R&D/Saves" became
59: # garbage and "/a|b" failed the write while OK was printed (audit #307
60: # PL-051) -- and a value that would mean something to a shell between double
61: # quotes (" $ ` \) is refused where it is typed (syncpath_problem).
62: #
63: # conf_set KEY VALUE [KEY VALUE ...] writes every pair in one pass, each
64: # KEY= line replaced (every one, as the sed was) or appended, to a file
65: # beside the config that is renamed over it: all the keys or none, and the
66: # previous config intact when the write fails. The values reach awk through
67: # the environment, so nothing in them is interpreted. Returns non-zero when
68: # the config could not be written.
69: conf_set() {
70:     local tmp="${SYNC_CONF}.tmp.$$" src="${SYNC_CONF}" n=0 i
71:     local -a pairs=() want=()
72:     # Something at the config's path that is not a file is not a config this
73:     # can write: read as "absent", `mv -f` then put the new file INSIDE a
74:     # directory there and succeeded (audit of stream C, G-C-04).
75:     if [ -e "${SYNC_CONF}" ] && [ ! -f "${SYNC_CONF}" ]; then
76:         return 1
77:     fi
78:     [ -f "${src}" ] || src=/dev/null
79:     while [ $# -ge 2 ]; do
80:         n=$((n + 1)); pairs+=("CONF_K${n}=$1" "CONF_V${n}=$2")
81:         want+=("$1=\"$2\""); shift 2
82:     done
83:     # Braced, and silenced as a whole: a redirection that fails opening the
84:     # temp file happens before a `2>/dev/null` written after it, and the
85:     # shell printed its own diagnostic -- a line number and the temp file's
86:     # path -- ahead of the caller's sentence (G-C-07).
87:     if { env "${pairs[@]}" CONF_N="${n}" awk '
88:         BEGIN {
89:             n = ENVIRON["CONF_N"] + 0
90:             for (i = 1; i <= n; i++) {
91:                 k[i] = ENVIRON["CONF_K" i]
92:                 line[i] = k[i] "=\"" ENVIRON["CONF_V" i] "\""
93:             }
94:         }
95:         {
96:             for (i = 1; i <= n; i++)
97:                 if (index($0, k[i] "=") == 1) { print line[i]; seen[i] = 1; next }
98:             print
99:         }
100:         END { for (i = 1; i <= n; i++) if (!seen[i]) print line[i] }
101:     ' "${src}" > "${tmp}" && mv -f "${tmp}" "${SYNC_CONF}"; } 2>/dev/null; then
102:         # Written is what the file says, not what mv returned: a regular
103:         # file at the path, holding every line asked for.
104:         [ -f "${SYNC_CONF}" ] || return 1
105:         for i in "${want[@]}"; do
106:             grep -qFx -- "${i}" "${SYNC_CONF}" 2>/dev/null || return 1
107:         done
108:         return 0
109:     fi
110:     rm -f "${tmp}" 2>/dev/null
111:     return 1
112: }
113: 
114: # One value from the config, read as text -- never by sourcing or eval, since
115: # a value an earlier build wrote with $( ) in it would run (PL-051) -- and as
116: # the scripts that run with it read it, so this and they never disagree
117: # about a player's folder:
118: #   - Of two assignments of a key, the FIRST: every saves run the interface
119: #     starts is --yes, which runs cloud_sync_cleanup_duplicates.sh, which
120: #     keeps the first and is what the file becomes; the content scripts'
121: #     conf_get reads the first too. This read the last, as `source` alone
122: #     would, so with a key written twice the hub's line and
123: #     --content-location named a folder the scripts stopped using at their
124: #     next run (the audit of the fix round, PL-021; the first cut's G-C-03
125: #     gpt and G-C-06 claude had moved it from first to last).
126: #   - The value double quoted, single quoted or a bare word, then nothing,
127: #     or blanks and a # comment: the forms conf_valid lets a file through
128: #     with. Anything else is exit 2 and nothing printed -- /Mine/'My Saves',
129: #     text after a closing quote, a double-quoted value with $, ` or \ in it
130: #     (what a shell would expand there) -- as the content scripts' conf_get
131: #     answers it and as conf_valid refuses the whole file. The first cut
132: #     read /Mine/'My as the folder, one no script would ever use (the audit
133: #     of the fix round, gpt G2-C-01).
134: # Nothing when the key is absent. The same awk as cloud_content_backup's and
135: # cloud_content_restore's conf_get, on the file SYNC_CONF names.
136: conf_get() { # <KEY> (the content scripts' reader, mirrored so every reader agrees, D-CLOUD-149): its value, quotes off; nothing when absent; exit 2 when unreadable, and why on stdout
137:     [ -f ${SYNC_CONF} ] || return 0
138:     awk -v k="$1" '
139:         { t = $0; gsub(/\t/, "", t); if (t ~ /[[:cntrl:]]/ && !cntrl) cntrl = NR }
140:         index($0, k "=") != 1 && !other \
141:             && $0 ~ ("^[ \t]*((export|declare|typeset|readonly|local)([ \t]+-[A-Za-z]+)*[ \t]+)?" k "[ \t]*[+]?=") { other = NR }
142:         index($0, k "=") == 1 {
143:             s = substr($0, length(k) + 2); v = ""; r = ""; ok = 1; why = ""
144:             c = substr(s, 1, 1)
145:             if (c == "\"") {
146:                 # Inside double quotes bash reads \" \\ \$ and \` as the one
147:                 # character each (PL-015), and so does this; an unescaped $
148:                 # or backtick is an expansion this reader does not make, and
149:                 # any other backslash is refused as conf_valid refuses it.
150:                 n = length(s); i = 2; closed = 0
151:                 while (i <= n) {
152:                     d = substr(s, i, 1)
153:                     if (d == "\"") { closed = 1; break }
154:                     if (d == "\\") {
155:                         e = substr(s, i + 1, 1)
156:                         if (e == "\"" || e == "\\" || e == "$" || e == "`") { v = v e; i += 2; continue }
157:                         ok = 0
158:                         why = (e == "") ? "a value continued onto the next line, which this reader does not follow" \
159:                                         : "a backslash inside double quotes that is not one of the escapes bash reads there"
160:                         break
161:                     }
162:                     if (d == "$" || d == "`") { ok = 0; why = "a $ or a backtick inside double quotes"; break }
163:                     v = v d; i++
164:                 }
165:                 if (ok && !closed) { ok = 0; why = "a double-quoted value that does not close on its line" }
166:                 if (ok) r = substr(s, i + 1)
167:             } else if (c == "'"'"'") {
168:                 j = index(substr(s, 2), c)
169:                 if (j) { v = substr(s, 2, j - 1); r = substr(s, j + 2) } else { ok = 0; why = "a single-quoted value that does not close on its line" }
170:             } else {
171:                 match(s, /^[A-Za-z0-9_.\/:@%+,=-]*/); v = substr(s, 1, RLENGTH); r = substr(s, RLENGTH + 1)
172:             }
173:             if (ok && r !~ /^([ \t]+(#.*)?)?$/) { ok = 0; why = "something after the value that is not a # comment" }
174:             if (!found) { found = 1; first = v; firstok = ok; firstwhy = "line " NR ": " why }
175:         }
176:         END {
177:             if (cntrl) { print "line " cntrl ": a control character other than a tab"; exit 2 }
178:             if (other) { print "line " other ": " k " set in a form this reader does not read"; exit 2 }
179:             if (found && !firstok) { print firstwhy; exit 2 }
180:             if (found) print first
181:         }
182:     ' ${SYNC_CONF}
183: }
184: 
185: # Wait for any confirm/cancel input: controller (evtest) or keyboard.
186: wait_for_button() {
187:     local input_device=""
188:     for dev in /dev/input/event*; do
189:         if [ -c "$dev" ]; then
190:             local supports=$(udevadm info "$dev" 2>/dev/null | awk '/ID_INPUT_JOYSTICK=1/ {print "joystick"}')
191:             if [ "$supports" = "joystick" ]; then
192:                 input_device="$dev"
193:                 break
194:             fi
195:         fi
196:     done
197:     if [ -n "$input_device" ]; then
198:         evtest "$input_device" 2>/dev/null | grep -m 1 -E "BTN_(SOUTH|EAST|A|B|START).*value 1" >/dev/null
199:     else
200:         read -sn1 2>/dev/null
201:     fi
202: }
203: 
204: # Connection facts, shared by the console flow and the native UI.
205: # resolve_connection sets SSH_CMD, SHOW_QR, OVERRIDE_ACTIVE and IP_ADDR
206: # (empty when offline).
207: resolve_connection() {
208:     OVERRIDE_ACTIVE=0
209:     IP_ADDR=$(ip route get 1 2>/dev/null | awk '{for (i=1;i<=NF;i++) if ($i=="src") {print $(i+1); exit}}')
210:     # The -L tunnel lets the provider sign-in page (which rclone serves on
211:     # the handheld at localhost:53682) open in the computer's own browser,
212:     # so the full 'auto config' flow works over SSH - see
213:     # rclone.org/remote_setup.
214:     SSH_CMD="ssh -L 53682:localhost:53682 root@${IP_ADDR}"
215:     SHOW_QR=1
216:     # Optional connection override: when the device is reached through a
217:     # gateway that remaps its address (development setups, tunnels,
218:     # proxies), the command in this file is shown instead of the direct one.
219:     OVERRIDE_FILE="/storage/.config/cloud_setup_ssh"
220:     if [ -s "${OVERRIDE_FILE}" ]; then
221:         SSH_CMD=$(head -n1 "${OVERRIDE_FILE}")
222:         SHOW_QR=0
223:         OVERRIDE_ACTIVE=1
224:         log_message "Using connection override: ${SSH_CMD}"
225:     fi
226: }
227: 
228: # True when at least one inbound SSH session is established (a peer is
229: # connected to local port 22). Reads /proc/net/tcp* directly so it works
230: # without ss/netstat; port 22 is 0016 hex, state 01 is ESTABLISHED.
231: ssh_session_established() {
232:     local f
233:     for f in /proc/net/tcp /proc/net/tcp6; do
234:         [ -r "$f" ] || continue
235:         if awk 'NR>1 { n=split($2,a,":"); if (a[n]=="0016" && $4=="01") found=1 } END { exit found?0:1 }' "$f"; then
236:             return 0
237:         fi
238:     done
239:     return 1
240: }
241: 
242: # True when something on the device already listens on rclone's OAuth
243: # port 53682 (hex D1B2, state 0A is LISTEN) - a stale sign-in webserver
244: # from an interrupted `rclone config` would make the next auto-config
245: # attempt fail with "bind: address already in use".
246: auth_port_busy() {
247:     local f
248:     for f in /proc/net/tcp /proc/net/tcp6; do
249:         [ -r "$f" ] || continue
250:         if awk 'NR>1 { n=split($2,a,":"); if (a[n]=="D1B2" && $4=="0A") found=1 } END { exit found?0:1 }' "$f"; then
251:             return 0
252:         fi
253:     done
254:     return 1
255: }
256: 
257: # Does this cloud folder work on this remote?
258: #
259: # Dropbox, Google Drive and OneDrive are path-based: "/GAMES" is a folder and
260: # any name will do. S3, B2 and friends are bucket-based - the first path
261: # component IS the bucket, and bucket names have rules the shipped default
262: # breaks (uppercase is illegal), so a sync fails with InvalidBucketName and
263: # nothing in that message points back at this setting.
264: #
265: # rclone reports the distinction itself, so no provider list is hardcoded.
266: # Returns 0 when the path will work; prints a reason and returns 1 when not.
267: # Listings that decide something get a bound (as the sync scripts' do) -- the
268: # folder probe below and the parent walk alike; `backend features` asks
269: # rclone about itself and makes no round trip: a cloud that never answers is
270: # a refusal in 30 s, not a wizard that hangs. Until #151 PL-15 the probe was
271: # the one unbounded listing here, and this comment covered only the walk.
272: readonly -a RCLONE_LIST_OPTS=(--contimeout 15s --timeout 30s --low-level-retries 3 --retries 1)
273: # Is this remote path missing, rather than unreadable? rclone answers "not
274: # found" (exit 3) when the server's reply is the one it maps to that, and a
275: # plain error (exit 1) when the words differ: an FTP server that answers a
276: # missing folder with 501 "No such directory." where the standard reply is
277: # 550 makes every "is it there yet?" branch read as "the cloud is broken"
278: # (#142, from the #133 matrix). The parent settles it, whatever the words:
279: # walk up until a level lists. A level that lists and lacks the next name is
280: # a path not created yet (0); one that lists and holds it means the failure
281: # was something else (1); a remote whose root will not list is broken (1).
282: # On a bucket an absent prefix lists as empty, which is the same answer
283: # (D-CLOUD-120). Called only after a listing has already failed with a code
284: # other than 3, so the everyday path costs nothing extra.
285: absent_not_broken() {
286:     local path="${1%/}" remote rel name parent listing
287:     remote="${path%%:*}:"; rel="${path#*:}"
288:     while [ -n "${rel}" ]; do
289:         name="${rel##*/}"
290:         case "${rel}" in */*) parent="${rel%/*}/" ;; *) parent="" ;; esac
291:         if listing=$(rclone lsf --dirs-only "${remote}${parent}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
292:             printf '%s\n' "${listing}" | grep -qFx -- "${name}/" && return 1
293:             return 0
294:         fi
295:         [ -n "${parent}" ] || return 1
296:         rel="${parent%/}"
297:     done
298:     return 1
299: }
300: 
301: # Configuration, availability and the current format are read separately
302: # from linking an rclone remote. Existing paths are never adopted or rewritten
303: # from another device's folders; only explicit setters change these values.
304: folder_path() {
305:     local part out="" lead=""; local -a parts=()
306:     case "$1" in /*) lead=/ ;; esac
307:     IFS=/ read -r -a parts <<< "$1"
308:     for part in "${parts[@]}"; do
309:         case "${part}" in ""|.) ;; ..) return 2 ;; *) out="${out:+${out}/}${part}" ;; esac
310:     done
311:     # A nonempty relative dot-only path names the remote root. It must never
312:     # collapse into a missing setting and silently select a fresh default.
313:     [ -z "$1" ] || [ -n "${lead}${out}" ] || return 2
314:     printf '%s%s' "${lead}" "${out}"
315: }
316: folder_values() {
317:     local value field
318:     if [ -e "${SYNC_CONF}" ] && [ ! -f "${SYNC_CONF}" ]; then
319:         echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"
320:         return 2
321:     fi
322:     for field in SAVES_REMOTE SETTINGS_REMOTE CONTENT_REMOTE; do
323:         value=$(conf_get "${field}") || { echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"; return 2; }
324:         value=$(folder_path "${value}") || { echo ">>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ"; return 2; }
325:         case "${field}" in
326:             SAVES_REMOTE) SAVES="${value:-/pixelelated/Saves}" ;;
327:             SETTINGS_REMOTE) BACKUPS="${value:-/pixelelated/Backups}" ;;
328:             CONTENT_REMOTE)
329:                 # Explicit empty still means the cloud root; an absent setting
330:                 # alone receives the fresh-install default.
331:                 CONTENT="${value}"
332:                 grep -q '^CONTENT_REMOTE=' "${SYNC_CONF}" || CONTENT=/pixelelated/Content ;;
333:         esac
334:     done
335: }
336: folder_listing() { # <remote path> [lsf flags]; missing is distinct from unreadable
337:     local path="$1" rc; shift
338:     FOLDER_LISTING=$(rclone lsf "$@" "${path}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); rc=$?
339:     [ "${rc}" -ne 0 ] || return 0
340:     # A failed listing may already have printed entries. Those bytes cannot
341:     # establish presence or absence, even for a not-found return code.
342:     if [ -n "${FOLDER_LISTING}" ]; then
343:         echo ">>> why YOUR CLOUD STOPPED ANSWERING"
344:         return "${rc}"
345:     fi
346:     if [ "${rc}" -eq 3 ] || [ "${rc}" -eq 4 ] || absent_not_broken "${path}"; then
347:         FOLDER_LISTING=""
348:         return 0
349:     fi
350:     echo ">>> why YOUR CLOUD STOPPED ANSWERING"
351:     return "${rc}"
352: }
353: folder_exists() { # return 0 present, 1 absent, or >1 unreadable
354:     local path="$1" remote relative parent name rc
355:     # An absolute remote root and its relative home are different on SFTP.
356:     case "${path#*:}" in /) ;; *) path="${path%/}" ;; esac
357:     folder_listing "${path}"; rc=$?
358:     [ "${rc}" -eq 0 ] || return 5
359:     [ -z "${FOLDER_LISTING}" ] || return 0
360:     # A successfully listed remote root exists even when it is empty.
361:     case "${path#*:}" in ""|/) return 0 ;; esac
362:     remote="${path%%:*}:"; relative="${path#*:}"
363:     name="${relative##*/}"
364:     [ -n "${name}" ] || return 1
365:     # A relative one-component name belongs to remote:, while /Name belongs
366:     # to remote:/. Preserve that distinction for SFTP and similar providers.
367:     case "${relative}" in */*) parent="${relative%/*}/" ;; *) parent="" ;; esac
368:     folder_listing "${remote}${parent}" --dirs-only; rc=$?
369:     [ "${rc}" -eq 0 ] || return 5
370:     printf '%s\n' "${FOLDER_LISTING}" | grep -qxF -- "${name}/"
371: }
372: folder_current_namespace() {
373:     local identity="${SAVES#/}" features folding
374:     [ "${identity}" = pixelelated/Saves ] && return 0
375:     [ "${identity,,}" = pixelelated/saves ] || return 1
376:     # Case variants are the default only on a folding provider. Read the
377:     # selected parent in its own spelling; SFTP leading slashes still matter.
378:     features=$(rclone backend features "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null) || features=""
379:     folding=$(printf '%s' "${features}" | jq -r 'if .Features.CaseInsensitive == true then "true" elif .Features.CaseInsensitive == false then "false" else "unknown" end' 2>/dev/null)
380:     case "${folding}" in
381:         true) return 0 ;;
382:         false) return 1 ;;
383:         *)
384:             echo ">>> why YOUR CLOUD FOLDER COULDN'T BE READ"
385:             return 5 ;;
386:     esac
387: }
388: folder_marker_read() {
389:     FOLDER_VERSION=0
390:     # Custom/legacy paths are independent choices, not a renamed layout.
391:     folder_current_namespace; local scope=$?
392:     case "${scope}" in 0) ;; 1) return 0 ;; *) return "${scope}" ;; esac
393:     local tmp rc version
394:     tmp=$(mktemp /tmp/cloud_folder_marker.XXXXXX) || return 5
395:     rclone cat "${REMOTE}${SAVES%/*}/.layout" "${RCLONE_LIST_OPTS[@]}" > "${tmp}" 2>/dev/null; rc=$?
396:     if [ "${rc}" -ne 0 ]; then
397:         rm -f "${tmp}"
398:         folder_listing "${REMOTE}${SAVES%/*}/" --files-only || return $?
399:         if printf '%s\n' "${FOLDER_LISTING}" | grep -qxF '.layout'; then
400:             echo ">>> why YOUR CLOUD STOPPED ANSWERING"
401:             return "${rc}"
402:         fi
403:         return 0
404:     fi
405:     for version in 1 2; do
406:         if printf 'layout=%s\n' "${version}" | cmp -s - "${tmp}"; then
407:             FOLDER_VERSION="${version}"
408:             rm -f "${tmp}"
409:             return 0
410:         fi
411:     done
412:     rm -f "${tmp}"
413:     echo ">>> why YOUR CLOUD FOLDER COULDN'T BE READ"
414:     echo "This cloud folder uses a layout this version can't read. Check for a newer system version before trying again."
415:     return 4
416: }
417: folder_marker_write() {
418:     folder_current_namespace; local scope=$?
419:     case "${scope}" in 0) ;; 1) return 0 ;; *) return "${scope}" ;; esac
420:     folder_marker_read || return $?
421:     printf 'layout=2\n' | rclone rcat "${REMOTE}${SAVES%/*}/.layout" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null || return 5
422:     folder_marker_read || return $?
423:     [ "${FOLDER_VERSION}" = 2 ] || return 5
424: }
425: 
426: # Callers pass the first remote; an empty one stops after the string checks,
427: # which hold with no remote configured at all.
428: syncpath_problem() {
429:     local path="$1" remote="$2" bucket probe
430:     path="${path%/}"
431:     case "${path}" in .|..|./*|../*) echo "That folder name can't be used."; return 1 ;; esac
432: 
433:     if [ -z "${path}" ] || [ "${path}" = "/" ]; then
434:         echo "Your cloud folder can't be empty."
435:         return 1
436:     fi
437:     # The config is shell, sourced by every cloud script: the characters a
438:     # shell reads inside double quotes, and control characters, are refused
439:     # where the folder is typed (audit #307 PL-051, conf_set).
440:     case "${path}" in
441:         *[\"\$\`\\]*|*[[:cntrl:]]*)
442:             echo "Your cloud folder's name can't contain \", \$, \`, or \\."
443:             return 1
444:             ;;
445:     esac
446:     # Every part of the path is a folder's name, and the checks below read
447:     # the text. A part that is empty (//), . or .. names no folder of its
448:     # own: /Mine/Backups/. is /Mine/Backups on a cloud that resolves it,
449:     # while its siblings -- <parent>/Backups and <parent>/Content, made from
450:     # the text by dirname -- came out as /Mine/Backups/Backups and
451:     # /Mine/Backups/Content, inside it: the nesting the sibling check below
452:     # exists to stop, walked past (the audit of the fix round, PL-009; gpt
453:     # G2-C-04). Refused where it is typed, before any other check reads the
454:     # text, with the folder the path would have meant.
455:     case "${path}/" in
456:         *//*|*/./*|*/../*)
457:             local part canon="" try
458:             local -a parts=()
459:             IFS=/ read -r -a parts <<< "${path#/}"
460:             for part in "${parts[@]}"; do
461:                 case "${part}" in
462:                     ""|.) ;;
463:                     ..) canon="${canon%/*}" ;;
464:                     *) canon="${canon}/${part}" ;;
465:                 esac
466:             done
467:             if [ -z "${canon}" ]; then
468:                 echo "Your cloud folder can't be empty."
469:                 return 1
470:             fi
471:             try="${canon}"
472:             case "${path}" in /*) ;; *) try="${try#/}" ;; esac
473:             echo "Your cloud folder can't have an empty part, or a part called . or .., in its path."
474:             echo "Try ${try}."
475:             return 1
476:             ;;
477:     esac
478:     [ -n "${remote}" ] || return 0
479: 
480:     # No provider rules are encoded here on purpose. rclone does not validate
481:     # bucket names itself - it hands them to the provider and relays the
482:     # rejection - so the rules live with the provider, differ between them,
483:     # and would go stale in this script. The problem was never missing
484:     # validation; it was validation arriving at sync time, in a log, as
485:     # "InvalidBucketName" with nothing tying it to the folder that caused it.
486:     #
487:     # So: ask the provider now, and attach the answer to the setting.
488:     #
489:     # Only what rclone says went wrong, never its listing. This used to read
490:     # stdout as well, so a folder that already existed and held anything --
491:     # a saves folder with savestates/ in it, which is every folder somebody
492:     # would type on a second device -- was refused as "your provider would
493:     # not accept this folder", with the folder's own contents quoted as the
494:     # reason (found by the A3 fixture on the VM pair, 2026-09-06).
495:     probe=$(rclone lsd "${remote}${path}" "${RCLONE_LIST_OPTS[@]}" --log-level ERROR 2>&1 >/dev/null | head -2)
496:     case "${probe}" in
497:         # A folder that does not exist yet is fine - it gets created on use.
498:         *"not found"*|*NoSuchBucket*|"") return 0 ;;
499:     esac
500:     # The same folder, on a server whose "missing" rclone relays as a plain
501:     # error rather than "not found" (#142). On a path-based cloud a folder
502:     # its parent lacks is a folder not created yet, whatever the words. On
503:     # a bucket the first component is a bucket name the provider judges,
504:     # and the provider's own answer stands -- the parent rule would read
505:     # InvalidBucketName as "not there yet" and store the name it rejected.
506:     #
507:     # Which kind this remote is, rclone says in JSON, and the answer has to
508:     # be one of the two before anything rests on it. A `backend features`
509:     # that fails or prints neither is "unknown", and unknown takes the
510:     # provider's refusal at face value: the parent walk runs only on a
511:     # remote known to be path-based. Until #151 PL-14 a failed call read as
512:     # "not bucket-based" -- a grep over empty output -- and the walk ran,
513:     # so the one guard against storing a rejected bucket name fell open
514:     # exactly when rclone could not be asked.
515:     local features bucket_based=unknown
516:     if features=$(rclone backend features "${remote}" 2>/dev/null); then
517:         case "${features}" in
518:             *'"BucketBased": true'*)  bucket_based=yes ;;
519:             *'"BucketBased": false'*) bucket_based=no ;;
520:         esac
521:     fi
522:     if [ "${bucket_based}" = no ] && absent_not_broken "${remote}${path}"; then
523:         return 0
524:     fi
525: 
526:     # Something is wrong. If the remote is bucket-based, name the reason the
527:     # message will not: the first path component is a bucket, not a folder.
528:     if [ "${bucket_based}" = yes ]; then
529:         bucket="${path#/}"; bucket="${bucket%%/*}"
530:         echo "Your provider wouldn't accept \"${bucket}\"."
531:         echo
532:         echo "This provider keeps things in buckets, so the first part of the"
533:         echo "folder is a bucket name, not a folder - and bucket names have"
534:         echo "rules that folders do not. They are also shared with everyone"
535:         echo "else using the provider, not private to your account."
536:         echo
537:         echo "  ${probe}"
538:         echo
539:         echo "Try something like /pixelelated-saves-yourname/Saves instead."
540:     else
541:         echo "Your provider wouldn't accept this folder:"
542:         echo
543:         echo "  ${probe}"
544:     fi
545:     return 1
546: }
547: 
548: validation_context() {
549:     folder_values >/dev/null || return 2
550:     local remotes config_file config_id
551:     REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null) || return 2
552:     [ -n "${REMOTE}" ] || return 2
553:     config_file=$(timeout 3 rclone config file 2>/dev/null | tail -1)
554:     [ -f "${config_file}" ] && [ -r "${config_file}" ] || return 2
555:     # Only a digest leaves this scope; never print credential/config bytes.
556:     config_id=$( set -o pipefail; { printf '%s\0' "${REMOTE}" "${SAVES}" "${BACKUPS}" "${CONTENT}";
557:         sha256sum "${config_file}" || exit 1
558:         if [ -f "${SYNC_CONF}" ]; then sha256sum "${SYNC_CONF}" || exit 1; fi
559:         if [ -f /storage/.config/rclone/active-connection ]; then
560:             sha256sum /storage/.config/rclone/active-connection || exit 1
561:         fi
562:     } | sha256sum) || return 2
563:     config_id="${config_id%% *}"
564:     jq -n --arg id "${config_id}" --arg remote "${REMOTE}" \
565:         --arg saves "${SAVES}" --arg settings "${BACKUPS}" --arg content "${CONTENT}" \
566:         '{schema_version:1,config_id:$id,remote:$remote,paths:{saves:$saves,settings:$settings,content:$content,
567:           roms:(($content | rtrimstr("/")) + (if $content == "" then "" else "/" end) + "ROMs"),bios:(($content | rtrimstr("/")) + (if $content == "" then "" else "/" end) + "BIOS"),media:(($content | rtrimstr("/")) + (if $content == "" then "" else "/" end) + "ROMs")}}'
568: }
569: 
570: seed_categories() {
571:     local category
572:     [ -n "$1" ] || return 2
573:     case "$1" in ,*|*,|*,,*|*[!a-z,]*) return 2 ;; esac
574:     IFS=, read -r -a SEED_CATEGORIES <<< "$1"
575:     local seen=,
576:     for category in "${SEED_CATEGORIES[@]}"; do
577:         case "${category}" in saves|settings|roms|bios|media) ;; *) return 2 ;; esac
578:         case "${seen}" in *,"${category}",*) return 2 ;; esac
579:         seen+="${category},"
580:     done
581: }
582: seed_selected() { local category; for category in "${SEED_CATEGORIES[@]}"; do [ "${category}" != "$1" ] || return 0; done; return 1; }
583: 
584: case "$1" in
585:     --validation-context)
586:         [ "$#" -eq 1 ] || exit 2
587:         validation_context || { echo '{"schema_version":1,"error":"unreadable-config"}'; exit 2; }
588:         exit 0
589:     ;;
590:     --validate-folders)
591:         [ "$#" -eq 3 ] || exit 2
592:         tool="$(dirname "$(readlink -f "$0")")/cloud_folder_validate"
593:         [ -x "${tool}" ] || tool=/usr/bin/cloud_folder_validate
594:         exec "${tool}" "$2" "$3"
595:     ;;
596:     --folder-state)
597:         REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
598:         [ -n "${REMOTE}" ] || { echo "STATE=no-remote"; exit 1; }
599:         folder_values || exit $?
600:         folder_marker_read || exit $?
601:         folder_exists "${REMOTE}${SAVES}"; rc=$?
602:         case "${rc}" in 0) state=ready; present=1 ;; 1) state=missing; present=0 ;; *) exit "${rc}" ;; esac
603:         printf 'STATE=%s\nSAVES=%s\nBACKUPS=%s\nCONTENT=%s\nSAVES_EXISTS=%s\n' \
604:             "${state}" "${SAVES}" "${BACKUPS}" "${CONTENT}" "${present}"
605:         exit 0
606:     ;;
607:     --info)
608:         # Machine-readable connection facts for the native UI.
609:         resolve_connection
610:         echo "IP=${IP_ADDR}"
611:         echo "SSH_CMD=${SSH_CMD}"
612:         echo "OVERRIDE=${OVERRIDE_ACTIVE}"
613:         # Whether a root password is set, never the password: this output is
614:         # parsed by EmulationStation through a pipeline, and a credential that
615:         # crosses a script boundary is one careless echo from a log (#116,
616:         # D-INFRA-008). The page that must show or pre-fill it reads
617:         # root.password in-process from its own settings.
618:         echo "PASSWORD_SET=$([ -n "$(get_setting root.password)" ] && echo 1 || echo 0)"
619:         echo "SSH_UP=$(systemctl is-active sshd 2>/dev/null)"
620:         echo "AUTH_PORT=$(auth_port_busy && echo busy || echo free)"
621:         # Both names for one value: EmulationStation reads SYNCPATH= until its
622:         # side of the vocabulary sweep (#73) lands; SAVES_REMOTE= is the name.
623:         # A folder in a form the scripts cannot read is named as none: the
624:         # sync refuses that config too, and the folder editor the interface
625:         # opens from this line is the way to set one it can (gpt G2-C-01).
626:         if ! saves_remote="$(conf_get SAVES_REMOTE)"; then
627:             log_message "SAVES_REMOTE in ${SYNC_CONF} is not in a form the sync reads (${saves_remote}); no folder named"
628:             saves_remote=""
629:         fi
630:         echo "SAVES_REMOTE=${saves_remote}"
631:         echo "SYNCPATH=${saves_remote}"
632:         if folder_values >/dev/null; then
633:             echo "SETTINGS_REMOTE=${BACKUPS}"
634:             echo "CONTENT_REMOTE=${CONTENT}"
635:         else
636:             echo "SETTINGS_REMOTE="
637:             echo "CONTENT_REMOTE="
638:         fi
639:         echo "REMOTES=$(rclone listremotes 2>/dev/null | tr '\n' ' ')"
640:         # Which provider this device is actually connected to. The name is the
641:         # player's own label for the remote; the type is rclone's word for the
642:         # service (dropbox, drive, webdav...), which EmulationStation turns
643:         # into the name the player picked it by. Until this, nothing on any
644:         # screen said who the cloud was -- the setup page offered to connect
645:         # one and never mentioned the one already there (fork #110).
646:         remote_name="$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)"
647:         remote_name="${remote_name%:}"
648:         echo "REMOTE_NAME=${remote_name}"
649:         remote_type=""
650:         if [ -n "${remote_name}" ]; then
651:             remote_type=$(rclone config show "${remote_name}" 2>/dev/null | sed -n 's/^[[:space:]]*type[[:space:]]*=[[:space:]]*//p' | head -1)
652:         fi
653:         echo "REMOTE_TYPE=${remote_type}"
654:         exit 0
655:     ;;
656:     --content-location)
657:         tool="$(dirname "$(readlink -f "$0")")/cloud_folder_validate"
658:         [ -x "${tool}" ] || tool=/usr/bin/cloud_folder_validate
659:         result=$("${tool}" roms,bios "location-$$") || { echo "STATE=unreadable"; exit 1; }
660:         CP=$(printf '%s' "${result}" | jq -r '.paths.content')
661:         AT_PATH=$(printf '%s' "${result}" | jq '[.categories[] | select(.state == "present")] | length')
662:         printf 'CONTENT_REMOTE=%s\nAT_PATH=%s\nAT_ROOT=0\nROOT_DIRS=\nFOUND=\n' "${CP}" "${AT_PATH}"
663:         if [ "${AT_PATH}" -gt 0 ]; then echo "STATE=ok"; else echo "STATE=empty"; fi
664:         exit 0
665:     ;;
666: 
667:     --set-content-remote|--set-settings-remote)
668:         SETTING=CONTENT_REMOTE
669:         [ "$1" != --set-settings-remote ] || SETTING=SETTINGS_REMOTE
670:         # Change exactly one selected location. Leading slash semantics are
671:         # preserved for path-based providers; no discovery or relocation.
672:         # Spaces, apostrophes and dots within a name are literal text.
673:         NEWPATH="$2"
674:         [ -z "${NEWPATH}" ] && { echo "ERROR empty path"; exit 1; }
675:         # Reject controls before command substitution can strip a trailing
676:         # newline and turn an invalid name into a different valid one.
677:         case "${NEWPATH}" in
678:             *[\$\`\\\"]*|*[[:cntrl:]]*) echo "That folder name has characters your cloud sync settings can't hold."; exit 1 ;;
679:         esac
680:         [ "${NEWPATH}" = / ] || NEWPATH="${NEWPATH%/}"
681:         case "${NEWPATH}" in
682:             .|..|./*|../*|*/../*|*/..|*/./*|*/.|*//*) echo "That folder name can't be used."; exit 1 ;;
683:         esac
684:         if ! conf_set "${SETTING}" "${NEWPATH}"; then
685:             echo "Your cloud sync settings couldn't be saved."
686:             log_message "${SETTING} NOT changed to ${NEWPATH}: ${SYNC_CONF} could not be written"
687:             exit 1
688:         fi
689:         log_message "${SETTING} set to ${NEWPATH} by request"
690:         echo "OK ${NEWPATH}"
691:         exit 0
692:     ;;
693:     --use-content-root)
694:         # The safe resolution: point this device back at the root where its
695:         # content already is. Moves nothing, reversible, instant.
696:         if ! conf_set CONTENT_REMOTE ""; then
697:             echo "ERROR the cloud sync settings could not be saved"
698:             log_message "Content path NOT changed: ${SYNC_CONF} could not be written"
699:             exit 1
700:         fi
701:         log_message "Content path set to the remote root by request"
702:         echo "OK content stays at the remote root"
703:         exit 0
704:     ;;
705: 
706:     --accept-saves-root)
707:         # The owner says the card the saves folder is on now is the right
708:         # one (#83): remember it, so saves transfers stop refusing.
709:         tool="$(dirname "$(readlink -f "$0")")/cloud_saves_root"
710:         [ -x "${tool}" ] || tool=/usr/bin/cloud_saves_root
711:         exec "${tool}" accept
712:     ;;
713:     --check-syncpath)
714:         # Validate a candidate cloud folder without changing anything, so the
715:         # UI can refuse a bad one where it is typed rather than letting it
716:         # fail later inside a sync.
717:         if [ -n "${2:-}" ]; then
718:             CAND="$2"
719:         elif ! CAND="$(conf_get SAVES_REMOTE)"; then
720:             echo "Your cloud sync settings couldn't be read."
721:             exit 1
722:         else
723:             # One trailing slash is a spelling, not an empty part
724:             # (the audit of the fixes, claude G3-D-07).
725:             CAND="${CAND%/}"
726:         fi
727:         REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
728:         if [ -z "${REMOTE}" ]; then
729:             echo "No cloud remote configured."
730:             exit 2
731:         fi
732:         if syncpath_problem "${CAND}" "${REMOTE}"; then
733:             echo "OK ${CAND}"
734:             exit 0
735:         fi
736:         exit 1
737:     ;;
738: 
739:     --set-saves-remote|--set-syncpath)
740:         # Select only the saves location. Settings and library choices belong
741:         # to separate controls, including on upgrades from public ROCKNIX.
742:         NEWPATH="$2"
743:         if [ -z "${NEWPATH}" ]; then
744:             echo "ERROR empty path"
745:             exit 1
746:         fi
747:         case "${NEWPATH}" in
748:             *[\$\`\\\"]*|*[[:cntrl:]]*) echo "That folder name can't be used."; exit 1 ;;
749:         esac
750:         NEWPATH="${NEWPATH%/}"
751:         if [ "${NEWPATH}" = "/" ]; then
752:             echo "ERROR root path not allowed"
753:             exit 1
754:         fi
755:         # Refuse a path this remote cannot use. The literal path checks also
756:         # hold with no remote; existing independent pointers are preserved.
757:         SP_REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
758:         if ! syncpath_problem "${NEWPATH}" "${SP_REMOTE}"; then
759:             exit 1
760:         fi
761:         if ! conf_set SAVES_REMOTE "${NEWPATH}"; then
762:             # Under the interface's "THE CLOUD FOLDER WAS NOT CHANGED": this line
763:             # says why, and nothing the title already said (G-C-03 claude).
764:             echo "Your cloud sync settings couldn't be saved."
765:             log_message "Sync path NOT changed to ${NEWPATH}: ${SYNC_CONF} could not be written"
766:             exit 1
767:         fi
768:         log_message "Sync path changed to ${NEWPATH}"
769:         echo "OK ${NEWPATH}"
770:         exit 0
771:     ;;
772:     --free-auth-port)
773:         # Clear a stale sign-in webserver left by an interrupted
774:         # `rclone config`, so the next auto-config attempt can bind.
775:         pkill -f "rclone config" 2>/dev/null
776:         pkill -f "rclone authorize" 2>/dev/null
777:         log_message "Cleared stale processes holding the OAuth port"
778:         echo "OK"
779:         exit 0
780:     ;;
781:     --connected)
782:         # The native UI gates its connect step on this, so the player
783:         # cannot advance without an SSH session actually being open.
784:         if ssh_session_established; then
785:             echo "CONNECTED"
786:             exit 0
787:         fi
788:         echo "NONE"
789:         exit 1
790:     ;;
791:     --seed-folders)
792:         [ "$#" -eq 2 ] && seed_categories "$2" || { echo "Choose which cloud folders to create."; exit 2; }
793:         REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
794:         [ -n "${REMOTE}" ] || { echo "ERROR no remote"; exit 2; }
795:         folder_values || exit $?
796:         seed_failed=0
797:         # Only the saves action reads/writes its historical layout guard.
798:         if seed_selected saves; then folder_marker_read || exit $?; fi
799:         declare -a seed_dirs=() check_dirs=()
800:         for category in "${SEED_CATEGORIES[@]}"; do
801:             case "${category}" in
802:                 saves) seed_dirs+=("${SAVES}" "${SAVES}/savefiles" "${SAVES}/savestates" "${SAVES}/screenshots"); check_dirs+=("${SAVES}") ;;
803:                 settings) seed_dirs+=("${BACKUPS}"); check_dirs+=("${BACKUPS}") ;;
804:                 roms|media) seed_dirs+=("${CONTENT%/}${CONTENT:+/}ROMs"); check_dirs+=("${CONTENT%/}${CONTENT:+/}ROMs") ;;
805:                 bios) seed_dirs+=("${CONTENT%/}${CONTENT:+/}BIOS"); check_dirs+=("${CONTENT%/}${CONTENT:+/}BIOS") ;;
806:             esac
807:         done
808:         for d in "${seed_dirs[@]}"; do
809:             if ! rclone mkdir --s3-directory-markers "${REMOTE}${d}" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null; then
810:                 echo ">>> why YOUR CLOUD FOLDERS COULDN'T BE CREATED"
811:                 exit 5
812:             fi
813:         done
814:         if seed_selected saves; then folder_marker_write || exit $?; fi
815: 
816:         seed_note() {
817:             local dir="$1" listing tmp rc; shift
818:             # Never clobber a note the owner may have written themselves, and
819:             # never write on a guess. The folder's own listing says whether a
820:             # README.txt is in it. Asking for the file by name could not: a
821:             # listing that failed for any reason read as "absent" and the
822:             # owner's note was replaced (audit #307 PL-047), and on a bucket
823:             # a key that is not there lists as nothing with exit 0, which read
824:             # as "present" -- so no README was ever written there (#308
825:             # claude F-RS-09). A listing that fails writes nothing.
826:             if ! listing=$(rclone lsf --files-only "${REMOTE}${dir}/" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null); then
827:                 log_message "Seeding: ${dir} could not be listed, so its README was not written"
828:                 return 1
829:             fi
830:             printf '%s\n' "${listing}" | grep -qFx -- 'README.txt' && return 0
831:             tmp=$(mktemp) || return 1
832:             printf '%s\n' "$@" > "${tmp}"
833:             # --ignore-existing: another device may have written one since
834:             # the listing.
835:             rclone copyto --ignore-existing "${tmp}" "${REMOTE}${dir}/README.txt" "${RCLONE_LIST_OPTS[@]}" 2>/dev/null; rc=$?
836:             rm -f "${tmp}"
837:             return "${rc}"
838:         }
839: 
840:         if seed_selected saves; then
841:             seed_note "${SAVES}" "Game saves, save states, and screenshots." "" \
842:                 "Use savefiles/, savestates/, and screenshots/ for emulator progress." \
843:                 "Game saves in supported system folders keep their normal layout." || seed_failed=1
844:         fi
845:         if seed_selected settings; then
846:             seed_note "${BACKUPS}" "Settings backups, one folder per handheld." \
847:                 "Written by the device when you back up your settings." || seed_failed=1
848:         fi
849:         if seed_selected roms || seed_selected media; then
850:             seed_note "${CONTENT%/}${CONTENT:+/}ROMs" "Your games, one folder per system." "" \
851:                 "Use system folder names such as snes, psx, n64, or gba." \
852:                 "Game content stays in its system folder beside the games." || seed_failed=1
853:         fi
854:         if seed_selected bios; then
855:             seed_note "${CONTENT%/}${CONTENT:+/}BIOS" "BIOS and firmware files." \
856:                 "Keep the subfolders required by the emulator you use." || seed_failed=1
857:         fi
858: 
859:         # Report what is actually there, not what we asked for: on a bucket
860:         # remote a mkdir can succeed and leave nothing behind.
861:         for d in "${check_dirs[@]}"; do
862:             # A listing, never lsjson --stat: on a bucket remote stat reports
863:             # success for any path at all, so the MISSING branch could never
864:             # be reached -- the report would have been unconditionally OK,
865:             # which is the shape of an assertion that cannot fail.
866:             folder_exists "${REMOTE}${d}"; read_rc=$?
867:             case "${read_rc}" in
868:                 0) echo "OK ${d}" ;;
869:                 1) echo "MISSING ${d}"; seed_failed=1 ;;
870:                 *) seed_failed=1 ;;
871:             esac
872:         done
873:         [ "${seed_failed}" -eq 0 ] || { echo ">>> why YOUR CLOUD FOLDERS COULDN'T BE CREATED"; exit 5; }
874:         exit 0
875:     ;;
876: 
877:     --check)
878:         # Verify a remote ($2 if given, else the first configured one);
879:         # plain-text verdict on stdout, exit 0 = working, 1 = missing,
880:         # 2 = configured but unreachable.
881:         REMOTE="$2"
882:         [ -z "${REMOTE}" ] && REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
883:         if [ -z "${REMOTE}" ]; then
884:             echo "NONE"
885:             log_message "Cloud setup check: no remotes configured"
886:             exit 1
887:         fi
888:         # The probe is bounded like every other listing here (RCLONE_LIST_OPTS:
889:         # one run, three low-level retries). It carried only the two timeouts,
890:         # so rclone's own defaults applied -- three runs of ten retries each --
891:         # under a blocking spinner on three interface pages; the shape #113
892:         # bounded for the syncs (traced 2026-09-25, #273).
893:         if rclone lsd "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1; then
894:             echo "OK ${REMOTE}"
895:             log_message "Cloud setup verified working remote: ${REMOTE}"
896:             exit 0
897:         fi
898:         echo "FAIL ${REMOTE}"
899:         log_message "Cloud setup: remote ${REMOTE} failed verification"
900:         exit 2
901:     ;;
902: esac
903: 
904: clear
905: 
906: # Need a network address to be reachable over SSH
907: resolve_connection
908: if [ -z "${IP_ADDR}" ]; then
909:     echo -e "\e[31mNo network connection detected.\e[0m"
910:     echo "Connect to a network first, then try again."
911:     echo
912:     echo "Press any button to exit."
913:     wait_for_button
914:     exit 1
915: fi
916: 
917: ROOTPASS=$(get_setting root.password)
918: 
919: log_message "Cloud setup instructions shown (${SSH_CMD})"
920: 
921: echo -e "\e[32m=> ${OS_NAME:-ROCKNIX} CLOUD SETUP\e[0m"
922: echo
923: echo "Connect from a computer on your network and follow rclone's"
924: echo "step-by-step setup. It signs in to your cloud provider and picks"
925: echo "the account/folder to use."
926: echo
927: echo -e "  1. On your computer, connect:  \e[1;36m${SSH_CMD}\e[0m"
928: echo -e "     Password:                   \e[1;36m${ROOTPASS:-<not set>}\e[0m"
929: echo -e "  2. Run:                        \e[1;36mrclone config\e[0m"
930: echo "     Choose 'n' for a new remote, pick your provider, and follow"
931: echo "     the prompts. Defaults are fine if you are unsure."
932: echo "     When asked 'Use auto config?', answer Y, then open the"
933: echo "     sign-in link it prints in your computer's browser."
934: echo "  3. Quit with 'q' when the remote is listed, then come back here."
935: echo
936: if [ "${SHOW_QR}" = "1" ]; then
937:     echo "Phone with an SSH app instead? Scan to connect:"
938:     qrencode -t ANSIUTF8 -m 2 "ssh://root@${IP_ADDR}"
939:     echo
940: fi
941: echo "Press any button here when you are done (or to cancel)."
942: 
943: wait_for_button
944: 
945: echo
946: REMOTE=$("$(dirname "${BASH_SOURCE[0]}")/cloud_remote" active 2>/dev/null)
947: if [ -z "${REMOTE}" ]; then
948:     echo -e "\e[33mNo cloud remote configured yet.\e[0m"
949:     echo "Run this again once you have completed 'rclone config'."
950:     log_message "Cloud setup finished with no remotes configured"
951:     sleep 5
952:     exit 0
953: fi
954: 
955: echo "Checking ${REMOTE} ..."
956: if rclone lsd "${REMOTE}" "${RCLONE_LIST_OPTS[@]}" >/dev/null 2>&1; then
957:     echo -e "\e[32mCloud remote configured and working: ${REMOTE}\e[0m"
958:     echo "You can now use the cloud backup and restore tools."
959:     log_message "Cloud setup verified working remote: ${REMOTE}"
960: else
961:     echo -e "\e[31mThe remote ${REMOTE} exists but is not responding.\e[0m"
962:     echo "Its sign-in may be incomplete or expired. Connect again and"
963:     echo "run 'rclone config reconnect ${REMOTE}' to repair it."
964:     log_message "Cloud setup: remote ${REMOTE} failed verification"
965: fi
966: sleep 5
967: exit 0



# FILE distribution/projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool


## Original lines 705–765
705: RATOKENSETTINGS=(
706:     /storage/.config/duckstation/settings.ini   # Token =   (DuckStation's own sign-in; cheevos_duckstation.sh is disabled upstream)
707:     /storage/.config/melonDS/melonDS.ini        # RA_Token= RA_Password=   (cheevos_melonds.sh)
708:     /storage/.config/flycast/emu.cfg            # Token =   (cheevos_flycast.sh)
709:     /storage/.config/aethersx2/inis/PCSX2.ini   # Token =   (cheevos_aethersx2.sh)
710: )
711: # The offline RetroAchievements proxy's own folder (#165; D-RA-002,
712: # D-INFRA-010). Its cache holds the RetroAchievements token three ways -- the
713: # cached login2 row, auth::invalid_token, the t= in every queued award -- and
714: # the HMAC key that signs the award queue. There is no sanitised copy worth
715: # keeping: a queue is bound to the device that earned it, a copy on a second
716: # device would replay the same awards, and the cache re-fills from the next
717: # online launch. So the whole folder is held back, by prefix, and never put
718: # back on a restore. Not in the default LOCATIONS; a custom list such as
719: # /storage/.config sweeps it in. The toggle itself
720: # (global.retroachievements.offlineproxy) is a line in system.cfg and travels.
721: # Connection transactions and interrupted atomic writes can leave private
722: # staging files beside rclone.conf. The entire directory stays on this device.
723: DEVICEONLYDIRS=(
724:     /storage/.config/rclone/
725:     /storage/.config/raofflineproxy/
726: )
727: # The same folders as restore patterns, each with its own wildcard. Written
728: # inline as "${DEVICEONLYDIRS[@]#/}"'*' the '*' joined the LAST element only, so
729: # a second folder in the list would have left the first as a bare name --
730: # which busybox unzip -x matches against nothing (busybox tar -X happens to
731: # take a folder's subtree from its bare name; unzip does not, probed on the
732: # image's binary), and that folder's token cache would come back from a zip
733: # (#308 claude F-BR-13).
734: DEVICEONLYDIR_PATTERNS=()
735: for D in "${DEVICEONLYDIRS[@]}"; do DEVICEONLYDIR_PATTERNS+=("${D#/}*"); done
736: # This device's cloud sign-in and its name in the cloud: never in an archive,
737: # never put back from one, whichever archive it is (#307 PL-010). rclone.conf
738: # is live OAuth tokens (#52); cloud_device_id's record is the name this
739: # device's backups live under, and a restore that put another device's over
740: # it made two devices one identity in the cloud (cloud_device_id's own
741: # header: "a restore cannot clone one device's identity onto another. Keep
742: # it that way."). Held back at backup time -- rclone.conf already was, the
743: # id files now are too -- and skipped on restore, which neither branch did:
744: # an archive from before the hold-back, or from another device, put its
745: # rclone.conf over this one's and the restore reported success.
746: DEVICEONLY=(
747:     /storage/.config/rclone/rclone.conf
748:     /storage/.config/rclone/active-connection
749:     /storage/.config/cloud_sync-device-id
750:     /storage/.config/cloud_sync-device-id.previous
751: )
752: # The files a backup left out as identical to the image's own (#45), by
753: # their path under /storage/.config, one per line, as a member of the
754: # archive. A restore puts each one back to this image's copy: the backup
755: # said "this file was at its default", and a restore that left an edit made
756: # since then in place was not the settings the backup held (#307 PL-037).
757: # Never extracted onto the device itself; an image from before the change
758: # extracts it as an inert file, and a backup never collects one.
759: SEEDLIST="/storage/.config/.backuptool-seeds"
760: # Where a backup is staged (see write_archive); a run killed part-way leaves
761: # one behind, swept by the next run under the lock.
762: STAGING_PREFIX="/storage/.cache/backuptool-staging."
763: # The files a restore and the boot use to talk about a restore: the mark the
764: # boot's revert reads (and its temporary), the revert's answer for the
765: # interface, and the one-shot markers a finished restore leaves for the next



# FILE distribution/projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl


## Original lines 1–534
1: #!/bin/bash
2: # SPDX-License-Identifier: Apache-2.0
3: # Copyright (C) 2023 JELOS (https://github.com/JustEnoughLinuxOS)
4: # Copyright (C) 2022 kkoshelev (https://github.com/kkoshelev)
5: # Wi-Fi via NetworkManager (iwd backend). AP/netplay still uses iwctl on the interface.
6: 
7: . /etc/profile
8: 
9: NMCLI="$(command -v nmcli 2>/dev/null)"
10: 
11: ###
12: ### Basic WIFI properties used across the tool.
13: ###
14: ### Usage:
15: ###     wifictl command [ssid] [psk]
16: ###
17: ### For the interface's network rows (fork #191), reading NetworkManager
18: ### rather than the wifi.ssid setting:
19: ###     wifictl current           the network joined now; nothing and exit 1 when none,
20: ###                               exit 2 when NetworkManager could not be asked
21: ###     wifictl saved             the remembered networks, one per line: <name><TAB>active|saved
22: ###     wifictl saved --ssid      the same with each profile's SSID between: <name><TAB><ssid><TAB>active|saved,
23: ###                               a tab or backslash inside the name or the SSID written \t or \\;
24: ###                               nothing and exit 1 when any of it could not be read
25: ###     wifictl forget <name>     forget one: prints "forgotten", then "disconnected" on a
26: ###                               second line when it was the one in use, and clears wifi.ssid /
27: ###                               wifi.key when they name it; exit 1, nothing printed, when it is
28: ###                               not a remembered network or the delete failed; exit 2 when
29: ###                               NetworkManager could not be asked
30: ###     wifictl join <name>       join a saved network with the key NetworkManager holds for it
31: ###                               (the picker's press on a SAVED row): prints "joined" once its
32: ###                               profile is active and moves wifi.ssid / wifi.key onto it; exit 1,
33: ###                               nothing printed, when it is not a saved network or the
34: ###                               activation failed; exit 2 when NetworkManager could not be asked
35: ###
36: 
37: WIFI_TYPE=$(get_setting wifi.adhoc.enabled)
38: NETWORK_ADDRESS="192.168.80"
39: ADHOC_CLIENT_ID=$(get_setting wifi.adhoc.id)
40: [ -z "${ADHOC_CLIENT_ID}" ] && ADHOC_CLIENT_ID="1"
41: NETPLAY_SSID="NETPLAY_AP"
42: WIFI_DEV="$(ls /sys/class/net | grep -m1 ^wlan)"
43: 
44: # Typed security/join callers must not read an unavailable radio as success.
45: if [ "${1}" = security ] || [ "${1}" = connect-open ]; then
46:   [ -n "${WIFI_DEV}" ] && [ -d "/sys/class/net/${WIFI_DEV}" ] && [ -n "${NMCLI}" ] || exit 2
47: fi
48: 
49: # Exit the script if the WiFi device isn't available
50: [ -z "${WIFI_DEV}" ] && exit 0
51: [ ! -d "/sys/class/net/${WIFI_DEV}" ] && exit 0
52: [ -z "${NMCLI}" ] && exit 0
53: 
54: SSID="${2:-$(get_setting wifi.ssid 2>/dev/null)}"
55: PSK="${3-$(get_setting wifi.key 2>/dev/null)}"
56: COUNTRY="${4:-$(get_setting wifi.country | tr -d '[:space:]' 2>/dev/null)}"
57: 
58: if [ "${WIFI_TYPE}" = "1" ]; then
59:   SSID="${NETPLAY_SSID}"
60:   PSK="deadbeef"
61: fi
62: 
63: ###
64: ### Functions...
65: ###
66: 
67: # Wait for iwd to start and have a device available
68: wait_for_wifi() {
69:   for i in $(seq 1 5); do
70:     iwctl device list | grep -q "${WIFI_DEV}" && break
71:     sleep 1
72:   done
73:   [ -n "${COUNTRY}" ] && iw reg set "${COUNTRY}"
74: }
75: 
76: # lists all wifi networks, each name as the network has it: terse output
77: # escapes ':' and '\', so "Cafe: Guest" arrived as "Cafe\: Guest" from here
78: # and as "Cafe: Guest" from current and saved, and the picker -- which
79: # compares names exactly -- showed the network twice and tried to connect
80: # to the escaped name (#308 claude F-WF-05). nm_unescape is defined below;
81: # this runs after the whole file is read.
82: list_wifi() {
83:   wait_for_wifi
84:   "${NMCLI}" -w 15 dev wifi rescan ifname "${WIFI_DEV}" 2>/dev/null
85:   sleep 1
86:   "${NMCLI}" -t -f SSID dev wifi list ifname "${WIFI_DEV}" 2>/dev/null | nm_unescape | sed '/^$/d' | sort -u
87: }
88: 
89: # Only an explicit, unanimous open result may skip the key prompt. SECURITY
90: # has no colons; SSIDs do, escaped by nmcli. Unknown/mixed scans fail closed.
91: wifi_security() {
92:   local wanted="${1}" rows line name security found=0 open=0 protected=0
93:   rows=$(LC_ALL=C "${NMCLI}" -t -f SSID,SECURITY device wifi list ifname "${WIFI_DEV}" --rescan no 2>/dev/null) || { echo unknown; return 1; }
94:   while IFS= read -r line; do
95:     [[ "${line}" == *:* ]] || continue
96:     name=$(printf '%s\n' "${line%:*}" | nm_unescape)
97:     [ "${name}" = "${wanted}" ] || continue
98:     found=1
99:     security="${line##*:}"
100:     case "${security}" in
101:       ''|--) open=1 ;;
102:       *WPA*|*WEP*|*802.1X*|*OWE*) protected=1 ;;
103:       *) echo unknown; return 1 ;;
104:     esac
105:   done <<< "${rows}"
106:   if [ "${found}" = 0 ] || { [ "${open}" = 1 ] && [ "${protected}" = 1 ]; }; then
107:     echo unknown; return 1
108:   fi
109:   if [ "${open}" = 1 ]; then echo open; else echo protected; fi
110: }
111: 
112: # An unsaved open network never borrows wifi.key or deletes a saved profile.
113: # Check again at the mutation boundary, including profiles renamed by NM.
114: connect_open_wifi() {
115:   local name="${1}" rows line profile saved_ssid
116:   [ "${WIFI_TYPE}" != 1 ] && [ -n "${name}" ] || return 1
117:   [ "$(wifi_security "${name}")" = open ] || return 1
118:   rows=$(saved_wifi) || return 1
119:   while IFS= read -r line; do
120:     [ -n "${line}" ] || continue
121:     profile="${line%$'\t'*}"
122:     saved_ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${profile}" 2>/dev/null) || return 1
123:     [ "${profile}" != "${name}" ] && [ "${saved_ssid}" != "${name}" ] || return 1
124:   done <<< "${rows}"
125:   wait_for_wifi
126:   "${NMCLI}" -w 90 device wifi connect "${name}" ifname "${WIFI_DEV}" >/dev/null 2>&1
127: }
128: 
129: connect_wifi() {
130:   wait_for_wifi
131:   # Ensure NM has the device ready and has scanned
132:   for i in $(seq 1 10); do
133:     "${NMCLI}" -t -f DEVICE,STATE dev status 2>/dev/null | grep -q "^${WIFI_DEV}:disconnected" && break
134:     "${NMCLI}" -t -f DEVICE,STATE dev status 2>/dev/null | grep -q "^${WIFI_DEV}:connected" && break
135:     sleep 1
136:   done
137:   "${NMCLI}" dev wifi rescan ifname "${WIFI_DEV}" 2>/dev/null
138:   sleep 2
139:   # If a keyfile profile for this SSID already exists but is incomplete (e.g. missing
140:   # 802-11-wireless-security.key-mgmt), NM fails connection-update with "key-mgmt: property is missing".
141:   # Drop the stale profile so "device wifi connect" creates a clean one.
142:   # Two lines taken from ROCKNIX's own saved-network work (spycat88,
143:   # b1f8464241; the merged design D-UI-118, #318): with no key given, a
144:   # profile NetworkManager already holds for the name is brought up before
145:   # anything is deleted and rebuilt -- the settings-driven paths (ENABLE
146:   # WI-FI, the restore wizard) reach a saved network that way -- and a keyed
147:   # connect stores the key in the profile explicitly (psk-flags 0), so a
148:   # later join can read it.
149:   if [ -z "${PSK}" ] && "${NMCLI}" -w 30 connection up id "${SSID}" ifname "${WIFI_DEV}" >/dev/null 2>&1; then
150:     return 0
151:   fi
152:   "${NMCLI}" connection delete id "${SSID}" >/dev/null 2>&1 || true
153:   if [ -n "${PSK}" ]; then
154:     "${NMCLI}" -w 90 device wifi connect "${SSID}" password "${PSK}" ifname "${WIFI_DEV}" >/dev/null 2>&1 || return 1
155:     "${NMCLI}" connection modify "${SSID}" wifi-sec.psk-flags 0 >/dev/null 2>&1 || true
156:   else
157:     "${NMCLI}" -w 90 device wifi connect "${SSID}" ifname "${WIFI_DEV}" >/dev/null 2>&1
158:   fi
159: }
160: 
161: create_adhoc() {
162:   wait_for_wifi
163:   # NetworkManager drives iwd into AP mode itself (Device.Mode + AP.Start).
164:   # Switching the mode behind its back only makes NM force the device back to
165:   # station mode, so the netplay AP has to be a NetworkManager connection.
166:   # No DHCP: the clients derive their address from the local play ID.
167:   "${NMCLI}" connection delete id "${SSID}" >/dev/null 2>&1
168:   "${NMCLI}" connection add type wifi ifname "${WIFI_DEV}" con-name "${SSID}" ssid "${SSID}" \
169:     802-11-wireless.mode ap \
170:     802-11-wireless.band bg \
171:     802-11-wireless-security.key-mgmt wpa-psk \
172:     802-11-wireless-security.psk "${PSK}" \
173:     ipv4.method manual ipv4.addresses "${NETWORK_ADDRESS}.${ADHOC_CLIENT_ID}/24" \
174:     ipv6.method disabled || return 1
175:   "${NMCLI}" -w 30 connection up id "${SSID}" || return 1
176: }
177: 
178: connect_adhoc_client() {
179:   destroy_adhoc
180:   # Static lease: the netplay host runs no DHCP server, so the client
181:   # address is derived from the local play ID. Autoconnect stays off so a
182:   # vanished host doesn't keep the device from returning to ordinary
183:   # networks; rejoining is an explicit wifictl connect (ES toggle).
184:   "${NMCLI}" connection add type wifi ifname "${WIFI_DEV}" con-name "${SSID}" ssid "${SSID}" \
185:     802-11-wireless-security.key-mgmt wpa-psk \
186:     802-11-wireless-security.psk "${PSK}" \
187:     ipv4.method manual ipv4.addresses "${NETWORK_ADDRESS}.${ADHOC_CLIENT_ID}/24" \
188:     ipv6.method disabled connection.autoconnect no || return 1
189:   # The iwd backend fails "connection up" instantly when the SSID is not in
190:   # the scan cache yet, so make sure the host AP shows up first
191:   for i in $(seq 1 15); do
192:     "${NMCLI}" device wifi rescan ifname "${WIFI_DEV}" >/dev/null 2>&1
193:     sleep 2
194:     "${NMCLI}" -t -f SSID device wifi list ifname "${WIFI_DEV}" 2>/dev/null | grep -q "^${SSID}$" && break
195:   done
196:   "${NMCLI}" -t -f SSID device wifi list ifname "${WIFI_DEV}" 2>/dev/null | grep -q "^${SSID}$" || return 1
197:   # The host may still be coming up
198:   for i in $(seq 1 3); do
199:     "${NMCLI}" -w 20 connection up id "${SSID}" && return 0
200:     sleep 3
201:   done
202:   return 1
203: }
204: 
205: destroy_adhoc() {
206:   # Remove the netplay connection (host or client) so NM autoconnect
207:   # can't resurrect it and the device returns to the ordinary networks
208:   "${NMCLI}" connection delete id "${NETPLAY_SSID}" >/dev/null 2>&1
209: }
210: 
211: # Prefer the network currently in use for the next automatic connection. On
212: # resume the radio is only rfkill-unblocked, so NetworkManager autoconnect
213: # chooses among every saved profile and can join a different access point than
214: # the one in use -- often on another subnet, silently moving the device and
215: # dropping whatever was connected. The same applies at boot. Raising the
216: # priority of the active profile makes NM try that one first.
217: #
218: # Priority only, deliberately: every profile keeps autoconnect enabled, so a
219: # preferred network that is out of range just loses to whatever is in range.
220: # Turning autoconnect off on the others would pin harder but strand the device
221: # on a network it can no longer see. With no active connection there is nothing
222: # to prefer, and the priorities from the previous call still stand.
223: pin_wifi() {
224:   local active name
225: 
226:   active=$("${NMCLI}" -t -f GENERAL.CONNECTION device show "${WIFI_DEV}" 2>/dev/null | cut -d: -f2-)
227:   [ -z "${active}" ] && return 0
228: 
229:   "${NMCLI}" -t -f NAME,TYPE connection show 2>/dev/null |
230:     awk -F: '$2 ~ /wireless/ {print $1}' |
231:     while IFS= read -r name; do
232:       if [ "${name}" = "${active}" ]; then
233:         "${NMCLI}" connection modify "${name}" connection.autoconnect-priority 100 >/dev/null 2>&1
234:       else
235:         "${NMCLI}" connection modify "${name}" connection.autoconnect-priority 0 >/dev/null 2>&1
236:       fi
237:     done
238: }
239: 
240: # What NetworkManager remembers and what it is joined to, for the interface
241: # (fork #191). The setting wifi.ssid is the network the player configured
242: # last; NetworkManager keeps a profile for every network the device has
243: # joined and autoconnects to whichever remembered one is in range, so the
244: # two are not the same network -- and NETWORK SETTINGS showed the setting as
245: # though it were the connection. These read NetworkManager itself.
246: #
247: # nmcli -t separates fields with ':' and escapes a ':' or '\' inside a value
248: # with a backslash. A network's name can carry either, so the fields that
249: # cannot (TYPE, ACTIVE) are taken from the right, and the name is unescaped
250: # once it stands alone.
251: nm_unescape() {
252:   sed 's/\\\(.\)/\1/g'
253: }
254: 
255: # The state saved_wifi gives a remembered network, by its whole name: the
256: # name is everything before the LAST tab (the state is after it), as the
257: # interface's parser reads it. awk -F'\t' compared the part before the
258: # FIRST tab, so a profile whose name holds a tab -- listed as SAVED and
259: # accepted by the interface -- could be neither joined nor forgotten (#308
260: # claude F-WF-06, gpt F-WF-04). The name crosses through the environment,
261: # not awk -v, which would read backslashes in it as escapes.
262: saved_state() { # <saved_wifi rows> <name>
263:   printf '%s\n' "${1}" | NAME="${2}" awk '{ n = $0; sub(/\t[^\t]*$/, "", n); if (n == ENVIRON["NAME"]) { s = $0; sub(/^.*\t/, "", s); print s } }'
264: }
265: 
266: # The SSID the device is joined to now: the one access point NetworkManager
267: # marks active, from the list it already holds (no rescan). Nothing and exit
268: # 1 when the device is joined to none; exit 2 when NetworkManager could not
269: # be asked, so a caller cannot read a silence as "not connected".
270: current_wifi() {
271:   local aps ssid
272:   aps=$("${NMCLI}" -t -f ACTIVE,SSID device wifi list ifname "${WIFI_DEV}" --rescan no 2>/dev/null) || return 2
273:   ssid=$(printf '%s\n' "${aps}" | sed -n 's/^yes://p' | head -n 1 | nm_unescape)
274:   [ -n "${ssid}" ] || return 1
275:   printf '%s\n' "${ssid}"
276: }
277: 
278: # Every network NetworkManager remembers: one line per wireless profile,
279: # <name><TAB>active or <name><TAB>saved, in nmcli's order (the one in use
280: # first). Wired and other profiles are not networks a player joined and are
281: # left out. Exit 1 with nothing printed when NetworkManager could not be
282: # asked -- an empty list and no list are different answers.
283: saved_wifi() {
284:   local profiles
285:   profiles=$("${NMCLI}" -t -f NAME,TYPE,ACTIVE connection show 2>/dev/null) || return 1
286:   printf '%s\n' "${profiles}" |
287:     awk -F: 'NF >= 3 && $(NF-1) ~ /wireless/ {
288:       name = $1; for (i = 2; i <= NF - 2; i++) name = name ":" $i
289:       print name "\t" ($NF == "yes" ? "active" : "saved")
290:     }' | nm_unescape
291: }
292: 
293: # saved with each profile's SSID (--ssid): a profile's name need not be its
294: # SSID (renamed, or NetworkManager's own "Home 1"), and the picker marks a
295: # scanned network SAVED by its SSID (stream E2's 6caac243c, #308 F-WF-12).
296: # A third column, not a change to saved's own shape, which the interface's
297: # parser and join and forget read: <name><TAB><ssid><TAB>active|saved, with
298: # a tab or backslash inside the name or the SSID written \t or \\ so the
299: # three fields split cleanly. Buffered: an SSID that cannot be read prints
300: # nothing and exits 1, never a list short of one.
301: field_escape() {
302:   local v="${1//\\/\\\\}"
303:   printf '%s' "${v//$'\t'/\\t}"
304: }
305: saved_with_ssids() {
306:   local rows line name state ssid out=""
307:   rows=$(saved_wifi) || return 1
308:   while IFS= read -r line; do
309:     [ -n "${line}" ] || continue
310:     name="${line%$'\t'*}"; state="${line##*$'\t'}"
311:     ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${name}" 2>/dev/null) || return 1
312:     out="${out}$(field_escape "${name}")"$'\t'"$(field_escape "${ssid}")"$'\t'"${state}"$'\n'
313:   done <<< "${rows}"
314:   printf '%s' "${out}"
315: }
316: 
317: # Forget a remembered network: delete its profile, and say when that dropped
318: # the connection. Prints "forgotten" once the profile is gone, then
319: # "disconnected" on a second line when it was the one in use --
320: # NetworkManager deactivates a profile as it deletes it, so the device is
321: # off that network from this moment (autoconnect may then join another
322: # remembered one in range). A name that is not a remembered wireless
323: # network, a NetworkManager that cannot be asked, or a delete that fails:
324: # nothing printed and exit 1, so a caller cannot read a refusal as done.
325: # The name is matched whole (saved_state).
326: #
327: # NetworkManager not answering is exit 2, as for current and join: "could
328: # not ask" is a different answer from "no such network" (#308 claude
329: # F-WF-07). And a network forgotten here is forgotten in the settings too:
330: # when wifi.ssid names it (by SSID, or by the profile name an older join
331: # wrote), wifi.ssid and wifi.key are removed -- otherwise the paths that
332: # connect from the settings (ENABLE WI-FI, the restore wizard; the WI-FI
333: # KEY row until #318) rebuilt the profile the player had just forgotten, with its key,
334: # which also stayed in system.cfg and travelled in the settings backup
335: # (#308 claude F-WF-01, gpt F-WF-07).
336: forget_wifi() {
337:   local name="${1}" rows state ssid named
338:   [ -n "${name}" ] || return 1
339:   rows=$(saved_wifi) || return 2
340:   state=$(saved_state "${rows}" "${name}")
341:   [ -n "${state}" ] || return 1
342:   #
343:   # And the settings go first, checked, and come back if the delete then
344:   # fails: a forget that deleted the profile and could not clear the
345:   # settings said "forgotten" while the settings-driven paths could still
346:   # rebuild it; an SSID that could not be read is not guessed at (exit 2)
347:   # (#307, the audit of the fixes, gpt G-B-11).
348:   #
349:   # The pair is cleared, and put back, in one write each (set_settings): two
350:   # set_setting calls could fail between them, and the put-back after a
351:   # failed delete was not checked at all (#307, the audit of the fix round,
352:   # gpt G2-B-11). A put-back that fails is said in the log, with the state
353:   # it leaves.
354:   local key clear=0
355:   ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${name}" 2>/dev/null) || return 2
356:   named=$(get_setting wifi.ssid 2>/dev/null)
357:   if [ -n "${named}" ] && { [ "${named}" = "${name}" ] || [ "${named}" = "${ssid}" ]; }; then
358:     clear=1
359:     key=$(get_setting wifi.key 2>/dev/null)
360:     if ! set_settings wifi.ssid default wifi.key default; then
361:       return 1
362:     fi
363:   fi
364:   if ! "${NMCLI}" connection delete id "${name}" >/dev/null 2>&1; then
365:     if [ "${clear}" -eq 1 ] && ! set_settings wifi.ssid "${named}" wifi.key "${key}"; then
366:       logger -t wifictl "forget ${name}: its profile could not be deleted, and the Wi-Fi settings cleared for it could not be put back; wifi.ssid and wifi.key are unset while the profile remains" 2>/dev/null
367:     fi
368:     return 1
369:   fi
370:   echo "forgotten"
371:   case "${state}" in *active*) echo "disconnected" ;; esac
372:   return 0
373: }
374: 
375: # Join a saved network by its profile, with the key NetworkManager holds --
376: # the picker's press on a network the device has joined before (fork #191;
377: # the maintainer's paradigm of 2026-09-15: the WI-FI NETWORK row -- WI-FI SSID
378: # until D-UI-071 renamed it -- is the network
379: # you are on, the list behind it is what is in range, a saved one joins with
380: # a press). `connect` would have deleted the profile and rebuilt it from the
381: # wifi.key setting, which held the last key typed, for some other network
382: # (the WI-FI KEY row that wrote it is gone since #318, D-UI-118).
383: # Prints "joined" once the profile is active (at once when it already is),
384: # then the settings wifi.ssid and wifi.key follow the profile, so the paths
385: # that connect from the settings -- the ENABLE WI-FI switch, the restore
386: # wizard -- name the network the player is on; the key is
387: # read from NetworkManager and never printed. pin_wifi then prefers this
388: # network at the next boot and resume. A name that is not a saved wireless
389: # network, or an activation that fails: nothing printed, exit 1. NetworkManager
390: # not answering: exit 2, so a caller cannot read a silence as a refusal.
391: # The profile active on this device's adapter, by name, unescaped. A
392: # profile's ACTIVE in saved_wifi says it is up somewhere -- on any adapter.
393: wifi_dev_connection() {
394:   "${NMCLI}" -t -f GENERAL.CONNECTION device show "${WIFI_DEV}" 2>/dev/null | sed -n 's/^GENERAL\.CONNECTION://p' | nm_unescape
395: }
396: 
397: join_wifi() {
398:   local name="${1}" rows state psk
399:   [ -n "${name}" ] || return 1
400:   rows=$(saved_wifi) || return 2
401:   state=$(saved_state "${rows}" "${name}")
402:   [ -n "${state}" ] || return 1
403:   # Judged on the adapter the picker speaks for (WIFI_DEV, as current_wifi
404:   # is): a profile already up on another adapter read as "active" and
405:   # skipped the activation, and "joined" was said while this adapter stayed
406:   # on another network (#307 PL-031). So the profile is brought up on
407:   # WIFI_DEV by name, and joined is said only once WIFI_DEV reads it.
408:   if [ "$(wifi_dev_connection)" != "${name}" ]; then
409:     "${NMCLI}" -w 90 connection up id "${name}" ifname "${WIFI_DEV}" >/dev/null 2>&1 || return 1
410:     [ "$(wifi_dev_connection)" = "${name}" ] || return 1
411:   fi
412:   # The key as NetworkManager holds it, byte for byte. -g is terse output,
413:   # which escapes ':' and '\' in a value -- ab:cd\ef12345 came back as
414:   # ab\:cd\\ef12345 on the target's nmcli (guest d, 2026-09-27) and that was
415:   # stored as wifi.key -- so --escape no (#307 PL-003). Its status is read
416:   # before anything is written: a read that failed is not an open network,
417:   # and writing its empty answer over wifi.key cleared the key of a network
418:   # the device is on (#308 claude F-WF-02). An empty key is written only
419:   # when the profile has no key management -- an open network; a keyed one
420:   # whose key did not come back leaves the settings as they were. Either
421:   # way the device is joined, and says so.
422:   #
423:   # And wifi.ssid is the network's SSID, not the profile's name: the two
424:   # differ for a renamed profile or one NetworkManager deduplicated ("Home
425:   # 1"), and connect -- which the settings-driven paths run -- looks the
426:   # SSID up in the scan, where a profile's name is not found (#308 claude
427:   # F-WF-12, gpt F-WF-03).
428:   local keyed ssid
429:   if psk=$("${NMCLI}" --escape no -s -g 802-11-wireless-security.psk connection show id "${name}" 2>/dev/null) \
430:      && ssid=$("${NMCLI}" --escape no -g 802-11-wireless.ssid connection show id "${name}" 2>/dev/null) \
431:      && [ -n "${ssid}" ]; then
432:     if [ -z "${psk}" ]; then
433:       keyed=$("${NMCLI}" --escape no -g 802-11-wireless-security.key-mgmt connection show id "${name}" 2>/dev/null) || keyed="unread"
434:     fi
435:     if [ -z "${psk}" ] && [ -n "${keyed}" ]; then
436:       logger -t wifictl "joined ${name}; its key did not come back from NetworkManager, so the Wi-Fi settings were left as they were" 2>/dev/null
437:     elif ! set_settings wifi.ssid "${ssid}" wifi.key "${psk}"; then
438:       # One write for the pair (set_settings): a second write failing after
439:       # the first left this network's SSID with the last network's key, and
440:       # nothing said so (#307, the audit of the fix round, gpt G2-B-11).
441:       # The device is joined either way, and says so.
442:       logger -t wifictl "joined ${name}; its Wi-Fi settings could not be saved, so they were left as they were" 2>/dev/null
443:     fi
444:   else
445:     logger -t wifictl "joined ${name}; its key or SSID could not be read from NetworkManager, so the Wi-Fi settings were left as they were" 2>/dev/null
446:   fi
447:   pin_wifi
448:   echo "joined"
449:   return 0
450: }
451: 
452: has_ap_mode() {
453:   wait_for_wifi
454: 
455:   PHY=$(basename "$(readlink /sys/class/net/${WIFI_DEV}/phy80211)")
456:   if iwctl adapter "$PHY" show | grep -q 'SupportedModes.*ap'; then
457:     exit 0
458:   else
459:     exit 1
460:   fi
461: }
462: 
463: case "${1}" in
464:   enable)
465:     rfkill unblock wifi
466:     ;;
467:   disable)
468:     rfkill block wifi
469:     ;;
470:   pin)
471:     pin_wifi
472:     ;;
473:   security)
474:     wifi_security "${2}"
475:     ;;
476:   connect-open)
477:     connect_open_wifi "${2}"
478:     ;;
479:   connect)
480:     if [ "${WIFI_TYPE}" = "1" ] && \
481:        [ "${ADHOC_CLIENT_ID}" = "1" ]; then
482:       create_adhoc
483:     elif [ "${WIFI_TYPE}" = "1" ]; then
484:       connect_adhoc_client
485:     else
486:       destroy_adhoc
487:       connect_wifi
488:     fi
489:   ;;
490:   disconnect)
491:     if [ "${WIFI_TYPE}" = "1" ]; then
492:       destroy_adhoc
493:     else
494:       "${NMCLI}" device disconnect "${WIFI_DEV}" >/dev/null 2>&1
495:     fi
496:     ;;
497:   reconnect)
498:     /usr/bin/wifictl disconnect
499:     /usr/bin/wifictl connect
500:     ;;
501:   list)
502:     list_wifi
503:     ;;
504:   channels)
505:     iw list | awk '/[0-9] MHz \[/ && ! /disabled|radar|no IR/ { gsub(/^.*\[/,""); gsub(/\].*$/,""); print}'
506:     ;;
507:   has_ap_mode)
508:     has_ap_mode
509:     ;;
510:   scan)
511:     "${NMCLI}" dev wifi rescan ifname "${WIFI_DEV}" 2>/dev/null
512:     ;;
513:   scanlist)
514:     "${NMCLI}" dev wifi rescan ifname "${WIFI_DEV}" 2>/dev/null
515:     sleep 2
516:     list_wifi
517:     ;;
518:   current)
519:     current_wifi
520:     ;;
521:   saved)
522:     if [ "${2:-}" = "--ssid" ]; then
523:       saved_with_ssids
524:     else
525:       saved_wifi
526:     fi
527:     ;;
528:   forget)
529:     forget_wifi "${2}"
530:     ;;
531:   join)
532:     join_wifi "${2}"
533:     ;;
534: esac



# FILE distribution/tools/cloud-connections-test


## Original lines 1–227
1: #!/usr/bin/env python3
2: """Credential-free regression tests using the actual connection module/rclone."""
3: import importlib.util
4: import os
5: from pathlib import Path
6: import subprocess
7: import sys
8: import tempfile
9: import unittest
10: import importlib.machinery
11: from unittest import mock
12: 
13: ROOT = Path(__file__).resolve().parents[1]
14: SOURCE = ROOT / 'projects/ROCKNIX/packages/network/rclone/sources'
15: sys.path.insert(0, str(SOURCE))
16: import cloud_connections as c
17: 
18: class Connections(unittest.TestCase):
19:     def setUp(self):
20:         self.tmp = tempfile.TemporaryDirectory()
21:         self.addCleanup(self.tmp.cleanup)
22:         self.root = Path(self.tmp.name)
23:         c.CONFIG = self.root / 'rclone.conf'
24:         c.ACTIVE = self.root / 'active-connection'
25:         c.LOCK = self.root / 'cloud.lock'
26:         c.SYSTEM = self.root / 'system.cfg'
27:         self.data = self.root / 'files'
28:         self.data.mkdir()
29:         self.settings = [('remote', str(self.data))]
30:         c.CONFIG.write_text('[zulu]\ntype = alias\nremote = %s\n' % self.data)
31:         self.original = c.CONFIG.read_bytes()
32: 
33:     def test_encrypted_config_stays_encrypted_through_management(self):
34:         import pexpect
35:         password = 'qa-only-fixture-password'
36:         child = pexpect.spawn(c.RCLONE, ['--config', str(c.CONFIG), 'config'], encoding='utf-8', timeout=5)
37:         try:
38:             child.expect('e/n/d/r/c/s/q>'); child.sendline('s')
39:             child.expect('a/q>'); child.sendline('a')
40:             child.expect('Enter NEW configuration password:'); child.sendline(password)
41:             child.expect('Confirm NEW configuration password:'); child.sendline(password)
42:             child.expect('c/u/q>'); child.sendline('q')
43:             child.expect('e/n/d/r/c/s/q>'); child.sendline('q')
44:             child.expect(pexpect.EOF)
45:         finally:
46:             child.close(force=True)
47:         self.assertIn(b'RCLONE_ENCRYPT_V0:', c.CONFIG.read_bytes())
48:         with mock.patch.dict(os.environ, {'RCLONE_CONFIG_PASS': password}):
49:             self.assertEqual(c.active(), 'zulu')
50:             c.save('alpha', 'alias', self.settings)
51:             c.save('zulu', 'alias', self.settings, replace=True)
52:             c.select('alpha'); c.remove('alpha')
53:             self.assertEqual(c.active(), '')
54:             self.assertEqual(c.read_config()[1]['zulu']['remote'], str(self.data))
55:         self.assertIn(b'RCLONE_ENCRYPT_V0:', c.CONFIG.read_bytes())
56:         self.assertNotIn(str(self.data).encode(), c.CONFIG.read_bytes())
57: 
58:     def test_add_keeps_legacy_selection(self):
59:         c.save('alpha', 'alias', self.settings)
60:         self.assertEqual(c.active(), 'zulu')
61:         self.assertEqual(c.ACTIVE.stat().st_mode & 0o777, 0o600)
62:         self.assertEqual(c.CONFIG.stat().st_mode & 0o777, 0o600)
63:         self.assertEqual(c.read_config()[1]['zulu']['remote'], str(self.data))
64: 
65:     def test_failed_first_publication_restores_absence(self):
66:         c.CONFIG.unlink()
67:         def failed_record(commit):
68:             commit()
69:             raise OSError('record failed')
70:         with self.assertRaises(OSError): c.save('alpha', 'alias', self.settings, publish=failed_record)
71:         self.assertFalse(c.CONFIG.exists())
72:         self.assertFalse(c.ACTIVE.exists())
73: 
74:     def test_duplicate_keeps_old_bytes(self):
75:         with self.assertRaises(c.Refused): c.save('zulu', 'alias', self.settings)
76:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
77:         self.assertFalse(c.ACTIVE.exists())
78: 
79:     def test_failed_renewal_keeps_old_bytes(self):
80:         with self.assertRaises(c.Refused): c.save('zulu', 'alias', [('remote', str(self.root/'absent'))], replace=True)
81:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
82:         self.assertEqual(list(self.root.glob('.connection-*')), [])
83: 
84:     def test_cancelled_attempt_does_not_install(self):
85:         def cancelled(commit): raise c.Refused('cancelled')
86:         with self.assertRaises(c.Refused): c.save('alpha', 'alias', self.settings, publish=cancelled)
87:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
88: 
89:     def test_success_record_failure_rolls_back(self):
90:         def failed_record(commit):
91:             commit()
92:             raise OSError('record failed')
93:         with self.assertRaises(OSError): c.save('zulu', 'alias', self.settings, replace=True, publish=failed_record)
94:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
95:         self.assertFalse(c.ACTIVE.exists())
96: 
97:     def test_remove_write_failure_restores_selection(self):
98:         atomic = c.atomic
99:         def failed_config(path, data):
100:             if path == c.CONFIG:
101:                 raise OSError('synthetic write failure')
102:             atomic(path, data)
103:         for selected in (None, b'zulu\n'):
104:             if selected is None:
105:                 c.ACTIVE.unlink(missing_ok=True)
106:             else:
107:                 c.ACTIVE.write_bytes(selected)
108:             with mock.patch.object(c, 'atomic', side_effect=failed_config):
109:                 with self.assertRaises(OSError): c.remove('zulu')
110:             self.assertEqual(c.CONFIG.read_bytes(), self.original)
111:             self.assertEqual(c.ACTIVE.read_bytes() if c.ACTIVE.exists() else None, selected)
112: 
113:     def test_external_write_refuses_commit(self):
114:         def changed(commit):
115:             c.CONFIG.write_bytes(self.original + b'other = preserved\n')
116:             commit()
117:         with self.assertRaises(c.Refused): c.save('alpha', 'alias', self.settings, publish=changed)
118:         self.assertEqual(c.CONFIG.read_bytes(), self.original + b'other = preserved\n')
119: 
120:     def test_selection_and_removal_never_move_files(self):
121:         marker = self.data / 'save.srm'; marker.write_bytes(b'fixture-save')
122:         c.save('alpha', 'alias', self.settings)
123:         c.select('alpha')
124:         self.assertEqual(c.active(), 'alpha')
125:         c.remove('alpha')
126:         self.assertEqual(c.active(), '')
127:         self.assertIn('zulu', c.read_config()[1])
128:         self.assertEqual(marker.read_bytes(), b'fixture-save')
129: 
130:     def test_missing_selection_never_falls_back(self):
131:         c.ACTIVE.write_text('missing\n')
132:         with self.assertRaises(c.Refused): c.active()
133:         c.select('zulu')
134:         self.assertEqual(c.active(), 'zulu')
135: 
136:     def test_automatic_sync_requires_deliberate_disable(self):
137:         c.SYSTEM.write_text('cloudsaves.startup=1\ncloudsaves.gameexit=0\n')
138:         for action in (lambda: c.select('zulu'), lambda: c.remove('zulu'), lambda: c.save('zulu','alias',self.settings,replace=True)):
139:             with self.assertRaises(c.Refused): action()
140:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
141: 
142:     def test_busy_transfer_refuses_management(self):
143:         with c.locked():
144:             for action in (lambda: c.select('zulu'), lambda: c.remove('zulu'), lambda: c.save('alpha','alias',self.settings)):
145:                 with self.assertRaises(c.Refused): action()
146:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
147: 
148:     def test_dependency_refuses_removal(self):
149:         c.CONFIG.write_bytes(self.original + b'\n[wrapped]\ntype = alias\nremote = zulu:folder\n')
150:         before = c.CONFIG.read_bytes()
151:         with self.assertRaises(c.Refused): c.remove('zulu')
152:         self.assertEqual(c.CONFIG.read_bytes(), before)
153: 
154:     def test_first_connection_and_manual_empty_selection(self):
155:         c.CONFIG.unlink()
156:         c.save('first','alias',self.settings)
157:         self.assertEqual(c.active(), 'first')
158:         c.remove('first')
159:         c.save('second','alias',self.settings)
160:         self.assertEqual(c.active(), '')
161: 
162:     def test_blank_edit_preserves_existing_values(self):
163:         before = dict(c.read_config()[1]['zulu'])
164:         c.save('zulu', 'alias', [], replace=True)
165:         self.assertEqual(dict(c.read_config()[1]['zulu']), before)
166: 
167:     def test_object_store_defaults_only_apply_to_new_connections(self):
168:         loader = importlib.machinery.SourceFileLoader('qa_cloud_remote', str(SOURCE/'cloud_remote'))
169:         spec = importlib.util.spec_from_loader(loader.name, loader)
170:         cli = importlib.util.module_from_spec(spec); loader.exec_module(cli)
171:         with mock.patch.object(cli, 'load_providers', return_value=[{'Name':'s3'}]), mock.patch.object(c, 'save') as save, mock.patch('builtins.print'):
172:             cli.cmd_create('bucket', 's3', [], replace=True)
173:             self.assertEqual(save.call_args.args[2], [])
174:             cli.cmd_create('bucket2', 's3', [], replace=False)
175:             self.assertIn(('directory_markers', 'true'), save.call_args.args[2])
176: 
177:     def test_verified_update_keeps_other_connections(self):
178:         c.save('alpha','alias',self.settings)
179:         elsewhere = self.root/'elsewhere'; elsewhere.mkdir()
180:         c.save('zulu','alias',[('remote',str(elsewhere))],replace=True)
181:         config = c.read_config()[1]
182:         self.assertEqual(config['alpha']['remote'], str(self.data))
183:         self.assertEqual(config['zulu']['remote'], str(elsewhere))
184:         self.assertEqual(c.active(), 'zulu')
185: 
186: class OAuthOwnership(unittest.TestCase):
187:     def setUp(self):
188:         Connections.setUp(self)
189:         loader = importlib.machinery.SourceFileLoader('qa_cloud_oauth', str(SOURCE/'cloud_oauth'))
190:         spec = importlib.util.spec_from_loader(loader.name, loader)
191:         self.oauth = importlib.util.module_from_spec(spec)
192:         loader.exec_module(self.oauth)
193:         self.oauth.STATE_DIR = str(self.root/'oauth-state')
194:         self.oauth.LOG_FILE = str(self.root/'oauth.log')
195:         self.oauth.reset_state(attempt='serve-old', session='session-old', status='waiting')
196:         self.session = self.oauth.Session('alias', 'zulu', 60)
197:         self.session.attempt = 'serve-old'; self.session.gen = 'session-old'
198:         self.session.replace = True; self.session.token = '{"access_token":"synthetic-only"}'
199: 
200:     def test_superseded_session_cannot_replace_credentials(self):
201:         self.oauth.write_state(session='session-new')
202:         ok, _ = self.session._create_remote()
203:         self.assertFalse(ok)
204:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
205:         self.assertEqual(self.oauth.read_state()['session'], 'session-new')
206: 
207:     def test_cancel_during_verification_prevents_commit(self):
208:         original_run = c.run
209:         def cancel_during_listing(args):
210:             result = original_run(args)
211:             if 'lsd' in args: self.oauth.write_state(status='idle')
212:             return result
213:         with mock.patch.object(c, 'run', side_effect=cancel_during_listing):
214:             ok, _ = self.session._create_remote()
215:         self.assertFalse(ok)
216:         self.assertEqual(c.CONFIG.read_bytes(), self.original)
217:         self.assertEqual(self.oauth.read_state()['status'], 'idle')
218: 
219:     def test_success_publishes_matching_connection_and_state(self):
220:         ok, name = self.session._create_remote()
221:         self.assertTrue(ok, name)
222:         self.assertEqual(name, 'zulu')
223:         self.assertEqual(self.oauth.read_state()['status'], 'signed-in')
224:         self.assertEqual(self.oauth.read_state()['remote'], 'zulu')
225:         self.assertEqual(c.read_config()[1]['zulu']['token'], self.session.token)
226: 
227: if __name__ == '__main__': unittest.main(verbosity=2)



# FILE distribution/tools/cloud-input-test


## Original lines 1–130
1: #!/usr/bin/env python3
2: """Full wifictl with synthetic NetworkManager; actual phone JS under delayed HTTP."""
3: from pathlib import Path
4: import json, os, re, subprocess, sys, tempfile, unittest
5: ROOT=Path(__file__).resolve().parents[1]
6: WIFI=ROOT/'projects/ROCKNIX/packages/rocknix/sources/scripts/wifictl'
7: OAUTH=ROOT/'projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'
8: 
9: class Wifi(unittest.TestCase):
10:  def setUp(self):
11:   self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
12:   self.root=Path(self.temp.name);(self.root/'shim').mkdir();(self.root/'run').mkdir()
13:   (self.root/'profile').write_text('get_setting() { case "$1" in wifi.key) echo OLD_FIXTURE_KEY;; wifi.adhoc.enabled) echo 0;; esac; }\n')
14:   shim=self.root/'shim'
15:   (shim/'nmcli').write_text('''#!/usr/bin/python3
16: import sys,json
17: from pathlib import Path
18: a=sys.argv[1:]
19: with open('/run/calls','a') as f:f.write(json.dumps(a)+'\\n')
20: if Path('/run/fail').exists():sys.exit(1)
21: if 'SSID,SECURITY' in a: print(Path('/run/scan').read_text(),end='')
22: elif 'NAME,TYPE,ACTIVE' in a: print(Path('/run/profiles').read_text(),end='')
23: elif '802-11-wireless.ssid' in a: print(Path('/run/saved-ssid').read_text(),end='')
24: elif 'DEVICE,STATE' in a: print('wlan0:disconnected')
25: ''')
26:   (shim/'iwctl').write_text('#!/bin/sh\necho wlan0\n')
27:   for name in ('sleep','iw'): (shim/name).write_text('#!/bin/sh\nexit 0\n')
28:   for p in shim.iterdir():p.chmod(0o755)
29:   for name in ('scan','profiles','saved-ssid','calls'):(self.root/'run'/name).write_text('')
30:  def call(self,*args):
31:   result = subprocess.run(['bwrap','--ro-bind','/','/','--dev','/dev','--tmpfs','/sys','--dir','/sys/class/net/wlan0','--ro-bind',str(self.root/'profile'),'/etc/profile','--ro-bind',str(self.root/'shim'),str(self.root/'shim'),'--bind',str(self.root/'run'),'/run','--setenv','PATH',str(self.root/'shim')+':/usr/bin:/bin','bash',str(WIFI),*args],text=True,capture_output=True)
32:   self.assertEqual(result.stderr, '', 'fixture or script emitted an unexpected error')
33:   return result
34:  def scan(self,*rows): (self.root/'run/scan').write_text('\n'.join(rows)+'\n')
35:  def calls(self):return [json.loads(x) for x in (self.root/'run/calls').read_text().splitlines()]
36:  def test_open_escaped_name_connects_without_key_or_delete(self):
37:   name='Cafe: \\Guest';self.scan('Cafe\\: \\\\Guest:')
38:   r=self.call('security',name);self.assertEqual((r.returncode,r.stdout),(0,'open\n'),r.stderr)
39:   r=self.call('connect-open',name);self.assertEqual(r.returncode,0,r.stderr)
40:   args=next(a for a in self.calls() if 'connect' in a)
41:   self.assertIn(name,args);self.assertNotIn('password',args)
42:   self.assertFalse(any('delete' in a for a in self.calls()))
43:  def test_protected_and_unknown_do_not_connect_open(self):
44:   for value in ('WPA2','WEP','OWE','802.1X','unexpected'):
45:    self.scan('Public:'+value)
46:    self.assertNotEqual(self.call('security','Public').stdout,'open\n')
47:    self.assertNotEqual(self.call('connect-open','Public').returncode,0)
48:   self.assertFalse(any('connect' in a for a in self.calls()))
49:  def test_mixed_and_absent_fail_closed(self):
50:   self.scan('Public:','Public:WPA2')
51:   self.assertEqual(self.call('security','Public').stdout,'unknown\n')
52:   self.assertNotEqual(self.call('connect-open','Public').returncode,0)
53:   self.assertNotEqual(self.call('connect-open','Missing').returncode,0)
54:  def test_service_failure_does_not_connect(self):
55:   self.scan('Public:');(self.root/'run/fail').touch()
56:   self.assertNotEqual(self.call('connect-open','Public').returncode,0)
57:   self.assertFalse(any('connect' in a for a in self.calls()))
58:  def test_renamed_saved_profile_is_preserved(self):
59:   self.scan('Public:');(self.root/'run/profiles').write_text('Personal Name:802-11-wireless:no\n');(self.root/'run/saved-ssid').write_text('Public\n')
60:   self.assertNotEqual(self.call('connect-open','Public').returncode,0)
61:   self.assertFalse(any('connect' in a or 'delete' in a for a in self.calls()))
62:  def test_explicit_empty_key_never_borrows_old_key(self):
63:   self.scan('Public:')
64:   r=self.call('connect','Public','','US')
65:   self.assertEqual(r.returncode,0)
66:   self.assertTrue(self.calls())
67:   self.assertFalse(any('OLD_FIXTURE_KEY' in x for a in self.calls() for x in a))
68: 
69: class Phone(unittest.TestCase):
70:  def program(self,source):
71:   # Evaluate unchanged production functions, with controllably delayed fetch.
72:   start=source.index('  var queue = Promise.resolve();')
73:   end=source.index('  // Two different strings,',start)
74:   send=source[start:end]
75:   a=source.index('  // Movement is coalesced, not queued.') if '  // Movement is coalesced, not queued.' in source else source.index('  // Coalesce only adjacent, unsent moves')
76:   b=source.index('  function down(e)',a)
77:   move=source[a:b]
78:   a=source.index('  function up(e)');b=source.index('  pad.addEventListener',a)
79:   up=source[a:b]
80:   return '''var pin='1234', events=[], waiting=[];
81: var tracking=true,moved=0,pad={classList:{remove:function(){}}};
82: function fetch(url,opts) {events.push(opts.body.split('&')[0]);return new Promise(function(resolve){waiting.push(resolve);});}
83: '''+send+move+up+'''
84: (async function(){
85:  pushMove(3,0); await Promise.resolve();
86:  pushMove(2,0); up({preventDefault:function(){}});
87:  await new Promise(r=>setTimeout(r,100));
88:  if(events.length!==1)throw Error('click overtook unfinished movement: '+events);
89:  waiting.shift()(); await new Promise(r=>setImmediate(r));
90:  if(events[1]!=='move=2,0')throw Error('pending movement lost: '+events);
91:  waiting.shift()(); await new Promise(r=>setImmediate(r));
92:  if(events[2]!=='click=1')throw Error('tap missing or out of order: '+events);
93:  waiting.shift()(); await new Promise(r=>setImmediate(r));
94:  console.log('PASS delayed movement arrives before tap');
95: })().catch(e=>{console.error(e.message);process.exitCode=1;});
96: '''
97:  def test_delayed_movement_and_click(self):
98:   result=subprocess.run(['node','-e',self.program(OAUTH.read_text())],text=True,capture_output=True)
99:   self.assertEqual(result.returncode,0,result.stderr)
100:  def test_drag_moves_without_click_and_keys_stay_ordered(self):
101:   source=OAUTH.read_text()
102:   queue=source[source.index('  var queue = Promise.resolve();'):source.index('  // Two different strings,')]
103:   movement=source[source.index('  var px = 0, py = 0, moved = 0, tracking = false;'):source.index('  pad.addEventListener')]
104:   program="""var pin='1234', events=[], waiting=[], pad={classList:{add:function(){},remove:function(){}}};
105: function fetch(url,opts) {events.push(opts.body.split('&')[0]);return new Promise(resolve=>waiting.push(resolve));}
106: """+queue+movement+"""
107: (async function(){
108:  const event=(x,y)=>({clientX:x,clientY:y,preventDefault:function(){}});
109:  down(event(0,0));move(event(20,10));await Promise.resolve();
110:  move(event(35,20));up(event(35,20));send('key=tab');
111:  down(event(0,0));up(event(0,0));
112:  if(events.join('|')!=='move=20,10')throw Error('drag sent a click or overtook motion');
113:  const expected=['move=20,10','move=15,10','key=tab','click=1'];
114:  for(let n=0;n<4;n++) {
115:   if(events[n]!==expected[n])throw Error('event ordering: '+events);
116:   waiting.shift()();await new Promise(r=>setImmediate(r));
117:  }
118:  if(events.length!==4)throw Error('drag produced unexpected events: '+events);
119:  console.log('PASS drag has no click and later key/tap preserve order');
120: })().catch(e=>{console.error(e.message);process.exitCode=1;});
121: """
122:   result=subprocess.run(['node','-e',program],text=True,capture_output=True)
123:   self.assertEqual(result.returncode,0,result.stderr)
124:  def test_original_source_negative_control(self):
125:   old=subprocess.check_output(['git','show','a1b0c65165:projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth'],cwd=ROOT,text=True)
126:   result=subprocess.run(['node','-e',self.program(old)],text=True,capture_output=True)
127:   self.assertNotEqual(result.returncode,0)
128:   self.assertIn('click overtook',result.stderr)
129: 
130: if __name__=='__main__': unittest.main(verbosity=2)



# FILE distribution/tools/test-fixtures/cloud_connections_fixture.py


## Original lines 1–43
1: """External-rclone adapter for the historical OAuth race fixtures.
2: 
3: The production transaction, locks, state guards and atomic writes run unchanged.
4: Only the fixture rclone's successful config-create side effect is simulated.
5: Real-rclone transactions are covered separately by cloud-connections-test.
6: """
7: import configparser
8: import io
9: from pathlib import Path
10: import sys
11: import subprocess
12: 
13: def configure(module, directory):
14:     c = module.connections
15:     root = Path(directory)
16:     c.CONFIG = root / 'rclone.conf'
17:     c.ACTIVE = root / 'active-connection'
18:     c.LOCK = root / 'cloud.lock'
19:     c.SYSTEM = root / 'system.cfg'
20:     def run(args):
21:         stage = Path(args[1])
22:         command = args[2:]
23:         if module.subprocess is subprocess and module.RCLONE == '/usr/bin/rclone':
24:             raise RuntimeError('OAuth fixture needs its fake provider')
25:         answer = module.subprocess.run([module.RCLONE] + command, capture_output=True, text=True)
26:         if answer.returncode:
27:             raise c.Refused('The connection could not be verified. Your settings were not changed.')
28:         if command[:2] == ['config', 'create']:
29:             parser = configparser.RawConfigParser()
30:             parser.read(stage)
31:             parser.add_section(command[2])
32:             parser.set(command[2], 'type', command[3])
33:             with stage.open('w') as stream: parser.write(stream)
34:         return answer.stdout
35:     c.run = run
36:     if hasattr(module, 'main'):
37:         original = module.main
38:         def main(argv):
39:             try: return original(argv)
40:             except c.Refused as error:
41:                 sys.stderr.write(str(error) + '\n')
42:                 return 2
43:         module.main = main



# FILE emulationstation/es-app/src/ApiSystem.cpp


## Original lines 450–510
450: 	LOG(LogDebug) << "ApiSystem::canUpdate";
451:     // Manual adoption in pixelelated0.0.1, including inherited force settings.
452:     if (getApplicationName() == "pixelelated")
453:         return false;
454: 
455: 	FILE *pipe = popen("rocknix-update check", "r");
456: 	if (pipe == NULL)
457: 		return false;
458: 
459: 	char line[1024];
460: 	while (fgets(line, 1024, pipe)) 
461: 	{
462: 		strtok(line, "\n");
463: 		output.push_back(std::string(line));
464: 	}
465: 
466: 	int res = WEXITSTATUS(pclose(pipe));
467: 	bool ForceUpdateEnabled = SystemConf::getInstance()->getBool("updates.force");
468: 	if (res == 0 || ForceUpdateEnabled == true)
469: 	{
470: 		LOG(LogInfo) << "Can update ";
471: 		return true;
472: 	}
473: 
474: 	LOG(LogInfo) << "Cannot update ";
475: 	return false;
476: }
477: 
478: void ApiSystem::launchExternalWindow_before(Window *window) 
479: {
480: 	LOG(LogDebug) << "ApiSystem::launchExternalWindow_before";
481: 
482: 	AudioManager::getInstance()->deinit();
483: 	VolumeControl::getInstance()->deinit();
484: 	window->deinit();
485: 
486: 	LOG(LogDebug) << "ApiSystem::launchExternalWindow_before OK";
487: }
488: 
489: void ApiSystem::launchExternalWindow_after(Window *window) 
490: {
491: 	LOG(LogDebug) << "ApiSystem::launchExternalWindow_after";
492: 
493: 	Utils::FileSystem::FileSystemCache::reset();
494: 
495: 	window->init();
496: 	VolumeControl::getInstance()->init();
497: 	AudioManager::getInstance()->init();
498: 	window->normalizeNextUpdate();
499: 	window->reactivateGui();
500: 
501: 	AudioManager::getInstance()->playRandomMusic();
502: 
503: 	LOG(LogDebug) << "ApiSystem::launchExternalWindow_after OK";
504: }
505: 
506: #ifdef BATOCERA
507: void ApiSystem::launchControlcenter() {
508:   system("batocera-controlcenter");
509: }
510: #endif

## Original lines 1410–1520
1410: 	}
1411: 
1412: 	return std::pair<std::string, int>(std::string(""), 1);
1413: }
1414: 
1415: std::pair<std::string, int> ApiSystem::uninstallBatoceraTheme(std::string thname, const std::function<void(const std::string)>& func)
1416: {
1417: 	for (auto theme : getBatoceraThemesList())
1418: 	{
1419: 		if (!theme.isInstalled || theme.name != thname)
1420: 			continue;
1421: 
1422: 		std::string installFolder = Paths::getUserThemesPath();
1423: 		if (installFolder.empty())
1424: 			installFolder = Paths::getThemesPath();
1425: 		if (installFolder.empty())
1426: 			installFolder = Paths::getUserEmulationStationPath() + "/themes";
1427: 
1428: 		std::string themeFileName = Utils::FileSystem::getFileName(theme.url);
1429: 
1430: 		std::string folderName = installFolder + "/" + themeFileName;
1431: 		if (!Utils::FileSystem::exists(folderName))
1432: 			folderName = folderName + "-master";
1433: 
1434: 		if (Utils::FileSystem::exists(folderName))
1435: 		{
1436: 			Utils::FileSystem::deleteDirectoryFiles(folderName, true);
1437: 			return std::pair<std::string, int>("OK", 0);
1438: 		}
1439: 
1440: 		break;
1441: 	}
1442: 
1443: 	return std::pair<std::string, int>(std::string(""), 1);
1444: }
1445: 
1446: std::vector<BatoceraBezel> ApiSystem::getBatoceraBezelsList()
1447: {
1448: 	LOG(LogInfo) << "ApiSystem::getBatoceraBezelsList";
1449: 
1450: 	std::vector<BatoceraBezel> res;
1451: 
1452: 	auto lines = executeEnumerationScript("rocknix-es-thebezelproject list");
1453: 	for (auto line : lines)
1454: 	{
1455: 		auto parts = Utils::String::splitAny(line, " \t");
1456: 		if (parts.size() < 2)
1457: 			continue;
1458: 
1459: 		if (!Utils::String::startsWith(parts[0], "[I]") && !Utils::String::startsWith(parts[0], "[A]"))
1460: 			continue;
1461: 
1462: 		BatoceraBezel bz;
1463: 		bz.isInstalled = (Utils::String::startsWith(parts[0], "[I]"));
1464: 		bz.name = parts[1];
1465: 		bz.url = parts.size() < 3 ? "" : (parts[2] == "-" ? parts[3] : parts[2]);
1466: 		bz.folderPath = parts.size() < 4 ? "" : parts[3];
1467: 
1468: 		if (bz.name != "?")
1469: 			res.push_back(bz);
1470: 	}
1471: 
1472: 	return res;
1473: }
1474: 
1475: std::pair<std::string, int> ApiSystem::installBatoceraBezel(std::string bezelsystem, const std::function<void(const std::string)>& func)
1476: {
1477: 	return executeScript("rocknix-es-thebezelproject install " + bezelsystem, func);
1478: }
1479: 
1480: std::pair<std::string, int> ApiSystem::uninstallBatoceraBezel(std::string bezelsystem, const std::function<void(const std::string)>& func)
1481: {
1482: 	return executeScript("rocknix-es-thebezelproject remove " + bezelsystem, func);
1483: }
1484: 
1485: std::string ApiSystem::getMD5(const std::string fileName, bool fromZipContents)
1486: {
1487: 	LOG(LogDebug) << "getMD5 >> " << fileName;
1488: 
1489: 	// 7za x -so test.7z | md5sum
1490: 	std::string ext = Utils::String::toLower(Utils::FileSystem::getExtension(fileName));
1491: 	if (ext == ".zip" && fromZipContents)
1492: 	{
1493: 		Utils::Zip::ZipFile file;
1494: 		if (file.load(fileName))
1495: 		{
1496: 			std::string romName;
1497: 
1498: 			for (auto name : file.namelist())
1499: 			{
1500: 				if (Utils::FileSystem::getExtension(name) != ".txt" && !Utils::String::endsWith(name, "/"))
1501: 				{
1502: 					if (!romName.empty())
1503: 					{
1504: 						romName = "";
1505: 						break;
1506: 					}
1507: 
1508: 					romName = name;
1509: 				}
1510: 			}
1511: 
1512: 			if (!romName.empty())
1513: 				return file.getFileMd5(romName);
1514: 		}
1515: 	}
1516: 
1517: #if !WIN32
1518: 	if (fromZipContents && ext == ".7z")
1519: 	{
1520: 		auto cmd = getSevenZipCommand() + " x -so \"" + fileName + "\" | md5sum";



# FILE emulationstation/es-app/src/WifiText.cpp


## Original lines 1–265
1: #include "WifiText.h"
2: 
3: // Only a CR: the name is the rest of the line, spaces and all.
4: static std::string withoutCR(const std::string& line)
5: {
6: 	if (!line.empty() && line.back() == '\r')
7: 		return line.substr(0, line.size() - 1);
8: 	return line;
9: }
10: 
11: bool WifiText::parseSavedLine(const std::string& rawLine, SavedNetwork& network)
12: {
13: 	const std::string line = withoutCR(rawLine);
14: 	const size_t tab = line.rfind('\t');
15: 	if (tab == std::string::npos)
16: 		return false;
17: 
18: 	const std::string name = line.substr(0, tab);
19: 	const std::string flag = line.substr(tab + 1);
20: 	if (name.empty())
21: 		return false;
22: 
23: 	if (flag == "active")
24: 		network.inUse = true;
25: 	else if (flag == "saved")
26: 		network.inUse = false;
27: 	else
28: 		return false;
29: 
30: 	network.name = name;
31: 	return true;
32: }
33: 
34: static std::string savedField(const std::string& field)
35: {
36: 	std::string result;
37: 	for (size_t i = 0; i < field.size(); ++i)
38: 		if (field[i] == '\\' && i + 1 < field.size() && (field[i + 1] == '\\' || field[i + 1] == 't'))
39: 			result += field[++i] == 't' ? '\t' : '\\';
40: 		else result += field[i];
41: 	return result;
42: }
43: 
44: bool WifiText::parseSavedDetailsLine(const std::string& rawLine, SavedNetwork& network)
45: {
46: 	const std::string line = withoutCR(rawLine);
47: 	const size_t first = line.find('\t'), last = line.rfind('\t');
48: 	if (first == std::string::npos || first == last || line.find('\t', first + 1) != last)
49: 		return false;
50: 	const auto flag = line.substr(last + 1);
51: 	if (flag != "active" && flag != "saved") return false;
52: 	network.name = savedField(line.substr(0, first));
53: 	network.ssid = savedField(line.substr(first + 1, last - first - 1));
54: 	network.inUse = flag == "active";
55: 	return !network.name.empty() && !network.ssid.empty();
56: }
57: 
58: std::vector<WifiText::SavedNetwork> WifiText::profilesForSsid(const std::string& ssid, const std::vector<SavedNetwork>& saved)
59: {
60: 	std::vector<SavedNetwork> result;
61: 	for (const auto& profile : saved)
62: 		if ((profile.ssid.empty() ? profile.name : profile.ssid) == ssid)
63: 			result.push_back(profile);
64: 	return result;
65: }
66: 
67: std::string WifiText::preferredProfile(const std::string& ssid, const std::vector<SavedNetwork>& saved)
68: {
69: 	const auto matching = profilesForSsid(ssid, saved);
70: 	if (matching.size() == 1) return matching.front().name;
71: 	int active = 0;
72: 	std::string name, namesake;
73: 	for (const auto& profile : matching)
74: 	{
75: 		if (profile.name == ssid) namesake = profile.name;
76: 		if (profile.inUse) { ++active; name = profile.name; }
77: 		if (profile.inUse && profile.name == ssid) return profile.name;
78: 	}
79: 	if (active == 1) return name;
80: 	return active == 0 ? namesake : "";
81: }
82: 
83: std::vector<WifiText::SavedNetwork> WifiText::parseSaved(const std::vector<std::string>& lines)
84: {
85: 	std::vector<SavedNetwork> networks;
86: 	for (const auto& line : lines)
87: 	{
88: 		SavedNetwork network;
89: 		if (parseSavedLine(line, network))
90: 			networks.push_back(network);
91: 	}
92: 	return networks;
93: }
94: 
95: std::string WifiText::parseCurrent(const std::vector<std::string>& lines)
96: {
97: 	for (const auto& line : lines)
98: 	{
99: 		const std::string ssid = withoutCR(line);
100: 		if (!ssid.empty())
101: 			return ssid;
102: 	}
103: 	return "";
104: }
105: 
106: std::vector<WifiText::PickerRow> WifiText::pickerRows(const std::vector<std::string>& inRange, const std::vector<SavedNetwork>& saved, const std::string& current,
107: 	bool savedKnown, bool currentKnown)
108: {
109: 	// The device's network when `wifictl current` could not say: the saved
110: 	// list marks the profile that is active (#308 F-WF-03).
111: 	std::string joinedNow = current;
112: 	if (!currentKnown && savedKnown)
113: 		for (const auto& network : saved)
114: 			if (network.inUse)
115: 			{
116: 				joinedNow = network.ssid.empty() ? network.name : network.ssid;
117: 				break;
118: 			}
119: 
120: 	const bool detailed = [&saved] {
121: 		for (const auto& profile : saved) if (!profile.ssid.empty()) return true;
122: 		return false;
123: 	}();
124: 	auto isSaved = [&saved](const std::string& name) { return !profilesForSsid(name, saved).empty(); };
125: 
126: 	std::vector<PickerRow> rows;
127: 	auto listed = [&rows](const std::string& name)
128: 	{
129: 		for (const auto& row : rows)
130: 			if (row.name == name)
131: 				return true;
132: 		return false;
133: 	};
134: 
135: 	// The profile the device is on (#308 claude F-WF-12, gpt F-WF-03).
136: 	// wifictl speaks two names: current the SSID, saved and join a profile's
137: 	// name, and the two differ for a renamed profile or NetworkManager's
138: 	// "Home 1". So the connected row joins by a profile, in this order:
139: 	//   - the one named as its SSID, when that one is up;
140: 	//   - else the one profile that is up -- even beside a namesake that is
141: 	//     not: the name used to decide first, and an old "Home" left saved
142: 	//     beside the "Home 1" in use took the row's FORGET and JOIN (audit of
143: 	//     the fix round, gpt G2-E-app-01);
144: 	//   - else, with none up (the list's flags behind the join), the one
145: 	//     named as the SSID, as before.
146: 	// Two or more up and none of them named so (a second adapter: saved's
147: 	// ACTIVE is any adapter's, where current is this device's) is not
148: 	// guessed at, a namesake that is not up included -- it is the one
149: 	// profile known not to be this connection -- and the row joins by its
150: 	// name, as before.
151: 	std::string joinedProfile;
152: 	if (!joinedNow.empty() && savedKnown && !detailed)
153: 	{
154: 		int up = 0;
155: 		bool namedUp = false;
156: 		std::string theOneUp;
157: 		for (const auto& network : saved)
158: 			if (network.inUse)
159: 			{
160: 				up++;
161: 				theOneUp = network.name;
162: 				if (network.name == joinedNow)
163: 					namedUp = true;
164: 			}
165: 		if (namedUp)
166: 			joinedProfile = joinedNow;
167: 		else if (up == 1)
168: 			joinedProfile = theOneUp;
169: 		else if (up == 0 && isSaved(joinedNow))
170: 			joinedProfile = joinedNow;
171: 	}
172: 
173: 	if (detailed && savedKnown) joinedProfile = preferredProfile(joinedNow, saved);
174: 
175: 	if (!joinedNow.empty())
176: 	{
177: 		PickerRow row{ joinedNow, !joinedProfile.empty(), true, savedKnown };
178: 		row.profile = joinedProfile;
179: 		rows.push_back(row);
180: 	}
181: 
182: 	for (const auto& rawName : inRange)
183: 	{
184: 		const std::string name = withoutCR(rawName);
185: 		if (name.empty() || listed(name))
186: 			continue;
187: 		PickerRow row{ name, savedKnown && isSaved(name), false, savedKnown };
188: 		if (row.saved)
189: 			row.profile = preferredProfile(name, saved);
190: 		rows.push_back(row);
191: 	}
192: 	return rows;
193: }
194: 
195: bool WifiText::parseJoin(const std::vector<std::string>& lines)
196: {
197: 	for (const auto& rawLine : lines)
198: 		if (withoutCR(rawLine) == "joined")
199: 			return true;
200: 	return false;
201: }
202: 
203: WifiText::JoinFailure WifiText::joinFailure(int exitCode)
204: {
205: 	return exitCode == 2 ? JoinFailure::ServiceNotAnswering : JoinFailure::MayBeKey;
206: }
207: 
208: WifiText::ForgetOutcome WifiText::parseForget(const std::vector<std::string>& lines)
209: {
210: 	ForgetOutcome outcome;
211: 	for (const auto& rawLine : lines)
212: 	{
213: 		const std::string line = withoutCR(rawLine);
214: 		if (line == "forgotten")
215: 			outcome.forgotten = true;
216: 		else if (line == "disconnected" && outcome.forgotten)
217: 			outcome.disconnected = true;
218: 	}
219: 	return outcome;
220: }
221: 
222: WifiText::PressAction WifiText::pressAction(const PickerRow& row)
223: {
224: 	if (row.connected)
225: 		return PressAction::Join;
226: 	if (row.saved)
227: 		return PressAction::ChooseSaved;
228: 	if (!row.savedKnown)
229: 		return PressAction::CheckAgain;
230: 	return PressAction::AskKey;
231: }
232: 
233: WifiText::PressAction WifiText::manualAction(const std::string& name, const std::string& current, const std::vector<SavedNetwork>& saved, bool savedKnown)
234: {
235: 	if (!name.empty() && name == current)
236: 		return PressAction::Join;
237: 	for (const auto& network : saved)
238: 		if ((network.ssid.empty() ? network.name : network.ssid) == name)
239: 			return PressAction::Join;
240: 	if (!savedKnown)
241: 		return PressAction::CheckAgain;
242: 	return PressAction::AskKey;
243: }
244: 
245: // A row joins by its profile when it has one, and by its name when not --
246: // the connected row whose profile could not be told, which join then
247: // answers for itself.
248: std::string WifiText::joinName(const PickerRow& row)
249: {
250: 	return row.profile.empty() ? row.name : row.profile;
251: }
252: 
253: // A typed name is taken as a row would be: the network the device is on
254: // joins by its profile, anything else by the name as typed.
255: std::string WifiText::manualJoinName(const std::string& name, const std::string& current, const std::string& currentProfile)
256: {
257: 	if (!name.empty() && name == current && !currentProfile.empty())
258: 		return currentProfile;
259: 	return name;
260: }
261: 
262: std::string WifiText::joinedNotice(const std::string& name, const std::string& connectedWord)
263: {
264: 	return name + " : " + connectedWord;
265: }



# FILE emulationstation/es-app/src/WifiText.h


## Original lines 1–164
1: #pragma once
2: #ifndef ES_APP_WIFI_TEXT_H
3: #define ES_APP_WIFI_TEXT_H
4: 
5: // The pure text of the Wi-Fi rows (fork #191): what wifictl prints for the
6: // interface, read into values the pages can show, with nothing from the
7: // window, the settings or a script behind it, so es-unit-tests can hold the
8: // rules (es-app/tests/unit). The thin shells that run wifictl are in
9: // ApiSystem; the rows themselves are in GuiMenu.
10: //
11: // The setting wifi.ssid is the network the player configured last.
12: // NetworkManager keeps a profile for every network the device has joined and
13: // autoconnects to whichever remembered one is in range, so what the device is
14: // on and what the setting says are two different facts; these are the shapes
15: // wifictl reports the first in.
16: 
17: #include <string>
18: #include <vector>
19: 
20: namespace WifiText
21: {
22: 	// A network NetworkManager remembers, as one line of `wifictl saved`
23: 	// reads: <name><TAB>active or <name><TAB>saved.
24: 	struct SavedNetwork
25: 	{
26: 		std::string name;
27: 		bool inUse = false;
28: 		std::string ssid; // optional for legacy two-column readers
29: 	};
30: 
31: 	// One line of `wifictl saved`. False for a line that is not a network:
32: 	// no tab, an empty name, a flag that is neither word. A trailing CR is
33: 	// tolerated. The name keeps its case and every space in it -- a network's
34: 	// name is case-sensitive, and is what the player recognises it by -- and
35: 	// the flag is read after the last tab, so a tab inside a name still
36: 	// leaves the flag whole.
37: 	bool parseSavedLine(const std::string& line, SavedNetwork& network);
38: 	// Current wifictl saved --ssid: escaped profile, escaped SSID, state.
39: 	bool parseSavedDetailsLine(const std::string& line, SavedNetwork& network);
40: 	std::vector<SavedNetwork> profilesForSsid(const std::string& ssid, const std::vector<SavedNetwork>& saved);
41: 	std::string preferredProfile(const std::string& ssid, const std::vector<SavedNetwork>& saved);
42: 
43: 
44: 	// Every network in the lines, in the order given (nmcli puts the one in
45: 	// use first); lines that are not networks are passed over.
46: 	std::vector<SavedNetwork> parseSaved(const std::vector<std::string>& lines);
47: 
48: 	// The first line of `wifictl current`, the SSID the device is joined to;
49: 	// empty when there is none. Only a trailing CR is trimmed: a name may
50: 	// begin or end with a space.
51: 	std::string parseCurrent(const std::vector<std::string>& lines);
52: 
53: 	// A row of the Wi-Fi picker (fork #191; the maintainer's paradigm of
54: 	// 2026-09-15: the WI-FI NETWORK row -- WI-FI SSID until D-UI-071 renamed
55: 	// it for its new value -- is the network the device is on, the
56: 	// list behind it is what is in range, and a saved one joins with a
57: 	// press). Built by pickerRows from what `wifictl list` found, the
58: 	// profiles `wifictl saved` holds and the network `wifictl current`
59: 	// answered.
60: 	struct PickerRow
61: 	{
62: 		std::string name;
63: 		bool saved = false;
64: 		bool connected = false;
65: 		// Whether `saved` is an answer: false when `wifictl saved` could
66: 		// not be asked (#308 F-WF-03/06), and the row is then neither saved
67: 		// nor unsaved, only unknown.
68: 		bool savedKnown = true;
69: 		// The saved profile a press joins by, as `wifictl join` takes it;
70: 		// empty when the row has none known.
71: 		std::string profile;
72: 	};
73: 
74: 	// The rows in the order the list shows them: the network joined now
75: 	// first (added when the scan missed it -- a hidden network is joined and
76: 	// not listed), then the rest in the scan's order, empty names and repeats
77: 	// dropped, each marked saved when NetworkManager holds a profile for it.
78: 	// Saved networks out of range are not rows: this list is what can be
79: 	// joined from here; MANAGE SAVED NETWORKS lists them all. Names compare
80: 	// exactly, as NetworkManager does.
81: 	// savedKnown and currentKnown say whether `wifictl saved` and `wifictl
82: 	// current` answered (ApiSystem's two getters return it): an empty list
83: 	// and no list are different answers (#308 F-WF-03/06).
84: 	std::vector<PickerRow> pickerRows(const std::vector<std::string>& inRange, const std::vector<SavedNetwork>& saved, const std::string& current,
85: 		bool savedKnown = true, bool currentKnown = true);
86: 
87: 	// What a press on a row does, and what INPUT MANUALLY does with a name.
88: 	//
89: 	// The network the device is on is joined too, not taken on trust
90: 	// (#308 F-WF-05): the row was built from a snapshot, and the device may
91: 	// have dropped it or moved to another since. wifictl join answers
92: 	// "joined" at once for a profile that is active and brings back one that
93: 	// is not, so the press confirms or repairs, and the picker closes only
94: 	// on its answer. A network whose profile could not be asked about is
95: 	// asked about again, never taken for one with no profile: the key path
96: 	// (wifictl connect) deletes and rebuilds a profile of that name (#308
97: 	// F-WF-03/06).
98: 	//
99: 	// A saved network the device is not on is a choice, not a join (#318,
100: 	// D-UI-118, taken from ROCKNIX's own saved-Wi-Fi work): CONNECT with the
101: 	// key NetworkManager holds, or FORGET it. The connected row still joins
102: 	// at once -- the press confirms or repairs -- and a typed name that is
103: 	// saved still joins, since typing it is asking to join it.
104: 	enum class PressAction
105: 	{
106: 		Join,         // join by the profile NetworkManager holds (wifictl join)
107: 		ChooseSaved,  // a saved network not in use: CONNECT / FORGET / CANCEL
108: 		AskKey,       // a network with no profile: its key, then connect
109: 		CheckAgain    // whether it has a profile could not be asked: never assume it has none
110: 	};
111: 	PressAction pressAction(const PickerRow& row);
112: 	PressAction manualAction(const std::string& name, const std::string& current, const std::vector<SavedNetwork>& saved, bool savedKnown);
113: 
114: 	// The name `wifictl join` is handed for a row's press, and for a typed
115: 	// name (current is the connected row's name, currentProfile its
116: 	// profile).
117: 	std::string joinName(const PickerRow& row);
118: 	std::string manualJoinName(const std::string& name, const std::string& current, const std::string& currentProfile);
119: 
120: 	// The toast when the picker has joined a network, in the toast's shape
121: 	// (es-ui-style-guide.md: <glyph> <subject> : <outcome>): the name as
122: 	// NetworkManager has it, then the word the row uses for the same fact
123: 	// (#308 F-WF-08). The caller puts the glyph in front.
124: 	std::string joinedNotice(const std::string& name, const std::string& connectedWord);
125: 
126: 	// What `wifictl join` printed: "joined" once the saved network's profile
127: 	// is active. Anything else, or nothing, is not a join that happened.
128: 	bool parseJoin(const std::vector<std::string>& lines);
129: 
130: 	// What a join that did not happen means, from `wifictl join`'s exit code
131: 	// (#308 2-wifi claude F-WF-03, gpt F-WF-06): 2 is NetworkManager not
132: 	// answering -- nothing was tried, and the key is not in question; any
133: 	// other (1: the profile would not come up or is not saved, 124: the
134: 	// timeout's bound on the activation, 0 without "joined") may be the key.
135: 	enum class JoinFailure { ServiceNotAnswering, MayBeKey };
136: 	JoinFailure joinFailure(int exitCode);
137: 
138: 	// wifictl join's answer, as ApiSystem::joinWifiNetwork gives it: the
139: 	// exit code (0 joined; 1 not joined; 2 NetworkManager not answering;
140: 	// 124 the timeout's bound), in a type that does not turn into a bool.
141: 	// The call returned bool, true for joined, until #308 F-WF-03/06, and 0
142: 	// means joined now: a caller left testing it as a truth value would
143: 	// compile and read every join backwards (audit of the fixes, E2 claude
144: 	// G-E2-01). This one does not compile.
145: 	struct JoinAnswer
146: 	{
147: 		int code = 1;
148: 		bool joined() const { return code == 0; }
149: 	};
150: 
151: 	// What `wifictl forget` printed: "forgotten" when the profile went, then
152: 	// "disconnected" on a second line when it was the one in use. A
153: 	// "disconnected" with no "forgotten" before it is not a forget that
154: 	// happened; nothing printed is not one either -- a caller reads the
155: 	// word, not the absence of an error.
156: 	struct ForgetOutcome
157: 	{
158: 		bool forgotten = false;
159: 		bool disconnected = false;
160: 	};
161: 	ForgetOutcome parseForget(const std::vector<std::string>& lines);
162: }
163: 
164: #endif // ES_APP_WIFI_TEXT_H



# FILE emulationstation/es-app/src/guis/GuiMenu.cpp


## Original lines 5300–5810
5300: 			// empty content root, exclusions not loaded, no systems selected
5301: 			// for this device -- by exiting non-zero and printing why. Show
5302: 			// its words rather than inventing a summary of a refusal we did
5303: 			// not make: "No systems are selected for this device yet." used
5304: 			// to fall through to THIS DEVICE ALREADY MATCHES YOUR CLOUD,
5305: 			// which was false (#105).
5306: 			if (result.rc == CloudExit::NoNetwork)
5307: 			{
5308: 				window->pushGui(new GuiMsgBox(window, _("COULDN'T REACH YOUR CLOUD.\n\nTRY AGAIN WHEN YOU'RE ONLINE."), _("OK")));
5309: 				return;
5310: 			}
5311: 			bool refusal = false;
5312: 			std::string said;
5313: 			for (auto& raw : result.lines)
5314: 			{
5315: 				const std::string line = Utils::String::trim(raw);
5316: 				if (line.empty() || line.find('|') != std::string::npos)
5317: 					continue;   // a plan line, read below
5318: 				if (Utils::String::startsWith(line, "Refusing"))
5319: 					refusal = true;
5320: 				said += (said.empty() ? "" : "\n") + Utils::String::toUpper(line);
5321: 			}
5322: 			if (result.rc != 0 || refusal)
5323: 			{
5324: 				if (said.empty())
5325: 					said = _("COULDN'T READ YOUR CLOUD'S CONTENT.");
5326: 				window->pushGui(new GuiMsgBox(window, said + "\n\n" + _("NOTHING WAS CHANGED."), _("OK")));
5327: 				return;
5328: 			}
5329: 
5330: 			struct Change { std::string name; long files; long bytes; };
5331: 			std::vector<Change> changes;
5332: 			long totalFiles = 0, totalBytes = 0;
5333: 			for (auto& line : result.lines)
5334: 			{
5335: 				auto p = Utils::String::split(Utils::String::trim(line), '|', true);
5336: 				if (p.size() < 4)
5337: 					continue;
5338: 				long files = atol(p[2].c_str());
5339: 				if (files <= 0)
5340: 					continue;
5341: 				long bytes = atol(p[3].c_str());
5342: 				changes.push_back({ p[0], files, bytes });
5343: 				totalFiles += files;
5344: 				totalBytes += bytes;
5345: 			}
5346: 
5347: 			if (changes.empty())
5348: 			{
5349: 				window->pushGui(new GuiMsgBox(window,
5350: 					_("THIS DEVICE ALREADY MATCHES YOUR CLOUD.\n\nTHERE IS NOTHING TO REMOVE."), _("OK")));
5351: 				return;
5352: 			}
5353: 
5354: 			// Sizes are the transfer page's (GuiCloudTransfer::sizeLabel), as
5355: 			// on the picker rows and the done page this dialog leads to, so
5356: 			// the number a player agrees to here is the number they see
5357: 			// removed there. kiloBytesToString of a KB-rounded size read
5358: 			// "200.00 KB" -- two decimals that could only ever be zero (#85).
5359: 			std::string detail;
5360: 			for (auto& c : changes)
5361: 			{
5362: 				detail += Utils::String::toUpper(c.name) + "  -  "
5363: 					+ std::to_string(c.files) + " " + (c.files == 1 ? _("FILE") : _("FILES"));
5364: 				if (c.bytes > 0)
5365: 					detail += "  (" + GuiCloudTransfer::sizeLabel((unsigned long) c.bytes) + ")";
5366: 				detail += "\n";
5367: 			}
5368: 
5369: 			// Says what goes, what arrives, and what is never touched. The
5370: 			// third line matters most: this is the one action that can delete
5371: 			// a library, and somebody about to press YES needs to know their
5372: 			// saves are not in scope.
5373: 			std::string text = _("REMOVE") + std::string(" ") + std::to_string(totalFiles)
5374: 				+ " " + (totalFiles == 1 ? _("FILE FROM THIS DEVICE?") : _("FILES FROM THIS DEVICE?"));
5375: 			if (totalBytes > 0)
5376: 				text += "  (" + GuiCloudTransfer::sizeLabel((unsigned long) totalBytes) + ")";
5377: 			text += "\n\n" + detail
5378: 				+ "\n" + _("ANYTHING YOUR CLOUD HAS THAT THIS DEVICE DOES NOT IS DOWNLOADED AT THE SAME TIME.")
5379: 				+ "\n" + _("GAME SAVES, SAVE STATES, AND SCREENSHOTS ARE NEVER TOUCHED.");
5380: 
5381: 			window->pushGui(new GuiMsgBox(window, text, _("YES"), [window]
5382: 			{
5383: 				window->pushGui(new GuiCloudTransfer(window,
5384: 					"/usr/bin/cloud_content_restore --match --apply",
5385: 					_("MATCHING THIS DEVICE TO THE CLOUD")));
5386: 			}, _("NO"), nullptr));
5387: 		}));
5388: }
5389: 
5390: // The three rows of BACKUP AND RESTORE follow the transfer that is current
5391: // (CloudTransferJob::current). Built for a page that could be left with
5392: // its run going on (fork #187; the scan row under SCAN GAMES was the model,
5393: // audit #186 PL-07); since D-UI-078 the transfer page is sat in, so while
5394: // a run goes this hub is under it and is not ticked, and what these rows
5395: // meet is the run's outcome, kept current until the outcome page has been
5396: // dismissed (D-UI-070): LAST <date> - COMPLETED, then the row's own line
5397: // again. The running words (BACKING UP... - ITEM 2 OF 4 . NES) and the
5398: // press that opens the run's page remain for the seam -- a run that is
5399: // current with no page over it -- and are not a design anybody can reach
5400: // by pressing B (#258 PL-006). The other two rows dim meanwhile -- the scripts' flock refuses
5401: // a second run, so the only thing a press on them can do is show the one in
5402: // flight, which it does. Nothing here is written to disk: the scripts stamp
5403: // each part of a run as they always did (last-backup, last-content-restore,
5404: // ...), and the rows that read those stamps go on reading them. The line
5405: // returns to what the row does because that is the line the maintainer
5406: // chose for these rows (2026-09-06: a stamp on MATCH read as a third kind of
5407: // row beside two submenus); it changes only while there is a run to report.
5408: 
5409: // A hub row is dimmed while another row's run is in flight, by the entry
5410: // itself: ComponentList::render sets every element's colour every frame
5411: // from the theme, so a colour set once is gone by the first frame.
5412: // MultiLineMenuEntry::setDimmed does that (ComponentListFlags::dimmed, the
5413: // same 0x50), as the offline scan row in GuiRetroAchievementsSettings.cpp
5414: // uses it; the page's own subclass for it went (#308 8-es claude F-ES-25).
5415: // It applied the dim at the next frame, where setDimmed applies it at once;
5416: // nothing else differed.
5417: 
5418: // The three rows, held weakly as every row on a page is, each with the line
5419: // it returns to.
5420: struct CloudHubRows
5421: {
5422: 	struct Row
5423: 	{
5424: 		std::weak_ptr<MultiLineMenuEntry> entry;
5425: 		std::string idle;
5426: 	};
5427: 	Row backup, restore, match;
5428: };
5429: 
5430: // The line under the row that launched the run: in flight, the page's own
5431: // words for it (GuiCloudTransfer::rowWords) with the item where the panel
5432: // has room and the verb's word as the form that fits any panel (D-UI-035);
5433: // ended, the outcome dated the way every LAST row is. The description is
5434: // drawn in the menu's small font, in a row that spans the menu less its
5435: // insets; 0.86 of the menu width is what a 640x480 frame showed the line
5436: // to have (the scan row's measure).
5437: static std::string cloudTransferRowLine(const std::shared_ptr<CloudTransferJob>& job)
5438: {
5439: 	std::vector<std::string> candidates;
5440: 	if (!job->finished())
5441: 	{
5442: 		const GuiCloudTransfer::RowWords w = GuiCloudTransfer::rowWords(job);
5443: 		if (!w.item.empty())
5444: 			candidates.push_back(w.counted + "  ·  " + w.item);
5445: 		if (w.counted != w.word)
5446: 			candidates.push_back(w.counted);
5447: 		candidates.push_back(w.word);
5448: 	}
5449: 	else
5450: 	{
5451: 		const std::string outcome = GuiCloudTransfer::outcomeWord(job);
5452: 		candidates.push_back(cloudLastLabel(job->finishedAt()) + "  -  " + outcome);
5453: 		candidates.push_back(outcome);
5454: 	}
5455: 	auto theme = ThemeData::getMenuTheme();
5456: 	const float menuWidth = Renderer::ScreenSettings::fullScreenMenus()
5457: 		? (float) Renderer::getScreenWidth()
5458: 		: (float) Math::min((int) Renderer::getScreenHeight(), (int) (Renderer::getScreenWidth() * 0.90f));
5459: 	std::shared_ptr<Font> font = theme->TextSmall.font;
5460: 	return CloudText::chooseThatFits(candidates, menuWidth * 0.86f,
5461: 		[font](const std::string& t) { return font ? font->sizeText(t).x() : 0.0f; });
5462: }
5463: 
5464: static void cloudHubRefreshRow(CloudHubRows::Row& row, const std::shared_ptr<CloudTransferJob>& job, bool launchedHere)
5465: {
5466: 	auto entry = row.entry.lock();
5467: 	if (!entry)
5468: 		return;
5469: 	std::string text = row.idle;
5470: 	bool dimmed = false;
5471: 	if (job != nullptr)
5472: 	{
5473: 		if (launchedHere)
5474: 			text = cloudTransferRowLine(job);
5475: 		else
5476: 			dimmed = true;
5477: 	}
5478: 	entry->setDimmed(dimmed);
5479: 	// Only when the words change: the refresher asks once a second, and a
5480: 	// line set to itself would still lay the row out again.
5481: 	if (text != entry->getDescription())
5482: 		entry->setDescription(text);
5483: }
5484: 
5485: static void cloudHubRefresh(const std::shared_ptr<CloudHubRows>& rows)
5486: {
5487: 	const std::shared_ptr<CloudTransferJob> job = CloudTransferJob::current();
5488: 	const CloudText::TransferKind kind = job != nullptr
5489: 		? CloudText::transferKind(job->command()) : CloudText::TransferKind::Other;
5490: 	cloudHubRefreshRow(rows->backup,  job, kind == CloudText::TransferKind::Backup);
5491: 	cloudHubRefreshRow(rows->restore, job, kind == CloudText::TransferKind::Restore);
5492: 	cloudHubRefreshRow(rows->match,   job, kind == CloudText::TransferKind::Match);
5493: }
5494: 
5495: // The hub carries one component that is never drawn and never focused,
5496: // asks once a second while the hub is the top page, and refreshes the rows
5497: // -- which change their words only when they differ (cloudHubRefreshRow).
5498: // Owned by the page (EXTRACHILDREN: GuiComponent's destructor deletes it),
5499: // so it dies with the page; ticked by the page's update, which Window
5500: // gives to the top page alone, so the transfer page over it pauses it and
5501: // the rows catch up the second that page is dismissed -- which, with the
5502: // page sat in (D-UI-078), is when the run has ended and its outcome is
5503: // what there is to show. Built as the scan row's refresher was, for a run
5504: // nobody was watching (#187).
5505: class CloudHubRefresher : public GuiComponent
5506: {
5507: public:
5508: 	CloudHubRefresher(Window* window, const std::shared_ptr<CloudHubRows>& rows)
5509: 		: GuiComponent(window), mRows(rows), mElapsedMs(0)
5510: 	{
5511: 		setVisible(false);
5512: 		setExtraType(ExtraType::EXTRACHILDREN);
5513: 	}
5514: 
5515: 	void update(int deltaTime) override
5516: 	{
5517: 		GuiComponent::update(deltaTime);
5518: 		mElapsedMs += deltaTime;
5519: 		if (mElapsedMs < 1000)
5520: 			return;
5521: 		mElapsedMs = 0;
5522: 		cloudHubRefresh(mRows);
5523: 	}
5524: 
5525: private:
5526: 	std::shared_ptr<CloudHubRows> mRows;
5527: 	int mElapsedMs;
5528: };
5529: 
5530: // A row of BACKUP AND RESTORE: cloudAddGatedEntry's row -- the label over
5531: // one wrapped line, the action on A, the setup offer before a cloud is
5532: // connected -- as an entry the page keeps a weak hold of once the cloud is
5533: // connected, so its line can follow a run. A press while a run is current
5534: // opens the run's page: there is nothing else it can do (the flock), and
5535: // the page shows the run or its outcome.
5536: static void cloudAddTransferRow(GuiSettings* s, Window* window, bool configured, CloudHubRows::Row& slot,
5537: 	const std::string& label, const std::string& description, const std::function<void()>& action)
5538: {
5539: 	slot.idle = description;
5540: 	// One press for both branches: a row greyed at build time and set up
5541: 	// since runs this too (cloudAddGatedEntry re-checks at the press).
5542: 	const std::function<void()> press = [window, action]
5543: 	{
5544: 		if (const std::shared_ptr<CloudTransferJob> job = CloudTransferJob::current())
5545: 		{
5546: 			window->pushGui(new GuiCloudTransfer(window, job));
5547: 			return;
5548: 		}
5549: 		action();
5550: 	};
5551: 	if (!configured)
5552: 	{
5553: 		cloudAddGatedEntry(s, window, false, label, description, press);
5554: 		return;
5555: 	}
5556: 	auto entry = std::make_shared<MultiLineMenuEntry>(window, Utils::String::toUpper(label), description, true);
5557: 	slot.entry = entry;
5558: 	ComponentListRow row;
5559: 	row.addElement(entry, true);
5560: 	row.makeAcceptInputHandler(press);
5561: 	s->addRow(row);
5562: }
5563: 
5564: // The cloud hub. One page, reachable from one place.
5565: //
5566: // Cloud used to live in two menus: saves and content under GAME SETTINGS,
5567: // connection and system settings under NETWORK SETTINGS. Two of the three data
5568: // classes were in a different menu from the third, so "back up my handheld"
5569: // meant knowing which half of the split you wanted before you could start.
5570: // Direction first, then what moves -- the split the system actually keeps is
5571: // the one the player is shown.
5572: // A connection can change on a child page. Refresh its parent on return,
5573: // after the input callback has unwound; never rebuild a live button bar.
5574: class CloudConnectionsPage : public GuiSettings
5575: {
5576: public:
5577: 	CloudConnectionsPage(Window* window, const std::string& title, const std::function<void()>& refresh)
5578: 		: GuiSettings(window, title), mRefresh(refresh), mAlive(std::make_shared<bool>(true)),
5579: 		  mSnapshot(Utils::Platform::GetShOutput("/usr/bin/cloud_remote list")) { }
5580: 	~CloudConnectionsPage() override { *mAlive = false; }
5581: 	void topWindow(bool isTop) override
5582: 	{
5583: 		GuiSettings::topWindow(isTop);
5584: 		if (!isTop) return;
5585: 		auto alive = mAlive;
5586: 		mWindow->postToUiThread([this, alive]
5587: 		{
5588: 			if (!*alive || mWindow->peekGui() != this) return;
5589: 			const auto current = Utils::Platform::GetShOutput("/usr/bin/cloud_remote list");
5590: 			if (current == mSnapshot) return;
5591: 			mSnapshot = current;
5592: 			mRefresh();
5593: 			close();
5594: 		});
5595: 	}
5596: private:
5597: 	std::function<void()> mRefresh;
5598: 	std::shared_ptr<bool> mAlive;
5599: 	std::string mSnapshot;
5600: };
5601: 
5602: void GuiMenu::openCloud(Window* window, bool onFolderRow)
5603: {
5604: 	const bool configured = Utils::FileSystem::exists("/storage/.config/rclone/rclone.conf", false);
5605: 	auto s = new CloudConnectionsPage(window, _("CLOUD"), [window] { GuiMenu::openCloud(window); });
5606: 
5607: 	// The three rows follow the current transfer's outcome (D-UI-070; the
5608: 	// page is sat in since D-UI-078): see cloudAddTransferRow and the
5609: 	// refresher above.
5610: 	auto rows = std::make_shared<CloudHubRows>();
5611: 	s->addGroup(_("BACKUP AND RESTORE"));
5612: 	cloudAddTransferRow(s, window, configured, rows->backup, _("BACK UP TO THE CLOUD"),
5613: 		_("SEND THIS DEVICE'S DATA TO YOUR CLOUD."),
5614: 		[window] { cloudOpenTransfer(window, true); });
5615: 	cloudAddTransferRow(s, window, configured, rows->restore, _("RESTORE FROM THE CLOUD"),
5616: 		_("BRING DATA BACK ONTO THIS DEVICE."),
5617: 		[window] { cloudOpenTransfer(window, false); });
5618: 
5619: 	// The third action, and the only one that deletes. Below the two safe ones
5620: 	// deliberately: a destructive row above RESTORE would be the one a thumb
5621: 	// reaches first.
5622: 	if (Utils::FileSystem::exists("/usr/bin/cloud_content_restore"))
5623: 	{
5624: 		// Two lines (D-UI-023), and the same two as its siblings: a label and a
5625: 		// line saying what it does. This is the one row in the group that removes
5626: 		// something, so that is the line -- the preview then names every ROM.
5627: 		// It briefly carried its last-run stamp instead, which read as a third
5628: 		// kind of row beside two submenus (maintainer, 2026-09-06).
5629: 		cloudAddTransferRow(s, window, configured, rows->match, _("MATCH THIS DEVICE TO THE CLOUD"),
5630: 			_("REMOVE ROMS YOUR CLOUD NO LONGER HAS."), [window] { cloudOpenMatch(window); });
5631: 	}
5632: 	// Once now, so the first frame is right, then once a second while the
5633: 	// page is up.
5634: 	cloudHubRefresh(rows);
5635: 	s->addChild(new CloudHubRefresher(window, rows));
5636: 
5637: 	s->addGroup(_("SAVE MANAGEMENT"));
5638: 
5639: 	// The line under each toggle is how its sync last went, read from the
5640: 	// whole-run stamp ThreadedCloudSync leaves per cause (fork #94). The
5641: 	// card that shows the run is gone seconds after it ends, and a startup
5642: 	// sync runs while the player is looking at the boot splash or not at the
5643: 	// device at all -- so this row is where "did it run?" gets answered, and
5644: 	// it answers whether the toggle is on now or not: a stamp is a fact about
5645: 	// a run that happened. It replaced REQUIRES NETWORK ACCESS, which the
5646: 	// outcome says better when it matters (SKIPPED, NO NETWORK). Two lines,
5647: 	// never three (D-UI-023).
5648: 	auto cloud_startup = std::make_shared<SwitchComponent>(window);
5649: 	cloud_startup->setState(SystemConf::getInstance()->get("cloudsaves.startup") == "1");
5650: 	s->addWithDescription(_("SYNC SAVES DURING STARTUP"), cloudLastRunDetail("sync-startup"), cloud_startup);
5651: 	cloud_startup->setOnChangedCallback([cloud_startup] {
5652: 		SystemConf::getInstance()->set("cloudsaves.startup", cloud_startup->getState() ? "1" : "0");
5653: 		SystemConf::getInstance()->saveSystemConf();
5654: 	});
5655: 	auto cloud_gameexit = std::make_shared<SwitchComponent>(window);
5656: 	cloud_gameexit->setState(SystemConf::getInstance()->get("cloudsaves.gameexit") == "1");
5657: 	s->addWithDescription(_("SYNC SAVES WHEN EXITING A GAME"), cloudLastRunDetail("sync-exit"), cloud_gameexit);
5658: 	cloud_gameexit->setOnChangedCallback([cloud_gameexit] {
5659: 		SystemConf::getInstance()->set("cloudsaves.gameexit", cloud_gameexit->getState() ? "1" : "0");
5660: 		SystemConf::getInstance()->saveSystemConf();
5661: 	});
5662: 
5663: 	s->addGroup(_("CLOUD STORAGE SETUP"));
5664: 	if (configured)
5665: 	{
5666: 		// Who this device is connected to, and whether it answers.
5667: 		//
5668: 		// The page offered to connect a provider and never said one already
5669: 		// was: "there's nowhere where it shows what cloud backend you
5670: 		// currently have, which seems like a miss" (maintainer, 2026-09-10,
5671: 		// fork #110). The name is the player's own label for the remote when
5672: 		// they gave it one, otherwise the provider's name.
5673: 		//
5674: 		// One cloud_setup --info for the page: it runs rclone listremotes, a
5675: 		// route lookup and systemctl, synchronously on the interface thread,
5676: 		// and the page asked it three times -- once for a name nothing read
5677: 		// (#308 8-es claude F-ES-03).
5678: 		std::map<std::string, std::string> info = cloudSetupInfo();
5679: 		const std::string provider = CloudText::providerLabel(info["REMOTE_TYPE"]);
5680: 		if (!provider.empty())
5681: 			s->addWithLabel(_("CONNECTED TO"), std::make_shared<TextComponent>(window, provider,
5682: 				ThemeData::getMenuTheme()->Text.font, ThemeData::getMenuTheme()->Text.color));
5683: 
5684: 		// The thing to reach for when a sync has just failed: does the cloud
5685: 		// answer right now? Behind GuiLoading, because it is a network round
5686: 		// trip -- bounded by the script (a single listing, 10 s to connect,
5687: 		// 30 s to answer), so the page cannot hang on it.
5688: 		s->addWithDescription(_("CHECK CONNECTION"), _("SEE WHETHER YOUR CLOUD ANSWERS RIGHT NOW."), nullptr,
5689: 			[window, provider]
5690: 			{
5691: 				window->pushGui(new GuiLoading<int>(window, _("CHECKING YOUR CLOUD..."),
5692: 					[](auto gui)
5693: 					{
5694: 						return ApiSystem::executeScriptLegacy("/usr/bin/cloud_setup --check", [](const std::string) {}).second;
5695: 					},
5696: 					[window, provider](int rc)
5697: 					{
5698: 						const std::string who = provider.empty() ? _("YOUR CLOUD") : provider;
5699: 						std::string text;
5700: 						if (rc == 0)
5701: 							text = who + " " + _("ANSWERED. YOU'RE CONNECTED.");
5702: 						else if (rc == 1)
5703: 							text = _("NO CLOUD STORAGE IS SET UP ON THIS DEVICE YET.");
5704: 						else
5705: 							text = _("COULDN'T REACH") + " " + who + ".\n\n"
5706: 								+ _("CHECK WI-FI, THEN TRY AGAIN. IF IT KEEPS FAILING, SIGN IN AGAIN UNDER CLOUD CONNECTIONS.");
5707: 						window->pushGui(new GuiMsgBox(window, text, _("OK")));
5708: 					}));
5709: 			}, "", false, true);
5710: 
5711: 
5712: 		// Each data root keeps its own selection. Returning from the editor
5713: 		// rebuilds this hub at the same row, so the next press stays here.
5714: 		const std::string syncpath = info["SAVES_REMOTE"];
5715: 		s->addWithDescription(_("CHANGE CLOUD FOLDER"),
5716: 			_("YOUR SAVES ARE IN:") + " " + syncpath,
5717: 			nullptr, [window, s] { cloudOpenFolderSettings(window, [window, s] { GuiMenu::openCloud(window, true); s->close(); }); },
5718: 			"", onFolderRow, true);
5719: 		s->addWithDescription(_("CHECK CLOUD FOLDERS"), _("CHECK THE FOLDERS YOU CHOOSE."), nullptr,
5720: 			[window] { cloudSetupShowDoneStep(window, "", nullptr); }, "", false, true);
5721: 	}
5722: 	s->addWithDescription(_("CLOUD CONNECTIONS"),
5723: 		_("ADD, CHOOSE, OR MANAGE YOUR CONNECTIONS."),
5724: 		nullptr, [window] { GuiMenu::openCloudConnections(window); }, "", false, true);
5725: 
5726: 	// Only while there is a restore to finish.
5727: 	// Read uncached: exists() remembers its answer for the session, and this
5728: 	// marker is written by a restore that ran after boot -- a cached "absent"
5729: 	// from startup hid the row until the next restart (guest b, 2026-09-13).
5730: 	if (Utils::FileSystem::exists("/storage/.config/.restore-finish-pending", false))
5731: 	{
5732: 		// One line under the label on both panels (D-UI-023; the budget is
5733: 		// noted at openRestoreRelink's DEVICE PASSWORD row).
5734: 		// FINISH from here finishes the restore, as it does from NETWORK
5735: 		// SETTINGS: the row exists only while the marker does, and passing
5736: 		// false -- from when the row was always there -- left the marker, so
5737: 		// the page came back at the next start after FINISH (#308 8a gpt
5738: 		// F-ES-06).
5739: 		s->addWithDescription(_("FINISH RESTORE PROCESS"),
5740: 			_("RE-ENTER THE PASSWORDS BACKUPS LEAVE OUT (WI-FI, ACCOUNTS, DEVICE)."), nullptr,
5741: 			[window] { GuiMenu::openRestoreRelink(window, true); }, "", false, true);
5742: 	}
5743: 
5744: 	window->pushGui(s);
5745: }
5746: 
5747: void GuiMenu::openGamesSettings()
5748: {
5749: 	Window* window = mWindow;
5750: 
5751: 	auto s = new GuiSettings(mWindow, _("GAME SETTINGS").c_str());
5752: 
5753: 	s->addGroup(_("TOOLS"));
5754: 
5755: 	// Game List Update
5756: 	s->addEntry(_("UPDATE GAMELISTS"), false, [this, window] { updateGameLists(window); });
5757: 
5758: 	s->addEntry(_("MOONLIGHT GAME STREAMING"), false, [this, window] { GuiMoonlight::show(mWindow); });
5759: 
5760: 	if (SystemConf::getInstance()->getBool("global.retroachievements") && !Settings::getInstance()->getBool("RetroachievementsMenuitem") && SystemConf::getInstance()->get("global.retroachievements.username") != "")
5761: 	{
5762: 		s->addEntry(_("RETROACHIEVEMENTS").c_str(), true, [this] 
5763: 		{ 
5764: 			if (!OfflineAchievements::proxyOffline() && !checkNetwork())
5765: 				return;
5766: 
5767: 			GuiRetroAchievements::show(mWindow); 
5768: 		});
5769: 	}
5770: 	
5771: 
5772: 	if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::RETROACHIVEMENTS) || (SystemData::isNetplayActivated() && ApiSystem::getInstance()->isScriptingSupported(ApiSystem::NETPLAY)))
5773: 		s->addGroup(_("ACCOUNTS"));
5774: 
5775: 	// Retroachievements
5776: 	if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::RETROACHIVEMENTS))
5777: 		s->addEntry(_("RETROACHIEVEMENTS SETTINGS"), true, [this] { openRetroachievementsSettings(); });
5778: 
5779: 	// Netplay
5780: 	if (SystemData::isNetplayActivated() && ApiSystem::getInstance()->isScriptingSupported(ApiSystem::NETPLAY))
5781: 		s->addEntry(_("NETPLAY SETTINGS"), true, [this] { openNetplaySettings(); }, "iconNetplay");
5782: 
5783: 	// Missing Bios
5784: 	if (ApiSystem::getInstance()->isScriptingSupported(ApiSystem::BIOSINFORMATION))
5785: 	{
5786: 		s->addGroup(_("BIOS SETTINGS"));
5787: 		s->addEntry(_("BIOS CHECK"), true, [this, s] { openMissingBiosSettings(); });
5788: 
5789: 		auto checkBiosesAtLaunch = std::make_shared<SwitchComponent>(mWindow);
5790: 		checkBiosesAtLaunch->setState(Settings::getInstance()->getBool("CheckBiosesAtLaunch"));
5791: 		s->addWithLabel(_("CHECK BIOS FILES BEFORE RUNNING A GAME"), checkBiosesAtLaunch);
5792: 		s->addSaveFunc([checkBiosesAtLaunch] { Settings::getInstance()->setBool("CheckBiosesAtLaunch", checkBiosesAtLaunch->getState()); });
5793: 	}
5794: 
5795: 	// Custom config for systems
5796: 	s->addGroup(_("SAVE STATES"));
5797: 
5798: 	// AUTO SAVE/LOAD
5799: 	auto autosave_enabled = std::make_shared<SwitchComponent>(mWindow);
5800: 	autosave_enabled->setState(SystemConf::getInstance()->get("global.autosave") == "1");
5801: 	s->addWithDescription(_("AUTO SAVE/LOAD"), _("Load latest save state on game launch and save state when exiting game."), autosave_enabled);
5802: 	s->addSaveFunc([autosave_enabled] { SystemConf::getInstance()->set("global.autosave", autosave_enabled->getState() ? "1" : ""); });
5803: 
5804: 	// INCREMENTAL SAVESTATES
5805: 	auto incrementalSaveStates = std::make_shared<OptionListComponent<std::string>>(mWindow, _("INCREMENTAL SAVE STATES"));
5806: 	// A device upgraded from before the row had two spellings can hold "0",
5807: 	// which matches no entry, so the row showed INCREMENT PER SAVE while the
5808: 	// launcher ran with auto-index off. "0" reads as DO NOT INCREMENT, which
5809: 	// is what it does (fork #209, D-UI-083); the row's next save writes "2".
5810: 	// The launcher that reads it is ROCKNIX's setsettings.sh, set_savestates:

## Original lines 6350–8200
6350: 	float height = 0;
6351: 	for (int i = 0; i < (int)lines.size(); i++)
6352: 	{
6353: 		auto tc = std::make_shared<TextComponent>(window, lines[i].first, theme->Text.font,
6354: 			lines[i].second ? theme->Text.selectedColor : theme->Text.color);
6355: 		tc->setPadding(CLOUD_SETUP_ROW_PADDING);
6356: 		tc->setVerticalAlignment(ALIGN_TOP);
6357: 		grid->setEntry(tc, Vector2i(0, i), false, true);
6358: 
6359: 		// Absolute row heights, so the stack keeps its shape when
6360: 		// ComponentList later resizes it to the width left over beside the
6361: 		// image. A percentage would re-divide whatever height it was given.
6362: 		const float lineHeight = tc->getSize().y();
6363: 		grid->setRowHeight(i, lineHeight, false);
6364: 		height += lineHeight;
6365: 	}
6366: 
6367: 	grid->setSize(0, height);
6368: 	return grid;
6369: }
6370: 
6371: // An image with text beside it rather than under it.
6372: //
6373: // The sign-in page cannot scroll: every row on it is unselectable, so
6374: // ComponentList never moves its camera and anything past the fold is
6375: // unreachable rather than merely off-screen (which is why a QR stacked above
6376: // the address cut the address in half). Vertical space is therefore the
6377: // binding constraint, and a square code sitting alone on a wide row wastes
6378: // most of it. A row centres its elements vertically and gives fixed-width
6379: // ones their own column, so the code and its text share one row's height.
6380: // An image that keeps its own colour inside a menu row.
6381: //
6382: // ComponentList::render calls setColor(Text.color) on every element of every
6383: // row, every frame, and ImageComponent::setColor is setColorShift. So a QR
6384: // added to a row is tinted with the menu's muted text colour sixty times a
6385: // second, and setting the shift once at construction achieves nothing -- the
6386: // first cut of this did exactly that and the code stayed grey. The text
6387: // beside it kept its brightness only because it sits in a ComponentGrid,
6388: // whose setColor does not reach the labels inside.
6389: //
6390: // A QR is not text and must not be themed like text: a phone camera needs
6391: // black on white, and "dimmer than the address next to it" is the visible
6392: // form of that bug.
6393: class UntintedImageComponent : public ImageComponent
6394: {
6395: public:
6396: 	UntintedImageComponent(Window* window) : ImageComponent(window)
6397: 	{
6398: 		ImageComponent::setColorShift(0xFFFFFFFF);
6399: 	}
6400: 	void setColor(unsigned int /*color*/) override
6401: 	{
6402: 		ImageComponent::setColorShift(0xFFFFFFFF);
6403: 	}
6404: };
6405: 
6406: static void cloudSetupAddQrRow(GuiSettings* s, Window* window, const std::string& imagePath,
6407: 	const std::vector<std::pair<std::string, bool>>& lines)
6408: {
6409: 	ComponentListRow row;
6410: 	row.selectable = false;
6411: 
6412: 	// A share of the screen, not of the menu: the menu is capped at the
6413: 	// screen height, so this stays the same physical size on a wide panel
6414: 	// and a square one, and always leaves the majority of the width to text.
6415: 	const float qrEdge = Renderer::getScreenHeight() * 0.28f;
6416: 
6417: 	auto qr = std::make_shared<UntintedImageComponent>(window);
6418: 	qr->setOpacity(255);
6419: 	// Padding before setMaxSize -- ImageComponent folds it into the size it
6420: 	// reports, which is what the row measures the column by.
6421: 	qr->setPadding(CLOUD_SETUP_ROW_PADDING);
6422: 	qr->setImage(imagePath, false, MaxSizeInfo(qrEdge, qrEdge));
6423: 	qr->setMaxSize(qrEdge, qrEdge);
6424: 	row.addElement(qr, false);
6425: 
6426: 	row.addElement(cloudSetupTextStack(window, lines), true);
6427: 	s->addRow(row);
6428: }
6429: 
6430: // A blank row. Group headers butt straight against whatever precedes them,
6431: // which reads as cramped where a group follows body text rather than another
6432: // group. Small font, so it is one short line rather than a full gap.
6433: static void cloudSetupAddSpacer(GuiSettings* s, Window* window)
6434: {
6435: 	auto theme = ThemeData::getMenuTheme();
6436: 	ComponentListRow row;
6437: 	row.selectable = false;
6438: 	row.addElement(std::make_shared<TextComponent>(window, "", theme->TextSmall.font, theme->Text.color), true);
6439: 	s->addRow(row);
6440: }
6441: 
6442: // A label/value row: the same read-only fact shape the rest of the app
6443: // uses (see NETWORK SETTINGS' IP ADDRESS and the system information
6444: // page) - a label with the value as its right-hand component. Passing a
6445: // func makes the row actionable; without one it is a plain fact.
6446: static void cloudSetupAddFact(GuiSettings* s, Window* window, const std::string& label, const std::string& value, const std::function<void()>& func = nullptr)
6447: {
6448: 	auto theme = ThemeData::getMenuTheme();
6449: 	s->addWithLabel(label, std::make_shared<TextComponent>(window, value, theme->Text.font, theme->Text.color), false, func);
6450: }
6451: 
6452: // The sign-in pages that own a waiting `cloud_oauth serve` (#308 8a gpt
6453: // F-ES-17). A page handed on to the next one by cloudSetupPresent leaves
6454: // the session to it; a page that closes any other way -- EXIT, back -- is
6455: // the player leaving the sign-in, and the session is cancelled then rather
6456: // than left listening until its own 900-second timeout. The interface
6457: // thread only, like the pages.
6458: static std::set<GuiSettings*> sOAuthSessionPages;
6459: 
6460: static void cloudOAuthOwnSession(GuiSettings* s)
6461: {
6462: 	sOAuthSessionPages.insert(s);
6463: 	s->onFinalize([s]
6464: 	{
6465: 		if (sOAuthSessionPages.erase(s) == 0)
6466: 			return;   // handed on: the next page owns the session
6467: 		LOG(LogInfo) << "cloud_oauth: the sign-in was left; cancelling its session";
6468: 		Utils::Platform::runSystemCommand("/usr/bin/cloud_oauth cancel", "", nullptr);
6469: 	});
6470: }
6471: 
6472: // Show a freshly built wizard page: give it the standard large-menu
6473: // height (the cap MenuComponent::updateSize applies) so the window does
6474: // not jump between steps, push it, then close the page it replaces -
6475: // closing first would flash the menu underneath.
6476: static void cloudSetupPresent(Window* window, GuiSettings* s, GuiSettings* prev)
6477: {
6478: 	if (prev != nullptr)
6479: 		sOAuthSessionPages.erase(prev);   // handed on, not left
6480: 	if (!Renderer::ScreenSettings::fullScreenMenus())
6481: 	{
6482: 		float width = Renderer::getScreenWidth() * 0.90f;
6483: 		if (width > Renderer::getScreenHeight())
6484: 			width = (float)Renderer::getScreenHeight();
6485: 		s->getMenu().setSize(width, Renderer::getScreenHeight() * 0.75f);
6486: 	}
6487: 	window->pushGui(s);
6488: 	if (prev != nullptr)
6489: 		prev->close();
6490: }
6491: 
6492: // Bottom button row for a wizard page: EXIT SETUP on the left and,
6493: // once the step's check has passed, CONTINUE on the right - replacing
6494: // the default BACK button so each page offers exactly those two ways
6495: // out.
6496: static void cloudSetupSetButtons(GuiSettings* s, const std::function<void()>& onContinue)
6497: {
6498: 	s->getMenu().clearButtons();
6499: 	// One word each. A button bar is read at a glance and the page title
6500: 	// already says what is being exited, so "EXIT SETUP" spent width on a
6501: 	// word that carried nothing -- and the wider the buttons, the more two
6502: 	// of them read as a single control.
6503: 	s->getMenu().addButton(_("EXIT"), _("exit setup"), [s] { s->close(); });
6504: 	if (onContinue != nullptr)
6505: 		s->getMenu().addButton(_("CONTINUE"), _("continue"), onContinue);
6506: }
6507: 
6508: // View or change the SSH password; onDone runs after the page closes.
6509: static void cloudSetupOpenPasswordPage(Window* window, const std::string& current, const std::function<void()>& onDone)
6510: {
6511: 	auto pw = new GuiSettings(window, _("SSH PASSWORD"));
6512: 	cloudSetupAddFact(pw, window, _("CURRENT PASSWORD"), current.empty() ? _("<NOT SET>") : current);
6513: 	pw->addInputTextConfigRow(_("CHANGE PASSWORD"), "root.password", false);
6514: 	pw->addSaveFunc([current]
6515: 	{
6516: 		// Apply only a real change; running setrootpass with an
6517: 		// empty value would clear the device password.
6518: 		const std::string changed = SystemConf::getInstance()->get("root.password");
6519: 		if (!changed.empty() && changed != current)
6520: 		{
6521: 			SystemConf::getInstance()->saveSystemConf();
6522: 			LOG(LogInfo) << "cloud_setup wizard: applying new device password";
6523: 			Utils::Platform::runSystemCommand("setrootpass " + Utils::String::shellQuote(changed), "", nullptr); // fork #198
6524: 		}
6525: 	});
6526: 	pw->onFinalize(onDone);
6527: 	window->pushGui(pw);
6528: }
6529: 
6530: // Edit the cloud folder (SYNCPATH) the sync tools read from and write
6531: // to, without touching config files by hand. onDone runs after a
6532: // successful change.
6533: static void cloudSetupOpenPathEditor(Window* window, const std::string& title, const std::string& command,
6534: 	const std::string& current, const std::function<void()>& onDone)
6535: {
6536: 	auto save = [window, onDone, command, current](const std::string& value)
6537: 	{
6538: 		const std::string path = Utils::String::trim(value);
6539: 		if (path == current) return;
6540: 		if (path.empty())
6541: 		{
6542: 			window->pushGui(new GuiMsgBox(window, _("ENTER A CLOUD FOLDER PATH."), _("OK")));
6543: 			return;
6544: 		}
6545: 		using PathResult = std::pair<CloudText::FolderPathRefusal, int>;
6546: 		window->pushGui(new GuiLoading<PathResult>(window, _("CHECKING..."),
6547: 			[path, command](IGuiLoadingHandler*)
6548: 			{
6549: 				auto reason = CloudText::FolderPathRefusal::Unknown;
6550: 				const auto result = ApiSystem::executeScriptLegacy("timeout 30 /usr/bin/cloud_setup " + command
6551: 					+ " " + Utils::String::shellQuote(path), [&reason](const std::string& line)
6552: 					{
6553: 						const auto known = CloudText::folderPathRefusal(line);
6554: 						if (reason == CloudText::FolderPathRefusal::Unknown)
6555: 							reason = known;
6556: 					});
6557: 				return PathResult(reason, result.second);
6558: 			},
6559: 			[window, onDone](PathResult result)
6560: 			{
6561: 				if (result.second != 0)
6562: 				{
6563: 					window->pushGui(new GuiMsgBox(window,
6564: 						_("THE CLOUD FOLDER WAS NOT CHANGED.") + "\n\n" +
6565: 						CloudText::folderPathRefusalMessage(result.first, result.second), _("OK")));
6566: 					return;
6567: 				}
6568: 				sCloudScanRun.clear();
6569: 				sCloudContentScanRun.clear();
6570: 				LOG(LogInfo) << "cloud_setup wizard: selected folder changed";
6571: 				if (onDone) onDone();
6572: 			}));
6573: 	};
6574: 	if (Settings::getInstance()->getBool("UseOSK"))
6575: 		window->pushGui(new GuiTextEditPopupKeyboard(window, title, current, save, false));
6576: 	else
6577: 		window->pushGui(new GuiTextEditPopup(window, title, current, save, false));
6578: }
6579: static void cloudSetupOpenSyncPathEditor(Window* window, const std::string& current, const std::function<void()>& onDone)
6580: {
6581: 	cloudSetupOpenPathEditor(window, _("SAVES FOLDER"), "--set-syncpath", current, onDone);
6582: }
6583: static void cloudOpenFolderSettings(Window* window, const std::function<void()>& onDone)
6584: {
6585: 	auto s = new GuiSettings(window, _("CLOUD FOLDERS"));
6586: 	auto info = cloudSetupInfo();
6587: 	cloudSetupAddProse(s, window, _("CHOOSE WHERE TO LOOK"),
6588: 		_("CHANGING A PATH DOES NOT MOVE YOUR FILES."));
6589: 	const std::vector<std::tuple<std::string, std::string, std::string>> folders = {
6590: 		{_("SAVES FOLDER"), "SAVES_REMOTE", "--set-syncpath"},
6591: 		{_("SETTINGS FOLDER"), "SETTINGS_REMOTE", "--set-settings-remote"},
6592: 		{_("ROMS, BIOS, AND GAME CONTENT FOLDER"), "CONTENT_REMOTE", "--set-content-remote"}
6593: 	};
6594: 	for (const auto& item : folders)
6595: 	{
6596: 		const auto title = std::get<0>(item), path = info[std::get<1>(item)], command = std::get<2>(item);
6597: 		s->addWithDescription(title, path, nullptr, [window, s, title, path, command, onDone]
6598: 		{
6599: 			const auto editorTitle = command == "--set-content-remote"
6600: 				? _("ROMS, BIOS, AND GAME CONTENT") : title;
6601: 			cloudSetupOpenPathEditor(window, editorTitle, command, path, [window, s, onDone]
6602: 			{
6603: 				cloudOpenFolderSettings(window, onDone);
6604: 				s->onFinalize(nullptr);
6605: 				s->close();
6606: 			});
6607: 		}, "", false, true);
6608: 	}
6609: 	s->onFinalize(onDone);
6610: 	window->pushGui(s);
6611: }
6612: 
6613: // Run `cloud_setup --check [remote]` and hand (exit code, remote name) to
6614: // onResult on the UI thread. 0 = working, 1 = missing, 2 = unreachable.
6615: // The only slow call in the wizard - a remote check can take up to the
6616: // rclone timeout - so the only one behind the GuiLoading spinner.
6617: static void cloudSetupRunCheck(Window* window, const std::string& remote, const std::function<void(int, const std::string&)>& onResult)
6618: {
6619: 	std::string cmd = "/usr/bin/cloud_setup --check";
6620: 	if (!remote.empty())
6621: 		cmd += " " + remote;
6622: 	window->pushGui(new GuiLoading<std::pair<int, std::string>>(window, _("CHECKING..."),
6623: 		[cmd](auto gui)
6624: 		{
6625: 			std::string out = Utils::String::trim(Utils::Platform::GetShOutput(cmd + "; echo RC=$?"));
6626: 			int rc = 1;
6627: 			auto pos = out.rfind("RC=");
6628: 			if (pos != std::string::npos)
6629: 			{
6630: 				rc = atoi(out.substr(pos + 3).c_str());
6631: 				out = Utils::String::trim(out.substr(0, pos));
6632: 			}
6633: 			std::string name = out.find(' ') != std::string::npos ? out.substr(out.find(' ') + 1) : "";
6634: 			LOG(LogInfo) << "cloud_setup wizard: --check rc=" << rc << " remote=" << name;
6635: 			return std::pair<int, std::string>(rc, name);
6636: 		},
6637: 		[onResult](std::pair<int, std::string> result)
6638: 		{
6639: 			onResult(result.first, result.second);
6640: 		}));
6641: }
6642: 
6643: // Step 1 of 3: SSH must be reachable - a device password and a running
6644: // SSH service, checked together on one page. Each actionable row is
6645: // marked with its state; CONTINUE appears once both checks pass.
6646: static void cloudSetupShowSshStep(Window* window, CloudSetupMode mode, const std::string& remote, const std::string& preexisting, GuiSettings* prev)
6647: {
6648: 	auto info = cloudSetupInfo();
6649: 	if (info["IP"].empty())
6650: 	{
6651: 		window->pushGui(new GuiMsgBox(window, _("NO NETWORK CONNECTION DETECTED.\n\nCONNECT TO A NETWORK FIRST, THEN TRY AGAIN.")));
6652: 		return;
6653: 	}
6654: 
6655: 	// cloud_setup --info says whether a password is set, never what it is:
6656: 	// a credential that crosses a script boundary is one careless echo from
6657: 	// a log (#116, D-INFRA-010). The value, where this page must show or
6658: 	// pre-fill it, is read in-process from the device's own settings.
6659: 	const bool pwOk = info["PASSWORD_SET"] == "1";
6660: 	const bool sshOk = info["SSH_UP"] == "active";
6661: 	LOG(LogInfo) << "cloud_setup wizard: step 1 ssh setup, password=" << pwOk << " sshd=" << info["SSH_UP"];
6662: 
6663: 	auto s = new GuiSettings(window, cloudSetupTitle(mode));
6664: 	s->setSubTitle(_("STEP 1 OF 3 - SET UP SSH"));
6665: 
6666: 	const std::string current = SystemConf::getInstance()->get("root.password");
6667: 	s->addEntry((pwOk ? _U("\uF058  ") : _U("\uF071  ")) + _("SET SSH PASSWORD"), true, [window, s, mode, remote, preexisting, current]
6668: 	{
6669: 		cloudSetupOpenPasswordPage(window, current, [window, s, mode, remote, preexisting]
6670: 		{
6671: 			cloudSetupShowSshStep(window, mode, remote, preexisting, s);
6672: 		});
6673: 	});
6674: 
6675: 	if (sshOk)
6676: 		cloudSetupAddInfoRow(s, window, _U("\uF058  ") + _("SSH SERVICE IS ENABLED"));
6677: 	else
6678: 		s->addEntry(_U("\uF071  ") + _("ENABLE SSH SERVICE"), true, [window, s, mode, remote, preexisting]
6679: 		{
6680: 			LOG(LogInfo) << "cloud_setup wizard: enabling sshd";
6681: 			Utils::Platform::runSystemCommand("mkdir -p /storage/.cache/services/", "", nullptr);
6682: 			Utils::Platform::runSystemCommand("touch /storage/.cache/services/sshd.conf", "", nullptr);
6683: 			Utils::Platform::runSystemCommand("systemctl enable sshd", "", nullptr);
6684: 			Utils::Platform::runSystemCommand("systemctl start sshd", "", nullptr);
6685: 			SystemConf::getInstance()->set("ssh.enabled", "1");
6686: 			SystemConf::getInstance()->saveSystemConf();
6687: 			cloudSetupShowSshStep(window, mode, remote, preexisting, s);
6688: 		});
6689: 
6690: 	std::function<void()> onContinue = nullptr;
6691: 	if (pwOk && sshOk)
6692: 		onContinue = [window, s, mode, remote, preexisting]
6693: 		{
6694: 			cloudSetupShowConnectStep(window, mode, remote, preexisting, s);
6695: 		};
6696: 	cloudSetupSetButtons(s, onContinue);
6697: 
6698: 	cloudSetupPresent(window, s, prev);
6699: }
6700: 
6701: // Step 2 of 3: connect from the computer; CONTINUE passes only when
6702: // --connected sees an established inbound SSH session.
6703: static void cloudSetupShowConnectStep(Window* window, CloudSetupMode mode, const std::string& remote, const std::string& preexisting, GuiSettings* prev)
6704: {
6705: 	auto info = cloudSetupInfo();
6706: 	LOG(LogInfo) << "cloud_setup wizard: step 2 connect, override=" << info["OVERRIDE"];
6707: 
6708: 	auto s = new GuiSettings(window, cloudSetupTitle(mode));
6709: 	s->setSubTitle(_("STEP 2 OF 3 - CONNECT FROM YOUR COMPUTER"));
6710: 
6711: 	s->addGroup(_("HOW TO CONNECT"));
6712: 	cloudSetupAddProse(s, window, _("ON YOUR COMPUTER"),
6713: 		_("OPEN A TERMINAL ON A COMPUTER ON THE SAME NETWORK, RUN THE COMMAND BELOW, AND ENTER THE PASSWORD WHEN ASKED."));
6714: 	cloudSetupAddInfoRow(s, window, info["SSH_CMD"], true);
6715: 
6716: 	cloudSetupAddSpacer(s, window);
6717: 	s->addGroup(_("CONNECTION DETAILS"));
6718: 	// Read in-process, not from the script (#116): this row exists so the
6719: 	// player can type the password into their computer's ssh prompt.
6720: 	const std::string current = SystemConf::getInstance()->get("root.password");
6721: 	cloudSetupAddFact(s, window, _("CURRENT PASSWORD"), current, [window, s, mode, remote, preexisting, current]
6722: 	{
6723: 		cloudSetupOpenPasswordPage(window, current, [window, s, mode, remote, preexisting]
6724: 		{
6725: 			cloudSetupShowConnectStep(window, mode, remote, preexisting, s);
6726: 		});
6727: 	});
6728: 	// With a connection override the direct address is not the one to
6729: 	// use, so showing it would only mislead.
6730: 	if (info["OVERRIDE"] != "1")
6731: 		cloudSetupAddFact(s, window, _("DEVICE IP"), info["IP"]);
6732: 
6733: 	cloudSetupSetButtons(s, [window, s, mode, remote, preexisting]
6734: 	{
6735: 		bool connected = Utils::String::trim(Utils::Platform::GetShOutput("/usr/bin/cloud_setup --connected")) == "CONNECTED";
6736: 		LOG(LogInfo) << "cloud_setup wizard: --connected=" << connected;
6737: 		if (connected)
6738: 		{
6739: 			cloudSetupShowConfigureStep(window, mode, remote, preexisting, s);
6740: 			return;
6741: 		}
6742: 		window->pushGui(new GuiMsgBox(window,
6743: 			_("THERE IS NO ACTIVE SSH CONNECTION TO THE DEVICE.\n\nTRY CONNECTING FROM YOUR COMPUTER AGAIN, LEAVE THE TERMINAL OPEN, AND THEN SELECT 'CONTINUE'."),
6744: 			_("OK"), nullptr,
6745: 			_("EXIT"), [s] { s->close(); }));
6746: 	});
6747: 
6748: 	cloudSetupPresent(window, s, prev);
6749: }
6750: 
6751: // Gate for the configure step: advance to the done step only when the
6752: // checked remote verifies; otherwise explain and stay (or exit).
6753: static void cloudSetupGateCheck(Window* window, GuiSettings* s, const std::string& remote)
6754: {
6755: 	cloudSetupRunCheck(window, remote, [window, s](int rc, const std::string& name)
6756: 	{
6757: 		if (rc == 0)
6758: 		{
6759: 			cloudSetupShowDoneStep(window, name, s);
6760: 		}
6761: 		else if (rc == 2)
6762: 			window->pushGui(new GuiMsgBox(window,
6763: 				_("THIS CONNECTION ISN'T ANSWERING:") + " " + cloudSetupDisplayName(name) + "\n\n" + _("ITS SIGN-IN MAY BE INCOMPLETE OR EXPIRED. IN THE TERMINAL, RUN:") + "\n'rclone config reconnect " + name + "'",
6764: 				_("OK"), nullptr,
6765: 				_("EXIT"), [s] { s->close(); }));
6766: 		else
6767: 			window->pushGui(new GuiMsgBox(window,
6768: 				_("NO CLOUD STORAGE IS SET UP ON THIS DEVICE YET.\n\nFINISH 'RCLONE CONFIG' IN THE TERMINAL, THEN SELECT 'CONTINUE' AGAIN."),
6769: 				_("OK"), nullptr,
6770: 				_("EXIT"), [s] { s->close(); }));
6771: 	});
6772: }
6773: 
6774: // Step 3 of 3: what to do inside the SSH session, as short numbered
6775: // steps branched by scenario; CONTINUE passes only when the remote
6776: // verifies via --check. The auto-config sign-in must go through the
6777: // step 2 tunnel - `rclone authorize` on the computer cannot bind its
6778: // port while that tunnel is open, so the instructions forbid it, and a
6779: // stale sign-in webserver on the device gets a clear-it action.
6780: static void cloudSetupShowConfigureStep(Window* window, CloudSetupMode mode, const std::string& remote, const std::string& preexisting, GuiSettings* prev)
6781: {
6782: 	auto info = cloudSetupInfo();
6783: 	LOG(LogInfo) << "cloud_setup wizard: step 3 configure, mode=" << (int)mode << " remote=" << remote << " auth_port=" << info["AUTH_PORT"];
6784: 
6785: 	auto s = new GuiSettings(window, cloudSetupTitle(mode));
6786: 
6787: 	if (mode == CloudSetupMode::RepairRemote)
6788: 	{
6789: 		s->setSubTitle(_("STEP 3 OF 3 - REPAIR THE CONNECTION"));
6790: 		s->addGroup(_("IN THE TERMINAL"));
6791: 		cloudSetupAddInfoRow(s, window, _("1. RUN 'rclone config reconnect ") + remote + "'");
6792: 		cloudSetupAddInfoRow(s, window, _("2. THAT RENEWS AN EXPIRED SIGN-IN."));
6793: 		cloudSetupAddInfoRow(s, window, _("3. FOR OTHER OPTIONS: RUN 'rclone config', PRESS 'E' TO EDIT."));
6794: 		cloudSetupAddInfoRow(s, window, _("4. PRESS 'Q' TO QUIT WHEN YOU ARE DONE."));
6795: 	}
6796: 	else
6797: 	{
6798: 		s->setSubTitle(_("STEP 3 OF 3 - CREATE THE CONNECTION"));
6799: 		s->addGroup(_("IN THE TERMINAL"));
6800: 		// Step 5 is the one people get wrong: rclone's own prompt says to
6801: 		// answer N on a machine with no browser, which describes this
6802: 		// handheld exactly. Answering N is fatal here.
6803: 		// Steps 6-7 describe what rclone actually does. There is no browser
6804: 		// on the device, so it always takes its "Failed to open browser
6805: 		// automatically ... please go to the following link" branch and
6806: 		// prints the URL to the terminal. Saying "the link in your browser"
6807: 		// implied one opens by itself and left people with nothing to click.
6808: 		cloudSetupAddInfoRow(s, window, _("1. RUN 'rclone config'"));
6809: 		cloudSetupAddInfoRow(s, window, _("2. PRESS 'N' FOR A NEW REMOTE (RCLONE'S WORD FOR A CONNECTION)"));
6810: 		cloudSetupAddInfoRow(s, window, _("3. NAME IT, PICK YOUR PROVIDER, TAKE DEFAULTS"));
6811: 		cloudSetupAddInfoRow(s, window, _("4. AT 'USE AUTO CONFIG?' PRESS 'Y'"));
6812: 		cloudSetupAddInfoRow(s, window, _("5. 'FAILED TO OPEN BROWSER' IS NORMAL HERE"));
6813: 		cloudSetupAddInfoRow(s, window, _("6. COPY THE LINK IT PRINTS INTO YOUR BROWSER"));
6814: 		cloudSetupAddInfoRow(s, window, _("7. SIGN IN, THEN PRESS 'Q' WHEN THE REMOTE IS LISTED"));
6815: 		// Kept short on purpose: this page has no selectable rows, so
6816: 		// ComponentList cannot scroll it (the camera follows the cursor,
6817: 		// and the cursor skips unselectable rows). Anything past the fold
6818: 		// is unreachable, so the text has to fit. Steps 5 and 6 already
6819: 		// say to answer 'Y' and sign in; the only new fact is the
6820: 		// 'rclone authorize' trap.
6821: 		s->addGroup(_("IMPORTANT"));
6822: 		cloudSetupAddProse(s, window, _("DO NOT USE 'rclone authorize'"),
6823: 			_("IT CANNOT BIND ITS PORT WHILE STEP 2'S CONNECTION IS OPEN."));
6824: 		if (mode == CloudSetupMode::AddRemote)
6825: 			cloudSetupAddInfoRow(s, window, _("NOTE: CLOUD SYNC USES THE FIRST REMOTE IN ALPHABETICAL ORDER."));
6826: 	}
6827: 
6828: 	if (info["AUTH_PORT"] == "busy")
6829: 		s->addEntry(_U("\uF071  ") + _("A STALE SIGN-IN IS BLOCKING THE PORT - PRESS TO CLEAR IT"), true, [window, s, mode, remote, preexisting]
6830: 		{
6831: 			LOG(LogInfo) << "cloud_setup wizard: freeing stale auth port";
6832: 			Utils::Platform::runSystemCommand("/usr/bin/cloud_setup --free-auth-port", "", nullptr);
6833: 			cloudSetupShowConfigureStep(window, mode, remote, preexisting, s);
6834: 		});
6835: 
6836: 	cloudSetupSetButtons(s, [window, s, mode, remote, preexisting]
6837: 	{
6838: 		if (mode == CloudSetupMode::AddRemote)
6839: 		{
6840: 			// The new remote is whichever name was not configured when the
6841: 			// wizard started - gate on that one, not the existing first.
6842: 			std::string newRemote;
6843: 			for (auto& name : Utils::String::split(cloudSetupInfo()["REMOTES"], ' '))
6844: 			{
6845: 				auto n = Utils::String::trim(name);
6846: 				if (!n.empty() && (" " + preexisting + " ").find(" " + n + " ") == std::string::npos)
6847: 					newRemote = n;
6848: 			}
6849: 			LOG(LogInfo) << "cloud_setup wizard: add-mode new remote=" << newRemote;
6850: 			if (newRemote.empty())
6851: 			{
6852: 				window->pushGui(new GuiMsgBox(window,
6853: 					_("NO NEW CONNECTION WAS ADDED YET.\n\nFINISH 'RCLONE CONFIG' IN THE TERMINAL, THEN SELECT 'CONTINUE' AGAIN."),
6854: 					_("OK"), nullptr,
6855: 					_("EXIT"), [s] { s->close(); }));
6856: 				return;
6857: 			}
6858: 			cloudSetupGateCheck(window, s, newRemote);
6859: 			return;
6860: 		}
6861: 		cloudSetupGateCheck(window, s, mode == CloudSetupMode::RepairRemote ? remote : "");
6862: 	});
6863: 
6864: 	cloudSetupPresent(window, s, prev);
6865: }
6866: 
6867: // Folder checks are explicit, selected-category reads. Linking alone does not
6868: // create anything or look outside the selected roots.
6869: static std::string cloudFolderCategoryLabel(const std::string& category)
6870: {
6871: 	if (category == "saves") return _("SAVES");
6872: 	if (category == "settings") return _("SETTINGS");
6873: 	if (category == "roms") return _("ROMS");
6874: 	if (category == "bios") return _("BIOS FILES");
6875: 	return _("GAME CONTENT");
6876: }
6877: static std::string cloudFolderStateLabel(const std::string& state)
6878: {
6879: 	if (state == "present") return _("FILES FOUND");
6880: 	if (state == "missing") return _("FOLDER MISSING");
6881: 	if (state == "empty") return _("NO FILES FOUND");
6882: 	if (state == "misplaced") return _("CHECK FILE LOCATIONS");
6883: 	return _("COULDN'T READ THIS FOLDER");
6884: }
6885: // Legacy line readers discard chunks longer than their line buffer. JSON is
6886: // a byte stream, and a populated five-category result can exceed that buffer.
6887: static std::pair<std::string, int> cloudReadFolderJson(const std::string& command)
6888: {
6889: 	FILE* pipe = popen(command.c_str(), "r");
6890: 	if (!pipe) return {"", -1};
6891: 	std::string json;
6892: 	char buffer[1024];
6893: 	bool bounded = true;
6894: 	std::size_t count;
6895: 	while ((count = fread(buffer, 1, sizeof(buffer), pipe)) != 0)
6896: 		if (bounded) bounded = CloudFolderValidation::appendOutput(json, buffer, count);
6897: 	const bool failed = ferror(pipe) != 0;
6898: 	const int status = pclose(pipe);
6899: 	if (!bounded || failed) json.clear();
6900: 	return {json, status != -1 && WIFEXITED(status) ? WEXITSTATUS(status) : -1};
6901: }
6902: static CloudFolderValidation::Context cloudFolderContext()
6903: {
6904: 	const auto output = cloudReadFolderJson("timeout 5 /usr/bin/cloud_setup --validation-context");
6905: 	return output.second == 0 ? CloudFolderValidation::parseContext(output.first) : CloudFolderValidation::Context();
6906: }
6907: static void cloudFolderInstructions(Window* window, const CloudFolderValidation::Category& item)
6908: {
6909: 	auto s = new GuiSettings(window, _("CLOUD FOLDER INSTRUCTIONS"));
6910: 	s->addGroup(cloudFolderCategoryLabel(item.category));
6911: 	cloudSetupAddProse(s, window, _("CLOUD FOLDER"), item.path);
6912: 	if (item.category == "roms")
6913: 		cloudSetupAddProse(s, window, _("ADD ROMS FROM A COMPUTER"),
6914: 			_("PUT EACH SYSTEM'S ROMS IN ITS OWN FOLDER HERE, SUCH AS nes OR gba. THEN CHECK AGAIN."));
6915: 	else if (item.category == "bios")
6916: 		cloudSetupAddProse(s, window, _("ADD BIOS FILES FROM A COMPUTER"),
6917: 			_("PUT YOUR BIOS FILES HERE, KEEPING THE NAMES AND SUBFOLDERS REQUIRED BY YOUR EMULATORS."));
6918: 	else if (item.category == "media")
6919: 		cloudSetupAddProse(s, window, _("ADD GAME CONTENT FROM A COMPUTER"),
6920: 			_("PUT EACH SYSTEM'S ARTWORK, VIDEOS, MANUALS, AND GAME LIST HERE IN ITS SYSTEM FOLDER."));
6921: 	else if (item.category == "saves")
6922: 		cloudSetupAddProse(s, window, _("ADD SAVES"),
6923: 			_("BACK UP GAME SAVES, SAVE STATES, AND SCREENSHOTS TO THIS FOLDER, OR COPY THEM HERE FROM A COMPUTER."));
6924: 	else
6925: 		cloudSetupAddProse(s, window, _("SETTINGS BACKUPS"),
6926: 			_("BACK UP SETTINGS TO POPULATE THIS FOLDER, OR COPY A SETTINGS BACKUP HERE FROM A COMPUTER."));
6927: 	cloudSetupAddProse(s, window, _("AFTER ADDING FILES"),
6928: 		_("CHECK FOLDERS AGAIN. THIS CHECK DOES NOT TEST FILE INTEGRITY OR GAME COMPATIBILITY."));
6929: 	window->pushGui(s);
6930: }
6931: static void cloudShowFolderResult(Window* window, const CloudFolderValidation::Result& result)
6932: {
6933: 	if (!result.valid)
6934: 	{
6935: 		window->pushGui(new GuiMsgBox(window,
6936: 			_("COULDN'T CHECK YOUR FOLDERS. CHECK YOUR CONNECTION, THEN TRY AGAIN."), _("OK")));
6937: 		return;
6938: 	}
6939: 	auto s = new GuiSettings(window, _("CLOUD FOLDER CHECK"));
6940: 	s->setSubTitle(result.complete ? _("COMPLETED") : _("COULDN'T FINISH"));
6941: 	cloudSetupAddProse(s, window, _("FOLDER LOCATIONS ONLY"),
6942: 		_("FILES FOUND DOES NOT MEAN THEY ARE COMPLETE OR COMPATIBLE."));
6943: 	for (const auto& item : result.categories)
6944: 	{
6945: 		s->addGroup(cloudFolderCategoryLabel(item.category));
6946: 		cloudSetupAddProse(s, window, cloudFolderStateLabel(item.state), item.path);
6947: 		s->addEntry(_("SEE INSTRUCTIONS"), true, [window, item] { cloudFolderInstructions(window, item); });
6948: 	}
6949: 	window->pushGui(s);
6950: }
6951: static void cloudCheckFolders(Window* window, const std::vector<std::string>& selected)
6952: {
6953: 	if (selected.empty())
6954: 	{
6955: 		window->pushGui(new GuiMsgBox(window, _("CHOOSE AT LEAST ONE ITEM TO CHECK."), _("OK")));
6956: 		return;
6957: 	}
6958: 	const std::string run = cloudNewCheckId();
6959: 	std::string csv;
6960: 	for (const auto& category : selected) csv += (csv.empty() ? "" : ",") + category;
6961: 	LOG(LogInfo) << "cloud_setup wizard: checking selected folders, run=" << run;
6962: 	window->pushGui(new GuiLoading<CloudFolderValidation::Result>(window, _("CHECKING YOUR CLOUD FOLDERS"),
6963: 		[selected, csv, run](IGuiLoadingHandler*)
6964: 	{
6965: 			const auto started = cloudFolderContext();
6966: 			if (!started.valid) return CloudFolderValidation::Result();
6967: 			const auto output = cloudReadFolderJson("timeout 35 /usr/bin/cloud_setup --validate-folders "
6968: 				+ Utils::String::shellQuote(csv) + " " + Utils::String::shellQuote(run));
6969: 			auto result = CloudFolderValidation::parseResult(output.first, run, started, cloudFolderContext(), selected);
6970: 			if (output.second != 0) result.complete = false;
6971: 			return result;
6972: 		}, [window](CloudFolderValidation::Result result) { cloudShowFolderResult(window, result); }));
6973: }
6974: static void cloudShowFolderSelection(Window* window, GuiSettings* prev, const std::vector<std::string>& selected)
6975: {
6976: 	auto s = new GuiSettings(window, _("CLOUD FOLDERS"));
6977: 	cloudSetupAddProse(s, window, _("CHOOSE FOLDERS"),
6978: 		_("SELECT WHAT TO CHECK OR CREATE FOLDERS FOR. THIS DOES NOT CHANGE AUTOMATIC SYNC."));
6979: 	const auto context = cloudFolderContext();
6980: 	auto switches = std::make_shared<std::vector<std::pair<std::string, std::shared_ptr<SwitchComponent>>>>();
6981: 	for (const auto& category : std::vector<std::string>{"saves", "settings", "roms", "bios", "media"})
6982: 	{
6983: 		auto toggle = std::make_shared<SwitchComponent>(window);
6984: 		toggle->setState(std::find(selected.begin(), selected.end(), category) != selected.end());
6985: 		switches->push_back({category, toggle});
6986: 		const auto path = context.paths.find(category);
6987: 		s->addWithDescription(cloudFolderCategoryLabel(category),
6988: 			path == context.paths.end() ? _("<NOT SET>") : path->second, toggle);
6989: 	}
6990: 	auto picked = [switches]
6991: 	{
6992: 		std::vector<std::string> selected;
6993: 		for (const auto& item : *switches) if (item.second->getState()) selected.push_back(item.first);
6994: 		return selected;
6995: 	};
6996: 	// A page describes the paths an action will use. Even an external settings
6997: 	// change must not turn a press on an old path into work somewhere else.
6998: 	auto stillSelected = [window, context]
6999: 	{
7000: 		const auto current = cloudFolderContext();
7001: 		if (context.valid && current.valid && context.configId == current.configId && context.paths == current.paths)
7002: 			return true;
7003: 		cloudCheckChanged(window);
7004: 		return false;
7005: 	};
7006: 	s->addGroup(_("FOLDER ACTIONS"));
7007: 	s->addEntry(_("CHECK FOLDERS"), true, [window, picked, stillSelected]
7008: 	{
7009: 		if (stillSelected()) cloudCheckFolders(window, picked());
7010: 	});
7011: 	s->addEntry(_("CREATE FOLDERS"), true, [window, picked, stillSelected]
7012: 	{
7013: 		if (!stillSelected()) return;
7014: 		const auto selected = picked();
7015: 		if (selected.empty())
7016: 		{
7017: 			window->pushGui(new GuiMsgBox(window, _("CHOOSE AT LEAST ONE ITEM TO CREATE FOLDERS FOR."), _("OK")));
7018: 			return;
7019: 		}
7020: 		std::string csv;
7021: 		for (const auto& category : selected) csv += (csv.empty() ? "" : ",") + category;
7022: 		window->pushGui(new GuiMsgBox(window,
7023: 			_("CREATE FOLDERS AND SETUP NOTES FOR THE ITEMS YOU CHOSE?\n\nYOUR FILES WILL NOT BE MOVED OR REORGANIZED."),
7024: 			_("YES"), [window, csv, selected, stillSelected]
7025: 			{
7026: 				if (!stillSelected()) return;
7027: 				auto page = new GuiCloudTransfer(window, "/usr/bin/cloud_setup --seed-folders "
7028: 					+ Utils::String::shellQuote(csv), _("CREATING CLOUD FOLDERS"), (int)selected.size());
7029: 				page->setAutoContinue([window, selected] { cloudCheckFolders(window, selected); });
7030: 				window->pushGui(page);
7031: 			}, _("NO"), nullptr));
7032: 	});
7033: 	s->addEntry(_("CHANGE CLOUD FOLDER"), true, [window, s, picked]
7034: 	{
7035: 		cloudOpenFolderSettings(window, [window, s, picked]
7036: 		{
7037: 			cloudShowFolderSelection(window, s, picked());
7038: 		});
7039: 	});
7040: 	s->getMenu().clearButtons();
7041: 	s->getMenu().addButton(_("FINISH"), _("finish"), [s] { s->close(); });
7042: 	cloudSetupPresent(window, s, prev);
7043: }
7044: static void cloudSetupShowDoneStep(Window* window, const std::string& remote, GuiSettings* prev)
7045: {
7046: 	const auto active = Utils::String::trim(Utils::Platform::GetShOutput("/usr/bin/cloud_remote active"));
7047: 	if (!remote.empty() && remote + (remote.back() == ':' ? "" : ":") != active)
7048: 	{
7049: 		auto s = new GuiSettings(window, _("CONNECTION SAVED"));
7050: 		cloudSetupAddProse(s, window, remote,
7051: 			_("YOUR CURRENT CONNECTION HAS NOT CHANGED. CHOOSE THIS CONNECTION UNDER CLOUD CONNECTIONS WHEN YOU WANT TO USE IT."));
7052: 		cloudSetupPresent(window, s, prev);
7053: 		return;
7054: 	}
7055: 	cloudShowFolderSelection(window, prev, {"saves", "settings"});
7056: }
7057: 
7058: 
7059: // Wizard entry point: network is a hard precondition; then branch on the
7060: // scenario - no remotes yet goes straight into the first-remote wizard,
7061: // otherwise offer check / add / repair-or-modify for the existing ones.
7062: // ---------------------------------------------------------------------------
7063: // Add a cloud remote without rclone's interactive configuration.
7064: //
7065: // `rclone config` asks its questions in a terminal, which on a handheld means
7066: // an SSH session from another computer -- a flow that fails in ways the player
7067: // cannot act on, and that needs a machine able to reach the device over the
7068: // LAN. `cloud_remote` asks rclone what a backend needs, we ask the player here,
7069: // and it writes the remote directly. See fork issue #51.
7070: //
7071: // Only backends that need no browser are offered. The rest keep the SSH
7072: // wizard, listed separately so nobody discovers three screens in that they
7073: // need an account somewhere else first.
7074: // ---------------------------------------------------------------------------
7075: 
7076: struct CloudBackend
7077: {
7078: 	std::string tier;         // keys | oauth | fallback | plumbing
7079: 	std::string name;         // rclone's backend id, e.g. "sftp"
7080: 	std::string label;        // human name, e.g. "SSH/SFTP Connection"
7081: 	std::string subprovider;  // vendor within the backend, where it has one
7082: 	bool reauthorize = false;
7083: };
7084: 
7085: struct CloudBackendField
7086: {
7087: 	std::string name;
7088: 	bool required = false;
7089: 	bool password = false;
7090: 	bool sensitive = false;
7091: 	std::string type;
7092: 	std::string deflt;
7093: 	std::string help;
7094: 	int choices = 0;
7095: };
7096: 
7097: // Backends worth putting in front of someone who has not decided yet. rclone
7098: // carries 69, most of which are plumbing (alias, chunker, combine, hasher,
7099: // memory) that is meaningless as a "cloud provider" choice.
7100: //
7101: // Each carries a short name of our own. rclone's descriptions are written for
7102: // its documentation, so "Amazon S3 Compliant Storage Providers including AWS,
7103: // Alibaba, ArvanCloud..." is accurate and useless on a handheld -- it is
7104: // truncated mid-word in a menu and tells the player nothing the first three
7105: // characters did not.
7106: // The table and the label it gives a provider live in CloudText, which is
7107: // where the pure cloud text is tested from (es-app/tests/unit): translated
7108: // at the point of use, since _() at static-init time would run before the
7109: // locale is loaded.
7110: 
7111: static std::vector<std::string> cloudRemoteLines(const std::string& args)
7112: {
7113: 	// GetShOutputLines, not GetShOutput: the latter drops the last character
7114: 	// of every chunk it reads, so multi-line output arrives as one
7115: 	// concatenated string. Parsing that yields a single nonsense record
7116: 	// rather than an error, which is how this first shipped -- the provider
7117: 	// list rendered empty with nothing logged.
7118: 	std::vector<std::string> lines;
7119: 	for (auto& line : Utils::Platform::GetShOutputLines("/usr/bin/cloud_remote " + args))
7120: 		if (!Utils::String::trim(line).empty())
7121: 			lines.push_back(line);
7122: 	return lines;
7123: }
7124: 
7125: static std::string cloudConnectionError(const std::string& output)
7126: {
7127: 	if (output.find("A cloud operation is running.") != std::string::npos)
7128: 		return _("A CLOUD OPERATION IS RUNNING. WAIT FOR IT TO FINISH, THEN TRY AGAIN.");
7129: 	if (output.find("Turn off both automatic") != std::string::npos)
7130: 		return _("TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS UNDER MANAGE CLOUD STORAGE BEFORE CHANGING THIS CONNECTION.");
7131: 	if (output.find("different connection name") != std::string::npos)
7132: 		return _("CHOOSE A DIFFERENT CONNECTION NAME.");
7133: 	if (output.find("Another connection uses") != std::string::npos)
7134: 		return _("ANOTHER CONNECTION USES THIS ONE. CHANGE THAT CONNECTION FIRST.");
7135: 	if (output.find("additional setup") != std::string::npos)
7136: 		return _("THIS PROVIDER NEEDS ADDITIONAL SETUP. USE A COMPUTER TO FINISH CONNECTING IT.");
7137: 	if (output.find("could not be verified") != std::string::npos || output.find("stopped answering") != std::string::npos)
7138: 		return _("THE CONNECTION DIDN'T ANSWER. CHECK ITS DETAILS AND YOUR NETWORK, THEN TRY AGAIN. YOUR SETTINGS HAVE NOT CHANGED.");
7139: 	return _("YOUR CLOUD SETTINGS COULD NOT BE READ OR SAVED. TRY AGAIN.");
7140: }
7141: 
7142: // Split a TSV record, keeping empty fields. removeEmptyEntries would drop
7143: // them, and most rows have an empty column somewhere -- a backend option with
7144: // no default, or no help text -- which shifts every later field left and
7145: // silently discards the row for being too short.
7146: static std::string cloudTsvField(const std::vector<std::string>& cols, size_t i)
7147: {
7148: 	return i < cols.size() ? cols[i] : std::string();
7149: }
7150: 
7151: static std::vector<CloudBackend> cloudRemoteBackends()
7152: {
7153: 	std::vector<CloudBackend> list;
7154: 	for (auto& line : cloudRemoteLines("providers"))
7155: 	{
7156: 		auto cols = Utils::String::splitAny(line, "\t", false);
7157: 		if (cols.size() < 3)
7158: 			continue;
7159: 		list.push_back({ cols[0], cols[1], cols[2], std::string() });
7160: 	}
7161: 	return list;
7162: }
7163: 
7164: // Shell-quote a value on its way to cloud_remote. Passwords and keys routinely
7165: // contain characters the shell would otherwise act on, and a mangled secret
7166: // fails in a way that looks like the provider rejecting the credential.
7167: static std::string cloudShellQuote(const std::string& value)
7168: {
7169: 	std::string quoted = "'";
7170: 	for (char c : value)
7171: 	{
7172: 		if (c == '\'')
7173: 			quoted += "'\\''";
7174: 		else
7175: 			quoted += c;
7176: 	}
7177: 	return quoted + "'";
7178: }
7179: 
7180: // Open an editor that reads the value from `values` rather than the copy
7181: // addInputTextRow captured when the row was built. Without this the second
7182: // edit of a field starts from the original value again.
7183: //
7184: // The obvious alternative -- rebuild the page after each edit -- is unsafe
7185: // here: GuiSettings::close() is `delete this`, and the callback doing the
7186: // rebuild is owned by the page being deleted.
7187: static std::function<void(Window*, std::string, std::string,
7188: 	const std::function<void(std::string)>&)>
7189: cloudRemoteEditor(std::shared_ptr<std::map<std::string, std::string>> values,
7190: 	const std::string& key)
7191: {
7192: 	return [values, key](Window* w, std::string title, std::string /*stale*/,
7193: 		const std::function<void(std::string)>& onsave)
7194: 	{
7195: 		std::string current = values->count(key) ? (*values)[key] : "";
7196: 		if (Settings::getInstance()->getBool("UseOSK"))
7197: 			w->pushGui(new GuiTextEditPopupKeyboard(w, title, current, onsave, false));
7198: 		else
7199: 			w->pushGui(new GuiTextEditPopup(w, title, current, onsave, false));
7200: 	};
7201: }
7202: 
7203: // One provider's questions.
7204: static void cloudRemoteShowForm(Window* window, const CloudBackend& backend,
7205: 	std::shared_ptr<std::map<std::string, std::string>> values, GuiSettings* prev)
7206: {
7207: 	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
7208: 	s->setSubTitle(CloudText::providerSubtitle(backend.name, backend.label));
7209: 
7210: 	std::vector<CloudBackendField> fields;
7211: 	// The backend id is quoted: rclone has ids with spaces in them
7212: 	// ("google cloud storage", "google photos"), which would otherwise split
7213: 	// into extra arguments.
7214: 	std::string fieldsArgs = "fields " + cloudShellQuote(backend.name);
7215: 	if (!backend.subprovider.empty())
7216: 		fieldsArgs += " " + cloudShellQuote(backend.subprovider);
7217: 	for (auto& line : cloudRemoteLines(fieldsArgs))
7218: 	{
7219: 		auto cols = Utils::String::splitAny(line, "\t", false);
7220: 		if (cols.size() < 5 || cols[0].empty())
7221: 			continue;
7222: 		CloudBackendField f;
7223: 		f.name      = cloudTsvField(cols, 0);
7224: 		f.required  = cloudTsvField(cols, 1) == "1";
7225: 		f.password  = cloudTsvField(cols, 2) == "1";
7226: 		f.sensitive = cloudTsvField(cols, 3) == "1";
7227: 		f.type      = cloudTsvField(cols, 4);
7228: 		f.deflt     = cloudTsvField(cols, 5);
7229: 		f.help      = cloudTsvField(cols, 6);
7230: 		f.choices   = atoi(cloudTsvField(cols, 7).c_str());
7231: 		fields.push_back(f);
7232: 	}
7233: 
7234: 	if (values->find("__name__") == values->end())
7235: 		(*values)["__name__"] = backend.name;
7236: 
7237: 	s->addGroup(_("NAME"));
7238: 	if (values->count("__edit__"))
7239: 	{
7240: 		cloudSetupAddFact(s, window, _("CONNECTION NAME"), (*values)["__name__"]);
7241: 		cloudSetupAddProse(s, window, _("EDIT CONNECTION"),
7242: 			_("BLANK FIELDS KEEP THEIR CURRENT VALUES."));
7243: 	}
7244: 	else s->addInputTextRow(_("CONNECTION NAME"), (*values)["__name__"], false,
7245: 		cloudRemoteEditor(values, "__name__"),
7246: 		[values](const std::string& newVal) { (*values)["__name__"] = newVal; });
7247: 
7248: 	// Required first: on a small panel the fold is close, and a required field
7249: 	// below it reads as absent rather than as further down.
7250: 	for (int pass = 0; pass < 2; pass++)
7251: 	{
7252: 		bool wantRequired = (pass == 0);
7253: 		bool headed = false;
7254: 		for (auto& f : fields)
7255: 		{
7256: 			if (f.required != wantRequired)
7257: 				continue;
7258: 			if (!headed)
7259: 			{
7260: 				s->addGroup(wantRequired ? _("REQUIRED") : _("OPTIONAL"));
7261: 				headed = true;
7262: 			}
7263: 			// Mask anything the backend calls a password or marks sensitive.
7264: 			// rclone's two flags do not agree on what a credential is -- it
7265: 			// marks sftp's host sensitive, and s3's secret_access_key
7266: 			// sensitive but not a password -- so masking either flag is the
7267: 			// only rule that never leaves a key on screen. Opening the row
7268: 			// still shows the value, which is the reveal.
7269: 			bool mask = f.password || f.sensitive;
7270: 			if (!values->count("__edit__") && !values->count(f.name) && !f.deflt.empty())
7271: 				(*values)[f.name] = f.deflt;
7272: 			std::string current = values->count(f.name) ? (*values)[f.name] : "";
7273: 			// The rclone name is the key the value is stored under; the row
7274: 			// shows CloudText::fieldLabel's words for it (#123).
7275: 			std::string fieldName = f.name;
7276: 
7277: 			// Match the widget to the option. Everything was a text box before,
7278: 			// which meant typing "true" for a switch, and guessing that the
7279: 			// answer for a generic WebDAV server is the literal string "other".
7280: 			if (f.type == "bool" && !values->count("__edit__"))
7281: 			{
7282: 				auto sw = std::make_shared<SwitchComponent>(window);
7283: 				sw->setState(current == "true");
7284: 				s->addWithLabel(CloudText::fieldLabel(fieldName), sw);
7285: 				sw->setOnChangedCallback([values, fieldName, sw]
7286: 				{
7287: 					(*values)[fieldName] = sw->getState() ? "true" : "false";
7288: 				});
7289: 				continue;
7290: 			}
7291: 
7292: 			// Only offer a list when it is short enough to scroll on a handheld.
7293: 			// s3's endpoint carries 351 suggestions and its region 150; those are
7294: 			// effectively free-form and stay as text.
7295: 			if (f.choices > 0 && f.choices <= 12 && !values->count("__edit__"))
7296: 			{
7297: 				std::string choicesArgs = "choices " + cloudShellQuote(backend.name)
7298: 					+ " " + cloudShellQuote(fieldName);
7299: 				if (!backend.subprovider.empty())
7300: 					choicesArgs += " " + cloudShellQuote(backend.subprovider);
7301: 
7302: 				auto list = std::make_shared<OptionListComponent<std::string>>(
7303: 					window, CloudText::fieldLabel(fieldName), false);
7304: 				bool any = false;
7305: 				for (auto& line : cloudRemoteLines(choicesArgs))
7306: 				{
7307: 					auto cols = Utils::String::splitAny(line, "\t", false);
7308: 					if (cols.empty() || cols[0].empty())
7309: 						continue;
7310: 					std::string value = cols[0];
7311: 					std::string label = cloudTsvField(cols, 1).empty() ? value : cols[1];
7312: 					list->add(label, value, current == value);
7313: 					any = true;
7314: 				}
7315: 				if (any)
7316: 				{
7317: 					// Seed the map with whatever the list starts on, and keep
7318: 					// it current as the choice changes.
7319: 					//
7320: 					// NOT addSaveFunc: those run from GuiSettings::save(),
7321: 					// which happens when the page closes. The CONNECT row builds
7322: 					// its command while the page is still open, so a value
7323: 					// left to save() never reaches it -- the chosen vendor was
7324: 					// dropped, silently and with a success dialog, because
7325: 					// WebDAV tolerates an empty one. On Sharepoint or
7326: 					// Nextcloud that is the wrong dialect, not a no-op.
7327: 					// getSelected() asserts that exactly one entry is
7328: 					// selected and abort()s otherwise, and nothing is
7329: 					// selected when the option has no default and so no
7330: 					// entry matched. getSelectedIndex() returns -1 instead.
7331: 					// Leaving it unset is right: we should not invent a
7332: 					// vendor the player did not choose.
7333: 					if (list->getSelectedIndex() >= 0)
7334: 						(*values)[fieldName] = list->getSelected();
7335: 					list->setSelectedChangedCallback(
7336: 						[values, fieldName](const std::string& picked)
7337: 						{
7338: 							(*values)[fieldName] = picked;
7339: 						});
7340: 					s->addWithLabel(CloudText::fieldLabel(fieldName), list);
7341: 					continue;
7342: 				}
7343: 			}
7344: 
7345: 			s->addInputTextRow(CloudText::fieldLabel(fieldName), current, mask,
7346: 				cloudRemoteEditor(values, fieldName),
7347: 				[values, fieldName](const std::string& newVal)
7348: 				{
7349: 					(*values)[fieldName] = newVal;
7350: 				});
7351: 		}
7352: 	}
7353: 
7354: 	s->addGroup(_("FINISH"));
7355: 	s->addEntry(values->count("__edit__") ? _("SAVE CONNECTION") : _("CONNECT"), true, [window, backend, values, s]
7356: 	{
7357: 		std::string name = Utils::String::trim((*values)["__name__"]);
7358: 		if (name.empty())
7359: 		{
7360: 			window->pushGui(new GuiMsgBox(window,
7361: 				_("GIVE THE CONNECTION A NAME FIRST."), _("OK"), nullptr));
7362: 			return;
7363: 		}
7364: 
7365: 		std::string cmd = std::string(values->count("__edit__") ? "update " : "create ") + cloudShellQuote(name) + " "
7366: 			+ cloudShellQuote(backend.name);
7367: 		// The sub-provider is a real config value, not just a filter.
7368: 		if (!backend.subprovider.empty())
7369: 			cmd += " " + cloudShellQuote("provider=" + backend.subprovider);
7370: 		for (auto& kv : *values)
7371: 		{
7372: 			if (Utils::String::startsWith(kv.first, "__") || Utils::String::trim(kv.second).empty())
7373: 				continue;
7374: 			cmd += " " + cloudShellQuote(kv.first + "=" + kv.second);
7375: 		}
7376: 
7377: 		window->pushGui(new GuiMsgBox(window,
7378: 			values->count("__edit__")
7379: 				? _("UPDATE THIS CONNECTION AND KEEP YOUR SELECTED FOLDERS?\n\nYOUR CURRENT SETTINGS ARE KEPT UNTIL THE NEW ONES WORK.")
7380: 				: _("CONNECT TO THIS PROVIDER NOW?\n\nTHE CONNECTION IS ONLY SAVED IF IT ANSWERS."),
7381: 			values->count("__edit__") ? _("UPDATE CONNECTION") : _("CONNECT"), [window, cmd, s]
7382: 			{
7383: 				// cloud_remote verifies private staged settings before publication;
7384: 				// failure keeps the existing connection. Its two subprocesses
7385: 				// are each bounded to 40 seconds, below this outer deadline. Behind GuiLoading, because that round trip
7386: 				// ran in this callback on the interface thread (fork #103);
7387: 				// the outer box is for an rclone that outlives its own flags.
7388: 				window->pushGui(new GuiLoading<std::string>(window, _("CONNECTING..."),
7389: 					[cmd](IGuiLoadingHandler*)
7390: 					{
7391: 						std::string out = Utils::Platform::GetShOutput(
7392: 							"timeout 100 /usr/bin/cloud_remote " + cmd + " 2>&1");
7393: 						// Masked: the command carries the form's pass=, key= and
7394: 						// token= values, and a script that echoes its arguments
7395: 						// in a usage or an error would put them in es_log.txt
7396: 						// (#308 8-es claude F-ES-21; fork #177's rule, every
7397: 						// logged command line).
7398: 						LOG(LogInfo) << "cloud_remote create: " << Utils::String::maskSecrets(out);
7399: 						return out;
7400: 					},
7401: 					[window, s](std::string out)
7402: 					{
7403: 						if (out.find("OK=") != std::string::npos)
7404: 						{
7405: 							const size_t start = out.find("OK=") + 3;
7406: 							const std::string remote = Utils::String::trim(out.substr(start, out.find_first_of("\r\n", start) - start));
7407: 							cloudSetupShowDoneStep(window, remote, s);
7408: 							return;
7409: 						}
7410: 						// Show what actually went wrong. The player can fix a
7411: 						// typo in a key far more easily than they can act on
7412: 						// "it failed".
7413: 						window->pushGui(new GuiMsgBox(window,
7414: 							_("THE CONNECTION COULDN'T BE SAVED.") + std::string("\n\n") +
7415: 								cloudConnectionError(out),
7416: 							_("OK"), nullptr));
7417: 					}));
7418: 			},
7419: 			_("NO"), nullptr));
7420: 	});
7421: 
7422: 	// prev->close(), never delete: the window owns it and is mid-input on it.
7423: 	cloudSetupPresent(window, s, prev);
7424: }
7425: 
7426: // Several backends ask which vendor you are using before their other
7427: // options mean anything: koofr carries three separate options all named
7428: // `password` (Koofr, Digi Storage, other) and s3 has 51 vendors with
7429: // options like ibm_api_key that are noise unless you picked IBMCOS.
7430: // Asking first keeps the form to the questions that apply.
7431: static void cloudRemoteChooseBackend(Window* window, const CloudBackend& backend)
7432: {
7433: 	std::vector<std::pair<std::string, std::string>> subs;
7434: 	for (auto& line : cloudRemoteLines("subproviders " + cloudShellQuote(backend.name)))
7435: 	{
7436: 		auto cols = Utils::String::splitAny(line, "\t", false);
7437: 		if (cols.size() < 1 || cols[0].empty())
7438: 			continue;
7439: 		subs.push_back({ cols[0], cloudTsvField(cols, 1).empty() ? cols[0] : cols[1] });
7440: 	}
7441: 
7442: 	if (subs.empty())
7443: 	{
7444: 		auto values = std::make_shared<std::map<std::string, std::string>>();
7445: 		cloudRemoteShowForm(window, backend, values, nullptr);
7446: 		return;
7447: 	}
7448: 
7449: 	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
7450: 	s->setSubTitle(_("WHICH SERVICE?"));
7451: 	for (auto& sub : subs)
7452: 	{
7453: 		CloudBackend chosen = backend;
7454: 		chosen.subprovider = sub.first;
7455: 		s->addEntry(Utils::String::toUpper(sub.second), true, [window, chosen]
7456: 		{
7457: 			auto values = std::make_shared<std::map<std::string, std::string>>();
7458: 			cloudRemoteShowForm(window, chosen, values, nullptr);
7459: 		});
7460: 	}
7461: 	cloudSetupPresent(window, s, nullptr);
7462: }
7463: 
7464: // Sign in to a provider using a phone, with nothing else involved.
7465: //
7466: // cloud_oauth starts rclone's own authorize flow, reads the provider's real
7467: // sign-in URL out of it, and serves that on the LAN behind a PIN. All this
7468: // page does is start it, show where to go, and ask rclone afterwards whether
7469: // it worked -- the same shape as the SSH wizard's CONTINUE gate, which exists
7470: // because a page that assumes success is how a failed setup gets reported as
7471: // a working one.
7472: struct CloudOAuthReady
7473: {
7474: 	bool started = false;
7475: 	bool onDevice = false;
7476: 	std::string url;
7477: 	std::string exitHint = "SELECT + START";
7478: };
7479: 
7480: static void cloudOAuthShowSignIn(Window* window, const CloudBackend& backend,
7481: 	const std::string& remoteName, GuiSettings* prev, bool usePhone,
7482: 	const CloudOAuthReady& ready);
7483: static void cloudOAuthPresentChoice(Window* window, const CloudBackend& backend,
7484: 	const std::string& remoteName, GuiSettings* prev,
7485: 	const CloudOAuthReady& ready);
7486: static void cloudOAuthShowConnected(Window* window, const CloudBackend& backend,
7487: 	const std::string& remoteName, GuiSettings* prev);
7488: static void cloudOAuthChooseInput(Window* window, const CloudBackend& backend,
7489: 	const std::string& remoteName, GuiSettings* prev);
7490: 
7491: static void cloudOAuthStart(Window* window, const CloudBackend& backend,
7492: 	const std::string& remoteName, GuiSettings* prev)
7493: {
7494: 	// Clear the previous attempt's state first, and wait for it: a finished
7495: 	// session leaves its address and PIN behind, and the poll below would
7496: 	// read those and put a dead code on the screen. Doing it here rather
7497: 	// than inside the detached launch means it has already happened before
7498: 	// the first poll, so there is no window where the old one is readable.
7499: 	Utils::Platform::runSystemCommand("/usr/bin/cloud_oauth cancel", "", nullptr);
7500: 
7501: 	// Detached, because it stays up until someone signs in or it times out.
7502: 	// Its own output carries the URL and PIN, which `cloud_oauth info` reads
7503: 	// back rather than this parsing them out of a launch.
7504: 	// --label carries the name we already show in our own menu, so the page
7505: 	// on the phone says "Connect Dropbox" rather than "Connect dropbox".
7506: 	// rclone's backend names are lowercase identifiers, and a page headed
7507: 	// with one reads like a typo on the screen where somebody is deciding
7508: 	// whether to trust us with their storage.
7509: 	std::string cmd = "setsid sh -c " + cloudShellQuote(
7510: 		"/usr/bin/cloud_oauth serve " + cloudShellQuote(backend.name)
7511: 		+ " --name " + cloudShellQuote(remoteName)
7512: 		+ " --label " + cloudShellQuote(backend.label)
7513: 		+ (backend.reauthorize ? " --replace" : "")
7514: 		+ " --timeout 900 >/dev/null 2>&1") + " </dev/null >/dev/null 2>&1 &";
7515: 	Utils::Platform::runSystemCommand(cmd, "", nullptr);
7516: 
7517: 	cloudOAuthChooseInput(window, backend, remoteName, prev);
7518: }
7519: 
7520: // Wait for the listener to say it is *waiting*, not merely for an address to
7521: // appear: a URL on its own proves nothing about whose session it belongs to,
7522: // which is how a previous attempt's PIN once reached the screen.
7523: static bool cloudOAuthAwaitSession(std::string& url, bool& onDevice,
7524: 	std::string& exitHint)
7525: {
7526: 	url.clear();
7527: 	onDevice = false;
7528: 	// A sane default for an image whose cloud_oauth predates EXIT_HINT.
7529: 	// Select exists on every pad we ship for; Mode does not.
7530: 	exitHint = "SELECT + START";
7531: 	bool understood = true;
7532: 
7533: 	// Sixty rather than twenty-four: this runs on a worker thread now, so
7534: 	// patience costs a spinner rather than a frozen screen, and a second
7535: 	// attempt after a cancel was timing out at the old limit.
7536: 	for (int attempt = 0; attempt < 60 && understood; attempt++)
7537: 	{
7538: 		std::string status;
7539: 		url.clear();
7540: 
7541: 		auto reported = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth info");
7542: 		// An older script answers `info` with its usage on stderr and nothing
7543: 		// on stdout. Fall through to `url` at once rather than spending the
7544: 		// whole poll waiting for a command that will never answer.
7545: 		understood = !reported.empty();
7546: 
7547: 		for (auto& line : reported)
7548: 		{
7549: 			const std::string trimmed = Utils::String::trim(line);
7550: 			if (Utils::String::startsWith(trimmed, "URL="))
7551: 				url = trimmed.substr(4);
7552: 			else if (Utils::String::startsWith(trimmed, "STATUS="))
7553: 				status = trimmed.substr(7);
7554: 			else if (Utils::String::startsWith(trimmed, "ON_DEVICE="))
7555: 				onDevice = trimmed.substr(10) == "yes";
7556: 			// Which two buttons leave differs by handheld, so the device is
7557: 			// asked rather than the string being written here.
7558: 			else if (Utils::String::startsWith(trimmed, "EXIT_HINT="))
7559: 			{
7560: 				const std::string reported = Utils::String::trim(trimmed.substr(10));
7561: 				if (!reported.empty())
7562: 					exitHint = reported;
7563: 			}
7564: 		}
7565: 
7566: 		if (status == "waiting" && !url.empty())
7567: 			return true;
7568: 
7569: 		url.clear();
7570: 		// A sleep, not a shell running sleep (#308 8-es claude F-ES-16): a
7571: 		// fork and exec every poll for nothing, and runSystemCommand is not
7572: 		// a promise to wait for its child.
7573: 		std::this_thread::sleep_for(std::chrono::milliseconds(500));
7574: 	}
7575: 
7576: 	// A script that answered `info` and never said waiting has had its say:
7577: 	// failed, or not yet, for the whole poll. The address `url` still holds
7578: 	// then is not this session's (#308 8a gpt F-ES-18) -- the case the wait
7579: 	// above exists to rule out. Fail closed.
7580: 	if (understood)
7581: 		return false;
7582: 
7583: 	// An image whose cloud_oauth predates `info` still answers `url`.
7584: 	auto lines = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth url");
7585: 	if (!lines.empty())
7586: 		url = Utils::String::trim(lines.front());
7587: 	return !url.empty();
7588: }
7589: 
7590: // How do you want to type?
7591: //
7592: // The sign-in page used to open onto the QR screen whichever way you meant to
7593: // work, so somebody signing in on the handheld met a page about their phone
7594: // and stopped there. The phone was never the place the sign-in happens -- it
7595: // is one of two keyboards -- and a screen that leads with a code to scan says
7596: // the opposite.
7597: //
7598: // Asked once, up front, because it is the only thing that differs between the
7599: // two routes and everything after it follows.
7600: static void cloudOAuthChooseInput(Window* window, const CloudBackend& backend,
7601: 	const std::string& remoteName, GuiSettings* prev)
7602: {
7603: 	// Off the UI thread. This waits on a provider round trip and used to run
7604: 	// inline, spawning a subprocess per poll, so ES painted nothing for the
7605: 	// fifteen-odd seconds it took -- indistinguishable from a freeze, and
7606: 	// reported as one. It is also why the wait could not afford to be
7607: 	// patient; now it can.
7608: 	window->pushGui(new GuiLoading<CloudOAuthReady>(window, _("STARTING SIGN-IN"),
7609: 		[](IGuiLoadingHandler*)
7610: 		{
7611: 			CloudOAuthReady ready;
7612: 			ready.started = cloudOAuthAwaitSession(ready.url, ready.onDevice,
7613: 			                                       ready.exitHint);
7614: 			return ready;
7615: 		},
7616: 		[window, backend, remoteName, prev](CloudOAuthReady ready)
7617: 		{
7618: 			cloudOAuthPresentChoice(window, backend, remoteName, prev, ready);
7619: 		}));
7620: }
7621: 
7622: static void cloudOAuthPresentChoice(Window* window, const CloudBackend& backend,
7623: 	const std::string& remoteName, GuiSettings* prev,
7624: 	const CloudOAuthReady& ready)
7625: {
7626: 	// An image that cannot host the page has only one route; asking would be
7627: 	// a question with a single answer.
7628: 	if (!ready.started || !ready.onDevice)
7629: 	{
7630: 		cloudOAuthShowSignIn(window, backend, remoteName, prev, true, ready);
7631: 		return;
7632: 	}
7633: 
7634: 	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
7635: 	s->setSubTitle(CloudText::providerSubtitle(backend.name, backend.label));
7636: 
7637: 	// Showing this choice closes prev. Each action must replace this page,
7638: 	// not the provider page that has already been deleted.
7639: 	s->addGroup(_("HOW DO YOU WANT TO TYPE?"));
7640: 	s->addWithDescription(_("WITH THE ON-SCREEN KEYBOARD"),
7641: 		_("WORKED WITH THE D-PAD, ON THIS SCREEN."),
7642: 		nullptr, [window, backend, remoteName, s, ready]
7643: 		{
7644: 			cloudOAuthShowSignIn(window, backend, remoteName, s, false, ready);
7645: 		}, "", false, true);
7646: 
7647: 	s->addWithDescription(_("WITH MY PHONE"),
7648: 		// One line (D-UI-023): the sentence this replaced measured 929 of
7649: 		// 780 px at 1280x800 and 701 of 620 at 640x480 (#308 F-ES-14).
7650: 		_("YOUR PHONE BECOMES THE KEYBOARD. SCAN THE CODE, THEN CONTINUE."),
7651: 		nullptr, [window, backend, remoteName, s, ready]
7652: 		{
7653: 			cloudOAuthShowSignIn(window, backend, remoteName, s, true, ready);
7654: 		}, "", false, true);
7655: 
7656: 	cloudSetupSetButtons(s, nullptr);
7657: 	cloudOAuthOwnSession(s);
7658: 	cloudSetupPresent(window, s, prev);
7659: }
7660: 
7661: static void cloudOAuthShowSignIn(Window* window, const CloudBackend& backend,
7662: 	const std::string& remoteName, GuiSettings* prev, bool usePhone,
7663: 	const CloudOAuthReady& ready)
7664: {
7665: 	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
7666: 	s->setSubTitle(CloudText::providerSubtitle(backend.name, backend.label));
7667: 
7668: 	// The address carries its own PIN in its path. ADDRESS and PIN are still
7669: 	// reported by `info` for anything driving this from a shell, but the page
7670: 	// has nothing to do with them separately -- two numbers on one screen is
7671: 	// what made "code" ambiguous the first time.
7672: 	const std::string url = ready.url;
7673: 	const bool onDevice = ready.onDevice;
7674: 	const std::string exitHint = ready.exitHint;
7675: 
7676: 	if (!ready.started)
7677: 	{
7678: 		cloudSetupAddProse(s, window, _("SIGN-IN DID NOT START"),
7679: 			_("THE DEVICE COULD NOT REACH THE PROVIDER. CHECK THE NETWORK AND TRY AGAIN."));
7680: 		// One button, and it goes back. This page used to carry CONTINUE as
7681: 		// well, which offered to continue with a sign-in that had not begun.
7682: 		s->getMenu().clearButtons();
7683: 		s->getMenu().addButton(_("GO BACK"), _("go back"), [s] { s->close(); });
7684: 		cloudOAuthOwnSession(s);
7685: 		cloudSetupPresent(window, s, prev);
7686: 		return;
7687: 	}
7688: 
7689: 	// Typing on the handheld: nothing to read off the screen, nothing to
7690: 	// scan. Open the provider's page and get out of the way. The keyboard
7691: 	// raises itself on the first field, so there is no instruction to give
7692: 	// that the page does not give better.
7693: 	const bool openImmediately = onDevice && !usePhone;
7694: 	if (openImmediately)
7695: 	{
7696: 		cloudSetupAddProse(s, window, _("SIGNING IN"),
7697: 			_("THE PROVIDER'S PAGE IS OPENING. A KEYBOARD APPEARS WHEN YOU PICK A BOX; MOVE WITH THE D-PAD AND CHOOSE WITH A."));
7698: 		cloudSetupAddSpacer(s, window);
7699: 		cloudSetupAddInfoRow(s, window,
7700: 			Utils::String::format(_("TO COME BACK HERE, PRESS %s").c_str(), exitHint.c_str()));
7701: 		cloudSetupAddInfoRow(s, window, _("THEN CHOOSE 'CONTINUE' TO FINISH"));
7702: 	}
7703: 	else
7704: 	{
7705: 		// The phone is a keyboard, not the place the sign-in happens. Saying
7706: 		// "sign in on your phone" sent people looking for a provider page
7707: 		// there; the page is on the handheld either way.
7708: 		const std::string qrPath = "/tmp/cloud-oauth-qr.png";
7709: 		Utils::Platform::runSystemCommand(
7710: 			"rm -f " + qrPath + "; /usr/bin/qrencode -o " + qrPath
7711: 			+ " -s 8 -m 4 --background=FFFFFF --foreground=000000 -l M "
7712: 			+ cloudShellQuote(url), "", nullptr);
7713: 
7714: 		std::vector<std::pair<std::string, bool>> lines;
7715: 		if (onDevice)
7716: 		{
7717: 			s->addGroup(_("USE YOUR PHONE AS A KEYBOARD"));
7718: 			cloudSetupAddSpacer(s, window);
7719: 			lines.push_back(std::make_pair(_("SCAN THIS, OR OPEN"), false));
7720: 			lines.push_back(std::make_pair(url, true));
7721: 			lines.push_back(std::make_pair(_("WHAT YOU TYPE THERE APPEARS HERE"), false));
7722: 		}
7723: 		else
7724: 		{
7725: 			// The older route, for an image that cannot host the page: the
7726: 			// player signs in on their phone and brings an address back.
7727: 			lines.push_back(std::make_pair(_("OPEN THIS IN A BROWSER"), false));
7728: 			lines.push_back(std::make_pair(url, true));
7729: 			lines.push_back(std::make_pair(_("THE LAST 4 DIGITS ARE A PIN"), false));
7730: 			lines.push_back(std::make_pair(_("IT KEEPS OTHERS OFF THIS PAGE"), false));
7731: 		}
7732: 
7733: 		if (Utils::FileSystem::exists(qrPath))
7734: 			cloudSetupAddQrRow(s, window, qrPath, lines);
7735: 		else
7736: 			for (auto& line : lines)
7737: 				cloudSetupAddInfoRow(s, window, line.first, line.second);
7738: 
7739: 		if (onDevice)
7740: 			cloudSetupAddProse(s, window, _("THEN"),
7741: 				_("CONNECT YOUR PHONE FIRST, THEN CHOOSE 'CONTINUE', AND THE PROVIDER'S PAGE OPENS ON THIS SCREEN."));
7742: 		else
7743: 			cloudSetupAddProse(s, window, _("THEN"),
7744: 				_("THAT PAGE WALKS YOU THROUGH SIGNING IN. COME BACK HERE AND SELECT 'CONTINUE' WHEN IT SAYS YOU ARE CONNECTED."));
7745: 	}
7746: 
7747: 	// Ask cloud_oauth, which asks rclone. Nothing here decides on its own
7748: 	// that a sign-in worked.
7749: 	//
7750: 	// openOnContinue is false when the page is already open: pressing
7751: 	// CONTINUE then means "I am done", not "open it".
7752: 	const bool openOnContinue = onDevice && usePhone;
7753: 	cloudSetupSetButtons(s, [window, backend, remoteName, s, openOnContinue]
7754: 	{
7755: 		if (openOnContinue)
7756: 		{
7757: 			auto info = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth status");
7758: 			std::string now = info.empty() ? "" : Utils::String::trim(info.front());
7759: 			if (now == "waiting")
7760: 			{
7761: 				// Blocks until the player comes back out of the page, so
7762: 				// there is no dialog to dismiss afterwards and no second
7763: 				// CONTINUE to press -- fall through and say what happened.
7764: 				ApiSystem::getInstance()->launchCloudSignIn(window, true);
7765: 			}
7766: 		}
7767: 
7768: 		auto lines = Utils::Platform::GetShOutputLines("/usr/bin/cloud_oauth status");
7769: 		std::string status = lines.empty() ? "" : Utils::String::trim(lines.front());
7770: 		LOG(LogInfo) << "cloud_oauth status=" << status;
7771: 
7772: 		if (status == "signed-in")
7773: 		{
7774: 			cloudOAuthShowConnected(window, backend, remoteName, s);
7775: 			return;
7776: 		}
7777: 		if (status == "failed")
7778: 		{
7779: 			window->pushGui(new GuiMsgBox(window,
7780: 				_("THE SIGN-IN DID NOT COMPLETE. TRY AGAIN TO START A NEW SIGN-IN."),
7781: 				_("TRY AGAIN"), [window, backend, remoteName, s] { cloudOAuthStart(window, backend, remoteName, s); },
7782: 				_("CANCEL SIGN-IN"), [s] { s->close(); }));
7783: 			return;
7784: 		}
7785: 		window->pushGui(new GuiMsgBox(window,
7786: 			_("STILL WAITING FOR THE SIGN-IN.\n\nFINISH IT, THEN CHOOSE 'CONTINUE' AGAIN."),
7787: 			_("OK"), nullptr,
7788: 			_("CANCEL SIGN-IN"), [window, s]
7789: 			{
7790: 				Utils::Platform::runSystemCommand("/usr/bin/cloud_oauth cancel", "", nullptr);
7791: 				s->close();
7792: 			}));
7793: 	});
7794: 
7795: 	cloudOAuthOwnSession(s);
7796: 	cloudSetupPresent(window, s, prev);
7797: 
7798: 	// After the page is on the stack, never while it is being built: this
7799: 	// blocks for as long as somebody is signing in, and ES is suspended for
7800: 	// the duration. The page has to already be there for ES to come back to.
7801: 	if (openImmediately)
7802: 		ApiSystem::getInstance()->launchCloudSignIn(window, false);
7803: }
7804: 
7805: // What it means to have connected something, said once, at the only moment
7806: // anybody is going to read it.
7807: //
7808: // The old ending was a one-line dialog -- "CONNECTED. CLOUD TOOLS ARE NOW
7809: // AVAILABLE" -- which named neither the provider just connected nor anything
7810: // the player could go and do. Somebody who has just finished a sign-in on a
7811: // handheld deserves to be told what they now have.
7812: static void cloudOAuthShowConnected(Window* window, const CloudBackend& backend,
7813: 	const std::string& remoteName, GuiSettings* prev)
7814: {
7815: 	cloudSetupShowDoneStep(window, remoteName, prev);
7816: }
7817: 
7818: // Adding and renewing are distinct before a sign-in begins. A new name is
7819: // editable and never overwrites an existing connection at the backend.
7820: static void cloudOAuthAdd(Window* window, const CloudBackend& backend, GuiSettings* prev)
7821: {
7822: 	auto s = new GuiSettings(window, _("ADD CONNECTION"));
7823: 	auto name = std::make_shared<std::string>(backend.name);
7824: 	std::set<std::string> existing;
7825: 	for (const auto& line : cloudRemoteLines("list"))
7826: 	{
7827: 		auto cols = Utils::String::splitAny(line, "\t", false);
7828: 		if (cols.size() >= 2) existing.insert(cols[0]);
7829: 	}
7830: 	for (int suffix = 2; existing.count(*name); ++suffix)
7831: 		*name = backend.name + std::to_string(suffix);
7832: 	s->addInputTextRow(_("CONNECTION NAME"), *name, false,
7833: 		[name](Window* w, std::string title, std::string /*initial*/,
7834: 			const std::function<void(std::string)>& save)
7835: 		{
7836: 			if (Settings::getInstance()->getBool("UseOSK"))
7837: 				w->pushGui(new GuiTextEditPopupKeyboard(w, title, *name, save, false));
7838: 			else
7839: 				w->pushGui(new GuiTextEditPopup(w, title, *name, save, false));
7840: 		},
7841: 		[name](const std::string& value) { *name = Utils::String::trim(value); });
7842: 	cloudSetupAddProse(s, window, _("ADD A SEPARATE CONNECTION"),
7843: 		_("THIS KEEPS YOUR EXISTING CONNECTIONS. TO RENEW A SIGN-IN, CHOOSE THAT CONNECTION UNDER CLOUD CONNECTIONS."));
7844: 	s->addEntry(_("SIGN IN"), true, [window, backend, name, existing, s]
7845: 	{
7846: 		if (name->empty() || existing.count(*name))
7847: 		{
7848: 			window->pushGui(new GuiMsgBox(window, _("CHOOSE A DIFFERENT CONNECTION NAME."), _("OK")));
7849: 			return;
7850: 		}
7851: 		cloudOAuthStart(window, backend, *name, s);
7852: 	});
7853: 	cloudSetupPresent(window, s, prev);
7854: }
7855: 
7856: // A filtered list of backends. `tier` empty means every tier.
7857: static void cloudRemoteShowList(Window* window, const std::string& title,
7858: 	const std::string& tier, const std::string& textFilter)
7859: {
7860: 	auto s = new GuiSettings(window, title);
7861: 
7862: 	auto backends = cloudRemoteBackends();
7863: 	int shown = 0;
7864: 	for (auto& b : backends)
7865: 	{
7866: 		if (b.tier == "plumbing")
7867: 			continue;
7868: 		// "needs-browser" spans both tiers that cannot be finished on the
7869: 		// handheld today.
7870: 		if (tier == "needs-browser")
7871: 		{
7872: 			if (b.tier != "oauth")
7873: 				continue;
7874: 		}
7875: 		else if (!tier.empty() && b.tier != tier)
7876: 			continue;
7877: 		if (!textFilter.empty()
7878: 			&& !Utils::String::containsIgnoreCase(b.label, textFilter)
7879: 			&& !Utils::String::containsIgnoreCase(b.name, textFilter))
7880: 			continue;
7881: 
7882: 		CloudBackend backend = b;
7883: 		shown++;
7884: 		// "oauth" means a backend we could drive natively once the
7885: 		// device-flow work lands (#51 P2). Until then it needs a browser
7886: 		// exactly like "fallback" does, and the form would ask a player for
7887: 		// a client_id and a token they have no way to produce. Group it with
7888: 		// what is honest today rather than with what is planned.
7889: 		if (b.tier == "oauth")
7890: 		{
7891: 			// Not "sign in with your phone": the provider's page opens on
7892: 			// this screen, and the phone is only one of the two keyboards
7893: 			// you can type on. Which one is asked after this, so the row
7894: 			// says what kind of sign-in it is and nothing about where.
7895: 			s->addWithDescription(Utils::String::toUpper(b.label),
7896: 				_("OPENS THE PROVIDER'S SIGN-IN PAGE."), nullptr,
7897: 				[window, backend, s] { cloudOAuthAdd(window, backend, s); },
7898: 				"", false, true);
7899: 		}
7900: 		else
7901: 		{
7902: 			s->addEntry(Utils::String::toUpper(b.label), true, [window, backend]
7903: 			{
7904: 				cloudRemoteChooseBackend(window, backend);
7905: 			});
7906: 		}
7907: 	}
7908: 
7909: 	if (shown == 0)
7910: 		s->addEntry(_("NOTHING MATCHED THAT SEARCH"), false, [] {});
7911: 
7912: 	cloudSetupPresent(window, s, nullptr);
7913: }
7914: 
7915: static bool cloudConnectionManual(Window* window)
7916: {
7917: 	if (SystemConf::getInstance()->get("cloudsaves.startup") != "1" &&
7918: 		SystemConf::getInstance()->get("cloudsaves.gameexit") != "1") return true;
7919: 	window->pushGui(new GuiMsgBox(window,
7920: 		_("TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS UNDER MANAGE CLOUD STORAGE BEFORE CHANGING THIS CONNECTION."), _("OK")));
7921: 	return false;
7922: }
7923: 
7924: static void cloudConnectionChange(Window* window, const std::string& command, GuiSettings* page)
7925: {
7926: 	window->pushGui(new GuiLoading<std::string>(window, _("SAVING CONNECTION"),
7927: 		[command](IGuiLoadingHandler*) { return Utils::Platform::GetShOutput("timeout 60 /usr/bin/cloud_remote " + command + " 2>&1"); },
7928: 		[window, page](const std::string& result)
7929: 		{
7930: 			if (!Utils::String::startsWith(result, "OK="))
7931: 			{
7932: 				window->pushGui(new GuiMsgBox(window,
7933: 					_("THE CONNECTION COULDN'T BE CHANGED.") + std::string("\n\n") + cloudConnectionError(result), _("OK")));
7934: 				return;
7935: 			}
7936: 			page->close();
7937: 		}));
7938: }
7939: 
7940: static void cloudConnectionDetails(Window* window, const std::string& name, const std::string& type, const std::string& subprovider)
7941: {
7942: 	auto s = new GuiSettings(window, _("CLOUD CONNECTION"));
7943: 	cloudSetupAddFact(s, window, _("CONNECTION NAME"), name);
7944: 	cloudSetupAddFact(s, window, _("PROVIDER"), CloudText::providerLabel(type));
7945: 	s->addEntry(_("CHECK CONNECTION"), true, [window, name]
7946: 	{
7947: 		cloudSetupRunCheck(window, name + ":", [window](int rc, const std::string&)
7948: 		{
7949: 			window->pushGui(new GuiMsgBox(window, rc == 0 ? _("THE CONNECTION ANSWERED.") : _("COULDN'T REACH THIS CONNECTION. CHECK WI-FI OR SIGN IN AGAIN."), _("OK")));
7950: 		});
7951: 	});
7952: 	s->addEntry(_("USE THIS CONNECTION"), true, [window, name, s]
7953: 	{
7954: 		if (!cloudConnectionManual(window)) return;
7955: 		window->pushGui(new GuiMsgBox(window,
7956: 			_("USE THIS CONNECTION FOR CLOUD TOOLS? YOUR SELECTED FOLDER PATHS WILL STAY THE SAME. CHECK THEM BEFORE YOUR NEXT BACKUP OR RESTORE."),
7957: 			_("USE CONNECTION"), [window, name, s] { cloudConnectionChange(window, "select " + cloudShellQuote(name), s); }, _("CANCEL"), nullptr));
7958: 	});
7959: 	for (auto backend : cloudRemoteBackends())
7960: 	{
7961: 		if (backend.name != type) continue;
7962: 		backend.subprovider = subprovider;
7963: 		if (backend.tier == "oauth")
7964: 		{
7965: 			backend.reauthorize = true;
7966: 			s->addEntry(_("SIGN IN AGAIN"), true, [window, backend, name, s]
7967: 			{
7968: 				if (!cloudConnectionManual(window)) return;
7969: 				window->pushGui(new GuiMsgBox(window,
7970: 					_("SIGN IN TO THE SAME CLOUD ACCOUNT AGAIN. YOUR CURRENT SIGN-IN IS KEPT UNTIL THE NEW ONE WORKS. YOUR SELECTED FOLDERS WILL STAY THE SAME."),
7971: 					_("SIGN IN"), [window, backend, name, s] { cloudOAuthStart(window, backend, name, s); }, _("CANCEL"), nullptr));
7972: 			});
7973: 		}
7974: 		else
7975: 			s->addEntry(_("EDIT CONNECTION"), true, [window, backend, name, s]
7976: 			{
7977: 				if (!cloudConnectionManual(window)) return;
7978: 				auto values = std::make_shared<std::map<std::string, std::string>>();
7979: 				(*values)["__name__"] = name;
7980: 				(*values)["__edit__"] = "1";
7981: 				cloudRemoteShowForm(window, backend, values, s);
7982: 			});
7983: 		break;
7984: 	}
7985: 	s->addEntry(_("REMOVE CONNECTION"), true, [window, name, s]
7986: 	{
7987: 		if (!cloudConnectionManual(window)) return;
7988: 		window->pushGui(new GuiMsgBox(window,
7989: 			_("REMOVE THIS CONNECTION FROM THIS DEVICE? YOUR CLOUD FILES STAY WHERE THEY ARE. IF THIS IS YOUR ACTIVE CONNECTION, CHOOSE ANOTHER BEFORE USING CLOUD TOOLS."),
7990: 			_("REMOVE CONNECTION"), [window, name, s] { cloudConnectionChange(window, "remove " + cloudShellQuote(name), s); }, _("CANCEL"), nullptr));
7991: 	});
7992: 	cloudSetupPresent(window, s, nullptr);
7993: }
7994: 
7995: void GuiMenu::openCloudConnections(Window* window)
7996: {
7997: 	auto s = new CloudConnectionsPage(window, _("CLOUD CONNECTIONS"), [window] { GuiMenu::openCloudConnections(window); });
7998: 	const auto rows = cloudRemoteLines("list");
7999: 	const bool readable = !rows.empty() && Utils::String::startsWith(rows.front(), "STATE=");
8000: 	if (!readable)
8001: 		cloudSetupAddProse(s, window, _("CONNECTIONS UNAVAILABLE"), _("YOUR CLOUD CONNECTIONS COULDN'T BE READ. TRY AGAIN."));
8002: 	else if (rows.front() != "STATE=active")
8003: 		cloudSetupAddProse(s, window, _("NO CONNECTION IN USE"), _("CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS."));
8004: 	for (const auto& line : rows)
8005: 	{
8006: 		auto cols = Utils::String::splitAny(line, "\t", false);
8007: 		if (cols.size() < 3) continue;
8008: 		const auto name = cols[0], type = cols[1];
8009: 		const std::string subprovider = cols.size() > 3 ? cols[3] : "";
8010: 		const auto detail = CloudText::providerLabel(type) + (cols[2] == "active" ? " - " + _("IN USE") : "");
8011: 		s->addWithDescription(name, detail, nullptr,
8012: 			[window, name, type, subprovider] { cloudConnectionDetails(window, name, type, subprovider); }, "", false, true);
8013: 	}
8014: 	if (readable) s->addEntry(_("ADD CONNECTION"), true, [window] { GuiMenu::openCloudAddRemote(window); });
8015: 	s->addEntry(_("USE A COMPUTER INSTEAD"), true, [window] { GuiMenu::openCloudSetup(window); });
8016: 	cloudSetupPresent(window, s, nullptr);
8017: }
8018: 
8019: void GuiMenu::openCloudAddRemote(Window* window)
8020: {
8021: 	auto s = new GuiSettings(window, _("CONNECT CLOUD STORAGE"));
8022: 
8023: 	auto backends = cloudRemoteBackends();
8024: 	if (backends.empty())
8025: 	{
8026: 		// cloud_remote asks rclone for this list, so an empty result means
8027: 		// rclone is missing or broken -- not that there are no providers.
8028: 		s->addEntry(_("PROVIDER LIST UNAVAILABLE"), false, [] {});
8029: 		cloudSetupPresent(window, s, nullptr);
8030: 		return;
8031: 	}
8032: 
8033: 	s->addGroup(_("RECOMMENDED"));
8034: 	for (auto& want : CloudText::recommendedProviders())
8035: 	{
8036: 		for (auto& b : backends)
8037: 		{
8038: 			if (b.name != want.first)
8039: 				continue;
8040: 			// Show our short name here; the form still titles itself with
8041: 			// rclone's description, which is useful once you have chosen.
8042: 			// The tier decides what happens next, so the player never has to
8043: 			// know there are two kinds of sign-in before they pick.
8044: 			CloudBackend backend = b;
8045: 			// The list is handed over as the page this replaces, so the flow
8046: 			// closes back to network settings rather than depositing somebody
8047: 			// who has just connected onto the list of things to connect.
8048: 			s->addEntry(_(want.second.c_str()), true, [window, backend, s]
8049: 			{
8050: 				if (backend.tier == "oauth")
8051: 					cloudOAuthAdd(window, backend, s);
8052: 				else
8053: 					cloudRemoteChooseBackend(window, backend);
8054: 			});
8055: 			break;
8056: 		}
8057: 	}
8058: 
8059: 	s->addGroup(_("MORE"));
8060: 	s->addEntry(_("SEARCH PROVIDERS"), true, [window]
8061: 	{
8062: 		auto onSearch = [window](const std::string& term)
8063: 		{
8064: 			if (Utils::String::trim(term).empty())
8065: 				return;
8066: 			cloudRemoteShowList(window, _("SEARCH RESULTS"), "", Utils::String::trim(term));
8067: 		};
8068: 		if (Settings::getInstance()->getBool("UseOSK"))
8069: 			window->pushGui(new GuiTextEditPopupKeyboard(window, _("SEARCH PROVIDERS"), "", onSearch, false));
8070: 		else
8071: 			window->pushGui(new GuiTextEditPopup(window, _("SEARCH PROVIDERS"), "", onSearch, false));
8072: 	});
8073: 
8074: 	// One complete list, not one per tier. Two entries that each showed part
8075: 	// of the catalogue made the recommendations above look like a third
8076: 	// category rather than a shortlist -- and left no single place to answer
8077: 	// "is my provider supported at all?".
8078: 	s->addWithDescription(_("COMPLETE LIST"),
8079: 		_("EVERY PROVIDER RCLONE SUPPORTS."),
8080: 		nullptr, [window] { cloudRemoteShowList(window, _("COMPLETE LIST"), "", ""); },
8081: 		"", false, true);
8082: 
8083: 	// The old SSH wizard, one level down. It is still the only way to reach
8084: 	// rclone's own config for the things a form cannot express -- crypt and
8085: 	// union remotes, or reconnecting one whose sign-in has lapsed -- but it
8086: 	// is no longer a second front door offering the same job as the first.
8087: 	s->addWithDescription(_("USE A COMPUTER INSTEAD"),
8088: 		_("RUN RCLONE'S SETUP OVER SSH. FOR CONNECTIONS THIS PAGE CAN'T MAKE."),
8089: 		nullptr, [window] { GuiMenu::openCloudSetup(window); }, "", false, true);
8090: 
8091: 	cloudSetupPresent(window, s, nullptr);
8092: }
8093: 
8094: void GuiMenu::openCloudSetup(Window* window)
8095: {
8096: 	auto info = cloudSetupInfo();
8097: 	if (info["IP"].empty())
8098: 	{
8099: 		window->pushGui(new GuiMsgBox(window, _("NO NETWORK CONNECTION DETECTED.\n\nCONNECT TO A NETWORK FIRST, THEN TRY AGAIN.")));
8100: 		return;
8101: 	}
8102: 
8103: 	// Remote names from `rclone listremotes` keep their trailing colon.
8104: 	std::vector<std::string> remotes;
8105: 	for (auto& name : Utils::String::split(info["REMOTES"], ' '))
8106: 		if (!Utils::String::trim(name).empty())
8107: 			remotes.push_back(Utils::String::trim(name));
8108: 
8109: 	LOG(LogInfo) << "cloud_setup wizard: entry, remotes=" << remotes.size();
8110: 
8111: 	if (remotes.empty())
8112: 	{
8113: 		cloudSetupShowSshStep(window, CloudSetupMode::FirstRemote, "", "", nullptr);
8114: 		return;
8115: 	}
8116: 
8117: 	auto s = new GuiSettings(window, _("CLOUD STORAGE SETUP"));
8118: 
8119: 	s->addGroup(_("YOUR CONNECTIONS"));
8120: 	for (auto remote : remotes)
8121: 	{
8122: 		s->addEntry(cloudSetupDisplayName(remote) + "  -  " + _("CHECK IT WORKS"), true, [window, remote]
8123: 		{
8124: 			cloudSetupRunCheck(window, remote, [window](int rc, const std::string& name)
8125: 			{
8126: 				if (rc == 0)
8127: 					window->pushGui(new GuiMsgBox(window, _("YOUR CLOUD IS ANSWERING:") + " " + cloudSetupDisplayName(name)));
8128: 				else if (rc == 2)
8129: 					window->pushGui(new GuiMsgBox(window, _("THIS CONNECTION ISN'T ANSWERING:") + " " + cloudSetupDisplayName(name) + "\n\n" + _("USE 'REPAIR A CONNECTION' TO RENEW ITS SIGN-IN.")));
8130: 				else
8131: 					window->pushGui(new GuiMsgBox(window, _("NO CLOUD STORAGE IS SET UP ON THIS DEVICE YET.")));
8132: 			});
8133: 		});
8134: 	}
8135: 
8136: 	s->addGroup(_("WHAT DO YOU WANT TO DO?"));
8137: 	const std::string syncpath = info["SAVES_REMOTE"];
8138: 	cloudSetupAddFact(s, window, _("CLOUD FOLDER"), syncpath, [window, s, syncpath]
8139: 	{
8140: 		cloudOpenFolderSettings(window, [window, s]
8141: 		{
8142: 			GuiMenu::openCloudSetup(window);
8143: 			s->close();
8144: 		});
8145: 	});
8146: 	std::string preexisting = Utils::String::trim(info["REMOTES"]);
8147: 	s->addEntry(_("ADD ANOTHER CONNECTION"), true, [window, s, preexisting]
8148: 	{
8149: 		cloudSetupShowSshStep(window, CloudSetupMode::AddRemote, "", preexisting, s);
8150: 	});
8151: 	s->addEntry(_("REPAIR A CONNECTION"), true, [window, s, remotes]
8152: 	{
8153: 		if (remotes.size() == 1)
8154: 		{
8155: 			cloudSetupShowSshStep(window, CloudSetupMode::RepairRemote, remotes.front(), "", s);
8156: 			return;
8157: 		}
8158: 		auto picker = new GuiSettings(window, _("WHICH CONNECTION?"));
8159: 		for (auto remote : remotes)
8160: 		{
8161: 			picker->addEntry(cloudSetupDisplayName(remote), true, [window, s, picker, remote]
8162: 			{
8163: 				// The chooser (s) is not the page owning this handler,
8164: 				// so closing it here is safe; the picker itself is
8165: 				// replaced by the wizard page.
8166: 				s->close();
8167: 				cloudSetupShowSshStep(window, CloudSetupMode::RepairRemote, remote, "", picker);
8168: 			});
8169: 		}
8170: 		window->pushGui(picker);
8171: 	});
8172: 
8173: 	window->pushGui(s);
8174: }
8175: 
8176: // Post-restore credential re-entry. Backups deliberately carry no
8177: // secrets, so a restored device needs its credentials back; this page
8178: // shows each one with its verified state and an inline way to fix it.
8179: //
8180: // It is a single page rather than a gated wizard on purpose: every item
8181: // here is independent and optional (a player with no RetroAchievements
8182: // account should not be walked through a step for it), so there is no
8183: // mandatory sequence to enforce - only state to show and actions to
8184: // offer.
8185: //
8186: // Wi-Fi comes first because it is the one item other things depend on:
8187: // the sanitized system.cfg drops `wifi.key`, so a settings restore
8188: // disconnects Wi-Fi, and the cloud-journey continuation that follows
8189: // this page needs the network back.
8190: static void networkApplyWifi(Window* window, const std::string& title,
8191: 	const std::function<bool()>& apply, const std::function<void(bool)>& onDone);
8192: 
8193: void GuiMenu::openRestoreRelink(Window* window, bool consumeMarker)
8194: {
8195: 	const std::string restoreMarker = "/storage/.config/.restore-finish-pending";
8196: 
8197: 	auto theme = ThemeData::getMenuTheme();
8198: 	auto s = new GuiSettings(window, _("FINISH RESTORE PROCESS"));
8199: 	s->setSubTitle(_("RE-ENTER THE PASSWORDS BACKUPS DO NOT INCLUDE"));
8200: 



# FILE emulationstation/es-app/src/guis/GuiWifi.cpp


## Original lines 1–387
1: #include "guis/GuiWifi.h"
2: #include "guis/GuiMenu.h"
3: #include "guis/GuiMsgBox.h"
4: #include "guis/GuiSettings.h"
5: #include "guis/GuiTextEditPopup.h"
6: #include "guis/GuiTextEditPopupKeyboard.h"
7: #include "components/TextComponent.h"
8: #include "ApiSystem.h"
9: #include "GuiLoading.h"
10: #include "LocaleES.h"
11: #include "Log.h"
12: #include "Settings.h"
13: #include "SystemConf.h"
14: #include "ThemeData.h"
15: #include "Window.h"
16: #include "utils/StringUtil.h"
17: 
18: GuiWifi::GuiWifi(Window* window, const std::string& title, const std::function<void()>& onJoined)
19: 	: GuiComponent(window), mMenu(window, title.c_str()), mTitle(title), mOnJoined(onJoined), mSavedKnown(true), mWaitingLoad(false)
20: {
21: 	addChild(&mMenu);
22: 
23: 	// Fetched off the interface thread. wifictl list is itself a rescan --
24: 	// it waits for the adapter, asks NetworkManager to scan, sleeps, then
25: 	// lists -- so this constructor used to run up to twenty seconds of
26: 	// nmcli with nothing drawn, and with NetworkManager unresponsive (fork
27: 	// #102) nothing bounded it at all. Posted rather than pushed here,
28: 	// because the page has to be on the stack before anything can go over
29: 	// it; an empty first answer still turns into the full scan it always did.
30: 	mWindow->postToUiThread([this]() { onRefresh(false); });
31: 
32: 	mMenu.addButton(_("REFRESH"), "refresh", [&] { onRefresh(); });
33: 	mMenu.addButton(_("INPUT MANUALLY"), "manual input", [&] { onManualInput(); });
34: 	mMenu.addButton(_("BACK"), "back", [&] { delete this; });
35: 
36: 	if (Renderer::ScreenSettings::fullScreenMenus())
37: 		mMenu.setPosition((Renderer::getScreenWidth() - mMenu.getSize().x()) / 2, (Renderer::getScreenHeight() - mMenu.getSize().y()) / 2);
38: 	else
39: 		mMenu.setPosition((Renderer::getScreenWidth() - mMenu.getSize().x()) / 2, Renderer::getScreenHeight() * 0.15f);
40: }
41: 
42: void GuiWifi::load(const std::vector<WifiText::PickerRow>& rows)
43: {
44: 	mMenu.clear();
45: 
46: 	// A list whose SAVED marks could not be read says so, once, under the
47: 	// title (#308 F-WF-03): the rows are then neither saved nor unsaved, and
48: 	// a press on one asks before it acts.
49: 	mMenu.setSubTitle(mSavedKnown ? "" : _("COULDN'T CHECK WHICH NETWORKS ARE SAVED."));
50: 
51: 	if (rows.empty())
52: 		mMenu.addEntry(_("NO WI-FI NETWORKS FOUND"), false, [this] { onRefresh(); });
53: 	else
54: 		for (const auto& row : rows)
55: 			addRow(row);
56: 
57: 	mMenu.updateSize();
58: 
59: 	if (Renderer::ScreenSettings::fullScreenMenus())
60: 		mMenu.setPosition((Renderer::getScreenWidth() - mMenu.getSize().x()) / 2, (Renderer::getScreenHeight() - mMenu.getSize().y()) / 2);
61: 
62: 	mWaitingLoad = false;
63: }
64: 
65: // The name as NetworkManager has it -- case and spaces kept, since a
66: // network's name is what the player recognises it by (addEntry would
67: // upper-case it) -- and, on the right at the row's own weight, CONNECTED for
68: // the network the device is on or SAVED for one it holds a profile for: the
69: // shape and the word of MANAGE SAVED NETWORKS' mark, a fact beside the
70: // action.
71: void GuiWifi::addRow(const WifiText::PickerRow& network)
72: {
73: 	auto theme = ThemeData::getMenuTheme();
74: 	ComponentListRow row;
75: 
76: 	auto name = std::make_shared<TextComponent>(mWindow, network.name, theme->Text.font, theme->Text.color);
77: 	if (EsLocale::isRTL())
78: 		name->setHorizontalAlignment(Alignment::ALIGN_RIGHT);
79: 	row.addElement(name, true);
80: 
81: 	if (network.connected || network.saved)
82: 	{
83: 		const std::string mark = network.connected ? _("CONNECTED") : _("SAVED");
84: 		auto label = std::make_shared<TextComponent>(mWindow, mark, theme->Text.font, theme->Text.color, Alignment::ALIGN_RIGHT);
85: 		label->setSize(theme->Text.font->sizeText(mark + "  ").x(), 0);
86: 		row.addElement(label, false);
87: 	}
88: 
89: 	const WifiText::PickerRow chosen = network;
90: 	row.makeAcceptInputHandler([this, chosen] { onSelect(chosen); });
91: 	mMenu.addRow(row);
92: }
93: 
94: // A press: the network the device is on joins again with the key
95: // NetworkManager holds -- it answers at once, or comes back if it had
96: // dropped (#308 F-WF-05: this used to close on the list's snapshot); a
97: // saved one is offered CONNECT / FORGET / CANCEL (#318, D-UI-118); any
98: // unsaved open network connects without a key; protected or unknown ones ask
99: // for their key. One whose profile could not be asked about
100: // is asked about again first (F-WF-03/06). WifiText::pressAction decides.
101: void GuiWifi::onSelect(const WifiText::PickerRow& row)
102: {
103: 	if (mWaitingLoad)
104: 		return;
105: 
106: 	if (row.savedKnown && WifiText::profilesForSsid(row.name, mSaved).size() > 1 && row.profile.empty())
107: 	{
108: 		chooseProfile(row.name);
109: 		return;
110: 	}
111: 	act(WifiText::pressAction(row), row.name, WifiText::joinName(row));
112: }
113: 
114: // Several profiles can name one SSID. The player chooses a profile before
115: // CONNECT or FORGET; neither operation guesses which stored key they meant.
116: void GuiWifi::chooseProfile(const std::string& name)
117: {
118: 	auto page = new GuiSettings(mWindow, _("SAVED NETWORKS"));
119: 	for (const auto& profile : WifiText::profilesForSsid(name, mSaved))
120: 		page->addEntry(profile.name, true, [this, name, profile, page]
121: 		{
122: 			// Closing page destroys this row's callback and its captures.
123: 			// Keep the values on the stack before opening the next dialog.
124: 			GuiWifi* picker = this;
125: 			const std::string networkName = name;
126: 			const std::string profileName = profile.name;
127: 			page->close();
128: 			picker->act(WifiText::PressAction::ChooseSaved, networkName, profileName);
129: 		});
130: 	mWindow->pushGui(page);
131: }
132: 
133: // A join goes by the profile's name, which need not be the SSID the row
134: // shows (#308 claude F-WF-12, gpt F-WF-03): the connected row joined by its
135: // SSID, which is no profile's name for a renamed one, and the player read
136: // COULDN'T CONNECT, with forget-and-rejoin advice, about the network they
137: // were on.
138: void GuiWifi::act(WifiText::PressAction action, const std::string& name, const std::string& joinAs)
139: {
140: 	switch (action)
141: 	{
142: 	case WifiText::PressAction::Join:
143: 		join(name, joinAs);
144: 		break;
145: 	case WifiText::PressAction::ChooseSaved:
146: 	{
147: 		// A saved network the device is not on: CONNECT with the key
148: 		// NetworkManager holds, or FORGET it -- the second choice is the one
149: 		// ROCKNIX's own saved-Wi-Fi work offers, behind the manage page's
150: 		// confirmation and reader (GuiMenu::forgetWifiNetworkWithConfirmation),
151: 		// which rebuilds this list once the profile is gone. CONNECT first;
152: 		// CANCEL last, so B lands on it (es-ui-style-guide: back never lands
153: 		// on the destructive choice). The profile is forgotten by the name
154: 		// NetworkManager has for it (joinAs), which is the name the manage
155: 		// page shows.
156: 		const std::string text = Utils::String::format(_("%s IS SAVED.").c_str(), name.c_str())
157: 			+ "\n\n" + _("CONNECT WITH ITS SAVED KEY, OR FORGET IT?");
158: 		mWindow->pushGui(new GuiMsgBox(mWindow, text,
159: 			_("CONNECT"), [this, name, joinAs] { join(name, joinAs); },
160: 			_("FORGET"), [this, joinAs] { GuiMenu::forgetWifiNetworkWithConfirmation(mWindow, joinAs, false, [this] { onRefresh(false); }); },
161: 			_("CANCEL"), nullptr));
162: 		break;
163: 	}
164: 	case WifiText::PressAction::AskKey:
165: 		checkSecurityAndConnect(name);
166: 		break;
167: 	case WifiText::PressAction::CheckAgain:
168: 		// Never taken for a network with no profile: the key path rebuilds a
169: 		// profile of that name from what is typed.
170: 		mWindow->pushGui(new GuiMsgBox(mWindow,
171: 			_("COULDN'T CHECK WHICH NETWORKS ARE SAVED.") + std::string("\n\n") + _("CHECK AGAIN NOW?"),
172: 			_("YES"), [this] { onRefresh(false); },
173: 			_("NO"), nullptr));
174: 		break;
175: 	}
176: }
177: 
178: // INPUT MANUALLY: a hidden network's name, taken as a row would be -- a
179: // name NetworkManager holds a profile for joins, the one the device is on
180: // needs nothing, any other is asked for its key. Not trimmed: a name may
181: // begin or end with a space, and it is matched as NetworkManager has it.
182: void GuiWifi::onManualInput()
183: {
184: 	auto onName = [this](const std::string& name)
185: 	{
186: 		if (name.empty())
187: 			return;
188: 		const auto profile = WifiText::preferredProfile(name, mSaved);
189: 		if (mSavedKnown && WifiText::profilesForSsid(name, mSaved).size() > 1 && profile.empty())
190: 		{
191: 			chooseProfile(name);
192: 			return;
193: 		}
194: 		act(WifiText::manualAction(name, mCurrent, mSaved, mSavedKnown), name,
195: 			profile.empty() ? WifiText::manualJoinName(name, mCurrent, mCurrentProfile) : profile);
196: 	};
197: 
198: 	if (Settings::getInstance()->getBool("UseOSK"))
199: 		mWindow->pushGui(new GuiTextEditPopupKeyboard(mWindow, mTitle, "", onName, false));
200: 	else
201: 		mWindow->pushGui(new GuiTextEditPopup(mWindow, mTitle, "", onName, false));
202: }
203: 
204: // A saved network: its profile, with the key NetworkManager holds, behind
205: // the spinner -- wifictl join waits up to 90 s for the association, as
206: // connect does, and the screen would otherwise freeze for it. The script
207: // also moves the settings wifi.ssid and wifi.key onto the joined network,
208: // so the paths that connect from the settings (the restore wizard, the
209: // ENABLE WI-FI switch) still name the network the player is on; SystemConf
210: // is re-read so the interface sees the same file.
211: void GuiWifi::join(const std::string& name, const std::string& profile)
212: {
213: 	Window* window = mWindow;
214: 	mWaitingLoad = true;
215: 	LOG(LogInfo) << "wifi picker: joining the saved network " << name << " (profile " << profile << ")";
216: 	window->pushGui(new GuiLoading<WifiText::JoinAnswer>(window, _("CONNECTING TO WI-FI"),
217: 		[profile](IGuiLoadingHandler*) { return ApiSystem::getInstance()->joinWifiNetwork(profile); },
218: 		[this, window, name, profile](WifiText::JoinAnswer answer)
219: 		{
220: 			mWaitingLoad = false;
221: 			const int code = answer.code;
222: 			if (!answer.joined())
223: 			{
224: 				LOG(LogWarning) << "wifi picker: could not join the saved network " << name << " (profile " << profile << ", wifictl join exited " << code << ")";
225: 				// The advice by what happened (WifiText::joinFailure, #308
226: 				// F-WF-03/06): NetworkManager not answering is not a key that
227: 				// changed, and forgetting the network on that advice would
228: 				// lose a profile that was fine.
229: 				const std::string advice = WifiText::joinFailure(code) == WifiText::JoinFailure::ServiceNotAnswering
230: 					? _("THE WI-FI SERVICE DIDN'T ANSWER. TRY AGAIN IN A MOMENT.")
231: 					: _("IF ITS KEY HAS CHANGED, FORGET IT UNDER MANAGE SAVED NETWORKS AND JOIN IT AGAIN WITH THE NEW KEY.");
232: 				window->pushGui(new GuiMsgBox(window,
233: 					Utils::String::format(_("COULDN'T CONNECT TO %s.").c_str(), name.c_str()) + "\n\n" + advice, _("OK")));
234: 				return;
235: 			}
236: 			// Re-read for what the join wrote (wifi.ssid, wifi.key), keeping
237: 			// any change this interface has not saved yet -- one the settings
238: 			// lock refused -- unless the join wrote that key (G-E1-03).
239: 			SystemConf::getInstance()->loadSystemConf(true);
240: 			joined(name);
241: 		}));
242: }
243: 
244: // Any other network: its key first -- empty for an open network -- then
245: // the connection wifictl connect makes, which leaves a profile behind for
246: // next time. On success the settings take the network and its key, as they
247: // did when the row edited them: the network configured last, for the paths
248: // that connect from the settings.
249: void GuiWifi::checkSecurityAndConnect(const std::string& name)
250: {
251: 	mWaitingLoad = true;
252: 	mWindow->pushGui(new GuiLoading<std::string>(mWindow, _("CHECKING WI-FI NETWORK"),
253: 		[name](IGuiLoadingHandler*) { return ApiSystem::getInstance()->getWifiSecurity(name); },
254: 		[this, name](const std::string& security)
255: 		{
256: 			mWaitingLoad = false;
257: 			if (security == "open")
258: 				connect(name, "", true);
259: 			else
260: 				askKeyAndConnect(name);
261: 		}));
262: }
263: 
264: void GuiWifi::askKeyAndConnect(const std::string& name)
265: {
266: 	auto onKey = [this, name](const std::string& key) { connect(name, key); };
267: 
268: 	if (Settings::getInstance()->getBool("UseOSK"))
269: 		mWindow->pushGui(new GuiTextEditPopupKeyboard(mWindow, _("WI-FI KEY"), "", onKey, false));
270: 	else
271: 		mWindow->pushGui(new GuiTextEditPopup(mWindow, _("WI-FI KEY"), "", onKey, false));
272: }
273: 
274: void GuiWifi::connect(const std::string& name, const std::string& key, bool openNetwork)
275: {
276: 	Window* window = mWindow;
277: 	mWaitingLoad = true;
278: 	LOG(LogInfo) << "wifi picker: connecting to " << name;
279: #if !WIN32
280: 	const std::string country = SystemConf::getInstance()->get("wifi.country");
281: 	auto apply = [name, key, country, openNetwork](IGuiLoadingHandler*) { return openNetwork ? ApiSystem::getInstance()->connectOpenWifi(name) : ApiSystem::getInstance()->enableWifi(name, key, country); };
282: #else
283: 	auto apply = [name, key, openNetwork](IGuiLoadingHandler*) { return openNetwork ? ApiSystem::getInstance()->connectOpenWifi(name) : ApiSystem::getInstance()->enableWifi(name, key); };
284: #endif
285: 	window->pushGui(new GuiLoading<bool>(window, _("CONNECTING TO WI-FI"), apply,
286: 		[this, window, name, key, openNetwork](bool ok)
287: 		{
288: 			mWaitingLoad = false;
289: 			if (!ok)
290: 			{
291: 				LOG(LogWarning) << "wifi picker: could not connect to " << name;
292: 				window->pushGui(new GuiMsgBox(window,
293: 					Utils::String::format(_("COULDN'T CONNECT TO %s.").c_str(), name.c_str()) + "\n\n" + (openNetwork ? _("REFRESH THE NETWORK LIST AND TRY AGAIN.") : _("CHECK THE KEY AND TRY AGAIN.")), _("OK")));
294: 				return;
295: 			}
296: 			SystemConf::getInstance()->set("wifi.ssid", name);
297: 			SystemConf::getInstance()->set("wifi.key", key);
298: 			SystemConf::getInstance()->saveSystemConf();
299: 			joined(name);
300: 		}));
301: }
302: 
303: // The picker's job is done: the toast says so over whatever the page
304: // returns to, and the page that opened the picker rebuilds to read the
305: // connection back. The callback is copied out first -- it belongs to that
306: // page, and this component is gone before it runs.
307: void GuiWifi::joined(const std::string& name)
308: {
309: 	Window* window = mWindow;
310: 	auto onJoined = mOnJoined;
311: 	// <glyph> <subject> : <outcome>, one space after the glyph, as every
312: 	// toast (#308 F-WF-08); CONNECTED is the row's word for the same fact.
313: 	window->displayNotificationMessage(_U("\uF058 ") + WifiText::joinedNotice(name, _("CONNECTED")));
314: 	delete this;
315: 	if (onJoined != nullptr)
316: 		onJoined();
317: }
318: 
319: bool GuiWifi::input(InputConfig* config, Input input)
320: {
321: 	if (GuiComponent::input(config, input))
322: 		return true;
323: 
324: 	if (input.value != 0 && config->isMappedTo(BUTTON_BACK, input))
325: 	{
326: 		if (!mWaitingLoad)
327: 			delete this;
328: 
329: 		return true;
330: 	}
331: 
332: 	return false;
333: }
334: 
335: std::vector<HelpPrompt> GuiWifi::getHelpPrompts()
336: {
337: 	std::vector<HelpPrompt> prompts = mMenu.getHelpPrompts();
338: 	prompts.push_back(HelpPrompt(BUTTON_BACK, _("BACK")));
339: 	return prompts;
340: }
341: 
342: // rescan: ask NetworkManager for a fresh scan first (REFRESH, and an empty
343: // first list); false lists what it already knows, which is what the page
344: // opens with. The saved profiles and the network joined now come with the
345: // same wait, behind the spinner, each time-boxed in ApiSystem.
346: void GuiWifi::onRefresh(bool rescan)
347: {
348: 	Window* window = mWindow;
349: 	mWaitingLoad = true;
350: 
351: 	window->pushGui(new GuiLoading<Answer>(window, _("SEARCHING WI-FI NETWORKS"),
352: 		[rescan](IGuiLoadingHandler*)
353: 		{
354: 			// Each getter says whether it could ask at all (true for an
355: 			// answer, "none" included), and that is kept: "could not ask"
356: 			// used to be read as "none" (#308 F-WF-03/06).
357: 			Answer answer;
358: 			answer.inRange = ApiSystem::getInstance()->getWifiNetworks(rescan);
359: 			answer.savedKnown = ApiSystem::getInstance()->getSavedWifiNetworks(answer.saved);
360: 			answer.currentKnown = ApiSystem::getInstance()->getCurrentWifiSsid(answer.current);
361: 			return answer;
362: 		},
363: 		[this, rescan](Answer answer)
364: 		{
365: 			mWaitingLoad = false;
366: 			if (answer.inRange.empty() && !rescan)
367: 			{
368: 				onRefresh(true);
369: 				return;
370: 			}
371: 			const std::vector<WifiText::PickerRow> rows = WifiText::pickerRows(answer.inRange, answer.saved, answer.current,
372: 				answer.savedKnown, answer.currentKnown);
373: 			mSaved = answer.saved;
374: 			mSavedKnown = answer.savedKnown;
375: 			// The network the device is on, as the rows have it: from the
376: 			// saved list's active profile when current could not say.
377: 			mCurrent.clear();
378: 			mCurrentProfile.clear();
379: 			for (const auto& row : rows)
380: 				if (row.connected)
381: 				{
382: 					mCurrent = row.name;
383: 					mCurrentProfile = row.profile;
384: 				}
385: 			load(rows);
386: 		}));
387: }



# FILE emulationstation/es-app/src/guis/GuiWifi.h


## Original lines 1–67
1: #pragma once
2: 
3: #include "GuiComponent.h"
4: #include "components/MenuComponent.h"
5: #include "WifiText.h"
6: 
7: #include <functional>
8: #include <string>
9: #include <vector>
10: 
11: // The Wi-Fi picker behind NETWORK SETTINGS' WI-FI NETWORK row (fork #191,
12: // renamed from WI-FI SSID by D-UI-071; the
13: // maintainer's paradigm of 2026-09-15: the row is the network the device is
14: // on, this list is what is in range). One row per network in range -- the
15: // one joined now first and marked CONNECTED, the ones NetworkManager holds a
16: // profile for marked SAVED. A press on a saved row offers CONNECT (with
17: // the key NetworkManager has), FORGET (the manage page's confirmation and
18: // reader) or CANCEL (#318, D-UI-118); a press on the connected row joins it
19: // again at once; a press on any other asks for the key and connects,
20: // which saves it for next time; INPUT MANUALLY takes a hidden network's
21: // name the same way. Once the device is on a network the page that opened
22: // the picker is told, so it rebuilds and reads the connection back.
23: class GuiWifi : public GuiComponent
24: {
25: public:
26: 	GuiWifi(Window* window, const std::string& title, const std::function<void()>& onJoined);
27: 	bool input(InputConfig* config, Input input) override;
28: 	std::vector<HelpPrompt> getHelpPrompts() override;
29: 
30: private:
31: 	// The three answers the list is built from, fetched together off the
32: 	// interface thread.
33: 	struct Answer
34: 	{
35: 		std::vector<std::string> inRange;
36: 		std::vector<WifiText::SavedNetwork> saved;
37: 		std::string current;
38: 		// Whether `wifictl saved` and `wifictl current` answered at all: an
39: 		// empty list and no list are different answers (#308 F-WF-03/06).
40: 		bool savedKnown = false;
41: 		bool currentKnown = false;
42: 	};
43: 
44: 	void load(const std::vector<WifiText::PickerRow>& rows);
45: 	void addRow(const WifiText::PickerRow& row);
46: 	void onSelect(const WifiText::PickerRow& row);
47: 	void chooseProfile(const std::string& name);
48: 	// name is the network as the player sees it; joinAs the name `wifictl
49: 	// join` takes (WifiText::joinName, manualJoinName).
50: 	void act(WifiText::PressAction action, const std::string& name, const std::string& joinAs);
51: 	void onManualInput();
52: 	void onRefresh(bool rescan = true);
53: 	void join(const std::string& name, const std::string& profile);
54: 	void checkSecurityAndConnect(const std::string& name);
55: 	void askKeyAndConnect(const std::string& name);
56: 	void connect(const std::string& name, const std::string& key, bool openNetwork = false);
57: 	void joined(const std::string& name);
58: 
59: 	MenuComponent mMenu;
60: 	std::string mTitle;
61: 	std::function<void()> mOnJoined;
62: 	std::vector<WifiText::SavedNetwork> mSaved;
63: 	std::string mCurrent;
64: 	std::string mCurrentProfile;   // the connected row's profile, for a typed name
65: 	bool mSavedKnown;
66: 	bool mWaitingLoad;
67: };



# FILE emulationstation/es-app/tests/unit/WifiTextTests.cpp


## Original lines 1–352
1: // The Wi-Fi rows' pure text (fork #191), checked without a device.
2: //
3: // Runs against es-app/src/WifiText.cpp alone: the lines wifictl prints for
4: // the interface -- saved, current, forget -- including the ones nobody
5: // meant to write. A parser is judged on its junk, so most of these are junk.
6: 
7: #include "doctest/doctest.h"
8: 
9: #include "WifiText.h"
10: 
11: #include <string>
12: #include <type_traits>
13: #include <vector>
14: 
15: using namespace WifiText;
16: 
17: TEST_CASE("parseSaved: two remembered networks, the one in use first, as wifictl saved prints them")
18: {
19: 	auto networks = parseSaved({ "Home Wi-Fi\tactive", "Cafe: Guest\tsaved" });
20: 	REQUIRE(networks.size() == 2);
21: 	CHECK(networks[0].name == "Home Wi-Fi");
22: 	CHECK(networks[0].inUse);
23: 	CHECK(networks[1].name == "Cafe: Guest");
24: 	CHECK_FALSE(networks[1].inUse);
25: }
26: 
27: TEST_CASE("parseSavedLine keeps a name as NetworkManager has it: case, inner spaces, a colon, an edge space")
28: {
29: 	SavedNetwork network;
30: 	CHECK(parseSavedLine("MyHome_5g\tsaved", network));
31: 	CHECK(network.name == "MyHome_5g");            // not upper-cased: the name is case-sensitive
32: 	CHECK(parseSavedLine("  two  spaces \tactive", network));
33: 	CHECK(network.name == "  two  spaces ");        // every space kept, the flag read after the tab
34: 	CHECK(network.inUse);
35: 	CHECK(parseSavedLine("a\tb\tsaved", network));  // a tab inside a name: the flag is after the last one
36: 	CHECK(network.name == "a\tb");
37: 	CHECK_FALSE(network.inUse);
38: }
39: 
40: TEST_CASE("parseSavedLine tolerates a trailing CR and nothing else that is not a network")
41: {
42: 	SavedNetwork network;
43: 	CHECK(parseSavedLine("Home\tactive\r", network));
44: 	CHECK(network.name == "Home");
45: 	CHECK(network.inUse);
46: 
47: 	CHECK_FALSE(parseSavedLine("", network));
48: 	CHECK_FALSE(parseSavedLine("Home", network));               // no tab
49: 	CHECK_FALSE(parseSavedLine("\tactive", network));           // no name
50: 	CHECK_FALSE(parseSavedLine("Home\tyes", network));          // nmcli's own word, not wifictl's
51: 	CHECK_FALSE(parseSavedLine("Home\tACTIVE", network));       // the flag is exact
52: 	CHECK_FALSE(parseSavedLine("Home\tactive extra", network));
53: 	CHECK_FALSE(parseSavedLine("Home\t", network));
54: }
55: 
56: TEST_CASE("parseSaved passes junk lines over and keeps the order of the rest")
57: {
58: 	auto networks = parseSaved({ "", "Error: NetworkManager is not running.", "B\tsaved", "junk\tmaybe", "A\tactive", "\tsaved" });
59: 	REQUIRE(networks.size() == 2);
60: 	CHECK(networks[0].name == "B");
61: 	CHECK(networks[1].name == "A");
62: 	CHECK(networks[1].inUse);
63: 	CHECK(parseSaved({}).empty());
64: 	CHECK(parseSaved({ "", "\r" }).empty());
65: }
66: 
67: TEST_CASE("parseCurrent: the first line is the SSID, CR dropped, spaces kept; none is empty")
68: {
69: 	CHECK(parseCurrent({ "Home Wi-Fi" }) == "Home Wi-Fi");
70: 	CHECK(parseCurrent({ "Home Wi-Fi\r" }) == "Home Wi-Fi");
71: 	CHECK(parseCurrent({ " edge " }) == " edge ");
72: 	CHECK(parseCurrent({ "", "Late" }) == "Late");      // an empty first line is not an answer
73: 	CHECK(parseCurrent({}) == "");
74: 	CHECK(parseCurrent({ "", "\r" }) == "");
75: }
76: 
77: TEST_CASE("parseForget reads the word, not the absence of an error")
78: {
79: 	auto both = parseForget({ "forgotten", "disconnected" });
80: 	CHECK(both.forgotten);
81: 	CHECK(both.disconnected);
82: 
83: 	auto one = parseForget({ "forgotten" });
84: 	CHECK(one.forgotten);
85: 	CHECK_FALSE(one.disconnected);
86: 
87: 	auto none = parseForget({});
88: 	CHECK_FALSE(none.forgotten);
89: 	CHECK_FALSE(none.disconnected);
90: 
91: 	// A "disconnected" with nothing forgotten before it is not a forget.
92: 	auto orphan = parseForget({ "disconnected" });
93: 	CHECK_FALSE(orphan.forgotten);
94: 	CHECK_FALSE(orphan.disconnected);
95: 
96: 	auto junk = parseForget({ "Error: unknown connection 'x'.", "FORGOTTEN", "forgotten " });
97: 	CHECK_FALSE(junk.forgotten);
98: 
99: 	auto cr = parseForget({ "forgotten\r", "disconnected\r" });
100: 	CHECK(cr.forgotten);
101: 	CHECK(cr.disconnected);
102: }
103: 
104: TEST_CASE("pickerRows: the joined network first, the rest in the scan's order, the saved ones marked")
105: {
106: 	auto rows = pickerRows({ "Cafe: Guest", "Home Wi-Fi", "Library" }, { { "Home Wi-Fi", true }, { "Cafe: Guest", false } }, "Home Wi-Fi");
107: 	REQUIRE(rows.size() == 3);
108: 	CHECK(rows[0].name == "Home Wi-Fi");
109: 	CHECK(rows[0].connected);
110: 	CHECK(rows[0].saved);
111: 	CHECK(rows[1].name == "Cafe: Guest");
112: 	CHECK_FALSE(rows[1].connected);
113: 	CHECK(rows[1].saved);
114: 	CHECK(rows[2].name == "Library");
115: 	CHECK_FALSE(rows[2].connected);
116: 	CHECK_FALSE(rows[2].saved);
117: }
118: 
119: TEST_CASE("pickerRows: a saved network out of range is not a row; the joined one is, even when the scan missed it")
120: {
121: 	auto rows = pickerRows({ "Library" }, { { "Home Wi-Fi", true }, { "Office", false } }, "Home Wi-Fi");
122: 	REQUIRE(rows.size() == 2);
123: 	CHECK(rows[0].name == "Home Wi-Fi");
124: 	CHECK(rows[0].connected);
125: 	CHECK(rows[1].name == "Library");
126: 	CHECK_FALSE(rows[1].saved);
127: }
128: 
129: TEST_CASE("pickerRows drops empty names and repeats, keeps a name's case, and has no connected row when the device is on none")
130: {
131: 	auto rows = pickerRows({ "", "Cafe: Guest\r", "Cafe: Guest", "cafe: guest" }, {}, "");
132: 	REQUIRE(rows.size() == 2);
133: 	CHECK(rows[0].name == "Cafe: Guest");
134: 	CHECK_FALSE(rows[0].connected);
135: 	CHECK_FALSE(rows[0].saved);
136: 	CHECK(rows[1].name == "cafe: guest");
137: }
138: 
139: TEST_CASE("parseJoin reads the word, not the absence of an error")
140: {
141: 	CHECK(parseJoin({ "joined" }));
142: 	CHECK(parseJoin({ "joined\r" }));
143: 	CHECK_FALSE(parseJoin({}));
144: 	CHECK_FALSE(parseJoin({ "" }));
145: 	CHECK_FALSE(parseJoin({ "Error: Connection activation failed." }));
146: }
147: 
148: // ------------------------------------------------------ #308 F-WF-03/05/06/08
149: 
150: TEST_CASE("pickerRows: a saved list that could not be asked leaves every row unknown, not unsaved (#308 2 claude F-WF-03, gpt F-WF-06)")
151: {
152: 	// wifictl saved exits 1 when NetworkManager cannot be asked, "so a
153: 	// caller cannot read a silence as none"; the picker read it as none, and
154: 	// a press on the player's own network asked for a key and rebuilt its
155: 	// profile from what was typed.
156: 	auto rows = pickerRows({ "Home Wi-Fi", "Library" }, {}, "Home Wi-Fi", false, true);
157: 	REQUIRE(rows.size() == 2);
158: 	CHECK(rows[0].connected);
159: 	CHECK_FALSE(rows[0].savedKnown);
160: 	CHECK_FALSE(rows[1].savedKnown);
161: 	CHECK_FALSE(rows[1].saved);
162: 
163: 	// And an answered list is known, as it always was.
164: 	auto known = pickerRows({ "Library" }, {}, "", true, true);
165: 	REQUIRE(known.size() == 1);
166: 	CHECK(known[0].savedKnown);
167: }
168: 
169: TEST_CASE("pickerRows: a current that could not be asked takes the connected row from the saved list's active profile (#308 F-WF-03)")
170: {
171: 	// wifictl current exits 2 when NetworkManager cannot be asked; the saved
172: 	// list already says which profile is active.
173: 	auto rows = pickerRows({ "Cafe: Guest", "Home Wi-Fi" }, { { "Home Wi-Fi", true }, { "Cafe: Guest", false } }, "", true, false);
174: 	REQUIRE(rows.size() == 2);
175: 	CHECK(rows[0].name == "Home Wi-Fi");
176: 	CHECK(rows[0].connected);
177: 	CHECK(rows[0].saved);
178: 	CHECK(rows[1].name == "Cafe: Guest");
179: 	CHECK_FALSE(rows[1].connected);
180: }
181: 
182: TEST_CASE("a press: the connected row is checked by a join, a saved one joins, an unknown one is asked again (#308 F-WF-03/05/06)")
183: {
184: 	// The connected row closed the picker on the snapshot it was built from,
185: 	// with no look at whether the device was still on it (gpt F-WF-05).
186: 	// wifictl join answers "joined" at once for the active profile and brings
187: 	// back one that has dropped, so a press on it goes that way.
188: 	PickerRow connected{ "Home Wi-Fi", true, true };
189: 	CHECK(pressAction(connected) == PressAction::Join);
190: 	// A saved network the device is not on is offered CONNECT / FORGET /
191: 	// CANCEL (#318, D-UI-118); the connected one, saved or not, joins at once.
192: 	PickerRow saved{ "Cafe: Guest", true, false };
193: 	CHECK(pressAction(saved) == PressAction::ChooseSaved);
194: 	PickerRow savedConnected{ "Home Wi-Fi", true, true };
195: 	CHECK(pressAction(savedConnected) == PressAction::Join);
196: 	PickerRow other{ "Library", false, false };
197: 	CHECK(pressAction(other) == PressAction::AskKey);
198: 	PickerRow unknown{ "Library", false, false, false };
199: 	CHECK(pressAction(unknown) == PressAction::CheckAgain);
200: 	PickerRow unknownConnected{ "Home Wi-Fi", false, true, false };
201: 	CHECK(pressAction(unknownConnected) == PressAction::Join);   // the device is on it: it has a profile
202: 
203: 	// INPUT MANUALLY, the same rules for a typed name.
204: 	const std::vector<SavedNetwork> profiles = { { "Home Wi-Fi", true }, { "Hidden", false } };
205: 	CHECK(manualAction("Home Wi-Fi", "Home Wi-Fi", profiles, true) == PressAction::Join);
206: 	CHECK(manualAction("Hidden", "Home Wi-Fi", profiles, true) == PressAction::Join);
207: 	CHECK(manualAction("Guest", "Home Wi-Fi", profiles, true) == PressAction::AskKey);
208: 	CHECK(manualAction("Guest", "Home Wi-Fi", {}, false) == PressAction::CheckAgain);
209: 	CHECK(manualAction("", "", {}, true) == PressAction::AskKey);
210: }
211: 
212: TEST_CASE("the joined toast is <subject> : <outcome>, the name as it is (#308 2 claude F-WF-08, gpt F-WF-08)")
213: {
214: 	// It was "CONNECTED TO" + name: a translated fragment a translation could
215: 	// not move, and not the toast shape the style guide sets.
216: 	CHECK(joinedNotice("Home Wi-Fi", "CONNECTED") == "Home Wi-Fi : CONNECTED");
217: 	CHECK(joinedNotice("cafe guest", "CONNECT\xC3\x89") == "cafe guest : CONNECT\xC3\x89");
218: }
219: 
220: 
221: TEST_CASE("a join that did not happen: NetworkManager not answering is not a key that changed (#308 2 claude F-WF-03, gpt F-WF-06)")
222: {
223: 	// wifictl join: exit 2 when NetworkManager could not be asked -- nothing
224: 	// was tried, and the key is not in question. The picker told the player
225: 	// to forget the network and join it again with a new key.
226: 	CHECK(joinFailure(2) == JoinFailure::ServiceNotAnswering);
227: 	// Exit 1: the profile would not come up, or the name is not a saved
228: 	// network -- the key may be why. 124 is the timeout's own bound on the
229: 	// activation: the same may.
230: 	CHECK(joinFailure(1) == JoinFailure::MayBeKey);
231: 	CHECK(joinFailure(124) == JoinFailure::MayBeKey);
232: 	// A run that exited 0 without printing "joined" (parseJoin) is not a
233: 	// join; nothing in it points away from the key either.
234: 	CHECK(joinFailure(0) == JoinFailure::MayBeKey);
235: }
236: 
237: // wifictl speaks two names (#308 2-wifi claude F-WF-12, gpt F-WF-03): current
238: // and list the SSID, saved and join the profile's name -- which need not be
239: // the SSID (a renamed profile, or NetworkManager's "Home 1"). Stream B's
240: // join now writes the SSID to wifi.ssid and is judged on this device's
241: // adapter; the picker still handed join the SSID for the network the device
242: // is on, which is no profile's name, and said COULDN'T CONNECT TO HOME with
243: // forget-and-rejoin advice about the network the player was on.
244: TEST_CASE("the connected row joins by the profile that is up, not by its SSID (#308 2 claude F-WF-12, gpt F-WF-03)")
245: {
246: 	const std::vector<SavedNetwork> profiles = { { "Home 1", true }, { "Cafe", false } };
247: 	auto rows = pickerRows({ "Home", "Cafe", "Library" }, profiles, "Home", true, true);
248: 	REQUIRE(rows.size() == 3);
249: 	CHECK(rows[0].name == "Home");        // the SSID, as the player knows it
250: 	CHECK(rows[0].connected);
251: 	CHECK(rows[0].saved);                 // joined through a profile: it has one
252: 	CHECK(rows[0].profile == "Home 1");
253: 	CHECK(joinName(rows[0]) == "Home 1");
254: 	CHECK(rows[1].name == "Cafe");
255: 	CHECK(joinName(rows[1]) == "Cafe");   // a profile named as its SSID
256: 	CHECK(joinName(rows[2]) == "Library");
257: 
258: 	// Typed: the current network's name joins by its profile too.
259: 	CHECK(manualJoinName("Home", "Home", "Home 1") == "Home 1");
260: 	CHECK(manualJoinName("Cafe", "Home", "Home 1") == "Cafe");
261: 	CHECK(manualJoinName("Hidden", "Home", "") == "Hidden");
262: 
263: 	// A profile named as the SSID is the one, even with another up (a second
264: 	// adapter): the name decides before the active flag.
265: 	auto two = pickerRows({ "Home" }, { { "Work", true }, { "Home", true } }, "Home", true, true);
266: 	REQUIRE(two.size() == 1);
267: 	CHECK(two[0].profile == "Home");
268: 	// Two up and neither named as the SSID: no guess; the row joins by its name.
269: 	auto ambiguous = pickerRows({ "Home" }, { { "Work", true }, { "Home 1", true } }, "Home", true, true);
270: 	REQUIRE(ambiguous.size() == 1);
271: 	CHECK(ambiguous[0].profile.empty());
272: 	CHECK(joinName(ambiguous[0]) == "Home");
273: 
274: 	// Could not ask which are saved: no profile is claimed.
275: 	auto unknown = pickerRows({ "Home" }, {}, "Home", false, true);
276: 	REQUIRE(unknown.size() == 1);
277: 	CHECK(unknown[0].profile.empty());
278: 	CHECK_FALSE(unknown[0].saved);
279: }
280: 
281: // The audit of the fix round, gpt G2-E-app-01 (handed to stream E1): the
282: // name decided before the active flag, so a saved profile named as the SSID
283: // but not in use outranked the one profile that was -- NetworkManager's
284: // "Home 1" beside an old "Home" -- and the connected row's FORGET and JOIN
285: // went to the profile the device was not on.
286: TEST_CASE("the connected row's profile is the one in use, over an inactive namesake (audit of the fix round, gpt G2-E-app-01)")
287: {
288: 	auto rows = pickerRows({ "Home" }, { { "Home", false }, { "Home 1", true } }, "Home", true, true);
289: 	REQUIRE(rows.size() == 1);
290: 	CHECK(rows[0].connected);
291: 	CHECK(rows[0].profile == "Home 1");
292: 	CHECK(joinName(rows[0]) == "Home 1");
293: 
294: 	// Two up (a second adapter) and neither named as the SSID: which one is
295: 	// this device's cannot be told, and the namesake is known not to be in
296: 	// use, so none is claimed.
297: 	auto twoUp = pickerRows({ "Home" }, { { "Home", false }, { "Work", true }, { "Home 1", true } }, "Home", true, true);
298: 	REQUIRE(twoUp.size() == 1);
299: 	CHECK(twoUp[0].profile.empty());
300: 	CHECK(joinName(twoUp[0]) == "Home");
301: 
302: 	// None up -- the list's flags behind the join -- and a namesake: the
303: 	// namesake, as before.
304: 	auto noneUp = pickerRows({ "Home" }, { { "Home", false } }, "Home", true, true);
305: 	REQUIRE(noneUp.size() == 1);
306: 	CHECK(noneUp[0].profile == "Home");
307: }
308: 
309: // Audit of the fixes (#307), E2 claude G-E2-01: joinWifiNetwork returned
310: // bool (true = joined) and returns the exit code now (0 = joined), so a
311: // caller left testing it as a truth value compiles and reads every join
312: // backwards. The answer is a type that does not turn into a bool.
313: TEST_CASE("a join's answer is not a truth value (#308 F-WF-03/06; audit G-E2-01)")
314: {
315: 	static_assert(!std::is_convertible<JoinAnswer, bool>::value, "a join's answer must not read as a truth value");
316: 	static_assert(!std::is_constructible<bool, JoinAnswer>::value, "nor be cast to one");
317: 	CHECK(JoinAnswer{ 0 }.joined());
318: 	CHECK_FALSE(JoinAnswer{ 1 }.joined());
319: 	CHECK_FALSE(JoinAnswer{ 2 }.joined());
320: 	CHECK_FALSE(JoinAnswer().joined());
321: 	CHECK(joinFailure(JoinAnswer{ 2 }.code) == JoinFailure::ServiceNotAnswering);
322: }
323: 
324: TEST_CASE("saved SSIDs preserve renamed profiles and escaped fields (#535)")
325: {
326: 	SavedNetwork profile;
327: 	REQUIRE(parseSavedDetailsLine("Remembered\tCafe\\tGuest\\\\room\tsaved", profile));
328: 	CHECK(profile.name == "Remembered");
329: 	CHECK(profile.ssid == "Cafe\tGuest\\room");
330: 	CHECK_FALSE(parseSavedDetailsLine("Name\tactive", profile));
331: 	CHECK_FALSE(parseSavedDetailsLine("Name\tSSID\tother", profile));
332: 	CHECK_FALSE(parseSavedDetailsLine("Name\t\tsaved", profile));
333: 	std::vector<SavedNetwork> saved = { { "Remembered", false, "Cafe" } };
334: 	auto rows = pickerRows({"Cafe", "Open"}, saved, "");
335: 	REQUIRE(rows.size() == 2);
336: 	CHECK(rows[0].saved);
337: 	CHECK(joinName(rows[0]) == "Remembered");
338: 	CHECK(pressAction(rows[0]) == PressAction::ChooseSaved);
339: 	CHECK_FALSE(rows[1].saved);
340: 	CHECK(manualAction("Cafe", "", saved, true) == PressAction::Join);
341: 	CHECK(preferredProfile("Cafe", saved) == "Remembered");
342: 	// An active profile on another radio/network cannot claim this row.
343: 	saved.push_back({ "Other", true, "Office" });
344: 	rows = pickerRows({"Cafe"}, saved, "Cafe");
345: 	CHECK(rows[0].profile == "Remembered");
346: 	saved.push_back({ "Another", false, "Cafe" });
347: 	CHECK(profilesForSsid("Cafe", saved).size() == 2);
348: 	CHECK(preferredProfile("Cafe", saved).empty());
349: 	rows = pickerRows({"Cafe"}, saved, "");
350: 	CHECK(rows[0].saved);
351: 	CHECK(rows[0].profile.empty()); // requires the explicit profile chooser
352: }



# FILE emulationstation/es-core/src/guis/GuiTextEditPopup.cpp


## Original lines 1–86
1: #include "guis/GuiTextEditPopup.h"
2: 
3: #include "components/ButtonComponent.h"
4: #include "components/MenuComponent.h"
5: #include "LocaleES.h"
6: #include "components/TextEditComponent.h"
7: 
8: GuiTextEditPopup::GuiTextEditPopup(Window* window, const std::string& title, const std::string& initValue, 
9: 	const std::function<void(const std::string&)>& okCallback, bool multiLine, const char* acceptBtnText)
10: 	: GuiComponent(window), mBackground(window, ":/frame.png"), mGrid(window, Vector2i(1, 3)), mMultiLine(multiLine)
11: {
12: 	setTag("popup");
13: 
14: 	auto theme = ThemeData::getMenuTheme();
15: 	mBackground.setImagePath(theme->Background.path);
16: 	mBackground.setEdgeColor(theme->Background.color);
17: 	mBackground.setCenterColor(theme->Background.centerColor);
18: 	mBackground.setCornerSize(theme->Background.cornerSize);
19: 	mBackground.setPostProcessShader(theme->Background.menuShader);
20: 
21: 	addChild(&mBackground);
22: 	addChild(&mGrid);
23: 
24: 	mTitle = std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(title), theme->Title.font, theme->Title.color, ALIGN_CENTER);
25: 
26: 	mText = std::make_shared<TextEditComponent>(mWindow);
27: 	mText->setValue(initValue);
28: 
29: 	if(!multiLine)
30: 		mText->setCursor(initValue.size());
31: 
32: 	std::vector< std::shared_ptr<ButtonComponent> > buttons;
33: 	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, acceptBtnText, acceptBtnText, [this, okCallback] { okCallback(mText->getValue()); delete this; }));
34: 	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CLEAR"), _("CLEAR"), [this, okCallback] { okCallback(""); delete this; }));
35: 	buttons.push_back(std::make_shared<ButtonComponent>(mWindow, _("CANCEL"), _("DISCARD CHANGES"), [this] { delete this; })); 
36: 
37: 	mButtonGrid = makeButtonGrid(mWindow, buttons);
38: 
39: 	mGrid.setEntry(mTitle, Vector2i(0, 0), false, true);
40: 	mGrid.setEntry(mText, Vector2i(0, 1), true, false, Vector2i(1, 1), GridFlags::BORDER_TOP | GridFlags::BORDER_BOTTOM);
41: 	mGrid.setEntry(mButtonGrid, Vector2i(0, 2), true, false);
42: 
43: 	float textHeight = mText->getFont()->getHeight();
44: 	if(multiLine)
45: 		textHeight *= 6;
46: 	mText->setSize(0, textHeight);
47: 
48: 	setSize(Renderer::getScreenWidth() * 0.5f, mTitle->getFont()->getHeight() + textHeight + mButtonGrid->getSize().y() + 40);
49: 	setPosition((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2);
50: }
51: 
52: void GuiTextEditPopup::onSizeChanged()
53: {
54: 	GuiComponent::onSizeChanged();
55: 
56: 	mBackground.fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
57: 
58: 	mText->setSize(mSize.x() - 40, mText->getSize().y());
59: 
60: 	// update grid
61: 	mGrid.setRowHeightPerc(0, mTitle->getFont()->getHeight() / mSize.y());
62: 	mGrid.setRowHeightPerc(2, mButtonGrid->getSize().y() / mSize.y());
63: 	mGrid.setSize(mSize);
64: }
65: 
66: bool GuiTextEditPopup::input(InputConfig* config, Input input)
67: {
68: 	if(GuiComponent::input(config, input))
69: 		return true;
70: 
71: 	// pressing back when not text editing closes us
72: 	if(config->isMappedTo(BUTTON_BACK, input) && input.value)
73: 	{
74: 		delete this;
75: 		return true;
76: 	}
77: 
78: 	return false;
79: }
80: 
81: std::vector<HelpPrompt> GuiTextEditPopup::getHelpPrompts()
82: {
83: 	std::vector<HelpPrompt> prompts = mGrid.getHelpPrompts();
84: 	prompts.push_back(HelpPrompt(BUTTON_BACK, _("BACK")));
85: 	return prompts;
86: }



# FILE emulationstation/es-core/src/guis/GuiTextEditPopupKeyboard.cpp


## Original lines 1–533
1: #include "guis/GuiTextEditPopupKeyboard.h"
2: #include "components/MenuComponent.h"
3: #include "utils/StringUtil.h"
4: #include "Log.h"
5: #include "LocaleES.h"
6: #include "SystemConf.h"
7: 
8: #define OSK_WIDTH (Renderer::ScreenSettings::fullScreenMenus() ? Renderer::getScreenWidth() : Renderer::getScreenWidth() * 0.78f)
9: #define OSK_HEIGHT (Renderer::ScreenSettings::fullScreenMenus() ? Renderer::getScreenHeight() : Renderer::getScreenHeight() * 0.60f)
10: 
11: #define OSK_PADDINGX (Renderer::getScreenWidth() * 0.02f)
12: #define OSK_PADDINGY (Renderer::getScreenWidth() * 0.01f)
13: 
14: #define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.0052083333)
15: #define BUTTON_LAYER_SIZE (4)
16: 
17: std::vector<std::vector<const char*>> kbUs {
18: 
19: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_", "+", "DEL" },
20: 	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "DEL" },
21: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_", "+", "DEL" },
22: 	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "DEL" },
23: 
24: 	{ "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "{", "}", "OK" },
25: 	{ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "OK" },
26: 	{ "à", "ä", "è", "ë", "ì", "ï", "ò", "ö", "ù", "ü", "¨", "¿", "OK" },
27: 	{ "à", "ä", "è", "ë", "ì", "ï", "ò", "ö", "ù", "ü", "¨", "¿", "OK" },
28: 
29: 	{ "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "\"", "|", "-rowspan-" },
30: 	{ "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "'", "\\", "-rowspan-" },
31: 	{ "á", "â", "é", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "-rowspan-" },
32: 	{ "á", "â", "é", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "-rowspan-" },
33: 
34: 	{ "~", "z", "x", "c", "v", "b", "n", "m", ",", ".", "?", "ALT", "-colspan-" },
35: 	{ "`", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "/", "ALT", "-colspan-" },
36: 	{ "€", "", "", "", "", "", "", "", "", "", "", "ALT", "-colspan-" },
37: 	{ "€", "", "", "", "", "", "", "", "", "", "", "ALT", "-colspan-" },
38: 
39: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
40: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
41: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
42: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
43: };
44: 
45: std::vector<std::vector<const char*>> kbFr {
46: 	{ "&", "é", "\"", "'", "(", "#", "è", "!", "ç", "à", ")", "-", "DEL" },
47: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "_", "DEL" },
48: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "_", "DEL" },
49: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "@", "_", "DEL" },
50: 
51: 	{ "a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "^", "$", "OK" },
52: 	{ "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "¨", "*", "OK" },
53: 	{ "à", "ä", "ë", "ì", "ï", "ò", "ö", "ü", "\\", "|", "§", "°", "OK" },
54: 	{ "à", "ä", "ë", "ì", "ï", "ò", "ö", "ü", "\\", "|", "§", "°", "OK" },
55: 
56: 	{ "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "ù", "`", "-rowspan-" },
57: 	{ "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "%", "£", "-rowspan-" },
58: 	{ "á", "â", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "¿", "-rowspan-" },
59: 	{ "á", "â", "ê", "í", "î", "ó", "ô", "ú", "û", "ñ", "¡", "¿", "-rowspan-" },
60: 
61: 	{ "<", "w", "x", "c", "v", "b", "n", ",", ";", ":", "=", "ALT", "-colspan-" },
62: 	{ ">", "W", "X", "C", "V", "B", "N", "?", ".", "/", "+", "ALT", "-colspan-" },
63: 	{ "€", "[", "]", "{", "}", "", "", "", "", "", "", "ALT", "-colspan-" },
64: 	{ "€", "[", "]", "{", "}", "", "", "", "", "", "", "ALT", "-colspan-" },
65: 
66: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
67: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
68: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
69: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
70: };
71: 
72: std::vector<std::vector<const char*>> kbKr{
73: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "DEL" },
74: 	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "DEL" },
75: 	{ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "DEL" },
76: 	{ "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "DEL" },
77: 
78: 	{ "ㅂ", "ㅈ", "ㄷ", "ㄱ", "ㅅ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ", "[", "]", "OK" },
79: 	{ "ㅃ", "ㅉ", "ㄸ", "ㄲ", "ㅆ", "ㅛ", "ㅕ", "ㅑ", "ㅒ", "ㅖ", "{", "}", "OK" },
80: 	{ "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "OK" },
81: 	{ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "OK" },
82: 
83: 	{ "ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", ";", "'", "\\", "-rowspan-" },
84: 	{ "ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", ":", "\"", "|", "-rowspan-" },
85: 	{ "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\", "-rowspan-" },
86: 	{ "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "|", "-rowspan-" },
87: 
88: 	{ "ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ", "ㅜ", "ㅡ", ",", ".", "/", "`", "ALT", "-colspan-" },
89: 	{ "ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ", "ㅜ", "ㅡ", "<", ">", "?", "~", "ALT", "-colspan-" },
90: 	{ "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "`", "ALT", "-colspan-" },
91: 	{ "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "~", "ALT", "-colspan-" },
92: 
93: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
94: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
95: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" },
96: 	{ "SHIFT", "-colspan-", "SPACE", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "-colspan-", "CLEAR", "-colspan-", "CANCEL", "-colspan-" }
97: };
98: 
99: GuiTextEditPopupKeyboard::GuiTextEditPopupKeyboard(Window* window, const std::string& title, const std::string& initValue,
100: 	const std::function<void(const std::string&)>& okCallback, bool multiLine, const std::string acceptBtnText)
101: 	: GuiComponent(window), mBackground(window, ":/frame.png"), mGrid(window, Vector2i(1, 6)), mMultiLine(multiLine)
102: {
103: 	setTag("popup");
104: 
105: 	mOkCallback = okCallback;
106: 
107: 	auto theme = ThemeData::getMenuTheme();
108: 	mBackground.setImagePath(theme->Background.path);
109: 	mBackground.setEdgeColor(theme->Background.color);
110: 	mBackground.setCenterColor(theme->Background.centerColor);
111: 	mBackground.setCornerSize(theme->Background.cornerSize);
112: 	mBackground.setPostProcessShader(theme->Background.menuShader);
113: 
114: 	addChild(&mBackground);
115: 	addChild(&mGrid);
116: 
117: 	mTitle = std::make_shared<TextComponent>(mWindow, Utils::String::toUpper(title), theme->Title.font, theme->Title.color, ALIGN_CENTER);
118: 	
119: 	mKeyboardGrid = std::make_shared<ComponentGrid>(mWindow, Vector2i(kbUs[0].size(), kbUs.size() / BUTTON_LAYER_SIZE));
120: 
121: 	mText = std::make_shared<TextEditComponent>(mWindow);
122: 	mText->setValue(initValue);
123: 
124: 	if (!multiLine)
125: 		mText->setCursor(initValue.size());
126: 
127: 	// Header
128: 	mGrid.setEntry(mTitle, Vector2i(0, 0), false, true);
129: 
130: 	// Text edit add
131: 	mGrid.setEntry(mText, Vector2i(0, 1), true, false, Vector2i(1, 1), GridFlags::BORDER_TOP);
132: 
133: 	std::vector< std::vector< std::shared_ptr<ButtonComponent> > > buttonList;
134: 
135: 	// Keyboard
136: 	// Case for if multiline is enabled, then don't create the keyboard.
137: 	// if (!mMultiLine) 
138: 	{
139: 		std::vector<std::vector<const char*>>* layout = &kbUs;
140: 
141: 		std::string language = SystemConf::getInstance()->get("system.language");
142: 		if (!language.empty())
143: 		{
144: 			auto shortNameDivider = language.find("_");
145: 			if (shortNameDivider != std::string::npos)
146: 				language = Utils::String::toLower(language.substr(0, shortNameDivider));
147: 		}
148: 
149: 		if (language == "fr")
150: 			layout = &kbFr;
151: 		else if (language == "ko")
152: 			layout = &kbKr;
153: 
154: 		for (unsigned int i = 0; i < layout->size() / BUTTON_LAYER_SIZE; i++)
155: 		{			
156: 			std::vector<std::shared_ptr<ButtonComponent>> buttons;
157: 			for (unsigned int j = 0; j < (*layout)[i].size(); j++)
158: 			{
159: 				std::string lower = (*layout)[BUTTON_LAYER_SIZE * i][j];
160: 				if (lower.empty() || lower == "-rowspan-" || lower == "-colspan-")
161: 					continue;
162: 
163: 				std::string upper = (*layout)[BUTTON_LAYER_SIZE * i + 1][j];
164: 				std::string lowerAlted = (*layout)[BUTTON_LAYER_SIZE * i + 2][j];
165: 				std::string upperAlted = (*layout)[BUTTON_LAYER_SIZE * i + 3][j];
166: 
167: 				std::shared_ptr<ButtonComponent> button = nullptr;
168: 
169: 				if (lower == "DEL")
170: 				{
171: 					lower = _U("\uF177");
172: 					upper = _U("\uF177");
173: 					lowerAlted = _U("\uF177");
174: 					upperAlted = _U("\uF177");
175: 				}
176: 				else if (lower == "OK")
177: 				{
178: 					lower = _U("\uF058");
179: 
180: 					if (mMultiLine)
181: 					{
182: 						upper = _U("\uF149");
183: 						lowerAlted = _U("\uF149");
184: 						upperAlted = _U("\uF149");
185: 					}
186: 					else
187: 					{
188: 						upper = _U("\uF058");
189: 						lowerAlted = _U("\uF058");
190: 						upperAlted = _U("\uF058");
191: 					}
192: 				}
193: 				else if (lower == "SPACE")
194: 				{
195: 					lower = " ";
196: 					upper = " ";
197: 				}
198: 				else if (lower != "SHIFT" && lower.length() > 1)
199: 				{
200: 					lower = _(lower.c_str());
201: 					upper = _(upper.c_str());
202: 					lowerAlted = _(lowerAlted.c_str());
203: 					upperAlted = _(upperAlted.c_str());
204: 				}
205: 
206: 				if (lower == "SHIFT")
207: 				{
208: 					// Special case for shift key
209: 					mShiftButton = std::make_shared<ButtonComponent>(mWindow, _U("\uF176"), _("SHIFTS FOR UPPER, LOWER, AND SPECIAL"), [this] { shiftKeys(); }, false);					
210: 					button = mShiftButton;
211: 				}
212: 				else if (lower == "ALT")
213: 				{
214: 					mAltButton = std::make_shared<ButtonComponent>(mWindow, _U("\uF141"), _("ALT GR"), [this] { altKeys(); }, false);
215: 					button = mAltButton;
216: 				}
217: 				else
218: 					button = makeButton(lower, upper, lowerAlted, upperAlted);
219: 
220: 				button->setPadding(Vector4f(BUTTON_GRID_HORIZ_PADDING / 4.0f, BUTTON_GRID_HORIZ_PADDING / 4.0f, BUTTON_GRID_HORIZ_PADDING / 4.0f, BUTTON_GRID_HORIZ_PADDING / 4.0f));
221: 				button->setRenderNonFocusedBackground(false);
222: 				buttons.push_back(button);
223: 
224: 				int colSpan = 1;
225: 				for (unsigned int cs = j + 1; cs < (*layout)[i].size(); cs++)
226: 				{
227: 					if (std::string((*layout)[BUTTON_LAYER_SIZE * i][cs]) == "-colspan-")
228: 						colSpan++;
229: 					else
230: 						break;
231: 				}
232: 				
233: 				int rowSpan = 1;
234: 				for (unsigned int cs = (BUTTON_LAYER_SIZE * i) + BUTTON_LAYER_SIZE; cs < layout->size(); cs += BUTTON_LAYER_SIZE)
235: 				{
236: 					if (std::string((*layout)[cs][j]) == "-rowspan-")
237: 						rowSpan++;
238: 					else
239: 						break;
240: 				}
241: 
242: 				mKeyboardGrid->setEntry(button, Vector2i(j, i), true, true, Vector2i(colSpan, rowSpan));
243: 
244: 				buttonList.push_back(buttons);
245: 			}
246: 		}		
247: 		// END KEYBOARD IF
248: 	}
249: 
250: 	// Add keyboard keys
251: 	mGrid.setEntry(mKeyboardGrid, Vector2i(0, 2), true, true, Vector2i(2, 4));
252: 
253: 	// Determine size from text size
254: 	float textHeight = mText->getFont()->getHeight();
255: 	if (multiLine)
256: 		textHeight *= 4;
257: 
258: 	mText->setSize(0, textHeight);
259: 
260: 	mGrid.setUnhandledInputCallback([this](InputConfig* config, Input input) -> bool 
261: 	{		
262: 		if (config->isMappedLike("down", input)) 
263: 		{
264: 			mGrid.setCursorTo(mText);
265: 			return true;
266: 		}
267: 		else if (config->isMappedLike("up", input)) 
268: 		{
269: 			mGrid.setCursorTo(mKeyboardGrid);
270: 			return true;
271: 		}
272: 		else if (config->isMappedLike("left", input))
273: 		{		
274: 			if (mGrid.getSelectedComponent() == mKeyboardGrid)
275: 			{
276: 				Vector2i curCursor = mKeyboardGrid->getCursor();
277: 				mKeyboardGrid->setCursorTo(Vector2i(kbUs[0].size() - 1, curCursor.y()));
278: 				return true;
279: 			}
280: 		}
281: 		else if (config->isMappedLike("right", input))
282: 		{
283: 			if (mGrid.getSelectedComponent() == mKeyboardGrid)
284: 			{
285: 				Vector2i curCursor = mKeyboardGrid->getCursor();
286: 				mKeyboardGrid->setCursorTo(Vector2i(0, curCursor.y()));
287: 				return true;
288: 			}
289: 		}
290: 
291: 		return false;
292: 	});
293: 
294: 	
295: 	// If multiline, set all diminsions back to default, else draw size for keyboard.
296: 	if (mMultiLine) 
297: 	{
298: 		if (Renderer::ScreenSettings::fullScreenMenus())
299: 			setSize(OSK_WIDTH, Renderer::getScreenHeight());
300: 		else
301: 			setSize(OSK_WIDTH, OSK_HEIGHT - mText->getFont()->getHeight() + textHeight);
302: 
303: 		setPosition((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2);
304: 	}
305: 	else
306: 	{
307: 		//setSize(OSK_WIDTH, mTitle->getFont()->getHeight() + textHeight + 40 + (Renderer::getScreenHeight() * 0.085f) * 6);
308: 		setSize(OSK_WIDTH, OSK_HEIGHT);
309: 		setPosition((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2);
310: 		animateTo(Vector2f((Renderer::getScreenWidth() - mSize.x()) / 2, (Renderer::getScreenHeight() - mSize.y()) / 2));
311: 	}
312: }
313: 
314: void GuiTextEditPopupKeyboard::onSizeChanged()
315: {
316: 	GuiComponent::onSizeChanged();
317: 
318: 	mBackground.fitTo(mSize, Vector3f::Zero(), Vector2f(-32, -32));
319: 
320: 	mText->setSize(mSize.x() - (2 * OSK_PADDINGX), mText->getSize().y());
321: 
322: 	// update grid
323: 	mGrid.setRowHeight(0, mTitle->getFont()->getHeight() + OSK_PADDINGY);
324: 	mGrid.setRowHeight(1, mText->getSize().y() + 2 * OSK_PADDINGY);
325: 	mGrid.setRowHeight(2, mKeyboardGrid->getSize().y());
326: 	mGrid.setSize(mSize);
327: 
328: 	auto pos = mKeyboardGrid->getPosition();
329: 	auto sz = mKeyboardGrid->getSize();
330: 
331: 	mKeyboardGrid->setSize(mSize.x() - OSK_PADDINGX - OSK_PADDINGX, sz.y() - OSK_PADDINGY); // Small margin between buttons
332: 	mKeyboardGrid->setPosition(OSK_PADDINGX, pos.y());	
333: }
334: 
335: bool GuiTextEditPopupKeyboard::input(InputConfig* config, Input input)
336: {
337: 	if (GuiComponent::input(config, input))
338: 		return true;
339: 
340: 	// pressing start
341: 	if (config->isMappedTo("start", input) && input.value)
342: 	{
343: 		if (mOkCallback)
344: 			mOkCallback(mText->getValue());
345: 
346: 		delete this;
347: 		return true;
348: 	}
349: 
350: 	if ((config->getDeviceId() == DEVICE_KEYBOARD && input.id == SDLK_ESCAPE))
351: 	{
352: 		delete this;
353: 		return true;
354: 	}
355: 
356: 	// pressing back when not text editing closes us
357: 	if (config->isMappedTo(BUTTON_BACK, input) && input.value)
358: 	{
359: 		delete this;
360: 		return true;
361: 	}
362: 
363: 	// For deleting a chara (Left Top Button)
364: 	if (config->isMappedTo("leftshoulder", input) && input.value) {
365: 		bool editing = mText->isEditing();
366: 		if (!editing)
367: 			mText->startEditing();
368: 
369: 		mText->textInput("\b");
370: 
371: 		if (!editing)
372: 			mText->stopEditing();
373: 	}
374: 
375: 	// For Adding a space (Right Top Button)
376: 	if (config->isMappedTo("rightshoulder", input) && input.value)
377: 	{
378: 		bool editing = mText->isEditing();
379: 		if (!editing)
380: 			mText->startEditing();
381: 
382: 		mText->textInput(" ");
383: 
384: 		if (!editing)
385: 			mText->stopEditing();
386: 	}
387: 
388: 	// For Shifting (Y)
389: 	if (config->isMappedTo("y", input) && input.value) 
390: 		shiftKeys();
391: 
392: 	if (config->isMappedTo("x", input) && input.value && mOkCallback != nullptr)
393: 	{
394: 		mOkCallback(""); 
395: 		delete this;
396: 		return true;
397: 	}
398: 
399: 	return false;
400: }
401: 
402: void GuiTextEditPopupKeyboard::toggleKeyState(bool& state, std::shared_ptr<ButtonComponent>& button)
403: {
404: 	state = !state;
405: 
406: 	if (state)
407: 	{
408: 		button->setRenderNonFocusedBackground(true);
409: 		button->setColorShift(0xFF0000FF);
410: 	}
411: 	else
412: 	{
413: 		button->setRenderNonFocusedBackground(false);
414: 		button->removeColorShift();
415: 	}
416: 
417: 	updateKeyboardButtons();
418: }
419: 
420: void GuiTextEditPopupKeyboard::updateKeyboardButtons()
421: {
422: 	for (auto& kb : keyboardButtons)
423: 	{
424: 		const std::string& text = (mAlt && mShift) ? kb.altedShiftedKey
425: 			: (mAlt) ? kb.altedKey
426: 			: (mShift) ? kb.shiftedKey
427: 			: kb.key;
428: 
429: 		auto sz = kb.button->getSize();
430: 		kb.button->setText(text, text, false);
431: 		kb.button->setSize(sz);
432: 	}
433: }
434: 
435: // Shifts the keys when user hits the shift button.
436: void GuiTextEditPopupKeyboard::shiftKeys() 
437: {
438: 	toggleKeyState(mShift, mShiftButton);
439: }
440: 
441: void GuiTextEditPopupKeyboard::altKeys()
442: {
443: 	if (mShift)
444: 		toggleKeyState(mShift, mShiftButton);
445: 
446: 	toggleKeyState(mAlt, mAltButton);
447: }
448: 
449: std::vector<HelpPrompt> GuiTextEditPopupKeyboard::getHelpPrompts()
450: {
451: 	std::vector<HelpPrompt> prompts = mGrid.getHelpPrompts();
452: 
453: 	if (mOkCallback != nullptr)
454: 		prompts.push_back(HelpPrompt("x", _("CLEAR")));
455: 
456: 	prompts.push_back(HelpPrompt("y", _("SHIFT")));
457: 	prompts.push_back(HelpPrompt("start", _("OK")));
458: 	prompts.push_back(HelpPrompt(BUTTON_BACK, _("BACK")));
459: 	prompts.push_back(HelpPrompt("r", _("SPACE")));
460: 	prompts.push_back(HelpPrompt("l", _("DELETE")));
461: 	return prompts;
462: }
463: 
464: std::shared_ptr<ButtonComponent> GuiTextEditPopupKeyboard::makeButton(const std::string& key, const std::string& shiftedKey, const std::string& altedKey, const std::string& altedShiftedKey)
465: {
466: 	std::shared_ptr<ButtonComponent> button = std::make_shared<ButtonComponent>(mWindow, key, key, [this, key, shiftedKey, altedKey, altedShiftedKey]
467: 	{						
468: 		if (key == _U("\uF058") || key.find("OK") != std::string::npos)
469: 		{	
470: 			if (mMultiLine && (mShift || mAlt))
471: 			{
472: 				mText->startEditing(); mText->textInput("\r\n"); mText->stopEditing();
473: 			}
474: 			else
475: 			{
476: 				mOkCallback(mText->getValue());
477: 				delete this;
478: 			}
479: 			return;
480: 		}
481: 		else if (key == _U("\uF177") || key == "DEL")
482: 		{
483: 			mText->startEditing(); mText->textInput("\b"); mText->stopEditing();
484: 			return;
485: 		}
486: 		else if (key == _("SPACE") || key == " ")
487: 		{
488: 			mText->startEditing(); mText->textInput(" "); mText->stopEditing();
489: 			return;
490: 		}
491: 		else if (key == _("CLEAR"))
492: 		{
493: 			mOkCallback(""); 
494: 			delete this;
495: 			return;
496: 		}
497: 		else if (key == _("CANCEL"))
498: 		{
499: 			delete this;
500: 			return;
501: 		}
502: 
503: 		if (mAlt)
504: 		{
505: 			if (mShift && altedShiftedKey.empty())
506: 				return;
507: 			if (altedKey.empty())
508: 				return;
509: 		}
510: 
511: 		mText->startEditing();
512: 
513: 		const char* text;
514: 		if (mAlt && mShift)
515: 			text = altedShiftedKey.c_str();
516: 		else if (mAlt)
517: 			text = altedKey.c_str();
518: 		else if (mShift)
519: 			text = shiftedKey.c_str();
520: 		else
521: 			text = key.c_str();
522: 		mText->textInput(text);
523: 
524: 		mText->stopEditing();
525: 
526: 		if (Utils::String::isKorean(text) && mShift)
527: 			shiftKeys();
528: 	}, false);
529: 	
530: 	KeyboardButton kb(button, key, shiftedKey, altedKey, altedShiftedKey);
531: 	keyboardButtons.push_back(kb);
532: 	return button;
533: }

