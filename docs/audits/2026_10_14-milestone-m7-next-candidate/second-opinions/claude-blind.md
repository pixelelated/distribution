# Independent blind review — M7 engineering delta (Milestone tier)

Basis: distribution `fac608ff8994` and ES `3178b832b8d1` deltas as embedded, the embedded originals (Install Steam.sh, dolphin-save-paths, cheevos_dolphin.sh, wifictl, raofflineproxy-ctl excerpt, GuiWifi/WifiScanProcess, rvz_hash, Dolphin 6094cfcf sources, Dolphin baseline stderr/fields, Steam 14-case readback, proxy installed-result.json, two command readbacks). Locator-only evidence is treated as unverified here. Source comments are cited as claims, fixture PASS/FAIL fields as data.

---

## Findings

### F-01 — High — Default standalone Dolphin launcher never creates the RetroAchievements client, so #584 offline-proxy routing (and online RA) is inert for `dolphin-sa-gc`/`dolphin-sa-wii`

**Trigger/effect.** `cheevos_dolphin.sh` writes `RetroAchievements.ini` (including the new `HostUrl = 127.0.0.1:8080` routing) and the launcher runs `dolphin-emu-nogui`. In the built frozen Dolphin, `AchievementManager::Init()` — the only place `m_client = rc_client_create(...)` and `rc_client_set_host(...)` happen — is called from the Qt `MainWindow` only. `MainNoGUI.cpp` (complete file embedded) never calls it; `UICommon::Init()` doesn't either. `LoadGame()` therefore hits `if (!m_client) ERROR … return;`. Result: no login, no host interpretation, no awards, for the default core on every device. The configured-INI "proof" cannot become behavior on this launcher.

**Evidence.**
- Dolphin `MainNoGUI.cpp` 1–347: no `AchievementManager` include or `Init`; 280–287 `UICommon::Init()/InitControllers()`, 315 `BootCore`.
- Dolphin `AchievementManager.cpp` 64–99 (`Init` creates client, applies `RA_HOST_URL`), 156–167 (`LoadGame`: `!m_client` → error, return).
- Dolphin `UICommon.cpp` 126–145: no achievement init. `MainWindow.cpp` 269–279 / 347–350: Qt path calls `Init`/`Shutdown`.
- **Original** baseline stderr: `Core/AchievementManager.cpp:164 E … Attempted to load game achievements without achievement client initialized.`; fields: argv `/usr/bin/dolphin-emu-nogui -p headless …`, `"enabled": true`, `"initialized": 0`, `"requests": []`. (`original_exit: 0` is the headless loop.dol run, not RA success.)
- Distro `dolphin-sa/package.mk` 50–52: comment claims RA "is not tied to either [frontend]" — a comment, contradicted above. `emulators/package.mk` GENERIC_X64 and device rows: `add_emu_core … dolphin-sa-gc true` (nogui default). `cheevos_dolphin.sh` 58–89 (routing), 91–103 (INI).
- Criteria touched: AC-059, AC-061/062, AC-065, AC-096, AC-100–103.

**Refutation attempt.** Perhaps a Platform (`PlatformWayland.cpp`, not embedded) initialises the manager; but the error at runtime with `-p headless` and `initialized: 0` is observed, and nothing in `MainNoGUI` reaches the manager regardless of platform. Perhaps the fork intends RA only via `dolphin-qt-gc`; nothing in the delta's copy or AC-103 text embedded here says so, and the default is nogui.

**Smallest correction/check.** Either (a) add a dolphin-sa patch mirroring `MainWindow.cpp` 270/349 in `MainNoGUI.cpp` (`AchievementManager::GetInstance().Init(nullptr)` after `UICommon::Init()`, `Shutdown()` before `UICommon::Shutdown()`), rerun the existing native-owner fixture and require `Achievement Manager Initialized` plus one request on 127.0.0.1:8080; or (b) record in flow/limitations that RA/offline for standalone Dolphin applies to the Qt core only and hide/qualify the Dolphin offline-proxy copy for the nogui default. Re-mark AC-102/103 accordingly.

---

### F-02 — Medium (High if the NetworkManager guard applies on-device) — `wifictl list/scanlist` now propagates rescan refusals; real NM/iwd refuses explicit scans in common states, and `scanlist` requests two rescans ~2 s apart

**Trigger/effect.** Previously rescan errors were discarded and the cached list was returned. Now `list_wifi` returns the rescan's exit status and `scanlist` exits on its first rescan, then `list_wifi` rescans again after `sleep 2`. NetworkManager refuses explicit scans in some states (“Scanning not allowed at this time/while unavailable”, and on some backends “…immediately following previous scan” within ~10 s). ES maps any nonzero code to `inRangeKnown=false` → “COULDN'T SEARCH WI-FI NETWORKS. TRY AGAIN.” REFRESH on real hardware may fail routinely; initial open fails whenever NM scanned/was connecting moments before (first-boot setup, after a failed join). The VM fixture used stubbed `iwctl/nmcli`, so it cannot have observed this.

**Evidence.** wifictl 101–110 (`rescan … || return $?`), 536–540 (`scanlist` second rescan), 48–52; ES `GuiWifi.cpp` 494–497 (`inRangeKnown = range.code == 0`), 454–458; locator AC067–072 (“controlled lower iwctl/nmcli … Physical radio behavior excluded”). AC-068/071/072.

**Refutation attempt.** NM's iwd backend may answer success for an in-progress scan and have no 10 s guard; then only the "connecting/unavailable" refusal remains, which is less frequent. Nothing in the packet shows real `nmcli` exit codes for these paths.

**Smallest correction/check.** Local check (no device gate): on any host with real NM + Wi‑Fi run `nmcli dev wifi rescan; sleep 2; nmcli dev wifi rescan; echo $?` and the same during a connection attempt. Fix: make a rescan refusal non-fatal in `list_wifi`/`scanlist` (log it; failure reserved for the `dev wifi list` query), and drop the duplicate rescan in `scanlist`.

---

### F-03 — Medium — Retained-storage Dolphin launches are refused where the predecessor converted unambiguously (regular memory card in `.config/dolphin-emu/GC/`)

**Trigger/effect.** Old scripts moved a card existing only in `${CONF_DIR}/GC/` to `/storage/roms/bios/GC/` and linked it (`mv -f … ; ln -sf`). The new preparer rejects any non-link, non-absent source (`elif value != "absent": reject`) including the unambiguous "config copy exists, canonical absent" case, exiting 250 before Dolphin starts. A device upgraded after one old-image launch (card created by Dolphin, not yet migrated) cannot play GameCube until the player rearranges files with a file manager. No data loss, but AC-088's retained path regresses from "works" to "refuses".

**Evidence.** dolphin-save-paths 165–177 (card links), 180–188 (rejection incl. comment "Even equal-looking … copies need an explicit retention choice"), 268–285 (`apply`), message 25–26; `start_dolphin_gc.sh`/`wii.sh` diff removed `mv -f "${CONFIG_MEM_CARD}" "${ROMS_BIOS_MEM_CARD}"` branch. AC-086/088.

**Refutation attempt.** AC-086 mandates refusing *ambiguous* conversion; the two-copies case is ambiguous and correctly refused. The single-copy case is not ambiguous, so the refusal is stricter than the criterion requires. The upgrade window is narrow.

**Smallest correction.** Handle `kind(source)=="file" and kind(canonical)=="absent"` for the six card names with `renameat2(RENAME_NOREPLACE)` into `roms/bios/GC/` then symlink (same primitives already present), add that fixture row; or document the refusal explicitly in the Dolphin flow/limitations and ES message.

---

### F-04 — Medium (evidence gap, not asserted failure) — Fail-closed validators for FEX RootFS, Steam runtime and Proton encode exact real-artifact layouts that the packet proves only against synthetic fixtures

**Trigger/effect.** If any assumption differs from the real upstream artifact, every real install stops at that step with no fallback (the old script had no such checks). Assumptions without embedded real-artifact receipts: FEX fetched image must contain `usr/bin/env`, `usr/lib/ld-linux-x86-64.so.2`, `usr/lib/libc.so.6` (x86-64 ELF), root-level `graphics_provider.json` (non-empty object), `usr/share/vulkan/icd.d/freedreno_icd.x86_64.json`, ≤250 000 entries, no file >2 GiB, fetch+extract ≤900 s; fetcher accepts `--force-ui=tty`; runtime has exactly one `steamrt3c_platform_*` and exactly one `libibus-1.0.so.5.*`/`libva.so.2.*`; Proton tarball root equals derived name and contains `files/bin-arm64/wine|wineserver` (ARM64 ELF), `filelock.py`, `version`. The client inventory is pinned to exactly 55 members with `made==20`, `attr==2176188416`, `comment==0` — this one was taken from the real archive per locator, but is forward-brittle: any Valve packaging change breaks fresh installs until the list is edited.

**Evidence.** Install Steam.sh 281–287, 371–402, 405–424, 487; 856–875; 2470–2496, 2402–2403, 2519–2524; 1206–1261, 1979–2006, 2023. Locator AC077–093: real-archive contract stated for the client only; "Native ARM exec deliberately denied". AC-079/082/092.

**Refutation attempt.** Several checks mirror the old script's own assumptions (globs, ICD sed target) and FEX/Proton layouts are stable; the client contract was sampled. The deliberately unrun real downloads are not a failure. Still, AC-092's "real archive layout" discipline was applied only to the client.

**Smallest check.** One lab-only download each (not on device) of the current FEX image, runtime tarball and both Proton assets, running the embedded `validate()`/`unpack()` functions against them, with the resulting member counts/paths recorded in the Steam packet; document the client-inventory maintenance response.

---

### F-05 — Medium — ES RVZ reader requires decoded group size to equal the expected size; Dolphin may write shorter groups (trailing zeroes trimmed), which this reader would reject

**Trigger/effect.** `decode()` requires `input.size() == expected` (NONE) or `ZSTD_decompress` result `== expected`; `unpack()` requires `output == expected`. If the WIA/RVZ group rule "data shorter than expected → remaining bytes are zero" applies to Dolphin-written files, legitimate RVZs with zero-tailed groups fail in the frontend, the sentinel stays all-zero, and F-13's per-startup retry repeats. The proxy path would still succeed (its reader is separate), masking the frontend defect.

**Evidence.** `rvz_hash.cpp` 320–335, 100–129, 276–290; `RVZ-NOTICES.md` scope lists many rejections but not short groups; `installed-result.json` hashes for `dolphin-none.rvz`/`dolphin-zstd.rvz` are from `rvz_datasource.pyc` (proxy), not the ES reader. AC-094/095.

**Refutation attempt.** My recollection of the short-group rule may be wrong, or the fixture RVZs (apparently Dolphin-produced) may already contain such groups and pass the ES reader in the unembedded AC-095 control. Nothing in the packet settles it.

**Smallest check.** Quote the governing clause of Dolphin's `docs/WiaAndRvz.md` in `RVZ-NOTICES.md`; add one Dolphin-converted RVZ whose last raw group ends in ≥1 sector of zeroes to the ES reader regression; zero-fill to `expected` if the rule applies.

---

### F-06 — Medium — Recent-collection repair changes only the compiled default; a persisted spaced value on retained devices would keep the #578 symptom

**Trigger/effect.** `CollectionSystemsAuto` default becomes `"favorites,recent"`. A device whose `es_settings.cfg` already holds `"favorites, recent"` (if the predecessor ever wrote the default) keeps the parser mismatch after upgrade; Recent remains missing. Locators show fresh-default and explicit-token controls only.

**Evidence.** `Settings.cpp` 321; locator AC073–076 ("fresh settings favorites,recent and explicit-token preservation"). AC-074/075.

**Refutation attempt.** If `Settings::saveFile` skips default-valued keys, no device persisted the spaced string and the change is complete; the packet does not show that.

**Smallest check.** Read `CollectionSystemsAuto` from a retained baseline `es_settings.cfg` (library03 artifacts). If present with a space, trim tokens in the collection parser (one line) and add the retained frame.

---

### F-07 — Low — `wait_for_wifi` now fails the whole listing when `iw reg set "${COUNTRY}"` fails

A malformed/unsupported `wifi.country` value (e.g., three letters, lowercase junk) now yields “COULDN'T SEARCH WI-FI NETWORKS” with no hint. Previously ignored. Evidence: wifictl 89–92, 103. Refutation: UI-set values are valid codes; only edited/migrated settings trigger it. Fix: log and continue on `iw reg set` failure for read-only callers.

---

### F-08 — Low (pre-existing packaging, surfaced by the auditor's own observation) — Dolphin's compiled Sys directory does not exist in the image

`-DDATA_DIR="/usr/share/dolphin-emu/"` → `GetSysDirectory()` = `/usr/share/dolphin-emu/sys/`; the image has no `share/dolphin-emu`, while `Data/Sys/*` is copied to `/usr/config/dolphin-emu`. Consequences: `LoadApprovedList()` (hardcore approved-settings) and default RA badges fail to load; global `Sys/GameSettings` load only via the user-dir copy. Evidence: relink flags; `FileUtil.cpp` 760–793; Dolphin `CMakeLists.txt` 174–175, 856–858; package.mk 94–97; `AchievementManager.cpp` 101–127, 881–926; `GameConfigLoader.cpp` 190–191; Phase3 observation. Fix: `-DCMAKE_INSTALL_DATADIR` or a packaged symlink `/usr/share/dolphin-emu/sys → /usr/config/dolphin-emu`; record under AC-059.

---

### F-09 — Low — Several "kept for review" refusals are player-facing dead ends without recovery guidance

Unmatched `transfer-start` journal (`starts == stops`), existing client missing a core ELF, unrecognised Proton stage, ambiguous FEX recovery all refuse deterministically on every retry; terminal text is generic ("Steam client files could not be checked. Nothing was changed."). Evidence: Install Steam.sh 2184–2187, 1366–1375/1589–1593, 2546–2559, 616–654, 2716/1161. Refutation: preservation-first by design (AC-090/092) and stderr prints the specific reason; power-loss durability is out of scope. Fix: include the owned path and a one-sentence next step in the `die` text (it already sleeps 10 s to be read).

---

### F-10 — Low — `readonly STEAM STEAM_GAMES_ROOT` precedes `source /etc/profile`; a profile assigning either aborts via bash readonly error, bypassing `die`

Evidence: Install Steam.sh 2714–2718; the predecessor sourced profile first and defaulted `STEAM="${STEAM:-…}"` afterwards (implying profiles may set it). Check: grep `STEAM=`/`STEAM_GAMES_ROOT=` in the installed image's `/etc/profile` and `profile.d`.

---

### F-11 — Low — New sign-in failure dialog's CANCEL closes the page without `cloud_oauth cancel`, unlike the still-waiting path

Evidence: `GuiMenu.cpp` diff `cloudOAuthOpenSignIn` (`_("CANCEL SIGN-IN"), [page] { page->close(); }`) vs `finishSignIn` (`runSystemCommand("/usr/bin/cloud_oauth cancel")` then `s->close()`). Refutation: `cloudOAuthOwnSession(s)` (not embedded) may cancel on close. Check that function; otherwise add the cancel call.

---

### F-12 — Low — Hygiene

(a) During a scan, `input()` swallows controller accept on the visible BACK button while `hitTest` still lets a mouse/touch press it (`GuiWifi.cpp` 377–391, 393–409). (b) Scan worker is detached and may run through ES shutdown (490–531). (c) `emulationstation2.pot` gained only the ScreenScraper string; the other seven new msgids exist only in the `.po` files. (d) `emulationstation/package.mk` declares an unused `local screenscraper_shared_dev="jelos"`.

---

### F-13 — Low — Failed RVZ hashes are re-attempted at every startup index while they keep failing

`needed()` treats the all-zero sentinel as "retry"; a supported-format but broken RVZ costs up to 128 MiB read / 512 MiB decode per startup. Evidence: `GameCubeRvzHashRetry.h` 31–43; `ThreadedHasher.cpp` 220–228, 320–325; `rvz_hash.cpp` 246, 317. Refutation: unsupported formats fail at header parse (cheap); work is bounded and background. Fix: retry only when file mtime/size changed or after an explicit scan.

---

## What I cannot judge from this packet

- Any image/frame-based criterion (AC-003/010/043/049/067/069/072/076/088): images are not embedded.
- All locator-only originals: Wi‑Fi03 transcript, FEX43/runtime39/Proton56 cases, state-isolation 143 controls, RSS medians, #589 harness repair, ABL/FEX custody and licence inventory (AC-018), rules/register/work-log beyond the embedded readback, and whether candidate image `d816d36a…` was qualified.
- Whether ES consumes `/tmp/launch_error.log` on exit 250 and exports `LANGUAGE` to launchers (claimed in comments; `runemu.sh`/`dolphin-save-paths` depend on it).
- Whether `rc_client_set_host` prepends `http://` (comment in `cheevos_dolphin.sh` 62–63); moot for nogui per F-01.
- Whether `-Dtools=enabled` is what builds `gst-plugin-scanner` (recipe comment) versus the registry option; installed `gst-inspect`/scanner checks are locator-only (AC-051/052).
- Whether `/storage/roms` is a mount point and `/storage/.config/fex-emu` is a real directory on all device layouts (preconditions in `dolphin-save-paths` 147 and `FexUpdate.check_live`).
- Proton `aarch64`/`arm64` asset availability and `rc_hash_iterator_t` API compatibility (compiled, so presumably fine).
- All SM8250 DTS/wireplumber/UCM and kernel patch 0011/0016/0019 effects: upstream hardware foundation, explicitly not recertified here; the 0011 enum reorder matches SMB5 register semantics on reading but no device observation exists.