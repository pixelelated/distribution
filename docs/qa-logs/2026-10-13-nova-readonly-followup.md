# Nova read-only provenance follow-up

Refs #565. Owner explicitly authorized read-only troubleshooting after bringing
the Nova online. Authorization/plan: issuecomment-6147924942. Observed October13
14:33–14:37UTC on the accepted bc9dfe8141 engineering image. The host ran short
Python collectors through SSH stdin with -I -B; no collector file was staged on
the device, and no settings/game/cloud/input/reboot action occurred. SSH itself
may produce ordinary access logs; this is not a byte-invariant whole-device claim.

## What the live artifacts establish

- The two reported game histories remain in /storage/roms/gba/gamelist.xml and
  /storage/roms/genesis/gamelist.xml. Corresponding ROMs exist; references are
  relative. The metadata dates predate the first fork installation.
- Neither system has a game-list fallback in the inspected user-ES locations or
  a recovery directory. /storage/.emulationstation resolves to the same config
  directory as /storage/.config/emulationstation. Under the accepted ES path
  precedence, the ROM-folder lists are the available sources for those entries.
- Both lists were last modified October12 around17:56UTC. File rewrites can
  change these times; they do not establish when the lists were first copied.
  The bounded birth-time query returned no usable values.
- The old backup/restore stamps still report the September30 successful empty
  operations previously corroborated by retained logs. Their dates do not
  describe newly transferred ROMs or copied account configuration.
- The surviving October9 preparation archive's original system.cfg matches the
  original plan's private binding. Four current global RetroAchievements account
  fields are nonempty and exactly equal to that archived pre-preparation copy.
  No values or credential-derived hashes are disclosed. These fields therefore
  existed before that preparation step; their original entry remains unknown.
- The accepted preparation receipt is present. Its19 protected file records
  match the original plan's records; the configured safe payload scope is empty
  in both. This is the recorded protected scope, not proof that the entire card
  or every possible file was empty.
- The three preserved preparation scripts match both the plan's source hashes
  and the retained host scripts reviewed in nova-library-copy.md. The wrapper
  archives local settings and changes two automatic-sync flags; it does not call
  the core's broader alignment routine. Current flags are off, original flags
  were on. No custom autostart or ES script-hook path was present in the two
  inspected locations.

## Limits and correction

A first collector looked for unprefixed RetroAchievements identifiers and
reported missing rows. Those account-only observations are INVALID: system.cfg
uses global.retroachievements.*. A separate corrected read, using identifiers
confirmed from accepted source and historical field names, established the
presence/equality above. The original evidence and correction remain private;
no empty-account conclusion is claimed. Library/stamp observations were not
affected. This is source/forensic readback, not a runtime fixture PASS.

The original computer/Dropbox library has not been compared. A copied game list
remains a strong explanation supported by the owner's stated transfer route,
but this is not proof of the original copy event. Current timestamps do not
identify a writer. The preparation/update evidence narrows later operations;
it cannot rule out every earlier unrecorded action. No further device experiment
is needed for the current explanation. The synthetic VM copy scenario and the
next firmware's clean/retained qualification remain in #565.

Private source/receipts/readbacks: /workspace/tmp/pix565-nova-readonly-20261013/.
All three bounded reads returned0 and exited. No device worker was left running.
