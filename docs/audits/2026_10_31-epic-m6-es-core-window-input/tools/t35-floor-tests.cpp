// T35 (#682) stage E, S0 (ruling 21): floor-tests, the floor cases no stream holds --
// 3.6, 3.7, 3.8, 3.9, 3.12, 3.13, 3.20, 3.22, 3.24, 3.25 -- each over the pin's lines
// lifted verbatim by tools/t35-extract.py (a range that moved is refused and this binary is
// not built). InputConfig's functions are lifted whole and compiled against the pin's own
// InputConfig.h (SDL from stage-a/fakes, the log from tests/app-unit/fakes/Log.h). Each case
// asserts what the brief's floor table says the pin does; it is run at the pin and its PASS or
// FAIL recorded as written. 3.20 and 3.24 read their lifts as text (T35_X names the folder).
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <unordered_map>
#include <vector>
#define PUGIXML_HEADER_ONLY
#include "pugixml/src/pugixml.hpp"
#include "Log.h"            // tests/app-unit/fakes/Log.h: every line kept
#include "InputConfig.h"    // the pin's header
#include "MameNames.h"      // the pin's header: ArcadeRom, ArcadeRomType

namespace FakeLog
{
	std::vector<std::string>& lines() { static std::vector<std::string> l; return l; }
	std::mutex& lock() { static std::mutex m; return m; }
}
static bool logHas(const std::string& s) { for (auto& l : FakeLog::lines()) if (l.find(s) != std::string::npos) return true; return false; }
static std::string slurp(const std::string& name) { std::ifstream f(std::string(T35_X) + "/x_" + name + ".inc"); std::stringstream ss; ss << f.rdbuf(); return ss.str(); }
static size_t count(const std::string& hay, const std::string& needle) { size_t n = 0; for (size_t i = hay.find(needle); i != std::string::npos; i = hay.find(needle, i + 1)) n++; return n; }

// ---- InputConfig's functions, lifted whole (3.7, 3.8, 3.9) -------------------------
struct Settings { bool invert = false; static Settings* getInstance() { static Settings s; return &s; } bool getBool(const std::string&) { return invert; } };
#include "x_ic_utils.inc"
#include "x_ic_ctor.inc"
#include "x_ic_map.inc"
#include "x_ic_buttons.inc"

TEST_CASE("3.7 mapInput lower-cases the name; a hat matches by bitmask, an axis by sign (InputConfig.cpp:186-189, :210-231)")
{
	InputConfig c(0, 0, "Pad", "0300abcd", 12, 1, 4, "");
	c.mapInput("HotKeyEnable", Input(0, TYPE_BUTTON, 9, 1, true));
	Input got;
	CHECK(c.getInputByName("hotkeyenable", &got));
	CHECK(c.isMappedTo("HOTKEYENABLE", Input(0, TYPE_BUTTON, 9, 1, false)));
	c.mapInput("up", Input(0, TYPE_HAT, 0, 1, true));
	CHECK(c.isMappedTo("up", Input(0, TYPE_HAT, 0, 1 | 8, false)));      // a diagonal carries the up bit
	CHECK_FALSE(c.isMappedTo("up", Input(0, TYPE_HAT, 0, 4, false)));    // down does not
	c.mapInput("leftanalogleft", Input(0, TYPE_AXIS, 0, -1, true));
	CHECK(c.isMappedTo("leftanalogleft", Input(0, TYPE_AXIS, 0, -1, false)));
	CHECK_FALSE(c.isMappedTo("leftanalogleft", Input(0, TYPE_AXIS, 0, 1, false)));
	CHECK(c.isMappedLike("left", Input(0, TYPE_AXIS, 0, -1, false)));
}

TEST_CASE("3.7 the XML round trip keeps every mapping; an unknown type is skipped with LogError (InputConfig.cpp:285-345)")
{
	InputConfig a(0, 0, "Pad", "0300abcd", 12, 1, 4, "");
	a.mapInput("a", Input(0, TYPE_BUTTON, 1, 1, true));
	a.mapInput("up", Input(0, TYPE_HAT, 0, 1, true));
	a.mapInput("joystick1left", Input(0, TYPE_AXIS, 0, -1, true));
	pugi::xml_document doc;
	pugi::xml_node root = doc.append_child("inputList");
	a.writeToXML(root);
	pugi::xml_node cfg = root.child("inputConfig");
	REQUIRE(cfg);
	CHECK(std::string(cfg.attribute("deviceName").value()) == "Pad");
	InputConfig b(0, 0, "Pad", "0300abcd", 12, 1, 4, "");
	b.loadFromXML(cfg);
	for (auto n : { "a", "up", "joystick1left" })
	{
		Input x, y;
		REQUIRE(a.getInputByName(n, &x));
		REQUIRE(b.getInputByName(n, &y));
		CHECK(x.type == y.type); CHECK(x.id == y.id); CHECK(x.value == y.value);
	}
	pugi::xml_document bad;
	bad.load_string("<inputConfig><input name=\"x\" type=\"wobble\" id=\"3\" value=\"1\"/></inputConfig>");
	FakeLog::lines().clear();
	pugi::xml_node bn = bad.child("inputConfig");
	b.loadFromXML(bn);
	Input z;
	CHECK_FALSE(b.getInputByName("x", &z));
	CHECK(logHas("is invalid! Skipping input"));
}

TEST_CASE("3.8 buttonLabel returns the key unchanged off WIN32, an unknown key and a translated one included (InputConfig.cpp:353-366)")
{
	CHECK(InputConfig::buttonLabel("a") == "a");
	CHECK(InputConfig::buttonLabel("up/down") == "up/down");
	CHECK(InputConfig::buttonLabel("haut/bas") == "haut/bas");
	CHECK(InputConfig::buttonLabel("nonsense") == "nonsense");
}

TEST_CASE("3.9 AssignActionButtons sets OK and BACK from the setting, the same on a second call (InputConfig.cpp:347-351, :403-414)")
{
	Settings::getInstance()->invert = false;
	InputConfig::AssignActionButtons();
	std::string ok1 = BUTTON_OK, back1 = BUTTON_BACK;
	InputConfig::AssignActionButtons();
	CHECK(std::string(BUTTON_OK) == ok1); CHECK(std::string(BUTTON_BACK) == back1);
	CHECK(ok1 == "b"); CHECK(back1 == "a");       // off WIN32 the default puts OK on b (the pin's :411-412)
	Settings::getInstance()->invert = true;
	InputConfig::AssignActionButtons();
	CHECK(std::string(BUTTON_OK) == "a"); CHECK(std::string(BUTTON_BACK) == "b");
	Settings::getInstance()->invert = false;
	InputConfig::AssignActionButtons();
}

// ---- 3.12: the hotkey fallback (InputManager.cpp:1101-1108) ------------------------
static void hotkeyFallback(InputConfig* config, bool isConfigured)
{
	#include "x_im_hotkey.inc"
}

TEST_CASE("3.12 a mapping with no hotkey gets select copied to hotkey; one that has hotkey keeps it (InputManager.cpp:1101-1108)")
{
	InputConfig c(0, 0, "Pad", "g", 12, 1, 4, "");
	c.mapInput("select", Input(0, TYPE_BUTTON, 6, 1, true));
	hotkeyFallback(&c, true);
	Input h;
	REQUIRE(c.getInputByName("hotkey", &h));
	CHECK(h.id == 6);
	InputConfig d(0, 0, "Pad", "g", 12, 1, 4, "");
	d.mapInput("select", Input(0, TYPE_BUTTON, 6, 1, true));
	d.mapInput("hotkey", Input(0, TYPE_BUTTON, 10, 1, true));
	hotkeyFallback(&d, true);
	REQUIRE(d.getInputByName("hotkey", &h));
	CHECK(h.id == 10);
	InputConfig e(0, 0, "Pad", "g", 12, 1, 4, "");
	e.mapInput("select", Input(0, TYPE_BUTTON, 6, 1, true));
	hotkeyFallback(&e, false);
	CHECK_FALSE(e.getInputByName("hotkey", &h));   // not configured: nothing copied
}

// ---- 3.13: doOnFinish hands every onfinish command over, synchronously (InputManager.cpp:1244-1283)
#define WINSTRINGW(x) (x)
namespace f13
{
	static std::string cfgPath;
	static std::vector<std::string> ran;
	static std::vector<int> codes;
	namespace Utils
	{
		namespace FileSystem { static bool exists(const std::string& p) { struct stat st; return stat(p.c_str(), &st) == 0; } }
		namespace String { static std::string maskSecrets(const std::string& s) { return s; } }
		namespace Platform
		{
			struct ProcessStartInfo
			{
				std::string cmd;
				ProcessStartInfo(const std::string& c) : cmd(c) {}
				int run() { ran.push_back(cmd); int rc = codes.empty() ? 0 : codes.front(); if (!codes.empty()) codes.erase(codes.begin()); return rc; }
			};
		}
	}
	static bool initialized() { return true; }
	static std::string getConfigPath() { return cfgPath; }
	static void doOnFinish()
	{
		#include "x_im_onfinish.inc"
	}
}

TEST_CASE("3.13 every onfinish <command> is handed to the executor as written, in order; a non-zero exit is a LogWarning (InputManager.cpp:1244-1283)")
{
	char dir[] = "/workspace/tmp/m6-t35/tmp/t313-XXXXXX";
	REQUIRE(mkdtemp(dir) != nullptr);
	f13::cfgPath = std::string(dir) + "/es_input.cfg";
	{
		std::ofstream o(f13::cfgPath);
		o << "<inputList><inputAction type=\"onfinish\"><command>first --one</command><command>second --two</command></inputAction></inputList>";
	}
	f13::ran.clear(); f13::codes = { 0, 3 }; FakeLog::lines().clear();
	std::streambuf* saved = std::cout.rdbuf(); std::ostringstream sink; std::cout.rdbuf(sink.rdbuf());
	f13::doOnFinish();
	std::cout.rdbuf(saved);
	REQUIRE(f13::ran.size() == 2);
	CHECK(f13::ran[0] == "first --one");
	CHECK(f13::ran[1] == "second --two");
	CHECK(logHas("nonzero exit code 3"));
	unlink(f13::cfgPath.c_str()); rmdir(dir);
}

// ---- 3.6: the single-script pass (Scripting.cpp:182-207) ---------------------------
namespace f6
{
	struct Entry { std::string path; bool directory; };
	static std::vector<std::pair<std::string, std::string>> ran;
	static std::set<std::string> _supportedExtensions = { ".exe", ".cmd", ".bat", ".ps1", ".sh", ".py" };
	namespace Paths { static std::string getUserEmulationStationPath() { return "/u"; } static std::string getEmulationStationPath() { return "/e"; } }
	namespace VectorHelper { template <class T, class F> static std::vector<T> distinct(const std::vector<T>& v, F) { std::vector<T> o; for (auto& x : v) if (std::find(o.begin(), o.end(), x) == o.end()) o.push_back(x); return o; } }
	namespace Utils
	{
		namespace FileSystem
		{
			static bool exists(const std::string& d) { return d == "/u/scripts"; }
			static std::vector<Entry> getDirectoryFiles(const std::string& d) { return { { d + "/a.sh", false }, { d + "/b.py", false }, { d + "/notes.txt", false }, { d + "/sub.sh", true } }; }
			static std::string getExtension(const std::string& p) { auto i = p.rfind('.'); return i == std::string::npos ? "" : p.substr(i); }
		}
		namespace String { static std::string toLower(std::string s) { for (auto& c : s) c = (char)tolower(c); return s; } }
	}
	static bool isAsyncEvent(const std::string&) { return true; }
	static void executeScript(const std::string& script, const std::string& eventName, const std::string&, const std::string&, const std::string&, bool) { ran.push_back({ script, eventName }); }
	static void singlePass(const std::string& eventName, const std::string& arg1, const std::string& arg2, const std::string& arg3)
	{
		#include "x_sc_single.inc"
	}
}

TEST_CASE("3.6 the single-script pass runs .sh and .py with the event name first, and skips .txt and a directory (Scripting.cpp:182-207)")
{
	f6::ran.clear();
	f6::singlePass("game-start", "", "", "");
	REQUIRE(f6::ran.size() == 2);
	CHECK(f6::ran[0].first == "/u/scripts/a.sh"); CHECK(f6::ran[0].second == "game-start");
	CHECK(f6::ran[1].first == "/u/scripts/b.py"); CHECK(f6::ran[1].second == "game-start");
}

// ---- 3.20 and 3.24, as text --------------------------------------------------------
TEST_CASE("3.20 GuiMsgBox's constructor calls TextToSpeech::say three times (guis/GuiMsgBox.cpp:34-244; recorded, PL-24)")
{
	CHECK(count(slurp("mb_ctor"), "TextToSpeech::getInstance()->say(") == 3);
}

TEST_CASE("3.24 the favourites file is appended to at :71 and truncated then rewritten at :115 (FavoriteMusicManager.cpp; recorded, PL-08)")
{
	CHECK(slurp("fm_app").find("std::ios::app") != std::string::npos);
	CHECK(slurp("fm_trunc").find("std::ios::trunc") != std::string::npos);
}

// ---- 3.22: GuiInfoPopup's fade (guis/GuiInfoPopup.cpp:85-111) ----------------------
namespace f22
{
	static int now = 0;
	static int SDL_GetTicks() { return now; }
	namespace Math { static float easeOutCubic(float t) { t -= 1.0f; return t * t * t + 1.0f; } }
	struct Popup
	{
		int mStartTime = 0; int mDuration; bool mRunning = true; float mFadeOut = 0;
		explicit Popup(int d) : mDuration(d) {}
		int lastAlpha = -1;
		int frame()
		{
			draw();
			return lastAlpha;
		}
		void draw()
		{
			#include "x_ip_fade.inc"
			lastAlpha = alpha;
		}
	};
}

TEST_CASE("3.22 the toast fades in over 250 ms, holds, fades out over its last 250 ms, and stops past its duration (guis/GuiInfoPopup.cpp:85-111)")
{
	f22::Popup p(3000);
	f22::now = 1000; CHECK(p.frame() == 0);          // the first frame starts the clock (elapsed 0, alpha 0)
	f22::now = 1125; int half = p.frame(); CHECK(half > 0); CHECK(half < 255);
	f22::now = 1250; CHECK(p.frame() == 255);
	f22::now = 2500; CHECK(p.frame() == 255);
	f22::now = 3875; int out = p.frame(); CHECK(out < 255); CHECK(p.mFadeOut > 0.0f);
	CHECK(p.mRunning);
	f22::now = 4001; p.frame(); CHECK_FALSE(p.mRunning);
	f22::Popup q(3000); f22::now = 5000; q.frame(); f22::now = 4000; q.frame(); CHECK_FALSE(q.mRunning);   // the clock went back: stop
}

// ---- 3.25: a malformed arcade-roms file is reported, never thrown (MameNames.cpp:60-124)
#include "x_mame_ops.inc"
namespace f25
{
	static std::string xml;
	struct RM { std::string getResourcePath(const std::string&) { return xml; } static RM* getInstance() { static RM r; return &r; } };
	using ResourceManager = RM;
	namespace Utils { namespace FileSystem { static bool exists(const std::string& p) { struct stat st; return stat(p.c_str(), &st) == 0; } } }
	static std::unordered_map<std::string, ArcadeRom> parse()
	{
		std::unordered_map<std::string, ArcadeRom> mArcadeRoms;
		std::string xmlpath;
		pugi::xml_document doc;
		pugi::xml_parse_result result;
		#include "x_mame_roms.inc"
		return mArcadeRoms;
	}
}

TEST_CASE("3.25 a malformed or rootless arcade-roms file is logged as an error and loads nothing; a good one loads (MameNames.cpp:60-124)")
{
	char dir[] = "/workspace/tmp/m6-t35/tmp/t325-XXXXXX";
	REQUIRE(mkdtemp(dir) != nullptr);
	f25::xml = std::string(dir) + "/arcaderoms.xml";
	{ std::ofstream o(f25::xml); o << "<roms><rom id=\"pacman\" name=\"Pac-Man\"/><rom id=\"x\""; }
	FakeLog::lines().clear();
	CHECK(f25::parse().empty());
	CHECK(logHas("Error parsing XML file"));
	{ std::ofstream o(f25::xml); o << "<games><rom id=\"pacman\" name=\"Pac-Man\"/></games>"; }
	FakeLog::lines().clear();
	CHECK(f25::parse().empty());
	CHECK(logHas("<roms> root is missing"));
	{ std::ofstream o(f25::xml); o << "<roms><rom id=\"pacman\" name=\"Pac-Man\" vert=\"true\"/><rom id=\"neogeo\" bios=\"true\"/></roms>"; }
	auto m = f25::parse();
	CHECK(m.size() == 2);
	CHECK(m["pacman"].displayName == "Pac-Man");
	unlink(f25::xml.c_str()); rmdir(dir);
}
