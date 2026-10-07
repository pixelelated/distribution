# Cloud folders in pixelelated 0.0.1

A new setup uses `/pixelelated` on your cloud provider. `Saves` holds game
saves, save states, and screenshots; `Backups` holds settings backups;
`Content` holds ROMs, BIOS files, and other game content you choose to back up.

An upgrade from ROCKNIX preserves your sign-in and configured folders.
Connecting cloud storage creates the selected folders and instructions for
adding your files. It does not move an existing library.

To use `/pixelelated`, arrange your files there using your cloud provider
or a computer. Then open `Game Settings` → `Cloud Settings` →
`Manage Cloud Storage` → `Cloud Storage Setup` → `Change Cloud Folder`
and select `/pixelelated/Saves`. This also selects the sibling `Backups`
and `Content` folders. Repeat the folder selection on each device that
uses this cloud; other devices keep their existing selection.

Put ROMs in `Content/ROMs`, using one folder per system, and BIOS files in
`Content/BIOS`. `Restore from the Cloud` lets you choose which systems to
download. Your device does not need a copy of the whole cloud library.

If both `/ROCKNIX` and `/pixelelated` already contain files, compare their
contents before combining them. Keep both versions of any differing file
until you have chosen which to use.

Settings backups written by ROCKNIX remain readable. Backup filenames,
partition labels, the default hostname and stored settings keys retain
ROCKNIX identifiers for compatibility; the displayed project name is
pixelelated. Blitterbot remains the developer account, and Rasteratops is a
character rather than the distribution name.

This is prepared release documentation for #508 (D-CLOUD-175), replacing
the migration instructions from #409. Publish it with the qualified build
that includes manual cloud setup. The accepted H700 and SM8550 artifacts
from earlier on 2026-10-07 still contain the previous migration flow.
