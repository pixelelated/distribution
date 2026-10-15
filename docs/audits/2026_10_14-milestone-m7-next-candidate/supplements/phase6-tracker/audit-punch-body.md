# M7 independent audit punch list

## Executive Summary

The independent audit examined the M7 delta, retaining explicit baseline exclusions and distinguishing actual installed artifacts from helper, source-chroot and private-candidate controls. It derived every criterion before opening prior per-criterion verdicts. Source, original command/child results, selected before/after identities, databases and UI frames support substantial preservation and recovery behavior. The largest remaining evidence scope is final composed installed/native gameplay and save behavior, not a reason to replay already accepted synthetic matrices.

Six audit findings survive: one High (F-002 NoGUI achievement lifecycle), three Medium (F-001 metadata bounds, F-003 missing Sys resources, G-02 stale retained achievement settings), and two Low (G-01 normal ES scan shutdown, G-03 runtime Python isolation). The first three have later landed corrections and independently checked bounded runtime evidence; the three external-derived corrections remain open pending their exact acceptance proof. Source-reviewed proposals are not installed success.

Both pinned Anthropic Fable5.1/xhigh calls completed through the Facilitator with matching prompts/output digests, provider-response model identity and original successful channels. Every blind/refutation lead was checked against source/originals. The external reviewer received no pixels and only attested summaries for later image receipts; primary visual/original readback remains separately identified. Native gameplay export is not yet independently consumed. Primary exact model identity remains unverified; OpenAI lab and Codex harness are known.


Current score:80PASS /16PARTIAL /16SKIP /3FAIL /0UNTESTABLE, total115. Frozen fac608/ES3178 source; later fixes are supplemental.

## Task checklist

- [x] PL-001 — Initialize and shut down achievements in DolphinNoGUI (High); Resolved in `9aaaaa0f642b97ebf722c2e1aeedb7e4d00bcbdc`, present in d4af and next by direct branch/read checks. `dolphin-installed-supplement-readback.md` verifies original installed evidence. G-02 is a separate retained-settings defect, not a reason to erase this lifecycle correction.
- [x] PL-002 — Bound Proton release metadata requests (Medium); Resolved in `9aaaaa0f642b97ebf722c2e1aeedb7e4d00bcbdc`; exact metadata control/readback in `steam-supplement-readback.json` and durable Steam remaining result. Undeclared-length size enforcement is not claimed; total time remains bounded. No installed ARM Steam claim.
- [x] PL-003 — Supply Dolphin resources at its compiled immutable Sys path (Medium); Resolved in `6616cc36cb85d86878870feafdcb64edbc192df8` under #592, present in d4af/next; engineering-image and dolphin-installed supplemental readbacks directly verify originals. No claim every Sys consumer was separately exercised.
- [ ] PL-004 — Clear retained Dolphin achievements when disabled or signed out (Medium); Open — #594 source preparation exists, but no integrated correction or executed acceptance has been verified by this audit.
- [ ] PL-005 — Cancel and join the Wi-Fi scan worker at normal ES exit (Low); Open — #593; source-only proposal `16dbac5211eea7e70db7394372033be2be7df829`, not integrated or executed. Normal-exit scope is deliberate; no universal signal-custody claim.
- [ ] PL-006 — Isolate the Steam runtime Python invocation (Low); Open — parent preparing the one-line correction and its scoped tracking/control; no executed proof or landed fix verified yet.

# M7 next candidate audit punch list

Scope: independent Milestone audit #590; frozen distribution fac608ff89940ce358ea9b8a95e9a08a6fe26568 and ES3178b832b8d134198b2b4eede4f725d4ed283f8c. Two verified Fable5.1/xhigh passes plus the primary OpenAI perspective, all leads independently graded. This is not a council or RC approval.

Six audit-discovered findings: 0 Critical, 1 High, 3 Medium, 2 Low. Three have later landed, narrowly verified corrections; three remain open. Frozen/current-audit score: 80 PASS, 16 PARTIAL, 16 SKIP, 3 FAIL, 0 UNTESTABLE of115. Original pre-external score remains in pre-external-scorecard.json. Later source fixes do not rewrite frozen behavior.

Execute open items within root-owned serialized integration/runtime. No broad accepted matrix must be repeated merely to improve audit prose. Each acceptance states the bounded proof needed; preserve original failed observations and explicitly distinguish source proposal, private candidate and installed artifact.

Audit issue: #590 is the scope/intake link. Mandatory Phase6 punch tracker creation/update is root-owned and pending; its final URL will be recorded here after original tracker readback. Source follow-ups #592/#593/#594 do not by themselves substitute for the punch checklist.

## PL-001: Initialize and shut down achievements in DolphinNoGUI

- **Severity:** High
- **Category:** Interaction Defect
- **Source Finding:** F-002
- **Owner area:** Dolphin package / default frontend
- **What:** Supply the lifecycle missing from the default frontend while preserving disabled and failed-boot cleanup.
- **Where:** projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch
- **Why:** Correct INI and a compile flag cannot enable a client that was never constructed; AC102 fails on frozen fac608.
- **Evidence:** Original installed baseline logs the null-client error with enabled=true, initialized=0 and no requests. Complete frozen source shows Qt-only lifecycle. Later installed d4af ELF5cb5dac has original enabled/disabled/failed-boot exits0/0/1 and lifecycle1/1,0/0,1/1.
- **Acceptance:** Land the guarded lifecycle patch, compile the actual target, and retain original actual-installed enabled/disabled/failed-boot lifecycle and loopback request/cleanup evidence. No real login, award or gameplay inference.

## PL-002: Bound Proton release metadata requests

- **Severity:** Medium
- **Category:** Code Quality
- **Source Finding:** F-001
- **Owner area:** Steam installer
- **What:** Put -q first and retain finite connect/total/response-size limits on the two top-level release metadata requests.
- **Where:** projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:213
- **Why:** Exited Python child alarms do not cover this shell curl; a stalled server can keep foreground installation waiting. AC083 fails on frozen source.
- **Evidence:** Full caller/source trace plus original installed-curl candidate controls: normal0/0, declared-size oversize63, stall28 at30.006s and function failure after its existing10s message delay; no forced cleanup or unexpected requests.
- **Acceptance:** Land the bounded exact function and preserve installed curl/Bash normal, declared-size oversize and stalled-response originals, exact argv, family-state equality and child cleanup.

## PL-003: Supply Dolphin resources at its compiled immutable Sys path

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** F-003
- **Owner area:** Dolphin package installation
- **What:** Install the immutable relative Sys alias without moving resources into retained storage.
- **Where:** projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk
- **Why:** Compiled /usr/share/dolphin-emu/sys is absent while resources live in /usr/config/dolphin-emu; badges, approved lists and global configuration consumers share the root.
- **Evidence:** Frozen staged path missing and original private candidate badge loads fail. Later d4af image six resource paths match pinned source hashes and resolve inside read-only squashfs; all12 historical badge-error counts are0 across three actual installed startup cases.
- **Acceptance:** Land the package alias, pass package checks/build, and retain exact installed link/resource identities plus absence of the four previous badge failures across enabled, disabled and boot-error startup controls.

## PL-004: Clear retained Dolphin achievements when disabled or signed out

- **Severity:** Medium
- **Category:** Interaction Defect
- **Source Finding:** G-02 (external R-01)
- **Owner area:** Dolphin helper and both native launchers
- **What:** Atomically publish an explicitly inactive credential-free INI for both negative states, and refuse native launch if publication fails.
- **Where:** projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/cheevos_dolphin.sh:21
- **Why:** Early1 leaves prior Enabled=True/token/hardcore/host intact; launchers continue. Already affects Qt and becomes active on default NoGUI after the lifecycle repair. AC100 FAIL, AC101 PARTIAL.
- **Evidence:** Complete source/package search confirms sole writer and unchecked caller exits; pinned manager reads retained settings. No authentication success is assumed. Root #594 proposal reviewed at source level only.
- **Acceptance:** Two seeded-enabled-state transitions produce disabled/blank outputs with expected original1 and unchanged source settings. Failed publication preserves prior bytes and prevents both engines from launching with original error status; unchanged enabled routing and narrow EN/FR refusal flow/frame proof retained.

## PL-005: Cancel and join the Wi-Fi scan worker at normal ES exit

- **Severity:** Low
- **Category:** Code Quality
- **Source Finding:** G-01 (external F-12b)
- **Owner area:** ES Wi-Fi worker lifecycle
- **What:** Retain application lifetime ownership and cooperative cancellation, then join before frontend/log teardown while preserving picker Back/reopen behavior.
- **Where:** es-app/src/guis/GuiWifi.cpp:470; es-app/src/guis/WifiScanProcess.h; es-app/src/main.cpp
- **Why:** Detached worker owns the deadline and group cleanup; normal whole-ES exit can remove it with a blocked child outstanding. Historical picker-close proof did not cover process exit.
- **Evidence:** Frozen source confirms no join/hook; inherited emustation.service uses KillMode=process. Proposed ES16dbac52 and focused four-control observer/driver sources reviewed, all execution unrun.
- **Acceptance:** Land exact ES source with required syntax check. Preserve an original known-bad normal-exit negative, candidate cancellation/atexit/completed-refresh results and actual frontend Back/reopen/SIGINT exit proof with exact child identities, no candidate forced cleanup and unchanged presentation. Document signal/fatal residual under D-CLOUD-133.

## PL-006: Isolate the Steam runtime Python invocation

- **Severity:** Low
- **Category:** Code Quality
- **Source Finding:** G-03 (external R-03)
- **Owner area:** Steam runtime helper invocation
- **What:** Use /usr/bin/python3 -I -S -B - for the self-contained runtime helper, matching all four sibling helpers.
- **Where:** projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:780
- **Why:** Unisolated stdin Python admits cwd/module-path/site influence and PATH interpreter substitution after profile loading; no site dependency appears in the complete stdlib-only helper.
- **Evidence:** Exact invocation/source comparison; shipped-profile searches do not eliminate ordinary Python import context. No hostile file or target runtime failure is claimed.
- **Acceptance:** Land the one-line invocation with unchanged embedded body, preserve a bounded import-shadow old-negative/candidate-positive control and one narrow successful runtime-helper control using the installed interpreter. Keep broader native ARM qualification separate.

## Pre-existing tracked scope (not punch items; exempt from Phase7 discovery gate)

- #563 — source/licence custody for adopted artifacts and final composition acceptance; no blanket upstream hardware recertification.
- #564/#579/#580/#582 — actual payload/installed ARM Steam/FEX/Proton/native/self-update boundaries, separate from passing synthetic full callers and exact installed-curl function proof.
- #574/#575/#583/#584 — combined selected native engine, effective setting, gameplay/game-save/manual-state/automatic-state behavior and exact installed composition. Parent reports native03 completion, but its export is not yet consumed independently here.
- #577 and public setup documentation tracking — current source/flow/frame binding plus separate public-doc publication; physical radio behavior excluded from controlled backend proof.
- #349/#344/#511 and release/device issues — prior explicitly excluded restore/docs/device/publication work remains on its original tracker, not newly numbered by this audit.
- #590 — final artifact/tracker/resolution closure. Audit completion cannot be inferred from this pre-issue list.

## Leads resolved by review or retained as boundaries

All blind/refutation rows are preserved in04 and second-opinions readbacks. RVZ short-group speculation, normal persisted spaced Recent, missing OAuth cancel and the sanitizer-created unused-variable claim are refuted by source. Busy scans, conservative retained-card refusal, invalid stored country, manual recovery guidance, scan-input asymmetry, generated POT hygiene and repeated failed-RVZ cost are narrowed to their documented behaviors or coverage. F-10 profile reassignment is an explicit recorded restriction with environment overrides retained. R-02 slow-storage total-budget exhaustion is plausible but unverified as a defect; the finite global bound remains intentional. No silent dropped lead or extra runtime requirement is created.

## Machine-readable index

```yaml
punch_index:

- id: PL-001
  severity: "High"
  category: "Interaction Defect"
  source_finding: "F-002"
  owner_area: "Dolphin package / default frontend"
  where: "projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/patches/018-nogui-achievements-lifecycle.patch"
  acceptance: "Land the guarded lifecycle patch, compile the actual target, and retain original actual-installed enabled/disabled/failed-boot lifecycle and loopback request/cleanup evidence. No real login, award or gameplay inference."
  outcome: "resolved"

- id: PL-002
  severity: "Medium"
  category: "Code Quality"
  source_finding: "F-001"
  owner_area: "Steam installer"
  where: "projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:213"
  acceptance: "Land the bounded exact function and preserve installed curl/Bash normal, declared-size oversize and stalled-response originals, exact argv, family-state equality and child cleanup."
  outcome: "resolved"

- id: PL-003
  severity: "Medium"
  category: "Interaction Defect"
  source_finding: "F-003"
  owner_area: "Dolphin package installation"
  where: "projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/package.mk"
  acceptance: "Land the package alias, pass package checks/build, and retain exact installed link/resource identities plus absence of the four previous badge failures across enabled, disabled and boot-error startup controls."
  outcome: "resolved"

- id: PL-004
  severity: "Medium"
  category: "Interaction Defect"
  source_finding: "G-02 (external R-01)"
  owner_area: "Dolphin helper and both native launchers"
  where: "projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/scripts/cheevos_dolphin.sh:21"
  acceptance: "Two seeded-enabled-state transitions produce disabled/blank outputs with expected original1 and unchanged source settings. Failed publication preserves prior bytes and prevents both engines from launching with original error status; unchanged enabled routing and narrow EN/FR refusal flow/frame proof retained."
  outcome: "open"

- id: PL-005
  severity: "Low"
  category: "Code Quality"
  source_finding: "G-01 (external F-12b)"
  owner_area: "ES Wi-Fi worker lifecycle"
  where: "es-app/src/guis/GuiWifi.cpp:470; es-app/src/guis/WifiScanProcess.h; es-app/src/main.cpp"
  acceptance: "Land exact ES source with required syntax check. Preserve an original known-bad normal-exit negative, candidate cancellation/atexit/completed-refresh results and actual frontend Back/reopen/SIGINT exit proof with exact child identities, no candidate forced cleanup and unchanged presentation. Document signal/fatal residual under D-CLOUD-133."
  outcome: "open"

- id: PL-006
  severity: "Low"
  category: "Code Quality"
  source_finding: "G-03 (external R-03)"
  owner_area: "Steam runtime helper invocation"
  where: "projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh:780"
  acceptance: "Land the one-line invocation with unchanged embedded body, preserve a bounded import-shadow old-negative/candidate-positive control and one narrow successful runtime-helper control using the installed interpreter. Keep broader native ARM qualification separate."
  outcome: "open"

```

## Phase 7 resolution gate

This table records verified outcomes available at creation; three open items prevent resolution completion. Final formal gate follows the root-owned Phase6 tracker and fresh outcome readback. A source-only proposal is not Resolved.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-001 | Resolved | Resolved in `9aaaaa0f642b97ebf722c2e1aeedb7e4d00bcbdc`, present in d4af and next by direct branch/read checks. `dolphin-installed-supplement-readback.md` verifies original installed evidence. G-02 is a separate retained-settings defect, not a reason to erase this lifecycle correction. |
| PL-002 | Resolved | Resolved in `9aaaaa0f642b97ebf722c2e1aeedb7e4d00bcbdc`; exact metadata control/readback in `steam-supplement-readback.json` and durable Steam remaining result. Undeclared-length size enforcement is not claimed; total time remains bounded. No installed ARM Steam claim. |
| PL-003 | Resolved | Resolved in `6616cc36cb85d86878870feafdcb64edbc192df8` under #592, present in d4af/next; engineering-image and dolphin-installed supplemental readbacks directly verify originals. No claim every Sys consumer was separately exercised. |
| PL-004 | Open | Open — #594 source preparation exists, but no integrated correction or executed acceptance has been verified by this audit. |
| PL-005 | Open | Open — #593; source-only proposal `16dbac5211eea7e70db7394372033be2be7df829`, not integrated or executed. Normal-exit scope is deliberate; no universal signal-custody claim. |
| PL-006 | Open | Open — parent preparing the one-line correction and its scoped tracking/control; no executed proof or landed fix verified yet. |
