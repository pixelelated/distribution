"""S4a (#680; #1276 PL-06, #1288 PL-23, #1283 PL-14): NetworkThread's token check, extracted as written.

    python3 -I s4a-token-check.py <es-app/src> [--tsan] [case ...]

Extracted from NetworkThread.cpp and .h as the tree has them: the
CheckCheevosTokenComponent class, every member the .cpp defines,
OnWatcherChanged's token branch (the `if (component ==
&mCheckCheevosTokenComponent)` block) and droppedAfterClosing when the
file has one; AppWindow.h and CheevosRetry.{h,cpp} whole. Doubled:
RetroAchievements::testAccount (a latch the test releases; the token is
"tok-" + the user), SystemConf (a map, every set() of the token
recorded; the page's own writes go round it), Window's queue, LOG, and
WatchersManager with the pin's lock shape (WatchersManager.cpp:181-199:
enabled(), check() and the notify under mWatchersLock, then
nextCheckTime = now + updateTime(); ResetComponent takes the same lock,
:92-100). The manager's clock is the harness's, a second a pass. The
components are globals, as NetworkThread is never deleted (main.cpp:898).

  switchoff  (i) PL-23: the sign-in held, the page turns achievements off
             and clears the token (GuiRetroAchievementsSettings.cpp:795-796),
             the latch released: no token is written
  account    (ii) the account changed under the sign-in: the old account's
             token is never written, and the drop is logged
  sameacct   ruling 5: the switch off and on again for the same account
             while the sign-in is held writes only that account's token,
             the value a fresh check writes
  reset      (iii) PL-14: ResetComponent from another thread while the
             sign-in is held (a latch that lets go by itself at 2 s) returns
             within 50 ms with the latch still held
  closing    (iv) EP-7: a token after AppWindow::closing() queues no task,
             and the drop is logged

The cases run in this order in one process; closing is last because
AppWindow's gate is the process's. --tsan builds under ThreadSanitizer
instead of ASan/UBSan.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import block, function, run  # noqa: E402

src = Path(sys.argv[1])
args = sys.argv[2:]
tsan = "--tsan" in args
cases = [a for a in args if not a.startswith("--")] or ["switchoff", "account", "sameacct", "reset", "closing"]
cpp = (src / "NetworkThread.cpp").read_text()
hdr = (src / "NetworkThread.h").read_text()
klass = function(hdr, r"^class CheckCheevosTokenComponent : public IWatcher", "S4a") + ";"
members = [function(cpp[m.start():], r"\A" + re.escape(m.group(0)), "S4a")
           for m in re.finditer(r"^[\w:<>\*& ]*\bCheckCheevosTokenComponent::~?\w+\(", cpp, re.M)]
branch = "if (component == &mCheckCheevosTokenComponent)" + block(cpp, r"if \(component == &mCheckCheevosTokenComponent\)", "S4a")
dropped = function(cpp, r"^static void droppedAfterClosing\(", "S4a") if re.search(r"^static void droppedAfterClosing\(", cpp, re.M) else ""
retry_h = (src / "CheevosRetry.h").read_text().replace("#pragma once", "")
retry_c = re.sub(r'#include "CheevosRetry.h"', "", (src / "CheevosRetry.cpp").read_text())
appwin = (src / "AppWindow.h").read_text()
print("extracted: the class, %d member(s) (%s), the token branch%s" % (
    len(members), ", ".join(re.search(r"::(~?\w+)\(", m).group(1) for m in members),
    ", droppedAfterClosing" if dropped else ""))

harness = r'''
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <functional>
#include <map>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

enum LogLevel { LogError, LogWarning, LogInfo, LogDebug };
static std::mutex gLogLock;
static std::vector<std::string> gLog;
struct LogLine
{
	std::ostringstream s;
	~LogLine() { std::lock_guard<std::mutex> l(gLogLock); gLog.push_back(s.str()); }
	template <class T> LogLine& operator<<(const T& v) { s << v; return *this; }
};
#define LOG(level) LogLine()
''' + retry_h + retry_c + appwin + r'''

struct SystemConf
{
	std::mutex m;
	std::map<std::string, std::string> kv;
	std::vector<std::string> tokenWrites;   // every set() of the token: the product's writes
	static SystemConf* getInstance() { static SystemConf s; return &s; }
	std::string get(const std::string& k) { std::lock_guard<std::mutex> l(m); auto it = kv.find(k); return it == kv.end() ? "" : it->second; }
	bool getBool(const std::string& k, bool def = false) { std::string v = get(k); return v.empty() ? def : (v == "1" || v == "true"); }
	bool set(const std::string& k, const std::string& v) { std::lock_guard<std::mutex> l(m); if (k == "global.retroachievements.token") tokenWrites.push_back(v); kv[k] = v; return true; }
	void saveSystemConf() {}
	void page(const std::string& k, const std::string& v) { std::lock_guard<std::mutex> l(m); kv[k] = v; }   // the settings page's own write
};

struct Window
{
	std::mutex m;
	std::vector<std::function<void()>> q;
	void postToUiThread(const std::function<void()>& f) { std::lock_guard<std::mutex> l(m); q.push_back(f); }
	size_t pending() { std::lock_guard<std::mutex> l(m); return q.size(); }
	void drain() { std::vector<std::function<void()>> t; { std::lock_guard<std::mutex> l(m); t.swap(q); } for (auto& f : t) f(); }
};
static Window gWin;

static struct Latch
{
	std::mutex m;
	std::condition_variable cv;
	bool held = false;
	int entered = 0, inside = 0, timeoutMs = 0;
} gLatch;

namespace RetroAchievements
{
	bool testAccount(const std::string& username, const std::string& password, std::string& tokenOrError, bool* refused = nullptr)
	{
		if (refused != nullptr)
			*refused = false;
		std::unique_lock<std::mutex> l(gLatch.m);
		gLatch.entered++;
		gLatch.inside++;
		gLatch.cv.notify_all();
		if (gLatch.timeoutMs > 0)
			gLatch.cv.wait_for(l, std::chrono::milliseconds(gLatch.timeoutMs), [] { return !gLatch.held; });
		else
			gLatch.cv.wait(l, [] { return !gLatch.held; });
		gLatch.held = false;   // the 2 s latch lets go by itself
		gLatch.inside--;
		gLatch.cv.notify_all();
		tokenOrError = "tok-" + username;
		return true;
	}
}

class WatchersManager;
class IWatcher
{
	friend class WatchersManager;
protected:
	virtual bool enabled() = 0;
	virtual int  updateTime() = 0;
	virtual bool check() = 0;
	virtual int  initialUpdateTime() { return 5 * 1000; }
};

// The pin's shape (WatchersManager.cpp:92-100, :181-199), one component.
class WatchersManager
{
public:
	static std::mutex mWatchersLock;
	static long sNow;
	static IWatcher* sItem;
	static long sNext;
	static WatchersManager* getInstance() { static WatchersManager m; return &m; }
	static void RegisterComponent(IWatcher* w) { std::unique_lock<std::mutex> l(mWatchersLock); sItem = w; sNext = sNow + w->initialUpdateTime(); }
	static void ResetComponent(IWatcher* w) { std::unique_lock<std::mutex> l(mWatchersLock); if (sItem == w) sNext = sNow; }
	static void pass(const std::function<void(IWatcher*)>& notify)
	{
		std::unique_lock<std::mutex> l(mWatchersLock);
		long now = sNow;
		if (sItem == nullptr || !sItem->enabled() || now < sNext)
			return;
		if (sItem->check())
			notify(sItem);
		sNext = now + sItem->updateTime();
	}
};
std::mutex WatchersManager::mWatchersLock;
long WatchersManager::sNow = 0;
IWatcher* WatchersManager::sItem = nullptr;
long WatchersManager::sNext = 0;

''' + klass + "\n\n" + "\n\n".join(members) + "\n\n" + dropped + r'''

struct NT
{
	CheckCheevosTokenComponent& mCheckCheevosTokenComponent;
	Window* mWindow;
	void OnWatcherChanged(IWatcher* component)
	{
''' + branch + r'''
	}
};

static CheckCheevosTokenComponent gComp[5];
static int gFails = 0;

template <class P> static bool waitFor(P p, int ms)
{
	for (int i = 0; i < ms; i++) { if (p()) return true; std::this_thread::sleep_for(std::chrono::milliseconds(1)); }
	return p();
}
static int inside() { std::lock_guard<std::mutex> l(gLatch.m); return gLatch.inside; }
static int entered() { std::lock_guard<std::mutex> l(gLatch.m); return gLatch.entered; }
static bool held() { std::lock_guard<std::mutex> l(gLatch.m); return gLatch.held; }
static void release() { std::lock_guard<std::mutex> l(gLatch.m); gLatch.held = false; gLatch.cv.notify_all(); }
static bool logged(const char* what) { std::lock_guard<std::mutex> l(gLogLock); for (auto& s : gLog) if (s.find(what) != std::string::npos) return true; return false; }

static CheckCheevosTokenComponent* setup(int i, const std::string& user, bool hold, int timeoutMs = 0)
{
	SystemConf* c = SystemConf::getInstance();
	{ std::lock_guard<std::mutex> l(c->m); c->kv.clear(); c->tokenWrites.clear(); }
	c->page("global.retroachievements", "1");
	c->page("global.retroachievements.username", user);
	c->page("global.retroachievements.password", "pw");
	{ std::lock_guard<std::mutex> l(gLatch.m); gLatch.held = hold; gLatch.entered = 0; gLatch.timeoutMs = timeoutMs; }
	{ std::lock_guard<std::mutex> l(gLogLock); gLog.clear(); }
	WatchersManager::sNow = 0;
	WatchersManager::RegisterComponent(&gComp[i]);
	WatchersManager::sNow = 1000;   // the first check is due (its initial 100 ms has passed)
	return &gComp[i];
}

// Passes of the watcher, a second of its clock each, the interface thread
// draining between them unless the loop has ended.
static void advance(NT& nt, int passes, bool drain = true)
{
	for (int k = 0; k < passes; k++)
	{
		waitFor([] { return inside() == 0; }, 200);
		std::this_thread::sleep_for(std::chrono::milliseconds(5));
		WatchersManager::pass([&](IWatcher* w) { nt.OnWatcherChanged(w); });
		WatchersManager::sNow += 1000;
		if (drain)
			gWin.drain();
	}
}

static std::string writes()
{
	SystemConf* c = SystemConf::getInstance();
	std::lock_guard<std::mutex> l(c->m);
	std::string s;
	for (auto& w : c->tokenWrites) s += (s.empty() ? "" : ",") + (w.empty() ? std::string("\"\"") : w);
	return s.empty() ? "none" : s;
}

static void verdict(const char* name, bool pass, const std::string& what)
{
	printf("%s %s: %s\n", pass ? "PASS" : "FAIL", name, what.c_str());
	if (!pass) gFails++;
}

int main(int argc, char** argv)
{
	setvbuf(stdout, nullptr, _IONBF, 0);
	SystemConf* conf = SystemConf::getInstance();
	for (int a = 1; a < argc; a++)
	{
		std::string c = argv[a];
		if (c == "switchoff" || c == "account" || c == "sameacct")
		{
			int i = c == "switchoff" ? 0 : c == "account" ? 1 : 2;
			std::string user = c == "switchoff" ? "alice" : c == "account" ? "bob" : "erin";
			CheckCheevosTokenComponent* comp = setup(i, user, true);
			NT nt { *comp, &gWin };
			std::thread watcher([&] { WatchersManager::pass([&](IWatcher* w) { nt.OnWatcherChanged(w); }); });
			bool in = waitFor([] { return entered() > 0; }, 2000);
			if (c == "switchoff")
			{
				conf->page("global.retroachievements", "0");          // GuiRetroAchievementsSettings.cpp:795-796
				conf->page("global.retroachievements.token", "");
			}
			else if (c == "account")
				conf->page("global.retroachievements.username", "carol");
			else
			{
				conf->page("global.retroachievements", "0");
				conf->page("global.retroachievements.token", "");
				conf->page("global.retroachievements", "1");
			}
			release();
			watcher.join();
			gWin.drain();
			advance(nt, 6);
			std::string w = writes(), now = conf->get("global.retroachievements.token");
			char line[512];
			snprintf(line, sizeof line, "sign-in entered %s; token writes after the page's change: %s; stored token \"%s\"", in ? "yes" : "NO", w.c_str(), now.c_str());
			if (c == "switchoff")
				verdict("switchoff (i) PL-23", in && w == "none" && now.empty(), line);
			else if (c == "account")
				verdict("account (ii) PL-23", in && w.find("tok-bob") == std::string::npos && logged("dropped"), std::string(line) + (logged("dropped") ? "; the drop logged" : "; no drop logged"));
			else
				verdict("sameacct ruling 5", in && w == "tok-erin" && now == "tok-erin", std::string(line) + " (a fresh check writes tok-erin)");
		}
		else if (c == "reset")
		{
			CheckCheevosTokenComponent* comp = setup(3, "dave", true, 2000);
			NT nt { *comp, &gWin };
			std::thread watcher([&] { WatchersManager::pass([&](IWatcher* w) { nt.OnWatcherChanged(w); }); });
			bool in = waitFor([] { return entered() > 0; }, 2000);
			auto t0 = std::chrono::steady_clock::now();
			WatchersManager::ResetComponent(comp);   // the page's close (NetworkThread.cpp:21-25), from another thread
			long ms = (long)std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - t0).count();
			bool still = held();
			release();
			watcher.join();
			gWin.drain();
			advance(nt, 3);
			char line[256];
			snprintf(line, sizeof line, "sign-in entered %s; ResetComponent waited %ld ms; the latch %s when it returned", in ? "yes" : "NO", ms, still ? "still held" : "already let go");
			verdict("reset (iii) PL-14", in && ms < 50 && still, line);
		}
		else if (c == "closing")
		{
			CheckCheevosTokenComponent* comp = setup(4, "frank", false);
			NT nt { *comp, &gWin };
			AppWindow::closing();   // main.cpp:1322: the loop has ended
			advance(nt, 4, false);
			size_t queued = gWin.pending();
			char line[256];
			snprintf(line, sizeof line, "after closing(): %zu task(s) queued that no loop will run; the drop %s", queued, logged("closing") ? "logged" : "not logged");
			verdict("closing (iv) EP-7", queued == 0 && logged("closing"), line);
		}
	}
	waitFor([] { return inside() == 0; }, 2000);
	if (gFails)
		printf("FAIL S4a: %d case(s)\n", gFails);
	return gFails ? 1 : 0;
}
'''
flags = ("-fsanitize=thread",) if tsan else ("-fsanitize=address,undefined",)
run(harness, "s4a", flags, args=tuple(cases))
