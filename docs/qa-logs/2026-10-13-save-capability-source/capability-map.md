# Preference, launcher, engine, and manager are separate

Source receipt: [source.json](source.json), eight ES files and eighteen
distribution files. Distribution inputs match coordinator `c75b8d1dae` byte for
byte. ES starts at composed `a7dcdbb38009d8d2a81c7c2b4bc1d8c2d0d38a20`.
No installed firmware, Nova config, emulator, or save was read or run here.

| Layer | RetroArch | Dolphin standalone | Flycast standalone |
| --- | --- | --- | --- |
| Selection identity | Emulator `retroarch`; core selected independently, e.g. `flycast` is a RetroArch core | Emulator `dolphin`; GC nogui/Qt and Wii choices are separate cores | Emulator `flycast`, core `flycast-sa` |
| Global preference | `global.autosave` supplies a default, overridden by per-system/per-game values and launch arguments | May remain explicitly saved; launcher does not read it | May remain explicitly saved; launcher does not read it |
| Specific UI option | `EmulatorFeatures::autosave` in `es_features.cfg` controls the override row per core | Shipped features omit `autosave`, so no override row | Shipped features omit `autosave`, so no override row |
| Launcher implementation | `runemu.sh` RetroArch branch parses state arguments; `setsettings.sh:set_autosave` writes `savestate_auto_save`, `savestate_auto_load`, and slot/entry arguments | `start_dolphin_gc.sh` / `start_dolphin_wii.sh` launch the chosen Dolphin frontend, without this preference or ES state-file/slot wiring | `start_flycast.sh` configures selected display/input/achievement options and launches Flycast; no ES `autosave` or state-file/slot wiring |
| Engine capability | Core serialization support and session restrictions still matter; the preference cannot make every core serializable | Manual State::Save/Load exists. Shipped Wayland nogui hotkey patch invokes those methods. This packet makes no claim that Dolphin lacks all engine-native automatic-state options | Separate `Dreamcast.AutoSaveState`, `Dreamcast.AutoLoadState`, and `Dreamcast.SavestateSlot` exist. Engine defaults for the bool options are false, and the inspected GENERIC_X64/SM8550 templates do not set them |
| Frontend manager | `SaveStateRepository::isEnabled` requires `retroarch`, excludes IMAGEVIEWER, and needs a layout; shipped `es_savestates.cfg` contains only this emulator | Rejected by the explicit emulator gate, even if state files or another layout exist | Rejected by the explicit emulator gate, independently of Flycast's native automatic options |
| Normal in-game saves | Core's ordinary game-save path, distinct from state serialization | Memory card/GCI/Wii data, distinct from StateSaves | VMU/game data, distinct from save states |

The UI setting is **AUTO SAVE/LOAD**, not an assertion that every selected
emulator saves its session at exit. Similarly, **SHOW SAVE STATE MANAGER = ALWAYS**
means every eligible launch, not every emulator. The owner's phrase “Save on
exit” describes their observation; it does not identify a core or effective key.
Nova's selected emulator/core and effective values remain **unknown** after the
previous timed-out read reported in the issue. No platform-based inference is made.

## Selection and preference resolution

`FileData::getEmulator` validates an explicit game emulator against that system's
available emulators. Empty, `auto`, or unavailable choices fall back to the system.
`SystemData::getEmulator` accepts an available system choice or resolves the
default core marker/first emulator via `getDefaultEmulator`. Collection items use
their source game's system. Core selection has its own validation/fallback; a
Dreamcast game can use `retroarch/flycast` or `flycast/flycast-sa`, which are
different implementations. This help uses the existing **resolved emulator** getter,
not a platform or core-name substring.

`FileData::getCurrentGameSetting` checks the game's configuration name, then its
source system, then global. Nonempty values other than `auto` stop inheritance.
Thus an explicit per-game `0` remains off even with global `1`. The new help has
no setter/save callback; existing setting serialization, inheritance, and emulator
selection/rebuild callbacks are unchanged. It neither clears preferences nor
migrates them when the selected emulator changes.

## RetroArch contract is already owned by #196

D-UI-057, D-UI-069, and D-UI-083 remain in force. A numbered tile supplies its
state file and entry slot (`-e N`), an auto tile supplies the `.auto` file, and
START NEW GAME supplies `-autosave 0`. The launcher keeps the exit auto-save
decision distinct from the state loaded at entry. Numbered slots are not
renumbered. `es_savestates.cfg` selects this path instead of the historical
parking/restoring fallback. This candidate does not change any of it.

Reuse `tools/last-good-scripts-test` section **v**, around line 2991, for the
existing #196 parser/auto-file/slot controls when the coordinator allocates its
regression run. No duplicate implementation or run is added here. Core serialization,
netplay (which writes auto-state settings off in `set_netplay`), and achievement
restrictions must remain separate observations from the frontend manager's gate.

## Engine-native Flycast capability is real, but is not this preference

Pinned Flycast `5aa091fde632fb332c8d8c34e280d62dc951954c` declares its own options
in [option.cpp](https://github.com/flyinghead/flycast/blob/5aa091fde632fb332c8d8c34e280d62dc951954c/core/cfg/option.cpp).
Its [load/unload paths](https://github.com/flyinghead/flycast/blob/5aa091fde632fb332c8d8c34e280d62dc951954c/core/emulator.cpp)
conditionally load the native slot and save on a loaded game's orderly unload,
subject to content/network/multiboard conditions. A process kill is not proof that
unload ran. The standalone launcher registers a `-9` exit fallback; that fact alone
cannot establish the actual exit path on a given device.

[nullDC.cpp](https://github.com/flyinghead/flycast/blob/5aa091fde632fb332c8d8c34e280d62dc951954c/core/nullDC.cpp)
refuses state loading in hardcore mode; state availability also depends on online,
multiboard, and Maple storage state. The [native GUI](https://github.com/flyinghead/flycast/blob/5aa091fde632fb332c8d8c34e280d62dc951954c/core/ui/gui.cpp)
disables the load control when hardcore is active or a state is absent. This does
not imply every state write is forbidden in hardcore. Native options in retained
configuration must stay independent; enabling ES `global.autosave` does not set
them. No automatic bridge is proposed.

## Dolphin paths and retention need separate proof

Pinned Dolphin `6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4` checks hardcore before
loading in [State.cpp](https://github.com/dolphin-emu/dolphin/blob/6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4/Source/Core/Core/State.cpp).
The distribution additionally patches state names (`002-savestate-names.patch`)
and Wayland nogui hotkeys (`015-wayland-nogui-platform.patch`). Use the **installed,
patched** binary for manual-state/slot evidence, not a stock upstream executable.

The GC launcher replaces `StateSaves` with a link to
`/storage/roms/savestates/gamecube` and moves/links memory-card storage separately.
Its existing `rm -rf ${CONF_DIR}/StateSaves` is a specific reason to cover a real
retained-directory fixture before any launcher change or preservation claim.
Flycast also moves an existing config `data` directory and creates a BIOS/data
link. These are inherited operations, unchanged by this ES-only patch. All future
launcher runs must use a disposable guest with manifests for both canonical and
retained paths; an ordinary-memory-card save is not an exit-state observation.

This packet does not certify those inherited storage migrations as safe or fixed.
It does not authorize running either launcher on owner data.

## Upstream applicability and remaining limits

The upstream ES gate originated in ROCKNIX commit
`b6eb1047bdc75f16b5b4129f7a9e2ae1e2e4a217` (“Only show save states for RA”,
2024-12-06). Removing it would invent manager integration and contradict the
shipped layout. The narrow correction is expectation/help text, not a new
standalone save-state implementation. Another launcher, `dsperate-sa`, already
reads `autosave`, so the global preference is deliberately **not** described as
RetroArch-only. This is a mapping of the three requested emulator families, not
a complete capability inventory of every standalone engine.

[upstream-source.json](upstream-source.json) retains exact public pinned blobs,
SHA256s, URLs, and relevant line excerpts read on 2026-10-13. Initial web search
located Flycast's current implementation; pinned GitHub contents were then read
directly when the web cache missed files. No source was built, executed, or
installed. Source establishes possible paths; only coordinator runtime can prove
exit method, slot/path, restart restoration, ordinary saves, and installed manager
visibility. Hardcore runtime proof is not inferred from a configured flag alone.
