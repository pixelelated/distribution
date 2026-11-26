# Calibration batch: build 12, 640x480, English

`phase-d.sh --res 640x480 --lang en` on build 12 (`a069abd236`, ES `d87891f24`), 2026-11-26 15:45 to 16:00 UTC. It calibrated the walk counts. These frames are not the campaign's review set, which is taken on the ES that ships.

**What it found:**
- **#1480, the hub with no connection selected** (`en/s04/02-hub-unselected.png`): CHANGE CLOUD FOLDER LOCATIONS reads `YOUR SAVES ARE IN:` with nothing after it.
- **#1480, the hub with a connection under review** (`en/s05/02-hub-review.png`): NO CONNECTION SELECTED, while the connections page (`en/s08/03-connections-page.png`) shows the connection IN USE under REVIEW FOLDER LOCATIONS.
- **The driver's own fault.** s08 appended a copy of the `qa-cloud` stanza to `rclone.conf` behind the module, as #1428's suite does. That put the profile in review, and the put-back `cloud_remote remove qa-two` was refused, so s09–s13 ran in that state. Their frames show CLOUD FOLDERS unavailable and walks that drifted into the main menu.
  - The driver now adds and removes the second connection through the installed module (`conn.py`).
  - Before each screen it requires `STATE=selected CONNECTION=qa-cloud SECTIONS=qa-cloud SYNC=off/off`, repairing and saying so, or skipping the screen.

**Confirmed counts** (ES `d87891f24`):

| Count | From | To |
| --- | --- | --- |
| 6 downs | the hub's top | CHANGE CLOUD FOLDER LOCATIONS |
| 4 downs | the editor's CONNECTION row | USE pixelelated DEFAULTS |
| 4 downs, A | the hub's top | the exit sync switch, toggled |
