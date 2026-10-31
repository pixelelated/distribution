"""02 § The structure: the include reach, the guards the host does not parse, the CMake lists, the cross-tree include, the gates, the map (#682, Q7).

    python3 -I t35-includes.py <es worktree> <commit> <paths.txt> [headers=N cpp_named_once=N unregistered=N batocera=N cmake_ifs=N rocknix=N map_titles=N]

The include reach counts, per header of the 96, the files in es-core/ and es-app/ at the
commit whose `#include` names it by its path's tail (inside the 96 and outside). The guards
are every `#if`/`#ifdef`/`#ifndef`/`#elif` line naming a platform macro. The map's per-file
count applies `tools/es-menu-map-check`'s three `SCREEN_PATTERNS` (read from the
distribution worktree) to the slice's dialogs.
"""
import ast
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t35lib import Ctx, table  # noqa: E402

c = Ctx(sys.argv, "t35-includes.py <es worktree> <commit> <paths.txt> [key=value ...]")
S = "es-core/src/"
gg = subprocess.run(["git", "-C", c.W, "grep", "-I", "-n", "-E", r"^\s*#\s*include\s*[<\"]", c.ref, "--", "es-core", "es-app"], capture_output=True)
if gg.returncode:
    c.fail.append("the include grep failed")
inc_re = re.compile(r'^\s*#\s*include\s*[<"]([^">]+)[">]')
includes = {}
for l in gg.stdout.decode("utf-8", "replace").split("\n"):
    parts = l.split(":", 3)
    if len(parts) < 4:
        continue
    m = inc_re.match(parts[3])
    if m:
        includes.setdefault(m.group(1), set()).add(parts[1])

headers = [p for p in c.paths if p.endswith(".h")]
cnt = {"headers": len(headers), "cpp_named_once": 0, "unregistered": 0, "batocera": 0, "cmake_ifs": 0, "rocknix": 0, "map_titles": 0}
rows = []
for h in headers:
    rel = h[len(S):]
    base = rel.split("/")[-1]
    who = set()
    for inc, files in includes.items():
        tail = inc.split("/")[-1]
        if tail == base and (inc.endswith(rel) or "/" not in inc or inc.endswith("/" + base)):
            who |= files
    who.discard(h)
    inside = len([w for w in who if w in c.inside])
    app = len([w for w in who if w.startswith("es-app/")])
    core_out = len([w for w in who if w.startswith("es-core/") and w not in c.inside])
    rows.append([f"`{h}`", inside, core_out, app, inside + core_out + app, "tool-run"])
rows.sort(key=lambda r: -r[4])
print("**The include reach** (every header of the 96, ranked by its includers across `es-core/` and `es-app/` at the pin; a change to a header with outside includers is a change to their lanes):\n")
print(table(["Header", "Includers in the 96", "es-core outside the 96", "es-app", "Total", "proved:"], rows))

# The guards the host does not parse.
G = {}
for p, n, t in c.grep(r"^\s*#\s*(if|ifdef|ifndef|elif)\b"):
    for mac in re.findall(r"\b(WIN32|_WIN32|_ENABLE_PULSE_|_ENABLE_TTS_|HAVE_LIBCEC|HAVE_UDEV|UDEV_FOUND|ROCKNIX|BATOCERA|_RPI_|_" r"_APPLE_" r"_|_DEBUG|SDL_JoystickDevicePathById|HAVE_CEC|CEC_FOUND|USE_OPENGL_\w+|RENDERER_\w+|\w+_FOUND)\b", t):
        G.setdefault(mac, []).append(f"{p.replace(S, '')}:{n}")
gr = []
HOST = {"WIN32": "not the image's branch: the `#else` is parsed", "_WIN32": "as WIN32", "_ENABLE_PULSE_": "**not parsed** on the host (no pulse headers); the ALSA branch is", "_ENABLE_TTS_": "**not parsed**; compiled out on the image",
        "HAVE_LIBCEC": "**not parsed**; CEC compiled out", "HAVE_UDEV": "**not parsed** without libudev headers; G-01's `ldd` settles the image's", "UDEV_FOUND": "as HAVE_UDEV", "ROCKNIX": "parsed with `-DROCKNIX` in the stand-in (stage C)",
        "_RPI_": "not defined for these images: the other branch is parsed", "BATOCERA": "not defined in a ROCKNIX build: the other branch is parsed", "_" "_APPLE_" "_": "not the image's",
        "SDL_JoystickDevicePathById": "defined only by an SDL that carries it; the image's SDL decides, the host parses without it", "_DEBUG": "not defined in a release build"}
for mac, sites in sorted(G.items(), key=lambda kv: -len(kv[1])):
    shown = f"`{mac.strip('_')}` (double-underscore-wrapped: the compiler's predefined macro)" if mac.startswith("__") and mac.endswith("__") else f"`{mac}`"
    gr.append([shown, len(sites), ", ".join(f"`{s}`" for s in sites[:6]) + (" ..." if len(sites) > 6 else ""), HOST.get(mac, "parsed as the image's (default)"), "tool-run"])
print("\n**The guards** (every preprocessor condition naming a platform or feature macro; the host's stand-in parses one branch, stage C):\n")
print(table(["Macro", "Lines", "First sites", "On the host", "proved:"], gr))

# The CMake lists.
cm = c.text("es-core/CMakeLists.txt").split("\n")
for p in c.paths:
    if p == "es-core/CMakeLists.txt":
        continue
    rel = p[len("es-core/"):]
    named = [i for i, t in enumerate(cm, 1) if re.search(r"\$\{CMAKE_CURRENT_SOURCE_DIR\}/" + re.escape(rel) + r"(\s|$|#)", t)]
    if p.endswith(".cpp"):
        if len(named) == 1:
            cnt["cpp_named_once"] += 1
        else:
            c.fail.append(f"{p} named {len(named)} times in es-core/CMakeLists.txt")
    elif not named:
        cnt["unregistered"] += 1
unreg = [p for p in headers if not any(re.search(r"/" + re.escape(p[len("es-core/"):]) + r"(\s|$|#)", t) for t in cm)]
cnt["batocera"] = sum(1 for t in cm if "# batocera" in t)
bat96 = [i for i, t in enumerate(cm, 1) if "# batocera" in t and any(("/" + p[len("es-core/"):] + " ") in t or ("/" + p[len("es-core/"):] + "\t") in t for p in c.paths)]
cnt["batocera_96"] = len(bat96)
ifs = [i for i, t in enumerate(cm, 1) if re.match(r"^if\(", t)]
cnt["cmake_ifs"] = len(ifs)
c.need("es-core/CMakeLists.txt", 278, r'^if\(\$\{GLSystem\} MATCHES "OpenGL ES 3\.0"\)')
c.need("es-core/CMakeLists.txt", 287, r"^if\(MSVC\)")
td = subprocess.run(["git", "-C", c.W, "diff", c.ref, "3ae9610b0", "--", "es-core/CMakeLists.txt"], capture_output=True, text=True)
t21 = [l for l in td.stdout.split("\n") if l.startswith("+") and not l.startswith("+++")]
if td.returncode or len(t21) != 5:
    c.fail.append(f"T21's hunk at 3ae9610b0: {len(t21)} added lines, expected 5")
print(f"\n**The CMake lists:** every `.cpp` of the 96 is named once in `es-core/CMakeLists.txt` ({cnt['cpp_named_once']} of {len([p for p in c.paths if p.endswith('.cpp')])}); the headers it does not list: {', '.join(f'`{u}`' for u in unreg)}; {cnt['batocera']} lines carry a trailing `# batocera`, {cnt['batocera_96']} of them naming a path of the 96 (`:{"`, `:".join(str(i) for i in bat96)}`); the lists are unconditional but for the two `if(` blocks at `:{ifs[0]}` (the GLES renderer pair) and `:{ifs[1]}` (`MSVC`'s source groups). **T21's hunk** (the pin to T21's tip `3ae9610b0`): {len(t21)} added lines -- `HttpText.h`, `RecoveryOutcome.h` (`@@ -9`), `utils/DownloadFile.h` (`@@ -124`), `HttpText.cpp` (`@@ -151`), `utils/DownloadFile.cpp` (`@@ -259`); the integration's, named in the hand-back (§ 1 h, L-26). `proved: tool-run`.")

# The cross-tree include, the gates, the two record items.
c.need(S + "Window.cpp", 29, r'^#include "\.\./es-app/src/ApiSystem\.h"')
rk = c.grep(r"\bROCKNIX\b")
cnt["rocknix"] = len(rk)
print(f"\n**`Window.cpp:29`** includes `../es-app/src/ApiSystem.h` for `processStorageRequest`'s four workers (`:1554-1637`): es-core depending on es-app, upstream ROCKNIX's, outside the lanes (D-UI-079); **recorded as upstream's, not changed** (L-04). **The `ROCKNIX` lines:** {', '.join(f'`{p.replace(S, chr(0)).replace(chr(0), S) if False else p}:{n}`' for p, n, _ in rk)} ({len(rk)}).")
rule = subprocess.run(["sed", "-n", "30p", ".claude/rules/es-native-ui.md"], capture_output=True, text=True).stdout
if "top-right progress card" not in rule:
    c.fail.append("es-native-ui.md:30 no longer says top-right")
print("\n**L-22, the stale rule sentence:** `.claude/rules/es-native-ui.md:30` calls `AsyncNotificationComponent` the *top-right progress card*; the card is centred at the pin (`Window.cpp:1192`, the fork's hunk) and the same rule says so at `:191-197` and `:208`. For the coordinator's sweep (`tools/archaeology --reversal`), not the lane's edit.")
d = subprocess.run(["git", "-C", c.W, "diff", "--quiet", "cada856d86", c.ref, "--", S + "guis/GuiTextEditPopupKeyboard.h"])
if d.returncode != 0:
    c.fail.append("GuiTextEditPopupKeyboard.h differs from cada856d86")
print("\n**L-25, the footnote:** the inventory records `last_fork_commit 1593c299f3 2026-09-10` on `guis/GuiTextEditPopupKeyboard.h`, which is byte-identical to the merge base `cada856d86` (`git diff --quiet` exit 0): a fork touch undone or merged away. Nothing to fix; § The merge debt carries it.")

# The map.
src = open("tools/es-menu-map-check").read()
pats = re.search(r"SCREEN_PATTERNS = \[(.*?)\n\]", src, re.S).group(1)
regs = [re.compile(ast.literal_eval(m)) for m in re.findall(r"re\.compile\((r'[^']*')\)", pats)]
if len(regs) != 3:
    c.fail.append(f"{len(regs)} SCREEN_PATTERNS read, expected 3")
dialogs = [p for p in c.paths if p.startswith(S + "guis/") and p.endswith(".cpp")]
mr = []
for p in dialogs:
    n = sum(len(r.findall(c.text(p))) for r in regs)
    cnt["map_titles"] += n
    mr.append(f"`{p.replace(S, '')}` {n}")
print(f"\n**The map:** `tools/es-menu-map-check`'s `SOURCE_DIRS` at its `:58` includes `es-core/src/guis`; at the pin it printed `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` rc 0 (stage A, `stage-a/runs.out`). Its three patterns over this slice's {len(dialogs)} dialogs: {', '.join(mr)} -- **{cnt['map_titles']} titles**: these dialogs build no `GuiSettings`/`MenuComponent` page, so the checker sees nothing here and has nothing to miss; a stream that adds a page must map it (D-UI-039).")
c.finish("t35-includes", cnt, f"{len(headers)} headers' reach, {len(gr)} guard macros, {cnt['cpp_named_once']} `.cpp` named once, {len(unreg)} headers unregistered, {cnt['batocera']} `# batocera` lines, {cnt['cmake_ifs']} CMake `if(`, {cnt['rocknix']} `ROCKNIX` lines, {cnt['map_titles']} map titles")
