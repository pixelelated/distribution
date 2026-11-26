# Phase D: the cloud folder and connection screens on build 13, EN and FR

OS coordinator, 2026-11-26.

- **The image:** build 13, `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261126T161646Z.gbc81894fa826-from-ROCKNIX` (round `bc81894fa8`, ES `c0fd03e1b`, the route `m7-20261126-16a1ec4e624a`). Standard `vm-qa` run 10 PASS on it.
- **The driver:** `phase-d.sh`, one fresh `vm-pair` guest per panel size, with the QA WebDAV cloud seeded as `tools/vm-qa` seeds it (a run-time stanza, never in this tree).
- **Each screen:**
  1. Arms its state over ssh.
  2. Walks from the carousel through `tools/vm-walks/to-manage-cloud-storage` and counts calibrated on build 12 (`cal-640-en/`).
  3. Puts the state back.

  Before each screen the driver requires `STATE=selected CONNECTION=qa-cloud SECTIONS=qa-cloud SYNC=off/off` (`conn.py`); no screen needed a repair. Since s17, each arm's exit code is recorded and fails the run unless the screen is listed in `ARM_REFUSED`. s17's refused arm had gone unnoticed until its frames were read.
- **Can this be done on the VM? Yes.** Every state is local: a selection file, a pointer, a switch, a second connection made through the installed module, a dead port, or 4,097 files in the QA cloud.
- **What was shown:** on the guest's panel, connection names and provider types only, never a URL, user or password.
- **Not for review:** the `cal-640-en/` frames are build 12's calibration and are kept as #1480's "before".
- **Review:** frames were reviewed on tiled sheets (`/workspace/tmp/rocknix-session/tile.py`, standard library). `reviewed.txt` lists every `<size>/<lang>/<screen>` looked at, and `index.py` writes `evidence-index.json` from it: a frame is `reviewed` only when its screen is listed there.

| Screen | State and walk | What the frames show | Criteria |
| --- | --- | --- | --- |
| s01 | hub, CHANGE CLOUD FOLDER LOCATIONS, USE pixelelated DEFAULTS, NO | SET CLOUD FOLDER LOCATIONS names the connection. Three locations, with SETTINGS BACKUP FOLDER. The preview names `qa-cloud` and the three paths, and says files are not moved or created and other connections do not change. NO leaves the page as it was. | #1111 C03, C18, C20, C21, C24 |
| s02 | saves set to `/Custom/Saves`, then the defaults, YES | `/Custom/Saves`, then the three defaults | C20, C21 |
| s03 | content set to `/` | CLOUD ROOT (/) · RACINE DU CLOUD (/) | C19 |
| s04 | explicit empty selection | Hub: NO CONNECTION SELECTED, and the choose-a-connection sentence under CHANGE CLOUD FOLDER LOCATIONS. Editor: FOLDER LOCATIONS UNAVAILABLE with MANAGE CLOUD CONNECTIONS. | C10, C11, C03; #1480 c1 |
| s05 | saves pointer changed behind the profile | Hub: ACTIVE CONNECTION: QA-CLOUD with CONFIRM THIS CONNECTION'S FOLDER LOCATIONS…. Editor: REVIEW FOLDER LOCATIONS. | C11; #1480 c2 |
| s06 | exit sync switched on, then the defaults | TURN OFF BOTH AUTOMATIC SAVE SYNC OPTIONS…; the switch off again | C06, C22, C03 |
| s07 | one connection | AVAILABLE CONNECTIONS, QA-CLOUD IN USE, ADD A NEW CONNECTION | C12, C03 |
| s08 | a second connection through the module | QA-CLOUD IN USE and QA-TWO under AVAILABLE CONNECTIONS | C12 |
| s09 | the connection's own page | CLOUD CONNECTION with CHANGE CLOUD FOLDER LOCATIONS | C18, C03 |
| s10 | CHECK CLOUD FOLDERS (default categories), then each instruction page | COMPLETED: five categories with paths, NOT CHECKED for ROMS, BIOS FILES and GAME CONTENT. A category's own instruction page each, none implying a repair. CLOUD FOLDERS carries CHANGE CLOUD FOLDER LOCATIONS. | C16, C17, C18, C24; #1115 C04 (success) |
| s11 | 4,097 files in the settings backup folder | COULDN'T FINISH. SETTINGS BACKUPS: CHECK INCOMPLETE, FOLDER ACCESSIBLE, "THIS FOLDER'S LISTING IS TOO LARGE FOR ONE CHECK. YOUR FILES HAVE NOT BEEN CHANGED." SAVES still FILES FOUND. | #1115 C02, C04 (limit) |
| s12 | the WebDAV URL on a dead port | COULDN'T FINISH; each folder COULDN'T READ THIS FOLDER | #1115 C04 (failure) |
| s13 | CHECK CLOUD SETUP | CLOUD SETUP CHECK: the connection, CLOUD ANSWERED. WRITING FILES WAS NOT TESTED., the local folders, the sync switches, the folder checks | C18 (its foot is s16) |
| s14 | LINK FROM A COMPUTER | CLOUD STORAGE SETUP with CHANGE CLOUD FOLDER LOCATIONS and `/pixelelated/Saves` | C18 |
| s15 | no saved connection (`rclone.conf` moved aside, then put back) | The hub keeps CHECK CLOUD SETUP and MANAGE CLOUD CONNECTIONS and hides the connection and folder rows; the content rows are dimmed. MANAGE CLOUD CONNECTIONS: NO CONNECTION IN USE, then ADD A NEW CONNECTION. Its line, CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS., asks for a choice with nothing to choose: **#1482**, fixed on the ES round in `7ff5f6b77` for the next build. | C12 |
| s16 | CHECK CLOUD SETUP to the foot of the page | WHAT THIS CHECK COVERS, then CHANGE CLOUD FOLDER LOCATIONS, CHECK OTHER CLOUD FOLDERS and MANAGE CLOUD CONNECTIONS | C18 |
| s17 | `cloud_remote set-folder saves /` | **Refused** by the profile module: "Choose a separate folder for saves or settings backups." (`cloud_connection_profiles.py` never accepts `''` or `/` for saves; `s17.arm.log`). The hub and the editor stay at `/pixelelated/Saves`. So a saves folder at the cloud root cannot occur, and #1480's root clause is answered by the code, not a frame. | #1480 c1 |
| s18 | a second connection (qa-two) removed from its own page | The confirmation says the cloud files stay. CANCEL leaves the page as it was. REMOVE CONNECTION leaves QA-CLOUD alone and IN USE; the restore's state line confirms qa-two was gone. | #1111 C01, C08 |
| s19 | EDIT CONNECTION on qa-two with its endpoint dead, backed out of, then saved | **Not usable on build 13.** Back on the form returns to MANAGE CLOUD CONNECTIONS, not the connection's page. The walk assumed otherwise, and its next presses removed qa-two. That return is **#1483**, fixed in ES `274d3716b`; the screen is redone on build 14. Indexed `walk-failed`. | #1111 C03, C08 |
| s20 | a line before `rclone.conf`'s first section (an unreadable setup) | CLOUD SETUP CHECK: SETUP COULD NOT BE READ. MANAGE CLOUD CONNECTIONS: CONNECTIONS UNAVAILABLE. **But the hub reads NO CONNECTION SELECTED, and the editor and CLOUD FOLDERS ask the player to choose a connection:** an unreadable setup read as no selection. Fixed in ES `6cdcb7a64`. | #1111 C11 |
| s21 | the saves folder changed while CLOUD FOLDERS is open, then CHECK CLOUD FOLDERS | THE CLOUD CHECK IS NO LONGER CURRENT. REOPEN CLOUD FOLDERS AND CHECK AGAIN.: the stale wording, for the change of context. Frames in `s21/` and, after the change, `s21-b/`. | #1111 C11, C14 |
| s22 | the selection emptied while CLOUD FOLDERS is open, then CHECK CLOUD FOLDERS | Not the stale wording, but COULDN'T CHECK YOUR FOLDERS. CHECK YOUR CONNECTION, THEN TRY AGAIN., which points at a connection fault when the known cause is no selection. Fixed in ES `6cdcb7a64`: it names the case (CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS.). | #1111 C10, C11, C20 |

## The runs

| Directory | Size | Screens | Result |
| --- | --- | --- | --- |
| `build13-640x480/` | 640x480 | s01–s14, EN and FR | every walk ran |
| `build13-1280x800/` | 1280x800 | s01–s14, EN and FR | every walk ran except FR s13 (walk rc 3: the `key up` after the check was not seen). Its one frame, `fr/s13/01-stuck-after-up.png`, stays as the record and is indexed `walk-failed`. |
| `build13-640x480-extra/` | 640x480 | s15, s16 | every walk ran |
| `build13-1280x800-extra/` | 1280x800 | s13 (the FR rerun, EN again), s15, s16 | every walk ran |
| `build13-640x480-root/` | 640x480 | s17 | every walk ran; the arm was refused, as the screen now expects (`ARM_REFUSED`) |
| `build13-640x480-more/` | 640x480 | s18–s22 | Every walk ran. s19's path is wrong, as above. The first attempt was cut off by the host restart at 18:27 UTC; its three empty frames were deleted. The second went astray in s18/s19 by reusing the shared connections walk; it was stopped by its process groups, the guests were taken down, and it was rerun. |

Each run used its own fresh guest. `RESULT.txt` in each directory carries the guest's `BUILD_ID` and every arm and restore line. At 1280x800 the menus are a centred panel over the carousel, not full screen, and nothing overruns in either language.

**French.** Every fork string has French: `es-untranslated` reports 818 of 818, and nothing overruns at 640x480. One inconsistency stays, as #1478 put it to Max. The settings-backup folder is ARCHIVES DE RÉGLAGES in the editor and the instruction rows, but SAUVEGARDES DES PARAMÈTRES on the results and setup-check pages, beside SAUVEGARDES for saves. #1111 C24's French half waits on that answer.

## Build 14: the fixes

Build 14 is `ed61fe8e59`, with ES `6cdcb7a64`, route `m7-20261126-552f3815e4b4`, and image `…20261126T192845Z.ged61fe8e5922…`. It carries the three fixes the screens above found. Every frame is at 640x480, in EN and FR, and is indexed with build 14's source.

| Screen | Directory | What the frames show | Criteria |
| --- | --- | --- | --- |
| s04, s05 | `build14-640x480/` | The hub's no-selection and review lines, unchanged on the changed code. | #1111 C10, C11 |
| s15 | `build14-640x480/` | MANAGE CLOUD CONNECTIONS with nothing saved: ADD A CONNECTION BEFORE USING CLOUD TOOLS. Its setup check reads SETUP COULD NOT BE READ, because this arm moves only `rclone.conf` and leaves a profile store naming qa-cloud: an inconsistent store, not a fresh device. | #1482 c1 |
| s25, s26 | `build14-640x480-b/` (EN), `-c/` (FR) | A fresh device, and every connection removed through the module. `setup-info` reads `no-connections`; CLOUD SETUP CHECK and MANAGE CLOUD CONNECTIONS read ADD A CONNECTION BEFORE USING CLOUD TOOLS. | #1482 c1, c2; #1111 C12 |
| s23 | `build14-640x480/` | Saved but none selected: both pages still read CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS. | #1482 c3; #1111 C10 |
| s19 | `build14-640x480-b/` (EN), `-c/` (FR) | Back on EDIT CONNECTION's form returns to the connection's page. A save that re-verifies a dead endpoint ends in THE CONNECTION COULDN'T BE SAVED. … YOUR SETTINGS HAVE NOT CHANGED., and the section's hash is the same before and after. | #1483 c1, c2; #1111 C03, C06, C08 |
| s20 | `build14-640x480/` | An unreadable setup is named on the hub (SETUP COULD NOT BE READ, and the folder row's YOUR FOLDER LOCATIONS CAN'T BE SHOWN RIGHT NOW.), the editor, CLOUD FOLDERS, the setup check and the connections page. | #1111 C11 |
| s22 | `build14-640x480/` | A selection lost while CLOUD FOLDERS is open: CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS., not a connection fault. | #1111 C10, C11, C20 |
| s24 | `build14-640x480/` | Back on LINK FROM THIS DEVICE's WebDAV form returns to the provider chooser with WEBDAV focused. In French the form's row labels are English: #1485. | #1483 c3 |

**s19 in `build14-640x480/` is indexed walk-failed.**
- Run right after s15, its arm could not add qa-two in either language. On its own it could.
- The driver then walked anyway, opened MEGA's form and pressed CONNECT with empty fields. No account or credential was involved, but the guest tried MEGA's servers.
- Since then, a screen whose arm failed is not walked.
- s27 diagnoses the s15 interaction, and s28 shows a completed edit.

**The s15 → s19 add failure.** Build 14's first run could not add qa-two right after s15, in either language.
- **s27** runs the add after s15, with the four files' hashes and a bare listing around it.
- **It worked every time we tried:**
  - s15 first (`-d/`, EN);
  - s15 with a store already present (`-d/`, FR);
  - the exact failing order, s04, s05, s15, then the add (`-e/`).
- **Every file hashes the same before and after s15.**

Nothing on hand explains the failure, so it is **#1487**, keep an eye on, with what would turn it into a bug: the staged verification's own rclone error, which the module does not record.

**A completed edit (s28, `-d/`):** CONNECTION SAVED, and back returns to the connection's page (#1483). That is now in the menu map.

**1280x800 (`build14-1280x800/`):** s25 in EN and FR. Both pages read ADD A CONNECTION BEFORE USING CLOUD TOOLS. / AJOUTEZ UNE CONNEXION AVANT D’UTILISER LES OUTILS CLOUD. (#1482 c1). The first attempt's arm assumed a profile store that does not exist before a first folder action; the new guard skipped its walk. s25 and s26 now save and restore only the files that exist, and the attempt's directory, which held only that arm log, was replaced by the rerun.

## Build 15: the provider labels and SIGN IN AGAIN

Build 15 is `90b95f7259`, with ES `334ee42b8` and route `m7-20261126-3817c3c0b12f`. It carries #1485 (the provider form's labels translated), #1486 (back from SIGN IN AGAIN) and the repaired host tests (#1488). All frames are at 640x480, in EN and FR, in `build15-640x480/`; the French s29 rerun is in `-b/`.

| Screen | What the frames show | Criteria |
| --- | --- | --- |
| s24 | Back on the WebDAV form lands on the provider chooser. In French the form reads ADRESSE DU SERVEUR, TYPE DE SERVEUR, NOM D'UTILISATEUR, MOT DE PASSE, JETON D'ACCÈS. | #1485 c1; #1483 c3 |
| s30 | The S3 form and its lower half. In French: CLÉS DU SYSTÈME, IDENTIFIANT DE CLÉ D'ACCÈS, CLÉ D'ACCÈS SECRÈTE, RÉGION, ADRESSE DU POINT D'ACCÈS, EMPLACEMENT, AUTORISATIONS D'ACCÈS, CLASSE DE STOCKAGE, VERROUILLAGE D'OBJETS DU BUCKET. SERVER SIDE ENCRYPTION and SSE KMS KEY ID are unmapped and keep rclone's names, as D-UI-038 says. The subtitle AMAZON S3 AND COMPATIBLE is #1490. | #1485 c1, c4 |
| s29 | SIGN IN AGAIN, then back from the choice page, returns to the connection's page. The broker reports `idle` afterwards. In English this is `build15-640x480/`; in French, `-b/`. | #1486 c2 |
| s19 | Back on EDIT CONNECTION and a failed save, unchanged from build 14. | #1483 |

**The first French s29 went astray.** The English pass had left a profile store, so qa-oauth, added behind it, read as review-folders. The extra row moved the cursor to qa-cloud, and the walk opened its EDIT form; nothing was saved. That state is #1489. The screen was redone alone, as the first of its pass.

**#1486's before frames** are on build 14 (`build14-640x480-oauth/`): back from the choice page landed on MANAGE CLOUD CONNECTIONS.

**Witness fix:** the broker count in s29's put back used `pgrep -c`, which the guest's busybox lacks. It now pipes to `wc -l`.

## Build 16: connections changed outside the interface, and two provider names

Build 16 is `fc3e489f8a`, with ES `c8bf10703` and route `m7-20261126-29256fe7fb07`. It carries #1489 (a connection added outside the interface is named, and USE THIS CONNECTION checks it and adds it) and #1490 (two provider names translated). All frames are at 640x480, in EN and FR, in `build16-640x480/`. The rerun with the store dumped before and after USE, and the malformed-config screen, is in `-r2/`.

| Screen | What the frames show | Criteria |
| --- | --- | --- |
| s31 | qa-cloud's section copied as qa-ext into rclone.conf behind the module, after the store exists. The hub, CLOUD SETUP CHECK and MANAGE CLOUD CONNECTIONS all read CLOUD CONNECTIONS CHANGED / CONNEXIONS AU CLOUD MODIFIÉES, each with its way out. QA-EXT reads NOT CHECKED YET / PAS ENCORE VÉRIFIÉE. USE THIS CONNECTION confirms, and the list then shows QA-EXT IN USE, with the notice gone. | #1489 c1, c2 |
| s31 (`-r2/`) | The same walk. Its arm log carries the store before and after USE: qa-ext added with the standard folders (`/pixelelated/Saves`, `/pixelelated/Backups`, `/pixelelated/Content`), qa-cloud's entry unchanged. The host case `test_use_checks_and_adds_an_external_connection` proves custom paths survive. | #1489 c2 |
| s20 (`-r2/`) | A malformed rclone.conf still reads SETUP COULD NOT BE READ / RÉGLAGES ILLISIBLES on the hub and the setup check, and CONNECTIONS UNAVAILABLE on the connections page and CLOUD FOLDERS. | #1489 c3 |
| s30, s24 | In French, the chooser's rows and the S3 form's subtitle read PARTAGE WINDOWS (SMB) and AMAZON S3 ET COMPATIBLES. The brand names are unchanged, and the English names are unchanged in English. | #1490 c1, c3 |

**Witnesses from the arm logs:** `setup-info` reads `STATE=connections-changed` before USE, and `cloud_remote list` marks qa-ext `new`. After USE it reads `active` for qa-ext.

**Two findings from the review:**

- **#1492:** a transfer refused in this state said CHOOSE A CONNECTION BEFORE USING CLOUD TOOLS. A connection is chosen. Fixed in build 17.
- **#1493:** three rows run to three lines at 640x480: the French connections-page line here, the hub's CHECK CLOUD SETUP line in French, and CONNECTION CHECK's not-confirmed line in both languages.

**Driver change:** s31's arm and put back now print the store's profiles (names, providers and paths only; the store holds no credentials).
