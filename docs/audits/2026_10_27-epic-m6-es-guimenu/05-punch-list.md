# Punch list — M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

Written by the first reader (Opus 5.5) at stage C, from `02` § The leads and § Corrections and new leads from the seat, `04` § Risk assessment, the guest cycle and `stage-c/astra-grades.md`.

- **reviewed-at:** `db7be4b104` (distribution), **reviewed-at-es:** `16dbac5211` (the pin). **fixed-at** and **fixed-at-es:** at stage F.
- **Independent depth:** one seat, GPT-6 Astra at `max` (42 items: 40 accepted, 1 in part, 1 plausible).
- **One item per defect or reusable improvement**, however many leads found it, ordered by severity. Not items: L-07 (T21's S1 covers it), L-14 (never built on ROCKNIX), L-30 (the reads table, recorded).
- **Nothing here changes a file** under the distribution's `packages/`, `projects/` or `tools/`, or an ES file, at stages A to D. A fix lands only under a stream brief on the ES branch, proven twice. A row added, moved or renamed updates `docs/es-menu-map.md` in the same commit (D-UI-039).
- **Lines** are the pin's, and `8ebaf8daad`'s for the scripts. "Guest" means the M6 image (M7's composition over the pin).

---

## PL-01: the REPAIR A CONNECTION picker calls `close()` on a page it already closed when the network drops before the press (a `bug` proposed)

- **Severity:** High
- **Category:** Correctness
- **Question:** Q1
- **Family:** a page's lifetime or thread
- **Source Finding:** L-31 (Astra GM-31, accepted at its lines) -- proved: tree
- **Owner area:** `GuiMenu::openCloudSetup` (`:8219-8239`), `cloudSetupShowSshStep` (`:6660-6713`)
- **What:** the picker's row closes the setup page `s` (`:8234`) and then calls `cloudSetupShowSshStep(..., picker)`, which returns without presenting when `cloudSetupInfo()` reports no IP (`:6662-6667`). The picker stays, its rows holding the freed `s`; the next press calls `s->close()` on it. **Fix shape:** close `s` only once the next page is presented (hand `s` to the step to close, or check the network before closing), so a refused step leaves every page valid.
- **Can this be done on the VM?** Yes -- an AddressSanitizer case in `tests/cloud-oauth-lifetime.py`'s shape (the extracted functions, `cloudSetupInfo` stubbed to return no IP): heap-use-after-free on the second press before the fix, clean after (`fix-unit-test`); the guest walk with two remotes and the network cut (`fix-walk-pending-image`).
- **question:** none -- the fix is contained.

## PL-02: after a failed CHECK CONNECTION the relink page sends the player to CONNECT OR REPAIR CLOUD STORAGE, a row renamed CLOUD CONNECTIONS on 2026-10-11 (a `bug` proposed)

- **Severity:** Medium
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-18 (Astra GM-17) -- proved: history (`c8dc72cf9`), tree, guest (G08, G11: English and French)
- **Owner area:** `GuiMenu::openRestoreRelink` (`:8460`); `locale/lang/fr/LC_MESSAGES/emulationstation2.po`
- **What:** the sentence names a row the pin does not build; the rename updated the hub's sentence (`:5706`) and missed this one. **Fix shape:** name the pin's row (GAME SETTINGS > MANAGE CLOUD STORAGE > CLOUD CONNECTIONS) with its French; sweep the catalog's three old msgids.
- **Can this be done on the VM?** Yes -- `tools/vocabulary-check`-style grep of every row name cited in a `_("")` against the titles the pin builds (`fix-unit-test` as a new case), and the G08 walk on an image that carries the fix (`fix-walk-pending-image`).
- **question:** the exact path words (the image's composition says MANAGE CLOUD CONNECTIONS; the pin says CLOUD CONNECTIONS).

## PL-03: the global VIDEO FILTER writes `global.videofilters`; the launch script reads `videofilter`, so the global choice reaches no game (a `bug` proposed; upstream's row)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-09 (Astra GM-1) -- proved: tool-run (§ The rows' OS column), tree, guest (G04: `global.videofilters=none`, `get_setting videofilter nes` empty)
- **Owner area:** `GuiMenu::openGamesSettings` (`:5928`, `:5946-5947`); `setsettings.sh:793`, `001-functions:164-172` (T1's, read)
- **What:** one letter: the row's key against the script's. **Fix shape:** the row reads and writes `global.videofilter`; **Already written:** devices carry `global.videofilters` -- read it when `global.videofilter` is absent and write the new key (read both, write the new one).
- **Can this be done on the VM?** Yes -- G04's walk and `get_setting` answer the chosen filter (`fix-walk-pending-image`); a rows-table case asserting the key (`fix-unit-test`).
- **question:** a contained fix of upstream's row (`bugs-are-agent-first.md` rule 6) or left to upstream (D-UI-079)? A #585 line either way.

## PL-04: GAME MEDIAS DURING FAST SCROLLING saves to `system.cfg`; its reader reads `es_settings.cfg`, so the switch does nothing (a `bug` proposed; upstream's row)

- **Severity:** Medium
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-10 (Astra GM-2) -- proved: tree, guest (G03)
- **Owner area:** `GuiMenu::openUISettings` (`:9485`); `IList.h:110`, `:118`, `:418`; `Settings.cpp:37`, `:61`, `:145`
- **What:** `addSwitch(..., "ScrollLoadMedias", false)` -- the bool is `storeInSettings`. **Fix shape:** `true`. **Already written:** a device that toggled it carries `ScrollLoadMedias=` in `system.cfg`; carry that value into `es_settings.cfg` once, or accept the default (argued in the stream).
- **Can this be done on the VM?** Yes -- G03's walk reading `es_settings.cfg` (`fix-walk-pending-image`).
- **question:** as PL-03 (rule 6 or D-UI-079).

## PL-05: the device password: ROOT PASSWORD is unmasked and applied on every close; three password pages can persist an empty `root.password` while the device keeps its password (a `bug` proposed)

- **Severity:** Medium
- **Category:** Security
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-08 (Astra GM-5, narrowed: the split is at the pin, not from S1), L-32 (Astra GM-32) -- proved: tree
- **Owner area:** `openSystemSettings`' SECURITY page (`:3261-3275`), `cloudSetupOpenPasswordPage` (`:6523-6542`), `openRestoreRelink`'s DEVICE PASSWORD (`:8412-8425`); `GuiSettings::save()` (`GuiSettings.cpp:82-95`); `setrootpass:20-26` (T1's, read)
- **What:** ROOT PASSWORD runs `setrootpass` on every close, changed or not, re-hashing and restarting services on the interface thread; an empty entry is persisted by `save()` while `setrootpass` refuses it, so `root.password` reads empty and the wizard's CURRENT PASSWORD shows blank. **Fix shape:** one guarded apply for the three pages: non-empty and changed, else the stored value is restored before the save; the SECURITY row masked; the unused `rootpassword` text removed.
- **Can this be done on the VM?** Yes -- a harness case over the three save hooks (`fix-unit-test`); the guest: open and close SECURITY unchanged and read the journal for no `setrootpass` (`fix-walk-pending-image`).
- **question:** should the SECURITY row show the password at all (the SSH wizard shows it by design)?

## PL-06: 116 process starts on the interface thread with no caller-side bound; each `cloud_oauth cancel` sleeps a second there (a `bug` proposed for the cloud pages)

- **Severity:** Medium
- **Category:** Reliability
- **Question:** Q3
- **Family:** a page's lifetime or thread
- **Source Finding:** L-04 (Astra GM-10, narrowed: caller-side sites, not proved indefinite blocks; the cancel sleeps added) -- proved: tool-run (`t26-pages.py`), tree
- **Owner area:** the cloud pages: `CloudConnectionsPage` (`:5579`, `:5589`), `cloudRemoteBackends`/`cloudRemoteLines` callers (`:7233`, `:7321`, `:7450`, `:7930`, `:8027`, `:8091`), `--connected` (`:6749`), `cloud_remote active` (`:7060`), `cloud_oauth status`/`cancel` (`:7515`, `:7692`, `:7708`, `:7813`, `:7835`, `:7848`, `:6476`), `--set-systems` (`:4207`), `systemctl` for SSH (`:6695-6698`)
- **What:** each is usually quick and none is bounded; the player sees nothing while it runs; the cancel's one-second sleep is certain. **Fix shape:** a `timeout` on each local helper call and a spinner where it can exceed a frame; the cancel off the interface thread. The fork's lanes only; upstream's service rows are recorded (D-UI-079).
- **Can this be done on the VM?** Yes -- the pages tool's interface-unbounded count for the cloud pages falls to 0 (`fix-unit-test` as the generator's asserted count); the guest timing a sign-in start (`fix-walk-pending-image`).
- **question:** the bound for each (a few seconds, per D-CLOUD-109's spirit) -- the coordinator's.

## PL-07: the sign-in's QR read is cached, so one failed attempt leaves the session text-only; a page built while the old one lives may draw the old code (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read that can be stale
- **Source Finding:** L-01 (Astra GM-11), L-02 (Astra GM-12, conditional) -- proved: guest with a control (G10), tree
- **Owner area:** `cloudOAuthShowSignIn` (`:7767-7796`), `cloudOAuthPresentChoice` (`:7644-7646`)
- **What:** `exists(qrPath)` remembers its first answer until the cache is reset; `TextureResource` returns a live texture of the same key. **Fix shape:** `exists(qrPath, false)` and a path that names the session (or the image's reload), with `qrencode`'s result read.
- **Can this be done on the VM?** Yes -- G10's three attempts (`fix-walk-pending-image`); a harness case for the read (`fix-unit-test`).
- **question:** none.

## PL-08: cached reads of files other processes write: the scan and selection files through `isRegularFile` (its comment says uncached) and `wg0.conf` (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q4
- **Family:** a read that can be stale
- **Source Finding:** L-03 (Astra GM-13: `:4589` is not a gate), L-34 (Astra GM-34) -- proved: tree
- **Owner area:** `cloudSelectionRead` (`:4133-4150`), the comment at `:4154-4156`; `openNetworkSettings` (`:10303`)
- **What:** a miss is remembered; the consequence differs by file. **Fix shape:** an uncached regular-file test (`exists(p, false)` then a stat), and `exists(wg0.conf, false)`; the comment made true.
- **Can this be done on the VM?** Yes -- `tests/cloud-content-selection.py` gains a case with the file absent then written (`fix-unit-test`).
- **question:** none.

## PL-09: script text reaches the screen untranslated: the match's refusal and a failed maintenance run's why (a `bug` proposed)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-19 (Astra GM-18), L-37 (Astra GM-37) -- proved: tree
- **Owner area:** `cloudOpenMatch` (`:5313-5326`), `runMaintenanceCommand` (`:360-389`)
- **What:** raw English lines upper-cased into a dialog, where the cloud's last-run why goes through `CloudText::localizedWhy` (`:4697`). **Fix shape:** the same localization for both, with the scripts' sentences in `CloudText::whySentences` and the French catalog (`es-player-text.md` § French).
- **Can this be done on the VM?** Yes -- `es-unit-tests` cases over the mapping; the guest under `fr_FR` with a refused match (`fix-walk-pending-image`).
- **question:** none.

## PL-10: provider labels bypass the French: a runtime msgid with no extractable literal, `providerLabel()` without gettext, and the form's script-supplied choice labels (a `bug` proposed)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-20 (Astra GM-19), L-36 (Astra GM-36) -- proved: tree, guest (G11: the two phrases in English among French rows)
- **Owner area:** `openCloudAddRemote` (`:8116`), `CloudText.cpp:18-46`, `:5679-5682`, `:8012`, `:8078`, `:7323-7328`, `:7452-7455`
- **What:** WINDOWS SHARE (SMB) and AMAZON S3 AND COMPATIBLE are phrases; the rest are names. **Fix shape:** the table's phrases marked for extraction (`N_()`) and translated at every display; the script's choice labels left as the provider's names, or mapped.
- **Can this be done on the VM?** Yes -- `tools/es-untranslated` counts them once extractable; G11's frame (`fix-walk-pending-image`).
- **question:** which provider strings are names (left) and which are phrases (translated).

## PL-11: the command readers: `GetShOutput` drops a byte per read and does not test `popen`; two parses of one success line; a lost status line reads as YOUR CLOUD IS ANSWERING (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q6
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-05 (Astra GM-26), L-06 (GM-27), L-38 (GM-38, plausible), L-39 (GM-39) -- proved: fixture (`stage-b/positives/getshoutput.out`), tree
- **Owner area:** `:7407-7422`, `:7995-8001`, `:8445-8453`, `:5579`, `:5589`; `Platform.cpp:891-905` (`es-core`'s)
- **What:** a long line loses a byte, so a refusal sentence can fail to match; the success parses differ; an empty status reads as 0. **Fix shape:** this file's callers move to `GetShOutputLines` with the exit status (`executeScriptLegacy`'s pair), one parse of `OK=<name>` as a whole line; `GetShOutput` itself is a #585 line (upstream's).
- **Can this be done on the VM?** Yes -- the fixture extended to the callers' parse (`fix-unit-test`).
- **question:** none.

## PL-12: the relink WI-FI PASSWORD page reconnects on every close, changed or not (a `bug` proposed)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-40 (Astra GM-40) -- proved: tree
- **Owner area:** `openRestoreRelink` (`:8307-8318`)
- **What:** opening the page and pressing back starts an association. **Fix shape:** reconnect only when the key changed (compare with the value at entry).
- **Can this be done on the VM?** Yes -- a harness case counting `enableWifi` calls over the finalizer (`fix-unit-test`).
- **question:** none.

## PL-13: a stored `led.color` reaches `sh -lc "..."` unquoted (a `bug` proposed)

- **Severity:** Low
- **Category:** Security
- **Question:** Q6
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-35 (Astra GM-35) -- proved: tree
- **Owner area:** `openSystemSettings` (`:2150-2167`), ROCKNIX-built behind `DEVICE_LED_CONTROL`
- **What:** a value kept from `system.cfg` is selectable and interpolated into nested shell syntax. **Fix shape:** `Utils::String::shellQuote` on the argument; `credential-quoting.py`'s count gains the site.
- **Can this be done on the VM?** Yes -- `tests/credential-quoting.py`-style case (`fix-unit-test`).
- **question:** ROCKNIX's code in a lane the fork has not worked in: contained (rule 6) or left (D-UI-079)?

## PL-14: the MANUAL UPDATES dialog is sentence-case prose, in the fork's own code (a `bug` proposed)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-21 (Astra GM-20, narrowed: the URL is not itself the break) -- proved: history (`975235429`), tree
- **Owner area:** `openUpdatesSettings` (`:1513-1521`)
- **What:** the fork's dialect is ALL CAPS (`es-ui-style-guide.md` § Text). **Fix shape:** the sentence in capitals with the URL as written, and its French.
- **Can this be done on the VM?** Yes -- a frame of the dialog (`fix-walk-pending-image`).
- **question:** the words.

## PL-15: the menu map's relink heading reads FINISH RESTORE SETUP against D-UI-046 (the map, a stream's commit)

- **Severity:** Low
- **Category:** Docs
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-23 (Astra GM-22) -- proved: tree (`docs/es-menu-map.md:405`)
- **Owner area:** `docs/es-menu-map.md:405`
- **What:** the code builds FINISH RESTORE PROCESS everywhere. **Fix shape:** the heading renamed, in the commit of a stream (D-UI-039), `tools/es-menu-map-check` passing before it.
- **Can this be done on the VM?** Not needed -- a document; the check runs on the host.
- **question:** none.

## PL-16: the Wi-Fi verdict is said three ways (a design item)

- **Severity:** Low
- **Category:** UX
- **Question:** Q7
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-26 (Astra GM-28) -- proved: tree
- **Owner area:** `:8320-8332`, `:10084-10090`, `:10124-10129`, `:10172`
- **What:** WI-FI ENABLED on a page close; nothing on the relink page's success; nothing either way from the switch. **Fix shape:** one composer, decided at the pause (`least-surprise.md`).
- **Can this be done on the VM?** Yes -- frames of the three paths.
- **question:** what each path should say.

## PL-17: a page of only `addInputTextConfigRow` rows writes nothing on its close; four sub-pages work around it with `onFinalize` saves (another slice's file)

- **Severity:** Low
- **Category:** Maintainability
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-12 (Astra GM-7: four pages, not six) -- proved: tree
- **Owner area:** `GuiSettings.cpp:88-89` (another interface slice's); the four sub-pages (`:8307-8309`, `:8360`, `:8376`, `:8393`)
- **What:** the next such page will not persist, silently. **Fix shape:** `save()` saves when a text row changed a store; for the slice that owns `GuiSettings.cpp`.
- **Can this be done on the VM?** Yes -- a unit case over `save()`.
- **question:** deferred to the owning slice, or folded into T21's `GuiSettings` work?

## PL-18: two conditional writes when SOUND SETTINGS opens, and the timezone written by every close (a `bug` proposed, Low)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-11 (Astra GM-6) -- proved: tree, guest (G05: the seed already carries the threshold)
- **Owner area:** `openSoundSettings` (`:9609-9613`, `:9653-9661`), `openSystemSettings` (`:1857-1870`)
- **What:** writes before any player action; upstream's and ROCKNIX's rows. **Fix shape:** read the default without writing it; write the timezone only when it changed.
- **Can this be done on the VM?** Yes -- the stores read before and after a no-change visit.
- **question:** rule 6 or D-UI-079 (upstream's and ROCKNIX's rows).

## PL-19: back on TRY AGAIN / CANCEL SIGN-IN lands on CANCEL SIGN-IN (a style item)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-22 (Astra GM-21: two sites) -- proved: tool-run, tree; guest `CANNOT in this window`
- **Owner area:** `:7702-7717`, `:7824-7827`
- **What:** the one place in the wizard where back leaves. **Fix shape:** as ruled.
- **Can this be done on the VM?** Yes -- a failing sign-in on the guest (a dead provider address) and the frame after B.
- **question:** keep, or make back retry/dismiss?

## PL-20: an empty HOSTNAME shows a blank row, where the style guide gives `AUTO` for "system decides" (a design item)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-25 (Astra GM-24: at the pin, not from S1) -- proved: tree
- **Owner area:** `openNetworkSettings` (`:9929`)
- **What:** the empty value means the device's own name. **Fix shape:** as ruled.
- **Can this be done on the VM?** Yes -- a frame.
- **question:** show `AUTO`, the cleaned name, or nothing?

## PL-21: one quoting algorithm in two functions (a refactor)

- **Severity:** Low
- **Category:** Maintainability
- **Question:** Q6
- **Family:** --
- **Source Finding:** L-27 (Astra GM-25) -- proved: tree
- **Owner area:** `cloudShellQuote` (`:7183-7194`), `Utils::String::shellQuote`
- **What:** identical. **Fix shape:** one function.
- **Can this be done on the VM?** Not needed -- `credential-quoting.py` and `cloud-set-systems-quoting.py` cover the callers.
- **question:** now, or with PL-22's split?

## PL-22: the structure and the merge debt: the fork's pages out of `GuiMenu.cpp` (D-WORKFLOW-080 option (a)), `cada856d8`'s hotspots named (a Backlog proposal)

- **Severity:** Low
- **Category:** Maintainability
- **Question:** Q7
- **Family:** --
- **Source Finding:** L-28 (Astra GM-29: hotspots, not certain conflicts), L-29 (GM-30) -- proved: tool-run
- **Owner area:** `GuiMenu.cpp` as a whole
- **What:** 11,747 lines; the cloud pages (`:4086-8497`) and the network pages (`:9744-10512`) separable; `cada856d8` meets the fork in all four of its hunks. **Fix shape:** a Backlog the coordinator files.
- **Can this be done on the VM?** Not needed.
- **question:** file the Backlog?

## PL-23: built rows write keys nothing reads, by name or by `get_setting`'s fallback (recorded; upstream's rows)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q2
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** L-13 (Astra GM-3: compiled, reachable, persisted and applied directly distinguished) -- proved: tool-run, guest (G06)
- **Owner area:** `:6085` (PAUSE ON TRANSLATED SCREEN, reachable), `:1390`, `:5853`, `:6111` and the rest of § The rows' list
- **What:** PAUSE ON TRANSLATED SCREEN is reachable and its key unread; VIDEO MODE and AUTOCONFIGURE CONTROLLERS are hidden on the image; AUDIO PROFILE and WIREGUARD VPN apply directly. **Fix shape:** recorded for upstream (a #585 line).
- **Can this be done on the VM?** Yes -- frames (G06).
- **question:** none.

## PL-24: upstream's smaller ones: `exitreboot` with no quit on its page, the fuel gauge's French, three lower-case `Reboot now` / `later` dialogs (recorded, D-UI-079)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-15 (Astra GM-9), L-24 (Astra GM-23, narrowed) -- proved: tool-run, tree
- **Owner area:** `:1100`, `:517-518`, the three dialogs (§ The pages)
- **What:** upstream's lane. **Fix shape:** none here; #585 lines.
- **Can this be done on the VM?** Not needed.
- **question:** none.

## PL-25: the theme-set file is written with `writeAllText` (Backlog #1186: this slice's to move onto the atomic writer)

- **Severity:** Low
- **Category:** Reliability
- **Question:** Q4
- **Family:** a row that writes or reads the wrong place
- **Source Finding:** the dispatch (Backlog #1186, T21's PL-26) -- proved: tree
- **Owner area:** `saveSubsetSettings` (`:11587`)
- **What:** a kill during the write can leave a cut file. **Fix shape:** `Utils::AtomicFile::writeText`. **Already written:** existing theme-set files are read as before.
- **Can this be done on the VM?** Yes -- T21's kill sweep pattern over the writer (`fix-unit-test`).
- **question:** none.

## PL-26: the 0.75 wizard page relies on `GuiSettings`' default position (recorded)

- **Severity:** Low
- **Category:** UX
- **Question:** Q1
- **Family:** a page's lifetime or thread
- **Source Finding:** L-16 (Astra GM-15) -- proved: tree; guest: not reached at 640x480 (full-screen menus)
- **Owner area:** `cloudSetupPresent` (`:6484-6504`)
- **What:** one constant from #540's shape. **Fix shape:** position the 0.75 page as the 0.90 one is.
- **Can this be done on the VM?** At 1280x800 only: `fix-walk-pending-image` until `vm-pair` has `--res`.
- **question:** none.

## PL-27: self-capturing callbacks leak each page's switches (and the provider form's values map) on every visit (recorded)

- **Severity:** Low
- **Category:** Maintainability
- **Question:** Q1
- **Family:** a page's lifetime or thread
- **Source Finding:** L-17 (Astra GM-16), L-33 (Astra GM-33) -- proved: tree
- **Owner area:** `:5651`, `:5658`, `:7301`, `:10097`, `:10133`, `:10182`, `:10201`, `:10220`
- **What:** the cycles keep the closures, which is also what keeps `:10149` from freeing its own callback. **Fix shape:** weak captures, or the transfer page's `onFinalize` clearing (`:5202-5206`); the delete-from-own-callback paths restructured to post.
- **Can this be done on the VM?** Yes -- LeakSanitizer over an extracted builder.
- **question:** none.

## PL-28: FINISH ignores a failed marker removal and says nothing (recorded, Low)

- **Severity:** Low
- **Category:** UX
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-41 (Astra GM-41, in part) -- proved: tree
- **Owner area:** `openRestoreRelink` (`:8486-8493`)
- **What:** the marker stays (the page returns at the next start: the safe direction). **Fix shape:** a sentence when the removal fails.
- **Can this be done on the VM?** Yes -- a read-only marker on the guest.
- **question:** worth a sentence?

## PL-29: with `cloud_scan` absent the fallback cannot reach the transfer options (latent)

- **Severity:** Low
- **Category:** Correctness
- **Question:** Q5
- **Family:** a word or a dialog that breaks the house rules
- **Source Finding:** L-42 (Astra GM-42) -- proved: tree
- **Owner area:** `cloudOpenTransfer` (`:5253-5256`), `cloudOpenTransferOptions` (`:4838-4841`)
- **What:** every image ships `cloud_scan`. **Fix shape:** remove the fallback (D-CLOUD-175's scripts are current) or let it skip the stamp.
- **Can this be done on the VM?** Yes -- a harness case with `cloud_scan` absent.
- **question:** remove the fallback?

---

## Phase 7 resolution gate

At stage C, before the audit issue: every item open. Stage F writes each outcome -- resolved with its commit, deferred to a named issue, withdrawn, or recorded as written -- in this table and the index together.

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | -- |
| PL-02 | Open | -- |
| PL-03 | Open | -- |
| PL-04 | Open | -- |
| PL-05 | Open | -- |
| PL-06 | Open | -- |
| PL-07 | Open | -- |
| PL-08 | Open | -- |
| PL-09 | Open | -- |
| PL-10 | Open | -- |
| PL-11 | Open | -- |
| PL-12 | Open | -- |
| PL-13 | Open | -- |
| PL-14 | Open | -- |
| PL-15 | Open | -- |
| PL-16 | Open | -- |
| PL-17 | Open | -- |
| PL-18 | Open | -- |
| PL-19 | Open | -- |
| PL-20 | Open | -- |
| PL-21 | Open | -- |
| PL-22 | Open | -- |
| PL-23 | Open | -- |
| PL-24 | Open | -- |
| PL-25 | Open | -- |
| PL-26 | Open | -- |
| PL-27 | Open | -- |
| PL-28 | Open | -- |
| PL-29 | Open | -- |

```yaml
punch_index:
- id: PL-01
  severity: "High"
  category: Correctness
  question: Q1
  source_finding: "L-31"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: UX
  question: Q5
  source_finding: "L-18"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-09"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Correctness
  question: Q2
  source_finding: "L-10"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Security
  question: Q2
  source_finding: "L-08, L-32"
  outcome: "open"
- id: PL-06
  severity: "Medium"
  category: Reliability
  question: Q3
  source_finding: "L-04"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-01, L-02"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Correctness
  question: Q4
  source_finding: "L-03, L-34"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-19, L-37"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-20, L-36"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Correctness
  question: Q6
  source_finding: "L-05, L-06, L-38, L-39"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-40"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Security
  question: Q6
  source_finding: "L-35"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-21"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Docs
  question: Q5
  source_finding: "L-23"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: UX
  question: Q7
  source_finding: "L-26"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: Maintainability
  question: Q2
  source_finding: "L-12"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-11"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-22"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-25"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Maintainability
  question: Q6
  source_finding: "L-27"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Maintainability
  question: Q7
  source_finding: "L-28, L-29"
  outcome: "open"
- id: PL-23
  severity: "Low"
  category: Correctness
  question: Q2
  source_finding: "L-13"
  outcome: "open"
- id: PL-24
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-15, L-24"
  outcome: "open"
- id: PL-25
  severity: "Low"
  category: Reliability
  question: Q4
  source_finding: "Backlog #1186"
  outcome: "open"
- id: PL-26
  severity: "Low"
  category: UX
  question: Q1
  source_finding: "L-16"
  outcome: "open"
- id: PL-27
  severity: "Low"
  category: Maintainability
  question: Q1
  source_finding: "L-17, L-33"
  outcome: "open"
- id: PL-28
  severity: "Low"
  category: UX
  question: Q5
  source_finding: "L-41"
  outcome: "open"
- id: PL-29
  severity: "Low"
  category: Correctness
  question: Q5
  source_finding: "L-42"
  outcome: "open"
```
