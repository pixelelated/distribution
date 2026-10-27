"""S2 (#679; #1259 PL-02, #1261 PL-04, #1262 PL-05, #1267 PL-18): the registry,
the logo test, the run's count and outcome class, and the thread the first
searches run on.

    python3 -I s2-scrapers.py <Scraper.cpp> <ThreadedScraper.cpp>

Extracted as written: `Scraper::getScraper` and `Scraper::hasAnyMedia`
(Scraper.cpp); `ThreadedScraper`'s `Process`, `run`, `ProcessNextGame`,
`updateUI`, `processError`, `start`, `stop`, destructor, and `isRunning` and
`reapFinished` where the file defines them (ThreadedScraper.cpp). Doubles: a
registry of two scrapers, Settings, a FileData with a marquee, `exists`, and a
ScraperThread whose search records the thread it ran on and ends with the
case's status. Cases, each printed with its verdict:

- **registry** (PL-04): `getScraper()` with `Scraper` saved as a name the
  build does not register must return a scraper (the first registered), so
  ThreadedScraper.cpp:296 has something to call. At the pin: nullptr.
- **logo** (PL-18): a game whose only media is an existing marquee, the
  scraper offering Marquee: `hasAnyMedia` must be true with `ScrapperLogoSrc`
  set and false with it empty, as its sibling `:145` reads the setting. At
  the pin: false, then true.
- **count** (PL-02, 3.19): ten games on one thread, each found: the run must
  end with `done 10` and not failed. At the pin: `done 9`.
- **offline**, **busy** (PL-02, ruling 5): three games whose searches end in
  an IO error (code 3), or in a spent 429: the run must end `failed` with
  the class's why on the page's line 4 (YOU'RE NOT ONLINE. / THE SCRAPER IS
  BUSY RIGHT NOW.). At the pin: not failed, no why.
- **media**, **media404** (S2b, the coordinator's 18:24 UTC follow-up, D-UI-030):
  three games whose images failed after their data arrived (a rename or a
  resize, code 200; or a 404): COULDN'T FINISH with SOME IMAGES COULDN'T BE
  SAVED. on line 4. At S2's tip: errors 3, not failed, no why.
- **nomatch** (ruling 5): three games, no match (DONE, no result): COMPLETED
  -- not failed, errors 0. Right at the pin; kept.
- **thread** (PL-05): the first search must run on the worker, not on the
  thread that called start(). At the pin: the caller's thread.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

sc = Path(sys.argv[1]).read_text()
ts = Path(sys.argv[2]).read_text()


def maybe(src, head):
    return function(src, head, "S2") if re.search(head, src, re.M) else ""


gs = function(sc, r"^Scraper\* Scraper::getScraper\(const std::string name\)", "S2")
ha = function(sc, r"^bool Scraper::hasAnyMedia\(FileData\* file\)", "S2")
parts = [function(ts, h, "S2") for h in (
    r"^ThreadedScraper::~ThreadedScraper\(\)", r"^void ThreadedScraper::Process\(\)", r"^void ThreadedScraper::run\(\)",
    r"^void ThreadedScraper::ProcessNextGame\(ScraperThread\* thread\)", r"^void ThreadedScraper::updateUI\(\)",
    r"^void ThreadedScraper::processError\(int status, const std::string statusString\)", r"^void ThreadedScraper::stop\(\)",
    r"^void ThreadedScraper::start\(Window\* window, const std::queue<ScraperSearchParams>& searches\)")]
parts += [x for x in (maybe(ts, r"^bool ThreadedScraper::isRunning\(\)"), maybe(ts, r"^void ThreadedScraper::reapFinished\(\)")) if x]
if not re.search(r"^bool ThreadedScraper::isRunning\(\)", ts, re.M):
    parts.append("bool ThreadedScraper::isRunning() { return mInstance != nullptr; }")
harness = r'''
#include <atomic>
#include <chrono>
#include <cstdio>
#include <map>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>
#define _(x) std::string(x)
enum AsyncHandleStatus { ASYNC_IN_PROGRESS, ASYNC_ERROR, ASYNC_DONE };
struct NullLog { template<typename T> NullLog& operator<<(const T&) { return *this; } };
#define LOG(x) NullLog()
struct HttpReq { enum Status { REQ_IN_PROGRESS = 0, REQ_IO_ERROR = 3, REQ_FILESTREAM_ERROR = 4, REQ_SUCCESS = 200, REQ_400_BADREQUEST = 400,
    REQ_401_FORBIDDEN = 401, REQ_403_BADLOGIN = 403, REQ_404_NOTFOUND = 404, REQ_426_SERVERMAINTENANCE = 423, REQ_426_BLACKLISTED = 426,
    REQ_429_TOOMANYREQUESTS = 429, REQ_430_TOOMANYSCRAPS = 430, REQ_430_TOOMANYFAILURES = 431 }; };
struct Settings { std::map<std::string, std::string> s; std::map<std::string, bool> b;
    static Settings* getInstance() { static Settings x; return &x; }
    std::string getString(const std::string& k) { return s[k]; } bool getBool(const std::string& k) { return b[k]; } };
enum class MetaDataId { Image, Thumbnail, Marquee, Manual, Map, FanArt, Video, BoxBack, Cartridge, Magazine, TitleShot, Bezel, Wheel, Mix, Box3d, BoxArt };
struct FileData { std::map<MetaDataId, std::string> md; std::string getMetadata(MetaDataId id) { return md[id]; } };
namespace Utils { namespace FileSystem { bool exists(const std::string& p, bool = true) { return !p.empty(); } } }
struct Scraper {
    enum class ScraperMediaSource { Screenshot = 1, Video, Marquee, Box2d, Box3d, FanArt, TitleShot, Cartridge, Map, Manual, Wheel, Mix, BoxBack, Magazine, PadToKey, Ratings, Bezel_16_9, ShortTitle, Region };
    std::vector<ScraperMediaSource> supported;
    bool isMediaSupported(const ScraperMediaSource& m) { for (auto x : supported) if (x == m) return true; return false; }
    static std::vector<std::pair<std::string, Scraper*>> scrapers;
    static Scraper* getScraper(const std::string name = "");
    bool hasAnyMedia(FileData* file);
    int getThreadCount(std::string&) { return 1; }
};
typedef Scraper::ScraperMediaSource ScraperMediaSource;
std::vector<std::pair<std::string, Scraper*>> Scraper::scrapers;
''' + gs + "\n" + ha + r'''
struct ScraperSearchParams { int n = 0; std::string getGameName() const { return "game" + std::to_string(n); } };
static std::thread::id gSearchThread; static std::atomic<int> gSearches{0};
static int gCaseStatus = ASYNC_DONE, gCaseCode = 0; static bool gCaseMatch = true, gCaseMedia = false;
struct ScraperThread { int mThreadId; int mStatus = ASYNC_IN_PROGRESS;
    ScraperThread(int i) : mThreadId(i) {}
    void run(const ScraperSearchParams&) { if (gSearches++ == 0) gSearchThread = std::this_thread::get_id(); mStatus = gCaseStatus; }
    int updateState() { return mStatus; } int getError() { return gCaseCode; } std::string getErrorString() { return "the scraper's words"; }
    bool isMediaError() { return gCaseMedia; } };   // S2b's (#1259; D-WORKFLOW-211)
struct Window { template<class T> void pushGui(T* g) { delete g; } };
struct GuiMsgBox { GuiMsgBox(Window*, const std::string&) {} };
struct ThreadedScraper {
    struct Progress { bool running = false; int done = 0, total = 0; std::string game; int errors = 0;
        bool finished = false, cancelled = false, failed = false; std::string failure; int elapsedMs = 0; };
    static ThreadedScraper* mInstance; static std::atomic<bool> mPaused; static std::mutex sProgressMutex; static Progress sProgress;
    static std::chrono::steady_clock::time_point sStarted;
    Window* mWindow; std::string mCurrentGame; std::vector<std::string> mErrors;
    std::thread* mHandle = nullptr; std::thread mWorker;
    std::queue<ScraperSearchParams> mSearchQueue; std::vector<ScraperThread*> mScraperThreads;
    int mTotal, mThreadCount; std::atomic<int> mExitCode{ASYNC_IN_PROGRESS};
    int mOfflineErrors = 0, mBusyErrors = 0, mMediaErrors = 0;
    ThreadedScraper(Window* w, const std::queue<ScraperSearchParams>& s, int threadCount)
        : mWindow(w), mSearchQueue(s), mTotal((int) s.size()), mThreadCount(threadCount) {}
    ~ThreadedScraper();
    void Process(); void run(); void ProcessNextGame(ScraperThread* thread); void updateUI();
    void processError(int status, const std::string statusString);
    void acceptResult(ScraperThread&) {}
    static void start(Window* window, const std::queue<ScraperSearchParams>& searches);
    static void stop(); static bool isRunning(); static void reapFinished();
};
ThreadedScraper* ThreadedScraper::mInstance = nullptr; std::atomic<bool> ThreadedScraper::mPaused{false};
std::mutex ThreadedScraper::sProgressMutex; ThreadedScraper::Progress ThreadedScraper::sProgress;
std::chrono::steady_clock::time_point ThreadedScraper::sStarted;
''' + "\n".join(parts) + r'''
static Window gW;
static ThreadedScraper::Progress runGames(int n, int status, int code, bool media = false) {
    gCaseStatus = status; gCaseCode = code; gCaseMedia = media; gSearches = 0;
    std::queue<ScraperSearchParams> q; for (int i = 0; i < n; i++) q.push({i});
    ThreadedScraper::start(&gW, q);
    for (int i = 0; i < 400; i++) {
        { std::unique_lock<std::mutex> l(ThreadedScraper::sProgressMutex); if (ThreadedScraper::sProgress.finished) break; }
        std::this_thread::sleep_for(std::chrono::milliseconds(5)); }
    std::this_thread::sleep_for(std::chrono::milliseconds(30));
    ThreadedScraper::Progress p; { std::unique_lock<std::mutex> l(ThreadedScraper::sProgressMutex); p = ThreadedScraper::sProgress; }
    ThreadedScraper::stop();
    return p;
}
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    Scraper a, b; Scraper::scrapers = {{"ScreenScraper", &a}, {"IGDB", &b}};
    Settings::getInstance()->s["Scraper"] = "TheGamesDB";
    Scraper* g = Scraper::getScraper();
    printf("registry: Scraper=TheGamesDB (not registered) -> %s\n", g == &a ? "ScreenScraper (the first registered)" : g ? "another" : "nullptr");
    if (g != &a) bad++;
    Scraper m; m.supported = {ScraperMediaSource::Marquee}; FileData f; f.md[MetaDataId::Marquee] = "/roms/gb/images/x-marquee.png";
    Settings::getInstance()->s["ScrapperLogoSrc"] = "wheel"; bool set = m.hasAnyMedia(&f);
    Settings::getInstance()->s["ScrapperLogoSrc"] = ""; bool off = m.hasAnyMedia(&f);
    printf("logo: a present marquee, ScrapperLogoSrc set -> %d, empty -> %d\n", set, off);
    if (!set || off) bad++;
    auto p = runGames(10, ASYNC_DONE, 0);
    printf("count: ten games found on one thread -> done %d of %d, failed %d\n", p.done, p.total, p.failed);
    if (p.done != 10 || p.failed) bad++;
    std::thread::id me = std::this_thread::get_id();
    printf("thread: the first search ran on %s\n", gSearchThread == me ? "the caller's thread (the interface thread)" : "the worker");
    if (gSearchThread == me) bad++;
    p = runGames(3, ASYNC_ERROR, 3);
    printf("offline: three IO errors -> failed %d, errors %d, why '%s'\n", p.failed, p.errors, p.failure.c_str());
    if (!p.failed || p.failure != "YOU'RE NOT ONLINE.") bad++;
    p = runGames(3, ASYNC_ERROR, 429);
    printf("busy: three spent 429s -> failed %d, errors %d, why '%s'\n", p.failed, p.errors, p.failure.c_str());
    if (!p.failed || p.failure != "THE SCRAPER IS BUSY RIGHT NOW.") bad++;
    p = runGames(3, ASYNC_ERROR, 200, true);
    printf("media: three games whose images failed (rename, resize) -> failed %d, errors %d, why '%s'\n", p.failed, p.errors, p.failure.c_str());
    if (!p.failed || p.failure != "SOME IMAGES COULDN'T BE SAVED.") bad++;
    p = runGames(3, ASYNC_ERROR, 404, true);
    printf("media404: three games whose images were not found -> failed %d, why '%s'\n", p.failed, p.failure.c_str());
    if (!p.failed || p.failure != "SOME IMAGES COULDN'T BE SAVED.") bad++;
    p = runGames(3, ASYNC_DONE, 0);
    printf("nomatch: three games, each answered -> failed %d, errors %d\n", p.failed, p.errors);
    if (p.failed || p.errors) bad++;
    if (bad) { printf("FAIL S2: %d case(s)\n", bad); return 1; }
    return 0;
}
'''
run(harness, "s2", ("-fsanitize=address,undefined",))
