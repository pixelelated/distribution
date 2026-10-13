# Nova library-copy provenance follow-up

Refs #565; static source and retained-script inspection only. No device contact,
provider request, config change, game launch, or runtime experiment.

The owner clarified that the ROM library came from the computer's Dropbox ROMs
directory and was manually copied through the Nova's USB gadget connection.
The exact request and clarification are recorded in #565.

## What can travel with a ROM folder

Accepted distribution `bc9dfe8141d9561dc1d8502313d00a84c4566ee8`:
`projects/ROCKNIX/packages/sysutils/umtprd/etc/umtprd.conf:14` exports
`/storage/roms` as the Roms MTP share. The accepted file equals current source.
This is the content tree, not the ordinary account/settings/cache locations.

Accepted ES `c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`:

- `es-app/src/SystemData.cpp:1648`: getGamelistPath prefers the system ROM
  folder's gamelist.xml, then the user ES gamelists/system fallback.
- `es-app/src/Gamelist.cpp:208` and `:239`: loads XML metadata; also loads
  the ES recovery directory. Mere presence is not proof of which copy supplied
  the current value; a comparison must include the fallback/recovery paths.
- `es-app/src/MetaData.cpp:81`: favorite, playcount, lastplayed and gametime
  are stored metadata fields; the same file also holds titles/artwork paths
  and other library information.
- `es-app/src/CollectionSystemManager.cpp:1042`: positive PlayCount includes
  a game in Recently Played; no local launch event is required by that test.

A whole-folder copy that includes gamelist.xml can therefore bring Recent
history/favorites with it. A copy containing only ordinary game files does not
itself provide those ES history fields, though an existing local game list can
still supply them. The owner's described route makes imported library metadata
a leading explanation for the two Recent entries. No source/destination game
list comparison was made; arrival method remains unproved.

D-CLOUD-049 already places game lists in game content. Accepted
`projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore:618`
explicitly describes transferable game lists and file-level sharing of play
statistics. ROM-only transfer excludes them; a manual computer copy does not
apply the application's tier filters. No new metadata policy or automatic
stripping was introduced here. A clean firmware gate does not mean that later
user-imported library metadata must be absent.

## Account and operation history are separate

Usual player settings are under `/storage/.config/system/configs/system.cfg`
and other emulator/ES config files; rclone credentials under
`/storage/.config/rclone/rclone.conf`; operation stamps under
`/storage/.cache/cloud_sync/last-*`. A normal system-ROM-folder copy through
this exported tree does not target those paths. A game list is not an account
restore or cloud-operation stamp import. The earlier account-origin uncertainty
therefore remains; the library-copy explanation does not settle it.

Retained October9 source reviewed:
`/tmp/pixelelated-device-deploy-20261009/nova-presync/apply.py`, its
`operation-core.py`, and `postupdate-inspect.py`. The wrapper restricts mutable
settings to local system.cfg and its backup; it archives local originals and
calls settings0 to disable cloudsaves.startup and cloudsaves.gameexit. settings0
compares bytes with those two assignments removed, and protected state is
compared against the device's original binding. The wrapper does not call the
core's broader folder-alignment routine or copy another device's configuration.
The accepted deployment's existing preservation evidence is corroboration;
source inspection alone is not proof that every historical action was logged.

Accepted `projects/ROCKNIX/packages/sysutils/systemd/scripts/userconfig-setup`
seeds missing config from the image on first boot; accepted
`projects/ROCKNIX/packages/rocknix/sources/post-update` refreshes shipped defaults
and includes engineering SSH/Wi-Fi seeding hooks when payloads exist. Both
files equal current source. These mechanisms reinforce why actual final-image
inspection is necessary; their existence does not prove personal data was
present in a particular historical image. The selected accepted-image checks
remain clean within their documented coverage, not a whole-image guarantee.

## Useful next observation

No need to power on the Nova solely to repeat the prior account/history reads.
A read-only comparison of the two affected entries in the original computer
library and the Nova's active game list, including fallback/recovery precedence,
could strengthen the copy explanation. Timestamps and matching values alone
would still not identify the credential writer. No personal cloud scan, script
replay, or configuration reset is proposed.

#565 now carries a disposable-VM library-copy acceptance case: ROM files alone
versus ROM files plus a synthetic game list, expected Recent behavior, and no
new account or cloud-operation stamp state. That experiment is UNRUN; this note
records source inspection only. Existing clean-image/retained-upgrade gates and
the M7 browser-first priority order remain unchanged.
