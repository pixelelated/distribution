# Independent blind review — Milestone delta #507 (frozen ac64c806 / e6645cb5 / ES 4e410dc9)

Method: source reading of the four diffs and six full artifacts in the packet, cross-checked against `checks/*/results.json` and the three frozen issue bodies. No checks were run by me. Where a finding depends on an interaction with a real provider, device or runtime I label it a **source lead needing target proof**; where the packet itself demonstrates the behaviour I label it **confirmed**.

---

## A. Findings

### F-1 — Two delta-added regression tools cannot pass against the delta's own product source (confirmed defect, retained tool)
**Severity: Medium** (tool/evidence integrity; not a player-facing defect)

- `inputs/distribution-tools-diff.patch`, `tools/pixelelated-cloud-folder-test`: `seed()`, `fresh_beside_legacy()`, `carried_root()`, `interrupted_state()`, `write_refused()` all call `good(f,'cloud_setup','--seed-folders')` with no category list; `explicit()` requires `--set-saves-remote /Selected/Saves` to yield `('/Selected/Saves','/Selected/Backups','/Selected/Content')`; `guard()` requires `'>>> why ' in r.stdout` from a bare `--seed-folders`.
- `tools/pixelelated-cloud-folder-vm-test`: `script('cloud_setup','--seed-folders')` (default `ok=True`) and `assert 'SETTINGS_REMOTE="/Selected/Backups"' in pointers`.
- Frozen product: `cloud_setup:785-786` refuses a bare `--seed-folders` with exit 2 and the sentence `Choose which cloud folders to create.` (no `>>> why`); `cloud_setup:733-765` writes `SAVES_REMOTE` only (no sibling derivation).
- Demonstrated: `checks/retrospective-controls01/results.json` rc=1; `folder-regression-tool.log`: `FAIL fresh-empty-seed-beside-legacy cloud_setup ('--seed-folders',): rc=2`.
- Contrast: `tools/cloud-round-trip` (same tools diff) was updated to independent pointers and `--seed-folders saves,settings,roms,bios,media`; `last-good-scripts-test` gates on `SEED_ARGS`/`VALIDATOR_AVAILABLE`. These two tools were not.
- Secondary hazard: the vm-test's `ok=False` cases (`future-marker`, `relative-future-marker`, `dot-*`) would pass *vacuously* via the argument refusal, not via the guard under test.
- Requirement vs actual: AC-508-02/-03 cite synthetic linking/seed/public-config proof. Any receipt from these two tools can only predate the `--seed-folders <csv>`/independent-pointer change and must not be counted as current proof. The still-valid proof for those criteria is `checks/cloud-controls01/results.json` (`validator`, `save-layout`, `content-scope`, rc 0) whose tools are current.
- Falsifying observation: a `result.json` from either tool showing all cases PASS with `source_sha256` matching e6645cb5's `cloud_setup`.

### F-2 — Configuration identity hashes the live `rclone.conf`; rclone persists refreshed OAuth tokens into that file, so first-use-after-expiry checks/scans fail with misleading reasons (source lead needing target proof)
**Severity: Medium** (recoverable by retry; misleading wording; undetectable by the frozen fixtures)

- `cloud_setup:548-566 validation_context`: `config_id` = sha256 over `rclone config file` bytes (+ sync conf + paths).
- `cloud_scan:171-189 context_id`: hashes `/storage/.config/rclone/rclone.conf`; `cloud_scan:216-220 write_completion` fails with `>>> why YOUR CLOUD SETTINGS CHANGED. CHECK AGAIN` (exit 1) when the hash moved during the scan; `--stamp-valid` (231-244) re-hashes it.
- `cloud_folder_validate:265-269`: raises `configuration-changed` when the after-context differs.
- `ES GuiMenu.cpp:6927-6932` compares started/current context; `6960-6967 stillSelected` compares the page-build context before CHECK/CREATE and shows "THE CLOUD CHECK IS NO LONGER CURRENT"; `6895-6899` reports an invalid result as "COULDN'T CHECK YOUR FOLDERS. CHECK YOUR CONNECTION".
- rclone writes a refreshed OAuth token back to its config file during ordinary listings (Dropbox/Drive/OneDrive). The deleted `cloud_migrate_layout` (`inputs/distribution-product-diff.patch`, `remote_fingerprint()`) explicitly documented and avoided this ("rclone refreshes OAuth tokens during ordinary transfers. Bind the configured provider/root, not that routinely changing credential"); the replacement design reintroduces the dependency.
- Expected actual behaviour on an OAuth remote whose access token has expired: the first opening scan after expiry ends "SETTINGS CHANGED"; the first CHECK FOLDERS ends "CHECK YOUR CONNECTION"; after a successful CHECK FOLDERS that refreshed the token, CREATE FOLDERS on the same page refuses until the page is reopened.
- Coverage limitation: every fixture remote in the delta is `type = local`/alias (`rasteratops-cloud-layout-test`), shim `local` (`last-good-scripts-test`), or WebDAV/SFTP (`cloud-round-trip`, vm-test) — none can rewrite `rclone.conf`.
- Falsifying observation: on an owned GENERIC_X64 guest with an OAuth remote and a deliberately expired access token, `sha256sum rclone.conf` before/after `cloud_setup --validate-folders saves run1` unchanged **and** rc 0 — or proof that the pinned rclone is configured not to persist tokens.

### F-3 — The new path editor discards the script's refusal reason that an earlier audited requirement (G-C-03) made player-facing (confirmed source regression)
**Severity: Medium** (player guidance regression; worst for bucket providers)

- `inputs/es-diff.patch` `cloudSetupOpenPathEditor`: `ApiSystem::executeScriptLegacy(... , [](const std::string&) {}).second`; on `rc != 0` shows only "THE CLOUD FOLDER WAS NOT CHANGED. CHECK THE PATH AND YOUR CONNECTION, THEN TRY AGAIN." The removed editor surfaced `why` line by line.
- The scripts still print the reason: `cloud_setup:473-474` ("...empty part... Try X."), `530-539` bucket explanation ("Try something like /pixelelated-saves-yourname/Saves instead."), `541-543` provider refusal. `cloud_setup:756-757` still claims "Under the interface's THE CLOUD FOLDER WAS NOT CHANGED: this line says why" — now stale.
- Also inconsistent refusal strings for identical input across setters (`cloud_setup:672` "...has characters your cloud sync settings can't hold." vs `:742` "That folder name can't be used.") — moot while ES hides them, but it will matter if F-3 is fixed.
- Requirement vs actual: AC-508-06/513-02 "adjacent setup guidance accurate"; a bucket-name refusal now reads as a connectivity problem.
- Falsifying observation: a frame from the frozen ES showing the bucket/empty-part reason under the editor's refusal dialog.

### F-4 — "No ancestor outside the selected root is read" holds for the validator and restore, not for `cloud_setup` folder discovery (design inconsistency; source lead)
**Severity: Low**

- `cloud_folder_validate:9` and the restore diff (`absent_not_broken` with `boundary="${ROOT}"`) bound probes to the selected root; the harness proves it (`unreadable selected parent stays unreadable without account-root discovery`).
- `cloud_setup:285-299 absent_not_broken` walks to `remote:`; it is used by `folder_listing` (`:346`) ← `folder_exists` (`:353-371`) ← `--folder-state` (`:599`), `--seed-folders` readback (`:860`), and `syncpath_problem` (`:522`). `folder_exists:367-370` also lists the parent (account home for a one-component relative name).
- The harness silently dropped the old "cloud_setup carries the identical function" check for current source (`if [ "${LL_SCOPED}" -eq 0 ]`), documenting the divergence rather than resolving it.
- Impact is only metadata reads (dirs-only), nothing is offered from them; but the opening scan (`cloud_scan:286-293` → `--folder-state`) can still list the account root on a provider with non-standard not-found codes.
- Falsifying observation: argv log of `--folder-state` with a shim failing rc 1 on `SAVES` and its parent, showing no `lsf --dirs-only qa:/`.

### F-5 — `cloud_setup --seed-folders` emits no `>>> unit`/`>>> doing` protocol while ES declares N expected items (source lead; needs frame confirmation)
**Severity: Low**

- `GuiMenu.cpp:6989-6990`: `new GuiCloudTransfer(window, "/usr/bin/cloud_setup --seed-folders <csv>", _("CREATING CLOUD FOLDERS"), (int)selected.size())`.
- `cloud_setup:785-868`: prints only `OK/MISSING <dir>` and `>>> why ...`; no unit/doing lines. The previous CREATE IT command prepended `echo '>>> unit CLOUD FOLDER||'` for exactly this reason (removed in `es-diff.patch`).
- `CloudTransferJob.cpp:31` sets `mItemCount = mItemsExpected` with no units to fill it. Row 2/3 wording on the CREATING page therefore depends on defaults; D-UI-026 ("ITEM 1 OF n from the first announcement") is not met by the emitter.
- Falsifying observation: the reviewed CF create frames (EN/FR 640×480) showing the item rows populated as intended.

### F-6 — Misleading failure wording in the folder page for non-connectivity causes (confirmed source; wording)
**Severity: Low**

- `GuiMenu.cpp:6960-6967`: if the page was built with an invalid context (unreadable `cloud_sync.conf`, no remote, `timeout 5` expiry), every CHECK/CREATE press says "THE CLOUD CHECK IS NO LONGER CURRENT. CHECK YOUR FOLDERS AGAIN." instead of the truthful `YOUR CLOUD SYNC SETTINGS COULDN'T BE READ` that `cloud_setup:319-324` emits (ES ignores stdout on rc 2).
- `GuiMenu.cpp:6895-6899`: a `configuration-changed`/parse failure reads "CHECK YOUR CONNECTION".
- `cloud_setup:417-424 folder_marker_write` returns 5 with no `>>> why` on `rcat`/re-read failure; the page then falls back to a generic code sentence while other seeding failures print `YOUR CLOUD FOLDERS COULDN'T BE CREATED` (`:804,867`).

### F-7 — Dead/misleading fallback when `/usr/bin/cloud_scan` is absent (confirmed source; unreachable on the pinned image)
**Severity: Low**

- `es-diff.patch` keeps `if (!exists("/usr/bin/cloud_scan")) { cloudOpenTransferOptions(window, backup); return; }` but `cloudOpenTransferOptions` now begins `if (!cloudScanStamped("done")) { cloudCheckChanged(window); return; }` and `cloudScanStamped` returns false when `sCloudScanRun` is empty. The branch can only produce "no longer current". Same for `cloudScanContent`. Harmless because `rclone/package.mk` installs `cloud_scan`, but the branch should either be removed or say what it means.

### F-8 — `tools/ceremony-check completed_audit_marker` crashes rather than reporting on mistyped receipts (confirmed by source reading)
**Severity: Low** (host control)

- `inputs/distribution-tools-diff.patch`: `data['evidence'].items()`, `issue.get(...)`, `receipt.get(...)` raise `AttributeError` when `evidence`/readback/completion JSON is a list or scalar; the handler is `except (OSError, ValueError, KeyError, TypeError)`. AC-489-02 requires malformed receipts to be *rejected*; here the checker aborts. `checks/host-controls01/results.json` `cadence` rc 0 does not show whether `test-cadence.py:35-76` includes a non-object shape.
- Falsifying observation: a cadence test case with `"evidence": ["x"]` producing `audit: invalid completion marker`.

### F-9 — Catalog/template drift (confirmed; low)
**Severity: Low**

- `locale/emulationstation2.pot` gains only seven msgids while the fr `.po` gains ~50 new source strings (CLOUD FOLDERS, CHECK FOLDERS, …) — the template is partially stale.
- Orphan fr entries with no source string: "YOUR CLOUD FOLDERS COULD NOT BE CREATED" (source says COULDN'T), "BACK UP SAVES TO POPULATE THIS FOLDER, OR COPY YOUR SAVES HERE FROM A COMPUTER.", "MOVED YOUR CLOUD FOLDER?", "USE CHANGE CLOUD FOLDER ON EACH DEVICE.", "ADD ROMS AND BIOS FROM A COMPUTER", "CLOUD SETUP", plus retained translations for removed flows ("CHOOSE A FOLDER", "DISCARDED SAVES", "YOUR CLOUD HAS NO ROMS OR BIOS AT %s…").
- `msgid "PRESS ANY BUTTON TO CONTINUE"` translation was deleted; the only visible caller was removed — confirm no other `setCompletedAction` caller remains (otherwise FR falls back to EN). `checks/es-controls01` `catalog`/`vocabulary` rc 0 would not catch a missing msgid.

### F-10 — Residual unpublished-state behaviours and marker interaction with the owner's un-upgraded devices (existing open scope; low)
**Severity: Low** — tracked by #519/#516

- `cloud_backup` (product diff) `superseded_saves_setting`: `case "${SAVES_REMOTE%/}" in /GAMES|/ROCKNIX/Saves)` — `/ROCKNIX/Saves` was never a public default (#510 "Unpublished fork/PR states are historical, not public compatibility gates"; AC-508-03). Effect is only "don't auto-create", so harmless, but it is a compatibility rule for an unpublished state.
- `cloud_setup:808/417-424` writes `layout=2` at `/pixelelated/.layout` on CREATE FOLDERS (saves). The retained engine on devices still running build 43d0bc3 (#500 readback) treats a `layout=2` marker as `fleet_made` → `RELOCATE_MERGE=1` (deleted `cloud_migrate_layout`), i.e. an older device's TIDY would merge instead of refuse. Not a public-user interaction; it is exactly the #519 pre-upgrade alignment gate and should stay named there.

### F-11 — Interface-thread shell-outs bounded only by `timeout 5` (source lead needing target timing)
**Severity: Low**

- `GuiMenu.cpp:6941` (page build) and `:6962` (`stillSelected`) run `timeout 5 /usr/bin/cloud_setup --validation-context` (two bounded rclone starts + sha256) on the UI thread; `cloudScanStamped` runs `timeout 5 cloud_scan --stamp-valid` on the UI thread from `cloudOpenTransferOptions`. The project's own history (fork #103) moved comparable work behind `GuiLoading`. Needs A53 timing before grading above Low.

### F-12 — Stale tracker wording (not defects)
- `inputs/issues/497.json`: criteria 3 and 4 remain `[ ]` and "Current state — 07:02" says "Actual handoff is still pending", while AC-500-03's device readback records BUILD_ID 43d0bc3 installed. AC-497-03/-04 cannot be counted from the tracker; they need `B/rg35xxsp-adoption01/h700-artifact-acceptance.json` (not in packet).
- `inputs/issues/510.json` "Current qualification": "Both product branches remain local/unintegrated; the product pin is unchanged… a new owned #520/#521 guest is active… No new firmware build or #507 audit has started" vs `docs/qa-logs/2026-10-08-save-repair-cases/README.md` ("integrated through #508 in e6645cb5ea… guest retired… #515 and #520–#523 closed"). AC-510-04 is unchecked although the "Source-supported repair disposition" section records the instructions-only disposition. AC-510-06 (checked) asserts tracker/checkpoint agreement; the frozen body does not agree with itself.
- The frozen #504 excerpt lists four criteria; the audit's AC-504-05 (power readbacks) has no visible origin in the excerpt — provenance should be confirmed in `inputs/criteria.json`.
- Minor stale comments: `cloud_setup:19-20` ("the chooser's, fork #352"), `:756-757` (see F-3); `cloud_scan:20` `--folder` mode retained with no ES caller (retained interface, not a defect).

---

## B. Things I traced and found consistent (so they are not counted as findings)
- Retirement sweep: `cloud_migrate_layout` deleted and removed from `rclone/package.mk`; no remaining product reference in `cloud_backup`/`cloud_scan`/`cloud_setup`/ES; startup step, `armCloudFolderStep`, TIDY row, `--follow/--join/--settle` all gone; historical tools (`cloud-pair-migration`, `rasteratops-vm-cloud-epic`, `pixelelated-vm-cloud-boundaries`, `migration-protocol.sh`) refuse before writing when the engine is absent (AC-508-01).
- `cloud_content_restore` `absent_not_broken`/`list_content_dirs` boundary logic traced for `ROOT` = `qa:`, `qa:/`, `qa:/x/`; partial output → exit 5; `DIRS` name validation; `SYSTEM_SAVE_EXCLUDES` anchored at system root; awk cloud filter matches `ROMs/n64/*.st[0-9]`.
- Filter/validator/content consistency for PSP `PSP/SAVEDATA`, DuckStation `psx/duckstation/memcards` depth 4, N64 slots at system root only; validator depth bounds and `deeper-folders-not-checked`.
- `duckstation_screenshot_path`: regular-file check, single-key/section guard, owner-symlink respect, write probe, same-mode/owner staged replace, identity recheck, rmdir of a target it created on failure; launchers call it `|| :`; `install -m 0755`; both entrypoints.
- ES unit shape table line references match the frozen scripts (`cloud_scan:219/358`, `cloud_setup:804/867`); `lockHeldOutcome` keeps sync wording; `CloudFolderValidation` binds run/config/paths/categories and treats `unreadable` as incomplete.
- `ceremony-check` closure counting after the exact completion time, future/unzoned refusal, evidence hashing (apart from F-8).
- `retention-report`: fixtures only as exact archive members inside protected roots; hardlink/uid/format/active-use/PID holds; no deletion path.

---

## C. Coverage limitations
- Not in the packet: `00-running-log.md`, `inputs/source-manifest.json`, `inputs/criteria.json`, `inputs/verdicts.jsonl`, all `B/`, `S/`, `S2/`, `V/` receipts, owner-readbacks, frames, `pkgcheck`/`cadence`/`retention` logs. AC-461, 489, 490, 491, 492, 494, 495, 496, 498, 499, 500, 501, 502, 503, 504, 505/506, 517, 519 and all AC-507-x meta criteria are therefore **unassessed** here, not passed. Private/device/cloud items were excluded by design; no severity is attached to their absence.
- `checks/*/results.json` show rc and `<distribution-worktree>` placeholders only; I cannot confirm the worktree at run time was e6645cb5/4e410dc9 (owner-readback needed).
- `docs/qa-logs/2026-10-07-cloud-validator/README.md` binds its numbers to 6f89bc7cec (pre-#520); the frozen product is e6645cb5. `checks/cloud-controls01` re-runs cover the changed tools; UI-frame reuse across that gap (AC-508-04 "unchanged tests keep exact input identity") is unverifiable from this packet.
- Only `GuiMenu.cpp:6790-7010` of the frozen ES is available verbatim; other ES behaviour is inferred from the diff.
- F-2 and F-4 need provider/guest proof; F-5 and F-3 need the reviewed frames; F-8 needs the cadence test source.