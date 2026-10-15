# Proposed state-only continuation — UNRUN

This is a narrow proposal, not a prepared executable derivative or allocation.
Use the existing revision04 lifecycle source retained under
`../2026-10-15-native-gameplay-correction/revision04/` and source seal
`c9d6faa5bb47950f5c73f947bf03fa925ba2fbdebc8a4d0c5ffb3824ae02379d`.
Keep its single guest, controller identity, shared serial lock, live profile
readback, observed input, first-frame deadline, whole-family deadline and bounded
cleanup. Do not reuse a consumed admission or mutate owner03/source originals.

Can the VM prove this? Yes. Native state creation/loading, settings separation,
ES manager availability and orderly native shutdown are software behavior. Root
records the answer and criteria in the issue, then allocates one fresh owner.

## Dependencies before any execution

Root selects and binds the actual installed image and final reviewed source after
#594 is settled; any candidate helper overlay must have its own exact installed
binding. Preserve the accepted ordinary-save scope on d4af5a rather than silently
claiming it tested a later image. Reuse the already authored homebrew inputs;
no fresh game download, ordinary save score session or puzzle-cell replay.

Before preparing a continuation, make only the necessary source changes in a new
owned revision: remove full packaged GameSettings/immutable Sys copies from
snapshot payloads while retaining source hashes and selected config/state/log
inventories; preserve all needed dynamic data and account for generated files.
Correct the export count guard with an explicit bounded inventory contract. Do
not simply suppress validation or mutate the failed historical exporter. The
old count failure and all-byte supplemental proof remain retained. Root reviews
that exact small diff and derived seals before fresh preparation.

No need to copy either 128 MiB SD image into every state snapshot. The accepted
ordinary saves need no re-extraction. Keep one exact source input binding, and
capture native .s01/.state bytes once per materially changed state plus hashes.
Use the existing live profile status route before input, with no serial bypass.

## Four-launch state sequence

1. **One Wii launch: finish manual restore.** Open a fresh puzzle without an
   ordinary Save and Quit. Through the reviewed actual pad profile select native
   slot 1 (`back,up`), save (`back,rt`), wait for the completed Saved State message
   and record the .s01 identity. Change to the visibly paused scene (`start`),
   then load (`back,lt`). Review a settled restored scene after Decompressing
   State has cleared, and verify resumed input/timer behavior within the existing
   family deadline. Do not count a pending/decompressing frame as completion.
   Orderly shutdown uses a released Back+Start request; if the Wii power event
   leaves this DOL active, a second released request follows the exact shipped
   NoGUI shutdown path. Snapshot while stopped. No ordinary-save claim is added.
2. **Flycast launch 1: global on, native off, manual restore.** Reuse native03's
   recorded global0/native-off baseline. With engines stopped, use the existing
   `global-auto --value 1`; leave native AutoSave/AutoLoad off. Review both actual
   values and the selected standalone core. Capture the ES game options showing
   the RetroArch-only manager remains absent. Launch Tetris 2, reach an observable
   menu scene A without earning or saving a score, native Save State, change to
   a distinct menu scene B, then native Load State and verify settled scene A.
   Record exact selected slot, actual .state path/hash and completed feedback.
   Normal native-menu Exit; check the manually saved state was not rewritten by
   the ES global setting. This directly contrasts with the retained global0 case.
3. **Flycast launch 2: global off, native on, automatic save.** With engines
   stopped, use existing `global-auto --value 0` and `native-auto --value 1`.
   The current Flycast source uses the same config::SavestateSlot for manual and
   automatic state; retain that selected slot rather than assume a separate auto
   filename. First launch may automatically restore the preceding manual state.
   Change to a distinct menu scene C, perform no manual save, and use normal
   native-menu Exit. Require a changed state file/hash and original exit-path
   observations; global stays off. This is the automatic-save witness.
4. **Flycast launch 3: automatic restore.** Cold ES launch with those unchanged
   native options must restore scene C before any manual Load input. Bind frame,
   selected slot/path/hash, real generated options, process identity and launch
   record. Then exit normally; reset native options off and global off while the
   engine is stopped before final export. Avoid a scored game and VMU Save.

The sequence is four launches, not an exhaustive matrix. If a manual load fails
or does not finish, preserve the original failure and stop that acceptance claim;
source investigation is separate from retiming or replaying inputs blindly.

## Exact source constraints already checked

- Dolphin PlatformWayland.cpp uses Hotkey+right trigger for State::Save and
  Hotkey+left trigger for State::Load; actions require release between presses.
  Original owner03 actions used `back,rt` and `back,lt`, 120 ms each.
- Flycast `core/emulator.cpp:682-683` auto-loads config::SavestateSlot;
  `:751-753` unload auto-save calls gui_saveState(false).
- `core/ui/gui.cpp:513` saves config::SavestateSlot and `:666` displays slot+1.
  `core/oslib/oslib.cpp:198-206` uses .state, with _N suffix only for index>0.
  Inspect actual path rather than guessing from the displayed one-based slot.
- Existing launcher routes Dreamcast data to `/storage/roms/bios/dc`; no native
  SavestatePath override was present in native03's selected config. Re-read any
  continuation's actual configuration and resolved paths before asserting this.

Retain source and installed bindings, all original command/controller/lifecycle
results, the new state bytes and hashes, reviewed frames before/save/change/load,
actual global/native settings and no-manager screen. Wrapper success never
substitutes for unobserved native original wait status. No RC claim follows.
