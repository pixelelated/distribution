# Independent blind review — pixelelated M7 P4 (external reviewer)

Scope note: I reviewed the packet sources only. Where I say "observed", the evidence is in the packet (source lines plus retained outputs). Where I say "criterion/evidence gap", no product defect is proven; an exact criterion or its approval/evidence chain is unexecuted or untraceable in the packet. P5 device/publication items are not treated as implementation failures.

---

## B-01 — Configured content root with only unrelated folders classifies as `ok`; chooser question and `/…/Content` auto-fallback never run

**Severity:** High — observed code defect, target-executed on frozen 14 (bundle b77e47e5, source 7afa9efcfc; refutation-03/console.log:2,5).

**Location:** `cloud_setup:523-525` (`AT_PATH=$(rclone lsf --dirs-only "${REMOTE}${CP#/}" … | wc -l)` counts *any* subdirectory, with no ROMs/BIOS/known-system test), `cloud_setup:538` (fallback gated on `AT_PATH -eq 0 && AT_ROOT -eq 0`), `cloud_setup:557-558` (`AT_PATH>0 → STATE=ok`); consumer `GuiMenu.cpp:5239-5243` (`if (state != "empty") { then(); return; }`).

**Trigger:** `CONTENT_REMOTE=/Mine`; cloud holds `Mine/Photos/x.jpg` (and, in the second case, a real library at `/pixelelated/Content/ROMs/gb/A.gb`).

**Actual:** `refutation-03/artifacts/results.json:58-70` — `unrelated-configured` → `AT_PATH=1`, `STATE=ok` (expected `empty`). `results.json:97-109` — `unrelated-configured-fallback` → `STATE=ok`, `FOUND=""` (expected `found-elsewhere`, `/pixelelated/Content`). `console.log:11,13` record both FAIL. The ES consumer therefore takes `then()` directly: no "YOUR CLOUD HAS NO ROMS OR BIOS AT …" question, no chooser, no automatic re-point; the content scan then lists nothing of the player's.

**Required:** I352-L33 ("content root holds no ROMs/ and no known system folder → the page says so … with a row that opens the folder chooser") and I352-L44 ("… the scan looks under the cloud root's Content folder and … uses that folder automatically and writes CONTENT_REMOTE"). Neither can occur for any configured root that lists any subdirectory. The retained guest-11 D proof passed only because `CONTENT_REMOTE=""` bypasses `AT_PATH` (line 523).

**Falsifying observation:** a results row for `unrelated-configured` with `STATE=empty`, or a frame of the question dialog with `CONTENT_REMOTE=/Mine` holding only `Photos/`.

**Secondary note (same function):** all three listings discard errors (`2>/dev/null | wc -l`, lines 524, 526, 543), so a listing failure on the configured path alone reads as absence — the fail-closed rule the rest of the stack adopts (PL-027) is not applied here.

---

## B-02 — Explicit root (`CONTENT_REMOTE=""`) holding `ROMs/`/`BIOS/` or legacy system folders classifies as `empty`; player is shown a false "no ROMs" prompt and offered to move the pointer

**Severity:** Medium — observed code defect, target-executed on frozen 14.

**Location:** `cloud_setup:523` (AT_PATH skipped when CP empty), `cloud_setup:526-530` (AT_ROOT counts only root dirs equal to `cloud_content_backup --list` output, i.e. local dirs that *hold content*; never `ROMs`/`BIOS`, never `supported_systems`), `GuiMenu.cpp:5244-5248` (message "YOUR CLOUD HAS NO ROMS OR BIOS AT /").

**Trigger:** `CONTENT_REMOTE=""`; cloud root holds `ROMs/gb/A.gb` + `BIOS/qa.bin`, or legacy flat `gb/A.gb`; local `/storage/roms/gb` exists but is empty.

**Actual:** `results.json:175-187` `tiered-explicit-root` → `STATE=empty`; `results.json:212-224` `legacy-explicit-root` → `STATE=empty` (console.log:17,19). `cloud_content_restore --scan` for the same cloud would list `gb` (legacy rule, `cloud_content_restore:1307-1309`, 1343) and `ROOT=remote:` with `ROMs/` is a working root — so the page text contradicts the listing that follows. Choosing a folder from the offered chooser (`/ROMs`, `/BIOS`, …) re-points the device off a working root (`--set-content-remote`, `cloud_setup:586`).

**Required:** I352-L32 ("the same rule `resolve_src` applies" — local folder *or* supported system), I352-L33's prompt only when nothing is there, I380-L23 ("an explicit root holding ROMs/BIOS remains the selected location"). The classifier and the scan apply different membership rules (`has_content` vs `legacy_dirs`/`supported_systems`) and the classifier never tests for the tiered `ROMs/`/`BIOS/` shape at an explicit root.

**Falsifying observation:** `tiered-explicit-root` → `STATE=ok`; or the frozen-14 guest showing the options page directly (no question) for an explicit root with `ROMs/`.

---

## B-03 — cloud_migrate_layout's own return codes are interpreted as rclone codes by cloud_scan; unsupported-marker reason is lost and replaced by "COULDN'T FIND YOUR CLOUD FOLDER"

**Severity:** Medium — observed code defect (UI26 on both 07-failed and 08).

**Location:** `cloud_migrate_layout:991-994` (unsupported/malformed marker → `say` + `>>> why YOUR CLOUD FOLDER COULDN'T BE READ` *only when `MODE=--apply`* → `return 4`); `cloud_scan:163-168, 177-183` (`--join`/`--follow` run with `>/dev/null 2>&1`; rc 4 → `stop_on`); `cloud_scan:93-100` (`why_for_rc`: `3|4 → COULDN'T FIND YOUR CLOUD FOLDER`, `5|124 → STOPPED ANSWERING`, `* → SOMETHING WENT WRONG`). The migrate tool returns 2 (conf unreadable), 3 (nothing to do), 4 (refused: marker unsupported, `..` in pointer, destination has files), 5 (record/marker/pointer failure) — a disjoint namespace from rclone's.

**Trigger:** fleet marker `layout=3` or malformed; device on `/ROCKNIX/Saves` opens a transfer page or boots with `--needs-step`=0.

**Actual:** `UI26-future-script.log:3` / `UI26-malformed-script.log:3` → `>>> why COULDN'T FIND YOUR CLOUD FOLDER`; `UI26-*-interface.log` → `CHECKING YOUR CLOUD exited 4`. The script's own sentence ("…layout this version can't read… Check for a newer system version") is discarded. The French string added for it (`es-diff.patch:523-524`) can only be reached via `--apply`.

**Required:** I356-L76 ("showing a supported outcome"), I363-L76 ("a refused join ending with its why"). A folder that is *found* and refused for version is reported as *not found*; the correct player action (update) is not conveyed. Same collision maps conf-unreadable (2) to "SOMETHING WENT WRONG" instead of "YOUR CLOUD SYNC SETTINGS COULDN'T BE READ", and record failures (5) to "YOUR CLOUD STOPPED ANSWERING" (see B-06).

**Falsifying observation:** a UI26 frame/log carrying "YOUR CLOUD FOLDER COULDN'T BE READ".

---

## B-04 — Startup saves sync runs networked join/state/follow (pointer-writing) before transfer, contradicting I363-L73 / I353-L33; any failure of that step suppresses the startup restore

**Severity:** High — contradiction between criterion text and shipped ES composite, with functional consequence; the cited PASS lines do not exercise the composite.

**Location:** `es-diff.patch:205-209` (main.cpp startup worker: `cloud_migrate_layout --needs-step`; if 0 → `timeout 30 /usr/bin/cloud_scan --folder; … || exit "$_s"`; `elif != 1 → exit`) placed before `>>> doing receive` / `cloud_restore … --saves-only --automatic` (lines 210-211). `cloud_scan:153-185` `read_folder` runs `--join` (writes SAVES/SETTINGS/CONTENT pointers, `cloud_migrate_layout:922-924`), `--state` (probe + features + marker reads + listings), and `--follow` (writes pointers, `:878-884`).

**Actual vs required:** I363-L73 requires "No sync runs networked layout join/state/follow/migration preparation before transfer" (only local `--superseded` and the single parent probe permitted); I353-L33 requires the folder "settled by the cloud folder step … never by a sync." The startup sync does exactly that for every boot of a device on a superseded default that answered NOT NOW (I363-L79 says NOT NOW recurs). The observation for I363-L73 ("Fresh scripts.log:1461-1462 records both no-folder-check PASS lines") covers `cloud_backup`/`cloud_restore` only; nothing in the packet executes the ES composite against that criterion.

**Consequences observed from source:**
1. Recurring networked probing at boot (lsd probe, backend features, `rclone cat` marker, 2–6 listings, run twice: once in the worker, again on the CHECKING YOUR CLOUD step page) — I377-L25 states "No extra recurring network probe is introduced without #364's timing acceptance being reverified"; the acceptance (I363-L74, I429-L30) measured the exit sync only.
2. Any non-zero `cloud_scan --folder` (4 future marker, 5 record/cloud, 124 timeout, 2 conf) exits the worker before the receive: no startup saves restore that boot, with a reason mis-mapped per B-03.
3. Pointer writes occur inside the sync with no lock and no all-or-none write (B-07).

**Falsifying observation:** an owner decision re-wording I363-L73/I353-L33 to permit boot-only join/follow inside the worker *and* a boot-path timing/time-to-play measurement for the NOT-NOW population; or a trace showing `cloud_restore` still runs after a non-zero `cloud_scan --folder`.

---

## B-05 — A sibling's conflict-loser shelf under a superseded default makes every current-layout device read `migration-pending` and nags "YOUR CLOUD FOLDER MOVE DIDN'T FINISH"

**Severity:** Medium — observed code defect (source), falsifiable by a host/guest case.

**Location:** `cloud_migrate_layout:819-828` (`layout_state`: for saves=NEW && backups=NEW, `has_entries "${remote}${earlier}-replaced/"` over `/GAMES`, `/ROCKNIX/Saves` → `state=migration-pending`); `:1239-1244` (`migration_step_1` adopts the shelf as `old_replaced` and plans "discarded"); `es-diff.patch:138-155` (ES offers TRY AGAIN / NOT NOW, no KEEP).

**Trigger:** Device A migrated to `/pixelelated`. Device B chose KEEP USING `/ROCKNIX` (I353-L32: "for good") or is an un-upgraded RC2 device on `/GAMES`; B's `cloud_backup` sets aside a conflict loser at `/ROCKNIX/Saves-replaced/<stamp>/…` (D-CLOUD-165 shelf, `<saves>-replaced`).

**Actual:** A's every transfer-page open reads `STATE=migration-pending` and shows "YOUR CLOUD FOLDER MOVE DIDN'T FINISH. TRY AGAIN? FILES ALREADY MOVED WILL BE KEPT." — false for A. TRY AGAIN relocates B's live shelf to `/pixelelated/Saves-replaced` and deletes it from `/ROCKNIX`. NOT NOW re-asks on every open while B exists. Nothing distinguishes "my unfinished run101/RC2 move" from "a kept sibling's active shelf".

**Required:** I391-L22/23 recovery is meant for *this device's* interrupted predecessor state; I353-L32's KEEP USING coexistence; I380-L24 ("without silently replacing a player-selected folder" — here a sibling's folder is moved on A's press).

**Falsifying observation:** `cloud_migrate_layout --state` on a current guest, with a sibling-written `/ROCKNIX/Saves-replaced/<stamp>/x.srm` present, printing `STATE=current`.

---

## B-06 — A migration record whose remote name/fingerprint no longer matches is unrecoverable from the UI and blocks the startup restore every boot

**Severity:** Medium — observed code defect (source).

**Location:** `cloud_migrate_layout:1056-1072` (`migration_record_load` → `return 5` on `.remote`/`.fingerprint` mismatch, message discarded upstream), `:795-798` (`layout_state` returns that 5 before printing any fact), `:1509-1512` (`--needs-step` → 0 whenever the record file exists, no validation), `:1185-1191` (`--join/--follow` → 3; `--settle/--keep/--write-marker` → 5), `es-diff.patch:205-209` (boot composite exits on 5), `cloud_scan:96` (5 → "YOUR CLOUD STOPPED ANSWERING").

**Trigger:** a move was interrupted (record at stage ≠ complete); the player then re-creates/renames the rclone remote or re-runs setup (plausible after "Try again when you're online").

**Actual:** every boot: `--needs-step`=0 → `cloud_scan --folder` → `--state` → 5 → startup card "COULDN'T FINISH – YOUR CLOUD STOPPED ANSWERING", no saves restore; the folder step page fails before any dialog; opening scans fail the same way; `--settle`/`--keep` refuse. No UI path removes `/storage/.config/cloud-layout-migration.json`.

**Required:** I391-L23 ("Recovery remains interruptible and repeatable"), I356-L77 ("retry … completes"); a safe refusal must still leave a supported way out and state its reason ("The previous cloud move couldn't be read safely" is never shown).

**Falsifying observation:** a guest proof with a stale record and changed remote name reaching a dialog that lets the player discard/retry.

---

## B-07 — `layout_join`/`layout_follow`/`layout_settle` write three pointers sequentially, not all-or-none

**Severity:** Low — observed (source).

**Location:** `cloud_migrate_layout:922-924, 878-884, 948-952` (three `set_pointer … || return 1`); contrast `cloud_setup:64-107` `conf_set` (one temp, one rename, all keys or none).

**Trigger:** write failure after the first `set_pointer` (read-only/full `/storage`, concurrent rewrite).

**Actual:** SAVES_REMOTE re-pointed, SETTINGS/CONTENT not — a split layout the next boot/scan keeps; `cloud_scan` reports rc 1 → "SOMETHING WENT WRONG" (B-03). I380-L22/L24 state-table consistency assumes the three move together.

**Falsifying observation:** a host case injecting failure on the second write and showing the first reverted or all three landing.

---

## B-08 — Owner approval is cited only for the thirteen 2026-10-01 strings; later-added interface strings have no cited approval

**Severity:** Medium — unexecuted exact criterion / evidence gap (not a code defect).

**Location:** I354-L69, I353-L35 ("Every string … approved by the maintainer before the build"); packet observation cites only D-CLOUD-164 (`docs/decision-register.md:549`, thirteen strings). New strings in `es-diff.patch:142, 146, 164, 511-524` (TRY AGAIN dialog, "WHAT MOVED IS IN THE NEW FOLDER…", "YOUR CLOUD FOLDER COULDN'T BE READ", MANUAL UPDATES + sentence, "ENABLE pixelelated SCREENSHOT"); script sentences `cloud_migrate_layout:571, 640, 785, 800, 1005, 1025, 1070, 1081, 1189`, `cloud_setup:749`, `cloud_content_restore:1298`; and the 640 px live-line fallback "CHECKING WHAT YOUR CLOUD HAS FOR THIS DEVICE..." (I349-L44/I350-L36) which differs from the approved sentence.

**Actual vs required:** `tools/vocabulary-check` passing (164/0) establishes vocabulary conformance, not owner approval "before the build". D-CLOUD-164 allows later fine-tuning but does not pre-approve new strings.

**Falsifying observation:** a register row or #354/#383 owner comment approving the post-10-01 strings (and the fallback clause).

---

## B-09 — `cloud_scan`'s private `conf_get` diverges from the shared grammar (D-CLOUD-149)

**Severity:** Low — observed (source).

**Location:** `cloud_scan:60-72` vs `cloud_setup:131-178` / `cloud_migrate_layout:160-207`.

**Trigger:** `export SETTINGS_REMOTE="/Mine/Backups"` or an indented key, or a value with a control character.

**Actual:** cloud_scan reads the key as *absent* (empty `settings_remote` → archives listed at the remote root, `cloud_scan:211-217`); the shared readers return 2 (unreadable) and the scripts refuse. Two readers disagree on one file.

**Falsifying observation:** a host case where `cloud_scan` emits `>>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ` for the `export` form.

---

## B-10 — I363-L75 text vs `--needs-step` behaviour

**Severity:** Low — criterion/code mismatch.

**Location:** `cloud_migrate_layout:1507-1526`: returns 0 for a *current* folder with historical content (1515-1521) and for any record file (1509-1512, unvalidated). I363-L75 states "1 for the current folder"; the host cases cited (scripts.log 1453-1460) are "earlier defaults 0, current/custom/kept/no-remote 1" and do not name the new 0-returning current-layout sub-cases. Interacts with B-06.

**Falsifying observation:** updated criterion text or named PASS lines for current+historical-content → 0 and record-present → 0.

---

## B-11 — Inactivity guard covers copy/sync only; listings and mkdir remain on rclone's own retry bound

**Severity:** Low — scope question; cannot fully judge.

**Location:** `cloud_content_transfer` applied at `cloud_content_backup:708,721`, `cloud_content_restore:736,1026,1547,1560`; unguarded: `cloud_content_backup:702` (`rclone mkdir`), `cloud_content_restore:1245,1260` (`lsf -R` scan), `:433,437,408,412` (`exists_remote`/`resolve_src`), `:1454`.

**Actual vs required:** I401-L34 says "Content network operations stop after bounded inactivity across provider SDK retries". The S3 SDK retry pattern that produced success-after-outage (I401-L33) is a client-side behaviour that can also apply to list calls; the packet's scan evidence (I401-L35) shows link-loss recovery, not a stalled-listing bound. If listings under `--low-level-retries 3 --timeout 30s` cannot exceed the inactivity ceiling on the shipped rclone/S3 build, this is moot.

**Falsifying observation:** a scan or mkdir stalled by injected SDK-level retries terminating within the documented bound.

---

## B-12 — UI frame evidence reused from replacement 09 under the pre-10 compositor path

**Severity:** Low — evidence traceability gap (not a new failure).

**Location:** I349-L29/L42/L44, I350-L24/25/35, I352-L35/L45, I353-L31/33/34, I363-L78–81, I364-L34 all cite guest-11 (replacement 09) frames; evidence domain states 09→10 changed rendering, and I447-L74 records reproducible stale/partial scanout on the software profile before 10. ES/script bytes are unchanged (byte-identity rule satisfied), but the capture path is not. The frozen-14 defaults suite (I354-L68: 16 walks/78 frames, 34 claimed regions) is not mapped to these criteria in the packet.

**Falsifying observation:** a frame-diff manifest listing which of the 78 frozen-14 frames cover the cloud-epic rows/dialogs, or a statement that guest-11 ran on virgl.

---

## B-13 — Open infrastructure/evidence items the packet itself reports missing

**Severity:** Low — evidence gaps (confirming, not new).

- I344-L213: bot token repositories×permissions×expiry inventory and tested mail reminder — not located (packet observation agrees).
- I344-L229/L231/L256: brand/secret/localisation sweeps last run on 09; 10→14 changed proxy sources (patch 018 adds a brand predicate, `raofflineproxy-ctl` note) — renewed classification on 14 not supplied (acknowledged in the primary's own observation).
- I351-L62: French for `cloud_oauth` phone-page strings (`cloud_oauth:1015-1017`) and `cloud-signin-window.c:438-439` is absent; whether D-UI-051 applies to browser-delivered pages is unresolved in the packet.

---

## B-14 — Chooser can list a folder `--set-content-remote` refuses

**Severity:** Low — observed (source), likely pre-existing but in P1 (#352) scope.

**Location:** `cloud_setup:581-585` refuses any `[[:space:]]` and any `..` substring; `cloud_scan:243` lists all root dirs for the chooser; the saves-folder validator (`cloud_setup:298-456`) and both `conf_get` readers accept spaces inside double quotes.

**Trigger:** root folder "My Games" or "Games..old" chosen in CHOOSE A CLOUD FOLDER.

**Actual:** "That folder name has characters your cloud sync settings can't hold." — inconsistent with the saves path and the reader; the chooser offers a folder that cannot be chosen.

**Falsifying observation:** a guest pick of a space-named root folder succeeding.

---

## Reviewed without finding a defect (for coverage)

- `SystemConf::recordLastGood` (`es-diff.patch:404-418`) reacquires the lock and compares the complete choice; tests at `:244-285` match the described race and LockBusy cases. (See "cannot judge" on `LoadedConfig::record`.)
- `prepare_settings_temp` (`distribution-product-diff.patch:759-779`): mode = AND of existing sources ∧ ~umask, applied while empty; callers gate on it; `chksysconfig put` intersects src/dst.
- `cloud_backup:2185-2200, 2211-2228` and `cloud_restore:3223-3261, 3286-3320`: three-way presence; unknown (2) never yields a create offer.
- `rasteratops-settings-archive:8-43`: 3/4 → next candidate; other rc → propagated; shared by scan and restore.
- `cloud_content_transfer`: high-water marks across five counters, fallback never counts as progress, TERM→KILL escalation, 124 mapped in both `why_for`s.
- `relocate`/`merge_into`: list → copy → verify → pointer → delete; merge shelves differing files before `--update`.
- Mesa `rtasm` `atexit(destroy_heap)` and virgl empty-table release; SDL `SDL_DelVideoDisplay` mode release; ES udev `unref` paths; `malloc_trim` placement.
- `sway-generic-x64` selector: explicit overrides respected; non-virtio/multi-card/malformed feature strings leave selection alone.
- `rocknix-update` shim and `ApiSystem::canUpdate` for pixelelated; `rocknix-report-stats` inert, timer masked.

## What I cannot judge from the packet

- `GuiMenu.cpp:5440-5475`, `cloudFolderStepAtBoot`, and ES `whyForCode` mapping (not in packet) — whether the step page re-runs `cloud_scan --folder` (asserted from I363-L79's frame order) and how rc 2/4/5 render on the card.
- `Utils::AtomicFile::LoadedConfig::record` semantics in `recordLastGood`'s guard (`es-diff.patch:415-417`).
- Whether the shipped `timeout` kills the process group (orphaned `cloud_migrate_layout --join` writing pointers after the worker moved on).
- Whether `WLR_DRM_DEVICES` is set in the GENERIC_X64 sway unit (the wrapper returns early otherwise); QA18 renderer records say Pixman was selected, so presumably yes.
- UI26 marker *bytes* before/after (only pointer files are in the packet).
- Whether rclone's `--progress` on a non-TTY emits the stats block the guard parses on the shipped build (I401 controls say yes; not verifiable here).
- Dropbox trust page (owner-waived) and all P5 site/release-note/device items.