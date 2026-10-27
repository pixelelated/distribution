"""S6 (#679; #1268 PL-21, #1269 PL-22): the local API's /isIdle and POST /launch.

    python3 -I s6-api.py <HttpServerThread.cpp>

- **isidle** (PL-21): the predicate `/isIdle` answers, extracted as written --
  the route's `bool idle = ...;`, or, when that is a call, the called
  function's returned expression -- over doubles for each source it asks.
  It must be false while a cloud sync runs, while
  `/var/run/cloud_sync.lock` is held by another process, and while the
  proxy's send or top-up runs, and true with none of them. At the pin it
  is true in each of those (it asks none of them).
- **launch** (PL-22): the `/launch` route's body, extracted as written into a
  fake server, over doubles for the systems, the files, the window's
  `postToUiThread` (which records the work) and `ViewController::launch`
  (which reads the file it is given). Two systems carry one path; the route
  runs; then the library is rebuilt (every FileData deleted and made again)
  before the posted work runs, as a reload between the request and the
  interface thread's turn. One launch must be posted, and it must reach the
  rebuilt file. At the pin, under ASan: two posts, each holding a raw
  FileData* the rebuild freed -- a heap-use-after-free.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t32extract import function, run  # noqa: E402

src = Path(sys.argv[1]).read_text()
m = re.search(r'mHttpServer->Get\("/isIdle".*?bool idle\s*=\s*(.*?);', src, re.S)
assert m, "/isIdle's predicate not found"
expr = m.group(1).strip()
c = re.match(r"^(\w+)\(\)$", expr)
if c:
    body = function(src, r"^static bool %s\(\)" % c.group(1), "S6")
    r = re.search(r"return\s+(.*?);\s*\}\s*$", body, re.S)
    assert r, "the called predicate returns no expression"
    expr = r.group(1).strip()
route = function(src, r'^\tmHttpServer->Post\("/launch", \[this\]\(const httplib::Request& req, httplib::Response& res\)', "S6")
route_body = route[route.index("{"):]
harness = r'''
#include <cstdio>
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <vector>
struct Src { bool game = false, scraper = false, installer = false, hasher = false, updater = false, sync = false, lock = false, send = false, topup = false; } gS;
namespace HttpApi { std::string getRunnningGameInfo() { return gS.game ? "{}" : ""; } }
namespace ThreadedScraper { bool isRunning() { return gS.scraper; } }
namespace ContentInstaller { bool isRunning() { return gS.installer; } }
namespace ThreadedHasher { bool isRunning() { return gS.hasher; } }
enum class GuiUpdateState { NOTHING, UPDATER_RUNNING };
namespace GuiUpdate { GuiUpdateState state = GuiUpdateState::NOTHING; }
namespace ThreadedCloudSync { bool isRunning() { return gS.sync; } }
namespace ProxyCards { bool sendRunning() { return gS.send; } bool topUpRunning() { return gS.topup; } }
namespace Utils { namespace AtomicFile { bool isFlockHeld(const std::string& p) { return p == "/var/run/cloud_sync.lock" && gS.lock; } }
                  namespace FileSystem { std::string getAbsolutePath(const std::string& p) { return p; } } }
static bool pred() { GuiUpdate::state = gS.updater ? GuiUpdateState::UPDATER_RUNNING : GuiUpdateState::NOTHING;
    return ''' + expr + r'''; }
// The launch route's doubles.
enum FileType { GAME = 1 };
struct FileData { std::string path; FileData(const std::string& p) : path(p) {} std::string getFullPath() { return path; } std::string getPath() { return path; } };
struct FolderData { std::vector<FileData*> files; std::vector<FileData*> getFilesRecursive(int) { return files; } };
struct SystemData { FolderData root; FolderData* getRootFolder() { return &root; } bool isCollection() { return false; } bool isGameSystem() { return true; }
    static std::vector<SystemData*> sSystemVector; };
std::vector<SystemData*> SystemData::sSystemVector;
static std::vector<std::function<void()>> gPosted; static int gLaunches = 0; static std::string gLaunched;
struct Window { void postToUiThread(const std::function<void()>& f) { gPosted.push_back(f); } void cancelScreenSaver() {} };
struct ViewController { static ViewController* get() { static ViewController v; return &v; } void launch(FileData* f) { gLaunches++; gLaunched = f->getPath(); } };
namespace httplib { struct Request { std::string body; std::string remote_addr = "127.0.0.1"; }; struct Response { int status = 200; std::string body;
    void set_content(const std::string& b, const char*) { body = b; } }; }
static bool isAllowed(const httplib::Request&, httplib::Response&) { return true; }
struct Server { Window* mWindow; void launchRoute(const httplib::Request& req, httplib::Response& res)
''' + route_body + r'''
};
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    int bad = 0;
    struct C { const char* what; Src s; bool want; } cases[] = {
        {"nothing running", {}, true},
        {"a cloud sync running", {false, false, false, false, false, true, false, false, false}, false},
        {"the cloud lock held by a script", {false, false, false, false, false, false, true, false, false}, false},
        {"the proxy's send running", {false, false, false, false, false, false, false, true, false}, false},
        {"the proxy's top-up running", {false, false, false, false, false, false, false, false, true}, false},
        {"a scrape running", {false, true}, false},
    };
    for (auto& c : cases) {
        gS = c.s; bool got = pred();
        printf("isidle: %-34s -> %s%s\n", c.what, got ? "[ true ]" : "[ false ]", got == c.want ? "" : "   (want the other)");
        if (got != c.want) bad++;
    }
    SystemData a, b; SystemData::sSystemVector = {&a, &b};
    a.root.files = {new FileData("/roms/gb/Alpha.gb")}; b.root.files = {new FileData("/roms/gb/Alpha.gb")};
    Window w; Server s{&w}; httplib::Request req; req.body = "/roms/gb/Alpha.gb"; httplib::Response res;
    s.launchRoute(req, res);
    printf("launch: the route posted %zu piece(s) of work\n", gPosted.size());
    for (auto sys : SystemData::sSystemVector) { for (auto f : sys->root.files) delete f; sys->root.files = {new FileData("/roms/gb/Alpha.gb")}; }
    printf("launch: the library rebuilt before the interface thread ran the work\n");
    for (auto& f : gPosted) f();
    printf("launch: %d launch(es), the last of '%s'\n", gLaunches, gLaunched.c_str());
    if (gLaunches != 1) bad++;
    for (auto sys : SystemData::sSystemVector) for (auto f : sys->root.files) delete f;
    if (bad) { printf("FAIL S6: %d case(s)\n", bad); return 1; }
    return 0;
}
'''
run(harness, "s6", ("-fsanitize=address,undefined",))
