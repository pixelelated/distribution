# Refutation review — pixelelated M7 P4, second pass (same reviewer)

Scope note: packet bytes only. "Target-executed" means a retained installed-guest result is in the packet; "source-only" means I read the shipped source and no execution exists in the packet. P5 device/publication items are not treated as implementation failures. No product edit is proposed or assumed.

---

## 1. Additional findings from the whole packet

### R-01 — `STATE=stranded-at-root` is computed but no consumer in the scan-first flow acts on it; the chooser cannot select the cloud root

**Severity:** Medium — source-only (not target-executed). Sibling of F-01/#467; repair scope, not a separate blocker.

**Location:** `cloud_setup:519–530,538,555–565` (AT_ROOT counted; FOUND computed only when `AT_PATH -eq 0 && AT_ROOT -eq 0`; `STATE=stranded-at-root` when CP set, AT_PATH=0, AT_ROOT>0); `cloud_setup:580–582` (`--set-content-remote` normalises to `/` and refuses "root path not allowed"); `GuiMenu.cpp:5228–5251` (only `found-elsewhere` and `empty` are acted on; every other state → `then()`); `GuiMenu.cpp:5256–5276` (chooser lists `found` plus root-level subfolders only; `--use-content-root` is not reachable from it).

**Trigger:** upgraded device whose default `CONTENT_REMOTE=/pixelelated/Content` has been materialised, whose cloud still holds pre-`CONTENT_REMOTE` systems at the account root (e.g. `gb/`), and whose local library holds content for those systems → `AT_ROOT=1`, `AT_PATH=0`, `STATE=stranded-at-root`.

**Actual:** ES proceeds to `cloud_scan --content` against `/pixelelated/Content`; the picker lists nothing of the root; no offer, no question; the chooser cannot name `/`.
**Required:** D-CLOUD-156 ("the content folder is found under the cloud root when the configured content root holds no ROMs or BIOS, with a choice offered when nothing is found"), D-CLOUD-167 ("the one the scan found is used without a question"). The automatic path is implemented only for the `<saves-parent>/Content` candidate.

**Falsifying observation:** an ES consumer of `stranded-at-root` outside the excerpt (e.g. a hub row that still offers `--use-content-root`), or a recorded decision confining automatic discovery to the sibling Content folder. The primary should check the full `GuiMenu.cpp`; the excerpt is complete for `cloudOfferContentFolder` itself.

### R-02 — a *missing* `CONTENT_REMOTE` key is the cloud root to the content scripts and `--content-location`, but the default/follow value to seeding and migration

**Severity:** Low — source-only; transient window.

**Location:** `cloud_content_restore:179,207` and `cloud_content_backup:176,204` (absent key → `""` → `ROOT="${REMOTENAME}"`; both explicitly do not run `cloud_sync_helper`, lines 212–213); `cloud_setup:511,555` (CP `""` treated as explicit root); versus `cloud_setup:770–774` (missing → `/pixelelated/Content`) and `cloud_migrate_layout:113` (`content_unset` → follow/default).

**Trigger:** stock-shaped conf adopted from ROCKNIX (no `CONTENT_REMOTE` line), NOT NOW at the folder step, then RESTORE FROM THE CLOUD before any saves sync has materialised the key.

**Actual:** the opening scan classifies the account root; the content scan lists the whole account root (`sizes_under "${ROOT}"` recursive). **Required:** I380-L24's "one representation" (the table's T21 claim covers only the layout tool). The primary graded I380-L24 PASS on the layout tool alone.

**Falsifying observation:** `cloud_sync_helper` (not in packet) being invoked by `cloud_scan`/ES before any content path, or stock ROCKNIX `cloud_sync.conf` shipping `CONTENT_REMOTE`.

### R-03 — the startup composite can now exit 124 with no `>>> why`, and ES `whyForCode` has no 124 case

**Severity:** Low — source-only.

**Location:** `main.cpp:686` (`timeout 30 /usr/bin/cloud_scan --folder; … exit "$_s"`); `ThreadedCloudSync.cpp:80–96` (3/4, 5, 7/8, sentinels, default); `cloud_scan:96` maps 124 itself, but the outer timeout kills `cloud_scan`, so no why line is printed.

**Actual:** card reads `COULDN'T FINISH - SOMETHING WENT WRONG`; the scripts' own vocabulary for 124 is `YOUR CLOUD STOPPED ANSWERING` (`cloud_content_*:why_for`, `cloud_scan:why_for_rc`). Same family as F-02; also applies to `--needs-step` rc 2 at `main.cpp:687` (conf unreadable → generic sentence, where `cloud_restore` would have said `YOUR CLOUD SYNC SETTINGS COULDN'T BE READ`).

**Falsifying observation:** a 124/2 mapping elsewhere in ES not in the excerpt, or evidence the outer 30-s ceiling is unreachable given the inner `timeout 20` bounds (two `--state` calls have no inner bound).

### R-04 — the opening scan's root-dirs listing is fatal although it serves only the chooser

**Severity:** Low — already tracked (state table T25 residual).

**Location:** `cloud_scan:243–244` (`stop_on "${rc}" "root listing"`) versus `:241–242` (content-location "reported, not fatal").

**Trigger:** provider policy allowing the configured prefixes but denying root enumeration (the table's T25). **Actual:** BACK UP/RESTORE pages never reach options. The table records "Root probe may refuse scan … S3 policy/prefix behavior remains candidate qualification"; no new claim beyond that.

**Falsifying observation:** a T25 S3 fixture showing the opening scan completes, or a decision accepting the failure.

### R-05 — `cloud_setup --seed-folders` runs `--write-marker` without a ceiling

**Severity:** Low — source-only.

**Location:** `cloud_setup:744` (`timeout 30 … --settle`) versus `:797` (`"${layout_tool}" --write-marker` unbounded). `main()` then performs probe, features, `read_marker` cat, `rcat`, `read_marker` cat — five network calls each under `RCLONE_LIST_OPTS`/`NET_OPTS` retries, under the interface's "90 s box" the file's own comment names (`:784`).

**Falsifying observation:** the GuiLoading wrapper around seeding having its own bound (not in packet), or a measured worst case under the box.

I found no further defects in the newly supplied ES/`AtomicFileUtil` excerpts (see §4 for resolved "cannot judge" items). The `111-sway-init` `cut -b 5` card-number derivation would truncate `card10+`; that is pre-existing upstream, not a P1–P3 change, and the VM has `card0` — noted only so the wrapper's multi-digit control is not mistaken for end-to-end coverage.

---

## 2. Refutation attempts on the primary findings

### F-01 (High, #467) — content classifier vs restore disagree

**Attempted refutation:** (a) "Any directory at an explicitly configured path is the player's content by choice" — fails: I352-L33's text is literal ("holds no `ROMs/` and no known system folder → the page says so"), and D-CLOUD-156 is the owner's own requirement ("not showing content that's not relevant"). (b) "Root-tiered content needs local presence" — fails: I352-L32 names the `legacy_dirs`/`supported_systems` rule, and I380-L23 passed on a root `ROMs/` scan, so the classifier contradicts the scanner the page then shows. (c) Probe validity — `refutation-03/results.json` shows seven cases, before==after, rc 0, 3 PASS/4 FAIL, on bundle `b77e47e5` / source `7afa9efcfc` (`console.log:2,5`); internally consistent. The `boundaries.py` base is not in the packet (§4).

**Verdict: agree, severity High stands** for the aggregate (two distinct wrong classifications, target-executed; blocks or misdirects the first restore on an empty-local device). Split, B-01-type (false `ok` suppresses the approved fallback) is the High half; B-02-type is Medium.

**Nuance for the repair, not a refutation:** D-CLOUD-167's silent re-point to `found` sits in tension with #380/D-UI-042 for an *explicitly configured non-default* folder. If the classifier starts returning `empty`/`found-elsewhere` for a player-chosen path holding unrelated folders, the question (not a silent `--set-content-remote`) is the least-surprise outcome; automatic re-point should stay confined to default/unset values. Owner's call; record it.

**What would make F-01 false:** `unrelated-configured → empty` and `tiered-explicit-root → ok` on frozen 14, or a recorded decision adopting the current semantics.

### F-02 (Medium, #468) — refusal is safe but says the folder is missing

**Attempted refutation:** "4 is the shared vocabulary's 'not found' and the cloud scripts agree" — fails: `cloud_migrate_layout` defines 4 as *refused* (unsupported marker `:994`, `..` pointer `:1166`, destination has files `:1365`) and emits a truthful sentence only under `MODE=--apply` (`:992`); `cloud_scan:163–168,177–183` discard stdout and map through `why_for_rc:95`. UI26 logs on both 07-failed and 08 show `COULDN'T FIND YOUR CLOUD FOLDER` with pointers unchanged. D-UI-028 requires a truthful why; the corrective action (update) is not conveyed. Not Low: the player is pointed at the wrong remedy (recreate/choose a folder).

**Verdict: agree, Medium stands.** Extend the sibling list the primary's survey already has (`--follow`, `--state`) with `main.cpp:687` (`--needs-step` rc 2 → generic) and R-03 (outer 124). Safe refusal is proven by pointers; marker bytes are asserted by the primary but not in the packet (§4).

**What would make F-02 false:** a UI26 frame/log reading `YOUR CLOUD FOLDER COULDN'T BE READ` (the string whose French already exists, `es-diff.patch:523–524`).

### F-03 (Medium) — standalone sign-in pages omit French

**Attempted refutation:** "D-UI-051's mechanism is ES gettext; pages served by Python/C are outside it" — fails: D-CLOUD-164 explicitly lists "the phone page's close confirmation; the finishing page's two lines" among the thirteen and says "each lands with its French (D-UI-051)". That owner-approved row refines the mechanism question. I351-L62 is a source contract; no French-mode run is claimed and none is needed to establish the miss.

**Verdict: agree, Medium as an acceptance/contract gap.** Scope note for the fix: the rest of the phone page (`PAGE`, `PIN_PAGE`, `DONE_PAGE`, keyboard labels) is English and expressly deferred by D-UI-051's own text; translating only strings 12–13 on an otherwise English page implies a locale mechanism decision for the whole surface (system.language vs the phone's `Accept-Language`). Record that before implementing.

**What would make F-03 false:** `cloud_oauth`/`cloud-signin-window.c` selecting text by `system.language` outside the excerpts, or a decision exempting standalone HTML.

### Primary PASS/PARTIAL grades I would narrow

- **I380-L24 PASS** → suggest a note or PARTIAL: "one representation" is proven for the layout tool; the content scripts read a missing key as root (R-02).
- **I363-L75 PASS** — correct on behaviour; the checkbox text ("1 for the current folder") is now stale for the #391 historical-content sub-case (B-10); reconcile the text, not the code.
- **I409-L239 / I353-L32** — B-05 bears on "KEEP USING leaves a device on `/ROCKNIX` for good": the kept device's live shelf triggers a false `migration-pending` on current-layout siblings. Keep I353-L32 PARTIAL; add B-05 to its ledger.

---

## 3. Reassessment of B-01 … B-14

| ID | Disposition | Class | Reasoning against the primary analysis and added context |
| --- | --- | --- | --- |
| B-01 | **Keep** (High) | Runtime defect, target-executed | Identical to F-01's `unrelated-configured` / `unrelated-configured-fallback` rows (`refutation-03/results.json:58–109`). Consumer branch confirmed in the supplied `GuiMenu.cpp:5239–5243`. Secondary note (listing errors read as absence, `cloud_setup:524,526,543`) is source-only and matches the primary's "Content Adjacent: listing error versus emptiness — FILE-FOLLOWUP within #467". |
| B-02 | **Keep** (Medium) | Runtime defect, target-executed | F-01's `tiered-explicit-root` / `legacy-explicit-root` rows (`results.json:175–224`). Consequence (chooser offers `/ROMs` → `remote:/ROMs/ROMs/<sys>`) remains source-reasoned. Merge into #467; severity rolls up into F-01 High. |
| B-03 | **Keep** (Medium) | Runtime defect, installed logs | = F-02/#468. Supplied `ThreadedCloudSync::whyForCode` confirms the card's fallback carries the same 3/4 collision. Add callers: `main.cpp:687` (rc 2), outer 124 (R-03). The French for the true sentence exists only on the `--apply` path. |
| B-04 | **Retract as defect → Low contract drift** | Contract drift | D-CLOUD-173 (2026-10-02) expressly authorises boot-only join/state/follow preparation inside the startup worker with a 30-s ceiling and "a failed preparation ends the worker without transferring". The rewritten I363-L73 cites 170/172/173; the primary's reading ("the no-per-sync rule applies to the transfer scripts") is the correct one. Residuals: (i) I363-L73/I353-L33 wording should name the boot-only exception explicitly; (ii) boot-path cost for the NOT-NOW population (worker scan at `main.cpp:686` plus the step page's second `cloud_scan --folder` at `GuiMenu.cpp:5517`) has no numeric criterion and no measurement — an observation, not a gap in an existing checkbox; (iii) the mis-mapped reason on failure is B-03, not a separate item. |
| B-05 | **Keep** (Medium) | Source-only defect; untested cell | Re-read `cloud_migrate_layout:819–828` and `:1240–1244,1355–1362,1455–1459`: a sibling's live `<earlier>-replaced/` shelf (KEEP USING device on `/ROCKNIX`, or an un-upgraded device on `/GAMES`) makes every current-layout device read `migration-pending` on each transfer-page open; TRY AGAIN relocates/merges that sibling's shelf. The state table calls the shelf check deliberate ("a remaining old shelf is also reported by the folder scan") but has no kept-sibling cell (T20–T26). Not in `--needs-step`, so boot is unaffected. Not target-executed; moves to runtime only with a host/guest case. |
| B-06 | **Keep** (Medium) | Source-only defect; untested cell | `migration_record_load:1056–1072` → 5 on remote/fingerprint mismatch; `layout_state:795–798` returns before any fact; `--needs-step:1509–1512` returns 0 unvalidated; `--join/--follow` → 3, `--settle/--keep/--write-marker` → 5 (`:1185–1191`); `main.cpp:687` exits 5 → no startup restore every boot; `cloud_scan:96` → `STOPPED ANSWERING`. Add: wizard seeding then fails with "couldn't be checked" (`cloud_setup:748–750`) while the real reason (`:1070`) is discarded by `>/dev/null`. No UI route removes the record. T23 covers interruption/retry, not a stale fingerprint; `.remote` is `listremotes \| head -1`, so adding an alphabetically earlier remote also triggers it. |
| B-07 | **Keep** (Low) | Source-only robustness | Three sequential `set_pointer` calls (`:878–884,922–924,948–952`) vs `conf_set`'s all-or-none (`cloud_setup:64–107`, used by `--set-saves-remote:675–677`). Each `sed -i` is atomic per key; the set is not. |
| B-08 | **Narrow → Low bookkeeping** | Evidence gap, not a defect | Retract the fallback-line clause: the 640-px whole-clause shortening is the size-aware policy (D-UI-045/D-UI-035) the primary cites at I349-L44/I350-L36. For post-10-01 strings (migration-pending dialog, `WHAT MOVED IS IN THE NEW FOLDER…`, `MANUAL UPDATES` + sentence, `ENABLE pixelelated SCREENSHOT`, script sentences), D-CLOUD-164 approves thirteen as baseline and D-WORKFLOW-094 permits later fine-tuning; the project's own practice (D-UI-112; `es-player-text.md`: "proposed by the fix streams, built with the proposed words, and put to the maintainer") lets proposed strings ship. Remaining ask: record those strings as proposed/put-to-owner in the ledger, as D-UI-112 did. Approval comments are not in the packet (§4). |
| B-09 | **Keep, narrowed** (Low) | Source-only; D-CLOUD-149 literal miss | `cloud_scan:60–72` is not the shared awk (`cloud_setup:131–178`, `cloud_migrate_layout:160–207`): it treats `export`/indented forms as absent and ignores control characters. Impact is mitigated because `read_folder` runs the strict reader first (`cloud_migrate_layout:1105–1107` exits 2 → scan stops) before line 211 is reached; the divergence is latent, but D-CLOUD-149's "every reader" is not met and the file's own comment claims it is. |
| B-10 | **Keep** (Low) | Contract drift | Behaviour is intentional (#391; primary notes "pending-record exception intentionally returns 0"). The checkbox text "1 for the current folder" needs the two 0-returning sub-cases (record present; current + `/ROCKNIX|/GAMES/Content`) named. |
| B-11 | **Retract** | — | Listings/mkdir/`exists_remote`/`resolve_src` all carry `RCLONE_LIST_OPTS` (`--low-level-retries 3 --timeout 30s --retries 1`, `cloud_content_restore:234`), which the scripts' own comment says the S3 backend hands to the SDK as attempts; the original #401 failure was the transfer path under ten retries. Target evidence (I401-L35: S3 scan rc 1 after 41.4 s with truthful reason) shows the listing path terminates. |
| B-12 | **Retract** | — | The primary directly inspected 09 frames for expected content per AC (e.g. `04-A-options-after-move.png` text) and cross-read `run.log`; a stale/partial scanout would show the wrong page, not the right one. Frozen-14 QA18 carries 78 frames with a 34-region frame-diff claim map (I354-L68), and ES/script bytes are byte-identical. Traceability is adequate. |
| B-13 | **Keep** | Confirming | Agrees with the primary: I344-L213 PARTIAL, I344-L229/L231/L256 PARTIAL, I351-L62 FAIL. D-CLOUD-164 settles my open question: D-UI-051 *does* apply to the phone confirmation and finishing page. |
| B-14 | **Keep** (Low) | Source-only; #352 P1 scope | `cloud_setup:581–585` refuses any whitespace and any `..` substring; `cloud_scan:243` lists all root folders; `syncpath_problem` and both `conf_get` readers accept spaces in double quotes. The chooser offers names the setter refuses. |

Previously "reviewed without defect" items stand. Resolved from the new excerpts: `LoadedConfig::record` semantics (`AtomicFileUtil.cpp:352–389`: record true for complete live/temporary, false for Backup/Damaged; `SystemConf.cpp:95–97` publishes only when `current.text == text` and `(record || source == Backup)`) — the guard is correct; `WLR_DRM_DEVICES` is written by `111-sway-init:37` and the wrapper's early return on its absence is fail-safe, with QA18 renderer records proving selection on target.

---

## 4. What I still cannot judge, and what settles it

1. **R-01 consumer completeness** — whether any ES surface outside `GuiMenu.cpp:5228–5276` consumes `stranded-at-root` or exposes `--use-content-root`. Settle: grep of the full ES tree for `stranded-at-root` / `--use-content-root`.
2. **R-02 window** — whether `cloud_sync_helper` materialises `CONTENT_REMOTE` before any content path can run on a stock-shaped conf. Settle: the helper's call sites and the stock ROCKNIX `cloud_sync.conf`.
3. **`timeout` semantics on the image** — BusyBox vs coreutils process-group behaviour for `timeout 20`/`timeout 30` wrappers (`cloud_scan:163,177`, `main.cpp:686`): whether a killed `cloud_scan` leaves `cloud_migrate_layout --join/--follow` writing pointers after the worker moved on. Settle: `readlink -f $(command -v timeout)` on the guest plus one wrapped `sleep` child test.
4. **UI26 marker bytes** — the primary states before/after hashes prove write refusal; the packet shows pointer files only. Settle: the marker-hash lines from `UI26-*` artifacts.
5. **`boundaries.py` base** — `Proof.start/reset/conf/put/hashes` underpin refutation-03; not in packet. Settle: the file, or a statement that it is the retained `cloud-boundaries-01/proof.py` base.
6. **B-05 / B-06 execution** — both are source-only. Settle: a host `last-good-scripts-test` case seeding `/ROCKNIX/Saves-replaced/<stamp>/x.srm` on a current-layout config (expect `STATE=current`), and one with a valid record plus renamed remote (expect a supported dialog or state).
7. **B-08 approvals** — tracker comments approving post-10-01 strings are not in the packet. Settle: #354/#383/#391 owner comments or a register row.
8. **Startup card rendering of the new `>>> unit CLOUD FOLDER||` / `>>> doing scan` lines** emitted by the worker (`cloud_scan:155–156`) under the SYNC SAVES title. Settle: the E/I startup frames the primary reviewed, read specifically for the card's line during preparation.
9. **R-03 reachability** — whether the outer 30-s ceiling can fire given the inner bounds. Settle: the two unbounded `--state` calls' worst case under `RCLONE_LIST_OPTS`, or a guest trace.
10. **rclone `--progress` on a non-TTY writing to stdout** — relied on by the guard's trace; I401 target results (LINK3/4 stop at 35.1/35.2 s) make this effectively settled, but no raw trace is in the packet.

Net effect on the primary's conclusion: unchanged — not RC-ready; three confirmed findings stand; B-05 and B-06 are the only new candidate product defects and both remain source-only until executed; B-04, B-11 and B-12 are withdrawn as defects.