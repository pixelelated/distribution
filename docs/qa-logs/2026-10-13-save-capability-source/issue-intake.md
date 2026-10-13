# Issue #575 intake

Cached issue supplied by coordinator; complete body below. One public comment read through GitHub API on 2026-10-13 (6138380456, updated 2026-10-13T04:41:09Z) confirms the RetroArch-only manager, absent standalone global-setting wiring, and timed-out Nova selection read. No newer owner selection was inferred.

## Owner report — October 13

> Another item I found is that on the RetroAchievements Nova, even though "Save on exit" was selected, it doesn't seem to save the session or show the EmulationStation save state manager. This might be how the emulators for GameCube and Dreamcast work, and if this is the expected behavior, then that's fine, but it is in contrast to what you have with the other retroarch cores.

Refers to the Retroid Pocket Nova. Duplicate report is one issue.

## Current behavior and investigation

The fork's es_savestates.cfg registers the frontend manager layout only for retroarch. Standalone Dolphin and Flycast have separate launchers; those launchers do not currently consume global.autosave. Dolphin's StateSaves folder exists independently of manager integration. Flycast upstream has AutoSaveState/AutoLoadState behavior, so standalone status alone is not a reason to claim the emulator cannot do it. Separate engine capability, configured launcher behavior and frontend manager support.

Already written: existing firmware offers global automatic save/load controls and preserves per-emulator/per-game preferences. Do not overwrite existing memory-card/VMU saves, save states, or enabled account settings while investigating. D-UI-057/#196 owns RetroArch auto-state correctness, which must not regress.

Can this be done on the VM? Yes: inspect exact installed configuration and exercise disposable/homebrew emulator exit/relaunch and frontend manager paths with synthetic save data. The owner report is intake, not the acceptance test. Only scoped read-only device inspection is needed to determine selected emulators; no games, saves, screenshots, input, sync or account operations are implied.

## Acceptance criteria

- [ ] Bind the observed systems to selected emulator/core and effective automatic save/load settings; artifact/source receipt separates global preference, runtime implementation, and manager support.
- [ ] Document and verify behavior for RetroArch, standalone Dolphin and standalone Flycast using disposable VM fixtures: ordinary in-game save, manual state, exit auto-state and manager visibility are separate observations.
- [ ] If the current UI implies unsupported behavior, correct capability gating or help text with EN/FR flow references and exact-source screenshots; do not silently promise session preservation.
- [ ] Any proposed standalone integration proves exit/load/slot/path handling, clean and retained-storage behavior, existing state preservation and relevant hardcore restrictions; otherwise record the supported limitation explicitly and scope enhancement separately.

Track the inconsistency before next-candidate qualification; do not equate lack of automatic states with loss of normal game saves. Related #574 (GameCube achievement recognition, separate issue).
