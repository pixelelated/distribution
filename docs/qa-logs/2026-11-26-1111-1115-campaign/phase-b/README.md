# Phase B: the installed connection and folder scripts on build 12

OS coordinator, 2026-11-26.

- **The guest:** a fresh `tools/vm-pair` guest from build 12's image (`BUILD_ID` `a069abd236…`, rclone 1.76.0), 640x480.
- **The scripts:** `phase-b.sh` (the host half) and `guest-b.py` (the guest half). The guest half is ported from October's `2026-10-26-cloud-profiles-installed-component/payload/guest.py`, which staged an overlay on `bcc866f1`; here the image ships the scripts.
- **How it drives them:** through the installed `cloud_connections` module, which is what `cloud_remote` and the pages call, and through the installed `cloud_folder_validate`.
- **Can this be done on the VM? Yes.** It uses two local alias accounts and a WebDAV account on the host's QA backend. That stanza is generated at run time, copied to the guest at mode 0600, revealed there, and deleted at the end; no credential value is in this tree.

**The witnesses.** Every step writes `witness-<step>.json`:
- rclone section names and types;
- the selection;
- the profile store's sha256 (its bytes include the credentials, so only the hash is kept);
- the three pointers and the two sync switches;
- payload hashes for the local saves and both alias accounts.

## run-1531Z: PASSED

**Clean phase: 43 of 43.**

| Checks | Criteria |
| --- | --- |
| A fresh guest has no connections and both sync switches off | #1111 C01, C06 |
| The first link is In use, has the three defaults, and leaves sync and payload unchanged | C01, C04, C06, C07 |
| A link to a dead port is refused and leaves no section, the same selection and the same profile store | C01, C06 |
| A custom folder on A projects to the pointers. A second link keeps A selected and A's folders | C02, C05 |
| Switching to B shows B's defaults. A folder editor opened on A is refused after the switch. Switching back shows A's folder. Renewing A keeps it | C02, C04, C05, C14 |
| With the transfer lock held (seen held, then seen released), select and defaults are refused as busy, and nothing changes | C06, C22 |
| With the exit sync switched on, select and remove are refused with the automatic-sync reason, and nothing changes | C06 |
| USE pixelelated DEFAULTS applies the three paths to the selected connection only; B keeps `/B/Saves`; no cloud folder is created | C21, C07 |
| Removing the active connection while another remains leaves no selection. An explicit select restores the rows | C01, C10 |
| Remove all, then re-add the same name, a new name, and a WebDAV account: each is In use or selectable with the defaults, and the deleted `/Gone/Saves` is not reused | C01, C04 |
| Across all of it, payload is unchanged and neither switch was ever turned on. The settings-backup default is `/pixelelated/Backups` | C07, C06, C25 |

**Reboot.** The boot id changed.

**Retained phase: 14 of 14.**

| Checks | Criteria |
| --- | --- |
| The selection, the paths and the sections survive the reboot | #1111 C09 |
| A restored global pointer that disagrees with the profile reads as review-folders; an explicit select repairs the pointer | C10, C11 |
| The validator binds to the current config_id; empty saves and settings folders are reported accessible | C11; #1115 C02, C05 |
| A 4,097-entry settings folder is still accessible, with the run not complete; the saves result is still present; nothing is written | #1115 C02, C03 |
| The WebDAV account, selected, gets a validator answer bound to its own config_id (saves present, settings empty, both accessible) | #1115 C05 |

## The two failed runs, kept

- **run-1526Z: a check that passed for the wrong reason.**
  - The lock holder was `flock … sleep`. Terminating `flock` left `sleep` holding the lock.
  - `select` takes the lock before it reads the sync switches, so the two autosync checks "passed" on the still-held lock, and the next step was refused as busy.
  - The fix: the holder runs in a session of its own and is killed as a group, the lock is seen held before and free after, and each refusal check requires its own reason's words. run-1531Z's autosync refusals read "Turn off both automatic save sync options".
- **run-1529Z: the WebDAV link was refused.**
  - The stanza's password is rclone's obscured form, and `save()` obscures what it is given (the page hands it what the player typed), so it was obscured twice.
  - `guest-b.py` now reveals it on the guest first.
  - The same run's `autosync-never-enabled` compared the whole settings dict. The switch existed at `0` after the autosync case, so the check now asks only that neither switch is `1`.
