# Refutation pass — M7 Milestone audit #590 (second serial call)

**Standing.** I read the sealed base, my verified blind response (SHA256 `98482d2f…ad46` as stated), the readback, G-01, the counter-source, the d4af delta, and the embedded supplemental originals. Embedded originals I treat as data: Dolphin baseline and private-candidate stderr/fields, the metadata result JSON, the Steam 14-case readback. The d4af image, composition, and installed-Dolphin readbacks are primary-attested summaries (hashes, counts); I did not see those originals and grade them as attested, not independently verified. I have no frame pixels. Nothing below is an executed test by me; everything is source readback plus reading of others' original records.

---

## 1. Additional findings

### R-01 — Medium — Disabling or logging out of RetroAchievements in ES leaves the previous `RetroAchievements.ini` active for Dolphin; patch 018 makes this live on the default frontend

**Trigger/effect.** `cheevos_dolphin.sh` writes the INI only when RA is enabled *and* a token exists; both negative branches `exit 1` before the write (`cheevos_dolphin.sh:21–28` enabled≠1 → exit 1; `:30–34` empty token → exit 1; the sole write is `:91–103`). The launcher calls it unconditionally and continues regardless of its exit (`start_dolphin_gc.sh` hunk `@@ -450,19 +414,17 @@`, `# Retroachievements` → `/usr/bin/cheevos_dolphin.sh`; same in the Wii script). Sequence: enable RA + login in ES, launch a GC game once (INI written with `Enabled = True`, `ApiToken`, `HardcoreEnabled`, possibly `HostUrl = 127.0.0.1:8080`); later disable RA or log out in ES; launch again → INI untouched → with d4af patch 018, `AchievementManager::Init` reads `RA_ENABLED` true (`AchievementManager.cpp:67`), `HasAPIToken()` true (`:94–95`, `:151–154`) and logs in with the stale token; stale `HardcoreEnabled = True` also keeps hardcore restrictions. Local ES logout does not revoke the RA token server-side, so a still-valid token authenticates. On frozen fac608 this was dormant for NoGUI (no Init) and only affected the Qt core.

**Why it is not already covered.** The AC-101 description records the disabled/missing-token cases as "expected early exit 1" with "unchanged input settings"; no pre-existing-INI precondition is described. The d4af `installed-disabled` case authored its INI directly in a private `-u` user dir, not through the launcher.

**Refutation attempted.** The full `start_dolphin_*.sh` is not embedded; if it deletes or rewrites the INI elsewhere this is false. Bounded check: `rg -n 'RetroAchievements.ini' projects/ROCKNIX/packages/emulators/standalone/dolphin-sa/` — a single-file grep, no matrix. Also false if the launcher were changed to pass RA flags on the command line (it is not; `-v`, `-a`, `-u`, `-e` only per the fields).

**Smallest correction/check.** In both early-exit branches write the INI with `Enabled = False` (fields otherwise blank) before `exit 1`, or `rm -f` it — writing is deterministic. One added routing-fixture row: pre-existing `Enabled = True`/token INI + `global.retroachievements=0` → assert resulting `Enabled = False` and no token; a sibling row for logged-out. Attach to the F-002 remediation punch list before RC; frozen verdicts unchanged.

### R-02 — Low (lead) — Client installer: a single 360 s alarm must cover 300 s of explicit stage bounds plus two unbounded full-payload hashes

`Install Steam.sh:2338` `signal.alarm(360 …)` once, never reset. Explicit bounds: manifest 30 s (`:1954`), archive 180 s (`:1962`), decode 90 s (`:2030`) = 300 s. Unbounded-by-stage work: `digest_file(archive)` (`:1965`, ≤128 MiB), `tree(payload)` (`:2080`) and again `tree(root/CLIENT)` in `commit()` (`:2174`), each hashing up to 384 MiB (`:1194`), plus fsyncs. If the alarm fires after a near-maximal download, `interrupted` (`:2327`) → cleanup → retry re-downloads from scratch (no resume). Arithmetic only; no observation; realistic only on slow storage with a slow link. Falsifier: real stage timings well under budget — but measuring that is device-shaped, so the proportionate resolution is a source decision (reset the alarm per phase, or make the budget the sum of stage bounds plus a hashing allowance) rather than a timing matrix.

### R-03 — Low (hygiene) — Runtime helper is the only embedded Python not run with `-I -S -B`

`Install Steam.sh:780` `python3 - …` after `source /etc/profile` (`:2718`), versus `/usr/bin/python3 -I -S -B -` at `:20, :253, :1168, :2377`. Only this helper is exposed to `PYTHONPATH`/site from the profile. Falsifier: no `PYTHON*` assignments in `/etc/profile`, `profile.d`, or `/storage/.profile` on the Steam device images — a grep.

### Observations (not findings)

- **Patch 018 ordering review.** Init is placed after the signal handlers and after the save-state-without-game early return (`MainNoGUI.cpp:289–293`), so no leak on that path; the guard is declared after `ui_common_guard` (`:284–287`) so Shutdown precedes `UICommon::Shutdown` on the failed-boot return; the normal path calls `Exit()` after `Core::Shutdown` and before `s_platform.reset()`. The private-candidate `failed-boot` stderr ends with `Achievement Manager shut down.` and exit 1; `disabled` logs no client; `enabled` logs one Init, one login request, one Shutdown. Consistent with the source; startup scope only.
- **Metadata "oversize" control exercised the declared-size refusal only** (curl exit 63 at 4 ms; the 10 s is `die`'s sleep). An undeclared-length oversize body is bounded by `--max-time 30` regardless, so the F-001 bound holds; just do not describe the 1 MiB cap as proven against chunked responses.
- **Supplemental `enabled` case did not reach game-load requests** (synthetic invalid token → login failed; one request total). It proves lifecycle and host interpretation, not post-login behavior.
- **Retained-update supplements upgrade from d6a87f (and earlier from d6a→fac), not from the last accepted baseline image.** The realistic player path (older accepted image → candidate) is not among embedded receipts; this matters most where launchers inspect retained state (F-03/R-01).

---

## 2. Refutation attempts — primary findings and G-01

### F-001 (Steam metadata bounds, Medium) — **not refuted; agree**
Attempt: look for an enclosing bound. The function at `Install Steam.sh:213` has none; callers `:2748/:2750` are bare; runemu's `setup` platform runs the script in the foreground with no timeout; `set_kill set "-9 steam FEX"` (`:2739`) targets steam/FEX names, so the global exit hotkey does not kill a stalled `curl` — the player is stranded until reboot. `.curlrc` cannot be relied on and is explicitly bypassed by the fix. Would be false if: the script ran under a supervisor with a deadline (none in packet), or curl defaults imposed one (they do not). Supplemental d4af: `-q` first, 10/30 s, 1 MiB; embedded result shows stall → curl 28 at 30.006 s, oversize → 63, normal → 0, both callers unchanged, old function bound but deliberately not run. Correction supported within that exact-function/installed-curl scope; frozen verdict stands.

### F-002 (NoGUI achievement lifecycle, High) — **not refuted; agree**
Attempt: find any Init in the NoGUI path. `MainNoGUI.cpp:1–347` (complete) has none; `UICommon.cpp:126–145` has none; only `MainWindow.cpp:270/349`. Original baseline stderr `AchievementManager.cpp:164 E … without achievement client initialized`, fields `enabled:true, initialized:0, requests:[]`. Residual falsifier: a Platform implementation (`PlatformWayland.cpp` etc., not embedded) calling Init — implausible for windowing code and contradicted by the headless run; a one-line `rg -n AchievementManager Source/Core/DolphinNoGUI/` closes it. High is earned: a milestone feature is inert on every device's default core. Supplemental: private relink hash equals the installed d4af binary (`5cb5dac…`), so the embedded candidate stderr is representative; startup/lifecycle only, no login success, award, gameplay or save. Frozen FAIL stands; see R-01 for the companion defect the repair activates.

### F-003 (immutable Sys root, Medium) — **not refuted; agree with the re-grade**
Attempt: show the compiled path is satisfied some other way. Compile argv has `-DDATA_DIR="/usr/share/dolphin-emu/"`; `FileUtil.cpp:762–790` resolves `…/sys/`; `-u` only moves user paths; recipe `package.mk:89–97` installs to `/usr/config/dolphin-emu` and never the datadir; Phase 3 observation: `share/dolphin-emu` absent. Candidate badge errors at `AchievementManager.cpp:892/902/912/922` in all three private cases confirm the reader side. Medium is earned because `LoadApprovedList()` (`:101–127`) and `Sys/GameSettings` (`GameConfigLoader.cpp:190–191`) share the root; hardcore-mode approved-modification filtering with an empty list is a functional effect, not only cosmetics (individual effects unmeasured, as the primary states). Supplemental alias `../../config/dolphin-emu` resolves correctly inside squashfs; the readback's six resource hashes and zero badge errors across three installed cases are attested, not seen by me. Residual: device-config files now also appear under "Sys" — no name collision with Sys consumers is visible, but it is a shared directory by construction.

### G-01 (whole-ES Wi-Fi worker shutdown, Low) — **not refuted; agree Low, narrow**
Facts check: `.detach()` (`GuiWifi.cpp:531`), deadline/kill/wait live in the worker (`WifiScanProcess.h:38–61, 135–175`), child in its own group (`:119–120`), no Wi-Fi join in `main.cpp:1317–1362` or `onExit:346–352`, `emustation.service:13 KillMode=process`, `essway.service` default cgroup kill, D-CLOUD-133 forbids SIGTERM teardown. Narrowing the primary did not state: the orphan is self-bounding. `wifictl list` is bounded by `wait_for_wifi` (≤5 iterations, `:76–93`), `nmcli -w 15` (`:104`), `sleep 1`, and D-Bus default timeouts on the remaining `nmcli` queries (`:108, :295, :308, :334`); `scanlist` adds one `-w 15` and `sleep 2` (`:537–539`); its only write to ES's pipe happens at the end and hits EPIPE/SIGPIPE once ES is gone. Worst case is a minute or two with an unresponsive NM, no storage writes, at most one overlapping rescan after `Restart=always`. Would be false if the child were spawned into ES's group or every unit used control-group kill. On the "additional constraint": under D-CLOUD-133 nothing in-process can run on SIGTERM/SIGKILL, and a custodian surviving ES death is disproportionate to the harm. Proportionate correction: a cooperative cancel flag checked in the 25 ms poll loop plus a bounded join at normal exit (≤2 s via `Child::finish`), and a documented residual for signal termination. No device test needed.

---

## 3. Primary grading of the blind items

| Item | Primary grade | My position | What would make the conclusion false |
|---|---|---|---|
| F-01 | confirmed → F-002 High | **Agree.** Earned: full source + original baseline stderr. | A Platform file calling Init (bounded grep closes). |
| F-02 | agree, narrowed | **Agree; re-grade Low.** NM 1.51.4 iwd `dbus_request_scan_cb:1240–1252` returns success when already scanning; refusals only while activating/unavailable (`:1286–1306`, `:2786`), yielding a distinct retryable message with prior rows retained. | Real-device refusal in DISCONNECTED/ACTIVATED state; a device using the wpa_supplicant backend (pin is iwd default). |
| F-03 | agree, narrowed | **Agree; re-grade Low.** No data loss; actionable two-path message (`dolphin-save-paths:25–26`). I do not accept "#581 excludes owner-data migration" as the justification — that sentence is about the owner's device — but refuse-over-migrate for the single-copy card is a defensible, documented (locator-only) product choice. AC-086's literal "ambiguous" wording does not cover it; record the policy or add the one `RENAME_NOREPLACE` row. | A policy decision to migrate; or an upgrade-from-accepted-baseline receipt showing refusal on a realistic device. |
| F-04 | agree, narrowed | **Agree;** coverage boundary, not a product defect; AC-080/084 PARTIAL is the right expression. | Lab-only validation of current real FEX/runtime/Proton assets against the embedded `validate()`/`unpack()`. |
| F-05 | disagree | **Accept the disagreement.** `WiaAndRvz.md:124,129,193` define partial last groups and size-0 groups only; `rvz_hash.cpp:271` computes the declared remainder. My short-group claim had no spec basis. | A conforming writer emitting short nonzero raw groups, or the Dolphin reader zero-filling them (not in packet). Residual: ES-reader controls (AC-095) are locator-only to me; embedded hashes are proxy-reader. |
| F-06 | disagree | **Accept.** `Settings.cpp:500–502` (both pins) omits default-equal values; the spaced default was never persisted by the predecessor. | Another writer (`es_settings` ExecStartPre, GUI chooser) emitting a spaced value — `rg CollectionSystemsAuto projects/` closes it. |
| F-07 | agree, narrowed | **Agree Low.** A bad stored country now fails read-only listing (`wifictl:89–92`); UI-set codes are valid. | A supported UI path producing an invalid code. |
| F-08 | agree, re-graded → F-003 Medium | **Agree.** Re-grade earned (shared root; approved-list effect). | None from packet. |
| F-09 | agree, narrowed | **Agree Low UX.** Preservation-first refusals are by design; specific Python stderr precedes the generic `die`. | — |
| F-10 | disagree, with the artifact | **Challenge: over-dismissal in scope.** The counter-source is the GENERIC_X64 image's `/etc/profile`, but Install Steam ships only on SM4450/SM8250/SM8550/SM8650/SM8750 (primary's own note; `emulators/package.mk:753–766`), whose `devices/<DEVICE>/filesystem/` overlays can carry their own `profile.d`. Lead stays open as Low. | `rg -n '^\s*(export\s+)?STEAM(_GAMES_ROOT)?=' projects/ distributions/` finding nothing (closes it) or something (confirms it). |
| F-11 | disagree | **Accept.** `GuiSettings::close:73–81` → finalizer; `cloudOAuthOwnSession:6468–6477` registered at `7673/7743/7861`; CANCEL → `page->close()` → cancel. | — |
| F-12(a) | agree, narrowed | **Agree.** Controller BUTTON_BACK accepted (`GuiWifi.cpp:379–384`); only the on-screen button row is controller-inert during scan. Cosmetic asymmetry. | — |
| F-12(b) | confirmed → G-01 Low | **Agree Low, narrowed** (self-bounding orphan; see §2). | — |
| F-12(c) | agree, narrowed | **Agree.** `locale/CMakeLists.txt:6–33` regenerates POT and compiles PO at build; repo hygiene only. | A build without gettext tools (`CMakeLists.txt:573–578` would then disable NLS, not ship stale catalogs). |
| F-12(d) | disagree (sanitizer artifact) | **Withdrawn.** Note the "structurally accurate" counter-source still shows a literal placeholder rather than `${screenscraper_shared_dev}`; I accept the stated explanation because it is trivially checkable (`rg -c screenscraper_shared_dev …/emulationstation/package.mk` ≥ 2). | Count = 1. |
| F-13 | agree, narrowed | **Agree Low.** Bounded, background, deliberate; cost unmeasured. | A measured first-frame regression on a large broken-RVZ library. |

No unearned confirmation found. One over-dismissal (F-10, scope of counter-source). Two of my blind severities were too high (F-02, F-03 → Low).

---

## 4. What cannot be judged from this packet

- Any frame-based criterion; I have no pixels (AC-003/010/043/049/067/069/072/076/088; the #591 frame-claim supplement is attested only).
- The d4af image, composition, retained-update and installed-Dolphin originals beyond the readback summaries and hashes; their claims are primary-attested within their stated scopes.
- Native gameplay/save/manual-state/exit-auto-state for RetroArch/Dolphin/Flycast (AC-064), and real RA login success, game-load requests, awards, proxy award queueing through Dolphin — the synthetic token never authenticated.
- Whether GENERIC_X64 and the device images run under `essway` (cgroup kill) or `emustation` (`KillMode=process`), and device `profile.d` contents (F-10, R-03).
- Real NetworkManager/iwd behavior on device radios (F-02, F-07), including nmcli exit codes for refusals.
- Installed curl's `--max-filesize` behavior on undeclared-length bodies; bounded by `--max-time` regardless.
- Proton asset naming/availability for both families against `FAMILIES` regexes and `tar_name == name + suffix` (`Install Steam.sh:2402–2403, :2584`); real FEX/runtime layouts (F-04).
- Whether `/storage/roms` is a mount point and `/storage/.config/fex-emu` a real directory on all device layouts.
- Whether ES consumes `/tmp/launch_error.log` on exit 250 and exports `LANGUAGE` to launchers.
- SM8250 DTS/wireplumber/UCM and kernel patches 0011/0016/0019 — upstream hardware foundation, outside this delta's recertification.
- Public documentation follow-up (AC-072), ABL/FEX corresponding-source custody (AC-018), and the composed native proof (AC-020) — tracked PARTIAL scope, not inferred either way.

**Net effect:** F-001/F-002/F-003 stand as frozen fac608 defects; supplemental d4af corrections are supported within the exact scopes embedded or attested (bounded function on installed curl; NoGUI startup lifecycle; Sys alias and six resources), none of which is gameplay, award, native-ARM or RC acceptance. G-01 stands as Low with the self-bounding narrowing. New punch item R-01 (Medium) should accompany the F-002 remediation; R-02/R-03 are Low leads; F-10 reopens as a Low lead pending a repo grep.