# Punch list (Phases 5 and 6) — M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)

Written by `tools/t35-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 the queue and its surfaces, Q2 the input's writes and commands, Q3 the watchers' lock, Q4 lifetimes, Q5 scripts and the shell, Q6 the popups and the words, Q7 cost, structure and merge debt). Every item is **Open** until the stage-D pause disposes it.

reviewed-at-es: 16dbac5211eea7e70db7394372033be2be7df829

## PL-01: A watcher's probe holds the list lock, and the interface thread waits for it

- **Severity:** Medium; **category:** Locks; **question:** Q3
- **Source finding:** L-11, 3.1, #1283's es-core half
- **Lines at the pin:** `watchers/WatchersManager.cpp:181-199` against `:66`, `:78`, `:94`, `:143`, `.h:35`
- **Owner:** T35 (#1283's es-core half; the observers es-app's)
- **What is wrong:** `run()` holds `mWatchersLock` across every `check()` (a network or battery probe) and then takes `mNotificationLock` inside it; `RegisterComponent`, `UnregisterComponent`, `ResetComponent`, `GetComponent` and the destructor take the same lock from the interface thread. 3.1 at the pin: `ResetComponent` returned after **1,491 ms** behind a 1.5 s probe. A real probe's bound is its network timeout.
- **Proposed disposition:** a `bug` under rule 6: snapshot the due watchers under the lock, probe outside it, re-validate before writing back (EP-13's `WatcherInfo` lifetime kept), and make `mRunning`/`mPaused` atomic; 3.1 the covering case, 3.3 (TSan) beside it, 3.2 (ASan) owed
- **proved:** fixture (3.1 FAIL at the pin; 3.3 TSan: `WatchersManager.cpp:151` writes `mRunning` while `:161` reads it)

## PL-02: The toast queue drains newest first, against D-UI-093's decided row

- **Severity:** Medium; **category:** Surfaces; **question:** Q1
- **Source finding:** L-01, 3.14
- **Lines at the pin:** `Window.cpp:339-340` against `:334-335` and `decision-register.md:404`; `:1159-1160`
- **Owner:** T35 (upstream's pop, the fork's rule)
- **What is wrong:** `processNotificationMessages` takes `back()` and `pop_back()`; D-UI-093 says *the order is the order things happened*. Two toasts queued under a card (a pad connected then disconnected) show in reverse. 3.14 at the pin: B shown before A.
- **Proposed disposition:** a `bug` under rule 6: pop the front, and reverse the re-queue loop at `:1163-1164` so a returned toast keeps its place; 3.14 the covering case; a #585 line
- **proved:** fixture (3.14 FAIL at the pin)

## PL-03: A script argument reaches /bin/sh unquoted, so $( ) and backticks in a file name run

- **Severity:** Medium; **category:** Scripts; **question:** Q5
- **Source finding:** L-18, 3.4, T2 FD-9/FD-19
- **Lines at the pin:** `Scripting.cpp:92-113`, `:137-148`; `utils/Platform.cpp:162-181` (T36's)
- **Owner:** T35 with T2 (the callers' arguments)
- **What is wrong:** `executeScript` quotes an argument only when it contains a space and strips every `"`; `ProcessStartInfo::run` hands the line to `system()` or `/bin/sh -c`. A ROM `a$(id)b.zip` or a scraped name with a backtick is expanded by the shell whenever any script sits in an event folder. 3.4 at the pin: the argument arrives unquoted. Medium because it needs a hook present; G-01 reads whether the image ships one under `/usr/bin/scripts/`.
- **Proposed disposition:** a `bug` under rule 6: single-quote every argument (with `'` escaped) and the script path; 3.4 the covering case; a #585 line
- **proved:** fixture (3.4 FAIL at the pin)

## PL-04: A file written by pugixml after a cached miss reads as absent for the rest of the session

- **Severity:** Medium; **category:** Input; **question:** Q2
- **Source finding:** L-07, 3.11
- **Lines at the pin:** `InputManager.cpp:893`, `:1187`, `:1225`, `:1239`, `:1250`; `utils/FileSystemUtil.cpp:296`, `:323` (T36's)
- **Owner:** T35 (the three reads); the cache T36's
- **What is wrong:** With the cache on, a first `exists(es_input.cfg)` that misses is remembered; `save_file` writes through `fopen`, so the cache never learns of the file. On a device whose user `es_input.cfg` did not exist at startup, the second pad configured in the session skips the merge at `:1187` and its save keeps that pad alone; `loadInputConfig` after the write (`:1239`) and `doOnFinish` (`:1250`) read the same miss. 3.11 at the pin: the cached read stays false after the write.
- **Proposed disposition:** a `bug` under rule 6: `exists(path, false)` at `:893`, `:1187`, `:1250` (the `es-code-traps.md` § Three things a font is not rule); 3.11 the covering case; G-01 reads the precondition on the image
- **proved:** fixture (3.11 FAIL at the pin)

## PL-05: The window's half of #1305: the screensaver starts over a page that owns the screen

- **Severity:** Medium; **category:** Lifetimes; **question:** Q4
- **Source finding:** L-27, 3.27, #1305
- **Lines at the pin:** `Window.cpp:777-779`, `:1091-1105`, `:1107-1138` (`:1117`); `SystemScreenSaver.cpp:342-358` (T33's); `SystemData.cpp:459-473` (T2's)
- **Owner:** T35 (the window's half); T33's and T2's halves
- **What is wrong:** The screensaver starts from `render()` on idle time alone; each page is told and cannot refuse; the slideshow's `FileData` list is cleared only when it stops. A transfer's rescan then deletes a game the next pick reads. 3.27 at the pin: `heap-use-after-free ... in FileData::getImagePath`.
- **Proposed disposition:** #1305 (open, `bug`): the window's half proposed for the pause (a start the top page can hold off); T33's and T2's halves named for their owners; 3.27 PASS when one half lands
- **proved:** fixture (3.27 FAIL at the pin)

## PL-06: The window's teardown frees no card and no popup, and the holders keep raw pointers

- **Severity:** Medium; **category:** Lifetimes; **question:** Q4
- **Source finding:** L-02, T2 PC-1
- **Lines at the pin:** `Window.cpp:188-207`, `:49-63`, `:1246-1248`; the holders in es-app (§ The surfaces)
- **Owner:** T35 (the teardown); the holders T18's, T20's, T34's
- **What is wrong:** `deinit` and `~Window` leave `mAsyncNotificationComponent` and `mNotificationPopups` as they are; the one free is `:1248`. A card alive at `deinit` is drawn again at the next `init()`; a holder's late call after `:1248` is a use after free the card cannot detect.
- **Proposed disposition:** a design ruling at the pause: T34's `s2-window.patch` (#1310) is a collision (10 es-app callers, 3 doubles); the window-side alternative frees cards and popups in `deinit` and refuses a close after it
- **proved:** tree

## PL-07: `unregisterPostedFunctions` walks the posted functions without their lock

- **Severity:** Low; **category:** Lifetimes; **question:** Q4
- **Source finding:** L-03, 3.17
- **Lines at the pin:** `Window.cpp:1262-1274` against `:1278`, `:1296`
- **Owner:** T35
- **What is wrong:** `postToUiThread` and `processPostedFunctions` take `mNotificationMessagesLock`; the erase loop does not. A worker posting while a page unregisters races the vector.
- **Proposed disposition:** a `bug` under rule 6: take the lock; 3.17 (TSan) the covering case
- **proved:** fixture (3.17 TSan at the pin: the erase loop's read against the post's reallocation under the mutex)

## PL-08: The input files are written in place, none atomically

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-06
- **Lines at the pin:** `InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:71`, `:115`
- **Owner:** T35
- **What is wrong:** Five writes, `AtomicFile::` 0. A cut `es_input.cfg` fails to parse: the pad reads as unconfigured and the next save keeps one device. The grep's seven sites include two read-mode `fopen`s.
- **Proposed disposition:** a pause ruling (D-CLOUD-078's family): `es_input.cfg` through the fork's `AtomicFile`, the rest recorded
- **proved:** tree

## PL-09: The approximate-match log reads the node before it is assigned

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-10, 3.10
- **Lines at the pin:** `InputManager.cpp:946`, `:960`
- **Owner:** T35 (upstream's lines, rule 6)
- **What is wrong:** Both lines log `configNode`'s attributes one line before `configNode = item`: empty fields. 3.10 at the pin: no device named.
- **Proposed disposition:** log `item`; 3.10 the covering case; a #585 line
- **proved:** fixture (3.10 FAIL at the pin)

## PL-10: F4 leaks one SDL_Event per press

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-24
- **Lines at the pin:** `InputManager.cpp:795`
- **Owner:** T35 (upstream's line, rule 6)
- **What is wrong:** `new SDL_Event()` is never freed; `SDL_PushEvent` copies.
- **Proposed disposition:** a stack event; a #585 line
- **proved:** tree

## PL-11: One macro name, two values: the keyboard's button padding

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-13, 3.19, T34 PL-16
- **Lines at the pin:** `guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` against `components/MenuComponent.cpp:14` (T34's)
- **Owner:** T35 (the define); T34's comment names it
- **What is wrong:** `BUTTON_GRID_HORIZ_PADDING` is `0.022 W` in the menu and `0.0052083333 W` in the keyboard: 14.08 px against 3.33 px at 640. 3.19 at the pin: the two differ.
- **Proposed disposition:** a pause ruling: the keyboard's own name (the value is its design), or one definition
- **proved:** fixture (3.19 FAIL at the pin)

## PL-12: CLEAR and the keyboard's `x` commit an empty value with no question

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-14
- **Lines at the pin:** `guis/GuiTextEditPopupKeyboard.cpp:392-397`, `:491-496`; `guis/GuiTextEditPopup.cpp:34`
- **Owner:** the pause (the lanes' fields: the cloud folder, the Wi-Fi key)
- **What is wrong:** One press empties the field and submits it; `es-ui-style-guide.md` § Confirmations asks a consequential action to ask.
- **Proposed disposition:** a pause ruling (a register row); G-06 frames it on the image
- **proved:** tree; guest owed

## PL-13: The re-queued toast returns with a fresh default duration

- **Severity:** Low; **category:** Surfaces; **question:** Q1
- **Source finding:** L-01, 3.14 (second case)
- **Lines at the pin:** `Window.cpp:1164`
- **Owner:** T35
- **What is wrong:** A toast half-read and taken off by a new card comes back whole, not for its remainder. Recorded as by design; costs seconds, loses no words.
- **Proposed disposition:** recorded as written; the pause may rule otherwise
- **proved:** fixture (PASS, recorded)

## PL-14: F-ES-24: every toast waits while any card is up, a long upstream card included

- **Severity:** Low; **category:** Surfaces; **question:** Q1
- **Source finding:** F-ES-24, brief § 9
- **Lines at the pin:** `Window.cpp:336-337`
- **Owner:** the pause
- **What is wrong:** The hasher's minutes-long card holds every toast behind it (D-UI-079 keeps that card as upstream has it). Recorded Low on 2026-09-25 and never dispositioned.
- **Proposed disposition:** a pause ruling: stands, or a bound (brief § 9's first register row)
- **proved:** tree

## PL-15: Back on a dialog without OK or NO takes the last button, and an unconfigured pad's any button fires it

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-12, 3.18
- **Lines at the pin:** `guis/GuiMsgBox.cpp:116-134`, `:257`
- **Owner:** upstream's; the callers choose labels
- **What is wrong:** The accelerator's third branch binds the last button; `:257` fires it for any button of an unconfigured pad.
- **Proposed disposition:** recorded; G-04 and G-05 frame the behaviour
- **proved:** tree; guest owed

## PL-16: The configuration page's subtitle numbers the SDL instance, not the seat

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-17, 3.21
- **Lines at the pin:** `guis/GuiInputConfig.cpp:134`
- **Owner:** T35 (upstream's line, rule 6)
- **What is wrong:** `GAMEPAD %i` prints `getDeviceId() + 1`; a third pad plugged in reads GAMEPAD 3 whatever its seat.
- **Proposed disposition:** the seat or the name; a #585 line
- **proved:** tree

## PL-17: The per-event `quit` scripts do not wait

- **Severity:** Low; **category:** Scripts; **question:** Q5
- **Source finding:** L-18
- **Lines at the pin:** `Scripting.cpp:142`, `:177`
- **Owner:** T35
- **What is wrong:** The per-event pass passes `""` as the event name, so `waitForExit = (eventName == "quit")` is false there even for `quit`; only the single-script pass waits.
- **Proposed disposition:** a pause question; recorded
- **proved:** tree

## PL-18: A per-event folder runs every file in it

- **Severity:** Low; **category:** Scripts; **question:** Q5
- **Source finding:** L-18, 3.5
- **Lines at the pin:** `Scripting.cpp:169-178`
- **Owner:** T35
- **What is wrong:** The extension filter is inside `#if WIN32`; on the device a `notes.txt` is handed to the shell. 3.5 at the pin: it is run.
- **Proposed disposition:** a pause ruling: the single-script pass's filter for both passes; 3.5 the covering case
- **proved:** fixture (3.5 FAIL at the pin)

## PL-19: `doOnFinish` runs its commands synchronously on the interface thread, inside the joystick lock on a hot-plug write

- **Severity:** Low; **category:** Locks; **question:** Q3
- **Source finding:** L-08, 3.13
- **Lines at the pin:** `InputManager.cpp:1272`, `:485-623`, `:605`
- **Owner:** upstream's; recorded
- **What is wrong:** A slow `onfinish` command freezes the interface; reached from the rebuild it runs with `mJoysticksLock` held.
- **Proposed disposition:** recorded; G-01 counts the shipped `inputAction` lines
- **proved:** tree

## PL-20: Two names for the hotkey

- **Severity:** Low; **category:** Input; **question:** Q2
- **Source finding:** L-09, 3.12
- **Lines at the pin:** `InputManager.cpp:1105-1107`; `guis/GuiInputConfig.cpp:73`, `:273`, `:279`
- **Owner:** T3 (the templates)
- **What is wrong:** The SDL-mapping fallback writes `hotkey`, the configuration page `hotkeyenable`.
- **Proposed disposition:** recorded for T3
- **proved:** tree

## PL-21: Four keyboard debug chords run with their gate commented out

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-05
- **Lines at the pin:** `Window.cpp:262-281`
- **Owner:** upstream's (outside the lanes)
- **What is wrong:** Ctrl+G/T/I/M change the screen with no setting.
- **Proposed disposition:** recorded (D-UI-079)
- **proved:** tree

## PL-22: es-core reaches into es-app, and four detached workers capture the window

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-04
- **Lines at the pin:** `Window.cpp:29`, `:1554-1637`
- **Owner:** upstream ROCKNIX's (outside the lanes)
- **What is wrong:** `#include "../es-app/src/ApiSystem.h"`; `processStorageRequest`'s workers capture `this` and post back; nothing joins them.
- **Proposed disposition:** recorded (D-UI-079); `Window.cpp:29`'s disposition
- **proved:** tree

## PL-23: A rule sentence still calls the card top-right

- **Severity:** Low; **category:** Structure; **question:** Q7
- **Source finding:** L-22
- **Lines at the pin:** `.claude/rules/es-native-ui.md:30` against `Window.cpp:1192`
- **Owner:** the coordinator's sweep
- **What is wrong:** The card is centred at the pin, and the same rule says so at `:191-197`.
- **Proposed disposition:** the coordinator's sweep (`tools/archaeology --reversal`)
- **proved:** tree

## PL-24: A dialog speaks its text twice

- **Severity:** Low; **category:** Words; **question:** Q6
- **Source finding:** L-16, 3.20
- **Lines at the pin:** `guis/GuiMsgBox.cpp:44`, `:234`, `:240`
- **Owner:** upstream's
- **What is wrong:** Three `say(` calls in the constructor (TTS compiled out on the image).
- **Proposed disposition:** recorded
- **proved:** tree

## Phase 7 resolution gate

| Item | Outcome | Evidence |
| --- | --- | --- |
| PL-01 | Open | the stage-D pause disposes it |
| PL-02 | Open | the stage-D pause disposes it |
| PL-03 | Open | the stage-D pause disposes it |
| PL-04 | Open | the stage-D pause disposes it |
| PL-05 | Open | the stage-D pause disposes it |
| PL-06 | Open | the stage-D pause disposes it |
| PL-07 | Open | the stage-D pause disposes it |
| PL-08 | Open | the stage-D pause disposes it |
| PL-09 | Open | the stage-D pause disposes it |
| PL-10 | Open | the stage-D pause disposes it |
| PL-11 | Open | the stage-D pause disposes it |
| PL-12 | Open | the stage-D pause disposes it |
| PL-13 | Open | the stage-D pause disposes it |
| PL-14 | Open | the stage-D pause disposes it |
| PL-15 | Open | the stage-D pause disposes it |
| PL-16 | Open | the stage-D pause disposes it |
| PL-17 | Open | the stage-D pause disposes it |
| PL-18 | Open | the stage-D pause disposes it |
| PL-19 | Open | the stage-D pause disposes it |
| PL-20 | Open | the stage-D pause disposes it |
| PL-21 | Open | the stage-D pause disposes it |
| PL-22 | Open | the stage-D pause disposes it |
| PL-23 | Open | the stage-D pause disposes it |
| PL-24 | Open | the stage-D pause disposes it |

## punch_index

```yaml
punch_index:
- id: PL-01
  severity: "Medium"
  category: Locks
  question: Q3
  source_finding: "L-11, 3.1, #1283's es-core half"
  outcome: "open"
- id: PL-02
  severity: "Medium"
  category: Surfaces
  question: Q1
  source_finding: "L-01, 3.14"
  outcome: "open"
- id: PL-03
  severity: "Medium"
  category: Scripts
  question: Q5
  source_finding: "L-18, 3.4, T2 FD-9/FD-19"
  outcome: "open"
- id: PL-04
  severity: "Medium"
  category: Input
  question: Q2
  source_finding: "L-07, 3.11"
  outcome: "open"
- id: PL-05
  severity: "Medium"
  category: Lifetimes
  question: Q4
  source_finding: "L-27, 3.27, #1305"
  outcome: "open"
- id: PL-06
  severity: "Medium"
  category: Lifetimes
  question: Q4
  source_finding: "L-02, T2 PC-1"
  outcome: "open"
- id: PL-07
  severity: "Low"
  category: Lifetimes
  question: Q4
  source_finding: "L-03, 3.17"
  outcome: "open"
- id: PL-08
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-06"
  outcome: "open"
- id: PL-09
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-10, 3.10"
  outcome: "open"
- id: PL-10
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-24"
  outcome: "open"
- id: PL-11
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-13, 3.19, T34 PL-16"
  outcome: "open"
- id: PL-12
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-14"
  outcome: "open"
- id: PL-13
  severity: "Low"
  category: Surfaces
  question: Q1
  source_finding: "L-01, 3.14 (second case)"
  outcome: "open"
- id: PL-14
  severity: "Low"
  category: Surfaces
  question: Q1
  source_finding: "F-ES-24, brief § 9"
  outcome: "open"
- id: PL-15
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-12, 3.18"
  outcome: "open"
- id: PL-16
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-17, 3.21"
  outcome: "open"
- id: PL-17
  severity: "Low"
  category: Scripts
  question: Q5
  source_finding: "L-18"
  outcome: "open"
- id: PL-18
  severity: "Low"
  category: Scripts
  question: Q5
  source_finding: "L-18, 3.5"
  outcome: "open"
- id: PL-19
  severity: "Low"
  category: Locks
  question: Q3
  source_finding: "L-08, 3.13"
  outcome: "open"
- id: PL-20
  severity: "Low"
  category: Input
  question: Q2
  source_finding: "L-09, 3.12"
  outcome: "open"
- id: PL-21
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-05"
  outcome: "open"
- id: PL-22
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-04"
  outcome: "open"
- id: PL-23
  severity: "Low"
  category: Structure
  question: Q7
  source_finding: "L-22"
  outcome: "open"
- id: PL-24
  severity: "Low"
  category: Words
  question: Q6
  source_finding: "L-16, 3.20"
  outcome: "open"
```
