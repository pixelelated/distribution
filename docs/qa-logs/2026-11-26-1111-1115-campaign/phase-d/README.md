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

## The runs

| Directory | Size | Screens | Result |
| --- | --- | --- | --- |
| `build13-640x480/` | 640x480 | s01–s14, EN and FR | every walk ran |
| `build13-1280x800/` | 1280x800 | s01–s14, EN and FR | every walk ran except FR s13 (walk rc 3: the `key up` after the check was not seen). Its one frame, `fr/s13/01-stuck-after-up.png`, stays as the record and is indexed `walk-failed`. |
| `build13-640x480-extra/` | 640x480 | s15, s16 | every walk ran |
| `build13-1280x800-extra/` | 1280x800 | s13 (the FR rerun, EN again), s15, s16 | every walk ran |
| `build13-640x480-root/` | 640x480 | s17 | every walk ran; the arm was refused, as the screen now expects (`ARM_REFUSED`) |

Each run used its own fresh guest. `RESULT.txt` in each directory carries the guest's `BUILD_ID` and every arm and restore line. At 1280x800 the menus are a centred panel over the carousel, not full screen, and nothing overruns in either language.

**French.** Every fork string has French: `es-untranslated` reports 818 of 818, and nothing overruns at 640x480. One inconsistency stays, as #1478 put it to Max. The settings-backup folder is ARCHIVES DE RÉGLAGES in the editor and the instruction rows, but SAUVEGARDES DES PARAMÈTRES on the results and setup-check pages, beside SAUVEGARDES for saves. #1111 C24's French half waits on that answer.
