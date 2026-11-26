# #1428: the cloud setup pages, EN and FR, at 640x480 and 1280x800

Proof packet for [#1428](https://github.com/pixelelated/distribution/issues/1428), 2026-11-26. The frame index is `evidence-index.json` (schema 1, 11 reviewed entries).

**Source:** EmulationStation `d87891f24` (local) in the round `30e6ff3db9`, image `…g30e6ff3db9ac`.

**Walks:** `WALK_SUITE=tools/vm-walks/suite-1428.txt tools/vm-qa <image> --only walks` (round `b1938d2adf`). It was run once at 1280x800 (`qa-30e6ff3db9-webdav-a-20261126-1231`) and once at 640x480 (`VM_RES=640x480`, `…-1240`). Both are VERDICT PASS, with 6 walks of 4 frames each, EN and FR. The frames kept here are the ones read.

| Criterion | What the frames and source show |
| --- | --- |
| 1. Category switches: purpose and cloud destination before action | CLOUD FOLDERS opens with WHAT THESE CHOICES DO ("choosing alone changes nothing") and NO BACKUP OR RESTORE. Each switch names its folder (IN YOUR CLOUD: /pixelelated/…). Each action says what it does: CHECK CLOUD FOLDERS creates nothing; CREATE CLOUD FOLDERS creates folders and setup notes in your cloud. The text fits in EN and FR at both sizes. |
| 3. The overall check includes the connection, and its outcomes stay separate | The hub has CHECK CLOUD SETUP and no peer CHECK CONNECTION. `cloudCheckSetup` (`GuiMenu.cpp` ~7430) runs `cloud_setup --check '<connection>:'`, then `cloud_setup --validate-folders saves,settings`, both bound to one `config_id`. The result page shows CONNECTION / PROVIDER / CONNECTION CHECK apart from ON THIS DEVICE, AUTOMATIC SAVE SYNC and CLOUD FOLDER CHECKS. |

**Not covered here:**
- criterion 2 (before and after fixture manifests);
- criterion 4 (two saved connections, two on one provider);
- criterion 5 (the branch receipts);
- the last criterion (the hub's transfer entries in FR and at 640x480).

**Seen, for review:**
- GAME CONTENT names the same folder as ROMS (`/pixelelated/Content/ROMs`).
- The French page mixes PARAMÈTRES and RÉGLAGES for *settings*.
