# Research notes — M6.P2 T35, EmulationStation's window, input, settings and the rest of es-core (#682)

## Scope

**The slice.** `es-core/**` as `rest` (`{"globs": ["es:es-core/**"], "rest": true}`, area `interface`), at the pin `16dbac5211eea7e70db7394372033be2be7df829`, read from the distribution worktree stacked on the P1 branch at `2174265e9c` (the coordinator's `be119338ff` merged at `b51dd8a805`; HEAD `b1f2908a55` at stage A). The brief is `docs/reviews/briefs/es-core-window-input.md` at `8b5d9b9b62`, version 2.

**The membership block** (brief § 2, run verbatim from the brief's text; `stage-a/membership.sh`; its output `stage-a/membership.out`, rc 0, 2026-10-31 05:58:56Z). The first pass against `/dev/null` made the paths file from its own TSV; the second proved equality:

```
96 .qa-scratch/t35/paths.txt
mine: 96 paths.txt: 96 equal: True
only-mine: []
only-paths.txt: []
lines: 22575 reach: {'shipped': 96} tier: {'fork-own': 13, 'upstream-carried': 83} lang: {'cmake': 1, 'c-header': 51, 'c++': 44}
fork-own lines: 6759
read lines: 22575
wc -l 22567
grep -c 22575
95
95
 13 files changed, 247 insertions(+), 71 deletions(-)
 13 files changed, 247 insertions(+), 71 deletions(-)
```

- **Two counting rules:** `wc -l` sums to 22,567 and `grep -c ''` to 22,575, because eight files end without a newline (the § 5 run's list): `MultiStateInput.cpp` 52/53, `MultiStateInput.h` 18/19, `anim/StoryboardAnimator.cpp` 236/237, `anim/ThemeAnimation.h` 145/146, `anim/ThemeStoryboard.cpp` 241/242, `math/Vector2f.cpp` 38/39, `math/Vector4f.cpp` 106/107, `watchers/BatteryLevelWatcher.cpp` 8/9.
- **The `cat-file` counts:** 95 paths exist at the merge base `cada856d86` and 95 at `bccd715707`. `LogPolicy.h` is absent from both, so it is the fork's one added file.
- **The fork's delta** is `13 files changed, 247 insertions(+), 71 deletions(-)` against both bases. The § 5 run prints the same line a third time from `rocknix/master`'s side, with `added 1` and 12 numstat rows.
- **The tiers:** fork-added 1 (`LogPolicy.h`), fork-modified 12, upstream-carried 83; the inventory's `fork-own` 13 / 6,759 lines is the whole lines of the 13 files the fork touched.
- **`CLAIMS`:**
  - the thirteen of this slice, `in-T35 rest [('es-core-window-input', 35)]`;
  - `Settings.cpp`, `Settings.h`, `SystemConf.cpp`, `HttpReq.cpp`, `HttpReq.h`, `utils/AtomicFileUtil.{cpp,h}` and `es-app/src/ApiSystem.cpp`, all T21's;
  - `components/MenuComponent.cpp` and `components/AsyncNotificationComponent.cpp`, T34's;
  - `utils/FileSystemUtil.cpp`, `utils/StringUtil.cpp`, `resources/Font.cpp`, `renderers/Renderer.cpp` and `utils/OfflineProxyUrl.cpp`, T36's;
  - `es-app/src/CloudText.cpp`, T18's; `es-app/src/main.cpp`, T2's.

  That is 30 rows. **Delta:** the brief's prose also names two `GuiLoading.h` rows that the script's `named` list does not carry.
- **`ES-CORE BY SLICE`:** `96 paths 22575 lines (('es-core-window-input',), 'rest')`, `80 paths 21984 lines (('es-core-components',), 'non-rest')`, `58 paths 50840 lines (('es-core-utils-resources',), 'non-rest')`, `8 paths 3344 lines (('es-state-and-bridge',), 'non-rest')`.

**The bases** (the § 1 first commands and the § 5 run). The merge base with `rocknix/master` (`f6c542872e`) is `cada856d86`, and `bccd715707` is its parent. The merge base with `batocera/master` (`b2ceb55a7e`) is `1750dded8c`. The counts: `rev-list --count bccd715707..PIN` 725; `cada856d86..rocknix/master` 14; `bccd715707..cada856d86` 1; `upstream/master..rocknix/master` 15 (the stale ref).

**The § 5 runs' figures** (`stage-a/runs.out`; every run's `rc` and wall time beside it there):

| Run | Figure | rc |
| --- | --- | --- |
| the scope | 96; 44 `.cpp`; 51 `.h`; 1 other | 0 |
| the delta | `13 files changed, 247 insertions(+), 71 deletions(-)` three times; added 1; 12 numstat rows; 19 commits, 17 without merges, 2 merges | 0 |
| upstream's delta | upstream commits 0 (rc 1), numstat 0 (rc 1); identical to `rocknix/master` 83; to `cada856d86` 83; base to master 96; batocera commits on the 96: 12; batocera files 9; both-changed 6 | 0 |
| the other lanes | every stat line empty except T21's `es-core/CMakeLists.txt` `1 file changed, 5 insertions(+)`; T34's ref resolves now, to `dbe4c2db0f`, and its delta inside the 96 is empty | 0 |
| the strings | `_(" lines TOTAL 86 in 10 files`; 97 occurrences; per file `BindingManager.cpp:2 GunManager.cpp:6 InputManager.cpp:4 TextToSpeech.cpp:1 Window.cpp:37 guis/GuiDetectDevice.cpp:5 guis/GuiInputConfig.cpp:14 guis/GuiMsgBox.cpp:3 guis/GuiTextEditPopup.cpp:3 guis/GuiTextEditPopupKeyboard.cpp:11` | 0 |
| the log lines | `LOG(Log lines TOTAL 158 in 20 files` | 0 |
| the threads | 18 matching lines; `.detach(` 4; `postToUiThread` at `Window.cpp:1276 :1556 :1574 :1612 :1636`, `Window.h:91` | 0 |
| the process spawns | `InputManager.cpp:1272`, `Scripting.cpp:43 :131 :140`; shell spawns 0 (rc 1) | 0 |
| the writes | 9 lines (`CMakeLists.txt:122 :257`, `AudioManager.cpp:539 :610`, `FavoriteMusicManager.cpp:71 :115`, `InputManager.cpp:1225 :1232`, `Log.cpp:179`); `AtomicFile::` 0 (rc 1) | 0 |
| the reads | `FileSystem::exists(` 41; uncached 0 (rc 1) | 0 |
| the input and help bar | `getHelpPrompts` 3; `input(InputConfig` 6; `mHelp->` at `745 1001 1009 1011 1012 1077 1397 1398`; `mHelp->setOpacity` 0 (rc 1) | 0 |
| the constants | `MenuComponent.cpp:14` 0.022 and `GuiTextEditPopupKeyboard.cpp:14` 0.0052083333 (use `:220`); `Window.cpp:1181` `PADDING_H`, `:1192` the card's `posX`; `GuiInfoPopup.cpp:17-18` 0.9f / 0.2f; `GuiMsgBox.cpp:21-23` 0.6f / 0.8f / 4 | 0 |
| the includes | SDL/VLC/GL angle lines 18; quoted 2; `Window.cpp:29:#include "../es-app/src/ApiSystem.h"`; `named-0-times (or more than once): 9` -- `HelpPrompt.h`, `Scripting.h` and the seven `# batocera` entries; `if(` at `278 287` | 0 |
| the gates | 128 items; the `ROCKNIX` lines 3 (`InputManager.cpp:585`, `Paths.cpp:76`, `Splash.h:10`) | 0 |
| the non-ASCII bytes | 28 (git grep -P rc 0); 4 files (`AudioManager.cpp:3`, `GunManager.cpp:1`, `InputManager.cpp:2`, `guis/GuiTextEditPopupKeyboard.cpp:22`); comment lines in 3 files | 0 |
| the French | `49 CANCEL`, `3779 HOLD A BUTTON ON YOUR DEVICE TO CONFIGURE IT.`, `3898 GAMEPAD %i`, `3915 SET SELECT AS HOTKEY`, `3918 DO NOT ASSIGN HOTKEY`, `6923 CLEAR`; `^msgid` 2207; `es-untranslated` 706 of 706 (rc 0) and 703 of 703 against `cada856d86` (rc 0) | 0 |
| the candidate lines | `339 340`; `1164`; the lock grep `66 78 94 143 181 196` (the brief's comment names `181` and `196`; the others are § 2's other acquisitions); `946 960`; `1225 1232`; `say(` `44 234 240` (three lines, as correction 7 states); `134` | 0 |
| the menu map | `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (rc 0); the map 989 lines; `SOURCE_DIRS = ["es-app/src/guis", "es-core/src/guis"]` | 0 |
| the compile | `es-syntax-check: no build root at /nonexistent (ES_BUILD_ROOT, --root)` rc 2 (#1137); plain `g++` on `GuiMsgBox.cpp`: `es-core/src/InputConfig.h:6:10: fatal error: SDL_joystick.h: No such file or directory`, rc 1; the pugixml root present | 0 |
| STAGE C | `CANNOT` at stage A: the stand-in, the build script and the screensaver script are the lane's stage-C inputs | -- |
| the removal check | with the lane's own tip `b51dd8a805`: the distribution's `packages projects tools` diff empty; the ES diff against the pin empty | 0 |

## Read in this session (`working-principles.md` § Pre-flight)

- **Stage A:** the dispatch comment (#682 comment 6539807425), whole; the pointer; the brief at `8b5d9b9b62`, whole, § 10 first; the issue states of § 3 item 9 (`stage-a/issues.out`).
- **The rules:** the session loaded its rules at start from the T5 worktree. Six rule files in this worktree are newer -- `device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide` and `generic-x64-vm-testing` -- and their newer hunks were read here at stage A (the sandbox's `--clearenv`; a count is a claim about one tree; the granted window names what stops the guest; the stub checked against the unfixed code; `rc=$?` on its own line; the widened mask; the added-lines non-ASCII check; curl's header length; the image versus the read tree).
- **Owed at stage B,** before `02`'s sections are written: the § 3 item 1 table's rule sections at their cited lines in this worktree, with a moved line recorded beside the one the brief cites (§ 3 item 1's own instruction), the register and `tools/archaeology` reads of § 3 item 2, the map (item 3), the blindspots (item 4), the tests (item 5), the walks (item 6), the French (item 7, the parser re-run), the audits (item 8) and time to play (item 10). Each is named here as it is read.
