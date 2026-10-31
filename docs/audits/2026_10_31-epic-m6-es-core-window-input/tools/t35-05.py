"""Write 05-punch-list.md (#682) from one item table: each item's section, the Phase 7
resolution gate (every item Open before stage D's issue exists), and the punch_index YAML
(question: in the brief's § 4 numbering). T34's t34-05.py's shape. Asserts unique ids, a
known severity and question per item, and the three views agreeing.
    t35-05.py"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEV = ("Critical", "High", "Medium", "Low")
# (title, severity, category, question, source, lines at the pin, owner, what is wrong, proposed disposition, proved)
I = [
    ("A watcher's probe holds the list lock, and the interface thread waits for it", "Medium", "Locks", "Q3", "L-11, 3.1, #1283's es-core half",
     "`watchers/WatchersManager.cpp:181-199` against `:66`, `:78`, `:94`, `:143`, `.h:35`", "T35 (#1283's es-core half; the observers es-app's)",
     "`run()` holds `mWatchersLock` across every `check()` (a network or battery probe) and then takes `mNotificationLock` inside it; `RegisterComponent`, `UnregisterComponent`, `ResetComponent`, `GetComponent` and the destructor take the same lock from the interface thread. 3.1 at the pin: `ResetComponent` returned after **1,491 ms** behind a 1.5 s probe. A real probe's bound is its network timeout.",
     "a `bug` under rule 6: snapshot the due watchers under the lock, probe outside it, re-validate before writing back (EP-13's `WatcherInfo` lifetime kept), and make `mRunning`/`mPaused` atomic; 3.1 the covering case, 3.3 (TSan) beside it, 3.2 (ASan) owed", "fixture (3.1 FAIL at the pin; 3.3 TSan: `WatchersManager.cpp:151` writes `mRunning` while `:161` reads it)"),
    ("The toast queue drains newest first, against D-UI-093's decided row", "Medium", "Surfaces", "Q1", "L-01, 3.14",
     "`Window.cpp:339-340` against `:334-335` and `decision-register.md:404`; `:1159-1160`", "T35 (upstream's pop, the fork's rule)",
     "`processNotificationMessages` takes `back()` and `pop_back()`; D-UI-093 says *the order is the order things happened*. Two toasts queued under a card (a pad connected then disconnected) show in reverse. 3.14 at the pin: B shown before A.",
     "a `bug` under rule 6: pop the front, and reverse the re-queue loop at `:1163-1164` so a returned toast keeps its place; 3.14 the covering case; a #585 line", "fixture (3.14 FAIL at the pin)"),
    ("A script argument reaches /bin/sh unquoted, so $( ) and backticks in a file name run", "Medium", "Scripts", "Q5", "L-18, 3.4, T2 FD-9/FD-19",
     "`Scripting.cpp:92-113`, `:137-148`; `utils/Platform.cpp:162-181` (T36's)", "T35 with T2 (the callers' arguments)",
     "`executeScript` quotes an argument only when it contains a space and strips every `\"`; `ProcessStartInfo::run` hands the line to `system()` or `/bin/sh -c`. A ROM `a$(id)b.zip` or a scraped name with a backtick is expanded by the shell whenever any script sits in an event folder. 3.4 at the pin: the argument arrives unquoted. Medium because it needs a hook present; G-01 reads whether the image ships one under `/usr/bin/scripts/`.",
     "a `bug` under rule 6: single-quote every argument (with `'` escaped) and the script path; 3.4 the covering case; a #585 line", "fixture (3.4 FAIL at the pin)"),
    ("A file written by pugixml after a cached miss reads as absent for the rest of the session", "Medium", "Input", "Q2", "L-07, 3.11",
     "`InputManager.cpp:893`, `:1187`, `:1225`, `:1239`, `:1250`; `utils/FileSystemUtil.cpp:296`, `:323` (T36's)", "T35 (the three reads); the cache T36's",
     "With the cache on, a first `exists(es_input.cfg)` that misses is remembered; `save_file` writes through `fopen`, so the cache never learns of the file. On a device whose user `es_input.cfg` did not exist at startup, the second pad configured in the session skips the merge at `:1187` and its save keeps that pad alone; `loadInputConfig` after the write (`:1239`) and `doOnFinish` (`:1250`) read the same miss. 3.11 at the pin: the cached read stays false after the write.",
     "a `bug` under rule 6: `exists(path, false)` at `:893`, `:1187`, `:1250` (the `es-code-traps.md` § Three things a font is not rule); 3.11 the covering case; G-01 reads the precondition on the image", "fixture (3.11 FAIL at the pin)"),
    ("The window's half of #1305: the screensaver starts over a page that owns the screen", "Medium", "Lifetimes", "Q4", "L-27, 3.27, #1305",
     "`Window.cpp:777-779`, `:1091-1105`, `:1107-1138` (`:1117`); `SystemScreenSaver.cpp:342-358` (T33's); `SystemData.cpp:459-473` (T2's)", "T35 (the window's half); T33's and T2's halves",
     "The screensaver starts from `render()` on idle time alone; each page is told and cannot refuse; the slideshow's `FileData` list is cleared only when it stops. A transfer's rescan then deletes a game the next pick reads. 3.27 at the pin: `heap-use-after-free ... in FileData::getImagePath`.",
     "#1305 (open, `bug`): the window's half proposed for the pause (a start the top page can hold off); T33's and T2's halves named for their owners; 3.27 PASS when one half lands", "fixture (3.27 FAIL at the pin)"),
    ("The window's teardown frees no card and no popup, and the holders keep raw pointers", "Medium", "Lifetimes", "Q4", "L-02, T2 PC-1",
     "`Window.cpp:188-207`, `:49-63`, `:1246-1248`; the holders in es-app (§ The surfaces)", "T35 (the teardown); the holders T18's, T20's, T34's",
     "`deinit` and `~Window` leave `mAsyncNotificationComponent` and `mNotificationPopups` as they are; the one free is `:1248`. A card alive at `deinit` is drawn again at the next `init()`; a holder's late call after `:1248` is a use after free the card cannot detect.",
     "a design ruling at the pause: T34's `s2-window.patch` (#1310) is a collision (10 es-app callers, 3 doubles); the window-side alternative frees cards and popups in `deinit` and refuses a close after it", "tree"),
    ("`unregisterPostedFunctions` walks the posted functions without their lock", "Low", "Lifetimes", "Q4", "L-03, 3.17",
     "`Window.cpp:1262-1274` against `:1278`, `:1296`", "T35",
     "`postToUiThread` and `processPostedFunctions` take `mNotificationMessagesLock`; the erase loop does not. A worker posting while a page unregisters races the vector.",
     "a `bug` under rule 6: take the lock; 3.17 (TSan) the covering case", "fixture (3.17 TSan at the pin: the erase loop's read against the post's reallocation under the mutex)"),
    ("The input files are written in place, none atomically", "Low", "Input", "Q2", "L-06",
     "`InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:71`, `:115`", "T35",
     "Five writes, `AtomicFile::` 0. A cut `es_input.cfg` fails to parse: the pad reads as unconfigured and the next save keeps one device. The grep's seven sites include two read-mode `fopen`s.",
     "a pause ruling (D-CLOUD-078's family): `es_input.cfg` through the fork's `AtomicFile`, the rest recorded", "tree"),
    ("The approximate-match log reads the node before it is assigned", "Low", "Input", "Q2", "L-10, 3.10",
     "`InputManager.cpp:946`, `:960`", "T35 (upstream's lines, rule 6)",
     "Both lines log `configNode`'s attributes one line before `configNode = item`: empty fields. 3.10 at the pin: no device named.",
     "log `item`; 3.10 the covering case; a #585 line", "fixture (3.10 FAIL at the pin)"),
    ("F4 leaks one SDL_Event per press", "Low", "Input", "Q2", "L-24",
     "`InputManager.cpp:795`", "T35 (upstream's line, rule 6)",
     "`new SDL_Event()` is never freed; `SDL_PushEvent` copies.", "a stack event; a #585 line", "tree"),
    ("One macro name, two values: the keyboard's button padding", "Low", "Words", "Q6", "L-13, 3.19, T34 PL-16",
     "`guis/GuiTextEditPopupKeyboard.cpp:14`, `:220` against `components/MenuComponent.cpp:14` (T34's)", "T35 (the define); T34's comment names it",
     "`BUTTON_GRID_HORIZ_PADDING` is `0.022 W` in the menu and `0.0052083333 W` in the keyboard: 14.08 px against 3.33 px at 640. 3.19 at the pin: the two differ.",
     "a pause ruling: the keyboard's own name (the value is its design), or one definition", "fixture (3.19 FAIL at the pin)"),
    ("CLEAR and the keyboard's `x` commit an empty value with no question", "Low", "Words", "Q6", "L-14",
     "`guis/GuiTextEditPopupKeyboard.cpp:392-397`, `:491-496`; `guis/GuiTextEditPopup.cpp:34`", "the pause (the lanes' fields: the cloud folder, the Wi-Fi key)",
     "One press empties the field and submits it; `es-ui-style-guide.md` § Confirmations asks a consequential action to ask.",
     "a pause ruling (a register row); G-06 frames it on the image", "tree; guest owed"),
    ("The re-queued toast returns with a fresh default duration", "Low", "Surfaces", "Q1", "L-01, 3.14 (second case)",
     "`Window.cpp:1164`", "T35",
     "A toast half-read and taken off by a new card comes back whole, not for its remainder. Recorded as by design; costs seconds, loses no words.",
     "recorded as written; the pause may rule otherwise", "fixture (PASS, recorded)"),
    ("F-ES-24: every toast waits while any card is up, a long upstream card included", "Low", "Surfaces", "Q1", "F-ES-24, brief § 9",
     "`Window.cpp:336-337`", "the pause",
     "The hasher's minutes-long card holds every toast behind it (D-UI-079 keeps that card as upstream has it). Recorded Low on 2026-09-25 and never dispositioned.",
     "a pause ruling: stands, or a bound (brief § 9's first register row)", "tree"),
    ("Back on a dialog without OK or NO takes the last button, and an unconfigured pad's any button fires it", "Low", "Words", "Q6", "L-12, 3.18",
     "`guis/GuiMsgBox.cpp:116-134`, `:257`", "upstream's; the callers choose labels",
     "The accelerator's third branch binds the last button; `:257` fires it for any button of an unconfigured pad.",
     "recorded; G-04 and G-05 frame the behaviour", "tree; guest owed"),
    ("The configuration page's subtitle numbers the SDL instance, not the seat", "Low", "Words", "Q6", "L-17, 3.21",
     "`guis/GuiInputConfig.cpp:134`", "T35 (upstream's line, rule 6)",
     "`GAMEPAD %i` prints `getDeviceId() + 1`; a third pad plugged in reads GAMEPAD 3 whatever its seat.",
     "the seat or the name; a #585 line", "tree"),
    ("The per-event `quit` scripts do not wait", "Low", "Scripts", "Q5", "L-18",
     "`Scripting.cpp:142`, `:177`", "T35",
     "The per-event pass passes `\"\"` as the event name, so `waitForExit = (eventName == \"quit\")` is false there even for `quit`; only the single-script pass waits.",
     "a pause question; recorded", "tree"),
    ("A per-event folder runs every file in it", "Low", "Scripts", "Q5", "L-18, 3.5",
     "`Scripting.cpp:169-178`", "T35",
     "The extension filter is inside `#if WIN32`; on the device a `notes.txt` is handed to the shell. 3.5 at the pin: it is run.",
     "a pause ruling: the single-script pass's filter for both passes; 3.5 the covering case", "fixture (3.5 FAIL at the pin)"),
    ("`doOnFinish` runs its commands synchronously on the interface thread, inside the joystick lock on a hot-plug write", "Low", "Locks", "Q3", "L-08, 3.13",
     "`InputManager.cpp:1272`, `:485-623`, `:605`", "upstream's; recorded",
     "A slow `onfinish` command freezes the interface; reached from the rebuild it runs with `mJoysticksLock` held.",
     "recorded; G-01 counts the shipped `inputAction` lines", "tree"),
    ("Two names for the hotkey", "Low", "Input", "Q2", "L-09, 3.12",
     "`InputManager.cpp:1105-1107`; `guis/GuiInputConfig.cpp:73`, `:273`, `:279`", "T3 (the templates)",
     "The SDL-mapping fallback writes `hotkey`, the configuration page `hotkeyenable`.", "recorded for T3", "tree"),
    ("Four keyboard debug chords run with their gate commented out", "Low", "Structure", "Q7", "L-05",
     "`Window.cpp:262-281`", "upstream's (outside the lanes)",
     "Ctrl+G/T/I/M change the screen with no setting.", "recorded (D-UI-079)", "tree"),
    ("es-core reaches into es-app, and four detached workers capture the window", "Low", "Structure", "Q7", "L-04",
     "`Window.cpp:29`, `:1554-1637`", "upstream ROCKNIX's (outside the lanes)",
     "`#include \"../es-app/src/ApiSystem.h\"`; `processStorageRequest`'s workers capture `this` and post back; nothing joins them.",
     "recorded (D-UI-079); `Window.cpp:29`'s disposition", "tree"),
    ("A rule sentence still calls the card top-right", "Low", "Structure", "Q7", "L-22",
     "`.claude/rules/es-native-ui.md:30` against `Window.cpp:1192`", "the coordinator's sweep",
     "The card is centred at the pin, and the same rule says so at `:191-197`.", "the coordinator's sweep (`tools/archaeology --reversal`)", "tree"),
    ("A dialog speaks its text twice", "Low", "Words", "Q6", "L-16, 3.20",
     "`guis/GuiMsgBox.cpp:44`, `:234`, `:240`", "upstream's",
     "Three `say(` calls in the constructor (TTS compiled out on the image).", "recorded", "tree"),
]
ids = ["PL-%02d" % (i + 1) for i in range(len(I))]
if len(set(t[0] for t in I)) != len(I):
    print("ASSERT: duplicate titles", file=sys.stderr); sys.exit(1)
for t in I:
    if t[1] not in SEV or not re.fullmatch(r"Q[1-7]", t[3]):
        print("ASSERT: a bad severity or question in %r" % t[0], file=sys.stderr); sys.exit(1)
out = ["# Punch list (Phases 5 and 6) — M6.P2 T35, EmulationStation's window, input and the rest of es-core (#682)", "",
       "Written by `tools/t35-05.py` from one item table, so the sections, the Phase 7 gate and the `punch_index` agree. `question:` is the brief's § 4 numbering (Q1 the queue and its surfaces, Q2 the input's writes and commands, Q3 the watchers' lock, Q4 lifetimes, Q5 scripts and the shell, Q6 the popups and the words, Q7 cost, structure and merge debt). Every item is **Open** until the stage-D pause disposes it.", "",
       "reviewed-at-es: 16dbac5211eea7e70db7394372033be2be7df829", ""]
for pl, (title, sev, cat, q, src, lines, own, what, disp, proved) in zip(ids, I):
    out += ["## %s: %s" % (pl, title), "", "- **Severity:** %s; **category:** %s; **question:** %s" % (sev, cat, q), "- **Source finding:** %s" % src,
            "- **Lines at the pin:** %s" % lines, "- **Owner:** %s" % own, "- **What is wrong:** %s" % what, "- **Proposed disposition:** %s" % disp, "- **proved:** %s" % proved, ""]
out += ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
out += ["| %s | **Open** | the stage-D pause disposes it |" % pl for pl in ids]
out += ["", "## punch_index", "", "```yaml", "punch_index:"]
for pl, t in zip(ids, I):
    out += ["- id: %s" % pl, "  severity: \"%s\"" % t[1], "  category: %s" % t[2], "  question: %s" % t[3], "  source_finding: \"%s\"" % t[4].replace('"', "'"), "  outcome: \"open\""]
out += ["```", ""]
open(os.path.join(os.path.dirname(HERE), "05-punch-list.md"), "w", encoding="utf-8").write("\n".join(out))
c = {s: sum(1 for t in I if t[1] == s) for s in SEV}
print("t35-05: %d items (%s); all Open before stage D" % (len(I), ", ".join("%d %s" % (c[s], s) for s in SEV)))
