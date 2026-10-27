"""L-12 (#680): NetworkThread's posts bypass AppWindow's closing gate.

    python3 -I l12-network-posts.py <NetworkThread.cpp> <AppWindow.h> [--control]

The fork's rule (AppWindow.h, #308 F-ES-26): once main() calls
AppWindow::closing() (main.cpp:1322, the loop ended), every post from a
worker is dropped. NetworkThread's watchers run on es-core's watcher
thread until WatchersManager::stop() (main.cpp:1330), and its five posts
(:206, :237, :251, :257, :266) call `mWindow->postToUiThread` directly. The
harness counts the posts that do not go through AppWindow::post, then runs
the pin's AppWindow.h, included whole, against a window double with the
interface thread's queue: closing() is called, then one post each way. A
direct post lands in a queue no loop will run again (:266's token write is
one such task); a gated one is refused. Asserted: no NetworkThread post
bypasses the gate. At the pin five do. --control rewrites the five as
AppWindow::post(mWindow, ...), the lane's proposed fix, and must PASS.
AppWindow's own case (tests/app-unit/AppWindowTests.cpp) passed in the
stage-C build.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t33extract import run  # noqa: E402

src = Path(sys.argv[1]).read_text()
hdr = Path(sys.argv[2]).read_text()
if "--control" in sys.argv:
    src, n = re.subn(r"mWindow->postToUiThread\(", "AppWindow::post(mWindow, ", src)
    assert n == 5, n
direct = [src.count("\n", 0, m.start()) + 1 for m in re.finditer(r"mWindow->postToUiThread\(", src)]
gated = len(re.findall(r"AppWindow::post\(", src))
print("NetworkThread.cpp: %d direct post(s) at %s; %d through AppWindow::post" % (len(direct), ", ".join(":%d" % l for l in direct) or "-", gated))
harness = hdr + r'''
#include <cstdio>
#include <vector>
struct Window { std::vector<std::function<void()>> mFunctions; void postToUiThread(const std::function<void()>& f) { mFunctions.push_back(f); } };
int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IONBF, 0);
    Window w;
    AppWindow::closing();                 // main.cpp:1322: the loop has ended
    w.postToUiThread([] {});              // a direct post, as NetworkThread's five
    bool posted = AppWindow::post(&w, [] {});
    printf("after closing(): the direct post queued (%zu task(s) no loop will run); AppWindow::post %s\n", w.mFunctions.size(), posted ? "posted" : "refused");
    if (argv[1][0] != '0') { printf("FAIL L-12: %s NetworkThread post(s) bypass the closing gate\n", argv[1]); return 1; }
    return 0;
}
'''
run(harness, "l12", ("-fsanitize=address,undefined",), args=(str(len(direct)),))
