"""L-22 (#678): GuiLoading's mRunning and result across its two threads, under ThreadSanitizer.

    python3 -I l22-guiloading-race.py <GuiLoading.h> [--control]

The handler interface and the class template are extracted as written (from
`class IGuiLoadingHandler` to GuiLoading's closing `};`) and compiled with -fsanitize=thread over
doubles of GuiComponent, Window, BusyComponent and LambdaAnimation. One
GuiLoading<int> runs a worker returning 42; the test's "interface thread"
calls update() until the page deletes itself and its completion has run. A
data race reported on mRunning or result FAILs the case (TSan's exit 66).
--control declares mRunning std::atomic<bool> (the constructed variant): no
race, the completion receives 42.
"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from t31extract import run  # noqa: E402

src = Path(sys.argv[1]).read_text()
control = "--control" in sys.argv
a = src.index("class IGuiLoadingHandler")
b = src.index("\n};", src.index("class GuiLoading", a)) + 3
cls = src[a:b]
if "bool\t\t\tmRunning;" not in cls and not re.search(r"bool\s+mRunning;", cls):
    sys.exit("FAIL l22: mRunning is no longer a plain bool -- this test models the pin")
if control:
    cls = re.sub(r"bool(\s+)mRunning;", r"std::atomic<bool>\1mRunning;", cls)
harness = r'''
#include <atomic>
#include <chrono>
#include <functional>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
struct Transform4x4f { Transform4x4f operator*(const Transform4x4f&) const { return *this; } };
struct Vector2f { float x = 0, y = 0; };
namespace Renderer { inline int getScreenWidth() { return 640; } inline int getScreenHeight() { return 480; } inline void setMatrix(const Transform4x4f&) {} }
namespace Math { inline float easeOutCubic(float t) { return t; } }
struct Window {};
struct InputConfig {}; struct Input {};
struct LambdaAnimation { LambdaAnimation(std::function<void(float)>, int) {} };
struct GuiComponent {
    Window* mWindow; bool mVisible = true; Vector2f mSize;
    explicit GuiComponent(Window* w) : mWindow(w) {}
    virtual ~GuiComponent() {}
    void setSize(float x, float y) { mSize.x = x; mSize.y = y; }
    void setTag(const char*) {}
    void setAnimation(LambdaAnimation* a, int, std::function<void()>) { delete a; }
    Transform4x4f getTransform() { return Transform4x4f(); }
    void renderChildren(const Transform4x4f&) {}
    virtual void update(int) {}
    virtual void render(const Transform4x4f&) {}
    virtual bool input(InputConfig*, Input) { return false; }
};
struct BusyComponent { explicit BusyComponent(Window*) {} void setText(const std::string&) {} void setSize(Vector2f) {} void setOpacity(unsigned char) {} void render(const Transform4x4f&) {} void update(int) {} };
''' + cls + r'''
int main()
{
    Window w; std::atomic<int> got{0};
    auto* g = new GuiLoading<int>(&w, "PLEASE WAIT",
        [](IGuiLoadingHandler*) { std::this_thread::sleep_for(std::chrono::milliseconds(50)); return 42; },
        [&got](int r) { got = r; });
    for (int i = 0; i < 400 && got == 0; i++) { g->update(16); std::this_thread::sleep_for(std::chrono::milliseconds(1)); }
    std::cout << "completion received " << got << "\n";
    return got == 42 ? 0 : 1;
}
'''
run(harness, "l22", flags=("-fsanitize=thread",))
