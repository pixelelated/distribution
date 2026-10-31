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
    # S0 (stage E, ruling 21): the floor cases no stream holds
    ("ic_utils", "InputConfig.cpp", 14, 58, "//some util functions", "}"),
    ("ic_ctor", "InputConfig.cpp", 124, 135, "InputConfig::InputConfig(int deviceId", "}"),
    ("ic_map", "InputConfig.cpp", 176, 345, "void InputConfig::clear()", "}"),
    ("ic_buttons", "InputConfig.cpp", 347, 414, 'static char ABUTTON[2] = "a";', "}"),
    ("im_hotkey", "InputManager.cpp", 1101, 1108, "if (isConfigured)", "}"),
    ("im_onfinish", "InputManager.cpp", 1244, 1283, "if (!initialized())", "}"),
    ("sc_single", "Scripting.cpp", 182, 207, "std::vector<std::string> paths =", "}"),
    ("mb_ctor", "guis/GuiMsgBox.cpp", 34, 244, "GuiMsgBox::GuiMsgBox(Window* window, const std::string& text,", "}"),
    ("ip_fade", "guis/GuiInfoPopup.cpp", 85, 111, "int curTime = SDL_GetTicks();", "alpha = (int) (Math::easeOutCubic(alpha / 255.0f) * 255.0f);"),
    ("fm_app", "FavoriteMusicManager.cpp", 71, 71, "std::ofstream ofs(favoritesFile, std::ios::app);", "std::ios::app"),
    ("fm_trunc", "FavoriteMusicManager.cpp", 115, 115, "std::ofstream ofs(favoritesFile, std::ios::trunc);", "std::ios::trunc"),
    ("mame_ops", "MameNames.cpp", 38, 51, "static ArcadeRomType& operator |=(ArcadeRomType& a, ArcadeRomType b)", "}"),
    ("mame_roms", "MameNames.cpp", 60, 124, "// Read mame games information", "}"),
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
