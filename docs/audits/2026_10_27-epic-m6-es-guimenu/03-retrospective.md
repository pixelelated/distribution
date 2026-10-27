# Retrospective audit — M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

Written by the first reader (Opus 5.5) after stages A and B and the guest window, before any seat saw the packet. Line numbers are the pin's (`16dbac5211`) unless they name a script, which is `8ebaf8daad`'s. The leads are `02`'s (L-01 to L-30).

## 3.1 Architectural coherence

- **One file builds every fork page in place.** 97 of the file's 156 definitions are the fork's own, 3,599 lines, from the content picker (`:4086`) to MANAGE SAVED NETWORKS (`:10512`): the cloud pages, the wizard, the sign-in, the connections, the relink page and the network pages. Each page is one function, and the two largest fork-own ones are over 300 lines (`cloudOpenTransferOptions` 375, `cloudContentSystemPicker` 317). The definitions table separates the cloud and network buckets cleanly, which is D-WORKFLOW-080's option (a) (`02` § The merge debt).
- **The wizard's lifetime discipline holds.** Every page change goes through `cloudSetupPresent` as its scope's last statement, hands the new page on, and closes the old one after the push. Dialog callbacks run on their own copies (`GuiMsgBox.cpp:286-294`). The posted rebuilds are weakly held or owned by their page. The 2026-09-05 shape (a callback capturing a deleted predecessor) is gone (`02` § The transitions).
- **The thread rule holds for the long calls and not for the short ones.** Every network-bound cloud call runs behind `GuiLoading`. The short local ones run on the interface thread with no bound: 116 starts (`cloud_remote list`/`providers`/`fields`, `--connected`, `cloud_oauth status`, `systemctl`). Each is usually quick and none is bounded, so a wedged `rclone` or NetworkManager freezes the menu with nothing on screen (L-04).
- **Reads of other processes' files are mostly uncached, and two are not.** The twelve `exists(p, false)` reads cover the stamps, `rclone.conf` and the markers. The QR (`:7792`) and the scan and selection files (`:4136`, through `isRegularFile`) read the cache, which remembers a miss (L-01, L-03). The QR's miss was shown on the guest with a control.
- **Two readers of one shell output.** `GetShOutput` drops a byte per read; the fork knew (`:7127-7131`) and moved the line readers to `GetShOutputLines`, but the create/update and select/remove paths still read through it, matching sentences by substring (L-05, fixture).

## 3.2 Project conformance

- **`least-surprise.md` and `player-language.md`:** a failure dialog sends the player to a row that does not exist (L-18, guest), the match's refusal and two provider labels reach a French player in English (L-19, L-20, guest), and the Wi-Fi verdict is said three different ways (L-26).
- **`es-player-text.md` § "Every fork string ships in English and French":** the script-supplied refusal (L-19) and the runtime msgid (L-20). The fork's 706 extracted strings all have French.
- **`es-ui-style-guide.md` § Saving:** "apply a credential only when it is non-empty *and* changed". DEVICE PASSWORD and SSH PASSWORD do (`:8417`, `:6533`); the ROCKNIX SECURITY page's ROOT PASSWORD runs `setrootpass` on every close (L-08). The six relink rows are fixed by T21's S1 (L-07).
- **`es-ui-style-guide.md` § Text:** the fork's MANUAL UPDATES dialog is sentence-case prose with a URL (L-21).
- **`upgrade-and-install.md`, "does any string still name the old path?":** `c8dc72cf9` renamed the row and updated one of the two sentences naming it (L-18): the sweep `decision-register.md` asks of a rename covered fewer sites than it changed (blindspot 57's shape).
- **D-UI-039:** the menu map's relink heading is stale against D-UI-046 (L-23); `es-menu-map-check` passes because it checks titles, not headings.
- **D-CLOUD-175/178/179:** the pin builds no join, follow or move; the folder step is CHECK and CREATE with explicit confirmation (`02` § Positives).

## 3.3 Spec fidelity

The brief's figures held at their hashes (`01` § Scope, `02` § The runs). Four of its statements were corrected by command and received as errata at 08:06 UTC: MANUAL UPDATES is the fork's (`975235429`); the RGB LED page and the first SECURITY page are `BATOCERA`-only, never built on ROCKNIX (closing T21's `:2989` and `:3209` notes); the six unguarded credential rows are already fixed by T21's S1; and 11 of the 33 "unread keys" hold once `get_setting`'s `global.` fallback is read. The digest's 15/44 definitions split is its body-text rule; the lane's exact-text rule reads 12/47 (`01` § Scope).

## 3.4 Platform conformance

- **The image is M7's composition over the pin** (G01: both literals). Four of the five scripts the proofs touch are `8ebaf8daad`'s bytes; `cloud_oauth` differs and its `ON_DEVICE` check is the tree's. The composition renames two of the hub's rows (MANAGE CLOUD CONNECTIONS, ADD FROM THIS DEVICE).
- **640x480 menus are full-screen**, so `cloudSetupPresent`'s sizing never runs on the panel the walks use (L-16 not reached).
- **The image's seed `system.cfg` carries `system.battery.warning_threshold=25`**, so the SOUND page's write-if-empty acts only on a device whose file lacks it (L-11).
- **`qrencode` and the sign-in window ship;** `ON_DEVICE=yes`, so L-02's route is not reached here.

## 3.5 Cross-system interaction audit

### Interaction: the global VIDEO FILTER row x `setsettings.sh` x `get_setting`

The row writes `global.videofilters` (`:5947`); the launch script asks `game_setting videofilter` (`setsettings.sh:793`), whose last fallback is `global.videofilter` (`001-functions:164-172`). The names differ by one letter, so the global choice never reaches a game (L-09, guest).

### Interaction: the fast-scrolling switch x `Settings` x `SystemConf`

`addSwitch(..., false)` stores in `system.cfg`; the list reads `Settings::ScrollLoadMedias()` from `es_settings.cfg` (`IList.h:110`, `:118`, `:418`). The switch shows and saves a value nothing reads (L-10, guest).

### Interaction: the QR page x the file cache x the texture cache

`qrencode` writes `/tmp/cloud-oauth-qr.png`; the page asks `exists` through the cache (L-01, guest with control) and asks `TextureResource` by path, which returns any live texture of that name (L-02, not reached on this image).

### Interaction: the relink page x the renamed row

The relink page's failure text names CONNECT OR REPAIR CLOUD STORAGE (`:8460`); the hub's row has been CLOUD CONNECTIONS since `c8dc72cf9` (MANAGE CLOUD CONNECTIONS on the image). The French catalog keeps the old msgids (L-18, guest in both languages).

### Interaction: the ROCKNIX SECURITY page x `setrootpass` x T21's S1

Every close runs `setrootpass` (`:3267-3273`). The script refuses an empty password, so the device's is safe; but after S1 a typed-empty entry is saved to `system.cfg` before the refusal, and the wizard's CURRENT PASSWORD then reads blank while the device keeps its password (L-08).

### Interaction: `cloud_remote` x `GetShOutput` x `cloudConnectionError`

The create and change paths merge stderr into stdout and read the result through a reader that drops one byte per 255 of a long line; a refusal sentence across that byte no longer matches, and the generic sentence shows (L-05, fixture).

## 3.6 Time to play

From `docs/vm-qa-log.md` (the September rows: interface to a game's first frame 0.6 to 1.11 s; `Not measured` on 2026-10-14 and -16). This slice changed nothing, and it names three costs it found:
- **The main menu's build at START:** `GuiMenu::GuiMenu` (`:160-277`) reads the stores, asks `ApiSystem::isScriptingSupported` (T21's) a dozen times and builds rows; no call of this file's starts a process there (`launchKodi` runs on a press, `:182`). The hasher at `:1214` is T20's and starts from FIND ALL GAMES on FRONTEND DEVELOPER OPTIONS, also a press.
- **A page's close before a launch:** every settings page's close writes `es_settings.cfg` (G05 showed a rewrite with no change) and, through `saveSystemConf`, `system.cfg` under the lock. The ROCKNIX SECURITY page's close also re-runs `setrootpass` and its service restarts (L-08), seconds on the interface thread.
- **Opening a cloud page:** the hub starts `cloud_remote list` and `cloud_setup --info` (10 s bound) on the interface thread; CLOUD CONNECTIONS starts `list` twice (L-04). None sits between a launch press and a frame.
