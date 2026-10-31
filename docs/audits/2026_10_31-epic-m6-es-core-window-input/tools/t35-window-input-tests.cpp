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
#include <cstdio>
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

TEST_CASE("3.4 the shapes at the pin, recorded: a space quoted with double quotes, a double quote stripped")
{
	CHECK(sc::command_for("/s/hook.sh", "game-start", "a b.zip") == "/s/hook.sh game-start \"a b.zip\"");
	CHECK(sc::command_for("/s/hook.sh", "game-start", "a\"b.zip") == "/s/hook.sh game-start ab.zip");
}

TEST_CASE("3.5 a non-script file in a per-event folder is not run (Scripting.cpp:169-178, the filter WIN32-only)")
{
	sc::ran.clear();
	sc::per_event("/storage/.config/emulationstation/scripts/game-start", "game-start", "", "", "");
	CHECK(std::find(sc::ran.begin(), sc::ran.end(), "/storage/.config/emulationstation/scripts/game-start/notes.txt") == sc::ran.end());
	CHECK(std::find(sc::ran.begin(), sc::ran.end(), "/storage/.config/emulationstation/scripts/game-start/run.sh") != sc::ran.end());
}

// ---- 3.19: one name, one value (L-13) -----------------------------------------
namespace Renderer { static int getScreenWidth() { return 640; } }
static double kbPad() {
	#include "x_kb_pad.inc"
	double v = BUTTON_GRID_HORIZ_PADDING;
	#undef BUTTON_GRID_HORIZ_PADDING
	return v;
}
static double menuPad() {
	#include "x_menu_pad.inc"
	double v = BUTTON_GRID_HORIZ_PADDING;
	#undef BUTTON_GRID_HORIZ_PADDING
	return v;
}

TEST_CASE("3.19 BUTTON_GRID_HORIZ_PADDING means one thing (guis/GuiTextEditPopupKeyboard.cpp:14 against components/MenuComponent.cpp:14)")
{
	CHECK(kbPad() == doctest::Approx(menuPad()));
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

TEST_CASE("3.11 a file written by pugixml's save_file after a cached miss reads as present (InputManager.cpp:1187 with utils/FileSystemUtil.cpp, T36's)")
{
	char dir[] = "/workspace/tmp/m6-t35/tmp/t311-XXXXXX";
	REQUIRE(mkdtemp(dir) != nullptr);
	std::string p = std::string(dir) + "/es_input.cfg";
	CHECK_FALSE(Utils::FileSystem::exists(p));          // the first check, as tryLoadInputConfig :893 makes at startup
	pugi::xml_document doc;
	doc.append_child("inputList");
	REQUIRE(doc.save_file(p.c_str()));                   // the write, as writeDeviceConfig :1225 makes it
	CHECK(Utils::FileSystem::exists(p));                // the cached read, as :1187 makes it next: the merge depends on it
	CHECK(Utils::FileSystem::exists(p, false));         // the file is there (the uncached read, which also rewrites the entry, :161-162)
	CHECK(Utils::FileSystem::exists(p));                // after that rewrite the cached read agrees (recorded)
	unlink(p.c_str());
	rmdir(dir);
}

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
