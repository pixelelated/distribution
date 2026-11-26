# #1111 and #1115 on the round's bytes: the qualification plan

OS coordinator, 2026-11-26. Written before any run, as #1111's comment of 2026-11-25 asked. It covers both issues because they share fixtures and a guest.

## Where the evidence stands

A read-only inventory (2026-11-26) compared every existing cloud record with the round, `a069abd236`, whose ES is `d87891f24` and which is build 12's image.

- **One packet matches the round's bytes:** #1428's, `docs/qa-logs/2026-11-26-1428-cloud-setup/` on `next`. It covers part of #1111: the in-use row, the two-connection page, two of the CHANGE CLOUD FOLDER LOCATIONS entry points, and folder-action witnesses.
- **Every other record ran on older bytes.** From October and November, they are:
  - **The installed-component record** (`2026-10-26-cloud-profiles-installed-component`): 34 clean and 29 reboot-retained checks, as an overlay on `bcc866f1`.
  - **The refresh and prose qualifications** (`2026-10-26-cloud-refresh-qualified`, `2026-10-27-cloud-prose-qualification`).
  - **The stale and F06 frames** (`2026-11-01-*`).
  - **G1 and G2** (`2026-11-02-cloud-upgrade-validator`, PASS_G1_G2_SCOPED).
  - **The November 7 map** (`2026-11-07-cloud-tracker-reconciliation/criteria.md`). It proposed ticking 24 of #1111's 25 and all 5 of #1115's, on November's bytes.

  Those records are in the candidate line's tree (`m7-rc-round-20261125/docs/qa-logs/`), not on `next`.
- **Since then the round has changed:**
  - `cloud_connections.py`: #1465's no-op save in `set_folders`.
  - `cloud_setup`: `--locations-only`, and `--seed-folders` now wants a config_id.
  - `cloud_folder_validate`: adds only `--locations-only`; the default path is unchanged.
  - `cloud_oauth`: #1473's crash fix.
  - rclone, from 1.75.2 to 1.76.0.
  - ES's `GuiMenu.cpp` and its French catalog.
  - Unchanged: `cloud_connection_profiles.py`, the transfer scripts, `backuptool`, and the `CloudFolderValidation` parser and its tests.
- **So the campaign reruns the proofs on build 12** and ticks from those artifacts. The November 7 map is the case list. Its evidence is not reused for a tick unless the bytes it exercised are unchanged, and the inventory names which those are.
- **Already rerun today on the round's bytes:** `tools/cloud-connections-test` passed 48 of 48 on the host (rclone 1.60.1 on the host, not the image's).

## C15 is not a test

#1111 C15 asks that a routine credential renewal keep an earlier folder check valid, while a real account, endpoint or path replacement invalidates it. The November 7 map leaves it unmet, and no register row or work log records that it was ever put to Max. It is his decision: D-CLOUD-194 in Open decisions, home #1111. Put plainly:

> When you sign in again to the same cloud account, should the folder check you already ran stay valid? Today any change to the saved connection, the renewed sign-in included, means checking the folders again. Keeping it valid needs the device to prove it is the same account, which it cannot do yet.
> **A (recommended for 0.0.1):** keep today's behavior, and C15 is reworded to say so.
> **B:** build same-account verification first.

The campaign runs everything else and does not wait for this answer.

## The phases

Each phase records its artifacts here, in `docs/qa-logs/2026-11-26-1111-1115-campaign/`.

### A. Host suites on the round's bytes (minutes, no guest)

| Suite | Criteria it feeds |
| --- | --- |
| `tools/cloud-connections-test`: 48 of 48 already | #1111 C01, C04, C06 and C22 source halves |
| `tools/cloud-connection-profiles-test` | C02, C05 source halves |
| `tools/cloud-validator-limits-test`, against the original `cloud_folder_validate` (`bcc866f1`'s) and the round's | #1115 C01, C03 |
| `tools/pixelelated-cloud-validator-test` | #1115 C01, C03; #1111 C16, C19 |

### B. Installed scripts on one fresh guest from build 12 (about 45 minutes)

A driver ports the installed-component checks to a plain `vm-pair` guest. No overlay is needed, because the image ships the scripts.

- **Connections:** made with `cloud_remote create`. At least two backend types are needed for C04's different backend: a local alias, plus WebDAV or SFTP on the host's `tools/cloud-test-backend`.
- **Every step's witness:** `rclone.conf` section names only, the active selection, the profile store, `cloud_sync.conf`'s three remotes and sync flags, and payload manifests on both sides.

Cases, in order:
1. **First link on a fresh install** is In use, and autosync stays off (C01).
2. **A failed link** (a dead port) selects nothing (C01, C06).
3. **A second connection** keeps the selection (C01, C05).
4. **Each connection keeps its own custom folders** across switching (C02).
5. **Renewal** keeps the choices (C05).
6. **Removing the active connection** leaves no selection (C01).
7. **Remove all, then re-add** (same name, a different name, a different backend type) gets the three defaults; the deleted paths are not reused (C04).
8. **No selection with saved paths:** `setup-info` and `folder-context` give a choose-connection state, and an explicit select restores the rows (C10).
9. **The root fixtures:** absent, empty, `/`, a named path, an unreadable config, and no active connection (C19).
10. **`default-folders`:** preview the three paths, cancel, apply, check that other connections are unchanged, and check refusal while busy (a held lock) and while autosync is on (C21, C22).
11. **Payload and folder manifests** before and after every management step: nothing moved and no folder created (C07).
12. **The validator on `bcc866f1`'s and the round's code paths:**
    - a 4,097-entry folder, a deep tree, a delayed listing, missing, permission and malformed cases;
    - accessible-but-limited, and saves results surviving a content limit (#1115 C01–C03);
    - G2's three backend cases (#1115 C05).
13. **Reboot,** then every witness again: retained configuration (C09, #1115 C05).
14. **The settings-backup pointer:** `SETTINGS_REMOTE` keeps its value through the wording change, and a default reset gives `/pixelelated/Backups` (C25).

### C. Upgrade onto build 12 (about 30 minutes)

G1's procedure:
1. A guest from the previous PC image, `43d0bc3b` (kept at `m7-pc-43d0bc3b-20261125/target`).
2. Two local connections, one selected, and six custom paths.
3. The update in place to build 12's tar.

Every witness must be equal before and after the update and after a reboot (C05, C09; #1115 C05 retained). `tools/vm-upgrade-rehearsal` seeds a QA cloud and can carry the connection seed.

### D. Frames on the round's ES (one to two hours)

English and French at 640x480 and 1280x800, through walks driven by `WALK_SUITE`. The #1428 packet's frames are reused where they cover the same screen on the same bytes.

- **The CLOUD CONNECTIONS page:** empty, one connection, several, the AVAILABLE CONNECTIONS group, the spacing before ADD A NEW CONNECTION, focus and scrolling (C12).
- **First connection In use after linking,** and the failed and cancelled linking branches (C03).
- **The folder editor:** SET CLOUD FOLDER LOCATIONS, its body, all three values with the root named, and SETTINGS BACKUP FOLDER (C20, C24, C19's display).
- **USE pixelelated DEFAULTS:** the preview, cancel and confirm (C21).
- **The results page:** five categories, NOT CHECKED, the five instruction pages (C16, C17).
- **Every CHANGE CLOUD FOLDER LOCATIONS entry point,** computer setup included (C18).
- **The no-selection, unreadable and context-changed branches:** stale wording only for the last, and the busy refusal (C11, C14, C06).
- **The limited check, access success and a real connection failure** (#1115 C04).

Each frame goes in `evidence-index.json`. `docs/es-menu-map.md` and the cloud-folder flow are updated in the same change (C08, C13, C23).

## Futro

1. **Assumed.** That build 12's image is what ships these flows: its `BUILD_ID` and the ES pin are checked on the guest first. Also that `cloud_remote` can create a WebDAV or SFTP connection without a provider sign-in; it can, since those are the `keys` tier.
2. **Known unknowns.**
   - Whether the October `run.py` checks port without its sealed QEMU harness.
   - Whether rclone 1.76.0 changes the validator's listing shapes; the limits test answers that in phase A.
   - Whether the French catalog covers every new string; `tools/es-untranslated` answers that before phase D.
3. **Patterns that apply.**
   - #1428's walks (`suite-1428.txt`, the `-unchanged-`/`-witnessed-` witness) are the frame route.
   - #1427's driver is the shape for a scripted guest proof with per-step hashes.
   - G1 is the upgrade route.
4. **What could be missed.**
   - **A walk that toggles the wrong row:** #1428's first folder-action run toggled one row high. Every walk reads its landing frame before acting.
   - **A tick from a record on older bytes:** the inventory's byte comparison is the gate.
   - **A frame that shows text the round no longer renders:** patches 017, 019, 020, 025 and 026 lost lines in the composition, so frames are taken fresh.
   - **C15 ticked without Max's answer:** it is not ticked.
   - **The deleted-connection path reuse checked only by name:** C04 also needs a different backend type, so WebDAV or SFTP alongside the alias.
5. **Before running:** phase A first, because it is the cheapest check that the case list still holds on these bytes. Then B and C share the guest, and D comes last.

## What closes them

- **#1111** closes when C01–C14 and C16–C25 are ticked from phases A–D, and C15 is either reworded on Max's answer or carried as an open decision. Its closure follows the bug rule (D-QA-051): a trace with its `Already written:` line.
- **#1115** closes when C01–C05 are ticked from phases A, B and D.
