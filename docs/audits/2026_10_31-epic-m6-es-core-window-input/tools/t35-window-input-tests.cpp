// T35 (#682): window-input-tests. Each case lifts the pin's lines verbatim
// (tools/t35-extract.py, each extract refused unless its first and last lines
// hold the code they were written for) into the smallest double that compiles
// them, and asserts the behaviour the slice should have: a defect at the pin is
// a FAIL here, the case's "seen to FAIL against the unfixed extract". 3.1 links
// the pin's own watchers/WatchersManager.cpp behind tests/app-unit/fakes/Log.h.
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cassert>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <functional>
#include <memory>
#include <map>
#include <optional>
#include <set>
#include <shared_mutex>
#include <sstream>
#include <string>
#include <sys/stat.h>
#include <thread>
#include <unistd.h>
#include <unordered_map>
#include <utility>
#include <vector>
#define PUGIXML_HEADER_ONLY
#include "pugixml/src/pugixml.hpp"
#include "watchers/WatchersManager.h"
#include "HelpPrompt.h"
#include "utils/AtomicFileUtil.h"

// tests/app-unit/fakes/Log.h's two definitions (the double keeps every line).
namespace FakeLog
{
	std::vector<std::string>& lines() { static std::vector<std::string> l; return l; }
	std::mutex& lock() { static std::mutex m; return m; }
}

// ---- 3.14: the toast queue's order (L-01, D-UI-093) -------------------------
namespace q
{
	typedef std::pair<std::string, int> NotificationMessage;
	struct Popup { std::string m; std::string getMessage() { return m; } };
	struct SettingsD { int t = 10; int getInt(const std::string&) { return t; } static SettingsD* getInstance() { static SettingsD s; return &s; } };
	#define Settings SettingsD
	#include "x_duration.inc"
	#undef Settings
	struct WindowQ
	{
		std::vector<NotificationMessage> mNotificationMessages;
		std::vector<Popup*> mNotificationPopups;
		NotificationMessage next() {
			#include "x_queue_pop.inc"
			return msg;
		}
		void requeue() {
			#include "x_queue_requeue.inc"
		}
	};
}

TEST_CASE("3.14 the toast queue drains in the order things happened (D-UI-093, Window.cpp:339-340)")
{
	q::WindowQ w;
	w.mNotificationMessages.push_back({"A first", 3000});
	w.mNotificationMessages.push_back({"B second", 3000});
	CHECK(w.next().first == "A first");
	CHECK(w.next().first == "B second");
}

TEST_CASE("3.14 a re-queued toast returns with the default duration, not its remainder (Window.cpp:1164; recorded, by design)")
{
	q::WindowQ w;
	q::Popup p{"halfway"};
	w.mNotificationPopups.push_back(&p);
	w.requeue();
	REQUIRE(w.mNotificationMessages.size() == 1);
	CHECK(w.mNotificationMessages[0].second == q::notificationDuration(-1));
}

TEST_CASE("3.15 notificationDuration's three branches (Window.cpp:298-309)")
{
	q::SettingsD::getInstance()->t = 5;  CHECK(q::notificationDuration(-1) == 5000);
	q::SettingsD::getInstance()->t = 2;  CHECK(q::notificationDuration(0) == 10000);
	q::SettingsD::getInstance()->t = 121; CHECK(q::notificationDuration(-1) == 10000);
	CHECK(q::notificationDuration(4200) == 4200);
}

// ---- 3.10: the approximate-match log (L-10, InputManager.cpp:946, :960) -----
namespace im
{
	enum LogLevel { LogInfo };
	static std::vector<std::string> logged;
	struct Line { std::ostringstream o; template <class T> Line& operator<<(const T& v) { o << v; return *this; } ~Line() { logged.push_back(o.str()); } };
	#define LOG(l) im::Line()
	struct ConfigD { std::string guid, name; std::string getDeviceGUIDString() { return guid; } std::string getDeviceName() { return name; } };
	pugi::xml_node approx(pugi::xml_node root, ConfigD* config, bool allowApproximate) {
		pugi::xml_node configNode(NULL);
		#include "x_approx.inc"
		return configNode;
	}
	#undef LOG
}

TEST_CASE("3.10 the approximate-match log names the device it found (InputManager.cpp:946, :960)")
{
	pugi::xml_document doc;
	doc.load_string("<inputList><inputConfig deviceGUID=\"0300abcd\" deviceName=\"Pad X\"/></inputList>");
	im::ConfigD byGuid{"0300abcd", "other name"};
	im::logged.clear();
	pugi::xml_node n = im::approx(doc.child("inputList"), &byGuid, true);
	REQUIRE(n);
	REQUIRE(im::logged.size() == 1);
	CHECK(im::logged[0].find("guid=0300abcd") != std::string::npos);
	im::ConfigD byName{"ffff", "Pad X"};
	im::logged.clear();
	REQUIRE(im::approx(doc.child("inputList"), &byName, true));
	REQUIRE(im::logged.size() == 1);
	CHECK(im::logged[0].find("name=Pad X") != std::string::npos);
}

// ---- 3.4 and 3.5: the script runner (L-18, Scripting.cpp) -------------------
namespace sc
{
	namespace Utils { namespace String {
		bool startsWith(const std::string& s, const std::string& p) { return s.compare(0, p.size(), p) == 0; }
		std::string replace(std::string s, const std::string& a, const std::string& b) { size_t i = 0; while ((i = s.find(a, i)) != std::string::npos) { s.replace(i, a.size(), b); i += b.size(); } return s; }
		std::string toLower(std::string s) { for (auto& c : s) c = (char)tolower(c); return s; }
		bool endsWith(const std::string& s, const std::string& e) { return s.size() >= e.size() && s.compare(s.size() - e.size(), e.size(), e) == 0; }
		#include "x_str_shellquote.inc"
	} }
	std::string command_for(const std::string& script, const std::string& eventName, const std::string& arg1, const std::string& arg2 = "", const std::string& arg3 = "") {
		#include "x_exec_cmd.inc"
		return command;
	}
	static std::vector<std::string> ran;
	static void executeScript(const std::string& script, const std::string&, const std::string&, const std::string&, const std::string&, bool) { ran.push_back(script); }
	static bool isAsyncEvent(const std::string&) { return true; }
	namespace Utils { namespace FileSystem {
		std::vector<std::string> getDirContent(const std::string& dir) { return { dir + "/notes.txt", dir + "/run.sh" }; }
		std::string getExtension(const std::string& p) { auto i = p.rfind('.'); return i == std::string::npos ? "" : p.substr(i); }
	} }
	static std::set<std::string> _supportedExtensions = { ".exe", ".cmd", ".bat", ".ps1", ".sh", ".py" };
	void per_event(const std::string& dir, const std::string& eventName, const std::string& arg1, const std::string& arg2, const std::string& arg3) {
		(void)_supportedExtensions;
		#include "x_event_pass.inc"
	}
}

TEST_CASE("3.4 an argument reaches the shell quoted so that $( ) and backticks stay text (Scripting.cpp:98-113)")
{
	std::string c = sc::command_for("/storage/.config/emulationstation/scripts/game-start.sh", "game-start", "/storage/roms/nes/a$(id)b.zip");
	CHECK(c.find("'/storage/roms/nes/a$(id)b.zip'") != std::string::npos);
	std::string t = sc::command_for("/s/hook.sh", "game-start", "x`id`y.zip");
	CHECK(t.find("'x`id`y.zip'") != std::string::npos);
}

// D-WORKFLOW-211 (S5, #1339): at the pin this case recorded the pin's shapes -- `/s/hook.sh
// game-start "a b.zip"` and `/s/hook.sh game-start ab.zip` (a space in double quotes, a double
// quote stripped), PASS in stage-e/s5-before.txt. From S5 it holds the fixed shapes.
TEST_CASE("3.4 the shapes, recorded: each word single-quoted, a double quote kept, a single quote escaped (were: a space in double quotes, a double quote stripped)")
{
	CHECK(sc::command_for("/s/hook.sh", "game-start", "a b.zip") == "'/s/hook.sh' 'game-start' 'a b.zip'");
	CHECK(sc::command_for("/s/hook.sh", "game-start", "a\"b.zip") == "'/s/hook.sh' 'game-start' 'a\"b.zip'");
	CHECK(sc::command_for("/s/hook.sh", "game-start", "it's.zip") == "'/s/hook.sh' 'game-start' 'it'\\''s.zip'");
}

TEST_CASE("S5 an argument that starts with a double quote keeps its last character (Scripting.cpp:104; PL-03, #1339)")
{
	std::string c = sc::command_for("/s/hook.sh", "game-start", "\"abc");
	CHECK(c.find("abc") != std::string::npos);
}

TEST_CASE("S5 the script path and the event name reach the shell single-quoted (Scripting.cpp:90-96; PL-03, #1339)")
{
	std::string c = sc::command_for("/s/my hook$(id).sh", "game-start", "x");
	CHECK(c.rfind("'/s/my hook$(id).sh' 'game-start' ", 0) == 0);
}

// Rulings 9 and 20 (stage E S5): PL-18 is recorded, not fixed -- on the device a file runs only
// with its execute bit, and the filter would silently stop a player's working hook after an
// update -- so 3.5 stays as written and is marked may_fail with PL-18 named.
TEST_CASE("3.5 a non-script file in a per-event folder is not run (Scripting.cpp:169-178, the filter WIN32-only; PL-18 recorded, may_fail)" * doctest::may_fail())
{
	sc::ran.clear();
	sc::per_event("/storage/.config/emulationstation/scripts/game-start", "game-start", "", "", "");
	CHECK(std::find(sc::ran.begin(), sc::ran.end(), "/storage/.config/emulationstation/scripts/game-start/notes.txt") == sc::ran.end());
	CHECK(std::find(sc::ran.begin(), sc::ran.end(), "/storage/.config/emulationstation/scripts/game-start/run.sh") != sc::ran.end());
}

// ---- 3.19: one name, one value (L-13) -----------------------------------------
namespace Renderer { static int getScreenWidth() { return 640; } }
// The text of a lift (T35_X/<inc>), for a case that asserts a definition rather than runs it.
static std::string t35_slurpX(const std::string& inc) { std::ifstream in(std::string(T35_X) + "/" + inc); std::stringstream ss; ss << in.rdbuf(); return ss.str(); }
// S8 (D-WORKFLOW-211): the keyboard's value read from its line's text (the factor after
// getScreenWidth()*), so the case holds whatever the line's macro is called.
static double kbPad() {
	std::string l = t35_slurpX("x_kb_pad.inc");
	auto i = l.find("getScreenWidth()*");
	return i == std::string::npos ? -1.0 : 640.0 * std::stod(l.substr(i + 17));
}
static double menuPad() {
	#include "x_menu_pad.inc"
	double v = BUTTON_GRID_HORIZ_PADDING;
	#undef BUTTON_GRID_HORIZ_PADDING
	return v;
}

// 3.19, re-shaped under ruling 3 (D-UI-135; D-WORKFLOW-211): stage C asserted the two values
// equal (`kbPad() == doctest::Approx(menuPad())`, 3.33333 against 14.08 at the pin), which
// fitted one definition read by both. The ruling keeps the keyboard's value under its own
// name, so the case asserts the name is defined once, in MenuComponent.cpp, and the value kept.
TEST_CASE("3.19 BUTTON_GRID_HORIZ_PADDING is defined once, in MenuComponent.cpp; the keyboard's key inset keeps its value under its own name (guis/GuiTextEditPopupKeyboard.cpp:14, :220 against components/MenuComponent.cpp:14; PL-11, #1351)")
{
	CHECK(t35_slurpX("x_menu_pad.inc").find("#define BUTTON_GRID_HORIZ_PADDING") != std::string::npos);
	CHECK(t35_slurpX("x_kb_pad.inc").find("BUTTON_GRID_HORIZ_PADDING") == std::string::npos);
	CHECK(t35_slurpX("x_kb_pad_use.inc").find("BUTTON_GRID_HORIZ_PADDING") == std::string::npos);
	CHECK(kbPad() == doctest::Approx(640 * 0.0052083333));
	CHECK(menuPad() == doctest::Approx(640 * 0.022));
}

// ---- 3.11: the exists cache after a writer outside Utils::FileSystem (L-07) ---
struct Settings { static bool UseFileCache() { return true; } };
namespace Utils { namespace FileSystem {
	std::string getGenericPath(const std::string& p) { return p; }
	std::string getParent(const std::string& p) { auto i = p.find_last_of('/'); return i == std::string::npos ? "" : p.substr(0, i); }
	std::string resolveSymlink(const std::string& p) { return p; }
	std::string getFileName(const std::string& p) { auto i = p.find_last_of('/'); return i == std::string::npos ? p : p.substr(i + 1); }
	#include "x_fs_cache.inc"
	bool exists(const std::string& _path, bool enableCache = true);
	#include "x_fs_exists.inc"
} }

// 3.11 is reshaped in S6 (D-WORKFLOW-211) and moved below, after the writer's double: as
// stage C wrote it, it asserted the cache's own answer after a save_file (exists(p) false
// after the write, the uncached read true), which S6 does not change; it now reads through
// writeDeviceConfig's lifted :1187, #1340's first checkbox.

// ---- 3.1: a probe holds the list lock (L-11, #1283's es-core half) ------------
struct SlowWatcher : IWatcher
{
	std::atomic<bool> started{ false };
	bool enabled() override { return true; }
	int updateTime() override { return 60000; }
	int initialUpdateTime() override { return 0; }
	bool check() override { started = true; std::this_thread::sleep_for(std::chrono::milliseconds(1500)); return false; }
};

TEST_CASE("3.1 ResetComponent from another thread does not wait for a running probe (watchers/WatchersManager.cpp:92-104 against :181-199)")
{
	static SlowWatcher w;
	WatchersManager::getInstance();
	WatchersManager::RegisterComponent(&w);
	for (int i = 0; i < 400 && !w.started; i++)
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	REQUIRE(w.started);
	auto t0 = std::chrono::steady_clock::now();
	WatchersManager::ResetComponent(&w);
	auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - t0).count();
	MESSAGE("ResetComponent returned after " << ms << " ms");
	CHECK(ms < 300);
	WatchersManager::UnregisterComponent(&w);
	WatchersManager::stop();
}

// ---- S1, PL-15 (#1342): back on the drive dialogs; 3.18 the accelerator ------
// The pin's accelerator (guis/GuiMsgBox.cpp:116-134) runs over buttons built
// from the labels each drive dialog's call passes, read in order from the
// call's own lines (Window.cpp, lifted as text): a label is a line that opens
// with _("...") and a comma, as every name argument in those calls does.
namespace mb
{
	static std::string _(const std::string& s) { return s; }
	namespace Utils { namespace String {
		static std::string toUpper(const std::string& s) { std::string r = s; for (auto& c : r) c = (char)toupper((unsigned char)c); return r; }
	} }
	struct Button
	{
		std::string t; std::function<void()> f;
		std::string getText() const { return t; }
		std::function<void()> getPressedFunc() const { return f; }
	};
	struct Box
	{
		std::vector<std::shared_ptr<Button>> mButtons;
		std::function<void()> mAcceleratorFunc;
		std::string pressed;
		explicit Box(const std::vector<std::string>& labels)
		{
			for (auto& l : labels)
				mButtons.push_back(std::make_shared<Button>(Button{ l, [this, l] { pressed = l; } }));
			#include "x_mb_accel.inc"
		}
		std::string back() { pressed.clear(); if (mAcceleratorFunc) mAcceleratorFunc(); return pressed; }
	};
	static std::vector<std::string> labels(const std::string& inc)
	{
		std::ifstream in(std::string(T35_X) + "/" + inc);
		std::vector<std::string> out;
		std::string line;
		while (std::getline(in, line))
		{
			auto i = line.find_first_not_of(" \t");
			if (i == std::string::npos || line.compare(i, 3, "_(\"") != 0)
				continue;
			auto e = line.find("\")", i + 3);
			if (e != std::string::npos && line.find(',', e) != std::string::npos)
				out.push_back(line.substr(i + 3, e - i - 3));
		}
		return out;
	}
	static std::string backOn(const std::string& inc) { Box b(labels(inc)); return b.back(); }
}

TEST_CASE("3.18 the accelerator's three branches: the only button, the first named OK or NO, else the last (guis/GuiMsgBox.cpp:116-134; recorded)")
{
	CHECK(mb::Box({ "CLOSE" }).back() == "CLOSE");
	CHECK(mb::Box({ "YES", "NO", "MAYBE" }).back() == "NO");
	CHECK(mb::Box({ "ok", "CANCEL" }).back() == "ok");
	CHECK(mb::Box({ "A", "B", "C" }).back() == "C");
}

TEST_CASE("S1 back on GAME DRIVE DETECTED with an id lands on NO, IGNORE THIS TIME, with YES first (Window.cpp's call through guis/GuiMsgBox.cpp:116-134; PL-15, #1342)")
{
	auto l = mb::labels("x_dlg_game_id.inc");
	REQUIRE(l.size() == 3);
	CHECK(l.front().rfind("YES", 0) == 0);
	CHECK(mb::backOn("x_dlg_game_id.inc") == "NO, IGNORE THIS TIME");
}

TEST_CASE("S1 back on NEW DRIVE DETECTED with an id lands on NO, IGNORE THIS TIME, with YES first (PL-15, #1342)")
{
	auto l = mb::labels("x_dlg_new_id.inc");
	REQUIRE(l.size() == 3);
	CHECK(l.front().rfind("YES", 0) == 0);
	CHECK(mb::backOn("x_dlg_new_id.inc") == "NO, IGNORE THIS TIME");
}

TEST_CASE("S1 back on NEW DRIVE DETECTED without an id lands on NO, IGNORE, with YES first (PL-15, #1342)")
{
	auto l = mb::labels("x_dlg_new.inc");
	REQUIRE(l.size() == 2);
	CHECK(l.front().rfind("YES", 0) == 0);
	CHECK(mb::backOn("x_dlg_new.inc") == "NO, IGNORE");
}

TEST_CASE("S1 back on GAME DRIVE DETECTED without an id binds NO by name (PL-15, #1342; the guard, PASS at the pin)")
{
	REQUIRE(mb::labels("x_dlg_game.inc").size() == 2);
	CHECK(mb::backOn("x_dlg_game.inc") == "NO");
}

TEST_CASE("S1 back on ARE YOU SURE? binds NO by name (ruling 5: stays NO / YES; recorded)")
{
	REQUIRE(mb::labels("x_dlg_sure.inc").size() == 2);
	CHECK(mb::backOn("x_dlg_sure.inc") == "NO");
}

// ---- S2, PL-02 (#1338): a toast a card takes off the screen keeps its place ---
// q::WindowQ's requeue() runs the lifted re-queue and next() the lifted pop; the
// case clears the popups as stopNotificationPopups does. Three toasts, so a fix
// of the pop alone (B, C, A) fails as the pin's pop does (A, C, B).
TEST_CASE("S2 a toast a card takes off the screen shows before the toasts queued after it (Window.cpp:339-340 with :1163-1164; PL-02, #1338)")
{
	q::WindowQ w;
	q::Popup a{"A on screen"};
	w.mNotificationPopups.push_back(&a);
	w.mNotificationMessages.push_back({"B queued", 3000});
	w.mNotificationMessages.push_back({"C queued", 3000});
	w.requeue();
	w.mNotificationPopups.clear();
	CHECK(w.next().first == "A on screen");
	CHECK(w.next().first == "B queued");
	CHECK(w.next().first == "C queued");
}

// ---- 3.16, PL-25 (#1354): the help bar's dpad merge ---------------------------
// The pin's setHelpPrompts (Window.cpp:1005-1078) lifted whole into a window
// double whose help component keeps the prompts it is given.
namespace hp
{
	struct HelpStyle {};
	static char* BUTTON_OK = (char*)"a";
	static char* BUTTON_BACK = (char*)"b";
	struct Help
	{
		std::vector<HelpPrompt> prompts;
		void* getGrid() { return nullptr; }
		void clearPrompts() { prompts.clear(); }
		void setStyle(const HelpStyle&) {}
		void setPrompts(const std::vector<HelpPrompt>& p) { prompts = p; }
	};
	struct Window
	{
		Help help; Help* mHelp = &help; int mClockElapsed = 0;
		void setHelpPrompts(const std::vector<HelpPrompt>& prompts, const HelpStyle& style);
	};
	#include "x_help_prompts.inc"
	static std::string bar(const std::vector<HelpPrompt>& in)
	{
		Window w;
		w.setHelpPrompts(in, HelpStyle());
		std::string out;
		for (auto& p : w.mHelp->prompts)
			out += (out.empty() ? "" : " | ") + p.first + " " + p.second;
		return out;
	}
}

TEST_CASE("3.16 the dpad's two halves with one action merge into up/down/left/right, either order (Window.cpp:1031-1041; PL-25, #1354)")
{
	CHECK(hp::bar({ HelpPrompt("up/down", "CHOOSE"), HelpPrompt("left/right", "CHOOSE") }) == "up/down/left/right CHOOSE");
	CHECK(hp::bar({ HelpPrompt("left/right", "CHOOSE"), HelpPrompt("up/down", "CHOOSE") }) == "up/down/left/right CHOOSE");
}

TEST_CASE("3.16 an unrelated prompt sharing the action text is kept, not replaced (Window.cpp:1031-1041; PL-25, #1354)")
{
	auto b = hp::bar({ HelpPrompt("a", "CHOOSE"), HelpPrompt("up/down", "CHOOSE") });
	CHECK(b.find("a CHOOSE") != std::string::npos);
	CHECK(b.find("up/down CHOOSE") != std::string::npos);
}

// ---- S3, PL-05 (#1305's window half): a page that owns the screen holds the screensaver
// render's start (Window.cpp:777-779) and startScreenSaver lifted verbatim into a
// window double: a gui stack of page doubles, a screensaver that records its start.
namespace ss
{
	struct Settings { static int ScreenSaverTime() { return 1000; } };
	struct GuiComponent
	{
		bool hold = false, activated = false;
		bool allowScreenSaver() { return !hold; }
		void onScreenSaverActivate() { activated = true; }
	};
	struct ScreenSaver { bool started = false; void startScreenSaver() { started = true; } };
	struct Window
	{
		ScreenSaver saver; ScreenSaver* mScreenSaver = &saver; bool mRenderScreenSaver = false;
		std::vector<GuiComponent*> mScreenExtras, mGuiStack;
		unsigned int mTimeSinceLastInput = 0;
		GuiComponent* peekGui() { return mGuiStack.empty() ? nullptr : mGuiStack.back(); }
		void startScreenSaver();
		void frame(unsigned int idle)
		{
			mTimeSinceLastInput = idle;
			#include "x_ss_render.inc"
		}
	};
	#include "x_ss_start.inc"
}

TEST_CASE("S3 a top page that holds the screensaver keeps it off past the idle time, and it starts once the page lets go (Window.cpp:777-779, startScreenSaver; PL-05, #1305)")
{
	ss::GuiComponent menu, job;
	job.hold = true;
	ss::Window w;
	w.mGuiStack = { &menu, &job };
	w.frame(5000);
	CHECK_FALSE(w.saver.started);
	CHECK_FALSE(job.activated);
	job.hold = false;
	w.frame(5016);
	CHECK(w.saver.started);
}

TEST_CASE("S3 a top page that does not hold it lets the screensaver start, as every upstream page does (the guard; PASS before and after)")
{
	ss::GuiComponent menu, page;
	ss::Window w;
	w.mGuiStack = { &menu, &page };
	w.frame(5000);
	CHECK(w.saver.started);
	CHECK(page.activated);
}

// ---- S4, PL-01 (#1283's es-core half): the watchers probe outside the list lock -----
// The pin's watchers/WatchersManager.cpp, linked as for 3.1.
struct QuickWatcher : IWatcher
{
	std::atomic<int> probes{ 0 };
	bool enabled() override { return true; }
	int updateTime() override { return 60000; }
	int initialUpdateTime() override { return 60000; }
	bool check() override { probes++; return false; }
};

TEST_CASE("S4 a second watcher's ResetComponent returns at once while the first's probe runs (watchers/WatchersManager.cpp:92-104 against :181-199; PL-01, #1283)")
{
	static SlowWatcher slow;
	static QuickWatcher other;
	slow.started = false;
	WatchersManager::getInstance();
	WatchersManager::RegisterComponent(&slow);
	WatchersManager::RegisterComponent(&other);
	for (int i = 0; i < 400 && !slow.started; i++)
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	REQUIRE(slow.started);
	auto t0 = std::chrono::steady_clock::now();
	WatchersManager::ResetComponent(&other);
	auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - t0).count();
	MESSAGE("the second watcher's ResetComponent returned after " << ms << " ms");
	CHECK(ms < 300);
	WatchersManager::UnregisterComponent(&other);
	WatchersManager::UnregisterComponent(&slow);
	WatchersManager::stop();
}

struct ResetWatcher : IWatcher
{
	std::atomic<int> probes{ 0 };
	bool enabled() override { return true; }
	int updateTime() override { return 60000; }
	int initialUpdateTime() override { return 0; }
	bool check() override { probes++; if (probes == 1) std::this_thread::sleep_for(std::chrono::milliseconds(600)); return false; }
};

TEST_CASE("S4 a reset during a probe is not lost: the watcher is probed again at the next pass, not after its update time (WatchersManager.cpp:92-104, :199; PL-01, #1283; PASS at the pin, the guard)")
{
	static ResetWatcher w;
	WatchersManager::getInstance();
	WatchersManager::RegisterComponent(&w);
	for (int i = 0; i < 400 && w.probes == 0; i++)
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	REQUIRE(w.probes >= 1);
	WatchersManager::ResetComponent(&w);   // during the first, 600 ms probe
	for (int i = 0; i < 400 && w.probes < 2; i++)
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	CHECK(w.probes >= 2);
	WatchersManager::UnregisterComponent(&w);
	WatchersManager::stop();
}

// ---- S6, PL-04 (#1340) and PL-08 (#1348): the input file's writer ---------------
// writeDeviceConfig (InputManager.cpp:1179-1240) lifted whole into an InputManager double
// whose paths are a temporary directory's; the exists cache is 3.11's lift above, and
// utils/AtomicFileUtil.cpp (T21's) is linked.
namespace im6
{
	enum LogLevel { LogError };
	struct Line { template <class T> Line& operator<<(const T&) { return *this; } };
	#define LOG(l) im6::Line()
	#define WINSTRINGW(x) (x)
	namespace Scripting { static void fireEvent(const std::string&) {} }
	struct InputConfig
	{
		std::string guid, name;
		int inputs = 1;
		std::string getDeviceGUIDString() { return guid; }
		std::string getDeviceName() { return name; }
		void writeToXML(pugi::xml_node& parent)
		{
			pugi::xml_node cfg = parent.append_child("inputConfig");
			cfg.append_attribute("type") = "joystick";
			cfg.append_attribute("deviceName") = name.c_str();
			cfg.append_attribute("deviceGUID") = guid.c_str();
			for (int i = 0; i < inputs; i++)
			{
				pugi::xml_node in = cfg.append_child("input");
				in.append_attribute("name") = ("b" + std::to_string(i)).c_str();
				in.append_attribute("type") = "button";
				in.append_attribute("id") = i;
				in.append_attribute("value") = 1;
			}
		}
	};
	struct InputManager
	{
		static std::string& cfg() { static std::string p; return p; }
		static std::string& last() { static std::string p; return p; }
		static std::string getConfigPath() { return cfg(); }
		static std::string getTemporaryConfigPath() { return last(); }
		bool initialized() const { return true; }
		void doOnFinish() {}
		bool loadInputConfig(InputConfig*) { return true; }
		void writeDeviceConfig(InputConfig* config);
	};
	#include "x_im_writecfg.inc"
	#undef LOG
	#undef WINSTRINGW

	static std::string tmpdir(const char* tag)
	{
		std::string d = std::string("/workspace/tmp/m6-t35/tmp/") + tag + "-XXXXXX";
		std::vector<char> b(d.begin(), d.end());
		b.push_back(0);
		return mkdtemp(b.data()) ? std::string(b.data()) : std::string();
	}
	static void paths(const std::string& d) { InputManager::cfg() = d + "/es_input.cfg"; InputManager::last() = d + "/es_last_input.cfg"; }
	static void tidy(const std::string& d, const std::vector<std::string>& extra = {})
	{
		unlink(InputManager::cfg().c_str());
		unlink(InputManager::last().c_str());
		for (auto& e : extra) unlink((d + "/" + e).c_str());
		rmdir(d.c_str());
	}
	static std::string slurp(const std::string& p) { std::ifstream f(p, std::ios::binary); std::stringstream ss; ss << f.rdbuf(); return ss.str(); }
	static int entries(const std::string& p)
	{
		pugi::xml_document d;
		if (!d.load_file(p.c_str())) return -1;
		int n = 0;
		for (auto c = d.child("inputList").child("inputConfig"); c; c = c.next_sibling("inputConfig")) n++;
		return n;
	}
}

TEST_CASE("3.11 two configurations in one session both reach es_input.cfg when the file was absent at startup (InputManager.cpp:1187 through the lifted writeDeviceConfig; PL-04, #1340; reshaped in S6)")
{
	std::string d = im6::tmpdir("t311");
	REQUIRE(!d.empty());
	im6::paths(d);
	CHECK_FALSE(Utils::FileSystem::exists(im6::InputManager::cfg()));   // the startup check, as tryLoadInputConfig :893 makes it
	im6::InputManager m;
	im6::InputConfig a{ "0300aaaa", "Pad A" }, b{ "0300bbbb", "Pad B" };
	m.writeDeviceConfig(&a);
	m.writeDeviceConfig(&b);
	CHECK(im6::entries(im6::InputManager::cfg()) == 2);
	im6::tidy(d);
}

TEST_CASE("S6 the input files' bytes are save_file's for one document (InputManager.cpp:1225, :1232; PL-08, #1348; PASS at the pin, the format's guard)")
{
	std::string d = im6::tmpdir("s6bytes");
	REQUIRE(!d.empty());
	im6::paths(d);
	im6::InputManager m;
	im6::InputConfig a{ "0300aaaa", "Pad A", 40 };
	m.writeDeviceConfig(&a);
	pugi::xml_document ref;
	pugi::xml_node root = ref.append_child("inputList");
	a.writeToXML(root);
	REQUIRE(ref.save_file((d + "/ref.cfg").c_str()));
	CHECK(im6::slurp(im6::InputManager::cfg()) == im6::slurp(d + "/ref.cfg"));
	CHECK(im6::slurp(im6::InputManager::last()) == im6::slurp(d + "/ref.cfg"));
	im6::tidy(d, { "ref.cfg" });
}

TEST_CASE("S6 a reader polling es_input.cfg while it is rewritten sees only whole documents (InputManager.cpp:1225; PL-08, #1348)")
{
	std::string d = im6::tmpdir("s6poll");
	REQUIRE(!d.empty());
	im6::paths(d);
	im6::InputManager m;
	im6::InputConfig a{ "0300aaaa", "Pad A", 3000 };
	m.writeDeviceConfig(&a);
	std::atomic<bool> done{ false };
	std::atomic<int> reads{ 0 }, shorts{ 0 };
	std::thread reader([&] {
		while (!done)
		{
			std::string s = im6::slurp(im6::InputManager::cfg());
			reads++;
			if (s.size() < 13 || s.compare(s.size() - 13, 13, "</inputList>\n") != 0)
				shorts++;
		}
	});
	for (int i = 0; i < 60; i++)
		m.writeDeviceConfig(&a);
	done = true;
	reader.join();
	MESSAGE("the reader made " << reads.load() << " reads, " << shorts.load() << " of a short file");
	CHECK(shorts.load() == 0);
	im6::tidy(d);
}

// ---- S8, PL-12 (#1352): CLEAR and the keyboard's x ---------------------------
// The text popup's CLEAR button (guis/GuiTextEditPopup.cpp:34), the keyboard's x
// (GuiTextEditPopupKeyboard.cpp:392-397) and its CLEAR key (:491-496), each lifted
// verbatim into a popup double that counts its deletions and its OK callback's calls.
namespace pp
{
	static std::string _(const std::string& s) { return s; }
	static int deleted = 0, committed = 0;
	struct Text { std::string v; size_t cursor = 99; void setValue(const std::string& s) { v = s; } std::string getValue() const { return v; } void setCursor(size_t c) { cursor = c; } };
	struct Window {};
	struct ButtonComponent
	{
		std::string label; std::function<void()> f;
		ButtonComponent(Window*, const std::string& l, const std::string&, const std::function<void()>& fn) : label(l), f(fn) {}
	};
	struct Input { int value = 1; };
	struct Config { bool isMappedTo(const std::string& n, Input) { return n == "x"; } };
	struct Popup
	{
		Window* mWindow = nullptr;
		std::shared_ptr<Text> mText = std::make_shared<Text>();
		std::function<void(const std::string&)> mOkCallback;
		std::vector<std::shared_ptr<ButtonComponent>> buttons;
		explicit Popup(const std::function<void(const std::string&)>& okCallback) : mOkCallback(okCallback)
		{
			mText->setValue("my-cloud-folder");
			#include "x_pp_clear.inc"
		}
		~Popup() { deleted++; }
		bool x(Config* config, Input input)
		{
			#include "x_kb_x.inc"
			return false;
		}
		void key(const std::string& key)
		{
			if (key == "not a key") {}
			#include "x_kb_clear.inc"
		}
	};
	static Popup* fresh() { deleted = 0; committed = 0; return new Popup([](const std::string&) { committed++; }); }
}

TEST_CASE("S8 CLEAR on the text popup empties the field and keeps the popup open, committing nothing (guis/GuiTextEditPopup.cpp:34; PL-12, #1352)")
{
	pp::Popup* p = pp::fresh();
	REQUIRE(p->buttons.size() == 1);
	auto press = p->buttons[0]->f;   // a copy: at the pin the press deletes the popup and its button
	press();
	CHECK(pp::committed == 0);
	CHECK(pp::deleted == 0);
	if (pp::deleted == 0)
	{
		CHECK(p->mText->getValue() == "");
		delete p;
	}
}

TEST_CASE("S8 the keyboard's x empties the field and keeps the keyboard open (guis/GuiTextEditPopupKeyboard.cpp:392-397; PL-12, #1352)")
{
	pp::Popup* p = pp::fresh();
	pp::Config c;
	CHECK(p->x(&c, pp::Input()));
	CHECK(pp::committed == 0);
	CHECK(pp::deleted == 0);
	if (pp::deleted == 0)
	{
		CHECK(p->mText->getValue() == "");
		CHECK(p->mText->cursor == 0);
		delete p;
	}
}

TEST_CASE("S8 the keyboard's CLEAR key empties the field and keeps the keyboard open (guis/GuiTextEditPopupKeyboard.cpp:491-496; PL-12, #1352)")
{
	pp::Popup* p = pp::fresh();
	p->key("CLEAR");
	CHECK(pp::committed == 0);
	CHECK(pp::deleted == 0);
	if (pp::deleted == 0)
	{
		CHECK(p->mText->getValue() == "");
		CHECK(p->mText->cursor == 0);
		delete p;
	}
}

// ---- 3.21, PL-16 (#1353): the configuration page's subtitle (lifted as text) --
TEST_CASE("3.21 the configuration page's subtitle names the pad being configured, GAMEPAD when it has no name (guis/GuiInputConfig.cpp:128-136; PL-16, #1353)")
{
	std::string t = t35_slurpX("x_cfg_subtitle.inc");
	CHECK(t.find("getDeviceName()") != std::string::npos);
	CHECK(t.find("getDeviceId() + 1") == std::string::npos);
	CHECK(t.find("_(\"GAMEPAD\")") != std::string::npos);
}
