"""02 § The leads: L-01 to L-29 and the floor's 3.1 to 3.27, each anchored at its line (#682).

    python3 -I t35-leads.py <es worktree> <commit> <paths.txt> [leads=N cases=N confirmed=N contradicted=N]

Every lead's anchor line is checked for its text at <commit> (a line outside the 96 is
checked as such); the disposition is the stage-B reading of the tree, before stage C's
cases and the guest. The brief's lead table is the source of the ids and their lines
(`docs/reviews/briefs/es-core-window-input.md` § 2 at `8b5d9b9b62`).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-leads.py <es worktree> <commit> <paths.txt> [key=value ...]")
S = "es-core/src/"
W, IM, SC, WM = S + "Window.cpp", S + "InputManager.cpp", S + "Scripting.cpp", S + "watchers/WatchersManager.cpp"
MB, KB, IC, GI = S + "guis/GuiMsgBox.cpp", S + "guis/GuiTextEditPopupKeyboard.cpp", S + "InputConfig.cpp", S + "guis/GuiInputConfig.cpp"

# id, (file, line, needle, outside), lines, family, owner, disposition, proof, proved
L = [
    ("L-01", (W, 339, r"mNotificationMessages\.back\(\)", False), "`Window.cpp:339-340` against `:334-335`; `:1159-1160`; `:1164`", "the queue", "this lane (rule 6)",
     "**confirmed at the tree:** the pop is from the back (upstream's, `back()`/`pop_back()` at the base `bccd715707`), **D-UI-093's decided row (`decision-register.md:404`) and the fork's comment at `c1c0d6ddc` both say *the order is the order things happened***, while its own `:1159-1160` says *a toast returned last shows first*: a defect against a decided row; a re-queued toast takes a fresh default duration (`:1164`). A contained fix (pop the front) for the pause", "3.14; G-02; G-03 `CANNOT`", "tree"),
    ("L-02", (W, 1248, r"delete mAsyncNotificationComponent\[i\];", False), "`Window.cpp:188-207`, `:49-63`, `:1246-1248`; the raw holders in es-app", "lifetimes", "this lane (the teardown), T18/T20/T34 (the holders)",
     "**confirmed:** `deinit` and `~Window` free no card or popup; the one free is `:1248`. T34's `s2-window.patch` (#1310) is the input: a `weak_ptr` return changes 10 es-app callers and 3 doubles -- **a collision for the pause** (§ 1 i), § The surfaces' last row", "Q4; the pause", "tree"),
    ("L-03", (W, 1262, r"void Window::unregisterPostedFunctions\(void\* data\)", False), "`Window.cpp:1262-1274` against `:1278`, `:1296`", "lifetimes", "this lane (rule 6)",
     "**confirmed:** no lock in `unregisterPostedFunctions`; the two others take it. A contained fix (take the lock) for the pause", "3.17 (TSan)", "tree"),
    ("L-04", (W, 29, r'#include "\.\./es-app/src/ApiSystem\.h"', False), "`Window.cpp:1554-1637`; `:29`", "lifetimes, structure", "upstream ROCKNIX's (outside the lanes, D-UI-079)",
     "**confirmed:** four detached workers capture `this` and post back; `:29` reaches into es-app. Recorded as upstream's, not changed; `Window.cpp:29`'s disposition is *recorded*", "--", "tree"),
    ("L-05", (W, 262, r"SDLK_g && SDL_GetModState\(\) & KMOD_LCTRL\) // && Settings::getInstance\(\)->getBool\(\"Debug\"\)", False), "`Window.cpp:262-281`", "input", "upstream's",
     "**confirmed:** four Ctrl chords with the gate commented out on each line. Recorded (cost: a keyboard on a handheld; value: debugging)", "--", "tree"),
    ("L-06", (IM, 1225, r"doc\.save_file", False), "`InputManager.cpp:1225`, `:1232`; `FavoriteMusicManager.cpp:115`", "input (writes)", "this lane (rule 6) for `es_input.cfg`; the pause for the rest",
     "**confirmed:** five writes, none atomic, `AtomicFile::` 0 (§ The input); the grep's seven include two read-mode `fopen`s. The `es_input.cfg` write through the fork's `AtomicFile` is a candidate for the pause (D-CLOUD-078's family)", "§ The input", "tree"),
    ("L-07", (IM, 1187, r"if \(Utils::FileSystem::exists\(path\)\)", False), "`InputManager.cpp:893`, `:1187`, `:1225`, `:1250`; T36's cache", "input (reads)", "this lane (the read passes `false`), T36 (the cache)",
     "**supported by the tree:** the cache stores misses (`FileSystemUtil.cpp:296`, `:323`, T36's) and `save_file` bypasses it; the hypothesis stands until 3.11 runs; G-01 reads the precondition", "3.11; G-01", "tree"),
    ("L-08", (IM, 1272, r"ProcessStartInfo\(tocall\)\.run\(\)", False), "`InputManager.cpp:1242-1284`", "scripts", "upstream's; recorded",
     "**confirmed:** synchronous on the interface thread, inside the rebuild's lock when reached from the hot-plug write (§ The locks)", "3.13; G-01's count", "tree"),
    ("L-09", (IM, 1105, r'getInputByName\("hotkey", &tmp\)', False), "`InputManager.cpp:1101-1108`; `GuiInputConfig.cpp:73`, `:270-281`; `InputConfig.cpp:186-189`", "input", "T3 (which name the templates read)",
     "**confirmed:** two names, `hotkey` and `hotkeyenable`; no verdict here", "3.12", "tree"),
    ("L-10", (IM, 946, r'Approximative device found using guid=" << configNode\.attribute', False), "`InputManager.cpp:946`, `:960`", "input", "this lane (rule 6)",
     "**confirmed:** both lines read `configNode` before `configNode = item` (`:947`, `:961`). A one-word fix (log `item`) for the pause", "3.10", "tree"),
    ("L-11", (WM, 181, r"std::unique_lock<std::mutex> lock\(mWatchersLock\);", False), "`WatchersManager.cpp:181-199` and the entry points", "locks", "this lane (#1283's es-core half)",
     "**confirmed:** the list lock is held across every probe; five interface-thread entry points wait (§ The locks). The fix (snapshot, then probe unlocked, re-validating) for the pause", "3.1, 3.2, 3.3", "tree"),
    ("L-12", (MB, 133, r"mAcceleratorFunc = mButtons\.back\(\)->getPressedFunc\(\);", False), "`GuiMsgBox.cpp:116-134`, `:246-264`", "dialogs", "upstream's; the callers pick their labels",
     "**confirmed:** the third branch binds back to the last button; an unconfigured pad's any button fires it (`:257`). Read; G-04 and G-05 frame it", "3.18; G-04; G-05", "tree"),
    ("L-13", (KB, 14, r"#define BUTTON_GRID_HORIZ_PADDING \(Renderer::getScreenWidth\(\)\*0\.0052083333\)", False), "`GuiTextEditPopupKeyboard.cpp:14`, `:220` against `MenuComponent.cpp:14` (T34's)", "dialogs", "this lane (the define)",
     "**confirmed:** one macro name, two values in two files. A rename for the pause (the keyboard's own name); the value is the keyboard's design", "3.19; G-06", "tree"),
    ("L-14", (KB, 394, r'mOkCallback\(""\);', False), "`GuiTextEditPopupKeyboard.cpp:392-397`, `:453-454`, `:491-496`; `GuiTextEditPopup.cpp:34`", "dialogs", "the pause (the lanes' fields: the cloud folder, the Wi-Fi key)",
     "**confirmed:** `x` and CLEAR commit `\"\"` and close with no question", "G-06", "tree"),
    ("L-15", (S + "guis/GuiTextEditPopup.h", 16, r"const std::function<void\(const std::string&\)>& okCallback, bool multiLine", False), "`GuiTextEditPopup.h:15-16`, `GuiTextEditPopupKeyboard.h:13-14`", "dialogs", "Backlog #1192",
     "**confirmed:** no masking parameter in either constructor. Deferred to #1192", "--", "tree"),
    ("L-16", (MB, 44, r"TextToSpeech::getInstance\(\)->say\(text\);", False), "`GuiMsgBox.cpp:44`, `:234`, `:240`", "words", "upstream's",
     "**confirmed:** three `say(` calls (TTS compiled out on the image); recorded", "3.20", "tree"),
    ("L-17", (GI, 134, r"target->getDeviceId\(\) \+ 1", False), "`GuiInputConfig.cpp:134`", "words", "this lane (rule 6)",
     "**confirmed:** the subtitle's number is the SDL instance id plus one", "3.21; G-08", "tree"),
    ("L-18", (SC, 92, r'if \(script\.find\(" "\) != std::string::npos\)', False), "`Scripting.cpp:88-149`, `:169-178`", "scripts", "this lane (rule 6) with T2 (FD-9/FD-19)",
     "**confirmed:** quoting only on a space, `\"` stripped, `$`/backtick unquoted to `/bin/sh -c`; every file in a per-event folder runs (§ The scripts)", "3.4, 3.5, 3.6", "tree"),
    ("L-19", (SC, 193, r"if \(!Utils::FileSystem::exists\(dir\)\)", False), "`Scripting.cpp:158-207`; `WatchersManager.cpp:29-53`", "scripts", "time to play",
     "**confirmed:** three folder listings and three directory scans per event; priced on the guest (the retro's time-to-play)", "the guest", "tree"),
    ("L-20", (IM, 1482, r'"guid "', False), "`InputManager.cpp` `configureEmulators` (`:1474-1488`)", "scripts", "T2 (the launch path), T3 (the templates)",
     "**contradicted at the pin for es-core:** the blob is `-pNindex <int> -pNguid <hex>`, no device name (`:1481-1482`); built unconditionally at `FileData.cpp:547` (T2's). The quoting half is where a name enters, not here", "--", "tree"),
    ("L-21", (W, 743, r"if \(mGuiStack\.size\(\) < 2 \|\| !Renderer::ScreenSettings::fullScreenMenus\(\)\)", False), "`Window.cpp:743-745`, `:999-1003`; the eight `mHelp->` lines", "help bar", "read",
     "**confirmed:** no Window bar under a second full-screen page; none of the eight calls `setOpacity`, so batocera's guard has no caller here", "G-04", "tree"),
    ("L-22", (W, 1192, r"float posX = Renderer::getScreenWidth\(\) \* 0\.5f - child->getSize\(\)\.x\(\) \* 0\.5f;", False), "`.claude/rules/es-native-ui.md:30` against `Window.cpp:1192` (the rule's line is checked by `t35-includes.py`)", "record", "the coordinator's sweep",
     "**confirmed:** *top-right progress card* against a centred card; § The structure", "--", "tree"),
    ("L-23", (S + "ThemeData.cpp", 745, r"void ThemeData::loadFile\(", False), "`ThemeData.cpp:745-856`, `:1094-1150`", "structure", "upstream's",
     "**read:** the throw/warn asymmetry recorded; parse-only on the host", "3.26", "tree"),
    ("L-24", (IM, 795, r"SDL_Event\* quit = new SDL_Event\(\);", False), "`InputManager.cpp:792-800`", "input", "this lane (rule 6)",
     "**confirmed:** a `new SDL_Event` per F4 press, never freed (`SDL_PushEvent` copies). A one-line fix (a stack event) for the pause", "--", "tree"),
    ("L-25", (S + "guis/GuiTextEditPopupKeyboard.h", 13, r"GuiTextEditPopupKeyboard\(Window\* window", False), "`guis/GuiTextEditPopupKeyboard.h`", "record", "§ The merge debt",
     "**confirmed:** byte-identical to `cada856d86`; a footnote", "--", "tree"),
    ("L-26", ("es-core/CMakeLists.txt", 278, r"^if\(", False), "`es-core/CMakeLists.txt` at T21's `3ae9610b0`", "structure", "the integration (§ 1 h)",
     "**confirmed:** five added lines in four hunks; named in the hand-back", "--", "tree"),
    ("L-27", (W, 779, r"startScreenSaver\(\);", False), "`Window.cpp:777-779`, `:1091-1138`; T33's and T2's", "lifetimes", "this lane's half, T33's, T2's",
     "**confirmed (the window's half):** the start from `render()` on idle time alone, with no way for a page to refuse; § The lifetimes' three halves", "3.27; G-09", "tree"),
    ("L-28", (W, 1023, r"if\(inputSeenMap\.emplace\(it->first, true\)\.second\)", False), "`Window.cpp:743-745`, `:1005-1078`; T34's chain", "help bar", "read; the pause with G-11",
     "**read:** the window's collection drops only a repeated icon (`:1023`) and merges the two dpad halves (`:1031-1041`); it adds nothing and drops no other prompt, so an empty bar comes from the prompts it was given -- the components or the image's composition. G-11 frames the page", "3.16; G-11", "tree"),
    ("L-29", (W, 1067, r"if\(a\.first == map\[i\]\)", False), "`Window.cpp:1005-1078`; `ComponentList.cpp:568` (T34's)", "help bar", "read",
     "**read:** a key `setHelpPrompts` does not know passes through untouched and sorts with index 0 (`:1062-1074`); it neither translates nor drops it -- whether its icon draws is `HelpComponent`'s (T34's)", "3.16", "tree"),
]
rows = []
cnt = {"leads": 0, "cases": 0, "confirmed": 0, "contradicted": 0}
for lid, (f, n, needle, out), lines, fam, owner, disp, proof, proved in L:
    c.need(f, n, needle, outside=out)
    cnt["leads"] += 1
    cnt["confirmed"] += disp.startswith("**confirmed")
    cnt["contradicted"] += disp.startswith("**contradicted")
    rows.append([lid, lines, fam, owner, disp, proof, proved])
print(table(["Lead", "Lines", "Family", "Owner", "Disposition (stage B)", "Proof", "proved:"], rows))

# The floor's cases: each anchored; all run at stage C.
F3 = [
    ("**3.1**", WM, 196, r"if \(item->component->check\(\)\)", "a probe that sleeps; `ResetComponent` from a second thread waits for it", "FAIL at the pin expected (L-11)"),
    ("3.2", WM, 86, r"delete info;", "ASan: unregister during a running probe", "FAIL expected (EP-13)"),
    ("3.3", WM, 151, r"mRunning = false;", "TSan: `mRunning` written and read unsynchronised", "a race report expected"),
    ("**3.4**", SC, 109, r'if \(data\.find\(" "\) != std::string::npos\)', "`a$(id)b.zip` unquoted, `a b.zip` quoted, `\"` stripped", "FAIL expected (L-18)"),
    ("**3.5**", SC, 172, r"^#if WIN32", "a `notes.txt` in a per-event folder handed to the executor", "FAIL expected (L-18)"),
    ("3.6", SC, 202, r"_supportedExtensions\.find\(ext\)", "the single-script pass filters by extension", "PASS expected (contract)"),
    ("3.7", IC, 188, r"mNameMap\[toLower\(name\)\] = input;", "`mapInput` lower-cases; the XML round trip keeps every mapping", "PASS expected (contract)"),
    ("3.8", IC, 353, r"std::string InputConfig::buttonLabel\(const std::string& button\)", "`buttonLabel` returns an unknown key unchanged", "PASS expected (contract)"),
    ("3.9", IC, 347, r'static char ABUTTON\[2\] = "a";', "`AssignActionButtons` swaps once and is idempotent", "PASS expected (contract)"),
    ("**3.10**", IM, 960, r"Approximative device found", "the two lines print empty attributes", "FAIL expected (L-10)"),
    ("**3.11**", IM, 893, r"if \(!Utils::FileSystem::exists\(path\)\)", "miss, `save_file`, `exists` again: false while the miss is cached", "FAIL expected if the cache holds (L-07)"),
    ("3.12", IM, 1107, r'config->mapInput\("hotkey", tmp\);', "`select` copied to `hotkey`", "PASS expected (documents the two names)"),
    ("3.13", IM, 1262, r'find_child_by_attribute\("inputAction", "type", "onfinish"\)', "every `onfinish` command handed to the executor, synchronously", "PASS expected (contract)"),
    ("**3.14**", W, 340, r"mNotificationMessages\.pop_back\(\);", "queue [A, B] under a card: B then A; the re-queued duration", "FAIL expected (L-01)"),
    ("3.15", W, 298, r"static int notificationDuration\(int duration\)", "the duration's three branches", "PASS expected (contract)"),
    ("3.16", W, 1036, r'addPrompts\.at\(mappedTo->second\)\.first = "up/down/left/right";', "the dedup, the merge, the sort", "PASS expected (contract)"),
    ("3.17", W, 1267, r"for \(auto it = mFunctions\.cbegin\(\); it != mFunctions\.cend\(\); \)", "TSan: unregister against a post", "a race report expected (L-03)"),
    ("3.18", MB, 125, r'_\("OK"\) \|\| Utils::String::toUpper\(\(\*it\)->getText\(\)\) == _\("NO"\)', "the three accelerator branches in the text", "PASS expected (text)"),
    ("**3.19**", KB, 220, r"BUTTON_GRID_HORIZ_PADDING / 4\.0f", "the macro defined in two files with two factors", "FAIL expected (L-13)"),
    ("3.20", MB, 240, r"TextToSpeech::getInstance\(\)->say\(btn->getText\(\), true\);", "three `say(` in the constructor", "recorded (L-16)"),
    ("3.21", GI, 134, r'_\("GAMEPAD %i"\)', "`getDeviceId() + 1` is the argument", "recorded (L-17)"),
    ("3.22", S + "guis/GuiInfoPopup.cpp", 98, r"#define FADE_DURATION 250", "the fade's alpha curve and `mRunning`", "PASS expected (contract)"),
    ("3.23", S + "Log.cpp", 60, r"mThread = std::thread\(&AsyncLogger::workerLoop, this\);", "every batch reaches the file (#178)", "PASS expected (the natural first binary)"),
    ("3.24", S + "FavoriteMusicManager.cpp", 115, r"std::ios::trunc", "the rewrite is truncate-then-write", "recorded (L-06)"),
    ("3.25", S + "MameNames.cpp", 6, r"#include <pugixml/src/pugixml\.hpp>", "a malformed file: warned or thrown", "recorded"),
    ("3.26", S + "ThemeData.cpp", 1094, r"void ThemeData::parseInclude\(", "parse-only; the asymmetry recorded", "no host case (L-23)"),
    ("**3.27**", W, 778, r"mTimeSinceLastInput >= screensaverTime", "T33's `pl25-screensaver.py`, unchanged", "FAIL at the pin expected (#1305)"),
]
fr = []
for cid, f, n, needle, what, expect in F3:
    c.need(f, n, needle)
    cnt["cases"] += 1
    fr.append([cid, f"`{f.replace(S, '')}:{n}`", what, expect, "stage C", "design"])
print("\n**The floor's cases** (the seven candidates and 3.27 in bold; every case runs at stage C against the unfixed extract first; `proved: design` until it has):\n")
print(table(["Case", "Anchor", "What it checks", "Expected at the pin", "When", "proved:"], fr))
c.finish("t35-leads", cnt, f"{cnt['leads']} leads ({cnt['confirmed']} confirmed at the tree, {cnt['contradicted']} contradicted, the rest read or supported), {cnt['cases']} floor cases anchored")
