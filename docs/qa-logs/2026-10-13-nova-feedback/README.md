# Nova account, activity, achievements and state feedback — October 13, 2026

All feedback is tracked in the fork: [#565](https://github.com/pixelelated/distribution/issues/565),
[#574](https://github.com/pixelelated/distribution/issues/574) and
[#575](https://github.com/pixelelated/distribution/issues/575). These are
read-only diagnostic findings, not fixes or clean-install qualification. Private
owner logs/configuration remain outside the repository. No credentials were
printed, no provider request made, and no game launched or state changed.

## Activity provenance (#565)

The September30 restore/backup dates match retained completion records and the
current stamps, rather than establishing copied history. The restore found the
old selected cloud folder absent and treated it as empty; the immediately
following backup transferred0B and reported nothing to transfer. Both completed
successfully, explaining timestamps without a ROM library. This does not prove
who initiated them. The first Nova fork installation was an in-place update over
stock20260901, preserving storage; it was not a clean installation.

Two Recent entries carry positive playcounts and September6/8 lastplayed values,
before that first fork installation. Accepted ES `c8dc72cf9e`,
`CollectionSystemManager.cpp`, includes a game in AUTO_LAST_PLAYED when PlayCount
is greater than"0"; imported metadata can therefore populate Recently Played
without a local launch. Gamelist modification times do not identify their arrival
method. That provenance remains unresolved; copied library metadata, prior
storage and restore must not be asserted as the cause without evidence.

#565 now covers exact artifact/default/first-boot activity isolation as well as
credentials, and retained-upgrade preservation. Selected-file no-account checks
from prior work are not a complete executable image contamination gate.

## GameCube achievements (#574)

Scoped installed readback found9 RVZ games, zero achievement IDs, and9 frontend
“Unable to extract hash” events. The current frontend's GameCube hash path reads
raw disc magic at0x1c; no RVZ decompressor is wired into that reader. This binds
an actual frontend recognition failure to an applicable source limitation.

Dolphin2606 is compiled with RetroAchievements support; its enabled configuration
and nonempty account-field presence were confirmed without displaying or retaining their values in the readback.
In-game awards were not exercised. Do not equate frontend hash failure with lack
of Dolphin support. Upstream RetroArch's RVZ implementation is a reuse lead,
not a reviewed or adopted fix. #574 requires format-aware recognition with
negative/corrupt controls and separate frontend/offline versus Dolphin evidence.

## Save on exit and the manager (#575)

Accepted `SaveStateRepository.cpp` explicitly rejects manager support for an
emulator other than `retroarch`; shipped `es_savestates.cfg` lists only RetroArch.
Standalone Dolphin and Flycast launchers do not consume the global auto-save
setting as equivalent session save/restore behavior. Manual emulator states,
ordinary game saves, automatic exit states and ES manager integration are
separate capabilities.

The targeted Nova emulator-selection read timed out. Its actual selected cores
remain unverified, so platform name alone does not establish which launcher ran.
#575 owns that readback, disposable emulator controls and accurate setting/help
behavior. It does not silently promise full standalone integration. Any visible
repair needs the canonical flow and exact-source reviewed frames.

Authoritative source paths: ES `es-app/src/CollectionSystemManager.cpp`,
`es-app/src/SaveStateRepository.cpp`, `external/libcheevos/cheevos.cpp`,
`external/libcheevos/rcheevos/src/rhash/hash_disc.c`; distribution
`projects/ROCKNIX/packages/ui/emulationstation/config/common/es_savestates.cfg`
and standalone Dolphin/Flycast launchers. Device source
`bc9dfe8141d9561dc1d8502313d00a84c4566ee8`, ES
`c8dc72cf9ec00ab00d6c4a9fcdcea1746c6f1f78`.
