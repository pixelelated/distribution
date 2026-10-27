"""S10 (#678, #1252): the image viewer's pool jobs and the viewer they report to.

    python3 -I s10-viewer-guard.py <GuiImageViewer.cpp>

GuiImageViewer::loadPdf is extracted as written (t31extract) and compiled as
a member of a test viewer over doubles: ApiSystem (a page count, and
extractPdfImages answering from a table, slowly), Utils::ThreadPool (one real
thread running the queued items after start(); stop() joins it), the window
(postToUiThread queues; the test runs the queue as the interface thread
would; pushGui records a viewer and deletes a GuiLoading), and GuiLoading (its
work and its completion run in its constructor). The viewer's constructor and
destructor carry the source's own global writes when the source has them
(`g_isGuiImageViewerRunning = true;` / `= false;`), so the pin is modelled
where it differs. Three cases, each its own binary:
  race      viewer A's pool job reads its guard while viewer B is constructed
            on the interface thread (ThreadSanitizer; the pin: a race on the
            global).
  late      A's posted callback is run after A is deleted and B constructed
            (AddressSanitizer; the pin: the global is B's true, and A's grid
            is written after A is gone).
  empty     the first pages extract to nothing (LeakSanitizer; the pin: A
            neither pushed nor deleted, its pool running). After: A deleted
            and one toast, COULDN'T OPEN THIS FILE.
loadCbz has the same two guards and the same completion; it is not run here
(its file list needs a zip reader the doubles do not have), and is read.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import function  # noqa: E402

src = Path(sys.argv[1]).read_text()
load = function(src, r"^void GuiImageViewer::loadPdf\(const std::string& imagePath\)", "s10").replace("GuiImageViewer::loadPdf", "Viewer::loadPdf", 1)
ctor_global = "g_isGuiImageViewerRunning = true;" in src
dtor_global = "g_isGuiImageViewerRunning = false;" in src

prelude = r'''
#include <atomic>
#include <chrono>
#include <deque>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
#define _(x) std::string(x)
static bool g_isGuiImageViewerRunning = false;
static std::vector<std::string> gToasts;
static std::map<int, std::vector<std::string>> gPages;   // first page -> what it extracts to
static int gPageCount = 3;
struct GuiComponent;
struct Window {
    std::mutex m; std::deque<std::function<void()>> posted; std::vector<GuiComponent*> pushed;
    void postToUiThread(const std::function<void()>& f) { std::lock_guard<std::mutex> g(m); posted.push_back(f); }
    size_t queued() { std::lock_guard<std::mutex> g(m); return posted.size(); }
    void runPosted() { std::deque<std::function<void()>> q; { std::lock_guard<std::mutex> g(m); q.swap(posted); } for (auto& f : q) f(); }
    void pushGui(GuiComponent* g);
    void displayNotificationMessage(const std::string& t, int = -1) { gToasts.push_back(t); }
};
struct GuiComponent { Window* mWindow; explicit GuiComponent(Window* w) : mWindow(w) {} virtual ~GuiComponent() {} };
struct ApiSystem {
    static ApiSystem* getInstance() { static ApiSystem a; return &a; }
    int getPdfPageCount(const std::string&) { return gPageCount; }
    std::vector<std::string> extractPdfImages(const std::string&, int start, int) {
        std::this_thread::sleep_for(std::chrono::milliseconds(30));
        auto it = gPages.find(start); return it == gPages.end() ? std::vector<std::string>() : it->second;
    }
};
namespace Utils {
struct ThreadPool {
    std::vector<std::function<void()>> items; std::thread t;
    ThreadPool(const char*, int) {}
    void queueWorkItem(const std::function<void()>& f) { items.push_back(f); }
    void start() { t = std::thread([this] { for (auto& f : items) f(); }); }
    void stop() { if (t.joinable()) t.join(); }
};
}
template <typename T>
struct GuiLoading : GuiComponent {
    GuiLoading(Window* w, const std::string&, const std::function<T(GuiComponent*)>& work, const std::function<void(T)>& done) : GuiComponent(w) { T r = work(this); done(r); }
};
struct Grid {
    std::map<std::string, std::string> images;
    void add(const std::string&, const std::string&, const std::string& key) { images[key] = ""; }
    void setImage(const std::string& path, const std::string& key) { images[key] = path; }
};
struct Viewer : GuiComponent {
    Grid mGrid; Utils::ThreadPool* mPdfThreads = nullptr; std::string mPdf;
    std::shared_ptr<int> mLifeToken = std::make_shared<int>(0);
    explicit Viewer(Window* w) : GuiComponent(w) { ''' + ("g_isGuiImageViewerRunning = true;" if ctor_global else "") + r''' }
    ~Viewer() { ''' + ("g_isGuiImageViewerRunning = false;" if dtor_global else "") + r''' if (mPdfThreads) { mPdfThreads->stop(); delete mPdfThreads; } }
    void loadPdf(const std::string& imagePath);
};
static std::vector<Viewer*> gPushedViewers;
void Window::pushGui(GuiComponent* g) { if (auto* v = dynamic_cast<Viewer*>(g)) gPushedViewers.push_back(v); else delete g; }
''' + load + "\n"

cases = {
"race": (("-fsanitize=thread",), r'''
int main() {
    Window w; gPages = { {1, {"p1.png"}}, {2, {"p2.png"}}, {3, {"p3.png"}} };
    Viewer* a = new Viewer(&w); a->loadPdf("a.pdf");          // pool job for pages 2 and 3 running
    std::this_thread::sleep_for(std::chrono::milliseconds(35));
    Viewer* b = new Viewer(&w);                                // the interface thread opens another viewer
    a->mPdfThreads->stop(); w.runPosted();
    delete b; delete a;
    std::cout << "race: ran" << std::endl;
}'''),
"late": (("-fsanitize=address",), r'''
int main() {
    Window w; gPages = { {1, {"p1.png"}}, {2, {"p2.png"}}, {3, {"p3.png"}} };
    Viewer* a = new Viewer(&w); a->loadPdf("a.pdf");
    a->mPdfThreads->stop();                                    // its jobs have posted
    std::cout << "late: " << w.queued() << " callback(s) queued for A" << std::endl;
    delete a;                                                  // A closed
    Viewer* b = new Viewer(&w);                                // B open
    w.runPosted();                                             // A's callbacks delivered now
    std::cout << "late: callbacks returned" << std::endl;
    delete b;
}'''),
"empty": (("-fsanitize=address",), r'''
int main() {
    Window w; gPages = { {2, {"p2.png"}}, {3, {"p3.png"}} };   // the first page extracts to nothing
    Viewer* a = new Viewer(&w); a->loadPdf("a.pdf");
    std::this_thread::sleep_for(std::chrono::milliseconds(150));
    w.runPosted();
    std::cout << "empty: pushed " << gPushedViewers.size() << ", toasts " << gToasts.size();
    for (auto& t : gToasts) std::cout << " [" << t << "]";
    std::cout << std::endl;
    return gPushedViewers.empty() && gToasts.size() == 1 && gToasts[0] == "COULDN'T OPEN THIS FILE." ? 0 : 3;
}'''),
}
failed = 0
with tempfile.TemporaryDirectory(prefix="s10-", dir="/workspace/tmp/m6-t31/tmp") as d:
    d = Path(d)
    for name, (flags, main) in cases.items():
        (d / (name + ".cpp")).write_text(prelude + main)
        b = subprocess.run(["g++", "-std=c++17", "-O0", "-g", *flags, str(d / (name + ".cpp")), "-o", str(d / name), "-pthread"], capture_output=True, text=True)
        if b.returncode:
            print("FAIL s10 %s: does not compile\n%s" % (name, b.stderr[-1500:])); failed += 1; continue
        env = dict(os.environ, ASAN_OPTIONS="detect_leaks=1", TSAN_OPTIONS="halt_on_error=0")
        r = subprocess.run([str(d / name)], capture_output=True, text=True, timeout=60, env=env)
        heads = [l for l in r.stderr.splitlines() if l.startswith(("WARNING: ThreadSanitizer", "SUMMARY:", "==") ) and ("ERROR" in l or "SUMMARY" in l or "WARNING" in l)]
        print(r.stdout.strip())
        for h in heads[:3]:
            print("  " + h.split("/workspace/tmp")[0].strip())
        ok = r.returncode == 0
        print(("ok   " if ok else "FAIL ") + "%s (rc %d)" % (name, r.returncode))
        failed += 0 if ok else 1
if failed:
    print("FAIL s10: %d of %d cases" % (failed, len(cases))); sys.exit(1)
print("s10: PASS, %d cases" % len(cases))
