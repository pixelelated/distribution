"""L-02 (#679, T31's inherited L-02): a CANCEL that lands as the run finishes marks
a completed run cancelled, and writes through a pointer the run may have freed.

    python3 -I l02-stop-after-finish.py <ThreadedScraper.cpp> [--control]

ThreadedScraper::run, ::stop and the destructor are extracted as written, over
a fake class holding the members they use and one doubled ScraperThread that
finishes its game at once (ASYNC_DONE, empty queue). The page is T31's
GuiScraperRun:140-141: a progress with `cancelled` reads SKIPPED - YOU
CANCELLED IT, whatever was scraped.
The window is widened, and this is the synthetic input (vm-first.md): the
LOG(LogInfo) inside run()'s finishing block, which runs with sProgressMutex
held after `finished = true`, starts the player's stop() on a second thread
and waits 50 ms, so stop() has read mInstance and is blocked on the mutex.
On the device the same order needs a YES pressed in the frame the last game
ends; the code permits it, the timing is the harness's.
- A stop() after `finished` must leave `cancelled` false: the run completed.
  At the pin it sets it -- FAIL.
- stop() must not write through mInstance after run() has done `delete this`.
  At the pin the write at :333 races the delete at :238; ASan reports it when
  the delete wins.
--plain builds without the sanitizers, so the write after the free goes
unreported and the flag it set can be printed.
--control: stop() takes the mutex first, returns when `finished` is set, and
reads mInstance under it (run() would clear it under the same lock).
Noticed while writing it (L-23): run() erases each finished ScraperThread from
mScraperThreads without deleting it (:218, 717e7d8c3, upstream), so the
destructor's delete loop finds none, and mHandle (the std::thread, :53) is
never joined or freed: every run leaks its threads' objects.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
rn = function(src, r"^void ThreadedScraper::run\(\)", "L-02")
st = function(src, r"^void ThreadedScraper::stop\(\)", "L-02")
dt = function(src, r"^ThreadedScraper::~ThreadedScraper\(\)", "L-02")
if "--control" in sys.argv:
    st = """void ThreadedScraper::stop()
{
	std::unique_lock<std::mutex> lock(sProgressMutex);
	auto thread = ThreadedScraper::mInstance;
	if (thread == nullptr || sProgress.finished)
		return;
	sProgress.cancelled = true;
	thread->mExitCode = ASYNC_DONE;
}"""
    a = "\tdelete this;\n\tThreadedScraper::mInstance = nullptr;"
    assert a in rn
    rn = rn.replace(a, "\t{ std::unique_lock<std::mutex> lock(sProgressMutex); ThreadedScraper::mInstance = nullptr; }\n\tdelete this;")
    a = "\tThreadedScraper::mInstance = nullptr;\n}"
    assert dt.endswith(a)
    dt = dt[: -len(a)] + "}"
harness = r'''
#include <atomic>
#include <chrono>
#include <cstdio>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <vector>
enum AsyncHandleStatus { ASYNC_IN_PROGRESS, ASYNC_ERROR, ASYNC_DONE };
static void hook();
static bool gHookArmed = false;
struct Log { Log(int lvl) { if (lvl == 1 && gHookArmed) { gHookArmed = false; hook(); } }
    template<typename T> Log& operator<<(const T&) { return *this; } };
enum { LogDebug = 0, LogInfo = 1 };
#define LOG(x) Log(x)
struct ScraperThread { int updateState() { return ASYNC_DONE; } int getError() { return 0; } std::string getErrorString() { return ""; } };
struct ThreadedScraper {
    struct Progress { bool running = false, finished = false, cancelled = false, failed = false; int done = 0, total = 0, errors = 0; int elapsedMs = 0; };
    static ThreadedScraper* mInstance; static bool mPaused; static std::mutex sProgressMutex; static Progress sProgress;
    static std::chrono::steady_clock::time_point sStarted;
    volatile int mExitCode = ASYNC_IN_PROGRESS;
    std::vector<ScraperThread*> mScraperThreads; std::queue<int> mSearchQueue;
    ~ThreadedScraper();
    void run(); static void stop();
    void acceptResult(ScraperThread&) {} void processError(int, const std::string) {} void ProcessNextGame(ScraperThread*) {}
};
ThreadedScraper* ThreadedScraper::mInstance = nullptr; bool ThreadedScraper::mPaused = false;
std::mutex ThreadedScraper::sProgressMutex; ThreadedScraper::Progress ThreadedScraper::sProgress;
std::chrono::steady_clock::time_point ThreadedScraper::sStarted;
''' + dt + "\n" + rn + "\n" + st + r'''
static std::thread gStop;
static void hook() {
    gStop = std::thread([] { ThreadedScraper::stop(); });
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
}
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    static ScraperThread one; // static: run() erases it from the vector without a delete (:218), L-23
    auto t = new ThreadedScraper(); t->mScraperThreads.push_back(&one);
    ThreadedScraper::mInstance = t; gHookArmed = true;
    t->run();
    gStop.join();
    auto p = ThreadedScraper::sProgress;
    printf("finished %d, cancelled %d\n", p.finished, p.cancelled);
    if (p.cancelled) { printf("FAIL L-02: a stop() after the run finished marked it cancelled: the page reads SKIPPED - YOU CANCELLED IT\n"); return 1; }
    return 0;
}
'''
run(harness, "l02", () if "--plain" in sys.argv else ("-fsanitize=address,undefined",))
