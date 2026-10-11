# Independent review — M7 #535–539 (Anthropic seat)

Scope honoured: frozen bytes per `inputs/source-manifest.json`; guest hashes in `checks/target-original/installed.json` match the manifest for `cloud_connections.py`, `cloud_remote`, `cloud_setup`, `cloud_scan`, `cloud_content_restore`; `QA/browser/installed.json` binds `cloud_oauth` (0d4012…). Everything below is marked either **runtime proof** (a receipt in the packet) or **source lead** (my reading; no tool run).

---

## 1. Own findings

### O-1 — OAuth sign-in may now be refused by the new `State` check (source lead, **unverified; High if confirmed**)

- **Where:** `cloud_connections.py:160-166` raises `Refused('This provider needs additional setup…')` whenever `rclone config create/update … --non-interactive` prints a JSON blob with `State`. The OAuth call site passes only `[("token", self.token)]` (`cloud_oauth:544`).
- **Why it matters:** every OAuth backend's `Config()` goes through rclone's `oauthutil` state machine, whose first step, when a `token` is already present, is the confirm question `config_refresh_token` ("Already have a token - refresh?"). Nothing in the delta pre-answers it (`config_refresh_token=false`). The deleted code (diff hunk at old `cloud_oauth:530-600`) ignored stdout, relied on the remote already being written, and verified with `lsd` — so a pending question never mattered. The new path refuses on it and rolls back.
- **Why no existing guard/receipt covers it:** every OAuth receipt in the packet runs against the *authorize fixture* (`QA/receipts/pix537-oauth-lifetime.log`, `cloud_connections_fixture.py` replaces `c.run` and never emits `State`); the only real-rclone transaction tests use `alias` (`tools/cloud-connections-test:30`), which has no `Config()` state machine. The guest `OAuthOwnership` tests use `alias` too (`cloud-connections-test:196`).
- **Decider (credential-free, one command on the guest):** `rclone --config /tmp/p.conf config create probe dropbox token='{"access_token":"x"}' --non-interactive --obscure`; if stdout contains `"State"`, every on-device Dropbox/Drive/OneDrive sign-in now ends in "THE SIGN-IN DID NOT COMPLETE. TRY AGAIN" with the module logging "could not be saved". Fix if confirmed: append `("config_refresh_token","false")` for oauth-tier saves at `cloud_oauth:544` (and consider `config_is_local=false`), or whitelist that one question in `save()`.
- I cannot confirm rclone's non-interactive handling from here; I am flagging a strict-mode regression that no receipt exercises, not a proven failure.

### O-2 — ES-side scan run ids are not invalidated on connection change (source lead, **Medium**, part of the F-01 repair)

- `sCloudScanRun` / `sCloudContentScanRun` are cleared only in the folder editor (`GuiMenu.cpp:6568-6569`). `cloudConnectionChange` (`GuiMenu.cpp:7924-7938`) and the OAuth success path (`GuiMenu.cpp:7812-7816`) never touch them. Even after `cloud_scan context_id` is repaired, a stale in-memory run id plus a valid-looking stamp is the same seam from the other side. The consumer code (GuiCloudTransfer scan reuse) is not in the packet — see coverage limits.

### O-3 — Stale player-facing text under explicit selection (source lead, **Low**)

- `GuiMenu.cpp:6825` still shows "NOTE: CLOUD SYNC USES THE FIRST REMOTE IN ALPHABETICAL ORDER." in the SSH add-remote step. With a sidecar present this is false (D-CLOUD-184). The done step (`GuiMenu.cpp:7044-7056`) handles the state correctly, so the harm is a wrong instruction, not a wrong action.

### O-4 — Dangling selection blocks adding a connection with a generic message (source lead, **Low**)

- `cloud_connections.py:146` calls `active(config)`, which raises when `active-connection` names a section no longer present (`:59-60`, only reachable via external `rclone config` rename/delete). `save()` therefore refuses *adding* a new connection; `cloudConnectionError` (`GuiMenu.cpp:7125-7140`) has no mapping for "selected connection is missing", so the player sees "COULD NOT BE READ OR SAVED". Recovery exists (`select()` at `:203-209` does not call `active()`), but nothing tells the player that.

### O-5 — Apply-time name recheck refuses silently and leaves the plan unspent (source lead, **Low**)

- `cloud_content_restore:857` `return 1` emits no `>>> why` and no stamp, unlike the equivalent guard at `:1484-1488`; the plan is removed only at `:895`, so a refused apply leaves `content-match-plan` on disk for a later CLI `--match --apply`. The GUI always re-previews (`GuiMenu.cpp:5290-5388`), so this is CLI-only.

### O-6 — "Isn't set up yet" wording for a tombstoned/unselected state (source lead, **Low**)

- `cloud_remote:309-314` exits 1 silently for the empty tombstone; `cloud_scan:140-143`, `cloud_content_restore:235-238`, `cloud_content_backup:198-202`, `cloud_backup:2420-2424` then say "Your cloud storage isn't set up yet" while saved connections exist. The connections page says the right thing ("NO CONNECTION IN USE", `GuiMenu.cpp:8002-8003`); the transfer surfaces do not.

### O-7 — `--check` does not shell-quote the remote (source lead, **Low**)

- `cloudSetupRunCheck` builds `cmd += " " + remote` (`GuiMenu.cpp:6619-6621`); `cloudConnectionDetails` passes `name + ":"` (`:7947`). `save()` accepts names with spaces (`cloud_connections.py:134` rejects only `:[]\r\n\t` and leading `-`); such a name makes CHECK CONNECTION report "COULDN'T REACH" against the wrong argument. Misreport only.

### O-8 — Popup return depends on the provider closing it (source lead, **Low/UX**)

- `on_auth_close` (`cloud-signin-window.c:866-879`) is the only path back to the parent view; a popup that posts its result but does not `window.close()` leaves B/Backspace as in-popup history only (`:692-698`) and Escape as "end the sign-in" (`:544-547`). Provider-dependent; not provable from the synthetic provider receipt (`QA/browser/result.json` `popup_return: true` covers the self-closing case only).

### O-9 — UI-thread process spawn on every return-to-top (source lead, **Low/perf**)

- `CloudConnectionsPage::topWindow` (`GuiMenu.cpp:5586-5594`) runs `cloud_remote list` synchronously on the UI thread each time a child closes (Python start; `rclone config dump` for encrypted configs via `cloud_connections.py:41`). Lifetime handling (`mAlive`, `peekGui()==this`) is correct; the cost is jank on a handheld that VM frames will not show.

### O-10 — Minor: CLEAR semantics on the WI-FI KEY prompt (source lead, **Low**, within #538's accepted scope)

- `GuiTextEditPopup.cpp:34` CLEAR = `okCallback("")` + close; on the key prompt (`GuiWifi.cpp:264-272`) that submits an empty key, i.e. `wifictl connect <ssid> '' <country>` → `PSK=""` (`wifictl:55`, now correctly not borrowing `wifi.key`) → passwordless attempt (`wifictl:149-158`). AskKey rows have no same-SSID profile (`WifiText.cpp:222-231`, `:58-65`), so the `connection delete` at `wifictl:152` deletes nothing; the result is just a failed connect. Noting because the relabel makes "submit empty" read as "erase the draft".

### O-11 — Minor: `holder.end()` join vs. staged-save worst case (source lead, **Low**)

- `cloud_oauth:2031-2033` joins the collector for 45 s; `cloud_connections.run` is bounded at 40 s per call (`:124`) and `save()` makes two (`:159`, `:167`). The `lsd` carries `--contimeout 10s --timeout 20s` so the realistic ceiling is ~35 s, but a process exit mid-`save()` leaves a `.connection-*` staging dir holding a token under `/storage/.config/rclone/` with no sweep; backups exclude the directory (`backuptool:723-726`).

Checked and found sound (no finding): OAuth lock order (connection lock then `session.lock`, `cloud_connections.py:136` → `cloud_oauth:533`); rollback on publish failure (`cloud_connections.py:190-199`); `atomic()` mode via `mkstemp` (`:67`); `restore_selection` only undoes its own write (`:84-96`); `wifictl:91-110` security parsing with escaped SSIDs and fail-closed mixed/absent; `connect_open_wifi` refusing any same-SSID profile including renamed (`:118-124`); back-key script guards for editables/modifiers/`defaultPrevented` (`cloud-signin-window.c:692-698`); single-popup invariant (`:898`); stale-probe filter (`:391`); `pushMove`/`send` sealing (`cloud_oauth:1032-1044`, `:1185-1200`); `DEVICEONLYDIRS` restore skip on both formats (`backuptool:1539-1542`, `:1648`); `cloudShowFolderSelection::stillSelected` refusing a changed configId before a seed starts (`GuiMenu.cpp:6998-7005`).

---

## 2. Refutation / re-grade of the frozen primary findings

### F-01 — scan identity omits the active connection → **High, survives**

- **Source:** `cloud_scan:171-189` fingerprints `cloud_sync.conf`, `rclone.conf`, rules, `content-systems`, two `es_systems.cfg`; not `/storage/.config/rclone/active-connection`. `prepare()` reads the selection at `:139`. `--stamp-valid` (`:231-244`) and `write_completion` (`:216-227`) compare only that id.
- **Runtime proof:** `checks/target-original/scan.json` — `alpha`/`beta` `--context` stdout identical (`de8d13ff…`), `switch` `OK=beta`, `valid_before` and `valid_after` both rc 0, on a guest whose `cloud_scan` hash matches the manifest.
- **Refutation attempts that fail:** `cloud_setup validation_context` (`:556-562`) does hash the sidecar and REMOTE, but `cloud_scan` never consumes it (`:290-292`, `:347` call `cloud_setup` for *results*, not identity). Credential edits and removals change `rclone.conf` and so invalidate; only "select among already-saved connections" slips through — exactly the new feature's main action.
- **What I would add:** unlike F-02/F-03 this needs no concurrency — scan, back, USE THIS CONNECTION, back, open a transfer page is a sequential in-UI walk, *if* ES reuses stamps (consumer code not in packet; `sCloudScanRun` handling at `GuiMenu.cpp:6568-6569` indicates it does). Repair must cover three sites: add the sidecar to the `context_id` list (its absent/present/empty shapes are already distinct at `:179-185`, so the in-flight `write_completion` check comes for free), clear the ES run ids on connection change and OAuth publication (O-2), and decide what a tombstone (`''`) means to the scan (today `prepare()` exits 1 "NOT SET UP YET", `:140-143`).

### F-02 — seed writer outside the shared lock → **re-graded to Medium**; AC-537-04 FAIL overstated

- **What is proven:** `cloud_setup --seed-folders` (`:791-875`) takes no lock (no `take_cloud_lock` exists in `cloud_setup`); `seed.json` shows `select beta` rc 0 while the seed was blocked inside `mkdir`. That proves the exclusion claim in `cloud_connections.py:7` ("All writers share the transfer lock") is false for this writer.
- **What is not proven, and does not follow:** `REMOTE` is resolved once into a string at `:793`; every later command uses `"${REMOTE}${d}"` (`:809`, `:826`, `:835`, `:866`). A `select` cannot redirect the seed — it finished on alpha, the account the player named when pressing CREATE FOLDERS. Misdirection needs `update`/`--replace` publication (new credentials under the *same* name) or `remove` mid-run; the probe exercised neither. `remove` is transactional (`cloud_connections.py:212-243`): the seed's later `rclone` calls fail on a missing section and exit 5 with a why — the *job* fails, the configuration never becomes invalid. So AC-537-04's "cannot race an active cloud job into an invalid configuration" reads PARTIAL, not FAIL.
- **Harm bound:** the seed is create-only — `mkdir`, `copyto --ignore-existing` after a listing (`:826-835`), and the one overwrite primitive `rcat .layout` (`:421`), which only runs for the default `pixelelated/Saves` namespace (`:372-387`). No deletion path exists.
- **Reachability bound:** `GuiCloudTransfer` is sat in (D-UI-078; `GuiMenu.cpp:5390-5400`) and an OAuth serve is cancelled when its page is left (`cloudOAuthOwnSession`, `GuiMenu.cpp:6460-6470`), so an in-product concurrent writer during a seed is not reachable; the race needs SSH or a future UI change. Still worth fixing cheaply (flock the same path before `:793`, body with fd closed as `cloud_content_backup:678-684` does) because the busy refusal is the project's stated invariant and the auto-continue check after a seed reports against the *current* selection (`GuiMenu.cpp:7029` → `cloudFolderContext()`).

### F-03 — destructive preview lacks account binding → **High, survives (trigger narrowed)**

- **Source:** plan header is `plan <epoch>` plus `sys|verb|files|bytes` (`cloud_content_restore:799-804`); apply binds to verb and `files ≤` only (`:955-965`); `REMOTENAME` is this process's (`:234`) and the lock-time recheck (`:856-857`) compares it to itself, not to the preview's.
- **Runtime proof:** `match.json` — preview on alpha `qa537audit|sync|1|14`, `select beta` OK, apply rc 0, "Deleted: 1 (files) … 14 B", 13 B transferred, `local_after` shows `beta.rom` present and `local.rom` gone, `save.srm` intact. The verb/count guard passed by coincidence (one file each side), which is the ordinary case for a system folder that exists in both accounts.
- **Refutation attempts that fail:** `--max-delete` caps *how many*, not *from which account's plan*; `cloud_root_populated` (`:864`) only proves the new account is non-empty; the GUI's immediate preview→YES→apply (`GuiMenu.cpp:5290-5386`) leaves only a modal between them, so exposure in-UI needs an out-of-band writer during the confirmation — narrower than "a different account selected since the earlier preview" implies, but the plan is the consent artifact and its binding is incomplete by construction, and the outcome is irreversible (D-CLOUD-023).
- **Repair shape I concur with, extended:** write a configuration digest into the plan header (REMOTE + sha256 of `rclone.conf` + sha256/absence of `active-connection`, i.e. what `validation_context` already computes), compare it under the lock at `:856`, reject old two-field headers, and emit a `>>> why` there (O-5). Apply the same digest comparison to the name-only rechecks at `cloud_content_backup:687` and `cloud_content_restore:1484`, so a same-name credential replacement (the retrospective's adjacent FIX-NOW) is also refused.

---

## 3. Coverage limits (specific)

1. **No real-rclone OAuth-type `config create/update` receipt** anywhere in the packet; O-1 cannot be closed without the guest probe above.
2. **Consumer side of F-01 not supplied:** the GuiCloudTransfer/scan-page code that reads `--stamp-valid` and `sCloudScanRun`; F-01's in-UI consequence rests on the primary's statement that ES reuses stamps.
3. **Saves scripts' lock placement not visible:** `cloud_backup:2419` and `cloud_restore:2219` resolve `first_remote` in `main()`; `take_cloud_lock` call sites are outside the supplied ranges, and neither script has the post-lock recheck the content scripts have (`cloud_content_backup:687`, `cloud_content_restore:1484`). The retrospective's "SAFE-AS-TESTED/code-read" for saves backup/restore is unverified here.
4. **Not in packet:** `cloud_content_transfer` (`bounded_content_rclone`), `cloud_folder_validate`, `CloudText`, `ApiSystem::enableWifi/launchCloudSignIn`, `GuiSettings::close`, the es11 binary binding and the frame `binding.json` files referenced by `QA/editor/review.json`; guest hashes for `wifictl`, `backuptool`, `cloud_oauth` serve on the guest (only browser/oauth in `QA/browser/installed.json`).
5. **Reviewed-frame receipts only;** no image bytes. `checks/gate-pkgcheck.log` carries no verdict line and is not proof.
6. **Reproductions are CLI-actor races** (F-02, F-03); no receipt demonstrates an in-UI trigger, which is the basis of my narrowing.
7. **Synthetic providers only:** real Wi-Fi radio, provider popup behaviour (O-8), bucket directory-marker remotes, and the #536 UA question remain untested by design.
8. `launcher-result.json` records submission, not completion (`submission_is_not_completion: true`); the result files themselves are the evidence I used.

---

## 4. Verdict

I agree the delta is **not ready to integrate**. F-01 and F-03 stand as High (F-01 is the only one a lone player can walk into sequentially; F-03 is the only one that deletes). F-02 is a real invariant gap but Medium on harm and reachability, and AC-537-04 should read PARTIAL. Before any remediation round claims the OAuth path, run the one-line real-rclone probe for O-1 — if it emits `State`, it outranks all three primary findings.