"""02 § The lifetimes: every thread line, detach, `delete this`, post and raw pointer the window hands out or holds; #1305's three halves (#682, Q4).

    python3 -I t35-lifetimes.py <es worktree> <commit> <paths.txt> [threads=N detach=N delete_this=N posts=N raw=N rows=N]

The thread, detach and post lines are the § 5 threads run's greps, recomputed; `delete
this` is `git grep -F`'s. Each row says who joins or frees the thing and what it touches on
the interface thread, read at its lines. #1305's other two halves are read at T33's and
T2's lines (outside the 96, checked as such).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-lifetimes.py <es worktree> <commit> <paths.txt> [key=value ...]")
S = "es-core/src/"
thr = c.grep(r"std::thread|\.detach\(|new std::thread|std::async")
det = c.grep(r"\.detach\(")
dts = c.grep(r"delete this")
pst = c.grep(r"postToUiThread")
cnt = {"threads": len(thr), "detach": len(det), "delete_this": len(dts), "posts": len(pst), "raw": 0, "rows": 0}

# Every thread line: what it is, who joins it, what it touches on the interface thread.
T = {
    ("Log.cpp", 60): ("start: the logger's worker", "`AsyncLogger::close` joins (`:76-77`), from `onExit` at exit", "nothing; it writes the file"),
    ("Log.cpp", 180): ("the member `std::thread mThread`", "as above", "--"),
    ("Scripting.cpp", 18): ("the member `std::thread* mScriptQueueThread` (**WIN32**)", "`exitScriptingEngine`", "--"),
    ("Scripting.cpp", 68): ("start: `new std::thread(&executeCommandsThread)` (**WIN32**; not a detach)", "`exitScriptingEngine` (`:75-81`)", "nothing"),
    ("TextToSpeech.cpp", 92): ("start: the speak thread (**WIN32**)", "`~TextToSpeech` (`:128`)", "nothing"),
    ("TextToSpeech.h", 47): ("the member `std::thread* mSpeakThread`", "as above", "--"),
    ("VolumeControl.cpp", 32): ("start: `PulseAudioControl::run` (`_ENABLE_PULSE_`)", "`exit()` (`:68-73`)", "nothing; the volume is read under `mLock`"),
    ("VolumeControl.cpp", 203): ("the member `std::thread* mThread`", "as above", "--"),
    ("watchers/WatchersManager.cpp", 61): ("start: the watcher thread", "`~WatchersManager` joins (`:154`) from `stop()` (`main.cpp:1330`)", "**the observers' `OnWatcherChanged` runs on this thread** under two locks (`:197` -> `:128-131`)"),
    ("watchers/WatchersManager.h", 88): ("the member `std::thread* mThread`", "as above", "--"),
}
STORAGE = {1554: "`mergeDrive`", 1572: "`ignoreDevicePermanently`", 1608: "`prepareDrive` (format)", 1634: "`ignoreDevicePermanently`"}
rows = []
for p, n, t in thr:
    f = p.replace(S, "")
    if (f, n) in T:
        what, who, ui = T[(f, n)]
    elif f == "Window.cpp" and n in STORAGE:
        what, who, ui = (f"start: a storage worker for {STORAGE[n]} in `processStorageRequest`, capturing `this`", "**nobody: detached**", "posts back to the window (`postToUiThread`) and, on failure, pushes a `GuiMsgBox`")
    elif f == "Window.cpp" and ".detach(" in t:
        what, who, ui = ("the detach", "--", "--")
    else:
        c.fail.append(f"{f}:{n} is a thread line with no row")
        continue
    rows.append([f"`{f}:{n}`", what, who, ui, "tree"])
for f, n, needle in [("Window.cpp", 1563, r"\}\)\.detach\(\);"), ("Window.cpp", 1575, r"\}\)\.detach\(\);"), ("Window.cpp", 1619, r"\}\)\.detach\(\);"), ("Window.cpp", 1637, r"\}\)\.detach\(\);")]:
    c.need(S + f, n, needle)
if sorted((p.replace(S, ""), n) for p, n, _ in det) != [("Window.cpp", 1563), ("Window.cpp", 1575), ("Window.cpp", 1619), ("Window.cpp", 1637)]:
    c.fail.append("the detaches are not the four Window.cpp lines")
print("**Every thread line** (the § 5 threads run's grep, recomputed):\n")
print(table(["Site", "What", "Who joins it", "What it touches on the interface thread", "proved:"], rows))

# delete this: what calls it and what follows it.
D = {
    ("guis/GuiDetectDevice.cpp", 99): "`input`: back cancels; `return true` follows",
    ("guis/GuiDetectDevice.cpp", 132): "`update`: the first-run skip after `mDoneCallback()`; the function ends (`:133-149`) and `Window::update` touches nothing after the call (`Window.cpp:542-543`)",
    ("guis/GuiDetectDevice.cpp", 145): "`update`: the hold done, `GuiInputConfig` pushed first; the function ends",
    ("guis/GuiInputConfig.cpp", 262): "`okFunction` (`:258-263`): after `writeDeviceConfig` (`:259`) and `okCallback()`; reached from the OK button and from the hotkey dialog's two buttons through `GuiMsgBox::deleteMeAndCall`",
    ("guis/GuiInputConfig.cpp", 288): "the CANCEL button's own closure: the button is destroyed while its `std::function` runs; nothing follows",
    ("guis/GuiMsgBox.cpp", 289): "`deleteMeAndCall`: the callback copied first (`:288`), then called after the delete (`:291-292`) -- the safe shape",
    ("guis/GuiTextEditPopup.cpp", 33): "the accept button's closure: `okCallback(value)` then the delete; nothing follows",
    ("guis/GuiTextEditPopup.cpp", 34): "the CLEAR button's closure: `okCallback(\"\")` then the delete, **no question asked** (L-14)",
    ("guis/GuiTextEditPopup.cpp", 35): "the CANCEL button's closure",
    ("guis/GuiTextEditPopup.cpp", 74): "`input`: back; `return true`",
    ("guis/GuiTextEditPopupKeyboard.cpp", 346): "`input`: START submits after `mOkCallback(value)`; `return true`",
    ("guis/GuiTextEditPopupKeyboard.cpp", 352): "`input`: ESC on the keyboard device; `return true`",
    ("guis/GuiTextEditPopupKeyboard.cpp", 359): "`input`: back; `return true`",
    ("guis/GuiTextEditPopupKeyboard.cpp", 395): "`input`: **`x` commits `\"\"`** (`:392-397`, L-14); `return true`",
    ("guis/GuiTextEditPopupKeyboard.cpp", 477): "`pressedKey`: OK after `mOkCallback(value)`; `return` follows",
    ("guis/GuiTextEditPopupKeyboard.cpp", 494): "`pressedKey`: the CLEAR key commits `\"\"` (L-14); `return`",
    ("guis/GuiTextEditPopupKeyboard.cpp", 499): "`pressedKey`: CANCEL; `return`",
}
dr = []
for p, n, t in dts:
    f = p.replace(S, "")
    if (f, n) not in D:
        c.fail.append(f"{f}:{n} is a `delete this` with no row")
        continue
    dr.append([f"`{f}:{n}`", D[(f, n)], "`~GuiComponent` calls `removeGui(this)` (`GuiComponent.cpp:30`, T34's), which also clears the mouse capture (`Window.cpp:86-87`)", "tree"])
c.need(S + "guis/GuiMsgBox.cpp", 288, r"auto funcCopy = func;")
c.need(S + "Window.cpp", 543, r"peekGui\(\)->update\(deltaTime\);")
c.need(S + "Window.cpp", 86, r"if \(mMouseCapture == gui\)")
c.need(S + "GuiComponent.cpp", 30, r"mWindow->removeGui\(this\);", outside=True)
print("\n**Every `delete this`** (all in the six dialogs, all on the interface thread; none touches a member after the delete):\n")
print(table(["Site", "What reaches it, and what follows", "What the delete does to the window", "proved:"], dr))

# The posts.
P = [
    ("Window.cpp", 1276, r"void Window::postToUiThread\(const std::function<void\(\)>& func, void\* data", "the definition: appended under the lock (`:1278`); the owner token `data` is what `unregisterPostedFunctions` (`:1262-1274`) erases by, **without the lock** (L-03)"),
    ("Window.h", 91, r"void postToUiThread\(const std::function<void\(\)>& func, void\* data", "the declaration (the signature § 1 i names with the three doubles)"),
    ("Window.cpp", 1556, r"this->postToUiThread\(\[this, success, processNext\]", "the merge worker's result: runs on the interface thread, pushes `GuiMsgBox` on failure"),
    ("Window.cpp", 1574, r"this->postToUiThread\(\[processNext\]", "the ignore worker's continuation"),
    ("Window.cpp", 1612, r"this->postToUiThread\(\[this, success, processNext\]", "the format worker's result"),
    ("Window.cpp", 1636, r"this->postToUiThread\(\[processNext\]", "the ignore worker's continuation"),
]
pr = []
for f, n, needle, what in P:
    c.need(S + f, n, needle)
    pr.append([f"`{f}:{n}`", what, "tree"])
if len(pst) != len(P):
    c.fail.append(f"{len(pst)} postToUiThread lines, {len(P)} rows")
print("\n**Every `postToUiThread` line** (a post runs once at the next update, on the interface thread; nothing promises a poster that dies before the drain anything; the four workers post with `this` captured, and the window outlives them only because it is `main`'s stack object until `return`):\n")
print(table(["Site", "What", "proved:"], pr))

# The raw pointers the window hands out or holds.
R = [
    ("Window.h", 123, r"std::vector<AsyncNotificationComponent\*> mAsyncNotificationComponent", "the cards", "handed out raw by `createAsyncNotificationComponent` (`Window.cpp:1168-1174`)", "the window, at `:1248` only, once `isRunning()` is false; never in `deinit` or `~Window` (L-02)"),
    ("Window.h", 135, r"std::vector<GuiInfoPopup\*> mNotificationPopups", "the toasts", "held", "the window, at `:358` (stop) and `:377` (faded); never in `deinit` or `~Window` (L-02)"),
    ("Window.h", 147, r"ScreenSaver\*\s+mScreenSaver;", "the screensaver", "set by es-app (`SystemScreenSaver.cpp:49`, T33's)", "its owner, es-app; the window only calls it"),
    ("Window.h", 151, r"std::vector<GuiComponent\*> mGuiStack;", "the page stack", "`peekGui()` hands the top out raw", "each page deletes itself or is deleted by its opener; `~GuiComponent` removes it (`removeGui`); `~Window` deletes what is left (`:59-60`)"),
    ("Window.h", 150, r"std::vector<GuiComponent\*> mScreenExtras;", "the screen extras", "held", "`~Window` (`:53-54`)"),
    ("Window.h", 186, r"GuiComponent\* mMouseCapture;", "the mouse capture", "set by any component (`setMouseCapture`, `.h:111`)", "cleared by `removeGui` (`:86-87`), which every `~GuiComponent` calls -- no dangling capture"),
    ("Window.h", 145, r"HelpComponent\*\s+mHelp;", "the help bar", "held", "`~Window` (`:62`)"),
    ("Window.h", 146, r"ImageComponent\* mBackgroundOverlay;", "the overlay", "held", "`~Window` (`:56`)"),
]
rr = []
for f, n, needle, what, out, free in R:
    c.need(S + f, n, needle)
    cnt["raw"] += 1
    rr.append([f"`{f}:{n}`", what, out, free, "tree"])
c.need("es-app/src/SystemScreenSaver.cpp", 49, r"mWindow->setScreenSaver\(this\);", outside=True)
print("\n**The raw pointers the window hands out or holds:**\n")
print(table(["Member", "What", "Handed out or held", "Who frees it", "proved:"], rr))

# #1305's three halves.
c.need(S + "Window.cpp", 778, r"if \(mTimeSinceLastInput >= screensaverTime && screensaverTime != 0\)")
c.need(S + "Window.cpp", 779, r"startScreenSaver\(\);")
c.need(S + "Window.cpp", 1117, r"mScreenSaver->resetCounts\(\);")
c.need(S + "Window.cpp", 1100, r"\(\*i\)->onScreenSaverActivate\(\);")
H = [
    ["the window's (this slice's)", "`Window.cpp:777-779`, `:1091-1105`, `:1107-1138`",
     "the screensaver starts **from `render()`** on idle time alone (`:778-779`); each page is told (`onScreenSaverActivate`, `:1100`) but cannot refuse, so nothing holds it off while `GuiCloudTransfer` owns the screen; the slideshow's list is cleared only by `resetCounts` from `cancelScreenSaver` (`:1117`) -- a rescan or a `removeGui` does not clear it",
     "a contained hold (the start refused while the top page asks for it) is a candidate for the pause; G-09 frames the start over the transfer page; 3.27 FAILs at the pin until one half lands", "tree; 3.27 and G-09 owed"],
    ["T33's (`SystemScreenSaver`)", "`es-app/src/SystemScreenSaver.cpp:342-358`, `:378-380`, `:538-548`", "the slideshow keeps `FileData*` across picks; its retirement on a rescan is T33's", "named for T33's owner at the pause", "design"],
    ["T2's (the rescan)", "`es-app/src/SystemData.cpp:459-473`", "the rescan deletes a `FileData` gone from disk while a holder keeps it", "named for T2's owner at the pause", "design"],
]
print("\n**#1305's three halves** (read; the body was read to its last comment at stage A, `stage-a/issues.out`):\n")
print(table(["Half", "Lines", "What it does", "Disposition", "proved:"], H))
cnt["rows"] = len(rows) + len(dr) + len(pr) + len(rr) + len(H)
c.finish("t35-lifetimes", cnt, f"{len(rows)} thread rows ({cnt['detach']} detaches), {len(dr)} `delete this`, {len(pr)} posts, {len(rr)} raw pointers, {len(H)} halves of #1305")
