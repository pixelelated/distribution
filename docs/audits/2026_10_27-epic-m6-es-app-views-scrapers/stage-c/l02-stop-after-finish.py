"""L-02, L-23, EP-34, EP-37 (#679; #1258, PL-01 and PL-14): the batch scrape's lifetime.

    python3 -I l02-stop-after-finish.py <ThreadedScraper.cpp> [--control] [--plain] [--case NAME]

ThreadedScraper's `Process`, `run`, `stop`, `start` and destructor are extracted
as written (and `isRunning` and `reapFinished` when the file defines them; at
the pin `isRunning` is the header's inline `mInstance != nullptr`), over a fake
class holding the members they use and a doubled ScraperThread that finishes
its game at once (ASYNC_DONE). The page is T31's GuiScraperRun:140-141: a
progress with `cancelled` reads SKIPPED - YOU CANCELLED IT, whatever was
scraped. Four cases, each its own process (a sanitizer stops at its first
report):

- **cancel** (L-01, L-02): the LOG(LogInfo) inside run()'s finishing block,
  which runs with sProgressMutex held after `finished = true`, starts the
  player's stop() on a second thread and waits 50 ms, so stop() is past its
  read of mInstance and blocked on the mutex. The window is widened by that
  hook, and this is the synthetic input (vm-first.md); the seat showed the
  order needs no hook (EP-6). A stop() after `finished` must leave `cancelled`
  false and must not write through a freed instance. At the pin: a
  heap-use-after-free in stop(); under --plain, cancelled 1 over finished 1.
- **leak** (L-23, PL-14): a run of two games, then the reap the interface
  thread does (stop() at exit). LeakSanitizer must report nothing. At the pin
  run() erases each ScraperThread without a delete, and `mHandle` (a
  `new std::thread`) is never freed.
- **publish** (EP-34): the worker's whole run completes before the creator
  stores the thread it made. The hook is named: the extract's
  `<x> = new std::thread(...)` / `<x> = std::thread(...)` is rewritten to make
  the thread, wait until the run has finished, then store it -- the same
  statements in the same order, with the wait between. At the pin the store
  writes into the instance the worker has deleted.
- **startup** (EP-37): `Process()` throws after it published `running` (the
  first hand-out's search, as `generateRequests`' INVALID CREDENTIALS does).
  start()'s catch must leave a snapshot the page can end on (`finished`). At
  the pin: running 1, finished 0.

The fake class carries both shapes' members (D-WORKFLOW-211: completed for the
fixed shape, an owned `std::thread mWorker` and an atomic `mExitCode` beside
the pin's `mHandle`), and its asserted lines are unchanged. --control runs
the pin's file with stop() taking the mutex first and run() clearing
mInstance under it (stage C's control); against a file without those lines
it is CANNOT, not a stub failure. --plain builds without the sanitizers.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function  # noqa: E402

args = sys.argv[1:]
src = Path(args[0]).read_text()
control, plain = "--control" in args, "--plain" in args
only = args[args.index("--case") + 1] if "--case" in args else None


def maybe(head):
    return function(src, head, "L-02") if re.search(head, src, re.M) else ""


rn = function(src, r"^void ThreadedScraper::run\(\)", "L-02")
st = function(src, r"^void ThreadedScraper::stop\(\)", "L-02")
dt = function(src, r"^ThreadedScraper::~ThreadedScraper\(\)", "L-02")
pr = function(src, r"^void ThreadedScraper::Process\(\)", "L-02")
sa = function(src, r"^void ThreadedScraper::start\(Window\* window, const std::queue<ScraperSearchParams>& searches\)", "L-02")
ir = maybe(r"^bool ThreadedScraper::isRunning\(\)")
rf = maybe(r"^void ThreadedScraper::reapFinished\(\)")
if control:
    a = "\tdelete this;\n\tThreadedScraper::mInstance = nullptr;"
    if a not in rn:
        print("CANNOT l02 --control: run() has no `delete this` to rewrite (the control is the pin's)")
        sys.exit(2)
    st = """void ThreadedScraper::stop()
{
	std::unique_lock<std::mutex> lock(sProgressMutex);
	auto thread = ThreadedScraper::mInstance;
	if (thread == nullptr || sProgress.finished)
		return;
	sProgress.cancelled = true;
	thread->mExitCode = ASYNC_DONE;
}"""
    rn = rn.replace(a, "\t{ std::unique_lock<std::mutex> lock(sProgressMutex); ThreadedScraper::mInstance = nullptr; }\n\tdelete this;")
    b = "\tThreadedScraper::mInstance = nullptr;\n}"
    assert dt.endswith(b)
    dt = dt[: -len(b)] + "}"
# EP-34's named hook: the thread is made, the run is let finish, then the store.
m = re.search(r"\t(\w+) = (new )?std::thread\(([^;]*)\);", pr)
assert m, "Process() makes no std::thread"
if m.group(2):
    pr = pr.replace(m.group(0), "\t{ auto* t32h = new std::thread(%s); hookPublish(); %s = t32h; }" % (m.group(3), m.group(1)))
else:
    pr = pr.replace(m.group(0), "\t{ std::thread t32h(%s); hookPublish(); %s = std::move(t32h); }" % (m.group(3), m.group(1)))
ir = ir or "bool ThreadedScraper::isRunning() { return mInstance != nullptr; }"

harness = r'''
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstring>
#include <memory>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
enum AsyncHandleStatus { ASYNC_IN_PROGRESS, ASYNC_ERROR, ASYNC_DONE };
#define _(x) std::string(x)
static void hook();
static bool gHookArmed = false;
struct Log { Log(int lvl) { if (lvl == 1 && gHookArmed) { gHookArmed = false; hook(); } }
    template<typename T> Log& operator<<(const T&) { return *this; } };
enum { LogDebug = 0, LogInfo = 1, LogError = 2, LogWarning = 3 };
#define LOG(x) Log(x)
struct ScraperSearchParams { int n = 0; };
static bool gThrowOnHandout = false;
struct ScraperThread { int mThreadId; ScraperThread(int i) : mThreadId(i) {}
    int updateState() { return ASYNC_DONE; } int getError() { return 0; } std::string getErrorString() { return ""; } };
struct Window { template<class T> void pushGui(T* g) { delete g; } };   // the window owns what is pushed
struct GuiMsgBox { GuiMsgBox(Window*, const std::string&) {} };
struct FakeScraper { int getThreadCount(std::string&) { return 1; } };
struct Scraper { static FakeScraper* getScraper() { static FakeScraper s; return &s; } };
struct ThreadedScraper {
    struct Progress { bool running = false; int done = 0, total = 0; std::string game; int errors = 0;
        bool finished = false, cancelled = false, failed = false; std::string failure; int elapsedMs = 0; };
    static ThreadedScraper* mInstance; static std::atomic<bool> mPaused; static std::mutex sProgressMutex; static Progress sProgress;
    static std::chrono::steady_clock::time_point sStarted;
    Window* mWindow; std::string mCurrentGame; std::vector<std::string> mErrors;
    std::thread* mHandle = nullptr;   // the pin's
    std::thread mWorker;              // the fixed shape's (D-WORKFLOW-211)
    std::queue<ScraperSearchParams> mSearchQueue; std::vector<ScraperThread*> mScraperThreads;
    int mTotal, mThreadCount; std::atomic<int> mExitCode{ASYNC_IN_PROGRESS};
    ThreadedScraper(Window* w, const std::queue<ScraperSearchParams>& s, int threadCount)
        : mWindow(w), mSearchQueue(s), mTotal((int) s.size()), mThreadCount(threadCount) {}
    ~ThreadedScraper();
    void Process(); void run();
    static void start(Window* window, const std::queue<ScraperSearchParams>& searches);
    static void stop(); static bool isRunning(); static void reapFinished();
    void ProcessNextGame(ScraperThread*) {
        if (gThrowOnHandout) throw std::runtime_error("INVALID CREDENTIALS");
        mSearchQueue.pop(); }
    void acceptResult(ScraperThread&) {} void processError(int, const std::string) {} void updateUI() {}
};
ThreadedScraper* ThreadedScraper::mInstance = nullptr; std::atomic<bool> ThreadedScraper::mPaused{false};
std::mutex ThreadedScraper::sProgressMutex; ThreadedScraper::Progress ThreadedScraper::sProgress;
std::chrono::steady_clock::time_point ThreadedScraper::sStarted;
static std::atomic<bool> gPublishHook{false};
static void hookPublish() {
    if (!gPublishHook) return;
    for (int i = 0; i < 400; i++) {   // up to 2 s for the run to finish before the store
        { std::unique_lock<std::mutex> l(ThreadedScraper::sProgressMutex); if (ThreadedScraper::sProgress.finished) break; }
        std::this_thread::sleep_for(std::chrono::milliseconds(5)); }
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
}
''' + "\n".join(x for x in (dt, pr, rn, st, sa, ir, rf) if x) + r'''
static std::thread gStop;
static void hook() {
    gStop = std::thread([] { ThreadedScraper::stop(); });
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
}
static std::queue<ScraperSearchParams> games(int n) { std::queue<ScraperSearchParams> q; for (int i = 0; i < n; i++) q.push({i}); return q; }
static Window gW;
static void waitFinished() {
    for (int i = 0; i < 400; i++) {
        { std::unique_lock<std::mutex> l(ThreadedScraper::sProgressMutex); if (ThreadedScraper::sProgress.finished) return; }
        std::this_thread::sleep_for(std::chrono::milliseconds(5)); } }
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    std::string c = argc > 1 ? argv[1] : "";
    if (c == "cancel") {
        gHookArmed = true;
        ThreadedScraper::start(&gW, games(1));
        waitFinished(); std::this_thread::sleep_for(std::chrono::milliseconds(100));
        if (gStop.joinable()) gStop.join();
        ThreadedScraper::stop();   // the reap the interface thread does at exit
        auto p = ThreadedScraper::sProgress;
        printf("cancel: finished %d, cancelled %d\n", p.finished, p.cancelled);
        if (p.cancelled) { printf("FAIL L-02: a stop() after the run finished marked it cancelled: the page reads SKIPPED - YOU CANCELLED IT\n"); return 1; }
    } else if (c == "leak") {
        ThreadedScraper::start(&gW, games(2));
        waitFinished(); std::this_thread::sleep_for(std::chrono::milliseconds(100));
        ThreadedScraper::stop();   // main.cpp:1332 at exit
        printf("leak: a two-game run started, finished and reaped (LeakSanitizer reads the rest)\n");
    } else if (c == "publish") {
        gPublishHook = true;
        ThreadedScraper::start(&gW, games(1));
        waitFinished(); std::this_thread::sleep_for(std::chrono::milliseconds(100));
        ThreadedScraper::stop();
        printf("publish: the worker's run finished before the creator stored its thread\n");
    } else if (c == "startup") {
        gThrowOnHandout = true;
        ThreadedScraper::start(&gW, games(1));
        auto p = ThreadedScraper::sProgress;
        printf("startup: running %d, finished %d, failed %d, isRunning %d\n", p.running, p.finished, p.failed, ThreadedScraper::isRunning());
        if (!p.finished) { printf("FAIL EP-37: a startup throw leaves the snapshot running and not finished: the page reads a run forever\n"); return 1; }
    }
    return 0;
}
'''
flags = [] if plain else ["-fsanitize=address,undefined"]
cases = [only] if only else ["cancel", "leak", "publish", "startup"]
worst = 0
with tempfile.TemporaryDirectory(prefix="l02-", dir="/workspace/tmp/m6-t32/tmp") as d:
    d = Path(d)
    (d / "a.cpp").write_text(harness)
    b = subprocess.run(["g++", "-std=c++17", "-O0", "-g", *flags, str(d / "a.cpp"), "-o", str(d / "a"), "-pthread"], capture_output=True, text=True)
    if b.returncode:
        print("FAIL l02: the extract does not compile\n%s" % b.stderr[-2500:])
        sys.exit(2)
    for c in cases:
        env = {"PATH": "/usr/bin:/bin", "ASAN_OPTIONS": "detect_leaks=1"}
        r = subprocess.run([str(d / "a"), c], capture_output=True, text=True, timeout=60, env=env)
        out = r.stdout.strip()
        print(out if out else "%s: (no line; the process stopped)" % c)
        for line in r.stderr.splitlines():
            if line.startswith(("WARNING: ", "SUMMARY: ")) or (" a.cpp:" in line and line.lstrip().startswith("#")):
                print("  " + line.replace(str(d) + "/", ""))
        if r.returncode and "FAIL" not in out:
            print("FAIL %s: rc %d (a sanitizer report or a signal)" % (c, r.returncode))
        print("  %s rc=%d" % (c, r.returncode))
        worst = worst or (1 if r.returncode else 0)
sys.exit(worst)
