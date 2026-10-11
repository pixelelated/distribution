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
