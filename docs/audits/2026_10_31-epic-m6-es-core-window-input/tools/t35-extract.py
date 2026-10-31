"""Lift the seams' lines from the pin, verbatim, into <out>/x_<name>.inc for T35's
window-input-tests (#682; T34's t34-extract.py's shape). Each spec names its file, its
line range and the code its first and last lines must hold; a range that no longer holds
it is refused (exit 1, nothing written), so a case never runs against lines it was not
written for.
    t35-extract.py <ES worktree> <pin> <out dir>"""
import os
import subprocess
import sys

W, PIN, OUT = sys.argv[1:4]
S = "es-core/src/"
SPECS = [  # name, file, first, last, the first line holds, the last line holds
    ("queue_pop", "Window.cpp", 339, 340, "NotificationMessage msg = mNotificationMessages.back();", "mNotificationMessages.pop_back();"),
    ("queue_requeue", "Window.cpp", 1163, 1164, "for (auto ip : mNotificationPopups)", "notificationDuration(-1)));"),
    ("duration", "Window.cpp", 298, 309, "static int notificationDuration(int duration)", "}"),
    ("approx", "InputManager.cpp", 939, 965, "// Search for exact match guid", "}"),
    ("exec_cmd", "Scripting.cpp", 90, 113, "std::string command = script;", "}"),
    ("event_pass", "Scripting.cpp", 169, 178, "auto scripts = Utils::FileSystem::getDirContent(dir);", "}"),
    ("kb_pad", "guis/GuiTextEditPopupKeyboard.cpp", 14, 14, "#define BUTTON_GRID_HORIZ_PADDING", "0.0052083333"),
    ("menu_pad", "components/MenuComponent.cpp", 14, 14, "#define BUTTON_GRID_HORIZ_PADDING", "0.022"),
    ("fs_cache", "utils/FileSystemUtil.cpp", 48, 341, "struct FileCache", "std::shared_mutex FileCache::mFileCacheMutex;"),
    ("fs_exists", "utils/FileSystemUtil.cpp", 1122, 1147, "bool exists(const std::string& _path, bool enableCache)", "} // exists"),
    ("posts_unreg", "Window.cpp", 1262, 1274, "void Window::unregisterPostedFunctions(void* data)", "}"),
    ("posts_post", "Window.cpp", 1276, 1290, "void Window::postToUiThread(const std::function<void()>& func, void* data)", "}"),
]
got = {}
for name, f, a, b, first, last in SPECS:
    r = subprocess.run(["git", "-C", W, "show", f"{PIN}:{S}{f}"], capture_output=True, text=True, errors="replace")
    if r.returncode:
        sys.exit(f"t35-extract: {f} not at {PIN}")
    L = r.stdout.split("\n")
    lines = L[a - 1:b]
    if first not in lines[0] or last not in lines[-1]:
        sys.exit(f"t35-extract: {f}:{a}-{b} no longer holds its code (first {lines[0].strip()[:60]!r}, last {lines[-1].strip()[:60]!r}); nothing written")
    got[name] = f"// {S}{f}:{a}-{b} at {PIN}, verbatim\n" + "\n".join(lines) + "\n"
os.makedirs(OUT, exist_ok=True)
for name, text in got.items():
    open(os.path.join(OUT, f"x_{name}.inc"), "w").write(text)
print(f"t35-extract: {len(got)} extracts at {PIN}")
