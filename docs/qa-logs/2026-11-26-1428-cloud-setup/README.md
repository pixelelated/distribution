# #1428: the cloud setup pages, EN and FR, at 640x480 and 1280x800

Proof packet for [#1428](https://github.com/pixelelated/distribution/issues/1428), 2026-11-26. The frame index is `evidence-index.json` (schema 1, 33 reviewed entries).

**Source:** EmulationStation `d87891f24` (local) in the round `30e6ff3db9`, image `…g30e6ff3db9ac`.

**Walks:** `WALK_SUITE=tools/vm-walks/suite-1428.txt tools/vm-qa <image> --only walks` (round `b1938d2adf`). It was run once at 1280x800 (`qa-30e6ff3db9-webdav-a-20261126-1231`) and once at 640x480 (`VM_RES=640x480`, `…-1240`). Both are VERDICT PASS, with 6 walks of 4 frames each, EN and FR. The frames kept here are the ones read.

| Criterion | What the frames and source show |
| --- | --- |
| 1. Category switches: purpose and cloud destination before action | CLOUD FOLDERS opens with WHAT THESE CHOICES DO ("choosing alone changes nothing") and NO BACKUP OR RESTORE. Each switch names its folder (IN YOUR CLOUD: /pixelelated/…). Each action says what it does: CHECK CLOUD FOLDERS creates nothing; CREATE CLOUD FOLDERS creates folders and setup notes in your cloud. The text fits in EN and FR at both sizes. |
| 2. Toggling or cancelling changes nothing; creation needs confirmation and adds only the selected folders and setup notes | vm-qa's walk witness (cloud and rclone conf hashes, `cloudsaves.*`, the validation context, every local file under `/storage/roms`, every cloud file) is identical before and after three walks: ROMS and BIOS FILES turned on then the page left; CHECK CLOUD FOLDERS; CREATE CLOUD FOLDERS answered NO. Creation asks CREATE THE SELECTED FOLDERS AND SETUP NOTES IN YOUR CLOUD? ... AUTOMATIC SYNC WILL NOT CHANGE. Answered YES with the default selection, the cloud gains `pixelelated/Saves/README.txt`, `pixelelated/Backups/README.txt` and `pixelelated/.layout` (the layout version marker `cloud_setup --seed-folders` writes beside them), removes nothing, and everything else is identical (`criterion-2-witness.txt`). |
| 3. The overall check includes the connection, and its outcomes stay separate | The hub has CHECK CLOUD SETUP and no peer CHECK CONNECTION. `cloudCheckSetup` (`GuiMenu.cpp` ~7430) runs `cloud_setup --check '<connection>:'`, then `cloud_setup --validate-folders saves,settings`, both bound to one `config_id`. The result page shows CONNECTION / PROVIDER / CONNECTION CHECK apart from ON THIS DEVICE, AUTOMATIC SAVE SYNC and CLOUD FOLDER CHECKS. |
| 4. Two saved connections on one provider; the active one named; the change action and its cancellation | With a second WebDAV connection (the guest's qa-cloud stanza copied as qa-two on the guest), the hub reads ACTIVE CONNECTION: QA-CLOUD (WEBDAV). That row opens MANAGE CLOUD CONNECTIONS, the existing management flow: QA-CLOUD WEBDAV - IN USE, QA-TWO WEBDAV. Choosing QA-TWO offers CLOUD CONNECTION with USE THIS CONNECTION among its actions; B backs out to the list with QA-CLOUD still IN USE. Nothing is written by the cancel, so `config_id` and the checks bound to it (`cloudCheckSetup`) are untouched. EN and FR at 640x480, run `…-1307`. |
| 5. Branches, clean and retained state | On both shapes: the retained one (folders in `cloud_sync.conf`, no profile store, as an updated device) and the clean one (a profile store published by the walk's pre-hook, as the setup wizard leaves; a different `config_id`, the same paths). No selection: CHOOSE AT LEAST ONE ITEM TO CHECK., witness identical. Offline (the WebDAV address on a dead port) and a wrong password: COULD NOT REACH THIS CONNECTION. CHECK WI-FI OR SIGN-IN UNDER MANAGE CLOUD CONNECTIONS. Empty selected folders: NO FILES FOUND. Toggle, check and cancel: witness identical on both shapes. Confirmed creation: the same three files added on both, nothing else (`criterion-2-witness.txt`). |
| 6. The transfer entries: direction and next step at the hub, selection before any transfer | The hub (EN and FR) reads BACK UP TO CLOUD / CHOOSE CONTENT FROM THIS DEVICE TO BACK UP. and RESTORE FROM CLOUD / CHOOSE CONTENT TO RESTORE TO THIS DEVICE. Pressing either opens a page titled as its row (ES `d87891f24`) that asks WHAT WOULD YOU LIKE TO BACK UP? / RESTORE? and transfers nothing until its own BACK UP / RESTORE button, whose existing confirmation and preview follow. Frames at 640x480 (EN and FR) and 1280x800 (FR here, EN in standard run 8), from runs `…-1254` and `…-1259`. |

**Not covered here:** nothing in the criteria; the release catalogue is written at the candidate's call.

**Seen, for review** (filed as their own issue):
- After a confirmed creation the page shows CLOUD FOLDER CHECK / COMPLETED (SAVES: NO FILES FOUND, since a setup note is not a save) and says nowhere that folders were created.
- GAME CONTENT names the same folder as ROMS (`/pixelelated/Content/ROMs`).
- The French page mixes PARAMÈTRES and RÉGLAGES for *settings*.

## Build 20: French settings read PARAMÈTRES (#1478 item 2)

Build 20 is round `1d3c0c735e`, ES `0b5e210c5` (D-UI-147). It was walked with `WALK_SUITE=tools/vm-walks/suite-1428.txt tools/vm-qa --only walks`, once at 640x480 (`qa-1d3c0c735e-webdav-a-20261127-0448`) and once at 1280x800 (`…-0520`).

`frames/build20/` keeps the six pages that name the settings tier, in EN and FR at both sizes: 24 frames, indexed in `evidence-index.json` under `build20/`. They are the setup check (both halves), CLOUD FOLDERS (both halves), BACK UP TO CLOUD and RESTORE FROM CLOUD.

- **French** reads PARAMÈTRES throughout: ARCHIVES LOCALES DES PARAMÈTRES, SAUVEGARDES DES PARAMÈTRES, the PARAMÈTRES category, and AUCUNE SAUVEGARDE DES PARAMÈTRES DE CET APPAREIL POUR L'INSTANT. RÉGLAGES appears on none of these pages.
- **English** is unchanged.

**Both runs ended VERDICT: FAIL.** The suite run whole lets its two connection-breaking failure branches (walks 20 and 21) leave the guest's connection broken, so five later witness walks failed (#1498). The walks kept here ran before that, and captured.
