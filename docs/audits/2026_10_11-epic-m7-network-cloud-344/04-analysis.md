# Audit Analysis — M7 network/cloud feedback #344

Date:2026-10-11. Issues:#535–539. Scope:Epic issue chain under #344.
Source:uncommitted frozen snapshots, inputs/source-manifest.json.

## Executive summary

The UI and transactional connection changes have substantial target proof,
including rejected-original controls. The change is not ready to integrate:
seven repair items remain after independent verification (3 High,1 Medium,3 Low). Nothing here
certifies a new installed firmware image or a release candidate.

## Acceptance-criteria scorecard (frozen primary pass)

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

### Independent-review changes to the frozen scorecard

AC-537-03 is now FAIL: G-01 rejects real OAuth configuration after token collection.
AC-537-04 is PARTIAL: F-02 proves a lock-contract violation, not invalid credential
publication; its trigger/harm are narrowed above. Other frozen verdicts remain
unchanged pending repair/integration. Revised counts remain12 PASS/7 PARTIAL/1 FAIL.
The final UI index is delivered; the older packet deliberately retains its original
boundary. Installed-image qualification is still pre-existing tracked scope.

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
| F-02 | Medium | seed writer can interleave with connection update/remove | use shared lock before target resolution until final folder writes/readback |
| F-03 | High | destructive apply uses different account from preview | bind preview to full context, recheck under lock, reject old unbound plans; cover adjacent copy preflight |

## Finding Verification (Phase 4.5)

| Finding | Severity | Survived refutation? | What was checked |
| --- | --- | --- | --- |
| F-01 | High | yes | Full cloud_scan context/result/completion path re-read; actual VM scan rc0 and stamp valid both before/after switch. Separate setup validation hash is not consumed by scan. |
| F-02 | Medium | yes | Full seed branch and direct GuiCloudTransfer invocation re-read; no outer lock. Actual blocked mkdir permits cloud_remote select rc0 while seed process alive. |
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

The authorized call completed at 14:53:22 UTC on attempt1, rc0. Facilitator1.14.0
verified anthropic/claude-fable-5.1 at xhigh, observed provider Anthropic via OpenRouter.
The output SHA256 is b2391801ba09d94bc18d6c7a9b859617ad0a412580bb945032b313d4cb8b0edb.
Receipt: second-opinions/claude-audit.md.provenance.json. Review-plan identity, effort
and output-digest checks passed; checks/second-opinion-verification/verified-review.json.
Command: primary tools/council/run invoke --member claude --provider openrouter
--prompt-file second-opinions/claude-brief.md --output second-opinions/claude-audit.md
(full paths in /tmp/pix537-fable-review25/command.json). Two model perspectives,
one external reviewer, one Epic refutation call. Source remains frozen while leads
are verified. Primary Codex/OpenAI exact model remains unknown.

### Verified additional lead G-01 (Fable O-1) — High

Actual packaged guest rclone (SHA256361c27d953f822969afc25a73e0cc2122fd8e161545f9c0e5f63c5baad92724c)
config create probe dropbox token=<synthetic-token> --non-interactive --obscure
returns rc0 and State=*oauth-confirm,,, / Option.Name=config_refresh_token.
cloud_connections.py159–166 refuses that result; cloud_oauth544 supplies only token.
The same credential-free command with config_refresh_token=false returns empty State.
No external account contacted, and temporary config removed. Raw sanitized result:
checks/second-opinion-verification/oauth-config-probe.json. Confirmed High; repair
the OAuth-token handoff without broadly accepting unanswered provider questions.
### Lead grading (primary verification, not reviewer consensus)

| Fable item | Grade | Primary evidence / disposition |
| --- | --- | --- |
| O-1 | confirmed, High → G-01 | Real packaged rclone noninteractive Dropbox config probe above; original pending State, specific pre-answer completes. |
| O-2 | disagree as an independent defect; folded into F-01 acceptance | GuiMenu.cpp4181–4189 checks every nonempty cached run with cloud_scan --stamp-valid. Once F-01 includes selection, an old ID cannot bypass the script check. Test this consumer path; clearing IDs is optional defense, not a separate required fix. |
| O-3 | confirmed, Low → G-02 | GuiMenu.cpp6825 says alphabetical-first even after explicit selection. Correct SSH setup guidance and stale instruction-file single-remote wording. |
| O-4 | confirmed, Low → G-02 | lead30-result.json records actual module refusal with unchanged config when selection names a missing connection; GuiMenu.cpp7125–7140 drops the supplied recovery instruction. Preserve safe refusal, show how to choose a remaining connection. |
| O-5 | confirmed, Low; folded into F-03 | cloud_content_restore857 returns silently before plan spending. The context-bound repair must spend/refuse stale plans and give the same actionable reason as other content paths. |
| O-6 | confirmed, Low → G-02 | cloud_scan139–143, content backup197–202/restore234–238, saves backup2419–2425/restore2219–2225 say not set up after empty selection; manager8002–8003 correctly says choose a connection. Align refusal with stored-but-unselected state. |
| O-7 | confirmed, Low → G-03 | Actual guest lead30: unquoted check returns2/FAIL two; identical named alias quoted returns0/OK two words:. GuiMenu.cpp6621 concatenates unquoted name. |
| O-8 | disagree with successful-sign-in stranding; provider-specific cancellation UX unverified | cloud_oauth1963–1990 writes signed-in marker independently of popup.close; cloud-signin-window.c465–482 switches the current view to Finishing up on that marker. Escape/phone Close remains an explicit exit. A provider-specific incomplete popup may still warrant future evidence, not a demonstrated regression here. |
| O-9 | could not verify performance defect | topWindow5586–5594 does synchronous list; five actual VM calls took0.0298–0.0340s with rc0. No stated threshold failed. Encrypted-config/physical-device latency remains a coverage boundary, not a measured pass or proven defect. |
| O-10 | agree, narrowed: accepted behavior, no new defect | Canonical flow562 explicitly says CLEAR commits empty; #538 requires preserving existing callbacks. GuiWifi asks only without a same-SSID profile; clearing never overwrites a stored credential. No change to that accepted contract. |
| O-11 | confirmed, Low → G-04 | Actual guest, two bounded24s stages: real holder.end returns at45.0s with collector alive and one staged config; subprocess then exits. Live config unchanged. Join must cover/cancel the entire staged transaction and clean temporary bytes on normal shutdown. |
| F-01 | confirmed, High | Original actual guest stamp remained valid after alpha→beta; consumer checks script result. |
| F-02 | agree, re-graded Medium | Seed retains resolved remote name; selection alone does not redirect it. No deletion and foreground modal blocks ordinary same-UI concurrency. Existing actual CLI writer probe proves exclusion gap; same-name replacement/removal remains forbidden by intended lock contract. |
| F-03 | agree, narrowed, High | Original actual guest preview alpha/apply beta deleted local.rom, retained save sentinel. Trigger is CLI/out-of-band change during modal or between CLI calls, not ordinary same-UI selection while confirmation is open. |

Net effect: four new finding IDs G-01–04 (G-02 consolidates three related copy gaps),
O-2/O-5 folded into primary repairs, F-02 re-graded Medium, F-03 trigger narrowed.
Seven punch items:3 High,1 Medium,3 Low. No Critical item. All reviewer items retained.

Coverage follow-through: saves backup2507–2508 and restore2321–2322 call
`take_cloud_lock` before `main 9>&-`, where selection resolves. This settles the
packet-only visibility question; no new race there. Prior pkgcheck log has only
its printed package path; its existing exit receipt, not that text, establishes
success. Final UI index/95entries were delivered after the packet was frozen;
that does not retroactively change its evidence or prove an installed image.
Provider-specific popup cancellation, encrypted/physical menu latency and genuine
provider authorization remain untested. Synthetic target proof does not claim them.

## Instruction File Recommendations

No new doctrine: existing shared-state rules apply. Add target regression
controls for selection, seed exclusion and preview account binding.

## Quality self-check

| Item | Status |
| --- | --- |
| Scorecard IDs match02 | yes; computed counts |
| Conformance and sibling tables | present in03 |
| Coverage boundary | present02/04 |
| Critical/High verification | all3 primary defects reproduced on actual guest |
| Second opinion | verified; every lead graded |
| Instruction recommendations | present; no unnecessary new rule |
| Tier B review | editor/browser accepted; full-index delivery still open |
| Evidence/reproducible/actionable | fixtures/hashes/results retained; no release claim |

Audit remediation tracker: [M7.P5 #540](https://github.com/pixelelated/distribution/issues/540), child of #344.

## Repair qualification addendum — 2026-10-11

The original frozen-source scorecard above remains unchanged. All seven confirmed
findings now have implemented repairs and passing actual-target controls; Phase 7
records landed commits separately. Evidence root: `checks/remediation/`.

| Item | Repair evidence and acceptance result |
| --- | --- |
| PL-001 | `guest53/transactions.log`: real-rclone OAuth create/update uses the completed token without refresh; unknown State, obsolete/cancelled attempts and replacement preservation pass. All26 transaction cases pass. |
| PL-002 | `pix540-scan34/result.json`: completed and in-flight scans invalidate after account change; absent/empty/selected identities differ; unchanged control succeeds. |
| PL-003 | `pix540-content35/result.json`: nine target controls reject changed accounts, same-name settings/folders, old/unbound plans and mid-preview changes; local/cloud sentinels remain; unchanged apply succeeds. Regression52 preserves save exclusions and delete caps. |
| PL-004 | `pix540-seed37/result.json`: six real-guest controls prove seed/select/replace/remove exclusion, busy75 before writes, ordinary creation and no child-retained descriptor. |
| PL-005 | `guest53/refusals.json`:15 whole-script state refusals preserve settings/payload. Final54/matrix55 has16 reviewed EN/FR640/1280 frames, canonical flows and source-bound schema1 entries. |
| PL-006 | Matrix55 NC13 runs CHECK CONNECTION against actual alias `two words`; all four locale/size cohorts succeed. Source uses the established shellQuote helper for the complete argument. |
| PL-007 | `pix540-final-guest39/result.json`: collector and HTTP worker shutdown each complete at~24s, no remaining stage/worker, live settings unchanged. Success/obsolete/cancelled transaction controls remain green. |

Regression52 completes with1,373 PASS lines,0FAIL,0SKIP,1 explicitly retired
historical group. Protocol49 completes108 WebDAV+108 SFTP controls and restores
absent/empty/named prior selection. Final54 syntax/compile/link/catalog checks
and matrix55 review cover the later SSH-only sizing/position change; unchanged
cloud-suite inputs retain their existing completed proof.

Original failed fixtures and rejected UI47/51 frames remain source-bound. Small
panels still elide inherited long terminal-instruction suffixes; the repaired
selection direction and both final-page buttons are readable. This review does
not claim to redesign every terminal instruction or prove live provider policy.
No owner cloud/device operations occurred. #535–539 combined-image installation,
clean/retained qualification and #528 remain pre-existing delivery scope.

## Phase 7 landed resolution

All seven findings are resolved in distribution `bc2dceb406969a401d987de168acfb3ae60b7e01`
and ES `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`. Branch-containment and last-path-commit
commands were run again; `checks/resolution59/landed-readback.json` is the receipt.
The punch-list table and machine-readable outcomes agree. The original frozen
scorecard remains historical; #537's combined-image clean/retained criterion is
still open, alongside #528 source/component dispositions and publication gates.
