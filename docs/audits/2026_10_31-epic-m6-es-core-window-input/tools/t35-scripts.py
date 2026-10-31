"""02 § The scripts: the four `ProcessStartInfo` sites -- what builds each string, what is quoted, which thread runs it, whether it waits (#682, Q5).

    python3 -I t35-scripts.py <es worktree> <commit> <paths.txt> [sites=N shell_direct=N]

The sites are the § 5 spawns run's `ProcessStartInfo` lines that construct and run one
(the four R2 cmd 11 names); `ProcessStartInfo::run`'s Linux branch is read in
`utils/Platform.cpp` (T36's, outside the 96, checked as such) for how the string reaches
a shell.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-scripts.py <es worktree> <commit> <paths.txt> [key=value ...]")
S = "es-core/src/"
SC, IM, PL = S + "Scripting.cpp", S + "InputManager.cpp", S + "utils/Platform.cpp"
spawn = c.grep(r"ProcessStartInfo")
direct = c.grep(r"(^|[^A-Za-z_:])system\(|popen\(|runSystemCommand\(")
cnt = {"sites": 0, "shell_direct": len(direct), "spawn_lines": len(spawn)}

for n, needle in [(162, r'std::string cmdOutput = "\(\(\(\(" \+ cmd_utf8 \+ " 2> "'), (167, r"int n = system\(cmdOutput\.c_str\(\)\);"),
                  (178, r'execl\("/bin/sh", "sh", "-c", cmdOutput\.c_str\(\), \(char \*\) NULL\);'), (52, r"waitForExit = true;")]:
    c.need(PL, n, needle, outside=True)

Z = [
    (IM, 1272, r"int exitCode = Utils::Platform::ProcessStartInfo\(tocall\)\.run\(\);",
     "`doOnFinish` (`:1242-1284`)", "`tocall` = the text of each `<command>` under `<inputAction type=\"onfinish\">` in `es_input.cfg` (`:1262-1268`), as written", "nothing quoted by ES: the text is the command line",
     "the interface thread, from `writeDeviceConfig` (`:1238`) -- inside the rebuild's `mJoysticksLock` when reached from the hot-plug write (`:485-623`, `:605`)", "**waits** (the constructor's `waitForExit = true`, `Platform.cpp:52`; `system()` at `:167`); the logged line is masked (`:1270`)"),
    (SC, 140, r"ProcessStartInfo psi;",
     "`executeScript`, non-WIN32 (`:137-148`)", "the script path, quoted only when it has a space (`:92-93`); the event name; up to three arguments, each with every `\"` stripped (`:104-107`) and quoted only when it has a space (`:109-112`)",
     "**a `$`, a backtick, a `;` or a `'` in an argument reaches `sh` unquoted** (L-18, 3.4); a file name is a player's (a ROM, a scraped name)",
     "the caller's: `fireEvent`, on the interface thread for the launch events", "waits only for `quit` and only in the single-script pass -- the per-event pass passes `\"\"` as the event name (`:177`), so `waitForExit = (eventName == \"quit\")` (`:142`) is false there even for `quit`; output to `es_script_stdout.log`, `head -300` (`Platform.cpp:162`)"),
    (SC, 131, r"ProcessStartInfo psi;",
     "`executeScript`, WIN32, the `-wait` branch (`:127-136`)", "as above, with `powershell` prefixed for `.ps1` (`:116-117`)", "as above", "the caller's", "waits (`:133`); WIN32 only, not on the image"),
    (SC, 43, r"ProcessStartInfo psi;",
     "`executeCommandsThread`, WIN32 (`:24-54`)", "a command queued by `pushCommand` (`:58-`)", "as above", "the script queue's thread (WIN32)", "does not wait (`:45`); WIN32 only"),
]
c.need(SC, 142, r'psi\.waitForExit = \(eventName == "quit"\);')
c.need(SC, 177, r'executeScript\(script, "", arg1, arg2, arg3, isAsyncEvent\(eventName\)\);')
c.need(SC, 172, r"^#if WIN32")
c.need(SC, 202, r"if \(_supportedExtensions\.find\(ext\) == _supportedExtensions\.cend\(\)\)")
rows = []
for f, n, needle, fn, built, quoted, thread, waits in Z:
    c.need(f, n, needle)
    cnt["sites"] += 1
    rows.append([f"`{f.replace(S, '')}:{n}`", fn, built, quoted, thread, waits, "tree"])
print("**How every site's string reaches a shell** (`utils/Platform.cpp`, T36's, read): on Linux `run()` wraps the command as `((((<cmd> 2> <log>/<stderr> ; echo $? >&3) | head -300 > <log>/<stdout>) 3>&1) | (read xs; exit $xs))` (`:162`) and hands it to `system()` when it waits (`:167`) or to `/bin/sh -c` in a double-forked child when it does not (`:172-181`). So each of the four is a shell command line; the § 5 run's direct-spawn count (`system(`/`popen(`/`runSystemCommand(` in the 96) is 0 because the shell is inside `ProcessStartInfo`.\n")
print(table(["Site", "Function", "What builds the string", "What is quoted", "Which thread", "Waits", "proved:"], rows))
print("\n**The per-event pass runs every file** in `scripts/<event>/` on the device: the extension filter is inside `#if WIN32` (`:172-176`); only the single-script pass filters by extension (`:201-203`) (L-18, 3.5, 3.6).")
c.finish("t35-scripts", cnt, f"{cnt['sites']} sites ({cnt['spawn_lines']} `ProcessStartInfo` lines in the 96), direct shell spawns {cnt['shell_direct']}")
