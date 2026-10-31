"""02 § The locks: every lock line in the 96, each lock's acquisition sites and order, the blocking entry points, the threads against main.cpp (#682, Q3).

    python3 -I t35-locks.py <es worktree> <commit> <paths.txt> [lines=N files=N locks=N weak=N includes=N]

The lock grep is the one this script runs (stated in its first output line); every hit is
classed -- a declaration, an acquisition, a release, an include or a `weak_ptr::lock` -- and
named under its lock. `main.cpp` (es-app, outside the 96) is read for the threads' start
and stop order and checked as such.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-locks.py <es worktree> <commit> <paths.txt> [key=value ...]")
PAT = r"std::(recursive_|shared_|timed_)?mutex|lock_guard|unique_lock|scoped_lock|shared_lock|\.lock\(\)|\.unlock\(\)|condition_variable"
hits = c.grep(PAT)
S = "es-core/src/"

# Which lock a line belongs to, by the name it carries; the function by an explicit table where the
# enclosing-definition reader cannot see a class-inline method.
LOCKS = [
    ("mNotificationMessagesLock", "Window.cpp:293", "the toast queue, the cards, the posted functions"),
    ("mJoysticksLock", "InputManager.cpp:52", "the joystick and input-config maps"),
    ("mWatchersLock", "watchers/WatchersManager.cpp:7 (.h:77)", "the watcher list"),
    ("mNotificationLock", "watchers/WatchersManager.cpp:5 (.h:80)", "the watcher observers"),
    ("mThreadLock", "watchers/WatchersManager.h:83 (with `mEvent` `:84`)", "the watcher thread's pause and wake"),
    ("mMutex@Log", "Log.cpp:187 (with `mCV` `:188`)", "the logger's double buffer"),
    ("mScriptQueueLock", "Scripting.cpp:20 (with `:21`)", "the script queue (**WIN32 only**, `#if WIN32` `:17-73`)"),
    ("mMutex@TTS", "TextToSpeech.h:48 (with `mEvent` `:49`)", "the speech queue (the speak thread is WIN32 only, `:90-92`)"),
    ("_lock", "ThemeData.h:594", "the theme file cache"),
    ("mLock", "VolumeControl.cpp:205 (with `mEvent` `:206`)", "the PulseAudio wait (`_ENABLE_PULSE_` only, `:11`)"),
]
FUNC = {
    ("Log.cpp", 70): "AsyncLogger::close", ("Log.cpp", 104): "AsyncLogger::enqueue", ("Log.cpp", 122): "AsyncLogger::workerLoop",
    ("Scripting.cpp", 29): "executeCommandsThread", ("Scripting.cpp", 40): "executeCommandsThread", ("Scripting.cpp", 60): "pushCommand", ("Scripting.cpp", 78): "exitScriptingEngine",
    ("VolumeControl.cpp", 199): "PulseAudioControl::WaitEvent", ("watchers/WatchersManager.h", 35): "WatchersManager::GetComponent",
}


def lock_of(f, t):
    for name, decl, _ in LOCKS:
        base = name.split("@")[0]
        if re.search(r"(?<!\w)" + re.escape(base) + r"(?!\w)", t):
            if "@" in name:
                owner = name.split("@")[1]
                if (owner == "Log" and f != "Log.cpp") or (owner == "TTS" and not f.startswith("TextToSpeech")):
                    continue
            return name
    if re.search(r"lock\(mInstance->mThreadLock\)|lock\(mThreadLock\)", t):
        return "mThreadLock"
    if f == "Log.cpp" and re.search(r"mMutex|mCV", t):
        return "mMutex@Log"
    if f.startswith("TextToSpeech") and re.search(r"lock\(mMutex\)|mMutex;|mEvent;|lock\.unlock", t):
        return "mMutex@TTS"
    if f == "Scripting.cpp" and re.search(r"mScriptQueue|lock\.unlock", t):
        return "mScriptQueueLock"
    if f == "Window.cpp" and "lock.unlock" in t:
        return "mNotificationMessagesLock"
    if f == "VolumeControl.cpp" and "mEvent" in t:
        return "mLock"
    if f == "watchers/WatchersManager.h" and "mEvent" in t:
        return "mThreadLock"
    return None


rows = []
cnt = {"lines": len(hits), "files": len({p for p, _, _ in hits}), "locks": len(LOCKS), "weak": 0, "includes": 0}
by_lock = {name: [] for name, _, _ in LOCKS}
for p, n, t in hits:
    f = p.replace(S, "")
    s = t.strip()
    if s.startswith("#include"):
        kind, lk = "include", "--"
        cnt["includes"] += 1
    elif ".lock();" in s and "sInstance.lock()" in s:
        kind, lk = "`weak_ptr::lock`, not a mutex", "--"
        cnt["weak"] += 1
    else:
        lk = lock_of(f, s)
        if lk is None:
            c.fail.append(f"{f}:{n} names no known lock: {s[:80]!r}")
            lk = "?"
        if re.search(r"^(static )?std::(mutex|condition_variable)|^std::mutex WatchersManager::", s) or re.search(r"\bstd::(mutex|condition_variable)\s+\w+;", s):
            kind = "declaration"
        elif ".unlock()" in s:
            kind = "release (manual)"
        elif ".lock()" in s:
            kind = "acquire (manual)"
        else:
            kind = "acquire (RAII)"
        if lk in by_lock and kind.startswith("acquire"):
            by_lock[lk].append(f"`{'.h' if f.endswith('.h') else ''}:{n}`")
    fn = "--" if kind in ("declaration", "include") else (FUNC.get((f, n)) or c.enclosing(p, n))
    rows.append([f"`{f}:{n}`", kind, lk.split("@")[0] if lk != "--" else "--", fn, "tree"])

c.need(S + "InputManager.cpp", 485, r"mJoysticksLock\.lock\(\);")
c.need(S + "InputManager.cpp", 623, r"mJoysticksLock\.unlock\(\);")
c.need(S + "InputManager.cpp", 605, r"writeDeviceConfig\(mInputConfigs\[joyId\]\)")
c.need(S + "watchers/WatchersManager.cpp", 197, r"NotifyComponentChanged\(item->component\)")
c.need(S + "watchers/WatchersManager.cpp", 128, r"unique_lock<std::mutex> lock\(mNotificationLock\)")
c.need("es-app/src/NetworkThread.cpp", 206, r"postToUiThread\(\[pads\]\(\) \{ for \(auto pad : pads\) InputManager::getInstance\(\)->updateBatteryLevel", outside=True)

summary = [
    ["`mNotificationMessagesLock` (`Window.cpp:293`)", "toasts, cards, posts", ", ".join(by_lock["mNotificationMessagesLock"]),
     "none nested; the cards' render pass holds it for the whole pass (`:1179`); `unregisterPostedFunctions` (`:1262-1274`) walks `mFunctions` **without it** (L-03)",
     "a worker's `displayNotificationMessage` or `postToUiThread` waits out one render pass (bounded); the interface thread never waits on a worker here"],
    ["`mJoysticksLock` (`InputManager.cpp:52`)", "joysticks, input configs", ", ".join(by_lock["mJoysticksLock"]),
     "three manual lock/unlock pairs (`:227-242`, `:485-623`, `:1494-1520`) with no `return` between them (read), and no RAII; the rebuild's pair spans `writeDeviceConfig` (`:605`), which fires two events (`:1234-1235`) and runs `doOnFinish`'s commands **synchronously** (`:1272`) with the lock held",
     "interface thread only: SDL events, the launch path's `computePlayersConfigs` (`:1343`), and `updateBatteryLevel` posted from `NetworkThread.cpp:206`; no second thread takes it"],
    ["`mWatchersLock` (`WatchersManager.cpp:7`)", "the watcher list", ", ".join(by_lock["mWatchersLock"]),
     "**held across every `check()`** (`:181`, `:196`) and then `mNotificationLock` inside it (`:197` -> `:128`): order **mWatchersLock -> mNotificationLock**, and the observers' `OnWatcherChanged` runs on the watcher thread under both",
     "**`RegisterComponent` `:66`, `UnregisterComponent` `:78`, `ResetComponent` `:94`, `GetComponent` `.h:35` and the destructor `:143` wait for a running probe** (L-11, #1283's es-core half; 3.1 at stage C)"],
    ["`mNotificationLock` (`WatchersManager.cpp:5`)", "observers", ", ".join(by_lock["mNotificationLock"]),
     "inner to `mWatchersLock` when taken from `run()`", "`UnregisterNotify` `:114` waits for a callback in flight"],
    ["`mThreadLock` (`WatchersManager.h:83`)", "pause and wake", ", ".join(by_lock["mThreadLock"]),
     "its own scope before `mWatchersLock` in `run()` (`:164-171`), never nested with it; `mPaused` is read and written under it, while **`mRunning` is a plain `bool` written at `:151` and read at `:161`, `:172`, `:187` outside any lock** (3.3's ThreadSanitizer race)", "`pause` `:35` and `resume` `:48` take it briefly"],
    ["`mMutex` (`Log.cpp:187`)", "the log buffer", ", ".join(by_lock["mMutex@Log"]), "none nested", "any thread's `LOG(...)` takes it briefly to enqueue"],
    ["`mScriptQueueLock` (`Scripting.cpp:20`)", "script queue", ", ".join(by_lock["mScriptQueueLock"]), "WIN32 only", "--"],
    ["`mMutex` (`TextToSpeech.h:48`)", "speech queue", ", ".join(by_lock["mMutex@TTS"]), "the speak thread is WIN32 only; TTS is compiled out on the image (§ 5)", "--"],
    ["`_lock` (`ThemeData.h:594`)", "theme file cache", ", ".join(by_lock["_lock"]), "held across `load_file` of a theme file (`ThemeData.cpp:716-723`)", "a theme load"],
    ["`mLock` (`VolumeControl.cpp:205`)", "PulseAudio wait", ", ".join(by_lock["mLock"]), "`_ENABLE_PULSE_` only (the pulse branch, not parsed on the host)", "--"],
]
print(f"**The grep:** `git grep -n -E '{PAT}'` over the 96 at the pin.\n")
print(table(["Site", "Kind", "Lock", "Function", "proved:"], rows))
print("\n**Each lock, its acquisition sites, its order, and who waits:**\n")
print(table(["Lock", "Guards", "Acquired at", "Order and what it is held across", "Who blocks on it", ], summary))

# Threads against main.cpp's order (es-app, outside the 96).
M = "es-app/src/main.cpp"
for n, needle in [(788, r"Log::init\(\);"), (793, r"atexit\(&onExit\);"), (353, r"Log::close\(\);"), (898, r"NetworkThread\* nthread = new NetworkThread\(&window\);"),
                  (1330, r"WatchersManager::stop\(\);"), (1347, r"Scripting::exitScriptingEngine\(\);"), (1358, r"window\.deinit\(\);")]:
    c.need(M, n, needle, outside=True)
c.need(S + "Log.cpp", 60, r"mThread = std::thread\(&AsyncLogger::workerLoop, this\);")
c.need(S + "Log.cpp", 77, r"mThread\.join\(\);")
c.need(S + "watchers/WatchersManager.cpp", 61, r"mThread = new std::thread\(&WatchersManager::run, this\);")
c.need(S + "watchers/WatchersManager.cpp", 154, r"mThread->join\(\);")
c.need(S + "VolumeControl.cpp", 32, r"mThread = new std::thread\(&PulseAudioControl::run, this\);")
c.need(S + "VolumeControl.cpp", 72, r"mThread->join\(\);")
c.need(S + "TextToSpeech.cpp", 92, r"mSpeakThread = new std::thread\(&TextToSpeech::SpeakThread, this\);")
c.need(S + "Scripting.cpp", 68, r"mScriptQueueThread = new std::thread\(&executeCommandsThread\);")
threads = [
    ["the logger's worker", "`Log.cpp:60`, from `Log::init` (`main.cpp:788`)", "`AsyncLogger::close` joins (`:76-77`) from `onExit` (`main.cpp:353`, registered `:793`) -- after `window.deinit()` (`:1358`)", "tree"],
    ["the watcher thread", "`WatchersManager.cpp:61`, on the first `getInstance()` (`:15`)", "`WatchersManager::stop()` at `main.cpp:1330` joins (`:154`) -- **before** `window.deinit()`; the join waits for a probe in flight and the 1 s `wait_for` (`:170`)", "tree"],
    ["the PulseAudio loop", "`VolumeControl.cpp:32` (`_ENABLE_PULSE_`)", "`exit()` joins (`:68-73`) from `~PulseAudioControl`", "tree (branch not parsed)"],
    ["the speak thread", "`TextToSpeech.cpp:92` (**WIN32**)", "`:128`", "tree"],
    ["the script queue", "`Scripting.cpp:68` (**WIN32**, `new std::thread`, not a detach)", "**not joined**: `exitScriptingEngine` (`main.cpp:1347`) only sets the flag and notifies (`Scripting.cpp:75-82`, the seat's G-7)", "tree"],
    ["four storage workers", "`Window.cpp:1554`, `:1572`, `:1608`, `:1634` (`processStorageRequest`)", "**detached** (`:1563`, `:1575`, `:1619`, `:1637`); each captures `this` and posts back (L-04); nothing joins them", "tree"],
    ["`NetworkThread` (es-app's)", "`main.cpp:898`", "not deleted at exit; named for its owner, outside the 96", "tree"],
]
print("\n**The threads' start and stop against `main.cpp`'s order** (es-app's, read at the pin):\n")
print(table(["Thread", "Started", "Stopped", "proved:"], threads))
c.finish("t35-locks", cnt, f"{cnt['lines']} lock lines in {cnt['files']} files ({cnt['includes']} includes, {cnt['weak']} `weak_ptr::lock`), {cnt['locks']} locks summarised, {len(threads)} threads")
