# Refutation pass — Milestone delta #507 (frozen ac64c806 / e6645cb5 / ES 4e410dc9)

Second sequential call, same reviewer. Packet-only source reading; no tools or executions were run by me. IDs: **my F-1…F-12** are the blind-pass findings (appended verbatim above, unchanged); **primary F-01/F-02/F-03, L-01, L-02** are the primary's. Every statement below is a lead for primary verification, not a verdict.

---

## 1. My findings (unchanged blind list, condensed)

| ID | Severity (blind) | Kind | One-line claim | Packet anchors |
|---|---|---|---|---|
| F-1 | Medium | confirmed (tool) | Two delta-added regression tools cannot pass against the delta's own `cloud_setup` (bare `--seed-folders`; sibling-pointer expectation in `explicit()`/vm-test); negative cases would pass vacuously | tools diff `pixelelated-cloud-folder-test`, `…-vm-test`; `cloud_setup:786, 755`; `checks/retrospective-controls01/{results.json,folder-regression-tool.log}` |
| F-2 | Medium | source lead → target proof | `config_id`/`context_id` hash the live `rclone.conf`; OAuth token refresh rewrites that file → first check/scan after expiry fails with "SETTINGS CHANGED"/"CHECK YOUR CONNECTION" | `cloud_setup:548–566`; `cloud_scan:171–189, 216–227, 231–244`; `cloud_folder_validate:79–86, 267–269`; ES `GuiMenu.cpp:6895–6899, 6927–6932, 6960–6967`; deleted `cloud_migrate_layout remote_fingerprint()` comment |
| F-3 | Medium | confirmed source regression | New `cloudSetupOpenPathEditor` discards the script's refusal sentence(s) (bucket/“Try X” guidance) that G-C-03 made player-facing | es-diff `cloudSetupOpenPathEditor`; `cloud_setup:473–474, 530–543, 756–757` |
| F-4 | Low | design inconsistency | `cloud_setup absent_not_broken` still walks to the account root; validator/restore are root-bounded | `cloud_setup:285–299, 346, 353–371, 522, 599, 860`; harness `LL_SCOPED` branch |
| F-5 | Low | lead → frames | `--seed-folders` emits no `>>> unit/doing`; ES declares N items | `GuiMenu.cpp:6989–6990`; `cloud_setup:785–868`; `CloudTransferJob.cpp:31` |
| F-6 | Low | wording | Invalid page context → "NO LONGER CURRENT"; parse/`configuration-changed` → "CHECK YOUR CONNECTION"; `folder_marker_write` returns 5 with no `>>> why` | `GuiMenu.cpp:6960–6967, 6895–6899`; `cloud_setup:417–424, 319–324` |
| F-7 | Low | dead branch | `!exists(cloud_scan)` fallback can only produce "no longer current" | es-diff `cloudOpenTransfer`, `cloudOpenTransferOptions` |
| F-8 | Low | host control | `completed_audit_marker` raises `AttributeError` (uncaught) on non-object receipt shapes instead of reporting | tools diff `ceremony-check` |
| F-9 | Low | hygiene | `.pot` drift; orphan FR msgids; deleted "PRESS ANY BUTTON TO CONTINUE" translation | es-diff `locale/*` |
| F-10 | Low | existing scope (#519) | `/ROCKNIX/Saves` retained in `superseded_saves_setting`; `layout=2` marker written by CREATE interacts with un-upgraded owner devices | product diff `cloud_backup`; `cloud_setup:808, 417–424` |
| F-11 | Low | lead → timing | `timeout 5` shell-outs on the UI thread (page build, `stillSelected`, `--stamp-valid`) | `GuiMenu.cpp:6941, 6962`; es-diff `cloudScanStamped` |
| F-12 | — | stale tracker | #497 criteria 3/4 unchecked + "actively compiling"; #510 "local/unintegrated… pin unchanged… guest active… no audit started" | frozen #497/#510 bodies; product diff `emulationstation/package.mk`; `docs/qa-logs/2026-10-08-save-repair-cases/README.md:3–5, 70–74` |

No item is added to or removed from this list in the refutation pass. Observations made only now are marked "(refutation-pass note)".

---

## 2. Refutation of primary Medium-or-higher items

### Primary F-01 — Reconcile tracker bodies (#510, #497) — Medium, Spec Drift

**Claim as stated:** #510 and #497 current-state prose/criteria contradict integrated/closed state; AC-510-06 FAIL, AC-515-02 PARTIAL, AC-497-04 PARTIAL.

**In-packet evidence for:**
- `inputs/distribution-product-diff.patch` → `projects/ROCKNIX/packages/ui/emulationstation/package.mk`: `PKG_VERSION` 72494bc7… → 4e410dc9…. The frozen #510 body ("Current qualification") says "the product pin is unchanged" and "Both product branches remain local/unintegrated." The pin is changed in the frozen tree; that sentence is false at freeze.
- `docs/qa-logs/2026-10-08-save-repair-cases/README.md:3–5`: "integrated through #508 in e6645cb5ea… #515 and source fixes #520/#521/#522/#523 are closed; #507's independent audit is next"; `:70–71` "The guest/compiler were retired." The #510 body says "#515 … (active, including children #520/#521)" and "a new owned #520/#521 source-overlay guest is active."
- Frozen #497: criteria 3 and 4 `[ ]`; "Current state — 2026-10-07 07:02 UTC … actively compiling … Actual handoff is still pending." The packet's AC-500-02/03 criterion text (from `inputs/issues/500.json`) names the accepted update `a419dc33…` and installed `BUILD_ID 43d0bc3b…`, i.e. the firmware #497 calls "actively compiling". The #497 body also already contains "H700 arm acceptance — 04:50" (938 ARM ELF objects accepted) yet criterion 3 stays unchecked.

**Refutation attempts:**
1. *"Dated sections are historical, not current directions."* #497's drift section is dated but titled "Current state"; #510's "Current qualification" and the "Ordered implementation path" items 2–4 carry no date and are written in present tense. The primary's characterization ("current assertions, not labeled historical sections") matches the frozen text. Not refuted.
2. *"The snapshot is stale, not the tracker."* Possible: if the live body was edited after `inputs/issues/*.json` were frozen, the defect is a snapshot artifact. The packet cannot distinguish this (no live readback). Either way the required change—reconcile and re-read the exact body—is identical; only the "who" differs.
3. *"AC-510-06 should be PARTIAL, not FAIL."* The criterion has a historical half (published in next b115af8d with receipts) and a present-tense half ("agree on this implementation order and remaining gates"). The present-tense half does not hold for the frozen body against #508/#515 state. FAIL vs PARTIAL is a vocabulary choice under the primary's defined verdict set (not in packet); it produces the same punch item. Not material.
4. *Severity inflation?* No product/code impact; the harm is an agent restarting retired work (a guest, re-integration) or mis-reading readiness. Medium is defensible; Low would understate the "assumed-done/list drift" risk the primary's own blindspots 27/51 name. **Survives at Medium.**

**Falsifiers:** an exact-head readback of #510/#497 at freeze time showing the contradicted sentences already replaced or labeled historical; or evidence that `inputs/issues/510.json` was captured before e6645cb5 integration *and* the live body was corrected before dispatch.

**Cannot be judged:** live tracker state; #515/#508 bodies (not in packet); the b115af8d publication receipts.

### Primary F-03 — Retire or adapt regression tools calling the removed implicit-seeding contract — Medium, Test Gap

**Claim as stated:** `pixelelated-cloud-folder-test` (no-category calls) and `pixelelated-cloud-folder-vm-test` (lines 131/138/146/150/153; overlay list predates the validator) fail or vacuously pass against frozen source; fresh one-case run rc1/inner rc2; remediation = adapt or mark historical and repoint the canonical entry.

**In-packet evidence for:**
- `cloud_setup:785–786`: bare `--seed-folders` → `Choose which cloud folders to create.` exit 2 (no `>>> why`).
- `checks/retrospective-controls01/results.json` rc 1; `folder-regression-tool.log`: `FAIL fresh-empty-seed-beside-legacy cloud_setup ('--seed-folders',): rc=2`.
- Tools diff: `seed()`, `fresh_beside_legacy()`, `carried_root()`, `interrupted_state()`, `write_refused()`, `guard()` all invoke `--seed-folders` bare; vm-test `script('cloud_setup','--seed-folders')` with default `ok=True`.
- Sibling tools in the same diff *were* adapted (`cloud-round-trip` → `--seed-folders saves,settings,roms,bios,media` and independent pointers; `last-good-scripts-test` gates on `SEED_ARGS`/`VALIDATOR_AVAILABLE`), which shows the contract change was known when these two were left behind.

**Convergence with my F-1 and two extensions the primary should fold in (same tools, same remediation):**
- `explicit()` requires `--set-saves-remote /Selected/Saves` to produce `('/Selected/Saves','/Selected/Backups','/Selected/Content')`; vm-test asserts `SETTINGS_REMOTE="/Selected/Backups"`. Frozen `cloud_setup:733–765` writes `SAVES_REMOTE` only. Adapting the seed arguments alone will still leave these cases failing.
- vm-test `script('cloud_setup','--content-location')` (default `ok=True`) on a candidate16 guest whose overlay installs only `cloud_setup/cloud_scan/cloud_backup`: `cloud_setup:650–653` exec's `cloud_folder_validate`, absent on that image → `STATE=unreadable` exit 1 → assertion failure. This is the concrete consequence of the "overlay list predates the validator" point.
- `guard()` expects `'>>> why '` from the bare seed call; the frozen refusal prints no `>>> why`. So even a "guard" case fails for the wrong reason, matching the primary's vacuous-pass concern.

**Refutation attempts:**
1. *"The tools are historical-only."* Both headers claim currency ("fast regression control", "(#508)… --ref supplies old production bytes"), and neither has a historical opt-in gate like `cloud-pair-migration`/`rasteratops-vm-cloud-epic` received in this same delta. Not refuted. (Refutation-pass note: both tools appear in `.githooks/pre-push` `PERSONAL_PATTERNS`; the semantics of that list are not in the packet and do not change the finding.)
2. *"Replacement controls cover the contract, so this is Low."* Current coverage is real (`checks/cloud-controls01`: validator 30, save-layout 39, content-scope 21, all rc 0) and the primary says so. The residual harm is a documented entrypoint that produces false failures or vacuous refusals, plus a VM cycle wasted if launched. Medium for a *test-oracle* finding is proportionate; it is explicitly not a product failure. **Survives at Medium.**
3. *"It is a product regression."* No: explicit categories are the intended D-CLOUD-178/179 contract (`CloudOffer.cpp:37` passes `saves`; `GuiMenu.cpp:6989` passes the csv). Classification as Test Gap is correct.

**Falsifiers:** a `result.json` from either tool with all cases PASS and `source_sha256` of `cloud_setup` matching e6645cb5's; or a canonical instruction entry already marking both tools historical-only with the replacement named.

**Cannot be judged:** `instruction-files.md:196`; the "four terminal channels 1" and owner-exit receipts (only rc 1 is in the packet); whether the tools ever produced accepted receipts under an intermediate contract.

### Primary F-02 — withdrawn

Agreed and not resurrected. The frozen #504 excerpt itself says "these paths currently identify retained local evidence, not an already-published commit," and criterion 4 reads "retained under `<path>`", not "published." AC-504-04 UNTESTABLE within the audit boundary is consistent with the excerpt and with exclusion of private custody. One provenance note only (not a finding): the excerpt lists four criteria while the primary cites `inputs/issues/504.json:body-line32` for AC-504-05; the excerpt states operational observations were omitted, so line 32 may sit in the omitted span. Confirm in `inputs/criteria.json`; nothing in that confirmation touches publication.

### Primary L-01 — post-confirmation UI→backend configuration race (lead, not graded)

Traced in packet: `GuiMenu.cpp:6960–6967` (`stillSelected`), re-check at `6988`, then `GuiCloudTransfer` starts `cloud_setup --seed-folders <csv>` (`6989–6990`), `CloudTransferJob::start` detaches the worker (`CloudTransferJob.cpp:54–67`), backend reads its own paths at `cloud_setup:789` with no expected-context argument. The window exists; an external writer is required; the consequence is folders/notes at a path the player did not see, not data loss. **Low/lead is correct, not under-graded.** The cheap closure is to pass the started `config_id` to `--seed-folders` and refuse on mismatch, mirroring `cloud_folder_validate:267–269`. Note the shared mechanism also underlies my F-2: if the config digest is sensitive to token refresh (F-2), such a binding would surface F-2 on CREATE as well, so the two should be decided together.

### Primary L-02 — `rclone/package.mk:84` "no lock" comment (Low)

`package.mk:84` is not in the packet; `cloud_scan:355–359` does hold a parent flock and the script header no longer claims lock-free operation. Grade cannot be verified from the packet; Low explanatory lead is not misgraded on the evidence available.

---

## 3. Primary verdicts that my blind items put in question (leads, not re-grades)

| Primary verdict | My item | Why it may be over-graded | What would settle it |
|---|---|---|---|
| AC-508-06 PASS; AC-513-02 PASS; AC-514-02 PASS ("adjacent setup guidance accurate") | F-3 | The frozen editor shows one generic sentence for every refusal; the script still prints bucket/“Try X” guidance (`cloud_setup:473–474, 530–543`) and comments at `:756–757` still promise it reaches the screen. Nuance: the earlier A3 bug (page continues on refusal) is **not** reintroduced—rc is checked; only the reason is lost. A possible deliberate trade is that the old reasons were un-localized English and the new message is localized. | An indexed, reviewed frame of the editor's refusal dialog, or a decision/register entry accepting the generic localized message; absent either, the frame set for "affected surfaces" is incomplete. Severity: Medium if G-C-03 still binds, Low if the trade was decided. |
| AC-508-02/-04 (PARTIAL for CF10 only); AC-520-05 PASS | F-2 | The new identity design binds to `rclone.conf` bytes. The deleted engine's own comment ("rclone refreshes OAuth tokens during ordinary transfers. Bind the configured provider/root, not that routinely changing credential") shows the hazard was known. Every delta fixture remote is local/alias/shim/WebDAV/SFTP; none can rewrite `rclone.conf`. Primary's coverage boundary already excludes "hosted-provider timing or OAuth", so this is inside a declared gap, but the design dependency is a source fact, not a provider fact. | On an owned guest with an OAuth remote and an expired access token: `sha256sum rclone.conf` before/after `cloud_setup --validate-folders saves run1` unchanged **and** rc 0; or documentation that pinned rclone 1.75.1 does not persist refreshed tokens. If confirmed, Medium (recoverable by retry, misleading wording, frequent on short-lived-token providers). |
| AC-489-02 PASS ("controls reject … malformed receipts") | F-8 | `completed_audit_marker` calls `.get/.items/.replace` on `data`, `data['evidence']`, `issue`, `receipt`; a list/scalar at any of those raises `AttributeError`, which the `except (OSError, ValueError, KeyError, TypeError)` does not catch—the checker aborts instead of appending `invalid completion marker`. Fail-closed by crash, but the whole ceremony report is lost. | `test-cadence.py:35–76` containing a non-object `evidence`/readback/completion shape that yields the rejection message. Low either way. |
| AC-508-02 PARTIAL (selected creation proof) | F-5 | `--seed-folders` prints no `>>> unit/doing`; ES passes `selected.size()` as expected items; the old CREATE command prepended a unit line precisely for this. | The reviewed CF03/create frames (EN/FR 640×480) in `V/ui/evidence-index.json` showing acceptable row 2/3 text. Low. |
| AC-512-02/513-02 catalog PASS | F-9 | `.pot` gains 7 msgids vs ~50 new sources; orphan FR entries; "PRESS ANY BUTTON TO CONTINUE" translation removed. `msgfmt --check` would not catch an absent msgid. | A grep of the frozen ES for `PRESS ANY BUTTON TO CONTINUE` callers; `xgettext` regeneration diff. Low, hygiene. |

AC-508-01 PASS, the restore/validator boundary logic, the DuckStation helper and launchers, `CloudFolderValidation` binding, and the retention/cadence core paths traced consistently in my blind pass (section B there) and I found nothing in the primary's analysis of them to refute.

---

## 4. Three-way comparison (blind list ↔ primary ↔ this pass)

| My blind | Primary | Disposition now |
|---|---|---|
| F-1 | **F-03** | Converge. Primary's evidence and remedy stand; add sibling-pointer expectations and `--content-location`-without-validator to the remediation scope so an "adapt" pass does not stop at the seed arguments. |
| F-12 | **F-01** | Converge. Both #497 and #510 drift are demonstrable from packet artifacts alone (pin change in product diff; save-repair README; #500 criterion text). |
| F-2 | — (declared coverage boundary, blindspots 22/36) | New lead, Medium-conditional; strongest primary-unidentified item; needs OAuth target proof. |
| F-3 | — | New; Medium or Low depending on whether the generic localized refusal was decided; needs frame/decision evidence. |
| F-4, F-5, F-6, F-7, F-11 | — | Low leads; F-5 and F-6 touch "affected frames reviewed" claims. |
| F-8 | — (AC-489-02 PASS) | Low; possible over-grade pending the cadence test source. |
| F-9 | — | Low hygiene; not a verdict change. |
| F-10 | #519/#516 scope (acknowledged) | Agree it belongs to #519; the `layout=2`/`fleet_made` interaction with build-43d0bc3 devices is worth naming explicitly in #519's residue list. |
| — | **L-01** | Agree Low lead; couple its fix decision with F-2. |
| — | **L-02** | Cannot verify from packet; Low not misgraded. |
| — | **F-02 withdrawn** | Agree; no publication requirement asserted. |

Net: no primary Medium is refuted; none appears inflated. My blind list contains two Medium-grade leads (F-2, F-3) the primary did not surface, both inside areas the primary either declared out of fixture reach (OAuth) or graded PASS on frame review I cannot see.

---

## 5. What cannot be judged from this packet

- Everything under `B/`, `S/`, `S2/`, `V/`, `inputs/criteria.json`, `inputs/source-manifest.json`, `inputs/verdicts.jsonl`, `00-running-log.md`, owner-readbacks, frames, and `pkgcheck/cadence/retention` logs. AC-461/489(-01,-03)/490/491/492/494–496/498–504/506/517/519 and all AC-507-x remain **unassessed by me**, not passed.
- `checks/*/results.json` give rc and normalized placeholders only; that the run-time worktree was e6645cb5/4e410dc9 depends on owner-readbacks not in the packet. `docs/qa-logs/2026-10-07-cloud-validator/README.md` binds its counts to 6f89bc7c (pre-#520); frame reuse across that gap (AC-508-04 "unchanged tests keep their exact input identity") is unverifiable here.
- Live tracker state (F-01 "snapshot vs tracker").
- Private device/cloud/alignment material is excluded by design and carries no severity.
- Reviewer identity: the primary's 04-analysis names an external model/slug. Nothing in my output can establish that identity; AC-507-03 depends on the facilitator's receipts (served model, effort, outcome, digest), not on reviewer prose.

---

## 6. Closing

Primary F-01 and F-03 survive refutation at Medium with the extensions above; F-02 stays withdrawn; L-01/L-02 are correctly graded as far as the packet allows. The items the primary should add to its verification queue, in priority order, are my F-2 (OAuth token refresh vs config digest; target proof required), F-3 (lost refusal guidance; frame or decision required), then F-8/F-5/F-6 as Low checks against receipts I cannot see. All of the above are leads requiring primary verification against primary artifacts before any verdict or punch-list item changes.