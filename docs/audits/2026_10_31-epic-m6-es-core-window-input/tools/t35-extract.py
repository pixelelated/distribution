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
    # D-WORKFLOW-210, S2 (ES 453dffd0a): queue_pop asserted back()/pop_back() at the pin's 339-340
    # and asserts front()/erase(begin()) on the same lines; queue_requeue lifted the pin's
    # 1163-1164 (the append) and lifts 1166-1169 (the insert at the front).
    ("queue_pop", "Window.cpp", 339, 340, "NotificationMessage msg = mNotificationMessages.front();", "mNotificationMessages.erase(mNotificationMessages.begin());"),
    ("queue_requeue", "Window.cpp", 1166, 1169, "std::vector<NotificationMessage> returned;", "mNotificationMessages.insert(mNotificationMessages.begin(), returned.begin(), returned.end());"),
    ("duration", "Window.cpp", 298, 309, "static int notificationDuration(int duration)", "}"),
    ("approx", "InputManager.cpp", 939, 965, "// Search for exact match guid", "}"),
    ("exec_cmd", "Scripting.cpp", 90, 113, "std::string command = script;", "}"),
    ("event_pass", "Scripting.cpp", 169, 178, "auto scripts = Utils::FileSystem::getDirContent(dir);", "}"),
    ("kb_pad", "guis/GuiTextEditPopupKeyboard.cpp", 14, 14, "#define BUTTON_GRID_HORIZ_PADDING", "0.0052083333"),
    ("menu_pad", "components/MenuComponent.cpp", 14, 14, "#define BUTTON_GRID_HORIZ_PADDING", "0.022"),
    ("fs_cache", "utils/FileSystemUtil.cpp", 48, 341, "struct FileCache", "std::shared_mutex FileCache::mFileCacheMutex;"),
    ("fs_exists", "utils/FileSystemUtil.cpp", 1122, 1147, "bool exists(const std::string& _path, bool enableCache)", "} // exists"),
    # S2: posts_unreg was the pin's 1262-1274 and posts_post 1276-1290 (the lock and the wake added)
    ("posts_unreg", "Window.cpp", 1267, 1282, "void Window::unregisterPostedFunctions(void* data)", "}"),
    ("posts_post", "Window.cpp", 1284, 1302, "void Window::postToUiThread(const std::function<void()>& func, void* data)", "}"),
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
    # S1 (stage E, ruling 5; #1342): the accelerator, and the drive dialogs' calls read as text.
    # D-WORKFLOW-210: at the pin the calls were 1568-1578, 1583-1586, 1623-1625, 1630-1640 and
    # 1645-1648; S1's ES commit 56aa398b8 adds a comment line above three of them, so the tip's
    # ranges below hold the same calls with the labels reordered (s1-before.txt ran the pin's).
    ("mb_accel", "guis/GuiMsgBox.cpp", 116, 134, "// set accelerator automatically", "}"),
    # S2's ES commit 453dffd0a adds 22 lines above them: 1569-1579 ... 1648-1651 at S1's tip become
    # 1591-1601, 1606-1609, 1646-1648, 1654-1664 and 1670-1673 (the same calls; the refused run
    # stage-e/s2-after-refused.txt is the extractor seeing the move).
    ("dlg_game_id", "Window.cpp", 1591, 1601, "auto* msg = new GuiMsgBox(this, message,", ");"),
    ("dlg_game", "Window.cpp", 1606, 1609, "auto* msg = new GuiMsgBox(this, message,", ");"),
    ("dlg_sure", "Window.cpp", 1646, 1648, 'this->pushGui(new GuiMsgBox(this, _("ARE YOU SURE?"),', "formatLambda));"),
    ("dlg_new_id", "Window.cpp", 1654, 1664, "auto* msg = new GuiMsgBox(this, message,", ");"),
    ("dlg_new", "Window.cpp", 1670, 1673, "auto* msg = new GuiMsgBox(this, message,", ");"),
    # S2 (stage E, rulings 1, 2, 15; #1338, #1341, #1354, #1355): the help bar, the drain, the idle state
    # S2's before run (s2-before.txt, at S1's tip) lifted help_prompts 1005-1078, posts_drain 1292-1307,
    # win_issleeping Window.h:69 and win_idle Window.h:174-175 (bool mSleeping; the idle count);
    # at S2's tip they are 1005-1079, 1304-1329, :70 and :175-177 (the atomic flag and mWakePosted).
    ("help_prompts", "Window.cpp", 1005, 1079, "void Window::setHelpPrompts(const std::vector<HelpPrompt>& prompts, const HelpStyle& style)", "}"),
    ("posts_drain", "Window.cpp", 1304, 1329, "void Window::processPostedFunctions()", "}"),
    ("upd_idle", "Window.cpp", 540, 540, "mTimeSinceLastInput += deltaTime;", "mTimeSinceLastInput += deltaTime;"),
    ("win_issleeping", "Window.h", 70, 70, "inline bool isSleeping() const { return mSleeping; }", "return mSleeping;"),
    ("win_idle", "Window.h", 175, 177, "std::atomic<bool> mSleeping;", "bool mWakePosted = false;"),
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
