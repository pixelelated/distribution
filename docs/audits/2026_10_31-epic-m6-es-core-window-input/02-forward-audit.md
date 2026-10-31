# Forward audit — M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

- **reviewed-at:** `b1f2908a55` (the distribution worktree at stage A); **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`, the 96 paths of `.qa-scratch/t35/paths.txt`, read by `git -C <W> show` and never from a working tree.
- **Stage B, composed by `tools/t35-02.py` from this template**: every generated section is the named script's output at the pin, and its last line is `generated, asserted: ...`. Each script was seen to exit 1 on three constructed drifts before it was trusted (§ The runs).
- Every proof carries a `proved:` cell: `tree`, `history`, `tool-run`, `fixture`, `guest`, `fix-unit-test`, `fix-walk-pending-image` or `design`. Stage C (the host's cases and builds) and the guest window come after this composition, and their rows say `owed` until they run.

## Coverage

| Path | Lines | Read tier | Inventory tier | Fork stat (vs `bccd715707`) | What | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `es-core/CMakeLists.txt` | 303 | fork-modified | fork-own | +7/-0 | the build lists | tree |
| `es-core/src/AsyncHandle.h` | 57 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/AudioManager.cpp` | 749 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/AudioManager.h` | 86 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/BindingManager.cpp` | 522 | upstream-carried | upstream-carried | -- | the theme bindings | tree |
| `es-core/src/BindingManager.h` | 118 | upstream-carried | upstream-carried | -- | the theme bindings | tree |
| `es-core/src/CECInput.cpp` | 376 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/CECInput.h` | 38 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/FavoriteMusicManager.cpp` | 127 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/FavoriteMusicManager.h` | 27 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/GuiComponent.cpp` | 1540 | upstream-carried | upstream-carried | -- | the component base | tree |
| `es-core/src/GuiComponent.h` | 298 | upstream-carried | upstream-carried | -- | the component base | tree |
| `es-core/src/GunManager.cpp` | 1057 | fork-modified | fork-own | +2/-0 | the light guns | tree |
| `es-core/src/GunManager.h` | 155 | upstream-carried | upstream-carried | -- | the light guns | tree |
| `es-core/src/HelpPrompt.h` | 27 | upstream-carried | upstream-carried | -- | the help prompts | tree |
| `es-core/src/HelpStyle.cpp` | 87 | upstream-carried | upstream-carried | -- | the help prompts | tree |
| `es-core/src/HelpStyle.h` | 31 | upstream-carried | upstream-carried | -- | the help prompts | tree |
| `es-core/src/ImageIO.cpp` | 394 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/ImageIO.h` | 54 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/InputConfig.cpp` | 446 | fork-modified | fork-own | +8/-1 | the input manager and its config | tree |
| `es-core/src/InputConfig.h` | 176 | upstream-carried | upstream-carried | -- | the input manager and its config | tree |
| `es-core/src/InputManager.cpp` | 1552 | fork-modified | fork-own | +5/-2 | the input manager and its config | tree |
| `es-core/src/InputManager.h` | 109 | upstream-carried | upstream-carried | -- | the input manager and its config | tree |
| `es-core/src/LocaleES.cpp` | 427 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/LocaleES.h` | 83 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/Log.cpp` | 322 | fork-modified | fork-own | +19/-40 | the log | tree |
| `es-core/src/Log.h` | 56 | upstream-carried | upstream-carried | -- | the log | tree |
| `es-core/src/LogPolicy.h` | 55 | fork-added | fork-own | +55/-0 | the log | tree |
| `es-core/src/MameNames.cpp` | 461 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/MameNames.h` | 62 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/MultiStateInput.cpp` | 53 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/MultiStateInput.h` | 19 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/Paths.cpp` | 363 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/Paths.h` | 112 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/PowerSaver.cpp` | 122 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/PowerSaver.h` | 84 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Scripting.cpp` | 209 | fork-modified | fork-own | +3/-3 | the script runner | tree |
| `es-core/src/Scripting.h` | 13 | upstream-carried | upstream-carried | -- | the script runner | tree |
| `es-core/src/Sound.cpp` | 115 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Sound.h` | 38 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Splash.cpp` | 337 | upstream-carried | upstream-carried | -- | the splash | tree |
| `es-core/src/Splash.h` | 44 | fork-modified | fork-own | +4/-1 | the splash | tree |
| `es-core/src/TextToSpeech.cpp` | 284 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/TextToSpeech.h` | 64 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/ThemeData.cpp` | 2891 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/ThemeData.h` | 599 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/ThemeVariables.cpp` | 44 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/ThemeVariables.h` | 15 | upstream-carried | upstream-carried | -- | the theme parser | tree |
| `es-core/src/VolumeControl.cpp` | 668 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/VolumeControl.h` | 61 | upstream-carried | upstream-carried | -- | the device and audio layer | tree |
| `es-core/src/Window.cpp` | 1656 | fork-modified | fork-own | +49/-6 | the window and its surfaces | tree |
| `es-core/src/Window.h` | 197 | fork-modified | fork-own | +2/-0 | the window and its surfaces | tree |
| `es-core/src/anim/StoryboardAnimator.cpp` | 237 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/StoryboardAnimator.h` | 192 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/ThemeAnimation.h` | 146 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/ThemeStoryboard.cpp` | 242 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/anim/ThemeStoryboard.h` | 28 | upstream-carried | upstream-carried | -- | the storyboards | tree |
| `es-core/src/animations/Animation.h` | 12 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/animations/AnimationController.cpp` | 38 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/animations/AnimationController.h` | 35 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/animations/LambdaAnimation.h` | 27 | upstream-carried | upstream-carried | -- | the animations | tree |
| `es-core/src/gettext.h` | 300 | upstream-carried | upstream-carried | -- | the rest | tree |
| `es-core/src/guis/GuiDetectDevice.cpp` | 149 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiDetectDevice.h` | 37 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInfoPopup.cpp` | 115 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInfoPopup.h` | 37 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInputConfig.cpp` | 433 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiInputConfig.h` | 72 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiMsgBox.cpp` | 299 | fork-modified | fork-own | +78/-3 | the es-core dialogs | tree |
| `es-core/src/guis/GuiMsgBox.h` | 61 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopup.cpp` | 86 | fork-modified | fork-own | +1/-1 | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopup.h` | 33 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopupKeyboard.cpp` | 533 | fork-modified | fork-own | +14/-14 | the es-core dialogs | tree |
| `es-core/src/guis/GuiTextEditPopupKeyboard.h` | 57 | upstream-carried | upstream-carried | -- | the es-core dialogs | tree |
| `es-core/src/math/Misc.cpp` | 159 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Misc.h` | 40 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Transform4x4f.cpp` | 329 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Transform4x4f.h` | 53 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2f.cpp` | 39 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2f.h` | 73 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2i.cpp` | 1 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector2i.h` | 61 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector3f.cpp` | 21 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector3f.h` | 104 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector4f.cpp` | 107 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/math/Vector4f.h` | 101 | upstream-carried | upstream-carried | -- | the math | tree |
| `es-core/src/playlists/AnimatedGifPlaylist.cpp` | 33 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/playlists/AnimatedGifPlaylist.h` | 18 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/playlists/M3uPlaylist.cpp` | 87 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/playlists/M3uPlaylist.h` | 26 | upstream-carried | upstream-carried | -- | the playlists | tree |
| `es-core/src/watchers/BatteryLevelWatcher.cpp` | 9 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/BatteryLevelWatcher.h` | 21 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/NetworkStateWatcher.cpp` | 21 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/NetworkStateWatcher.h` | 25 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/WatchersManager.cpp` | 203 | upstream-carried | upstream-carried | -- | the watchers | tree |
| `es-core/src/watchers/WatchersManager.h` | 92 | upstream-carried | upstream-carried | -- | the watchers | tree |

generated, asserted: 96 rows, 22575 lines (grep -c rule); read tiers fork-added 1 / fork-modified 12 / upstream-carried 83; inventory fork-own 13 / upstream-carried 83

## The leads

L-01 to L-29 are the brief's § 2 lead table. L-28 and L-29 are T34's PL-05 and PL-04, carried in version 2; § 6 still says *L-01 to L-27*, an erratum. 3.1 to 3.27 are the floor's cases. Each anchor line is checked for its text at the pin.

| Lead | Lines | Family | Owner | Disposition (stage B) | Proof | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| L-01 | `Window.cpp:339-340` against `:334-335`; `:1159-1160`; `:1164` | the queue | this lane (rule 6) | **confirmed at the tree:** the pop is from the back (upstream's, `back()`/`pop_back()` at the base `bccd715707`), **D-UI-093's decided row (`decision-register.md:404`) and the fork's comment at `c1c0d6ddc` both say *the order is the order things happened***, while its own `:1159-1160` says *a toast returned last shows first*: a defect against a decided row; a re-queued toast takes a fresh default duration (`:1164`). A contained fix (pop the front) for the pause | 3.14; G-02; G-03 `CANNOT` | tree |
| L-02 | `Window.cpp:188-207`, `:49-63`, `:1246-1248`; the raw holders in es-app | lifetimes | this lane (the teardown), T18/T20/T34 (the holders) | **confirmed:** `deinit` and `~Window` free no card or popup; the one free is `:1248`. T34's `s2-window.patch` (#1310) is the input: a `weak_ptr` return changes 10 es-app callers and 3 doubles -- **a collision for the pause** (§ 1 i), § The surfaces' last row | Q4; the pause | tree |
| L-03 | `Window.cpp:1262-1274` against `:1278`, `:1296` | lifetimes | this lane (rule 6) | **confirmed:** no lock in `unregisterPostedFunctions`; the two others take it. A contained fix (take the lock) for the pause | 3.17 (TSan) | tree |
| L-04 | `Window.cpp:1554-1637`; `:29` | lifetimes, structure | upstream ROCKNIX's (outside the lanes, D-UI-079) | **confirmed:** four detached workers capture `this` and post back; `:29` reaches into es-app. Recorded as upstream's, not changed; `Window.cpp:29`'s disposition is *recorded* | -- | tree |
| L-05 | `Window.cpp:262-281` | input | upstream's | **confirmed:** four Ctrl chords with the gate commented out on each line. Recorded (cost: a keyboard on a handheld; value: debugging) | -- | tree |
| L-06 | `InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:115` | input (writes) | this lane (rule 6) for `es_input.cfg`; the pause for the rest | **confirmed:** five writes, none atomic, `AtomicFile::` 0 (§ The input); the grep's seven include two read-mode `fopen`s. The `es_input.cfg` write through the fork's `AtomicFile` is a candidate for the pause (D-CLOUD-078's family) | § The input | tree |
| L-07 | `InputManager.cpp:893`, `:1187`, `:1225`, `:1250`; T36's cache | input (reads) | this lane (the read passes `false`), T36 (the cache) | **supported by the tree:** the cache stores misses (`FileSystemUtil.cpp:296`, `:323`, T36's) and `save_file` bypasses it; the hypothesis stands until 3.11 runs; G-01 reads the precondition | 3.11; G-01 | tree |
| L-08 | `InputManager.cpp:1242-1284` | scripts | upstream's; recorded | **confirmed:** synchronous on the interface thread, inside the rebuild's lock when reached from the hot-plug write (§ The locks) | 3.13; G-01's count | tree |
| L-09 | `InputManager.cpp:1101-1108`; `GuiInputConfig.cpp:73`, `:270-281`; `InputConfig.cpp:186-189` | input | T3 (which name the templates read) | **confirmed:** two names, `hotkey` and `hotkeyenable`; no verdict here | 3.12 | tree |
| L-10 | `InputManager.cpp:946`, `:960` | input | this lane (rule 6) | **confirmed:** both lines read `configNode` before `configNode = item` (`:947`, `:961`). A one-word fix (log `item`) for the pause | 3.10 | tree |
| L-11 | `WatchersManager.cpp:181-199` and the entry points | locks | this lane (#1283's es-core half) | **confirmed:** the list lock is held across every probe; five interface-thread entry points wait (§ The locks). The fix (snapshot, then probe unlocked, re-validating) for the pause | 3.1, 3.2, 3.3 | tree |
| L-12 | `GuiMsgBox.cpp:116-134`, `:246-264` | dialogs | upstream's; the callers pick their labels | **confirmed:** the third branch binds back to the last button; an unconfigured pad's any button fires it (`:257`). Read; G-04 and G-05 frame it | 3.18; G-04; G-05 | tree |
| L-13 | `GuiTextEditPopupKeyboard.cpp:14`, `:220` against `MenuComponent.cpp:14` (T34's) | dialogs | this lane (the define) | **confirmed:** one macro name, two values in two files. A rename for the pause (the keyboard's own name); the value is the keyboard's design | 3.19; G-06 | tree |
| L-14 | `GuiTextEditPopupKeyboard.cpp:392-397`, `:453-454`, `:491-496`; `GuiTextEditPopup.cpp:34` | dialogs | the pause (the lanes' fields: the cloud folder, the Wi-Fi key) | **confirmed:** `x` and CLEAR commit `""` and close with no question | G-06 | tree |
| L-15 | `GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14` | dialogs | Backlog #1192 | **confirmed:** no masking parameter in either constructor. Deferred to #1192 | -- | tree |
| L-16 | `GuiMsgBox.cpp:44`, `:234`, `:240` | words | upstream's | **confirmed:** three `say(` calls (TTS compiled out on the image); recorded | 3.20 | tree |
| L-17 | `GuiInputConfig.cpp:134` | words | this lane (rule 6) | **confirmed:** the subtitle's number is the SDL instance id plus one | 3.21; G-08 | tree |
| L-18 | `Scripting.cpp:88-149`, `:169-178` | scripts | this lane (rule 6) with T2 (FD-9/FD-19) | **confirmed:** quoting only on a space, `"` stripped, `$`/backtick unquoted to `/bin/sh -c`; every file in a per-event folder runs (§ The scripts) | 3.4, 3.5, 3.6 | tree |
| L-19 | `Scripting.cpp:158-207`; `WatchersManager.cpp:29-53` | scripts | time to play | **confirmed:** three folder listings and three directory scans per event; priced on the guest (the retro's time-to-play) | the guest | tree |
| L-20 | `InputManager.cpp` `configureEmulators` (`:1474-1488`) | scripts | T2 (the launch path), T3 (the templates) | **contradicted at the pin for es-core:** the blob is `-pNindex <int> -pNguid <hex>`, no device name (`:1481-1482`); built unconditionally at `FileData.cpp:547` (T2's). The quoting half is where a name enters, not here | -- | tree |
| L-21 | `Window.cpp:743-745`, `:999-1003`; the eight `mHelp->` lines | help bar | read | **confirmed:** no Window bar under a second full-screen page; none of the eight calls `setOpacity`, so batocera's guard has no caller here | G-04 | tree |
| L-22 | `.claude/rules/es-native-ui.md:30` against `Window.cpp:1192` (the rule's line is checked by `t35-includes.py`) | record | the coordinator's sweep | **confirmed:** *top-right progress card* against a centred card; § The structure | -- | tree |
| L-23 | `ThemeData.cpp:745-856`, `:1094-1150` | structure | upstream's | **read:** the throw/warn asymmetry recorded; parse-only on the host | 3.26 | tree |
| L-24 | `InputManager.cpp:792-800` | input | this lane (rule 6) | **confirmed:** a `new SDL_Event` per F4 press, never freed (`SDL_PushEvent` copies). A one-line fix (a stack event) for the pause | -- | tree |
| L-25 | `guis/GuiTextEditPopupKeyboard.h` | record | § The merge debt | **confirmed:** byte-identical to `cada856d86`; a footnote | -- | tree |
| L-26 | `es-core/CMakeLists.txt` at T21's `3ae9610b0` | structure | the integration (§ 1 h) | **confirmed:** five added lines in four hunks; named in the hand-back | -- | tree |
| L-27 | `Window.cpp:777-779`, `:1091-1138`; T33's and T2's | lifetimes | this lane's half, T33's, T2's | **confirmed (the window's half):** the start from `render()` on idle time alone, with no way for a page to refuse; § The lifetimes' three halves | 3.27; G-09 | tree |
| L-28 | `Window.cpp:743-745`, `:1005-1078`; T34's chain | help bar | read; the pause with G-11 | **read, then seen:** the window's collection drops a repeated icon (`:1023`), and its dpad merge compares the wrong way (`:1032-1033`, the seat's G-1, verified: two complementary halves do not merge, and an unrelated icon sharing the action text is replaced); it adds no prompt. G-11 framed the tabbed SCRAPEUR page with only FERMER and RETOUR while the non-tabbed PARAMÈTRES AUDIO page shows CHANGER and CHOISIR through the same window: the prompts are lost before the window | 3.16; G-11 | tree; guest (image) |
| L-29 | `Window.cpp:1005-1078`; `ComponentList.cpp:568` (T34's) | help bar | read | **read:** a key `setHelpPrompts` does not know passes through untouched and sorts with index 0 (`:1062-1074`); it neither translates nor drops it -- whether its icon draws is `HelpComponent`'s (T34's) | 3.16 | tree |

**The floor's cases** (the seven candidates and 3.27 in bold; each run against the unfixed extract first -- stage C wrote twelve, S0 the ten no stream holds (`stage-e/s0-floor.txt`, each seen to fail on a constructed mutation, `stage-e/s0-mutations.txt`); `proved: design` until a run holds it):

| Case | Anchor | What it checks | Expected at the pin | Run | proved: |
| --- | --- | --- | --- | --- | --- |
| **3.1** | `watchers/WatchersManager.cpp:196` | a probe that sleeps; `ResetComponent` from a second thread waits for it | FAIL at the pin expected (L-11) | FAIL at the pin, stage C and S0 (`ResetComponent returned after 1496 ms` / `1495 ms`) | tool-run |
| 3.2 | `watchers/WatchersManager.cpp:86` | ASan: unregister during a running probe | PASS at the pin (the lock spans the probe); the guard PL-01's fix keeps | PASS at the pin, no report (`SAN asan-watchers (-fsanitize=address): rc 0`, S0) | tool-run |
| 3.3 | `watchers/WatchersManager.cpp:151` | TSan: `mRunning` written and read unsynchronised | a race report expected | FAIL at the pin, a race (`SAN tsan-watchers ... rc 66`) | tool-run |
| **3.4** | `Scripting.cpp:109` | `a$(id)b.zip` unquoted, `a b.zip` quoted, `"` stripped | FAIL expected (L-18) | FAIL at the pin | tool-run |
| **3.5** | `Scripting.cpp:172` | a `notes.txt` in a per-event folder handed to the executor | FAIL expected (L-18) | FAIL at the pin (recorded: PL-18, ruling 9) | tool-run |
| 3.6 | `Scripting.cpp:202` | the single-script pass filters by extension | PASS expected (contract) | PASS at the pin (S0) | tool-run |
| 3.7 | `InputConfig.cpp:188` | `mapInput` lower-cases; the XML round trip keeps every mapping | PASS expected (contract) | PASS at the pin (S0, two cases) | tool-run |
| 3.8 | `InputConfig.cpp:353` | `buttonLabel` returns an unknown key unchanged | PASS expected (contract) | PASS at the pin (S0) | tool-run |
| 3.9 | `InputConfig.cpp:347` | `AssignActionButtons` swaps once and is idempotent | PASS expected (contract) | PASS at the pin (S0) | tool-run |
| **3.10** | `InputManager.cpp:960` | the two lines print empty attributes | FAIL expected (L-10) | FAIL at the pin | tool-run |
| **3.11** | `InputManager.cpp:893` | miss, `save_file`, `exists` again: false while the miss is cached | FAIL expected if the cache holds (L-07) | FAIL at the pin | tool-run |
| 3.12 | `InputManager.cpp:1107` | `select` copied to `hotkey` | PASS expected (documents the two names) | PASS at the pin (S0) | tool-run |
| 3.13 | `InputManager.cpp:1262` | every `onfinish` command handed to the executor, synchronously | PASS expected (contract) | PASS at the pin (S0) | tool-run |
| **3.14** | `Window.cpp:340` | queue [A, B] under a card: B then A; the re-queued duration | FAIL expected (L-01) | FAIL at the pin (the order); the duration case PASS (the contract, ruling 2) | tool-run |
| 3.15 | `Window.cpp:298` | the duration's three branches | PASS expected (contract) | PASS at the pin | tool-run |
| 3.16 | `Window.cpp:1036` | the dedup, the merge, the sort | PASS expected (contract) | stage E S2 | design |
| 3.17 | `Window.cpp:1267` | TSan: unregister against a post | a race report expected (L-03) | FAIL at the pin, a race (`SAN tsan-posts ... rc 66`) | tool-run |
| 3.18 | `guis/GuiMsgBox.cpp:125` | the three accelerator branches in the text | PASS expected (text) | stage E S1 | design |
| **3.19** | `guis/GuiTextEditPopupKeyboard.cpp:220` | the macro defined in two files with two factors | FAIL expected (L-13) | FAIL at the pin (re-shaped in S8, ruling 3) | tool-run |
| 3.20 | `guis/GuiMsgBox.cpp:240` | three `say(` in the constructor | recorded (L-16) | PASS at the pin, recorded (S0) | tool-run |
| 3.21 | `guis/GuiInputConfig.cpp:134` | `getDeviceId() + 1` is the argument | recorded (L-17) | stage E S8 | design |
| 3.22 | `guis/GuiInfoPopup.cpp:98` | the fade's alpha curve and `mRunning` | PASS expected (contract) | PASS at the pin (S0) | tool-run |
| 3.23 | `Log.cpp:60` | every batch reaches the file (#178) | PASS expected (the natural first binary) | stage E S7 | design |
| 3.24 | `FavoriteMusicManager.cpp:115` | the rewrite is truncate-then-write | recorded (L-06) | PASS at the pin, recorded (S0) | tool-run |
| 3.25 | `MameNames.cpp:6` | a malformed file: warned or thrown | recorded | PASS at the pin, recorded (S0) | tool-run |
| 3.26 | `ThemeData.cpp:1094` | parse-only; the asymmetry recorded | no host case (L-23) | no host case (parse-only), recorded | design |
| **3.27** | `Window.cpp:778` | T33's `pl25-screensaver.py`, unchanged | FAIL at the pin expected (#1305) | FAIL at the pin (`heap-use-after-free ... FileData::getImagePath`); stays FAIL until T33's or T2's half (ruling 12) | tool-run |

generated, asserted: 29 leads (24 confirmed at the tree, 1 contradicted, the rest read or supported), 27 floor cases anchored, 22 run

## The surfaces

| Site | Kind | Function | Container | Lock | What it does | Invariant | Proof or frame | proved: |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Window.h:123` | container | -- | the card vector | the lock below | raw pointers the window `new`s at `:1168` and frees at `:1248`; the caller keeps the same raw pointer | a card is owned by the window and freed only once `isRunning()` is false | Q4's lifetimes table; L-02 | tree |
| `Window.h:133` | container | -- | the posted functions | the lock below (not in `unregisterPostedFunctions`) | each a `std::function` and an owner token `void* container` (`:127-131`) | a post runs once, on the interface thread, at the next update | L-03 | tree |
| `Window.h:135` | container | -- | the toasts on screen | taken where they are removed under a card or a song; not in `update`/`render` | raw `GuiInfoPopup` pointers, top-centred, stacked | one floating surface at a time with the cards (D-UI-093) | G-02 | tree |
| `Window.h:154` | container | -- | the toast queue | the lock below | pairs of words and a duration in ms (`:153`) | nothing is dropped (D-UI-093's sentence) | 3.14 | tree |
| `Window.cpp:293` | lock | -- | the queue, the cards, the posts | -- | one file-static mutex | every enqueue and dequeue of the queue, the cards and the posts takes it, except `unregisterPostedFunctions` | Q3's locks table | tree |
| `Window.cpp:311` | enqueue | displayNotificationMessage | the toast queue | taken (`:313`) | `push_back` of the words with `notificationDuration(duration)` (`:298-309`: `<= 0` is the display-titles setting within 2..120 s, else 10 s) | kept: any thread may call it | 3.15 | tree |
| `Window.cpp:324` | dequeue | processNotificationMessages (update `:466`) | the queue -> the popups | taken (`:326`) | returns while any card is up (`:336-337`); takes the **back** of the queue (`:339-340`), builds a `GuiInfoPopup`, lays out | one surface at a time: kept; *the order is the order things happened* (`:334-335`): **not kept** -- the newest first (L-01) | 3.14; G-02 (the toast after the card); G-03 `CANNOT` | tree |
| `Window.cpp:353` | free | stopNotificationPopups | the popups | the caller's (`:1165` holds it) | deletes every popup and clears the vector | kept: called with the lock from the card's creation | -- | tree |
| `Window.cpp:365` | free | updateNotificationPopups (update `:557`) | the popups | not taken | updates each popup, deletes one whose fade has ended (`:373-379`), lays out | kept while every card is created on the interface thread (each caller at the pin does; a read, Q4) | Q4's caller read | tree |
| `Window.cpp:396` | layout | layoutNotificationPopups | the popups | the caller's | stacks from 0.02 H with a 0.02 H gap, a fading popup sliding up by its eased height | kept | G-02 | tree |
| `Window.cpp:418` | free + enqueue | processSongTitleNotifications (update `:465`) | the popups, the queue | taken (`:427`), released before the enqueue (`:441`) | removes an on-screen song toast, then queues the new title through `displayNotificationMessage` (`:442`) | kept: a song toast queues like any other | -- | tree |
| `Window.cpp:782` | draw | render | the popups, the cards | the cards' pass takes it (`:1179`); the popups' loop does not | popups then cards, both only while no screensaver draws (`:782-788`) | kept: the screensaver hides both | G-09 | tree |
| `Window.cpp:1146` | read | hasAsyncNotifications | the card vector | taken (`:1148`) | true while any card is queued, lingering or fading (`.h:100-101`) | kept | -- | tree |
| `Window.cpp:1152` | enqueue | createAsyncNotificationComponent | the cards; the queue | taken (`:1154`) | a toast on screen goes back on the queue with `notificationDuration(-1)` (`:1164`) -- **a fresh default duration, not its remainder** -- and the popups stop (`:1165`); the card is `new`ed and its raw pointer returned (`:1168-1174`) | one surface at a time: kept; the toast's words: kept whole | 3.14's second half; G-02 | tree |
| `Window.cpp:1177` | layout + draw | renderAsyncNotifications | the cards | taken for the whole pass (`:1179`) | each card centred, `posX = W*0.5 - w*0.5` (`:1192`), from 0.02 H (`:1183`), stacked by height + 0.01 W (`:1194`, `:1231`); fades in place (`:1217-1221`), slides up under a clip when closing (`:1203-1215`) | the position re-applied every frame agrees with the component's own (next row) | G-02's two edges | tree |
| `components/AsyncNotificationComponent.cpp:112` (T34's) | position (T34's) | AsyncNotificationComponent ctor | the card | -- | the card's own position before its first render, centred at 0.02 H (`:112-113`); its width `max(text, 0.9 W)` (`:62-64`); the comment `:110-111` asks the two to agree | kept at the pin: `:1192` and `:112` compute the same x | G-02 measures the edges at 640 | tree |
| `Window.cpp:1236` | free | updateAsyncNotifications (update `:556`) | the card vector | taken (`:1238`) | **the one place a card is freed** (`:1246-1248`), once `isRunning()` is false | kept while the caller stops using its raw pointer before the card ends; `deinit` (`:188-207`) and `~Window` (`:49-63`) never free a card, a popup or the queue (L-02) | Q4 | tree |
| `Window.cpp:1262` | free | unregisterPostedFunctions | the posted functions | **not taken** | erases the owner's posts while iterating `mFunctions` (`:1267-1273`) | **not kept**: `postToUiThread` (`:1278`) and `processPostedFunctions` (`:1296`) take the lock (L-03) | 3.17 (TSan) | tree |
| `Window.cpp:1276` | enqueue | postToUiThread | the posted functions | taken (`:1278`) | appends the function and its owner token, and wakes a sleeping window (`:1284-1289`) | kept; it promises nothing to a poster that dies before the drain (L-03, T34 L-12) | Q4 | tree |
| `Window.cpp:1292` | dequeue | processPostedFunctions (update `:464`) | the posted functions | taken to copy and clear (`:1296-1303`), released to run | runs each copied function under `TRYCATCH` (`:1305-1306`) | kept: a post may post again without a deadlock | -- | tree |
| T34's `stage-e/s2-window.patch` (#1310) | held patch | createAsyncNotificationComponent, updateAsyncNotifications | the card vector | taken, as now | the window owns each card through a `shared_ptr` whose deleter frees it on the interface thread; the caller gets a `weak_ptr`; a stopped card is retired until the window holds the last reference | would make the card's free safe against a holder's late use (L-02's half); **changes `createAsyncNotificationComponent`'s return type**, so the 10 callers in es-app (`ContentInstaller.cpp:60`, `ProxyCards.cpp:215`, `:257`, `:514`, `ThreadedBluetooth.cpp:15`, `:72`, `ThreadedCloudSync.cpp:46`, `ThreadedHasher.cpp:126`, `guis/GuiMenu.cpp:11717`, `guis/GuiUpdate.cpp:162`: five lanes) and the three doubles (`tests/app-unit/fakes/Window.h:11`, `ProxyCardsTests.cpp:154`, `tests/hasher-offline-index.py:65`) change with it | proposed for the pause: adopted into a stage-E stream only with its callers' half named for their owners, else a collision named (§ 1 i) | design |
| T34's `stage-e/s3-msgbox.patch` (S3, 06:12; Q6) | held patch | `GuiMsgBox` constructor | -- (the dialog's height) | -- | removes `GuiMsgBox`'s #48 workaround -- the height measured again at the drawn width (`guis/GuiMsgBox.cpp:167-202` at the pin) -- because T34's `TextComponent` fix (#1315, D-UI-130) measures at the width it draws at; proven by T34 on a scratch copy of the pin's file, not applied | **ordered after #1315**: applied without T34's `TextComponent` change it returns #48 (the OK button over the message on a small panel); it touches one of the 96 and depends on a file of T34's 80, so it lands with T34's fix or after it, at the integration | a collision named for the pause (§ 1 i's family): not adopted by this lane; G-04 and G-11 frame the pin's dialog either way | design |

generated, asserted: 22 rows: 5 containers and the lock, 15 sites (one of them T34's component's, outside the 96), and T34's two held patches

**The queue's order (`:339-340`).** The queue drains **newest first**. The pop is upstream's: the base `bccd715707` pops from the back at its `:322-323`. **D-UI-093's decided row says it plainly** (`decision-register.md:404`: *Nothing is dropped; the order is the order things happened.*), as does the fork's comment (`c1c0d6ddc`, `:334-335`). The fork's own re-queue comment (`:1159-1160`) relies on the opposite. **Disposition: a defect against a decided row, contained in `processNotificationMessages`**, the order cited and not re-argued (`decision-register.md` § Read it when), proposed for the pause as a rule-6 fix (pop the front, and reverse the re-queue loop so a returned toast keeps its place). 3.14's FAIL line at stage C is the evidence. G-03 is `CANNOT`.

**The re-queued toast's duration (`:1164`).** A toast taken off the screen by a new card comes back with `notificationDuration(-1)`, a fresh default, not its remainder. **Disposition: by design, recorded.** A toast half-read and then re-shown whole costs the player seconds and loses no words. The pause may rule otherwise (a register row, brief § 9).

**F-ES-24** (the 2026-09-25 audit `02:199`, Low, never dispositioned): every toast waits while *any* card is up (`:336-337`), including the hasher's minutes-long upstream card that D-UI-079 keeps as upstream has it. **Disposition: stands as recorded, with a bound proposed for the pause.** It is the one surface D-UI-093 and D-UI-078 together did not decide, so it is put to the coordinator as brief § 9's first register row, not decided here.

**Item 13, the card's position:** `:1183` (0.02 H from the top) and `:1192` (centred) are re-applied every frame. They agree with the component's own first position (`AsyncNotificationComponent.cpp:112-113`, T34's) and its width `max(text, 0.9 W)` (`:62-64`). G-02 measures the edges at 640 (x 32 and x 608).

## The input

**The write sites** (the writes grep's 9 hits less the two CMake registrations `:122`, `:257`; `AtomicFile::` 0):

| Site | Kind | File | Mechanism | Atomic | A cut file reads as | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `InputManager.cpp:1225` | write | `es_input.cfg` (`getConfigPath()`) | pugixml `save_file`: the path opened for writing and the document written in place | no | `load_file` fails: at load `tryLoadInputConfig` logs `Error parsing input config` and returns false (`:899-903`), the pad reads as unconfigured; at the next write the merge is skipped (`:1191-1193`) and the file is rewritten with that one device | tree |
| `InputManager.cpp:1232` | write | `es_last_input.cfg` (`getTemporaryConfigPath()`, `:1291-1293`) | pugixml `save_file`, in place; the last device alone, *so that people can easily share their config* (`:1227`) | no | nothing in es-core or es-app reads it back (the two lines that name it are `:1231`, `:1293`); a cut file is a cut share | tree |
| `FavoriteMusicManager.cpp:71` | write | the favourites file (`getFavoriteMusicFilePath()`) | `std::ofstream`, `std::ios::app`: one `path;name` line appended | no (an append) | a cut last line: `readAllLines` (`:34`, `:89`) returns it as one more line that matches no song | tree |
| `FavoriteMusicManager.cpp:115` | write | the favourites file | `std::ofstream`, `std::ios::trunc` then the remaining lines (`:121-123`); the last removal deletes the file instead (`:104-106`) | no | the file emptied or cut at a line: favourites lost from that line on, with no error | tree |
| `Log.cpp:179` | write | the log (`es_log.txt`) | the member, opened `std::ios::out \| std::ios::trunc` at `:46`; the worker flushes per batch (`:98`, `:147`) | no (a log, rewritten each start) | a shorter log; nothing reads it back (#178's proof is the batch reaching the file) | tree |
| `AudioManager.cpp:539` | read | a song file | `fopen(..., "r")`: **a read**, counted by the grep's `fopen\(` alternation | -- | -- | tree |
| `AudioManager.cpp:610` | read | a song file (its ID3 tag) | `fopen(..., "r")`: **a read**, as above | -- | -- | tree |

**Every `exists(` of an input file** (none passes `false`; the § 5 reads run: 41 `FileSystem::exists(` lines, 0 uncached):

| Site | File checked | Writer | Cache | proved: |
| --- | --- | --- | --- | --- |
| `InputManager.cpp:420` | the SDL mapping files (`gamecontrollerdb.txt`, shipped and user) | none in ES | **WIN32 only**: the block `:404-483` is `#if WIN32`; it never runs on the device | tree; 3.11 at stage C |
| `InputManager.cpp:893` | `es_input.cfg` (`tryLoadInputConfig`) | `:1225` | cached; a miss is remembered, and `loadInputConfig` after a write (`:1239`) reads it | tree; 3.11 at stage C |
| `InputManager.cpp:1187` | `es_input.cfg` (`writeDeviceConfig`'s merge) | `:1225` | cached; a remembered miss skips the merge and the save keeps only this device (L-07) | tree; 3.11 at stage C |
| `InputManager.cpp:1250` | `es_input.cfg` (`doOnFinish`) | `:1225` | cached; a remembered miss skips the `onfinish` commands written a line earlier | tree; 3.11 at stage C |
| `guis/GuiDetectDevice.cpp:127` | `es_input.cfg` (the detect page's first-run skip) | `InputManager.cpp:1225` | cached | tree; 3.11 at stage C |

**3.11, the cache's answer, read:** `exists(p)` with the cache on (`Settings.cpp:155`, T36's) asks the cache first (`FileSystemUtil.cpp:1127-1131`) and on a miss stores what `stat64` found, **absence included** (`:296`, `:306`, `:323`); `pugi::xml_document::save_file` writes through `fopen`, never through `Utils::FileSystem`, so nothing clears the entry. On a device whose `es_input.cfg` was absent at the first check, every later `exists(` of it in the session reads false until a cache reset. The unit case 3.11 proves the sequence at stage C; G-01 reads whether the user file exists before any configuration on the image (L-07's precondition). For T36's `FileSystemUtil`: the cache remembers misses; a writer outside `Utils::FileSystem` is invisible to it.

**The two hotkey names:** the SDL-mapping fallback copies `select` to **`hotkey`** (`InputManager.cpp:1105-1107`); the configuration page maps **`HotKeyEnable`** (`GuiInputConfig.cpp:73`, `:273`, `:279`), stored as `hotkeyenable` (`InputConfig.cpp:188`). Which one the launch scripts read is T3's templates; the two names are a fact of these lines (L-09, 3.12). `proved: tree`.

**`doOnFinish`'s `<command>`** (`:1242-1284`): every `<inputAction type="onfinish">` `<command>` text runs through `ProcessStartInfo(tocall).run()` at `:1272`, **synchronously, on the interface thread**, from `writeDeviceConfig` (`:1238`); a non-zero exit is a `LogWarning` (`:1277`). The shipped `es_input.cfg`'s `inputAction` count is G-01's line (owed). `proved: tree`.

**The hot-plug rebuild's cost:** a pad added (`:813`) or removed (`:864`) rebuilds every joystick on the interface thread (`:852`, `:875`): the joystick subsystem quit and re-initialised (`:376-382`, `:402`), every device reopened (`:517-`), each configuration re-read from `es_input.cfg` (`loadInputConfig`, `:583`), and an SDL-mapped device written back (`:605`, the hot-plug write); the mapping-file pass and the 500 ms settle poll are WIN32-only (`:404-483`). One file parse per pad per event; G-10 is `CANNOT` (no pad on the guest). `proved: tree`.

**The controllers blob, for T3's half:** `configureEmulators` (`:1474-1488`) writes `-pNindex <int> -pNguid <hex>` per seat and **no device name**; the GUID string is SDL's hex. The quoting T2 FD-6/FD-7 describe is where a name enters, not here; the blob is built on every launch (`FileData.cpp:547`, T2's) whether `includeControllers` is set or not (L-20). `proved: tree`.

generated, asserted: 7 write-site rows (5 writes, 2 reads the grep counts), 5 exists rows; the writes grep 9 hits

## The locks

**The grep:** `git grep -n -E 'std::(recursive_|shared_|timed_)?mutex|lock_guard|unique_lock|scoped_lock|shared_lock|\.lock\(\)|\.unlock\(\)|condition_variable'` over the 96 at the pin.

| Site | Kind | Lock | Function | proved: |
| --- | --- | --- | --- | --- |
| `InputManager.cpp:52` | declaration | mJoysticksLock | -- | tree |
| `InputManager.cpp:200` | acquire (RAII) | mJoysticksLock | InputManager::getNumJoysticks | tree |
| `InputManager.cpp:227` | acquire (manual) | mJoysticksLock | InputManager::clearJoysticks | tree |
| `InputManager.cpp:242` | release (manual) | mJoysticksLock | InputManager::clearJoysticks | tree |
| `InputManager.cpp:485` | acquire (manual) | mJoysticksLock | InputManager::rebuildAllJoysticks | tree |
| `InputManager.cpp:623` | release (manual) | mJoysticksLock | InputManager::rebuildAllJoysticks | tree |
| `InputManager.cpp:1343` | acquire (RAII) | mJoysticksLock | InputManager::computePlayersConfigs | tree |
| `InputManager.cpp:1494` | acquire (manual) | mJoysticksLock | InputManager::updateBatteryLevel | tree |
| `InputManager.cpp:1520` | release (manual) | mJoysticksLock | InputManager::updateBatteryLevel | tree |
| `Log.cpp:18` | include | -- | -- | tree |
| `Log.cpp:70` | acquire (RAII) | mMutex | AsyncLogger::close | tree |
| `Log.cpp:104` | acquire (RAII) | mMutex | AsyncLogger::enqueue | tree |
| `Log.cpp:122` | acquire (RAII) | mMutex | AsyncLogger::workerLoop | tree |
| `Log.cpp:187` | declaration | mMutex | -- | tree |
| `Log.cpp:188` | declaration | mMutex | -- | tree |
| `Scripting.cpp:20` | declaration | mScriptQueueLock | -- | tree |
| `Scripting.cpp:21` | declaration | mScriptQueueLock | -- | tree |
| `Scripting.cpp:29` | acquire (RAII) | mScriptQueueLock | executeCommandsThread | tree |
| `Scripting.cpp:40` | release (manual) | mScriptQueueLock | executeCommandsThread | tree |
| `Scripting.cpp:60` | acquire (RAII) | mScriptQueueLock | pushCommand | tree |
| `Scripting.cpp:78` | acquire (RAII) | mScriptQueueLock | exitScriptingEngine | tree |
| `TextToSpeech.cpp:27` | acquire (RAII) | mMutex | TextToSpeech::SpeakThread | tree |
| `TextToSpeech.cpp:41` | release (manual) | mMutex | TextToSpeech::SpeakThread | tree |
| `TextToSpeech.cpp:76` | `weak_ptr::lock`, not a mutex | -- | TextToSpeech::getInstance | tree |
| `TextToSpeech.cpp:256` | acquire (RAII) | mMutex | TextToSpeech::say | tree |
| `TextToSpeech.h:12` | include | -- | -- | tree |
| `TextToSpeech.h:48` | declaration | mMutex | -- | tree |
| `TextToSpeech.h:49` | declaration | mMutex | -- | tree |
| `ThemeData.cpp:716` | acquire (RAII) | _lock | ThemeFileCache::getXmlDocument | tree |
| `ThemeData.cpp:737` | acquire (RAII) | _lock | ThemeFileCache::clear | tree |
| `ThemeData.h:594` | declaration | _lock | -- | tree |
| `VolumeControl.cpp:13` | include | -- | -- | tree |
| `VolumeControl.cpp:199` | acquire (RAII) | mLock | PulseAudioControl::WaitEvent | tree |
| `VolumeControl.cpp:205` | declaration | mLock | -- | tree |
| `VolumeControl.cpp:206` | declaration | mLock | -- | tree |
| `VolumeControl.cpp:254` | `weak_ptr::lock`, not a mutex | -- | VolumeControl::getInstance | tree |
| `Window.cpp:293` | declaration | mNotificationMessagesLock | -- | tree |
| `Window.cpp:313` | acquire (RAII) | mNotificationMessagesLock | Window::displayNotificationMessage | tree |
| `Window.cpp:326` | acquire (RAII) | mNotificationMessagesLock | Window::processNotificationMessages | tree |
| `Window.cpp:427` | acquire (RAII) | mNotificationMessagesLock | Window::processSongTitleNotifications | tree |
| `Window.cpp:441` | release (manual) | mNotificationMessagesLock | Window::processSongTitleNotifications | tree |
| `Window.cpp:1148` | acquire (RAII) | mNotificationMessagesLock | Window::hasAsyncNotifications | tree |
| `Window.cpp:1154` | acquire (RAII) | mNotificationMessagesLock | Window::createAsyncNotificationComponent | tree |
| `Window.cpp:1179` | acquire (RAII) | mNotificationMessagesLock | Window::renderAsyncNotifications | tree |
| `Window.cpp:1238` | acquire (RAII) | mNotificationMessagesLock | Window::updateAsyncNotifications | tree |
| `Window.cpp:1278` | acquire (RAII) | mNotificationMessagesLock | Window::postToUiThread | tree |
| `Window.cpp:1296` | acquire (manual) | mNotificationMessagesLock | Window::processPostedFunctions | tree |
| `Window.cpp:1303` | release (manual) | mNotificationMessagesLock | Window::processPostedFunctions | tree |
| `watchers/WatchersManager.cpp:5` | declaration | mNotificationLock | -- | tree |
| `watchers/WatchersManager.cpp:7` | declaration | mWatchersLock | -- | tree |
| `watchers/WatchersManager.cpp:35` | acquire (RAII) | mThreadLock | WatchersManager::pause | tree |
| `watchers/WatchersManager.cpp:48` | acquire (RAII) | mThreadLock | WatchersManager::resume | tree |
| `watchers/WatchersManager.cpp:66` | acquire (RAII) | mWatchersLock | WatchersManager::RegisterComponent | tree |
| `watchers/WatchersManager.cpp:78` | acquire (RAII) | mWatchersLock | WatchersManager::UnregisterComponent | tree |
| `watchers/WatchersManager.cpp:94` | acquire (RAII) | mWatchersLock | WatchersManager::ResetComponent | tree |
| `watchers/WatchersManager.cpp:108` | acquire (RAII) | mNotificationLock | WatchersManager::RegisterNotify | tree |
| `watchers/WatchersManager.cpp:114` | acquire (RAII) | mNotificationLock | WatchersManager::UnregisterNotify | tree |
| `watchers/WatchersManager.cpp:128` | acquire (RAII) | mNotificationLock | WatchersManager::NotifyComponentChanged | tree |
| `watchers/WatchersManager.cpp:143` | acquire (RAII) | mWatchersLock | WatchersManager::~WatchersManager | tree |
| `watchers/WatchersManager.cpp:165` | acquire (RAII) | mThreadLock | WatchersManager::run | tree |
| `watchers/WatchersManager.cpp:181` | acquire (RAII) | mWatchersLock | WatchersManager::run | tree |
| `watchers/WatchersManager.h:4` | include | -- | -- | tree |
| `watchers/WatchersManager.h:35` | acquire (RAII) | mWatchersLock | WatchersManager::GetComponent | tree |
| `watchers/WatchersManager.h:77` | declaration | mWatchersLock | -- | tree |
| `watchers/WatchersManager.h:80` | declaration | mNotificationLock | -- | tree |
| `watchers/WatchersManager.h:83` | declaration | mThreadLock | -- | tree |
| `watchers/WatchersManager.h:84` | declaration | mThreadLock | -- | tree |

**Each lock, its acquisition sites, its order, and who waits:**

| Lock | Guards | Acquired at | Order and what it is held across | Who blocks on it |
| --- | --- | --- | --- | --- |
| `mNotificationMessagesLock` (`Window.cpp:293`) | toasts, cards, posts | `:313`, `:326`, `:427`, `:1148`, `:1154`, `:1179`, `:1238`, `:1278`, `:1296` | none nested; the cards' render pass holds it for the whole pass (`:1179`); `unregisterPostedFunctions` (`:1262-1274`) walks `mFunctions` **without it** (L-03) | a worker's `displayNotificationMessage` or `postToUiThread` waits out one render pass (bounded); the interface thread never waits on a worker here |
| `mJoysticksLock` (`InputManager.cpp:52`) | joysticks, input configs | `:200`, `:227`, `:485`, `:1343`, `:1494` | three manual lock/unlock pairs (`:227-242`, `:485-623`, `:1494-1520`) with no `return` between them (read), and no RAII; the rebuild's pair spans `writeDeviceConfig` (`:605`), which fires two events (`:1234-1235`) and runs `doOnFinish`'s commands **synchronously** (`:1272`) with the lock held | interface thread only: SDL events, the launch path's `computePlayersConfigs` (`:1343`), and `updateBatteryLevel` posted from `NetworkThread.cpp:206`; no second thread takes it |
| `mWatchersLock` (`WatchersManager.cpp:7`) | the watcher list | `:66`, `:78`, `:94`, `:143`, `:181`, `.h:35` | **held across every `check()`** (`:181`, `:196`) and then `mNotificationLock` inside it (`:197` -> `:128`): order **mWatchersLock -> mNotificationLock**, and the observers' `OnWatcherChanged` runs on the watcher thread under both | **`RegisterComponent` `:66`, `UnregisterComponent` `:78`, `ResetComponent` `:94`, `GetComponent` `.h:35` and the destructor `:143` wait for a running probe** (L-11, #1283's es-core half; 3.1 at stage C) |
| `mNotificationLock` (`WatchersManager.cpp:5`) | observers | `:108`, `:114`, `:128` | inner to `mWatchersLock` when taken from `run()` | `UnregisterNotify` `:114` waits for a callback in flight |
| `mThreadLock` (`WatchersManager.h:83`) | pause and wake | `:35`, `:48`, `:165` | its own scope before `mWatchersLock` in `run()` (`:164-171`), never nested with it; `mPaused` is read and written under it, while **`mRunning` is a plain `bool` written at `:151` and read at `:161`, `:172`, `:187` outside any lock** (3.3's ThreadSanitizer race) | `pause` `:35` and `resume` `:48` take it briefly |
| `mMutex` (`Log.cpp:187`) | the log buffer | `:70`, `:104`, `:122` | none nested | any thread's `LOG(...)` takes it briefly to enqueue |
| `mScriptQueueLock` (`Scripting.cpp:20`) | script queue | `:29`, `:60`, `:78` | WIN32 only | -- |
| `mMutex` (`TextToSpeech.h:48`) | speech queue | `:27`, `:256` | the speak thread is WIN32 only; TTS is compiled out on the image (§ 5) | -- |
| `_lock` (`ThemeData.h:594`) | theme file cache | `:716`, `:737` | held across `load_file` of a theme file (`ThemeData.cpp:716-723`) | a theme load |
| `mLock` (`VolumeControl.cpp:205`) | PulseAudio wait | `:199` | `_ENABLE_PULSE_` only (the pulse branch, not parsed on the host) | -- |

**The threads' start and stop against `main.cpp`'s order** (es-app's, read at the pin):

| Thread | Started | Stopped | proved: |
| --- | --- | --- | --- |
| the logger's worker | `Log.cpp:60`, from `Log::init` (`main.cpp:788`) | `AsyncLogger::close` joins (`:76-77`) from `onExit` (`main.cpp:353`, registered `:793`) -- after `window.deinit()` (`:1358`) | tree |
| the watcher thread | `WatchersManager.cpp:61`, on the first `getInstance()` (`:15`) | `WatchersManager::stop()` at `main.cpp:1330` joins (`:154`) -- **before** `window.deinit()`; the join waits for a probe in flight and the 1 s `wait_for` (`:170`) | tree |
| the PulseAudio loop | `VolumeControl.cpp:32` (`_ENABLE_PULSE_`) | `exit()` joins (`:68-73`) from `~PulseAudioControl` | tree (branch not parsed) |
| the speak thread | `TextToSpeech.cpp:92` (**WIN32**) | `:128` | tree |
| the script queue | `Scripting.cpp:68` (**WIN32**, `new std::thread`, not a detach) | **not joined**: `exitScriptingEngine` (`main.cpp:1347`) only sets the flag and notifies (`Scripting.cpp:75-82`, the seat's G-7) | tree |
| four storage workers | `Window.cpp:1554`, `:1572`, `:1608`, `:1634` (`processStorageRequest`) | **detached** (`:1563`, `:1575`, `:1619`, `:1637`); each captures `this` and posts back (L-04); nothing joins them | tree |
| `NetworkThread` (es-app's) | `main.cpp:898` | not deleted at exit; named for its owner, outside the 96 | tree |

generated, asserted: 67 lock lines in 11 files (4 includes, 2 `weak_ptr::lock`), 10 locks summarised, 7 threads

## The lifetimes

**Every thread line** (the § 5 threads run's grep, recomputed):

| Site | What | Who joins it | What it touches on the interface thread | proved: |
| --- | --- | --- | --- | --- |
| `Log.cpp:60` | start: the logger's worker | `AsyncLogger::close` joins (`:76-77`), from `onExit` at exit | nothing; it writes the file | tree |
| `Log.cpp:180` | the member `std::thread mThread` | as above | -- | tree |
| `Scripting.cpp:18` | the member `std::thread* mScriptQueueThread` (**WIN32**) | **nobody** (`exitScriptingEngine` sets the flag and notifies, `:75-82`; the seat's G-7) | -- | tree |
| `Scripting.cpp:68` | start: `new std::thread(&executeCommandsThread)` (**WIN32**; not a detach) | **nobody**: never joined or deleted (`:75-82`; G-7) | nothing | tree |
| `TextToSpeech.cpp:92` | start: the speak thread (**WIN32**) | `~TextToSpeech` (`:128`) | nothing | tree |
| `TextToSpeech.h:47` | the member `std::thread* mSpeakThread` | as above | -- | tree |
| `VolumeControl.cpp:32` | start: `PulseAudioControl::run` (`_ENABLE_PULSE_`) | `exit()` (`:68-73`) | nothing; the volume is read under `mLock` | tree |
| `VolumeControl.cpp:203` | the member `std::thread* mThread` | as above | -- | tree |
| `Window.cpp:1554` | start: a storage worker for `mergeDrive` in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1563` | the detach | -- | -- | tree |
| `Window.cpp:1572` | start: a storage worker for `ignoreDevicePermanently` in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1575` | the detach | -- | -- | tree |
| `Window.cpp:1608` | start: a storage worker for `prepareDrive` (format) in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1619` | the detach | -- | -- | tree |
| `Window.cpp:1634` | start: a storage worker for `ignoreDevicePermanently` in `processStorageRequest`, capturing `this` | **nobody: detached** | posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox` | tree |
| `Window.cpp:1637` | the detach | -- | -- | tree |
| `watchers/WatchersManager.cpp:61` | start: the watcher thread | `~WatchersManager` joins (`:154`) from `stop()` (`main.cpp:1330`) | **the observers' `OnWatcherChanged` runs on this thread** under two locks (`:197` -> `:128-131`) | tree |
| `watchers/WatchersManager.h:88` | the member `std::thread* mThread` | as above | -- | tree |

**Every `delete this`** (all in the six dialogs, all on the interface thread; none touches a member after the delete):

| Site | What reaches it, and what follows | What the delete does to the window | proved: |
| --- | --- | --- | --- |
| `guis/GuiDetectDevice.cpp:99` | `input`: back cancels; `return true` follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiDetectDevice.cpp:132` | `update`: the first-run skip after `mDoneCallback()`; the function ends (`:133-149`) and `Window::update` touches nothing after the call (`Window.cpp:542-543`) | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiDetectDevice.cpp:145` | `update`: the hold done, `GuiInputConfig` pushed first; the function ends | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiInputConfig.cpp:262` | `okFunction` (`:258-263`): after `writeDeviceConfig` (`:259`) and `okCallback()`; reached from the OK button and from the hotkey dialog's two buttons through `GuiMsgBox::deleteMeAndCall` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiInputConfig.cpp:288` | the CANCEL button's own closure: the button is destroyed while its `std::function` runs; nothing follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiMsgBox.cpp:289` | `deleteMeAndCall`: the callback copied first (`:288`), then called after the delete (`:291-292`) -- the safe shape | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:33` | the accept button's closure: `okCallback(value)` then the delete; nothing follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:34` | the CLEAR button's closure: `okCallback("")` then the delete, **no question asked** (L-14) | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:35` | the CANCEL button's closure | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopup.cpp:74` | `input`: back; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:346` | `input`: START submits after `mOkCallback(value)`; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:352` | `input`: ESC on the keyboard device; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:359` | `input`: back; `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:395` | `input`: **`x` commits `""`** (`:392-397`, L-14); `return true` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:477` | `pressedKey`: OK after `mOkCallback(value)`; `return` follows | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:494` | `pressedKey`: the CLEAR key commits `""` (L-14); `return` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:499` | `pressedKey`: CANCEL; `return` | `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`) | tree |

**Every `postToUiThread` line** (a post runs once at the next update, on the interface thread; nothing promises a poster that dies before the drain anything; the four workers post with `this` captured, and the window outlives them only because it is `main`'s stack object until `return`):

| Site | What | proved: |
| --- | --- | --- |
| `Window.cpp:1276` | the definition: appended under the lock (`:1278`); the owner token `data` is what `unregisterPostedFunctions` (`:1262-1274`) erases by, **without the lock** (L-03) | tree |
| `Window.h:91` | the declaration (the signature § 1 i names with the three doubles) | tree |
| `Window.cpp:1556` | the merge worker's result: runs on the interface thread, pushes `GuiMsgBox` on failure | tree |
| `Window.cpp:1574` | the ignore worker's continuation | tree |
| `Window.cpp:1612` | the format worker's result | tree |
| `Window.cpp:1636` | the ignore worker's continuation | tree |

**The raw pointers the window hands out or holds:**

| Member | What | Handed out or held | Who frees it | proved: |
| --- | --- | --- | --- | --- |
| `Window.h:123` | the cards | handed out raw by `createAsyncNotificationComponent` (`Window.cpp:1168-1174`) | the window, at `:1248` only, once `isRunning()` is false; never in `deinit` or `~Window` (L-02) | tree |
| `Window.h:135` | the toasts | held | the window, at `:358` (stop) and `:377` (faded); never in `deinit` or `~Window` (L-02) | tree |
| `Window.h:147` | the screensaver | set by es-app (`SystemScreenSaver.cpp:49`, T33's) | its owner, es-app; the window only calls it | tree |
| `Window.h:151` | the page stack | `peekGui()` hands the top out raw | each page deletes itself or is deleted by its opener; `~GuiComponent` removes it (`removeGui`); `~Window` deletes what is left (`:59-60`) | tree |
| `Window.h:150` | the screen extras | held | `~Window` (`:53-54`) | tree |
| `Window.h:186` | the mouse capture | set by any component (`setMouseCapture`, `.h:111`) | cleared by `removeGui` (`:86-87`), which every `~GuiComponent` calls -- no dangling capture | tree |
| `Window.h:145` | the help bar | held | `~Window` (`:62`) | tree |
| `Window.h:146` | the overlay | held | `~Window` (`:56`) | tree |

**#1305's three halves** (read; the body was read to its last comment at stage A, `stage-a/issues.out`):

| Half | Lines | What it does | Disposition | proved: |
| --- | --- | --- | --- | --- |
| the window's (this slice's) | `Window.cpp:777-779`, `:1091-1105`, `:1107-1138` | the screensaver starts **from `render()`** on idle time alone (`:778-779`); each page is told (`onScreenSaverActivate`, `:1100`) but cannot refuse, so nothing holds it off while `GuiCloudTransfer` owns the screen; the slideshow's list is cleared only by `resetCounts` from `cancelScreenSaver` (`:1117`) -- a rescan or a `removeGui` does not clear it | a contained hold (the start refused while the top page asks for it) is a candidate for the pause; G-09 frames the start over the transfer page; 3.27 FAILs at the pin until one half lands | tree; 3.27 and G-09 owed |
| T33's (`SystemScreenSaver`) | `es-app/src/SystemScreenSaver.cpp:342-358`, `:378-380`, `:538-548` | the slideshow keeps `FileData*` across picks; its retirement on a rescan is T33's | named for T33's owner at the pause | design |
| T2's (the rescan) | `es-app/src/SystemData.cpp:459-473` | the rescan deletes a `FileData` gone from disk while a holder keeps it | named for T2's owner at the pause | design |

generated, asserted: 18 thread rows (4 detaches), 17 `delete this`, 6 posts, 8 raw pointers, 3 halves of #1305

## The scripts

**How every site's string reaches a shell** (`utils/Platform.cpp`, T36's, read): on Linux `run()` wraps the command as `((((<cmd> 2> <log>/<stderr> ; echo $? >&3) | head -300 > <log>/<stdout>) 3>&1) | (read xs; exit $xs))` (`:162`) and hands it to `system()` when it waits (`:167`) or to `/bin/sh -c` in a double-forked child when it does not (`:172-181`). So each of the four is a shell command line; the § 5 run's direct-spawn count (`system(`/`popen(`/`runSystemCommand(` in the 96) is 0 because the shell is inside `ProcessStartInfo`.

| Site | Function | What builds the string | What is quoted | Which thread | Waits | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `InputManager.cpp:1272` | `doOnFinish` (`:1242-1284`) | `tocall` = the text of each `<command>` under `<inputAction type="onfinish">` in `es_input.cfg` (`:1262-1268`), as written | nothing quoted by ES: the text is the command line | the interface thread, from `writeDeviceConfig` (`:1238`) -- inside the rebuild's `mJoysticksLock` when reached from the hot-plug write (`:485-623`, `:605`) | **waits** (the constructor's `waitForExit = true`, `Platform.cpp:52`; `system()` at `:167`); the logged line is masked (`:1270`) | tree |
| `Scripting.cpp:140` | `executeScript`, non-WIN32 (`:137-148`) | the script path, quoted only when it has a space (`:92-93`); the event name; up to three arguments, each with every `"` stripped (`:104-107`) and quoted only when it has a space (`:109-112`) | **a `$`, a backtick, a `;` or a `'` in an argument reaches `sh` unquoted** (L-18, 3.4); a file name is a player's (a ROM, a scraped name) | the caller's: `fireEvent`, on the interface thread for the launch events | waits only for `quit` and only in the single-script pass -- the per-event pass passes `""` as the event name (`:177`), so `waitForExit = (eventName == "quit")` (`:142`) is false there even for `quit`; output to `es_script_stdout.log`, `head -300` (`Platform.cpp:162`) | tree |
| `Scripting.cpp:131` | `executeScript`, WIN32, the `-wait` branch (`:127-136`) | as above, with `powershell` prefixed for `.ps1` (`:116-117`) | as above | the caller's | waits (`:133`); WIN32 only, not on the image | tree |
| `Scripting.cpp:43` | `executeCommandsThread`, WIN32 (`:24-54`) | a command queued by `pushCommand` (`:58-`) | as above | the script queue's thread (WIN32) | does not wait (`:45`); WIN32 only | tree |

**The per-event pass runs every file** in `scripts/<event>/` on the device: the extension filter is inside `#if WIN32` (`:172-176`); only the single-script pass filters by extension (`:201-203`) (L-18, 3.5, 3.6).

generated, asserted: 4 sites (4 `ProcessStartInfo` lines in the 96), direct shell spawns 0

## The words

**The French catalog:** `locale/lang/fr/LC_MESSAGES/emulationstation2.po` at the pin, 2173 entries parsed (context-less).

| Site | msgid(s) | French | Tier or verb words | proved: |
| --- | --- | --- | --- | --- |
| `BindingManager.cpp:136` | `YES` / `NO` | `OUI` / `NON` | -- | tree |
| `BindingManager.cpp:150` | `Unknown` / `None` | `Inconnu` / `Aucun` | -- | tree |
| `GunManager.cpp:686` | `%s connected` | `%s connectée` | -- | tree |
| `GunManager.cpp:703` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `GunManager.cpp:724` | `%s connected` | `%s connectée` | -- | tree |
| `GunManager.cpp:734` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `GunManager.cpp:1004` | `%s connected` | `%s connectée` | -- | tree |
| `GunManager.cpp:1031` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `InputManager.cpp:856` | `%s connected` | `%s connectée` | -- | tree |
| `InputManager.cpp:858` | `%s connected` | `%s connectée` | -- | tree |
| `InputManager.cpp:869` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `InputManager.cpp:871` | `%s disconnected` | `%s déconnectée` | -- | tree |
| `TextToSpeech.cpp:177` | `SCREEN READER ENABLED` / `SCREEN READER DISABLED` | `LECTEUR D’ÉCRAN ACTIVÉ` / `LECTEUR D’ÉCRAN DÉSACTIVÉ` | -- | tree |
| `Window.cpp:442` | `Now playing: ` | `En cours : ` | -- | tree |
| `Window.cpp:1367` | `CALIBRATING GUN\nFire on targets to calibrate` | `CALIBRATION DU PISTOLET\nCalibrez en tirant sur les cibles` | -- | tree |
| `Window.cpp:1505` | `Reloaded the games list...` | `Rechargement de la liste des jeux…` | -- | tree |
| `Window.cpp:1542` | `GAME DRIVE DETECTED` | `DISQUE DE JEU DÉTECTÉ` | -- | tree |
| `Window.cpp:1543` | `DEVICE` | `APPAREIL` | -- | tree |
| `Window.cpp:1544` | `MODEL` | `MODÈLE` | -- | tree |
| `Window.cpp:1545` | `SIZE` | `TAILLE` | -- | tree |
| `Window.cpp:1546` | `MOUNT` | `MONTER` | -- | tree |
| `Window.cpp:1547` | `Merge games from this drive partition now?` | `Fusionner les jeux de cette partition du disque dur maintenant ?` | -- | tree |
| `Window.cpp:1548` | `(This will also apply on future boots)` | `(Cela s’appliquera également aux démarrages futurs)` | -- | tree |
| `Window.cpp:1551` | `Merge requested... Please wait.` | `Fusion demandée… Veuillez patienter.` | -- | tree |
| `Window.cpp:1558` | `MERGE FAILED` / `Please check the logs.` / `OK` | `ÉCHEC DE LA FUSION` / `Veuillez consulter les journaux.` / `OK` | -- | tree |
| `Window.cpp:1569` | `NO, IGNORE THIS TIME` | `NON, IGNORER CETTE FOIS` | -- | tree |
| `Window.cpp:1570` | `NO, IGNORE FOREVER` | `NON, IGNORER À JAMAIS` | -- | tree |
| `Window.cpp:1571` | `Adding drive to ignore list...` | `Ajout du disque à la liste d’exclusion…` | -- | tree |
| `Window.cpp:1577` | `YES, MERGE DRIVE` | `OUI, FUSIONNER LES DISQUES` | -- | tree |
| `Window.cpp:1584` | `YES` | `OUI` | -- | tree |
| `Window.cpp:1585` | `NO` | `NON` | -- | tree |
| `Window.cpp:1593` | `N/A` | `N/D` | -- | tree |
| `Window.cpp:1594` | `N/A` | `N/D` | -- | tree |
| `Window.cpp:1597` | `NEW DRIVE DETECTED` | `NOUVEAU DISQUE DÉTECTÉ` | -- | tree |
| `Window.cpp:1598` | `DEVICE` | `APPAREIL` | -- | tree |
| `Window.cpp:1599` | `MODEL` | `MODÈLE` | -- | tree |
| `Window.cpp:1600` | `SIZE` | `TAILLE` | -- | tree |
| `Window.cpp:1601` | `Format and prepare this drive for game storage?` | `Formater et préparer ce disque pour le stockage de jeux ?` | -- | tree |
| `Window.cpp:1602` | `(ALL EXISTING DATA WILL BE ERASED)` | `(TOUTES LES DONNÉES EXISTANTES SERONT EFFACÉES)` | -- | tree |
| `Window.cpp:1605` | `Starting format process...` | `Démarrage du processus de formatage…` | -- | tree |
| `Window.cpp:1614` | `FORMAT FAILED` / `Please check the logs.` / `OK` | `ÉCHEC DU FORMATTAGE` / `Veuillez consulter les journaux.` / `OK` | -- | tree |
| `Window.cpp:1623` | `ARE YOU SURE?` | `ÊTES-VOUS SÛR(E) ?` | -- | tree |
| `Window.cpp:1624` | `NO` | `NON` | -- | tree |
| `Window.cpp:1625` | `YES` | `OUI` | -- | tree |
| `Window.cpp:1631` | `NO, IGNORE THIS TIME` | `NON, IGNORER CETTE FOIS` | -- | tree |
| `Window.cpp:1632` | `NO, IGNORE FOREVER` | `NON, IGNORER À JAMAIS` | -- | tree |
| `Window.cpp:1633` | `Adding drive to ignore list...` | `Ajout du disque à la liste d’exclusion…` | -- | tree |
| `Window.cpp:1639` | `YES, FORMAT & MERGE` | `OUI, FORMATER & FUSIONNER` | -- | tree |
| `Window.cpp:1646` | `NO, IGNORE` | `NON, IGNORER` | -- | tree |
| `Window.cpp:1647` | `YES, FORMAT & MERGE` | `OUI, FORMATER & FUSIONNER` | -- | tree |
| `guis/GuiDetectDevice.cpp:32` | `WELCOME` / `CONFIGURE INPUT` | `BIENVENUE` / `CONFIGURER LES MANETTES` | -- | tree |
| `guis/GuiDetectDevice.cpp:46` | `NO GAMEPADS DETECTED` | `AUCUNE MANETTE DÉTECTÉE` | -- | tree |
| `guis/GuiDetectDevice.cpp:52` | `HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT.` | `MAINTENEZ UN BOUTON DE VOTRE MANETTE POUR LA CONFIGURER.` | -- | tree |
| `guis/GuiDetectDevice.cpp:56` | `PRESS ESC TO CANCEL.` | `APPUYEZ SUR ESC POUR ANNULER.` | -- | tree |
| `guis/GuiDetectDevice.cpp:58` | `PRESS ESC OR A HOTKEY TO CANCEL.` | `APPUYEZ SUR ESC OU UN RACCOURCI POUR ANNULER.` | -- | tree |
| `guis/GuiInputConfig.cpp:125` | `CONFIGURING` | `CONFIGURATION` | -- | tree |
| `guis/GuiInputConfig.cpp:130` | `KEYBOARD` | `CLAVIER` | -- | tree |
| `guis/GuiInputConfig.cpp:132` | `CEC` | `CEC` | -- | tree |
| `guis/GuiInputConfig.cpp:134` | `GAMEPAD %i` | `MANETTE %i` | -- | tree |
| `guis/GuiInputConfig.cpp:139` | `HOLD ANY BUTTON TO SKIP` | `MAINTENEZ UN BOUTON POUR PASSER` | -- | tree |
| `guis/GuiInputConfig.cpp:166` | `-NOT DEFINED-` | `-NON DÉFINI-` | -- | tree |
| `guis/GuiInputConfig.cpp:264` | `OK` | `OK` | -- | tree |
| `guis/GuiInputConfig.cpp:269` | `NO HOTKEY BUTTON HAS BEEN ASSIGNED. THIS IS REQUIRED FOR EXITING GAMES WITH A CONTROLLER. DO YOU WANT TO USE THE SELECT BUTTON AS YOUR HOTKEY?` | `VOUS N’AVEZ PAS ASSIGNÉ DE BOUTON DE RACCOURCI. CECI EST NÉCESSAIRE POUR QUITTER UN JEU AVEC UNE MANETTE. VOULEZ-VOUS UTILISER LE BOUTON SELECT COMME RACCOURCI ?` | -- | tree |
| `guis/GuiInputConfig.cpp:270` | `SET SELECT AS HOTKEY` | `DÉFINIR SELECT COMME RACCOURCI` | -- | tree |
| `guis/GuiInputConfig.cpp:276` | `DO NOT ASSIGN HOTKEY` | `NE PAS ASSIGNER DE RACCOURCI` | -- | tree |
| `guis/GuiInputConfig.cpp:288` | `CANCEL` | `ANNULER` | -- | tree |
| `guis/GuiInputConfig.cpp:379` | `PRESS ANYTHING` | `APPUYEZ SUR UN BOUTON` | -- | tree |
| `guis/GuiInputConfig.cpp:385` | `-NOT DEFINED-` | `-NON DÉFINI-` | -- | tree |
| `guis/GuiInputConfig.cpp:397` | `ALREADY TAKEN` | `DÉJÀ UTILISÉ` | -- | tree |
| `guis/GuiMsgBox.cpp:75` | `YES` | `OUI` | -- | tree |
| `guis/GuiMsgBox.cpp:77` | `OK` | `OK` | -- | tree |
| `guis/GuiMsgBox.cpp:125` | `OK` / `NO` | `OK` / `NON` | -- | tree |
| `guis/GuiTextEditPopup.cpp:34` | `CLEAR` / `CLEAR` | `EFFACER` / `EFFACER` | -- | tree |
| `guis/GuiTextEditPopup.cpp:35` | `CANCEL` / `DISCARD CHANGES` | `ANNULER` / `ANNULER LES CHANGEMENTS` | -- | tree |
| `guis/GuiTextEditPopup.cpp:84` | `BACK` | `RETOUR` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:209` | `SHIFTS FOR UPPER, LOWER, AND SPECIAL` | `MAJ POUR MAJUSCULE, MINUSCULE ET SPÉCIAL` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:214` | `ALT GR` | `ALT GR` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:454` | `CLEAR` | `EFFACER` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:456` | `SHIFT` | `MAJ` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:457` | `OK` | `OK` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:458` | `BACK` | `RETOUR` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:459` | `SPACE` | `ESPACE` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:460` | `DELETE` | `SUPPRIMER` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:486` | `SPACE` | `ESPACE` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:491` | `CLEAR` | `EFFACER` | -- | tree |
| `guis/GuiTextEditPopupKeyboard.cpp:497` | `CANCEL` | `ANNULER` | -- | tree |

**msgids without a French entry:** none.

**`GAMEPAD %i`** (`guis/GuiInputConfig.cpp:134`): French `MANETTE %i`; the argument is `getDeviceId() + 1`, the SDL instance id, not the seat (L-17, 3.21).

**The glyph literals** (`\uF...`, outside `_()`; `es-ui-style-guide.md` § Glyphs): `GunManager.cpp:686`, `GunManager.cpp:703`, `GunManager.cpp:724`, `GunManager.cpp:734`, `GunManager.cpp:1004`, `GunManager.cpp:1031`, `InputManager.cpp:856`, `InputManager.cpp:858`, `InputManager.cpp:869`, `InputManager.cpp:871`, `Window.cpp:431`, `Window.cpp:442`, `guis/GuiTextEditPopupKeyboard.cpp:171`, `guis/GuiTextEditPopupKeyboard.cpp:172`, `guis/GuiTextEditPopupKeyboard.cpp:173`, `guis/GuiTextEditPopupKeyboard.cpp:174`, `guis/GuiTextEditPopupKeyboard.cpp:178`, `guis/GuiTextEditPopupKeyboard.cpp:182`, `guis/GuiTextEditPopupKeyboard.cpp:183`, `guis/GuiTextEditPopupKeyboard.cpp:184`, `guis/GuiTextEditPopupKeyboard.cpp:188`, `guis/GuiTextEditPopupKeyboard.cpp:189`, `guis/GuiTextEditPopupKeyboard.cpp:190`, `guis/GuiTextEditPopupKeyboard.cpp:209`, `guis/GuiTextEditPopupKeyboard.cpp:214`, `guis/GuiTextEditPopupKeyboard.cpp:468`, `guis/GuiTextEditPopupKeyboard.cpp:481` -- 27 lines: the twelve notifications carry the light-gun `\uF05B`, the wheel `\uF1B9` or the pad `\uF11B` with one space (a notification's single space) and the song `\uF028` with two; the rest are the keyboard's key faces (DEL `\uF177`, OK `\uF058` or the multi-line `\uF149`, and the shift and alt keys).

**The fork's read for the tiers and the verbs:** 0 of the 86 lines carry a tier or a verb word of D-UI-022's (the column above), so the slice's strings sit outside the cloud vocabulary and owe it nothing. **The sentence-case dialogs are upstream's** (the description dialect, `es-ui-style-guide.md` § Text): recorded, not changed.

The `ngettext` and `pgettext` lines in the 96 outside `LocaleES` and `gettext.h`, with the catalog's context and plural entries:

| Site | Call | French | proved: |
| --- | --- | --- | --- |
| `guis/GuiDetectDevice.cpp:42` | `ngettext` `%i GAMEPAD DETECTED` / `%i GAMEPADS DETECTED` | `%i MANETTE DÉTECTÉE` / `%i MANETTES DÉTECTÉES` | tree |
| `guis/GuiInputConfig.cpp:11` | `pgettext` `joystick` / `NORTH` | `NORD` | tree |
| `guis/GuiInputConfig.cpp:12` | `pgettext` `joystick` / `SOUTH` | `SUD` | tree |
| `guis/GuiInputConfig.cpp:13` | `pgettext` `joystick` / `EAST` | `EST` | tree |
| `guis/GuiInputConfig.cpp:14` | `pgettext` `joystick` / `WEST` | `OUEST` | tree |
| `guis/GuiInputConfig.cpp:16` | `pgettext` `joystick` / `START` | `START` | tree |
| `guis/GuiInputConfig.cpp:17` | `pgettext` `joystick` / `SELECT` | `SELECT` | tree |
| `guis/GuiInputConfig.cpp:19` | `pgettext` `joystick` / `D-PAD UP` | `D-PAD HAUT` | tree |
| `guis/GuiInputConfig.cpp:20` | `pgettext` `joystick` / `D-PAD DOWN` | `D-PAD BAS` | tree |
| `guis/GuiInputConfig.cpp:21` | `pgettext` `joystick` / `D-PAD LEFT` | `D-PAD GAUCHE` | tree |
| `guis/GuiInputConfig.cpp:22` | `pgettext` `joystick` / `D-PAD RIGHT` | `D-PAD DROITE` | tree |
| `guis/GuiInputConfig.cpp:24` | `pgettext` `joystick` / `LEFT ANALOG UP` | `STICK GAUCHE : HAUT` | tree |
| `guis/GuiInputConfig.cpp:25` | `pgettext` `joystick` / `LEFT ANALOG DOWN` | `STICK GAUCHE : BAS` | tree |
| `guis/GuiInputConfig.cpp:26` | `pgettext` `joystick` / `LEFT ANALOG LEFT` | `STICK GAUCHE : GAUCHE` | tree |
| `guis/GuiInputConfig.cpp:27` | `pgettext` `joystick` / `LEFT ANALOG RIGHT` | `STICK GAUCHE : DROITE` | tree |
| `guis/GuiInputConfig.cpp:28` | `pgettext` `joystick` / `RIGHT ANALOG UP` | `STICK DROIT : HAUT` | tree |
| `guis/GuiInputConfig.cpp:29` | `pgettext` `joystick` / `RIGHT ANALOG DOWN` | `STICK DROIT : BAS` | tree |
| `guis/GuiInputConfig.cpp:30` | `pgettext` `joystick` / `RIGHT ANALOG LEFT` | `STICK DROIT : GAUCHE` | tree |
| `guis/GuiInputConfig.cpp:31` | `pgettext` `joystick` / `RIGHT ANALOG RIGHT` | `STICK DROIT : DROITE` | tree |
| `guis/GuiInputConfig.cpp:33` | `pgettext` `joystick` / `LEFT SHOULDER` | `TRANCHE GAUCHE (L1)` | tree |
| `guis/GuiInputConfig.cpp:34` | `pgettext` `joystick` / `RIGHT SHOULDER` | `TRANCHE DROITE (R1)` | tree |
| `guis/GuiInputConfig.cpp:35` | `pgettext` `joystick` / `LEFT TRIGGER` | `GÂCHETTE GAUCHE (L2)` | tree |
| `guis/GuiInputConfig.cpp:36` | `pgettext` `joystick` / `RIGHT TRIGGER` | `GÂCHETTE DROITE (R2)` | tree |
| `guis/GuiInputConfig.cpp:37` | `pgettext` `joystick` / `LEFT STICK PRESS` | `CLIC STICK GAUCHE (L3)` | tree |
| `guis/GuiInputConfig.cpp:38` | `pgettext` `joystick` / `RIGHT STICK PRESS` | `CLIC STICK DROIT (R3)` | tree |
| `guis/GuiInputConfig.cpp:40` | `pgettext` `joystick` / `HOTKEY` | `RACCOURCI` | tree |
| `guis/GuiInputConfig.cpp:163` | `pgettext` with a runtime key (xgettext cannot see it; the `fake_gettext_*` macros above exist so it can) | -- | tree |
| `guis/GuiInputConfig.cpp:347` | `ngettext` `HOLD FOR %iS TO SKIP` / `HOLD FOR %iS TO SKIP` | `MAINTENEZ PENDANT %iS POUR PASSER` / `MAINTENEZ PENDANT %iS POUR PASSER` | tree |

generated, asserted: 86 lines in 10 files, 97 occurrences, 61 msgids, 0 without French; 27 glyph lines; 28 `pgettext`/`ngettext` lines, 0 without French

## The structure

**The include reach** (every header of the 96, ranked by its includers across `es-core/` and `es-app/` at the pin; a change to a header with outside includers is a change to their lanes):

| Header | Includers in the 96 | es-core outside the 96 | es-app | Total | proved: |
| --- | --- | --- | --- | --- | --- |
| `es-core/src/Log.h` | 21 | 30 | 57 | 108 | tool-run |
| `es-core/src/LocaleES.h` | 13 | 22 | 66 | 101 | tool-run |
| `es-core/src/GuiComponent.h` | 9 | 28 | 37 | 74 | tool-run |
| `es-core/src/Window.h` | 10 | 14 | 45 | 69 | tool-run |
| `es-core/src/guis/GuiMsgBox.h` | 4 | 0 | 43 | 47 | tool-run |
| `es-core/src/ThemeData.h` | 8 | 20 | 11 | 39 | tool-run |
| `es-core/src/Paths.h` | 8 | 9 | 16 | 33 | tool-run |
| `es-core/src/InputManager.h` | 5 | 7 | 6 | 18 | tool-run |
| `es-core/src/guis/GuiTextEditPopup.h` | 1 | 0 | 17 | 18 | tool-run |
| `es-core/src/guis/GuiTextEditPopupKeyboard.h` | 1 | 0 | 17 | 18 | tool-run |
| `es-core/src/math/Misc.h` | 7 | 6 | 2 | 15 | tool-run |
| `es-core/src/AudioManager.h` | 4 | 2 | 7 | 13 | tool-run |
| `es-core/src/ImageIO.h` | 1 | 8 | 4 | 13 | tool-run |
| `es-core/src/PowerSaver.h` | 4 | 6 | 3 | 13 | tool-run |
| `es-core/src/animations/LambdaAnimation.h` | 1 | 3 | 9 | 13 | tool-run |
| `es-core/src/math/Vector2i.h` | 4 | 8 | 1 | 13 | tool-run |
| `es-core/src/Scripting.h` | 3 | 2 | 7 | 12 | tool-run |
| `es-core/src/TextToSpeech.h` | 3 | 3 | 6 | 12 | tool-run |
| `es-core/src/math/Vector2f.h` | 6 | 5 | 1 | 12 | tool-run |
| `es-core/src/BindingManager.h` | 3 | 3 | 5 | 11 | tool-run |
| `es-core/src/Sound.h` | 3 | 3 | 4 | 10 | tool-run |
| `es-core/src/watchers/WatchersManager.h` | 3 | 4 | 3 | 10 | tool-run |
| `es-core/src/math/Transform4x4f.h` | 2 | 7 | 0 | 9 | tool-run |
| `es-core/src/VolumeControl.h` | 1 | 1 | 4 | 6 | tool-run |
| `es-core/src/animations/Animation.h` | 3 | 0 | 3 | 6 | tool-run |
| `es-core/src/InputConfig.h` | 3 | 1 | 1 | 5 | tool-run |
| `es-core/src/guis/GuiDetectDevice.h` | 1 | 0 | 4 | 5 | tool-run |
| `es-core/src/watchers/BatteryLevelWatcher.h` | 1 | 3 | 1 | 5 | tool-run |
| `es-core/src/FavoriteMusicManager.h` | 2 | 0 | 2 | 4 | tool-run |
| `es-core/src/HelpStyle.h` | 2 | 1 | 1 | 4 | tool-run |
| `es-core/src/MameNames.h` | 1 | 0 | 3 | 4 | tool-run |
| `es-core/src/anim/ThemeStoryboard.h` | 4 | 0 | 0 | 4 | tool-run |
| `es-core/src/math/Vector4f.h` | 4 | 0 | 0 | 4 | tool-run |
| `es-core/src/watchers/NetworkStateWatcher.h` | 1 | 2 | 1 | 4 | tool-run |
| `es-core/src/CECInput.h` | 3 | 0 | 0 | 3 | tool-run |
| `es-core/src/GunManager.h` | 3 | 0 | 0 | 3 | tool-run |
| `es-core/src/MultiStateInput.h` | 1 | 0 | 2 | 3 | tool-run |
| `es-core/src/ThemeVariables.h` | 3 | 0 | 0 | 3 | tool-run |
| `es-core/src/guis/GuiInfoPopup.h` | 2 | 0 | 1 | 3 | tool-run |
| `es-core/src/math/Vector3f.h` | 2 | 1 | 0 | 3 | tool-run |
| `es-core/src/playlists/M3uPlaylist.h` | 1 | 1 | 1 | 3 | tool-run |
| `es-core/src/AsyncHandle.h` | 0 | 0 | 2 | 2 | tool-run |
| `es-core/src/HelpPrompt.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/LogPolicy.h` | 1 | 0 | 1 | 2 | tool-run |
| `es-core/src/Splash.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/anim/StoryboardAnimator.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/anim/ThemeAnimation.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/animations/AnimationController.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/guis/GuiInputConfig.h` | 2 | 0 | 0 | 2 | tool-run |
| `es-core/src/playlists/AnimatedGifPlaylist.h` | 1 | 1 | 0 | 2 | tool-run |
| `es-core/src/gettext.h` | 1 | 0 | 0 | 1 | tool-run |

**The guards** (every preprocessor condition naming a platform or feature macro; the host's stand-in parses one branch, stage C):

| Macro | Lines | First sites | On the host | proved: |
| --- | --- | --- | --- | --- |
| `WIN32` | 69 | `AudioManager.cpp:22`, `GunManager.cpp:22`, `GunManager.cpp:197`, `GunManager.cpp:319`, `GunManager.cpp:556`, `GunManager.cpp:794` ... | not the image's branch: the `#else` is parsed | tool-run |
| `HAVE_UDEV` | 23 | `GunManager.cpp:15`, `GunManager.cpp:163`, `GunManager.cpp:180`, `GunManager.cpp:208`, `GunManager.cpp:311`, `GunManager.cpp:516` ... | **not parsed** without libudev headers; G-01's `ldd` settles the image's | tool-run |
| `HAVE_LIBCEC` | 11 | `CECInput.cpp:3`, `CECInput.cpp:23`, `CECInput.cpp:94`, `CECInput.cpp:154`, `CECInput.cpp:175`, `CECInput.cpp:196` ... | **not parsed**; CEC compiled out | tool-run |
| `_WIN32` | 10 | `Log.cpp:200`, `Splash.cpp:331`, `VolumeControl.cpp:234`, `VolumeControl.cpp:378`, `VolumeControl.cpp:471`, `VolumeControl.cpp:533` ... | as WIN32 | tool-run |
| `APPLE` (double-underscore-wrapped: the compiler's predefined macro) | 9 | `Log.cpp:204`, `VolumeControl.cpp:230`, `VolumeControl.cpp:265`, `VolumeControl.cpp:456`, `VolumeControl.cpp:488`, `VolumeControl.cpp:589` ... | not the image's | tool-run |
| `_ENABLE_PULSE_` | 7 | `VolumeControl.cpp:11`, `VolumeControl.cpp:243`, `VolumeControl.cpp:269`, `VolumeControl.cpp:460`, `VolumeControl.cpp:492`, `VolumeControl.cpp:593` ... | **not parsed** on the host (no pulse headers); the ALSA branch is | tool-run |
| `_RPI_` | 5 | `CECInput.cpp:8`, `CECInput.cpp:53`, `CECInput.cpp:95`, `CECInput.cpp:162`, `VolumeControl.cpp:217` | not defined for these images: the other branch is parsed | tool-run |
| `_ENABLE_TTS_` | 5 | `TextToSpeech.cpp:53`, `TextToSpeech.cpp:94`, `TextToSpeech.cpp:138`, `TextToSpeech.cpp:197`, `TextToSpeech.cpp:268` | **not parsed**; compiled out on the image | tool-run |
| `BATOCERA` | 4 | `InputManager.cpp:585`, `Paths.cpp:24`, `Paths.cpp:48`, `Splash.cpp:103` | not defined in a ROCKNIX build: the other branch is parsed | tool-run |
| `ROCKNIX` | 3 | `InputManager.cpp:585`, `Paths.cpp:76`, `Splash.h:10` | parsed with `-DROCKNIX` in the stand-in (stage C) | tool-run |
| `SDL_JoystickDevicePathById` | 1 | `InputManager.cpp:840` | defined only by an SDL that carries it; the image's SDL decides, the host parses without it | tool-run |
| `_DEBUG` | 1 | `Paths.cpp:40` | not defined in a release build | tool-run |

**The CMake lists:** every `.cpp` of the 96 is named once in `es-core/CMakeLists.txt` (44 of 44); the headers it does not list: `es-core/src/HelpPrompt.h`, `es-core/src/Scripting.h`; 9 lines carry a trailing `# batocera`, 7 of them naming a path of the 96 (`:19`, `:20`, `:96`, `:98`, `:160`, `:229`, `:231`); the lists are unconditional but for the two `if(` blocks at `:278` (the GLES renderer pair) and `:287` (`MSVC`'s source groups). **T21's hunk** (the pin to T21's tip `3ae9610b0`): 5 added lines -- `HttpText.h`, `RecoveryOutcome.h` (`@@ -9`), `utils/DownloadFile.h` (`@@ -124`), `HttpText.cpp` (`@@ -151`), `utils/DownloadFile.cpp` (`@@ -259`); the integration's, named in the hand-back (§ 1 h, L-26). `proved: tool-run`.

**`Window.cpp:29`** includes `../es-app/src/ApiSystem.h` for `processStorageRequest`'s four workers (`:1554-1637`): es-core depending on es-app, upstream ROCKNIX's, outside the lanes (D-UI-079); **recorded as upstream's, not changed** (L-04). **The `ROCKNIX` lines:** `es-core/src/InputManager.cpp:585`, `es-core/src/Paths.cpp:76`, `es-core/src/Splash.h:10` (3).

**L-22, the stale rule sentence:** `.claude/rules/es-native-ui.md:30` calls `AsyncNotificationComponent` the *top-right progress card*; the card is centred at the pin (`Window.cpp:1192`, the fork's hunk) and the same rule says so at `:191-197` and `:208`. For the coordinator's sweep (`tools/archaeology --reversal`), not the lane's edit.

**L-25, the footnote:** the inventory records `last_fork_commit 1593c299f3 2026-09-10` on `guis/GuiTextEditPopupKeyboard.h`, which is byte-identical to the merge base `cada856d86` (`git diff --quiet` exit 0): a fork touch undone or merged away. Nothing to fix; § The merge debt carries it.

**The map:** `tools/es-menu-map-check`'s `SOURCE_DIRS` at its `:58` includes `es-core/src/guis`; at the pin it printed `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 (stage A, `stage-a/runs.out`). Its three patterns over this slice's 6 dialogs: `guis/GuiDetectDevice.cpp` 0, `guis/GuiInfoPopup.cpp` 0, `guis/GuiInputConfig.cpp` 0, `guis/GuiMsgBox.cpp` 0, `guis/GuiTextEditPopup.cpp` 0, `guis/GuiTextEditPopupKeyboard.cpp` 0 -- **0 titles**: these dialogs build no `GuiSettings`/`MenuComponent` page, so the checker sees nothing here and has nothing to miss; a stream that adds a page must map it (D-UI-039).

generated, asserted: 51 headers' reach, 12 guard macros, 44 `.cpp` named once, 2 headers unregistered, 9 `# batocera` lines, 2 CMake `if(`, 3 `ROCKNIX` lines, 0 map titles

## The merge debt

`cada856d86` is the merge base against `rocknix/master` (`f6c542872e`), and `bccd715707` is its parent and the stale `upstream/master` (2026-09-22). Upstream has **0** commits on the 96 since the base (14 on any path; numstat 0), **96 of 96** blobs are identical between the base and master, and **83 of 96** between the pin and master. Batocera's **twelve** commits since `1750dded8c` touch **nine** files, six of them fork-modified (`GunManager.cpp`, `InputManager.cpp`, `Log.cpp`, `Window.cpp`, `Window.h`, `guis/GuiMsgBox.cpp`): the reconciliation list only. T21's `3ae9610b0` hunk in `es-core/CMakeLists.txt` (five added lines, § The structure) is the integration's. **T34's ES tip, read at stage B:** local `568ef099d` and `origin` `a9017ff50` at 06:29:09Z (`git -C <W> rev-parse`/`diff --name-only`): **empty inside the 96** (19 and 18 files on other paths). The first read, at 06:08:37Z, was local `db12b1598a` and `origin` `2cbb62d7bd`, also empty inside the 96; the hand-back reads it a third time. L-25's footnote: `guis/GuiTextEditPopupKeyboard.h` carries a fork commit in the inventory and is byte-identical to the base. `proved: tool-run` (stage A's run 5, `stage-a/runs.out`).

## The runs

**The § 5 runs** (stage A, `stage-a/runs.sh` -> `stage-a/runs.out`, 05:59:32Z to 05:59:35Z; each block wrapped in `rc=$?` and a `date +%s` pair; every figure as the brief expects but the deltas `00` names):

| # | Run | Exit | Wall | Figure (the command's own lines) | A FAIL would mean | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | the scope | 0 | 0 s | `96; 44; 51; 1` | the paths list is not the slice the brief names: a scope drift, stop (§ 8) | tool-run |
| 2 | the ES worktree at the pin, clean; the bases; the counts | 0 | 0 s | `16dbac5211; 0; cada856d86; f6c542872e; b2ceb55a7e; 1750dded8c; 725; 14; 1; 15` | the read is not the pin's, or a base moved: the merge debt is re-derived | tool-run |
| 3 | the lines two ways | 0 | 1 s | `wc -l 22567; grep -c 22575; no newline: es-core/src/MultiStateInput.cpp 52/53; no newline: es-core/src/MultiStateInput.h 18/19; no newline: es-core/src/anim/StoryboardAnimator.cpp 236/237; no newline: es-core/src/anim/ThemeAnimation.h 145/146; no newline: es-core/src/anim/ThemeStoryboard.cpp 241/242; no newline: es-core/src/math/Vector2f.cpp 38/39; no newline: es-core/src/math/Vector4f.cpp 106/107; no newline: es-cor ...` | a line rule differs: the coverage table's lines are wrong | tool-run |
| 4 | the fork's delta | 0 | 0 s | `13 files changed, 247 insertions(+), 71 deletions(-); 13 files changed, 247 insertions(+), 71 deletions(-); 13 files changed, 247 insertions(+), 71 deletions(-); 1; added rc=0; 7	0	es-core/CMakeLists.txt; 2	0	es-core/src/GunManager.cpp; 8	1	es-core/src/InputConfig.cpp; 5	2	es-core/src/InputManager.cpp; 19	40	es-core/src/Log.cpp; 3	3	es-core/src/Scripting.cpp; 4	1	es-core/src/Splash.h; 49	6	es-core/src/Window.cpp; 2	0 ...` | the fork changed the slice since the brief: the 13 are re-read | tool-run |
| 5 | upstream's delta: the merge-debt record | 0 | 0 s | `0; upstream commits rc=1; 0; upstream numstat rc=1; identical to rocknix/master: 83; identical to cada856d86: 83; MB-vs-master identical: 96; 12; 9; 6` | upstream moved on the 96: the merge debt grows | tool-run |
| 6 | the other lanes' deltas inside the 96 | 0 | 0 s | `== m6-es-launch-path-649; == m6-es-cloud-pages-665; == m6-es-achievements-pages-667; == m6-es-state-and-bridge-668; 1 file changed, 5 insertions(+); == m6-es-guimenu-673; == m6-es-pages-678; == m6-es-app-views-scrapers-679; == m6-es-app-system-680; == m6-es-core-components-681` | another lane edited inside the 96: a collision for the hand-back | tool-run |
| 7 | the strings, two ways | 0 | 0 s | `_(" lines TOTAL 86 in 10 files; 97; BindingManager.cpp:2 GunManager.cpp:6 InputManager.cpp:4 TextToSpeech.cpp:1 Window.cpp:37 guis/GuiDetectDevice.cpp:5 guis/GuiInputConfig.cpp:14 guis/GuiMsgBox.cpp:3 guis/GuiTextEditPopup.cpp:3 guis/GuiTextEditPopupKeyboard.cpp:11` | the strings moved: § The words is regenerated | tool-run |
| 8 | the log lines | 0 | 0 s | `LOG(Log lines TOTAL 158 in 20 files` | the log lines moved | tool-run |
| 9 | the threads and the lifetimes | 0 | 0 s | `es-core/src/Log.cpp:60 es-core/src/Log.cpp:180 es-core/src/Scripting.cpp:18 es-core/src/Scripting.cpp:68 es-core/src/TextToSpeech.cpp:92 es-core/src/TextToSpeech.h:47 es-core/src/VolumeControl.cpp:32 es-core/src/VolumeControl.cpp:203 es-core/src/Window.cpp:1554 es-core/src/Window.cpp:1563 es-core/src/Window.cpp:1572 es-core/src/Window.cpp:1575 es-core/src/Window.cpp:1608 es-core/src/Window.cpp:1619 es-core/src/Window ...` | a thread was added or removed: § The lifetimes' base | tool-run |
| 10 | the process spawns | 0 | 0 s | `es-core/src/InputManager.cpp:1272 es-core/src/Scripting.cpp:43 es-core/src/Scripting.cpp:131 es-core/src/Scripting.cpp:140; 0; shell spawns rc=1` | a new spawn: § The scripts' base | tool-run |
| 11 | the writes | 0 | 0 s | `es-core/CMakeLists.txt:122 es-core/CMakeLists.txt:257 es-core/src/AudioManager.cpp:539 es-core/src/AudioManager.cpp:610 es-core/src/FavoriteMusicManager.cpp:71 es-core/src/FavoriteMusicManager.cpp:115 es-core/src/InputManager.cpp:1225 es-core/src/InputManager.cpp:1232 es-core/src/Log.cpp:179; 9; 0; atomic rc=1` | a write was added: § The input's base | tool-run |
| 12 | the reads | 0 | 0 s | `41; 0; uncached rc=1` | a read changed its cache use: 3.11's base | tool-run |
| 13 | the input and the help bar | 0 | 0 s | `3; 6; 745 1001 1009 1011 1012 1077 1397 1398; 0; mHelp setOpacity rc=1` | a help-prompt definition or a `setOpacity` caller changed (L-21) | tool-run |
| 14 | the constants | 0 | 0 s | `es-core/src/components/MenuComponent.cpp:14:#define BUTTON_GRID_HORIZ_PADDING (Renderer::getScreenWidth()*0.022); es-core/src/components/MenuComponent.cpp:547:	float buttonGridWidth = (float)BUTTON_GRID_HORIZ_PADDING * buttons.size(); // initialize to padding; es-core/src/components/MenuComponent.cpp:555:		buttonGrid->setColWidthPerc(i, (buttons.at(i)->getSize().x() + BUTTON_GRID_HORIZ_PADDING) / buttonGridWidth);; e ...` | the two defines changed (L-13) | tool-run |
| 15 | the includes | 0 | 0 s | `18; 2; es-core/src/Window.cpp:29:#include "../es-app/src/ApiSystem.h"; not once: es-core/src/HelpPrompt.h; not once: es-core/src/LocaleES.cpp; not once: es-core/src/LocaleES.h; not once: es-core/src/Scripting.h; not once: es-core/src/gettext.h; not once: es-core/src/guis/GuiInfoPopup.cpp; not once: es-core/src/guis/GuiInfoPopup.h; not once: es-core/src/guis/GuiTextEditPopupKeyboard.cpp; not once: es-core/src/guis/Gui ...` | an include changed: the stand-in's fakes and `Window.cpp:29` | tool-run |
| 16 | the in-source gates | 0 | 1 s | `es-core/src/AudioManager.cpp:22 es-core/src/CECInput.cpp:3 es-core/src/CECInput.cpp:8 es-core/src/CECInput.cpp:23 es-core/src/CECInput.cpp:53 es-core/src/CECInput.cpp:94 es-core/src/CECInput.cpp:95 es-core/src/CECInput.cpp:154 es-core/src/CECInput.cpp:162 es-core/src/CECInput.cpp:175 es-core/src/CECInput.cpp:196 es-core/src/CECInput.cpp:281 es-core/src/CECInput.h:7 es-core/src/CECInput.h:24 es-core/src/GunManager.cpp ...` | a guard was added: the stand-in's branch list | tool-run |
| 17 | the non-ASCII bytes | 0 | 0 s | `28; git grep -P rc=0; AudioManager.cpp:3; GunManager.cpp:1; InputManager.cpp:2; guis/GuiTextEditPopupKeyboard.cpp:22; files with a non-ascii byte: 4; comment: AudioManager.cpp:3; comment: GunManager.cpp:1; comment: InputManager.cpp:2; files with a non-ascii comment line: 3` | a non-ASCII byte in a comment near `_()`: xgettext stops the image build (`es-code-traps.md`) | tool-run |
| 18 | the French | 0 | 0 s | `49:msgid "CANCEL" 3779:msgid "HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT." 3898:msgid "GAMEPAD %i" 3915:msgid "SET SELECT AS HOTKEY" 3918:msgid "DO NOT ASSIGN HOTKEY" 6923:msgid "CLEAR"; locale/lang/fr/LC_MESSAGES/emulationstation2.po:2207; es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without; es-untranslated rc=0; es-untranslated: 703 fork string(s) in the source, 703 with French, 0 withou ...` | a msgid lost its French (D-UI-051) | tool-run |
| 19 | the candidate lines | 0 | 0 s | `339 340; 1164; 66 78 94 143 181 196; 946 960; 1225 1232; 44 234 240; 134` | a lead's line moved: § The leads re-anchored | tool-run |
| 20 | the menu map | 0 | 1 s | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing; es-menu-map-check rc=0; 989 docs/es-menu-map.md; SOURCE_DIRS = ["es-app/src/guis", "es-core/src/guis"]` | a screen the map does not describe (D-UI-039) | tool-run |
| 21 | the compile | 0 | 0 s | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root); es-syntax-check rc=2; /home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682/es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory; plain g++ rc=1; pugixml root present` | the host gained a toolchain, or the first error moved: the stand-in's fakes | tool-run |
| 22 | STAGE C -- the lane's scripts, which do not exist at stage A | CANNOT | -- | `CANNOT at stage A: the three scripts below are the lane's stage-C inputs (stage-a/syntax-check.sh, tools/t35-build-tests.sh, stage-c/pl25-screensaver.py) and do not exist yet; each runs at stage C; (not run) bash docs/audits/*-epic-m6-es-core-window-input/stage-a/syntax-check.sh 2>&1 \| tail -n 46; (not run) bash docs/audits/*-epic-m6-es-core-window-input/tools/t35-build-tests.sh "$W" 2>&1 \| tail -n 10; (not run) pyth ...` | -- | -- |
| 23 | STAGE A, after the pointer is read -- the removal check: the lane's own tip, b51dd8a805 at stage A (the merge commit the dispatch comment and the pointer name, filling the brief's placeholder) | 0 | 0 s | `(the lane's own tip is b51dd8a805 at stage A: the merge commit the dispatch comment and the pointer name)` | the lane wrote under `packages/`, `projects/` or `tools/`, or in the ES worktree: § 8 | tool-run |
| 24 | (added at stage A) the ROCKNIX lines over the 96, which the gates run's expectation names and the block does not run | 0 | 0 s | `es-core/src/InputManager.cpp:585 es-core/src/Paths.cpp:76 es-core/src/Splash.h:10; 3` | a `ROCKNIX` gate was added or removed | tool-run |
| 25 | (added at stage A) the gates run's line count, which the block prints as one line | one line | -- | `128` | the gates list changed | tool-run |

**The generators, each seen to exit 1 on a constructed drift before it was trusted** (`stage-b/drift.sh` -> `stage-b/generators.txt`; (a) a wrong expectation, (b) the paths list with a cited file dropped, (c) the pin's paths read at the base, where the cited lines have moved):

| Generator | Clean | Its last line | (a) | (b) | (c) | proved: |
| --- | --- | --- | --- | --- | --- | --- |
| `tools/t35-coverage.py` | 0 | `generated, asserted: 96 rows, 22575 lines (grep -c rule); read tiers fork-added 1 / fork-modified 12 / upstream-carried 83; inventory fork-own 13 / upstream-carried 83` | `rows=95` -> 1: `FAIL t35-coverage: rows 96, expected 95` | without `Window.cpp` -> 1: `FAIL t35-coverage: rows 95, expected 96` | at `bccd715707` -> 1: `FAIL t35-coverage: es-core/CMakeLists.txt: 296 lines at bccd715707, inventory 303` | tool-run |
| `tools/t35-leads.py` | 0 | `generated, asserted: 29 leads (24 confirmed at the tree, 1 contradicted, the rest read or supported), 27 floor cases anchored, 22 run` | `cases=26` -> 1: `FAIL t35-leads: cases 27, expected 26` | without `Window.cpp` -> 1: `FAIL t35-leads: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-leads: es-core/src/Window.cpp:339 does not carry /mNotificationMessages\.back\(\)/ (reads: 'return;')` | tool-run |
| `tools/t35-surfaces.py` | 0 | `generated, asserted: 22 rows: 5 containers and the lock, 15 sites (one of them T34's component's, outside the 96), and T34's two held patches` | `sites=14` -> 1: `FAIL t35-surfaces: sites 15, expected 14` | without `Window.cpp` -> 1: `FAIL t35-surfaces: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-surfaces: es-core/src/Window.h:123 does not carry /std::vector<AsyncNotificationComponent\*> mAsyncNo` | tool-run |
| `tools/t35-input.py` | 0 | `generated, asserted: 7 write-site rows (5 writes, 2 reads the grep counts), 5 exists rows; the writes grep 9 hits` | `real_writes=7` -> 1: `FAIL t35-input: real_writes 5, expected 7` | without `InputManager.cpp` -> 1: `FAIL t35-input: es-core/src/InputManager.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-input: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-locks.py` | 0 | `generated, asserted: 67 lock lines in 11 files (4 includes, 2 `weak_ptr::lock`), 10 locks summarised, 7 threads` | `lines=66` -> 1: `FAIL t35-locks: lines 67, expected 66` | without `Window.cpp` -> 1: `FAIL t35-locks: lines 55, expected 67` | at `bccd715707` -> 1: `FAIL t35-locks: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-lifetimes.py` | 0 | `generated, asserted: 18 thread rows (4 detaches), 17 `delete this`, 6 posts, 8 raw pointers, 3 halves of #1305` | `detach=5` -> 1: `FAIL t35-lifetimes: detach 4, expected 5` | without `Window.cpp` -> 1: `FAIL t35-lifetimes: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-lifetimes: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-scripts.py` | 0 | `generated, asserted: 4 sites (4 `ProcessStartInfo` lines in the 96), direct shell spawns 0` | `shell_direct=1` -> 1: `FAIL t35-scripts: shell_direct 0, expected 1` | without `Scripting.cpp` -> 1: `FAIL t35-scripts: es-core/src/Scripting.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-scripts: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-words.py` | 0 | `generated, asserted: 86 lines in 10 files, 97 occurrences, 61 msgids, 0 without French; 27 glyph lines; 28 `pgettext`/`ngettext` lines, 0 without French` | `msgids=62` -> 1: `FAIL t35-words: msgids 61, expected 62` | without `Window.cpp` -> 1: `FAIL t35-words: lines 49, expected 86` | at `bccd715707` -> 1: `FAIL t35-words: es-core/src/LogPolicy.h not at bccd715707` | tool-run |
| `tools/t35-includes.py` | 0 | `generated, asserted: 51 headers' reach, 12 guard macros, 44 `.cpp` named once, 2 headers unregistered, 9 `# batocera` lines, 2 CMake `if(`, 3 `ROCKNIX` lines, 0 map titles` | `rocknix=4` -> 1: `FAIL t35-includes: rocknix 3, expected 4` | without `Window.cpp` -> 1: `FAIL t35-includes: es-core/src/Window.cpp is not in the paths list` | at `bccd715707` -> 1: `FAIL t35-includes: es-core/src/LogPolicy.h not at bccd715707` | tool-run |

**Stage C's runs** (read from their records, each figure asserted):

| Run | Exit | Wall | Figure | Note |
| --- | --- | --- | --- | --- |
| the stand-in over the 44 (`stage-a/syntax-check.sh`, the fakes under `stage-a/fakes/`, the pugixml root and rapidjson; udev, pulse, TTS, CEC and WIN32 not parsed) | 0 | 11 s | `t35-syntax-check: 44 file(s) checked, 44 rc 0, 0 not` | the first run (`syntax-check-first.out`) printed `37 rc 0, 7 not`: the seven stopped at the fakes' gaps, closed by `t35-sdl-more.h` and the T35 sections |
| the unit build (`tools/t35-build-tests.sh`) | 1 (window-input-tests' candidates, by design) | 41 s | `TOTAL: 249 test cases in 6 binaries` | es-unit-tests 185/185; es-file-tests 24/24; es-conf-tests 10/10; es-file-tests-win32 2/2; app-unit-tests 18/18 |
| `window-input-tests` before any fix | 1 | in the above | `10 cases, 3 passed, 7 failed` | the seven candidates FAIL at the pin: 3.1, 3.4, 3.5, 3.10, 3.11, 3.14, 3.19; 3.11's first ordering passed because the uncached read rewrites the entry (`FileSystemUtil.cpp:161-162`), now made second |
| 3.17 and 3.3 under ThreadSanitizer (`stage-c/tsan-posts.cpp` over the extracts; `stage-c/tsan-watchers.cpp` over the pin's `WatchersManager.cpp`) | 66, 66 | in the build | `tsan-posts`: WARNING: ThreadSanitizer: data race; `tsan-watchers`: WARNING: ThreadSanitizer: data race | posts: the erase loop's read (thread T2) against the post's reallocation under the mutex (T1); watchers: `WatchersManager.cpp:151` (the destructor's write) against `:161` (`run()`'s read) |
| 3.2 under AddressSanitizer (`stage-c/asan-watchers.cpp`, the pin's `WatchersManager.cpp`) | 0 | 1 s | `asan-watchers: done, 1 notification(s)`, no report (`stage-c/asan-watchers.out`) | PASS at the pin: the list lock spans the probe; the guard PL-01's fix must keep passing |
| 3.27, T33's `stage-c/pl25-screensaver.py` unchanged from `947ace1966` | 1 | 1 s | `heap-use-after-free a.cpp:14 in FileData::getImagePath[abi:cxx11]()` | FAIL at the pin as #1305 says; the script takes `SystemScreenSaver.cpp`'s path, not the worktree the brief's line passes |

**Stage E's runs** (read from their records, each figure asserted):

| Run | Exit | Wall | Figure | Note |
| --- | --- | --- | --- | --- |
| S0: the floor cases no stream holds (`floor-tests`, `tools/t35-floor-tests.cpp`, ruling 21), at the pin | 0 | in the build | `11 cases, 11 passed, 0 failed` | 3.6, 3.7 (two), 3.8, 3.9, 3.12, 3.13, 3.20, 3.22, 3.24, 3.25 PASS at the pin as the floor table expects; 3.26 no host case |
| S0: each floor case seen to fail on a constructed mutation (`stage-e/s0-mutations.txt`) | 1, 1, 1 | -- | ic_utils -> 3.7 fails; mb_ctor -> 3.20 fails; ip_fade -> 3.22 fails | toLower made a no-op; one say( call's text removed; FADE_DURATION 250 -> 500 |
| S0: the unit build at the pin (`stage-e/s0-floor.txt`) | 1 (window-input-tests' seven candidates, by design) | 49 s | `TOTAL: 260 test cases in 7 binaries` | the rapidjson root re-made from the source cache's tarball with the package's two header patches (document.h a8c29c92d1e89279, stage C's); the pugixml root printed |
| S0: 3.2's own `SAN` line at the pin (the brief's figure 2) | 0 | in the build | `SAN asan-watchers (-fsanitize=address): rc 0; no sanitizer report` | the line the stage-C record lacked |
| S0: 3.1's figure at the pin (the brief's figure 1) | -- | -- | `ResetComponent returned after 1495 ms` | 1,496 ms in `stage-c/build-tests.out`; the 1,491 ms the stage-C record quoted was the first direct run's console line, not kept; the records now quote the kept lines |
| S1 before (`stage-e/s1-before.txt`, at the pin, before the fix, ES `16dbac521`) | 1 | in the build | `window-input-tests`: `16 cases, 6 passed, 10 failed`; `TOTAL: 266 test cases in 7 binaries` | the stream's cases failing: S1 back on GAME DRIVE DETECTED with an id; S1 back on NEW DRIVE DETECTED with an id; S1 back on NEW DRIVE DETECTED without an id; `SAN tsan-posts` rc 66; `SAN tsan-watchers` rc 66; `SAN asan-watchers` rc 0 |
| S1 after (`stage-e/s1-after.txt`, at the tip 56aa398b8, after the fix, ES `56aa398b8`) | 1 | in the build | `window-input-tests`: `16 cases, 9 passed, 7 failed`; `TOTAL: 266 test cases in 7 binaries` | the stream's cases all pass; S1 back on GAME DRIVE DETECTED with an id; S1 back on NEW DRIVE DETECTED with an id; S1 back on NEW DRIVE DETECTED without an id no longer fail; `SAN tsan-posts` rc 66; `SAN tsan-watchers` rc 66; `SAN asan-watchers` rc 0 |
| S2 before (`stage-e/s2-before.txt`, at S1's tip 56aa398b8, before the fix, ES `56aa398b8`) | 1 | in the build | `window-input-tests`: `19 cases, 9 passed, 10 failed`; `TOTAL: 269 test cases in 7 binaries` | the stream's cases failing: 3.14 the toast queue drains in the order things happened; 3.16 an unrelated prompt sharing the action text; 3.16 the dpad's two halves; S2 a toast a card takes off the screen; `SAN tsan-posts` rc 66; `SAN tsan-watchers` rc 66; `SAN asan-watchers` rc 0 |
| S2 after (`stage-e/s2-after.txt`, at the tip 453dffd0a, after the fix, ES `453dffd0a`) | 1 | in the build | `window-input-tests`: `19 cases, 13 passed, 6 failed`; `TOTAL: 269 test cases in 7 binaries` | the stream's cases all pass; 3.14 the toast queue drains in the order things happened; 3.16 an unrelated prompt sharing the action text; 3.16 the dpad's two halves; S2 a toast a card takes off the screen no longer fail; `SAN tsan-posts` rc 0; `SAN tsan-watchers` rc 66; `SAN asan-watchers` rc 0 |

**Still owed:**

| Run | When | Figure expected |
| --- | --- | --- |
| 3.3 after its fix (3.17's came with S2: `SAN tsan-posts ... rc 0`) | stage E, S4 | no ThreadSanitizer report |
| the PASS halves of the seven | stage E | each candidate's PASS line after its fix |
| the streams' guest halves (`fix-walk-pending-image`) | the coordinator's integration window | S1's dialog after `z`, S2's toasts and French bar, S3's held screensaver, S5's argv file, S6's reconfigured file, S8's CLEAR and subtitle |

generated, asserted: 25 run blocks, 9 generators with three drifts each

## The guest cycle

- **The grant:** #682 comment 6540234733 (06:45 UTC), queued behind M7. The coordinator's 10:42 block fixed the order (slot 1 M7 native, slot 2 M7's RA guest, slot 3 T35, slot 4 M7's cloud-native guest). M7's slot 2 returned at 11:06:57. **START 11:07:40 UTC** (#682 comment 6542598902; the host file read at 11:07:26; the host-file line with the census `qemu 0, compilers 0, listeners 0`). **RETURN 11:31:00 UTC** (#682 comment 6542812230; the census `qemu 0, compilers 0, listeners 0`), inside the 11:42:40 bound.
- **The timer:** pid 3085742 armed at START for 11:42:41. It carried `--timeout 90`, which `tools/vm-stop` refuses (at most 60 s). That was found when my own stop failed at 11:24:57 (the first boot still up, the second boot refused the disk), then replaced by its PID with pid 3339644 at the same deadline and `--timeout 60` (`guest-cycle/helpers/stop-timer.sh`). It was stopped by its PID at the RETURN, unfired. Supervision was continuous, never 60 s apart.
- **The image:** `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (sha256 matching its `.sha256`), read from the guest as `BUILD_ID=069fc270442134fe771258418adf4e666e0473fb`, `BUILD_BRANCH=build/m7-signin-20261022-07`, at `640x480-0` (`guest-cycle/g01-identity.txt`). Every frame is **`image`** side (ES sha256 `25155163...1226`, M7's composition).
- **The network:** `restrict=on` plus `guestfwd=tcp:10.0.2.100:9010-tcp:127.0.0.1:9010`, read back from `/proc`. A `tcp:` guestfwd is one connection opened at QEMU's start, so after rclone's first connection the WebDAV did not answer (`curl` rc 28). G-02 and G-09 ran on the unreachable cloud's bounded outcomes, which still draw the card and the page.
- **G-01:** `640x480-0`; theme `es-theme-art-book-next`. The user `es_input.cfg` exists before any configuration (117,859 bytes, the shipped copy: PL-04 lowered). The shipped file has 0 `inputAction` lines. libudev is linked (1). No `/usr/bin/scripts` and no user scripts folder (PL-03 needs an added hook). `curl` is present. `proved: guest`.
- **G-02 and G-03:** under SYNCING SAVES AT STARTUP (`g02-01.png` RECEIVING · STARTING..., `g02-29.png` SENDING · STARTING..., 11:11:51 to 11:12:34), `POST /notify` sent T35 TOAST A then T35 TOAST B at 11:11:48 (guest clock). No toast was drawn while the card was up. After it left, **both appeared together, B above A** (`g02b-001.png`, 11:13:37): newest first, L-01/PL-02 on the image. The card's solid run is x 23 to 616 at row 60 (`tools/t35-png.py`), centred at 319.5 -- 0.9 W plus, by inference, the frame image's outset. `proved: guest`.
- **G-04:** REALLY RESTART EMULATIONSTATION? YES / NO (`g04-2-dialog.png`). B closed it and ES stayed pid 1605 (`g04-pids.txt`). MAIN MENU and QUIT at 640 draw no window help bar (`g04-0-menu-bottom.png`, `g04-1-quit-page.png`, L-21). `proved: guest`.
- **G-05: `CANNOT`.** REMOVE CONNECTION refuses with one OK while the automatic save syncs are on (`g05-4-dialog.png`), and a serial `set_setting cloudsaves.startup 0` did not reach ES's own copy (`g05-6-dialog2.png`). The two-button dialog was not reached. The candidates stay: REMOVE CONNECTION / CANCEL (`GuiMenu.cpp:8057-8058`), USE CONNECTION / CANCEL (`:8025`).
- **G-06:** the keyboard is full-screen at 640 (`g06-walk/03-folder-editor.png`). ESC closes it with SAVES FOLDER unchanged (`g06-1-after-esc.png`). `s` with the keyboard device types into the field rather than acting as X, so L-14's clear-and-commit is not shown by this route (`g06-3-after-s.png`). The startup card drew over the keyboard's field (PL-34). `proved: guest`.
- **G-07 (French):** VRAIMENT REDÉMARRER EMULATIONSTATION ? OUI / NON (`g07-1-quit-dialog-fr.png`). B kept ES pid 6597. The detect page fits at 640 (`g07-4-detect-fr.png`). The AZERTY keyboard shows EFFACER / ANNULER (`g07-walk/03-folder-editor.png`). `proved: guest`.
- **G-08:** HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT. at 640 (`g08-2-detect-page.png`). **One `sendkey x 1000` over the monitor held a key, and the page advanced** to CONFIGURING / KEYBOARD (`g08-3-after-hold.png`): the harness gap is closed. `proved: guest`.
- **G-09:**
  - The screensaver came up after about five idle minutes (`g02b-115.png`, 11:16:42). `shift` woke it with the carousel unmoved (`g09-2-after-shift.png`), and `down` then moved it (`g09-3-after-down.png`).
  - With SCREENSAVER AFTER at 60 s, **the screensaver started over VÉRIFICATION DE VOTRE CLOUD while its job ran** (`g09-4-page-t30.png` at 11:29:33, ÉCOULÉ 0:47; `g09-4-page-t45.png` black at 11:29:49): #1305's window half on the image. `proved: guest`.
- **G-10: `CANNOT`** (no pad).
- **G-11 (1280x800, `1280x800-0`):**
  - The keyboard is a box of about 0.78 W x 0.6 H with the help bar under it (`g11-walk/03-folder-editor.png`). The QUIT box is about 0.6 W wide, with OUI / NON (`g11-1-quit-dialog-1280.png`).
  - **T34 PL-05 reproduced:** the tabbed SCRAPEUR page's bar reads FERMER and RETOUR with a row and with the strip focused (`g11-4-scrapeur-row.png`, `g11-5-scrapeur-strip.png`).
  - The non-tabbed PARAMÈTRES AUDIO page shows FERMER, RETOUR, CHANGER and CHOISIR through the same window (`g11-3-scraper-tabs.png`), so the prompts are lost before the window (L-28). `proved: guest`.
- **G-12:** the disk retired (`guest-cycle/retired.txt`): `/workspace/tmp/m6-t35/guest/disk.qcow2`, 2,312,372,224 bytes, sha256 `c98ec34b491ff866f9d2e135af5374e7bb6cb7f34e695c42b3a77a6c4d1385e7`, now absent. The host's WebDAV is down by its pidfile. Leftover check: `qemu 0, compilers 0, listeners 0`.
- **Time to play** (for the retro): on the unreachable cloud the startup card stayed at STARTING... for about 100 s while the hub row reads AT STARTUP - SKIPPED, NO NETWORK (`g05-0-hub-bottom.png`). That is the cloud lane's bounded sync, recorded for its owner.

## The streams

**Stage E, as the coordinator's stream brief orders it** (`docs/reviews/briefs/t35-streams.md` at `0f9f8f69fe` on the coordinator's branch; twenty-one rulings, D-UI-134 to D-UI-137, Backlogs #1344 to #1347). One row per stream, written as each lands; each before and after line is the build script's own (`stage-e/sN-before.txt`, `sN-after.txt`), asserted by `tools/t35-runs.py` in § The runs, and each stream's other checks are `stage-e/sN-checks.txt`. Every guest half is `fix-walk-pending-image`: the coordinator's, at the integration window, on the image that carries the fix.

| Stream | Items and bugs | Positive before | ES commit | Positive after | `Already written:` | proved: | The guest half; patches and collisions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | PL-15, #1342 (ruling 5) | the drive dialogs' cases (`tools/t35-window-input-tests.cpp`, the pin's accelerator `guis/GuiMsgBox.cpp:116-134` over each call's labels read from `Window.cpp`): back binds YES, MERGE DRIVE on GAME DRIVE DETECTED with an id and YES, FORMAT & MERGE on both NEW DRIVE DETECTED forms -- `window-input-tests` 16 cases, 10 failed (the seven candidates and these three); 3.18 and the two NO-by-name guards PASS | `56aa398b8` (`Window.cpp`, 9 insertions, 6 deletions; the labels and their lambdas reordered, no word changed) | 16 cases, 7 failed (the seven candidates only): back binds NO, IGNORE THIS TIME (both with-id forms), NO, IGNORE, and NO by name; the stand-in 44 of 44; the lane's count 2 three-button calls without OK or NO in the 96, both now ending on the safe choice (es-app's 3 for #1344) | #1342's: a merge already applied by a back press is persisted for future boots and is indistinguishable from one chosen on purpose -- nothing migrated; the fix changes the dialog, not what an earlier press wrote | `fix-unit-test` | `fix-walk-pending-image`: `POST /storage/event` with a `REQUEST_MERGE` line, then `z`; a frame with the dialog closed and no `Merge requested` toast, and no merge request in the journal, at 640x480 and 1280x800 in English and French (the flow step: the drive dialog's back). No patch; no collision (`GuiMsgBox.cpp` untouched, so T34's `s3-msgbox.patch` is unaffected) |
| S2 | PL-02 #1338, PL-07 #1341, PL-25 #1354, PL-26 #1355 (rulings 1, 2, 15) | at S1's tip: `window-input-tests` 19 cases, 10 failed -- 3.14 (`values: CHECK( B second == A first )`), the interruption case (A on screen, B and C queued, a card: `values: CHECK( C queued == B queued )`), and 3.16's two (`left/right CHOOSE \| up/down CHOOSE == up/down/left/right CHOOSE`; the `a` prompt replaced); `SAN tsan-posts ... rc 66`, the first report the post's write of `mTimeSinceLastInput` against update's (`x_posts_post.inc:13` against `x_upd_idle.inc:2`), 3.17's race in its second phase | `453dffd0a` (`Window.cpp`, `Window.h`; 35 insertions, 11 deletions) | 19 cases, 6 failed (3.1, 3.4, 3.5, 3.10, 3.11, 3.19 only); `SAN tsan-posts (-fsanitize=thread): rc 0; no sanitizer report`, the PL-26 phase included; the stand-in 44 of 44; es-app's `main.cpp` syntax-only rc 0 against the atomic flag | nothing inherited (#1338, #1341, #1354, #1355): the queue, the posted functions, the prompt list and the idle count live in memory | `fix-unit-test` | `fix-walk-pending-image`: two `POST /notify` while a card is up, then a frame after it leaves with the toasts in the order posted; a list's help bar at 640x480 in French with the dpad prompt merged (the flow steps: the toast order after a card; the list's help bar). No patch. The one departure from the brief's words: the refresh event stays with the post (it ends the loop's `SDL_WaitEventTimeout`), `mSleeping` atomic for the post's read (`stage-e/s2-checks.txt`). Collision: T34's `s2-window.patch` hunks (`@@ -1149`, `@@ -1165`, `@@ -1245`) sit beside the re-queue edit and `Window.h`'s members; the hand-back dry-runs it |

At stage B the lane left this heading for the pause with the following, which the brief's rulings now dispose:

> Stage E: **written by the coordinator after stage D**, as for T21, T26, T32, T33 and T34. The lane leaves this heading and puts the following to the pause:
>
> - **Four register rows expected** (brief § 9), each put to the coordinator and none decided by the lane: F-ES-24's toast behind a long card; the re-queued toast's duration (L-01, 3.14; the order itself is D-UI-093's, already decided, so the pause rules only whether the fix lands); the second `BUTTON_GRID_HORIZ_PADDING` (L-13); and the CLEAR without a question (L-14).
> - **Rule-6 candidates, contained:** L-01 (pop the front), L-03 (take the lock), L-10 (log `item`), L-11 (probe outside the list lock, #1283's es-core half), L-24 (a stack event), L-06's `es_input.cfg` through `AtomicFile`, and L-07's read with `exists(path, false)` once 3.11 has run.
> - **The collision:** T34's `s2-window.patch` (#1310), which changes `createAsyncNotificationComponent`'s return. It touches 10 es-app callers in five lanes and the three doubles, so § 1 i names it in the hand-back.
> - **#1305:** the window's half (a start the top page can refuse) beside T33's and T2's halves, named for their owners.

## Positives

- `GuiMsgBox::deleteMeAndCall` copies the callback before `delete this` and calls the copy after (`guis/GuiMsgBox.cpp:286-292`): the safe shape, and the model for the other 16. None of them touches a member after the delete. `proved: tree`.
- Every `~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), and `removeGui` clears the mouse capture (`Window.cpp:86-87`), so a captured component freed under its page leaves no dangling pointer. `proved: tree`.
- `processPostedFunctions` copies and clears under the lock, then runs outside it (`Window.cpp:1292-1307`), so a post may post again without a deadlock. `proved: tree`.
- One floating surface at a time holds both ways (D-UI-093): a toast waits for the card (`:336-337`), and a card puts the toast's words back (`:1161-1165`). `proved: tree`; G-02 frames it.
- The window and T34's component compute the same centred position (`:1192`, `AsyncNotificationComponent.cpp:112`). `proved: tree`.
- `doOnFinish` masks its logged command (`InputManager.cpp:1270`). `configureEmulators` carries no device name (`:1481-1482`), so the blob it splices is index and hex only. `proved: tree`.
- All 61 msgids and all 28 `pgettext`/`ngettext` entries have their French at the pin. `proved: tool-run`.
- The logger and the watcher thread are joined (`Log.cpp:76-77` from `onExit`; `WatchersManager.cpp:154` from `stop()`). Every `.cpp` of the 96 is registered once in `es-core/CMakeLists.txt`. `proved: tree`.

## The #585 lines owed

One line per upstream-carried defect closed under rule 6, in the lane's shape, **never sent** (D-WORKFLOW-164, D-WORKFLOW-165). At stage B none is closed yet, so each is a line owed **if** the pause rules its fix. They are listed for the coordinator, beginning with T33's never-posted candidate:

- `es-core/src/watchers/WatchersManager.cpp:181-199` (`rocknix/master`): the watcher list lock is held across every `check()`, so `ResetComponent`/`GetComponent`/`Register`/`Unregister` wait on the interface thread for a network probe. Fix: snapshot under the lock and probe outside it, re-validating. Evidence: 3.1. This is T33's candidate and this slice's lock line.
- `es-core/src/Scripting.cpp:88-113` (`rocknix/master`): arguments are quoted only on a space and `"` is stripped, so `$`/backtick reach `/bin/sh -c`. Fix: single-quote every argument. Evidence: 3.4.
- `es-core/src/Window.cpp:339-340` (upstream's queue): the toast queue pops its newest. Fix: pop the front. Evidence: 3.14.
- `es-core/src/Window.cpp:1262-1274`: `unregisterPostedFunctions` walks `mFunctions` without the lock its two siblings take. Fix: take it. Evidence: 3.17.
- `es-core/src/InputManager.cpp:946`, `:960`: the approximate-match log reads the node before it is assigned. Fix: log `item`. Evidence: 3.10.
- `es-core/src/InputManager.cpp:795`: a `new SDL_Event` per F4 press, never freed. Fix: a stack event.
- `es-core/src/guis/GuiTextEditPopupKeyboard.cpp:14`: the second `BUTTON_GRID_HORIZ_PADDING`, **only if** the pause deletes or renames it.
- **No line** for the controllers blob: at the pin it carries no device name (L-20, contradicted).

**Stage E's lines, each stream's `git log -S` saying whose the line is** (ruling 19; never sent, the coordinator posts them after acceptance):

- **S1, PL-15 (#1342):** `es-core/src/Window.cpp:1568-1578`, `:1630-1648` (`rocknix/master`): GAME DRIVE DETECTED and NEW DRIVE DETECTED list NO, IGNORE THIS TIME / NO, IGNORE FOREVER / YES, MERGE DRIVE (or YES, FORMAT & MERGE), and no name is OK or NO, so `GuiMsgBox`'s back falls through to the last button: a merge kept for future boots, or the format's confirmation. Fix: YES first and the choice that changes nothing last, no word changed. Evidence: the drive dialogs' cases. Whose: `git log -S'NO, IGNORE THIS TIME'` names `a8513aec1` and `eeaa8616a` (Daniel Martin, 2026-03-24 and 2025-12-08), both ancestors of `cada856d86`: upstream ROCKNIX's.
- **S2, PL-02 (#1338):** the stage-B line for `Window.cpp:339-340` stands, now closed. Whose: the pop is `49efd94495` (blame) from `ac0fbeac8` (`git log -S'pop_back'`), both ancestors of `cada856d86`: upstream's. The re-queue (`:1163-1164`) is the fork's `c1c0d6ddcf`, so no line for that half.
- **S2, PL-07 (#1341):** the stage-B line for `Window.cpp:1262-1274` stands, now closed. Whose: `c5ceca49a8` (2021-05-13, *Fix potential crash with gameslists*), an ancestor of `cada856d86`: upstream's.
- **S2, PL-25 (#1354):** `es-core/src/Window.cpp:1032-1033` (`rocknix/master`): the help bar's dpad merge compares with `!=`, so the dpad's two halves with one action stay apart, and an unrelated prompt with that action is replaced by `up/down/left/right`. Fix: `==`. Evidence: 3.16's two cases. Whose: `8d7fb7b3e8` (2019-04-25, *the big merge*), an ancestor of `cada856d86`.
- **S2, PL-26 (#1355):** `es-core/src/Window.cpp:1284-1289` (`rocknix/master`): `postToUiThread` writes `mSleeping` and `mTimeSinceLastInput` from the posting thread while `update` and `render` read and write them unlocked. Fix: mark the wake under the queue's lock and apply it in `processPostedFunctions`; keep the refresh event with the post; `mSleeping` atomic for the post's read. Evidence: `tsan-posts`' first phase. Whose: `d1106f674a` and `8c25e2b086` (2022-02-05 and -06), ancestors of `cada856d86`.

## What T36 and T37 inherit

Brief § 5 item 3's items, with their lines:

1. **The provenance table:** 1 / 12 / 83, with both bases named (`cada856d86` against `rocknix/master`, `1750dded8c` against `batocera/master`). § Coverage, § The merge debt.
2. **The surfaces table:** the queue's two containers and the lock, and every enqueue, dequeue, layout and free with its invariant (`Window.cpp:293-1307`). § The surfaces.
3. **The input table:** every write site with its mechanism and atomicity, and every `exists(` of the input files with its writer (`InputManager.cpp:893`, `:1187`, `:1225`, `:1232`, `:1250`; `GuiDetectDevice.cpp:127`). § The input.
4. **The locks table:** every lock, its sites and order, and the interface-thread entry points that block (`WatchersManager.cpp:66`, `:78`, `:94`, `:143`, `.h:35`). § The locks.
5. **The lifetimes table:** 18 thread lines, 4 detaches, 17 `delete this`, 6 posts and 8 raw pointers. § The lifetimes.
6. **The scripts table:** the four `ProcessStartInfo` sites and `Platform.cpp:162-181`'s shell. § The scripts.
7. **The `window-input-tests` build recipe** (the doubles, the extracts, the pugixml root, the fakes the first errors forced): owed at stage C, `tools/t35-build-tests.sh`.
8. **The stand-in's rc per file over the 44:** owed at stage C, `stage-a/syntax-check.out`.
9. **The branches it did not parse:** `HAVE_UDEV` (23 lines), `_ENABLE_PULSE_` (7), `_ENABLE_TTS_` (5), `HAVE_LIBCEC` (11), and the WIN32 branches. § The structure's guards.
10. **The `exists` cache's answer for T36's `FileSystemUtil`:** misses are stored (`FileSystemUtil.cpp:296`, `:323`), and a writer outside `Utils::FileSystem` is invisible to the cache. Read at stage B; 3.11 proves it at stage C.
11. **`Window.cpp:29`'s disposition:** recorded as upstream's (L-04, D-UI-079). § The structure.
